# <a name="s-expr"></a>ES : Expressions et énoncés

Les expressions et les énoncés constituent la manière la plus basse et la plus directe d'exprimer des actions et des calculs. Les déclarations dans des portées locales sont des énoncés.

Pour les règles de nommage, de commentaires et d'indentation, voir [NL : Nommage et mise en page](024-naming.md).

Règles générales :

* [ES.1 : Privilégier la bibliothèque standard par rapport à d'autres bibliothèques et au « code fait main »](010-expr.md#res-lib)
* [ES.2 : Privilégier des abstractions adaptées à l'utilisation directe des fonctionnalités du langage](010-expr.md#res-abstr)
* [ES.3 : Ne pas se répéter, éviter le code redondant](010-expr.md#res-dry)

Règles de déclaration :

* [ES.5 : Garder les portées petites](010-expr.md#res-scope)
* [ES.6 : Déclarer les noms dans les initialiseurs et les conditions des énoncés for pour limiter la portée](010-expr.md#res-cond)
* [ES.7 : Garder les noms courants et locaux courts, et garder les noms peu courants et non locaux plus longs](010-expr.md#res-name-length)
* [ES.8 : Éviter les noms qui se ressemblent](010-expr.md#res-name-similar)
* [ES.9 : Éviter les noms en `MAJUSCULES`](010-expr.md#res-not-caps)
* [ES.10 : Déclarer un seul nom (à la fois) par déclaration](010-expr.md#res-name-one)
* [ES.11 : Utiliser `auto` pour éviter les répétitions redondantes de noms de types](010-expr.md#res-auto)
* [ES.12 : Ne pas réutiliser des noms dans des portées imbriquées](010-expr.md#res-reuse)
* [ES.20 : Toujours initialiser un objet](010-expr.md#res-always)
* [ES.21 : Ne pas introduire une variable (ou une constante) avant d'en avoir besoin](010-expr.md#res-introduce)
* [ES.22 : Ne pas déclarer une variable tant qu'on n'a pas de valeur pour l'initialiser](010-expr.md#res-init)
* [ES.23 : Privilégier la syntaxe d'initialisation par `{}`}](010-expr.md#res-list)
* [ES.24 : Utiliser un `unique_ptr<T>` pour conserver des pointeurs](010-expr.md#res-unique)
* [ES.25 : Déclarer un objet `const` ou `constexpr` sauf si vous souhaitez modifier sa valeur plus tard](010-expr.md#res-const)
* [ES.26 : Ne pas utiliser une variable pour deux finalités sans rapport](010-expr.md#res-recycle)
* [ES.27 : Utiliser `std::array` ou `stack_array` pour les tableaux sur la pile](010-expr.md#res-stack)
* [ES.28 : Utiliser des lambda pour les initialisations complexes, en particulier de variables `const`](010-expr.md#res-lambda-init)
* [ES.30 : Ne pas utiliser de macros pour la manipulation du texte de programme](010-expr.md#res-macros)
* [ES.31 : Ne pas utiliser de macros pour les constantes ou les « fonctions »](010-expr.md010-expr.md#res-macros2)
* [ES.32 : Utiliser `MAJUSCULES` pour tous les noms de macros](010-expr.md#res-all_caps)
* [ES.33 : Si vous devez utiliser des macros, donnez-leur des noms uniques](010-expr.md010-expr.md#res-macros3)
* [ES.34 : Ne pas définir de fonction variable (au sens C)](010-expr.md#res-ellipses)

Règles d'expression :

* [ES.40 : Éviter les expressions compliquées](010-expr.md#res-complicated)
* [ES.41 : En cas de doute sur la priorité des opérateurs, ajouter des parenthèses](010-expr.md#res-parens)
* [ES.42 : Garder l'utilisation des pointeurs simple et directe](010-expr.md#res-ptr)
* [ES.43 : Éviter les expressions dont l'ordre d'évaluation est indéfini](010-expr.md#res-order)
* [ES.44 : Ne pas dépendre de l'ordre d'évaluation des arguments de fonction](010-expr.md010-expr.md#res-order-fct)
* [ES.45 : Éviter les « constantes magiques » ; utiliser des constantes symboliques](010-expr.md#res-magic)
* [ES.46 : Éviter les conversions rétrécissantes](010-expr.md#res-narrowing)
* [ES.47 : Utiliser `nullptr` plutôt que `0` ou `NULL`](010-expr.md#res-nullptr)
* [ES.48 : Éviter les transpositions (casts)](010-expr.md#res-casts)
* [ES.49 : Si vous devez utiliser une transposition, utilisez une transposition nommée](010-expr.md010-expr.md#res-casts-named)
* [ES.50 : Ne pas éliminer `const` par transposition](010-expr.md010-expr.md#res-casts-const)
* [ES.55 : Éviter le besoin de vérification de plage](010-expr.md#res-range-checking)
* [ES.56 : Écrire `std::move()` seulement quand vous avez besoin de déplacer explicitement un objet vers une autre portée](010-expr.md#res-move)
* [ES.60 : Éviter `new` et `delete` en dehors des fonctions de gestion de ressources](010-expr.md#res-new)
* [ES.61 : Supprimer les tableaux avec `delete[]` et les non-tableaux avec `delete`](010-expr.md#res-del)
* [ES.62 : Ne pas comparer des pointeurs vers des tableaux différents](010-expr.md#res-arr2)
* [ES.63 : Ne pas effectuer de tranchage (slicing)](010-expr.md#res-slice)
* [ES.64 : Utiliser la notation `T{e}` pour la construction](010-expr.md010-expr.md#res-construct)
* [ES.65 : Ne pas déréférencer un pointeur invalide](010-expr.md#res-deref)

Règles d'énoncé :

* [ES.70 : Privilégier un énoncé `switch` à un énoncé `if` quand c'est possible](010-expr.md#res-switch-if)
* [ES.71 : Privilégier un énoncé `for`-par-plage à un énoncé `for` quand c'est possible](010-expr.md#res-for-range)
* [ES.72 : Privilégier un énoncé `for` à un énoncé `while` quand il y a une variable de boucle évidente](010-expr.md#res-for-while)
* [ES.73 : Privilégier un énoncé `while` à un énoncé `for` quand il n'y a pas de variable de boucle évidente](010-expr.md#res-while-for)
* [ES.74 : Privilégier la déclaration d'une variable de boucle dans la partie initialiseur d'un énoncé `for`](010-expr.md#res-for-init)
* [ES.75 : Éviter les énoncés `do`](010-expr.md#res-do)
* [ES.76 : Éviter `goto`](010-expr.md#res-goto)
* [ES.77 : Minimiser l'utilisation de `break` et `continue` dans les boucles](010-expr.md#res-continue)
* [ES.78 : Ne pas compter sur le découlement implicite dans les énoncés `switch`](010-expr.md#res-break)
* [ES.79 : Utiliser `default` pour gérer les cas courants (uniquement)](010-expr.md#res-default)
* [ES.84 : Ne pas essayer de déclarer une variable locale sans nom](010-expr.md#res-noname)
* [ES.85 : Rendre les énoncés vides visibles](010-expr.md#res-empty)
* [ES.86 : Éviter de modifier les variables de contrôle de boucle dans le corps de boucles `for` simples](010-expr.md#res-loop-counter)
* [ES.87 : Ne pas ajouter de `==` ou `!=` redondants dans les conditions](010-expr.md#res-if)

Règles arithmétiques :

* [ES.100 : Ne pas mélanger l'arithmétique signée et non signée](010-expr.md#res-mix)
* [ES.101 : Utiliser des types non signés pour la manipulation de bits](010-expr.md#res-unsigned)
* [ES.102 : Utiliser des types signés pour l'arithmétique](010-expr.md#res-signed)
* [ES.103 : Ne pas dépasser (débordement)](010-expr.md#res-overflow)
* [ES.104 : Ne pas sous-dépasser](010-expr.md#res-underflow)
* [ES.105 : Ne pas diviser par zéro (entier)](010-expr.md#res-zero)
* [ES.106 : Ne pas essayer d'éviter les valeurs négatives en utilisant `unsigned`](010-expr.md#res-nonnegative)
* [ES.107 : Ne pas utiliser `unsigned` pour les indices, privilégier `gsl::index`](010-expr.md#res-subscripts)

### <a name="res-lib"></a>ES.1 : Privilégier la bibliothèque standard par rapport à d'autres bibliothèques et au « code fait main »

##### Justification

Un code utilisant une bibliothèque peut être beaucoup plus facile à écrire qu'un code travaillant directement avec les fonctionnalités du langage, beaucoup plus court, tend à être à un niveau d'abstraction plus élevé, et le code de la bibliothèque est supposé déjà testé.
La bibliothèque standard ISO C++ fait partie des bibliothèques les plus connues et les mieux testées.
Elle est disponible dans le cadre de toutes les implémentations C++.

##### Exemple

    auto sum = accumulate(begin(a), end(a), 0.0);   // bon

Une version par plage d'`accumulate` serait encore meilleure :

    auto sum = accumulate(v, 0.0); // meilleur

mais ne codez pas à la main un algorithme bien connu :

    int max = v.size();   // mauvais : verbeux, but non exprimé
    double sum = 0.0;
    for (int i = 0; i < max; ++i)
        sum = sum + v[i];

##### Exception

De grandes parties de la bibliothèque standard reposent sur l'allocation dynamique (mémoire libre). Ces parties, notamment les conteneurs mais pas les algorithmes, ne conviennent pas à certaines applications temps réel durcies et embarquées. Dans de tels cas, envisagez de fournir/utiliser des facilités similaires, par exemple un conteneur de style bibliothèque standard implémenté à l'aide d'un allocateur par pool.

##### Application

Pas facile. ??? Chercher des boucles embrouillées, des boucles imbriquées, des fonctions longues, l'absence d'appels de fonction, le manque d'utilisation de types intégrés. Complexité cyclomatique ?

### <a name="res-abstr"></a>ES.2 : Privilégier des abstractions adaptées à l'utilisation directe des fonctionnalités du langage

##### Justification

Une « abstraction adaptée » (par exemple une bibliothèque ou une classe) est plus proche des concepts de l'application que le langage nu, conduit à un code plus court et plus clair, et est susceptible d'être mieux testée.

##### Exemple

    vector<string> read1(istream& is)   // bon
    {
        vector<string> res;
        for (string s; is >> s;)
            res.push_back(s);
        return res;
    }

L'équivalent plus traditionnel et de plus bas niveau est plus long, plus embrouillé, plus difficile à obtenir correctement, et probablement plus lent :

    char** read2(istream& is, int maxelem, int maxstring, int* nread)   // mauvais : verbeux et incomplet
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

Dès que les vérifications de débordement et la gestion des erreurs ont été ajoutées, ce code devient assez embrouillé, et il y a le problème de se souvenir de `delete` le pointeur retourné et les chaînes de caractères de style C que le tableau contient.

##### Application

Pas facile. ??? Chercher des boucles embrouillées, des boucles imbriquées, des fonctions longues, l'absence d'appels de fonction, le manque d'utilisation de types intégrés. Complexité cyclomatique ?

### <a name="res-dry"></a>ES.3 : Ne pas se répéter, éviter le code redondant

Un code dupliqué ou autrement redondant obscurcit l'intention, rend la logique plus difficile à comprendre et complique la maintenance, entre autres problèmes. Il naît souvent de la programmation par copier-coller.

Utiliser les algorithmes standard quand c'est approprié, au lieu d'écrire une implémentation maison.

**Voir aussi** : [SL.1](018-stdlib.md#rsl-lib), [ES.11](010-expr.md#res-auto)

##### Exemple

    void func(bool flag)    // Mauvais, code dupliqué.
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

    void func(bool flag)    // Meilleur, pas de code dupliqué.
    {
        x();

        if (flag)
            y();
        else
            z();
    }


##### Application

* Utiliser un analyseur statique. Il détectera au moins certaines constructions redondantes.
* Revue de code

## ES.dcl : Déclarations

Une déclaration est un énoncé. Une déclaration introduit un nom dans une portée et peut provoquer la construction d'un objet nommé.

### <a name="res-scope"></a>ES.5 : Garder les portées petites

##### Justification

Lisibilité. Minimiser la rétention de ressources. Éviter une mauvaise utilisation accidentelle d'une valeur.

**Formulation alternative** : Ne pas déclarer un nom dans une portée inutilement grande.

##### Exemple

    void use()
    {
        int i;    // mauvais : i est inutilement accessible après la boucle
        for (i = 0; i < 20; ++i) { /* ... */ }
        // pas d'utilisation prévue de i ici
        for (int i = 0; i < 20; ++i) { /* ... */ }  // bon : i est local à la boucle for

        if (auto pc = dynamic_cast<Circle*>(ps)) {  // bon : pc est local à l'énoncé if
            // ... gérer Circle ...
        }
        else {
            // ... gérer l'erreur ...
        }
    }

##### Exemple, mauvais

    void use(const string& name)
    {
        string fn = name + ".txt";
        ifstream is {fn};
        Record r;
        is >> r;
        // ... 200 lignes de code sans utilisation prévue de fn ou is ...
    }

Cette fonction est, à bien des égards, trop longue de toute façon, mais le point est que les ressources utilisées par `fn` et le descripteur de fichier détenu par `is`
sont conservées bien plus longtemps que nécessaire et qu'une utilisation inattendue de `is` et `fn` pourrait se produire plus tard dans la fonction.
Dans ce cas, il serait peut-être judicieux de factoriser la lecture :

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
        // ... 200 lignes de code ...
    }

##### Application

* Signaler une variable de boucle déclarée en dehors d'une boucle et non utilisée après la boucle
* Signaler lorsque des ressources coûteuses, telles que des descripteurs de fichiers et des verrous, ne sont pas utilisées pendant N lignes (pour un N approprié)

### <a name="res-cond"></a>ES.6 : Déclarer les noms dans les initialiseurs et les conditions des énoncés for pour limiter la portée

##### Justification

Lisibilité.
Limiter la visibilité de la variable de boucle à la portée de la boucle.
Éviter d'utiliser la variable de boucle à d'autres fins après la boucle.
Minimiser la rétention de ressources.

##### Exemple

    void use()
    {
        for (string s; cin >> s;)
            v.push_back(s);

        for (int i = 0; i < 20; ++i) {   // bon : i est local à la boucle for
            // ...
        }

        if (auto pc = dynamic_cast<Circle*>(ps)) {   // bon : pc est local à l'énoncé if
            // ... gérer Circle ...
        }
        else {
            // ... gérer l'erreur ...
        }
    }

##### Exemple, à ne pas faire

    int j;                            // MAUVAIS : j est visible en dehors de la boucle
    for (j = 0; j < 100; ++j) {
        // ...
    }
    // j est encore visible ici et n'est pas nécessaire

**Voir aussi** : [Ne pas utiliser une variable pour deux finalités sans rapport](010-expr.md#res-recycle)

##### Application

* Émettre un avertissement lorsqu'une variable modifiée dans l'énoncé `for` est déclarée en dehors de la boucle et non utilisée en dehors de la boucle.
* (strict) Signaler les variables de boucle déclarées avant la boucle et utilisées après la boucle à une fin sans rapport.

**Discussion** : Restreindre la portée de la variable de boucle au corps de la boucle aide aussi énormément les optimiseurs de code. Reconnaître que la variable d'induction n'est accessible que dans le corps de la boucle débloque des optimisations telles que l'élévation, la réduction de force, le déplacement de code invariant dans la boucle, etc.

##### Exemple C++17 et C++20

Note : C++17 et C++20 ajoutent également des énoncés d'initialisation pour `if`, `switch` et `for`-par-plage. Ceux-ci nécessitent le support C++17 et C++20.

    map<int, string> mymap;

    if (auto result = mymap.insert(value); result.second) {
        // insertion réussie, et result est valide pour ce bloc
        use(result.first);  // ok
        // ...
    } // result est détruit ici

##### Application C++17 et C++20 (si utilisation d'un compilateur C++17 ou C++20)

* Signaler les variables de sélection/boucle déclarées avant le corps et non utilisées après le corps
* (strict) Signaler les variables de sélection/boucle déclarées avant le corps et utilisées après le corps à une fin sans rapport.

### <a name="res-name-length"></a>ES.7 : Garder les noms courants et locaux courts, et garder les noms peu courants et non locaux plus longs

##### Justification

Lisibilité. Réduire le risque de conflits entre noms non locaux sans rapport.

##### Exemple

Des noms courts et locaux conventionnels augmentent la lisibilité :

    template<typename T>    // bon
    void print(ostream& os, const vector<T>& v)
    {
        for (gsl::index i = 0; i < v.size(); ++i)
            os << v[i] << '\n';
    }

Un indice est conventionnellement appelé `i` et il n'y a pas d'indice sur la signification du vecteur dans cette fonction générique, donc `v` est aussi bon nom que n'importe quel autre. Comparez :

    template<typename Element_type>   // mauvais : verbeux, difficile à lire
    void print(ostream& target_stream, const vector<Element_type>& current_vector)
    {
        for (gsl::index current_element_index = 0;
             current_element_index < current_vector.size();
             ++current_element_index
        )
        target_stream << current_vector[current_element_index] << '\n';
    }

Oui, c'est une caricature, mais nous avons vu pire.

##### Exemple

Des noms non locaux courts et non conventionnels obscurcissent le code :

    void use1(const string& s)
    {
        // ...
        tt(s);   // mauvais : qu'est-ce que tt() ?
        // ...
    }

Mieux, donnez aux entités non locales des noms lisibles :

    void use1(const string& s)
    {
        // ...
        trim_tail(s);   // meilleur
        // ...
    }

Ici, il y a de bonnes chances que le lecteur sache ce que signifie `trim_tail` et que le lecteur puisse s'en souvenir après l'avoir consulté.

##### Exemple, mauvais

Les noms d'arguments de grandes fonctions sont de facto non locaux et devraient être significatifs :

    void complicated_algorithm(vector<Record>& vr, const vector<int>& vi, map<string, int>& out)
    // lit depuis les événements de vr (en marquant les Records utilisés) pour les indices de
    // vi en plaçant des paires (nom, indice) dans out
    {
        // ... 500 lignes de code utilisant vr, vi, et out ...
    }

Nous recommandons de garder les fonctions courtes, mais cette règle n'est pas universellement respectée et le nommage devrait refléter cela.

##### Application

Vérifier la longueur des noms locaux et non locaux. Tenir aussi compte de la longueur de la fonction.

### <a name="res-name-similar"></a>ES.8 : Éviter les noms qui se ressemblent

##### Justification

Clarté et lisibilité du code. Des noms trop similaires ralentissent la compréhension et augmentent la probabilité d'erreur.

##### Exemple, mauvais

    if (readable(i1 + l1 + ol + o1 + o0 + ol + o1 + I0 + l0)) surprise();

##### Exemple, mauvais

Ne pas déclarer un nom non type avec le même nom qu'un type dans la même portée. Cela élimine le besoin de désambiguïsation avec un mot-clé tel que `struct` ou `enum`. Cela élimine aussi une source d'erreurs, car `struct X` peut implicitement déclarer `X` si la recherche échoue.

    struct foo { int n; };
    struct foo foo();       // MAUVAIS, foo est déjà un type en portée
    struct foo x = foo();   // nécessite une désambiguïsation

##### Exception

Les fichiers d'en-tête anciens pourraient déclarer des noms non types et des types avec le même nom dans la même portée.

##### Application

* Vérifier les noms par rapport à une liste de combinaisons connues de lettres et chiffres qui causent de la confusion.
* Signaler la déclaration d'une variable, fonction ou énumérateur qui masque une classe ou une énumération déclarée dans la même portée.

### <a name="res-not-caps"></a>ES.9 : Éviter les noms en `MAJUSCULES`

##### Justification

De tels noms sont couramment utilisés pour les macros. Ainsi, un nom en `MAJUSCULES` est vulnérable à une substitution macro non intentionnelle.

##### Exemple

    // quelque part dans un en-tête :
    #define NE !=

    // quelque part dans un autre en-tête :
    enum Coord { N, NE, NW, S, SE, SW, E, W };

    // quelque part troisième dans un .cpp d'un pauvre programmateur :
    switch (direction) {
    case N:
        // ...
    case NE:
        // ...
    // ...
    }

##### Note

N'utilisez pas `MAJUSCULES` pour les constantes juste parce que les constantes étaient autrefois des macros.

##### Application

Signaler toutes les utilisations en MAJUSCULES. Pour du code ancien, accepter les MAJUSCULES pour les noms de macros et signaler tous les noms de macros non en MAJUSCULES.

### <a name="res-name-one"></a>ES.10 : Déclarer un seul nom (à la fois) par déclaration

##### Justification

Une déclaration par ligne augmente la lisibilité et évite les erreurs liées à la grammaire C/C++. Cela laisse aussi de la place pour un commentaire de fin de ligne plus descriptif.

##### Exemple, mauvais

    char *p, c, a[7], *pp[7], **aa[10];   // beurk !

##### Exception

Une déclaration de fonction peut contenir plusieurs déclarations d'arguments de fonction.

##### Exception

Un lien structuré (C++17) est spécifiquement conçu pour introduire plusieurs variables :

    auto [iter, inserted] = m.insert_or_assign(k, val);
    if (inserted) { /* une nouvelle entrée a été insérée */ }

##### Exemple

    template<class InputIterator, class Predicate>
    bool any_of(InputIterator first, InputIterator last, Predicate pred);

ou mieux en utilisant des concepts :

    bool any_of(input_iterator auto first, input_iterator auto last, predicate auto pred);

##### Exemple

    double scalbn(double x, int n);   // OK : x * pow(FLT_RADIX, n) ; FLT_RADIX est généralement 2

ou :

    double scalbn(    // meilleur : x * pow(FLT_RADIX, n) ; FLT_RADIX est généralement 2
        double x,     // valeur de base
        int n         // exposant
    );

ou :

    // meilleur : base * pow(FLT_RADIX, exposant) ; FLT_RADIX est généralement 2
    double scalbn(double base, int exponent);

##### Exemple

    int a = 10, b = 11, c = 12, d, e = 14, f = 15;

Dans une longue liste de déclarateurs, il est facile de rater une variable non initialisée.

##### Application

Signaler les déclarations de variables et de constantes avec plusieurs déclarateurs (par exemple `int* p, q;`)

### <a name="res-auto"></a>ES.11 : Utiliser `auto` pour éviter les répétitions redondantes de noms de types

##### Justification

* La simple répétition est fastidieuse et sujet à erreurs.
* Quand on utilise `auto`, le nom de l'entité déclarée est à une position fixe dans la déclaration, ce qui augmente la lisibilité.
* Dans une déclaration de gabarit de fonction, le type de retour peut être un type membre.

##### Exemple

Considérez :

    auto p = v.begin();      // vector<DataRecord>::iterator
    auto z1 = v[3];          // fait une copie de DataRecord
    auto& z2 = v[3];         // évite la copie
    const auto& z3 = v[3];   // const et évite la copie
    auto h = t.future();
    auto q = make_unique<int[]>(s);
    auto f = [](int x) { return x + 10; };

Dans chaque cas, nous évitons d'écrire un type long et difficile à mémoriser que le compilateur connaît déjà mais qu'un programmeur pourrait mal orthographier.

##### Exemple

    template<class T>
    auto Container<T>::first() -> Iterator;   // Container<T>::Iterator

##### Exception

Éviter `auto` pour les listes d'initialisation et dans les cas où vous savez exactement quel type vous voulez et où un initialiseur pourrait nécessiter une conversion.

##### Exemple

    auto lst = { 1, 2, 3 };   // lst est une liste d'initialisation
    auto x{1};   // x est un int (en C++17 ; initializer_list en C++11)

##### Note

Depuis C++20, nous pouvons (et devrions) utiliser des concepts pour être plus précis sur le type que nous déduisons :

    // ...
    forward_iterator auto p = algo(x, y, z);

##### Exemple (C++17)

    std::set<int> values;
    // ...
    auto [ position, newly_inserted ] = values.insert(5);   // décomposer les membres du std::pair

##### Application

Signaler les répétitions redondantes de noms de types dans une déclaration.

### <a name="res-reuse"></a>ES.12 : Ne pas réutiliser des noms dans des portées imbriquées

##### Justification

Il est facile de se tromper sur quelle variable est utilisée.
Peut causer des problèmes de maintenance.

##### Exemple, mauvais

    int d = 0;
    // ...
    if (cond) {
        // ...
        d = 9;
        // ...
    }
    else {
        // ...
        int d = 7;
        // ...
        d = value_to_be_returned;
        // ...
    }

    return d;

S'il s'agit d'un grand énoncé `if`, il est facile de rater qu'un nouveau `d` a été introduit dans la portée interne.
C'est une source connue de bogues.
Parfois, cette telle réutilisation d'un nom dans une portée interne est appelée « ombrage ».

##### Note

L'ombrage est principalement un problème lorsque les fonctions sont trop grandes et trop complexes.

##### Exemple

L'ombrage d'arguments de fonction dans le bloc le plus externe est interdit par le langage :

    void f(int x)
    {
        int x = 4;  // erreur : réutilisation du nom d'argument de fonction

        if (x) {
            int x = 7;  // autorisé, mais mauvais
            // ...
        }
    }

##### Exemple, mauvais

La réutilisation d'un nom de membre comme variable locale peut aussi poser problème :

    struct S {
        int m;
        void f(int x);
    };

    void S::f(int x)
    {
        m = 7;    // affectation au membre
        if (x) {
            int m = 9;
            // ...
            m = 99; // affectation à la variable locale
            // ...
        }
    }

##### Exception

Nous réutilisons souvent des noms de fonction d'une classe de base dans une classe dérivée :

    struct B {
        void f(int);
    };

    struct D : B {
        void f(double);
        using B::f;
    };

Cela est sujet à erreurs.
Par exemple, si nous avions oublié la déclaration `using`, un appel `d.f(1)` n'aurait pas trouvé la version `int` de `f`.

??? Avons-nous besoin d'une règle spécifique sur l'ombrage/le masquage dans les hiérarchies de classes ?

##### Application

* Signaler la réutilisation d'un nom dans des portées locales imbriquées
* Signaler la réutilisation d'un nom de membre comme variable locale dans une fonction membre
* Signaler la réutilisation d'un nom global comme variable locale ou nom de membre
* Signaler la réutilisation d'un nom de membre d'une classe de base dans une classe dérivée (sauf pour les noms de fonctions)

### <a name="res-always"></a>ES.20 : Toujours initialiser un objet

##### Justification

Éviter les erreurs d'utilisation avant affectation et leur comportement indéfini associé.
Éviter les problèmes de compréhension d'initialisations complexes.
Simplifier la refactoring.

##### Exemple

    void use(int arg)
    {
        int i;   // mauvais : variable non initialisée
        // ...
        i = 7;   // initialiser i
    }

Non, `i = 7` n'initialise pas `i` ; cela lui affecte une valeur. De plus, `i` peut être lu dans la partie `...`. Mieux :

    void use(int arg)   // OK
    {
        int i = 7;   // OK : initialisé
        string s;    // OK : initialisé par défaut
        // ...
    }

##### Note

La règle *toujours initialiser* est délibérément plus stricte que la règle langagière *un objet doit être affecté avant d'être utilisé*.
La seconde, règle plus souple, capture les bogues techniques, mais :

* Elle conduit à un code moins lisible
* Elle encourage les gens à déclarer des noms dans des portées plus grandes que nécessaire
* Elle conduit à un code plus difficile à lire
* Elle conduit à des bogues logiques en encourageant un code complexe
* Elle gêne la refactoring

La règle *toujours initialiser* est une règle de style visant à améliorer la maintenabilité ainsi qu'une règle de protection contre les erreurs d'utilisation avant affectation.

##### Exemple

Voici un exemple souvent considéré comme démontrant le besoin d'une règle d'initialisation plus souple

    widget i;    // "widget" un type coûteux à initialiser, possiblement un grand type trivial
    widget j;

    if (cond) {  // mauvais : i et j sont initialisés "tard"
        i = f1();
        j = f2();
    }
    else {
        i = f3();
        j = f4();
    }

Cela ne peut pas être trivialement réécrit pour initialiser `i` et `j` avec des initialiseurs.
Notez que pour les types avec un constructeur par défaut, tenter de reporter l'initialisation conduit simplement à une initialisation par défaut suivie d'une affectation.
Une raison populaire pour de tels exemples est l'« efficacité », mais un compilateur capable de détecter si nous avons commis une erreur d'utilisation avant affectation peut aussi éliminer toute double initialisation redondante.

En supposant qu'il y ait un lien logique entre `i` et `j`, ce lien devrait probablement être exprimé dans le code :

    pair<widget, widget> make_related_widgets(bool x)
    {
        return (x) ? {f1(), f2()} : {f3(), f4()};
    }

    auto [i, j] = make_related_widgets(cond);    // C++17

Si la fonction `make_related_widgets` est autrement redondante,
nous pouvons l'éliminer en utilisant une lambda [ES.28](010-expr.md#res-lambda-init) :

    auto [i, j] = [x] { return (x) ? pair{f1(), f2()} : pair{f3(), f4()} }();    // C++17

Utiliser une valeur représentant « non initialisé » est un symptôme d'un problème et non une solution :

    widget i = uninit;  // mauvais
    widget j = uninit;

    // ...
    use(i);         // possiblement utilisé avant affectation
    // ...

    if (cond) {     // mauvais : i et j sont initialisés "tard"
        i = f1();
        j = f2();
    }
    else {
        i = f3();
        j = f4();
    }

Maintenant, le compilateur ne peut même plus simplement détecter une utilisation avant affectation. De plus, nous avons introduit de la complexité dans l'espace d'états pour widget : quelles opérations sont valides sur un widget `uninit` et lesquelles ne le sont pas ?

##### Note

L'initialisation complexe a été populaire chez les programmeurs brillants depuis des décennies.
Cela a aussi été une source majeure d'erreurs et de complexité.
Beaucoup de ces erreurs sont introduites pendant la maintenance des années après l'implémentation initiale.

##### Exemple

Cette règle couvre les membres de données.

    class X {
    public:
        X(int i, int ci) : m2{i}, cm2{ci} {}
        // ...

    private:
        int m1 = 7;
        int m2;
        int m3;

        const int cm1 = 7;
        const int cm2;
        const int cm3;
    };

Le compilateur signalera `cm3` non initialisé car il est `const`, mais il ne capttera pas le manque d'initialisation de `m3`.
Habituellement, une initialisation de membre rarement superflue vaut l'absence d'erreurs dues au manque d'initialisation et souvent un optimiseur
peut éliminer une initialisation redondante (par exemple, une initialisation qui se produit juste avant une affectation).

##### Exception

Si vous déclarez un objet qui est sur le point d'être initialisé depuis une entrée, l'initialiser causerait une double initialisation.
Cependant, attention que cela pourrait laisser des données non initialisées au-delà de l'entrée -- et cela a été une source féconde d'erreurs et de violations de sécurité :

    constexpr int max = 8 * 1024;
    int buf[max];         // OK, mais suspect : non initialisé
    f.read(buf, max);

Le coût d'initialisation de ce tableau pourrait être significatif dans certaines situations.
Cependant, de tels exemples ont tendance à laisser des variables non initialisées accessibles, donc ils doivent être traités avec suspicion.

    constexpr int max = 8 * 1024;
    int buf[max] = {};   // zéro tous les éléments ; meilleur dans certaines situations
    f.read(buf, max);

À cause des règles restrictives d'initialisation pour les tableaux et `std::array`, ceux-ci offrent les exemples les plus convaincants du besoin de cette exception.

Quand c'est faisable, utiliser une fonction de bibliothèque connue pour ne pas déborder. Par exemple :

    string s;   // s est initialisé par défaut à ""
    cin >> s;   // s s'étend pour contenir la chaîne

Ne considérez pas comme exception à cette règle les variables simples qui sont des cibles d'opérations d'entrée :

    int i;   // mauvais
    // ...
    cin >> i;

Dans le cas non rare où la cible d'entrée et l'opération d'entrée se séparent (comme elles ne devraient pas), la possibilité d'utilisation avant affectation s'ouvre.

    int i2 = 0;   // meilleur, en supposant que zéro est une valeur acceptable pour i2
    // ...
    cin >> i2;

Un bon optimiseur devrait connaître les opérations d'entrée et éliminer l'opération redondante.


##### Note

Parfois, une lambda peut être utilisée comme initialiseur pour éviter une variable non initialisée :

    error_code ec;
    Value v = [&] {
        auto p = get_value();   // get_value() retourne un pair<error_code, Value>
        ec = p.first;
        return p.second;
    }();

ou peut-être :

    Value v = [] {
        auto p = get_value();   // get_value() retourne un pair<error_code, Value>
        if (p.first) throw Bad_value{p.first};
        return p.second;
    }();

**Voir aussi** : [ES.28](010-expr.md#res-lambda-init)

##### Application

* Signaler chaque variable non initialisée.
  Ne pas signaler les variables de types définis par l'utilisateur avec des constructeurs par défaut.
* Vérifier qu'un tampon non initialisé est écrit *immédiatement* après la déclaration.
  Passer une variable non initialisée comme référence à un argument non-`const` peut être supposé être une écriture dans la variable.

### <a name="res-introduce"></a>ES.21 : Ne pas introduire une variable (ou une constante) avant d'en avoir besoin

##### Justification

Lisibilité. Limiter la portée dans laquelle la variable peut être utilisée.

##### Exemple

    int x = 7;
    // ... pas d'utilisation de x ici ...
    ++x;

##### Application

Signaler les déclarations qui sont éloignées de leur première utilisation.

### <a name="res-init"></a>ES.22 : Ne pas déclarer une variable tant qu'on n'a pas de valeur pour l'initialiser

##### Justification

Lisibilité. Limiter la portée dans laquelle une variable peut être utilisée. Ne pas risquer une utilisation avant affectation. L'initialisation est souvent plus efficace que l'affectation.

##### Exemple, mauvais

    string s;
    // ... pas d'utilisation de s ici ...
    s = "what a waste";

##### Exemple, mauvais

    SomeLargeType var;  // Difficile à lire CaMeLcAsEvArIaBlE

    if (cond)   // certaines conditions non triviales
        Set(&var);
    else if (cond2 || !cond3) {
        var = Set2(3.14);
    }
    else {
        var = 0;
        for (auto& e : something)
            var += e;
    }

    // utiliser var ; que cela ne soit pas fait trop tôt peut être garanti statiquement avec seulement le flux de contrôle

Ce serait correct s'il y avait une initialisation par défaut pour `SomeLargeType` qui n'était pas trop coûteuse.
Sinon, un programmeur pourrait très bien se demander si tous les chemins possibles à travers le labyrinthe de conditions ont été couverts.
Si ce n'est pas le cas, nous avons un bogue d'« utilisation avant affectation ». C'est un piège de maintenance.

Pour des initialiseurs de complexité modérée, y compris pour des variables `const`, envisagez d'utiliser une lambda pour exprimer l'initialiseur ; voir [ES.28](010-expr.md#res-lambda-init).

##### Application

* Signaler les déclarations avec initialisation par défaut qui sont affectées avant d'être lues pour la première fois.
* Signaler tout calcul compliqué après une variable non initialisée et avant son utilisation.

### <a name="res-list"></a>ES.23 : Privilégier la syntaxe d'initialisation par `{}`}

##### Justification

Privilégier `{}`. Les règles d'initialisation par `{}` sont plus simples, plus générales, moins ambiguës et plus sûres que pour d'autres formes d'initialisation.

Utiliser `=` seulement quand vous êtes sûr qu'il ne peut pas y avoir de conversions rétrécissantes. Pour les types arithmétiques intégrés, utiliser `=` seulement avec `auto`.

Éviter l'initialisation par `()`, qui permet des ambiguïtés d'analyse.

##### Exemple

    int x {f(99)};
    int y = x;
    vector<int> v = {1, 2, 3, 4, 5, 6};

##### Exception

Pour les conteneurs, il y a une tradition d'utiliser `{...}` pour une liste d'éléments et `(...)` pour les tailles :

    vector<int> v1(10);    // vecteur de 10 éléments avec la valeur par défaut 0
    vector<int> v2{10};    // vecteur de 1 élément avec la valeur 10

    vector<int> v3(1, 2);  // vecteur de 1 élément avec la valeur 2
    vector<int> v4{1, 2};  // vecteur de 2 éléments avec les valeurs 1 et 2

##### Note

Les initialiseurs `{}` n'autorisent pas les conversions rétrécissantes (et c'est généralement une bonne chose) et autorisent les constructeurs explicites (ce qui est normal, nous initialisons intentionnellement une nouvelle variable).

##### Exemple

    int x {7.9};   // erreur : rétrécissement
    int y = 7.9;   // OK : y devient 7. Espérons un avertissement du compilateur
    int z {gsl::narrow_cast<int>(7.9)};    // OK : vous l'avez demandé
    auto zz = gsl::narrow_cast<int>(7.9);  // OK : vous l'avez demandé

##### Note

L'initialisation par `{}` peut être utilisée pour presque toute initialisation ; d'autres formes d'initialisation ne peuvent pas :

    auto p = new vector<int> {1, 2, 3, 4, 5};   // vecteur initialisé
    D::D(int a, int b) :m{a, b} {   // initialiseur de membre (par exemple, m pourrait être un pair)
        // ...
    };
    X var {};   // initialiser var à vide
    struct S {
        int m {7};   // initialiseur par défaut pour un membre
        // ...
    };

Pour cette raison, l'initialisation par `{}` est souvent appelée « initialisation uniforme »
(bien qu'il y ait malheureusement quelques irrégularités restantes).

##### Note

L'initialisation d'une variable déclarée avec `auto` par une seule valeur, par exemple `{v}`, avait des résultats surprenants jusqu'à C++17.
Les règles C++17 sont un peu moins surprenantes :

    auto x1 {7};        // x1 est un int avec la valeur 7
    auto x2 = {7};      // x2 est un initializer_list<int> avec un élément 7

    auto x11 {7, 8};    // erreur : deux initialiseurs
    auto x22 = {7, 8};  // x22 est un initializer_list<int> avec les éléments 7 et 8

Utiliser `={...}` si vous voulez vraiment un `initializer_list<T>`

    auto fib10 = {1, 1, 2, 3, 5, 8, 13, 21, 34, 55};   // fib10 est une liste

##### Note

`={}` donne une initialisation par copie tandis que `{}` donne une initialisation directe.
Comme la distinction entre initialisation par copie et initialisation directe elle-même, cela peut conduire à des surprises.
`{}` accepte les constructeurs `explicit` ; `={}` ne le fait pas. Par exemple :

    struct Z { explicit Z() {} };

    Z z1{};     // OK : initialisation directe, donc nous utilisons le constructeur explicit
    Z z2 = {};  // erreur : initialisation par copie, donc nous ne pouvons pas utiliser le constructeur explicit

Utiliser l'initialisation simple par `{}` sauf si vous souhaitez spécifiquement désactiver les constructeurs explicites.

##### Exemple

    template<typename T>
    void f()
    {
        T x1(1);    // T initialisé avec 1
        T x0();     // mauvais : déclaration de fonction (souvent une erreur)

        T y1 {1};   // T initialisé avec 1
        T y0 {};    // T initialisé par défaut
        // ...
    }

**Voir aussi** : [Discussion](#???) @TODO-LINK

##### Application

* Signaler les utilisations de `=` pour initialiser des types arithmétiques où un rétrécissement se produit.
* Signaler les utilisations de la syntaxe d'initialisation `()` qui sont en fait des déclarations. (Beaucoup de compilateurs devraient déjà avertir à ce sujet.)

### <a name="res-unique"></a>ES.24 : Utiliser un `unique_ptr<T>` pour conserver des pointeurs

##### Justification

L'utilisation de `std::unique_ptr` est la manière la plus simple d'éviter les fuites. C'est fiable, il
laisse le système de types faire une grande partie du travail de validation de la sécurité de propriété, il
augmente la lisibilité, et il a un coût d'exécution nul ou quasi nul.

##### Exemple

    void use(bool leak)
    {
        auto p1 = make_unique<int>(7);   // OK
        int* p2 = new int{7};            // mauvais : pourrait fuir
        // ... pas d'affectation à p2 ...
        if (leak) return;
        // ... pas d'affectation à p2 ...
        vector<int> v(7);
        v.at(7) = 0;                    // exception levée
        delete p2;                      // trop tard pour empêcher les fuites
        // ...
    }

Si `leak == true`, l'objet pointé par `p2` fuit et l'objet pointé par `p1` ne fuit pas.
C'est le même cas quand `at()` lève une exception. Dans les deux cas, l'énoncé `delete p2` n'est pas atteint.

##### Application

Chercher des pointeurs bruts qui sont des cibles de `new`, `malloc()`, ou de fonctions qui pourraient retourner de tels pointeurs.

### <a name="res-const"></a>ES.25 : Déclarer un objet `const` ou `constexpr` sauf si vous souhaitez modifier sa valeur plus tard

##### Justification

De cette façon vous ne pouvez pas changer la valeur par accident. De cette façon le compilateur pourrait bénéficier d'opportunités d'optimisation.

##### Exemple

    void f(int n)
    {
        const int bufmax = 2 * n + 2;  // bon : nous ne pouvons pas changer bufmax par accident
        int xmax = n;                  // suspect : xmax est-il censé changer ?
        // ...
    }

##### Application

Voir si une variable est effectivement mutée, et la signaler si
non. Malheureusement, il pourrait être impossible de détecter quand un non-`const` n'était pas
*censé* varier (par opposition à simplement n'avoir pas varié).

### <a name="res-recycle"></a>ES.26 : Ne pas utiliser une variable pour deux finalités sans rapport

##### Justification

Lisibilité et sûreté.

##### Exemple, mauvais

    void use()
    {
        int i;
        for (i = 0; i < 20; ++i) { /* ... */ }
        for (i = 0; i < 200; ++i) { /* ... */ } // mauvais : i réutilisé
    }

##### Note

En tant qu'optimisation, vous pourriez vouloir réutiliser un tampon comme zone de travail, mais même dans ce cas, préférez limiter la portée de la variable autant que possible et faites attention à ne pas causer de bogues à partir de données laissées dans un tampon réutilisé, car c'est une source commune de bogues de sécurité.

    void write_to_file()
    {
        std::string buffer;             // pour éviter les réallocations à chaque itération de boucle
        for (auto& o : objects) {
            // Première partie du travail.
            generate_first_string(buffer, o);
            write_to_file(buffer);

            // Seconde partie du travail.
            generate_second_string(buffer, o);
            write_to_file(buffer);

            // etc...
        }
    }

##### Application

Signaler les variables réutilisées.

### <a name="res-stack"></a>ES.27 : Utiliser `std::array` ou `stack_array` pour les tableaux sur la pile

##### Justification

Ils sont lisibles et ne convertissent pas implicitement en pointeurs.
Ils ne sont pas confondus avec des extensions non standard des tableaux intégrés.

##### Exemple, mauvais

    const int n = 7;
    int m = 9;

    void f()
    {
        int a1[n];
        int a2[m];   // erreur : non ISO C++
        // ...
    }

##### Note

La définition de `a1` est un C++ légal et l'a toujours été.
Il y a beaucoup de tel code.
Cependant, c'est sujet à erreurs, surtout quand la borne est non locale.
De plus, c'est une source « populaire » d'erreurs (débordement de tampon, pointeurs par dégénérescence de tableau, etc.).
La définition de `a2` est du C mais pas du C++ et est considérée comme un risque de sécurité.

##### Exemple

    const int n = 7;
    int m = 9;

    void f()
    {
        array<int, n> a1;
        stack_array<int> a2(m);
        // ...
    }

##### Application

* Signaler les tableaux avec des bornes non constantes (VLAs de style C)
* Signaler les tableaux avec des bornes constantes non locales

### <a name="res-lambda-init"></a>ES.28 : Utiliser des lambda pour les initialisations complexes, en particulier de variables `const`

##### Justification

Cela encapsule proprement l'initialisation locale, y compris le nettoyage des variables temporaires nécessaires uniquement pour l'initialisation, sans avoir à créer une fonction non locale inutilement non réutilisable. Cela fonctionne aussi pour des variables qui devraient être `const` mais seulement après un travail d'initialisation.

##### Exemple, mauvais

    widget x;   // devrait être const, mais :
    for (auto i = 2; i <= N; ++i) {          // cela pourrait être du code
        x += some_obj.do_something_with(i);  // arbitrairement long
    }                                        // nécessaire pour initialiser x
    // d'ici, x devrait être const, mais nous ne pouvons pas le dire dans le code dans ce style

##### Exemple, bon

    const widget x = [&] {
        widget val;                                // suppose que widget a un constructeur par défaut
        for (auto i = 2; i <= N; ++i) {            // cela pourrait être du code
            val += some_obj.do_something_with(i);  // arbitrairement long
        }                                          // nécessaire pour initialiser x
        return val;
    }();

Si possible, réduisez les conditions à un simple ensemble d'alternatives (par exemple, un `enum`) et ne mélangez pas sélection et initialisation.

##### Application

Difficile. Au mieux une heuristique. Chercher une variable non initialisée suivie d'une boucle qui lui affecte.

### <a name="res-macros"></a>ES.30 : Ne pas utiliser de macros pour la manipulation du texte de programme

##### Justification

Les macros sont une source majeure de bogues.
Les macros n'obéissent pas aux règles habituelles de portée et de type.
Les macros garantissent que le lecteur humain voit quelque chose de différent de ce que le compilateur voit.
Les macros compliquent la construction d'outils.

##### Exemple, mauvais

    #define Case break; case   /* MAUVAIS */

Cette macro qui semble inoffensive transforme un simple `c` minuscule au lieu d'un `C` en un bogue de contrôle de flux.

##### Note

Cette règle n'interdit pas l'utilisation de macros pour le « contrôle de configuration » dans des `#ifdef`, etc.

À l'avenir, les modules élimineront probablement le besoin de macros dans le contrôle de configuration.

##### Note

Cette règle vise aussi à décourager l'utilisation de `#` pour la stringify et `##` pour la concaténation.
Comme d'habitude pour les macros, il y a des utilisations « quasi inoffensives », mais même celles-ci peuvent créer des problèmes pour les outils,
tels que les compléteurs automatiques, les analyseurs statiques, et les débogueurs.
Souvent le désir d'utiliser des macros sophistiquées est un signe d'une conception trop complexe.
De plus, `#` et `##` encouragent la définition et l'utilisation de macros :

    #define CAT(a, b) a ## b
    #define STRINGIFY(a) #a

    void f(int x, int y)
    {
        string CAT(x, y) = "asdf";   // MAUVAIS : difficile pour les outils à traiter (et laid)
        string sx2 = STRINGIFY(x);
        // ...
    }

Il existe des alternatives pour la manipulation de bas niveau de chaînes utilisant des macros. Par exemple :

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
        // ...
    }

Cela n'est pas aussi pratique qu'une macro à définir, mais aussi facile à utiliser, a un coût nul, et est typé et scoppé.

À l'avenir, la réflexion statique éliminera probablement les derniers besoins du préprocesseur pour la manipulation du texte de programme.

##### Application

Crierez quand vous voyez une macro qui n'est pas simplement utilisée pour le contrôle de source (par exemple `#ifdef`)

### <a name="res-macros2"></a>ES.31 : Ne pas utiliser de macros pour les constantes ou les « fonctions »

##### Justification

Les macros sont une source majeure de bogues.
Les macros n'obéissent pas aux règles habituelles de portée et de type.
Les macros n'obéissent pas aux règles habituelles de passage d'arguments.
Les macros garantissent que le lecteur humain voit quelque chose de différent de ce que le compilateur voit.
Les macros compliquent la construction d'outils.

##### Exemple, mauvais

    #define PI 3.14
    #define SQUARE(a, b) (a * b)

Même si nous n'avions pas laissé un bogue bien connu dans `SQUARE`, il existe des alternatives beaucoup mieux comportées ; par exemple :

    constexpr double pi = 3.14;
    template<typename T> T square(T a, T b) { return a * b; }

##### Application

Crierez quand vous voyez une macro qui n'est pas simplement utilisée pour le contrôle de source (par exemple `#ifdef`)

### <a name="res-all_caps"></a>ES.32 : Utiliser `MAJUSCULES` pour tous les noms de macros

##### Justification

Convention. Lisibilité. Distinction des macros.

##### Exemple

    #define forever for (;;)   /* très MAUVAIS */

    #define FOREVER for (;;)   /* Toujours mauvais, mais au moins visible pour les humains */

##### Application

Crierez quand vous voyez une macro en minuscules.

### <a name="res-macros3"></a>ES.33 : Si vous devez utiliser des macros, donnez-leur des noms uniques

##### Justification

Les macros n'obéissent pas aux règles de portée.

##### Exemple

    #define MYCHAR        /* MAUVAIS, finira par entrer en conflit avec le MYCHAR de quelqu'un d'autre */

    #define ZCORP_CHAR    /* Toujours mauvais, mais moins susceptible d'entrer en conflit */

##### Note

Évitez les macros si vous le pouvez : [ES.30](010-expr.md#res-macros), [ES.31](010-expr.md010-expr.md#res-macros2), et [ES.32](010-expr.md#res-all_caps).
Cependant, il y a des milliards de lignes de code parsemées de macros et une longue tradition d'utilisation et de surutilisation des macros.
Si vous êtes forcé d'utiliser des macros, utilisez des noms longs et des préfixes prétendument uniques (par exemple, le nom de votre organisation) pour réduire la probabilité d'un conflit.

##### Application

Émettre un avertissement contre les noms de macros courts.

### <a name="res-ellipses"></a> ES.34 : Ne pas définir de fonction variable (au sens C)

##### Justification

Pas de sécurité de type.
Nécessite un code embrouillé plein de transpositions et de macros pour fonctionner correctement.

##### Exemple

    #include <cstdarg>

    // "severity" suivi d'une liste de char* terminée par zéro ; écrire les chaînes de style C sur cerr
    void error(int severity ...)
    {
        va_list ap;             // un type magique pour contenir les arguments
        va_start(ap, severity); // démarrage des arguments : "severity" est le premier argument de error()

        for (;;) {
            // traiter le prochain var comme un char* ; pas de vérification : une transposition déguisée
            char* p = va_arg(ap, char*);
            if (!p) break;
            cerr << p << ' ';
        }

        va_end(ap);             // nettoyage des arguments (ne pas oublier cela)

        cerr << '\n';
        if (severity) exit(severity);
    }

    void use()
    {
        error(7, "this", "is", "an", "error", nullptr);
        error(7); // crash
        error(7, "this", "is", "an", "error");  // crash
        const char* is = "is";
        string an = "an";
        error(7, "this", is, an, "error"); // crash
    }

**Alternative** : Surcharge. Gabarits. Gabarits variables.

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
        error(7); // Pas de crash !
        error(5, "this", "is", "not", "an", "error"); // Pas de crash !

        std::string an = "an";
        error(7, "this", "is", "not", an, "error"); // Pas de crash !

        error(5, "oh", "no", nullptr); // Erreur de compilation ! Pas besoin de nullptr.
    }


##### Note

C'est essentiellement la manière dont `printf` est implémentée.

##### Application

* Signaler les définitions de fonctions variables de style C.
* Signaler `#include <cstdarg>` et `#include <stdarg.h>`


## ES.expr : Expressions

Les expressions manipulent des valeurs.

### <a name="res-complicated"></a>ES.40 : Éviter les expressions compliquées

##### Justification

Les expressions compliquées sont sujettes aux erreurs.

##### Exemple

    // mauvais : affectation cachée dans une sous-expression
    while ((c = getc()) != -1)

    // mauvais : deux variables non locales affectées dans des sous-expressions
    while ((cin >> c1, cin >> c2), c1 == c2)

    // meilleur, mais possiblement toujours trop compliqué
    for (char c1, c2; cin >> c1 >> c2 && c1 == c2;)

    // OK : si i et j ne sont pas aliasés
    int x = ++i + ++j;

    // OK : si i != j et i != k
    v[i] = v[j] + v[k];

    // mauvais : plusieurs affectations « cachées » dans des sous-expressions
    x = a + (b = f()) + (c = g()) * 7;

    // mauvais : repose sur des règles de priorité souvent mal comprises
    x = a & b + c * d && e ^ f == 7;

    // mauvais : comportement indéfini
    x = x++ + x++ + ++x;

Certaines de ces expressions sont inconditionnellement mauvaises (par exemple, elles reposent sur un comportement indéfini). D'autres sont simplement tellement compliquées et/ou inhabituelles que même de bons programmeurs pourraient les mal comprendre ou rater un problème en étant pressés.

##### Note

C++17 resserre les règles pour l'ordre d'évaluation
(gauche-à-droite sauf droite-à-gauche dans les affectations, et l'ordre d'évaluation des arguments de fonction est non spécifié ; [voir ES.43](010-expr.md#res-order)),
mais cela ne change pas le fait que les expressions compliquées sont potentiellement confuses.

##### Note

Un programmeur devrait connaître et utiliser les règles de base pour les expressions.

##### Exemple

    x = k * y + z;             // OK

    auto t1 = k * y;           // mauvais : inutilement verbeux
    x = t1 + z;

    if (0 <= x && x < max)   // OK

    auto t1 = 0 <= x;        // mauvais : inutilement verbeux
    auto t2 = x < max;
    if (t1 && t2)            // ...

##### Application

Difficile. Quelle doit être la complexité d'une expression pour être considérée comme compliquée ? Écrire des calculs comme des énoncés avec une opération chacun est aussi confus. Choses à considérer :

* effets de bord : effets de bord sur plusieurs variables non locales (pour certaines définitions de non-local) peuvent être suspects, surtout si les effets de bord sont dans des sous-expressions séparées
* écritures sur des variables aliasées
* plus de N opérateurs (et que devrait être N ?)
* dépendance à des règles de priority subtiles
* utilisation de comportement indéfini (peut-on capturer tout le comportement indéfini ?)
* comportement défini par l'implémentation ?
* ???

### <a name="res-parens"></a>ES.41 : En cas de doute sur la priorité des opérateurs, ajouter des parenthèses

##### Justification

Éviter les erreurs. Lisibilité. Tout le monde n'a pas mémorisé le tableau des opérateurs.

##### Exemple

    const unsigned int flag = 2;
    unsigned int a = flag;

    if (a & flag != 0)  // mauvais : signifie a&(flag != 0)

Note : Nous recommandons que les programmeurs connaissent leur tableau de priorité pour les opérations arithmétiques, les opérations logiques, mais considèrent le mélange d'opérateurs logiques bit à bit avec d'autres opérateurs comme nécessitant des parenthèses.

    if ((a & flag) != 0)  // OK : fonctionne comme prévu

##### Note

Vous devriez savoir assez pour ne pas avoir besoin de parenthèses pour :

    if (a < 0 || a <= max) {
        // ...
    }

##### Application

* Signaler les combinaisons d'opérateurs logiques bit à bit et d'autres opérateurs.
* Signaler les opérateurs d'affectation non en position la plus à gauche.
* ???

### <a name="res-ptr"></a>ES.42 : Garder l'utilisation des pointeurs simple et directe

##### Justification

La manipulation de pointeurs compliquée est une source majeure d'erreurs.

##### Note

Utiliser `gsl::span` à la place.
Les pointeurs devraient [ne référencer que des objets uniques](005-interfaces.md#ri-array).
L'arithmétique sur les pointeurs est fragile et facile à obtenir de travers, source de nombreux, nombreux mauvais bogues et violations de sécurité.
`span` est un type vérifié par limites, sûr pour accéder aux tableaux de données.
L'accès dans un tableau avec des bornes connues en utilisant une constante comme indice peut être validé par le compilateur.

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

    void f(span<int> a) // MEILLEUR : utiliser span dans la déclaration de fonction
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

L'indexation avec une variable est difficile à valider comme sûre, tant pour les outils que pour les humains.
`span` est un type vérifié par limites à l'exécution, sûr pour accéder aux tableaux de données.
`at()` est une autre alternative qui garantit que les accès unitaires sont vérifiés par limites.
Si des itérateurs sont nécessaires pour accéder à un tableau, utiliser les itérateurs d'un `span` construit sur le tableau.

##### Exemple, mauvais

    void f(array<int, 10> a, int pos)
    {
        a[pos / 2] = 1; // MAUVAIS
        a[pos - 1] = 2; // MAUVAIS
        a[-1] = 3;    // MAUVAIS (mais facilement capturé par les outils) -- pas de remplacement, ne faites pas ça
        a[10] = 4;    // MAUVAIS (mais facilement capturé par les outils) -- pas de remplacement, ne faites pas ça
    }

##### Exemple, bon

Utiliser un `span` :

    void f1(span<int, 10> a, int pos) // A1 : Changer le type de paramètre pour utiliser span
    {
        a[pos / 2] = 1; // OK
        a[pos - 1] = 2; // OK
    }

    void f2(array<int, 10> arr, int pos) // A2 : Ajouter un span local et l'utiliser
    {
        span<int> a = {arr.data(), pos};
        a[pos / 2] = 1; // OK
        a[pos - 1] = 2; // OK
    }

Utiliser `at()` :

    void f3(array<int, 10> a, int pos) // ALTERNATIVE B : Utiliser at() pour l'accès
    {
        at(a, pos / 2) = 1; // OK
        at(a, pos - 1) = 2; // OK
    }

##### Exemple, mauvais

    void f()
    {
        int arr[COUNT];
        for (int i = 0; i < COUNT; ++i)
            arr[i] = i; // MAUVAIS, ne peut pas utiliser un index non constant
    }

##### Exemple, bon

Utiliser un `span` :

    void f1()
    {
        int arr[COUNT];
        span<int> av = arr;
        for (int i = 0; i < COUNT; ++i)
            av[i] = i;
    }

Utiliser un `span` et un `for`-par-plage :

    void f1a()
    {
         int arr[COUNT];
         span<int, COUNT> av = arr;
         int i = 0;
         for (auto& e : av)
             e = i++;
    }

Utiliser `at()` pour l'accès :

    void f2()
    {
        int arr[COUNT];
        for (int i = 0; i < COUNT; ++i)
            at(arr, i) = i;
    }

Utiliser un `for`-par-plage