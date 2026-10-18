# <a name="s-class"></a>C : Classes et hiérarchies de classes

Une classe est un type défini par l'utilisateur, pour lequel un programmeur peut définir la représentation, les opérations et les interfaces.
Les hiérarchies de classes sont utilisées pour organiser les classes apparentées en structures hiérarchiques.

Résumé des règles sur les classes :

* [C.1 : Organiser les données apparentées dans des structures (`struct` ou `class`)](007-class.md#rc-org)
* [C.2 : Utiliser `class` si la classe a un invariant ; utiliser `struct` si les membres de données peuvent varier indépendamment](007-class.md#rc-struct)
* [C.3 : Représenter la distinction entre une interface et une implémentation à l'aide d'une classe](007-class.md#rc-interface)
* [C.4 : Rendre une fonction membre uniquement si elle a besoin d'un accès direct à la représentation d'une classe](007-class.md#rc-member)
* [C.5 : Placer les fonctions auxiliaires dans le même espace de noms que la classe qu'elles accompagnent](007-class.md#rc-helper)
* [C.7 : Ne pas définir une classe ou un enum et déclarer une variable de ce type dans la même déclaration](007-class.md#rc-standalone)
* [C.8 : Utiliser `class` plutôt que `struct` si un membre n'est pas public](007-class.md#rc-class)
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
Si des données sont apparentées (pour des raisons fondamentales), ce fait devrait être reflété dans le code.

##### Exemple

    void draw(int x, int y, int x2, int y2);  // MAUVAIS : relations implicites inutiles
    void draw(Point from, Point to);          // mieux

##### Remarque

Une classe simple sans fonctions virtuelles n'implique aucun surcoût en mémoire ou en temps.

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

Un invariant est une condition logique sur les membres d'un objet qu'un constructeur doit établir pour que les fonctions membres publiques puissent en faire l'hypothèse.
Après l'établissement de l'invariant (typiquement par un constructeur), chaque fonction membre peut être appelée sur l'objet.
Un invariant peut être formulé informellement (par exemple dans un commentaire) ou plus formellement à l'aide de `Expects`.

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

Si une classe a des données `private`, un utilisateur ne peut pas initialiser complètement un objet sans utiliser un constructeur.
Par conséquent, le défineur de la classe fournira un constructeur et devra spécifier sa signification.
Cela signifie de fait que le défineur doit définir un invariant.

**Voir aussi** :

* [définir une classe avec des données privées comme `class`](007-class.md#rc-class)
* [Préférer de placer l'interface en premier dans une classe](024-naming.md#rl-order)
* [minimiser l'exposition des membres](007-class.md#rc-private)
* [Éviter les données `protected`](007-class.md#rh-protected)

##### Application

Chercher des `struct` dont toutes les données sont privées et des `class` avec des membres publics.

### <a name="rc-interface"></a>C.3 : Représenter la distinction entre une interface et une implémentation à l'aide d'une classe

##### Raison

Une distinction explicite entre l'interface et l'implémentation améliore la lisibilité et simplifie la maintenance.

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
        // ... quelque représentation ...
    };

Par exemple, nous pouvons maintenant changer la représentation d'un `Date` sans affecter ses utilisateurs (la recompilation est probable, cependant).

##### Remarque

L'utilisation d'une classe de cette manière pour représenter la distinction entre interface et implémentation n'est pas la seule façon, bien sûr.
Par exemple, nous pouvons utiliser un ensemble de déclarations de fonctions libres dans un espace de noms, une classe de base abstraite, ou un modèle de fonction avec des concepts pour représenter une interface.
La question la plus importante est de distinguer explicitement entre une interface et les « détails » de son implémentation.
Idéalement, et typiquement, une interface est bien plus stable que son/ses implémentation(s).

##### Application

???

### <a name="rc-member"></a>C.4 : Rendre une fonction membre uniquement si elle a besoin d'un accès direct à la représentation d'une classe

##### Raison

Moins de couplage que avec les fonctions membres, moins de fonctions pouvant causer des problèmes en modifiant l'état d'un objet, réduit le nombre de fonctions devant être modifiées après un changement de représentation.

##### Exemple

    class Date {
        // ... interface relativement petite ...
    };

    // fonctions auxiliaires :
    Date next_weekday(Date);
    bool operator==(Date, Date);

Les « fonctions auxiliaires » n'ont pas besoin d'un accès direct à la représentation d'un `Date`.

##### Remarque

Cette règle devient encore meilleure si C++ obtient l'« appel uniforme de fonctions » ([uniform function call](https://www.open-std.org/jtc1/sc22/wg21/docs/papers/2016/p0251r0.pdf)).

##### Exception

Le langage exige que les fonctions `virtual` soient des membres, et toutes les fonctions `virtual` n'accèdent pas directement aux données.
En particulier, les membres d'une classe abstraite le font rarement.

Voir [méthodes multiples](https://web.archive.org/web/20200605021759/https://parasol.tamu.edu/~yuriys/papers/OMM10.pdf).

##### Exception

Le langage exige que les opérateurs `=`, `()`, `[]` et `->` soient des membres.

##### Exception

Un ensemble de surcharge peut avoir des membres qui n'accèdent pas directement aux données `private` :

    class Foobar {
    public:
        void foo(long x) { /* manipuler les données privées */ }
        void foo(double x) { foo(std::lround(x)); }
        // ...
    private:
        // ...
    };

##### Exception

De manière similaire, un ensemble de fonctions peut être conçu pour être utilisé en chaîne :

    x.scale(0.5).rotate(45).set_color(Color::red);

Typiquement, certaines de ces fonctions (mais pas toutes) accèdent directement aux données `private`.

##### Application

* Chercher des fonctions membres non-`virtual` qui ne touchent pas directement les membres de données.
L'obstacle est que de nombreuses fonctions membres qui n'ont pas besoin de toucher les membres de données directement le font.
* Ignorer les fonctions `virtual`.
* Ignorer les fonctions faisant partie d'un ensemble de surcharge dont au moins une fonction accède à des membres `private`.
* Ignorer les fonctions renvoyant `this`.

### <a name="rc-helper"></a>C.5 : Placer les fonctions auxiliaires dans le même espace de noms que la classe qu'elles accompagnent

##### Raison

Une fonction auxiliaire est une fonction (fournie généralement par l'auteur d'une classe) qui n'a pas besoin d'un accès direct à la représentation de la classe, mais qui est considérée comme faisant partie de l'interface utile de la classe.
Les placer dans le même espace de noms que la classe rend leur relation avec la classe évidente et permet qu'elles soient trouvées par la recherche dépendante des arguments (ADL).

##### Exemple

    namespace Chrono { // ici nous gardons les services liés au temps

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

### <a name="rc-standalone"></a>C.7 : Ne pas définir une classe ou un enum et déclarer une variable de ce type dans la même déclaration

##### Raison

Mélanger une définition de type et la définition d'une autre entité dans la même déclaration est confusionnant et inutile.

##### Exemple, mauvais

    struct Data { /*...*/ } data{ /*...*/ };

##### Exemple, bon

    struct Data { /*...*/ };
    Data data{ /*...*/ };

##### Application

* Signaler si la `}` d'une définition de classe ou d'enumération n'est pas suivie d'un `;`. Le `;` est manquant.

### <a name="rc-class"></a>C.8 : Utiliser `class` plutôt que `struct` si un membre n'est pas public

##### Raison

Lisibilité.
Pour rendre clair que quelque chose est masqué/abstrait.
C'est une convention utile.

##### Exemple, mauvais

    struct Date {
        int d, m;

        Date(int i, Month m);
        // ... beaucoup de fonctions ...
    private:
        int y;  // année
    };

Il n'y a rien de mal avec ce code d'un point de vue des règles du langage C++,
mais presque tout est faux d'un point de vue de la conception.
Les données privées sont masquées loin des données publiques.
Les données sont divisées dans différentes parties de la déclaration de classe.
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
Minimiser la possibilité d'accès non intentionnel.
Cela simplifie la maintenance.

##### Exemple

    template<typename T, typename U>
    struct pair {
        T a;
        U b;
        // ...
    };

Peu importe ce que nous faisons dans la partie `//`, un utilisateur arbitraire d'une `pair` peut arbitrairement et indépendamment changer son `a` et son `b`.
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
        int r1 = x.bar(1);      // OK, vérifiera
        int r2 = x.do_bar(2);   // erreur : contournerait la vérification
        // ...
    }

##### Remarque

[Les données `protected` sont une mauvaise idée](007-class.md#rh-protected).

##### Remarque

Préférer l'ordre : membres `public` avant les membres `protected` avant les membres `private` ; voir [NL.16](024-naming.md#rl-order).

##### Application

* [Signaler les données protected](007-class.md#rh-protected).
* Signaler les mélanges de données `public` et `private`

## <a name="ss-concrete"></a>C.concrete : Types concrets

Résumé des règles sur les types concrets :

* [C.10 : Privilégier les types concrets aux hiérarchies de classes](007-class.md#rc-concrete)
* [C.11 : Rendre les types concrets réguliers](007-class.md#rc-regular)
* [C.12 : Ne pas rendre les membres de données `const` ou des références dans un type copiable ou déplaçable](007-class.md#rc-constref)
* [C.13 : Si le membre de données `B` utilise un autre membre de données `A`, déclarer `A` avant `B`](007-class.md#rc-lifetime)


### <a name="rc-concrete"></a>C.10 : Privilégier les types concrets aux hiérarchies de classes

##### Raison

Un type concret est fondamentalement plus simple qu'un type dans une hiérarchie de classes :
plus facile à concevoir, plus facile à implémenter, plus facile à utiliser, plus facile à raisonner, plus petit et plus rapide.
Il faut une raison (cas d'utilisation) pour utiliser une hiérarchie.

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

        auto p21 = make_unique<Point2>(1, 2);   // créer un objet sur le tas
        auto p22 = p21->clone();                // faire une copie
        // ...
    }

Si une classe fait partie d'une hiérarchie, nous (dans du code réel, même si ce n'est pas nécessairement le cas dans de petits exemples) devons manipuler ses objets à travers des pointeurs ou des références.
Cela implique plus de surcoût mémoire, plus d'allocation et de libération, et plus de surcoût à l'exécution pour effectuer les indirections résultantes.

##### Remarque

Les types concrets peuvent être alloués sur la pile et être membres d'autres classes.

##### Remarque

L'utilisation de l'indirection est fondamentale pour les interfaces polymorphiques à l'exécution.
Le surcoût d'allocation/libération ne l'est pas (c'est juste le cas le plus courant).
Nous pouvons utiliser une classe de base comme interface d'un objet englobé d'une classe dérivée.
Cela est fait là où l'allocation dynamique est interdite (par exemple temps réel dur) et pour fournir une interface stable à certains types de modules.


##### Application

???


### <a name="rc-regular"></a>C.11 : Rendre les types concrets réguliers

##### Raison

Les types réguliers sont plus faciles à comprendre et à raisonner que les types irréguliers (les irrégularités nécessitent un effort supplémentaire pour les comprendre et les utiliser).

Les types intégrés de C++ sont réguliers, et de même pour les classes de la bibliothèque standard comme `string`, `vector` et `map`. Des classes concrètes sans affectation ni égalité peuvent être définies, mais elles sont (et devraient être) rares.

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

En particulier, si un type concret est copiable, préférer aussi lui fournir un opérateur de comparaison d'égalité, et s'assurer que `a = b` implique `a == b`.

##### Remarque

Pour les structures destinées à être partagées avec du code C, la définition de `operator==` peut ne pas être faisable.

##### Remarque

Les gestionnaires de ressources qui ne peuvent pas être dupliqués, par exemple un `scoped_lock` pour un `mutex`, sont des types concrets mais ne peuvent généralement pas être copiés (en revanche, ils peuvent généralement être déplacés),
ils ne peuvent donc pas être réguliers ; au lieu de cela, ils tendent à être exclusivement déplaçables.

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

Les membres de données `const` et `&` rendent cette classe « seulement partiellement copiable » — construisible par copie mais pas affectable par copie.

##### Remarque

Si vous avez besoin qu'un membre pointe vers quelque chose, utilisez un pointeur (brut ou intelligent, et `gsl::not_null` s'il ne doit pas être nul) au lieu d'une référence.

##### Application

Signaler un membre de données qui est `const`, `&` ou `&&` dans un type qui a une opération de copie ou de déplacement.


### <a name="rc-lifetime"></a>C.13 : Si le membre de données `B` utilise un autre membre de données `A`, déclarer `A` avant `B`

##### Raison

Les membres de données sont initialisés dans l'ordre dans lequel ils sont déclarés, et détruits dans l'ordre inverse.

##### Discussion

Si le membre de données `B` utilise un autre membre de données `A`, alors `A` doit être déclaré avant `B` afin que `A` survive à `B`, ce qui signifie que la durée de vie de `A` commence avant et se termine après celle de `B`. Sinon, lors de la construction et de la destruction, `B` tentera d'utiliser `A` en dehors de sa durée de vie.

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
        X() : b{a} {}   // utilise a avant qu'il soit construit -> utilisation avant allocation (UB)
        ~X() = default; // accède à a après qu'il a été détruit -> utilisation après libération (UB)
    };

##### Exemple ; bon

    // Corrigé : simplement déclarer a avant b

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

Cela peut aussi se présenter avec la concurrence. Assurez-vous qu'une opération asynchrone qui accède à une valeur est jointe avant que la valeur à laquelle elle accède soit détruite.

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

Cela peut aussi se présenter avec la concurrence. Assurez-vous qu'une opération asynchrone qui accède à une valeur est jointe avant que la valeur à laquelle elle accède soit détruite.

    // Corrigé : simplement déclarer a avant b

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
Définissez des constructeurs pour garantir et simplifier l'initialisation des classes.

Ce sont les *opérations par défaut* :

* un constructeur par défaut : `X()`
* un constructeur de copie : `X(const X&)`
* une affectation de copie : `operator=(const X&)`
* un constructeur de déplacement : `X(X&&)`
* une affectation de déplacement : `operator=(X&&)`
* un destructeur : `~X()`

Par défaut, le compilateur définit chacune de ces opérations s'il y a lieu, mais le comportement par défaut peut être supprimé.

Les opérations par défaut sont un ensemble d'opérations apparentées qui ensemble implémentent la sémantique de cycle de vie d'un objet.
Par défaut, C++ traite les classes comme des types de valeur, mais tous les types ne sont pas de type valeur.

Ensemble de règles sur les opérations par défaut :

* [C.20 : Si vous pouvez éviter de définir des opérations par défaut, faites-le](007-class.md#rc-zero)
* [C.21 : Si vous définissez ou `=delete` une fonction de copie, de déplacement ou de destructeur, définissez-les ou supprimez-les toutes](007-class.md#rc-five)
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
* [C.41 : Un constructeur devrait créer un objet entièrement initialisé](007-class.md#rc-complete)
* [C.42 : Si un constructeur ne peut pas construire un objet valide, lever une exception](007-class.md#rc-throw)
* [C.43 : S'assurer qu'une classe copiable a un constructeur par défaut](007-class.md#rc-default0)
* [C.44 : Privilégier les constructeurs par défaut simples et non lanceurs d'exception](007-class.md#rc-default00)
* [C.45 : Ne pas définir un constructeur par défaut qui n'initialise que les membres de données ; utiliser des initialiseurs de membres par défaut à la place](007-class.md#rc-default)
* [C.46 : Par défaut, déclarer les constructeurs à un seul argument `explicit`](007-class.md#rc-explicit)
* [C.47 : Définir et initialiser les membres de données dans l'ordre de déclaration des membres](007-class.md#rc-order)
* [C.48 : Privilégier les initialiseurs de membres par défaut aux initialiseurs de membres dans les constructeurs pour les initialiseurs constants](007-class.md#rc-in-class-initializer)
* [C.49 : Privilégier l'initialisation à l'affectation dans les constructeurs](007-class.md#rc-initialize)
* [C.50 : Utiliser une fonction fabrique si vous avez besoin d'un « comportement virtuel » lors de l'initialisation](007-class.md#rc-factory)
* [C.51 : Utiliser les constructeurs délégants pour représenter les actions communes à tous les constructeurs d'une classe](007-class.md#rc-delegating)
* [C.52 : Utiliser les constructeurs hérités pour importer des constructeurs dans une classe dérivée qui n'a pas besoin d'initialisation explicite supplémentaire](007-class.md#rc-inheriting)

Règles sur la copie et le déplacement :

* [C.60 : Rendre l'affectation de copie non-`virtual`, prendre le paramètre par `const&`, et renvoyer par référence non-`const`](007-class.md#rc-copy-assignment)
* [C.61 : Une opération de copie devrait copier](007-class.md#rc-copy-semantic)
* [C.62 : Rendre l'affectation de copie sûre pour l'auto-affectation](007-class.md#rc-copy-self)
* [C.63 : Rendre l'affectation de déplacement non-`virtual`, prendre le paramètre par `&&`, et renvoyer par référence non-`const`](007-class.md#rc-move-assignment)
* [C.64 : Une opération de déplacement devrait déplacer et laisser sa source dans un état valide](007-class.md#rc-move-semantic)
* [C.65 : Rendre l'affectation de déplacement sûre pour l'auto-affectation](007-class.md#rc-move-self)
* [C.66 : Rendre les opérations de déplacement `noexcept`](007-class.md#rc-move-noexcept)
* [C.67 : Une classe polymorphe devrait supprimer la copie/déplacement publics](007-class.md#rc-copy-virtual)

Autres règles sur les opérations par défaut :

* [C.80 : Utiliser `=default` si vous devez être explicite sur l'utilisation de la sémantique par défaut](007-class.md#rc-eqdefault)
* [C.81 : Utiliser `=delete` quand vous voulez désactiver le comportement par défaut (sans vouloir d'alternative)](007-class.md#rc-delete)
* [C.82 : Ne pas appeler de fonctions virtuelles dans les constructeurs et destructeurs](007-class.md#rc-ctor-virtual)
* [C.83 : Pour les types de valeur, considérer la fourniture d'une fonction `swap` `noexcept`](007-class.md#rc-swap)
* [C.84 : Un `swap` ne doit pas échouer](007-class.md#rc-swap-fail)
* [C.85 : Rendre `swap` `noexcept`](007-class.md#rc-swap-noexcept)
* [C.86 : Rendre `==` symétrique par rapport aux types d'opérandes et `noexcept`](007-class.md#rc-eq)
* [C.87 : Méfiez-vous de `==` sur les classes de base](007-class.md#rc-eq-base)
* [C.89 : Rendre un `hash` `noexcept`](007-class.md#rc-hash)
* [C.90 : S'appuyer sur les constructeurs et les opérateurs d'affectation, pas sur memset et memcpy](007-class.md#rc-memset)

## <a name="ss-defop"></a>C.defop : Opérations par défaut

Par défaut, le langage fournit les opérations par défaut avec leur sémantique par défaut.
Cependant, un programmeur peut désactiver ou remplacer ces valeurs par défaut.

### <a name="rc-zero"></a>C.20 : Si vous pouvez éviter de définir des opérations par défaut, faites-le

##### Raison

C'est le plus simple et donne les sémantiques les plus propres.

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

C'est connu sous le nom de « règle de zéro ».

##### Application

(Ne peut pas être appliquée) Bien qu'elle ne puisse pas être appliquée automatiquement, un bon analyseur statique peut détecter des motifs indiquant une amélioration possible pour respecter cette règle.
Par exemple, une classe avec une paire de membres (pointeur, taille) et un destructeur qui `delete` le pointeur pourrait probablement être convertie en `vector`.

### <a name="rc-five"></a>C.21 : Si vous définissez ou `=delete` une fonction de copie, de déplacement ou de destructeur, définissez-les ou supprimez-les toutes

##### Raison

Les sémantiques de la copie, du déplacement et de la destruction sont étroitement liées, donc si l'une doit être déclarée, il est probable que d'autres nécessitent aussi une réflexion.

Déclarer n'importe quelle fonction de copie/déplacement/destructeur,
même en `=default` ou `=delete`, supprimera la déclaration implicite
du constructeur de déplacement et de l'opérateur d'affectation de déplacement.
Déclarer un constructeur de déplacement ou un opérateur d'affectation de déplacement, même en
`=default` ou `=delete`, entraînera qu'un constructeur de copie implicitement généré
ou un opérateur d'affectation de copie implicitement généré sera défini comme supprimé.
Dès lors qu'une de ces fonctions est déclarée, les autres devraient
toutes être déclarées pour éviter des effets indésirables comme transformer tous les déplacements potentiels
en copies plus coûteuses, ou rendre une classe exclusivement déplaçable.

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

Étant donné qu'une « attention spéciale » était nécessaire pour le destructeur (ici, pour libérer la mémoire), la probabilité que les opérateurs d'affectation de copie et de déplacement implicitement définis soient corrects est faible (ici, nous aurions une double libération).

##### Remarque

C'est connu sous le nom de « règle de cinq ».

##### Remarque

Si vous voulez une implémentation par défaut (en définissant une autre), écrivez `=default` pour montrer que vous le faites intentionnellement pour cette fonction.
Si vous ne voulez pas de fonction par défaut générée, supprimez-la avec `=delete`.

##### Exemple, bon

Lorsqu'un destructeur doit être déclaré simplement pour le rendre `virtual`, il peut être
défini comme par défaut.

    class AbstractBase {
    public:
        virtual void foo() = 0;  // au moins une méthode abstraite pour rendre la classe abstraite
        virtual ~AbstractBase() = default;
        // ...
    };

Pour empêcher la découpe conformément à [C.67](007-class.md#rc-copy-virtual),
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
même effet ici, mais indiquer l'intention explicitement pour chaque membre spécial
le rend plus évident pour le lecteur.

##### Remarque

Les compilateurs appliquent une grande partie de cette règle et idéalement émettent un avertissement pour toute violation.

##### Remarque

S'appuyer sur une opération de copie implicitement générée dans une classe avec un destructeur est déconseillé.

##### Remarque

L'écriture de ces fonctions peut être source d'erreurs.
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

Une petite erreur (comme une coquille, l'omission d'un `const`, l'utilisation de `&` au lieu de `&&`, ou l'omission d'une fonction spéciale) peut conduire à des erreurs ou des avertissements.
Pour éviter la fastidieuse et la possibilité d'erreurs, essayez de suivre la [règle de zéro](007-class.md#rc-zero).

##### Application

(Simple) Une classe devrait avoir une déclaration (même en `=delete`) pour toutes ou aucune des fonctions de copie/déplacement/destructeur.

### <a name="rc-matched"></a>C.22 : Rendre les opérations par défaut cohérentes

##### Raison

Les opérations par défaut forment conceptuellement un ensemble apparié. Leurs sémantiques sont interdépendantes.
Les utilisateurs seront surpris si la construction par copie/déplacement et l'affectation par copie/déplacement font logiquement des choses différentes. Les utilisateurs seront surpris si les constructeurs et les destructeurs ne fournissent pas une vue cohérente de la gestion des ressources. Les utilisateurs seront surpris si la copie et le déplacement ne reflètent pas le fonctionnement des constructeurs et destructeurs.

##### Exemple, mauvais

    class Silly {   // MAUVAIS : opérations de copie incohérentes
        class Impl {
            // ...
        };
        shared_ptr<Impl> p;
    public:
        Silly(const Silly& a) : p(make_shared<Impl>()) { *p = *a.p; }   // copie profonde
        Silly& operator=(const Silly& a) { p = a.p; return *this; }   // copie superficielle
        // ...
    };

Ces opérations sont en désaccord sur les sémantiques de copie. Cela conduira à des confusions et des bogues.

##### Application

* (Complexe) Un constructeur de copie/déplacement et l'opérateur d'affectation de copie/déplacement correspondant devraient écrire dans les mêmes membres de données au même niveau de déréférencement.
* (Complexe) Tout membre de données écrit dans un constructeur de copie/déplacement devrait aussi être initialisé par tous les autres constructeurs.
* (Complexe) Si un constructeur de copie/déplacement effectue une copie profonde d'un membre de données, alors le destructeur devrait modifier ce membre de données.
* (Complexe) Si un destructeur modifie un membre de données, ce membre de données devrait être écrit dans tous les constructeurs ou opérateurs d'affectation de copie/déplacement.

## <a name="ss-dtor"></a>C.dtor : Destructeurs

« Cette classe a-t-elle besoin d'un destructeur ? » est une question de conception étonnamment révélatrice.
Pour la plupart des classes, la réponse est « non », soit parce que la classe ne détient pas de ressources, soit parce que la destruction est gérée par [la règle de zéro](007-class.md#rc-zero) ;
c'est-à-dire que ses membres peuvent s'en occuper en ce qui concerne la destruction.
Si la réponse est « oui », une grande partie de la conception de la classe en découle (voir [la règle de cinq](007-class.md#rc-five)).

### <a name="rc-dtor"></a>C.30 : Définir un destructeur si une classe a besoin d'une action explicite à la destruction de l'objet

##### Raison

Un destructeur est implicitement appelé à la fin de la durée de vie d'un objet.
Si le destructeur par défaut suffit, utilisez-le.
Ne définissez un destructeur non par défaut que si une classe a besoin d'exécuter du code qui n'est pas déjà fait partie des destructeurs de ses membres.

##### Exemple

    template<typename A>
    struct final_action {   // légèrement simplifié
        A act;
        final_action(A a) : act{a} {}
        ~final_action() { act(); }
    };

    template<typename A>
    final_action<A> finally(A act)   // déduire le type de l'action
    {
        return final_action<A>{act};
    }

    void test()
    {
        auto act = finally([] { cout << "Exit test\n"; });  // établir l'action de sortie
        // ...
        if (something) return;   // act est fait ici
        // ...
    } // act est fait ici

Le but entier de `final_action` est de faire exécuter un morceau de code (généralement une lambda) lors de la destruction.

##### Remarque

Il y a deux catégories générales de classes qui ont besoin d'un destructeur défini par l'utilisateur :

* Une classe avec une ressource qui n'est pas déjà représentée comme une classe avec un destructeur, par exemple un `vector` ou une classe de transaction.
* Une classe qui existe principalement pour exécuter une action lors de la destruction, comme un traceur ou `final_action`.

##### Exemple, mauvais

    class Foo {   // mauvais ; utiliser le destructeur par défaut
    public:
        // ...
        ~Foo() { s = ""; i = 0; vi.clear(); }  // nettoyer
    private:
        string s;
        int i;
        vector<int> vi;
    };

Le destructeur par défaut le fait mieux, plus efficacement, et ne peut pas se tromper.

##### Application

Chercher des « ressources implicites » probables, comme les pointeurs et les références. Chercher des classes avec des destructeurs alors que tous leurs membres de données ont des destructeurs.

### <a name="rc-dtor-release"></a>C.31 : Toutes les ressources acquises par une classe doivent être libérées par le destructeur de la classe

##### Raison

Prévention des fuites de ressources, en particulier dans les cas d'erreur.

##### Remarque

Pour les ressources représentées comme des classes avec un ensemble complet d'opérations par défaut, cela se fait automatiquement.

##### Exemple

    class X {
        ifstream f;   // pourrait posséder un fichier
        // ... pas d'opérations par défaut définies ou supprimées ...
    };

Le `ifstream` de `X` ferme implicitement tout fichier qu'il pourrait avoir ouvert lors de la destruction de son `X`.

##### Exemple, mauvais

    class X2 {     // mauvais
        FILE* f;   // pourrait posséder un fichier
        // ... pas d'opérations par défaut définies ou supprimées ...
    };

`X2` pourrait fuir un descripteur de fichier.

##### Remarque

Qu'en est-il d'un socket qui ne se ferme pas ? Un destructeur, une fermeture ou une opération de nettoyage [ne devrait jamais échouer](007-class.md#rc-dtor-fail).
Si cela arrive néanmoins, nous avons un problème qui n'a pas vraiment de bonne solution.
Pour commencer, l'auteur d'un destructeur ne sait pas pourquoi le destructeur est appelé et ne peut pas « refuser d'agir » en levant une exception.
Voir [discussion](028-discussion.md#sd-never-fail).
Pour aggraver les choses, de nombreuses opérations de « fermeture/libération » ne sont pas réessayables.
Beaucoup ont essayé de résoudre ce problème, mais aucune solution générale n'est connue.
Dans la mesure du possible, considérer l'échec de fermeture/nettoyage comme une erreur fondamentale de conception et terminer le programme.

##### Remarque

Une classe peut détenir des pointeurs et des références vers des objets qu'elle ne possède pas.
Évidemment, de tels objets ne doivent pas être `delete`d par le destructeur de la classe.
Par exemple :

    Preprocessor pp { /* ... */ };
    Parser p { pp, /* ... */ };
    Type_checker tc { p, /* ... */ };

Ici `p` fait référence à `pp` mais ne le possède pas.

##### Application

* (Simple) Si une classe a des membres pointeurs ou références qui sont propriétaires
  (par exemple, jugés propriétaires en utilisant `gsl::owner`), alors ils devraient être référencés dans son destructeur.
* (Difficile) Déterminer si des membres pointeurs ou références sont propriétaires lorsqu'il n'y a pas de déclaration explicite de propriété
  (par exemple, regarder dans les constructeurs).

### <a name="rc-dtor-ptr"></a>C.32 : Si une classe a un pointeur brut (`T*`) ou une référence (`T&`), considérer si elle pourrait être propriétaire

##### Raison

Il y a beaucoup de code qui n'est pas spécifique quant à la propriété.

##### Exemple

    class legacy_class
    {
        foo* m_owning;   // Mauvais : changer en unique_ptr<T> ou owner<T*>
        bar* m_observer; // OK : garder
    }

La seule façon de déterminer la propriété peut être l'analyse du code.

##### Remarque

La propriété devrait être claire dans le nouveau code (et le code legacy refactorisé) conformément à [R.20](009-resource.md#rr-owner) pour les
pointeurs propriétaires et [R.3](009-resource.md#rr-ptr) pour les pointeurs non propriétaires.  Les références ne devraient jamais être propriétaires [R.4](009-resource.md#rr-ref).

##### Application

Regarder l'initialisation des membres pointeurs bruts et des membres références et voir si une allocation est utilisée.

### <a name="rc-dtor-ptr2"></a>C.33 : Si une classe a un membre pointeur propriétaire, définir un destructeur

##### Raison

Un objet possédé doit être `delete`d lors de la destruction de l'objet qui le possède.

##### Exemple

Un membre pointeur pourrait représenter une ressource.
[Un `T*` ne devrait pas le faire](009-resource.md#rr-ptr), mais dans du code plus ancien, c'est courant.
Considérer un `T*` comme propriétaire possible et donc suspect.

    template<typename T>
    class Smart_ptr {
        T* p;   // MAUVAIS : vague quant à la propriété de *p
        // ...
    public:
        // ... pas d'opérations par défaut définies par l'utilisateur ...
    };

    void use(Smart_ptr<int> p1)
    {
        // erreur : p2.p est fuit (si pas nullptr et pas possédé par un autre code)
        auto p2 = p1;
    }

Notez que si vous définissez un destructeur, vous devez définir ou supprimer [toutes les opérations par défaut](007-class.md#rc-five) :

    template<typename T>
    class Smart_ptr2 {
        T* p;   // MAUVAIS : vague quant à la propriété de *p
        // ...
    public:
        // ... pas d'opérations de copie définies par l'utilisateur ...
        ~Smart_ptr2() { delete p; }  // p est propriétaire !
    };

    void use(Smart_ptr2<int> p1)
    {
        auto p2 = p1;   // erreur : double libération
    }

L'opération de copie par défaut copiera simplement `p1.p` dans `p2.p` menant à une double destruction de `p1.p`. Soyez explicite quant à la propriété :

    template<typename T>
    class Smart_ptr3 {
        owner<T*> p;   // OK : explicite quant à la propriété de *p
        // ...
    public:
        // ...
        // ... opérations de copie et de déplacement ...
        ~Smart_ptr3() { delete p; }
    };

    void use(Smart_ptr3<int> p1)
    {
        auto p2 = p1;   // OK : pas de double libération
    }

##### Remarque

Souvent, la façon la plus simple d'obtenir un destructeur est de remplacer le pointeur par un pointeur intelligent (par exemple `std::unique_ptr`) et de laisser le compilateur organiser la destruction appropriée implicitement.

##### Remarque

Pourquoi ne pas simplement exiger que tous les pointeurs propriétaires soient des « pointeurs intelligents » ?
Cela nécessiterait parfois des modifications de code non triviales et pourrait affecter les ABI.

##### Application

* Une classe avec un membre de données pointeur est suspecte.
* Une classe avec un `owner<T>` devrait définir ses opérations par défaut.


### <a name="rc-dtor-virtual"></a>C.35 : Le destructeur d'une classe de base doit être soit public et virtuel, soit protégé et non virtuel

##### Raison

Pour prévenir les comportements indéfinis.
Si le destructeur est public, alors le code appelant peut tenter de détruire un objet de classe dérivée à travers un pointeur de classe de base, et le résultat est indéfini si le destructeur de la classe de base est non virtuel.
Si le destructeur est protégé, alors le code appelant ne peut pas détruire à travers un pointeur de classe de base et le destructeur n'a pas besoin d'être virtuel ; il a besoin d'être protégé, et non privé, pour que les destructeurs dérivés puissent l'appeler.
En général, l'auteur d'une classe de base ne connaît pas l'action appropriée à effectuer lors de la destruction.

##### Discussion

Voir [cela dans la section Discussion](028-discussion.md#sd-dtor).

##### Exemple, mauvais

    struct Base {  // MAUVAIS : a implicitement un destructeur public non virtuel
        virtual void f();
    };

    struct D : Base {
        string s {"a resource needing cleanup"};
        ~D() { /* ... faire quelque nettoyage ... */ }
        // ...
    };

    void use()
    {
        unique_ptr<Base> p = make_unique<D>();
        // ...
    } // la destruction de p appelle ~Base(), pas ~D(), ce qui fuit D::s et peut-être plus

##### Remarque

Une fonction virtuelle définit une interface vers les classes dérivées qui peut être utilisée sans regarder les classes dérivées.
Si l'interface permet la destruction, cela devrait être sûr de le faire.

##### Remarque

Un destructeur doit être non privé sinon il empêchera l'utilisation du type :

    class X {
        ~X();   // destructeur privé
        // ...
    };

    void use()
    {
        X a;                        // erreur : ne peut pas détruire
        auto p = make_unique<X>();  // erreur : ne peut pas détruire
    }

##### Exception

Nous pouvons imaginer un cas où vous pourriez vouloir un destructeur virtuel protégé : quand un objet d'un type dérivé (et uniquement de tel type) devrait être autorisé à détruire *un autre* objet (pas lui-même) à travers un pointeur vers la base. Nous n'avons pas vu tel cas en pratique, cependant.


##### Application

* Une classe avec des fonctions virtuelles devrait avoir un destructeur qui soit soit public et virtuel, soit protégé et non virtuel.
* Si une classe hérite publiquement d'une classe de base, la classe de base devrait avoir un destructeur qui soit soit public et virtuel, soit protégé et non virtuel.

### <a name="rc-dtor-fail"></a>C.36 : Un destructeur ne doit pas échouer

##### Raison

En général, nous ne savons pas comment écrire du code sans erreur si un destructeur doit échouer.
La bibliothèque standard exige que toutes les classes avec lesquelles elle travaille aient des destructeurs qui ne sortent pas par exception.

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

##### Remarque

Beaucoup ont essayé de concevoir un système infaillible pour gérer l'échec dans les destructeurs.
Aucun n'a réussi à trouver un schéma général.
Cela peut être un vrai problème pratique : par exemple, qu'en est-il d'un socket qui ne se ferme pas ?
L'auteur d'un destructeur ne sait pas pourquoi le destructeur est appelé et ne peut pas « refuser d'agir » en levant une exception.
Voir [discussion](028-discussion.md#sd-never-fail).
Pour aggraver les choses, de nombreuses opérations de « fermeture/libération » ne sont pas réessayables.
Dans la mesure du possible, considérer l'échec de fermeture/nettoyage comme une erreur fondamentale de conception et terminer le programme.

##### Remarque

Déclarer un destructeur `noexcept`. Cela garantira qu'il soit soit terminé normalement, soit le programme se termine.

##### Remarque

Si une ressource ne peut pas être libérée et que le programme ne doit pas échouer, essayez de signaler l'échec au reste du système d'une manière ou d'une autre
(peut-être même en modifiant certains états globaux et en espérant que quelque chose le remarquera et pourra prendre soin du problème).
Soyez pleinement conscient que cette technique est à usage spécifique et source d'erreurs.
Considérez l'exemple « ma connexion ne se ferme pas ».
Probablement il y a un problème à l'autre bout de la connexion et seul un morceau de code responsable des deux bouts de la connexion peut correctement gérer le problème.
Le destructeur pourrait envoyer un message (d'une manière ou d'une autre) à la partie responsable du système, considérer que la connexion est fermée, et retourner normalement.

##### Remarque

Si un destructeur utilise des opérations qui peuvent échouer, il peut capturer les exceptions et dans certains cas toujours se terminer avec succès
(par exemple en utilisant un mécanisme de nettoyage différent de celui qui a levé l'exception).

##### Application

(Simple) Un destructeur devrait être déclaré `noexcept` s'il pourrait lever une exception.

### <a name="rc-dtor-noexcept"></a>C.37 : Rendre les destructeurs `noexcept`

##### Raison

 [Un destructeur ne doit pas échouer](007-class.md#rc-dtor-fail). Si un destructeur tente de sortir avec une exception, c'est une mauvaise erreur de conception et le programme ferait mieux de se terminer.

##### Remarque

Un destructeur (que ce soit défini par l'utilisateur ou généré par le compilateur) est implicitement déclaré `noexcept` (indépendamment du code dans son corps) si tous les membres de sa classe ont des destructeurs `noexcept`. En marquant explicitement les destructeurs `noexcept`, un auteur se protège contre le destructeur devenant implicitement `noexcept(false)` par l'ajout ou la modification d'un membre de classe.

##### Exemple

Tous les destructeurs ne sont pas noexcept par défaut ; un membre qui lève une exception contamine toute la hiérarchie de classes

    struct X {
        Details x;  // a un destructeur qui lève une exception
        // ...
        ~X() { }    // implicitement noexcept(false) ; autrement dit peut lever
    };

Donc, en cas de doute, déclarer un destructeur noexcept.

##### Remarque

Pourquoi ne pas alors déclarer tous les destructeurs noexcept ?
Parce que cela serait dans de nombreux cas — surtout les cas simples — du bruit distrayant.

##### Application

(Simple) Un destructeur devrait être déclaré `noexcept` s'il pourrait lever une exception.

## <a name="ss-ctor"></a>C.ctor : Constructeurs

Un constructeur définit comment un objet est initialisé (construit).

### <a name="rc-ctor"></a>C.40 : Définir un constructeur si une classe a un invariant

##### Raison

C'est à ça que servent les constructeurs.

##### Exemple

    class Date {  // un Date représente une date valide
                  // dans la plage du 1er janvier 1900 au 31 décembre 2100
        Date(int dd, int mm, int yy)
            :d{dd}, m{mm}, y{yy}
        {
            if (!is_valid(d, m, y)) throw Bad_date{};  // forcer l'invariant
        }
        // ...
    private:
        int d, m, y;
    };

C'est souvent une bonne idée d'exprimer l'invariant comme un `Ensures` sur le constructeur.

##### Remarque

Un constructeur peut être utilisé pour la commodité même si une classe n'a pas d'invariant. Par exemple :

    struct Rec {
        string s;
        int i {0};
        Rec(const string& ss) : s{ss} {}
        Rec(int ii) :i{ii} {}
    };

    Rec r1 {7};
    Rec r2 {"Foo bar"};

##### Remarque

La règle de la liste d'initialisation de C++11 élimine le besoin de nombreux constructeurs. Par exemple :

    struct Rec2{
        string s;
        int i;
        Rec2(const string& ss, int ii = 0) :s{ss}, i{ii} {}   // redondant
    };

    Rec2 r1 {"Foo", 7};
    Rec2 r2 {"Bar"};

Le constructeur de `Rec2` est redondant.
Aussi, la valeur par défaut pour `int` serait mieux faite comme [initialiseur de membre par défaut](007-class.md#rc-in-class-initializer).

**Voir aussi** : [construire un objet valide](007-class.md#rc-complete) et [constructeur qui lève](007-class.md#rc-throw).

##### Application

* Signaler les classes avec des opérations de copie définies par l'utilisateur mais sans constructeur (une opération de copie définie par l'utilisateur est un bon indicateur que la classe a un invariant)

### <a name="rc-complete"></a>C.41 : Un constructeur devrait créer un objet entièrement initialisé

##### Raison

Un constructeur établit l'invariant d'une classe. Un utilisateur d'une classe devrait pouvoir supposer qu'un objet construit est utilisable.

##### Exemple, mauvais

    class X1 {
        FILE* f;   // appeler init() avant toute autre fonction
        // ...
    public:
        X1() {}
        void init();   // initialiser f
        void read();   // lire depuis f
        // ...
    };

    void f()
    {
        X1 file;
        file.read();   // crash ou mauvaise lecture !
        // ...
        file.init();   // trop tard
        // ...
    }

Les compilateurs ne lisent pas les commentaires.

##### Exception

Si un objet valide ne peut pas être construit commodément par un constructeur, [utiliser une fonction fabrique](007-class.md#rc-factory).

##### Application

* (Simple) Chaque constructeur devrait initialiser chaque membre de données (soit explicitement, via un appel de constructeur délégant, soit via la construction par défaut).
* (Inconnu) Si un constructeur a un contrat `Ensures`, essayer de voir si c'est un postcondition.

##### Remarque

Si un constructeur acquiert une ressource (pour créer un objet valide), cette ressource devrait être [libérée par le destructeur](007-class.md#rc-dtor-release).
L'idio