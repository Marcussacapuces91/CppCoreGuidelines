# <a name="s-class"></a>C : Classes et hiérarchies de classes

Une classe est un type défini par l'utilisateur, pour lequel un programmeur peut définir la représentation, les opérations et les interfaces.
Les hiérarchies de classes sont utilisées pour organiser des classes apparentées en structures hiérarchiques.

Résumé des règles sur les classes :

* [C.1 : Organiser les données apparentées dans des structures (`struct` ou `class`)](007-class.md#rc-org)
* [C.2 : Utiliser `class` si la classe a un invariant ; utiliser `struct` si les membres de données peuvent varier indépendamment](007-class.md#rc-struct)
* [C.3 : Représenter la distinction entre une interface et une implémentation à l'aide d'une classe](007-class.md#rc-interface)
* [C.4 : Rendre une fonction membre uniquement si elle a besoin d'un accès direct à la représentation d'une classe](007-class.md#rc-member)
* [C.5 : Placer les fonctions auxiliaires dans le même espace de noms que la classe qu'elles accompagnent](007-class.md#rc-helper)
* [C.7 : Ne pas définir une classe ou un enum et déclarer une variable de son type dans la même déclaration](007-class.md#rc-standalone)
* [C.8 : Utiliser `class` plutôt que `struct` si un membre est non public](007-class.md#rc-class)
* [C.9 : Minimiser l'exposition des membres](007-class.md#rc-private)

Sous-sections :

* [C.concrete : Types concrets](007-class.md#ss-concrete)
* [C.ctor : Constructeurs, affectations et destructeurs](007-class.md)
* [C.con : Conteneurs et autres gestionnaires de ressources](007-class.md#ss-containers)
* [C.lambdas : Objets de fonction et lambdas](007-class.md#ss-lambdas)
* [C.hier : Hiérarchies de classes (POO)](007-class.md#ss-hier)
* [C.over : Surcharge et opérateurs surchargés](007-class.md#ss-overload)
* [C.union : Unions](007-class.md#ss-union)

### <a name="rc-org"></a>C.1 : Organiser les données apparentées dans des structures (`struct` ou `class`)

##### Raison

Facilité de compréhension.
Si des données sont apparentées (pour des raisons fondamentales), ce fait doit être reflété dans le code.

##### Exemple

    void draw(int x, int y, int x2, int y2);  // MAUVAIS : relations implicites inutiles
    void draw(Point from, Point to);          // meilleur

##### Remarque

Une classe simple sans fonctions virtuelles n'implique aucun surcoût en espace ou en temps.

##### Remarque

D'un point de vue du langage, `class` et `struct` ne diffèrent que par la visibilité par défaut de leurs membres.

##### Application

Probablement impossible. Peut-être qu'une heuristique cherchant des éléments de données utilisés ensemble est possible.

### <a name="rc-struct"></a>C.2 : Utiliser `class` si la classe a un invariant ; utiliser `struct` si les membres de données peuvent varier indépendamment

##### Raison

Lisibilité.
Facilité de compréhension.
L'utilisation de `class` alerte le programmeur sur la nécessité d'un invariant.
C'est une convention utile.

##### Remarque

Un invariant est une condition logique sur les membres d'un objet qu'un constructeur doit établir pour que les fonctions membres publiques puissent l'assumer.
Après l'établissement de l'invariant (typiquement par un constructeur), chaque fonction membre peut être appelée sur l'objet.
Un invariant peut être énoncé informellement (par exemple, dans un commentaire) ou plus formellement à l'aide de `Expects`.

Si tous les membres de données peuvent varier indépendamment les uns des autres, aucun invariant n'est possible.

##### Exemple

    struct Pair {  // les membres peuvent varier indépendamment
        string name;
        int volume;
    };

mais :

    class Date {
    public:
        // valider que {yy, mm, dd} est une date valide et initialiser
        Date(int yy, Month mm, char dd);
        // ...
    private:
        int y;
        Month m;
        char d;    // jour
    };

##### Remarque

Si une classe a des données `private`, un utilisateur ne peut pas initialiser complètement un objet sans l'utilisation d'un constructeur.
Par conséquent, le définiteur de la classe fournira un constructeur et devra spécifier sa signification.
Cela signifie en pratique que le définiteur doit définir un invariant.

**Voir aussi** :

* [définir une classe avec des données privées en tant que `class`](007-class.md#rc-class)
* [Préférer de placer l'interface en premier dans une classe](024-naming.md#rl-order)
* [minimiser l'exposition des membres](007-class.md#rc-private)
* [Éviter les données `protected`](007-class.md#rh-protected)

##### Application

Chercher des `struct` avec toutes les données privées et des `class` avec des membres publics.

### <a name="rc-interface"></a>C.3 : Représenter la distinction entre une interface et une implémentation à l'aide d'une classe

##### Raison

Une distinction explicite entre interface et implémentation améliore la lisibilité et simplifie la maintenance.

##### Exemple

    class Date {
    public:
        Date();
        // valider que {yy, mm, dd} est une date valide et initialiser
        Date(int yy, Month mm, char dd);

        int day() const;
        Month month() const;
        // ...
    private:
        // ... une certaine représentation ...
    };

Par exemple, nous pouvons maintenant changer la représentation d'une `Date` sans affecter ses utilisateurs (la recompilation est probable, cependant).

##### Remarque

Utiliser une classe de cette manière pour représenter la distinction entre interface et implémentation n'est bien sûr pas la seule façon.
Par exemple, nous pouvons utiliser un ensemble de déclarations de fonctions autonomes dans un espace de noms, une classe de base abstraite, ou un modèle de fonction avec concepts pour représenter une interface.
Le point le plus important est de distinguer explicitement entre une interface et les « détails » de son implémentation.
Idéalement, et typiquement, une interface est beaucoup plus stable que ses implémentations.

##### Application

???

### <a name="rc-member"></a>C.4 : Rendre une fonction membre uniquement si elle a besoin d'un accès direct à la représentation d'une classe

##### Raison

Moins de couplage qu'avec des fonctions membres, moins de fonctions pouvant causer des problèmes en modifiant l'état d'un objet, réduit le nombre de fonctions devant être modifiées après un changement de représentation.

##### Exemple

    class Date {
        // ... interface relativement petite ...
    };

    // fonctions auxiliaires :
    Date next_weekday(Date);
    bool operator==(Date, Date);

Les « fonctions auxiliaires » n'ont pas besoin d'un accès direct à la représentation d'une `Date`.

##### Remarque

Cette règle devient encore meilleure si C++ obtient l'« appel de fonction uniforme » (["uniform function call"](https://www.open-std.org/jtc1/sc22/wg21/docs/papers/2016/p0251r0.pdf)).

##### Exception

Le langage exige que les fonctions `virtual` soient des membres, et toutes les fonctions `virtual` n'accèdent pas directement aux données.
En particulier, les membres d'une classe abstraite le font rarement.

Voir [les multi-méthodes](https://web.archive.org/web/20200605021759/https://parasol.tamu.edu/~yuriys/papers/OMM10.pdf).

##### Exception

Le langage exige que les opérateurs `=`, `()`, `[]` et `->` soient des membres.

##### Exception

Un ensemble de surcharges pourrait avoir certains membres qui n'accèdent pas directement aux données `private` :

    class Foobar {
    public:
        void foo(long x) { /* manipuler les données privées */ }
        void foo(double x) { foo(std::lround(x)); }
        // ...
    private:
        // ...
    };

##### Exception

De même, un ensemble de fonctions pourrait être conçu pour être utilisé en chaîne :

    x.scale(0.5).rotate(45).set_color(Color::red);

Typiquement, certaines mais pas toutes de ces fonctions accèdent directement aux données `private`.

##### Application

* Chercher des fonctions membres non `virtual` qui ne touchent pas directement les membres de données.
Le hic est que beaucoup de fonctions membres qui n'ont pas besoin de toucher directement les membres de données le font.
* Ignorer les fonctions `virtual`.
* Ignorer les fonctions faisant partie d'un ensemble de surcharges dont au moins une accède à des membres `private`.
* Ignorer les fonctions renvoyant `this`.

### <a name="rc-helper"></a>C.5 : Placer les fonctions auxiliaires dans le même espace de noms que la classe qu'elles accompagnent

##### Raison

Une fonction auxiliaire est une fonction (fournie généralement par l'auteur d'une classe) qui n'a pas besoin d'un accès direct à la représentation de la classe, mais qui est considérée comme faisant partie de l'interface utile de la classe.
Les placer dans le même espace de noms que la classe rend leur relation avec la classe évidente et permet qu'elles soient trouvées par la recherche dépendante des arguments (ADL).

##### Exemple

    namespace Chrono { // ici nous conservons les services liés au temps

        class Time { /* ... */ };
        class Date { /* ... */ };

        // fonctions auxiliaires :
        bool operator==(Date, Date);
        Date next_weekday(Date);
        // ...
    }

##### Remarque

C'est particulièrement important pour les [opérateurs surchargés](007-class.md#ro-namespace).

##### Application

* Signaler les fonctions globales prenant des arguments de types d'un seul espace de noms.

### <a name="rc-standalone"></a>C.7 : Ne pas définir une classe ou un enum et déclarer une variable de son type dans la même déclaration

##### Raison

Mélanger une définition de type et la définition d'une autre entité dans la même déclaration est confus et inutile.

##### Exemple, mauvais

    struct Data { /*...*/ } data{ /*...*/ };

##### Exemple, bon

    struct Data { /*...*/ };
    Data data{ /*...*/ };

##### Application

* Signaler si la `}` d'une définition de classe ou d'énumération n'est pas suivie d'un `;`. Le `;` est manquant.

### <a name="rc-class"></a>C.8 : Utiliser `class` plutôt que `struct` si un membre est non public

##### Raison

Lisibilité.
Pour rendre clair que quelque chose est caché/abstrait.
C'est une convention utile.

##### Exemple, mauvais

    struct Date {
        int d, m;

        Date(int i, Month m);
        // ... beaucoup de fonctions ...
    private:
        int y;  // année
    };

Il n'y a rien de mal avec ce code du point de vue des règles du langage C++,
mais presque tout est mal du point de vue de la conception.
Les données privées sont cachées loin des données publiques.
Les données sont réparties dans différentes parties de la déclaration de la classe.
Différentes parties des données ont des accès différents.
Tout cela diminue la lisibilité et complique la maintenance.

##### Remarque

Préférer de placer l'interface en premier dans une classe, [voir NL.16](024-naming.md#rl-order).

##### Application

Signaler les classes déclarées avec `struct` s'il y a un membre `private` ou `protected`.

### <a name="rc-private"></a>C.9 : Minimiser l'exposition des membres

##### Raison

Encapsulation.
Masquage d'information.
Minimiser la probabilité d'accès non intentionnel.
Cela simplifie la maintenance.

##### Exemple

    template<typename T, typename U>
    struct pair {
        T a;
        U b;
        // ...
    };

Peu importe ce que nous faisons dans la partie `//`, un utilisateur arbitraire d'une `pair` peut modifier arbitrairement et indépendamment ses `a` et `b`.
Dans une grande base de code, nous ne pouvons pas facilement trouver quel code fait quoi aux membres de `pair`.
Cela pourrait être exactement ce que nous voulons, mais si nous voulons forcer une relation entre les membres, nous devons les rendre `private`
et forcer cette relation (invariant) à travers les constructeurs et les fonctions membres.
Par exemple :

    class Distance {
    public:
        // ...
        double meters() const { return magnitude*unit; }
        void set_unit(double u)
        {
                // ... vérifier que u est un facteur de 10 ...
                // ... changer magnitude en conséquence ...
                unit = u;
        }
        // ...
    private:
        double magnitude;
        double unit;    // 1 est mètres, 1000 est kilomètres, 0.001 est millimètres, etc.
    };

##### Remarque

Si l'ensemble des utilisateurs directs d'un ensemble de variables ne peut pas être facilement déterminé, le type ou l'utilisation de cet ensemble ne peut pas être (facilement) modifié/amélioré.
Pour les données `public` et `protected`, c'est généralement le cas.

##### Exemple

Une classe peut fournir deux interfaces à ses utilisateurs.
Une pour les classes dérivées (`protected`) et une pour les utilisateurs généraux (`public`).
Par exemple, une classe dérivée pourrait être autorisée à sauter une vérification à l'exécution parce qu'elle a déjà garanti la correction :

    class Foo {
    public:
        int bar(int x) { check(x); return do_bar(x); }
        // ...
    protected:
        int do_bar(int x); // effectuer une opération sur les données
        // ...
    private:
        // ... données ...
    };

    class Dir : public Foo {
        //...
        int mem(int x, int y)
        {
            /* ... faire quelque chose ... */
            return do_bar(x + y); // OK : la classe dérivée peut contourner la vérification
        }
    };

    void user(Foo& x)
    {
        int r1 = x.bar(1);      // OK, effectuera la vérification
        int r2 = x.do_bar(2);   // erreur : contournerait la vérification
        // ...
    }

##### Remarque

[Les données `protected` sont une mauvaise idée](007-class.md#rh-protected).

##### Remarque

Préférer l'ordre : membres `public` avant membres `protected` avant membres `private` ; voir [NL.16](024-naming.md#rl-order).

##### Application

* [Signaler les données protected](007-class.md#rh-protected).
* Signaler les mélanges de données `public` et `private`

## <a name="ss-concrete"></a>C.concrete : Types concrets

Résumé des règles sur les types concrets :

* [C.10 : Préférer les types concrets aux hiérarchies de classes](007-class.md#rc-concrete)
* [C.11 : Rendre les types concrets réguliers](007-class.md#rc-regular)
* [C.12 : Ne pas rendre les membres de données `const` ou des références dans un type copiable ou déplaçable](007-class.md#rc-constref)
* [C.13 : Si le membre de données `B` utilise un autre membre de données `A`, déclarer `A` avant `B`](007-class.md#rc-lifetime)


### <a name="rc-concrete"></a>C.10 : Préférer les types concrets aux hiérarchies de classes

##### Raison

Un type concret est fondamentalement plus simple qu'un type dans une hiérarchie de classes :
plus facile à concevoir, plus facile à implémenter, plus facile à utiliser, plus facile à raisonner, plus petit et plus rapide.
Vous avez besoin d'une raison (cas d'usage) pour utiliser une hiérarchie.

##### Exemple

    class Point1 {
        int x, y;
        // ... opérations ...
        // ... pas de fonctions virtuelles ...
    };

    class Point2 {
        int x, y;
        // ... opérations, certaines virtuelles ...
        virtual ~Point2();
    };

    void use()
    {
        Point1 p11 {1, 2};   // créer un objet sur la pile
        Point1 p12 {p11};    // une copie

        auto p21 = make_unique<Point2>(1, 2);   // créer un objet sur la zone libre
        auto p22 = p21->clone();                // créer une copie
        // ...
    }

Si une classe fait partie d'une hiérarchie, nous (dans du code réel, même si ce n'est pas nécessairement dans de petits exemples) devons manipuler ses objets à travers des pointeurs ou des références.
Cela implique plus de surcoût mémoire, plus d'allocations et de désallocations, et plus de surcoût à l'exécution pour effectuer les indirections résultantes.

##### Remarque

Les types concrets peuvent être alloués sur la pile et être membres d'autres classes.

##### Remarque

L'utilisation de l'indirection est fondamentale pour les interfaces polymorphes à l'exécution.
Le surcoût d'allocation/désallocation ne l'est pas (c'est juste le cas le plus courant).
Nous pouvons utiliser une classe de base comme interface d'un objet à portée d'une classe dérivée.
Cela est fait là où l'allocation dynamique est interdite (par exemple, temps réel dur) et pour fournir une interface stable à certains types de modules.


##### Application

???


### <a name="rc-regular"></a>C.11 : Rendre les types concrets réguliers

##### Raison

Les types réguliers sont plus faciles à comprendre et à raisonner que les types non réguliers (les irrégularités nécessitent un effort supplémentaire pour les comprendre et les utiliser).

Les types intégrés de C++ sont réguliers, et de même pour les classes de la bibliothèque standard telles que `string`, `vector` et `map`. Les classes concrètes sans affectation et égalité peuvent être définies, mais elles sont (et devraient être) rares.

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

En particulier, si un type concret est copiable, préférer de lui donner également un opérateur de comparaison d'égalité, et s'assurer que `a = b` implique `a == b`.

##### Remarque

Pour les structures destinées à être partagées avec du code C, définir `operator==` peut ne pas être réalisable.

##### Remarque

Les gestionnaires de ressources qui ne peuvent pas être clonés, par exemple un `scoped_lock` pour un `mutex`, sont des types concrets mais ne peuvent généralement pas être copiés (au lieu de cela, ils peuvent généralement être déplacés),
donc ils ne peuvent pas être réguliers ; au lieu de cela, ils tendent à être uniquement déplaçables.

##### Application

???


### <a name="rc-constref"></a>C.12 : Ne pas rendre les membres de données `const` ou des références dans un type copiable ou déplaçable

##### Raison

Les membres de données `const` et les références ne sont pas utiles dans un type copiable ou déplaçable, et rendent de tels types difficiles à utiliser en les rendant au moins partiellement non copiables/non déplaçables pour des raisons subtiles.

##### Exemple ; mauvais

    class bad {
        const int i;    // mauvais
        string& s;      // mauvais
        // ...
    };

Les membres de données `const` et `&` rendent cette classe « seulement partiellement copiable » -- copiable par construction mais non copiable par affectation.

##### Remarque

Si vous avez besoin qu'un membre pointe vers quelque chose, utilisez un pointeur (brut ou intelligent, et `gsl::not_null` s'il ne doit pas être nul) au lieu d'une référence.

##### Application

Signaler un membre de données qui est `const`, `&` ou `&&` dans un type qui a une opération de copie ou de déplacement.


### <a name="rc-lifetime"></a>C.13 : Si le membre de données `B` utilise un autre membre de données `A`, déclarer `A` avant `B`

##### Raison

Les membres de données sont initialisés dans l'ordre dans lequel ils sont déclarés, et détruits dans l'ordre inverse.

##### Discussion

Si le membre de données `B` utilise un autre membre de données `A`, alors `A` doit être déclaré avant `B` afin que `A` survive à `B`, c'est-à-dire que la durée de vie de `A` commence avant et se termine après celle de `B`. Sinon, pendant la construction et la destruction, `B` tentera d'utiliser `A` en dehors de sa durée de vie.

##### Exemple ; mauvais

    // Mauvais : b utilise a, mais a est déclaré après b.
    //      L'ordre de construction est b puis a ; l'ordre de destruction est a puis b.
    //      Donc b touche a en dehors de la durée de vie de a.

    class X {
        struct B {
            string* p;
            explicit B(string& a) : p{&a} {}
            ~B() { cout << *p; }                       // utilise a (via p)
        };

        B      b;                                      // construit en premier
        string a = "some heap allocated string value"; // construit après b ; détruit avant b

    public:
        X() : b{a} {}   // utilise a avant qu'il soit construit -> UB d'utilisation avant allocation
        ~X() = default; // accède à a après qu'il est détruit -> UB d'utilisation après libération
    };

##### Exemple ; bon

    // Corrigé : il suffit de déclarer a avant b

    class X {
        struct B {
            string* p;
            explicit B(string& a) : p{&a} {}
            ~B() { cout << *p; }                       // utilise a (via p)
        };

        string a = "some heap allocated string value"; // construit avant b ; détruit après b
        B      b;                                      // construit en second

    public:
        X() : b{a} {}   // ok
        ~X() = default; // ok
    };

##### Exemple ; mauvais

Cela peut aussi se produire avec la concurrence. S'assurer qu'une opération asynchrone qui accède à une valeur est jointe avant que la valeur qu'elle accède ne soit détruite.

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

##### Exemple ; bon

Cela peut aussi se produire avec la concurrence. S'assurer qu'une opération asynchrone qui accède à une valeur est jointe avant que la valeur qu'elle accède ne soit détruite.

    // Corrigé : il suffit de déclarer a avant b

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

* Signaler un initialiseur de membre qui fait référence à un objet avant qu'il soit construit.


## <a name="s-ctor"></a>C.ctor : Constructeurs, affectations et destructeurs

Ces fonctions contrôlent le cycle de vie des objets : création, copie, déplacement et destruction.
Définir des constructeurs pour garantir et simplifier l'initialisation des classes.

Ce sont des *opérations par défaut* :

* un constructeur par défaut : `X()`
* un constructeur de copie : `X(const X&)`
* une affectation de copie : `operator=(const X&)`
* un constructeur de déplacement : `X(X&&)`
* une affectation de déplacement : `operator=(X&&)`
* un destructeur : `~X()`

Par défaut, le compilateur définit chacune de ces opérations si elle est utilisée, mais le comportement par défaut peut être supprimé.

Les opérations par défaut sont un ensemble d'opérations liées qui ensemble implémentent la sémantique du cycle de vie d'un objet.
Par défaut, C++ traite les classes comme des types de type valeur, mais tous les types ne sont pas de type valeur.

Règles sur l'ensemble des opérations par défaut :

* [C.20 : Si vous pouvez éviter de définir des opérations par défaut, faites-le](007-class.md#rc-zero)
* [C.21 : Si vous définissez ou `=delete` une fonction de copie, de déplacement ou de destructeur, définissez-les ou `=delete`-les toutes](007-class.md#rc-five)
* [C.22 : Rendre les opérations par défaut cohérentes](007-class.md#rc-matched)

Règles sur les destructeurs :

* [C.30 : Définir un destructeur si une classe a besoin d'une action explicite à la destruction de l'objet](007-class.md#rc-dtor)
* [C.31 : Toutes les ressources acquises par une classe doivent être libérées par le destructeur de la classe](007-class.md#rc-dtor-release)
* [C.32 : Si une classe a un pointeur brut (`T*`) ou une référence (`T&`), considérer si elle pourrait être propriétaire](007-class.md#rc-dtor-ptr)
* [C.33 : Si une classe a un membre pointeur propriétaire, définir un destructeur](007-class.md#rc-dtor-ptr2)
* [C.35 : Le destructeur d'une classe de base doit être soit public et virtuel, soit protégé et non virtuel](007-class.md#rc-dtor-virtual)
* [C.36 : Un destructeur ne doit pas échouer](007-class.md#rc-dtor-fail)
* [C.37 : Rendre les destructeurs `noexcept`](007-class.md#rc-dtor-noexcept)

Règles sur les constructeurs :

* [C.40 : Définir un constructeur si une classe a un invariant](007-class.md#rc-ctor)
* [C.41 : Un constructeur doit créer un objet entièrement initialisé](007-class.md#rc-complete)
* [C.42 : Si un constructeur ne peut pas construire un objet valide, lever une exception](007-class.md#rc-throw)
* [C.43 : S'assurer qu'une classe copiable a un constructeur par défaut](007-class.md#rc-default0)
* [C.44 : Préférer que les constructeurs par défaut soient simples et non levants](007-class.md#rc-default00)
* [C.45 : Ne pas définir un constructeur par défaut qui n'initialise que des membres de données ; utiliser des initialiseurs de membres par défaut à la place](007-class.md#rc-default)
* [C.46 : Par défaut, déclarer les constructeurs à un argument `explicit`](007-class.md#rc-explicit)
* [C.47 : Définir et initialiser les membres de données dans l'ordre de déclaration des membres](007-class.md#rc-order)
* [C.48 : Préférer les initialiseurs de membres par défaut aux initialiseurs de membres dans les constructeurs pour les initialiseurs constants](007-class.md#rc-in-class-initializer)
* [C.49 : Préférer l'initialisation à l'affectation dans les constructeurs](007-class.md#rc-initialize)
* [C.50 : Utiliser une fonction de fabrique si vous avez besoin d'un « comportement virtuel » pendant l'initialisation](007-class.md#rc-factory)
* [C.51 : Utiliser les constructeurs déléguants pour représenter les actions communes à tous les constructeurs d'une classe](007-class.md#rc-delegating)
* [C.52 : Utiliser les constructeurs hérités pour importer des constructeurs dans une classe dérivée qui n'a pas besoin d'initialisation explicite supplémentaire](007-class.md#rc-inheriting)

Règles sur la copie et le déplacement :

* [C.60 : Rendre l'affectation de copie non `virtual`, prendre le paramètre par `const&`, et renvoyer par non-`const&`](007-class.md#rc-copy-assignment)
* [C.61 : Une opération de copie doit copier](007-class.md#rc-copy-semantic)
* [C.62 : Rendre l'affectation de copie sûre pour l'auto-affectation](007-class.md#rc-copy-self)
* [C.63 : Rendre l'affectation de déplacement non `virtual`, prendre le paramètre par `&&`, et renvoyer par non-`const&`](007-class.md#rc-move-assignment)
* [C.64 : Une opération de déplacement doit déplacer et laisser sa source dans un état valide](007-class.md#rc-move-semantic)
* [C.65 : Rendre l'affectation de déplacement sûre pour l'auto-affectation](007-class.md#rc-move-self)
* [C.66 : Rendre les opérations de déplacement `noexcept`](007-class.md#rc-move-noexcept)
* [C.67 : Une classe polymorphe doit supprimer la copie/déplacement publics](007-class.md#rc-copy-virtual)

Règles sur les autres opérations par défaut :

* [C.80 : Utiliser `=default` si vous devez être explicite sur l'utilisation de la sémantique par défaut](007-class.md#rc-eqdefault)
* [C.81 : Utiliser `=delete` lorsque vous voulez désactiver le comportement par défaut (sans vouloir une alternative)](007-class.md#rc-delete)
* [C.82 : Ne pas appeler de fonctions virtuelles dans les constructeurs et destructeurs](007-class.md#rc-ctor-virtual)
* [C.83 : Pour les types de type valeur, envisager de fournir une fonction `swap` `noexcept`](007-class.md#rc-swap)
* [C.84 : Un `swap` ne doit pas échouer](007-class.md#rc-swap-fail)
* [C.85 : Rendre `swap` `noexcept`](007-class.md#rc-swap-noexcept)
* [C.86 : Rendre `==` symétrique par rapport aux types d'opérandes et `noexcept`](007-class.md#rc-eq)
* [C.87 : Se méfier de `==` sur les classes de base](007-class.md#rc-eq-base)
* [C.89 : Rendre un `hash` `noexcept`](007-class.md#rc-hash)
* [C.90 : S'appuyer sur les constructeurs et les opérateurs d'affectation, pas sur memset et memcpy](007-class.md#rc-memset)

## <a name="ss-defop"></a>C.defop : Opérations par défaut

Par défaut, le langage fournit les opérations par défaut avec leur sémantique par défaut.
Cependant, un programmeur peut désactiver ou remplacer ces valeurs par défaut.

### <a name="rc-zero"></a>C.20 : Si vous pouvez éviter de définir des opérations par défaut, faites-le

##### Raison

C'est le plus simple et donne la sémantique la plus propre.

##### Exemple

    struct Named_map {
    public:
        explicit Named_map(const string& n) : name(n) {}
        // pas de constructeurs de copie/déplacement
        // pas d'opérateurs d'affectation de copie/déplacement
        // pas de destructeur
    private:
        string name;
        map<int, int> rep;
    };

    Named_map nm("map"); // construire
    Named_map nm2 {nm};  // construire par copie

Puisque `std::map` et `string` ont toutes les fonctions spéciales, aucun travail supplémentaire n'est nécessaire.

##### Remarque

C'est connu sous le nom de « règle du zéro ».

##### Application

(Non applicable) Bien que non applicable, un bon analyseur statique peut détecter des motifs indiquant une amélioration possible pour respecter cette règle.
Par exemple, une classe avec une paire de membres (pointeur, taille) et un destructeur qui `delete` le pointeur pourrait probablement être convertie en `vector`.

### <a name="rc-five"></a>C.21 : Si vous définissez ou `=delete` une fonction de copie, de déplacement ou de destructeur, définissez-les ou `=delete`-les toutes

##### Raison

La sémantique de la copie, du déplacement et de la destruction est étroitement liée, donc si l'une doit être déclarée, il est probable que les autres nécessitent aussi une attention.

Déclarer n'importe quelle fonction de copie/déplacement/destructeur,
même en tant que `=default` ou `=delete`, supprimera la déclaration implicite
d'un constructeur de déplacement et d'un opérateur d'affectation de déplacement.
Déclarer un constructeur de déplacement ou un opérateur d'affectation de déplacement, même en tant que
`=default` ou `=delete`, entraînera qu'un constructeur de copie généré implicitement
ou un opérateur d'affectation de copie généré implicitement sera défini comme supprimé.
Dès qu'une de ces fonctions est déclarée, les autres devraient
toutes être déclarées pour éviter des effets indésirables comme transformer tous les déplacements potentiels
en copies plus coûteuses, ou rendre une classe uniquement déplaçable.

##### Exemple, mauvais

    struct M2 {   // mauvais : ensemble incomplet d'opérations de copie/déplacement/destructeur
    public:
        // ...
        // ... pas d'opérations de copie ou de déplacement ...
        ~M2() { delete[] rep; }
    private:
        pair<int, int>* rep;  // ensemble de paires terminé par zéro
    };

    void use()
    {
        M2 x;
        M2 y;
        // ...
        x = y;   // l'affectation par défaut
        // ...
    }

Étant donné qu'une « attention spéciale » était nécessaire pour le destructeur (ici, pour la désallocation), la probabilité que les opérateurs d'affectation de copie et de déplacement implicitement définis soient corrects est faible (ici, nous obtiendrions une double suppression).

##### Remarque

C'est connu sous le nom de « règle des cinq ».

##### Remarque

Si vous voulez une implémentation par défaut (tout en définissant une autre), écrivez `=default` pour montrer que vous le faites intentionnellement pour cette fonction.
Si vous ne voulez pas de fonction par défaut générée, supprimez-la avec `=delete`.

##### Exemple, bon

Lorsqu'un destructeur doit être déclaré juste pour le rendre `virtual`, il peut être
défini comme par défaut.

    class AbstractBase {
    public:
        virtual void foo() = 0;  // au moins une méthode abstraite pour rendre la classe abstraite
        virtual ~AbstractBase() = default;
        // ...
    };

Pour empêcher le tranchage conformément à [C.67](007-class.md#rc-copy-virtual),
rendre les opérations de copie et de déplacement protégées ou `=delete`, et ajouter un `clone` :

    class CloneableBase {
    public:
        virtual unique_ptr<CloneableBase> clone() const;
        virtual ~CloneableBase() = default;
        CloneableBase() = default;
        CloneableBase(const CloneableBase&) = delete;
        CloneableBase& operator=(const CloneableBase&) = delete;
        CloneableBase(CloneableBase&&) = delete;
        CloneableBase& operator=(CloneableBase&&) = delete;
        // ... autres constructeurs et fonctions ...
    };

Définir uniquement les opérations de déplacement ou uniquement les opérations de copie aurait le
même effet ici, mais énoncer l'intention explicitement pour chaque membre spécial
le rend plus évident pour le lecteur.

##### Remarque

Les compilateurs appliquent une grande partie de cette règle et idéalement émettent un avertissement pour toute violation.

##### Remarque

S'appuyer sur une opération de copie implicitement générée dans une classe avec un destructeur est déprécié.

##### Remarque

Écrire ces fonctions peut être source d'erreurs.
Notez leurs types d'arguments :

    class X {
    public:
        // ...
        virtual ~X() = default;               // destructeur (virtuel si X est censé être une classe de base)
        X(const X&) = default;                // constructeur de copie
        X& operator=(const X&) = default;     // affectation de copie
        X(X&&) noexcept = default;            // constructeur de déplacement
        X& operator=(X&&) noexcept = default; // affectation de déplacement
    };

Une petite erreur (telle qu'une faute de frappe, l'omission d'un `const`, l'utilisation de `&` au lieu de `&&`, ou l'omission d'une fonction spéciale) peut conduire à des erreurs ou des avertissements.
Pour éviter la fastidie
