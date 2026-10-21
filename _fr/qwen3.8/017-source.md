# <a name="s-source"></a>SF : Fichiers source

Distinguer les déclarations (utilisées comme interfaces) des définitions (utilisées comme implémentations).
Utiliser les fichiers d'en-tête pour représenter les interfaces et souligner la structure logique.

Résumé des règles sur les fichiers source :

* [SF.1 : Utiliser un suffixe `.cpp` pour les fichiers de code et `.h` pour les fichiers d'interface si votre projet ne suit pas déjà une autre convention](017-source.md#rs-file-suffix)
* [SF.2 : Un fichier d'en-tête ne doit pas contenir de définitions d'objets ni de définitions de fonctions non `inline`](017-source.md#rs-inline)
* [SF.3 : Utiliser des fichiers d'en-tête pour toutes les déclarations utilisées dans plusieurs fichiers source](017-source.md#rs-declaration-header)
* [SF.4 : Inclure les fichiers d'en-tête avant les autres déclarations dans un fichier](017-source.md#rs-include-order)
* [SF.5 : Un fichier `.cpp` doit inclure le(s) fichier(s) d'en-tête qui définit sa(son) interface](017-source.md#rs-consistency)
* [SF.6 : Utiliser les directives `using namespace` uniquement pour la transition, pour les bibliothèques de base (telles que `std`), ou dans un périmètre local (uniquement)](017-source.md#rs-using)
* [SF.7 : Ne pas écrire `using namespace` au périmètre global dans un fichier d'en-tête](017-source.md#rs-using-directive)
* [SF.8 : Utiliser des gardes d'inclusion (`#include` guards) pour tous les fichiers d'en-tête](017-source.md#rs-guards)
* [SF.9 : Éviter les dépendances cycliques entre fichiers source](017-source.md#rs-cycles)
* [SF.10 : Éviter les dépendances sur des noms inclus implicitement via `#include`](017-source.md#rs-implicit)
* [SF.11 : Les fichiers d'en-tête doivent être autonomes](017-source.md#rs-contained)
* [SF.12 : Préférer la forme avec guillemets de `#include` pour les fichiers relatifs au fichier incluant, et la forme avec chevrons partout ailleurs](017-source.md#rs-incform)
* [SF.13 : Utiliser des identifiants de fichiers d'en-tête portables dans les directives `#include`](017-source.md#rs-portable-header-id)

* [SF.20 : Utiliser des `namespace` pour exprimer la structure logique](017-source.md#rs-namespace)
* [SF.21 : Ne pas utiliser un espace de noms anonyme dans un fichier d'en-tête](017-source.md#rs-unnamed)
* [SF.22 : Utiliser un espace de noms anonyme pour toutes les entités internes/non exportées](017-source.md#rs-unnamed2)

### <a name="rs-file-suffix"></a>SF.1 : Utiliser un suffixe `.cpp` pour les fichiers de code et `.h` pour les fichiers d'interface si votre projet ne suit pas déjà une autre convention

Voir [NL.27](024-naming.md#rl-file-suffix)

### <a name="rs-inline"></a>SF.2 : Un fichier d'en-tête ne doit pas contenir de définitions d'objets ni de définitions de fonctions non `inline`

##### Raison

Inclure des entités soumises à la règle d'une seule définition entraîne des erreurs de liaison.

##### Exemple

    // file.h :
    namespace Foo {
        int x = 7;
        int xx() { return x+x; }
    }

    // file1.cpp :
    #include <file.h>
    // ... suite ...

    // file2.cpp :
    #include <file.h>
    // ... suite ...

La liaison de `file1.cpp` et `file2.cpp` produira deux erreurs du lien.

**Formulation alternative** : Un fichier d'en-tête ne doit contenir que :

* des `#include` d'autres fichiers d'en-tête (éventuellement avec gardes d'inclusion)
* des gabarits (templates)
* des définitions de classes
* des déclarations de fonctions
* des déclarations `extern`
* des définitions de fonctions `inline`
* des définitions `constexpr`
* des définitions `const`
* des alias `using`
* ???

##### Application

Vérifier la liste positive ci-dessus.

### <a name="rs-declaration-header"></a>SF.3 : Utiliser des fichiers d'en-tête pour toutes les déclarations utilisées dans plusieurs fichiers source

##### Raison

Maintenabilité. Lisibilité.

##### Exemple, mauvais

    // bar.cpp :
    void bar() { cout << "bar\n"; }

    // foo.cpp :
    extern void bar();
    void foo() { bar(); }

Un mainteneur de `bar` ne peut pas trouver toutes les déclarations de `bar` si son type doit changer.
L'utilisateur de `bar` ne peut pas savoir si l'interface utilisée est complète et correcte. Au mieux, les messages d'erreur proviennent (en retard) du lien.

##### Application

* Signaler les déclarations d'entités dans d'autres fichiers source qui ne sont pas placées dans un fichier `.h`.

### <a name="rs-include-order"></a>SF.4 : Inclure les fichiers d'en-tête avant les autres déclarations dans un fichier

##### Raison

Minimiser les dépendances contextuelles et augmenter la lisibilité.

##### Exemple

    #include <vector>
    #include <algorithm>
    #include <string>

    // ... mon code ici ...

##### Exemple, mauvais

    #include <vector>

    // ... mon code ici ...

    #include <algorithm>
    #include <string>

##### Remarque

Cela s'applique aussi bien aux fichiers `.h` qu'aux fichiers `.cpp`.

##### Remarque

On peut argumenter en faveur de l'isolement du code par rapport aux déclarations et macros des fichiers d'en-tête en incluant les en-têtes *après* le code que l'on souhaite protéger
(comme dans l'exemple étiqueté « mauvais »).
Cependant :

* cela ne fonctionne que pour un seul fichier (à un seul niveau) : utiliser cette technique dans un en-tête inclus avec d'autres en-têtes fait réapparaître la vulnérabilité.
* un espace de noms (un « espace de noms d'implémentation ») peut protéger contre de nombreuses dépendances contextuelles.
* une protection et une flexibilité complètes nécessitent les modules.

**Voir aussi** :

* [Working Draft, Extensions to C++ for Modules](https://www.open-std.org/jtc1/sc22/wg21/docs/papers/2016/n4592.pdf)
* [Modules, Componentization, and Transition](https://www.open-std.org/jtc1/sc22/wg21/docs/papers/2016/p0141r0.pdf)

##### Application

Facile.

### <a name="rs-consistency"></a>SF.5 : Un fichier `.cpp` doit inclure le(s) fichier(s) d'en-tête qui définit sa(son) interface

##### Raison

Cela permet au compilateur d'effectuer une vérification de cohérence précoce.

##### Exemple, mauvais

    // foo.h :
    void foo(int);
    int bar(long);
    int foobar(int);

    // foo.cpp :
    void foo(int) { /* ... */ }
    int bar(double) { /* ... */ }
    double foobar(int);

Les erreurs ne seront pas détectées avant la phase de liaison pour un programme appelant `bar` ou `foobar`.

##### Exemple

    // foo.h :
    void foo(int);
    int bar(long);
    int foobar(int);

    // foo.cpp :
    #include "foo.h"

    void foo(int) { /* ... */ }
    int bar(double) { /* ... */ }
    double foobar(int);   // erreur : type de retour incorrect

L'erreur de type de retour de `foobar` est maintenant détectée immédiatement lors de la compilation de `foo.cpp`.
L'erreur de type d'argument de `bar` ne peut pas être détectée avant la phase de liaison à cause de la possibilité de surcharge, mais l'utilisation systématique de fichiers `.h` augmente la probabilité qu'elle soit détectée plus tôt par le programmeur.

##### Application

???

### <a name="rs-using"></a>SF.6 : Utiliser les directives `using namespace` uniquement pour la transition, pour les bibliothèques de base (telles que `std`), ou dans un périmètre local (uniquement)

##### Raison

`using namespace` peut entraîner des conflits de noms, il doit donc être utilisé avec parcimonie.
Cependant, il n'est pas toujours possible de qualifier chaque nom d'un espace de noms dans le code utilisateur (par exemple, pendant la transition)
et parfois un espace de noms est si fondamental et omniprésent dans une base de code qu'un qualificatif systématique serait verbeux et distrayant.

##### Exemple

    #include <string>
    #include <vector>
    #include <iostream>
    #include <memory>
    #include <algorithm>

    using namespace std;

    // ...

Ici (évidemment), la bibliothèque standard est utilisée de manière omniprésente et apparemment aucune autre bibliothèque n'est utilisée, donc exiger `std::` partout
pourrait être distrayant.

##### Exemple

L'utilisation de `using namespace std;` expose le programmeur à un conflit de noms avec un nom de la bibliothèque standard

    #include <cmath>
    using namespace std;

    int g(int x)
    {
        int sqrt = 7;
        // ...
        return sqrt(x); // erreur
    }

Cependant, il est peu probable que cela conduise à une résolution qui ne soit pas une erreur,
et les personnes qui utilisent `using namespace std` sont censées connaître `std` et ce risque.

##### Remarque

Un fichier `.cpp` est une forme de périmètre local.
Il y a peu de différence dans les opportunités de conflits de noms entre un fichier `.cpp` de N lignes contenant un `using namespace X`,
une fonction de N lignes contenant un `using namespace X`,
et M fonctions contenant chacune un `using namespace X` avec N lignes de code au total.

##### Remarque

[Ne pas écrire `using namespace` au périmètre global dans un fichier d'en-tête](017-source.md#rs-using-directive).

### <a name="rs-using-directive"></a>SF.7 : Ne pas écrire `using namespace` au périmètre global dans un fichier d'en-tête

##### Raison

Le faire prive celui qui inclut (`#include`) de la capacité de désambiguïser efficacement et d'utiliser des alternatives. Cela rend également les en-têtes inclus dépendants de l'ordre, car ils peuvent avoir un sens différent selon l'ordre d'inclusion.

##### Exemple

    // bad.h
    #include <iostream>
    using namespace std; // mauvais

    // user.cpp
    #include "bad.h"

    bool copy(/*... certains paramètres ...*/);    // une fonction qui se trouve s'appeler copy

    int main()
    {
        copy(/*...*/);    // surcharge maintenant ::copy local et std::copy, peut être ambigu
    }

##### Remarque

Une exception est `using namespace std::literals;`. C'est nécessaire pour utiliser des littéraux de chaîne
dans les fichiers d'en-tête et étant donné [les règles](https://eel.is/c++draft/over.literal) — les utilisateurs sont tenus
de nommer leurs propres UDL `operator""_x` — ils ne entreront pas en collision avec la bibliothèque standard.

##### Application

Signaler `using namespace` au périmètre global dans un fichier d'en-tête.

### <a name="rs-guards"></a>SF.8 : Utiliser des gardes d'inclusion (`#include` guards) pour tous les fichiers d'en-tête

##### Raison

Pour éviter qu'un fichier soit inclus (`#include`) plusieurs fois.

Afin d'éviter les collisions de gardes d'inclusion, ne nommer pas simplement la garde d'après le nom du fichier.
S'assurer d'inclure également une clé et un bon différenciateur, tel que le nom de la bibliothèque ou du composant
auquel le fichier d'en-tête appartient.

##### Exemple

    // fichier foobar.h :
    #ifndef LIBRARY_FOOBAR_H
    #define LIBRARY_FOOBAR_H
    // ... déclarations ...
    #endif // LIBRARY_FOOBAR_H

##### Application

Signaler les fichiers `.h` sans gardes d'inclusion.

##### Remarque

Certaines implémentations proposent des extensions spécifiques au fournisseur comme `#pragma once` en alternative aux gardes d'inclusion.
Ce n'est pas standard et ce n'est pas portable. Cela injecte la sémantique du système de fichiers de la machine hôte
dans votre programme, en plus de vous lier à un fournisseur.
Notre recommandation est d'écrire en C++ ISO : voir [règle P.2](004-philosophy.md#rp-cplusplus).

### <a name="rs-cycles"></a>SF.9 : Éviter les dépendances cycliques entre fichiers source

##### Raison

Les cycles compliquent la compréhension et ralentissent la compilation. Ils compliquent également
la conversion vers l'utilisation de modules pris en charge par le langage (quand ils deviendront
disponibles).

##### Remarque

Éliminer les cycles ; ne pas simplement les briser avec des gardes d'inclusion.

##### Exemple, mauvais

    // file1.h :
    #include "file2.h"

    // file2.h :
    #include "file3.h"

    // file3.h :
    #include "file1.h"

##### Application

Signaler tous les cycles.

### <a name="rs-implicit"></a>SF.10 : Éviter les dépendances sur des noms inclus implicitement via `#include`

##### Raison

Éviter les surprises.
Éviter de devoir modifier les `#include` si un en-tête inclus change.
Éviter de devenir accidentellement dépendant de détails d'implémentation et d'entités logiquement séparées incluses dans un en-tête.

##### Exemple, mauvais

    #include <iostream>
    using namespace std;

    void use()
    {
        string s;
        cin >> s;               // correct
        getline(cin, s);        // erreur : getline() non défini
        if (s == "surprise") {  // erreur : == non défini
            // ...
        }
    }

`<iostream>` expose la définition de `std::string` (« pourquoi ? » fait une bonne question de culture générale),
mais il n'est pas tenu de le faire en incluant transitivement l'intégralité de l'en-tête `<string>`,
ce qui donne lieu à la question populaire des débutants « pourquoi `getline(cin,s);` ne fonctionne-t-il pas ? »
ou même occasionnellement « les `string` ne peuvent pas être comparés avec `==` »).

La solution est d'inclure explicitement `<string>` :

##### Exemple, bon

    #include <iostream>
    #include <string>
    using namespace std;

    void use()
    {
        string s;
        cin >> s;               // correct
        getline(cin, s);        // correct
        if (s == "surprise") {  // correct
            // ...
        }
    }

##### Remarque

Certains en-têtes existent précisément pour collecter un ensemble de déclarations cohérentes à partir de divers en-têtes.
Par exemple :

    // basic_std_lib.h :

    #include <string>
    #include <map>
    #include <iostream>
    #include <random>
    #include <vector>

un utilisateur peut maintenant obtenir cet ensemble de déclarations avec un seul `#include`

    #include "basic_std_lib.h"

Cette règle contre l'inclusion implicite n'a pas pour but d'empêcher une telle agrégation délibérée.

##### Application

L'application nécessiterait une certaine connaissance de ce qui, dans un en-tête, est destiné à être « exporté » vers les utilisateurs et ce qui y est présent pour permettre l'implémentation.
Aucune solution vraiment bonne n'est possible tant que nous n'avons pas de modules.

### <a name="rs-contained"></a>SF.11 : Les fichiers d'en-tête doivent être autonomes

##### Raison

Utilisabilité : les en-têtes doivent être simples à utiliser et fonctionner lorsqu'ils sont inclus isolément.
Les en-têtes doivent encapsuler la fonctionnalité qu'ils fournissent.
Éviter que les clients d'un en-tête aient à gérer les dépendances de cet en-tête.

##### Exemple

    #include "helpers.h"
    // helpers.h dépend de std::string et inclut <string>

##### Remarque

Le non-respect de cette règle entraîne des erreurs difficiles à diagnostiquer pour les clients d'un en-tête.

##### Remarque

Un en-tête doit inclure toutes ses dépendances. Faire attention à l'utilisation de chemins relatifs car les implémentations C++ divergent sur leur signification.

##### Application

Un test doit vérifier que le fichier d'en-tête lui-même se compile ou qu'un fichier `.cpp` qui n'inclut que le fichier d'en-tête se compile.

### <a name="rs-incform"></a>SF.12 : Préférer la forme avec guillemets de `#include` pour les fichiers relatifs au fichier incluant, et la forme avec chevrons partout ailleurs

##### Raison

La [norme](https://eel.is/c++draft/cpp.include) offre une flexibilité aux compilateurs pour implémenter
les deux formes de `#include` sélectionnées à l'aide de la syntaxe avec chevrons (`<>`) ou avec guillemets (`""`). Les fournisseurs en
profitent et utilisent des algorithmes de recherche et des méthodes de spécification du chemin d'inclusion différents.

Néanmoins, la recommandation est d'utiliser la forme avec guillemets pour inclure des fichiers qui existent à un chemin relatif par rapport au fichier contenant la directive `#include` (au sein du même composant ou projet) et d'utiliser la forme avec chevrons partout ailleurs, lorsque c'est possible. Cela encourage à être clair sur la localité du fichier par rapport aux fichiers qui l'incluent, ou sur les scénarios où l'algorithme de recherche différent est requis. Cela permet de comprendre d'un coup d'œil si un en-tête est inclus depuis un fichier local relatif ou depuis un en-tête de la bibliothèque standard ou un en-tête du chemin de recherche alternatif (par exemple, un en-tête d'une autre bibliothèque ou un ensemble commun d'inclusions).

##### Exemple

    // foo.cpp :
    #include <string>                // De la bibliothèque standard, nécessite la forme <>
    #include <some_library/common.h> // Un fichier non localement relatif, inclus depuis une autre bibliothèque ; utiliser la forme <>
    #include "foo.h"                 // Un fichier localement relatif à foo.cpp dans le même projet, utiliser la forme ""
    #include "util/util.h"           // Un fichier localement relatif à foo.cpp dans le même projet, utiliser la forme ""
    #include <component_b/bar.h>     // Un fichier du même projet localisé via un chemin de recherche, utiliser la forme <>

##### Remarque

Le non-respect de cette règle entraîne des erreurs difficiles à diagnostiquer dues à la récupération du mauvais fichier en spécifiant incorrectement le périmètre lors de l'inclusion. Par exemple, dans un cas typique où l'algorithme de recherche de `#include ""` recherche d'abord un fichier existant à un chemin relatif local, puis l'utilisation de cette forme pour référencer un fichier non localement relatif pourrait signifier que si un fichier venait à exister au chemin relatif local (par exemple, le fichier incluant est déplacé vers un nouvel emplacement), il serait maintenant trouvé avant le fichier d'inclusion précédent et l'ensemble des inclusions aurait été modifié de manière inattendue.

Les créateurs de bibliothèques doivent placer leurs en-têtes dans un dossier et faire inclure ces fichiers par les clients en utilisant le chemin relatif `#include <some_library/common.h>`

##### Application

Un test doit identifier si les en-têtes référencés via `""` pourraient être référencés avec `<>`.

### <a name="rs-portable-header-id"></a>SF.13 : Utiliser des identifiants de fichiers d'en-tête portables dans les directives `#include`

##### Raison

La [norme](https://eel.is/c++draft/cpp.include) ne spécifie pas comment les compilateurs localisent de manière unique les en-têtes à partir d'un identifiant dans une directive `#include`, ni ce qui constitue l'unicité. Par exemple, si l'implémentation considère les identifiants comme sensibles à la casse, ou si les identifiants sont des chemins de système de fichiers vers un fichier d'en-tête, et le cas échéant, comment un chemin de système de fichiers hiérarchique est délimité.

Pour maximiser la portabilité des directives `#include` entre compilateurs, la recommandation est de :

* utiliser la sensibilité à la casse pour l'identifiant de l'en-tête, en correspondance avec la manière dont l'en-tête est défini par la norme, la spécification, l'implémentation ou le fichier qui fournit l'en-tête.
* lorsque l'identifiant de l'en-tête est un chemin de fichier hiérarchique, utiliser le slash avant `/` pour délimiter les composants du chemin, car c'est le caractère de délimitation de chemin le plus largement accepté.

##### Exemple

    // bons exemples
    #include <vector>
    #include <string>
    #include "util/util.h"

    // mauvais exemples
    #include <VECTOR>        // mauvais : la bibliothèque standard définit un en-tête identifié par <vector>, pas <VECTOR>
    #include <String>        // mauvais : la bibliothèque standard définit un en-tête identifié par <string>, pas <String>
    #include "Util/Util.H"   // mauvais : le fichier d'en-tête existe sur le système de fichiers sous "util/util.h"
    #include "util\util.h"   // mauvais : peut ne pas fonctionner si l'implémentation interprète `\u` comme une séquence d'échappement, ou si '\' n'est pas un séparateur de chemin valide

##### Application

Il n'est possible de l'appliquer que sur les implémentations où les identifiants d'en-têtes sont sensibles à la casse et qui ne prennent en charge que `/` comme séparateur de chemin de fichier.

### <a name="rs-namespace"></a>SF.20 : Utiliser des `namespace` pour exprimer la structure logique

##### Raison

???

##### Exemple

???

##### Application

???

### <a name="rs-unnamed"></a>SF.21 : Ne pas utiliser un espace de noms anonyme dans un fichier d'en-tête

##### Raison

Mentionner un espace de noms anonyme dans un fichier d'en-tête est presque toujours une erreur.

##### Exemple

    // fichier foo.h :
    namespace
    {
        const double x = 1.234;  // mauvais

        double foo(double y)     // mauvais
        {
            return y + x;
        }
    }

    namespace Foo
    {
        const double x = 1.234; // bon

        inline double foo(double y)        // bon
        {
            return y + x;
        }
    }

##### Application

* Signaler toute utilisation d'un espace de noms anonyme dans un fichier d'en-tête.

### <a name="rs-unnamed2"></a>SF.22 : Utiliser un espace de noms anonyme pour toutes les entités internes/non exportées

##### Raison

Rien d'externe ne peut dépendre d'une entité dans un espace de noms anonyme imbriqué.
Envisager de placer chaque définition dans un fichier source d'implémentation dans un espace de noms anonyme, sauf si elle définit une entité « externe/exportée ».

##### Exemple ; mauvais

    static int f();
    int g();
    static bool h();
    int k();

##### Exemple ; bon

    namespace {
        int f();
        bool h();
    }
    int g();
    int k();

##### Exemple

Une classe d'API et ses membres ne peuvent pas vivre dans un espace de noms anonyme ; mais toute classe ou fonction « d'aide » définie dans un fichier source d'implémentation devrait être dans le périmètre d'un espace de noms anonyme.

    ???

##### Application

* ???
