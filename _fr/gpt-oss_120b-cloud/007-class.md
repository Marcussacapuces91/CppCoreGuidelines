# <a name="s-class"></a>C : Classes et hiérarchies de classes

Une classe est un type défini par l'utilisateur, pour lequel un programmeur peut définir la représentation, les opérations et les interfaces. Les hiérarchies de classes sont utilisées pour organiser les classes liées en structures hiérarchiques.

## Résumé des règles de classe :

* [C.1 : Organiser les données liées dans des structures (`struct`s ou `class`s)](007-class.md#rc-org)
* [C.2 : Utiliser `class` si la classe possède une invariant ; utiliser `struct` si les membres de données peuvent varier indépendamment](007-class.md#rc-struct)
* [C.3 : Représenter la distinction entre une interface et une implémentation à l'aide d'une classe](007-class.md#rc-interface)
* [C.4 : Faire d'une fonction un membre uniquement si elle a besoin d'un accès direct à la représentation d'une classe](007-class.md#rc-member)
* [C.5 : Placer les fonctions auxiliaires dans le même espace de noms que la classe qu'elles soutiennent](007-class.md#rc-helper)
* [C.7 : Ne pas définir une classe ou une énumération et déclarer une variable de son type dans la même instruction](007-class.md#rc-standalone)
* [C.8 : Utiliser `class` plutôt que `struct` si un membre est non public](007-class.md#rc-class)
* [C.9 : Minimiser l'exposition des membres](007-class.md#rc-private)

## Sous‑sections :

* [C.concrete : Types concrets](007-class.md#ss-concrete)
* [C.ctor : Constructeurs, assignations et destructeurs](007-class.md)
* [C.con : Conteneurs et autres gestionnaires de ressources](007-class.md#ss-containers)
* [C.lambdas : Objets fonctionnels et lambdas](007-class.md#ss-lambdas)
* [C.hier : Hiérarchies de classes (POO)](007-class.md#ss-hier)
* [C.over : Surcharge et opérateurs surchargés](007-class.md#ss-overload)
* [C.union : Unions](007-class.md#ss-union)

### <a name="rc-org"></a>C.1 : Organiser les données liées dans des structures (`struct`s ou `class`s)

##### Raison

Facilité de compréhension.  
Si les données sont liées (pour des raisons fondamentales), ce fait doit être reflété dans le code.

##### Exemple

    void draw(int x, int y, int x2, int y2);  // BAD : relations implicites inutiles
    void draw(Point from, Point to);          // meilleur

##### Note

Une classe simple sans fonctions virtuelles n'implique aucun surcoût en espace ou en temps.

##### Note

Du point de vue du langage, `class` et `struct` ne diffèrent que par la visibilité par défaut de leurs membres.

##### Application

Probablement impossible. Peut-être une heuristique cherchant des éléments de données utilisés ensemble est possible.

### <a name="rc-struct"></a>C.2 : Utiliser `class` si la classe possède une invariant ; utiliser `struct` si les membres de données peuvent varier indépendamment

##### Raison

Lisibilité. Facilité de compréhension. L'utilisation de `class` alerte le programmeur sur la nécessité d'une invariant. C'est une convention utile.

##### Note

Une invariant est une condition logique pour les membres d'un objet qu'un constructeur doit établir afin que les fonctions membres publiques puissent en tenir compte. Après l'établissement de l'invariant (généralement par un constructeur), chaque fonction membre peut être appelée pour l'objet. Une invariant peut être exprimée de façon informelle (par exemple, dans un commentaire) ou plus formellement en utilisant `Expects`. Si tous les membres de données peuvent varier indépendamment les uns des autres, aucune invariant n'est possible.

##### Exemple

    struct Pair {  // the members can vary independently
        string name;
        int volume;
    };

but:

    class Date {
    public:
        // validate that {yy, mm, dd} is a valid date and initialize
        Date(int yy, Month mm, char dd);
        // ...
    private:
        int y;
        Month m;
        char d;    // day
    };

##### Note

Si une classe possède des données `private`, un utilisateur ne peut pas initialiser complètement un objet sans l'utilisation d'un constructeur. Ainsi, le concepteur de la classe fournira un constructeur et devra en spécifier le sens. Cela signifie effectivement que le concepteur doit définir une invariant.

**Voir aussi** :

* [définir une classe avec des données privées comme `class`](007-class.md#rc-class)
* [Préférer placer l'interface en premier dans une classe](024-naming.md#rl-order)
* [minimiser l'exposition des membres](007-class.md#rc-private)
* [Éviter les données `protected`](007-class.md#rh-protected)

##### Application

Rechercher les `struct`s dont toutes les données sont privées et les `class`es avec des membres publics.

### <a name="rc-interface"></a>C.3 : Représenter la distinction entre une interface et une implémentation à l'aide d'une classe

##### Raison

Une distinction explicite entre interface et implémentation améliore la lisibilité et simplifie la maintenance.

##### Exemple

    class Date {
    public:
        Date();
        // validate that {yy, mm, dd} is a valid date and initialize
        Date(int yy, Month mm, char dd);

        int day() const;
        Month month() const;
        // ...
    private:
        // ... some representation ...
    };

Par exemple, nous pouvons maintenant changer la représentation d'un `Date` sans affecter ses utilisateurs (une recompilation est probable, toutefois).

##### Note

Utiliser une classe de cette manière pour représenter la distinction entre interface et implémentation n'est bien sûr pas la seule façon. Par exemple, nous pouvons utiliser un ensemble de déclarations de fonctions autonomes dans un espace de noms, une classe de base abstraite, ou un modèle de fonction avec des concepts pour représenter une interface. La question la plus importante est de distinguer explicitement entre une interface et les « détails » de son implémentation. Idéalement, et généralement, une interface est bien plus stable que ses implémentations.

##### Application

???

### <a name="rc-member"></a>C.4 : Faire d'une fonction un membre uniquement si elle a besoin d'un accès direct à la représentation d'une classe

##### Raison

Moins d'accouplement qu'avec des fonctions membres, moins de fonctions susceptibles de causer des problèmes en modifiant l'état d'un objet, réduit le nombre de fonctions qui doivent être modifiées après un changement de représentation.

##### Exemple

    class Date {
        // ... relatively small interface ...
    };

    // helper functions:
    Date next_weekday(Date);
    bool operator==(Date, Date);

Les « fonctions auxiliaires » n'ont pas besoin d'un accès direct à la représentation d'un `Date`.

##### Note

Cette règle devient encore meilleure si C++ obtient le ["appel de fonction uniforme"](https://www.open-std.org/jtc1/sc22/wg21/docs/papers/2016/p0251r0.pdf).

##### Exception

Le langage exige que les fonctions `virtual` soient des membres, et toutes les fonctions `virtual` n'accèdent pas directement aux données. En particulier, les membres d'une classe abstraite le font rarement.

> Note : [multi‑methods](https://web.archive.org/web/20200605021759/https://parasol.tamu.edu/~yuriys/papers/OMM10.pdf).

##### Exception

Le langage exige que les opérateurs `=`, `()`, `[]` et `->` soient des membres.

##### Exception

Un ensemble de surcharges peut contenir certains membres qui n'accèdent pas directement aux données `private` :

    class Foobar {
    public:
        void foo(long x) { /* manipulate private data */ }
        void foo(double x) { foo(std::lround(x)); }
        // ...
    private:
        // ...
    };

##### Exception

De même, un ensemble de fonctions peut être conçu pour être utilisé en chaîne :

    x.scale(0.5).rotate(45).set_color(Color::red);

Typiquement, certaines mais pas toutes ces fonctions accèdent directement aux données `private`.

##### Application

* Rechercher les fonctions membres non‑`virtual` qui ne touchent pas directement les membres de données. Le problème est que de nombreuses fonctions membres qui n'ont pas besoin de toucher directement les membres de données le font.
* Ignorer les fonctions `virtual`.
* Ignorer les fonctions qui font partie d'un ensemble de surcharge dont au moins une fonction accède aux membres `private`.
* Ignorer les fonctions retournant `this`.

### <a name="rc-helper"></a>C.5 : Placer les fonctions auxiliaires dans le même espace de noms que la classe qu'elles soutiennent

##### Raison

Une fonction auxiliaire est une fonction (généralement fournie par le créateur d'une classe) qui n'a pas besoin d'un accès direct à la représentation de la classe, mais qui est considérée comme faisant partie de l'interface utile de la classe. Les placer dans le même espace de noms que la classe rend leur relation avec la classe évidente et permet de les trouver via la recherche dépendante des arguments (ADL).

##### Exemple

    namespace Chrono { // ici nous conservons les services liés au temps

        class Time { /* ... */ };
        class Date { /* ... */ };

        // helper functions:
        bool operator==(Date, Date);
        Date next_weekday(Date);
        // ...
    }

##### Note

Ceci est particulièrement important pour les [opérateurs surchargés](007-class.md#ro-namespace).

##### Application

* Signaler les fonctions globales prenant des types d'argument provenant d'un seul espace de noms.

### <a name="rc-standalone"></a>C.7 : Ne pas définir une classe ou une énumération et déclarer une variable de son type dans la même instruction

##### Raison

Mélanger une définition de type et la définition d'une autre entité dans la même déclaration est confus et inutile.

##### Exemple, mauvais

    struct Data { /*...*/ } data{ /*...*/ };

##### Exemple, bon

    struct Data { /*...*/ };
    Data data{ /*...*/ };

##### Application

* Signaler si le `}` d'une définition de classe ou d'énumération n'est pas suivi d'un `;`. Le `;` est manquant.

### <a name="rc-class"></a>C.8 : Utiliser `class` plutôt que `struct` si un membre est non public

##### Raison

Lisibilité. Pour rendre clair que quelque chose est caché/abstrait. C'est une convention utile.

##### Exemple, mauvais

    struct Date {
        int d, m;

        Date(int i, Month m);
        // ... lots of functions ...
    private:
        int y;  // year
    };

Il n'y a rien d'incorrect dans ce code du point de vue des règles du langage C++, mais presque tout est incorrect du point de vue de la conception. Les données privées sont cachées loin des données publiques. Les données sont réparties dans différentes parties de la déclaration de la classe. Différentes parties des données ont des accès différents. Tout cela diminue la lisibilité et complique la maintenance.

##### Note

Préférer placer l'interface en premier dans une classe, [voir NL.16](024-naming.md#rl-order).

##### Application

* Signaler les classes déclarées avec `struct` s'il existe un membre `private` ou `protected`.

### <a name="rc-private"></a>C.9 : Minimiser l'exposition des membres

##### Raison

Encapsulation. Masquage de l'information. Minimiser le risque d'accès non intentionnel. Cela simplifie la maintenance.

##### Exemple

    template<typename T, typename U>
    struct pair {
        T a;
        U b;
        // ...
    };

Quoi que nous fassions dans la partie `//`, un utilisateur arbitraire d'un `pair` peut modifier arbitrairement et indépendamment ses `a` et `b`. Dans une grande base de code, il est difficile de savoir quel code agit sur les membres de `pair`. Cela peut être exactement ce que nous voulons, mais si nous voulons imposer une relation entre les membres, nous devons les rendre `private` et faire respecter cette relation (invariant) via les constructeurs et les fonctions membres. Par exemple :

    class Distance {
    public:
        // ...
        double meters() const { return magnitude*unit; }
        void set_unit(double u)
        {
                // ... check that u is a factor of 10 ...
                // ... change magnitude appropriately ...
                unit = u;
        }
        // ...
    private:
        double magnitude;
        double unit;    // 1 is meters, 1000 is kilometers, 0.001 is millimeters, etc.
    };

##### Note

Si l'ensemble des utilisateurs directs d'un ensemble de variables ne peut pas être déterminé facilement, le type ou l'utilisation de cet ensemble ne peut pas être (facilement) modifié/amélioré. Pour les données `public` et `protected`, c'est généralement le cas.

##### Exemple

Une classe peut fournir deux interfaces à ses utilisateurs. L'une pour les classes dérivées (`protected`) et l'autre pour les utilisateurs généraux (`public`). Par exemple, une classe dérivée pourrait être autorisée à ignorer une vérification d'exécution parce qu'elle a déjà garanti la correction :

    class Foo {
    public:
        int bar(int x) { check(x); return do_bar(x); }
        // ...
    protected:
        int do_bar(int x); // do some operation on the data
        // ...
    private:
        // ... data ...
    };

    class Dir : public Foo {
        //...
        int mem(int x, int y)
        {
            /* ... do something ... */
            return do_bar(x + y); // OK: derived class can bypass check
        }
    };

    void user(Foo& x)
    {
        int r1 = x.bar(1);      // OK, will check
        int r2 = x.do_bar(2);   // error: would bypass check
        // ...
    }

##### Note

[Les données `protected` sont une mauvaise idée](007-class.md#rh-protected).

##### Note

Préférer l'ordre `public` avant `protected` avant `private` ; voir [NL.16](024-naming.md#rl-order).

##### Application

* Signaler les données `protected`.
* Signaler les mélanges de données `public` et `private`.

## <a name="ss-concrete"></a>C.concrete : Types concrets

### Résumé des règles de type concret :

* [C.10 : Préférer les types concrets aux hiérarchies de classes](007-class.md#rc-concrete)
* [C.11 : Rendre les types concrets réguliers](007-class.md#rc-regular)
* [C.12 : Ne pas rendre les membres de données `const` ou des références dans un type copiable ou déplaçable](007-class.md#rc-constref)
* [C.13 : Si le membre de données `B` utilise un autre membre de données `A`, déclarer `A` avant `B`](007-class.md#rc-lifetime)

### <a name="rc-concrete"></a>C.10 : Préférer les types concrets aux hiérarchies de classes

##### Raison

Un type concret est fondamentalement plus simple qu'un type dans une hiérarchie de classes : plus facile à concevoir, à implémenter, à utiliser, à raisonner, plus petit et plus rapide. Vous avez besoin d'une raison (cas d'utilisation) pour utiliser une hiérarchie.

##### Exemple

    class Point1 {
        int x, y;
        // ... operations ...
        // ... no virtual functions ...
    };

    class Point2 {
        int x, y;
        // ... operations, some virtual ...
        virtual ~Point2();
    };

    void use()
    {
        Point1 p11 {1, 2};   // make an object on the stack
        Point1 p12 {p11};    // a copy

        auto p21 = make_unique<Point2>(1, 2);   // make an object on the free store
        auto p22 = p21->clone();                // make a copy
        // ...
    }

Si une classe fait partie d'une hiérarchie, nous (dans le code réel, même si ce n'est pas toujours le cas dans de petits exemples) devons manipuler ses objets via des pointeurs ou des références. Cela implique plus de surcharge mémoire, plus d'allocations et de désallocations, et plus de surcharge d'exécution pour gérer les indirections résultantes.

##### Note

Les types concrets peuvent être alloués sur la pile et être membres d'autres classes.

##### Note

L'utilisation d'indirection est fondamentale pour les interfaces polymorphes à l'exécution. La surcharge d'allocation/désallocation n'est pas (c'est juste le cas le plus courant). Nous pouvons utiliser une classe de base comme interface d'un objet à portée d'une classe dérivée. Cela se fait là où l'allocation dynamique est interdite (par ex. temps réel strict) et pour fournir une interface stable à certains types de plug‑ins.

##### Application

???

### <a name="rc-regular"></a>C.11 : Rendre les types concrets réguliers

##### Raison

Les types réguliers sont plus faciles à comprendre et à raisonner que les types qui ne le sont pas (les irrégularités nécessitent un effort supplémentaire pour être compris et utilisés). Les types intégrés de C++ sont réguliers, tout comme les classes de la bibliothèque standard telles que `string`, `vector` et `map`. Les classes concrètes sans assignation et égalité peuvent être définies, mais elles sont (et devraient être) rares.

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

En particulier, si un type concret est copiable, il est préférable de lui fournir également un opérateur de comparaison d'égalité, et de s'assurer que `a = b` implique `a == b`.

##### Note

Pour les `struct` destinés à être partagés avec du code C, définir `operator==` peut ne pas être faisable.

##### Note

Les gestionnaires de ressources qui ne peuvent pas être clonés, par ex. un `scoped_lock` pour un `mutex`, sont des types concrets mais ne peuvent généralement pas être copiés (à la place, ils peuvent généralement être déplacés), ils ne peuvent donc pas être réguliers ; ils tendent à être uniquement déplaçables.

##### Application

???

### <a name="rc-constref"></a>C.12 : Ne pas rendre les membres de données `const` ou des références dans un type copiable ou déplaçable

##### Raison

Les membres de données `const` et les références ne sont pas utiles dans un type copiable ou déplaçable, et rendent ces types difficiles à utiliser en les rendant au moins partiellement non copiable/non déplaçable pour des raisons subtiles.

##### Exemple ; mauvais

    class bad {
        const int i;    // bad
        string& s;      // bad
        // ...
    };

Les membres de données `const` et `&` rendent cette classe « seulement à moitié copiable » — constructible par copie mais non assignable par copie.

##### Note

Si vous avez besoin qu'un membre pointe vers quelque chose, utilisez un pointeur (brut ou intelligent, et `gsl::not_null` s'il ne doit pas être nul) au lieu d'une référence.

##### Application

Signaler un membre de données qui est `const`, `&` ou `&&` dans un type qui possède une opération de copie ou de déplacement.

### <a name="rc-lifetime"></a>C.13 : Si le membre de données `B` utilise un autre membre de données `A`, déclarer `A` avant `B`

##### Raison

Les membres de données sont initialisés dans l'ordre de leur déclaration, et détruits dans l'ordre inverse.

##### Discussion

Si le membre de données `B` utilise un autre membre de données `A`, alors `A` doit être déclaré avant `B` afin que `A` survive plus longtemps que `B`, c'est‑à‑dire que la durée de vie de `A` commence avant et se termine après celle de `B`. Sinon, pendant la construction et la destruction, `B` tentera d'utiliser `A` en dehors de sa durée de vie.

##### Exemple ; mauvais

    // Bad: b uses a, but a is declared after b.
    //      Construction order is b then a; destruction order is a then b.
    //      So b touches a outside the lifetime of a.

    class X {
        struct B {
            string* p;
            explicit B(string& a) : p{&a} {}
            ~B() { cout << *p; }                       // uses a (via p)
        };

        B      b;                                      // constructed first
        string a = "some heap allocated string value"; // constructed after b; destroyed before b

    public:
        X() : b{a} {}   // uses a before it is constructed -> use-before-alloc UB
        ~X() = default; // accesses a after it is destroyed -> use-after-free UB
    };

##### Exemple ; bon

    // Corrected: Just declare a before b

    class X {
        struct B {
            string* p;
            explicit B(string& a) : p{&a} {}
            ~B() { cout << *p; }                       // uses a (via p)
        };

        string a = "some heap allocated string value"; // constructed before b; destroyed after b
        B      b;                                      // constructed second

    public:
        X() : b{a} {}   // ok
        ~X() = default; // ok
    };

##### Exemple ; mauvais

Cela peut également se produire avec la concurrence. Assurez‑vous qu'une opération asynchrone qui accède à une valeur soit jointe avant que la valeur qu'elle accède ne soit détruite.

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

##### Exemple ; bon

    // Corrected: Just declare a before b

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

* Signaler un initialiseur de membre qui fait référence à un objet avant qu'il ne soit construit.

## <a name="s-ctor"></a>C.ctor : Constructeurs, assignations et destructeurs

Ces fonctions contrôlent le cycle de vie des objets : création, copie, déplacement et destruction. Définissez les constructeurs pour garantir et simplifier l'initialisation des classes.

Ce sont les *opérations par défaut* :

* un constructeur par défaut : `X()`
* un constructeur de copie : `X(const X&)`
* une assignation de copie : `operator=(const X&)`
* un constructeur de déplacement : `X(X&&)`
* une assignation de déplacement : `operator=(X&&)`
* un destructeur : `~X()`

Par défaut, le compilateur définit chacune de ces opérations si elle est utilisée, mais le comportement par défaut peut être supprimé.

Les opérations par défaut sont un ensemble d'opérations liées qui implémentent ensemble la sémantique du cycle de vie d'un objet. Par défaut, C++ traite les classes comme des types de valeur, mais tous les types ne sont pas de type valeur.

### Règles concernant l'ensemble des opérations par défaut :

* [C.20 : Si vous pouvez éviter de définir des opérations par défaut, ne le faites pas](007-class.md#rc-zero)
* [C.21 : Si vous définissez ou `=delete` une fonction de copie, de déplacement ou de destructeur, définissez ou `=delete` toutes les fonctions correspondantes](007-class.md#rc-five)
* [C.22 : Rendre les opérations par défaut cohérentes](007-class.md#rc-matched)

### Règles du destructeur :

* [C.30 : Définir un destructeur si une classe a besoin d'une action explicite à la destruction de l'objet](007-class.md#rc-dtor)
* [C.31 : Toutes les ressources acquises par une classe doivent être libérées par le destructeur de la classe](007-class.md#rc-dtor-release)
* [C.32 : Si une classe possède un pointeur brut (`T*`) ou une référence (`T&`), considérer si elle peut être propriétaire](007-class.md#rc-dtor-ptr)
* [C.33 : Si une classe possède un membre pointeur propriétaire, définir un destructeur](007-class.md#rc-dtor-ptr2)
* [C.35 : Le destructeur d'une classe de base doit être soit public et virtuel, soit protégé et non virtuel](007-class.md#rc-dtor-virtual)
* [C.36 : Un destructeur ne doit pas échouer](007-class.md#rc-dtor-fail)
* [C.37 : Rendre les destructeurs `noexcept`](007-class.md#rc-dtor-noexcept)

### Règles du constructeur :

* [C.40 : Définir un constructeur si une classe possède une invariant](007-class.md#rc-ctor)
* [C.41 : Un constructeur doit créer un objet entièrement initialisé](007-class.md#rc-complete)
* [C.42 : Si un constructeur ne peut pas construire un objet valide, lancer une exception](007-class.md#rc-throw)
* [C.43 : S'assurer qu'une classe copiable possède un constructeur par défaut](007-class.md#rc-default0)
* [C.44 : Préférer que les constructeurs par défaut soient simples et ne lèvent pas d'exception](007-class.md#rc-default00)
* [C.45 : Ne pas définir un constructeur par défaut qui ne fait qu'initialiser les membres de données ; utiliser des initialiseurs de membres par défaut à la place](007-class.md#rc-default)
* [C.46 : Par défaut, déclarer les constructeurs à un seul argument `explicit`](007-class.md#rc-explicit)
* [C.47 : Définir et initialiser les membres de données dans l'ordre de leur déclaration](007-class.md#rc-order)
* [C.48 : Préférer les initialiseurs de membres par défaut aux initialiseurs de membres dans les constructeurs pour les initialiseurs constants](007-class.md#rc-in-class-initializer)
* [C.49 : Préférer l'initialisation à l'assignation dans les constructeurs](007-class.md#rc-initialize)
* [C.50 : Utiliser une fonction fabrique si vous avez besoin d'un « comportement virtuel » pendant l'initialisation](007-class.md#rc-factory)
* [C.51 : Utiliser des constructeurs délégués pour représenter des actions communes à tous les constructeurs d'une classe](007-class.md#rc-delegating)
* [C.52 : Utiliser les constructeurs hérités pour importer les constructeurs dans une classe dérivée qui n'a pas besoin d'une initialisation explicite supplémentaire](007-class.md#rc-inheriting)

### Règles de copie et de déplacement :

* [C.60 : Rendre l'assignation de copie non‑`virtual`, prendre le paramètre par `const&` et retourner par non‑`const&`](007-class.md#rc-copy-assignment)
* [C.61 : Une opération de copie doit copier](007-class.md#rc-copy-semantic)
* [C.62 : Rendre l'assignation de copie sûre pour l'auto‑assignation](007-class.md#rc-copy-self)
* [C.63 : Rendre l'assignation de déplacement non‑`virtual`, prendre le paramètre par `&&` et retourner par non‑`const&`](007-class.md#rc-move-assignment)
* [C.64 : Une opération de déplacement doit déplacer et laisser sa source dans un état valide](007-class.md#rc-move-semantic)
* [C.65 : Rendre l'assignation de déplacement sûre pour l'auto‑assignation](007-class.md#rc-move-self)
* [C.66 : Rendre les opérations de déplacement `noexcept`](007-class.md#rc-move-noexcept)
* [C.67 : Une classe polymorphe doit supprimer les copies/déplacements publics](007-class.md#rc-copy-virtual)

### Autres règles concernant les opérations par défaut :

* [C.80 : Utiliser `=default` si vous devez être explicite sur l'utilisation de la sémantique par défaut](007-class.md#rc-eqdefault)
* [C.81 : Utiliser `=delete` lorsque vous voulez désactiver le comportement par défaut (sans vouloir une alternative)](007-class.md#rc-delete)
* [C.82 : Ne pas appeler de fonctions virtuelles dans les constructeurs et les destructeurs](007-class.md#rc-ctor-virtual)
* [C.83 : Pour les types de valeur, envisager de fournir une fonction `swap` `noexcept`](007-class.md#rc-swap)
* [C.84 : Un `swap` ne doit pas échouer](007-class.md#rc-swap-fail)
* [C.85 : Rendre le `swap` `noexcept`](007-class.md#rc-swap-noexcept)
* [C.86 : Rendre `==` symétrique par rapport aux types d'opérandes et `noexcept`](007-class.md#rc-eq)
* [C.87 : Se méfier de `==` sur les classes de base](007-class.md#rc-eq-base)
* [C.89 : Rendre un `hash` `noexcept`](007-class.md#rc-hash)
* [C.90 : S'appuyer sur les constructeurs et les opérateurs d'assignation, pas sur `memset` et `memcpy`](007-class.md#rc-memset)

## <a name="ss-defop"></a>C.defop : Opérations par défaut

Par défaut, le langage fournit les opérations par défaut avec leurs sémantiques par défaut. Cependant, un programmeur peut désactiver ou remplacer ces comportements par défaut.

### <a name="rc-zero"></a>C.20 : Si vous pouvez éviter de définir des opérations par défaut, ne le faites pas

##### Raison

C'est le plus simple et cela donne les sémantiques les plus propres.

##### Exemple

    struct Named_map {
    public:
        explicit Named_map(const string& n) : name(n) {}
        // no copy/move constructors
        // no copy/move assignment operators
        // no destructor
    private:
        string name;
        map<int, int> rep;
    };

    Named_map nm("map"); // construct
    Named_map nm2 {nm};  // copy construct

Comme `std::map` et `string` possèdent toutes les fonctions spéciales, aucun travail supplémentaire n'est nécessaire.

##### Note

Ceci est connu sous le nom de « règle du zéro ».

##### Application

(Non applicable) Bien que non applicable, un bon analyseur statique peut détecter des motifs indiquant une amélioration possible pour respecter cette règle. Par exemple, une classe avec une paire de membres (pointeur, taille) et un destructeur qui `delete` le pointeur pourrait probablement être convertie en `vector`.

### <a name="rc-five"></a>C.21 : Si vous définissez ou `=delete` une fonction de copie, de déplacement ou de destructeur, définissez ou `=delete` toutes les fonctions correspondantes

##### Raison

Les sémantiques de copie, de déplacement et de destruction sont étroitement liées, donc si l'une doit être déclarée, il est probable que les autres nécessitent également une considération.

Déclarer toute fonction de copie/déplacement/destructeur,
même en tant que `=default` ou `=delete`, supprime la déclaration implicite
d'un constructeur de déplacement et d'un opérateur d'assignation de déplacement.
Déclarer un constructeur de déplacement ou un opérateur d'assignation de déplacement, même en tant que
`=default` ou `=delete`, entraînera la définition implicite d'un constructeur de copie
ou d'un opérateur d'assignation de copie comme étant supprimé.
Ainsi, dès que l'une de ces fonctions est déclarée, les autres doivent
être toutes déclarées pour éviter des effets indésirables comme transformer tous les déplacements potentiels en copies plus coûteuses, ou rendre une classe uniquement déplaçable.

##### Exemple, mauvais

    struct M2 {   // bad: incomplete set of copy/move/destructor operations
    public:
        // ...
        // ... no copy or move operations ...
        ~M2() { delete[] rep; }
    private:
        pair<int, int>* rep;  // zero-terminated set of pairs
    };

    void use()
    {
        M2 x;
        M2 y;
        // ...
        x = y;   // the default assignment
        // ...
    }

Étant donné que « attention spéciale » était nécessaire pour le destructeur (ici, pour désallouer), la probabilité que les opérateurs d'assignation de copie et de déplacement implicites soient corrects est faible (ici, nous aurions une double suppression).

##### Note

Ceci est connu sous le nom de « règle des cinq ».

##### Note

Si vous voulez une implémentation par défaut (tout en définissant une autre), écrivez `=default` pour montrer que vous le faites intentionnellement pour cette fonction. Si vous ne voulez pas d'une fonction par défaut générée, supprimez‑la avec `=delete`.

##### Exemple, bon

Lorsque le destructeur doit être déclaré simplement pour le rendre `virtual`, il peut être
défini comme par défaut.

    class AbstractBase {
    public:
        virtual void foo() = 0;  // at least one abstract method to make the class abstract
        virtual ~AbstractBase() = default;
        // ...
    };

Pour empêcher le slicing conformément à [C.67](007-class.md#rc-copy-virtual),
rendre les opérations de copie protégées ou `=delete`es, et ajouter un `clone` :

    class CloneableBase {
    public:
        virtual unique_ptr<CloneableBase> clone() const;
        virtual ~CloneableBase() = default;
        CloneableBase() = default;
        CloneableBase(const CloneableBase&) = delete;
        CloneableBase& operator=(const CloneableBase&) = delete;
        CloneableBase(CloneableBase&&) = delete;
        CloneableBase& operator=(CloneableBase&&) = delete;
        // ... other constructors and functions ...
    };

Définir uniquement les opérations de déplacement ou uniquement les opérations de copie aurait le même effet ici, mais déclarer explicitement l'intention pour chaque fonction spéciale la rend plus évidente pour le lecteur.

##### Note

Les compilateurs imposent une grande partie de cette règle et, idéalement, avertissent de toute violation.

##### Note

S'appuyer sur une opération de copie implicite dans une classe avec un destructeur est obsolète.

##### Note

Écrire ces fonctions peut être source d'erreurs.
Notez leurs types d'argument :

    class X {
    public:
        // ...
        virtual ~X() = default;               // destructor (virtual if X is meant to be a base class)
        X(const X&) = default;                // copy constructor
        X& operator=(const X&) = default;     // copy assignment
        X(X&&) noexcept = default;            // move constructor
        X& operator=(X&&) noexcept = default; // move assignment
    };

Une petite erreur (comme une faute de frappe, l'oubli d'un `const`, l'utilisation de `&` au lieu de `&&`, ou l'oubli d'une fonction spéciale) peut entraîner des erreurs ou des avertissements.
Pour éviter la fastidiosité et la possibilité d'erreurs, essayez de suivre la [règle du zéro](007-class.md#rc-zero).

##### Application

(Un simple) Une classe devrait avoir une déclaration (même `=delete`) pour soit toutes, soit aucune des fonctions de copie/déplacement/destructeur.

### <a name="rc-matched"></a>C.22 : Rendre les opérations par défaut cohérentes

##### Raison

Les opérations par défaut sont conceptuellement un ensemble assorti. Leurs sémantiques sont interconnectées. Les utilisateurs seront surpris si la construction/copiedéplacement et l'assignation de copie/déplacement font logiquement des choses différentes. Les utilisateurs seront surpris si les constructeurs et destructeurs ne fournissent pas une vue cohérente de la gestion des ressources. Les utilisateurs seront surpris si la copie et le déplacement ne reflètent pas la façon dont les constructeurs et destructeurs fonctionnent.

##### Exemple, mauvais

    class Silly {   // BAD: Inconsistent copy operations
        class Impl {
            // ...
        };
        shared_ptr<Impl> p;
    public:
        Silly(const Silly& a) : p(make_shared<Impl>()) { *p = *a.p; }   // deep copy
        Silly& operator=(const Silly& a) { p = a.p; return *this; }   // shallow copy
        // ...
    };

Ces opérations ne sont pas d'accord sur la sémantique de copie. Cela entraînera confusion et bugs.

##### Application

* (Complexe) Un constructeur de copie/de déplacement et l'opérateur d'assignation de copie/de déplacement correspondant devraient écrire aux mêmes membres de données au même niveau de déréférencement.
* (Complexe) Tout membre écrit dans un constructeur de copie/de déplacement devrait également être initialisé par tous les autres constructeurs.
* (Complexe) Si un constructeur de copie/de déplacement effectue une copie profonde d'un membre de données, alors le destructeur devrait modifier le membre de données.
* (Complexe) Si un destructeur modifie un membre de données, ce membre de données devrait être écrit dans tout constructeur ou opérateur d'assignation de copie/de déplacement.

## <a name="ss-dtor"></a>C.dtor : Destructeurs

« Cette classe a‑t‑elle besoin d'un destructeur ? » est une question de conception étonnamment perspicace. Pour la plupart des classes, la réponse est « non » soit parce que la classe ne détient aucune ressource, soit parce que la destruction est gérée par [la règle du zéro](007-class.md#rc-zero) ; c'est‑à‑dire, ses membres peuvent s'occuper d'elles‑mêmes en ce qui concerne la destruction. Si la réponse est « oui », une grande partie de la conception de la classe suit (voir [la règle des cinq](007-class.md#rc-five)).

### <a name="rc-dtor"></a>C.30 : Définir un destructeur si une classe a besoin d'une action explicite à la destruction de l'objet

##### Raison

Un destructeur est invoqué implicitement à la fin de la durée de vie d'un objet. Si le destructeur par défaut suffit, utilisez‑le. Ne définissez un destructeur non‑par défaut que si une classe doit exécuter du code qui ne fait pas déjà partie des destructeurs de ses membres.

##### Exemple

    template<typename A>
    struct final_action {   // slightly simplified
        A act;
        final_action(A a) : act{a} {}
        ~final_action() { act(); }
    };

    template<typename A>
    final_action<A> finally(A act)   // deduce action type
    {
        return final_action<A>{act};
    }

    void test()
    {
        auto act = finally([] { cout << "Exit test\n"; });  // establish exit action
        // ...
        if (something) return;   // act done here
        // ...
    } // act done here

Le but de `final_action` est d'obtenir un morceau de code (généralement un lambda) exécuté lors de la destruction.

##### Note

Il existe deux catégories générales de classes qui ont besoin d'un destructeur défini :

* Une classe avec une ressource qui n'est pas déjà représentée comme une classe avec un destructeur, par ex. un `vector` ou une classe de transaction.
* Une classe qui existe principalement pour exécuter une action lors de la destruction, telle qu'un traceur ou `final_action`.

##### Exemple, mauvais

    class Foo {   // bad; use the default destructor
    public:
        // ...
        ~Foo() { s = ""; i = 0; vi.clear(); }  // clean up
    private:
        string s;
        int i;
        vector<int> vi;
    };

Le destructeur par défaut le fait mieux, plus efficacement, et ne peut pas se tromper.

##### Application

Rechercher les « ressources implicites », telles que les pointeurs et références. Rechercher les classes avec des destructeurs alors que tous leurs membres de données ont des destructeurs.

### <a name="rc-dtor-release"></a>C.31 : Toutes les ressources acquises par une classe doivent être libérées par le destructeur de la classe

##### Raison

Prévention des fuites de ressources, surtout en cas d'erreur.

##### Note

Pour les ressources représentées comme des classes avec un ensemble complet d'opérations par défaut, cela se produit automatiquement.

##### Exemple

    class X {
        ifstream f;   // might own a file
        // ... no default operations defined or =deleted ...
    };

`X`'s `ifstream` ferme implicitement tout fichier qu'il pourrait avoir ouvert lors de la destruction de son `X`.

##### Exemple, mauvais

    class X2 {     // bad
        FILE* f;   // might own a file
        // ... no default operations defined or =deleted ...
    };

`X2` pourrait fuir un descripteur de fichier.

##### Note

Qu'en est‑il d'une socket qui ne se ferme pas ? Un destructeur, une fermeture ou une opération de nettoyage [ne devrait jamais échouer](007-class.md#rc-dtor-fail). Si cela échoue néanmoins, nous avons un problème qui n'a pas vraiment de bonne solution. Pour commencer, l'auteur d'un destructeur ne sait pas pourquoi le destructeur est appelé et ne peut « refuser d'agir » en lançant une exception. Voir [discussion](028-discussion.md#sd-never-fail). Pour aggraver le problème, de nombreuses opérations « close/release » ne sont pas réessayables. Beaucoup ont essayé de résoudre ce problème, mais aucune solution générale n'est connue. Si possible, considérez l'échec de la fermeture/du nettoyage comme une erreur de conception fondamentale et terminez le programme.

##### Note

Une classe peut contenir des pointeurs et références vers des objets qu'elle ne possède pas. Évidemment, ces objets ne doivent pas être `delete`és par le destructeur de la classe. Par exemple :

    Preprocessor pp { /* ... */ };
    Parser p { pp, /* ... */ };
    Type_checker tc { p, /* ... */ };

Ici `p` fait référence à `pp` mais ne le possède pas.

##### Application

* (Simple) Si une classe possède des membres pointeur ou référence qui sont propriétaires (par ex. désignés comme propriétaires avec `gsl::owner`), alors ils devraient être mentionnés dans son destructeur.
* (Difficile) Déterminer si les membres pointeur ou référence sont propriétaires lorsqu'il n'y a aucune déclaration explicite de propriété (par ex. examiner les constructeurs).

### <a name="rc-dtor-ptr"></a>C.32 : Si une classe possède un pointeur brut (`T*`) ou une référence (`T&`), considérer si elle peut être propriétaire

##### Raison

Il existe beaucoup de code qui n'est pas spécifique sur la propriété.

##### Exemple

    class legacy_class
    {
        foo* m_owning;   // Bad: change to unique_ptr<T> or owner<T*>
        bar* m_observer; // OK: keep
    }

La seule façon de déterminer la propriété peut être l'analyse du code.

##### Note

La propriété doit être claire dans le nouveau code (et le code refactorisé) selon [R.20](009-resource.md#rr-owner) pour les pointeurs propriétaires et [R.3](009-resource.md#rr-ptr) pour les pointeurs non propriétaires. Les références ne devraient jamais être propriétaires [R.4](009-resource.md#rr-ref).

##### Application

Regarder l'initialisation des pointeurs membres bruts et des références membres et voir si une allocation est utilisée.

### <a name="rc-dtor-ptr2"></a>C.33 : Si une classe possède un membre pointeur propriétaire, définir un destructeur

##### Raison

Un objet possédé doit être `delete`é lors de la destruction de l'objet qui le possède.

##### Exemple

Un membre pointeur pourrait représenter une ressource.
[Un `T*` ne devrait pas le faire](009-resource.md#rr-ptr), mais dans le code hérité, c'est fréquent.
Considérez un `T*` comme un propriétaire possible et donc suspect.

    template<typename T>
    class Smart_ptr {
        T* p;   // BAD: vague about ownership of *p
        // ...
    public:
        // ... no user-defined default operations ...
    };

    void use(Smart_ptr<int> p1)
    {
        // error: p2.p leaked (if not nullptr and not owned by some other code)
        auto p2 = p1;
    }

Notez que si vous définissez un destructeur, vous devez définir ou supprimer [toutes les opérations par défaut](007-class.md#rc-five) :

    template<typename T>
    class Smart_ptr2 {
        T* p;   // BAD: vague about ownership of *p
        // ...
    public:
        // ... no user-defined copy operations ...
        ~Smart_ptr2() { delete p; }  // p is an owner!
    };

    void use(Smart_ptr2<int> p1)
    {
        auto p2 = p1;   // error: double deletion
    }

Le constructeur de copie par défaut copiera simplement `p1.p` dans `p2.p`, entraînant une double destruction de `p1.p`. Soyez explicite sur la propriété :

    template<typename T>
    class Smart_ptr3 {
        owner<T*> p;   // OK: explicit about ownership of *p
        // ...
    public:
        // ...
        // ... copy and move operations ...
        ~Smart_ptr3() { delete p; }
    };

    void use(Smart_ptr3<int> p1)
    {
        auto p2 = p1;   // OK: no double deletion
    }

##### Note

Souvent, la façon la plus simple d'obtenir un destructeur est de remplacer le pointeur par un pointeur intelligent (par ex. `std::unique_ptr`) et laisser le compilateur gérer la destruction correctement.

##### Note

Pourquoi ne pas simplement exiger que tous les pointeurs propriétaires soient des « pointeurs intelligents » ? Cela impliquerait parfois des changements de code non triviaux et pourrait affecter les ABI.

##### Application

* Une classe avec un membre pointeur est suspecte.
* Une classe avec un `owner<T>` devrait définir ses opérations par défaut.

### <a name="rc-dtor-virtual"></a>C.35 : Le destructeur d'une classe de base doit être soit public et virtuel, soit protégé et non‑virtuel

##### Raison

Éviter le comportement indéfini. Si le destructeur est public, le code appelant peut tenter de détruire un objet dérivé via un pointeur de base, et le résultat est indéfini si le destructeur de la base n'est pas virtuel. Si le destructeur est protégé, le code appelant ne peut pas détruire via un pointeur de base et le destructeur n'a pas besoin d'être virtuel ; il doit être protégé, pas privé, afin que les destructeurs dérivés puissent l'invoquer. En général, l'auteur d'une classe de base ne connaît pas l'action appropriée à effectuer lors de la destruction.

##### Discussion

Voir [cette discussion](028-discussion.md#sd-dtor).

##### Exemple, mauvais

    struct Base {  // BAD: implicitly has a public non-virtual destructor
        virtual void f();
    };

    struct D : Base {
        string s {"a resource needing cleanup"};
        ~D() { /* ... do some cleanup ... */ }
        // ...
    };

    void use()
    {
        unique_ptr<Base> p = make_unique<D>();
        // ...
    } // p's destruction calls ~Base(), not ~D(), which leaks D::s and possibly more

##### Note

Une fonction virtuelle définit une interface pour les classes dérivées qui peut être utilisée sans regarder les classes dérivées. Si l'interface permet la destruction, elle doit être sûre à faire.

##### Note

Un destructeur doit être non‑privé sinon il empêchera l'utilisation du type :

    class X {
        ~X();   // private destructor
        // ...
    };

    void use()
    {
        X a;                        // error: cannot destroy
        auto p = make_unique<X>();  // error: cannot destroy
    }

##### Exception

On peut imaginer un cas où vous voudriez un destructeur virtuel protégé : lorsqu'un objet d'un type dérivé (et uniquement d'un tel type) devrait être autorisé à détruire *un autre* objet (pas lui‑même) via un pointeur vers la base. Nous n'avons pas vu de tel cas en pratique, cependant.

##### Application

* Une classe avec des fonctions virtuelles doit avoir un destructeur qui est soit public et virtuel, soit protégé et non‑virtuel.
* Si une classe hérite publiquement d'une classe de base, la base doit avoir un destructeur qui est soit public et virtuel, soit protégé et non‑virtuel.

### <a name="rc-dtor-fail"></a>C.36 : Un destructeur ne doit pas échouer

##### Raison

En général, nous ne savons pas comment écrire du code sans erreur si un destructeur doit échouer. La bibliothèque standard exige que toutes les classes qu'elle manipule aient des destructeurs qui ne sortent pas en lançant une exception.

##### Exemple

    class X {
    public:
        ~X() noexcept;
        // ...
    };

    X::~X() noexcept
    {
        // ...
        if (cannot_release_a_resource) terminate();
        // ...
    }

##### Note

Beaucoup ont essayé de concevoir un schéma infaillible pour gérer les échecs dans les destructeurs. Aucun n'a réussi à proposer une solution générale. Cela peut être un problème pratique réel : par exemple, qu'en est‑il d'une socket qui ne se ferme pas ? L'auteur d'un destructeur ne sait pas pourquoi le destructeur est appelé et ne peut « refuser d'agir » en lançant une exception. Voir [discussion](028-discussion.md#sd-never-fail). Pour aggraver le problème, de nombreuses opérations « close/release » ne sont pas réessayables. Si possible, considérez l'échec de fermeture/nettoyage comme une erreur de conception fondamentale et terminez le programme.

##### Note

Déclarez un destructeur `noexcept`. Cela garantira qu'il se termine normalement ou termine le programme.

##### Note

Si une ressource ne peut pas être libérée et que le programme ne doit pas échouer, essayez de signaler l'échec au reste du système d'une manière quelconque (peut‑être même en modifiant un état global et en espérant que quelque chose le remarquera et pourra s'en occuper). Soyez pleinement conscient que cette technique est spéciale et sujette à erreurs. Considérez l'exemple « ma connexion ne se ferme pas » : il y a probablement un problème à l'autre extrémité de la connexion et seul un morceau de code responsable des deux extrémités peut gérer correctement le problème. Le destructeur pourrait envoyer un message (d'une manière ou d'une autre) à la partie responsable du système, considérer que la connexion est fermée, et retourner normalement.

##### Note

Si un destructeur utilise des opérations qui pourraient échouer, il peut attraper les exceptions et, dans certains cas, terminer avec succès (par ex. en utilisant un mécanisme de nettoyage différent de celui qui a lancé l'exception).

##### Application

(Simple) Un destructeur devrait être déclaré `noexcept` s'il pourrait lancer une exception.

### <a name="rc-dtor-noexcept"></a>C.37 : Rendre les destructeurs `noexcept`

##### Raison

[Un destructeur ne doit pas échouer](007-class.md#rc-dtor-fail). Si un destructeur tente de sortir avec une exception, c'est une mauvaise conception et le programme devrait plutôt se terminer.

##### Note

Un destructeur (qu'il soit défini par l'utilisateur ou généré par le compilateur) est implicitement déclaré `noexcept` (indépendamment du code de son corps) si tous les membres de sa classe ont des destructeurs `noexcept`. En déclarant explicitement les destructeurs `noexcept`, un auteur se protège contre le fait que le destructeur devienne implicitement `noexcept(false)` suite à l'ajout ou à la modification d'un membre de classe.

##### Exemple

Tous les destructeurs ne sont pas `noexcept` par défaut ; un destructeur avec un membre qui lance une exception rend toute la hiérarchie `noexcept(false)`.

    struct X {
        Details x;  // has a throwing destructor
        // ...
        ~X() { }    // implicitly noexcept(false); aka can throw
    };

Donc, en cas de doute, déclarez un destructeur `noexcept`.

##### Note

Pourquoi ne pas déclarer tous les destructeurs `noexcept` ? Parce que cela serait souvent, surtout dans les cas simples, du bruit inutile.

##### Application

(Simple) Un destructeur devrait être déclaré `noexcept` s'il pourrait lancer une exception.

## <a name="ss-ctor"></a>C.ctor : Constructeurs

Un constructeur définit comment un objet est initialisé (construit).

### <a name="rc-ctor"></a>C.40 : Définir un constructeur si une classe possède une invariant

##### Raison

C'est à quoi servent les constructeurs.

##### Exemple

    class Date {  // a Date represents a valid date
                  // in the January 1, 1900 to December 31, 2100 range
        Date(int dd, int mm, int yy)
            :d{dd}, m{mm}, y{yy}
        {
            if (!is_valid(d, m, y)) throw Bad_date{};  // enforce invariant
        }
        // ...
    private:
        int d, m, y;
    };

Il est souvent judicieux d'exprimer l'invariant comme un `Ensures` sur le constructeur.

##### Note

Un constructeur peut être utilisé par commodité même si une classe n'a pas d'invariant. Par exemple :

    struct Rec {
        string s;
        int i {0};
        Rec(const string& ss) : s{ss} {}
        Rec(int ii) :i{ii} {}
    };

    Rec r1 {7};
    Rec r2 {"Foo bar"};

##### Note

La règle C++11 de la liste d'initialisation élimine le besoin de nombreux constructeurs. Par exemple :

    struct Rec2{
        string s;
        int i;
        Rec2(const string& ss, int ii = 0) :s{ss}, i{ii} {}   // redundant
    };

    Rec2 r1 {"Foo", 7};
    Rec2 r2 {"Bar"};

Le constructeur `Rec2` est redondant. De plus, la valeur par défaut pour `int` serait mieux faite comme un [initialiseur de membre par défaut](007-class.md#rc-in-class-initializer).

**Voir aussi** : [construire un objet valide](007-class.md#rc-complete) et [le constructeur lance une exception](007-class.md#rc-throw).

##### Application

* Signaler les classes avec des opérations de copie définies mais aucun constructeur (une opération de copie définie est un bon indicateur que la classe possède une invariant).

### <a name="rc-complete"></a>C.41 : Un constructeur doit créer un objet entièrement initialisé

##### Raison

Un constructeur établit l'invariant d'une classe. Un utilisateur de la classe doit pouvoir supposer qu'un objet construit est utilisable.

##### Exemple, mauvais

    class X1 {
        FILE* f;   // call init() before any other function
        // ...
    public:
        X1() {}
        void init();   // initialize f
        void read();   // read from f
        // ...
    };

    void f()
    {
        X1 file;
        file.read();   // crash or bad read!
        // ...
        file.init();   // too late
        // ...
    }

Les compilateurs ne lisent pas les commentaires.

##### Exception

Si un objet valide ne peut pas être construit commodément par un constructeur, [utilisez une fonction fabrique](007-class.md#rc-factory).

##### Application

* (Simple) Chaque constructeur doit initialiser chaque membre de données (soit explicitement, via un appel de constructeur délégué ou via la construction par défaut).
* (Inconnu) Si un constructeur possède un contrat `Ensures`, essayez de vérifier qu'il tient en tant que postcondition.

##### Note

Si un constructeur acquiert une ressource (pour créer un objet valide), cette ressource doit être [libérée par le destructeur](007-class.md#rc-dtor-release). L'idiome consistant à acquérir des ressources dans le constructeur et à les libérer dans le destructeur s'appelle [RAII](009-resource.md#rr-raii) (« Resource Acquisition Is Initialization »).

### <a name="rc-throw"></a>C.42 : Si un constructeur ne peut pas construire un objet valide, lancer une exception

##### Raison

Laisser derrière soi un objet invalide invite aux ennuis.

##### Exemple

    class X2 {
        FILE* f;
        // ...
    public:
        X2(const string& name)
            :f{fopen(name.c_str(), "r")}
        {
            if (!f) throw runtime_error{"could not open" + name};
            // ...
        }

        void read();      // read from f
        // ...
    };

    void f()
    {
        X2 file {"Zeno"}; // throws if file isn't open
        file.read();      // fine
        // ...
    }

##### Exemple, mauvais

    class X3 {     // bad: the constructor leaves a non-valid object behind
        FILE* f;   // call is_valid() before any other function
        bool valid;
        // ...
    public:
        X3(const string& name)
            :f{fopen(name.c_str(), "r")}, valid{false}
        {
            if (f) valid = true;
            // ...
        }

        bool is_valid() { return valid; }
        void read();   // read from f
        // ...
    };

    void f()
    {
        X3 file {"Heraclides"};
        file.read();   // crash or bad read!
        // ...
        if (file.is_valid()) {
            file.read();
            // ...
        }
        else {
            // ... handle error ...
        }
        // ...
    }

##### Note

Pour une définition de variable (par ex. sur la pile ou comme membre d'un autre objet) il n'y a pas d'appel de fonction explicite d'où un code d'erreur pourrait être retourné. Laisser derrière soi un objet invalide et compter sur les utilisateurs pour vérifier systématiquement une fonction `is_valid()` avant utilisation est fastidieux, source d'erreurs et inefficace.

##### Exception

Il existe des domaines, comme certains systèmes temps réel stricts (pensons aux contrôles d'avion), où (sans support d'outils supplémentaire) la gestion des exceptions n'est pas suffisamment prévisible du point de vue du timing. Dans de tels cas, la technique `is_valid()` doit être utilisée. Dans ces cas, vérifiez `is_valid()` de façon cohérente et immédiate pour simuler [RAII](009-resource.md#rr-raii).

##### Alternative

Si vous êtes tenté d'utiliser une « initialisation post‑constructeur » ou une « initialisation en deux étapes », essayez de ne pas le faire. Si vous devez vraiment le faire, examinez les [fonctions fabrique](007-class.md#rc-factory).

##### Note

Une des raisons pour lesquelles les gens utilisent des fonctions `init()` plutôt que de faire le travail d'initialisation dans un constructeur a été d'éviter la duplication de code. Les [constructeurs délégués](007-class.md#rc-delegating) et les [initialiseurs de membres par défaut](007-class.md#rc-in-class-initializer) font cela mieux. Une autre raison a été de retarder l'initialisation jusqu'à ce qu'un objet soit réellement nécessaire ; la solution est souvent [de ne pas déclarer une variable tant qu'elle ne peut pas être correctement initialisée](010-expr.md#res-init).

##### Application

???

### <a name="rc-default0"></a>C.43 : S'assurer qu'une classe copiable possède un constructeur par défaut

##### Raison

C'est‑à‑dire, s'assurer que si une classe concrète est copiable, elle satisfait également le reste de la « semiregularité ».

De nombreuses installations et bibliothèques reposent sur les constructeurs par défaut pour initialiser leurs éléments, par ex. `T a[10]` et `std::vector<T> v(10)`. Un constructeur par défaut simplifie souvent la tâche de définir un état « déplacé‑de » approprié pour un type qui est également copiable.

##### Exemple

    class Date { // BAD: no default constructor
    public:
        Date(int dd, int mm, int yyyy);
        // ...
    };

    vector<Date> vd1(1000);   // default Date needed here
    vector<Date> vd2(1000, Date{7, Month::October, 1885});   // alternative

Le constructeur par défaut n'est généré que s'il n'y a aucun constructeur déclaré par l'utilisateur, d'où il est impossible d'initialiser le vecteur `vd1` dans l'exemple ci‑dessus. L'absence d'une valeur par défaut peut surprendre les utilisateurs et compliquer son utilisation, donc si une valeur raisonnable peut être définie, elle devrait l'être.

`Date` est choisi pour encourager la réflexion : il n'y a pas de « date par défaut naturelle » (le Big Bang est trop lointain pour la plupart des gens). `{0, 0, 0}` n'est pas une date valide dans la plupart des calendriers, donc choisir cela reviendrait à introduire quelque chose comme le `NaN` des flottants. Cependant, la plupart des classes `Date` réalistes ont une « première date » (par ex. le 1er janvier 1970 est populaire), donc en faire la valeur par défaut est généralement trivial.

    class Date {
    public:
        Date(int dd, int mm, int yyyy);
        Date() = default; // [See also](007-class.md#rc-default)
        // ...
    private:
        int dd {1};
        int mm {1};
        int yyyy {1970};
        // ...
    };

    vector<Date> vd1(1000);

##### Note

Une classe dont tous les membres ont des constructeurs par défaut possède implicitement un constructeur par défaut :

    struct X {
        string s;
        vector<int> v;
    };

    X x; // équivaut à X{ { }, { } }; c'est‑à‑dire la chaîne vide et le vecteur vide

Attention : les types intégrés ne sont pas correctement construits par défaut :

    struct X {
        string s;
        int i;
    };

    void f()
    {
        X x;    // x.s est initialisée à la chaîne vide ; x.i est non initialisée
        cout << x.s << ' ' << x.i << '\n';
        ++x.i;
    }

Les objets statiquement alloués de types intégrés sont initialisés à `0` par défaut, mais les variables locales de type intégré ne le sont pas. Votre compilateur pourrait initialiser les variables locales intégrées, alors qu'une construction optimisée ne le ferait pas. Ainsi, le code ci‑dessus pourrait sembler fonctionner, mais il repose sur un comportement indéfini. Si vous voulez une initialisation, une initialisation explicite peut aider :

    struct X {
        string s;
        int i {};   // default initialize (to 0)
    };

##### Notes

Les classes qui n'ont pas de construction par défaut raisonnable ne sont généralement pas copiabiles non plus, donc elles ne relèvent pas de cette directive.

Par exemple, une classe de base ne devrait pas être copiable, et n'a donc pas nécessairement besoin d'un constructeur par défaut :

    // Shape is an abstract base class, not a copyable type.
    // It might or might not need a default constructor.
    struct Shape {
        virtual void draw() = 0;
        virtual void rotate(int) = 0;
        // =delete copy/move functions
        // ...
    };

Une classe qui doit acquérir une ressource fournie par l'appelant pendant la construction ne peut souvent pas avoir de constructeur par défaut, mais elle ne relève pas de cette directive car une telle classe n'est généralement pas copiable de toute façon :

    // std::lock_guard is not a copyable type.
    // It does not have a default constructor.
    lock_guard g {mx};  // guard the mutex mx
    lock_guard g2;      // error: guarding nothing

Une classe qui possède un « état spécial » qui doit être géré séparément des autres états par des fonctions membres ou par les utilisateurs entraîne un travail supplémentaire (et très probablement plus d'erreurs). Un tel type peut naturellement utiliser cet état spécial comme valeur construite par défaut, qu'il soit copiable ou non :

    // std::ofstream is not a copyable type.
    // It does happen to have a default constructor
    // that goes along with a special "not open" state.
    ofstream out {"Foobar"};
    // ...
    out << log(time, transaction);

Des types d'état spécial copiabiles, comme les pointeurs intelligents copiabiles qui ont l'état spécial `==nullptr`, devraient utiliser cet état spécial comme valeur construite par défaut.

Cependant, il est préférable d'avoir un constructeur par défaut qui initialise à un état significatif tel que `std::string` `""` et `std::vector` `{}`.

##### Application

* Signaler les classes qui sont copiabiles par `=` sans constructeur par défaut.
* Signaler les classes qui sont comparables avec `==` mais pas copiabiles.

### <a name="rc-default00"></a>C.44 : Préférer que les constructeurs par défaut soient simples et ne lèvent pas d'exception

##### Raison

Pouvoir mettre une valeur à « la valeur par défaut » sans opérations qui pourraient échouer simplifie la gestion des erreurs et le raisonnement sur les opérations de déplacement.

##### Exemple, problématique

    template<typename T>
    // elem points to space-elem element allocated using new
    class Vector0 {
    public:
        Vector0() :Vector0{0} {}
        Vector0(int n) :elem{new T[n]}, space{elem + n}, last{elem} {}
        // ...
    private:
        own<T*> elem;
        T* space;
        T* last;
    };

C'est joli et général, mais mettre un `Vector0` à vide après une erreur implique une allocation, qui peut échouer. De plus, avoir un `Vector` par défaut représenté comme `{new T[0], 0, 0}` semble gaspilleur. Par exemple, `Vector0<int> v[100]` coûte 100 allocations.

##### Exemple

    template<typename T>
    // elem is nullptr or elem points to space-elem element allocated using new
    class Vector1 {
    public:
        // sets the representation to {nullptr, nullptr, nullptr}; doesn't throw
        Vector1() noexcept {}
        Vector1(int n) :elem{new T[n]}, space{elem + n}, last{elem} {}
        // ...
    private:
        own<T*> elem {};
        T* space {};
        T* last {};
    };

Utiliser `{nullptr, nullptr, nullptr}` rend `Vector1{}` peu coûteux, mais introduit un cas spécial et implique des vérifications d'exécution. Mettre un `Vector1` à vide après la détection d'une erreur devient trivial.

##### Application

* Signaler les constructeurs par défaut qui lancent des exceptions.

### <a name="rc-default"></a>C.45 : Ne pas définir un constructeur par défaut qui ne fait qu'initialiser les membres de données ; utiliser des initialiseurs de membres par défaut à la place

##### Raison

Utiliser des initialiseurs de membres par défaut laisse le compilateur générer la fonction pour vous. La fonction générée par le compilateur peut être plus efficace.

##### Exemple, mauvais

    class X1 { // BAD: doesn't use member initializers
        string s;
        int i;
    public:
        X1() :s{"default"}, i{1} { }
        // ...
    };

##### Exemple

    class X2 {
        string s {"default"};
        int i {1};
    public:
        // use compiler-generated default constructor
        // ...
    };

##### Application

(Simple) Signaler si l'initialiseur explicite d'un constructeur par défaut est une constante, et recommander que la constante soit écrite comme initialiseur de donnée.

### <a name="rc-explicit"></a>C.46 : Par défaut, déclarer les constructeurs à un seul argument `explicit`

##### Raison

Éviter les conversions implicites non désirées.

##### Exemple, mauvais

    class String {
    public:
        String(int);   // BAD
        // ...
    };

    String s = 10;   // surprise: string of size 10

##### Exception

Si vous voulez réellement une conversion implicite du type d'argument vers le type de classe, n'utilisez pas `explicit` :

    class Complex {
    public:
        Complex(double d);   // OK: we want a conversion from d to {d, 0}
        // ...
    };

    Complex z = 10.7;   // unsurprising conversion

**Voir aussi** : [Discussion des conversions implicites](007-class.md#ro-conversion)

##### Note

Les constructeurs de copie et de déplacement ne doivent pas être `explicit` car ils ne réalisent pas de conversions. Des constructeurs de copie/déplacement `explicit` rendent le passage et le retour par valeur difficiles.

##### Application

(Simple) Les constructeurs à un seul argument devraient être déclarés `explicit`. Les bons constructeurs à un seul argument non‑`explicit` sont rares dans la plupart des bases de code. Avertir pour tous ceux qui ne figurent pas sur une « liste positive ».

### <a name="rc-order"></a>C.47 : Définir et initialiser les membres de données dans l'ordre de leur déclaration

##### Raison

Minimiser la confusion et les erreurs. C'est l'ordre dans lequel l'initialisation se produit (indépendamment de l'ordre des initialiseurs de membres).

##### Exemple, mauvais

    class Foo {
        int m1;
        int m2;
    public:
        Foo(int x) :m2{x}, m1{++x} { }   // BAD: misleading initializer order
        // ...
    };

    Foo x(1); // surprise: x.m1 == x.m2 == 2

##### Application

(Simple) Une liste d'initialisation de membres devrait mentionner les membres dans le même ordre que leur déclaration.

**Voir aussi** : [Discussion](028-discussion.md#sd-order)

### <a name="rc-in-class-initializer"></a>C.48 : Préférer les initialiseurs de membres par défaut aux initialiseurs de membres dans les constructeurs pour les initialiseurs constants

##### Raison

Rendre explicite que la même valeur est attendue dans tous les constructeurs. Éviter la répétition. Éviter les problèmes de maintenance. Cela conduit au code le plus court et le plus efficace.

##### Exemple, mauvais

    class X {   // BAD
        int i;
        string s;
        int j;
    public:
        X() :i{666}, s{"qqq"} { }   // j is uninitialized
        X(int ii) :i{ii} {}         // s is "" and j is uninitialized
        // ...
    };

Comment un mainteneur saurait‑il si `j` était intentionnellement non initialisé (probablement une mauvaise idée) et si `s` était intentionnellement `" "` dans un cas et `"qqq"` dans l'autre (presque certainement un bug) ? Le problème avec `j` (oublier d'initialiser un membre) survient souvent lorsqu'un nouveau membre est ajouté à une classe existante.

##### Exemple

    class X2 {
        int i {666};
        string s {"qqq"};
        int j {numeric_limits<int>::min()};
    public:
        X2() = default;        // all members are initialized to their defaults
        X2(int ii) :i{ii} {}   // s and j initialized to their defaults
        // ...
    };

**Alternative** : Nous pouvons obtenir une partie des bénéfices des arguments par défaut aux constructeurs, mais cela est moins explicite, entraîne plus de passage d'arguments, et est répétitif lorsqu'il y a plus d'un constructeur :

    class X3 {   // BAD: inexplicit, argument passing overhead
        int i;
        string s;
        int j;
    public:
        X3(int ii = 666, const string& ss = "qqq", int jj = numeric_limits<int>::min())
            :i{ii}, s{ss}, j{jj} { }   // all members are initialized to their defaults
        // ...
    };

##### Application

* (Simple) Chaque constructeur doit initialiser chaque membre de données (soit explicitement, via un appel de constructeur délégué ou via la construction par défaut).
* (Simple) Les arguments par défaut aux constructeurs suggèrent qu'un initialiseur de membre par défaut pourrait être plus approprié.

### <a name="rc-initialize"></a>C.49 : Préférer l'initialisation à l'assignation dans les constructeurs

##### Raison

Une initialisation indique explicitement que l'on initialise plutôt qu'on assigne, et peut être plus élégante et efficace. Elle empêche les erreurs « utiliser avant de définir ».

##### Exemple, bon

    class A {   // Good
        string s1;
    public:
        A(czstring p) : s1{p} { }    // GOOD: directly construct (and the C-string is explicitly named)
        // ...
    };

##### Exemple, mauvais

    class B {   // BAD
        string s1;
    public:
        B(const char* p) { s1 = p; }   // BAD: default constructor followed by assignment
        // ...
    };

    class C {   // UGLY, aka very bad
        int* p;
    public:
        C() { cout << *p; p = new int{10}; }   // accidental use before initialized
        // ...
    };

##### Exemple, encore meilleur

Au lieu d'utiliser des `const char*`, nous pourrions utiliser le `std::string_view` C++17 ou `gsl::span<char>` comme [une façon plus générale de présenter des arguments à une fonction](018-stdlib.md#rstr-view) :

    class D {   // Good
        string s1;
    public:
        D(string_view v) : s1{v} { }    // GOOD: directly construct
        // ...
    };

### <a name="rc-factory"></a>C.50 : Utiliser une fonction fabrique si vous avez besoin d'un « comportement virtuel » pendant l'initialisation

##### Raison

Si l'état d'un objet de base doit dépendre de l'état d'une partie dérivée de l'objet, nous devons utiliser une fonction virtuelle (ou équivalente) tout en minimisant la fenêtre d'opportunité d'abuser d'un objet imparfaitement construit.

##### Note

Le type de retour de la fabrique devrait normalement être `unique_ptr` par défaut ; si certains usages sont partagés, l'appelant peut `move` le `unique_ptr` dans un `shared_ptr`. Cependant, si le créateur de la fabrique sait que toutes les utilisations de l'objet retourné seront partagées, retourner `shared_ptr` et utiliser `make_shared` dans le corps permet d'économiser une allocation.

##### Exemple, mauvais

    class B {
    public:
        B()
        {
            /* ... */
            f(); // BAD: C.82: Don't call virtual functions in constructors and destructors
            /* ... */
        }

        virtual void f() = 0;
    };

##### Exemple

    class B {
    protected:
        class Token {};

    public:
        explicit B(Token) { /* ... */ }  // create an imperfectly initialized object
        virtual void f() = 0;

        template<class T>
        static shared_ptr<T> create()    // interface for creating shared objects
        {
            auto p = make_shared<T>(typename T::Token{});
            p->post_initialize();
            return p;
        }

    protected:
        virtual void post_initialize()   // called right after construction
            { /* ... */ f(); /* ... */ } // GOOD: virtual dispatch is safe
    };

    class D : public B {                 // some derived class
    protected:
        class Token {};

    public:
        explicit D(Token) : B{ B::Token{} } {}
        void f() override { /* ...  */ };

    protected:
        template<class T>
        friend shared_ptr<T> B::create();
    };

    shared_ptr<D> p = D::create<D>();  // creating a D object

`make_shared` nécessite que le constructeur soit public. En exigeant un `Token` protégé, le constructeur ne peut plus être appelé publiquement, évitant ainsi qu'un objet imparfaitement construit ne s'échappe dans le monde. En fournissant la fonction fabrique `create()`, nous rendons la construction (sur le tas) pratique.

##### Note

Les fonctions fabrique conventionnelles allouent sur le tas, plutôt que sur la pile ou dans un objet englobant.

**Voir aussi** : [Discussion](028-discussion.md#sd-factory)

### <a name="rc-delegating"></a>C.51 : Utiliser des constructeurs délégués pour représenter des actions communes à tous les constructeurs d'une classe

##### Raison

Éviter la répétition et les différences accidentelles.

##### Exemple, mauvais

    class Date {   // BAD: repetitive
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
        // ...
    };

L'action commune devient fastidieuse à écrire et pourrait accidentellement ne pas être commune.

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
        // ...
    };

**Voir aussi** : Si l'« action répétée » est une simple initialisation, envisagez [un initialiseur de membre par défaut](007-class.md#rc-in-class-initializer).

##### Application

(Moderate) Rechercher des corps de constructeurs similaires.

### <a name="rc-inheriting"></a>C.52 : Utiliser les constructeurs hérités pour importer les constructeurs dans une classe dérivée qui n'a pas besoin d'une initialisation explicite supplémentaire

##### Raison

Si vous avez besoin de ces constructeurs pour une classe dérivée, les ré‑implémenter est fastidieux et source d'erreurs.

##### Exemple

`std::vector` possède de nombreux constructeurs délicats, donc si je veux mon propre `vector`, je ne veux pas les ré‑implémenter :

    class Rec {
        // ... data and lots of nice constructors ...
    };

    class Oper : public Rec {
        using Rec::Rec;
        // ... no data members ...
        // ... lots of nice utility functions ...
    };

##### Exemple, mauvais

    struct Rec2 : public Rec {
        int x;
        using Rec::Rec;
    };

    Rec2 r {"foo", 7};
    int val = r.x;   // uninitialized

##### Application

S'assurer que chaque membre de la classe dérivée est initialisé.

## <a name="ss-copy"></a>C.copy : Copie et déplacement

Les types concrets devraient généralement être copiable, mais les interfaces dans une hiérarchie de classes ne le devraient pas. Les gestionnaires de ressources peuvent ou non être copiable. Les types peuvent être définis comme déplaçables pour des raisons logiques ainsi que de performance.

### <a name="rc-copy-assignment"></a>C.60 : Rendre l'assignation de copie non‑`virtual`, prendre le paramètre par `const&`, et retourner par non‑`const&`

##### Raison

C'est simple et efficace. Si vous voulez optimiser pour les r‑values, fournissez une surcharge qui prend un `&&` (voir [F.18](006-functions.md#rf-consume)).

##### Exemple

    class Foo {
    public:
        Foo& operator=(const Foo& x)
        {
            // GOOD: no need to check for self-assignment (other than performance)
            auto tmp = x;
            swap(tmp); // see C.83
            return *this;
        }
        // ...
    };

    Foo a;
    Foo b;
    Foo f();

    a = b;    // assign lvalue: copy
    a = f();  // assign rvalue: potentially move

##### Note

La technique d'implémentation `swap` offre la [garantie forte](032-bibliography.md#Abrahams01).

##### Exemple

Mais que faire si vous pouvez obtenir une performance nettement meilleure en n'effectuant pas de copie temporaire ? Considérons un simple `Vector` destiné à un domaine où l'assignation de grands `Vector`s de même taille est courante. Dans ce cas, la copie des éléments impliquée par la technique `swap` pourrait augmenter le coût d'un ordre de grandeur :

    template<typename T>
    class Vector {
    public:
        Vector& operator=(const Vector&);
        // ...
    private:
        T* elem;
        int sz;
    };

    Vector& Vector::operator=(const Vector& a)
    {
        if (a.sz > sz) {
            // ... use the swap technique, it can't be bettered ...
            return *this;
        }
        // ... copy sz elements from *a.elem to elem ...
        if (a.sz < sz) {
            // ... destroy the surplus elements in *this and adjust size ...
        }
        return *this;
    }

En écrivant directement dans les éléments cibles, nous n'obtenons que la [garantie de base](032-bibliography.md#Abrahams01) plutôt que la garantie forte offerte par la technique `swap`. Méfiez‑vous de [l'auto‑assignation](007-class.md#rc-copy-self).

**Alternatives** : Si vous pensez avoir besoin d'un opérateur d'assignation `virtual` et comprenez pourquoi c'est profondément problématique, ne l'appeler pas `operator=`. Faites‑en une fonction nommée comme `virtual void assign(const Foo&)`. Voir [copy constructor vs. `clone()`](007-class.md#rc-copy-virtual).

##### Application

* (Simple) Un opérateur d'assignation ne doit pas être `virtual`. Here be dragons!
* (Simple) Un opérateur d'assignation doit retourner `T&` pour permettre le chaînage, pas des alternatives comme `const T&` qui interfèrent avec la composabilité et le placement d'objets dans des conteneurs.
* (Moderate) Un opérateur d'assignation doit (implicitement ou explicitement) invoquer tous les opérateurs d'assignation des bases et des membres. Examinez le destructeur pour déterminer si le type a une sémantique de pointeur ou de valeur.

### <a name="rc-copy-semantic"></a>C.61 : Une opération de copie doit copier

##### Raison

C'est la sémantique généralement attendue. Après `x = y`, nous devrions avoir `x == y`. Après une copie, `x` et `y` peuvent être des objets indépendants (sémantique de valeur, comme les types intégrés non pointeurs et les types de la bibliothèque standard) ou référencer un objet partagé (sémantique de pointeur, comme les pointeurs).

##### Exemple

    class X {   // OK: value semantics
    public:
        X();
        X(const X&);     // copy X
        void modify();   // change the value of X
        // ...
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
    if (x == y) throw Bad{};   // assume value semantics

##### Exemple

    class X2 {  // OK: pointer semantics
    public:
        X2();
        X2(const X2&) = default; // shallow copy
        ~X2() = default;
        void modify();          // change the pointed-to value
        // ...
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
    if (x != y) throw Bad{};  // assume pointer semantics

##### Note

Préférez la sémantique de valeur sauf si vous construisez un « smart pointer ». La sémantique de valeur est la plus simple à raisonner et ce que les installations de la bibliothèque standard attendent.

##### Application

(Not enforceable)

### <a name="rc-copy-self"></a>C.62 : Rendre l'assignation de copie sûre pour l'auto‑assignation

##### Raison

Si `x = x` modifie la valeur de `x`, les gens seront surpris et des erreurs graves peuvent survenir (souvent incluant des fuites).

##### Exemple

Les conteneurs de la bibliothèque standard gèrent l'auto‑assignation de façon élégante et efficace :

    std::vector<int> v = {3, 1, 4, 1, 5, 9};
    v = v;
    // the value of v is still {3, 1, 4, 1, 5, 9}

##### Note

L'assignation par défaut générée à partir de membres qui gèrent correctement l'auto‑assignation le fait correctement.

    struct Bar {
        vector<pair<int, int>> v;
        map<string, int> m;
        string s;
    };

    Bar b;
    // ...
    b = b;   // correct and efficient

##### Note

Vous pouvez gérer l'auto‑assignation en testant explicitement l'auto‑assignation, mais souvent il est plus rapide et plus élégant de s'en passer (par ex. en utilisant `swap`).

    class Foo {
        string s;
        int i;
    public:
        Foo& operator=(const Foo& a);
        // ...
    };

    Foo& Foo::operator=(const Foo& a)   // OK, but there is a cost
    {
        if (this == &a) return *this;
        s = a.s;
        i = a.i;
        return *this;
    }

C'est évidemment sûr et apparemment efficace. Cependant, que se passe‑t‑il si nous faisons un auto‑assignement par million d'assignations ? Ce sont environ un million de tests redondants (mais comme la réponse est essentiellement toujours la même, le prédicteur de branche du processeur devinera correctement presque tout le temps). Considérez :

    Foo& Foo::operator=(const Foo& a)   // simpler, and probably much better
    {
        s = a.s;
        i = a.i;
        return *this;
    }

`std::string` est sûr pour l'auto‑assignation et il en va de même pour `int`. Tout le coût est supporté par le (rare) cas d'auto‑assignation.

##### Application

(Simple) Les opérateurs d'assignation ne devraient pas contenir le motif `if (this == &a) return *this;` ???

### <a name="rc-move-assignment"></a>C.63 : Rendre l'assignation de déplacement non‑`virtual`, prendre le paramètre par `&&`, et retourner par non‑`const&`

##### Raison

C'est simple et efficace.

**Voir** : [La règle pour l'assignation de copie](007-class.md#rc-copy-assignment).

##### Application

Équivalent à ce qui est fait pour [l'assignation de copie](007-class.md#rc-copy-assignment).

* (Simple) Un opérateur d'assignation ne doit pas être `virtual`. Here be dragons!
* (Simple) Un opérateur d'assignation doit retourner `T&` pour permettre le chaînage, pas des alternatives comme `const T&` qui interfèrent avec la composabilité et le placement d'objets dans des conteneurs.
* (Moderate) Un opérateur d'assignation de déplacement doit (implicitement ou explicitement) invoquer tous les opérateurs d'assignation de déplacement des bases et des membres.

### <a name="rc-move-semantic"></a>C.64 : Une opération de déplacement doit déplacer et laisser sa source dans un état valide

##### Raison

C'est la sémantique généralement attendue. Après `y = std::move(x)` la valeur de `y` doit être celle que `x` avait et `x` doit être dans un état valide.

##### Exemple

    class X {   // OK: value semantics
    public:
        X();
        X(X&& a) noexcept;  // move X
        X& operator=(X&& a) noexcept; // move-assign X
        void modify();     // change the value of X
        // ...
        ~X() { delete[] p; }
    private:
        T* p;
        int sz;
    };

    X::X(X&& a) noexcept
        :p{a.p}, sz{a.sz}  // steal representation
    {
        a.p = nullptr;     // set to "empty"
        a.sz = 0;
    }

    void use()
    {
        X x{};
        // ...
        X y = std::move(x);
        x = X{};   // OK
    } // OK: x can be destroyed

##### Note

Idéalement, l'objet déplacé devrait être l'état par défaut du type. Assurez‑vous que, sauf raison exceptionnelle, l'état déplacé correspond à l'état par défaut. Cependant, tous les types n'ont pas d'état par défaut et pour certains types établir l'état par défaut peut être coûteux. La norme exige seulement que l'objet déplacé puisse être détruit. Souvent, nous pouvons faire mieux : la bibliothèque standard suppose qu'il est possible d'assigner à un objet déplacé. Laissez toujours l'objet déplacé dans un état valide (nécessairement spécifié).

##### Note

À moins d'une raison exceptionnellement forte, faites en sorte que `x = std::move(y); y = z;` fonctionne avec les sémantiques conventionnelles.

##### Application

(Not enforceable) Recherchez les assignations aux membres dans l'opération de déplacement. Si un constructeur par défaut existe, comparez ces assignations aux initialisations du constructeur par défaut.

### <a name="rc-move-self"></a>C.65 : Rendre l'assignation de déplacement sûre pour l'auto‑assignation

##### Raison

Si `x = x` modifie la valeur de `x`, les gens seront surpris et des erreurs graves peuvent survenir. Cependant, les gens n'écrivent généralement pas directement une auto‑assignation qui devient un déplacement, mais cela peut arriver. De plus, `std::swap` est implémenté en utilisant les opérations de déplacement, donc si vous faites accidentellement `swap(a, b)` où `a` et `b` font référence au même objet, ne pas gérer l'auto‑déplacement pourrait être une erreur sérieuse et subtile.

##### Exemple

    class Foo {
        string s;
        int i;
    public:
        Foo& operator=(Foo&& a) noexcept;
        // ...
    };

    Foo& Foo::operator=(Foo&& a) noexcept  // OK, but there is a cost
    {
        if (this == &a) return *this;  // this line is redundant
        s = std::move(a.s);
        i = a.i;
        return *this;
    }

L'argument « un‑sur‑un‑million » contre le test `if (this == &a) return *this;` est encore plus pertinent pour l'auto‑déplacement.

##### Note

Il n'existe aucune façon générale connue d'éviter le test `if (this == &a) return *this;` pour une assignation de déplacement et d'obtenir tout de même un résultat correct (c'est‑à‑dire, après `x = x` la valeur de `x` reste inchangée).

##### Note

La norme ISO ne garantit qu'un état « valide mais non spécifié » pour les conteneurs de la bibliothèque standard. Apparemment cela n'a pas posé de problème pendant une dizaine d'années d'utilisation expérimentale et en production. Contactez les éditeurs si vous trouvez un contre‑exemple. Cette règle est plus prudente et insiste sur la sécurité totale.

##### Exemple

Voici une façon de déplacer un pointeur sans test (imaginez cela comme du code dans l'implémentation d'une assignation de déplacement) :

    // move from other.ptr to this->ptr
    T* temp = other.ptr;
    other.ptr = nullptr;
    delete ptr; // in self-move, this->ptr is also null; delete is a no-op
    ptr = temp; // in self-move, the original ptr is restored

##### Application

* (Moderate) Dans le cas d'une auto‑assignation, un opérateur d'assignation de déplacement ne doit pas laisser l'objet contenant des pointeurs qui ont été `delete`d ou mis à `nullptr`.
* (Not enforceable) Examinez l'utilisation des types de la bibliothèque standard (incluant `string`) et considérez‑les sûrs pour les usages ordinaires (non critiques).

### <a name="rc-move-noexcept"></a>C.66 : Rendre les opérations de déplacement `noexcept`

##### Raison

Une opération de déplacement qui lance une exception viole les hypothèses raisonnables de la plupart des gens. Une opération de déplacement non‑exceptionnelle sera utilisée plus efficacement par les installations de la bibliothèque standard et les fonctionnalités du langage.

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
        // ...
    private:
        T* elem;
        int sz;
    };

Ces opérations ne lancent pas d'exception.

##### Exemple, mauvais

    template<typename T>
    class Vector2 {
    public:
        Vector2(Vector2&& a) noexcept { *this = a; }             // just use the copy
        Vector2& operator=(Vector2&& a) noexcept { *this = a; }  // just use the copy
        // ...
    private:
        T* elem;
        int sz;
    };

Ce `Vector2` n'est pas seulement inefficace, mais comme une copie de vecteur nécessite une allocation, il peut lancer une exception.

##### Application

(Simple) Une opération de déplacement doit être marquée `noexcept`.

### <a name="rc-copy-virtual"></a>C.67 : Une classe polymorphe doit supprimer les copies/déplacements publics

##### Raison

Une *classe polymorphe* est une classe qui définit ou hérite d'au moins une fonction virtuelle. Il est probable qu'elle sera utilisée comme classe de base pour d'autres classes dérivées avec un comportement polymorphe. Si elle est accidentellement passée par valeur, avec les constructeurs et assignations de copie générés implicitement, nous risquons le *slicing* : seule la partie base d'un objet dérivé sera copiée, et le comportement polymorphe sera corrompu.

Si la classe n'a pas de données, `=delete` les fonctions de copie/déplacement. Sinon, les rendre `protected`.

##### Exemple, mauvais

    class B { // BAD: polymorphic base class doesn't suppress copying
    public:
        virtual char m() { return 'B'; }
        // ... nothing about copy operations, so uses default ...
    };

    class D : public B {
    public:
        char m() override { return 'D'; }
        // ...
    };

    void f(B& b)
    {
        auto b2 = b; // oops, slices the object; b2.m() will return 'B'
    }

    D d;
    f(d);

##### Exemple

    class B { // GOOD: polymorphic class suppresses copying
    public:
        B() = default;
        B(const B&) = delete;
        B& operator=(const B&) = delete;
        virtual char m() { return 'B'; }
        // ...
    };

    class D : public B {
    public:
        char m() override { return 'D'; }
        // ...
    };

    void f(B& b)
    {
        auto b2 = b; // ok, compiler will detect inadvertent copying, and protest
    }

    D d;
    f(d);

##### Note

Si vous avez besoin de créer des copies profondes d'objets polymorphes, utilisez des fonctions `clone()` virtuelles : voir [C.130](007-class.md#rh-copy).

##### Exception

Les classes qui représentent des objets d'exception doivent être à la fois polymorphes et copiable‑constructibles.

##### Application

* Signaler une classe polymorphe avec une opération de copie publique.
* Signaler une assignation d'objets de classe polymorphe.

## C.other : Autres règles d'opérations par défaut

En plus des opérations pour lesquelles le langage offre des implémentations par défaut,
il existe quelques opérations si fondamentales que des règles spécifiques sont nécessaires :
comparaisons, `swap` et `hash`.

### <a name="rc-eqdefault"></a>C.80 : Utiliser `=default` si vous devez être explicite sur l'utilisation de la sémantique par défaut

##### Raison

Le compilateur est plus susceptible d'obtenir les sémantiques par défaut correctement et vous ne pouvez pas implémenter ces fonctions mieux que le compilateur.

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

Parce que nous avons défini le destructeur, nous devons définir les opérations de copie et de déplacement. Le `= default` est la meilleure et la plus simple façon de le faire.

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

Écrire les corps des opérations de copie et de déplacement est verbeux, fastidieux et source d'erreurs. Un compilateur le fait mieux.

##### Application

(Moderate) Le corps d'une opération définie par l'utilisateur ne doit pas avoir les mêmes sémantiques que la version générée par le compilateur, car cela serait redondant.

### <a name="rc-delete"></a>C.81 : Utiliser `=delete` lorsque vous voulez désactiver le comportement par défaut (sans vouloir une alternative)

##### Raison

Dans quelques cas, une opération par défaut n'est pas souhaitable.

##### Exemple

    class Immortal {
    public:
        ~Immortal() = delete;   // do not allow destruction
        // ...
    };

    void use()
    {
        Immortal ugh;   // error: ugh cannot be destroyed
        Immortal* p = new Immortal{};
        delete p;       // error: cannot destroy *p
    }

##### Exemple

Un `unique_ptr` peut être déplacé, mais pas copié. Pour y parvenir, ses opérations de copie sont supprimées. Pour éviter la copie, il est nécessaire de `=delete` ses opérations de copie depuis des l‑values :

    template<class T, class D = default_delete<T>> class unique_ptr {
    public:
        // ...
        constexpr unique_ptr() noexcept;
        explicit unique_ptr(pointer p) noexcept;
        // ...
        unique_ptr(unique_ptr&& u) noexcept;   // move constructor
        // ...
        unique_ptr(const unique_ptr&) = delete; // disable copy from lvalue
        // ...
    };

    unique_ptr<int> make();   // make "something" and return it by moving

    void f()
    {
        unique_ptr<int> pi {};
        auto pi2 {pi};      // error: no move constructor from lvalue
        auto pi3 {make()};  // OK, move: the result of make() is an rvalue
    }

Notez que les fonctions supprimées devraient être publiques.

##### Application

La suppression d'une opération par défaut est (devrait être) basée sur la sémantique souhaitée de la classe. Considérez ces classes comme suspectes, mais maintenez une « liste positive » de classes où un humain a affirmé que la sémantique est correcte.

### <a name="rc-ctor-virtual"></a>C.82 : Ne pas appeler de fonctions virtuelles dans les constructeurs et les destructeurs

##### Raison

La fonction appelée sera celle de l'objet construit jusqu'à présent, plutôt que celle éventuellement surchargée dans une classe dérivée. Cela peut être très déroutant. Pire, un appel direct ou indirect à une fonction virtuelle pure non implémentée depuis un constructeur ou un destructeur entraîne un comportement indéfini.

##### Exemple, mauvais

    class Base {
    public:
        virtual void f() = 0;   // not implemented
        virtual void g();       // implemented with Base version
        virtual void h();       // implemented with Base version
        virtual ~Base();        // implemented with Base version
    };

    class Derived : public Base {
    public:
        void g() override;   // provide Derived implementation
        void h() final;      // provide Derived implementation

        Derived()
        {
            // BAD: attempt to call an unimplemented virtual function
            f();

            // BAD: will call Derived::g, not dispatch further virtually
            g();

            // GOOD: explicitly state intent to call only the visible version
            Derived::g();

            // ok, no qualification needed, h is final
            h();
        }
    };

Notez que l'appel d'une fonction explicitement qualifiée n'est pas un appel virtuel même si la fonction est `virtual`.

**Voir aussi** : [fonctions fabrique](007-class.md#rc-factory) pour comment obtenir l'effet d'un appel à une fonction dérivée sans risquer un comportement indéfini.

##### Note

Il n'y a rien d'intrinsèquement mauvais à appeler des fonctions virtuelles depuis les constructeurs et destructeurs. La sémantique de tels appels est sûre. Cependant, l'expérience montre que ces appels sont rarement nécessaires, facilement source de confusion et deviennent une source d'erreurs lorsqu'ils sont utilisés par des novices.

##### Application

* Signaler les appels de fonctions virtuelles depuis les constructeurs et destructeurs.

### <a name="rc-swap"></a>C.83 : Pour les types de valeur, envisager de fournir une fonction `swap` `noexcept`

##### Raison

Un `swap` peut être pratique pour implémenter un certain nombre d'idiomes, de la manipulation fluide d'objets à l'implémentation d'une assignation facile, en passant par la fourniture d'une fonction de commit garantie qui permet aux appels de code d'être fortement sûrs en cas d'erreur. Voir aussi [destructeurs, désallocation et `swap` ne doivent jamais échouer](013-errors.md#re-never-fail).

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

* Les types non trivially copyable devraient fournir un `swap` membre ou une surcharge libre de `swap`.
* (Simple) Lorsqu'une classe possède une fonction `swap` membre, elle devrait être déclarée `noexcept`.

### <a name="rc-swap-fail"></a>C.84 : Une fonction `swap` ne doit pas échouer

##### Raison

`swap` est largement utilisé de façon à supposer qu'il ne échoue jamais et les programmes ne peuvent pas être écrits facilement pour fonctionner correctement en présence d'un `swap` qui échoue. Les conteneurs et algorithmes de la bibliothèque standard ne fonctionneront pas correctement si le `swap` d'un type d'élément échoue.

##### Exemple, mauvais

    void swap(My_vector& x, My_vector& y)
    {
        auto tmp = x;   // copy elements
        x = y;
        y = tmp;
    }

Ce n'est pas seulement lent, mais si une allocation de mémoire se produit pour les éléments dans `tmp`, ce `swap` pourrait lancer une exception et ferait échouer les algorithmes STL s'ils l'utilisent.

##### Application

(Simple) Lorsqu'une classe possède une fonction `swap` membre, elle devrait être déclarée `noexcept`.

### <a name="rc-swap-noexcept"></a>C.85 : Rendre le `swap` `noexcept`

##### Raison

[Un `swap` ne doit pas échouer](007-class.md#rc-swap-fail). Si un `swap` tente de sortir avec une exception, c'est une mauvaise conception et le programme devrait plutôt se terminer.

##### Application

(Simple) Lorsqu'une classe possède une fonction `swap` membre, elle devrait être déclarée `noexcept`.

### <a name="rc-eq"></a>C.86 : Rendre `==` symétrique par rapport aux types d'opérandes et `noexcept`

##### Raison

Un traitement asymétrique des opérandes est surprenant et source d'erreurs lorsque des conversions sont possibles. `==` est une opération fondamentale et les programmeurs devraient pouvoir l'utiliser sans crainte d'échec.

##### Exemple

    struct X {
        string name;
        int number;
    };

    bool operator==(const X& a, const X& b) noexcept {
        return a.name == b.name && a.number == b.number;
    }

##### Exemple, mauvais

    class B {
        string name;
        int number;
        bool operator==(const B& a) const {
            return name == a.name && number == a.number;
        }
        // ...
    };

L'opérateur de comparaison de `B` accepte les conversions pour son second opérande, mais pas pour le premier.

##### Note

Si une classe possède un état d'échec, comme le `NaN` de `double`, il y a une tentation de faire lancer une exception lors de la comparaison avec l'état d'échec. L'alternative est de faire comparer les deux états d'échec comme égaux et tout état valide comme faux contre l'état d'échec.

##### Note

Cette règle s'applique à tous les opérateurs de comparaison habituels : `!=`, `<`, `<=`, `>`, `>=`.

##### Application

* Signaler un `operator==()` dont les types d'argument diffèrent ; idem pour les autres opérateurs de comparaison : `!=`, `<`, `<=`, `>`, `>=`.
* Signaler les `operator==()` membres ; idem pour les autres opérateurs de comparaison.

### <a name="rc-eq-base"></a>C.87 : Se méfier de `==` sur les classes de base

##### Raison

Il est vraiment difficile d'écrire un `==` fiable et utile pour une hiérarchie.

##### Exemple, mauvais

    class B {
        string name;
        int number;
    public:
        virtual bool operator==(const B& a) const
        {
             return name == a.name && number == a.number;
        }
        // ...
    };

L'opérateur de comparaison de `B` accepte les conversions pour son second opérande, mais pas pour le premier.

    class D : public B {
    public:
        char character;
    public:
        virtual bool operator==(const D& a) const
        {
            return B::operator==(a) && character == a.character;
        }
        // ...
    };

    B b = ...;
    D d = ...;
    b == d;    // compares name and number, ignores d's character
    d == b;    // compares name and number, ignores d's character
    D d2;
    d == d2;   // compares name, number, and character
    B& b2 = d2;
    b2 == d;   // compares name and number, ignores d2's and d's character

Bien sûr, il existe des moyens de faire fonctionner `==` dans une hiérarchie, mais les approches naïves ne sont pas évolutives.

##### Note

Cette règle s'applique à tous les opérateurs de comparaison habituels : `!=`, `<`, `<=`, `>`, `>=`, et `<=>`.

##### Application

* Signaler un `operator==()` virtuel ; idem pour les autres opérateurs de comparaison.

### <a name="rc-hash"></a>C.89 : Rendre un `hash` `noexcept`

##### Raison

Les utilisateurs de conteneurs de hachage utilisent le hachage indirectement et ne s'attendent pas à ce qu'un simple accès lance une exception. C'est une exigence de la bibliothèque standard.

##### Exemple, mauvais

    template<>
    struct hash<My_type> {  // thoroughly bad hash specialization
        using result_type = size_t;
        using argument_type = My_type;

        size_t operator()(const My_type & x) const
        {
            size_t xs = x.s.size();
            if (xs < 4) throw Bad_My_type{};    // "Nobody expects the Spanish inquisition!"
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

Si vous devez définir une spécialisation `hash`, essayez simplement de laisser combiner les spécialisations `hash` de la bibliothèque standard avec `^` (xor). Cela fonctionne généralement mieux que la « magie » pour les non‑spécialistes.

##### Application

* Signaler les `hash` qui lancent des exceptions.

### <a name="rc-memset"></a>C.90 : S'appuyer sur les constructeurs et les opérateurs d'assignation, pas sur `memset` et `memcpy`

##### Raison

Le mécanisme C++ standard pour construire une instance d'un type est d'appeler son constructeur. Comme indiqué dans la directive [C.41](007-class.md#rc-complete) : un constructeur doit créer un objet entièrement initialisé. Aucun initialisation supplémentaire, telle que `memcpy`, ne devrait être requise. Un type fournira un constructeur de copie et/ou un opérateur d'assignation de copie pour copier correctement la classe, en préservant les invariants du type. Utiliser `memcpy` pour copier un type non trivially copyable entraîne un comportement indéfini. Souvent cela conduit à du slicing ou à la corruption de données.

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

Cette opération n'est pas sûre pour le type : elle écrase la table virtuelle.

##### Exemple, mauvais

    void copy(derived& a, derived& b)
    {
        memcpy(&a, &b, sizeof(derived));
    }

Cette opération n'est pas sûre pour le type : elle écrase la table virtuelle.

##### Application

* Signaler le passage d'un type non trivially‑copyable à `memset` ou `memcpy`.

## <a name="ss-containers"></a>C.con : Conteneurs et autres gestionnaires de ressources

Un conteneur est un objet contenant une séquence d'objets d'un certain type ; `std::vector` est le conteneur archétypal. Un gestionnaire de ressources est une classe qui possède une ressource ; `std::vector` est le gestionnaire de ressources typique ; sa ressource est sa séquence d'éléments.

Résumé des règles de conteneur :

* [C.100 : Suivre la STL lors de la définition d'un conteneur](007-class.md#rcon-stl)
* [C.101 : Donner à un conteneur des sémantiques de valeur](007-class.md#rcon-val)
* [C.102 : Donner à un conteneur des opérations de déplacement](007-class.md#rcon-move)
* [C.103 : Donner à un conteneur un constructeur `initializer_list`](007-class.md#rcon-init)
* [C.104 : Donner à un conteneur un constructeur par défaut qui le place à vide](007-class.md#rcon-empty)
* ???
* [C.109 : Si un gestionnaire de ressources a une sémantique de pointeur, fournir `*` et `->`](007-class.md#rcon-ptr)

**Voir aussi** : [Ressources](009-resource.md)

### <a name="rcon-stl"></a>C.100 : Suivre la STL lors de la définition d'un conteneur

##### Raison

Les conteneurs STL sont familiers à la plupart des programmeurs C++ et fondamentalement bien conçus.

##### Note

Il existe bien sûr d'autres styles de conception fondamentalement solides et parfois des raisons de s'écarter du style de la bibliothèque standard, mais en l'absence de raison solide, il est plus simple et plus facile pour les implémenteurs et les utilisateurs de suivre la norme.

En particulier, `std::vector` et `std::map` offrent des modèles relativement simples.

##### Exemple

    // simplified (e.g., no allocators):

    template<typename T>
    class Sorted_vector {
        using value_type = T;
        // ... iterator types ...

        Sorted_vector() = default;
        Sorted_vector(initializer_list<T>);    // initializer-list constructor: sort and store
        Sorted_vector(const Sorted_vector&) = default;
        Sorted_vector(Sorted_vector&&) noexcept = default;
        Sorted_vector& operator=(const Sorted_vector&) = default;     // copy assignment
        Sorted_vector& operator=(Sorted_vector&&) noexcept = default; // move assignment
        ~Sorted_vector() = default;

        Sorted_vector(const std::vector<T>& v);   // store and sort
        Sorted_vector(std::vector<T>&& v);        // sort and "steal representation"

        const T& operator[](int i) const { return rep[i]; }
        // no non-const direct access to preserve order

        void push_back(const T&);   // insert in the right place (not necessarily at back)
        void push_back(T&&);        // insert in the right place (not necessarily at back)

        // ... cbegin(), cend() ...
    private:
        std::vector<T> rep;  // use a std::vector to hold elements
    };

    template<typename T> bool operator==(const Sorted_vector<T>&, const Sorted_vector<T>&);
    template<typename T> bool operator!=(const Sorted_vector<T>&, const Sorted_vector<T>&);
    // ...

Ici, le style STL est suivi, mais de façon incomplète. Ce n'est pas rare. Fournissez uniquement les fonctionnalités qui ont du sens pour un conteneur spécifique. L'essentiel est de définir les constructeurs, assignations, destructeurs et itérateurs (dans la mesure où ils sont pertinents pour le conteneur) avec leurs sémantiques conventionnelles. À partir de cela, le conteneur peut être étendu selon les besoins. Ici, des constructeurs spéciaux à partir de `std::vector` ont été ajoutés.

##### Application

???

### <a name="rcon-val"></a>C.101 : Donner à un conteneur des sémantiques de valeur

##### Raison

Les objets réguliers sont plus simples à comprendre et à raisonner que les objets irréguliers. Familiarité.

##### Note

Si cela a du sens, faites d'un conteneur un `Regular` (le concept). En particulier, assurez‑vous qu'un objet compare égal à sa copie.

##### Exemple

    void f(const Sorted_vector<string>& v)
    {
        Sorted_vector<string> v2 {v};
        if (v != v2)
            cout << "Behavior against reason and logic.\n";
        // ...
    }

##### Application

???

### <a name="rcon-move"></a>C.102 : Donner à un conteneur des opérations de déplacement

##### Raison

Les conteneurs ont tendance à être volumineux ; sans constructeur et opérateur de déplacement, un objet peut être coûteux à déplacer, incitant les gens à passer des pointeurs autour et à rencontrer des problèmes de gestion de ressources.

##### Exemple

    Sorted_vector<int> read_sorted(istream& is)
    {
        vector<int> v;
        cin >> v;   // assume we have a read operation for vectors
        Sorted_vector<int> sv = v;  // sorts
        return sv;
    }

Un utilisateur peut raisonnablement s'attendre à ce que le retour d'un conteneur de style standard soit bon marché.

##### Application

???

### <a name="rcon-init"></a>C.103 : Donner à un conteneur un constructeur `initializer_list`

##### Raison

Les gens s'attendent à pouvoir initialiser un conteneur avec un ensemble de valeurs. Familiarité.

##### Exemple

    Sorted_vector<int> sv {1, 3, -1, 7, 0, 0}; // Sorted_vector sorts elements as needed

##### Application

???

### <a name="rcon-empty"></a>C.104 : Donner à un conteneur un constructeur par défaut qui le place à vide

##### Raison

Pour le rendre `Regular`.

##### Exemple

    vector<Sorted_sequence<string>> vs(100);    // 100 Sorted_sequences each with the value ""

##### Application

???

### <a name="rcon-ptr"></a>C.109 : Si un gestionnaire de ressources a une sémantique de pointeur, fournir `*` et `->`

##### Raison

C'est ce que l'on attend des pointeurs. Familiarité.

##### Exemple

    ???

##### Application

???

## <a name="ss-lambdas"></a>C.lambdas : Objets fonctionnels et lambdas

Un objet fonctionnel est un objet fournissant un opérateur `()` surchargé afin que vous puissiez l'appeler. Une expression lambda (souvent abrégée en « lambda ») est une notation pour générer un objet fonctionnel. Les objets fonctionnels devraient être peu coûteux à copier (et donc [passés par valeur](006-functions.md#rf-in)).

Résumé :

* [F.10 : Si une opération peut être réutilisée, donnez‑lui un nom](006-functions.md#rf-name)
* [F.11 : Utiliser une lambda anonyme si vous avez besoin d'un simple objet fonctionnel à un seul endroit](006-functions.md#rf-lambda)
* [F.50 : Utiliser une lambda quand une fonction ne suffit pas (pour capturer des variables locales, ou pour écrire une fonction locale)](006-functions.md#rf-capture-vs-overload)
* [F.52 : Préférer la capture par référence dans les lambdas qui seront utilisées localement, y compris passées aux algorithmes](006-functions.md#rf-reference-capture)
* [F.53 : Éviter la capture par référence dans les lambdas qui seront utilisées de façon non locale, y compris retournées, stockées sur le tas, ou passées à un autre thread](006-functions.md#rf-value-capture)
* [ES.28 : Utiliser les lambdas pour les initialisations complexes, surtout des variables `const`](010-expr.md#res-lambda-init)

## <a name="ss-hier"></a>C.hier : Hiérarchies de classes (POO)

Une hiérarchie de classes est construite pour représenter un ensemble de concepts organisés hiérarchiquement (uniquement). Typiquement, les classes de base agissent comme interfaces. Il existe deux usages majeurs des hiérarchies, souvent appelés héritage d'implémentation et héritage d'interface.

Résumé des règles de hiérarchie de classe :

* [C.120 : Utiliser les hiérarchies de classes pour représenter des concepts avec une structure hiérarchique inhérente (uniquement)](007-class.md#rh-domain)
* [C.121 : Si une classe de base est utilisée comme interface, en faire une classe purement abstraite](007-class.md#rh-abstract)
* [C.122 : Utiliser des classes abstraites comme interfaces lorsque la séparation complète de l'interface et de l'implémentation est nécessaire](007-class.md#rh-separation)

Conception de règles pour les classes dans une hiérarchie :

* [C.126 : Une classe abstraite n'a généralement pas besoin d'un constructeur écrit par l'utilisateur](007-class.md#rh-abstract-ctor)
* [C.127 : Une classe avec une fonction virtuelle doit avoir un destructeur virtuel ou protégé](007-class.md#rh-dtor)
* [C.128 : Les fonctions virtuelles doivent spécifier exactement l'un de `virtual`, `override` ou `final`](007-class.md#rh-override)
* [C.129 : Lors de la conception d'une hiérarchie de classes, distinguer l'héritage d'implémentation de l'héritage d'interface](007-class.md#rh-kind)
* [C.130 : Pour faire des copies profondes de classes polymorphes, privilégier une fonction virtuelle `clone` plutôt qu'un constructeur/assignation public : copie](007-class.md#rh-copy)
* [C.131 : Éviter les getters et setters triviaux](007-class.md#rh-get)
* [C.132 : Ne pas rendre une fonction `virtual` sans raison](007-class.md#rh-virtual)
* [C.133 : Éviter les données `protected`](007-class.md#rh-protected)
* [C.134 : Assurer que tous les membres non‑`const` ont le même niveau d'accès](007-class.md#rh-public)
* [C.135 : Utiliser l'héritage multiple pour représenter plusieurs interfaces distinctes](007-class.md#rh-mi-interface)
* [C.136 : Utiliser l'héritage multiple pour représenter l'union d'attributs d'implémentation](007-class.md#rh-mi-implementation)
* [C.137 : Utiliser des bases virtuelles pour éviter les classes de base trop générales](007-class.md#rh-vbase)
* [C.138 : Créer un ensemble de surcharges pour une classe dérivée et ses bases avec `using`](007-class.md#rh-using)
* [C.139 : Utiliser `final` sur les classes avec parcimonie](007-class.md#rh-final)
* [C.140 : Ne pas fournir des arguments par défaut différents pour une fonction virtuelle et un redéfinisseur](007-class.md#rh-virtual-default-arg)

Accès aux objets dans une hiérarchie :

* [C.145 : Accéder aux objets polymorphes via des pointeurs et références](007-class.md#rh-poly)
* [C.146 : Utiliser `dynamic_cast` lorsque la navigation dans la hiérarchie de classes est inévitable](007-class.md#rh-dynamic_cast)
* [C.147 : Utiliser `dynamic_cast` vers un type référence lorsque l'échec à trouver la classe requise est considéré comme une erreur](007-class.md#rh-ref-cast)
* [C.148 : Utiliser `dynamic_cast` vers un type pointeur lorsque l'échec à trouver la classe requise est considéré comme une alternative valide](007-class.md#rh-ptr-cast)
* [C.149 : Utiliser `unique_ptr` ou `shared_ptr` pour éviter d'oublier de `delete` les objets créés avec `new`](007-class.md#rh-smart)
* [C.150 : Utiliser `make_unique()` pour construire des objets possédés par des `unique_ptr`s](007-class.md#rh-make_unique)
* [C.151 : Utiliser `make_shared()` pour construire des objets possédés par des `shared_ptr`s](007-class.md#rh-make_shared)
* [C.152 : Ne jamais assigner un pointeur vers un tableau d'objets dérivés à un pointeur vers sa base](007-class.md#rh-array)
* [C.153 : Privilégier la fonction virtuelle au cast](007-class.md#rh-use-virtual)

### <a name="rh-domain"></a>C.120 : Utiliser les hiérarchies de classes pour représenter des concepts avec une structure hiérarchique inhérente (uniquement)

##### Raison

La représentation directe d'idées dans le code facilite la compréhension et la maintenance. Assurez‑vous que le concept représenté dans la classe de base correspond exactement à tous les types dérivés et qu'il n'existe pas de meilleure façon de l'exprimer que d'utiliser le couplage étroit de l'héritage.

Ne *pas* utiliser l'héritage lorsqu'un simple membre de données suffit. Cela signifie généralement que le type dérivé doit surcharger une fonction virtuelle de la base ou avoir besoin d'un membre protégé.

##### Exemple

    class DrawableUIElement {
    public:
        virtual void render() const = 0;
        // ...
    };

    class AbstractButton : public DrawableUIElement {
    public:
        virtual void onClick() = 0;
        // ...
    };

    class PushButton : public AbstractButton {
        void render() const override;
        void onClick() override;
        // ...
    };

    class Checkbox : public AbstractButton {
    // ...
    };

##### Exemple, mauvais

Ne *pas* représenter des concepts de domaine non hiérarchiques comme des hiérarchies de classes.

    template<typename T>
    class Container {
    public:
        // list operations:
        virtual T& get() = 0;
        virtual void put(T&) = 0;
        virtual void insert(Position) = 0;
        // ...
        // vector operations:
        virtual T& operator[](int) = 0;
        virtual void sort() = 0;
        // ...
        // tree operations:
        virtual void balance() = 0;
        // ...
    };

Ici, la plupart des classes dérivées ne peuvent pas implémenter la plupart des fonctions requises dans l'interface correctement. Ainsi, la classe de base devient un fardeau d'implémentation. De plus, l'utilisateur de `Container` ne peut pas compter sur le fait que les fonctions membres effectuent réellement des opérations significatives de façon raisonnablement efficace ; elles pourraient lancer une exception. Les utilisateurs doivent alors recourir à la vérification d'exécution et/ou ne pas utiliser cette (sur‑)interface générale au profit d'une interface particulière trouvée via une interrogation de type à l'exécution (par ex. `dynamic_cast`).

##### Application

* Rechercher les classes avec de nombreux membres qui ne font que lancer des exceptions.
* Signaler chaque utilisation d'une classe de base non publique `B` où la classe dérivée `D` ne surcharge pas une fonction virtuelle ou n'accède pas à un membre protégé de `B`, et `B` n'est pas l'un des suivants : vide, un paramètre de modèle ou pack de paramètres de `D`, une classe modèle spécialisée avec `D`.

### <a name="rh-abstract"></a>C.121 : Si une classe de base est utilisée comme interface, en faire une classe purement abstraite

##### Raison

Une classe est plus stable (moins fragile) si elle ne contient pas de données. Les interfaces devraient normalement être composées uniquement de fonctions virtuelles pures publiques et d'un destructeur virtuel par défaut/vidé.

##### Exemple

    class My_interface {
    public:
        // ... only pure virtual functions here ...
        virtual ~My_interface() {}   // or =default
    };

##### Exemple, mauvais

    class Goof {
    public:
        // ... only pure virtual functions here ...
        // no virtual destructor
    };

    class Derived : public Goof {
        string s;
        // ...
    };

    void use()
    {
        unique_ptr<Goof> p {new Derived{"here we go"}};
        f(p.get()); // use Derived through the Goof interface
        g(p.get()); // use Derived through the Goof interface
    } // leak

Le `Derived` est `delete`d via son interface `Goof`, donc son `string` fuit. Donnez à `Goof` un destructeur virtuel et tout est bien.

##### Application

* Avertir sur toute classe qui contient des membres de données et possède également une fonction virtuelle (non‑`final`) qui n'a pas été héritée d'une classe de base.

### <a name="rh-separation"></a>C.122 : Utiliser des classes abstraites comme interfaces lorsque la séparation complète de l'interface et de l'implémentation est nécessaire

##### Raison

Par exemple, sur une frontière ABI (lien).

##### Exemple

    struct Device {
        virtual ~Device() = default;
        virtual void write(span<const char> outbuf) = 0;
        virtual void read(span<char> inbuf) = 0;
    };

    class D1 : public Device {
        // ... data ...

        void write(span<const char> outbuf) override;
        void read(span<char> inbuf) override;
    };

    class D2 : public Device {
        // ... different data ...

        void write(span<const char> outbuf) override;
        void read(span<char> inbuf) override;
    };

Un utilisateur peut maintenant utiliser `D1` et `D2` de façon interchangeable via l'interface fournie par `Device`. De plus, nous pouvons mettre à jour `D1` et `D2` de façon qui n'est pas binaire compatible avec les versions antérieures tant que tout l'accès passe par `Device`.

##### Application

    ???

### <a name="rh-abstract-ctor"></a>C.126 : Une classe abstraite n'a généralement pas besoin d'un constructeur écrit par l'utilisateur

##### Raison

Une classe abstraite n'a généralement pas de données pour qu'un constructeur les initialise.

##### Exemple

    class Shape {
    public:
        // no user-written constructor needed in abstract base class
        virtual Point center() const = 0;    // pure virtual
        virtual void move(Point to) = 0;
        // ... more pure virtual functions ...
        virtual ~Shape() {}                 // destructor
    };

    class Circle : public Shape {
    public:
        Circle(Point p, int rad);           // constructor in derived class
        Point center() const override { return x; }
    };

##### Exception

* Un constructeur de classe de base qui fait du travail, comme enregistrer un objet quelque part, pourrait nécessiter un constructeur.
* Dans de très rares cas, vous pourriez trouver raisonnable qu'une classe abstraite possède un peu de données partagées par toutes les classes dérivées (par ex. des données statistiques, des informations de débogage, etc.) ; ces classes ont tendance à nécessiter une inheritance virtuelle.

##### Application

Signaler les classes abstraites avec des constructeurs.

### <a name="rh-dtor"></a>C.127 : Une classe avec une fonction virtuelle devrait avoir un destructeur virtuel ou protégé

##### Raison

Une classe avec une fonction virtuelle est généralement (et en général) utilisée via un pointeur vers la base. Souvent, le dernier utilisateur doit appeler `delete` sur un pointeur vers la base, souvent via un `unique_ptr` ou `shared_ptr` de base, donc le destructeur devrait être public et virtuel. Moins souvent, si la suppression via un pointeur vers la base n'est pas prévue, le destructeur devrait être protégé et non‑virtuel ; voir [C.35](007-class.md#rc-dtor-virtual).

##### Exemple, mauvais

    struct B {
        virtual int f() = 0;
        // ... no user-written destructor, defaults to public non-virtual ...
    };

    // bad: derived from a class without a virtual destructor
    struct D : B {
        string s {"default"};
        // ...
    };

    void use()
    {
        unique_ptr<B> p = make_unique<D>();
        // ...
    } // undefined behavior, might call B::~B only and leak D::s and possibly more

##### Note

Certaines personnes ne suivent pas cette règle parce qu'elles prévoient d'utiliser une classe uniquement via un `shared_ptr` : `std::shared_ptr<B> p = std::make_shared<D>(args);` Ici, le `shared_ptr` s'occupe de la destruction, donc aucune fuite ne se produit à cause d'un `delete` inapproprié de la base. Les personnes qui font cela de façon cohérente peuvent obtenir un faux‑positif, mais la règle reste importante — que se passe‑t‑il si l'on a alloué avec `make_unique` ? Ce n'est pas sûr à moins que l'auteur de `B` garantisse que cela ne peut jamais être mal utilisé, par ex. en rendant tous les constructeurs privés et en fournissant une fonction fabrique qui impose l'allocation avec `make_shared`.

##### Application

* Une classe avec des fonctions virtuelles doit avoir un destructeur qui est soit public et virtuel, soit protégé et non‑virtuel.
* Signaler le `delete` d'une classe avec fonction virtuelle mais sans destructeur virtuel.

### <a name="rh-override"></a>C.128 : Les fonctions virtuelles doivent spécifier exactement l'un de `virtual`, `override` ou `final`

##### Raison

Lisibilité. Détection d'erreurs. Écrire explicitement `virtual`, `override` ou `final` est auto‑documentaire et permet au compilateur de détecter les incompatibilités de types et/ou de noms entre les classes de base et dérivées. Cependant, écrire plus d'un de ces trois est redondant et source potentielle d'erreurs.

C'est simple et clair :

* `virtual` signifie exactement et uniquement « c'est une nouvelle fonction virtuelle ».
* `override` signifie exactement et uniquement « c'est un redéfinisseur non‑final ».
* `final` signifie exactement et uniquement « c'est un redéfinisseur final ».

##### Exemple, mauvais

    struct B {
        void f1(int);
        virtual void f2(int) const;
        virtual void f3(int);
        // ...
    };

    struct D : B {
        void f1(int);        // bad (hope for a warning): D::f1() hides B::f1()
        void f2(int) const;  // bad (but conventional and valid): no explicit override
        void f3(double);     // bad (hope for a warning): D::f3() hides B::f3()
        // ...
    };

##### Exemple, bon

    struct Better : B {
        void f1(int) override;        // error (caught): Better::f1() hides B::f1()
        void f2(int) const override;
        void f3(double) override;     // error (caught): Better::f3() hides B::f3()
        // ...
    };

#### Discussion

Nous voulons éliminer deux classes particulières d'erreurs :

* **implicit virtual** : le programmeur voulait que la fonction soit implicitement virtuelle et elle l'est (mais les lecteurs du code ne peuvent pas le voir) ; ou le programmeur voulait que la fonction soit implicitement virtuelle mais elle ne l'est pas (par ex. à cause d'une subtile différence de signature) ; ou le programmeur ne voulait pas que la fonction soit virtuelle mais elle l'est (parce qu'elle a la même signature qu'une fonction virtuelle de la base).
* **implicit override** : le programmeur voulait que la fonction soit implicitement un redéfinisseur et elle l'est (mais les lecteurs du code ne peuvent pas le voir) ; ou le programmeur voulait que la fonction soit implicitement un redéfinisseur mais elle ne l'est pas (par ex. à cause d'une subtile différence de signature) ; ou le programmeur ne voulait pas que la fonction soit un redéfinisseur mais elle l'est (parce qu'elle a la même signature qu'une fonction virtuelle de la base) — ce problème apparaît que la fonction soit explicitement déclarée `virtual` ou non, car le programmeur pourrait vouloir créer soit une nouvelle fonction virtuelle, soit une nouvelle fonction non‑virtuelle.

Note : sur une classe définie comme `final`, chaque fonction virtuelle individuelle devrait utiliser soit `override` soit `final` ; il n'y a pas de différence sémantique dans ce cas.

Note : Utilisez `final` sur les fonctions avec parcimonie. Cela ne conduit pas nécessairement à une optimisation et empêche toute dérivation ultérieure.

##### Application

* Comparer les noms de fonctions virtuelles dans les bases et dérivées et signaler les utilisations du même nom qui ne surchargent pas.
* Signaler les redéfinisseurs qui n'ont ni `override` ni `final`.
* Signaler les déclarations de fonction qui utilisent plus d'un de `virtual`, `override` et `final`.

### <a name="rh-kind"></a>C.129 : Lors de la conception d'une hiérarchie de classes, distinguer l'héritage d'implémentation de l'héritage d'interface

##### Raison

Les détails d'implémentation dans une interface rendent l'interface fragile ; les utilisateurs sont vulnérables à devoir recompiler après des changements d'implémentation. Les données dans une classe de base augmentent la complexité de l'implémentation de la base et peuvent entraîner une duplication de code.

Définition :

* l'héritage d'interface est l'utilisation de l'héritage pour séparer les utilisateurs des implémentations, en particulier pour permettre aux classes dérivées d'être ajoutées et modifiées sans affecter les utilisateurs des bases.
* l'héritage d'implémentation est l'utilisation de l'héritage pour simplifier l'implémentation de nouvelles fonctionnalités en rendant utiles les opérations disponibles pour les implémenteurs de nouvelles opérations liées (parfois appelé « programming by difference »).

Une classe d'interface pure est simplement un ensemble de fonctions virtuelles pures ; voir [I.25](005-interfaces.md#ri-abstract).

Dans les débuts de la POO (années 1980‑1990), l'héritage d'implémentation et d'interface étaient souvent mélangés et les mauvaises habitudes persistent. Même aujourd'hui, les mélanges ne sont pas rares dans les anciens codebases et le matériel d'enseignement ancien.

L'importance de garder les deux types d'héritage augmente

* avec la taille d'une hiérarchie (des dizaines de classes dérivées),
* avec la durée d'utilisation d'une hiérarchie (des décennies),
* avec le nombre d'organisations distinctes qui utilisent une hiérarchie (il peut être difficile de distribuer une mise à jour d'une classe de base).

##### Exemple, mauvais

    class Shape {   // BAD, mixed interface and implementation
    public:
        Shape();
        Shape(Point ce = {0, 0}, Color co = none): cent{ce}, col {co} { /* ... */}

        Point center() const { return cent; }
        Color color() const { return col; }

        virtual void rotate(int) = 0;
        virtual void move(Point p) { cent = p; redraw(); }

        virtual void redraw();

        // ...
    private:
        Point cent;
        Color col;
    };

    class Circle : public Shape {
    public:
        Circle(Point c, int r) : Shape{c}, rad{r} { /* ... */ }

        // ...
    private:
        int rad;
    };

    class Triangle : public Shape {
    public:
        Triangle(Point p1, Point p2, Point p3); // calculate center
        // ...
    };

Problèmes :

* À mesure que la hiérarchie grandit et que plus de données sont ajoutées à `Shape`, les constructeurs deviennent plus difficiles à écrire et à maintenir.
* Pourquoi calculer le centre pour le `Triangle` ? Nous pourrions ne jamais l'utiliser.
* Ajouter un membre à `Shape` (par ex. style de dessin ou canevas) implique que toutes les classes dérivées de `Shape` et tout le code utilisant `Shape` devront être revus, probablement modifiés, et probablement recompilés.

L'opération `Shape::move()` est un exemple d'héritage d'implémentation : nous avons défini `move()` une fois pour toutes, pour toutes les classes dérivées. Plus le code de ces fonctions membres de base est important et plus de données sont partagées en les plaçant dans la base, plus les bénéfices sont grands — et la hiérarchie devient moins stable.

##### Exemple

Cette hiérarchie de `Shape` peut être réécrite en utilisant l'héritage d'interface :

    class Shape {  // pure interface
    public:
        virtual Point center() const = 0;
        virtual Color color() const = 0;

        virtual void rotate(int) = 0;
        virtual void move(Point p) = 0;

        virtual void redraw() = 0;

        // ...
    };

    class Circle : public Shape {
    public:
        Circle(Point c, int r, Color c) : cent{c}, rad{r}, col{c} { /* ... */ }

        Point center() const override { return cent; }
        Color color() const override { return col; }

        // ...
    private:
        Point cent;
        int rad;
        Color col;
    };

L'interface est maintenant moins fragile, mais il y a plus de travail dans les fonctions membres. Par exemple, `center` doit être implémentée par chaque classe dérivée.

##### Exemple, hiérarchie double

Comment obtenir le bénéfice des hiérarchies stables des interfaces et de l'avantage de la réutilisation d'implémentation ? Une technique populaire est les hiérarchies doubles. Il existe de nombreuses façons d'implémenter l'idée de hiérarchies doubles ; ici, nous utilisons une variante d'héritage multiple.

Tout d'abord, nous concevons une hiérarchie de classes d'interface :

    class Shape {   // pure interface
    public:
        virtual Point center() const = 0;
        virtual Color color() const = 0;

        virtual void rotate(int) = 0;
        virtual void move(Point p) = 0;

        virtual void redraw() = 0;

        // ...
    };

    class Circle : public virtual Shape {   // pure interface
    public:
        virtual int radius() = 0;
        // ...
    };

Pour rendre cette interface utile, nous devons fournir des classes d'implémentation (ici, nommées de façon équivalente, mais dans l'espace de noms `Impl`) :

    class Impl::Shape : public virtual ::Shape { // implementation
    public:
        // constructors, destructor
        // ...
        Point center() const override { /* ... */ }
        Color color() const override { /* ... */ }

        void rotate(int) override { /* ... */ }
        void move(Point p) override { /* ... */ }

        void redraw() override { /* ... */ }

        // ...
    };

    class Impl::Circle : public virtual ::Circle, public Impl::Shape {   // implementation
    public:
        // constructors, destructor

        int radius() override { /* ... */ }
        // ...
    };

Et nous pourrions étendre les hiérarchies en ajoutant une classe `Smiley` :

    class Smiley : public virtual Circle { // pure interface
    public:
        // ...
    };

    class Impl::Smiley : public virtual ::Smiley, public Impl::Circle {   // implementation
    public:
        // constructors, destructor
        // ...
    }

Il y a maintenant deux hiérarchies :

* interface : Smiley → Circle → Shape
* implémentation : Impl::Smiley → Impl::Circle → Impl::Shape

Puisque chaque implémentation dérive également de son interface ainsi que de sa classe de base d'implémentation, nous obtenons un graphe en forme de DAG :

    Smiley     ->         Circle     ->  Shape
      ^                     ^               ^
      |                     |               |
    Impl::Smiley -> Impl::Circle -> Impl::Shape

Comme indiqué, cette technique n'est qu'une façon de construire une hiérarchie double.

L'implémentation peut être utilisée directement, sans passer par l'interface.

    void work_with_shape(Shape&);

    int user()
    {
        Impl::Smiley my_smiley{ /* args */ };   // create concrete shape
        // ...
        my_smiley.some_member();        // use implementation class directly
        // ...
        work_with_shape(my_smiley);     // use implementation through abstract interface
        // ...
    }

Ceci peut être utile lorsque la classe d'implémentation possède des membres qui ne sont pas offerts dans l'interface abstraite
ou si l'accès direct à un membre offre des opportunités d'optimisation (par ex. si un membre de fonction d'implémentation est `final`).

##### Note

Une technique connexe pour séparer interface et implémentation est le [Pimpl](005-interfaces.md#ri-pimpl).

##### Note

Il y a souvent un choix entre offrir une fonctionnalité commune comme fonctions de base (implémentées) et fonctions libres (dans un espace de noms d'implémentation). Les classes de base offrent une notation plus courte et un accès plus facile aux données partagées (dans la base) au prix d'une disponibilité de la fonctionnalité uniquement aux utilisateurs de la hiérarchie.

##### Application

* Signaler une conversion dérivée → base où la base possède à la fois des données et des fonctions virtuelles (sauf appels depuis un membre dérivé à un membre de base).

### <a name="rh-copy"></a>C.130 : Pour faire des copies profondes de classes polymorphes, privilégier une fonction virtuelle `clone` plutôt qu'un constructeur/assignation public

##### Raison

Copier une classe polymorphe est découragé à cause du problème du slicing, voir [C.67](007-class.md#rc-copy-virtual). Si vous avez réellement besoin d'une sémantique de copie, copiez en profondeur : fournissez une fonction virtuelle `clone` qui copiera le type le plus dérivé réel et renverra un pointeur propriétaire vers le nouvel objet, puis dans les classes dérivées, retournez le type dérivé (utilisez un type de retour covariant).

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
        // ...
    };

    class D : public B {
    public:
        gsl::owner<D*> clone() const override
        {
            return new D{*this};
        };
    };

En général, il est recommandé d'utiliser des pointeurs intelligents pour représenter la propriété (voir [R.20](009-resource.md#rr-owner)). Cependant, à cause des règles du langage, le type de retour covariant ne peut pas être un pointeur intelligent : `D::clone` ne peut pas retourner `unique_ptr<D>` alors que `B::clone` retourne `unique_ptr<B>`. Vous devez donc soit retourner `unique_ptr<B>` dans toutes les surcharges, soit utiliser le type `owner<>` de la [Guidelines Support Library](023-gsl.md#ss-views).

### <a name="rh-get"></a>C.131 : Éviter les getters et setters triviaux

##### Raison

Un getter ou setter trivial n'ajoute aucune valeur sémantique ; la donnée pourrait simplement être `public`.

##### Exemple

    class Point {   // Bad: verbose
        int x;
        int y;
    public:
        Point(int xx, int yy) : x{xx}, y{yy} { }
        int get_x() const { return x; }
        void set_x(int xx) { x = xx; }
        int get_y() const { return y; }
        void set_y(int yy) { y = yy; }
        // no behavioral member functions
    };

Considérez faire de telle classe un `struct` — c'est‑à‑dire, un groupe de variables sans comportement, toutes publiques et sans fonctions membres.

    struct Point {
        int x {0};
        int y {0};
    };

Notez que nous pouvons mettre des initialiseurs de membres par défaut : [C.49 : Préférer l'initialisation à l'assignation dans les constructeurs](007-class.md#rc-initialize).

##### Note

La clé de cette règle est de savoir si la sémantique du getter/setter est triviale. Bien que ce ne soit pas une définition complète de « trivial », demandez‑vous s'il y aurait une différence au‑delà de la syntaxe si le getter/setter était un membre de données public. Des sémantiques non triviales incluraient : maintenir une invariant de classe ou convertir entre un type interne et un type d'interface.

##### Application

Signaler plusieurs fonctions `get` et `set` qui accèdent simplement à un membre sans sémantique supplémentaire.

### <a name="rh-virtual"></a>C.132 : Ne pas rendre une fonction `virtual` sans raison

##### Raison

Une fonction `virtual` redondante augmente le temps d'exécution et la taille du code objet. Une fonction virtuelle peut être surchargée et est donc ouverte aux erreurs dans une classe dérivée. Une fonction virtuelle assure la réplication du code dans une hiérarchie de modèles.

##### Exemple, mauvais

    template<class T>
    class Vector {
    public:
        // ...
        virtual int size() const { return sz; }   // bad: what good could a derived class do?
    private:
        T* elem;   // the elements
        int sz;    // number of elements
    };

Cette sorte de « vector » n'est pas censée être utilisée comme classe de base du tout.

##### Application

* Signaler une classe avec des fonctions virtuelles mais aucune classe dérivée.
* Signaler une classe où toutes les fonctions membres sont virtuelles et ont des implémentations.

### <a name="rh-protected"></a>C.133 : Éviter les données `protected`

**Formulation alternative** : Rendre les données membres `public` ou (préférablement) `private`.

##### Raison

Les données `protected` sont une source de complexité et d'erreurs. Elles compliquent la déclaration d'invariants. Les données `protected` violent la directive contre le placement de données dans les classes d'interface, ce qui conduit généralement à devoir gérer l'héritage virtuel.

##### Exemple, mauvais

    class Shape {
    public:
        // ... interface functions ...
    protected:
        // data for use in derived classes:
        Color fill_color;
        Color edge_color;
        Style st;
    };

Maintenant, chaque classe dérivée de `Shape` doit manipuler correctement les données protégées. Cela a été populaire, mais c'est aussi une source majeure de problèmes de maintenance. Dans une grande hiérarchie de classes, le maintien de l'utilisation correcte des données protégées est difficile parce qu'il y a beaucoup de code, réparti sur de nombreuses classes. L'ensemble des classes qui peuvent toucher ces données est ouvert : n'importe qui peut dériver une nouvelle classe et commencer à manipuler les données protégées. Souvent, il n'est pas possible d'examiner l'ensemble complet des classes, donc toute modification de la représentation de la classe devient impossible. Il n'y a pas d'invariant appliqué aux données protégées ; c'est comme un ensemble de variables globales. Les données protégées sont devenues de facto globales pour un large corps de code.

##### Note

Les données protégées semblent tentantes pour permettre des améliorations arbitraires via la dérivation. Souvent, ce que vous obtenez est une modification non principielle et des erreurs.

> [Prefer `private` data](007-class.md#rc-private) avec un invariant bien spécifié et appliqué.
> Alternativement, [keep data out of any class used as an interface](007-class.md#rh-abstract).

##### Note

Les fonctions membres protégées peuvent très bien être.

##### Application

Signaler les classes avec des données `protected`.

### <a name="rh-public"></a>C.134 : Assurer que tous les membres non‑`const` ont le même niveau d'accès

##### Raison

Prévention de la confusion logique menant à des erreurs. Si les membres non‑`const` n'ont pas le même niveau d'accès, le type est confus quant à ce qu'il essaie de faire. S'agit‑il d'un type qui maintient une invariant ou simplement d'un agrégat de valeurs ?

##### Discussion

Il y a exactement deux catégories de membres de données :

* A : Ceux qui ne participent pas à l'invariant de l'objet. Toute combinaison de valeurs pour ces membres est valide.
* B : Ceux qui participent à l'invariant de l'objet. Toutes les combinaisons de valeurs ne sont pas significatives (sinon il n'y aurait pas d'invariant). Par conséquent, tout code qui a un accès en écriture à ces variables doit connaître l'invariant, la sémantique et appliquer les règles pour maintenir les valeurs correctes.

Les membres de catégorie A devraient simplement être `public` (ou, plus rarement, `protected` si vous ne voulez les exposer qu'aux classes dérivées). Ils n'ont pas besoin d'encapsulation. Tout le code du système pourrait tout aussi bien les voir et les manipuler.

Les membres de catégorie B devraient être `private` ou `const`. Cela est dû au fait que l'encapsulation est importante. Rendre ces membres non‑`private` et non‑`const` signifie que la classe ne peut pas contrôler son propre état : une quantité indéfinie de code au‑delà de la classe aurait besoin de connaître l'invariant et de le faire respecter (si les membres étaient `public`, ce serait tout le code appelant ; si `protected`, ce serait tout le code des classes dérivées). Cela conduit à du code fragile et fortement couplé qui devient rapidement un cauchemar à maintenir. Tout code qui modifie accidentellement les membres à un état invalide ou inattendu corromprait l'objet et toutes les utilisations ultérieures de l'objet.

La plupart des classes sont soit toutes A, soit toutes B :

* *Toutes publiques* : si vous écrivez un agrégat de variables sans invariant entre ces variables, alors toutes les variables devraient être `public`. [Par convention, déclarez de telles classes `struct`](007-class.md#rc-struct)
* *Toutes privées* : si vous écrivez un type qui maintient un invariant, alors tous les membres non‑`const` devraient être `private` ; cela devrait être encapsulé.

##### Exception

Occasionnellement, les classes mélangent A et B, généralement pour des raisons de débogage. Un objet encapsulé peut contenir, par exemple, des données de débogage non‑`const` qui ne font pas partie de l'invariant et qui tombent donc dans la catégorie A — ce n'est pas vraiment la partie « valeur » ou l'état observable du type non plus. Dans ce cas, les parties A devraient être traitées comme A (rendues `public`, ou dans de rares cas `protected` si elles ne doivent être visibles que par les classes dérivées) et les parties B devraient toujours être traitées comme B (`private` ou `const`).

##### Application

Signaler toute classe qui possède des membres non‑`const` avec des niveaux d'accès différents.

### <a name="rh-mi-interface"></a>C.135 : Utiliser l'héritage multiple pour représenter plusieurs interfaces distinctes

##### Raison

Toutes les classes ne supporteront pas forcément toutes les interfaces, et tous les appelants ne voudront pas forcément gérer toutes les opérations. En particulier, pour séparer les aspects de comportement pris en charge par une classe dérivée donnée.

##### Exemple

    class iostream : public istream, public ostream {   // very simplified
        // ...
    };

`istream` fournit l'interface aux opérations d'entrée ; `ostream` fournit l'interface aux opérations de sortie. `iostream` fournit l'union des interfaces `istream` et `ostream` ainsi que la synchronisation nécessaire pour permettre les deux sur un même flux.

##### Note

C'est un usage très commun de l'héritage car le besoin d'interfaces multiples pour un implémentateur est fréquent et ces interfaces ne sont souvent pas facilement organisées dans une hiérarchie à racine unique.

##### Note

Ces interfaces sont typiquement des classes abstraites.

##### Application

???

### <a name="rh-mi-implementation"></a>C.136 : Utiliser l'héritage multiple pour représenter l'union d'attributs d'implémentation

##### Raison

Certaines formes de mixins ont un état et souvent des opérations sur cet état. Si les opérations sont virtuelles, l'utilisation de l'héritage est nécessaire ; sinon, éviter l'héritage peut éviter le code boilerplate et le forwarding.

##### Exemple

    class iostream : public istream, public ostream {   // very simplified
        // ...
    };

`istream` fournit l'interface aux opérations d'entrée (et certaines données) ; `ostream` fournit l'interface aux opérations de sortie (et certaines données). `iostream` fournit l'union des interfaces `istream` et `ostream` ainsi que la synchronisation nécessaire pour permettre les deux sur un même flux.

##### Note

C'est relativement rare car l'implémentation peut souvent être organisée dans une hiérarchie à racine unique.

##### Exemple

Parfois, un « attribut d'implémentation » ressemble plus à un « mixin » qui détermine le comportement d'une implémentation et injecte des membres pour permettre l'implémentation des politiques qu'il requiert. Par exemple, voyez `std::enable_shared_from_this` ou diverses bases de Boost.Intrusive (par ex. `list_base_hook` ou `intrusive_ref_counter`).

##### Application

???

### <a name="rh-vbase"></a>C.137 : Utiliser des bases virtuelles pour éviter les classes de base trop générales

##### Raison

Permet la séparation des données partagées et de l'interface. Évite que toutes les données partagées soient placées dans une classe de base ultime.

##### Exemple

    struct Interface {
        virtual void f();
        virtual int g();
        // ... no data here ...
    };

    class Utility {  // with data
        void utility1();
        virtual void utility2();    // customization point
    public:
        int x;
        int y;
    };

    class Derive1 : public Interface, virtual protected Utility {
        // override Interface functions
        // Maybe override Utility virtual functions
        // ...
    };

    class Derive2 : public Interface, virtual protected Utility {
        // override Interface functions
        // Maybe override Utility virtual functions
        // ...
    };

Factoriser `Utility` a du sens si de nombreuses classes dérivées partagent des « détails d'implémentation ».

##### Note

Évidemment, l'exemple est trop « théorique », mais il est difficile de trouver un petit exemple réaliste. `Interface` est un exemple d'[interface hierarchy](007-class.md#rh-abstract). `Utility` est un exemple d'[implementation hierarchy](007-class.md#rh-kind).

##### Note

Souvent, la linéarisation d'une hiérarchie est une meilleure solution.

##### Application

Signaler les hiérarchies mixtes d'interface et d'implémentation.

### <a name="rh-using"></a>C.138 : Créer un ensemble de surcharges pour une classe dérivée et ses bases avec `using`

##### Raison

Sans une déclaration `using`, les fonctions membres de la classe dérivée masquent l'ensemble complet des surcharges héritées.

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
        std::cout << d.f(2) << '\n';   // prints "f(int): 3"
        std::cout << d.f(2.3) << '\n'; // prints "f(int): 3"
    }

##### Exemple, bon

    class D: public B {
    public:
        int f(int i) override { std::cout << "f(int): "; return i + 1; }
        using B::f; // exposes f(double)
    };

##### Note

Ce problème affecte à la fois les fonctions virtuelles et non‑virtuelles.

Pour les bases variadiques, C++17 a introduit une forme variadique de la déclaration `using` :

    template<class... Ts>
    struct Overloader : Ts... {
        using Ts::operator()...; // exposes operator() from every base
    };

##### Application

Diagnostiquer le masquage de noms.

### <a name="rh-final"></a>C.139 : Utiliser `final` sur les classes avec parcimonie

##### Raison

Capter une hiérarchie avec des classes `final` est rarement nécessaire pour des raisons logiques et peut nuire à l'extensibilité d'une hiérarchie.

##### Exemple, mauvais

    class Widget { /* ... */ };

    // nobody will ever want to improve My_widget (or so you thought)
    class My_widget final : public Widget { /* ... */ };

    class My_improved_widget : public My_widget { /* ... */ };  // error: can't do that

##### Note

Toutes les classes ne sont pas destinées à être des classes de base. La plupart des classes de la bibliothèque standard sont des exemples de cela (par ex. `std::vector` et `std::string` ne sont pas conçues pour être dérivées). Cette règle concerne l'utilisation de `final` sur les classes avec fonctions virtuelles destinées à être des interfaces pour une hiérarchie de classes.

##### Note

Les affirmations d'amélioration des performances grâce à `final` devraient être étayées. Trop souvent, ces affirmations sont basées sur des conjectures ou sur l'expérience avec d'autres langages.

Il existe des exemples où `final` peut être important tant logiquement que pour les performances. Un exemple est une hiérarchie AST (arbre syntaxique) complexe dans un compilateur ou un outil d'analyse de langage. Les classes dérivées ne sont pas ajoutées chaque année et ne le sont que par les implémenteurs de bibliothèques. Cependant, les mauvais usages sont (ou ont été) beaucoup plus fréquents.

##### Application

Signaler les utilisations de `final` sur les classes.

### <a name="rh-virtual-default-arg"></a>C.140 : Ne pas fournir des arguments par défaut différents pour une fonction virtuelle et un redéfinisseur

##### Raison

Cela peut créer de la confusion : un redéfinisseur n'hérite pas des arguments par défaut.

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

    b.multiply(10);  // these two calls will call the same function but
    d.multiply(10);  // with different arguments and so different results

##### Application

Signaler les arguments par défaut sur les fonctions virtuelles s'ils diffèrent entre les déclarations de base et de dérivation.

## C.hier-access : Accès aux objets dans une hiérarchie

### <a name="rh-poly"></a>C.145 : Accéder aux objets polymorphes via des pointeurs et références

##### Raison

Si vous avez une classe avec une fonction virtuelle, vous ne (en général) ne savez pas quelle classe a fourni la fonction à utiliser.

##### Exemple

    struct B { int a; virtual int f(); virtual ~B() = default };
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

Both `d`s are sliced.

##### Exception

You can safely access a named polymorphic object in the scope of its definition, just don't slice it.

    void use3()
    {
        D d;
        d.f();   // OK
    }

##### See also

[A polymorphic class should suppress copying](007-class.md#rc-copy-virtual)

##### Application

Signaler tout slicing.

### <a name="rh-dynamic_cast"></a>C.146 : Utiliser `dynamic_cast` lorsque la navigation dans la hiérarchie de classes est inévitable

##### Raison

`dynamic_cast` est vérifié à l'exécution.

##### Exemple

    struct B {   // an interface
        virtual void f();
        virtual void g();
        virtual ~B();
    };

    struct D : B {   // a wider interface
        void f() override;
        virtual void h();
    };

    void user(B* pb)
    {
        if (D* pd = dynamic_cast<D*>(pb)) {
            // ... use D's interface ...
        }
        else {
            // ... make do with B's interface ...
        }
    }

L'utilisation des autres casts peut violer la sécurité de type et amener le programme à accéder à une variable d'un type `X` réellement, mais traitée comme si elle était d'un type non‑lié `Z` :

    void user2(B* pb)   // bad
    {
        D* pd = static_cast<D*>(pb);    // I know that pb really points to a D; trust me
        // ... use D's interface ...
    }

    void user3(B* pb)    // unsafe
    {
        if (some_condition) {
            D* pd = static_cast<D*>(pb);   // I know that pb really points to a D; trust me
            // ... use D's interface ...
        }
        else {
            // ... make do with B's interface ...
        }
    }

    void f()
    {
        B b;

        user(&b);   // OK
        user2(&b);  // bad error
        user3(&b);  // OK *if* the programmer got the some_condition check right
    }

##### Note

`dynamic_cast` est souvent sur‑utilisé. [Prefer virtual functions to casting](007-class.md#rh-use-virtual). Prefer [static polymorphism](#???) where possible (no runtime resolution necessary) and reasonably convenient.

##### Note

Certaines personnes utilisent `dynamic_cast` où `typeid` aurait été plus approprié ; `dynamic_cast` est une opération « is‑kind » générale pour découvrir la meilleure interface d'un objet, alors que `typeid` est une opération « give‑me‑the‑exact‑type » pour découvrir le type exact d'un objet. La seconde est une opération plus simple qui devrait être plus rapide. La seconde (`typeid`) est facilement implémentable si nécessaire (par ex. si vous travaillez sur un système où RTTI est – pour une raison quelconque – prohibée), alors que `dynamic_cast` est beaucoup plus difficile à implémenter correctement en général.

Considérez :

    struct B {
        const char* name {"B"};
        // if pb1->id() == pb2->id() *pb1 is the same type as *pb2
        virtual const char* id() const { return name; }
        // ...
    };

    struct D : B {

        const char* name {"D"};
        const char* id() const override { return name; }
        // ...
    };

    void use()
    {
        B* pb1 = new B;
        B* pb2 = new D;

        cout << pb1->id(); // "B"
        cout << pb2->id(); // "D"


        if (pb2->id() == "D") {         // looks innocent
            D* pd = static_cast<D*>(pb2);
            // ...
        }
        // ...
    }

Le résultat de `pb2->id() == "D"` est en fait implémentation‑déterminé.
Nous l'avons ajouté pour avertir des dangers du RTTI maison.
Ce code pourrait fonctionner pendant des années, pour ne finalement échouer que sur une nouvelle machine, un nouveau compilateur ou un nouveau linker qui ne fusionne pas les littéraux de caractères.

Si vous implémentez votre propre RTTI, soyez prudent.

##### Exception

If your implementation provided a really slow `dynamic_cast`, you might have to use a workaround.
However, all workarounds that cannot be statically resolved involve explicit casting (typically `static_cast`) and are error‑prone.
You will basically be crafting your own special‑purpose `dynamic_cast`.
So, first make sure that your `dynamic_cast` really is as slow as you think it is (there are a fair number of unsupported rumors about)
and that your use of `dynamic_cast` is really performance critical.

In very rare cases, if you have measured that the `dynamic_cast` overhead is material, you have other means to statically guarantee that a downcast will succeed (e.g., you are using CRTP carefully), and there is no virtual inheritance involved, consider tactically using `static_cast` with a prominent comment and disclaimer summarizing this paragraph and that human attention is needed under maintenance because the type system can't verify correctness.

##### Exception

    template<typename B>
    class Dx : B {
        // ...
    };

##### Application

* Flag all uses of `static_cast` for downcasts, including C‑style casts that perform a `static_cast`.
* This rule is part of the [type‑safety profile](022-profile.md#pro-type-downcast).

### <a name="rh-ref-cast"></a>C.147 : Utiliser `dynamic_cast` vers un type référence lorsque l'échec à trouver la classe requise est considéré comme une erreur

##### Raison

Caster vers une référence exprime que vous avez l'intention d'obtenir un objet valide, donc le cast doit réussir. `dynamic_cast` lèvera alors une exception si cela ne réussit pas.

##### Exemple

    std::string f(Base& b)
