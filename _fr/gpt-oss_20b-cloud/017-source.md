# <a name="s-source"></a>SF: Fichiers source

Distinguish between declarations (used as interfaces) and definitions (used as implementations).  
Use header files to represent interfaces and to emphasize logical structure.

Source file rule summary:

* [SF.1: Utiliser une extension `.cpp` pour les fichiers de code et `.h` pour les fichiers d'interface si votre projet ne suit pas déjà une autre convention](017-source.md#rs-file-suffix)
* [SF.2: Un fichier d'en-tête ne doit pas contenir de définitions d'objets ou de fonctions non‑inline](017-source.md#rs-inline)
* [SF.3: Utiliser des fichiers d'en-tête pour toutes les déclarations utilisées dans plusieurs fichiers source](017-source.md#rs-declaration-header)
* [SF.4: Inclure les fichiers d'en-tête avant les autres déclarations dans un fichier](017-source.md#rs-include-order)
* [SF.5: Un fichier `.cpp` doit inclure le ou les fichiers d'en-tête qui définissent son interface](017-source.md#rs-consistency)
* [SF.6: Utiliser les directives `using namespace` pour la transition, pour les bibliothèques de base (telles que `std`), ou uniquement dans un scope local](017-source.md#rs-using)
* [SF.7: Ne pas écrire `using namespace` à l'échelle globale dans un fichier d'en-tête](017-source.md#rs-using-directive)
* [SF.8: Utiliser des garde‑fous `#include` pour tous les fichiers d'en-tête](017-source.md#rs-guards)
* [SF.9: Éviter les dépendances cycliques entre les fichiers source](017-source.md#rs-cycles)
* [SF.10: Éviter les dépendances sur les noms inclus implicitement](017-source.md#rs-implicit)
* [SF.11: Les fichiers d'en-tête doivent être autonomes](017-source.md#rs-contained)
* [SF.12: Préférer la forme citée de `#include` pour les fichiers relatifs au fichier qui les inclut et la forme aux chevrons partout ailleurs](017-source.md#rs-incform)
* [SF.13: Utiliser des identifiants d'en-tête portables dans les instructions `#include`](017-source.md#rs-portable-header-id)

* [SF.20: Utiliser les `namespace`s pour exprimer la structure logique](017-source.md#rs-namespace)
* [SF.21: Ne pas utiliser de namespace anonyme dans un fichier d'en-tête](017-source.md#rs-unnamed)
* [SF.22: Utiliser un namespace anonyme pour toutes les entités internes/non-exportées](017-source.md#rs-unnamed2)

### <a name="rs-file-suffix"></a>SF.1: Utiliser une extension `.cpp` pour les fichiers de code et `.h` pour les fichiers d'interface si votre projet ne suit pas déjà une autre convention

Voir [NL.27](024-naming.md#rl-file-suffix) @TODO-LINK

### <a name="rs-inline"></a>SF.2: Un fichier d'en-tête ne doit pas contenir de définitions d'objets ou de fonctions non‑inline

##### Raisons

Inclure des entités soumises à la règle de définition unique entraîne des erreurs de linkage.

##### Exemple

    // file.h:
    namespace Foo {
        int x = 7;
        int xx() { return x+x; }
    }

    // file1.cpp:
    #include <file.h>
    // ... more ...

     // file2.cpp:
    #include <file.h>
    // ... more ...

Lier `file1.cpp` et `file2.cpp` provoquera deux erreurs de linkage.

**Formulation alternative**: Un fichier d'en-tête ne doit contenir que:

* `#include`s d'autres fichiers d'en-tête (éventuellement avec des garde‑fous)
* templates
* class definitions
* function declarations
* `extern` declarations
* `inline` function definitions
* `constexpr` definitions
* `const` definitions
* `using` alias definitions
* ???

##### Application Vérifiez la liste positive ci‑dessus.

### <a name="rs-declaration-header"></a>SF.3: Utiliser des fichiers d'en-tête pour toutes les déclarations utilisées dans plusieurs fichiers source

##### Raisons

Maintenance. Lisibilité.

##### Exemple, mauvais

    // bar.cpp:
    void bar() { cout << "bar\n"; }

    // foo.cpp:
    extern void bar();
    void foo() { bar(); }

Un mainteneur de `bar` ne peut pas trouver toutes les déclarations de `bar` si son type doit être modifié. L'utilisateur de `bar` ne peut pas savoir si l'interface utilisée est complète et correcte. Au mieux, les messages d'erreur proviennent (tard) du linker.

##### Application

* Signaler les déclarations d'entités dans d'autres fichiers source qui ne sont pas placées dans un `.h`.

### <a name="rs-include-order"></a>SF.4: Inclure les fichiers d'en-tête avant les autres déclarations dans un fichier

##### Raisons

Minimiser les dépendances de contexte et améliorer la lisibilité.

##### Exemple

    #include <vector>
    #include <algorithm>
    #include <string>

    // ... my code here ...

##### Exemple, mauvais

    #include <vector>

    // ... my code here ...

    #include <algorithm>
    #include <string>

##### Note

Cela s'applique à la fois aux fichiers `.h` et aux fichiers `.cpp`.

##### Note

Un argument existe pour isoler le code des déclarations et des macros dans les fichiers d'en-tête en `#including` les en-têtes *après* le code que l'on souhaite protéger (comme dans l'exemple marqué "bad"). Cependant

* Cela ne fonctionne que pour un seul fichier (à un seul niveau) : utilisez cette technique dans un en-tête inclus par d'autres en-têtes et la vulnérabilité réapparaît.
* Un namespace (un “namespace de mise en œuvre”) peut protéger contre de nombreuses dépendances de contexte.
* La protection complète et la flexibilité nécessitent des modules.

**Voir également**:

* [Working Draft, Extensions to C++ for Modules](https://www.open-std.org/jtc1/sc22/wg21/docs/papers/2016/n4592.pdf)
* [Modules, Componentization, and Transition](https://www.open-std.org/jtc1/sc22/wg21/docs/papers/2016/p0141r0.pdf)

##### Application Facile

### <a name="rs-consistency"></a>SF.5: Un fichier `.cpp` doit inclure le ou les fichiers d'en-tête qui définissent son interface

##### Raisons

Cela permet au compilateur de faire une vérification de cohérence précoce.

##### Exemple, mauvais

    // foo.h:
    void foo(int);
    int bar(long);
    int foobar(int);

    // foo.cpp:
    void foo(int) { /* ... */ }
    int bar(double) { /* ... */ }
    double foobar(int);

Les erreurs ne seront pas détectées jusqu'au moment du lien pour un programme appelant `bar` ou `foobar`.

##### Exemple

    // foo.h:
    void foo(int);
    int bar(long);
    int foobar(int);

    // foo.cpp:
    #include "foo.h"

    void foo(int) { /* ... */ }
    int bar(double) { /* ... */ }
    double foobar(int);   // erreur : type de retour incorrect

L'erreur de type de retour pour `foobar` est désormais détectée immédiatement lorsque `foo.cpp` est compilé. L'erreur de type d'argument pour `bar` ne peut pas être détectée avant le lien à cause de la possibilité de surcharge, mais l'utilisation systématique des fichiers `.h` augmente la probabilité qu'elle soit détectée plus tôt par le programmeur.

##### Application ??? 

### <a name="rs-using"></a>SF.6: Utiliser les directives `using namespace` pour la transition, pour les bibliothèques de base (telles que `std`), ou uniquement dans un scope local

##### Raisons

`using namespace` peut entraîner des collisions de noms, il doit donc être utilisé avec parcimonie. Cependant, il n'est pas toujours possible de qualifier chaque nom provenant d'un namespace dans le code utilisateur (par exemple pendant une transition) et parfois un namespace est si fondamental et omniprésent dans une base de code qu'une qualification cohérente serait verbale et distrayante.

##### Exemple

    #include <string>
    #include <vector>
    #include <iostream>
    #include <memory>
    #include <algorithm>

    using namespace std;

    // ...

Ici, évidemment, la bibliothèque standard est utilisée de façon omniprésente et apparemment aucune autre bibliothèque n'est utilisée, donc exiger `std::` partout pourrait être distractif.

##### Exemple

L'utilisation de `using namespace std;` expose le programmeur à un conflit de noms avec un nom provenant de la bibliothèque standard

    #include <cmath>
    using namespace std;

    int g(int x)
    {
        int sqrt = 7;
        // ...
        return sqrt(x); // erreur
    }

Cependant, ceci n'est pas particulièrement susceptible d'entraîner une résolution qui ne soit pas une erreur et les personnes qui utilisent `using namespace std` sont censées connaître `std` et ce risque.

##### Note

Un fichier `.cpp` est une forme de scope local. Il y a peu de différence dans les opportunités de collision de noms dans un fichier `.cpp` de N lignes contenant un `using namespace X`, une fonction de N lignes contenant un `using namespace X`, et M fonctions contenant chacune un `using namespace X` avec un total de N lignes de code.

##### Note

[Ne pas écrire `using namespace` à l'échelle globale dans un fichier d'en-tête](017-source.md#rs-using-directive).

##### Application Signaler l'utilisation de `using namespace` à l'échelle globale dans un fichier d'en-tête.

### <a name="rs-guards"></a>SF.8: Utiliser des garde‑fous `#include` pour tous les fichiers d'en-tête

##### Raisons

Pour éviter que des fichiers soient `#include`s plusieurs fois.

Pour éviter les collisions de garde‑fous, ne nommez pas simplement le garde après le nom du fichier. Soyez sûr d'inclure également une clé et un bon différenciateur, tel que le nom de la bibliothèque ou du composant dont le fichier d'en-tête fait partie.

##### Exemple

    // file foobar.h:
    #ifndef LIBRARY_FOOBAR_H
    #define LIBRARY_FOOBAR_H
    // ... déclarations ...
    #endif // LIBRARY_FOOBAR_H

##### Application Signaler les fichiers `.h` sans garde‑fous `#include`.

##### Note

Certaines implémentations offrent des extensions du vendeur telles que `#pragma once` comme alternative aux garde‑fous. Ce n'est pas standard et ce n'est pas portable. Cela injecte la sémantique du système de fichiers de la machine hôte dans votre programme, en plus de vous enfermer à un vendeur. Notre recommandation est de rédiger en ISO C++: Voir [rule P.2](004-philosophy.md#rp-cplusplus).

### <a name="rs-cycles"></a>SF.9: Éviter les dépendances cycliques entre les fichiers source

##### Raisons

Les cycles compliquent la compréhension et ralentissent la compilation. Ils compliquent également la conversion à l'utilisation de modules du langage (lorsqu'ils deviennent disponibles).

##### Note

Éliminer les cycles ; ne les rompre pas simplement avec des garde‑fous `#include`.

##### Exemple, mauvais

    // file1.h:
    #include "file2.h"

    // file2.h:
    #include "file3.h"

    // file3.h:
    #include "file1.h"

##### Application Signaler tous les cycles.

### <a name="rs-implicit"></a>SF.10: Éviter les dépendances sur les noms inclus implicitement

##### Raisons

Éviter les surprises.  
Éviter d'avoir à changer les `#include`s si un `#include`d header change.  
Éviter d'être accidentellement dépendant des détails d'implémentation et des entités logiquement séparées incluses dans un header.

##### Exemple, mauvais

    #include <iostream>
    using namespace std;

    void use()
    {
        string s;
        cin >> s;               // fine
        getline(cin, s);        // erreur : getline() non défini
        if (s == "surprise") {  // erreur == non défini
            // ...
        }
    }

`<iostream>` expose la définition de `std::string` ("pourquoi ?" fait une question trivia), mais il n'est pas requis de le faire en incluant transitivement tout le header `<string>`, résultant en la fameuse question de débutant "pourquoi `getline(cin,s);` ne fonctionne pas?" ou même d'une question occasionnelle "`string`s ne peut pas être comparé avec `==`").

La solution est de faire explicitement `#include <string>`:

##### Exemple, bon

    #include <iostream>
    #include <string>
    using namespace std;

    void use()
    {
        string s;
        cin >> s;               // fine
        getline(cin, s);        // fine
        if (s == "surprise") {  // fine
            // ...
        }
    }

##### Note

Certains headers existent exactement pour agréger un ensemble de déclarations cohérentes provenant de divers headers. Par exemple:

    // basic_std_lib.h:

    #include <string>
    #include <map>
    #include <iostream>
    #include <random>
    #include <vector>

Un utilisateur peut désormais obtenir cet ensemble de déclarations avec un seul `#include`

    #include "basic_std_lib.h"

Cette règle contre l'inclusion implicite n'est pas destinée à prévenir de telles agrégations intentionnelles.

##### Application

### <a name="rs-contained"></a>SF.11: Les fichiers d'en-tête devraient être autonomes

##### Raisons

Usabilité. Les headers devraient être simples à utiliser et fonctionner lorsqu'ils sont inclus seuls. Les headers devraient encapsuler la fonctionnalité qu'ils fournissent. Éviter que les clients d'un header aient à gérer les dépendances de ce header.

##### Exemple

    #include "helpers.h"
    // helpers.h dépend de std::string et inclut <string>

##### Note

Ne pas suivre cette règle donne des erreurs difficiles à diagnostiquer pour les clients d'un header.

##### Note

Un header devrait inclure toutes ses dépendances. Faites attention à l'utilisation de chemins relatifs car les implémentations C++ divergent dans leur signification.

##### Application

Un test devrait vérifier que le header lui‑même se compile ou qu'un fichier `.cpp` qui inclut uniquement le header compile.

### <a name="rs-incform"></a>SF.12: Préférer la forme citée de `#include` pour les fichiers relatifs au fichier qui les inclut et la forme aux chevrons partout ailleurs

##### Raisons

La [standard](https://eel.is/c++draft/cpp.include) offre une flexibilité pour que les compilateurs puissent implémenter deux formes de `#include` choisies en utilisant l'angle (`<>`) ou la citation (`""`). Les vendeurs tirent profit de cela et utilisent des algorithmes de recherche et des méthodes différentes pour spécifier le chemin d'inclusion.

Néanmoins, les guidelines conseillent d'utiliser la forme citée pour inclure les fichiers qui se trouvent à un chemin relatif au fichier contenant la directive `#include` (dans le même composant ou projet) et d'utiliser la forme aux chevrons partout ailleurs, quand c'est possible. Cela encourage à être clair sur la localisation du fichier par rapport aux fichiers qui l'incluent, ou aux scénarios où un algorithme de recherche différent est requis. Cela rend facile de comprendre d'un coup d'œil s'il s'agit d'un header inclus depuis un fichier local relatif ou d'une bibliothèque standard ou d'un header d'une bibliothèque alternative.

##### Exemple

    // foo.cpp:
    #include <string>                // Depuis la bibliothèque standard, nécessite la forme <> 
    #include <some_library/common.h> // Un fichier qui n'est pas localement relatif, inclus depuis une autre bibliothèque ; utiliser la forme <> 
    #include "foo.h"                 // Un fichier localement relatif à foo.cpp dans le même projet, utiliser la forme "" 
    #include "util/util.h"           // Un fichier localement relatif à foo.cpp dans le même projet, utiliser la forme "" 
    #include <component_b/bar.h>     // Un fichier dans le même projet situé via un chemin de recherche, utiliser la forme <> 

##### Note

Ne pas suivre cette règle mène à des erreurs difficiles à diagnostiquer à cause de l'assemblage d'un mauvais fichier par une spécification incorrecte du scope lorsqu'il est inclus. Par exemple, dans un cas typique où l'algorithme `#include ""` chercherait un fichier à un chemin relatif local d'abord, puis utiliser cette forme pour désigner un fichier qui n'est pas localement relatif pourrait signifier que si un fichier vient à exister à ce chemin relatif (par ex. le fichier inclu est déplacé), il sera maintenant trouvé en priorité sur le fichier d'inclusion précédent et l'ensemble des includes sera modifié d'une manière inattendue.

Les créateurs de bibliothèques doivent mettre leurs headers dans un dossier et faire en sorte que les clients incluent ces fichiers en utilisant le chemin relatif `#include <some_library/common.h>`

##### Application

Un test devrait identifier si les headers référencés via `""` pourraient être référencés avec `<>`.

### <a name="rs-portable-header-id"></a>SF.13: Utiliser des identifiants d'en-tête portables dans les instructions `#include`

##### Raisons

La [standard](https://eel.is/c++draft/cpp.include) ne spécifie pas comment les compilateurs localisent de façon unique les headers à partir d'un identifiant dans une directive `#include`, ni ne précise ce qui constitue l'unicité. Par exemple, si l'implémentation considère les identifiants comme sensibles à la casse, ou si les identifiants sont des chemins de fichiers du système, et si oui, comment un chemin hiérarchique est délimité.

Pour maximiser la portabilité des directives `#include` entre les compilateurs, la guidance est de:

* utiliser la sensibilité à la casse pour l'identifiant d'en-tête, correspondant à la façon dont l'en-tête est défini par la standard, la spécification, l'implémentation, ou le fichier qui fournit l'en-tête.
* lorsque l'identifiant d'en-tête est un chemin hiérarchique, utiliser la barre oblique (``/``) pour délimiter les composants du chemin, car c'est le caractère de séparation de dossiers le plus largement accepté.

##### Exemple

    // good examples
    #include <vector>
    #include <string>
    #include "util/util.h"

    // bad examples
    #include <VECTOR>        // mauvais : la bibliothèque standard définit un header identifié comme <vector>, pas comme <VECTOR>
    #include <String>        // mauvais : la bibliothèque standard définit un header identifié comme <string>, pas comme <String>
    #include "Util/Util.H"   // mauvais : le fichier d'en-tête existe sur le système d'exploitation comme "util/util.h"
    #include "util\util.h"   // mauvais : peut ne pas fonctionner si l'implémentation interprète `\u` comme une séquence d'échappement, ou où `\` n'est pas un séparateur de chemin valide

##### Application

Il n'est possible d'appliquer que sur les implémentations où les identifiants d'en-tête sont sensibles à la casse et ne supportent que `/` comme séparateur de chemin de fichier.

### <a name="rs-namespace"></a>SF.20: Utiliser les `namespace`s pour exprimer la structure logique

##### Raisons

???

##### Exemple

    ???

##### Application

???

### <a name="rs-unnamed"></a>SF.21: Ne pas utiliser de namespace anonyme dans un fichier d'en-tête

##### Raisons

Il est presque toujours une erreur mentionner un namespace anonyme dans un fichier d'en-tête.

##### Exemple

    // file foo.h:
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

Signaler toute utilisation d'un namespace anonyme dans un fichier d'en-tête.

### <a name="rs-unnamed2"></a>SF.22: Utiliser un namespace anonyme pour toutes les entités internes/non-exportées

##### Raisons

Aucune entité externe ne peut dépendre d'une entité dans un namespace anonyme imbriqué.  
Considérez placer chaque définition dans un fichier source d'implémentation dans un namespace anonyme sauf si cela définit une entité « externe/exportée ».

##### Exemple, mauvais

    static int f();
    int g();
    static bool h();
    int k();

##### Exemple, bon

    namespace {
        int f();
        bool h();
    }
    int g();
    int k();

##### Exemple

Une classe d'API et ses membres ne peuvent pas vivre dans un namespace anonyme ; mais toute classe ou fonction « helper » définie dans un fichier source d'implémentation devrait se trouver dans le scope d'un namespace anonyme.

    ???

##### Application

* ???