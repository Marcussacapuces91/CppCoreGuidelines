# <a name="s-stdlib"></a>SL : La Bibliothèque Standard

En utilisant uniquement le langage de base, chaque tâche est fastidieuse (dans n’importe quel langage). En utilisant une bibliothèque adaptée, chaque tâche peut devenir raisonnablement simple.

La bibliothèque standard a connu une croissance constante au fil des années. Sa description dans le standard est désormais plus grande que celle des caractéristiques du langage. Il est donc probable que cette section des directives sur la bibliothèque finira par atteindre, voire dépasser, la taille des autres sections.

<< Il faut un niveau supplémentaire de numérotation des règles >> 

Résumé des composantes de la bibliothèque standard C++:

* [SL.con: Conteneurs](#ss-con)
* [SL.str: Chaînes](#ss-string)
* [SL.io: Iostream](#ss-io)
* [SL.regex: Expressions régulières](#ss-regex)
* [SL.chrono: Temps](#ss-chrono)
* [SL.C: La bibliothèque C](#ss-clib)

Résumé des règles de la bibliothèque standard:

* [SL.1: Utiliser des bibliothèques partout où c'est possible](#rsl-lib)
* [SL.2: Privilégier la bibliothèque standard par rapport aux autres bibliothèques](#rsl-sl)
* [SL.3: Ne pas ajouter d'entités non standards au namespace `std`](#sl-std)
* [SL.4: Utiliser la bibliothèque standard de manière typée](#sl-safe)
* ???

### <a name="rsl-lib"></a>SL.1 : Utiliser des bibliothèques partout où c'est possible

##### Raison

Gagner du temps. Ne pas réinventer la roue.  
Ne pas reproduire le travail des autres.  
Profiter du travail des autres lorsqu'ils apportent des améliorations.  
Aider les autres lorsque vous apportez des améliorations.

### <a name="rsl-sl"></a>SL.2 : Privilégier la bibliothèque standard plutôt que d'autres bibliothèques

##### Raison

Plus de personnes connaissent la bibliothèque standard.  
Elle est plus susceptible d'être stable, bien maintenue et largement disponible que votre propre code ou la plupart des autres bibliothèques.

### <a name="sl-std"></a>SL.3 : Ne pas ajouter d'entités non standards au namespace `std`

##### Raison

Ajouter à `std` peut changer la signification d'un code qui est autrement conforme au standard.  
Les ajouts à `std` peuvent entrer en conflit avec les futures versions du standard.

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

##### Application

Possible, mais chaotique et susceptible de causer des problèmes sur les plateformes.

### <a name="sl-safe"></a>SL.4 : Utiliser la bibliothèque standard de manière typée

##### Raison

Parce qu'en effet, violer cette règle peut conduire à un comportement indéfini, à des corruptions mémoire et à toutes sortes d'autres erreurs graves.

##### Note

Il s'agit d'une méta-règle semi-philosophique, nécessitant de nombreuses règles concrètes de soutien. Nous l'avons besoin comme un parapluie pour les règles plus spécifiques.

Résumé des règles plus spécifiques:

* [SL.4 : Utiliser la bibliothèque standard de manière typée](#sl-safe)

## <a name="ss-con"></a>SL.con : Conteneurs

???

### <a name="ss-con"></a>SL.con : Conteneurs

Résumé des règles sur les conteneurs:

* [SL.con.1: Préférer l'utilisation de STL `array` ou `vector` devant un tableau C](#rsl-arrays)
* [SL.con.2: Préférer l'utilisation de STL `vector` par défaut sauf si vous avez une raison d'utiliser un autre conteneur](#rsl-vector)
* [SL.con.3: Éviter les erreurs de dépassement de bornes](#rsl-bounds)
* [SL.con.4: ne pas utiliser `memset` ou `memcpy` pour des arguments qui ne sont pas trivially-copyable](#rsl-copy)

### <a name="rsl-arrays"></a>SL.con.1 : Préférer l'utilisation de STL `array` ou `vector` plutôt qu'un tableau C

##### Raison

Les tableaux C sont moins sûrs, et n'ont aucune amélioration par rapport à `array` et `vector`.  
Pour un tableau de longueur fixe, utilisez `std::array`, qui ne se dégrade pas en pointeur lorsqu'il est passé à une fonction et connaît sa taille.  
De plus, comme un tableau natif, un `std::array` alloué sur la pile conserve ses éléments sur la pile.  
Pour un tableau de longueur variable, utilisez `std::vector`, qui peut également changer sa taille et gérer l'allocation mémoire.

##### Exemple

    int v[SIZE];                        // BAD

    std::array<int, SIZE> w;            // ok

##### Exemple

    int* v = new int[initial_size];     // BAD, owning raw pointer
    delete[] v;                         // BAD, manual delete

    std::vector<int> w(initial_size);   // ok

##### Note

Utilisez `gsl::span` pour les références non propriétaires vers un conteneur.

##### Note

Comparer la performance d'un tableau fixe alloué sur la pile à un `vector` avec ses éléments sur le tas est futile.  
Vous pourriez tout aussi bien comparer un `std::array` sur la pile à la résultante d'un `malloc()` accédé via un pointeur.  
Pour la plupart du code, même la différence entre l'allocation pile et l'allocation au tas n'a pas vraiment d'importance, mais la commodité et la sécurité du `vector` le rendent plus judicieux.  
Les personnes travaillant avec du code où cette différence a de l'importance sont tout à fait capables de choisir entre `array` et `vector`.

##### Application

* Marquer la déclaration d'un tableau C dans une fonction ou une classe qui déclare également un conteneur STL (pour éviter des avertissements bruyants excessifs sur le code hérité non-STL).  
Pour corriger : au moins changer le tableau C en `std::array`.

### <a name="rsl-vector"></a>SL.con.2 : Préférer l'utilisation de STL `vector` par défaut sauf si vous avez une raison d'utiliser un autre conteneur

##### Raison

`vector` et `array` sont les seuls conteneurs standards qui offrent les avantages suivants :

* le meilleur accès général (accès aléatoire, y compris la vectorisation) ;
* le meilleur patron d'accès par défaut (de début à fin ou de fin à début est préchargeur-friendly) ;
* la plus faible surcharge d'espace (layout contigu a aucune surcharge par élément, ce qui est bon pour le cache).

Habituellement, vous avez besoin d'ajouter et de supprimer des éléments du conteneur, alors utilisez `vector` par défaut ; si vous n'avez pas besoin de modifier la taille du conteneur, utilisez `array`.

Même si d'autres conteneurs semblent mieux adaptés, comme `map` pour une performance O(log N) ou une `list` pour une insertion efficiente au milieu, un `vector` fonctionnera généralement mieux pour les conteneurs d'une taille de quelques KB.

##### Note

`string` ne doit pas être utilisé comme un conteneur de caractères individuels.  
`string` est une chaîne de texte ; si vous voulez un conteneur de caractères, utilisez `vector</*char_type*/>` ou `array</*char_type*/>` à la place.

##### Exceptions

Si vous avez une bonne raison d'utiliser un autre conteneur, utilisez-le à la place.  
Par exemple :

* Si `vector` convient à vos besoins mais que vous n'avez pas besoin que le conteneur soit de taille variable, utilisez `array` à la place.
* Si vous souhaitez un conteneur de type dictionnaire qui garantit des recherches O(K) ou O(log N), le conteneur sera plus gros (plus de quelques KB) et vous effectuez fréquemment des insertions, de manière à ce que le surcoût de maintien d'un `vector` trié soit irréalisable, alors utilisez un `unordered_map` ou `map` à la place.

##### Note

Pour initialiser un vecteur avec un nombre d'éléments, utilisez l'initialisation `()`.

Pour initialiser un vecteur avec une liste d'éléments, utilisez l'initialisation `{}`.

    vector<int> v1(20);  // v1 a 20 éléments avec la valeur 0 (vector<int>{})
    vector<int> v2 {20}; // v2 a 1 élément avec la valeur 20

[Préférer la syntaxe `{}`-initialiser](#res-list) @TODO-LINK

##### Application

* Marquer un `vector` dont la taille ne change jamais après construction (tels que parce qu'il est `const` ou parce qu'aucune fonction non-`const` n'est appelée sur celui-ci).  
Pour corriger : utilisez un `array` à la place.

### <a name="rsl-bounds"></a>SL.con.3 : Éviter les erreurs de dépassement de bornes

##### Raison

Lire ou écrire au-delà d'une plage d'éléments alloués conduit généralement à des erreurs graves, à de mauvais résultats, à des plantages et à des violations de sécurité.

##### Note

Les fonctions de la bibliothèque standard qui s'appliquent aux intervalles d'éléments possèdent toutes (ou pourraient posséder) des overloads sécurisés par les bornes qui prennent `span`.  
Les types standards tels que `vector` peuvent être modifiés pour exécuter des vérifications de bornes sous le profil de bornes (de façon compatible, par ex. en ajoutant des contrats), ou utilisés avec `at()`.

Idéalement, la garantie `in-bounds` devrait être statiquement imposée.  
Par exemple :

* une boucle `range-for` ne peut pas dépasser la plage du conteneur auquel elle est appliquée
* `v.begin(),v.end()` est facilement déterminé comme sécurisé par les bornes

Ces boucles sont aussi rapides que n'importe quel équivalent non vérifié/non sûr.

Souvent, un simple contrôle prédéfini peut éliminer le besoin de vérifier les indices individuels.  
Par exemple :

* pour `v.begin(),v.begin()+i` l'expression `i` peut être facilement vérifiée par rapport à `v.size()`

De telles boucles peuvent être beaucoup plus rapides que d'accès à chaque élément vérifié individuellement.

##### Exemple, mauvais

    void f()
    {
        array<int, 10> a, b;
        memset(a.data(), 0, 10);         // BAD, and contains a length error (length = 10 * sizeof(int))
        memcmp(a.data(), b.data(), 10);  // BAD, and contains a length error (length = 10 * sizeof(int))
    }

De plus, `std::array<>::fill()` ou `std::fill()` ou même un initialiseur vide sont de meilleurs candidats que `memset()`.

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

Si le code utilise une bibliothèque standard non modifiée, il existe encore des solutions de contournement qui permettent d'utiliser `std::array` et `std::vector` dans une manière sécurisée par les bornes. Le code peut appeler la méthode membre `.at()` sur chaque classe, ce qui lèvera une exception `std::out_of_range`. Alternativement, le code peut appeler la fonction libre `at()`, ce qui imposera une vérification rapide (ou une action personnalisée) sur une violation de bornes.

    void f(std::vector<int>& v, std::array<int, 12> a, int i)
    {
        v[0] = a[0];        // BAD
        v.at(0) = a[0];     // OK (alternative 1)
        at(v, 0) = a[0];    // OK (alternative 2)

        v.at(0) = a[i];     // BAD
        v.at(0) = a.at(i);  // OK (alternative 1)
        v.at(0) = at(a, i); // OK (alternative 2)
    }

##### Application

* Signaler une quelconque appel à une fonction de la bibliothèque standard qui n'est pas vérifiée par les bornes.
??? insert link to a list of banned functions

Cette règle fait partie du [profil de bornes](#ss-bounds) @TODO-LINK

### <a name="rsl-copy"></a>SL.con.4 : ne pas utiliser `memset` ou `memcpy` pour des arguments qui ne sont pas trivially-copyable

##### Raison

Faire cela perturbe la sémantique des objets (par ex. en écrasant un `vptr`).

##### Note

De même pour (w)memset, (w)memcpy, (w)memmove, et (w)memcmp

##### Exemple

    struct base {
        virtual void update() = 0;
    };

    struct derived : public base {
        void update() override {}
    };


    void f(derived& a, derived& b) // goodbye v-tables
    {
        memset(&a, 0, sizeof(derived));
        memcpy(&a, &b, sizeof(derived));
        memcmp(&a, &b, sizeof(derived));
    }

À la place, définissez des fonctions d'initialisation, de copie et de comparaison appropriées

    void g(derived& a, derived& b)
    {
        a = {};    // default initialize
        b = a;     // copy
        if (a == b) do_something(a, b);
    }

##### Application

* Signaler l'utilisation de ces fonctions pour les types qui ne sont pas trivially copyable

**TODO Notes**:

* Impact sur la bibliothèque standard nécessitera une coordination étroite avec WG21, si l'unique but est d'assurer la compatibilité même si jamais standardisée.
* Nous considérons la spécification de surcharge sécurisée par les bornes pour les fonctions de bibliothèque standard (surtout C stdlib) comme `memcmp` et les emballer dans le GSL.
* Pour les fonctions de bibliothèque standard et les types comme `vector` qui ne sont pas entièrement vérifiés, le but est que ces fonctionnalités soient vérifiées lorsque le profil de bornes est activé, et non vérifiées lorsqu'elles sont appelées depuis le code hérité, éventuellement en utilisant ce qui est proposé en même temps par plusieurs membres WG21.

## <a name="ss-string"></a>SL.str : Chaînes

La manipulation du texte est un sujet vaste. `std::string` ne couvre pas tout. Cette section essaie principalement de clarifier la relation de `std::string` avec `char*`, `zstring`, `string_view` et `gsl::span<char>`. La question importante des jeux de caractères non ASCII et des encodages (par ex. `wchar_t`, Unicode et UTF‑8) sera abordée ailleurs.

**Voir aussi** : [Expressions régulières](#ss-regex)

Ici, nous appelons « séquence de caractères » ou « chaîne » pour désigner une séquence de caractères destinées à être lues comme du texte (d'une manière ou d'une autre, éventuellement). Nous ne considérons pas ???

Résumé des chaînes :

* [SL.str.1 : Utiliser `std::string` pour détenir des séquences de caractères](#rstr-string)
* [SL.str.2 : Utiliser `std::string_view` ou `gsl::span<char>` pour référencer des séquences de caractères](#rstr-view)
* [SL.str.3 : Utiliser `zstring` ou `czstring` pour référencer une séquence C‑style nul terminée de caractères](#rstr-zstring)
* [SL.str.4 : Utiliser `char*` pour référencer un caractère unique](#rstr-charp)
* [SL.str.5 : Utiliser `std::byte` pour référencer des valeurs bytes qui ne représentent pas nécessairement des caractères](#rstr-byte)

* [SL.str.10 : Utiliser `std::string` lorsque vous avez besoin d'opérations sensibles à la locale](#rstr-locale)
* [SL.str.11 : Utiliser `gsl::span<char>` plutôt que `std::string_view` lorsque vous avez besoin de muter une chaîne](#rstr-span)
* [SL.str.12 : Utiliser le suffixe `s` pour les littéraux de chaînes destinés à être standard-library `string`s](#rstr-s)

**Voir aussi** :

* [F.24 span](#rf-range) @TODO-LINK
* [F.25 zstring](#rf-zstring) @TODO-LINK

### <a name="rstr-string"></a>SL.str.1 : Utiliser `std::string` pour détenir des séquences de caractères

##### Raison

`string` gère correctement l'allocation, la propriété, la copie, l'expansion graduelle et propose une variété d'opérations utiles.

##### Exemple

    vector<string> read_until(const string& terminator)
    {
        vector<string> res;
        for (string s; cin >> s && s != terminator; ) // read a word
            res.push_back(s);
        return res;
    }

Notez comment `>>` et `!=` sont fournis pour `string` (en tant qu'exemples d'opérations utiles) et qu'il n'y a aucune allocation explicite, désallocation ou vérification de plage (`string` s'en occupe).

En C++17, nous pourrions utiliser `string_view` comme argument, plutôt que `const string&` pour permettre plus de flexibilité aux appelants :

    vector<string> read_until(string_view terminator)   // C++17
    {
        vector<string> res;
        for (string s; cin >> s && s != terminator; ) // read a word
            res.push_back(s);
        return res;
    }

##### Exemple, mauvais

Ne pas utiliser de chaînes C‑style pour les opérations qui nécessitent une gestion mémoire non triviale

    char* cat(const char* s1, const char* s2)   // beware!
        // return s1 + '.' + s2
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

Nous avons‑t‑on le bon ? ... ... ???

##### Note

Ne pas supposer que `string` est plus lent qu'une technique de bas niveau sans mesurer et souvenez‑vous que tout n'est pas du code critique de performance.  
[Ne pas optimiser prématurément](#rper-knuth) @TODO-LINK

##### Application

???

### <a name="rstr-view"></a>SL.str.2 : Utiliser `std::string_view` ou `gsl::span<char>` pour référencer des séquences de caractères

##### Raison

`std::string_view` ou `gsl::span<char>` fournit un accès simple et (potentiellement) sûr aux séquences de caractères indépendamment de la façon dont ces séquences sont allouées et stockées.

##### Exemple

    vector<string> read_until(string_view terminator);

    void user(zstring p, const string& s, string_view ss)
    {
        auto v1 = read_until(p);
        auto v2 = read_until(s);
        auto v3 = read_until(ss);
        // ...
    }

##### Note

`std::string_view` (C++17) est en lecture seule.

##### Application

???

### <a name="rstr-zstring"></a>SL.str.3 : Utiliser `zstring` ou `czstring` pour référencer une séquence C‑style nul terminée de caractères

##### Raison

Lisibilité.  
Déclaration d'intention.  
Une simple `char*` peut être un pointeur vers un caractère unique, un pointeur vers un tableau de caractères, un pointeur vers une chaîne C‑style (nul terminée) ou même vers un petit entier.  
Distinction entre ces alternatives empêche les malentendus et les bugs.

##### Exemple

    void f1(const char* s); // s est probablement une chaîne

Tout ce que nous savons, c'est qu'elle doit être le pointeur nul ou pointer vers au moins un caractère

    void f1(zstring s);     // s est une chaîne C‑style ou le pointeur nul
    void f1(czstring s);    // s est une chaîne C‑style constante ou le pointeur nul
    void f1(std::byte* s);  // s est un pointeur vers un byte (C++17)

##### Note

Ne pas convertir une chaîne C‑style en `string` sauf s'il y a une raison.

##### Note

Comme tout autre "plain pointer", un `zstring` ne doit pas représenter la propriété.

##### Note

Il existe des milliards de lignes de C++ « out there », l'utilisation de `char*` et `const char*` sans documenter l'intention. Ils sont utilisés dans une large gamme de façons. ... (Compléter la traduction).

##### Application

* Marquer les utilisations de `[]` sur un `char*`
* Marquer les utilisations de `delete` sur un `char*`
* Marquer les utilisations de `free()` sur un `char*`

### <a name="rstr-charp"></a>SL.str.4 : Utiliser `char*` pour référencer un caractère unique

##### Raison

La variété d'utilisations de `char*` dans le code actuel est une source majeure d'erreurs.

##### Exemple, mauvais

    char arr[] = {'a', 'b', 'c'};

    void print(const char* p)
    {
        cout << p << '\n';
    }

    void use()
    {
        print(arr);   // run-time error; potentially very bad
    }

Le tableau `arr` n'est pas une chaîne C‑style car il n'est pas nul‑terminé.

##### Alternative

Voir [`zstring`](#rstr-zstring), [`string`](#rstr-string), et [`string_view`](#rstr-view).

##### Application

* Marquer les utilisations de `[]` sur un `char*`

### <a name="rstr-byte"></a>SL.str.5 : Utiliser `std::byte` pour référencer des valeurs bytes qui ne représentent pas nécessairement des caractères

##### Raison

L'utilisation de `char*` pour représenter un pointeur vers quelque chose qui n'est pas nécessairement un caractère provoque une confusion et désactive d'importants optimisations.

##### Exemple

    ???

##### Note

C++17

##### Application

???

### <a name="rstr-locale"></a>SL.str.10 : Utiliser `std::string` lorsque vous avez besoin d'opérations sensibles à la locale

##### Raison

`std::string` supporte les facilities de locale du standard.

##### Exemple

    ???

##### Note

???

##### Application

???

### <a name="rstr-span"></a>SL.str.11 : Utiliser `gsl::span<char>` plutôt que `std::string_view` lorsque vous avez besoin de muter une chaîne

##### Raison

`std::string_view` est en lecture seule.

##### Exemple

???

##### Note

???

##### Application

Le compilateur signalera les tentatives d'écrire dans un `string_view`.

### <a name="rstr-s"></a>SL.str.12 : Utiliser le suffixe `s` pour les littéraux de chaînes destinés à être standard-library `string`s

##### Raison

Déclaration directe de l'idée minimise les erreurs.

##### Exemple

    auto pp1 = make_pair("Tokyo", 9.00);         // {C-style string,double} intended?
    pair<string, double> pp2 = {"Tokyo", 9.00};  // a bit verbose
    auto pp3 = make_pair("Tokyo"s, 9.00);        // {std::string,double}    // C++14
    pair pp4 = {"Tokyo"s, 9.00};                 // {std::string,double}    // C++17

##### Application

???

## <a name="ss-io"></a>SL.io : Iostream

`iostream`s est une bibliothèque d'E/S typée, extensible, formatée et non formatée pour le streaming d'E/S.  
Elle supporte plusieurs stratégies de mise en tampon (et extensibles par l'utilisateur) ainsi que plusieurs locales.  

Elle peut être utilisée pour l'E/S conventionnelle, la lecture et l'écriture en mémoire (flux de chaînes), et pour des extensions définies par l'utilisateur, comme le streaming sur réseau (asio : pas encore standardisé).

Résumé des règles pour iostream :

* [SL.io.1 : Utiliser l'entrée caractère par caractère uniquement si nécessaire](#rio-low)
* [SL.io.2 : Lors de la lecture, toujours prendre en compte l'entrée malformée](#rio-validate)
* [SL.io.3 : Préférer les iostreams pour l'E/S](#rio-streams)
* [SL.io.10 : Sauf si vous utilisez les fonctions de la famille `printf`, appelez `ios_base::sync_with_stdio(false)`](#rio-sync)
* [SL.io.50 : Éviter `endl`](#rio-endl)
* [???] : ???

### <a name="rio-low"></a>SL.io.1 : Utiliser l'entrée caractère par caractère uniquement si nécessaire

##### Raison

Gagner du temps. Ne pas réinventer la roue. Ne pas reproduire le travail des autres.

##### Exemple

    char c;
    char buf[128];
    int i = 0;
    while (cin.get(c) && !isspace(c) && i < 128)
        buf[i++] = c;
    if (i == 128) {
        // ... handle too long string ....
    }

Meilleure (beaucoup plus simple et probablement plus rapide) :

    string s;
    s.reserve(128);
    cin >> s;

et le `reserve(128)` est probablement inutile.

##### Application

????

### <a name="rio-validate"></a>SL.io.2 : Lors de la lecture, toujours prendre en compte l'entrée malformée

##### Raison

Les erreurs sont généralement mieux gérées dès que possible.  
Si l'entrée n'est pas validée, chaque fonction doit être écrite pour gérer les données bad (et ce n'est pas pratique).

##### Exemple

    ???

##### Application

???

### <a name="rio-streams"></a>SL.io.3 : Préférer les iostreams pour l'E/S

##### Raison

Les iostream sont sûrs, flexibles et extensibles.

##### Exemple

    // write a complex number:
    complex<double> z{ 3, 4 };
    cout << z << '\n';

`complex` est un type défini par l'utilisateur et son I/O est défini sans modifier la bibliothèque iostream.

##### Exemple

    // read a file of complex numbers:
    for (complex<double> z; cin >> z; )
        v.push_back(z);

##### Exception

??? performance ???

##### Discussion : iostream vs la famille `printf`

Il est souvent (et souvent correctement) dit que la famille `printf` a deux avantages par rapport aux iostreams :

* flexibilité de formatage et performance.  
Cela doit être pondéré contre les avantages de la famille iostream en matière d'expansion pour l'ajout d'un type utilisateur, de résilience aux violations de sécurité, de gestion implicite de la mémoire et de traitement du locale.

Si vous avez besoin d'un bonio performance, vous pouvez presque toujours faire mieux que `printf`.

`gets()`, `scanf()` avec `%s`, et `printf()` avec `%s` sont des risques de sécurité (vulnérables à un overflow de buffer et généralement mauvais).  
C11 définit des extensions obligatoires qui vérifient leurs arguments. Si présent, `gets_s()`, `scanf_s()`, et `printf_s()` sont plus sûrs, mais ils ne sont pas toujours disponibles.

##### Application

Optionnellement flag `<cstdio>` et `<stdio.h>`.

### <a name="rio-sync"></a>SL.io.10 : Sauf si vous utilisez les fonctions de la famille `printf`, appelez `ios_base::sync_with_stdio(false)`

##### Raison

La synchronisation d'un iostream avec l’I/O style printf peut coûter cher.  
`cin` et `cout` sont par défaut synchronisés avec la fonction printf.

##### Exemple

    int main()
    {
        ios_base::sync_with_stdio(false);
        // ... use iostreams ...
    }

##### Application

???

### <a name="rio-endl"></a>SL.io.50 : Éviter `endl`

##### Raison

Le manipueur `endl` est en grande partie équivalent à `'\n'` et `"\n"` ; comme la façon la plus courante, il ralentit la sortie simplement par le flush supplémentaire.

Cette réduction peut être importante par rapport à l’output de style `printf`.

##### Exemple

    cout << "Hello, World!" << endl;    // deux opérations de sortie et un flush
    cout << "Hello, World!\n";          // un seul pas de ^

##### Note

Pour ce qui est de l’interaction  `cin` / `cout` (et équivalents) il n'y a pas de raison de forcer un flush ; c’est fait automatiquement.  
Pour écrire dans un fichier, il n'y a rarement besoin de `flush`.

##### Note

Pour les flux de chaînes (`ostringstream` par exemple), l'insertion d'un `endl` est totalement équivalente à l'insertion d'un `'\n'` caractère, mais aussi dans ce cas, `endl` peut être significativement plus lent.

`endl` ne prend pas en charge la production d’une fin de ligne spécifique au système d'exploitation (comme `"\r\n"` sous Windows).  
Donc pour un flux de chaînes, `s << endl` insère simplement un *seul* caractère, `'\n'`.

##### Note

Outre l'aspect (souvent important) de la performance, le choix entre `'\n'` et `endl` est presque entièrement esthétique.

## <a name="ss-regex"></a>SL.regex : Expressions régulières

`<regex>` est la bibliothèque d'expressions régulières du standard C++.  
Elle prend en charge une variété de conventions de modèles d'expressions régulières.  
Pour les travaux à haute performance, envisager une bibliothèque d'expressions régulières tierce.

## <a name="ss-chrono"></a>SL.chrono : Temps

`<chrono>` (défini dans le namespace `std::chrono`) fournit les notions de time_point et duration ainsi que les fonctions pour afficher le temps dans différentes unités.  
Il fournit des horloges pour enregistrer des time_point.

## <a name="ss-clib"></a>SL.C : La Bibliothèque C

???

Résumé des règles de la bibliothèque C :

* [SL.C.1 : Ne pas utiliser setjmp/longjmp](#rclib-jmp)
* [???](#???)
* [???](#???)

### <a name="rclib-jmp"></a>SL.C.1 : Ne pas utiliser setjmp/longjmp

##### Raison

Un `longjmp` ignore les destructeurs, invalidant ainsi toutes les stratégies de gestion de ressources reposant sur RAII.

##### Application

Marquer toutes les occurrences de `longjmp` et `setjmp`.