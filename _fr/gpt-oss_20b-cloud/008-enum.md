# <a name="s-enum"></a>Enum: Énumérations

Les énumérations servent à définir des ensembles de valeurs entières et à créer des types pour de tels ensembles. Il existe deux types d'énumérations, les `enum` classiques et les `enum class`.

Résumé des règles d'énumération :

* [Enum.1: Préférer les énumérations aux macros](008-enum.md#renum-macro)
* [Enum.2: Utiliser les énumérations pour représenter des ensembles de constantes nommées liées](008-enum.md#renum-set)
* [Enum.3: Préférer les `enum class` aux `enum`s classiques](008-enum.md#renum-class)
* [Enum.4: Définir des opérations sur les énumérations pour une utilisation sûre et simple](008-enum.md#renum-oper)
* [Enum.5: Ne pas utiliser `ALL_CAPS` pour les énumérateurs](008-enum.md#renum-caps)
* [Enum.6: Éviter les énumérations non nommées](008-enum.md#renum-unnamed)
* [Enum.7: Spécifier le type sous‑jacent d'une énumération uniquement lorsque c'est nécessaire](008-enum.md#renum-underlying)
* [Enum.8: Spécifier les valeurs des énumérateurs uniquement lorsque nécessaire](008-enum.md#renum-value)

### <a name="renum-macro"></a>Enum.1: Préférer les énumérations aux macros

##### Raison

Les macros n'obéissent pas aux règles de portée et de type. De plus, les noms de macro sont supprimés lors du prétraitement et ne figurent donc généralement pas dans les outils comme les débogueurs.

##### Exemple

Tout d'abord, un mauvais ancien code :

    // webcolors.h (en-tête tiers)
    #define RED   0xFF0000
    #define GREEN 0x00FF00
    #define BLUE  0x0000FF

    // productinfo.h
    // Les lignes suivantes définissent les sous‑types de produit basés sur la couleur
    #define RED    0
    #define PURPLE 1
    #define BLUE   2

    int webby = BLUE;   // webby == 2; probablement pas ce qui était voulu

Au lieu d'utiliser une `enum` :

    enum class Web_color { red = 0xFF0000, green = 0x00FF00, blue = 0x0000FF };
    enum class Product_info { red = 0, purple = 1, blue = 2 };

    int webby = blue;   // erreur : être précis
    Web_color webby = Web_color::blue;

Nous avons utilisé un `enum class` pour éviter les conflits de noms.

##### Note

Considérez également les variables `constexpr` et `const inline`.

##### Application

Détectez les macros qui définissent des valeurs entières. Utilisez un `enum`, une variable `const inline` ou une autre alternative non‑macro à la place.

### <a name="renum-set"></a>Enum.2: Utiliser les énumérations pour représenter des ensembles de constantes nommées liées

##### Raison

Une énumération montre que les énumérateurs sont liés et peut être un type nommé.

##### Exemple

    enum class Web_color { red = 0xFF0000, green = 0x00FF00, blue = 0x0000FF };

##### Note

Le « switch » sur une énumération est courant et le compilateur peut avertir contre des schémas de labels de case inhabituels. Par exemple :

    enum class Product_info { red = 0, purple = 1, blue = 2 };

    void print(Product_info inf)
    {
        switch (inf) {
        case Product_info::red: cout << "red"; break;
        case Product_info::purple: cout << "purple"; break;
        }
    }

De tels `switch` avec un décalage d'un pas sont souvent la conséquence d'un énumérateur ajouté et d'un test insuffisant.

##### Application

* Signaler les statements `switch` où les `case` couvrent la plupart mais pas tous les énumérateurs d'une énumération.
* Signaler les statements `switch` où les `case` couvrent seulement quelques énumérateurs d'une énumération, sans qu'il y ait de `default`.

### <a name="renum-class"></a>Enum.3: Préférer les enums de classe aux enums classiques

##### Raison

Pour minimiser les surprises : les enums traditionnels se convertissent trop facilement en `int`.

##### Exemple

    void Print_color(int color);

    enum Web_color { red = 0xFF0000, green = 0x00FF00, blue = 0x0000FF };
    enum Product_info { red = 0, purple = 1, blue = 2 };

    Web_color webby = Web_color::blue;

    // Il est clair qu'au moins l'un de ces appels est erroné.
    Print_color(webby);
    Print_color(Product_info::blue);

Au lieu d'utiliser un `enum class` :

    void Print_color(int color);

    enum class Web_color { red = 0xFF0000, green = 0x00FF00, blue = 0x0000FF };
    enum class Product_info { red = 0, purple = 1, blue = 2 };

    Web_color webby = Web_color::blue;
    Print_color(webby);  // Erreur : impossible de convertir Web_color en int.
    Print_color(Product_info::red);  // Erreur : impossible de convertir Product_info en int.

##### Application

(Simpliste) Avertir sur toute définition d'`enum` non-classe.

### <a name="renum-oper"></a>Enum.4: Définir des opérations sur les énumérations pour une utilisation sûre et simple

##### Raison

Commodité d'utilisation et évitement d'erreurs.

##### Exemple

    enum class Day { mon, tue, wed, thu, fri, sat, sun };

    Day& operator++(Day& d)
    {
        return d = (d == Day::sun) ? Day::mon : static_cast<Day>(static_cast<int>(d)+1);
    }

    Day today = Day::sat;
    Day tomorrow = ++today;

L'utilisation d'un `static_cast` n'est pas esthétique, mais

    Day& operator++(Day& d)
    {
        return d = (d == Day::sun) ? Day::mon : Day{++d};    // erreur
    }

est une récursion infinie, et l'écrire sans cast, en utilisant un `switch` sur tous les cas, est verbeux.

##### Application

Signaler les expressions répétées converties en retour dans une énumération.

### <a name="renum-caps"></a>Enum.5: Ne pas utiliser `ALL_CAPS` pour les énumérateurs

##### Raison

Éviter les collisions avec les macros.

##### Exemple, mauvais

    // webcolors.h (en-tête tiers)
    #define RED   0xFF0000
    #define GREEN 0x00FF00
    #define BLUE  0x0000FF

    // productinfo.h
    // Les lignes suivantes définissent les sous‑types de produit basés sur la couleur

    enum class Product_info { RED, PURPLE, BLUE };   // erreur de syntaxe

##### Application

Signaler les énumérateurs en majuscules (`ALL_CAPS`).

### <a name="renum-unnamed"></a>Enum.6: Éviter les énumérations non nommées

##### Raison

Si vous ne pouvez pas nommer une énumération, les valeurs ne sont pas liées.

##### Exemple, mauvais

    enum { red = 0xFF0000, scale = 4, is_signed = 1 };

##### Alternative

Utilisez plutôt des valeurs `constexpr`. Par exemple :

    constexpr int red = 0xFF0000;
    constexpr short scale = 4;
    constexpr bool is_signed = true;

##### Application

Signaler les énumérations non nommées.

### <a name="renum-underlying"></a>Enum.7: Spécifier le type sous‑jacent d'une énumération uniquement lorsque c'est nécessaire

##### Raison

La valeur par défaut est la plus simple à lire et à écrire.  
`int` est le type entier par défaut et est compatible avec les `enum` en C.

##### Exemple

    enum class Direction : char { n, s, e, w,
                                  ne, nw, se, sw };  // le type sous-jacent économise de l'espace

    enum class Web_color : int32_t { red   = 0xFF0000,
                                     green = 0x00FF00,
                                     blue  = 0x0000FF };  // le type sous-jacent est redondant

##### Note

Spécifier le type sous‑jacent est nécessaire pour déclarer en avance un `enum` ou un `enum class` :

    enum Flags : char;

    void f(Flags);

    // ....

    enum Flags : char { /* ... */ };

ou pour garantir que les valeurs de ce type ont une précision binaire spécifiée :

    enum Bitboard : uint64_t { /* ... */ };

### <a name="renum-value"></a>Enum.8: Spécifier les valeurs des énumérateurs uniquement lorsque nécessaire

##### Raison

C'est le plus simple.  
Il évite les doublons d'énumérateurs.  
La valeur par défaut donne un ensemble consécutif de valeurs qui convient aux implémentations d'un `switch`.

##### Exemple

    enum class Col1 { red, yellow, blue };
    enum class Col2 { red = 1, yellow = 2, blue = 2 }; // faute de frappe
    enum class Month { jan = 1, feb, mar, apr, may, jun,
                       jul, august, sep, oct, nov, dec }; // commencer à 1 est conventionnel
    enum class Base_flag { dec = 1, oct = dec << 1, hex = dec << 2 }; // ensemble de bits

##### Note

Spécifier les valeurs est nécessaire pour correspondre aux valeurs conventionnelles (par ex., `Month`) et lorsque des valeurs consécutives sont indésirables (par ex., pour obtenir des bits séparés comme dans `Base_flag`).

##### Application

* Signaler les valeurs d'énumérateurs en double.
* Signaler les valeurs d'énumérateurs explicitement spécifiées toutes consécutives.