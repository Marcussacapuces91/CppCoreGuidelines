# <a name="s-errors"></a>E : Gestion des erreurs

La gestion des erreurs implique :

* Détecter une erreur
* Transmettre des informations sur une erreur à un code de gestion
* Préserver un état valide du programme
* Éviter les fuites de ressources

Il n'est pas possible de se remettre de toutes les erreurs.  
Si la récupération d'une erreur n'est pas possible, il est important de « sortir » rapidement d'une manière bien définie.  
Une stratégie de gestion des erreurs doit être simple, sinon elle devient une source d'erreurs encore pires.  
Le code de gestion des erreurs non testé et rarement exécuté est lui‑même source de nombreux bogues.

Les règles visent à aider à éviter plusieurs types d'erreurs :

* Violations de type (par ex., mauvaise utilisation des `union`s et des conversions)
* Fuites de ressources (y compris les fuites de mémoire)
* Erreurs de limites
* Erreurs de cycle de vie (p. ex., accéder à un objet après qu'il ait été `delete`d)
* Erreurs de complexité (erreurs logiques dues à une expression trop complexe d'idées)
* Erreurs d'interface (p. ex., une valeur inattendue est transmise à travers une interface)

Résumé des règles de gestion des erreurs :

* [E.1: Développer une stratégie de gestion des erreurs dès la conception](#re-design)
* [E.2: Lever une exception pour signaler qu'une fonction ne peut pas effectuer la tâche assignée](#re-throw)
* [E.3: Utiliser les exceptions uniquement pour la gestion des erreurs](#re-errors)
* [E.4: Concevoir votre stratégie de gestion des erreurs autour des invariants](#re-design-invariants)
* [E.5: Que le constructeur établisse un invariant, et lever une exception s'il ne peut pas](#re-invariant)
* [E.6: Utiliser RAII pour éviter les fuites](#re-raii)
* [E.7: Préciser vos préconditions](#re-precondition)
* [E.8: Préciser vos postconditions](#re-postcondition)

* [E.12: Utiliser `noexcept` lors de la sortie d'une fonction à cause d'un `throw` qui est impossible ou inacceptable](#re-noexcept)
* [E.13: Ne jamais lever une exception lorsqu'on est le propriétaire direct d'un objet](#re-never-throw)
* [E.14: Utiliser des types définis par l'utilisateur spécifiquement conçus comme exceptions (pas de types intégrés)](#re-exception-types)
* [E.15: Lever par valeur, attraper les exceptions d'une hiérarchie par référence](#re-exception-ref)
* [E.16: Les destructeurs, la désallocation, `swap`, et la construction par copie/move d'un type d'exception ne doivent jamais échouer](#re-never-fail)
* [E.17: Ne pas essayer d'attraper chaque exception dans chaque fonction](#re-not-always)
* [E.18: Minimiser l'utilisation explicite de `try/catch`](#re-catch)
* [E.19: Utiliser un objet `final_action` pour exprimer le nettoyage si aucun gestionnaire de ressource approprié n'est disponible](#re-finally)

* [E.25: Si vous ne pouvez pas lever d'exceptions, simulez RAII pour la gestion des ressources](#re-no-throw-raii)
* [E.26: Si vous ne pouvez pas lever d'exceptions, envisagez d'échouer rapidement](#re-no-throw-crash)
* [E.27: Si vous ne pouvez pas lever d'exceptions, utilisez systématiquement des codes d'erreur](#re-no-throw-codes)
* [E.28: Éviter la gestion des erreurs basée sur un état global (ex. errno)](#re-no-throw)

* [E.30: Ne pas utiliser de spécifications d'exception](#re-specifications)
* [E.31: Ordonnancer correctement vos clauses catch](#re_catch)

### <a name="re-design"></a>E.1: Développer une stratégie de gestion des erreurs dès la conception

##### Raison

Une stratégie cohérente et complète pour la gestion des erreurs et des fuites de ressources est difficile à réinjecter dans un système.

### <a name="re-throw"></a>E.2: Lever une exception pour signaler qu'une fonction ne peut pas effectuer la tâche assignée

##### Raison

Pour rendre la gestion des erreurs systématique, robuste et non répétitive.

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

Ici, les constructeurs de `vector` et `string` peuvent ne pas être capables d'allouer suffisamment de mémoire pour leurs éléments, le constructeur de `vector` peut ne pas être capable de copier les `Thing` dans sa liste d'initialisation, et `File_handle` peut ne pas être capable d'ouvrir le fichier requis.  
Dans chaque cas, ils lancent une exception pour que l'appelant de `use()` puisse gérer.  
Si `use()` pouvait gérer l'échec de la construction de `bar` il peut reprendre le contrôle en utilisant `try/catch`.  
Dans les deux cas, le constructeur de `Foo` détruit correctement les membres construits avant de transmettre le contrôle à celui qui a tenté de créer un `Foo`.  
Notez qu'il n'y a pas de valeur de retour pouvant contenir un code d'erreur.

Le constructeur de `File_handle` pourrait être défini comme suit :

    File_handle::File_handle(const string& name, const string& mode)
        : f{fopen(name.c_str(), mode.c_str())}
    {
        if (!f)
            throw runtime_error{"File_handle: could not open " + name + " as " + mode};
    }

##### Note

Il est souvent affirmé que les exceptions sont destinées à signaler des événements exceptionnels et des échecs.  
Cependant, c’est un peu circulaire car « quoi est exceptionnel ? »  
Exemples :

* Un prérequis qui ne peut pas être satisfait
* Un constructeur qui ne peut pas construire un objet (échec d'établir l'[invariant](#rc-struct) @TODO-LINK) de sa classe
* Une erreur hors limites (p. ex., `v[v.size()] = 7`)
* Incapacité à acquérir une ressource (p. ex. le réseau est en panne)

Au contraire, la terminaison d’une boucle ordinaire n’est pas exceptionnelle.  
À moins que la boucle n'ait été censée être infinie, sa terminaison est normale et attendue.

##### Note

Ne pas utiliser un `throw` simplement comme une alternative pour retourner une valeur d'une fonction.

##### Exception

Certains systèmes, tels que les systèmes temps réel dur, exigent une garantie que l'action est prise dans un (généralement court) temps maximum constant connu avant le démarrage de l'exécution.  
De tels systèmes ne peuvent utiliser les exceptions que s'il existe un support d'outils permettant de prévoir précisément le temps maximal de récupération d'un `throw`.

**Voir également** : [RAII](#re-raii)

**Voir également** : [discussion](#sd-noexcept) @TODO-LINK

##### Note

Avant de décider que vous ne pouvez pas vous permettre ou que vous n'aimez pas la gestion des erreurs basée sur les exceptions, jetez un œil aux [alternatives](#re-no-throw-raii);  
elles ont leurs propres complexités et problèmes.  
De plus, dans la mesure du possible, mesurez avant de faire des affirmations sur l'efficacité.

### <a name="re-errors"></a>E.3: Utiliser les exceptions uniquement pour la gestion des erreurs

##### Raison

Séparer la gestion des erreurs du « code ordinaire ».  
Les implémentations C++ tendent à être optimisées sur la base de l'hypothèse que les exceptions sont rares.

##### Exemple, ne pas

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

Ceci est plus compliqué et est probablement beaucoup plus lent que l'alternative évidente.  
Il n'y a rien d'exceptionnel à chercher une valeur dans un `vector`.

##### Application

Devrait être heuristique.  
Rechercher les valeurs d'exception « fuites » à partir des clauses `catch`.

### <a name="re-design-invariants"></a>E.4: Concevoir votre stratégie de gestion des erreurs autour des invariants

##### Raison

Un objet doit être dans un état valide (défini formellement ou de façon informelle par un invariant) et pour récupérer d'une erreur, chaque objet non détruit doit être dans un état valide.

##### Note

Un [invariant](#rc-struct) @TODO-LINK est une condition logique pour les membres d'un objet qu'un constructeur doit établir pour que les fonctions membres publiques puissent l'adopter.

##### Application

???

### <a name="re-invariant"></a>E.5: Que le constructeur établisse un invariant, et lever une exception s'il ne peut pas

##### Raison

Laisser un objet sans son invariant établi est une invitation à la complication.  
Toutes les fonctions membres ne peuvent pas être appelées.

##### Exemple

    class Vector {  // très simple vecteur de doubles
        // si elem != nullptr alors elem pointe vers sz doubles
    public:
        Vector() : elem{nullptr}, sz{0} {}
        Vector(int s) : elem{new double[s]}, sz{s} { /* initialiser les éléments */ }
        ~Vector() { delete [] elem; }
        double& operator[](int s) { return elem[s]; }
        // ...
    private:
        owner<double*> elem;
        int sz;
    };

L'invariant de classe – ici indiqué comme un commentaire – est établi par les constructeurs.  
`new` lance une exception s'il ne peut pas allouer la mémoire requise.  
Les opérateurs, notamment l'opérateur souscript, dépendent de l'invariant.

**Voir également** : [Si un constructeur ne peut pas construire un objet valide, lancer une exception](#rc-throw) @TODO-LINK

##### Application

Défiler les classes avec un état privé sans constructeur (public, protégé ou privé).

### <a name="re-raii"></a>E.6: Utiliser RAII pour éviter les fuites

##### Raison

Les fuites sont généralement inacceptables.  
La libération manuelle de ressources est sujette aux erreurs.  
RAII (« Resource Acquisition Is Initialization ») est le moyen le plus simple et le plus systématique d'éviter les fuites.

##### Exemple

    void f1(int i)   // Mauvais : fuite possible
    {
        int* p = new int[12];
        // ...
        if (i < 17) throw Bad{"in f()", i};
        // ...
    }

On pourrait libérer la ressource avant le lancement :

    void f2(int i)   // Gênant et sujet aux erreurs : libération explicite
    {
        int* p = new int[12];
        // ...
        if (i < 17) {
            delete[] p;
            throw Bad{"in f()", i};
        }
        // ...
    }

Ceci est verbeux. Dans un code plus grand avec plusieurs `throw` possibles, les libérations explicites deviennent répétitives et sujettes aux erreurs.

    void f3(int i)   // OK : gestion de la ressource effectuée par un handle (voir ci-après)
    {
        auto p = make_unique<int[]>(12);
        // ...
        if (i < 17) throw Bad{"in f()", i};
        // ...
    }

Notez que cela fonctionne même lorsque le `throw` est implicite car il s'est produit dans une fonction appelée :

    void f4(int i)   // OK : gestion de la ressource effectuée par un handle (voir ci-après)
    {
        auto p = make_unique<int[]>(12);
        // ...
        helper(i);   // could throw
        // ...
    }

En dehors d'une réelle nécessité de la sémantique pointeur, il faut utiliser un objet ressource local :

    void f5(int i)   // OK : gestion de la ressource effectuée par un objet local
    {
        vector<int> v(12);
        // ...
        helper(i);   // could throw
        // ...
    }

C'est encore plus simple et plus sûr, et souvent plus performant.

##### Note

Si aucun gestionnaire de ressource évident n'existe et qu'il devient impossible de définir un objet/handle RAII approprié, en dernier recours, les actions de nettoyage peuvent être représentées par un objet [`final_action`](#re-finally).

##### Note

Mais que faisons‑nous si nous écrivons un programme où les exceptions ne peuvent pas être utilisées ?  
La première question est qu'il y a beaucoup de mythes anti‑exceptions.  
Nous ne connaissons qu’un petit nombre de bonnes raisons :

* On se trouve sur un système si petit que le support d'exceptions gaspillerait la majorité des 2 K de mémoire.
* On est dans un système temps réel dur et on ne possède pas d'outils garantissant qu'une exception est traitée dans le temps requis.
* On est dans un système plein de code hérité utilisant de nombreux pointeurs de manière difficile à comprendre (en particulier sans stratégie d'appropriation reconnue) de sorte que les exceptions pourraient provoquer des fuites.
* La mise en œuvre du mécanisme des exceptions C++ est inacceptable (lente, gourmande en mémoire, ne fonctionnant pas correctement pour les bibliothèques liées dynamiquement, etc.). Plaidez auprès de votre fournisseur ; s'il n'y a pas de plaintes, aucune amélioration ne surviendra.
* On sera renvoyé si l'on remet en question la sagesse ancienne du manager.

Seule la première raison est fondamentale, donc chaque fois que c'est possible, utilisez les exceptions pour implémenter RAII, ou conservez vos objets RAII afin qu'ils ne puissent jamais échouer.  
Quand les exceptions ne peuvent pas être utilisées, simulez RAII.  
C’est‑à‑dire, vérifiez systématiquement que les objets sont valides après construction et que vous libérez toujours les ressources dans le destructeur.  
Une stratégie consiste à ajouter une opération `valid()` à chaque gestionnaire de ressource :

    void f()
    {
        vector<string> vs(100);   // non std::vector : valid() ajouté
        if (!vs.valid()) {
            // gérer l'erreur ou quitter
        }

        ifstream fs("foo");   // non std::ifstream : valid() ajouté
        if (!fs.valid()) {
            // gérer l'erreur ou quitter
        }

        // ...
    } // destructeurs nettoient comme d'habitude

Évidemment, cela augmente la taille du code, ne permet pas la propagation implicite des « exceptions » (`valid()` checks) et ces vérifications peuvent être oubliées.  
Préférez utiliser des exceptions.

**Voir également** : [Use of `noexcept`](#re-noexcept)

##### Application

???

### <a name="re-precondition"></a>E.7: Préciser vos préconditions

##### Raison

Éviter les erreurs d'interface.

**Voir également** : [precondition rule](#ri-pre) @TODO-LINK

### <a name="re-postcondition"></a>E.8: Préciser vos postconditions

##### Raison

Éviter les erreurs d'interface.

**Voir également** : [postcondition rule](#ri-post) @TODO-LINK

### <a name="re-noexcept"></a>E.12: Utiliser `noexcept` lors de la sortie d'une fonction à cause d'un `throw` qui est impossible ou inacceptable

##### Raison

Rendre la gestion des erreurs systématique, robuste et efficace.

##### Exemple

    double compute(double d) noexcept
    {
        return log(sqrt(d <= 0 ? 1 : d));
    }

Ici, nous savons que `compute` ne lancera pas d'exception car elle est construite à partir d'opérations qui ne lancent pas d'exception.  
En déclarant `compute` comme `noexcept`, nous donnons au compilateur et aux lecteurs une information qui peut faciliter leur compréhension et manipulation de `compute`.

##### Note

De nombreuses fonctions de la bibliothèque standard sont `noexcept`, y compris toutes les fonctions de la bibliothèque standard « héritées » de la bibliothèque C.

##### Exemple

    vector<double> munge(const vector<double>& v) noexcept
    {
        vector<double> v2(v.size());
        // ... faire quelque chose ...
    }

Le mot-clé `noexcept` indique que je ne suis pas disposé ou capable de gérer la situation où je ne peux pas construire le `vector` local.  
C’est‑à‑dire que je considère l'épuisement de mémoire comme une erreur de conception grave (à la hauteur des défaillances matérielles) et je suis disposé à faire planter le programme si cela se produit.

##### Note

Ne pas utiliser les [exception-specifications traditionnelles](#re-specifications).

##### Voir également

[discussion](#sd-noexcept) @TODO-LINK

### <a name="re-never-throw"></a>E.13: Ne jamais lever une exception lorsqu'on est le propriétaire direct d'un objet

##### Raison

Cela entraînerait une fuite.

##### Exemple

    void leak(int x)   // ne pas : risque de fuite
    {
        auto p = new int{7};
        if (x < 0) throw Get_me_out_of_here{};  // risque de fuite *p
        // ...
        delete p;   // nous pourrions ne jamais arriver ici
    }

Une façon d'éviter ces problèmes consiste à utiliser les gestionnaires de ressources de façon cohérente :

    void no_leak(int x)
    {
        auto p = make_unique<int>(7);
        if (x < 0) throw Get_me_out_of_here{};  // supprimera *p si nécessaire
        // ...
        // pas besoin de delete p
    }

Une autre solution (souvent meilleure) consiste à utiliser une variable locale pour éliminer l'utilisation explicite des pointeurs :

    void no_leak_simplified(int x)
    {
        vector<int> v(7);
        // ...
    }

##### Note

Si vous avez un objet local « qui nécessite un nettoyage », mais qui n'est pas représenté par un objet avec un destructeur, ce nettoyage doit également être effectué avant un `throw`.  
Parfois, [`finally()`](#re-finally) peut rendre un tel nettoyage peu systématique un peu plus gérable.

### <a name="re-exception-types"></a>E.14: Utiliser des types définis par l'utilisateur spécifiquement conçus comme exceptions (pas de types intégrés)

##### Raison

Un type défini par l'utilisateur peut transmettre de meilleures informations sur une erreur à un gestionnaire. L'information peut être encodée dans le type lui‑même et il est peu probable qu'il entre en conflit avec les exceptions d'autres personnes.

##### Exemple

    throw 7; // mauvais

    throw "something bad";  // mauvais

    throw std::exception{}; // mauvais - pas d'information

Hériter de `std::exception` donne la flexibilité d'attraper l'exception spécifique ou de gérer de façon générale via `std::exception` :

    class MyException : public std::runtime_error
    {
    public:
        MyException(const string& msg) : std::runtime_error{msg} {}
        // ...
    };

    // ...

    throw MyException{"something bad"};  // bon

Les exceptions n'ont pas besoin d'hériter de `std::exception` :

    class MyCustomError final {};  // pas dérivé de std::exception

    // ...

    throw MyCustomError{};  // bon – les gestionnaires doivent attraper ce type (ou ...)

Les types de bibliothèque dérivés de `std::exception` peuvent être utilisés comme exceptions génériques si aucune information utile ne peut être ajoutée au point de détection :

    throw std::runtime_error("something bad"); // bon

    // ...

    throw std::invalid_argument("i is not even"); // bon

Les classes `enum` sont également autorisées :

    enum class alert {RED, YELLOW, GREEN};

    throw alert::RED; // bon

##### Application

Attraper un `throw` de types intégrés et `std::exception`.

### <a name="re-exception-ref"></a>E.15: Lever par valeur, attraper les exceptions d'une hiérarchie par référence

##### Raison

Lever par valeur (et non par pointeur) et attraper par référence évite les copies, notamment les troncatures d'objets de base.

##### Exemple, mauvais

    void f()
    {
        try {
            // ...
            throw new widget{}; // ne pas : lever par valeur, pas par pointeur brut
            // ...
        }
        catch (base_class e) {  // ne pas : pourrait tronquer
            // ...
        }
    }

À la place, utilisez une référence :

    catch (base_class& e) { /* ... */ }

ou – généralement encore mieux – une référence `const` :

    catch (const base_class& e) { /* ... */ }

La plupart des gestionnaires ne modifient pas leur exception et, en général, nous recommandons l'utilisation de `const`.

##### Note

Attraper par valeur peut être approprié pour un type à petite valeur tel qu'une valeur d'énumération.

##### Note

Pour relancer une exception attrapée, utilisez `throw;` et non `throw e;`.  
L'utilisation de `throw e;` lancerait une nouvelle copie de `e` (tranchée au type statique `std::exception`, lorsqu'une exception est attrapée par `catch (const std::exception& e)`) au lieu de relancer l'exception originale de type `std::runtime_error`. (Mais gardez à l'esprit **Ne pas essayer d'attraper chaque exception dans chaque fonction**([#re-not-always]) et **Minimiser l'utilisation explicite de `try/catch`**([#re-catch]).)

##### Application

* Marquer l'attrapage par valeur d'un type qui possède une fonction virtuelle.
* Marquer le lancer de pointeurs bruts.

### <a name="re-never-fail"></a>E.16: Les destructeurs, la désallocation, `swap`, et la construction par copie/move d'un type d'exception ne doivent jamais échouer

##### Raison

Nous ne savons pas comment écrire des programmes fiables si un destructeur, un swap, une désallocation de mémoire ou la tentative de copie/move‑construction d'un objet d'exception échouent ; c’est‑à‑dire s’ils sortent par une exception ou ne remplissent tout simplement pas leur action requise.

##### Exemple, ne pas

    class Connection {
        // ...
    public:
        ~Connection()   // Ne pas : destructeur très mauvais
        {
            if (cannot_disconnect()) throw I_give_up{information};
            // ...
        }
    };

##### Note

Beaucoup ont essayé d'écrire du code fiable violant cette règle, tel qu'une connexion réseau qui « refuse » de se fermer.  
D'après nos connaissances, personne n'a trouvé de façon générale de le faire.  
Parfois, pour des exemples très spécifiques, on peut se débrouiller en mettant un état pour un nettoyage futur.  
Par exemple, on peut mettre un socket qui ne veut pas se fermer sur une liste « socket mauvais », à examiner par un balayage régulier de l'état du système.  
Chaque exemple que nous avons vu de cela est source d'erreurs, spécialisé, et souvent sujet à bogues.

##### Note

La bibliothèque standard suppose que les destructeurs, les fonctions de désallocation (p. ex. `operator delete`), et `swap` ne lancent pas d'exception. Si elles le font, les invariants de base de la bibliothèque standard sont brisés.

##### Note

* Les fonctions de désallocation, y compris `operator delete`, doivent être `noexcept`.
* Les fonctions `swap` doivent être `noexcept`.
* La plupart des destructeurs sont implicites `noexcept` par défaut.
* De plus, [faire en sorte que les opérations de move soient `noexcept`](#rc-move-noexcept) @TODO-LINK.
* Si vous écrivez un type destiné à être utilisé comme type d'exception, assurez-vous que son constructeur de copie est `noexcept`. En général nous ne pouvons pas l'imposer mécaniquement parce que nous ne savons pas si un type est destiné à être utilisé comme type d'exception.
* Essayez de ne pas `throw` un type dont le constructeur de copie n'est pas `noexcept`. En général nous ne pouvons pas l'imposer mécaniquement, car même `throw std::string(...)` pourrait lancer une exception mais ne le fait pas en pratique.

##### Application

* Attraper les destructeurs, opérations de désallocation, et `swap`s qui `throw`.
* Attraper les opérations qui ne sont pas `noexcept`.

**Voir également** : [discussion](#sd-never-fail) @TODO-LINK

### <a name="re-not-always"></a>E.17: Ne pas essayer d'attraper chaque exception dans chaque fonction

##### Raison

Attraper une exception dans une fonction qui ne peut pas prendre d'action de récupération significative entraîne de la complexité et du gaspillage.  
Laissez une exception se propager jusqu'à ce qu'elle atteigne une fonction capable de la gérer.  
Les actions de nettoyage sur le chemin de déballage sont gérées par [RAII](#re-raii).

##### Exemple, ne pas

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

* Marquer les blocs `try` imbriqués.
* Marquer les fichiers source avec un ratio trop élevé de blocs `try` à fonctions. (???) Problème : définir « trop élevé »

### <a name="re-catch"></a>E.18: Minimiser l'utilisation explicite de `try/catch`

##### Raison

`try/catch` est verbeux et les usages non trivials sont source d'erreurs.  
`try/catch` peut indiquer une gestion de ressources ou une gestion d'erreurs non systématique et/​ou de bas niveau.

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
Il pourrait y avoir une fuite provenant du pointeur nu dans le bloc `try`.  
Toutes les exceptions ne sont pas gérées.  
Supprimer un objet qui n'a pas pu être construit est très probablement une erreur.  
Meilleur :

    void f2(zstring s)
    {
        Gadget g {s};
    }

##### Alternatives

* gestionnaires de ressources appropriés et [RAII](#re-raii)
* [`finally`](#re-finally)

##### Application

??? difficile, nécessite une heuristique

### <a name="re-finally"></a>E.19: Utiliser un objet `final_action` pour exprimer le nettoyage si aucun gestionnaire de ressource approprié n'est disponible

##### Raison

`finally` du [GSL](#gsl-guidelines-support-library) @TODO-LINK est moins verbeux et plus sûr que `try/catch`.

##### Exemple

    void f(int n)
    {
        void* p = malloc(n);
        auto _ = gsl::finally([p] { free(p); });
        // ...
    }

##### Note

`finally` n'est pas aussi désordonné que `try/catch`, mais il reste ad-hoc.  
Préférez des objets de gestion de ressources appropriés ([RAII](#re-raii)).  
Considérez `finally` comme dernier recours.

##### Note

L'utilisation de `finally` est une alternative systématique et relativement propre à l’ancienne technique [`goto exit;`](#re-no-throw-codes) pour gérer le nettoyage lorsqu'il n'y a pas de gestion systématique des ressources.

##### Application

Heuristique : détecter `goto exit;`

### <a name="re-no-throw-raii"></a>E.25: Si vous ne pouvez pas lever d'exceptions, simulez RAII pour la gestion des ressources

##### Raison

Même sans exceptions, [RAII](#re-raii) est généralement le meilleur et le moyen le plus systématique de gérer les ressources.

##### Note

La gestion des erreurs à l'aide d'exceptions est la seule façon complète et systématique de gérer les erreurs non locales en C++.  
En particulier, signaler de manière non intrusive l'échec de construction d'un objet nécessite une exception.  
Signalement d'erreurs d'une manière qui ne peut pas être ignorée nécessite des exceptions.  
Si vous ne pouvez pas utiliser d'exceptions, simulez leur utilisation au mieux que vous le pouvez.

La peur des exceptions est largement mal orientée.  
Quand elles sont utilisées dans des circonstances exceptionnelles dans un code non saturé en pointeurs et en structures de contrôle compliquées, la gestion d'exception est presque toujours abordable (en temps et espace) et conduit presque toujours à un meilleur code.  
Cela présuppose une bonne implémentation du mécanisme d'exceptions, qui n'est pas disponible sur tous les systèmes.  
Il existe aussi des cas où les problèmes ci‑dessus ne s'appliquent pas, mais les exceptions ne peuvent pas être utilisées pour d'autres raisons.  
Certains systèmes temps réel dur sont un exemple : une opération doit être terminée dans un temps fixe avec une erreur ou une réponse correcte.  
En l'absence d'outils d'estimation temporelle appropriés, il est difficile de garantir les exceptions.  
De tels systèmes (par ex., logiciel de contrôle de vol) interdisent généralement également l'utilisation de la mémoire dynamique (tas).

Donc, le principal point directrice pour la gestion des erreurs est « utiliser les exceptions et [RAII](#re-raii) ».  
Cette section traite des cas où vous n'avez soit pas une implémentation efficace d'exceptions, soit un tas de code hérité (p. ex., beaucoup de pointeurs, propriété mal définie, et gestion d'erreurs non systématique) qui rend impossible l'introduction d'une gestion d'exceptions simple et systématique.

Avant de condamner les exceptions ou de trop se plaindre de leur coût, considérez des exemples de l'utilisation de [codes d'erreur](#re-no-throw-codes). Considérez le coût et la complexité de l'utilisation des codes d'erreur. Si la performance est votre préoccupation, mesurez.

##### Exemple

Supposons que vous vouliez écrire

    void func(zstring arg)
    {
        Gadget g {arg};
        // ...
    }

Si le `gadget` n'est pas correctement construit, `func` quitte avec une exception.  
Si nous ne pouvons pas lever d'exception, nous pouvons simuler ce style RAII en ajoutant une fonction membre `valid()` à `Gadget` :

    error_indicator func(zstring arg)
    {
        Gadget g {arg};
        if (!g.valid()) return gadget_construction_error;
        // ...
        return 0;   // zéro indique « bon »
    }

Le problème est, bien sûr, que l'appelant doit maintenant se souvenir de tester la valeur de retour.  
Pour encourager la pratique, considérez d'ajouter un `[[nodiscard]]`.

**Voir également** : [Discussion](#sd-???) @TODO-LINK

##### Application

Possible seulement pour des versions spécifiques de cette idée : par ex., tester de façon systématique `valid()` après la construction d'un gestionnaire de ressource.

**Voir également** : [Simuler RAII](#re-no-throw-raii)

### <a name="re-no-throw-crash"></a>E.26: Si vous ne pouvez pas lever d'exceptions, envisagez d'échouer rapidement

##### Raison

Si vous ne pouvez pas bien récupérer, vous pouvez au moins sortir avant qu'un trop grand dommage ne soit produit.

**Voir également** : [Simuler RAII](#re-no-throw-raii)

##### Note

Si vous ne pouvez pas être systématique dans la gestion des erreurs, envisagez de « crash » comme réponse à toute erreur qui ne peut pas être gérée localement.  
C’est‑à‑dire, si vous ne pouvez pas récupérer d'une erreur dans le contexte de la fonction qui l'a détectée, appelez `abort()`, `quick_exit()`, ou une fonction similaire qui déclenchera un redémarrage du système.

Dans les systèmes où vous avez beaucoup de processus et/ou beaucoup d'ordinateurs, vous devez vous attendre et gérer les crashes fatals de toute façon, par ex. des défaillances matérielles.  
Dans de tels cas, « crashing » signifie simplement laisser la gestion des erreurs au niveau suivant du système.

##### Exemple

    void f(int n)
    {
        // ...
        p = static_cast<X*>(malloc(n * sizeof(X)));
        if (!p) abort();     // aborter si la mémoire est épuisée
        // ...
    }

La plupart des programmes ne peuvent pas gérer l'épuisement de mémoire de manière élégante de toute façon.  
C’est à peu près équivalent à

    void f(int n)
    {
        // ...
        p = new X[n];    // lance une exception si la mémoire est épuisée (par défaut, termine)
        // ...
    }

Il est généralement une bonne idée d'enregistrer la raison du « crash » avant de quitter.

##### Application

Awkward

### <a name="re-no-throw-codes"></a>E.27: Si vous ne pouvez pas lever d'exceptions, utilisez systématiquement des codes d'erreur

##### Raison

L'utilisation systématique de toute stratégie de gestion d'erreur minimise la probabilité d'oublier de gérer une erreur.

**Voir également** : [Simuler RAII](#re-no-throw-raii)

##### Note

Il y a plusieurs points à traiter :

* Comment transmettre un indicateur d'erreur hors d'une fonction ?
* Comment libérer toutes les ressources d'une fonction avant de faire une sortie d'erreur ?
* Que utilisez‑vous comme indicateur d'erreur ?

En général, retourner un indicateur d'erreur implique le retour de deux valeurs : le résultat et un indicateur d'erreur.  
L’indicateur d'erreur peut faire partie de l'objet, p. ex. un objet peut avoir un indicateur `valid()` ou une paire de valeurs peut être retournée.

##### Exemple

    Gadget make_gadget(int n)
    {
        // ...
    }

    void user()
    {
        Gadget g = make_gadget(17);
        if (!g.valid()) {
                // gestion d'erreur
        }
        // ...
    }

Cette approche convient à la [gestion des ressources simulées RAII](#re-no-throw-raii).

##### Exemple

Que faire si nous ne pouvons pas ou ne voulons pas modifier le type `Gadget` ? Dans ce cas, nous devons retourner une paire de valeurs. Par exemple :

    std::pair<Gadget, error_indicator> make_gadget(int n)
    {
        // ...
    }

    void user()
    {
        auto r = make_gadget(17);
        if (!r.second) {
                // gestion d'erreur
        }
        Gadget& g = r.first;
        // ...
    }

Comme illustré, `std::pair` est un type de retour possible.  
Certaines personnes préfèrent un type spécifique. Par exemple :

    Gval make_gadget(int n)
    {
        // ...
    }

    void user()
    {
        auto r = make_gadget(17);
        if (!r.err) {
                // gestion d'erreur
        }
        Gadget& g = r.val;
        // ...
    }

Une raison de préférer un type de retour spécifique est d'avoir des noms pour ses membres, plutôt que les noms quelque peu obscurs `first` et `second`, et d'éviter les confusions avec d'autres utilisations de `std::pair`.

##### Exemple

En général, vous devez nettoyer avant une sortie d'erreur.  
Cela peut être compliqué :

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

Simuler RAII peut être non trivial, surtout dans les fonctions avec plusieurs ressources et plusieurs erreurs possibles.  
Une technique pas rare consiste à rassembler le nettoyage à la fin de la fonction pour éviter la répétition (notez que la portée supplémentaire autour de `g2` est indésirable mais nécessaire pour que la version `goto` compile)  :

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

Plus la fonction est grande, plus cette technique est tentante.  
`finally` peut [adoucir un peu la douleur](#re-finally).  
De plus, plus le programme est grand, plus il est difficile d'appliquer une stratégie de gestion d'erreurs basée sur un indicateur d'erreur de façon systématique.

Nous [préférons la gestion d'erreurs basée sur les exceptions](#re-throw) et recommandons [de garder les fonctions courtes](#rf-single) @TODO-LINK.

**Voir également** : [Discussion](#sd-???) @TODO-LINK

**Voir également** : [Retour de multiples valeurs](#rf-out-multi) @TODO-LINK

##### Application

Awkward

### <a name="re-no-throw"></a>E.28: Éviter la gestion des erreurs basée sur un état global (ex. errno)

##### Raison

Un état global est difficile à gérer et il est facile d'oublier de le vérifier.  
Quand avez‑vous testé pour la dernière fois la valeur de retour de `printf()` ?

**Voir également** : [Simuler RAII](#re-no-throw-raii)

##### Exemple, mauvais

    int last_err;

    void f(int n)
    {
        // ...
        p = static_cast<X*>(malloc(n * sizeof(X)));
        if (!p) last_err = -1;     // erreur si mémoire épuisée
        // ...
    }

##### Note

La gestion d'erreurs en C est basée sur la variable globale `errno`, il est donc pratiquement impossible d'éviter ce style entièrement.

##### Application

Awkward

### <a name="re-specifications"></a>E.30: Ne pas utiliser de spécifications d'exception

##### Raison

Les spécifications d'exception rendent la gestion des erreurs fragile, imposent un coût d'exécution et ont été retirées du standard C++.

##### Exemple

    int use(int arg)
        throw(X, Y)
    {
        // ...
        auto x = f(arg);
        // ...
    }

Si `f()` lance une exception différente de `X` et `Y`, le gestionnaire inattendu est invoqué, ce qui, par défaut, termine.  
C’est acceptable, mais supposons que nous ayons vérifié qu’il ne se produit pas et que `f` est modifiée pour lancer une nouvelle exception `Z`,  
nous avons alors un crash tant que nous ne changeons pas `use()` (et que nous ne tout testons pas).  
Le problème est que `f()` peut se trouver dans une bibliothèque que nous ne contrôlons pas et que la nouvelle exception n’est rien que ce que `use()` peut faire.  
Nous pouvons changer `use()` pour transmettre `Z`, mais maintenant les appelants de `use()` devraient probablement être modifiés.  
Cela devient rapidement ingérable.  
Alternativement, on peut ajouter un `try/catch` à `use()` pour mapper `Z` vers une exception acceptable.  
Ce dernier endommage aussi rapidement l'utilisation.  
Notez que les changements à l'ensemble des exceptions se produisent souvent au niveau le plus bas du système (p.ex., en raison de modifications d'une bibliothèque réseau ou d'un middleware), de sorte que les changements « bougent » à travers de longues chaînes d'appels.  
Dans une grande base de code, cela pourrait signifier que personne ne peut mettre à jour à une nouvelle version d'une bibliothèque jusqu'à ce que le dernier utilisateur soit modifié.  
Si `use()` fait partie d'une bibliothèque, il peut ne pas être possible de le mettre à jour parce qu'un changement pourrait affecter des clients inconnus.

La politique de laisser les exceptions se propager jusqu'à ce qu'elles atteignent une fonction capable de les gérer a fait ses preuves au fil des ans.

##### Note

Non. Ce serait tout aussi mauvais si les spécifications d'exception étaient imposées statiquement.  
Par ex., voir [Stroustrup94](#Stroustrup94).

##### Note

Si aucune exception ne peut être levée, utilisez [`noexcept`](#re-noexcept).

##### Application

Marquer toutes les spécifications d'exception.

### <a name="re_catch"></a>E.31: Ordonnancer correctement vos clauses catch

##### Raison

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
Le gestionnaire « tout attraper » a assuré que le gestionnaire `std::exception` ne sera jamais invoqué.

##### Application

Marquer tous les gestionnaires « masquants ».

---