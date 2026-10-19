# <a name="s-stdlib"></a>SL: La bibliothèque standard

En n'utilisant que le langage brut, chaque tâche est fastidieuse (dans n'importe quel langage). En utilisant une bibliothèque adaptée, chaque tâche peut devenir raisonnablement simple.

La bibliothèque standard a progressivement grandi au fil des années.

Sa description dans le standard est maintenant plus longue que celle des caractéristiques du langage.

Il est donc probable que cette section bibliothèque des lignes directrices finira par atteindre ou dépasser la taille de toutes les autres sections.

<< ??? Besoin d'un autre niveau de numérotation des règles ??? >>

Résumé des composants de la bibliothèque standard C++ :

* [SL.con: Conteneurs](018-stdlib.md#ss-con)
* [SL.str: Chaîne de caractères](018-stdlib.md#ss-string)
* [SL.io: Iostream](018-stdlib.md#ss-io)
* [SL.regex: Regex](018-stdlib.md#ss-regex)
* [SL.chrono: Temps](018-stdlib.md#ss-chrono)
* [SL.C: La bibliothèque standard C](018-stdlib.md#ss-clib)

Résumé des règles concernant la bibliothèque standard :

* [SL.1: Utiliser les bibliothèques partout où c'est possible](018-stdlib.md#rsl-lib)
* [SL.2: Préférer la bibliothèque standard aux autres bibliothèques](018-stdlib.md#rsl-sl)
* [SL.3: Ne pas ajouter d'entités non-standards au namespace `std`](018-stdlib.md#sl-std)
* [SL.4: Utiliser la bibliothèque standard d'une manière type-safe](018-stdlib.md#sl-safe)
* ??? 

### <a name="rsl-lib"></a>SL.1:  Utiliser les bibliothèques partout où c'est possible

##### Raison

Gagnez du temps. Ne réinventez pas la roue. Ne reproduisez pas le travail d'autrui. Profitez du travail des autres lorsqu'ils apportent des améliorations. Aidez les autres lorsque vous apportez des améliorations.

### <a name="rsl-sl"></a>SL.2: Préférer la bibliothèque standard aux autres bibliothèques

##### Raison

Plus de gens connaissent la bibliothèque standard. Il est plus probable qu'elle soit stable, bien entretenue et largement disponible que votre propre code ou la plupart des autres bibliothèques.

### <a name="sl-std"></a>SL.3: Ne pas ajouter d'entités non-standards au namespace `std`

##### Raison

Ajouter à `std` peut modifier la signification de code autrement conforme au standard. Les ajouts à `std` peuvent entrer en conflit avec les futures versions du standard.

##### Exemple

    namespace std { // BAD: violates standard

    class My_vector {
        //     . . .
    };

    }

    namespace Foo { // GOOD: user namespace is allowed

    class My_vector {
        //     . . .
    };

    }

##### Mise en œuvre

Possible, mais désordonné et susceptible de causer des problèmes sur les plateformes.

### <a name="sl-safe"></a>SL.4: Utiliser la bibliothèque standard d'une manière type-safe

##### Raison

Car, évidemment, enfreindre cette règle peut entraîner un comportement indéfini, une corruption de mémoire et toutes sortes d'autres erreurs.

##### Remarque

Il s'agit d'une méta-règle semi-philosophique, nécessitant de nombreuses règles concrètes de support. Nous en avons besoin comme un bouclier couvrant les règles plus précises.

Résumé des règles plus spécifiques :

* [SL.4: Utiliser la bibliothèque standard d'une manière type-safe](018-stdlib.md#sl-safe)

---

## <a name="ss-con"></a>SL.con: Conteneurs

???

Résumé des règles de conteneur :

* [SL.con.1: Préférer l'utilisation de `array` ou `vector` STL plutôt qu'un tableau C](018-stdlib.md#rsl-arrays)
* [SL.con.2: Préférer l'utilisation de `vector` STL par défaut à moins d'avoir une raison d'utiliser un conteneur différent](018-stdlib.md#rsl-vector)
* [SL.con.3: Éviter les dépassements de limites](018-stdlib.md#rsl-bounds)
* [SL.con.4: Ne pas utiliser `memset` ou `memcpy` pour des arguments qui ne sont pas directement copiables](018-stdlib.md#rsl-copy)

### <a name="rsl-arrays"></a>SL.con.1: Préférer l'utilisation de `array` ou `vector` STL plutôt qu'un tableau C

##### Raison

Les tableaux C sont moins sûrs et n'ont aucun avantage sur `array` et `vector`. Pour un tableau de longueur fixe, utilisez `std::array`, qui ne se transforme pas en pointeur lorsqu'il est passé à une fonction et connaît sa taille. De plus, comme un tableau natif, un `std::array` alloué sur la pile conserve ses éléments sur la pile. Pour un tableau de longueur variable, utilisez `std::vector`, qui peut changer de taille et gérer l'allocation mémoire.

##### Exemple

    int v[SIZE];                        // MAUVE
    std::array<int, SIZE> w;            // correct

##### Exemple

    int* v = new int[initial_size];     // MAUVE, pointeur brut
    delete[] v;                         // MAUVE, suppression manuelle
    std::vector<int> w(initial_size);   // correct

##### Remarque

Utilisez `gsl::span` pour les références non possédantes vers un conteneur.

##### Remarque

Comparer les performances d'un tableau à taille fixe alloué sur la pile avec un `vector` dont les éléments sont dans le tas est fallacieux. Vous pourriez tout aussi bien comparer un `std::array` sur la pile avec le résultat d'un `malloc()` accédé via un pointeur. Pour la plupart du code, même la différence entre l'allocation sur pile et sur tas ne compte pas, mais la commodité et la sécurité de `vector` comptent. Les personnes qui travaillent avec du code où cette différence a une importance sont tout à fait capables de choisir entre `array` et `vector`.

### <a name="rsl-vector"></a>SL.con.2: Préférer l'utilisation de `vector` STL par défaut à moins d'avoir une raison d'utiliser un conteneur différent

##### Raison

`vector` et `array` sont les seuls conteneurs standards qui offrent les avantages suivants :
- Le plus rapide d'accès généraliste (accès aléatoire, y compris compatible avec la vectorisation) ;
- Le motif d'accès par défaut le plus rapide (début→fin ou fin→début est préfetcher-friendly) ;
- La charge d'espace la plus faible (mise en page contiguë n'a aucune surcharge par élément, ce qui est cache-friendly).

Habituellement, vous devez ajouter et supprimer des éléments du conteneur, utilisez donc `vector` par défaut ; si vous n'avez pas besoin de modifier la taille du conteneur, utilisez `array`.

Même lorsque d'autres conteneurs semblent mieux adaptés, comme `map` pour une performance de recherche O(log N) ou un `list` pour une insertion efficace au milieu, un `vector` fera généralement mieux pour les conteneurs jusqu'à quelques kilo-octets en taille.

##### Remarque

`string` ne doit pas être utilisé comme conteneur de caractères individuels. Un `string` est une chaîne de texte ; si vous voulez un conteneur de caractères, utilisez plutôt `vector</*char_type*>` ou `array</*char_type*>`.

##### Exceptions

Si vous avez une bonne raison d'utiliser un autre conteneur, utilisez-le à la place. Par exemple :
* Si `vector` convient à vos besoins mais vous n'avez pas besoin que le conteneur soit de taille variable, utilisez `array` à la place.
* Si vous désirez un conteneur à recherche de style dictionnaire garantissant O(K) ou O(log N) recherches, et que le conteneur sera plus grand (plusieurs kilo-octets) et que vous effectuez fréquemment des insertions de sorte que le surcoût de maintien d'un `vector` trié est prohibitif, utilisez plutôt un `unordered_map` ou un `map`.

##### Remarque

Pour initialiser un `vector` avec un nombre d'éléments, utilisez l'initialisation `()`-initial. Pour initialiser un `vector` avec une liste d'éléments, utilisez l'initialisation `{}`-initial.

    vector<int> v1(20);  // v1 a 20 éléments avec la valeur 0 (vector<int>{})
    vector<int> v2 {20}; // v2 a 1 élément avec la valeur 20

[Préférer la syntaxe d'initialisation {}](010-expr.md#res-list).

##### Mise en œuvre

* Signaler un `vector` dont la taille ne change jamais après la construction (par exemple, s'il est `const` ou si aucune fonction non‑`const` n'est appelée). À corriger : utiliser `array` à la place.

### <a name="rsl-bounds"></a>SL.con.3: Éviter les dépassements de limites

##### Raison

Lire ou écrire au-delà d'une plage allouée d'éléments conduit généralement à de mauvaises erreurs, résultats erronés, plantages et violations de sécurité.

##### Remarque

Les fonctions de la bibliothèque standard qui s'appliquent à des plages d'éléments ont toutes (ou peuvent avoir) des surcharges sécurisées en termes de limites qui prennent `span`. Les types standards tels que `vector` peuvent être modifiés pour effectuer des vérifications de limites dans le profil de limites (de façon compatible, par ex. en ajoutant des contrats), ou être utilisés avec `at()`.

Idéalement, la garantie d'être dans les limites devrait être imposée statiquement. Par exemple :
- Un boucle `for` sur une plage ne peut pas dépasser la plage du conteneur auquel elle est appliquée.
- Une paire `v.begin(), v.end()` est aisément considérée comme sûre en termes de limites.

De telles boucles sont aussi rapides que toute version sans vérification/unsafe. Souvent, une simple vérification préalable peut éliminer le besoin de vérifier chaque indice. Par exemple :
* pour `v.begin(), v.begin()+i`, le `i` peut facilement être vérifié par rapport à `v.size()`

Ces boucles peuvent être beaucoup plus rapides que les accès aux éléments vérifiés individuellement.

##### Exemple, mauvais

    void f()
    {
        array<int, 10> a, b;
        memset(a.data(), 0, 10);         // MAUVE, et contient une erreur de longueur (longueur = 10 * sizeof(int))
        memcmp(a.data(), b.data(), 10);  // MAUVE, et contient une erreur de longueur (longueur = 10 * sizeof(int))
    }

##### Exemple, bon

    void f()
    {
        array<int, 10> a, b, c{};       // c est initialisé à zéro
        a.fill(0);
        fill(b.begin(), b.end(), 0);    // std::fill()
        fill(b, 0);                     // std::ranges::fill()

        if ( a == b ) {
          // ...
        }
    }

##### Exemple

    void f(std::vector<int>& v, std::array<int, 12> a, int i)
    {
        v[0] = a[0];        // MAUVE
        v.at(0) = a[0];     // OK (alternative 1)
        at(v, 0) = a[0];    // OK (alternative 2)

        v.at(0) = a[i];     // MAUVE
        v.at(0) = a.at(i);  // OK (alternative 1)
        v.at(0) = at(a, i); // OK (alternative 2)
    }

##### Mise en œuvre

* Émettre un diagnostic pour tout appel à une fonction de la bibliothèque standard qui n'est pas vérifiée en termes de limites.  
    ??? insérer un lien vers une liste de fonctions interdites

Cette règle fait partie du [profil de limites](022-profile.md#ss-bounds).

### <a name="rsl-copy"></a>SL.con.4: Ne pas utiliser `memset` ou `memcpy` pour des arguments qui ne sont pas directement copiables

##### Raison

Le fait de le faire perturbe la sémantique des objets (par ex., en écrasant un vptr).

##### Remarque

Également pour (w)memset, (w)memcpy, (w)memmove, et (w)memcmp.

##### Exemple

    struct base {
        virtual void update() = 0;
    };

    struct derived : public base {
        void update() override {}
    };

    void f(derived& a, derived& b) // adieu aux tables virtuelles
    {
        memset(&a, 0, sizeof(derived));
        memcpy(&a, &b, sizeof(derived));
        memcmp(&a, &b, sizeof(derived));
    }

Au lieu de cela, définissez une initialisation, une copie et une fonction de comparaison appropriées :

    void g(derived& a, derived& b)
    {
        a = {};    // initialisation par défaut
        b = a;     // copie
        if (a == b) do_something(a, b);
    }

##### Mise en œuvre

* Signaler l'utilisation de ces fonctions pour des types qui ne sont pas trivialement copiables.

**Notes à faire** :

* L'impact sur la bibliothèque standard devra nécessiter une coordination étroite avec WG21, si ce n'est que pour assurer la compatibilité même s'il n'est jamais standardisé.
* Nous envisageons de spécifier des surcharges sécurisées en termes de limites pour les fonctions de la bibliothèque standard (en particulier C stdlib) comme `memcmp` et de les livrer dans la GSL.
* Pour les fonctions et types existants de la stdlib tels que `vector` qui ne sont pas entièrement vérifiés, l'objectif est que ces caractéristiques soient vérifiées en mode profil limites lorsqu'elles sont appelées depuis du code avec le profil limites activé, et non vérifiées lorsqu'elles sont appelées depuis un code hérité, éventuellement en utilisant des contrats (proposé simultanément par plusieurs membres de WG21).

---

## <a name="ss-string"></a>SL.str: Chaîne de caractères

La manipulation de texte est un sujet vaste. `std::string` ne couvre pas tout. Cette section cherche principalement à clarifier la relation de `std::string` avec `char*`, `zstring`, `std::string_view` et `gsl::span<char>`. La question importante des jeux de caractères non ASCII et des encodages (par ex., `wchar_t`, Unicode, et UTF‑8) sera abordée ailleurs.

**Voir aussi** : [expressions régulières](018-stdlib.md#ss-regex)

Ici, nous utilisons les termes « séquence de caractères » ou « chaîne » pour désigner une séquence de caractères destinée à être lue comme texte (d'une façon ou d'une autre, éventuellement). Nous ne considérons pas ???.

Résumé des chaînes :

* [SL.str.1: Utiliser `std::string` pour posséder des séquences de caractères](018-stdlib.md#rstr-string)
* [SL.str.2: Utiliser `std::string_view` ou `gsl::span<char>` pour référer à des séquences de caractères](018-stdlib.md#rstr-view)
* [SL.str.3: Utiliser `zstring` ou `czstring` pour référer à une séquence de caractères de style C terminée par zéro](018-stdlib.md#rstr-zstring)
* [SL.str.4: Utiliser `char*` pour référer à un seul caractère](018-stdlib.md#rstr-charp)
* [SL.str.5: Utiliser `std::byte` pour référer à des valeurs d'octets qui ne représentent pas nécessairement des caractères](018-stdlib.md#rstr-byte)

* [SL.str.10: Utiliser `std::string` lorsque vous avez besoin de réaliser des opérations de chaînes sensibles aux paramètres d'environnement](018-stdlib.md#rstr-locale)
* [SL.str.11: Utiliser `gsl::span<char>` plutôt que `std::string_view` lorsqu'il faut modifier une chaîne](018-stdlib.md#rstr-span)
* [SL.str.12: Utiliser le suffixe `s` pour les littéraux de chaînes destinés à être des `std::string` de la bibliothèque standard](018-stdlib.md#rstr-s)

**Voir aussi** :

* [F.24 span](006-functions.md#rf-range)
* [F.25 zstring](006-functions.md#rf-zstring)

### <a name="rstr-string"></a>SL.str.1: Utiliser `std::string` pour posséder des séquences de caractères

##### Raison

`string` gère correctement l'allocation, la possession, la copie, l'expansion progressive et propose une variété d'opérations utiles.

##### Exemple

    vector<string> read_until(const string& terminator)
    {
        vector<string> res;
        for (string s; cin >> s && s != terminator; ) // lire un mot
            res.push_back(s);
        return res;
    }

Remarquez que `>>` et `!=` sont fournis pour `string` (en guise d'exemples d'opérations utiles) et qu'il n'y a aucune allocation, désallocation ou vérification d'intervalle explicites (`string` s'occupe de ces aspects).

En C++17, nous pourrions utiliser `string_view` comme argument, plutôt que `const string&` afin de laisser plus de flexibilité aux appelants :

    vector<string> read_until(string_view terminator)   // C++17
    {
        vector<string> res;
        for (string s; cin >> s && s != terminator; ) // lire un mot
            res.push_back(s);
        return res;
    }

##### Exemple, mauvais

Ne pas utiliser les chaînes de style C pour des opérations qui nécessitent une gestion mémoire non triviale

    char* cat(const char* s1, const char* s2)   // attention !
        // renvoie s1 + '.' + s2
    {
        int l1 = strlen(s1);
        int l2 = strlen(s2);
        char* p = (char*) malloc(l1 + l2 + 2);
        strcpy(p, s1, l1);
        p[l1] = '.';
        strcpy(p + l1 + 1, s2, l2);
        p[l1 + l2 + 1] = 0;
        return p;
    }

Avons-nous bien compris ? L'appelant se souviendra‑t‑il d'appeler `free()` sur le pointeur retourné ? Ce code passera‑t‑il un examen de sécurité ?

##### Remarque

Ne supposez pas que `string` soit plus lent que les techniques de bas niveau sans mesure et rappelez‑vous que tout le code n'est pas critique en performance. [Ne pas optimiser prématurément](011-performance.md#rper-knuth)

##### Mise en œuvre

???

### <a name="rstr-view"></a>SL.str.2: Utiliser `std::string_view` ou `gsl::span<char>` pour référer à des séquences de caractères

##### Raison

`std::string_view` ou `gsl::span<char>` offre un accès simple et (potentiellement) sécurisé aux séquences de caractères, indépendamment de leur mode d'allocation ou de stockage.

##### Exemple

    vector<string> read_until(string_view terminator);

    void user(zstring p, const string& s, string_view ss)
    {
        auto v1 = read_until(p);
        auto v2 = read_until(s);
        auto v3 = read_until(ss);
        // ...
    }

##### Remarque

`std::string_view` (C++17) est en lecture seule.

##### Mise en œuvre

???

### <a name="rstr-zstring"></a>SL.str.3: Utiliser `zstring` ou `czstring` pour référer à une séquence de caractères de style C terminée par zéro

##### Raison

Lisibilité. Déclaration d'intention. Un `char*` simple peut pointer vers un seul caractère, un pointeur vers un tableau de caractères, un pointeur vers une chaîne de caractères de style C terminée par zéro, ou même vers un petit entier. Différencier ces alternatives empêche les malentendus et les bugs.

##### Exemple

    void f1(const char* s); // s est probablement une chaîne

    void f1(zstring s);     // s est une chaîne de style C ou le pointeur nul
    void f1(czstring s);    // s est une chaîne de style C constante ou le pointeur nul
    void f1(std::byte* s);  // s est un pointeur vers un byte (C++17)

##### Remarque

Ne convertissez pas une chaîne de style C en `string` à moins qu'il n'y ait une raison.

##### Remarque

Comme tout autre « pointeur simple », un `zstring` ne doit pas signifier la possession.

##### Remarque

Il existe des milliards de lignes de C++ « out there », la plupart utilisent `char*` et `const char*` sans documenter l'intention. Ils sont utilisés dans une variété de façons, y compris pour représenter la possession et comme pointeurs génériques vers la mémoire (au lieu de `void*`). Il est difficile de séparer ces usages, donc cette directive est difficile à suivre. C'est l'une des principales sources de bugs dans les programmes C et C++, il est donc utile de suivre cette directive autant que possible.

##### Mise en œuvre

* Signaler l'utilisation de `[]` sur un `char*`
* Signaler l'utilisation de `delete` sur un `char*`
* Signaler l'utilisation de `free()` sur un `char*`

### <a name="rstr-charp"></a>SL.str.4: Utiliser `char*` pour référer à un seul caractère

##### Raison

La variété d'usages de `char*` dans le code actuel est une source majeure d'erreurs.

##### Exemple, mauvais

    char arr[] = {'a', 'b', 'c'};

    void print(const char* p)
    {
        cout << p << '\n';
    }

    void use()
    {
        print(arr);   // Erreur d'exécution ; potentiellement très mauvaise
    }

##### Alternative

Voir `zstring`, `string`, et `string_view`.

##### Mise en œuvre

* Signaler l'utilisation de `[]` sur un `char*`

### <a name="rstr-byte"></a>SL.str.5: Utiliser `std::byte` pour référer à des valeurs d'octets qui ne représentent pas nécessairement des caractères

##### Raison

L'utilisation de `char*` pour représenter un pointeur vers quelque chose qui n'est pas nécessairement un caractère crée de la confusion et désactive les optimisations précieuses.

##### Exemple

???

##### Remarque

C++17

##### Mise en œuvre

???

### <a name="rstr-locale"></a>SL.str.10: Utiliser `std::string` lorsque vous avez besoin de réaliser des opérations de chaînes sensibles aux paramètres d'environnement

##### Raison

`std::string` prend en charge les fonctionnalités de localisation de la bibliothèque standard.

##### Exemple

???

##### Remarque

???

##### Mise en œuvre

???

### <a name="rstr-span"></a>SL.str.11: Utiliser `gsl::span<char>` plutôt que `std::string_view` lorsqu'il faut modifier une chaîne

##### Raison

`std::string_view` est en lecture seule.

##### Exemple

???

##### Remarque

???

##### Mise en œuvre

Le compilateur indiquera les tentatives d'écriture sur un `string_view`.

### <a name="rstr-s"></a>SL.str.12: Utiliser le suffixe `s` pour les littéraux de chaînes destinés à être des `std::string` de la bibliothèque standard

##### Raison

Exprimer directement une idée minimise les erreurs.

##### Exemple

    auto pp1 = make_pair("Tokyo", 9.00);         // {chaîne C, double} prévu ?
    pair<string, double> pp2 = {"Tokyo", 9.00};  // un peu verbeux
    auto pp3 = make_pair("Tokyo"s, 9.00);        // {std::string,double}    // C++14
    pair pp4 = {"Tokyo"s, 9.00};                 // {std::string,double}    // C++17

##### Mise en œuvre

???

---

## <a name="ss-io"></a>SL.io: Iostream

Les iostreams sont une bibliothèque d'E/S type‑safe, extensible, formatée et non formatée pour le streaming d'E/S. Ils prennent en charge plusieurs stratégies de tamponnement (y compris celles extensibles par l'utilisateur) et plusieurs locales. Ils peuvent être utilisés pour l'E/S conventionnelle, la lecture et l'écriture en mémoire (flux de chaînes), et les extensions définies par l'utilisateur, comme le streaming sur les réseaux (asio : pas encore standardisé).

Résumé des règles Iostream :

* [SL.io.1: Utiliser l'entrée au niveau des caractères seulement quand c'est nécessaire](018-stdlib.md#rio-low)
* [SL.io.2: Lors de la lecture, considérer toujours les entrées mal formées](018-stdlib.md#rio-validate)
* [SL.io.3: Préférer les iostreams pour l'E/S](018-stdlib.md#rio-streams)
* [SL.io.10: À moins d'utiliser la famille de fonctions `printf` appelez `ios_base::sync_with_stdio(false)`](018-stdlib.md#rio-sync)
* [SL.io.50: Éviter `endl`](018-stdlib.md#rio-endl)
* * ???  

### <a name="rio-low"></a>SL.io.1: Utiliser l'entrée au niveau des caractères seulement quand c'est nécessaire

##### Raison

À moins de réellement ne traiter qu'avec des caractères individuels, l'utilisation d'une entrée au niveau des caractères conduit le code utilisateur à composer potentiellement des jetons à partir de caractères, un processus subject à erreurs et potentiellement inefficace.

##### Exemple

    char c;
    char buf[128];
    int i = 0;
    while (cin.get(c) && !isspace(c) && i < 128)
        buf[i++] = c;
    if (i == 128) {
        // ... gérer chaîne trop longue ....
    }

Meilleur (beaucoup plus simple et probablement plus rapide) :

    string s;
    s.reserve(128);
    cin >> s;

et la `reserve(128)` n'est probablement pas utile.

##### Mise en œuvre

???

### <a name="rio-validate"></a>SL.io.2: Lors de la lecture, considérer toujours les entrées mal formées

##### Raison

???

##### Exemple

    ???

##### Mise en œuvre

???

### <a name="rio-streams"></a>SL.io.3: Préférer les `iostream`s pour l'E/S

##### Raison

`iostreams` sont sûres, flexibles et extensibles.

##### Exemple

    // écrire un nombre complexe :
    complex<double> z{ 3, 4 };
    cout << z << '\n';

##### Exemple

    // lire un fichier de nombres complexes :
    for (complex<double> z; cin >> z; )
        v.push_back(z);

##### Exception

??? performance ???

##### Discussion : iostreams vs la famille `printf`

Il est souvent (et souvent correctement) pointé que la famille `printf` a deux avantages par rapport aux `iostream`s : flexibilité du formatage et performance. Il faut pondérer ces avantages contre ceux des `iostream`s, à savoir l'extensibilité pour gérer les types définis par l'utilisateur, la résilience aux violations de sécurité, la gestion implicite de la mémoire et la prise en charge des locales.

Si vous avez besoin de performances I/O, vous pouvez presque toujours faire mieux que `printf()`.

`gets()` , `scanf()` utilisant `%s`, et `printf()` utilisant `%s` sont des risques de sécurité (vulnérables aux dépassements de tampon et généralement source d'erreurs). C11 définit certaines « extensions optionnelles » qui effectuent un contrôle supplémentaire de leurs arguments. Si elles sont présentes dans votre bibliothèque C, `gets_s()`, `scanf_s()`, et `printf_s()` pourraient être des alternatives plus sûres, mais elles ne sont toujours pas sécurisées en termes de type.

##### Mise en œuvre

Optionnellement, signaler `<cstdio>` et `<stdio.h>`.

### <a name="rio-sync"></a>SL.io.10: À moins d'utiliser la famille de fonctions `printf` appelez `ios_base::sync_with_stdio(false)`

##### Raison

La synchronisation des `iostreams` avec l'I/O de style `printf` peut être coûteuse. `cin` et `cout` sont synchronisés par défaut avec `printf`.

##### Exemple

    int main()
    {
        ios_base::sync_with_stdio(false);
        // ... utiliser les iostreams ...
    }

##### Mise en œuvre

???

### <a name="rio-endl"></a>SL.io.50: Éviter `endl`

##### Raison

Le manipulant `endl` est essentiellement équivalent à `'\n'` et à `"\n"`. S'il est le plus couramment utilisé, il ralentit simplement la sortie en effectuant des `flush()` inutiles. Ce ralentissement peut être significatif par rapport à la sortie de style `printf`.

##### Exemple

    cout << "Hello, World!" << endl;    // deux opérations d'affichage et un flush
    cout << "Hello, World!\n";          // une opération d'affichage et aucun flush

##### Remarque

Pour l'interaction `cin`/`cout` (et équivalents), il n'y a aucune raison de faire un `flush` ; cela est effectué automatiquement.

Pour l'écriture vers un fichier, il n'y a rarement besoin de `flush`.

Pour les flux de chaînes (spécialement `ostringstream`), l'insertion d'un `endl` est entièrement équivalente à l'insertion d'un caractère `'\n'`, mais dans ce cas, `endl` peut être significativement plus lent.

`endl` ne prend pas en charge la production d'un indicateur de fin de ligne spécifique à la plateforme (comme `"\r\n"` sur Windows). Ainsi, pour un flux de chaînes, `s << endl` insère simplement un caractère unique, `'\n'`.

À part le problème de performance (éventuellement important), le choix entre `'\n'` et `endl` est presque entièrement esthétique.

---

## <a name="ss-regex"></a>SL.regex: Expressions régulières

`<regex>` est la bibliothèque standard de C++ pour les expressions régulières. Elle prend en charge une variété de conventions de motifs d'expressions régulières. Pour un travail à haute performance, envisagez d'utiliser une bibliothèque d'expressions régulières tierce.

---

## <a name="ss-chrono"></a>SL.chrono: Temps

`<chrono>` (défini dans l'espace de noms `std::chrono`) fournit les notions de `time_point` et `duration` ainsi que des fonctions pour l'affichage du temps dans diverses unités. Il fournit des horloges pour enregistrer des `time_point`.

---

## <a name="ss-clib"></a>SL.C: La bibliothèque standard C

Résumé des règles de la bibliothèque standard C :

* [SL.C.1: Ne pas utiliser setjmp/longjmp](018-stdlib.md#rclib-jmp)
* * ???  
* * ???  

### <a name="rclib-jmp"></a>SL.C.1: Ne pas utiliser setjmp/longjmp

##### Raison

Un `longjmp` ignore les destructeurs ; ce qui invalide toutes les stratégies de gestion de ressources reposant sur RAII.

##### Mise en œuvre

Signaliser toutes les occurrences de `longjmp` et de `setjmp`.