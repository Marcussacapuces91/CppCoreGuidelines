# <a name="s-expr"></a>ES : Expressions et instructions

Les expressions et les instructions sont les moyens les plus bas et les plus directs d'exprimer des actions et des calculs. Les déclarations dans les portées locales sont des instructions.

Pour les règles de nommage, de commentaires et d'indentation, voir [NL : Nommage et mise en page](024-naming.md) @TODO‑LINK.

## Règles générales :

* [ES.1 : Préférer la bibliothèque standard aux autres bibliothèques et au code « fait maison »](010-expr.md#res-lib)
* [ES.2 : Préférer les abstractions appropriées à l'utilisation directe des fonctionnalités du langage](010-expr.md#res-abstr)
* [ES.3 : Ne pas se répéter, éviter le code redondant](010-expr.md#res-dry) @TODO‑LINK (voir [SL.1](018-stdlib.md#rsl-lib) @TODO‑LINK)

## Règles de déclaration :

* [ES.5 : Garder les portées petites](010-expr.md#res-scope)
* [ES.6 : Déclarer les noms dans les initialiseurs et les conditions des boucles `for` afin de limiter la portée](010-expr.md#res-cond)
* [ES.7 : Garder les noms courants et locaux courts, et les noms peu courants et non‑locaux plus longs](010-expr.md#res-name-length)
* [ES.8 : Éviter les noms qui se ressemblent](010-expr.md#res-name-similar)
* [ES.9 : Éviter les noms en `ALL_CAPS`](010-expr.md#res-not-caps)
* [ES.10 : Déclarer un seul nom par déclaration](010-expr.md#res-name-one)
* [ES.11 : Utiliser `auto` pour éviter la répétition redondante des noms de type](010-expr.md#res-auto)
* [ES.12 : Ne pas réutiliser les noms dans des portées imbriquées](010-expr.md#res-reuse)
* [ES.20 : Toujours initialiser un objet](010-expr.md#res-always)
* [ES.21 : Ne pas introduire une variable (ou constante) avant d'en avoir besoin](010-expr.md#res-introduce)
* [ES.22 : Ne pas déclarer une variable tant qu'on n'a pas de valeur pour l'initialiser](010-expr.md#res-init)
* [ES.23 : Préférer la syntaxe d'initialisation `{}`](010-expr.md#res-list)
* [ES.24 : Utiliser `unique_ptr<T>` pour détenir des pointeurs](010-expr.md#res-unique)
* [ES.25 : Déclarer un objet `const` ou `constexpr` sauf si vous avez besoin de le modifier plus tard](010-expr.md#res-const)
* [ES.26 : Ne pas utiliser une variable à deux fins différentes](010-expr.md#res-recycle)
* [ES.27 : Utiliser `std::array` ou `stack_array` pour les tableaux sur la pile](010-expr.md#res-stack)
* [ES.28 : Utiliser les lambdas pour les initialisations complexes, surtout pour les variables `const`](010-expr.md#res-lambda-init)
* [ES.30 : Ne pas utiliser les macros pour la manipulation de texte du programme](010-expr.md#res-macros)
* [ES.31 : Ne pas utiliser les macros pour les constantes ou les « fonctions »](010-expr.md#res-macros2)
* [ES.32 : Utiliser `ALL_CAPS` pour tous les noms de macros](010-expr.md#res-all_caps)
* [ES.33 : Si vous devez utiliser des macros, leur donner des noms uniques](010-expr.md#res-macros3)
* [ES.34 : Ne pas définir une fonction variadique de style C](010-expr.md#res-ellipses)

## Règles d'expression :

* [ES.40 : Éviter les expressions compliquées](010-expr.md#res-complicated)
* [ES.41 : En cas de doute sur la priorité des opérateurs, mettre des parenthèses](010-expr.md#res-parens)
* [ES.42 : Garder l'utilisation des pointeurs simple et directe](010-expr.md#res-ptr)
* [ES.43 : Éviter les expressions avec un ordre d'évaluation indéfini](010-expr.md#res-order)
* [ES.44 : Ne pas dépendre de l'ordre d'évaluation des arguments de fonction](010-expr.md#res-order-fct)
* [ES.45 : Éviter les « magic constants » ; utiliser des constantes symboliques](010-expr.md#res-magic)
* [ES.46 : Éviter les conversions rétrécissantes](010-expr.md#res-narrowing)
* [ES.47 : Utiliser `nullptr` plutôt que `0` ou `NULL`](010-expr.md#res-nullptr)
* [ES.48 : Éviter les castings](010-expr.md#res-casts)
* [ES.49 : Si vous devez caster, utilisez un cast nommé](010-expr.md#res-casts-named)
* [ES.50 : Ne pas enlever le `const` avec un cast](010-expr.md#res-casts-const)
* [ES.55 : Éviter le besoin de vérifications de limites](010-expr.md#res-range-checking)
* [ES.56 : N'écrire `std::move()` que lorsqu'il faut explicitement déplacer un objet vers une autre portée](010-expr.md#res-move)
* [ES.60 : Éviter `new` et `delete` en dehors des fonctions de gestion de ressources](010-expr.md#res-new)
* [ES.61 : Supprimer les tableaux avec `delete[]` et les non‑tableaux avec `delete`](010-expr.md#res-del)
* [ES.62 : Ne pas comparer des pointeurs appartenant à des tableaux différents](010-expr.md#res-arr2)
* [ES.63 : Ne pas « slice »](010-expr.md#res-slice)
* [ES.64 : Utiliser la notation `T{e}` pour la construction](010-expr.md#res-construct)
* [ES.65 : Ne pas déréférencer un pointeur invalide](010-expr.md#res-deref)

## Règles d'instruction :

* [ES.70 : Préférer une instruction `switch` à une instruction `if` lorsqu'il y a un choix](010-expr.md#res-switch-if)
* [ES.71 : Préférer une boucle `for`‑range à une boucle `for` lorsqu'il y a un choix](010-expr.md#res-for-range)
* [ES.72 : Préférer une boucle `for` à une boucle `while` lorsqu'il y a une variable de boucle évidente](010-expr.md#res-for-while)
* [ES.73 : Préférer une boucle `while` à une boucle `for` lorsqu'il n'y a pas de variable de boucle évidente](010-expr.md#res-while-for)
* [ES.74 : Préférer déclarer la variable de boucle dans la partie initialisation d'une instruction `for`](010-expr.md#res-for-init)
* [ES.75 : Éviter les instructions `do`](010-expr.md#res-do)
* [ES.76 : Éviter `goto`](010-expr.md#res-goto)
* [ES.77 : Minimiser l'usage de `break` et `continue` dans les boucles](010-expr.md#res-continue)
* [ES.78 : Ne pas compter sur le « fall‑through » implicite dans les `switch`](010-expr.md#res-break)
* [ES.79 : Utiliser `default` pour gérer les cas courants (seulement)](010-expr.md#res-default)
* [ES.84 : Ne pas essayer de déclarer une variable locale sans nom](010-expr.md#res-noname)
* [ES.85 : Rendre les instructions vides visibles](010-expr.md#res-empty)
* [ES.86 : Éviter de modifier les variables de contrôle de boucle à l'intérieur du corps des boucles `for` classiques](010-expr.md#res-loop-counter)
* [ES.87 : Ne pas ajouter de `==` ou `!=` redondants aux conditions](010-expr.md#res-if)

## Règles arithmétiques :

* [ES.100 : Ne pas mélanger arithmétique signée et non signée](010-expr.md#res-mix)
* [ES.101 : Utiliser des types non signés pour la manipulation de bits](010-expr.md#res-unsigned)
* [ES.102 : Utiliser des types signés pour l'arithmétique](010-expr.md#res-signed)
* [ES.103 : Ne pas provoquer de dépassement de capacité (overflow)](010-expr.md#res-overflow)
* [ES.104 : Ne pas provoquer de sous‑débordement (underflow)](010-expr.md#res-underflow)
* [ES.105 : Ne pas diviser par zéro entier](010-expr.md#res-zero)
* [ES.106 : Ne pas essayer d'éviter les valeurs négatives en utilisant `unsigned`](010-expr.md#res-nonnegative)
* [ES.107 : Ne pas utiliser `unsigned` pour les indices, préférer `gsl::index`](010-expr.md#res-subscripts)

---

### <a name="res-lib"></a>ES.1 : Préférer la bibliothèque standard aux autres bibliothèques et au code « fait maison »

##### Raison

Le code qui utilise une bibliothèque peut être beaucoup plus facile à écrire que le code qui travaille directement avec les fonctionnalités du langage, être beaucoup plus court, offrir un niveau d'abstraction plus élevé, et le code de la bibliothèque est supposé déjà testé.  
La bibliothèque standard ISO C++ est parmi les bibliothèques les plus largement connues et les mieux testées. Elle est disponible dans toutes les implémentations de C++.

##### Exemple

    auto sum = accumulate(begin(a), end(a), 0.0);   // bon

Une version range de `accumulate` serait encore meilleure :

    auto sum = accumulate(v, 0.0); // meilleur

mais ne ré‑implémentez pas un algorithme bien connu :

    int max = v.size();   // mauvais : verbeux, but non indiqué
    double sum = 0.0;
    for (int i = 0; i < max; ++i)
        sum = sum + v[i];

##### Exception

De grandes parties de la bibliothèque standard reposent sur l'allocation dynamique (free store). Ces parties, notamment les conteneurs mais pas les algorithmes, ne conviennent pas à certaines applications temps réel strict et embarquées. Dans ces cas, envisagez de fournir/utiliser des installations similaires, par ex. un conteneur de style bibliothèque standard implémenté à l'aide d'un allocateur de pool.

##### Application

Pas facile. ??? Rechercher des boucles désordonnées, boucles imbriquées, fonctions longues, absence d'appels de fonction, manque d'utilisation de types intégrés. Complexité cyclomatique ?

---

### <a name="res-abstr"></a>ES.2 : Préférer les abstractions appropriées à l'utilisation directe des fonctionnalités du langage

##### Raison

Une « abstraction appropriée » (par ex. bibliothèque ou classe) se rapproche davantage des concepts de l'application que le langage brut, conduit à du code plus court et plus clair, et est probablement mieux testé.

##### Exemple

    vector<string> read1(istream& is)   // bon
    {
        vector<string> res;
        for (string s; is >> s;)
            res.push_back(s);
        return res;
    }

L'équivalent plus traditionnel et bas‑niveau est plus long, plus désordonné, plus difficile à bien faire, et généralement plus lent :

    char** read2(istream& is, int maxelem, int maxstring, int* nread)   // mauvais : verbeux et incomplet
    {
        auto res = new char*[maxelem];
        int elemcount = 0;
        while (is && elemcount < maxelem) {
            auto s = new char[maxstring];
            is.read(s, maxstring);
            res[elemcount++] = s;
        }
        *nread = elemcount;
        return res;
    }

Une fois les vérifications de dépassement et la gestion des erreurs ajoutées, ce code devient assez désordonné, et il faut se souvenir de `delete` le pointeur retourné ainsi que les chaînes C‑style que le tableau contient.

##### Application

Pas facile. ??? Rechercher des boucles désordonnées, boucles imbriquées, fonctions longues, absence d'appels de fonction, manque d'utilisation de types intégrés. Complexité cyclomatique ?

---

### <a name="res-dry"></a>ES.3 : Ne pas se répéter, éviter le code redondant

Le code dupliqué ou autrement redondant masque l'intention, rend la logique plus difficile à comprendre et complique la maintenance, entre autres problèmes. Il provient souvent de la programmation « couper‑coller ».

Utilisez les algorithmes standard quand c'est approprié, au lieu d'écrire votre propre implémentation.

**Voir aussi** : [SL.1](018-stdlib.md#rsl-lib) @TODO‑LINK, [ES.11](010-expr.md#res-auto)

##### Exemple

    void func(bool flag)    // mauvais, code dupliqué.
    {
        if (flag) {
            x();
            y();
        }
        else {
            x();
            z();
        }
    }

    void func(bool flag)    // meilleur, pas de code dupliqué.
    {
        x();

        if (flag)
            y();
        else
            z();
    }

##### Application

* Utiliser un analyseur statique ; il détectera au moins certaines constructions redondantes.  
* Revue de code.

---

## ES.dcl : Déclarations

Une déclaration est une instruction. Une déclaration introduit un nom dans une portée et peut entraîner la construction d'un objet nommé.

### <a name="res-scope"></a>ES.5 : Garder les portées petites

##### Raison

Lisibilité. Minimiser la rétention de ressources. Éviter les usages accidentels de valeurs.

**Formulation alternative** : Ne pas déclarer un nom dans une portée inutilement grande.

##### Exemple

    void use()
    {
        int i;    // mauvais : i est inutilement accessible après la boucle
        for (i = 0; i < 20; ++i) { /* … */ }
        // aucune utilisation prévue de i ici
        for (int i = 0; i < 20; ++i) { /* … */ }  // bon : i est local à la boucle `for`

        if (auto pc = dynamic_cast<Circle*>(ps)) {  // bon : pc est local à l'instruction `if`
            // … gérer le cercle …
        }
        else {
            // … gérer l'erreur …
        }
    }

##### Exemple, mauvais

    void use(const string& name)
    {
        string fn = name + ".txt";
        ifstream is {fn};
        Record r;
        is >> r;
        // … 200 lignes de code sans utilisation prévue de fn ou is …
    }

Cette fonction est déjà trop longue, mais le problème est que les ressources utilisées par `fn` et le handle de fichier `is` sont conservés bien plus longtemps que nécessaire, et une utilisation non anticipée de `is` ou `fn` pourrait survenir plus tard dans la fonction.  
Dans ce cas, il serait judicieux d'extraire la lecture :

    Record load_record(const string& name)
    {
        string fn = name + ".txt";
        ifstream is {fn};
        Record r;
        is >> r;
        return r;
    }

    void use(const string& name)
    {
        Record r = load_record(name);
        // … 200 lignes de code …
    }

##### Application

* Signaler les variables de boucle déclarées en dehors d'une boucle et non utilisées après la boucle.  
* Signaler les ressources coûteuses (par ex. handles de fichiers, verrous) qui ne sont pas utilisées pendant N lignes (pour un N approprié).

### <a name="res-cond"></a>ES.6 : Déclarer les noms dans les initialiseurs et les conditions des boucles `for` afin de limiter la portée

##### Raison

Lisibilité. Limiter la visibilité de la variable de boucle à la portée de la boucle. Éviter d'utiliser la variable de boucle à d'autres fins après la boucle. Minimiser la rétention de ressources.

##### Exemple

    void use()
    {
        for (string s; cin >> s;)
            v.push_back(s);

        for (int i = 0; i < 20; ++i) {   // bon : i est local à la boucle `for`
            // …
        }

        if (auto pc = dynamic_cast<Circle*>(ps)) {   // bon : pc est local à l'instruction `if`
            // … gérer le cercle …
        }
        else {
            // … gérer l'erreur …
        }
    }

##### Exemple, mauvais

    int j;                            // MAUVAIS : j est visible hors de la boucle
    for (j = 0; j < 100; ++j) {
        // …
    }
    // j est encore visible ici et n'est pas nécessaire

**Voir aussi** : [Ne pas utiliser une variable à deux fins différentes](010-expr.md#res-recycle)

##### Application

* Avertir lorsqu'une variable modifiée à l'intérieur de l'instruction `for` est déclarée à l'extérieur de la boucle et n'est pas utilisée hors de la boucle.  
* (difficile) Signaler les variables de boucle déclarées avant la boucle et utilisées après la boucle à des fins non liées.

**Discussion** : Restreindre la portée de la variable de boucle aide grandement les optimiseurs. Reconnaître que la variable d'induction n'est accessible que dans le corps de la boucle débloque des optimisations telles que le levage, la réduction de force, le déplacement de code invariant, etc.

##### Exemple C++17 et C++20

Note : C++17 et C++20 ajoutent également les initialiseurs d'instructions `if`, `switch` et `for‑range`. Ceux‑ci nécessitent le support de C++17 et C++20.

    map<int, string> mymap;

    if (auto result = mymap.insert(value); result.second) {
        // insertion réussie, et `result` est valide pour ce bloc
        use(result.first);  // ok
        // …
    } // `result` est détruit ici

##### Application C++17/C++20 (si compilation avec un compilateur C++17 ou C++20)

* Signaler les variables de sélection/ boucle déclarées avant le corps et non utilisées après le corps.  
* (difficile) Signaler les variables de sélection/ boucle déclarées avant le corps et utilisées après le corps à des fins non liées.

### <a name="res-name-length"></a>ES.7 : Garder les noms courants et locaux courts, et les noms peu courants et non‑locaux plus longs

##### Raison

Lisibilité. Réduire les risques de collisions entre noms non‑locaux non liés.

##### Exemple

Les noms courts et locaux conventionnels augmentent la lisibilité :

    template<typename T>    // bon
    void print(ostream& os, const vector<T>& v)
    {
        for (gsl::index i = 0; i < v.size(); ++i)
            os << v[i] << '\n';
    }

Un indice est conventionnellement appelé `i` et il n'y a aucun indice sur la signification du vecteur dans cette fonction générique, donc `v` est aussi bon qu'un autre. Comparez :

    template<typename Element_type>   // mauvais : verbeux, difficile à lire
    void print(ostream& target_stream, const vector<Element_type>& current_vector)
    {
        for (gsl::index current_element_index = 0;
             current_element_index < current_vector.size();
             ++current_element_index)
            target_stream << current_vector[current_element_index] << '\n';
    }

Oui, c'est une caricature, mais on a vu pire.

##### Exemple

Des noms non‑locaux non conventionnels et courts obscurcissent le code :

    void use1(const string& s)
    {
        // …
        tt(s);   // mauvais : qu'est‑ce que tt() ?
        // …
    }

Mieux, donner aux entités non‑locales des noms lisibles :

    void use1(const string& s)
    {
        // …
        trim_tail(s);   // meilleur
        // …
    }

Ici, le lecteur a une chance de savoir ce que `trim_tail` signifie et de s'en souvenir après l'avoir cherché.

##### Exemple, mauvais

Les noms d'arguments de fonctions volumineuses sont de facto non‑locaux et devraient être significatifs :

    void complicated_algorithm(vector<Record>& vr, const vector<int>& vi, map<string, int>& out)
    // lire les événements dans vr (marquer les Records utilisés) pour les indices dans
    // vi plaçant des paires (nom, indice) dans out
    {
        // … 500 lignes de code utilisant vr, vi et out …
    }

Nous recommandons de garder les fonctions courtes, mais cette règle n'est pas universellement respectée et le nommage doit en tenir compte.

##### Application

Vérifier la longueur des noms locaux et non‑locaux. Prendre également en compte la longueur des fonctions.

### <a name="res-name-similar"></a>ES.8 : Éviter les noms qui se ressemblent

##### Raison

Clarté et lisibilité du code. Des noms trop similaires ralentissent la compréhension et augmentent la probabilité d'erreur.

##### Exemple, mauvais

    if (readable(i1 + l1 + ol + o1 + o0 + ol + o1 + I0 + l0)) surprise();

##### Exemple, mauvais

Ne pas déclarer un non‑type avec le même nom qu'un type dans la même portée. Cela supprime le besoin de désambiguïser avec un mot‑clé tel que `struct` ou `enum`. Cela élimine également une source d'erreurs, car `struct X` peut implicitement déclarer `X` si la recherche échoue.

    struct foo { int n; };
    struct foo foo();       // MAUVAIS, foo est déjà un type dans la portée
    struct foo x = foo();   // nécessite désambiguïsation

##### Exception

Des en‑têtes anciens peuvent déclarer des non‑types et des types avec le même nom dans la même portée.

##### Application

* Vérifier les noms contre une liste de combinaisons de lettres et chiffres connues pour être confuses.  
* Signaler la déclaration d'une variable, fonction ou énumérateur qui masque une classe ou une énumération déclarée dans la même portée.

### <a name="res-not-caps"></a>ES.9 : Éviter les noms en `ALL_CAPS`

##### Raison

Ces noms sont couramment utilisés pour les macros. Ainsi, les noms en `ALL_CAPS` sont vulnérables à une substitution macro non intentionnelle.

##### Exemple

    // quelque part dans un en‑tête :
    #define NE !=

    // ailleurs dans un autre en‑tête :
    enum Coord { N, NE, NW, S, SE, SW, E, W };

    // dans le .cpp d'un mauvais programmeur :
    switch (direction) {
    case N:
        // …
    case NE:
        // …
    // …
    }

##### Note

Ne pas utiliser `ALL_CAPS` pour les constantes simplement parce que les constantes étaient autrefois des macros.

##### Application

Signaler toutes les utilisations de `ALL_CAPS`. Pour le code ancien, accepter `ALL_CAPS` pour les noms de macros et signaler tous les noms de macros qui ne sont pas en `ALL_CAPS`.

### <a name="res-name-one"></a>ES.10 : Déclarer un seul nom (uniquement) par déclaration

##### Raison

Une déclaration par ligne augmente la lisibilité et évite les erreurs liées à la grammaire C/C++. Elle laisse aussi de la place pour un commentaire de fin de ligne plus descriptif.

##### Exemple, mauvais

    char *p, c, a[7], *pp[7], **aa[10];   // yuck !

##### Exception

Une déclaration de fonction peut contenir plusieurs déclarations d'arguments de fonction.

##### Exception

Une liaison structurée (C++17) est spécifiquement conçue pour introduire plusieurs variables :

    auto [iter, inserted] = m.insert_or_assign(k, val);
    if (inserted) { /* nouvelle entrée insérée */ }

##### Exemple

    template<class InputIterator, class Predicate>
    bool any_of(InputIterator first, InputIterator last, Predicate pred);

ou mieux en utilisant les concepts :

    bool any_of(input_iterator auto first, input_iterator auto last, predicate auto pred);

##### Exemple

    double scalbn(double x, int n);   // OK : x * pow(FLT_RADIX, n); FLT_RADIX vaut généralement 2

ou :

    double scalbn(    // meilleur : x * pow(FLT_RADIX, n); FLT_RADIX vaut généralement 2
        double x,     // valeur de base
        int n         // exposant
    );

ou :

    // meilleur : base * pow(FLT_RADIX, exponent); FLT_RADIX vaut généralement 2
    double scalbn(double base, int exponent);

##### Exemple

    int a = 10, b = 11, c = 12, d, e = 14, f = 15;

Dans une longue liste de déclarateurs, il est facile d'oublier une variable non initialisée.

##### Application

Signaler les déclarations de variables ou constantes avec plusieurs déclarateurs (par ex. `int* p, q;`).

### <a name="res-auto"></a>ES.11 : Utiliser `auto` pour éviter la répétition redondante des noms de type

##### Raison

* La répétition simple est fastidieuse et source d'erreurs.  
* Avec `auto`, le nom de l'entité déclarée se trouve à une position fixe dans la déclaration, augmentant la lisibilité.  
* Dans une déclaration de fonction‑template, le type de retour peut être un type membre.

##### Exemple

    auto p = v.begin();      // vector<DataRecord>::iterator
    auto z1 = v[3];          // copie de DataRecord
    auto& z2 = v[3];         // évite la copie
    const auto& z3 = v[3];   // const et évite la copie
    auto h = t.future();
    auto q = make_unique<int[]>(s);
    auto f = [](int x) { return x + 10; };

Dans chaque cas, on évite d'écrire un type long et difficile à retenir que le compilateur connaît déjà, mais qu'un programmeur pourrait mal écrire.

##### Exemple

    template<class T>
    auto Container<T>::first() -> Iterator;   // Container<T>::Iterator

##### Exception

Éviter `auto` pour les listes d'initialisation et dans les cas où vous connaissez exactement le type que vous voulez et où une initialisation pourrait nécessiter une conversion.

##### Exemple

    auto lst = { 1, 2, 3 };   // `lst` est une `initializer_list<int>`
    auto x{1};   // `x` est un `int` (en C++17 ; `initializer_list` en C++11)

##### Note

Depuis C++20, nous pouvons (et devons) utiliser les concepts pour être plus précis sur le type que nous déduisons :

    // …
    forward_iterator auto p = algo(x, y, z);

##### Exemple (C++17)

    std::set<int> values;
    // …
    auto [ position, newly_inserted ] = values.insert(5);   // extraire les membres du `std::pair`

##### Application

Signaler la répétition redondante de noms de type dans une déclaration.

### <a name="res-reuse"></a>ES.12 : Ne pas réutiliser les noms dans des portées imbriquées

##### Raison

Il est facile de se tromper sur la variable réellement utilisée. Cela peut entraîner des problèmes de maintenance.

##### Exemple, mauvais

    int d = 0;
    // …
    if (cond) {
        // …
        d = 9;
        // …
    }
    else {
        // …
        int d = 7;
        // …
        d = value_to_be_returned;
        // …
    }

    return d;

Si ce `if` est volumineux, il est facile d'oublier qu'un nouveau `d` a été introduit dans la portée interne. C'est une source connue de bugs. Parfois, ce ré‑emploi d'un nom dans une portée interne est appelé « shadowing ».

##### Note

Le shadowing pose surtout problème lorsque les fonctions sont trop grandes et trop complexes.

##### Exemple

Le shadowing des arguments de fonction dans le bloc le plus externe est interdit par le langage :

    void f(int x)
    {
        int x = 4;  // erreur : ré‑utilisation du nom d'argument de fonction

        if (x) {
            int x = 7;  // autorisé, mais mauvais
            // …
        }
    }

##### Exemple, mauvais

Réutiliser le nom d'un membre comme variable locale peut aussi poser problème :

    struct S {
        int m;
        void f(int x);
    };

    void S::f(int x)
    {
        m = 7;    // assigner au membre
        if (x) {
            int m = 9;
            // …
            m = 99; // assigner à la variable locale
            // …
        }
    }

##### Exception

Nous réutilisons souvent les noms de fonctions d'une classe de base dans une classe dérivée :

    struct B {
        void f(int);
    };

    struct D : B {
        void f(double);
        using B::f;
    };

C'est source d'erreurs. Par exemple, si nous avions oublié la déclaration `using`, un appel `d.f(1)` n'aurait pas trouvé la version `int` de `f`.

??? Faut‑il une règle spécifique sur le shadowing/hiding dans les hiérarchies de classes ?

##### Application

* Signaler la ré‑utilisation d'un nom dans des portées locales imbriquées.  
* Signaler la ré‑utilisation d'un nom de membre comme variable locale dans une fonction membre.  
* Signaler la ré‑utilisation d'un nom global comme variable locale ou nom de membre.  
* Signaler la ré‑utilisation d'un nom de membre de classe de base dans une classe dérivée (sauf pour les noms de fonctions).

### <a name="res-always"></a>ES.20 : Toujours initialiser un objet

##### Raison

Éviter les erreurs « utilisé avant d'être défini » et le comportement indéfini qui en découle. Éviter les problèmes de compréhension d'une initialisation complexe. Simplifier le refactoring.

##### Exemple

    void use(int arg)
    {
        int i;   // mauvais : variable non initialisée
        // …
        i = 7;   // initialise i
    }

Non, `i = 7` n'initialise pas `i` ; cela l'affecte. De plus, `i` peut être lu dans la partie `…`. Mieux :

    void use(int arg)   // OK
    {
        int i = 7;   // OK : initialisé
        string s;    // OK : initialisé par défaut
        // …
    }

##### Note

La règle « toujours initialiser » est délibérément plus stricte que la règle du langage « un objet doit être défini avant d'être utilisé ». Cette dernière règle, plus souple, détecte les bugs techniques, mais :

* Elle conduit à un code moins lisible.  
* Elle encourage les déclarations de noms dans des portées plus grandes que nécessaire.  
* Elle rend le code plus difficile à lire.  
* Elle engendre des bugs logiques en encourageant du code complexe.  
* Elle freine le refactoring.

La règle « toujours initialiser » est une règle de style visant à améliorer la maintenabilité ainsi qu'une règle protégeant contre les erreurs d'utilisation avant définition.

##### Exemple

Voici un exemple souvent cité pour montrer le besoin d'une règle plus souple d'initialisation :

    widget i;    // « widget » est un type coûteux à initialiser, possiblement un grand type trivial
    widget j;

    if (cond) {  // mauvais : i et j sont initialisés « tard »
        i = f1();
        j = f2();
    }
    else {
        i = f3();
        j = f4();
    }

Cela ne peut pas être réécrit triviale­ment pour initialiser `i` et `j` avec des initialiseurs. Notez que pour les types avec un constructeur par défaut, tenter de différer l'initialisation conduit simplement à une initialisation par défaut suivie d'une assignation.  
Une raison populaire pour de tels exemples est « l'efficacité », mais un compilateur capable de détecter une erreur d'utilisation avant définition peut aussi éliminer toute double initialisation redondante.

En supposant qu'il existe une connexion logique entre `i` et `j`, cette connexion devrait probablement être exprimée dans le code :

    pair<widget, widget> make_related_widgets(bool x)
    {
        return (x) ? {f1(), f2()} : {f3(), f4()};
    }

    auto [i, j] = make_related_widgets(cond);    // C++17

Si la fonction `make_related_widgets` est sinon redondante, on peut l'éliminer en utilisant une lambda [ES.28](010-expr.md#res-lambda-init) :

    auto [i, j] = [x] { return (x) ? pair{f1(), f2()} : pair{f3(), f4()} }();    // C++17

Utiliser une valeur représentant « non initialisé » est le symptôme d'un problème et non une solution :

    widget i = uninit;  // mauvais
    widget j = uninit;

    // …
    use(i);         // possiblement utilisé avant définition
    // …

    if (cond) {     // mauvais : i et j sont initialisés « tard »
        i = f1();
        j = f2();
    }
    else {
        i = f3();
        j = f4();
    }

Le compilateur ne peut même pas détecter une utilisation avant définition. De plus, nous avons introduit de la complexité dans l'espace d'état de `widget` : quelles opérations sont valides sur un widget « uninit » et lesquelles ne le sont pas ?

##### Note

L'initialisation complexe est populaire depuis des décennies chez les programmeurs ingénieux. Elle a aussi été une source majeure d'erreurs et de complexité. Beaucoup de ces erreurs sont introduites des années après l'implémentation initiale lors de la maintenance.

##### Exemple

Cette règle couvre les membres de données.

    class X {
    public:
        X(int i, int ci) : m2{i}, cm2{ci} {}
        // …

    private:
        int m1 = 7;
        int m2;
        int m3;

        const int cm1 = 7;
        const int cm2;
        const int cm3;
    };

Le compilateur signalera le `cm3` non initialisé parce que c'est un `const`, mais il ne détectera pas le manque d'initialisation de `m3`. En général, une initialisation de membre rare vaut la peine d'éviter les erreurs d'absence d'initialisation, et souvent un optimiseur peut éliminer une initialisation redondante (par ex. une initialisation qui se produit immédiatement avant une assignation).

##### Exception

Si vous déclarez un objet qui va être immédiatement initialisé à partir d'une entrée, l'initialiser provoquerait une double initialisation. Cependant, méfiez‑vous : cela peut laisser des données non initialisées au‑delà de l'entrée – et cela a été une source fertile d'erreurs et de failles de sécurité :

    constexpr int max = 8 * 1024;
    int buf[max];         // OK, mais suspect : non initialisé
    f.read(buf, max);

Le coût d'initialiser ce tableau peut être important dans certaines situations. Cependant, de tels exemples laissent souvent des variables non initialisées accessibles, il faut donc les traiter avec suspicion.

    constexpr int max = 8 * 1024;
    int buf[max] = {};   // zéro tous les éléments ; meilleur dans certaines situations
    f.read(buf, max);

En raison des règles restrictives d'initialisation pour les tableaux et `std::array`, ils offrent les exemples les plus convaincants justifiant cette exception.

Lorsque cela est possible, utilisez une fonction de bibliothèque connue pour ne pas déborder. Par ex. :

    string s;   // s est initialisé par défaut à `""`
    cin >> s;   // s s'étend pour contenir la chaîne

Ne considérez pas les variables simples qui sont des cibles d'opérations d'entrée comme une exception à cette règle :

    int i;   // mauvais
    // …
    cin >> i;

Dans le cas non rare où la cible d'entrée et l'opération d'entrée sont séparées (ce qui ne devrait pas arriver), le risque d'utilisation avant définition apparaît.

    int i2 = 0;   // meilleur, en supposant que zéro soit une valeur acceptable pour i2
    // …
    cin >> i2;

Un bon optimiseur devrait connaître les opérations d'entrée et éliminer l'opération redondante.

##### Note

Parfois, une lambda peut être utilisée comme initialiseur pour éviter une variable non initialisée :

    error_code ec;
    Value v = [&] {
        auto p = get_value();   // `get_value()` renvoie un `pair<error_code, Value>`
        ec = p.first;
        return p.second;
    }();

ou peut‑être :

    Value v = [] {
        auto p = get_value();   // `get_value()` renvoie un `pair<error_code, Value>`
        if (p.first) throw Bad_value{p.first};
        return p.second;
    }();

**Voir aussi** : [ES.28](010-expr.md#res-lambda-init)

##### Application

* Signaler chaque variable non initialisée.  
* Ne pas signaler les variables de types définis par l'utilisateur avec des constructeurs par défaut.  
* Vérifier qu'un tampon non initialisé est écrit *immédiatement* après la déclaration.  
* Passer une variable non initialisée comme référence à un argument non‑`const` peut être supposé être une écriture dans la variable.

### <a name="res-introduce"></a>ES.21 : Ne pas introduire une variable (ou constante) avant d'en avoir besoin

##### Raison

Lisibilité. Limiter la portée dans laquelle la variable peut être utilisée.

##### Exemple

    int x = 7;
    // … aucune utilisation de x ici …
    ++x;

##### Application

Signaler les déclarations qui sont éloignées de leur première utilisation.

### <a name="res-init"></a>ES.22 : Ne pas déclarer une variable tant qu'on n'a pas de valeur pour l'initialiser

##### Raison

Lisibilité. Limiter la portée d'utilisation de la variable. Éviter le risque d'utilisation avant définition. L'initialisation est souvent plus efficace qu'une assignation.

##### Exemple, mauvais

    string s;
    // … aucune utilisation de s ici …
    s = "what a waste";

##### Exemple, mauvais

    SomeLargeType var;  // CaMeLcAsEvArIaBlE

    if (cond)   // condition non triviale
        Set(&var);
    else if (cond2 || !cond3) {
        var = Set2(3.14);
    }
    else {
        var = 0;
        for (auto& e : something)
            var += e;
    }

    // utilisation de var ; le fait que cela ne soit pas fait trop tôt peut être imposé statiquement avec seulement le contrôle de flux

Ce serait acceptable si `SomeLargeType` possédait une initialisation par défaut peu coûteuse. Sinon, le programmeur pourrait très bien se demander si chaque chemin possible à travers le labyrinthe de conditions a bien été couvert. Si ce n'est pas le cas, nous avons un bug « utilisé avant définition ». C'est un piège de maintenance.

Pour les initialiseurs d'une complexité modérée, y compris pour les variables `const`, envisagez d'utiliser une lambda pour exprimer l'initialiseur ; voir [ES.28](010-expr.md#res-lambda-init).

##### Application

* Signaler les déclarations avec initialisation par défaut qui sont assignées avant d'être lues pour la première fois.  
* Signaler tout calcul compliqué après une variable non initialisée et avant son utilisation.

### <a name="res-list"></a>ES.23 : Préférer la syntaxe d'initialisation `{}`

##### Raison

Préférer `{}`. Les règles d'initialisation avec `{}` sont plus simples, plus générales, moins ambiguës et plus sûres que les autres formes d'initialisation.

Utilisez `=` uniquement lorsque vous êtes sûr qu'il ne peut y avoir aucune conversion rétrécissante. Pour les types arithmétiques intégrés, utilisez `=` uniquement avec `auto`.

Évitez l'initialisation `()` qui autorise des ambiguïtés d'analyse.

##### Exemple

    int x {f(99)};
    int y = x;
    vector<int> v = {1, 2, 3, 4, 5, 6};

##### Exception

Pour les conteneurs, il y a une tradition d'utiliser `{…}` pour une liste d'éléments et `(...)` pour les tailles :

    vector<int> v1(10);    // vecteur de 10 éléments avec la valeur par défaut 0
    vector<int> v2{10};    // vecteur d'un seul élément de valeur 10

    vector<int> v3(1, 2);  // vecteur d'un seul élément de valeur 2
    vector<int> v4{1, 2};  // vecteur de 2 éléments avec les valeurs 1 et 2

##### Note

Les initialiseurs `{}` n'autorisent pas les conversions rétrécissantes (et c'est généralement une bonne chose) et autorisent les constructeurs explicites (ce qui est correct, nous initialisons intentionnellement une nouvelle variable).

##### Exemple

    int x {7.9};   // erreur : rétrécissement
    int y = 7.9;   // OK : y devient 7. Espérer un avertissement du compilateur
    int z {gsl::narrow_cast<int>(7.9)};    // OK : vous avez demandé le cast
    auto zz = gsl::narrow_cast<int>(7.9);  // OK : vous avez demandé le cast

##### Note

L'initialisation `{}` peut être utilisée pour presque toutes les initialisations ; les autres formes ne le peuvent pas :

    auto p = new vector<int> {1, 2, 3, 4, 5};   // vecteur initialisé
    D::D(int a, int b) :m{a, b} {   // initialiseur de membre (par ex. `m` peut être une paire)
        // …
    };
    X var {};   // initialise `var` à vide
    struct S {
        int m {7};   // initialiseur par défaut pour un membre
        // …
    };

Pour cette raison, l'initialisation `{}` est souvent appelée « initialisation uniforme » (bien qu'il reste malheureusement quelques irrégularités).

##### Note

L'initialisation d'une variable déclarée avec `auto` à l'aide d'une seule valeur, par ex. `{v}`, a donné des résultats surprenants jusqu'à C++17. Les règles de C++17 sont un peu moins surprenantes :

    auto x1 {7};        // `x1` est un `int` valant 7
    auto x2 = {7};      // `x2` est une `initializer_list<int>` contenant l'élément 7

    auto x11 {7, 8};    // erreur : deux initialiseurs
    auto x22 = {7, 8};  // `x22` est une `initializer_list<int>` contenant les éléments 7 et 8

Utilisez `={…}` si vous voulez vraiment une `initializer_list<T>` :

    auto fib10 = {1, 1, 2, 3, 5, 8, 13, 21, 34, 55};   // `fib10` est une liste

##### Note

`={}` donne une initialisation par copie alors que `{}` donne une initialisation directe. Comme pour la distinction entre initialisation par copie et initialisation directe, cela peut entraîner des surprises. `{}` accepte les constructeurs `explicit` ; `={}` ne les accepte pas. Par ex. :

    struct Z { explicit Z() {} };

    Z z1{};     // OK : initialisation directe, on utilise le constructeur `explicit`
    Z z2 = {};  // erreur : initialisation par copie, on ne peut pas utiliser le constructeur `explicit`

Utilisez l'initialisation `{}` sauf si vous voulez spécifiquement désactiver les constructeurs explicites.

##### Exemple

    template<typename T>
    void f()
    {
        T x1(1);    // `T` initialisé avec 1
        T x0();     // mauvais : déclaration de fonction (souvent une erreur)

        T y1 {1};   // `T` initialisé avec 1
        T y0 {};    // `T` initialisé par défaut
        // …
    }

**Voir aussi** : [Discussion](#???)

##### Application

* Signaler l'utilisation de `=` pour initialiser des types arithmétiques lorsqu'un rétrécissement se produit.  
* Signaler l'utilisation de la syntaxe d'initialisation `()` qui sont en fait des déclarations. (De nombreux compilateurs devraient déjà avertir à ce sujet.)

### <a name="res-unique"></a>ES.24 : Utiliser un `unique_ptr<T>` pour détenir des pointeurs

##### Raison

Utiliser `std::unique_ptr` est le moyen le plus simple d'éviter les fuites. C'est fiable, cela fait que le système de types effectue une grande partie du travail de validation de la sécurité de la propriété, cela augmente la lisibilité, et cela a un coût d'exécution nul ou quasi‑nul.

##### Exemple

    void use(bool leak)
    {
        auto p1 = make_unique<int>(7);   // OK
        int* p2 = new int{7};            // mauvais : peut fuir
        // … aucune assignation à p2 …
        if (leak) return;
        // … aucune assignation à p2 …
        vector<int> v(7);
        v.at(7) = 0;                    // exception levée
        delete p2;                      // trop tard pour éviter les fuites
        // …
    }

Si `leak == true`, l'objet pointé par `p2` fuit et l'objet pointé par `p1` ne le fait pas. C'est le même cas lorsque `at()` lance une exception. Dans les deux cas, l'instruction `delete p2` n'est jamais atteinte.

##### Application

Rechercher les pointeurs bruts qui sont cibles de `new`, `malloc()` ou de fonctions pouvant retourner de tels pointeurs.

### <a name="res-const"></a>ES.25 : Déclarer un objet `const` ou `constexpr` sauf si vous voulez le modifier plus tard

##### Raison

Ainsi, vous ne pouvez pas changer la valeur par accident. Cela offre également au compilateur des opportunités d'optimisation.

##### Exemple

    void f(int n)
    {
        const int bufmax = 2 * n + 2;  // bon : on ne peut pas changer `bufmax` par accident
        int xmax = n;                  // suspect : `xmax` est‑il censé changer ?
        // …
    }

##### Application

Vérifier si une variable est réellement mutée, et la signaler si ce n'est pas le cas. Malheureusement, il peut être impossible de détecter quand une variable non‑`const` n'était pas *intentionnellement* mutable (vs quand elle ne l'a simplement pas été).

### <a name="res-recycle"></a>ES.26 : Ne pas utiliser une variable à deux fins différentes

##### Raison

Lisibilité et sécurité.

##### Exemple, mauvais

    void use()
    {
        int i;
        for (i = 0; i < 20; ++i) { /* … */ }
        for (i = 0; i < 200; ++i) { /* … */ } // mauvais : `i` recyclé
    }

##### Note

Comme optimisation, vous pourriez vouloir ré‑utiliser un tampon comme espace de travail, mais même dans ce cas, limitez autant que possible la portée de la variable et soyez prudent de ne pas causer de bugs à cause de données résiduelles dans un tampon recyclé ; c'est une source fréquente de bugs de sécurité.

    void write_to_file()
    {
        std::string buffer;             // éviter les réallocations à chaque itération
        for (auto& o : objects) {
            // Première partie du travail.
            generate_first_string(buffer, o);
            write_to_file(buffer);

            // Deuxième partie du travail.
            generate_second_string(buffer, o);
            write_to_file(buffer);

            // …
        }
    }

##### Application

Signaler les variables recyclées.

### <a name="res-stack"></a>ES.27 : Utiliser `std::array` ou `stack_array` pour les tableaux sur la pile

##### Raison

Ils sont lisibles et ne se convertissent pas implicitement en pointeurs. Ils ne sont pas confondus avec les extensions non‑standard des tableaux intégrés.

##### Exemple, mauvais

    const int n = 7;
    int m = 9;

    void f()
    {
        int a1[n];
        int a2[m];   // erreur : pas ISO C++
        // …
    }

##### Note

La définition de `a1` est du C++ légal et a toujours existé. Il y a beaucoup de ce code. Elle est toutefois source d'erreurs, surtout lorsque la borne n'est pas locale. C'est aussi une source « populaire » d'erreurs (débordement de tampon, conversion de tableau en pointeur, etc.). La définition de `a2` est du C mais pas du C++ et constitue un risque de sécurité.

##### Exemple

    const int n = 7;
    int m = 9;

    void f()
    {
        array<int, n> a1;
        stack_array<int> a2(m);
        // …
    }

##### Application

* Signaler les tableaux avec des bornes non constantes (VLAs de style C).  
* Signaler les tableaux avec des bornes constantes non locales.

### <a name="res-lambda-init"></a>ES.28 : Utiliser les lambdas pour les initialisations complexes, surtout pour les variables `const`

##### Raison

Cela encapsule joliment l'initialisation locale, y compris le nettoyage des variables temporaires nécessaires uniquement à l'initialisation, sans créer de fonction non‑locale inutile. Cela fonctionne aussi pour les variables qui devraient être `const` mais seulement après une initialisation longue.

##### Exemple, mauvais

    widget x;   // devrait être `const`, mais :
    for (auto i = 2; i <= N; ++i) {          // ceci pourrait être du code arbitrairement long
        x += some_obj.do_something_with(i);  // code long
    }                                        // à partir d'ici, `x` devrait être `const`
    // …

##### Exemple, bon

    const widget x = [&] {
        widget val;                                // supposons que `widget` possède un constructeur par défaut
        for (auto i = 2; i <= N; ++i) {            // code long
            val += some_obj.do_something_with(i); // code long
        }
        return val;
    }();

Si possible, réduisez les conditions à un simple ensemble d'alternatives (par ex. un `enum`) et ne mélangez pas sélection et initialisation.

##### Application

Difficile. Au mieux une heuristique. Rechercher une variable non initialisée suivie d'une boucle qui lui assigne des valeurs.

### <a name="res-macros"></a>ES.30 : Ne pas utiliser les macros pour la manipulation de texte du programme

##### Raison

Les macros sont une source majeure de bugs. Elles ne respectent pas les règles habituelles de portée et de typage. Elles font voir à l'humain quelque chose de différent de ce que voit le compilateur. Elles compliquent la construction d'outils.

##### Exemple, mauvais

    #define Case break; case   /* MAUVAIS */

Cette macro apparemment inoffensive transforme un `c` minuscule en `C` majuscule, créant un bug de flux de contrôle difficile à repérer.

##### Note

Cette règle n'interdit pas l'utilisation des macros pour le « contrôle de configuration » dans les `#ifdef`, etc.

À l'avenir, les modules devraient éliminer le besoin de macros pour le contrôle de configuration.

##### Note

Cette règle vise également à décourager l'utilisation de `#` pour la stringification et `##` pour la concaténation. Comme d'habitude pour les macros, il existe des usages « principalement inoffensifs », mais même ceux‑ci peuvent créer des problèmes pour les outils (autocomplétion, analyseurs statiques, débogueurs). Souvent, le désir d'utiliser des macros sophistiquées indique un design trop complexe. De plus, `#` et `##` encouragent la définition et l'utilisation de macros :

    #define CAT(a, b) a ## b
    #define STRINGIFY(a) #a

    void f(int x, int y)
    {
        string CAT(x, y) = "asdf";   // MAUVAIS : difficile à gérer pour les outils (et moche)
        string sx2 = STRINGIFY(x);
        // …
    }

Il existe des solutions de contournement pour la manipulation de chaînes de bas niveau avec des macros. Par ex. :

    enum E { a, b };

    template<int x>
    constexpr const char* stringify()
    {
        switch (x) {
        case a: return "a";
        case b: return "b";
        }
    }

    void f()
    {
        string s1 = stringify<a>();
        string s2 = stringify<b>();
        // …
    }

Ce n'est pas aussi pratique qu'une macro, mais c'est aussi simple à utiliser, sans coût d'exécution, typé et limité à la portée.

À l'avenir, la réflexion statique devrait éliminer le dernier besoin du préprocesseur pour la manipulation de texte du programme.

##### Application

Screamer lorsqu'une macro n'est pas uniquement utilisée pour le contrôle de source (par ex. `#ifdef`).

### <a name="res-macros2"></a>ES.31 : Ne pas utiliser les macros pour les constantes ou les « fonctions »

##### Raison

Les macros sont une source majeure de bugs. Elles ne respectent pas les règles habituelles de portée et de typage. Elles ne respectent pas les règles habituelles de passage d'arguments. Elles font voir à l'humain quelque chose de différent de ce que voit le compilateur. Elles compliquent la construction d'outils.

##### Exemple, mauvais

    #define PI 3.14
    #define SQUARE(a, b) (a * b)

Même si nous n'avions pas laissé le bug bien connu dans `SQUARE`, il existe des alternatives bien mieux comportées ; par ex. :

    constexpr double pi = 3.14;
    template<typename T> T square(T a, T b) { return a * b; }

##### Application

Screamer lorsqu'une macro n'est pas uniquement utilisée pour le contrôle de source (par ex. `#ifdef`).

### <a name="res-all_caps"></a>ES.32 : Utiliser `ALL_CAPS` pour tous les noms de macros

##### Raison

Convention. Lisibilité. Distinction des macros.

##### Exemple

    #define forever for (;;)   /* très MAUVAIS */

    #define FOREVER for (;;)   /* Toujours mauvais, mais au moins visible pour les humains */

##### Application

Screamer lorsqu'une macro est en minuscules.

### <a name="res-macros3"></a>ES.33 : Si vous devez absolument utiliser des macros, leur donner des noms uniques

##### Raison

Les macros ne respectent pas les règles de portée.

##### Exemple

    #define MYCHAR        /* MAUVAIS, entrera éventuellement en conflit avec un autre MYCHAR */

    #define ZCORP_CHAR    /* Toujours mauvais, mais moins susceptible de conflit */

##### Note

Évitez les macros si vous le pouvez : [ES.30](010-expr.md#res-macros), [ES.31](010-expr.md#res-macros2) et [ES.32](010-expr.md#res-all_caps).  
Cependant, il existe des milliards de lignes de code parsemées de macros et une longue tradition d'utilisation et d'abus des macros. Si vous êtes forcé d'utiliser des macros, utilisez des noms longs et, idéalement, un préfixe unique (par ex. le nom de votre organisation) pour réduire la probabilité de conflit.

##### Application

Avertir les noms de macros courts.

### <a name="res-ellipses"></a>ES.34 : Ne pas définir une fonction variadique de style C

##### Raison

Pas sûr au niveau du type. Nécessite du code de cast et de macro désordonné pour fonctionner correctement.

##### Exemple

    #include <cstdarg>

    // « severity » suivi d'une liste terminée par zéro de `char*` ; écrit les chaînes C‑style sur `cerr`
    void error(int severity ...)
    {
        va_list ap;             // type magique pour contenir les arguments
        va_start(ap, severity); // démarrage des arguments : « severity » est le premier argument de `error()`

        for (;;) {
            // traiter le prochain var comme un `char*` ; pas de vérification : cast déguisé
            char* p = va_arg(ap, char*);
            if (!p) break;
            cerr << p << ' ';
        }

        va_end(ap);             // nettoyage des arguments (ne pas oublier)

        cerr << '\n';
        if (severity) exit(severity);
    }

    void use()
    {
        error(7, "this", "is", "an", "error", nullptr);
        error(7); // plantage
        error(7, "this", "is", "an", "error");  // plantage
        const char* is = "is";
        string an = "an";
        error(7, "this", is, an, "error"); // plantage
    }

**Alternative** : surcharge, templates, variadic templates.

    #include <iostream>

    void error(int severity)
    {
        std::cerr << '\n';
        std::exit(severity);
    }

    template<typename T, typename... Ts>
    constexpr void error(int severity, T head, Ts... tail)
    {
        std::cerr << head;
        error(severity, tail...);
    }

    void use()
    {
        error(7); // Pas de plantage !
        error(5, "this", "is", "not", "an", "error"); // Pas de plantage !

        std::string an = "an";
        error(7, "this", "is", "not", an, "error"); // Pas de plantage !

        error(5, "oh", "no", nullptr); // Erreur de compilation ! Pas besoin de `nullptr`.
    }

##### Note

C'est essentiellement la façon dont `printf` est implémenté.

##### Application

* Signaler les définitions de fonctions variadiques de style C.  
* Signaler les inclusions de `<cstdarg>` et `<stdarg.h>`.

## ES.expr : Expressions

Les expressions manipulent des valeurs.

### <a name="res-complicated"></a>ES.40 : Éviter les expressions compliquées

##### Raison

Les expressions compliquées sont sources d'erreurs.

##### Exemple

    // mauvais : assignation cachée dans une sous‑expression
    while ((c = getc()) != -1)

    // mauvais : deux variables non‑locales assignées dans des sous‑expressions
    while ((cin >> c1, cin >> c2), c1 == c2)

    // meilleur, mais peut‑être encore trop compliqué
    for (char c1, c2; cin >> c1 >> c2 && c1 == c2;)

    // OK : si i et j ne sont pas aliasés
    int x = ++i + ++j;

    // OK : si i != j et i != k
    v[i] = v[j] + v[k];

    // mauvais : plusieurs assignations « cachées » dans des sous‑expressions
    x = a + (b = f()) + (c = g()) * 7;

    // mauvais : s'appuie sur des règles de priorité souvent mal comprises
    x = a & b + c * d && e ^ f == 7;

    // mauvais : comportement indéfini
    x = x++ + x++ + ++x;

Certaines de ces expressions sont inconditionnellement mauvaises (par ex. elles reposent sur un comportement indéfini). D'autres sont simplement tellement compliquées et/ou inhabituelles que même de bons programmeurs pourraient les mal interpréter ou en passer à côté lorsqu'ils sont pressés.

##### Note

C++17 resserre les règles d'ordre d'évaluation (de gauche à droite sauf de droite à gauche dans les assignations, et l'ordre d'évaluation des arguments de fonction reste non spécifié ; voir [ES.43](010-expr.md#res-order)), mais cela ne change pas le fait que les expressions compliquées peuvent être source de confusion.

##### Note

Un programmeur devrait connaître et utiliser les règles de base des expressions.

##### Exemple

    x = k * y + z;             // OK

    auto t1 = k * y;           // mauvais : inutilement verbeux
    x = t1 + z;

    if (0 <= x && x < max)   // OK

    auto t1 = 0 <= x;        // mauvais : inutilement verbeux
    auto t2 = x < max;
    if (t1 && t2)            // …

##### Application

Difficile. Quelle complexité doit-on considérer comme « compliquée » ? Écrire les calculs comme des instructions avec une opération chacune est aussi déroutant. Points à considérer :

* effets de bord : les effets de bord sur plusieurs variables non‑locales (pour une certaine définition de non‑local) peuvent être suspects, surtout si les effets de bord sont dans des sous‑expressions séparées  
* écritures sur des variables aliasées  
* plus de N opérateurs (et quel N choisir ?)  
* dépendance à des règles de priorité subtiles  
* utilisation de comportements indéfinis (peut‑on tous les détecter ?)  
* comportement dépendant de l'implémentation ?  
* ???

### <a name="res-parens"></a>ES.41 : En cas de doute sur la priorité des opérateurs, mettre des parenthèses

##### Raison

Éviter les erreurs. Lisibilité. Tout le monde ne connaît pas la table de priorité par cœur.

##### Exemple

    const unsigned int flag = 2;
    unsigned int a = flag;

    if (a & flag != 0)  // mauvais : signifie `a&(flag != 0)`

Note : Nous recommandons que les programmeurs connaissent leur table de priorité pour les opérations arithmétiques, logiques, mais envisagent de parenthéser lorsqu'ils mélangent des opérations logiques bit à bit avec d'autres opérateurs.

    if ((a & flag) != 0)  // OK : fonctionne comme prévu

##### Note

Vous devriez savoir suffisamment pour ne pas avoir besoin de parenthèses pour :

    if (a < 0 || a <= max) {
        // …
    }

##### Application

* Signaler les combinaisons d'opérateurs logiques bit à bit et d'autres opérateurs.  
* Signaler les opérateurs d'assignation qui ne sont pas l'opérateur le plus à gauche.  
* ???

### <a name="res-ptr"></a>ES.42 : Garder l'utilisation des pointeurs simple et directe

##### Raison

La manipulation compliquée de pointeurs est une source majeure d'erreurs.

##### Note

Utilisez `gsl::span` à la place. Les pointeurs ne devraient [déférer qu'à des objets uniques](005-interfaces.md#ri-array). L'arithmétique de pointeurs est fragile et facile à mal faire, source de nombreux bugs et violations de sécurité. `span` est un type sûr, vérifié à la compilation, pour accéder à des tableaux de données. L'accès à un tableau avec des bornes connues en utilisant une constante comme indice peut être validé par le compilateur.

##### Exemple, mauvais

    void f(int* p, int count)
    {
        if (count < 2) return;

        int* q = p + 1;    // MAUVAIS

        ptrdiff_t d;
        int n;
        d = (p - &n);      // OK
        d = (q - p);       // OK

        int n = *p++;      // MAUVAIS

        if (count < 6) return;

        p[4] = 1;          // MAUVAIS

        p[count - 1] = 2;  // MAUVAIS

        use(&p[0], 3);     // MAUVAIS
    }

##### Exemple, bon

    void f(span<int> a) // MIEUX : utiliser `span` dans la déclaration de fonction
    {
        if (a.size() < 2) return;

        int n = a[0];      // OK

        span<int> q = a.subspan(1); // OK

        if (a.size() < 6) return;

        a[4] = 1;          // OK

        a[a.size() - 1] = 2;  // OK

        use(a.data(), 3);  // OK
    }

##### Note

L'indexation avec une variable est difficile à valider tant pour les outils que pour les humains. `span` est un type sûr, vérifié à l'exécution, pour accéder à des tableaux de données. `at()` est une autre alternative qui assure que chaque accès est vérifié. Si des itérateurs sont nécessaires pour accéder à un tableau, utilisez les itérateurs fournis par un `span` construit sur le tableau.

##### Exemple, mauvais

    void f(array<int, 10> a, int pos)
    {
        a[pos / 2] = 1; // MAUVAIS
        a[pos - 1] = 2; // MAUVAIS
        a[-1] = 3;    // MAUVAIS (facile à détecter par les outils) – pas de remplacement, il faut simplement ne pas le faire
        a[10] = 4;    // MAUVAIS (facile à détecter par les outils) – pas de remplacement, il faut simplement ne pas le faire
    }

##### Exemple, bon

Utiliser un `span` :

    void f1(span<int, 10> a, int pos) // A1 : changer le type de paramètre pour utiliser `span`
    {
        a[pos / 2] = 1; // OK
        a[pos - 1] = 2; // OK
    }

    void f2(array<int, 10> arr, int pos) // A2 : ajouter un `span` local et l'utiliser
    {
        span<int> a = {arr.data(), pos};
        a[pos / 2] = 1; // OK
        a[pos - 1] = 2; // OK
    }

Utiliser `at()` :

    void f3(array<int, 10> a, int pos) // ALTERNATIVE B : utiliser `at()`
    {
        at(a, pos / 2) = 1; // OK
        at(a, pos - 1) = 2; // OK
    }

##### Exemple, mauvais

    void f()
    {
        int arr[COUNT];
        for (int i = 0; i < COUNT; ++i)
            arr[i] = i; // MAUVAIS, ne peut pas utiliser d'indice non constant
    }

##### Exemple, bon

Utiliser un `span` :

    void f1()
    {
        int arr[COUNT];
        span<int> av = arr;
        for (int i = 0; i < COUNT; ++i)
            av[i] = i;
    }

Utiliser un `span` et une boucle `range‑for` :

    void f1a()
    {
         int arr[COUNT];
         span<int, COUNT> av = arr;
         int i = 0;
         for (auto& e : av)
             e = i++;
    }

Utiliser `at()` :

    void f2()
    {
        int arr[COUNT];
        for (int i = 0; i < COUNT; ++i)
            at(arr, i) = i;
    }

Utiliser une boucle `range‑for` :

    void f3()
    {
        int arr[COUNT];
        int i = 0;
        for (auto& e : arr)
             e = i++;
    }

##### Note

Les outils peuvent proposer des réécritures d'accès à un tableau qui impliquent une expression d'indice dynamique afin d'utiliser `at()` à la place :

    static int a[10];

    void f(int i, int j)
    {
        a[i + j] = 12;      // MAUVAIS, pourrait être réécrit en …
        at(a, i + j) = 12;  // OK – vérifié à l'exécution
    }

##### Exemple

Transformer un tableau en pointeur (ce que le langage fait essentiellement toujours) supprime les possibilités de vérification, il faut donc l'éviter :

    void g(int* p);

    void f()
    {
        int a[5];
        g(a);        // MAUVAIS : essayons‑nous de passer un tableau ?
        g(&a[0]);    // OK : on passe un seul objet
    }

Si vous voulez passer un tableau, dites‑le :

    void g(int* p, size_t length);  // ancien (dangereux) code

    void g1(span<int> av); // MIEUX : changer `g()`.

    void f2()
    {
        int a[5];
        span<int> av = a;

        g(av.data(), av.size());   // OK, si vous n'avez pas le choix
        g1(a);                     // OK – pas de décadence ici, utilisation du constructeur implicite de `span`
    }

##### Application

* Signaler toute opération arithmétique sur une expression de type pointeur qui aboutit à une valeur de type pointeur.  
* Signaler toute expression d'indexation sur une expression ou variable de type tableau (tableau statique ou `std::array`) où l'indice n'est pas une constante d'expression connue entre `0` et la borne supérieure du tableau.  
* Signaler toute expression qui dépendrait de la conversion implicite d'un type tableau en pointeur.

Cette règle fait partie du [profil de sécurité des limites](022-profile.md#ss-bounds).

### <a name="res-order"></a>ES.43 : Éviter les expressions avec un ordre d'évaluation indéfini

##### Raison

Vous n'avez aucune idée de ce que fait un tel code. Portabilité. Même si le code fait quelque chose de sensé pour vous, il pourrait faire autre chose avec un autre compilateur (par ex. la prochaine version de votre compilateur) ou avec d'autres options d'optimisation.

##### Note

C++17 resserre les règles d'ordre d'évaluation : de gauche à droite sauf de droite à gauche dans les assignations, et l'ordre d'évaluation des arguments de fonction reste non spécifié.

Cependant, rappelez‑vous que votre code pourrait être compilé avec un compilateur pré‑C++17 (par ex. via du copier‑coller) donc ne soyez pas trop astucieux.

##### Exemple

    v[i] = ++i;   // le résultat est indéfini

Une bonne règle de base est de ne pas lire une valeur deux fois dans une expression où vous l'écrivez.

##### Application

Peut être détecté par un bon analyseur.

### <a name="res-order-fct"></a>ES.44 : Ne pas dépendre de l'ordre d'évaluation des arguments de fonction

##### Raison

Parce que cet ordre n'est pas spécifié.

##### Note

C++17 resserre les règles d'ordre d'évaluation, mais l'ordre d'évaluation des arguments de fonction reste non spécifié.

##### Exemple

    int i = 0;
    f(++i, ++i);

Avant C++17, le comportement est indéfini, donc le résultat pourrait être n'importe quoi (par ex. `f(2, 2)`). Depuis C++17, ce code n'a pas de comportement indéfini, mais il n'est toujours pas spécifié quel argument est évalué en premier. L'appel sera `f(1, 2)` ou `f(2, 1)`, mais vous ne le savez pas.

##### Exemple

Les opérateurs surchargés peuvent entraîner des problèmes d'ordre d'évaluation :

    f1()->m(f2());          // m(f1(), f2())
    cout << f1() << f2();   // operator<<(operator<<(cout, f1()), f2())

En C++17, ces exemples fonctionnent comme prévu (de gauche à droite) et les assignations sont évaluées de droite à gauche (tout comme la liaison de `=`).

    f1() = f2();    // comportement indéfini en C++14 ; en C++17, `f2()` est évalué avant `f1()`

##### Application

Peut être détecté par un bon analyseur.

### <a name="res-magic"></a>ES.45 : Éviter les « magic constants » ; utiliser des constantes symboliques

##### Raison

Les constantes non nommées intégrées dans les expressions sont facilement oubliées et souvent difficiles à comprendre.

##### Exemple

    for (int m = 1; m <= 12; ++m)   // ne pas : constante magique 12
        cout << month[m] << '\n';

Nous ne savons pas tous qu'il y a 12 mois, numérotés de 1 à 12, dans une année. Mieux :

    // les mois sont indexés de 1 à 12
    constexpr int first_month = 1;
    constexpr int last_month = 12;

    for (int m = first_month; m <= last_month; ++m)   // meilleur
        cout << month[m] << '\n';

Encore mieux, ne pas exposer les constantes :

    for (auto m : month)
        cout << m << '\n';

##### Application

Signaler les littéraux dans le code. Autoriser une liste blanche pour `0`, `1`, `nullptr`, `'\n'`, `""`, etc.

### <a name="res-narrowing"></a>ES.46 : Éviter les conversions rétrécissantes (narrowing)

##### Raison

Une conversion rétrécissante détruit de l'information, souvent de façon inattendue.

##### Exemple, mauvais

Un exemple de base de rétrécissement :

    double d = 7.9;
    int i = d;    // mauvais : rétrécissement ; i devient 7
    i = (int) d;  // mauvais : on prétend que cela n'est toujours pas assez explicite

    void f(int x, long y, double d)
    {
        char c1 = x;   // mauvais : rétrécissement
        char c2 = y;   // mauvais : rétrécissement
        char c3 = d;   // mauvais : rétrécissement
    }

##### Note

La bibliothèque de directives propose une opération `narrow_cast` pour spécifier que le rétrécissement est acceptable et une fonction `narrow` (« narrow if ») qui lance une exception si le rétrécissement perdrait des valeurs légales :

    i = gsl::narrow_cast<int>(d);   // OK (vous avez demandé le rétrécissement) : i devient 7
    i = gsl::narrow<int>(d);        // OK : lance `narrowing_error`

Nous incluons également les castings arithmétiques rétrécissants, comme d'un type flottant négatif vers un type entier non signé :

    double d = -7.9;
    unsigned u = 0;

    u = d;                               // mauvais : rétrécissement
    u = gsl::narrow_cast<unsigned>(d);   // OK (vous avez demandé le rétrécissement) : u devient 4294967289
    u = gsl::narrow<unsigned>(d);        // OK : lance `narrowing_error`

##### Note

Cette règle ne s'applique pas aux [conversions contextuelles en booléen](https://en.cppreference.com/w/cpp/language/implicit_conversion#Contextual_conversions) :

    if (ptr) do_something(*ptr);   // OK : `ptr` est utilisé comme condition
    bool b = ptr;                  // mauvais : rétrécissement

##### Application

Un bon analyseur peut détecter toutes les conversions rétrécissantes. Cependant, signaler toutes les conversions rétrécissantes entraînera beaucoup de faux positifs. Suggestions :

* Signaler toutes les conversions de `float` → `int` (peut‑être seulement `float`→`char` et `double`→`int`. Ici il faut des données.)  
* Signaler toutes les conversions `long` → `char`. (Je soupçonne que `int`→`char` est très fréquent. Ici il faut des données.)  
* Considérer les conversions rétrécissantes pour les arguments de fonction comme particulièrement suspectes.

### <a name="res-nullptr"></a>ES.47 : Utiliser `nullptr` plutôt que `0` ou `NULL`

##### Raison

Lisibilité. Minimiser les surprises : `nullptr` ne peut pas être confondu avec un `int`. `nullptr` possède également un type très bien spécifié, et fonctionne donc dans plus de scénarios où `NULL` ou `0` pourraient induire le compilateur en erreur.

##### Exemple

    void f(int);
    void f(char*);
    f(0);         // appel à f(int)
    f(nullptr);   // appel à f(char*)

##### Application

Signaler les utilisations de `0` et `NULL` pour les pointeurs. La transformation peut être aidée par une simple transformation de programme.

### <a name="res-casts"></a>ES.48 : Éviter les castings

##### Raison

Les castings sont une source bien connue d'erreurs et rendent certaines optimisations peu fiables.

##### Exemple, mauvais

    double d = 2;
    auto p = (long*)&d;
    auto q = (long long*)&d;
    cout << d << ' ' << *p << ' ' << *q << '\n';

Que pensez‑vous que ce fragment imprime ? Le résultat est au mieux implémentation‑défini. J'ai obtenu :

    2 0 4611686018427387904

En ajoutant :

    *q = 666;
    cout << d << ' ' << *p << ' ' << *q << '\n';

J'ai obtenu :

    3.29048e-321 666 666

Surpris ? C'est en fait un comportement indéfini, et cela pourrait aussi bien planter le programme.

##### Note

Les programmeurs qui écrivent des castings supposent généralement qu'ils savent ce qu'ils font, ou que le cast rend le programme « plus lisible ». En fait, ils désactivent souvent les règles générales pour l'utilisation des valeurs. La résolution de surcharge et l'instanciation de templates choisissent généralement la bonne fonction s'il existe une fonction appropriée. S'il n'y en a pas, il vaudrait mieux en créer une plutôt que d'appliquer un correctif local (cast).

##### Notes

Les castings sont nécessaires dans un langage de programmation système. Par ex. comment obtenir l'adresse d'un registre de périphérique dans un pointeur ? Cependant, les castings sont sérieusement sur‑utilisés et constituent une source majeure d'erreurs.

Si vous sentez le besoin d'un grand nombre de castings, il y a probablement un problème de conception fondamental.

Le [profil de type](022-profile.md#pro-type-reinterpretcast) interdit `reinterpret_cast` et les castings de style C.

Ne jamais caster vers `(void)` pour ignorer une valeur de retour `[[nodiscard]]`. Si vous voulez vraiment ignorer ce résultat, réfléchissez d'abord si c'est réellement une bonne idée (il y a généralement une bonne raison pour laquelle l'auteur de la fonction ou du type de retour a utilisé `[[nodiscard]]`). Si vous êtes toujours convaincu, utilisez `std::ignore =` pour désactiver l'avertissement : c'est simple, portable et facile à rechercher.

##### Alternatives

Les castings sont largement (mal) utilisés. Le C++ moderne propose des règles et constructions qui éliminent le besoin de castings dans de nombreux contextes, tels que :

* Utiliser des templates  
* Utiliser `std::variant`  
* S'appuyer sur les conversions implicites bien définies et sûres entre types de pointeurs  
* Utiliser `std::ignore =` pour ignorer les valeurs `[[nodiscard]]`

##### Application

* Signaler tous les castings de style C, y compris vers `void`.  
* Signaler les castings de style fonctionnel `Type(value)`. Utilisez `Type{value}` à la place (voir [ES.64](010-expr.md#res-construct)).  
* Signaler les castings d'identité entre types pointeurs où le type source et le type cible sont les mêmes ([profil de type identité cast](022-profile.md#pro-type-identitycast)).  
* Signaler un cast de pointeur explicite qui pourrait être [implicite](022-profile.md#pro-type-implicitpointercast).

### <a name="res-casts-named"></a>ES.49 : Si vous devez caster, utilisez un cast nommé

##### Raison

Lisibilité. Éviter les erreurs. Les castings nommés sont plus spécifiques qu'un cast de style C ou fonctionnel, ce qui permet au compilateur d'intercepter certaines erreurs.

Les castings nommés sont :

* `static_cast`  
* `const_cast`  
* `reinterpret_cast`  
* `dynamic_cast`  
* `std::move`         // `move(x)` est une référence r‑value à `x`  
* `std::forward`      // `forward<T>(x)` est une référence l‑value ou r‑value à `x` selon `T`  
* `gsl::narrow_cast`  // `narrow_cast<T>(x)` est `static_cast<T>(x)`  
* `gsl::narrow`       // `narrow<T>(x)` est `static_cast<T>(x)` si `static_cast<T>(x) == x` sinon lance `narrowing_error`

##### Exemple

    class B { /* … */ };
    class D { /* … */ };

    D* downcast(B* pb)
    {
        D* pd0 = pb;                        // erreur : aucune conversion implicite de B* vers D*
        D* pd1 = (D*)pb;                    // légal, mais que fait‑on ?
        D* pd2 = static_cast<D*>(pb);       // erreur : D n'est pas dérivé de B
        D* pd3 = reinterpret_cast<D*>(pb); // OK : à vos risques et périls !
        D* pd4 = dynamic_cast<D*>(pb);      // OK : renvoie `nullptr`
        // …
    }

L'exemple provient de bugs réels où `D` dérivait de `B`, mais quelqu'un a refactorisé la hiérarchie. Le cast de style C est dangereux car il peut faire n'importe quel type de conversion, nous privant de toute protection contre les erreurs (aujourd'hui ou à l'avenir).

##### Note

Lors de la conversion entre types sans perte d'information (par ex. de `float` à `double` ou de `int32` à `int64`), l'initialisation avec des accolades peut être utilisée à la place.

    double d {some_float};
    int64_t i {some_int32};

Cela rend explicite que la conversion de type était intentionnelle et empêche les conversions entre types qui pourraient entraîner une perte de précision. (Il s'agit d'une erreur de compilation d'essayer d'initialiser un `float` à partir d'un `double`, par ex.).

##### Note

`reinterpret_cast` peut être essentiel, mais les usages essentiels (par ex. transformer une adresse machine en pointeur) ne sont pas sûrs au niveau du type :

    auto p = reinterpret_cast<Device_register>(0x800);  // intrinsèquement dangereux

##### Application

* Signaler tous les castings de style C, y compris vers `void`.  
* Signaler les castings de style fonctionnel `Type(value)`. Utilisez `Type{value}` à la place (voir [ES.64](010-expr.md#res-construct)).  
* Le [profil de type](022-profile.md#pro-type-reinterpretcast) interdit `reinterpret_cast`.  
* Le [profil de type](022-profile.md#pro-type-arithmeticcast) avertit lorsqu'on utilise `static_cast` entre types arithmétiques.

### <a name="res-casts-const"></a>ES.50 : Ne pas enlever le `const` avec un cast

##### Raison

Cela ment au `const`. Si la variable est réellement déclarée `const`, la modifier entraîne un comportement indéfini.

##### Exemple, mauvais

    void f(const int& x)
    {
        const_cast<int&>(x) = 42;   // MAUVAIS
    }

    static int i = 0;
    static const int j = 0;

    f(i); // effet de bord silencieux
    f(j); // comportement indéfini

##### Exemple

Parfois, vous pourriez être tenté d'utiliser `const_cast` pour éviter la duplication de code, par ex. lorsque deux fonctions d'accès qui ne diffèrent que par le `const` ont une implémentation similaire. Par ex. :

    class Bar;

    class Foo {
    public:
        // MAUVAIS, duplique la logique
        Bar& get_bar()
        {
            /* logique complexe pour obtenir une référence non‑const à my_bar */
        }

        const Bar& get_bar() const
        {
            /* même logique complexe */
        }
    private:
        Bar my_bar;
    };

Au lieu de cela, partagez les implémentations. Normalement, vous pouvez simplement faire appeler la fonction non‑`const` la fonction `const`. Cependant, lorsqu'il y a une logique complexe, cela peut conduire au modèle suivant qui utilise encore `const_cast` :

    class Foo {
    public:
        // pas idéal, non‑const appelle la version const mais utilise `const_cast`
        Bar& get_bar()
        {
            return const_cast<Bar&>(static_cast<const Foo&>(*this).get_bar());
        }
        const Bar& get_bar() const
        {
            /* logique complexe pour obtenir une référence const à my_bar */
        }
    private:
        Bar my_bar;
    };

Bien que ce modèle soit sûr lorsqu'il est appliqué correctement, ce n'est pas idéal car la sécurité est difficile à faire appliquer automatiquement comme règle de vérification.

Au lieu de cela, placez le code commun dans une fonction d'aide — et faites‑en une fonction‑template afin qu'elle déduise `const`. Cela n'utilise aucun `const_cast` :

    class Foo {
    public:                         // bon
              Bar& get_bar()       { return get_bar_impl(*this); }
        const Bar& get_bar() const { return get_bar_impl(*this); }
    private:
        Bar my_bar;

        template<class T>           // bon, déduit si T est `const` ou non
        static auto& get_bar_impl(T& t)
            { /* logique complexe pour obtenir une référence possiblement‑const à my_bar */ }
    };

Note : Ne pas mettre trop de travail non‑dépendant dans un template, sinon cela peut entraîner un gonflement du code. Par ex., une amélioration supplémentaire serait que certaines parties de `get_bar_impl` puissent être non‑dépendantes et extraites dans une fonction non‑template, réduisant ainsi la taille du code.

##### Exception

Vous pourriez devoir enlever le `const` lors de l'appel de fonctions qui ne sont pas `const`‑correctes. Préférez encapsuler de telles fonctions dans des wrappers `inline` `const`‑corrects afin de centraliser le cast à un seul endroit.

##### Exemple

Parfois, « enlever le `const` » sert à mettre à jour des informations transitoires d'un objet autrement immuable. Des exemples sont la mise en cache, la mémoïsation et le pré‑calcul. Ces cas sont souvent gérés de façon plus ou moins correcte avec `mutable` ou une indirection plutôt qu'avec `const_cast`.

Considérez la mise en cache des résultats d'une opération coûteuse :

    int compute(int x); // calculer une valeur pour x ; on suppose que c'est coûteux

    class Cache {   // type implémentant un cache pour une fonction int → int
    public:
        pair<bool, int> find(int x) const;   // y a‑t‑il une valeur pour x ?
        void set(int x, int v);             // enregistrer la valeur pour x
        // …
    private:
        // …
    };

    class X {
    public:
        int get_val(int x)
        {
            auto p = cache.find(x);
            if (p.first) return p.second;
            int val = compute(x);
            cache.set(x, val); // insérer la valeur pour x
            return val;
        }
        // …
    private:
        Cache cache;
    };

Ici, `get_val()` est logiquement `const`, donc nous aimerions le rendre `const`. Pour ce faire, nous devons encore muter `cache`, donc les programmeurs utilisent parfois `const_cast` :

    class X {   // solution douteuse basée sur le cast
    public:
        int get_val(int x) const
        {
            auto p = cache.find(x);
            if (p.first) return p.second;
            int val = compute(x);
            const_cast<Cache&>(cache).set(x, val);   // laid
            return val;
        }
        // …
    private:
        Cache cache;
    };

Heureusement, il existe une meilleure solution : déclarer `cache` comme `mutable` même pour les objets `const` :

    class X {   // meilleure solution
    public:
        int get_val(int x) const
        {
            auto p = cache.find(x);
            if (p.first) return p.second;
            int val = compute(x);
            cache.set(x, val);
            return val;
        }
        // …
    private:
        mutable Cache cache;
    };

Une solution alternative serait de stocker un pointeur vers le `cache` :

    class X {   // OK, mais légèrement plus compliqué
    public:
        int get_val(int x) const
        {
            auto p = cache->find(x);
            if (p.first) return p.second;
            int val = compute(x);
            cache->set(x, val);
            return val;
        }
        // …
    private:
        unique_ptr<Cache> cache;
    };

Cette solution est la plus flexible, mais nécessite une construction et une destruction explicites de `*cache` (probablement dans le constructeur et le destructeur de `X`).

Dans tous les cas, nous devons protéger contre les courses de données sur `cache` dans le code multithread, éventuellement en utilisant un `std::mutex`.

##### Application

* Signaler les `const_cast`.  
* Cette règle fait partie du [profil de sécurité du type](022-profile.md#pro-type-constcast) pour le profil correspondant.

### <a name="res-range-checking"></a>ES.55 : Éviter le besoin de vérifications de limites

##### Raison

Les constructions qui ne peuvent pas déborder ne déborderont jamais (et généralement s'exécutent plus rapidement) :

##### Exemple

    for (auto& x : v)      // imprimer tous les éléments de v
        cout << x << '\n';

    auto p = find(v, x);   // trouver x dans v

##### Application

Rechercher les vérifications de limites explicites et suggérer heuristiquement des alternatives.

### <a name="res-move"></a>ES.56 : N'écrire `std::move()` que lorsqu'il faut explicitement déplacer un objet vers une autre portée

##### Raison

Nous déplaçons, plutôt que de copier, pour éviter la duplication et améliorer les performances.

Un déplacement laisse généralement derrière lui un objet vide ([C.64](007-functions.md#rc-move-semantic) @TODO‑LINK), ce qui peut surprendre ou même être dangereux, donc nous essayons d'éviter de déplacer des l‑values (elles pourraient être utilisées plus tard).

##### Notes

Le déplacement se fait implicitement lorsque la source est une r‑value (par ex. la valeur retournée d'une fonction ou le résultat d'une fonction), donc n'ajoutez pas inutilement `move` dans ces cas. Au lieu de cela, écrivez de petites fonctions qui retournent des valeurs ; le retour de la fonction et l'acceptation du retour par l'appelant seront optimisés naturellement.

En général, suivre les directives de ce document (y compris ne pas déclarer des portées de variables inutilement grandes, écrire de petites fonctions qui retournent des valeurs, retourner des variables locales) aide à éliminer la plupart des besoins de `std::move` explicite. `std::move` explicite est nécessaire pour déplacer explicitement un objet vers une autre portée, notamment pour le passer à une fonction « sink » et dans les implémentations des opérateurs de déplacement eux‑mêmes (constructeur de déplacement, opérateur d'affectation de déplacement) et les opérations d'échange.

##### Exemple, mauvais

    void sink(X&& x);   // `sink` prend possession de x

    void user()
    {
        X x;
        // erreur : impossible de lier une l‑value à une référence r‑value
        sink(x);
        // OK : `sink` prend le contenu de x, x doit maintenant être considéré comme vide
        sink(std::move(x));

        // ...

        // probablement une erreur
        use(x);
    }

Habituellement, `std::move()` est utilisé comme argument d'un paramètre `&&`. Après cela, supposez que l'objet a été déplacé (par ex. `use(x)` devrait être évité jusqu'à ce que vous le ré‑initialisiez).

    void f()
    {
        string s1 = "supercalifragilisticexpialidocious";

        string s2 = s1;             // ok, copie
        assert(s1 == "supercalifragilisticexpialidocious");  // ok

        // mauvais, si vous voulez garder la valeur de s1
        string s3 = move(s1);

        // mauvais, l'assertion échouera probablement, s1 a probablement changé
        assert(s1 == "supercalifragilisticexpialidocious");
    }

##### Exemple

    void sink(unique_ptr<widget> p);  // passer la propriété de p à sink()

    void f()
    {
        auto w = make_unique<widget>();
        // …
        sink(std::move(w));               // ok, donner à sink()
        // …
        sink(w);    // Erreur : `unique_ptr` est conçu pour empêcher la copie
    }

##### Notes

`std::move()` est un cast vers `&&` déguisé ; il ne déplace rien en soi, il marque simplement un objet nommé comme candidat pouvant être déplacé. Le langage connaît déjà les cas courants où les objets peuvent être déplacés, notamment lors du retour de valeurs depuis des fonctions, donc n'encombrez pas le code avec des `std::move()` redondants.

Ne jamais écrire `std::move()` simplement parce qu'on a entendu « c'est plus efficace ». En général, ne croyez pas les affirmations d'« efficacité » sans données (???). En général, ne compliquez pas votre code sans raison (??). Ne jamais écrire `std::move()` sur un objet `const`, cela se transforme silencieusement en copie (voir l'Item 23 dans [Meyers15](032-bibliography.md#Meyers15) @TODO‑LINK).

##### Exemple, mauvais

    vector<int> make_vector()
    {
        vector<int> result;
        // … charger result avec des données
        return std::move(result);       // mauvais ; écrivez simplement « return result ; »
    }

Ne jamais écrire `return move(local_variable);`, car le langage sait déjà que la variable locale est un candidat au déplacement. Écrire `move` dans ce code n'aide pas, et peut même être préjudiciable car certains compilateurs interfèrent avec le RVO (l'optimisation de retour de valeur) en créant une référence supplémentaire à la variable locale.

##### Exemple, mauvais

    vector<int> v = std::move(make_vector());   // mauvais ; le `std::move` est totalement redondant

Ne jamais écrire `move` sur une valeur retournée telle que `x = move(f());` où `f` retourne par valeur. Le langage sait déjà que la valeur retournée est un objet temporaire qui peut être déplacé.

##### Exemple

    void mover(X&& x)
    {
        call_something(std::move(x));         // ok
        call_something(std::forward<X>(x));   // mauvais, ne pas `std::forward` une r‑value reference
        call_something(x);                    // suspect, pourquoi pas `std::move` ?
    }

    template<class T>
    void forwarder(T&& t)
    {
        call_something(std::move(t));         // mauvais, ne pas `std::move` une référence de transmission
        call_something(std::forward<T>(t));   // ok
        call_something(t);                    // suspect, pourquoi pas `std::forward` ?
    }

##### Application

* Signaler l'utilisation de `std::move(x)` où `x` est une r‑value ou le langage le traitera déjà comme une r‑value, y compris `return std::move(local_variable);` et `std::move(f())` sur une fonction qui retourne par valeur.  
* Signaler les fonctions prenant un paramètre `S&&` s'il n'existe pas de surcharge `const S&` pour gérer les l‑values.  
* Signaler un argument `std::move`‑é passé à un paramètre, sauf lorsque le type du paramètre est une référence r‑value `S&&` ou que le type est move‑only et le paramètre est passé par valeur.  
* Signaler un `std::move` appliqué à une référence de transmission (`T&&` où `T` est un paramètre de template). Utilisez `std::forward` à la place.  
* Signaler un `std::move` appliqué à autre chose qu'une référence r‑value non‑`const`. (Cas plus général du point précédent pour couvrir les cas non‑transmission.)  
* Signaler un `std::forward` appliqué à une référence r‑value (`X&&` où `X` n'est pas un paramètre de template). Utilisez `std::move` à la place.  
* Signaler un `std::forward` appliqué à autre chose qu'une référence de transmission. (Cas plus général du point précédent.)  
* Signaler lorsqu'un objet est potentiellement déplacé et que l'opération suivante est une opération `const` ; il devrait d'abord y avoir une opération non‑`const`, idéalement une assignation, pour réinitialiser la valeur de l'objet.

### <a name="res-new"></a>ES.60 : Éviter `new` et `delete` en dehors des fonctions de gestion de ressources

##### Raison

La gestion directe des ressources dans le code applicatif est source d'erreurs et fastidieuse.

##### Note

C'est aussi connu sous le nom de règle « Pas de `new` nu ! »

##### Exemple, mauvais

    void f(int n)
    {
        auto p = new X[n];   // n objets `X` par défaut construits
        // …
        delete[] p;
    }

Il peut y avoir du code dans la partie `…` qui empêche que le `delete` soit jamais exécuté.

**Voir aussi** : [R : Gestion des ressources](009-resource.md)

##### Application

Signaler les `new` nus et les `delete` nus.

### <a name="res-del"></a>ES.61 : Supprimer les tableaux avec `delete[]` et les non‑tableaux avec `delete`

##### Raison

C'est ce que le langage exige, et les incompatibilités peuvent entraîner des erreurs de libération de ressources et/ou des corruptions de mémoire.

##### Exemple, mauvais

    void f(int n)
    {
        auto p = new X[n];   // n objets `X` par défaut construits
        // …
        delete p;   // erreur : supprime l'objet `p`, pas le tableau `p[]`
    }

##### Note

Cet exemple ne viole pas seulement la règle « pas de `new` nu » précédente, il comporte bien plus de problèmes.

##### Application

* Signaler les `new` et `delete` incompatibles lorsqu'ils sont dans la même portée.  
* Signaler les `new` et `delete` incompatibles lorsqu'ils sont dans une paire constructeur / destructeur.

### <a name="res-arr2"></a>ES.62 : Ne pas comparer des pointeurs appartenant à des tableaux différents

##### Raison

Le résultat est indéfini.

##### Exemple, mauvais

    void f()
    {
        int a1[7];
        int a2[9];
        if (&a1[5] < &a2[7]) {}       // mauvais : indéfini
        if (0 < &a1[5] - &a2[7]) {}   // mauvais : indéfini
    }

##### Note

Cet exemple comporte de nombreux autres problèmes.

##### Application

???

### <a name="res-slice"></a>ES.63 : Ne pas « slice »

##### Raison

Le slicing — c'est‑à‑dire copier seulement une partie d'un objet via assignation ou initialisation — conduit le plus souvent à des erreurs parce que l'objet était censé être considéré dans son ensemble. Dans les rares cas où le slicing était intentionnel, le code peut être surprenant.

##### Note

Il n'est pas possible de copier une partie d'un objet vide, donc cette définition de slicing exclut délibérément les objets vides (sans membres de données non statiques), tels que les types vides utilisés pour le dispatch par tag.

##### Exemple

    class Shape { /* … */ };
    class Circle : public Shape { /* … */ Point c; int r; };

    Circle c { {0, 0}, 42 };
    Shape s {c};    // copie uniquement la partie `Shape` de `Circle`
    s = c;          // ou copie‑assignation uniquement la partie `Shape` de `Circle`

    void assign(const Shape& src, Shape& dest)
    {
        dest = src;
    }
    Circle c2 { {1, 1}, 43 };
    assign(c, c2);   // oups, tout l'état n'est pas transféré
    assert(c == c2); // si nous fournissons une comparaison, elle sera probablement fausse

Le résultat sera dénué de sens parce que le centre et le rayon ne sont pas copiés de `c` vers `s`. La première défense contre cela est d'[interdire la copie du type de base `Shape`](007-class.md#rc-copy-virtual).

##### Alternative

Si vous vouliez réellement « slice », définissez une opération explicite pour le faire. Cela évite aux lecteurs d'être confus.

    class Smiley : public Circle {
        public:
        Circle copy_circle();
        // …
    };

    Smiley sm { /* … */ };
    Circle c1 {sm};  // idéalement empêché par la définition de `Circle`
    Circle c2 {sm.copy_circle()};

##### Application

Avertir du slicing si le type de base possède des membres de données non statiques (possiblement via des bases transverses).

### <a name="res-construct"></a>ES.64 : Utiliser la notation `T{e}` pour la construction

##### Raison

La syntaxe de construction `T{e}` rend explicite que l'on veut construire. Elle n'autorise pas le rétrécissement. `T{e}` est la seule expression sûre et générale pour construire une valeur de type `T` à partir d'une expression `e`. Les notations de cast `T(e)` et `(T)e` ne sont ni sûres ni générales.

##### Exemple

Pour les types intégrés, la notation de construction protège contre le rétrécissement et la réinterprétation :

    void use(char ch, int i, double d, char* p, long long lng)
    {
        int x1 = int{ch};     // OK, mais redondant
        int x2 = int{d};      // erreur : double→int rétrécissant ; utilisez un cast si vous en avez besoin
        int x3 = int{p};      // erreur : pointeur→int ; utilisez `reinterpret_cast` si vous en avez vraiment besoin
        int x4 = int{lng};    // erreur : long long→int rétrécissant ; utilisez un cast si vous en avez besoin

        int y1 = int(ch);     // OK, mais redondant
        int y2 = int(d);      // mauvais : double→int rétrécissant ; utilisez un cast si vous en avez besoin
        int y3 = int(p);      // mauvais : pointeur→int ; utilisez `reinterpret_cast` si vous en avez vraiment besoin
        int y4 = int(lng);    // mauvais : long long→int rétrécissant ; utilisez un cast si vous en avez besoin

        int z1 = (int)ch;     // OK, mais redondant
        int z2 = (int)d;      // mauvais : double→int rétrécissant ; utilisez un cast si vous en avez besoin
        int z3 = (int)p;      // mauvais : pointeur→int ; utilisez `reinterpret_cast` si vous en avez vraiment besoin
        int z4 = (int)lng;    // mauvais : long long→int rétrécissant ; utilisez un cast si vous en avez besoin
    }

Les conversions entiers ↔ pointeurs sont implémentation‑définies avec les notations `T(e)` ou `(T)e`, et non portables entre plates‑formes avec des tailles d'entier et de pointeur différentes.

##### Note

[Éviter les castings](010-expr.md#res-casts) (conversion de type explicite) et si vous devez caster, préférez les castings nommés ([ES.49](010-expr.md#res-casts-named)).

##### Note

Lorsque c'est non ambigu, le `T` peut être omis de `T{e}`.

    complex<double> f(complex<double>);

    auto z = f({2*pi, 1});

##### Note

La notation de construction est la plus générale [notation d'initialisation](010-expr.md#res-list).

##### Exception

`std::vector` et d'autres conteneurs ont été définis avant que nous ayons `{}` comme notation de construction. Considérez :

    vector<string> vs {10};                           // dix chaînes vides
    vector<int> vi1 {1, 2, 3, 4, 5, 6, 7, 8, 9, 10};  // dix éléments 1..10
    vector<int> vi2 {10};                             // un élément de valeur 10

Comment obtenir un `vector` de 10 `int`s initialisés par défaut ?

    vector<int> v3(10); // dix éléments avec valeur 0

L'utilisation de `()` plutôt que `{}` pour le nombre d'éléments est une tradition (remontant aux années 1980), difficile à changer, mais c'est tout de même une erreur de conception : pour un conteneur où le type d'élément peut être confondu avec le nombre d'éléments, nous avons une ambiguïté qui doit être résolue. La résolution conventionnelle consiste à interpréter `{10}` comme une liste d'un seul élément et à utiliser `(10)` pour distinguer une taille.

Cette ambiguïté n'a pas besoin d'être répétée dans le nouveau code. Nous pouvons définir un type pour représenter le nombre d'éléments :

    struct Count { int n; };

    template<typename T>
    class Vector {
    public:
        Vector(Count n);                     // n éléments initialisés par défaut
        Vector(initializer_list<T> init);    // init.size() éléments
        // …
    };

    Vector<int> v1{10};
    Vector<int> v2{Count{10}};
    Vector<Count> v3{Count{10}};    // oui, il reste un tout petit problème

Le principal problème restant est de trouver un nom approprié pour `Count`.

##### Application

Signaler les castings C‑style `(T)e` et les castings fonctionnels `T(e)`.

### <a name="res-deref"></a>ES.65 : Ne pas déréférencer un pointeur invalide

##### Raison

Déréférencer un pointeur invalide, tel que `nullptr`, entraîne un comportement indéfini, généralement un plantage immédiat, des résultats erronés ou une corruption de mémoire.

##### Note

Par « pointeur », on entend toute indirection vers un objet, y compris un itérateur ou une vue équivalente.

##### Note

Cette règle est évidente et bien connue, mais peut être difficile à appliquer. Elle nécessite de bons styles de codage, le support de bibliothèques et l'analyse statique pour éliminer les violations sans surcharge majeure. C'est une partie importante de la discussion sur le modèle C++ de sécurité de type et de ressources ([Stroustrup15](032-bibliography.md#Stroustrup15)).

**Voir aussi** :

* Utiliser [RAII](009-resource.md#rr-raii) pour éviter les problèmes de durée de vie.  
* Utiliser [unique_ptr](006-functions.md#rf-unique_ptr) pour éviter les problèmes de durée de vie.  
* Utiliser [shared_ptr](006-functions.md#rf-shared_ptr) pour éviter les problèmes de durée de vie.  
* Utiliser [références](006-functions.md#rf-ptr-ref) lorsque `nullptr` n'est pas une possibilité.  
* Utiliser [not_null](006-functions.md#rf-nullptr) pour détecter tôt les `nullptr` inattendus.  
* Utiliser le [profil des limites](022-profile.md#ss-bounds) pour éviter les erreurs de plage.

##### Exemple

    void f()
    {
        int x = 0;
        int* p = &x;

        if (condition()) {
            int y = 0;
            p = &y;
        } // invalide p

        *p = 42;            // MAUVAIS, p pourrait être invalide si le branchement a été pris
    }

Pour résoudre le problème, soit étendre la durée de vie de l'objet auquel le pointeur doit se référer, soit raccourcir la durée de vie du pointeur (déplacer le déréférencement avant la fin de vie de l'objet).

    void f1()
    {
        int x = 0;
        int* p = &x;

        int y = 0;
        if (condition()) {
            p = &y;
        }

        *p = 42;            // OK, p pointe sur x ou y et les deux sont encore en portée
    }

Malheureusement, la plupart des problèmes de pointeur invalide sont plus difficiles à repérer et à corriger.

##### Exemple

    void f(int* p)
    {
        int x = *p; // MAUVAIS : comment savoir que p est valide ?
    }

Il existe une énorme quantité de ce type de code. La plupart du temps – après de nombreux tests – il est impossible de dire si `p` pourrait être `nullptr`. Par conséquent, c'est aussi une source majeure d'erreurs. Il existe de nombreuses approches pour gérer ce problème potentiel :

    void f1(int* p) // gérer `nullptr`
    {
        if (!p) {
            // gérer `nullptr` (allocation, retour, exception, etc.)
        }
        int x = *p;
    }

Il y a deux problèmes potentiels avec le test `nullptr` :

* il n'est pas toujours évident quoi faire si on trouve `nullptr` ;  
* le test peut être redondant et/ou relativement coûteux ;  
* il n'est pas évident si le test sert à protéger contre une violation ou fait partie de la logique requise.

<!-- commentaire nécessaire pour le bloc de code après la liste -->
    void f2(int* p) // indiquer que p ne doit pas être `nullptr`
    {
        assert(p);
        int x = *p;
    }

Cela ne coûterait que lorsqu'on active les assertions et fournirait aux compilateurs/analyseurs des informations utiles. Cela fonctionnerait encore mieux si/ quand C++ propose des contrats :

    void f3(int* p) // indiquer que p ne doit pas être `nullptr`
        [[expects: p]]
    {
        int x = *p;
    }

Ou bien, on pourrait utiliser `gsl::not_null` pour garantir que `p` n'est pas le `nullptr` :

    void f(not_null<int*> p)
    {
        int x = *p;
    }

Ces remèdes ne concernent que les `nullptr`. Rappelez‑vous qu'il existe d'autres façons d'obtenir un pointeur invalide.

##### Exemple

    void f(int* p)  // code ancien, n'utilise pas de propriétaire
    {
        delete p;
    }

    void g()        // code ancien : utilise `new` nu
    {
        auto q = new int{7};
        f(q);
        int x = *q; // MAUVAIS : déréférence d'un pointeur invalide
    }

##### Exemple

    void f()
    {
        vector<int> v(10);
        int* p = &v[5];
        v.push_back(99); // pourrait réallouer les éléments de v
        int x = *p; // MAUVAIS : déréférence d'un pointeur potentiellement invalide
    }

##### Application

Cette règle fait partie du [profil de sécurité de durée de vie](022-profile.md#ss-lifetime)

* Signaler un déréférencement d'un pointeur qui pointe vers un objet qui a quitté la portée.  
* Signaler un déréférencement d'un pointeur qui pourrait avoir été invalidé par une assignation à `nullptr`.  
* Signaler un déréférencement d'un pointeur qui pourrait avoir été invalidé par un `delete`.  
* Signaler un déréférencement d'un pointeur vers un élément de conteneur qui pourrait avoir été invalidé par une réallocation.

---

## ES.stmt : Instructions

Les instructions contrôlent le flux (à l'exception des appels de fonction et des lancers d'exception, qui sont des expressions).

### <a name="res-switch-if"></a>ES.70 : Préférer une instruction `switch` à une instruction `if` lorsqu'il y a un choix

##### Raison

* Lisibilité.  
* Efficacité : un `switch` compare contre des constantes et est généralement mieux optimisé qu'une série de tests dans une chaîne `if‑then‑else`.  
* Un `switch` permet certains contrôles heuristiques de cohérence. Par ex. toutes les valeurs d'une `enum` ont‑elles été couvertes ? Si non, y a‑t‑il un `default` ?

##### Exemple

    void use(int n)
    {
        switch (n) {   // bon
        case 0:
            // …
            break;
        case 7:
            // …
            break;
        default:
            // …
            break;
        }
    }

plutôt que :

    void use2(int n)
    {
        if (n == 0)   // mauvais : chaîne `if‑then‑else` comparant contre un ensemble de constantes
            // …
        else if (n == 7)
            // …
    }

##### Application

Signaler les chaînes `if‑then‑else` qui comparent contre des constantes uniquement.

### <a name="res-for-range"></a>ES.71 : Préférer une boucle `for‑range` à une boucle `for` lorsqu'il y a un choix

##### Raison

Lisibilité. Prévention d'erreurs. Efficacité.

##### Exemple

    for (gsl::index i = 0; i < v.size(); ++i)   // mauvais
        cout << v[i] << '\n';

    for (auto p = v.begin(); p != v.end(); ++p)   // mauvais
        cout << *p << '\n';

    for (auto& x : v)    // OK
        cout << x << '\n';

    for (gsl::index i = 1; i < v.size(); ++i) // touche deux éléments : ne peut pas être un `range‑for`
        cout << v[i] + v[i - 1] << '\n';

    for (gsl::index i = 0; i < v.size(); ++i) // possible effet de bord : ne peut pas être un `range‑for`
        cout << f(v, &v[i]) << '\n';

    for (gsl::index i = 0; i < v.size(); ++i) { // le corps modifie la variable de boucle : ne peut pas être un `range‑for`
        if (i % 2 != 0)
            cout << v[i] << '\n'; // sortie des éléments impairs
    }

Un humain ou un bon analyseur statique pourrait déterminer qu'il n'y a réellement aucun effet de bord sur `v` dans `f(v, &v[i])` afin que la boucle puisse être réécrite.

« Modifier la variable de boucle » dans le corps d'une boucle est généralement à éviter.

##### Note

Ne pas utiliser de copies coûteuses de la variable de boucle d'un `range‑for` :

    for (string s : vs) // ...

Mieux :

    for (string& s : vs) // ...

Encore mieux, si la variable de boucle n'est pas modifiée ou copiée :

    for (const string& s : vs) // ...

##### Application

Regarder les boucles ; si une boucle traditionnelle ne fait que parcourir chaque élément d'une séquence et qu'il n'y a pas d'effets de bord sur ce que fait la boucle avec les éléments, réécrire la boucle en `range‑for`.

### <a name="res-for-while"></a>ES.72 : Préférer une boucle `for` à une boucle `while` lorsqu'il y a une variable de boucle évidente

##### Raison

Lisibilité : la logique complète de la boucle est visible « au départ ». La portée de la variable de boucle peut être limitée.

##### Exemple

    for (gsl::index i = 0; i < vec.size(); i++) {
        // faire le travail
    }

##### Exemple, mauvais

    int i = 0;
    while (i < vec.size()) {
        // faire le travail
        i++;
    }

##### Application

???

### <a name="res-while-for"></a>ES.73 : Préférer une boucle `while` à une boucle `for` lorsqu'il n'y a pas de variable de boucle évidente

##### Raison

Lisibilité.

##### Exemple

    int events = 0;
    for (; wait_for_event(); ++events) {  // mauvais, confus
        // …
    }

La « boucle d'événement » est trompeuse parce que le compteur `events` n'a rien à voir avec la condition `wait_for_event()`.

Mieux :

    int events = 0;
    while (wait_for_event()) {      // meilleur
        ++events;
        // …
    }

##### Application

Signaler les actions dans les parties `for‑initializer` et `for‑increment` qui ne sont pas liées à la condition du `for`.

### <a name="res-for-init"></a>ES.74 : Préférer déclarer une variable de boucle dans la partie initialisation d'une instruction `for`

Voir [ES.6](010-expr.md#res-cond)

### <a name="res-do"></a>ES.75 : Éviter les instructions `do`

##### Raison

Lisibilité, éviter les erreurs. La condition de terminaison est à la fin (où elle peut être négligée) et la condition n'est pas vérifiée la première fois.

##### Exemple

    int x;
    do {
        cin >> x;
        // …
    } while (x < 0);

##### Note

Oui, il existe des exemples légitimes où une instruction `do` est claire, mais il y a aussi de nombreux bugs.

##### Application

Signaler les instructions `do`.

### <a name="res-goto"></a>ES.76 : Éviter `goto`

##### Raison

Lisibilité, éviter les erreurs. Il existe de meilleures structures de contrôle pour les humains ; `goto` est destiné au code généré par machine.

##### Exception

Sortir d'une boucle imbriquée. Dans ce cas, sautez toujours en avant.

    for (int i = 0; i < imax; ++i)
        for (int j = 0; j < jmax; ++j) {
            if (a[i][j] > elem_max) goto finished;
            // …
        }
    finished:
    // ...

##### Exemple, mauvais

Il y a pas mal d'utilisation du « idiome C goto‑exit » :

    void f()
    {
        // …
            goto exit;
        // …
            goto exit;
        // …
    exit:
        // … code de nettoyage commun …
    }

C'est une simulation ad‑hoc des destructeurs. Déclarez vos ressources avec des gestionnaires qui nettoient automatiquement.  
Si, pour une raison quelconque, vous ne pouvez pas gérer tout le nettoyage avec des destructeurs pour les variables utilisées, envisagez `gsl::finally()` comme alternative plus propre et plus fiable au `goto exit`.

##### Application

* Signaler `goto`. Mieux encore, signaler tous les `goto` qui ne sautent pas d'une boucle imbriquée à l'instruction immédiatement après la fin de la boucle.

### <a name="res-continue"></a>ES.77 : Minimiser l'usage de `break` et `continue` dans les boucles

##### Raison

Dans une boucle non triviale, il est facile d'oublier un `break` ou un `continue`.

Un `break` dans une boucle a une signification très différente d'un `break` dans une instruction `switch` (et vous pouvez avoir un `switch` dans une boucle et une boucle dans un `case` de `switch`).

##### Alternative

Souvent, une boucle qui nécessite un `break` est un bon candidat pour une fonction (algorithme), auquel cas le `break` devient un `return`.

    // Code original : `break` dans la boucle
    void use1()
    {
        std::vector<T> vec = {/* initialisé avec certaines valeurs */};
        T value;
        for (const T item : vec) {
            if (/* condition */) {
                value = item;
                break;
            }
        }
        /* puis faire quelque chose avec value */
    }

    // MIEUX : créer une fonction et `return` à l'intérieur de la boucle
    T search(const std::vector<T> &vec)
    {
        for (const T &item : vec) {
            if (/* condition */) return item;
        }
        return T(); // valeur par défaut
    }

    void use2()
    {
        std::vector<T> vec = {/* initialisé avec certaines valeurs */};
        T value = search(vec);
        /* puis faire quelque chose avec value */
    }

Souvent, une boucle qui utilise `continue` peut être réécrite de façon tout aussi claire avec un `if` :

    for (int item : vec) {  // MAUVAIS
        if (item%2 == 0) continue;
        if (item == 5) continue;
        if (item > 10) continue;
        /* faire quelque chose avec item */
    }

    for (int item : vec) {  // BON
        if (item%2 != 0 && item != 5 && item <= 10) {
            /* faire quelque chose avec item */
        }
    }

##### Note

Si vous devez vraiment sortir d'une boucle, un `break` est généralement meilleur qu'une modification de la variable de boucle (`skip`), ou qu'un `goto` :

##### Application

???

### <a name="res-break"></a>ES.78 : Ne pas compter sur le « fall‑through » implicite dans les `switch`

##### Raison

Toujours terminer un `case` non vide par un `break`. Oublier accidentellement un `break` est une erreur assez courante. Un `fall‑through` délibéré peut être un risque de maintenance et doit être rare et explicite.

##### Exemple

    switch (eventType) {
    case Information:
        update_status_bar();
        break;
    case Warning:
        write_event_log();
        // Mauvais – fall‑through implicite
    case Error:
        display_error_window();
        break;
    }

Des étiquettes `case` multiples pour une même instruction sont OK :

    switch (x) {
    case 'a':
    case 'b':
    case 'f':
        do_something(x);
        break;
    }

Les instructions `return` dans un `case` sont aussi OK :

    switch (x) {
    case 'a':
        return 1;
    case 'b':
        return 2;
    case 'c':
        return 3;
    }

##### Exceptions

Dans de rares cas où le fall‑through est jugé approprié, soyez explicite et utilisez l'annotation `[[fallthrough]]` :

    switch (eventType) {
    case Information:
        update_status_bar();
        break;
    case Warning:
        write_event_log();
        [[fallthrough]];
    case Error:
        display_error_window();
        break;
    }

##### Note

##### Application

Signaler tous les fall‑through implicites depuis des `case` non vides.

### <a name="res-default"></a>ES.79 : Utiliser `default` pour gérer les cas courants (seulement)

##### Raison

Clarté du code. Meilleures opportunités de détection d'erreurs.

##### Exemple

    enum E { a, b, c, d };

    void f1(E x)
    {
        switch (x) {
        case a:
            do_something();
            break;
        case b:
            do_something_else();
            break;
        default:
            take_the_default_action();
            break;
        }
    }

Ici il est clair qu'il y a une action par défaut et que les cas `a` et `b` sont spéciaux.

##### Exemple

Mais que se passe‑t‑il s'il n'y a pas d'action par défaut et que vous ne voulez gérer que des cas spécifiques ? Dans ce cas, ajoutez un `default` vide ou sinon il est impossible de savoir si vous avez oublié un cas :

    void f2(E x)
    {
        switch (x) {
        case a:
            do_something();
            break;
        case b:
            do_something_else();
            break;
        default:
            // ne rien faire pour les autres cas
            break;
        }
    }

Si vous omettez le `default`, un mainteneur et/ou un compilateur pourraient raisonnablement supposer que vous aviez l'intention de gérer tous les cas :

    void f2(E x)
    {
        switch (x) {
        case a:
            do_something();
            break;
        case b:
        case c:
            do_something_else();
            break;
        }
    }

Avez‑vous oublié le cas `d` ou l'avez‑vous délibérément omis ? Oublier un cas se produit souvent lorsqu'un nouveau cas est ajouté à une énumération et que la personne qui le fait oublie de l'ajouter à chaque `switch` sur les énumérateurs.

##### Application

Signaler les `switch` sur une énumération qui ne gèrent pas tous les énumérateurs et qui n'ont pas de `default`. Cela peut générer trop de faux positifs dans certains projets ; si c'est le cas, ne signaler que les `switch` qui gèrent la plupart mais pas tous les cas (c'était la stratégie du tout premier compilateur C++).

### <a name="res-noname"></a>ES.84 : Ne pas essayer de déclarer une variable locale sans nom

##### Raison

Il n'existe pas de tel concept. Ce qui ressemble à une variable sans nom pour un humain est, pour le compilateur, une instruction constituée d'un temporaire qui sort immédiatement de la portée.

##### Exemple, mauvais

    void f()
    {
        lock_guard<mutex>{mx};   // Mauvais
        // …
    }

Cela déclare un objet `lock_guard` anonyme qui sort immédiatement de la portée au point du point‑virgule. Ce n'est pas rare. En particulier, cet exemple peut entraîner des conditions de concurrence difficiles à repérer.

##### Note

Les arguments de fonction anonymes sont acceptables.

##### Application

Signaler les instructions qui ne sont qu'un temporaire.

### <a name="res-empty"></a>ES.85 : Rendre les instructions vides visibles

##### Raison

Lisibilité.

##### Exemple

    for (i = 0; i < max; ++i);   // MAUVAIS : l'instruction vide est facilement négligée
    v[i] = f(v[i]);

    for (auto x : v) {           // meilleur
        // rien
    }
    v[i] = f(v[i]);

##### Application

Signaler les instructions vides qui ne sont pas des blocs et ne contiennent pas de commentaires.

### <a name="res-loop-counter"></a>ES.86 : Éviter de modifier les variables de contrôle de boucle à l'intérieur du corps des boucles `for` classiques

##### Raison

Le contrôle de boucle en amont doit permettre de raisonner correctement sur ce qui se passe à l'intérieur de la boucle. Modifier les compteurs de boucle à la fois dans l'expression d'itération et dans le corps de la boucle est une source perpétuelle de surprises et de bugs.

##### Exemple

    for (int i = 0; i < 10; ++i) {
        // aucune mise à jour de i – ok
    }

    for (int i = 0; i < 10; ++i) {
        //
        if (/* quelque chose */) ++i; // MAUVAIS
        //
    }

    bool skip = false;
    for (int i = 0; i < 10; ++i) {
        if (skip) { skip = false; continue; }
        //
        if (/* quelque chose */) skip = true;  // Mieux : deux variables pour deux concepts.
        //
    }

##### Application

Signaler les variables qui sont potentiellement mises à jour (utilisation non `const`) à la fois dans l'expression d'itération du contrôle de boucle et dans le corps de la boucle.

### <a name="res-if"></a>ES.87 : Ne pas ajouter de `==` ou `!=` redondants aux conditions

##### Raison

Cela évite la verbosité et élimine certaines opportunités d'erreurs. Aide à rendre le style cohérent et conventionnel.

##### Exemple

Par définition, une condition dans une instruction `if`, `while` ou `for` sélectionne entre `true` et `false`. Une valeur numérique est comparée à `0` et une valeur pointeur à `nullptr`.

    // Tous ces signifient « si p n'est pas `nullptr` »
    if (p) { ... }            // bon
    if (p != 0) { ... }       // redondant !=0, mauvais : ne pas utiliser 0 pour les pointeurs
    if (p != nullptr) { ... } // redondant !=nullptr, pas recommandé

Souvent, `if (p)` se lit comme « si `p` est valide », ce qui exprime directement l'intention du programmeur, alors que `if (p != nullptr)` serait une solution détournée.

##### Exemple

Ce règle est particulièrement utile lorsqu'une déclaration est utilisée comme condition :

    if (auto pc = dynamic_cast<Circle*>(ps)) { ... } // exécuter si `ps` pointe vers un `Circle`, bon

    if (auto pc = dynamic_cast<Circle*>(ps); pc != nullptr) { ... } // non recommandé

##### Exemple

Notez que les conversions implicites en booléen sont appliquées dans les conditions. Par ex. :

    for (string s; cin >> s; ) v.push_back(s);

Cela invoque `operator bool()` de `istream`.

##### Note

La comparaison explicite d'un entier à `0` n'est généralement pas redondante. La raison est que (contrairement aux pointeurs et aux booléens) un entier possède souvent plus de valeurs raisonnables. De plus, `0` (zéro) est souvent utilisé pour indiquer le succès. Ainsi, il vaut mieux être précis sur la comparaison.

    void f(int i)
    {
        if (i)            // suspect
        // …
        if (i == success) // peut être meilleur
        // …
    }

Rappelez‑vous toujours qu'un entier peut avoir plus de deux valeurs.

##### Exemple, mauvais

Il a été noté que

    if(strcmp(p1, p2)) { ... }   // les deux chaînes C‑style sont‑elles égales ? (erreur !)

est une erreur fréquente chez les débutants. Si vous utilisez des chaînes C, vous devez bien connaître les fonctions `<cstring>`. Être verbeux et écrire :

    if(strcmp(p1, p2) != 0) { ... }   // les deux chaînes C‑style sont‑elles égales ? (erreur !)

ne résoudrait pas le problème en soi.

##### Note

La condition opposée s'exprime le plus simplement avec une négation :

    // Tous ces signifient « si p est `nullptr` »
    if (!p) { ... }           // bon
    if (p == 0) { ... }       // redondant == 0, mauvais : ne pas utiliser 0 pour les pointeurs
    if (p == nullptr) { ... } // redondant == nullptr, pas recommandé

##### Application

Facile : simplement vérifier la présence de `!=` et `==` redondants dans les conditions.

---

## <a name="ss-numbers"></a>Arithmétique

### <a name="res-mix"></a>ES.100 : Ne pas mélanger arithmétique signée et non signée

##### Raison

Éviter les résultats erronés.

##### Exemple

    int x = -3;
    unsigned int y = 7;

    cout << x - y << '\n';  // résultat non signé, possiblement 4294967286
    cout << x + y << '\n';  // résultat non signé : 4
    cout << x * y << '\n';  // résultat non signé, possiblement 4294967275

Il est plus difficile de repérer le problème dans des exemples plus réalistes.

##### Note

Malheureusement, C++ utilise des entiers signés pour les indices de tableau et la bibliothèque standard utilise des entiers non signés pour les indices de conteneur. Cela empêche la cohérence. Utilisez `gsl::index` pour les indices ; [voir ES.107](010-expr.md#res-subscripts).

##### Application

* Les compilateurs savent déjà et parfois avertissent.  
* (Pour éviter le bruit) Ne pas signaler sur une comparaison signée/non signée où l'un des arguments est `sizeof` ou un appel à `.size()` du conteneur et l'autre est `ptrdiff_t`.

### <a name="res-unsigned"></a>ES.101 : Utiliser des types non signés pour la manipulation de bits

##### Raison

Les types non signés supportent la manipulation de bits sans les surprises du bit de signe.

##### Exemple

    unsigned char x = 0b1010'1010;
    unsigned char y = ~x;   // y == 0b0101'0101;

##### Note

Les types non signés peuvent aussi être utiles pour l'arithmétique modulaire. Cependant, si vous voulez de l'arithmétique modulaire, ajoutez des commentaires indiquant la dépendance au comportement de débordement, car ce code peut surprendre de nombreux programmeurs.

##### Application

* Pratiquement impossible en général à cause de l'utilisation des indices non signés dans la bibliothèque standard.  
* ???

### <a name="res-signed"></a>ES.102 : Utiliser des types signés pour l'arithmétique

##### Raison

Parce que la plupart des calculs sont supposés être signés ; `x - y` renvoie un nombre négatif lorsque `y > x`, sauf dans les rares cas où vous voulez réellement de l'arithmétique modulaire.

##### Exemple

L'arithmétique non signée peut produire des résultats surprenants si vous ne vous y attendez pas. C'est encore plus vrai pour l'arithmétique signée/non signée mélangée.

    template<typename T, typename T2>
    T subtract(T x, T2 y)
    {
        return x - y;
    }

    void test()
    {
        int s = 5;
        unsigned int us = 5;
        cout << subtract(s, 7) << '\n';       // -2
        cout << subtract(us, 7u) << '\n';     // 4294967294
        cout << subtract(s, 7u) << '\n';      // -2
        cout << subtract(us, 7) << '\n';      // 4294967294
        cout << subtract(s, us + 2) << '\n';  // -2
        cout << subtract(us, s + 2) << '\n';  // 4294967294
    }

Nous avons été très explicites sur ce qui se passe, mais si vous aviez vu `us - (s + 2)` ou `s += 2; …; us - s`, auriez‑vous deviné que le résultat serait `4294967294` ?

##### Exception

Utilisez des types non signés si vous voulez réellement de l'arithmétique modulaire – ajoutez des commentaires indiquant la dépendance au comportement de débordement, car ce code peut surprendre de nombreux programmeurs.

##### Exemple

La bibliothèque standard utilise des types non signés pour les indices de conteneur. Le tableau intégré utilise des types signés pour les indices. Cela rend inévitable les surprises (et les bugs).

    int a[10];
    for (int i = 0; i < 10; ++i) a[i] = i;
    vector<int> v(10);
    // compare signed à unsigned ; certains compilateurs avertissent, mais nous ne devrions pas
    for (gsl::index i = 0; i < v.size(); ++i) v[i] = i;

    int a2[-2];         // erreur : taille négative

    // OK, mais le nombre d'entiers (4294967294) est tellement grand qu'on devrait lever une exception
    vector<int> v2(-2);

 Utilisez `gsl::index` pour les indices ; [voir ES.107](010-expr.md#res-subscripts).

##### Application

* Signaler les mélanges d'arithmétique signée et non signée.  
* Signaler les résultats d'arithmétique non signée assignés ou affichés comme signés.  
* Signaler les littéraux négatifs (ex. `-2`) utilisés comme indices de conteneur.  
* (Pour éviter le bruit) Ne pas signaler sur une comparaison signée/non signée où l'un des arguments est `sizeof` ou un appel à `.size()` du conteneur et l'autre est `ptrdiff_t`.

### <a name="res-overflow"></a>ES.103 : Ne pas dépasser la capacité (overflow)

##### Raison

Un overflow rend généralement votre algorithme numérique dénué de sens. Incrémenter une valeur au‑delà d'une valeur maximale peut entraîner une corruption mémoire et un comportement indéfini.

##### Exemple, mauvais

    int a[10];
    a[10] = 7;   // mauvais, dépassement de tableau

    for (int n = 0; n <= 10; ++n)
        a[n] = 9;   // mauvais, dépassement de tableau

##### Exemple, mauvais

    int n = numeric_limits<int>::max();
    int m = n + 1;   // mauvais, overflow numérique

##### Exemple, mauvais

    int area(int h, int w) { return h * w; }

    auto a = area(10'000'000, 100'000'000);   // mauvais, overflow numérique

##### Exception

Utilisez des types non signés si vous voulez réellement de l'arithmétique modulaire.

**Alternative** : Pour les applications critiques qui peuvent se permettre un certain surcoût, utilisez un entier ou un type à virgule flottante avec vérification de limites.

##### Application

???

### <a name="res-underflow"></a>ES.104 : Ne pas sous‑déborder (underflow)

##### Raison

Décrémenter une valeur au‑delà d'une valeur minimale peut entraîner une corruption mémoire et un comportement indéfini.

##### Exemple, mauvais

    int a[10];
    a[-2] = 7;   // mauvais

    int n = 101;
    while (n--)
        a[n - 1] = 9;   // mauvais (deux fois)

##### Exception

Utilisez des types non signés si vous voulez réellement de l'arithmétique modulaire.

##### Application

???

### <a name="res-zero"></a>ES.105 : Ne pas diviser par zéro entier

##### Raison

Le résultat est indéfini et probablement un plantage.

##### Note

Cela s'applique aussi à l'opérateur `%`.

##### Exemple, mauvais

    int divide(int a, int b)
    {
        // MAUVAIS, devrait être vérifié (par ex. dans une précondition)
        return a / b;
    }

##### Exemple, bon

    int divide(int a, int b)
    {
        // bon, gérer via précondition (et remplacer par les contrats quand C++ les aura)
        Expects(b != 0);
        return a / b;
    }

    double divide(double a, double b)
    {
        // bon, gérer via double
        return a / b;
    }

**Alternative** : Pour les applications critiques qui peuvent se permettre un certain surcoût, utilisez un entier ou un type à virgule flottante avec vérification de limites.

##### Application

* Signaler la division par une valeur entière qui pourrait être zéro.

### <a name="res-nonnegative"></a>ES.106 : Ne pas essayer d'éviter les valeurs négatives en utilisant `unsigned`

##### Raison

Choisir `unsigned` implique de nombreux changements de comportement des entiers, y compris l'arithmétique modulaire, supprime les avertissements liés aux overflow, et ouvre la porte à des erreurs liées aux mélanges signés/non signés. Utiliser `unsigned` n'élimine pas réellement la possibilité de valeurs négatives.

##### Exemple

    unsigned int u1 = -2;   // valide : la valeur de u1 est 4294967294
    int i1 = -2;
    unsigned int u2 = i1;   // valide : la valeur de u2 est 4294967294
    int i2 = u2;            // valide : la valeur de i2 est -2

Ces problèmes avec de telles constructions parfaitement légales sont difficiles à repérer dans le code réel et sont à l'origine de nombreuses erreurs réelles. Considérez :

    unsigned area(unsigned height, unsigned width) { return height*width; } // [voir aussi](005-interfaces.md#ri-expects)
    // …
    int height;
    cin >> height;
    auto a = area(height, 2);   // si l'entrée est -2, a devient 4294967292

Rappelez‑vous que `-1` assigné à un `unsigned int` devient le plus grand `unsigned int`. De plus, comme l'arithmétique non signée est modulaire, la multiplication n'a pas overflow, elle a simplement « wrap‑around ».

##### Exemple

    unsigned max = 100000;    // « typo » accidentelle, je voulais dire 10'000
    unsigned short x = 100;
    while (x < max) x += 100; // boucle infinie

Si `x` était un `short` signé, nous pourrions avertir d'un comportement indéfini lors de l'overflow.

##### Alternatives

* Utiliser des entiers signés et vérifier `x >= 0`.  
* Utiliser un type entier positif.  
* Utiliser un type entier de sous‑intervalle.  
* `Assert(-1 < x)`

Par ex.

    struct Positive {
        int val;
        Positive(int x) :val{x} { Assert(0 < x); }
        operator int() { return val; }
    };

    int f(Positive arg) { return arg; }

    int r1 = f(2);
    int r2 = f(-2);  // lance

##### Note

???

##### Application

Voir les applications de ES.100.

### <a name="res-subscripts"></a>ES.107 : Ne pas utiliser `unsigned` pour les indices, préférer `gsl::index`

##### Raison

Éviter la confusion entre signés et non signés. Permettre de meilleures optimisations. Permettre une meilleure détection d'erreurs. Éviter les problèmes avec `auto` et `int`.

##### Exemple, mauvais

    vector<int> vec = /*…*/;

    for (int i = 0; i < vec.size(); i += 2)                    // peut ne pas être assez grand
        cout << vec[i] << '\n';
    for (unsigned i = 0; i < vec.size(); i += 2)               // risque de wrap‑around
        cout << vec[i] << '\n';
    for (auto i = 0; i < vec.size(); i += 2)                   // peut ne pas être assez grand
        cout << vec[i] << '\n';
    for (vector<int>::size_type i = 0; i < vec.size(); i += 2) // verbeux
        cout << vec[i] << '\n';
    for (auto i = vec.size()-1; i >= 0; i -= 2)                // bug
        cout << vec[i] << '\n';
    for (int i = vec.size()-1; i >= 0; i -= 2)                 // peut ne pas être assez grand
        cout << vec[i] << '\n';

##### Exemple, bon

    vector<int> vec = /*…*/;

    for (gsl::index i = 0; i < vec.size(); i += 2)             // ok
        cout << vec[i] << '\n';
    for (gsl::index i = vec.size()-1; i >= 0; i -= 2)          // ok
        cout << vec[i] << '\n';

##### Note

Le tableau intégré utilise des indices signés. Les conteneurs de la bibliothèque standard utilisent des indices non signés. Ainsi, aucune solution parfaite et totalement compatible n'est possible (à moins que les conteneurs de la bibliothèque standard changent un jour pour utiliser des indices signés).  
Étant donné les problèmes connus avec les non signés et les mélanges signés/non signés, il vaut mieux s'en tenir à des entiers (signés) de taille suffisante, garantis par `gsl::index`.

##### Exemple

    template<typename T>
    struct My_container {
    public:
        // …
        T& operator[](gsl::index i);    // pas `unsigned`
        // …
    };

##### Exemple

    ??? démontrer l'amélioration du code généré et le potentiel de détection d'erreurs ???

##### Alternatives

Alternatives pour les utilisateurs :

* Utiliser les algorithmes  
* Utiliser `range‑for`  
* Utiliser les itérateurs/pointeurs

##### Application

* Très difficile tant que les conteneurs de la bibliothèque standard restent incohérents.  
* (Pour éviter le bruit) Ne pas signaler sur une comparaison signée/non signée où l'un des arguments est `sizeof` ou un appel à `.size()` du conteneur et l'autre est `ptrdiff_t`.

---
