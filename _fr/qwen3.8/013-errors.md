# <a name="s-errors"></a>E : Gestion des erreurs

La gestion des erreurs implique :

* La détection d'une erreur
* La transmission d'informations sur l'erreur à un code de gestion
* Le maintien d'un état valide du programme
* L'évitement des fuites de ressources

Il n'est pas possible de récupérer de toutes les erreurs. Si la récupération d'une erreur est impossible, il est important de « sortir » rapidement d'une manière bien définie. Une stratégie de gestion des erreurs doit être simple, sinon elle devient une source d'erreurs encore plus graves. Le code de gestion des erreurs non testé et rarement exécuté est lui-même la source de nombreux bogues.

Les règles sont conçues pour aider à éviter plusieurs types d'erreurs :

* Violations de type (p. ex., mauvaise utilisation des `union` et des casts)
* Fuites de ressources (y compris les fuites mémoire)
* Erreurs de bornes
* Erreurs de durée de vie (p. ex., accès à un objet après son `delete`)
* Erreurs de complexité (erreurs logiques rendues probables par une expression trop complexe des idées)
* Erreurs d'interface (p. ex., une valeur inattendue est transmise à travers une interface)

Résumé des règles de gestion des erreurs :

* [E.1 : Élaborer une stratégie de gestion des erreurs tôt dans la conception](013-errors.md#re-design)
* [E.2 : Lancer une exception pour signaler qu'une fonction ne peut pas accomplir sa tâche](013-errors.md#re-throw)
* [E.3 : Utiliser les exceptions uniquement pour la gestion des erreurs](013-errors.md#re-errors)
* [E.4 : Concevoir sa stratégie de gestion des erreurs autour des invariants](013-errors.md#re-design-invariants)
* [E.5 : Laisser un constructeur établir un invariant, et lancer une exception s'il y parvient pas](013-errors.md#re-invariant)
* [E.6 : Utiliser le RAII pour prévenir les fuites](013-errors.md#re-raii)
* [E.7 : Énoncer ses préconditions](013-errors.md#re-precondition)
* [E.8 : Énoncer ses postconditions](013-errors.md#re-postcondition)

* [E.12 : Utiliser `noexcept` lorsque la sortie d'une fonction par `throw` est impossible ou inacceptable](013-errors.md#re-noexcept)
* [E.13 : Ne jamais lancer une exception en étant le propriétaire direct d'un objet](013-errors.md#re-never-throw)
* [E.14 : Utiliser des types définis par l'utilisateur conçus à cet effet comme exceptions (et non des types intégrés)](013-errors.md#re-exception-types)
* [E.15 : Lancer par valeur, capturer les exceptions d'une hiérarchie par référence](013-errors.md#re-exception-ref)
* [E.16 : Les destructeurs, la libération mémoire, `swap` et la construction par copie/déplacement des types d'exception ne doivent jamais échouer](013-errors.md#re-never-fail)
* [E.17 : Ne pas essayer de capturer toutes les exceptions dans chaque fonction](013-errors.md#re-not-always)
* [E.18 : Minimiser l'utilisation explicite de `try`/`catch`](013-errors.md#re-catch)
* [E.19 : Utiliser un objet `final_action` pour exprimer un nettoyage si aucun gestionnaire de ressource approprié n'est disponible](013-errors.md#re-finally)

* [E.25 : Si vous ne pouvez pas lancer d'exceptions, simuler le RAII pour la gestion des ressources](013-errors.md#re-no-throw-raii)
* [E.26 : Si vous ne pouvez pas lancer d'exceptions, envisager d'échouer rapidement](013-errors.md#re-no-throw-crash)
* [E.27 : Si vous ne pouvez pas lancer d'exceptions, utiliser des codes d'erreur de manière systématique](013-errors.md#re-no-throw-codes)
* [E.28 : Éviter la gestion des erreurs basée sur un état global (p. ex. `errno`)](013-errors.md#re-no-throw)

* [E.30 : Ne pas utiliser les spécifications d'exceptions](013-errors.md#re-specifications)
* [E.31 : Ordonner correctement ses clauses `catch`](013-errors.md#re_catch)

### <a name="re-design"></a>E.1 : Élaborer une stratégie de gestion des erreurs tôt dans la conception

##### Justification

Il est difficile de rétro-fitter une stratégie cohérente et complète de gestion des erreurs et des fuites de ressources dans un système existant.

### <a name="re-throw"></a>E.2 : Lancer une exception pour signaler qu'une fonction ne peut pas accomplir sa tâche

##### Justification

Pour rendre la gestion des erreurs systématique, robuste et non redondante.

##### Exemple

    struct Foo {
        vector<Thing> v;
        File_handle f;
        string s;
    };

    void use()
    {
        Foo bar { {Thing{1}, Thing{2}, Thing{monkey} }, {"my_file", "r"}, "Here we go!"};
        // ...
    }

Ici, les constructeurs de `vector` et de `string` ne peuvent pas allouer suffisamment de mémoire pour leurs éléments, le constructeur de `vector` ne peut pas copier les `Thing` de sa liste d'initialisation, et `File_handle` ne peut pas ouvrir le fichier requis.
Dans chaque cas, ils lancent une exception pour que l'appelant de `use()` puisse la gérer.
Si `use()` peut gérer l'échec de la construction de `bar`, il peut reprendre le contrôle à l'aide de `try`/`catch`.
Dans les deux cas, le constructeur de `Foo` détruit correctement les membres déjà construits avant de rendre le contrôle à celui qui a tenté de créer un `Foo`.
Remarquez qu'il n'y a pas de valeur de retour qui pourrait contenir un code d'erreur.

Le constructeur de `File_handle` pourrait être défini ainsi :

    File_handle::File_handle(const string& name, const string& mode)
        : f{fopen(name.c_str(), mode.c_str())}
    {
        if (!f)
            throw runtime_error{"File_handle: could not open " + name + " as " + mode};
    }

##### Remarque

On dit souvent que les exceptions sont destinées à signaler des événements exceptionnels et des échecs.
Cependant, c'est un peu circulaire car « qu'est-ce qui est exceptionnel ? »
Exemples :

* Une précondition qui ne peut pas être satisfaite
* Un constructeur qui ne peut pas construire un objet (échec à établir l'[invariant](007-class.md#rc-struct) @TODO-LINK de sa classe)
* Une erreur de dépassement de plage (p. ex., `v[v.size()] = 7`)
* L'impossibilité d'acquérir une ressource (p. ex., le réseau est en panne)

En revanche, la terminaison d'une boucle ordinaire n'est pas exceptionnelle.
Sauf si la boucle était censée être infinie, la terminaison est normale et attendue.

##### Remarque

Ne pas utiliser un `throw` comme simple alternative pour retourner une valeur d'une fonction.

##### Exception

Certains systèmes, tels que les systèmes temps réel dur, exigent une garantie qu'une action est effectuée dans un temps maximal constant (généralement court) connu avant le début de l'exécution. De tels systèmes ne peuvent utiliser les exceptions que s'il existe un support d'outils permettant de prédire précisément le temps maximal de récupération d'un `throw`.

**Voir aussi** : [RAII](013-errors.md#re-raii)

**Voir aussi** : [discussion](028-discussion.md#sd-noexcept) @TODO-LINK

##### Remarque

Avant de décider que vous ne pouvez pas vous permettre ou que vous n'aimez pas la gestion des erreurs basée sur les exceptions, jetez un œil aux [alternatives](013-errors.md#re-no-throw-raii) ;
elles ont leurs propres complexités et problèmes.
De plus, dans la mesure du possible, mesurez avant de faire des affirmations sur l'efficacité.

### <a name="re-errors"></a>E.3 : Utiliser les exceptions uniquement pour la gestion des erreurs

##### Justification

Pour garder la gestion des erreurs séparée du « code ordinaire ».
Les implémentations C++ ont tendance à être optimisées sur la base de l'hypothèse que les exceptions sont rares.

##### Exemple, à éviter

    // à éviter : exception non utilisée pour la gestion des erreurs
    int find_index(vector<string>& vec, const string& x)
    {
        try {
            for (gsl::index i = 0; i < vec.size(); ++i)
                if (vec[i] == x) throw i;  // x trouvé
        }
        catch (int i) {
            return i;
        }
        return -1;   // non trouvé
    }

Ceci est plus compliqué et s'exécute probablement beaucoup plus lentement que l'alternative évidente.
Il n'y a rien d'exceptionnel à trouver une valeur dans un `vector`.

##### Application

Devrait être heuristique.
Rechercher des valeurs d'exception « fuites » hors des clauses `catch`.

### <a name="re-design-invariants"></a>E.4 : Concevoir sa stratégie de gestion des erreurs autour des invariants

##### Justification

Pour utiliser un objet, il doit être dans un état valide (défini formellement ou informellement par un invariant) et pour récupérer d'une erreur, chaque objet non détruit doit être dans un état valide.

##### Remarque

Un [invariant](007-class.md#rc-struct) @TODO-LINK est une condition logique sur les membres d'un objet qu'un constructeur doit établir pour que les fonctions membres publiques puissent la supposer.

##### Application

???

### <a name="re-invariant"></a>E.5 : Laisser un constructeur établir un invariant, et lancer une exception s'il y parvient pas

##### Justification

Laisser un objet sans son invariant établi est une invitation aux ennuis.
Toutes les fonctions membres ne peuvent pas être appelées.

##### Exemple

    class Vector {  // très simplifié : vector de doubles
        // si elem != nullptr alors elem pointe vers sz doubles
    public:
        Vector() : elem{nullptr}, sz{0}{}
        Vector(int s) : elem{new double[s]}, sz{s} { /* initialiser les éléments */ }
        ~Vector() { delete [] elem; }
        double& operator[](int s) { return elem[s]; }
        // ...
    private:
        owner<double*> elem;
        int sz;
    };

L'invariant de classe — ici énoncé en commentaire — est établi par les constructeurs.
`new` lance une exception s'il ne peut pas allouer la mémoire requise.
Les opérateurs, notamment l'opérateur d'indexation, s'appuient sur l'invariant.

**Voir aussi** : [Si un constructeur ne peut pas construire un objet valide, lancer une exception](007-class.md#rc-throw) @TODO-LINK

##### Application

Signaler les classes avec un état `private` sans constructeur (public, protégé ou privé).

### <a name="re-raii"></a>E.6 : Utiliser le RAII pour prévenir les fuites

##### Justification

Les fuites sont généralement inacceptables.
La libération manuelle des ressources est source d'erreurs.
Le RAII (« Resource Acquisition Is Initialization ») est la manière la plus simple et la plus systématique de prévenir les fuites.

##### Exemple

    void f1(int i)   // Mauvais : fuite possible
    {
        int* p = new int[12];
        // ...
        if (i < 17) throw Bad{"in f()", i};
        // ...
    }

Nous pourrions soigneusement libérer la ressource avant le throw :

    void f2(int i)   // Maladroit et source d'erreurs : libération explicite
    {
        int* p = new int[12];
        // ...
        if (i < 17) {
            delete[] p;
            throw Bad{"in f()", i};
        }
        // ...
    }

Ceci est verbeux. Dans un code plus volumineux avec plusieurs `throw` possibles, les libérations explicites deviennent redondantes et source d'erreurs.

    void f3(int i)   // OK : gestion des ressources par un gestionnaire (mais voir ci-dessous)
    {
        auto p = make_unique<int[]>(12);
        // ...
        if (i < 17) throw Bad{"in f()", i};
        // ...
    }

Remarquez que cela fonctionne même lorsque le `throw` est implicite car il s'est produit dans une fonction appelée :

    void f4(int i)   // OK : gestion des ressources par un gestionnaire (mais voir ci-dessous)
    {
        auto p = make_unique<int[]>(12);
        // ...
        helper(i);   // peut lancer une exception
        // ...
    }

À moins d'avoir vraiment besoin de sémantique de pointeur, utilisez un objet ressource local :

    void f5(int i)   // OK : gestion des ressources par un objet local
    {
        vector<int> v(12);
        // ...
        helper(i);   // peut lancer une exception
        // ...
    }

C'est encore plus simple et plus sûr, et souvent plus efficace.

##### Remarque

S'il n'y a pas de gestionnaire de ressource évident et que pour une raison quelconque définir un objet/gestionnaire RAII approprié est irréalisable,
en dernier recours, les actions de nettoyage peuvent être représentées par un objet [`final_action`](013-errors.md#re-finally).

##### Remarque

Mais que faire si nous écrivons un programme où les exceptions ne peuvent pas être utilisées ?
D'abord, mettez en doute cette hypothèse ; il y a beaucoup de mythes anti-exceptions.
Nous ne connaissons que quelques bonnes raisons :

* Nous sommes sur un système si petit que le support des exceptions consommerait la majeure partie de nos 2 Ko de mémoire.
* Nous sommes dans un système temps réel dur et nous n'avons pas d'outils qui nous garantissent qu'une exception est gérée dans le temps requis.
* Nous sommes dans un système avec beaucoup de code legacy utilisant de nombreux pointeurs de manière difficile à comprendre
  (en particulier sans stratégie de propriété reconnaissable) de sorte que les exceptions pourraient causer des fuites.
* Notre implémentation des mécanismes d'exceptions C++ est déraisonnablement médiocre
(lente, consommatrice de mémoire, ne fonctionnant pas correctement pour les bibliothèques liées dynamiquement, etc.).
Plaignez-vous auprès de votre fournisseur d'implémentation ; si aucun utilisateur ne se plaint, aucune amélioration n'aura lieu.
* Nous sommes licenciés si nous remettons en question la sagesse ancestrale de notre manager.

Seule la première de ces raisons est fondamentale, donc dans la mesure du possible, utilisez les exceptions pour implémenter le RAII, ou concevez vos objets RAII pour ne jamais échouer.
Lorsque les exceptions ne peuvent pas être utilisées, simulez le RAII.
C'est-à-dire, vérifiez systématiquement que les objets sont valides après construction et libérez toujours toutes les ressources dans le destructeur.
Une stratégie consiste à ajouter une opération `valid()` à chaque gestionnaire de ressource :

    void f()
    {
        vector<string> vs(100);   // pas std::vector : valid() ajouté
        if (!vs.valid()) {
            // gérer l'erreur ou quitter
        }

        ifstream fs("foo");   // pas std::ifstream : valid() ajouté
        if (!fs.valid()) {
            // gérer l'erreur ou quitter
        }

        // ...
    } // les destructeurs nettoient comme d'habitude

Évidemment, cela augmente la taille du code, ne permet pas la propagation implicite des « exceptions » (vérifications `valid()`), et les vérifications `valid()` peuvent être oubliées.
Préférez l'utilisation des exceptions.

**Voir aussi** : [Utilisation de `noexcept`](013-errors.md#re-noexcept)

##### Application

???

### <a name="re-precondition"></a>E.7 : Énoncer ses préconditions

##### Justification

Pour éviter les erreurs d'interface.

**Voir aussi** : [règle des préconditions](005-interfaces.md#ri-pre) @TODO-LINK

### <a name="re-postcondition"></a>E.8 : Énoncer ses postconditions

##### Justification

Pour éviter les erreurs d'interface.

**Voir aussi** : [règle des postconditions](005-interfaces.md#ri-post) @TODO-LINK

### <a name="re-noexcept"></a>E.12 : Utiliser `noexcept` lorsque la sortie d'une fonction par `throw` est impossible ou inacceptable

##### Justification

Pour rendre la gestion des erreurs systématique, robuste et efficace.

##### Exemple

    double compute(double d) noexcept
    {
        return log(sqrt(d <= 0 ? 1 : d));
    }

Ici, nous savons que `compute` ne lancera pas d'exception car il est composé d'opérations qui ne lancent pas d'exception.
En déclarant `compute` comme `noexcept`, nous fournissons au compilateur et aux lecteurs humains des informations qui peuvent leur faciliter la compréhension et la manipulation de `compute`.

##### Remarque

De nombreuses fonctions de la bibliothèque standard sont `noexcept`, y compris toutes les fonctions de la bibliothèque standard « héritées » de la bibliothèque standard C.

##### Exemple

    vector<double> munge(const vector<double>& v) noexcept
    {
        vector<double> v2(v.size());
        // ... faire quelque chose ...
    }

Le `noexcept` ici indique que je ne suis pas disposé ou capable de gérer la situation où je ne peux pas construire le `vector` local.
C'est-à-dire que je considère l'épuisement de la mémoire comme une erreur de conception grave (au même titre que les pannes matérielles) et que je suis prêt à faire planter le programme si cela se produit.

##### Remarque

Ne pas utiliser les [spécifications d'exceptions](013-errors.md#re-specifications) traditionnelles.

##### Voir aussi

[discussion](028-discussion.md#sd-noexcept) @TODO-LINK.

### <a name="re-never-throw"></a>E.13 : Ne jamais lancer une exception en étant le propriétaire direct d'un objet

##### Justification

Cela serait une fuite.

##### Exemple

    void leak(int x)   // à éviter : fuite possible
    {
        auto p = new int{7};
        if (x < 0) throw Get_me_out_of_here{};  // peut fuir *p
        // ...
        delete p;   // nous n'atteindrons peut-être jamais cette ligne
    }

Un moyen d'éviter ce type de problème est d'utiliser des gestionnaires de ressources de manière cohérente :

    void no_leak(int x)
    {
        auto p = make_unique<int>(7);
        if (x < 0) throw Get_me_out_of_here{};  // supprimera *p si nécessaire
        // ...
        // pas besoin de delete p
    }

Une autre solution (souvent meilleure) consisterait à utiliser une variable locale pour éliminer l'utilisation explicite de pointeurs :

    void no_leak_simplified(int x)
    {
        vector<int> v(7);
        // ...
    }

##### Remarque

Si vous avez un « truc » local qui nécessite un nettoyage, mais qui n'est pas représenté par un objet avec un destructeur, ce nettoyage doit
également être effectué avant un `throw`.
Parfois, [`finally()`](013-errors.md#re-finally) peut rendre ce type de nettoyage non systématique un peu plus gérable.

### <a name="re-exception-types"></a>E.14 : Utiliser des types définis par l'utilisateur conçus à cet effet comme exceptions (et non des types intégrés)

##### Justification

Un type défini par l'utilisateur peut mieux transmettre des informations sur une erreur à un gestionnaire. Les
informations peuvent être encodées dans le type lui-même et le type est peu susceptible d'entrer en conflit avec les exceptions d'autres personnes.

##### Exemple

    throw 7; // mauvais

    throw "something bad";  // mauvais

    throw std::exception{}; // mauvais - aucune information

Dériger de `std::exception` offre la flexibilité de capturer l'exception spécifique ou de la gérer de manière générale via `std::exception` :

    class MyException : public std::runtime_error
    {
    public:
        MyException(const string& msg) : std::runtime_error{msg} {}
        // ...
    };

    // ...

    throw MyException{"something bad"};  // bon

Les exceptions n'ont pas besoin d'être dérivées de `std::exception` :

    class MyCustomError final {};  // non dérivé de std::exception

    // ...

    throw MyCustomError{};  // bon - les gestionnaires doivent capturer ce type (ou ...)

Les types de bibliothèque dérivés de `std::exception` peuvent être utilisés comme exceptions génériques si
aucune information utile ne peut être ajoutée au point de détection :

    throw std::runtime_error("something bad"); // bon

    // ...

    throw std::invalid_argument("i is not even"); // bon

Les classes `enum` sont également autorisées :

    enum class alert {RED, YELLOW, GREEN};

    throw alert::RED; // bon

##### Application

Capturer les `throw` de types intégrés et de `std::exception`.

### <a name="re-exception-ref"></a>E.15 : Lancer par valeur, capturer les exceptions d'une hiérarchie par référence

##### Justification

Lancer par valeur (et non par pointeur) et capturer par référence empêche la copie, en particulier le troncage des sous-objets de base.

##### Exemple ; mauvais

    void f()
    {
        try {
            // ...
            throw new widget{}; // à éviter : lancer par valeur, pas par pointeur brut
            // ...
        }
        catch (base_class e) {  // à éviter : risque de troncature
            // ...
        }
    }

Au lieu de cela, utilisez une référence :

    catch (base_class& e) { /* ... */ }

ou — généralement encore mieux — une référence `const` :

    catch (const base_class& e) { /* ... */ }

La plupart des gestionnaires ne modifient pas leur exception et en général nous [recommandons l'utilisation de `const`](010-expr.md#res-const) @TODO-LINK.

##### Remarque

Capturer par valeur peut être approprié pour un petit type de valeur tel qu'une valeur `enum`.

##### Remarque

Pour relancer une exception capturée, utilisez `throw;` et non `throw e;`. Utiliser `throw e;` lancerait une nouvelle copie de `e` (tronquée au type statique `std::exception`, lorsque l'exception est capturée par `catch (const std::exception& e)`) au lieu de relancer l'exception originale de type `std::runtime_error`. (Mais gardez en tête [Ne pas essayer de capturer toutes les exceptions dans chaque fonction](013-errors.md#re-not-always) et [Minimiser l'utilisation explicite de `try`/`catch`](013-errors.md#re-catch).)

##### Application

* Signaler la capture par valeur d'un type qui a une fonction virtuelle.
* Signaler le lancement de pointeurs bruts.

### <a name="re-never-fail"></a>E.16 : Les destructeurs, la libération mémoire, `swap` et la construction par copie/déplacement des types d'exception ne doivent jamais échouer

##### Justification

Nous ne savons pas comment écrire des programmes fiables si un destructeur, un swap, une libération mémoire ou une tentative de construction par copie/déplacement d'un objet d'exception échoue ; c'est-à-dire s'il sort par une exception ou simplement n'effectue pas son action requise.

##### Exemple, à éviter

    class Connection {
        // ...
    public:
        ~Connection()   // À éviter : très mauvais destructeur
        {
            if (cannot_disconnect()) throw I_give_up{information};
            // ...
        }
    };

##### Remarque

Beaucoup ont essayé d'écrire du code fiable en violant cette règle, par exemple pour une connexion réseau qui « refuse de se fermer ».
À notre connaissance, personne n'a trouvé de manière générale de le faire.
Parfois, pour des exemples très spécifiques, on peut se contenter de définir un état pour un nettoyage ultérieur.
Par exemple, nous pourrions mettre un socket qui ne veut pas se fermer sur une liste de « mauvais sockets »,
à examiner lors d'un balayage régulier de l'état du système.
Chaque exemple que nous avons vu de cela est source d'erreurs, spécialisé et souvent bogué.

##### Remarque

La bibliothèque standard suppose que les destructeurs, les fonctions de libération (p. ex., `operator delete`) et `swap` ne lancent pas d'exception. S'ils le font, les invariants de base de la bibliothèque standard sont brisés.

##### Remarque

* Les fonctions de libération, y compris `operator delete`, doivent être `noexcept`.
* Les fonctions `swap` doivent être `noexcept`.
* La plupart des destructeurs sont implicitement `noexcept` par défaut.
* De plus, [rendre les opérations de déplacement `noexcept`](007-class.md#rc-move-noexcept) @TODO-LINK.
* Si vous écrivez un type destiné à être utilisé comme type d'exception, assurez-vous que son constructeur de copie est `noexcept`. En général, nous ne pouvons pas l'appliquer mécaniquement, car nous ne savons pas si un type est destiné à être utilisé comme type d'exception.
* Essayez de ne pas `throw` un type dont le constructeur de copie n'est pas `noexcept`. En général, nous ne pouvons pas l'appliquer mécaniquement, car même `throw std::string(...)` pourrait lancer une exception mais ne le fait pas en pratique.

##### Application

* Capturer les destructeurs, les opérations de libération et les `swap` qui lancent une exception.
* Capturer ces opérations qui ne sont pas `noexcept`.

**Voir aussi** : [discussion](028-discussion.md#sd-never-fail) @TODO-LINK

### <a name="re-not-always"></a>E.17 : Ne pas essayer de capturer toutes les exceptions dans chaque fonction

##### Justification

Capturer une exception dans une fonction qui ne peut pas prendre d'action de récupération significative conduit à la complexité et au gaspillage.
Laissez une exception se propager jusqu'à ce qu'elle atteigne une fonction qui peut la gérer.
Laissez les actions de nettoyage sur le chemin de déroulement de la pile être gérées par le [RAII](013-errors.md#re-raii).

##### Exemple, à éviter

    void f()   // mauvais
    {
        try {
            // ...
        }
        catch (...) {
            // aucune action
            throw;   // propager l'exception
        }
    }

##### Application

* Signaler les blocs try imbriqués.
* Signaler les fichiers de code avec un ratio trop élevé de blocs try par rapport aux fonctions. (??? Problème : définir « trop élevé »)

### <a name="re-catch"></a>E.18 : Minimiser l'utilisation explicite de `try`/`catch`

##### Justification

`try`/`catch` est verbeux et les utilisations non triviales sont source d'erreurs.
`try`/`catch` peut être le signe d'une gestion des ressources et/ou des erreurs non systématique et/ou de bas niveau.

##### Exemple, mauvais

    void f(zstring s)
    {
        Gadget* p;
        try {
            p = new Gadget(s);
            // ...
            delete p;
        }
        catch (Gadget_construction_failure) {
            delete p;
            throw;
        }
    }

Ce code est désordonné.
Il pourrait y avoir une fuite depuis le pointeur nu dans le bloc `try`.
Toutes les exceptions ne sont pas gérées.
`delete` d'un objet qui a échoué à se construire est presque certainement une erreur.
Mieux :

    void f2(zstring s)
    {
        Gadget g {s};
    }

##### Alternatives

* des gestionnaires de ressources appropriés et le [RAII](013-errors.md#re-raii)
* [`finally`](013-errors.md#re-finally)

##### Application

??? difficile, nécessite une heuristique

### <a name="re-finally"></a>E.19 : Utiliser un objet `final_action` pour exprimer un nettoyage si aucun gestionnaire de ressource approprié n'est disponible

##### Justification

`finally` de la [GSL](#gsl-guidelines-support-library) @TODO-LINK est moins verbeux et plus difficile à mal faire que `try`/`catch`.

##### Exemple

    void f(int n)
    {
        void* p = malloc(n);
        auto _ = gsl::finally([p] { free(p); });
        // ...
    }

##### Remarque

`finally` n'est pas aussi désordonné que `try`/`catch`, mais c'est toujours ad hoc.
Préférez des [objets de gestion des ressources appropriés](013-errors.md#re-raii).
Considérez `finally` comme un dernier recours.

##### Remarque

L'utilisation de `finally` est une alternative systématique et raisonnablement propre à l'ancienne [technique `goto exit;`](013-errors.md#re-no-throw-codes)
pour gérer le nettoyage lorsque la gestion des ressources n'est pas systématique.

##### Application

Heuristique : détecter `goto exit;`

### <a name="re-no-throw-raii"></a>E.25 : Si vous ne pouvez pas lancer d'exceptions, simuler le RAII pour la gestion des ressources

##### Justification

Même sans exceptions, le [RAII](013-errors.md#re-raii) est généralement la meilleure et la plus systématique manière de gérer les ressources.

##### Remarque

La gestion des erreurs à l'aide d'exceptions est la seule manière complète et systématique de gérer les erreurs non locales en C++.
En particulier, signaler de manière non intrusive l'échec de la construction d'un objet nécessite une exception.
Signaler des erreurs d'une manière qui ne peut pas être ignorée nécessite des exceptions.
Si vous ne pouvez pas utiliser les exceptions, simulez leur utilisation autant que possible.

Beaucoup de craintes envers les exceptions sont infondées.
Lorsqu'elles sont utilisées pour des circonstances exceptionnelles dans un code qui n'est pas jonché de pointeurs et de structures de contrôle compliquées,
la gestion des exceptions est presque toujours abordable (en temps et en espace) et mène presque toujours à un meilleur code.
Ceci suppose bien sûr une bonne implémentation des mécanismes de gestion des exceptions, qui n'est pas disponible sur tous les systèmes.
Il y a aussi des cas où les problèmes ci-dessus ne s'appliquent pas, mais où les exceptions ne peuvent pas être utilisées pour d'autres raisons.
Certains systèmes temps réel dur en sont un exemple : une opération doit être terminée dans un temps fixe avec une erreur ou une réponse correcte.
En l'absence d'outils appropriés d'estimation du temps, c'est difficile à garantir pour les exceptions.
De tels systèmes (p. ex. le logiciel de contrôle de vol) interdisent généralement également l'utilisation de la mémoire dynamique (tas).

Ainsi, la règle principale pour la gestion des erreurs est « utiliser les exceptions et le [RAII](013-errors.md#re-raii). »
Cette section traite des cas où vous n'avez pas une implémentation efficace des exceptions,
ou où vous avez un tel enchevêtrement de code de l'ancien style
(p. ex., beaucoup de pointeurs, une propriété mal définie, et beaucoup de gestion des erreurs non systématique basée sur des tests de codes d'erreur)
qu'il est irréalisable d'introduire une gestion des exceptions simple et systématique.

Avant de condamner les exceptions ou de vous plaindre trop de leur coût, considérez des exemples d'utilisation de [codes d'erreur](013-errors.md#re-no-throw-codes).
Considérez le coût et la complexité de l'utilisation de codes d'erreur.
Si les performances sont votre préoccupation, mesurez.

##### Exemple

Supposons que vous vouliez écrire

    void func(zstring arg)
    {
        Gadget g {arg};
        // ...
    }

Si le `gadget` n'est pas correctement construit, `func` sort avec une exception.
Si nous ne pouvons pas lancer d'exception, nous pouvons simuler ce style de gestion des ressources RAII en ajoutant une fonction membre `valid()` à `Gadget` :

    error_indicator func(zstring arg)
    {
        Gadget g {arg};
        if (!g.valid()) return gadget_construction_error;
        // ...
        return 0;   // zéro indique « bon »
    }

Le problème est bien sûr que l'appelant doit maintenant se souvenir de tester la valeur de retour. Pour l'encourager à le faire, envisagez d'ajouter un `[[nodiscard]]`.

**Voir aussi** : [Discussion](#sd-???) @TODO-LINK

##### Application

Possible (uniquement) pour des versions spécifiques de cette idée : p. ex., tester la vérification systématique de `valid()` après la construction d'un gestionnaire de ressource

### <a name="re-no-throw-crash"></a>E.26 : Si vous ne pouvez pas lancer d'exceptions, envisager d'échouer rapidement

##### Justification

Si vous ne pouvez pas faire un bon travail de récupération, du moins vous pouvez sortir avant que trop de dégâts consécutifs ne soient causés.

**Voir aussi** : [Simuler le RAII](013-errors.md#re-no-throw-raii)

##### Remarque

Si vous ne pouvez pas être systématique dans la gestion des erreurs, envisagez de « planter » comme réponse à toute erreur qui ne peut pas être gérée localement.
C'est-à-dire, si vous ne pouvez pas récupérer d'une erreur dans le contexte de la fonction qui l'a détectée, appelez `abort()`, `quick_exit()`,
ou une fonction similaire qui déclenchera une sorte de redémarrage du système.

Dans les systèmes où vous avez beaucoup de processus et/ou beaucoup d'ordinateurs, vous devez de toute façon vous attendre et gérer des plantations fatales,
disons dues à des pannes matérielles.
Dans de tels cas, « planter » revient simplement à laisser la gestion des erreurs au niveau supérieur du système.

##### Exemple

    void f(int n)
    {
        // ...
        p = static_cast<X*>(malloc(n * sizeof(X)));
        if (!p) abort();     // abort si la mémoire est épuisée
        // ...
    }

La plupart des programmes ne peuvent pas gérer l'épuisement de la mémoire gracieusement de toute façon. Ceci est approximativement équivalent à

    void f(int n)
    {
        // ...
        p = new X[n];    // throw si la mémoire est épuisée (par défaut, terminate)
        // ...
    }

Généralement, c'est une bonne idée de journaliser la raison de la « plantation » avant de quitter.

##### Application

Malaisé

### <a name="re-no-throw-codes"></a>E.27 : Si vous ne pouvez pas lancer d'exceptions, utiliser des codes d'erreur de manière systématique

##### Justification

L'utilisation systématique de toute stratégie de gestion des erreurs minimise la probabilité d'oublier de gérer une erreur.

**Voir aussi** : [Simuler le RAII](013-errors.md#re-no-throw-raii)

##### Remarque

Il y a plusieurs problèmes à aborder :

* Comment transmettre un indicateur d'erreur depuis l'extérieur d'une fonction ?
* Comment libérer toutes les ressources d'une fonction avant une sortie en erreur ?
* Que utiliser comme indicateur d'erreur ?

En général, retourner un indicateur d'erreur implique de retourner deux valeurs : le résultat et un indicateur d'erreur.
L'indicateur d'erreur peut faire partie de l'objet, p. ex. un objet peut avoir un indicateur `valid()`
ou une paire de valeurs peut être retournée.

##### Exemple

    Gadget make_gadget(int n)
    {
        // ...
    }

    void user()
    {
        Gadget g = make_gadget(17);
        if (!g.valid()) {
                // gestion de l'erreur
        }
        // ...
    }

Cette approche s'inscrit dans la [gestion des ressources par RAII simulé](013-errors.md#re-no-throw-raii).
La fonction `valid()` pourrait retourner un `error_indicator` (p. ex. un membre d'une énumération `error_indicator`).

##### Exemple

Et si nous ne pouvons pas ou ne voulons pas modifier le type `Gadget` ?
Dans ce cas, nous devons retourner une paire de valeurs.
Par exemple :

    std::pair<Gadget, error_indicator> make_gadget(int n)
    {
        // ...
    }

    void user()
    {
        auto r = make_gadget(17);
        if (!r.second) {
                // gestion de l'erreur
        }
        Gadget& g = r.first;
        // ...
    }

Comme on le voit, `std::pair` est un type de retour possible.
Certaines personnes préfèrent un type spécifique.
Par exemple :

    Gval make_gadget(int n)
    {
        // ...
    }

    void user()
    {
        auto r = make_gadget(17);
        if (!r.err) {
                // gestion de l'erreur
        }
        Gadget& g = r.val;
        // ...
    }

Une raison de préférer un type de retour spécifique est d'avoir des noms pour ses membres, plutôt que les quelque peu cryptiques `first` et `second`
et d'éviter la confusion avec d'autres utilisations de `std::pair`.

##### Exemple

En général, vous devez nettoyer avant une sortie en erreur.
Cela peut être désordonné :

    std::pair<int, error_indicator> user()
    {
        Gadget g1 = make_gadget(17);
        if (!g1.valid()) {
            return {0, g1_error};
        }

        Gadget g2 = make_gadget(31);
        if (!g2.valid()) {
            cleanup(g1);
            return {0, g2_error};
        }

        // ...

        if (all_foobar(g1, g2)) {
            cleanup(g2);
            cleanup(g1);
            return {0, foobar_error};
        }

        // ...

        cleanup(g2);
        cleanup(g1);
        return {res, 0};
    }

Simuler le RAII peut être non trivial, en particulier dans les fonctions avec plusieurs ressources et plusieurs erreurs possibles.
Une technique pas si rare consiste à regrouper le nettoyage à la fin de la fonction pour éviter la répétition (remarquez que la portée supplémentaire autour de `g2` est indésirable mais nécessaire pour que la version `goto` compile) :

    std::pair<int, error_indicator> user()
    {
        error_indicator err = 0;
        int res = 0;

        Gadget g1 = make_gadget(17);
        if (!g1.valid()) {
            err = g1_error;
            goto g1_exit;
        }

        {
            Gadget g2 = make_gadget(31);
            if (!g2.valid()) {
                err = g2_error;
                goto g2_exit;
            }

            if (all_foobar(g1, g2)) {
                err = foobar_error;
                goto g2_exit;
            }

            // ...

        g2_exit:
            if (g2.valid()) cleanup(g2);
        }

    g1_exit:
        if (g1.valid()) cleanup(g1);
        return {res, err};
    }

Plus la fonction est grande, plus cette technique devient tentante.
`finally` peut [alléger un peu la douleur](013-errors.md#re-finally).
De plus, plus le programme devient grand, plus il est difficile d'appliquer systématiquement une stratégie de gestion des erreurs basée sur des indicateurs d'erreur.

Nous [préférons la gestion des erreurs basée sur les exceptions](013-errors.md#re-throw) et recommandons de [garder les fonctions courtes](006-functions.md#rf-single) @TODO-LINK.

**Voir aussi** : [Discussion](#sd-???) @TODO-LINK

**Voir aussi** : [Retourner plusieurs valeurs](006-functions.md#rf-out-multi) @TODO-LINK

##### Application

Malaisé.

### <a name="re-no-throw"></a>E.28 : Éviter la gestion des erreurs basée sur un état global (p. ex. `errno`)

##### Justification

L'état global est difficile à gérer et il est facile d'oublier de le vérifier.
Quand avez-vous pour la dernière fois testé la valeur de retour de `printf()` ?

**Voir aussi** : [Simuler le RAII](013-errors.md#re-no-throw-raii)

##### Exemple, mauvais

    int last_err;

    void f(int n)
    {
        // ...
        p = static_cast<X*>(malloc(n * sizeof(X)));
        if (!p) last_err = -1;     // erreur si la mémoire est épuisée
        // ...
    }

##### Remarque

La gestion des erreurs de style C est basée sur la variable globale `errno`, donc il est essentiellement impossible d'éviter complètement ce style.

##### Application

Malaisé.


### <a name="re-specifications"></a>E.30 : Ne pas utiliser les spécifications d'exceptions

##### Justification

Les spécifications d'exceptions rendent la gestion des erreurs fragile, imposent un coût d'exécution et ont été supprimées de la norme C++.

##### Exemple

    int use(int arg)
        throw(X, Y)
    {
        // ...
        auto x = f(arg);
        // ...
    }

Si `f()` lance une exception différente de `X` et `Y`, le gestionnaire inattendu est invoqué, ce qui par défaut termine le programme.
C'est acceptable, mais supposons que nous ayons vérifié que cela ne peut pas se produire et que `f` est modifié pour lancer une nouvelle exception `Z`,
nous avons maintenant une plantation à moins de modifier `use()` (et de retester tout).
Le problème est que `f()` pourrait être dans une bibliothèque que nous ne contrôlons pas et que la nouvelle exception n'est rien que `use()` ne puisse
rien faire à son sujet ou qui ne l'intéresse en aucune manière.
Nous pouvons modifier `use()` pour laisser passer `Z`, mais maintenant les appelants de `use()` ont probablement besoin d'être modifiés.
Cela devient rapidement ingérable.
Alternativement, nous pouvons ajouter un `try`-`catch` à `use()` pour mapper `Z` vers une exception acceptable.
Cela devient aussi rapidement ingérable.
Remarquez que les modifications de l'ensemble des exceptions se produisent souvent au niveau le plus bas d'un système
(p. ex., à cause de modifications d'une bibliothèque réseau ou d'un middleware), donc les modifications « remontent » à travers de longues chaînes d'appels.
Dans une grande base de code, cela pourrait signifier que personne ne pourrait mettre à jour vers une nouvelle version d'une bibliothèque jusqu'à ce que le dernier utilisateur soit modifié.
Si `use()` fait partie d'une bibliothèque, il se peut qu'il ne soit pas possible de la mettre à jour car une modification pourrait affecter des clients inconnus.

La politique de laisser les exceptions se propager jusqu'à ce qu'elles atteignent une fonction qui peut potentiellement les gérer s'est avérée efficace au fil des années.

##### Remarque

Non. Ce ne serait pas mieux si les spécifications d'exceptions étaient appliquées statiquement.
Par exemple, voir [Stroustrup94](032-bibliography.md#Stroustrup94) @TODO-LINK.

##### Remarque

Si aucune exception ne peut être lancée, utilisez [`noexcept`](013-errors.md#re-noexcept).

##### Application

Signaler toute spécification d'exception.

### <a name="re_catch"></a>E.31 : Ordonner correctement ses clauses `catch`

##### Justification

Les clauses `catch` sont évaluées dans l'ordre où elles apparaissent et une clause peut masquer une autre.

##### Exemple, mauvais

    void f()
    {
        // ...
        try {
                // ...
        }
        catch (Base& b) { /* ... */ }
        catch (Derived& d) { /* ... */ }
        catch (...) { /* ... */ }
        catch (std::exception& e) { /* ... */ }
    }

Si `Derived` est dérivé de `Base`, le gestionnaire `Derived` ne sera jamais invoqué.
Le gestionnaire « capturer tout » (`...`) garantit que le gestionnaire `std::exception` ne sera jamais invoqué.

##### Application

Signaler tous les « gestionnaires masqués ».
