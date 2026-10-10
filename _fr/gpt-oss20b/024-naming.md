# <a name="s-naming"></a>NL: Suggestions de nommage et de mise en page

Un nommage et une mise en page cohérents sont utiles.  
En particulier, cela minimise les arguments du type « mon style est meilleur que le vôtre ».  
Cependant, il existe de nombreux styles différents et les gens y sont passionnés (pro et con).  
De plus, la plupart des projets réels intègrent du code provenant de nombreuses sources; il est donc souvent impossible de standardiser sur un seul style pour tout le code.  
Suite à de nombreuses requêtes d’assistance, nous présentons un ensemble de règles que vous pourriez utiliser en l’absence d’idées meilleures, mais l’objectif réel est la cohérence, plutôt qu’un ensemble de règles particulier.  
Les IDE et outils peuvent aider (tout comme freiner).

## Naming and layout rules

* [NL.1: Ne dites pas dans les commentaires ce qui peut être clairement exprimé dans le code](#rl-comments)
* [NL.2: Exprimez l'intention dans les commentaires](#rl-comments-intent)
* [NL.3: Gardez les commentaires concis](#rl-comments-crisp)
* [NL.4: Maintenez un style d'indentation cohérent](#rl-indent)
* [NL.5: Évitez d'encoder les informations de type dans les noms](#rl-name-type)
* [NL.7: Faites en sorte que la longueur d'un nom soit à peu près proportionnelle à l'étendue de son champ](#rl-name-length)
* [NL.8: Utilisez un style de nommage cohérent](#rl-name)
* [NL.9: Utilisez `ALL_CAPS` uniquement pour les noms de macro](#rl-all-caps)
* [NL.10: Préférez les noms en underscore_style](#rl-camel)
* [NL.11: Rendez les littéraux lisibles](#rl-literals)
* [NL.15: Utilisez les espaces avec parcimonie](#rl-space)
* [NL.16: Utilisez un ordre conventionnel de déclaration des membres de classe](#rl-order)
* [NL.17: Utilisez la mise en page dérivée de K&R](#rl-knr)
* [NL.18: Utilisez la mise en page du déclarateur de style C++](#rl-ptr)
* [NL.19: Évitez les noms facilement mal lus](#rl-misread)
* [NL.20: Ne placez pas deux instructions sur la même ligne](#rl-stmt)
* [NL.21: Déclarez un seul nom (seulement) par déclaration](#rl-dcl)
* [NL.25: N'utilisez pas `void` comme type d'argument](#rl-void)
* [NL.26: Utilisez la notation conventionnelle `const`](#rl-const)
* [NL.27: Utilisez l'extension .cpp pour les fichiers de code et .h pour les fichiers d'interface](#rl-file-suffix)

La plupart de ces règles sont esthétiques et les programmeurs ont des opinions fortes.  
Les IDE ont aussi tendance à avoir des valeurs par défaut et une gamme d’alternatives.  
Ces règles sont des valeurs par défaut suggérées à suivre, sauf si vous avez des raisons de ne pas le faire.

Nous avons reçu des commentaires indiquant que le nommage et la mise en page sont si personnels et/ou arbitraires que nous ne devrions pas tenter de les « légiférer ». Nous ne « légiférons » pas (voir le paragraphe précédent).  
Cependant, nous avons reçu de nombreuses demandes d’un ensemble de conventions de nommage et de mise en page à utiliser lorsqu’il n’y a pas de contraintes externes.

Des règles plus spécifiques et détaillées sont plus faciles à faire respecter.

Ces règles ressemblent fortement aux recommandations du [PPP Style Guide](https://www.stroustrup.com/Programming/PPP-style.pdf), écrit en soutien du livre de Stroustrup [Programming: Principles and Practice using C++](https://www.stroustrup.com/programming.html).

## <a name="rl-comments"></a>NL.1: Ne dites pas dans les commentaires ce qui peut être clairement exprimé dans le code

### Raison

Les compilateurs ne lisent pas les commentaires.  
Les commentaires sont moins précis que le code.  
Les commentaires ne sont pas mis à jour de façon aussi régulière que le code.

### Exemple, mauvais

    auto x = m * v1 + vv;   // multiplier m par v1 et ajouter le résultat à vv

### Application

Construisez un programme d’IA qui interprète un texte en anglais familier et vérifiez si ce qui est dit pourrait être mieux exprimé en C++.

## <a name="rl-comments-intent"></a>NL.2: Exprimez l'intention dans les commentaires

### Raison

Le code indique ce qui est fait, pas ce qui est supposé être fait. Souvent l'intention peut être exprimée plus clairement et plus concisément que l'implémentation.

### Exemple

    void stable_sort(Sortable& c)
        // trie c dans l'ordre déterminé par <, conserve les éléments égaux (définis par ==) dans
        // leur ordre relatif d'origine
    {
        // ... quite a few lines of non-trivial code ...
    }

### Remarque

Si le commentaire et le code ne correspondent pas, il est probable qu'ils soient tous les deux incorrects.

## <a name="rl-comments-crisp"></a>NL.3: Gardez les commentaires concis

### Raison

La verbosité ralentit la compréhension et rend le code plus difficile à lire en le dispersant dans le fichier source.

### Remarque

Utilisez un anglais intelligible.  
Je pourrais être couramment bilingue français, mais la plupart des programmeurs ne le sont pas ; les responsables de mon code ne le seront peut-être pas.  
Évitez le langage SMS et surveillez votre grammaire, ponctuation et capitalisation.  
Viser le professionnalisme, pas le « cool ».

### Application

impossible.

## <a name="rl-indent"></a>NL.4: Maintenez un style d'indentation cohérent

### Raison

Lisibilité. Évitement des « erreurs stupides ».

### Exemple, mauvais

    int i;
    for (i = 0; i < max; ++i); // bogue qui attend d'arriver
    if (i == j)
        return i;

### Remarque

Il est généralement une bonne idée d'indiquer la déclaration après `if (...)`, `for (...)` et `while (...)` :

    if (i < 0) error("negative argument");

    if (i < 0)
        error("negative argument");

### Application

Utilisez un outil.

## <a name="rl-name-type"></a>NL.5: Évitez d'encoder les informations de type dans les noms

### Motif

Si les noms reflètent des types plutôt qu’une fonctionnalité, il devient difficile de changer les types employés pour fournir cette fonctionnalité.  
De plus, si le type d’une variable change, le code qui l’utilise doit être modifié.  
Minimisez les conversions non voulues.

### Exemple, mauvais

    void print_int(int i);
    void print_string(const char*);

    print_int(1);          // répétitif, correspondance manuelle de type
    print_string("xyzzy"); // répétitif, correspondance manuelle de type

### Exemple, bon

    void print(int i);
    void print(string_view);    // fonctionne également sur toute séquence semblable à une chaîne

    print(1);              // clair, correspondance de type automatique
    print("xyzzy");        // clair, correspondance de type automatique

### Remarque

Les noms où les types sont encodés sont soit verbeux soit cryptiques.

    printS  // affiche un std::string
    prints  // affiche une chaîne C‑style
    printi  // affiche un int

L’utilisation de techniques comme la notation hongroise pour encoder un type a été utilisée dans des langages non typés, mais elle est généralement inutile et nuisible dans un langage fortement typé statiquement comme le C++, car ces annotations deviennent obsolètes (les défauts sont semblables aux commentaires et se détériorent comme eux) et elles interfèrent avec une bonne utilisation du langage (utilisez le même nom et la résolution de surcharge).

### Remarque

Certains styles utilisent des préfixes très généraux (non spécifiques à un type) pour indiquer l’usage général d’une variable.

    auto p = new User();
    auto p = make_unique<User>();
    // note : "p" n'est pas utilisé pour dire « pointeur brut vers User »,
    //        juste pour dire « c’est une indirection »

    auto cntHits = calc_total_of_hits(/*...*/);
    // note : "cnt" n'est pas utilisé pour encoder un type,
    //        juste pour dire « c’est un compte de quelque chose »

Ceci n’est pas nuisible et ne relève pas de cette directive car il ne encode pas l’information de type.

### Remarque

Certains styles distinguent les membres des variables locales, et/ou des variables globales.

    struct S {
        int m_;
        S(int m) : m_{abs(m)} { }
    };

Ceci n’est pas nuisible et ne relève pas de cette directive car il ne encode pas l’information de type.

### Remarque

Comme le C++, certains styles distinguent les types des non-types.  
Par exemple, en capitalisant les noms de type, mais pas les noms de fonctions et de variables.

    typename<typename T>
    class HashTable {   // maps string to T
        // ...
    };

    HashTable<int> index;

Ceci n’est pas nuisible et ne relève pas de cette directive car il ne encode pas l’information de type.

## <a name="rl-name-length"></a>NL.7: Faites en sorte que la longueur d'un nom soit à peu près proportionnelle à l'étendue de son champ

**Motif** : Plus l’étendue est grande, plus la chance de confusion et de collision inattendue augmente.

### Exemple

    double sqrt(double x);   // renvoie la racine carrée de x ; x doit être non négatif

    int length(const char* p);  // renvoie le nombre de caractères dans une chaîne C‑style terminée par zéro

    int length_of_string(const char zero_terminated_array_of_char[])    // mauvais : verbeux

    int g;      // mauvais : variable globale avec un nom cryptique

    int open;   // mauvais : variable globale avec un nom court, populaire

L’utilisation de `p` pour un pointeur et de `x` pour une variable flottante est conventionnelle et non trompeuse dans un champ restreint.

### Application

???

## <a name="rl-name"></a>NL.8: Utilisez un style de nommage cohérent

**Motif** : La cohérence dans le choix et le style des noms augmente la lisibilité.

### Remarque

Il existe de nombreux styles et, lorsque vous utilisez plusieurs bibliothèques, vous ne pouvez pas suivre toutes leurs conventions différentes.  
Choisissez un *style d’entreprise*, mais laissez les bibliothèques *importées* avec leur style original.

### Exemple

Standard ISO, utilisez uniquement des minuscules et des chiffres, séparez les mots avec des underscores :

* `int`
* `vector`
* `my_map`

Évitez les noms d’identificateurs contenant des soulignements doubles `__` ou commençant par un soulignement suivi d’une majuscule (par ex. `_Throws`). Ces identificateurs sont réservés à l’implémentation C++.

### Exemple

[Stroustrup](https://www.stroustrup.com/Programming/PPP-style.pdf) : Standard ISO, mais en utilisant la majuscule pour vos propres types et concepts :

* `int`
* `vector`
* `My_map`

### Exemple

CamelCase : mettez la majuscule à chaque mot d’un identifiant composé :

* `int`
* `vector`
* `MyMap`
* `myMap`

Certains styles mettent la majuscule à la première lettre, d’autres pas.

### Remarque

Soyez cohérent dans l’emploi d’acronymes et de la longueur des identificateurs :

    int mtbf {12};
    int mean_time_between_failures {12}; // choisissez une convention

## <a name="rl-all-caps"></a>NL.9: Utilisez `ALL_CAPS` uniquement pour les noms de macro

### Raison

Éviter de confondre les macros avec les noms qui respectent les règles de portée et de type.

### Exemple

    void f()
    {
        const int SIZE{1000};  // mauvais, utilisez « size » à la place
        int v[SIZE];
    }

### Remarque

En particulier, cela évite de confondre les macros avec les constantes symboliques non macro (voir aussi [Enum.5 : Ne pas utiliser `ALL_CAPS` pour les énumérateurs](#renum-caps))
@TODO-LINK

    enum bad { BAD, WORSE, HORRIBLE }; // BAD

### Application

* Marquez les macros en minuscules  
* Marquez les noms non macro en `ALL_CAPS`

## <a name="rl-camel"></a>NL.10: Préférez les noms en underscore_style

### Raison

L’usage des soulignements pour séparer les parties d’un nom est le style original de C et C++ et est utilisé dans la bibliothèque standard C++.

### Remarque

Cette règle est une valeur par défaut à utiliser uniquement si vous avez un choix.  
Souvent, vous n’avez pas de choix et devez suivre un style établi pour la [cohérence](#rl-name).  
Le besoin de cohérence l’emporte sur le goût personnel.

Ceci est une recommandation pour [lorsque vous n’avez pas de contraintes ou d’idées meilleures](024-naming.md).  
Cette règle a été ajoutée après de nombreuses demandes de conseils.

### Exemple

[Stroustrup](https://www.stroustrup.com/Programming/PPP-style.pdf) : Standard ISO, mais en utilisant la majuscule pour vos propres types et concepts  :

* `int`
* `vector`
* `My_map`

### Application

Impossible.

## <a name="rl-literals"></a>NL.11: Rendez les littéraux lisibles

### Raison

Lisibilité.

### Exemple

Utilisez des séparateurs de chiffres pour éviter de longues chaînes de chiffres

    auto c = 299'792'458; // m/s2
    auto q2 = 0b0000'1111'0000'0000;
    auto ss_number = 123'456'7890;

### Exemple

Utilisez des suffixes littéraux quand une clarification est nécessaire

    auto hello = "Hello!"s; // une std::string
    auto world = "world";   // une chaîne C‑style
    auto interval = 100ms;  // en utilisant <chrono>

### Remarque

Les littéraux ne doivent pas être répandus partout dans le code comme ["magic constants"](#res-magic),
@TODO-LINK
mais il est toujours une bonne idée de les rendre lisibles où ils sont définis.  
Il est facile de commettre une faute de frappe dans une longue chaîne d’entiers.

### Application

Marquez les longues séquences de chiffres. Le problème est de définir « long » ; peut‑être 7.

## <a name="rl-space"></a>NL.15: Utilisez les espaces avec parcimonie

### Raison

Trop d’espace rend le texte plus grand et distrayant.

### Exemple, mauvais

    #include < map >

    int main(int argc, char * argv [ ])
    {
        // ...
    }

### Exemple

    #include <map>

    int main(int argc, char* argv[])
    {
        // ...
    }

### Remarque

Certains IDE ont leurs propres opinions et ajoutent un espace distrayant.  
Ceci est une recommandation pour [lorsque vous n’avez pas de contraintes ou d’idées meilleures](024-naming.md).  
Cette règle a été ajoutée après de nombreuses demandes de conseils.

### Remarque

Nous apprécions l’espacement bien placé comme aide importante à la lisibilité. Ne faites simplement pas trop.

## <a name="rl-order"></a>NL.16: Utilisez un ordre conventionnel de déclaration des membres de classe

### Raison

Un ordre conventionnel des membres améliore la lisibilité.

Lors de la déclaration d’une classe utilisez l’ordre suivant

- types : classes, enums et alias (`using`)
- constructeurs, affectations, destructeur
- fonctions
- données

Utilisez l’ordre `public` avant `protected` avant `private`.

Ceci est une recommandation pour [lorsque vous n’avez pas de contraintes ou d’idées meilleures](024-naming.md).  
Cette règle a été ajoutée après de nombreuses demandes de conseils.

### Exemple

    class X {
    public:
        // interface
    protected:
        // fonction non vérifiée pour utilisation par les implémentations de classes dérivées
    private:
        // détails d'implémentation
    };

### Exemple

Parfois, l’ordre par défaut des membres entre en conflit avec le désir de séparer l’interface publique des détails d’implémentation.  
Dans de tels cas, les types et fonctions privés peuvent être placés avec les données privées.

    class X {
    public:
        // interface
    protected:
        // fonction non vérifiée pour utilisation par les implémentations de classes dérivées
    private:
        // détails d'implémentation (types, fonctions et données)
    };

### Exemple, mauvais

Évitez plusieurs blocs de déclarations d’un même accès (p. ex. `public`) dispersés parmi des blocs de déclarations avec d’autres accès (ex. `private`).

    class X {   // mauvais
    public:
        void f();
    public:
        int g();
        // ...
    }

L’utilisation de macros pour déclarer des groupes de membres conduit souvent à violer n’importe quelle règle d’ordre.  
Cependant, l’utilisation de macros rend vague ce qui est exprimé de toute façon.

### Application

Marquez les écarts par rapport à l’ordre suggéré. Il y aura beaucoup de vieux codes qui ne suivent pas cette règle.

## <a name="rl-knr"></a>NL.17: Utilisez la mise en page dérivée de K&R

### Raison

C’est la mise en page originale de C et C++. Elle préserve bien l’espace vertical. Elle distingue bien les différents constructions du langage (telles que fonctions et classes).

### Remarque

Dans le contexte de C++, ce style est souvent appelé « Stroustrup ».

Ceci est une recommandation pour [lorsque vous n’avez pas de contraintes ou d’idées meilleures](024-naming.md).  
Cette règle a été ajoutée après de nombreuses demandes de conseils.

### Exemple

    struct Cable {
        int x;
        // ...
    };

    double foo(int x)
    {
        if (0 < x) {
            // ...
        }

        switch (x) {
        case 0:
            // ...
            break;
        case amazing:
            // ...
            break;
        default:
            // ...
            break;
        }

        if (0 < x)
            ++x;

        if (x < 0)
            something();
        else
            something_else();

        return some_value;
    }

Remarquez l’espace entre `if` et `(`

### Remarque

Utilisez des lignes séparées pour chaque instruction, les branches d’un `if`, et le corps d’un `for`.

### Remarque

Le `{` pour une `class` et un `struct` n’est généralement *pas* sur une ligne séparée, mais le `{` pour une fonction l’est.

### Remarque

Capitalisez les noms de vos types définis par l’utilisateur pour les distinguer des types de la bibliothèque standard.

### Remarque

Ne capitalisez pas les noms de fonction.

### Application

Si vous voulez appliquer une vérification, utilisez un IDE pour reformat.

## <a name="rl-ptr"></a>NL.18: Utilisez la mise en page du déclarateur de style C++

### Raison

Le format C souligne l’utilisation dans les expressions et la grammaire, alors que le format C++ souligne les types.  
L’utilisation des expressions ne tient pas pour les références.

### Exemple

    T& operator[](size_t);   // OK
    T &operator[](size_t);   // juste étrange
    T & operator[](size_t);   // indécis

### Remarque

Ceci est une recommandation pour [lorsque vous n’avez pas de contraintes ou d’idées meilleures](024-naming.md).  
Cette règle a été ajoutée après de nombreuses demandes de conseils.

### Application

Impossible face à l’histoire.

## <a name="rl-misread"></a>NL.19: Évitez les noms facilement mal lus

### Raison

Lisibilité.  
Tout le monde n’a pas d’écrans ou d’imprimantes qui rendent facile de distinguer tous les caractères.  
Nous confondons facilement des mots semblables et légèrement mal orthographiés.

### Exemple

    int oO01lL = 6; // mauvais

    int splunk = 7;
    int splonk = 8; // mauvais : splunk et splonk sont facilement confus

### Application

???

## <a name="rl-stmt"></a>NL.20: Ne placez pas deux instructions sur la même ligne

### Raison

Lisibilité.  
Il est vraiment facile d’omettre une instruction lorsqu’il y a plus sur une ligne.

### Exemple

    int x = 7; char* p = 29;    // ne pas
    int x = 7; f(x);  ++x;      // ne pas

### Application

Facile.

## <a name="rl-dcl"></a>NL.21: Déclarez un seul nom (seulement) par déclaration

### Raison

Lisibilité.  
Réduire la confusion avec la syntaxe de déclarateur.

### Remarque

Pour plus de détails, voir [ES.10](#res-name-one).  
@TODO-LINK

## <a name="rl-void"></a>NL.25: N'utilisez pas `void` comme type d'argument

### Raison

C’est verbeux et n’est requis que lorsqu’il y a compatibilité C.

### Exemple

    void f(void);   // mauvais

    void g();       // mieux

### Remarque

Même Dennis Ritchie a qualifié `void f(void)` d’abomination.  
Vous pouvez faire un argument pour que l’abomination soit abominable en C quand les prototypes de fonctions étaient rares, afin que bannir :

    int f();
    f(1, 2, "weird but valid C89");   // hope that f() is defined int f(a, b, c) char* c; { /* ... */ }

avoirait causé de gros problèmes, mais non au 21ᵉ siècle et en C++.

## <a name="rl-const"></a>NL.26: Utilisez la notation conventionnelle `const`

### Raison

La notation conventionnelle est plus familière à plus de programmeurs.  
La cohérence dans les grandes bases de code.

### Exemple

    const int x = 7;    // OK
    int const y = 9;    // mauvais

    const int *const p = nullptr;   // OK, pointeur constant vers int constant
    int const *const p = nullptr;   // mauvais, pointeur constant vers int constant

### Remarque

Nous sommes bien conscients que vous pourriez dire que les exemples « mauvais » sont plus logiques que ceux marqués « OK », mais ils sont plus confus pour beaucoup, en particulier les novices qui se réfèrent à du matériel d’enseignement davantage aux deux exemples « OK ».

### Application

Marquez le `const` utilisé comme suffixe d’un type.

## <a name="rl-file-suffix"></a>NL.27: Utilisez l’extension .cpp pour les fichiers de code et .h pour les fichiers d’interface

### Raison

C’est une convention de longue date.  
Mais la cohérence est plus importante, donc si votre projet utilise quelque chose d’autre, suivez‑le.

### Remarque

Cette convention reflète un motif d’utilisation commun :  
Les en-têtes sont plus souvent partagés avec le C pour compiler en C++ et en C, ce qui utilise généralement des `.h`,  
et il est plus facile de nommer tous les en-têtes `.h` plutôt que d’avoir des extensions différentes uniquement pour ces en-têtes destinés à être partagés avec le C.  
D’un autre côté, les fichiers d’implémentation sont rarement partagés avec le C et devraient donc généralement différer des fichiers `.c`,  
et il est donc généralement préférable de nommer tous les fichiers d’implémentation C++ plutôt que `.c`.

Les noms particuliers `.h` et `.cpp` ne sont pas obligatoires (seulement une valeur par défaut) et d’autres noms sont largement utilisés.  
Exemples : `.hh`, `.C`, et `.cxx`. Utilisez ces noms de façon équivalente.  
Dans ce document, nous faisons référence aux `.h` et aux `.cpp` comme un raccourci pour les fichiers d’en-tête et d’implémentation, même si l’extension réelle pourrait être différente.

Votre IDE (si vous en utilisez un) peut avoir des opinions fortes sur les suffixes.

### Exemple

    // foo.h:
    extern int a;   // une déclaration
    extern void foo();

    // foo.cpp:
    int a;   // une définition
    void foo() { ++a; }

`foo.h` fournit l'interface à `foo.cpp`. Les variables globales sont à éviter.

### Exemple, mauvais

    // foo.h:
    int a;   // une définition
    void foo() { ++a; }

`#include <foo.h>` deux fois dans un programme et vous obtiendrez une erreur de liaison pour deux violations de la règle d’une seule définition.

### Application

* Marquez les noms de fichiers non conventionnels.  
* Vérifiez que les `.h` et `.cpp` (et équivalents) suivent les règles ci-dessous.