# <a name="s-interfaces"></a>I: Interfaces

Un contrat est défini entre deux parties d'un programme. Définir précisément ce qui est attendu d'un fournisseur de service et d'un utilisateur de ce service est essentiel. Avoir des interfaces faciles à comprendre, favorisant un usage efficace, peu sujettes aux erreurs et facilitant les tests, constitue probablement l'aspect le plus important de l'organisation du code.

Interface rule summary:
- [I.1: Rendre les interfaces explicites](#ri-explicit)
- [I.2: Éviter les variables globales non `const`](#ri-global)
- [I.3: Éviter les singletons](#ri-singleton)
- [I.4: Rendre les interfaces précisément et fortement typées](#ri-typed)
- [I.5: Énoncer les préconditions (le cas échéant)](#ri-pre)
- [I.6: Préférer `Expects()` pour exprimer les préconditions](#ri-expects)
- [I.7: Énoncer les postconditions](#ri-post)
- [I.8: Préférer `Ensures()` pour exprimer les postconditions](#ri-ensures)
- [I.9: Si une interface est un modèle, documenter ses paramètres en utilisant des concepts](#ri-concepts)
- [I.10: Utiliser des exceptions pour signaler une erreur de tâche requise](#ri-except)
- [I.11: Ne jamais transférer la propriété via un pointeur brut (`T*`) ou une référence (`T&`)](#ri-raw)
- [I.12: Déclarer un pointeur qui ne doit pas être nul comme `not_null`](#ri-nullptr)
- [I.13: Ne pas passer un tableau comme un seul pointeur](#ri-array)
- [I.22: Éviter l'initialisation complexe des objets globaux](#ri-global-init)
- [I.23: Garder le nombre d'arguments de fonction faible](#ri-nargs)
- [I.24: Éviter les paramètres adjacents pouvant être invoqués par les mêmes arguments dans n'importe quel ordre avec une signification différente](#ri-unrelated)
- [I.25: Préférer les classes abstraites vides comme interfaces aux hiérarchies de classes](#ri-abstract)
- [I.26: Si vous désirez un ABI multiplateforme, utilisez un sous-ensemble de style C](#ri-abi)
- [I.27: Pour un ABI de bibliothèque stable, envisager l'idéone Pimpl](#ri-pimpl)
- [I.30: Encapsuler les violations de règle](#ri-encapsulate)

**Voir également**:
- [F: Functions](006-functions.md)
- [C.concrete: Concrete types](#ss-concrete) @TODO-LINK
- [C.hier: Class hierarchies](#ss-hier) @TODO-LINK
- [C.over: Overloading and overloaded operators](#ss-overload) @TODO-LINK
- [C.con: Containers and other resource handles](#ss-containers) @TODO-LINK
- [E: Error handling](013-errors.md)
- [T: Templates and generic programming](015-templates.md)

### <a name="ri-explicit"></a>I.1: Rendre les interfaces explicites

**Raison**

Correctitude. Les suppositions non énoncées dans une interface sont facilement négligées et difficiles à tester.

**Exemple, mauvais**

Contrôler le comportement d'une fonction via une variable globale (dans l'espace de noms) (un mode d'appel) est implicite et potentiellement source de confusion. Par exemple:

    int round(double d)
    {
        return (round_up) ? ceil(d) : d;    // ne pas : dépendance « invisible »
    }

Il ne sera pas évident pour un appelant que l'appel de `round(7.2)` puisse donner des résultats différents.

**Exception**

Parfois, nous contrôlons les détails d'un ensemble d'opérations à travers une variable d'environnement, par ex. sortie normale vs. verbeuse ou debug vs. optimisé. L'utilisation d'un contrôle non local peut prêter à confusion, mais elle ne contrôle que les détails d'implémentation d'une sémantique restée autrement fixe.

**Exemple, mauvais**

Un rapport via des variables non locales (p.ex. `errno`) est facile à ignorer. Par exemple:
    // ne pas : pas de test de la valeur de retour de fprintf
    fprintf(connection, "logging: %d %d %d\n", x, y, s);

Que se passe-t-il si la connexion est perdue, de sorte qu'aucune sortie de journalisation n'est produite ? Cf. I.??? @TODO-LINK.

**Alternative**: Lever une exception. Une exception ne peut pas être ignorée.

**Formulation alternative**: Éviter de transmettre des informations à travers une interface via un état non local ou implicite. Notez que les fonctions non constantes passent des informations à d’autres fonctions membres via l’état de leur objet.

**Formulation alternative**: Une interface devrait être une fonction ou un ensemble de fonctions. Les fonctions peuvent être des modèles de fonctions et les ensembles de fonctions peuvent être des classes ou des modèles de classe.

**Application**

- (Simple) Une fonction ne doit pas prendre de décisions de flux de contrôle basées sur les valeurs des variables déclarées à l'échelle de nom.
- (Simple) Une fonction ne doit pas écrire dans des variables déclarées à l'échelle de nom.

### <a name="ri-global"></a>I.2: Éviter les variables globales non `const`

**Raison**

Les variables globales non `const` cachent des dépendances et la rendent sujettes à des changements imprévisibles.

**Exemple**

    struct Data {
        // ... beaucoup de choses ...
    } data;            // data non-const

    void compute()     // ne pas
    {
        // ... utiliser data ...
    }

    void output()     // ne pas
    {
        // ... utiliser data ...
    }

Qui d'autre pourrait modifier `data` ?

**Avertissement**

L'initialisation des objets globaux n'est pas totalement ordonnée. Si vous utilisez un objet global, initialisez-le avec une constante. Notez qu'il est possible d'obtenir un ordre d'initialisation indéfini même pour les objets `const`.

**Exception**

Un objet global est souvent meilleur qu'un singleton.

**Remarque**

Les constantes globales sont utiles.

**Remarque**

La règle contre les variables globales s'applique également aux variables en espace de noms.

**Formulation alternative**: Si vous utilisez des données globales (ou plus généralement de l'échelle de nom) pour éviter la copie, envisagez de passer ces données comme un objet par référence const. Une autre solution consiste à définir les données comme l'état d'un objet et les opérations comme fonctions membres.

**Avertissement**: Méfiez-vous des conditions de course : si un fil peut accéder à des données non locales (ou données passées par référence) alors qu'un autre fil exécute le callee, nous pouvons avoir une condition de course. Chaque pointeur ou référence à des données mutables est un potentiel de course.

Utiliser des pointeurs ou références globaux pour accéder et changer des données non constantes n'est pas une meilleure alternative aux variables globales non constantes puisque cela ne résout pas les problèmes de dépendances cachées ou de conditions de course potentielles.

**Remarque**

Vous ne pouvez pas avoir une condition de course sur des données immuables.

**Références** : Voir les règles pour l'appel de fonctions (#ss-call) @TODO-LINK

**Remarque**

La règle est « éviter », pas « ne pas utiliser ». Évidemment il y aura des exceptions (rare), comme `cin`, `cout`, et `cerr`.

**Application**

- (Simple) Signaler toutes les variables non `const` déclarées à l'échelle de nom et les pointeurs/références globales vers des données non constantes.

### <a name="ri-singleton"></a>I.3: Éviter les singletons

**Raison**

Les singletons sont essentiellement des objets globaux compliqués déguisés.

**Exemple**

    class Singleton {
        // ... beaucoup de choses pour s'assurer que seul un Singleton est créé,
        // qu'il est initialisé correctement, etc.
    };

Il existe de nombreuses variantes de l'idée de singleton, c'est en partie le problème.

**Remarque**

Si vous ne souhaitez pas qu'un objet global change, déclarez-le `const` ou `constexpr`.

**Exception**

Vous pouvez utiliser le plus simple « singleton » (si simple qu'il n’est souvent pas considéré comme un singleton) pour obtenir l'initialisation à la première utilisation, si besoin :

    X& myX()
    {
        static X my_x {3};
        return my_x;
    }

C’est l’une des solutions les plus efficaces pour les problèmes liés à l’ordre d’initialisation. Dans un environnement multithread, l'initialisation d'un `static` local ne crée pas de condition de course (à moins d'accéder de façon négligée à un objet partagé depuis son constructeur).

Notez qu'une initialisation d'un `static` local ne signifie pas une condition de course. Cependant, si la destruction de `X` implique une opération qui doit être synchronisée, nous devons utiliser une solution moins simple. Par exemple:

    X& myX()
    {
        static auto p = new X {3};
        return *p;  // fuite potentielle
    }

Maintenant quelqu'un doit `delete` cet objet d'une manière thread-safe. C’est une erreur potentielle, donc nous n'utilisons pas cette technique à moins que

- `myX` soit dans un code multithread,
- que cet objet `X` doive être détruit (par ex. libération d'une ressource),
- que le code du destructeur de `X` doive être synchronisé.

Si vous, comme beaucoup, définissez un singleton comme une classe pour laquelle un seul objet est créé, des fonctions comme `myX` ne sont pas des singletons, et cette technique utile n’est pas une exception à la règle « pas de singleton ».

**Application**

Très difficile en général.

- Rechercher des classes dont le nom inclut `singleton`.
- Rechercher des classes pour lesquelles un seul objet est créé (en comptant les objets ou en examinant les constructeurs).
- Si une classe X possède une fonction statique publique qui contient un `static` local de type X et retourne un pointeur ou une référence vers celui‑ci, bannir cela.

### <a name="ri-typed"></a>I.4: Rendre les interfaces précisément et fortement typées

**Raison**

Les types sont la documentation la plus simple et la mieux documentée, améliorent la lisibilité grâce à leur signification bien définie et sont vérifiés à la compilation. De plus, un code typé précisément est souvent mieux optimisé.

**Exemple, ne pas**

Considérez :

    void pass(void* data);    // type faible et sous-qualifié, suspect

Les appelants ne savent pas quels types sont autorisés et si les données peuvent être modifiées car `const` n’est pas spécifié. Notez que tous les types de pointeur se convertissent implicitement à `void*`, il est donc facile pour un appelant de fournir cette valeur.

Le callee doit `static_cast` la donnée à un type vérifié pour l'utiliser. C’est sujet aux erreurs et verbeux.

Utilisez `const void*` uniquement pour passer des données dans des conceptions indescriptibles en C++. Envisagez d'utiliser un `variant` ou un pointeur vers la base à la place.

**Alternative** : Souvent, un paramètre modèle peut éliminer le `void*`, le transformant en `T*` ou `T&`. Pour le code générique, ces `T` peuvent être des paramètres de modèle générique ou être contrainte par des concepts.

**Exemple, mauvais**

Considérez :

    draw_rect(100, 200, 100, 500); // que signifient les nombres ?

    draw_rect(p.x, p.y, 10, 20); // quelles unités 10 et 20 représentent‑elles ?

Il est clair que l’appelant décrit un rectangle, mais il n’est pas clair quelles parties se rapportent à quels. De plus, un `int` peut porter des formes arbitraires d’information, incluant des valeurs de nombreuses unités, donc il faut deviner la signification des quatre `int`. Probablement, les deux premiers sont une paire de coordonnées `x`,`y`, mais que sont les deux derniers ?

Les commentaires et noms de paramètres peuvent aider, mais nous pouvons être explicites :

    void draw_rectangle(Point top_left, Point bottom_right);
    void draw_rectangle(Point top_left, Size height_width);

    draw_rectangle(p, Point{10, 20});  // deux coins
    draw_rectangle(p, Size{10, 20});   // un coin et un couple (hauteur, largeur)

Naturellement, nous ne pouvons pas attraper toutes les erreurs via le système de types statiques (ex. la première argument doit être un coin supérieur gauche) laissé par convention (naming et commentaires).

**Exemple, mauvais**

Considérez :

    set_settings(true, false, 42); // que signifient les nombres ?

Les types de paramètres ainsi que leurs valeurs ne communiquent pas quel réglage est spécifié ou ce que ces valeurs signifient.

Cette conception est plus explicite, sûre et lisible :

    alarm_settings s{};
    s.enabled = true;
    s.displayMode = alarm_settings::mode::spinning_light;
    s.frequency = alarm_settings::every_10_seconds;
    set_settings(s);

Pour le cas d'un ensemble de valeurs booléennes, envisagez un `enum` de drapeaux ; un motif qui exprime un ensemble de valeurs booléennes.

    enable_lamp_options(lamp_option::on | lamp_option::animate_state_transitions);

**Exemple, mauvais**

Dans l'exemple suivant, il n'est pas clair dans l'interface ce que `time_to_blink` signifie : secondes ? millisecondes ?

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

**Exemple, bon**

Les types `std::chrono::duration` aident à rendre l'unité explicite :

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

La fonction peut également être écrite de telle façon qu'elle accepte n'importe quelle unité de durée.

    template<class rep, class period>
    void blink_led(duration<rep, period> time_to_blink) // bon -- accepte n'importe quelle unité
    {
        // supposons que millisecond est l'unité la plus petite pertinente
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

**Application**

- (Simple) Signaler l'utilisation de `void*` comme paramètre ou type de retour.
- (Simple) Signaler l'utilisation de plus d'un booléen paramètre.
- (Diffique) Rechercher des fonctions qui utilisent trop d'arguments de type primitif.

### <a name="ri-pre"></a>I.5: Énoncer les préconditions (le cas échéant)

**Raison**

Les arguments ont une signification qui peut restreindre leur utilisation appropriée dans l'appelé.

**Exemple**

Considérez :

    double sqrt(double x);

Ici `x` doit être non négatif. Le système de types ne peut pas (facilement et naturellement) l'exprimer, il faut donc d'autres moyens. Par exemple :

    double sqrt(double x); // x doit être non négatif

Certaines préconditions peuvent être exprimées comme assertions. Par exemple :

    double sqrt(double x) { Expects(x >= 0); /* ... */ }

Idéalement, cette `Expects(x >= 0)` devrait faire partie de l'interface de `sqrt()` mais ce n’est pas facile à faire. Pour l'instant, nous la plaçons dans la définition (corps de fonction).

**Références** : `Expects()` est décrite dans les [directives de soutien GSL](#gsl-guidelines-support-library) @TODO-LINK

**Remarque**

Préférer une spécification formelle des exigences, comme `Expects(p);`. Si cela est irréalisable, utiliser du texte anglais dans les commentaires, tel que `// la séquence [p:q) est triée en utilisant <`.

**Remarque**

La plupart des fonctions membres ont comme précondition qu'une certaine invariant de classe tient. Cet invariant est établi par un constructeur et doit être rétabli à la sortie par chaque fonction membre appelée depuis l'extérieur de la classe. Nous n'avons pas besoin de le mentionner pour chaque fonction membre.

**Application**

(Not enforceable)

**Voir également** : les règles pour passer des pointeurs. @TODO-LINK

### <a name="ri-expects"></a>I.6: Préférer `Expects()` pour exprimer les préconditions

**Raison**

Pour mettre en évidence qu'une condition est une précondition et permettre l'utilisation d'outils.

**Exemple**

    int area(int height, int width)
    {
        Expects(height > 0 && width > 0);            // bon
        if (height <= 0 || width <= 0) my_error();   // obscur
        // ...
    }

**Remarque**

Les préconditions peuvent être exprimées de plusieurs façons, y compris des commentaires, des instructions `if` et `assert()`. Cela les rend difficiles à distinguer du code ordinaire, difficiles à mettre à jour, difficiles à manipuler par des outils, et peuvent avoir la mauvaise sémantique (dois‑je toujours aborter en mode debug et rien ne vérifier en mode production ?).

**Remarque**

Les préconditions devraient faire partie de l'interface plutôt que de l'implémentation, mais nous n'avons pas encore la capacité linguistique pour le faire. Une fois l'appui de la langue disponible (p.ex. voir la [proposition de contrat](https://www.open-std.org/jtc1/sc22/wg21/docs/papers/2016/p0380r1.pdf)), nous adopterons la version standard des préconditions, postconditions et assertions.

**Remarque**

`Expects()` peut également être utilisé pour vérifier une condition en plein milieu d'un algorithme.

**Remarque**

Non, utiliser `unsigned` n'est pas un bon moyen de contourner le problème de [assurer qu'une valeur est non négative](#res-nonnegative) @TODO-LINK

**Application**

(Not enforceable) Trouver la variété de façons dont les préconditions peuvent être vérifiées n'est pas faisable. Avertir ceux qui peuvent être identifiés facilement (assert()) a une valeur douteuse en l'absence d'un support langue.

### <a name="ri-post"></a>I.7: Énoncer les postconditions

**Raison**

Pour détecter les malentendus sur le résultat et éventuellement détecter des implémentations erronées.

**Exemple, mauvais**

Considérez :

    int area(int height, int width) { return height * width; }  // mauvais

Ici, nous avons accidentellement laissé de côté la spécification de précondition, donc il n'est pas clair que height et width doivent être positifs. Nous avons également omis la spécification de postcondition, donc il n'est pas évident que l'algorithme (`height * width`) soit incorrect pour des surfaces > le plus grand entier. Une déformation peut survenir. Considérez :

    int area(int height, int width)
    {
        auto res = height * width;
        Ensures(res > 0);
        return res;
    }

**Exemple, mauvais**

Considérez un bogue de sécurité célèbre :

    void f()    // problématique
    {
        char buffer[MAX];
        // ...
        memset(buffer, 0, sizeof(buffer));
    }

Il n'y avait pas de postcondition indiquant que le tampon devait être effacé et l'optimiseur a éliminé l'appel `memset()` apparemment redondant :

    void f()    // meilleur
    {
        char buffer[MAX];
        // ...
        memset(buffer, 0, sizeof(buffer));
        Ensures(buffer[0] == 0);
    }

**Remarque**

Les postconditions sont souvent exprimées de façon informelle dans un commentaire indiquant la finalité d'une fonction ; `Ensures()` peut être utilisé pour rendre cela plus systématique, visible et vérifiable.

**Remarque**

Les postconditions sont d'autant plus importantes lorsqu'elles concernent quelque chose qui n’est pas directement reflété dans un résultat retourné, tel qu'un état d'une structure de données utilisée.

**Exemple**

Considérez une fonction qui manipule une `Record`, utilisant un `mutex` pour éviter les conditions de course :

    mutex m;

    void manipulate(Record& r)    // ne pas
    {
        m.lock();
        // ... pas de m.unlock() ...
    }

Ici, nous « avons oublié » d'indiquer que le `mutex` devrait être libéré, donc nous ne savons pas si l'échec d'assurer la libération du `mutex` était un bug ou un trait. Afficher la postcondition aurait clarifié :

    void manipulate(Record& r)    // postcondition : m est débloqué à la sortie
    {
        m.lock();
        // ... pas de m.unlock() ...
    }

Le bug devient maintenant évident (mais uniquement d'un humain lisant les commentaires).

**Mieux encore**, utilisez [RAII](#rr-raii) @TODO-LINK afin d'assurer que la postcondition (« le verrou doit être libéré ») est respectée dans le code :

    void manipulate(Record& r)    // meilleur
    {
        lock_guard<mutex> _ {m};
        // ...
    }

**Remarque**

Idéalement, les postconditions sont exprimées dans l'interface/déclaration afin que les utilisateurs puissent les voir le plus aisément. Seules les postconditions relatives aux utilisateurs peuvent être exprimées dans l'interface. Les postconditions relatives uniquement à l'état interne appartiennent à la définition/implémentation.

**Application**

(Not enforceable) Ceci est un principe directif qui n’est pas réalisable à vérifier dans le cas général. Des vérificateurs spécifiques aux domaines (comme les vérificateurs de détention de verrou) existent pour de nombreuses chaînes d'outils.

### <a name="ri-ensures"></a>I.8: Préférer `Ensures()` pour exprimer les postconditions

**Raison**

Pour mettre en évidence qu'une condition est une postcondition et permettre l'utilisation d'outils.

**Exemple**

    void f()
    {
        char buffer[MAX];
        // ...
        memset(buffer, 0, MAX);
        Ensures(buffer[0] == 0);
    }

**Remarque**

Les postconditions peuvent être exprimées de plusieurs façons, y compris des commentaires, des instructions `if` et `assert()`. Cela les rend difficiles à distinguer du code ordinaire, difficiles à mettre à jour, difficiles à manipuler par des outils, et peuvent avoir la mauvaise sémantique.

**Alternative** : Les postconditions de la forme « cette ressource doit être libérée » sont mieux exprimées par [RAII](#rr-raii) @TODO-LINK.

**Remarque**

Ideally, this `Ensures` should be part of the interface, but that's not easily done. For now, we place it in the definition (function body). Once language support becomes available (e.g., see the [contract proposal](https://www.open-std.org/jtc1/sc22/wg21/docs/papers/2016/p0380r1.pdf)), we will adopt the standard version of preconditions, postconditions, and assertions.

**Application**

(Not enforceable) Trouver la variété de façons que les postconditions peuvent être vérifiées n'est pas faisable. Avertir ceux qui peuvent être identifiés facilement (assert()) a une valeur douteuse en l'absence d'un support langue.

### <a name="ri-concepts"></a>I.9: Si une interface est un modèle, documenter ses paramètres en utilisant des concepts

**Raison**

Spécifier l'interface de façon précise et vérifiable à la compilation dans un futur proche.

**Exemple**

Utiliser la spécification de exigences de la C++20. Par ex. :

    template<typename Iter, typename Val>
      requires input_iterator<Iter> && equality_comparable_with<iter_value_t<Iter>, Val>
    Iter find(Iter first, Iter last, Val v)
    {
        // ...
    }

**Voir également** : [Programmation générique](#ss-gp) @TODO-LINK et [concepts](#ss-concepts) @TODO-LINK.

**Application**

Avertir si tout paramètre de modèle non var-adic n’est pas restreint par un concept (dans sa déclaration ou mentionné dans une clause `requires`).

### <a name="ri-except"></a>I.10: Utiliser des exceptions pour signaler une erreur de tâche requise

**Raison**

Il ne devrait pas être possible d'ignorer une erreur car cela pourrait laisser le système ou une computation dans un état non défini (ou inattendu). C'est une source majeure d'erreur.

**Exemple**

    int printf(const char* ...);    // mauvais : retourne un nombre négatif si l'affichage échoue

    template<class F, class ...Args>
    // bon : lancer `system_error` si impossible de démarrer le nouveau thread
    explicit thread(F&& f, Args&&... args);

**À propos de qu'est une erreur?**

Une erreur signifie que la fonction ne peut pas atteindre son objectif annoncé (y compris l'établissement des postconditions). Ignorer une erreur peut conduire à des résultats erronés ou à des états système indéfinis. Par exemple, ne pas pouvoir se connecter à un serveur distant n’est pas en soi une erreur : le serveur peut refuser la connexion pour de nombreuses raisons, donc la chose naturelle est de retourner un résultat que l'appelant devrait toujours vérifier. Cependant, si l'échec d'établir une connexion est considéré comme une erreur, alors une erreur devrait lancer une exception.

**Exception**

De nombreuses fonctions d'interface traditionnelles (p.ex. des gestionnaires de signal UNIX) utilisent des codes d'erreur (p.ex. `errno`) pour rapporter ce qui sont en fait des codes de statut, et non des erreurs. Vous n'avez pas de bonne alternative à l'utilisation de tels, donc appeler ces fonctions ne viole pas la règle.

**Alternative**

Si vous ne pouvez pas utiliser des exceptions (par ex. votre code est plein d'utilisation de pointeur brut ou a des contraintes temps réel hard), envisagez un style qui renvoie une paire de valeurs :

    int val;
    int error_code;
    tie(val, error_code) = do_something();
    if (error_code) {
        // ... gérer l'erreur ou quitter ...
    }
    // ... utiliser val ...

Ce style malheureusement conduit à des variables non initialisées. Depuis C++17, la fonctionnalité de *bindings structurés* peut être utilisée pour initialiser des variables directement à partir de la valeur de retour :

    auto [val, error_code] = do_something();
    if (error_code) {
        // ... gérer l'erreur ou quitter ...
    }
    // ... utiliser val ...

**À propos de performance**.

* On ne considère pas la performance comme une raison valide de ne pas utiliser des exceptions.
* Souvent, la vérification explicite et la gestion des erreurs consomment autant de temps et d'espace que le traitement d'exception.
* Souvent, un code plus propre donne une meilleure performance grâce à l'optimisation des chemins d'exécution du programme.
* Une bonne règle pour le code critique est de déplacer les vérifications hors de la partie [critical](#rper-critical) du code (???).
* À long terme, un code plus régulier est mieux optimisé.
* Mesurer soigneusement avant de faire des déclarations de performance.

**Voir également** : [I.5](#ri-pre) et [I.7](#ri-post) pour le signalement des violations de précondition et postcondition.

**Application**

- (Not enforceable) C’est un principe philosophique qui n’est pas faisable à vérifier directement.
- Rechercher `errno`.

### <a name="ri-raw"></a>I.11: Ne jamais transférer la propriété via un pointeur brut (`T*`) ou une référence (`T&`)

**Raison**

Si un doute persiste que l'appelant ou le callee possède un objet, des fuites ou des destructions prématurées surviendront.

**Exemple**

Considérez :

    X* compute(args)    // ne pas
    {
        X* res = new X{};
        // ...
        return res;
    }

Qui supprime le `X` retourné ? Le problème serait plus difficile à repérer si `compute` retournait une référence. Considérez : retourner le résultat par valeur (utiliser le passage par valeur ou *move semantics* si le résultat est volumineux) :

    vector<double> compute(args)  // bon
    {
        vector<double> res(10000);
        // ...
        return res;
    }

**Alternative** : [Pass ownership](#rr-smartptrparam) @TODO-LINK en utilisant un «pointeur intelligent», tel que `unique_ptr` (pour la propriété exclusive) ou `shared_ptr` (pour la propriété partagée). Cependant, cela est moins élégant et souvent moins efficace que retourner l'objet lui‑même, donc utilisez les pointeurs intelligents uniquement si la sémantique de référence est nécessaire.

**Alternative** : Parfois, un ancien code ne peut être modifié à cause de contraintes de compatibilité ABI ou de ressources manquantes. Dans ce cas, marquez les pointeurs propriétaires en utilisant `owner` de la [bibliothèque de soutien GSL](#gsl-guidelines-support-library) @TODO-LINK :

    owner<X*> compute(args)    // Le ownership est clairement transféré
    {
        owner<X*> res = new X{};
        // ...
        return res;
    }

Ceci indique aux outils d’analyse que `res` est un owner. Autrement dit, sa valeur doit être `delete` ou transféré à un autre owner, comme c'est le cas ici via le `return`.

`owner` est utilisé de façon similaire dans l'implémentation des handles de ressources.

**Note**

Chaque objet passé sous forme de pointeur brut (ou d’itérateur) est supposé être la propriété de l'appelant, de sorte que sa durée de vie est gérée par celui‑ci. Autrement, les API de transfert de propriété sont relativement rares comparées aux API de passage de pointeur. L'**adresse par défaut** est donc : « pas de transfert de propriété ».

**Voir aussi** : [Passage d'arguments](#rf-conventional) @TODO-LINK, [utilisation d’arguments de pointeur intelligents](#rr-smartptrparam) @TODO-LINK et [retour de valeur](#rf-value-return) @TODO-LINK.

**Application**

- (Simple) Avertir sur `delete` d'un pointeur brut qui n’est pas `owner<T>`. Suggérer l'utilisation d'un handle de ressources de la bibliothèque standard ou de `owner<T>`.
- (Simple) Avertir sur l'absence de `reset` ou sur la suppression explicite d'un `owner` sur chaque chemin d'exécution.
- (Simple) Avertir si la valeur de retour d'un `new` ou d'un appel de fonction retournant un `owner` est assignée à un pointeur brut ou à une référence non-`owner`.

### <a name="ri-nullptr"></a>I.12: Déclarer un pointeur qui ne doit pas être nul comme `not_null`

**Raison**

Pour éviter des erreurs de dereference `nullptr`. Pour améliorer la performance en supprimant les vérifications redondantes de `nullptr`.

**Exemple**

    int length(const char* p);            // il n'est pas clair si length(nullptr) est valide

    length(nullptr);                      // OK ?

    int length(not_null<const char*> p);  // mieux : on peut supposer que p ne peut être nullptr

    int length(const char* p);            // on doit supposer que p peut être nullptr

En déclarant l’intention dans le code source, les implémenteurs et les outils peuvent fournir de meilleurs diagnostics, comme l'identification de certains groupes d'erreurs via l'analyse statique, et réaliser des optimisations, comme l'élimination des branches et des tests `nullptr`.

**Note**

`not_null` est défini dans la [bibliothèque de soutien GSL](#gsl-guidelines-support-library) @TODO-LINK.

**Note**

L'hypothèse que le pointeur `char*` pointe vers une chaîne de caractères de type C (une chaîne terminée par zéro) est toujours implicite et peut être source de confusion et d'erreur. Utilisez `czstring` en lieu et place de `const char*`.

    // on peut supposer que p ne peut être nullptr
    // on peut supposer que p pointe vers un tableau nul-terminé de caractères
    int length(not_null<czstring> p);

Note : `length()` est, bien sûr, `std::strlen()` en déguisement.

**Application**

- (Simple) ((Fondation)) Si une fonction teste un pointeur paramètre contre `nullptr` avant l’accès, sur tous les chemins de contrôle, alors avertir qu’elle devrait être déclarée `not_null`.
- (Complexe) Si une fonction avec un retour pointeur garantit qu'il n'est pas `nullptr` sur tous les chemins de retour, avertir que le type de retour devrait être déclaré `not_null`.

### <a name="ri-array"></a>I.13: Ne pas passer un tableau comme un seul pointeur

**Raison**

Les interfaces de style (pointeur, taille) sont sujettes aux erreurs. De plus, un pointeur simple (vers tableau) doit compter sur une convention pour permettre à l'appelant de déterminer la taille.

**Exemple**

Considérez :

    void copy_n(const T* p, T* q, int n); // copier de [p:p+n) vers [q:q+n)

Que se passe‑t-il s'il y a moins de `n` éléments dans le tableau pointées par `q` ? Alors, nous surchargerons probablement de la mémoire non liée. Que se passe‑t-il s'il y a moins de `n` éléments dans le tableau pointé par `p` ? Alors, nous lisons probablement hors limites. Les deux sont un comportement indéfini et un bug potentiellement très grave.

**Alternative**

Considérez l’utilisation de `span` explicite :

    void copy(span<const T> r, span<T> r2); // copier r vers r2

**Exemple, mauvais**

Considérez :

    void draw(Shape* p, int n);  // interface médiocre
    Circle arr[10];
    // ...
    draw(arr, 10);

Passer `10` comme argument `n` peut être une erreur : la convention la plus courante suppose `[0:n)` mais cela n’est jamais indiqué. De pire, l’appel à `draw()` compile : il y a une conversion implicite de tableau en pointeur (decay) puis une conversion de `Circle` en `Shape`. Il n'existe aucun moyen pour `draw()` d'itérer en toute sécurité à travers ce tableau : il n'a aucun moyen de connaître la taille des éléments.

**Alternative** : utilisez une classe de support assurant que le nombre d'éléments est correct et empêchant les conversions implicites dangereuses. Par ex. :

    void draw2(span<Circle>);
    Circle arr[10];
    // ...
    draw2(span<Circle>(arr));  // déduire le nombre d’éléments
    draw2(arr);    // déduire le type d’objet et la taille du tableau

    void draw3(span<Shape>);
    draw3(arr);    // erreur : ne peut pas convertir Circle[10] en span<Shape>

Cette `draw2()` transmet la même quantité d'information à `draw()`, mais rend explicite que c’est censé être une plage de `Circle`s. Voir ???.

**Exception**

Utilisez `zstring` et `czstring` pour représenter les chaînes de caractères zéro-terminées. Mais lorsque vous faites cela, utilisez `std::string_view` ou `span<char>` du [GSL](#gsl-guidelines-support-library) @TODO-LINK pour prévenir les erreurs de plage.

**Application**

- (Simple) ((Bornes)) Avertir toute expression qui dépendrait d’une conversion implicite d’un type de tableau en type pointeur. Autoriser l'exception aux types `zstring`/`czstring` pointeurs.
- (Simple) ((Bornes)) Avertir toute opération arithmétique sur une expression de type pointeur qui produit une valeur de type pointeur. Autoriser l'exception aux types `zstring`/`czstring` pointeurs.

### <a name="ri-global-init"></a>I.22: Éviter l'initialisation complexe des objets globaux

**Raison**

Une initialisation complexe peut conduire à un ordre d'exécution indéfini.

**Exemple**

    // file1.cpp

    extern const X x;

    const Y y = f(x);   // lit x, écrit y

    // file2.cpp

    extern const Y y;

    const X x = g(y);   // lit y, écrit x

Comme `x` et `y` se trouvent dans différents modules de traduction, l'ordre des appels à `f()` et `g()` est indéfini ; l'un accède à un `const` non initialisé. Cela démontre que les problèmes d’ordre d'initialisation ne se limitent pas aux variables globales.

**Remarque**

Les problèmes d'ordre d'initialisation deviennent particulièrement difficiles à gérer dans le code concurrent. Il est habituellement préférable d’éviter complètement les objets globaux de l’espace de noms.

**Application**

- Signaler les initialisateurs de globales qui appellent des fonctions non constexpr.
- Signaler les initialisateurs de globales qui accèdent à des objets externes.

### <a name="ri-nargs"></a>I.23: Garder le nombre d'arguments de fonction faible

**Raison**

Avoir beaucoup d'arguments ouvre des opportunités de confusion. Passer beaucoup d'arguments est souvent coûteux comparé aux alternatives.

**Discussion**

Les deux raisons les plus fréquentes pour lesquelles les fonctions ont trop d'arguments sont :

1. *Manque d’abstraction.* Il manque une abstraction, donc une valeur composite est passée comme éléments individuels au lieu d’un unique objet qui impose une invariant. Cela ne fait pas seulement que la liste d'arguments croît, mais il y a erreur parce que les valeurs des composants ne sont plus protégées par une invariant imposée.

2. *Violation de « une fonction, une responsabilité ».* La fonction essaie de faire plus d'une tâche, et doit probablement être refactorisée.

**Exemple**

La `merge()` de la bibliothèque standard est à la limite de ce que nous pouvons gérer de façon confortable :

    template<class InputIterator1, class InputIterator2, class OutputIterator, class Compare>
    OutputIterator merge(InputIterator1 first1, InputIterator1 last1,
                         InputIterator2 first2, InputIterator2 last2,
                         OutputIterator result, Compare comp);

Notez qu’il s’agit d’un problème #1 ci‑dessus — manque d’abstraction. Au lieu de passer un range (abstraction), STLa a passé des paires d’itérateurs (non encapsulés). 

Pour simplifier l’usage le plus fréquent, le paramètre de comparaison peut être par défaut à `<` :

    template<class InputIterator1, class InputIterator2, class OutputIterator>
    OutputIterator merge(InputIterator1 first1, InputIterator1 last1,
                         InputIterator2 first2, InputIterator2 last2,
                         OutputIterator result);

Cela ne diminue pas la complexité globale mais réduit la surface de complexité présentée aux utilisateurs fréquents.

Pour vraiment réduire le nombre d'arguments, nous devons regrouper les arguments dans des abstractions de niveau supérieur :

    template<class InputRange1, class InputRange2, class OutputIterator>
    OutputIterator merge(InputRange1 r1, InputRange2 r2, OutputIterator result);

Regrouper les arguments en « bundles » est une technique générale pour réduire le nombre d'arguments et augmenter les opportunités de vérification.

**Exemple**

Les profils de sécurité recommandent de remplacer

    void f(int* some_ints, int some_ints_length);  // BAD : C style, unsafe

par

    void f(gsl::span<int> some_ints);              // GOOD : sécurisé, vérifié en borne

Parler d’une abstraction a des bénéfices en sûreté et robustesse, et naturellement réduit aussi le nombre d’arguments.

**Remarque**

Combien d’arguments sont trop nombreux ? Essayez d’utiliser moins de quatre (4) paramètres. Il y a des fonctions qui sont meilleures avec quatre paramètres individuels, mais pas beaucoup.

**Alternative** : Utiliser une meilleure abstraction : grouper les arguments dans des objets significatifs et les passer par valeur ou référence.

**Alternative** : Utiliser des arguments par défaut ou surnoms pour permettre les formes d’appels les plus courantes à être faites avec moins d'arguments.

**Application**

- Avertir lorsqu’une fonction déclare deux itérateurs (incluant les pointeurs) du même type au lieu d’un range ou d’une vue.
- (Not enforceable) Ceci est un principe guidé qui n’est pas réalisable à vérifier directement.

### <a name="ri-unrelated"></a>I.24: Éviter les paramètres adjacents pouvant être invoqués par les mêmes arguments dans n'importe quel ordre avec une signification différente

**Raison**

Les arguments adjacents du même type sont facilement inversés par erreur.

**Exemple, mauvais**

Considérez :

    void copy_n(T* p, T* q, int n);  // copier de [p:p+n) vers [q:q+n)

C’est une mauvaise variante d’une interface style K&R C. Il est facile d’inverser les arguments « vers » et « de ».

Utiliser `const` pour l’argument « de » :

    void copy_n(const T* p, T* q, int n);  // copier de [p:p+n) vers [q:q+n)

**Exception**

Si l'ordre des paramètres n’est pas important, il n’y a pas de problème :

    int max(int a, int b);

**Alternative**

Ne pas donner de pointeur de tableau, donnez un objet qui représente une plage (p. ex. `span`) :

    void copy_n(span<const T> p, span<T> q);  // copier p à q

**Alternative**

Définir une structure comme type du paramètre et nommer les champs pour ces paramètres :

    struct SystemParams {
        string config_file;
        string output_path;
        seconds timeout;
    };
    void initialize(SystemParams p);

Cela tend à rendre les appels lisibles aux futurs lecteurs, car les paramètres sont souvent remplis par nom à l’appel.

**Remarque**

Ce n’est qu’au concepteur de l’interface que l’on peut aborder la source des violations.

**Stratégie d’application**

(Simple) Avertir si deux paramètres consécutifs partagent le même type.

Nous cherchons encore une technique moins simple.

### <a name="ri-abstract"></a>I.25: Préférer les classes abstraites vides comme interfaces aux hiérarchies de classes

**Raison**

Une classe abstraite vide (sans données membres non statiques) est plus susceptible d’être stable que des classes de base avec état.

**Exemple, mauvais**

Vous n'avez tout simplement pas vu que `Shape` était là :

    class Shape {  // mauvais : interface chargée de données
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

Cela forcerait chaque classe dérivée à calculer un centre — même si c'est non triviale et que le centre n’est jamais utilisé. De même, aucun `Shape` ne possède une `Color`, et beaucoup de `Shape` seraient mieux représentées sans un `Outline` de `Point`.

Utiliser une classe abstraite pure :

    class Shape {    // meilleur : interface abstraite
    public:
        virtual Point center() const = 0;   // fonction pure virtuelle
        virtual void draw() const = 0;
        virtual void rotate(int) = 0;
        // ...
        // ... pas de membres de données ...
        virtual ~Shape() = default;
    };

**Application**

(Simple) Avertir si un pointeur/référence à une classe `C` est assigné à un pointeur/référence vers une classe de base de `C` et que la classe de base contient des membres de données.

### <a name="ri-abi"></a>I.26: Si vous désirez un ABI multiplateforme, utilisez un sous-ensemble de style C

**Raison**

Les compilateurs différents implémentent des emplacements binaires différents pour les classes, la gestion des exceptions, les noms de fonctions, etc.

**Exception**

Les ABIs communs émergent sur certaines plateformes qui vous libèrent des restrictions draconiennes.

**Remarque**

Si vous utilisez un seul compilateur, vous pouvez utiliser le plein C++ dans les interfaces. Cela peut nécessiter une recompilation après chaque mise à jour vers une nouvelle version de compilateur.

**Application**

(Not enforceable) Il est difficile d'identifier fiablement où l'interface constitue une partie d'un ABI.

### <a name="ri-pimpl"></a>I.27: Pour un ABI de bibliothèque stable, envisager l'idéone Pimpl

**Raison**

Car les membres privés participent au layout des classes et à la résolution d'overload, les changements à ces détails d’implémentation nécessitent la recompilation de tous les utilisateurs d'une classe. Une classe d'interface non-polymorphe qui contient un pointeur vers l'implémentation (Pimpl) peut isoler les utilisateurs de la classe des changements de son implémentation en échange d'une indirection.

**Exemple**

interface (widget.h)

    class widget {
        class impl;
        std::unique_ptr<impl> pimpl;
    public:
        void draw(); // public API qui sera redirigé vers l'implémentation
        widget(int); // défini dans le fichier d'implémentation
        ~widget();   // défini dans le fichier d'implémentation, où impl est un type complet
        widget(widget&&) noexcept; // défini dans le fichier d'implémentation
        widget(const widget&) = delete;
        widget& operator=(widget&&) noexcept; // défini dans le fichier d'implémentation
        widget& operator=(const widget&) = delete;
    };

implementation (widget.cpp)

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

**Notes**

Voir [GOTW #100](https://herbsutter.com/gotw/_100/) et [cppreference](https://en.cppreference.com/w/cpp/language/pimpl) pour les compromis, et les détails supplémentaires d’implémentation associés à cette idiom.

**Application**

(Not enforceable) Il est difficile d'identifier fiablement où l'interface est dans un ABI.

### <a name="ri-encapsulate"></a>I.30: Encapsuler les violations de règle

**Raison**

Pour garder le code simple et sûr. Parfois, des techniques peu esthétiques, non sécurisées ou susceptibles au bug sont nécessaires pour des raisons logiques ou de performance. Dans ce cas, les garder localement plutôt que "infecter" les interfaces afin que les plus grands groupes de programmeurs n’aient pas à se soucier des subtilités.

**Exemple**

Considérons un program

    bool owned;
    owner<istream*> inp;
    switch (source) {
    case std_in:        owned = false; inp = &cin;                       break;
    case command_line:  owned = true;  inp = new istringstream{argv[2]}; break;
    case file:          owned = true;  inp = new ifstream{argv[2]};      break;
    }
    istream& in = *inp;

Cela violait les règles contre l'initialisation non propre, la règle contre l'ignorer ownership et la règle contre les constantes magiques (#res-always) @TODO-LINK, (#ri-raw), (#res-magic) @TODO-LINK. En particulier, quelqu'un doit se souvenir d'écrire

    if (owned) delete inp;

Nous pourrions gérer cette particularité en utilisant `unique_ptr` avec un deleter spécial qui ne fait rien pour `cin`, mais c’est compliqué pour les novices. 

Nous écrivons donc une classe

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

Maintenant, la nature dynamique de l'ownership d`istream` est encapsulée. Presum

ivement, un peu de vérification fera l'affaire en code réel.

**Application**

- Difficile, il est difficile de décider quel code interdépendant est essentiel.
- Marquer l'emprunt de suppression qui permet cross-interfaces de violations de règle.