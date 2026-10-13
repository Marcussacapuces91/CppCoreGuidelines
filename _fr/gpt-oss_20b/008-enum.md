# <a name="s-enum"></a>Enum : Énumérations

Les énumérations servent à définir des ensembles de valeurs entières et à créer des types pour ces ensembles de valeurs. Il existe deux sortes d'énumérations : les `enum` « simples » et les `enum class`.

Résumé des règles d’énumérations :

* [Enum.1 : Préférer les énumérations aux macros](#renum-macro)
* [Enum.2 : Utiliser les énumérations pour représenter des ensembles de constantes nommées liées](#renum-set)
* [Enum.3 : Préférer les `enum class` aux `enum` « simples »](#renum-class)
* [Enum.4 : Définir des opérations sur les énumérations pour une utilisation sûre et simple](#renum-oper)
* [Enum.5 : Ne pas utiliser `ALL_CAPS` pour les énumérateurs](#renum-caps)
* [Enum.6 : Éviter les énumérations anonymes](#renum-unnamed)
* [Enum.7 : Spécifier le type sous-jacent d’une énumération uniquement quand nécessaire](#renum-underlying)
* [Enum.8 : Spécifier les valeurs des énumérateurs uniquement quand nécessaire](#renum-value)

### <a name="renum-macro"></a>Enum.1 : Préférer les énumérations aux macros

#### Raison

Les macros ne respectent pas les règles de portée et de type. De plus, leurs noms sont supprimés lors du prétraitement et ne figurent généralement pas dans les outils comme les débogueurs.

#### Exemple

Voici un ancien code mal écrit :

    // webcolors.h (third party header)
    #define RED   0xFF0000
    #define GREEN 0x00FF00
    #define BLUE  0x0000FF

    // productinfo.h
    // The following define product subtypes based on color
    #define RED    0
    #define PURPLE 1
    #define BLUE   2

    int webby = BLUE;   // webby == 2; probably not what was desired

Au lieu de cela, utilisez un `enum` :

    enum class Web_color { red = 0xFF0000, green = 0x00FF00, blue = 0x0000FF };
    enum class Product_info { red = 0, purple = 1, blue = 2 };

    int webby = blue;   // error: be specific
    Web_color webby = Web_color::blue;

Nous avons utilisé un `enum class` pour éviter les collisions de noms.

#### Remarque

Il faut également considérer les variables `constexpr` et `const inline`.

#### Application

Signaliser les macros qui définissent des valeurs entières. Utiliser un `enum`, `const inline` ou une alternative non-macro à la place.

### <a name="renum-set"></a>Enum.2 : Utiliser les énumérations pour représenter des ensembles de constantes nommées liées

#### Raison

Une énumération montre que les énumérateurs sont liés et peut être un type nommé.

#### Exemple

    enum class Web_color { red = 0xFF0000, green = 0x00FF00, blue = 0x0000FF };

#### Remarque

Passer un énumérateur dans une instruction `switch` est courant et le compilateur peut avertir contre des modèles de cas inhabituels. Par exemple :

    enum class Product_info { red = 0, purple = 1, blue = 2 };

    void print(Product_info inf)
    {
        switch (inf) {
        case Product_info::red: cout << "red"; break;
        case Product_info::purple: cout << "purple"; break;
        }
    }

Ces `switch` avec un décalage d’un sont souvent le résultat d’un énumérateur ajouté et d’un test insuffisant.

#### Application

* Signaler les instructions `switch` où les `case` couvrent la plupart mais pas tous les énumérateurs d’une énumération.
* Signaler les instructions `switch` où les `case` couvrent quelques énumérateurs, mais il n’y a pas de `default`.

### <a name="renum-class"></a>Enum.3 : Préférer les `enum class` aux `enum` « simples »

#### Raison

Pour minimiser les surprises : les `enum` traditionnels se convertissent trop facilement vers int.

#### Exemple

    void Print_color(int color);

    enum Web_color { red = 0xFF0000, green = 0x00FF00, blue = 0x0000FF };
    enum Product_info { red = 0, purple = 1, blue = 2 };

    Web_color webby = Web_color::blue;

    // Clearly at least one of these calls is buggy.
    Print_color(webby);
    Print_color(Product_info::blue);

Au lieu de cela, utilisez un `enum class` :

    void Print_color(int color);

    enum class Web_color { red = 0xFF0000, green = 0x00FF00, blue = 0x0000FF };
    enum class Product_info { red = 0, purple = 1, blue = 2 };

    Web_color webby = Web_color::blue;
    Print_color(webby);        // Error: cannot convert Web_color to int.
    Print_color(Product_info::red);  // Error: cannot convert Product_info to int.

#### Application

* (Simple) Avertir pour toute définition d’un `enum` non‑classe.

### <a name="renum-oper"></a>Enum.4 : Définir des opérations sur les énumérations pour une utilisation sûre et simple

#### Raison

La commodité d’utilisation et l’évitement d’erreurs.

#### Exemple

    enum class Day { mon, tue, wed, thu, fri, sat, sun };

    Day& operator++(Day& d)
    {
        return d = (d == Day::sun) ? Day::mon : static_cast<Day>(static_cast<int>(d)+1);
    }

    Day today = Day::sat;
    Day tomorrow = ++today;

L’utilisation d'un `static_cast` n’est pas esthétique, mais

    Day& operator++(Day& d)
    {
        return d = (d == Day::sun) ? Day::mon : Day{++d};    // error
    }

est une récursion infinie, et l’écrire sans cast, en utilisant un `switch` sur tous les cas, est laborieux.

#### Application

Signaliser les expressions répétées qui font un cast vers l’énumération.

### <a name="renum-caps"></a>Enum.5 : Ne pas utiliser `ALL_CAPS` pour les énumérateurs

#### Raison

Éviter les collisions avec les macros.

#### Exemple

    // webcolors.h (third party header)
    #define RED   0xFF0000
    #define GREEN 0x00FF00
    #define BLUE  0x0000FF

    // productinfo.h
    // The following define product subtypes based on color

    enum class Product_info { RED, PURPLE, BLUE };   // syntax error

#### Application

Signaliser les énumérateurs en `ALL_CAPS`.

### <a name="renum-unnamed"></a>Enum.6 : Éviter les énumérations anonymes

#### Raison

Si vous ne pouvez pas nommer une énumération, les valeurs ne sont pas liées.

#### Exemple, mauvaise :

    enum { red = 0xFF0000, scale = 4, is_signed = 1 };

Ce type de code n’est pas rare dans les programmes écrits avant qu’on n’ait des moyens plus pratiques pour spécifier des constantes entières.

#### Alternative

Utilisez des valeurs `constexpr` à la place :

    constexpr int red = 0xFF0000;
    constexpr short scale = 4;
    constexpr bool is_signed = true;

#### Application

Signaliser les énumérations anonymes.

### <a name="renum-underlying"></a>Enum.7 : Spécifier le type sous-jacent d’une énumération uniquement quand nécessaire

#### Raison

Le type par défaut est le plus facile à lire et à écrire.  
`int` est le type entier par défaut.  
`int` est compatible avec les énumérations C.

#### Exemple

    enum class Direction : char { n, s, e, w,
                                  ne, nw, se, sw };  // underlying type saves space

    enum class Web_color : int32_t { red   = 0xFF0000,
                                     green = 0x00FF00,
                                     blue  = 0x0000FF };  // underlying type is redundant

#### Note

Spécifier le type sous-jacent est nécessaire pour faire une déclaration anticipée d’un `enum` ou d’un `enum class` :

    enum Flags : char;

    void f(Flags);

    // ....

    enum Flags : char { /* ... */ };

ou pour vous assurer que les valeurs de ce type ont une précision binaire spécifiée :

    enum Bitboard : uint64_t { /* ... */ };

#### Application

* À définir.

### <a name="renum-value"></a>Enum.8 : Spécifier les valeurs des énumérateurs uniquement quand nécessaire

#### Raison

C’est le plus simple. Cela évite les doublons de valeurs d’énumérateurs. La valeur par défaut est une suite de valeurs consécutives, ce qui est utile pour les implémentations d’instructions `switch`.

#### Exemple

    enum class Col1 { red, yellow, blue };
    enum class Col2 { red = 1, yellow = 2, blue = 2 }; // typo
    enum class Month { jan = 1, feb, mar, apr, may, jun,
                      jul, august, sep, oct, nov, dec }; // starting with 1 is conventional
    enum class Base_flag { dec = 1, oct = dec << 1, hex = dec << 2 }; // set of bits

#### Application

* Signaler les valeurs d’énumérateurs dupliquées.
* Signaler les valeurs d’énumérateurs explicitement spécifiées et consécutives.