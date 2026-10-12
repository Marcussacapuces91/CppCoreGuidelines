# <a name="s-interfaces"></a>I : Interfaces

Une interface est un contrat entre deux parties d'un programme. Énoncer précisément ce qui est attendu d'un fournisseur de service et d'un utilisateur de ce service est essentiel.
Disposer de bonnes interfaces (faciles à comprendre, encourageant un usage efficace, peu sujettes aux erreurs, permettant les tests, etc.) est probablement l'aspect le plus important de l'organisation du code.

Résumé des règles sur les interfaces :

* [I.1 : Rendre les interfaces explicites](005-interfaces.md#ri-explicit)
* [I.2 : Éviter les variables globales non `const`](005-interfaces.md#ri-global)
* [I.3 : Éviter les singletons](005-interfaces.md#ri-singleton)
* [I.4 : Rendre les interfaces précisément et fortement typées](005-interfaces.md#ri-typed)
* [I.5 : Énoncer les préconditions (le cas échéant)](005-interfaces.md#ri-pre)
* [I.6 : Préférer `Expects()` pour exprimer les préconditions](005-interfaces.md#ri-expects)
* [I.7 : Énoncer les postconditions](005-interfaces.md#ri-post)
* [I.8 : Préférer `Ensures()` pour exprimer les postconditions](005-interfaces.md#ri-ensures)
* [I.9 : Si une interface est un gabarit, documenter ses paramètres à l'aide de concepts](005-interfaces.md#ri-concepts)
* [I.10 : Utiliser les exceptions pour signaler l'échec d'une tâche requise](005-interfaces.md#ri-except)
* [I.11 : Ne jamais transférer la propriété par un pointeur brut (`T*`) ou une référence (`T&`)](005-interfaces.md#ri-raw)
* [I.12 : Déclarer un pointeur qui ne doit pas être nul comme `not_null`](005-interfaces.md#ri-nullptr)
* [I.13 : Ne pas passer un tableau en tant que simple pointeur](005-interfaces.md#ri-array)
* [I.22 : Éviter l'initialisation complexe des objets globaux](005-interfaces.md#ri-global-init)
* [I.23 : Limiter le nombre d'arguments de fonction](005-interfaces.md#ri-nargs)
* [I.24 : Éviter les paramètres adjacents qui peuvent être appelés dans les deux ordres avec la même signature mais des significations différentes](005-interfaces.md#ri-unrelated)
* [I.25 : Préférer les classes abstraites vides en tant qu'interfaces aux hiérarchies de classes](005-interfaces.md#ri-abstract)
* [I.26 : Si vous souhaitez une ABI inter-compilateurs, utiliser un sous-ensemble de style C](005-interfaces.md#ri-abi)
* [I.27 : Pour une ABI de bibliothèque stable, envisager l'idiome Pimpl](005-interfaces.md#ri-pimpl)
* [I.30 : Encapsuler les violations de règles](005-interfaces.md#ri-encapsulate)

**Voir aussi** :

* [F : Fonctions](006-functions.md)
* [C.concrete : Types concrets](007-class.md#ss-concrete) <!-- @TODO-LINK : référence d'origine ambiguë (007-class.md018-stdlib.md#ss-concrete) -->
* [C.hier : Hiérarchies de classes](007-class.md#ss-hier)
* [C.over : Surcharge et opérateurs surchargés](007-class.md#ss-overload)
* [C.con : Conteneurs et autres poignées de ressources](007-class.md#ss-containers) <!-- @TODO-LINK : référence d'origine ambiguë (007-class.md018-stdlib.md#ss-containers) -->
* [E : Gestion des erreurs](013-errors.md)
* [T : Gabarits et programmation générique](015-templates.md)

### <a name="ri-explicit"></a>I.1 : Rendre les interfaces explicites

##### Raison

La justesse. Les hypothèses non énoncées dans une interface sont facilement négligées et difficiles à tester.

##### Exemple, mauvais

Contrôler le comportement d'une fonction à l'aide d'une variable globale (portée de l'espace de noms) — un mode d'appel — est implicite et potentiellement source de confusion. Par exemple :

    int round(double d)
    {
        return (round_up) ? ceil(d) : d;    // à éviter : dépendance « invisible »
    }

Il ne sera pas évident pour l'appelant que deux appels de `round(7.2)` peuvent donner des résultats différents.

##### Exception

Parfois, nous contrôlons les détails d'un ensemble d'opérations par une variable d'environnement, par exemple la sortie normale vs. détaillée ou le mode débogage vs. optimisé.
L'utilisation d'un contrôle non local est potentiellement source de confusion, mais ne contrôle que des détails d'implémentation d'une sémantique par ailleurs fixe.

##### Exemple, mauvais

Signaler via des variables non locales (par exemple `errno`) est facilement ignoré. Par exemple :

    // à éviter : aucune vérification de la valeur de retour de fprintf
    fprintf(connection, "journalisation : %d %d %d\n", x, y, s);

Que se passe-t-il si la connexion tombe et qu'aucune sortie de journalisation n'est produite ? Voir I.??? <!-- @TODO-LINK : référence manquante dans le document -->

**Alternative** : Lever une exception. Une exception ne peut pas être ignorée.

**Formulation alternative** : Éviter de transmettre des informations à travers une interface via un état non local ou implicite.
Remarquez que les fonctions membres non `const` transmettent des informations à d'autres fonctions membres à travers l'état de leur objet.

**Formulation alternative** : Une interface doit être une fonction ou un ensemble de fonctions.
Les fonctions peuvent être des gabarits de fonctions et les ensembles de fonctions peuvent être des classes ou des gabarits de classes.

##### Application

* (Simple) Une fonction ne devrait pas prendre de décisions de flux de contrôle sur la base des valeurs de variables déclarées en portée d'espace de noms.
* (Simple) Une fonction ne devrait pas écrire dans des variables déclarées en portée d'espace de noms.

### <a name="ri-global"></a>I.2 : Éviter les variables globales non `const`

##### Raison

Les variables globales non `const` masquent les dépendances et les rendent sujettes à des modifications imprévisibles.

##### Exemple

    struct Data {
        // ... beaucoup de choses ...
    } data;            // data non const

    void compute()     // à éviter
    {
        // ... utiliser data ...
    }

    void output()     // à éviter
    {
        // ... utiliser data ...
    }

Qui d'autre pourrait modifier `data` ?

**Attention** : L'initialisation des objets globaux n'est pas totalement ordonnée.
Si vous utilisez un objet global, initialisez-le avec une constante.
Notez qu'il est possible d'obtenir un ordre d'initialisation indéfini même pour des objets `const`.

##### Exception

Un objet global est souvent préférable à un singleton.

##### Remarque

Les constantes globales sont utiles.

##### Remarque

La règle sur les variables globales s'applique également aux variables de portée d'espace de noms.

**Alternative** : Si vous utilisez des données globales (plus généralement de portée d'espace de noms) pour éviter les copies, envisagez de passer les données par référence en tant qu'objet `const`.
Une autre solution consiste à définir les données comme l'état d'un objet et les opérations comme des fonctions membres.

**Attention** : Méfiez-vous des conditions de course : si un thread peut accéder à des données non locales (ou passées par référence) pendant qu'un autre thread exécute la fonction appelée, nous pouvons avoir une condition de course.
Chaque pointeur ou référence vers des données mutables est une condition de course potentielle.

L'utilisation de pointeurs globaux ou de références pour accéder et modifier des données non `const`, non globales par ailleurs,
n'est pas une meilleure alternative aux variables globales non `const`, car cela ne résout pas les problèmes de dépendances cachées ou de conditions de course potentielles.

##### Remarque

On ne peut pas avoir de condition de course sur des données immuables.

**Références** : Voir les [règles d'appel de fonctions](006-functions.md#ss-call).

##### Remarque

La règle est « éviter », pas « n'utilisez pas ». Il y aura bien sûr des (rares) exceptions, comme `cin`, `cout` et `cerr`.

##### Application

(Simple) Signaler toutes les variables non `const` déclarées en portée d'espace de noms et tous les pointeurs/références globaux vers des données non `const`.


### <a name="ri-singleton"></a>I.3 : Éviter les singletons

##### Raison

Les singletons sont essentiellement des objets globaux compliqués déguisés.

##### Exemple

    class Singleton {
        // ... beaucoup de choses pour garantir qu'un seul objet Singleton est créé,
        // qu'il est initialisé correctement, etc.
    };

Il existe de nombreuses variantes de l'idée du singleton.
C'est en soi un problème.

##### Remarque

Si vous ne voulez pas qu'un objet global change, déclarez-le `const` ou `constexpr`.

##### Exception

Vous pouvez utiliser le singleton le plus simple (si simple qu'il n'est souvent pas considéré comme un singleton) pour obtenir l'initialisation à la première utilisation, le cas échéant :

    X& myX()
    {
        static X my_x {3};
        return my_x;
    }

C'est l'une des solutions les plus efficaces aux problèmes liés à l'ordre d'initialisation.
Dans un environnement multi-threadé, l'initialisation de l'objet statique n'introduit pas de condition de course
(sauf si vous accédez imprudemment à un objet partagé depuis son constructeur).

Notez que l'initialisation d'un `static` local n'implique pas de condition de course.
Cependant, si la destruction de `X` implique une opération qui doit être synchronisée, nous devons utiliser une solution moins simple.
Par exemple :

    X& myX()
    {
        static auto p = new X {3};
        return *p;  // fuite potentielle
    }

Il faut maintenant que quelqu'un fasse `delete` sur cet objet d'une manière suffisamment sûre pour les threads.
C'est sujet aux erreurs, donc nous n'utilisons pas cette technique sauf si

* `myX` est dans du code multi-threadé,
* que l'objet `X` doit être détruit (par exemple parce qu'il libère une ressource), et
* que le code du destructeur de `X` doit être synchronisé.

Si, comme beaucoup, vous définissez un singleton comme une classe pour laquelle un seul objet est créé, des fonctions comme `myX` ne sont pas des singletons, et cette technique utile n'est pas une exception à la règle du non-singleton.

##### Application

Très difficile en général.

* Cherchez des classes dont le nom contient `singleton`.
* Cherchez des classes pour lesquelles un seul objet est créé (en comptant les objets ou en examinant les constructeurs).
* Si une classe X a une fonction statique publique qui contient un statique local de fonction du type X de la classe et renvoie un pointeur ou une référence vers celui-ci, l'interdire.

### <a name="ri-typed"></a>I.4 : Rendre les interfaces précisément et fortement typées

##### Raison

Les types sont la documentation la plus simple et la meilleure, améliorent la lisibilité grâce à leur signification bien définie et sont vérifiés à la compilation.
De plus, le code précisément typé est souvent mieux optimisé.

##### Exemple, à éviter

Considérez :

    void pass(void* data);    // type void* faible et insuffisamment qualifié est suspect

Les appelants ne savent pas quels types sont autorisés et si les données peuvent
être mutées car `const` n'est pas précisé. Notez que tous les types de pointeurs
se convertissent implicitement en `void*`, il est donc facile pour les appelants de fournir cette valeur.

La fonction appelée doit faire un `static_cast` des données vers un type non vérifié pour les utiliser.
C'est sujet aux erreurs et verbeux.

N'utilisez `const void*` que pour passer des données dans des conceptions qui ne sont pas descriptibles en C++. Envisagez plutôt d'utiliser un `variant` ou un pointeur vers une classe de base.

**Alternative** : Souvent, un paramètre de gabarit peut éliminer le `void*` en le transformant en `T*` ou `T&`.
Pour du code générique, ces `T` peuvent être des paramètres de gabarit généraux ou contraints par des concepts.

##### Exemple, mauvais

Considérez :

    draw_rect(100, 200, 100, 500); // que spécifient les nombres ?

    draw_rect(p.x, p.y, 10, 20); // dans quelles unités sont 10 et 20 ?

Il est clair que l'appelant décrit un rectangle, mais il n'est pas clair à quoi chaque partie correspond. De plus, un `int` peut porter des formes arbitraires d'informations, y compris des valeurs de nombreuses unités, nous devons donc deviner la signification des quatre `int`. Probablement, les deux premiers sont un couple de coordonnées `x`, `y`, mais qu'en est-il des deux derniers ?

Les commentaires et les noms de paramètres peuvent aider, mais nous pouvons être explicites :

    void draw_rectangle(Point haut_gauche, Point bas_droite);
    void draw_rectangle(Point haut_gauche, Size hauteur_largeur);

    draw_rectangle(p, Point{10, 20});  // deux coins
    draw_rectangle(p, Size{10, 20});   // un coin et un couple (hauteur, largeur)

Évidemment, nous ne pouvons pas détecter toutes les erreurs via le système de types statique
(par exemple, le fait que le premier argument soit censé être un point en haut à gauche est laissé à la convention (nommage et commentaires)).

##### Exemple, mauvais

Considérez :

    set_settings(true, false, 42); // que spécifient les nombres ?

Les types des paramètres et leurs valeurs ne communiquent pas quels réglages sont spécifiés ni ce que ces valeurs signifient.

Cette conception est plus explicite, sûre et lisible :

    alarm_settings s{};
    s.enabled = true;
    s.displayMode = alarm_settings::mode::spinning_light;
    s.frequency = alarm_settings::every_10_seconds;
    set_settings(s);

Pour le cas d'un ensemble de valeurs booléennes, envisagez d'utiliser un enum de drapeaux ; un motif qui exprime un ensemble de valeurs booléennes.

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

La fonction peut également être écrite de telle sorte qu'elle acceptera n'importe quelle unité de durée.

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

* (Simple) Signaler l'utilisation de `void*` en tant que paramètre ou type de retour.
* (Simple) Signaler l'utilisation de plus d'un paramètre `bool`.
* (Difficile à bien faire) Chercher des fonctions qui utilisent trop d'arguments de type primitif.

### <a name="ri-pre"></a>I.5 : Énoncer les préconditions (le cas échéant)

##### Raison

Les arguments ont une signification qui peut contraindre leur usage correct dans la fonction appelée.

##### Exemple

Considérez :

    double sqrt(double x);

Ici `x` doit être non négatif. Le système de types ne peut pas (facilement et naturellement) l'exprimer, nous devons donc utiliser d'autres moyens. Par exemple :

    double sqrt(double x); // x doit être non négatif

Certaines préconditions peuvent être exprimées comme des assertions. Par exemple :

    double sqrt(double x) { Expects(x >= 0); /* ... */ }

Idéalement, cet `Expects(x >= 0)` devrait faire partie de l'interface de `sqrt()` mais ce n'est pas facile à faire. Pour l'instant, nous le plaçons dans la définition (corps de la fonction).

**Références** : `Expects()` est décrite dans [GSL](#gsl-guidelines-support-library).

##### Remarque

Préférez une spécification formelle des exigences, comme `Expects(p);`.
Si cela n'est pas réalisable, utilisez du texte en anglais dans des commentaires, comme `// the sequence [p:q) is ordered using <`.

##### Remarque

La plupart des fonctions membres ont comme précondition qu'un invariant de classe est respecté.
Cet invariant est établi par un constructeur et doit être rétabli à la sortie par chaque fonction membre appelée depuis l'extérieur de la classe.
Nous n'avons pas besoin de le mentionner pour chaque fonction membre.

##### Application

(Non applicable)

**Voir aussi** : Les règles sur le passage de pointeurs. ??? <!-- @TODO-LINK : référence manquante dans le document -->

### <a name="ri-expects"></a>I.6 : Préférer `Expects()` pour exprimer les préconditions

##### Raison

Pour rendre clair que la condition est une précondition et pour permettre l'utilisation d'outils.

##### Exemple

    int area(int height, int width)
    {
        Expects(height > 0 && width > 0);            // bon
        if (height <= 0 || width <= 0) my_error();   // obscur
        // ...
    }

##### Remarque

Les préconditions peuvent être exprimées de nombreuses manières, y compris dans des commentaires, des énoncés `if` et `assert()`.
Cela peut les rendre difficiles à distinguer du code ordinaire, difficiles à mettre à jour, difficiles à manipuler par des outils, et peuvent avoir la mauvaise sémantique (voulez-vous toujours interrompre en mode débogage et ne rien vérifier en production ?).

##### Remarque

Les préconditions devraient faire partie de l'interface plutôt que de l'implémentation,
mais nous n'avons pas encore les capacités du langage pour le faire.
Dès que le support du langage sera disponible (par exemple, voir la [proposition de contrat](https://www.open-std.org/jtc1/sc22/wg21/docs/papers/2016/p0380r1.pdf)), nous adopterons la version standard des préconditions, des postconditions et des assertions.

##### Remarque

`Expects()` peut également être utilisée pour vérifier une condition au milieu d'un algorithme.

##### Remarque

Non, l'utilisation de `unsigned` n'est pas un bon moyen de contourner le problème de [garantir qu'une valeur est non négative](010-expr.md#res-nonnegative).

##### Application

(Non applicable) Trouver la variété des manières dont les préconditions peuvent être affirmées n'est pas réalisable. Émettre un avertissement pour celles qui peuvent être facilement identifiées (`assert()`) a une valeur discutable en l'absence d'une capacité du langage.

### <a name="ri-post"></a>I.7 : Énoncer les postconditions

##### Raison

Pour détecter les malentendus sur le résultat et éventuellement attraper des implémentations erronées.

##### Exemple, mauvais

Considérez :

    int area(int height, int width) { return height * width; }  // mauvais

Ici, nous (imprudemment) avons omis la spécification de la précondition, donc il n'est pas explicite que hauteur et largeur doivent être positives.
Nous avons également omis la spécification de la postcondition, donc il n'est pas évident que l'algorithme (`hauteur * largeur`) est incorrect pour des surfaces supérieures au plus grand entier.
Un dépassement peut survenir.
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

Il n'y avait pas de postcondition stipulant que le tampon devait être effacé, et l'optimiseur a éliminé l'appel `memset()` apparemment redondant :

    void f()    // mieux
    {
        char buffer[MAX];
        // ...
        memset(buffer, 0, sizeof(buffer));
        Ensures(buffer[0] == 0);
    }

##### Remarque

Les postconditions sont souvent informellement énoncées dans un commentaire qui indique le but d'une fonction ; `Ensures()` peut être utilisé pour rendre cela plus systématique, visible et vérifiable.

##### Remarque

Les postconditions sont particulièrement importantes lorsqu'elles se rapportent à quelque chose qui n'est pas directement reflété dans un résultat retourné, comme l'état d'une structure de données utilisée.

##### Exemple

Considérez une fonction qui manipule un `Record`, utilisant un `mutex` pour éviter les conditions de course :

    mutex m;

    void manipulate(Record& r)    // à éviter
    {
        m.lock();
        // ... pas de m.unlock() ...
    }

Ici, nous avons « oublié » de préciser que le `mutex` doit être libéré, nous ne savons donc pas si l'échec à garantir la libération du `mutex` était un bug ou une fonctionnalité.
Énoncer la postcondition aurait rendu la situation claire :

    void manipulate(Record& r)    // postcondition : m est déverrouillé à la sortie
    {
        m.lock();
        // ... pas de m.unlock() ...
    }

Le bug est maintenant évident (mais seulement pour un humain lisant les commentaires).

Mieux encore, utiliser [RAII](009-resource.md#rr-raii) pour garantir que la postcondition (« le verrou doit être libéré ») est appliquée dans le code :

    void manipulate(Record& r)    // le mieux
    {
        lock_guard<mutex> _ {m};
        // ...
    }

##### Remarque

Idéalement, les postconditions sont énoncées dans l'interface/déclaration pour que les utilisateurs puissent les voir facilement.
Seules les postconditions liées aux utilisateurs peuvent être énoncées dans l'interface.
Les postconditions liées uniquement à l'état interne appartiennent à la définition/implémentation.

##### Application

(Non applicable) C'est une directive philosophique qui est irréalisable à vérifier
directement dans le cas général. Des vérificateurs spécifiques au domaine (comme les
vérificateurs de verrouillage) existent pour de nombreuses chaînes d'outils.

### <a name="ri-ensures"></a>I.8 : Préférer `Ensures()` pour exprimer les postconditions

##### Raison

Pour rendre clair que la condition est une postcondition et pour permettre l'utilisation d'outils.

##### Exemple

    void f()
    {
        char buffer[MAX];
        // ...
        memset(buffer, 0, MAX);
        Ensures(buffer[0] == 0);
    }

##### Remarque

Les postconditions peuvent être exprimées de nombreuses manières, y compris dans des commentaires, des énoncés `if` et `assert()`.
Cela peut les rendre difficiles à distinguer du code ordinaire, difficiles à mettre à jour, difficiles à manipuler par des outils, et peuvent avoir la mauvaise sémantique.

**Alternative** : Les postconditions de la forme « cette ressource doit être libérée » sont le mieux exprimées par [RAII](009-resource.md#rr-raii).

##### Remarque

Idéalement, cet `Ensures` devrait faire partie de l'interface, mais ce n'est pas facile à faire.
Pour l'instant, nous le plaçons dans la définition (corps de la fonction).
Dès que le support du langage sera disponible (par exemple, voir la [proposition de contrat](https://www.open-std.org/jtc1/sc22/wg21/docs/papers/2016/p0380r1.pdf)), nous adopterons la version standard des préconditions, des postconditions et des assertions.

##### Application

(Non applicable) Trouver la variété des manières dont les postconditions peuvent être affirmées n'est pas réalisable. Émettre un avertissement pour celles qui peuvent être facilement identifiées (`assert()`) a une valeur discutable en l'absence d'une capacité du langage.

### <a name="ri-concepts"></a>I.9 : Si une interface est un gabarit, documenter ses paramètres à l'aide de concepts

##### Raison

Rendre l'interface précisément spécifiée et vérifiable à la compilation dans le (pas si lointain) futur.

##### Exemple

Utiliser le style C++20 de spécification des exigences. Par exemple :

    template<typename Iter, typename Val>
      requires input_iterator<Iter> && equality_comparable_with<iter_value_t<Iter>, Val>
    Iter find(Iter first, Iter last, Val v)
    {
        // ...
    }

**Voir aussi** : [Programmation générique](015-templates.md#ss-gp) et [concepts](015-templates.md#ss-concepts). <!-- @TODO-LINK : référence d'origine ambiguë (015-templates.md018-stdlib.md#ss-concepts) -->

##### Application

Avertir si un paramètre de gabarit non variadique n'est pas contraint par un concept (dans sa déclaration ou mentionné dans une clause `requires`).

### <a name="ri-except"></a>I.10 : Utiliser les exceptions pour signaler l'échec d'une tâche requise

##### Raison

Il ne devrait pas être possible d'ignorer une erreur, car cela pourrait laisser le système ou un calcul dans un état indéfini (ou inattendu).
C'est une source majeure d'erreurs.

##### Exemple

    int printf(const char* ...);    // mauvais : renvoie un nombre négatif si la sortie échoue

    template<class F, class ...Args>
    // bon : lève system_error si impossible de démarrer le nouveau thread
    explicit thread(F&& f, Args&&... args);

##### Remarque

Qu'est-ce qu'une erreur ?

Une erreur signifie que la fonction ne peut pas atteindre son but annoncé (y compris l'établissement des postconditions).
Un code appelant qui ignore une erreur peut conduire à des résultats erronés ou à un état système indéfini.
Par exemple, ne pas pouvoir se connecter à un serveur distant n'est pas en soi une erreur :
le serveur peut refuser une connexion pour toutes sortes de raisons, la chose naturelle est donc de renvoyer un résultat que l'appelant doit toujours vérifier.
Cependant, si l'échec à établir une connexion est considéré comme une erreur, alors l'échec doit lever une exception.

##### Exception

De nombreuses fonctions d'interface traditionnelles (par exemple, les gestionnaires de signaux UNIX) utilisent des codes d'erreur (par exemple, `errno`) pour signaler ce qui sont en réalité des codes de statut, plutôt que des erreurs. Vous n'avez pas de bonne alternative à l'utilisation de ceux-ci, donc appeler ces fonctions ne viole pas la règle.

##### Alternative

Si vous ne pouvez pas utiliser d'exceptions (par exemple, parce que votre code est rempli d'utilisation de pointeurs bruts de l'ancien style ou parce qu'il y a des contraintes temps réel strictes), envisagez d'utiliser un style qui renvoie une paire de valeurs :

    int val;
    int error_code;
    tie(val, error_code) = do_something();
    if (error_code) {
        // ... gérer l'erreur ou quitter ...
    }
    // ... utiliser val ...

Ce style conduit malheureusement à des variables non initialisées.
Depuis C++17, la fonctionnalité de « liaisons structurées » peut être utilisée pour initialiser directement les variables depuis la valeur de retour :

    auto [val, error_code] = do_something();
    if (error_code) {
        // ... gérer l'erreur ou quitter ...
    }
    // ... utiliser val ...

##### Remarque

Nous ne considérons pas la « performance » comme une raison valable de ne pas utiliser d'exceptions.

* Souvent, la vérification et la gestion explicites des erreurs consomment autant de temps et d'espace que la gestion d'exceptions.
* Souvent, un code plus propre produit de meilleures performances avec les exceptions (en simplifiant le traçage des chemins à travers le programme et leur optimisation).
* Une bonne règle pour le code sensible aux performances est de déplacer la vérification en dehors de la partie [critique](011-performance.md#rper-critical) du code.
* À plus long terme, un code plus régulier est mieux optimisé.
* Mesurez toujours [attentivement](011-performance.md#rper-measure) avant de faire des allégations de performance.

**Voir aussi** : [I.5](005-interfaces.md#ri-pre) et [I.7](005-interfaces.md#ri-post) pour le signalement des violations de préconditions et de postconditions.

##### Application

* (Non applicable) C'est une directive philosophique qui est irréalisable à vérifier directement.
* Chercher `errno`.

### <a name="ri-raw"></a>I.11 : Ne jamais transférer la propriété par un pointeur brut (`T*`) ou une référence (`T&`)

##### Raison

S'il existe le moindre doute sur le fait que l'appelant ou l'appelé possède l'objet, des fuites ou des destructions prématurées se produiront.

##### Exemple

Considérez :

    X* compute(args)    // à éviter
    {
        X* res = new X{};
        // ...
        return res;
    }

Qui supprime le `X` retourné ? Le problème serait plus difficile à détecter si `compute` renvoyait une référence.
Envisagez de renvoyer le résultat par valeur (utiliser la sémantique de déplacement si le résultat est volumineux) :

    vector<double> compute(args)  // bon
    {
        vector<double> res(10000);
        // ...
        return res;
    }

**Alternative** : [Passer la propriété](009-resource.md#rr-smartptrparam) à l'aide d'un « pointeur intelligent », comme `unique_ptr` (pour la propriété exclusive) et `shared_ptr` (pour la propriété partagée).
Cependant, c'est moins élégant et souvent moins efficace que de renvoyer l'objet lui-même,
donc n'utilisez les pointeurs intelligents que si des sémantiques de référence sont nécessaires.

**Alternative** : Parfois, l'ancien code ne peut pas être modifié en raison de contraintes de compatibilité ABI ou du manque de ressources.
Dans ce cas, marquez les pointeurs propriétaires à l'aide de `owner` de la [bibliothèque de support des directives](#gsl-guidelines-support-library) :

    owner<X*> compute(args)    // Il est maintenant clair que la propriété est transférée
    {
        owner<X*> res = new X{};
        // ...
        return res;
    }

Cela indique aux outils d'analyse que `res` est un propriétaire.
C'est-à-dire que sa valeur doit être supprimée par `delete` ou transférée à un autre propriétaire, comme c'est fait ici par le `return`.

`owner` est utilisé de manière similaire dans l'implémentation des poignées de ressources.

##### Remarque

Tout objet passé en tant que pointeur brut (ou itérateur) est supposé être possédé par l'appelant,
de sorte que sa durée de vie est gérée par l'appelant. Vu autrement :
les API de transfert de propriété sont relativement rares par rapport aux API de passage de pointeurs,
donc la valeur par défaut est « pas de transfert de propriété ».

**Voir aussi** : [Passage d'arguments](006-functions.md#rf-conventional), [utilisation d'arguments pointeur intelligent](009-resource.md#rr-smartptrparam), et [retour par valeur](006-functions.md#rf-value-return).

##### Application

* (Simple) Avertir sur le `delete` d'un pointeur brut qui n'est pas un `owner<T>`. Suggérer l'utilisation d'une poignée de ressources de la bibliothèque standard ou de `owner<T>`.
* (Simple) Avertir sur l'échec à soit `reset` soit `delete` explicitement un pointeur `owner` sur tous les chemins de code.
* (Simple) Avertir si la valeur de retour de `new` ou d'un appel de fonction avec une valeur de retour `owner` est assignée à un pointeur brut ou une référence non `owner`.

### <a name="ri-nullptr"></a>I.12 : Déclarer un pointeur qui ne doit pas être nul comme `not_null`

##### Raison

Pour aider à éviter les erreurs de déréférencement de `nullptr`.
Pour améliorer les performances en évitant les vérifications redondantes de `nullptr`.

##### Exemple

    int length(const char* p);            // il n'est pas clair si length(nullptr) est valide

    length(nullptr);                      // OK ?

    int length(not_null<const char*> p);  // mieux : nous pouvons supposer que p ne peut pas être nullptr

    int length(const char* p);            // nous devons supposer que p peut être nullptr

En énonçant l'intention dans le code source, les implémenteurs et les outils peuvent fournir de meilleurs diagnostics, comme la détection de certaines classes d'erreurs par analyse statique, et effectuer des optimisations, comme la suppression de branches et de tests de nullité.

##### Remarque

`not_null` est défini dans la [bibliothèque de support des directives](#gsl-guidelines-support-library).

##### Remarque

L'hypothèse que le pointeur vers `char` pointait vers une chaîne de style C (une chaîne de caractères terminée par zéro) restait implicite, et une source potentielle de confusion et d'erreurs. Utilisez `czstring` de préférence à `const char*`.

    // nous pouvons supposer que p ne peut pas être nullptr
    // nous pouvons supposer que p pointe vers un tableau de caractères terminé par zéro
    int length(not_null<czstring> p);

Note : `length()` est, bien sûr, `std::strlen()` déguisé.

##### Application

* (Simple) ((Fondations)) Si une fonction vérifie un paramètre pointeur contre `nullptr` avant accès, sur tous les chemins de flux de contrôle, alors avertir qu'il devrait être déclaré `not_null`.
* (Complexe) Si une fonction avec une valeur de retour pointeur garantit qu'elle n'est pas `nullptr` sur tous les chemins de retour, alors avertir que le type de retour devrait être déclaré `not_null`.

### <a name="ri-array"></a>I.13 : Ne pas passer un tableau en tant que simple pointeur

##### Raison

Les interfaces de style (pointeur, taille) sont sujettes aux erreurs. De plus, un simple pointeur (vers un tableau) doit s'appuyer sur une certaine convention pour permettre à la fonction appelée de déterminer la taille.

##### Exemple

Considérez :

    void copy_n(const T* p, T* q, int n); // copie de [p:p+n) vers [q:q+n)

Que se passe-t-il s'il y a moins de `n` éléments dans le tableau pointé par `q` ? Dans ce cas, nous écrasons une mémoire probablement sans rapport.
Que se passe-t-il s'il y a moins de `n` éléments dans le tableau pointé par `p` ? Dans ce cas, nous lisons une mémoire probablement sans rapport.
Les deux sont un comportement indéfini et un bug potentiellement très nuisible.

##### Alternative

Envisagez d'utiliser des spans explicites :

    void copy(span<const T> r, span<T> r2); // copie r vers r2

##### Exemple, mauvais

Considérez :

    void draw(Shape* p, int n);  // mauvaise interface ; mauvais code
    Circle arr[10];
    // ...
    draw(arr, 10);

Passer `10` en tant qu'argument `n` pourrait être une erreur : la convention la plus courante est de supposer `[0:n)` mais cela n'est nulle part énoncé. Pire encore est que l'appel de `draw()` a pu être compilé : il y a eu une conversion implicite du tableau en pointeur (décroissance de tableau) puis une autre conversion implicite de `Circle` en `Shape`. Il n'y a aucun moyen que `draw()` puisse itérer en sécurité à travers ce tableau : il n'a aucun moyen de connaître la taille des éléments.

**Alternative** : Utilisez une classe de support qui garantit que le nombre d'éléments est correct et empêche les conversions implicites dangereuses. Par exemple :

    void draw2(span<Circle>);
    Circle arr[10];
    // ...
    draw2(span<Circle>(arr));  // déduit le nombre d'éléments
    draw2(arr);    // déduit le type d'élément et la taille du tableau

    void draw3(span<Shape>);
    draw3(arr);    // erreur : ne peut pas convertir Circle[10] en span<Shape>

Ce `draw2()` passe la même quantité d'informations à `draw()`, mais rend explicite le fait qu'il est censé être un ensemble de `Circle`. Voir ???. <!-- @TODO-LINK : référence manquante dans le document -->

##### Exception

Utilisez `zstring` et `czstring` pour représenter des chaînes de style C, terminées par zéro.
Mais lors de leur utilisation, utilisez `std::string_view` ou `span<char>` de la [GSL](#gsl-guidelines-support-library) pour prévenir les erreurs de plage.

##### Application

* (Simple) ((Bornes)) Avertir pour toute expression qui s'appuierait sur la conversion implicite d'un type tableau en type pointeur. Permettre l'exception pour les types de pointeur zstring/czstring.
* (Simple) ((Bornes)) Avertir pour toute opération arithmétique sur une expression de type pointeur qui aboutit à une valeur de type pointeur. Permettre l'exception pour les types de pointeur zstring/czstring.

### <a name="ri-global-init"></a>I.22 : Éviter l'initialisation complexe des objets globaux

##### Raison

L'initialisation complexe peut conduire à un ordre d'exécution indéfini.

##### Exemple

    // fichier1.c

    extern const X x;

    const Y y = f(x);   // lit x ; écrit y

    // fichier2.c

    extern const Y y;

    const X x = g(y);   // lit y ; écrit x

Puisque `x` et `y` sont dans différentes unités de traduction, l'ordre des appels à `f()` et `g()` est indéfini ;
l'un d'eux accèdera à une `const` non initialisée.
Cela montre que le problème d'ordre d'initialisation pour les objets globaux (portée d'espace de noms) n'est pas limité aux *variables* globales.

##### Remarque

Les problèmes d'ordre d'initialisation deviennent particulièrement difficiles à gérer dans le code concourant.
Il est généralement préférable d'éviter complètement les objets globaux (portée d'espace de noms).

##### Application

* Signaler les initialiseurs de globaux qui appellent des fonctions non `constexpr`
* Signaler les initialiseurs de globaux qui accèdent à des objets `extern`

### <a name="ri-nargs"></a>I.23 : Limiter le nombre d'arguments de fonction

##### Raison

Avoir de nombreux arguments ouvre la porte à la confusion. Passer beaucoup d'arguments est souvent coûteux par rapport aux alternatives.

##### Discussion

Les deux raisons les plus courantes pour lesquelles les fonctions ont trop de paramètres sont :

1. *Absence d'abstraction.*
   Il manque une abstraction, de sorte qu'une valeur composée est passée en éléments individuels au lieu d'un seul objet qui impose un invariant.
   Cela n'élargit pas seulement la liste des paramètres, mais conduit à des erreurs car les valeurs composantes
   ne sont plus protégées par un invariant appliqué.

2. *Violation du principe « une fonction, une responsabilité ».
   La fonction essaie de faire plus d'un travail et devrait probablement être refactorisée.

##### Exemple

La `merge()` de la bibliothèque standard est à la limite de ce que nous pouvons gérer confortablement :

    template<class InputIterator1, class InputIterator2, class OutputIterator, class Compare>
    OutputIterator merge(InputIterator1 first1, InputIterator1 last1,
                         InputIterator2 first2, InputIterator2 last2,
                         OutputIterator result, Compare comp);

Notez que c'est en raison du problème 1 ci-dessus — absence d'abstraction. Au lieu de passer une plage (abstraction), la STL passe des paires d'itérateurs (valeurs composantes non encapsulées).

Ici, nous avons quatre arguments de gabarit et six arguments de fonction.
Pour simplifier les utilisations les plus fréquentes et les plus simples, l'argument de comparaison peut être par défaut à `<` :

    template<class InputIterator1, class InputIterator2, class OutputIterator>
    OutputIterator merge(InputIterator1 first1, InputIterator1 last1,
                         InputIterator2 first2, InputIterator2 last2,
                         OutputIterator result);

Cela ne réduit pas la complexité totale, mais réduit la complexité de surface présentée à de nombreux utilisateurs.
Pour vraiment réduire le nombre d'arguments, nous devons regrouper les arguments en abstractions de plus haut niveau :

    template<class InputRange1, class InputRange2, class OutputIterator>
    OutputIterator merge(InputRange1 r1, InputRange2 r2, OutputIterator result);

Regrouper les arguments en « lots » est une technique générale pour réduire le nombre d'arguments et augmenter les opportunités de vérification.

Alternativement, nous pourrions utiliser un concept de la bibliothèque standard pour définir la notion de trois types qui doivent être utilisables pour la fusion :

    template<class In1, class In2, class Out>
      requires mergeable<In1, In2, Out>
    Out merge(In1 r1, In2 r2, Out result);

##### Exemple

Les Profils de sécurité recommandent de remplacer

    void f(int* some_ints, int some_ints_length);  // MAUVAIS : style C, non sûr

par

    void f(gsl::span<int> some_ints);              // BON : sûr, bornes vérifiées

Ici, l'utilisation d'une abstraction apporte des avantages en matière de sûreté et de robustesse, et réduit naturellement aussi le nombre de paramètres.

##### Remarque

Combien de paramètres sont trop ? Essayez d'utiliser moins de quatre (4) paramètres.
Il existe des fonctions qui s'expriment le mieux avec quatre paramètres individuels, mais peu.

**Alternative** : Utilisez une meilleure abstraction : regroupez les arguments en objets significatifs et passez les objets (par valeur ou par référence).

**Alternative** : Utilisez des arguments par défaut ou des surcharges pour permettre les formes d'appels les plus courantes avec moins d'arguments.

##### Application

* Avertir lorsqu'une fonction déclare deux itérateurs (y compris des pointeurs) du même type au lieu d'une plage ou d'une vue.
* (Non applicable) C'est une directive philosophique qui est irréalisable à vérifier directement.

### <a name="ri-unrelated"></a>I.24 : Éviter les paramètres adjacents qui peuvent être appelés dans les deux ordres avec la même signature mais des significations différentes

##### Raison

Des arguments adjacents du même type sont facilement intervertis par erreur.

##### Exemple, mauvais

Considérez :

    void copy_n(T* p, T* q, int n);  // copie de [p:p + n) vers [q:q + n)

C'est une variante désagréable d'une interface de style C K&R. Il est facile d'inverser les arguments « vers » et « depuis ».

Utilisez `const` pour l'argument « depuis » :

    void copy_n(const T* p, T* q, int n);  // copie de [p:p + n) vers [q:q + n)

##### Exception

Si l'ordre des paramètres n'est pas important, il n'y a pas de problème :

    int max(int a, int b);

##### Alternative

Ne pas passer des tableaux en tant que pointeurs, passez un objet représentant une plage (par exemple, un `span`) :

    void copy_n(span<const T> p, span<T> q);  // copie de p vers q

##### Alternative

Définissez une `struct` comme type de paramètre et nommez les champs pour ces paramètres en conséquence :

    struct SystemParams {
        string config_file;
        string output_path;
        seconds timeout;
    };
    void initialize(SystemParams p);

Cela tend à rendre les appels clairs pour les lecteurs futurs, car les paramètres
sont souvent remplis par nom sur le site d'appel.

##### Remarque

Seul le concepteur de l'interface peut adéquatement traiter la source des violations de cette directive.

##### Stratégie d'application

(Simple) Avertir si deux paramètres consécutifs partagent le même type.

Nous cherchons toujours une application moins simple.

### <a name="ri-abstract"></a>I.25 : Préférer les classes abstraites vides en tant qu'interfaces aux hiérarchies de classes

##### Raison

Les classes abstraites vides (sans données membres non statiques) sont plus susceptibles d'être stables que les classes de base avec état.

##### Exemple, mauvais

Vous saviez que `Shape` allait apparaître quelque part :-)

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

Cela obligera chaque classe dérivée à calculer un centre — même si c'est non trivial et que le centre n'est jamais utilisé. De même, toutes les `Shape` n'ont pas une `Color`, et beaucoup de `Shape` sont mieux représentées sans contour défini comme une suite de `Point`. L'utilisation d'une classe abstraite est meilleure :

    class Shape {    // mieux : Shape est une pure interface
    public:
        virtual Point center() const = 0;   // fonctions virtuelles pures
        virtual void draw() const = 0;
        virtual void rotate(int) = 0;
        // ...
        // ... pas de membres de données ...
        // ...
        virtual ~Shape() = default;
    };

##### Application

(Simple) Avertir si un pointeur/référence à une classe `C` est assigné à un pointeur/référence à une classe de base de `C` et que la classe de base contient des membres de données.

### <a name="ri-abi"></a>I.26 : Si vous souhaitez une ABI inter-compilateurs, utiliser un sous-ensemble de style C

##### Raison

Différents compilateurs implémentent différentes dispositions binaires pour les classes, la gestion des exceptions, les noms de fonctions et d'autres détails d'implémentation.

##### Exception

Des ABI communes émergent sur certaines plateformes, vous affranchissant des restrictions les plus draconiennes.

##### Remarque

Si vous utilisez un seul compilateur, vous pouvez utiliser le C++ complet dans les interfaces. Cela pourrait nécessiter une recompilation après une mise à niveau vers une nouvelle version de compilateur.

##### Application

(Non applicable) Il est difficile d'identifier de manière fiable où une interface fait partie d'une ABI.

### <a name="ri-pimpl"></a>I.27 : Pour une ABI de bibliothèque stable, envisager l'idiome Pimpl

##### Raison

Parce que les membres de données privés participent à la disposition de classe et les fonctions membres privées participent à la résolution de la surcharge, les modifications de ces détails d'implémentation nécessitent la recompilation de tous les utilisateurs d'une classe qui les utilisent. Une classe d'interface non polymorphe tenant un pointeur vers l'implémentation (Pimpl) peut isoler les utilisateurs d'une classe des modifications de son implémentation au prix d'une indirection.

##### Exemple

interface (widget.h)

    class widget {
        class impl;
        std::unique_ptr<impl> pimpl;
    public:
        void draw(); // API publique qui sera transmise à l'implémentation
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

##### Remarques

Voir [GOTW #100](https://herbsutter.com/gotw/_100/) et [cppreference](https://en.cppreference.com/w/cpp/language/pimpl) pour les compromis et les détails d'implémentation supplémentaires associés à cet idiome.

##### Application

(Non applicable) Il est difficile d'identifier de manière fiable où une interface fait partie d'une ABI.

### <a name="ri-encapsulate"></a>I.30 : Encapsuler les violations de règles

##### Raison

Pour garder le code simple et sûr.
Parfois, des techniques moches, non sûres ou sujettes aux erreurs sont nécessaires pour des raisons logiques ou de performance.
Dans ce cas, garcz-les locales, plutôt que de « contaminer » les interfaces pour que des groupes plus larges de programmeurs soient conscients des subtilités.
La complexité d'implémentation ne devrait pas, si possible, fuir à travers les interfaces dans le code utilisateur.

##### Exemple

Considérez un programme qui, selon une forme d'entrée (par exemple, les arguments de `main`), doit consommer une entrée
depuis un fichier, depuis la ligne de commande, ou depuis l'entrée standard.
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
En particulier, quelqu'un doit se rappeler de quelque part écrire

    if (owned) delete inp;

Nous pourrions traiter cet exemple particulier en utilisant `unique_ptr` avec un destructeur spécial qui ne fait rien pour `cin`,
mais c'est compliqué pour les novices (qui peuvent facilement rencontrer ce problème) et l'exemple illustre un problème plus général
où une propriété que nous voudrions considérer statique (ici, la propriété) doit être traitée occasionnellement
à l'exécution.
Les exemples courants, les plus fréquents et les plus sûrs peuvent être traités statiquement, nous ne voulons donc pas ajouter de coût et de complexité à ceux-ci.
Mais nous devons aussi gérer les cas rares, moins sûrs et nécessairement plus coûteux.
De tels exemples sont discutés dans [[Str15]](https://www.stroustrup.com/resource-model.pdf).

Alors, nous écrivons une classe

    class Istream { [[gsl::suppress("lifetime")]]
    public:
        enum Opt { from_line = 1 };
        Istream() { }
        Istream(czstring p) : owned{true}, inp{new ifstream{p}} {}            // lire depuis un fichier
        Istream(czstring p, Opt) : owned{true}, inp{new istringstream{p}} {}  // lire depuis la ligne de commande
        ~Istream() { if (owned) delete inp; }
        operator istream&() { return *inp; }
    private:
        bool owned = false;
        istream* inp = &cin;
    };

Maintenant, la nature dynamique de la propriété de `istream` a été encapsulée.
Présumablement, un peu de vérification d'erreurs potentielles serait ajoutée dans un code réel.

##### Application

* Difficile, il est difficile de déterminer quel code de violation de règle est essentiel
* Signaler la suppression de règles qui permettent aux violations de règles de traverser les interfaces