# <a name="s-errors"></a>E : Gestion des erreurs

La gestion des erreurs implique :

* Détection d'une erreur
* Transmission d'informations sur une erreur vers du code de gestion
* Maintien d'un état valide du programme
* Évitement des fuites de ressources

Il n'est pas possible de récupérer de toutes les erreurs. Si la récupération d'une erreur n'est pas possible, il est important de « sortir » rapidement d'une façon bien définie. Une stratégie de gestion des erreurs doit rester simple, sinon elle deviendra une source d'erreurs encore pires. Le code de gestion des erreurs non testé et rarement exécuté est lui‑même l'origine de nombreux bugs.

Les règles sont conçues pour aider à éviter plusieurs types d'erreurs :

* Violations de types (ex. mauvaise utilisation des `union` et des conversions)
* Fuites de ressources (incluant les fuites de mémoire)
* Erreurs de dépassement de limites
* Erreurs de durée de vie (ex. accéder à un objet après qu'il ait été `delete`d)
* Erreurs de complexité (erreurs logiques dues à une expression trop complexe des idées)
* Erreurs d'interface (ex. une valeur inattendue est transmise via une interface)

## Résumé des règles de gestion des erreurs :

* [E.1 : Développer une stratégie de gestion des erreurs dès la phase de conception](013-errors.md#re-design)
* [E.2 : Lancer une exception pour signaler qu'une fonction ne peut pas accomplir sa tâche assignée](013-errors.md#re-throw)
* [E.3 : Utiliser les exceptions uniquement pour le traitement d'erreurs](013-errors.md#re-errors)
* [E.4 : Concevoir votre stratégie de gestion des erreurs autour des invariants](013-errors.md#re-design-invariants)
* [E.5 : Laisser un constructeur établir un invariant et lancer une exception s'il ne le peut pas](013-errors.md#re-invariant)
* [E.6 : Utiliser RAII pour empêcher les fuites](013-errors.md#re-raii)
* [E.7 : Énoncer vos préconditions](013-errors.md#re-precondition)
* [E.8 : Énoncer vos postconditions](013-errors.md#re-postcondition)
* [E.12 : Utiliser `noexcept` lorsqu'une fonction quitte à cause d'un `throw` est impossible ou inacceptable](013-errors.md#re-noexcept)
* [E.13 : Ne jamais lancer une exception lorsqu'on est le propriétaire direct d'un objet](013-errors.md#re-never-throw)
* [E.14 : Utiliser des types définis par l'utilisateur spécifiquement conçus comme exceptions (et non les types intégrés)](013-errors.md#re-exception-types)
* [E.15 : Lancer par valeur, capturer les exceptions d'une hiérarchie par référence](013-errors.md#re-exception-ref)
* [E.16 : Les destructeurs, la désallocation, `swap` et la création de copie/move d'une exception ne doivent jamais échouer](013-errors.md#re-never-fail)
* [E.17 : Ne jamais essayer de capturer toutes les exceptions dans chaque fonction](013-errors.md#re-not-always)
* [E.18 : Minimiser l'usage explicite de `try`/`catch`](013-errors.md#re-catch)
* [E.19 : Utiliser un objet `final_action` pour exprimer le nettoyage si aucun handle de ressource approprié n'est disponible](013-errors.md#re-finally)
* [E.25 : Si vous ne pouvez pas lancer d'exceptions, simuler RAII pour la gestion des ressources](013-errors.md#re-no-throw-raii)
* [E.26 : Si vous ne pouvez pas lancer d'exceptions, envisager de sortir rapidement](013-errors.md#re-no-throw-crash)
* [E.27 : Si vous ne pouvez pas lancer d'exceptions, utiliser systématiquement des codes d'erreur](013-errors.md#re-no-throw-codes)
* [E.28 : Éviter le traitement d'erreurs basé sur l'état global (ex. `errno`)](013-errors.md#re-no-throw)
* [E.30 : Ne pas utiliser les spécifications d'exceptions](013-errors.md#re-specifications)
* [E.31 : Ordre correctement vos clauses `catch`](013-errors.md#re_catch)

---

### <a name="re-design"></a>E.1 : Développer une stratégie de gestion des erreurs dès la phase de conception

**Raison**

Une stratégie cohérente et complète de gestion des erreurs et des fuites de ressources est difficile à ajouter à un système une fois celui‑ci construit.

---

### <a name="re-throw"></a>E.2 : Lancer une exception pour signaler qu'une fonction ne peut pas accomplir sa tâche assignée

**Raison**

Faire en sorte que la gestion des erreurs soit systématique, robuste et non répétitive.

**Exemple**

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

Ici, les constructeurs de `vector` et de `string` pourraient ne pas être capables d'allouer assez de mémoire pour leurs éléments, le constructeur de `vector` pourrait ne pas pouvoir copier les `Thing` dans sa liste d'initialisation, et `File_handle` pourrait ne pas pouvoir ouvrir le fichier requis.
Dans chaque cas, ils lancent une exception que le call‑er de `use()` doit gérer.
Si `use()` pouvait gérer l'échec de construction de `bar`, il peut prendre le contrôle en utilisant `try`/`catch`.
Dans les deux cas, le constructeur de `Foo` détruit correctement les membres construits avant de transmettre le contrôle à ce qui a tenté de créer un `Foo`.
Notez qu'il n'y a aucune valeur de retour qui pourrait contenir un code d'erreur.

Le constructeur de `File_handle` pourrait être défini comme ceci :

    File_handle::File_handle(const string& name, const string& mode)
        : f{fopen(name.c_str(), mode.c_str())}
    {
        if (!f)
            throw runtime_error{"File_handle: could not open " + name + " as " + mode};
    }

**Remarque**

On dit souvent que les exceptions sont destinées à signaler des événements et des échecs exceptionnels.
Cela reste assez circulaire car « exceptionnel » n'est pas bien défini.
Exemples :

* Une précondition qui ne peut pas être satisfaite
* Un constructeur qui ne peut pas construire un objet (échec d'établissement de son invariant de classe)
* Une erreur hors de portée (ex. `v[v.size()] = 7`)
* Incapacité à acquérir une ressource (ex. le réseau est hors service)

En revanche, l'achèvement d'une boucle ordinaire n'est pas exceptionnel.
À moins que la boucle soit censée être infinie, son terme est normal et attendu.

**Remarque**

Ne pas utiliser un `throw` simplement comme une alternative de retourner une valeur d'une fonction.

**Exception**

Certains systèmes, comme les systèmes temps réel strict, exigent la garantie qu'une action est prise dans un temps maximum fixe (souvent court) connu avant le début de l'exécution. Ces systèmes peuvent utiliser des exceptions uniquement s'il existe un support d'outils pour prédire avec précision le temps maximum de récupération d'un `throw`.

**Voir aussi** : [RAII](013-errors.md#re-raii)

**Voir aussi** : [discussion](028-discussion.md#sd-noexcept)

**Remarque**

Avant de décider que vous ne pouvez pas vous permettre ou que vous n'aimez pas la gestion d'erreurs basée sur les exceptions, jetez un œil aux [alternatives](013-errors.md#re-no-throw-raii) ; elles ont elles‑mêmes leurs complexités et problèmes. Par ailleurs, autant que possible, mesurez avant de faire des affirmations sur les performances.

---

### <a name="re-errors"></a>E.3 : Utiliser les exceptions uniquement pour le traitement d'erreurs

**Raison**

Gardez la gestion d'erreurs séparée du « code ordinaire ».
Les implémentations C++ tendent à être optimisées en supposant que les exceptions sont rares.

**Exemple, ne faites pas**

    // ne pas : exception non utilisée pour le traitement d'erreurs
    int find_index(vector<string>& vec, const string& x)
    {
        try {
            for (gsl::index i = 0; i < vec.size(); ++i)
                if (vec[i] == x) throw i;  // trouvé x
        }
        catch (int i) {
            return i;
        }
        return -1;   // pas trouvé
    }

C'est plus compliqué et c'est très probablement beaucoup plus lent que l'alternative évidente.
Il n'y a rien d'exceptionnel à trouver une valeur dans un `vector`.

**Application**

Nécessite un heuristic.
Recherchez les valeurs d'exceptions « fugues » hors des clauses `catch`.

---

### <a name="re-design-invariants"></a>E.4 : Concevoir votre stratégie de gestion des erreurs autour des invariants

**Raison**

Pour pouvoir utiliser un objet, il doit se trouver dans un état valide (défini formellement ou informellement par un invariant) et, pour se remettre d'une erreur, chaque objet non détruit doit se trouver dans un état valide.

**Remarque**

Un [invariant](007-class.md#rc-struct) est une condition logique pour les membres d'un objet qu'un constructeur doit établir pour que les fonctions membres publiques puissent supposer.

**Application**

???

---

### <a name="re-invariant"></a>E.5 : Laisser un constructeur établir un invariant, et lancer une exception s'il ne le peut pas

**Raison**

Laisser un objet sans son invariant établi crée de la malléabilité. Aucun membre ne peut être appelé.

**Exemple**

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

L'invariant de classe – ici déclaré en commentaire – est établi par les constructeurs.
`new` lance une exception s'il ne peut pas allouer la mémoire requise.
Les opérateurs, notamment l'opérateur de souscription, comptent sur l'invariant.

**Voir aussi** : [Si un constructeur ne peut pas construire un objet valide, lancer une exception](007-class.md#rc-throw)

**Application**

Marquer les classes avec un état privé sans constructeur (public, protégé, ou privé).

---

### <a name="re-raii"></a>E.6 : Utiliser RAII pour empêcher les fuites

**Raison**

Les fuites sont généralement inacceptables.
La libération manuelle de ressources est sujette à erreur.
RAII (« Resource Acquisition Is Initialization ») est la manière la plus simple et systématique d'empêcher les fuites.

**Exemple**

    void f1(int i)   // Mauvais : fuite potentielle
    {
        int* p = new int[12];
        // ...
        if (i < 17) throw Bad{"in f()", i};
        // ...
    }

On pourrait libérer méticuleusement la ressource avant le `throw` :

    void f2(int i)   // Badine et sujet à erreur : libération explicite
    {
        int* p = new int[12];
        // ...
        if (i < 17) {
            delete[] p;
            throw Bad{"in f()", i};
        }
        // ...
    }

C'est verbeux. Dans un code plus grand avec plusieurs `throw` la libération explicite devient répétitive et sujet à erreur.

    void f3(int i)   // OK : gestion de la ressource assurée par une poignée (mais voir ci‑dessous)
    {
        auto p = make_unique<int[]>(12);
        // ...
        if (i < 17) throw Bad{"in f()", i};
        // ...
    }

Cette approche fonctionne même lorsque le `throw` est implicite parce qu'il se produit dans une fonction appelée :

    void f4(int i)   // OK : gestion de la ressource assurée par une poignée (mais voir ci‑dessous)
    {
        auto p = make_unique<int[]>(12);
        // ...
        helper(i);   // pourrait lancer
        // ...
    }

À moins d'avoir réellement besoin de la sémantique pointeur, utilisez un objet ressource local :

    void f5(int i)   // OK : gestion de la ressource assurée par un objet local
    {
        vector<int> v(12);
        // ...
        helper(i);   // pourrait lancer
        // ...
    }

C'est encore plus simple et plus sûr, et souvent plus efficace.

**Remarque**

S'il n'y a pas de handle de ressource évident et pour une raison quelconque que la définition d'un objet/poignée RAII approprié est inabordable, en dernier recours, les actions de nettoyage peuvent être représentées par un objet [`final_action`](013-errors.md#re-finally).

**Remarque**

Mais que faisons‑nous si nous écrivons un programme où les exceptions ne peuvent pas être utilisées ?  
Première défi : cette hypothèse ; il y a beaucoup de mythes anti‑exceptions.  
On connaît seulement quelques bons motifs :  

* Nous sommes sur un système si petit que le support d'exception occuperait la majorité de nos 2 Ko de mémoire.  
* Nous sommes dans un système temps réel strict et nous n'avons pas d'outils garantissant que l'exception est traitée dans le temps requis.  
* Nous sommes dans un système avec beaucoup de code héritage utilisant beaucoup de pointeurs dans des manières difficiles à comprendre (en particulier sans stratégie d'ownership reconnaissable), de sorte que les exceptions pourraient entraîner des fuites.  
* Notre implémentation des mécanismes d'exception C++ est inacceptable (lent, consomme beaucoup de mémoire, échoue à fonctionner correctement avec des bibliothèques dynamiquement liées, etc.).  
  Plaignez‑vous auprès du distributeur de votre implémentation ; si aucun utilisateur ne se plaint, aucune amélioration ne se produira.  
* On se fait licencier si l'on conteste la sagesse ancienne du manager.

Seule la première raison est fondamentale ; alors que possible, utilisez les exceptions pour implémenter RAII, ou concevez vos objets RAII pour qu'ils ne puissent jamais échouer.
Lorsque les exceptions ne peuvent pas être utilisées, simulez RAII.  
Autrement dit, vérifiez systématiquement que les objets sont valides après construction et libérez encore toutes les ressources dans le destructeur.  
Une stratégie consiste à ajouter une opération `valid()` à chaque poignée de ressource :

    void f()
    {
        vector<string> vs(100);   // pas un std::vector : valid() ajouté
        if (!vs.valid()) {
            // gérer l'erreur ou sortir
        }

        ifstream fs("foo");   // pas un std::ifstream : valid() ajouté
        if (!fs.valid()) {
            // gérer l'erreur ou sortir
        }

        // ...
    } // destructeurs nettoient comme d'habitude

Évidemment, cela augmente la taille du code, ne permet pas la propagation implicite d'« exceptions » (`valid()` vérifie), et les vérifications `valid()` peuvent être oubliées.  
Privilégiez l'utilisation d'exceptions.

**Voir aussi** : [Utilisation de `noexcept`](013-errors.md#re-noexcept)

**Application**

???

---

### <a name="re-precondition"></a>E.7 : Énoncer vos préconditions

**Raison**

Éviter les erreurs d'interface.

**Voir aussi** : [Règle de précondition](005-interfaces.md#ri-pre)

---

### <a name="re-postcondition"></a>E.8 : Énoncer vos postconditions

**Raison**

Éviter les erreurs d'interface.

**Voir aussi** : [Règle de postcondition](005-interfaces.md#ri-post)

---

### <a name="re-noexcept"></a>E.12 : Utiliser `noexcept` lorsqu'un départ d'une fonction à cause d'un `throw` est impossible ou inacceptable

**Raison**

Faites la gestion d'erreur systématique, robuste et efficace.

**Exemple**

    double compute(double d) noexcept
    {
        return log(sqrt(d <= 0 ? 1 : d));
    }

Ici, nous savons que `compute` ne lancera pas d'exception car elle est composée d'opérations qui ne lancent pas d'exception. En déclarant `compute` comme `noexcept`, nous donnons au compilateur et aux lecteurs l'information qui peut les aider à comprendre et manipuler `compute`.

**Remarque**

De nombreuses fonctions de la bibliothèque standard sont `noexcept`, y compris toutes celles héritées de la bibliothèque standard C.

**Exemple**

    vector<double> munge(const vector<double>& v) noexcept
    {
        vector<double> v2(v.size());
        // ... faire quelque chose ...
    }

Le `noexcept` indique que je ne suis pas disposé ou que je ne peux pas gérer la situation où je ne peux pas construire le `vector` local. Autrement dit, je considère l'épuisement de mémoire comme une erreur de conception grave (à l'échelon d'une panne matérielle) et suis prêt à faire planter le programme si cela se produit.

**Remarque**

Ne pas utiliser les spécifications d'exception traditionnelles.

**Voir aussi**

[discussion](028-discussion.md#sd-noexcept).

---

### <a name="re-never-throw"></a>E.13 : Ne jamais lancer une exception en étant le propriétaire direct d'un objet

**Raison**

Cela provoquerait une fuite.

**Exemple**

    void leak(int x)   // ne pas : risque de fuite
    {
        auto p = new int{7};
        if (x < 0) throw Get_me_out_of_here{};  // pourrait fuir *p
        // ...
        delete p;   // on peut ne jamais y arriver
    }

Une façon d'éviter de tels problèmes est d'utiliser des handles de ressource de façon cohérente :

    void no_leak(int x)
    {
        auto p = make_unique<int>(7);
        if (x < 0) throw Get_me_out_of_here{};  // supprime *p si nécessaire
        // ...
        // pas besoin de delete p
    }

Une autre solution (souvent meilleure) est d'utiliser une variable locale pour éliminer l'usage explicite de pointeurs :

    void no_leak_simplified(int x)
    {
        vector<int> v(7);
        // ...
    }

**Remarque**

Si vous avez un « truc » local qui nécessite un nettoyage mais n'est pas représenté par un objet ayant un destructeur, ce nettoyage doit également être effectué avant un `throw`.  
Parfois, `finally()` peut rendre un tel nettoyage un peu plus gérable.

---

### <a name="re-exception-types"></a>E.14 : Utiliser des types définis par l'utilisateur spécifiquement conçus comme exceptions (et non les types intégrés)

**Raison**

Un type défini par l'utilisateur peut mieux transmettre des informations d'erreur à un gestionnaire. Les informations peuvent être encodées dans le type lui‑même et ce type est peu susceptible de colider avec d'autres exceptions.

**Exemple**

    throw 7; // mauvais

    throw "something bad";  // mauvais

    throw std::exception{}; // mauvais – aucune info

Hériter de `std::exception` donne la flexibilité de capturer l'exception spécifique ou de gérer globalement via `std::exception` :

    class MyException : public std::runtime_error
    {
    public:
        MyException(const string& msg) : std::runtime_error{msg} {}
        // ...
    };

    // ...

    throw MyException{"something bad"};  // bon

Les exceptions ne doivent pas nécessairement dériver de `std::exception` :

    class MyCustomError final {};  // non dérivé de std::exception

    // ...

    throw MyCustomError{};  // bon – les gestionnaires doivent attraper ce type (ou ...)

Les types du standard dérivés de `std::exception` peuvent être utilisés comme exceptions génériques s'il n'est pas possible d'ajouter des informations utiles au point de détection :

    throw std::runtime_error("something bad"); // bon

    // ...

    throw std::invalid_argument("i is not even"); // bon

Les `enum` classes sont également permis  :

    enum class alert {RED, YELLOW, GREEN};

    throw alert::RED; // bon

**Application**

Attraper les `throw` de types intégrés et `std::exception`.

---

### <a name="re-exception-ref"></a>E.15 : Lancer par valeur, capturer les exceptions d'une hiérarchie par référence

**Raison**

Lancer par valeur (et non par pointeur) et capturer par référence empêche les copies, en particulier le tranchage des sous‑objets de base.

**Exemple ; mauvais**

    void f()
    {
        try {
            // ...
            throw new widget{}; // ne pas : lancer par valeur, pas par pointeur brut
            // ...
        }
        catch (base_class e) {  // ne pas : peut trancher
            // ...
        }
    }

Utilisez plutôt une référence :

    catch (base_class& e) { /* ... */ }

ou - généralement mieux - une référence constante :

    catch (const base_class& e) { /* ... */ }

La plupart des gestionnaires ne modifient pas leur exception et en général nous recommandons l'utilisation de `const`.

**Remarque**

Attraper par valeur peut convenir pour un petit type de valeur comme une valeur d'`enum`.

**Remarque**

Pour relancer une exception attrapée, utilisez `throw;` et non `throw e;`.  
Utiliser un `throw e;` lancerait une nouvelle copie de `e` (tranchée vers le type statique `std::exception`, lorsque l'exception est capturée par `catch (const std::exception& e)`) au lieu de relancer l'original `std::runtime_error`. (Mais gardez à l'esprit [ne pas tenter de capturer chaque exception dans chaque fonction](013-errors.md#re-not-always) et [minimiser l'usage explicite de `try`/`catch`](013-errors.md#re-catch)).

**Application**

* Marquer les captures par valeur d'un type qui possède une fonction virtuelle.  
* Marquer les lancers de pointeurs bruts.

---

### <a name="re-never-fail"></a>E.16 : Les destructeurs, la désallocation, `swap` et la création de copie/move d'une exception ne doivent jamais échouer

**Raison**

On ne sait pas comment écrire des programmes fiables si un destructeur, un échange, une désallocation ou la tentative de copie/move d'un objet d'exception échoue ; c'est‑à‑dire s'il se termine par une exception ou s'il ne réalise tout simplement pas l'action requise.

**Exemple, ne pas**

    class Connection {
        // ...
    public:
        ~Connection()   // Ne pas : destructeur très mauvais
        {
            if (cannot_disconnect()) throw I_give_up{information};
            // ...
        }
    };

**Remarque**

Beaucoup ont tenté d'écrire du code fiable violant cette règle, par exemple un réseau refusant de se fermer. À ce jour, personne n'a trouvé de manière générale de procéder.  
Il arrive parfois, dans des exemples très spécifiques, qu'on réussisse à mettre un état pour un nettoyage futur. Par exemple, nous pourrions placer un socket qui ne veut pas se fermer dans une liste « bad socket », à examiner par un balayage régulier de l'état du système. Tous les exemples que nous avons vus sont sujets aux erreurs, spécialisés et souvent problématiques.

**Remarque**

La bibliothèque standard suppose que les destructeurs, les fonctions de désallocation (ex. `operator delete`), et les fonctions `swap` ne lancent pas d'exception. Si elles le faisaient, les invariants de base de la bibliothèque standard seraient rompus.

**Remarque**

* Les fonctions de désallocation, y compris `operator delete`, doivent être `noexcept`.  
* Les fonctions `swap` doivent être `noexcept`.  
* La plupart des destructeurs sont implicitement `noexcept` par défaut.  
* De même, [rendre les opérations de mouvement `noexcept`](007-class.md#rc-move-noexcept).  
* Si vous écrivez un type destiné à être utilisé comme type d'exception, assurez‑vous que son constructeur de copie est `noexcept`. En général, nous ne pouvons pas l'imposer mécaniquement, car il n'est pas toujours clair qu'un type est destiné à être utilisé comme exception.  
* Essayez de ne pas `throw` un type dont le constructeur de copie n'est pas `noexcept`. En général nous ne pouvons pas l'imposer mécaniquement, car même `throw std::string(...)` pourrait lancer mais ne le fait pas en pratique.

**Application**

* Marquer les destructeurs, opérations de désallocation et `swap` qui `throw`.  
* Marquer les opérations qui ne sont pas `noexcept`.

**Voir aussi** : [discussion](028-discussion.md#sd-never-fail)

---

### <a name="re-not-always"></a>E.17 : Ne pas tenter de capturer toutes les exceptions dans chaque fonction

**Raison**

Capturer une exception dans une fonction qui ne peut pas prendre une action de récupération significative crée de la complexité et du gaspillage.  
Laissez une exception se propager jusqu'à une fonction qui peut potentiellement la gérer.  
Laissez les actions de nettoyage sur le chemin d'annulation être gérées par [RAII](013-errors.md#re-raii).

**Exemple, ne pas**

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

**Application**

* Marquer les blocs `try` imbriqués.  
* Marquer les fichiers source avec un ratio trop élevé de blocs `try` par fonction. (??? – Problème : définir « trop élevé »)

---

### <a name="re-catch"></a>E.18 : Minimiser l'usage explicite de `try`/`catch`

**Raison**

`try`/`catch` est verbeux et les utilisations non triviales sont sujettes à erreur.<br>
`try`/`catch` peut être un signe de gestion de ressources et de traitement d'erreurs non systématique ou de bas niveau.

**Exemple, mauvais**

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

Ce code encombrant.  
Il pourrait y avoir une fuite de pointeur non protégé dans le bloc `try`.  
Toutes les exceptions ne sont pas gérées.  
`delete` d'un objet qui n'a pas fini de se construire est très probablement une erreur.

**Meilleure solution**

    void f2(zstring s)
    {
        Gadget g {s};
    }

**Alternatives**

* Poignées de ressource appropriées et [RAII](013-errors.md#re-raii)  
* [`finally`](013-errors.md#re-finally)

**Application**

??? difficile ; besoin d'un heuristic

---

### <a name="re-finally"></a>E.19 : Utiliser un objet `final_action` pour exprimer le nettoyage si aucun handle de ressource approprié n'est disponible

**Raison**

`finally` de la [GSL](#gsl-guidelines-support-library) est moins verbeux et plus difficile à faire faux que `try`/`catch`.

**Exemple**

    void f(int n)
    {
        void* p = malloc(n);
        auto _ = gsl::finally([p] { free(p); });
        // ...
    }

**Remarque**

`finally` n'est pas aussi encombrant que `try`/`catch`, mais reste ad hoc.  
Préférez les [objets de gestion de ressources adéquats](013-errors.md#re-raii).  
Considérez `finally` comme un dernier recours.

**Remarque**

L'usage de `finally` est une alternative systématique et relativement propre à la vieille technique `goto exit;` pour gérer le nettoyage lorsqu'il n'y a pas de gestion systématique des ressources.

**Application**

Heuristique : détecter `goto exit;`.

---

### <a name="re-no-throw-raii"></a>E.25 : Si vous ne pouvez pas lancer d'exceptions, simuler RAII pour la gestion des ressources

**Raison**

Même sans exceptions, le RAII est généralement la meilleure façon systématique de gérer les ressources.

**Remarque**

La gestion d'erreurs par exceptions est le seul moyen complet et systématique de gérer les erreurs non locales en C++.  
En particulier, signaler de façon non intrusive un échec de construction d'un objet exige une exception.  
Signaler des erreurs de façon à ne pas pouvoir être ignorée nécessite des exceptions.  
Si vous ne pouvez pas utiliser d'exceptions, simulez leur utilisation au mieux.

Une grande peur des exceptions est mal fondée.  
Quand utilisé pour des circonstances exceptionnelles dans un code qui n'est pas jonché de pointeurs et de structures de contrôle compliquées, la gestion des exceptions est presque toujours abordable (en temps et en espace) et mène presque toujours à un code meilleur.  
Cela suppose une implémentation fiable des mécanismes de gestion des exceptions, qui n'est pas toujours disponible.  
Il existe également des cas où les problèmes ci‑dessus ne s'appliquent pas, mais les exceptions ne peuvent pas être utilisées pour d'autres raisons.  
Certains systèmes temps réel strict en sont un exemple : une opération doit être terminée dans un temps fixe avec une erreur ou une réponse correcte. En l'absence d'outils d'estimation du temps appropriés, il est difficile de garantir.  
Ces systèmes (ex. le logiciel de contrôle de vol) interdisent généralement l'utilisation de la mémoire dynamique (tas).

Donc, la directive principale pour la gestion des erreurs est « utiliser les exceptions et le RAII ».  
Cette section traite des cas où vous n'avez pas une implémentation efficace d'exceptions, ou un tas de code legacy utilisant beaucoup de pointeurs, une stratégie d'ownership illue, et beaucoup de gestion d'erreurs non systématique basée sur les codes d'erreur, ce qui rend difficile la prise de place d'une gestion exceptionnelle simple.

Avant de condamner les exceptions ou de se plaindre trop du coût, envisagez des exemples d'utilisation de codes d'erreur. Considérez le coût et la complexité de l'utilisation de codes d'erreur. Si la performance est votre souci, mesurez.

**Exemple**

Supposons que vous vouliez écrire

    void func(zstring arg)
    {
        Gadget g {arg};
        // ...
    }

Si le `gadget` n'est pas correctement construit, `func` se termine par une exception.  
Si nous ne pouvons pas lancer une exception, nous pouvons simuler ce style de gestion RAII en ajoutant une fonction membre `valid()` à `Gadget` :

    error_indicator func(zstring arg)
    {
        Gadget g {arg};
        if (!g.valid()) return gadget_construction_error;
        // ...
        return 0;   // zéro indique « bon »
    }

Le problème est bien sûr que l'appelant doit maintenant se souvenir de tester la valeur de retour. Pour inciter ce comportement, pensez à ajouter un `[[nodiscard]]`.

**Voir aussi** : [Discussion](#sd-???)

**Application**

Possible (uniquement) pour des versions spécifiques de cette idée : par ex. tester systématiquement `valid()` après la construction d'une poignée de ressource.

---

### <a name="re-no-throw-crash"></a>E.26 : Si vous ne pouvez pas lancer d'exceptions, envisager de sortir rapidement

**Raison**

Si vous ne pouvez pas faire un bon travail de récupération, vous pouvez au moins sortir avant que trop de dégâts conséquents ne soient commis.

**Voir aussi** : [Simulation de RAII](013-errors.md#re-no-throw-raii)

**Remarque**

Si vous ne pouvez pas gérer la fiabilité de la gestion d'erreurs, envisagez de « crasher » en réponse à toute erreur qui ne peut être traitée localement.  
C'est‑à‑dire, si vous ne pouvez pas récupérer d'une erreur dans le contexte de la fonction qui l'a détectée, appelez `abort()`, `quick_exit()` ou une fonction similaire qui déclenchera une forme de redémarrage du système.

Dans les systèmes avec beaucoup de processus et/ou d'ordinateurs, vous devez vous attendre et gérer les plantages fatals de toute façon, par ex. des pannes matérielles.  
Dans ces cas, « crasher » revient à laisser la gestion d'erreurs au niveau suivant du système.

**Exemple**

    void f(int n)
    {
        // ...
        p = static_cast<X*>(malloc(n * sizeof(X)));
        if (!p) abort();     // abort si mémoire épuisée
        // ...
    }

La plupart des programmes ne peuvent pas gérer l'épuisement de mémoire de façon gracieu.  
Ceci est pratiquement équivalent à

    void f(int n)
    {
        // ...
        p = new X[n];    // lance exception si mémoire épuisée (par défaut, termine)
        // ...
    }

Il est généralement une bonne idée d'enregistrer la raison du « crash » avant de quitter.

**Application**

Amusant

---

### <a name="re-no-throw-codes"></a>E.27 : Si vous ne pouvez pas lancer d'exceptions, utilisez systématiquement des codes d'erreur

**Raison**

Un usage systématique d'une stratégie de gestion d'erreur minimise la chance d'oublier de gérer une erreur.

**Voir aussi** : [Simulation de RAII](013-errors.md#re-no-throw-raii)

**Remarque**

Il y a plusieurs points à aborder :

* Comment transmettre un indicateur d'erreur hors d'une fonction ?  
* Comment libérer toutes les ressources d'une fonction avant de quitter sur une erreur ?  
* Que utilisez‑vous comme indicateur d'erreur ?

En général, retourner un indicateur d'erreur implique de retourner deux valeurs : le résultat et l'indicateur d'erreur.  
L'indicateur peut faire partie de l'objet, e.g., un objet peut avoir un indicateur `valid()` ou deux valeurs peuvent être retournées.

**Exemple**

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

Cette approche convient à [la gestion RAII simulée des ressources](013-errors.md#re-no-throw-raii).  
La fonction `valid()` peut retourner un `error_indicator` (e.g., un membre d'une énumération `error_indicator`).

**Exemple**

Que se passe‑il si nous ne pouvons pas ou ne voulons pas modifier le type `Gadget` ?  
Dans ce cas, il faut retourner une paire de valeurs.  
Par ex.:

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

Comme montré, `std::pair` est un type de retour possible.  
Certains préfèrent un type spécifique.  
Par ex.:

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

Une raison de préférer un type de retour spécifique est d'avoir des noms pour ses membres, plutôt que les cryptiques `first` et `second`, et d'éviter les confusions avec d'autres utilisations de `std::pair`.

**Exemple**

En général, vous devez libérer avant un arrêt d'erreur. Cela peut devenir désordonné :

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

Simuler RAII peut être non trivial, surtout dans des fonctions avec plusieurs ressources et plusieurs erreurs possibles.  
Une technique courante est de regrouper le nettoyage à la fin de la fonction pour éviter la répétition (notez que la portée supplémentaire autour de `g2` est indésirable mais nécessaire pour compilé la version `goto`):

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

Plus la fonction grandit, plus la tentation de ce technique augmente.  
`finally` peut [alléger un peu la douleur](013-errors.md#re-finally).  
En outre, au fur et à mesure que le programme grandit, il devient plus difficile d'appliquer de façon systématique une stratégie basée sur l'indicateur d'erreur.

Nous [préférons la gestion d'erreur basée sur les exceptions](013-errors.md#re-throw) et recommandons [de garder les fonctions courtes](006-functions.md#rf-single).

**Voir aussi** : [Discussion](#sd-???)

**Voir aussi** : [Retour de multiples valeurs](006-functions.md#rf-out-multi)

**Application**

Des difficultés.

---

### <a name="re-no-throw"></a>E.28 : Éviter le traitement d'erreurs basé sur l'état global (ex. `errno`)

**Raison**

L'état global est difficile à gérer et on oublie facilement de le vérifier.  
Quand avez‑vous test‑sans dernier fois le résultat de `printf()` ?

**Voir aussi** : [Simulation de RAII](013-errors.md#re-no-throw-raii)

**Exemple, mauvais**

    int last_err;

    void f(int n)
    {
        // ...
        p = static_cast<X*>(malloc(n * sizeof(X)));
        if (!p) last_err = -1;     // erreur si mémoire épuisée
        // ...
    }

**Remarque**

Le traitement d'erreurs en style C repose sur la variable globale `errno`, donc il est pratiquement impossible d'éviter complètement ce style.

**Application**

Des difficultés.

---

### <a name="re-specifications"></a>E.30 : Ne pas utiliser les spécifications d'exceptions

**Raison**

Les spécifications d'exceptions rendent la gestion d'erreur fragile, imposent un coût d'exécution, et ont été supprimées du standard C++.

**Exemple**

    int use(int arg)
        throw(X, Y)
    {
        // ...
        auto x = f(arg);
        // ...
    }

Si `f()` lance une exception différente d'`X` ou d'`Y`, le gestionnaire inattendu est invoqué, ce qui tue par défaut.  
C'est bon, mais supposons que nous ayons vérifié que cela ne se produit pas et que `f` lance une nouvelle exception `Z`, nous avons désormais un crash à moins de changer `use()` (et retester tout).  
Le problème est que `f()` peut être dans une bibliothèque que nous ne contrôlons pas et que la nouvelle exception n'est rien que `use()` pour prendre en compte ou qui n'est pas du tout d'intérêt à ce titre.  
On peut changer `use()` pour passer `Z` sans problème, mais alors les appelants de `use()` devront être modifiés.  
Ceci devient rapidement ingérable.  
Une alternative, on peut ajouter un bloc `try`/`catch` à `use()` pour mapper `Z` en une exception acceptable.  
Cela devient également ingérable rapidement.  
Notez que les changements du set d'exceptions se produisent souvent au niveau le plus bas d'un système (ex. à cause de modifications d'une bibliothèque réseau ou d'un middleware), donc les changements « bougent » à travers de longues chaînes d'appels.  
Dans une grande base de code, cela pourrait signifier que personne ne puisse mettre à jour une nouvelle version de la bibliothèque tant que le dernier utilisateur n'a pas été modifié.  
Si `use()` fait partie d'une bibliothèque, il n'est peut‑être pas possible de le mettre à jour car cela pourrait affecter des clients inconnus.

La politique de laisser les exceptions se propager jusqu'à une fonction qui peut potentiellement les gérer s'est « prouvée » au fil des années.

**Remarque**

Non. Cela ne serait pas mieux si les spécifications d'exceptions étaient statiquement imposées.  
Par ex. voir [Stroustrup94](032-bibliography.md#Stroustrup94).

**Remarque**

Si aucune exception ne peut être lancée, utilisez `noexcept`.

**Application**

Marquer chaque spécification d'exception.

---

### <a name="re_catch"></a>E.31 : Ordre correctement vos clauses `catch`

**Raison**

Les clauses `catch` sont évaluées dans l'ordre où elles apparaissent et une clause peut en masquer une autre.

**Exemple, mauvais**

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
Le gestionnaire qui attrape tout (`catch (...)`) a assuré que le gestionnaire `std::exception` ne sera jamais invoqué.

**Application**

Marquer les « gestionnaires dissimulés ».