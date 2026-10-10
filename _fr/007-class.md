# <a name="s-class"></a>C : Classes et hiérarchies de classes

Une classe est un type défini par l'utilisateur, pour lequel un programmeur peut définir la représentation, les opérations et les interfaces.  
Les hiérarchies de classes sont utilisées pour organiser des classes liées dans des structures hiérarchiques.

## Récapitulatif des règles de classe :

* [C.1 : Organiser les données liées en structures (`struct` ou `class`)](#rc-org)
* [C.2 : Utiliser `class` si la classe possède une invariant ; utiliser `struct` si les membres de données peuvent varier indépendamment](#rc-struct)
* [C.3 : Représenter la distinction entre une interface et une implémentation à l’aide d’une classe](#rc-interface)
* [C.4 : Faire d’une fonction un membre uniquement si elle nécessite un accès direct à la représentation d’une classe](#rc-member)
* [C.5 : Placer les fonctions d’assistance dans le même espace de noms que la classe qu’elles supportent](#rc-helper)
* [C.7 : Ne pas définir une classe ou une énumération et déclarer une variable de son type dans la même instruction](#rc-standalone)
* [C.8 : Utiliser `class` plutôt que `struct` si un membre est non public](#rc-class)
* [C.9 : Minimiser l’exposition des membres](#rc-private)

### Sous‑sections :

* [C.concrete : Types concrets](#ss-concrete)
* [C.ctor : Constructeurs, affectations et destructeurs](#s-ctor)
* [C.con : Conteneurs et autres gestionnaires de ressources](#ss-containers)
* [C.lambdas : Objets fonction et lambdas](#ss-lambdas)
* [C.hier : Hiérarchies de classes (POO)](#ss-hier)
* [C.over : Surcharge et opérateurs surchargés](#ss-overload)
* [C.union : Unions](#ss-union)

## <a name="rc-org"></a>C.1 : Organiser les données liées en structures (`struct` ou `class`)

### ### Raisonnement

Facilité de compréhension.  
Si les données sont liées (pour des raisons fondamentales), ce fait devrait se refléter dans le code.

### ### Exemple

```
    void draw(int x, int y, int x2, int y2);  // MIEUX : relations implicites inutiles
    void draw(Point from, Point to);          // mieux
```

### ### Remarque

Une classe simple sans fonctions virtuelles ne comporte pas de surcoût de mémoire ou de temps.

### ### Remarque

En termes de langage, `class` et `struct` ne diffèrent que par la visibilité par défaut de leurs membres.

### ### Mise en œuvre

Probablement impossible. Un heuristique visant à détecter les éléments de données utilisés ensemble pourrait toutefois être envisageable.

## <a name="rc-struct"></a>C.2 : Utiliser `class` si la classe possède un invariant ; utiliser `struct` si les membres de données peuvent varier indépendamment

### ### Raisonnement

Lisibilité.  
Facilité de compréhension.  
L’utilisation de `class` alerte le programmeur sur la nécessité d’un invariant.  
C’est une convention utile.

### ### Remarque

Un invariant est une condition logique portant sur les membres d’un objet qu’un constructeur doit établir afin que les fonctions membres publiques passent.  
Après l’invariant est établi (généralement par un constructeur), chaque fonction membre peut être appelée pour l’objet.  
L’invariant peut être énoncé de façon informelle (ex. dans un commentaire) ou plus formellement en utilisant `Expects`.

Si tous les membres de données peuvent varier indépendamment les uns des autres, aucun invariant n’est possible.

### ### Exemple

```
    struct Pair {  // les membres peuvent varier indépendamment
        string name;
        int volume;
    };

    class Date {
    public:
        // valider que {yy, mm, dd} est une date valide et initialiser
        Date(int yy, Month mm, char dd);
    private:
        int y;
        Month m;
        char d;    // jour
    };
```

### ### Remarque

Si une classe possède des données privées, l’utilisateur ne peut pas complètement initialiser un objet sans l’usage d’un constructeur.  
Par conséquent, le créateur de la classe devra fournir un constructeur et préciser sa signification.  
Cela signifie essentiellement que le créateur doit définir un invariant.

**Voir aussi** :

* [définir une classe avec des données privées comme `class`](#rc-class)
* [préférer placer l’interface en premier dans une classe](#rl-order)
* [minimiser l’exposition des membres](#rc-private)
* [éviter les données `protected`](#rh-protected)

### ### Mise en œuvre

Rechercher des `struct` dont tous les données sont privées et des `class` dont les membres publics sont visibles.

## <a name="rc-interface"></a>C.3 : Représenter la distinction entre une interface et une implémentation à l’aide d’une classe

### ### Raisonnement

Une distinction explicite entre l’interface et l’implémentation améliore la lisibilité et simplifie la maintenance.

### ### Exemple

```
    class Date {
    public:
        Date();
        // valider que {yy, mm, dd} est une date valide et initialiser
        Date(int yy, Month mm, char dd);

        int day() const;
        Month month() const;
        // ...
    private:
        // ... représentation ...
    };
```

Par exemple, nous pouvons maintenant changer la représentation d’un `Date` sans affecter ses utilisateurs (recompilation probable, cependant).

### ### Remarque

Utiliser une classe de cette façon pour représenter la distinction entre interface et implémentation n’est bien sûr pas la seule façon.  
Par exemple, on peut utiliser un ensemble de déclarations de fonctions à libération de la fonction dans un espace de noms, une classe de base abstraite ou un modèle fonctionnel avec des concepts pour représenter une interface.  
Le point le plus important est de distinguer explicitement l’interface de ses « détails » d’implémentation.  
Idéalement, l’interface est beaucoup plus stable que ses implémentations.

### ### Mise en œuvre

???

## <a name="rc-member"></a>C.4 : Faire d’une fonction un membre uniquement si elle nécessite un accès direct à la représentation d’une classe

### ### Raisonnement

Moins de couplage qu’avec les fonctions membres, moins de fonctions pouvant créer des problèmes en modifiant l’état d’un objet, réduction du nombre de fonctions à modifier après un changement d’implémentation.

### ### Exemple

```
    class Date {
        // ... interface relativement petite ...
    };

    // fonctions auxiliaires :
    Date next_weekday(Date);
    bool operator==(Date, Date);
```

Les « fonctions auxiliaires » n’ont aucune nécessité d’avoir un accès direct à la représentation d’un `Date`.

### ### Remarque

Cette règle devient encore meilleure si C++ obtient les appels de fonction « uniform» (https://www.open-std.org/jtc1/sc22/wg21/docs/papers/2016/p0251r0.pdf).

### ### Exception

Le langage requiert que les fonctions virtuelles soient des membres, et toutes les fonctions virtuelles ne touchent pas directement aux données.  
En particulier, les membres d’une classe abstraite ne touchent pas toujours les données.

Note [Multi‑méthodes](https://web.archive.org/web/20200605021759/https://parasol.tamu.edu/~yuriys/papers/OMM10.pdf).

### ### Exception

Le langage impose que les opérateurs `=`, `()`, `[]` et `->` soient des membres.

### ### Exception

Un ensemble de surcharge peut contenir des membres qui n’accèdent pas directement aux données `private` :

```
    class Foobar {
    public:
        void foo(long x) { /* manipuler des données privées */ }
        void foo(double x) { foo(std::lround(x)); }
        // ...
    private:
        // ...
    };
```

### ### Exception

De même, un ensemble de fonctions peut être conçu pour être utilisé dans une chaîne :

```
    x.scale(0.5).rotate(45).set_color(Color::red);
```

Typiquement, certaines mais pas toutes de ces fonctions accèdent directement aux données `private`.

### ### Mise en œuvre

* Chercher les fonctions membres non virtuelles qui n’affectent pas directement les membres de données.  
Le problème est que de nombreuses fonctions membres ne touchent pas sans nécessité des membres de données directement.
* Ignorer les fonctions virtuelles.
* Ignorer les fonctions faisant partie d’un ensemble de surcharge dont au moins une fonction accède aux membres privés.
* Ignorer les fonctions renvoyant `this`.

## <a name="rc-helper"></a>C.5 : Placer les fonctions d’assistance dans le même espace de noms que la classe qu’elles soutiennent

### ### Raisonnement

Une fonction d’assistance est une fonction (souvent fournie par l’auteur d’une classe) qui n’a pas besoin d’accéder directement à la représentation d’une classe, mais qui fait partie de son interface utile.  
La placer dans le même espace de noms que la classe rend la relation évidente et permet de la trouver par la recherche basée sur les arguments.

### ### Exemple

```
    namespace Chrono { // ici nous conservons les services liés au temps

        class Time { /* ... */ };
        class Date { /* ... */ };

        // fonctions auxiliaires :
        bool operator==(Date, Date);
        Date next_weekday(Date);
        // ...
    }
```

### ### Remarque

C’est d’autant plus important pour les opérateurs surchargés.

### ### Mise en œuvre

* Marquer les fonctions globales prenant des types d’arguments provenant d’un même espace de noms.

## <a name="rc-standalone"></a>C.7 : Ne pas définir une classe ou une énumération et déclarer une variable de son type dans la même instruction

### ### Raisonnement

Mélanger une définition de type et la définition d’une autre entité dans la même déclaration est source de confusion et inutile.

### ### Exemple, mauvais

```
    struct Data { /*...*/ } data{ /*...*/ };
```

### ### Exemple, bon

```
    struct Data { /*...*/ };
    Data data{ /*...*/ };
```

### ### Mise en œuvre

* Marquer si le `}` d’une définition de classe ou d’énumération n’est pas suivi d’un `;`. Le `;` manque.

## <a name="rc-class"></a>C.8 : Utiliser `class` plutôt que `struct` si un membre est non public

### ### Raisonnement

Lisibilité.  
Faire clairement comprendre que quelque chose est caché/abstrait.  
C’est une convention utile.

### ### Exemple, mauvais

```
    struct Date {
        int d, m;

        Date(int i, Month m);
        // ... beaucoup de fonctions ...
    private:
        int y;  // année
    };
```

Il n’y a rien qui cloue ce code du point de vue des règles du langage C++, mais presque tout est mal du point de vue de conception.  
Les données privées sont cachées loin des données publiques.  
Les données sont réparties en différentes parties de la déclaration de classe.  
Les différentes parties de données ont différents accès.  
Tout cela diminue la lisibilité et rend la maintenance plus difficile.

### ### Remarque

Préférer placer l’interface en premier dans une classe, [voir NL.16](#rl-order).

### ### Mise en œuvre

Marquer les classes déclarées avec `struct` si elles possèdent un membre `private` ou `protected`.

## <a name="rc-private"></a>C.9 : Minimiser l’exposition des membres

### ### Raisonnement

Encapsulation.  
Masquage d’informations.  
Réduire la chance d’accès non intentionnel.  
Cela simplifie la maintenance.

### ### Exemple

```
    template<typename T, typename U>
    struct pair {
        T a;
        U b;
        // ...
    };
```

Quoi que l’on fasse dans la partie `//`, un utilisateur arbitraire d’un `pair` peut arbitrer et indépendamment changer son `a` et son `b`.  
Dans une base de code grande, nous ne pouvons pas facilement trouver quel code fait quoi aux membres de `pair`.  
Cela peut être exactement ce que l’on veut, mais si l’on veut forcer une relation entre les membres, nous devons les rendre `private` et imposer cette relation (invariant) via le constructeur et les fonctions membres. Par exemple :

```
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
        double unit;    // 1 est mètres, 1000 est kilomètres, 0,001 est millimètres, etc.
    };
```

### ### Remarque

Si le jeu d’utilisateurs directs d’un jeu de variables ne peut pas être facilement déterminé, le type ou l’usage de ce jeu ne peut pas être (facilement) changé/amélioré.  
Pour `public` et `protected`, c’est généralement le cas.

### ### Exemple

Une classe peut fournir deux interfaces à ses utilisateurs.  
Une pour les classes dérivées (`protected`) et une pour les utilisateurs généraux (`public`).  
Par exemple, une classe dérivée peut être autorisée à sauter un contrôle d’exécution car elle a déjà garanti la correction :

```
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
            return do_bar(x + y); // OK : la classe dérivée peut contourner le test
        }
    };

    void user(Foo& x)
    {
        int r1 = x.bar(1);      // OK, sera vérifié
        int r2 = x.do_bar(2);   // erreur : contourner le test
        // ...
    }
```

### ### Remarque

[`protected` data is a bad idea](#rh-protected).

### ### Remarque

Préférer l’ordre `public` > `protected` > `private` ; consulter [NL.16](#rl-order).

### ### Mise en œuvre

* [Marquer les données `protected`](#rh-protected).
* Marquer les mélanges de `public` et `private` en données.

---

## <a name="ss-concrete"></a>C.concrete : Types concrets

### Récapitulatif de la règle de type concret :

* [C.10 : Préférer les types concrets aux hiérarchies de classes](#rc-concrete)
* [C.11 : Rendre les types concrets « reguliers »](#rc-regular)
* [C.12 : Ne pas rendre les membres de données `const` ou références dans un type copiable ou déplaçable](#rc-constref)
* [C.13 : Si le membre de données `B` utilise un autre membre de données `A`, déclarer `A` avant `B`](#rc-lifetime)

### <a name="rc-concrete"></a>C.10 : Préférer les types concrets aux hiérarchies de classes

### ### Raisonnement

Un type concret est fondamentalement plus simple qu’un type dans une hiérarchie de classes : plus facile à concevoir, plus facile à implémenter, plus facile à utiliser, plus facile à raisonner, plus petit et plus rapide.  
Vous avez besoin d’une raison (cas d’usage) pour utiliser une hiérarchie.

### ### Exemple

```
    class Point1 {
        int x, y;
        // ... opérations ...
        // ... pas de fonctions virtuelles ...
    };

    class Point2 {
        int x, y;
        // ... opérations, quelques-unes virtuelles ...
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
```

Si une classe fait partie d’une hiérarchie, nous (dans le code réel s’il n’est pas forcément dans de petits exemples) devons manipuler ses objets par des pointeurs ou références.  
Cela implique plus de surcoût mémoire, plus d’allocation et de désallocation, ainsi qu’un surcoût d’exécution à effectuer les indirections résultantes.

### ### Remarque

Les types concrets peuvent être alloués sur la pile et être membres d’autres classes.

### ### Remarque

L’usage de l’indirection est fondamental pour les interfaces polymorphes à l'exécution.  
Le surcoût d'allocation/désallocation n’est pas (c’est juste le cas le plus courant).  
Nous pouvons utiliser une classe de base comme interface d’un objet encapsulé d’une classe dérivée.  
Ceci est fait quand l’allocation dynamique est interdite (e.g. temps réel stricte) et pour fournir une interface stable à certains types de plugins.

### ### Mise en œuvre

???

### <a name="rc-regular"></a>C.11 : Rendre les types concrets « reguliers »

### ### Raisonnement

Les types réguliers sont plus faciles à comprendre que les types qui ne sont pas réguliers (les irrégularités requièrent un effort supplémentaire pour les comprendre et les utiliser).

Les types natifs de C++ l’ont, ainsi que les classes de la bibliothèque standard telles que `string`, `vector`, et `map`.  
Les classes concrètes sans assignation et égalité peuvent être définies, mais elles sont (et devraient être) rares.

### ### Exemple

```
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
```

En particulier, si un type concret est copiable, il vaut mieux aussi fournir un opérateur d’égalité et s’assurer que `a = b` implique `a == b`.

### ### Remarque

Pour les structures destinées à être partagées avec du code C, définir `operator==` peut ne pas être faisable.

### ### Remarque

Des gestionnaires de ressources qui ne peuvent pas être clonés, par ex. un `scoped_lock` sur un `mutex`, sont des types concrets mais généralement non copiables (ils sont mo‑move‑only).

### ### Mise en œuvre

???. 

### <a name="rc-constref"></a>C.12 : Ne pas rendre les membres de données `const` ou références dans un type copiable ou déplaçable

### ### Raisonnement

`const` et `&` sur les membres de données ne servent pas dans un type copiable ou déplaçable, et rendent ces types difficiles à utiliser en les rendant partiellement non copiable/non déplaçable pour des raisons subtiles.

### ### Exemple; mauvais

```
    class bad {
        const int i;    // mauvais
        string& s;      // mauvais
        // ...
    };
```

Les membres `const` et `&` rendent cette classe « seulement partiellement-copiable » — construction par copie mais pas d’affectation par copie.

### ### Remarque

Si vous avez besoin d’un membre qui pointe vers quelque chose, utilisez un pointeur (brut ou intelligent, et `gsl::not_null` si il ne doit pas être nul) à la place d’une référence.

### ### Mise en œuvre

Détecter tout membre `const`, `&` ou `&&` dans un type disposant d’une opération de copie ou de déplacement.

### <a name="rc-lifetime"></a>C.13 : Si le membre de données `B` utilise un autre membre de données `A`, déclarer `A` avant `B`

### ### Raisonnement

Les membres de données sont initialisés dans l’ordre de déclaration, et détruits dans l’ordre inverse.

### ### Discussion

Si le membre de données `B` utilise un autre membre de données `A`, alors `A` doit être déclaré avant `B` afin que `A` survive à `B`, c’est‑à‑dire que la durée de vie de `A` commence avant et se termine après la durée de vie de `B`. Sinon, lors de la construction et de la destruction, `B` tentera d’utiliser `A` hors de sa durée de vie.

### ### Exemple; mauvais

```
    // Mauvais : b utilise a, mais a est déclaré après b.
    //      Ordre de construction est b puis a ; ordre de destruction est a puis b.
    //      Donc b touche a hors de la durée de vie de a.

    class X {
        struct B {
            string* p;
            explicit B(string& a) : p{&a} {}
            ~B() { cout << *p; }                       // utilise a (via p)
        };

        B      b;                                      // construit d’abord
        string a = "some heap allocated string value"; // construit après b ; détruit avant b

    public:
        X() : b{a} {}   // utilise a avant qu'il ne soit construit -> UB use-before-alloc
        ~X() = default; // accède a après sa destruction -> UB use-after-free
    };
```

### ### Exemple; bon

```
    // Corrigé : déclarer a avant b

    class X {
        struct B {
            string* p;
            explicit B(string& a) : p{&a} {}
            ~B() { cout << *p; }                       // utilise a (via p)
        };

        string a = "some heap allocated string value"; // construit avant b ; détruit après b
        B      b;                                      // construit deuxième

    public:
        X() : b{a} {}   // ok
        ~X() = default; // ok
    };
```

### ### Exemple; mauvais

Cet exemple peut également survenir avec la concurrence. Assurez‑vous qu’une opération asynchrone qui accède à une valeur soit jointe avant la valeur qu’elle accède est détruite.

```
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
```

### ### Exemple; bon

```
    // Corrigé : déclarer a avant b

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
```

### ### Mise en œuvre

* Marquer un initialiseur d’instance qui se réfère à un objet avant qu’il ne soit construit.

---

## <a name="s-ctor"></a>C.ctor : Constructeurs, affectations et destructeurs

Ces fonctions contrôlent le cycle de vie des objets : création, copie, déplacement et destruction.  
Définir des constructeurs permet de garantir et de simplifier l’initialisation des classes.

### Fonctionnalités par défaut

* un constructeur par défaut : `X()`
* un constructeur de copie : `X(const X&)`
* une affectation par copie : `operator=(const X&)`
* un constructeur de déplacement : `X(X&&)`
* une affectation de déplacement : `operator=(X&&)`
* un destructeur : `~X()`

Par défaut, le compilateur définit chacune de ces opérations s’il est utilisé, mais le défaut peut être supprimé.

Les opérations par défaut sont un set d’opérations liées qui, ensemble, implémentent la sémantique du cycle de vie d’un objet.  
Par défaut, C++ considère les classes comme des types « valeur », mais pas tous les types le sont.

### Règles du set d’opérations par défaut

* [C.20 : Si vous pouvez éviter de définir des opérations par défaut, faites‑le](#rc-zero)
* [C.21 : Si vous définissez ou `=delete` n’importe quelle fonction de copie, de déplacement ou de destruction, définissez ou `=delete` toutes](#rc-five)
* [C.22 : Rendre les opérations par défaut cohérentes](#rc-matched)

### Règles des destructeurs :

* [C.30 : Définir un destructeur si une classe a besoin d’une action explicite lors de la destruction d’un objet](#rc-dtor)
* [C.31 : Toutes ressources acquises par une classe doivent être libérées par le destructeur d’une classe](#rc-dtor-release)
* [C.32 : Si une classe possède un pointeur brut (`T*`) ou une référence (`T&`), considérer s’il peut être propriétaire](#rc-dtor-ptr)
* [C.33 : Si une classe possède un pointeur propriétaire, définir un destructeur](#rc-dtor-ptr2)
* [C.35 : Un destructeur de classe de base doit être public et virtuel, ou protégé et non virtuel](#rc-dtor-virtual)
* [C.36 : Un destructeur ne doit pas échouer](#rc-dtor-fail)
* [C.37 : Faire des destructeurs `noexcept`](#rc-dtor-noexcept)

### Règles des constructeurs :

* [C.40 : Définir un constructeur si une classe possède un invariant](#rc-ctor)
* [C.41 : Un constructeur doit créer un objet entièrement initialisé](#rc-complete)
* [C.42 : Si un constructeur ne peut pas construire un objet valide, lancer une exception](#rc-throw)
* [C.43 : Assurer qu’une classe copiable possède un constructeur par défaut](#rc-default0)
* [C.44 : Préférer les constructeurs par défaut simples et non lançant](#rc-default00)
* [C.45 : Ne pas définir un constructeur par défaut qui initialise uniquement des membres de données ; utiliser les initialisateurs de membres par défaut](#rc-default)
* [C.46 : Par défaut, déclarer explicitement les constructeurs à un seul argument](#rc-explicit)
* [C.47 : Définir et initialiser les membres de données dans l’ordre de déclaration](#rc-order)
* [C.48 : Préférer les initialisateurs de membres par défaut aux initialisateurs de constructeurs pour les initialisations constantes](#rc-in-class-initializer)
* [C.49 : Préférer l’initialisation à l’affectation dans les constructeurs](#rc-initialize)
* [C.50 : Utiliser une fonction de fabrique si vous avez besoin d’un « comportement virtuel » lors de l’initialisation](#rc-factory)
* [C.51 : Utiliser les constructeurs de délégation pour représenter des actions communes à tous les constructeurs d’une classe](#rc-delegating)
* [C.52 : Utiliser les constructeurs hérités pour importer les constructeurs dans une classe dérivée qui n’a pas besoin d’une explicitité de l’initialisation supplémentaire](#rc-inheriting)

### Règles de copie et de déplacement :

* [C.60 : Faire que l’affectation par copie ne soit pas virtuelle, prendre le paramètre par `const&`, et renvoyer par `non‑const&`](#rc-copy-assignment)
* [C.61 : Une opération de copie doit copier](#rc-copy-semantic)
* [C.62 : Faire de l’affectation par copie sûre pour l’auto‑affectation](#rc-copy-self)
* [C.63 : Faire que l’affectation par déplacement ne soit pas virtuelle, prendre le paramètre par `&&`, et renvoyer par `non‑const&`](#rc-move-assignment)
* [C.64 : Une opération de déplacement doit déplacer et laisser son source dans un état valide](#rc-move-semantic)
* [C.65 : Faire de l’affectation par déplacement sûre pour l’auto‑affectation](#rc-move-self)
* [C.66 : Faire en sorte que les opérations de déplacement soient `noexcept`](#rc-move-noexcept)
* [C.67 : Une classe polymorphe doit supprimer les copies/movements publics](#rc-copy-virtual)

### Autres règles d’opérations par défaut :

* [C.80 : Utiliser `=default` si vous devez expliciter l’usage de la sémantique par défaut](#rc-eqdefault)
* [C.81 : Utiliser `=delete` lorsqu’il faut désactiver le comportement par défaut](#rc-delete)
* [C.82 : Ne pas appeler les fonctions virtuelles dans les constructeurs et destructeurs](#rc-ctor-virtual)
* [C.83 : Pour les types de type valeur, envisager de fournir une fonction `swap` `noexcept`](#rc-swap)
* [C.84 : Un `swap` doit ne pas échouer](#rc-swap-fail)
* [C.85 : Faire `swap` `noexcept`](#rc-swap-noexcept)
* [C.86 : Faire `==` symétrique par rapport aux types d’opérande et `noexcept`](#rc-eq)
* [C.87 : Méfiez‑vous de `==` sur les classes de base](#rc-eq-base)
* [C.89 : Faire un `hash` `noexcept`](#rc-hash)
* [C.90 : Confiance sur les constructeurs et opérateurs d’assignation, pas sur `memset` et `memcpy`](#rc-memset)

### <a name="ss-defop"></a>C.defop : Opérations par défaut

Par défaut, le langage fournit les opérations par défaut avec leurs sémantiques par défaut.  
Cependant, un programmeur peut désactiver ou remplacer ces defaults.

### <a name="rc-zero"></a>C.20 : Si vous pouvez éviter de définir des opérations par défaut, faites‑le

### ### Raisonnement

C’est le plus simple et donne la sémantique la plus propre.

### ### Exemple

```
    struct Named_map {
    public:
        explicit Named_map(const string& n) : name(n) {}
        // pas de constructeurs/copy/move
        // pas d’opérateurs d’affectation
        // pas de destructeur
    private:
        string name;
        map<int, int> rep;
    };

    Named_map nm("map"); // construire
    Named_map nm2 {nm};  // copie
```

Comme `std::map` et `string` ont toutes les fonctions spéciales, plus de travail n’est pas nécessaire.

### ### Remarque

C’est connu comme « la règle du zéro ».

### ### Mise en œuvre

(Not enforceable) While not enforceable, a good static analyzer can detect patterns that indicate a possible improvement to meet this rule. For example, a class with a (pointer, size) pair of members and a destructor that `delete`s the pointer could probably be converted to a `vector`.

---

### <a name="rc-five"></a>C.21 : Si vous définissez ou `=delete` n’importe quelle fonction de copie, de déplacement ou de destruction, définissez ou `=delete` toutes

### ### Raisonnement

Les sémantiques de copie, déplacement et destruction sont étroitement liées, donc si l’une doit être déclarée, les chances sont que les autres doivent également être considérées.

Déclarer n’importe quelle fonction de copie/mouvement/détruction, même comme `=default` ou `=delete`, supprime l’implémentation implicite d’un constructeur de déplacement et d’une affectation de déplacement.  
Déclarer un constructeur de déplacement ou une affectation de déplacement, même comme `=default` ou `=delete`, entraînera la génération implicite d’un constructeur de copie ou d’une affectation de copie qui est définie comme supprimée.  
Donc dès qu’une de ces opérations est déclarée, les autres devraient l’être également pour éviter des effets indésirables comme transformer toutes les possibilités de déplacement en copies plus coûteuses, ou rendre une classe "move‑only".

### ### Exemple, mauvais

```
    struct M2 {   // mauvais : ensemble incomplet d’opérations de copie/mouvement/détruction
    public:
        // ...
        // ... pas d’opérations de copie ou de déplacement ...
        ~M2() { delete[] rep; }
    private:
        pair<int, int>* rep;  // ensemble fini de paires
    };

    void use()
    {
        M2 x;
        M2 y;
        // ...
        x = y;   // affectation par défaut
        // ...
    }
```

Comme la fonction spéciale de destruction est nécessaire, la probabilité que le générateur implicite d’affectation de copie et de déplacement sera correct est faible (ici, nous aurions une double suppression).

### ### Remarque

C’est connue comme « la règle des cinq ».

### ### Remarque

Si vous voulez une implémentation par défaut (tout en définissant une autre), utilisez `=default` pour montrer que vous le faites intentionnellement.  
Si vous ne voulez pas un générateur par défaut, supprimez-le avec `=delete`.

### ### Exemple, bon

Quand un destructeur doit être déclaré simplement pour le rendre `virtual`, il peut être défini comme par défaut.

```
    class AbstractBase {
    public:
        virtual void foo() = 0;  // au moins une méthode abstraite pour rendre la classe abstraite
        virtual ~AbstractBase() = default;
        // ...
    };
```

Pour éviter le tranchage conformément à [C.67](#rc-copy-virtual), faites les opérations de copie/mouvement protégées ou `=delete`, et ajoutez un `clone` :

```
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
```

Définir uniquement les opérations de déplacement ou uniquement les opérations de copie aurait le même effet ici, mais déclarer explicitement l’intention rend plus clair.

### ### Remarque

Les compilateurs appliquent la plupart de cette règle et jurent d’avertir de toute violation.

### ### Remarque

Se fier à une opération de copie implicite dans une classe avec un destructeur est obsolète.

### ### Remarque

Écrire ces fonctions peut être sujet à erreurs.  
Notez leurs types d’arguments :

```
    class X {
    public:
        // ...
        virtual ~X() = default;               // destructeur (virtuel si X est une classe de base)
        X(const X&) = default;                // constructeur de copie
        X& operator=(const X&) = default;     // affectation de copie
        X(X&&) noexcept = default;            // constructeur de déplacement
        X& operator=(X&&) noexcept = default; // affectation de déplacement
    };
```

Une petite faute (comme un faux accent, laisser tomber `const`, utiliser `&` au lieu de `&&`, ou supprimer une fonction spéciale) peut provoquer des erreurs ou des avertissements.  
Pour éviter la corvée et les possibles erreurs, essayez de suivre la [règle du zéro](#rc-zero).

### ### Mise en œuvre

(Simple) Une classe doit déclarer (même une `=delete`) pour toutes les fonctions de copie/mouvement/détruction ou aucune.

### <a name="rc-matched"></a>C.22 : Rendre les opérations par défaut cohérentes

### ### Raisonnement

Les opérations par défaut sont conceptuellement un set apparié.  
Leur sémantique est interconnectée.  
Les utilisateurs seront surpris si la construction et l’assignation par copie/mouvement fait logiquement les choses différentes.  
Ils seront surpris si les constructeurs et destructeurs ne présentent pas une vue cohérente de la gestion des ressources.  
Ils seront surpris si la copie et le déplacement ne reflètent pas la façon dont les constructeurs et destructeurs fonctionnent.

### ### Exemple, mauvais

```
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
```

Ces opérations sont incohérentes sur la sémantique de la copie. Cela conduira à la confusion et aux bugs.

### ### Mise en œuvre

* (Complex) Un constructeur de copie/mouvement et l’opérateur d’affectation correspondant doivent écrire les mêmes membres de données au même niveau de déférencement.
* (Complex) Tout membre de données écrit dans le constructeur de copie/mouvement doit également être initialisé par tous les autres constructeurs.
* (Complex) Si le constructeur de copie/mouvement effectue une copie profonde d’un membre, alors le destructeur doit modifier le membre.
* (Complex) Si le destructeur modifie un membre, ce membre doit être écrit dans les constructeurs/assignations de copie/mouvement.

---

## <a name="ss-dtor"></a>C.dtor : Destructeurs

« Cette classe a-t‑elle besoin d’un destructeur ? » est une question de conception remarquablement perspicace.  
Pour la plupart des classes, la réponse est « non » , soit parce qu’elle ne détient pas de ressources, soit parce que la destruction est gérée par la [règle du zéro]().  
Si la réponse est « oui », bon nombre de la conception du classe suivra.  
Voir [la règle du cinq]()

### <a name="rc-dtor"></a>C.30 : Définir un destructeur si la classe a besoin d’une action explicite lors de la destruction d’un objet

### ### Raisonnement

Un destructeur est invoqué implicitement à la fin de la durée de vie d’un objet.  
Si le destructeur par défaut est suffisant, utilisez‑il.  
N’utilisez un destructeur non‑défaut que si la classe doit exécuter du code qui ne fait pas déjà partie des destructeurs de ses membres.

### ### Exemple

```
    template<typename A>
    struct final_action {   // simplifié
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
        // ...
        if (something) return;   // act est accompli ici
        // ...
    } // act accompli ici
```

Le but de `final_action` est d’obtenir un morceau de code (souvent une lambda) exécuté à la destruction.

### ### Remarque

Il existe deux catégories générales de classes nécessitant un destructeur défini par l’utilisateur :

* une classe avec une ressource qui n’est pas déjà représentée par une classe disposant d’un destructeur ; par ex. `vector` ou une classe transaction
* une classe qui existe principalement pour exécuter une action lors de la destruction, comme un traçeur ou `final_action`

### ### Exemple, mauvais

```
    class Foo {   // mauvais ; utilisez le destructeur par défaut
    public:
        // ...
        ~Foo() { s = ""; i = 0; vi.clear(); }  // nettoyage
    private:
        string s;
        int i;
        vector<int> vi;
    };
```

Le destructeur par défaut effectue mieux, plus efficacement, et ne peut pas se tromper.

### ### Mise en œuvre

Chercher les "ressources implicites", telles que pointeurs et références.  
Chercher les classes ayant des destructeurs alors que tous leurs membres n’ont pas de destructeur.

---

### <a name="rc-dtor-release"></a>C.31 : Toutes ressources acquises par une classe doivent être libérées par le destructeur de la classe

### ### Raisonnement

Prévention des fuites de ressources, surtout dans des cas d’erreur.

### ### Remarque

Les ressources représentées comme des classes disposant d’un set complet d’opérations par défaut sont automatiquement libérées.

### ### Exemple

```
    class X {
        ifstream f;   // pourrait posséder un fichier
        // ... pas d’opérations par défaut définies ou =deleted ...
    };
```

`ifstream` de la classe `X` fermera automatiquement tout fichier ouvert lors de la destruction de `X`.

### ### Exemple, mauvais

```
    class X2 {     // mauvais
        FILE* f;   // pourrait posséder un fichier
        // ... pas d’opérations par défaut définies ou =deleted ...
    };
```

`X2` peut fuir un gestionnaire de fichiers.

### ### Remarque

Que faire d’un socket qui ne se ferme pas ? Un destructeur, close, ou une opération de nettoyage ne doit jamais échouer.  
Si cela échoue, nous ayons un problème qui n’a pas de bonne solution.  
Pour l’arrêt du programme, ce doit être un problème de conception fondamental et vous devriez l'arrêter.

### ### Remarque

Une classe peut contenir des pointeurs et des références à des objets qu’elle ne possède pas.  
Clairement, ces objets ne doivent pas être supprimés dans le destructeur.  
Par ex.

```
    Preprocessor pp { /* ... */ };
    Parser p { pp, /* ... */ };
    Type_checker tc { p, /* ... */ };
```

`p` fait référence à `pp` mais ne le possède pas.

### ### Mise en œuvre

* (Simple) Si une classe possède des pointeurs ou références propriétaires (définis par `gsl::owner`), elles devraient être référencées dans son destructeur.
* (Hard) Déterminer si un pointeur ou une référence est propriétaire lorsqu’il n’existe pas l’énoncé explicite d’ownership.

---

### <a name="rc-dtor-ptr"></a>C.32 : Si une classe possède un pointeur brut (`T*`) ou une référence (`T&`), considérez s’il peut être propriétaire

### ### Raisonnement

Il y a beaucoup de code qui n’est pas spécifique à la propriété.

### ### Exemple

```
    class legacy_class
    {
        foo* m_owning;   // Mauvais : changer en unique_ptr<T> ou owner<T*>
        bar* m_observer; // OK : garder
    }
```

La seule façon de déterminer la propriété peut être l’analyse de code.

### ### Remarque

La propriété doit être claire dans le nouveau code (et le code plus ancien refondu) conformément à [R.20](#rr-owner) pour les pointeurs propriétaires et [R.3](#rr-ptr) pour les pointeurs non propriétaires. Les références ne doivent jamais être propriétaires [R.4](#rr-ref).

### ### Mise en œuvre

Regarder l’initialisation des pointeurs et des références membres et voir si une allocation est utilisée.

---

### <a name="rc-dtor-ptr2"></a>C.33 : Si une classe possède un membre pointeur propriétaire, définir un destructeur

### ### Raisonnement

Un objet propriétaire doit être `delete` dès la destruction de l’objet qui l’own.

### ### Exemple

Un membre pointeur peut représenter une ressource.  
[Un `T*` ne devrait pas en être] (#rr-ptr), mais dans le code plus ancien, c’est fréquent.  
Considérons le pointeur `T*` comme un propriétaire possible et donc suspect.

```
    template<typename T>
    class Smart_ptr {
        T* p;   // BAD : vague sur la propriété de *p
        // ...
    public:
        // ... pas d’opérations par défaut définies par l’utilisateur ...
    };

    void use(Smart_ptr<int> p1)
    {
        // erreur : p2.p est fuité (s’il n’est pas nullptr et n’est pas géré par un autre code)
        auto p2 = p1;
    }
```

Notez que si vous définissez un destructeur, vous devez définir ou supprimer [tous les opérations par défaut](#rc-five).

```
    template<typename T>
    class Smart_ptr2 {
        T* p;   // BAD : vague sur la propriété de *p
        // ...
    public:
        // ... pas d’opérations de copie définies par l’utilisateur ...
        ~Smart_ptr2() { delete p; }  // p est un propriétaire !
    };

    void use(Smart_ptr2<int> p1)
    {
        auto p2 = p1;   // erreur : double suppression
    }
```

L’opération implicite de copie aura simplement copié `p1.p` vers `p2.p` menant à une double destruction de `p1.p`.

```
    template<typename T>
    class Smart_ptr3 {
        owner<T*> p;   // OK : explicite sur la propriété de *p
        // ...
    public:
        // ...
        // ... opérations de copie/mouvement ...
        ~Smart_ptr3() { delete p; }
    };

    void use(Smart_ptr3<int> p1)
    {
        auto p2 = p1;   // OK : pas de double suppression
    }
```

### ### Remarque

Souvent la façon la plus simple d’obtenir un destructeur est de remplacer le pointeur par un pointeur intelligent (par ex. `std::unique_ptr`) et de laisser le compilateur gérer la destruction implicite.

### ### Remarque

Pourquoi ne pas simplement exiger que tous les pointeurs propriétaires soient « pointeurs intelligents » ?  
Cela requiert parfois des changements de code non trivials et peut affecter les ABI.

### ### Mise en œuvre

* Une classe avec un membre pointeur est suspect.
* Une classe avec un `owner<T>` doit définir ses opérations par défaut.

---

### <a name="rc-dtor-virtual"></a>C.35 : Un destructeur de classe de base doit être public et virtuel, ou protégé et non virtuel

### ### Raisonnement

Pour éviter un comportement indéfini.  
Si le destructeur est public, le code appelant peut tenter de détruire un objet dérivé via un pointeur de base, et le résultat est indéfini si le destructeur de la classe de base n’est pas virtuel.  
Si le destructeur est protégé, le code appelant ne peut pas désallouer via un pointeur de base et donc le destructeur n’a pas besoin d’être virtuel ; il doit être protégé pour que les destructeurs dérivés puissent l’invoquer.

### ### Discussion

Voir [ce point de discussion](#sd-dtor).

### ### Exemple, mauvais

```
    struct Base {  // MAUVAIS : a implicitement un destructeur public non virtuel
        virtual void f();
    };

    struct D : Base {
        string s {"une ressource nécessitant un nettoyage"};
        ~D() { /* ... faire un nettoyage ... */ }
        // ...
    };

    void use()
    {
        unique_ptr<Base> p = make_unique<D>();
        // ...
    } // la destruction de p appelle ~Base() et non ~D() → fuite de D::s
```

### ### Remarque

Une fonction virtuelle définit une interface pour les classes dérivées pouvant être utilisée sans regarder les classes dérivées.  
Si l’interface permet la destruction, il doit être sûr de le faire.

### ### Remarque

Un destructeur doit être non privé ou il empêchera l’utilisation du type :

```
    class X {
        ~X();   // destructeur privé
        // ...
    };

    void use()
    {
        X a;                        // erreur : ne peut pas être détruit
        auto p = make_unique<X>();  // erreur : ne peut pas être détruit
    }
```

### ### Exception

On pourrait imaginer un cas où l’on voudrait un destructeur virtuel protégé : lorsqu’un objet d’un type dérivé (et seulement de ce type) doit pouvoir détruire un autre objet (pas lui-même) via un pointeur de base. Nous n’avons pas vu de cas de pratique.

### ### Mise en œuvre

* Un ensemble de classes avec une fonction virtuelle doit avoir un destructeur qui est publique et virtuel ou bien protégé et non virtuel.
* S’il héritée publiquement d’une classe de base, la classe de base doit disposer d'un destructeur qui est public et virtuel ou bien protégé et non virtuel.

---

### <a name="rc-dtor-fail"></a>C.36 : Un destructeur ne doit pas échouer

### ### Raisonnement

En général, il n’est pas connu comment écrire du code exempt d’erreurs si le destructeur devait échouer.  
La bibliothèque standard exige que tous les destructeurs ne quittent pas par exception.

### ### Exemple

```
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
```

### ### Remarque

Beaucoup tentent de créer un schéma infaillible pour gérer les échecs dans les destructeurs.  
Aucun n’est réussi à proposer une solution générale.  
Pour encore le faire, l'échec de contact d’une ressource séparée est un problème de conception fondamental, et le programme doit être arrêté.

### ### Remarque

Déclarez un destructeur `noexcept`. Cela garantit qu’il termine normal ou termine le programme.

### ### Remarque

Si la ressource ne peut pas être libérée et le programme ne doit pas cesser, essayez d’indiquer le échec au reste du système d’une façon ou d’une autre (par ex. en modifiant l’état global et en espérant qu’un observateur le remarquera et prendra soin du problème). Soyez conscient que cette technique est à usage spécialisé et source d’erreurs ; considérer le « h̀euh, ma connexion ne se fermera pas » comme un design fondamental défectueux, l’on dirait généralement finir le programme.

### ### Remarque

Si un destructeur utilise des opérations qui peuvent échouer, il peut attraper une exception et, dans certains cas, finir normalement (par ex. en utilisant un mécanisme de nettoyage différent).

### ### Mise en œuvre

(Simple) Un destructeur devrait être déclaré `noexcept` s’il peut lever une exception.

---

### <a name="rc-dtor-noexcept"></a>C.37 : Faire des destructeurs `noexcept`

### ### Raisonnement

[Un destructeur ne doit pas échouer](#rc-dtor-fail).  
S’il essaie de terminer avec une exception, c’est une faute de conception.

### ### Remarque

Un destructeur (qu’il soit défini par l’utilisateur ou généré par le compilateur) est implicitement `noexcept` (indépendamment du code qui se trouve dans son corps) si tous les membres de la classe ont un destructeur `noexcept`.  
En déclarant explicitement les destructeurs `noexcept`, l’auteur protège le destructeur de devenir implicitement `noexcept(false)` par l’ajout ou la modification d’un membre de classe.

### ### Exemple

Les destructeurs ne sont pas `noexcept` par défaut ; une fonction qui lève une exception tue toute la hiérarchie :

```
    struct X {
        Details x;  // a un destructeur qui lève une exception
        // ...
        ~X() { }    // implicit noexpt(false) ; alias peut lever une exception
    };
```

Donc, si vous avez un doute, déclarez un destructeur `noexcept`.

### ### Remarque

Pourquoi ne pas déclarer tous les destructeurs `noexcept` ?  
Parce que cela irait en distraction dans de nombreuses situations simples et peu importantes.

### ### Mise en œuvre

(Simple) Un destructeur devrait être déclaré `noexcept` s’il peut lever une exception.

---

## <a name="ss-ctor"></a>C.ctor : Constructeurs

Un constructeur définit comment un objet est initialisé (construit).

### <a name="rc-ctor"></a>C.40 : Définir un constructeur si une classe possède un invariant

### ### Raisonnement

C’est le but des constructeurs.

### ### Exemple

```
    class Date {  // un Date représente une date valide
                  // du 1er janvier 1900 au 31 décembre 2100
        Date(int dd, int mm, int yy)
            :d{dd}, m{mm}, y{yy}
        {
            if (!is_valid(d, m, y)) throw Bad_date{};  // imposer l’invariant
        }
        // ...
    private:
        int d, m, y;
    };
```

Il est souvent une bonne idée d’exprimer l’invariant en tant que `Ensures` sur le constructeur.

### ### Remarque

Un constructeur peut être utilisé par commodité même sans invariant. Par ex. :

```
    struct Rec {
        string s;
        int i {0};
        Rec(const string& ss) : s{ss} {}
        Rec(int ii) :i{ii} {}
    };

    Rec r1 {7};
    Rec r2 {"Foo bar"};
```

### ### Remarque

La règle du constructeur C++11 élimine le besoin de nombreux constructeurs. Ex :

```
    struct Rec2{
        string s;
        int i;
        Rec2(const string& ss, int ii = 0) :s{ss}, i{ii} {}   // redondant
    };

    Rec2 r1 {"Foo", 7};
    Rec2 r2 {"Bar"};
```

Le constructeur de `Rec2` est redondant.  
L’option par défaut pour `int` serait mieux faite par un `default member initializer` (#rc-in-class-initializer).

**Voir aussi** : [construire un objet valide] (#rc-complete) et [constructeur qui lève] (#rc-throw).

### ### Mise en œuvre

* Marquer les classes qui ont une opération de copie mais pas de constructeur (une opération de copie est un bon indicateur d’invariant)

---

### <a name="rc-complete"></a>C.41 : Un constructeur doit créer un objet entièrement initialisé

### ### Raisonnement

Un constructeur établir l’invariant pour une classe. Un utilisateur d’une classe doit pouvoir supposer qu’un objet construit est utilisable.

### ### Exemple, mauvais

```
    class X1 {
        FILE* f;   // appeler init() avant toute autre fonction
        // ...
    public:
        X1() {}
        void init();   // initialiser f
        void read();   // lire de f
        // ...
    };
```

```
    void f()
    {
        X1 file;
        file.read();   // plantage ou mauvaise lecture !
        // ...
        file.init();   // trop tard
        // ...
    }
```

Les compilateurs ne lisent pas les commentaires.

### ### Exception

Si un objet valide ne peut pas être facilement construit par un constructeur, [utiliser une fonction de fabrique] (#rc-factory).

### ### Mise en œuvre

* (Simple) Chaque constructeur doit initialiser chaque membre de données (explicitement, via un appel de constructeur déléguée ou via construction par défaut).
* (Inconnu) Si un constructeur a une contract `Ensures`, essayez de voir si elle tient comme post‑condition.

### ### Remarque

Si un constructeur acquiert une ressource pour créer un objet valide, cette ressource devrait être [libérée par le destructeur] (#rc-dtor-release).  
L’idée d’avoir des constructeurs qui acquièrent et des destructeurs qui libèrent est appelée [RAII] (#rr-raii) (« Resource Acquisition Is Initialization »).

---

### <a name="rc-throw"></a>C.42 : Si un constructeur ne peut pas construire un objet valide, lancer une exception

### ### Raisonnement

Laisser derrière un objet invalide est une invitation à l’échec.

### ### Exemple

```
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

        void read();      // lire de f
        // ...
    };
```

```
    void f()
    {
        X2 file {"Zeno"}; // lève une exception si le fichier n’est pas ouvert
        file.read();      // bien
        // ...
    }
```

### ### Exemple, mauvais

```
    class X3 {     // mauvais : le constructeur laisse un objet non valide derrière
        FILE* f;   // établir is_valid() avant toute autre fonction
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
        void read();   // lire de f
        // ...
    };
```

```
    void f()
    {
        X3 file {"Heraclides"};
        file.read();   // plantage ou mauvaise lecture !
        // ...
        if (file.is_valid()) {
            file.read();
            // ...
        }
        else {
            // ... gérer l’erreur ...
        }
        // ...
    }
```

### ### Remarque

Pour une définition de variable (ex. sur la pile ou comme membre d’un autre objet) il n’y a pas de fonction explicite d’où pourrait sortir un code d’erreur.  
Laisser derrière un objet invalide et compter sur les utilisateurs pour vérifier une fonction `is_valid()` avant l’utilisation est fatigant, source d’erreurs, et inefficace.

### ### Exception

Il existe des domaines, tels que certains systèmes temps réel robuste (penser aux contrôles aériens), où (sans support d’outils supplémentaires) la gestion d’exceptions n’est pas suffisamment prévisible du point de vue de l’horloge.  
Dans ces cas, la technique `is_valid()` doit être utilisée. Dans les cas où, vérifiez `is_valid()` systématiquement et immédiatement pour simuler [RAII] (#rr-raii).

### ### Alternative

Si vous avez une envie de pratiquer une initialisation post‑constructeur ou une initialisation à deux stades, essayez de ne pas le faire ; si vous en avez vraiment besoin, regardez les [fonctions de fabrique] (#rc-factory).

### ### Remarque

Une des raisons pour lesquelles la communauté a utilisé les fonctions `init()` plutôt que de réaliser le travail d’initialisation dans un constructeur est d’éviter la duplication de code.  
[Les constructeurs de délégation] (#rc-delegating) et les initialisateurs de membre par défaut le font mieux.  
Une autre raison est de retarder l’initialisation jusqu’à ce qu’un objet soit nécessaire ; la solution est la plus simple souvent [ne pas déclarer une variable tant qu’elle ne peut pas être correctement initialisée] (#res-init).

### ### Mise en œuvre

???

---

### <a name="rc-default0"></a>C.43 : Assurer qu’une classe copiable a un constructeur par défaut

### ### Raisonnement

C’est, assurer qu’une classe concrète copiable comporte une opération par défaut de construction.

### ### Exemple

```
    class Date { // MAUVAIS : aucun constructeur par défaut
    public:
        Date(int dd, int mm, int yyyy);
        // ...
    };

    vector<Date> vd1(1000);   // nécessite un Date par défaut ici
    vector<Date> vd2(1000, Date{7, Month::October, 1885});   // alternative
```

Le constructeur par défaut est uniquement généré s’il n’y a pas de constructeur utilisateur déclaré, il est donc impossible d’initialiser `vd1` dans l’exemple ci‑dessus.  
L’absence d’une valeur par défaut peut surprendre les utilisateurs et compliquer son usage, alors si elle peut être raisonnablement définie, elle doit être.

`Date` est choisi pour pousser la réflexion : il n’y a pas de « Date naturelle » (le big bang est trop loin dans le passé pour être utile à la plupart des gens), donc cet exemple est non trivial.  
`{0, 0, 0}` n’est pas une date valide dans la plupart des systèmes de calendrier, donc choisir cela introduirait une sorte de `NaN` des nombres flottants.  
Cependant, la plupart des classes `Date` réalistes ont un « repère » (ex. 1 Jan 1970) donc rendre cela la valeur par défaut est habituellement trivial.

```
    class Date {
    public:
        Date(int dd, int mm, int yyyy);
        Date() = default; // [voir aussi](#rc-default)
        // ...
    private:
        int dd {1};
        int mm {1};
        int yyyy {1970};
        // ...
    };
```

```
    vector<Date> vd1(1000);
```

### ### Remarque

Une classe avec des membres qui ont tous des constructeurs par défaut obtient un constructeur par défaut automatiquement :

```
    struct X {
        string s;
        vector<int> v;
    };

    X x; // signifie X{ { }, { } }; c’est la chaîne vide et le vecteur vide
```

Faites attention aux types intégrés qui ne sont pas correctement initialisés par défaut :

```
    struct X {
        string s;
        int i;
    };

    void f()
    {
        X x;    // x.s est initialisé à la chaîne vide ; x.i est non initialisé

        cout << x.s << ' ' << x.i << '\n';
        ++x.i;
    }
```

Les objets statiquement alloués de type intégrée sont initialisés à `0` par défaut, mais les variables locales ne le sont pas. Notez que votre compilateur pourrait initialiser par défaut les variables locales intégrées, mais une build optimisée le ne fera pas. Ainsi, le code comme ci‑dessus peut sembler marcher mais dépendent du comportement indéfini.  
Si vous voulez l’initialisation, une initialisation par défaut explicite peut aider :

```
    struct X {
        string s;
        int i {};   // initialiser par défaut (à 0)
    };
```

### ### Notes

Les classes qui n’ont pas une construction raisonnable sont généralement non copiables donc elles ne figurent pas dans ce guide.

Exemple : une classe de base abstraite ne doit probablement pas être copiée et ne nécessite donc pas de constructeur par défaut :

```
    // Shape est une classe de base abstraite, pas un type copiable.
    // Elle peut ou non avoir besoin de constructeur par défaut.
    struct Shape {
        virtual void draw() = 0;
        virtual void rotate(int) = 0;
        // =delete copy/move
        // ...
    };
```

Une classe qui doit acquérir une ressource fournie par le client lors de la construction ne peut généralement pas avoir de constructeur par défaut, mais elle n’appartient pas à ce guide, car souvent elle n’est pas copiée :

```
    lock_guard g {mx};  // protège le mutex mx
    lock_guard g2;      // erreur : protéger rien
```

Une classe avec un « état spécial » qui doit être géré séparément de tout autre état via des méthodes d’utilisation ou par les utilisateurs rend les choses difficiles (et plus probablement des erreurs). Ce type peut naturellement utiliser l’état spécial comme valeur par défaut, que la classe soit copiable ou non :

```
    ofstream out {"Foobar"};
    // ...
    out << log(time, transaction);
```

Les types spéciaux similaires qui sont copiables, comme les pointeurs intelligents copiables qui ont l’état spécial « == nullptr », devraient utiliser l’état spécial comme valeur par défaut.

Toutefois, il est préférable d’avoir un constructeur par défaut donnant une valeur « utile » telle que `""` de `std::string` ou `{}` de `std::vector`.

### ### Mise en œuvre

* Marquer les classes qui sont copiables par `=` sans constructeur par défaut
* Marquer les classes qui sont comparables par `==` mais pas copiables

---

### <a name="rc-default00"></a>C.44 : Préférer un constructeur par défaut simple et non‑lancé

### ### Raisonnement

Pouvoir fixer une valeur à l’« défaut » sans des opérations qui peuvent échouer simplifie la gestion des erreurs et la raison d’être de la cause de déplacement.

### ### Exemple problématique

```
    template<typename T>
    // elem pointe vers un élément "space-elem" alloué à l’aide de new
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
```

C’est bien et général, mais mettre un `Vector0` à vide après une erreur implique une allocation, qui peut échouer.  
De plus, un `Vector0{}` avec `{new T[0], 0, 0}` semble gaspillé.  
Par ex., `Vector0<int> v[100]` coûte 100 allocations.

### ### Exemple

```
    template<typename T>
    // elem est nullptr ou elem pointe vers un élément "space-elem" alloué à l’aide de new
    class Vector1 {
    public:
        // fixer la représentation à {nullptr, nullptr, nullptr}; ne lance rien
        Vector1() noexcept {}
        Vector1(int n) :elem{new T[n]}, space{elem + n}, last{elem} {}
        // ...
    private:
        own<T*> elem {};
        T* space {};
        T* last {};
    };
```

Utiliser `{nullptr, nullptr, nullptr}` rend `Vector1{}` bon marché, mais avec un cas spécial et implique des vérifications d’exécution.  
Définir un `Vector1` à vide après avoir détecté une erreur est trivial.

### ### Mise en œuvre

* Marquer les constructeurs par défaut qui lèvent des exceptions

---

### <a name="rc-default"></a>C.45 : Ne pas définir un constructeur par défaut qui ne fait que initialiser des membres ; utilisez les initialisateurs de membre par défaut à la place

### ### Raisonnement

L’utilisation de initialisateurs de membre par défaut permet au compilateur de générer la fonction pour vous.  
La fonction générée par le compilateur peut être plus efficace.

### ### Exemple, mauvais

```
    class X1 { // MAUVAIS : n’utilise pas les initialisateurs de membre
        string s;
        int i;
    public:
        X1() :s{"default"}, i{1} { }
        // ...
    };
```

### ### Exemple

```
    class X2 {
        string s {"default"};
        int i {1};
    public:
        // employez le constructeur par défaut généré par le compilateur
        // ...
    };
```

### ### Mise en œuvre

*(Simple)* Marquer si un constructeur par défaut a un initialiseur constant, et recommander que le constant soit écrit comme initialiseur de membre à la place.

---

### <a name="rc-explicit"></a>C.46 : Par défaut, déclarer explicitement les constructeurs à un seul argument

### ### Raisonnement

Éviter les conversions implicites.

### ### Exemple, mauvais

```
    class String {
    public:
        String(int);   // MAUVAIS
        // ...
    };

    String s = 10;   // surprise : string de taille 10
```

### ### Exception

Si vous voulez vraiment une conversion implicite du type d’argument du constructeur vers le type de la classe, n’utilisez pas `explicit` :

```
    class Complex {
    public:
        Complex(double d);   // OK : conversion de d vers {d, 0}
        // ...
    };

    Complex z = 10.7;   // conversion non surprenante
```

**Voir aussi** : [discussion sur les conversions implicites] (#ro-conversion).

### ### Remarque

Les constructeurs de copie et de déplacement ne doivent pas être rendus `explicit` car ils ne réalisent pas de conversions.  
Les constructeurs `explicit` de copie/rétransfert rendent le passage et le retour de valeurs par valeur difficile.

### ### Mise en œuvre

*(Simple)* Les constructeurs à un argument qui ne sont pas `explicit`.

---

### <a name="rc-order"></a>C.47 : Définir et initialiser les membres de données dans l’ordre de déclaration

### ### Raisonnement

Réduire les confusions et erreurs.  

C’est l’ordre d’initialisation (indépendamment de l’ordre des initialisateurs).

### ### Exemple, mauvais

```
    class Foo {
        int m1;
        int m2;
    public:
        Foo(int x) :m2{x}, m1{++x} { }   // MAUVAIS : ordre d’initialisation trompeur
        // ...
    };
```

```
    Foo x(1); // surprise : x.m1 == x.m2 == 2
```

### ### Mise en œuvre

*(Simple)* La liste d’initialisateur de membre devrait mentionner les membres dans le même ordre qu’ils sont déclarés.

**Voir aussi** : [discussion](#sd-order).

---

### <a name="rc-in-class-initializer"></a>C.48 : Préférer les initialisateurs de membre par défaut aux initialisateurs de constructeur pour les initialisations constantes

### ### Raisonnement

Il rend explicite que la même valeur est attendue pour tous les constructeurs.  
Évite la répétition.  
Évite les problèmes de maintenance.  
Conduit au code le plus court et le plus efficace.

### ### Exemple, mauvais

```
    class X {   // MAUVAIS
        int i;
        string s;
        int j;
    public:
        X() :i{666}, s{"qqq"} { }   // j n’est pas initialisé
        X(int ii) :i{ii} {}         // s est "" et j n’est pas initialisé
        // ...
    };
```

Comment un mainteneur sait‑il si `j` a été intentionnellement omis (probablement mauvais) ou si c’était volontaire de donner à `s` la valeur par défaut `""` dans un cas et `qqq` dans l’autre ?  
C’est normalement un bug.

### ### Exemple

```
    class X2 {
        int i {666};
        string s {"qqq"};
        int j {numeric_limits<int>::min()};
    public:
        X2() = default;        // tous les membres sont initialisés aux valeurs par défaut
        X2(int ii) :i{ii} {}   // s et j initialisés aux valeurs par défaut
        // ...
    };
```

**Alternative** : Nous pouvons bénéficier à partir des paramètres par défaut de constructeurs, ce qui n’est pas rare dans le code plus ancien.  
Cependant, c’est moins explicite, provoque plus d'arguments à passer et est répétitif lorsqu’il y en a plus d’un constructeur :

```
    class X3 {   // MAUVAIS : inexplicit, passage d’arguments en culot
        int i;
        string s;
        int j;
    public:
        X3(int ii = 666, const string& ss = "qqq", int jj = numeric_limits<int>::min())
            :i{ii}, s{ss}, j{jj} { }   // tous les membres initialisés aux valeurs par défaut
        // ...
    };
```

### ### Mise en œuvre

* *(Simple)* Tout constructeur doit initialiser chaque membre de données (explicitement, via appel de constructeur délègué ou via construction par défaut).
* *(Simple)* Les paramètres par défaut aux constructeurs suggèrent qu’un initialiseur de membre par défaut pourrait être plus approprié.

---

### <a name="rc-initialize"></a>C.49 : Préférer l’initialisation à l’affectation dans les constructeurs

### ### Raisonnement

Une initialisation explicite indique qu’il s’agit d’une initialisation plutôt qu’un simple assignement, peut être plus élégante et plus efficace.  
Prévenir les erreurs du type « utilisation avant l’initialisation ».

### ### Exemple, bon

```
    class A {   // Bon
        string s1;
    public:
        A(czstring p) : s1{p} { }    // BON : construire directement (et la chaîne c‑string est explicitement nommée)
        // ...
    };
```

### ### Exemple, mauvais

```
    class B {   // MAUVAIS
        string s1;
    public:
        B(const char* p) { s1 = p; }   // MAUVAIS : constructeur par défaut suivi d’assignation
        // ...
    };
```

```
    class C {   // UGLI, alias très mauvais
        int* p;
    public:
        C() { cout << *p; p = new int{10}; }   // usage accidentel avant initialisation
        // ...
    };
```

### ### Exemple, meilleur encore

Au lieu de ces `const char*` on peut utiliser C++17 `std::string_view` ou `gsl::span<char>` comme [une façon plus générale de présenter des arguments à une fonction] (#rstr-view):

```
    class D {   // Bon
        string s1;
    public:
        D(string_view v) : s1{v} { }    // BON : construire directement
        // ...
    };
```

---

### <a name="rc-factory"></a>C.50 : Utiliser une fonction de fabrique si vous avez besoin d’un « comportement virtuel » pendant l’initialisation

### ### Raisonnement

Si l’état d’un objet de base dépend de l’état d’une partie dérivée de l’objet, il faut utiliser une fonction virtuelle (ou équivalente) tout en minimisant la période où l’on utilise un objet incomplètement initialisé.

### ### Remarque

Le type de retour de la fabrique devrait normalement être `unique_ptr` par défaut ; si certaines utilisations sont partagées, le client peut `move` le `unique_ptr` dans un `shared_ptr`.  
Cependant, si le auteur de la fabrique sait que toutes les utilisations de l’objet retourné seront partagées, il peut retourner un `shared_ptr` et utiliser `make_shared` dans le corps pour éviter une allocation supplémentaire.

### ### Exemple, mauvais

```
    class B {
    public:
        B()
        {
            /* ... */
            f(); // MAUVAIS : C.82 : Ne pas appeler des fonctions virtuelles dans constructeurs et destructeurs
            /* ... */
        }

        virtual void f() = 0;
    };
```

### ### Exemple

```
    class B {
    protected:
        class Token {};

    public:
        explicit B(Token) { /* ... */ }  // créer un objet imperfectement initialisé
        virtual void f() = 0;

        template<class T>
        static shared_ptr<T> create()    // interface pour créer des objets partagés
        {
            auto p = make_shared<T>(typename T::Token{});
            p->post_initialize();
            return p;
        }

    protected:
        virtual void post_initialize()   // appelée juste après la construction
            { /* ... */ f(); /* ... */ } // BON : le dispatch virtuel est sûr
    };

    class D : public B {                 // un dérivé
    protected:
        class Token {};

    public:
        explicit D(Token) : B{ B::Token{} } {}
        void f() override { /* ...  */ };

    protected:
        template<class T>
        friend shared_ptr<T> B::create();
    };

    shared_ptr<D> p = D::create<D>();  // création d’un objet D
```

`make_shared` nécessite que le constructeur soit public. En exigeant un `Token` protégé, le constructeur ne peut pas être public et on évite qu’un objet incomplet s’échappe dans le monde.  

En fournissant la fonction de fabrique `create()`, vous facilitez la construction (sur le tas) tout en évitant à l’utilisateur de pouvoir accidentellement créer un objet incomplet.

### ### Remarque

Les fabriques conventionnelles allouent sur le tas, au lieu d’être sur la pile ou dans un objet englobant.

**Voir aussi** : [discussion](#sd-factory).

---

### <a name="rc-delegating"></a>C.51 : Utiliser les constructeurs délégants pour représenter des actions communes à tous les constructeurs d’une classe

### ### Raisonnement

Éviter la répétition et les différences involontaires.

### ### Exemple, mauvais

```
    class Date {   // MAUVAIS : répétitif
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
```

L’action commune devient fastidieuse et peut être involontairement différente.

### ### Exemple

```
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
```

**Voir aussi** : si la « action répétée » est une simple initialisation, considérez un initialiseur de membre par défaut (#rc-in-class-initializer).

### ### Mise en œuvre

(Moderate) Rechercher des corps de constructeurs similaires.

---

### <a name="rc-inheriting"></a>C.52 : Utiliser les constructeurs hérités pour importer les constructeurs dans une classe dérivée ne nécessitant pas d’initialisation explicite supplémentaire

### ### Raisonnement

Si vous avez besoin de ces constructeurs, re‑implémenter ces constructeurs est fastidieux et sujet à erreur.

### ### Exemple

`std::vector` a de nombreux constructeurs complexes, donc si je veux mon propre `vector`, je ne veux pas re‑implémenter :

```
    class Rec {
        // ... données et beaucoup de constructeurs utiles ...
    };

    class Oper : public Rec {
        using Rec::Rec;
        // ... pas de membres de données ...
        // ... beaucoup de fonctions utilitaires ...
    };
```

### ### Exemple, mauvais

```
    struct Rec2 : public Rec {
        int x;
        using Rec::Rec;
    };

    Rec2 r {"foo", 7};
    int val = r.x;   // non initialisé
```

### ### Mise en œuvre

S’assurer que chaque membre de la classe dérivée est initialisé.

---

## <a name="ss-copy"></a>C.copy : Copie et déplacement

Les types concrets sont généralement copiables; les interfaces dans une hiérarchie de classes ne le sont pas.  
Les gestionnaires de ressources peuvent ou non être copiables.  
Les types peuvent être conçus pour être déplacés pour des raisons logiques ou de performance.

---

### <a name="rc-copy-assignment"></a>C.60 : Faire l’affectation par copie non virtuelle, prendre le paramètre par `const&`, et le renvoyer par `non‑const&`

### ### Raisonnement

C’est simple et efficace.  
S’il vaut la peine d’optimiser pour les rvalues, fournissez une surcharge qui prend un `&&` (voir [F.18](#rf-consume)).

### ### Exemple

```
    class Foo {
    public:
        Foo& operator=(const Foo& x)
        {
            // BON : pas besoin de vérifier l’auto‑affectation (sauf performance)
            auto tmp = x;
            swap(tmp); // voir C.83
            return *this;
        }
        // ...
    };
```

```
    Foo a;
    Foo b;
    Foo f();

    a = b;    // affecter par valeur : copie
    a = f();  // affecter par valeur : potentiellement déplacer
```

### ### Remarque

La technique d’implémentation `swap` fournit la garantie forte (#Abrahams01).

### ### Exemple

Mais qu’accompagnez‑vous une performance significativement meilleure sans faire une copie temporaire ?  
Par exemple une simple `Vector` destinée à un domaine où l’affectation de grands `Vector` de même taille est fréquente.  

```
    template<typename T>
    class Vector {
    public:
        Vector& operator=(const Vector&);
        // ...
    private:
        T* elem;
        int sz;
    };
```

```
    Vector& Vector::operator=(const Vector& a)
    {
        if (a.sz > sz) {
            // ... on peut utiliser la technique `swap`, on ne peut pas être meilleur ...
            return *this;
        }
        // ... copier sz éléments de *a.elem à elem ...
        if (a.sz < sz) {
            // ... détruire les éléments supplémentaires et ajuster la taille ...
        }
        return *this;
    }
```

En écrivant directement sur les éléments cibles, nous n’obtiendrons qu’une garantie de base (#Abrahams01) plutôt que la garantie forte de `swap`.  
Faites attention à l’auto‑affectation (#rc-copy-self).

**Alternatives** : Si vous pensez qu’une fonction virtuelle d’affectation est nécessaire et que vous comprenez pourquoi les choses profondes, ne l’appellez pas `operator=`.  
Faites un nom de fonction nommé telle que `virtual void assign(const Foo&)`.  
Voir [constructeur vs. `clone()`] (#rc-copy-virtual).

### ### Mise en œuvre

* (Simple) Un opérateur de copie ne doit pas être virtuel.  
* (Simple) Un opérateur de copie doit renvoyer `T&` pour permettre la chaîne, pas `const T&` qui perturbent la composabilité et le placement dans les conteneurs.  
* (Moyen) Un opérateur de copie doit (implicitement ou explicitement) invoquer toutes les affectations de cop
ie de base et de membre.

---

### <a name="rc-copy-semantic"></a>C.61 : Une opération de copie doit copier

### ### Raisonnement

C’est la sémantique habituellement supposée.  
Après `x = y`, nous devrions avoir `x == y`.  
Après une copie, `x` et `y` peuvent être des objets indépendants (nom de la valeur) ou faire référence à la même pièce d’objet (nom de pointeur).

### ### Exemple

```
    class X {   // OK : valeur
    public:
        X();
        X(const X&);     // copier X
        void modify();   // changer la valeur de X
        // ...
        ~X() { delete[] p; }
    private:
        T* p;
        int sz;
    };
```

```
    bool operator==(const X& a, const X& b)
    {
        return a.sz == b.sz && equal(a.p, a.p + a.sz, b.p, b.p + b.sz);
    }
```

```
    X::X(const X& a)
        :p{new T[a.sz]}, sz{a.sz}
    {
        copy(a.p, a.p + sz, p);
    }
```

```
    X x;
    X y = x;
    if (x != y) throw Bad{};
    x.modify();
    if (x == y) throw Bad{};   // suppose une valeur
```

### ### Exemple

```
    class X2 {  // OK : pointer
    public:
        X2();
        X2(const X2&) = default; // copie superficielle
        ~X2() = default;
        void modify();          // changer la valeur pointée
        // ...
    private:
        T* p;
        int sz;
    };
```

```
    bool operator==(const X2& a, const X2& b)
    {
        return a.sz == b.sz && a.p == b.p;
    }
```

```
    X2 x;
    X2 y = x;
    if (x != y) throw Bad{};
    x.modify();
    if (x != y) throw Bad{};  // supposé pointer
```

### ### Remarque

Préférence pour les valeurs à moins que vous ne construisiez un « smart pointer ».  
Les valeurs sont plus simples à raisonner et ce que les facilities de la bibliothèque standard attendent.

### ### Mise en œuvre

(Not enforceable)

---

### <a name="rc-copy-self"></a>C.62 : Faire l’affectation par copie sûre pour l’auto‑affectation

### ### Raisonnement

Si `x = x` modifie la valeur de `x`, les gens seront surpris et des erreurs graves se produiront ; souvent il faut éviter le double appel.

### ### Exemple

Les conteneurs standards gèrent parfaitement l’auto‑affectation.

```
    std::vector<int> v = {3, 1, 4, 1, 5, 9};
    v = v;
    // la valeur de v est toujours {3, 1, 4, 1, 5, 9}
```

### ### Remarque

Les affectations par défaut générées à partir des membres qui traitent correctement l’auto‑affectation le font.

```
    struct Bar {
        vector<pair<int, int>> v;
        map<string, int> m;
        string s;
    };
```

```
    Bar b;
    // ...
    b = b;   // correct et efficace
```

### ### Remarque

Vous pouvez gérer l’auto‑affectation en testant explicitement l’auto‑affectation, mais souvent il est plus rapide et plus élégant d’éviter le test (e.g. via `swap`).

```
    class Foo {
        string s;
        int i;
    public:
        Foo& operator=(const Foo& a);
        // ...
    };
```

```
    Foo& Foo::operator=(const Foo& a)   // OK, mais avec un coût
    {
        if (this == &a) return *this;
        s = a.s;
        i = a.i;
        return *this;
    }
```

Cela est évidemment sûr et apparemment efficace.  
Mais que faire si on fait un auto‑affectation par million d’affectations ?  
Il y a donc environ un million de tests redondants (mais généralement, le prédicteur de branche devine correctement).  
Examinons :

```
    Foo& Foo::operator=(const Foo& a)   // simple, et probablement bien mieux
    {
        s = a.s;
        i = a.i;
        return *this;
    }
```

`std::string` est sûr pour l’auto‑affectation et `int` aussi.  
Tout le coût est porté par le cas rare d’auto‑affectation.

### ### Mise en œuvre

*(Simple)* L’opérateur de copie ne doit pas contenir le modèle `if (this == &a) return *this;` ?

---

### <a name="rc-move-assignment"></a>C.63 : Faire l’affectation par déplacement non virtuelle, prendre le paramètre par `&&`, et le renvoyer par `non‑const&`

### ### Raisonnement

C’est simple et efficace.

**Voir** : [la règle d’affectation par copie] (#rc-copy-assignment).

### ### Mise en œuvre

Équivalente à celle pour [l’affectation par copie] (#rc-copy-assignment).

* (Simple) L’affectation ne doit pas être virtuelle.  
* (Simple) L’affectation doit renvoyer `T&`.  
* (Moyen) L’opérateur doit invoquer tous les opérateurs d’affectation/ de déplacement des membres et bases.

---

### <a name="rc-move-semantic"></a>C.64 : Une opération de déplacement doit déplacer et laisser son source dans un état valide

### ### Raisonnement

C’est la sémantique généralement supposée.  
Après `y = std::move(x)`, la valeur de `y` doit être la valeur que `x` avait, et `x` doit être dans un état valide.

### ### Exemple

```
    class X {
    public:
        X();
        X(X&& a) noexcept;  // déplacer X
        X& operator=(X&& a) noexcept; // déplacement
        void modify();     // changer la valeur de X
        // ...
        ~X() { delete[] p; }
    private:
        T* p;
        int sz;
    };
```

```
    X::X(X&& a) noexcept
        :p{a.p}, sz{a.sz}  // voler la représentation
    {
        a.p = nullptr;     // mettre à "vide"
        a.sz = 0;
    }
```

```
    void use()
    {
        X x{};
        // ...
        X y = std::move(x);
        x = X{};   // ok
    } // ok, x peut être détruit
```

### ### Remarque

Idéalement, ce 'moved‑from' est la valeur par défaut de

ltype.  
Il faut que, sauf s’il y a une bonne raison d’être différent, l’état passé après déplacement soit l’état par défaut.  
Cependant, tous les types n’ont pas une valeur par défaut, et pour certains types, établir la valeur par défaut peut être cher.  
Le C++ exige uniquement que l’objet déplacé puisse être détruit.  
Souvent, on peut facilement et à moindre coût faire mieux : l’opérateur `move` peut laisser l’objet s

erve dans un état (qui est forcément spécifié) mais valide.

### ### Remarque

Sauf s’il y a une raison fortée, faites `x = std::move(y); y = z;` fonctionner avec la sémantique conventionnelle.

### ### Mise en œuvre

(Not enforceable)

---

### <a name="rc-move-self"></a>C.65 : Faire l’affectation par déplacement sûre pour l’auto‑affectation

### ### Raisonnement

Si `x = x` modifie la valeur de `x`, les gens seront surpris et de gros bugs peuvent survenir.  
Les gens ne sont pas toujours directement `move` un objet, mais cela peut arriver.

### ### Exemple

```
    class Foo {
        string s;
        int i;
    public:
        Foo& operator=(Foo&& a) noexcept;
        // ...
    };
```

```
    Foo& Foo::operator=(Foo&& a) noexcept  // OK, mais avec un coût
    {
        if (this == &a) return *this;  // cette ligne est redondante
        s = std::move(a.s);
        i = a.i;
        return *this;
    }
```

L’argument `if (this == &a) return *this;` est débattu dans <…>.

### ### Remarque

Il n’y a pas de façon valable (generale) d’éviter le test et de rester correct.

### ### Remarque

La norme ISO ne garantit qu’un état “valide mais non précisé” pour les conteneurs standards.  
Cela n’a pas posé de problème en pratiquement 10 ans d’utilisation.

### ### Exemple

Voici un moyen de déplacer un pointeur sans test (imaginez‑le comme le code d’une affectation de déplacement) :

```
    // déplacer from other.ptr to this->ptr
    T* temp = other.ptr;
    other.ptr = nullptr;
    delete ptr; // dans un self‑move, this->ptr est aussi null; delete est un no‑op
    ptr = temp; // dans un self‑move, l’ancien ptr est restauré
```

### ### Mise en œuvre

* (Moderate) Dans le cas d’auto‑affectation, un opérateur de déplacement ne doit pas laisser l’objet posséder un pointeur qui a été supprimé ou mis à `nullptr`.  
* (Not enforceable) Examiner l’usage de conteneurs standard (incluant `string`) et considérer qu’ils sont sûrs pour les usages ordinaires.

---

### <a name="rc-move-noexcept"></a>C.66 : Faire des opérations de déplacement `noexcept`

### ### Raisonnement

Un déplacement qui lève une exception enfreint la plupart des attentes rationnelles.  
Un déplacement non‑lancé sera plus efficacement utilisé par les facilities de la langue et du standard.

### ### Exemple

```
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
```

Ces opérations ne lèvent pas d’exception.

### ### Exemple, mauvais

```
    template<typename T>
    class Vector2 {
    public:
        Vector2(Vector2&& a) noexcept { *this = a; }             // juste utiliser la copie
        Vector2& operator=(Vector2&& a) noexcept { *this = a; }  // juste utiliser la copie
        // ...
    private:
        T* elem;
        int sz;
    };
```

Cette classe `Vector2` n’est pas seulement inefficiente, elle peut aussi lancer des exceptions lors de la copie en allocation.

### ### Mise en œuvre

*(Simple)* Une opération de déplacement doit être marquée `noexcept`.

---

### <a name="rc-copy-virtual"></a>C.67 : Une classe polymorphe doit supprimer les copies/mouvements publics

### ### Raisonnement

Une *classe polymorphe* est une classe qui définit ou hérite au moins une fonction virtuelle.  
Il est probable qu’elle soit utilisée comme base pour d’autres classes dérivées.  
Si on la passe par valeur accidentellement, on risque le tranchage : seul le segment de base d’un objet dérivé sera copié, et le comportement polymorphe sera corrompu.

Si la classe n’ait pas de données, `=delete` les fonctions de copie/ déplacement.  
Sinon, faites-les protégées.

### ### Exemple, mauvais

```
    class B { // MAUVAIS : classe de base polymorphe ne supprime pas le copier
    public:
        virtual char m() { return 'B'; }
        // ...
    };

    class D : public B {
    public:
        char m() override { return 'D'; }
        // ...
    };
```

```
    void f(B& b)
    {
        auto b2 = b; // oops, tranchage de l’objet ; b2.m() renvoie 'B'
    }
```

```
    D d;
    f(d);
```

### ### Exemple

```
    class B { // BON : classe polymorphe supprime la copie
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
```

```
    void f(B& b)
    {
        auto b2 = b; // ok, compilateur détecte copie involontaire et se plaint
    }
```

```
    D d;
    f(d);
```

### ### Remarque

Si vous avez besoin de copies profondes d’objets polymorphes, utilisez `clone()` : voir [C.130](#rh-copy).

### ### Exception

Les classes représentant des objets d’exception doivent être polymorphes et copy‑constructible.

### ### Mise en œuvre

* Marquer une classe polymorphe avec une opération de copie publique.
* Marquer une affectation d’objets polymorphes.

---

## C.other : Autres règles d’opérations par défaut

En plus des opérations offertes par le langage, il existe quelques opérations fondamentales qui nécessitent des règles spécifiques : comparaisons, `swap`, et `hash`.

### <a name="rc-eqdefault"></a>C.80 : Utiliser `=default` si vous avez besoin de préciser que vous utilisez la sémantique par défaut

### ### Raisonnement

Le compilateur est plus susceptible de produire la sémantique par défaut et vous ne pouvez pas implémenter ces fonctions mieux que le compilateur.

### ### Exemple

```
    class Tracer {
        string message;
    public:
        Tracer(const string& m) : message{m} { cerr << "entree " << message << '\n'; }
        ~Tracer() { cerr << "sortie " << message << '\n'; }

        Tracer(const Tracer&) = default;
        Tracer& operator=(const Tracer&) = default;
        Tracer(Tracer&&) noexcept = default;
        Tracer& operator=(Tracer&&) noexcept = default;
    };
```

Comme on a défini un destructeur, on doit définir les copies/mouvements. `= default` est la meilleure façon de le faire.

### ### Exemple, mauvais

```
    class Tracer2 {
        string message;
    public:
        Tracer2(const string& m) : message{m} { cerr << "entree " << message << '\n'; }
        ~Tracer2() { cerr << "sortie " << message << '\n'; }

        Tracer2(const Tracer2& a) : message{a.message} {}
        Tracer2& operator=(const Tracer2& a) { message = a.message; return *this; }
        Tracer2(Tracer2&& a) noexcept :message{a.message} {}
        Tracer2& operator=(Tracer2&& a) noexcept { message = a.message; return *this; }
    };
```

Écrire les corps des opérations par copie/déplacement est verbeux, fastidieux et sujet à erreur.  
Le compilateur fait mieux.

### ### Mise en œuvre

(Moyen) Le corps d’une opération définie par l’utilisateur ne doit pas avoir les mêmes sémantiques qu’une valeur par défaut générée, car cela serait redondant.

---

### <a name="rc-delete"></a>C.81 : Utiliser `=delete` lorsque vous voulez désactiver le comportement par défaut (sans vouloir d’alternative)

### ### Raisonnement

Dans quelques cas, une opération par défaut n’est pas souhaitable.

### ### Exemple

```
    class Immortal {
    public:
        ~Immortal() = delete;   // ne pas autoriser la destruction
        // ...
    };
```

```
    void use()
    {
        Immortal ugh;   // erreur : ugh ne peut être détruit
        Immortal* p = new Immortal{};
        delete p;       // erreur : ne peut pas détruire *p
    }
```

### ### Exemple

`unique_ptr` peut être déplacé mais pas copié. Pour qu’il ne puisse pas être copié, on déclare les opérations de copie et d’affectation par lvalue `=delete`.

```
    template<class T, class D = default_delete<T>> class unique_ptr {
    public:
        // ...
        constexpr unique_ptr() noexcept;
        explicit unique_ptr(pointer p) noexcept;
        // ...
        unique_ptr(unique_ptr&& u) noexcept;   // constructeur de déplacement
        // ...
        unique_ptr(const unique_ptr&) = delete; // empêcher la copie d'une lvalue
        // ...
    };
```

```
    unique_ptr<int> make();   // fabriquer quelque chose et renvoyer le résultat par déplacement

    void f()
    {
        unique_ptr<int> pi {};
        auto pi2 {pi};      // erreur : pas de constructeur de déplacement d’une lvalue
        auto pi3 {make()};  // ok, déplacement : l’opération `make()` est un rvalue
    }
```

Les fonctions supprimées devraient être publiques.

### ### Mise en œuvre

La suppression d’une opération par défaut est (devrait être) motivée par la sémantique voulue.  
Considérez ces classes suspectes mais maintenez une « liste positive » de classes où le programmeur a affirmé que la sémantique est correcte.

---

### <a name="rc-ctor-virtual"></a>C.82 : N’appeler pas les fonctions virtuelles dans les constructeurs et destructeurs

### ### Raisonnement

La fonction appelée sera celle de l’objet déjà construit, pas d’une éventuelle version dérivée.  
Cela peut être confus.
Une appel directe/nécessaire à une fonction virtuelle non‐implémentée dans un constructeur ou destructeur entraîne un comportement indéfini.

### ### Exemple, mauvais

```
    class Base {
    public:
        virtual void f() = 0;   // non implémenté
        virtual void g();       // implémenté dans Base
        virtual void h();       // implémenté dans Base
        virtual ~Base();        // implémenté dans Base
    };

    class Derived : public Base {
    public:
        void g() override;   // provides Derived implementation
        void h() final;      // provides Derived implementation

        Derived()
        {
            // MAUVAIS : boucle a un appel d’une fonction virtuelle non‑implémentée
            f();

            // MAUVAIS : invoquera Derived::g, pas dispatch plus tard
            g();

            // BON : appeler explicitement la fonction visible
            Derived::g();

            // Ok, pas de qualification, h est final
            h();
        }
    };
```

Notez que appeler une fonction explicitement qualifiée n’est pas une appel virtuel même si elle est `virtual`.

**Voir aussi** : [fonctions de fabrique] (#rc-factory) pour reproduire l’effet d’un appel à une fonction dérivée sans risque d’undefined behavior.

### ### Remarque

Il n’est pas intrinsèquement mauvais d’appeler les fonctions virtuelles depuis les constructeurs et destructeurs.  
Les sémantiques de ces appels sont valides.  
Cependant, l’expérience indique que ces appels sont rarement nécessaires, faciles à confondre et deviennent une source d’erreurs lorsque novices l’utilisent.

### ### Mise en œuvre

* Marquer les appels de fonctions virtuelles depuis les constructeurs et destructeurs.

---

### <a name="rc-swap"></a>C.83 : Pour les types de valeur, envisager de fournir une fonction `swap` `noexcept`

### ### Raisonnement

Un `swap` peut être utile pour implémenter divers idiomes, du déplacement d’objets à l’implémentation d’affectation ou de commit sûr en cas d’erreur.  
Envisager l’utilisation de `swap` pour implémenter l’affectation par copie en termes de construction par copie.

### ### Exemple, bon

```
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
```

Fournir une fonction `swap` membre ou une surcharge non‑membre dans le même espace de noms que le type pour la commodité du paqueteur.

```
    void swap(Foo& a, Foo& b)
    {
        a.swap(b);
    }
```

### ### Mise en œuvre

* Les types non trivially copyable doivent fournir une fonction `swap` membre ou une surcharge non‑membre.
* (Simple) Lorsqu'une classe possède une méthode `swap`, elle doit être déclarée `noexcept`.

---

### <a name="rc-swap-fail"></a>C.84 : Un `swap` doit ne pas échouer

### ### Raisonnement

`swap` est largement utilisé dans des contextes qui s’obligent à ne jamais échouer et il est difficile d’écrire des programmes corrects lorsqu’un `swap` échoue.

Les containers et algorithmes de la bibliothèque standard ne fonctionneront pas correctement si `swap` d’un type échoue.

### ### Exemple, mauvais

```
    void swap(My_vector& x, My_vector& y)
    {
        auto tmp = x;   // copy elements
        x = y;
        y = tmp;
    }
```

C’est non seulement lent mais si une allocation de mémoire se produit pour les éléments de `tmp`, ce `swap` pourra lancer une exception et rendra les STL algorithms désordonnés.

### ### Mise en œuvre

Simple) Lorsqu’une classe possède une fonction don swap, elle devrait être `noexcept`.

---

### <a name="rc-swap-noexcept"></a>C.85 : Faire `swap` `noexcept`

### ### Raisonnement

Voir [C.84] (#rc-swap-fail).

### ### Mise en œuvre

Simple) Quand une classe possède un `swap`, il devrait être `noexcept`.

---

### <a name="rc-eq"></a>C.86 : Faire `==` symétrique par rapport aux types d’opérande et `noexcept`

### ### Raisonnement

Le traitement asymétrique des opérandes est surprenant et source d'erreurs où des conversions sont possibles.  
`==` est une opération fondamentale et les programmeurs doivent pouvoir l’utiliser sans crainte d’échec.

### ### Exemple

```
    struct X {
        string name;
        int number;
    };

    bool operator==(const X& a, const X& b) noexcept {
        return a.name == b.name && a.number == b.number;
    }
```

### ### Exemple, mauvais

```
    class B {
        string name;
        int number;
        bool operator==(const B& a) const {
            return name == a.name && number == a.number;
        }
        // ...
    };
```

`B`’s comparison accepts conversions for its second operand, but not for the first.

### ### Remarque

Si une classe a un état d’échec, tel que `double NaN`, il es préférable de ne pas faire lever une exception.  Alternativement, faites deux états d’échec comparables égaux et tout état valide comparez faussement.

Cette règle s’applique à tous les opérateurs de comparaison usuels : `!=`, `<`, `<=`, `>`, `>=`.

### ### Mise en œuvre

* Marquer un `operator==()` pour lequel les types d’arguments diffèrent ; idem pour les autres opérateurs (`!=`, `<`, `<=`, `>`, `>=`).
* Marquer les `operator==()` membres ; idem pour les autres opérateurs.

---

### <a name="rc-eq-base"></a>C.87 : Méfiez‑vous de `==` sur les classes de base

### ### Raisonnement

Il est très difficile d’écrire un `==` fiable et utile pour une hiérarchie.

### ### Exemple, bad

```
    class B {
    public:
        string name;
        int number;
    };
```

**…** (Example continues but truncated due to length limit).