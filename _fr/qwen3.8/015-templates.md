# <a name="s-templates"></a>T : Modèles et programmation générique

La programmation générique consiste à programmer en utilisant des types et des algorithmes paramétrés par des types, des valeurs et des algorithmes.
En C++, la programmation générique est prise en charge par les mécanismes de langage `template`.

Les arguments des fonctions génériques sont caractérisés par des ensembles d'exigences sur les types et les valeurs des arguments impliqués.
En C++, ces exigences sont exprimées par des prédicats de temps de compilation appelés concepts.

Les modèles peuvent également être utilisés pour la métaprogrammation, c'est-à-dire des programmes qui composent du code au moment de la compilation.

Une notion centrale en programmation générique est celle de « concepts » ; c'est-à-dire des exigences sur les arguments de modèle présentées sous forme de prédicats de temps de compilation.
Les « concepts » ont été normalisés en C++20, bien qu'ils aient d'abord été rendus disponibles, avec une syntaxe légèrement différente, dans GCC 6.1.

Résumé des règles d'utilisation des modèles :

* [T.1 : Utiliser les modèles pour élever le niveau d'abstraction du code](015-templates.md#rt-raise)
* [T.2 : Utiliser les modèles pour exprimer des algorithmes applicables à de nombreux types d'arguments](015-templates.md#rt-algo)
* [T.3 : Utiliser les modèles pour exprimer des conteneurs et des plages](015-templates.md#rt-cont)
* [T.4 : Utiliser les modèles pour exprimer la manipulation d'arbres syntaxiques](015-templates.md#rt-expr)
* [T.5 : Combiner les techniques génériques et OO pour amplifier leurs forces, non leurs coûts](015-templates.md#rt-generic-oo)

Résumé des règles d'utilisation des concepts :

* [T.10 : Spécifier des concepts pour tous les arguments de modèle](015-templates.md#rt-concepts)
* [T.11 : Utiliser les concepts standard dès que possible](015-templates.md#rt-std-concepts)
* [T.12 : Préférer les noms de concepts à `auto` pour les variables locales](015-templates.md#rt-auto)
* [T.13 : Préférer la notation abrégée pour les concepts simples à un seul argument de type](015-templates.md#rt-shorthand)
* ???

Résumé des règles de définition des concepts :

* [T.20 : Éviter les « concepts » sans sémantique significative](015-templates.md#rt-low)
* [T.21 : Exiger un ensemble complet d'opérations pour un concept](015-templates.md#rt-complete)
* [T.22 : Spécifier des axiomes pour les concepts](015-templates.md#rt-axiom)
* [T.23 : Différencier un concept raffiné de son cas plus général en ajoutant de nouveaux motifs d'utilisation](015-templates.md#rt-refine)
* [T.24 : Utiliser des classes d'étiquette ou des traits pour différencier des concepts qui ne diffèrent que par leur sémantique](015-templates.md#rt-tag)
* [T.25 : Éviter les contraintes complémentaires](015-templates.md#rt-not)
* [T.26 : Préférer de définir les concepts en termes de motifs d'utilisation plutôt que de simple syntaxe](015-templates.md#rt-use)
* [T.30 : Utiliser la négation de concept (`!C<T>`) avec parcimonie pour exprimer une différence mineure](#rt-??? @TODO-LINK)
* [T.31 : Utiliser la disjonction de concepts (`C1<T> || C2<T>`) avec parcimonie pour exprimer des alternatives](#rt-??? @TODO-LINK)
* ???

Résumé des règles d'interface des modèles :

* [T.40 : Utiliser des objets de fonction pour passer des opérations aux algorithmes](015-templates.md#rt-fo)
* [T.41 : Exiger uniquement les propriétés essentielles dans les concepts d'un modèle](015-templates.md#rt-essential)
* [T.42 : Utiliser des alias de modèle pour simplifier la notation et masquer les détails d'implémentation](015-templates.md#rt-alias)
* [T.43 : Préférer `using` à `typedef` pour définir des alias](015-templates.md#rt-using)
* [T.44 : Utiliser des modèles de fonction pour déduire les types d'arguments de modèles de classe (lorsque c'est faisable)](015-templates.md#rt-deduce)
* [T.46 : (supprimée)](015-templates.md#rt-regular)
* [T.47 : Éviter les modèles non contraints très visibles portant des noms courants](015-templates.md#rt-visible)
* [T.48 : Si votre compilateur ne prend pas en charge les concepts, les simuler avec `enable_if`](015-templates.md#rt-concept-def)
* [T.49 : Éviter l'effacement de type lorsque c'est possible](015-templates.md#rt-erasure)

Résumé des règles de définition des modèles :

* [T.60 : Minimiser les dépendances contextuelles d'un modèle](015-templates.md#rt-depend)
* [T.61 : Ne pas sur-paramétrer les membres (SCARY)](015-templates.md#rt-scary)
* [T.62 : Placer les membres non dépendants d'un modèle de classe dans une classe de base non paramétrée](015-templates.md#rt-nondependent)
* [T.64 : Utiliser la spécialisation pour fournir des implémentations alternatives de modèles de classe](015-templates.md#rt-specialization)
* [T.65 : Utiliser le dépêchage par étiquette pour fournir des implémentations alternatives de fonctions](015-templates.md#rt-tag-dispatch)
* [T.67 : Utiliser la spécialisation pour fournir des implémentations alternatives pour des types irréguliers](015-templates.md#rt-specialization2)
* [T.68 : Utiliser `{}` plutôt que `()` dans les modèles pour éviter les ambiguïtés](015-templates.md#rt-cast)
* [T.69 : Dans un modèle, ne pas effectuer d'appel non qualifié d'une fonction non membre à moins de vouloir en faire un point de personnalisation](015-templates.md#rt-customization)

Résumé des règles sur les modèles et les hiérarchies :

* [T.80 : Ne pas paramétrer naïvement une hiérarchie de classes](015-templates.md#rt-hier)
* [T.81 : Ne pas mélanger hiérarchies et tableaux](015-templates.md#rt-array) // ??? quelque part dans « hiérarchies »
* [T.82 : Linéariser une hiérarchie lorsque les fonctions virtuelles sont indésirables](015-templates.md#rt-linear)
* [T.83 : Ne pas déclarer une fonction membre modèle comme virtuelle](015-templates.md#rt-virtual)
* [T.84 : Utiliser une implémentation de base non paramétrée pour fournir une interface ABI-stable](015-templates.md#rt-abi)
* [T.??: ????](#rt-??? @TODO-LINK)

Résumé des règles sur les modèles variadiques :

* [T.100 : Utiliser les modèles variadiques lorsque vous avez besoin d'une fonction acceptant un nombre variable d'arguments de types variés](015-templates.md#rt-variadic)
* [T.101 : ??? Comment passer des arguments à un modèle variadique ???](015-templates.md#rt-variadic-pass)
* [T.102 : ??? Comment traiter les arguments d'un modèle variadique ???](015-templates.md#rt-variadic-process)
* [T.103 : Ne pas utiliser les modèles variadiques pour des listes d'arguments homogènes](015-templates.md#rt-variadic-not)
* [T.??: ????](#rt-??? @TODO-LINK)

Résumé des règles de métaprogrammation :

* [T.120 : N'utiliser la métaprogrammation par modèles que lorsque c'est vraiment nécessaire](015-templates.md#rt-metameta)
* [T.121 : Utiliser la métaprogrammation par modèles principalement pour émuler les concepts](015-templates.md#rt-emulate)
* [T.122 : Utiliser des modèles (généralement des alias de modèle) pour calculer des types au moment de la compilation](015-templates.md#rt-tmp)
* [T.123 : Utiliser des fonctions `constexpr` pour calculer des valeurs au moment de la compilation](015-templates.md#rt-fct)
* [T.124 : Préférer d'utiliser les installations TMP de la bibliothèque standard](015-templates.md#rt-std-tmp)
* [T.125 : Si vous devez aller au-delà des installations TMP de la bibliothèque standard, utiliser une bibliothèque existante](015-templates.md#rt-lib)
* [T.??: ????](#rt-??? @TODO-LINK)

Résumé des autres règles sur les modèles :

* [T.140 : Si une opération peut être réutilisée, lui donner un nom](015-templates.md#rt-name)
* [T.141 : Utiliser une lambda anonyme si vous avez besoin d'un simple objet de fonction en un seul endroit](015-templates.md#rt-lambda)
* [T.142 : Utiliser des variables de modèle pour simplifier la notation](015-templates.md#rt-var)
* [T.143 : Ne pas écrire de code non générique involontairement](015-templates.md#rt-non-generic)
* [T.144 : Ne pas spécialiser des modèles de fonction](015-templates.md#rt-specialize-function)
* [T.150 : Vérifier qu'une classe satisfait un concept à l'aide de `static_assert`](015-templates.md#rt-check-class)
* [T.??: ????](#rt-??? @TODO-LINK)

## <a name="ss-gp"></a>T.gp : Programmation générique

La programmation générique consiste à programmer en utilisant des types et des algorithmes paramétrés par des types, des valeurs et des algorithmes.

### <a name="rt-raise"></a>T.1 : Utiliser les modèles pour élever le niveau d'abstraction du code

##### Raison

Généralité. Réutilisation. Efficacité. Encourage une définition cohérente des types utilisateur.

##### Exemple, mauvais

Conceptuellement, les exigences suivantes sont incorrectes car ce que nous attendons de `T` est plus que les simples concepts de bas niveau « peut être incrémenté » ou « peut être additionné » :

    template<typename T>
        requires Incrementable<T>
    T sum1(vector<T>& v, T s)
    {
        for (auto x : v) s += x;
        return s;
    }

    template<typename T>
        requires Simple_number<T>
    T sum2(vector<T>& v, T s)
    {
        for (auto x : v) s = s + x;
        return s;
    }

En supposant que `Incrementable` ne prend pas en charge `+` et que `Simple_number` ne prend pas en charge `+=`, nous avons surdéterminé les implémenteurs de `sum1` et `sum2`.
Et, dans ce cas, nous avons manqué une opportunité de généralisation.

##### Exemple

    template<typename T>
        requires Arithmetic<T>
    T sum(vector<T>& v, T s)
    {
        for (auto x : v) s += x;
        return s;
    }

En supposant que `Arithmetic` exige à la fois `+` et `+=`, nous avons contraint l'utilisateur de `sum` à fournir un type arithmétique complet.
Ce n'est pas une exigence minimale, mais cela donne à l'implémenteur d'algorithmes une liberté très nécessaire et garantit que tout type `Arithmetic`
peut être utilisé pour une grande variété d'algorithmes.

Pour une généralité et une réutilisabilité accrues, nous pourrions également utiliser un concept plus général `Container` ou `Range` au lieu de nous limiter à un seul conteneur, `vector`.

##### Remarque

Si nous définissons un modèle exigeant exactement les opérations requises pour une seule implémentation d'un seul algorithme
(par exemple, exiger uniquement `+=` plutôt que `=` et `+` également) et rien d'autre, nous avons surdéterminé les mainteneurs.
Nous visons à minimiser les exigences sur les arguments de modèle, mais les exigences absolument minimales d'une implémentation sont rarement un concept significatif.

##### Remarque

Les modèles peuvent être utilisés pour exprimer essentiellement tout (ils sont complets de Turing), mais l'objectif de la programmation générique (telle qu'exprimée à l'aide de modèles)
est de généraliser efficacement des opérations/algorithmes sur un ensemble de types ayant des propriétés sémantiques similaires.

##### Application

* Signaler les algorithmes avec des exigences « trop simples », telles que l'utilisation directe d'opérateurs spécifiques sans concept.
* Ne pas signaler la définition des concepts « trop simples » eux-mêmes ; ils pourraient simplement être des briques de base pour des concepts plus utiles.

### <a name="rt-algo"></a>T.2 : Utiliser les modèles pour exprimer des algorithmes applicables à de nombreux types d'arguments

##### Raison

Généralité. Minimisation de la quantité de code source. Interopérabilité. Réutilisation.

##### Exemple

C'est le fondement de la STL. Un seul algorithme `find` fonctionne facilement avec n'importe quel type de plage d'entrée :

    template<typename Iter, typename Val>
        // requires Input_iterator<Iter>
        //       && Equality_comparable<Value_type<Iter>, Val>
    Iter find(Iter b, Iter e, Val v)
    {
        // ...
    }

##### Remarque

N'utiliser un modèle que si vous avez un besoin réaliste de plus d'un type d'argument de modèle.
Ne pas sur-abstraire.

##### Application

??? difficile, probablement besoin d'un humain

### <a name="rt-cont"></a>T.3 : Utiliser les modèles pour exprimer des conteneurs et des plages

##### Raison

Les conteneurs ont besoin d'un type d'élément, et l'exprimer comme argument de modèle est général, réutilisable et sûr du point de vue des types.
Cela évite également des contournements fragiles ou inefficaces. Convention : c'est ainsi que la STL le fait.

##### Exemple

    template<typename T>
        // requires Regular<T>
    class Vector {
        // ...
        T* elem;   // pointe vers sz Ts
        int sz;
    };

    Vector<double> v(10);
    v[7] = 9.9;

##### Exemple, mauvais

    class Container {
        // ...
        void* elem;   // pointe vers size éléments d'un certain type
        int sz;
    };

    Container c(10, sizeof(double));
    ((double*) c.elem)[7] = 9.9;

Cela n'exprime pas directement l'intention du programmeur et masque la structure du programme au système de types et à l'optimiseur.

Masquer le `void*` derrière des macros obscurcit simplement les problèmes et introduit de nouvelles possibilités de confusion.

**Exceptions** : Si vous avez besoin d'une interface ABI-stable, vous pourriez devoir fournir une implémentation de base et exprimer le modèle (sûr du point de vue des types) en termes de celle-ci.
Voir [Base stable](015-templates.md#rt-abi).

##### Application

* Signaler les utilisations de `void*` et de casts en dehors du code d'implémentation de bas niveau

### <a name="rt-expr"></a>T.4 : Utiliser les modèles pour exprimer la manipulation d'arbres syntaxiques

##### Raison

 ???

##### Exemple

    ???

**Exceptions** : ???

### <a name="rt-generic-oo"></a>T.5 : Combiner les techniques génériques et OO pour amplifier leurs forces, non leurs coûts

##### Raison

Les techniques génériques et OO sont complémentaires.

##### Exemple

Le statique aide le dynamique : utiliser le polymorphisme statique pour implémenter des interfaces polymorphes dynamiques.

    class Command {
        // fonctions virtuelles pures
    };

    // implémentations
    template</*...*/>
    class ConcreteCommand : public Command {
        // implémenter les virtuelles
    };

##### Exemple

Le dynamique aide le statique : offrir une interface générique, confortable, liée statiquement, mais dépêcher dynamiquement en interne, afin d'offrir un agencement d'objets uniforme.
Des exemples incluent l'effacement de type comme avec le destructeur de `std::shared_ptr` (mais [ne pas surutiliser l'effacement de type](015-templates.md#rt-erasure)).

    #include <memory>

    class Object {
    public:
        template<typename T>
        Object(T&& obj)
            : concept_(std::make_shared<ConcreteCommand<T>>(std::forward<T>(obj))) {}

        int get_id() const { return concept_->get_id(); }

    private:
        struct Command {
            virtual ~Command() {}
            virtual int get_id() const = 0;
        };

        template<typename T>
        struct ConcreteCommand final : Command {
            ConcreteCommand(T&& obj) noexcept : object_(std::forward<T>(obj)) {}
            int get_id() const final { return object_.get_id(); }

        private:
            T object_;
        };

        std::shared_ptr<Command> concept_;
    };

    class Bar {
    public:
        int get_id() const { return 1; }
    };

    struct Foo {
    public:
        int get_id() const { return 2; }
    };

    Object o(Bar{});
    Object o2(Foo{});

##### Remarque

Dans un modèle de classe, les fonctions non virtuelles ne sont instanciées que si elles sont utilisées — mais les fonctions virtuelles sont instanciées à chaque fois.
Cela peut gonfler la taille du code et peut surdéterminer un type générique en instanciant des fonctionnalités qui ne sont jamais nécessaires.
Éviter cela, même si les facettes de la bibliothèque standard ont fait cette erreur.

##### Voir aussi

* réf ???
* réf ???
* réf ???

##### Application

Voir la référence vers des règles plus spécifiques.

## <a name="ss-concepts"></a>T.concepts : Règles sur les concepts

Les concepts sont une installation C++20 pour spécifier des exigences sur les arguments de modèle.
Ils sont cruciaux dans la réflexion sur la programmation générique et constituent la base de nombreux travaux sur les futures bibliothèques C++
(standard et autres).

Cette section suppose la prise en charge des concepts.

Résumé des règles d'utilisation des concepts :

* [T.10 : Spécifier des concepts pour tous les arguments de modèle](015-templates.md#rt-concepts)
* [T.11 : Utiliser les concepts standard dès que possible](015-templates.md#rt-std-concepts)
* [T.12 : Préférer les noms de concepts à `auto`](015-templates.md#rt-auto)
* [T.13 : Préférer la notation abrégée pour les concepts simples à un seul argument de type](015-templates.md#rt-shorthand)
* ???

Résumé des règles de définition des concepts :

* [T.20 : Éviter les « concepts » sans sémantique significative](015-templates.md#rt-low)
* [T.21 : Exiger un ensemble complet d'opérations pour un concept](015-templates.md#rt-complete)
* [T.22 : Spécifier des axiomes pour les concepts](015-templates.md#rt-axiom)
* [T.23 : Différencier un concept raffiné de son cas plus général en ajoutant de nouveaux motifs d'utilisation](015-templates.md#rt-refine)
* [T.24 : Utiliser des classes d'étiquette ou des traits pour différencier des concepts qui ne diffèrent que par leur sémantique](015-templates.md#rt-tag)
* [T.25 : Éviter les contraintes complémentaires](015-templates.md#rt-not)
* [T.26 : Préférer de définir les concepts en termes de motifs d'utilisation plutôt que de simple syntaxe](015-templates.md#rt-use)
* ???

## <a name="ss-concept-use"></a>T.con-use : Utilisation des concepts

### <a name="rt-concepts"></a>T.10 : Spécifier des concepts pour tous les arguments de modèle

##### Raison

Correctitude et lisibilité.
Le sens supposé (syntaxe et sémantique) d'un argument de modèle est fondamental pour l'interface d'un modèle.
Un concept améliore considérablement la documentation et la gestion des erreurs du modèle.
Spécifier des concepts pour les arguments de modèle est un puissant outil de conception.

##### Exemple

    template<typename Iter, typename Val>
        requires input_iterator<Iter>
                 && equality_comparable_with<iter_value_t<Iter>, Val>
    Iter find(Iter b, Iter e, Val v)
    {
        // ...
    }

ou de manière équivalente et plus concise :

    template<input_iterator Iter, typename Val>
        requires equality_comparable_with<iter_value_t<Iter>, Val>
    Iter find(Iter b, Iter e, Val v)
    {
        // ...
    }

##### Remarque

Un simple `typename` (ou `auto`) est le concept le moins contraignant.
Il ne devrait être utilisé que rarement lorsque rien de plus que « c'est un type » ne peut être supposé.
Cela n'est généralement nécessaire que lorsque (dans le cadre d'un code de métaprogrammation par modèles) nous manipulons des arbres d'expressions purs, en reportant la vérification des types.

**Références** : TC++PL4

##### Application

Signaler les arguments de type de modèle sans concepts

### <a name="rt-std-concepts"></a>T.11 : Utiliser les concepts standard dès que possible

##### Raison

Les concepts « standard » (tels que fournis par la [GSL](#gsl-guidelines-support-library @TODO-LINK) et la norme ISO elle-même)
nous épargnent le travail d'inventer nos propres concepts, sont mieux réfléchis que nous ne pourrions le faire à la hâte, et améliorent l'interopérabilité.

##### Remarque

À moins de créer une nouvelle bibliothèque générique, la plupart des concepts dont vous avez besoin seront déjà définis par la bibliothèque standard.

##### Exemple

    template<typename T>
        // ne pas définir ceci : sortable est dans <iterator>
    concept Ordered_container = Sequence<T> && Random_access<Iterator<T>> && Ordered<Value_type<T>>;

    void sort(Ordered_container auto& s);

Ce `Ordered_container` est tout à fait plausible, mais il est très similaire au concept `sortable` de la bibliothèque standard.
Est-il meilleur ? Est-il correct ? Reflète-t-il fidèlement les exigences de la norme pour `sort` ?
Il est meilleur et plus simple d'utiliser simplement `sortable` :

    void sort(sortable auto& s);   // meilleur

##### Remarque

L'ensemble des concepts « standard » évolue à mesure que nous approchons d'une norme ISO incluant les concepts.

##### Remarque

Concevoir un concept utile est un défi.

##### Application

Difficile.

* Rechercher des arguments non contraints, des modèles utilisant des concepts « inhabituels »/non standard, des modèles utilisant des concepts « maison » sans axiomes.
* Développer un outil de découverte de concepts (par exemple, voir [une expérience précoce](https://www.stroustrup.com/sle2010_webversion.pdf)).

### <a name="rt-auto"></a>T.12 : Préférer les noms de concepts à `auto` pour les variables locales

##### Raison

`auto` est le concept le plus faible. Les noms de concepts transmettent plus de sens que simplement `auto`.

##### Exemple

    vector<string> v{ "abc", "xyz" };
    auto& x = v.front();        // mauvais
    String auto& s = v.front(); // bon (String est un concept GSL)

##### Application

* ???

### <a name="rt-shorthand"></a>T.13 : Préférer la notation abrégée pour les concepts simples à un seul argument de type

##### Raison

Lisibilité. Expression directe d'une idée.

##### Exemple

Pour dire « `T` est `sortable` » :

    template<typename T>       // Correct mais verbeux : « Le paramètre est
        requires sortable<T>   // de type T qui est le nom d'un type
    void sort(T&);             // qui est sortable »

    template<sortable T>       // Meilleur : « Le paramètre est de type T
    void sort(T&);             // qui est Sortable »

    void sort(sortable auto&); // Le meilleur : « Le paramètre est Sortable »

Les versions plus courtes correspondent mieux à la façon dont nous parlons. Notez que de nombreux modèles n'ont pas besoin d'utiliser le mot-clé `template`.

##### Application

* Non réalisable à court terme lorsque les gens convertissent depuis la notation `<typename T>` et `<class T>`.
* Plus tard, signaler les déclarations qui introduisent d'abord un typename puis le contraignent avec un concept simple à un seul argument de type.

## <a name="ss-concepts-def"></a>T.concepts.def : Règles de définition des concepts

Définir de bons concepts n'est pas trivial.
Les concepts sont censés représenter des notions fondamentales dans un domaine d'application (d'où le nom « concepts »).
De même, assembler un ensemble de contraintes syntaxiques à utiliser pour les arguments d'une seule classe ou d'un seul algorithme n'est pas ce pour quoi les concepts ont été conçus
et ne donnera pas les avantages complets du mécanisme.

Évidemment, définir des concepts est le plus utile pour du code pouvant utiliser une implémentation (par exemple, C++20 ou ultérieur),
mais définir des concepts est en soi une technique de conception utile et aide à détecter des erreurs conceptuelles et à nettoyer les concepts (sic !) d'une implémentation.

### <a name="rt-low"></a>T.20 : Éviter les « concepts » sans sémantique significative

##### Raison

Les concepts sont censés exprimer des notions sémantiques, telles que « un nombre », « une plage » d'éléments, et « totalement ordonné ».
Des contraintes simples, telles que « a un opérateur `+` » et « a un opérateur `>` » ne peuvent pas être spécifiées de manière significative de façon isolée
et ne devraient être utilisées que comme briques de base pour des concepts significatifs, plutôt que dans le code utilisateur.

##### Exemple, mauvais

    template<typename T>
    // mauvais ; insuffisant
    concept Addable = requires(T a, T b) { a + b; };

    template<Addable N>
    auto algo(const N& a, const N& b) // utiliser deux nombres
    {
        // ...
        return a + b;
    }

    int x = 7;
    int y = 9;
    auto z = algo(x, y);   // z = 16

    string xx = "7";
    string yy = "9";
    auto zz = algo(xx, yy);   // zz = "79"

Peut-être que la concaténation était attendue. Plus probablement, c'était un accident. Définir la soustraction de manière équivalente donnerait des ensembles de types acceptés radicalement différents.
Ce `Addable` viole la règle mathématique selon laquelle l'addition est censée être commutative : `a+b == b+a`.

##### Remarque

La capacité à spécifier une sémantique significative est une caractéristique définissante d'un véritable concept, par opposition à une contrainte syntaxique.

##### Exemple

    template<typename T>
    // Les opérateurs +, -, *, et / pour un nombre sont supposés suivre les règles mathématiques usuelles
    concept Number = requires(T a, T b) { a + b; a - b; a * b; a / b; };

    template<Number N>
    auto algo(const N& a, const N& b)
    {
        // ...
        return a + b;
    }

    int x = 7;
    int y = 9;
    auto z = algo(x, y);   // z = 16

    string xx = "7";
    string yy = "9";
    auto zz = algo(xx, yy);   // erreur : string n'est pas un Number

##### Remarque

Les concepts avec plusieurs opérations ont beaucoup moins de chances de correspondre accidentellement à un type qu'un concept à une seule opération.

##### Application

* Signaler les `concepts` à une seule opération lorsqu'ils sont utilisés en dehors de la définition d'autres `concepts`.
* Signaler les utilisations de `enable_if` qui semblent simuler des `concepts` à une seule opération.


### <a name="rt-complete"></a>T.21 : Exiger un ensemble complet d'opérations pour un concept

##### Raison

Facilité de compréhension.
Interopérabilité améliorée.
Aide les implémenteurs et les mainteneurs.

##### Remarque

C'est une variante spécifique de la règle générale selon laquelle [un concept doit avoir un sens sémantique](015-templates.md#rt-low).

##### Exemple, mauvais

    template<typename T> concept Subtractable = requires(T a, T b) { a - b; };

Cela n'a pas de sens sémantique.
Il faut au moins `+` pour que `-` ait un sens et soit utile.

Des exemples d'ensembles complets sont :

* `Arithmetic` : `+`, `-`, `*`, `/`, `+=`, `-=`, `*=`, `/=`
* `Comparable` : `<`, `>`, `<=`, `>=`, `==`, `!=`

##### Remarque

Cette règle s'applique que nous utilisions ou non un support direct du langage pour les concepts.
C'est une règle de conception générale qui s'applique même aux non-modèles :

    class Minimal {
        // ...
    };

    bool operator==(const Minimal&, const Minimal&);
    bool operator<(const Minimal&, const Minimal&);

    Minimal operator+(const Minimal&, const Minimal&);
    // aucun autre opérateur

    void f(Minimal x, Minimal y)
    {
        if (!(x == y)) { /* ... */ }    // OK
        if (x != y) { /* ... */ }       // surprise ! erreur

        while (!(x < y)) { /* ... */ }  // OK
        while (x >= y) { /* ... */ }    // surprise ! erreur

        x = x + y;          // OK
        x += y;             // surprise ! erreur
    }

C'est minimal, mais surprenant et contraignant pour les utilisateurs.
Cela pourrait même être moins efficace.

Cette règle soutient l'idée qu'un concept doit refléter un ensemble (mathématiquement) cohérent d'opérations.

##### Exemple

    class Convenient {
        // ...
    };

    bool operator==(const Convenient&, const Convenient&);
    bool operator<(const Convenient&, const Convenient&);
    // ... et les autres opérateurs de comparaison ...

    Convenient operator+(const Convenient&, const Convenient&);
    // ... et les autres opérateurs arithmétiques ...

    void f(const Convenient& x, const Convenient& y)
    {
        if (!(x == y)) { /* ... */ }    // OK
        if (x != y) { /* ... */ }       // OK

        while (!(x < y)) { /* ... */ }  // OK
        while (x >= y) { /* ... */ }    // OK

        x = x + y;     // OK
        x += y;        // OK
    }

Cela peut être fastidieux de définir tous les opérateurs, mais ce n'est pas difficile.
Idéalement, cette règle devrait être prise en charge par le langage en fournissant les opérateurs de comparaison par défaut.

##### Application

* Signaler les classes qui supportent des sous-ensembles « inhabituels » d'un ensemble d'opérateurs, par exemple `==` mais pas `!=` ou `+` mais pas `-`.
  Oui, `std::string` est « inhabituel », mais il est trop tard pour le changer.


### <a name="rt-axiom"></a>T.22 : Spécifier des axiomes pour les concepts

##### Raison

Un concept significatif/utile a une signification sémantique.
Exprimer ces sémantiques de manière informelle, semi-formelle ou formelle rend le concept compréhensible pour les lecteurs et l'effort pour l'exprimer peut détecter des erreurs conceptuelles.
Spécifier les sémantiques est un puissant outil de conception.

##### Exemple

    template<typename T>
        // Les opérateurs +, -, *, et / pour un nombre sont supposés suivre les règles mathématiques usuelles
        // axiom(T a, T b) { a + b == b + a; a - a == 0; a * (b + c) == a * b + a * c; /*...*/ }
        concept Number = requires(T a, T b) {
            { a + b } -> convertible_to<T>;
            { a - b } -> convertible_to<T>;
            { a * b } -> convertible_to<T>;
            { a / b } -> convertible_to<T>;
        };

##### Remarque

C'est un axiome au sens mathématique : quelque chose qui peut être supposé sans preuve.
En général, les axiomes ne sont pas démontrables, et lorsqu'ils le sont, la démonstration est souvent au-delà des capacités d'un compilateur.
Un axiome peut ne pas être général, mais l'auteur du modèle peut supposer qu'il tient pour toutes les entrées réellement utilisées (similaire à une précondition).

##### Remarque

Dans ce contexte, les axiomes sont des expressions booléennes.
Voir le [TR de Palo Alto](021-references.md) pour des exemples.
Actuellement, C++ ne prend pas en charge les axiomes (même la TS Concepts ISO), nous devons donc nous contenter de commentaires pendant un certain temps.
Dès que le support du langage sera disponible, le `//` devant l'axiome pourra être retiré.

##### Remarque

Les concepts GSL ont des sémantiques bien définies ; voir le TR de Palo Alto et la TS Ranges.

##### Exception

Les premières versions d'un nouveau « concept » encore en développement définissent souvent simplement des ensembles de contraintes sans sémantique bien spécifiée.
Trouver de bonnes sémantiques peut demander des efforts et du temps.
Un ensemble incomplet de contraintes peut tout de même être très utile :

    // équilibreur pour un arbre binaire générique
    template<typename Node> concept Balancer = requires(Node* p) {
        add_fixup(p);
        touch(p);
        detach(p);
    };

Ainsi, un `Balancer` doit fournir au moins ces opérations sur un nœud `Node` d'arbre,
mais nous ne sommes pas encore prêts à spécifier des sémantiques détaillées car un nouveau type d'arbre équilibré pourrait nécessiter plus d'opérations
et les sémantiques générales précises pour tous les nœuds sont difficiles à cerner dans les premières étapes de la conception.

Un « concept » incomplet ou sans sémantique bien spécifiée peut tout de même être utile.
Par exemple, il permet certaines vérifications lors des premières expérimentations.
Cependant, il ne devrait pas être considéré comme stable.
Chaque nouveau cas d'utilisation pourrait nécessiter d'améliorer un tel concept incomplet.

##### Application

* Rechercher le mot « axiom » dans les commentaires de définition de concepts

### <a name="rt-refine"></a>T.23 : Différencier un concept raffiné de son cas plus général en ajoutant de nouveaux motifs d'utilisation.

##### Raison

Sinon, ils ne peuvent pas être distingués automatiquement par le compilateur.

##### Exemple

    template<typename I>
    // Note : input_iterator est défini dans <iterator>
    concept Input_iter = requires(I iter) { ++iter; };

    template<typename I>
    // Note : forward_iterator est défini dans <iterator>
    concept Fwd_iter = Input_iter<I> && requires(I iter) { iter++; };

Le compilateur peut déterminer le raffinement sur la base des ensembles d'opérations requises (ici, le `++` postfixe).
Cela réduit la charge sur les implémenteurs de ces types car
ils n'ont pas besoin de déclarations spéciales pour « s'ancrer dans le concept ».
Si deux concepts ont exactement les mêmes exigences, ils sont logiquement équivalents (il n'y a pas de raffinement).

##### Application

* Signaler un concept qui a exactement les mêmes exigences qu'un autre concept déjà vu (aucun n'est plus raffiné).
Pour les désambiguïser, voir [T.24](015-templates.md#rt-tag).

### <a name="rt-tag"></a>T.24 : Utiliser des classes d'étiquette ou des traits pour différencier des concepts qui ne diffèrent que par leur sémantique.

##### Raison

Deux concepts exigeant la même syntaxe mais ayant des sémantiques différentes conduisent à l'ambiguïté à moins que le programmeur ne les différencie.

##### Exemple

    template<typename I>    // itérateur fournissant un accès aléatoire
    // Note : random_access_iterator est défini dans <iterator>
    concept RA_iter = ...;

    template<typename I>    // itérateur fournissant un accès aléatoire à des données contiguës
    // Note : contiguous_iterator est défini dans <iterator>
    concept Contiguous_iter =
        RA_iter<I> && is_contiguous_v<I>;  // en utilisant le trait is_contiguous

Le programmeur (dans une bibliothèque) doit définir `is_contiguous` (un trait) de manière appropriée.

Envelopper une classe d'étiquette dans un concept conduit à une expression plus simple de cette idée :

    template<typename I> concept Contiguous = is_contiguous_v<I>;

    template<typename I>
    concept Contiguous_iter = RA_iter<I> && Contiguous<I>;

Le programmeur (dans une bibliothèque) doit définir `is_contiguous` (un trait) de manière appropriée.

##### Remarque

Les traits peuvent être des classes de traits ou des traits de type.
Ces derniers peuvent être définis par l'utilisateur ou provenir de la bibliothèque standard.
Préférer ceux de la bibliothèque standard.

##### Application

* Le compilateur signale l'utilisation ambiguë de concepts identiques.
* Signaler la définition de concepts identiques.

### <a name="rt-not"></a>T.25 : Éviter les contraintes complémentaires

##### Raison

Clarté. Maintenabilité.
Les fonctions avec des exigences complémentaires exprimées par négation sont fragiles.

##### Exemple

Au début, les gens essaieront de définir des fonctions avec des exigences complémentaires :

    template<typename T>
        requires !C<T>    // mauvais
    void f();

    template<typename T>
        requires C<T>
    void f();

Ceci est meilleur :

    template<typename T>   // modèle général
        void f();

    template<typename T>   // spécialisation par concept
        requires C<T>
    void f();

Le compilateur choisira le modèle non contraint uniquement lorsque `C<T>` n'est
pas satisfait. Si vous ne voulez pas (ou ne pouvez pas) définir une version non contrainte
de `f()`, alors supprimez-la.

    template<typename T>
    void f() = delete;

Le compilateur sélectionnera la surcharge, ou émettra une erreur appropriée.

##### Remarque

Les contraintes complémentaires sont malheureusement courantes dans le code `enable_if` :

    template<typename T>
    enable_if<!C<T>, void>   // mauvais
    f();

    template<typename T>
    enable_if<C<T>, void>
    f();


##### Remarque

Les exigences complémentaires sur une seule exigence sont parfois (à tort) considérées comme gérables.
Cependant, pour deux exigences ou plus, le nombre de définitions nécessaires peut croître exponentiellement (2, 4, 8, 16, ...) :

    C1<T> && C2<T>
    !C1<T> && C2<T>
    C1<T> && !C2<T>
    !C1<T> && !C2<T>

Les possibilités d'erreurs se multiplient alors.

##### Application

* Signaler les paires de fonctions avec des contraintes `C<T>` et `!C<T>`

### <a name="rt-use"></a>T.26 : Préférer de définir les concepts en termes de motifs d'utilisation plutôt que de simple syntaxe

##### Raison

La définition est plus lisible et correspond directement à ce qu'un utilisateur doit écrire.
Les conversions sont prises en compte. Vous n'avez pas à mémoriser les noms de tous les traits de type.

##### Exemple

Vous pourriez être tenté de définir un concept `Equality` comme ceci :

    template<typename T> concept Equality = has_equal<T> && has_not_equal<T>;

Évidemment, il serait meilleur et plus simple d'utiliser simplement `equality_comparable` standard,
mais — à titre d'exemple — si vous deviez définir un tel concept, préférez :

    template<typename T> concept Equality = requires(T a, T b) {
        { a == b } -> std::convertible_to<bool>;
        { a != b } -> std::convertible_to<bool>;
        // axiom { !(a == b) == (a != b) }
        // axiom { a = b; => a == b }  // => signifie « implique »
    };

plutôt que de définir deux concepts sans sens `has_equal` et `has_not_equal` simplement comme aides dans la définition de `Equality`.
Par « sans sens », nous entendons que nous ne pouvons pas spécifier la sémantique de `has_equal` de façon isolée.

##### Application

???

## <a name="ss-temp-interface"></a>Interfaces de modèles

Au fil des années, la programmation avec des modèles a souffert d'une distinction faible entre l'interface d'un modèle
et son implémentation.
Avant les concepts, cette distinction n'avait pas de support direct dans le langage.
Cependant, l'interface d'un modèle est un concept critique — un contrat entre un utilisateur et un implémenteur — et devrait être soigneusement conçue.

### <a name="rt-fo"></a>T.40 : Utiliser des objets de fonction pour passer des opérations aux algorithmes

##### Raison

Les objets de fonction peuvent transporter plus d'informations à travers une interface qu'un simple pointeur vers fonction.
En général, passer des objets de fonction donne de meilleures performances que passer des pointeurs vers fonctions.

##### Exemple

    bool greater(double x, double y) { return x > y; }
    sort(v, greater);                                    // pointeur vers fonction : potentiellement lent
    sort(v, [](double x, double y) { return x > y; });   // objet de fonction
    sort(v, std::greater{});                             // objet de fonction

    bool greater_than_7(double x) { return x > 7; }
    auto x = find_if(v, greater_than_7);                 // pointeur vers fonction : inflexible
    auto y = find_if(v, [](double x) { return x > 7; }); // objet de fonction : transporte les données nécessaires
    auto z = find_if(v, Greater_than<double>(7));        // objet de fonction : transporte les données nécessaires

Bien sûr, vous pouvez généraliser ces fonctions en utilisant `auto` ou des concepts. Par exemple :

    auto y1 = find_if(v, [](totally_ordered auto x) { return x > 7; }); // exiger un type ordonné
    auto z1 = find_if(v, [](auto x) { return x > 7; });                 // espérer que le type a un >

##### Remarque

Les lambdas génèrent des objets de fonction.

##### Remarque

L'argument de performances dépend de la technologie du compilateur et de l'optimiseur.

##### Application

* Signaler les arguments de modèle pointeur vers fonction.
* Signaler les pointeurs vers fonctions passés comme arguments à un modèle (risque de faux positifs).


### <a name="rt-essential"></a>T.41 : Exiger uniquement les propriétés essentielles dans les concepts d'un modèle

##### Raison

Garder les interfaces simples et stables.

##### Exemple

Considérons un `sort` instrumenté avec un support de débogage simple (simplifié) :

    void sort(sortable auto& s)  // trier la séquence s
    {
        if (debug) cerr << "enter sort( " << s <<  ")\n";
        // ...
        if (debug) cerr << "exit sort( " << s <<  ")\n";
    }

Devrait-on le réécrire ainsi :

    template<sortable S>
        requires Streamable<S>
    void sort(S& s)  // trier la séquence s
    {
        if (debug) cerr << "enter sort( " << s <<  ")\n";
        // ...
        if (debug) cerr << "exit sort( " << s <<  ")\n";
    }

Après tout, rien dans `sortable` n'exige le support `iostream`.
D'un autre côté, rien dans l'idée fondamentale du tri ne dit quoi que ce soit sur le débogage.

##### Remarque

Si nous exigeons que chaque opération utilisée soit listée parmi les exigences, l'interface devient instable :
Chaque fois que nous changeons les installations de débogage, la collecte de données d'utilisation, le support de test, la signalisation d'erreurs, etc.,
la définition du modèle devrait changer et chaque utilisation du modèle devrait être re-compilée.
C'est fastidieux, et dans certains environnements infeasible.

Inversement, si nous utilisons une opération dans l'implémentation qui n'est pas garantie par la vérification de concepts,
nous pourrions obtenir une erreur tardive au moment de la compilation.

En n'utilisant pas la vérification de concepts pour les propriétés d'un argument de modèle qui ne sont pas considérées comme essentielles,
nous reportons la vérification au moment de l'instanciation.
Nous considérons cela comme un compromis judicieux.

Notez que l'utilisation de noms non locaux et non dépendants (tels que `debug` et `cerr`) introduit également des dépendances contextuelles qui peuvent conduire à des erreurs « mystérieuses ».

##### Remarque

Il peut être difficile de décider quelles propriétés d'un type sont essentielles et lesquelles ne le sont pas.

##### Application

???

### <a name="rt-alias"></a>T.42 : Utiliser des alias de modèle pour simplifier la notation et masquer les détails d'implémentation

##### Raison

Lisibilité améliorée.
Masquage de l'implémentation.
Notez que les alias de modèle remplacent de nombreuses utilisations de traits pour calculer un type.
Ils peuvent également être utilisés pour envelopper un trait.

##### Exemple

    template<typename T, size_t N>
    class Matrix {
        // ...
        using Iterator = typename std::vector<T>::iterator;
        // ...
    };

Cela épargne à l'utilisateur de `Matrix` de savoir que ses éléments sont stockés dans un `vector` et l'épargne également de retaper `typename std::vector<T>::` à chaque fois.

##### Exemple

    template<typename T>
    void user(T& c)
    {
        // ...
        typename container_traits<T>::value_type x; // mauvais, verbeux
        // ...
    }

    template<typename T>
    using Value_type = typename container_traits<T>::value_type;


Cela épargne à l'utilisateur de `Value_type` de connaître la technique utilisée pour implémenter les `value_type`.

    template<typename T>
    void user2(T& c)
    {
        // ...
        Value_type<T> x;
        // ...
    }

##### Remarque

Une utilisation simple et courante pourrait être exprimée ainsi : « Enveloppez les traits ! »

##### Application

* Signaler l'utilisation de `typename` comme désambiguïsateur en dehors des déclarations `using`.
* ???

### <a name="rt-using"></a>T.43 : Préférer `using` à `typedef` pour définir des alias

##### Raison

Lisibilité améliorée : avec `using`, le nouveau nom vient en premier plutôt que d'être enfoui quelque part dans une déclaration.
Généralité : `using` peut être utilisé pour les alias de modèle, alors que les `typedef` ne peuvent pas facilement être des modèles.
Uniformité : `using` est syntaxiquement similaire à `auto`.

##### Exemple

    typedef int (*PFI)(int);   // OK, mais contourné

    using PFI2 = int (*)(int);   // OK, préféré

    template<typename T>
    typedef int (*PFT)(T);      // erreur

    template<typename T>
    using PFT2 = int (*)(T);   // OK

##### Application

* Signaler les utilisations de `typedef`. Cela donnera beaucoup de « hits » :-(

### <a name="rt-deduce"></a>T.44 : Utiliser des modèles de fonction pour déduire les types d'arguments de modèles de classe (lorsque c'est faisable)

##### Raison

Écrire explicitement les types d'arguments de modèle peut être fastidieux et inutilement verbeux.

##### Exemple

    tuple<int, string, double> t1 = {1, "Hamlet", 3.14};   // type explicite
    auto t2 = make_tuple(1, "Ophelia"s, 3.14);         // meilleur ; type déduit

Notez l'utilisation du suffixe `s` pour s'assurer que la chaîne est un `std::string`, plutôt qu'une chaîne au style C.

##### Remarque

Puisque vous pouvez écrire trivialement une fonction `make_T`, le compilateur pourrait le faire aussi. Ainsi, les fonctions `make_T` pourraient devenir redondantes à l'avenir.

##### Exception

Parfois, il n'y a pas de bonne façon de faire déduire les arguments de modèle et parfois, vous voulez spécifier les arguments explicitement :

    vector<double> v = { 1, 2, 3, 7.9, 15.99 };
    list<Record*> lst;

##### Remarque

Notez que C++17 rendra cette règle redondante en permettant la déduction des arguments de modèle directement depuis les arguments du constructeur :
[Déd
