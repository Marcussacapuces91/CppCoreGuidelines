# <a name="s-enum"></a>Énumérations : Énumérations

Les énumérations servent à définir des ensembles de valeurs entières et à déclarer des types pour ces ensembles de valeurs.
Il existe deux types d'énumérations : les `enum` « simples » et les `enum class`.

Résumé des règles sur les énumérations :

* [Enum.1 : Privilégier les énumérations par rapport aux macros](008-enum.md#renum-macro)
* [Enum.2 : Utiliser des énumérations pour représenter des ensembles de constantes nommées liées entre elles](008-enum.md#renum-set)
* [Enum.3 : Privilégier les `enum class` par rapport aux `enum` « simples »](008-enum.md#renum-class)
* [Enum.4 : Définir des opérations sur les énumérations pour un usage sûr et simple](008-enum.md#renum-oper)
* [Enum.5 : Ne pas utiliser `MAJUSCULES` pour les énumérateurs](008-enum.md#renum-caps)
* [Enum.6 : Éviter les énumérations sans nom](008-enum.md#renum-unnamed)
* [Enum.7 : Spécifier le type sous-jacent d'une énumération uniquement quand c'est nécessaire](008-enum.md#renum-underlying)
* [Enum.8 : Spécifier les valeurs des énumérateurs uniquement quand c'est nécessaire](008-enum.md#renum-value)

### <a name="renum-macro"></a>Enum.1 : Privilégier les énumérations par rapport aux macros

##### Justification

Les macros ne respectent pas les règles de portée et de typage. De plus, les noms de macros sont supprimés lors de la précompilation et n'apparaissent donc généralement pas dans les outils comme les débogueurs.

##### Exemple

D'abord un mauvais code légendaire :

    // webcolors.h (en-tête tiers)
    #define RED   0xFF0000
    #define GREEN 0x00FF00
    #define BLUE  0x0000FF

    // productinfo.h
    // Les définitions suivantes définissent des sous-types de produits basés sur la couleur
    #define RED    0
    #define PURPLE 1
    #define BLUE   2

    int webby = BLUE;   // webby == 2 ; probablement pas ce qui était souhaité

Utilisez plutôt une `enum` :

    enum class Web_color { red = 0xFF0000, green = 0x00FF00, blue = 0x0000FF };
    enum class Product_info { red = 0, purple = 1, blue = 2 };

    int webby = blue;   // erreur : soyez explicite
    Web_color webby = Web_color::blue;

Nous avons utilisé un `enum class` pour éviter les conflits de noms.

##### Remarque

Envisagez également les variables `constexpr` et `const inline`.

##### Application

Signaler les macros qui définissent des valeurs entières. Utilisez plutôt une `enum`, une variable `const inline` ou une autre alternative non-macro.


### <a name="renum-set"></a>Enum.2 : Utiliser des énumérations pour représenter des ensembles de constantes nommées liées entre elles

##### Justification

Une énumération montre que les énumérateurs sont liés entre eux et peut servir de type nommé.



##### Exemple

    enum class Web_color { red = 0xFF0000, green = 0x00FF00, blue = 0x0000FF };


##### Remarque

L'usage de `switch` sur une énumération est courant et le compilateur peut avertir contre des motifs inhabituels d'étiquettes de cas. Par exemple :

    enum class Product_info { red = 0, purple = 1, blue = 2 };

    void print(Product_info inf)
    {
        switch (inf) {
        case Product_info::red: cout << "red"; break;
        case Product_info::purple: cout << "purple"; break;
        }
    }

Ce genre d'instructions `switch` avec une erreur de décalage d'un élément résulte souvent d'un énumérateur ajouté sans test suffisant.

##### Application

* Signaler les instructions `switch` dont les `case` couvrent la plupart mais pas tous les énumérateurs d'une énumération.
* Signaler les instructions `switch` dont les `case` ne couvrent que quelques énumérateurs d'une énumération, sans clause `default`.


### <a name="renum-class"></a>Enum.3 : Privilégier les énumérations de classe par rapport aux énumérations « simples »

##### Justification

Pour minimiser les surprises : les énumérations traditionnelles se convertissent en `int` trop facilement.

##### Exemple

    void Print_color(int color);

    enum Web_color { red = 0xFF0000, green = 0x00FF00, blue = 0x0000FF };
    enum Product_info { red = 0, purple = 1, blue = 2 };

    Web_color webby = Web_color::blue;

    // Clairement, au moins l'un de ces appels est fautif.
    Print_color(webby);
    Print_color(Product_info::blue);

Utilisez plutôt un `enum class` :

    void Print_color(int color);

    enum class Web_color { red = 0xFF0000, green = 0x00FF00, blue = 0x0000FF };
    enum class Product_info { red = 0, purple = 1, blue = 2 };

    Web_color webby = Web_color::blue;
    Print_color(webby);  // Erreur : impossible de convertir Web_color en int.
    Print_color(Product_info::red);  // Erreur : impossible de convertir Product_info en int.

##### Application

(Simple) Avertir sur toute définition d'`enum` non de classe.

### <a name="renum-oper"></a>Enum.4 : Définir des opérations sur les énumérations pour un usage sûr et simple

##### Justification

Confort d'utilisation et évitement d'erreurs.

##### Exemple

    enum class Day { mon, tue, wed, thu, fri, sat, sun };

    Day& operator++(Day& d)
    {
        return d = (d == Day::sun) ? Day::mon : static_cast<Day>(static_cast<int>(d)+1);
    }

    Day today = Day::sat;
    Day tomorrow = ++today;

L'usage d'un `static_cast` n'est pas élégant, mais

    Day& operator++(Day& d)
    {
        return d = (d == Day::sun) ? Day::mon : Day{++d};    // erreur
    }

est une récursion infinie, et le rédiger sans conversion en utilisant un `switch` sur tous les cas serait trop verbeux.


##### Application

Signaler les expressions répétées qui sont recastées dans une énumération.


### <a name="renum-caps"></a>Enum.5 : Ne pas utiliser `MAJUSCULES` pour les énumérateurs

##### Justification

Éviter les conflits avec les macros.

##### Exemple, incorrect

     // webcolors.h (en-tête tiers)
    #define RED   0xFF0000
    #define GREEN 0x00FF00
    #define BLUE  0x0000FF

    // productinfo.h
    // Les définitions suivantes définissent des sous-types de produits basés sur la couleur

    enum class Product_info { RED, PURPLE, BLUE };   // erreur de syntaxe

##### Application

Signaler les énumérateurs en MAJUSCULES.

### <a name="renum-unnamed"></a>Enum.6 : Éviter les énumérations sans nom

##### Justification

Si vous ne pouvez pas nommer une énumération, c'est que les valeurs ne sont pas liées entre elles.

##### Exemple, incorrect

    enum { red = 0xFF0000, scale = 4, is_signed = 1 };

Ce type de code n'est pas rare dans du code écrit avant qu'il n'existe des moyens alternatifs pratiques de spécifier des constantes entières.

##### Alternative

Utilisez plutôt des valeurs `constexpr`. Par exemple :

    constexpr int red = 0xFF0000;
    constexpr short scale = 4;
    constexpr bool is_signed = true;

##### Application

Signaler les énumérations sans nom.


### <a name="renum-underlying"></a>Enum.7 : Spécifier le type sous-jacent d'une énumération uniquement quand c'est nécessaire

##### Justification

Le type par défaut est le plus facile à lire et à écrire.
`int` est le type entier par défaut.
`int` est compatible avec les `enum` du C.

##### Exemple

    enum class Direction : char { n, s, e, w,
                                  ne, nw, se, sw };  // le type sous-jacent fait gagner de la place

    enum class Web_color : int32_t { red   = 0xFF0000,
                                     green = 0x00FF00,
                                     blue  = 0x0000FF };  // le type sous-jacent est redondant

##### Remarque

Spécifier le type sous-jacent est nécessaire pour déclarer en avant une enum ou un enum class :

    enum Flags : char;

    void f(Flags);

    // ....

    enum Flags : char { /* ... */ };

ou pour garantir que les valeurs de ce type ont une précision binaire spécifiée :

    enum Bitboard : uint64_t { /* ... */ };

##### Application

@TODO-LINK


### <a name="renum-value"></a>Enum.8 : Spécifier les valeurs des énumérateurs uniquement quand c'est nécessaire

##### Justification

C'est la solution la plus simple.
Cela évite les valeurs d'énumérateurs dupliquées.
Le comportement par défaut fournit un ensemble de valeurs consécutives, idéal pour les implémentations de `switch`.

##### Exemple

    enum class Col1 { red, yellow, blue };
    enum class Col2 { red = 1, yellow = 2, blue = 2 }; // faute de frappe
    enum class Month { jan = 1, feb, mar, apr, may, jun,
                       jul, august, sep, oct, nov, dec }; // commencer à 1 est conventionnel
    enum class Base_flag { dec = 1, oct = dec << 1, hex = dec << 2 }; // ensemble de bits

Spécifier des valeurs est nécessaire pour respecter des valeurs conventionnelles (p. ex. `Month`)
et quand des valeurs consécutives sont indésirables (p. ex. pour obtenir des bits distincts comme dans `Base_flag`).

##### Application

* Signaler les valeurs d'énumérateurs dupliquées.
* Signaler les valeurs d'énumérateurs explicitement spécifiées qui forment une suite entièrement consécutive.