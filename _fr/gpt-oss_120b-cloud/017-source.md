# <a name="s-source"></a>SF : Fichiers source

Distinguez les déclarations (utilisées comme interfaces) des définitions (utilisées comme implémentations).  
Utilisez les fichiers d’en‑tête pour représenter les interfaces et mettre en avant la structure logique.

**Résumé des règles relatives aux fichiers source :**

* [SF.1 : Utilisez l’extension `.cpp` pour les fichiers de code et `.h` pour les fichiers d’interface si votre projet ne suit pas déjà une autre convention](017-source.md#rs-file-suffix)
* [SF.2 : Un fichier d’en‑tête ne doit pas contenir de définitions d’objets ni de définitions de fonctions non‑inline](017-source.md#rs-inline)
* [SF.3 : Utilisez les fichiers d’en‑tête pour toutes les déclarations utilisées dans plusieurs fichiers source](017-source.md#rs-declaration-header)
* [SF.4 : Incluez les fichiers d’en‑tête avant les autres déclarations dans un fichier](017-source.md#rs-include-order)
* [SF.5 : Un fichier `.cpp` doit inclure le(s) fichier(s) d’en‑tête qui définissent son interface](017-source.md#rs-consistency)
* [SF.6 : Utilisez les directives `using namespace` pour la transition, pour les bibliothèques fondamentales (telles que `std`) ou uniquement à l’intérieur d’une portée locale](017-source.md#rs-using)
* [SF.7 : N’écrivez pas `using namespace` à l’échelle globale dans un fichier d’en‑tête](017-source.md#rs-using-directive)
* [SF.8 : Utilisez des garde‑fous `#include` pour tous les fichiers d’en‑tête](017-source.md#rs-guards)
* [SF.9 : Évitez les dépendances cycliques entre les fichiers source](017-source.md#rs-cycles)
* [SF.10 : Évitez les dépendances sur des noms inclus implicitement avec `#include`](017-source.md#rs-implicit)
* [SF.11 : Les fichiers d’en‑tête doivent être autonomes](017-source.md#rs-contained)
* [SF.12 : Privilégiez la forme entre guillemets de `#include` pour les fichiers relatifs au fichier incluant et la forme entre chevrons ailleurs](017-source.md#rs-incform)
* [SF.13 : Utilisez des identifiants d’en‑tête portables dans les directives `#include`](017-source.md#rs-portable-header-id)

* [SF.20 : Utilisez les `namespace`s pour exprimer la structure logique](017-source.md#rs-namespace)
* [SF.21 : N’utilisez pas d’espace de noms anonyme (unnamed namespace) dans un en‑tête](017-source.md#rs-unnamed)
* [SF.22 : Utilisez un espace de noms anonyme pour toutes les entités internes/non‑exportées](017-source.md#rs-unnamed2)

---

### <a name="rs-file-suffix"></a>SF.1 : Utilisez l’extension `.cpp` pour les fichiers de code et `.h` pour les fichiers d’interface si votre projet ne suit pas déjà une autre convention

Voir [NL.27](024-naming.md#rl-file-suffix)

---

### <a name="rs-inline"></a>SF.2 : Un fichier d’en‑tête ne doit pas contenir de définitions d’objets ni de définitions de fonctions non‑inline

##### Raison

Inclure des entités soumises à la règle de la définition unique entraîne des erreurs d’édition de liens.

##### Exemple

```cpp
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
```

Le lien de `file1.cpp` et `file2.cpp` produira deux erreurs d’édition de liens.

**Formulation alternative** :

* `#include`s d’autres fichiers d’en‑tête (éventuellement avec des garde‑fous)
* `templates`
* définitions de classes
* déclarations de fonctions
* déclarations `extern`
* définitions de fonctions `inline`
* définitions `constexpr`
* définitions `const`
* définitions d’alias `using`
* ???

##### Application

Vérifiez la liste positive ci‑dessus.

---

### <a name="rs-declaration-header"></a>SF.3 : Utilisez les fichiers d’en‑tête pour toutes les déclarations utilisées dans plusieurs fichiers source

##### Raison

Maintenabilité. Lisibilité.

##### Exemple, mauvais

```cpp
    // bar.cpp:
    void bar() { cout << "bar\n"; }

    // foo.cpp:
    extern void bar();
    void foo() { bar(); }
```

Un mainteneur de `bar` ne peut pas retrouver toutes les déclarations de `bar` si son type doit être modifié.  
L’utilisateur de `bar` ne peut pas savoir si l’interface utilisée est complète et correcte. Au mieux, les messages d’erreur proviennent (tardivement) du lienur.

##### Application

* Signaler les déclarations d’entités provenant d’autres fichiers source qui ne sont pas placées dans un fichier `.h`.

---

### <a name="rs-include-order"></a>SF.4 : Incluez les fichiers d’en‑tête avant les autres déclarations dans un fichier

##### Raison

Réduire les dépendances contextuelles et améliorer la lisibilité.

##### Exemple

```cpp
    #include <vector>
    #include <algorithm>
    #include <string>

    // ... my code here ...
```

##### Exemple, mauvais

```cpp
    #include <vector>

    // ... my code here ...

    #include <algorithm>
    #include <string>
```

##### Note

Cela s’applique aux fichiers `.h` et `.cpp`.

##### Note

Il existe un argument en faveur de l’isolation du code des déclarations et macro dans les fichiers d’en‑tête en incluant les en‑têtes *après* le code que l’on veut protéger (comme dans l’exemple « mauvais »). Cependant :

* cela ne fonctionne que pour un seul fichier (à un seul niveau) : si on utilise cette technique dans un en‑tête qui est inclus par d’autres en‑têtes, la vulnérabilité réapparaît.
* un espace de noms (un « namespace d’implémentation ») peut protéger contre de nombreuses dépendances contextuelles.
* une protection complète et une flexibilité nécessitent les modules.

**Voir aussi** :

* [Working Draft, Extensions to C++ for Modules](https://www.open-std.org/jtc1/sc22/wg21/docs/papers/2016/n4592.pdf)
* [Modules, Componentization, and Transition](https://www.open-std.org/jtc1/sc22/wg21/docs/papers/2016/p0141r0.pdf)

##### Application

Facile.

---

### <a name="rs-consistency"></a>SF.5 : Un fichier `.cpp` doit inclure le(s) fichier(s) d’en‑tête qui définissent son interface

##### Raison

Cela permet au compilateur d’effectuer une vérification de cohérence précoce.

##### Exemple, mauvais

```cpp
    // foo.h:
    void foo(int);
    int bar(long);
    int foobar(int);

    // foo.cpp:
    void foo(int) { /* ... */ }
    int bar(double) { /* ... */ }
    double foobar(int);
```

Les erreurs ne seront détectées qu’à l’étape d’édition de liens lorsqu’un programme appellera `bar` ou `foobar`.

##### Exemple

```cpp
    // foo.h:
    void foo(int);
    int bar(long);
    int foobar(int);

    // foo.cpp:
    #include "foo.h"

    void foo(int) { /* ... */ }
    int bar(double) { /* ... */ }
    double foobar(int);   // error: wrong return type
```

L’erreur de type de retour de `foobar` est maintenant détectée immédiatement lors de la compilation de `foo.cpp`.  
L’erreur de type d’argument de `bar` ne peut pas être détectée avant l’édition de liens à cause de la possibilité de surcharge, mais l’utilisation systématique de fichiers `.h` augmente la probabilité qu’elle soit repérée plus tôt par le programmeur.

##### Application

???

---

### <a name="rs-using"></a>SF.6 : Utilisez les directives `using namespace` pour la transition, pour les bibliothèques fondamentales (telles que `std`), ou uniquement à l’intérieur d’une portée locale

##### Raison

`using namespace` peut entraîner des collisions de noms, il doit donc être utilisé avec parcimonie.  
Cependant, il n’est pas toujours possible de qualifier chaque nom d’un espace de noms dans le code utilisateur (par ex., pendant une transition) et parfois un espace de noms est si fondamental et répandu dans une base de code que la qualification systématique serait verbeuse et distrayante.

##### Exemple

```cpp
    #include <string>
    #include <vector>
    #include <iostream>
    #include <memory>
    #include <algorithm>

    using namespace std;

    // ...
```

Évidemment, la bibliothèque standard est utilisée de manière pervasive et apparemment aucune autre bibliothèque n’est utilisée, donc exiger `std::` partout pourrait être distrayant.

##### Exemple

Le fait d’utiliser `using namespace std;` expose le programmeur à une collision de nom avec un nom de la bibliothèque standard :

```cpp
    #include <cmath>
    using namespace std;

    int g(int x)
    {
        int sqrt = 7;
        // ...
        return sqrt(x); // error
    }
```

Cependant, cela ne conduit pas particulièrement à une résolution qui ne serait pas une erreur, et les personnes qui utilisent `using namespace std` sont censées connaître `std` ainsi que ce risque.

##### Note

Un fichier `.cpp` constitue une forme de portée locale.  
Il y a peu de différence entre les possibilités de collisions de noms dans un `.cpp` contenant une directive `using namespace X` sur N lignes, une fonction N‑lignes contenant `using namespace X`, et M fonctions contenant chacune `using namespace X` avec N lignes de code au total.

##### Note

[Ne pas écrire `using namespace` à l’échelle globale dans un fichier d’en‑tête](017-source.md#rs-using-directive).

---

### <a name="rs-using-directive"></a>SF.7 : N’écrivez pas `using namespace` à l’échelle globale dans un fichier d’en‑tête

##### Raison

Le faire prive l’inclureur (`#include`ur) de la capacité à désambiguïser efficacement et à utiliser des alternatives. Cela rend également les en‑têtes `#include` dépendants de l’ordre d’inclusion, car ils peuvent avoir des significations différentes selon l’ordre.

##### Exemple

```cpp
    // bad.h
    #include <iostream>
    using namespace std; // bad

    // user.cpp
    #include "bad.h"

    bool copy(/*... some parameters ...*/);    // some function that happens to be named copy

    int main()
    {
        copy(/*...*/);    // now overloads local ::copy and std::copy, could be ambiguous
    }
```

##### Note

Une exception est `using namespace std::literals;`. Cette directive est nécessaire pour utiliser les littéraux de chaîne dans les en‑têtes et, conformément aux [règles](https://eel.is/c++draft/over.literal), les utilisateurs sont tenus de nommer leurs propres UDLs `operator""_x` ; ils ne rentreront donc pas en conflit avec la bibliothèque standard.

##### Application

Signaler toute utilisation de `using namespace` à l’échelle globale dans un fichier d’en‑tête.

---

### <a name="rs-guards"></a>SF.8 : Utilisez des garde‑fous `#include` pour tous les fichiers d’en‑tête

##### Raison

Afin d’éviter que les fichiers soient inclus plusieurs fois.

Pour éviter les collisions de garde‑fous, ne nommez pas simplement le garde‑fous d’après le nom du fichier. Assurez‑vous d’inclure également une clé et un différenciateur adéquat, comme le nom de la bibliothèque ou du composant auquel le fichier d’en‑tête appartient.

```cpp
    // file foobar.h:
    #ifndef LIBRARY_FOOBAR_H
    #define LIBRARY_FOOBAR_H
    // ... declarations ...
    #endif // LIBRARY_FOOBAR_H
```

##### Application

Signaler les fichiers `.h` dépourvus de garde‑fous `#include`.

##### Note

Certaines implémentations proposent des extensions propriétaires comme `#pragma once` en alternative aux garde‑fous. Ce n’est pas standard et ce n’est pas portable ; cela injecte les sémantiques du système de fichiers de la machine hôte dans votre programme, en plus de vous lier à un fournisseur.  
Notre recommandation est d’écrire en ISO C++ : voir [rule P.2](004-philosophy.md#rp-cplusplus).

---

### <a name="rs-cycles"></a>SF.9 : Évitez les dépendances cycliques entre les fichiers source

##### Raison

Les cycles compliquent la compréhension et ralentissent la compilation. Ils compliquent également la conversion vers l’utilisation de modules supportés par le langage (lorsqu’ils seront disponibles).

##### Note

Éliminez les cycles ; ne les résolvez pas simplement en ajoutant des garde‑fous `#include`.

##### Exemple, mauvais

```cpp
    // file1.h:
    #include "file2.h"

    // file2.h:
    #include "file3.h"

    // file3.h:
    #include "file1.h"
```

##### Application

Signaler tous les cycles.

---

### <a name="rs-implicit"></a>SF.10 : Évitez les dépendances sur des noms inclus implicitement avec `#include`

##### Raison

Évitez les surprises. Évitez d’avoir à modifier les `#include`s si un en‑tête inclus change. Évitez de devenir dépendant accidentellement des détails d’implémentation et des entités logiquement séparées incluses dans un en‑tête.

##### Exemple, mauvais

```cpp
    #include <iostream>
    using namespace std;

    void use()
    {
        string s;
        cin >> s;               // fine
        getline(cin, s);        // error: getline() not defined
        if (s == "surprise") {  // error == not defined
            // ...
        }
    }
```

`<iostream>` expose la définition de `std::string` (pourquoi ? Cela fait un bon sujet de curiosité), mais il n’est pas obligé de le faire en incluant transitivement l’en‑tête complet `<string>`, ce qui conduit à la question fréquente des débutants « pourquoi `getline(cin,s)` ne fonctionne‑t‑il pas ? » ou même à l’occasionnelle « les `string`s ne peuvent pas être comparés avec `==` ».

**Solution :** inclure explicitement `<string>` :

##### Exemple, bon

```cpp
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
```

##### Note

Certains en‑têtes existent exactement pour rassembler un ensemble cohérent de déclarations provenant d’une variété d’en‑têtes. Par exemple :

```cpp
    // basic_std_lib.h:

    #include <string>
    #include <map>
    #include <iostream>
    #include <random>
    #include <vector>
```

Un utilisateur peut maintenant obtenir cet ensemble de déclarations avec un seul `#include` :

```cpp
    #include "basic_std_lib.h"
```

Cette règle contre l’inclusion implicite n’est pas destinée à empêcher une agrégation délibérée.

##### Application

L’application de la règle nécessiterait de connaître quels éléments d’un en‑tête sont destinés à être « exportés » aux utilisateurs et quels sont là simplement pour permettre l’implémentation.  
Aucune vraie solution n’est possible tant que les modules ne sont pas disponibles.

---

### <a name="rs-contained"></a>SF.11 : Les fichiers d’en‑tête doivent être autonomes

##### Raison

Utilisabilité. Les en‑têtes doivent être simples à utiliser et fonctionner lorsqu’ils sont inclus seuls.  
Les en‑têtes doivent encapsuler la fonctionnalité qu’ils fournissent.  
Évitez que les clients d’un en‑tête aient à gérer les dépendances de cet en‑tête.

##### Exemple

```cpp
    #include "helpers.h"
    // helpers.h dépend de std::string et inclut <string>
```

##### Note

Ne pas respecter cela engendre des erreurs difficiles à diagnostiquer pour les clients d’un en‑tête.

##### Note

Un en‑tête doit inclure toutes ses dépendances. Soyez prudent avec l’utilisation de chemins relatifs, car les implémentations C++ diffèrent quant à leur signification.

##### Application

Un test doit vérifier que le fichier d’en‑tête compile seul ou qu’un fichier `.cpp` ne contenant que l’inclusion du fichier d’en‑tête compile.

---

### <a name="rs-incform"></a>SF.12 : Privilégiez la forme entre guillemets de `#include` pour les fichiers relatifs au fichier incluant et la forme entre chevrons dans les autres cas

##### Raison

La norme offre aux implémentations une flexibilité quant au choix entre la forme chevron (`<>`) ou guillemets (`""`). Les vendeurs exploitent cette liberté et utilisent différents algorithmes de recherche et méthodes pour spécifier le chemin d’inclusion.

Néanmoins, la recommandation est d’utiliser la forme entre guillemets pour inclure les fichiers qui existent à un chemin relatif par rapport au fichier contenant la directive `#include` (dans le même composant ou projet) et d’utiliser la forme entre chevrons dans tous les autres cas, si possible. Cette pratique rend explicite la localisation du fichier par rapport aux fichiers qui l’incluent et, le cas échéant, justifie l’utilisation d’un algorithme de recherche différent. Elle permet de voir d’un seul coup d’œil si un en‑tête provient d’un fichier local ou d’une bibliothèque standard/externes.

##### Exemple

```cpp
    // foo.cpp:
    #include <string>                // Depuis la bibliothèque standard, nécessite la forme <>
    #include <some_library/common.h> // Un fichier qui n’est pas localement relatif, inclus depuis une autre bibliothèque ; utilisez la forme <>
    #include "foo.h"                 // Un fichier localement relatif à foo.cpp dans le même projet, utilisez la forme ""
    #include "util/util.h"           // Un fichier localement relatif à foo.cpp dans le même projet, utilisez la forme ""
    #include <component_b/bar.h>     // Un fichier du même projet accessible via un chemin de recherche, utilisez la forme <>
```

##### Note

Ne pas suivre cette règle entraîne des erreurs difficiles à diagnostiquer, car on risque de récupérer le mauvais fichier en spécifiant mal le scope. Par exemple, l’algorithme de recherche pour `#include ""` recherche d’abord un fichier localement relatif ; l’utiliser pour un fichier qui n’est pas réellement local peut, si un fichier avec ce même nom apparaît plus tard à un chemin relatif (p. ex. parce que le fichier incluant a été déplacé), changer silencieusement l’ensemble des en‑têtes incluses.

Les créateurs de bibliothèques devraient placer leurs en‑têtes dans un dossier et demander aux clients de les inclure via le chemin relatif `#include <some_library/common.h>`.

##### Application

Un test doit identifier si les en‑têtes référencés via `""` pourraient être référencés avec `<>`.

---

### <a name="rs-portable-header-id"></a>SF.13 : Utilisez des identifiants d’en‑tête portables dans les directives `#include`

##### Raison

La norme ne spécifie pas comment les compilateurs localisent de façon unique les en‑têtes à partir d’un identifiant dans une directive `#include`, ni ce qui constitue l’unicité. Par exemple, on ne sait pas si l’implémentation considère les identifiants sensibles à la casse, ou si les identifiants sont des chemins de fichiers, et dans ce cas comment les composants d’un chemin hiérarchique sont délimités.

Pour maximiser la portabilité des directives `#include` entre compilateurs, il est recommandé :

* d’utiliser la casse exacte de l’identifiant (conforme à la façon dont le fichier d’en‑tête est défini par la norme, la spécification ou l’implémentation) ;
* lorsque l’identifiant d’en‑tête est un chemin de fichier hiérarchique, d’utiliser le slash `/` comme séparateur, car c’est le caractère le plus largement accepté.

##### Exemple

```cpp
    // bons exemples
    #include <vector>
    #include <string>
    #include "util/util.h"

    // mauvais exemples
    #include <VECTOR>        // mauvais : la bibliothèque standard définit un en‑tête identifié par <vector>, non <VECTOR>
    #include <String>        // mauvais : la bibliothèque standard définit un en‑tête identifié par <string>, non <String>
    #include "Util/Util.H"   // mauvais : le fichier d’en‑tête existe sur le système de fichiers sous le nom "util/util.h"
    #include "util\util.h"   // mauvais : peut ne pas fonctionner si l’implémentation interprète `\u` comme une séquence d’échappement, ou si '\' n’est pas un séparateur de chemin valide
```

##### Application

Il n’est possible de l’appliquer que sur les implémentations où les identifiants d’en‑tête sont sensibles à la casse et ne supportent que `/` comme séparateur de chemin.

---

### <a name="rs-namespace"></a>SF.20 : Utilisez les `namespace`s pour exprimer la structure logique

##### Raison

???

##### Exemple

???

##### Application

???

---

### <a name="rs-unnamed"></a>SF.21 : N’utilisez pas d’espace de noms anonyme (anonymous namespace) dans un en‑tête

##### Raison

Il s’agit quasi toujours d’un bug d’utiliser un espace de noms anonyme dans un fichier d’en‑tête.

##### Exemple

```cpp
    // file foo.h:
    namespace
    {
        const double x = 1.234;  // bad

        double foo(double y)     // bad
        {
            return y + x;
        }
    }

    namespace Foo
    {
        const double x = 1.234; // good

        inline double foo(double y)        // good
        {
            return y + x;
        }
    }
```

##### Application

* Signaler tout usage d’un espace de noms anonyme dans un fichier d’en‑tête.

---

### <a name="rs-unnamed2"></a>SF.22 : Utilisez un espace de noms anonyme pour toutes les entités internes/non exportées

##### Raison

Aucune entité externe ne peut dépendre d’un élément placé dans un espace de noms anonyme imbriqué.  
Considérez de placer chaque définition dans un fichier source d’implémentation dans un espace de noms anonyme, sauf si cette définition correspond à une entité « externe/exportée ».

##### Exemple, mauvais

```cpp
    static int f();
    int g();
    static bool h();
    int k();
```

##### Exemple, bon

```cpp
    namespace {
        int f();
        bool h();
    }
    int g();
    int k();
```

##### Exemple

Une classe d’API et ses membres ne peuvent pas vivre dans un espace de noms anonyme ; mais toute classe ou fonction « helper » définie dans un fichier source d’implémentation devrait se trouver dans un espace de noms anonyme.

```cpp
    ???
```

##### Application

* ???