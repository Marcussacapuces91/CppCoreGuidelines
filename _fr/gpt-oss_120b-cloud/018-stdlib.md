# <a name="s-stdlib"></a>SL : Bibliothèque standard

En n'utilisant que le langage pur, chaque tâche est fastidieuse (dans n'importe quel langage). En utilisant une bibliothèque adaptée, toute tâche peut être raisonnablement simple.

La bibliothèque standard s'est développée régulièrement au fil des ans. Sa description dans la norme est maintenant plus volumineuse que celle des fonctionnalités du langage. Ainsi, il est probable que cette section sur la bibliothèque des lignes directrices finisse par croître en taille pour égaler ou dépasser le reste.

<< ??? Nous avons besoin d'un autre niveau de numérotation des règles ??? >>

Résumé des composants de la bibliothèque standard C++ :

* [SL.con : Conteneurs](018-stdlib.md#ss-con)
* [SL.str : Chaîne](018-stdlib.md#ss-string)
* [SL.io : Flux d’E/S](018-stdlib.md#ss-io)
* [SL.regex : Expressions régulières](018-stdlib.md#ss-regex)
* [SL.chrono : Temps](018-stdlib.md#ss-chrono)
* [SL.C : Bibliothèque C standard](018-stdlib.md#ss-clib)

Résumé des règles de la bibliothèque standard :

* [SL.1 : Utilisez les bibliothèques chaque fois que possible](018-stdlib.md#rsl-lib)
* [SL.2 : Privilégiez la bibliothèque standard plutôt que d'autres bibliothèques](018-stdlib.md#rsl-sl)
* [SL.3 : N'ajoutez pas d'entités non standard dans l'espace de noms `std`](018-stdlib.md#sl-std)
* [SL.4 : Utilisez la bibliothèque standard de façon sûre du point de vue des types](018-stdlib.md#sl-safe)
* ???

### <a name="rsl-lib"></a>SL.1 : Utiliser les bibliothèques chaque fois que possible

##### Raison

Gagner du temps. Ne pas réinventer la roue.  
Ne pas reproduire le travail des autres.  
Profiter des améliorations apportées par les autres.  
Aider les autres lorsque vous apportez des améliorations.

### <a name="rsl-sl"></a>SL.2 : Privilégier la bibliothèque standard plutôt que d'autres bibliothèques

##### Raison

Plus de personnes connaissent la bibliothèque standard.  
Il est plus probable qu'elle soit stable, bien maintenue et largement disponible que votre propre code ou la plupart des autres bibliothèques.

### <a name="sl-std"></a>SL.3 : N'ajoutez pas d'entités non standard dans l'espace de noms `std`

##### Raison

Ajouter à `std` pourrait changer le sens d'un code autrement conforme aux standards.  
Les ajouts à `std` pourraient entrer en conflit avec les futures versions du standard.

##### Exemple

    namespace std { // MAUVAIS : viole le standard

        class My_vector {
            //     . . .
        };

    }

    namespace Foo { // BON : l'espace de noms utilisateur est autorisé

        class My_vector {
            //     . . .
        };

    }

##### Application

Possible, mais désordonné et susceptible de poser des problèmes de portabilité.

### <a name="sl-safe"></a>SL.4 : Utilisez la bibliothèque standard de façon sûre du point de vue des types

##### Raison

Parce que, évidemment, enfreindre cette règle peut conduire à un comportement indéfini, à des corruptions de mémoire et à toutes sortes d'autres erreurs graves.

##### Note

Il s'agit d'une méta‑règle semi‑philosophique, qui nécessite de nombreuses règles concrètes de soutien.  
Nous l'utilisons comme parapluie pour les règles plus spécifiques.

Résumé des règles plus spécifiques :

* [SL.4 : Utilisez la bibliothèque standard de façon sûre du point de vue des types](018-stdlib.md#sl-safe)


## <a name="ss-con"></a>SL.con : Conteneurs

???

Résumé des règles de conteneurs :

* [SL.con.1 : Préférez `array` ou `vector` de la STL plutôt qu'un tableau C](018-stdlib.md#rsl-arrays)
* [SL.con.2 : Préférez `vector` de la STL par défaut sauf si vous avez une raison d'utiliser un autre conteneur](018-stdlib.md#rsl-vector)
* [SL.con.3 : Évitez les erreurs de débordement](018-stdlib.md#rsl-bounds)
* [SL.con.4 : N'utilisez pas `memset` ou `memcpy` pour des arguments qui ne sont pas trivially‑copyable](018-stdlib.md#rsl-copy)

### <a name="rsl-arrays"></a>SL.con.1 : Préférez l’utilisation de `array` ou `vector` de la STL plutôt qu’un tableau C

##### Raison

Les tableaux C sont moins sûrs et n'offrent aucun avantage par rapport à `array` et `vector`.  
Pour un tableau de longueur fixe, utilisez `std::array`, qui ne dégénère pas en pointeur lorsqu'il est passé à une fonction et connaît sa taille.  
De plus, comme un tableau intégré, un `std::array` alloué sur la pile garde ses éléments sur la pile.  
Pour un tableau de longueur variable, utilisez `std::vector`, qui peut changer de taille et gère l’allocation de mémoire.

##### Exemple

    int v[SIZE];                        // MAUVAIS

    std::array<int, SIZE> w;            // ok

##### Exemple

    int* v = new int[initial_size];     // MAUVAIS, pointeur brut propriétaire
    delete[] v;                         // MAUVAIS, suppression manuelle

    std::vector<int> w(initial_size);   // ok

##### Note

Utilisez `gsl::span` pour les références non‑possédées dans un conteneur.

##### Note

Comparer les performances d’un tableau de taille fixe alloué sur la pile avec un `vector` dont les éléments sont sur le tas est fallacieux.  
On pourrait tout aussi bien comparer un `std::array` sur la pile avec le résultat d’un `malloc()` accédé via un pointeur.  
Pour la plupart du code, même la différence entre allocation sur la pile et sur le tas n’a pas d’importance, mais la commodité et la sûreté du `vector` le rendent préférable.  
Les programmeurs qui travaillent sur du code où cette différence compte sont tout à fait capables de choisir entre `array` et `vector`.

##### Application

* Signaler la déclaration d’un tableau C à l’intérieur d’une fonction ou d’une classe qui déclare également un conteneur STL (pour éviter des avertissements excessifs sur du code hérité non‑STL). Pour corriger : au moins remplacer le tableau C par un `std::array`.

### <a name="rsl-vector"></a>SL.con.2 : Préférez l’utilisation de `vector` de la STL par défaut sauf si vous avez une raison d’utiliser un autre conteneur

##### Raison

`vector` et `array` sont les seuls conteneurs standard offrant les avantages suivants :

* l’accès général le plus rapide (accès aléatoire, y compris vecteur‑friendly) ;
* le modèle d’accès par défaut le plus rapide (début‑à‑fin ou fin‑à‑début, favorable au préfetch) ;
* le plus faible overhead mémoire (mise en page contiguë, zéro surcharge par élément, ce qui est cache‑friendly).

En général, on a besoin d’ajouter et de retirer des éléments du conteneur ; utilisez donc `vector` par défaut ; si vous n’avez pas besoin de modifier la taille du conteneur, utilisez `array`.

Même lorsque d’autres conteneurs semblent plus appropriés, comme `map` pour des recherches en O(log N) ou `list` pour des insertions efficaces au milieu, un `vector` sera généralement plus performant pour des conteneurs jusqu’à quelques kilo‑octets.

##### Note

`string` ne doit pas être utilisé comme conteneur de caractères individuels. Une `string` est une chaîne de texte ; si vous voulez un conteneur de caractères, utilisez `vector</*char_type*/>` ou `array</*char_type*/>`.

##### Exceptions

Si vous avez une bonne raison d’utiliser un autre conteneur, utilisez‑le à la place. Par exemple :

* Si `vector` convient mais que vous n’avez pas besoin que le conteneur soit de taille variable, utilisez `array` à la place.
* Si vous avez besoin d’un conteneur de type dictionnaire garantissant des recherches en O(K) ou O(log N), dont la taille dépasse quelques kilo‑octets et que vous effectuez des insertions fréquentes rendant le maintien d’un `vector` trié impossible, utilisez alors `unordered_map` ou `map`.

##### Note

Pour initialiser un `vector` avec un certain nombre d’éléments, utilisez l’initialisation avec parenthèses.  
Pour initialiser un `vector` avec une liste d’éléments, utilisez l’initialisation avec accolades.

    vector<int> v1(20);  // v1 possède 20 éléments initialisés à 0 (vector<int>{})
    vector<int> v2 {20}; // v2 possède 1 élément de valeur 20

[Préférez la syntaxe d’initialisation `{}`](010-expr.md#res-list).

##### Application

* Signaler un `vector` dont la taille ne change jamais après construction (parce qu’il est `const` ou parce qu’aucune fonction non‑`const` n’est appelée). Pour corriger : utilisez un `array`.

### <a name="rsl-bounds"></a>SL.con.3 : Évitez les erreurs de débordement

##### Raison

Lire ou écrire au‑delà d’une plage d’éléments allouée conduit généralement à des erreurs graves, à des résultats incorrects, à des plantages et à des violations de sécurité.

##### Note

Les fonctions de la bibliothèque standard qui opèrent sur des plages d’éléments possèdent (ou pourraient posséder) des surcharges sûres qui acceptent `span`.  
Les types standards tels que `vector` peuvent être modifiés pour effectuer des vérifications de limites sous le profil « bounds » (par exemple via des contrats), ou être utilisés avec `at()`.

Idéalement, la garantie d’être dans les limites devrait être imposée statiquement.  
Par exemple :

* une boucle « range‑for » ne peut pas itérer au‑delà de la plage du conteneur auquel elle s’applique ;
* `v.begin(), v.end()` est facilement déterminé comme sûr vis‑à‑vis des limites.

Ces boucles sont aussi rapides que leurs équivalents non vérifiés.

Souvent, une simple pré‑vérification peut éliminer le besoin de vérifier chaque indice individuellement.  
Par exemple, pour `v.begin(), v.begin()+i`, le `i` peut être comparé à `v.size()`.

Ces boucles peuvent être bien plus rapides que des accès individuels vérifiés.

##### Exemple, mauvais

    void f()
    {
        array<int, 10> a, b;
        memset(a.data(), 0, 10);         // MAUVAIS, et comporte une erreur de longueur (longueur = 10 * sizeof(int))
        memcmp(a.data(), b.data(), 10);  // MAUVAIS, et comporte une erreur de longueur (longueur = 10 * sizeof(int))
    }

Il vaut mieux utiliser `std::array<>::fill()`, `std::fill()` ou même un initialiseur vide plutôt que `memset()`.

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

Si le code utilise la bibliothèque standard non modifiée, il existe des solutions de contournement permettant d’utiliser `std::array` et `std::vector` de manière sûre vis‑à‑vis des limites. Le code peut appeler la fonction membre `.at()` sur chaque classe, ce qui déclenchera une exception `std::out_of_range`. Alternativement, le code peut appeler la fonction libre `at()`, qui provoquera un échec immédiat (ou une action personnalisée) en cas de violation de limites.

    void f(std::vector<int>& v, std::array<int, 12> a, int i)
    {
        v[0] = a[0];        // MAUVAIS
        v.at(0) = a[0];     // OK (alternative 1)
        at(v, 0) = a[0];    // OK (alternative 2)

        v.at(0) = a[i];     // MAUVAIS
        v.at(0) = a.at(i);  // OK (alternative 1)
        v.at(0) = at(a, i); // OK (alternative 2)
    }

##### Application

* Émettre un diagnostic pour tout appel à une fonction de la bibliothèque standard qui n’est pas vérifiée par limites.
@TODO-LINK
Cette règle fait partie du [profil de limites](022-profile.md#ss-bounds). @TODO-LINK

### <a name="rsl-copy"></a>SL.con.4 : N’utilisez pas `memset` ou `memcpy` pour des arguments qui ne sont pas trivially‑copyable

##### Raison

Faire cela corrompt la sémantique des objets (par exemple en écrasant un `vptr`).

##### Note

De même pour (w)memset, (w)memcpy, (w)memmove, et (w)memcmp.

##### Exemple

    struct base {
        virtual void update() = 0;
    };

    struct derived : public base {
        void update() override {}
    };


    void f(derived& a, derived& b) // adieu v‑tables
    {
        memset(&a, 0, sizeof(derived));
        memcpy(&a, &b, sizeof(derived));
        memcmp(&a, &b, sizeof(derived));
    }

À la place, définissez des fonctions d’initialisation, de copie et de comparaison appropriées :

    void g(derived& a, derived& b)
    {
        a = {};    // initialisation par défaut
        b = a;     // copie
        if (a == b) do_something(a, b);
    }

##### Application

* Signaler l’utilisation de ces fonctions pour des types qui ne sont pas trivially copyable.

**Notes TODO** :

* L’impact sur la bibliothèque standard nécessitera une coordination étroite avec le WG21, ne serait‑ce que pour garantir la compatibilité même si la règle n’est jamais standardisée.
* Nous envisageons de spécifier des surcharges sûres pour les fonctions stdlib (en particulier la libc C) comme `memcmp` et de les livrer dans le GSL.
* Pour les fonctions et types stdlib existants comme `vector` qui ne sont pas entièrement vérifiés, l’objectif est que ces fonctionnalités soient vérifiées lorsqu’elles sont appelées depuis du code avec le profil de limites activé, et non vérifiées lorsqu’elles sont appelées depuis du code hérité, éventuellement à l’aide de contrats (actuellement proposés par plusieurs membres du WG21).

## <a name="ss-string"></a>SL.str : Chaîne

La manipulation de texte est un sujet vaste.  
`std::string` ne couvre pas tout.  
Cette section tente principalement de clarifier la relation entre `std::string` et `char*`, `zstring`, `string_view` et `gsl::span<char>`.  
La question importante des jeux de caractères non ASCII et des encodages (par exemple `wchar_t`, Unicode et UTF‑8) sera traitée ailleurs.

**Voir aussi** : [expressions régulières](018-stdlib.md#ss-regex)

Dans ce texte, nous utilisons « séquence de caractères » ou « chaîne » pour désigner une séquence de caractères destinée à être lue comme texte (d’une façon ou d’une autre, finalement).  
Nous ne considérons pas ???

Résumé des règles concernant les chaînes :

* [SL.str.1 : Utilisez `std::string` pour posséder des séquences de caractères](018-stdlib.md#rstr-string)
* [SL.str.2 : Utilisez `std::string_view` ou `gsl::span<char>` pour faire référence à des séquences de caractères](018-stdlib.md#rstr-view)
* [SL.str.3 : Utilisez `zstring` ou `czstring` pour faire référence à une séquence de caractères C‑style terminée par zéro](018-stdlib.md#rstr-zstring)
* [SL.str.4 : Utilisez `char*` pour faire référence à un caractère unique](018-stdlib.md#rstr-charp)
* [SL.str.5 : Utilisez `std::byte` pour faire référence à des valeurs d’octet qui ne représentent pas nécessairement des caractères](018-stdlib.md#rstr-byte)

* [SL.str.10 : Utilisez `std::string` lorsque vous devez effectuer des opérations sensibles à la locale](018-stdlib.md#rstr-locale)
* [SL.str.11 : Utilisez `gsl::span<char>` plutôt que `std::string_view` lorsque vous devez muter une chaîne](018-stdlib.md#rstr-span)
* [SL.str.12 : Utilisez le suffixe `s` pour les littéraux de chaîne destinés à être des `std::string` de la bibliothèque standard](018-stdlib.md#rstr-s)

**Voir aussi** :

* [F.24 span](006-functions.md#rf-range)
* [F.25 zstring](006-functions.md#rf-zstring)


### <a name="rstr-string"></a>SL.str.1 : Utilisez `std::string` pour posséder des séquences de caractères

##### Raison

`string` gère correctement l’allocation, la possession, la copie, l’expansion progressive et propose une variété d’opérations utiles.

##### Exemple

    vector<string> read_until(const string& terminator)
    {
        vector<string> res;
        for (string s; cin >> s && s != terminator; ) // lire un mot
            res.push_back(s);
        return res;
    }

Remarquez que les opérateurs `>>` et `!=` sont fournis pour `string` (exemples d’opérations utiles) et qu’il n’y a aucune allocation, désallocation ou vérification de borne explicite (`string` s’en charge).

En C++17, nous pourrions utiliser `string_view` comme argument, plutôt que `const string&`, afin d’offrir plus de souplesse aux appelants :

    vector<string> read_until(string_view terminator)   // C++17
    {
        vector<string> res;
        for (string s; cin >> s && s != terminator; ) // lire un mot
            res.push_back(s);
        return res;
    }

##### Exemple, mauvais

Ne pas utiliser les chaînes de style C pour des opérations qui nécessitent une gestion mémoire non triviale :

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

Avons‑nous bien compris ?  
L’appelant se souviendra‑t‑il d’appeler `free()` sur le pointeur retourné ?  
Ce code passera‑t‑il un audit de sécurité ?

##### Note

Ne supposez pas que `string` est plus lent que des techniques de bas niveau sans mesure, et rappelez‑vous que tout le code n’est pas critique en termes de performance.  
[Ne pas optimiser prématurément](011-performance.md#rper-knuth)

##### Application

???

### <a name="rstr-view"></a>SL.str.2 : Utilisez `std::string_view` ou `gsl::span<char>` pour faire référence à des séquences de caractères

##### Raison

`std::string_view` ou `gsl::span<char>` offrent un accès simple et (potentiellement) sûr aux séquences de caractères, indépendamment de la façon dont ces séquences sont allouées et stockées.

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

`std::string_view` (C++17) est en lecture‑seule.

##### Application

???

### <a name="rstr-zstring"></a>SL.str.3 : Utilisez `zstring` ou `czstring` pour faire référence à une séquence de caractères C‑style terminée par zéro

##### Raison

Lisibilité.  
Déclaration d’intention.  
Un simple `char*` peut être un pointeur vers un caractère unique, un pointeur vers un tableau de caractères, une chaîne C‑style (terminée par zéro) ou même un petit entier.  
Faire la distinction prévient les malentendus et les bugs.

##### Exemple

    void f1(const char* s); // s est probablement une chaîne

Tous nous savons que `s` doit être `nullptr` ou pointer sur au moins un caractère

    void f1(zstring s);     // s est une chaîne C‑style ou nullptr
    void f1(czstring s);    // s est une constante de chaîne C‑style ou nullptr
    void f1(std::byte* s);  // s est un pointeur vers un octet (C++17)

##### Note

Ne convertissez pas une chaîne C‑style en `string` sans raison valable.

##### Note

Comme tout autre « pointeur brut », un `zstring` ne doit pas représenter la possession.

##### Note

Il existe des milliards de lignes de code C++ « dans le monde », la plupart utilisent `char*` et `const char*` sans documenter l’intention.  
Ils sont employés de multiples façons, notamment pour représenter la possession et comme pointeurs génériques vers la mémoire (au lieu de `void*`).  
Il est difficile de séparer ces usages, d’où la difficulté à appliquer cette ligne directrice.  
C’est l’une des principales sources de bugs dans les programmes C et C++, il vaut donc la peine d’appliquer cette règle chaque fois que cela est possible.

##### Application

* Signaler l’utilisation de `[]` sur un `char*`
* Signaler l’utilisation de `delete` sur un `char*`
* Signaler l’utilisation de `free()` sur un `char*`

### <a name="rstr-charp"></a>SL.str.4 : Utilisez `char*` pour faire référence à un caractère unique

##### Raison

La variété d’utilisations de `char*` dans le code actuel est une source majeure d’erreurs.

##### Exemple, mauvais

    char arr[] = {'a', 'b', 'c'};

    void print(const char* p)
    {
        cout << p << '\n';
    }

    void use()
    {
        print(arr);   // erreur d’exécution ; potentiellement très grave
    }

Le tableau `arr` n’est pas une chaîne C‑style car il n’est pas terminée par zéro.

##### Alternative

Voir [`zstring`](018-stdlib.md#rstr-zstring), [`string`](018-stdlib.md#rstr-string) et [`string_view`](018-stdlib.md#rstr-view).

##### Application

* Signaler l’utilisation de `[]` sur un `char*`

### <a name="rstr-byte"></a>SL.str.5 : Utilisez `std::byte` pour faire référence à des valeurs d’octet qui ne représentent pas nécessairement des caractères

##### Raison

L’usage de `char*` pour représenter un pointeur vers quelque chose qui n’est pas forcément un caractère crée de la confusion et empêche des optimisations précieuses.

##### Exemple

    ???

##### Note

C++17

##### Application

??

### <a name="rstr-locale"></a>SL.str.10 : Utilisez `std::string` lorsque vous devez effectuer des opérations sensibles à la locale

##### Raison

`std::string` supporte les facilities de la bibliothèque standard [`locale`](018-stdlib.md#rstr-locale)

##### Exemple

    ???

##### Note

???

##### Application

???

### <a name="rstr-span"></a>SL.str.11 : Utilisez `gsl::span<char>` plutôt que `std::string_view` lorsque vous devez muter une chaîne

##### Raison

`std::string_view` est en lecture‑seule.

##### Exemple

???

##### Note

???

##### Application

Le compilateur signalera les tentatives d’écriture sur un `string_view`.

### <a name="rstr-s"></a>SL.str.12 : Utilisez le suffixe `s` pour les littéraux de chaîne destinés à être des `std::string` de la bibliothèque standard

##### Raison

L’expression directe d’une idée minimise les erreurs.

##### Exemple

    auto pp1 = make_pair("Tokyo", 9.00);         // {C‑style string,double} souhaité ?
    pair<string, double> pp2 = {"Tokyo", 9.00};  // un peu verbeux
    auto pp3 = make_pair("Tokyo"s, 9.00);        // {std::string,double}    // C++14
    pair pp4 = {"Tokyo"s, 9.00};                 // {std::string,double}    // C++17



##### Application

??

## <a name="ss-io"></a>SL.io : Flux d’E/S

`iostream`s est une bibliothèque typée, extensible, formatée et non formatée d’E/S en flux.  
Elle supporte plusieurs stratégies de mise en mémoire tampon (et extensibles par l’utilisateur) et plusieurs locales.  
Elle peut être utilisée pour les I/O conventionnels, la lecture et l’écriture en mémoire (flux de chaînes), et des extensions définies par l’utilisateur, comme le streaming à travers les réseaux (asio : pas encore standardisé).

Résumé des règles d’E/S  :

* [SL.io.1 : Utilisez l’entrée de niveau caractère uniquement lorsque cela est nécessaire](018-stdlib.md#rio-low)
* [SL.io.2 : Lors de la lecture, considérez toujours les entrées mal formées](018-stdlib.md#rio-validate)
* [SL.io.3 : Privilégiez les iostreams pour l’I/O](018-stdlib.md#rio-streams)
* [SL.io.10 : Sauf si vous utilisez les fonctions de la famille `printf`, appelez `ios_base::sync_with_stdio(false)`](018-stdlib.md#rio-sync)
* [SL.io.50 : Évitez `endl`](018-stdlib.md#rio-endl)
* [???](#???)

### <a name="rio-low"></a>SL.io.1 : Utilisez l’entrée de niveau caractère uniquement lorsque vous devez le faire

##### Raison

À moins d’avoir réellement besoin de manipuler des caractères individuels, l’entrée de niveau caractère conduit le code utilisateur à composer des tokens à partir de caractères, ce qui est potentiellement source d’erreurs et d’inefficacité.

##### Exemple

    char c;
    char buf[128];
    int i = 0;
    while (cin.get(c) && !isspace(c) && i < 128)
        buf[i++] = c;
    if (i == 128) {
        // ... gérer une chaîne trop longue ...
    }

Mieux (beaucoup plus simple et probablement plus rapide) :

    string s;
    s.reserve(128);
    cin >> s;

et le `reserve(128)` n’est probablement pas indispensable.

##### Application

??

### <a name="rio-validate"></a>SL.io.2 : Lors de la lecture, considérez toujours les entrées mal formées

##### Raison

Les erreurs sont généralement mieux traitées le plus tôt possible.  
Si l’entrée n’est pas validée, chaque fonction doit être écrite pour gérer des données erronées (et cela n’est pas pratique).

##### Exemple

    ???

##### Application

???

### <a name="rio-streams"></a>SL.io.3 : Privilégiez les iostreams pour l’I/O

##### Raison

Les iostreams sont sûrs, flexibles et extensibles.

##### Exemple

    // écrire un nombre complexe :
    complex<double> z{ 3, 4 };
    cout << z << '\n';

`complex` est un type défini par l'utilisateur et son I/O est défini sans modifier la bibliothèque iostream.

##### Exemple

    // lire un fichier de nombres complexes :
    for (complex<double> z; cin >> z; )
        v.push_back(z);

##### Exception

??? performances ???

##### Discussion : iostreams vs. famille `printf()`

Il est souvent (et à juste titre) souligné que la famille `printf()` possède deux avantages comparés aux iostreams : flexibilité de formatage et performances.  
Il faut les mettre en balance avec les avantages des iostreams, à savoir l’extensibilité pour gérer des types définis par l'utilisateur, la résilience aux failles de sécurité, la gestion implicite de la mémoire et le support des locales.

Si vous avez besoin de performances d’I/O, vous pouvez presque toujours faire mieux que `printf()`.

`gets()`, `scanf()` avec `%s` et `printf()` avec `%s` sont des risques de sécurité (vulnérables aux dépassements de tampon et généralement source d’erreurs).  
C11 définit des « extensions optionnelles » qui ajoutent des vérifications supplémentaires à leurs arguments.  
Si votre bibliothèque C les propose, `gets_s()`, `scanf_s()` et `printf_s()` peuvent être des alternatives plus sûres, mais elles ne sont toujours pas typées.

##### Application

Optionnellement signaler les inclusions de `<cstdio>` et `<stdio.h>`.

### <a name="rio-sync"></a>SL.io.10 : Sauf si vous utilisez les fonctions de la famille `printf`, appelez `ios_base::sync_with_stdio(false)`

##### Raison

Synchroniser les iostreams avec les I/O de style `printf` peut être coûteux.  
`cin` et `cout` sont, par défaut, synchronisés avec `printf`.

##### Exemple

    int main()
    {
        ios_base::sync_with_stdio(false);
        // ... utilisez les iostreams ...
    }

##### Application

??

### <a name="rio-endl"></a>SL.io.50 : Évitez `endl`

##### Raison

Le manipulateur `endl` est essentiellement équivalent à `'\n'` et `"\n"` ; dans la plupart des cas il ralentit la sortie en effectuant un `flush()` redondant. Ce ralentissement peut être significatif comparé à la sortie de style `printf`.

##### Exemple

    cout << "Hello, World!" << endl;    // deux opérations d’écriture et un flush
    cout << "Hello, World!\n";          // une opération d’écriture et aucun flush

##### Note

Pour l’interaction `cin`/`cout` (et équivalents), il n’y a aucune raison de flusher ; cela est fait automatiquement.  
Pour l’écriture dans un fichier, il est rarement nécessaire de `flush`.

##### Note

Pour les flux de chaînes (`ostringstream`), l’insertion de `endl` est entièrement équivalente à l’insertion d’un caractère `'\n'`, mais dans ce cas `endl` peut être sensiblement plus lent.

`endl` ne prend pas en charge la production d’une séquence de fin de ligne spécifique à la plateforme (par exemple `"\r\n"` sous Windows). Ainsi, pour un flux de chaîne, `s << endl` insère simplement un *unique* caractère, `'\n'`.

##### Note

Outre la (occasionnellement importante) question de performance, le choix entre `'\n'` et `endl` est presque entièrement esthétique.

## <a name="ss-regex"></a>SL.regex : Regex

`<regex>` est la bibliothèque standard C++ d’expressions régulières.  
Elle supporte une variété de conventions de motifs d’expression régulière.  
Pour les travaux sensibles aux performances, envisagez d’utiliser une bibliothèque tierce d’expression régulière.

## <a name="ss-chrono"></a>SL.chrono : Temps

`<chrono>` (défini dans l’espace de noms `std::chrono`) fournit les notions de `time_point` et `duration` ainsi que des fonctions pour afficher le temps dans diverses unités.  
Il fournit des horloges pour enregistrer des `time_point`.

## <a name="ss-clib"></a>SL.C : Bibliothèque C standard

???

Résumé des règles de la bibliothèque C  :

* [SL.C.1 : N’utilisez pas `setjmp`/`longjmp`](018-stdlib.md#rclib-jmp)
* [???](#???)
* [???](#???)

### <a name="rclib-jmp"></a>SL.C.1 : N’utilisez pas `setjmp`/`longjmp`

##### Raison

`longjmp` ignore les destructeurs, invalidant ainsi toutes les stratégies de gestion de ressources basées sur RAII.

##### Application

Signaler toutes les occurrences de `longjmp` et `setjmp`.