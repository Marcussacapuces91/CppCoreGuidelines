# <a name="s-source"></a>SF : Fichiers sources

Faire la distinction entre les déclarations (utilisées comme interfaces) et les définitions (utilisées comme implémentations).

Utiliser les fichiers d'en-tête pour représenter les interfaces et souligner la structure logique.

Résumé des règles concernant les fichiers source :

* [SF.1: Utiliser l'extension .cpp pour les fichiers de code et .h pour les fichiers d'interface si votre projet ne suit pas déjà une autre convention](#rs-file-suffix)
* [SF.2: Un fichier d'en-tête ne doit pas contenir de définitions d'objets ou de définitions de fonctions non inline](#rs-inline)
* [SF.3: Utiliser les fichiers d'en-tête pour toutes les déclarations utilisées dans plusieurs fichiers source](#rs-declaration-header)
* [SF.4: Inclure les fichiers d'en-tête avant les autres déclarations d'un fichier](#rs-include-order)
* [SF.5: Un fichier .cpp doit inclure le(s) fichier(s) d'en-tête qui définissent son interface](#rs-consistency)
* [SF.6: Utiliser les directives `using namespace` pour la transition, les bibliothèques de base (telles que `std`) ou dans un scope local uniquement](#rs-using)
* [SF.7: Ne pas écrire `using namespace` au niveau global dans un fichier d'en-tête](#rs-using-directive)
* [SF.8: Utiliser les guards `#include` pour tous les fichiers d'en-tête](#rs-guards)
* [SF.9: Éviter les dépendances cycliques entre les fichiers source](#rs-cycles)
* [SF.10: Éviter les dépendances sur les noms implicitement `#include`d](#rs-implicit)
* [SF.11: Les fichiers d'en-tête doivent être auto-contenus](#rs-contained)
* [SF.12: Préférer la forme citée de `#include` pour les fichiers relatifs au fichier incluant et la forme d'accolade partout ailleurs](#rs-incform)
* [SF.13: Utiliser des identifiants de header portables dans les directives `#include`](#rs-portable-header-id)

* [SF.20: Utiliser les `namespace` pour exprimer la structure logique](#rs-namespace)
* [SF.21: Ne pas utiliser un namespace anonyme (sans nom) dans un fichier d'en-tête](#rs-unnamed)
* [SF.22: Utiliser un namespace anonyme (sans nom) pour toutes les entités internes/non exportées](#rs-unnamed2)

### <a name="rs-file-suffix"></a>SF.1 : Utiliser l'extension `.cpp` pour les fichiers de code et `.h` pour les fichiers d'interface si votre projet ne suit pas déjà une autre convention

Voir [NL.27](#rl-file-suffix) @TODO-LINK

### <a name="rs-inline"></a>SF.2 : Un fichier d'en-tête ne doit pas contenir de définitions d'objets ou de définitions de fonctions non inline

##### Raison

Inclure des entités soumises à la règle de définition unique entraîne des erreurs de liaison.

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

Le lien entre `file1.cpp` et `file2.cpp` produira deux erreurs de liaison.

**Formulation alternative** : un fichier d'en-tête ne doit contenir que :

* `#include`s d'autres fichiers d'en-tête (possiblement avec des guards d'inclusion)
* modèles
* définitions de classe
* déclarations de fonction
* déclarations `extern`
* définitions de fonction `inline`
* définitions `constexpr`
* définitions `const`
* définitions d'alias `using`
* ???

##### Application

Vérifier la liste positive ci‑dessous.

### <a name="rs-declaration-header"></a>SF.3 : Utiliser les fichiers d'en-tête pour toutes les déclarations utilisées dans plusieurs fichiers source

##### Raison

Maintenabilité. Lisibilité.

##### Exemple, mauvais

    // bar.cpp:
    void bar() { cout << "bar\n"; }

    // foo.cpp:
    extern void bar();
    void foo() { bar(); }

Un mainteneur de `bar` ne peut pas trouver toutes les déclarations de `bar` si son type doit changer.  
L'utilisateur de `bar` ne peut pas savoir si l'interface utilisée est complète et correcte. Au mieux, les messages d'erreur proviennent (retard) du linker.

##### Application

* Signaler les déclarations d'entités dans d'autres fichiers source qui ne sont pas placées dans un `.h`.

### <a name="rs-include-order"></a>SF.4 : Inclure les fichiers d'en-tête avant les autres déclarations dans un fichier

##### Raison

Minimiser les dépendances de contexte et augmenter la lisibilité.

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

Cette règle s'applique tant aux fichiers `.h` qu'aux fichiers `.cpp`.

##### Note

On peut insulter le code des déclarations et des macros dans les fichiers d'en-tête en `#including` les fichiers *après* le code à protéger (comme dans l'exemple « mauvais »). Cependant

* ça ne fonctionne que pour un seul fichier (à un seul niveau) : l'utiliser dans un header inclus avec d'autres headers et la vulnérabilité réapparaît.
* un namespace (un "namespace d'implémentation") peut protéger contre de nombreuses dépendances de contexte.
* une protection complète et une flexibilité nécessitent des modules.

**Voir aussi** :

* [Working Draft, Extensions to C++ for Modules](https://www.open-std.org/jtc1/sc22/wg21/docs/papers/2016/n4592.pdf)
* [Modules, Componentization, and Transition](https://www.open-std.org/jtc1/sc22/wg21/docs/papers/2016/p0141r0.pdf)

##### Application

Facile.

### <a name="rs-consistency"></a>SF.5 : Un fichier `.cpp` doit inclure le(s) fichier(s) d'en-tête qui définissent son interface

##### Raison

Cela permet au compilateur de faire une vérification cohérente précoce.

##### Exemple, mauvais

    // foo.h:
    void foo(int);
    int bar(long);
    int foobar(int);

    // foo.cpp:
    void foo(int) { /* ... */ }
    int bar(double) { /* ... */ }
    double foobar(int);

Les erreurs ne seront pas détectées avant le moment de liaison pour un programme appelant `bar` ou `foobar`.

##### Exemple

    // foo.h:
    void foobar(int);

    // foo.cpp:
    #include "foo.h"

    void foo(int) { /* ... */ }
    int bar(double) { /* ... */ }
    double foobar(int);   // erreur : type de retour incorrect

L'erreur de type de retour pour `foobar` est désormais détectée immédiatement lors de la compilation de `foo.cpp`.  
L'erreur de type d'argument pour `bar` ne peut être détectée qu'au moment de la liaison à cause de la possibilité de surcharge, mais l'utilisation systématique des fichiers `.h` augmente la probabilité qu'elle soit détectée plus tôt par le programmeur.

##### Application

???

### <a name="rs-using"></a>SF.6 : Utiliser les directives `using namespace` pour la transition, les bibliothèques de base (telles que `std`) ou dans un scope local uniquement

##### Raison

`using namespace` peut conduire à des conflits de noms, il faut donc l'utiliser avec parcimonie.  
Cependant, il n'est pas toujours possible de qualifier chaque nom provenant d'un namespace dans le code utilisateur (ex. pendant la transition) et parfois un namespace est si fondamental et si présent dans une base de code que la qualification cohérente serait verbeuse et distrayante.

##### Exemple

    #include <string>
    #include <vector>
    #include <iostream>
    #include <memory>
    #include <algorithm>

    // ...

Ici (évidemment), la bibliothèque standard est utilisée de façon omniprésente et aucune autre bibliothèque n'est utilisée, donc exiger `std::` partout pourrait être distrayant.

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

Cependant, il n'est pas particulièrement probable que cela mène à une résolution qui ne soit pas une erreur et les personnes qui utilisent `using namespace std` sont censées connaître `std` et ce risque.

##### Note

Un fichier `.cpp` est une forme d'espace de portée local.  
Il n'y a pas de différence notable entre les opportunités de conflits de noms dans un fichier `.cpp` de N lignes contenant un `using namespace X`, une fonction de N lignes contenant un `using namespace X`, et M fonctions chacune contenant un `using namespace X` avec N lignes de code au total.

##### Note

[Ne pas écrire `using namespace` au niveau global dans un fichier d'en-tête](#rs-using-directive).

### <a name="rs-using-directive"></a>SF.7 : Ne pas écrire `using namespace` au niveau global dans un fichier d'en-tête

##### Raison

Le faire enlève la capacité de l'`#include` à disambiguïser efficacement et à utiliser des alternatives. Il rend également les headers `#include` dépendants de l'ordre, car ils peuvent avoir une signification différente selon l'ordre d'inclusion.

##### Exemple

    // bad.h
    #include <iostream>
    using namespace std; // mauvais

    // user.cpp
    #include "bad.h"

    bool copy(/*... some parameters ...*/);    // fonc. qui s'appelle copy

    int main()
    {
        copy(/*...*/);    // maintenant surcharge de ::copy local et std::copy, pourrait être ambigu
    }

##### Note

Une exception est `using namespace std::literals;`. Cela est nécessaire pour utiliser les littéraux de chaîne dans les fichiers d'en-tête et, compte tenu des [règles](https://eel.is/c++draft/over.literal) - les utilisateurs sont tenus de nommer leurs propres UDLs `operator""_x` - ils ne colliderez pas avec la bibliothèque standard.

##### Application

Marquer `using namespace` au niveau global dans un fichier d'en-tête.

### <a name="rs-guards"></a>SF.8 : Utiliser les guards `#include` pour tous les fichiers d'en-tête

##### Raison

Pour éviter que les fichiers soient `#include` plusieurs fois.

Dans le but d'éviter les collisions de guards d'inclusion, ne nommez pas simplement le guard après le nom du fichier. Incluez toujours une clé et un différenciateur pertinent, tel que le nom de la bibliothèque ou du composant dont fait partie le fichier d'en-tête.

##### Exemple

    // file foobar.h:
    #ifndef LIBRARY_FOOBAR_H
    #define LIBRARY_FOOBAR_H
    // ... declarations ...
    #endif // LIBRARY_FOOBAR_H

##### Application

Marquer les fichiers `.h` sans guards `#include`.

##### Note

Certaines implémentations offrent des extensions de fournisseurs comme `#pragma once` comme alternative aux guards d'inclusion. Ce n'est pas standard et n'est pas portable.  Il injecte la sémantique du système de fichiers de la machine hôte dans votre programme, en plus de vous verrouiller à un fournisseur.  
Notre recommandation est d'écrire en ISO C++ : Voir [rule P.2](#rp-cplusplus) @TODO-LINK

### <a name="rs-cycles"></a>SF.9 : Éviter les dépendances cycliques entre les fichiers source

##### Raison

Les cycles compliquent la compréhension et ralentissent la compilation. Ils compliquent également la conversion vers des modules pris en charge par le langage (lorsqu'ils deviennent disponibles).

##### Note

Éliminer les cycles ; ne pas les rompre simplement avec des guards d'inclusion.

##### Exemple, mauvais

    // file1.h:
    #include "file2.h"

    // file2.h:
    #include "file3.h"

    // file3.h:
    #include "file1.h"

##### Application

Signaler tous les cycles.

### <a name="rs-implicit"></a>SF.10 : Éviter les dépendances sur les noms implicitement `#include`d

##### Raison

Éviter les surprises.  
Éviter d'avoir à changer les `#include` si un header `#include`d change.  
Éviter de devenir accidentellement dépendant des détails d'implémentation et des entités logiquement séparées incluses dans un header.

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

`<iostream>` expose la définition de `std::string` ("pourquoi ?" rend une question trivia), mais elle n'est pas exigée d'être transitive via `<string>`.

La solution consiste à inclure explicitement `<string>` :

##### Exemple, bon

    #include <iostream>
    #include <string>
    using namespace std;

    void use

