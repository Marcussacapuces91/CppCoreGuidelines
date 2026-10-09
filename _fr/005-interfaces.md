# <a name="s-interfaces"></a>I: Interfaces

Une interface est un contrat entre deux parties d’un programme. Décrire précisément ce qui est attendu d’un fournisseur de service et d’un utilisateur de ce service est essentiel.  
Disposer d’interfaces de bonne qualité (faciles à comprendre, encourageant une utilisation efficace, peu sujettes aux erreurs, soutenant les tests, etc.) est probablement l’aspect le plus important de l’organisation du code.

Résumé des règles d’interface :

* [I.1 : Rendre les interfaces explicites](#ri-explicit)
* [I.2 : Éviter les variables globales non‑`const`](#ri-global)
* [I.3 : Éviter les singletons](#ri-singleton)
* [I.4 : Rendre les interfaces précisément et fortement typées](#ri-typed)
* [I.5 : Indiquer les préconditions (le cas échéant)](#ri-pre)
* [I.6 : Privilégier `Expects()` pour exprimer les préconditions](#ri-expects)
* [I.7 : Indiquer les postconditions](#ri-post)
* [I.8 : Privilégier `Ensures()` pour exprimer les postconditions](#ri-ensures)
* [I.9 : Si une interface est un modèle, documenter ses paramètres à l’aide de concepts](#ri-concepts)
* [I.10 : Utiliser les exceptions pour signaler un échec à l’accomplissement d’une tâche requise](#ri-except)
* [I.11 : Ne jamais transférer la propriété via un pointeur brut (`T*`) ou une référence (`T&`)](#ri-raw)
* [I.12 : Déclarer un pointeur qui ne doit pas être nul comme `not_null`](#ri-nullptr)
* [I.13 : Ne pas passer un tableau comme un seul pointeur](#ri-array)
* [I.22 : Éviter l’initialisation complexe d’objets globaux](#ri-global-init)
* [I.23 : Limiter le nombre d’arguments de fonction](#ri-nargs)
* [I.24 : Éviter des paramètres adjacents qui peuvent être invoqués avec les mêmes arguments dans n’importe quel ordre avec un sens différent](#ri-unrelated)
* [I.25 : Privilégier les classes abstraites vides comme interfaces aux hiérarchies de classes](#ri-abstract)
* [I.26 : Si vous voulez une ABI inter‑compilateur, utilisez un sous‑ensemble de style C](#ri-abi)
* [I.27 : Pour une ABI stable de bibliothèque, envisagez le idiome Pimpl](#ri-pimpl)
* [I.30 : Encapsuler les violations de règle](#ri-encapsulate)

**Voir aussi** :

* [F : Fonctions](#s-functions)
* [C.concrete : Types concrets](#ss-concrete)
* [C.hier : Hiérarchies de classes](#ss-hier)
* [C.over : Surcharge et opérateurs surchargés](#ss-overload)
* [C.con : Conteneurs et autres gestionnaires de ressources](#ss-containers)
* [E : Gestion des erreurs](#s-errors)
* [T : Modèles et programmation générique](#s-templates)

### <a name="ri-explicit"></a>I.1 : Rendre les interfaces explicites

##### Raison

Exactitude. Les hypothèses non explicitées dans une interface sont facilement négligées et difficiles à tester.

##### Exemple, mauvais

    int round(double d)
    {
        return (round_up) ? ceil(d) : d;    // don't: "invisible" dependency
    }

Il ne sera pas évident pour l’appelant que le résultat de deux appels à `round(7.2)` puisse être différent.

##### Exception

Parfois, nous contrôlons les détails d’un ensemble d’opérations à l’aide d’une variable d’environnement, par ex., sortie normale vs. verbeuse ou débogage vs. optimisé.  
L’utilisation d’un contrôle non local peut être source de confusion, mais ne concerne que les détails d’implémentation d’une sémantique autrement fixe.

##### Exemple, mauvais

Signaler via des variables non locales (par ex., `errno`) est facilement ignoré. Par exemple :

    // don't: no test of fprintf's return value
    fprintf(connection, "logging: %d %d %d\n", x, y, s);

Que se passe‑t‑il si la connexion tombe et qu’aucune sortie de journal n’est produite ? Voir I.???.

**Alternative** : Lancer une exception. Une exception ne peut pas être ignorée.

**Formulation alternative** : Éviter de transmettre des informations à travers une interface via un état non local ou implicite.  
Notez que les fonctions membres non‑`const` transmettent des informations à d’autres fonctions membres via l’état de leur objet.

**Formulation alternative** : Une interface devrait être une fonction ou un ensemble de fonctions.  
Les fonctions peuvent être des modèles de fonction et les ensembles de fonctions peuvent être des classes ou des modèles de classe.

##### Application

* (Simple) Une fonction ne doit pas prendre des décisions de contrôle de flux basées sur les valeurs de variables déclarées à la portée du namespace.  
* (Simple) Une fonction ne doit pas écrire dans des variables déclarées à la portée du namespace.

### <a name="ri-global"></a>I.2 : Éviter les variables globales non‑`const`

##### Raison

Les variables globales non‑`const` dissimulent des dépendances et rendent celles‑ci sujettes à des changements imprévisibles.

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

**Avertissement** : L’initialisation des objets globaux n’est pas totalement ordonnée.  
Si vous utilisez un objet global, initialisez‑le avec une constante.  
Notez qu’il est possible d’obtenir un ordre d’initialisation indéfini même pour des objets `const`.

##### Exception

Un objet global est souvent préférable à un singleton.

##### Note

Les constantes globales sont utiles.

##### Note

La règle contre les variables globales s’applique également aux variables à la portée du namespace.

##### Alternative

Si vous utilisez des données globales (ou plus généralement à la portée du namespace) pour éviter des copies, envisagez de passer les données sous forme d’objet par référence `const`.  
Une autre solution consiste à définir les données comme l’état d’un objet et les opérations comme fonctions membres.

**Avertissement** : Méfiez‑vous des data‑races : si un fil d’exécution peut accéder à des données non locales (ou à des données passées par référence) pendant qu’un autre fil exécute la fonction appelée, nous pouvons avoir une data‑race.  
Tout pointeur ou référence à des données mutables est une data‑race potentielle.

Utiliser des pointeurs ou références globaux pour accéder et modifier des données non‑const (et non‑globales) n’est pas une meilleure alternative aux variables globales non‑const, car cela ne résout pas les problèmes de dépendances cachées ou de conditions de course potentielles.

##### Note

On ne peut pas avoir de data‑race sur des données immuables.

**Références** : Voir les [règles d’appel de fonctions](#ss-call).

##### Note

La règle est « éviter », pas « ne pas utiliser ». Bien sûr, il y aura (rarement) des exceptions, telles que `cin`, `cout` et `cerr`.

##### Application

(Simple) Signaler toutes les variables non‑`const` déclarées à la portée du namespace ainsi que tous les pointeurs/références globaux vers des données non‑const.

### <a name="ri-singleton"></a>I.3 : Éviter les singletons

##### Raison

Les singletons sont essentiellement des objets globaux compliqués déguisés.

##### Exemple


    class Singleton {
        // ... lots of stuff to ensure that only one Singleton object is created,
        // that it is initialized properly, etc.
    };

Il existe de nombreuses variantes de l’idée de singleton. C’est là une partie du problème.

##### Note

Si vous ne voulez pas qu’un objet global change, déclarez‑le `const` ou `constexpr`.

##### Exception

Vous pouvez utiliser le « singleton » le plus simple (tel qu’il ne est souvent même pas considéré comme un singleton) pour obtenir une initialisation à la première utilisation, le cas échéant :

    X& myX()
    {
        static X my_x {3};
        return my_x;
    }

C’est l’une des solutions les plus efficaces aux problèmes liés à l’ordre d’initialisation.  
Dans un environnement multithread, l’initialisation de l’objet static ne crée pas de data‑race (à moins que vous n’accédiez négligemment à un objet partagé depuis son constructeur).

Notez que l’initialisation d’un `static` local n’implique pas de data‑race. Cependant, si la destruction de `X` implique une opération qui doit être synchronisée, il faut recourir à une solution moins triviale. Par exemple :


    X& myX()
    {
        static auto p = new X {3};
        return *p;  // potential leak
    }

Quelqu’un doit alors `delete` cet objet d’une manière correctement thread‑safe. Cette technique est source d’erreurs, on ne l’utilise donc que si :

* `myX` est employé dans du code multithread,  
* cet objet `X` doit être détruit (par ex. il libère une ressource), et  
* le code du destructeur de `X` doit être synchronisé.

Si, comme beaucoup le font, vous définissez un singleton comme une classe dont un seul objet est créé, les fonctions comme `myX` ne sont pas des singletons, et cette technique utile n’est pas une exception à la règle d’interdiction des singletons.

##### Enforcement

Très difficile en général.

* Rechercher des classes dont le nom contient `singleton`.  
* Rechercher des classes dont un seul objet est créé (en comptant les objets ou en examinant les constructeurs).  
* Si une classe `X` possède une fonction statique publique qui contient un static local de type `X` et renvoie un pointeur ou une référence vers celui‑ci, interdire cela.

### <a name="ri-typed"></a>I.4 : Rendre les interfaces précisément et fortement typées

##### Raison

Les types sont la documentation la plus simple et la plus fiable : ils améliorent la lisibilité grâce à leur signification bien définie et sont vérifiés à la compilation. De plus, un code fortement typé est souvent mieux optimisé.

##### Exemple, ne pas faire

    void pass(void* data);    // weak and under-qualified type void* is suspicious

Les appelants ne savent pas quels types sont autorisés ni si les données peuvent être modifiées (le `const` n’est pas indiqué). Tous les types pointeur se convertissent implicitement en `void*`, il est donc facile pour les appelants de fournir cette valeur.  

Le callee doit alors `static_cast` les données vers un type non vérifié pour les utiliser. C’est source d’erreurs et verbeux.  

N’utilisez `const void*` que dans des conceptions qui ne peuvent pas être décrites en C++. Considérez l’usage d’un `variant` ou d’un pointeur vers une base à la place.

**Alternative** : souvent, un paramètre de modèle peut éliminer le `void*` en le transformant en `T*` ou `T&`. Pour le code générique, ces `T` peuvent être généraux ou des paramètres de modèle limités par des concepts.

##### Exemple, mauvais


    draw_rect(100, 200, 100, 500); // what do the numbers specify?
    draw_rect(p.x, p.y, 10, 20);   // what units are 10 and 20 in?

Il est clair que l’appelant décrit un rectangle, mais il est incertain à quoi se rapportent les quatre entiers. Un `int` peut porter des informations de toute nature, y compris des valeurs d’unités diverses, donc il faut deviner la signification des quatre `int`. Le plus souvent, les deux premiers sont les coordonnées `x`,`y`, mais que représentent les deux derniers ?

Les commentaires et les noms de paramètres peuvent aider, mais on peut être explicite :


    void draw_rectangle(Point top_left, Point bottom_right);
    void draw_rectangle(Point top_left, Size height_width);

    draw_rectangle(p, Point{10, 20});  // deux coins
    draw_rectangle(p, Size{10, 20});   // un coin et un couple (hauteur, largeur)

Évidemment, on ne peut pas capturer toutes les erreurs via le système de types statiques (par ex., le fait que le premier argument doit être le coin supérieur gauche relève de la convention – noms et commentaires).

##### Exemple, mauvais

    set_settings(true, false, 42); // what do the numbers specify?

Les types de paramètres et leurs valeurs ne communiquent pas quels réglages sont spécifiés ni ce que signifient ces valeurs.

Ce design est plus explicite, sûr et lisible :

    alarm_settings s{};
    s.enabled = true;
    s.displayMode = alarm_settings::mode::spinning_light;
    s.frequency = alarm_settings::every_10_seconds;
    set_settings(s);

Pour un ensemble de valeurs booléennes, on peut utiliser un `enum` de drapeaux ; un motif qui exprime un ensemble de valeurs booléennes.

    enable_lamp_options(lamp_option::on | lamp_option::animate_state_transitions);

##### Exemple, mauvais

    void blink_led(int time_to_blink) // bad -- the unit is ambiguous
    {
        // ...
        // do something with time_to_blink
        // ...
    }

Il n’est pas clair ce que signifie `time_to_blink` : secondes ? millisecondes ?

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
* (Simple) Signaler l’utilisation de plusieurs paramètres `bool`.  
* (Difficile à faire correctement) Rechercher les fonctions qui utilisent trop d’arguments de types primitifs.

### <a name="ri-pre"></a>I.5 : Indiquer les préconditions (le cas échéant)

##### Raison

Les arguments ont une signification qui peut contraindre leur utilisation correcte dans le callee.

##### Exemple

    double sqrt(double x);

Ici `x` doit être non‑négatif. Le système de types ne peut pas (facilement et naturellement) exprimer cela, nous devons donc recourir à d’autres moyens. Par exemple :

    double sqrt(double x); // x must be non-negative

Certaines préconditions peuvent être exprimées sous forme d’assertions. Par exemple :

    double sqrt(double x) { Expects(x >= 0); /* ... */ }

Idéalement, ce `Expects(x >= 0)` devrait faire partie de l’interface de `sqrt()`, mais ce n’est pas simple à faire. Pour l’instant, nous le plaçons dans la définition (corps de fonction).

**Références** : `Expects()` est décrit dans la [bibliothèque de support des lignes directrices (GSL)](#gsl-guidelines-support-library).

##### Note

Privilégiez une spécification formelle des exigences, telle que `Expects(p);`.  
Si cela est impossible, utilisez du texte anglais dans les commentaires, par ex. `// the sequence [p:q) is ordered using <`.

##### Note

La plupart des fonctions membres ont comme précondition qu’un certain invariant de classe soit respecté. Cet invariant est établi par le constructeur et doit être ré‑établi à la sortie par chaque fonction membre appelée depuis l’extérieur de la classe. Il n’est pas nécessaire de le mentionner pour chaque fonction membre.

##### Application

(Not enforceable)

**Voir aussi** : les règles de passage de pointeurs. ???

### <a name="ri-expects"></a>I.6 : Privilégier `Expects()` pour exprimer les préconditions

##### Raison

Faire clairement comprendre que la condition est une précondition et permettre l’utilisation d’outils.

##### Exemple

    int area(int height, int width)
    {
        Expects(height > 0 && width > 0);            // good
        if (height <= 0 || width <= 0) my_error();   // obscure
        // ...
    }

##### Note

Les préconditions peuvent être exprimées de nombreuses façons, y compris les commentaires, les instructions `if` et `assert()`. Cela peut les rendre difficiles à distinguer du code ordinaire, difficiles à mettre à jour, difficiles à manipuler par des outils, et peut leur donner une sémantique inadéquate (voulez‑vous toujours aborter en mode debug et ne rien vérifier en production ?).

##### Note

Les préconditions devraient faire partie de l’interface plutôt que de l’implémentation, mais le langage ne fournit pas encore les moyens de le faire. Dès que le support du langage sera disponible (par ex. la [proposition de contrat](https://www.open-std.org/jtc1/sc22/wg21/docs/papers/2016/p0380r1.pdf)), nous adopterons la version standard des préconditions, postconditions et assertions.

##### Note

`Expects()` peut également être utilisé pour vérifier une condition au milieu d’un algorithme.

##### Note

Non : utiliser `unsigned` n’est pas une bonne façon d’éviter le problème d’[assurer qu’une valeur est non‑négative](#res-nonnegative).

##### Application

(Not enforceable) Trouver toutes les manières dont les préconditions peuvent être affirmées n’est pas faisable. Signaler celles qui sont facilement identifiables (`assert()`) a une valeur discutable en l’absence d’une facility linguistique.

### <a name="ri-post"></a>I.7 : Indiquer les postconditions

##### Raison

Détecter les malentendus sur le résultat et éventuellement attraper des implémentations erronées.

##### Exemple, mauvais

    int area(int height, int width) { return height * width; }  // bad

Nous avons (incautieusement) omis la spécification de la précondition, il n’est donc pas explicite que `height` et `width` doivent être positifs. Nous avons également omis la spécification de la postcondition, il n’est donc pas évident que l’algorithme (`height * width`) est erroné pour des aires supérieures au plus grand entier. Un débordement peut se produire.  
Considérez plutôt :

    int area(int height, int width)
    {
        auto res = height * width;
        Ensures(res > 0);
        return res;
    }

##### Exemple, mauvais

    void f()    // problematic
    {
        char buffer[MAX];
        // ...
        memset(buffer, 0, sizeof(buffer));
    }

Aucune postcondition ne stipulait que le tampon devait être vidé, et l’optimiseur a éliminé l’appel `memset()` apparemment redondant :

    void f()    // better
    {
        char buffer[MAX];
        // ...
        memset(buffer, 0, sizeof(buffer));
        Ensures(buffer[0] == 0);
    }

##### Note

Les postconditions sont souvent exprimées de façon informelle dans un commentaire qui indique le but d’une fonction ; `Ensures()` peut être utilisé pour rendre cela plus systématique, visible et vérifiable.

##### Note

Les postconditions sont particulièrement importantes lorsqu’elles concernent quelque chose qui n’est pas directement reflété dans le résultat retourné, par ex. l’état d’une structure de données utilisée.

##### Exemple

    mutex m;

    void manipulate(Record& r)    // don't
    {
        m.lock();
        // ... no m.unlock() ...
    }

Ici, nous « avons » oublié de préciser que le `mutex` devait être libéré, donc on ne sait pas si l’absence de libération du `mutex` est un bug ou une fonctionnalité. La postcondition aurait rendu cela clair :

    void manipulate(Record& r)    // postcondition: m is unlocked upon exit
    {
        m.lock();
        // ... no m.unlock() ...
    }

Le bug devient alors évident (mais uniquement pour un humain lisant les commentaires).

Mieux encore, utilisez [RAII](#rr-raii) pour garantir que la postcondition (« le verrou doit être libéré ») est appliquée dans le code :

    void manipulate(Record& r)    // best
    {
        lock_guard<mutex> _ {m};
        // ...
    }

##### Note

Idéalement, les postconditions sont indiquées dans l’interface/déclaration afin que les utilisateurs puissent les voir facilement. Seules les postconditions visibles par l’utilisateur peuvent être placées dans l’interface. Les postconditions qui ne concernent que l’état interne appartiennent à la définition/implémentation.

##### Application

(Not enforceable) Cette ligne directrice philosophique est impossible à vérifier directement dans le cas général. Des analyseurs spécifiques au domaine (comme les vérificateurs de détention de verrou) existent pour de nombreuses chaînes d’outils.

### <a name="ri-ensures"></a>I.8 : Privilégier `Ensures()` pour exprimer les postconditions

##### Raison

Faire clairement comprendre que la condition est une postcondition et permettre l’utilisation d’outils.

##### Exemple

    void f()
    {
        char buffer[MAX];
        // ...
        memset(buffer, 0, MAX);
        Ensures(buffer[0] == 0);
    }

##### Note

Les postconditions peuvent être exprimées de nombreuses façons, y compris les commentaires, les `if`‑statements et `assert()`. Cela peut les rendre difficiles à distinguer du code ordinaire, difficiles à mettre à jour, difficiles à manipuler par des outils, et peut leur donner une sémantique inappropriée.

**Alternative** : les postconditions du type « cette ressource doit être libérée » sont mieux exprimées par [RAII](#rr-raii).

##### Note

Idéalement, `Ensures` devrait faire partie de l’interface, mais ce n’est pas facile à mettre en œuvre. Pour l’instant, nous le plaçons dans la définition (corps de fonction). Dès que le support du langage sera disponible (voir la [proposition de contrat](https://www.open-std.org/jtc1/sc22/wg21/docs/papers/2016/p0380r1.pdf)), nous adopterons la version standard des préconditions, postconditions et assertions.

##### Application

(Not enforceable) Trouver toutes les manières dont les postconditions peuvent être affirmées n’est pas faisable. Signaler celles qui sont facilement identifiables (`assert()`) a une valeur discutable en l’absence d’une facility linguistique.

### <a name="ri-concepts"></a>I.9 : Si une interface est un modèle, documenter ses paramètres à l’aide de concepts

##### Raison

Spécifier précisément l’interface et rendre possible une vérification à la compilation dans un futur proche.

##### Exemple

Utilisez le style C++20 de spécification des exigences. Par exemple :

    template<typename Iter, typename Val>
      requires input_iterator<Iter> && equality_comparable_with<iter_value_t<Iter>, Val>
    Iter find(Iter first, Iter last, Val v)
    {
        // ...
    }

**Voir aussi** : [Programmation générique](#ss-gp) et [concepts](#ss-concepts).

##### Application

Avertir si tout paramètre de modèle non variadique n’est pas contraint par un concept (dans sa déclaration ou mentionné dans une clause `requires`).

### <a name="ri-except"></a>I.10 : Utiliser les exceptions pour signaler un échec à l’accomplissement d’une tâche requise

##### Raison

Il ne doit pas être possible d’ignorer une erreur, car cela pourrait laisser le système ou un calcul dans un état indéfini (ou inattendu). C’est une source majeure d’erreurs.

##### Exemple

    int printf(const char* ...);    // bad: return negative number if output fails

    template<class F, class ...Args>
        // good: throw system_error if unable to start the new thread
        explicit thread(F&& f, Args&&... args);

##### Note

**Qu’est‑ce qu’une erreur ?**  
Une erreur signifie que la fonction ne peut pas atteindre le but annoncé (y compris établir les postconditions). Un code appelant qui ignore une erreur peut produire des résultats erronés ou laisser le système dans un état indéfini. Par exemple, ne pas pouvoir se connecter à un serveur distant n’est pas en soi une erreur : le serveur peut refuser la connexion pour de nombreuses raisons, donc le plus naturel est de renvoyer un résultat que l’appelant doit toujours vérifier. Cependant, si l’échec de connexion est considéré comme une erreur, alors il faut lancer une exception.

##### Exception

De nombreuses fonctions d’interface traditionnelles (par ex. les gestionnaires de signaux UNIX) utilisent des codes d’erreur (par ex. `errno`) pour rapporter ce qui est en réalité des codes d’état, pas des erreurs. Vous n’avez pas de bonne alternative à cela, donc les appeler ne viole pas la règle.

##### Alternative

Si vous ne pouvez pas utiliser d’exceptions (par ex. votre code est truffé d’usage de pointeurs bruts legacy ou vous avez des contraintes temps‑réel strictes), envisagez un style qui renvoie une paire de valeurs :

    int val;
    int error_code;
    tie(val, error_code) = do_something();
    if (error_code) {
        // ... handle the error or exit ...
    }
     // ... use val ...

Ce style conduit malheureusement à des variables non initialisées. Depuis C++17, la fonctionnalité « structured bindings » peut être utilisée pour initialiser les variables directement depuis la valeur retournée :

    auto [val, error_code] = do_something();
    if (error_code) {
        // ... handle the error or exit ...
    }
     // ... use val ...

##### Note

Nous ne considérons pas la performance comme une raison valable de ne pas utiliser les exceptions.

* Souvent, la vérification explicite des erreurs et leur gestion consomment autant de temps et d’espace que la gestion par exception.  
* Souvent, un code plus propre donne de meilleures performances avec les exceptions (simplification du traçage des chemins à travers le programme et leur optimisation).  
* Une bonne règle pour le code critique en performance est de déplacer les vérifications hors de la partie [critique](#rper-critical) du code.  
* À plus long terme, un code plus régulier est mieux optimisé.  
* Toujours mesurer soigneusement ([mesurer](#rper-measure)) avant de faire des affirmations de performance.

**Voir aussi** : [I.5](#ri-pre) et [I.7](#ri-post) pour le signalement des violations de préconditions et postconditions.

##### Application

* (Not enforceable) Il s’agit d’une ligne directrice philosophique qu’il est impossible de vérifier directement.  
* Rechercher les usages de `errno`.

### <a name="ri-raw"></a>I.11 : Ne jamais transférer la propriété via un pointeur brut (`T*`) ou une référence (`T&`)

##### Raison

Si l’on doute de qui, de l’appelant ou du callee, possède l’objet, des fuites ou des destructions prématurées surviendront.

##### Exemple

    X* compute(args)    // don't
    {
        X* res = new X{};
        // ...
        return res;
    }

Qui supprime le `X` retourné ? Le problème serait plus difficile à repérer si `compute` retournait une référence.

Envisagez de retourner le résultat par valeur (en utilisant la sémantique de déplacement si le résultat est volumineux) :

    vector<double> compute(args)  // good
    {
        vector<double> res(10000);
        // ...
        return res;
    }

**Alternative** : [Passer la propriété](#rr-smartptrparam) à l’aide d’un « smart pointer », tel que `unique_ptr` (pour la propriété exclusive) et `shared_ptr` (pour la propriété partagée). Cependant, cela est moins élégant et souvent moins efficace que de retourner l’objet lui‑même, donc utilisez les smart pointers uniquement si la sémantique de référence est requise.

**Alternative** : parfois le code legacy ne peut pas être modifié à cause d’exigences de compatibilité d’ABI ou d’un manque de ressources. Dans ce cas, marquez les pointeurs propriétaires avec `owner` de la [bibliothèque de support des lignes directrices](#gsl-guidelines-support-library) :

    owner<X*> compute(args)    // It is now clear that ownership is transferred
    {
        owner<X*> res = new X{};
        // ...
        return res;
    }

Cela indique aux outils d’analyse que `res` est un propriétaire. Cela signifie que sa valeur doit être `delete`‑ée ou transférée à un autre propriétaire, comme le fait le `return`.

`owner` est utilisé de façon similaire dans l’implémentation des gestionnaires de ressources.

##### Note

Tout objet passé comme pointeur brut (ou itérateur) est supposé être possédé par l’appelant, de sorte que son cycle de vie soit géré par l’appelant. Autrement dit, les API qui transfèrent la propriété sont relativement rares comparées aux API qui ne font que passer des pointeurs, donc le défaut est « pas de transfert de propriété ».

**Voir aussi** : [Passage d’argument](#rf-conventional), [utilisation d’arguments smart‑pointer](#rr-smartptrparam) et [retour de valeur](#rf-value-return).

##### Application

* (Simple) Avertir lorsqu’on fait `delete` d’un pointeur brut qui n’est pas un `owner<T>`. Suggérer l’utilisation d’un gestionnaire de ressources de la bibliothèque standard ou de `owner<T>`.  
* (Simple) Avertir lorsqu’on ne fait ni `reset` ni `delete` explicite d’un pointeur `owner` sur chaque chemin d’exécution.  
* (Simple) Avertir si la valeur de retour de `new` ou d’une fonction renvoyant `owner` est assignée à un pointeur brut ou à une référence non `owner`.

### <a name="ri-nullptr"></a>I.12 : Déclarer un pointeur qui ne doit pas être nul comme `not_null`

##### Raison

Éviter les erreurs de déréférencement de `nullptr`. Améliorer les performances en évitant les vérifications redondantes de `nullptr`.

##### Exemple

    int length(const char* p);            // it is not clear whether length(nullptr) is valid
    length(nullptr);                      // OK?
    int length(not_null<const char*> p);  // better: we can assume that p cannot be nullptr
    int length(const char* p);            // we must assume that p can be nullptr

En indiquant l’intention dans le code source, les implémenteurs et les outils peuvent fournir de meilleurs diagnostics, comme la détection de certaines classes d’erreurs via l’analyse statique, et réaliser des optimisations, comme la suppression de branches et de tests de nullité.

##### Note

`not_null` est défini dans la [bibliothèque de support des lignes directrices](#gsl-guidelines-support-library).

##### Note

L’hypothèse que le pointeur `char` pointe vers une chaîne de style C (une chaîne terminée par zéro) était encore implicite, et source de confusion et d’erreurs. Utilisez `czstring` plutôt que `const char*`.

    // we can assume that p cannot be nullptr
    // we can assume that p points to a zero-terminated array of characters
    int length(not_null<czstring> p);

Note : `length()` est, bien sûr, `std::strlen()` déguisé.

##### Application

* (Simple) ((Foundation)) Si une fonction teste un paramètre pointeur contre `nullptr` avant tout accès, sur tous les chemins de contrôle, alors avertir qu’il devrait être déclaré `not_null`.  
* (Complexe) Si une fonction qui renvoie un pointeur assure qu’il n’est jamais `nullptr` sur tous les chemins de retour, alors avertir que le type de retour devrait être déclaré `not_null`.

### <a name="ri-array"></a>I.13 : Ne pas passer un tableau comme un seul pointeur

##### Raison

Les interfaces du style (pointeur, taille) sont sujettes à erreurs. De plus, un simple pointeur (vers un tableau) doit s’appuyer sur une convention pour que le callee détermine la taille.

##### Exemple

    void copy_n(const T* p, T* q, int n); // copy from [p:p+n) to [q:q+n)

Que se passe‑t‑il s’il y a moins de `n` éléments dans le tableau pointé par `q` ? On écraserait alors de la mémoire probablement non liée.  
Que se passe‑t‑il s’il y a moins de `n` éléments dans le tableau pointé par `p` ? On lirait alors de la mémoire probablement non liée.  
Dans les deux cas, le comportement est indéfini et peut provoquer de graves bugs.

##### Alternative

Utilisez des `span` explicites :

    void copy(span<const T> r, span<T> r2); // copy r to r2

##### Exemple, mauvais

    void draw(Shape* p, int n);  // poor interface; poor code
    Circle arr[10];
    /* ... */
    draw(arr, 10);

Passer `10` comme argument `n` peut être une erreur : la convention la plus courante suppose `[0:n)`, mais cela n’est déclaré nulle part. Pire, l’appel à `draw()` compile tout de même : il y a une conversion implicite du tableau vers un pointeur (décroissance de tableau) puis une conversion implicite de `Circle` vers `Shape`. `draw()` ne peut pas itérer en toute sécurité sur ce tableau : il n’a aucun moyen de connaître la taille des éléments.

**Alternative** : Utilisez une classe d’assistance qui garantit que le nombre d’éléments est correct et empêche les conversions implicites dangereuses. Par exemple :

    void draw2(span<Circle>);
    Circle arr[10];
    /* ... */
    draw2(span<Circle>(arr));  // deduce the number of elements
    draw2(arr);                // deduce the element type and array size

    void draw3(span<Shape>);
    draw3(arr);                // error: cannot convert Circle[10] to span<Shape>

`draw2()` passe la même quantité d’information à `draw()`, mais rend explicite le fait qu’il s’agit d’une plage de `Circle`. Voir ???.

##### Exception

Utilisez `zstring` et `czstring` pour représenter des chaînes C‑style zéro‑terminées. Mais dans ce cas, utilisez `std::string_view` ou `span<char>` du [GSL](#gsl-guidelines-support-library) afin d’éviter les erreurs de portée.

##### Application

* (Simple) ((Bounds)) Avertir toute expression qui s’appuierait sur la conversion implicite d’un type tableau vers un type pointeur. Autoriser les exceptions pour les types pointeur `zstring`/`czstring`.  
* (Simple) ((Bounds)) Avertir toute opération arithmétique sur une expression de type pointeur aboutissant à une valeur de type pointeur. Autoriser les exceptions pour `zstring`/`czstring`.

### <a name="ri-global-init"></a>I.22 : Éviter l’initialisation complexe d’objets globaux

##### Raison

Une initialisation complexe peut conduire à un ordre d’exécution indéfini.

##### Exemple


    // file1.c

    extern const X x;

    const Y y = f(x);   // read x; write y

    // file2.c

    extern const Y y;

    const X x = g(y);   // read y; write x

Comme `x` et `y` sont dans des unités de traduction différentes, l’ordre d’appels à `f()` et `g()` est indéfini ; l’un d’eux accédera à un `const` non initialisé. Cela montre que le problème d’ordre d’initialisation des objets globaux (portée namespace) ne se limite pas aux variables globales.

##### Note

Les problèmes d’ordre d’initialisation deviennent particulièrement difficiles à gérer dans le code concurrent. Il est généralement préférable d’éviter complètement les objets globaux (portée namespace).

##### Application

* Signaler les initialiseurs de globals qui appellent des fonctions non `constexpr`.  
* Signaler les initialiseurs de globals qui accèdent à des objets `extern`.

### <a name="ri-nargs"></a>I.23 : Limiter le nombre d’arguments de fonction

##### Raison

Un grand nombre d’arguments ouvre la porte à la confusion. Passer beaucoup d’arguments est souvent coûteux comparé à des alternatives.

##### Discussion

Les deux raisons les plus courantes pour lesquelles les fonctions ont trop de paramètres sont :

1. *Absence d’abstraction.*  
   Il manque une abstraction, de sorte qu’une valeur composée est passée sous forme d’éléments individuels plutôt que comme un objet unique qui impose un invariant. Cela augmente la liste des paramètres et entraîne des erreurs, puisque les valeurs composantes ne sont plus protégées par un invariant.

2. *Violation du principe « une fonction, une responsabilité ».*
   La fonction essaie de faire plus d’une chose et devrait probablement être refactorisée.

##### Exemple

L’interface de la bibliothèque standard `merge()` est à la limite du raisonnable :

    template<class InputIterator1, class InputIterator2, class OutputIterator, class Compare>
    OutputIterator merge(InputIterator1 first1, InputIterator1 last1,
                         InputIterator2 first2, InputIterator2 last2,
                         OutputIterator result, Compare comp);

C’est dû au problème 1 ci‑dessus – absence d’abstraction. Au lieu de passer une plage (abstraction), la STL passe des paires d’itérateurs (valeurs non encapsulées).

Nous avons ici quatre paramètres de modèle et six paramètres de fonction. Pour simplifier les usages les plus fréquents et les plus simples, l’argument de comparaison peut être donné par défaut à `<` :

    template<class InputIterator1, class InputIterator2, class OutputIterator>
    OutputIterator merge(InputIterator1 first1, InputIterator1 last1,
                         InputIterator2 first2, InputIterator2 last2,
                         OutputIterator result);

Cela ne réduit pas la complexité totale, mais diminue la complexité apparente présentée à de nombreux utilisateurs.  
Pour réellement réduire le nombre d’arguments, il faut regrouper les arguments dans des abstractions de plus haut niveau :

    template<class InputRange1, class InputRange2, class OutputIterator>
    OutputIterator merge(InputRange1 r1, InputRange2 r2, OutputIterator result);

Regrouper les arguments en « bundles » est une technique générale pour réduire le nombre d’arguments et augmenter les possibilités de vérification.

On pourrait également utiliser un concept de la bibliothèque standard pour définir la notion de trois types utilisables pour la fusion :

    template<class In1, class In2, class Out>
      requires mergeable<In1, In2, Out>
    Out merge(In1 r1, In2 r2, Out result);

##### Exemple

Les profils de sécurité recommandent de remplacer :

    void f(int* some_ints, int some_ints_length);  // BAD: C style, unsafe

par :

    void f(gsl::span<int> some_ints);              // GOOD: safe, bounds-checked

En utilisant une abstraction, on obtient des bénéfices de sécurité et de robustesse, et on réduit naturellement le nombre de paramètres.

##### Note

Combien de paramètres est‑t‑on prêt à tolérer ? Essayez d’utiliser moins de quatre (4) paramètres. Certaines fonctions sont mieux exprimées avec quatre paramètres individuels, mais ce n’est pas fréquent.

**Alternative** : Utilisez une meilleure abstraction : regroupez les arguments dans des objets significatifs et passez les objets (par valeur ou par référence).

**Alternative** : Utilisez des arguments par défaut ou des surcharges afin que les formes d’appel les plus courantes puissent être réalisées avec moins d’arguments.

##### Application

* Avertir lorsqu’une fonction déclare deux itérateurs (y compris des pointeurs) du même type au lieu d’une plage ou d’une vue.  
* (Not enforceable) Cette règle est philosophique et impossible à vérifier directement.

### <a name="ri-unrelated"></a>I.24 : Éviter des paramètres adjacents qui peuvent être invoqués avec les mêmes arguments dans n’importe quel ordre avec un sens différent

##### Raison

Des arguments adjacents du même type peuvent être intervertis par erreur.

##### Exemple, mauvais

    void copy_n(T* p, T* q, int n);  // copy from [p:p + n) to [q:q + n)

C’est une variante peu recommandée d’une interface style K&R C. Il est facile d’inverser les arguments « de » et « vers ».

Utilisez `const` pour l’argument « de » :

    void copy_n(const T* p, T* q, int n);  // copy from [p:p + n) to [q:q + n)

##### Exception

Si l’ordre des paramètres n’a aucune importance, il n’y a pas de problème :

    int max(int a, int b);

##### Alternative

Ne pas passer des tableaux comme pointeurs, mais passer un objet représentant une plage (par ex., un `span`) :

    void copy_n(span<const T> p, span<T> q);  // copy from p to q


##### Alternative

Définissez une `struct` comme type de paramètre et nommez les champs en conséquence :

    struct SystemParams {
        string config_file;
        string output_path;
        seconds timeout;
    };
    void initialize(SystemParams p);

Cela rend les appels plus clairs, car les paramètres sont souvent remplis par nom sur le site d’appel.

##### Note

Seul le concepteur de l’interface peut répondre adéquatement aux sources de violations de cette ligne directrice.

##### Stratégie d’application

(Simple) Avertir si deux paramètres consécutifs partagent le même type.

Nous recherchons encore une stratégie d’application moins simple.

### <a name="ri-abstract"></a>I.25 : Privilégier les classes abstraites vides comme interfaces aux hiérarchies de classes

##### Raison

Les classes abstraites vides (sans membres non‑statiques) sont plus susceptibles d’être stables que les classes de base contenant un état.

##### Exemple, mauvais

Vous avez simplement deviné que `Shape` apparaîtrait quelque part :-)

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

Cela force chaque classe dérivée à calculer un centre – même si cela est non trivial et que le centre n’est jamais utilisé. De même, toutes les formes n’ont pas forcément de couleur, et de nombreuses formes sont mieux représentées sans un contour défini comme une séquence de `Point`. Utiliser une classe abstraite est préférable :

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

(Simple) Avertir lorsqu’un pointeur/référence à une classe `C` est assigné à un pointeur/référence à une base de `C` dont la classe de base possède des membres de données.

### <a name="ri-abi"></a>I.26 : Si vous voulez une ABI inter‑compilateur, utilisez un sous‑ensemble de style C

##### Raison

Différents compilateurs implémentent des mises en page binaires différentes pour les classes, la gestion des exceptions, les noms de fonctions et d’autres détails d’implémentation.

##### Exception

Des ABI communes émergent sur certaines plateformes, vous libérant ainsi des restrictions plus draconiennes.

##### Note

Si vous n’utilisez qu’un seul compilateur, vous pouvez employer le C++ complet dans les interfaces. Cela peut nécessiter une recompilation après une mise à jour vers une nouvelle version du compilateur.

##### Application

(Not enforceable) Il est difficile d’identifier de façon fiable où une interface fait partie d’une ABI.

### <a name="ri-pimpl"></a>I.27 : Pour une ABI stable de bibliothèque, envisagez le idiome Pimpl

##### Raison

Étant donné que les membres de données privés participent à la mise en page de la classe et que les fonctions membres privées participent à la résolution des surcharges, toute modification de ces détails d’implémentation oblige à recompilation de tous les utilisateurs de la classe. Une interface non polymorphe contenant un pointeur vers une implémentation (`Pimpl`) peut isoler les utilisateurs d’une classe des changements internes, au prix d’une indirection.

##### Exemple

**interface (widget.h)**

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

**implémentation (widget.cpp)**

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

Voir [GOTW #100](https://herbsutter.com/gotw/_100/) et la page [cppreference sur le Pimpl](https://en.cppreference.com/w/cpp/language/pimpl) pour les compromis et les détails d’implémentation associés à cet idiome.

##### Application

(Not enforceable) Il est difficile d’identifier de façon fiable où une interface constitue une partie d’une ABI.

### <a name="ri-encapsulate"></a>I.30 : Encapsuler les violations de règle

##### Raison

Maintenir le code simple et sûr.  
Parfois, des techniques laides, dangereuses ou sujettes aux erreurs sont nécessaires pour des raisons logiques ou de performance. Si tel est le cas, gardez‑les locales plutôt que de « contaminer » les interfaces, afin que de plus grands groupes de programmeurs n’aient pas à connaître les subtilités. La complexité d’implémentation ne doit, si possible, pas se propager aux utilisateurs via les interfaces.

##### Exemple

Considérez un programme qui, selon une forme d’entrée (par ex. les arguments de `main`), doit lire depuis un fichier, depuis la ligne de commande ou depuis l’entrée standard. On pourrait écrire :

    bool owned;
    owner<istream*> inp;
    switch (source) {
    case std_in:        owned = false; inp = &cin;                       break;
    case command_line:  owned = true;  inp = new istringstream{argv[2]}; break;
    case file:          owned = true;  inp = new ifstream{argv[2]};      break;
    }
    istream& in = *inp;

Cela viole la règle [contre les variables non initialisées](#res-always), la règle contre [l’ignorance de la propriété](#ri-raw), et la règle [contre les constantes magiques](#res-magic). En particulier, quelqu’un doit se souvenir d’écrire quelque part :

    if (owned) delete inp;

On pourrait gérer cet exemple particulier en utilisant `unique_ptr` avec un destructeur spécial qui ne fait rien pour `cin`, mais cela reste compliqué pour les novices (qui peuvent facilement rencontrer ce problème) et l’exemple illustre un problème plus général où une propriété que nous aimerions considérer statique (ici, la propriété) doit parfois être traitée à l’exécution. Les cas les plus fréquents et les plus sûrs peuvent être gérés statiquement, donc nous ne voulons pas ajouter de coût et de complexité à ceux‑ci. Mais nous devons aussi prendre en compte les cas rares, moins sûrs, et nécessairement plus coûteux. Ces exemples sont discutés dans [[Str15]](https://www.stroustrup.com/resource-model.pdf).

Nous écrivons alors une classe :

    class Istream { [[gsl::suppress("lifetime")]]
    public:
        enum Opt { from_line = 1 };
        Istream() { }
        Istream(czstring p) : owned{true}, inp{new ifstream{p}} {}            // read from file
        Istream(czstring p, Opt) : owned{true}, inp{new istringstream{p}} {}  // read from the command line
        ~Istream() { if (owned) delete inp; }
        operator istream&() { return *inp; }
    private:
        bool owned = false;
        istream* inp = &cin;
    };

Ainsi, la nature dynamique de la propriété `istream` a été encapsulée. En pratique, on ajouterait naturellement des contrôles d’erreurs supplémentaires.

##### Application

* Difficile : il est ardu de décider quels morceaux de code qui violent les règles sont indispensables.  
* Signaler les suppressions de règles qui permettent aux violations de traverser les interfaces.