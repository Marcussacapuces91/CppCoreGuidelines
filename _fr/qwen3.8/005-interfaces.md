# <a name="s-interfaces"></a>I: Interfaces

Une interface est un contrat entre deux parties d'un programme. Définir précisément ce qui est attendu d'un fournisseur de service et de son utilisateur est essentiel.
Disposer de bonnes interfaces (faciles à comprendre, encourageant un usage efficace, sans risque d'erreur, favorisant les tests, etc.) est probablement l'aspect le plus important de l'organisation du code.

Résumé des règles sur les interfaces :

* [I.1: Rendre les interfaces explicites](005-interfaces.md#ri-explicit)
* [I.2: Éviter les variables globales non `const`](005-interfaces.md#ri-global)
* [I.3: Éviter les singletons](005-interfaces.md#ri-singleton)
* [I.4: Rendre les interfaces précisément et fortement typées](005-interfaces.md#ri-typed)
* [I.5: Énoncer les préconditions (le cas échéant)](005-interfaces.md#ri-pre)
* [I.6: Privilégier `Expects()` pour exprimer les préconditions](005-interfaces.md#ri-expects)
* [I.7: Énoncer les postconditions](005-interfaces.md#ri-post)
* [I.8: Privilégier `Ensures()` pour exprimer les postconditions](005-interfaces.md#ri-ensures)
* [I.9: Si une interface est un modèle, documenter ses paramètres au moyen de concepts](005-interfaces.md#ri-concepts)
* [I.10: Utiliser les exceptions pour signaler l'échec d'une tâche requise](005-interfaces.md#ri-except)
* [I.11: Ne jamais transférer la propriété par un pointeur brut (`T*`) ou une référence (`T&`)](005-interfaces.md#ri-raw)
* [I.12: Déclarer un pointeur qui ne doit pas être nul comme `not_null`](005-interfaces.md#ri-nullptr)
* [I.13: Ne pas passer un tableau en tant que simple pointeur](005-interfaces.md#ri-array)
* [I.22: Éviter les initialisations complexes d'objets globaux](005-interfaces.md#ri-global-init)
* [I.23: Garder le nombre de paramètres de fonction bas](005-interfaces.md#ri-nargs)
* [I.24: Éviter des paramètres adjacents qui peuvent être intervertis sans changer l'appel mais avec un sens différent](005-interfaces.md#ri-unrelated)
* [I.25: Privilégier les classes abstraites vides comme interfaces plutôt que des hiérarchies de classes](005-interfaces.md#ri-abstract)
* [I.26: Si vous souhaitez une ABI compatible entre compilateurs, utiliser un sous-ensemble de style C](005-interfaces.md#ri-abi)
* [I.27: Pour une ABI de bibliothèque stable, envisager l'idiome Pimpl](005-interfaces.md#ri-pimpl)
* [I.30: Encapsuler les violations de règles](005-interfaces.md#ri-encapsulate)

**Voir aussi** :

* [F: Fonctions](006-functions.md)
* [C.concrete: Types concrets](007-class.md#ss-concrete)
* [C.hier: Hiérarchies de classes](007-class.md#ss-hier)
* [C.over: Surcharge et opérateurs surchargés](007-class.md#ss-overload)
* [C.con: Conteneurs et autres gestionnaires de ressources](007-class.md#ss-containers)
* [E: Gestion des erreurs](013-errors.md)
* [T: Modèles et programmation générique](015-templates.md)

### <a name="ri-explicit"></a>I.1: Rendre les interfaces explicites

##### Raison

Exactitude. Les hypothèses non explicitées dans une interface sont facilement négligées et difficiles à tester.

##### Exemple, mauvais

Contrôler le comportement d'une fonction via une variable globale (portée de namespace) (un mode d'appel) est implicite et potentiellement source de confusion. Par exemple :

    int round(double d)
    {
        return (round_up) ? ceil(d) : d;    // à éviter : dépendance « invisible »
    }

Il ne sera pas évident pour l'appelant que deux appels de `round(7.2)` pourraient donner des résultats différents.

##### Exception

Parfois, nous contrôlons certains détails d'un ensemble d'opérations via une variable d'environnement, par exemple une sortie normale ou verbale, ou un mode de débogage ou optimisé.
L'usage d'un contrôle non local est potentiellement source de confusion, mais ne contrôle que des détails d'implémentation d'une sémantique par ailleurs fixe.

##### Exemple, mauvais

Rapporter via des variables non locales (par exemple `errno`) est facilement ignoré. Par exemple :

    // à éviter : absence de test de la valeur de retour de fprintf
    fprintf(connection, "journalisation : %d %d %d\n", x, y, s);

Et si la connexion est rompue, si bien qu'aucune sortie de journalisation n'est produite ? Voir I.??? @TODO-LINK.

**Alternative** : Lever une exception. Une exception ne peut pas être ignorée.

**Formulation alternative** : Éviter de transmettre de l'information à travers une interface via un état non local ou implicite.
Notez que les fonctions membres non-`const` transmettent de l'information à d'autres fonctions membres via l'état de l'objet.

**Formulation alternative** : Une interface doit être une fonction ou un ensemble de fonctions.
Les fonctions peuvent être des modèles de fonction, et un ensemble de fonctions peut être une classe ou un modèle de classe.

##### Application

* (Simple) Une fonction ne doit pas prendre de décisions de flux de contrôle sur la base de valeurs de variables déclarées en portée de namespace.
* (Simple) Une fonction ne doit pas écrire dans des variables déclarées en portée de namespace.

### <a name="ri-global"></a>I.2: Éviter les variables globales non `const`

##### Raison

Les variables globales non `const` masquent les dépendances et les rendent sujettes à des modifications imprévisibles.

##### Exemple

    struct Data {
        // ... beaucoup de choses ...
    } data;            // data non const

    void compute()     // à éviter
    {
        // ... utilisation de data ...
    }

    void output()     // à éviter
    {
        // ... utilisation de data ...
    }

Qui d'autre pourrait modifier `data` ?

**Avertissement** : L'initialisation des objets globaux n'est pas totalement ordonnée.
Si vous utilisez un objet global, initialisez-le avec une constante.
Notez qu'il est possible d'obtenir un ordre d'initialisation indéfini même pour des objets `const`.

##### Exception

Un objet global est souvent préférable à un singleton.

##### Note

Les constantes globales sont utiles.

##### Note

La règle contre les variables globales s'applique également aux variables en portée de namespace.

**Alternative** : Si vous utilisez des données globales (plus généralement en portée de namespace) pour éviter la copie, envisagez de passer ces données par référence à un `const`.
Une autre solution consiste à définir les données comme l'état d'un objet et les opérations comme des fonctions membres.

**Avertissement** : Méfiez-vous des conflits de données : si un thread peut accéder à des données non locales (ou passées par référence) pendant qu'un autre thread exécute l'appelé, un conflit de données peut survenir.
Chaque pointeur ou référence vers des données mutables est un conflit de données potentiel.

L'usage de pointeurs globaux ou de références pour accéder et modifier des données non const, et par ailleurs non globales,
n'est pas une meilleure alternative aux variables globales non const, car cela ne résout pas les problèmes de dépendances masquées ni de conditions de concurrence potentielles.

##### Note

Il ne peut pas y avoir de conflit de données sur des données immuables.

**Références** : Voir les [règles sur l'appel de fonctions](006-functions.md#ss-call).

##### Note

La règle est « éviter », pas « ne pas utiliser ». Il y aura bien sûr des (rares) exceptions, telles que `cin`, `cout` et `cerr`.

##### Application

(Simple) Signaler toutes les variables non `const` déclarées en portée de namespace et les pointeurs/références globaux vers des données non const.


### <a name="ri-singleton"></a>I.3: Éviter les singletons

##### Raison

Les singletons sont essentiellement des objets globaux compliqués déguisés.

##### Exemple

    class Singleton {
        // ... beaucoup de choses pour s'assurer qu'un seul objet Singleton est créé,
        // qu'il est initialisé correctement, etc.
    };

Il existe de nombreuses variantes de l'idée du singleton.
C'est en partie le problème.

##### Note

Si vous ne voulez pas qu'un objet global change, déclarez-le `const` ou `constexpr`.

##### Exception

Vous pouvez utiliser le « singleton » le plus simple (si simple qu'il n'est souvent pas considéré comme un singleton) pour obtenir une initialisation à la première utilisation, le cas échéant :

    X& myX()
    {
        static X my_x {3};
        return my_x;
    }

C'est l'une des solutions les plus efficaces aux problèmes liés à l'ordre d'initialisation.
Dans un environnement multithreadé, l'initialisation de l'objet statique n'introduit pas de conflit de données
(sauf si vous accédez imprudemment à un objet partagé depuis son constructeur).

Notez que l'initialisation d'un `static` local n'implique pas de conflit de données.
Cependant, si la destruction de `X` implique une opération qui doit être synchronisée, nous devons utiliser une solution moins simple.
Par exemple :

    X& myX()
    {
        static auto p = new X {3};
        return *p;  // fuite potentielle
    }

Là, quelqu'un doit `delete` cet objet d'une manière convenablement sûre pour le multithreading.
C'est source d'erreurs, donc nous n'utilisons cette technique que si :

* `myX` est dans du code multithreadé,
* cet objet `X` doit être détruit (par exemple parce qu'il libère une ressource), et
* le code du destructeur de `X` doit être synchronisé.

Si, comme beaucoup, vous définissez un singleton comme une classe pour laquelle un seul objet est créé, des fonctions comme `myX` ne sont pas des singletons, et cette technique utile n'est pas une exception à la règle anti-singleton.

##### Application

Très difficile en général.

* Rechercher des classes dont le nom contient `singleton`.
* Rechercher des classes pour lesquelles un seul objet est créé (en comptant les objets ou en examinant les constructeurs).
* Si une classe X a une fonction statique publique contenant un statique local de la classe X et renvoyant un pointeur ou une référence vers celui-ci, l'interdire.

### <a name="ri-typed"></a>I.4: Rendre les interfaces précisément et fortement typées

##### Raison

Les types sont la documentation la plus simple et la meilleure, améliorent la lisibilité grâce à leur signification bien définie, et sont vérifiées à la compilation.
De plus, un code précisément typé est souvent mieux optimisé.

##### Exemple, à éviter

Considérez :

    void pass(void* data);    // type faible et sous-qualifié void* est suspect

Les appelants ne sont pas sûrs des types autorisés ni si les données peuvent être modifiées, car `const` n'est pas spécifié. Notez que tous les types de pointeurs
sont convertis implicitement en `void*`, si bien qu'il est facile pour les appelants de fournir cette valeur.

L'appelé doit faire un `static_cast` des données vers un type non vérifié pour les utiliser.
Cela est source d'erreurs et verbeux.

N'utilisez `const void*` que pour passer des données dans des conceptions qui ne peuvent pas être décrites en C++. Envisagez plutôt d'utiliser un `variant` ou un pointeur vers une classe de base.

**Alternative** : Souvent, un paramètre de modèle peut éliminer le `void*` et le transformer en `T*` ou `T&`.
Pour du code générique, ces `T` peuvent être des paramètres de modèle généraux ou contraints par un concept.

##### Exemple, mauvais

Considérez :

    draw_rect(100, 200, 100, 500); // que spécifient ces nombres ?

    draw_rect(p.x, p.y, 10, 20); // dans quelles unités sont 10 et 20 ?

Il est clair que l'appelant décrit un rectangle, mais il est flou quels éléments ces valeurs représentent. De plus, un `int` peut contenir toute forme d'information, y compris des valeurs dans de nombreuses unités, donc nous devons deviner le sens des quatre `int`. Le plus probable, c'est que les deux premiers sont un couple de coordonnées `x`, `y`, mais quels sont les deux derniers ?

Les commentaires et les noms de paramètres peuvent aider, mais nous pouvons être explicites :

    void draw_rectangle(Point top_left, Point bottom_right);
    void draw_rectangle(Point top_left, Size height_width);

    draw_rectangle(p, Point{10, 20});  // deux coins
    draw_rectangle(p, Size{10, 20});   // un coin et un couple (hauteur, largeur)

Évidemment, nous ne pouvons pas capturer toutes les erreurs via le système de types statique
(par exemple, le fait qu'un premier argument est censé être un coin supérieur gauche est laissé à la convention (nommage et commentaires)).

##### Exemple, mauvais

Considérez :

    set_settings(true, false, 42); // que spécifient ces valeurs ?

Les types de paramètres et leurs valeurs ne communiquent pas quelles réglages sont spécifiés ni ce que ces valeurs signifient.

Cette conception est plus explicite, sûre et lisible :

    alarm_settings s{};
    s.enabled = true;
    s.displayMode = alarm_settings::mode::spinning_light;
    s.frequency = alarm_settings::every_10_seconds;
    set_settings(s);

Dans le cas d'un ensemble de valeurs booléennes, envisagez d'utiliser un `enum` de drapeaux ; un motif qui exprime un ensemble de valeurs booléennes.

    enable_lamp_options(lamp_option::on | lamp_option::animate_state_transitions);

##### Exemple, mauvais

Dans l'exemple suivant, il n'est pas clair depuis l'interface ce que signifie `time_to_blink` : des secondes ? des millisecondes ?

    void blink_led(int time_to_blink) // mauvais -- l'unité est ambiguë
    {
        // ...
        // faire quelque chose avec time_to_blink
        // ...
    }

    void use()
    {
        blink_led(2);
    }

##### Exemple, bon

Les types `std::chrono::duration` aident à rendre l'unité de durée de temps explicite.

    void blink_led(milliseconds time_to_blink) // bon -- l'unité est explicite
    {
        // ...
        // faire quelque chose avec time_to_blink
        // ...
    }

    void use()
    {
        blink_led(1500ms);
    }

La fonction peut également être écrite de manière à accepter n'importe quelle unité de durée de temps.

    template<class rep, class period>
    void blink_led(duration<rep, period> time_to_blink) // bon -- accepte n'importe quelle unité
    {
        // en supposant que la milliseconde est la plus petite unité pertinente
        auto milliseconds_to_blink = duration_cast<milliseconds>(time_to_blink);
        // ...
        // faire quelque chose avec milliseconds_to_blink
        // ...
    }

    void use()
    {
        blink_led(2s);
        blink_led(1500ms);
    }

##### Application

* (Simple) Signaler l'usage de `void*` comme paramètre ou type de retour.
* (Simple) Signaler l'usage de plus d'un paramètre `bool`.
* (Difficile à bien faire) Rechercher des fonctions utilisant trop de paramètres de types primitifs.

### <a name="ri-pre"></a>I.5: Énoncer les préconditions (le cas échéant)

##### Raison

Les arguments ont une signification qui peut contraindre leur usage correct dans l'appelé.

##### Exemple

Considérez :

    double sqrt(double x);

Ici `x` doit être non négatif. Le système de types ne peut pas (facilement et naturellement) l'exprimer, donc nous devons utiliser d'autres moyens. Par exemple :

    double sqrt(double x); // x doit être non négatif

Certaines préconditions peuvent être exprimées comme des assertions. Par exemple :

    double sqrt(double x) { Expects(x >= 0); /* ... */ }

Idéalement, cette `Expects(x >= 0)` devrait faire partie de l'interface de `sqrt()`, mais ce n'est pas facile à faire. Pour l'instant, nous la plaçons dans la définition (corps de la fonction).

**Références** : `Expects()` est décrite dans [GSL](#gsl-guidelines-support-library) @TODO-LINK.

##### Note

Privilégiez une spécification formelle des exigences, telle que `Expects(p);`.
Si cela est irréalisable, utilisez du texte en anglais dans des commentaires, tel que `// la séquence [p:q) est ordonnée avec <`.

##### Note

La plupart des fonctions membres ont comme précondition qu'une invariant de la classe tient.
Cette invariant est établie par un constructeur et doit être rétablie à la sortie par chaque fonction membre appelée depuis l'extérieur de la classe.
Nous n'avons pas besoin de la mentionner pour chaque fonction membre.

##### Application

(Non applicable)

**Voir aussi** : Les règles sur le passage de pointeurs. ???

### <a name="ri-expects"></a>I.6: Privilégier `Expects()` pour exprimer les préconditions

##### Raison

Pour rendre clair que la condition est une précondition et pour permettre l'usage d'outils.

##### Exemple

    int area(int height, int width)
    {
        Expects(height > 0 && width > 0);            // bon
        if (height <= 0 || width <= 0) my_error();   // obscur
        // ...
    }

##### Note

Les préconditions peuvent être exprimées de nombreuses façons, y compris des commentaires, des instructions `if`, et `assert()`.
Cela peut les rendre difficiles à distinguer du code ordinaire, difficiles à mettre à jour, difficiles à manipuler par des outils, et peut avoir une sémantique incorrecte (souhaitez-vous toujours interrompre en mode débogage et ne rien vérifier en production ?).

##### Note

Les préconditions devraient faire partie de l'interface plutôt que de l'implémentation,
mais nous n'avons pas encore les mécanismes de langage pour le faire.
Dès que le support du langage deviendra disponible (par exemple, voir la [proposition de contrat](https://www.open-std.org/jtc1/sc22/wg21/docs/papers/2016/p0380r1.pdf)), nous adopterons la version standard des préconditions, postconditions et assertions.

##### Note

`Expects()` peut également être utilisée pour vérifier une condition au milieu d'un algorithme.

##### Note

Non, utiliser `unsigned` n'est pas un bon moyen de contourner le problème de [garantir qu'une valeur est non négative](010-expr.md#res-nonnegative).

##### Application

(Non applicable) Trouver la variété des façons dont les préconditions peuvent être assertées n'est pas réalisable. Signaler celles qui peuvent être facilement identifiées (`assert()`) a une valeur discutable en l'absence d'un mécanisme de langage.

### <a name="ri-post"></a>I.7: Énoncer les postconditions

##### Raison

Pour détecter les malentendus sur le résultat et éventuellement capturer des implémentations erronées.

##### Exemple, mauvais

Considérez :

    int area(int height, int width) { return height * width; }  // mauvais

Ici, nous avons (imprudemment) omis la spécification de la précondition, si bien qu'il n'est pas explicite que hauteur et largeur doivent être positives.
Nous avons également omis la spécification de la postcondition, si bien qu'il n'est pas évident que l'algorithme (`height * width`) est incorrect pour des aires supérieures à l'entier maximal.
Un débordement peut survenir.
Envisagez d'utiliser :

    int area(int height, int width)
    {
        auto res = height * width;
        Ensures(res > 0);
        return res;
    }

##### Exemple, mauvais

Considérez un célèbre bug de sécurité :

    void f()    // problématique
    {
        char buffer[MAX];
        // ...
        memset(buffer, 0, sizeof(buffer));
    }

Il n'y avait pas de postcondition déclarant que le tampon doit être effacé, et l'optimiseur a éliminé l'appel apparemment redondant à `memset()` :

    void f()    // mieux
    {
        char buffer[MAX];
        // ...
        memset(buffer, 0, sizeof(buffer));
        Ensures(buffer[0] == 0);
    }

##### Note

Les postconditions sont souvent informellement exprimées dans un commentaire qui énonce le but d'une fonction ; `Ensures()` peut être utilisé pour rendre cela plus systématique, visible et vérifiable.

##### Note

Les postconditions sont particulièrement importantes quand elles portent sur quelque chose qui n'est pas directement reflété dans un résultat renvoyé, comme un état d'une structure de données utilisée.

##### Exemple

Considérez une fonction qui manipule un `Record`, utilisant un `mutex` pour éviter les conflits de données :

    mutex m;

    void manipulate(Record& r)    // à éviter
    {
        m.lock();
        // ... pas de m.unlock() ...
    }

Ici, nous avons « oublié » de déclarer que le `mutex` doit être libéré, si bien que nous ne savons pas si l'échec à garantir la libération du `mutex` était un bug ou une fonctionnalité.
Énoncer la postcondition aurait rendu cela clair :

    void manipulate(Record& r)    // postcondition : m est déverrouillé à la sortie
    {
        m.lock();
        // ... pas de m.unlock() ...
    }

Le bug est maintenant évident (mais uniquement pour un humain lisant les commentaires).

Mieux encore, utilisez [RAII](009-resource.md#rr-raii) pour garantir que la postcondition (« le verrou doit être libéré ») est appliquée dans le code :

    void manipulate(Record& r)    // meilleur
    {
        lock_guard<mutex> _ {m};
        // ...
    }

##### Note

Idéalement, les postconditions sont énoncées dans l'interface/déclaration pour que les utilisateurs puissent facilement les voir.
Seules les postconditions liées aux utilisateurs peuvent être énoncées dans l'interface.
Les postconditions liées uniquement à l'état interne appartiennent à la définition/implémentation.

##### Application

(Non applicable) C'est une ligne directrice philosophique qui est irréalisable à vérifier
directement dans le cas général. Des vérificateurs spécifiques au domaine (comme les vérificateurs de
verrouillage) existent pour de nombreuses chaînes d'outils.

### <a name="ri-ensures"></a>I.8: Privilégier `Ensures()` pour exprimer les postconditions

##### Raison

Pour rendre clair que la condition est une postcondition et pour permettre l'usage d'outils.

##### Exemple

    void f()
    {
        char buffer[MAX];
        // ...
        memset(buffer, 0, MAX);
        Ensures(buffer[0] == 0);
    }

##### Note

Les postconditions peuvent être exprimées de nombreuses façons, y compris des commentaires, des instructions `if`, et `assert()`.
Cela peut les rendre difficiles à distinguer du code ordinaire, difficiles à mettre à jour, difficiles à manipuler par des outils, et peut avoir une sémantique incorrecte.

**Alternative** : Les postconditions de la forme « cette ressource doit être libérée » sont le mieux exprimées par [RAII](009-resource.md#rr-raii).

##### Note

Idéalement, cette `Ensures` devrait faire partie de l'interface, mais ce n'est pas facile à faire.
Pour l'instant, nous la plaçons dans la définition (corps de la fonction).
Dès que le support du langage deviendra disponible (par exemple, voir la [proposition de contrat](https://www.open-std.org/jtc1/sc22/wg21/docs/papers/2016/p0380r1.pdf)), nous adopterons la version standard des préconditions, postconditions et assertions.

##### Application

(Non applicable) Trouver la variété des façons dont les postconditions peuvent être assertées n'est pas réalisable. Signaler celles qui peuvent être facilement identifiées (`assert()`) a une valeur discutable en l'absence d'un mécanisme de langage.

### <a name="ri-concepts"></a>I.9: Si une interface est un modèle, documenter ses paramètres au moyen de concepts

##### Raison

Rendre l'interface précisément spécifiée et vérifiable à la compilation dans l'avenir (pas si lointain).

##### Exemple

Utiliser le style C++20 de spécification des exigences. Par exemple :

    template<typename Iter, typename Val>
      requires input_iterator<Iter> && equality_comparable_with<iter_value_t<Iter>, Val>
    Iter find(Iter first, Iter last, Val v)
    {
        // ...
    }

**Voir aussi** : [Programmation générique](015-templates.md#ss-gp) et [concepts](015-templates.md#ss-concepts).

##### Application

Émettre un avertissement si un paramètre de modèle non variadique n'est pas contraint par un concept (dans sa déclaration ou mentionné dans une clause `requires`).

### <a name="ri-except"></a>I.10: Utiliser les exceptions pour signaler l'échec d'une tâche requise

##### Raison

Il ne devrait pas être possible d'ignorer une erreur, car cela pourrait laisser le système ou un calcul dans un état indéfini (ou inattendu).
C'est une source majeure d'erreurs.

##### Exemple

    int printf(const char* ...);    // mauvais : renvoyer un nombre négatif si la sortie échoue

    template<class F, class ...Args>
    // bon : lever system_error si impossible de démarrer le nouveau thread
    explicit thread(F&& f, Args&&... args);

##### Note

Qu'est-ce qu'une erreur ?

Une erreur signifie que la fonction ne peut pas atteindre son but annoncé (y compris l'établissement des postconditions).
Du code appelant qui ignore une erreur peut conduire à des résultats incorrects ou à un état système indéfini.
Par exemple, ne pas pouvoir se connecter à un serveur distant n'est pas en soi une erreur :
le serveur peut refuser une connexion pour toutes sortes de raisons, donc la chose naturelle est de renvoyer un résultat que l'appelant doit toujours vérifier.
Cependant, si l'échec de la connexion est considéré comme une erreur, alors l'échec devrait lever une exception.

##### Exception

De nombreuses fonctions d'interface traditionnelles (par exemple les gestionnaires de signaux UNIX) utilisent des codes d'erreur (par exemple `errno`) pour rapporter ce qui sont en réalité des codes de statut, plutôt que des erreurs. Vous n'avez pas de bonne alternative à leur utilisation, donc les appeler ne viole pas la règle.

##### Alternative

Si vous ne pouvez pas utiliser les exceptions (par exemple parce que votre code regorge d'usages de pointeurs bruts de l'ancien style ou parce qu'il y a des contraintes temps réel strictes), envisagez d'utiliser un style qui renvoie un couple de valeurs :

    int val;
    int error_code;
    tie(val, error_code) = do_something();
    if (error_code) {
        // ... gérer l'erreur ou quitter ...
    }
    // ... utiliser val ...

Ce style conduit malheureusement à des variables non initialisées.
Depuis C++17, la fonctionnalité des « liaisons structurées » peut être utilisée pour initialiser directement les variables à partir de la valeur de retour :

    auto [val, error_code] = do_something();
    if (error_code) {
        // ... gérer l'erreur ou quitter ...
    }
    // ... utiliser val ...

##### Note

Nous ne considérons pas la « performance » comme une raison valide de ne pas utiliser les exceptions.

* Souvent, la vérification et le traitement explicites des erreurs consomment autant de temps et d'espace que le traitement des exceptions.
* Souvent, un code plus propre donne de meilleures performances avec les exceptions (en simplifiant le traçage des chemins à travers le programme et leur optimisation).
* Une bonne règle pour le code sensible aux performances est de déplacer la vérification en dehors de la partie [critique](011-performance.md#rper-critical) du code.
* À plus long terme, un code plus régulier est mieux optimisé.
* Toujours [mesurer](011-performance.md#rper-measure) soigneusement avant de faire des affirmations sur les performances.

**Voir aussi** : [I.5](005-interfaces.md#ri-pre) et [I.7](005-interfaces.md#ri-post) pour le signalement des violations de préconditions et postconditions.

##### Application

* (Non applicable) C'est une ligne directrice philosophique qui est irréalisable à vérifier directement.
* Rechercher `errno`.

### <a name="ri-raw"></a>I.11: Ne jamais transférer la propriété par un pointeur brut (`T*`) ou une référence (`T&`)

##### Raison

S'il y a le moindre doute sur le fait que l'appelant ou l'appelé possède l'objet, des fuites ou des destructions prématurées se produiront.

##### Exemple

Considérez :

    X* compute(args)    // à éviter
    {
        X* res = new X{};
        // ...
        return res;
    }

Qui supprime le `X` renvoyé ? Le problème serait plus difficile à repérer si `compute` renvoyait une référence.
Envisagez de renvoyer le résultat par valeur (utiliser la sémantique de déplacement si le résultat est volumineux) :

    vector<double> compute(args)  // bon
    {
        vector<double> res(10000);
        // ...
        return res;
    }

**Alternative** : [Transférer la propriété](009-resource.md#rr-smartptrparam) en utilisant un « pointeur intelligent », tel que `unique_ptr` (pour une propriété exclusive) et `shared_ptr` (pour une propriété partagée).
Cependant, c'est moins élégant et souvent moins efficace que de renvoyer l'objet lui-même,
donc n'utilisez des pointeurs intelligents que si la sémantique de référence est nécessaire.

**Alternative** : Parfois, un ancien code ne peut pas être modifié en raison de contraintes de compatibilité ABI ou d'un manque de ressources.
Dans ce cas, marquez les pointeurs possesseurs en utilisant `owner` depuis la [bibliothèque de support des lignes directrices](#gsl-guidelines-support-library) @TODO-LINK :

    owner<X*> compute(args)    // Il est maintenant clair que la propriété est transférée
    {
        owner<X*> res = new X{};
        // ...
        return res;
    }

Cela indique aux outils d'analyse que `res` est un possesseur.
C'est-à-dire que sa valeur doit être `delete`e ou transférée à un autre possesseur, comme c'est fait ici par le `return`.

`owner` est utilisé de manière similaire dans l'implémentation des gestionnaires de ressources.

##### Note

Chaque objet passé en tant que pointeur brut (ou itérateur) est supposé être possédé par
l'appelant, de sorte que sa durée de vie est gérée par l'appelant. Vu autrement :
les API de transfert de propriété sont relativement rares par rapport aux API de passage de pointeurs,
donc la valeur par défaut est « pas de transfert de propriété ».

**Voir aussi** : [Passage d'arguments](006-functions.md#rf-conventional), [utilisation d'arguments pointeurs intelligents](009-resource.md#rr-smartptrparam), et [retour par valeur](006-functions.md#rf-value-return).

##### Application

* (Simple) Avertir sur un `delete` d'un pointeur brut qui n'est pas un `owner<T>`. Suggérer l'usage d'un gestionnaire de ressources de la bibliothèque standard ou l'usage de `owner<T>`.
* (Simple) Avertir sur l'absence de `reset` ou de `delete` explicite d'un pointeur `owner` sur tous les chemins de code.
* (Simple) Avertir si la valeur de retour de `new` ou d'un appel de fonction avec une valeur de retour `owner` est assignée à un pointeur brut ou une référence non-`owner`.

### <a name="ri-nullptr"></a>I.12: Déclarer un pointeur qui ne doit pas être nul comme `not_null`

##### Raison

Pour aider à éviter les erreurs de déréférencement de `nullptr`.
Pour améliorer les performances en évitant des vérifications redondantes de `nullptr`.

##### Exemple

    int length(const char* p);            // il n'est pas clair si length(nullptr) est valide

    length(nullptr);                      // OK ?

    int length(not_null<const char*> p);  // mieux : nous pouvons supposer que p ne peut pas être nullptr

    int length(const char* p);            // nous devons supposer que p peut être nullptr

En exprimant l'intention dans le code source, les implémenteurs et les outils peuvent fournir de meilleurs diagnostics, tels que la détection de certaines classes d'erreurs par analyse statique, et effectuer des optimisations, telles que l'élimination de branches et de tests de nullité.

##### Note

`not_null` est défini dans la [bibliothèque de support des lignes directrices](#gsl-guidelines-support-library) @TODO-LINK.

##### Note

L'hypothèse que le pointeur vers `char` pointait vers une chaîne de style C (une chaîne de caractères terminée par zéro) restait implicite, et une source potentielle de confusion et d'erreurs. Utilisez `czstring` en préférence à `const char*`.

    // nous pouvons supposer que p ne peut pas être nullptr
    // nous pouvons supposer que p pointe vers un tableau de caractères terminé par zéro
    int length(not_null<czstring> p);

Note : `length()` est bien sûr `std::strlen()` déguisé.

##### Application

* (Simple) ((Fondation)) Si une fonction vérifie un paramètre pointeur contre `nullptr` avant accès, sur tous les chemins de contrôle, alors avertir qu'il devrait être déclaré `not_null`.
* (Complexe) Si une fonction avec une valeur de retour pointeur garantit qu'elle n'est pas `nullptr` sur tous les chemins de retour, alors avertir que le type de retour devrait être déclaré `not_null`.

### <a name="ri-array"></a>I.13: Ne pas passer un tableau en tant que simple pointeur

##### Raison

Les interfaces de style (pointeur, taille) sont sources d'erreurs. De plus, un simple pointeur (vers tableau) doit s'appuyer sur une convention pour permettre à l'appelé de déterminer la taille.

##### Exemple

Considérez :

    void copy_n(const T* p, T* q, int n); // copier de [p:p+n) vers [q:q+n)

Et s'il y a moins de `n` éléments dans le tableau pointé par `q` ? Alors, nous écrasons une mémoire probablement sans rapport.
Et s'il y a moins de `n` éléments dans le tableau pointé par `p` ? Alors, nous lisons une mémoire probablement sans rapport.
Les deux sont un comportement indéfini et un bug potentiellement très nuisible.

##### Alternative

Envisagez d'utiliser des spans explicites :

    void copy(span<const T> r, span<T> r2); // copier r vers r2

##### Exemple, mauvais

Considérez :

    void draw(Shape* p, int n);  // mauvaise interface ; mauvais code
    Circle arr[10];
    // ...
    draw(arr, 10);

Passer `10` en tant que `n` pourrait être une erreur : la convention la plus courante est de supposer `[0:n)` mais cela n'est nulle part déclaré. Pire encore, c'est que l'appel à `draw()` a compilé du tout : il y a eu une conversion implicite de tableau vers pointeur (décroissance de tableau) puis une autre conversion implicite de `Circle` vers `Shape`. Il n'y a aucun moyen que `draw()` puisse parcourir en sécurité ce tableau : il n'a aucun moyen de connaître la taille des éléments.

**Alternative** : Utiliser une classe de support qui garantit que le nombre d'éléments est correct et empêche les conversions implicites dangereuses. Par exemple :

    void draw2(span<Circle>);
    Circle arr[10];
    // ...
    draw2(span<Circle>(arr));  // déduire le nombre d'éléments
    draw2(arr);    // déduire le type d'élément et la taille du tableau

    void draw3(span<Shape>);
    draw3(arr);    // erreur : impossible de convertir Circle[10] en span<Shape>

Ce `draw2()` passe la même quantité d'information à `draw()`, mais rend explicite le fait qu'il s'agit d'un ensemble de `Circle`. Voir ??? @TODO-LINK.

##### Exception

Utilisez `zstring` et `czstring` pour représenter les chaînes de style C, terminées par zéro.
Mais en le faisant, utilisez `std::string_view` ou `span<char>` de la [GSL](#gsl-guidelines-support-library) @TODO-LINK pour prévenir les erreurs de plage.

##### Application

* (Simple) ((Bornes)) Avertir pour toute expression qui s'appuierait sur une conversion implicite d'un type tableau vers un type pointeur. Autoriser l'exception pour les types de pointeurs zstring/czstring.
* (Simple) ((Bornes)) Avertir pour toute opération arithmétique sur une expression de type pointeur qui résulte en une valeur de type pointeur. Autoriser l'exception pour les types de pointeurs zstring/czstring.

### <a name="ri-global-init"></a>I.22: Éviter les initialisations complexes d'objets globaux

##### Raison

Une initialisation complexe peut conduire à un ordre d'exécution indéfini.

##### Exemple

    // file1.c

    extern const X x;

    const Y y = f(x);   // lire x ; écrire y

    // file2.c

    extern const Y y;

    const X x = g(y);   // lire y ; écrire x

Puisque `x` et `y` sont dans différentes unités de traduction, l'ordre des appels à `f()` et `g()` est indéfini ;
l'un accèdera à un `const` non initialisé.
Cela montre que le problème de l'ordre d'initialisation pour les objets globaux (portée de namespace) n'est pas limité aux variables *globales*.

##### Note

Les problèmes d'ordre d'initialisation deviennent particulièrement difficiles à gérer dans le code concurrent.
Il est généralement préférable d'éviter les objets globaux (portée de namespace) en totalité.

##### Application

* Signaler les initialiseurs de globaux qui appellent des fonctions non-`constexpr`
* Signaler les initialiseurs de globaux qui accèdent à des objets `extern`

### <a name="ri-nargs"></a>I.23: Garder le nombre de paramètres de fonction bas

##### Raison

Avoir beaucoup de paramètres ouvre des possibilités de confusion. Passer beaucoup d'arguments est souvent coûteux par rapport aux alternatives.

##### Discussion

Les deux raisons les plus courantes pour lesquelles une fonction a trop de paramètres sont :

1. *Manque d'abstraction.*
   Il manque une abstraction, de sorte qu'une valeur composée est
   passée comme éléments individuels au lieu d'un seul objet qui applique une invariant.
   Cela non seulement étend la liste des paramètres, mais conduit à des erreurs car les valeurs composantes
   ne sont plus protégées par une invariant appliquée.

2. *Violation du « une fonction, une responsabilité ».
   La fonction essaie de faire plus qu'un travail et devrait probablement être refactorisée.

##### Exemple

La fonction `merge()` de la bibliothèque standard est à la limite de ce que nous pouvons gérer confortablement :

    template<class InputIterator1, class InputIterator2, class OutputIterator, class Compare>
    OutputIterator merge(InputIterator1 first1, InputIterator1 last1,
                         InputIterator2 first2, InputIterator2 last2,
                         OutputIterator result, Compare comp);

Notez que c'est à cause du problème 1 ci-dessus -- manque d'abstraction. Au lieu de passer une plage (abstraction), STL passe des paires d'itérateurs (valeurs composantes non encapsulées).

Ici, nous avons quatre arguments de modèle et six arguments de fonction.
Pour simplifier les usages les plus fréquents et les plus simples, l'argument de comparaison peut être par défaut `<` :

    template<class InputIterator1, class InputIterator2, class OutputIterator>
    OutputIterator merge(InputIterator1 first1, InputIterator1 last1,
                         InputIterator2 first2, InputIterator2 last2,
                         OutputIterator result);

Cela ne réduit pas la complexité totale, mais réduit la complexité de surface présentée à de nombreux utilisateurs.
Pour vraiment réduire le nombre d'arguments, nous devons regrouper les arguments en abstractions de plus haut niveau :

    template<class InputRange1, class InputRange2, class OutputIterator>
    OutputIterator merge(InputRange1 r1, InputRange2 r2, OutputIterator result);

Regrouper les arguments en « lots » est une technique générale pour réduire le nombre d'arguments et augmenter les possibilités de vérification.

Alternativement, nous pourrions utiliser un concept de la bibliothèque standard pour définir la notion de trois types qui doivent être utilisables pour la fusion :

    template<class In1, class In2, class Out>
      requires mergeable<In1, In2, Out>
    Out merge(In1 r1, In2 r2, Out result);

##### Exemple

Les profils de sécurité recommandent de remplacer

    void f(int* some_ints, int some_ints_length);  // MAUVAIS : style C, non sûr

par

    void f(gsl::span<int> some_ints);              // BON : sûr, bornes vérifiées

Ici, l'usage d'une abstraction apporte des avantages en termes de sécurité et de robustesse, et réduit naturellement aussi le nombre de paramètres.

##### Note

Combien de paramètres est trop ? Essayez d'utiliser moins de quatre (4) paramètres.
Il y a des fonctions qui sont mieux exprimées avec quatre paramètres individuels, mais pas beaucoup.

**Alternative** : Utiliser une meilleure abstraction : regrouper les arguments en objets significatifs et passer les objets (par valeur ou par référence).

**Alternative** : Utiliser des arguments par défaut ou des surcharges pour permettre les formes d'appels les plus courantes avec moins d'arguments.

##### Application

* Avertir quand une fonction déclare deux itérateurs (y compris des pointeurs) du même type au lieu d'une plage ou d'une vue.
* (Non applicable) C'est une ligne directrice philosophique qui est irréalisable à vérifier directement.

### <a name="ri-unrelated"></a>I.24: Éviter des paramètres adjacents qui peuvent être intervertis sans changer l'appel mais avec un sens différent

##### Raison

Des arguments adjacents du même type sont facilement intervertis par erreur.

##### Exemple, mauvais

Considérez :

    void copy_n(T* p, T* q, int n);  // copier de [p:p + n) vers [q:q + n)

C'est une variante pénible d'une interface de style C K&R. Il est facile d'inverser les arguments « vers » et « depuis ».

Utiliser `const` pour l'argument « depuis » :

    void copy_n(const T* p, T* q, int n);  // copier de [p:p + n) vers [q:q + n)

##### Exception

Si l'ordre des paramètres n'est pas important, il n'y a pas de problème :

    int max(int a, int b);

##### Alternative

Ne pas passer des tableaux en tant que pointeurs, passer un objet représentant une plage (par exemple un `span`) :

    void copy_n(span<const T> p, span<T> q);  // copier de p vers q

##### Alternative

Définir un `struct` comme type de paramètre et nommer les champs pour ces paramètres en conséquence :

    struct SystemParams {
        string config_file;
        string output_path;
        seconds timeout;
    };
    void initialize(SystemParams p);

Cela a tendance à rendre les appels clairs pour les lecteurs futurs, car les paramètres
sont souvent remplis par nom au point d'appel.

##### Note

Seul le concepteur de l'interface peut adéquatement traiter la source des violations de cette ligne directrice.

##### Stratégie d'application

(Simple) Avertir si deux paramètres consécutifs partagent le même type.

Nous cherchons encore une application moins simple.

### <a name="ri-abstract"></a>I.25: Privilégier les classes abstraites vides comme interfaces plutôt que des hiérarchies de classes

##### Raison

Les classes abstraites vides (sans données membres non statiques) sont plus susceptibles d'être stables que des classes de base avec état.

##### Exemple, mauvais

Vous auriez pu deviner que `Shape` apparaîtrait quelque part :-)

    class Shape {  // mauvais : classe d'interface chargée de données
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

Cela forcera chaque classe dérivée à calculer un centre -- même si c'est non trivial et que le centre n'est jamais utilisé. De même, chaque `Shape` n'a pas une `Color`, et beaucoup de `Shape` sont mieux représentés sans contour défini comme une séquence de `Point`. L'usage d'une classe abstraite est meilleur :

    class Shape {    // mieux : Shape est une pure interface
    public:
        virtual Point center() const = 0;   // fonctions virtuelles pures
        virtual void draw() const = 0;
        virtual void rotate(int) = 0;
        // ...
        // ... pas de données membres ...
        // ...
        virtual ~Shape() = default;
    };

##### Application

(Simple) Avertir si un pointeur/référence vers une classe `C` est assigné à un pointeur/référence vers une classe de base de `C` et que la classe de base contient des données membres.

### <a name="ri-abi"></a>I.26: Si vous souhaitez une ABI compatible entre compilateurs, utiliser un sous-ensemble de style C

##### Raison

Différents compilateurs implémentent des dispositions binaires différentes pour les classes, le traitement des exceptions, les noms de fonctions, et d'autres détails d'implémentation.

##### Exception

Des ABI communs émergent sur certaines plateformes, vous affranchissant des restrictions les plus draconiennes.

##### Note

Si vous utilisez un seul compilateur, vous pouvez utiliser le C++ complet dans les interfaces. Cela peut nécessiter une recompilation après une mise à niveau vers une nouvelle version du compilateur.

##### Application

(Non applicable) Il est difficile d'identifier fiablement là où une interface fait partie d'une ABI.

### <a name="ri-pimpl"></a>I.27: Pour une ABI de bibliothèque stable, envisager l'idiome Pimpl

##### Raison

Parce que les données membres privées participent à la disposition de la classe et les fonctions membres privées participent à la résolution de surcharge, les modifications de ces
détails d'implémentation nécessitent la recompilation de tous les utilisateurs d'une classe qui les utilise. Une classe d'interface non polymorphe tenant un pointeur vers
l'implémentation (Pimpl) peut isoler les utilisateurs d'une classe des changements dans son implémentation au prix d'une indirection.

##### Exemple

interface (widget.h)

    class widget {
        class impl;
        std::unique_ptr<impl> pimpl;
    public:
        void draw(); // API publique qui sera transférée à l'implémentation
        widget(int); // défini dans le fichier d'implémentation
        ~widget();   // défini dans le fichier d'implémentation, où impl est un type complet
        widget(widget&&) noexcept; // défini dans le fichier d'implémentation
        widget(const widget&) = delete;
        widget& operator=(widget&&) noexcept; // défini dans le fichier d'implémentation
        widget& operator=(const widget&) = delete;
    };


implémentation (widget.cpp)

    class widget::impl {
        int n; // données privées
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

Voir [GOTW #100](https://herbsutter.com/gotw/_100/) et [cppreference](https://en.cppreference.com/w/cpp/language/pimpl) pour les compromis et les détails d'implémentation supplémentaires associés à cet idiome.

##### Application

(Non applicable) Il est difficile d'identifier fiablement là où une interface fait partie d'une ABI.

### <a name="ri-encapsulate"></a>I.30: Encapsuler les violations de règles

##### Raison

Pour garder le code simple et sûr.
Parfois, des techniques laides, non sûres ou sources d'erreurs sont nécessaires pour des raisons logiques ou de performance.
Si c'est le cas, gardez-les locales, plutôt que de « contaminer » les interfaces de sorte que des groupes plus larges de programmeurs doivent être conscients des
subtilités.
La complexité d'implémentation ne devrait pas, si possible, se propager à travers les interfaces dans le code utilisateur.

##### Exemple

Considérez un programme qui, en fonction d'une forme d'entrée (par exemple les arguments de `main`), doit consommer l'entrée
d'un fichier, de la ligne de commande, ou de l'entrée standard.
Nous pourrions écrire

    bool owned;
    owner<istream*> inp;
    switch (source) {
    case std_in:        owned = false; inp = &cin;                       break;
    case command_line:  owned = true;  inp = new istringstream{argv[2]}; break;
    case file:          owned = true;  inp = new ifstream{argv[2]};      break;
    }
    istream& in = *inp;

Cela viole la règle [contre les variables non initialisées](010-expr.md#res-always),
la règle contre [l'ignorance de la propriété](005-interfaces.md#ri-raw),
et la règle [contre les constantes magiques](010-expr.md#res-magic).
En particulier, quelqu'un doit se souvenir d'écrire quelque part

    if (owned) delete inp;

Nous pourrions gérer cet exemple particulier en utilisant `unique_ptr` avec un destructeur spécial qui ne fait rien pour `cin`,
mais c'est compliqué pour les débutants (qui peuvent facilement rencontrer ce problème) et l'exemple illustre un problème plus général
où une propriété que nous voudrions considérer statique (ici, la propriété) doit être traitée occasionnellement
à l'exécution.
Les exemples communs, les plus fréquents et les plus sûrs peuvent être traités statiquement, donc nous ne voulons pas ajouter de coût et de complexité à ceux-ci.
Mais nous devons aussi gérer les cas peu courants, moins sûrs et nécessairement plus coûteux.
De tels exemples sont discutés dans [[Str15]](https://www.stroustrup.com/resource-model.pdf).

Donc, nous écrivons une classe

    class Istream { [[gsl::suppress("lifetime")]]
    public:
        enum Opt { from_line = 1 };
        Istream() { }
        Istream(czstring p) : owned{true}, inp{new ifstream{p}} {}            // lire d'un fichier
        Istream(czstring p, Opt) : owned{true}, inp{new istringstream{p}} {}  // lire de la ligne de commande
        ~Istream() { if (owned) delete inp; }
        operator istream&() { return *inp; }
    private:
        bool owned = false;
        istream* inp = &cin;
    };

Maintenant, la nature dynamique de la propriété de `istream` a été encapsulée.
Présumablement, un peu de vérification d'erreurs potentielles serait ajoutée dans un code réel.

##### Application

* Difficile, il est difficile de décider quel code en violation de règles est essentiel
* Signaler la suppression de règles qui permet aux violations de règles de traverser les interfaces