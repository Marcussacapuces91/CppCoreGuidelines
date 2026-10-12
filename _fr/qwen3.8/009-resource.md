# <a name="s-resource"></a>R: Gestion des ressources

Cette section contient des règles relatives aux ressources.
Une ressource est tout ce qui doit être acquis puis (explicitement ou implicitement) libéré, comme la mémoire, les descripteurs de fichiers, les sockets ou les verrous.
La raison pour laquelle elle doit être libérée est généralement qu'elle peut être en quantité limitée, si bien qu'un libérer retardé pourrait être préjudiciable.
L'objectif fondamental est de garantir que nous ne fuyons aucune ressource et que nous ne retenons une ressource plus longtemps que nécessaire.
Une entité qui est responsable de la libération d'une ressource est appelée *propriétaire* (owner).

Il existe quelques cas où des fuites peuvent être acceptables, voire optimales :
si vous écrivez un programme qui se contente de produire une sortie à partir d'une entrée et que la quantité de mémoire nécessaire est proportionnelle à la taille de l'entrée, la stratégie optimale (en termes de performances et de simplicité de programmation) est parfois tout simplement de ne jamais rien supprimer.
Si vous avez suffisamment de mémoire pour traiter votre plus grande entrée, fuyez, mais assurez-vous d'afficher un bon message d'erreur si vous avez tort.
Ici, nous ignorons de tels cas.

* Résumé des règles de gestion des ressources :

  * [R.1 : Gérer les ressources automatiquement à l'aide de gestionnaires de ressources et du RAII (Resource Acquisition Is Initialization)](009-resource.md#rr-raii)
  * [R.2 : Dans les interfaces, utiliser des pointeurs bruts pour désigner des objets individuels (uniquement)](009-resource.md#rr-use-ptr)
  * [R.3 : Un pointeur brut (un `T*`) est non-propriétaire](009-resource.md#rr-ptr)
  * [R.4 : Une référence brute (un `T&`) est non-propriétaire](009-resource.md#rr-ref)
  * [R.5 : Privilégier les objets au portée, ne pas allouer sur le tas inutilement](009-resource.md#rr-scoped)
  * [R.6 : Éviter les variables globales non `const`](009-resource.md#rr-global)

* Résumé des règles d'allocation et de libération :

  * [R.10 : Éviter `malloc()` et `free()`](009-resource.md#rr-mallocfree)
  * [R.11 : Éviter d'appeler `new` et `delete` explicitement](009-resource.md#rr-newdelete)
  * [R.12 : Transférer immédiatement le résultat d'une allocation de ressource explicite à un objet gestionnaire](009-resource.md#rr-immediate-alloc)
  * [R.13 : Effectuer au plus une seule allocation de ressource explicite dans une instruction d'expression unique](009-resource.md#rr-single-alloc)
  * [R.14 : Éviter les paramètres `[]`, privilégier `span`](009-resource.md#rr-ap)
  * [R.15 : Surcharger toujours des paires appariées d'allocation/libération](009-resource.md#rr-pair)

* <a name="rr-summary-smartptrs"></a>Résumé des règles sur les pointeurs intelligents :

  * [R.20 : Utiliser `unique_ptr` ou `shared_ptr` pour représenter la propriété](009-resource.md#rr-owner)
  * [R.21 : Privilégier `unique_ptr` plutôt que `shared_ptr`, sauf si vous devez partager la propriété](009-resource.md#rr-unique)
  * [R.22 : Utiliser `make_shared()` pour créer des `shared_ptr`](009-resource.md#rr-make_shared)
  * [R.23 : Utiliser `make_unique()` pour créer des `unique_ptr`](009-resource.md#rr-make_unique)
  * [R.24 : Utiliser `std::weak_ptr` pour briser les cycles de `shared_ptr`](009-resource.md#rr-weak_ptr)
  * [R.30 : Accepter des pointeurs intelligents en paramètre uniquement pour exprimer explicitement la sémantique de durée de vie](009-resource.md#rr-smartptrparam)
  * [R.31 : Si vous avez des pointeurs intelligents non `std`, suivre le modèle de base de `std`](009-resource.md#rr-smart)
  * [R.32 : Accepter un paramètre `unique_ptr<widget>` pour exprimer qu'une fonction prend la propriété d'un `widget`](009-resource.md#rr-uniqueptrparam)
  * [R.33 : Accepter un paramètre `unique_ptr<widget>&` pour exprimer qu'une fonction réaffecte le `widget`](009-resource.md#rr-reseat)
  * [R.34 : Accepter un paramètre `shared_ptr<widget>` pour exprimer une propriété partagée](009-resource.md#rr-sharedptrparam-owner)
  * [R.35 : Accepter un paramètre `shared_ptr<widget>&` pour exprimer qu'une fonction pourrait réaffecter le pointeur partagé](009-resource.md#rr-sharedptrparam)
  * [R.36 : Accepter un paramètre `const shared_ptr<widget>&` pour exprimer qu'elle pourrait conserver un compte de référence à l'objet ???](009-resource.md#rr-sharedptrparam-const)
  * [R.37 : Ne pas passer un pointeur ou une référence obtenu à partir d'un pointeur intelligent aliasé](009-resource.md#rr-smartptrget)

### <a name="rr-raii"></a>R.1 : Gérer les ressources automatiquement à l'aide de gestionnaires de ressources et du RAII (Resource Acquisition Is Initialization)

##### Raison

Pour éviter les fuites et la complexité de la gestion manuelle des ressources.
La symétrie imposeur/constructeur-déstructeur du langage C++ reflète la symétrie inhérente aux paires de fonctions d'acquisition/libération de ressources telles que `fopen`/`fclose`, `lock`/`unlock` et `new`/`delete`.
Chaque fois que vous manipulez une ressource qui nécessite des appels de fonctions d'acquisition/libération appariés, encapsulez cette ressource dans un objet qui force l'appariement pour vous — acquérez la ressource dans son constructeur et libérez-la dans son destructeur.

##### Exemple, inadéquat

Considérez :

    void send(X* x, string_view destination)
    {
        auto port = open_port(destination);
        my_mutex.lock();
        // ...
        send(port, x);
        // ...
        my_mutex.unlock();
        close_port(port);
        delete x;
    }

Dans ce code, vous devez vous souvenir de faire `unlock`, `close_port` et `delete` sur tous les chemins d'exécution, et faire chaque opération exactement une fois.
De plus, si l'un des morceaux de code marqués `...` lève une exception, alors `x` est perdu (fuite mémoire) et `my_mutex` reste verrouillé.

##### Exemple

Considérez :

    void send(unique_ptr<X> x, string_view destination)  // x est propriétaire du X
    {
        Port port{destination};            // port est propriétaire du PortHandle
        lock_guard<mutex> guard{my_mutex}; // guard est propriétaire du verrou
        // ...
        send(port, x);
        // ...
    } // déverrouille automatiquement my_mutex et supprime le pointeur dans x

Désormais, tout le nettoyage des ressources est automatique, effectué une seule fois sur tous les chemins d'exécution, que des exceptions surviennent ou non. En prime, la fonction indique désormais explicitement qu'elle prend la propriété du pointeur.

Qu'est-ce que `Port` ? Un wrapper pratique qui encapsule la ressource :

    class Port {
        PortHandle port;
    public:
        Port(string_view destination) : port{open_port(destination)} { }
        ~Port() { close_port(port); }
        operator PortHandle() { return port; }

        // les handles de port ne peuvent généralement pas être clonés, donc désactiver la copie et l'assignation si nécessaire
        Port(const Port&) = delete;
        Port& operator=(const Port&) = delete;
    };

##### Note

Lorsqu'une ressource se comporte mal, c'est-à-dire qu'elle n'est pas représentée par une classe avec un destructeur, encapsulez-la dans une classe ou utilisez [`finally`](013-errors.md#re-finally) @TODO-LINK

**Voir aussi** : [RAII](013-errors.md#re-raii) @TODO-LINK

### <a name="rr-use-ptr"></a>R.2 : Dans les interfaces, utiliser des pointeurs bruts pour désigner des objets individuels (uniquement)

##### Raison

Les tableaux sont mieux représentés par un type de conteneur (par ex. `vector` (propriétaire)) ou un `span` (non-propriétaire).
De tels conteneurs et vues contiennent suffisamment d'informations pour effectuer un contrôle de plage.

##### Exemple, inadéquat

    void f(int* p, int n)   // n est le nombre d'éléments dans p[]
    {
        // ...
        p[2] = 7;   // inadéquat : indexage sur pointeur brut
        // ...
    }

Le compilateur ne lit pas les commentaires, et sans lire le reste du code vous ne savez pas si `p` pointe réellement vers `n` éléments.
Utilisez un `span` à la place.

##### Exemple

    void g(int* p, int fmt)   // affiche *p en utilisant le format #fmt
    {
        // ... utilise uniquement *p et p[0] ...
    }

##### Exception

Les chaînes au style C sont passées comme un simple pointeur vers une séquence de caractères terminée par zéro.
Utilisez `zstring` plutôt que `char*` pour indiquer que vous vous appuyez sur cette convention.

##### Note

Beaucoup d'utilisations actuelles de pointeurs vers un seul élément pourraient être des références.
Cependant, lorsque `nullptr` est une valeur possible, une référence pourrait ne pas être une alternative raisonnable.

##### Contrôle

* Signaler l'arithmétique sur pointeurs (y compris `++`) sur un pointeur qui ne fait pas partie d'un conteneur, d'une vue ou d'un itérateur.
  Cette règle générerait un nombre énorme de faux positifs si elle était appliquée à une base de code ancienne.
* Signaler les noms de tableaux passés comme simples pointeurs

### <a name="rr-ptr"></a>R.3 : Un pointeur brut (un `T*`) est non-propriétaire

##### Raison

Rien (dans le standard C++ ni dans la majorité du code) ne dit le contraire et la plupart des pointeurs bruts sont non-propriétaires.
Nous voulons que les pointeurs propriétaires soient identifiés afin que nous puissions supprimer de manière fiable et efficace les objets pointés par les pointeurs propriétaires.

##### Exemple

    void f()
    {
        int* p1 = new int{7};           // inadéquat : pointeur brut propriétaire
        auto p2 = make_unique<int>(7);  // correct : l'int est propriétaire par un pointeur unique
        // ...
    }

Le `unique_ptr` protège contre les fuites en garantissant la suppression de son objet (même en présence d'exceptions). Le `T*` ne le fait pas.

##### Exemple

    template<typename T>
    class X {
    public:
        T* p;   // inadéquat : il est incertain que p soit propriétaire ou non
        T* q;   // inadéquat : il est incertain que q soit propriétaire ou non
        // ...
    };

Nous pouvons corriger ce problème en rendant la propriété explicite :

    template<typename T>
    class X2 {
    public:
        owner<T*> p;  // correct : p est propriétaire
        T* q;         // correct : q n'est pas propriétaire
        // ...
    };

##### Exception

Une grande classe d'exceptions est le code hérité (legacy), en particulier le code qui doit rester compilable en C ou faire interface avec C et le C++ au style C via des ABI.
Le fait qu'il existe des milliards de lignes de code qui violent cette règle concernant les `T*` propriétaires ne peut être ignoré.
Nous aimerions voir des outils de transformation de programmes transformer le code « hérité » de 20 ans en code moderne et éclatant,
nous encourageons le développement, le déploiement et l'utilisation de tels outils,
nous espérons que les lignes directrices aideront au développement de tels outils,
et nous avons même contribué (et contribuons) à la recherche et au développement dans ce domaine.
Cependant, cela prendra du temps : le code « hérité » est généré plus vite que nous ne pouvons rénover l'ancien code, et ce sera le cas pendant quelques années encore.

Ce code ne peut pas tous être réécrit (même en supposant un bon logiciel de transformation de code), surtout pas rapidement.
Ce problème ne peut pas être résolu (à grande échelle) en transformant tous les pointeurs propriétaires en `unique_ptr` et `shared_ptr`,
partiellement parce que nous avons besoin/utilisons des « pointeurs bruts » propriétaires ainsi que de simples pointeurs dans l'implémentation de nos gestionnaires de ressources fondamentaux.
Par exemple, les implémentations courantes de `vector` ont un pointeur propriétaire et deux pointeurs non-propriétaires.
Beaucoup d'ABI (et essentiellement toutes les interfaces avec du code C) utilisent des `T*`, certains propriétaires.
Certaines interfaces ne peuvent pas être simplement annotées avec `owner` parce qu'elles doivent rester compilables en C
(bien que ce serait un bon cas d'utilisation rare pour une macro qui se développe en `owner` uniquement en mode C++).

##### Note

`owner<T*>` n'a pas de sémantique au-delà de `T*`. Il peut être utilisé sans modifier le code qui l'utilise et sans affecter les ABI.
C'est simplement un indicateur pour les programmeurs et les outils d'analyse.
Par exemple, si un `owner<T*>` est un membre d'une classe, cette classe devrait avoir un destructeur qui fait `delete` dessus.

##### Exemple, inadéquat

Retourner un pointeur (brut) impose au caller une incertitude de gestion de durée de vie : qui supprime l'objet pointé ?

    Gadget* make_gadget(int n)
    {
        auto p = new Gadget{n};
        // ...
        return p;
    }

    void caller(int n)
    {
        auto p = make_gadget(n);   // ne pas oublier de supprimer p
        // ...
        delete p;
    }

En plus de souffrir du problème de [fuite](004-philosophy.md#rp-leak) @TODO-LINK, cela ajoute une opération d'allocation et de libération superflue, et est inutilement verbeux. Si Gadget est peu coûteux à déplacer depuis une fonction (c'est-à-dire qu'il est petit ou a une opération de déplacement efficace), renvoyez-le simplement « par valeur » (voir [valeurs de retour « out »](006-functions.md#rf-out) @TODO-LINK) :

    Gadget make_gadget(int n)
    {
        Gadget g{n};
        // ...
        return g;
    }

##### Note

Cette règle s'applique aux fonctions fabriques.

##### Note

Si des sémantiques de pointeur sont requises (par ex. parce que le type de retour doit référencer une classe de base d'une hiérarchie de classes (une interface)), retournez un « pointeur intelligent ».

##### Contrôle

* (Simple) Alerter sur `delete` d'un pointeur brut qui n'est pas un `owner<T>`.
* (Modéré) Alerter sur l'échec de faire `reset` ou `delete` explicitement un pointeur `owner<T>` sur tous les chemins d'exécution.
* (Simple) Alerter si la valeur de retour de `new` est assignée à un pointeur brut.
* (Simple) Alerter si une fonction retourne un objet qui a été alloué dans la fonction mais qui a un constructeur de déplacement.
  Suggérer d'envisager de le retourner par valeur à la place.

### <a name="rr-ref"></a>R.4 : Une référence brute (un `T&`) est non-propriétaire

##### Raison

Rien (dans le standard C++ ni dans la majorité du code) ne dit le contraire et la plupart des références brutes sont non-propriétaires.
Nous voulons que les propriétaires soient identifiés afin que nous puissions supprimer de manière fiable et efficace les objets pointés par les pointeurs propriétaires.

##### Exemple

    void f()
    {
        int& r = *new int{7};  // inadéquat : référence brute propriétaire
        // ...
        delete &r;             // inadéquat : violation de la règle contre la suppression de pointeurs bruts
    }

**Voir aussi** : [la règle des pointeurs bruts](009-resource.md#rr-ptr)

##### Contrôle

Voir [la règle des pointeurs bruts](009-resource.md#rr-ptr)

### <a name="rr-scoped"></a>R.5 : Privilégier les objets à portée, ne pas allouer sur le tas inutilement

##### Raison

Un objet à portée est un objet local, un objet global ou un membre.
Cela implique qu'il n'y a pas de coût supplémentaire d'allocation et de libération au-delà de celui déjà utilisé pour la portée ou l'objet contenant.
Les membres d'un objet à portée sont eux-mêmes à portée, et le constructeur et le destructeur de l'objet à portée gèrent les durées de vie des membres.

##### Exemple

L'exemple suivant est inefficace (car il a des opérations d'allocation et de libération inutiles), vulnérable aux exceptions et retours dans la partie `...` (conduisant à des fuites), et verbeux :

    void f(int n)
    {
        auto p = new Gadget{n};
        // ...
        delete p;
    }

Au lieu de cela, utilisez une variable locale :

    void f(int n)
    {
        Gadget g{n};
        // ...
    }

##### Contrôle

* (Modéré) Alerter si un objet est alloué puis libéré sur tous les chemins dans une fonction. Suggérer qu'il devrait être un objet local sur la pile.
* (Simple) Alerter si un `Unique_pointer` ou `Shared_pointer` local qui n'est ni déplacé, ni copié, ni réassigné, ni `reset` avant la fin de sa durée de vie n'est pas déclaré `const`.
Exception : ne pas générer un tel avertissement sur un `Unique_pointer` local vers un tableau non borné. (Voir ci-dessous.)

##### Exception

Si votre espace de pile est limité, il est acceptable de créer un `const unique_ptr<BigObject>` local pour stocker l'objet sur le tas plutôt que sur la pile.

### <a name="rr-global"></a>R.6 : Éviter les variables globales non `const`

Voir [I.2](005-interfaces.md#ri-global) @TODO-LINK

## <a name="ss-alloc"></a>R.alloc : Allocation et libération

### <a name="rr-mallocfree"></a>R.10 : Éviter `malloc()` et `free()`

##### Raison

`malloc()` et `free()` ne prennent pas en charge la construction et la destruction, et ne se combinent pas bien avec `new` et `delete`.

##### Exemple

    class Record {
        int id;
        string name;
        // ...
    };

    void use()
    {
        // p1 pourrait être nullptr
        // *p1 n'est pas initialisé ; en particulier,
        // cette string n'est pas une string, mais un sac de bits de la taille d'une string
        Record* p1 = static_cast<Record*>(malloc(sizeof(Record)));

        auto p2 = new Record;

        // sauf si une exception est levée, *p2 est initialisé par défaut
        auto p3 = new(nothrow) Record;
        // p3 pourrait être nullptr ; si ce n'est pas le cas, *p3 est initialisé par défaut

        // ...

        delete p1;    // erreur : ne peut pas supprimer un objet alloué par malloc()
        free(p2);    // erreur : ne peut pas free() un objet alloué par new
    }

Dans certaines implémentations, ce `delete` et ce `free()` pourraient fonctionner, ou peut-être causer-ils des erreurs d'exécution.

##### Exception

Il existe des applications et des sections de code où les exceptions ne sont pas acceptables.
Certains des meilleurs exemples de ce type se trouvent dans le code temps réel dur à criticité vitale.
Gardez à l'esprit que beaucoup d'interdictions d'utilisation des exceptions sont basées sur la superstition (mauvaise)
ou sur des préoccupations concernant les anciennes bases de code avec une gestion des ressources non systématique (malheureusement, mais parfois nécessaire).
Dans de tels cas, envisagez les versions `nothrow` de `new`.

##### Contrôle

Signaler toute utilisation explicite de `malloc` et `free`.

### <a name="rr-newdelete"></a>R.11 : Éviter d'appeler `new` et `delete` explicitement

##### Raison

Le pointeur retourné par `new` devrait appartenir à un gestionnaire de ressources (qui peut appeler `delete`).
Si le pointeur retourné par `new` est assigné à un pointeur simple/nu, l'objet peut être perdu (fuite mémoire).

##### Note

Dans un grand programme, un `delete` nu (c'est-à-dire un `delete` dans le code applicatif, plutôt que dans du code dédié à la gestion des ressources)
est un bug probable : si vous avez N `delete`, comment pouvez-vous être certain de n'en avoir pas besoin N+1 ou N-1 ?
Le bug pourrait être latent : il pourrait ne se manifester qu'au cours de la maintenance.
Si vous avez un `new` nu, vous avez probablement besoin d'un `delete` nu quelque part, donc vous avez probablement un bug.

##### Contrôle

(Simple) Alerter sur toute utilisation explicite de `new` et `delete`. Suggérer d'utiliser `make_unique` à la place.

### <a name="rr-immediate-alloc"></a>R.12 : Transférer immédiatement le résultat d'une allocation de ressource explicite à un objet gestionnaire

##### Raison

Sinon, une exception ou un retour pourrait provoquer une fuite.

##### Exemple, inadéquat

    void func(const string& name)
    {
        FILE* f = fopen(name, "r");            // ouvrir le fichier
        vector<char> buf(1024);
        auto _ = finally([f] { fclose(f); });  // se souvenir de fermer le fichier
        // ...
    }

L'allocation de `buf` pourrait échouer et provoquer une fuite du descripteur de fichier.

##### Exemple

    void func(const string& name)
    {
        ifstream f{name};   // ouvrir le fichier
        vector<char> buf(1024);
        // ...
    }

L'utilisation du descripteur de fichier (dans `ifstream`) est simple, efficace et sûre.

##### Contrôle

* Signaler les allocations explicites utilisées pour initialiser des pointeurs (problème : combien d'allocations de ressources directes pouvons-nous reconnaître ?)

### <a name="rr-single-alloc"></a>R.13 : Effectuer au plus une seule allocation de ressource explicite dans une instruction d'expression unique

##### Raison

Si vous effectuez deux allocations de ressources explicites dans une seule instruction, vous pourriez provoquer des fuites de ressources car l'ordre d'évaluation de nombreuses sous-expressions, y compris les arguments de fonction, n'est pas spécifié.

##### Exemple

    void fun(shared_ptr<Widget> sp1, shared_ptr<Widget> sp2);

Cette fonction `fun` peut être appelée ainsi :

    // INADÉQUAT : fuite potentielle
    fun(shared_ptr<Widget>(new Widget(a, b)), shared_ptr<Widget>(new Widget(c, d)));

Cela n'est pas sûr face aux exceptions car le compilateur pourrait réordonner les deux expressions qui construisent les deux arguments de la fonction.
En particulier, le compilateur peut entremêler l'exécution des deux expressions :
l'allocation mémoire (en appelant `operator new`) pourrait être effectuée en premier pour les deux objets, suivie des tentatives d'appel des deux constructeurs `Widget`.
Si l'un des appels de constructeur lève une exception, alors la mémoire de l'autre objet ne sera jamais libérée !

Ce problème subtil a une solution simple : ne jamais effectuer plus d'une seule allocation de ressource explicite dans une instruction d'expression unique.
Par exemple :

    shared_ptr<Widget> sp1(new Widget(a, b)); // Mieux, mais maladroit
    fun(sp1, new Widget(c, d));

La meilleure solution est d'éviter toute allocation explicite, en utilisant des fonctions fabriques qui retournent des objets propriétaires :

    fun(make_shared<Widget>(a, b), make_shared<Widget>(c, d)); // Meilleur

Écrivez votre propre wrapper fabrique s'il n'en existe pas déjà.

##### Contrôle

* Signaler les expressions avec plusieurs allocations de ressources explicites (problème : combien d'allocations de ressources directes pouvons-nous reconnaître ?)

### <a name="rr-ap"></a>R.14 : Éviter les paramètres `[]`, privilégier `span`

##### Raison

Un tableau se dégrade en pointeur, perdant ainsi sa taille, ouvrant la porte aux erreurs de plage.
Utilisez `span` pour préserver l'information de taille.

##### Exemple

    void f(int[]);          // déconseillé

    void f(int*);           // déconseillé pour plusieurs objets
                            // (un pointeur devrait pointer vers un seul objet, ne pas indexer)

    void f(gsl::span<int>); // bon, recommandé

##### Contrôle

Signaler les paramètres `[]`. Utiliser `span` à la place.

### <a name="rr-pair"></a>R.15 : Surcharger toujours des paires appariées d'allocation/libération

##### Raison

Sinon vous obtenez des opérations non appariées et le chaos.

##### Exemple

    class X {
        // ...
        void* operator new(size_t s);
        void operator delete(void*);
        // ...
    };

##### Note

Si vous voulez de la mémoire qui ne peut pas être libérée, faites `=delete` sur l'opération de libération.
Ne la laissez pas non déclarée.

##### Contrôle

Signaler les paires incomplètes.

## <a name="ss-smart"></a>R.smart : Pointeurs intelligents

### <a name="rr-owner"></a>R.20 : Utiliser `unique_ptr` ou `shared_ptr` pour représenter la propriété

##### Raison

Ils peuvent empêcher les fuites de ressources.

##### Exemple

Considérez :

    void f()
    {
        X* p1 { new X };              // inadéquat, p1 fuit
        auto p2 = make_unique<X>();   // correct, propriété unique
        auto p3 = make_shared<X>();   // correct, propriété partagée
    }

Cela provoque une fuite de l'objet utilisé pour initialiser `p1` (uniquement).

##### Contrôle

* (Simple) Alerter si la valeur de retour de `new` est assignée à un pointeur brut.
* (Simple) Alerter si le résultat d'une fonction retournant un pointeur brut propriétaire est assigné à un pointeur brut.

### <a name="rr-unique"></a>R.21 : Privilégier `unique_ptr` plutôt que `shared_ptr`, sauf si vous devez partager la propriété

##### Raison

Un `unique_ptr` est conceptuellement plus simple et plus prévisible (vous savez quand la destruction se produit) et plus rapide (vous ne maintenez pas implicitement un compteur d'utilisation).

##### Exemple, inadéquat

Cela ajoute et maintient inutilement un compteur de référence.

    void f()
    {
        shared_ptr<Base> base = make_shared<Derived>();
        // utiliser base localement, sans le copier -- le compteur ne dépasse jamais 1
    } // détruire base

##### Exemple

Ceci est plus efficace :

    void f()
    {
        unique_ptr<Base> base = make_unique<Derived>();
        // utiliser base localement
    } // détruire base

##### Contrôle

(Simple) Alerter si une fonction utilise un `Shared_pointer` avec un objet alloué dans la fonction, mais ne retourne jamais le `Shared_pointer` ni ne le passe à une fonction nécessitant un `Shared_pointer`. Suggérer d'utiliser `unique_ptr` à la place.

### <a name="rr-make_shared"></a>R.22 : Utiliser `make_shared()` pour créer des `shared_ptr`

##### Raison

`make_shared` donne une déclaration plus concise de la construction.
Il offre également la possibilité d'éliminer une allocation séparée pour les compteurs de référence, en plaçant les compteurs d'utilisation du `shared_ptr` à côté de son objet.
Il garantit également la sécurité face aux exceptions dans les expressions complexes (dans le code antérieur à C++17).

##### Exemple

Considérez :

    shared_ptr<X> p1 { new X{2} }; // inadéquat
    auto p = make_shared<X>(2);    // correct

La version `make_shared()` mentionne `X` une seule fois, donc elle est généralement plus courte (ainsi que plus rapide) que la version avec `new` explicite.

##### Contrôle

(Simple) Alerter si un `shared_ptr` est construit à partir du résultat de `new` plutôt que `make_shared`.

### <a name="rr-make_unique"></a>R.23 : Utiliser `make_unique()` pour créer des `unique_ptr`

##### Raison

`make_unique` donne une déclaration plus concise de la construction.
Il garantit également la sécurité face aux exceptions dans les expressions complexes (dans le code antérieur à C++17).

##### Exemple

    unique_ptr<Foo> p {new Foo{7}};    // correct : mais répétitif

    auto q = make_unique<Foo>(7);      // Mieux : pas de répétition de Foo

##### Contrôle

(Simple) Alerter si un `unique_ptr` est construit à partir du résultat de `new` plutôt que `make_unique`.

### <a name="rr-weak_ptr"></a>R.24 : Utiliser `std::weak_ptr` pour briser les cycles de `shared_ptr`

##### Raison

Les `shared_ptr` reposent sur le comptage d'utilisation et le compteur d'utilisation d'une structure cyclique n'atteint jamais zéro, il faut donc un mécanisme pour
pouvoir détruire une structure cyclique.

##### Exemple

    #include <memory>

    class bar;

    class foo {
    public:
      explicit foo(const std::shared_ptr<bar>& forward_reference)
        : forward_reference_(forward_reference)
      { }
    private:
      std::shared_ptr<bar> forward_reference_;
    };

    class bar {
    public:
      explicit bar(const std::weak_ptr<foo>& back_reference)
        : back_reference_(back_reference)
      { }
      void do_something()
      {
        if (auto shared_back_reference = back_reference_.lock()) {
          // Utiliser *shared_back_reference
        }
      }
    private:
      std::weak_ptr<foo> back_reference_;
    };

##### Note

??? (HS : Beaucoup de gens disent « pour briser les cycles », alors que je pense que « propriété partagée temporaire » est plus à propos.)
???(BS : briser les cycles est ce qu'il faut faire ; partager temporairement la propriété est la façon de le faire.
On pourrait « partager temporairement la propriété » simplement en utilisant un autre `shared_ptr`.)

##### Contrôle

??? probablement impossible. Si nous pouvions détecter statiquement les cycles, nous n'aurions pas besoin de `weak_ptr`

### <a name="rr-smartptrparam"></a>R.30 : Accepter des pointeurs intelligents en paramètre uniquement pour exprimer explicitement la sémantique de durée de vie

Voir [F.7](006-functions.md#rf-smart) @TODO-LINK.

### <a name="rr-smart"></a>R.31 : Si vous avez des pointeurs intelligents non `std`, suivre le modèle de base de `std`

##### Raison

Les règles de la section suivante fonctionnent également pour d'autres types de pointeurs intelligents tierce partie ou sur mesure, et sont très utiles pour diagnostiquer les erreurs courantes de pointeurs intelligents qui causent des problèmes de performances et de correction.
Vous voulez que les règles fonctionnent sur tous les pointeurs intelligents que vous utilisez.

Tout type (y compris un gabarit primaire ou une spécialisation) qui surcharge l'opérateur unaire `*` et `->` est considéré comme un pointeur intelligent :

* S'il est copiable, il est reconnu comme un `shared_ptr` à comptage de référence.
* S'il n'est pas copiable, il est reconnu comme un `unique_ptr` unique.

##### Exemple, inadéquat

    // utiliser le intrusive_ptr de Boost
    #include <boost/intrusive_ptr.hpp>
    void f(boost::intrusive_ptr<widget> p)  // erreur selon la règle 'sharedptrparam'
    {
        p->foo();
    }

    // utiliser le CComPtr de Microsoft
    #include <atlbase.h>
    void f(CComPtr<widget> p)               // erreur selon la règle 'sharedptrparam'
    {
        p->foo();
    }

Les deux cas sont une erreur selon la [ligne directrice `sharedptrparam`](009-resource.md#rr-smartptrparam) :
`p` est un `Shared_pointer`, mais rien dans sa nature partagée n'est utilisé ici et le passer par valeur est une pessimisation silencieuse ;
ces fonctions ne devraient accepter un pointeur intelligent que s'il ont besoin de participer à la gestion de durée de vie du widget. Sinon, elles devraient accepter un `widget*`, s'il peut être `nullptr`. Sinon, et idéalement, la fonction devrait accepter un `widget&`.
Ces pointeurs intelligents correspondent au concept de `Shared_pointer`, donc ces règles de contrôle des lignes directrices fonctionnent sur eux dès le départ et exposent cette pessimisation courante.

### <a name="rr-uniqueptrparam"></a>R.32 : Accepter un paramètre `unique_ptr<widget>` pour exprimer qu'une fonction prend la propriété d'un `widget`

##### Raison

Utiliser `unique_ptr` de cette façon documente et applique à la fois le transfert de propriété de l'appel de fonction.

##### Exemple

    void sink(unique_ptr<widget>); // prend la propriété du widget

    void uses(widget*);            // utilise simplement le widget

##### Contrôle

* (Simple) Alerter si une fonction accepte un paramètre `Unique_pointer<T>` par référence à valeur et ne lui assigne pas ou n'appelle pas `reset()` dessus sur au moins un chemin d'exécution. Suggérer d'accepter un `T*` ou `T&` à la place.

### <a name="rr-reseat"></a>R.33 : Accepter un paramètre `unique_ptr<widget>&` pour exprimer qu'une fonction réaffecte le `widget`

##### Raison

Utiliser `unique_ptr` de cette façon documente et applique à la fois les sémantiques de réaffectation de l'appel de fonction.

##### Note

« Réaffecter » (reseat) signifie « faire qu'un pointeur ou un pointeur intelligent référence un objet différent. »

##### Exemple

    void reseat(unique_ptr<widget>&); // « fera » ou « pourrait » réaffecter le pointeur

##### Contrôle

* (Simple) Alerter si une fonction accepte un paramètre `Unique_pointer<T>` par référence à valeur et ne lui assigne pas ou n'appelle pas `reset()` dessus sur au moins un chemin d'exécution. Suggérer d'accepter un `T*` ou `T&` à la place.

### <a name="rr-sharedptrparam-owner"></a>R.34 : Accepter un paramètre `shared_ptr<widget>` pour exprimer une propriété partagée

##### Raison

Cela rend le partage de propriété de la fonction explicite.

##### Exemple, bon

    class WidgetUser
    {
    public:
        // WidgetUser partagera la propriété du widget
        explicit WidgetUser(std::shared_ptr<widget> w) noexcept:
            m_widget{std::move(w)} {}
        // ...
    private:
        std::shared_ptr<widget> m_widget;
    };

##### Contrôle

* (Simple) Alerter si une fonction accepte un paramètre `Shared_pointer<T>` par référence à valeur et ne lui assigne pas ou n'appelle pas `reset()` dessus sur au moins un chemin d'exécution. Suggérer d'accepter un `T*` ou `T&` à la place.
* (Simple) ((Foundation)) Alerter si une fonction accepte un `Shared_pointer<T>` par valeur ou par référence à `const` et ne le copie ni ne le déplace dans un autre `Shared_pointer` sur au moins un chemin d'exécution. Suggérer d'accepter un `T*` ou `T&` à la place.
* (Simple) ((Foundation)) Alerter si une fonction accepte un `Shared_pointer<T>` par référence à valeur éphémère (rvalue reference). Suggérer de l'accepter par valeur à la place.

### <a name="rr-sharedptrparam"></a>R.35 : Accepter un paramètre `shared_ptr<widget>&` pour exprimer qu'une fonction pourrait réaffecter le pointeur partagé

##### Raison

Cela rend la réaffectation de la fonction explicite.

##### Note

« Réaffecter » (reseat) signifie « faire qu'une référence ou un pointeur intelligent référence un objet différent. »

##### Exemple, bon

    void ChangeWidget(std::shared_ptr<widget>& w)
    {
        // Cela changera le widget de l'appelant
        w = std::make_shared<widget>(widget{});
    }

##### Contrôle

* (Simple) Alerter si une fonction accepte un paramètre `Shared_pointer<T>` par référence à valeur et ne lui assigne pas ou n'appelle pas `reset()` dessus sur au moins un chemin d'exécution. Suggérer d'accepter un `T*` ou `T&` à la place.
* (Simple) ((Foundation)) Alerter si une fonction accepte un `Shared_pointer<T>` par valeur ou par référence à `const` et ne le copie ni ne le déplace dans un autre `Shared_pointer` sur au moins un chemin d'exécution. Suggérer d'accepter un `T*` ou `T&` à la place.
* (Simple) ((Foundation)) Alerter si une fonction accepte un `Shared_pointer<T>` par référence à valeur éphémère (rvalue reference). Suggérer de l'accepter par valeur à la place.

### <a name="rr-sharedptrparam-const"></a>R.36 : Accepter un paramètre `const shared_ptr<widget>&` pour exprimer qu'elle pourrait conserver un compte de référence à l'objet ???

##### Raison

Cela rend le ??? de la fonction explicite.

##### Exemple, bon

    void share(shared_ptr<widget>);            // partager -- « conservera » le compteur de référence

    void reseat(shared_ptr<widget>&);          // « pourrait » réaffecter le pointeur

    void may_share(const shared_ptr<widget>&); // « pourrait » conserver le compteur de référence

##### Contrôle

* (Simple) Alerter si une fonction accepte un paramètre `Shared_pointer<T>` par référence à valeur et ne lui assigne pas ou n'appelle pas `reset()` dessus sur au moins un chemin d'exécution. Suggérer d'accepter un `T*` ou `T&` à la place.
* (Simple) ((Foundation)) Alerter si une fonction accepte un `Shared_pointer<T>` par valeur ou par référence à `const` et ne le copie ni ne le déplace dans un autre `Shared_pointer` sur au moins un chemin d'exécution. Suggérer d'accepter un `T*` ou `T&` à la place.
* (Simple) ((Foundation)) Alerter si une fonction accepte un `Shared_pointer<T>` par référence à valeur éphémère (rvalue reference). Suggérer de l'accepter par valeur à la place.

### <a name="rr-smartptrget"></a>R.37 : Ne pas passer un pointeur ou une référence obtenu à partir d'un pointeur intelligent aliasé

##### Raison

Violer cette règle est la cause numéro un de la perte de compteurs de référence et de la découverte d'un pointeur pendentif (dangling).
Les fonctions devraient préférer passer des pointeurs bruts et des références le long des chaînes d'appels.
Au sommet de l'arbre d'appels où vous obtenez le pointeur brut ou la référence à partir d'un pointeur intelligent qui maintient l'objet en vie.
Vous devez vous assurer que le pointeur intelligent ne peut pas être réaffecté ou réassigné accidentellement depuis l'intérieur de l'arbre d'appels en dessous.

##### Note

Pour ce faire, vous avez parfois besoin de prendre une copie locale d'un pointeur intelligent, qui maintient fermement l'objet en vie pendant la durée de la fonction et de l'arbre d'appels.

##### Exemple

Considérez ce code :

    // global (statique ou tas), ou local aliasé ...
    shared_ptr<widget> g_p = ...;

    void f(widget& w)
    {
        g();
        use(w);  // A
    }

    void g()
    {
        g_p = ...; // oops, si c'était le dernier shared_ptr vers ce widget, détruit le widget
    }

Le suivant ne devrait pas passer une revue de code :

    void my_code()
    {
        // INADÉQUAT : passer un pointeur ou une référence obtenu à partir d'un pointeur intelligent
        //            non local qui pourrait être réaffecté accidentellement quelque part dans f ou ses appelants
        f(*g_p);

        // INADÉQUAT : même raison, juste en le passant comme pointeur « this »
        g_p->func();
    }

La correction est simple — prenez une copie locale du pointeur pour « maintenir un compte de référence » pour votre arbre d'appels :

    void my_code()
    {
        // peu coûteux : 1 incrémentation couvre toute cette fonction et tous les arbres d'appels en dessous
        auto pin = g_p;

        // CORRECT : passer un pointeur ou une référence obtenu à partir d'un pointeur intelligent local non aliasé
        f(*pin);

        // CORRECT : même raison
        pin->func();
    }

##### Contrôle

* (Simple) Alerter si un pointeur ou une référence obtenu à partir d'une variable de pointeur intelligent (`Unique_pointer` ou `Shared_pointer`) qui n'est pas locale, ou qui est locale mais potentiellement aliasée, est utilisé dans un appel de fonction. Si le pointeur intelligent est un `Shared_pointer`, suggérer de prendre une copie locale du pointeur intelligent et d'obtenir un pointeur ou une référence à partir de celle-ci.