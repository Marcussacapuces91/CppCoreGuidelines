# <a name="s-naming"></a>NL : Suggestions de nommage et de mise en page

Un nommage et une mise en page cohérents sont utiles.
Même pour cette seule raison, car cela minimise les débats du type « mon style est meilleur que le tien ».
Cependant, il existe de nombreux styles différents et les gens y sont passionnément attachés (pour ou contre).
De plus, la plupart des projets réels intègrent du code provenant de nombreuses sources, ce qui rend souvent impossible l'adoption d'un style unique pour l'ensemble du code.
Après de nombreuses demandes de la part des utilisateurs, nous présentons un ensemble de règles que vous pouvez adopter si vous n'avez pas de meilleure idée, mais l'objectif réel est la cohérence, plutôt qu'un ensemble de règles particulier.
Les IDE et les outils peuvent aider (mais aussi nuire).

Règles de nommage et de mise en page :

* [NL.1 : Ne pas dire dans un commentaire ce qui peut être clairement exprimé dans le code](024-naming.md#rl-comments)
* [NL.2 : Exprimer l'intention dans les commentaires](024-naming.md#rl-comments-intent)
* [NL.3 : Garder les commentaires concis](024-naming.md#rl-comments-crisp)
* [NL.4 : Maintenir un style d'indentation cohérent](024-naming.md#rl-indent)
* [NL.5 : Éviter d'encoder des informations de type dans les noms](024-naming.md#rl-name-type)
* [NL.7 : Rendre la longueur d'un nom approximativement proportionnelle à la taille de sa portée](024-naming.md#rl-name-length)
* [NL.8 : Utiliser un style de nommage cohérent](024-naming.md#rl-name)
* [NL.9 : Réserver `MAJUSCULES` aux noms de macros uniquement](024-naming.md#rl-all-caps)
* [NL.10 : Préférer les noms en `style_sous_ligne`](024-naming.md#rl-camel)
* [NL.11 : Rendre les littéraux lisibles](024-naming.md#rl-literals)
* [NL.15 : Utiliser les espaces avec parcimonie](024-naming.md#rl-space)
* [NL.16 : Utiliser un ordre conventionnel pour la déclaration des membres de classe](024-naming.md#rl-order)
* [NL.17 : Utiliser une mise en page dérivée de K&R](024-naming.md#rl-knr)
* [NL.18 : Utiliser la mise en page des déclarateurs à la C++](024-naming.md#rl-ptr)
* [NL.19 : Éviter les noms facilement mal interprétés](024-naming.md#rl-misread)
* [NL.20 : Ne pas placer deux instructions sur la même ligne](024-naming.md#rl-stmt)
* [NL.21 : Déclarer un seul nom par déclaration](024-naming.md#rl-dcl)
* [NL.25 : Ne pas utiliser `void` comme type d'argument](024-naming.md#rl-void)
* [NL.26 : Utiliser la notation conventionnelle de `const`](024-naming.md#rl-const)
* [NL.27 : Utiliser le suffixe `.cpp` pour les fichiers de code et `.h` pour les fichiers d'interface](024-naming.md#rl-file-suffix)

La plupart de ces règles sont esthétiques et les programmeurs ont des opinions fermes à leur sujet.
Les IDE ont également tendance à avoir des valeurs par défaut et un éventail d'alternatives.
Ces règles sont des valeurs par défaut suggérées à suivre, sauf si vous avez des raisons de ne pas le faire.

Nous avons reçu des commentaires indiquant que le nommage et la mise en page sont si personnels et/ou arbitraires que nous ne devrions pas essayer de les « légiférer ».
Nous ne « légiférons » pas (voir le paragraphe précédent).
Cependant, nous avons reçu de nombreuses demandes pour un ensemble de conventions de nommage et de mise en page à utiliser en l'absence de contraintes externes.

Des règles plus spécifiques et détaillées sont plus faciles à faire respecter.

Ces règles ressemblent fortement aux recommandations du [Guide de style PPP](https://www.stroustrup.com/Programming/PPP-style.pdf),
rédigé en soutien à l'ouvrage de Stroustrup [Programming: Principles and Practice using C++](https://www.stroustrup.com/programming.html).

### <a name="rl-comments"></a>NL.1 : Ne pas dire dans un commentaire ce qui peut être clairement exprimé dans le code

##### Raison

Les compilateurs ne lisent pas les commentaires.
Les commentaires sont moins précis que le code.
Les commentaires ne sont pas mis à jour aussi régulièrement que le code.

##### Exemple, incorrect

    auto x = m * v1 + vv;   // multiplier m par v1 et ajouter le résultat à vv

##### Application

Construire un programme d'IA qui interprète le texte anglais courant et vérifier si ce qui est dit pourrait être mieux exprimé en C++.

### <a name="rl-comments-intent"></a>NL.2 : Exprimer l'intention dans les commentaires

##### Raison

Le code indique ce qui est fait, pas ce qui est censé être fait. Souvent, l'intention peut être exprimée plus clairement et plus concisément que l'implémentation.

##### Exemple

    void stable_sort(Sortable& c)
        // trier c dans l'ordre déterminé par <, en conservant les éléments égaux (définis par ==)
        // dans leur ordre relatif d'origine
    {
        // ... un certain nombre de lignes de code non triviales ...
    }

##### Remarque

Si le commentaire et le code sont en désaccord, il est probable que les deux soient erronés.

### <a name="rl-comments-crisp"></a>NL.3 : Garder les commentaires concis

##### Raison

La verbosité ralentit la compréhension et rend le code plus difficile à lire en l'éparpillant dans le fichier source.

##### Remarque

Utiliser un anglais compréhensible.
Je peux être bilingue en danois, mais la plupart des programmeurs ne le sont pas ; les mainteneurs de mon code ne le sont peut-être pas non plus.
Éviter le langage SMS et veiller à la grammaire, à la ponctuation et à la majuscule.
Viser le professionnalisme, pas le « cool ».

##### Application

Impossible.

### <a name="rl-indent"></a>NL.4 : Maintenir un style d'indentation cohérent

##### Raison

Lisibilité. Éviter les « erreurs bêtes ».

##### Exemple, incorrect

    int i;
    for (i = 0; i < max; ++i); // bug en puissance
    if (i == j)
        return i;

##### Remarque

Indenter systématiquement l'instruction après `if (...)`, `for (...)` et `while (...)` est généralement une bonne idée :

    if (i < 0) error("argument négatif");

    if (i < 0)
        error("argument négatif");

##### Application

Utiliser un outil.

### <a name="rl-name-type"></a>NL.5 : Éviter d'encoder des informations de type dans les noms

##### Justification

Si les noms reflètent les types plutôt que la fonctionnalité, il devient difficile de changer les types utilisés pour fournir cette fonctionnalité.
De plus, si le type d'une variable est modifié, le code qui l'utilise devra être modifié.
Minimiser les conversions non intentionnelles.

##### Exemple, incorrect

    void print_int(int i);
    void print_string(const char*);

    print_int(1);          // répétitif, correspondance de type manuelle
    print_string("xyzzy"); // répétitif, correspondance de type manuelle

##### Exemple, correct

    void print(int i);
    void print(string_view);    // fonctionne aussi sur toute séquence de type chaîne

    print(1);              // clair, correspondance de type automatique
    print("xyzzy");        // clair, correspondance de type automatique

##### Remarque

Les noms avec des types encodés sont soit verbeux, soit cryptiques.

    printS  // imprimer un std::string
    prints  // imprimer une chaîne au style C
    printi  // imprimer un int

Exiger des techniques comme la notation hongroise pour encoder un type a été utilisé dans les langages non typés, mais est généralement inutile et activement nuisible dans un langage fortement typé statiquement comme C++, car les annotations deviennent obsolètes (les verrues sont comme des commentaires et pourrissent de la même façon) et elles entravent une bonne utilisation du langage (utiliser le même nom et la résolution de surcharge à la place).

##### Remarque

Certains styles utilisent des préfixes très généraux (non spécifiques au type) pour indiquer l'usage général d'une variable.

    auto p = new User();
    auto p = make_unique<User>();
    // note : « p » n'est pas utilisé pour dire « pointeur brut vers le type User »,
    //       mais simplement pour dire « c'est une référence indirecte »

    auto cntHits = calc_total_of_hits(/*...*/);
    // note : « cnt » n'est pas utilisé pour encoder un type,
    //       mais simplement pour dire « c'est un compteur de quelque chose »

Ceci n'est pas nuisible et ne relève pas de cette directive car cela n'encode pas d'information de type.

##### Remarque

Certains styles distinguent les membres des variables locales, et/ou des variables globales.

    struct S {
        int m_;
        S(int m) : m_{abs(m)} { }
    };

Ceci n'est pas nuisible et ne relève pas de cette directive car cela n'encode pas d'information de type.

##### Remarque

Comme en C++, certains styles distinguent les types des non-types.
Par exemple, en majuscule les noms de types, mais pas les noms de fonctions et de variables.

    typename<typename T>
    class HashTable {   // associe une chaîne à T
        // ...
    };

    HashTable<int> index;

Ceci n'est pas nuisible et ne relève pas de cette directive car cela n'encode pas d'information de type.

### <a name="rl-name-length"></a>NL.7 : Rendre la longueur d'un nom approximativement proportionnelle à la taille de sa portée

**Justification** : Plus la portée est grande, plus la probabilité de confusion et de collision de noms non intentionnelle est élevée.

##### Exemple

    double sqrt(double x);   // renvoie la racine carrée de x ; x doit être non négatif

    int length(const char* p);  // renvoie le nombre de caractères d'une chaîne C terminée par zéro

    int length_of_string(const char zero_terminated_array_of_char[])    // incorrect : verbeux

    int g;      // incorrect : variable globale au nom cryptique

    int open;   // incorrect : variable globale au nom court et courant

L'utilisation de `p` pour un pointeur et `x` pour une variable à virgule flottante est conventionnelle et non ambiguë dans une portée restreinte.

##### Application

???

### <a name="rl-name"></a>NL.8 : Utiliser un style de nommage cohérent

**Justification** : La cohérence dans le nommage et le style de nommage augmente la lisibilité.

##### Remarque

Il existe de nombreux styles et lorsque vous utilisez plusieurs bibliothèques, vous ne pouvez pas suivre toutes leurs conventions différentes.
Choisissez un « style de la maison », mais laissez les bibliothèques « importées » avec leur style d'origine.

##### Exemple

Norme ISO, utiliser uniquement des minuscules et des chiffres, séparer les mots par des tirets bas :

* `int`
* `vector`
* `my_map`

Éviter les noms d'identifiants contenant des doubles tirets bas `__` ou commençant par un tiret bas suivi d'une majuscule (par ex. `_Throws`).
De tels identifiants sont réservés à l'implémentation C++.

##### Exemple

[Stroustrup](https://www.stroustrup.com/Programming/PPP-style.pdf) :
Norme ISO, mais avec des majuscules pour vos propres types et concepts :

* `int`
* `vector`
* `My_map`

##### Exemple

CamelCase : mettre en majuscule chaque mot dans un identifiant multi-mots :

* `int`
* `vector`
* `MyMap`
* `myMap`

Certaines conventions mettent en majuscule la première lettre, d'autres non.

##### Remarque

Essayez d'être cohérent dans l'utilisation des acronymes et la longueur des identifiants :

    int mtbf {12};
    int mean_time_between_failures {12}; // décidez-vous

##### Application

Ce serait possible, à l'exception de l'utilisation de bibliothèques aux conventions variées.

### <a name="rl-all-caps"></a>NL.9 : Réserver `MAJUSCULES` aux noms de macros uniquement

##### Raison

Pour éviter de confondre les macros avec des noms qui obéissent aux règles de portée et de type.

##### Exemple

    void f()
    {
        const int SIZE{1000};  // Incorrect, utiliser « size » à la place
        int v[SIZE];
    }

##### Remarque

En particulier, cela évite de confondre les macros avec des constantes symboliques non-macro (voir aussi [Enum.5 : Ne pas utiliser `MAJUSCULES` pour les énumérateurs](008-enum.md#renum-caps))

    enum bad { BAD, WORSE, HORRIBLE }; // MAUVAIS

##### Application

* Signaler les macros contenant des minuscules
* Signaler les noms non-macro en `MAJUSCULES`

### <a name="rl-camel"></a>NL.10 : Préférer les noms en `style_sous_ligne`

##### Raison

L'utilisation de tirets bas pour séparer les parties d'un nom est le style original de C et C++ et est utilisé dans la bibliothèque standard C++.

##### Remarque

Cette règle est une valeur par défaut à n'utiliser que si vous avez le choix.
Souvent, vous n'avez pas le choix et devez suivre un style établi pour la [cohérence](024-naming.md#rl-name).
Le besoin de cohérence prime sur le goût personnel.

Ceci est une recommandation pour [lorsque vous n'avez ni contraintes ni meilleure idée](024-naming.md).
Cette règle a été ajoutée après de nombreuses demandes de guidance.

##### Exemple

[Stroustrup](https://www.stroustrup.com/Programming/PPP-style.pdf) :
Norme ISO, mais avec des majuscules pour vos propres types et concepts :

* `int`
* `vector`
* `My_map`

##### Application

Impossible.

### <a name="rl-literals"></a>NL.11 : Rendre les littéraux lisibles

##### Raison

Lisibilité.

##### Exemple

Utiliser des séparateurs de chiffres pour éviter de longues suites de chiffres

    auto c = 299'792'458; // m/s²
    auto q2 = 0b0000'1111'0000'0000;
    auto ss_number = 123'456'7890;

##### Exemple

Utiliser des suffixes de littéraux lorsque la clarification est nécessaire

    auto hello = "Hello!"s; // un std::string
    auto world = "world";   // une chaîne au style C
    auto interval = 100ms;  // en utilisant <chrono>

##### Remarque

Les littéraux ne doivent pas être éparpillés partout dans le code en tant que [« constantes magiques »](010-expr.md#res-magic),
mais il reste une bonne idée de les rendre lisibles là où ils sont définis.
Il est facile de faire une coquille dans une longue suite de chiffres.

##### Application

Signaler les longues suites de chiffres. Le problème est de définir « longue » ; peut-être 7.

### <a name="rl-space"></a>NL.15 : Utiliser les espaces avec parcimonie

##### Raison

Trop d'espaces rend le texte plus volumineux et distrait.

##### Exemple, incorrect

    #include < map >

    int main(int argc, char * argv [ ])
    {
        // ...
    }

##### Exemple

    #include <map>

    int main(int argc, char* argv[])
    {
        // ...
    }

##### Remarque

Certains IDE ont leurs propres opinions et ajoutent des espaces distrayants.

Ceci est une recommandation pour [lorsque vous n'avez ni contraintes ni meilleure idée](024-naming.md).
Cette règle a été ajoutée après de nombreuses demandes de guidance.

##### Remarque

Nous valorisons les espaces bien placés comme une aide significative à la lisibilité. Ne les abusez simplement pas.

### <a name="rl-order"></a>NL.16 : Utiliser un ordre conventionnel pour la déclaration des membres de classe

##### Raison

Un ordre conventionnel des membres améliore la lisibilité.

Lors de la déclaration d'une classe, utiliser l'ordre suivant :

* types : classes, énumérations et alias (`using`)
* constructeurs, affectations, destructeur
* fonctions
* données

Utiliser l'ordre `public` avant `protected` avant `private`.

Ceci est une recommandation pour [lorsque vous n'avez ni contraintes ni meilleure idée](024-naming.md).
Cette règle a été ajoutée après de nombreuses demandes de guidance.

##### Exemple

    class X {
    public:
        // interface
    protected:
        // fonction non vérifiée pour usage par les implémentations de classes dérivées
    private:
        // détails d'implémentation
    };

##### Exemple

Parfois, l'ordre par défaut des membres entre en conflit avec le souhait de séparer l'interface publique des détails d'implémentation.
Dans de tels cas, les types et fonctions privés peuvent être placés avec les données privées.

    class X {
    public:
        // interface
    protected:
        // fonction non vérifiée pour usage par les implémentations de classes dérivées
    private:
        // détails d'implémentation (types, fonctions et données)
    };

##### Exemple, incorrect

Éviter de multiples blocs de déclarations d'un même accès (par ex. `public`) dispersés parmi des blocs de déclarations avec un accès différent (par ex. `private`).

    class X {   // incorrect
    public:
        void f();
    public:
        int g();
        // ...
    };

L'utilisation de macros pour déclarer des groupes de membres conduit souvent à la violation de toute règle d'ordre.
Cependant, l'utilisation de macros obscurcit de toute façon ce qui est exprimé.

##### Application

Signaler les écarts par rapport à l'ordre suggéré. Il y aura beaucoup de code ancien qui ne suit pas cette règle.

### <a name="rl-knr"></a>NL.17 : Utiliser une mise en page dérivée de K&R

##### Raison

C'est la mise en page originale de C et C++. Elle préserve bien l'espace vertical. Elle distingue bien les différentes constructions du langage (telles que les fonctions et les classes).

##### Remarque

Dans le contexte de C++, ce style est souvent appelé « Stroustrup ».

Ceci est une recommandation pour [lorsque vous n'avez ni contraintes ni meilleure idée](024-naming.md).
Cette règle a été ajoutée après de nombreuses demandes de guidance.

##### Exemple

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

Notez l'espace entre `if` et `(`

##### Remarque

Utiliser des lignes séparées pour chaque instruction, les branches d'un `if` et le corps d'un `for`.

##### Remarque

Le `{` d'une `class` et d'un `struct` n'est *pas* sur une ligne séparée, mais le `{` d'une fonction l'est.

##### Remarque

Mettre en majuscule les noms de vos types définis par l'utilisateur pour les distinguer des types de la bibliothèque standard.

##### Remarque

Ne pas mettre en majuscule les noms de fonctions.

##### Application

Si vous souhaitez une application, utilisez un IDE pour reformater.

### <a name="rl-ptr"></a>NL.18 : Utiliser la mise en page des déclarateurs à la C++

##### Raison

La mise en page au style C met l'accent sur l'utilisation dans les expressions et la grammaire, tandis que la mise en page au style C++ met l'accent sur les types.
L'argument de l'utilisation dans les expressions ne tient pas pour les références.

##### Exemple

    T& operator[](size_t);   // OK
    T &operator[](size_t);   // simplement étrange
    T & operator[](size_t);   // indécis

##### Remarque

Ceci est une recommandation pour [lorsque vous n'avez ni contraintes ni meilleure idée](024-naming.md).
Cette règle a été ajoutée après de nombreuses demandes de guidance.

##### Application

Impossible face à l'histoire.


### <a name="rl-misread"></a>NL.19 : Éviter les noms facilement mal interprétés

##### Raison

Lisibilité.
Tout le monde n'a pas des écrans et des imprimantes qui facilitent la distinction de tous les caractères.
Nous confondons facilement des mots orthographiés de manière similaire et légèrement mal orthographiés.

##### Exemple

    int oO01lL = 6; // incorrect

    int splunk = 7;
    int splonk = 8; // incorrect : splunk et splonk sont facilement confondus

##### Application

???

### <a name="rl-stmt"></a>NL.20 : Ne pas placer deux instructions sur la même ligne

##### Raison

Lisibilité.
Il est très facile de négliger une instruction lorsqu'il y en a plus sur une ligne.

##### Exemple

    int x = 7; char* p = 29;    // à éviter
    int x = 7; f(x);  ++x;      // à éviter

##### Application

Facile.

### <a name="rl-dcl"></a>NL.21 : Déclarer un seul nom par déclaration

##### Raison

Lisibilité.
Minimiser la confusion avec la syntaxe du déclarateur.

##### Remarque

Pour les détails, voir [ES.10](010-expr.md#res-name-one).


### <a name="rl-void"></a>NL.25 : Ne pas utiliser `void` comme type d'argument

##### Raison

C'est verbeux et n'est nécessaire que lorsque la compatibilité avec C est importante.

##### Exemple

    void f(void);   // incorrect

    void g();       // meilleur

##### Remarque

Même Dennis Ritchie considérait `void f(void)` comme une abomination.
On peut faire un argument en faveur de cette abomination en C lorsque les prototypes de fonctions étaient rares, de sorte qu'interdire :

    int f();
    f(1, 2, "étrange mais du C89 valide");   // en espérant que f() est défini comme int f(a, b, c) char* c; { /* ... */ }

aurait causé de graves problèmes, mais pas au 21e siècle et pas en C++.

### <a name="rl-const"></a>NL.26 : Utiliser la notation conventionnelle de `const`

##### Raison

La notation conventionnelle est plus familière pour plus de programmeurs.
Cohérence dans les grandes bases de code.

##### Exemple

    const int x = 7;    // OK
    int const y = 9;    // incorrect

    const int *const p = nullptr;   // OK, pointeur constant vers int constant
    int const *const p = nullptr;   // incorrect, pointeur constant vers int constant

##### Remarque

Nous sommes bien conscients que vous pourriez affirmer que les exemples « incorrects » sont plus logiques que ceux marqués « OK »,
mais ils confondent aussi plus de gens, en particulier les novices qui s'appuient sur des supports pédagogiques utilisant le style OK conventionnel beaucoup plus courant.

Comme toujours, rappelez-vous que l'objectif de ces règles de nommage et de mise en page est la cohérence et que l'esthétique varie énormément.

Ceci est une recommandation pour [lorsque vous n'avez ni contraintes ni meilleure idée](024-naming.md).
Cette règle a été ajoutée après de nombreuses demandes de guidance.

##### Application

Signaler `const` utilisé comme suffixe d'un type.

### <a name="rl-file-suffix"></a>NL.27 : Utiliser le suffixe `.cpp` pour les fichiers de code et `.h` pour les fichiers d'interface

##### Raison

C'est une convention de longue date.
Mais la cohérence est plus importante, donc si votre projet utilise autre chose, suivez-le.

##### Remarque

Cette convention reflète un schéma d'utilisation courant :
Les en-têtes sont plus souvent partagés avec C pour être compilés en C++ et en C, ce qui utilise typiquement `.h`,
et il est plus facile de nommer tous les en-têtes `.h` plutôt que d'avoir des extensions différentes pour seulement ceux qui sont destinés à être partagés avec C.
D'autre part, les fichiers d'implémentation sont rarement partagés avec C et doivent donc typiquement être distingués des fichiers `.c`,
il est donc normalement préférable de nommer tous les fichiers d'implémentation C++ autrement (comme `.cpp`).

Les noms spécifiques `.h` et `.cpp` ne sont pas obligatoires (simplement recommandés par défaut) et d'autres noms sont largement utilisés.
Des exemples sont `.hh`, `.C` et `.cxx`. Utilisez de tels noms de manière équivalente.
Dans ce document, nous faisons référence à `.h` et `.cpp` comme raccourci pour les fichiers d'en-tête et d'implémentation,
même si l'extension réelle peut être différente.

Votre IDE (si vous en utilisez un) peut avoir des opinions fortes sur les suffixes.

##### Exemple

    // foo.h :
    extern int a;   // une déclaration
    extern void foo();

    // foo.cpp :
    int a;   // une définition
    void foo() { ++a; }

`foo.h` fournit l'interface de `foo.cpp`. Les variables globales sont à éviter autant que possible.

##### Exemple, incorrect

    // foo.h :
    int a;   // une définition
    void foo() { ++a; }

`#include <foo.h>` deux fois dans un programme et vous obtenez une erreur de lien pour deux violations de la règle d'une seule définition.

##### Application

* Signaler les noms de fichiers non conventionnels.
* Vérifier que `.h` et `.cpp` (et équivalents) suivent les règles ci-dessus.
