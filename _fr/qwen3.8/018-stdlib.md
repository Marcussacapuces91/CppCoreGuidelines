# <a name="s-stdlib"></a>SL : La bibliothèque standard

En utilisant uniquement le langage nu, chaque tâche est fastidieuse (dans n'importe quel langage).
En utilisant une bibliothèque adaptée, toute tâche peut être raisonnablement simple.

La bibliothèque standard a considérablement grandi au fil des années.
Sa description dans la norme est désormais plus volumineuse que celle des fonctionnalités du langage.
Il est donc probable que cette section de la bibliothèque des lignes directrices finira par atteindre, voire dépasser, la taille du reste du document.

<< ??? Nous avons besoin d'un autre niveau de numérotation des règles ??? >>

Résumé des composants de la bibliothèque standard C++ :

* [SL.con : Conteneurs](018-stdlib.md#ss-con)
* [SL.str : Chaînes de caractères](018-stdlib.md#ss-string)
* [SL.io : Iostream](018-stdlib.md#ss-io)
* [SL.regex : Expressions régulières](018-stdlib.md#ss-regex)
* [SL.chrono : Temps](018-stdlib.md#ss-chrono)
* [SL.C : La bibliothèque standard C](018-stdlib.md#ss-clib)

Résumé des règles de la bibliothèque standard :

* [SL.1 : Utiliser des bibliothèques dès que possible](018-stdlib.md#rsl-lib)
* [SL.2 : Privilégier la bibliothèque standard aux autres bibliothèques](018-stdlib.md#rsl-sl)
* [SL.3 : Ne pas ajouter d'entités non standard dans l'espace de noms `std`](018-stdlib.md#sl-std)
* [SL.4 : Utiliser la bibliothèque standard de manière sûre du point de vue des types](018-stdlib.md#sl-safe)
* ???

### <a name="rsl-lib"></a>SL.1 : Utiliser des bibliothèques dès que possible

##### Justification

Gagner du temps. Ne pas réinventer la roue.
Ne pas dupliquer le travail des autres.
Bénéficier des améliorations apportées par d'autres.
Aider les autres lorsque vous apportez des améliorations.

### <a name="rsl-sl"></a>SL.2 : Privilégier la bibliothèque standard aux autres bibliothèques

##### Justification

Plus de personnes connaissent la bibliothèque standard.
Elle est plus susceptible d'être stable, bien maintenue et largement disponible que votre propre code ou la plupart des autres bibliothèques.


### <a name="sl-std"></a>SL.3 : Ne pas ajouter d'entités non standard dans l'espace de noms `std`

##### Justification

L'ajout d'entités dans `std` peut modifier la signification de code autrement conforme à la norme.
Les ajouts dans `std` peuvent entrer en conflit avec des versions futures de la norme.

##### Exemple

    namespace std { // MAUVAIS : viole la norme

    class My_vector {
        //     . . .
    };

    }

    namespace Foo { // BON : un espace de noms utilisateur est autorisé

    class My_vector {
        //     . . .
    };

    }

##### Application

Possible, mais fastidieux et susceptible de poser des problèmes avec certaines plateformes.

### <a name="sl-safe"></a>SL.4 : Utiliser la bibliothèque standard de manière sûre du point de vue des types

##### Justification

Parce que, évidemment, le non-respect de cette règle peut conduire à un comportement indéfini, à une corruption de la mémoire et à toutes sortes d'autres erreurs graves.

##### Remarque

Il s'agit d'une méta-règle semi-philosophique, qui nécessite de nombreuses règles concrètes de soutien.
Nous en avons besoin comme parapluie pour les règles plus spécifiques.

Résumé des règles plus spécifiques :

* [SL.4 : Utiliser la bibliothèque standard de manière sûre du point de vue des types](018-stdlib.md#sl-safe)


## <a name="ss-con"></a>SL.con : Conteneurs

???

Résumé des règles sur les conteneurs :

* [SL.con.1 : Privilégier l'utilisation de `array` ou `vector` de la STL plutôt qu'un tableau C](018-stdlib.md#rsl-arrays)
* [SL.con.2 : Privilégier l'utilisation de `vector` de la STL par défaut, sauf si vous avez une raison d'utiliser un autre conteneur](018-stdlib.md#rsl-vector)
* [SL.con.3 : Éviter les erreurs de bornes](018-stdlib.md#rsl-bounds)
* [SL.con.4 : Ne pas utiliser `memset` ou `memcpy` pour des arguments qui ne sont pas copiables de manière triviale](018-stdlib.md#rsl-copy)

### <a name="rsl-arrays"></a>SL.con.1 : Privilégier l'utilisation de `array` ou `vector` de la STL plutôt qu'un tableau C

##### Justification

Les tableaux C sont moins sûrs et n'ont aucun avantage sur `array` et `vector`.
Pour un tableau de longueur fixe, utilisez `std::array`, qui ne se dégrade pas en pointeur lorsqu'il est passé à une fonction et qui connaît sa taille.
De plus, comme un tableau intégré, un `std::array` alloué sur la pile conserve ses éléments sur la pile.
Pour un tableau de longueur variable, utilisez `std::vector`, qui peut en outre changer de taille et gère l'allocation mémoire.

##### Exemple

    int v[SIZE];                        // MAUVAIS

    std::array<int, SIZE> w;            // correct

##### Exemple

    int* v = new int[initial_size];     // MAUVAIS, pointeur brut propriétaire
    delete[] v;                         // MAUVAIS, suppression manuelle

    std::vector<int> w(initial_size);   // correct

##### Remarque

Utilisez `gsl::span` pour les références non propriétaires vers un conteneur.

##### Remarque

Comparer les performances d'un tableau de taille fixe alloué sur la pile avec un `vector` dont les éléments sont sur la zone libre est absurde.
Vous pourriez tout aussi bien comparer un `std::array` sur la pile avec le résultat d'un `malloc()` accédé via un pointeur.
Pour la plupart du code, même la différence entre l'allocation sur la pile et l'allocation sur la zone libre n'a pas d'importance, mais la commodité et la sécurité de `vector`, si.
Les personnes travaillant sur du code pour lequel cette différence compte sont tout à fait capables de choisir entre `array` et `vector`.

##### Application

* Signaler la déclaration d'un tableau C dans une fonction ou une classe qui déclare également un conteneur STL (pour éviter des avertissements excessifs sur du code legacy non-STL). Pour corriger : remplacer au minimum le tableau C par un `std::array`.

### <a name="rsl-vector"></a>SL.con.2 : Privilégier l'utilisation de `vector` de la STL par défaut, sauf si vous avez une raison d'utiliser un autre conteneur

##### Justification

`vector` et `array` sont les seuls conteneurs standard qui offrent les avantages suivants :

* l'accès général le plus rapide (accès aléatoire, y compris la compatibilité avec la vectorisation) ;
* le schéma d'accès par défaut le plus rapide (du début à la fin ou de la fin au début est compatible avec le préchargeur) ;
* la surcharge spatiale la plus faible (la disposition contiguë n'a aucune surcharge par élément, ce qui est compatible avec le cache).

En général, vous devez ajouter et supprimer des éléments du conteneur, utilisez donc `vector` par défaut ; si vous n'avez pas besoin de modifier la taille du conteneur, utilisez `array`.

Même lorsque d'autres conteneurs semblent plus adaptés, comme `map` pour des performances de recherche en O(log N) ou une `list` pour une insertion efficace en milieu de liste, un `vector` aura généralement de meilleures performances pour des conteneurs de quelques Ko.

##### Remarque

`string` ne doit pas être utilisé comme conteneur de caractères individuels. Une `string` est une chaîne de caractères textuelle ; si vous souhaitez un conteneur de caractères, utilisez `vector</*char_type*/>` ou `array</*char_type*/>` à la place.

##### Exceptions

Si vous avez une bonne raison d'utiliser un autre conteneur, utilisez-le. Par exemple :

* Si `vector` convient à vos besoins mais que vous n'avez pas besoin d'un conteneur de taille variable, utilisez `array` à la place.

* Si vous souhaitez un conteneur de recherche de type dictionnaire garantissant des recherches en O(K) ou O(log N), que le conteneur sera plus volumineux (plus de quelques Ko) et que vous effectuez des insertions fréquentes rendant la surcharge de maintenance d'un `vector` trié inacceptable, utilisez alors `unordered_map` ou `map`.

##### Remarque

Pour initialiser un vector avec un nombre d'éléments, utilisez l'initialisation par `()`.
Pour initialiser un vector avec une liste d'éléments, utilisez l'initialisation par `{}`.

    vector<int> v1(20);  // v1 a 20 éléments de valeur 0 (vector<int>{})
    vector<int> v2 {20}; // v2 a 1 élément de valeur 20

[Privilégier la syntaxe d'initialisation {}](010-expr.md#res-list).

##### Application

* Signaler un `vector` dont la taille ne change jamais après la construction (par exemple parce qu'il est `const` ou parce qu'aucune fonction non-`const` n'est appelée dessus). Pour corriger : utiliser un `array` à la place.

### <a name="rsl-bounds"></a>SL.con.3 : Éviter les erreurs de bornes

##### Justification

Lire ou écrire au-delà d'une plage d'éléments alloués conduit typiquement à des erreurs graves, des résultats incorrects, des plantages et des violations de sécurité.

##### Remarque

Les fonctions de la bibliothèque standard qui s'appliquent à des plages d'éléments ont toutes (ou pourraient avoir) des surcharges sûres sur les bornes qui prennent un `span`.
Les types standard tels que `vector` peuvent être modifiés pour effectuer des vérifications de bornes sous le profil de bornes (de manière compatible, par exemple en ajoutant des contrats), ou utilisés avec `at()`.

Idéalement, la garantie de bornes devrait être appliquée statiquement.
Par exemple :

* une boucle `for` sur une plage ne peut pas dépasser la plage du conteneur auquel elle s'applique
* un `v.begin(),v.end()` est facilement déterminé comme sûr sur les bornes

De telles boucles sont aussi rapides que n'importe quel équivalent non vérifié/non sûr.

Souvent, une simple vérification préalable peut éliminer le besoin de vérifier chaque index individuellement.
Par exemple

* pour `v.begin(),v.begin()+i`, le `i` peut facilement être vérifié par rapport à `v.size()`

De telles boucles peuvent être beaucoup plus rapides que des accès aux éléments individuellement vérifiés.

##### Exemple, incorrect

    void f()
    {
        array<int, 10> a, b;
        memset(a.data(), 0, 10);         // MAUVAIS, et contient une erreur de longueur (longueur = 10 * sizeof(int))
        memcmp(a.data(), b.data(), 10);  // MAUVAIS, et contient une erreur de longueur (longueur = 10 * sizeof(int))
    }

De plus, `std::array<>::fill()` ou `std::fill()` ou même un initialiseur vide sont de meilleurs candidats que `memset()`.

##### Exemple, correct

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

Si le code utilise une bibliothèque standard non modifiée, il existe encore des solutions de contournement permettant d'utiliser `std::array` et `std::vector` de manière sûre sur les bornes. Le code peut appeler la fonction membre `.at()` sur chaque classe, ce qui entraînera le lancement d'une exception `std::out_of_range`. Alternativement, le code peut appeler la fonction libre `at()`, ce qui entraînera un échec rapide (ou une action personnalisée) en cas de violation de bornes.

    void f(std::vector<int>& v, std::array<int, 12> a, int i)
    {
        v[0] = a[0];        // MAUVAIS
        v.at(0) = a[0];     // CORRECT (alternative 1)
        at(v, 0) = a[0];    // CORRECT (alternative 2)

        v.at(0) = a[i];     // MAUVAIS
        v.at(0) = a.at(i);  // CORRECT (alternative 1)
        v.at(0) = at(a, i); // CORRECT (alternative 2)
    }

##### Application

* Émettre un diagnostic pour tout appel à une fonction de la bibliothèque standard qui n'est pas vérifiée sur les bornes.
??? insérer un lien vers une liste de fonctions interdites

Cette règle fait partie du [profil de bornes](022-profile.md#ss-bounds).


### <a name="rsl-copy"></a>SL.con.4 : Ne pas utiliser `memset` ou `memcpy` pour des arguments qui ne sont pas copiables de manière triviale

##### Justification

Le faire altère la sémantique des objets (par exemple en écrasant un `vptr`).

##### Remarque

De même pour (w)memset, (w)memcpy, (w)memmove et (w)memcmp

##### Exemple

    struct base {
        virtual void update() = 0;
    };

    struct derived : public base {
        void update() override {}
    };


    void f(derived& a, derived& b) // au revoir les tables de vptr
    {
        memset(&a, 0, sizeof(derived));
        memcpy(&a, &b, sizeof(derived));
        memcmp(&a, &b, sizeof(derived));
    }

À la place, définissez des fonctions d'initialisation par défaut, de copie et de comparaison appropriées

    void g(derived& a, derived& b)
    {
        a = {};    // initialisation par défaut
        b = a;     // copie
        if (a == b) do_something(a, b);
    }

##### Application

* Signaler l'utilisation de ces fonctions pour des types qui ne sont pas copiables de manière triviale

**Notes TODO** :

* L'impact sur la bibliothèque standard nécessitera une coordination étroite avec le WG21, ne serait-ce que pour assurer la compatibilité, même si elle n'est jamais normalisée.
* Nous envisageons de spécifier des surcharges sûres sur les bornes pour les fonctions de la bibliothèque standard (en particulier la bibliothèque standard C) comme `memcmp` et de les livrer dans la GSL.
* Pour les fonctions et types existants de la bibliothèque standard comme `vector` qui ne sont pas entièrement vérifiés sur les bornes, l'objectif est que ces fonctionnalités soient vérifiées sur les bornes lorsqu'elles sont appelées depuis du code avec le profil de bornes activé, et non vérifiées lorsqu'elles sont appelées depuis du code legacy, éventuellement en utilisant des contrats (proposés simultanément par plusieurs membres du WG21).



## <a name="ss-string"></a>SL.str : Chaînes de caractères

La manipulation de texte est un vaste sujet.
`std::string` ne couvre pas tout.
Cette section tente principalement de clarifier la relation de `std::string` avec `char*`, `zstring`, `string_view` et `gsl::span<char>`.
Le problème important des jeux de caractères et encodages non-ASCII (par exemple `wchar_t`, Unicode et UTF-8) sera traité ailleurs.

**Voir aussi** : [expressions régulières](018-stdlib.md#ss-regex)

Ici, nous utilisons « séquence de caractères » ou « chaîne » pour désigner une séquence de caractères destinée à être lue comme du texte (d'une manière ou d'une autre, à terme).
Nous ne considérons pas ???

Résumé des règles sur les chaînes :

* [SL.str.1 : Utiliser `std::string` pour posséder des séquences de caractères](018-stdlib.md#rstr-string)
* [SL.str.2 : Utiliser `std::string_view` ou `gsl::span<char>` pour référencer des séquences de caractères](018-stdlib.md#rstr-view)
* [SL.str.3 : Utiliser `zstring` ou `czstring` pour référencer une séquence de caractères de style C, terminée par zéro](018-stdlib.md#rstr-zstring)
* [SL.str.4 : Utiliser `char*` pour référencer un caractère unique](018-stdlib.md#rstr-charp)
* [SL.str.5 : Utiliser `std::byte` pour référencer des valeurs d'octets qui ne représentent pas nécessairement des caractères](018-stdlib.md#rstr-byte)

* [SL.str.10 : Utiliser `std::string` lorsque vous devez effectuer des opérations sur les chaînes sensibles à la localisation](018-stdlib.md#rstr-locale)
* [SL.str.11 : Utiliser `gsl::span<char>` plutôt que `std::string_view` lorsque vous devez modifier une chaîne](018-stdlib.md#rstr-span)
* [SL.str.12 : Utiliser le suffixe `s` pour les littéraux de chaînes destinés à être des `string` de la bibliothèque standard](018-stdlib.md#rstr-s)

**Voir aussi** :

* [F.24 span](006-functions.md#rf-range)
* [F.25 zstring](006-functions.md#rf-zstring)


### <a name="rstr-string"></a>SL.str.1 : Utiliser `std::string` pour posséder des séquences de caractères

##### Justification

`string` gère correctement l'allocation, la propriété, la copie, l'expansion progressive et offre une variété d'opérations utiles.

##### Exemple

    vector<string> read_until(const string& terminator)
    {
        vector<string> res;
        for (string s; cin >> s && s != terminator; ) // lire un mot
            res.push_back(s);
        return res;
    }

Notez que `>>` et `!=` sont fournis pour `string` (en tant qu'exemples d'opérations utiles) et qu'il n'y a pas d'allocations, de désallocations ou de vérifications de bornes explicites (`string` s'en charge).

En C++17, nous pourrions utiliser `string_view` comme argument, plutôt que `const string&`, pour offrir plus de flexibilité aux appelants :

    vector<string> read_until(string_view terminator)   // C++17
    {
        vector<string> res;
        for (string s; cin >> s && s != terminator; ) // lire un mot
            res.push_back(s);
        return res;
    }

##### Exemple, incorrect

N'utilisez pas de chaînes de style C pour des opérations nécessitant une gestion mémoire non triviale

    char* cat(const char* s1, const char* s2)   // attention !
        // retourne s1 + '.' + s2
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

Avons-nous bien fait ?
L'appelant se souviendra-t-il d'appeler `free()` sur le pointeur retourné ?
Ce code passera-t-il un audit de sécurité ?

##### Remarque

Ne supposez pas que `string` est plus lent que des techniques de bas niveau sans mesurer, et rappelez-vous que tout le code n'est pas critique en termes de performances.
[Ne pas optimiser prématurément](011-performance.md#rper-knuth)

##### Application

???

### <a name="rstr-view"></a>SL.str.2 : Utiliser `std::string_view` ou `gsl::span<char>` pour référencer des séquences de caractères

##### Justification

`std::string_view` ou `gsl::span<char>` fournit un accès simple et (potentiellement) sûr aux séquences de caractères, indépendamment de la manière dont
ces séquences sont allouées et stockées.

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

##### Application

???

### <a name="rstr-zstring"></a>SL.str.3 : Utiliser `zstring` ou `czstring` pour référencer une séquence de caractères de style C, terminée par zéro

##### Justification

Lisibilité.
Expression d'intention.
Un simple `char*` peut être un pointeur vers un caractère unique, un pointeur vers un tableau de caractères, un pointeur vers une chaîne de style C (terminée par zéro), ou même vers un petit entier.
Distinguer ces alternatives prévient les malentendus et les bogues.

##### Exemple

    void f1(const char* s); // s est probablement une chaîne

Tout ce que nous savons, c'est qu'elle est censée être nullptr ou pointer vers au moins un caractère

    void f1(zstring s);     // s est une chaîne de style C ou nullptr
    void f1(czstring s);    // s est une constante de chaîne de style C ou nullptr
    void f1(std::byte* s);  // s est un pointeur vers un octet (C++17)

##### Remarque

Ne convertissez pas une chaîne de style C en `string` à moins d'en avoir la raison.

##### Remarque

Comme tout autre « pointeur brut », un `zstring` ne doit pas représenter la propriété.

##### Remarque

Il existe des milliards de lignes de C++ « dans la nature », la plupart utilisent `char*` et `const char*` sans documenter l'intention.
Ils sont utilisés de très nombreuses manières, y compris pour représenter la propriété et comme pointeurs génériques vers la mémoire (au lieu de `void*`).
Il est difficile de séparer ces usages, donc cette ligne directrice est difficile à suivre.
C'est l'une des principales sources de bogues dans les programmes C et C++, il est donc utile de suivre cette ligne directrice partout où c'est faisable.

##### Application

* Signaler les utilisations de `[]` sur un `char*`
* Signaler les utilisations de `delete` sur un `char*`
* Signaler les utilisations de `free()` sur un `char*`

### <a name="rstr-charp"></a>SL.str.4 : Utiliser `char*` pour référencer un caractère unique

##### Justification

La variété des usages de `char*` dans le code actuel est une source majeure d'erreurs.

##### Exemple, incorrect

    char arr[] = {'a', 'b', 'c'};

    void print(const char* p)
    {
        cout << p << '\n';
    }

    void use()
    {
        print(arr);   // erreur d'exécution ; potentiellement très grave
    }

Le tableau `arr` n'est pas une chaîne de style C car il n'est pas terminé par zéro.

##### Alternative

Voir [`zstring`](018-stdlib.md#rstr-zstring), [`string`](018-stdlib.md#rstr-string) et [`string_view`](018-stdlib.md#rstr-view).

##### Application

* Signaler les utilisations de `[]` sur un `char*`

### <a name="rstr-byte"></a>SL.str.5 : Utiliser `std::byte` pour référencer des valeurs d'octets qui ne représentent pas nécessairement des caractères

##### Justification

L'utilisation de `char*` pour représenter un pointeur vers quelque chose qui n'est pas nécessairement un caractère cause de la confusion
et désactive des optimisations précieuses.

##### Exemple

    ???

##### Remarque

C++17

##### Application

???


### <a name="rstr-locale"></a>SL.str.10 : Utiliser `std::string` lorsque vous devez effectuer des opérations sur les chaînes sensibles à la localisation

##### Justification

`std::string` prend en charge les [`facilités de localisation`](018-stdlib.md#rstr-locale) de la bibliothèque standard

##### Exemple

    ???

##### Remarque

???

##### Application

???

### <a name="rstr-span"></a>SL.str.11 : Utiliser `gsl::span<char>` plutôt que `std::string_view` lorsque vous devez modifier une chaîne

##### Justification

`std::string_view` est en lecture seule.

##### Exemple

???

##### Remarque

???

##### Application

Le compilateur signalera les tentatives d'écriture dans un `string_view`.

### <a name="rstr-s"></a>SL.str.12 : Utiliser le suffixe `s` pour les littéraux de chaînes destinés à être des `string` de la bibliothèque standard

##### Justification

L'expression directe d'une idée minimise les erreurs.

##### Exemple

    auto pp1 = make_pair("Tokyo", 9.00);         // {chaîne de style C, double} voulu ?
    pair<string, double> pp2 = {"Tokyo", 9.00};  // un peu verbeux
    auto pp3 = make_pair("Tokyo"s, 9.00);        // {std::string, double}    // C++14
    pair pp4 = {"Tokyo"s, 9.00};                 // {std::string, double}    // C++17



##### Application

???


## <a name="ss-io"></a>SL.io : Iostream

Les `iostream` constituent une bibliothèque d'E/S en flux, sûre du point de vue des types, extensible, avec formatage et sans formatage.
Elle prend en charge plusieurs stratégies de tamponnage (et extensibles par l'utilisateur) et plusieurs localisations.
Elle peut être utilisée pour l'E/S conventionnelle, la lecture et l'écriture en mémoire (flux de chaînes),
et des extensions définies par l'utilisateur, telles que le streaming à travers des réseaux (asio : pas encore normalisé).

Résumé des règles sur les iostream :

* [SL.io.1 : N'utiliser l'entrée au niveau des caractères que lorsque c'est nécessaire](018-stdlib.md#rio-low)
* [SL.io.2 : Lors de la lecture, toujours considérer une entrée mal formée](018-stdlib.md#rio-validate)
* [SL.io.3 : Privilégier les iostream pour l'E/S](018-stdlib.md#rio-streams)
* [SL.io.10 : À moins d'utiliser les fonctions de la famille `printf`, appeler `ios_base::sync_with_stdio(false)`](018-stdlib.md#rio-sync)
* [SL.io.50 : Éviter `endl`](018-stdlib.md#rio-endl)
* [???](#???)

### <a name="rio-low"></a>SL.io.1 : N'utiliser l'entrée au niveau des caractères que lorsque c'est nécessaire

##### Justification

À moins que vous ne traitiez réellement des caractères individuels, l'utilisation de l'entrée au niveau des caractères conduit le code utilisateur à effectuer une composition potentiellement source d'erreurs
et potentiellement inefficace de jetons à partir de caractères.

##### Exemple

    char c;
    char buf[128];
    int i = 0;
    while (cin.get(c) && !isspace(c) && i < 128)
        buf[i++] = c;
    if (i == 128) {
        // ... gérer une chaîne trop longue ....
    }

Mieux (beaucoup plus simple et probablement plus rapide) :

    string s;
    s.reserve(128);
    cin >> s;

et le `reserve(128)` est probablement inutile.

##### Application

???


### <a name="rio-validate"></a>SL.io.2 : Lors de la lecture, toujours considérer une entrée mal formée

##### Justification

Les erreurs sont généralement mieux gérées le plus tôt possible.
Si l'entrée n'est pas validée, chaque fonction doit être écrite pour gérer des données invalides (et ce n'est pas pratique).

##### Exemple

    ???

##### Application

???

### <a name="rio-streams"></a>SL.io.3 : Privilégier les `iostream` pour l'E/S

##### Justification

Les `iostream` sont sûrs, flexibles et extensibles.

##### Exemple

    // écrire un nombre complexe :
    complex<double> z{ 3, 4 };
    cout << z << '\n';

`complex` est un type défini par l'utilisateur et son E/S est définie sans modifier la bibliothèque `iostream`.

##### Exemple

    // lire un fichier de nombres complexes :
    for (complex<double> z; cin >> z; )
        v.push_back(z);

##### Exception

??? performances ???

##### Discussion : `iostream` vs. la famille `printf()`

Il est souvent (et souvent à juste titre) souligné que la famille `printf()` a deux avantages par rapport aux `iostream` :
la flexibilité du formatage et les performances.
Cela doit être pesé face aux avantages des `iostream` en termes d'extensibilité pour gérer les types définis par l'utilisateur, de résistance aux violations de sécurité,
de gestion mémoire implicite et de gestion des `locale`.

Si vous avez besoin de performances d'E/S, vous pouvez presque toujours faire mieux que `printf()`.

`gets()`, `scanf()` utilisant `%s`, et `printf()` utilisant `%s` sont des dangers pour la sécurité (vulnérables aux dépassements de tampon et généralement source d'erreurs).
C11 définit certaines « extensions optionnelles » qui effectuent des vérifications supplémentaires de leurs arguments.
Si elles sont présentes dans votre bibliothèque C, `gets_s()`, `scanf_s()` et `printf_s()` peuvent être des alternatives plus sûres, mais elles ne sont toujours pas sûres du point de vue des types.

##### Application

Signaler éventuellement `<cstdio>` et `<stdio.h>`.

### <a name="rio-sync"></a>SL.io.10 : À moins d'utiliser les fonctions de la famille `printf`, appeler `ios_base::sync_with_stdio(false)`

##### Justification

La synchronisation des `iostream` avec l'E/S de style `printf` peut être coûteuse.
`cin` et `cout` sont synchronisés par défaut avec `printf`.

##### Exemple

    int main()
    {
        ios_base::sync_with_stdio(false);
        // ... utiliser les iostream ...
    }

##### Application

???

### <a name="rio-endl"></a>SL.io.50 : Éviter `endl`

##### Justification

Le manipulateur `endl` est essentiellement équivalent à `'\n'` et `"\n"` ;
tel qu'il est le plus souvent utilisé, il ralentit simplement la sortie en effectuant des `flush()` redondants.
Ce ralentissement peut être significatif par rapport à une sortie de style `printf`.

##### Exemple

    cout << "Hello, World!" << endl;    // deux opérations de sortie et un flush
    cout << "Hello, World!\n";          // une opération de sortie et pas de flush

##### Remarque

Pour l'interaction `cin`/`cout` (et équivalents), il n'y a aucune raison de faire un flush ; c'est fait automatiquement.
Pour l'écriture dans un fichier, il y a rarement besoin de faire un `flush`.

##### Remarque

Pour les flux de chaînes (en particulier `ostringstream`), l'insertion d'un `endl` est entièrement équivalente
à l'insertion d'un caractère `'\n'`, mais dans ce cas également, `endl` peut être significativement plus lent.

`endl` ne prend *pas* en charge la production d'une séquence de fin de ligne spécifique à la plateforme (comme `"\r\n"` sous
Windows). Donc pour un flux de chaînes, `s << endl` insère simplement un *seul* caractère, `'\n'`.

##### Remarque

En dehors du problème de performances (parfois important),
le choix entre `'\n'` et `endl` est presque entièrement esthétique.

## <a name="ss-regex"></a>SL.regex : Expressions régulières

`<regex>` est la bibliothèque d'expressions régulières standard de C++.
Elle prend en charge une variété de conventions de motifs d'expressions régulières.
Pour les travaux critiques en termes de performances, envisagez une bibliothèque d'expressions régulières tierce.

## <a name="ss-chrono"></a>SL.chrono : Temps

`<chrono>` (défini dans l'espace de noms `std::chrono`) fournit les notions de `time_point` et `duration` ainsi que des fonctions pour
afficher le temps dans diverses unités.
Il fournit des horloges pour enregistrer des `time_point`.

## <a name="ss-clib"></a>SL.C : La bibliothèque standard C

???

Résumé des règles sur la bibliothèque standard C :

* [SL.C.1 : Ne pas utiliser setjmp/longjmp](018-stdlib.md#rclib-jmp)
* [???](#???)
* [???](#???)

### <a name="rclib-jmp"></a>SL.C.1 : Ne pas utiliser setjmp/longjmp

##### Justification

Un `longjmp` ignore les destructeurs, invalidant ainsi toutes les stratégies de gestion des ressources reposant sur le RAII

##### Application

Signaler toutes les occurrences de `longjmp` et `setjmp`
