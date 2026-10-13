# <a name="s-enum"></a>Enum : Énumérations

Les énumérations sont utilisées pour définir des ensembles de valeurs entières et pour définir des types pour de tels ensembles de valeurs. Il existe deux sortes d'énumérations : les `enum` « classiques » et les `enum class`.

## Résumé des règles d'énumération :

* [Enum.1 : Préférer les énumérations aux macros](008-enum.md#renum-macro)
* [Enum.2 : Utiliser les énumérations pour représenter des ensembles de constantes nommées liées](008-enum.md#renum-set)
* [Enum.3 : Préférer les `enum class` aux `enum` « classiques »](008-enum.md#renum-class)
* [Enum.4 : Définir des opérations sur les énumérations pour un usage sûr et simple](008-enum.md#renum-oper)
* [Enum.5 : Ne pas utiliser `ALL_CAPS` pour les énumérateurs](008-enum.md#renum-caps)
* [Enum.6 : Éviter les énumérations non nommées](008-enum.md#renum-unnamed)
* [Enum.7 : Spécifier le type sous‑jacent d’une énumération uniquement si nécessaire](008-enum.md#renum-underlying)
* [Enum.8 : Spécifier les valeurs des énumérateurs uniquement si nécessaire](008-enum.md#renum-value)

---

### <a name="renum-macro"></a>Enum.1 : Préférer les énumérations aux macros

##### Raison

Les macros ne respectent pas les règles de portée et de typage. De plus, les noms de macros sont supprimés lors du pré‑traitement et n’apparaissent généralement pas dans les outils tels que les débogueurs.

##### Exemple

Mauvais code historique :

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

Utilisez plutôt une `enum` :

    enum class Web_color { red = 0xFF0000, green = 0x00FF00, blue = 0x0000FF };
    enum class Product_info { red = 0, purple = 1, blue = 2 };

    int webby = blue;   // error: be specific
    Web_color webby = Web_color::blue;

Nous avons utilisé un `enum class` pour éviter les conflits de noms.

##### Note

Envisagez également les variables `constexpr` et `const inline`.

##### Application

Signaler les macros qui définissent des valeurs entières. Utiliser une `enum`, ou `const inline`, ou une autre alternative non macro à la place.

---

### <a name="renum-set"></a>Enum.2 : Utiliser les énumérations pour représenter des ensembles de constantes nommées liées

##### Raison

Une énumération montre que les énumérateurs sont liés et peut être un type nommé.

##### Exemple

    enum class Web_color { red = 0xFF0000, green = 0x00FF00, blue = 0x0000FF };

##### Note

Utiliser un `switch` sur une énumération est courant et le compilateur peut avertir contre des modèles de `case` inhabituels. Par exemple :

    enum class Product_info { red = 0, purple = 1, blue = 2 };

    void print(Product_info inf)
    {
        switch (inf) {
        case Product_info::red: cout << "red"; break;
        case Product_info::purple: cout << "purple"; break;
        }
    }

Ce type d’instructions `switch` avec un décalage d’un est souvent le résultat d’un ajout d’énumérateur et d’un manque de tests.

##### Application

* Signaler les instructions `switch` dont les `case` couvrent la plupart mais pas tous les énumérateurs d’une énumération.  
* Signaler les instructions `switch` dont les `case` ne couvrent que quelques énumérateurs d’une énumération, sans `default`.

---

### <a name="renum-class"></a>Enum.3 : Préférer les `enum class` aux `enum` « classiques »

##### Raison

Pour limiter les surprises : les `enum` traditionnels se convertissent trop facilement en `int`.

##### Exemple

    void Print_color(int color);

    enum Web_color { red = 0xFF0000, green = 0x00FF00, blue = 0x0000FF };
    enum Product_info { red = 0, purple = 1, blue = 2 };

    Web_color webby = Web_color::blue;

    // Clearly at least one of these calls is buggy.
    Print_color(webby);
    Print_color(Product_info::blue);

Utilisez plutôt un `enum class` :

    void Print_color(int color);

    enum class Web_color { red = 0xFF0000, green = 0x00FF00, blue = 0x0000FF };
    enum class Product_info { red = 0, purple = 1, blue = 2 };

    Web_color webby = Web_color::blue;
    Print_color(webby);  // Error: cannot convert Web_color to int.
    Print_color(Product_info::red);  // Error: cannot convert Product_info to int.

##### Application

Avertir sur toute définition d’`enum` non `class`.

---

### <a name="renum-oper"></a>Enum.4 : Définir des opérations sur les énumérations pour un usage sûr et simple

##### Raison

Facilité d’utilisation et prévention des erreurs.

##### Exemple

    enum class Day { mon, tue, wed, thu, fri, sat, sun };

    Day& operator++(Day& d)
    {
        return d = (d == Day::sun) ? Day::mon : static_cast<Day>(static_cast<int>(d)+1);
    }

    Day today = Day::sat;
    Day tomorrow = ++today;

L’utilisation d’un `static_cast` n’est pas très élégante, mais

    Day& operator++(Day& d)
    {
        return d = (d == Day::sun) ? Day::mon : Day{++d};    // error
    }

est une récursion infinie, et l’écrire sans cast en utilisant un `switch` couvrant tous les cas est lourd.

##### Application

Signaler les expressions répétées qui sont à nouveau castées en une énumération.

---

### <a name="renum-caps"></a>Enum.5 : Ne pas utiliser `ALL_CAPS` pour les énumérateurs

##### Raison

Éviter les conflits avec les macros.

##### Exemple, mauvais

     // webcolors.h (third party header)
    #define RED   0xFF0000
    #define GREEN 0x00FF00
    #define BLUE  0x0000FF

    // productinfo.h
    // The following define product subtypes based on color

    enum class Product_info { RED, PURPLE, BLUE };   // syntax error

##### Application

Signaler les énumérateurs en `ALL_CAPS`.

---

### <a name="renum-unnamed"></a>Enum.6 : Éviter les énumérations non nommées

##### Raison

Si vous ne pouvez pas nommer une énumération, les valeurs ne sont pas liées.

##### Exemple, mauvais

    enum { red = 0xFF0000, scale = 4, is_signed = 1 };

Ce type de code n’est pas rare dans du code écrit avant qu’il ne soit possible de spécifier des constantes entières de manière pratique.

##### Alternative

    constexpr int red = 0xFF0000;
    constexpr short scale = 4;
    constexpr bool is_signed = true;

##### Application

Signaler les énumérations non nommées.

---

### <a name="renum-underlying"></a>Enum.7 : Spécifier le type sous‑jacent d’une énumération uniquement si nécessaire

##### Raison

Le type par défaut est le plus simple à lire et à écrire. `int` est le type entier par défaut. `int` est compatible avec les `enum` en C.

##### Exemple

    enum class Direction : char { n, s, e, w,
                                  ne, nw, se, sw };  // underlying type saves space

    enum class Web_color : int32_t { red   = 0xFF0000,
                                     green = 0x00FF00,
                                     blue  = 0x0000FF };  // underlying type is redundant

##### Note

Spécifier le type sous‑jacent est nécessaire pour une déclaration anticipée (forward‑declare) d’un `enum` ou d’un `enum class` :

    enum Flags : char;

    void f(Flags);

    // ....

    enum Flags : char { /* ... */ };

ou pour garantir que les valeurs de ce type ont une précision binaire spécifiée :

    enum Bitboard : uint64_t { /* ... */ };

##### Application

????

---

### <a name="renum-value"></a>Enum.8 : Spécifier les valeurs des énumérateurs uniquement si nécessaire

##### Raison

C’est le plus simple. Cela évite les valeurs d’énumérateurs dupliquées. La valeur par défaut génère un ensemble de valeurs consécutives, ce qui est idéal pour les implémentations d’instructions `switch`.

##### Exemple

    enum class Col1 { red, yellow, blue };
    enum class Col2 { red = 1, yellow = 2, blue = 2 }; // typo
    enum class Month { jan = 1, feb, mar, apr, may, jun,
                       jul, august, sep, oct, nov, dec }; // starting with 1 is conventional
    enum class Base_flag { dec = 1, oct = dec << 1, hex = dec << 2 }; // set of bits

Spécifier les valeurs est nécessaire pour correspondre aux valeurs conventionnelles (p. ex., `Month`) et lorsque des valeurs consécutives sont indésirables (p. ex., pour obtenir des bits séparés comme dans `Base_flag`).

##### Application

* Signaler les valeurs d’énumérateurs dupliquées.  
* Signaler les valeurs d’énumérateurs explicitement spécifiées consécutives.