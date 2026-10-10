# <a name="s-resource"></a>R: Gestion des ressources

Cette section contient des règles relatives aux ressources.  
Une ressource est tout ce qui doit être acquis et (explicitement ou implicitement) libéré, comme la mémoire, les handles de fichiers, les sockets et les verrous.  
La raison pour laquelle elle doit être libérée est généralement qu'elle peut être limitée en quantité ; une libération retardée peut donc être dommageable.  
L'objectif fondamental est de garantir qu'aucune ressource ne fuit et qu'aucune ressource ne soit conservée plus longtemps que nécessaire.  
Une entité chargée de la libération d'une ressource est appelée **propriétaire**.

Il existe quelques cas où les fuites peuvent être acceptables ou même optimales :  
* Si vous écrivez un programme qui produit simplement une sortie à partir d'une entrée et que la quantité de mémoire nécessaire est proportionnelle à la taille de l'entrée, la stratégie optimale (pour la performance et la simplicité de programmation) est parfois simplement de ne jamais rien supprimer.  
* Si vous avez suffisamment de mémoire pour gérer votre entrée la plus volumineuse, laissez-la fuiter, mais assurez‑vous de fournir un bon message d'erreur si vous vous trompez.  

Ici, nous ignorons ces cas.

* Résumé des règles de gestion des ressources :  
  * [R.1 : Gérer les ressources automatiquement en utilisant des gestionnaires de ressources et l'RAII (Acquisition des Ressources au Moment de l'Initialisation)](#rr-raii)  
  * [R.2 : Dans les interfaces, utilisez des pointeurs bruts pour désigner des objets individuels (uniquement)](#rr-use-ptr)  
  * [R.3 : Un pointeur brut (`T*`) est non possédant](#rr-ptr)  
  * [R.4 : Une référence brut (`T&`) est non possédante](#rr-ref)  
  * [R.5 : Préférez les objets scoped, évitez d'allouer inutilement sur le tas](#rr-scoped)  
  * [R.6 : Évitez les variables globales non `const`](#rr-global)  

* Résumé des règles d'allocation et de désallocation :  
  * [R.10 : Évitez `malloc()` et `free()`](#rr-mallocfree)  
  * [R.11 : Évitez d'appeler explicitement `new` et `delete`](#rr-newdelete)  
  * [R.12 : Affectez immédiatement le résultat d'une allocation explicite de ressource à un objet gestionnaire](#rr-immediate-alloc)  
  * [R.13 : Réalisez au plus une allocation explicite de ressource dans une seule instruction d'expression](#rr-single-alloc)  
  * [R.14 : Évitez les paramètres `[]`, préférez `span`](#rr-ap)  
  * [R.15 : Surchargez toujours les paires d'allocation/désallocation correspondantes](#rr-pair)  

* Résumé des règles relatives aux pointeurs intelligents :  
  * [R.20 : Utilisez `unique_ptr` ou `shared_ptr` pour représenter la possession](#rr-owner)  
  * [R.21 : Privilégiez `unique_ptr` plutôt que `shared_ptr` sauf si vous devez partager la possession](#rr-unique)  
  * [R.22 : Utilisez `make_shared()` pour créer des `shared_ptr`](#rr-make_shared)  
  * [R.23 : Utilisez `make_unique()` pour créer des `unique_ptr`](#rr-make_unique)  
  * [R.24 : Utilisez `std::weak_ptr` pour rompre les cycles de pointeurs partagés](#rr-weak_ptr)  
  * [R.30 : Prenez des pointeurs intelligents comme paramètres uniquement pour exprimer explicitement les paramètres de durée de vie](#rr-smartptrparam)  
  * [R.31 : Si vous avez des pointeurs intelligents non-`std`, suivez le schéma de base fourni par `std`](#rr-smart)  
  * [R.32 : Prenez un paramètre `unique_ptr<widget>` pour exprimer que la fonction assume la possession d'un `widget`](#rr-uniqueptrparam)  
  * [R.33 : Prenez un paramètre `unique_ptr<widget>&` pour exprimer que la fonction réalloue le `widget`](#rr-reseat)  
  * [R.34 : Prenez un paramètre `shared_ptr<widget>` pour exprimer la possession partagée](#rr-sharedptrparam-owner)  
  * [R.35 : Prenez un paramètre `shared_ptr<widget>&` pour exprimer que la fonction peut réallouer le pointeur partagé](#rr-sharedptrparam)  
  * [R.36 : Prenez un paramètre `const shared_ptr<widget>&` pour exprimer qu'il peut retenir un compteur de référence vers l'objet ???](#rr-sharedptrparam-const)  
  * [R.37 : Ne transmettez pas un pointeur ou une référence obtenus d'un pointeur intelligent aliasé](#rr-smartptrget)  

## <a name="rr-raii"></a>R.1 : Gérer les ressources automatiquement en utilisant des gestionnaires de ressources et l'RAII (Acquisition des Ressources au Moment de l'Initialisation)

#### Raison

Pour éviter les fuites et la complexité d'une gestion manuelle des ressources.  
La symétrie des constructeurs/détructeurs imposée par le langage C++ reflète la symétrie inhérente aux paires de fonctions d'acquisition/libération de ressources telles que `fopen`/`fclose`, `lock`/`unlock` et `new`/`delete`.  
Chaque fois que vous traitez une ressource qui nécessite des appels de fonctions d'acquisition/libération « couplés », encapsulez cette ressource dans un objet qui impose cette paire ; acquérez la ressource dans son constructeur et libérez‑la dans son destructeur.

#### Exemple, mauvais

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

Dans ce code, vous devez vous rappeler de `unlock`, `close_port` et `delete` sur tous les chemins, et de les exécuter exactement une fois. En outre, si l'un des fragments de code marqués `...` déclenche une exception, `x` fuit et `my_mutex` reste verrouillé.

#### Exemple

Considérez :

    void send(unique_ptr<X> x, string_view destination)  // x possédant X
    {
        Port port{destination};            // port possédant PortHandle
        lock_guard<mutex> guard{my_mutex}; // guard possédant le verrou
        // ...
        send(port, x);
        // ...
    } // libère automatiquement my_mutex et supprime le pointeur dans x

Maintenant tout le nettoyage de ressource est automatique, effectué une fois sur tous les chemins, qu'il y ait ou non une exception. En bonus, la fonction indique maintenant qu'elle prend possession du pointeur.

Qu'est‑ce que `Port` ? Un wrapper pratique qui encapsule la ressource :

    class Port {
        PortHandle port;
    public:
        Port(string_view destination) : port{open_port(destination)} { }
        ~Port() { close_port(port); }
        operator PortHandle() { return port; }

        // les handles de port ne se clonent généralement pas, désactiver la copie et l'assignation si nécessaire
        Port(const Port&) = delete;
        Port& operator=(const Port&) = delete;
    };

#### Remarque

Où une ressource se comporte mal alors qu'elle n'est pas représentée comme une classe disposant d'un destructeur, enveloppez‑la dans une classe ou utilisez [finally](#re-finally) @TODO-LINK

**Voir également** : [RAII](#re-raii) @TODO-LINK

## <a name="rr-use-ptr"></a>R.2 : Dans les interfaces, utilisez des pointeurs bruts pour désigner des objets individuels (uniquement)

#### Raison

Les tableaux sont mieux représentés par un type de conteneur (ex. `vector` (propriétaire)) ou un `span` (non propriétaire). Ces conteneurs et vues contiennent suffisamment d'informations pour effectuer une vérification d'intervalle.

#### Exemple, mauvais

    void f(int* p, int n)   // n est le nombre d'éléments dans p[]
    {
        // ...
        p[2] = 7;   // mauvais : sous‑script d'un pointeur brut
        // ...
    }

Le compilateur ne lit pas les commentaires, et sans examiner le reste du code, vous ne savez pas si `p` pointe réellement vers `n` éléments. Utilisez plutôt un `span`.

#### Exemple

    void g(int* p, int fmt)   // afficher *p en utilisant le format #fmt
    {
        // ... uses *p and p[0] only ...
    }

#### Exception

Les chaînes de caractères au style C sont transmises sous forme de pointeur unique vers une séquence terminée par un zéro de caractères. Utilisez `zstring` plutôt que `char*` pour indiquer que vous faites confiance à cette convention.

#### Remarque

Nombreuses utilisations actuelles de pointeurs vers un seul élément pourraient être des références. Toutefois, lorsqu'une valeur `nullptr` est possible, une référence peut ne pas être une alternative raisonnable.

#### Application

* Détecter l'arithmétique de pointeurs (y compris `++`) sur un pointeur qui ne fait pas partie d'un conteneur, d'une vue ou d'un itérateur. Cette règle entraînerait un grand nombre de faux positifs si elle était appliquée à une base de code plus ancienne.  
* Signaler les noms de tableaux transmis comme de simples pointeurs.

## <a name="rr-ptr"></a>R.3 : Un pointeur brut (`T*`) est non possédant

#### Raison

Il n'y a rien (dans le standard C++ ou dans la plupart des codes) qui indique le contraire et la plupart des pointeurs bruts sont non possédants. Nous voulons identifier les pointeurs propriétaires afin de pouvoir supprimer fiable et efficacement les objets pointés par les pointeurs propriétaires.

#### Exemple

    void f()
    {
        int* p1 = new int{7};           // mauvais : pointeur brut propriétaire
        auto p2 = make_unique<int>(7);  // OK : l'entier est possédé par un unique_ptr
        // ...
    }

Le `unique_ptr` protège contre les fuites en garantissant la suppression de son objet (même en présence d'exceptions). Le `T*` ne le fait pas.

#### Exemple

    template<typename T>
    class X {
    public:
        T* p;   // mauvaise : il est incertain que p soit propriétaire ou non
        T* q;   // mauvaise : il est incertain que q soit propriétaire ou non
        // ...
    };

Nous pouvons corriger ce problème en rendant la propriété explicite :

    template<typename T>
    class X2 {
    public:
        owner<T*> p;  // OK : p est propriétaire
        T* q;         // OK : q n'est pas propriétaire
        // ...
    };

#### Exception

Une grande classe d'exceptions est le code hérité, surtout le code qui doit rester compatible C ou interagir avec le C et le C++ de style C via les ABI. Le fait qu'il existe des milliards de lignes de code qui violent cette règle contre les pointeurs bruts propriétaires ne peut être ignoré. Nous aimerions voir des outils de transformation de programmes convertir le code « hérité » de 20 ans en code moderne. Nous encourageons le développement, le déploiement et l'utilisation de tels outils. Nous espérons que les directives aideront à développer de tels outils, et nous avons même contribué (et contribuons) à la recherche et au développement dans ce domaine. Cependant, il faudra du temps : le code hérité est généré plus rapidement que nous pouvons rénover l'ancien code, et donc cela restera le cas pendant quelques années.

Tout ce code ne peut pas être réécrit (même si le logiciel de transformation était bon) surtout pas tout de suite. Ce problème ne peut pas être résolu (à grande échelle) en transformant tous les pointeurs propriétaires en `unique_ptr` et `shared_ptr`, en partie parce que nous utilisons/avons des pointeurs bruts propriétaires ainsi que des pointeurs simples dans l'implémentation de nos gestionnaires de ressources fondamentaux. Par exemple, les implémentations communes de `vector` comportent un pointeur propriétaire et deux pointeurs non‑propriétaires. De nombreux ABI (et essentiellement toutes les interfaces vers du code C) utilisent des `T*`, certains d'entre eux sont propriétaires. Certaines interfaces ne peuvent pas être simplement annotées avec `owner` parce qu'elles doivent rester compilables en C (même si cela serait une rare bonne utilisation d'un macro qui s'étendait uniquement à `owner` en mode C++).

#### Remarque

`owner<T*>` n'a pas de sémantique par défaut autre que `T*`. Il peut être utilisé sans changer le code le utilisant et sans affecter les ABI. C'est simplement un indicateur pour les programmeurs et les outils d'analyse. Par exemple, si un `owner<T*>` est membre d'une classe, il est recommandé que cette classe ait un destructeur qui le supprime.

#### Exemple, mauvais

Les fonctions qui retournent un pointeur brut imposent une incertitude de gestion de la durée de vie sur l'appelant ; qui supprime l'objet pointé ?

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

En plus de souffrir du problème de la [fuite] (#rp-leak) @TODO-LINK, cela ajoute une allocation et désallocation, et est inutilement verbeux. Si Gadget est bon à déplacer hors d'une fonction (c’est‑à‑dire est petit ou possède une opération de déplacement efficiente), il suffit de le renvoyer « par valeur » (voir les valeurs de retour “out” (#rf-out) @TODO-LINK) :

    Gadget make_gadget(int n)
    {
        Gadget g{n};
        // ...
        return g;
    }

#### Remarque

Cette règle s'applique aux fonctions de fabrication (« factory »).

#### Remarque

Si la sémantique de pointeur est requise (par ex. parce que le type de retour doit référencer une classe de base d'une hiérarchie (une interface)), renvoyez un « pointeur intelligent ».

#### Application

* (Simple) Avertir lorsqu'un `delete` d'un pointeur brut qui n'est pas un `owner<T>` est effectué.  
* (Modéré) Avertir lorsqu'un `owner<T>` n'est pas `reset` ou explicitement `delete` sur chaque chemin de code.  
* (Simple) Avertir lorsqu'une valeur de `new` est assignée à un pointeur brut.  
* (Simple) Avertir lorsqu'une fonction retourne un objet alloué dans la fonction mais possède un constructeur de déplacement. Suggérer de le renvoyer par valeur à la place.

## <a name="rr-ref"></a>R.4 : Une référence brut (`T&`) est non possédante

#### Raison

Il n'y a rien (dans le standard C++ ou dans la plupart des codes) qui indique le contraire et la plupart des références brutes sont non possédantes. Nous voulons identifier les propriétaires afin de pouvoir supprimer fiable et efficacement les objets pointés par les pointeurs propriétaires.

#### Exemple

    void f()
    {
        int& r = *new int{7};  // mauvais : référence brute propriétaire
        // ...
        delete &r;             // mauvais : violation de la règle contre `delete` de pointeur brut
    }

**Voir également** : [La règle du pointeur brut](#rr-ptr)

#### Application

Voir la règle du pointeur brutal (#rr-ptr)

## <a name="rr-scoped"></a>R.5 : Préférez les objets scoped, évitez d'allouer inutilement sur le tas

#### Raison

Un objet scoped est un objet local, un objet global ou un membre. Cela implique qu'il n'y a pas de coût d'allocation/désallocation séparé au-delà de ce qui est déjà utilisé pour le scope ou l'objet contenant. Les membres d un objet scoped sont eux‑mêmes scoped et les constructeurs et destructeurs de l'objet scoped gèrent les durées de vie de ces membres.

#### Exemple

L'exemple suivant est inefficace (car il implique une allocation et désallocation inutiles), vulnérable aux exceptions et aux retours dans la partie `...` (conduisant à des fuites), et verbeux :

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

#### Application

* (Modéré) Avertir si un objet est alloué puis désalloué sur tous les chemins d'une fonction. Suggérer qu'il soit un objet local de pile à la place.  
* (Simple) Avertir si un `Unique_pointer` ou `Shared_pointer` local qui n'est pas déplacé, copié, réaffecté ou `reset` avant la fin de son cycle de vie n'est pas déclaré `const`. Exception : ne pas produire ce type d'avertissement sur un `Unique_pointer` local d'un tableau non délimité. (Voir ci‑dessous.)

#### Exception

Si votre espace pile est limité, il est acceptable de créer un `const unique_ptr<BigObject>` local pour stocker l'objet sur le tas au lieu de la pile.

## <a name="rr-global"></a>R.6 : Évitez les variables globales non `const`

Voir [I.2](#ri-global) @TODO-LINK

## <a name="ss-alloc"></a>R.alloc : Allocation et désallocation

## <a name="rr-mallocfree"></a>R.10 : Évitez `malloc()` et `free()`

#### Raison

`malloc()` et `free()` ne prennent pas en charge la construction et la destruction, et ne s'entremêlent pas bien avec `new` et `delete`.

#### Exemple

    class Record {
        int id;
        string name;
        // ...
    };

    void use()
    {
        // p1 pourrait être nullptr
        // *p1 n'est pas initialisé ; en particulier,
        // cette instance de string n'est pas une string, mais une boîte de bits de taille string
        Record* p1 = static_cast<Record*>(malloc(sizeof(Record)));

        auto p2 = new Record;

        // sauf si une exception est lancée, *p2 est initialisé par défaut
        auto p3 = new(nothrow) Record;
        // p3 pourrait être nullptr ; sinon, *p3 est initialisé par défaut

        // ...

        delete p1;    // erreur : ne peut pas delete un objet alloué par malloc()
        free(p2);    // erreur : ne peut pas free() un objet alloué par new
    }

Dans certaines implémentations, `delete` et `free()` pourraient fonctionner, ou pourraient causer des erreurs à l'exécution.

#### Exception

Il existe des applications et des sections de code où les exceptions ne sont pas acceptables. Certains des meilleurs exemples se trouvent dans le code critique en temps réel. Méfiez‑vous du fait que de nombreux interdits d'utilisation d'exceptions sont basés sur de la superstition (mauvais) ou par souci d'un ancien code source sans gestion systématique des ressources (infortunément, mais parfois nécessaire). Dans de tels cas, envisagez les variantes `nothrow` de `new`.

#### Application

Flag explicit use of `malloc` and `free`.

## <a name="rr-newdelete"></a>R.11 : Évitez d'appeler explicitement `new` et `delete`

#### Raison

Le pointeur retourné par `new` devrait appartenir à un gestionnaire de ressource (qui peut appeler `delete`). Si le pointeur retourné par `new` est assigné à un pointeur simple, l'objet peut fuser.

#### Remarque

Dans un gros programme, un `delete` simple (c‑à‑d‑ex. un `delete` situé dans le code d'application, plutôt qu'une partie consacrée à la gestion des ressources) est probablement un bug. Si vous avez N `delete`, comment êtes‑vous certain de ne pas en avoir besoin `N+1` ou `N-1` ? Le bug peut être latent : il n'apparaît que pendant la maintenance. Si vous avez un `new` simple, vous avez probablement besoin d'un `delete` somewhere, so you probably have a bug.

#### Application

(Si) Warn on any explicit use of `new` and `delete`. Suggest using `make_unique` instead.

## <a name="rr-immediate-alloc"></a>R.12 : Affectez immédiatement le résultat d'une allocation explicite de ressource à un objet gestionnaire

#### Raison

S'il ne l'est pas, une exception ou un retour peut entraîner une fuite.

#### Exemple, mauvais

    void func(const string& name)
    {
        FILE* f = fopen(name, "r");            // ouvrir le fichier
        vector<char> buf(1024);
        auto _ = finally([f] { fclose(f); });  // se souvenir de fermer le fichier
        // ...
    }

L'allocation de `buf` peut échouer et fuser le handle de fichier.

#### Exemple

    void func(const string& name)
    {
        ifstream f{name};   // ouvrir le fichier
        vector<char> buf(1024);
        // ...
    }

L'utilisation du handle de fichier (dans `ifstream`) est simple, efficace et sûre.

#### Application

* Flag explicit allocations used to initialize pointers (problem: how many direct resource allocations can we recognize?)

## <a name="rr-single-alloc"></a>R.13 : Réalisez au plus une allocation explicite de ressource dans une seule instruction d'expression

#### Raison

Si vous réalisez deux allocations explicites de ressource dans un seul statement, vous pourriez fuser des ressources parce que l'ordre d'évaluation de nombreuses sous‑expressions, y compris les arguments de fonction, est non spécifié.

#### Exemple

    void fun(shared_ptr<Widget> sp1, shared_ptr<Widget> sp2);

Cette fonction peut être appelée comme suit :

    // MAUVAIS : fuite potentielle
    fun(shared_ptr<Widget>(new Widget(a, b)), shared_ptr<Widget>(new Widget(c, d)));

Cette attaque tant qu'exception‑sûre parce que le compilateur peut réordonner les deux expressions créant les deux arguments. En particulier, le compilateur peut intercaler l'exécution des deux expressions : l'allocation mémoire (en appelant `operator new`) pourrait être faite d'abord pour les deux objets, suivie des appels aux deux constructeurs `Widget`. Si l'un des appels de constructeur lève une exception, la mémoire de l'autre objet ne sera jamais libérée !

Ce problème subtil a une solution simple : ne réalisez jamais plus d'une allocation explicite de ressource dans une seule instruction d'expression. Par exemple :

    shared_ptr<Widget> sp1(new Widget(a, b)); // préférable mais ennuyeux
    fun(sp1, new Widget(c, d));

La meilleure solution est d'éviter l'allocation explicite tout à fait, d'utiliser des fonctions de fabrication qui retournent des objets propriétaires :

    fun(make_shared<Widget>(a, b), make_shared<Widget>(c, d)); // meilleur

Écrivez votre propre wrapper de fabrication s'il n'en existe pas déjà un.

#### Application

* Flag expressions with multiple explicit resource allocations (problem: how many direct resource allocations can we recognize?)

## <a name="rr-ap"></a>R.14 : Évitez les paramètres `[]`, préférez `span`

#### Raison

Un tableau se décale en pointeur, perdant ainsi sa taille, ouvrant l'opportunité d'erreurs d'intervalle. Utilisez `span` pour préserver les informations de taille.

#### Exemple

    void f(int[]);          // non recommandé

    void f(int*);           // non recommandé pour plusieurs objets
                            // (un pointeur doit pointer vers un seul objet, ne souzérolez pas)

    void f(gsl::span<int>); // bon, recommandé

#### Application

Flag `[]` parameters. Use `span` instead.

## <a name="rr-pair"></a>R.15 : Surchargez toujours les paires d'allocation/désallocation correspondantes

#### Raison

Sinon vous obtiendrez des opérations d'allocation et de désallocation déséquilibrées et du chaos.

#### Exemple

    class X {
        // ...
        void* operator new(size_t s);
        void operator delete(void*);
        // ...
    };

#### Remarque

Si vous voulez de la mémoire qui ne peut pas être désallouée, `=delete` le op. de désallocation. N'y laissez pas non déclarée.

#### Application

Flag incomplete pairs.

## <a name="ss-smart"></a>R.smart : Pointeurs intelligents

## <a name="rr-owner"></a>R.20 : Utilisez `unique_ptr` ou `shared_ptr` pour représenter la possession

#### Raison

Ils peuvent prévenir les fuites de ressources.

#### Exemple

Considérez :

    void f()
    {
        X* p1 { new X };              // mauvais, p1 fuit
        auto p2 = make_unique<X>();   // bon, possession unique
        auto p3 = make_shared<X>();   // bon, possession partagée
    }

Ce code fuit l'objet utilisé pour initialiser `p1` (seul).

#### Application

* (Simple) Warn if the return value of `new` is assigned to a raw pointer.  
* (Simple) Warn if the result of a function returning a raw owning pointer is assigned to a raw pointer.

## <a name="rr-unique"></a>R.21 : Privilégiez `unique_ptr` plutôt que `shared_ptr` sauf si vous devez partager la possession

#### Raison

Un `unique_ptr` est conceptuellement plus simple et plus prévisible (vous savez quand la destruction se produit) et plus rapide (vous ne maintenez pas implicitement un compte d'utilisation).

#### Exemple, mauvais

Cette surcharge inutile d'un compte d'utilisation.

    void f()
    {
        shared_ptr<Base> base = make_shared<Derived>();
        // utilisez base localement, sans le copier – le compte d'utilisation ne dépasse jamais 1
    } // détruit base

#### Exemple

Ceci est plus efficace :

    void f()
    {
        unique_ptr<Base> base = make_unique<Derived>();
        // utilisez base localement
    } // détruit base

#### Application

(Si) Warn if a function uses a Shared_pointer with an object allocated within the function, but never returns the Shared_pointer or passes it to a function requiring a Shared_pointer. Suggest using unique_ptr instead.

## <a name="rr-make_shared"></a>R.22 : Utilisez `make_shared()` pour créer des `shared_ptr`

#### Raison

`make_shared` fournit une déclaration plus concise de la construction.  
Il fournit aussi l'occasion d'éliminer une allocation séparée pour les compteurs d'utilisation, en plaçant le compte des uses du `shared_ptr` à côté de son objet.  
Il garantit également la sécurité d'exception dans les expressions complexes (dans le code pré‑C++17).

#### Exemple

Considérez :

    shared_ptr<X> p1 { new X{2} }; // mauvais  
    auto p = make_shared<X>(2);    // bon

La version `make_shared()` ne mentionne `X` qu'une seule fois, elle est donc généralement plus courte (et plus rapide) que la version avec `new` explicite.

#### Application

(Si) Warn if a `shared_ptr` is constructed from the result of `new` rather than `make_shared`.

## <a name="rr-make_unique"></a>R.23 : Utilisez `make_unique()` pour créer des `unique_ptr`

#### Raison

`make_unique` fournit une déclaration plus concise de la construction.  
Il garantit également la sécurité d'exception dans les expressions complexes (dans le code pré‑C++17).

#### Exemple

    unique_ptr<Foo> p {new Foo{7}};    // OK : mais répétitif

    auto q = make_unique<Foo>(7);      // meilleur : pas de répétition de Foo

#### Application

(Si) Warn if a `unique_ptr` is constructed from the result of `new` rather than `make_unique`.

## <a name="rr-weak_ptr"></a>R.24 : Utilisez `std::weak_ptr` pour rompre les cycles de pointeurs partagés

#### Raison

`shared_ptr` s'appuie sur le compteur d'utilisation et le compteur d'utilisation pour une structure cyclique ne se termine jamais, nous avons besoin d'un mécanisme pour pouvoir détruire la structure cyclique.

#### Exemple

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
          // utiliser *shared_back_reference
        }
      }
    private:
      std::weak_ptr<foo> back_reference_;
    };

#### Remarque

?? (HS : Beaucoup de gens disent « pour rompre les cycles », alors que je pense que « propriété partagée temporaire » est plus pertinent.)  
?? (BS : rompre les cycles est ce que vous devez faire ; partager temporairement la propriété est comment vous le faites.  
Vous pourriez « partager temporairement la propriété » simplement en utilisant un autre `shared_ptr`.)

#### Application

?? probablement impossible. Si nous pouvions détecter statiquement les cycles, nous n'aurions pas besoin de `weak_ptr`.

## <a name="rr-smartptrparam"></a>R.30 : Prenez des pointeurs intelligents comme paramètres uniquement pour exprimer explicitement les paramètres de durée de vie

Voir [F.7](#rf-smart) @TODO-LINK

## <a name="rr-smart"></a>R.31 : Si vous avez des pointeurs intelligents non‑`std`, suivez le schéma de base fourni par `std`

#### Raison

Les règles de la section suivante fonctionnent également pour d’autres types de pointeurs intelligents tiers et sont très utiles pour diagnostiquer les erreurs de pointeur intelligent courantes qui causent des problèmes de performances et de correctness. Vous voulez que ces règles fonctionnent pour tous les pointeurs intelligents que vous utilisez.

Tout type (y compris le modèle primaire ou une spécialisation) qui surcharge `*` et `->` est considéré comme un pointeur intelligent :

* Si c’est copiable, il est reconu comme un `shared_ptr` référencé.  
* Si ce n’est pas copiable, il est reconnu comme un `unique_ptr`.

#### Exemple, mauvais

    // utilisez `intrusive_ptr` de Boost
    #include <boost/intrusive_ptr.hpp>
    void f(boost::intrusive_ptr<widget> p)  // erreur selon la règle `sharedptrparam`
    {
        p->foo();
    }

    // utilisez `CComPtr` de Microsoft
    #include <atlbase.h>
    void f(CComPtr<widget> p)               // erreur selon la règle `sharedptrparam`
    {
        p->foo();
    }

Dans les deux cas, c’est une erreur selon la [règle](#rr-smartptrparam) « smartptrparam » : `p` est un `Shared_pointer`, mais il n'y a rien qui l'emploie, et le transmettre par valeur est une pessimisation silencieuse ; ces fonctions devraient accepter un pointeur intelligent seulement si elles doivent intervenir dans la gestion de la durée de vie du widget. Sinon, elles devraient accepter un `widget*`, si celui‑ci peut être `nullptr`. Idéalement, la fonction devrait accepter un `widget&`.

Ces pointeurs intelligents correspondent au concept `Shared_pointer`, donc ces règles d'application fonctionnent directement sur eux et exposent cette pessimisation courante.

## <a name="rr-uniqueptrparam"></a>R.32 : Prenez un paramètre `unique_ptr<widget>` pour exprimer que la fonction assume la possession d'un `widget`

#### Exemple

    void sink(unique_ptr<widget>); // prend possession du widget

    void uses(widget*);            // utilise simplement le widget

#### Application

* (Simple) Warn if a function takes a `Unique_pointer<T>` parameter by lvalue reference and does not either assign to it or call `reset()` on it on at least one code path. Suggest taking a `T*` or `T&` instead.

## <a name="rr-reseat"></a>R.33 : Prenez un paramètre `unique_ptr<widget>&` pour exprimer que la fonction réalloue le widget

#### Exemple

    void reseat(unique_ptr<widget>&); // « va » ou « peut » réallouer le pointeur

#### Application

* (Simple) Warn if a function takes a `Unique_pointer<T>` parameter by lvalue reference and does not either assign to it or call `reset()` on it on at least one code path. Suggest taking a `T*` or `T&` instead.

## <a name="rr-sharedptrparam-owner"></a>R.34 : Prenez un paramètre `shared_ptr<widget>` pour exprimer la possession partagée

#### Exemple, bon

    class WidgetUser
    {
    public:
        // WidgetUser partagera la possession du widget
        explicit WidgetUser(std::shared_ptr<widget> w) noexcept:
            m_widget{std::move(w)} {}
        // ...
    private:
        std::shared_ptr<widget> m_widget;
    };

#### Application

* (Simple) Warn if a function takes a `Shared_pointer<T>` parameter by lvalue reference and does not either assign to it or call `reset()` on it on at least one code path. Suggest taking a `T*` or `T&` instead.  
* (Simple) ((Foundation)) Warn if a function takes a `Shared_pointer<T>` by value or by reference to `const` and does not copy or move it to another `Shared_pointer` on at least one code path. Suggest taking a `T*` or `T&` instead.  
* (Simple) ((Foundation)) Warn if a function takes a `Shared_pointer<T>` by rvalue reference. Suggest taking it by value instead.

## <a name="rr-sharedptrparam"></a>R.35 : Prenez un paramètre `shared_ptr<widget>&` pour exprimer que la fonction peut réallouer le pointeur partagé

#### Exemple, bon

    void ChangeWidget(std::shared_ptr<widget>& w)
    {
        // Cela changera l'objet widget du caller
        w = std::make_shared<widget>(widget{});
    }

#### Application

* (Simple) Warn if a function takes a `Shared_pointer<T>` parameter by lvalue reference and does not either assign to it or call `reset()` on it on at least one code path. Suggest taking a `T*` or `T&` instead.  
* (Simple) ((Foundation)) Warn if a function takes a `Shared_pointer<T>` by value or by reference to `const` and does not copy or move it to another `Shared_pointer` on at least one code path. Suggest taking a `T*` or `T&` instead.  
* (Simple) ((Foundation)) Warn if a function takes a `Shared_pointer<T>` by rvalue reference. Suggest taking it by value instead.

## <a name="rr-sharedptrparam-const"></a>R.36 : Prenez un paramètre `const shared_ptr<widget>&` pour exprimer qu'il peut retenir un compteur de référence vers l'objet ???

#### Exemple, bon

    void share(shared_ptr<widget>);            // compartlement – « retient refcount »  
    void reseat(shared_ptr<widget>&);          // « peut » réallouer le pointeur  
    void may_share(const shared_ptr<widget>&); // « peut » retenir le compteur de référence

#### Application

* (Simple) Warn if a function takes a `Shared_pointer<T>` parameter by lvalue reference and does not either assign to it or call `reset()` on it on at least one code path. Suggest taking a `T*` or `T&` instead.  
* (Simple) ((Foundation)) Warn if a function takes a `Shared_pointer<T>` by value or by reference to `const` and does not copy or move it to another `Shared_pointer` on at least one code path. Suggest taking a `T*` or `T&` instead.  
* (Simple) ((Foundation)) Warn if a function takes a `Shared_pointer<T>` by rvalue reference. Suggest taking it by value instead.

## <a name="rr-smartptrget"></a>R.37 : Ne transmettez pas un pointeur ou une référence obtenus d'un pointeur intelligent aliasé

#### Raison

Violating this rule is the number one cause of losing reference counts and finding yourself with a dangling pointer. Functions should prefer to pass raw pointers and references down call chains. At the top of the call tree where you obtain the raw pointer or reference from a smart pointer that keeps the object alive. You need to be sure that the smart pointer cannot inadvertently be reset or reassigned from within the call tree below.

#### Remarque

Pour faire cela, parfois vous devez prendre une copie locale d'un pointeur intelligent, ce qui maintient fermement l'objet vivant pendant toute la fonction et l'arbre d'appels.

#### Exemple

Considérez ce code :

    // global (static or heap), or aliased local ...
    shared_ptr<widget> g_p = ...;

    void f(widget& w)
    {
        g();
        use(w);  // A
    }

    void g()
    {
        g_p = ...; // oops, if this was the last shared_ptr to that widget, it destroys the widget
    }

Le suivant ne doit pas passer la revue de code :

    void my_code()
    {
        // MAUVAIS : passage d'un pointeur ou d'une référence obtenue d'un smart pointer non local
        // qui pourrait être inadvertamment réinitialisé quelque part dans f ou ses appels
        f(*g_p);

        // MAUVAIS : raison la même, en le passant comme pointeur `this`
        g_p->func();
    }

La solution est simple -- prendre une copie locale du pointeur pour « garder un compte de référence » pour toute votre fonction et l'arbre d'appels :

    void my_code()
    {
        // bon : 1 incrément couvre cette fonction entière et tous les arbres d'appels en dessous
        auto pin = g_p;

        // BON : passer un pointeur ou une référence obtenue d'un pointeur non aliasé local
        f(*pin);

        // BON : même raison
        pin->func();
    }

#### Application

* (Simple) Warn if a pointer or reference obtained from a smart pointer variable (`Unique_pointer` or `Shared_pointer`) that is non-local, or that is local but potentially aliased, is used in a function call. If the smart pointer is a `Shared_pointer` then suggest taking a local copy of the smart pointer and obtain a pointer or reference from that instead.