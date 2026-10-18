# <a name="s-enum"></a>Énumérations

Les énumérations servent à définir des ensembles de valeurs entières et à créer des types pour de tels ensembles.
Il existe deux sortes d'énumérations : les énumérations « simples » (`enum`) et les énumérations de classe (`enum class`).

Résumé des règles sur les énumérations :

* [Enum.1 : Préférer les énumérations aux macros](008-enum.md#renum-macro)
* [Enum.2 : Utiliser les énumérations pour représenter des ensembles de constantes nommées liées](008-enum.md#renum-set)
* [Enum.3 : Préférer les `enum class` aux `enum` simples](008-enum.md#renum-class)
* [Enum.4 : Définir des opérations sur les énumérations pour un usage sûr et simple](008-enum.md#renum-oper)
* [Enum.5 : Ne pas utiliser les `MAJUSCULES` pour les énumérateurs](008-enum.md#renum-caps)
* [Enum.6 : Éviter les énumérations sans nom](008-enum.md#renum-unnamed)
* [Enum.7 : Spécifier le type sous-jacent d'une énumération uniquement quand c'est nécessaire](008-enum.md#renum-underlying)
* [Enum.8 : Spécifier les valeurs des énumérateurs uniquement quand c'est nécessaire](008-enum.md#renum-value)

### <a name="renum-macro"></a>Enum.1 : Préférer les énumérations aux macros

##### Justification

Les macros ne respectent ni les règles de portée ni les règles de typage. De plus, les noms de macro sont supprimés lors du pré-traitement et apparaissent donc rarement dans les outils de débogage, par exemple.

##### Exemple

D'abord, un ancien code problématique :

    // webcolors.h (en-tête tiers)
    #define RED   0xFF0000
    #define GREEN 0x00FF00
    #define BLUE  0x0000FF

    // productinfo.h
    // Les définitions suivantes décrivent les sous-types de produit selon la couleur
    #define RED    0
    #define PURPLE 1
    #define BLUE   2

    int webby = BLUE;   // webby == 2 ; ce qui n'était probablement pas le comportement attendu

Utilisez plutôt une `enum` :

    enum class Web_color { red = 0xFF0000, green = 0x00FF00, blue = 0x0000FF };
    enum class Product_info { red = 0, purple = 1, blue = 2 };

    int webby = blue;   // erreur : être explicite
    Web_color webby = Web_color::blue;

Nous avons utilisé une `enum class` pour éviter les collisions de noms.

##### Note

Envisagez également les variables `constexpr` et `const inline`.

##### Détection

Signaler les macros qui définissent des valeurs entières. Utiliser plutôt `enum`, `const inline` ou toute autre alternative non macro.


### <a name="renum-set"></a>Enum.2 : Utiliser les énumérations pour représenter des ensembles de constantes nommées liées

##### Justification

Une énumération montre que ses énumérateurs sont liés entre eux et peut servir de type nommé.



##### Exemple

    enum class Web_color { red = 0xFF0000, green = 0x00FF00, blue = 0x0000FF };


##### Note

Utiliser une instruction `switch` sur une énumération est courant, et le compilateur peut émettre un avertissement pour des motifs inhabituels de libellés de cas. Par exemple :

    enum class Product_info { red = 0, purple = 1, blue = 2 };

    void print(Product_info inf)
    {
        switch (inf) {
        case Product_info::red: cout << "red"; break;
        case Product_info::purple: cout << "purple"; break;
        }
    }

Ce type d'omission d'un cas dans un `switch` est souvent le résultat de l'ajout d'un énumérateur et d'un test insuffisant.

##### Détection

* Signaler les instructions `switch` dont les `case` couvrent la plupart mais pas tous les énumérateurs d'une énumération.
* Signaler les instructions `switch` dont les `case` ne couvrent qu'une poignée d'énumérateurs d'une énumération, alors qu'aucun `default` n'est prévu.


### <a name="renum-class"></a>Enum.3 : Préférer les énumérations de classe aux énumérations simples

##### Justification

Pour minimiser les effets de bord inattendus : les énumérations traditionnelles sont trop facilement converties en `int`.

##### Exemple

    void Print_color(int color);

    enum Web_color { red = 0xFF0000, green = 0x00FF00, blue = 0x0000FF };
    enum Product_info { red = 0, purple = 1, blue = 2 };

    Web_color webby = Web_color::blue;

    // Au moins l'un de ces appels est manifestement erroné.
    Print_color(webby);
    Print_color(Product_info::blue);

Utilisez plutôt une `enum class` :

    void Print_color(int color);

    enum class Web_color { red = 0xFF0000, green = 0x00FF00, blue = 0x0000FF };
    enum class Product_info { red = 0, purple = 1, blue = 2 };

    Web_color webby = Web_color::blue;
    Print_color(webby);  // Erreur : impossible de convertir Web_color en int.
    Print_color(Product_info::red);  // Erreur : impossible de convertir Product_info en int.

##### Détection

(Simple) Émettre un avertissement pour toute définition de `enum` non de classe.

### <a name="renum-oper"></a>Enum.4 : Définir des opérations sur les énumérations pour un usage sûr et simple

##### Justification

Confort d'utilisation et prévention des erreurs.

##### Exemple

    enum class Day { mon, tue, wed, thu, fri, sat, sun };

    Day& operator++(Day& d)
    {
        return d = (d == Day::sun) ? Day::mon : static_cast<Day>(static_cast<int>(d)+1);
    }

    Day today = Day::sat;
    Day tomorrow = ++today;

L'utilisation d'un `static_cast` n'est pas élégante, mais

    Day& operator++(Day& d)
    {
        return d = (d == Day::sun) ? Day::mon : Day{++d};    // erreur
    }

est une récession infinie, et écrire cette fonction sans cast, en énumérant tous les cas dans un `switch`, est long et fastidieux.


##### Détection

Signaler les expressions qui recastent systématiquement une valeur dans une énumération.


### <a name="renum-caps"></a>Enum.5 : Ne pas utiliser les `MAJUSCULES` pour les énumérateurs

##### Justification

Éviter les collisions avec les macros.

##### Exemple, incorrect

    // webcolors.h (en-tête tiers)
    #define RED   0xFF0000
    #define GREEN 0x00FF00
    #define BLUE  0x0000FF

    // productinfo.h
    // Les définitions suivantes décrivent les sous-types de produit selon la couleur

    enum class Product_info { RED, PURPLE, BLUE };   // erreur de syntaxe

##### Détection

Signaler les énumérateurs en MAJUSCULES.

### <a name="renum-unnamed"></a>Enum.6 : Éviter les énumérations sans nom

##### Justification

Si vous ne pouvez pas donner de nom à une énumération, c'est que ses valeurs ne sont pas réellement liées entre elles.

##### Exemple, incorrect

    enum { red = 0xFF0000, scale = 4, is_signed = 1 };

Ce type de code n'est pas rare dans du code écrit avant l'existence d'alternatives pratiques pour spécifier des constantes entières.

##### Alternative

Utiliser des valeurs `constexpr` à la place. Par exemple :

    constexpr int red = 0xFF0000;
    constexpr short scale = 4;
    constexpr bool is_signed = true;

##### Détection

Signaler les énumérations sans nom.


### <a name="renum-underlying"></a>Enum.7 : Spécifier le type sous-jacent d'une énumération uniquement quand c'est nécessaire

##### Justification

Le type par défaut est le plus lisible et le plus facile à écrire.
`int` est le type entier par défaut.
`int` est compatible avec les `enum` du C.

##### Exemple

    enum class Direction : char { n, s, e, w,
                                  ne, nw, se, sw };  // le type sous-jacent permet d'économiser de l'espace

    enum class Web_color : int32_t { red   = 0xFF0000,
                                     green = 0x00FF00,
                                     blue  = 0x0000FF };  // le type sous-jacent est redondant

##### Note

La spécification du type sous-jacent est nécessaire pour faire une déclaration anticipée d'une enum ou enum class :

    enum Flags : char;

    void f(Flags);

    // ....

    enum Flags : char { /* ... */ };

ou pour garantir que les valeurs de ce type ont une précision binaire spécifique :

    enum Bitboard : uint64_t { /* ... */ };

##### Détection

????


### <a name="renum-value"></a>Enum.8 : Spécifier les valeurs des énumérateurs uniquement quand c'est nécessaire

##### Justification

C'est la solution la plus simple.
Cela évite les valeurs en double parmi les énumérateurs.
Par défaut, on obtient une suite de valeurs consécutives, pratique pour les implémentations d'instructions `switch`.

##### Exemple

    enum class Col1 { red, yellow, blue };
    enum class Col2 { red = 1, yellow = 2, blue = 2 }; // coquille
    enum class Month { jan = 1, feb, mar, apr, may, jun,
                       jul, august, sep, oct, nov, dec }; // commencer à 1 est conventionnel
    enum class Base_flag { dec = 1, oct = dec << 1, hex = dec << 2 }; // ensemble de bits

La spécification des valeurs est nécessaire pour correspondre à des valeurs conventionnelles (par ex. `Month`)
ainsi que dans les cas où des valeurs consécutives sont indésirables (par ex. obtenir des bits distincts comme dans `Base_flag`).

##### Détection

* Signaler les valeurs en double parmi les énumérateurs.
* Signaler les valeurs explicitement spécifiées qui sont toutes consécutives.