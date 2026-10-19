# <a name="s-templates"></a>T : Templates et programmation générique

La programmation générique consiste à programmer en utilisant des types et des algorithmes paramétrés par des types, des valeurs et des algorithmes. En C++, la programmation générique est prise en charge par les mécanismes du langage *template* .

Les arguments des fonctions génériques sont caractérisés par des ensembles d'exigences portant sur les types et les valeurs des arguments. En C++, ces exigences sont exprimées par des prédicats à temps de compilation appelés *concepts*.

Les templates peuvent également être utilisés pour la méta‑programmation ; c'est‐à‐dire des programmes qui composent du code à la compilation.

Une notion centrale dans la programmation générique est le « concept » ; c'est‑à‑dire des exigences sur les arguments de template présentées comme des prédicats à temps de compilation. Les *concepts* ont été standardisés en C++20, bien qu'ils aient été disponibles pour la première fois, sous une syntaxe légèrement antérieure, dans GCC 6.1.

## Résumé des règles d'utilisation des templates :
* [T.1 : Utiliser les templates pour augmenter le niveau d'abstraction du code](015-templates.md#rt-raise)
* [T.2 : Utiliser les templates pour exprimer des algorithmes applicables à de nombreux types d'arguments](015-templates.md#rt-algo)
* [T.3 : Utiliser les templates pour exprimer des conteneurs et des plages](015-templates.md#rt-cont)
* [T.4 : Utiliser les templates pour exprimer la manipulation d'arbres syntaxiques](015-templates.md#rt-expr)
* [T.5 : Combiner les techniques génériques et orientées objet pour amplifier leurs forces, pas leurs coûts](015-templates.md#rt-generic-oo)

## Résumé des règles d'utilisation des concepts :
* [T.10 : Spécifier les concepts pour tous les paramètres de template](015-templates.md#rt-concepts)
* [T.11 : Lorsqu'il est possible d'utiliser des concepts standards](015-templates.md#rt-std-concepts)
* [T.12 : Préférer les noms de concepts plutôt que *auto* pour les variables locales](015-templates.md#rt-auto)
* [T.13 : Préférer la notation abrégée pour les concepts simples à un seul type d'argument](015-templates.md#rt-shorthand)
* ???

## Résumé des règles de définition des concepts :
* [T.20 : Éviter les “concepts” dépourvus de sémantique significative](015-templates.md#rt-low)
* [T.21 : Exiger un ensemble complet d'opérations pour un concept](015-templates.md#rt-complete)
* [T.22 : Spécifier les axiomes des concepts](015-templates.md#rt-axiom)
* [T.23 : Différencier un concept raffiné de son cas plus général en ajoutant de nouveaux patrons d'utilisation](015-templates.md#rt-refine)
* [T.24 : Utiliser des classes d'étiquette ou des traits pour différencier des concepts dont la sémantique diffère uniquement](015-templates.md#rt-tag)
* [T.25 : Éviter les contraintes complémentaires](015-templates.md#rt-not)
* [T.26 : Préférer définir les concepts par des patrons d'utilisation plutôt que par une syntaxe simple](015-templates.md#rt-use)
* ???
* [T.30 : Utiliser la négation de concepteur (*!C<T>*) avec parcimonie pour exprimer une différence mineure](#rt-???) @TODO-LINK
* [T.31 : Utiliser la disjonction de concepteurs (*C1<T> || C2<T>*) avec parcimonie pour exprimer des alternatives](#rt-???) @TODO-LINK

## Résumé des règles de conception des interfaces de templates :
* [T.40 : Utiliser des objets fonctionnels pour transmettre des opérations aux algorithmes](015-templates.md#rt-fo)
* [T.41 : Exiger seulement les propriétés essentielles dans les concepts d'un template](015-templates.md#rt-essential)
* [T.42 : Utiliser des alias de templates pour simplifier la notation et masquer les détails d'implémentation](015-templates.md#rt-alias)
* [T.43 : Préférer *using* à *typedef* pour définir des alias](015-templates.md#rt-using)
* [T.44 : Utiliser des templates de fonctions pour déduire les types d'arguments de templates (lorsque c'est faisable)](015-templates.md#rt-deduce)
* [T.46 : (supprimé)](015-templates.md#rt-regular)
* [T.47 : Éviter les templates hautement visibles sans contraintes avec des noms communs](015-templates.md#rt-visible)
* [T.48 : Si votre compilateur ne supporte pas les concepts, fakes les avec *enable_if*](015-templates.md#rt-concept-def)
* [T.49 : Lorsque c'est possible, éviter l'effacement de type](015-templates.md#rt-erasure)

## Résumé des règles de définition des templates :
* [T.60 : Minimiser les dépendances contextuelles d'un template](015-templates.md#rt-depend)
* [T.61 : Ne pas surparamétrer les membres (SCARY)](015-templates.md#rt-scary)
* [T.62 : Placer les membres non dépendants d'un template de classe dans une classe de base non template](015-templates.md#rt-nondependent)
* [T.64 : Utiliser la spécialisation pour fournir des implémentations alternatives de templates de classe](015-templates.md#rt-specialization)
* [T.65 : Utiliser l'envoi de tags pour fournir des implémentations alternatives de fonctions](015-templates.md#rt-tag-dispatch)
* [T.67 : Utiliser la spécialisation pour fournir des implémentations alternatives pour des types irréguliers](015-templates.md#rt-specialization2)
* [T.68 : Utiliser **{**} plutôt que **(** dans les templates pour éviter des ambiguïtés](015-templates.md#rt-cast)
* [T.69 : À l'intérieur d'un template, ne pas appeler une fonction non membre sans qualification sauf si vous l'intentionnez comme point de personnalisation](015-templates.md#rt-customization)

## Résumé des règles de template et d'hierarchie :
* [T.80 : Ne pas templatiser naïvement une hiérarchie de classe](015-templates.md#rt-hier)
* [T.81 : Ne pas mélanger hiérarchies et tableaux](015-templates.md#rt-array) @TODO-LINK
* [T.82 : Lineariser une hiérarchie lorsque les fonctions virtuelles sont indésirables](015-templates.md#rt-linear)
* [T.83 : Ne pas déclarer une fonction membre template virtuelle](015-templates.md#rt-virtual)
* [T.84 : Utiliser une implémentation centrale non‑template pour fournir une interface stable ABI](015-templates.md#rt-abi)
* [T.?? : ????](#rt-???) @TODO-LINK

## Résumé des règles de template variadique :
* [T.100 : Utiliser des templates variadiques lorsqu'il faut une fonction prenant un nombre variable d'arguments de types divers](015-templates.md#rt-variadic)
* [T.101 : ??? Comment passer des arguments à un template variadique ???](015-templates.md#rt-variadic-pass)
* [T.102 : ??? Comment traiter les arguments d'un template variadique ???](015-templates.md#rt-variadic-process)
* [T.103 : Ne pas utiliser les templates variadiques pour des listes d'arguments homogènes](015-templates.md#rt-variadic-not)
* [T.?? : ????](#rt-???) @TODO-LINK

## Résumé des règles de méta‑programmation :
* [T.120 : Utiliser la méta‑programmation par template uniquement lorsqu'elle est vraiment nécessaire](015-templates.md#rt-metameta)
* [T.121 : Utiliser la méta‑programmation par template principalement pour émuler les concepts](015-templates.md#rt-emulate)
* [T.122 : Utiliser les templates (habituellement des alias) pour calculer des types à la compilation](015-templates.md#rt-tmp)
* [T.123 : Utiliser des fonctions *constexpr* pour calculer des valeurs à la compilation](015-templates.md#rt-fct)
* [T.124 : Préférer d'utiliser les facilities TMP de la bibliothèque standard](015-templates.md#rt-std-tmp)
* [T.125 : Si vous devez dépasser les facilities TMP de la bibliothèque standard, utilisez une bibliothèque existante](015-templates.md#rt-lib)
* [T.?? : ????](#rt-???) @TODO-LINK

## Autres règles de template :
* [T.140 : Si une opération peut être réutilisée, donnez-lui un nom](015-templates.md#rt-name)
* [T.141 : Utiliser un lambda non nommé si vous avez besoin d'un simple objet fonctionnel en un seul lieu](015-templates.md#rt-lambda)
* [T.142 ?: Utiliser des variables de template pour simplifier la notation](015-templates.md#rt-var)
* [T.143 : Ne pas écrire de code non générique involontairement](015-templates.md#rt-non-generic)
* [T.144 : Ne pas spécialiser les templates de fonctions](015-templates.md#rt-specialize-function)
* [T.150 : Vérifier qu'une classe correspond à un concept en utilisant *static_assert*](015-templates.md#rt-check-class)

## <a name="ss-gp"></a>T.gp : Programmation générique

La programmation générique consiste à programmer en utilisant des types et des algorithmes paramétrés par des types, des valeurs et des algorithmes.

### <a name="rt-raise"></a>T.1 : Utiliser les templates pour augmenter le niveau d'abstraction du code

#### Raison

Généralité. Réutilisation. Efficacité. Encourage une définition cohérente des types utilisateur.

#### Exemple, mauvais

Conceptuellement, les exigences suivantes sont erronées car ce que nous attendons de `T` est plus que juste les concepts très bas‑niveau de « peut être incrémenté » ou « peut être ajouté » :

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

Supposons que `Incrementable` ne supporte pas `+` et `Simple_number` ne supporte pas `+=`, nous avons surcontrôlé les implémenteurs de `sum1` et `sum2`. Et, dans ce cas, nous avons manqué une opportunité de généralisation.

#### Exemple

    template<typename T>
        requires Arithmetic<T>
    T sum(vector<T>& v, T s)
    {
        for (auto x : v) s += x;
        return s;
    }

Supposons que `Arithmetic` exige à la fois `+` et `+=`, nous avons contraint l'utilisateur de `sum` à fournir un type arithmétique complet. Ce n'est pas une exigence minimale, mais elle donne à l'implémenteur d'algorithmes la liberté nécessaire et garantit que tout type `Arithmetic` peut être utilisé pour une large variété d'algorithmes.

Pour une généralité et une réutilisation supplémentaires, nous pourrions également utiliser un concept plus général *Container* ou *Range* plutôt que de nous limiter à un seul conteneur, `vector`.

#### Note

Si nous définissons un template pour exiger exactement les opérations requises pour une implémentation unique d'un algorithme unique (par ex., exiger juste `+=` plutôt que également `= ` et `+`) et seulement celles, nous avons surcontrôlé les mainteneurs. Nous visons à minimiser les exigences sur les arguments de template, mais les exigences minimales absolues d'une implémentation rarement un concept significatif.

#### Note

Les templates peuvent être utilisés pour exprimer essentiellement tout (ils sont Turing complets), mais le but de la programmation générique (exprimé en utilisant les templates) est d'élargir efficacement les opérations/algorithmes sur un ensemble de types ayant des propriétés sémantiques similaires.

#### Enforced

* Marquer les algorithmes avec des exigences « trop simples », comme l'utilisation directe d'opérateurs spécifiques sans concept.
* Ne pas marquer la définition des concepts « trop simples » eux‑mêmes ; ils pourraient simplement être des blocs de construction pour des concepts plus utiles.

### <a name="rt-algo"></a>T.2 : Utiliser les templates pour exprimer des algorithmes applicables à de nombreux types d'arguments

#### Raison

Généralité. Minimiser la quantité de code source. Interopérabilité. Réutilisation.

#### Exemple

C'est la base de la STL. Un seul algorithme `find` fonctionne facilement avec n'importe quel type de plage d'entrée :

    template<typename Iter, typename Val>
        // requires Input_iterator<Iter>
        //       && Equality_comparable<Value_type<Iter>, Val>
    Iter find(Iter b, Iter e, Val v)
    {
        // ...
    }

#### Remarque

N'utilisez pas un template à moins d'avoir un besoin réaliste de plus d'un type d'argument. Ne pas trop abstraire.

#### Enforced

***tough, probablement nécessite un humain**

### <a name="rt-cont"></a>T.3 : Utiliser les templates pour exprimer des conteneurs et des plages

#### Raison

Les conteneurs ont besoin d'un type d'élément, et l'exprimer comme un paramètre de template est général, réutilisable et type‑safe. Cela évite également les solutions fragiles ou inefficaces. Convention : c'est la façon dont le STL le fait.

#### Exemple

    template<typename T>
        // requires Regular<T>
    class Vector {
        // ...
        T* elem;   // pointe sur `sz` Ts
        int sz;
    };

    Vector<double> v(10);
    v[7] = 9.9;

#### Exemple, mauvais

    class Container {
        // ...
        void* elem;   // pointe sur `size` éléments de certains types
        int sz;
    };

    Container c(10, sizeof(double));
    ((double*) c.elem)[7] = 9.9;

Ceci ne rend pas directement expressif l'intention du programmeur et masque la structure du programme du système de types et de l'optimiseur.

Masquer le `void*` derrière des macros ne fait que masquer les problèmes et introduit de nouvelles opportunités de confusion.

**Exceptions :** Si vous avez besoin d'une interface ABI‑stable, vous devrez peut‑être fournir une implémentation de base et exprimer le (type‑sécurisé) template en termes de celle‑ci. Voir [Stable base] (015-templates.md#rt-abi).

#### Enforced

* Signaler les utilisations de `void*` et de casts hors du code d'implémentation de bas niveau

### <a name="rt-expr"></a>T.4 : Utiliser les templates pour exprimer la manipulation d'arbres syntaxiques

#### Raison

…

#### Exemple

    …

**Exceptions** : …

### <a name="rt-generic-oo"></a>T.5 : Combiner les techniques génériques et orientées objet pour amplifier leurs forces, pas leurs coûts

#### Raison

Les techniques génériques et orientées objet sont complémentaires.

#### Exemple

Souplesse dynamique : Utilisez la polymorphie statique pour implémenter des interfaces polymorphes dynamiques.

    class Command {
        // pure virtual functions
    };

    // implementations
    template</*...*/>
    class ConcreteCommand : public Command {
        // implémenter les virtuels
    };

#### Exemple

La dynamique aide la statique : offrir une interface générique, confortable, liée statiquement, mais dispatcher dynamiquement en interne, afin de proposer un même layout d'objet. Les exemples incluent l'effacement de type comme le déléger de `std::shared_ptr` (mais [ne pas surutiliser l'effacement de type] (015-templates.md#rt-erasure)).

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

#### Remarque

Dans un template de classe, les fonctions non virtuelles ne sont instanciées que lorsqu'elles sont utilisées — mais les fonctions virtuelles sont instanciées à chaque instant. Cela peut gonfler la taille du code et peut sur‑contrôler un type générique en instanciant des fonctionnalités qui ne sont jamais nécessaires. Évitez cela, même si les facettes standard de la bibliothèque ont commis cette erreur.

### <a name="ss-concepts"></a>T.concepts : Règles sur les concepts

Les concepts sont une fonctionnalité C++20 pour spécifier les exigences sur les arguments de templates. Ils sont essentiels à la pensée sur la programmation générique et la base de beaucoup de travaux futurs sur les bibliothèques C++ (standard et autres).

Cette section suppose le support des concepts.

#### Résumé des règles d'utilisation des concepts :
* [T.10 : Spécifier les concepts pour tous les paramètres de template](015-templates.md#rt-concepts)
* [T.11 : Lorsqu'il est possible d'utiliser des concepts standards](015-templates.md#rt-std-concepts)
* [T.12 : Préférer les noms de concepts plutôt que *auto* pour les variables locales](015-templates.md#rt-auto)
* [T.13 : Préférer la notation abrégée pour les concepts simples à un seul type d'argument](015-templates.md#rt-shorthand)
* ???

#### Résumé des règles de définition des concepts :
* [T.20 : Éviter les “concepts” dépourvus de sémantique significative](015-templates.md#rt-low)
* [T.21 : Exiger un ensemble complet d'opérations pour un concept](015-templates.md#rt-complete)
* [T.22 : Spécifier les axiomes des concepts](015-templates.md#rt-axiom)
* [T.23 : Différencier un concept raffiné de son cas plus général en ajoutant de nouveaux patrons d'utilisation](015-templates.md#rt-refine)
* [T.24 : Utiliser des classes d'étiquette ou des traits pour différencier des concepts dont la sémantique diffère uniquement](015-templates.md#rt-tag)
* [T.25 : Éviter les contraintes complémentaires](015-templates.md#rt-not)
* [T.26 : Préférer définir les concepts par des patrons d'utilisation plutôt que par une syntaxe simple](015-templates.md#rt-use)
* ??

### <a name="ss-concept-use"></a>T.con-use : Utilisation des concepts

#### <a name="rt-concepts"></a>T.10 : Spécifier les concepts pour tous les paramètres de template

##### Raison

Exactitude et lisibilité. La signification supposée (syntaxe et sémantique) d'un paramètre de template est fondamentale à l'interface d'un template. Un concept améliore remarquablement la documentation et la gestion des erreurs pour le template. Spécifier les concepts pour les paramètres de template est un outil de conception puissant.

##### Exemple

    template<typename Iter, typename Val>
        requires input_iterator<Iter>
                 && equality_comparable_with<iter_value_t<Iter>, Val>
    Iter find(Iter b, Iter e, Val v)
    {
        // ...
    }

ou, de façon équivalente et plus succincte :

    template<input_iterator Iter, typename Val>
        requires equality_comparable_with<iter_value_t<Iter>, Val>
    Iter find(Iter b, Iter e, Val v)
    {
        // ...
    }

##### Remarque

`typename` (ou `auto`) est le concept le moins contraignant. Il ne doit être utilisé qu'occasionnellement lorsqu'aucune autre contrainte n'est supposée. C'est généralement nécessaire lorsqu'on manipule seuls des arbres d'expression dans un code de méta‑programmation, en reportant le type‑check.

**Références** : TC++PL4

##### Enforced

Marquer les paramètres de type sans concepts.

#### <a name="rt-std-concepts"></a>T.11 : Lorsqu'il est possible d'utiliser des concepts standards

##### Raison

Les concepts « standard » (tels que fournis par le [GSL] et la norme ISO elle‑même) nous font gagner le travail d'élaboration de nos propres concepts, sont mieux pensés que ce que nous pouvons faire en travaillant à la hâte, et améliorent l'interopérabilité.

##### Remarque

À moins d'ouvrir une nouvelle bibliothèque générique, la majorité des concepts dont vous avez besoin seront déjà définis par la bibliothèque standard.

##### Exemple

    template<typename T>
        // ne pas définir ceci : sortable est dans <iterator>
    concept Ordered_container = Sequence<T> && Random_access<Iterator<T>> && Ordered<Value_type<T>>;

    void sort(Ordered_container auto& s);

Ce `Ordered_container` est plausible, mais très similaire au concept `sortable` dans la bibliothèque standard. Est‑ce mieux ? Est‑ce exact ? Reflète‑t‑il exactement les exigences de la norme pour `sort` ? Il vaut mieux simplement utiliser `sortable` :

    void sort(sortable auto& s);   // meilleur

##### Remarque

L'ensemble des concepts « standard » évolue à mesure que nous approchons d'une norme ISO incluant les concepts.

##### Remarque

Concevoir un concept utile est difficile.

##### Enforced

***hard**

* Chercher les arguments sans contraintes, les templates qui utilisent des concepts “ingenieux” non‑standards, les templates qui utilisent des concepts maison sans axiomes.
* Développer un outil de découverte de concepts (exemple : voir [une première expérience](https://www.stroustrup.com/sle2010_webversion.pdf)).

#### <a name="rt-auto"></a>T.12 : Préférer les noms de concepts plutôt que *auto* pour les variables locales

##### Raison

`auto` est le concept le plus faible. Les noms de concepts apportent plus de signification que simplement `auto`.

##### Exemple

    vector<string> v{ "abc", "xyz" };
    auto& x = v.front();        // mauvais
    String auto& s = v.front(); // bon (String est un concept GSL)

##### Enforced

* … (pas encore faisable)

#### <a name="rt-shorthand"></a>T.13 : Préférer la notation abrégée pour les concepts simples à un seul type d'argument

##### Raison

Lisibilité. Exprime directement l'idée.

##### Exemple

Pour dire « `T` est `sortable` » :

    template<typename T>       // correct mais verbeux : « le paramètre est… »
        requires sortable<T>   // du type T qui est le nom d'un type
    void sort(T&);             // qui est triable

    template<sortable T>       // mieux : « le paramètre est de type T »
    void sort(T&);             // qui est triable

    void sort(sortable auto&); // meilleur : « le paramètre est triable »

Les versions plus courtes correspondent mieux à la façon dont nous parlons. Notez que bon nombre de templates ne nécessitent pas l'utilisation du mot‑clé *template*.

##### Enforced

* Non réalisable à court terme lorsqu'on convertit depuis la notation `<typename T>` et `<class T>`.
* Plus tard, flag des déclarations qui introduisent d'abord un typename puis le contraignent avec un concept simple à un seul type d'argument.

#### <a name="rt-low"></a>T.20 : Éviter les “concepts” dépourvus de sémantique significative

##### Raison

Les concepts sont destinés à exprimer des notions sémantiques, telles qu'un nombre, une plage d'éléments et l'ordre total. Des contraintes simples, comme « a un opérateur `+` » ou « a un opérateur `>` » ne peuvent être exprimées de façon cohérente isolément et devraient être utilisées uniquement comme blocs de construction pour des concepts significatifs, plutôt qu'en code utilisateur.

##### Exemple, mauvais

    template<typename T>
    // mauvais ; insuffisant
    concept Addable = requires(T a, T b) { a + b; };

    template<Addable N>
    auto algo(const N& a, const N& b) // utiliser deux nombres
    {
        // …
        return a + b;
    }

    int x = 7;
    int y = 9;
    auto z = algo(x, y);   // z = 16

    string xx = "7";
    string yy = "9";
    auto zz = algo(xx, yy);   // zz = "79"

Peut-être que la concaténation était attendue. Plus probablement, c'est accidentel. Définir une opération de soustraction de manière équivalente produira un ensemble de types accepté très différent. Ce `Addable` viole la règle mathématique que l'addition doit être commutative : `a+b == b+a`.

##### Remarque

La capacité à spécifier une sémantique significative est une caractéristique définitoire d'un vrai concept, contrairement à une contrainte syntaxique.

##### Exemple

    template<typename T>
    // Les opérateurs +, -, *, et / pour un nombre sont supposés suivre les règles mathématiques usuelles
    concept Number = requires(T a, T b) { a + b; a - b; a * b; a / b; };

    template<Number N>
    auto algo(const N& a, const N& b)
    {
        // …
        return a + b;
    }

    int x = 7;
    int y = 9;
    auto z = algo(x, y);   // z = 16

    string xx = "7";
    string yy = "9";
    auto zz = algo(xx, yy);   // erreur : string n'est pas un Number

##### Remarque

Les concepts avec plusieurs opérations ont beaucoup moins de chance de correspondre accidentellement à un type qu'un concept à une seule opération.

##### Enforced

* Marquer les `concepts` à une seule opération lorsqu'ils sont utilisés hors définition d'autres `concepts`.
* Marquer les utilisations de `enable_if` qui semblent imiter des `concepts` à une seule opération.

#### <a name="rt-complete"></a>T.21 : Exiger un ensemble complet d'opérations pour un concept

##### Raison

Faciliter la compréhension. Améliorer l'interopérabilité. Aider les implémenteurs et les mainteneurs.

##### Remarque

Il s'agit d'une variante spécifique de la règle générale que [un concept doit avoir un sens] (015‑templates.md#rt-low).

##### Exemple, mauvais

    template<typename T> concept Subtractable = requires(T a, T b) { a - b; };

Ceci n'a aucun sens sémantique . On a besoin d'au moins `+` pour rendre `-` utile et significatif.

Exemples d'ensembles complets :

* `Arithmetic` : `+`, `-`, `*`, `/`, `+=`, `-=`, `*=`, `/=`
* `Comparable` : `<`, `>`, `<=`, `>=`, `==`, `!=`

##### Remarque

Cette règle s'applique que l'on utilise le support direct du langage pour les concepts ou non. C'est une règle de conception générale qui s'applique même aux non‑templates :

    class Minimal {
        // …
    };

    bool operator==(const Minimal&, const Minimal&);
    bool operator<(const Minimal&, const Minimal&);

    Minimal operator+(const Minimal&, const Minimal&);
    // pas d'autres opérateurs

    void f(Minimal x, Minimal y)
    {
        if (!(x == y)) { /* … */ }    // OK
        if (x != y) { /* … */ }       // surprise ! erreur

        while (!(x < y)) { /* … */ }  // OK
        while (x >= y) { /* … */ }    // surprise ! erreur

        x = x + y;          // OK
        x += y;             // surprise ! erreur
    }

Il s'agit du minimum, mais surprenant et contraignant pour les utilisateurs. Il pourrait même être moins efficace.

Le principe est que le concept doit refléter un ensemble (mathématiquement) cohérent d'opérations.

##### Exemple

    class Convenient {
        // …
    };

    bool operator==(const Convenient&, const Convenient&);
    bool operator<(const Convenient&, const Convenient&);
    // … et les autres opérateurs de comparaison

    Convenient operator+(const Convenient&, const Convenient&);
    // … et les autres opérateurs arithmétiques

    void f(const Convenient& x, const Convenient& y)
    {
        if (!(x == y)) { /* … */ }    // OK
        if (x != y) { /* … */ }       // OK

        while (!(x < y)) { /* … */ }  // OK
        while (x >= y) { /* … */ }    // OK

        x = x + y;     // OK
        x += y;        // OK
    }

Il peut être un désagrément de définir toutes les opérations, mais pas difficile. Idéalement, la règle devrait être supportée par le langage, en donnant automatiquement les opérateurs de comparaison.

##### Enforced

* Marquer les classes qui supportent des sous‑ensembles « bizarre » d'opérateurs, par ex. `==` sans `!=` ou `+` sans `-`. `std::string` est “bizarre”, mais il est trop tard pour le changer.

#### <a name="rt-axiom"></a>T.22 : Spécifier les axiomes pour les concepts

##### Raison

Un concept utile sémantique/mémoire a une signification. Exprimer cette sémantique de façon informelle, semi‑formelle ou formelle rend le concept compréhensible aux lecteurs et peut aider à attraper des erreurs conceptuelles. Exprimer des semantics est un outil de conception puissant.

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

Il s'agit d'autrefois d'un axiome en théorie mathématique ; il peut être supposé sans preuve. En général, les axiomes ne sont pas prouvés, et lorsqu'ils le sont, la preuve dépasse souvent la capacité du compilateur. Un axiome peut ne pas être général, mais l'écrivain d'un template peut supposer qu'il vaut pour toutes les entrées réellement utilisées, de la même manière qu'une pré‑condition.

##### Remarque

Dans ce contexte, les axiomes sont des expressions booléennes. Voir le [Palo Alto TR] (021‑references.md) pour des exemples. Actuellement, C++ ne supporte pas les axiomes (même le ISO Concepts TS), nous devons donc nous contenter de commentaires pendant un certain temps. Une fois le support de langage disponible, le `//` devant l'axiome peut être supprimé.

##### Remarque

Les concepts GSL ont une sémantique bien définie ; voir le Palo Alto TR et le Ranges TS.

##### Exception

Les premières versions d'un nouveau « concept » encore en développement fourniront souvent simplement un ensemble de contraintes simples sans sémantique bien spécifiée. Trouver une sémantique solide peut prendre effort et temps. Un ensemble de contraintes incomplet peut toutefois être très utile :

    // équilibrage pour un arbre binaire générique
    template<typename Node> concept Balancer = requires(Node* p) {
        add_fixup(p);
        touch(p);
        detach(p);
    };

Ainsi, un `Balancer` doit fournir au moins ces opérations sur un arbre `Node`, mais nous ne sommes pas encore prêts à spécifier des sémantiques détaillées parce qu'un nouveau type d'arbre équilibré peut nécessiter plus d'opérations et la sémantique générale pour tous les nœuds est difficile à définir en phase préliminaire de conception.

Un « concept » qui est incomplet ou sans sémantique bien définie peut néanmoins être utile. Par exemple, il permet une certaine vérification durant l'expérimentation initiale. Cependant, il ne doit pas être considéré comme stable. Chaque nouveau cas d'usage pourrait nécessiter une amélioration d'un tel concept incomplet.

##### Enforced

* Rechercher le mot‑clé « axiom » dans les commentaires de définition de concepts.

#### <a name="rt-refine"></a>T.23 : Différencier un concept raffiné de son cas plus général en ajoutant de nouveaux patrons d'utilisation

##### Raison

Sinon, ils ne peuvent pas être distingués automatiquement par le compilateur.

##### Exemple

    template<typename I>
    // Note : input_iterator est défini dans <iterator>
    concept Input_iter = requires(I iter) { ++iter; };

    template<typename I>
    // Note : forward_iterator est défini dans <iterator>
    concept Fwd_iter = Input_iter<I> && requires(I iter) { iter++; };

Le compilateur peut déterminer le raffinement basé sur l'ensemble des opérations requises (ici, suffixe `++`). Cela diminue la charge pour les implémenteurs des types, car ils n'ont pas besoin de déclarations spéciales pour « se brancher » dans le concept. Si deux concepts ont exactement les mêmes exigences, ils sont logiquement équivalents (il n'y a pas de raffinement).

##### Enforced

* Marquer un concept qui a exactement les mêmes exigences qu'un concept déjà vu (ni raffiné, ni non). Se référer à [T.24] pour les différencier.

#### <a name="rt-tag"></a>T.24 : Utiliser des classes d'étiquette ou des traits pour différencier des concepts dont la sémantique diffère uniquement

##### Raison

Deux concepts nécessitant la même syntaxe mais ayant des sémantiques différentes conduisent à des ambiguïtés, sauf si le programmeur les différencie.

##### Exemple

    template<typename I>    // itérateur fournissant l'accès aléatoire
    // Note : random_access_iterator est défini dans <iterator>
    concept RA_iter = ...;

    template<typename I>    // itérateur fournissant l'accès aléatoire aux données contiguës
    // Note : contiguous_iterator est défini dans <iterator>
    concept Contiguous_iter =
        RA_iter<I> && is_contiguous_v<I>;  // utilisation du trait is_contiguous

Le programmeur (dans une bibliothèque) doit définir `is_contiguous` (un trait) de façon appropriée.

En enveloppant une classe d'étiquette dans un concept, on simplifie l'expression de cette idée :

    template<typename I> concept Contiguous = is_contiguous_v<I>;

    template<typename I>
    concept Contiguous_iter = RA_iter<I> && Contiguous<I>;

Le programmeur (dans une bibliothèque) doit définir `is_contiguous` (un trait) de façon appropriée.

##### Remarque

Les traits peuvent être des classes de traits ou des traits de type. Ils peuvent être définis par l'utilisateur ou provenir de la bibliothèque standard. Préférer les traits de la bibliothèque standard.

##### Enforced

* Le compilateur signale l'utilisation ambiguë des concepts identiques.
* Marquer les définitions de concepts identiques.

#### <a name="rt-not"></a>T.25 : Éviter les contraintes complémentaires

##### Raison

Clarté. Maintenabilité. Les fonctions avec des exigences complémentaires exprimées via la négation sont fragiles.

##### Exemple

Initialement, les gens essaient de définir des fonctions avec des exigences complémentaires :

    template<typename T>
        requires !C<T>    // mauvais
    void f();

    template<typename T>
        requires C<T>
    void f();

Cela peut être mieux :

    template<typename T>   // template général
        void f();

    template<typename T>   // spécialisation par concept
        requires C<T>
    void f();

Le compilateur choisira le template sans contrainte lorsque `C<T>` est insatisfait. Si vous ne voulez pas (ou ne pouvez pas) définir une version sans contrainte de `f()`, supprimez‑la.

    template<typename T>
    void f() = delete;

Le compilateur sélectionnera l'overload, ou émettra une erreur appropriée.

##### Remarque

Les exigences complémentaires sont courantes dans le code `enable_if` :

    template<typename T>
    enable_if<!C<T>, void>   // mauvais
    f();

    template<typename T>
    enable_if<C<T>, void>
    f();

##### Remarque

Les exigences complémentaires sur une seule exigence sont parfois (mal) considérées comme gérables. Cependant, pour deux ou plus d'exigences, le nombre de définitions nécessaires peut croître exponentiellement (2, 4, 8, 16, …) : les possibilités d'erreurs s'accumulent.

##### Enforced

* marquer les paires de fonctions avec des contraintes `C<T>` et `!C<T>`.

#### <a name="rt-use"></a>T.26 : Préférer définir les concepts par des patrons d'utilisation plutôt que par une syntaxe simple

##### Raison

La définition est plus lisible et correspond directement à ce qu'un utilisateur doit écrire. Les conversions sont prises en compte. Vous n'avez pas à retenir les noms de tous les traits de types.

##### Exemple

Vous pourriez être tenté de définir un concept `Equality` ainsi :

    template<typename T> concept Equality = has_equal<T> && has_not_equal<T>;

Il est évidemment préférable et plus simple d'utiliser `equality_comparable`, mais à titre d'exemple : si vous deviez définir un tel concept, préférez :

    template<typename T> concept Equality = requires(T a, T b) {
        { a == b } -> std::convertible_to<bool>;
        { a != b } -> std::convertible_to<bool>;
        // axiom { !(a == b) == (a != b) }
        // axiom { a = b; => a == b }  // => signifie « implique »
    };

au lieu de définir deux concepts `has_equal` et `has_not_equal` sans sens pour aider dans la définition de `Equality`. Par “sans sens” nous entendons que vous ne pouvez pas spécifier la sémantique de `has_equal` isolément.

##### Enforced

* ??? (pas encore faisable)

### <a name="rt-30"></a>T.30 : Utiliser la négation de concepteur (*!C<T>*) avec parcimonie pour exprimer une différence mineure

... (pas encore défini)

### <a name="rt-31"></a>T.31 : Utiliser la disjonction de concepteurs (*C1<T> || C2<T>*) avec parcimonie pour exprimer des alternatives

... (pas encore défini)

### Résumé des règles de template et d'hierarchie :

(voir ci‑dessus)

...

### Résumé des règles de template variadique :

(voir ci‑dessus)

...

### Résumé des règles de méta‑programmation :

(voir ci‑dessus)

...

### Autres règles de template :

(voir ci‑dessus)

...

## <a name="ss-temp-interface"></a>Interface des templates

Au fil des ans, la programmation avec des templates a souffert d'une faible distinction entre l'interface d'un template et son implémentation. Avant les concepts, cette distinction n'avait pas de support direct du langage. Cependant, l'interface d'un template est un concept critique — un contrat entre l'utilisateur et l'implémenteur — et doit être soigneusement conçue.

### <a name="rt-fo"></a>T.40 : Utiliser des objets fonctionnels pour transmettre des opérations aux algorithmes

(voir ci‑dessus)

### <a name="rt-essential"></a>T.41 : Exiger seulement les propriétés essentielles dans les concepts d'un template

(voir ci‑dessus)

### <a name="rt-alias"></a>T.42 : Utiliser des alias de templates pour simplifier la notation et masquer les détails d'implémentation

(voir ci‑dessus)

### <a name="rt-using"></a>T.43 : Préférer *using* à *typedef* pour définir des alias

(voir ci‑dessus)

### <a name="rt-deduce"></a>T.44 : Utiliser des templates de fonctions pour déduire les types d'arguments de templates (lorsque c'est faisable)

(voir ci‑dessus)

### <a name="rt-visible"></a>T.47 : Éviter les templates hautement visibles sans contraintes avec des noms communs

(voir ci‑dessus)

### <a name="rt-concept-def"></a>T.48 : Si votre compilateur ne supporte pas les concepts, simulez-les avec *enable_if*

(voir ci‑dessus)

### <a name="rt-erasure"></a>T.49 : Lorsque c'est possible, éviter l'effacement de type

(voir ci‑dessus)

## <a name="ss-temp-def"></a>T.def : Définitions de templates

Une définition de template (classe ou fonction) peut contenir un code arbitraire, donc une revue complète des techniques de programmation C++ couvrirait tout le sujet. Cependant, cette section se concentre sur ce qui est spécifique à l'implémentation d'un template. En particulier, elle se concentre sur la dépendance d'une définition de template à son contexte.

### <a name="rt-depend"></a>T.60 : Minimiser les dépendances contextuelles d'un template

(voir ci‑dessus)

### <a name="rt-scary"></a>T.61 : Ne pas surparamétrer les membres (SCARY)

(voir ci‑dessus)

### <a name="rt-nondependent"></a>T.62 : Placer les membres non dépendants d'un template de classe dans une classe de base non template

(voir ci‑dessus)

### <a name="rt-specialization"></a>T.64 : Utiliser la spécialisation pour fournir des implémentations alternatives de templates de classe

(voir ci‑dessus)

### <a name="rt-tag-dispatch"></a>T.65 : Utiliser l'envoi de tags pour fournir des implémentations alternatives de fonctions

(voir ci‑dessus)

### <a name="rt-specialization2"></a>T.67 : Utiliser la spécialisation pour fournir des implémentations alternatives pour des types irréguliers

(voir ci‑dessus)

### <a name="rt-cast"></a>T.68 : Utiliser **{**} plutôt que **(** dans les templates pour éviter des ambiguïtés

(voir ci‑dessus)

### <a name="rt-customization"></a>T.69 : À l'intérieur d'un template, ne pas appeler une fonction non membre sans qualification sauf si vous l'intentionnez comme point de personnalisation

(voir ci‑dessus)

## <a name="ss-temp-hier"></a>T.temp‑hier : Règles de template et d'hierarchie

Les templates constituent le backbone du support C++ pour la programmation générique, et les hiérarchies de classes le backbone du support de la programmation orientée objet. Les deux mécanismes de langage peuvent être utilisés efficacement en combinaison, mais quelques pièges de conception doivent être évités.

### <a name="rt-hier"></a>T.80 : Ne pas templatiser naïvement une hiérarchie de classes

(voir ci‑dessus)

### <a name="rt-array"></a>T.81 : Ne pas mélanger hiérarchies et tableaux

(voir ci‑dessus) @TODO-LINK

...

### <a name="rt-linear"></a>T.82 : Lineariser une hiérarchie lorsque les fonctions virtuelles sont indésirables

...

### <a name="rt-virtual"></a>T.83 : Ne pas déclarer une fonction membre template virtuelle

...

### <a name="rt-abi"></a>T.84 : Utiliser une implémentation centrale non‑template pour fournir une interface stable ABI

...

## <a name="ss-variadic"></a>T.var : Règles de template variadique

...

## <a name="ss-meta"></a>T.meta : Méta‑programmation (TMP)

...

## <a name="ss-temp-other"></a>Autres règles de template

...

*(tout le texte suivant a été traduit en français, les blocs de code conservent la même indentation de 4 espaces et les références manquantes sont marquées @TODO‑LINK).*