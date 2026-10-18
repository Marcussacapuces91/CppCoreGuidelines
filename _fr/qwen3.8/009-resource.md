# <a name="s-resource"></a>R : Gestion des ressources

Cette section contient des règles liées aux ressources.
Une ressource est tout élément qui doit être acquis puis (explicitement ou implicitement) libéré, tel que la mémoire, les descripteurs de fichiers, les sockets ou les verrous.
La raison pour laquelle une ressource doit être libérée est généralement qu'elle est rare, si bien qu'un retard de libération peut causer des dommages.
L'objectif fondamental est de nous assurer de ne pas provoquer de fuite de ressources et de ne pas retenir une ressource plus longtemps que nécessaire.
Une entité responsable de la libération d'une ressource est appelée propriétaire.

Il existe certains cas où les fuites peuvent être acceptables, voire optimales :
si vous écrivez un programme qui produit simplement une sortie à partir d'une entrée et que la quantité de mémoire nécessaire est proportionnelle à la taille de l'entrée, la stratégie optimale (en termes de performance et de facilité de programmation) est parfois tout simplement de ne jamais rien libérer.
Si vous disposez de suffisamment de mémoire pour traiter votre plus grande entrée, laissez fuir, mais assurez-vous d'afficher un bon message d'erreur si vous avez tort.
Ici, nous ignorons de tels cas.

* Résumé des règles de gestion des ressources :

  * [R.1 : Gérer automatiquement les ressources à l'aide de poignées de ressource et du RAII (Resource Acquisition Is Initialization)](009-resource.md#rr-raii)
  * [R.2 : Dans les interfaces, utiliser des pointeurs bruts pour désigner un objet individuel (uniquement)](009-resource.md#rr-use-ptr)
  * [R.3 : Un pointeur brut (un `T*`) est non-propriétaire](009-resource.md#rr-ptr)
  * [R.4 : Une référence brute (un `T&`) est non-propriétaire](009-resource.md#rr-ref)
  * [R.5 : Privilégier les objets bornés par une portée, ne pas allouer sur le tas inutilement](009-resource.md#rr-scoped)
  * [R.6 : Éviter les variables globales non-`const`](009-resource.md#rr-global)

* Résumé des règles d'allocation et de désallocation :

  * [R.10 : Éviter `malloc()` et `free()`](009-resource.md#rr-mallocfree)
  * [R.11 : Éviter d'appeler `new` et `delete` explicitement](009-resource.md#rr-newdelete)
  * [R.12 : Transférer immédiatement le résultat d'une allocation de ressource explicite à un objet gestionnaire](009-resource.md#rr-immediate-alloc)
  * [R.13 : Effectuer au plus une allocation de ressource explicite dans une unique instruction d'expression](009-resource.md#rr-single-alloc)
  * [R.14 : Éviter les paramètres `[]`, préférer `span`](009-resource.md#rr-ap)
  * [R.15 : Toujours surcharger les paires appariées d'allocation/désallocation](009-resource.md#rr-pair)

* <a name="rr-summary-smartptrs"></a>Résumé des règles des pointeurs intelligents :

  * [R.20 : Utiliser `unique_ptr` ou `shared_ptr` pour représenter la propriété](009-resource.md#rr-owner)
  * [R.21 : Préférer `unique_ptr` à `shared_ptr` sauf si le partage de propriété est nécessaire](009-resource.md#rr-unique)
  * [R.22 : Utiliser `make_shared()` pour créer des `shared_ptr`](009-resource.md#rr-make_shared)
  * [R.23 : Utiliser `make_unique()` pour créer des `unique_ptr`](009-resource.md#rr-make_unique)
  * [R.24 : Utiliser `std::weak_ptr` pour briser les cycles de `shared_ptr`](009-resource.md#rr-weak_ptr)
  * [R.30 : N'accepter des pointeurs intelligents en paramètre que pour exprimer explicitement la sémantique de durée de vie](009-resource.md#rr-smartptrparam)
  * [R.31 : Si vous utilisez des pointeurs intelligents non-`std`, suivre le modèle de base de `std`](009-resource.md#rr-smart)
  * [R.32 : Accepter un paramètre `unique_ptr<widget>` pour exprimer qu'une fonction assume la propriété d'un `widget`](009-resource.md#rr-uniqueptrparam)
  * [R.33 : Accepter un paramètre `unique_ptr<widget>&` pour exprimer qu'une fonction réassigne le `widget`](009-resource.md#rr-reseat)
  * [R.34 : Accepter un paramètre `shared_ptr<widget>` pour exprimer un partage de propriété](009-resource.md#rr-sharedptrparam-owner)
  * [R.35 : Accepter un paramètre `shared_ptr<widget>&` pour exprimer qu'une fonction peut réassigner le pointeur partagé](009-resource.md#rr-sharedptrparam)
  * [R.36 : Accepter un paramètre `const shared_ptr<widget>&` pour exprimer qu'il peut conserver un compteur de référence à l'objet ???](009-resource.md#rr-sharedptrparam-const)
  * [R.37 : Ne pas passer un pointeur ou une référence obtenus à partir d'un pointeur intelligent aliasé](009-resource.md#rr-smartptrget)

### <a name="rr-raii"></a>R.1 : Gérer automatiquement les ressources à l'aide de poignées de ressource et du RAII (Resource Acquisition Is Initialization)

##### Justification

Pour éviter les fuites et la complexité de la gestion manuelle des ressources.
La symétrie entre les constructeurs et destructeurs, imposée par le langage C++, reflète la symétrie inhérente aux paires de fonctions d'acquisition/libération de ressources telles que `fopen`/`fclose`, `lock`/`unlock` et `new`/`delete`.
Chaque fois que vous manipulez une ressource nécessitant des appels appariés d'acquisition/libération, encapsulez cette ressource dans un objet qui impose ce couplage à votre place : acquérez la ressource dans son constructeur, et libérez-la dans son destructeur.

##### Exemple non conforme

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

Dans ce code, vous devez vous souvenir d'appeler `unlock`, `close_port` et `delete` sur tous les chemins d'exécution, et chacun exactement une fois.
De plus, si l'une des parties de code marquées `...` lève une exception, alors `x` est perdu (fuite) et `my_mutex` reste verrouillé.

##### Exemple

Considérez :

    void send(unique_ptr<X> x, string_view destination)  // x possède le X
    {
        Port port{destination};            // port possède le PortHandle
        lock_guard<mutex> guard{my_mutex}; // guard possède le verrou
        // ...
        send(port, x);
        // ...
    } // déverrouille automatiquement my_mutex et supprime le pointeur contenu dans x

Dorénavant, tout le nettoyage des ressources est automatique, effectué une fois sur tous les chemins d'exécution, que l'exception se produise ou non. En prime, la fonction indique désormais qu'elle prend la propriété du pointeur.

Qu'est-ce que `Port` ? Un enveloppe pratique qui encapsule la ressource :

    class Port {
        PortHandle port;
    public:
        Port(string_view destination) : port{open_port(destination)} { }
        ~Port() { close_port(port); }
        operator PortHandle() { return port; }

        // les poignées de port ne peuvent généralement pas être clonées,
        // donc désactiver la copie et l'assignation si nécessaire
        Port(const Port&) = delete;
        Port& operator=(const Port&) = delete;
    };

##### Remarque

Lorsqu'une ressource est « mal comportée » en ce sens qu'elle n'est pas représentée par une classe avec un destructeur, enveloppez-la dans une classe ou utilisez [`finally`](013-errors.md#re-finally)

**Voir aussi** : [RAII](013-errors.md#re-raii)

### <a name="rr-use-ptr"></a>R.2 : Dans les interfaces, utiliser des pointeurs bruts pour désigner un objet individuel (uniquement)

##### Justification

Les tableaux sont mieux représentés par un type de conteneur (par exemple `vector` (propriétaire)) ou un `span` (non-propriétaire).
De tels conteneurs et vues contiennent suffisamment d'informations pour effectuer des contrôles de portée.

##### Exemple non conforme

    void f(int* p, int n)   // n est le nombre d'éléments dans p[]
    {
        // ...
        p[2] = 7;   // incorrect : indexation d'un pointeur brut
        // ...
    }

Le compilateur ne lit pas les commentaires, et sans lire le reste du code, vous ne savez pas si `p` pointe réellement vers `n` éléments.
Utilisez un `span` à la place.

##### Exemple

    void g(int* p, int fmt)   // afficher *p en utilisant le format #fmt
    {
        // ... n'utilise que *p et p[0] ...
    }

##### Exception

Les chaînes de caractères au style C sont transmises comme un unique pointeur vers une séquence de caractères terminée par un nul.
Utilisez `zstring` plutôt que `char*` pour indiquer que vous vous appuyez sur cette convention.

##### Remarque

Beaucoup d'usages actuels de pointeurs vers un seul élément pourraient être des références.
Cependant, lorsque `nullptr` est une valeur possible, une référence ne serait pas une alternative raisonnable.

##### Détection

* Signaler l'arithmétique sur pointeurs (y compris `++`) sur un pointeur qui ne fait pas partie d'un conteneur, d'une vue ou d'un itérateur.
  Cette règle générerait un nombre énorme de faux positifs si elle était appliquée à une base de code plus ancienne.
* Signaler les noms de tableaux passés comme simples pointeurs

### <a name="rr-ptr"></a>R.3 : Un pointeur brut (un `T*`) est non-propriétaire

##### Justification

Il n'y a rien (ni dans la norme C++ ni dans la plupart du code) pour dire le contraire, et la plupart des pointeurs bruts sont non-propriétaires.
Nous voulons que les pointeurs propriétaires soient identifiés afin de pouvoir supprimer de manière fiable et efficace les objets pointés par ces derniers.

##### Exemple

    void f()
    {
        int* p1 = new int{7};           // incorrect : pointeur brut propriétaire
        auto p2 = make_unique<int>(7);  // correct : l'int est possédé par un pointeur unique
        // ...
    }

Le `unique_ptr` protège contre les fuites en garantissant la suppression de son objet (même en présence d'exceptions). Le `T*` ne le fait pas.

##### Exemple

    template<typename T>
    class X {
    public:
        T* p;   // incorrect : il n'est pas clair que p soit propriétaire ou non
        T* q;   // incorrect : il n'est pas clair que q soit propriétaire ou non
        // ...
    };

Nous pouvons corriger ce problème en explicitant la propriété :

    template<typename T>
    class X2 {
    public:
        owner<T*> p;  // correct : p est propriétaire
        T* q;         // correct : q n'est pas propriétaire
        // ...
    };

##### Exception

Une grande catégorie d'exceptions concerne le code existant (legacy), en particulier le code qui doit rester compilable en C ou interagir avec du C et du C++ au style C à travers des ABI.
Le fait qu'il existe des milliards de lignes de code qui violent cette règle concernant les `T*` propriétaires ne peut être ignoré.
Nous aimerions voir des outils de transformation de programmes transformer le code « legacy » de 20 ans en code moderne éclatant,
nous encourageons le développement, le déploiement et l'utilisation de tels outils,
nous espérons que les lignes directrices aideront au développement de ces outils,
et nous avons même contribué (et contribuons) à la recherche et au développement dans ce domaine.
Cependant, cela prendra du temps : le code « legacy » est généré plus vite que nous ne pouvons rénover le vieux code, et il en sera ainsi pendant quelques années encore.

Ce code ne peut pas tous être réécrit (même en supposant de bons logiciels de transformation de code), surtout pas à court terme.
Ce problème ne peut pas être résolu (à grande échelle) en transformant tous les pointeurs propriétaires en `unique_ptr` et `shared_ptr`,
en partie parce que nous avons besoin/utilisons des pointeurs bruts propriétaires ainsi que des pointeurs simples dans l'implémentation de nos poignées de ressources fondamentales.
Par exemple, les implémentations courantes de `vector` ont un pointeur propriétaire et deux pointeurs non-propriétaires.
Beaucoup d'ABI (et essentiellement toutes les interfaces vers du code C) utilisent des `T*`, certains propriétaires.
Certaines interfaces ne peuvent pas être simplement annotées avec `owner` car elles doivent rester compilables en C
(quoique ce serait un bon usage rare d'une macro qui se développe en `owner` uniquement en mode C++).

##### Remarque

`owner<T*>` n'a pas de sémantique par défaut au-delà de `T*`. Il peut être utilisé sans modifier aucun code l'utilisant et sans affecter les ABI.
C'est simplement un indicateur destiné aux programmeurs et aux outils d'analyse.
Par exemple, si un `owner<T*>` est un membre d'une classe, cette classe doit avoir un destructeur qui fait `delete` dessus.

##### Exemple non conforme

Retourner un (pointeur) brut impose une incertitude de gestion de durée de vie à l'appelant : qui supprime l'objet pointé ?

    Gadget* make_gadget(int n)
    {
        auto p = new Gadget{n};
        // ...
        return p;
    }

    void caller(int n)
    {
        auto p = make_gadget(n);   // se souvenir de supprimer p
        // ...
        delete p;
    }

En plus de souffrir du problème de [fuite](004-philosophy.md#rp-leak), cela ajoute une opération d'allocation et de désallocation superflue, et est inutilement verbeux. Si Gadget est peu coûteux à déplacer hors d'une fonction (c'est-à-dire qu'il est petit ou a une opération de déplacement efficace), il suffit de le retourner « par valeur » (voir les [valeurs de retour « out »](006-functions.md#rf-out)) :

    Gadget make_gadget(int n)
    {
        Gadget g{n};
        // ...
        return g;
    }

##### Remarque

Cette règle s'applique aux fonctions fabrique.

##### Remarque

Si la sémantique de pointeur est requise (par exemple, parce que le type de retour doit faire référence à une classe de base d'une hiérarchie de classes (une interface)), retournez un « pointeur intelligent ».

##### Détection

* (Simple) Avertir en cas de `delete` d'un pointeur brut qui n'est pas un `owner<T>`.
* (Modéré) Avertir en cas de `reset` ou de `delete` explicite non effectué sur un pointeur `owner<T>` sur tous les chemins d'exécution.
* (Simple) Avertir si la valeur de retour de `new` est assignée à un pointeur brut.
* (Simple) Avertir si une fonction retourne un objet alloué dans la fonction mais ayant un constructeur de déplacement.
  Suggérer de envisager de le retourner par valeur à la place.

### <a name="rr-ref"></a>R.4 : Une référence brute (un `T&`) est non-propriétaire

##### Justification

Il n'y a rien (ni dans la norme C++ ni dans la plupart du code) pour dire le contraire, et la plupart des références brutes sont non-propriétaires.
Nous voulons que les propriétaires soient identifiés afin de pouvoir supprimer de manière fiable et efficace les objets pointés par des pointeurs propriétaires.

##### Exemple

    void f()
    {
        int& r = *new int{7};  // incorrect : référence brute propriétaire
        // ...
        delete &r;             // incorrect : viole la règle interdisant de supprimer un pointeur brut
    }

**Voir aussi** : [La règle des pointeurs bruts](009-resource.md#rr-ptr)

##### Détection

Voir [la règle des pointeurs bruts](009-resource.md#rr-ptr)

### <a name="rr-scoped"></a>R.5 : Privilégier les objets bornés par une portée, ne pas allouer sur le tas inutilement

##### Justification

Un objet borné par une portée est un objet local, un objet global ou un membre.
Cela implique qu'il n'y a pas de coût d'allocation et de désallocation supplémentaire au-delà de celui déjà utilisé pour la portée ou l'objet contenant.
Les membres d'un objet borné sont eux-mêmes bornés par une portée, et le constructeur et le destructeur de l'objet gèrent la durée de vie des membres.

##### Exemple

L'exemple suivant est inefficace (car il comporte une allocation et une désallocation inutiles), vulnérable aux exceptions et retours dans la partie `...` (provoquant des fuites), et verbeux :

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

##### Détection

* (Modéré) Avertir si un objet est alloué puis désalloué sur tous les chemins dans une fonction. Suggérer qu'il devrait être un objet local sur la pile.
* (Simple) Avertir si un `Unique_pointer` ou `Shared_pointer` local qui n'est ni déplacé, ni copié, ni réassigné, ni `reset` avant la fin de sa durée de vie n'est pas déclaré `const`.
  Exception : ne pas produire un tel avertissement pour un `Unique_pointer` local vers un tableau non borné. (Voir ci-dessous.)

##### Exception

Si votre espace de pile est limité, il est acceptable de créer un `const unique_ptr<BigObject>` local pour stocker l'objet sur le tas plutôt que sur la pile.

### <a name="rr-global"></a>R.6 : Éviter les variables globales non-`const`

Voir [I.2](005-interfaces.md#ri-global)

## <a name="ss-alloc"></a>R.alloc : Allocation et désallocation

### <a name="rr-mallocfree"></a>R.10 : Éviter `malloc()` et `free()`

##### Justification

`malloc()` et `free()` ne prennent pas en charge la construction et la destruction, et ne se combinent pas bien avec `new` et `delete`.

##### Exemple

    class Record {
        int id;
        string name;
        // ...
    };

    void use()
    {
        // p1 peut être nullptr
        // *p1 n'est pas initialisé ; en particulier,
        // cette string n'est pas une string, mais un sac de bits de la taille d'une string
        Record* p1 = static_cast<Record*>(malloc(sizeof(Record)));

        auto p2 = new Record;

        // sauf si une exception est levée, *p2 est initialisé par défaut
        auto p3 = new(nothrow) Record;
        // p3 peut être nullptr ; si ce n'est pas le cas, *p3 est initialisé par défaut

        // ...

        delete p1;    // erreur : impossible de supprimer un objet alloué par malloc()
        free(p2);    // erreur : impossible de free() un objet alloué par new
    }

Dans certaines implémentations, ce `delete` et ce `free()` pourraient fonctionner, ou peut-être provoqueront-ils des erreurs d'exécution.

##### Exception

Il existe des applications et des sections de code où les exceptions ne sont pas acceptables.
Certains des meilleurs exemples de ce type se trouvent dans du code temps réel dur critique pour la sécurité.
Méfiez-vous que beaucoup d'interdictions d'utilisation des exceptions sont basées sur de la superstition (mauvais)
ou sur des préoccupations liées aux anciennes bases de code ayant une gestion des ressources non systématique (malheureusement, mais parfois nécessaire).
Dans de tels cas, envisagez les versions `nothrow` de `new`.

##### Détection

Signaler l'utilisation explicite de `malloc` et `free`.

### <a name="rr-newdelete"></a>R.11 : Éviter d'appeler `new` et `delete` explicitement

##### Justification

Le pointeur retourné par `new` doit appartenir à une poignée de ressource (qui peut appeler `delete`).
Si le pointeur retourné par `new` est assigné à un pointeur nu, l'objet peut être perdu (fuite).

##### Remarque

Dans un grand programme, un `delete` nu (c'est-à-dire un `delete` dans le code applicatif, plutôt que dans du code dédié à la gestion des ressources)
est très probablement un bug : si vous avez N `delete`, comment pouvez-vous être certain que vous n'avez pas besoin de N+1 ou N-1 ?
Le bug peut être latent : il ne se manifesterait qu'au cours de la maintenance.
Si vous avez un `new` nu, vous avez probablement besoin d'un `delete` nu quelque part, donc vous avez probablement un bug.

##### Détection

(Simple) Avertir en cas d'utilisation explicite de `new` et `delete`. Suggérer d'utiliser `make_unique` à la place.

### <a name="rr-immediate-alloc"></a>R.12 : Transférer immédiatement le résultat d'une allocation de ressource explicite à un objet gestionnaire

##### Justification

Si vous ne le faites pas, une exception ou un retour pourrait provoquer une fuite.

##### Exemple non conforme

    void func(const string& name)
    {
        FILE* f = fopen(name, "r");            // ouvrir le fichier
        vector<char> buf(1024);
        auto _ = finally([f] { fclose(f); });  // se souvenir de fermer le fichier
        // ...
    }

L'allocation de `buf` peut échouer et provoquer une fuite du descripteur de fichier.

##### Exemple

    void func(const string& name)
    {
        ifstream f{name};   // ouvrir le fichier
        vector<char> buf(1024);
        // ...
    }

L'utilisation du descripteur de fichier (dans `ifstream`) est simple, efficace et sûre.

##### Détection

* Signaler les allocations explicites utilisées pour initialiser des pointeurs (problème : combien d'allocations de ressources directes pouvons-nous reconnaître ?)

### <a name="rr-single-alloc"></a>R.13 : Effectuer au plus une allocation de ressource explicite dans une unique instruction d'expression

##### Justification

Si vous effectuez deux allocations de ressources explicites dans une même instruction, vous pouvez provoquer des fuites de ressources car l'ordre d'évaluation de nombreuses sous-expressions, y compris les arguments de fonctions, n'est pas spécifié.

##### Exemple

    void fun(shared_ptr<Widget> sp1, shared_ptr<Widget> sp2);

Cette `fun` peut être appelée ainsi :

    // NON CONFORME : fuite potentielle
    fun(shared_ptr<Widget>(new Widget(a, b)), shared_ptr<Widget>(new Widget(c, d)));

Ceci n'est pas sûr face aux exceptions car le compilateur peut réordonner les deux expressions construisant les deux arguments de la fonction.
En particulier, le compilateur peut imbriquer l'exécution des deux expressions :
l'allocation mémoire (en appelant `operator new`) pourrait être effectuée en premier pour les deux objets, suivie des tentatives d'appel des deux constructeurs `Widget`.
Si l'un des appels de constructeur lève une exception, alors la mémoire de l'autre objet ne sera jamais libérée !

Ce problème subtil a une solution simple : ne jamais effectuer plus d'une allocation de ressource explicite dans une unique instruction d'expression.
Par exemple :

    shared_ptr<Widget> sp1(new Widget(a, b)); // Meilleur, mais maladroit
    fun(sp1, new Widget(c, d));

La meilleure solution est d'éviter toute allocation explicite, en utilisant des fonctions fabrique qui retournent des objets propriétaires :

    fun(make_shared<Widget>(a, b), make_shared<Widget>(c, d)); // Le meilleur

Écrivez votre propre enveloppe fabrique s'il n'en existe pas déjà une.

##### Détection

* Signaler les expressions comportant plusieurs allocations de ressources explicites (problème : combien d'allocations de ressources directes pouvons-nous reconnaître ?)

### <a name="rr-ap"></a>R.14 : Éviter les paramètres `[]`, préférer `span`

##### Justification

Un tableau se dégrade en pointeur, perdant ainsi sa taille et ouvrant la porte aux erreurs de portée.
Utilisez `span` pour préserver l'information de taille.

##### Exemple

    void f(int[]);          // non recommandé

    void f(int*);           // non recommandé pour plusieurs objets
                            // (un pointeur doit pointer vers un seul objet, ne pas indexer)

    void f(gsl::span<int>); // bon, recommandé

##### Détection

Signaler les paramètres `[]`. Utilisez `span` à la place.

### <a name="rr-pair"></a>R.15 : Toujours surcharger les paires appariées d'allocation/désallocation

##### Justification

Sinon vous obtenez des opérations non appariées et le chaos.

##### Exemple

    class X {
        // ...
        void* operator new(size_t s);
        void operator delete(void*);
        // ...
    };

##### Remarque

Si vous souhaitez de la mémoire qui ne peut pas être désallouée, utilisez `= delete` pour l'opération de désallocation.
Ne la laissez pas non déclarée.

##### Détection

Signaler les paires incomplètes.

## <a name="ss-smart"></a>R.smart : Pointeurs intelligents

### <a name="rr-owner"></a>R.20 : Utiliser `unique_ptr` ou `shared_ptr` pour représenter la propriété

##### Justification

Ils peuvent prévenir les fuites de ressources.

##### Exemple

Considérez :

    void f()
    {
        X* p1 { new X };              // incorrect, p1 provoquera une fuite
        auto p2 = make_unique<X>();   // correct, propriété unique
        auto p3 = make_shared<X>();   // correct, propriété partagée
    }

Ceci provoque une fuite de l'objet utilisé pour initialiser `p1` (uniquement).

##### Détection

* (Simple) Avertir si la valeur de retour de `new` est assignée à un pointeur brut.
* (Simple) Avertir si le résultat d'une fonction retournant un pointeur brut propriétaire est assigné à un pointeur brut.

### <a name="rr-unique"></a>R.21 : Préférer `unique_ptr` à `shared_ptr` sauf si le partage de propriété est nécessaire

##### Justification

Un `unique_ptr` est conceptuellement plus simple et plus prévisible (vous savez quand la destruction a lieu) et plus rapide (vous ne maintenez pas implicitement un compteur d'utilisation).

##### Exemple non conforme

Ceci ajoute et maintient inutilement un compteur de référence.

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

##### Détection

(Simple) Avertir si une fonction utilise un `Shared_pointer` avec un objet alloué dans la fonction, mais ne retourne jamais le `Shared_pointer` ni ne le passe à une fonction exigeant un `Shared_pointer`. Suggérer d'utiliser `unique_ptr` à la place.

### <a name="rr-make_shared"></a>R.22 : Utiliser `make_shared()` pour créer des `shared_ptr`

##### Justification

`make_shared` offre une formulation plus concise de la construction.
Il offre aussi l'opportunité d'éliminer une allocation séparée pour les compteurs de référence, en plaçant les compteurs d'utilisation du `shared_ptr` à côté de son objet.
Il assure aussi la sûreté face aux exceptions dans les expressions complexes (dans le code antérieur à C++17).

##### Exemple

Considérez :

    shared_ptr<X> p1 { new X{2} }; // incorrect
    auto p = make_shared<X>(2);    // correct

La version `make_shared()` mentionne `X` une seule fois, donc elle est généralement plus courte (et plus rapide) que la version avec `new` explicite.

##### Détection

(Simple) Avertir si un `shared_ptr` est construit à partir du résultat de `new` plutôt que de `make_shared`.

### <a name="rr-make_unique"></a>R.23 : Utiliser `make_unique()` pour créer des `unique_ptr`

##### Justification

`make_unique` offre une formulation plus concise de la construction.
Il assure aussi la sûreté face aux exceptions dans les expressions complexes (dans le code antérieur à C++17).

##### Exemple

    unique_ptr<Foo> p {new Foo{7}};    // acceptable : mais répétitif

    auto q = make_unique<Foo>(7);      // Meilleur : pas de répétition de Foo

##### Détection

(Simple) Avertir si un `unique_ptr` est construit à partir du résultat de `new` plutôt que de `make_unique`.

### <a name="rr-weak_ptr"></a>R.24 : Utiliser `std::weak_ptr` pour briser les cycles de `shared_ptr`

##### Justification

Les `shared_ptr` reposent sur le comptage d'utilisation et le compteur d'utilisation d'une structure cyclique n'atteint jamais zéro, donc nous avons besoin d'un mécanisme pour
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

##### Remarque

 ??? (HS : Beaucoup de gens disent « pour briser les cycles », tandis que je pense que « partage temporaire de propriété » est plus à propos.)
???(BS : briser les cycles est ce que vous devez faire ; partager temporairement la propriété est la manière de le faire.
Vous pourriez « partager temporairement la propriété » simplement en utilisant un autre `shared_ptr`.)

##### Détection

??? probablement impossible. Si nous pouvions détecter statiquement les cycles, nous n'aurions pas besoin de `weak_ptr`

### <a name="rr-smartptrparam"></a>R.30 : N'accepter des pointeurs intelligents en paramètre que pour exprimer explicitement la sémantique de durée de vie

Voir [F.7](006-functions.md#rf-smart).

### <a name="rr-smart"></a>R.31 : Si vous utilisez des pointeurs intelligents non-`std`, suivre le modèle de base de `std`

##### Justification

Les règles de la section suivante fonctionnent également pour d'autres types de pointeurs intelligents tiers et personnalisés et sont très utiles pour diagnostiquer les erreurs courantes de pointeurs intelligents qui causent des problèmes de performance et de correction.
Vous voulez que les règles fonctionnent sur tous les pointeurs intelligents que vous utilisez.

Tout type (y compris un gabarit primaire ou une spécialisation) qui surcharge les opérateurs unaires `*` et `->` est considéré comme un pointeur intelligent :

* S'il est copiable, il est reconnu comme un `shared_ptr` avec comptage de référence.
* S'il n'est pas copiable, il est reconnu comme un `unique_ptr` unique.

##### Exemple non conforme

    // utiliser l'intrusive_ptr de Boost
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

Les deux cas sont une erreur selon la [ligne directrice `sharedptrparam`](009-resource.md#rr-sharedptrparam) :
`p` est un `Shared_pointer`, mais rien de sa nature partagée n'est utilisé ici et le passage par valeur est une pessimisation silencieuse ;
ces fonctions ne devraient accepter un pointeur intelligent que si elles doivent participer à la gestion de la durée de vie du widget. Sinon, elles devraient accepter un `widget*`, si celui-ci peut être `nullptr`. Sinon, et idéalement, la fonction devrait accepter un `widget&`.
Ces pointeurs intelligents correspondent au concept `Shared_pointer`, donc ces règles de détection fonctionnent sur eux immédiatement et exposent cette pessimisation courante.

### <a name="rr-uniqueptrparam"></a>R.32 : Accepter un paramètre `unique_ptr<widget>` pour exprimer qu'une fonction assume la propriété d'un `widget`

##### Justification

L'utilisation de `unique_ptr` de cette manière documente et applique le transfert de propriété de l'appel de fonction.

##### Exemple

    void sink(unique_ptr<widget>); // prend la propriété du widget

    void uses(widget*);            // utilise simplement le widget

##### Détection

* (Simple) Avertir si une fonction accepte un paramètre `Unique_pointer<T>` par référence à lvalue et n'y effectue ni assignment ni appel à `reset()` sur au moins un chemin d'exécution. Suggérer d'accepter un `T*` ou `T&` à la place.

### <a name="rr-reseat"></a>R.33 : Accepter un paramètre `unique_ptr<widget>&` pour exprimer qu'une fonction réassigne le `widget`

##### Justification

L'utilisation de `unique_ptr` de cette manière documente et applique la sémantique de réassignation de l'appel de fonction.

##### Remarque

« Réassigner » signifie « faire en sorte qu'un pointeur ou un pointeur intelligent fasse référence à un objet différent ».

##### Exemple

    void reseat(unique_ptr<widget>&); // « va » ou « peut » réassigner le pointeur

##### Détection

* (Simple) Avertir si une fonction accepte un paramètre `Unique_pointer<T>` par référence à lvalue et n'y effectue ni assignment ni appel à `reset()` sur au moins un chemin d'exécution. Suggérer d'accepter un `T*` ou `T&` à la place.

### <a name="rr-sharedptrparam-owner"></a>R.34 : Accepter un paramètre `shared_ptr<widget>` pour exprimer un partage de propriété

##### Justification

Cela rend le partage de propriété de la fonction explicite.

##### Exemple correct

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

##### Détection

* (Simple) Avertir si une fonction accepte un paramètre `Shared_pointer<T>` par référence à lvalue et n'y effectue ni assignment ni appel à `reset()` sur au moins un chemin d'exécution. Suggérer d'accepter un `T*` ou `T&` à la place.
* (Simple) ((Foundation)) Avertir si une fonction accepte un `Shared_pointer<T>` par valeur ou par référence à `const` et ne le copie ni ne le déplace dans un autre `Shared_pointer` sur au moins un chemin d'exécution. Suggérer d'accepter un `T*` ou `T&` à la place.
* (Simple) ((Foundation)) Avertir si une fonction accepte un `Shared_pointer<T>` par référence à rvalue. Suggérer de l'accepter par valeur à la place.

### <a name="rr-sharedptrparam"></a>R.35 : Accepter un paramètre `shared_ptr<widget>&` pour exprimer qu'une fonction peut réassigner le pointeur partagé

##### Justification

Cela rend la réassignation de la fonction explicite.

##### Remarque

« Réassigner » signifie « faire en sorte qu'une référence ou un pointeur intelligent fasse référence à un objet différent ».

##### Exemple correct

    void ChangeWidget(std::shared_ptr<widget>& w)
    {
        // Cela changera le widget de l'appelant
        w = std::make_shared<widget>(widget{});
    }

##### Détection

* (Simple) Avertir si une fonction accepte un paramètre `Shared_pointer<T>` par référence à lvalue et n'y effectue ni assignment ni appel à `reset()` sur au moins un chemin d'exécution. Suggérer d'accepter un `T*` ou `T&` à la place.
* (Simple) ((Foundation)) Avertir si une fonction accepte un `Shared_pointer<T>` par valeur ou par référence à `const` et ne le copie ni ne le déplace dans un autre `Shared_pointer` sur au moins un chemin d'exécution. Suggérer d'accepter un `T*` ou `T&` à la place.
* (Simple) ((Foundation)) Avertir si une fonction accepte un `Shared_pointer<T>` par référence à rvalue. Suggérer de l'accepter par valeur à la place.

### <a name="rr-sharedptrparam-const"></a>R.36 : Accepter un paramètre `const shared_ptr<widget>&` pour exprimer qu'il peut conserver un compteur de référence à l'objet ???

##### Justification

Cela rend ??? de la fonction explicite.

##### Exemple correct

    void share(shared_ptr<widget>);            // partage -- « va » conserver le compteur de référence

    void reseat(shared_ptr<widget>&);          // « peut » réassigner le pointeur

    void may_share(const shared_ptr<widget>&); // « peut » conserver le compteur de référence

##### Détection

* (Simple) Avertir si une fonction accepte un paramètre `Shared_pointer<T>` par référence à lvalue et n'y effectue ni assignment ni appel à `reset()` sur au moins un chemin d'exécution. Suggérer d'accepter un `T*` ou `T&` à la place.
* (Simple) ((Foundation)) Avertir si une fonction accepte un `Shared_pointer<T>` par valeur ou par référence à `const` et ne le copie ni ne le déplace dans un autre `Shared_pointer` sur au moins un chemin d'exécution. Suggérer d'accepter un `T*` ou `T&` à la place.
* (Simple) ((Foundation)) Avertir si une fonction accepte un `Shared_pointer<T>` par référence à rvalue. Suggérer de l'accepter par valeur à la place.

### <a name="rr-smartptrget"></a>R.37 : Ne pas passer un pointeur ou une référence obtenus à partir d'un pointeur intelligent aliasé

##### Justification

La violation de cette règle est la cause numéro un de la perte de compteurs de référence et de la présence de pointeurs pendants.
Les fonctions devraient préférer transmettre des pointeurs bruts et des références le long des chaînes d'appels.
C'est au sommet de l'arbre d'appels que vous obtenez le pointeur brut ou la référence à partir d'un pointeur intelligent qui maintient l'objet en vie.
Vous devez vous assurer que le pointeur intelligent ne peut pas être réassigné ou réinitialisé inadvertément depuis l'intérieur de l'arbre d'appels en dessous.

##### Remarque

Pour ce faire, il est parfois nécessaire de prendre une copie locale du pointeur intelligent, ce qui maintient fermement l'objet en vie pour la durée de la fonction et de l'arbre d'appels.

##### Exemple

Considérez ce code :

    // global (statique ou sur le tas), ou local aliasé ...
    shared_ptr<widget> g_p = ...;

    void f(widget& w)
    {
        g();
        use(w);  // A
    }

    void g()
    {
        g_p = ...; // oops, si c'était le dernier shared_ptr de ce widget, détruit le widget
    }

Le code suivant ne devrait pas passer une revue de code :

    void my_code()
    {
        // NON CONFORME : passe un pointeur ou une référence obtenus à partir d'un
        //      pointeur intelligent non local qui pourrait être réassigné
        //      inadvertemment quelque part dans f ou ses appelés
        f(*g_p);

        // NON CONFORME : même raison, simplement en le passant comme pointeur « this »
        g_p->func();
    }

La correction est simple -- prenez une copie locale du pointeur pour « conserver un compteur de référence » pour votre arbre d'appels :

    void my_code()
    {
        // peu coûteux : 1 incrément couvre cette fonction entière et tous les arbres d'appels en dessous
        auto pin = g_p;

        // CONFORME : passe un pointeur ou une référence obtenus à partir d'un
        //      pointeur intelligent local non aliasé
        f(*pin);

        // CONFORME : même raison
        pin->func();
    }

##### Détection

* (Simple) Avertir si un pointeur ou une référence obtenu à partir d'une variable pointeur intelligent (`Unique_pointer` ou `Shared_pointer`) qui n'est pas locale, ou qui est locale mais potentiellement aliasé, est utilisé dans un appel de fonction. Si le pointeur intelligent est un `Shared_pointer`, suggérer de prendre une copie locale du pointeur intelligent et d'obtenir un pointeur ou une référence à partir de celle-ci à la place.