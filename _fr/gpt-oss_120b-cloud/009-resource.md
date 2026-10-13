# <a name="s-resource"></a>R : Gestion des ressources

Cette section contient les règles relatives aux ressources.  
Une ressource est tout ce qui doit être acquis et (explicitement ou implicitement) libéré, comme la mémoire, les descripteurs de fichiers, les sockets et les verrous.  
La raison de sa libération est généralement qu’elle peut être en quantité limitée, donc même une libération différée peut être préjudiciable.  
L’objectif fondamental est de s’assurer qu’on ne fuit aucune ressource et qu’on ne conserve jamais une ressource plus longtemps que nécessaire.  
Une entité responsable de la libération d’une ressource est appelée **propriétaire**.

Il existe quelques cas où les fuites peuvent être acceptables voire optimales :
* Si vous écrivez un programme qui se contente de produire une sortie à partir d’une entrée et que la quantité de mémoire nécessaire est proportionnelle à la taille de l’entrée, la stratégie optimale (pour les performances et la facilité de programmation) consiste parfois à ne jamais supprimer quoi que ce soit.  
* Si vous disposez de suffisamment de mémoire pour gérer votre plus grande entrée, vous pouvez laisser la mémoire fuiter, mais assurez‑vous d’afficher un bon message d’erreur en cas d’erreur.

Nous ignorons ici de tels cas.

### Résumé des règles de gestion des ressources :

* [R.1 : Gérer les ressources automatiquement à l’aide de handles de ressources et du RAII (Resource Acquisition Is Initialization)](009-resource.md#rr-raii)  
* [R.2 : Dans les interfaces, utiliser des pointeurs nus pour désigner des objets individuels (uniquement)](009-resource.md#rr-use-ptr)  
* [R.3 : Un pointeur nu (un `T*`) ne possède pas la ressource](009-resource.md#rr-ptr)  
* [R.4 : Une référence nue (un `T&`) ne possède pas la ressource](009-resource.md#rr-ref)  
* [R.5 : Préférer les objets à portée locale, éviter les allocations sur le tas inutiles](009-resource.md#rr-scoped)  
* [R.6 : Éviter les variables globales non `const`](009-resource.md#rr-global)

### Résumé des règles d’allocation et de désallocation :

* [R.10 : Éviter `malloc()` et `free()`](009-resource.md#rr-mallocfree)  
* [R.11 : Éviter d’appeler explicitement `new` et `delete`](009-resource.md#rr-newdelete)  
* [R.12 : Transmettre immédiatement le résultat d’une allocation de ressource explicite à un objet gestionnaire](009-resource.md#rr-immediate-alloc)  
* [R.13 : Effectuer au plus une allocation de ressource explicite dans une instruction d’expression unique](009-resource.md#rr-single-alloc)  
* [R.14 : Éviter les paramètres `[]`, préférer `span`](009-resource.md#rr-ap)  
* [R.15 : Toujours surcharger les paires d’allocation/désallocation correspondantes](009-resource.md#rr-pair)

* <a name="rr-summary-smartptrs"></a>Résumé des règles concernant les pointeurs intelligents :

  * [R.20 : Utiliser `unique_ptr` ou `shared_ptr` pour représenter la propriété](009-resource.md#rr-owner)  
  * [R.21 : Préférer `unique_ptr` à `shared_ptr` sauf si vous avez besoin de partager la propriété](009-resource.md#rr-unique)  
  * [R.22 : Utiliser `make_shared()` pour créer des `shared_ptr`](009-resource.md#rr-make_shared)  
  * [R.23 : Utiliser `make_unique()` pour créer des `unique_ptr`](009-resource.md#rr-make_unique)  
  * [R.24 : Utiliser `std::weak_ptr` pour rompre les cycles de `shared_ptr`](009-resource.md#rr-weak_ptr)  
  * [R.30 : Prendre les pointeurs intelligents comme paramètres uniquement pour exprimer explicitement les sémantiques de durée de vie](009-resource.md#rr-smartptrparam)  
  * [R.31 : Si vous avez des pointeurs intelligents non‑`std`, suivre le modèle de base de `std`](009-resource.md#rr-smart)  
  * [R.32 : Prendre un paramètre `unique_ptr<widget>` pour indiquer qu’une fonction assume la propriété d’un `widget`](009-resource.md#rr-uniqueptrparam)  
  * [R.33 : Prendre un paramètre `unique_ptr<widget>&` pour indiquer qu’une fonction réassigne le `widget`](009-resource.md#rr-reseat)  
  * [R.34 : Prendre un paramètre `shared_ptr<widget>` pour exprimer la propriété partagée](009-resource.md#rr-sharedptrparam-owner)  
  * [R.35 : Prendre un paramètre `shared_ptr<widget>&` pour indiquer qu’une fonction peut réassigner le pointeur partagé](009-resource.md#rr-sharedptrparam)  
  * [R.36 : Prendre un paramètre `const shared_ptr<widget>&` pour indiquer qu’il pourrait retenir un compteur de références sur l’objet ???](009-resource.md#rr-sharedptrparam-const)  
  * [R.37 : Ne pas passer un pointeur ou une référence obtenus à partir d’un pointeur intelligent aliassé](009-resource.md#rr-smartptrget)

### <a name="rr-raii"></a>R.1 : Gérer les ressources automatiquement à l’aide de handles de ressources et du RAII (Resource Acquisition Is Initialization)

##### Raison

Éviter les fuites et la complexité de la gestion manuelle des ressources.  
La symétrie constructeur/destructeur imposée par le langage C++ reflète la symétrie inhérente aux paires de fonctions d’acquisition/libération de ressources telles que `fopen`/`fclose`, `lock`/`unlock` et `new`/`delete`.  
Chaque fois que vous manipulez une ressource nécessitant des appels de fonctions d’acquisition/libération appariés, encapsulez cette ressource dans un objet qui impose l’appariement pour vous — acquérez la ressource dans son constructeur et libérez‑la dans son destructeur.

##### Exemple, mauvaise pratique

Considérez :

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

Dans ce code, vous devez vous souvenir d’appeler `unlock`, `close_port` et `delete` sur tous les chemins, et de le faire exactement une fois. De plus, si l’une des sections marquées `...` lève une exception, alors `x` sera fuité et `my_mutex` restera verrouillé.

##### Exemple

Considérez :

    void send(unique_ptr<X> x, string_view destination)  // x possède le X
    {
        Port port{destination};            // port possède le PortHandle
        lock_guard<mutex> guard{my_mutex}; // guard possède le lock
        // ...
        send(port, x);
        // ...
    } // déverrouille automatiquement my_mutex et supprime le pointeur dans x

Maintenant, tout le nettoyage des ressources est automatique, effectué une fois sur tous les chemins, qu’il y ait ou non une exception. En prime, la fonction indique désormais qu’elle prend possession du pointeur.

Qu’est‑ce que `Port` ? Un wrapper pratique qui encapsule la ressource :

    class Port {
        PortHandle port;
    public:
        Port(string_view destination) : port{open_port(destination)} { }
        ~Port() { close_port(port); }
        operator PortHandle() { return port; }

        // les handles de port ne peuvent généralement pas être clonés, donc désactiver la copie et l'affectation si nécessaire
        Port(const Port&) = delete;
        Port& operator=(const Port&) = delete;
    };

##### Note

Là où une ressource se comporte mal du fait qu’elle n’est pas représentée comme une classe avec un destructeur, encapsulez‑la dans une classe ou utilisez [`finally`](013-errors.md#re-finally).

**Voir aussi** : [RAII](013-errors.md#re-raii)

### <a name="rr-use-ptr"></a>R.2 : Dans les interfaces, utiliser des pointeurs nus pour désigner des objets individuels (uniquement)

##### Raison

Les tableaux sont mieux représentés par un type de conteneur (par ex., `vector` (possédant)) ou un `span` (non possédant). Ces conteneurs et vues contiennent suffisamment d’informations pour effectuer des vérifications de portée.

##### Exemple, mauvaise pratique

    void f(int* p, int n)   // n est le nombre d’éléments dans p[]
    {
        // ...
        p[2] = 7;   // mauvaise pratique : sous‑script d’un pointeur nu
        // ...
    }

Le compilateur ne lit pas les commentaires, et sans lire le reste du code vous ne savez pas si `p` pointe réellement sur `n` éléments. Utilisez plutôt un `span`.

##### Exemple

    void g(int* p, int fmt)   // afficher *p en utilisant le format #fmt
    {
        // ... utilise uniquement *p et p[0] ...
    }

##### Exception

Les chaînes de caractères de style C sont passées sous forme d’un pointeur unique vers une séquence de caractères terminée par zéro. Utilisez `zstring` plutôt que `char*` pour indiquer que vous vous appuyez sur cette convention.

##### Note

De nombreux usages actuels de pointeurs vers un seul élément pourraient être des références. Cependant, lorsqu’un `nullptr` est une valeur possible, une référence peut ne pas être une alternative raisonnable.

##### Enforcement

* Signaler l'arithmétique de pointeur (y compris `++`) sur un pointeur qui ne fait pas partie d’un conteneur, d’une vue ou d’un itérateur.  
* Cette règle générerait un grand nombre de faux positifs si elle était appliquée à une base de code plus ancienne.  
* Signaler les noms de tableaux passés comme pointeurs simples.

### <a name="rr-ptr"></a>R.3 : Un pointeur nu (un `T*`) ne possède pas la ressource

##### Raison

Il n’y a aucune disposition (dans la norme C++ ou dans la plupart des codes) indiquant le contraire et la plupart des pointeurs nus ne possèdent pas la ressource. Nous voulons identifier les pointeurs propriétaires afin de pouvoir supprimer de façon fiable et efficace les objets pointés par ces pointeurs.

##### Exemple

    void f()
    {
        int* p1 = new int{7};           // mauvaise pratique : pointeur propriétaire nu
        auto p2 = make_unique<int>(7);  // OK : l’entier est possédé par un pointeur unique
        // ...
    }

Le `unique_ptr` protège contre les fuites en garantissant la suppression de son objet (même en présence d’exceptions). Le `T*` ne le fait pas.

##### Exemple

    template<typename T>
    class X {
    public:
        T* p;   // mauvaise pratique : il n’est pas clair si `p` possède ou non
        T* q;   // mauvaise pratique : il n’est pas clair si `q` possède ou non
        // ...
    };

Nous pouvons corriger ce problème en rendant la propriété explicite :

    template<typename T>
    class X2 {
    public:
        owner<T*> p;  // OK : `p` possède
        T* q;         // OK : `q` ne possède pas
        // ...
    };

##### Exception

Une classe majeure d'exception est le code hérité, en particulier le code qui doit rester compilable en C ou interagir avec le C et le C‑style C++ via les ABI. Le fait qu’il y ait des milliards de lignes de code qui violent cette règle concernant les `T*` possédants ne peut être ignoré. Nous aimerions bien voir des outils de transformation de programmes transformer du code « legacy » de 20 ans en code moderne éclatant ; nous encourageons le développement, le déploiement et l’utilisation de tels outils, nous espérons que les lignes directrices aideront le développement de ces outils, et nous avons même contribué (et continuons de contribuer) à la recherche et au développement dans ce domaine. Cependant, cela prendra du temps : le « legacy code » est généré plus rapidement que nous ne pouvons rénover l'ancien code, et cela restera le cas pendant quelques années.

Ce code ne peut pas être entièrement réécrit (même en supposant de bons outils de transformation), surtout pas rapidement. Ce problème ne peut pas être résolu (à grande échelle) simplement en transformant tous les pointeurs possédants en `unique_ptr` et `shared_ptr`, partiellement parce que nous avons besoin/utilisons des « raw pointers » possédants ainsi que des pointeurs simples dans l’implémentation de nos handles de ressources fondamentaux. Par exemple, les implémentations courantes de `vector` possèdent un pointeur propriétaire et deux pointeurs non possédants. De nombreuses ABI (et essentiellement toutes les interfaces vers du code C) utilisent des `T*`, certains d'entre eux étant possédants. Certaines interfaces ne peuvent pas être simplement annotées avec `owner` parce qu’elles doivent rester compilables en C (bien que cela pourrait être un usage rare mais judicieux d’une macro qui s’étend à `owner` uniquement en mode C++).

##### Note

`owner<T*>` n’a aucune sémantique par défaut au‑delà de `T*`. Il peut être utilisé sans modifier le code qui l’utilise et sans affecter les ABI. C’est simplement un indicateur pour les programmeurs et les outils d’analyse. Par exemple, si un `owner<T*>` est un membre d’une classe, cette classe doit de préférence disposer d’un destructeur qui le `delete`.

##### Exemple, mauvaise pratique

    Gadget* make_gadget(int n)
    {
        auto p = new Gadget{n};
        // ...
        return p;
    }

    void caller(int n)
    {
        auto p = make_gadget(n);   // n’oubliez pas de supprimer `p`
        // ...
        delete p;
    }

En plus de souffrir du problème de [leak](004-philosophy.md#rp-leak), cela ajoute une opération d’allocation et de désallocation superflue, et le code devient inutilement verbeux. Si `Gadget` est peu coûteux à déplacer hors d’une fonction (c’est‑à‑dire petit ou possède une opération de déplacement efficace), renvoyez‑le « par valeur » (voir ["out" return values](006-functions.md#rf-out)) :

    Gadget make_gadget(int n)
    {
        Gadget g{n};
        // ...
        return g;
    }

##### Note

Cette règle s’applique aux fonctions fabrique.

##### Note

Si une sémantique de pointeur est requise (par ex., parce que le type de retour doit référencer une classe de base d’une hiérarchie de classes (une interface)), renvoyez un « pointeur intelligent ».

##### Enforcement

* (Simple) Avertir lorsqu’un `delete` est appliqué à un pointeur nu qui n’est pas un `owner<T>`.  
* (Modéré) Avertir en cas d’échec à `reset` ou à supprimer explicitement un pointeur `owner<T>` sur chaque chemin de code.  
* (Simple) Avertir si la valeur renvoyée par `new` est assignée à un pointeur nu.  
* (Simple) Avertir si une fonction renvoie un objet qui a été alloué à l’intérieur de la fonction mais possède un constructeur de déplacement. Suggérer de le renvoyer par valeur à la place.

### <a name="rr-ref"></a>R.4 : Une référence nue (un `T&`) ne possède pas la ressource

##### Raison

Il n’y a aucune disposition (dans la norme C++ ou dans la plupart des codes) indiquant le contraire et la plupart des références nus ne possèdent pas la ressource. Nous voulons identifier les propriétaires afin de pouvoir supprimer de façon fiable et efficace les objets pointés par ces pointeurs.

##### Exemple

    void f()
    {
        int& r = *new int{7};  // mauvaise pratique : référence propriétaire nue
        // ...
        delete &r;             // mauvaise pratique : violation de la règle interdisant la suppression de pointeurs nus
    }

**Voir aussi** : [La règle du pointeur nu](009-resource.md#rr-ptr)

##### Enforcement

Voir [la règle du pointeur nu](009-resource.md#rr-ptr)

### <a name="rr-scoped"></a>R.5 : Préférer les objets à portée locale, éviter les allocations sur le tas inutiles

##### Raison

Un objet à portée locale est un objet local, global ou un membre. Cela implique qu’il n’y a pas de coût d’allocation ou de désallocation supplémentaire à part celui déjà utilisé pour la portée ou l’objet contenant. Les membres d’un tel objet sont eux‑mêmes à portée locale et le constructeur et le destructeur de l’objet gèrent la durée de vie de ces membres.

##### Exemple

    void f(int n)
    {
        auto p = new Gadget{n};
        // ...
        delete p;
    }

Au lieu de cela, utilisez une variable locale :

    void f(int n)
    {
        Gadget g{n};
        // ...
    }

##### Enforcement

* (Modéré) Avertir si un objet est alloué puis désalloué sur tous les chemins d’une fonction. Suggérer qu’il devrait être un objet local sur la pile.  
* (Simple) Avertir si un `Unique_pointer` ou `Shared_pointer` local qui n’est ni déplacé, ni copié, ni réassigné, ni `reset` avant la fin de sa durée de vie n’est pas déclaré `const`. Exception : ne pas émettre cet avertissement pour un `Unique_pointer` local pointant vers un tableau non borné. (Voir ci‑dessous.)

##### Exception

Si votre espace de pile est limité, il est acceptable de créer un `unique_ptr<BigObject>` local `const` pour stocker l’objet sur le tas plutôt que sur la pile.

### <a name="rr-global"></a>R.6 : Éviter les variables globales non `const`

Voir [I.2](005-interfaces.md#ri-global)

## <a name="ss-alloc"></a>R.alloc : Allocation et désallocation

### <a name="rr-mallocfree"></a>R.10 : Éviter `malloc()` et `free()`

##### Raison

`malloc()` et `free()` ne supportent pas la construction et la destruction, et ne se combinent pas bien avec `new` et `delete`.

##### Exemple

    class Record {
        int id;
        string name;
        // ...
    };

    void use()
    {
        // p1 peut être nul
        // *p1 n’est pas initialisé ; en particulier,
        // cette chaîne n’est pas une chaîne, mais un sac de bits de la taille d’une chaîne
        Record* p1 = static_cast<Record*>(malloc(sizeof(Record)));

        auto p2 = new Record;

        // sauf si une exception est levée, *p2 est initialisé par défaut
        auto p3 = new(nothrow) Record;
        // p3 peut être nul ; sinon, *p3 est initialisé par défaut

        // ...

        delete p1;    // erreur : impossible de supprimer un objet alloué par malloc()
        free(p2);    // erreur : impossible d’appeler free() sur un objet alloué par new
    }

Dans certaines implémentations, `delete` et `free()` peuvent fonctionner, ou bien ils provoqueront des erreurs d’exécution.

##### Exception

Il existe des applications et des portions de code où les exceptions ne sont pas acceptables.  
Parmi les meilleurs exemples, on trouve du code dur‑temps réel critique pour la vie.  
Attention, de nombreuses interdictions d’utiliser les exceptions reposent sur des superstitions (mauvaises) ou sur des préoccupations liées aux anciens bases de code avec une gestion de ressources non systématique (malheureusement, mais parfois nécessaire). Dans de tels cas, envisagez les versions `nothrow` de `new`.

##### Enforcement

Signaler l’utilisation explicite de `malloc` et `free`.

### <a name="rr-newdelete"></a>R.11 : Éviter d’appeler explicitement `new` et `delete`

##### Raison

Le pointeur retourné par `new` doit appartenir à un gestionnaire de ressource (pouvant appeler `delete`). Si le pointeur retourné par `new` est assigné à un pointeur nu, l’objet peut être fuité.

##### Note

Dans un grand programme, un `delete` nu (c’est‑à‑dire un `delete` dans le code applicatif, plutôt que dans du code dédié à la gestion des ressources) est très probablement un bug : si vous avez N `delete`, comment être sûr de ne pas avoir besoin de N+1 ou N‑1 ? Le bug peut être latent : il peut n’apparaître qu’à la maintenance. Si vous avez un `new` nu, vous avez probablement besoin d’un `delete` nu quelque part, ce qui indique probablement un bug.

##### Enforcement

(Simple) Avertir toute utilisation explicite de `new` et `delete`. Suggérer d’utiliser `make_unique` à la place.

### <a name="rr-immediate-alloc"></a>R.12 : Transmettre immédiatement le résultat d’une allocation de ressource explicite à un objet gestionnaire

##### Raison

Si vous ne le faites pas, une exception ou un retour pourrait entraîner une fuite.

##### Exemple, mauvaise pratique

    void func(const string& name)
    {
        FILE* f = fopen(name, "r");            // ouvrir le fichier
        vector<char> buf(1024);
        auto _ = finally([f] { fclose(f); });  // se rappeler de fermer le fichier
        // ...
    }

L’allocation de `buf` pourrait échouer et faire fuir le descripteur de fichier.

##### Exemple

    void func(const string& name)
    {
        ifstream f{name};   // ouvrir le fichier
        vector<char> buf(1024);
        // ...
    }

L’utilisation du descripteur de fichier (dans `ifstream`) est simple, efficace et sûre.

##### Enforcement

* Signaler les allocations explicites utilisées pour initialiser des pointeurs (problème : combien d’allocations de ressources directes pouvons‑nous reconnaître ?)

### <a name="rr-single-alloc"></a>R.13 : Effectuer au plus une allocation de ressource explicite dans une instruction d’expression unique

##### Raison

Si vous effectuez deux allocations de ressource explicites dans une même instruction, vous pourriez fuir des ressources parce que l’ordre d’évaluation de nombreuses sous‑expressions, y compris les arguments de fonction, n’est pas spécifié.

##### Exemple

    void fun(shared_ptr<Widget> sp1, shared_ptr<Widget> sp2);

Cette fonction `fun` peut être appelée ainsi :

    // MAUVAIS : fuite potentielle
    fun(shared_ptr<Widget>(new Widget(a, b)), shared_ptr<Widget>(new Widget(c, d)));

Ce code n’est pas sûr en cas d’exception parce que le compilateur pourrait réordonner les deux expressions construisant les arguments de la fonction. En particulier, le compilateur peut intercaler l’exécution des deux expressions : l’allocation mémoire (en appelant `operator new`) pourrait être faite d’abord pour les deux objets, suivie des tentatives d’appeler les deux constructeurs `Widget`. Si l’un des constructeurs lève une exception, la mémoire de l’autre objet ne sera jamais libérée !

Ce problème subtil a une solution simple : ne jamais effectuer plus d’une allocation de ressource explicite dans une instruction d’expression unique. Par exemple :

    shared_ptr<Widget> sp1(new Widget(a, b)); // mieux, mais verbeux
    fun(sp1, new Widget(c, d));

La meilleure solution est d’éviter complètement l’allocation explicite, en utilisant des fonctions‑fabrique qui retournent des objets possédants :

    fun(make_shared<Widget>(a, b), make_shared<Widget>(c, d)); // optimal

Écrivez votre propre wrapper de fabrique s’il n’en existe pas déjà.

##### Enforcement

* Signaler les expressions contenant plusieurs allocations de ressources explicites (problème : combien d’allocations de ressources directes pouvons‑nous reconnaître ?)

### <a name="rr-ap"></a>R.14 : Éviter les paramètres `[]`, préférer `span`

##### Raison

Un tableau se convertit en pointeur, perdant ainsi ses informations de taille, ouvrant la porte à des erreurs de dépassement de limites. Utilisez `span` pour conserver l’information de taille.

##### Exemple

    void f(int[]);          // non recommandé

    void f(int*);           // non recommandé pour plusieurs objets
                            // (un pointeur doit pointer vers un seul objet, ne pas sous‑script)

    void f(gsl::span<int>); // bon, recommandé

##### Enforcement

Signaler les paramètres `[]`. Utiliser `span` à la place.

### <a name="rr-pair"></a>R.15 : Surcharger toujours les paires d’allocation/désallocation correspondantes

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

Si vous voulez une mémoire qui ne peut pas être désallouée, `=delete` l’opération de désallocation. Ne la laissez pas non déclarée.

##### Enforcement

Signaler les paires incomplètes.

## <a name="ss-smart"></a>R.smart : Pointeurs intelligents

### <a name="rr-owner"></a>R.20 : Utiliser `unique_ptr` ou `shared_ptr` pour représenter la propriété

##### Raison

Ils peuvent prévenir les fuites de ressources.

##### Exemple

    void f()
    {
        X* p1 { new X };              // mauvaise pratique, p1 fuira
        auto p2 = make_unique<X>();   // bon, propriété unique
        auto p3 = make_shared<X>();   // bon, propriété partagée
    }

##### Enforcement

* (Simple) Avertir si la valeur retournée par `new` est assignée à un pointeur nu.  
* (Simple) Avertir si le résultat d’une fonction retournant un pointeur propriétaire nu est assigné à un pointeur nu.

### <a name="rr-unique"></a>R.21 : Préférer `unique_ptr` à `shared_ptr` sauf si vous avez besoin de partager la propriété

##### Raison

Un `unique_ptr` est conceptuellement plus simple et plus prévisible (vous savez quand la destruction se produit) et plus rapide (vous ne maintenez pas implicitement un compteur d’utilisation).

##### Exemple, mauvaise pratique

    void f()
    {
        shared_ptr<Base> base = make_shared<Derived>();
        // utiliser `base` localement, sans le copier — le compteur de références ne dépasse jamais 1
    } // destruction de `base`

##### Exemple

    void f()
    {
        unique_ptr<Base> base = make_unique<Derived>();
        // utiliser `base` localement
    } // destruction de `base`

##### Enforcement

(Simple) Avertir si une fonction utilise un `Shared_pointer` avec un objet alloué à l’intérieur de la fonction, mais ne retourne jamais le `Shared_pointer` ou ne le passe pas à une fonction qui nécessite un `Shared_pointer`. Suggérer d’utiliser `unique_ptr` à la place.

### <a name="rr-make_shared"></a>R.22 : Utiliser `make_shared()` pour créer des `shared_ptr`

##### Raison

`make_shared` fournit une expression plus concise de la construction.  
Il offre également la possibilité d’éliminer une allocation distincte pour les compteurs de références, en plaçant les compteurs d’utilisation du `shared_ptr` à côté de son objet.  
Il assure aussi la sécurité en cas d’exception dans des expressions complexes (dans le code pré‑C++17).

##### Exemple

    shared_ptr<X> p1 { new X{2} }; // mauvaise pratique
    auto p = make_shared<X>(2);    // bon

##### Enforcement

(Simple) Avertir si un `shared_ptr` est construit à partir du résultat de `new` plutôt que de `make_shared`.

### <a name="rr-make_unique"></a>R.23 : Utiliser `make_unique()` pour créer des `unique_ptr`

##### Raison

`make_unique` fournit une expression plus concise de la construction. Il assure également la sécurité en cas d’exception dans des expressions complexes (dans le code pré‑C++17).

##### Exemple

    unique_ptr<Foo> p {new Foo{7}};    // OK : mais répétitif

    auto q = make_unique<Foo>(7);      // Meilleur : pas de répétition de `Foo`

##### Enforcement

(Simple) Avertir si un `unique_ptr` est construit à partir du résultat de `new` plutôt que de `make_unique`.

### <a name="rr-weak_ptr"></a>R.24 : Utiliser `std::weak_ptr` pour rompre les cycles de `shared_ptr`

##### Raison

Les `shared_ptr` s’appuient sur le comptage d’utilisation et le compteur d’une structure cyclique n’atteint jamais zéro, il faut donc un mécanisme pour pouvoir détruire une structure cyclique.

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

??? (HS : Beaucoup de gens disent « to break cycles », alors que je pense que « temporary shared ownership » est plus exact.)  
??? (BS : rompre les cycles est ce que vous devez faire ; partager temporairement la propriété est la façon de le faire. Vous pourriez « temporary shared ownership » simplement en utilisant un autre `shared_ptr`.)

##### Enforcement

??? probablement impossible. Si nous pouvions détecter statiquement les cycles, nous n’aurions pas besoin de `weak_ptr`.

### <a name="rr-smartptrparam"></a>R.30 : Prendre les pointeurs intelligents comme paramètres uniquement pour exprimer explicitement les sémantiques de durée de vie

Voir [F.7](006-functions.md#rf-smart).

### <a name="rr-smart"></a>R.31 : Si vous avez des pointeurs intelligents non‑`std`, suivre le modèle de base de `std`

##### Raison

Les règles de la section suivante s’appliquent également à d’autres types de pointeurs intelligents tiers et personnalisés et sont très utiles pour diagnostiquer les erreurs courantes de pointeurs intelligents qui provoquent des problèmes de performance et de correction. Vous voulez que les règles fonctionnent avec tous les pointeurs intelligents que vous utilisez.

Tout type (y compris le template primaire ou ses spécialisations) qui surcharge l’opérateur unaire `*` et `->` est considéré comme un pointeur intelligent :
* S’il est copiable, il est reconnu comme un `shared_ptr` à comptage de références.  
* S’il n’est pas copiable, il est reconnu comme un `unique_ptr`.

##### Exemple, mauvaise pratique

    // utilisation de `intrusive_ptr` de Boost
    #include <boost/intrusive_ptr.hpp>
    void f(boost::intrusive_ptr<widget> p)  // erreur selon la règle 'sharedptrparam'
    {
        p->foo();
    }

    // utilisation de `CComPtr` de Microsoft
    #include <atlbase.h>
    void f(CComPtr<widget> p)               // erreur selon la règle 'sharedptrparam'
    {
        p->foo();
    }

Ces deux cas constituent une erreur selon la [directive `sharedptrparam`](009-resource.md#rr-smartptrparam) : `p` est un `Shared_pointer`, mais aucune information sur son partage n’est utilisée ici et le passer par valeur entraîne une pessimisation silencieuse ; ces fonctions ne doivent accepter un pointeur intelligent que si elles ont besoin de participer à la gestion de la durée de vie du widget. Sinon, elles devraient accepter un `widget*`, si celui‑ci peut être `nullptr`. Idéalement, la fonction devrait accepter un `widget&`. Ces pointeurs intelligents correspondent au concept `Shared_pointer`, donc les règles d’application de ces directives fonctionnent immédiatement sur eux et mettent en évidence cette pessimisation courante.

### <a name="rr-uniqueptrparam"></a>R.32 : Prendre un paramètre `unique_ptr<widget>` pour indiquer qu’une fonction assume la propriété d’un `widget`

##### Raison

Utiliser `unique_ptr` de cette façon documente et impose le transfert de propriété de l’appel de fonction.

##### Exemple

    void sink(unique_ptr<widget>); // prend la propriété du widget

    void uses(widget*);            // se contente d’utiliser le widget

##### Enforcement

* (Simple) Avertir si une fonction prend un paramètre `Unique_pointer<T>` par référence lvalue et n’assigne pas à celui‑ci ou n’appelle pas `reset()` au moins sur un chemin de code. Suggérer de prendre un `T*` ou un `T&` à la place.

### <a name="rr-reseat"></a>R.33 : Prendre un paramètre `unique_ptr<widget>&` pour indiquer qu’une fonction réassigne le `widget`

##### Raison

Utiliser `unique_ptr` de cette manière documente et impose la sémantique de réaffectation de l’appel de fonction.

##### Note

`reseat` signifie « faire référencer à un objet différent un pointeur ou un pointeur intelligent ».

##### Exemple

    void reseat(unique_ptr<widget>&); // « va » ou « pourrait » réassigner le pointeur

##### Enforcement

* (Simple) Avertir si une fonction prend un paramètre `Unique_pointer<T>` par référence lvalue et n’assigne pas à celui‑ci ou n’appelle pas `reset()` au moins sur un chemin de code. Suggérer de prendre un `T*` ou un `T&` à la place.

### <a name="rr-sharedptrparam-owner"></a>R.34 : Prendre un paramètre `shared_ptr<widget>` pour exprimer la propriété partagée

##### Raison

Cela rend explicite le partage de propriété par la fonction.

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

##### Enforcement

* (Simple) Avertir si une fonction prend un paramètre `Shared_pointer<T>` par référence lvalue et n’assigne pas à celui‑ci ou n’appelle pas `reset()` au moins sur un chemin de code. Suggérer de prendre un `T*` ou un `T&` à la place.  
* (Simple) ((Foundation)) Avertir si une fonction prend un `Shared_pointer<T>` par valeur ou par référence à `const` et ne le copie ou ne le déplace pas vers un autre `Shared_pointer` au moins sur un chemin de code. Suggérer de prendre un `T*` ou un `T&` à la place.  
* (Simple) ((Foundation)) Avertir si une fonction prend un `Shared_pointer<T>` par référence rvalue. Suggérer de le prendre par valeur à la place.

### <a name="rr-sharedptrparam"></a>R.35 : Prendre un paramètre `shared_ptr<widget>&` pour indiquer qu’une fonction peut réassigner le pointeur partagé

##### Raison

Cela rend explicite la réaffectation de la fonction.

##### Note

`reseat` signifie « faire référencer à un autre objet une référence ou un pointeur intelligent ».

##### Exemple, bon

    void ChangeWidget(std::shared_ptr<widget>& w)
    {
        // Cela modifiera le widget de l’appelant
        w = std::make_shared<widget>(widget{});
    }

##### Enforcement

* (Simple) Avertir si une fonction prend un paramètre `Shared_pointer<T>` par référence lvalue et n’assigne pas à celui‑ci ou n’appelle pas `reset()` au moins sur un chemin de code. Suggérer de prendre un `T*` ou un `T&` à la place.  
* (Simple) ((Foundation)) Avertir si une fonction prend un `Shared_pointer<T>` par valeur ou par référence à `const` et ne le copie ou ne le déplace pas vers un autre `Shared_pointer` au moins sur un chemin de code. Suggérer de prendre un `T*` ou un `T&` à la place.  
* (Simple) ((Foundation)) Avertir si une fonction prend un `Shared_pointer<T>` par référence rvalue. Suggérer de le prendre par valeur à la place.

### <a name="rr-sharedptrparam-const"></a>R.36 : Prendre un paramètre `const shared_ptr<widget>&` pour indiquer qu’il pourrait retenir un compteur de références sur l’objet ???

##### Raison

Cela rend le ??? de la fonction explicite.

##### Exemple, bon

    void share(shared_ptr<widget>);            // partage — « va » retenir le compteur de références
    void reseat(shared_ptr<widget>&);          // « pourrait » réassigner le pointeur
    void may_share(const shared_ptr<widget>&); // « pourrait » retenir le compteur de références

##### Enforcement

* (Simple) Avertir si une fonction prend un paramètre `Shared_pointer<T>` par référence lvalue et n’assigne pas à celui‑ci ou n’appelle pas `reset()` au moins sur un chemin de code. Suggérer de prendre un `T*` ou un `T&` à la place.  
* (Simple) ((Foundation)) Avertir si une fonction prend un `Shared_pointer<T>` par valeur ou par référence à `const` et ne le copie ou ne le déplace pas vers un autre `Shared_pointer` au moins sur un chemin de code. Suggérer de prendre un `T*` ou un `T&` à la place.  
* (Simple) ((Foundation)) Avertir si une fonction prend un `Shared_pointer<T>` par référence rvalue. Suggérer de le prendre par valeur à la place.

### <a name="rr-smartptrget"></a>R.37 : Ne pas passer un pointeur ou une référence obtenus à partir d’un pointeur intelligent aliassé

##### Raison

Violér cette règle est la principale cause de perte de compteurs de références et de se retrouver avec un pointeur suspendu.  
Les fonctions devraient préférer passer des pointeurs et références nus le long des chaînes d’appels.  
Au sommet de l’arbre d’appels où vous obtenez le pointeur ou la référence brute à partir d’un pointeur intelligent qui maintient l’objet en vie.  
Vous devez vous assurer que le pointeur intelligent ne peut pas être réinitialisé ou réaffecté accidentellement depuis l’arbre d’appels inférieur.

##### Note

Pour ce faire, il faut parfois prendre une copie locale du pointeur intelligent, ce qui maintient fermement l’objet en vie pendant toute la durée de la fonction et de l’arbre d’appels.

##### Exemple

    // global (statique ou sur le tas), ou local aliassé ...
    shared_ptr<widget> g_p = ...;

    void f(widget& w)
    {
        g();
        use(w);  // A
    }

    void g()
    {
        g_p = ...; // oups, si c’était le dernier `shared_ptr` pointant sur ce widget, cela détruit le widget
    }

    void my_code()
    {
        // MAUVAIS : passer un pointeur ou une référence obtenus à partir d’un pointeur intelligent non‑local
        //      qui pourrait être réinitialisé accidentellement quelque part dans `f` ou ses appelés
        f(*g_p);

        // MAUVAIS : même raison, en le passant simplement comme pointeur « this »
        g_p->func();
    }

    void my_code()
    {
        // peu coûteux : 1 incrément couvre toute cette fonction et tous les arbres d’appels en dessous
        auto pin = g_p;

        // BON : passer un pointeur ou une référence obtenus à partir d’un pointeur intelligent local non‑aliassé
        f(*pin);

        // BON : même raison
        pin->func();
    }

##### Enforcement

* (Simple) Avertir si un pointeur ou une référence obtenus à partir d’une variable de pointeur intelligent (`Unique_pointer` ou `Shared_pointer`) qui est non‑locale, ou qui est locale mais potentiellement aliassée, est utilisé dans un appel de fonction. Si le pointeur intelligent est un `Shared_pointer`, suggérer de prendre une copie locale du pointeur intelligent et d’obtenir le pointeur ou la référence à partir de celle‑ci.