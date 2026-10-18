# <a name="s-interfaces"></a>I : Interfaces

Une interface est un contrat entre deux parties d'un programme. Préciser exactement ce qui est attendu d'un fournisseur de service et d'un utilisateur de ce service est essentiel.
Avoir de bonnes interfaces (faciles à comprendre, encourageant une utilisation efficace, sans erreur, favorisant les tests, etc.) est probablement l'aspect le plus important de l'organisation du code.

Résumé des règles d'interface:

* [I.1 : Faire explicites les interfaces](005-interfaces.md#ri-explicit)
* [I.2 : Éviter les variables globales non‑`const`](005-interfaces.md#ri-global)
* [I.3 : Éviter les singletons](005-interfaces.md#ri-singleton)
* [I.4 : Faire les interfaces précisément et fortement typées](005-interfaces.md#ri-typed)
* [I.5 : Préciser les préconditions (le cas échéant)](005-interfaces.md#ri-pre)
* [I.6 : Préférer `Expects()` pour exprimer les préconditions](005-interfaces.md#ri-expects)
* [I.7 : Préciser les postconditions](005-interfaces.md#ri-post)
* [I.8 : Préférer `Ensures()` pour exprimer les postconditions](005-interfaces.md#ri-ensures)
* [I.9 : Si une interface est un modèle, documenter ses paramètres à l'aide de concepts](005-interfaces.md#ri-concepts)
* [I.10 : Utiliser des exceptions pour signaler un échec de réalisation d'une tâche requise](005-interfaces.md#ri-except)
* [I.11 : Ne jamais transférer la propriété par un pointeur brut (`T*`) ou une référence (`T&`)](005-interfaces.md#ri-raw)
* [I.12 : Déclarer un pointeur qui ne doit pas être nul comme `not_null`](005-interfaces.md#ri-nullptr)
* [I.13 : Ne pas passer un tableau comme un seul pointeur](005-interfaces.md#ri-array)
* [I.22 : Éviter une initialisation complexe des objets globaux](005-interfaces.md#ri-global-init)
* [I.23 : Limiter le nombre d'arguments d'une fonction](005-interfaces.md#ri-nargs)
* [I.24 : Éviter les paramètres adjacents qui peuvent être invoqués par les mêmes arguments dans n'importe quel ordre avec des significations différentes](005-interfaces.md#ri-unrelated)
* [I.25 : Préférer les classes abstraites vides comme interfaces aux hiérarchies de classes](005-interfaces.md#ri-abstract)
* [I.26 : Si vous voulez une ABI cross‑compilatrice, utilisez un sous‑ensemble C‑style](005-interfaces.md#ri-abi)
* [I.27 : Pour une ABI stable de bibliothèque, envisagez l'idiome Pimpl](005-interfaces.md#ri-pimpl)
* [I.30 : Encapsuler les violations de règle](005-interfaces.md#ri-encapsulate)

**Voir aussi**:

* [F : Fonctions](006-functions.md)
* [C.concrete : Types concrets](007-class.md#ss-concrete)
* [C.hier : Hiérarchies de classes](007-class.md#ss-hier)
* [C.over : Surcharge et opérateurs surchargés](007-class.md#ss-overload)
* [C.con : Conteneurs et autres gestionnaires de ressources](007-class.md#ss-containers)
* [E : Gestion d'erreurs](013-errors.md)
* [T : Modèles et programmation générique](015-templates.md)

### <a name="ri-explicit"></a>I.1 : Faire explicites les interfaces

##### Raison

Exactitude. Les hypothèses non précisées dans une interface sont facilement négligées et difficiles à tester.

##### Exemple, mauvais

Contrôler le comportement d'une fonction à travers une variable globale (à l'échelle du namespace) (mode d'appel) est implicite et potentiellement déroutant. Par exemple :

    int round(double d)
    {
        return (round_up) ? ceil(d) : d;    // don't: "invisible" dependency
    }

Il ne sera pas évident pour l'appelant que la signification de deux appels à `round(7.2)` pourrait donner des résultats différents.

##### Exception

Parfois, nous contrôlons les détails d'un ensemble d'opérations à l'aide d'une variable d'environnement, par exemple sortie normale vs. détaillée ou mode débogage vs. optimisé.
L'utilisation d'un contrôle non local est potentiellement déroutante, mais ne contrôle que les détails d'implémentation d'une sémantique autrement fixe.

##### Exemple, mauvais

Rapporter via des variables non locales (p. ex. `errno`) est facilement ignoré. Par exemple :

    // don't: no test of fprintf's return value
    fprintf(connection, "logging: %d %d %d\n", x, y, s);

Que se passe-t-il si la connexion tombe afin qu'aucune sortie de journalisation ne soit produite ? Voir I.???.
@TODO-LINK

**Alternative** : Lancer une exception. Une exception ne peut pas être ignorée.

**Alternative de formulation** : Éviter de passer des informations à travers une interface via un état non local ou implicite.

Notez que les fonctions membres non‑`const` passent des informations à d'autres fonctions membres via l'état de l'objet.

**Alternative de formulation** : Une interface doit être une fonction ou un ensemble de fonctions.
Les fonctions peuvent être des modèles de fonctions et les ensembles de fonctions peuvent être des classes ou des modèles de classes.

##### Application

* (Simple) Une fonction ne doit pas prendre de décisions de flux de contrôle basées sur les valeurs de variables déclarées à l'échelle du namespace.
* (Simple) Une fonction ne doit pas écrire dans des variables déclarées à l'échelle du namespace.

### <a name="ri-global"></a>I.2 : Éviter les variables globales non‑`const`

##### Raison

Les variables globales non‑`const` dissimulent les dépendances et les rendent sujettes à des changements imprévisibles.

##### Exemple

    struct Data {
        // ... lots of stuff ...
    } data;            // non-const data

    void compute()     // don't
    {
        // ... use data ...
    }

    void output()     // don't
    {
        // ... use data ...
    }

Qui d'autre pourrait modifier `data` ?

**Avertissement** : L'initialisation des objets globaux n'est pas totalement ordonnée.
Si vous utilisez un objet global, initialisez-le avec une constante.
Notez qu'il est possible d'obtenir un ordre d'initialisation indéfini même pour les objets `const`.

##### Exception

Un objet global est souvent meilleur qu'un singleton.

##### Remarque

Les constantes globales sont utiles.

##### Remarque

La règle contre les variables globales s'applique également aux variables à l'échelle du namespace.

**Alternative** : Si vous utilisez des données mondiales (plus généralement à l'échelle du namespace) pour éviter la copie, envisagez de passer les données en tant qu'objet en référence à `const`.
Une autre solution consiste à définir les données comme l'état d'un objet et les opérations comme fonctions membres.

**Avertissement** : Attention aux conditions de concurrence : si un thread peut accéder à des données non locales (ou des données passées par référence) tandis qu'un autre thread exécute le callee, on peut avoir une condition de concurrence.
Tout pointeur ou référence vers des données modifiables est une condition de concurrence potentielle.

Utiliser des pointeurs ou références globaux pour accéder et modifier des données non‑`const`, et autrement non‑globales, n'est pas une meilleure alternative aux variables globales non‑`const` car cela ne résout pas les problèmes de dépendances cachées ni les éventuelles conditions de concurrence.

##### Remarque

Il ne peut pas y avoir de condition de concurrence sur des données immuables.

**Références** : Voir les [règles d'appel des fonctions](006-functions.md#ss-call).

##### Remarque

La règle est « éviter », pas « ne pas utiliser ». Bien sûr, il y aura (rare) des exceptions, comme `cin`, `cout` et `cerr`.

##### Application

*(Simple) Signaler toutes les variables non‑`const` déclarées à l'échelle du namespace et les pointeurs/références globaux vers des données non‑`const`.*

### <a name="ri-singleton"></a>I.3 : Éviter les singletons

##### Raison

Les singletons sont essentiellement des objets globaux compliqués déguisés.

##### Exemple

    class Singleton {
        // ... lots of stuff to ensure that only one Singleton object is created,
        // that it is initialized properly, etc.
    };

Il existe de nombreuses variantes de cette idée de singleton. Couchage de l'éditeur.

##### Remarque

Si vous ne souhaitez pas qu'un objet global change, déclarez-le `const` ou `constexpr`.

##### Exception

Vous pouvez utiliser le « singleton » le plus simple (s'il est si simple qu'il n'est souvent pas considéré comme un singleton) pour obtenir une initialisation à la première utilisation, s'il en existe une :

    X& myX()
    {
        static X my_x {3};
        return my_x;
    }

C'est l'une des solutions les plus efficaces aux problèmes liés à l'ordre d'initialisation.

Dans un environnement multi‑thread, l'initialisation d'un objet statique ne provoque pas de condition de concurrence
(sauf si vous accédez imprudemment à un objet partagé depuis son constructeur).

Notez que l'initialisation d'un `static` local n'implique pas une condition de concurrence.
Cependant, si la destruction de `X` implique une opération qui doit être synchronisée, nous devons utiliser une solution moins simple.

    X& myX()
    {
        static auto p = new X {3};
        return *p;  // potential leak
    }

Maintenant, quelqu'un doit `delete` cet objet d'une manière thread‑safe appropriée.
C'est source d'erreur, alors nous n'utilisons pas cette technique à moins que :

* `myX` se trouve dans du code multi‑thread,
* l'objet `X` doit être détruit (par ex. parce qu'il libère une ressource), et
* le code du destructeur de `X` doit être synchronisé.

Si vous, comme beaucoup, définissez un singleton comme une classe pour laquelle n'est créé qu'un seul objet, les fonctions comme `myX` ne sont pas des singletons, et cette technique utile n'est pas une exception à la règle d'absence de singleton.

##### Application

Très difficile en général.

* Rechercher les classes dont les noms incluent « singleton ».
* Rechercher les classes pour lesquelles ne est créé qu'un seul objet (en comptant les objets ou en examinant les constructeurs).
* Si une classe X possède une fonction statique publique qui contient un `static` local de type X et retourne un pointeur ou une référence vers celui‑ci, interdire cela.

### <a name="ri-typed"></a>I.4 : Faire les interfaces précisément et fortement typées

##### Raison

Les types sont la documentation la plus simple et la meilleure, améliorent la lisibilité grâce à leur signification bien définie et sont vérifiés à la compilation.
De plus, le code précisément typé est souvent mieux optimisé.

##### Exemple, mauvais

Considérez :

    void pass(void* data);    // weak and under-qualified type void* is suspicious

Les appelants ne savent pas quels types sont autorisés et si la donnée peut être modifiée alors que `const` n'est pas spécifié.
Notez que tous les types de pointeurs se convertissent implicitement vers `void*`, ce qui rend facile pour les appelants de fournir cette valeur.

Le callee doit `static_cast` la donnée vers un type non vérifié pour l'utiliser.
Cela est source d'erreurs et verbeux.

Seul `const void*` est à utiliser pour passer des données dans des conceptions indécrites en C++.
Considérez l'utilisation d'un `variant` ou d'un pointeur vers une base à la place.

**Alternative** : Souvent, un paramètre de modèle peut éliminer le `void*` et le transformer en `T*` ou `T&`. Pour un code générique, ces `T` peuvent être généraux ou des paramètres de modèle restreints par concept.

##### Exemple, mauvais

Considérez :

    draw_rect(100, 200, 100, 500); // what do the numbers specify?
    draw_rect(p.x, p.y, 10, 20); // what units are 10 and 20 in?

Il est clair que l'appelant décrit un rectangle, mais il n'est pas clair quelles parties il désigne.
De plus, un `int` peut porter des formes arbitraires d'information, y compris des valeurs de nombreuses unités, il faut donc deviner la signification des quatre `int`.
Probablement, les deux premiers constituent un couple (`x`,`y`) de coordonnées, mais que sont les deux derniers ?

Les commentaires et les noms des paramètres peuvent aider, mais l'on pourrait être explicite :

    void draw_rectangle(Point top_left, Point bottom_right);
    void draw_rectangle(Point top_left, Size height_width);

    draw_rectangle(p, Point{10, 20});  // two corners
    draw_rectangle(p, Size{10, 20});   // one corner and a (height, width) pair

Évidemment, on ne peut pas capturer toutes les erreurs par le système de type statique
(p. ex. le fait qu'un premier argument soit censé être un point haut‑gauche reste à la convention (nommage et commentaires).

##### Exemple, mauvais

Considérez :

    set_settings(true, false, 42); // what do the numbers specify?

Les types de paramètres et leurs valeurs ne communiquent pas quels réglages sont définis ou ce que signifient ces valeurs.

Cette conception est plus explicite, sûre et lisible :

    alarm_settings s{};
    s.enabled = true;
    s.displayMode = alarm_settings::mode::spinning_light;
    s.frequency = alarm_settings::every_10_seconds;
    set_settings(s);

Pour le cas d'un ensemble de valeurs booléennes, envisagez d'utiliser un `enum` de drapeaux ; un patron qui exprime un ensemble de valeurs booléennes.

    enable_lamp_options(lamp_option::on | lamp_option::animate_state_transitions);

##### Exemple, mauvais

Dans l'exemple suivant, il n'est pas clair d'après l'interface ce que signifie `time_to_blink` : secondes ? millisecondes ?

    void blink_led(int time_to_blink) // bad -- the unit is ambiguous
    {
        // ...
        // do something with time_to_blink
        // ...
    }

    void use()
    {
        blink_led(2);
    }

##### Exemple, bon

Les types `std::chrono::duration` aident à rendre explicite l'unité de durée.

    void blink_led(milliseconds time_to_blink) // good -- the unit is explicit
    {
        // ...
        // do something with time_to_blink
        // ...
    }

    void use()
    {
        blink_led(1500ms);
    }

La fonction peut aussi être écrite de façon à accepter toute unité de durée.

    template<class rep, class period>
    void blink_led(duration<rep, period> time_to_blink) // good -- accepts any unit
    {
        // assuming that millisecond is the smallest relevant unit
        auto milliseconds_to_blink = duration_cast<milliseconds>(time_to_blink);
        // ...
        // do something with milliseconds_to_blink
        // ...
    }

    void use()
    {
        blink_led(2s);
        blink_led(1500ms);
    }

##### Application

* (Simple) Signaler l'utilisation de `void*` comme paramètre ou type de retour.
* (Simple) Signaler l'utilisation de plus d'un paramètre booléen.
* (Difficile à bien faire) Chercher les fonctions qui utilisent trop d'arguments de type primitif.

### <a name="ri-pre"></a>I.5 : Préciser les préconditions (le cas échéant)

##### Raison

Les arguments ont une signification qui peut contraindre leur utilisation correcte par le callee.

##### Exemple

Considérez :

    double sqrt(double x);

Ici `x` doit être positif ou nul. Le système de type ne peut pas (facilement et naturellement) exprimer cela, donc nous devons utiliser d'autres moyens. Par exemple :

    double sqrt(double x); // x must be non-negative

Certaines préconditions peuvent être exprimées par des assertions. Par exemple :

    double sqrt(double x) { Expects(x >= 0); /* ... */ }

Idéalement, ce `Expects(x >= 0)` devrait faire partie de l'interface de `sqrt()` mais ce n'est pas facilement réalisable. Pour l'instant, on le place dans la définition (corps de fonction).

**Références** : `Expects()` est décrit dans [GSL (Guidelines Support Library)](#gsl-guidelines-support-library).

##### Remarque

Préférer une spécification formelle des exigences, telle que `Expects(p);`.
Si c'est infructueux, utiliser du texte en anglais dans les commentaires, tel que `// the sequence [p:q) is ordered using <`.

##### Remarque

La plupart des fonctions membres ont comme précondition qu'un certain invariant de classe est maintenu.
Cet invariant est établi par un constructeur et doit être rétabli à la sortie par chaque fonction membre appelée depuis l'extérieur de la classe.
Nous n'avons pas besoin de le mentionner pour chaque fonction membre.

##### Application

(N'agréable)

**Voir les règles d'appel des fonctions**.

### <a name="ri-expects"></a>I.6 : Préférer `Expects()` pour exprimer les préconditions

##### Raison

Pour clarifier que la condition est une précondition et permettre l'utilisation d'outils.

##### Exemple

    int area(int height, int width)
    {
        Expects(height > 0 && width > 0);            // good
        if (height <= 0 || width <= 0) my_error();   // obscure
        // ...
    }

##### Remarque

Les préconditions peuvent être exprimées de nombreuses manières, y compris les commentaires, les déclarations `if` et `assert()`.
Cela peut les rendre difficiles à distinguer du code ordinaire, difficiles à mettre à jour, difficiles à manipuler par des outils, et peut avoir la mauvaise sémantique (voulez‑vous toujours aborter en mode debug et ne rien vérifier en production ?).

##### Remarque

Les préconditions doivent faire partie de l'interface plutôt que de l'implémentation.
Mais nous n'avons pas encore les facilités linguistiques pour cela.
Lorsque le soutien linguistique sera disponible (par ex. voir la [proposition de contrat](https://www.open-std.org/jtc1/sc22/wg21/docs/papers/2016/p0380r1.pdf)), nous adopterons la version standard des préconditions, postconditions et assertions.

##### Remarque

`Expects()` peut aussi être utilisé pour vérifier une condition en milieu d'algorithme.

##### Remarque

Non, l'utilisation d'`unsigned` n'est pas un bon moyen de contourner le problème d'assurance d'une valeur non négative (ref: 010-expr.md#res-nonnegative).

##### Application

(N'agréable) Trouver les différentes façons dont les préconditions peuvent être assertées n'est pas faisable. Avertir de celles qui peuvent être facilement identifiées (`assert()`) a une valeur discutable en l'absence d'un dispositif de langage.

### <a name="ri-post"></a>I.7 : Préciser les postconditions

##### Raison

Pour détecter les malentendus sur le résultat et éventuellement capturer les implémentations erronées.

##### Exemple, mauvais

Considérez :

    int area(int height, int width) { return height * width; }  // bad

Ici, nous avons (incautionneusement) omis la spécification des préconditions, donc il n'est pas explicite que `height` et `width` doivent être positifs.
Nous avons aussi omis la spécification des postconditions, donc il n'est pas évident que l'algorithme (`height * width`) soit erroné pour des surfaces plus grandes que le plus grand entier.
L'overflow peut survenir.
Considérez l'utilisation :

    int area(int height, int width)
    {
        auto res = height * width;
        Ensures(res > 0);
        return res;
    }

##### Exemple, mauvais

Considérez un bug de sécurité célèbre :

    void f()    // problematic
    {
        char buffer[MAX];
        // ...
        memset(buffer, 0, sizeof(buffer));
    }

Il n'y avait pas de postcondition indiquant que le tampon doit être effacé et l'optimiseur a éliminé l'appel apparemment redondant `memset()` :

    void f()    // better
    {
        char buffer[MAX];
        // ...
        memset(buffer, 0, sizeof(buffer));
        Ensures(buffer[0] == 0);
    }

##### Remarque

Les postconditions sont souvent formulées de façon informelle dans un commentaire qui décrit le but d'une fonction ; `Ensures()` peut être utilisé pour rendre cela plus systématique, visible et vérifiable.

##### Remarque

Les postconditions sont particulièrement importantes lorsqu'elles concernent quelque chose qui n'est pas directement reflété par un résultat retourné, tel qu'un état d'une structure de données utilisée.

##### Exemple

Considérez une fonction qui manipule un `Record`, utilisant un `mutex` pour éviter des conditions de concurrence :

    mutex m;

    void manipulate(Record& r)    // don't
    {
        m.lock();
        // ... no m.unlock() ...
    }

Ici, nous « oubliions » d'indiquer que le `mutex` doit être libéré, donc nous ne savons pas si l'oubli de libération du `mutex` est un bug ou une fonctionnalité.
En déclarant la postcondition, cela serait clair :

    void manipulate(Record& r)    // postcondition: m is unlocked upon exit
    {
        m.lock();
        // ... no m.unlock() ...
    }

Le bug devient alors évident (mais uniquement à un humain lisant les commentaires).

Mieux encore, utilisez [RAII](009-resource.md#rr-raii) pour garantir que la postcondition (« le verrou doit être libéré ») est imposée dans le code :

    void manipulate(Record& r)    // best
    {
        lock_guard<mutex> _ {m};
        // ...
    }

##### Remarque

Idéalement les postconditions sont formulées dans l'interface/déclaration afin que les utilisateurs puissent les voir facilement.
Seules les postconditions relatives aux utilisateurs peuvent être formulées dans l'interface.
Les postconditions relatives uniquement à l'état interne appartiennent à la définition/implémentation.

##### Application

(N'agréable) C'est une directive philosophique qui n'est pas faisable à vérifier directement dans le cas général. Les vérificateurs spécifiques de domaine (par ex. vérificateur de possession de verrou) existent pour de nombreuses chaînes d'outils.

### <a name="ri-ensures"></a>I.8 : Préférer `Ensures()` pour exprimer les postconditions

##### Raison

Pour clarifier que la condition est une postcondition et permettre l'utilisation d'outils.

##### Exemple

    void f()
    {
        char buffer[MAX];
        // ...
        memset(buffer, 0, MAX);
        Ensures(buffer[0] == 0);
    }

##### Remarque

Les postconditions peuvent être exprimées de nombreuses manières, y compris les commentaires, les déclarations `if` et `assert()`.
Cela peut les rendre difficiles à distinguer du code ordinaire, difficiles à mettre à jour, difficiles à manipuler par des outils, et peut avoir la mauvaise sémantique.

**Alternative** : les postconditions de la forme « cette ressource doit être libérée » sont mieux exprimées par [RAII](009-resource.md#rr-raii).

##### Remarque

Idéalement, `Ensures` devrait être partie de l'interface, mais ce n'est pas réalisable.
Pour l'instant, nous le plaçons dans la définition (corps de fonction).
Quand le soutien du langage deviendra disponible (par ex. voir la [proposition de contrat](https://www.open-std.org/jtc1/sc22/wg21/docs/papers/2016/p0380r1.pdf)), nous adopterons la version standard des préconditions, postconditions et assertions.

##### Application

(N'agréable) Trouver les différentes façons dont les postconditions peuvent être assertées n'est pas faisable. Avertir de celles qui peuvent être facilement identifiées (`assert()`) a une valeur discutable en l'absence d'un dispositif de langage.

### <a name="ri-concepts"></a>I.9 : Si une interface est un modèle, documenter ses paramètres à l'aide de concepts

##### Raison

Faire que l'interface soit précisément spécifiée et vérifiable à la compilation dans un avenir proche.

##### Exemple

Utilisez le style C++20 de spécification des exigences. Par exemple :

    template<typename Iter, typename Val>
      requires input_iterator<Iter> && equality_comparable_with<iter_value_t<Iter>, Val>
    Iter find(Iter first, Iter last, Val v)
    {
        // ...
    }

**Voir aussi** : [Programmation générique](015-templates.md#ss-gp) et [Concepts](015-templates.md#ss-concepts).

##### Application

Avertir si tout paramètre de modèle non-variadic n'est pas contraint par un concept (dans sa déclaration ou mentionné dans une clause `requires`).

### <a name="ri-except"></a>I.10 : Utiliser des exceptions pour signaler un échec de réalisation d'une tâche requise

##### Raison

Il ne doit pas être possible d'ignorer une erreur car cela pourrait laisser le système ou un calcul dans un état indéfini (ou inattendu).
C'est une grande source d'erreurs.

##### Exemple

    int printf(const char* ...);    // bad: return negative number if output fails

    template<class F, class ...Args>
    // good: throw system_error if unable to start the new thread
    explicit thread(F&& f, Args&&... args);

##### Remarque

Qu'est ce qu'une erreur ?

Une erreur signifie que la fonction ne peut pas atteindre son objectif annoncé (y compris établir les postconditions).
Un appelant qui ignore une erreur peut conduire à des résultats erronés ou à un état du système indéfini.
Par exemple, ne pas pouvoir se connecter à un serveur distant n'est pas en soi une erreur :
le serveur peut refuser une connexion pour toutes sortes de raisons, donc la chose naturelle est de retourner un résultat que l'appelant doit toujours vérifier.
Cependant, si l'échec de connexion est considéré comme une erreur, alors un échec doit lancer une exception.

##### Exception

De nombreuses fonctions d'interface traditionnelles (p. ex. gestionnaires de signaux UNIX) utilisent des codes d'erreur (p. ex. `errno`) pour rapporter ce qui sont réellement des codes d'état, plutôt que des erreurs. Vous n'avez pas d'alternative viable à l'utilisation de tels codes, donc l'appeler n'enfreint pas la règle.

##### Alternative

Si vous ne pouvez pas utiliser d'exceptions (p. ex. parce que votre code est plein d'utilisation de pointeurs bruts ou à cause de contraintes de temps réel), envisagez un style qui retourne une paire de valeurs :

    int val;
    int error_code;
    tie(val, error_code) = do_something();
    if (error_code) {
        // ... handle the error or exit ...
    }
    // ... use val ...

Ce style conduit malheureusement à des variables non initialisées.
Depuis C++17, la fonctionnalité des « bindings structurés » peut être utilisée pour initialiser directement des variables à partir de la valeur de retour :

    auto [val, error_code] = do_something();
    if (error_code) {
        // ... handle the error or exit ...
    }
    // ... use val ...

##### Remarque

Nous ne considérons pas « performance » comme une raison valable de ne pas utiliser d'exceptions.

* Souvent, le contrôle d'erreur explicite et la gestion consomment autant de temps et d'espace que la gestion d'exceptions.
* Souvent, un code plus propre produit de meilleures performances grâce aux exceptions (en simplifiant le parcours des chemins dans le programme et leur optimisation).
* Une bonne règle pour le code critique en performance est de déplacer le contrôle hors de la [partie critique](011-performance.md#rper-critical).
* À long terme, un code plus régulier sera mieux optimisé.
* Toujours mesurer soigneusement ([mesure](011-performance.md#rper-measure)) avant d'affirmer des gains de performance.

**Voir aussi** : [I.5](005-interfaces.md#ri-pre) et [I.7](005-interfaces.md#ri-post) pour la déclaration des violations de précondition et de postcondition.

##### Application

* (Non réalisable) Cette directive philosophique n'est pas faisable à vérifier directement.
* Rechercher `errno`.

### <a name="ri-raw"></a>I.11 : Ne jamais transférer la propriété par un pointeur brut (`T*`) ou une référence (`T&`)

##### Raison

S'il y a un doute sur le fait que l'appelant ou le callee possède un objet, des fuites ou des destructions précoces se produiront.

##### Exemple

Considérez :

    X* compute(args)    // don't
    {
        X* res = new X{};
        // ...
        return res;
    }

Qui supprime le `X` renvoyé ? Le problème est plus difficile à détecter si `compute` renvoie une référence.
Envisagez de retourner le résultat par valeur (utiliser les sémantique de mouvement si le résultat est volumineux) :

    vector<double> compute(args)  // good
    {
        vector<double> res(10000);
        // ...
        return res;
    }

**Alternative** : [Passer la propriété](009-resource.md#rr-smartptrparam) en utilisant un "smart pointer", tel qu'un `unique_ptr` (pour la propriété exclusive) et `shared_ptr` (pour la propriété partagée).
Cependant, c'est moins élégant et souvent moins efficace que de retourner l'objet lui‑même, alors utilisez les pointeurs intelligents uniquement si la sémantique de référence est requise.

**Alternative** : Parfois, un ancien code ne peut être modifié en raison d'exigences de compatibilité ABI ou de manque de ressources.
Dans ce cas, marquez les pointeurs de propriétaire en utilisant `owner` de la [bibliothèque de support des lignes directrices](#gsl-guidelines-support-library) :

    owner<X*> compute(args)    // It is now clear that ownership is transferred
    {
        owner<X*> res = new X{};
        // ...
        return res;
    }

Cela indique aux outils d'analyse que `res` est un propriétaire.
En d'autres termes, sa valeur doit être `delete` ou transférée à un autre propriétaire, comme c'est le cas ici par le `return`.

`owner` est utilisé de façon similaire dans la mise en œuvre des gestionnaires de ressources.

##### Remarque

Tout objet passé en tant que pointeur brut (ou itérateur) est supposé être possédé par l'appelant, afin que sa durée de vie soit gérée par l'appelant. D'un autre côté : les API de transfert de propriété sont relativement rares par rapport aux API de passage de pointeurs, donc le défaut est « pas de transfert de propriété ».

**Voir aussi** : [Passage d'arguments](006-functions.md#rf-conventional), [utilisation de pointeurs intelligents en arguments](009-resource.md#rr-smartptrparam) et [retour par valeur](006-functions.md#rf-value-return).

##### Application

* (Simple) Avertir sur le `delete` d'un pointeur brut qui ne devient pas un `owner<T>`. Suggérer l'utilisation d'un gestionnaire de ressources de la bibliothèque standard ou l'utilisation de `owner<T>`.
* (Simple) Avertir en cas d'oubli de `reset` ou de `delete` explicite d'un `owner` sur chaque chemin de code.
* (Simple) Avertir si la valeur de retour d'un `new` ou d'un appel de fonction retournant un `owner` est assignée à un pointeur brut ou à une référence non‑`owner`.

### <a name="ri-nullptr"></a>I.12 : Déclarer un pointeur qui ne doit pas être nul comme `not_null`

##### Raison

Pour éviter les erreurs de déréférencement `nullptr`. Pour améliorer les performances en évitant les vérifications inutiles pour `nullptr`.

##### Exemple

    int length(const char* p);            // it is not clear whether length(nullptr) is valid

    length(nullptr);                      // OK?

    int length(not_null<const char*> p);  // better: we can assume that p cannot be nullptr

    int length(const char* p);            // we must assume that p can be nullptr

En déclarant l'intention dans le code source, les implémenteurs et les outils peuvent fournir de meilleures diagnostics, telles que la détection de certaines catégories d'erreurs par analyse statique, et effectuer des optimisations, telles que la suppression de branches et de tests nuls.

##### Remarque

`not_null` est défini dans la [bibliothèque de support des lignes directrices](#gsl-guidelines-support-library).

##### Remarque

L'hypothèse que le pointeur `char` pointe vers une chaîne C‑style (un tableau zéro‑terminé) était toujours implicite, et était une source potentielle de confusion et d'erreurs. Utilisez `czstring` en lieu et place de `const char*`.

    // we can assume that p cannot be nullptr
    // we can assume that p points to a zero-terminated array of characters
    int length(not_null<czstring> p);

Note : `length()` est en fait `std::strlen()` déguisé.

##### Application

* (Simple) ((Fondation)) Si une fonction vérifie un pointeur paramètre contre `nullptr` avant l'accès, sur tous les chemins, alors avertir qu'il devrait être déclaré `not_null`.
* (Complexe) Si une fonction avec valeur de retour pointeur s'assure qu'elle n'est pas `nullptr` sur tous les chemins de retour, avertir que le type de retour devrait être déclaré `not_null`.

### <a name="ri-array"></a>I.13 : Ne pas passer un tableau comme un seul pointeur

##### Raison

Les interfaces (pointeur, taille) sont source d'erreurs. En outre, un simple pointeur vers un tableau doit se fier à une convention pour permettre au callee de déterminer la taille.

##### Exemple

Considérez :

    void copy_n(const T* p, T* q, int n); // copy from [p:p+n) to [q:q+n)

Que se passe-t-il s'il y a moins que `n` éléments dans le tableau pointé par `q` ? On écrase alors de la mémoire probablement non liée.
Que se passe-t-il s'il y a moins que `n` éléments dans le tableau pointé par `p` ? On lit alors de la mémoire probablement non liée.
C'est un comportement indéfini et un bug potentiellement très maléfique.

##### Alternative

Considérez l'utilisation de `span`s explicites :

    void copy(span<const T> r, span<T> r2); // copy r to r2

##### Exemple, mauvais

Considérez :

    void draw(Shape* p, int n);  // poor interface; poor code
    Circle arr[10];
    // ...
    draw(arr, 10);

Passer `10` comme argument `n` peut être une erreur : la convention la plus courante suppose `[0:n)` mais ce n'est jamais déclaré. Mieux, l'appel de `draw()` compile : il y a une conversion implicite d'un tableau à un pointeur (décroissance du tableau) puis une autre conversion implicite de `Circle` à `Shape`. Il n'y a aucun moyen pour `draw()` d'itérer en toute sécurité sur ce tableau : il ne connaît pas la taille des éléments.

**Alternative** : Utiliser une classe de support qui garantit que le nombre d'éléments est correct et empêche les conversions implicites dangereuses. Par ex. :

    void draw2(span<Circle>);
    Circle arr[10];
    // ...
    draw2(span<Circle>(arr));  // deduce the number of elements
    draw2(arr);    // deduce the element type and array size

    void draw3(span<Shape>);
    draw3(arr);    // error: cannot convert Circle[10] to span<Shape>

Cette `draw2()` passe la même quantité d'information à `draw()`, mais rend explicite qu'il s'agit d'une plage de `Circle`. Voir ???.

##### Exception

Utilisez `zstring` et `czstring` pour représenter des chaînes C‑style et zéro‑terminées.
Mais quand vous le faites, utilisez `std::string_view` ou `span<char>` de la [bibliothèque GSL] pour éviter les erreurs de plage.

##### Application

* (Simple) ((Bornes)) Avertir pour toute expression qui dépendrait d'une conversion implicite d'un tableau vers un pointeur. Autoriser l'exception pour les pointeurs `zstring`/`czstring`.
* (Simple) ((Bornes)) Avertir pour toute opération arithmétique sur une expression de type pointeur qui aboutirait à une valeur de type pointeur. Autoriser l'exception pour les pointeurs `zstring`/`czstring`.

### <a name="ri-global-init"></a>I.22 : Éviter une initialisation complexe des objets globaux

##### Raison

Une initialisation complexe peut conduire à un ordre d'exécution indéfini.

##### Exemple

    // file1.c

    extern const X x;

    const Y y = f(x);   // read x; write y

    // file2.c

    extern const Y y;

    const X x = g(y);   // read y; write x

Comme `x` et `y` se trouvent dans deux unités de traduction différentes, l'ordre des appels à `f()` et `g()` est indéfini ; l'un lira un `const` non initialisé.
Ceci montre que le problème d'ordre d'initialisation des objets globaux (à l'échelle du namespace) n'est pas limité aux *variables* globales.

##### Remarque

Les problèmes d'ordre d'initialisation deviennent particulièrement difficiles à gérer dans un code concurrent.
Il est généralement préférable d'éviter les objets globaux (à l'échelle du namespace) en tout cas.

##### Application

* Marquer les initialiseurs de globales qui appellent des fonctions non‑`constexpr`.
* Marquer les initialiseurs de globales qui accèdent à des objets `extern`.

### <a name="ri-nargs"></a>I.23 : Limiter le nombre d'arguments d'une fonction

##### Raison

En avoir beaucoup ouvre des opportunités de confusion. Passer beaucoup d'arguments est souvent plus coûteux que des alternatives.

##### Discussion

Les deux raison les plus courantes pour lesquelles les fonctions ont trop d'arguments sont :

1. *Manquer une abstraction.* Il manque une abstraction, donc une valeur composée est passée comme éléments individuels plutôt que comme un seul objet qui impose une invariance. Cela ne fait pas qu'élargir la liste d'arguments, mais il conduit à des erreurs parce que les valeurs composantes ne sont plus protégées par une invariance imposée.

2. *Violating "one function, one responsibility."* La fonction essaie de faire plus qu'un travail et devrait probablement être refactorée.

##### Exemple

La fonction `merge()` de la bibliothèque standard est à la limite de ce que nous pouvons gérer confortablement :

    template<class InputIterator1, class InputIterator2, class OutputIterator, class Compare>
    OutputIterator merge(InputIterator1 first1, InputIterator1 last1,
                         InputIterator2 first2, InputIterator2 last2,
                         OutputIterator result, Compare comp);

Notez que c'est du fait du problème (1) ci‑dessus — manque d'abstraction. Au lieu de passer une plage (abstraction), le STL passe des paires d'itérateurs (valeurs component non encapsulées).

Ici, nous avons quatre paramètres de modèle et six arguments de fonction.
Pour simplifier les utilisations les plus fréquentes et les plus simples, l'argument de comparaison peut être par défaut à `<` :

    template<class InputIterator1, class InputIterator2, class OutputIterator>
    OutputIterator merge(InputIterator1 first1, InputIterator1 last1,
                         InputIterator2 first2, InputIterator2 last2,
                         OutputIterator result);

Cela ne réduit pas la complexité totale, mais diminue la surface de complexité présentée à la plupart des utilisateurs.
Pour vraiment réduire le nombre d'arguments, il faut regrouper les arguments dans des abstractions plus élevées :

    template<class InputRange1, class InputRange2, class OutputIterator>
    OutputIterator merge(InputRange1 r1, InputRange2 r2, OutputIterator result);

Mettre les arguments en "bundles" est une technique générale pour réduire le nombre d'arguments et augmenter les possibilités de vérification.

Alternativement, on pourrait utiliser une notion de concept de STL pour décrire les trois types qui doivent être utilisables pour le merge :

    template<class In1, class In2, class Out>
      requires mergeable<In1, In2, Out>
    Out merge(In1 r1, In2 r2, Out result);

##### Exemple

Les profils de sécurité recommandent le remplacement de

    void f(int* some_ints, int some_ints_length);  // BAD: C style, unsafe

par

    void f(gsl::span<int> some_ints);              // GOOD: safe, bounds-checked

En utilisant une abstraction, on obtient des bénéfices de sécurité et de robustesse, et naturellement on réduit le nombre de paramètres.

##### Remarque

Combien de paramètres sont trop ? Essayez d'utiliser moins de quatre (4) paramètres. Il existe des fonctions qui sont mieux exprimées avec quatre paramètres individuels, mais ce n'est pas beaucoup.

**Alternative** : Utiliser une meilleure abstraction : regrouper les arguments en objets significatifs et les passer par valeur ou par référence.

**Alternative** : Utiliser des paramètres par défaut ou surcharges pour permettre aux formes les plus fréquentes d'appels d'être faites avec moins d'arguments.

##### Application

* Avertir lorsqu'une fonction déclare deux itérateurs (y compris des pointeurs) de même type au lieu d'une plage ou d'une vue.
* (Non réalisable) C'est une directive philosophique qui n'est pas faisable à vérifier directement.

### <a name="ri-unrelated"></a>I.24 : Éviter les paramètres adjacents qui peuvent être invoqués par les mêmes arguments dans n'importe quel ordre avec des significations différentes

##### Raison

Les arguments adjacents de même type sont facilement inversés par erreur.

##### Exemple, mauvais

Considérez :

    void copy_n(T* p, T* q, int n);  // copy from [p:p + n) to [q:q + n)

C'est une mauvaise variante d'une interface de style C. Il est facile d'inverser les arguments « to » et « from ».

Utilisez `const` pour l'argument « from »  :

    void copy_n(const T* p, T* q, int n);  // copy from [p:p + n) to [q:q + n)

##### Exception

Si l'ordre des paramètres n'est pas important, il n'y a pas de problème :

    int max(int a, int b);

##### Alternative

Ne pas passer des tableaux comme pointeurs, passer un objet représentant une plage (p. ex. `span`)  :

    void copy_n(span<const T> p, span<T> q);  // copy from p to q

##### Alternative

Définir une `struct` comme type de paramètre et nommer les champs pour ces paramètres  :

    struct SystemParams {
        string config_file;
        string output_path;
        seconds timeout;
    };
    void initialize(SystemParams p);

Ceci tend à clarifier les appels de cette fonction pour les futurs lecteurs, puisque les paramètres sont souvent remplis par nom au point d'appel.

##### Remarque

Seul le concepteur de l'interface peut résoudre adéquatement la source des violations de cette directive.

##### Stratégie d'application

*(Simple) Avertir si deux paramètres consécutifs partagent le même type.*

Nous recherchons encore une approche moins simple.

### <a name="ri-abstract"></a>I.25 : Préférer les classes abstraites vides comme interfaces aux hiérarchies de classes

##### Raison

Les classes abstraites vides (sans données membres non‑statiques) sont plus susceptibles d'être stables que les classes de base avec état.

##### Exemple, mauvais

Vous avez simplement pensé que `Shape` apparaîtra un jour :-)

    class Shape {  // bad: interface class loaded with data
    public:
        Point center() const { return c; }
        virtual void draw() const;
        virtual void rotate(int);
        // ...
    private:
        Point c;
        vector<Point> outline;
        Color col;
    };

Cela forcerait chaque classe dérivée à calculer un centre — même si c'est non trivial et que le centre n'est jamais utilisé. De même, tous les `Shape` n'ont pas forcément de `Color`, et de nombreux `Shape` sont mieux représentés sans une `outline` définie comme une séquence de `Point`. Utiliser une classe abstraite est mieux :

    class Shape {    // better: Shape is a pure interface
    public:
        virtual Point center() const = 0;   // pure virtual functions
        virtual void draw() const = 0;
        virtual void rotate(int) = 0;
        // ...
        // ... no data members ...
        // ...
        virtual ~Shape() = default;
    };

##### Application

*(Simple) Avertir si un pointeur/référence à une classe `C` est assigné à un pointeur/référence à une base de `C` et que la classe de base contient des membres de données.*

### <a name="ri-abi"></a>I.26 : Si vous voulez une ABI cross‑compilatrice, utilisez un sous‑ensemble C‑style

##### Raison

Différents compilateurs utilisent des structures binaires différentes pour les classes, le traitement des exceptions, les noms de fonction et d'autres détails d'implémentation.

##### Exception

Des ABI communs émergent sur certains plateformes, vous libérant des restrictions plus draconiennes.

##### Remarque

Si vous utilisez un seul compilateur, vous pouvez utiliser le C++ complet dans les interfaces. Cela peut nécessiter une recompilation après une mise à jour de la version du compilateur.

##### Application

(N'agréable) C'est difficile à identifier de façon fiable où une interface fait partie d'une ABI.

### <a name="ri-pimpl"></a>I.27 : Pour une ABI stable de bibliothèque, envisagez l'idiome Pimpl

##### Raison

Comme les membres privés participent au layout d'une classe et les membres privés participent à la résolution de surcharge, les changements de ces détails d'implémentation exigent une recompilation de tous les utilisateurs d'une classe qui les utilise. Une classe d'interface non polymorphique contenant un pointeur vers l'implémentation (`Pimpl`) peut isoler les utilisateurs d'une classe des changements de son implémentation au prix d'une indirection.

##### Exemple

fichier interface (widget.h)

    class widget {
        class impl;
        std::unique_ptr<impl> pimpl;
    public:
        void draw(); // public API that will be forwarded to the implementation
        widget(int); // defined in the implementation file
        ~widget();   // defined in the implementation file, where impl is a complete type
        widget(widget&&) noexcept; // defined in the implementation file
        widget(const widget&) = delete;
        widget& operator=(widget&&) noexcept; // defined in the implementation file
        widget& operator=(const widget&) = delete;
    };

fichier implémentation (widget.cpp)

    class widget::impl {
        int n; // private data
    public:
        void draw(const widget& w) { /* ... */ }
        impl(int n) : n(n) {}
    };
    void widget::draw() { pimpl->draw(*this); }
    widget::widget(int n) : pimpl{std::make_unique<impl>(n)} {}
    widget::widget(widget&&) noexcept = default;
    widget::~widget() = default;
    widget& widget::operator=(widget&&) noexcept = default;

##### Notes

Consultez [GOTW #100](https://herbsutter.com/gotw/_100/) et [cppreference](https://en.cppreference.com/w/cpp/language/pimpl) pour les compromis et les détails d'implémentation supplémentaires associés à ce idiome.

##### Application

(N'agréable) Il est difficile d'identifier de façon fiable où une interface fait partie d'une ABI.

### <a name="ri-encapsulate"></a>I.30 : Encapsuler les violations de règle

##### Raison

Pour garder le code simple et sécurisé.
Parfois, des techniques proéminentes, peu sûres ou sujettes à erreurs sont nécessaires pour des raisons logiques ou de performance.
Si c'est le cas, gardez ces techniques localisées plutôt que d'« infecter » les interfaces afin que de plus grands groupes de programmeurs n'aient pas à connaître les subtilités.
La complexité d'implémentation ne devrait, si possible, pas s'échapper à travers les interfaces dans le code utilisateur.

##### Exemple

Considérons un programme qui, selon une forme d'entrée (p. ex. arguments de `main`), doit consommer l'entrée depuis un fichier, depuis la ligne de commande ou depuis l'entrée standard.
Nous pourrions écrire

    bool owned;
    owner<istream*> inp;
    switch (source) {
    case std_in:        owned = false; inp = &cin;                       break;
    case command_line:  owned = true;  inp = new istringstream{argv[2]}; break;
    case file:          owned = true;  inp = new ifstream{argv[2]};      break;
    }
    istream& in = *inp;

Cette violation de la règle des variables non initialisées, de la règle contre l'ignorance de la propriété et de la règle contre les constantes magiques. En particulier, quelqu'un doit se souvenir d'écrire

    if (owned) delete inp;

Nous pourrions gérer ce cas en utilisant `unique_ptr` avec un déléger spécial qui ne fait rien pour `cin`, mais c'est compliqué pour les novices (qui peuvent facilement rencontrer ce problème) et l'exemple est un exemple d'un problème plus général où une propriété que nous aimerions considérer statiquement (ici, la propriété de possession) doit rarement être abordée à l'exécution.
Les exemples courants, les plus fréquents et plus sûrs peuvent être traités statiquement, nous ne voulons pas ajouter de coûts et de complexité à ceux .
Mais nous devons aussi gérer les cas inhabituels, moins sûrs et forcément plus coûteux.
Ces exemples sont discutés dans [[Str15]](https://www.stroustrup.com/resource-model.pdf).

Ainsi, nous écrivons une classe

    class Istream { [[gsl::suppress("lifetime")]]
    public:
        enum Opt { from_line = 1 };
        Istream() { }
        Istream(czstring p) : owned{true}, inp{new ifstream{p}} {}            // read from file
        Istream(czstring p, Opt) : owned{true}, inp{new istringstream{p}} {}  // read from command line
        ~Istream() { if (owned) delete inp; }
        operator istream&() { return *inp; }
    private:
        bool owned = false;
        istream* inp = &cin;
    };

Maintenant, la nature dynamique de la propriété de l'`istream` a été encapsulée.
Probablement, un peu de vérification pour les erreurs potentielles serait ajouté dans le code réel.

##### Application

* Difficile, il est difficile de décider quel code viole réellement la règle et est essentiel
* Marquer l'utilisation de supressions de règle qui permettent aux violations de règle de transiter dans les interfaces

---