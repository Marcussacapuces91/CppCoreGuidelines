# <a name="s-expr"></a>ES : Expressions et déclarations

Les expressions et les déclarations sont le moyen le plus bas niveau et le plus direct d'exprimer des actions et des calculs. Les déclarations dans des étendues locales sont des déclarations (statements).

Pour les règles de nommage, de commentaires et d'indentation, voir [NL : Nommage et mise en page](024-naming.md).

Règles générales :

* [ES.1 : Privilégier la bibliothèque standard aux autres bibliothèques et au « code artisanal »](010-expr.md#res-lib)
* [ES.2 : Privilégier des abstractions appropriées à l'utilisation directe des fonctionnalités du langage](010-expr.md#res-abstr)
* [ES.3 : Ne pas se répéter, éviter le code redondant](010-expr.md#res-dry)

Règles de déclaration :

* [ES.5 : Garder les étendues (scopes) petites](010-expr.md#res-scope)
* [ES.6 : Déclarer les noms dans les initialisateurs et les conditions des boucles for pour limiter l'étendue](010-expr.md#res-cond)
* [ES.7 : Garder les noms courants et locaux courts, et les noms peu courants et non locaux plus longs](010-expr.md#res-name-length)
* [ES.8 : Éviter les noms qui se ressemblent](010-expr.md#res-name-similar)
* [ES.9 : Éviter les noms en `MAJUSCULES`](010-expr.md#res-not-caps)
* [ES.10 : Déclarer un seul nom (uniquement) par déclaration](010-expr.md#res-name-one)
* [ES.11 : Utiliser `auto` pour éviter la répétition redondante de noms de types](010-expr.md#res-auto)
* [ES.12 : Ne pas réutiliser des noms dans des étendues imbriquées](010-expr.md#res-reuse)
* [ES.20 : Toujours initialiser un objet](010-expr.md#res-always)
* [ES.21 : Ne pas introduire une variable (ou constante) avant d'en avoir besoin](010-expr.md#res-introduce)
* [ES.22 : Ne pas déclarer une variable tant qu'on n'a pas de valeur pour l'initialiser](010-expr.md#res-init)
* [ES.23 : Privilégier la syntaxe d'initialisation `{}`](010-expr.md#res-list)
* [ES.24 : Utiliser un `unique_ptr<T>` pour détenir des pointeurs](010-expr.md#res-unique)
* [ES.25 : Déclarer un objet `const` ou `constexpr` sauf si on souhaite modifier sa valeur plus tard](010-expr.md#res-const)
* [ES.26 : Ne pas utiliser une variable à deux fins non liées](010-expr.md#res-recycle)
* [ES.27 : Utiliser `std::array` ou `stack_array` pour les tableaux sur la pile](010-expr.md#res-stack)
* [ES.28 : Utiliser des lambdas pour les initialisations complexes, en particulier de variables `const`](010-expr.md#res-lambda-init)
* [ES.30 : Ne pas utiliser de macros pour la manipulation du texte du programme](010-expr.md#res-macros)
* [ES.31 : Ne pas utiliser de macros pour des constantes ou des « fonctions »](010-expr.md#res-macros2)
* [ES.32 : Utiliser `MAJUSCULES` pour tous les noms de macros](010-expr.md#res-all_caps)
* [ES.33 : Si vous devez utiliser des macros, donnez-leur des noms uniques](010-expr.md#res-macros3)
* [ES.34 : Ne pas définir de fonction variable (style C)](010-expr.md#res-ellipses)

Règles d'expression :

* [ES.40 : Éviter les expressions compliquées](010-expr.md#res-complicated)
* [ES.41 : En cas de doute sur la priorité des opérateurs, utiliser des parenthèses](010-expr.md#res-parens)
* [ES.42 : Garder l'utilisation des pointeurs simple et directe](010-expr.md#res-ptr)
* [ES.43 : Éviter les expressions avec un ordre d'évaluation indéfini](010-expr.md#res-order)
* [ES.44 : Ne pas dépendre de l'ordre d'évaluation des arguments de fonction](010-expr.md#res-order-fct)
* [ES.45 : Éviter les « constantes magiques » ; utiliser des constantes symboliques](010-expr.md#res-magic)
* [ES.46 : Éviter les conversions rétrécissantes (narrowing)](010-expr.md#res-narrowing)
* [ES.47 : Utiliser `nullptr` plutôt que `0` ou `NULL`](010-expr.md#res-nullptr)
* [ES.48 : Éviter les casts](010-expr.md#res-casts)
* [ES.49 : Si vous devez utiliser un cast, utiliser un cast nommé](010-expr.md#res-casts-named)
* [ES.50 : Ne pas supprimer le `const`](010-expr.md#res-casts-const)
* [ES.55 : Éviter le besoin de vérification de plage](010-expr.md#res-range-checking)
* [ES.56 : Écrire `std::move()` uniquement quand vous devez explicitement déplacer un objet vers une autre étendue](010-expr.md#res-move)
* [ES.60 : Éviter `new` et `delete` en dehors des fonctions de gestion de ressources](010-expr.md#res-new)
* [ES.61 : Supprimer les tableaux avec `delete[]` et les non-tableaux avec `delete`](010-expr.md#res-del)
* [ES.62 : Ne pas comparer des pointeurs vers des tableaux différents](010-expr.md#res-arr2)
* [ES.63 : Ne pas faire de troncature d'objet (slicing)](010-expr.md#res-slice)
* [ES.64 : Utiliser la notation `T{e}` pour la construction](010-expr.md#res-construct)
* [ES.65 : Ne pas déréférencer un pointeur invalide](010-expr.md#res-deref)

Règles de déclaration (statements) :

* [ES.70 : Privilégier une instruction `switch` à une instruction `if` quand il y a un choix](010-expr.md#res-switch-if)
* [ES.71 : Privilégier une boucle `for` par plage à une boucle `for` quand il y a un choix](010-expr.md#res-for-range)
* [ES.72 : Privilégier une boucle `for` à une boucle `while` quand il y a une variable de boucle évidente](010-expr.md#res-for-while)
* [ES.73 : Privilégier une boucle `while` à une boucle `for` quand il n'y a pas de variable de boucle évidente](010-expr.md#res-while-for)
* [ES.74 : Privilégier la déclaration d'une variable de boucle dans la partie initialisatrice d'une boucle `for`](010-expr.md#res-for-init)
* [ES.75 : Éviter les instructions `do`](010-expr.md#res-do)
* [ES.76 : Éviter `goto`](010-expr.md#res-goto)
* [ES.77 : Minimiser l'utilisation de `break` et `continue` dans les boucles](010-expr.md#res-continue)
* [ES.78 : Ne pas compter sur le passage implicite (fallthrough) dans les instructions `switch`](010-expr.md#res-break)
* [ES.79 : Utiliser `default` pour traiter les cas courants (uniquement)](010-expr.md#res-default)
* [ES.84 : Ne pas essayer de déclarer une variable locale sans nom](010-expr.md#res-noname)
* [ES.85 : Rendre les déclarations vides visibles](010-expr.md#res-empty)
* [ES.86 : Éviter de modifier les variables de contrôle de boucle dans le corps de boucles for brutes](010-expr.md#res-loop-counter)
* [ES.87 : Ne pas ajouter de `==` ou `!=` redondants aux conditions](010-expr.md#res-if)

Règles arithmétiques :

* [ES.100 : Ne pas mélanger l'arithmétique signée et non signée](010-expr.md#res-mix)
* [ES.101 : Utiliser des types non signés pour la manipulation de bits](010-expr.md#res-unsigned)
* [ES.102 : Utiliser des types signés pour l'arithmétique](010-expr.md#res-signed)
* [ES.103 : Ne pas déborder (overflow)](010-expr.md#res-overflow)
* [ES.104 : Ne pas sous-déborder (underflow)](010-expr.md#res-underflow)
* [ES.105 : Ne pas diviser par zéro (entier)](010-expr.md#res-zero)
* [ES.106 : Ne pas essayer d'éviter les valeurs négatives en utilisant `unsigned`](010-expr.md#res-nonnegative)
* [ES.107 : Ne pas utiliser `unsigned` pour les index, privilégier `gsl::index`](010-expr.md#res-subscripts)

### <a name="res-lib"></a>ES.1 : Privilégier la bibliothèque standard aux autres bibliothèques et au « code artisanal »

##### Raison

Un code utilisant une bibliothèque peut être beaucoup plus facile à écrire qu'un code travaillant directement avec les fonctionnalités du langage, beaucoup plus court, tend à être à un niveau d'abstraction plus élevé, et le code de la bibliothèque est présumé déjà testé.
La bibliothèque standard ISO C++ est parmi les bibliothèques les plus connues et les mieux testées.
Elle est disponible dans le cadre de toutes les implémentations C++.

##### Exemple

    auto sum = accumulate(begin(a), end(a), 0.0);   // bon

Une version par plage d'`accumulate` serait encore meilleure :

    auto sum = accumulate(v, 0.0); // meilleur

mais ne pas coder à la main un algorithme bien connu :

    int max = v.size();   // mauvais : verbeux, but non explicité
    double sum = 0.0;
    for (int i = 0; i < max; ++i)
        sum = sum + v[i];

##### Exception

De grandes parties de la bibliothèque standard reposent sur l'allocation dynamique (mémoire libre). Ces parties, notamment les conteneurs mais pas les algorithmes, sont inadaptées à certaines applications temps réel dur et embarquées. Dans de tels cas, envisagez de fournir/utiliser des facilités similaires, par exemple un conteneur de style bibliothèque standard implémenté avec un allocateur par pool.

##### Application

Pas facile. ??? Rechercher des boucles désordonnées, des boucles imbriquées, des fonctions longues, l'absence d'appels de fonctions, le manque d'utilisation de types intégrés. Complexité cyclomatique ?

### <a name="res-abstr"></a>ES.2 : Privilégier des abstractions appropriées à l'utilisation directe des fonctionnalités du langage

##### Raison

Une « abstraction appropriée » (par ex. une bibliothèque ou une classe) est plus proche des concepts de l'application que le langage brut, conduit à un code plus court et plus clair, et est susceptible d'être mieux testée.

##### Exemple

    vector<string> read1(istream& is)   // bon
    {
        vector<string> res;
        for (string s; is >> s;)
            res.push_back(s);
        return res;
    }

L'équivalent plus traditionnel et de plus bas niveau est plus long, plus désordonné, plus difficile à faire correctement, et probablement plus lent :

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

Une fois les vérifications de débordement et la gestion des erreurs ajoutées, ce code devient assez désordonné, et il y a le problème de se souvenir de `delete` le pointeur retourné et les chaînes de caractères style C que ce tableau contient.

##### Application

Pas facile. ??? Rechercher des boucles désordonnées, des boucles imbriquées, des fonctions longues, l'absence d'appels de fonctions, le manque d'utilisation de types intégrés. Complexité cyclomatique ?

### <a name="res-dry"></a>ES.3 : Ne pas se répéter, éviter le code redondant

Le code dupliqué ou autrement redondant obscurcit l'intention, rend la logique plus difficile à comprendre, et rend la maintenance plus difficile, entre autres problèmes. Il survient souvent de la programmation par copier-coller.

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

Une déclaration est une instruction (statement). Une déclaration introduit un nom dans une étendue et peut provoquer la construction d'un objet nommé.

### <a name="res-scope"></a>ES.5 : Garder les étendues (scopes) petites

##### Raison

Lisibilité. Minimiser la rétention de ressources. Éviter l'utilisation accidentelle d'une valeur.

**Formulation alternative** : Ne pas déclarer un nom dans une étendue inutilement grande.

##### Exemple

    void use()
    {
        int i;    // mauvais : i est inutilement accessible après la boucle
        for (i = 0; i < 20; ++i) { /* ... */ }
        // pas d'utilisation prévue de i ici
        for (int i = 0; i < 20; ++i) { /* ... */ }  // bon : i est local à la boucle for

        if (auto pc = dynamic_cast<Circle*>(ps)) {  // bon : pc est local à l'instruction if
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

Cette fonction est de toute façon trop longue selon la plupart des mesures, mais le point est que les ressources utilisées par `fn` et le descripteur de fichier détenu par `is`
sont retenues bien plus longtemps que nécessaire et qu'une utilisation inattendue de `is` et `fn` pourrait se produire plus tard dans la fonction.
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
* Signaler quand des ressources coûteuses, telles que des descripteurs de fichiers et des verrous, ne sont pas utilisées pendant N lignes (pour un N approprié)

### <a name="res-cond"></a>ES.6 : Déclarer les noms dans les initialisateurs et les conditions des boucles for pour limiter l'étendue

##### Raison

Lisibilité.
Limiter la visibilité de la variable de boucle à l'étendue de la boucle.
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

        if (auto pc = dynamic_cast<Circle*>(ps)) {   // bon : pc est local à l'instruction if
            // ... gérer Circle ...
        }
        else {
            // ... gérer l'erreur ...
        }
    }

##### Exemple, à éviter

    int j;                            // MAUVAIS : j est visible en dehors de la boucle
    for (j = 0; j < 100; ++j) {
        // ...
    }
    // j est toujours visible ici et n'est pas nécessaire

**Voir aussi** : [Ne pas utiliser une variable à deux fins non liées](010-expr.md#res-recycle)

##### Application

* Avertir quand une variable modifiée dans la boucle `for` est déclarée en dehors de la boucle et n'est pas utilisée en dehors de la boucle.
* (difficile) Signaler les variables de boucle déclarées avant la boucle et utilisées après la boucle à une fin non liée.

**Discussion** : Limiter l'étendue de la variable de boucle au corps de la boucle aide aussi grandement les optimiseurs de code. Reconnaître que la variable d'induction
n'est accessible que dans le corps de la boucle débloque des optimisations telles que le hoisting, la réduction de force, le déplacement de code invariant de boucle, etc.

##### Exemple C++17 et C++20

Note : C++17 et C++20 ajoutent également des instructions d'initialisation `if`, `switch` et `for` par plage. Ces fonctionnalités nécessitent le support de C++17 et C++20.

    map<int, string> mymap;

    if (auto result = mymap.insert(value); result.second) {
        // l'insertion a réussi, et result est valide pour ce bloc
        use(result.first);  // ok
        // ...
    } // result est détruit ici

##### Application C++17 et C++20 (si vous utilisez un compilateur C++17 ou C++20)

* Signaler les variables de sélection/boucle déclarées avant le corps et non utilisées après le corps
* (difficile) Signaler les variables de sélection/boucle déclarées avant le corps et utilisées après le corps à une fin non liée.

### <a name="res-name-length"></a>ES.7 : Garder les noms courants et locaux courts, et les noms peu courants et non locaux plus longs

##### Raison

Lisibilité. Réduire la probabilité de collisions entre noms non locaux non liés.

##### Exemple

Des noms courts et locaux conventionnels augmentent la lisibilité :

    template<typename T>    // bon
    void print(ostream& os, const vector<T>& v)
    {
        for (gsl::index i = 0; i < v.size(); ++i)
            os << v[i] << '\n';
    }

Un index est conventionnellement appelé `i` et il n'y a aucun indice sur la signification du vecteur dans cette fonction générique, donc `v` est aussi bon nom qu'un autre. Comparez avec

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

Mieux, donner des noms lisibles aux entités non locales :

    void use1(const string& s)
    {
        // ...
        trim_tail(s);   // meilleur
        // ...
    }

Ici, il y a une chance que le lecteur sache ce que signifie `trim_tail` et que le lecteur puisse s'en souvenir après l'avoir consulté.

##### Exemple, mauvais

Les noms d'arguments de grandes fonctions sont de facto non locaux et devraient être significatifs :

    void complicated_algorithm(vector<Record>& vr, const vector<int>& vi, map<string, int>& out)
    // lire depuis les événements dans vr (en marquant les Records utilisés) pour les indices dans
    // vi en plaçant des paires (nom, index) dans out
    {
        // ... 500 lignes de code utilisant vr, vi, et out ...
    }

Nous recommandons de garder les fonctions courtes, mais cette règle n'est pas universellement respectée et le nommage devrait en tenir compte.

##### Application

Vérifier la longueur des noms locaux et non locaux. Tenir aussi compte de la longueur de la fonction.

### <a name="res-name-similar"></a>ES.8 : Éviter les noms qui se ressemblent

##### Raison

Clarté et lisibilité du code. Des noms trop similaires ralentissent la compréhension et augmentent la probabilité d'erreurs.

##### Exemple, mauvais

    if (readable(i1 + l1 + ol + o1 + o0 + ol + o1 + I0 + l0)) surprise();

##### Exemple, mauvais

Ne pas déclarer un non-type avec le même nom qu'un type dans la même étendue. Cela supprime le besoin de désambiguïser avec un mot-clé tel que `struct` ou `enum`. Cela supprime aussi une source d'erreurs, car `struct X` peut implicitement déclarer `X` si la recherche échoue.

    struct foo { int n; };
    struct foo foo();       // MAUVAIS, foo est déjà un type dans l'étendue
    struct foo x = foo();   // nécessite une désambiguïsation

##### Exception

Les fichiers d'en-tête anciens pourraient déclarer des non-types et des types avec le même nom dans la même étendue.

##### Application

* Vérifier les noms contre une liste de combinaisons connues de lettres et de chiffres confondus.
* Signaler la déclaration d'une variable, d'une fonction ou d'un énumérateur qui masque une classe ou une énumération déclarée dans la même étendue.

### <a name="res-not-caps"></a>ES.9 : Éviter les noms en `MAJUSCULES`

##### Raison

De tels noms sont couramment utilisés pour les macros. Ainsi, un nom en `MAJUSCULES` est vulnérable à une substitution de macro non intentionnelle.

##### Exemple

    // quelque part dans un en-tête :
    #define NE !=

    // quelque part dans un autre en-tête :
    enum Coord { N, NE, NW, S, SE, SW, E, W };

    // quelque part ailleurs dans le .cpp d'un pauvre programmeur :
    switch (direction) {
    case N:
        // ...
    case NE:
        // ...
    // ...
    }

##### Note

Ne pas utiliser `MAJUSCULES` pour des constantes simplement parce que les constantes étaient autrefois des macros.

##### Application

Signaler toutes les utilisations de MAJUSCULES. Pour le code ancien, accepter les MAJUSCULES pour les noms de macros et signaler tous les noms de macros non en MAJUSCULES.

### <a name="res-name-one"></a>ES.10 : Déclarer un seul nom (uniquement) par déclaration

##### Raison

Une déclaration par ligne augmente la lisibilité et évite les erreurs liées à
la grammaire C/C++. Cela laisse aussi de la place pour un commentaire de fin de ligne
plus descriptif.

##### Exemple, mauvais

    char *p, c, a[7], *pp[7], **aa[10];   // beurk !

##### Exception

Une déclaration de fonction peut contenir plusieurs déclarations d'arguments de fonction.

##### Exception

Un lienage structuré (C++17) est spécifiquement conçu pour introduire plusieurs variables :

    auto [iter, inserted] = m.insert_or_assign(k, val);
    if (inserted) { /* une nouvelle entrée a été insérée */ }

##### Exemple

    template<class InputIterator, class Predicate>
    bool any_of(InputIterator first, InputIterator last, Predicate pred);

ou mieux en utilisant les concepts :

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

Dans une longue liste de déclarateurs, il est facile de manquer une variable non initialisée.

##### Application

Signaler les déclarations de variables et de constantes avec plusieurs déclarateurs (par ex. `int* p, q;`)

### <a name="res-auto"></a>ES.11 : Utiliser `auto` pour éviter la répétition redondante de noms de types

##### Raison

* La répétition simple est fastidieuse et source d'erreurs.
* Quand vous utilisez `auto`, le nom de l'entité déclarée est à une position fixe dans la déclaration, augmentant la lisibilité.
* Dans une déclaration de fonction template, le type de retour peut être un type membre.

##### Exemple

Considérons :

    auto p = v.begin();      // vector<DataRecord>::iterator
    auto z1 = v[3];          // fait une copie de DataRecord
    auto& z2 = v[3];         // évite la copie
    const auto& z3 = v[3];   // const et évite la copie
    auto h = t.future();
    auto q = make_unique<int[]>(s);
    auto f = [](int x) { return x + 10; };

Dans chaque cas, nous évitons d'écrire un type long et difficile à retenir que le compilateur connaît déjà mais qu'un programmeur pourrait mal écrire.

##### Exemple

    template<class T>
    auto Container<T>::first() -> Iterator;   // Container<T>::Iterator

##### Exception

Éviter `auto` pour les listes d'initialisation et dans les cas où vous savez exactement quel type vous voulez et où un initialiseur pourrait nécessiter une conversion.

##### Exemple

    auto lst = { 1, 2, 3 };   // lst est une liste d'initialisation
    auto x{1};   // x est un int (en C++17 ; initializer_list en C++11)

##### Note

Depuis C++20, nous pouvons (et devrions) utiliser les concepts pour être plus précis sur le type que nous déduisons :

    // ...
    forward_iterator auto p = algo(x, y, z);

##### Exemple (C++17)

    std::set<int> values;
    // ...
    auto [ position, newly_inserted ] = values.insert(5);   // décomposer les membres du std::pair

##### Application

Signaler la répétition redondante de noms de types dans une déclaration.

### <a name="res-reuse"></a>ES.12 : Ne pas réutiliser des noms dans des étendues imbriquées

##### Raison

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

Si c'est une grande instruction `if`, il est facile de manquer qu'un nouveau `d` a été introduit dans l'étendue interne.
C'est une source connue de bugs.
Parfois, cette réutilisation d'un nom dans une étendue interne est appelée « shadowing ».

##### Note

Le shadowing est principalement un problème quand les fonctions sont trop grandes et trop complexes.

##### Exemple

Le shadowing d'arguments de fonction dans le bloc le plus externe est interdit par le langage :

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
        m = 7;    // assignation au membre
        if (x) {
            int m = 9;
            // ...
            m = 99; // assignation à la variable locale
            // ...
        }
    }

##### Exception

Nous réutilisons souvent les noms de fonctions d'une classe de base dans une classe dérivée :

    struct B {
        void f(int);
    };

    struct D : B {
        void f(double);
        using B::f;
    };

Cela est source d'erreurs.
Par exemple, si nous avions oublié la déclaration using, un appel `d.f(1)` n'aurait pas trouvé la version `int` de `f`.

??? Avons-nous besoin d'une règle spécifique sur le shadowing/hiding dans les hiérarchies de classes ?

##### Application

* Signaler la réutilisation d'un nom dans des étendues locales imbriquées
* Signaler la réutilisation d'un nom de membre comme variable locale dans une fonction membre
* Signaler la réutilisation d'un nom global comme variable locale ou nom de membre
* Signaler la réutilisation d'un nom de membre de classe de base dans une classe dérivée (sauf pour les noms de fonctions)

### <a name="res-always"></a>ES.20 : Toujours initialiser un objet

##### Raison

Éviter les erreurs d'utilisation avant initialisation et leur comportement indéfini associé.
Éviter les problèmes de compréhension d'initialisations complexes.
Simplifier le refactoring.

##### Exemple

    void use(int arg)
    {
        int i;   // mauvais : variable non initialisée
        // ...
        i = 7;   // initialiser i
    }

Non, `i = 7` n'initialise pas `i` ; c'est une assignation. De plus, `i` peut être lu dans la partie `...`. Mieux :

    void use(int arg)   // OK
    {
        int i = 7;   // OK : initialisé
        string s;    // OK : initialisé par défaut
        // ...
    }

##### Note

La règle *toujours initialiser* est délibérément plus stricte que la règle du langage *un objet doit être initialisé avant d'être utilisé*.
Cette dernière, plus souple, détecte les bugs techniques, mais :

* Elle conduit à un code moins lisible
* Elle encourage les gens à déclarer des noms dans des étendues plus grandes que nécessaire
* Elle conduit à un code plus difficile à lire
* Elle conduit à des bugs logiques en encourageant un code complexe
* Elle entrave le refactoring

La règle *toujours initialiser* est une règle de style visant à améliorer la maintenabilité ainsi qu'une règle protégeant contre les erreurs d'utilisation avant initialisation.

##### Exemple

Voici un exemple souvent considéré comme démontrant le besoin d'une règle plus souple pour l'initialisation

    widget i;    // "widget" un type coûteux à initialiser, possiblement un grand type trivial
    widget j;

    if (cond) {  // mauvais : i et j sont initialisés « tard »
        i = f1();
        j = f2();
    }
    else {
        i = f3();
        j = f4();
    }

Cela ne peut pas être trivialement réécrit pour initialiser `i` et `j` avec des initialiseurs.
Notez que pour les types avec un constructeur par défaut, essayer de reporter l'initialisation conduit simplement à une initialisation par défaut suivie d'une assignation.
Une raison populaire pour de tels exemples est l'« efficacité », mais un compilateur capable de détecter si nous avons fait une erreur d'utilisation avant initialisation peut aussi éliminer toute double initialisation redondante.

En supposant qu'il y a un lien logique entre `i` et `j`, ce lien devrait probablement être exprimé dans le code :

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
    use(i);         // possiblement utilisé avant initialisation
    // ...

    if (cond) {     // mauvais : i et j sont initialisés « tard »
        i = f1();
        j = f2();
    }
    else {
        i = f3();
        j = f4();
    }

Maintenant, le compilateur ne peut même pas simplement détecter une utilisation avant initialisation. De plus, nous avons introduit de la complexité dans l'espace d'états pour widget : quelles opérations sont valides sur un widget `uninit` et lesquelles ne le sont pas ?

##### Note

L'initialisation complexe a été populaire chez les programmeurs ingénieux depuis des décennies.
Cela a aussi été une source majeure d'erreurs et de complexité.
Beaucoup de ces erreurs sont introduites lors de la maintenance des années après l'implémentation initiale.

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

Le compilateur signalera le `cm3` non initialisé parce qu'il est `const`, mais il ne détectera pas le manque d'initialisation de `m3`.
Habituellement, une initialisation rare et superflue de membre vaut l'absence d'erreurs dues au manque d'initialisation et souvent un optimiseur
peut éliminer une initialisation redondante (par ex. une initialisation qui se produit juste avant une assignation).

##### Exception

Si vous déclarez un objet qui va juste être initialisé depuis une entrée, l'initialiser causerait une double initialisation.
Cependant, attention que cela pourrait laisser des données non initialisées au-delà de l'entrée -- et cela a été une source fertile d'erreurs et de failles de sécurité :

    constexpr int max = 8 * 1024;
    int buf[max];         // OK, mais suspect : non initialisé
    f.read(buf, max);

Le coût d'initialisation de ce tableau pourrait être significatif dans certaines situations.
Cependant, de tels exemples ont tendance à laisser des variables non initialisées accessibles, donc ils devraient être traités avec suspicion.

    constexpr int max = 8 * 1024;
    int buf[max] = {};   // zéro tous les éléments ; meilleur dans certaines situations
    f.read(buf, max);

À cause des règles restrictives d'initialisation pour les tableaux et `std::array`, ils offrent les exemples les plus convaincants du besoin de cette exception.

Quand c'est faisable, utiliser une fonction de bibliothèque connue pour ne pas déborder. Par exemple :

    string s;   // s est initialisé par défaut à ""
    cin >> s;   // s s'agrandit pour contenir la chaîne

Ne pas considérer les variables simples qui sont des cibles d'opérations d'entrée comme des exceptions à cette règle :

    int i;   // mauvais
    // ...
    cin >> i;

Dans le cas non rare où la cible d'entrée et l'opération d'entrée se séparent (comme elles ne devraient pas), la possibilité d'utilisation avant initialisation s'ouvre.

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

* Signaler toute variable non initialisée.
  Ne pas signaler les variables de types définis par l'utilisateur avec des constructeurs par défaut.
* Vérifier qu'un tampon non initialisé est écrit *immédiatement* après la déclaration.
  Passer une variable non initialisée comme référence à un argument non-`const` peut être supposé être une écriture dans la variable.

### <a name="res-introduce"></a>ES.21 : Ne pas introduire une variable (ou constante) avant d'en avoir besoin

##### Raison

Lisibilité. Limiter l'étendue dans laquelle la variable peut être utilisée.

##### Exemple

    int x = 7;
    // ... pas d'utilisation de x ici ...
    ++x;

##### Application

Signaler les déclarations qui sont éloignées de leur première utilisation.

### <a name="res-init"></a>ES.22 : Ne pas déclarer une variable tant qu'on n'a pas de valeur pour l'initialiser

##### Raison

Lisibilité. Limiter l'étendue dans laquelle une variable peut être utilisée. Ne pas risquer une utilisation avant initialisation. L'initialisation est souvent plus efficace que l'assignation.

##### Exemple, mauvais

    string s;
    // ... pas d'utilisation de s ici ...
    s = "what a waste";

##### Exemple, mauvais

    SomeLargeType var;  // CaMeLcAsEvArIaBlE difficile à lire

    if (cond)   // une condition non triviale
        Set(&var);
    else if (cond2 || !cond3) {
        var = Set2(3.14);
    }
    else {
        var = 0;
        for (auto& e : something)
            var += e;
    }

    // utiliser var ; que cela ne soit pas fait trop tôt peut être appliqué statiquement avec seulement le flux de contrôle

Cela serait acceptable s'il y avait une initialisation par défaut pour `SomeLargeType` qui n'était pas trop coûteuse.
Sinon, un programmeur pourrait très bien se demander si tous les chemins possibles à travers le labyrinthe de conditions ont été couverts.
Si ce n'est pas le cas, nous avons un bug « utilisation avant initialisation ». C'est un piège de maintenance.

Pour des initialiseurs de complexité modérée, y compris pour des variables `const`, envisagez d'utiliser une lambda pour exprimer l'initialiseur ; voir [ES.28](010-expr.md#res-lambda-init).

##### Application

* Signaler les déclarations avec initialisation par défaut qui sont assignées avant d'être lues pour la première fois.
* Signaler tout calcul compliqué après une variable non initialisée et avant son utilisation.

### <a name="res-list"></a>ES.23 : Privilégier la syntaxe d'initialisation `{}`

##### Raison

Privilégier `{}`. Les règles pour l'initialisation `{}` sont plus simples, plus générales, moins ambiguës et plus sûres que pour d'autres formes d'initialisation.

Utiliser `=` uniquement quand vous êtes sûr qu'il ne peut y avoir aucune conversion rétrécissante. Pour les types arithmétiques intégrés, utiliser `=` uniquement avec `auto`.

Éviter l'initialisation `()`, qui permet des ambiguïtés d'analyse.

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

L'initialisation `{}` peut être utilisée pour presque toutes les initialisations ; d'autres formes d'initialisation ne le peuvent pas :

    auto p = new vector<int> {1, 2, 3, 4, 5};   // vecteur initialisé
    D::D(int a, int b) :m{a, b} {   // initialiseur de membre (par ex. m pourrait être un pair)
        // ...
    };
    X var {};   // initialiser var à vide
    struct S {
        int m {7};   // initialiseur par défaut pour un membre
        // ...
    };

Pour cette raison, l'initialisation `{}` est souvent appelée « initialisation uniforme »
(bien qu'il y ait malheureusement quelques irrégularités restantes).

##### Note

L'initialisation d'une variable déclarée avec `auto` avec une seule valeur, par ex. `{v}`, avait des résultats surprenants jusqu'à C++17.
Les règles C++17 sont un peu moins surprenantes :

    auto x1 {7};        // x1 est un int avec la valeur 7
    auto x2 = {7};      // x2 est un initializer_list<int> avec un élément 7

    auto x11 {7, 8};    // erreur : deux initialiseurs
    auto x22 = {7, 8};  // x22 est un initializer_list<int> avec les éléments 7 et 8

Utiliser `={...}` si vous voulez vraiment un `initializer_list<T>`

    auto fib10 = {1, 1, 2, 3, 5, 8, 13, 21, 34, 55};   // fib10 est une liste

##### Note

`={}` donne une initialisation par copie alors que `{}` donne une initialisation directe.
Comme la distinction entre initialisation par copie et initialisation directe elle-même, cela peut conduire à des surprises.
`{}` accepte les constructeurs `explicit` ; `={}` ne le fait pas. Par exemple :

    struct Z { explicit Z() {} };

    Z z1{};     // OK : initialisation directe, donc nous utilisons le constructeur explicit
    Z z2 = {};  // erreur : initialisation par copie, donc nous ne pouvons pas utiliser le constructeur explicit

Utiliser l'initialisation `{}` simple à moins que vous ne vouliez spécifiquement désactiver les constructeurs explicites.

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
* Signaler les utilisations de la syntaxe d'initialisation `()` qui sont en réalité des déclarations. (Beaucoup de compilateurs devraient déjà avertir de cela.)

### <a name="res-unique"></a>ES.24 : Utiliser un `unique_ptr<T>` pour détenir des pointeurs

##### Raison

L'utilisation de `std::unique_ptr` est le moyen le plus simple d'éviter les fuites. C'est fiable, il
laisse le système de types faire beaucoup du travail pour valider la sécurité de la propriété, il
augmente la lisibilité, et il a un coût d'exécution nul ou quasi nul.

##### Exemple

    void use(bool leak)
    {
        auto p1 = make_unique<int>(7);   // OK
        int* p2 = new int{7};            // mauvais : pourrait fuir
        // ... pas d'assignation à p2 ...
        if (leak) return;
        // ... pas d'assignation à p2 ...
        vector<int> v(7);
        v.at(7) = 0;                    // exception levée
        delete p2;                      // trop tard pour prévenir les fuites
        // ...
    }

Si `leak == true`, l'objet pointé par `p2` fuit et l'objet pointé par `p1` ne fuit pas.
C'est le même cas quand `at()` lève une exception. Dans les deux cas, l'instruction `delete p2` n'est pas atteinte.

##### Application

Rechercher des pointeurs bruts qui sont des cibles de `new`, `malloc()`, ou de fonctions qui pourraient retourner de tels pointeurs.

### <a name="res-const"></a>ES.25 : Déclarer un objet `const` ou `constexpr` sauf si vous souhaitez modifier sa valeur plus tard

##### Raison

De cette façon, vous ne pouvez pas changer la valeur par accident. De cette façon, vous pourriez offrir au compilateur des opportunités d'optimisation.

##### Exemple

    void f(int n)
    {
        const int bufmax = 2 * n + 2;  // bon : nous ne pouvons pas changer bufmax par accident
        int xmax = n;                  // suspect : xmax est-il censé changer ?
        // ...
    }

##### Application

Vérifier si une variable est effectivement modifiée, et la signaler si
non. Malheureusement, il peut être impossible de détecter quand un non-`const` n'était pas
*censé* varier (par opposition au fait qu'il n'a simplement pas varié).

### <a name="res-recycle"></a>ES.26 : Ne pas utiliser une variable à deux fins non liées

##### Raison

Lisibilité et sécurité.

##### Exemple, mauvais

    void use()
    {
        int i;
        for (i = 0; i < 20; ++i) { /* ... */ }
        for (i = 0; i < 200; ++i) { /* ... */ } // mauvais : i réutilisé
    }

##### Note

En tant qu'optimisation, vous pourriez vouloir réutiliser un tampon comme zone de travail, mais même dans ce cas, préférez limiter l'étendue de la variable autant que possible et faites attention à ne pas causer de bugs à partir de données laissées dans un tampon réutilisé, car c'est une source commune de bugs de sécurité.

    void write_to_file()
    {
        std::string buffer;             // pour éviter les réallocations à chaque itération de boucle
        for (auto& o : objects) {
            // Première partie du travail.
            generate_first_string(buffer, o);
            write_to_file(buffer);

            // Deuxième partie du travail.
            generate_second_string(buffer, o);
            write_to_file(buffer);

            // etc...
        }
    }

##### Application

Signaler les variables réutilisées.

### <a name="res-stack"></a>ES.27 : Utiliser `std::array` ou `stack_array` pour les tableaux sur la pile

##### Raison

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

La définition de `a1` est du C++ légal et l'a toujours été.
Il y a beaucoup de tel code.
Cependant, c'est source d'erreurs, surtout quand la borne est non locale.
De plus, c'est une source « populaire » d'erreurs (débordement de tampon, pointeurs par décadence de tableau, etc.).
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

* Signaler les tableaux avec des bornes non constantes (VLAs style C)
* Signaler les tableaux avec des bornes constantes non locales

### <a name="res-lambda-init"></a>ES.28 : Utiliser des lambdas pour les initialisations complexes, en particulier de variables `const`

##### Raison

Cela encapsule proprement l'initialisation locale, y compris le nettoyage des variables temporaires nécessaires uniquement pour l'initialisation, sans avoir besoin de créer une fonction non locale inutilement non réutilisable. Cela fonctionne aussi pour les variables qui devraient être `const` mais seulement après un travail d'initialisation.

##### Exemple, mauvais

    widget x;   // devrait être const, mais :
    for (auto i = 2; i <= N; ++i) {          // cela pourrait être un
        x += some_obj.do_something_with(i);  // code arbitrairement long
    }                                        // nécessaire pour initialiser x
    // d'ici, x devrait être const, mais nous ne pouvons pas le dire dans le code dans ce style

##### Exemple, bon

    const widget x = [&] {
        widget val;                                // supposons que widget a un constructeur par défaut
        for (auto i = 2; i <= N; ++i) {            // cela pourrait être un
            val += some_obj.do_something_with(i);  // code arbitrairement long
        }                                          // nécessaire pour initialiser x
        return val;
    }();

Si possible, réduire les conditions à un simple ensemble d'alternatives (par ex. un `enum`) et ne pas mélanger sélection et initialisation.

##### Application

Difficile. Au mieux une heuristique. Rechercher une variable non initialisée suivie d'une boucle qui lui assigne.

### <a name="res-macros"></a>ES.30 : Ne pas utiliser de macros pour la manipulation du texte du programme

##### Raison

Les macros sont une source majeure de bugs.
Les macros n'obéissent pas aux règles habituelles d'étendue et de type.
Les macros garantissent que le lecteur humain voit quelque chose de différent de ce que le compilateur voit.
Les macros compliquent la construction d'outils.

##### Exemple, mauvais

    #define Case break; case   /* MAUVAIS */

Cette macro qui semble inoffensive transforme un simple `c` minuscule au lieu d'un `C` en un bug de contrôle de flux.

##### Note

Cette règle n'interdit pas l'utilisation de macros pour le « contrôle de configuration » dans les `#ifdef`, etc.

À l'avenir, les modules sont susceptibles d'éliminer le besoin de macros dans le contrôle de configuration.

##### Note

Cette règle vise aussi à décourager l'utilisation de `#` pour la stringification et `##` pour la concaténation.
Comme d'habitude pour les macros, il y a des utilisations « principalement inoffensives », mais même celles-ci peuvent créer des problèmes pour les outils,
tels que les compléteurs automatiques, les analyseurs statiques, et les débogueurs.
Souvent, le désir d'utiliser des macros sophistiquées est un signe d'une conception trop complexe.
De plus, `#` et `##` encouragent la définition et l'utilisation de macros :

    #define CAT(a, b) a ## b
    #define STRINGIFY(a) #a

    void f(int x, int y)
    {
        string CAT(x, y) = "asdf";   // MAUVAIS : difficile pour les outils (et laid)
        string sx2 = STRINGIFY(x);
        // ...
    }

Il existe des solutions de contournement pour la manipulation de chaînes de bas niveau en utilisant des macros. Par exemple :

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

Cela n'est pas aussi pratique qu'une macro à définir, mais aussi facile à utiliser, a un coût nul, et est typé et étendu.

À l'avenir, la réflexion statique est susceptible d'éliminer les derniers besoins du préprocesseur pour la manipulation du texte du programme.

##### Application

Crier quand on voit une macro qui n'est pas simplement utilisée pour le contrôle de source (par ex. `#ifdef`)

### <a name="res-macros2"></a>ES.31 : Ne pas utiliser de macros pour des constantes ou des « fonctions »

##### Raison

Les macros sont une source majeure de bugs.
Les macros n'obéissent pas aux règles habituelles d'étendue et de type.
Les macros n'obéissent pas aux règles habituelles de passage d'arguments.
Les macros garantissent que le lecteur humain voit quelque chose de différent de ce que le compilateur voit.
Les macros compliquent la construction d'outils.

##### Exemple, mauvais

    #define PI 3.14
    #define SQUARE(a, b) (a * b)

Même si nous n'avions pas laissé un bug bien connu dans `SQUARE`, il existe des alternatives beaucoup mieux comportées ; par exemple :

    constexpr double pi = 3.14;
    template<typename T> T square(T a, T b) { return a * b; }

##### Application

Crier quand on voit une macro qui n'est pas simplement utilisée pour le contrôle de source (par ex. `#ifdef`)

### <a name="res-all_caps"></a>ES.32 : Utiliser `MAJUSCULES` pour tous les noms de macros

##### Raison

Convention. Lisibilité. Distinction des macros.

##### Exemple

    #define forever for (;;)   /* très MAUVAIS */

    #define FOREVER for (;;)   /* Toujours méchant, mais au moins visible pour les humains */

##### Application

Crier quand on voit une macro en minuscules.

### <a name="res-macros3"></a>ES.33 : Si vous devez utiliser des macros, donnez-leur des noms uniques

##### Raison

Les macros n'obéissent pas aux règles d'étendue.

##### Exemple

    #define MYCHAR        /* MAUVAIS, finira par entrer en collision avec le MYCHAR de quelqu'un d'autre */

    #define ZCORP_CHAR    /* Toujours méchant, mais moins susceptible d'entrer en collision */

##### Note

Éviter les macros si vous le pouvez : [ES.30](010-expr.md#res-macros), [ES.31](010-expr.md#res-macros2), et [ES.32](010-expr.md#res-all_caps).
Cependant, il y a des milliards de lignes de code parsemées de macros et une longue tradition d'utilisation et de surutilisation de macros.
Si vous êtes forcé d'utiliser des macros, utilisez des noms longs et des préfixes prétendument uniques (par ex. le nom de votre organisation) pour réduire la probabilité de collision.

##### Application

Avertir contre les noms de macros courts.

### <a name="res-ellipses"></a> ES.34 : Ne pas définir de fonction variable (style C)

##### Raison

Pas de sécurité de type.
Nécessite un code désordonné avec des casts et des macros pour fonctionner correctement.

##### Exemple

    #include <cstdarg>

    // "severity" suivi d'une liste de char* terminée par zéro ; écrire les chaînes de caractères style C dans cerr
    void error(int severity ...)
    {
        va_list ap;             // un type magique pour contenir les arguments
        va_start(ap, severity); // démarrage des arguments : "severity" est le premier argument de error()

        for (;;) {
            // traiter le prochain var comme un char* ; pas de vérification : un cast déguisé
            char* p = va_arg(ap, char*);
            if (!p) break;
            cerr << p << ' ';
        }

        va_end(ap);             // nettoyage des arguments (n'oubliez pas)

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

**Alternative** : Surcharge. Templates. Templates variables.

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

C'est essentiellement la façon dont `printf` est implémenté.

##### Application

* Signaler les définitions de fonctions variables style C.
* Signaler `#include <cstdarg>` et `#include <stdarg.h>`


## ES.expr : Expressions

Les expressions manipulent des valeurs.

### <a name="res-complicated"></a>ES.40 : Éviter les expressions compliquées

##### Raison

Les expressions compliquées sont source d'erreurs.

##### Exemple

    // mauvais : assignation cachée dans une sous-expression
    while ((c = getc()) != -1)

    // mauvais : deux variables non locales assignées dans des sous-expressions
    while ((cin >> c1, cin >> c2), c1 == c2)

    // meilleur, mais possiblement toujours trop compliqué
    for (char c1, c2; cin >> c1 >> c2 && c1 == c2;)

    // OK : si i et j ne sont pas aliasés
    int x = ++i + ++j;

    // OK : si i != j et i != k
    v[i] = v[j] + v[k];

    // mauvais : plusieurs assignations « cachées » dans des sous-expressions
    x = a + (b = f()) + (c = g()) * 7;

    // mauvais : repose sur des règles de priorité communément mal comprises
    x = a & b + c * d && e ^ f == 7;

    // mauvais : comportement indéfini
    x = x++ + x++ + ++x;

Certaines de ces expressions sont inconditionnellement mauvaises (par ex. elles reposent sur un comportement indéfini). D'autres sont simplement si compliquées et/ou inhabituelles que même de bons programmeurs pourraient les mal comprendre ou manquer un problème quand ils sont pressés.

##### Note

C++17 resserre les règles pour l'ordre d'évaluation
(gauche-à-droite sauf droite-à-gauche dans les assignations, et l'ordre d'évaluation des arguments de fonction est non spécifié ; [voir ES.43](010-expr.md#res-order)),
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

Délicat. Jusqu'à quel point une expression doit-elle être compliquée pour être considérée comme compliquée ? Écrire des calculs comme des instructions avec une opération chacune est aussi confus. Choses à considérer :

* effets de bord : effets de bord sur plusieurs variables non locales (pour une certaine définition de non-locale) peuvent être suspects, surtout si les effets de bord sont dans des sous-expressions séparées
* écritures sur des variables aliasées
* plus de N opérateurs (et quel devrait être N ?)
* reliance sur des règles de priorité subtiles
* utilisation de comportement indéfini (pouvons-nous attraper tout comportement indéfini ?)
* comportement défini par l'implémentation ?
* ???

### <a name="res-parens"></a>ES.41 : En cas de doute sur la priorité des opérateurs, utiliser des parenthèses

##### Raison

Éviter les erreurs. Lisibilité. Tout le monde n'a pas la table des opérateurs mémorisée.

##### Exemple

    const unsigned int flag = 2;
    unsigned int a = flag;

    if (a & flag != 0)  // mauvais : signifie a&(flag != 0)

Note : Nous recommandons que les programmeurs connaissent leur table de priorité pour les opérations arithmétiques, les opérations logiques, mais considèrent que mélanger des opérations logiques bit à bit avec d'autres opérateurs nécessite des parenthèses.

    if ((a & flag) != 0)  // OK : fonctionne comme prévu

##### Note

Vous devriez assez connaître pour ne pas avoir besoin de parenthèses pour :

    if (a < 0 || a <= max) {
        // ...
    }

##### Application

* Signaler les combinaisons d'opérateurs logiques bit à bit et d'autres opérateurs.
* Signaler les opérateurs d'assignation non comme opérateur le plus à gauche.
* ???

### <a name="res-ptr"></a>ES.42 : Garder l'utilisation des pointeurs simple et directe

##### Raison

La manipulation compliquée de pointeurs est une source majeure d'erreurs.

##### Note

Utiliser `gsl::span` à la place.
Les pointeurs devraient [ne référencer que des objets uniques](005-interfaces.md#ri-array).
L'arithmétique de pointeurs est fragile et facile à mal faire, la source de nombreux, nombreux bugs et violations de sécurité.
`span` est un type sûr avec vérification de bornes pour accéder à des tableaux de données.
L'accès dans un tableau avec des bornes connues en utilisant une constante comme index peut être validé par le compilateur.

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

L'indexation avec une variable est difficile à valider comme sûre pour les outils et les humains.
`span` est un type sûr avec vérification de bornes à l'exécution pour accéder à des tableaux de données.
`at()` est une autre alternative qui garantit que les accès unitaires sont vérifiés par bornes.
Si des itérateurs sont nécessaires pour accéder à un tableau, utiliser les itérateurs d'un `span` construit sur le tableau.

##### Exemple, mauvais

    void f(array<int, 10> a, int pos)
    {
        a[pos / 2] = 1; // MAUVAIS
        a[pos - 1] = 2; // MAUVAIS
        a[-1] = 3;    // MAUVAIS (mais facilement attrapé par les outils) -- pas de remplacement, ne faites pas ça
        a[10] = 4;    // MAUVAIS (mais facilement attrapé par les outils) -- pas de remplacement, ne faites pas ça
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

Utiliser un `span` et une boucle `for` par plage :

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

Utiliser une boucle `for` par plage :

    void f3()
    {
        int arr[COUNT];
        int i = 0;
        for (auto& e : arr)
             e = i++;
    }

##### Note

Les outils peuvent offrir des réécritures d'accès à des tableaux impliquant des expressions d'index dynamiques pour utiliser `at()` à la place :

    static int a[10];

    void f(int i, int j)
    {
        a[i + j] = 12;      // MAUVAIS, pourrait être réécrit comme ...
        at(a, i + j) = 12;  // OK -- vérifié par bornes
    }

##### Exemple

Transformer un tableau en pointeur (comme le langage le fait essentiellement toujours) supprime les opportunités de vérification, donc l'éviter

    void g(int* p);

    void f()
    {
        int a[5];
        g(a);        // MAUVAIS : essayons-nous de passer un tableau ?
        g(&a[0]);    // OK : passer un objet unique
    }

Si vous voulez passer un tableau, dites-le :

    void g(int* p, size_t length);  // ancien (dangereux) code

    void g1(span<int> av); // MEILLEUR : faire changer g().

    void f2()
    {
        int a[5];
        span<int> av = a;

        g(av.data(), av.size());   // OK, si vous n'avez pas le choix
        g1(a);                     // OK -- pas de décadence ici, utiliser plutôt le constructeur implicite de span
    }

##### Application

* Signaler toute opération arithmétique sur une expression de type pointeur qui résulte en une valeur de type pointeur.
* Signaler toute expression d'indexation sur une expression ou variable de type tableau (soit tableau statique soit `std::array`) où l'index n'est pas une expression constante du temps de compilation avec une valeur entre `0` et la borne supérieure du tableau.
* Signaler toute expression qui reposerait sur la conversion implicite d'un type tableau en type pointeur.

Cette règle fait partie du [profil de sécurité des bornes](022-profile.md#ss-bounds).


### <a name="res-order"></a>ES.43 : Éviter les expressions avec un ordre d'évaluation indéfini

##### Raison

Vous n'avez aucune idée de ce que fait un tel code. Portabilité.
Même si cela fait quelque chose de sensé pour vous, cela pourrait faire quelque chose de différent sur un autre compilateur (par ex. la prochaine version de votre compilateur) ou avec un réglage d'optimiseur différent.

##### Note

C++17 resserre les règles pour l'ordre d'évaluation :
gauche-à-droite sauf droite-à-gauche dans les assignations, et l'ordre d'évaluation des arguments de fonction est non spécifié.

Cependant, souvenez-vous que votre code pourrait être compilé avec un compilateur antérieur à C++17 (par ex. par copier-coller), donc ne soyez pas trop malin.

##### Exemple

    v[i] = ++i;   //  le résultat est indéfini

Une bonne règle de base est que vous ne devriez pas lire une valeur deux fois dans une expression où vous y écrivez.

##### Application

Peut être détecté par un bon analyseur.

### <a name="res-order-fct"></a>ES.44 : Ne pas dépendre de l'ordre d'évaluation des arguments de fonction

##### Raison

Parce que cet ordre est non spécifié.

##### Note

C++17 resserre les règles pour l'ordre d'évaluation, mais l'ordre d'évaluation des arguments de fonction est toujours non spécifié.

##### Exemple

    int i = 0;
    f(++i, ++i);

Avant C++17, le comportement est indéfini, donc le comportement pourrait être n'importe quoi (par ex. `f(2, 2)`).
Depuis C++17, ce code n'a pas de comportement indéfini, mais il n'est toujours pas spécifié quel argument est évalué en premier. L'appel sera `f(1, 2)` ou `f(2, 1)`, mais vous ne savez pas lequel.

##### Exemple

Les opérateurs surchargés peuvent conduire à des problèmes d'ordre d'évaluation :

    f1()->m(f2());          // m(f1(), f2())
    cout << f1() << f2();   // operator<<(operator<<(cout, f1()), f2())

En C++17, ces exemples fonctionnent comme prévu (gauche à droite) et les assignations sont évaluées de droite à gauche (tout comme la liaison de = est droite-à-gauche)

    f1() = f2();    // comportement indéfini en C++14 ; en C++17, f2() est évalué avant f1()

##### Application

Peut être détecté par un bon analyseur.

### <a name="res-magic"></a>ES.45 : Éviter les « constantes magiques » ; utiliser des constantes symboliques

##### Raison

Les constantes non nommées intégrées dans des expressions sont facilement manquées et souvent difficiles à comprendre :

##### Exemple

    for (int m = 1; m <= 12; ++m)   // ne pas : constante magique 12
        cout << month[m] << '\n';

Non, nous ne savons pas tous qu'il y a 12 mois, numérotés 1..12, dans une année. Mieux :

    // les mois sont indexés 1..12
    constexpr int first_month = 1;
    constexpr int last_month = 12;

    for (int m = first_month; m <= last_month; ++m)   // meilleur
        cout << month[m] << '\n';

Encore mieux, n'exposez pas les constantes :

    for (auto m : month)
        cout << m << '\n';

##### Application

Signaler les littéraux dans le code. Accepter `0`, `1`, `nullptr`, `\n`, `""`, et d'autres sur une liste positive.

### <a name="res-narrowing"></a>ES.46 : Éviter les conversions arithmétiques rétrécissantes (narrowing, tronquantes)

##### Raison

Une conversion rétrécissante détruit de l'information, souvent de manière inattendue.

##### Exemple, mauvais

Un exemple clé est le rétrécissement de base :

    double d = 7.9;
    int i = d;    // mauvais : rétrécissement : i devient 7
    i = (int) d;  // mauvais : nous allons prétendre que ce n'est toujours pas assez explicite

    void f(int x, long y, double d)
    {
        char c1 = x;   // mauvais : rétrécissement
        char c2 = y;   // mauvais : rétrécissement
        char c3 = d;   // mauvais : rétrécissement
    }

##### Note

La bibliothèque de support des lignes directrices offre une opération `narrow_cast` pour spécifier qu'un rétrécissement est acceptable et un `narrow` (« rétrécir si ») qui lève une exception si un rétrécissement jetterait des valeurs légales :

    i = gsl::narrow_cast<int>(d);   // OK (vous l'avez demandé) : rétrécissement : i devient 7
    i = gsl::narrow<int>(d);        // OK : lève narrowing_error

Nous incluons aussi les conversions arithmétiques avec perte, telles que d'un type flottant négatif vers un type entier non signé :

    double d = -7.9;
    unsigned u = 0;

    u = d;                               // mauvais : rétrécissement
    u = gsl::narrow_cast<unsigned>(d);   // OK (vous l'avez demandé) : u devient 4294967289
    u = gsl::narrow<unsigned>(d);        // OK : lève narrowing_error

##### Note

Cette règle ne s'applique pas aux [conversions contextuelles vers bool](https://en.cppreference.com/w/cpp/language/implicit_conversion#Contextual_conversions) :

    if (ptr) do_something(*ptr);   // OK : ptr est utilisé comme condition
    bool b = ptr;                  // mauvais : rétrécissement

##### Application

Un bon analyseur peut détecter toutes les conversions rétrécissantes. Cependant, signaler toutes les conversions rétrécissantes conduira à beaucoup de faux positifs. Suggestions :

* Signaler toutes les conversions flottant-vers-entier. (Peut-être seulement `float`->`char` et `double`->`int`. Attention aux dragons ! Nous avons besoin de données.)
* Signaler tous les `long`->`char`. (Je soupçonne que `int`->`char` est très courant. Attention aux dragons ! Nous avons besoin de données.)
* Considérer les conversions rétrécissantes pour les arguments de fonction comme particulièrement suspects.

### <a name="res-nullptr"></a>ES.47 : Utiliser `nullptr` plutôt que `0` ou `NULL`

##### Raison

Lisibilité. Minimiser les surprises : `nullptr` ne peut pas être confondu avec un
`int`. `nullptr` a aussi un type bien spécifié (très restrictif), et fonctionne donc
dans plus de scénarios où la déduction de type pourrait faire la mauvaise chose avec `NULL`
ou `0`.

##### Exemple

Considérons :

    void f(int);
    void f(char*);
    f(0);         // appelle f(int)
    f(nullptr);   // appelle f(char*)

##### Application

Signaler les utilisations de `0` et `NULL` pour des pointeurs. La transformation pourrait être aidée par une simple transformation de programme.

### <a name="res-casts"></a>ES.48 : Éviter les casts

##### Raison

Les casts sont une source connue d'erreurs et rendent certaines optimisations non fiables.

##### Exemple, mauvais

    double d = 2;
    auto p = (long*)&d;
    auto q = (long long*)&d;
    cout << d << ' ' << *p << ' ' << *q << '\n';

Que pensez-vous que ce fragment affiche ? Le résultat est au mieux défini par l'implémentation. J'ai obtenu

    2 0 4611686018427387904

En ajoutant

    *q = 666;
    cout << d << ' ' << *p << ' ' << *q << '\n';

J'ai obtenu

    3.29048e-321 666 666

Surpris ? C'est en réalité un comportement indéfini, et donc aurait aussi pu faire planter le programme.

##### Note

Les programmeurs qui écrivent des casts supposent typiquement qu'ils savent ce qu'ils font,
ou qu'écrire un cast rend le programme « plus facile à lire ».
En fait, ils désactivent souvent les règles générales pour l'utilisation des valeurs.
La résolution de surcharge et l'instantiation de templates choisissent généralement la bonne fonction s'il y a une bonne fonction à choisir.
S'il n'y en a pas, il y en aurait peut-être dû, plutôt que d'appliquer un correctif local (cast).

##### Notes

Les casts sont nécessaires dans un langage de programmation système. Par exemple, comment
obtiendrait-on autrement l'adresse d'un registre de périphérique dans un pointeur ? Cependant, les casts
sont sérieusement surutilisés ainsi qu'une source majeure d'erreurs.

Si vous sentez le besoin de beaucoup de casts, il pourrait y avoir un problème de conception fondamental.

Le [profil de type](022-profile.md#pro-type-reinterpretcast) interdit `reinterpret_cast` et les casts style C.

Ne jamais caster vers `(void)` pour ignorer une valeur de retour `[[nodiscard]]`.
Si vous voulez délibérément jeter un tel résultat, réfléchissez d'abord sérieusement à savoir si c'est vraiment une bonne idée (il y a généralement une bonne raison pour laquelle l'auteur de la fonction ou du type de retour a utilisé `[[nodiscard]]` en premier lieu).
Si vous pensez toujours que c'est approprié et que votre réviseur de code est d'accord, utilisez `std::ignore =` pour désactiver l'avertissement, ce qui est simple, portable et facile à chercher avec grep.

##### Alternatives

Les casts sont largement (mal)utilisés. Le C++ moderne a des règles et des constructions qui éliminent le besoin de casts dans de nombreux contextes, tels que

* Utiliser des templates
* Utiliser `std::variant`
* S'appuyer sur les conversions implicites bien définies et sûres entre types de pointeurs
* Utiliser `std::ignore =` pour ignorer les valeurs `[[nodiscard]]`.

##### Application

* Signaler tous les casts style C, y compris vers `void`.
* Signaler les casts en style fonctionnel utilisant `Type(value)`. Utiliser `Type{value}` à la place, qui n'est pas rétrécissant. (Voir [ES.64](010-expr.md#res-construct).)
* Signaler les [casts d'identité](022-profile.md#pro-type-identitycast) entre types de pointeurs, où les types source et cible sont les mêmes (022-profile.md#pro-type-identitycast).
* Signaler un cast de pointeur explicite qui pourrait être [implicite](022-profile.md#pro-type-implicitpointercast).

### <a name="res-casts-named"></a>ES.49 : Si vous devez utiliser un cast, utiliser un cast nommé

##### Raison

Lisibilité. Éviter les erreurs.
Les casts nommés sont plus spécifiques qu'un cast style C ou fonctionnel, permettant au compilateur d'attraper certaines erreurs.

Les casts nommés sont :

* `static_cast`
* `const_cast`
* `reinterpret_cast`
* `dynamic_cast`
* `std::move`         // `move(x)` est une référence rvalue à `x`
* `std::forward`      // `forward<T>(x)` est une référence rvalue ou lvalue à `x` selon `T`
* `gsl::narrow_cast`  // `narrow_cast<T>(x)` est `static_cast<T>(x)`
* `gsl::narrow`       // `narrow<T>(x)` est `static_cast<T>(x)` si `static_cast<T>(x) == x` ou lève `narrowing_error`

##### Exemple

    class B { /* ... */ };
    class D { /* ... */ };

    D* downcast(B* pb)
    {
        D* pd0 = pb;                        // erreur : pas de conversion implicite de B* à D*
        D* pd1 = (D*)pb;                    // légal, mais que fait-on ?
        D* pd2 = static_cast<D*>(pb);       // erreur : D n'est pas dérivé de B
        D* pd3 = reinterpret_cast<D*>(pb);  // OK : sur votre tête soit !
        D* pd4 = dynamic_cast<D*>(pb);      // OK : retourne nullptr
        // ...
    }

L'exemple a été synthétisé à partir de bugs du monde réel où `D` était dérivé de `B`, mais quelqu'un a refactorisé la hiérarchie.
Le cast style C est dangereux parce qu'il peut faire n'importe quel type de conversion, nous privant de toute protection contre les erreurs (maintenant ou à l'avenir).

##### Note

Quand on convertit entre des types sans perte d'information (par ex. de `float` vers
`double` ou de `int32` vers `int64`), l'initialisation par accolades pourrait être utilisée à la place.

    double d {some_float};
    int64_t i {some_int32};

Cela rend clair que la conversion de type était intentionnelle et empêche aussi
les conversions entre types qui pourraient entraîner une perte de précision. (C'est une
erreur de compilation d'essayer d'initialiser un `float` depuis un `double` de cette façon,
par exemple.)

##### Note

`reinterpret_cast` peut être essentiel, mais les utilisations essentielles (par ex. transformer une adresse machine en pointeur) ne sont pas sûres du point de vue des types :

    auto p = reinterpret_cast<Device_register>(0x800);  // intrinsèquement dangereux


##### Application

* Signaler tous les casts style C, y compris vers `void`.
* Signaler les casts en style fonctionnel utilisant `Type(value)`. Utiliser `Type{value}` à la place, qui n'est pas rétrécissant. (Voir [ES.64](010-expr.md#res-construct).)
* Le [profil de type](022-profile.md#pro-type-reinterpretcast) interdit `reinterpret_cast`.
* Le [profil de type](022-profile.md#pro-type-arithmeticcast) avertit quand on utilise `static_cast` entre types arithmétiques.

### <a name="res-casts-const"></a>ES.50 : Ne pas supprimer le `const`

##### Raison

Cela fait mentir le `const`.
Si la variable est effectivement déclarée `const`, la modifier résulte en un comportement indéfini.

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

Parfois, vous pourriez être tenté de recourir à `const_cast` pour éviter la duplication de code, par exemple quand deux fonctions d'accès qui ne diffèrent que par leur caractère `const` ont des implémentations similaires. Par exemple :

    class Bar;

    class Foo {
    public:
        // MAUVAIS, duplique la logique
        Bar& get_bar()
        {
            /* logique complexe autour de l'obtention d'une référence non-const à my_bar */
        }

        const Bar& get_bar() const
        {
            /* même logique complexe autour de l'obtention d'une référence const à my_bar */
        }
    private:
        Bar my_bar;
    };

Plutôt, préférez partager les implémentations. Normalement, vous pouvez simplement faire appel à la fonction `const` depuis la fonction non-`const`. Cependant, quand il y a une logique complexe, cela peut conduire au motif suivant qui recourt encore à un `const_cast` :

    class Foo {
    public:
        // pas génial, la version non-const appelle la version const mais recourt à const_cast
        Bar& get_bar()
        {
            return const_cast<Bar&>(static_cast<const Foo&>(*this).get_bar());
        }
        const Bar& get_bar() const
        {
            /* la logique complexe autour de l'obtention d'une référence const à my_bar */
        }
    private:
        Bar my_bar;
    };

Bien que ce motif soit sûr quand il est appliqué correctement, parce que l'appelant a dû avoir un objet non-`const` au départ, ce n'est pas idéal parce que la sécurité est difficile à appliquer automatiquement comme règle de vérification.

Plutôt, préférez mettre le code commun dans une fonction d'aide commune -- et faites-en un template pour qu'il déduise `const`. Cela n'utilise aucun `const_cast` du tout :

    class Foo {
    public:                         // bon
              Bar& get_bar()       { return get_bar_impl(*this); }
        const Bar& get_bar() const { return get_bar_impl(*this); }
    private:
        Bar my_bar;

        template<class T>           // bon, déduit si T est const ou non-const
        static auto& get_bar_impl(T& t)
            { /* la logique complexe autour de l'obtention d'une référence possiblement-const à my_bar */ }
    };

Note : Ne pas faire de gros travaux non dépendants dans un template, ce qui conduit à un gonflement du code. Par exemple, une amélioration supplémentaire serait si tout ou partie de `get_bar_impl` peut être non dépendant et factorisé dans une fonction commune non template, pour une réduction potentielle importante de la taille du code.

##### Exception

Vous pourriez avoir besoin de supprimer le `const` quand vous appelez des fonctions non `const`-correctes.
Préférez envelopper de telles fonctions dans des wrappers en ligne `const`-corrects pour encapsuler le cast en un seul endroit.

##### Exemple

Parfois, « supprimer le `const` » sert à permettre la mise à jour de certaines informations transitoires d'un objet autrement immuable.
Les exemples sont le cache, la mémorisation, et le précalcul.
De tels exemples sont souvent aussi bien ou mieux gérés en utilisant `mutable` ou une indirection qu'avec un `const_cast`.

Considérons le maintien de résultats précédemment calculés pour une opération coûteuse :

    int compute(int x); // calculer une valeur pour x ; supposons que c'est coûteux

    class Cache {   // un type implémentant un cache pour une opération int->int
    public:
        pair<bool, int> find(int x) const;   // y a-t-il une valeur pour x ?
        void set(int x, int v);             // faire de y la valeur pour x
        // ...
    private:
        // ...
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
        // ...
    private:
        Cache cache;
    };

Ici, `get_val()` est logiquement constante, donc nous aimerions en faire un membre `const`.
Pour le faire, nous devons encore muter `cache`, donc les gens recourent parfois à un `const_cast` :

    class X {   // Solution suspecte basée sur le cast
    public:
        int get_val(int x) const
        {
            auto p = cache.find(x);
            if (p.first) return p.second;
            int val = compute(x);
            const_cast<Cache&>(cache).set(x, val);   // laid
            return val;
        }
        // ...
    private:
        Cache cache;
    };

Heureusement, il y a une meilleure solution :
Déclarer que `cache` est mutable même pour un objet `const` :

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
        // ...
    private:
        mutable Cache cache;
    };

Une solution alternative serait de stocker un pointeur vers le `cache` :

    class X {   // OK, mais solution légèrement plus désordonnée
    public:
        int get_val(int x) const
        {
            auto p = cache->find(x);
            if (p.first) return p.second;
            int val = compute(x);
            cache->set(x, val);
            return val;
        }
        // ...
    private:
        unique_ptr<Cache> cache;
    };

Cette solution est la plus flexible, mais nécessite la construction et la destruction explicites de `*cache`
(probablement dans le constructeur et le destructeur de `X`).

Dans toute variante, nous devons nous protéger contre les conditions de course sur le `cache` dans le code multi-threadé, possiblement en utilisant un `std::mutex`.

##### Application

* Signaler les `const_cast`.
* Cette règle fait partie du [profil de sécurité de type](022-profile.md#pro-type-constcast) pour le profil associé.

### <a name="res-range-checking"></a>ES.55 : Éviter le besoin de vérification de plage

##### Raison

Les constructions qui ne peuvent pas déborder ne débordent pas (et tournent généralement plus vite) :

##### Exemple

    for (auto& x : v)      // afficher tous les éléments de v
        cout << x << '\n';

    auto p = find(v, x);   // trouver x dans v

##### Application

Rechercher des vérifications de plage explicites et suggérer heuristiquement des alternatives.

### <a name="res-move"></a>ES.56 : Écrire `std::move()` uniquement quand vous devez explicitement déplacer un objet vers une autre étendue

##### Raison

Nous déplaçons, plutôt que copier, pour éviter la duplication et pour une meilleure performance.

Un déplacement laisse typiquement derrière un objet vide ([C.64](007-class.md#rc-move-semantic)), ce qui peut être surprenant ou même dangereux, donc nous essayons d'éviter de déplacer depuis des lvalues (elles pourraient être accédées plus tard).

##### Notes

Le déplacement est fait implicitement quand la source est une rvalue (par ex. une valeur dans un traitement de `return` ou un résultat de fonction), donc ne compliquez pas inutilement le code dans ces cas en écrivant `move` explicitement. À la place, écrivez des fonctions courtes qui retournent des valeurs, et à la fois le retour de la fonction et l'acceptation du retour par l'appelant seront optimisés naturellement.

En général, suivre les lignes directrices de ce document (y compris ne pas rendre les étendues des variables inutilement grandes, écrire des fonctions courtes qui retournent des valeurs, retourner des variables locales) aide à éliminer la plupart du besoin de `std::move` explicite.

Un `move` explicite est nécessaire pour déplacer explicitement un objet vers une autre étendue, notamment pour le passer à une fonction « puits » (sink) et dans les implémentations des opérations de déplacement elles-mêmes (constructeur de déplacement, opérateur d'assignation par déplacement) et des opérations d'échange.

##### Exemple, mauvais

    void sink(X&& x);   // sink prend la propriété de x

    void user()
    {
        X x;
        // erreur : ne peut pas lier une lvalue à une référence rvalue
        sink(x);
        // OK : sink prend le contenu de x, x doit maintenant être supposé vide
        sink(std::move(x));

        // ...

        // probablement une erreur
        use(x);
    }

Habituellement, un `std::move()` est utilisé comme argument d'un paramètre `&&`.
Et après avoir fait cela, supposez que l'objet a été déplacé (voir [C.64](007-class.md#rc-move-semantic)) et ne relisez pas son état avant de lui assigner d'abord une nouvelle valeur.

    void f()
    {
        string s1 = "supercalifragilisticexpialidocious";

        string s2 = s1;             // ok, prend une copie
        assert(s1 == "supercalifragilisticexpialidocious");  // ok

        // mauvais, si vous voulez continuer à utiliser la valeur de s1
        string s3 = move(s1);

        // mauvais, l'assert échouera probablement, s1 a probablement changé
        assert(s1 == "supercalifragilisticexpialidocious");
    }

##### Exemple

    void sink(unique_ptr<widget> p);  // passer la propriété de p à sink()

    void f()
    {
        auto w = make_unique<widget>();
        // ...
        sink(std::move(w));               // ok, donner à sink()
        // ...
        sink(w);    // Erreur : unique_ptr est soigneusement conçu pour que vous ne puissiez pas le copier
    }

##### Notes

`std::move()` est un cast vers `&&` déguisé ; il ne déplace rien lui-même, mais marque un objet nommé comme candidat pouvant être déplacé.
Le langage connaît déjà les cas courants où des objets peuvent être déplacés, en particulier lors du retour de valeurs de fonctions, donc ne compliquez pas le code avec des `std::move()` redondants.

N'écrivez jamais `std::move()` simplement parce que vous avez entendu « c'est plus efficace ».
En général, ne croyez pas les affirmations d'« efficacité » sans données (???).
En général, ne compliquez pas votre code sans raison (??).
N'écrivez jamais `std::move()` sur un objet const, il est silencieusement transformé en copie (voir l'élément 23 dans [Meyers15](032-bibliography.md#Meyers15))

##### Exemple, mauvais

    vector<int> make_vector()
    {
        vector<int> result;
        // ... charger result avec des données
        return std::move(result);       // mauvais ; écrivez simplement "return result;"
    }

N'écrivez jamais `return move(variable_locale);`, parce que le langage sait déjà que la variable est un candidat au déplacement.
Écrire `move` dans ce code n'aidera pas, et peut en fait être préjudiciable car sur certains compilateurs cela interfère avec le RVO (l'optimisation de la valeur de retour) en créant un alias de référence supplémentaire vers la variable locale.


##### Exemple, mauvais

    vector<int> v = std::move(make_vector());   // mauvais ; le std::move est entièrement redondant

N'écrivez jamais `move` sur une valeur retournée telle que `x = move(f());` où `f` retourne par valeur.
Le langage sait déjà qu'une valeur retournée est un objet temporaire qui peut être déplacé.

##### Exemple

    void mover(X&& x)
    {
        call_something(std::move(x));         // ok
        call_something(std::forward<X>(x));   // mauvais, ne pas std::forward une référence rvalue
        call_something(x);                    // suspect, pourquoi pas std::move ?
    }

    template<class T>
    void forwarder(T&& t)
    {
        call_something(std::move(t));         // mauvais, ne pas std::move une référence de transfert
        call_something(std::forward<T>(t));   // ok
        call_something(t);                    // suspect, pourquoi pas std::forward ?
    }

##### Application

* Signaler l'utilisation de `std::move(x)` où `x` est une rvalue ou le langage la traitera déjà comme une rvalue, y compris `return std::move(variable_locale);` et `std::move(f())` sur une fonction qui retourne par valeur.
* Signaler les fonctions prenant un paramètre `S&&` s'il n'y a pas de surcharge `const S&` pour prendre en charge les lvalues.
* Signaler un argument `std::move`d passé à un paramètre, sauf si le type du paramètre est une référence rvalue `X&&` ou le type est move-only et le paramètre est passé par valeur.
* Signaler quand `std::move` est appliqué à une référence de transfert (`T&&` où `T` est un type de paramètre template). Utiliser `std::forward` à la place.
* Signaler quand `std::move` est appliqué à autre chose qu'une référence rvalue non-const. (Cas plus général de la règle précédente pour couvrir les cas non-transfert.)
* Signaler quand `std::forward` est appliqué à une référence rvalue (`X&&` où `X` est un type de paramètre non-template). Utiliser `std::move` à la place.
* Signaler quand `std::forward` est appliqué à autre chose qu'une référence de transfert. (Cas plus général de la règle précédente pour couvrir les cas non-déplacement.)
* Signaler quand un objet est potentiellement déplacé et que l'opération suivante est une opération `const` ; il devrait d'abord y avoir une opération non-`const` intermédiaire, idéalement une assignation, pour réinitialiser d'abord la valeur de l'objet.

### <a name="res-new"></a>ES.60 : Éviter `new` et `delete` en dehors des fonctions de gestion de ressources

##### Raison

La gestion directe de ressources dans le code applicatif est source d'erreurs et fastidieuse.

##### Note

Cela est aussi connu sous le nom de règle « Pas de `new` nu ! »

##### Exemple, mauvais

    void f(int n)
    {
        auto p = new X[n];   // n X construits par défaut
        // ...
        delete[] p;
    }

Il peut y avoir du code dans la partie `...` qui fait que le `delete` n'a jamais lieu.

**Voir aussi** : [R : Gestion de ressources](009-resource.md)

##### Application

Signaler les `new` nus et les `delete` nus.

### <a name="res-del"></a>ES.61 : Supprimer les tableaux avec `delete[]` et les non-tableaux avec `delete`

##### Raison

C'est ce que le langage exige, et les incohérences peuvent conduire à des erreurs de libération de ressources et/ou à la corruption de la mémoire.

##### Exemple, mauvais

    void f(int n)
    {
        auto p = new X[n];   // n X construits par défaut
        // ...
        delete p;   // erreur : supprime juste l'objet p, plutôt que de supprimer le tableau p[]
    }

##### Note

Cet exemple viole non seulement la [règle de pas de `new` nu](010-expr.md#res-new) comme dans l'exemple précédent, il a beaucoup plus de problèmes.

##### Application

* Signaler les `new` et `delete` incohérents s'ils sont dans la même étendue.
* Signaler les `new` et `delete` incohérents s'ils sont dans une paire constructeur/destructeur.

### <a name="res-arr2"></a>ES.62 : Ne pas comparer des pointeurs vers des tableaux différents

##### Raison

Le résultat de le faire est indéfini.

##### Exemple, mauvais

    void f()
    {
        int a1[7];
        int a2[9];
        if (&a1[5] < &a2[7]) {}       // mauvais : indéfini
        if (0 < &a1[5] - &a2[7]) {}   // mauvais : indéfini
    }

##### Note

Cet exemple a beaucoup plus de problèmes.

##### Application

???

### <a name="res-slice"></a>ES.63 : Ne pas faire de troncature d'objet (slicing)

##### Raison

La troncature d'objet -- c'est-à-dire, copier seulement une partie d'un objet en utilisant l'assignation ou l'initialisation -- conduit le plus souvent à des erreurs parce que
l'objet était censé être considéré comme un tout.
Dans les rares cas où la troncature était délibérée, le code peut être surprenant.

##### Note

Il n'est pas possible de copier une partie d'un objet vide, donc cette définition de la troncature n'inclut délibérément pas les objets vides (n'ayant pas de membres de données non statiques), tels que les types vides utilisés pour le tag dispatching.

##### Exemple

    class Shape { /* ... */ };
    class Circle : public Shape { /* ... */ Point c; int r; };

    Circle c { {0, 0}, 42 };
    Shape s {c};    // copie-construit seulement la partie Shape de Circle
    s = c;          // ou copie-assigne seulement la partie Shape de Circle

    void assign(const Shape& src, Shape& dest)
    {
        dest = src;
    }
    Circle c2 { {1, 1}, 43 };
    assign(c, c2);   // oops, pas tout l'état est transféré
    assert(c == c2); // si nous fournissons la copie, nous devrions aussi fournir la comparaison,
                     // mais cela retournera probablement false

Le résultat sera sans sens parce que le centre et le rayon ne seront pas copiés de `c` vers `s`.
La première défense contre cela est de [définir la classe de base `Shape` pour ne pas le permettre](007-class.md#rc-copy-virtual).

##### Alternative

Si vous voulez faire de la troncature, définissez une opération explicite pour le faire.
Cela sauve les lecteurs de la confusion.
Par exemple :

    class Smiley : public Circle {
        public:
        Circle copy_circle();
        // ...
    };

    Smiley sm { /* ... */ };
    Circle c1 {sm};  // idéalement empêché par la définition de Circle
    Circle c2 {sm.copy_circle()};

##### Application

Avertir contre la troncature si le type de base a des membres de données non statiques (possiblement via des bases transitives).

### <a name="res-construct"></a>ES.64 : Utiliser la notation `T{e}` pour la construction

##### Raison

La syntaxe de construction `T{e}` rend explicite que la construction est souhaitée.
La syntaxe de construction `T{e}` n'autorise pas le rétrécissement.
`T{e}` est la seule expression sûre et générale pour construire une valeur de type `T` depuis une expression `e`.
Les notations de cast `T(e)` et `(T)e` ne sont ni sûres ni générales.

##### Exemple

Pour les types intégrés, la notation de construction protège contre le rétrécissement et l'interprétation

    void use(char ch, int i, double d, char* p, long long lng)
    {
        int x1 = int{ch};     // OK, mais redondant
        int x2 = int{d};      // erreur : rétrécissement double->int ; utiliser un cast si vous en avez besoin
        int x3 = int{p};      // erreur : pointeur-vers-int ; utiliser un reinterpret_cast si vous en avez vraiment besoin
        int x4 = int{lng};    // erreur : rétrécissement long long->int ; utiliser un cast si vous en avez besoin

        int y1 = int(ch);     // OK, mais redondant
        int y2 = int(d);      // mauvais : rétrécissement double->int ; utiliser un cast si vous en avez besoin
        int y3 = int(p);      // mauvais : pointeur-vers-int ; utiliser un reinterpret_cast si vous en avez vraiment besoin
        int y4 = int(lng);    // mauvais : rétrécissement long long->int ; utiliser un cast si vous en avez besoin

        int z1 = (int)ch;     // OK, mais redondant
        int z2 = (int)d;      // mauvais : rétrécissement double->int ; utiliser un cast si vous en avez besoin
        int z3 = (int)p;      // mauvais : pointeur-vers-int ; utiliser un reinterpret_cast si vous en avez vraiment besoin
        int z4 = (int)lng;    // mauvais : rétrécissement long long->int ; utiliser un cast si vous en avez besoin
    }

Les conversions entier-vers/depuis-pointeur sont définies par l'implémentation quand on utilise les notations `T(e)` ou `(T)e`, et non portables
entre les plateformes avec différentes tailles d'entiers et de pointeurs.

##### Note

[Éviter les casts](010-expr.md#res-casts) (conversion de type explicite) et si vous devez [privilégier les casts nommés](010-expr.md#res-casts-named).

##### Note

Quand non ambigu, le `T` peut être omis de `T{e}`.

    complex<double> f(complex<double>);

    auto z = f({2*pi, 1});

##### Note

La notation de construction est la plus générale [notation d'initialisation](010-expr.md#res-list).

##### Exception

`std::vector` et d'autres conteneurs ont été définis avant que nous ayons `{}` comme notation de construction.
Considérons :

    vector<string> vs {10};                           // dix chaînes vides
    vector<int> vi1 {1, 2, 3, 4, 5, 6, 7, 8, 9, 10};  // dix éléments 1..10
    vector<int> vi2 {10};                             // un élément avec la valeur 10

Comment obtenir un `vector` de 10 `int` initialisés par défaut ?

    vector<int> v3(10); // dix éléments avec la valeur 0

L'utilisation de `()` plutôt que `{}` pour le nombre d'éléments est conventionnelle (remontant au début des années 1980), difficile à changer, mais reste
une erreur de conception : pour un conteneur où le type d'élément peut être confondu avec le nombre d'éléments, nous avons une ambiguïté qui
doit être résolue.
La résolution conventionnelle est d'interpréter `{10}` comme une liste d'un élément et d'utiliser `(10)` pour distinguer une taille.

Cette erreur ne doit pas être répétée dans le nouveau code.
Nous pouvons définir un type pour représenter le nombre d'éléments :

    struct Count { int n; };

    template<typename T>
    class Vector {
    public:
        Vector(Count n);                     // n éléments initialisés par défaut
        Vector(initializer_list<T> init);    // init.size() éléments
        // ...
    };

    Vector<int> v1{10};
    Vector<int> v2{Count{10}};
    Vector<Count> v3{Count{10}};    // oui, il y a encore un très petit problème

Le principal problème restant est de trouver un nom approprié pour `Count`.

##### Application

Signaler les casts style C `(T)e` et les casts en style fonctionnel `T(e)`.


### <a name="res-d
