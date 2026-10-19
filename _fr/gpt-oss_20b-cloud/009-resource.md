# <a name="s-resource"></a>R : Gestion des ressources

Cette section contient des règles relatives aux ressources.  
Une ressource est tout ce qui doit être acquis et (explicitement ou implicitement) libéré, comme la mémoire, les handles de fichiers, les sockets et les verrous.  
La raison pour laquelle elle doit être libérée est généralement qu'elle peut être en quantité limitée, de sorte qu'une libération tardive pourrait être préjudiciable.  
L'objectif fondamental est de s'assurer que nous ne perdons aucune ressource et que nous ne conservons une ressource plus longtemps que nécessaire.  
Une entité responsable de la libération d'une ressource est appelée un propriétaire.

Il existe quelques cas où les fuites peuvent être acceptables voire même optimales :  
Si vous écrivez un programme qui produit simplement une sortie à partir d'une entrée et que la quantité de mémoire requise est proportionnelle à la taille de l'entrée, la stratégie optimale (en termes de performance et de facilité de programmation) est parfois simplement de ne jamais rien supprimer.  
Si vous disposez d'assez de mémoire pour gérer votre plus grande entrée, laissez libre cours à la fuite, mais assurez-vous d'afficher un bon message d'erreur si vous vous trompez.  
Ici, nous ignorons de tels cas.

* Règle de gestion des ressources :  
  * [R.1 : Gérer automatiquement les ressources en utilisant des handles de ressources et RAII (Resource Acquisition Is Initialization)](009-resource.md#rr-raii)  
  * [R.2 : Dans les interfaces, utilisez des pointeurs bruts pour désigner des objets individuels (uniquement)](009-resource.md#rr-use-ptr)  
  * [R.3 : Un pointeur brut (`T*`) est non propriétaire](009-resource.md#rr-ptr)  
  * [R.4 : Une référence brute (`T&`) est non propriétaire](009-resource.md#rr-ref)  
  * [R.5 : Préférez les objets scopés, ne allouez pas inutilement sur le tas](009-resource.md#rr-scoped)  
  * [R.6 : Évitez les variables globales non-`const`](009-resource.md#rr-global)  

* Règle d'allocation et de désallocation :  
  * [R.10 : Évitez `malloc()` et `free()`](009-resource.md#rr-mallocfree)  
  * [R.11 : Évitez d'appeler `new` et `delete` explicitement](009-resource.md#rr-newdelete)  
  * [R.12 : Donnez immédiatement le résultat d'une allocation explicite de ressource à un objet gestionnaire](009-resource.md#rr-immediate-alloc)  
  * [R.13 : Effectuez au plus une allocation explicite de ressource dans une seule instruction d'expression](009-resource.md#rr-single-alloc)  
  * [R.14 : Évitez les paramètres `[]`, préférez `span`](009-resource.md#rr-ap)  
  * [R.15 : Survolez toujours les paires allocation/désallocation correspondantes](009-resource.md#rr-pair)  

* Règle des pointeurs intelligents :  
  * [R.20 : Utilisez `unique_ptr` ou `shared_ptr` pour représenter la propriété](009-resource.md#rr-owner)  
  * [R.21 : Préférez `unique_ptr` à `shared_ptr` sauf si vous avez besoin de partager la propriété](009-resource.md#rr-unique)  
  * [R.22 : Utilisez `make_shared()` pour créer des `shared_ptr`](009-resource.md#rr-make_shared)  
  * [R.23 : Utilisez `make_unique()` pour créer des `unique_ptr`](009-resource.md#rr-make_unique)  
  * [R.24 : Utilisez `std::weak_ptr` pour rompre les cycles de `shared_ptr`](009-resource.md#rr-weak_ptr)  
  * [R.30 : Prenez les pointeurs intelligents en paramètres uniquement pour exprimer explicitement les sémantiques de durée de vie](009-resource.md#rr-smartptrparam)  
  * [R.31 : Si vous avez des pointeurs intelligents non‑`std`, suivez le modèle de base de `std`](009-resource.md#rr-smart)  
  * [R.32 : Prenez un paramètre `unique_ptr<widget>` afin d'exprimer que la fonction assume la propriété d'un `widget`](009-resource.md#rr-uniqueptrparam)  
  * [R.33 : Prenez un paramètre `unique_ptr<widget>&` afin d'exprimer que la fonction réinstalle le `widget`](009-resource.md#rr-reseat)  
  * [R.34 : Prenez un paramètre `shared_ptr<widget>` afin d'exprimer la propriété partagée](009-resource.md#rr-sharedptrparam-owner)  
  * [R.35 : Prenez un paramètre `shared_ptr<widget>&` afin d'exprimer que la fonction peut réinstaller le pointeur partagé](009-resource.md#rr-sharedptrparam)  
  * [R.36 : Prenez un paramètre `const shared_ptr<widget>&` afin d'exprimer qu'il peut retenir le compte de référence de l'objet ???](009-resource.md#rr-sharedptrparam-const)  
  * [R.37 : Ne pas transmettre un pointeur ou une référence obtenus à partir d'un pointeur intelligent alié](009-resource.md#rr-smartptrget)  

### <a name="rr-raii"></a>R.1 : Gérer les ressources automatiquement en utilisant des handles de ressources et RAII (Resource Acquisition Is Initialization)

##### Raison

Pour éviter les fuites et la complexité de la gestion manuelle des ressources.  
La symétrie imposée par le langage en ce qui concerne les constructeurs/destructeurs reflète la symétrie inhérente aux paires de fonctions d'acquisition/libération de ressources telles que `fopen`/`fclose`, `lock`/`unlock` et `new`/`delete`.  
Lorsque vous travaillez avec une ressource nécessitant des appels fonctionnels d'acquisition/libération appariés, encapsulez cette ressource dans un objet qui impose l'appariement — acquérez la ressource dans son constructeur, et libérez‑la dans son destructeur.

##### Exemple, mauvais

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

Dans ce code, vous devez vous souvenir de `unlock`, `close_port` et `delete` sur tous les chemins, et d'exécuter chacun exactement une fois.  
De plus, si l'un des morceaux de code marqués `...` lève une exception, alors `x` est perdue et `my_mutex` reste verrouillé.

##### Exemple

    void send(unique_ptr<X> x, string_view destination)  // x possède le X
    {
        Port port{destination};            // port possède le PortHandle
        lock_guard<mutex> guard{my_mutex}; // guard possède le verrou
        // ...
        send(port, x);
        // ...
    } // déverrouille automatiquement my_mutex et supprime le pointeur dans x

Maintenant, tout le nettoyage de ressources est automatique, effectué une seule fois sur tous les chemins, qu'il y ait ou non une exception. En bonus, la fonction annonce désormais qu'elle prend en charge la propriété du pointeur.

Qu'est‑ce que `Port` ? Un wrapper pratique qui encapsule la ressource :

    class Port {
        PortHandle port;
    public:
        Port(string_view destination) : port{open_port(destination)} { }
        ~Port() { close_port(port); }
        operator PortHandle() { return port; }

        // les handles de port ne peuvent généralement pas être clonés, donc désactivez la copie et l'assignation si nécessaire
        Port(const Port&) = delete;
        Port& operator=(const Port&) = delete;
    };

**Note**  
Si une ressource se comporte mal car elle n'est pas représentée sous forme de classe avec un destructeur, enveloppez‑la dans une classe ou utilisez [`finally`](013-errors.md#re-finally).

**Voir également** : [RAII](013-errors.md#re-raii)

### <a name="rr-use-ptr"></a>R.2 : Dans les interfaces, utilisez des pointeurs bruts pour désigner des objets individuels (uniquement)

##### Raison

Les tableaux sont mieux représentés par un type de conteneur (par ex. `vector` (propriétaire)) ou par un `span` (non‑propriétaire). Ces conteneurs et vues détiennent suffisamment d'informations pour effectuer une vérification de plage.

##### Exemple, mauvais

    void f(int* p, int n)   // n est le nombre d'éléments dans p[]
    {
        // ...
        p[2] = 7;   // mauvais : sous‑indexation d'un pointeur brut
        // ...
    }

Dans ce code, le compilateur ne lit pas les commentaires, et sans étudier d'autres parties du code, vous ne savez pas si `p` pointe réellement vers `n` éléments. Utilisez plutôt un `span`.

##### Exemple

    void g(int* p, int fmt)   // afficher *p en utilisant le format #fmt
    {
        // ... utilise *p et p[0] seulement ...
    }

##### Exception

Les chaînes de caractères de style C sont transmises sous forme de pointeurs simples vers une séquence terminée par zéro de caractères. Utilisez `zstring` plutôt que `char*` pour indiquer que vous reposez sur cette convention.

##### Remarque

De nombreux usages actuels de pointeurs vers un seul élément pourraient être des références.  
Cependant, lorsque `nullptr` est une valeur possible, une référence peut ne pas être une alternative raisonnable.

##### Application

* Signaler l'arithmétique de pointeur (y compris `++`) sur un pointeur qui ne fait pas partie d'un conteneur, d'une vue ou d'un itérateur.  
  Cette règle générerait un énorme nombre de faux positifs si elle était appliquée à une ancienne base de code.

* Signaler les noms de tableaux passés comme pointeurs simples

### <a name="rr-ptr"></a>R.3 : Un pointeur brut (`T*`) est non propriétaire

##### Raison

Il n'y a rien (dans le standard C++ ou dans le code la plupart du temps) qui le contredit et la plupart des pointeurs bruts ne sont pas propriétaires. Nous voulons que les pointeurs propriétaires soient identifiés afin que nous puissions supprimer de manière fiable et efficace les objets pointés par les pointeurs propriétaires.

##### Exemple

    void f()
    {
        int* p1 = new int{7};           // mauvais : pointeur brut propriétaire
        auto p2 = make_unique<int>(7);  // OK : l'entier est possédé par un `unique_ptr`
        // ...
    }

Dans ce code, le `unique_ptr` protège contre les fuites en garantissant la suppression de son objet (même en présence d'exceptions). Le `T*` ne le fait pas.

##### Exemple

    template<typename T>
    class X {
    public:
        T* p;   // mauvais : il n'est pas clair si p est propriétaire ou non
        T* q;   // mauvais : il n'est pas clair si q est propriétaire ou non
        // ...
    };

    // Correction
    template<typename T>
    class X2 {
    public:
        owner<T*> p;  // OK : p est propriétaire
        T* q;         // OK : q n'est pas propriétaire
        // ...
    };

##### Exception

Une grande classe d'exception est le code hérité, en particulier le code qui doit rester compilable en C ou interfacer avec du C et du C++ de style C via les ABI.  
Le fait qu'il existe des milliards de lignes de code qui violent cette règle contre les `T*` propriétaires ne peut être ignoré.  
Nous aimerions voir des outils de transformation de programmes convertissant le code « hérité » de 20 ans en code moderne brillant, nous encourageons le développement, le déploiement et l'utilisation de tels outils, nous espérons que les lignes directrices aideront le développement de ces outils, et nous avons même contribué (et contribuons) à la recherche et au développement dans ce domaine.  
Cependant, il faudra du temps : le code « hérité » est généré plus vite que nous pouvons rénover l'ancien code, et donc cela durera quelques années.  

Ce code ne peut pas tous être réécrit (même en supposant un bon logiciel de transformation), surtout pas bientôt.  
Ce problème ne peut pas être résolu (à grande échelle) en transformant tous les pointeurs propriétaires en `unique_ptr` et `shared_ptr`, en partie parce que nous avons besoin d'utiliser les « pointeurs bruts propriétaires » ainsi que les pointeurs simples dans la mise en œuvre de nos handles de ressources fondamentales.  
Par exemple, les implémentations communes de `vector` ont un pointeur propriétaire et deux pointeurs non propriétaires.  
De nombreux ABI (et pratiquement toutes les interfaces à du code C) utilisent des `T*`, certaines d'entre elles propriétaires.  
Certaines interfaces ne peuvent pas être simplement annotées avec `owner` car elles doivent rester compilables en C (mais ce serait un usage rare et bon d'un macro, qui s'étend à `owner` seulement en mode C++).

##### Remarque

`owner<T*>` n'a pas de sémantique par défaut en dehors de `T*`. Il peut être utilisé sans modifier le code qui l'utilise et sans affecter les ABI.  
C'est simplement un indicateur pour les programmeurs et les outils d'analyse.  
Par exemple, si un `owner<T*>` est un membre d'une classe, la classe doit désigner un destructeur qui le supprime avec `delete`.

##### Exemple, mauvais

    Gadget* make_gadget(int n)
    {
        auto p = new Gadget{n};
        // ...
        return p;
    }

    void caller(int n)
    {
        auto p = make_gadget(n);   // souvenez‑vous de supprimer p
        // ...
        delete p;
    }

En plus de subir le problème de fuite, cela ajoute une allocation et une désallocation inutiles, et est inutilement verbeux. Si Gadget est peu coûteux à déplacer hors d'une fonction (c.-à-d. est petite ou possède un mouvement efficace), il suffit de le retourner « par valeur » (voir ["out" return values](006-functions.md#rf-out)):

    Gadget make_gadget(int n)
    {
        Gadget g{n};
        // ...
        return g;
    }

##### Remarque

Cette règle s'applique aux fonctions de fabrique.

##### Remarque

Si la sémantique du pointeur est requise (par ex. parce que le type de retour doit référer à une classe de base d'une hiérarchie de classes (une interface)), renvoyez un « pointeur intelligent ».

##### Application

* (Simple) Avertir si la valeur de retour de `new` est assignée à un pointeur brut.  
* (Modéré) Avertir si le résultat d'une fonction retournant un pointeur propriétaire brut est assigné à un pointeur brut sur chaque chemin de code.  
* (Simple) Avertir si la valeur de retour de `new` est assignée à un pointeur brut.  
* (Simple) Avertir si une fonction renvoie un objet alloué dans la fonction mais possède un constructeur de déplacement. Suggérer le renvoyer par valeur.

### <a name="rr-ref"></a>R.4 : Une référence brute (`T&`) est non propriétaire

##### Raison

Il n'y a rien (dans le standard C++ ou dans le code la plupart du temps) qui le contredit et la plupart des références brutes ne sont pas propriétaires. Nous voulons que les propriétaires soient identifiés afin que nous puissions supprimer de manière fiable et efficace les objets pointés.

##### Exemple

    void f()
    {
        int& r = *new int{7};  // mauvais : référence brute propriétaire
        // ...
        delete &r;             // mauvais : violé la règle contre la suppression de pointeurs bruts
    }

**Voir également** : [La règle du pointeur brut](009-resource.md#rr-ptr)

##### Application

Voir la règle précédente.

### <a name="rr-scoped"></a>R.5 : Privilégiez les objets scopés, ne allouez pas sans nécessité sur le tas

##### Raison

Un objet scopé est un objet local, un objet global ou un membre.  
Cela implique qu'il n'y a pas de coût d'allocation et de désallocation séparé au-delà de celui déjà utilisé pour la portée ou l'objet contenant.  
Les membres d'un objet scopé sont eux-mêmes scopés et le constructeur et destructeur de l'objet scopé gèrent les durées de vie des membres.

##### Exemple

L'exemple suivant est inefficace (car il comporte une allocation et une désallocation inutiles), vulnérable aux exceptions et aux retours dans la partie `...` (ce qui entraîne des fuites), et verbeux :

    void f(int n)
    {
        auto p = new Gadget{n};
        // ...
        delete p;
    }

À la place, utilisez une variable locale :

    void f(int n)
    {
        Gadget g{n};
        // ...
    }

##### Application

* (Modéré) Avertir si un objet est alloué et désalloué sur tous les chemins au sein d'une fonction. Suggérer d'utiliser un objet local alloué sur la pile à la place.  
* (Simple) Avertir si un `Unique_pointer` local ou `Shared_pointer` qui n'est pas déplacé, copié, réassigné ou `reset` avant la fin de son cycle de vie n'est pas déclaré `const`.  
  Exception : ne pas produire ce warning pour un `Unique_pointer` local à un tableau sans borne. (voir ci‑dessous.)

##### Exception

Si votre espace de pile est limité, il est acceptable de créer un `const unique_ptr<BigObject>` local pour stocker l'objet sur le tas au lieu de la pile.

### <a name="rr-global"></a>R.6 : Évitez les variables globales non‑`const`

Voir [I.2](005-interfaces.md#ri-global)

## <a name="ss-alloc"></a>R.alloc : Allocation et désallocation

### <a name="rr-mallocfree"></a>R.10 : Évitez `malloc()` et `free()`

##### Raison

`malloc()` et `free()` ne supportent pas la construction et la destruction, et ne s'intègrent pas bien avec `new` et `delete`.

##### Exemple

    class Record {
        int id;
        string name;
        // ...
    };

    void use()
    {
        // p1 pourrait être nullptr
        // *p1 n'est pas initialisé ; en particulier, cette chaîne n'est pas une chaîne, mais un sac de bits de la taille d'une chaîne
        Record* p1 = static_cast<Record*>(malloc(sizeof(Record)));

        auto p2 = new Record;

        // à moins qu'une exception ne soit lancée, *p2 est initialisé par défaut
        auto p3 = new(nothrow) Record;
        // p3 pourrait être nullptr ; si non, *p3 est initialisé par défaut

        // ...

        delete p1;    // erreur : ne pas supprimer un objet alloué par malloc()
        free(p2);    // erreur : ne pas libérer() un objet alloué par new
    }

Dans certaines implémentations, `delete` et `free()` peuvent fonctionner, ou provoquent des erreurs d'exécution.

##### Exception

Il existe des applications et des sections de code où les exceptions ne sont pas acceptables.  
Certains des meilleurs exemples se trouvent dans les systèmes critiques temps réel.  
Attention aux nombreux interdits d'utilisation d'exceptions fondés sur la superstition (mauvais) ou sur la préoccupation de la gestion des ressources des anciens codes (malheureusement, mais parfois nécessaire).  
Dans de tels cas, envisagez les versions `nothrow` de `new`.

##### Application

Signalé l'utilisation explicite de `malloc` et `free`.

### <a name="rr-newdelete"></a>R.11 : Évitez d'appeler `new` et `delete` explicitement

##### Raison

Le pointeur retourné par `new` devrait appartenir à un gestionnaire de ressources (qui peut appeler `delete`).  
Si le pointeur retourné par `new` est assigné à un pointeur simple/brut, l'objet peut être perdu.

##### Remarque

Dans un programme volumineux, un `delete` simple (qui est un `delete` dans du code applicatif, plutôt qu'une partie de code dédié à la gestion des ressources) est un bug probable : si vous avez N `delete`, comment pouvez‑vous être sûr de ne pas avoir besoin de N+1 ou N‑1 ?  
Le bug peut être latent : il peut ne se manifester que lors de la maintenance.  
Si vous avez un `new` simple, vous avez probablement besoin d'un `delete` simple quelque part, donc vous avez probablement un bug.

##### Application

(Simp.) Avertir sur toute utilisation explicite de `new` et `delete`. Suggérer d'utiliser `make_unique` à la place.

### <a name="rr-immediate-alloc"></a>R.12 : Donnez immédiatement le résultat d'une allocation explicite de ressource à un objet gestionnaire

##### Raison

S'il ne le fait pas, une exception ou un retour peut entraîner une fuite.

##### Exemple, mauvais

    void func(const string& name)
    {
        FILE* f = fopen(name, "r");            // ouvrir le fichier
        vector<char> buf(1024);
        auto _ = finally([f] { fclose(f); });  // se souvenir de fermer le fichier
        // ...
    }

L'allocation de `buf` peut échouer et fuiter le descripteur de fichier.

##### Exemple

    void func(const string& name)
    {
        ifstream f{name};   // ouvrir le fichier
        vector<char> buf(1024);
        // ...
    }

L'utilisation du descripteur de fichier (dans `ifstream`) est simple, efficace et sécurisée.

##### Application

* Signaler les allocations explicites utilisées pour initialiser des pointeurs.  

### <a name="rr-single-alloc"></a>R.13 : Effectuez au plus une allocation explicite de ressource dans une seule instruction d'expression

##### Raison

Si vous effectuez deux allocations explicites dans une seule instruction, vous pourriez perdre des ressources en raison de l'ordre d'évaluation des nombreuses sous‑expressions, y compris les arguments de fonction, qui est non spécifié.

##### Exemple

    void fun(shared_ptr<Widget> sp1, shared_ptr<Widget> sp2);

Cette fonction `fun` peut être appelée comme ceci :

    // MAUVAISE : fuite potentielle
    fun(shared_ptr<Widget>(new Widget(a, b)), shared_ptr<Widget>(new Widget(c, d)));

Cette approche est non sécurisée par rapport aux exceptions parce que le compilateur pourrait réordonner les deux expressions créant les deux arguments de la fonction.  
En particulier, le compilateur peut intercaler l'exécution des deux expressions : l'allocation de mémoire (en appelant `operator new`) peut être faite d'abord pour les deux objets, suivie des appels aux deux constructeurs de `Widget`. Si l'un des appels de constructeur lève une exception, l'autre objet ne verra jamais sa mémoire libérée !

Ce problème subtil a une solution simple : ne jamais effectuer plus d'une allocation explicite de ressource dans une seule instruction d'expression.  
Par exemple :

    shared_ptr<Widget> sp1(new Widget(a, b)); // Mieux, mais embêtant
    fun(sp1, new Widget(c, d));

La meilleure solution est d'éviter complètement l'allocation explicite, d'utiliser des fonctions de fabrique qui retournent des objets propriétaires :

    fun(make_shared<Widget>(a, b), make_shared<Widget>(c, d)); // Meilleur

Créer votre propre wrapper de fabrique si ce n'est pas déjà disponible.

##### Application

* Signaler les expressions avec plusieurs allocations explicites de ressource.  

### <a name="rr-ap"></a>R.14 : Évitez les paramètres `[]`, préférez `span`

##### Raison

Un tableau décale en pointeur, ce qui fait perdre sa taille, ouvrant l'opportunité d'erreurs de plage.  
Utilisez `span` pour préserver les informations de taille.

##### Exemple

    void f(int[]);          // pas conseillé

    void f(int*);           // pas conseillé pour plusieurs objets
                            // (un pointeur doit pointer vers un seul objet, ne pas le sous‑indexer)

    void f(gsl::span<int>); // bon, recommandé

##### Application

Signaler les paramètres `[]`. Utiliser `span` à la place.

### <a name="rr-pair"></a>R.15 : Survolez toujours les paires allocation/désallocation correspondantes

##### Raison

Sinon, vous obtenez des opérations déséquilibrées et du chaos.

##### Exemple

    class X {
        // ...
        void* operator new(size_t s);
        void operator delete(void*);
        // ...
    };

##### Remarque

Si vous voulez de la mémoire qui ne peut pas être désallouée, `=delete` l'opération de désallocation. Ne la laissez pas déclarée sans implémentation.

##### Application

Signaler les paires incomplètes.

## <a name="ss-smart"></a>R.smart : Pointeurs intelligents

### <a name="rr-owner"></a>R.20 : Utilisez `unique_ptr` ou `shared_ptr` pour représenter la propriété

##### Raison

Ils peuvent empêcher les fuites de ressources.

##### Exemple

Considérez :

    void f()
    {
        X* p1 { new X };              // mauvais, p1 fût une fuite
        auto p2 = make_unique<X>();   // bon, propriété unique
        auto p3 = make_shared<X>();   // bon, propriété partagée
    }

Cela fera fuites l'objet utilisé pour initialiser `p1` (seul).

##### Application

* (Simple) Avertir si la valeur de retour de `new` est assignée à un pointeur brut.  
* (Simple) Avertir si le résultat d'une fonction retournant un pointeur propriétaire brut est assigné à un pointeur brut.

### <a name="rr-unique"></a>R.21 : Préférez `unique_ptr` à `shared_ptr` sauf si vous avez besoin de partager la propriété

##### Raison

Un `unique_ptr` est conceptuellement plus simple et plus prévisible (vous savez quand la destruction se produit) et plus rapide (vous ne maintenez pas implicitement un compteur d'utilisation).

##### Exemple, mauvais

Cette approche ajoute inutilement et maintient un compteur de référence.

    void f()
    {
        shared_ptr<Base> base = make_shared<Derived>();
        // utilisez localement base, sans le copier -- le compteur ne dépasse jamais 1
    } // détruit base

##### Exemple

Ceci est plus efficace :

    void f()
    {
        unique_ptr<Base> base = make_unique<Derived>();
        // utilisez localement base
    } // détruit base

##### Application

(Simp.) Avertir si une fonction utilise un `Shared_pointer` avec un objet alloué dans la fonction, mais ne retourne jamais le `Shared_pointer` ou ne le passe pas à une fonction nécessitant un `Shared_pointer`. Suggérer d'utiliser `unique_ptr` à la place.

### <a name="rr-make_shared"></a>R.22 : Utilisez `make_shared()` pour créer des `shared_ptr`

##### Raison

`make_shared` fournit une déclaration plus concise de la construction.  
Il offre également la possibilité d'éliminer une allocation séparée pour les compteurs de référence, en plaçant les compteurs de référence du `shared_ptr` à côté de l'objet.  
Il assure également la sécurité des exceptions dans des expressions complexes (dans le code pré‑C++17).

##### Exemple

Considérez :

    shared_ptr<X> p1 { new X{2} }; // mauvais
    auto p = make_shared<X>(2);    // bon

La version `make_shared()` mentionne `X` une seule fois, alors elle est généralement plus courte (et plus rapide) que la version avec l'`new` explicite.

##### Application

(Simp.) Avertir si un `shared_ptr` est construit à partir du résultat d'un `new` au lieu de `make_shared`.

### <a name="rr-make_unique"></a>R.23 : Utilisez `make_unique()` pour créer des `unique_ptr`

##### Raison

`make_unique` fournit une déclaration plus concise de la construction.  
Il assure également la sécurité des exceptions dans des expressions complexes (dans le code pré‑C++17).

##### Exemple

    unique_ptr<Foo> p {new Foo{7}};    // OK : mais répétitif

    auto q = make_unique<Foo>(7);      // Meilleur : pas de répétition de Foo

##### Application

(Simp.) Avertir si un `unique_ptr` est construit à partir du résultat d'un `new` au lieu de `make_unique`.

### <a name="rr-weak_ptr"></a>R.24 : Utilisez `std::weak_ptr` pour rompre les cycles de `shared_ptr`

##### Raison

Les `shared_ptr` utilisent le comptage d'utilisation et leur compteur d'utilisation pour les structures cycliques ne atteint jamais zéro, donc il faut un mécanisme pour pouvoir détruire une structure cyclique.

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
                // Utilisez *shared_back_reference
            }
        }
    private:
        std::weak_ptr<foo> back_reference_;
    };

##### Remarque

??? (HS: A lot of people say "to break cycles", while I think "temporary shared ownership" is more to the point.)  
???(BS: breaking cycles is what you must do; temporarily sharing ownership is how you do it.  
You could "temporarily share ownership" simply by using another `shared_ptr`.)

##### Application

??? probablement impossible. Si nous pouvions détecter les cycles statiquement, nous n'aurions pas besoin de `weak_ptr`.

### <a name="rr-smartptrparam"></a>R.30 : Prenez les pointeurs intelligents en paramètres uniquement pour exprimer explicitement les sémantiques de durée de vie

Voir [F.7](006-functions.md#rf-smart).

### <a name="rr-smart"></a>R.31 : Si vous avez des pointeurs intelligents non‑`std`, suivez le modèle de base de `std`

##### Raison

Les règles de la section suivante fonctionnent également pour d'autres types de pointeurs intelligents tiers et sont très utiles pour diagnostiquer les problèmes courants de pointeurs intelligents qui causent des problèmes de performance et de correction.  
Vous voulez que les règles fonctionnent pour tous les pointeurs intelligents que vous utilisez.

Tout type (y compris le modèle primaire ou l'extension) qui surcharge l'opérateur unaires `*` et `->` est considéré comme un pointeur intelligent :

* S'il est copiable, il est reconnu comme un `shared_ptr` comptage de référence.  
* S'il n'est pas copiable, il est reconnu comme un `unique_ptr` unique.

##### Exemple, mauvais

    // utiliser intrusive_ptr de Boost
    #include <boost/intrusive_ptr.hpp>
    void f(boost::intrusive_ptr<widget> p)  // erreur sous la règle 'sharedptrparam'
    {
        p->foo();
    }

    // utiliser CComPtr de Microsoft
    #include <atlbase.h>
    void f(CComPtr<widget> p)               // erreur sous la règle 'sharedptrparam'
    {
        p->foo();
    }

Les deux cas sont des erreurs sous la directive `sharedptrparam`: `p` est un `Shared_pointer`, mais rien dans son utilisation ne reflète la propriété; la passer par valeur est une pessimisation silencieuse; ces fonctions devraient accepter un `widget*`, s'ils peuvent être `nullptr`. Sinon, idéalement, la fonction devrait accepter un `widget&`.  
Ces pointeurs intelligents répondent au concept `Shared_pointer`, donc ces règles fonctionnent sur eux et exposent les mauvaises optimisations courantes.

### <a name="rr-uniqueptrparam"></a>R.32 : Prenez un paramètre `unique_ptr<widget>` afin d'exprimer que la fonction assume la propriété d'un `widget`

##### Raison

L'utilisation de `unique_ptr` de cette façon documente et impose le transfert de propriété d'une fonction.

##### Exemple

    void sink(unique_ptr<widget>); // prend la propriété du widget

    void uses(widget*);            // juste utilise le widget

##### Application

* (Simple) Avertir si une fonction prend un paramètre `Unique_pointer<T>` par référence à chaînel et ne l'assign ne pas appelle `reset()` sur au moins un chemin de code. Suggérer d'utiliser un `T*` ou `T&` à la place.

### <a name="rr-reseat"></a>R.33 : Prenez un paramètre `unique_ptr<widget>&` afin d'exprimer que la fonction réinstalle le `widget`

##### Raison

Utiliser `unique_ptr` de cette façon à la fois documente et impose les sémantiques de réinstallation de la fonction.

##### Remarque

> “réinstaller” signifie “faire pointer le pointeur ou le pointeur intelligent vers un objet différent”.

##### Exemple

    void reseat(unique_ptr<widget>&); // "prévoit" ou "pourrait" réinstaller le pointeur

##### Application

* (Simple) Avertir si une fonction prend un paramètre `Unique_pointer<T>` par référence à chaînel et ne l'assign ne pas appelle `reset()` sur au moins un chemin de code. Suggérer d'utiliser un `T*` ou `T&` à la place.

### <a name="rr-sharedptrparam-owner"></a>R.34 : Prenez un paramètre `shared_ptr<widget>` afin d'exprimer la propriété partagée

##### Raison

Cela rend l'était de propriété partagée explicite.

##### Exemple, bon

    class WidgetUser
    {
    public:
        // WidgetUser va partager la propriété du widget
        explicit WidgetUser(std::shared_ptr<widget> w) noexcept:
            m_widget{std::move(w)} {}
        // ...
    private:
        std::shared_ptr<widget> m_widget;
    };

##### Application

* (Simple) Avertir si une fonction prend un paramètre `Shared_pointer<T>` par référence à chaînel et ne l'assign ne pas appelle `reset()` sur au moins un chemin de code. Suggérer d'utiliser un `T*` ou `T&` à la place.  
* (Simple) ((Fondamental)) Avertir si une fonction prend un paramètre `Shared_pointer<T>` par valeur ou par référence à `const` et ne copie ou ne déplace pas le `Shared_pointer` vers un autre `Shared_pointer` sur au moins un chemin de code. Suggérer d'utiliser un `T*` ou `T&` à la place.  
* (Simple) ((Fondamental)) Avertir si une fonction prend un paramètre `Shared_pointer<T>` par référence à r-value. Suggérer de le prendre par valeur à la place.

### <a name="rr-sharedptrparam"></a>R.35 : Prenez un paramètre `shared_ptr<widget>&` afin d'exprimer que la fonction peut réinstaller le pointeur partagé

##### Raison

Cela rend la réinstallation explicite.

##### Remarque

> “réinstaller” signifie “faire pointer ou faire pointer un pointeur intelligent vers un objet différent”.

##### Exemple, bon

    void ChangeWidget(std::shared_ptr<widget>& w)
    {
        // Cela va changer le widget du client
        w = std::make_shared<widget>(widget{});
    }

##### Application

* (Simple) Avertir si une fonction prend un paramètre `Shared_pointer<T>` par référence à chaînel et ne l'assign ne pas appelle `reset()` sur au moins un chemin de code. Suggérer d'utiliser un `T*` ou `T&` à la place.  
* (Simple) ((Fondamental)) Avertir si une fonction prend un paramètre `Shared_pointer<T>` par valeur ou par référence à `const` et ne copie ou ne déplace pas le `Shared_pointer` vers un autre `Shared_pointer` sur au moins un chemin de code. Suggérer d'utiliser un `T*` ou `T&` à la place.  
* (Simple) ((Fondamental)) Avertir si une fonction prend un paramètre `Shared_pointer<T>` par référence à r-value. Suggérer de le prendre par valeur à la place.

### <a name="rr-sharedptrparam-const"></a>R.36 : Prenez un paramètre `const shared_ptr<widget>&` afin d'exprimer qu'il peut retenir le compte de référence de l'objet ???

##### Raison

Cela rend l'étât de retient le compte de référence explicite.

##### Exemple, bon

    void share(shared_ptr<widget>);            // share – "retient" le compte de référence

    void reseat(shared_ptr<widget>&);          // "réinstalle" le pointeur

    void may_share(const shared_ptr<widget>&); // "pouvait" retenir le compte de référence

##### Application

* (Simple) Avertir si une fonction prend un paramètre `Shared_pointer<T>` par référence à chaînel et ne l'assign ne pas appelle `reset()` sur au moins un chemin de code. Suggérer d'utiliser un `T*` ou `T&` à la place.  
* (Simple) ((Fondamental)) Avertir si une fonction prend un paramètre `Shared_pointer<T>` par valeur ou par référence à `const` et ne copie ou ne déplace pas le `Shared_pointer` vers un autre `Shared_pointer` sur au moins un chemin de code. Suggérer d'utiliser un `T*` ou `T&` à la place.  
* (Simple) ((Fondamental)) Avertir si une fonction prend un paramètre `Shared_pointer<T>` par référence à r-value. Suggérer de le prendre par valeur à la place.

### <a name="rr-smartptrget"></a>R.37 : Ne pas transmettre un pointeur ou une référence obtenus à partir d'un pointeur intelligent alié

##### Raison

Violant cette règle est la principale cause de la perte de compte de référence et de se retrouver avec un pointeur pendante.  
Les fonctions devraient préférer passer des pointeurs bruts et des références le long de la chaîne d'appel.  
Au sommet de l'arbre d'appel où vous obtenez le pointeur brut ou la référence d'un pointeur intelligent qui maintient l'objet vivant.  
Vous devez être sûr que le pointeur intelligent ne sera pas inadvertidèle réinitialisé ou réassigné dans l'arbre d'appel du dessous.

##### Note

Pour le faire, il faut parfois prendre une copie locale d'un pointeur intelligent, qui garantira fermement que l'objet est vivant pendant tout le temps de la fonction et de l'arbre d'appel.

##### Exemple

Considérez ce code :

    // global (static ou heap), ou aliased local ...
    shared_ptr<widget> g_p = ...;

    void f(widget& w)
    {
        g();
        use(w);  // A
    }

    void g()
    {
        g_p = ...; // Oups, si c'était le dernier shared_ptr vers ce widget, détruit le widget
    }

Le code suivant ne doit pas passer la revue de code :

    void my_code()
    {
        // MAUVAISE : passer un pointeur ou une référence obtenu d'un shared_ptr non local pouvant être réinitialisé quelque part dans f ou ses appelants
        f(*g_p);

        // MAUVAISE : même raison, juste le passer comme un pointeur "this"
        g_p->func();
    }

La correction est simple – prenez un local copy du pointeur pour "retener un ref count" pendant toute la fonction et l'arbre d'appel :

    void my_code()
    {
        // bon : 1 incrément couvre l'ensemble de cette fonction et tous les appels en dessous
        auto pin = g_p;

        // BON : passer un pointeur ou une référence obtenu d'un pointeur intelligent local non aliasé
        f(*pin);

        // BON : même raison
        pin->func();
    }

##### Application

* (Simple) Avertir si un pointeur ou une référence obtenu d'un pointeur intelligent variable (`Unique_pointer` ou `Shared_pointer`) qui est non local, ou qui est local mais potentiellement aliasé, est utilisé dans un appel de fonction. S'il s'agit d'un `Shared_pointer` alors suggérer de prendre une copie locale du pointeur intelligent et d'obtenir un pointeur ou une référence à partir de celui‑ci à la place.