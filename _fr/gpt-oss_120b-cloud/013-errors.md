# <a name="s-errors"></a>E : Gestion des erreurs

La gestion des erreurs implique :

* Détecter une erreur
* Transmettre des informations sur une erreur à du code de traitement
* Conserver un état valide du programme
* Éviter les fuites de ressources

Il n’est pas possible de récupérer de toutes les erreurs. Si la récupération d’une erreur n’est pas possible, il est important de « sortir » rapidement de manière bien définie. Une stratégie de gestion des erreurs doit être simple, sinon elle devient source d’erreurs encore plus graves. Le code de gestion des erreurs, non testé et rarement exécuté, est lui‑même source de nombreux bugs.

Les règles sont conçues pour aider à éviter plusieurs types d’erreurs :

* Violations de type (par ex., mauvaise utilisation des `union`s et des casts)
* Fuites de ressources (y compris les fuites de mémoire)
* Erreurs de débordement
* Erreurs de durée de vie (par ex., accéder à un objet après qu’il a été `delete`d)
* Erreurs de complexité (erreurs logiques souvent dues à une expression trop complexe d’idées)
* Erreurs d’interface (par ex., une valeur inattendue transmise via une interface)

Résumé des règles de gestion des erreurs :

* [E.1 : Élaborer une stratégie de gestion des erreurs dès la conception](013-errors.md#re-design)
* [E.2 : Lancer une exception pour signaler qu’une fonction ne peut pas accomplir sa tâche assignée](013-errors.md#re-throw)
* [E.3 : N’utiliser les exceptions que pour la gestion des erreurs](013-errors.md#re-errors)
* [E.4 : Concevoir votre stratégie de gestion des erreurs autour des invariants](013-errors.md#re-design-invariants)
* [E.5 : Permettre à un constructeur d’établir un invariant, et lancer une exception s’il ne le peut pas](013-errors.md#re-invariant)
* [E.6 : Utiliser RAII pour prévenir les fuites](013-errors.md#re-raii)
* [E.7 : Déclarer vos préconditions](013-errors.md#re-precondition)
* [E.8 : Déclarer vos postconditions](013-errors.md#re-postcondition)

* [E.12 : Utiliser `noexcept` lorsqu’une sortie d’une fonction à cause d’un `throw` est impossible ou inacceptable](013-errors.md#re-noexcept)
* [E.13 : Ne jamais lancer d’exception lorsqu’on est le propriétaire direct d’un objet](013-errors.md#re-never-throw)
* [E.14 : Utiliser des types définis par l’utilisateur, conçus à cet effet, comme exceptions (et non les types intégrés)](013-errors.md#re-exception-types)
* [E.15 : Lancer par valeur, attraper les exceptions d’une hiérarchie par référence](013-errors.md#re-exception-ref)
* [E.16 : Les destructeurs, désallocations, `swap`, et la construction de copie/déplacement d’un type d’exception ne doivent jamais échouer](013-errors.md#re-never-fail)
* [E.17 : Ne pas essayer d’attraper chaque exception dans chaque fonction](013-errors.md#re-not-always)
* [E.18 : Minimiser l’utilisation explicite de `try`/`catch`](013-errors.md#re-catch)
* [E.19 : Utiliser un objet `final_action` pour exprimer le nettoyage lorsqu’aucun gestionnaire de ressources approprié n’est disponible](013-errors.md#re-finally)

* [E.25 : Si vous ne pouvez pas lancer d’exceptions, simuler RAII pour la gestion des ressources](013-errors.md#re-no-throw-raii)
* [E.26 : Si vous ne pouvez pas lancer d’exceptions, envisager une sortie rapide (fail fast)](013-errors.md#re-no-throw-crash)
* [E.27 : Si vous ne pouvez pas lancer d’exceptions, utilisez des codes d’erreur de façon systématique](013-errors.md#re-no-throw-codes)
* [E.28 : Éviter la gestion des erreurs basée sur un état global (ex. `errno`)](013-errors.md#re-no-throw)

* [E.30 : Ne pas utiliser les spécifications d’exception](013-errors.md#re-specifications)
* [E.31 : Ordonnancer correctement les clauses `catch`](013-errors.md#re_catch)

### <a name="re-design"></a>E.1 : Élaborer une stratégie de gestion des erreurs dès la conception

##### Raison

Une stratégie cohérente et complète pour gérer les erreurs et les fuites de ressources est difficile à ajouter rétroactivement à un système.

### <a name="re-throw"></a>E.2 : Lancer une exception pour signaler qu’une fonction ne peut pas accomplir sa tâche assignée

##### Raison

Rendre la gestion des erreurs systématique, robuste et non répétitive.

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

Ici, les constructeurs de `vector` et de `string` pourraient ne pas être capables d’allouer suffisamment de mémoire pour leurs éléments, le constructeur du `vector` pourrait ne pas pouvoir copier les `Thing` de sa liste d’initialisation, et `File_handle` pourrait ne pas être capable d’ouvrir le fichier requis.  
Dans chaque cas, ils lancent une exception que l’appelant de `use()` doit gérer.  
Si `use()` pouvait gérer l’échec de construction de `bar`, il peut prendre le contrôle en utilisant `try`/`catch`.  
Dans les deux cas, le constructeur de `Foo` détruit correctement les membres construits avant de passer le contrôle à celui qui a tenté de créer un `Foo`.  
Notez qu’il n’existe aucune valeur de retour pouvant contenir un code d’erreur.

Le constructeur de `File_handle` pourrait être défini ainsi :

    File_handle::File_handle(const string& name, const string& mode)
        : f{fopen(name.c_str(), mode.c_str())}
    {
        if (!f)
            throw runtime_error{"File_handle : impossible d'ouvrir " + name + " en tant que " + mode};
    }

##### Remarque

On dit souvent que les exceptions sont destinées à signaler des événements ou des échecs exceptionnels. Cependant, cela reste un raisonnement circulaire car « qu’est‑ce qui est exceptionnel ? »  
Exemples :

* Une précondition qui ne peut être remplie
* Un constructeur qui ne peut pas créer un objet (échec de l'[invariant](007-class.md#rc-struct) de la classe)
* Une erreur de dépassement d’indice (par ex., `v[v.size()] = 7`)
* L’impossibilité d’acquérir une ressource (par ex., le réseau est indisponible)

En revanche, la terminaison d’une boucle ordinaire n’est pas exceptionnelle.  
À moins que la boucle ne soit censée être infinie, sa terminaison est normale et attendue.

##### Remarque

Ne pas utiliser `throw` simplement comme une façon alternative de retourner une valeur depuis une fonction.

##### Exception

Certains systèmes, tels que les systèmes à temps réel strict, nécessitent la garantie qu’une action sera effectuée dans un délai maximal constant (généralement court) connu avant le démarrage de l’exécution. De tels systèmes ne peuvent utiliser les exceptions que s’ils disposent d’outils permettant d’estimer avec précision le temps maximal de récupération d’un `throw`.

**Voir aussi** : [RAII](013-errors.md#re-raii)

**Voir aussi** : [discussion](028-discussion.md#sd-noexcept)

##### Remarque

Avant de décider que vous ne pouvez pas vous permettre ou que vous n’aimez pas la gestion des erreurs basée sur les exceptions, examinez les [alternatives](013-errors.md#re-no-throw-raii) ; elles possèdent leurs propres complexités et problèmes.  
Dans la mesure du possible, mesurez avant de formuler des affirmations sur l’efficacité.

### <a name="re-errors"></a>E.3 : N’utiliser les exceptions que pour la gestion des erreurs

##### Raison

Séparer la gestion des erreurs du « code ordinaire ».  
Les implémentations C++ ont tendance à être optimisées en partant du principe que les exceptions sont rares.

##### Exemple, mauvais

    // ne pas : l'exception n'est pas utilisée pour la gestion des erreurs
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

Cette version est plus compliquée et, très probablement, beaucoup plus lente que l’alternative évidente. Il n’y a rien d’exceptionnel à trouver une valeur dans un `vector`.

##### Application

Il faudrait une heuristique.  
Rechercher les valeurs d’exception « fuites » hors des clauses `catch`.

### <a name="re-design-invariants"></a>E.4 : Concevoir votre stratégie de gestion des erreurs autour des invariants

##### Raison

Pour utiliser un objet, il doit être dans un état valide (défini formellement ou informellement par un invariant) et, pour se remettre d’une erreur, chaque objet non détruit doit être dans un état valide.

##### Remarque

Un [invariant](007-class.md#rc-struct) est une condition logique sur les membres d’un objet que le constructeur doit établir afin que les fonctions membres publiques puissent s’y fier.

##### Application

???

### <a name="re-invariant"></a>E.5 : Permettre à un constructeur d’établir un invariant, et lancer une exception s’il ne le peut pas

##### Raison

Laisser un objet sans invariant établi, c’est inviter les ennuis. Toutes les fonctions membres ne peuvent pas être appelées.

##### Exemple

    class Vector {  // vecteur très simplifié de doubles
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

L’invariant de la classe – indiqué ici comme commentaire – est établi par les constructeurs.  
`new` lance une exception s’il ne peut pas allouer la mémoire requise.  
Les opérateurs, notamment l’opérateur d’indexation, s’appuient sur l’invariant.

**Voir aussi** : [Si un constructeur ne peut pas créer un objet valide, lancer une exception](007-class.md#rc-throw)

##### Application

Signaler les classes dont l’état est `private` sans constructeur (public, protected ou private).

### <a name="re-raii"></a>E.6 : Utiliser RAII pour prévenir les fuites

##### Raison

Les fuites sont généralement inacceptables.  
La libération manuelle de ressources est source d’erreurs.  
RAII (« Resource Acquisition Is Initialization ») est la façon la plus simple et systématique d’éviter les fuites.

##### Exemple

    void f1(int i)   // Mauvais : fuite possible
    {
        int* p = new int[12];
        // ...
        if (i < 17) throw Bad{"in f()", i};
        // ...
    }

Nous pourrions libérer soigneusement la ressource avant le `throw` :

    void f2(int i)   // Maladroit et sujet à erreurs : libération explicite
    {
        int* p = new int[12];
        // ...
        if (i < 17) {
            delete[] p;
            throw Bad{"in f()", i};
        }
        // ...
    }

C’est verbeux. Dans du code plus important avec plusieurs `throw`s possibles, les libérations explicites deviennent répétitives et source d’erreurs.

    void f3(int i)   // OK : gestion de la ressource réalisée par un handle (voir ci‑dessous)
    {
        auto p = make_unique<int[]>(12);
        // ...
        if (i < 17) throw Bad{"in f()", i};
        // ...
    }

Remarquez que cela fonctionne même quand le `throw` est implicite parce qu’il se produit dans une fonction appelée :

    void f4(int i)   // OK : gestion de la ressource réalisée par un handle (voir ci‑dessous)
    {
        auto p = make_unique<int[]>(12);
        // ...
        helper(i);   // peut lancer une exception
        // ...
    }

À moins d’avoir réellement besoin de sémantique de pointeur, utilisez un objet local :

    void f5(int i)   // OK : gestion de la ressource réalisée par un objet local
    {
        vector<int> v(12);
        // ...
        helper(i);   // peut lancer une exception
        // ...
    }

C’est encore plus simple, plus sûr, et souvent plus efficace.

##### Remarque

S’il n’existe aucun gestionnaire de ressource évident et que, pour quelque raison, la définition d’un objet/handle RAII adéquat est impossible, comme dernier recours les actions de nettoyage peuvent être représentées par un objet [`final_action`](013-errors.md#re-finally).

##### Remarque

Mais que faire si l’on écrit un programme où les exceptions ne peuvent pas être utilisées ?  
Le premier défi consiste à contester cette hypothèse ; il existe de nombreux mythes anti‑exceptions.  
Nous ne connaissons que quelques bonnes raisons :

* Nous sommes sur un système si petit que le support des exceptions consommerait la majeure partie de nos 2 Ko de mémoire.  
* Nous sommes dans un système à temps réel strict et nous ne disposons pas d’outils garantissant qu’une exception sera traitée dans le temps requis.  
* Nous sommes dans un système avec un excédent de code hérité utilisant de nombreux pointeurs de façon difficile à comprendre (en particulier sans stratégie de propriété reconnaissable), ce qui pourrait entraîner des fuites.  
* L’implémentation des mécanismes d’exception C++ est déplorable (lente, gourmande en mémoire, ne fonctionne pas correctement avec les bibliothèques dynamiques, etc.).  
  Plaignez‑vous auprès de votre fournisseur d’implémentation ; si aucun utilisateur ne se plaint, aucune amélioration n’interviendra.  
* Nous serions licenciés si nous remettons en cause la sagesse ancestrale de notre manager.

Seule la première de ces raisons est fondamentale, donc chaque fois que possible, utilisez les exceptions pour implémenter RAII, ou concevez vos objets RAII de façon à ne jamais échouer.  
Lorsque les exceptions ne peuvent pas être utilisées, simulez RAII.  
C’est‑à‑dire, vérifiez systématiquement que les objets sont valides après construction et libérez toutes les ressources dans le destructeur.  
Une stratégie consiste à ajouter une opération `valid()` à chaque handle de ressource :

    void f()
    {
        vector<string> vs(100);   // pas std::vector : valid() ajouté
        if (!vs.valid()) {
            // gérer l'erreur ou sortir
        }

        ifstream fs("foo");   // pas std::ifstream : valid() ajouté
        if (!fs.valid()) {
            // gérer l'erreur ou sortir
        }

        // ...
    } // les destructeurs nettoient comme d’habitude

Évidemment, cela augmente la taille du code, n’autorise pas la propagation implicite de « exceptions » (`valid()` checks), et les vérifications `valid()` peuvent être oubliées.  
Privilégiez l’usage d’exceptions.

**Voir aussi** : [Utilisation de `noexcept`](013-errors.md#re-noexcept)

##### Application

???

### <a name="re-precondition"></a>E.7 : Déclarer vos préconditions

##### Raison

Éviter les erreurs d’interface.

**Voir aussi** : [règle de précondition](005-interfaces.md#ri-pre)

### <a name="re-postcondition"></a>E.8 : Déclarer vos postconditions

##### Raison

Éviter les erreurs d’interface.

**Voir aussi** : [règle de postcondition](005-interfaces.md#ri-post)

### <a name="re-noexcept"></a>E.12 : Utiliser `noexcept` lorsqu’une sortie d’une fonction à cause d’un `throw` est impossible ou inacceptable

##### Raison

Rendre la gestion des erreurs systématique, robuste et efficace.

##### Exemple

    double compute(double d) noexcept
    {
        return log(sqrt(d <= 0 ? 1 : d));
    }

Ici, nous savons que `compute` ne lancera pas d’exception car il est composé d’opérations qui ne lancent pas. En déclarant `compute` comme `noexcept`, nous donnons au compilateur et aux lecteurs humains des informations qui facilitent la compréhension et la manipulation de `compute`.

##### Remarque

De nombreuses fonctions de la bibliothèque standard sont `noexcept`, y compris toutes les fonctions « héritées » de la bibliothèque standard C.

##### Exemple

    vector<double> munge(const vector<double>& v) noexcept
    {
        vector<double> v2(v.size());
        // ... faire quelque chose ...
    }

Le `noexcept` ici indique que je ne suis pas disposé ou capable de gérer la situation où je ne pourrais pas construire le `vector` local. C’est‑à‑dire que j’estime l’épuisement de mémoire comme une erreur de conception grave (au même niveau que les pannes matérielles) et que je suis prêt à faire planter le programme si cela se produit.

##### Remarque

Ne pas utiliser les [spécifications d’exception](013-errors.md#re-specifications) traditionnelles.

##### Voir aussi

[discussion](028-discussion.md#sd-noexcept).

### <a name="re-never-throw"></a>E.13 : Ne jamais lancer d’exception lorsqu’on est le propriétaire direct d’un objet

##### Raison

Cela entraînerait une fuite.

##### Exemple

    void leak(int x)   // mauvais : pourrait fuir
    {
        auto p = new int{7};
        if (x < 0) throw Get_me_out_of_here{};  // pourrait fuir *p
        // ...
        delete p;   // nous pourrions ne jamais atteindre ici
    }

Une façon d’éviter de tels problèmes est d’utiliser des handles de ressources de façon cohérente :

    void no_leak(int x)
    {
        auto p = make_unique<int>(7);
        if (x < 0) throw Get_me_out_of_here{};  // supprimera *p si nécessaire
        // ...
        // pas besoin de delete p
    }

Une autre solution (souvent meilleure) consiste à utiliser une variable locale afin d’éliminer l’usage explicite de pointeurs :

    void no_leak_simplified(int x)
    {
        vector<int> v(7);
        // ...
    }

##### Remarque

Si vous avez une « chose » locale qui nécessite un nettoyage, mais qui n’est pas représentée par un objet avec destructeur, ce nettoyage doit également être effectué avant un `throw`.  
Parfois, [`finally()`](013-errors.md#re-finally) peut rendre ce nettoyage ad‑hoc un peu plus gérable.

### <a name="re-exception-types"></a>E.14 : Utiliser des types définis par l’utilisateur, conçus à cet effet, comme exceptions (et non les types intégrés)

##### Raison

Un type défini par l’utilisateur peut mieux transmettre les informations sur une erreur à un gestionnaire. L’information peut être encodée dans le type même et il est peu probable que le type entre en conflit avec les exceptions d’autres personnes.

##### Exemple

    throw 7; // mauvais

    throw "something bad";  // mauvais

    throw std::exception{}; // mauvais - aucune information

Dériver de `std::exception` donne la flexibilité d’attraper l’exception spécifique ou de gérer de façon générale via `std::exception` :

    class MyException : public std::runtime_error
    {
    public:
        MyException(const string& msg) : std::runtime_error{msg} {}
        // ...
    };

    // ...

    throw MyException{"something bad"};  // bon

Les exceptions n’ont pas besoin d’être dérivées de `std::exception` :

    class MyCustomError final {};  // ne dérive pas de std::exception

    // ...

    throw MyCustomError{};  // bon : les gestionnaires doivent attraper ce type (ou …)

Les types de bibliothèque dérivés de `std::exception` peuvent être utilisés comme exceptions génériques si aucune information utile ne peut être ajoutée au moment de la détection :

    throw std::runtime_error("something bad"); // bon

    // ...

    throw std::invalid_argument("i is not even"); // bon

Les `enum class` sont aussi autorisés :

    enum class alert {RED, YELLOW, GREEN};

    throw alert::RED; // bon

##### Application

Détecter les lancers de types intégrés et de `std::exception`.

### <a name="re-exception-ref"></a>E.15 : Lancer par valeur, attraper les exceptions d’une hiérarchie par référence

##### Raison

Lancer par valeur (et non par pointeur) et attraper par référence empêche les copies, en particulier l’écrasement (slicing) des sous‑objets de base.

##### Exemple ; mauvais

    void f()
    {
        try {
            // ...
            throw new widget{}; // mauvais : lancer par valeur, pas par pointeur brut
            // ...
        }
        catch (base_class e) {  // mauvais : pourrait tronquer
            // ...
        }
    }

Utilisez plutôt une référence :

    catch (base_class& e) { /* ... */ }

ou – généralement encore mieux – une référence `const` :

    catch (const base_class& e) { /* ... */ }

La plupart des gestionnaires ne modifient pas leur exception et, en général, nous [recommandons l’utilisation de `const`](010-expr.md#res-const).

##### Remarque

Attraper par valeur peut être approprié pour un petit type valeur tel qu’une valeur d’`enum`.

##### Remarque

Pour relancer une exception attrapée, utilisez `throw;` et non `throw e;`. Utiliser `throw e;` créerait une nouvelle copie de `e` (écrasée au type statique `std::exception` lorsqu’on attrape `catch (const std::exception& e)`) au lieu de relancer l’exception originale de type `std::runtime_error`. (Mais gardez à l’esprit [Ne pas essayer d’attraper chaque exception dans chaque fonction](013-errors.md#re-not-always) et [Minimiser l’utilisation explicite de `try`/`catch`](013-errors.md#re-catch).)

##### Application

* Détecter les captures par valeur d’un type possédant une fonction virtuelle.  
* Détecter les lancers de pointeurs bruts.

### <a name="re-never-fail"></a>E.16 : Les destructeurs, désallocations, `swap`, et la construction de copie/déplacement d’un type d’exception ne doivent jamais échouer

##### Raison

Nous ne savons pas comment écrire des programmes fiables si un destructeur, un `swap`, une désallocation ou la tentative de copie/déplacement d’un objet d’exception échoue ; c’est‑à‑dire si cela se solde par une exception ou n’effectue tout simplement pas son action requise.

##### Exemple, mauvais

    class Connection {
        // ...
    public:
        ~Connection()   // Mauvais : destructeur très mauvais
        {
            if (cannot_disconnect()) throw I_give_up{information};
            // ...
        }
    };

##### Remarque

Beaucoup ont tenté d’écrire du code fiable violant cette règle, par exemple une connexion réseau qui « refuse de se fermer ». À notre connaissance, personne n’a trouvé une façon générale de le faire.  
Occasionnellement, pour des exemples très spécifiques, on peut se débrouiller en enregistrant un état pour un nettoyage futur. Par exemple, on pourrait placer une socket qui ne veut pas se fermer dans une « liste de mauvaises sockets », pour être examinée par un balayage régulier de l’état du système. Tout exemple que nous avons vu est sujet à erreurs, spécialisé et souvent bogué.

##### Remarque

La bibliothèque standard suppose que les destructeurs, fonctions de désallocation (ex., `operator delete`) et `swap` ne lancent pas d’exception. S’ils le font, les invariants de base de la bibliothèque standard sont brisés.

##### Remarque

* Les fonctions de désallocation, y compris `operator delete`, doivent être `noexcept`.  
* Les fonctions `swap` doivent être `noexcept`.  
* La plupart des destructeurs sont implicitement `noexcept` par défaut.  
* De même, [rendre les opérations de déplacement `noexcept`](007-class.md#rc-move-noexcept).  
* Si vous écrivez un type destiné à être utilisé comme type d’exception, assurez‑vous que son constructeur de copie est `noexcept`. En général, nous ne pouvons pas appliquer cela mécaniquement, car nous ne savons pas si un type est destiné à être utilisé comme type d’exception.  
* Essayez de ne pas `throw` un type dont le constructeur de copie n’est pas `noexcept`. En général, nous ne pouvons pas appliquer cela mécaniquement, car même `throw std::string(...)` pourrait lancer, mais ne le fait pas en pratique.

##### Application

* Détecter les destructeurs, opérations de désallocation et `swap` qui lancent.  
* Détecter de telles opérations qui ne sont pas `noexcept`.

**Voir aussi** : [discussion](028-discussion.md#sd-never-fail)

### <a name="re-not-always"></a>E.17 : Ne pas essayer d’attraper chaque exception dans chaque fonction

##### Raison

Attraper une exception dans une fonction qui ne peut pas prendre une action de récupération significative entraîne complexité et gaspillage. Laissez l’exception remonter jusqu’à une fonction capable de la gérer. Laissez les actions de nettoyage sur le chemin de déroulement être gérées par [RAII](013-errors.md#re-raii).

##### Exemple, mauvais

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

* Détecter les blocs `try` imbriqués.  
* Détecter les fichiers source dont le ratio de blocs `try` par fonction est trop élevé. (??? Problème : définir « trop élevé »)

### <a name="re-catch"></a>E.18 : Minimiser l’utilisation explicite de `try`/`catch`

##### Raison

`try`/`catch` est verbeux et les usages non triviaux sont source d’erreurs. `try`/`catch` peut être le signe d’une gestion de ressources ou d’erreurs non systématique et/ou de bas niveau.

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
Il pourrait y avoir une fuite du pointeur nu dans le bloc `try`.  
Toutes les exceptions ne sont pas gérées.  
Supprimer un objet qui a échoué à la construction est presque certainement une erreur.  
Mieux :

    void f2(zstring s)
    {
        Gadget g {s};
    }

##### Alternatives

* Gestionnaires de ressources appropriés et [RAII](013-errors.md#re-raii)  
* [`finally`](013-errors.md#re-finally)

##### Application

??? difficile, nécessite une heuristique

### <a name="re-finally"></a>E.19 : Utiliser un objet `final_action` pour exprimer le nettoyage lorsqu’aucun gestionnaire de ressources approprié n’est disponible

##### Raison

`finally` de la [GSL](#gsl-guidelines-support-library) est moins verbeux et plus difficile à mal utiliser que `try`/`catch`.

##### Exemple

    void f(int n)
    {
        void* p = malloc(n);
        auto _ = gsl::finally([p] { free(p); });
        // ...
    }

##### Remarque

`finally` n’est pas aussi désordonné que `try`/`catch`, mais il reste ad‑hoc.  
Privilégiez les [objets de gestion de ressources appropriés](013-errors.md#re-raii).  
Considérez `finally` comme dernier recours.

##### Remarque

L’utilisation de `finally` constitue une alternative systématique et raisonnablement propre à l’ancienne technique [`goto exit;`](013-errors.md#re-no-throw-codes) pour gérer le nettoyage lorsqu’une gestion de ressource n’est pas systématique.

##### Application

Heuristique : détecter `goto exit;`

### <a name="re-no-throw-raii"></a>E.25 : Si vous ne pouvez pas lancer d’exceptions, simuler RAII pour la gestion des ressources

##### Raison

Même sans exceptions, [RAII](013-errors.md#re-raii) est généralement la meilleure et la plus systématique façon de gérer les ressources.

##### Remarque

La gestion des erreurs à l’aide d’exceptions est la seule façon complète et systématique de gérer les erreurs non locales en C++. En particulier, signaler de façon non intrusive l’échec de construction d’un objet nécessite une exception. Signaler les erreurs d’une manière qui ne puisse pas être ignorée requiert des exceptions. Si vous ne pouvez pas utiliser les exceptions, simulez leur utilisation du mieux possible.

Beaucoup de peur des exceptions est mal fondée. Lorsqu’elle est utilisée pour des circonstances exceptionnelles dans du code qui n’est pas envahi de pointeurs et de structures de contrôle compliquées, la gestion des exceptions est presque toujours abordable (en temps et en espace) et conduit presque toujours à un meilleur code. Cela suppose bien sûr une bonne implémentation des mécanismes d’exception, ce qui n’est pas disponible sur tous les systèmes. Il existe aussi des cas où ces problèmes ne s’appliquent pas, mais les exceptions ne peuvent pas être utilisées pour d’autres raisons. Certains systèmes à temps réel strict sont un exemple : une opération doit être terminée dans un temps fixe, avec succès ou avec erreur. En l’absence d’outils d’estimation du temps, il est difficile de garantir cela avec les exceptions. Ces systèmes (par ex., logiciels de commande de vol) interdisent également l’utilisation de la mémoire dynamique (heap).

Ainsi, la ligne directrice principale pour la gestion des erreurs est « utiliser les exceptions et [RAII](013-errors.md#re-raii) ». Cette section traite des cas où vous n’avez ni implémentation efficace des exceptions, ni possibilité d’introduire une gestion d’exception simple et systématique à cause d’un enchevêtrement d’un vieux code (pointeurs, stratégie de propriété non définie, gestion d’erreur via codes d’erreur non systématique, etc.).

Avant de condamner les exceptions ou de trop vous plaindre de leur coût, examinez les exemples d’utilisation des [codes d’erreur](013-errors.md#re-no-throw-codes). Considérez le coût et la complexité de l’usage des codes d’erreur. Si la performance vous préoccupe, mesurez.

##### Exemple

Supposons que vous vouliez écrire

    void func(zstring arg)
    {
        Gadget g {arg};
        // ...
    }

Si le `gadget` n’est pas correctement construit, `func` se termine par une exception. Si nous ne pouvons pas lancer d’exception, nous pouvons simuler ce style RAII de gestion de ressources en ajoutant une fonction `valid()` à `Gadget` :

    error_indicator func(zstring arg)
    {
        Gadget g {arg};
        if (!g.valid()) return gadget_construction_error;
        // ...
        return 0;   // zéro indique « bon »
    }

Le problème est bien sûr que l’appelant doit maintenant se souvenir de tester la valeur de retour. Pour l’encourager à le faire, pensez à ajouter `[[nodiscard]]`.

**Voir aussi** : [Discussion](#sd-???) @TODO-LINK

##### Application

Possible (unique) pour des versions spécifiques de cette idée : par ex., tester systématiquement `valid()` après la construction d’un handle de ressource.

### <a name="re-no-throw-crash"></a>E.26 : Si vous ne pouvez pas lancer d’exceptions, envisager une sortie rapide (fail fast)

##### Raison

Si vous ne pouvez pas faire un bon travail de récupération, au moins vous pouvez sortir avant que des dommages conséquents ne se produisent.

**Voir aussi** : [Simuler RAII](013-errors.md#re-no-throw-raii)

##### Remarque

Si vous ne pouvez pas être systématique dans la gestion des erreurs, envisagez de « crasher » en réponse à toute erreur qui ne peut être traitée localement. C’est‑à‑dire, si vous ne pouvez pas récupérer d’une erreur dans le contexte de la fonction qui l’a détectée, appelez `abort()`, `quick_exit()`, ou une fonction similaire qui déclenchera un redémarrage du système.

Dans les systèmes où vous avez de nombreux processus et/ou de nombreux ordinateurs, vous devez vous attendre à gérer des crashs fatals de toute façon, par exemple à cause de pannes matérielles. Dans de tels cas, « crasher » revient simplement à laisser la gestion des erreurs au niveau supérieur du système.

##### Exemple

    void f(int n)
    {
        // ...
        p = static_cast<X*>(malloc(n * sizeof(X)));
        if (!p) abort();     // abort si la mémoire est épuisée
        // ...
    }

La plupart des programmes ne peuvent pas gérer l’épuisement de mémoire de façon élégante de toute façon. Cela revient grosso modo à

    void f(int n)
    {
        // ...
        p = new X[n];    // lance une exception si la mémoire est épuisée (par défaut, termine)
        // ...
    }

Typiquement, il est conseillé de journaliser la raison du « crash » avant de sortir.

##### Application

Difficile

### <a name="re-no-throw-codes"></a>E.27 : Si vous ne pouvez pas lancer d’exceptions, utilisez des codes d’erreur de façon systématique

##### Raison

L’usage systématique de toute stratégie de gestion des erreurs minimise le risque d’oublier de gérer une erreur.

**Voir aussi** : [Simuler RAII](013-errors.md#re-no-throw-raii)

##### Remarque

Plusieurs questions se posent :

* Comment transmettre un indicateur d’erreur hors d’une fonction ?  
* Comment libérer toutes les ressources d’une fonction avant une sortie d’erreur ?  
* Qu’utiliser comme indicateur d’erreur ?

En général, retourner un indicateur d’erreur implique de retourner deux valeurs : le résultat et l’indicateur d’erreur. L’indicateur d’erreur peut faire partie de l’objet, par ex. un objet peut posséder une fonction `valid()` ou bien un couple de valeurs peut être retourné.

##### Exemple

    Gadget make_gadget(int n)
    {
        // ...
    }

    void user()
    {
        Gadget g = make_gadget(17);
        if (!g.valid()) {
                // gestion d’erreur
        }
        // ...
    }

Cette approche s’accorde avec la [gestion de ressources simulée RAII](013-errors.md#re-no-throw-raii). La fonction `valid()` pourrait retourner un `error_indicator` (par ex., un membre d’une énumération `error_indicator`).

##### Exemple

Et si nous ne pouvons pas ou ne voulons pas modifier le type `Gadget` ? Dans ce cas, nous devons retourner un couple de valeurs. Par exemple :

    std::pair<Gadget, error_indicator> make_gadget(int n)
    {
        // ...
    }

    void user()
    {
        auto r = make_gadget(17);
        if (!r.second) {
                // gestion d’erreur
        }
        Gadget& g = r.first;
        // ...
    }

Comme le montre cet exemple, `std::pair` est un type de retour possible. Certaines personnes préfèrent un type dédié. Par exemple :

    Gval make_gadget(int n)
    {
        // ...
    }

    void user()
    {
        auto r = make_gadget(17);
        if (!r.err) {
                // gestion d’erreur
        }
        Gadget& g = r.val;
        // ...
    }

Une raison de préférer un type de retour dédié est d’avoir des noms pour ses membres, plutôt que les quelque peu obscurs `first` et `second`, et d’éviter la confusion avec d’autres usages de `std::pair`.

##### Exemple

En général, vous devez nettoyer avant une sortie d’erreur. Cela peut être désordonné :

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

Simuler RAII peut être non trivial, surtout dans les fonctions avec plusieurs ressources et plusieurs erreurs possibles. Une technique pas rare consiste à rassembler le nettoyage à la fin de la fonction pour éviter les répétitions (notez que le scope supplémentaire autour de `g2` est indésirable mais nécessaire pour que la version `goto` compile) :

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

Plus la fonction est grande, plus cette technique devient tentante. `finally` peut [atténuer un peu la douleur](013-errors.md#re-finally). De plus, plus le programme grossit, plus il est difficile d’appliquer de façon systématique une stratégie basée sur des indicateurs d’erreur.

Nous [privilégions la gestion des erreurs basée sur les exceptions](013-errors.md#re-throw) et recommandons de [garder les fonctions courtes](006-functions.md#rf-single).

**Voir aussi** : [Discussion](#sd-???) @TODO-LINK

**Voir aussi** : [Retourner plusieurs valeurs](006-functions.md#rf-out-multi)

##### Application

Difficile.

### <a name="re-no-throw"></a>E.28 : Éviter la gestion des erreurs basée sur un état global (ex. `errno`)

##### Raison

L’état global est difficile à gérer et il est facile d’oublier de le vérifier. Quand avez‑vous vérifié pour la dernière fois la valeur de retour de `printf()` ?

**Voir aussi** : [Simuler RAII](013-errors.md#re-no-throw-raii)

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

La gestion des erreurs de style C repose sur la variable globale `errno`, il est donc essentiellement impossible d’éviter totalement ce style.

##### Application

Difficile.

### <a name="re-specifications"></a>E.30 : Ne pas utiliser les spécifications d’exception

##### Raison

Les spécifications d’exception rendent la gestion des erreurs fragile, imposent un coût d’exécution et ont été supprimées du standard C++.

##### Exemple

    int use(int arg)
        throw(X, Y)
    {
        // ...
        auto x = f(arg);
        // ...
    }

Si `f()` lance une exception différente de `X` et `Y`, le gestionnaire inattendu est invoqué, ce qui par défaut termine le programme. C’est acceptable, mais supposons que nous avons vérifié que cela ne peut pas arriver et que `f` est changé pour lancer une nouvelle exception `Z`. Nous aurions alors un plantage à moins de modifier `use()` (et de tout re‑tester). Le problème est que `f()` peut être dans une bibliothèque que nous ne contrôlons pas et la nouvelle exception ne peut rien faire à `use()` ou n’est en aucun cas d’intérêt. Nous pourrions changer `use()` pour laisser passer `Z`, mais alors les appelants de `use()` devraient probablement être modifiés. Ce scénario devient rapidement ingérable.  
Alternativement, nous pourrions ajouter un `try`‑`catch` à `use()` pour mapper `Z` à une exception acceptable. Cela devient aussi ingérable. Notez que les changements dans l’ensemble des exceptions surviennent souvent au niveau le plus bas d’un système (par ex., modification d’une bibliothèque réseau ou d’un middleware), de sorte que les changements « bubblent » à travers de longues chaînes d’appels. Dans un grand code‑base, cela pourrait signifier que personne ne peut mettre à jour une nouvelle version d’une bibliothèque tant que le dernier utilisateur n’est pas modifié. Si `use()` fait partie d’une bibliothèque, il se peut qu’il ne soit pas possible de le mettre à jour car le changement pourrait affecter des clients inconnus.

La politique de laisser les exceptions remonter jusqu’à une fonction qui peut potentiellement les gérer s’est avérée efficace au fil des années.

##### Remarque

Non. Cela ne serait pas meilleur même si les spécifications d’exception étaient appliquées de façon statique. Par exemple, voir [Stroustrup94](032-bibliography.md#Stroustrup94).

##### Remarque

Si aucune exception ne peut être lancée, utilisez `noexcept`.

##### Application

Signaler chaque spécification d’exception.

### <a name="re_catch"></a>E.31 : Ordonnancer correctement les clauses `catch`

##### Raison

Les clauses `catch` sont évaluées dans l’ordre où elles apparaissent et une clause peut masquer une autre.

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

Si `Derived` est dérivé de `Base`, le gestionnaire `Derived` ne sera jamais invoqué. Le gestionnaire « tout attraper » empêche le gestionnaire `std::exception` d’être invoqué.

##### Application

Signaler tous les « gestionnaires masquants ».