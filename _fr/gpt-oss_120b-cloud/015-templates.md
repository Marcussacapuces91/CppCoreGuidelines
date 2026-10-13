# <a name="s-templates"></a>T : Templates et programmation générique

La programmation générique désigne la programmation utilisant des types et des algorithmes paramétrés par des types, des valeurs et des algorithmes.  
En C++, la programmation générique est prise en charge par les mécanismes du langage `template`.

Les arguments des fonctions génériques sont caractérisés par un ensemble d’exigences sur les types d’arguments et les valeurs impliquées.  
En C++, ces exigences sont exprimées par des prédicats évalués à la compilation appelés **concepts**.

Les templates peuvent également servir à la **métaprogrammation**, c’est‑à‑dire à des programmes qui composent du code à la compilation.

Une notion centrale de la programmation générique est le **concept** : exigences sur les arguments de template présentées sous forme de prédicats à la compilation.  
Les concepts ont été normalisés dans C++20, bien qu’ils aient d’abord été introduits (avec une syntaxe légèrement antérieure) dans GCC 6.1.

### Résumé des règles d’utilisation des templates

* [T.1 : Utiliser les templates pour augmenter le niveau d’abstraction du code](015-templates.md#rt-raise)  
* [T.2 : Utiliser les templates pour exprimer des algorithmes applicables à de nombreux types d’argument](015-templates.md#rt-algo)  
* [T.3 : Utiliser les templates pour exprimer des conteneurs et des plages](015-templates.md#rt-cont)  
* [T.4 : Utiliser les templates pour manipuler des arbres syntaxiques](015-templates.md#rt-expr)  
* [T.5 : Combiner les techniques génériques et OO afin d’amplifier leurs forces, pas leurs coûts](015-templates.md#rt-generic-oo)

### Résumé des règles d’utilisation des concepts

* [T.10 : Spécifier des concepts pour tous les arguments de template](015-templates.md#rt-concepts)  
* [T.11 : Utiliser les concepts standard chaque fois que possible](015-templates.md#rt-std-concepts)  
* [T.12 : Préférer les noms de concepts à `auto` pour les variables locales](015-templates.md#rt-auto)  
* [T.13 : Préférer la notation raccourcie pour les concepts simples à un type d’argument](015-templates.md#rt-shorthand)  
* ??? @TODO‑LINK

### Résumé des règles de définition des concepts

* [T.20 : Éviter les concepts dépourvus de sémantique significative](015-templates.md#rt-low)  
* [T.21 : Exiger un ensemble complet d’opérations pour un concept](015-templates.md#rt-complete)  
* [T.22 : Spécifier les axiomes pour les concepts](015-templates.md#rt-axiom)  
* [T.23 : Différencier un concept raffiné de son cas plus général en ajoutant de nouveaux modèles d’utilisation](015-templates.md#rt-refine)  
* [T.24 : Utiliser des classes d’étiquettes ou des traits pour différencier des concepts qui ne diffèrent que par leur sémantique](015-templates.md#rt-tag)  
* [T.25 : Éviter les contraintes complémentaires](015-templates.md#rt-not)  
* [T.26 : Préférer définir les concepts en fonction de modèles d’utilisation plutôt que d’une simple syntaxe](015-templates.md#rt-use)  
* ??? @TODO‑LINK

### Résumé des règles d’interface des templates

* [T.40 : Utiliser des objets fonctionnels pour transmettre des opérations aux algorithmes](015-templates.md#rt-fo)  
* [T.41 : Exiger uniquement les propriétés essentielles dans les concepts d’un template](015-templates.md#rt-essential)  
* [T.42 : Utiliser des alias de template pour simplifier la notation et masquer les détails d’implémentation](015-templates.md#rt-alias)  
* [T.43 : Préférer `using` à `typedef` pour définir des alias](015-templates.md#rt-using)  
* [T.44 : Utiliser des templates de fonction pour déduire les types d’argument d’un template de classe (dans la mesure du possible)](015-templates.md#rt-deduce)  
* [T.46 : (supprimé)](015-templates.md#rt-regular)  
* [T.47 : Éviter les templates non contraints très visibles avec des noms courants](015-templates.md#rt-visible)  
* [T.48 : Si votre compilateur ne supporte pas les concepts, les simuler avec `enable_if`](015-templates.md#rt-concept-def)  
* [T.49 : Éviter, lorsque possible, l’effacement de type (type‑erasure)](015-templates.md#rt-erasure)

### Résumé des règles de définition des templates

* [T.60 : Minimiser les dépendances contextuelles d’un template](015-templates.md#rt-depend)  
* [T.61 : Ne pas sur‑paramétrer les membres (SCARY)](015-templates.md#rt-scary)  
* [T.62 : Placer les membres de classe template non‑dépendants dans une classe de base non‑template](015-templates.md#rt-nondependent)  
* [T.64 : Utiliser la spécialisation pour fournir des implémentations alternatives de templates de classe](015-templates.md#rt-specialization)  
* [T.65 : Utiliser le dispatch d’étiquette pour fournir des implémentations alternatives de fonctions](015-templates.md#rt-tag-dispatch)  
* [T.67 : Utiliser la spécialisation pour fournir des implémentations alternatives pour les types irréguliers](015-templates.md#rt-specialization2)  
* [T.68 : Utiliser `{}` plutôt que `()` à l’intérieur des templates pour éviter les ambiguïtés](015-templates.md#rt-cast)  
* [T.69 : Dans un template, ne pas appeler de fonction non‑membre non qualifiée à moins d’en faire un point de personnalisation](015-templates.md#rt-customization)  
* ??? @TODO‑LINK

### Résumé des règles de combinaison templates / hiérarchie

* [T.80 : Ne pas templatiser naïvement une hiérarchie de classes](015-templates.md#rt-hier)  
* [T.81 : Ne pas mélanger hiérarchies et tableaux](015-templates.md#rt-array) @TODO‑LINK  
* [T.82 : Linéariser une hiérarchie lorsque les fonctions virtuelles sont indésirables](015-templates.md#rt-linear)  
* [T.83 : Ne pas déclarer un template de fonction membre virtuel](015-templates.md#rt-virtual)  
* [T.84 : Utiliser une implémentation centrale non‑template pour fournir une interface stable au niveau de l’ABI](015-templates.md#rt-abi)  
* ??? @TODO‑LINK

### Résumé des règles des templates variadiques

* [T.100 : Utiliser les templates variadiques lorsqu’une fonction doit accepter un nombre variable d’arguments de types variés](015-templates.md#rt-variadic)  
* [T.101 : ??? Comment passer des arguments à un template variadique ???](015-templates.md#rt-variadic-pass) @TODO‑LINK  
* [T.102 : ??? Comment traiter les arguments d’un template variadique ???](015-templates.md#rt-variadic-process) @TODO‑LINK  
* [T.103 : Ne pas utiliser les templates variadiques pour des listes d’arguments homogènes](015-templates.md#rt-variadic-not)  
* ??? @TODO‑LINK

### Résumé des règles de métaprogrammation (TMP)

* [T.120 : Utiliser la métaprogrammation de template uniquement lorsque cela est réellement nécessaire](015-templates.md#rt-metameta)  
* [T.121 : Utiliser la métaprogrammation de template principalement pour émuler les concepts](015-templates.md#rt-emulate)  
* [T.122 : Utiliser les templates (généralement des alias de template) pour calculer des types à la compilation](015-templates.md#rt-tmp)  
* [T.123 : Utiliser des fonctions `constexpr` pour calculer des valeurs à la compilation](015-templates.md#rt-fct)  
* [T.124 : Privilégier l’utilisation des facilities de métaprogrammation du standard](015-templates.md#rt-std-tmp)  
* [T.125 : Si vous devez aller au‑delà des facilities TMP du standard, utilisez une bibliothèque existante](015-templates.md#rt-lib)  
* ??? @TODO‑LINK

### Résumé des autres règles liées aux templates

* [T.140 : Si une opération peut être réutilisée, lui donner un nom](015-templates.md#rt-name)  
* [T.141 : Utiliser une lambda anonyme si vous avez besoin d’un simple objet fonction dans un seul endroit](015-templates.md#rt-lambda)  
* [T.142 : Utiliser des variables de template pour simplifier la notation](015-templates.md#rt-var)  
* [T.143 : Ne pas écrire de code non‑générique de façon non intentionnelle](015-templates.md#rt-non-generic)  
* [T.144 : Ne pas spécialiser les templates de fonction](015-templates.md#rt-specialize-function)  
* [T.150 : Vérifier qu’une classe satisfait un concept à l’aide de `static_assert`](015-templates.md#rt-check-class)  
* ??? @TODO‑LINK

---

## <a name="ss-gp"></a>T.gp : Programmation générique

La programmation générique est la programmation qui utilise des types et des algorithmes paramétrés par des types, des valeurs et des algorithmes.

### <a name="rt-raise"></a>T.1 : Utiliser les templates pour augmenter le niveau d’abstraction du code

##### Raison  
Généralité. Réutilisation. Efficacité. Encourage la définition cohérente des types utilisateur.

##### Exemple, mauvais  

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

En supposant que `Incrementable` ne supporte pas `+` et que `Simple_number` ne supporte pas `+=`, nous sur‑contraignons les implémenteurs de `sum1` et `sum2`.  
De plus, nous ratons une occasion de généralisation.

##### Exemple  

    template<typename T>
        requires Arithmetic<T>
    T sum(vector<T>& v, T s)
    {
        for (auto x : v) s += x;
        return s;
    }

En supposant que le concept `Arithmetic` requiert à la fois `+` et `+=`, nous contraignons l’utilisateur de `sum` à fournir un type arithmétique complet. Ce n’est pas la contrainte minimale, mais cela donne à l’implémenteur d’algorithmes la liberté nécessaire et garantit que tout type `Arithmetic` peut être utilisé pour de nombreux algorithmes.

Pour plus de généralité et de réutilisabilité, on pourrait également employer un concept plus général tel que `Container` ou `Range` au lieu de se limiter à `vector`.

##### Note  
Si l’on définit un template qui n’exige que les opérations strictement nécessaires à une implémentation particulière (par ex. n’exiger que `+=` au lieu de `=` et `+`), on sur‑contraint les mainteneurs. L’objectif est de minimiser les exigences sur les arguments de template, mais l’ensemble absolument minimal d’une implémentation a rarement un sens sémantique clair.

##### Note  
Les templates peuvent exprimer essentiellement tout (ils sont Turing‑complets), mais le but de la programmation générique (en s’appuyant sur les templates) est de généraliser efficacement les opérations/algorithmes sur un ensemble de types partageant des propriétés sémantiques similaires.

##### Application  

* Signaler les algorithmes dont les exigences sont « trop simples », par exemple l’utilisation directe d’opérateurs spécifiques sans concept.  
* Ne pas signaler la définition des concepts « trop simples » eux‑mêmes ; ils peuvent simplement servir de blocs de construction pour des concepts plus utiles.

---

### <a name="rt-algo"></a>T.2 : Utiliser les templates pour exprimer des algorithmes applicables à de nombreux types d’argument

##### Raison  
Généralité. Réduction de la taille du code source. Interopérabilité. Réutilisation.

##### Exemple  

    // Base de la STL : l’algorithme `find` fonctionne avec n’importe quelle plage d’entrée.
    template<typename Iter, typename Val>
        // requires Input_iterator<Iter>
        //       && Equality_comparable<Value_type<Iter>, Val>
    Iter find(Iter b, Iter e, Val v)
    {
        // ...
    }

##### Note  
N’utilisez pas de template à moins d’avoir réellement besoin de plusieurs types d’argument.  
Ne sur‑abstrairez pas inutilement.

##### Application  
??? (nécessite une analyse humaine)  

---

### <a name="rt-cont"></a>T.3 : Utiliser les templates pour exprimer des conteneurs et des plages

##### Raison  
Les conteneurs ont besoin d’un type d’élément ; le faire paramétrer par un argument de template est général, réutilisable et sûr du point de vue du typage. Cela évite les astuces fragiles ou inefficaces. Convention : c’est ainsi que la STL le fait.

##### Exemple  

    template<typename T>
        // requires Regular<T>
    class Vector {
        // ...
        T* elem;   // points to sz Ts
        int sz;
    };

    Vector<double> v(10);
    v[7] = 9.9;

##### Exemple, mauvais  

    class Container {
        // ...
        void* elem;   // pointe vers size éléments d’un type quelconque
        int sz;
    };

    Container c(10, sizeof(double));
    ((double*) c.elem)[7] = 9.9;

Ce code ne reflète pas directement l’intention du programmeur et masque la structure du programme au système de types et à l’optimiseur.

Cacher le `void*` derrière des macros ne fait que masquer les problèmes et introduit de nouvelles sources de confusion.

**Exceptions** : si vous avez besoin d’une interface stable au niveau de l’ABI, vous devrez peut‑être fournir une implémentation de base et exprimer le template (type‑safe) en termes de celle‑ci. Voir [Stable base](015-templates.md#rt-abi).

##### Application  

* Signaler les usages de `void*` et de casts en dehors du code d’implémentation bas‑niveau.

---

### <a name="rt-expr"></a>T.4 : Utiliser les templates pour manipuler des arbres syntaxiques

##### Raison  
???

##### Exemple  

    ???

**Exceptions** : ???

---

### <a name="rt-generic-oo"></a>T.5 : Combiner les techniques génériques et OO afin d’amplifier leurs forces, pas leurs coûts

##### Raison  
Les techniques génériques et orientées objet sont complémentaires.

##### Exemple (static → dynamic)  

    class Command {
        // fonctions virtuelles pures
    };

    // implémentations
    template</*…*/>
    class ConcreteCommand : public Command {
        // implémenter les virtuels
    };

##### Exemple (dynamic → static)

    // Offrir une interface confortable, liée statiquement, mais dispatcher dynamiquement à l’intérieur.

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

##### Note  
Dans un template, les fonctions non‑virtuelles ne sont instanciées que si elles sont utilisées ; les fonctions virtuelles, en revanche, le sont à chaque instanciation. Cela peut gonfler la taille du code et contraindre un type générique en instanciant du code qui n’est jamais utilisé. Évitez ce piège, même si les facettes de la bibliothèque standard ont commis cette erreur.

##### Voir aussi  

* ref ???
* ref ???
* ref ???

##### Application  

Voir les références aux règles plus spécifiques.

---

## <a name="ss-concepts"></a>T.concepts : Règles relatives aux concepts

Les concepts, introduits dans C++20, permettent de spécifier les exigences pour les arguments de template. Ils sont essentiels à la pensée générique et constituent la base d’une grande partie des bibliothèques C++ futures (standard et tierces).  
Cette section suppose la prise en charge des concepts.

### Résumé des règles d’utilisation des concepts

* [T.10 : Spécifier les concepts pour tous les arguments de template](015-templates.md#rt-concepts)  
* [T.11 : Utiliser les concepts standard chaque fois que possible](015-templates.md#rt-std-concepts)  
* [T.12 : Préférer les noms de concepts à `auto` pour les variables locales](015-templates.md#rt-auto)  
* [T.13 : Préférer la notation raccourcie pour les concepts simples à un type d’argument](015-templates.md#rt-shorthand)  
* ??? @TODO‑LINK

### Résumé des règles de définition des concepts

* [T.20 : Éviter les concepts dépourvus de sémantique significative](015-templates.md#rt-low)  
* [T.21 : Exiger un ensemble complet d’opérations pour un concept](015-templates.md#rt-complete)  
* [T.22 : Spécifier les axiomes pour les concepts](015-templates.md#rt-axiom)  
* [T.23 : Différencier un concept raffiné de son cas plus général en ajoutant de nouveaux modèles d’utilisation](015-templates.md#rt-refine)  
* [T.24 : Utiliser des classes d’étiquettes ou des traits pour différencier les concepts qui ne diffèrent que par leur sémantique](015-templates.md#rt-tag)  
* [T.25 : Éviter les contraintes complémentaires](015-templates.md#rt-not)  
* [T.26 : Préférer définir les concepts en fonction de modèles d’utilisation plutôt que d’une simple syntaxe](015-templates.md#rt-use)  
* ??? @TODO‑LINK

---

## <a name="ss-concept-use"></a>T.con‑use : Utilisation des concepts

### <a name="rt-concepts"></a>T.10 : Spécifier les concepts pour tous les arguments de template

##### Raison  
Correction et lisibilité.  
Le sens (syntaxe et sémantique) présumé d’un argument de template constitue le coeur de l’interface du template. Un concept améliore radicalement la documentation et le diagnostic d’erreurs. Spécifier les concepts pour les arguments de template est un puissant outil de conception.

##### Exemple  

    template<typename Iter, typename Val>
        requires input_iterator<Iter>
                 && equality_comparable_with<iter_value_t<Iter>, Val>
    Iter find(Iter b, Iter e, Val v)
    {
        // ...
    }

ou, de façon plus succincte :

    template<input_iterator Iter, typename Val>
        requires equality_comparable_with<iter_value_t<Iter>, Val>
    Iter find(Iter b, Iter e, Val v)
    {
        // ...
    }

##### Note  
`typename` (ou `auto`) est le concept le moins contraignant. Il ne doit être utilisé que très rarement, lorsque l’on ne peut supposer rien de plus que « c’est un type ». Ceci est généralement nécessaire uniquement dans le cadre de la métaprogrammation où l’on manipule des arbres d’expressions pures, en différant la vérification de type.

**Références** : TC++PL4

##### Application  

* Signaler les arguments de type de template dépourvus de concept.

---

### <a name="rt-std-concepts"></a>T.11 : Utiliser les concepts standard chaque fois que possible

##### Raison  
Les concepts « standard » (fournis par la [GSL](#gsl-guidelines-support-library) et la norme ISO elle‑même) nous évitent de devoir inventer nos propres concepts, sont mieux pensés que ce que l’on peut fabriquer à la hâte et améliorent l’interopérabilité.

##### Note  
À moins que vous ne créiez une nouvelle bibliothèque générique, la plupart des concepts dont vous avez besoin sont déjà définis dans la bibliothèque standard.

##### Exemple  

    template<typename T>
        // ne définissez pas cela : sortable se trouve dans <iterator>
    concept Ordered_container = Sequence<T> && Random_access<Iterator<T>> && Ordered<Value_type<T>>;

    void sort(Ordered_container auto& s);

Ce `Ordered_container` est plausible, mais il ressemble fortement au concept `sortable` de la bibliothèque standard.  
Plutôt que d’introduire un nouveau concept, utilisez simplement `sortable` :

    void sort(sortable auto& s);   // meilleur

##### Note  
L’ensemble des concepts « standard » évolue à mesure que la norme ISO les intègre.

##### Note  
Concevoir un concept utile est un défi.

##### Application  

* Repérer les arguments non contraints, les templates qui utilisent des concepts « non‑standard » ou « fait‑maison » sans axiomes.  
* Développer un outil de découverte de concepts (voir [une première expérience](https://www.stroustrup.com/sle2010_webversion.pdf)).

---

### <a name="rt-auto"></a>T.12 : Préférer les noms de concepts à `auto` pour les variables locales

##### Raison  
`auto` est le concept le plus faible. Les noms de concepts transmettent plus de sens qu’un simple `auto`.

##### Exemple  

    vector<string> v{ "abc", "xyz" };
    auto& x = v.front();        // mauvais
    String auto& s = v.front(); // bon (String est un concept GSL)

##### Application  

* ???

---

### <a name="rt-shorthand"></a>T.13 : Préférer la notation raccourcie pour les concepts simples à un type d’argument

##### Raison  
Lisibilité. Expression directe d’une idée.

##### Exemple  

Pour dire « `T` est `sortable` » :

    template<typename T>       // Correct mais verbeux : « Le paramètre est
        requires sortable<T>   // de type T qui porte le concept sortable »
    void sort(T&);             // …

    template<sortable T>       // Mieux : « Le paramètre est de type T
    void sort(T&);             // qui est Sortable »

    void sort(sortable auto&); // Optimal : « Le paramètre est Sortable »

Les formes plus courtes correspondent mieux à notre façon de parler. Notez que de nombreux templates n’ont même pas besoin du mot‑clé `template`.

##### Application  

* Pas réalisable à court terme pendant la conversion du style `<typename T>`/`<class T>`.  
* Plus tard, signaler les déclarations qui introduisent d’abord un `typename` puis le contraignent avec un concept simple à type unique.

---

## <a name="ss-concepts-def"></a>T.concepts.def : Règles de définition des concepts

Définir de bons concepts n’est pas une mince affaire.  
Les concepts sont destinés à représenter des notions fondamentales dans un domaine d’application (d’où le nom « concepts »).  

Composer à la hâte un ensemble de contraintes syntaxiques pour les arguments d’une classe ou d’un algorithme n’est pas ce pour quoi les concepts ont été conçus et ne permet pas de profiter pleinement du mécanisme.

Il est évident que la définition de concepts est la plus utile lorsque le code cible un compilateur C++20 (ou plus récent).  
Mais la définition de concepts, en soi, est une technique de conception précieuse qui aide à détecter les erreurs conceptuelles et à nettoyer les concepts d’une implémentation.

### <a name="rt-low"></a>T.20 : Éviter les concepts « sans sémantique significative »

##### Raison  
Les concepts sont censés exprimer des notions sémantiques, telles que « un nombre », « une plage d’éléments » ou « totalement ordonné ».  
Des contraintes triviales comme « possède un opérateur `+` » ou « possède un `>` » ne sont pas significatives isolément ; elles ne doivent être utilisées que comme blocs de construction pour des concepts signifiants, et non dans le code utilisateur.

##### Exemple, mauvais  

    template<typename T>
    // mauvais ; insuffisant
    concept Addable = requires(T a, T b) { a + b; };

    template<Addable N>
    auto algo(const N& a, const N& b) // utilise deux nombres
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

Le résultat de la concaténation est peut‑être attendu, mais il s’agit très probablement d’un accident.  
Définir `Addable` de la sorte viole la règle mathématique selon laquelle l’addition doit être commutative : `a+b == b+a`.

##### Note  
La capacité à spécifier une sémantique significative est la caractéristique distinctive d’un vrai concept, à la différence d’une simple contrainte syntaxique.

##### Exemple  

    template<typename T>
    // Les opérateurs +, -, *, / pour un nombre sont supposés suivre les règles mathématiques habituelles
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
    auto zz = algo(xx, yy);   // erreur : `string` n’est pas un `Number`

##### Note  
Les concepts avec plusieurs opérations ont beaucoup moins de chances de correspondre accidentellement à un type que les concepts à opération unique.

##### Application  

* Signaler les concepts à opération unique lorsqu’ils sont utilisés en dehors de la définition d’autres concepts.  
* Signaler les usages de `enable_if` qui semblent simuler des concepts à opération unique.

---

### <a name="rt-complete"></a>T.21 : Exiger un ensemble complet d’opérations pour un concept

##### Raison  
Facilité de compréhension.  
Interopérabilité améliorée.  
Aide les implémenteurs et les mainteneurs.

##### Note  
Il s’agit d’une variante précise de la règle générale : « un concept doit avoir un sens sémantique » (voir [T.20](015-templates.md#rt-low)).

##### Exemple, mauvais  

    template<typename T> concept Subtractable = requires(T a, T b) { a - b; };

Ce concept n’a aucun sens sémantique. Vous avez besoin d’au moins `+` pour que `-` soit significatif et utile.

Exemples d’ensembles complets :

* `Arithmetic` : `+`, `-`, `*`, `/`, `+=`, `-=`, `*=`, `/=`  
* `Comparable` : `<`, `>`, `<=`, `>=`, `==`, `!=`

##### Note  
Cette règle s’applique que l’on utilise ou non la prise en charge native des concepts. C’est une règle de conception générale qui vaut aussi pour le code non‑template :

    class Minimal {
        // …
    };

    bool operator==(const Minimal&, const Minimal&);
    bool operator<(const Minimal&, const Minimal&);

    Minimal operator+(const Minimal&, const Minimal&);
    // aucune autre surcharge

    void f(Minimal x, Minimal y)
    {
        if (!(x == y)) { /* … */ }    // OK
        if (x != y) { /* … */ }        // surprise ! erreur

        while (!(x < y)) { /* … */ }   // OK
        while (x >= y) { /* … */ }    // surprise ! erreur

        x = x + y;                     // OK
        x += y;                        // surprise ! erreur
    }

Cette interface est minimale, mais surprenante et contraignante pour les utilisateurs ; elle pourrait même être moins efficace.

##### Exemple  

    class Convenient {
        // …
    };

    bool operator==(const Convenient&, const Convenient&);
    bool operator<(const Convenient&, const Convenient&);
    // … et les autres opérateurs de comparaison …

    Convenient operator+(const Convenient&, const Convenient&);
    // … et les autres opérateurs arithmétiques …

    void f(const Convenient& x, const Convenient& y)
    {
        if (!(x == y)) { /* … */ }    // OK
        if (x != y) { /* … */ }        // OK

        while (!(x < y)) { /* … */ }   // OK
        while (x >= y) { /* … */ }    // OK

        x = x + y;                     // OK
        x += y;                        // OK
    }

Définir toutes les surcharges peut être fastidieux, mais pas impossible. Idéalement, le langage fournirait ces opérateurs par défaut.

##### Application  

* Signaler les classes qui ne supportent qu’un sous‑ensemble « étrange » d’un groupe d’opérateurs (par ex. `==` mais pas `!=`, ou `+` mais pas `-`).  
  (*`std::string` est un cas « étrange », mais il est trop tard pour le changer.*)

---

### <a name="rt-axiom"></a>T.22 : Spécifier les axiomes pour les concepts

##### Raison  
Un concept utile possède un sens sémantique.  
Exprimer ces sémantiques de façon informelle, semi‑formelle ou formelle rend le concept compréhensible pour les lecteurs ; l’effort de les formuler permet souvent de repérer des erreurs conceptuelles. Les axiomes sont donc un puissant outil de conception.

##### Exemple  

    template<typename T>
        // Les opérateurs +, -, *, / d’un nombre sont supposés suivre les règles mathématiques usuelles
        // axiom(T a, T b) { a + b == b + a; a - a == 0; a * (b + c) == a * b + a * c; /*…*/ }
        concept Number = requires(T a, T b) {
            { a + b } -> convertible_to<T>;
            { a - b } -> convertible_to<T>;
            { a * b } -> convertible_to<T>;
            { a / b } -> convertible_to<T>;
        };

##### Note  
Il s’agit d’un **axiome** au sens mathématique : on l’accepte sans preuve.  
En général, les axiomes ne sont pas démontrables, et lorsqu’ils le sont, la preuve dépasse les capacités du compilateur. Un axiome peut ne pas être universel ; le programmeur peut simplement supposer qu’il est valable pour les entrées réellement utilisées (similaire à une précondition).

##### Note  
Dans ce contexte, les axiomes sont des expressions booléennes. Voir le [Palo Alto TR](021-references.md) pour des exemples. Actuellement, C++ ne supporte pas les axiomes (même le Concepts TS), donc nous nous contentons de commentaires pendant un certain temps. Quand le support sera disponible, le `//` pourra être retiré.

##### Note  
Les concepts de la GSL ont des sémantiques bien définies ; voir le Palo Alto TR et le Ranges TS.

##### Exception  
Les premières versions d’un nouveau « concept » sont souvent incomplètes ; on ne spécifie que des contraintes syntaxiques sans sémantique définie.  
Un concept incomplet peut néanmoins être très utile : il permet un certain contrôle pendant la phase d’expérimentation.  
Exemple :

    // équilibrage pour un arbre binaire générique
    template<typename Node> concept Balancer = requires(Node* p) {
        add_fixup(p);
        touch(p);
        detach(p);
    };

Ici, `Balancer` doit fournir au moins ces opérations sur un nœud d’arbre, mais on n’est pas encore prêt à préciser la sémantique exacte.

##### Application  

* Rechercher le mot « axiom » dans les commentaires des définitions de concepts.

---

### <a name="rt-refine"></a>T.23 : Différencier un concept raffiné de son cas plus général en ajoutant de nouveaux modèles d’utilisation

##### Raison  
Sans cela, le compilateur ne peut pas les distinguer automatiquement.

##### Exemple  

    template<typename I>
    // Note : `input_iterator` est défini dans <iterator>
    concept Input_iter = requires(I iter) { ++iter; };

    template<typename I>
    // Note : `forward_iterator` est défini dans <iterator>
    concept Fwd_iter = Input_iter<I> && requires(I iter) { iter++; };

Le compilateur peut déterminer le raffinement à partir des ensembles d’opérations requis (ici, l’opérateur postfixe `++`).  
Cela réduit la charge sur les implémenteurs, qui n’ont pas besoin de déclarations spéciales pour « brancher » le concept.  
Si deux concepts ont exactement les mêmes exigences, ils sont logiquement équivalents (pas de raffinement).

##### Application  

* Signaler un concept qui possède exactement les mêmes exigences qu’un autre déjà vu (aucun n’est plus raffiné).  
  Pour les désambiguïser, voir [T.24](015-templates.md#rt-tag).

---

### <a name="rt-tag"></a>T.24 : Utiliser des classes d’étiquettes ou des traits pour différencier les concepts qui ne diffèrent que par leur sémantique

##### Raison  
Deux concepts ayant la même syntaxe mais une sémantique différente entraînent une ambiguïté, sauf si le programmeur les différencie explicitement.

##### Exemple  

    template<typename I>    // itérateur à accès aléatoire
    // Note : `random_access_iterator` est défini dans <iterator>
    concept RA_iter = ...;

    template<typename I>    // itérateur à accès aléatoire sur des données contiguës
    // Note : `contiguous_iterator` est défini dans <iterator>
    concept Contiguous_iter =
        RA_iter<I> && is_contiguous_v<I>;  // via le trait `is_contiguous`

Le programmeur (dans une bibliothèque) doit fournir le trait `is_contiguous` adéquat.

Envelopper une classe d’étiquette dans un concept simplifie l’expression :

    template<typename I> concept Contiguous = is_contiguous_v<I>;

    template<typename I>
    concept Contiguous_iter = RA_iter<I> && Contiguous<I>;

##### Note  

* Les traits peuvent être des classes de traits ou des traits de type.  
* Ils peuvent être définis par l’utilisateur ou fournis par la bibliothèque standard.  
* Privilégier les traits de la bibliothèque standard.

##### Application  

* Le compilateur signale les usages ambigus de concepts identiques.  
* Signaler la définition de concepts identiques.

---

### <a name="rt-not"></a>T.25 : Éviter les contraintes complémentaires

##### Raison  
Clarté. Maintenabilité.  
Les fonctions dont les exigences sont complémentaires via la négation sont fragiles.

##### Exemple  

    template<typename T>
        requires !C<T>    // mauvais
    void f();

    template<typename T>
        requires C<T>
    void f();

Mieux vaut :

    template<typename T>   // template général
        void f();

    template<typename T>   // spécialisation par concept
        requires C<T>
    void f();

Le compilateur choisira le template non contraint uniquement si `C<T>` n’est pas satisfait. Si vous ne voulez pas (ou ne pouvez pas) fournir de version non contrainte, supprimez‑la :

    template<typename T>
    void f() = delete;

Le compilateur sélectionnera alors la surcharge ou émettra une erreur appropriée.

##### Note  
Les contraintes complémentaires sont fréquentes avec `enable_if` :

    template<typename T>
    enable_if<!C<T>, void>   // mauvais
    f();

    template<typename T>
    enable_if<C<T>, void>
    f();

##### Note  
Lorsque plusieurs exigences sont impliquées, le nombre de définitions nécessaires croît exponentiellement (2, 4, 8, 16, …).  
Exemple :

    C1<T> && C2<T>
    !C1<T> && C2<T>
    C1<T> && !C2<T>
    !C1<T> && !C2<T>

Les opportunités d’erreur se multiplient.

##### Application  

* Signaler les paires de fonctions contenant `C<T>` et `!C<T>` comme contraintes.

---

### <a name="rt-use"></a>T.26 : Préférer définir les concepts en fonction de modèles d’utilisation plutôt que d’une simple syntaxe

##### Raison  
La définition devient plus lisible et correspond directement à ce que l’utilisateur doit écrire.  
Les conversions sont prises en compte ; vous n’avez pas besoin de vous souvenir de tous les noms de traits.

##### Exemple  

Une définition naïve :

    template<typename T> concept Equality = has_equal<T> && has_not_equal<T>;

Mieux vaut utiliser le concept standard `equality_comparable`, mais à titre d’exemple :

    template<typename T> concept Equality = requires(T a, T b) {
        { a == b } -> std::convertible_to<bool>;
        { a != b } -> std::convertible_to<bool>;
        // axiom { !(a == b) == (a != b) }
        // axiom { a = b; => a == b }  // => signifie « implique »
    };

Les concepts `has_equal` et `has_not_equal` seraient des concepts « sans sens » s’ils étaient définis séparément.

##### Application  

* ???

---

## <a name="ss-temp-interface"></a>Interfaces de templates

Au fil des années, la programmation avec des templates a souffert d’une distinction trop faible entre l’interface d’un template et son implémentation.  
Avant les concepts, cette distinction n’était pas prise en charge directement par le langage.  
Cependant, l’interface d’un template est cruciale : c’est le contrat entre l’utilisateur et l’implémenteur, et elle doit être conçue avec soin.

### <a name="rt-fo"></a>T.40 : Utiliser des objets fonctionnels pour transmettre des opérations aux algorithmes

##### Raison  
Les objets fonctionnels peuvent transporter davantage d’information à travers une interface qu’un simple pointeur de fonction.  
En général, passer des objets fonctionnels donne de meilleures performances que passer des pointeurs de fonction.

##### Exemple  

    bool greater(double x, double y) { return x > y; }
    sort(v, greater);                                    // pointeur de fonction : potentiellement lent
    sort(v, [](double x, double y) { return x > y; });   // objet fonctionnel
    sort(v, std::greater{});                             // objet fonctionnel

    bool greater_than_7(double x) { return x > 7; }
    auto x = find_if(v, greater_than_7);                 // pointeur de fonction : peu souple
    auto y = find_if(v, [](double x) { return x > 7; }); // objet fonctionnel : porte les données nécessaires
    auto z = find_if(v, Greater_than<double>(7));        // objet fonctionnel : porte les données nécessaires

On peut bien sûr généraliser ces fonctions en utilisant `auto` ou des concepts :

    auto y1 = find_if(v, [](totally_ordered auto x) { return x > 7; }); // nécessite un type ordonné
    auto z1 = find_if(v, [](auto x) { return x > 7; });                 // espère que le type possède `>`

##### Note  
Les lambdas génèrent des objets fonctionnels.

##### Note  
L’argument de performance dépend du compilateur et des optimisations.

##### Application  

* Signaler les arguments de template qui sont des pointeurs de fonction.  
* Signaler les passages de pointeurs de fonction à des templates (risque de faux‑positifs).

---

### <a name="rt-essential"></a>T.41 : Exiger uniquement les propriétés essentielles dans les concepts d’un template

##### Raison  
Garder les interfaces simples et stables.

##### Exemple  

    void sort(sortable auto& s)  // trier la séquence `s`
    {
        if (debug) cerr << "enter sort( " << s <<  ")\n";
        // …
        if (debug) cerr << "exit sort( " << s <<  ")\n";
    }

Devrait‑on réécrire :

    template<sortable S>
        requires Streamable<S>
    void sort(S& s)  // trier la séquence `s`
    {
        if (debug) cerr << "enter sort( " << s <<  ")\n";
        // …
        if (debug) cerr << "exit sort( " << s <<  ")\n";
    }

Le concept `sortable` ne requiert pas de support `iostream`. D’un autre côté, le tri ne doit pas non plus obliger l’utilisateur à fournir du code de débogage.

##### Note  
Si l’on exige que chaque opération utilisée soit listée parmi les exigences, l’interface devient instable : chaque modification des facilities de débogage, de collecte de données, etc., impacterait la définition du template et obligerait à recompiler tout le code client. Cela est lourd et parfois impossible.

Inversement, utiliser une opération non garantie par le concept peut engendrer une erreur de compilation tardive. En ne vérifiant pas les propriétés non essentielles, on décale le diagnostic à l’instanciation, ce qui est souvent acceptable.

Notez que l’utilisation de noms non‑localisés et non‑dépendants (par ex. `debug` et `cerr`) introduit aussi des dépendances contextuelles susceptibles de provoquer des erreurs « mystérieuses ».

##### Note  
Il est parfois difficile de décider quelles propriétés d’un type sont essentielles et lesquelles ne le sont pas.

##### Application  

* ???

---

### <a name="rt-alias"></a>T.42 : Utiliser des alias de template pour simplifier la notation et masquer les détails d’implémentation

##### Raison  
Lisibilité améliorée.  
Masquage de l’implémentation.  
Les alias de template remplacent de nombreuses utilisations de traits pour calculer un type ; ils peuvent aussi envelopper un trait.

##### Exemple  

    template<typename T, size_t N>
    class Matrix {
        // …
        using Iterator = typename std::vector<T>::iterator;
        // …
    };

Cela évite à l’utilisateur de `Matrix` de savoir que les éléments sont stockés dans un `vector` et évite la répétition de `typename std::vector<T>::`.

##### Exemple  

    template<typename T>
    void user(T& c)
    {
        // …
        typename container_traits<T>::value_type x; // mauvais, verbeux
        // …
    }

    template<typename T>
    using Value_type = typename container_traits<T>::value_type;

    // L’utilisateur de `Value_type` n’a plus à connaître la technique employée pour implémenter `value_type`.

    template<typename T>
    void user2(T& c)
    {
        // …
        Value_type<T> x;
        // …
    }

##### Note  
Une utilisation simple et courante : « Envelopper les traits ! »

##### Application  

* Signaler l’usage de `typename` comme désambiguïsateur en dehors des déclarations `using`.  
* ???

---

### <a name="rt-using"></a>T.43 : Préférer `using` à `typedef` pour définir des alias

##### Raison  
Lisibilité améliorée : avec `using`, le nouveau nom vient en premier, au lieu d’être imbriqué dans une déclaration.  
Généralité : `using` peut être utilisé pour les alias de template, alors que `typedef` ne le supporte pas aisément.  
Uniformité : `using` ressemble syntaxiquement à `auto`.

##### Exemple  

    typedef int (*PFI)(int);   // OK, mais verbeux

    using PFI2 = int (*)(int);   // OK, préférable

    template<typename T>
    typedef int (*PFT)(T);      // erreur

    template<typename T>
    using PFT2 = int (*)(T);   // OK

##### Application  

* Signaler les usages de `typedef`. Cela générera de nombreux « hits » :-)

---

### <a name="rt-deduce"></a>T.44 : Utiliser des templates de fonction pour déduire les types d’argument de template de classe (lorsque cela est possible)

##### Raison  
Écrire explicitement les types d’argument du template peut être fastidieux et inutilement verbeux.

##### Exemple  

    tuple<int, string, double> t1 = {1, "Hamlet", 3.14};   // types explicites
    auto t2 = make_tuple(1, "Ophelia"s, 3.14);         // meilleur ; types déduits

Notez le suffixe `s` pour forcer la conversion en `std::string` plutôt qu’en chaîne C.

##### Note  
Puisqu’on peut trivially écrire une fonction `make_T`, le compilateur pourrait le faire à l’avenir ; ainsi, les fonctions `make_T` deviendront redondantes.

##### Exception  

Parfois il n’est pas possible de déduire les arguments du template, ou vous avez besoin de les spécifier explicitement :

    vector<double> v = { 1, 2, 3, 7.9, 15.99 };
    list<Record*> lst;

##### Note  

C++17 rendra cette règle redondante en autorisant la déduction directe des arguments de constructeur :

    tuple t1 = {1, "Hamlet"s, 3.14}; // déduit : tuple<int, string, double>

##### Application  

* Signaler les cas où le type explicitement spécialé correspond exactement aux types des arguments fournis.

---

### <a name="rt-regular"></a>T.46 : (supprimé)

---

### <a name="rt-visible"></a>T.47 : Éviter les templates non contraints très visibles avec des noms courants

##### Raison  
Un argument de template non contraint correspond à tout, ce qui peut faire prévaloir un tel template sur des types plus spécifiques nécessitant de petites conversions.  
C’est particulièrement gênant/dangereux lorsqu’on utilise la recherche d’argument dépendant (ADL).  
Les noms communs augmentent la probabilité de ce problème.

##### Exemple  

    namespace Bad {
        struct S { int m; };
        template<typename T1, typename T2>
        bool operator==(T1, T2) { cout << "Bad\n"; return true; }
    }

    namespace T0 {
        bool operator==(int, Bad::S) { cout << "T0\n"; return true; }  // comparaison avec int

        void test()
        {
            Bad::S bad{ 1 };
            vector<int> v(10);
            bool b = 1 == bad;
            bool b2 = v.size() == bad;
        }
    }

Cela affiche `T0` puis `Bad`.

L’opérateur `==` dans `Bad` a été conçu pour poser problème, mais l’auriez‑vous repéré dans du code réel ?  
`v.size()` renvoie un entier non signé, ce qui nécessite une conversion pour appeler l’`operator==` local ; l’opérateur `==` de `Bad` n’a aucune conversion à faire, il est donc préféré.

##### Note  

Si un template non contraint est défini dans le même espace de noms qu’un type, il peut être trouvé par ADL (comme dans l’exemple).  
En d’autres termes, il est **très visible**.

##### Note  

Cette règle ne devrait pas être nécessaire, mais le comité n’a pas réussi à exclure les templates non contraints d’ADL.

Malheureusement, cela générera de nombreux faux‑positifs ; la bibliothèque standard viole largement cette règle en plaçant de nombreux templates et types non contraints dans l’espace de noms `std`.

##### Application  

* Signaler les templates définis dans un espace de noms qui contient également des types concrets (peut‑être difficile tant que les concepts ne sont pas disponibles).

---

### <a name="rt-concept-def"></a>T.48 : Si votre compilateur ne supporte pas les concepts, les simuler avec `enable_if`

##### Raison  
C’est le meilleur compromis lorsqu’on ne dispose pas d’un support direct des concepts.  
`enable_if` permet de définir conditionnellement des fonctions et de sélectionner parmi un ensemble de fonctions.

##### Exemple  

    template<typename T>
    enable_if_t<is_integral_v<T>>
    f(T v)
    {
        // …
    }

    // Équivalent à :
    template<Integral T>
    void f(T v)
    {
        // …
    }

##### Note  

Attention aux [contraintes complémentaires](015-templates.md#rt-not).  
Simuler la surcharge de concepts avec `enable_if` force parfois l’utilisation de ce design fragile.

##### Application  

* ???

---

### <a name="rt-erasure"></a>T.49 : Éviter, lorsque possible, l’effacement de type

##### Raison  
L’effacement de type ajoute un niveau d’indirection supplémentaire en cachant l’information de type derrière une frontière de compilation distincte.

##### Exemple  

    ???

**Exceptions** : l’effacement de type est parfois approprié, par ex. pour `std::function`.

##### Application  

* ???

---

## <a name="ss-temp-def"></a>T.def : Définitions de templates

Une définition de template (classe ou fonction) peut contenir du code arbitraire, donc seule une revue exhaustive des techniques de programmation C++ couvrirait ce sujet.  
Cette section se concentre sur ce qui est spécifique à l’implémentation de templates, en particulier les dépendances contextuelles d’une définition.

### <a name="rt-depend"></a>T.60 : Minimiser les dépendances contextuelles d’un template

##### Raison  
Facilite la compréhension.  
Réduit les erreurs dues à des dépendances inattendues.  
Facilite la création d’outils.

##### Exemple  

    template<typename C>
    void sort(C& c)
    {
        std::sort(begin(c), end(c)); // dépendance nécessaire et utile
    }

    template<typename Iter>
    Iter algo(Iter first, Iter last)
    {
        for (; first != last; ++first) {
            auto x = sqrt(*first); // dépendance potentiellement surprenante : quel `sqrt` ?
            helper(first, x);      // dépendance potentiellement surprenante :
                                   // `helper` est choisi selon `first` et `x`
            TT var = 7;            // dépendance potentiellement surprenante : quel `TT` ?
        }
    }

##### Note  
Les templates apparaissent généralement dans les fichiers d’en‑tête, ce qui rend leurs dépendances plus sensibles à l’ordre d’inclusion que le code source `.cpp`.

##### Note  
Faire fonctionner un template uniquement sur ses arguments serait une manière de réduire au minimum le nombre de dépendances, mais cela serait généralement ingérable.  
Par exemple, les algorithmes utilisent souvent d’autres algorithmes et invoquent des opérations qui ne se limitent pas aux seuls arguments. Et ne parlons même pas des macros !

**Voir aussi** : [T.69](015-templates.md#rt-customization)

##### Application  

* ??? (détecter de façon fiable les dépendances superflues est difficile)

---

### <a name="rt-scary"></a>T.61 : Ne pas sur‑paramétrer les membres (SCARY)

##### Raison  
Un membre qui ne dépend pas d’un paramètre de template ne peut être utilisé que pour un argument de template précis.  
Cela limite l’usage et augmente généralement la taille du code.

##### Exemple, mauvais  

    template<typename T, typename A = std::allocator<T>>
        // requires Regular<T> && Allocator<A>
    class List {
    public:
        struct Link {   // ne dépend pas de A
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

    List<int> lst1;
    List<int, My_allocator> lst2;

`Link` semble anodin, mais il dépend formellement de l’allocateur (même s’il ne l’utilise pas). Cela force des instanciations redondantes et coûteuses.

Solution : rendre la classe imbriquée non dépendante en la déclarant hors de la classe template :

    template<typename T>
    struct Link {
        T elem;
        Link* pre;
        Link* suc;
    };

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

    List2<int> lst1;
    List2<int, My_allocator> lst2;

Certaines personnes trouvaient l’idée que `Link` ne soit plus caché « effrayante », d’où le nom **SCARY** (see the original paper).

##### Note  

Cela vaut aussi pour les lambdas qui ne dépendent pas de tous les paramètres de template.

##### Application  

* Signaler les types membres qui ne dépendent pas de chaque paramètre de template.  
* Signaler les fonctions membres qui ne dépendent pas de chaque paramètre.  
* Signaler les lambdas ou variables templates qui ne dépendent pas de chaque paramètre.

---

### <a name="rt-nondependent"></a>T.62 : Placer les membres de classe template non‑dépendants dans une classe de base non‑template

##### Raison  
Permettre aux membres de la classe de base d’être utilisés sans spécifier les arguments du template et sans instanciation du template.

##### Exemple  

    template<typename T>
    class Foo {
    public:
        enum { v1, v2 };
        // …
    };

    // …
    struct Foo_base {
        enum { v1, v2 };
        // …
    };

    template<typename T>
    class Foo : public Foo_base {
    public:
        // …
    };

##### Note  

Une version plus générale de cette règle serait : « Si un membre d’un template de classe dépend seulement de *N* paramètres sur *M*, le placer dans une classe de base qui ne possède que ces *N* paramètres. »  
Pour *N* = 1, on peut choisir une classe de base située dans l’espace de noms environnant, comme dans [T.61](015-templates.md#rt-scary).

*Qu’en est‑il des constantes ? des membres statiques de classe ?* @TODO‑LINK

##### Application  

* ???
  
---

### <a name="rt-specialization"></a>T.64 : Utiliser la spécialisation pour fournir des implémentations alternatives de templates de classe

##### Raison  
Un template définit une interface générale.  
La spécialisation offre un mécanisme puissant pour fournir des implémentations alternatives de cette interface.

##### Exemple  

    ??? string specialization (==)

    ??? representation specialization ?

##### Note  

???

##### Application  

???

---

### <a name="rt-tag-dispatch"></a>T.65 : Utiliser le dispatch d’étiquette pour fournir des implémentations alternatives de fonctions

##### Raison  

* Un template définit une interface générale.  
* Le dispatch d’étiquette permet de sélectionner des implémentations selon des propriétés spécifiques d’un type d’argument.  
* Performance.

##### Exemple (version simplifiée de `std::copy` qui ignore les séquences non contiguës)  

    struct trivially_copyable_tag {};
    struct non_trivially_copyable_tag {};

    // T n’est pas trivially copyable
    template<class T> struct copy_trait { using tag = non_trivially_copyable_tag; };
    // int est trivially copyable
    template<> struct copy_trait<int> { using tag = trivially_copyable_tag; };

    template<class Iter>
    Out copy_helper(Iter first, Iter last, Iter out, trivially_copyable_tag)
    {
        // utilisation de memmove
    }

    template<class Iter>
    Out copy_helper(Iter first, Iter last, Iter out, non_trivially_copyable_tag)
    {
        // boucle appelant les constructeurs de copie
    }

    template<class Iter>
    Out copy(Iter first, Iter last, Iter out)
    {
        using tag_type = typename copy_trait<std::iter_value_t<Iter>>::tag;
        return copy_helper(first, last, out, tag_type{});
    }

    void use(vector<int>& vi, vector<int>& vi2, vector<string>& vs, vector<string>& vs2)
    {
        copy(vi.begin(), vi.end(), vi2.begin()); // utilise memmove
        copy(vs.begin(), vs.end(), vs2.begin()); // boucle appelant les constructeurs de copie
    }

Avec les contraintes C++20, on peut distinguer les alternatives directement :

    template<class Iter>
        requires std::is_trivially_copyable_v<std::iter_value_t<Iter>>
    Out copy_helper(Iter first, Iter last, Out out)
    {
        // memmove
    }

    template<class Iter>
    Out copy_helper(Iter first, Iter last, Out out)
    {
        // boucle appelant les constructeurs de copie
    }

##### Application  

* ???

---

### <a name="rt-specialization2"></a>T.67 : Utiliser la spécialisation pour fournir des implémentations alternatives pour les types irréguliers

##### Raison  
???

##### Exemple  

    ???

##### Application  

* ???

---

### <a name="rt-cast"></a>T.68 : Utiliser `{}` plutôt que `()` à l’intérieur des templates pour éviter les ambiguïtés

##### Raison  
`()` est sujet à des ambiguïtés grammaticales.

##### Exemple  

    template<typename T, typename U>
    void f(T t, U u)
    {
        T v1(T(u));    // erreur : v1 est une fonction, pas une variable
        T v2{u};       // clair : évidemment une variable
        auto x = T(u); // ambigu : construction ou cast ?
    }

    f(1, "asdf"); // mauvais : cast de `const char*` vers `int`

##### Application  

* Signaler les initialiseurs avec `()`  
* Signaler les casts de style fonction  

---

### <a name="rt-customization"></a>T.69 : Dans un template, ne pas appeler de fonction non‑membre non qualifiée sauf si vous avez l’intention d’en faire un point de personnalisation

##### Raison  

* Fournir la flexibilité voulue uniquement.  
* Éviter la vulnérabilité aux changements accidentels de l’environnement.

##### Exemple  

Il existe trois principales façons de laisser le code appelant personnaliser un template.

    template<class T>
        // appel d’une fonction membre
    void test1(T t)
    {
        t.f();    // requiert que T fournisse `f()`
    }

    template<class T>
    void test2(T t)
        // appel d’une fonction non‑membre sans qualification
    {
        f(t);     // requiert que `f(T)` soit disponible dans l’espace de noms appelant ou dans le namespace de T
    }

    template<class T>
    void test3(T t)
        // invoquer un "trait"
    {
        test_traits<T>::f(t); // requiert la spécialisation de `test_traits<>` pour obtenir des fonctions/types non‑défault
    }

Un *trait* est généralement un alias de type, une fonction `constexpr` ou un template de traits à spécialiser sur le type de l’utilisateur.

##### Note  

Si vous avez l’intention d’appeler votre propre fonction auxiliaire `helper(t)` avec un argument `t` dépendant d’un paramètre de template, placez‑la dans un namespace `::detail` et qualifiez l’appel : `detail::helper(t);`.  
Un appel non qualifié devient alors un point de personnalisation : toute fonction `helper` dans le namespace du type de `t` pourra être invoquée, ce qui peut entraîner les problèmes décrits dans [T.47](015-templates.md#rt-visible).

##### Application  

* Dans un template, signaler un appel non qualifié à une fonction non‑membre qui reçoit une variable de type dépendant lorsqu’il existe une fonction non‑membre du même nom dans le namespace du template.

---

## <a name="ss-temp-hier"></a>T.temp‑hier : Règles concernant les templates et les hiérarchies

Les templates constituent le pilier du support générique de C++, tandis que les hiérarchies de classes constituent le pilier du support orienté‑objet.  
Les deux mécanismes peuvent être combinés efficacement, mais certains pièges de conception doivent être évités.

### <a name="rt-hier"></a>T.80 : Ne pas templatiser naïvement une hiérarchie de classes

##### Raison  
Templatiser une hiérarchie riche en fonctions, notamment en fonctions virtuelles, peut entraîner un gonflement du code.

##### Exemple, mauvais  

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

    Vector<int> vi;
    Vector<string> vs;

Définir `sort` comme fonction membre d’un conteneur n’est pas idéal, mais cela illustre bien ce qu’il ne faut pas faire.  
Le compilateur doit générer du code pour `vector<int>::sort()` et `vector<string>::sort()`, même si aucune de ces fonctions n’est réellement appelée ; cela cause du code bloat. Imaginez une hiérarchie avec des dizaines de fonctions membres et des dizaines de classes dérivées : le bloat devient massif.

##### Note  

Dans de nombreux cas, on peut fournir une interface stable sans paramétriser la base ; voir ["stable base"](015-templates.md#rt-abi) et [OO et GP](015-templates.md#rt-generic-oo).

##### Application  

* Signaler les fonctions virtuelles dépendant d’un paramètre de template. ??? (faux‑positifs possibles)

---

### <a name="rt-array"></a>T.81 : Ne pas mélanger hiérarchies et tableaux

##### Raison  
Un tableau de classes dérivées peut « se dégrader » implicitement en pointeur vers la classe de base, ce qui peut mener à des résultats désastreux.

##### Exemple  

    void maul(Fruit* p)
    {
        *p = Pear{};     // placer une poire dans *p
        p[1] = Pear{};   // placer une poire dans p[1]
    }

    Apple aa[] = { an_apple, another_apple };   // aa contient des Apples (évident)

    maul(aa);
    Apple& a0 = aa[0];   // une poire ?
    Apple& a1 = aa[1];   // une poire ?

Si `sizeof(Apple) != sizeof(Pear)` l’accès à `aa[1]` sera mal aligné, entraînant violation de type et probablement corruption de mémoire.  
Ne jamais écrire un tel code.

Note : `maul()` viole la règle ["`T*` pointe vers un objet individuel"](006-functions.md#rf-ptr).

**Alternative** : utiliser un conteneur templatisé approprié :

    void maul2(Fruit* p)
    {
        *p = Pear{};   // idem
    }

    vector<Apple> va = { an_apple, another_apple };

    maul2(va);               // erreur : impossible de convertir `vector<Apple>` en `Fruit*`
    maul2(&va[0]);           // vous avez explicitement demandé cela

    Apple& a0 = va[0];       // une poire ?

Note : l’affectation dans `maul2()` viole la règle ["pas de slicing"](010-expr.md#res-slice).

##### Application  

* Détecter ce pattern dangereux. @TODO‑LINK

---

### <a name="rt-linear"></a>T.82 : Linéariser une hiérarchie lorsque les fonctions virtuelles sont indésirables

##### Raison  

???

##### Exemple  

    ???

##### Application  

* ???

---

### <a name="rt-virtual"></a>T.83 : Ne pas déclarer un template de fonction membre virtuel

##### Raison  
C++ ne le permet pas.  
Si c’était autorisé, les tables virtuelles (vtbl) ne pourraient être générées qu’au moment de l’édition de liens, ce qui rendrait le linking difficile.

##### Exemple, mauvais  

    class Shape {
        // …
        template<class T>
        virtual bool intersect(T* p);   // erreur : un template ne peut pas être virtuel
    };

##### Note  

Nous avons besoin de cette règle car la question revient fréquemment.

##### Alternative  

Double dispatch, visiteurs, calcul du fonction à appeler.

##### Application  

Le compilateur gère déjà cette interdiction.

---

### <a name="rt-abi"></a>T.84 : Utiliser une implémentation centrale non‑template pour fournir une interface stable au niveau de l’ABI

##### Raison  
Améliorer la stabilité du code.  
Éviter le bloat du code.

##### Exemple  

    struct Link_base {   // stable
        Link_base* suc;
        Link_base* pre;
    };

    template<typename T>   // wrapper typé
    struct Link : Link_base {
        T val;
    };

    struct List_base {
        Link_base* first;   // premier élément (s’il y en a)
        int sz;             // nombre d’éléments
        void add_front(Link_base* p);
        // …
    };

    template<typename T>
    class List : List_base {
    public:
        void put_front(const T& e) { add_front(new Link<T>{e}); }   // cast implicite vers Link_base
        T& front() { return static_cast<Link<T>*>(first)->val; }    // cast explicite vers Link<T>
        // …
    };

    List<int> li;
    List<string> ls;

Il n’y a qu’une seule copie des opérations de liaison et de délégation d’éléments d’une `List`.  
Les classes `Link` et `List` ne font que manipuler les types.

Une autre technique courante consiste à spécialiser pour `void` ou `void*` et à faire du template général un simple wrapper autour de l’implémentation core `void`.

**Alternative** : utiliser le pattern [Pimpl](005-interfaces.md#ri-pimpl).

##### Application  

* ???

---

## <a name="ss-variadic"></a>T.var : Règles des templates variadiques

???

### <a name="rt-variadic"></a>T.100 : Utiliser les templates variadiques lorsqu’une fonction doit accepter un nombre variable d’arguments de types variés

##### Raison  
Les templates variadiques sont le mécanisme le plus général, efficace et sûr pour cela.  
Ne pas recourir aux `...` variadiques de C.

##### Exemple  

    ??? printf

##### Application  

* Signaler les usages de `va_arg` dans le code utilisateur.

---

### <a name="rt-variadic-pass"></a>T.101 : ??? Comment passer des arguments à un template variadique ???

##### Raison  

???

##### Exemple  

    ??? attention aux arguments move‑only et aux références

##### Application  

* ???

---

### <a name="rt-variadic-process"></a>T.102 : ??? Comment traiter les arguments d’un template variadique ???

##### Raison  

???

##### Exemple  

    ??? forwarding, vérification de type, références

##### Application  

* ???

---

### <a name="rt-variadic-not"></a>T.103 : Ne pas utiliser les templates variadiques pour des listes d’arguments homogènes

##### Raison  
Il existe des moyens plus précis pour spécifier une séquence homogène, comme `initializer_list`.

##### Exemple  

    ???

##### Application  

* ???

---

## <a name="ss-meta"></a>T.meta : Métaprogrammation de templates (TMP)

Les templates offrent un mécanisme général de programmation à la compilation.

La métaprogrammation consiste à écrire du code dont au moins une entrée ou un résultat est un **type**.  
Les templates offrent une forme de duck‑typing complet à la compilation (sous réserve de la mémoire disponible).  
La syntaxe et les techniques sont notoirement complexes.

### <a name="rt-metameta"></a>T.120 : Utiliser la métaprogrammation de template uniquement lorsque cela est réellement nécessaire

##### Raison  
La métaprogrammation de template est difficile à bien faire, ralentit la compilation et est souvent très dure à entretenir.  
Cependant, il existe des cas concrets où elle procure de meilleures performances que toute autre solution (sauf l’assembleur expert).  
Il existe aussi des cas où la métaprogrammation exprime mieux les idées fondamentales qu’un code d’exécution.

##### Exemple, mauvais  

    ???

##### Exemple, mauvais  

    enable_if

Mieux vaut utiliser les concepts. Voir [comment émuler les concepts sans support du langage](015-templates.md#rt-emulate).

##### Exemple, bon  

    ???

**Alternative** : Si le résultat est une valeur, utilisez plutôt une [`constexpr` function](015-templates.md#rt-fct).

##### Note  

Si vous sentez le besoin de cacher votre métaprogrammation derrière des macros, vous êtes probablement allé trop loin.

### <a name="rt-emulate"></a>T.121 : Utiliser la métaprogrammation de template principalement pour émuler les concepts

##### Raison  
Lorsque C++20 n’est pas disponible, on doit les émuler via TMP.  
Les cas d’usage qui requièrent des concepts (par ex. la surcharge basée sur des concepts) sont parmi les plus courants (et simples) d’utilisation du TMP.

##### Exemple  

    template<typename Iter>
        /*requires*/ enable_if<random_access_iterator<Iter>, void>
    advance(Iter p, int n) { p += n; }

    template<typename Iter>
        /*requires*/ enable_if<forward_iterator<Iter>, void>
    advance(Iter p, int n) { assert(n >= 0); while (n--) ++p;}

##### Note  

Avec les concepts cela devient beaucoup plus lisible :

    void advance(random_access_iterator auto p, int n) { p += n; }

    void advance(forward_iterator auto p, int n) { assert(n >= 0); while (n--) ++p;}

##### Application  

* ???

---

### <a name="rt-tmp"></a>T.122 : Utiliser les templates (généralement des alias de template) pour calculer des types à la compilation

##### Raison  
Le TMP est le seul moyen directement supporté et raisonnablement structuré de générer des types à la compilation.

##### Note  

Les techniques « traits » sont largement remplacées par des alias de template pour les types et des fonctions `constexpr` pour les valeurs.

##### Exemple  

    ??? big object / small object optimisation

##### Application  

* ???

---

### <a name="rt-fct"></a>T.123 : Utiliser des fonctions `constexpr` pour calculer des valeurs à la compilation

##### Raison  
Une fonction est le moyen le plus évident et conventionnel d’exprimer le calcul d’une valeur.  
Souvent, une fonction `constexpr` implique moins de surcharge à la compilation qu’une métaprogrammation TMP.

##### Exemple  

    template<typename T>
        // requires Number<T>
    constexpr T pow(T v, int n)   // puissance/exponentielle
    {
        T res = 1;
        while (n--) res *= v;
        return res;
    }

    constexpr auto f7 = pow(pi, 7);

##### Application  

* Signaler les programmes TMP qui produisent une valeur et suggérer de les remplacer par des fonctions `constexpr`.

---

### <a name="rt-std-tmp"></a>T.124 : Privilégier l’utilisation des facilities de métaprogrammation du standard

##### Raison  
Les facilities définies dans le standard (`conditional`, `enable_if`, `tuple`, …) sont portables et supposées être connues.

##### Exemple  

    ???

##### Application  

* ???

---

### <a name="rt-lib"></a>T.125 : Si vous devez aller au‑delà des facilities TMP du standard, utilisez une bibliothèque existante

##### Raison  
Obtenir des facilities TMP avancées n’est pas simple ; recourir à une bibliothèque vous intègre dans une communauté (espérons‑le) solidaire.  
N’écrivez votre propre « support TMP avancé » que si c’est absolument indispensable.

##### Exemple  

    ???

##### Application  

* ???

---

## <a name="ss-temp-other"></a>Autres règles relatives aux templates

### <a name="rt-name"></a>T.140 : Si une opération peut être réutilisée, lui donner un nom

Voir [F.10](006-functions.md#rf-name)

### <a name="rt-lambda"></a>T.141 : Utiliser une lambda anonyme si vous avez besoin d’un simple objet fonction dans un seul endroit

Voir [F.11](006-functions.md#rf-lambda)

### <a name="rt-var"></a>T.142 : Utiliser des variables de template pour simplifier la notation

##### Raison  
Lisibilité améliorée.

##### Exemple  

    ???

##### Application  

* ???

### <a name="rt-non-generic"></a>T.143 : Ne pas écrire de code non‑générique de façon non intentionnelle

##### Raison  
Généralité. Réutilisabilité.  
Ne pas s’engager gratuitement sur des détails ; utilisez les facilities les plus générales disponibles.

##### Exemple  

    for (auto i = first; i < last; ++i) {   // moins générique
        // …
    }

    for (auto i = first; i != last; ++i) {   // bon : plus générique
        // …
    }

Bien sûr, la boucle `for‑range` est encore meilleure lorsqu’elle convient.

##### Exemple  

    class Base {
    public:
        Bar f();
        Bar g();
    };

    class Derived1 : public Base {
    public:
        Bar h();
    };

    class Derived2 : public Base {
    public:
        Bar j();
    };

    // mauvais, sauf raison précise
    void my_func(Derived1& param)
    {
        use(param.f());
        use(param.g());
    }

    // bon, n’utilise que l’interface `Base`
    void my_func(Base& param)
    {
        use(param.f());
        use(param.g());
    }

##### Application  

* Signaler les comparaisons d’itérateurs avec `<` au lieu de `!=`.  
* Signaler `x.size() == 0` lorsqu’un appel à `x.empty()` ou `x.is_empty()` est disponible.  
* Signaler les fonctions qui prennent un pointeur ou une référence à un type plus dérivé alors qu’elles n’utilisent que des membres du type de base.

### <a name="rt-specialize-function"></a>T.144 : Ne pas spécialiser les templates de fonction

##### Raison  
On ne peut pas spécialiser partiellement un template de fonction selon les règles du langage.  
On peut le spécialiser complètement, mais on devrait alors surcharger ; les spécialisations de fonction ne participent pas à la surcharge, ce qui conduit souvent à des comportements inattendus.  
Dans les rares cas où la spécialisation est réellement justifiée, il faut déléguer à un template de classe spécializable.

##### Exemple  

    ???

**Exceptions** : si vous avez une raison valable de spécialiser un template de fonction, écrivez simplement un template de fonction qui délègue à un template de classe, puis spécialisez le template de classe (y compris les spécialisations partielles).

##### Application  

* Signaler toutes les spécialisations de templates de fonction. Suggérer la surcharge à la place.

---

### <a name="rt-check-class"></a>T.150 : Vérifier qu’une classe satisfait un concept à l’aide de `static_assert`

##### Raison  
Si vous prévoyez qu’une classe corresponde à un concept, le vérifier tôt évite bien des maux de tête aux utilisateurs.

##### Exemple  

    class X {
    public:
        X() = delete;
        X(const X&) = default;
        X(X&&) = default;
        X& operator=(const X&) = default;
        // …
    };

Quelque part (possiblement dans un fichier d’implémentation) :

    static_assert(Default_constructible<X>);    // erreur : X n’a pas de constructeur par défaut
    static_assert(Copyable<X>);                 // erreur : on a oublié de définir le constructeur de déplacement

##### Application  

* Non réaliste (difficile à automatiser).

---