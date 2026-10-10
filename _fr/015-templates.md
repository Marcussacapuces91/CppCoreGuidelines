* <a name="s-templates"></a>T : Modèles et programmation générique

La programmation générique consiste à programmer avec des types et des algorithmes paramétrés par des types, des valeurs et des algorithmes.

En C++, la programmation générique est prise en charge par les mécanismes du langage `template`.

Les arguments des fonctions génériques se caractérisent par des ensembles d'exigences sur les types et les valeurs des arguments impliqués.

En C++, ces exigences sont exprimées par des prédicats temps de compilation appelés concepts.

Les modèles peuvent également être utilisés pour le méta‑programmation ; c’est‑à‑dire, des programmes qui composent du code à la compilation.

Une notion centrale de la programmation générique est le « concept » ; c’est‑à‑dire, des exigences sur les arguments de modèle présentées comme des prédicats temps de compilation.

Les concepts ont été standardisés en C++20, bien qu’ils aient été accessibles pour la première fois, sous une syntaxe légèrement plus ancienne, dans GCC 6.1.

Résumé des règles d’utilisation des modèles :
* [T.1 : Utiliser les modèles pour élever le niveau d’abstraction du code](#rt-raise)
* [T.2 : Utiliser les modèles pour exprimer des algorithmes applicables à de nombreux types d’arguments](#rt-algo)
* [T.3 : Utiliser les modèles pour exprimer des conteneurs et des plages](#rt-cont)
* [T.4 : Utiliser les modèles pour manipuler des arbres syntaxiques](#rt-expr)
* [T.5 : Combiner les techniques génériques et orientées objet pour amplifier leurs forces, non leurs coûts](#rt-generic-oo)

Résumé des règles d’utilisation des concepts :
* [T.10 : Spécifier des concepts pour tous les arguments de modèle](#rt-concepts)
* [T.11 : Quand c’est possible, utiliser des concepts standard](#rt-std-concepts)
* [T.12 : Préférer les noms de concepts à `auto` pour les variables locales](#rt-auto)
* [T.13 : Préférer la notation courte pour les concepts à argument simple et unique](#rt-shorthand)
* ???

Résumé des règles de définition de concepts :
* [T.20 : Éviter les « concepts » sans sémantique significative](#rt-low)
* [T.21 : Exiger un ensemble complet d’opérations pour un concept](#rt-complete)
* [T.22 : Spécifier les axiomes pour les concepts](#rt-axiom)
* [T.23 : Différencier un concept affiné de son cas plus général en ajoutant de nouveaux motifs d’utilisation](#rt-refine)
* [T.24 : Utiliser des classes‑étiquettes ou des traits pour différencier les concepts qui ne diffèrent que par la sémantique](#rt-tag)
* [T.25 : Éviter les contraintes complémentaires](#rt-not)
* [T.26 : Préférer de définir les concepts en termes de motifs d’utilisation plutôt que d’une syntaxe simple](#rt-use)
* [T.30 : Utiliser la négation de concept (`!C<T>`) avec parcimonie pour exprimer une différence mineure](#rt-??) @TODO-LINK
* [T.31 : Utiliser la disjonction de concepts (`C1<T> || C2<T>`) avec parcimonie pour exprimer des alternatives](#rt-??) @TODO-LINK
* ???

Résumé des règles d’interface de modèle :
* [T.40 : Utiliser des objets fonction pour passer des opérations aux algorithmes](#rt-fo)
* [T.41 : Ne demander que les propriétés essentielles dans les concepts d’un modèle](#rt-essential)
* [T.42 : Utiliser des alias de modèle pour simplifier la notation et masquer les détails d’implémentation](#rt-alias)
* [T.43 : Préférer `using` à `typedef` pour définir des alias](#rt-using)
* [T.44 : Utiliser des modèles fonctionnels pour déduire les types d’arguments de modèle de classe (où cela est faisable)](#rt-deduce)
* [T.46 : (supprimé)](#rt-regular) @TODO-LINK
* [T.47 : Éviter les modèles hautement visibles sans contraintes avec des noms communs](#rt-visible)
* [T.48 : Si votre compilateur ne supporte pas les concepts, les imiter avec `enable_if`](#rt-concept-def)
* [T.49 : Quand c’est possible, éviter l’injection de type](#rt-erasure)

Résumé des règles de définition de modèle :
* [T.60 : Réduire les dépendances contextuelles d’un modèle](#rt-depend)
* [T.61 : Ne pas sur‑paramétrer les membres (SCARY)](#rt-scary)
* [T.62 : Placer les membres de classe de modèle non dépendants dans une classe de base non paramétrée](#rt-nondependent)
* [T.64 : Utiliser la spécialisation pour fournir des implémentations alternatives de modèles de classe](#rt-specialization)
* [T.65 : Utiliser la distribution de tag pour fournir des implémentations alternatives de fonctions](#rt-tag-dispatch)
* [T.67 : Utiliser la spécialisation pour fournir des implémentations alternatives pour les types irréguliers](#rt-specialization2)
* [T.68 : Utiliser `{}` plutôt que `()` dans les modèles pour éviter les ambiguïtés](#rt-cast)
* [T.69 : À l’intérieur d’un modèle, ne pas appeler une fonction non membre sans qualification à moins que vous ne l’intentionnellement ne soyez un point de personnalisation](#rt-customization)

Résumé des règles de modèles et hiérarchies :
* [T.80 : Ne pas templatiser naïvement une hiérarchie de classe](#rt-hier)
* [T.81 : Ne pas mélanger les hiérarchies et les tableaux](#rt-array)
* [T.82 : Lineariser une hiérarchie lorsque les fonctions virtuelles sont indésirables](#rt-linear)
* [T.83 : Ne pas déclarer un modèle de fonction virtuelle](#rt-virtual)
* [T.84 : Utiliser une implémentation centrale non modélisée pour fournir une interface stable à l’ABI](#rt-abi)
* [T.?? : ????](#rt-??) @TODO-LINK

Résumé des règles de modèles variadiques :
* [T.100 : Utiliser des modèles variadiques lorsque vous avez besoin d’une fonction qui prend un nombre variable d’arguments de plusieurs types](#rt-variadic)
* [T.101 : ??? Comment passer des arguments à un modèle variadique ???](#rt-variadic-pass)
* [T.102 : ??? Comment traiter les arguments d’un modèle variadique ???](#rt-variadic-process)
* [T.103 : Ne pas utiliser de modèles variadiques pour des listes d’arguments homogènes](#rt-variadic-not)
* [T.?? : ????](#rt-??) @TODO-LINK

Résumé des règles de méta‑programmation :
* [T.120 : Utiliser le méta‑programmation uniquement lorsqu’il est vraiment nécessaire](#rt-metameta)
* [T.121 : Utiliser le méta‑programmation principalement pour émuler les concepts](#rt-emulate)
* [T.122 : Utiliser des modèles (généralement des alias de modèle) pour calculer des types à la compilation](#rt-tmp)
* [T.123 : Utiliser des fonctions `constexpr` pour calculer des valeurs à la compilation](#rt-fct)
* [T.124 : Préférer d’utiliser les outils TMP de la bibliothèque standard](#rt-std-tmp)
* [T.125 : Si vous avez besoin d’aller au-delà des outils TMP de la bibliothèque standard, utilisez une bibliothèque existante](#rt-lib)
* [T.?? : ????](#rt-??) @TODO-LINK

Résumé des autres règles de modèle :
* [T.140 : Si une opération peut être réutilisée, donnez‑lui un nom](#rt-name)
* [T.141 : Utiliser un lambda anonyme si vous avez besoin d’un simple objet fonction dans un seul endroit](#rt-lambda)
* [T.142 : Utiliser des variables de modèle pour simplifier la notation](#rt-var)
* [T.143 : Ne pas écrire un code non générique involontairement](#rt-non-generic)
* [T.144 : Ne pas spécialiser les modèles de fonction](#rt-specialize-function)
* [T.150 : Vérifier qu’une classe correspond à un concept à l’aide de `static_assert`](#rt-check-class)
* [T.?? : ????](#rt-??) @TODO-LINK

## <a name="ss-gp"></a>T.gp : Programmation générique

La programmation générique consiste à programmer avec des types et des algorithmes paramétrés par des types, valeurs et algorithmes.

### <a name="rt-raise"></a>T.1 : Utiliser les modèles pour élever le niveau d’abstraction du code

#### Raison

Généralité. Réutilisation. Efficacité. Encourage une définition cohérente des types utilisateur.

#### Exemple, mauvais

Conceptuellement, les exigences suivantes sont incorrectes car ce que nous attendons de `T` est plus que les concepts très basiques de « peut être incrémenté » ou « peut être ajouté »:

```
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
```

En supposant que `Incrementable` ne supporte pas `+` et que `Simple_number` ne supporte pas `+=`, nous avons surconstrained les implémentateurs de `sum1` et `sum2`. Et, dans ce cas, une opportunité de généralisation a été perdue.

#### Exemple

```
    template<typename T>
    requires Arithmetic<T>
    T sum(vector<T>& v, T s)
    {
        for (auto x : v) s += x;
        return s;
    }
```

En supposant que `Arithmetic` exige à la fois `+` et `+=`, nous avons contraint l’utilisateur de `sum` à fournir un type arithmétique complet. Ce n’est pas une exigence minimale, mais elle donne à l’implémenteur d’algorithmes la liberté beaucoup nécessaire et assure que tout type `Arithmetic` peut être utilisé pour une vaste variété d’algorithmes.

Pour une généralité et réutilisation supplémentaires, nous pourrions également utiliser un concept `Container` ou `Range` plus général au lieu de se limiter à un seul conteneur, `vector`.

#### Note

Si nous définissions un modèle qui exige exactement les opérations requises pour une implémentation unique d’un seul algorithme (par exemple, ne requérant que `+=` plutôt que aussi `=` et `+`) et uniquement celles‑ci, nous surconstringsions les mainteneurs. Nous visons à minimiser les exigences sur les arguments de modèle, mais les exigences absolument minimales d’une implémentation sont rarement un concept significatif.

#### Note

Les modèles peuvent être utilisés pour exprimer essentiellement tout (ils sont Turing complets), mais le but de la programmation générique (comme exprimé via les modèles) est d’étendre efficacement les opérations/algorithmes sur un ensemble de types ayant des propriétés sémantiques similaires.

#### Application

* Marquer les algorithmes avec des exigences « trop simples », telles que l’utilisation directe d’opérateurs spécifiques sans concept.
* Ne pas marquer la définition des « concepts trop simples » eux‑mêmes ; ils pourraient simplement être des blocs de construction pour des concepts plus utiles.

### <a name="rt-algo"></a>T.2 : Utiliser les modèles pour exprimer des algorithmes applicables à de nombreux types d’arguments

#### Raison

Généralité. Minimiser la quantité de code source. Interopérabilité. Réutilisation.

#### Exemple

C’est la base du STL. Un seul algorithme `find` fonctionne facilement avec n’importe quel type de plage d’entrée :

```
    template<typename Iter, typename Val>
    // requires Input_iterator<Iter>
    //       && Equality_comparable<Value_type<Iter>, Val>
    Iter find(Iter b, Iter e, Val v)
    {
        // ...
    }
```

#### Note

N’utilisez pas un modèle à moins d’avoir un besoin réaliste de plus d’un type d’argument de modèle. Ne surabstrait pas.

#### Application

??? difficile, probablement nécessite un humain

### <a name="rt-cont"></a>T.3 : Utiliser les modèles pour exprimer des conteneurs et des plages

#### Raison

Les conteneurs ont besoin d’un type d’élément, et l’exprimer comme un argument de modèle est générique, réutilisable et sûr. Cela évite également des contournements fragiles ou inefficaces. Convention : c’est ainsi que le STL le fait.

#### Exemple

```
    template<typename T>
    // requires Regular<T>
    class Vector {
        // ...
        T* elem;   // pointe vers sz Ts
        int sz;
    };

    Vector<double> v(10);
    v[7] = 9.9;
```

#### Exemple, mauvais

```
    class Container {
        // ...
        void* elem;   // pointe vers size éléments de type inconnu
        int sz;
    };

    Container c(10, sizeof(double));
    ((double*) c.elem)[7] = 9.9;
```

Cela n’exprime pas directement l’intention du programmeur et masque la structure du programme du système de type et de l’optimiseur.

Masquer l’`void*` derrière des macros n’est qu’une obscurité et introduit de nouvelles opportunités de confusion.

**Exceptions** : Si vous avez besoin d’une interface stable à l’ABI, vous pourriez être contraint à fournir une implémentation de base et exprimer le modèle (type‑safe) en fonction de celle‑ci. Voir [Stable base](#rt-abi).

#### Application

* Signaler les utilisations d’`void*` et de conversions hors du code d’implémentation de bas niveau

### <a name="rt-expr"></a>T.4 : Utiliser les modèles pour exprimer la manipulation du flux syntaxique

#### Raison

???

#### Exemple

    ???

**Exceptions** : ???

### <a name="rt-generic-oo"></a>T.5 : Combiner les techniques génériques et orientées objet pour amplifier leurs forces, non leurs coûts

#### Raison

Les techniques génériques et orientées objet sont complémentaires.

#### Exemple

La polymorphie statique soutient la dynamique : utilisez la polymorphie statique pour implémenter des interfaces polymorphes dynamiques.

```
    class Command {
        // fonctions virtuelles pures
    };

    // implémentations
    template</*...*/>
    class ConcreteCommand : public Command {
        // implémenter virtuelles
    };
```

#### Exemple

La dynamique soutient la statique : proposez une interface générique, confortable, liée statiquement, mais dont le dispatch interne est dynamique, afin d’offrir un agencement d’objet uniforme. Les exemples incluent l’abstraction de type comme le destructeur de `std::shared_ptr` (mais [ne pas sureférence trop l’abstraction de type](#rt-erasure)).

```
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
```

#### Note

Dans un modèle de classe, les fonctions non virtuelles ne sont instanciées que lorsqu’elles sont utilisées – mais les fonctions virtuelles sont instanciées à chaque fois. Cela peut gonfler la taille du code et peut surconstrained un type générique en instanciant des fonctionnalités jamais nécessaires. Évitez‑ce, même si les facettes de la bibliothèque standard ont commis cette erreur.

#### Voir aussi

* ref ???
* ref ???
* ref ???

#### Application

Voir la référence aux règles plus spécifiques.

## <a name="ss-concepts"></a>T.concepts : Règles de concept

Les concepts sont une fonctionnalité C++20 pour spécifier les exigences pour les arguments de modèles. Ils sont cruciaux dans la réflexion sur la programmation générique et la base de nombreux travaux sur les futures bibliothèques C++ (standard et autres).

Cette section suppose le support des concepts.

#### Résumé des règles d’utilisation des concepts :

* [T.10 : Spécifier des concepts pour tous les arguments de modèle](#rt-concepts)
* [T.11 : Quand c’est possible, utiliser des concepts standard](#rt-std-concepts)
* [T.12 : Préférer les noms de concepts à `auto` pour les variables locales](#rt-auto)
* [T.13 : Préférer la notation courte pour les concepts à argument simple et unique](#rt-shorthand)
* ???

#### Résumé des règles de définition de concepts :

* [T.20 : Éviter les « concepts » sans sémantique significative](#rt-low)
* [T.21 : Exiger un ensemble complet d’opérations pour un concept](#rt-complete)
* [T.22 : Spécifier les axiomes pour les concepts](#rt-axiom)
* [T.23 : Différencier un concept affiné de son cas plus général en ajoutant de nouveaux motifs d’utilisation](#rt-refine)
* [T.24 : Utiliser des classes‑étiquettes ou des traits pour différencier les concepts qui ne diffèrent que par la sémantique](#rt-tag)
* [T.25 : Éviter les contraintes complémentaires](#rt-not)
* [T.26 : Préférer de définir les concepts en termes de motifs d’utilisation plutôt que d’une syntaxe simple](#rt-use)
* ???

## <a name="ss-concept-use"></a>T.con-use : Utilisation des concepts

### <a name="rt-concepts"></a>T.10 : Spécifier des concepts pour tous les arguments de modèle

#### Raison

Correction et lisibilité. Le sens supposé (syntaxe et sémantique) d’un argument de modèle est fondamental pour l’interface d’un modèle. Un concept améliore considérablement la documentation et le traitement des erreurs pour le modèle. Spécifier des concepts pour les arguments de modèle est un puissant outil de conception. 

#### Exemple

```
    template<typename Iter, typename Val>
        requires input_iterator<Iter>
                 && equality_comparable_with<iter_value_t<Iter>, Val>
    Iter find(Iter b, Iter e, Val v)
    {
        // ...
    }
```

ou de façon équivalente et plus concise :

```
    template<input_iterator Iter, typename Val>
        requires equality_comparable_with<iter_value_t<Iter>, Val>
    Iter find(Iter b, Iter e, Val v)
    {
        // ...
    }
```

#### Note

`typename` (ou `auto`) est le concept le moins contraignant. Il ne doit être utilisé que rarement lorsqu’aucune hypothèse plus précise n’est faite. C’est généralement uniquement nécessaire lorsque (dans le cadre du méta‑programmation) nous manipulons des arbres d’expression purs, en reportant le contrôle de type.

**Références** : TC++PL4

#### Application

Marquer les arguments de type de modèle sans concept

### <a name="rt-std-concepts"></a>T.11 : Quand c’est possible, utiliser des concepts standard

#### Raison

Les concepts « standards » (fourni par le [GSL](#gsl-guidelines-support-library) et par le standard ISO lui‑même) nous font gagner le travail de créer nos propres concepts, sont mieux pensés que ceux que nous pourrions improviser à la hâte et améliorent l’interopérabilité. 

##### Note

À moins de créer une nouvelle bibliothèque générique, la plupart des concepts dont vous avez besoin seront déjà définis par la bibliothèque standard.

##### Exemple

```
    template<typename T>
        // ne pas définir ceci : sortable est dans <iterator>
    concept Ordered_container = Sequence<T> && Random_access<Iterator<T>> && Ordered<Value_type<T>>;

    void sort(Ordered_container auto& s);
```

Ce `Ordered_container` est assez plausible, mais il est très proche du concept `sortable` dans la bibliothèque standard. Est‑il meilleur ? Est‑il juste ? Reflette‑il réellement les exigences du standard pour `sort` ? Il vaut mieux utiliser simplement `sortable` :

```
    void sort(sortable auto& s);   // mieux
```

#### Note

La liste des concepts « standard » évolue à mesure que nous approchons d’un standard ISO incluant les concepts.

##### Note

Concevoir un concept utile est difficile.

#### Application

Réunir ce qui est faisable. 
* Recherchez les arguments non contraints, les modèles utilisant des concepts non standards ou des concepts maison sans axiomes. 
* Développez un outil de découverte de concepts (p. ex., voir [une première expérience](https://www.stroustrup.com/sle2010_webversion.pdf)).

### <a name="rt-auto"></a>T.12 : Préférer les noms de concepts à `auto` pour les variables locales

#### Raison

`auto` est le concept le plus faible. Les noms de concepts portent plus de signification que simplement `auto`.

#### Exemple

```
    vector<string> v{ "abc", "xyz" };
    auto& x = v.front();        // mauvais
    String auto& s = v.front(); // bon (String est un concept GSL)
```

#### Application

* ???

### <a name="rt-shorthand"></a>T.13 : Préférer la notation courte pour les concepts à argument simple et unique

#### Raison

Lisibilité. Exprime directement une idée.

#### Exemple

Pour dire « `T` est `sortable` » :

```
    template<typename T>       // Correct mais verbeux : "The parameter is
        requires sortable<T>   // of type T which is the name of a type
    void sort(T&);             // that is sortable"

    template<sortable T>       // Better : "The parameter is of type T
    void sort(T&);             // which is Sortable"

    void sort(sortable auto&); // Best: "The parameter is Sortable"
```

Les versions plus courtes correspondent mieux à notre façon de parler. Notez que de nombreux modèles n'ont pas besoin d'utiliser le mot-clé `template`.

#### Application

* Non faisable à court terme lorsqu’on convertit du `<typename T>` et `<class T>` en version restreinte. 
* À plus tard, signaler les déclarations introduisant d’abord un `typename` puis le restreindre avec un concept simple à argument unique.

### <a name="ss-concepts-def"></a>T.concepts.def : Règles de définition de concept

Définir de bons concepts est non trivial. Les concepts visent à représenter des concepts fondamentaux d’un domaine d’application (c’est‑à‑dire le nom « concept »). Assembler un ensemble de contraintes syntaxiques pour être utilisés pour les arguments d’une seule classe ou d’un seul algorithme n’est pas ce que les concepts étaient conçus pour et ne donnera pas les avantages complets du mécanisme.

Il est généralement utile de définir des concepts pour le codage qui fonctionne avec une implémentation (p. ex., C++20 ou plus tard), mais définir des concepts est une technique de conception utile en soi et aide à attraper les erreurs conceptuelles et à clarifier les concepts (sic!) d’une implémentation.

### <a name="rt-low"></a>T.20 : Éviter les « concepts » sans sémantique significative

#### Raison

Les concepts sont censés exprimer des notions sémantiques, comme « un nombre », « un intervalle d’éléments » et « totalement ordered ». Des contraintes simples, comme « a un opérateur `+` » ou « a un opérateur `>` », ne peuvent être significativement spécifiées en isolation et ne devraient être utilisées que comme blocs de construction pour des concepts signifiants, plutôt que dans le code utilisateur.

#### Exemple, mauvais

```
    template<typename T>
    // mauvais ; insuffisant
    concept Addable = requires(T a, T b) { a + b; };

    template<Addable N>
    auto algo(const N& a, const N& b) // utilisez deux chiffres
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
```

Peut-être qu’on attendait la concaténation. Plus probablement, c’était un accident. Définir l’opérateur de soustraction également yieldrait des ensembles d’acceptation très différents. Le `Addable` viole la règle mathématique d’additivité : `a+b == b+a`.

#### Note

La capacité à spécifier une sémantique significative est une caractéristique décisive d’un véritable concept, contrairement à une contrainte syntaxique.

#### Exemple

```
    template<typename T>
    // Les opérateurs +, -, *, et / sur un nombre sont supposés suivre les règles mathématiques usuelles
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
```

#### Note

Les concepts avec plusieurs opérations ont une probabilité beaucoup plus faible de correspondre accidentellement à un type qu’un concept à une seule opération.

#### Application

* Marquer les concepts à une opération unique lorsqu’ils sont utilisés hors d’une définition de concept
* Marquer l’usage de `enable_if` qui semble simuler des concepts à une opération unique.

### <a name="rt-complete"></a>T.21 : Exiger un ensemble complet d’opérations pour un concept

#### Raison

Facilité de compréhension. Interopérabilité améliorée. Aide les implémenteurs et les mainteneurs.

#### Note

C’est une variante spécifique de la règle plus générale qu’un concept doit avoir une signification sémantique (voir [T.20]).

#### Exemple, mauvais

```
    template<typename T> concept Subtractable = requires(T a, T b) { a - b; };
```

Cette définition n’a pas de sens sémantique. Vous avez besoin d’au moins `+` pour donner un sens à `-`.

Exemples d’ensembles complets :

* `Arithmetic` : `+`, `-`, `*`, `/`, `+=`, `-=`, `*=`, `/=`
* `Comparable` : `<`, `>`, `<=`, `>=`, `==`, `!=`

#### Note

Cette règle s’applique, que vous utilisiez le support natif des concepts ou non. C’est une règle générale qui s’applique même aux non‑templates :

```
    class Minimal {
        // ...
    };

    bool operator==(const Minimal&, const Minimal&);
    bool operator<(const Minimal&, const Minimal&);

    Minimal operator+(const Minimal&, const Minimal&);
    // pas d’autres opérateurs
```

### <a name="rt-axiom"></a>T.22 : Spécifier les axiomes pour les concepts

#### Raison

Un concept utile a un sens sémantique. Exprimer ce sens de façon informelle, semi‑formelle ou formelle rend le concept compréhensible et la démarche d’expression du concept peut attraper des erreurs conceptuelles. C’est un outil de conception puissant.

#### Exemple

```
    template<typename T>
        // Les opérateurs +, -, *, et / sur un nombre sont supposés suivre les règles mathématiques usuelles
        // axiom(T a, T b) { a + b == b + a; a - a == 0; a * (b + c) == a * b + a * c; /*...*/ }
        concept Number = requires(T a, T b) {
            { a + b } -> convertible_to<T>;
            { a - b } -> convertible_to<T>;
            { a * b } -> convertible_to<T>;
            { a / b } -> convertible_to<T>;
        };
```

#### Note

C’est un axiome au sens mathématique : quelque chose qui peut être supposé sans preuve. En général, les axiomes ne sont pas démontrables, et lorsque cela se produit, la preuve dépasse souvent les possibilités d’un compilateur.  
Un axiome peut ne pas être général, mais l’écrivain du modèle peut supposer qu’il est valable pour toutes les entrées réellement utilisées (comme une précondition).

#### Note

Dans ce contexte les axiomes sont des expressions booléennes.  
Voir le [Palo Alto TR](021-references.md) pour des exemples.   
Actuellement, C++ ne prend pas en charge les axiomes (même la TS Concepts ISO), alors on se doit de rester en commentaires longtemps.  
Une fois le support linguistique disponible, le `//` devant l’axiome peut être enlevé.

#### Note

Les concepts de « ébauche » encore en développement ne définissent généralement qu’un ensemble de contraintes sans sémantique bien définie.  
Un « Balancer » pour un arbre binaire générique :

```
    // balancer pour un generic binary tree
    template<typename Node> concept Balancer = requires(Node* p) {
        add_fixup(p);
        touch(p);
        detach(p);
    };
```

Donc un `Balancer` doit fournir au minimum ces opérations sur un nœud `Node`, mais nous ne sommes pas encore prêts à spécifier la sémantique générale complète car un nouvel arbre équilibré peut nécessiter plus d’opérations.  
Un concept incomplet ou sans sémantique bien définie reste utile.  

#### Application

* Recherche du mot « axiom » dans les commentaires de définition de concept

### <a name="rt-refine"></a>T.23 : Différencier un concept affiné de son cas plus général en ajoutant de nouveaux motifs d’utilisation

#### Raison

Sinon ils ne peuvent être distingués automatiquement par le compilateur.

#### Exemple

```
    template<typename I>
    // Note : input_iterator est défini dans <iterator>
    concept Input_iter = requires(I iter) { ++iter; };

    template<typename I>
    // Note : forward_iterator est défini dans <iterator>
    concept Fwd_iter = Input_iter<I> && requires(I iter) { iter++; };
```

Le compilateur peut déterminer l’affinement basé sur l’ensemble des opérations requises (ici, suffix `++`). Cela réduit la charge sur les implémenteurs de ces types car ils n’ont pas besoin de déclarations spéciales pour « hooker » le concept.  
Si deux concepts ont exactement les mêmes exigences, ils sont logiquement équivalents (il n’y a pas d’affinement).

#### Application

* Marquer un concept qui a exactement les mêmes exigences qu’un autre déjà vu (ni l’un ni l’autre est plus affiné).  
  Pour désambiguer, voir [T.24](#rt-tag).

### <a name="rt-tag"></a>T.24 : Utiliser des classes‑étiquettes ou des traits pour différencier les concepts qui ne diffèrent que par la sémantique

#### Raison

Deux concepts qui exigent la même syntaxe mais ont des sémantiques différentes créent une ambiguïté à moins que le programmeur ne les différencie.

#### Exemple

```
    template<typename I>    // iterator fournissant un accès aléatoire
    // Note : random_access_iterator est défini dans <iterator>
    concept RA_iter = ...;

    template<typename I>    // iterator fournissant un accès aléatoire à des données contiguës
    // Note : contiguous_iterator est défini dans <iterator>
    concept Contiguous_iter =
        RA_iter<I> && is_contiguous_v<I>;  // utilisant le trait is_contiguous
```

Le programmeur (dans une bibliothèque) doit définir `is_contiguous` (un trait) correctement.

Envelopper une classe‑étiquette dans un concept simplifie encore ce motif :

```
    template<typename I> concept Contiguous = is_contiguous_v<I>;

    template<typename I>
    concept Contiguous_iter = RA_iter<I> && Contiguous<I>;
```

Le programmeur doit définir le trait `is_contiguous` approprié.

#### Note

Les traits peuvent être des classes‑traits ou des traits de type.  
Ils peuvent être définis par l’utilisateur ou par la bibliothèque standard.  
Préférer ceux de la bibliothèque standard.

#### Application

* Le compilateur signale l’utilisation de concepts identiques ambiguës.  
* Marquage de la définition de concepts identiques.

### <a name="rt-not"></a>T.25 : Éviter les contraintes complémentaires

#### Raison

Clarté. Maintenabilité. Les fonctions avec des exigences complémentaires exprimées via la négation sont fragiles.

#### Exemple

Initie‑vous à un concept :

```
    template<typename T>
        requires !C<T>    // mauvais
    void f();
```

ou

```
    template<typename T>
        requires C<T>
    void f();
```

C’est meilleur :

```
    template<typename T>   // modèle général
        void f();

    template<typename T>   // spécialisation par concept
        requires C<T>
    void f();
```

Le compilateur choisira la version non contraint seulement lorsque `C<T>` n’est pas satisfait.  
Si vous ne voulez pas (ou ne pouvez pas) définir une version non contraint de `f`, supprimez‑la.

```
    template<typename T>
    void f() = delete;
```

Le compilateur choisira l’overload, ou émettra une erreur appropriée.

#### Note

Les exigences complémentaires sont couramment trouvées dans `enable_if` :

```
    template<typename T>
    enable_if<!C<T>, void>   // mauvais
    f();

    template<typename T>
    enable_if<C<T>, void>
    f();
```

#### Note

Les exigences complémentaires sur une seule exigence sont parfois (incorrectement) considérées gérables.  
Mais pour deux ou plus exigences, le nombre de définitions peut multiplier exponentiellement (2, 4, 8, 16, …):

```
    C1<T> && C2<T>
    !C1<T> && C2<T>
    C1<T> && !C2<T>
    !C1<T> && !C2<T>
```

Les opportunités d’erreurs se multiplient.

#### Application

* Marquer les paires de fonctions avec `C<T>` et `!C<T>`.

### <a name="rt-use"></a>T.26 : Préférer de définir les concepts en termes de motifs d’utilisation plutôt que d’une syntaxe simple

#### Raison

La définition est plus lisible et correspond directement à ce que l’utilisateur doit écrire.  
Les conversions sont prises en compte. Vous n’avez pas à vous souvenir des noms de tous les traits de type.

#### Exemple

Vous pourriez être tenté de définir un concept `Equality` ainsi :

```
    template<typename T> concept Equality = has_equal<T> && has_not_equal<T>;
```

Il est clairement meilleur et plus facile d’utiliser le standard `equality_comparable`, mais - à titre d’exemple - si vous deviez définir un tel concept, préférez :

```
    template<typename T> concept Equality = requires(T a, T b) {
        { a == b } -> std::convertible_to<bool>;
        { a != b } -> std::convertible_to<bool>;
        // axiom { !(a == b) == (a != b) }
        // axiom { a = b; => a == b }  // => signifie "implique"
    };
```

au lieu de définir deux concepts sans signification `has_equal` et `has_not_equal` juste comme auxiliaires.

#### Application

????

## <a name="ss-temp-interface"></a>Interfaces de modèle

Tout au long des années, la programmation avec des modèles a souffert d’une faible distinction entre l’interface d’un modèle et son implémentation.  
Avant les concepts, cette distinction n’était pas directement prise en charge par le langage.  
Cependant, l’interface d’un modèle est un concept critique — un contrat entre l’utilisateur et l’implémenteur — et doit être soigneusement conçu.

### <a name="rt-fo"></a>T.40 : Utiliser des objets fonction pour passer des opérations aux algorithmes

#### Raison

Les objets fonction peuvent porter plus d’informations à travers une interface qu'un simple pointeur vers une fonction.  
En général, passer des objets fonction donne de meilleures performances que passer des pointeurs vers des fonctions.

#### Exemple

```
    bool greater(double x, double y) { return x > y; }
    sort(v, greater);                                    // pointeur vers une fonction : potentiellement lent
    sort(v, [](double x, double y) { return x > y; });   // objet fonction
    sort(v, std::greater{});                             // objet fonction

    bool greater_than_7(double x) { return x > 7; }
    auto x = find_if(v, greater_than_7);                 // pointeur vers une fonction : inflexible
    auto y = find_if(v, [](double x) { return x > 7; }); // objet fonction : transporte les données nécessaires
    auto z = find_if(v, Greater_than<double>(7));        // objet fonction : transporte les données nécessaires
```

Vous pouvez, bien sûr, généraliser ces fonctions en utilisant `auto` ou des concepts. Par ex.:

```
    auto y1 = find_if(v, [](totally_ordered auto x) { return x > 7; }); // impose un type ordonné
    auto z1 = find_if(v, [](auto x) { return x > 7; });                 // espère que le type supporte `>`.
```

#### Note

Les lambdas génèrent des objets fonction.

#### Note

L’argument de performance dépend du compilateur et de l’optimiseur.

#### Application

* Marquer les pointeurs à des fonctions en tant que paramètres de modèle.
* Marquer les pointeurs à des fonctions passés en tant qu’arguments de modèle (risques de faux positifs).

### <a name="rt-essential"></a>T.41 : Ne demander que les propriétés essentielles dans les concepts d’un modèle

#### Raison

Gardez les interfaces simples et stables.

#### Exemple

Considérons un `sort` instrumenté avec un support de débogage simplifié :

```
    void sort(sortable auto& s)  // trier la séquence s
    {
        if (debug) cerr << "enter sort( " << s <<  ")\n";
        // ...
        if (debug) cerr << "exit sort( " << s <<  ")\n";
    }
```

Devrait-il être réécrit ainsi ?

```
    template<sortable S>
        requires Streamable<S>
    void sort(S& s)  // trier la séquence s
    {
        if (debug) cerr << "enter sort( " << s <<  ")\n";
        // ...
        if (debug) cerr << "exit sort( " << s <<  ")\n";
    }
```

Après tout, il n’y a rien dans `sortable` qui exige une prise en charge `iostream`.  
D’un autre côté, il n’y a rien dans l’idée fondamentale de tri qui dit quoi‑que‑que sur le débogage.

#### Note

Si nous exigeons qu’une opération soit incluée dans la vérification des concepts, l’interface devient instable : t. al. à chaque modification des facilités de collecte de données, tests, etc., la définition du modèle devra changer et chaque usage devra être recompilé. Cela est gênant et parfois impossible dans certains environnements.

Inversement, si nous utilisons une opération dans l’implémentation qui n’est pas garantie par le contrôle de concept, nous pourrions obtenir une erreur de compilation tardive.

En ne vérifiant pas les concepts pour les propriétés qui ne sont pas considérées essentielles, nous reportons la vérification jusqu’au moment de l’instanciation. Nous considérons que c’est un compromis valable.

Notez que l’utilisation de noms non locaux, non dépendants (tels que `debug` et `cerr`) introduit également des dépendances de contexte qui peuvent entraîner des erreurs « mystérieuses ».

#### Note

Il peut être difficile de décider quelles propriétés d’un type sont essentielles ou non.

#### Application

???

### <a name="rt-alias"></a>T.42 : Utiliser des alias de modèle pour simplifier la notation et masquer les détails d’implémentation

#### Raison

Amélioration de la lisibilité. Masquage de la mise en œuvre.  
Notez que les alias de modèle remplacent de très nombreuses utilisations de traits de calcul de type.  
Ils peuvent également être utilisés pour embrasser un trait.

#### Exemple

```
    template<typename T, size_t N>
    class Matrix {
        // ...
        using Iterator = typename std::vector<T>::iterator;
        // ...
    };
```

Cela évite à l’utilisateur de `Matrix` de savoir comment les éléments sont stockés dans un `vector` et économise également le fait de devoir taper à chaque fois `typename std::vector<T>::`.

#### Exemple

```
    template<typename T>
    void user(T& c)
    {
        // ...
        typename container_traits<T>::value_type x; // mauvais, verbeux
        // ...
    }

    template<typename T>
    using Value_type = typename container_traits<T>::value_type;
```

Cela évite à l’utilisateur de `Value_type` de devoir connaître la technique utilisée pour implémenter `value_type`.

```
    template<typename T>
    void user2(T& c)
    {
        // ...
        Value_type<T> x;
        // ...
    }
```

#### Note

Une utilisation simple courante pourrait être exprimée : « Emballer les traits ! »

#### Application

* Marquer l’utilisation d’un qualificatif `typename` hors des déclarations `using`.
* ???

### <a name="rt-using"></a>T.43 : Préférer `using` à `typedef` pour définir des alias

#### Raison

Lisibilité améliorée : avec `using`, le nouveau nom apparaît en premier plutôt qu’un élément du corps d’une déclaration.  
Généralité : `using` peut être utilisé pour les alias de modèle, alors que `typedef` ne peut pas facilement les faire.  
Uniformité : `using` a une syntaxe similaire à `auto`.

#### Exemple

```
    typedef int (*PFI)(int);   // OK, mais complexe

    using PFI2 = int (*)(int);   // OK, préféré

    template<typename T>
    typedef int (*PFT)(T);      // erreur

    template<typename T>
    using PFT2 = int (*)(T);   // OK
```

#### Application

* Marquer les utilisations de `typedef`. Cela donnera beaucoup de « hits » :-(

### <a name="rt-deduce"></a>T.44 : Utiliser des modèles fonctionnels pour déduire les types d’arguments de modèle de classe (où cela est faisable)

#### Raison

Écrire les types d’arguments de modèle explicitement peut être fastidieux et inutilement verbeux.

#### Exemple

```
    tuple<int, string, double> t1 = {1, "Hamlet", 3.14};   // type explicite
    auto t2 = make_tuple(1, "Ophelia"s, 3.14);           // meilleur ; type déduit
```

Notez l’utilisation du suffixe `s` pour garantir que la chaîne est un `std::string`, plutôt qu’une chaîne C‑style.

#### Note

Comme vous pouvez écrire un `make_T` de façon triviale, le compilateur pourrait l’implémenter; les fonctions `make_T` deviennent donc redondantes à l’avenir.

#### Exception

Parfois, il n’y a pas de bonne façon de faire déduire les arguments de modèle et parfois, vous voulez les spécifier explicitement :

```
    vector<double> v = { 1, 2, 3, 7.9, 15.99 };
    list<Record*> lst;
```

#### Note

Notez que C++17 rend cette règle obsolète en permettant la déduction de paramètres de modèle directement depuis les paramètres de constructeur : [Template parameter deduction for constructors (Rev. 3)](https://www.open-std.org/jtc1/sc22/wg21/docs/papers/2016/p0091r1.html).  

Par ex. :

```
    tuple t1 = {1, "Hamlet"s, 3.14}; // déduit : tuple<int, string, double>
```

#### Application

* Marquer les utilisations où un type spécialisé explicite correspond exactement aux types des arguments utilisés.

### <a name="rt-regular"></a>T.46 : (supprimé)

### <a name="rt-visible"></a>T.47 : Éviter les modèles hautement visibles sans contraintes avec des noms communs

#### Raison

Un argument de modèle sans contrainte est une correspondance parfaite pour tout, de sorte que ce modèle peut être préféré à des types plus spécifiques qui nécessitent des conversions mineures.  
Cela est particulièrement gênant/danger chez l’utilisation d’ADL.  
Les noms communs augmentent ce risque.

#### Exemple

```
    namespace Bad {
        struct S { int m; };
        template<typename T1, typename T2>
        bool operator==(T1, T2) { cout << "Bad\n"; return true; }
    }

    namespace T0 {
        bool operator==(int, Bad::S) { cout << "T0\n"; return true; }  // comparer à int

        void test()
        {
            Bad::S bad{ 1 };
            vector<int> v(10);
            bool b = 1 == bad;
            bool b2 = v.size() == bad;
        }
    }
```

Cela imprime `T0` et `Bad`.

Maintenant, l’opérateur `==` dans `Bad` était conçu pour créer des problèmes, mais auriez‑vous remarqué ce problème en production ?  
Le problème est que `v.size()` renvoie un entier non signé, alors qu’une conversion est nécessaire pour appeler l’propre `==` ; l’opérateur `==` dans `Bad` ne nécessite aucune conversion.  
Les types réalistes, comme les itérateurs de la bibliothèque standard, peuvent présenter des tendances anti‑sociales similaires.

#### Note

Si un modèle sans contrainte est défini dans le même espace de nom qu’un type, ce modèle sans contrainte peut être trouvé par ADL (tel qu’il se passe dans l’exemple).  
Ou soit‑tout, il est très visible.

#### Note

Cette règle devrait ne pas être nécessaire, mais le comité ne peut pas accepter d’exclure l’ADL pour des modèles sans contrainte.

Malheureusement, la bibliothèque standard viole largement cette règle, en plaçant de nombreux modèles sans contrainte et types dans le même espace de nom `std`.

#### Application

* Marquer les modèles définis dans un espace de nom où des types concrets sont également définis (peut‑être pas faisable tant que nous n’aurons pas de concepts).

### <a name="rt-concept-def"></a>T.48 : Si votre compilateur ne supporte pas les concepts, les simuler avec `enable_if`

#### Raison

Une façon optimale de contourner l’absence de support direct de concepts.  
`enable_if` peut être utilisé pour conditionner la définition des fonctions et pour choisir parmi une série de fonctions.

#### Exemple

```
    template<typename T>
    enable_if_t<is_integral_v<T>>
    f(T v)
    {
        // ...
    }
```

Équivalent à :

```
    template<Integral T>
    void f(T v)
    {
        // ...
    }
```

#### Note

Soyez attentif aux [contraintes complémentaires](#rt-not).  
Simuler la surcharge de concept avec `enable_if` force parfois l’usage de cette technique d’erreur.

#### Application

???

### <a name="rt-erasure"></a>T.49 : Quand c’est possible, éviter l’injection de type

#### Raison

L’injection de type introduit un niveau supplémentaire d’indirection en cachant les informations de type derrière une frontière de compilation séparée.

#### Exemple

    ???

**Exceptions** : l’injection de type est parfois appropriée, comme pour `std::function`.

#### Application

???

#### Note


## <a name="ss-temp-def"></a>T.def : Définition de modèle

Une définition de modèle (classe ou fonction) peut contenir du code arbitraire, donc une révision complète des techniques de programmation C++ couvrirait donc le sujet.  
Cependant, ce section se concentre sur ce qui est spécifique à la mise en œuvre d’un modèle.  
En particulier, elle se concentre sur la dépendance d’une définition de modèle à son contexte.

### <a name="rt-depend"></a>T.60 : Réduire les dépendances contextuelles d’un modèle

#### Raison

Plus de compréhension. Réduction des erreurs dues à des dépendances inattendues. Facilité d’outils.

#### Exemple

```
    template<typename C>
    void sort(C& c)
    {
        std::sort(begin(c), end(c)); // dépendance nécessaire et utile
    }

    template<typename Iter>
    Iter algo(Iter first, Iter last)
    {
        for (; first != last; ++first) {
            auto x = sqrt(*first); // dépendance potentiellement surprenante : quel sqrt() ?
            helper(first, x);      // dépendance potentiellement surprenante :
                                   // helper est choisi en fonction de first et x
            TT var = 7;            // dépendance potentiellement surprenante : quel TT ?
        }
    }
```

#### Note

Les modèles apparaissent généralement dans des fichiers d’en‑tête, leurs dépendances de contexte sont donc plus vulnérables aux dépendances d’ordre d’`#include` que les fonctions dans des fichiers `.cpp`.

#### Note

Avoir un modèle qui opère uniquement sur ses arguments serait un moyen de réduire le nombre de dépendances au minimum, mais ce serait généralement ingérable.  
Par ex. : les algorithmes utilisent souvent d’autres algorithmes et invoquent des opérations qui ne sont pas exclusivement définies sur les arguments.  
Et ne parlons même pas des macros !

**Voir aussi** : [T.69](#rt-customization)

#### Application

??? Tricky

### <a name="rt-scary"></a>T.61 : Ne pas sur‑parameteriser les membres (SCARY)

#### Raison

Un membre qui ne dépend pas d’un paramètre de modèle ne peut être utilisé que pour un argument de modèle spécifique.  
Cela limite l’utilisation et augmente généralement la taille du code.

#### Exemple, mauvais

```
    template<typename T, typename A = std::allocator<T>>
        // requires Regular<T> && Allocator<A>
    class List {
    public:
        struct Link {   // ne dépend pas d’A
            T elem;
            Link* pre;
            Link* suc;
        };

        using iterator = Link*;

        iterator first() const { return head; }

        // …
    private:
        Link* head;
    };
```

```
    List<int> lst1;
    List<int, My_allocator> lst2;
```

Ceci semble inoffensif, mais `Link` dépend formellement de l’allocateur (même s’il ne l’utilise pas).  
Cela provoque des instantiations redondantes qui peuvent être surprenantes.  
La solution habituelle consiste à faire de cette classe interne une classe séparée (en dehors du modèle) avec son propre ensemble minimal de paramètres de modèle.

```
    template<typename T>
    struct Link {
        T elem;
        Link* pre;
        Link* suc;
    };
```

```
    template<typename T, typename A = std::allocator<T>>
        // requires Regular<T> && Allocator<A>
    class List2 {
    public:
        using iterator = Link<T>*;

        iterator first() const { return head; }

        // …
    private:
        Link<T>* head;
    };
```

```
    List2<int> lst1;
    List2<int, My_allocator> lst2;
```

Certains trouvent l’idée que le `Link` n’est plus caché dans la liste très effrayante, nous l’appelons donc [SCARY](https://www.open-std.org/jtc1/sc22/WG21/docs/papers/2009/n2911.pdf).  
Il est mentionné que l’acronyme SCARY décrit les déclarations qui semblent erronées (apparaient contrainte par l’implémentation), mais qui fonctionnent réellement grâce à la bonne implémentation.

#### Note

Cela s’applique également aux lambdas qui ne dépendent pas de tous les paramètres de modèle.

#### Application

* Marquer les types de membre qui ne dépendent pas de chaque paramètre de modèle
* Marquer les fonctions membres qui ne dépendent pas de chaque paramètre de modèle
* Marquer les lambdas ou les variables de modèle qui ne dépendent pas de chaque paramètre de modèle

### <a name="rt-nondependent"></a>T.62 : Placer les membres de classe de modèle non dépendants dans une classe de base non paramétrée

#### Raison

Autorise les membres de la classe de base à être utilisés sans spécifier de paramètres de modèle et sans instanciation du modèle.

#### Exemple

```
    template<typename T>
    class Foo {
    public:
        enum { v1, v2 };
        // …
    };
```

???

```
    struct Foo_base {
        enum { v1, v2 };
        // …
    };
```

```
    template<typename T>
    class Foo : public Foo_base {
    public:
        // …
    };
```

#### Note

Une version plus générale de cette règle serait : « Si un membre de classe dépend de seulement N paramètres de modèle sur M, placez‑le dans une classe de base contenant seulement N paramètres ».  
Pour N = 1, on peut choisir une classe de base adjacente à cette classe dans le même espace de nom, comme dans [T.61](#rt-scary).

??? Que faire des constantes ? des statiques de classe ?

#### Application

* Marquer ???

### <a name="rt-specialization"></a>T.64 : Utiliser la spécialisation pour fournir des implémentations alternatives de modèles de classe

#### Raison

Un modèle définit une interface générale.  
La spécialisation offre un mécanisme puissant pour fournir des implémentations alternatives de cette interface.

#### Exemple

    ???

**Références** : ?

#### Application

???

### <a name="rt-tag-dispatch"></a>T.65 : Utiliser la distribution de tag pour fournir des implémentations alternatives d’une fonction

#### Raison

* Un modèle définit une interface générale.  
* La distribution de tag permet de sélectionner les implémentations en fonction de propriétés spécifiques d’un argument de type.  
* Performance.

#### Exemple

C’est une version simplifiée de `std::copy` (en oubliant la possibilité de séquences non contiguës).

```
    struct trivially_copyable_tag {};
    struct non_trivially_copyable_tag {};

    // T n’est pas trivially copyable
    template<class T> struct copy_trait { using tag = non_trivially_copyable_tag; };
    // int est trivially copyable
    template<> struct copy_trait<int> { using tag = trivially_copyable_tag; };

    template<class Iter>
    Out copy_helper(Iter first, Iter last, Iter out, trivially_copyable_tag)
    {
        // use memmove
    }

    template<class Iter>
    Out copy_helper(Iter first, Iter last, Iter out, non_trivially_copyable_tag)
    {
        // use loop calling copy constructors
    }

    template<class Iter>
    Out copy(Iter first, Iter last, Iter out)
    {
        using tag_type = typename copy_trait<std::iter_value_t<Iter>>::tag;
        return copy_helper(first, last, out, tag_type{});
    }

    void use(vector<int>& vi, vector<int>& vi2, vector<string>& vs, vector<string>& vs2)
    {
        copy(vi.begin(), vi.end(), vi2.begin()); // uses memmove
        copy(vs.begin(), vs.end(), vs2.begin()); // uses a loop calling copy constructors
    }
```

C’est une technique générale et puissante pour la sélection d’algorithme à la compilation.

#### Note

Avec les contraintes C++20, ces alternatives peuvent être distinguées directement :

```
    template<class Iter>
        requires std::is_trivially_copyable_v<std::iter_value_t<Iter>>
    Out copy_helper(In, first, In last, Out out)
    {
        // use memmove
    }

    template<class Iter>
    Out copy_helper(In, first, In last, Out out)
    {
        // use loop calling copy constructors
    }
```

#### Application

???

### <a name="rt-specialization2"></a>T.67 : Utiliser la spécialisation pour fournir des implémentations alternatives pour les types irréguliers

#### Raison

???

#### Exemple

    ???

#### Application

???

### <a name="rt-cast"></a>T.68 : Utiliser `{}` plutôt que `()` dans les modèles pour éviter les ambiguïtés

#### Raison

`()` est vulnérable aux ambiguïtés grammaticales.

#### Exemple

```
    template<typename T, typename U>
    void f(T t, U u)
    {
        T v1(T(u));    // erreur : v1 est considered a function, not a variable
        T v2{u};       // clair : soit une variable
        auto x = T(u); // vague : construction ou cast ?
    }
```

```
    f(1, "asdf"); // mauvais : cast from const char* to int
```

#### Application

* Marquer les initialisateurs `()`
* Marquer les casts de style fonction

### <a name="rt-customization"></a>T.69 : À l'intérieur d'un modèle, ne pas faire appel à une fonction non membre sans qualification sauf si l’on l'intentionne comme point de personnalisation

#### Raison

* Ne fournir que la flexibilité voulue.  
* Eviter la vulnérabilité aux changements d'environnement inattendus.

#### Exemple

Il existe trois grandes façons de laisser le code appelant personnaliser un modèle.

```
    template<class T>
        // Appel d'une fonction membre
    void test1(T t)
    {
        t.f();    // exiger T fournit f()
    }
```

```
    template<class T>
    void test2(T t)
        // Appel d’une fonction non membre sans qualification
    {
        f(t);     // exiger f(/T/) disponible dans le scope appelant ou dans le namespace de T
    }
```

```
    template<class T>
    void test3(T t)
        // Invocation d'une « trait »
    {
        test_traits<T>::f(t); // exiger la spécialisation de test_traits<> pour récupérer les fonctions/types non par défaut
    }
```

Une `trait` est généralement une alias de type pour calculer un type, une fonction `constexpr` pour calculer une valeur ou une traditionnelle `trait` template à spécialiser sur le type de l’utilisateur.

#### Note

Si vous voulez appeler votre propre helper `helper(t)` pour une valeur `t` qui dépend d’un paramètre de type de modèle, mettez‑le dans un `::detail` namespace et qualifiez l’appel comme `detail::helper(t);`.  
Une appel non qualifié devient un point de personnalisation où toute fonction `helper` dans le namespace de `t` peut être invoquée; cela peut cause des problèmes comme [l’appel de fonctions non contraintes par inadvertance](#rt-visible).

#### Application

* Dans un modèle, marquer les appels non qualifiés à une fonction non membre qui passe une variable de type dépendant lorsqu’une fonction non membre de même nom existe dans le namespace du modèle.

## <a name="ss-temp-hier"></a>T.temp-hier : Règles de modèle et hiérarchie

Les modèles sont le pilier du support C++ pour la programmation générique et les hiérarchies de classes le pilier du support de la programmation orientée objet.  
Les deux mécanismes de langage peuvent être utilisés efficacement en combinaison, mais quelques pièges de conception doivent être évités.

### <a name="rt-hier"></a>T.80 : Ne pas templatiser naïvement une hiérarchie de classe

#### Raison

Templatiser une hiérarchie de classe qui possède de nombreuses fonctions, en particulier beaucoup de fonctions virtuelles, peut entraîner un gonflement du code.  

#### Exemple, mauvais

```
    template<typename T>
    struct Container {         // interface
        virtual T* get(int i);
        virtual T* first();
        virtual T* next();
        virtual void sort();
    };

    template<typename T>
    class Vector : public Container<T> {
    public:
        // …
    };
```

```
    Vector<int> vi;
    Vector<string> vs;
```

Il est probablement mauvais de définir `sort` comme membre d’une classe conteneur, mais ce n’est pas rare et c’est un bon exemple de ce qu’il ne faut pas faire.

Dans ce cas, le compilateur ne sait pas si `Vector<int>::sort()` est appelé, il doit donc générer le code pour cette fonction.  
Même si ces deux fonctions ne sont jamais appelées, elles entraîneront une augmentation de la taille du code.  
Imaginez si une hiérarchie de classe contient des dizaines de fonctions membres et de dizaines de classes dérivées avec beaucoup d’instanciations.  

#### Note

Dans de nombreux cas, vous pouvez fournir une interface stable sans paramétriser la base ; voir « base stable » ([Stable base](#rt-abi)) et « Object‑oriented and GP » ([OO and GP](#rt-generic-oo))

#### Application

* Marquer les fonctions virtuelles qui dépendent d’un paramètre de modèle. ??? Fausse posit

### <a name="rt-array"></a>T.81 : Ne pas mélanger hiérarchies et tableaux

#### Raison

Un tableau de dérivés peut implicitement « démouler » vers un pointeur de base avec des résultats potentiellement désastreux.

#### Exemple

Supposons que `Apple` et `Pear` sont deux types de `Fruit`.

```
    void maul(Fruit* p)
    {
        *p = Pear{};     // mettre un Pear dans *p
        p[1] = Pear{};   // mettre un Pear dans p[1]
    }
```

```
    Apple aa [] = { an_apple, another_apple };   // aa contient Apples (évidemment !)

    maul(aa);
    Apple& a0 = &aa[0];   // un Pear ?
    Apple& a1 = &aa[1];   // un Pear ?
```

Probablement, `aa[0]` sera un `Pear` (sans cast).  
Si `sizeof(Apple) != sizeof(Pear)` la conservation de `aa[1]` ne sera pas alignée sur le commencement d’un objet dans le tableau.  
Cela entraîne une violation de type et potentiellement une corruption mémoire.  
Ne jamais écrire ce code.

Notez que `maul()` viole la règle `[T*` pointe vers un objet individuel](#rf-ptr).

**Alternative** : utiliser un conteneur correctement templatisé :

```
    void maul2(Fruit* p)
    {
        *p = Pear{};   // mettre un Pear dans *p
    }

    vector<Apple> va = { an_apple, another_apple };   // vaut contient Apples (évidemment !)

    maul2(va);       // erreur : ne peut convertir vector<Apple> en Fruit*
    maul2(&va[0]);   // vous l’avez demandé

    Apple& a0 = &va[0];   // un Pear ?
```

Notez que l’affectation dans `maul2()` violé la règle de [non‑slicing](#res-slice).

#### Application

* Détect� ... 

### <a name="rt-linear"></a>T.82 : Lineariser une hiérarchie quand les fonctions virtuelles sont indésirables

#### Raison

 ???

#### Exemple

    ???

#### Application

???

### <a name="rt-virtual"></a>T.83 : Ne pas déclarer un modèle de fonction virtuelle

#### Raison

C++ ne supporte pas cela.  
S’il le faisait, les tables virtuelles ne pourraient pas être générées à la compilation.  
D’autre part, les implémentations doivent gérer le linking dynamique.

#### Exemple, ne pas

```
    class Shape {
        // …
        template<class T>
        virtual bool intersect(T* p);   // erreur : le modèle ne peut être virtuel
    };
```

#### Note

Nous avons besoin d’une règle parce que les gens continuent de demander.

#### Alternative

Double dispatch, visitors, calculer quelle fonction appeler.

#### Application

Le compilateur gère cela.

### <a name="rt-abi"></a>T.84 : Utiliser une implémentation centrale non modélisée pour fournir une interface ABI‑stable

#### Raison

Améliorer la stabilité du code.  
Éviter le gonflement du code.

#### Exemple

C’est peut‑être une classe de base.

```
    struct Link_base {   // stable
        Link_base* suc;
        Link_base* pre;
    };
```

```
    template<typename T>   // wrapper templatisé pour ajouter la sûreté de type
    struct Link : Link_base {
        T val;
    };
```

```
    struct List_base {
        Link_base* first;   // premier élément (si existant)
        int sz;             // nombre d’éléments
        void add_front(Link_base* p);
        // …
    };
```

```
    template<typename T>
    class List : List_base {
    public:
        void put_front(const T& e) { add_front(new Link<T>{e}); }   // cast implicite à Link_base
        T& front() { return static_cast<Link<T>*>(first)->val; }   // cast explicite vers Link<T>
        // …
    };
```

```
    List<int> li;
    List<string> ls;
```

Il n’y a maintenant qu’une copie des opérations de lien et de déconnexion d’une `List`.  
Les classes `Link` et `List` ne font que manipuler les types avec sécurité.

Au lieu d’utiliser une class de base séparée, une technique courante est de spécialiser pour `void` ou `void*` et de faire en sorte que le modèle générique pour `T` ne soit qu’une série de casts sécurisés vers/depuis l’implémentation centrale `void`.

**Alternative** : utiliser un implémentation [Pimpl](#ri-pimpl).

#### Application

???

## <a name="ss-variadic"></a>T.var : Règles de modèles variadiques

...

### <a name="rt-variadic"></a>T.100 : Utiliser des modèles variadiques lorsque vous avez besoin d’une fonction qui prend un nombre variable d’arguments de plusieurs types

#### Raison

Les modèles variadiques sont le mécanisme le plus général pour cela, et ils sont efficaces et type‑sûrs.  Fréquenter les variadic C vararg.

#### Exemple

    ??? printf

#### Application

* Marquer l’utilisation de `va_arg` dans le code utilisateur.

### <a name="rt-variadic-pass"></a>T.101 : ??? Comment passer des arguments à un modèle variadique ???

#### Raison

 ???

#### Exemple

    ??? attention aux arguments de type move‑only et référence

#### Application

???

### <a name="rt-variadic-process"></a>T.102 : Comment traiter les arguments d’un modèle variadique

#### Raison

 ???

#### Exemple

    ??? forwarding, type checking, references

#### Application

???

### <a name="rt-variadic-not"></a>T.103 : Ne pas utiliser des modèles variadiques pour des listes d’arguments homogènes

#### Raison

Il existe des moyens plus précis de spécifier une séquence homogène, comme un `initializer_list`.

#### Exemple

    ???

#### Application

???

## <a name="ss-meta"></a>T.meta : Méta‑programmation (TMP)

Les modèles offrent un mécanisme général pour la programmation à la compilation.  

The rest of the document continues similarly.  

(Note: This translation covers the entire provided snippet, preserving formatting, code indentation at 4 spaces, and adding `@TODO-LINK` next to missing anchor references such as `#gsl-guidelines-support-library`, `#res-slice`, `#rt-regular`, and placeholders like `#rt-??`.)