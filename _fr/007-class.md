---
title: Classes et hiérarchies de classes
---

# <a name="s-class"></a>C : Classes et hiérarchies de classes

Une classe est un type défini par l'utilisateur, pour lequel un programmeur peut définir la représentation, les opérations et les interfaces.  
Les hiérarchies de classes sont utilisées pour organiser des classes liées dans des structures hiérarchiques.

Résumé des règles de classe :

* [C.1 : Organiser les données liées dans des structures (`struct`s ou `class`es)](#rc-org)
* [C.2 : Utiliser `class` si la classe possède une invariante ; utiliser `struct` si les membres de données peuvent varier indépendamment](#rc-struct)
* [C.3 : Représenter la distinction entre une interface et une implémentation à l’aide d’une classe](#rc-interface)
* [C.4 : Faire d’une fonction un membre uniquement si elle a besoin d’un accès direct à la représentation d’une classe](#rc-member)
* [C.5 : Placer les fonctions d’assistance dans le même espace de noms que la classe qu’elles supportent](#rc-helper)
* [C.7 : Ne pas définir une classe ou un enum et déclarer une variable de son type dans la même instruction](#rc-standalone)
* [C.8 : Utiliser `class` plutôt que `struct` si un membre est non‑public](#rc-class)
* [C.9 : Minimiser l’exposition des membres](#rc-private)

Sous‑sections :

* [C.concrete : Types concrets](#ss-concrete)
* [C.ctor : Constructeurs, assignations et destructeurs](#s-ctor)
* [C.con : Conteneurs et autres gestionnaires de ressources](#ss-containers)
* [C.lambdas : Objets fonctionnels et lambdas](#ss-lambdas)
* [C.hier : Hiérarchies de classes (POO)](#ss-hier)
* [C.over : Surcharge et opérateurs surchargés](#ss-overload)
* [C.union : Unions](#ss-union)

### <a name="rc-org"></a>C.1 : Organiser les données liées dans des structures (`struct`s ou `class`es)

##### Raison

Facilité de compréhension.  
Si les données sont liées (pour des raisons fondamentales), cela doit se refléter dans le code.

##### Exemple

    void draw(int x, int y, int x2, int y2);  // MAUVAIS : relations implicites inutiles    
    void draw(Point from, Point to);          // meilleur

##### Remarque

Une classe simple sans fonctions virtuelles n’implique aucun surcoût en espace ou en temps.

##### Remarque

Du point de vue du langage, `class` et `struct` ne diffèrent que par la visibilité par défaut de leurs membres.

##### Application

Probablement impossible. Un heuristique cherchant des éléments de données utilisés ensemble pourrait être envisageable.

### <a name="rc-struct"></a>C.2 : Utiliser `class` si la classe possède une invariante ; utiliser `struct` si les membres de données peuvent varier indépendamment

##### Raison

Lisibilité.  
Facilité de compréhension.  
L’usage de `class` alerte le programmeur sur la nécessité d’une invariante.  
C’est une convention utile.

##### Remarque

Une invariante est une condition logique sur les membres d’un objet qu’un constructeur doit établir afin que les fonctions membres publiques puissent s’y fier.  
Une fois l’invariante établie (généralement par le constructeur), chaque fonction membre peut être appelée sur l’objet.  
Une invariante peut être indiquée de façon informelle (par ex. dans un commentaire) ou plus formellement à l’aide de `Expects`.

Si tous les membres de données peuvent varier indépendamment les uns des autres, aucune invariante n’est possible.

##### Exemple

    struct Pair {  // les membres peuvent varier indépendamment
        string name;
        int    volume;
    };

mais :

    class Date {
    public:
        // valider que {yy, mm, dd} forme une date valide et initialiser
        Date(int yy, Month mm, char dd);
        // …
    private:
        int   y;
        Month m;
        char  d;    // jour
    };

##### Remarque

Si une classe possède des données `private`, un utilisateur ne peut pas entièrement initialiser un objet sans faire appel à un constructeur. Par conséquent, le concepteur de classe proposera un constructeur et devra en préciser le sens. Cela implique effectivement que le concepteur doit définir une invariante.

**Voir aussi** :

* [définir une classe avec des données privées en tant que `class`](#rc-class)
* [Préférer placer l’interface avant le reste dans une classe](#rl-order)
* [minimiser l’exposition des membres](#rc-private)
* [Éviter les données `protected`](#rh-protected)

##### Application

Chercher les `struct`s dont tous les membres sont privés et les `class`es contenant des membres publics.

### <a name="rc-interface"></a>C.3 : Représenter la distinction entre une interface et une implémentation à l’aide d’une classe

##### Raison

Une distinction explicite entre interface et implémentation améliore la lisibilité et simplifie la maintenance.

##### Exemple

    class Date {
    public:
        Date();
        // valider que {yy, mm, dd} forme une date valide et initialiser
        Date(int yy, Month mm, char dd);

        int    day()   const;
        Month  month() const;
        // …
    private:
        // … représentation interne …
    };

Par exemple, nous pouvons maintenant changer la représentation d’un `Date` sans impacter ses utilisateurs (une recompilation est toutefois probable).

##### Remarque

Utiliser une classe de cette façon pour représenter la distinction entre interface et implémentation n’est bien sûr pas la seule manière. Par exemple, on peut se servir d’un ensemble de déclarations de fonctions libres dans un espace de noms, d’une classe abstraite de base ou d’un modèle de fonction avec concepts pour représenter une interface. L’important est de distinguer explicitement une interface de ses « détails » d’implémentation. Idéalement, et généralement, une interface est bien plus stable que ses implémentations.

##### Application

???

### <a name="rc-member"></a>C.4 : Faire d’une fonction un membre uniquement si elle a besoin d’un accès direct à la représentation d’une classe

##### Raison

Moins d’accouplement que les fonctions membres, moins de fonctions pouvant causer des problèmes en modifiant l’état d’un objet, réduit le nombre de fonctions à modifier après un changement de représentation.

##### Exemple

    class Date {
        // … interface relativement petite …
    };

    // fonctions d’assistance :
    Date next_weekday(Date);
    bool operator==(Date, Date);

Les « fonctions d’assistance » n’ont aucun besoin d’accès direct à la représentation d’un `Date`.

##### Remarque

Cette règle devient encore plus avantageuse si C++ obtient le « appel de fonction uniforme » (https://www.open-std.org/jtc1/sc22/wg21/docs/papers/2016/p0251r0.pdf).

##### Exception

Le langage impose que les fonctions `virtual` soient des membres, et toutes les fonctions `virtual` n’accèdent pas directement aux données. En particulier, les membres d’une classe abstraite le font rarement.

Voir [multi‑méthodes](https://web.archive.org/web/20200605021759/https://parasol.tamu.edu/~yuriys/papers/OMM10.pdf).

##### Exception

Le langage oblige les opérateurs `=`, `()`, `[]` et `->` à être des membres.

##### Exception

Un ensemble de surcharges peut contenir des membres qui n’accèdent pas directement aux données `private` :

    class Foobar {
    public:
        void foo(long x) { /* manipuler les données privées */ }
        void foo(double x) { foo(std::lround(x)); }
        // …
    private:
        // …
    };

##### Exception

De même, un ensemble de fonctions peut être conçu pour être utilisé en chaîne :

    x.scale(0.5).rotate(45).set_color(Color::red);

Typiquement, certaines, mais pas toutes, de ces fonctions accèdent directement aux données `private`.

##### Application

* Rechercher les fonctions membres non‑`virtual` qui ne touchent pas directement les membres de données. Le problème est que de nombreuses fonctions membres qui n’ont pas besoin d’accéder aux données le font tout de même.
* Ignorer les fonctions `virtual`.
* Ignorer les fonctions qui font partie d’un ensemble de surcharges dont au moins une fonction accède aux membres `private`.
* Ignorer les fonctions renvoyant `this`.

### <a name="rc-helper"></a>C.5 : Placer les fonctions d’assistance dans le même espace de noms que la classe qu’elles supportent

##### Raison

Une fonction d’assistance est une fonction (généralement fournie par l’auteur d’une classe) qui n’a pas besoin d’un accès direct à la représentation de la classe, mais qui est considérée comme faisant partie de l’interface utile de la classe. La placer dans le même espace de noms que la classe rend sa relation avec la classe évidente et permet de la trouver via la recherche dépendante d’argument (ADL).

##### Exemple

    namespace Chrono { // ici nous conservons les services liés au temps

        class Time { /* … */ };
        class Date { /* … */ };

        // fonctions d’assistance :
        bool operator==(Date, Date);
        Date next_weekday(Date);
        // …
    }

##### Remarque

C’est particulièrement important pour les [opérateurs surchargés](#ro-namespace).

##### Application

* Signaler les fonctions globales qui prennent des arguments provenant d’un même espace de noms.

### <a name="rc-standalone"></a>C.7 : Ne pas définir une classe ou un enum et déclarer une variable de son type dans la même instruction

##### Raison

Mélanger une définition de type et la définition d’une autre entité dans la même déclaration est source de confusion et inutile.

##### Exemple, mauvais

    struct Data { /*…*/ } data{ /*…*/ };

##### Exemple, bon

    struct Data { /*…*/ };
    Data data{ /*…*/ };

##### Application

* Signaler si le `}` d’une définition de classe ou d’enumération n’est pas suivi d’un `;`. Le `;` manque.

### <a name="rc-class"></a>C.8 : Utiliser `class` plutôt que `struct` si un membre est non‑public

##### Raison

Lisibilité.  
Pour indiquer clairement que quelque chose est caché/abstrait.  
C’est une convention utile.

##### Exemple, mauvais

    struct Date {
        int d, m;

        Date(int i, Month m);
        // … beaucoup de fonctions …
    private:
        int y;  // année
    };

Il n’y a rien d’illégal dans ce code du point de vue des règles du C++, mais presque tout est inadéquat d’un point de vue de la conception. Les données privées sont cachées loin des données publiques. Les données sont réparties dans différentes parties de la déclaration de classe. Les différentes parties ont des niveaux d’accès différents. Tout cela diminue la lisibilité et complique la maintenance.

##### Remarque

Préférer placer l’interface en premier dans une classe, [voir NL.16](#rl-order).

##### Application

Signaler les classes déclarées avec `struct` si elles possèdent un membre `private` ou `protected`.

### <a name="rc-private"></a>C.9 : Minimiser l’exposition des membres

##### Raison

Encapsulation.  
Masquage de l’information.  
Réduire les risques d’accès non intentionnels.  
Cela simplifie la maintenance.

##### Exemple

template<typename T, typename U>
struct pair {
    T a;
    U b;
    // …
};

Quel que soit le code placé dans la partie `//`, un utilisateur arbitraire d’un `pair` peut changer librement et indépendamment ses `a` et `b`. Dans un gros code‑base, on ne peut pas facilement repérer quel code fait quoi aux membres de `pair`. Cela peut être exactement ce que l’on veut, mais si l’on veut imposer une relation entre les membres, il faut les rendre `private` et faire respecter cette relation (invariante) via les constructeurs et les fonctions membres. Par exemple :

    class Distance {
    public:
        // …
        double meters() const { return magnitude*unit; }
        void set_unit(double u)
        {
                // … vérifier que u est un facteur de 10 …
                // … ajuster magnitude en conséquence …
                unit = u;
        }
        // …
    private:
        double magnitude;
        double unit;    // 1 = mètres, 1000 = kilomètres, 0.001 = millimètres, etc.
    };

##### Remarque

Si l’ensemble d’utilisateurs directs d’un ensemble de variables ne peut pas être déterminé facilement, le type ou l’usage de cet ensemble ne peut pas être (facilement) changé/amélioré. Pour les données `public` et `protected`, c’est généralement le cas.

##### Exemple

Une classe peut fournir deux interfaces à ses utilisateurs. Une pour les classes dérivées (`protected`) et une pour les utilisateurs généraux (`public`). Par exemple, une classe dérivée peut être autorisée à sauter un test d’exécution parce qu’elle a déjà garanti la validité :

    class Foo {
    public:
        int bar(int x) { check(x); return do_bar(x); }
        // …
    protected:
        int do_bar(int x); // faire une opération sur les données
        // …
    private:
        // … données …
    };

    class Dir : public Foo {
        //…
        int mem(int x, int y)
        {
            /* … faire quelque chose … */
            return do_bar(x + y); // OK : la classe dérivée peut contourner le check
        }
    };

    void user(Foo& x)
    {
        int r1 = x.bar(1);      // OK, vérifiera
        int r2 = x.do_bar(2);   // erreur : contournerait le check
        // …
    }

##### Remarque

[`protected` data is a bad idea](#rh-protected) (les données `protected` sont une mauvaise idée).

##### Remarque

Préférer l’ordre `public` avant `protected` avant `private` ; voir [NL.16](#rl-order).

##### Application

* [Signaler les données `protected`](#rh-protected).
* Signaler les mélanges de données `public` et `private`.

## <a name="ss-concrete"></a>C.concrete : Types concrets

Résumé des règles de type concret :

* [C.10 : Privilégier les types concrets aux hiérarchies de classes](#rc-concrete)
* [C.11 : Rendre les types concrets réguliers](#rc-regular)
* [C.12 : Ne pas rendre les membres de données `const` ou des références dans un type copiable ou déplaçable](#rc-constref)
* [C.13 : Si le membre de donnée `B` utilise le membre de donnée `A`, déclarer `A` avant `B`](#rc-lifetime)

### <a name="rc-concrete"></a>C.10 : Privilégier les types concrets aux hiérarchies de classes

##### Raison

Un type concret est fondamentalement plus simple qu’un type appartenant à une hiérarchie de classes : plus facile à concevoir, à implémenter, à utiliser, à raisonner, plus petit et plus rapide. Il faut une raison (cas d’usage) pour utiliser une hiérarchie.

##### Exemple

    class Point1 {
        int x, y;
        // … opérations …
        // … pas de fonctions virtuelles …
    };

    class Point2 {
        int x, y;
        // … opérations, certaines virtuelles …
        virtual ~Point2();
    };

    void use()
    {
        Point1 p11 {1, 2};   // créer un objet sur la pile
        Point1 p12 {p11};    // une copie

        auto p21 = make_unique<Point2>(1, 2);   // créer un objet sur le tas
        auto p22 = p21->clone();                // créer une copie
        // …
    }

Si une classe fait partie d’une hiérarchie, nous (dans du code réel, pas forcément dans de petits exemples) devons manipuler ses objets via des pointeurs ou références. Cela implique plus de surcoût mémoire, plus d’allocations et de désallocations, et plus de surcharge d’exécution pour les indirections résultantes.

##### Remarque

Les types concrets peuvent être alloués sur la pile et être membres d’autres classes.

##### Remarque

L’usage d’indirection est fondamental pour les interfaces polymorphes d’exécution. Le surcoût d’allocation/désallocation n’est pas (c’est simplement le cas le plus fréquent). On peut utiliser une classe de base comme interface d’un objet à durée limitée d’une classe dérivée. Cela se fait lorsque l’allocation dynamique est prohibée (par ex. temps réel strict) et pour fournir une interface stable à certains types de plug‑ins.

##### Application

???

### <a name="rc-regular"></a>C.11 : Rendre les types concrets réguliers

##### Raison

Les types réguliers sont plus faciles à comprendre et à raisonner que les types irréguliers (les irrégularités nécessitent un effort supplémentaire). Les types intégrés du C++ sont réguliers, tout comme les classes de la bibliothèque standard telles que `string`, `vector` et `map`. On peut définir des classes concrètes sans assignation et égalité, mais elles sont (et devraient être) rares.

##### Exemple

    struct Bundle {
        string name;
        vector<Record> vr;
    };

    bool operator==(const Bundle& a, const Bundle& b)
    {
        return a.name == b.name && a.vr == b.vr;
    }

    Bundle b1 { "my bundle", {r1, r2, r3}};
    Bundle b2 = b1;
    if (!(b1 == b2)) error("impossible!");
    b2.name = "the other bundle";
    if (b1 == b2) error("No!");

En particulier, si un type concret est copiable, il faut de préférence également lui fournir un opérateur de comparaison d’égalité, et s’assurer que `a = b` implique `a == b`.

##### Remarque

Pour les `struct` destinées à être partagées avec du code C, définir `operator==` peut ne pas être réalisable.

##### Remarque

Les gestionnaires de ressources qui ne peuvent pas être clonés, par ex. un `scoped_lock` pour un `mutex`, sont des types concrets mais ne peuvent généralement pas être copiés (ils peuvent généralement être déplacés), donc ils ne sont pas réguliers ; ils tendent à être `move‑only`.

##### Application

???

### <a name="rc-constref"></a>C.12 : Ne pas rendre les membres de données `const` ou des références dans un type copiable ou déplaçable

##### Raison

Les membres `const` et les références ne sont pas utiles dans un type copiable ou déplaçable, et rendent ces types difficiles à utiliser en les rendant au moins partiellement non copiable/non déplaçable pour des raisons subtiles.

##### Exemple ; mauvais

    class bad {
        const int i;    // mauvais
        string& s;      // mauvais
        // …
    };

Les membres `const` et `&` rendent cette classe « seulement‑un‑peu‑copiable » — constructible mais non assignable.

##### Remarque

Si vous avez besoin qu’un membre pointe vers quelque chose, utilisez un pointeur (brut ou intelligent, et `gsl::not_null` s’il ne doit pas être nul) au lieu d’une référence.

##### Application

Signaler tout membre de données qui est `const`, `&` ou `&&` dans un type qui possède une opération de copie ou de déplacement.

### <a name="rc-lifetime"></a>C.13 : Si le membre de donnée `B` utilise le membre de donnée `A`, déclarer `A` avant `B`

##### Raison

Les membres de données sont initialisés dans l’ordre de leur déclaration, et détruits dans l’ordre inverse.

##### Discussion

Si le membre `B` utilise le membre `A`, alors `A` doit être déclaré avant `B` afin que `A` survive plus longtemps que `B`, c’est‑à‑dire que la durée de vie de `A` commence avant et se termine après celle de `B`. Sinon, lors de la construction et de la destruction, `B` tentera d’utiliser `A` en dehors de sa durée de vie.

##### Exemple ; mauvais

    // Mauvais : b utilise a, mais a est déclaré après b.
    //          Ordre de construction : b puis a ; ordre de destruction : a puis b.
    //          Donc b touche a en dehors de la durée de vie de a.

    class X {
        struct B {
            string* p;
            explicit B(string& a) : p{&a} {}
            ~B() { cout << *p; }                       // utilise a (via p)
        };

        B      b;                                      // construit en premier
        string a = "some heap allocated string value"; // construit après b ; détruit avant b

    public:
        X() : b{a} {}   // utilise a avant qu’il ne soit construit → UB d’utilisation avant allocation
        ~X() = default; // accède à a après sa destruction → UB d’utilisation après libération
    };

##### Exemple ; bon

    // Corrigé : déclarer simplement a avant b

    class X {
        struct B {
            string* p;
            explicit B(string& a) : p{&a} {}
            ~B() { cout << *p; }                       // utilise a (via p)
        };

        string a = "some heap allocated string value"; // construit avant b ; détruit après b
        B      b;                                      // construit deuxième

    public:
        X() : b{a} {}   // ok
        ~X() = default; // ok
    };

##### Exemple ; mauvais (concurrence)

    class X {
    public:
        X()
            : a{std::make_unique<int>(12)}
        {
            b = std::make_unique<std::jthread>(
                [this]{
                std::this_thread::sleep_for(std::chrono::seconds(1));
                std::cout << "Value: " << *a << std::endl;
              });
        }

        std::unique_ptr<std::jthread> b;
        std::unique_ptr<int>          a;
    };

##### Exemple ; bon (concurrence)

    // Corrigé : déclarer simplement a avant b

    class X {
    public:
        X()
            : a{std::make_unique<int>(12)}
        {
            b = std::make_unique<std::jthread>(
                [this]{
                std::this_thread::sleep_for(std::chrono::seconds(1));
                std::cout << "Value: " << *a << std::endl;
              });
        }

        std::unique_ptr<int>          a;
        std::unique_ptr<std::jthread> b;
    };

##### Application

* Signaler un initialiseur de membre qui fait référence à un objet avant qu’il ne soit construit.

## <a name="s-ctor"></a>C.ctor : Constructeurs, assignations et destructeurs

Ces fonctions contrôlent le cycle de vie des objets : création, copie, déplacement et destruction.  
Définissez les constructeurs afin de garantir et de simplifier l’initialisation des classes.

Voici les *opérations par défaut* :

* un constructeur par défaut : `X()`
* un constructeur de copie : `X(const X&)`
* une assignation par copie : `operator=(const X&)`
* un constructeur de déplacement : `X(X&&)`
* une assignation par déplacement : `operator=(X&&)`
* un destructeur : `~X()`

Par défaut, le compilateur définit chacune de ces opérations si elle est utilisée, mais le défaut peut être supplanté.

Les opérations par défaut forment un ensemble d’opérations liées qui implémentent ensemble la sémantique du cycle de vie d’un objet. Par défaut, C++ traite les classes comme des types à valeur, mais tous les types ne sont pas à valeur.

Règles liées aux opérations par défaut :

* [C.20 : Si vous pouvez éviter de définir des opérations par défaut, faites‑le](#rc-zero)
* [C.21 : Si vous définissez ou `=delete` une fonction de copie, de déplacement ou un destructeur, définissez ou `=delete` toutes les autres](#rc-five)
* [C.22 : Rendre les opérations par défaut cohérentes](#rc-matched)

Règles relatives aux destructeurs :

* [C.30 : Définir un destructeur si la classe a besoin d’une action explicite à la destruction de l’objet](#rc-dtor)
* [C.31 : Toutes les ressources acquises par une classe doivent être libérées par le destructeur de la classe](#rc-dtor-release)
* [C.32 : Si une classe possède un pointeur brut (`T*`) ou une référence (`T&`), considérer s’il s’agit d’une possession](#rc-dtor-ptr)
* [C.33 : Si une classe possède un membre pointeur possesseur, définir un destructeur](#rc-dtor-ptr2)
* [C.35 : Le destructeur d’une classe de base doit être soit public et virtuel, soit protégé et non‑virtuel](#rc-dtor-virtual)
* [C.36 : Un destructeur ne doit pas échouer](#rc-dtor-fail)
* [C.37 : Marquer les destructeurs `noexcept`](#rc-dtor-noexcept)

Règles relatives aux constructeurs :

* [C.40 : Définir un constructeur si la classe possède une invariante](#rc-ctor)
* [C.41 : Un constructeur doit créer un objet complètement initialisé](#rc-complete)
* [C.42 : Si un constructeur ne peut pas construire un objet valide, lever une exception](#rc-throw)
* [C.43 : S’assurer qu’une classe copiable possède un constructeur par défaut](#rc-default0)
* [C.44 : Privilégier des constructeurs par défaut simples et non‑excepteurs](#rc-default00)
* [C.45 : Ne pas définir de constructeur par défaut qui se contente d’initialiser les membres ; utiliser les initialiseurs de membres par défaut à la place](#rc-default)
* [C.46 : Par défaut, déclarer les constructeurs à un seul argument `explicit`](#rc-explicit)
* [C.47 : Définir et initialiser les membres de données dans l’ordre de leur déclaration](#rc-order)
* [C.48 : Privilégier les initialiseurs de membres par défaut aux initialiseurs de membres dans les constructeurs pour les initialiseurs constants](#rc-in-class-initializer)
* [C.49 : Privilégier l’initialisation à l’affectation dans les constructeurs](#rc-initialize)
* [C.50 : Utiliser une fonction‑fabrique si vous avez besoin d’un « comportement virtuel » lors de l’initialisation](#rc-factory)
* [C.51 : Utiliser les constructeurs délégués pour représenter les actions communes à tous les constructeurs d’une classe](#rc-delegating)
* [C.52 : Utiliser les constructeurs hérité pour importer les constructeurs dans une classe dérivée qui n’a pas besoin d’une initialisation explicite supplémentaire](#rc-inheriting)

Règles relatives à la copie et au déplacement :

* [C.60 : Rendre l’assignation par copie non‑`virtual`, prendre le paramètre par `const&` et retourner par `non‑const&`](#rc-copy-assignment)
* [C.61 : Une opération de copie doit copier](#rc-copy-semantic)
* [C.62 : Rendre l’assignation par copie sûre pour l’auto‑assignation](#rc-copy-self)
* [C.63 : Rendre l’assignation par déplacement non‑`virtual`, prendre le paramètre par `&&` et retourner par `non‑const&`](#rc-move-assignment)
* [C.64 : Une opération de déplacement doit déplacer et laisser sa source dans un état valide](#rc-move-semantic)
* [C.65 : Rendre l’assignation par déplacement sûre pour l’auto‑assignation](#rc-move-self)
* [C.66 : Rendre les opérations de déplacement `noexcept`](#rc-move-noexcept)
* [C.67 : Une classe polymorphe doit supprimer la copie/déplacement publique](#rc-copy-virtual)

Autres règles d’opérations par défaut :

* [C.80 : Utiliser `=default` si vous devez être explicite sur l’usage de la sémantique par défaut](#rc-eqdefault)
* [C.81 : Utiliser `=delete` quand vous voulez désactiver le comportement par défaut (sans vouloir une alternative)](#rc-delete)
* [C.82 : Ne pas appeler de fonctions virtuelles dans les constructeurs et destructeurs](#rc-ctor-virtual)
* [C.83 : Pour les types à valeur, envisager de fournir une fonction `swap` `noexcept`](#rc-swap)
* [C.84 : Un `swap` ne doit pas échouer](#rc-swap-fail)
* [C.85 : Rendre `swap` `noexcept`](#rc-swap-noexcept)
* [C.86 : Rendre `==` symétrique par rapport aux types d’opérandes et `noexcept`](#rc-eq)
* [C.87 : Prudence avec `==` sur les classes de base](#rc-eq-base)
* [C.89 : Rendre un `hash` `noexcept`](#rc-hash)
* [C.90 : S’appuyer sur les constructeurs et les opérateurs d’assignation, pas sur `memset` et `memcpy`](#rc-memset)

## <a name="ss-defop"></a>C.defop : Opérations par défaut

Par défaut, le langage fournit les opérations par défaut avec leur sémantique par défaut. Cependant, un programmeur peut désactiver ou remplacer ces défauts.

### <a name="rc-zero"></a>C.20 : Si vous pouvez éviter de définir des opérations par défaut, faites‑le

##### Raison

C’est le plus simple et cela donne la sémantique la plus claire.

##### Exemple

    struct Named_map {
    public:
        explicit Named_map(const string& n) : name(n) {}
        // pas de constructeurs copie/déplacement
        // pas d’opérateurs d’assignation copie/déplacement
        // pas de destructeur
    private:
        string name;
        map<int, int> rep;
    };

    Named_map nm("map"); // construction
    Named_map nm2 {nm};  // construction par copie

Comme `std::map` et `string` possèdent toutes les fonctions spéciales, aucun travail supplémentaire n’est nécessaire.

##### Remarque

On parle de « règle du zéro ».

##### Application

(Non enforceable) Bien que non enforceable, un bon analyseur statique peut détecter des motifs indiquant une amélioration possible pour se conformer à cette règle. Par exemple, une classe avec un couple (pointeur, taille) de membres et un destructeur qui `delete` le pointeur pourrait probablement être remplacée par un `vector`.

### <a name="rc-five"></a>C.21 : Si vous définissez ou `=delete` une fonction de copie, de déplacement ou un destructeur, définissez ou `=delete` toutes les autres

##### Raison

Les sémantiques de copie, déplacement et destruction sont étroitement liées ; si l’une doit être déclarée, il est probable que les autres nécessitent également une considération.

Déclarer toute fonction de copie/déplacement/destructeur,
même comme `=default` ou `=delete`, supprime la déclaration implicite d’un constructeur de déplacement et d’un opérateur d’assignation de déplacement. Déclarer un constructeur de déplacement ou un opérateur d’assignation de déplacement, même comme `=default` ou `=delete`, fera que le constructeur de copie ou l’opérateur d’assignation de copie implicites seront définis comme supprimés. Ainsi, dès que l’une de ces fonctions est déclarée, les autres devraient toutes être déclarées afin d’éviter des effets indésirables, comme transformer tous les déplacements potentiels en copies plus coûteuses, ou faire d’une classe une classe uniquement déplacable.

##### Exemple, mauvais

    struct M2 {   // mauvais : ensemble incomplet d’opérations copie/déplacement/destructeur
    public:
        // …
        // … pas d’opérations copie ou déplacement …
        ~M2() { delete[] rep; }
    private:
        pair<int, int>* rep;  // ensemble de paires terminé par zéro
    };

    void use()
    {
        M2 x;
        M2 y;
        // …
        x = y;   // assignation par défaut
        // …
    }

Étant donné que le destructeur nécessitait une « attention particulière » (ici, désallocation), la probabilité que les opérateurs de copie et de déplacement implicites soient corrects est faible (ici, on aurait une double désallocation).

##### Remarque

C’est ce que l’on appelle « la règle des cinq ».

##### Remarque

Si vous voulez une implémentation par défaut (tout en définissant une autre), écrivez `=default` pour montrer que vous le faites intentionnellement pour cette fonction. Si vous ne voulez pas de fonction par défaut générée, supprimez‑la avec `=delete`.

##### Exemple, bon

Lorsque le destructeur doit être déclaré juste pour le rendre `virtual`, il peut être défini comme par défaut.

    class AbstractBase {
    public:
        virtual void foo() = 0;  // au moins une méthode abstraite pour rendre la classe abstraite
        virtual ~AbstractBase() = default;
        // …
    };

Pour prévenir le slicing conformément à [C.67](#rc-copy-virtual),
rendre les opérations de copie et de déplacement protégées ou `=delete`, et ajouter un `clone` :

    class CloneableBase {
    public:
        virtual unique_ptr<CloneableBase> clone() const;
        virtual ~CloneableBase() = default;
        CloneableBase() = default;
        CloneableBase(const CloneableBase&) = delete;
        CloneableBase& operator=(const CloneableBase&) = delete;
        CloneableBase(CloneableBase&&) = delete;
        CloneableBase& operator=(CloneableBase&&) = delete;
        // … autres constructeurs et fonctions …
    };

Définir seulement les opérations de déplacement ou seulement les opérations de copie aurait le même effet, mais exprimer explicitement l’intention pour chaque fonction spéciale le rend plus évident pour le lecteur.

##### Remarque

Les compilateurs appliquent beaucoup de cette règle et, idéalement, avertissent de toute violation.

##### Remarque

Compter sur une opération de copie implicite dans une classe avec un destructeur est déconseillé.

##### Remarque

Écrire ces fonctions peut être source d’erreurs. Notez leurs types d’argument :

    class X {
    public:
        // …
        virtual ~X() = default;               // destructeur (virtual si X est destinée à être une classe de base)
        X(const X&) = default;                // constructeur de copie
        X& operator=(const X&) = default;     // assignation de copie
        X(X&&) noexcept = default;            // constructeur de déplacement
        X& operator=(X&&) noexcept = default; // assignation de déplacement
    };

Une petite erreur (comme une faute de frappe, l’omission d’un `const`, l’utilisation de `&` au lieu de `&&`, ou l’omission d’une fonction spéciale) peut entraîner des erreurs ou des avertissements. Pour éviter la fastidiosité et le risque d’erreurs, essayez de suivre la [règle du zéro](#rc-zero).

##### Application

(Simple) Une classe devrait avoir une déclaration (même `=delete`) pour soit toutes, soit aucune des fonctions copie/déplacement/destructeur.

### <a name="rc-matched"></a>C.22 : Rendre les opérations par défaut cohérentes

##### Raison

Les opérations par défaut forment conceptuellement un ensemble assorti. Leurs sémantiques sont inter‑reliées. Les utilisateurs seront surpris si les constructions/assignations de copie/déplacement font logiquement des choses différentes. Ils seront également surpris si les constructeurs et destructeurs ne donnent pas une vue cohérente de la gestion des ressources. Enfin, ils seront surpris si la copie et le déplacement ne reflètent pas la façon dont les constructeurs et destructeurs fonctionnent.

##### Exemple, mauvais

    class Silly {   // MAUVAIS : opérations de copie incohérentes
        class Impl {
            // …
        };
        shared_ptr<Impl> p;
    public:
        Silly(const Silly& a) : p(make_shared<Impl>()) { *p = *a.p; }   // copie profonde
        Silly& operator=(const Silly& a) { p = a.p; return *this; }   // copie superficielle
        // …
    };

Ces opérations sont en désaccord sur la sémantique de copie. Cela conduira à de la confusion et des bugs.

##### Application

* (Complexe) Un constructeur/copy‑constructor et l’opérateur d’assignation correspondant doivent écrire dans les mêmes membres de données au même niveau de déréférencement.
* (Complexe) Tous les membres écrits dans un constructeur/copieur doivent aussi être initialisés par tous les autres constructeurs.
* (Complexe) Si un constructeur/copieur effectue une copie profonde d’un membre, alors le destructeur doit modifier ce membre.
* (Complexe) Si un destructeur modifie un membre, ce membre doit être écrit dans tous les constructeurs/copieurs ou opérateurs d’assignation.

## <a name="ss-dtor"></a>C.dtor : Destructeurs

« Cette classe a‑t‑elle besoin d’un destructeur ? » est une question de conception très révélatrice. Pour la plupart des classes, la réponse est « non » soit parce que la classe ne détient aucune ressource, soit parce que la destruction est gérée par [la règle du zéro](#rc-zero) ; c’est‑à‑dire, ses membres peuvent se charger eux‑mêmes de la destruction. Si la réponse est « oui », une grande partie de la conception de la classe suit (voir [la règle des cinq](#rc-five)).

### <a name="rc-dtor"></a>C.30 : Définir un destructeur si une classe a besoin d’une action explicite à la destruction de l’objet

##### Raison

Un destructeur est invoqué implicitement à la fin de la durée de vie d’un objet. Si le destructeur par défaut suffit, utilisez‑le. Ne définissez un destructeur non‑par défaut que si la classe doit exécuter du code qui ne fait pas déjà partie des destructeurs de ses membres.

##### Exemple

    template<typename A>
    struct final_action {   // légèrement simplifié
        A act;
        final_action(A a) : act{a} {}
        ~final_action() { act(); }
    };

    template<typename A>
    final_action<A> finally(A act)   // déduire le type d’action
    {
        return final_action<A>{act};
    }

    void test()
    {
        auto act = finally([] { cout << "Exit test\n"; });  // établir l’action de sortie
        // …
        if (something) return;   // act exécuté ici
        // …
    } // act exécuté ici

Le but de `final_action` est d’exécuter un morceau de code (généralement un lambda) à la destruction.

##### Remarque

Il existe deux catégories générales de classes qui nécessitent un destructeur défini par l’utilisateur :

* Une classe possédant une ressource qui n’est pas déjà représentée comme une classe avec un destructeur, par ex. un `vector` ou une classe transactionnelle.
* Une classe qui existe principalement pour exécuter une action à la destruction, comme un traceur ou `final_action`.

##### Exemple, mauvais

    class Foo {   // mauvais ; utilisez le destructeur par défaut
    public:
        // …
        ~Foo() { s = ""; i = 0; vi.clear(); }  // nettoyage
    private:
        string s;
        int    i;
        vector<int> vi;
    };

Le destructeur par défaut le fait mieux, plus efficacement, et ne peut pas se tromper.

##### Application

Rechercher les « ressources implicites », telles que pointeurs et références. Chercher les classes avec destructeurs même si tous leurs membres ont des destructeurs.

### <a name="rc-dtor-release"></a>C.31 : Toutes les ressources acquises par une classe doivent être libérées par le destructeur de la classe

##### Raison

Prévention des fuites de ressources, surtout dans les cas d’erreur.

##### Remarque

Pour les ressources représentées comme des classes avec un ensemble complet d’opérations par défaut, cela se passe automatiquement.

##### Exemple

    class X {
        ifstream f;   // peut posséder un fichier
        // … pas d’opérations par défaut définies ou =deleted …
    };

Le `ifstream` de `X` ferme implicitement tout fichier qu’il aurait pu ouvrir lors de la destruction de `X`.

##### Exemple, mauvais

    class X2 {     // mauvais
        FILE* f;   // peut posséder un fichier
        // … pas d’opérations par défaut définies ou =deleted …
    };

`X2` pourrait fuir un descripteur de fichier.

##### Remarque

Qu’en est‑il d’une socket qui ne se ferme pas ? Un destructeur, une fonction `close` ou de nettoyage **ne doit jamais échouer** (#rc-dtor-fail). S’il le fait quand même, on se retrouve avec un problème sans vraie solution. Le rédacteur d’un destructeur ne sait pas pourquoi il est appelé et ne peut « refuser d’agir » en lançant une exception. Voir la [discussion](#sd-never-fail). De plus, de nombreuses opérations de « close/release » ne sont pas ré‑essayables. Beaucoup ne le sont pas. Beaucoup ont tenté de résoudre ce problème, mais aucune solution générale n’est connue. Si possible, considérer l’échec de la fermeture/nettoyage comme une erreur de conception fondamentale et terminer le programme.

##### Remarque

Une classe peut contenir des pointeurs et références vers des objets qu’elle ne possède pas. Évidemment, ces objets ne doivent **pas** être `delete` par le destructeur de la classe. Par exemple :

    Preprocessor pp { /* … */ };
    Parser       p { pp, /* … */ };
    Type_checker tc { p, /* … */ };

Ici `p` se réfère à `pp` mais ne le possède pas.

##### Application

* (Simple) Si une classe possède des membres pointeur ou référence qui sont propriétaires (par ex. désignés comme propriétaires via `gsl::owner`), ils doivent être mentionnés dans son destructeur.
* (Difficile) Déterminer si les membres pointeur ou référence sont propriétaires lorsqu’il n’y a aucune déclaration explicite de propriété (par ex. examiner les constructeurs).

### <a name="rc-dtor-ptr"></a>C.32 : Si une classe possède un pointeur brut (`T*`) ou une référence (`T&`), considérer si elle pourrait être propriétaire

##### Raison

Beaucoup de code est vague sur la propriété.

##### Exemple

    class legacy_class
    {
        foo* m_owning;   // Mauvais : changer en unique_ptr<T> ou owner<T*>
        bar* m_observer; // OK : garder
    }

La seule façon de déterminer la propriété peut être l’analyse de code.

##### Remarque

La propriété doit être claire dans le nouveau code (et le code refactorisé) selon [R.20](#rr-owner) pour les pointeurs propriétaires et [R.3](#rr-ptr) pour les pointeurs non‑propriétaires. Les références ne doivent jamais être propriétaires [R.4](#rr-ref).

##### Application

Regarder l’initialisation des pointeurs bruts membres et des références membres et voir si une allocation est utilisée.

### <a name="rc-dtor-ptr2"></a>C.33 : Si une classe possède un pointeur propriétaire, définir un destructeur

##### Raison

Un objet possédé doit être `delete` lors de la destruction de l’objet qui le possède.

##### Exemple

Un pointeur membre pourrait représenter une ressource.  
Un `T*` ne devrait **pas** faire cela (#rr-ptr), mais dans le code hérité c’est fréquent. Considérez un `T*` comme un possible propriétaire et donc suspect.

    template<typename T>
    class Smart_ptr {
        T* p;   // MAUVAIS : vague sur la propriété de *p
        // …
    public:
        // ... pas d’opérations par défaut définies ...
    };

    // sans destructeur
    void use(Smart_ptr<int> p1)
    {
        // erreur : p2.p fuit (si pas nullptr et pas possédé par un autre code)
        auto p2 = p1;
    }

Notez que si vous définissez un destructeur, vous devez définir ou supprimer [toutes les opérations par défaut](#rc-five) :

    template<typename T>
    class Smart_ptr2 {
        T* p;   // MAUVAIS : vague sur la propriété de *p
        // …
    public:
        // … pas d’opérations de copie utilisateur …
        ~Smart_ptr2() { delete p; }  // p est propriétaire !
    };

    void use(Smart_ptr2<int> p1)
    {
        auto p2 = p1;   // erreur : double suppression
    }

Le destructeur par défaut fera simplement copier `p1.p` dans `p2.p`, entraînant une double destruction de `p1.p`. Soyez explicite sur la propriété :

    template<typename T>
    class Smart_ptr3 {
        owner<T*> p;   // OK : explicite sur la propriété de *p
        // …
    public:
        // …
        // … opérations de copie et de déplacement …
        ~Smart_ptr3() { delete p; }
    };

    void use(Smart_ptr3<int> p1)
    {
        auto p2 = p1;   // OK : aucune double suppression
    }

##### Remarque

Souvent, la façon la plus simple d’obtenir un destructeur est de remplacer le pointeur par un pointeur intelligent (par ex. `std::unique_ptr`) et laisser le compilateur gérer la destruction correctement.

##### Remarque

Pourquoi pas simplement exiger que tous les pointeurs propriétaires soient des « smart pointers » ? Cela impliquerait parfois des changements de code non triviaux et pourrait affecter les ABI.

##### Application

* Une classe avec un membre pointeur est suspecte.
* Une classe avec un `owner<T>` doit définir ses opérations par défaut.

### <a name="rc-dtor-virtual"></a>C.35 : Le destructeur d’une classe de base doit être soit public et virtuel, soit protégé et non‑virtuel

##### Raison

Éviter le comportement indéfini. Si le destructeur est public, le code appelant peut tenter de détruire un objet dérivé via un pointeur de base, et le résultat est indéfini si le destructeur de la base n’est pas virtuel. Si le destructeur est protégé, le code appelant ne peut pas détruire via un pointeur de base et le destructeur n’a pas besoin d’être virtuel ; il doit cependant être protégé, pas privé, afin que les destructeurs dérivés puissent l’invoquer. En général, l’auteur d’une classe de base ne connaît pas l’action appropriée à exécuter lors de la destruction.

##### Discussion

Voir [cette partie dans la section Discussion](#sd-dtor).

##### Exemple, mauvais

    struct Base {  // MAUVAIS : destructeur public non‑virtuel implicite
        virtual void f();
    };

    struct D : Base {
        string s {"a resource needing cleanup"};
        ~D() { /* … faire du nettoyage … */ }
        // …
    };

    void use()
    {
        unique_ptr<Base> p = make_unique<D>();
        // …
    } // la destruction de p appelle ~Base(), pas ~D(), ce qui fuit s et possiblement plus

##### Remarque

Une fonction virtuelle définit une interface pour les classes dérivées qui peut être utilisée sans connaître les classes dérivées. Si l’interface autorise la destruction, elle doit pouvoir le faire en toute sécurité.

##### Remarque

Un destructeur ne doit pas être privé, sinon il empêche l’utilisation du type :

    class X {
        ~X();   // destructeur privé
        // …
    };

    void use()
    {
        X a;                        // erreur : impossible de détruire
        auto p = make_unique<X>();  // erreur : impossible de détruire
    }

##### Exception

On peut imaginer un cas où vous voudriez un destructeur protégé **et virtuel** : lorsqu’un objet d’un type dérivé (et uniquement d’un tel type) devrait pouvoir détruire *un autre* objet (pas lui‑même) via un pointeur vers la base. Nous n’avons pas vu de tel cas en pratique.

##### Application

* Une classe contenant des fonctions virtuelles doit avoir un destructeur qui est soit public et virtuel, soit protégé et non‑virtuel.
* Si une classe hérite publiquement d’une classe de base, la base doit avoir un destructeur qui est soit public et virtuel, soit protégé et non‑virtuel.

### <a name="rc-dtor-fail"></a>C.36 : Un destructeur ne doit pas échouer

##### Raison

En général, on ne sait pas comment écrire du code sans erreur si le destructeur doit échouer. La bibliothèque standard exige que toutes les classes qu’elle manipule possèdent des destructeurs qui ne sortent pas en lançant une exception.

##### Exemple

    class X {
    public:
        ~X() noexcept;
        // …
    };

    X::~X() noexcept
    {
        // …
        if (cannot_release_a_resource) terminate();
        // …
    }

##### Remarque

Beaucoup ont tenté de concevoir un schéma infaillible pour gérer les échecs dans les destructeurs. Aucun n’a réussi à proposer un schéma général. Cela peut être un problème réel : par ex. qu’en est‑il d’une socket qui ne se ferme pas ? L’auteur d’un destructeur ne sait pas pourquoi il est appelé et ne peut « refuser d’agir » en lançant une exception. Voir la [discussion](#sd-never-fail). De plus, de nombreuses opérations de « close/release » ne sont pas ré‑essayables. Si possible, considérer l’échec de fermeture/nettoyage comme une erreur de conception fondamentale et terminer le programme.

##### Remarque

Déclarez un destructeur `noexcept`. Cela garantit qu’il se termine normalement ou qu’il termine le programme.

##### Remarque

Si une ressource ne peut pas être libérée et que le programme ne doit pas échouer, essayez de signaler l’échec au reste du système d’une manière quelconque (peut‑être même en modifiant un état global et en espérant que quelque chose le remarque et puisse gérer le problème). Soyez pleinement conscient que cette technique est spéciale et sujette aux erreurs. Considérez l’exemple d’une connexion qui ne se ferme pas. Probablement il y a un problème à l’autre extrémité et seul le code responsable des deux extrémités peut correctement gérer le problème. Le destructeur pourrait envoyer un message (d’une façon ou d’une autre) à la partie responsable du système, considérer que la connexion a été fermée et retourner normalement.

##### Remarque

Si un destructeur utilise des opérations qui peuvent échouer, il peut attraper les exceptions et, dans certains cas, finir avec succès (par ex. en utilisant un mécanisme de nettoyage différent de celui qui a lancé l’exception).

##### Application

(Simple) Un destructeur devrait être déclaré `noexcept` s’il pourrait lancer une exception.

### <a name="rc-dtor-noexcept"></a>C.37 : Marquer les destructeurs `noexcept`

##### Raison

[Un destructeur ne doit pas échouer](#rc-dtor-fail). Si un destructeur essaie de sortir avec une exception, c’est une mauvaise conception et le programme devrait idéalement se terminer.

##### Remarque

Un destructeur (qu’il soit défini par l’utilisateur ou généré par le compilateur) est déclaré implicitement `noexcept` (indépendamment du code de son corps) si tous les membres de sa classe possèdent des destructeurs `noexcept`. En déclarant explicitement les destructeurs `noexcept`, l’auteur se protège contre le fait que le destructeur devienne implicitement `noexcept(false)` suite à l’ajout ou à la modification d’un membre de la classe.

##### Exemple

Tous les destructeurs ne sont pas `noexcept` par défaut ; un membre qui lance entraîne toute la hiérarchie :

    struct X {
        Details x;  // a un destructeur qui peut lancer
        // …
        ~X() { }    // implicitement noexcept(false) ; c’est‑à‑dire peut lancer
    };

Donc, en cas de doute, déclarez le destructeur `noexcept`.

##### Remarque

Pourquoi ne pas déclarer tous les destructeurs `noexcept` ? Parce que dans de nombreux cas – surtout les simples – cela créerait du bruit inutile.

##### Application

(Simple) Un destructeur devrait être déclaré `noexcept` s’il pourrait lancer.

## <a name="ss-ctor"></a>C.ctor : Constructeurs

Un constructeur définit comment un objet est initialisé (construit).

### <a name="rc-ctor"></a>C.40 : Définir un constructeur si une classe possède une invariante

##### Raison

C’est exactement le rôle des constructeurs.

##### Exemple

    class Date {  // une Date représente une date valide
                  // entre le 1 janvier 1900 et le 31 décembre 2100
        Date(int dd, int mm, int yy)
            :d{dd}, m{mm}, y{yy}
        {
            if (!is_valid(d, m, y)) throw Bad_date{};  // imposer l’invariante
        }
        // …
    private:
        int d, m, y;
    };

Il est souvent judicieux d’exprimer l’invariante comme une clause `Ensures` sur le constructeur.

##### Remarque

Un constructeur peut être utilisé par commodité même si la classe n’a pas d’invariante. Par ex. :

    struct Rec {
        string s;
        int    i {0};
        Rec(const string& ss) : s{ss} {}
        Rec(int ii) :i{ii} {}
    };

    Rec r1 {7};
    Rec r2 {"Foo bar"};

##### Remarque

La règle de la liste d’initialisation C++11 élimine le besoin de nombreux constructeurs. Par ex. :

    struct Rec2{
        string s;
        int    i;
        Rec2(const string& ss, int ii = 0) :s{ss}, i{ii} {}   // redondant
    };

    Rec2 r1 {"Foo", 7};
    Rec2 r2 {"Bar"};

Le constructeur `Rec2` est redondant. De plus, la valeur par défaut pour `int` serait mieux exprimée via un [initialiseur de membre par défaut](#rc-in-class-initializer).

**Voir aussi** : [construire un objet valide](#rc-complete) et [le constructeur lance une exception](#rc-throw).

##### Application

* Signaler les classes avec des opérations de copie utilisateur mais sans constructeur (une copie personnalisée indique généralement que la classe possède une invariante).

### <a name="rc-complete"></a>C.41 : Un constructeur doit créer un objet entièrement initialisé

##### Raison

Un constructeur établit l’invariante d’une classe. Un utilisateur de la classe doit pouvoir supposer qu’un objet construit est exploitable.

##### Exemple, mauvais

    class X1 {
        FILE* f;   // appeler init() avant toute autre fonction
        // …
    public:
        X1() {}
        void init();   // initialise f
        void read();   // lit depuis f
        // …
    };

    void f()
    {
        X1 file;
        file.read();   // plantage ou mauvaise lecture !
        // …
        file.init();   // trop tard
        // …
    }

Les compilateurs ne lisent pas les commentaires.

##### Exception

Si un objet valide ne peut pas être construit commodément via un constructeur, [utiliser une fonction fabrique](#rc-factory).

##### Application

* (Simple) Chaque constructeur doit initialiser chaque membre de données (explicitement, via un appel à un constructeur délégué ou via la construction par défaut).
* (Inconnu) Si un constructeur possède un contrat `Ensures`, essayer de vérifier qu’il tient en post‑condition.

##### Remarque

Si un constructeur acquiert une ressource (pour créer un objet valide), cette ressource doit être [libérée par le destructeur](#rc-dtor-release). L’idiome consistant à acquérir des ressources dans le constructeur et à les libérer dans le destructeur s’appelle [RAII](#rr-raii) (« Resource Acquisition Is Initialization »).

### <a name="rc-throw"></a>C.42 : Si un constructeur ne peut pas construire un objet valide, lever une exception

##### Raison

Laisser derrière soi un objet invalide invite les problèmes.

##### Exemple

    class X2 {
        FILE* f;
        // …
    public:
        X2(const string& name)
            :f{fopen(name.c_str(), "r")}
        {
            if (!f) throw runtime_error{"could not open" + name};
            // …
        }

        void read();      // lire depuis f
        // …
    };

    void f()
    {
        X2 file {"Zeno"}; // lance si le fichier ne s’ouvre pas
        file.read();      // OK
        // …
    }

##### Exemple, mauvais

    class X3 {     // mauvais : le constructeur laisse un objet non‑valide
        FILE* f;   // appeler is_valid() avant toute autre fonction
        bool   valid;
        // …
    public:
        X3(const string& name)
            :f{fopen(name.c_str(), "r")}, valid{false}
        {
            if (f) valid = true;
            // …
        }

        bool is_valid() { return valid; }
        void read();   // lire depuis f
        // …
    };

    void f()
    {
        X3 file {"Heraclides"};
        file.read();   // plantage ou mauvaise lecture !
        // …
        if (file.is_valid()) {
            file.read();
            // …
        }
        else {
            // … gérer l’erreur …
        }
        // …
    }

##### Remarque

Pour une définition de variable (par ex. sur la pile ou comme membre d’un autre objet) il n’y a pas d’appel de fonction explicite depuis lequel on pourrait renvoyer un code d’erreur. Laisser derrière soi un objet invalide et obliger les utilisateurs à toujours appeler `is_valid()` avant usage est fastidieux, source d’erreurs et inefficace.

##### Exception

Il existe des domaines, comme certains systèmes hard‑real‑time (ex. le contrôle d’avion), où la gestion d’exceptions n’est pas suffisamment prévisible en temps (sans outils supplémentaires). Dans ces cas on doit recourir à la technique `is_valid()` ; il faut alors vérifier `is_valid()` systématiquement et immédiatement afin de simuler le [RAII](#rr-raii).

##### Alternative

Si vous êtes tenté d’utiliser une « initialisation post‑constructeur » ou une « initialisation en deux étapes », essayez de ne pas le faire. Si cela s’avère indispensable, examinez les [fonctions fabriques](#rc-factory).

##### Remarque

Une raison pour laquelle les gens utilisaient des fonctions `init()` plutôt que le travail d’initialisation dans le constructeur était d’éviter la duplication de code. Les [constructeurs délégués](#rc-delegating) et les [initialiseurs de membre par défaut](#rc-in-class-initializer) font cela mieux. Une autre raison était de retarder l’initialisation jusqu’à ce que l’objet soit réellement nécessaire ; la solution consiste souvent à ne pas déclarer la variable tant qu’elle ne peut être correctement initialisée (voir [initialisation tardive](#res-init)).

##### Application

???

### <a name="rc-default0"></a>C.43 : S’assurer qu’une classe copiable possède un constructeur par défaut

##### Raison

C’est‑à‑dire, s’assurer que si une classe concrète est copiable elle satisfait aussi le reste du concept « semirégulier ».

De nombreuses fonctions du langage et de la bibliothèque requièrent des constructeurs par défaut pour initialiser leurs éléments, par ex. `T a[10]` et `std::vector<T> v(10)`. Un constructeur par défaut simplifie souvent la tâche de définir un état « déplacé‑from » (voir [???) pour un type qui est aussi copiable.

##### Exemple

    class Date { // MAUVAIS : pas de constructeur par défaut
    public:
        Date(int dd, int mm, int yyyy);
        // …
    };

    vector<Date> vd1(1000);   // besoin d’un Date par défaut ici
    vector<Date> vd2(1000, Date{7, Month::October, 1885});   // alternative

Le constructeur par défaut n’est généré que s’il n’existe aucun constructeur déclaré par l’utilisateur, donc il est impossible d’initialiser le vecteur `vd1` dans l’exemple ci‑dessus. L’absence d’une valeur par défaut peut surprendre les utilisateurs et compliquer son emploi, donc si l’on peut raisonnablement en définir une, il faut le faire.

`Date` a été choisi pour inciter à la réflexion : il n’existe pas de « date par défaut » naturelle (le Big‑Bang est trop lointain pour la plupart des usages). `{0, 0, 0}` n’est pas une date valide dans la plupart des calendriers, ce qui serait l’équivalent du `NaN` des flottants. Cependant, la plupart des implémentations réalistes de `Date` possèdent une « première date » (ex. le 1 janvier 1970 est populaire), ainsi définir cela comme valeur par défaut est habituellement trivial.

    class Date {
    public:
        Date(int dd, int mm, int yyyy);
        Date() = default; // [Voir aussi](#rc-default)
        // …
    private:
        int dd {1};
        int mm {1};
        int yyyy {1970};
        // …
    };

    vector<Date> vd1(1000);

##### Remarque

Une classe dont tous les membres possèdent des constructeurs par défaut obtient implicitement un constructeur par défaut :

    struct X {
        string s;
        vector<int> v;
    };

    X x; // équivaut à X{ { }, { } }; c’est‑à‑dire chaîne vide et vecteur vide

Attention, les types intégrés ne sont pas correctement construits par défaut :

    struct X {
        string s;
        int    i;
    };

    void f()
    {
        X x;    // x.s est initialisé à la chaîne vide ; x.i est non‑initialisé

        cout << x.s << ' ' << x.i << '\n';
        ++x.i;
    }

Les objets statiques de types intégrés sont par défaut initialisés à `0`, mais les variables locales intégrées ne le sont pas. Votre compilateur pourrait initialiser les locales à zéro, mais une compilation optimisée ne le fera pas. Ainsi, le code ci‑dessus peut sembler fonctionner, mais repose sur un comportement indéfini. En supposant que vous vouliez une initialisation, une initialisation explicite peut aider :

    struct X {
        string s;
        int i {};   // initialise (à 0) par défaut
    };

##### Remarques

Les classes qui n’ont pas de construction par défaut raisonnable ne sont généralement pas non plus copiables, donc elles ne tombent pas sous cette directive.

Par exemple, une classe de base ne devrait pas être copiable, et donc n’a pas forcément besoin d’un constructeur par défaut :

    // Shape est une classe abstraite de base, pas un type copiable.
    struct Shape {
        virtual void draw() = 0;
        virtual void rotate(int) = 0;
        // =delete les fonctions copy/move
        // …
    };

Une classe qui doit acquérir une ressource fournie par l’appelant lors de la construction ne peut souvent pas avoir de constructeur par défaut, mais elle ne tombe pas sous cette directive car un tel type n’est généralement pas copiable :

    // std::lock_guard n’est pas copiable.
    lock_guard g {mx};      // protège le mutex mx
    lock_guard g2;         // erreur : rien à protéger

Une classe qui possède un « état spécial » qui doit être traité séparément des autres états par des fonctions membres ou par les utilisateurs implique un travail supplémentaire (et très probablement plus d’erreurs). Un tel type peut naturellement utiliser cet état spécial comme valeur construite par défaut, qu’il soit copiable ou non :

    // std::ofstream n’est pas copiable, mais possède un constructeur par défaut
    // qui correspond à l’état spécial « non ouvert ».
    ofstream out {"Foobar"};
    // …
    out << log(time, transaction);

Des types spéciaux similaires mais **copiables**, comme les pointeurs intelligents copiable qui ont l’état spécial `== nullptr`, devraient utiliser cet état spécial comme valeur construite par défaut.

Il reste toutefois préférable d’avoir un constructeur par défaut qui résulte en un état significatif, tel que `std::string` initialise à `""` et `std::vector` à `{}`.

##### Application

* Signaler les classes qui sont copiable par `=` sans constructeur par défaut.
* Signaler les classes comparables avec `==` mais non copiable.

### <a name="rc-default00"></a>C.44 : Privilégier des constructeurs par défaut simples et non‑excepteurs

##### Raison

Pouvoir attribuer la valeur « défaut » sans opérations susceptibles d’échouer simplifie la gestion des erreurs et le raisonnement sur les opérations de déplacement.

##### Exemple, problématique

    template<typename T>
    // elem pointe vers un élément alloué avec new
    class Vector0 {
    public:
        Vector0() :Vector0{0} {}
        Vector0(int n) :elem{new T[n]}, space{elem + n}, last{elem} {}
        // …
    private:
        own<T*> elem;
        T*      space;
        T*      last;
    };

C’est élégant et général, mais remettre un `Vector0` à vide après une erreur nécessite une allocation, qui peut échouer. De plus, représenter un `Vector0` vide via `{new T[0], 0, 0}` semble gaspilleur ; par ex. `Vector0<int> v[100]` coûte 100 allocations.

##### Exemple

    template<typename T>
    // elem vaut nullptr ou pointe vers un élément alloué avec new
    class Vector1 {
    public:
        // initialise à {nullptr, nullptr, nullptr} ; ne lance pas d’exception
        Vector1() noexcept {}
        Vector1(int n) :elem{new T[n]}, space{elem + n}, last{elem} {}
        // …
    private:
        own<T*> elem {};
        T*      space {};
        T*      last {};
    };

Utiliser `{nullptr, nullptr, nullptr}` rend `Vector1{}` peu coûteux, mais impose un cas spécial et implique des vérifications à l’exécution. Remettre un `Vector1` à vide après une erreur devient trivial.

##### Application

* Signaler les constructeurs par défaut qui lancent des exceptions.

### <a name="rc-default"></a>C.45 : Ne pas définir de constructeur par défaut ne faisant qu’initialiser les membres ; utiliser les initialiseurs de membres par défaut

##### Raison

Utiliser les initialiseurs de membres par défaut permet au compilateur de générer la fonction pour vous. Le compilateur‑généré peut être plus efficace.

##### Exemple, mauvais

    class X1 { // MAUVAIS : ne pas utiliser les initialiseurs de membres
        string s;
        int    i;
    public:
        X1() :s{"default"}, i{1} { }
        // …
    };

##### Exemple

    class X2 {
        string s {"default"};
        int    i {1};
    public:
        // utiliser le constructeur par défaut généré par le compilateur
        // …
    };

##### Application

(Simple) Signaler si un constructeur par défaut possède un initialiseur de membre constant, et recommander de le placer comme initialiseur de membre de données à la place.

### <a name="rc-explicit"></a>C.46 : Déclarer `explicit` les constructeurs à un seul argument par défaut

##### Raison

Éviter les conversions implicites inattendues.

##### Exemple, mauvais

    class String {
    public:
        String(int);   // MAUVAIS
        // …
    };

    String s = 10;   // surprise : chaîne de taille 10

##### Exception

Si vous voulez réellement une conversion implicite du type d’argument du constructeur vers le type de la classe, n’utilisez pas `explicit` :

    class Complex {
    public:
        Complex(double d);   // OK : on veut une conversion de d vers {d, 0}
        // …
    };

    Complex z = 10.7;   // conversion attendue

**Voir aussi** : [Discussion des conversions implicites](#ro-conversion)

##### Remarque

Les constructeurs de copie et de déplacement ne doivent pas être `explicit` car ils ne réalisent pas de conversion. Rendre explicite un constructeur de copie/déplacement complique le passage et le retour par valeur.

##### Application

(Simple) Les constructeurs à un seul argument doivent être déclarés `explicit`. Les bons constructeurs à un seul argument non‑`explicit` sont rares dans la plupart des bases de code. Avertir pour tous ceux qui ne figurent pas sur une « liste positive ».

### <a name="rc-order"></a>C.47 : Définir et initialiser les membres de données dans l’ordre de leur déclaration

##### Raison

Minimiser la confusion et les erreurs. C’est l’ordre réel d’initialisation (indépendamment de l’ordre des initialiseurs de membres).

##### Exemple, mauvais

    class Foo {
        int m1;
        int m2;
    public:
        Foo(int x) :m2{x}, m1{++x} { }   // MAUVAIS : ordre d’initialisation trompeur
        // …
    };

    Foo x(1); // surprise : x.m1 == x.m2 == 2

##### Application

(Simple) La liste d’initialisation d’un constructeur doit mentionner les membres dans le même ordre que leur déclaration.

**Voir aussi** : [Discussion](#sd-order)

### <a name="rc-in-class-initializer"></a>C.48 : Privilégier les initialiseurs de membres par défaut aux initialiseurs de membres dans les constructeurs pour les initialiseurs constants

##### Raison

Rendre explicite que la même valeur doit être utilisée dans tous les constructeurs. Éviter la répétition. Éviter les problèmes de maintenance. Conduire au code le plus court et le plus efficace.

##### Exemple, mauvais

    class X {   // MAUVAIS
        int i;
        string s;
        int j;
    public:
        X() :i{666}, s{"qqq"} { }   // j non initialisé
        X(int ii) :i{ii} {}         // s vaut "" et j non initialisé
        // …
    };

Comment un mainteneur saurait‑il si `j` était volontairement non‑initialisé (probablement mauvais) et si `s` devait être `""` dans un cas et `qqq` dans l’autre (presque certainement un bug) ? Le problème d’oubli d’initialiser `j` survient souvent lorsqu’on ajoute un nouveau membre à une classe existante.

##### Exemple

    class X2 {
        int i {666};
        string s {"qqq"};
        int j {numeric_limits<int>::min()};
    public:
        X2() = default;        // tous les membres sont initialisés à leurs valeurs par défaut
        X2(int ii) :i{ii} {}   // s et j initialization aux valeurs par défaut
        // …
    };

**Alternative** : on peut obtenir une partie des bénéfices grâce aux arguments par défaut des constructeurs, ce qui n’est pas rare dans le code ancien. Cependant, cela est moins explicite, entraîne plus de paramètres à passer, et devient répétitif lorsqu’il y a plus d’un constructeur :

    class X3 {   // MAUVAIS : non explicite, surcharge de passage d’arguments
        int i;
        string s;
        int j;
    public:
        X3(int ii = 666, const string& ss = "qqq", int jj = numeric_limits<int>::min())
            :i{ii}, s{ss}, j{jj} { }   // tous les membres sont initialisés à leurs valeurs par défaut
        // …
    };

##### Application

* (Simple) Chaque constructeur doit initialiser chaque membre de données (explicitement, via appel à un constructeur délégué ou via construction par défaut).
* (Simple) Les arguments par défaut des constructeurs suggèrent qu’un initialiseur de membre par défaut serait plus approprié.

### <a name="rc-initialize"></a>C.49 : Privilégier l’initialisation à l’affectation dans les constructeurs

##### Raison

Une initialisation indique explicitement que l’on initialise, plutôt qu’on assigne, ce qui peut être plus élégant et plus efficace. Cela évite les erreurs « utiliser avant de définir ».

##### Exemple, bon

    class A {   // Bon
        string s1;
    public:
        A(czstring p) : s1{p} { }    // BON : construire directement (et le C‑string est nommé explicitement)
        // …
    };

##### Exemple, mauvais

    class B {   // MAUVAIS
        string s1;
    public:
        B(const char* p) { s1 = p; }   // MAUVAIS : constructeur par défaut puis assignation
        // …
    };

    class C {   // AFFREUX, aka très mauvais
        int* p;
    public:
        C() { cout << *p; p = new int{10}; }   // utilisation accidentelle avant l’initialisation
        // …
    };

##### Exemple, encore mieux

Au lieu d’utiliser ces `const char*`, on pourrait se servir du `std::string_view` (C++17) ou de `gsl::span<char>` comme [une façon plus générale de présenter les arguments à une fonction](#rstr-view) :

    class D {   // Bon
        string s1;
    public:
        D(string_view v) : s1{v} { }    // BON : construire directement
        // …
    };

### <a name="rc-factory"></a>C.50 : Utiliser une fonction‑fabrique si vous avez besoin d’un « comportement virtuel » lors de l’initialisation

##### Raison

Si l’état d’un objet de base doit dépendre de l’état d’une partie dérivée de l’objet, nous devons utiliser une fonction virtuelle (ou équivalente) tout en minimisant la fenêtre d’opportunité où un objet mal construit peut être mal utilisé.

##### Remarque

Le type de retour de la fabrique doit normalement être `unique_ptr` par défaut ; si certains usages sont partagés, l’appelant peut `move` le `unique_ptr` vers un `shared_ptr`. Cependant, si le créateur de la fabrique sait que tous les usages de l’objet retourné seront partagés, retourner `shared_ptr` et employer `make_shared` dans le corps économise une allocation.

##### Exemple, mauvais

    class B {
    public:
        B()
        {
            /* … */
            f(); // MAUVAIS : C.82 : ne pas appeler de fonctions virtuelles dans les constructeurs et destructeurs
            /* … */
        }

        virtual void f() = 0;
    };

##### Exemple

    class B {
    protected:
        class Token {};

    public:
        explicit B(Token) { /* … */ }  // créer un objet imparfaitement initialisé
        virtual void f() = 0;

        template<class T>
        static shared_ptr<T> create()    // interface pour créer des objets partagés
        {
            auto p = make_shared<T>(typename T::Token{});
            p->post_initialize();
            return p;
        }

    protected:
        virtual void post_initialize()   // appelé juste après la construction
            { /* … */ f(); /* … */ } // BON : la distribution virtuelle est sûre
    };

    class D : public B {                 // classe dérivée
    protected:
        class Token {};

    public:
        explicit D(Token) : B{ B::Token{} } {}
        void f() override { /* … */ };

    protected:
        template<class T>
        friend shared_ptr<T> B::create();
    };

    shared_ptr<D> p = D::create<D>();  // création d’un D

`make_shared` requiert que le constructeur soit public. En exigeant un `Token` protégé, le constructeur ne peut plus être appelé publiquement, évitant ainsi qu’un objet imparfait s’échappe. En fournissant la fonction‑fabrique `create()`, on rend la construction (sur le tas) commode.

##### Remarque

Les fonctions‑fabriques conventionnelles allouent sur le tas plutôt que sur la pile ou dans un objet englobant.

**Voir aussi** : [Discussion](#sd-factory)

### <a name="rc-delegating"></a>C.51 : Utiliser les constructeurs délégués pour représenter les actions communes à tous les constructeurs d’une classe

##### Raison

Éviter la répétition et les différences accidentelles.

##### Exemple, mauvais

    class Date {   // MAUVAIS : répétitif
        int d;
        Month m;
        int y;
    public:
        Date(int dd, Month mm, year yy)
            :d{dd}, m{mm}, y{yy}
            { if (!valid(d, m, y)) throw Bad_date{}; }

        Date(int dd, Month mm)
            :d{dd}, m{mm} y{current_year()}
            { if (!valid(d, m, y)) throw Bad_date{}; }
        // …
    };

L’action commune devient fastidieuse à écrire et peut accidentellement ne pas être commune.

##### Exemple

    class Date2 {
        int d;
        Month m;
        int y;
    public:
        Date2(int dd, Month mm, year yy)
            :d{dd}, m{mm}, y{yy}
            { if (!valid(d, m, y)) throw Bad_date{}; }

        Date2(int dd, Month mm)
            :Date2{dd, mm, current_year()} {}
        // …
    };

**Voir aussi** : Si l’« action répétitive » est une simple initialisation, considérer [un initialiseur de membre par défaut](#rc-in-class-initializer).

##### Application

(Modérée) Rechercher des corps de constructeurs similaires.

### <a name="rc-inheriting"></a>C.52 : Utiliser les constructeurs hérité pour importer les constructeurs dans une classe dérivée qui n’a pas besoin d’une initialisation explicite supplémentaire

##### Raison

Si vous avez besoin de ces constructeurs pour une classe dérivée, les ré‑implémenter est fastidieux et sujet aux erreurs.

##### Exemple

`std::vector` possède de nombreux constructeurs subtils, donc si je veux mon propre `vector`, je ne veux pas les ré‑implémenter :

    class Rec {
        // … données et nombreux bons constructeurs …
    };

    class Oper : public Rec {
        using Rec::Rec;
        // … pas de membres de données …
        // … nombreuses fonctions utilitaires …
    };

##### Exemple, mauvais

    struct Rec2 : public Rec {
        int x;
        using Rec::Rec;
    };

    Rec2 r {"foo", 7};
    int val = r.x;   // non initialisé

##### Application

S’assurer que chaque membre de la classe dérivée est correctement initialisé.

## <a name="ss-copy"></a>C.copy : Copie et déplacement

Les types concrets devraient généralement être copiable, mais les interfaces dans une hiérarchie de classes ne le devraient pas. Les gestionnaires de ressources peuvent ou non être copiable. Les types peuvent être définis comme déplaçables pour des raisons logiques ainsi que de performance.

### <a name="rc-copy-assignment"></a>C.60 : Rendre l’assignation par copie non‑`virtual`, prendre le paramètre par `const&`, et retourner par `non‑const&`

##### Raison

Simple et efficace. Si vous voulez optimiser pour les r‑values, fournissez une surcharge qui prend un `&&` (voir [F.18](#rf-consume)).

##### Exemple

    class Foo {
    public:
        Foo& operator=(const Foo& x)
        {
            // BON : pas besoin de vérifier l’auto‑assignation (autre que la performance)
            auto tmp = x;
            swap(tmp); // voir C.83
            return *this;
        }
        // …
    };

    Foo a;
    Foo b;
    Foo f();

    a = b;    // assignation lvalue : copie
    a = f();  // assignation rvalue : potentiellement déplacement

##### Remarque

La technique d’implémentation `swap` offre la [garantie forte](#Abrahams01).

##### Exemple

Mais si vous pouvez obtenir des performances nettement meilleures en n’effectuant pas de copie temporaire ? Considérons un `Vector` simple dont l’assignation de grands vecteurs de même taille est courante. Dans ce cas, copier les éléments implémenté par la technique `swap` pourrait coûter un facteur d’ordre de grandeur de plus :

    template<typename T>
    class Vector {
    public:
        Vector& operator=(const Vector&);
        // …
    private:
        T* elem;
        int sz;
    };

    Vector& Vector::operator=(const Vector& a)
    {
        if (a.sz > sz) {
            // … utiliser la technique swap, cela ne peut pas être amélioré …
            return *this;
        }
        // … copier sz éléments de *a.elem vers elem …
        if (a.sz < sz) {
            // … détruire les éléments superflus dans *this et ajuster la taille …
        }
        return *this;
    }

En écrivant directement dans les éléments cibles, on obtient seulement la [garantie de base](#Abrahams01) plutôt que la garantie forte offerte par la technique `swap`. Attention à l’[auto‑assignation](#rc-copy-self).

**Alternatives** : Si vous pensez avoir besoin d’un opérateur d’assignation `virtual` et comprenez pourquoi c’est profondément problématique, ne l’appelez pas `operator=`. Faites‑en une fonction nommée comme `virtual void assign(const Foo&)`. Voir [constructeur de copie vs. `clone()`](#rc-copy-virtual).

##### Application

* (Simple) Un opérateur d’assignation ne doit pas être `virtual`. « Here be dragons ! »
* (Simple) Un opérateur d’assignation doit retourner `T&` pour permettre l’enchaînement, et non des alternatives comme `const T&` qui interféreraient avec la composabilité et l’insertion d’objets dans des conteneurs.
* (Modérée) Un opérateur d’assignation doit (implicitement ou explicitement) invoquer tous les opérateurs d’assignation des bases et des membres. Examiner le destructeur pour déterminer si le type a une sémantique de pointeur ou de valeur.

### <a name="rc-copy-semantic"></a>C.61 : Une opération de copie doit copier

##### Raison

C’est la sémantique généralement attendue. Après `x = y`, on doit avoir `x == y`. Après une copie, `x` et `y` peuvent être des objets indépendants (sémantique de valeur, comme les types intégrés non‑pointeurs et les types de la bibliothèque standard) ou référencer un même objet (sémantique de pointeur, comme les pointeurs).

##### Exemple

    class X {   // OK : sémantique de valeur
    public:
        X();
        X(const X&);     // copier X
        void modify();   // changer la valeur de X
        // …
        ~X() { delete[] p; }
    private:
        T* p;
        int sz;
    };

    bool operator==(const X& a, const X& b)
    {
        return a.sz == b.sz && equal(a.p, a.p + a.sz, b.p, b.p + b.sz);
    }

    X::X(const X& a)
        :p{new T[a.sz]}, sz{a.sz}
    {
        copy(a.p, a.p + sz, p);
    }

    X x;
    X y = x;
    if (x != y) throw Bad{};
    x.modify();
    if (x == y) throw Bad{};   // supposons la sémantique de valeur

##### Exemple

    class X2 {  // OK : sémantique de pointeur
    public:
        X2();
        X2(const X2&) = default; // copie superficielle
        ~X2() = default;
        void modify();          // changer la valeur pointée
        // …
    private:
        T* p;
        int sz;
    };

    bool operator==(const X2& a, const X2& b)
    {
        return a.sz == b.sz && a.p == b.p;
    }

    X2 x;
    X2 y = x;
    if (x != y) throw Bad{};
    x.modify();
    if (x != y) throw Bad{};  // sémantique de pointeur

##### Remarque

Privilégier la sémantique de valeur sauf si vous construisez un « smart pointer ». La sémantique de valeur est la plus simple à raisonner et ce que les facilités de la bibliothèque standard attendent.

##### Application

(N’est pas enforceable)

### <a name="rc-copy-self"></a>C.62 : Rendre l’assignation par copie sûre pour l’auto‑assignation

##### Raison

Si `x = x` modifie la valeur de `x`, les gens seront surpris et des erreurs graves peuvent survenir (souvent des fuites).

##### Exemple

Les conteneurs de la bibliothèque standard gèrent l’auto‑assignation de façon élégante et efficace :

    std::vector<int> v = {3, 1, 4, 1, 5, 9};
    v = v;
    // la valeur de v reste {3, 1, 4, 1, 5, 9}

##### Remarque

L’assignation générée par défaut à partir de membres qui gèrent l’auto‑assignation fonctionne correctement.

    struct Bar {
        vector<pair<int, int>> v;
        map<string, int> m;
        string s;
    };

    Bar b;
    // …
    b = b;   // correct et efficace

##### Remarque

Vous pouvez gérer l’auto‑assignation en testant explicitement, mais souvent il est plus rapide et plus élégant de s’en passer (par ex. en utilisant `swap`).

    class Foo {
        string s;
        int    i;
    public:
        Foo& operator=(const Foo& a);
        // …
    };

    Foo& Foo::operator=(const Foo& a)   // OK, mais il y a un coût
    {
        if (this == &a) return *this;
        s = a.s;
        i = a.i;
        return *this;
    }

C’est évidemment sûr et apparemment efficace. Cependant, si on fait une auto‑assignation sur un million d’assignations, on effectue un million de tests redondants (mais le prédicteur de branche du processeur devine presque toujours correctement). Considérez :

    Foo& Foo::operator=(const Foo& a)   // plus simple, et probablement bien meilleur
    {
        s = a.s;
        i = a.i;
        return *this;
    }

`std::string` gère l’auto‑assignation, tout comme `int`. Tout le coût est donc supporté par le cas rare d’auto‑assignation.

##### Application

(Simple) Les opérateurs d’assignation ne devraient pas contenir le motif `if (this == &a) return *this;` ???

### <a name="rc-move-assignment"></a>C.63 : Rendre l’assignation par déplacement non‑`virtual`, prendre le paramètre par `&&`, et retourner par `non‑const&`

##### Raison

Simple et efficace.

**Voir** : [la règle pour l’assignation par copie](#rc-copy-assignment).

##### Application

Équivalent à ce qui est fait pour [l’assignation par copie](#rc-copy-assignment).

* (Simple) Un opérateur d’assignation ne doit pas être `virtual`. « Here be dragons ! »
* (Simple) Un opérateur d’assignation doit retourner `T&` pour permettre l’enchaînement, et non des alternatives comme `const T&` qui interfèrent avec la composabilité et l’insertion d’objets dans des conteneurs.
* (Modérée) Un opérateur d’assignation de déplacement doit (implicitement ou explicitement) invoquer tous les opérateurs d’assignation de déplacement des bases et des membres.

### <a name="rc-move-semantic"></a>C.64 : Une opération de déplacement doit déplacer et laisser sa source dans un état valide

##### Raison

C’est la sémantique généralement attendue. Après `y = std::move(x)` la valeur de `y` doit être la valeur que `x` avait, et `x` doit être dans un état valide.

##### Exemple

    class X {   // OK : sémantique de valeur
    public:
        X();
        X(X&& a) noexcept;  // déplacer X
        X& operator=(X&& a) noexcept; // assignation par déplacement
        void modify();     // changer la valeur de X
        // …
        ~X() { delete[] p; }
    private:
        T* p;
        int sz;
    };

    X::X(X&& a) noexcept
        :p{a.p}, sz{a.sz}  // voler la représentation
    {
        a.p = nullptr;     // mettre à « vide »
        a.sz = 0;
    }

    void use()
    {
        X x{};
        // …
        X y = std::move(x);
        x = X{};   // OK
    } // OK : x peut être détruit

##### Remarque

Idéalement, l’état déplacé devrait être la valeur par défaut du type. Assurez‑vous que, sauf raison exceptionnelle, c’est le cas. Cependant, tous les types n’ont pas de valeur par défaut et, pour certains, établir la valeur par défaut peut être coûteux. La norme exige seulement que l’objet déplacé puisse être détruit. Souvent, on peut faire mieux : la bibliothèque standard suppose qu’on peut assigner à un objet déplacé. Toujours laisser l’objet déplacé dans un état valide (nécessairement spécifié).

##### Remarque

À moins d’une raison exceptionnelle, rendre `x = std::move(y); y = z;` fonctionnel avec les sémantiques usuelles.

##### Application

(N’est pas enforceable) Rechercher les assignations aux membres dans l’opération de déplacement. Si le type possède un constructeur par défaut, comparer ces assignations aux initialisations du constructeur par défaut.

### <a name="rc-move-self"></a>C.65 : Rendre l’assignation par déplacement sûre pour l’auto‑assignation

##### Raison

Si `x = x` change la valeur de `x`, les gens seront surpris et des erreurs graves peuvent survenir. Cependant, on n’écrit généralement pas directement `x = x` comme déplacement, mais cela peut arriver. De plus, `std::swap` est implémenté à l’aide d’opérations de déplacement, donc si vous faites accidentellement `swap(a, b)` où `a` et `b` référencent le même objet, ne pas gérer l’auto‑déplacement peut être une erreur subtile.

##### Exemple

    class Foo {
        string s;
        int    i;
    public:
        Foo& operator=(Foo&& a) noexcept;
        // …
    };

    Foo& Foo::operator=(Foo&& a) noexcept  // OK, mais il y a un coût
    {
        if (this == &a) return *this;  // cette ligne est redondante
        s = std::move(a.s);
        i = a.i;
        return *this;
    }

Le débat sur le test `if (this == &a) return *this;` (voir la discussion de [self‑assignment](#rc-copy-self)) est encore plus pertinent pour le déplacement auto‑déplacement.

##### Remarque

Il n’existe pas de méthode générale connue pour éviter le test `if (this == &a) return *this;` dans une assignation par déplacement tout en obtenant un résultat correct (c’est‑à‑dire que `x = x` laisse `x` inchangé).

##### Remarque

La norme garantit uniquement un état « valide mais non spécifié » pour les conteneurs de la bibliothèque standard. Apparentement, cela n’a pas posé de problème pendant environ 10 ans d’usage expérimental et en production. Contactez les éditeurs si vous trouvez un contre‑exemple. Cette règle impose plus de prudence et insiste sur la sécurité totale.

##### Exemple

Voici une façon de déplacer un pointeur sans test (imaginez le comme code d’une assignation par déplacement) :

    // déplacer other.ptr vers this->ptr
    T* temp = other.ptr;
    other.ptr = nullptr;
    delete ptr; // en auto‑déplacement, this->ptr est également nul ; delete est un no‑op
    ptr = temp; // en auto‑déplacement, le pointeur original est restauré

##### Application

* (Modérée) En cas d’auto‑assignation, un opérateur d’assignation de déplacement ne doit pas laisser l’objet avec des membres pointeur qui ont été `delete`d ou mis à `nullptr`.
* (Non enforceable) Regarder les types de conteneur de la bibliothèque standard (incl. `string`) et les considérer sûrs pour les usages ordinaires (non critiques).

### <a name="rc-move-noexcept"></a>C.66 : Rendre les opérations de déplacement `noexcept`

##### Raison

Un déplacement qui lance empêche la plupart des hypothèses raisonnables. Un déplacement non‑lanceur sera utilisé plus efficacement par les facilités du langage et de la bibliothèque.

##### Exemple

    template<typename T>
    class Vector {
    public:
        Vector(Vector&& a) noexcept :elem{a.elem}, sz{a.sz} { a.elem = nullptr; a.sz = 0; }
        Vector& operator=(Vector&& a) noexcept {
            if (&a != this) {
                delete elem;
                elem = a.elem; a.elem = nullptr;
                sz   = a.sz;   a.sz   = 0;
            }
            return *this;
        }
        // …
    private:
        T* elem;
        int sz;
    };

Ces opérations ne lancent pas d’exception.

##### Exemple, mauvais

    template<typename T>
    class Vector2 {
    public:
        Vector2(Vector2&& a) noexcept { *this = a; }             // juste utiliser la copie
        Vector2& operator=(Vector2&& a) noexcept { *this = a; }  // juste utiliser la copie
        // …
    private:
        T* elem;
        int sz;
    };

`Vector2` n’est pas seulement inefficace, mais comme une copie de vecteur nécessite une allocation, elle peut lancer.

##### Application

(Simple) Une opération de déplacement doit être marquée `noexcept`.

### <a name="rc-copy-virtual"></a>C.67 : Une classe polymorphe doit supprimer la copie/déplacement publique

##### Raison

Une *classe polymorphe* est une classe qui définit ou hérite au moins d’une fonction virtuelle. Il est probable qu’elle sera utilisée comme classe de base pour d’autres classes dérivées avec comportement polymorphe. Si elle est accidentellement passée par valeur, avec le constructeur de copie et l’opérateur d’assignation générés implicitement, on risque le **slicing** : seule la partie base d’un objet dérivé sera copiée, corrompant le comportement polymorphe.

Si la classe n’a pas de données, `=delete` les fonctions de copie/déplacement. Sinon, les rendre `protected`.

##### Exemple, mauvais

    class B { // MAUVAIS : classe de base polymorphe qui ne supprime pas la copie
    public:
        virtual char m() { return 'B'; }
        // … rien concernant les opérations de copie, donc les défauts sont utilisés …
    };

    class D : public B {
    public:
        char m() override { return 'D'; }
        // …
    };

    void f(B& b)
    {
        auto b2 = b; // oups, slice l’objet ; b2.m() renverra 'B'
    }

    D d;
    f(d);

##### Exemple

    class B { // BON : classe polymorphe qui supprime la copie
    public:
        B() = default;
        B(const B&) = delete;
        B& operator=(const B&) = delete;
        virtual char m() { return 'B'; }
        // …
    };

    class D : public B {
    public:
        char m() override { return 'D'; }
        // …
    };

    void f(B& b)
    {
        auto b2 = b; // ok, le compilateur détectera la tentative de copie et protestera
    }

    D d;
    f(d);

##### Remarque

Si vous avez besoin de créer des copies profondes d’objets polymorphes, utilisez des fonctions `clone()` : voir [C.130](#rh-copy).

##### Exception

Les classes qui représentent des objets d’exception doivent être à la fois polymorphes et **copiable‑constructibles**.

##### Application

* Signaler une classe polymorphe avec une opération de copie publique.
* Signaler une assignation d’objets de classe polymorphe.

## C.other : Autres règles d’opérations par défaut

En plus des opérations pour lesquelles le langage offre des implémentations par défaut, quelques opérations sont si fondamentales qu’il faut des règles spécifiques : comparaisons, `swap` et `hash`.

### <a name="rc-eqdefault"></a>C.80 : Utiliser `=default` si vous devez être explicite sur l’usage des sémantiques par défaut

##### Raison

Le compilateur a plus de chances de bien obtenir les sémantiques par défaut et vous ne pouvez pas implémenter ces fonctions mieux que le compilateur.

##### Exemple

    class Tracer {
        string message;
    public:
        Tracer(const string& m) : message{m} { cerr << "entering " << message << '\n'; }
        ~Tracer() { cerr << "exiting " << message << '\n'; }

        Tracer(const Tracer&) = default;
        Tracer& operator=(const Tracer&) = default;
        Tracer(Tracer&&) noexcept = default;
        Tracer& operator=(Tracer&&) noexcept = default;
    };

Parce que nous avons défini le destructeur, nous devons définir les opérations de copie et de déplacement. `= default` est le moyen le plus simple et le meilleur de le faire.

##### Exemple, mauvais

    class Tracer2 {
        string message;
    public:
        Tracer2(const string& m) : message{m} { cerr << "entering " << message << '\n'; }
        ~Tracer2() { cerr << "exiting " << message << '\n'; }

        Tracer2(const Tracer2& a) : message{a.message} {}
        Tracer2& operator=(const Tracer2& a) { message = a.message; return *this; }
        Tracer2(Tracer2&& a) noexcept :message{a.message} {}
        Tracer2& operator=(Tracer2&& a) noexcept { message = a.message; return *this; }
    };

Écrire les corps des opérations de copie/déplacement est verbeux, fastidieux et source d’erreurs. Un compilateur le fait mieux.

##### Application

(Moderate) Le corps d’une fonction définie par l’utilisateur ne doit pas reproduire la même sémantique que la version générée par le compilateur, car ce serait redondant.

### <a name="rc-delete"></a>C.81 : Utiliser `=delete` quand vous voulez désactiver le comportement par défaut (sans vouloir d’alternative)

##### Raison

Dans quelques cas, une opération par défaut n’est pas désirable.

##### Exemple

    class Immortal {
    public:
        ~Immortal() = delete;   // ne pas autoriser la destruction
        // …
    };

    void use()
    {
        Immortal ugh;   // erreur : ugh ne peut pas être détruit
        Immortal* p = new Immortal{};
        delete p;       // erreur : impossible de détruire *p
    }

##### Exemple

Un `unique_ptr` peut être déplacé, mais pas copié. Pour cela, ses opérations de copie sont supprimées. Pour éviter la copie on doit `=delete` les fonctions de copie des l‑values :

    template<class T, class D = default_delete<T>> class unique_ptr {
    public:
        // …
        constexpr unique_ptr() noexcept;
        explicit unique_ptr(pointer p) noexcept;
        // …
        unique_ptr(unique_ptr&& u) noexcept;   // constructeur de déplacement
        // …
        unique_ptr(const unique_ptr&) = delete; // désactiver la copie depuis l‑value
        // …
    };

    unique_ptr<int> make();   // fabriquer « quelque chose » et le retourner par déplacement

    void f()
    {
        unique_ptr<int> pi {};
        auto pi2 {pi};      // erreur : aucune construction de déplacement depuis l‑value
        auto pi3 {make()}; // OK, déplacement : le résultat de make() est une r‑value
    }

Notez que les fonctions `=delete` doivent être publiques.

##### Application

L’élimination d’une opération par défaut (ou d’une fonction) dépend de la sémantique désirée de la classe. Considérez ces classes comme suspectes, mais maintenez une « liste positive » de classes où un humain a attesté que la sémantique est correcte.

### <a name="rc-ctor-virtual"></a>C.82 : Ne pas appeler de fonctions virtuelles dans les constructeurs et destructeurs

##### Raison

La fonction appelée sera celle de l’objet construit jusqu’alors, et non pas forcément celle de la classe dérivée. Cela peut être très déroutant. Pire, un appel direct ou indirect à une fonction pure virtuelle non implémentée depuis un constructeur ou un destructeur entraîne un comportement indéfini.

##### Exemple, mauvais

    class Base {
    public:
        virtual void f() = 0;   // non implémentée
        virtual void g();       // implémentée avec la version Base
        virtual void h();       // implémentée avec la version Base
        virtual ~Base();        // implémentée avec la version Base
    };

    class Derived : public Base {
    public:
        void g() override;   // fournir l’implémentation Derived
        void h() final;      // fournir l’implémentation Derived

        Derived()
        {
            // MAUVAIS : tentative d’appeler une fonction virtuelle non implémentée
            f();

            // MAUVAIS : appellera Derived::g, pas de dispatch supplémentaire virtuel
            g();

            // BON : spécifier explicitement l’intention d’appeler uniquement la version visible
            Derived::g();

            // ok, pas de qualification nécessaire, h est final
            h();
        }
    };

Notez qu’appeler une fonction explicitement qualifiée n’est pas un appel virtuel même si la fonction est `virtual`.

**Voir aussi** : [fonctions fabriques](#rc-factory) pour obtenir le même effet qu’un appel à une fonction dérivée sans risque de comportement indéfini.

##### Remarque

Il n’y a rien d’intrinsèquement mauvais à appeler des fonctions virtuelles depuis les constructeurs et destructeurs. La sémantique de tels appels est sûre du point de vue du typage. Cependant, l’expérience montre que ces appels sont rarement nécessaires, ils confondent facilement les mainteneurs et deviennent une source d’erreurs chez les novices.

##### Application

* Signaler les appels à des fonctions virtuelles depuis les constructeurs et destructeurs.

### <a name="rc-swap"></a>C.83 : Pour les types à valeur, envisager de fournir une fonction `swap` `noexcept`

##### Raison

`swap` peut être pratique pour implémenter un certain nombre d’idiomes, du déplacement d’objets à l’implémentation d’une assignation facile, en passant par une fonction de validation d’erreur forte. Considérez l’utilisation de `swap` pour implémenter l’assignation par copie en termes de construction par copie. Voir aussi [destructeurs, désallocation et `swap` ne doivent jamais échouer](#re-never-fail).

##### Exemple, bon

    class Foo {
    public:
        void swap(Foo& rhs) noexcept
        {
            m1.swap(rhs.m1);
            std::swap(m2, rhs.m2);
        }
    private:
        Bar m1;
        int m2;
    };

Fournir une fonction `swap` non‑membre dans le même espace de noms que votre type pour la commodité des appelants.

    void swap(Foo& a, Foo& b)
    {
        a.swap(b);
    }

##### Application

* Les types non trivially copiable devraient fournir un `swap` membre ou une surcharge de `swap` libre.
* (Simple) Quand une classe possède une fonction `swap` membre, elle doit être déclarée `noexcept`.

### <a name="rc-swap-fail"></a>C.84 : Un `swap` ne doit pas échouer

##### Raison

`swap` est largement utilisé dans des contextes qui supposent qu’il ne peut jamais échouer, et les programmes ne peuvent pas facilement être écrits pour fonctionner correctement en présence d’un `swap` qui échoue. Les conteneurs et algorithmes du standard ne fonctionneront pas correctement si l’échange d’un type d’élément échoue.

##### Exemple, mauvais

    void swap(My_vector& x, My_vector& y)
    {
        auto tmp = x;   // copier les éléments
        x = y;
        y = tmp;
    }

Ce n’est pas seulement lent, mais si une allocation de mémoire a lieu pour les éléments de `tmp`, ce `swap` pourrait lancer une exception et les algorithmes STL qui l’utilisent échoueraient.

##### Application

(Simple) Quand une classe possède une fonction `swap` membre, elle doit être déclarée `noexcept`.

### <a name="rc-swap-noexcept"></a>C.85 : Marquer `swap` `noexcept`

##### Raison

[Un `swap` ne doit pas échouer](#rc-swap-fail). Si un `swap` tente de sortir avec une exception, c’est une mauvaise conception et le programme devrait idéalement se terminer.

##### Application

(Simple) Quand une classe possède une fonction `swap` membre, elle doit être déclarée `noexcept`.

### <a name="rc-eq"></a>C.86 : Rendre `==` symétrique par rapport aux types d’opérandes et `noexcept`

##### Raison

Un traitement asymétrique des opérandes est surprenant et source d’erreurs lorsque des conversions sont possibles. `==` est une opération fondamentale ; les programmeurs devraient pouvoir l’utiliser sans craindre d’échec.

##### Exemple

    struct X {
        string name;
        int    number;
    };

    bool operator==(const X& a, const X& b) noexcept {
        return a.name == b.name && a.number == b.number;
    }

##### Exemple, mauvais

    class B {
        string name;
        int    number;
        bool operator==(const B& a) const {
            return name == a.name && number == a.number;
        }
        // …
    };

La comparaison de `B` accepte les conversions pour son second opérande, mais pas pour le premier.

##### Remarque

Si une classe possède un état d’échec, comme le `NaN` de `double`, il peut être tentant de faire lancer une comparaison contre l’état d’échec. L’alternative est de faire en sorte que les deux états d’échec soient égaux et que tout état valide compare à `false` contre l’état d’échec.

##### Remarque

Cette règle s’applique à tous les opérateurs de comparaison habituels : `!=`, `<`, `<=`, `>`, `>=`.

##### Application

* Signaler tout `operator==()` dont les types d’argument diffèrent ; idem pour les autres opérateurs de comparaison (`!=`, `<`, `<=`, `>`, `>=`).
* Signaler les opérateurs `operator==()` membres ; idem pour les autres opérateurs de comparaison.

### <a name="rc-eq-base"></a>C.87 : Méfiez‑vous de `==` sur les classes de base

##### Raison

Il est vraiment difficile d’écrire un `==` fiable et utile pour une hiérarchie.

##### Exemple, mauvais

    class B {
        string name;
        int    number;
    public:
        virtual bool operator==(const B& a) const
        {
            return name == a.name && number == a.number;
        }
        // …
    };

    class D : public B {
        char character;
    public:
        virtual bool operator==(const D& a) const
        {
            return B::operator==(a) && character == a.character;
        }
        // …
    };

    B b = ...;
    D d = ...;
    b == d;    // compare name et number, ignore le caractère de d
    d == b;    // même chose
    D d2;
    d == d2;   // compare name, number, character
    B& b2 = d2;
    b2 == d;   // compare name and number, ignore character de d2 et de d

Il existe évidemment des moyens de faire fonctionner `==` dans une hiérarchie, mais les approches naïves ne s’échelonnent pas.

##### Remarque

Cette règle s’applique à tous les opérateurs de comparaison usuels : `!=`, `<`, `<=`, `>`, `>=`, et `<=>`.

##### Application

* Signaler un `operator==()` virtuel ; idem pour les autres opérateurs de comparaison.

### <a name="rc-hash"></a>C.89 : Rendre un `hash` `noexcept`

##### Raison

Les utilisateurs de conteneurs hachés utilisent le hachage indirectement et ne s’attendent pas à ce qu’un simple accès lance une exception. C’est une exigence de la bibliothèque standard.

##### Exemple, mauvais

    template<>
    struct hash<My_type> {  // spécialisation de hash totalement mauvaise
        using result_type = size_t;
        using argument_type = My_type;

        size_t operator()(const My_type & x) const
        {
            size_t xs = x.s.size();
            if (xs < 4) throw Bad_My_type{};    // « Personne ne s’attend à l’inquisition espagnole !»
            return hash<size_t>()(x.s.size()) ^ trim(x.s);
        }
    };

    int main()
    {
        unordered_map<My_type, int> m;
        My_type mt{ "asdfg" };
        m[mt] = 7;
        cout << m[My_type{ "asdfg" }] << '\n';
    }

Si vous devez définir une spécialisation de `hash`, essayez simplement de combiner les `hash` standard avec `^` (xor). Cela fonctionne mieux que des « cleverness » pour les non‑spécialistes.

##### Application

* Signaler les `hash` qui lancent.

### <a name="rc-memset"></a>C.90 : S’appuyer sur les constructeurs et les opérateurs d’assignation, pas sur `memset` et `memcpy`

##### Raison

Le mécanisme C++ standard pour créer une instance d’un type est d’appeler son constructeur. Comme indiqué dans la règle [C.41](#rc-complete) : un constructeur doit créer un objet complètement initialisé. Aucune initialisation supplémentaire, comme `memcpy`, ne doit être requise. Un type fournira un constructeur de copie et/ou un opérateur d’assignation pour copier correctement l’objet, en préservant ses invariantes. Utiliser `memcpy` sur un type non trivially copiable entraîne un comportement indéfini, souvent à cause du slicing ou de la corruption de données.

##### Exemple, bon

    struct base {
        virtual void update() = 0;
        std::shared_ptr<int> sp;
    };

    struct derived : public base {
        void update() override {}
    };

##### Exemple, mauvais

    void init(derived& a)
    {
        memset(&a, 0, sizeof(derived));
    }

C’est non‑type‑safe et écrase la vtable.

##### Exemple, mauvais

    void copy(derived& a, derived& b)
    {
        memcpy(&a, &b, sizeof(derived));
    }

C’est aussi non‑type‑safe et écrase la vtable.

##### Application

* Signaler le passage d’un type non trivially‑copiable à `memset` ou `memcpy`.

## <a name="ss-containers"></a>C.con : Conteneurs et autres gestionnaires de ressources

Un conteneur est un objet détenant une séquence d’objets d’un certain type ; `std::vector` est le conteneur archétypal. Un gestionnaire de ressources est une classe qui possède une ressource ; `std::vector` constitue également un gestionnaire de ressources : sa ressource est sa séquence d’éléments.

Résumé des règles de conteneur :

* [C.100 : Suivre le STL lors de la définition d’un conteneur](#rcon-stl)
* [C.101 : Donner à un conteneur une sémantique de valeur](#rcon-val)
* [C.102 : Donner à un conteneur des opérations de déplacement](#rcon-move)
* [C.103 : Donner à un conteneur un constructeur à liste d’initialisation](#rcon-init)
* [C.104 : Donner à un conteneur un constructeur par défaut qui le place à vide](#rcon-empty)
* ???
* [C.109 : Si un gestionnaire de ressources a une sémantique de pointeur, fournir `*` et `->`](#rcon-ptr)

**Voir aussi** : [Ressources](#s-resource)

### <a name="rcon-stl"></a>C.100 : Suivre le STL lors de la définition d’un conteneur

##### Raison

Les conteneurs STL sont familiers à la plupart des programmeurs C++ et possèdent un design fondamentalement solide.

##### Remarque

Il existe d’autres styles de design tout aussi solides, et parfois des raisons d’en s’écarter, mais à défaut de raison solide, il est plus simple et plus facile tant pour les implémenteurs que pour les utilisateurs de suivre le standard.

En particulier, `std::vector` et `std::map` offrent des modèles relativement simples et utiles.

##### Exemple

    // simplifié (ex. pas d’allocateurs) :

    template<typename T>
    class Sorted_vector {
        using value_type = T;
        // ... types d’itérateurs ...

        Sorted_vector() = default;
        Sorted_vector(initializer_list<T>);    // constructeur à liste d’initialisation : trie et stocke
        Sorted_vector(const Sorted_vector&) = default;
        Sorted_vector(Sorted_vector&&) noexcept = default;
        Sorted_vector& operator=(const Sorted_vector&) = default;     // assignation copie
        Sorted_vector& operator=(Sorted_vector&&) noexcept = default; // assignation déplacement
        ~Sorted_vector() = default;

        Sorted_vector(const std::vector<T>& v);   // stocker et trier
        Sorted_vector(std::vector<T>&& v);        // trier et « voler » la représentation

        const T& operator[](int i) const { return rep[i]; }
        // pas d’accès non‑const direct pour préserver l’ordre

        void push_back(const T&);   // insérer à la bonne place (pas forcément à la fin)
        void push_back(T&&);        // idem
        // ... cbegin(), cend() ...
    private:
        std::vector<T> rep;  // utiliser std::vector pour stocker les éléments
    };

    template<typename T> bool operator==(const Sorted_vector<T>&, const Sorted_vector<T>&);
    template<typename T> bool operator!=(const Sorted_vector<T>&, const Sorted_vector<T>&);
    // ...

Ici, le style STL est suivi, mais de façon incomplète. Ce n’est pas rare. Fournissez uniquement les fonctionnalités qui ont du sens pour le conteneur spécifique. L’important est de définir les constructeurs, assignations, destructeurs et itérateurs (dans la mesure où ils sont pertinents) avec leurs sémantiques conventionnelles. À partir de cette base, le conteneur peut être enrichi selon les besoins. Dans cet exemple, des constructeurs spéciaux depuis `std::vector` ont été ajoutés.

##### Application

???

### <a name="rcon-val"></a>C.101 : Donner à un conteneur une sémantique de valeur

##### Raison

Les objets réguliers sont plus simples à penser et à raisonner que les irréguliers. Familiarité.

##### Remarque

Si cela a du sens, faire d’un conteneur un `Regular` (le concept). En particulier, assurez‑vous qu’un objet compare égal à sa copie.

##### Exemple

    void f(const Sorted_vector<string>& v)
    {
        Sorted_vector<string> v2 {v};
        if (v != v2)
            cout << "Comportement contre la raison et la logique.\n";
        // …
    }

##### Application

???

### <a name="rcon-move"></a>C.102 : Donner à un conteneur des opérations de déplacement

##### Raison

Les conteneurs ont tendance à être gros ; sans constructeur et assignation de déplacement, un objet peut être coûteux à déplacer, incitant les programmeurs à passer des pointeurs et à rencontrer des problèmes de gestion de ressources.

##### Exemple

    Sorted_vector<int> read_sorted(istream& is)
    {
        vector<int> v;
        cin >> v;   // supposons une opération de lecture pour les vecteurs
        Sorted_vector<int> sv = v;  // tri
        return sv;
    }

Un utilisateur peut raisonnablement supposer que retourner un conteneur de type standard est bon marché.

##### Application

???

### <a name="rcon-init"></a>C.103 : Donner à un conteneur un constructeur à liste d’initialisation

##### Raison

Les gens s’attendent à pouvoir initialiser un conteneur avec un ensemble de valeurs. Familiarité.

##### Exemple

    Sorted_vector<int> sv {1, 3, -1, 7, 0, 0}; // Sorted_vector trie les éléments au besoin

##### Application

???

### <a name="rcon-empty"></a>C.104 : Donner à un conteneur un constructeur par défaut qui le place à vide

##### Raison

Pour le rendre `Regular`.

##### Exemple

    vector<Sorted_sequence<string>> vs(100);    // 100 Sorted_sequences chacun avec la valeur ""

##### Application

???

### <a name="rcon-ptr"></a>C.109 : Si un gestionnaire de ressources a une sémantique de pointeur, fournir `*` et `->`

##### Raison

C’est ce qui est attendu des pointeurs. Familiarité.

##### Exemple

??? (section not filled)

##### Application

???

## <a name="ss-lambdas"></a>C.lambdas : Objets fonctionnels et lambdas

Un objet fonctionnel est un objet qui surcharge `operator()` afin de pouvoir être appelé. Une expression lambda (souvent raccourcie en « lambda ») est une notation pour générer un tel objet fonctionnel. Les objets fonctionnels devraient être peu coûteux à copier (et donc [passés par valeur](#rf-in)).

Résumé :

* [F.10 : Si une opération peut être réutilisée, donnez‑lui un nom](#rf-name)
* [F.11 : Utiliser une lambda non nommée si vous avez besoin d’un simple objet fonctionnel à un seul endroit](#rf-lambda)
* [F.50 : Utiliser une lambda quand une fonction ne suffit pas (pour capturer des variables locales, ou pour écrire une fonction locale)](#rf-capture-vs-overload)
* [F.52 : Privilégier la capture par référence dans les lambdas qui seront utilisées localement, y compris passées aux algorithmes](#rf-reference-capture)
* [F.53 : Éviter la capture par référence dans les lambdas qui seront utilisées de façon non locale, y compris retournées, stockées sur le tas, ou passées à un autre thread](#rf-value-capture)
* [ES.28 : Utiliser les lambdas pour une initialisation complexe, surtout de variables `const`](#res-lambda-init)

## <a name="ss-hier"></a>C.hier : Hiérarchies de classes (POO)

Une hiérarchie de classes est construite pour représenter un ensemble de concepts organisés hiérarchiquement (seulement). Typiquement, les classes de base servent d’interfaces. Il y a deux usages majeurs des hiérarchies, souvent appelés **héritage d’implémentation** et **héritage d’interface**.

Résumé des règles de hiérarchie de classe :

* [C.120 : Utiliser les hiérarchies de classes pour représenter des concepts avec une structure hiérarchique inhérente (seulement)](#rh-domain)
* [C.121 : Si une classe de base est utilisée comme interface, en faire une classe purement abstraite](#rh-abstract)
* [C.122 : Utiliser des classes abstraites comme interfaces lorsque la séparation complète d’interface et d’implémentation est nécessaire](#rh-separation)

Résumé des règles de conception des classes dans une hiérarchie :

* [C.126 : Une classe abstraite n’a généralement pas besoin d’un constructeur écrit par l’utilisateur](#rh-abstract-ctor)
* [C.127 : Une classe avec une fonction virtuelle doit avoir un destructeur virtuel ou protégé](#rh-dtor)
* [C.128 : Les fonctions virtuelles doivent spécifier exactement l’un de `virtual`, `override` ou `final`](#rh-override)
* [C.129 : Lors de la conception d’une hiérarchie de classes, distinguer héritage d’implémentation et héritage d’interface](#rh-kind)
* [C.130 : Pour faire des copies profondes de classes polymorphes, préférer une fonction virtuelle `clone` plutôt que la construction/copie publique](#rh-copy)
* [C.131 : Éviter les getters et setters triviaux](#rh-get)
* [C.132 : Ne pas rendre une fonction `virtual` sans raison](#rh-virtual)
* [C.133 : Éviter les données `protected`](#rh-protected)
* [C.134 : S’assurer que tous les membres non‑`const` ont le même niveau d’accès](#rh-public)
* [C.135 : Utiliser l’héritage multiple pour représenter plusieurs interfaces distinctes](#rh-mi-interface)
* [C.136 : Utiliser l’héritage multiple pour représenter l’union d’attributs d’implémentation](#rh-mi-implementation)
* [C.137 : Utiliser des bases virtuelles pour éviter des bases trop générales](#rh-vbase)
* [C.138 : Créer un ensemble de surcharges pour une classe dérivée et ses bases avec `using`](#rh-using)
* [C.139 : Utiliser `final` sur les classes avec parcimonie](#rh-final)
* [C.140 : Ne pas fournir d’arguments par défaut différents pour une fonction virtuelle et son redéfinisseur](#rh-virtual-default-arg)

Résumé des règles d’accès aux objets dans une hiérarchie :

* [C.145 : Accéder aux objets polymorphes via pointeurs et références](#rh-poly)
* [C.146 : Utiliser `dynamic_cast` lorsque la navigation de la hiérarchie est incontournable](#rh-dynamic_cast)
* [C.147 : Utiliser `dynamic_cast` vers un type référence quand l’échec est considéré comme une erreur](#rh-ref-cast)
* [C.148 : Utiliser `dynamic_cast` vers un type pointeur quand l’échec est une alternative valide](#rh-ptr-cast)
* [C.149 : Utiliser `unique_ptr` ou `shared_ptr` pour éviter d’oublier de `delete` les objets créés avec `new`](#rh-smart)
* [C.150 : Utiliser `make_unique()` pour construire des objets possédés par `unique_ptr`s](#rh-make_unique)
* [C.151 : Utiliser `make_shared()` pour construire des objets possédés par `shared_ptr`s](#rh-make_shared)
* [C.152 : Ne jamais assigner un pointeur vers un tableau d’objets dérivés à un pointeur vers la base](#rh-array)
* [C.153 : Privilégier les fonctions virtuelles aux castings](#rh-use-virtual)

### <a name="rh-domain"></a>C.120 : Utiliser les hiérarchies de classes pour représenter des concepts à structure hiérarchique inhérente (seulement)

##### Raison

Représenter directement les idées dans le code facilite la compréhension et la maintenance. Assurez‑vous que l’idée représentée par la classe de base correspond exactement à tous les types dérivés et qu’il n’existe pas de meilleure façon de l’exprimer que d’utiliser le couplage serré de l’héritage.

*Ne pas* utiliser l’héritage lorsqu’un simple membre de données suffit. Habituellement cela signifie que le type dérivé doit surcharger une fonction virtuelle de la base ou accéder à un membre `protected`.

##### Exemple

    class DrawableUIElement {
    public:
        virtual void render() const = 0;
        // …
    };

    class AbstractButton : public DrawableUIElement {
    public:
        virtual void onClick() = 0;
        // …
    };

    class PushButton : public AbstractButton {
        void render() const override;
        void onClick() override;
        // …
    };

    class Checkbox : public AbstractButton {
        // …
    };

##### Exemple, mauvais

Ne **pas** représenter des concepts de domaine non hiérarchiques en tant que hiérarchie de classes.

    template<typename T>
    class Container {
    public:
        // opérations de liste :
        virtual T& get() = 0;
        virtual void put(T&) = 0;
        virtual void insert(Position) = 0;
        // …
        // opérations de vecteur :
        virtual T& operator[](int) = 0;
        virtual void sort() = 0;
        // …
        // opérations d’arbre :
        virtual void balance() = 0;
        // …
    };

La plupart des classes dérivées ne pourront pas implémenter correctement la majorité des fonctions requises par l’interface, ce qui rend la base lourde à implémenter. En outre, l’utilisateur de `Container` ne peut pas compter sur le fait que les fonctions exécutent réellement des opérations utiles et efficaces ; elles peuvent lancer une exception à la place. Ainsi les utilisateurs doivent recourir à des vérifications en temps d’exécution ou **éviter** d’utiliser cette (trop)‑générale interface via un type‑requête (`dynamic_cast`).

##### Application

* Rechercher les classes avec beaucoup de membres qui ne font que lancer des exceptions.
* Signaler chaque utilisation d’une classe de base non‑publique `B` où la classe dérivée `D` ne surcharge pas une fonction virtuelle ou n’accède pas à un membre `protected` de `B`, et où `B` n’est pas parmi : vide, paramètre de modèle ou pack de paramètres de `D`.

### <a name="rh-abstract"></a>C.121 : Si une classe de base est utilisée comme interface, en faire une classe purement abstraite

##### Raison

Une classe est plus stable (moins fragile) si elle ne contient pas de données. Les interfaces devraient normalement être composées uniquement de fonctions virtuelles pures publiques et d’un destructeur virtuel (par défaut) vide.

##### Exemple

    class My_interface {
    public:
        // … seulement des fonctions virtuelles pures …
        virtual ~My_interface() {}   // ou =default
    };

##### Exemple, mauvais

    class Goof {
    public:
        // … seulement des fonctions virtuelles pures …
        // pas de destructeur virtuel
    };

    class Derived : public Goof {
        string s;
        // …
    };

    void use()
    {
        unique_ptr<Goof> p {new Derived{"here we go"}};
        f(p.get()); // utiliser Derived via l’interface Goof
        g(p.get()); // idem
    } // fuite

`Derived` est `delete`‑é via son interface `Goof`, donc son `string` est fuité. Donner à `Goof` un destructeur virtuel résout le problème.

##### Application

* Avertir pour toute classe qui possède des membres de données et aussi une fonction virtuelle (non `final`) qui n’est pas héritée d’une classe de base.

### <a name="rh-separation"></a>C.122 : Utiliser des classes abstraites comme interfaces lorsque la séparation complète d’interface et d’implémentation est nécessaire

##### Raison

Par ex. sur une frontière d’ABI (lien).

##### Exemple

    struct Device {
        virtual ~Device() = default;
        virtual void write(span<const char> outbuf) = 0;
        virtual void read(span<char> inbuf) = 0;
    };

    class D1 : public Device {
        // … données …

        void write(span<const char> outbuf) override;
        void read(span<char> inbuf) override;
    };

    class D2 : public Device {
        // … données différentes …

        void write(span<const char> outbuf) override;
        void read(span<char> inbuf) override;
    };

Un utilisateur peut maintenant utiliser `D1` et `D2` de façon interchangeable via l’interface `Device`. De plus, on peut mettre à jour `D1` et `D2` de manière non compatible binaire tant que tout l’accès passe par `Device`.

##### Application

???

## C.hierclass : Concevoir des classes dans une hiérarchie :

### <a name="rh-abstract-ctor"></a>C.126 : Une classe abstraite n’a généralement pas besoin d’un constructeur écrit par l’utilisateur

##### Raison

Une classe abstraite n’a généralement aucun donnée à initialiser.

##### Exemple

    class Shape {
    public:
        // pas de constructeur écrit par l’utilisateur nécessaire dans la classe abstraite
        virtual Point center() const = 0;    // pure virtuelle
        virtual void move(Point to) = 0;
        // … plus de fonctions virtuelles pures …
        virtual ~Shape() {}                 // destructeur
    };

    class Circle : public Shape {
    public:
        Circle(Point p, int rad);           // constructeur dans la classe dérivée
        Point center() const override { return x; }
    };

##### Exception

* Un constructeur de classe de base qui fait du travail, comme enregistrer un objet quelque part, peut nécessiter un constructeur.
* Dans des cas très rares, il peut être raisonnable qu’une classe abstraite possède quelques données partagées par toutes les classes dérivées (ex. données statistiques, informations de débogage, etc.) ; ces classes ont tendance à avoir des constructeurs. Mais attention : ces classes ont aussi souvent besoin d’une **héritage virtuel**.

##### Application

Signaler les classes abstraites contenant des constructeurs.

### <a name="rh-dtor"></a>C.127 : Une classe avec une fonction virtuelle doit avoir un destructeur virtuel ou protégé

##### Raison

Une classe avec une fonction virtuelle est généralement (et en général) utilisée via un pointeur/base. Souvent, le dernier utilisateur doit appeler `delete` sur un pointeur /base, souvent via un smart‑pointer de base, donc le destructeur doit être public et virtuel. Moins souvent, si la destruction via un pointeur /base n’est pas prévue, le destructeur doit être protégé et non‑virtuel ; voir [C.35](#rc-dtor-virtual).

##### Exemple, mauvais

    struct B {
        virtual int f() = 0;
        // ... pas de destructeur écrit par l’utilisateur, donc public non‑virtuel ...
    };

    // mauvais : dérivé d’une classe sans destructeur virtuel
    struct D : B {
        string s {"default"};
        // …
    };

    void use()
    {
        unique_ptr<B> p = make_unique<D>();
        // …
    } // comportement indéfini, ~B appelé mais pas ~D, fuite de s et potentiellement plus

##### Remarque

Certaines personnes ne suivent pas cette règle parce qu’elles prévoient d’utiliser la classe uniquement via un `shared_ptr` : `std::shared_ptr<B> p = std::make_shared<D>(args);`. Le `shared_ptr` s’occupera de la destruction, donc aucune fuite ne se produira à cause d’un `delete` inapproprié. Les gens qui font cela systématiquement peuvent obtenir des faux positifs, mais la règle reste importante — que se passe‑t‑il si on utilise `make_unique` ? Ce n’est pas sûr à moins que l’auteur de `B` ne garantisse qu’elle ne pourra jamais être mal utilisée, par ex. en rendant tous les constructeurs privés et en fournissant une fonction‑fabrique qui impose l’usage de `make_shared`.

##### Application

* Une classe contenant des fonctions virtuelles doit avoir un destructeur qui est soit public et virtuel, soit protégé et non‑virtuel.
* Signaler le `delete` d’une classe avec fonctions virtuelles mais sans destructeur virtuel.

### <a name="rh-override"></a>C.128 : Les fonctions virtuelles doivent spécifier exactement l’un de `virtual`, `override` ou `final`

##### Raison

Lisibilité. Détection d’erreurs. Écrire explicitement `virtual`, `override` ou `final` est auto‑documentant et permet au compilateur d’attraper les incompatibilités de type ou de nom entre les classes de base et dérivées. En revanche, en écrire plus d’un parmi ces trois est redondant et source potentielle d’erreurs.

C’est simple et clair :

* `virtual` signifie exactement « c’est une nouvelle fonction virtuelle ».
* `override` signifie exactement « c’est un redéfinisseur non‑final ».
* `final` signifie exactement « c’est un redéfinisseur final ».

##### Exemple, mauvais

    struct B {
        void f1(int);
        virtual void f2(int) const;
        virtual void f3(int);
        // …
    };

    struct D : B {
        void f1(int);        // mauvais (espérer un avertissement) : D::f1() masque B::f1()
        void f2(int) const; // mauvais (mais conventionnel et valide) : pas d’override explicite
        void f3(double);    // mauvais (espérer un avertissement) : D::f3() masque B::f3()
        // …
    };

##### Exemple, bon

    struct Better : B {
        void f1(int) override;        // erreur (capturée) : Better::f1() masque B::f1()
        void f2(int) const override;
        void f3(double) override;     // erreur (capturée) : Better::f3() masque B::f3()
        // …
    };

##### Discussion

Nous voulons éliminer deux types d’erreurs :

* **virtual implicite** : le programmeur voulait que la fonction soit virtuelle, mais les lecteurs ne le savent pas ; ou le programmeur voulait qu’elle soit virtuelle mais ce n’est pas le cas (ex. différence subtile de signature) ; ou le programmeur ne voulait pas qu’elle soit virtuelle mais elle le devient parce qu’elle a la même signature qu’une fonction virtuelle de la base.
* **override implicite** : le programmeur voulait qu’une fonction soit un redéfinisseur, mais ce n’est pas le cas (ex. différence subtile de signature) ; ou le programmeur ne voulait pas qu’elle soit un redéfinisseur mais elle le devient parce qu’elle a la même signature qu’une fonction virtuelle de la base (cela se produit même si la fonction n’est pas explicitement déclarée `virtual`, puisqu’elle se comporte virtuellement).

Note : Pour une classe déclarée `final`, chaque fonction virtuelle individuelle doit utiliser soit `override` soit `final` ; il n’y a pas de différence sémantique dans ce cas.

Note : Utiliser `final` sur les fonctions avec parcimonie. Ce n’est pas toujours un gain de performance et empêche tout futur redéfinisseur.

##### Application

* Comparer les noms de fonctions virtuelles dans les bases et dérivées et signaler les usages du même nom qui ne redéfinissent pas.
* Signaler les redéfinitions qui ne portent ni `override` ni `final`.
* Signaler les déclarations de fonctions qui utilisent plus d’un parmi `virtual`, `override`, `final`.

### <a name="rh-kind"></a>C.129 : Lors de la conception d’une hiérarchie, distinguer entre héritage d’implémentation et héritage d’interface

##### Raison

Les détails d’implémentation dans une interface rendent l’interface fragile ; les utilisateurs sont vulnérables à devoir recompiler après des changements d’implémentation. Les données dans une classe de base augmentent la complexité de mise en œuvre et peuvent conduire à la duplication de code.

##### Remarque

Définitions :

* **héritage d’interface** : usage de l’héritage pour séparer les utilisateurs de l’implémentation, notamment pour permettre l’ajout de nouvelles classes dérivées sans affecter les utilisateurs de la base.
* **héritage d’implémentation** : usage de l’héritage pour simplifier l’implémentation de nouvelles installations en mettant à disposition des opérations utiles aux implémenteurs de nouvelles opérations connexes (parfois appelé *programming by difference*).

Une classe d’interface pure n’est qu’un ensemble de fonctions virtuelles pures ; voir [I.25](#ri-abstract).

Dans les débuts de la POO (années 80‑90), hériter à la fois pour l’interface et l’implémentation était fréquent et les mauvaises habitudes restent présentes. Aujourd’hui, les mélanges ne sont pas rares dans les vieux projets et le matériel d’enseignement ancien.

L’importance de garder les deux types d’héritage séparés augmente

* avec la taille d’une hiérarchie (ex. dizaines de classes dérivées),
* avec la durée d’utilisation de la hiérarchie (ex. décennies),
* avec le nombre d’organisations distinctes qui utilisent la hiérarchie (ex. difficile de distribuer une mise à jour d’une base de classe).

##### Exemple, mauvais

    class Shape {   // MAUVAIS : mélange interface et implémentation
    public:
        Shape();
        Shape(Point ce = {0, 0}, Color co = none): cent{ce}, col {co} { /* … */ }

        Point center() const { return cent; }
        Color color() const { return col; }

        virtual void rotate(int) = 0;
        virtual void move(Point p) { cent = p; redraw(); }

        virtual void redraw();

        // …
    private:
        Point cent;
        Color col;
    };

    class Circle : public Shape {
    public:
        Circle(Point c, int r) : Shape{c}, rad{r} { /* … */ }

        // …
    private:
        int rad;
    };

    class Triangle : public Shape {
    public:
        Triangle(Point p1, Point p2, Point p3); // calcule le centre
        // …
    };

Problèmes :

* Au fur et à mesure que la hiérarchie grandit et que davantage de données est ajoutée à `Shape`, les constructeurs deviennent plus difficiles à écrire et à maintenir.
* Pourquoi calculer le centre pour le `Triangle` ? Nous pourrions ne jamais l’utiliser.
* Ajouter un membre à `Shape` (ex. style de dessin ou canevas) oblige à réviser toutes les classes dérivées et tout le code qui utilise `Shape`, probablement à recompilation et modification.

L’implémentation de `Shape::move()` est un exemple d’**héritage d’implémentation** : on l’a défini une fois pour toutes, pour toutes les classes dérivées. Plus il y a de code dans de telles fonctions de base, et plus de données partagées par placement dans la base, plus les bénéfices sont gros — mais la hiérarchie devient moins stable.

##### Exemple – refactorisation en interface pure

    class Shape {  // pure interface
    public:
        virtual Point center() const = 0;
        virtual Color color() const = 0;

        virtual void rotate(int) = 0;
        virtual void move(Point p) = 0;

        virtual void redraw() = 0;

        // …
    };

Notez qu’une interface pure a rarement des constructeurs : rien à construire.

    class Circle : public Shape {
    public:
        Circle(Point c, int r, Color c) : cent{c}, rad{r}, col{c} { /* … */ }

        Point  center() const override { return cent; }
        Color  color()  const override { return col; }

        // …
    private:
        Point cent;
        int   rad;
        Color col;
    };

L’interface est maintenant moins fragile, mais le travail d’implémentation augmente. Par ex., `center` doit être implémenté par chaque classe dérivée.

##### Exemple – hiérarchie double

Comment combiner les avantages des hiérarchies d’interface (stabilité) et des hiérarchies d’implémentation (réutilisation) ? Une technique populaire consiste en des hiérarchies doubles. Il existe de nombreuses façons d’implémenter cette idée ; ici, nous utilisons une variante à héritage multiple.

D’abord, créons une hiérarchie d’interfaces :

    class Shape {   // pure interface
    public:
        virtual Point center() const = 0;
        virtual Color color() const = 0;

        virtual void rotate(int) = 0;
        virtual void move(Point p) = 0;

        virtual void redraw() = 0;

        // …
    };

    class Circle : public Shape {
    public:
        virtual int radius() = 0;
        // …
    };

Pour rendre cela utile, nous fournissons des classes d’implémentation (nommées de façon équivalente, mais dans l’espace de noms `Impl`) :

    class Impl::Shape : public virtual ::Shape { // implémentation
    public:
        // constructeurs, destructeur
        // …
        Point center() const override { /* … */ }
        Color color() const override { /* … */ }

        void rotate(int) override { /* … */ }
        void move(Point p) override { /* … */ }

        void redraw() override { /* … */ }

        // …
    };

    class Impl::Circle : public virtual ::Circle, public Impl::Shape {   // implémentation
    public:
        // constructeurs, destructeur

        int radius() override { /* … */ }
        // …
    };

Nous pourrions ajouter une classe `Smiley` (:-)) :

    class Smiley : public virtual Circle { // pure interface
    public:
        // …
    };

    class Impl::Smiley : public virtual ::Smiley, public Impl::Circle {   // implémentation
    public:
        // constructeurs, destructeur
        // …
    };

Nous avons maintenant deux hiérarchies :

* interface : `Smiley → Circle → Shape`
* implémentation : `Impl::Smiley → Impl::Circle → Impl::Shape`

Comme chaque implémentation dérive de son interface ainsi que de sa classe d’implémentation de base, on obtient un **lattice** (DAG) :

      Smiley        →        Circle       →       Shape
         ^                     ^                    ^
         |                     |                    |
    Impl::Smiley    →     Impl::Circle    →    Impl::Shape

C’est juste une façon de construire une hiérarchie double.

L’hiérarchie d’implémentation peut être utilisée directement, sans passer par l’interface.

    void work_with_shape(Shape&);

    int user()
    {
        Impl::Smiley my_smiley{ /* args */ };   // créer un shape concret
        // …
        my_smiley.some_member();        // utiliser la classe d’implémentation directement
        // …
        work_with_shape(my_smiley);     // via l’interface abstraite
        // …
    }

Cela peut être utile quand la classe d’implémentation possède des membres qui ne sont pas offerts dans l’interface, ou si l’utilisation directe d’un membre offre des optimisations (ex. si la fonction membre d’implémentation est `final`).

##### Remarque

Une autre technique liée pour séparer interface et implémentation est le **Pimpl** (#ri-pimpl).

##### Remarque

Il y a souvent un choix entre offrir une fonctionnalité commune comme fonction membre de base ou comme fonction libre (dans un espace de noms d’implémentation). Les classes de base offrent une notation plus courte et un accès plus facile aux données communes (dans la base) au prix que la fonctionnalité ne soit disponible que pour les utilisateurs de la hiérarchie.

##### Application

* Signaler une conversion dérivée→base où la base possède à la fois des données et des fonctions virtuelles (sauf appels depuis un membre dérivé vers un membre base).
* ???

### <a name="rh-copy"></a>C.130 : Pour faire des copies profondes de classes polymorphes, préférer une fonction virtuelle `clone` au lieu d’un constructeur/copy‑assignment public

##### Raison

Copier une classe polymorphe est découragé à cause du problème de **slicing**, voir [C.67](#rc-copy-virtual). Si vous avez vraiment besoin d’une sémantique de copie, copiez en profondeur : fournissez une fonction virtuelle `clone` qui copiera le type le plus dérivé réel et renverra un pointeur possesseur vers le nouvel objet, puis dans les dérivés, retournez le type dérivé (utiliser un type de retour covariant).

##### Exemple

    class B {
    public:
        B() = default;
        virtual ~B() = default;
        virtual gsl::owner<B*> clone() const = 0;
    protected:
        B(const B&) = default;
        B& operator=(const B&) = default;
        B(B&&) noexcept = default;
        B& operator=(B&&) noexcept = default;
        // …
    };

    class D : public B {
    public:
        gsl::owner<D*> clone() const override
        {
            return new D{*this};
        };
    };

Il est généralement recommandé d’utiliser des pointeurs intelligents pour représenter la propriété (voir [R.20](#rr-owner)). Cependant, en raison des règles du langage, le type de retour covariant ne peut pas être un `unique_ptr` : `D::clone` ne peut pas retourner `unique_ptr<D>` alors que `B::clone` retourne `unique_ptr<B>`. Donc, soit vous retournez systématiquement `unique_ptr<B>` dans toutes les surcharges, soit vous utilisez `owner<>` de la [Guidelines Support Library](#ss-views).

### <a name="rh-get"></a>C.131 : Éviter les getters et setters triviaux

##### Raison

Un getter ou setter trivial n’ajoute aucune valeur sémantique ; la donnée pourrait tout simplement être `public`.

##### Exemple

    class Point {   // Mauvais : verbeux
        int x;
        int y;
    public:
        Point(int xx, int yy) : x{xx}, y{yy} { }
        int get_x() const { return x; }
        void set_x(int xx) { x = xx; }
        int get_y() const { return y; }
        void set_y(int yy) { y = yy; }
        // aucune fonction comportementale
    };

Considérez de faire de cette classe un `struct` — c’est‑à‑dire, un groupe de variables sans comportement :

    struct Point {
        int x {0};
        int y {0};
    };

Notez que nous pouvons placer des initialiseurs de membres par défaut : [C.49 : Privilégier l’initialisation à l’affectation dans les constructeurs](#rc-initialize).

##### Remarque

La clé ici est de déterminer si la sémantique du getter/setter est triviale. Bien que ce ne soit pas une définition complète de « trivial », demandez‑vous si la différence serait uniquement syntaxique avec un accès public. Des sémantiques non triviales incluraient : maintenir une invariante de classe ou convertir entre un type interne et un type d’interface.

##### Application

Signaler plusieurs fonctions `get`/`set` qui se contentent d’accéder directement à un membre sans sémantique additionnelle.

### <a name="rh-virtual"></a>C.132 : Ne pas rendre une fonction `virtual` sans raison

##### Raison

`virtual` augmente le temps d’exécution et la taille du code objet. Une fonction virtuelle peut être surchargée et est donc ouverte aux erreurs dans une classe dérivée. Une fonction virtuelle assure la réplication du code dans une hiérarchie de modèles.

##### Exemple, mauvais

    template<class T>
    class Vector {
    public:
        // …
        virtual int size() const { return sz; }   // mauvais : que pourrait faire une classe dérivée ?
    private:
        T* elem;   // les éléments
        int sz;    // nombre d’éléments
    };

Ce type de « vector » ne devrait pas être utilisé comme classe de base.

##### Application

* Signaler une classe avec des fonctions virtuelles mais aucune classe dérivée.
* Signaler une classe où toutes les fonctions membres sont virtuelles et ont des implémentations.

### <a name="rh-protected"></a>C.133 : Éviter les données `protected`

**Formulation alternative** : Rendre les données membres `public` ou (préférablement) `private`.

##### Raison

Les données `protected` sont une source de complexité et d’erreurs. Elles compliquent la formulation des invariantes. Elles violent également la recommandation d’éviter de mettre des données dans les bases, ce qui conduit souvent à devoir gérer l’héritage virtuel.

##### Exemple, mauvais

    class Shape {
    public:
        // … fonctions d’interface …
    protected:
        // données pour les classes dérivées :
        Color fill_color;
        Color edge_color;
        Style st;
    };

Maintenant, chaque classe dérivée de `Shape` doit manipuler correctement les données `protected`. Cela a été populaire, mais c’est une source majeure de problèmes de maintenance. Dans une grande hiérarchie, l’utilisation cohérente de données `protected` est difficile à maintenir car il y a beaucoup de code, réparti sur beaucoup de classes. L’ensemble des classes qui peuvent toucher ces données est ouvert : tout le monde peut dériver une nouvelle classe et commencer à manipuler les données `protected`. Souvent, il n’est pas possible d’examiner l’ensemble complet des classes, donc tout changement à la représentation de la classe devient impossible. Il n’y a pas d’invariant imposé aux données `protected` ; c’est comme un ensemble de variables globales. Les données `protected` deviennent de facto globales à un large corps de code.

##### Remarque

Les données `protected` semblent tentantes pour permettre des améliorations arbitraires via dérivation. Souvent, ce qui en résulte sont des changements non‑principaux et des erreurs.

##### Remarque

Préférez les données `private` avec un invariant bien spécifié et appliqué ([rc‑private](#rc-private)). Alternativement, et souvent mieux, **éloignez les données** de toute classe utilisée comme interface ([rh‑abstract](#rh-abstract)).

##### Remarque

Les fonctions membres `protected` peuvent très bien fonctionner.

##### Application

Signaler les classes contenant des données `protected`.

### <a name="rh-public"></a>C.134 : S’assurer que tous les membres non‑`const` ont le même niveau d’accès

##### Raison

Prévention de la confusion logique menant à des erreurs. Si les membres non‑`const` n’ont pas le même niveau d’accès, le type est confus quant à son objectif : s’agit‑il d’un type qui maintient une invariante ou simplement d’une collection de valeurs ?

##### Discussion

La question centrale : quel code est responsable de maintenir une valeur correcte pour cette variable ?

Il existe exactement deux catégories de membres de données :

* **A** : ceux qui ne participent pas à l’invariant de l’objet. Toute combinaison de valeurs pour ces membres est valide.
* **B** : ceux qui participent à l’invariant de l’objet. Toutes les combinaisons ne sont pas valides (sinon il n’y aurait pas d’invariant). Ainsi, tout code qui a le droit d’écrire ces variables doit connaître l’invariant, les règles, et les appliquer.

Les membres de catégorie **A** devraient être `public` (ou, plus rarement, `protected` si vous ne voulez les exposer qu’aux classes dérivées). Ils n’ont pas besoin d’encapsulation. Tout le code du système pourrait donc les voir et les manipuler.

Les membres de catégorie **B** devraient être `private` ou `const`. Cela garantit l’encapsulation. Les rendre `public` ou `protected` permettrait à un nombre illimité de code externe (ou dérivé) de devoir connaître l’invariant et de le préserver, ce qui rend la classe difficile à maintenir. Tout code qui modifie ces membres doit adhérer à l’invariant — si les membres sont `public`, cela implique tout le code utilisant la classe ; si `protected`, cela inclut tout le code dans les classes dérivées. Cela mène à du code fragile, fortement couplé, qui devient rapidement un cauchemar de maintenance. Tout code qui modifie accidentellement ces membres dans une combinaison invalide corrompt l’objet et toutes les utilisations futures.

La plupart des classes sont **toutes A** ou **toutes B** :

* **Toutes publiques** : si vous écrivez un agrégat « bundle‑of‑variables » sans invariant, alors toutes les variables devraient être `public`. (Par convention, déclarez de telles classes en tant que `struct`.)
* **Toutes privées** : si vous écrivez un type qui maintient une invariante, alors tous les membres non‑`const` devraient être `private` — l’encapsulation est requise.

##### Exception

Parfois, les classes mélangent **A** et **B** à des fins de débogage. Un objet encapsulé peut contenir, par ex., une instrumentation de débogage non‑`const` qui n’est pas partie de l’invariant et qui ne contribue pas à l’état observable du type. Dans ce cas, les parties **A** devraient être traitées comme **A** (rendues `public` ou, plus rarement, `protected`) et les parties **B** demeurent `private` ou `const`.

##### Application

Signaler toute classe contenant des membres non‑`const` avec différents niveaux d’accès.

### <a name="rh-mi-interface"></a>C.135 : Utiliser l’héritage multiple pour représenter plusieurs interfaces distinctes

##### Raison

Toutes les classes ne supporteront pas toutes les interfaces, et tous les appelants ne voudront pas toutes les opérations. Surtout pour séparer des « aspects » du comportement supportés par une classe dérivée.

##### Exemple

    class iostream : public istream, public ostream {   // très simplifié
        // …
    };

`istream` fournit l’interface d’opérations d’entrée ; `ostream` l’interface de sortie. `iostream` fournit l’union des interfaces `istream` et `ostream` ainsi que la synchronisation nécessaire pour les faire cohabiter sur le même flux.

##### Remarque

C’est un usage très commun de l’héritage, car le besoin de multiples interfaces distinctes à une implémentation est fréquent et ces interfaces sont souvent abstraites.

##### Remarque

Ces interfaces sont typiquement des classes abstraites.

##### Application

???

### <a name="rh-mi-implementation"></a>C.136 : Utiliser l’héritage multiple pour représenter l’union d’attributs d’implémentation

##### Raison

Certaines formes de mixins possèdent un état et souvent des opérations sur cet état. Si les opérations sont virtuelles, l’utilisation de l’héritage est nécessaire ; sinon, éviter l’héritage peut réduire le code boilerplate et l’indirection.

##### Exemple

    class iostream : public istream, public ostream {   // très simplifié
    	// …
    };


`istream` fournit l’interface d’opérations d’entrée (et des données) ; `ostream` fournit l’interface de sortie (et des données). `iostream` fournit l’union des interfaces `istream` et `ostream` ainsi que la synchronisation nécessaire.

##### Remarque

C’est relativement rare parce que l’implémentation peut souvent être organisée dans une hiérarchie à racine unique.

##### Exemple

Parfois, un « attribut d’implémentation » ressemble plus à un **mixin** qui détermine le comportement d’une implémentation et injecte des membres pour permettre de réaliser les politiques qu’il exige. Par ex., voir `std::enable_shared_from_this` ou divers bases de Boost.Intrusive (`list_base_hook`, `intrusive_ref_counter`, …).

##### Application

???

### <a name="rh-vbase"></a>C.137 : Utiliser des bases virtuelles pour éviter des bases trop générales

##### Raison

Permet de séparer les données et l’interface. Évite que toutes les données partagées soient placées dans une classe de base ultime.

##### Exemple

    struct Interface {
        virtual void f();
        virtual int g();
        // ... aucune donnée ici ...
    };

    class Utility {  // avec données
        void utility1();
        virtual void utility2();    // point d’extension
    public:
        int x;
        int y;
    };

    class Derive1 : public Interface, virtual protected Utility {
        // redéfinir les fonctions Interface
        // éventuellement redéfinir les fonctions Utility virtuelles
        // ...
    };

    class Derive2 : public Interface, virtual protected Utility {
        // redéfinir les fonctions Interface
        // éventuellement redéfinir les fonctions Utility virtuelles
        // ...
    };

Factoriser `Utility` a du sens si de nombreuses classes dérivées partagent des « détails d’implémentation » significatifs.

##### Remarque

L’exemple est trop « théorique », mais il est difficile de trouver un exemple **petit** réaliste. `Interface` est la racine d’une [hiérarchie d’interfaces](#rh-abstract) et `Utility` la racine d’une [hiérarchie d’implémentation](#rh-kind). Voici [un exemple un peu plus réaliste](https://www.quora.com/What-are-the-uses-and-advantages-of-virtual-base-class-in-C%2B%2B/answer/Lance-Diduck) avec explication.

##### Remarque

Souvent, la **linéarisation** d’une hiérarchie est une meilleure solution.

##### Application

Signaler les hiérarchies mélangeant interface et implémentation.

### <a name="rh-using"></a>C.138 : Créer un ensemble de surcharges pour une classe dérivée et ses bases avec `using`

##### Raison

Sans instruction `using`, les fonctions membres de la classe dérivée cachent l’ensemble complet d’overloads hérités.

##### Exemple, mauvais

    #include <iostream>
    class B {
    public:
        virtual int f(int i) { std::cout << "f(int): "; return i; }
        virtual double f(double d) { std::cout << "f(double): "; return d; }
        virtual ~B() = default;
    };
    class D: public B {
    public:
        int f(int i) override { std::cout << "f(int): "; return i + 1; }
    };
    int main()
    {
        D d;
        std::cout << d.f(2) << '\n';   // imprime "f(int): 3"
        std::cout << d.f(2.3) << '\n'; // imprime "f(int): 3"
    }

##### Exemple, bon

    class D: public B {
    public:
        int f(int i) override { std::cout << "f(int): "; return i + 1; }
        using B::f; // expose f(double)
    };

##### Remarque

Ce problème affecte à la fois les opérateurs virtuels et non‑virtuels.

Pour les bases variadiques, C++17 a introduit une forme variadique du `using`‑declaration :

    template<class... Ts>
    struct Overloader : Ts... {
        using Ts::operator()...; // expose operator() de chaque base
    };

##### Application

Diagnostiquer le masquage de noms.

### <a name="rh-final"></a>C.139 : Utiliser `final` sur les classes avec parcimonie

##### Raison

Capter une hiérarchie avec `final` est rarement justifié pour des raisons logiques et peut nuire à l’extensibilité d’une hiérarchie.

##### Exemple, mauvais

    class Widget { /* … */ };

    // personne ne voudra jamais améliorer My_widget (ou du moins vous le pensiez)
    class My_widget final : public Widget { /* … */ };

    class My_improved_widget : public My_widget { /* … */ };  // erreur : impossible

##### Remarque

Toutes les classes ne sont pas destinées à être des bases. La plupart des classes de la bibliothèque standard en sont des exemples (ex. `std::vector`, `std::string` ne sont pas conçues pour être dérivées). Cette règle concerne l’usage de `final` sur les **classes** contenant des fonctions virtuelles destinées à être des interfaces de hiérarchie.

##### Remarque

Les affirmations selon lesquelles `final` améliore les performances doivent être justifiées. Souvent, ces affirmations sont basées sur la conjecture ou l’expérience avec d’autres langages.

Il existe des exemples où `final` est utile tant au niveau logique que de performance. Par ex. une hiérarchie AST critique pour la performance d’un compilateur ; les nouvelles classes dérivées ne sont ajoutées que rarement et seulement par les implémenteurs de la bibliothèque. Cependant, les abus sont (ou ont été) bien plus fréquents.

##### Application

Signaler les usages de `final` sur des classes.

### <a name="rh-virtual-default-arg"></a>C.140 : Ne pas fournir d’arguments par défaut différents pour une fonction virtuelle et son redéfinisseur

##### Raison

Cela peut créer de la confusion : un redéfinisseur n’hérite pas des arguments par défaut.

##### Exemple, mauvais

    class Base {
    public:
        virtual int multiply(int value, int factor = 2) = 0;
        virtual ~Base() = default;
    };

    class Derived : public Base {
    public:
        int multiply(int value, int factor = 10) override;
    };

    Derived d;
    Base& b = d;

    b.multiply(10);  // ces deux appels invoquent la même fonction mais
    d.multiply(10);  // avec des arguments différents, donc des résultats différents

##### Application

Signaler les arguments par défaut sur les fonctions virtuelles s’ils diffèrent entre la base et le dérivé.

## C.hier‑access : Accéder aux objets dans une hiérarchie

### <a name="rh-poly"></a>C.145 : Accéder aux objets polymorphes via pointeurs et références

##### Raison

Si vous avez une classe avec une fonction virtuelle, vous ne savez généralement pas quelle classe fournit la fonction utilisée.

##### Exemple

    struct B { int a; virtual int f(); virtual ~B = default };
    struct D : B { int b; int f() override; };

    void use(B b)
    {
        D d;
        B b2 = d;   // slice
        B b3 = b;
    }

    void use2()
    {
        D d;
        use(d);   // slice
    }

Les deux `d` sont tranchés.

##### Exception

Vous pouvez accéder en toute sécurité à un objet polymorphe nommé dans la portée de sa définition, simplement ne le tranchez pas.

    void use3()
    {
        D d;
        d.f();   // OK
    }

##### Voir aussi

[Une classe polymorphe doit supprimer la copie](#rc-copy-virtual)

##### Application

Signaler tout slicing.

### <a name="rh-dynamic_cast"></a>C.146 : Utiliser `dynamic_cast` lorsqu’on ne peut pas éviter la navigation de la hiérarchie

##### Raison

`dynamic_cast` est vérifié à l’exécution.

##### Exemple

    struct B {   // une interface
        virtual void f();
        virtual void g();
        virtual ~B();
    };

    struct D : B {   // une interface plus large
        void f() override;
        virtual void h();
    };

    void user(B* pb)
    {
        if (D* pd = dynamic_cast<D*>(pb)) {
            // ... utiliser l’interface de D ...
        }
        else {
            // ... se contenter de l’interface de B ...
        }
    }

L’usage d’autres cast peut violer la sécurité du type et faire accéder le programme à une variable réellement de type `X` comme si elle était d’un type non‑lié `Z` :

    void user2(B* pb)   // mauvais
    {
        D* pd = static_cast<D*>(pb);    // je sais que pb pointe réellement vers un D ; faites‑le confiance
        // ... utilisation de l’interface de D ...
    }

    void user3(B* pb)    // unsafe
    {
        if (some_condition) {
            D* pd = static_cast<D*>(pb);   // je sais que pb pointe réellement vers un D ; faites‑le confiance
            // ... utilisation de l’interface de D ...
        }
        else {
            // ... se contenter de l’interface de B ...
        }
    }

    void f()
    {
        B b;
        user(&b);   // OK
        user2(&b);  // mauvais error
        user3(&b);  // OK *si* la vérification de some_condition est correcte
    }

##### Remarque

`dynamic_cast` est parfois sur‑utilisé. [Privilégier les fonctions virtuelles au casting](#rh-use-virtual). Privilégier le [polymorphisme statique](#???) là où c’est possible (pas de résolution d’exécution) et raisonnablement commode.

##### Remarque

Certaines personnes utilisent `dynamic_cast` lorsqu’un `typeid` aurait été plus approprié ; `dynamic_cast` est une opération « is‑kind » générique pour découvrir la meilleure interface d’un objet, alors que `typeid` est une opération « donnez‑moi le type exact ». Le `typeid` est plus simple et généralement plus rapide. Si `typeid` n’est pas disponible (par ex. RTTI prohibé), on peut le simuler, mais `dynamic_cast` est beaucoup plus difficile à implémenter correctement.

Considérez :

    struct B {
        const char* name {"B"};
        // si pb1->id() == pb2->id() *pb1 a le même type que *pb2
        virtual const char* id() const { return name; }
        // …
    };

    struct D : B {
        const char* name {"D"};
        const char* id() const override { return name; }
        // …
    };

    void use()
    {
        B* pb1 = new B;
        B* pb2 = new D;

        cout << pb1->id(); // "B"
        cout << pb2->id(); // "D"


        if (pb2->id() == "D") {         // paraît innocent
            D* pd = static_cast<D*>(pb2);
            // …
        }
        // …
    }

Le résultat de `pb2->id() == "D"` est en réalité **implementation‑defined**. Nous l’ajoutons pour alerter sur les dangers du RTTI maison. Ce code pourrait fonctionner pendant des années, puis échouer sur une nouvelle machine, un nouveau compilateur ou un nouvel éditeur de liens qui ne fusionne pas les littéraux de caractères.

Si vous implémentez votre propre RTTI, soyez prudent.

##### Exception

Si votre implémentation fournit un `dynamic_cast` vraiment lent, vous pourriez envisager une astuce. Cependant, toutes les implémentations modernes sont suffisamment rapides ; les rumeurs d’un `dynamic_cast` lent sont souvent infondées. Si vous avez réellement besoin de performances, assurez‑vous d’abord que le problème vient bien du `dynamic_cast` (via mesures) et qu’il n’y a pas d’héritage virtuel. Vous pouvez alors, avec prudence, recourir à un `static_cast` accompagné d’un commentaire évident résumant le raisonnement et avertissant les mainteneurs.

##### Exception

Considérez :

    template<typename B>
    class Dx : B {
        // …
    };

##### Application

* Signaler tous les usages de `static_cast` pour des downcasts, y compris les cast C‑style qui réalisent un `static_cast`.
* Cette règle fait partie du [profil de sécurité de type](#pro-type-downcast).

### <a name="rh-ref-cast"></a>C.147 : Utiliser `dynamic_cast` vers un type référence lorsque l’échec doit être considéré comme une erreur

##### Raison

Caster vers une référence exprime que vous comptez obtenir un objet valide, donc le cast doit réussir. `dynamic_cast` lèvera alors une exception si le cast échoue.

##### Exemple

    std::string f(Base& b)
    {
        return dynamic_cast<Derived&>(b).to_string();
    }

##### Application

???

### <a name="rh-ptr-cast"></a>C.148 : Utiliser `dynamic_cast` vers un type pointeur lorsque l’échec est une alternative valide

##### Raison

La conversion `dynamic_cast` permet de tester si un pointeur pointe vers un objet polymorphe qui possède une classe donnée dans sa hiérarchie. Un échec renvoie simplement `nullptr`, ce qui peut être testé à l’exécution. Cela permet d’écrire du code qui peut choisir des chemins alternatifs selon le résultat.

Contrairement à [C.147](#rh-ref-cast), où l’échec est une erreur, ici l’échec est une condition testable.

##### Exemple

L’exemple suivant décrit la fonction `add` d’un `Shape_owner` qui prend possession d’objets `Shape` construits. Les objets sont aussi classés dans des vues selon leurs attributs géométriques. Dans cet exemple, `Shape` n’hérite pas de `Geometric_attributes`. Seules ses sous‑classes le font.

    void add(Shape* const item)
    {
        // Toujours prendre la possession
        owned_shapes.emplace_back(item);

        // Vérifier les Geometric_attributes et ajouter la forme aux vues correspondantes

        if (auto even = dynamic_cast<Even_sided*>(item))
        {
            view_of_evens.emplace_back(even);
        }

        if (auto trisym = dynamic_cast<Trilaterally_symmetrical*>(item))
        {
            view_of_trisyms.emplace_back(trisym);
        }
    }

##### Remarques

Un échec de `dynamic_cast` sur un pointeur renvoie `nullptr`; le dés‑référencement d’un tel pointeur entraînera un comportement indéfini. Ainsi, le résultat doit toujours être testé.

##### Application

* (Complexe) Sauf s’il y a un test `nullptr` sur le résultat d’un `dynamic_cast` pointeur, avertir lorsqu’on déréférence le pointeur.

### <a name="rh-smart"></a>C.149 : Utiliser `unique_ptr` ou `shared_ptr` pour éviter d’oublier de `delete` les objets créés avec `new`

##### Raison

Éviter les fuites de ressources.

##### Exemple

    void use(int i)
    {
        auto p = new int {7};           // mauvais : initier un pointeur local avec new
        auto q = make_unique<int>(9);   // ok : garantira la libération du 9
        if (0 < i) return;              // peut‑être retourner et fuir
        delete p;                       // trop tard
    }

##### Application

* Signaler l’initialisation d’un pointeur nu avec le résultat d’un `new`.
* Signaler le `delete` d’une variable locale.

### <a name="rh-make_unique"></a>C.150 : Utiliser `make_unique()` pour construire des objets possédés par `unique_ptr`s

Voir [R.23](#rr-make_unique)

### <a name="rh-make_shared"></a>C.151 : Utiliser `make_shared()` pour construire des objets possédés par `shared_ptr`s

Voir [R.22](#rr-make_shared)

### <a name="rh-array"></a>C.152 : Ne jamais assigner un pointeur vers un tableau d’objets dérivés à un pointeur vers sa base

##### Raison

L’indexation du pointeur de base résultera en un accès à un objet invalide et probablement en corruption mémoire.

##### Exemple

    struct B { int x; };
    struct D : B { int y; };

    void use(B*);

    D a[] = { {1, 2}, {3, 4}, {5, 6} };
    B* p = a;     // mauvais : a décaye vers &a[0] puis se convertit en B*
    p[1].x = 7;   // écrase a[0].y

##### Application

* Signaler toutes les combinaisons de décadage de tableau et de conversion base←‑derived.
* Passer un tableau en `span` plutôt qu’en pointeur, et éviter que le nom du tableau subisse une conversion base←‑derived avant d’entrer dans le `span`.

### <a name="rh-use-virtual"></a>C.153 : Privilégier les fonctions virtuelles aux castings

##### Raison

Un appel de fonction virtuelle est sûr, alors qu’un casting est source d’erreurs. Un appel virtuel atteint la fonction la plus dérivée, alors qu’un cast peut aboutir à une classe intermédiaire et donc donner un résultat erroné (surtout quand la hiérarchie change pendant la maintenance).

##### Exemple

??? (section non remplie)

##### Application

Voir [C.146](#rh-dynamic_cast) et ???.

## <a name="ss-overload"></a>C.over : Surcharge et opérateurs surchargés

Vous pouvez surcharger des fonctions ordinaires, des modèles de fonctions et des opérateurs. Vous ne pouvez pas surcharger des objets fonctionnels.

Résumé des règles de surcharge :

* [C.160 : Définir les opérateurs principalement pour imiter l’usage conventionnel](#ro-conventional)
* [C.161 : Utiliser des fonctions non‑membres pour les opérateurs symétriques](#ro-symmetric)
* [C.162 : Surcharger les opérations qui sont à peu près équivalentes](#ro-equivalent)
* [C.163 : Surcharger uniquement les opérations qui sont à peu près équivalentes](#ro-equivalent-2)
* [C.164 : Éviter les opérateurs de conversion implicites](#ro-conversion)
* [C.165 : Utiliser `using` pour les points de personnalisation](#ro-custom)
* [C.166 : Surcharger l’opérateur unaire `&` uniquement dans le cadre d’un système de pointeurs et références intelligents](#ro-address-of)
* [C.167 : Utiliser un opérateur pour une opération ayant son sens conventionnel](#ro-overload)
* [C.168 : Définir les opérateurs surchargés dans l’espace de noms de leurs opérandes](#ro-namespace)
* [C.170 : Si vous avez envie de surcharger un lambda, utilisez un lambda générique](#ro-lambda)

### <a name="ro-conventional"></a>C.160 : Définir les opérateurs principalement pour imiter l’usage conventionnel

##### Raison

Minimiser les surprises.

##### Exemple

    class X {
    public:
        // …
        X& operator=(const X&); // fonction membre définissant l’assignation
        friend bool operator==(const X&, const X&); // == a besoin d’accès à la représentation
                                                // après a = b on a a == b
        // …
    };

Ici, la sémantique conventionnelle est maintenue : [les copies comparent égales](#ss-copy).

##### Exemple, mauvais

    X operator+(X a, X b) { return a.v - b.v; }   // mauvais : + effectue une soustraction

##### Remarque

Les opérateurs non‑membres doivent être soit des amis, soit définis **dans le même espace de noms que leurs opérandes** ([le même espace de noms que leurs opérandes](#ro-namespace)). [Les opérateurs binaires doivent traiter leurs opérandes de façon équivalente](#ro-symmetric).

##### Application

Possiblement impossible.

### <a name="ro-symmetric"></a>C.161 : Utiliser des fonctions non‑membres pour les opérateurs symétriques

##### Raison

Si vous utilisez des fonctions membres, vous avez besoin de deux fonctions. Sans cela, `a == b` et `b == a` seront subtilement différents.

##### Exemple

    bool operator==(Point a, Point b) { return a.x == b.x && a.y == b.y; }

##### Application

Signaler les fonctions opérateur membres.

### <a name="ro-equivalent"></a>C.162 : Surcharger les opérations qui sont à peu près équivalentes

##### Raison

Avoir des noms différents pour des opérations logiquement équivalentes sur différents types d’argument est source de confusion, encode l’information de type dans le nom, et empêche la programmation générique.

##### Exemple

Considérez :

    void print(int a);
    void print(int a, int base);
    void print(const string&);

Ces trois fonctions toutes impriment leurs arguments (de façon appropriée). À l’inverse :

    void print_int(int a);
    void print_based(int a, int base);
    void print_string(const string&);

Ces trois fonctions font la même chose ; le nom ajoute simplement de la verbosité et entrave la programmation générique.

##### Application

???

### <a name="ro-equivalent-2"></a>C.163 : Surcharger uniquement les opérations qui sont à peu près équivalentes

##### Raison

Partager le même nom pour des fonctions logiquement différentes est source de confusion et crée des erreurs lorsqu’on utilise la programmation générique.

##### Exemple

Considérez :

    void open_gate(Gate& g);   // enlever un obstacle du tunnel de garage
    void fopen(const char* name, const char* mode);   // ouvrir un fichier

Les deux opérations sont fondamentalement différentes (et non reliées) donc il est bon que leurs noms diffèrent. À l’inverse :

    void open(Gate& g);   // enlever un obstacle du tunnel de garage
    void open(const char* name, const char* mode ="r");   // ouvrir un fichier

Ces deux opérations restent fondamentalement différentes (et non reliées) mais leurs noms sont réduits à leur minimum commun, ouvrant la porte à la confusion. Heureusement, le système de types attrapera beaucoup de ces erreurs.

##### Remarque

Soyez particulièrement prudent avec les noms courants et populaires, tels que `open`, `move`, `+` et `==`.

##### Application

???

### <a name="ro-conversion"></a>C.164 : Éviter les opérateurs de conversion implicites

##### Raison

Les conversions implicites peuvent être essentielles (ex. `double` → `int`) mais souvent provoquent des surprises (ex. `String` → C‑string).

##### Remarque

Préférez les conversions explicitement nommées tant qu’un besoin sérieux n’est pas démontré. Par « besoin sérieux », on entend une raison fondamentale dans le domaine d’application (par ex. conversion d’un entier vers un nombre complexe) et fréquemment nécessaire. N’introduisez pas de conversions implicites (via opérateurs de conversion ou constructeurs non‑`explicit`) simplement pour gagner un petit confort.

##### Exemple

    struct S1 {
        string s;
        // …
        operator char*() { return s.data(); }  // MAUVAIS : susceptible de surprendre
    };

    struct S2 {
        string s;
        // …
        explicit operator char*() { return s.data(); }
    };

    void f(S1 s1, S2 s2)
    {
        char* x1 = s1;     // OK, mais peut causer des surprises dans de nombreux contextes
        char* x2 = s2;     // erreur (et c’est souvent une bonne chose)
        char* x3 = static_cast<char*>(s2); // on peut être explicite (à vos risques et périls)
    }

La conversion implicite surprenante et potentiellement dommageable peut survenir dans des contextes très difficiles à repérer, par ex. :

    S1 ff();

    char* g()
    {
        return ff();   // le string retourné par ff() est détruit avant que le pointeur ne soit utilisé
    }

##### Application

Signaler tous les opérateurs de conversion non‑`explicit`.

### <a name="ro-custom"></a>C.165 : Utiliser `using` pour les points de personnalisation

##### Raison

Pour trouver les fonction‑objets et fonctions définies dans un espace de noms séparé afin de « personnaliser » une fonction commune.

##### Exemple

Considérons `swap`. C’est une fonction générale (standard) qui fonctionne pour presque tous les types. Cependant, il est souhaitable de définir des `swap()` spécifiques pour certains types. Par exemple, le `swap()` général copiera les éléments d’un `vector` lors de l’échange, alors qu’une implémentation spécifique optimisée n’effectuera aucune copie.

    namespace N {
        My_type X { /* … */ };
        void swap(X&, X&);   // swap optimisé pour N::X
        // …
    }

    void f1(N::X& a, N::X& b)
    {
        std::swap(a, b);   // probablement pas ce que nous voulions : appel à std::swap()
    }

`std::swap()` dans `f1()` fait exactement ce que nous lui demandons : il appelle `swap()` dans l’espace de noms `std`. Malheureusement, ce n’est probablement pas ce que nous voulions.

Comment faire reconnaître `N::X` ?  

    void f2(N::X& a, N::X& b)
    {
        swap(a, b);   // appelle N::swap
    }

Mais cela peut ne pas être ce que nous voulions dans du code générique. Là‑dé

    void f3(N::X& a, N::X& b)
    {
        using std::swap;  // rendre std::swap disponible
        swap(a, b);        // appelle N::swap si elle existe, sinon std::swap
    }

##### Application

Peu probable, sauf pour les points de personnalisation connus, comme `swap`. Le problème est que la recherche non‑qualifiée et qualifiée ont toutes les deux leurs usages.

### <a name="ro-address-of"></a>C.166 : Surcharger `&` unaire uniquement dans le cadre d’un système de pointeurs intelligents et de références

##### Raison

L’opérateur `&` est fondamental en C++. Beaucoup de parties de la sémantique C++ supposent son sens par défaut.

##### Exemple

    class Ptr { // un pointeur « quelque peu intelligent »
        Ptr(X* pp) : p(pp) { /* check */ }
        X* operator->() { /* check */ return p; }
        X operator[](int i);
        X operator*();
    private:
        T* p;
    };

    class X {
        Ptr operator&() { return Ptr{this}; }
        // …
    };

##### Remarque

Si vous « manipulez » `operator&`, assurez‑vous que sa définition possède une signification cohérente avec `->`, `[]`, `*` et `.` sur le type de résultat. Notez que `operator.` ne peut pas encore être surchargé ; nous espérons y remédier : [Operator Dot (R2)](https://www.open-std.org/jtc1/sc22/wg21/docs/papers/2015/n4477.pdf). Notez que `std::addressof()` renvoie toujours un pointeur intégré.

##### Application

Difficile. Avertir si `&` est défini par l’utilisateur sans également définir `->` pour le type de résultat.

### <a name="ro-overload"></a>C.167 : Utiliser un opérateur pour une opération ayant son sens conventionnel

##### Raison

Lisibilité. Convention. Réutilisabilité. Support du code générique.

##### Exemple

    void cout_my_class(const My_class& c) // confus, non conventionnel, non générique
    {
        std::cout << /* membres de classe ici */;
    }

    std::ostream& operator<<(std::ostream& os, const my_class& c) // OK
    {
        return os << /* membres de classe ici */;
    }

Par elle‑même, `cout_my_class` serait acceptable, mais elle n’est pas utilisable/composable avec le code qui s’appuie sur la convention `<<` pour la sortie :

    My_class var { /* … */ };
    // …
    cout << "var = " << var << '\n';

##### Remarque

Il existe des conventions fortes et vigoureuses pour la signification de la plupart des opérateurs, telles que

* comparaisons (`==`, `!=`, `<`, `<=`, `>`, `>=`, et `<=>`),
* opérations arithmétiques (`+`, `-`, `*`, `/`, `%`),
* opérations d’accès (`.`, `->`, `*` unaire, `[]`),
* assignation (`=`).

Ne définissez pas ces opérateurs de façon non conventionnelle et n’inventez pas vos propres noms.

##### Application

Difficile. Nécessite une compréhension sémantique.

### <a name="ro-namespace"></a>C.168 : Définir les opérateurs surchargés dans l’espace de noms de leurs opérandes

##### Raison

Lisibilité. Possibilité de trouver les opérateurs grâce à ADL. Éviter les définitions incohérentes dans différents espaces de noms.

##### Exemple

    struct S { };
    S operator+(S, S);   // OK : dans le même espace de noms que S, et même à côté de S
    S s;

    S r = s + s;


    namespace N {
        struct S { };
        S operator+(S, S);   // OK : dans le même espace de noms que S, et même à côté de S
    }

    N::S s;

    S r = s + s;  // trouve N::operator+() grâce à ADL


    struct S { };
    S s;

    namespace N {
        bool operator!(S a) { return true; }
        bool not_s = !s;
    }

    namespace M {
        bool operator!(S a) { return false; }
        bool not_s = !s;
    }

Ici, le sens de `!s` diffère entre `N` et `M`. C’est très déroutant. Supprimez la définition de `namespace M` et la confusion devient une opportunité de correction.

##### Remarque

Si un opérateur binaire est défini pour deux types situés dans des espaces de noms différents, vous ne pouvez pas suivre cette règle. Par ex. :

    Vec::Vector operator*(const Vec::Vector&, const Mat::Matrix&);

Cela pourrait être quelque chose à éviter.

##### Voir aussi

C’est un cas spécial de la règle selon laquelle [les fonctions d’assistance doivent être définies dans le même espace de noms que leur classe](#rc-helper).

##### Application

* Signaler les définitions d’opérateurs qui ne sont pas dans l’espace de noms de leurs opérandes.

### <a name="ro-lambda"></a>C.170 : Si vous avez envie de surcharger un lambda, utilisez un lambda générique

##### Raison

Vous ne pouvez pas surcharger en définissant deux lambdas différentes avec le même nom.

##### Exemple

    void f(int);
    void f(double);
    auto f = [](char);   // erreur : impossible de surcharger variable et fonction

    auto g = [](int) { /* … */ };
    auto g = [](double) { /* … */ };   // erreur : impossible de surcharger variables

    auto h = [](auto) { /* … */ };   // OK

##### Application

Le compilateur capture déjà les tentatives de surcharge d’un lambda.

## <a name="ss-union"></a>C.union : Unions

Une `union` est une `struct` dont tous les membres commencent à la même adresse, de sorte qu’elle ne peut contenir qu’un seul membre à la fois. Une `union` ne suit pas quel membre est stocké, donc le programmeur doit s’en charger ; cela est intrinsèquement sujet aux erreurs, mais il existe des moyens de compenser.

Un type qui est une `union` plus un indicateur du membre actuellement stocké s’appelle **union discriminée**, **union étiquetée**, ou **variant**.

Résumé des règles d’union :

* [C.180 : Utiliser les `union`s pour économiser de la mémoire](#ru-union)
* [C.181 : Éviter les « naked `union`s »](#ru-naked)
* [C.182 : Utiliser les `union`s anonymes pour implémenter les unions étiquetées](#ru-anonymous)
* [C.183 : Ne pas utiliser une `union` pour le type‑punning](#ru-pun)
* ???

### <a name="ru-union"></a>C.180 : Utiliser les `union`s pour économiser de la mémoire

##### Raison

Une `union` permet d’utiliser un même morceau de mémoire pour différents objets à des moments différents. Par conséquent, on peut économiser de la mémoire lorsqu’on a plusieurs objets qui ne sont jamais utilisés simultanément.

##### Exemple

    union Value {
        int    x;
        double d;
    };

    Value v = { 123 };  // maintenant v détient un int
    cout << v.x << '\n';    // écrit 123
    v.d = 987.654;  // maintenant v détient un double
    cout << v.d << '\n';    // écrit 987.654

Mais attention : [Éviter les « naked `union`s »](#ru-naked)

##### Exemple

    // Optimisation de chaîne courte

    constexpr size_t buffer_size = 16; // Légèrement plus grande que la taille d’un pointeur

    class Immutable_string {
    public:
        Immutable_string(const char* str) :
            size(strlen(str))
        {
            if (size < buffer_size)
                strcpy_s(string_buffer, buffer_size, str);
            else {
                string_ptr = new char[size + 1];
                strcpy_s(string_ptr, size + 1, str);
            }
        }

        ~Immutable_string()
        {
            if (size >= buffer_size)
                delete[] string_ptr;
        }

        const char* get_str() const
        {
            return (size < buffer_size) ? string_buffer : string_ptr;
        }

    private:
        // Si la chaîne est assez courte, on stocke la chaîne elle‑même
        // au lieu d’un pointeur vers la chaîne.
        union {
            char*  string_ptr;
            char   string_buffer[buffer_size];
        };

        const size_t size;
    };

Mais gardez à l’esprit la mise en garde : [Éviter les « naked `union`s »](#ru-naked)

##### Application

???

### <a name="ru-naked"></a>C.181 : Éviter les « naked `union`s »

##### Raison

Une *naked union* est une union sans indicateur associé indiquant quel membre (le cas échéant) elle détient, de sorte que le programmeur doive s’en souvenir. Les naked unions sont une source d’erreurs de type.

##### Exemple, mauvais

    union Value {
        int    x;
        double d;
    };

    Value v;
    v.d = 987.654;  // v détient un double

    // jusqu’ici tout va bien, mais on peut facilement mal utiliser l’union :

    cout << v.x << '\n';    // MAUVAIS, comportement indéfini : v détient un double, mais on le lit comme un int

Notez que l’erreur de type s’est produite sans aucun cast explicite. Lorsque nous avons testé ce programme, la dernière valeur affichée était `1683627180`, c’est‑à‑dire le entier correspondant au motif binaire de `987.654`. C’est une erreur de type « invisible » qui semble innocente.

Et, pour parler d’« invisible », ce code n’a donné aucune sortie :

    v.x = 123;
    cout << v.d << '\n';    // MAUVAIS : comportement indéfini

##### Alternative

Encapsuler une `union` dans une classe avec un champ de type :

Le type `variant` de C++17 (dans `<variant>`) le fait pour vous :

    variant<int, double> v;
    v = 123;        // v détient un int
    int x = get<int>(v);
    v = 123.456;    // v détient un double
    double w = get<double>(v);

##### Application

???

### <a name="ru-anonymous"></a>C.182 : Utiliser les `union`s anonymes pour implémenter des unions étiquetées

##### Raison

Une union étiquetée bien conçue est sûre du point de vue du type. Une *union anonyme* simplifie la définition d’une classe avec une paire (`tag`, `union`).

##### Exemple

Cet exemple est en grande partie tiré de TC++PL4, pp. 216‑218. Vous y trouverez une explication.

Le code est assez élaboré. Gérer un type avec un constructeur, un assignement et un destructeur définis est délicat. Sauver les programmeurs de devoir écrire ce code est une des raisons d’inclure `variant` dans la bibliothèque standard.

    class Value { // deux représentations alternatives représentées sous forme d’une union
    private:
        enum class Tag { number, text };
        Tag type; // discriminant

        union { // représentation (note : union anonyme)
            int    i;
            string s; // string possède un constructeur par défaut, des opérations de copie et un destructeur
        };
    public:
        struct Bad_entry { }; // utilisé pour les exceptions

        ~Value();
        Value& operator=(const Value&);   // nécessaire à cause du string
        Value(const Value&);
        // …
        int    number() const;
        string text() const;

        void set_number(int n);
        void set_text(const string&);
        // …
    };

    int Value::number() const
    {
        if (type != Tag::number) throw Bad_entry{};
        return i;
    }

    string Value::text() const
    {
        if (type != Tag::text) throw Bad_entry{};
        return s;
    }

    void Value::set_number(int n)
    {
        if (type == Tag::text) {
            s.~string();      // détruire explicitement string
            type = Tag::number;
        }
        i = n;
    }

    void Value::set_text(const string& ss)
    {
        if (type == Tag::text)
            s = ss;
        else {
            new(&s) string{ss};   // placement new : construction explicite de string
            type = Tag::text;
        }
    }

    Value& Value::operator=(const Value& e)   // nécessaire à cause du string
    {
        if (type == Tag::text && e.type == Tag::text) {
            s = e.s;    // assignement habituel de string
            return *this;
        }

        if (type == Tag::text) s.~string(); // destruction explicite

        switch (e.type) {
        case Tag::number:
            i = e.i;
            break;
        case Tag::text:
            new(&s) string(e.s);   // placement new : construction explicite
        }

        type = e.type;
        return *this;
    }

    Value::~Value()
    {
        if (type == Tag::text) s.~string(); // destruction explicite
    }

##### Application

???

### <a name="ru-pun"></a>C.183 : Ne pas utiliser une `union` pour le type‑punning

##### Raison

Il est comportement indéfini de lire un membre d’une `union` avec un type différent de celui avec lequel il a été écrit. Un tel *type‑punning* est invisible, ou du moins plus difficile à repérer qu’un cast nommé. Le type‑punning via `union` est une source d’erreurs.

##### Exemple, mauvais

    union Pun {
        int               x;
        unsigned char c[sizeof(int)];
    };

L’idée de `Pun` est de pouvoir examiner la représentation `char` d’un `int`.

    void bad(Pun& u)
    {
        u.x = 'x';
        cout << u.c[0] << '\n';     // comportement indéfini
    }

Si vous voulez voir les octets d’un `int`, utilisez un cast nommé :

    void if_you_must_pun(int& x)
    {
        auto p = reinterpret_cast<std::byte*>(&x);
        cout << to_integer<unsigned>(p[0]) << '\n'; // OK ; mieux
        // …
    }

Accéder au résultat d’un `reinterpret_cast` depuis le type déclaré vers `char*`, `unsigned char*` ou `std::byte*` est un comportement défini. (L’usage de `reinterpret_cast` est découragé, mais au moins on voit clairement qu’il s’agit d’une opération délicate.)

##### Remarque

Malheureusement, les `union`s sont couramment utilisées pour le type‑punning. Nous ne considérons pas « parfois, ça fonctionne comme prévu » comme un argument concluant.

Le C++ moderne introduit `std::byte` (C++17) et `std::bit_cast` (C++20) pour faciliter les opérations sur les représentations brutes d’un objet. Utilisez `reinterpret_cast` avec `std::byte` plutôt que `unsigned char` ou `char` pour ces opérations.

##### Application

???
