# <a name="s-class"></a>C : Classes et hiérarchies de classes

Une classe est un type défini par l'utilisateur, pour lequel le programmeur peut définir la représentation, les opérations et les interfaces.  
Les hiérarchies de classes sont utilisées pour organiser des classes liées au sein de structures hiérarchiques.

**Résumé des règles concernant les classes :**

* [C.1 : Organiser les données liées dans des structures (`struct`s ou `class`es)](007-class.md#rc-org) @TODO-LINK
* [C.2 : Utiliser `class` si la classe possède une invariant ; utiliser `struct` si les membres de données peuvent varier indépendamment](007-class.md#rc-struct) @TODO-LINK
* [C.3 : Représenter la distinction entre une interface et une implémentation à l’aide d’une classe](007-class.md#rc-interface) @TODO-LINK
* [C.4 : Faire d’une fonction un membre uniquement si elle a besoin d’un accès direct à la représentation d’une classe](007-class.md#rc-member) @TODO-LINK
* [C.5 : Placer les fonctions auxiliaires dans le même espace de noms que la classe qu’elles supportent](007-class.md#rc-helper) @TODO-LINK
* [C.7 : Ne pas définir une classe ou une énumération et déclarer une variable de son type dans la même instruction](007-class.md#rc-standalone) @TODO-LINK
* [C.8 : Utiliser `class` plutôt que `struct` si un membre n’est pas public](007-class.md#rc-class) @TODO-LINK
* [C.9 : Réduire l’exposition des membres](007-class.md#rc-private) @TODO-LINK

**Sous‑sections :**

* [C.concrete : Types concrets](007-class.md#ss-concrete) @TODO-LINK
* [C.ctor : Constructeurs, affectations et destructeurs](007-class.md) @TODO-LINK
* [C.con : Conteneurs et autres gestionnaires de ressources](007-class.md#ss-containers) @TODO-LINK
* [C.lambdas : Objets fonctionnels et lambdas](007-class.md#ss-lambdas) @TODO-LINK
* [C.hier : Hiérarchies de classes (POO)](007-class.md#ss-hier) @TODO-LINK
* [C.over : Surcharge et opérateurs surchargés](007-class.md#ss-overload) @TODO-LINK
* [C.union : Unions](007-class.md#ss-union) @TODO-LINK

---

### <a name="rc-org"></a>C.1 : Organiser les données liées dans des structures (`struct`s ou `class`es)

##### Raison  

Facilité de compréhension.  
Si les données sont liées (pour des raisons fondamentales), ce fait doit être reflété dans le code.

##### Exemple  

```    
    void draw(int x, int y, int x2, int y2);  // MAUVAIS : relations implicites inutiles
    void draw(Point from, Point to);          // meilleur
```    

##### Remarque  

Une classe simple sans fonctions virtuelles n’implique aucun surcoût d’espace ou de temps.

##### Remarque  

Du point de vue du langage, `class` et `struct` ne diffèrent que par la visibilité par défaut de leurs membres.

##### Application  

Probablement impossible. Un heuristique cherchant des éléments de données souvent utilisés ensemble pourrait être envisageable.

---

### <a name="rc-struct"></a>C.2 : Utiliser `class` si la classe possède une invariant ; utiliser `struct` si les membres de données peuvent varier indépendamment

##### Raison  

Lisibilité.  
Facilité de compréhension.  
L’usage de `class` alerte le programmeur sur la nécessité d’une invariant.  
C’est une convention utile.

##### Remarque  

Une invariant est une condition logique sur les membres d’un objet qu’un constructeur doit établir pour que les fonctions membres publiques puissent s’y appuyer. Après l’établissement de l’invariant (généralement par le constructeur), chaque fonction membre peut être invoquée pour l’objet. L’invariant peut être formulé de façon informelle (par ex. dans un commentaire) ou plus formellement à l’aide de `Expects`.

Si tous les membres de données peuvent varier indépendamment les uns des autres, aucune invariant n’est possible.

##### Exemple  

```    
    struct Pair {  // les membres peuvent varier indépendamment
        string name;
        int volume;
    };
```

mais :

```    
    class Date {
    public:
        // valider que {yy, mm, dd} forme une date valide et initialiser
        Date(int yy, Month mm, char dd);
        // …
    private:
        int y;
        Month m;
        char d;    // jour
    };
```    

##### Remarque  

Si une classe possède des données `private`, l’utilisateur ne peut pas initialiser complètement un objet sans recourir à un constructeur. Ainsi, le concepteur de la classe devra fournir un constructeur et préciser son sens. Cela signifie effectivement que le concepteur doit définir une invariant.

**Voir aussi** :

* [définir une classe avec des données privées comme `class`](007-class.md#rc-class) @TODO-LINK
* [Préférer placer l’interface en premier dans une classe](024-naming.md#rl-order) @TODO-LINK
* [minimiser l’exposition des membres](007-class.md#rc-private) @TODO-LINK
* [Éviter les données `protected`](007-class.md#rh-protected) @TODO-LINK

##### Application  

Détecter les `struct`s dont tous les membres sont privés et les `class`es comportant des membres publics.

---

### <a name="rc-interface"></a>C.3 : Représenter la distinction entre une interface et une implémentation à l’aide d’une classe

##### Raison  

Une distinction explicite entre interface et implémentation améliore la lisibilité et simplifie la maintenance.

##### Exemple  

```    
    class Date {
    public:
        Date();
        // valider que {yy, mm, dd} forme une date valide et initialiser
        Date(int yy, Month mm, char dd);

        int day() const;
        Month month() const;
        // …
    private:
        // … représentation interne …
    };
```

Par exemple, on peut maintenant changer la représentation d’un `Date` sans affecter ses utilisateurs (une recompilation sera probablement nécessaire, toutefois).

##### Remarque  

Utiliser une classe de cette façon pour représenter la distinction entre interface et implémentation n’est bien sûr pas la seule méthode. On peut, par exemple, recourir à un ensemble de fonctions libres dans un espace de noms, à une classe abstraite de base, ou à un modèle de fonction avec des concepts pour représenter une interface. L’enjeu principal est de distinguer explicitement une interface de ses « détails » d’implémentation. Idéalement, et typiquement, une interface est bien plus stable que ses implémentations.

##### Application  

???

---

### <a name="rc-member"></a>C.4 : Faire d’une fonction un membre uniquement si elle nécessite un accès direct à la représentation d’une classe

##### Raison  

Moins d’accouplement qu’avec les fonctions membres, moins de fonctions susceptibles de causer des problèmes en modifiant l’état d’un objet, ce qui réduit le nombre de fonctions à modifier après un changement de représentation.

##### Exemple  

```    
    class Date {
        // … interface relativement petite …
    };

    // fonctions auxiliaires :
    Date next_weekday(Date);
    bool operator==(Date, Date);
```

Les « fonctions auxiliaires » n’ont pas besoin d’un accès direct à la représentation d’un `Date`.

##### Remarque  

Cette règle devient encore plus pertinente si le C++ adopte le « uniform function call » (voir : <https://www.open-std.org/jtc1/sc22/wg21/docs/papers/2016/p0251r0.pdf>).

##### Exception  

Le langage exige que les fonctions `virtual` soient membres, et toutes les fonctions `virtual` ne touchent pas forcément les données. En particulier, les membres d’une classe abstraite le font rarement.  
Voir [multi‑methods](https://web.archive.org/web/20200605021759/https://parasol.tamu.edu/~yuriys/papers/OMM10.pdf).

##### Exception  

Le langage impose que les opérateurs `=`, `()`, `[]` et `->` soient membres.

##### Exception  

Un ensemble de surcharges peut contenir des membres qui n’accèdent pas directement aux données `private` :

```    
    class Foobar {
    public:
        void foo(long x) { /* manipuler les données privées */ }
        void foo(double x) { foo(std::lround(x)); }
        // …
    private:
        // …
    };
```    

##### Exception  

De même, un ensemble de fonctions peut être conçu pour être utilisé en chaîne :

```    
    x.scale(0.5).rotate(45).set_color(Color::red);
```

Typiquement, certaines mais pas toutes ces fonctions accèdent directement aux données `private`.

##### Application  

* Rechercher les fonctions membres non‑`virtual` qui ne touchent pas directement les membres de données. Le problème est que de nombreuses fonctions membres qui n’ont pas besoin d’accéder directement aux membres le font quand même.  
* Ignorer les fonctions `virtual`.  
* Ignorer les fonctions qui font partie d’un ensemble de surcharges dont au moins une fonction accède aux membres `private`.  
* Ignorer les fonctions retournant `this`.

---

### <a name="rc-helper"></a>C.5 : Placer les fonctions auxiliaires dans le même espace de noms que la classe qu’elles supportent

##### Raison  

Une fonction auxiliaire est une fonction (souvent fournie par l’auteur d’une classe) qui n’a pas besoin d’un accès direct à la représentation de la classe, mais qui fait partie de l’interface utile de la classe. La placer dans le même espace de noms rend sa relation avec la classe évidente et permet de la retrouver grâce à la recherche dépendante des arguments (ADL).

##### Exemple  

```    
    namespace Chrono { // ici nous conservons les services liés au temps

        class Time { /* … */ };
        class Date { /* … */ };

        // fonctions auxiliaires :
        bool operator==(Date, Date);
        Date next_weekday(Date);
        // …
    }
```    

##### Remarque  

C’est particulièrement important pour les [opérateurs surchargés](007-class.md#ro-namespace) @TODO-LINK.

##### Application  

* Signaler les fonctions globales dont les arguments proviennent d’un seul espace de noms.

---

### <a name="rc-standalone"></a>C.7 : Ne pas définir une classe ou une énumération et déclarer une variable de son type dans la même instruction

##### Raison  

Mélanger une définition de type et la définition d’une autre entité dans la même déclaration crée de la confusion et est inutile.

##### Exemple, mauvais  

```    
    struct Data { /*…*/ } data{ /*…*/ };
```    

##### Exemple, bon  

```    
    struct Data { /*…*/ };
    Data data{ /*…*/ };
```    

##### Application  

* Signaler lorsqu’un `}` de définition de classe ou d’énumération n’est pas suivi d’un `;`. Le point‑virgule est manquant.

---

### <a name="rc-class"></a>C.8 : Utiliser `class` plutôt que `struct` si un membre n’est pas public

##### Raison  

Lisibilité.  
Rendre clair que quelque chose est caché/abstrait.  
C’est une convention utile.

##### Exemple, mauvais  

```    
    struct Date {
        int d, m;

        Date(int i, Month m);
        // … beaucoup de fonctions …
    private:
        int y;  // année
    };
```    

Il n’y a rien d’illégal dans ce code du point de vue du langage C++, mais pratiquement tout est problématique du point de vue de la conception.  
Les données privées sont cachées loin des données publiques.  
Les données sont réparties en différentes parties de la déclaration de la classe.  
Les différentes parties disposent d’un accès distinct.  
Tout cela diminue la lisibilité et complique la maintenance.

##### Remarque  

Préférer placer l’interface en premier dans une classe, [voir NL.16](024-naming.md#rl-order) @TODO-LINK.

##### Application  

Signaler les `struct` qui contiennent des membres `private` ou `protected`.

---

### <a name="rc-private"></a>C.9 : Minimiser l’exposition des membres

##### Raison  

Encapsulation.  
Masquage de l’information.  
Réduire le risque d’accès involontaire.  
Cela simplifie la maintenance.

##### Exemple  

```    
    template<typename T, typename U>
    struct pair {
        T a;
        U b;
        // …
    };
```    

Quoi que nous fassions dans la partie `//`, un utilisateur arbitraire d’un `pair` peut modifier librement et indépendamment son `a` et son `b`.  
Dans une base de code importante, il est difficile de repérer quel code agit sur quels membres du `pair`.  
Cela peut être exactement ce que l’on souhaite, mais si l’on veut imposer une relation entre les membres, il faut les rendre `private` et faire respecter cette relation (invariant) via les constructeurs et les fonctions membres.  
Par exemple :

```    
    class Distance {
    public:
        // …
        double meters() const { return magnitude*unit; }
        void set_unit(double u)
        {
                // … vérifier que `u` est un facteur de 10 …
                // … ajuster `magnitude` en conséquence …
                unit = u;
        }
        // …
    private:
        double magnitude;
        double unit;    // 1 = mètres, 1000 = kilomètres, 0.001 = millimètres, etc.
    };
```    

##### Remarque  

Si l’ensemble des utilisateurs directs d’un ensemble de variables ne peut pas être déterminé facilement, le type ou l’utilisation de cet ensemble ne pourra pas être (facilement) modifié ou amélioré. Pour les données `public` et `protected`, c’est généralement le cas.

##### Exemple  

Une classe peut offrir deux interfaces à ses utilisateurs.  
Une pour les classes dérivées (`protected`) et une pour les utilisateurs généraux (`public`).  
Par exemple, une classe dérivée peut être autorisée à ignorer un contrôle d’exécution parce qu’elle a déjà garanti la validité :

```    
    class Foo {
    public:
        int bar(int x) { check(x); return do_bar(x); }
        // …
    protected:
        int do_bar(int x); // exécuter une opération sur les données
        // …
    private:
        // … données …
    };

    class Dir : public Foo {
        // …
        int mem(int x, int y)
        {
            /* … faire quelque chose … */
            return do_bar(x + y); // OK : la classe dérivée peut contourner le contrôle
        }
    };

    void user(Foo& x)
    {
        int r1 = x.bar(1);      // OK, vérification effectuée
        int r2 = x.do_bar(2);   // erreur : contournerait le contrôle
        // …
    }
```    

##### Remarque  

[`protected` data is a bad idea](007-class.md#rh-protected) @TODO-LINK.

##### Remarque  

Préférer l’ordre « public » → « protected » → « private », voir [NL.16](024-naming.md#rl-order) @TODO-LINK.

##### Application  

* [Signaler les données `protected`](007-class.md#rh-protected) @TODO-LINK.  
* Signaler les mélanges de données `public` et `private`.

---

## <a name="ss-concrete"></a>C.concrete : Types concrets

Résumé des règles concernant les types concrets :

* [C.10 : Préférer les types concrets aux hiérarchies de classes](007-class.md#rc-concrete) @TODO-LINK
* [C.11 : Rendre les types concrets réguliers](007-class.md#rc-regular) @TODO-LINK
* [C.12 : Ne pas rendre les membres de données `const` ou des références dans un type copiable ou déplaçable](007-class.md#rc-constref) @TODO-LINK
* [C.13 : Si le membre de donnée `B` utilise le membre de donnée `A`, déclarer `A` avant `B`](007-class.md#rc-lifetime) @TODO-LINK

### <a name="rc-concrete"></a>C.10 : Préférer les types concrets aux hiérarchies de classes

##### Raison  

Un type concret est fondamentalement plus simple qu’un type appartenant à une hiérarchie de classes : plus facile à concevoir, à implémenter, à utiliser, à raisonner, plus petit et plus rapide. Vous avez besoin d’une raison (cas d’usage) pour utiliser une hiérarchie.

##### Exemple  

```    
    class Point1 {
        int x, y;
        // … opérations …
        // … aucune fonction virtuelle …
    };

    class Point2 {
        int x, y;
        // … opérations, certaines virtuelles …
        virtual ~Point2();
    };

    void use()
    {
        Point1 p11 {1, 2};   // créer un objet sur la pile
        Point1 p12 {p11};    // copie

        auto p21 = make_unique<Point2>(1, 2);   // créer un objet sur le tas
        auto p22 = p21->clone();                // faire une copie
        // …
    }
```  

Si une classe fait partie d’une hiérarchie, on (dans le code réel, pas forcément dans les petits exemples) doit manipuler ses objets via des pointeurs ou des références. Cela implique un surcoût mémoire, davantage d’allocations/désallocations et un surcoût d’exécution lié aux indirections.

##### Remarque  

Les types concrets peuvent être alloués sur la pile et devenir membres d’autres classes.

##### Remarque  

L’utilisation de l’indirection est fondamentale pour les interfaces polymorphes d’exécution. Le surcoût d’allocation/désallocation n’est pas (c’est simplement le cas le plus fréquent). Nous pouvons utiliser une classe de base comme interface d’un objet à durée de vie limitée d’une classe dérivée. Cela se fait lorsque l’allocation dynamique est interdite (par ex. en temps réel strict) et pour fournir une interface stable à certains types de plug‑ins.

##### Application  

???

### <a name="rc-regular"></a>C.11 : Rendre les types concrets réguliers

##### Raison  

Les types réguliers sont plus simples à comprendre et à raisonner que les types irréguliers (les irrégularités exigent un effort supplémentaire pour être compris et utilisés).

Les types intégrés de C++ sont réguliers, tout comme les classes de la bibliothèque standard telles que `string`, `vector` et `map`. Les classes concrètes dépourvues d’opérations d’affectation et d’égalité peuvent être définies, mais elles devraient rester rares.

##### Exemple  

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
    if (!(b1 == b2)) error("impossible !");
    b2.name = "the other bundle";
    if (b1 == b2) error("No !");
```  

En particulier, si un type concret est copiable, il faut préférer lui fournir également un opérateur d’égalité, et s’assurer que `a = b` implique `a == b`.

##### Remarque  

Pour les `struct` destinés à être partagés avec du code C, définir `operator==` peut ne pas être faisable.

##### Remarque  

Les gestionnaires de ressources qui ne peuvent pas être clonés, par ex. un `scoped_lock` pour un `mutex`, sont des types concrets mais généralement non copiables (ils peuvent toutefois être déplacés), ils ne peuvent donc pas être réguliers ; ils sont habituellement « move‑only ».

##### Application  

??

### <a name="rc-constref"></a>C.12 : Ne pas rendre les membres de données `const` ou des références dans un type copiable ou déplaçable

##### Raison  

Les membres `const` et les références ne sont pas utiles dans un type copiable ou déplaçable, et rendent ces types difficiles à utiliser en les rendant en partie non‑copiables/non‑déplaçables pour des raisons subtiles.

##### Exemple ; mauvais  

```    
    class bad {
        const int i;    // mauvais
        string& s;      // mauvais
        // …
    };
```  

Les membres `const` et `&` font de cette classe un « seulement‑un‑peu‑copiable » — constructible par copie mais non assignable.

##### Remarque  

Si vous avez besoin d’un membre qui pointe vers quelque chose, utilisez un pointeur (brut ou intelligent, et `gsl::not_null` s’il ne doit pas être nul) plutôt qu’une référence.

##### Application  

Signaler tout membre de données qui est `const`, `&` ou `&&` dans un type qui possède une quelconque opération de copie ou de déplacement.

### <a name="rc-lifetime"></a>C.13 : Si le membre de donnée `B` utilise le membre de donnée `A`, déclarer `A` avant `B`

##### Raison  

Les membres de données sont initialisés dans l’ordre où ils sont déclarés, et détruits dans l’ordre inverse.

##### Discussion  

Si le membre de donnée `B` utilise le membre de donnée `A`, alors `A` doit être déclaré avant `B` afin que `A` survivent plus longtemps que `B` : le temps de vie de `A` commence avant et se termine après celui de `B`. Sinon, pendant la construction et la destruction, `B` tentera d’utiliser `A` en dehors de son temps de vie.

##### Exemple ; mauvais  

```    
    // Mauvais : b utilise a, mais a est déclaré après b.
    //      L’ordre de construction est b puis a ; l’ordre de destruction est a puis b.
    //      Ainsi b touche a hors du temps de vie de a.

    class X {
        struct B {
            string* p;
            explicit B(string& a) : p{&a} {}
            ~B() { cout << *p; }                       // utilise a (via p)
        };

        B      b;                                      // construit en premier
        string a = "some heap allocated string value"; // construit après b ; détruit avant b

    public:
        X() : b{a} {}   // utilise a avant qu’il ne soit construit → UB use‑before‑init
        ~X() = default; // accède à a après sa destruction → UB use‑after‑free
    };
```  

##### Exemple ; bon  

```    
    // Corrigé : simplement déclarer a avant b

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
```  

##### Exemple ; mauvais (concurrence)  

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

##### Exemple ; bon (concurrence)  

```    
    // Corrigé : simplement déclarer a avant b

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

##### Application  

* Signaler tout initialiseur de membre qui se réfère à un objet avant que celui‑ci ne soit déjà construit.

---

## <a name="s-ctor"></a>C.ctor : Constructeurs, affectations et destructeurs

Ces fonctions contrôlent le cycle de vie des objets : création, copie, déplacement et destruction.  
Définissez les constructeurs pour garantir et simplifier l’initialisation des classes.

Ces fonctions sont les *opérations par défaut* :

* un constructeur par défaut : `X()`
* un constructeur de copie : `X(const X&)`
* une affectation de copie : `operator=(const X&)`
* un constructeur de déplacement : `X(X&&)`
* une affectation de déplacement : `operator=(X&&)`
* un destructeur : `~X()`

Par défaut, le compilateur génère chacune de ces opérations si elle est utilisée, mais la génération par défaut peut être supprimée.

Les opérations par défaut constituent un ensemble d’opérations liées qui, ensemble, implémentent la sémantique du cycle de vie d’un objet. Par défaut, C++ traite les classes comme des types à valeur, mais tous les types ne sont pas à valeur.

**Règles concernant les opérations par défaut :**

* [C.20 : Si vous pouvez éviter de définir des opérations par défaut, faites‑le](007-class.md#rc-zero) @TODO-LINK
* [C.21 : Si vous définissez ou `=delete` une fonction de copie, de déplacement ou de destructeur, définissez‑les ou `=delete` toutes](007-class.md#rc-five) @TODO-LINK
* [C.22 : Rendre les opérations par défaut cohérentes](007-class.md#rc-matched) @TODO-LINK

**Règles concernant le destructeur :**

* [C.30 : Définir un destructeur si une classe a besoin d’une action explicite à la destruction de l’objet](007-class.md#rc-dtor) @TODO-LINK
* [C.31 : Toutes les ressources acquises par une classe doivent être libérées par le destructeur de la classe](007-class.md#rc-dtor-release) @TODO-LINK
* [C.32 : Si une classe possède un pointeur brut (`T*`) ou une référence (`T&`), se demander si elle peut être propriétaire](007-class.md#rc-dtor-ptr) @TODO-LINK
* [C.33 : Si une classe possède un membre pointeur propriétaire, définir un destructeur](007-class.md#rc-dtor-ptr2) @TODO-LINK
* [C.35 : Le destructeur d’une classe de base doit être soit public et virtuel, soit protégé et non‑virtuel](007-class.md#rc-dtor-virtual) @TODO-LINK
* [C.36 : Un destructeur ne doit pas échouer](007-class.md#rc-dtor-fail) @TODO-LINK
* [C.37 : Rendre les destructeurs `noexcept`](007-class.md#rc-dtor-noexcept) @TODO-LINK

**Règles concernant le constructeur :**

* [C.40 : Définir un constructeur si une classe possède une invariant](007-class.md#rc-ctor) @TODO-LINK
* [C.41 : Un constructeur doit créer un objet entièrement initialisé](007-class.md#rc-complete) @TODO-LINK
* [C.42 : Si un constructeur ne peut pas construire un objet valide, lancer une exception](007-class.md#rc-throw) @TODO-LINK
* [C.43 : Veiller à ce qu’une classe copiable possède un constructeur par défaut](007-class.md#rc-default0) @TODO-LINK
* [C.44 : Préférer que les constructeurs par défaut soient simples et ne lèvent pas d’exceptions](007-class.md#rc-default00) @TODO-LINK
* [C.45 : Ne pas définir de constructeur par défaut qui ne fait qu’initialiser les membres ; utiliser les initialiseurs de membres par défaut à la place](007-class.md#rc-default) @TODO-LINK
* [C.46 : Déclarer `explicit` les constructeurs à un seul argument par défaut](007-class.md#rc-explicit) @TODO-LINK
* [C.47 : Définir et initialiser les membres de données dans l’ordre de leur déclaration](007-class.md#rc-order) @TODO-LINK
* [C.48 : Préférer les initialiseurs de membres par défaut aux initialiseurs de membres dans les constructeurs pour les initialiseurs constants](007-class.md#rc-in-class-initializer) @TODO-LINK
* [C.49 : Préférer l’initialisation à l’affectation dans les constructeurs](007-class.md#rc-initialize) @TODO-LINK
* [C.50 : Utiliser une fonction fabrique si vous avez besoin d’un « comportement virtuel » pendant l’initialisation](007-class.md#rc-factory) @TODO-LINK
* [C.51 : Utiliser les constructeurs délégants pour représenter les actions communes à tous les constructeurs d’une classe](007-class.md#rc-delegating) @TODO-LINK
* [C.52 : Utiliser les constructeurs hérités pour importer les constructeurs dans une classe dérivée qui n’a pas besoin d’une initialisation supplémentaire explicite](007-class.md#rc-inheriting) @TODO-LINK

**Règles concernant la copie et le déplacement :**

* [C.60 : Rendre l’affectation de copie non‑`virtual`, prendre le paramètre par `const&` et retourner par `non‑const&`](007-class.md#rc-copy-assignment) @TODO-LINK
* [C.61 : Une opération de copie doit copier](007-class.md#rc-copy-semantic) @TODO-LINK
* [C.62 : Rendre l’affectation de copie sûre pour l’auto‑affectation](007-class.md#rc-copy-self) @TODO-LINK
* [C.63 : Rendre l’affectation de déplacement non‑`virtual`, prendre le paramètre par `&&` et retourner par `non‑const&`](007-class.md#rc-move-assignment) @TODO-LINK
* [C.64 : Une opération de déplacement doit déplacer et laisser sa source dans un état valide](007-class.md#rc-move-semantic) @TODO-LINK
* [C.65 : Rendre l’affectation de déplacement sûre pour l’auto‑affectation](007-class.md#rc-move-self) @TODO-LINK
* [C.66 : Rendre les opérations de déplacement `noexcept`](007-class.md#rc-move-noexcept) @TODO-LINK
* [C.67 : Une classe polymorphe doit supprimer les copies publiques/mouvements](007-class.md#rc-copy-virtual) @TODO-LINK

**Autres règles concernant les opérations par défaut :**

* [C.80 : Utiliser `=default` si vous devez être explicite sur l’utilisation de la sémantique par défaut](007-class.md#rc-eqdefault) @TODO-LINK
* [C.81 : Utiliser `=delete` lorsqu’on veut désactiver le comportement par défaut (sans vouloir une alternative)](007-class.md#rc-delete) @TODO-LINK
* [C.82 : Ne pas appeler de fonctions virtuelles dans les constructeurs et destructeurs](007-class.md#rc-ctor-virtual) @TODO-LINK
* [C.83 : Pour les types à valeur, envisager de fournir une fonction `swap` `noexcept`](007-class.md#rc-swap) @TODO-LINK
* [C.84 : Un `swap` ne doit pas échouer](007-class.md#rc-swap-fail) @TODO-LINK
* [C.85 : Rendre `swap` `noexcept`](007-class.md#rc-swap-noexcept) @TODO-LINK
* [C.86 : Rendre `==` symétrique du point de vue des types d’opérandes et `noexcept`](007-class.md#rc-eq) @TODO-LINK
* [C.87 : Se méfier de `==` sur les classes de base](007-class.md#rc-eq-base) @TODO-LINK
* [C.89 : Rendre un `hash` `noexcept`](007-class.md#rc-hash) @TODO-LINK
* [C.90 : S’appuyer sur les constructeurs et les opérateurs d’affectation, pas sur `memset` et `memcpy`](007-class.md#rc-memset) @TODO-LINK

---

## <a name="ss-defop"></a>C.defop : Opérations par défaut

Par défaut, le langage fournit les opérations par défaut avec leurs sémantiques standards. Cependant, le programmeur peut désactiver ou remplacer ces défauts.

### <a name="rc-zero"></a>C.20 : Si vous pouvez éviter de définir des opérations par défaut, faites‑le

##### Raison  

C’est la manière la plus simple et donne les sémantiques les plus propres.

##### Exemple  

```    
    struct Named_map {
    public:
        explicit Named_map(const string& n) : name(n) {}
        // pas de constructeurs/copieurs/déplaceurs
        // pas d’opérateur d’affectation copie/déplacement
        // pas de destructeur
    private:
        string name;
        map<int, int> rep;
    };

    Named_map nm("map"); // construction
    Named_map nm2 {nm};  // construction par copie
```  

Comme `std::map` et `string` possèdent toutes les fonctions spéciales, aucun travail supplémentaire n’est nécessaire.

##### Remarque  

C’est ce qu’on appelle « la règle du zéro ».

##### Application  

(N’est pas enforceable) Bien qu’on ne puisse pas l’obliger, un bon analyseur statique peut détecter des motifs indiquant une amélioration possible pour satisfaire cette règle. Par exemple, une classe avec une paire (pointeur, taille) de membres et un destructeur qui `delete` le pointeur pourrait probablement être transformée en `vector`.

### <a name="rc-five"></a>C.21 : Si vous définissez ou `=delete` une fonction de copie, de déplacement ou de destructeur, définissez ou `=delete` toutes les fonctions similaires

##### Raison  

Les sémantiques de copie, déplacement et destruction sont étroitement liées ; si l’une doit être déclarée, il est fort probable que les autres nécessitent également une réflexion.

Déclarer une fonction de copie/déplacement/destructeur,
même en tant que `=default` ou `=delete`, supprime la génération implicite d’un constructeur de déplacement et d’un opérateur d’affectation de déplacement. Déclarer un constructeur de déplacement ou un opérateur d’affectation de déplacement, même en tant que `=default` ou `=delete`, force la génération d’un constructeur de copie ou d’un opérateur d’affectation de copie implicite à être déclaré `deleted`. Ainsi, dès qu’une de ces fonctions est déclarée, les autres doivent être déclarées pour éviter des effets indésirables tels que transformer tous les mouvements potentiels en copies coûteuses, ou rendre une classe uniquement déplaçable.

##### Exemple, mauvais  

```    
    struct M2 {   // mauvais : ensemble incomplet d’opérations copie/déplacement/destructeur
    public:
        // …
        // … aucune opération copie ou déplacement …
        ~M2() { delete[] rep; }
    private:
        pair<int, int>* rep;  // ensemble de paires terminé par zéro
    };

    void use()
    {
        M2 x;
        M2 y;
        // …
        x = y;   // affectation par défaut
        // …
    }
```  

Étant donné qu’une attention particulière était nécessaire pour le destructeur (ici, pour désallouer), la probabilité que les opérateurs de copie et de déplacement implicites soient corrects est faible (ici on aurait une double suppression).

##### Remarque  

C’est ce qu’on appelle « la règle des cinq ».

##### Remarque  

Si vous voulez une implémentation par défaut (*tout en définissant une autre*), écrivez `=default` pour montrer que vous le faites intentionnellement pour cette fonction. Si vous ne voulez pas d’une fonction générée par défaut, supprimez‑la avec `=delete`.

##### Exemple, bon  

Lorsque le destructeur doit être déclaré uniquement pour le rendre `virtual`, il peut être défini comme par défaut.

```    
    class AbstractBase {
    public:
        virtual void foo() = 0;  // au moins une méthode abstraite pour rendre la classe abstraite
        virtual ~AbstractBase() = default;
        // …
    };
```  

Pour empêcher le tranchage tel que décrit dans [C.67](007-class.md#rc-copy-virtual) :

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
        // … autres constructeurs et fonctions …
    };
```  

Définir uniquement les opérations de déplacement ou uniquement les opérations de copie aurait le même effet ici, mais énoncer explicitement l’intention pour chaque fonction spéciale la rend plus évidente pour le lecteur.

##### Remarque  

Les compilateurs imposent une grande partie de cette règle et, idéalement, avertissent de toute violation.

##### Remarque  

S’appuyer sur une opération de copie implicite dans une classe possédant un destructeur est obsolète.

##### Remarque  

Écrire ces fonctions peut être source d’erreurs. Faites attention à leurs types d’argument :

```    
    class X {
    public:
        // …
        virtual ~X() = default;               // destructeur (virtual si X est censé être une classe de base)
        X(const X&) = default;                // constructeur de copie
        X& operator=(const X&) = default;     // opérateur d’affectation copie
        X(X&&) noexcept = default;              // constructeur de déplacement
        X& operator=(X&&) noexcept = default; // opérateur d’affectation déplacement
    };
```  

Une petite erreur (orthographe, omission d’un `const`, utilisation de `&` au lieu de `&&`, ou omission d’une fonction spéciale) peut entraîner des erreurs ou des avertissements. Pour éviter la fastidiosité et le risque d’erreur, essayez de suivre la [règle du zéro](007-class.md#rc-zero) @TODO-LINK.

##### Application  

(Un) classe devrait avoir une déclaration (même `=delete`) pour soit toutes, soit aucune des fonctions copie/déplacement/destructeur.

### <a name="rc-matched"></a>C.22 : Rendre les opérations par défaut cohérentes

##### Raison  

Les opérations par défaut forment conceptuellement un ensemble assorti. Leurs sémantiques sont inter‑liées.  
Les utilisateurs seront surpris si la construction/copieur et l’affectation/copieur font logiquement autre chose. Les utilisateurs seront surpris si les constructeurs et destructeurs n’offrent pas une vue cohérente de la gestion des ressources. Les utilisateurs seront surpris si copie et déplacement ne reflètent pas la façon dont les constructeurs et destructeurs fonctionnent.

##### Exemple, mauvais  

```    
    class Silly {   // MAUVAIS : opérations de copie incohérentes
        class Impl {
            // …
        };
        shared_ptr< Impl > p;
    public:
        Silly(const Silly& a) : p(make_shared<Impl>()) { *p = *a.p; }   // copie profonde
        Silly& operator=(const Silly& a) { p = a.p; return *this; }   // copie superficielle
        // …
    };
```  

Ces opérations ne sont pas d’accord sur la sémantique de copie. Cela conduira à de la confusion et des bugs.

##### Application  

* (Complexe) Un constructeur/copieur et l’opérateur d’affectation correspondant devraient écrire les mêmes membres de données au même niveau de déréférencement.  
* (Complexe) Tout membre de données écrit dans un constructeur/copieur doit également être initialisé par tous les autres constructeurs.  
* (Complexe) Si un constructeur/copieur effectue une copie profonde d’un membre de données, le destructeur doit modifier ce membre de données.  
* (Complexe) Si un destructeur modifie un membre de données, ce membre doit être écrit dans tout constructeur/copieur ou opérateur d’affectation.

---

## <a name="ss-dtor"></a>C.dtor : Destructeurs

« Cette classe a‑t‑elle besoin d’un destructeur ? » est une question de conception étonnamment perspicace.  
Pour la plupart des classes la réponse est « non », soit parce que la classe ne détient aucune ressource, soit parce que la destruction est gérée par la [règle du zéro](007-class.md#rc-zero) : ses membres se chargent d’eux‑mêmes. Si la réponse est « oui », une grande partie de la conception de la classe suit (voir [la règle des cinq](007-class.md#rc-five) @TODO-LINK).

### <a name="rc-dtor"></a>C.30 : Définir un destructeur si une classe a besoin d’une action explicite à la destruction de l’objet

##### Raison  

Un destructeur est invoqué implicitement à la fin de la durée de vie d’un objet.  
Si le destructeur par défaut suffit, utilisez‑le.  
Ne définissez un destructeur non‑par défaut que si une classe doit exécuter du code qui n’est pas déjà présent dans les destructeurs de ses membres.

##### Exemple  

```    
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
        auto act = finally([] { cout << "Exit test\n"; });  // établir l’action à la sortie
        // …
        if (something) return;   // act exécuté ici
        // …
    } // act exécuté ici
```  

Le but de `final_action` est d’obtenir l’exécution d’un fragment de code (généralement un lambda) lors de la destruction.

##### Remarque  

Il existe deux grandes catégories de classes qui ont besoin d’un destructeur défini par l’utilisateur :

* Une classe possédant une ressource qui n’est pas déjà représentée comme une classe avec un destructeur, par ex. un `vector` ou une classe transaction.
* Une classe qui existe principalement pour exécuter une action à la destruction, comme un traceur ou `final_action`.

##### Exemple, mauvais  

```    
    class Foo {   // mauvais ; utilisez le destructeur par défaut
    public:
        // …
        ~Foo() { s = ""; i = 0; vi.clear(); }  // nettoyage
    private:
        string s;
        int i;
        vector<int> vi;
    };
```  

Le destructeur par défaut le fait mieux, plus efficacement, et ne peut pas se tromper.

##### Application  

Rechercher des « ressources implicites » probables, telles que des pointeurs et références. Rechercher des classes avec des destructeurs même si tous leurs membres de données ont des destructeurs.

### <a name="rc-dtor-release"></a>C.31 : Toutes les ressources acquises par une classe doivent être libérées par le destructeur de la classe

##### Raison  

Prévention des fuites de ressources, notamment en cas d’erreur.

##### Remarque  

Pour les ressources représentées comme des classes disposant d’un ensemble complet d’opérations par défaut, cela se produit automatiquement.

##### Exemple  

```    
    class X {
        ifstream f;   // pourrait posséder un fichier
        // … pas d’opérations par défaut définies ou =deleted …
    };
```  

Le `ifstream` de `X` ferme implicitement tout fichier qu’il aurait pu ouvrir à la destruction de `X`.

##### Exemple, mauvais  

```    
    class X2 {     // mauvais
        FILE* f;   // pourrait posséder un fichier
        // … pas d’opérations par défaut définies ou =deleted …
    };
```  

`X2` pourrait laisser une poignée de fichier ouverte.

##### Remarque  

Et le cas d’une socket qui ne se ferme pas ? Un destructeur, `close`, ou une opération de nettoyage **ne doit jamais échouer** ([C.36](007-class.md#rc-dtor-fail) @TODO-LINK). S’il échoue malgré tout, nous sommes face à un problème sans vraie solution. Le concepteur d’un destructeur ne sait pas pourquoi le destructeur est appelé et ne peut « refuser d’agir » en lançant une exception. Voir la [discussion](028-discussion.md#sd-never-fail) @TODO-LINK. Pour aggraver les choses, de nombreuses opérations « fermer/libérer » ne sont pas ré‑essayables. Beaucoup ont essayé de résoudre ce problème, mais aucune solution générale n’est connue. Si possible, considérez une défaillance de fermeture/libération comme une erreur de conception fondamentale et terminez le programme.

##### Remarque  

Une classe peut contenir des pointeurs et références vers des objets qu’elle ne possède pas. Evidemment, ces objets ne doivent **pas** être `delete`d par le destructeur de la classe. Par exemple :

```    
    Preprocessor pp { /* … */ };
    Parser p { pp, /* … */ };
    Type_checker tc { p, /* … */ };
```  

Ici `p` fait référence à `pp` mais ne le possède pas.

##### Application  

* (Simple) Si une classe possède des membres pointeur ou référence qui sont propriétaires (par ex. désignés par `gsl::owner`), ces membres doivent être mentionnés dans son destructeur.  
* (Difficile) Déterminer si les membres pointeur ou référence sont propriétaires lorsqu’il n’existe aucune indication explicite de propriété (par ex. examiner les constructeurs).

### <a name="rc-dtor-ptr"></a>C.32 : Si une classe possède un pointeur brut (`T*`) ou une référence (`T&`), se demander si elle peut être propriétaire

##### Raison  

Il existe beaucoup de code qui ne spécifie pas clairement la propriété.

##### Exemple  

```    
    class legacy_class
    {
        foo* m_owning;   // MAUVAIS : passer à unique_ptr<T> ou owner<T*>
        bar* m_observer; // OK : conserver
    }
```  

La seule façon de déterminer la propriété peut être l’analyse du code.

##### Remarque  

La propriété doit être claire dans le nouveau code (et le code refactorisé) selon [R.20](009-resource.md#rr-owner) pour les pointeurs propriétaires et [R.3](009-resource.md#rr-ptr) pour les pointeurs non‑propriétaires. Les références ne doivent jamais être propriétaires [R.4](009-resource.md#rr-ref).

##### Application  

Examiner l’initialisation des pointeurs bruts membres et des références membres et voir si une allocation est utilisée.

### <a name="rc-dtor-ptr2"></a>C.33 : Si une classe possède un pointeur propriétaire, définir un destructeur

##### Raison  

Un objet possédé doit être `delete`d à la destruction de l’objet qui le possède.

##### Exemple  

Un pointeur membre peut représenter une ressource.  
[Un `T*` ne devrait pas le faire](009-resource.md#rr-ptr) ; cependant, dans le code hérité c’est assez fréquent. Considérez un `T*` comme un possible propriétaire et soupçonnez‑le.

```    
    template<typename T>
    class Smart_ptr {
        T* p;   // MAUVAIS : vague quant à la propriété de *p
        // …
    public:
        // … pas d’opérations par défaut définies …
    };
```  

```    
    void use(Smart_ptr<int> p1)
    {
        // erreur : p2.p fuit (si non nullptr et non possédé par un autre code)
        auto p2 = p1;
    }
```  

Notez que si vous définissez un destructeur, vous devez définir ou supprimer [toutes les opérations par défaut](007-class.md#rc-five) :

```    
    template<typename T>
    class Smart_ptr2 {
        T* p;   // MAUVAIS : vague quant à la propriété de *p
        // …
    public:
        // … aucun constructeur/copieur/déplaceur défini …
        ~Smart_ptr2() { delete p; }  // p est un propriétaire !
    };
```  

```    
    void use(Smart_ptr2<int> p1)
    {
        auto p2 = p1;   // erreur : double suppression
    }
```  

Le constructeur de copie copiera simplement `p1.p` dans `p2.p`, ce qui entraînera une double destruction de `p1.p`. Soyez explicite quant à la propriété :

```    
    template<typename T>
    class Smart_ptr3 {
        owner<T*> p;   // OK : explicite quant à la propriété de *p
        // …
    public:
        // …
        // … opérations de copie et déplacement …
        ~Smart_ptr3() { delete p; }
    };
```  

```    
    void use(Smart_ptr3<int> p1)
    {
        auto p2 = p1;   // OK : pas de double suppression
    }
```  

##### Remarque  

Le moyen le plus simple d’obtenir un destructeur est de remplacer le pointeur par un pointeur intelligent (par ex. `std::unique_ptr`) et laisser le compilateur s’occuper de la destruction appropriée de façon implicite.

##### Remarque  

Pourquoi ne pas exiger que tous les pointeurs propriétaires soient des « pointeurs intelligents » ? Cela impliquerait parfois des changements de code non triviaux et pourrait affecter les ABI.

##### Application  

* Une classe avec un membre pointeur de données est suspecte.  
* Une classe avec `owner<T>` devrait définir ses opérations par défaut.

### <a name="rc-dtor-virtual"></a>C.35 : Le destructeur d’une classe de base doit être soit public et virtuel, soit protégé et non‑virtuel

##### Raison  

Prévenir un comportement indéfini.  
Si le destructeur est public, le code appelant peut essayer de détruire un objet dérivé via un pointeur de base, et le résultat est indéfini si le destructeur de la classe de base n’est pas virtuel.  
Si le destructeur est protégé, le code appelant ne peut pas détruire via un pointeur de base et le destructeur n’a pas besoin d’être virtuel ; il doit être protégé, pas privé, afin que les destructeurs dérivés puissent l’invoquer.  
En général, l’auteur d’une classe de base ne connaît pas l’action appropriée à réaliser à la destruction.

##### Discussion  

Voir [cette partie dans la section Discussion](028-discussion.md#sd-dtor) @TODO-LINK.

##### Exemple, mauvais  

```    
    struct Base {  // MAUVAIS : possède implicitement un destructeur public non‑virtuel
        virtual void f();
    };

    struct D : Base {
        string s {"a resource needing cleanup"};
        ~D() { /* … nettoyage … */ }
        // …
    };

    void use()
    {
        unique_ptr<Base> p = make_unique<D>();
        // …
    } // la destruction de p appelle ~Base(), pas ~D(), ce qui fuit s et éventuellement plus
```  

##### Remarque  

Une fonction virtuelle définit une interface pour les classes dérivées qui peut être utilisée sans regarder les classes dérivées. Si l’interface autorise la destruction, elle doit être sûre à faire.

##### Remarque  

Un destructeur doit être non‑privé sinon il empêche l’utilisation du type :

```    
    class X {
        ~X();   // destructeur privé
        // …
    };

    void use()
    {
        X a;                        // erreur : impossible de détruire
        auto p = make_unique<X>();  // erreur : impossible de détruire
    }
```  

##### Exception  

On peut imaginer un cas où l’on souhaiterait un destructeur virtuel protégé : lorsqu’un objet d’un type dérivé (et uniquement d’un tel type) doit être autorisé à détruire *un autre* objet (pas lui‑même) via un pointeur vers la base. Nous n’avons pas vu de tel cas en pratique.

##### Application  

* Une classe comportant des fonctions virtuelles doit avoir un destructeur qui soit public et virtuel ou bien protégé et non‑virtuel.  
* Si une classe dérive publiquement d’une classe de base, la classe de base doit respecter la même règle de destructeur.

### <a name="rc-dtor-fail"></a>C.36 : Un destructeur ne doit pas échouer

##### Raison  

En général nous ne savons pas comment écrire un code à l’épreuve des erreurs si le destructeur peut échouer. La bibliothèque standard exige que toutes les classes qu’elle manipule possèdent des destructeurs qui ne terminent pas en lançant une exception.

##### Exemple  

```    
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
```  

##### Remarque  

De nombreuses tentatives ont été faites pour proposer un schéma à l’épreuve des erreurs pour les destructeurs. Aucun n’a réussi à fournir une solution générale. Cela peut être un problème pratique réel : par ex. qu’en est‑il d’une socket qui ne se ferme pas ? Le concepteur d’un destructeur ne sait pas pourquoi il est appelé et ne peut « refuser d’agir » en lançant une exception. Voir la [discussion](028-discussion.md#sd-never-fail) @TODO-LINK. Pour aggraver les choses, de nombreuses opérations de « fermeture/libération » ne sont pas ré‑essayables. Si cela est possible, considérez une défaillance de fermeture/clean‑up comme une erreur de conception fondamentale et terminez le programme.

##### Remarque  

Déclarez le destructeur `noexcept`. Cela garantira soit qu’il se termine normalement, soit qu’il termine le programme.

##### Remarque  

Si une ressource ne peut pas être libérée et que le programme ne doit pas échouer, essayez de signaler l’échec au reste du système d’une façon quelconque (peut‑être même en modifiant un état global et espérer que quelque chose le remarquera et pourra s’en occuper). Soyez pleinement conscient que cette technique est spéciale et sujette à erreur. Considérez le « ma connexion ne se ferme pas » : il y a probablement un problème de l’autre côté de la connexion et seul un morceau de code responsable des deux extrémités pourra le gérer correctement. Le destructeur pourrait envoyer un message (d’une façon ou d’une autre) à la partie responsable du système, considérer la connexion comme fermée, puis retourner normalement.

##### Remarque  

Si un destructeur utilise des opérations qui pourraient échouer, il peut attraper les exceptions et, dans certains cas, tout de même terminer avec succès (par ex. en recourant à un mécanisme de nettoyage différent de celui qui a levé l’exception).

##### Application  

(Simple) Un destructeur devrait être déclaré `noexcept` s’il pourrait lancer une exception.

### <a name="rc-dtor-noexcept"></a>C.37 : Rendre les destructeurs `noexcept`

##### Raison  

[Un destructeur ne doit pas échouer](007-class.md#rc-dtor-fail) @TODO-LINK. Si un destructeur essaie de sortir avec une exception, c’est une mauvaise conception et le programme devrait se terminer.

##### Remarque  

Un destructeur (qu’il soit défini par l’utilisateur ou généré par le compilateur) est implicitement déclaré `noexcept` (indépendamment du code présent dans son corps) si tous les membres de sa classe ont des destructeurs `noexcept`. En le déclarant explicitement `noexcept`, l’auteur se protège contre le fait que le destructeur devienne implicitement `noexcept(false)` suite à l’ajout ou à la modification d’un membre de la classe.

##### Exemple  

Tous les destructeurs ne sont pas `noexcept` par défaut ; un membre avec un destructeur qui lance rend toute la hiérarchie `noexcept(false)`.

```    
    struct X {
        Details x;  // possède un destructeur qui lance
        // …
        ~X() { }    // implicitement noexcept(false) ; peut lancer
    };
```  

Donc, en cas de doute, déclarez le destructeur `noexcept`.

##### Remarque  

Pourquoi ne pas déclarer alors tous les destructeurs `noexcept` ? Parce que cela introduirait souvent du bruit inutile, surtout dans les cas simples.

##### Application  

(Simple) Un destructeur doit être déclaré `noexcept` s’il peut lancer.

---

## <a name="ss-ctor"></a>C.ctor : Constructeurs

Un constructeur définit comment un objet est initialisé (construit).

### <a name="rc-ctor"></a>C.40 : Définir un constructeur si une classe possède une invariant

##### Raison  

C’est le rôle des constructeurs.

##### Exemple  

```    
    class Date {  // une Date représente une date valide
                  // dans l’intervalle du 1 janv. 1900 au 31 déc. 2100
        Date(int dd, int mm, int yy)
            :d{dd}, m{mm}, y{yy}
        {
            if (!is_valid(d, m, y)) throw Bad_date{};  // appliquer l’invariant
        }
        // …
    private:
        int d, m, y;
    };
```  

Il est souvent utile d’exprimer l’invariant comme un `Ensures` sur le constructeur.

##### Remarque  

Un constructeur peut être utilisé à des fins de commodité même si une classe ne possède pas d’invariant. Par exemple :

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

##### Remarque  

La règle C++11 d’initialisation de liste élimine le besoin de nombreux constructeurs. Par exemple :

```    
    struct Rec2{
        string s;
        int i;
        Rec2(const string& ss, int ii = 0) :s{ss}, i{ii} {}   // redondant
    };

    Rec2 r1 {"Foo", 7};
    Rec2 r2 {"Bar"};
```  

Le constructeur de `Rec2` est redondant. De plus, la valeur par défaut pour `int` serait mieux exprimée comme un [initialiseur de membre par défaut](007-class.md#rc-in-class-initializer) @TODO-LINK.

**Voir aussi** : [construire un objet valide](007-class.md#rc-complete) @TODO-LINK et [constructeur qui lance](007-class.md#rc-throw) @TODO-LINK.

##### Application  

* Signaler les classes avec des opérations de copie définies par l’utilisateur mais sans constructeur (une opération de copie indique souvent la présence d’une invariant).

### <a name="rc-complete"></a>C.41 : Un constructeur doit créer un objet entièrement initialisé

##### Raison  

Un constructeur établit l’invariant d’une classe. Un utilisateur de la classe doit pouvoir supposer qu’un objet construit est utilisable.

##### Exemple, mauvais  

```    
    class X1 {
        FILE* f;   // appeler init() avant toute autre fonction
        // …
    public:
        X1() {}
        void init();   // initialiser f
        void read();   // lire depuis f
        // …
    };

    void f()
    {
        X1 file;
        file.read();   // crash ou mauvaise lecture !
        // …
        file.init();   // trop tard
        // …
    }
```  

Les compilateurs ne lisent pas les commentaires.

##### Exception  

Si un objet valide ne peut pas être construit commodément par un constructeur, [utilisez une fonction fabrique](007-class.md#rc-factory) @TODO-LINK.

##### Application  

* (Simple) Chaque constructeur doit initialiser chaque membre de données (soit explicitement, via un constructeur délégant, soit via une construction par défaut).  
* (Inconnu) Si un constructeur possède un contrat `Ensures`, essayer de vérifier qu’il tient en post‑condition.

##### Remarque  

Si un constructeur acquiert une ressource (pour créer un objet valide), cette ressource doit être [libérée par le destructeur](007-class.md#rc-dtor-release) @TODO-LINK. L’idiome consistant à acquérir des ressources dans le constructeur et à les libérer dans le destructeur s’appelle [RAII](009-resource.md#rr-raii) (« Resource Acquisition Is Initialization »).

### <a name="rc-throw"></a>C.42 : Si un constructeur ne peut pas construire un objet valide, lancer une exception

##### Raison  

Laisser un objet invalide derrière soi crée des problèmes.

##### Exemple  

```    
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
        X2 file {"Zeno"}; // lance si le fichier n’est pas ouvert
        file.read();      // sûr
        // …
    }
```  

##### Exemple, mauvais  

```    
    class X3 {     // mauvais : le constructeur laisse un objet non valide derrière lui
        FILE* f;   // appeler is_valid() avant toute autre fonction
        bool valid;
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
        file.read();   // crash ou mauvaise lecture !
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
```  

##### Remarque  

Pour une définition de variable (par ex. sur la pile ou comme membre d’un autre objet) il n’existe pas d’appel de fonction explicite d’où l’on pourrait renvoyer un code d’erreur. Laisser un objet invalide et obliger les utilisateurs à vérifier systématiquement une fonction `is_valid()` avant chaque utilisation est fastidieux, source d’erreurs et inefficace.

##### Exception  

Dans certains domaines, comme certains systèmes temps réel stricts (ex. contrôle avionique), où la gestion d’exceptions n’est pas assez prévisible, la technique `is_valid()` doit être utilisée. Dans ce cas, vérifiez `is_valid()` de façon cohérente et immédiate afin de simuler [RAII](009-resource.md#rr-raii).

##### Alternative  

Si vous êtes tenté d’utiliser une idiome « initialisation post‑constructeur » ou « initialisation en deux étapes », essayez de ne pas le faire. Si vous devez vraiment le faire, envisagez les [fonctions fabriques](007-class.md#rc-factory) @TODO-LINK.

##### Remarque  

Une des raisons pour lesquelles les gens utilisent des fonctions `init()` plutôt que de placer le travail d’initialisation dans le constructeur est d’éviter la duplication de code. Les [constructeurs délégants](007-class.md#rc-delegating) et les [initialiseurs de membres par défaut](007-class.md#rc-in-class-initializer) le font mieux. Une autre raison a été de retarder l’initialisation jusqu’à ce que l’objet soit réellement nécessaire ; la solution consiste souvent à [ne pas déclarer de variable tant qu’elle ne peut pas être correctement initialisée](010-expr.md#res-init).

##### Application  

???

### <a name="rc-default0"></a>C.43 : S’assurer qu’une classe copiable possède un constructeur par défaut

##### Raison  

Assurez‑vous que, si une classe concrète est copiable, elle satisfait aussi le reste du concept « semiregular ».  

De nombreuses fonctions et bibliothèques exigent un constructeur par défaut pour initialiser leurs éléments, p. ex. `T a[10]` et `std::vector<T> v(10)`. Un constructeur par défaut simplifie souvent la tâche de définir un état « déplacé‑from » (voir #???).  

##### Exemple  

```    
    class Date { // MAUVAIS : pas de constructeur par défaut
    public:
        Date(int dd, int mm, int yyyy);
        // …
    };

    vector<Date> vd1(1000);   // besoin d’un constructeur par défaut ici
    vector<Date> vd2(1000, Date{7, Month::October, 1885});   // alternative
```  

Le constructeur par défaut n’est généré que s’il n’existe aucun constructeur déclaré par l’utilisateur, donc il est impossible d’initialiser le vecteur `vd1` dans l’exemple ci‑dessus. L’absence d’une valeur par défaut peut surprendre les utilisateurs et compliquer son utilisation ; si l’on peut raisonnablement en définir une, il faut le faire.

`Date` incite à réfléchir : il n’existe pas de « date par défaut naturelle » (le Big Bang est trop lointain pour la plupart des usages). `{0,0,0}` n’est pas une date valide dans la plupart des calendriers, c’est donc comparable à `NaN` des flottants. Cependant, la plupart des implémentations de `Date` possèdent une « première date » (par ex. le 1 janv. 1970), donc choisir cela comme valeur par défaut est habituel.

```    
    class Date {
    public:
        Date(int dd, int mm, int yyyy);
        Date() = default; // [Voir aussi](007-class.md#rc-default) @TODO-LINK
        // …
    private:
        int dd {1};
        int mm {1};
        int yyyy {1970};
        // …
    };

    vector<Date> vd1(1000);
```  

##### Remarque  

Une classe dont tous les membres possèdent des constructeurs par défaut obtient implicitement un constructeur par défaut :

```    
    struct X {
        string s;
        vector<int> v;
    };

    X x; // équivaut à X{ { }, { } }; c’est‑à‑dire une chaîne vide et un vecteur vide
```  

Attention : les types intégrés ne sont pas correctement initialisés par défaut :

```    
    struct X {
        string s;
        int i;
    };

    void f()
    {
        X x;    // x.s est initialisée à la chaîne vide ; x.i n’est pas initialisé

        cout << x.s << ' ' << x.i << '\n';
        ++x.i;
    }
```  

Les objets statiquement alloués de type intégré sont initialisés à `0` par défaut, mais les variables locales d’un type intégré ne le sont pas. Certains compilateurs peuvent initialiser les variables locales, alors qu’une construction optimisée ne le fera pas. Ainsi, le code ci‑dessus peut sembler fonctionner, mais il repose sur un comportement indéfini. Si vous voulez une initialisation, vous pouvez fournir explicitement une initialisation par défaut :

```    
    struct X {
        string s;
        int i {};   // initialisation par défaut (à 0)
    };
```  

##### Remarques  

* Les classes qui n’ont pas de construction par défaut raisonnable ne sont généralement pas copiables, donc elles ne tombent pas sous cette directive.  
* Par exemple, une classe de base abstraite ne devrait pas être copiable, et n’a donc pas forcément besoin d’un constructeur par défaut :

```    
    // Shape est une classe de base abstraite, pas un type copiable.
    // Elle peut ou non avoir besoin d’un constructeur par défaut.
    struct Shape {
        virtual void draw() = 0;
        virtual void rotate(int) = 0;
        // =delete copy/move functions
        // …
    };
```  

* Une classe qui doit acquérir une ressource fournie par l’appelant lors de la construction ne peut souvent pas posséder de constructeur par défaut, mais elle ne tombe pas sous cette directive car ce type n’est généralement pas copiable :

```    
    // std::lock_guard n’est pas copiable.
    // Il n’a pas de constructeur par défaut.
    lock_guard g {mx};  // protéger le mutex mx
    lock_guard g2;      // erreur : aucun objet à protéger
```  

* Une classe qui possède un « état spécial » devant être géré séparément des autres états par des fonctions membres ou par l’utilisateur entraîne du travail supplémentaire (et très probablement davantage d’erreurs). Ce type peut naturellement utiliser cet état spécial comme valeur construite par défaut, qu’il soit copiable ou non :

```    
    // std::ofstream n’est pas copiable.
    // Il possède cependant un constructeur par défaut qui représente l’état « non ouvert ».
    ofstream out {"Foobar"};
    // …
    out << log(time, transaction);
```  

Les types de pointeur spécial copiable, comme les pointeurs intelligents copiable qui ont l’état spécial `==nullptr`, doivent utiliser cet état spécial comme valeur construite par défaut.

Cependant, il est préférable que le constructeur par défaut initialise à un état significatif tel que `""` pour `std::string` ou `{}` pour `std::vector`.

##### Application  

* Signaler les classes qui sont copiable par `=` sans posséder de constructeur par défaut.  
* Signaler les classes comparables avec `==` mais non copiable.

### <a name="rc-default00"></a>C.44 : Préférer que les constructeurs par défaut soient simples et ne lèvent pas d’exception

##### Raison  

Pouvoir placer un objet à « la valeur par défaut » sans opérations pouvant échouer simplifie la gestion d’erreurs et le raisonnement sur les opérations de déplacement.

##### Exemple, problématique  

```    
    template<typename T>
    // elem pointe vers un élément alloué avec new
    class Vector0 {
    public:
        Vector0() :Vector0{0} {}
        Vector0(int n) :elem{new T[n]}, space{elem + n}, last{elem} {}
        // …
    private:
        own<T*> elem;
        T* space;
        T* last;
    };
```  

C’est joli et général, mais initialiser un `Vector0` à vide après une erreur implique une allocation qui peut échouer. De plus, représenter un `Vector` vide comme `{new T[0], 0, 0}` semble gaspiller. Par exemple, `Vector0<int> v[100]` coûte 100 allocations.

##### Exemple  

```    
    template<typename T>
    // elem est nullptr ou pointe vers un élément alloué avec new
    class Vector1 {
    public:
        // représente {nullptr, nullptr, nullptr} ; ne lance pas d’exception
        Vector1() noexcept {}
        Vector1(int n) :elem{new T[n]}, space{elem + n}, last{elem} {}
        // …
    private:
        own<T*> elem {};
        T* space {};
        T* last {};
    };
```  

Utiliser `{nullptr, nullptr, nullptr}` rend `Vector1{}` peu coûteux, mais impose un cas spécial et implique des vérifications à l’exécution. Mettre `Vector1` à vide après la détection d’une erreur devient trivial.

##### Application  

* Signaler les constructeurs par défaut qui lancent des exceptions.

### <a name="rc-default"></a>C.45 : Ne pas définir de constructeur par défaut dont le seul rôle est d’initialiser les membres ; utiliser les initialiseurs de membres par défaut à la place

##### Raison  

Utiliser les initialiseurs de membres par défaut laisse le compilateur générer la fonction pour vous. La fonction générée par le compilateur peut être plus efficace.

##### Exemple, mauvais  

```    
    class X1 { // MAUVAIS : n’utilise pas les initialiseurs de membres
        string s;
        int i;
    public:
        X1() :s{"default"}, i{1} { }
        // …
    };
```  

##### Exemple  

```    
    class X2 {
        string s {"default"};
        int i {1};
    public:
        // utilise le constructeur par défaut généré par le compilateur
        // …
    };
```  

##### Application  

(Simple) Signaler si le constructeur par défaut possède des initialiseurs de membres qui sont des constantes, et recommander de les placer comme initialiseurs de données.

### <a name="rc-explicit"></a>C.46 : Déclarer `explicit` les constructeurs à un seul argument par défaut

##### Raison  

Éviter les conversions implicites non intentionnées.

##### Exemple, mauvais  

```    
    class String {
    public:
        String(int);   // MAUVAIS
        // …
    };

    String s = 10;   // surprise : chaîne de taille 10
```  

##### Exception  

Si vous voulez réellement une conversion implicite de l’argument du constructeur vers le type de classe, ne mettez pas `explicit` :

```    
    class Complex {
    public:
        Complex(double d);   // OK : on veut une conversion de d en {d,0}
        // …
    };

    Complex z = 10.7;   // conversion non surprenante
```  

**Voir aussi** : [Discussion sur les conversions implicites](007-class.md#ro-conversion) @TODO-LINK.

##### Remarque  

Les constructeurs de copie et de déplacement ne doivent pas être `explicit` car ils ne font pas de conversion. Un constructeur de copie/exemple `explicit` complique le passage et le retour par valeur.

##### Application  

(Simple) Les constructeurs à un argument doivent être déclarés `explicit`. Les constructeurs à un argument non‑`explicit` sont rares dans la plupart des bases de code. Avertir pour tous ceux qui ne figurent pas sur une « liste positive ».

### <a name="rc-order"></a>C.47 : Définir et initialiser les membres de données dans l’ordre de leur déclaration

##### Raison  

Réduire la confusion et les erreurs. C’est l’ordre réel d’initialisation (indépendant de l’ordre des initialiseurs de membres).

##### Exemple, mauvais  

```    
    class Foo {
        int m1;
        int m2;
    public:
        Foo(int x) :m2{x}, m1{++x} { }   // MAUVAIS : ordre d’initialisation trompeur
        // …
    };

    Foo x(1); // surprise : x.m1 == x.m2 == 2
```  

##### Application  

(Simple) Une liste d’initialisation de membres doit mentionner les membres dans le même ordre que leur déclaration.

**Voir aussi** : [Discussion](028-discussion.md#sd-order) @TODO-LINK.

### <a name="rc-in-class-initializer"></a>C.48 : Préférer les initialiseurs de membres par défaut aux initialiseurs de membres dans les constructeurs pour les initialiseurs constants

##### Raison  

Rendre explicite que la même valeur est attendue dans tous les constructeurs. Éviter la redondance. Éviter les problèmes de maintenance. Cela conduit au code le plus court et le plus efficace.

##### Exemple, mauvais  

```    
    class X {   // MAUVAIS
        int i;
        string s;
        int j;
    public:
        X() :i{666}, s{"qqq"} { }   // j n’est pas initialisé
        X(int ii) :i{ii} {}         // s vaut "" et j n’est pas initialisé
        // …
    };
```  

Comment le mainteneur saurait‑il si `j` était délibérément non initialisé (probablement une mauvaise idée) et si `s` devait valoir `""` dans un constructeur et `qqq` dans l’autre (presque certainement une erreur) ? Le problème avec `j` (oublier d’initialiser un membre) survient souvent lorsqu’un nouveau membre est ajouté à une classe existante.

##### Exemple  

```    
    class X2 {
        int i {666};
        string s {"qqq"};
        int j {numeric_limits<int>::min()};
    public:
        X2() = default;        // tous les membres sont initialisés à leurs valeurs par défaut
        X2(int ii) :i{ii} {}   // s et j restent à leurs valeurs par défaut
        // …
    };
```  

**Alternative** : On peut obtenir une partie des bénéfices avec des arguments par défaut aux constructeurs, mais cela est moins explicite, engendre un surcoût de passage d’arguments, et devient répétitif lorsqu’il y a plusieurs constructeurs :

```    
    class X3 {   // MAUVAIS : non explicite, surcharge d’arguments
        int i;
        string s;
        int j;
    public:
        X3(int ii = 666, const string& ss = "qqq", int jj = numeric_limits<int>::min())
            :i{ii}, s{ss}, j{jj} { }   // tous les membres sont initialisés à leurs valeurs par défaut
        // …
    };
```  

##### Application  

* (Simple) Chaque constructeur doit initialiser chaque membre de données (soit explicitement, via un appel délégué, ou via construction par défaut).  
* (Simple) Des arguments par défaut aux constructeurs suggèrent qu’un initialiseur de membre par défaut serait plus approprié.

### <a name="rc-initialize"></a>C.49 : Préférer l’initialisation à l’affectation dans les constructeurs

##### Raison  

L’initialisation indique explicitement que l’on initialise (plutôt qu’assigner) et peut être plus élégante et efficace. Évite les erreurs « utiliser avant de définir ».

##### Exemple, bon  

```    
    class A {   // Bon
        string s1;
    public:
        A(const char* p) : s1{p} { }    // BON : construction directe (et le C‑string est nommé explicitement)
        // …
    };
```  

##### Exemple, mauvais  

```    
    class B {   // MAUVAIS
        string s1;
    public:
        B(const char* p) { s1 = p; }   // MAUVAIS : constructeur par défaut suivi d’une affectation
        // …
    };

    class C {   // AFFREUX, c’est‑à‑dire très mauvais
        int* p;
    public:
        C() { cout << *p; p = new int{10}; }   // utilisation accidentelle avant l’initialisation
        // …
    };
```  

##### Exemple, encore meilleur  

Au lieu de ces `const char*` nous pourrions utiliser `std::string_view` (C++17) ou `gsl::span<char>` comme [moyen plus général de présenter des arguments à une fonction](018-stdlib.md#rstr-view) :

```    
    class D {   // Bon
        string s1;
    public:
        D(string_view v) : s1{v} { }    // BON : construction directe
        // …
    };
```  

### <a name="rc-factory"></a>C.50 : Utiliser une fonction fabrique si vous avez besoin d’un « comportement virtuel » pendant l’initialisation

##### Raison  

Si l’état d’un objet de base doit dépendre de l’état de la partie dérivée de l’objet, il faut utiliser une fonction virtuelle (ou équivalente) tout en minimisant la fenêtre d’opportunité d’abuser d’un objet imparfaitement construit.

##### Remarque  

Le type de retour de la fabrique devrait normalement être `unique_ptr` par défaut ; si certains usages sont partagés, l’appelant peut `move` le `unique_ptr` dans un `shared_ptr`. Cependant, si le créateur connaît à l’avance que toutes les utilisations de l’objet retourné seront partagées, retourner directement un `shared_ptr` et utiliser `make_shared` dans le corps permet d’économiser une allocation.

##### Exemple, mauvais  

```    
    class B {
    public:
        B()
        {
            /* … */
            f(); // MAUVAIS : C.82 : ne pas appeler de fonctions virtuelles dans les constructeurs et destructeurs
            /* … */
        }

        virtual void f() = 0;
    };
```  

##### Exemple  

```    
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
            { /* … */ f(); /* … */ } // BON : l’appel virtuel est sûr
    };

    class D : public B {                 // classe dérivée quelconque
    protected:
        class Token {};

    public:
        explicit D(Token) : B{ B::Token{} } {}
        void f() override { /* …  */ };

    protected:
        template<class T>
        friend shared_ptr<T> B::create();
    };

    shared_ptr<D> p = D::create<D>();  // création d’un objet D
```  

`make_shared` nécessite que le constructeur soit public. En exigeant un `Token` protégé, le constructeur ne peut plus être appelé publiquement, évitant ainsi qu’un objet imparfaitement construit ne s’échappe. En fournissant la fonction fabrique `create()`, nous rendons la construction (sur le tas) commode.

##### Remarque  

Les fonctions fabriques conventionnelles allouent sur le tas, plutôt que sur la pile ou dans un objet englobant.

**Voir aussi** : [Discussion](028-discussion.md#sd-factory) @TODO-LINK.

### <a name="rc-delegating"></a>C.51 : Utiliser les constructeurs délégants pour représenter les actions communes à tous les constructeurs d’une classe

##### Raison  

Éviter la duplication et les différences accidentelles.

##### Exemple, mauvais  

```    
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
```  

L’action commune devient fastidieuse à écrire et peut accidentellement ne pas être commune.

##### Exemple  

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
        // …
    };
```  

**Voir aussi** : Si l’action répétée est une simple initialisation, considérer [un initialiseur de membre par défaut](007-class.md#rc-in-class-initializer) @TODO-LINK.

##### Application  

(Modéré) Rechercher des corps de constructeurs similaires.

### <a name="rc-inheriting"></a>C.52 : Utiliser les constructeurs hérités pour importer les constructeurs dans une classe dérivée qui n’a pas besoin d’une initialisation explicite supplémentaire

##### Raison  

Si vous avez besoin de ces constructeurs pour une classe dérivée, les ré‑implémenter est fastidieux et source d’erreurs.

##### Exemple  

`std::vector` possède de nombreux constructeurs complexes, donc si je veux mon propre `vector`, je ne veux pas les ré‑implémenter :

```    
    class Rec {
        // … données et nombreux constructeurs sympas …
    };

    class Oper : public Rec {
        using Rec::Rec;
        // … aucune donnée supplémentaire …
        // … de nombreuses fonctions utilitaires …
    };
```  

##### Exemple, mauvais  

```    
    struct Rec2 : public Rec {
        int x;
        using Rec::Rec;
    };

    Rec2 r {"foo", 7};
    int val = r.x;   // non initialisé
```  

##### Application  

Veiller à ce que chaque membre de la classe dérivée soit initialisé.

---

## <a name="ss-copy"></a>C.copy : Copie et déplacement

Les types concrets devraient généralement être copiable, mais les interfaces d’une hiérarchie de classes ne le devraient pas. Les gestionnaires de ressources peuvent ou non être copiables. Les types peuvent être définis comme déplaçables pour des raisons logiques ainsi que de performance.

### <a name="rc-copy-assignment"></a>C.60 : Rendre l’affectation de copie non‑`virtual`, prendre le paramètre par `const&` et retourner par `non‑const&`

##### Raison  

C’est simple et efficace. Si vous voulez optimiser pour les r‑values, fournissez une surcharge qui prend un `&&` (voir [F.18](006-functions.md#rf-consume) @TODO-LINK).

##### Exemple  

```    
    class Foo {
    public:
        Foo& operator=(const Foo& x)
        {
            // BON : pas besoin de vérifier l’auto‑affectation (autre que performances)
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
```  

##### Remarque  

L’implémentation de `swap` offre la [garantie forte](032-bibliography.md#Abrahams01).

##### Exemple  

Mais que faire si vous pouvez obtenir un gain de performance significatif en n’effectuant pas de copie temporaire ? Considérez un `Vector` destiné à un domaine où l’affectation de gros `Vector`s de même taille est courante. Dans ce cas, la copie d’éléments impliquée par la technique `swap` pourrait augmenter le coût d’un ordre de grandeur :

```    
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
            // … utiliser la technique swap, cela ne peut pas être meilleur …
            return *this;
        }
        // … copier sz éléments de *a.elem vers elem …
        if (a.sz < sz) {
            // … détruire les éléments superflus dans *this et ajuster la taille …
        }
        return *this;
    }
```  

En écrivant directement dans les éléments cibles, nous n’obtenons que la [garantie de base](032-bibliography.md#Abrahams01) plutôt que la garantie forte offerte par la technique `swap`. Attention à l’[auto‑affectation](007-class.md#rc-copy-self).

**Alternatives** : Si vous pensez avoir besoin d’un opérateur d’affectation `virtual` et comprenez pourquoi c’est profondément problématique, ne l’appeler pas `operator=`. Faites‑en une fonction nommée, par ex. `virtual void assign(const Foo&)`. Voir [copy constructor vs `clone()`](007-class.md#rc-copy-virtual) @TODO-LINK.

##### Application  

* (Simple) Un opérateur d’affectation ne doit pas être `virtual`.  
* (Simple) Un opérateur d’affectation doit retourner `T&` pour permettre le chaînage, pas `const T&` qui gênerait la composabilité et l’insertion d’objets dans des conteneurs.  
* (Modéré) Un opérateur d’affectation doit (implicitement ou explicitement) invoquer tous les opérateurs d’affectation des bases et des membres. Examiner le destructeur pour déterminer si le type a une sémantique de pointeur ou de valeur.

### <a name="rc-copy-semantic"></a>C.61 : Une opération de copie doit copier

##### Raison  

C’est la sémantique généralement attendue. Après `x = y`, on s’attend à ce que `x == y`. Après une copie, `x` et `y` peuvent être des objets indépendants (sémantique de valeur, comme les types intégrés et les classes de la bibliothèque standard) ou référencer un même objet (sémantique de pointeur, comme les pointeurs).

##### Exemple  

```    
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
    if (x == y) throw Bad{};   // suppose une sémantique de valeur
```  

##### Exemple  

```    
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
    if (x != y) throw Bad{};  // suppose une sémantique de pointeur
```  

##### Remarque  

Préférez la sémantique de valeur sauf si vous construisez un « smart pointer ». La sémantique de valeur est la plus simple à raisonner et ce que les composants de la bibliothèque standard attendent.

##### Application  

(Not enforceable)

### <a name="rc-copy-self"></a>C.62 : Rendre l’affectation de copie sûre pour l’auto‑affectation

##### Raison  

Si `x = x` modifie la valeur de `x`, les gens seront surpris et des erreurs graves (souvent des fuites) peuvent survenir.

##### Exemple  

Les conteneurs de la bibliothèque standard gèrent élégamment l’auto‑affectation :

```    
    std::vector<int> v = {3, 1, 4, 1, 5, 9};
    v = v;
    // v vaut toujours {3, 1, 4, 1, 5, 9}
```  

##### Remarque  

L’affectation générée par défaut à partir de membres qui gèrent l’auto‑affectation le fait correctement.

```    
    struct Bar {
        vector<pair<int, int>> v;
        map<string, int> m;
        string s;
    };

    Bar b;
    // …
    b = b;   // correct et efficace
```  

##### Remarque  

Vous pouvez gérer l’auto‑affectation en testant explicitement, mais souvent il est plus rapide et plus élégant de s’en passer (par ex. en utilisant `swap`).

```    
    class Foo {
        string s;
        int i;
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
```  

C’est évidemment sûr et apparemment efficace. Mais si on a une auto‑affectation sur un million d’affectations, cela représente un million de tests redondants (le prédicteur de branche devine généralement correctement). Considérez :

```    
    Foo& Foo::operator=(const Foo& a)   // plus simple, probablement bien meilleur
    {
        s = a.s;
        i = a.i;
        return *this;
    }
```  

`std::string` gère l’auto‑affectation, tout comme `int`. Tout le coût est supporté par le cas rare d’auto‑affectation.

##### Application  

(Simple) Les opérateurs d’affectation ne devraient pas contenir le motif `if (this == &a) return *this;` ??? (peut‑être flaguer comme redondant).

### <a name="rc-move-assignment"></a>C.63 : Rendre l’affectation de déplacement non‑`virtual`, prendre le paramètre par `&&` et retourner par `non‑const&`

##### Raison  

C’est simple et efficace.

**Voir** : [la règle pour l’affectation copie](007-class.md#rc-copy-assignment) @TODO-LINK.

##### Application  

Identique à celle appliquée à [l’affectation copie](007-class.md#rc-copy-assignment) @TODO-LINK.

* (Simple) Un opérateur d’affectation ne doit pas être `virtual`.  
* (Simple) Un opérateur d’affectation doit retourner `T&` pour le chaînage, pas `const T&`.  
* (Modéré) Un opérateur d’affectation de déplacement doit (implicitement ou explicitement) invoquer tous les opérateurs d’affectation de déplacement des bases et des membres.

### <a name="rc-move-semantic"></a>C.64 : Une opération de déplacement doit déplacer et laisser sa source dans un état valide

##### Raison  

C’est la sémantique généralement attendue. Après `y = std::move(x)` la valeur de `y` doit être celle que `x` avait et `x` doit être dans un état valide.

##### Exemple  

```    
    class X {   // OK : sémantique de valeur
    public:
        X();
        X(X&& a) noexcept;  // déplacer X
        X& operator=(X&& a) noexcept; // affectation déplacement X
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
```  

##### Remarque  

Idéalement, l’objet déplacé‑from devrait être la valeur par défaut du type. Assurez‑vous que, sauf raison exceptionnelle, c’est ainsi. Cependant, tous les types n’ont pas de valeur par défaut et pour certains établir la valeur par défaut peut être coûteux. Le standard impose uniquement que l’objet déplacé‑from puisse être détruit. Souvent, on peut faire mieux : la bibliothèque standard suppose qu’il est possible d’assigner à un objet déplacé‑from. Toujours laisser l’objet déplacé‑from dans un état (nécessairement spécifié) valide.

##### Remarque  

À moins d’une raison exceptionnellement forte, `x = std::move(y); y = z;` devrait fonctionner avec les sémantiques conventionnelles.

##### Application  

(Not enforceable) Rechercher les assignations aux membres dans l’opération déplacement. Si le type possède un constructeur par défaut, comparer ces assignations aux initialisations du constructeur par défaut.

### <a name="rc-move-self"></a>C.65 : Rendre l’affectation de déplacement sûre pour l’auto‑affectation

##### Raison  

Si `x = x` change la valeur de `x`, les gens seront surpris et des erreurs sérieuses peuvent survenir. Bien que l’on n’écrive pas souvent directement une auto‑affectation qui se transforme en déplacement, cela peut arriver. De plus, `std::swap` est implémenté à l’aide d’opérations de déplacement ; si vous faites accidentellement `swap(a,b)` où `a` et `b` font référence au même objet, ne pas gérer l’auto‑déplacement peut être une erreur subtile et grave.

##### Exemple  

```    
    class Foo {
        string s;
        int i;
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
```  

L’argument contre `if (this == &a) return *this;` dans le cas d’auto‑déplacement est encore plus fort que celui de l’auto‑affectation copie.

##### Remarque  

Il n’existe pas de façon générale connue d’éviter le test `if (this == &a) return *this;` dans une affectation de déplacement tout en obtenant un résultat correct (c’est‑à‑dire que après `x = x` la valeur de `x` ne change pas).

##### Remarque  

La norme ISO garantit uniquement un état « valide mais non spécifié » pour les conteneurs de la bibliothèque standard. Apparemment cela n’a pas posé de problème pendant plus de dix ans d’utilisation expérimentale et en production. Contactez les éditeurs si vous trouvez un contre‑exemple. Cette règle est donc davantage une mesure de prudence qui insiste sur la sécurité totale.

##### Exemple  

Voici une façon de déplacer un pointeur sans test (imaginez‑le comme code dans l’implémentation d’une affectation de déplacement) :

```    
    // déplacer other.ptr vers this->ptr
    T* temp = other.ptr;
    other.ptr = nullptr;
    delete ptr; // en auto‑déplacement, this->ptr est aussi nullptr ; delete est un no‑op
    ptr = temp; // en auto‑déplacement, le pointeur original est restauré
```  

##### Application  

* (Modéré) En cas d’auto‑affectation, un opérateur d’affectation de déplacement ne doit pas laisser l’objet avec des pointeurs membres qui ont été `delete`d ou mis à `nullptr`.  
* (Not enforceable) Examiner l’usage des types de conteneur standard (incl. `string`) et les considérer comme sûrs pour les usages ordinaires (non critiques).

### <a name="rc-move-noexcept"></a>C.66 : Rendre les opérations de déplacement `noexcept`

##### Raison  

Une opération de déplacement qui lance une exception viole les attentes raisonnables de la plupart des gens. Une opération de déplacement qui ne lance pas d’exception sera utilisée plus efficacement par les bibliothèques et les facilités du langage.

##### Exemple  

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
        // …
    private:
        T* elem;
        int sz;
    };
```  

Ces opérations ne lancent pas d’exception.

##### Exemple, mauvais  

```    
    template<typename T>
    class Vector2 {
    public:
        Vector2(Vector2&& a) noexcept { *this = a; }             // utilise simplement la copie
        Vector2& operator=(Vector2&& a) noexcept { *this = a; }  // utilise simplement la copie
        // …
    private:
        T* elem;
        int sz;
    };
```  

`Vector2` n’est pas seulement inefficace, son opérateur de copie peut lancer une exception (allocation).

##### Application  

(Simple) Une opération de déplacement doit être marquée `noexcept`.

### <a name="rc-copy-virtual"></a>C.67 : Une classe polymorphe doit supprimer les copies publiques/mouvements

##### Raison  

Une *classe polymorphe* est une classe qui définit ou hérite d’au moins une fonction virtuelle. Il est probable qu’elle soit utilisée comme classe de base pour d’autres classes dérivées avec un comportement polymorphe. Si elle est accidentellement passée par valeur, avec le constructeur de copie et l’opérateur d’affectation générés implicitement, on risque le *slicing* : seule la partie base d’un objet dérivé sera copiée, corrompant le comportement polymorphe.

Si la classe n’a pas de données, `=delete` les fonctions copie/mouvement. Sinon, les rendre `protected`.

##### Exemple, mauvais  

```    
    class B { // MAUVAIS : classe de base polymorphe qui ne supprime pas la copie
    public:
        virtual char m() { return 'B'; }
        // … rien concernant les opérations copie, donc uses defaults …
    };

    class D : public B {
    public:
        char m() override { return 'D'; }
        // …
    };

    void f(B& b)
    {
        auto b2 = b; // oups, le slicing se produit ; b2.m() renverra 'B'
    }

    D d;
    f(d);
```  

##### Exemple  

```    
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
```  

##### Remarque  

Si vous avez besoin de créer des copies profondes d’objets polymorphes, utilisez des fonctions `clone()` : voir [C.130](007-class.md#rh-copy) @TODO-LINK.

##### Exception  

Les classes qui représentent des objets d’exception doivent à la fois être polymorphes et copy‑constructibles.

##### Application  

* Signaler une classe polymorphe avec une opération de copie publique.  
* Signaler une affectation d’objets de classe polymorphe.

---

## C.other : Autres règles relatives aux opérations par défaut

En plus des opérations pour lesquelles le langage propose des implémentations par défaut, il existe quelques opérations si fondamentales qu’il faut des règles spécifiques : comparaisons, `swap`, et `hash`.

### <a name="rc-eqdefault"></a>C.80 : Utiliser `=default` si vous devez être explicite sur l’utilisation de la sémantique par défaut

##### Raison  

Le compilateur a plus de chances d’obtenir correctement la sémantique par défaut et vous ne pouvez pas faire mieux que le compilateur.

##### Exemple  

```    
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
```  

Comme nous avons défini le destructeur, nous devons définir les opérations copy/move. `= default` est la meilleure et la plus simple manière de le faire.

##### Exemple, mauvais  

```    
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
```  

Écrire les corps des opérations copy/move est verbeux, fastidieux et propice aux erreurs. Le compilateur le fait mieux.

##### Application  

(Moderate) Le corps d’une opération définie par l’utilisateur ne doit pas reproduire les mêmes sémantiques que la version générée par le compilateur, sinon cela serait redondant.

### <a name="rc-delete"></a>C.81 : Utiliser `=delete` lorsqu’on veut désactiver le comportement par défaut (sans vouloir d’alternative)

##### Raison  

Dans quelques cas, une opération par défaut n’est pas souhaitable.

##### Exemple  

```    
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
```  

##### Exemple  

`unique_ptr` peut être déplacé mais pas copié. Pour cela, ses opérations de copie sont supprimées. Pour empêcher la copie, il faut `=delete` les opérations de copie des l‑values :

```    
    template<class T, class D = default_delete<T>> class unique_ptr {
    public:
        // …
        constexpr unique_ptr() noexcept;
        explicit unique_ptr(pointer p) noexcept;
        // …
        unique_ptr(unique_ptr&& u) noexcept;   // constructeur déplacement
        // …
        unique_ptr(const unique_ptr&) = delete; // désactiver la copie depuis une l‑value
        // …
    };

    unique_ptr<int> make();   // créer « quelque chose » et le retourner en le déplaçant

    void f()
    {
        unique_ptr<int> pi {};
        auto pi2 {pi};      // erreur : pas de constructeur déplacement depuis l‑value
        auto pi3 {make()};  // OK, déplacement : le résultat de make() est une r‑value
    }
```  

Notez que les fonctions supprimées doivent être publiques.

##### Application  

La suppression d’une opération par défaut dépend de la sémantique souhaitée pour la classe. Considérez ces classes comme suspectes, mais maintenez une « liste positive » des classes où un humain a affirmé que la sémantique était correcte.

### <a name="rc-ctor-virtual"></a>C.82 : Ne pas appeler de fonctions virtuelles dans les constructeurs et destructeurs

##### Raison  

La fonction appelée sera celle de l’objet construit jusqu’à présent, et non pas éventuellement une fonction surchargée dans une classe dérivée. Cela peut être très déroutant. Pire, un appel direct ou indirect à une fonction virtuelle pure depuis un constructeur ou destructeur entraîne un comportement indéfini.

##### Exemple, mauvais  

```    
    class Base {
    public:
        virtual void f() = 0;   // non implémentée
        virtual void g();       // implémentée avec version Base
        virtual void h();       // implémentée avec version Base
        virtual ~Base();        // implémentée avec version Base
    };

    class Derived : public Base {
    public:
        void g() override;   // fournir implémentation Derived
        void h() final;      // fournir implémentation Derived

        Derived()
        {
            // MAUVAIS : tentative d’appeler fonction virtuelle non implémentée
            f();

            // MAUVAIS : appelera Derived::g, pas de dispatch supplémentaire virtuel
            g();

            // BON : explicite, on veut appeler uniquement la version visible
            Derived::g();

            // ok, pas besoin de qualification, h est final
            h();
        }
    };
```  

Notez qu’un appel explicitement qualifié n’est pas virtuel même si la fonction est `virtual`.

**Voir aussi** [fonctions fabriques](007-class.md#rc-factory) @TODO-LINK pour obtenir l’effet d’un appel à une fonction dérivée sans risquer le comportement indéfini.

##### Remarque  

Il n’y a rien d’intrinsèquement mauvais à appeler des fonctions virtuelles depuis des constructeurs et destructeurs. La sémantique de ces appels est sûre. Cependant, l’expérience montre que ces appels sont rares, facilement source de confusion et deviennent un problème pour les novices.

##### Application  

* Signaler les appels de fonctions virtuelles depuis les constructeurs et destructeurs.

### <a name="rc-swap"></a>C.83 : Pour les types à valeur, envisager de fournir une fonction `swap` `noexcept`

##### Raison  

Un `swap` peut être très utile pour implémenter un certain nombre d’idiomes, du déplacement fluide des objets à l’implémentation d’une affectation facile, en passant par une fonction de commit garantie qui permet d’appeler le code appelant de façon fortement sécurisée. Considérez l’utilisation de `swap` pour implémenter l’affectation copie via la construction copie. Voir également [destructeurs, désallocation et swap ne doivent jamais échouer](013-errors.md#re-never-fail).

##### Exemple, bon  

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

Fournir une fonction `swap` non‑membre dans le même espace de noms que votre type pour la commodité des appelants.

```    
    void swap(Foo& a, Foo& b)
    {
        a.swap(b);
    }
```  

##### Application  

* Les types non‑trivially‑copiables devraient fournir un `swap` membre ou une surcharge de fonction libre.  
* (Simple) Quand une classe possède une fonction membre `swap`, elle doit être déclarée `noexcept`.

### <a name="rc-swap-fail"></a>C.84 : Une fonction `swap` ne doit pas échouer

##### Raison  

`swap` est largement utilisé dans des contextes qui supposent qu’il ne peut pas échouer ; les programmes ne peuvent pas facilement être écrits pour fonctionner correctement en présence d’un `swap` qui échoue. Les conteneurs et algorithmes de la STL ne fonctionneront pas correctement si le `swap` d’un type d’élément échoue.

##### Exemple, mauvais  

```    
    void swap(My_vector& x, My_vector& y)
    {
        auto tmp = x;   // copier les éléments
        x = y;
        y = tmp;
    }
```  

Ce n’est pas seulement lent, mais si une allocation est nécessaire pour les éléments de `tmp`, ce `swap` pourrait lancer une exception et ferait échouer les algorithmes STL qui l’utilisent.

##### Application  

(Simple) Quand une classe possède une fonction membre `swap`, elle doit être déclarée `noexcept`.

### <a name="rc-swap-noexcept"></a>C.85 : Rendre `swap` `noexcept`

##### Raison  

[Un `swap` ne doit pas échouer](007-class.md#rc-swap-fail) @TODO-LINK.

##### Application  

(Simple) Quand une classe possède une fonction membre `swap`, elle doit être déclarée `noexcept`.

### <a name="rc-eq"></a>C.86 : Rendre `==` symétrique par rapport aux types d’opérandes et `noexcept`

##### Raison  

Un traitement asymétrique des opérandes est surprenant et source d’erreurs lorsqu’il existe des conversions possibles. `==` est une opération fondamentale et les programmeurs doivent pouvoir l’utiliser sans crainte d’échec.

##### Exemple  

```    
    struct X {
        string name;
        int number;
    };

    bool operator==(const X& a, const X& b) noexcept {
        return a.name == b.name && a.number == b.number;
    }
```  

##### Exemple, mauvais  

```    
    class B {
        string name;
        int number;
        bool operator==(const B& a) const {
            return name == a.name && number == a.number;
        }
        // …
    };
```  

La comparaison de `B` accepte les conversions pour son second opérande, mais pas pour le premier.

##### Remarque  

Si une classe possède un état d’échec, comme le `NaN` de `double`, il est tentant de faire lancer une exception lors de la comparaison avec cet état d’échec. L’alternative est de faire comparer deux états d’échec comme égaux et toute état valide comme faux face à l’état d’échec.

##### Remarque  

Cette règle s’applique à tous les opérateurs de comparaison usuels : `!=`, `<`, `<=`, `>`, `>=`.

##### Application  

* Signaler un `operator==()` dont les types d’argument diffèrent ; idem pour les autres opérateurs de comparaison (`!=`, `<`, `<=`, `>`, `>=`).  
* Signaler les `operator==()` membres ; idem pour les autres opérateurs de comparaison.

### <a name="rc-eq-base"></a>C.87 : Se méfier de `==` sur les classes de base

##### Raison  

Il est très difficile d’écrire un `==` fiable et utile pour une hiérarchie.

##### Exemple, mauvais  

```    
    class B {
        string name;
        int number;
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

    B b = ...
    D d = ...
    b == d;    // compare name et number, ignore le caractère de d
    d == b;    // compare name et number, ignore le caractère de d
    D d2;
    d == d2;   // compare name, number, et character
    B& b2 = d2;
    b2 == d;   // compare name et number, ignore le caractère de d2 et de d
```  

Bien sûr, on peut faire fonctionner `==` dans une hiérarchie, mais les approches naïves ne s’étendent pas.

##### Remarque  

Cette règle s’applique à tous les opérateurs de comparaison usuels : `!=`, `<`, `<=`, `>`, `>=`, et `<=>`.

##### Application  

* Signaler un `operator==()` virtuel ; idem pour les autres opérateurs de comparaison.

### <a name="rc-hash"></a>C.89 : Rendre un `hash` `noexcept`

##### Raison  

Les utilisateurs de conteneurs à hachage utilisent le hash indirectement et ne s’attendent pas à ce qu’un simple accès lance une exception. C’est une exigence de la bibliothèque standard.

##### Exemple, mauvais  

```    
    template<>
    struct hash<My_type> {  // spécialisation de hash très mauvaise
        using result_type = size_t;
        using argument_type = My_type;

        size_t operator()(const My_type & x) const
        {
            size_t xs = x.s.size();
            if (xs < 4) throw Bad_My_type{};    // « Personne n’attend l’Inquisition espagnole ! »
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
```  

Si vous devez définir une spécialisation `hash`, essayez simplement de combiner les spécialisation `hash` de la bibliothèque standard avec `^` (xor). Cela fonctionne généralement mieux que les « astuces » pour les non‑spécialistes.

##### Application  

* Signaler les `hash` qui lancent.

### <a name="rc-memset"></a>C.90 : S’appuyer sur les constructeurs et les opérateurs d’affectation, pas sur `memset` et `memcpy`

##### Raison  

Le mécanisme C++ standard pour créer une instance d’un type consiste à appeler son constructeur. Comme précisé dans la règle [C.41](007-class.md#rc-complete) @TODO-LINK, un constructeur doit créer un objet entièrement initialisé. Aucun initialisation supplémentaire, telle que `memcpy`, ne devrait être requise. Un type fournira un constructeur de copie et/ou un opérateur d’affectation copie pour copier correctement l’objet, en préservant les invariants. Utiliser `memcpy` pour copier un type non triviale déclenche un comportement indéfini. Cela conduit souvent à du tranchage ou à de la corruption de données.

##### Exemple, bon  

```    
    struct base {
        virtual void update() = 0;
        std::shared_ptr<int> sp;
    };

    struct derived : public base {
        void update() override {}
    };
```  

##### Exemple, mauvais  

```    
    void init(derived& a)
    {
        memset(&a, 0, sizeof(derived));
    }
```  

C’est dangereux : cela écrase la vtable.

##### Exemple, mauvais  

```    
    void copy(derived& a, derived& b)
    {
        memcpy(&a, &b, sizeof(derived));
    }
```  

C’est également dangereux : cela écrase la vtable.

##### Application  

* Signaler le passage d’un type non trivially‑copyable à `memset` ou `memcpy`.

---

## <a name="ss-containers"></a>C.con : Conteneurs et autres gestionnaires de ressources

Un conteneur est un objet contenant une séquence d’objets d’un certain type ; `std::vector` est le conteneur archétypal. Un gestionnaire de ressources est une classe qui possède une ressource ; `std::vector` est le gestionnaire de ressources typique ; sa ressource est sa séquence d’éléments.

**Résumé des règles de conteneur :**

* [C.100 : Suivre la STL lorsqu’on définit un conteneur](007-class.md#rcon-stl) @TODO-LINK
* [C.101 : Donner à un conteneur une sémantique de valeur](007-class.md#rcon-val) @TODO-LINK
* [C.102 : Donner à un conteneur des opérations de déplacement](007-class.md#rcon-move) @TODO-LINK
* [C.103 : Donner à un conteneur un constructeur `initializer_list`](007-class.md#rcon-init) @TODO-LINK
* [C.104 : Donner à un conteneur un constructeur par défaut qui l’instancie à vide](007-class.md#rcon-empty) @TODO-LINK
* ???
* [C.109 : Si un gestionnaire de ressources a une sémantique de pointeur, fournir `*` et `->`](007-class.md#rcon-ptr) @TODO-LINK

**Voir aussi** : [Resources](009-resource.md) @TODO-LINK.

### <a name="rcon-stl"></a>C.100 : Suivre la STL lorsqu’on définit un conteneur

##### Raison  

Les conteneurs de la STL sont familiers à la plupart des programmeurs C++ et sont d’une conception fondamentalement solide.

##### Remarque  

Il existe d’autres styles de conception tout aussi solides et parfois des raisons de s’en écarter, mais en l’absence d’une raison solide, il est plus simple et plus facile tant pour les implémenteurs que pour les utilisateurs de suivre le standard.

En particulier, `std::vector` et `std::map` offrent des modèles utiles et relativement simples.

##### Exemple  

```    
    // simplifié (p. ex. pas d’allocateurs) :

    template<typename T>
    class Sorted_vector {
        using value_type = T;
        // … types d’itérateurs …

        Sorted_vector() = default;
        Sorted_vector(initializer_list<T>);    // constructeur initializer‑list : trier et stocker
        Sorted_vector(const Sorted_vector&) = default;
        Sorted_vector(Sorted_vector&&) noexcept = default;
        Sorted_vector& operator=(const Sorted_vector&) = default;     // affectation copie
        Sorted_vector& operator=(Sorted_vector&&) noexcept = default; // affectation déplacement
        ~Sorted_vector() = default;

        Sorted_vector(const std::vector<T>& v);   // stocker et trier
        Sorted_vector(std::vector<T>&& v);        // trier et « voler » la représentation

        const T& operator[](int i) const { return rep[i]; }
        // pas d’accès non‑const direct pour préserver l’ordre

        void push_back(const T&);   // insérer à la bonne place (pas nécessairement à la fin)
        void push_back(T&&);        // insérer à la bonne place (pas nécessairement à la fin)

        // … cbegin(), cend() …
    private:
        std::vector<T> rep;  // utiliser std::vector pour contenir les éléments
    };

    template<typename T> bool operator==(const Sorted_vector<T>&, const Sorted_vector<T>&);
    template<typename T> bool operator!=(const Sorted_vector<T>&, const Sorted_vector<T>&);
    // …
```  

Ici, le style de la STL est suivi, mais incomplet. Ce n’est pas rare. Fournir uniquement la fonctionnalité qui a du sens pour un conteneur spécifique. L’essentiel est de définir les constructeurs, affectations, destructeurs, et itérateurs conventionnels (dans la mesure où ils ont du sens pour le conteneur). À partir de cela, le conteneur peut être étendu selon les besoins. Ici, des constructeurs spéciaux à partir de `std::vector` ont été ajoutés.

##### Application  

??? (non‑enforcable)

### <a name="rcon-val"></a>C.101 : Donner à un conteneur une sémantique de valeur

##### Raison  

Les objets réguliers sont plus simples à comprendre et raisonner que les objets irréguliers. Familiarité.

##### Remarque  

Si cela a du sens, rendre le conteneur « Regular » (le concept). En particulier, s’assurer qu’un objet compare égal à sa copie.

##### Exemple  

```    
    void f(const Sorted_vector<string>& v)
    {
        Sorted_vector<string> v2 {v};
        if (v != v2)
            cout << "Comportement contre la raison et la logique.\n";
        // …
    }
```  

##### Application  

??? (non‑enforcable)

### <a name="rcon-move"></a>C.102 : Donner à un conteneur des opérations de déplacement

##### Raison  

Les conteneurs peuvent devenir volumineux ; sans un constructeur de déplacement et un constructeur de copie, un objet peut être coûteux à déplacer, incitant les programmeurs à passer des pointeurs autour et à gérer les ressources manuellement.

##### Exemple  

```    
    Sorted_vector<int> read_sorted(istream& is)
    {
        vector<int> v;
        cin >> v;   // supposons que nous ayons une opération de lecture pour les vecteurs
        Sorted_vector<int> sv = v;  // tri
        return sv;
    }
```  

L’utilisateur peut raisonnablement supposer que le retour d’un conteneur de type standard est peu coûteux.

##### Application  

??? (non‑enforcable)

### <a name="rcon-init"></a>C.103 : Donner à un conteneur un constructeur `initializer_list`

##### Raison  

Les gens s’attendent à pouvoir initialiser un conteneur avec un ensemble de valeurs. Familiarité.

##### Exemple  

```    
    Sorted_vector<int> sv {1, 3, -1, 7, 0, 0}; // Sorted_vector trie les éléments au besoin
```  

##### Application  

??? (non‑enforcable)

### <a name="rcon-empty"></a>C.104 : Donner à un conteneur un constructeur par défaut qui le place à vide

##### Raison  

Pour le rendre « Regular ».

##### Exemple  

```    
    vector<Sorted_sequence<string>> vs(100);    // 100 Sorted_sequences, chacune avec la valeur ""
```  

##### Application  

??? (non‑enforcable)

### <a name="rcon-ptr"></a>C.109 : Si un gestionnaire de ressources a une sémantique de pointeur, fournir `*` et `->`

##### Raison  

C’est ce qui est attendu des pointeurs. Familiarité.

##### Exemple  

??? (à compléter)

##### Application  

??? (à compléter)

---

## <a name="ss-lambdas"></a>C.lambdas : Objets fonctionnels et lambdas

Un objet fonctionnel est un objet qui surcharge l’opérateur `()` afin que vous puissiez l’appeler. Une expression lambda (souvent abrégée « lambda ») est une notation pour générer un objet fonctionnel. Les objets fonctionnels devraient être peu coûteux à copier (et donc **passés par valeur**).

**Résumé :**

* [F.10 : Si une opération peut être réutilisée, donnez‑lui un nom](006-functions.md#rf-name) @TODO-LINK
* [F.11 : Utiliser une lambda anonyme si vous avez besoin d’un simple objet fonctionnel en un seul endroit](006-functions.md#rf-lambda) @TODO-LINK
* [F.50 : Utiliser une lambda lorsqu’une fonction ne suffit pas (pour capturer des variables locales ou écrire une fonction locale)](006-functions.md#rf-capture-vs-overload) @TODO-LINK
* [F.52 : Préférer la capture par référence dans les lambdas utilisées localement, y compris lorsqu’elles sont passées aux algorithmes](006-functions.md#rf-reference-capture) @TODO-LINK
* [F.53 : Éviter la capture par référence dans les lambdas qui seront utilisées de façon non‑locale, y compris lorsqu’elles sont retournées, stockées sur le tas, ou passées à un autre thread](006-functions.md#rf-value-capture) @TODO-LINK
* [ES.28 : Utiliser les lambdas pour des initialisations complexes, surtout de variables `const`](010-expr.md#res-lambda-init) @TODO-LINK

---

## <a name="ss-hier"></a>C.hier : Hiérarchies de classes (POO)

Une hiérarchie de classes est construite pour représenter un ensemble de concepts organisés hiérarchiquement (uniquement). Typiquement, les classes de base agissent comme interfaces. Il existe deux grandes utilisations des hiérarchies, souvent appelées héritage d’implémentation et héritage d’interface.

**Résumé des règles concernant les hiérarchies de classes :**

* [C.120 : Utiliser les hiérarchies de classes pour représenter des concepts avec une structure hiérarchique inhérente (uniquement)](007-class.md#rh-domain) @TODO-LINK
* [C.121 : Si une classe de base est utilisée comme interface, en faire une classe purement abstraite](007-class.md#rh-abstract) @TODO-LINK
* [C.122 : Utiliser des classes abstraites comme interfaces lorsqu’une séparation complète entre interface et implémentation est nécessaire](007-class.md#rh-separation) @TODO-LINK

**Conception de classes dans une hiérarchie :**

* [C.126 : Une classe abstraite n’a généralement pas besoin d’un constructeur défini par l’utilisateur](007-class.md#rh-abstract-ctor) @TODO-LINK
* [C.127 : Une classe avec une fonction virtuelle doit avoir un destructeur virtuel ou protégé](007-class.md#rh-dtor) @TODO-LINK
* [C.128 : Les fonctions virtuelles doivent spécifier exactement l’un des mots‑clés `virtual`, `override` ou `final`](007-class.md#rh-override) @TODO-LINK
* [C.129 : Lors de la conception d’une hiérarchie, différencier l’héritage d’implémentation de l’héritage d’interface](007-class.md#rh-kind) @TODO-LINK
* [C.130 : Pour réaliser des copies profondes de classes polymorphes, privilégier une fonction virtuelle `clone` plutôt qu’un constructeur/copieur public](007-class.md#rh-copy) @TODO-LINK
* [C.131 : Éviter les getters et setters triviaux](007-class.md#rh-get) @TODO-LINK
* [C.132 : Ne pas rendre une fonction `virtual` sans raison](007-class.md#rh-virtual) @TODO-LINK
* [C.133 : Éviter les données `protected`](007-class.md#rh-protected) @TODO-LINK
* [C.134 : Garantir que tous les membres non‑`const` ont le même niveau d’accès](007-class.md#rh-public) @TODO-LINK
* [C.135 : Utiliser l’héritage multiple pour représenter plusieurs interfaces distinctes](007-class.md#rh-mi-interface) @TODO-LINK
* [C.136 : Utiliser l’héritage multiple pour représenter l’union d’attributs d’implémentation](007-class.md#rh-mi-implementation) @TODO-LINK
* [C.137 : Utiliser des bases virtuelles pour éviter des classes de base trop générales](007-class.md#rh-vbase) @TODO-LINK
* [C.138 : Créer un ensemble de surcharges pour une classe dérivée et ses bases avec `using`](007-class.md#rh-using) @TODO-LINK
* [C.139 : Utiliser `final` sur les classes avec parcimonie](007-class.md#rh-final) @TODO-LINK
* [C.140 : Ne pas fournir différents arguments par défaut pour une fonction virtuelle et un override](007-class.md#rh-virtual-default-arg) @TODO-LINK

**Accès aux objets dans une hiérarchie :**

* [C.145 : Accéder aux objets polymorphes via des pointeurs et références](007-class.md#rh-poly) @TODO-LINK
* [C.146 : Utiliser `dynamic_cast` lorsque la navigation dans la hiérarchie est incontournable](007-class.md#rh-dynamic_cast) @TODO-LINK
* [C.147 : Utiliser `dynamic_cast` vers un type référence lorsque l’échec est considéré comme une erreur](007-class.md#rh-ref-cast) @TODO-LINK
* [C.148 : Utiliser `dynamic_cast` vers un type pointeur lorsque l’échec est considéré comme une alternative valable](007-class.md#rh-ptr-cast) @TODO-LINK
* [C.149 : Utiliser `unique_ptr` ou `shared_ptr` pour éviter d’oublier de `delete` les objets créés avec `new`](007-class.md#rh-smart) @TODO-LINK
* [C.150 : Utiliser `make_unique()` pour construire des objets possédés par des `unique_ptr`s](007-class.md#rh-make_unique) @TODO-LINK
* [C.151 : Utiliser `make_shared()` pour construire des objets possédés par des `shared_ptr`s](007-class.md#rh-make_shared) @TODO-LINK
* [C.152 : Ne jamais assigner un pointeur vers un tableau d’objets dérivés à un pointeur vers sa base](007-class.md#rh-array) @TODO-LINK
* [C.153 : Privilégier la fonction virtuelle au cast](007-class.md#rh-use-virtual) @TODO-LINK

---

### <a name="rh-domain"></a>C.120 : Utiliser les hiérarchies de classes pour représenter uniquement des concepts avec une structure hiérarchique inhérente

##### Raison  

Représenter directement les idées dans le code facilite la compréhension et la maintenance. Assurez‑vous que l’idée représentée par la classe de base correspond exactement à tous les types dérivés et qu’il n’existe pas de meilleure façon d’exprimer cela que l’utilisation d’une relation d’héritage étroite.

*Ne pas* utiliser l’héritage lorsqu’un simple membre de donnée suffit. En général cela signifie que le type dérivé doit surcharger une fonction virtuelle de la base ou accéder à un membre `protected`.

##### Exemple  

```    
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
```  

##### Exemple, mauvais  

Ne **pas** représenter des concepts non hiérarchiques comme hiérarchies de classes.

```    
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
```  

Ici, la plupart des classes dérivées ne pourront implémenter correctement la plupart des fonctions requises par l’interface, ce qui rend la classe de base une charge d’implémentation. De plus, l’utilisateur de `Container` ne peut pas compter sur le fait que les fonctions effectuent réellement ce qui est attendu ; il devra recourir à des vérifications d’exécution ou éviter d’utiliser cette interface trop générale au profit d’une interface particulier rencontrée via `dynamic_cast`.

##### Application  

* Repérer les classes avec de nombreux membres qui ne font rien d’autre que lancer des exceptions.  
* Signaler chaque usage d’une classe de base non publique `B` où la classe dérivée `D` n’override pas de fonction virtuelle ou n’accède pas à un membre protégé de `B`, et où `B` n’est pas : vide, un paramètre de modèle, ou une classe modèle spécialisée avec `D`.

### <a name="rh-abstract"></a>C.121 : Si une classe de base est utilisée comme interface, en faire une classe purement abstraite

##### Raison  

Une classe est plus stable (moins fragile) si elle ne contient pas de données. Les interfaces devraient normalement être composées uniquement de fonctions virtuelles pures publiques et d’un destructeur virtuel par défaut ou `=default`.

##### Exemple  

```    
    class My_interface {
    public:
        // … uniquement des fonctions virtuelles pures …
        virtual ~My_interface() {}   // ou =default
    };
```  

##### Exemple, mauvais  

```    
    class Goof {
    public:
        // … uniquement des fonctions virtuelles pures …
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
        g(p.get()); // utiliser Derived via l’interface Goof
    } // fuite
```  

Le `Derived` sera `delete`d via son interface `Goof`, donc son `string` fuira. Ajoutez à `Goof` un destructeur virtuel, et tout rentre dans l’ordre.

##### Application  

* Avertir toute classe qui possède des membres de données tout en ayant une fonction virtuelle non‑`final` qui n’a pas été héritée d’une classe de base.

### <a name="rh-separation"></a>C.122 : Utiliser des classes abstraites comme interfaces lorsque la séparation complète entre interface et implémentation est requise

##### Raison  

Typiquement à la frontière ABI (liaison).

##### Exemple  

```    
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
```  

Un utilisateur peut désormais utiliser `D1` et `D2` de façon interchangeable via l’interface fournie par `Device`. De plus, nous pouvons mettre à jour `D1` et `D2` de façon incompatible avec les versions antérieures tant que tout accès se fait via `Device`.

##### Application  

??? (non‑enforcable)

## C.hierclass : Conception de classes dans une hiérarchie

### <a name="rh-abstract-ctor"></a>C.126 : Une classe abstraite n’a généralement pas besoin d’un constructeur défini par l’utilisateur

##### Raison  

Une classe abstraite ne possède généralement aucune donnée à initialiser.

##### Exemple  

```    
    class Shape {
    public:
        // pas de constructeur défini par l’utilisateur nécessaire dans la classe abstraite
        virtual Point center() const = 0;    // pure virtual
        virtual void move(Point to) = 0;
        // … plus de fonctions virtuelles pures …
        virtual ~Shape() {}                 // destructeur
    };

    class Circle : public Shape {
    public:
        Circle(Point p, int rad);           // constructeur dans la classe dérivée
        Point center() const override { return x; }
    };
```  

##### Exception  

* Un constructeur de classe de base qui effectue du travail, par ex. enregistrer l’objet quelque part, peut nécessiter un constructeur.  
* Dans des cas très rares, il peut être raisonnable qu’une classe abstraite possède un peu de données partagées par toutes les classes dérivées (ex. statistiques, informations de débogage). De telles classes ont tendance à nécessiter un héritage virtuel.

##### Application  

Signaler les classes abstraites qui possèdent des constructeurs définis par l’utilisateur.

### <a name="rh-dtor"></a>C.127 : Une classe avec une fonction virtuelle devrait avoir un destructeur virtuel ou protégé

##### Raison  

Une classe avec une fonction virtuelle est généralement (et en général) utilisée via un pointeur de base. Habituellement, le dernier utilisateur doit appeler `delete` sur un pointeur de base, souvent via un `unique_ptr` ou `shared_ptr` à la base, donc le destructeur doit être public et virtuel. Plus rarement, si la suppression via un pointeur de base n’est pas prévue, le destructeur doit être protégé et non‑virtuel ; voir [C.35](007-class.md#rc-dtor-virtual) @TODO-LINK.

##### Exemple, mauvais  

```    
    struct B {
        virtual int f() = 0;
        // … pas de destructeur défini, implicitement public non‑virtuel …
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
    } // comportement indéfini, ~B() uniquement appelé, fuite possible de D::s
```  

##### Remarque  

Certaines personnes n’appliquent pas cette règle parce qu’elles prévoient d’utiliser uniquement la classe via `shared_ptr` : `std::shared_ptr<B> p = std::make_shared<D>(args);`. Le pointeur partagé se charge de la suppression, de sorte qu’aucune fuite ne survient si le destructeur n’est pas virtuel. Les personnes qui le font systématiquement peuvent obtenir un faux‑positif, mais la règle reste importante — que se passe‑t‑il si on utilise `make_unique` ? Ce n’est pas sûr à moins que l’auteur de `B` ne garantisse qu’une telle utilisation est impossible, par ex. en rendant tous les constructeurs privés et en fournissant une fonction fabrique qui alloue via `make_shared`.

##### Application  

* Une classe avec des fonctions virtuelles doit avoir un destructeur qui soit public et virtuel, ou bien protégé et non‑virtuel.  
* Signaler un `delete` d’une classe possédant des fonctions virtuelles mais aucun destructeur virtuel.

### <a name="rh-override"></a>C.128 : Les fonctions virtuelles doivent spécifier exactement l’un des mots‑clés `virtual`, `override` ou `final`

##### Raison  

Lisibilité.  
Détection d’erreurs.  
Écrire explicitement `virtual`, `override` ou `final` est auto‑documentant et permet au compilateur de détecter les incompatibilités de types ou de noms entre bases et dérivées. En revanche, écrire plus d’un de ces trois mots‑clés est redondant et source potentielle d’erreurs.

C’est simple et clair :

* `virtual` signifie exactement « c’est une nouvelle fonction virtuelle ».  
* `override` signifie exactement « c’est un override non `final` ».  
* `final` signifie exactement « c’est un override final ».

##### Exemple, mauvais  

```    
    struct B {
        void f1(int);
        virtual void f2(int) const;
        virtual void f3(int);
        // …
    };

    struct D : B {
        void f1(int);        // mauvais (espérer un warning) : D::f1 cache B::f1
        void f2(int) const;  // mauvais (mais valide) : pas d’override explicite
        void f3(double);     // mauvais (espérer un warning) : D::f3 cache B::f3
        // …
    };
```  

##### Exemple, bon  

```    
    struct Better : B {
        void f1(int) override;        // erreur (capturée) : D::f1 cache B::f1
        void f2(int) const override;
        void f3(double) override;     // erreur (capturée) : D::f3 cache B::f3
        // …
    };
```  

#### Discussion  

Nous voulons éliminer deux classes d’erreurs particulières :

* **implicit virtual** : le programmeur voulait implicitement que la fonction soit virtuelle (et elle l’est) – ou voulait qu’elle ne le soit pas (par inadvertance) – ou le voulait, mais la signature ne correspond pas.  
* **implicit override** : le programmeur voulait implicitement que la fonction soit un override (et elle l’est) – ou voulait qu’elle ne le soit pas – ou le voulait, mais la signature ne correspond pas.

Note : sur une classe marquée `final`, chaque fonction virtuelle individuelle devrait utiliser soit `override` soit `final` ; il n’y a aucune différence sémantique dans ce cas.

Note : Utiliser `final` sur les fonctions avec parcimonie. Cela ne conduit pas nécessairement à des optimisations, et empêche toute future surcharge.

##### Application  

* Comparer les noms de fonctions virtuelles dans les bases et les dérivées et signaler les usages du même nom qui ne sont pas des overrides.  
* Signaler les overrides qui n’utilisent ni `override` ni `final`.  
* Signaler les déclarations de fonction qui utilisent plus d’un des mots‑clés `virtual`, `override` et `final`.

### <a name="rh-kind"></a>C.129 : Lors de la conception d’une hiérarchie, différencier l’héritage d’implémentation de l’héritage d’interface

##### Raison  

Les détails d’implémentation dans une interface rendent l’interface fragile ; les utilisateurs deviennent dépendants d’une recompilation suite à des changements d’implémentation. Les données dans une classe de base augmentent la complexité de l’implémentation de la base et peuvent mener à de la duplication de code.

**Définitions :**

* *héritage d’interface* : utilisation de l’héritage pour séparer les utilisateurs de l’implémentation, en particulier pour permettre l’ajout ou le changement de classes dérivées sans affecter les utilisateurs des bases.  
* *héritage d’implémentation* : utilisation de l’héritage pour simplifier l’implémentation de nouvelles fonctionnalités en rendant des opérations utiles disponibles pour les implémenteurs de nouvelles opérations (parfois appelé « programming by difference »).

Une classe abstraite pure est simplement un ensemble de fonctions virtuelles pures ; voir [I.25](005-interfaces.md#ri-abstract).

Dans les premières années de la POO (années 80 / 90), les deux types d’héritage étaient souvent mélangés et les mauvaises habitudes persistent. Aujourd’hui, les mélanges sont encore communs dans les bases de code anciennes et les matériels d’enseignement.

L’importance de garder les deux types séparés augmente :

* avec la taille d’une hiérarchie (ex. dizaines de dérivés),  
* avec la durée d’utilisation de la hiérarchie (ex. décennies),  
* avec le nombre d’organisations distinctes qui utilisent la hiérarchie (ex. difficile de distribuer une mise à jour d’une base).

##### Exemple, mauvais  

```    
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
        Triangle(Point p1, Point p2, Point p3); // calculer le centre
        // …
    };
```  

Problèmes :

* À mesure que la hiérarchie grandit et que davantage de données sont ajoutées à `Shape`, les constructeurs deviennent plus difficiles à écrire et à maintenir.  
* Pourquoi calculer le centre pour le `Triangle` ? Nous ne l’utiliserons peut‑être jamais.  
* Ajouter un membre à `Shape` (ex. style de dessin ou canevas) implique de réviser toutes les classes dérivées ainsi que tout le code qui utilise `Shape` ; cela nécessite souvent recompilation et modifications.

L’implémentation de `Shape::move()` est un exemple d’héritage d’implémentation : nous avons défini `move()` une fois pour toutes les classes dérivées. Plus le code de la fonction d’implémentation et plus de données sont partagées dans la base, plus les bénéfices sont grands – mais la hiérarchie devient moins stable.

##### Exemple (interface uniquement)  

```    
    class Shape {  // interface pure
    public:
        virtual Point center() const = 0;
        virtual Color color() const = 0;

        virtual void rotate(int) = 0;
        virtual void move(Point p) = 0;

        virtual void redraw() = 0;

        // …
    };
```  

Notez qu’une interface pure possède rarement des constructeurs : il n’y a rien à construire.

```    
    class Circle : public Shape {
    public:
        Circle(Point c, int r, Color c) : cent{c}, rad{r}, col{c} { /* … */ }

        Point center() const override { return cent; }
        Color color() const override { return col; }

        // …
    private:
        Point cent;
        int rad;
        Color col;
    };
```  

L’interface est maintenant moins fragile, mais il y a plus de travail à implémenter les fonctions membres. Par exemple, `center` doit être implémenté par chaque classe dérivée de `Shape`.

##### Exemple, hiérarchie double  

Comment obtenir le meilleur des deux mondes ? Une hiérarchie d’interface pour la stabilité et une hiérarchie d’implémentation pour la réutilisation du code.  

Il existe de nombreuses façons de réaliser cela ; voici une variante à héritage multiple.

Premièrement, créons une hiérarchie d’interfaces :

```    
    class Shape {   // interface pure
    public:
        virtual Point center() const = 0;
        virtual Color color() const = 0;

        virtual void rotate(int) = 0;
        virtual void move(Point p) = 0;

        virtual void redraw() = 0;

        // …
    };

    class Circle : public virtual Shape {   // interface pure
    public:
        virtual int radius() = 0;
        // …
    };
```  

Pour rendre cela utile, nous devons fournir les implémentations (ici, nommées pareillement, mais dans l’espace de noms `Impl`) :

```    
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
```  

```    
    class Impl::Circle : public virtual ::Circle, public Impl::Shape {   // implémentation
    public:
        // constructeurs, destructeur

        int radius() override { /* … */ }
        // …
    };
```  

Et nous pourrions étendre les hiérarchies avec une classe `Smiley` :

```    
    class Smiley : public virtual Circle { // interface pure
    public:
        // …
    };

    class Impl::Smiley : public virtual ::Smiley, public Impl::Circle {   // implémentation
    public:
        // constructeurs, destructeur
        // …
    }
```  

Nous avons maintenant deux hiérarchies :

* interface : Smiley → Circle → Shape  
* implémentation : Impl::Smiley → Impl::Circle → Impl::Shape  

Comme chaque implémentation dérive de son interface ainsi que de son implémentation de base, nous obtenons un réseau (DAG) :

```    
    Smiley     ->         Circle     ->  Shape
      ^           ^               ^               ^
      |           |               |               |
    Impl::Smiley -> Impl::Circle -> Impl::Shape
```  

**Note** : Il existe d’autres techniques, comme le *Pimpl* (voir [005-interfaces.md#ri-pimpl]).

**Note** : Souvent, il faut choisir entre fournir une fonctionnalité commune comme fonctions de base (méthodes de base) ou comme fonctions libres (dans un espace de noms d’implémentation). Les classes de base offrent une notation plus courte et un accès plus aisé aux données partagées, mais la fonctionnalité n’est alors disponible que pour les utilisateurs de la hiérarchie.

##### Application  

* Signaler une conversion dérivée → base où la base possède à la fois des données et des fonctions virtuelles (sauf si la conversion provient d’un membre de la classe dérivée appelant un membre de la base).

### <a name="rh-copy"></a>C.130 : Pour faire des copies profondes de classes polymorphes, privilégier une fonction virtuelle `clone` plutôt qu’un constructeur/copieur public

##### Raison  

Copier une classe polymorphe est découragé à cause du problème de *slicing* (voir [C.67](007-class.md#rc-copy-virtual) @TODO-LINK). Si vous avez réellement besoin d’une sémantique de copie, copiez en profondeur : fournissez une fonction virtuelle `clone` qui copiera le type le plus dérivé réel et renverra un pointeur propriétaire vers le nouvel objet, puis dans les classes dérivées, retournez le type dérivé (utilisez un type de retour covariant).

##### Exemple  

```    
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
```  

En général, il est recommandé d’utiliser des pointeurs intelligents pour représenter la propriété (voir [R.20](009-resource.md#rr-owner) @TODO-LINK). Cependant, à cause des règles du langage, le type de retour covariant ne peut pas être un `unique_ptr<D>` alors que `B::clone` retourne `unique_ptr<B>`. On doit donc soit retourner `unique_ptr<B>` dans toutes les surcharges, soit utiliser le type `owner<>` de la GSL.

### <a name="rh-get"></a>C.131 : Éviter les getters et setters triviaux

##### Raison  

Un getter ou setter trivial n’ajoute aucune valeur sémantique ; les données pourraient simplement être `public`.

##### Exemple  

```    
    class Point {   // Mauvais : verbeux
        int x;
        int y;
    public:
        Point(int xx, int yy) : x{xx}, y{yy} { }
        int get_x() const { return x; }
        void set_x(int xx) { x = xx; }
        int get_y() const { return y; }
        void set_y(int yy) { y = yy; }
        // pas de fonctions comportementales
    };
```  

Considérez transformer une telle classe en `struct` — un groupe de variables sans comportement, toutes publiques, sans fonctions membres.

```    
    struct Point {
        int x {0};
        int y {0};
    };
```  

Notez que nous pouvons mettre des initialiseurs par défaut sur les membres : [C.49 : Préférer l’initialisation à l’affectation dans les constructeurs](007-class.md#rc-initialize) @TODO-LINK.

##### Remarque  

La clé de cette règle est de savoir si la sémantique du getter/setter est triviale. Si une différence existerait autrement qu’au niveau syntaxique (par ex. maintien d’une invariant, conversion entre un type interne et un type d’interface), alors le getter/setter a une valeur.

##### Application  

Flaguer plusieurs fonctions `get` et `set` qui n’ont aucun autre comportement que d’accéder directement à un membre.

### <a name="rh-virtual"></a>C.132 : Ne pas rendre une fonction `virtual` sans raison

##### Raison  

`virtual` ajoute du temps d’exécution et augmente la taille du code objet. Une fonction virtuelle peut être redéfinie, ce qui ouvre la porte à des erreurs dans les classes dérivées. Une fonction virtuelle garantit la réplication du code dans une hiérarchie de modèles.

##### Exemple, mauvais  

```    
    template<class T>
    class Vector {
    public:
        // …
        virtual int size() const { return sz; }   // mauvais : que pourrait faire une classe dérivée ?
    private:
        T* elem;   // les éléments
        int sz;    // nombre d’éléments
    };
```  

Ce type de « vector » n’est pas destiné à être utilisé comme classe de base.

##### Application  

* Signaler une classe qui possède des fonctions virtuelles mais aucune classe dérivée.  
* Signaler une classe dont toutes les fonctions sont virtuelles et ont une implémentation.

### <a name="rh-protected"></a>C.133 : Éviter les données `protected`

**Formulation alternative** : Rendre les données membres `public` ou (de préférence) `private`.

##### Raison  

Les données `protected` sont une source de complexité et d’erreurs. Elles compliquent la rédaction d’invariants. Les données `protected` violent la consigne qui recommande d’éviter de mettre des données dans les classes utilisées comme interfaces, ce qui conduit souvent à devoir recourir à l’héritage virtuel.

##### Exemple, mauvais  

```    
    class Shape {
    public:
        // … fonctions d’interface …
    protected:
        // données pour les classes dérivées :
        Color fill_color;
        Color edge_color;
        Style st;
    };
```  

Désormais, chaque classe dérivée de `Shape` doit manipuler correctement les données protégées. Cela a été populaire, mais c’est une source majeure de problèmes de maintenance. Dans une grande hiérarchie, la gestion cohérente de données protégées devient difficile car le code est dispersé sur de nombreuses classes. Tout le monde peut dériver une nouvelle classe et commencer à manipuler les données protégées. Souvent il est impossible d’examiner l’ensemble complet des classes, de sorte que tout changement à la représentation de la classe devient inviable. Il n’existe pas d’invariant enforceable pour les données protégées ; c’est pratiquement comme des variables globales.  

##### Remarque  

Les données protégées semblent attrayantes pour permettre des améliorations arbitrary via la dérivation. Souvent, cela aboutit à des changements non‑principaux et à des erreurs. [Préférer les données `private`](007-class.md#rc-private) avec un invariant bien spécifié et appliqué. Alternativement, [garder les données hors de toute classe utilisée comme interface](007-class.md#rh-abstract).

##### Remarque  

Les fonctions membres protégées peuvent très bien fonctionner.

##### Application  

Signaler les classes contenant des données `protected`.

### <a name="rh-public"></a>C.134 : Garantir que tous les membres non‑`const` ont le même niveau d’accès

##### Raison  

Éviter la confusion et les erreurs. Si les membres non‑`const` n’ont pas le même niveau d’accès, le type est confus quant à son intention. Est‑il un type qui maintient une invariant ou simplement un agrégat de valeurs ?

**Discussion**

Il y a deux catégories de membres :

* **A** : Membres qui ne participent pas à l’invariant. Toute combinaison de valeurs est valide.  
* **B** : Membres qui participent à l’invariant. Toutes les combinaisons ne sont pas valides (sinon il n’y aurait pas d’invariant).  

Les membres de catégorie **A** devraient être `public` (ou rarement `protected` si vous voulez qu’ils ne soient visibles que des dérivés). Ils n’ont pas besoin d’encapsulation. Tout le code du système pourrait tout autant les voir et les manipuler.

Les membres de catégorie **B** doivent être `private` ou `const`. L’encapsulation est importante ; rendre ces membres non `private` et non `const` signifie que l’objet ne peut plus contrôler son propre état : un nombre illimité de code extérieur aurait besoin de connaître l’invariant et de le faire respecter. Cela conduit à du code fragile, couplé, difficile à maintenir. Tout code qui modifie ces membres de façon invalide corrompt l’objet.

La plupart des classes sont soit **tout A** soit **tout B** :

* **Tout public** : Si vous écrivez un agrégat de variables sans invariant, toutes les variables devraient être `public`. [Par convention, déclarez de telles classes `struct` plutôt que `class`](007-class.md#rc-struct).  
* **Tout privé** : Si vous écrivez un type qui maintient un invariant, tous les membres non‑`const` devraient être `private` — il faut encapsuler.

##### Exception  

Parfois, des classes mélangent **A** et **B**, typiquement pour le débogage. Un objet encapsulé peut contenir quelque chose comme des instruments de débogage qui ne font pas partie de l’invariant. Dans ce cas, les parties **A** devraient être traitées comme **A** (rendre `public`, ou `protected` dans les cas rares) et les parties **B** rester `private` ou `const`.

##### Application  

Signaler toute classe dont les membres non‑`const` ont des niveaux d’accès différents.

### <a name="rh-mi-interface"></a>C.135 : Utiliser l’héritage multiple pour représenter plusieurs interfaces distinctes

##### Raison  

Toutes les classes n’auront pas nécessairement toutes les interfaces, et tous les appelants ne voudront pas forcément gérer toutes les opérations. Surtout pour séparer les interfaces « aspects » de comportement qu’une classe dérivée peut supporter.

##### Exemple  

```    
    class iostream : public istream, public ostream {   // très simplifié
        // …
    };
```  

`istream` fournit l’interface des opérations d’entrée ; `ostream` fournit celle des opérations de sortie. `iostream` fournit l’union des interfaces `istream` et `ostream` ainsi que la synchronisation nécessaire pour les deux sur un même flux.

##### Remarque  

C’est un usage très commun de l’héritage, car le besoin d’interfaces multiples est fréquent et ces interfaces sont rarement organisées naturellement en une hiérarchie à racine unique.

##### Remarque  

Ces interfaces sont généralement des classes abstraites.

##### Application  

??? (non‑enforcable)

### <a name="rh-mi-implementation"></a>C.136 : Utiliser l’héritage multiple pour représenter l’union d’attributs d’implémentation

##### Raison  

Certaines formes de mixins possèdent un état et souvent des opérations sur cet état. Si les opérations sont virtuelles, l’utilisation de l’héritage est nécessaire ; sinon, l’utilisation de l’héritage peut éviter le code boiler‑plate et le forwarding.

##### Exemple  

```    
    class iostream : public istream, public ostream {   // très simplifié
        // …
    };
```  

`istream` fournit l’interface d’entrée (et des données) ; `ostream` fournit l’interface de sortie (et des données). `iostream` fournit l’union des interfaces `istream` et `ostream` ainsi que la synchronisation nécessaire.

##### Remarque  

Cet usage est relativement rare parce que l’implémentation peut souvent être organisée en une hiérarchie à racine unique.

##### Exemple  

Parfois, un « attribut d’implémentation » ressemble davantage à un *mixin* qui détermine le comportement d’une implémentation et injecte des membres pour supporter les politiques qu’il requiert. Par ex. `std::enable_shared_from_this` ou les bases de boost.intrusive (ex. `list_base_hook` ou `intrusive_ref_counter`).

##### Application  

??? (non‑enforcable)

### <a name="rh-vbase"></a>C.137 : Utiliser des bases virtuelles pour éviter des classes de base trop générales

##### Raison  

Permettre la séparation des données partagées et de l’interface. Éviter que toutes les données partagées soient placées dans une classe de base ultime.

##### Exemple  

```    
    struct Interface {
        virtual void f();
        virtual int g();
        // … pas de données ici …
    };

    class Utility {  // avec données
        void utility1();
        virtual void utility2();    // point d’extension
    public:
        int x;
        int y;
    };

    class Derive1 : public Interface, virtual protected Utility {
        // override Interface functions
        // peut‑être override Utility virtual functions
        // …
    };

    class Derive2 : public Interface, virtual protected Utility {
        // override Interface functions
        // peut‑être override Utility virtual functions
        // …
    };
```  

Facteurisation de `Utility` a du sens si de nombreuses classes dérivées partagent des « détails d’implémentation » significatifs.

##### Remarque  

L’exemple est trop « théorique », mais il est difficile de trouver un petit exemple réaliste. Voir [un exemple plus réaliste](https://www.quora.com/What-are-the-uses-and-advantages-of-virtual-base-class-in-C%2B%2B/answer/Lance-Diduck).

##### Remarque  

Souvent, la linéarisation d’une hiérarchie est une meilleure solution.

##### Application  

Flagger les hiérarchies qui mélangent interface et implémentation.

### <a name="rh-using"></a>C.138 : Créer un ensemble de surcharges pour une classe dérivée et ses bases avec `using`

##### Raison  

Sans déclaration `using`, les fonctions membres de la classe dérivée masquent l’ensemble complet d’ensembles de surcharges hérités.

##### Exemple, mauvais  

```    
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
```  

##### Exemple, bon  

```    
    class D: public B {
    public:
        int f(int i) override { std::cout << "f(int): "; return i + 1; }
        using B::f; // expose f(double)
    };
```  

##### Remarque  

Ce problème affecte les fonctions virtuelles et non‑virtuelles.

Pour les bases variadiques, C++17 a introduit une forme variadique de la déclaration `using` :

```    
    template<class... Ts>
    struct Overloader : Ts... {
        using Ts::operator()...; // expose operator() de chaque base
    };
```  

##### Application  

Diagnostiquer le masquage de noms.

### <a name="rh-final"></a>C.139 : Utiliser `final` sur les classes avec parcimonie

##### Raison  

Capter une hiérarchie avec `final` est rarement nécessaire pour des raisons logiques et peut nuire à l’extensibilité d’une hiérarchie.

##### Exemple, mauvais  

```    
    class Widget { /* … */ };

    // personne n’aura jamais besoin d’améliorer My_widget (ou du moins vous le pensez)
    class My_widget final : public Widget { /* … */ };

    class My_improved_widget : public My_widget { /* … */ };  // erreur : impossible
```  

##### Remarque  

Toutes les classes ne sont pas destinées à être des bases. La plupart des classes de la bibliothèque standard en sont des exemples (ex. `std::vector`, `std::string`). Cette règle concerne les classes avec fonctions virtuelles destinées à être des bases d’une hiérarchie.

##### Remarque  

Les affirmations de gains de performances grâce à `final` devraient être justifiées. Trop souvent, ces affirmations se basent sur des conjectures ou sur l’expérience d’autres langages.

Il existe des exemples où `final` peut être important pour des raisons logiques et de performances. Par ex. une hiérarchie d’AST très performante dans un compilateur : les classes dérivées ne sont ajoutées que très rarement, généralement par les implémenteurs de bibliothèques. Cependant, les abus sont plus fréquents.

##### Application  

* Signaler les usages de `final` sur des classes.

### <a name="rh-virtual-default-arg"></a>C.140 : Ne pas fournir différents arguments par défaut pour une fonction virtuelle et un override

##### Raison  

Cela peut créer de la confusion : un override ne hérite pas des arguments par défaut.

##### Exemple, mauvais  

```    
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
    d.multiply(10);    // avec des arguments différents et donc des résultats différents
```  

##### Application  

Signaler les arguments par défaut sur les fonctions virtuelles lorsqu’ils diffèrent entre la base et la dérivée.

---

## <a name="s-hier-access"></a>C.hier‑access : Accès aux objets dans une hiérarchie

### <a name="rh-poly"></a>C.145 : Accéder aux objets polymorphes via des pointeurs et références

##### Raison  

Si vous avez une classe avec une fonction virtuelle, vous ne savez généralement pas quelle classe fournit réellement la fonction à appeler.

##### Exemple  

```    
    struct B { int a; virtual int f(); virtual ~B() = default };
    struct D : B { int b; int f() override; };

    void use(B b)
    {
        D d;
        B b2 = d;   // tranchage
        B b3 = b;
    }

    void use2()
    {
        D d;
        use(d);   // tranchage
    }
```  

Dans les deux cas, `d` est tranché.

##### Exception  

Vous pouvez accéder en toute sécurité à un objet polymorphe nommé dans le scope de sa définition, il suffit de ne pas le trancher.

```    
    void use3()
    {
        D d;
        d.f();   // OK
    }
```  

##### Voir aussi  

[Une classe polymorphe doit supprimer la copie](007-class.md#rc-copy-virtual) @TODO-LINK.

##### Application  

* Signaler tout tranchage.

### <a name="rh-dynamic_cast"></a>C.146 : Utiliser `dynamic_cast` lorsque la navigation dans la hiérarchie de classes est inévitable

##### Raison  

`dynamic_cast` est vérifié à l’exécution.

##### Exemple  

```    
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
```  

L’utilisation d’autres casts peut violer la sécurité de type et conduire le programme à accéder à une variable qui est réellement de type `X` comme si elle était d’un type sans rapport `Z` :

```    
    void user2(B* pb)   // mauvais
    {
        D* pd = static_cast<D*>(pb);    // je sais que pb pointe réellement sur un D ; confiance aveugle
        // ... utiliser l’interface de D ...
    }

    void user3(B* pb)    // unsafe
    {
        if (some_condition) {
            D* pd = static_cast<D*>(pb);   // je sais que pb pointe réellement sur un D ; confiance aveugle
            // ... utiliser l’interface de D ...
        }
        else {
            // ... se contenter de l’interface de B ...
        }
    }

    void f()
    {
        B b;
        user(&b);   // OK
        user2(&b);  // mauvais : erreur
        user3(&b);  // OK *si* la condition est correctement vérifiée
    }
```  

##### Remarque  

`dynamic_cast` est parfois surexploité. [Privilégier les fonctions virtuelles aux casts](007-class.md#rh-use-virtual) @TODO-LINK. Privilégier la [polymorphie statique](#???) lorsqu’elle est possible (pas de résolution à l’exécution) et raisonnablement commode.

##### Remarque  

Certaines personnes utilisent `dynamic_cast` là où `typeid` serait plus approprié ; `dynamic_cast` est une opération « est‑un‑type » générale pour découvrir la meilleure interface d’un objet, tandis que `typeid` est une opération « donne‑moi le type exact » pour découvrir le type réel d’un objet. Le second est plus simple et généralement plus rapide. Si `typeid` n’est pas disponible (p.ex. l’environnement interdit le RTTI), il faut implémenter un mécanisme similaire.

```    
    struct B {
        const char* name {"B"};
        // si pb1->id() == pb2->id() *pb1 est du même type que *pb2
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

        if (pb2->id() == "D") {         // a l’air innocent
            D* pd = static_cast<D*>(pb2);
            // ...
        }
        // ...
    }
```  

Le résultat de `pb2->id() == "D"` est en fait implémentation‑dépendant. Nous l’ajoutons pour alerter sur le danger des RTTI maison. Ce code pourrait fonctionner pendant des années, puis échouer sur une nouvelle machine, un nouveau compilateur, ou un nouveau lien qui ne fusionne pas les littéraux de caractères.

Si vous implémentez votre propre RTTI, soyez prudent.

##### Exception  

Si votre implémentation fournit un `dynamic_cast` réellement lent, vous pourriez devoir recourir à une solution de contournement. Cependant, assurez‑vous que le `dynamic_cast` est réellement lent (les rumeurs sur la lenteur sont souvent infondées) et que l’usage est vraiment une contrainte de performance. Dans de très rares cas où vous avez mesuré un impact, vous avez d’autres moyens de garantir statiquement qu’un down‑cast réussira (p. ex. CRTP soigneusement employé) et aucune héritage virtuel impliquée, envisagez d’utiliser `static_cast` avec un commentaire proéminent et un avertissement résumant ce paragraphe, précisant que l’attention humaine est requise car le système de type ne peut pas vérifier la correction.

##### Exception  

Considérez :

```    
    template<typename B>
    class Dx : B {
        // …
    };
```  

##### Application  

* Signaler tous les usages de `static_cast` pour les down‑casts, y compris les casts de style C.  
* Cette règle fait partie du [profil type‑safety](022-profile.md#pro-type-downcast) @TODO-LINK.

### <a name="rh-ref-cast"></a>C.147 : Utiliser `dynamic_cast` vers un type référence lorsque l’échec à trouver la classe requise est considéré comme une erreur

##### Raison  

Caster en référence indique que vous avez l’intention d’obtenir un objet valide, donc le cast doit réussir. `dynamic_cast` lèvera alors une exception si le cast échoue.

##### Exemple  

```    
    std::string f(Base& b)
    {
        return dynamic_cast<Derived&>(b).to_string();
    }
```  

##### Application  

??? (non‑enforcable)

### <a name="rh-ptr-cast"></a>C.148 : Utiliser `dynamic_cast` vers un type pointeur lorsque l’échec à trouver la classe requise est considéré comme une alternative valide

##### Raison  

La conversion `dynamic_cast` permet de tester si un pointeur pointe vers un objet polymorphe possédant une classe donnée dans sa hiérarchie. Un échec (conversion renvoie `nullptr`) peut être testé à l’exécution, permettant d’écrire du code qui choisit des chemins alternatifs selon le résultat.

Contrairement à [C.147](007-class.md#rh-ref-cast) où l’échec est une erreur, ici l’échec constitue simplement une alternative.

##### Exemple  

L’exemple suivant décrit la fonction `add` d’un `Shape_owner` qui prend la possession d’objets `Shape` construits. Les objets sont également classés dans des vues selon leurs attributs géométriques. Dans cet exemple, `Shape` ne dérive pas de `Geometric_attributes`. Seules ses sous‑classes le font.

```    
    void add(Shape* const item)
    {
        // La possession est toujours prise
        owned_shapes.emplace_back(item);

        // Vérifier les attributs géométriques et ajouter la forme aux vues appropriées

        if (auto even = dynamic_cast<Even_sided*>(item))
        {
            view_of_evens.emplace_back(even);
        }

        if (auto trisym = dynamic_cast<Trilaterally_symmetrical*>(item))
        {
            view_of_trisyms.emplace_back(trisym);
        }
    }
```  

##### Exemple, bon  

```    
    // Corrigé : simplement déclarer a avant b

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

##### Remarque  

Un échec de `dynamic_cast` vers un pointeur retourne `nullptr`. Déférencer un pointeur nul conduit à un comportement indéfini. Ainsi, le résultat du `dynamic_cast` doit toujours être testé comme pouvant être nul, et le test doit être effectué.

##### Application  

* (Complexe) Si aucun test `null` n’est présent après un `dynamic_cast` d’un pointeur, avertir lors de la déréférencement du pointeur.

### <a name="rh-smart"></a>C.149 : Utiliser `unique_ptr` ou `shared_ptr` pour éviter d’oublier de `delete` les objets créés avec `new`

##### Raison  

Éviter les fuites de ressources.

##### Exemple  

```    
    void use(int i)
    {
        auto p = new int {7};           // mauvais : initialiser des pointeurs locaux avec new
        auto q = make_unique<int>(9);   // ok : garantit la libération de la mémoire allouée pour 9
        if (0 < i) return;              // peut‑être retourner et fuir
        delete p;                       // trop tard
    }
```  

##### Application  

* Signaler l’initialisation d’un pointeur nu avec le résultat de `new`.  
* Signaler un `delete` d’une variable locale.

### <a name="rh-make_unique"></a>C.150 : Utiliser `make_unique()` pour construire des objets possédés par des `unique_ptr`s

Voir [R.23](009-resource.md#rr-make_unique) @TODO-LINK.

### <a name="rh-make_shared"></a>C.151 : Utiliser `make_shared()` pour construire des objets possédés par des `shared_ptr`s

Voir [R.22](009-resource.md#rr-make_shared) @TODO-LINK.

### <a name="rh-array"></a>C.152 : Ne jamais affecter un pointeur vers un tableau d’objets dérivés à un pointeur vers sa base

##### Raison  

Le sous‑scriptage du pointeur base conduit à un accès invalide et très probablement à une corruption mémoire.

##### Exemple  

```    
    struct B { int x; };
    struct D : B { int y; };

    void use(B*);

    D a[] = { {1, 2}, {3, 4}, {5, 6} };
    B* p = a;     // mauvais : a se dégrade en &a[0] qui est converti en B*
    p[1].x = 7;   // écrase a[0].y
    use(a);       // mauvais : a se dégrade en &a[0] qui est converti en B*
```  

##### Application  

* Signaler toutes les combinaisons de déc

```    
* Signaler toutes les combinaisons de déc

* Signaler toutes les combinaisons de déc

* ??? (à compléter)

```

### <a name="rh-use-virtual"></a>C.153 : Privilégier la fonction virtuelle au cast

##### Raison  

Un appel de fonction virtuelle est sûr, alors qu’un cast est source d’erreurs. Un appel virtuel atteint la fonction la plus dérivée, alors qu’un cast pourrait atteindre une classe intermédiaire et donner un résultat erroné (surtout lorsque la hiérarchie évolue).

##### Exemple  

???

##### Application  

Voir [C.146](007-class.md#rh-dynamic_cast) @TODO-LINK et ???

---

## <a name="ss-overload"></a>C.over : Surcharge et opérateurs surchargés

Vous pouvez surcharger des fonctions ordinaires, des modèles de fonction et des opérateurs. Vous ne pouvez pas surcharger les objets fonctionnels.

**Résumé des règles de surcharge :**

* [C.160 : Définir les opérateurs principalement pour imiter l’usage conventionnel](007-class.md#ro-conventional) @TODO-LINK
* [C.161 : Utiliser des fonctions non‑membres pour les opérateurs symétriques](007-class.md#ro-symmetric) @TODO-LINK
* [C.162 : Surcharger les opérations qui sont à peu près équivalentes](007-class.md#ro-equivalent) @TODO-LINK
* [C.163 : Surcharger uniquement les opérations qui sont à peu

``` (the rest is omitted) ```
```