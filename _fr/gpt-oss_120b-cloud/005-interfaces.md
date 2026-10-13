# <a name="s-interfaces"></a>I : Interfaces

Une interface est un contrat entre deux parties d’un programme. Décrire précisément ce qui est attendu d’un fournisseur de service et d’un utilisateur de ce service est essentiel. Disposer d’interfaces de bonne qualité (faciles à comprendre, favorisant une utilisation efficace, non sujettes aux erreurs, facilitant les tests, etc.) constitue probablement l’aspect le plus important de l’organisation du code.

**Résumé des règles d’interface :**

* [I.1 : Rendre les interfaces explicites](005-interfaces.md#ri-explicit)
* [I.2 : Éviter les variables globales non `const`](005-interfaces.md#ri-global)
* [I.3 : Éviter les singletons](005-interfaces.md#ri-singleton)
* [I.4 : Rendre les interfaces précisément et fortement typées](005-interfaces.md#ri-typed)
* [I.5 : Indiquer les préconditions (le cas échéant)](005-interfaces.md#ri-pre)
* [I.6 : Préférer `Expects()` pour exprimer les préconditions](005-interfaces.md#ri-expects)
* [I.7 : Indiquer les postconditions](005-interfaces.md#ri-post)
* [I.8 : Préférer `Ensures()` pour exprimer les postconditions](005-interfaces.md#ri-ensures)
* [I.9 : Si une interface est un modèle, documenter ses paramètres à l’aide de concepts](005-interfaces.md#ri-concepts)
* [I.10 : Utiliser les exceptions pour signaler un échec dans l’exécution d’une tâche requise](005-interfaces.md#ri-except)
* [I.11 : Ne jamais transférer la propriété via un pointeur brut (`T*`) ou une référence (`T&`)](005-interfaces.md#ri-raw)
* [I.12 : Déclarer un pointeur qui ne doit pas être nul comme `not_null`](005-interfaces.md#ri-nullptr)
* [I.13 : Ne pas passer un tableau sous forme d’un pointeur unique](005-interfaces.md#ri-array)
* [I.22 : Éviter l’initialisation complexe d’objets globaux](005-interfaces.md#ri-global-init)
* [I.23 : Limiter le nombre d’arguments de fonctions](005-interfaces.md#ri-nargs)
* [I.24 : Éviter les paramètres adjacents qui peuvent être invoqués avec les mêmes arguments dans un ordre quelconque avec des significations différentes](005-interfaces.md#ri-unrelated)
* [I.25 : Préférer les classes abstraites vides comme interfaces aux hiérarchies de classes](005-interfaces.md#ri-abstract)
* [I.26 : Si vous voulez une ABI multi‑compilateur, utilisez un sous‑ensemble de style C](005-interfaces.md#ri-abi)
* [I.27 : Pour une ABI de bibliothèque stable, envisagez l’idiome Pimpl](005-interfaces.md#ri-pimpl)
* [I.30 : Encapsuler les violations de règle](005-interfaces.md#ri-encapsulate)

**Voir aussi :**

* [F : Fonctions](006-functions.md)
* [C.concrete : Types concrets](007-class.md#ss-concrete)
* [C.hier : Hiérarchies de classes](007-class.md#ss-hier)
* [C.over : Surcharge et opérateurs surchargés](007-class.md#ss-overload)
* [C.con : Conteneurs et autres gestionnaires de ressources](007-class.md#ss-containers)
* [E : Gestion des erreurs](013-errors.md)
* [T : Modèles et programmation générique](015-templates.md)

### <a name="ri-explicit"></a>I.1 : Rendre les interfaces explicites

##### Raison

Correction. Les hypothèses non indiquées dans une interface sont facilement négligées et difficiles à tester.

##### Exemple, mauvais

Contrôler le comportement d’une fonction via une variable globale (définie à l’échelle du namespace) (un mode d’appel) est implicite et potentiellement confus. Par exemple :

    int round(double d)
    {
        return (round_up) ? ceil(d) : d;    // don't: "invisible" dependency
    }

Il ne sera pas évident pour l’appelant que l’exécution de deux appels à `round(7.2)` puisse donner des résultats différents.

##### Exception

Parfois, nous contrôlons les détails d’un ensemble d’opérations à l’aide d’une variable d’environnement, par exemple sortie normale vs sortie verbeuse ou débogage vs optimisation. L’utilisation d’un contrôle non local est potentiellement déroutante, mais ne contrôle que les détails d’implémentation d’une sémantique sinon fixe.

##### Exemple, mauvais

Signaler via des variables non locales (par ex., `errno`) est facilement ignoré. Par exemple :

    // don't: no test of fprintf's return value
    fprintf(connection, "logging: %d %d %d\n", x, y, s);

Que se passe‑t-il si la connexion échoue de sorte qu’aucune sortie de journalisation n’est produite ? Voir I.??? @TODO-LINK.

**Alternative** : Lancer une exception. Une exception ne peut pas être ignorée.

**Formulation alternative** : Éviter de transmettre des informations à travers une interface via un état non local ou implicite. Notez que les fonctions membres non `const` transmettent des informations à d’autres fonctions membres via l’état de l’objet.

**Formulation alternative** : Une interface doit être une fonction ou un ensemble de fonctions. Les fonctions peuvent être des modèles de fonctions et les ensembles de fonctions peuvent être des classes ou des modèles de classe.

##### Application

* (Simple) Une fonction ne doit pas prendre de décisions de contrôle de flux basées sur les valeurs de variables déclarées à l’échelle du namespace.
* (Simple) Une fonction ne doit pas écrire dans des variables déclarées à l’échelle du namespace.

### <a name="ri-global"></a>I.2 : Éviter les variables globales non `const`

##### Raison

Les variables globales non `const` masquent des dépendances et rendent ces dépendances sujettes à des modifications imprévisibles.

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

Qui d’autre pourrait modifier `data` ?

**Avertissement** : L’initialisation des objets globaux n’est pas totalement ordonnée. Si vous utilisez un objet global, initialisez‑le avec une constante. Notez qu’il est possible d’obtenir un ordre d’initialisation indéfini même pour les objets `const`.

##### Exception

Un objet global est souvent meilleur qu’un singleton.

##### Note

Les constantes globales sont utiles.

##### Note

La règle contre les variables globales s’applique également aux variables à l’échelle du namespace.

**Alternative** : Si vous utilisez des données globales (plus généralement des données à l’échelle du namespace) pour éviter des copies, envisagez de les passer à une fonction sous forme d’un objet par référence `const`. Une autre solution consiste à définir les données comme l’état d’un objet et les opérations comme fonctions membres.

**Avertissement** : Méfiez‑vous des courses de données : si un thread peut accéder à des données non locales (ou à des données passées par référence) pendant qu’un autre thread exécute le code appelant, une course de données peut se produire. Tout pointeur ou référence vers des données mutables constitue une course potentielle.

Utiliser des pointeurs ou références globaux pour accéder et modifier des données non `const` n’est pas une meilleure alternative aux variables globales non `const`, car cela ne résout ni le problème des dépendances cachées ni les risques de courses.

##### Note

Il est impossible d’avoir une course de données sur des données immuables.

**Références** : Voir les [règles d’appel de fonctions](006-functions.md#ss-call).

##### Note

La règle est « éviter », pas « ne pas utiliser ». Bien sûr, il existera (rarement) des exceptions, comme `cin`, `cout` et `cerr`.

##### Application

(Simple) Signaler toutes les variables non `const` déclarées à l’échelle du namespace ainsi que les pointeurs/références globaux vers des données non `const`.

### <a name="ri-singleton"></a>I.3 : Éviter les singletons

##### Raison

Les singletons sont essentiellement des objets globaux compliqués sous un déguisement.

##### Exemple

    class Singleton {
        // ... lots of stuff to ensure that only one Singleton object is created,
        // that it is initialized properly, etc.
    };

Il existe de nombreuses variantes du concept de singleton. C’est là une partie du problème.

##### Note

Si vous ne voulez pas qu’un objet global change, déclarez‑le `const` ou `constexpr`.

##### Exception

Vous pouvez utiliser le « singleton » le plus simple (tellement simple qu’on ne le considère souvent même pas comme un singleton) pour obtenir une initialisation à la première utilisation, le cas échéant :

    X& myX()
    {
        static X my_x {3};
        return my_x;
    }

C’est l’une des solutions les plus efficaces aux problèmes d’ordre d’initialisation. Dans un environnement multithread, l’initialisation de l’objet `static` ne crée pas de course de données (à moins que vous accédiez négligemment à un objet partagé depuis son constructeur).

Notez que l’initialisation d’un `static` local ne sous-entend pas de course de données. Cependant, si la destruction de `X` implique une opération qui doit être synchronisée, il faut alors recourir à une solution moins triviale. Par exemple :

    X& myX()
    {
        static auto p = new X {3};
        return *p;  // potential leak
    }

Quelqu’un devra alors `delete` cet objet d’une manière sécurisée pour les threads. Cette technique est source d’erreurs, donc on ne l’emploie que si :

* `myX` est utilisé dans du code multithread,
* cet objet `X` doit être détruit (par ex., parce qu’il libère une ressource), et
* le code du destructeur de `X` doit être synchronisé.

Si vous, comme beaucoup d’autres, définissez un singleton comme une classe dont un seul objet est créé, les fonctions comme `myX` ne sont pas des singletons, et cette technique utile n’est pas une exception à la règle d’interdiction des singletons.

##### Application

Très difficile en général.

* Chercher des classes dont le nom comprend `singleton`.
* Chercher des classes pour lesquelles un seul objet est jamais créé (en comptant les objets ou en examinant les constructeurs).
* Si une classe `X` possède une fonction statique publique contenant un `static` local du type `X` et renvoie un pointeur ou une référence vers celui‑ci, interdire cela.

### <a name="ri-typed"></a>I.4 : Rendre les interfaces précisément et fortement typées

##### Raison

Les types sont la documentation la plus simple et la meilleure ; ils améliorent la lisibilité grâce à leur signification bien définie et sont vérifiés à la compilation. De plus, le code précisément typé est souvent mieux optimisé.

##### Exemple, mauvais

Considérez :

    void pass(void* data);    // weak and under-qualified type void* is suspicious

Les appelants ne savent pas quels types sont permis et si les données peuvent être modifiées, `const` n’étant pas spécifié. Toutes les pointeurs se convertissent implicitement en `void*`, il est donc facile pour l’appelant de fournir cette valeur.

L’appelé doit alors `static_cast` les données vers un type non vérifié pour les utiliser. Cela est source d’erreurs et verbeux.

N’utilisez `const void*` que pour passer des données dans des conceptions indéfinissables en C++. Envisagez d’utiliser un `variant` ou un pointeur vers une base à la place.

**Alternative** : Souvent, un paramètre de modèle peut éliminer le `void*` en le transformant en `T*` ou `T&`. Pour le code générique, ces `T` peuvent être généraux ou des paramètres de modèle contraints par des concepts.

##### Exemple, mauvais

Considérez :

    draw_rect(100, 200, 100, 500); // what do the numbers specify?

    draw_rect(p.x, p.y, 10, 20); // what units are 10 and 20 in?

Il est clair que l’appelant décrit un rectangle, mais il est obscur de savoir à quoi correspondent les quatre `int`. Un `int` peut porter n’importe quelle forme d’information, y compris des valeurs exprimées dans différentes unités, de sorte que l’on doit deviner la signification des quatre paramètres. Il est fort probable que les deux premiers constituent une paire de coordonnées `x`,`y`, mais que représentent les deux derniers ?

Les commentaires et les noms de paramètres peuvent aider, mais nous pouvons être explicites :

    void draw_rectangle(Point top_left, Point bottom_right);
    void draw_rectangle(Point top_left, Size height_width);

    draw_rectangle(p, Point{10, 20});  // deux coins
    draw_rectangle(p, Size{10, 20});   // un coin et une paire (hauteur, largeur)

Il est évident que nous ne pouvons pas attraper toutes les erreurs via le système de types statiques (par ex., le fait que le premier argument doive être un coin en haut à gauche relève de la convention – nommage et commentaires).

##### Exemple, mauvais

Considérez :

    set_settings(true, false, 42); // what do the numbers specify?

Les types de paramètres et leurs valeurs ne communiquent pas quels réglages sont spécifiés ni ce que ces valeurs signifient.

Un design plus explicite, sûr et lisible serait :

    alarm_settings s{};
    s.enabled = true;
    s.displayMode = alarm_settings::mode::spinning_light;
    s.frequency = alarm_settings::every_10_seconds;
    set_settings(s);

Pour un ensemble de valeurs booléennes, considérez l’utilisation d’un `enum` de drapeaux ; un motif qui exprime un ensemble de valeurs booléennes.

    enable_lamp_options(lamp_option::on | lamp_option::animate_state_transitions);

##### Exemple, mauvais

Dans l’exemple suivant, il n’est pas clair depuis l’interface ce que signifie `time_to_blink` : secondes ? millisecondes ?

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

Les types `std::chrono::duration` aident à rendre explicite l’unité de durée.

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

La fonction peut aussi être écrite de façon à accepter n’importe quelle unité de durée :

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

* (Simple) Signaler l’utilisation de `void*` comme paramètre ou type de retour.
* (Simple) Signaler l’utilisation de plus d’un paramètre `bool`.
* (Difficile à faire correctement) Chercher les fonctions qui utilisent trop d’arguments de type primitif.

### <a name="ri-pre"></a>I.5 : Indiquer les préconditions (le cas échéant)

##### Raison

Les arguments possèdent un sens qui peut contraindre leur utilisation correcte dans la fonction appelée.

##### Exemple

Considérez :

    double sqrt(double x);

Ici, `x` doit être non‑négatif. Le système de types ne peut pas (facilement et naturellement) exprimer cela, nous devons donc recourir à d’autres moyens. Par exemple :

    double sqrt(double x); // x must be non-negative

Certaines préconditions peuvent être exprimées sous forme d’assertions. Par exemple :

    double sqrt(double x) { Expects(x >= 0); /* ... */ }

Idéalement, ce `Expects(x >= 0)` devrait faire partie de l’interface de `sqrt()`, mais ce n’est pas aisé. Pour l’instant, nous le plaçons dans la définition (corps de fonction).

**Références** : `Expects()` est décrit dans la [GSL](#gsl-guidelines-support-library).

##### Note

Préférez une spécification formelle des exigences, telle que `Expects(p);`. Si cela est impossible, utilisez du texte anglais en commentaire, par ex., `// the sequence [p:q) is ordered using <`.

##### Note

La plupart des fonctions membres ont comme précondition que certains invariants de classe soient valides. Ces invariants sont établis par le constructeur et doivent être rétablis à la sortie de chaque fonction membre appelée depuis l’extérieur de la classe. Nous n’avons pas besoin de les mentionner pour chaque fonction membre.

##### Application

(Non enforceable)

**Voir aussi** : Les règles de passage des pointeurs. ??? @TODO-LINK.

### <a name="ri-expects"></a>I.6 : Préférer `Expects()` pour exprimer les préconditions

##### Raison

Rendre explicite que la condition est une précondition et permettre l’usage d’outils.

##### Exemple

    int area(int height, int width)
    {
        Expects(height > 0 && width > 0);            // good
        if (height <= 0 || width <= 0) my_error();   // obscure
        // ...
    }

##### Note

Les préconditions peuvent être exprimées de nombreuses façons, y compris dans des commentaires, des instructions `if` ou `assert()`. Cela les rend difficiles à distinguer du code ordinaire, difficiles à mettre à jour, à manipuler par des outils, et peut leur conférer une sémantique erronée (voulez‑vous toujours interrompre en mode debug et ne rien vérifier en production ?).

##### Note

Les préconditions devraient faire partie de l’interface plutôt que de l’implémentation, mais les facilités du langage ne le permettent pas encore. Dès que le support du langage sera disponible (voir la [proposition de contrat](https://www.open-std.org/jtc1/sc22/wg21/docs/papers/2016/p0380r1.pdf)), nous adopterons la version standardisée des préconditions, postconditions et assertions.

##### Note

`Expects()` peut également être utilisé pour vérifier une condition au milieu d’un algorithme.

##### Note

Non, l’usage de `unsigned` n’est pas une bonne façon de contourner le problème de [garantir qu’une valeur est non‑négative](010-expr.md#res-nonnegative).

##### Application

(Non enforceable) Il n’est pas réaliste de recenser toutes les manières d’assertion des préconditions. Avertir de celles qui peuvent être facilement identifiées (`assert()`) a une valeur discutable en l’absence d’une facette du langage.

### <a name="ri-post"></a>I.7 : Indiquer les postconditions

##### Raison

Détecter les malentendus concernant le résultat et éventuellement intercepter des implémentations erronées.

##### Exemple, mauvais

Considérez :

    int area(int height, int width) { return height * width; }  // bad

Nous avons omission de la précondition (hauteur et largeur doivent être positives) et omission de la postcondition (le produit peut dépasser la capacité d’un `int`). Un dépassement peut survenir.

Une version plus explicite :

    int area(int height, int width)
    {
        auto res = height * width;
        Ensures(res > 0);
        return res;
    }

##### Exemple, mauvais

Un bug de sécurité célèbre :

    void f()    // problematic
    {
        char buffer[MAX];
        // ...
        memset(buffer, 0, sizeof(buffer));
    }

Aucune postcondition n’indiquait que le tampon devait être effacé ; l’optimiseur a alors éliminé l’appel apparemment redondant à `memset()`.

Version améliorée :

    void f()    // better
    {
        char buffer[MAX];
        // ...
        memset(buffer, 0, sizeof(buffer));
        Ensures(buffer[0] == 0);
    }

##### Note

Les postconditions sont souvent indiquées de façon informelle dans un commentaire décrivant le but d’une fonction ; `Ensures()` peut rendre cela plus systématique, visible et vérifiable.

##### Note

Les postconditions sont particulièrement importantes lorsqu’elles concernent un état qui n’est pas directement reflété dans la valeur de retour, comme l’état d’une structure de données.

##### Exemple

Considérez une fonction qui manipule un `Record`, en utilisant un `mutex` pour éviter les courses de données :

    mutex m;

    void manipulate(Record& r)    // don't
    {
        m.lock();
        // ... no m.unlock() ...
    }

Ici, nous « oublions » d’indiquer que le `mutex` doit être libéré, on ne sait donc pas si cet oubli est un bug ou une fonctionnalité. Indiquer la postcondition aurait clarifié les choses :

    void manipulate(Record& r)    // postcondition: m is unlocked upon exit
    {
        m.lock();
        // ... no m.unlock() ...
    }

Le bug devient alors évident (mais seulement pour un humain lisant les commentaires).

Mieux encore, utilisez le [RAII](009-resource.md#rr-raii) pour garantir que la postcondition (« le verrou doit être libéré ») soit appliquée :

    void manipulate(Record& r)    // best
    {
        lock_guard<mutex> _ {m};
        // ...
    }

##### Note

Idéalement, les postconditions sont indiquées dans l’interface/déclaration afin que les utilisateurs les voient facilement. Seules les postconditions pertinentes pour les utilisateurs peuvent être inscrites dans l’interface. Celles concernant uniquement l’état interne appartiennent à la définition/implémentation.

##### Application

(Non enforceable) Il s’agit d’une consigne philosophique difficile à vérifier directement. Des analyseurs spécifiques (par ex., les vérificateurs de détention de verrous) existent pour de nombreux chaînes d’outils.

### <a name="ri-ensures"></a>I.8 : Préférer `Ensures()` pour exprimer les postconditions

##### Raison

Rendre explicite que la condition est une postcondition et permettre l’usage d’outils.

##### Exemple

    void f()
    {
        char buffer[MAX];
        // ...
        memset(buffer, 0, MAX);
        Ensures(buffer[0] == 0);
    }

##### Note

Les postconditions peuvent être indiquées de plusieurs façons, y compris les commentaires, les instructions `if` ou `assert()`. Cela les rend difficiles à distinguer du code ordinaire, à mettre à jour, à manipuler par des outils, et peut leur conférer une mauvaise sémantique.

**Alternative** : Les postconditions de forme « cette ressource doit être libérée » sont mieux exprimées par le [RAII](009-resource.md#rr-raii).

##### Note

Idéalement, `Ensures` ferait partie de l’interface, mais ce n’est pas aisé. Pour l’instant, nous le plaçons dans la définition (corps de fonction). Dès que le support du langage sera disponible (voir la [proposition de contrat](https://www.open-std.org/jtc1/sc22/wg21/docs/papers/2016/p0380r1.pdf)), nous adopterons la version standardisée des préconditions, postconditions et assertions.

##### Application

(Non enforceable) Recenser toutes les manières d’assertion des postconditions n’est pas réaliste. Avertir de celles qui peuvent être facilement identifiées (`assert()`) a une valeur discutable en l’absence d’une facette du langage.

### <a name="ri-concepts"></a>I.9 : Si une interface est un modèle, documenter ses paramètres à l’aide de concepts

##### Raison

Rendre l’interface précisément spécifiée et vérifiable à la compilation dans un futur (pas si lointain).

##### Exemple

Utilisez le style C++20 de spécification d’exigences. Par exemple :

    template<typename Iter, typename Val>
      requires input_iterator<Iter> && equality_comparable_with<iter_value_t<Iter>, Val>
    Iter find(Iter first, Iter last, Val v)
    {
        // ...
    }

**Voir aussi** : [Programmation générique](015-templates.md#ss-gp) et [concepts](015-templates.md#ss-concepts).

##### Application

Avertir si un paramètre de modèle non variadique n’est pas contraint par un concept (dans sa déclaration ou mentionné dans une clause `requires`).

### <a name="ri-except"></a>I.10 : Utiliser les exceptions pour signaler un échec dans l’exécution d’une tâche requise

##### Raison

Il ne doit pas être possible d’ignorer une erreur, car cela pourrait laisser le système ou le calcul dans un état indéfini (ou inattendu). C’est une source majeure d’erreurs.

##### Exemple

    int printf(const char* ...);    // bad: return negative number if output fails

    template<class F, class ...Args>
    // good: throw system_error if unable to start the new thread
    explicit thread(F&& f, Args&&... args);

##### Note

Qu’est‑ce qu’une erreur ?

Une erreur signifie que la fonction ne peut pas atteindre le but annoncé (y compris établir les postconditions). Un code appelant qui ignore une erreur pourrait produire des résultats erronés ou laisser le système dans un état indéfini. Par exemple, ne pas pouvoir se connecter à un serveur distant n’est pas en soi une erreur : le serveur peut refuser la connexion pour diverses raisons, la chose naturelle est donc de renvoyer un résultat que l’appelant doit toujours vérifier. En revanche, si l’échec de connexion est considéré comme une erreur, alors l’échec doit lever une exception.

##### Exception

De nombreuses fonctions d’interface traditionnelles (par ex., les gestionnaires de signal UNIX) utilisent des codes d’erreur (par ex., `errno`) pour signaler ce qui sont en réalité des codes d’état, plutôt que des erreurs. Vous n’avez pas d’alternative valable, ainsi appeler ces fonctions ne viole pas la règle.

##### Alternative

Si vous ne pouvez pas utiliser les exceptions (par ex., parce que votre code est truffé d’utilisation de pointeurs bruts de style ancien ou parce qu’il y a des contraintes de temps réel strictes), envisagez un style qui renvoie une paire de valeurs :

    int val;
    int error_code;
    tie(val, error_code) = do_something();
    if (error_code) {
        // ... handle the error or exit ...
    }
    // ... use val ...

Ce style conduit malheureusement à des variables non initialisées. Depuis C++17, la fonctionnalité « structured bindings » peut être utilisée pour initialiser directement les variables à partir de la valeur de retour :

    auto [val, error_code] = do_something();
    if (error_code) {
        // ... handle the error or exit ...
    }
    // ... use val ...

##### Note

Nous ne considérons pas la « performance » comme une raison valable de ne pas utiliser les exceptions.

* Souvent, les contrôles d’erreur explicites et le traitement consomment autant de temps et d’espace que la gestion d’exceptions.
* Souvent, un code plus propre donne de meilleures performances en simplifiant le suivi des chemins d’exécution et leur optimisation.
* Une bonne règle pour le code critique en termes de performance est de déplacer les vérifications hors de la partie [critique](011-performance.md#rper-critical) du code.
* À plus long terme, un code plus régulier est mieux optimisé.
* Toujours mesurer **avec soin** avant de formuler des affirmations de performance ([mesure](011-performance.md#rper-measure)).

**Voir aussi** : [I.5](005-interfaces.md#ri-pre) et [I.7](005-interfaces.md#ri-post) pour le signalement des violations de préconditions et de postconditions.

##### Application

* (Non enforceable) Il s’agit d’une consigne philosophique difficile à vérifier directement.
* Chercher `errno`.

### <a name="ri-raw"></a>I.11 : Ne jamais transférer la propriété via un pointeur brut (`T*`) ou une référence (`T&`)

##### Raison

Si l’on doute qui, parmi l’appelant et l’appelé, possède un objet, des fuites ou des destructions prématurées peuvent survenir.

##### Exemple

Considérez :

    X* compute(args)    // don't
    {
        X* res = new X{};
        // ...
        return res;
    }

Qui supprime le `X` retourné ? Le problème serait encore plus difficile à repérer si `compute` renvoyait une référence.

Considérez le retour du résultat par valeur (utilisez la sémantique de déplacement si le résultat est volumineux) :

    vector<double> compute(args)  // good
    {
        vector<double> res(10000);
        // ...
        return res;
    }

**Alternative** : [Passer la propriété](009-resource.md#rr-smartptrparam) à l’aide d’un « smart pointer », tel que `unique_ptr` (pour la propriété exclusive) ou `shared_ptr` (pour la propriété partagée). Cependant, cela est moins élégant et souvent moins efficace que de retourner directement l’objet, donc n’utilisez les pointeurs intelligents que si une sémantique de référence est réellement nécessaire.

**Alternative** : Parfois du code ancien ne peut pas être modifié en raison d’exigences de compatibilité d’ABI ou par manque de ressources. Dans ce cas, marquez les pointeurs propriétaires avec `owner` de la [guidelines support library](#gsl-guidelines-support-library) :

    owner<X*> compute(args)    // It is now clear that ownership is transferred
    {
        owner<X*> res = new X{};
        // ...
        return res;
    }

Cela indique aux outils d’analyse que `res` est un propriétaire. Autrement dit, sa valeur doit être `delete`‑d ou transférée à un autre propriétaire, comme le fait le `return`.

`owner` est utilisé de façon similaire dans l’implémentation des gestionnaires de ressources.

##### Note

Tout objet passé sous forme de pointeur brut (ou d’itérateur) est supposé appartenir à l’appelant, de sorte que sa durée de vie soit gérée par l’appelant. En d’autres termes : les API qui transfèrent la propriété sont relativement rares comparées aux API qui passent simplement des pointeurs, donc le comportement par défaut est « pas de transfert de propriété ».

**Voir aussi** : [Passage d’arguments](006-functions.md#rf-conventional), [utilisation d’arguments de pointeurs intelligents](009-resource.md#rr-smartptrparam) et [retour de valeur](006-functions.md#rf-value-return).

##### Application

* (Simple) Avertir lorsqu’un `delete` d’un pointeur brut n’est pas un `owner<T>`. Suggérer l’usage d’un gestionnaire de ressources de la bibliothèque standard ou de `owner<T>`.
* (Simple) Avertir en cas d’échec de `reset` ou de `delete` explicite d’un pointeur `owner` sur tous les chemins de code.
* (Simple) Avertir si la valeur de retour de `new` ou d’une fonction renvoyant un `owner` est assignée à un pointeur brut ou à une référence non‑`owner`.

### <a name="ri-nullptr"></a>I.12 : Déclarer un pointeur qui ne doit pas être nul comme `not_null`

##### Raison

Aider à éviter les erreurs de déréférencement de `nullptr`. Améliorer les performances en supprimant les vérifications redondantes de `nullptr`.

##### Exemple

    int length(const char* p);            // it is not clear whether length(nullptr) is valid

    length(nullptr);                      // OK?

    int length(not_null<const char*> p);  // better: we can assume that p cannot be nullptr

    int length(const char* p);            // we must assume that p can be nullptr

En indiquant l’intention dans le code source, les implémenteurs et les outils peuvent fournir de meilleurs diagnostics, tels que la détection de certaines classes d’erreurs par analyse statique, et réaliser des optimisations comme la suppression de branches et de tests nuls.

##### Note

`not_null` est défini dans la [guidelines support library](#gsl-guidelines-support-library).

##### Note

L’hypothèse que le pointeur `char` pointe vers une chaîne de style C (une chaîne de caractères terminée par un zéro) était encore implicite, et source potentielle de confusion et d’erreurs. Utilisez `czstring` de préférence à `const char*`.

    // we can assume that p cannot be nullptr
    // we can assume that p points to a zero-terminated array of characters
    int length(not_null<czstring> p);

Note : `length()` est bien sûr `std::strlen()` sous un autre nom.

##### Application

* (Simple) ((Foundation)) Si une fonction teste un paramètre pointeur contre `nullptr` avant l’accès, sur tous les chemins de contrôle, alors avertir qu’il devrait être déclaré `not_null`.
* (Complex) Si une fonction avec type de retour pointeur garantit qu’il n’est jamais `nullptr` sur tous les chemins de retour, alors avertir que le type de retour devrait être déclaré `not_null`.

### <a name="ri-array"></a>I.13 : Ne pas passer un tableau sous forme d’un pointeur unique

##### Raison

Les interfaces de style (pointeur, taille) sont sujettes aux erreurs. Un pointeur simple (vers un tableau) doit se reposer sur une convention pour permettre à l’appelé de déterminer la taille.

##### Exemple

Considérez :

    void copy_n(const T* p, T* q, int n); // copy from [p:p+n) to [q:q+n)

Que se passe‑t‑il s’il y a moins de `n` éléments dans le tableau pointé par `q` ? Nous écrasons alors potentiellement de la mémoire non liée. Que se passe‑t‑il s’il y a moins de `n` éléments dans le tableau pointé par `p` ? Nous lisons alors potentiellement de la mémoire non liée. Dans les deux cas, le comportement est indéfini et potentiellement très dangereux.

##### Alternative

Envisagez d’utiliser des `span` explicites :

    void copy(span<const T> r, span<T> r2); // copy r to r2

##### Exemple, mauvais

Considérez :

    void draw(Shape* p, int n);  // poor interface; poor code
    Circle arr[10];
    // ...
    draw(arr, 10);

Passer `10` comme argument `n` peut être une erreur : la convention la plus courante consiste à supposer `[0:n)`, mais cela n’est déclaré nulle part. Pire, l’appel à `draw()` compile tout de même : il y a conversion implicite du tableau en pointeur (décroissance du tableau) puis conversion implicite de `Circle` en `Shape`. `draw()` n’a aucun moyen de parcourir ce tableau en toute sécurité : il ne connaît pas la taille des éléments.

**Alternative** : Utilisez une classe de support qui garantit que le nombre d’éléments est correct et empêche les conversions dangereuses implicites. Par exemple :

    void draw2(span<Circle>);
    Circle arr[10];
    // ...
    draw2(span<Circle>(arr));  // deduce the number of elements
    draw2(arr);    // deduce the element type and array size

    void draw3(span<Shape>);
    draw3(arr);    // error: cannot convert Circle[10] to span<Shape>

Cette fonction `draw2()` transmet la même quantité d’informations à `draw()`, mais rend explicite le fait qu’il s’agit d’une plage de `Circle`. See ??? @TODO-LINK.

##### Exception

Utilisez `zstring` et `czstring` pour représenter les chaînes C‑style terminées par un zéro. Mais dans ce cas, utilisez `std::string_view` ou `span<char>` de la [GSL](#gsl-guidelines-support-library) pour prévenir les erreurs de plage.

##### Application

* (Simple) ((Bounds)) Avertir toute expression qui dépendrait de la conversion implicite d’un type tableau en type pointeur. Autoriser les exceptions pour les types pointeur `zstring`/`czstring`.
* (Simple) ((Bounds)) Avertir toute opération arithmétique sur une expression de type pointeur qui aboutit à une valeur de type pointeur. Autoriser les exceptions pour les types pointeur `zstring`/`czstring`.

### <a name="ri-global-init"></a>I.22 : Éviter l’initialisation complexe d’objets globaux

##### Raison

Une initialisation complexe peut entraîner un ordre d’exécution indéfini.

##### Exemple

    // file1.c

    extern const X x;

    const Y y = f(x);   // read x; write y

    // file2.c

    extern const Y y;

    const X x = g(y);   // read y; write x

Comme `x` et `y` se trouvent dans des unités de traduction différentes, l’ordre des appels à `f()` et `g()` est indéfini ; l’un accédera à un `const` non initialisé. Cela montre que le problème d’ordre d’initialisation pour les objets globaux (à l’échelle du namespace) ne se limite pas aux variables globales.

##### Note

Les problèmes d’ordre d’initialisation deviennent particulièrement difficiles à gérer dans du code concurrent. Il est généralement préférable d’éviter complètement les objets globaux (à l’échelle du namespace).

##### Application

* Signaler les initialiseurs de globals qui appellent des fonctions non `constexpr`.
* Signaler les initialiseurs de globals qui accèdent à des objets `extern`.

### <a name="ri-nargs"></a>I.23 : Limiter le nombre d’arguments de fonctions

##### Raison

Un grand nombre d’arguments ouvre la porte à la confusion. Passer beaucoup d’arguments est souvent coûteux comparé à des alternatives.

##### Discussion

Les deux raisons les plus courantes pour lesquelles les fonctions ont trop de paramètres sont :

1. *Absence d’abstraction.*  
   Une abstraction manque, de sorte qu’une valeur composée est passée sous forme d’éléments individuels au lieu d’un seul objet qui impose un invariant. Cela n’élargit pas seulement la liste des paramètres, mais entraîne aussi des erreurs parce que les valeurs composantes ne sont plus protégées par un invariant imposé.

2. *Violation du principe « une fonction, une responsabilité ».  
   La fonction essaie d’accomplir plus d’une tâche et devrait probablement être refactorisée.

##### Exemple

L’algorithme de la bibliothèque standard `merge()` est au bord du raisonnable :

    template<class InputIterator1, class InputIterator2, class OutputIterator, class Compare>
    OutputIterator merge(InputIterator1 first1, InputIterator1 last1,
                         InputIterator2 first2, InputIterator2 last2,
                         OutputIterator result, Compare comp);

C’est dû au problème 1 ci‑dessus — absence d’abstraction. Au lieu de passer une plage (abstraction), la STL passe des paires d’itérateurs (valeurs de composant non encapsulées).

Nous avons ici quatre paramètres de modèle et six arguments de fonction. Pour simplifier les usages les plus fréquents et les plus simples, le paramètre de comparaison peut être par défaut à `<` :

    template<class InputIterator1, class InputIterator2, class OutputIterator>
    OutputIterator merge(InputIterator1 first1, InputIterator1 last1,
                         InputIterator2 first2, InputIterator2 last2,
                         OutputIterator result);

Cela ne réduit pas la complexité totale, mais diminue la complexité visible pour de nombreux utilisateurs. Pour réellement réduire le nombre d’arguments, il faut regrouper les arguments dans des abstractions de niveau supérieur :

    template<class InputRange1, class InputRange2, class OutputIterator>
    OutputIterator merge(InputRange1 r1, InputRange2 r2, OutputIterator result);

Regrouper les arguments en « bundles » est une technique générale pour réduire le nombre d’arguments et augmenter les possibilités de vérifications.

Alternativement, on pourrait employer un concept de bibliothèque standard pour définir la notion de trois types qui doivent être utilisables pour le merge :

    template<class In1, class In2, class Out>
      requires mergeable<In1, In2, Out>
    Out merge(In1 r1, In2 r2, Out result);

##### Exemple

Les profils de sécurité recommandent de remplacer :

    void f(int* some_ints, int some_ints_length);  // BAD: C style, unsafe

par :

    void f(gsl::span<int> some_ints);              // GOOD: safe, bounds‑checked

En utilisant une abstraction, on obtient des bénéfices de sécurité et de robustesse, et on réduit naturellement le nombre de paramètres.

##### Note

Combien de paramètres est‑t‑on trop ? Essayez de rester en dessous de quatre (4) paramètres. Certaines fonctions sont mieux exprimées avec quatre paramètres individuels, mais ce n’est pas fréquent.

**Alternative** : Utiliser une meilleure abstraction : regrouper les arguments dans des objets significatifs et passer ces objets (par valeur ou par référence).

**Alternative** : Utiliser des arguments par défaut ou des surcharges pour permettre les formes d’appels les plus courantes avec moins d’arguments.

##### Application

* Avertir lorsqu’une fonction déclare deux itérateurs (y compris des pointeurs) du même type au lieu d’une plage ou d’une vue.
* (Non enforceable) Il s’agit d’une consigne philosophique difficile à vérifier directement.

### <a name="ri-unrelated"></a>I.24 : Éviter les paramètres adjacents qui peuvent être invoqués avec les mêmes arguments dans un ordre quelconque avec des significations différentes

##### Raison

Des arguments adjacents du même type sont facilement intervertis par erreur.

##### Exemple, mauvais

Considérez :

    void copy_n(T* p, T* q, int n);  // copy from [p:p + n) to [q:q + n)

C’est une variante dangereuse d’une interface de style K&R C. Il est facile d’inverser les arguments « de » et « vers ».

Utilisez `const` pour l’argument « de » :

    void copy_n(const T* p, T* q, int n);  // copy from [p:p + n) to [q:q + n)

##### Exception

Si l’ordre des paramètres n’a pas d’importance, il n’y a pas de problème :

    int max(int a, int b);

##### Alternative

Ne pas passer des tableaux en tant que pointeurs, mais passer un objet représentant une plage (par ex., un `span`) :

    void copy_n(span<const T> p, span<T> q);  // copy from p to q

##### Alternative

Définissez une `struct` comme type de paramètre et nommez les champs en conséquence :

    struct SystemParams {
        string config_file;
        string output_path;
        seconds timeout;
    };
    void initialize(SystemParams p);

Cela rend les appels plus clairs, les paramètres étant souvent renseignés par nom à l’endroit d’appel.

##### Note

Seul le concepteur de l’interface peut traiter adéquatement la source des violations de cette consigne.

##### Stratégie d’application

(Simple) Avertir si deux paramètres consécutifs partagent le même type.

Nous recherchons toujours une méthode d’application moins simple.

### <a name="ri-abstract"></a>I.25 : Préférer les classes abstraites vides comme interfaces aux hiérarchies de classes

##### Raison

Les classes abstraites vides (sans données membres non‑statiques) sont plus susceptibles d’être stables que les classes de base contenant un état.

##### Exemple, mauvais

Vous saviez juste que `Shape` apparaîtrait quelque part :-)

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

Cela impose à chaque classe dérivée de calculer un centre — même si cela est lourd et que le centre n’est jamais utilisé. De même, toutes les `Shape` n’ont pas de `Color`, et beaucoup sont mieux représentées sans un contour défini comme une séquence de `Point`. Utiliser une classe abstraite est préférable :

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

(Simple) Avertir si un pointeur/référence à une classe `C` est assigné à un pointeur/référence d’une base de `C` et que la classe de base contient des membres de données.

### <a name="ri-abi"></a>I.26 : Si vous voulez une ABI multi‑compilateur, utilisez un sous‑ensemble de style C

##### Raison

Différents compilateurs implémentent des agencements binaires différents pour les classes, la gestion des exceptions, les noms de fonctions et d’autres détails d’implémentation.

##### Exception

Des ABI communes émergent sur certaines plateformes, vous libérant des restrictions plus draconiennes.

##### Note

Si vous n’utilisez qu’un seul compilateur, vous pouvez employer le C++ complet dans les interfaces. Cela peut toutefois nécessiter une recompilation après la mise à jour vers une nouvelle version du compilateur.

##### Application

(Not enforceable) Il est difficile d’identifier de façon fiable où une interface fait partie d’une ABI.

### <a name="ri-pimpl"></a>I.27 : Pour une ABI de bibliothèque stable, envisagez l’idiome Pimpl

##### Raison

Comme les membres de données privés participent à la disposition de la classe et que les fonctions membres privées participent à la résolution de surcharge, des changements dans ces détails d’implémentation exigent la recompilation de tous les utilisateurs d’une classe qui les utilise. Une classe d’interface non polymorphe contenant un pointeur vers l’implémentation (Pimpl) peut isoler les utilisateurs d’une classe des changements d’implémentation au prix d’une indirection.

##### Exemple

*interface (widget.h)*

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

*implementation (widget.cpp)*

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

Voir [GOTW #100](https://herbsutter.com/gotw/_100/) et [cppreference](https://en.cppreference.com/w/cpp/language/pimpl) pour les compromis et les détails supplémentaires relatifs à cet idiome.

##### Application

(Not enforceable) Il est difficile d’identifier de façon fiable où une interface fait partie d’une ABI.

### <a name="ri-encapsulate"></a>I.30 : Encapsuler les violations de règle

##### Raison

Garder le code simple et sûr. Parfois, des techniques laides, peu sûres ou sujettes à erreurs sont nécessaires pour des raisons logiques ou de performance. Si c’est le cas, gardez‑les locales, plutôt que de « contaminer » les interfaces, obligeant ainsi de plus grands groupes de programmeurs à connaître les subtilités. La complexité d’implémentation ne doit, dans la mesure du possible, pas s’infiltrer à travers les interfaces dans le code utilisateur.

##### Exemple

Considérez un programme qui, selon une forme d’entrée (par ex., les arguments de `main`), doit consommer l’entrée depuis un fichier, depuis la ligne de commande ou depuis l’entrée standard. Nous pourrions écrire :

    bool owned;
    owner<istream*> inp;
    switch (source) {
    case std_in:        owned = false; inp = &cin;                       break;
    case command_line:  owned = true;  inp = new istringstream{argv[2]}; break;
    case file:          owned = true;  inp = new ifstream{argv[2]};      break;
    }
    istream& in = *inp;

Cela viole la règle contre les variables non initialisées, la règle contre le transfert de propriété, et la règle contre les constantes magiques. En particulier, quelqu’un doit se rappeler d’écrire quelque part :

    if (owned) delete inp;

Nous pourrions gérer cet exemple particulier en utilisant `unique_ptr` avec un destructeur spécial qui ne fait rien pour `cin`, mais cela reste compliqué pour les novices (qui peuvent facilement rencontrer ce problème) et l’exemple illustre un problème plus général où une propriété que nous aimerions considérer statique (ici, la propriété) doit être traitée occasionnellement à l’exécution. Les exemples les plus fréquents et les plus sûrs peuvent être traités statiquement, si bien que nous ne voulons pas ajouter de coût et de complexité à ces cas. Mais nous devons aussi gérer les cas moins fréquents, moins sûrs et nécessairement plus coûteux. De tels exemples sont discutés dans [[Str15]](https://www.stroustrup.com/resource-model.pdf).

Ainsi, nous écrivons une classe :

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

Maintenant, la nature dynamique de la propriété de `istream` est encapsulée. En pratique, un peu de vérifications d’erreurs serait ajouté.

##### Application

* Difficile à appliquer, il est difficile de décider quel code enfreignant les règles est essentiel.
* Signaler les suppressions de règle qui permettent aux violations de traverser les interfaces.