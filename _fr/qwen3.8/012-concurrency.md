# <a name="s-concurrency"></a>CP : Concurrence et parallélisme

Nous souhaitons souvent que nos ordinateurs exécutent de nombreuses tâches simultanément (ou du moins qu'ils aient l'air de le faire).
Les raisons en sont variées (par exemple, attendre de nombreux événements en utilisant un seul processeur, traiter de nombreux flux de données simultanément, ou exploiter de nombreux périphériques matériels)
et les mécanismes de base pour exprimer la concurrence et le parallélisme le sont tout autant.
Ici, nous formulons des principes et des règles pour l'utilisation des fonctionnalités du standard ISO C++ destinées à exprimer la concurrence et le parallélisme de base.

Les fils d'exécution (*threads*) constituent le socle matériel de la programmation concurrente et parallèle.
Les fils d'exécution permettent d'exécuter de manière indépendante plusieurs sections d'un programme tout en partageant
la même mémoire. La programmation concurrente est délicate,
car protéger les données partagées entre les fils d'exécution est plus facile à dire qu'à faire.
Faire exécuter du code existant mono-fil en concurrence peut être
aussi simple que d'ajouter `std::async` ou `std::thread` de manière stratégique, ou nécessiter
une réécriture complète, selon que le code d'origine a été écrit
de manière favorable à la concurrence ou non.

Les règles de concurrence/parallélisme de ce document sont conçues avec trois objectifs
à l'esprit :

* Aider à écrire du code qui se prête à être utilisé dans un environnement
  multi-fils
* Montrer des façons propres et sûres d'utiliser les primitives de
  gestion des fils d'exécution offertes par la
  bibliothèque standard
* Offrir des conseils sur la marche à suivre lorsque la concurrence et le parallélisme n'apportent
  pas les gains de performance nécessaires

Il est également important de noter que la concurrence en C++ est une histoire
inachevée. C++11 a introduit de nombreuses primitives de concurrence de base, C++14 et C++17 les ont améliorées,
et il y a un vif intérêt à rendre la rédaction de
programmes concurrents en C++ encore plus facile. Nous nous attendons à ce que certaines des
orientations liées aux bibliothèques présentées ici évoluent significativement au fil du temps.

Cette section nécessite beaucoup de travail (évidemment).
Veuillez noter que nous commençons par des règles destinées aux non-experts.
Les vrais experts devront patienter un peu ;
les contributions sont les bienvenues,
mais veuillez penser à la majorité des programmeurs qui peinent à rendre leurs programmes concurrents corrects et performants.

Résumé des règles de concurrence et de parallélisme :

* [CP.1 : Partez du principe que votre code s'exécutera dans le cadre d'un programme multi-fils](012-concurrency.md#rconc-multi)
* [CP.2 : Évitez les conflits d'accès aux données](012-concurrency.md#rconc-races)
* [CP.3 : Minimisez le partage explicite de données modifiables](012-concurrency.md#rconc-data)
* [CP.4 : Pensez en termes de tâches, plutôt qu'en termes de fils d'exécution](012-concurrency.md#rconc-task)
* [CP.8 : N'essayez pas d'utiliser `volatile` pour la synchronisation](012-concurrency.md#rconc-volatile)
* [CP.9 : Utilisez des outils pour valider votre code concurrent dès que possible](012-concurrency.md#rconc-tools)

**Voir aussi** :

* [CP.con : Concurrence](012-concurrency.md#sscp-con)
* [CP.coro : Coroutines](012-concurrency.md#sscp-coro)
* [CP.par : Parallélisme](012-concurrency.md#sscp-par)
* [CP.mess : Passage de messages](012-concurrency.md#sscp-mess)
* [CP.vec : Vectorisation](012-concurrency.md#sscp-vec)
* [CP.free : Programmation sans verrou](012-concurrency.md#sscp-free)
* [CP.etc : Autres règles de concurrence](012-concurrency.md#sscp-etc)

### <a name="rconc-multi"></a>CP.1 : Partez du principe que votre code s'exécutera dans le cadre d'un programme multi-fils

##### Raison

Il est difficile d'être certain que la concurrence n'est pas utilisée actuellement ou ne le sera pas à l'avenir.
Le code est réutilisé.
Des bibliothèques n'utilisant pas de fils d'exécution peuvent être utilisées depuis une autre partie d'un programme qui, elle, en utilise.
Notez que cette règle s'applique le plus urgemment au code de bibliothèque et le moins aux applications autonomes.
Cependant, au fil du temps, des fragments de code peuvent apparaître dans des endroits inattendus.

##### Exemple, mauvais

    double cached_computation(int x)
    {
        // Mauvais : ces variables statiques provoquent des conflits d'accès en usage multi-fils
        static int cached_x = 0.0;
        static double cached_result = COMPUTATION_OF_ZERO;

        if (cached_x != x) {
            cached_x = x;
            cached_result = computation(x);
        }
        return cached_result;
    }

Bien que `cached_computation` fonctionne parfaitement dans un environnement mono-fil, dans un environnement multi-fils les deux variables `static` provoquent des conflits d'accès et donc un comportement indéfini.

##### Exemple, bon

    struct ComputationCache {
        int cached_x = 0;
        double cached_result = COMPUTATION_OF_ZERO;

        double compute(int x) {
            if (cached_x != x) {
                cached_x = x;
                cached_result = computation(x);
            }
            return cached_result;
        }
    };

Ici, le cache est stocké comme données membres d'un objet `ComputationCache`, plutôt que comme état statique partagé.
Cette refactoring délègue essentiellement la responsabilité vers le haut, au niveau de l'appelant : un programme mono-fil
peut toujours choisir d'avoir un `ComputationCache` global unique, tandis qu'un programme multi-fils peut
avoir une instance `ComputationCache` par fil d'exécution, ou une par « contexte » pour toute définition de « contexte ».
La fonction refactorisée ne tente plus de gérer l'allocation de `cached_x`. En ce sens,
c'est une application du Principe de Responsabilité Unique.

Dans cet exemple précis, le refactoring pour la sécurité des fils d'exécution a également amélioré la réutilisabilité dans les
programmes mono-fil. Il n'est pas difficile d'imaginer qu'un programme mono-fil pourrait vouloir deux instances de `ComputationCache`
pour un usage dans différentes parties du programme, sans qu'elles écrasent les données en cache de l'autre.

Il existe plusieurs autres façons d'ajouter la sécurité des fils d'exécution à un code écrit pour un environnement multi-fils standard
(c'est-à-dire un environnement où la seule forme de concurrence est `std::thread`) :

* Marquer les variables d'état comme `thread_local` au lieu de `static`.
* Implémenter un contrôle de concurrence, par exemple, protéger l'accès aux deux variables `static` avec un `static std::mutex`.
* Refuser de compiler et/ou d'exécuter dans un environnement multi-fils.
* Fournir deux implémentations : une pour les environnements mono-fil et une autre pour les environnements multi-fils.

##### Exception

Le code qui n'est jamais exécuté dans un environnement multi-fils.

Attention : il existe de nombreux exemples de code qui était « censé » ne jamais s'exécuter dans un programme multi-fils
et qui s'est exécuté dans le cadre d'un programme multi-fils, souvent des années plus tard.
Typiquement, de tels programmes mènent à un travail pénible pour éliminer les conflits d'accès.
Par conséquent, le code qui n'est jamais destiné à s'exécuter dans un environnement multi-fils doit être clairement étiqueté comme tel et idéalement accompagné de mécanismes d'application à la compilation ou à l'exécution pour détecter ces erreurs d'utilisation tôt.

### <a name="rconc-races"></a>CP.2 : Évitez les conflits d'accès aux données

##### Raison

À moins que vous ne le fassiez, rien n'est garanti de fonctionner et des erreurs subtiles persisteront.

##### Remarque

En résumé, si deux fils d'exécution peuvent accéder au même objet simultanément (sans synchronisation), et qu'au moins l'un est un écrivain (effectuant une opération non-`const`), vous avez un conflit d'accès.
Pour plus d'informations sur la manière d'utiliser correctement la synchronisation pour éliminer les conflits d'accès, veuillez consulter un bon livre sur la concurrence (voir [Étudiez attentivement la littérature](012-concurrency.md#rconc-literature)).

##### Exemple, mauvais

Il existe de nombreux exemples de conflits d'accès, certains d'entre eux tournant dans
des logiciels de production à cet instant même. Un exemple très simple :

    int get_id()
    {
      static int id = 1;
      return id++;
    }

L'incrémentation ici est un exemple de conflit d'accès. Cela peut mal tourner de nombreuses façons,
y compris :

* Le fil A charge la valeur de `id`, le système d'exploitation bascule le contexte de A pendant un
  certain temps, au cours duquel d'autres fils créent des centaines d'identifiants. Le fil A est alors
  autorisé à s'exécuter à nouveau, et `id` est réécrit à cet emplacement avec la valeur lue par A
  plus un.
* Les fils A et B chargent `id` et l'incrémentent simultanément. Ils obtiennent tous
  deux le même identifiant.

Les variables statiques locales sont une source courante de conflits d'accès.

##### Exemple, mauvais :

    void f(fstream& fs, regex pattern)
    {
        array<double, max> buf;
        int sz = read_vec(fs, buf, max);            // lit depuis fs dans buf
        gsl::span<double> s {buf};
        // ...
        auto h1 = async([&] { sort(std::execution::par, s); });     // lance une tâche de tri
        // ...
        auto h2 = async([&] { return find_all(buf, sz, pattern); });   // lance une tâche de recherche de correspondances
        // ...
    }

Ici, nous avons un (méchant) conflit d'accès sur les éléments de `buf` (`sort` lit et écrit).
Tous les conflits d'accès sont méchants.
Ici, nous avons réussi à provoquer un conflit d'accès sur des données sur la pile.
Tous les conflits d'accès ne sont pas aussi faciles à repérer que celui-ci.

##### Exemple, mauvais :

    // code non contrôlé par un verrou

    unsigned val;

    if (val < 5) {
        // ... un autre fil peut modifier val ici ...
        switch (val) {
        case 0: // ...
        case 1: // ...
        case 2: // ...
        case 3: // ...
        case 4: // ...
        }
    }

Maintenant, un compilateur qui ne sait pas que `val` peut changer implémentera très probablement ce `switch` à l'aide d'une table de saut avec cinq entrées.
Ensuite, une valeur de `val` hors de la plage `[0..4]` provoquera un saut vers une adresse qui pourrait être n'importe où dans le programme, et l'exécution se poursuivra à cet endroit.
Vraiment, « tout est possible » si vous avez un conflit d'accès.
En fait, cela peut être encore pire : en examinant le code généré, vous pourriez déterminer où le saut erratique ira pour une valeur donnée ;
cela peut constituer un risque de sécurité.

##### Application

Certaines vérifications sont possibles, faites au moins quelque chose.
Il existe des outils commerciaux et open source qui tentent d'aborder ce problème,
mais sachez que les solutions ont des coûts et des angles morts.
Les outils statiques ont souvent de nombreux faux positifs et les outils d'exécution ont souvent un coût significatif.
Nous espérons de meilleurs outils.
L'utilisation de plusieurs outils peut détecter plus de problèmes qu'un seul.

Il existe d'autres moyens d'atténuer le risque de conflits d'accès :

* Éviter les données globales
* Éviter les variables `static`
* Utiliser davantage de types concrets sur la pile (et ne pas passer trop de pointeurs)
* Utiliser davantage de données immuables (littéraux, `constexpr` et `const`)

### <a name="rconc-data"></a>CP.3 : Minimisez le partage explicite de données modifiables

##### Raison

Si vous ne partagez pas de données modifiables, vous ne pouvez pas avoir de conflit d'accès.
Moins vous partagez, moins vous risquez d'oublier de synchroniser l'accès (et de provoquer des conflits d'accès).
Moins vous partagez, moins vous risquez d'attendre un verrou (ce qui peut améliorer les performances).

##### Exemple

    bool validate(const vector<Reading>&);
    Graph<Temp_node> temperature_gradients(const vector<Reading>&);
    Image altitude_map(const vector<Reading>&);
    // ...

    void process_readings(const vector<Reading>& surface_readings)
    {
        auto h1 = async([&] { if (!validate(surface_readings)) throw Invalid_data{}; });
        auto h2 = async([&] { return temperature_gradients(surface_readings); });
        auto h3 = async([&] { return altitude_map(surface_readings); });
        // ...
        h1.get();
        auto v2 = h2.get();
        auto v3 = h3.get();
        // ...
    }

Sans ces `const`, nous devrions examiner chaque fonction appelée asynchronement pour détecter d'éventuels conflits d'accès sur `surface_readings`.
Rendre `surface_readings` `const` (par rapport à cette fonction) permet de raisonner en utilisant uniquement le corps de la fonction.

##### Remarque

Les données immuables peuvent être partagées en toute sécurité et efficacement.
Aucun verrouillage n'est nécessaire : on ne peut pas avoir de conflit d'accès sur une constante.
Voir aussi [CP.mess : Passage de messages](012-concurrency.md#sscp-mess) et [CP.31 : privilégier le passage par valeur](012-concurrency.md#rconc-data-by-value).

##### Application

???


### <a name="rconc-task"></a>CP.4 : Pensez en termes de tâches, plutôt qu'en termes de fils d'exécution

##### Raison

Un `thread` est un concept d'implémentation, une manière de penser la machine.
Une tâche est un notion applicative, quelque chose que vous souhaitez faire, de préférence en parallèle avec d'autres tâches.
Les notions applicatives sont plus faciles à appréhender.

##### Exemple

    void some_fun(const std::string& msg)
    {
        std::thread publisher([=] { std::cout << msg; });      // Mauvais : moins expressif
                                                               //      et plus sujet aux erreurs
        auto pubtask = std::async([=] { std::cout << msg; });  // OK
        // ...
        publisher.join();
    }

##### Remarque

À l'exception de `async()`, les fonctionnalités de la bibliothèque standard sont de bas niveau, orientées machine, au niveau des fils d'exécution et des verrous.
C'est une base nécessaire, mais nous devons essayer d'élever le niveau d'abstraction : pour la productivité, la fiabilité, et les performances.
C'est un argument puissant en faveur de l'utilisation de bibliothèques de plus haut niveau, plus orientées applications (si possible, construites sur les fonctionnalités de la bibliothèque standard).

##### Application

???

### <a name="rconc-volatile"></a>CP.8 : N'essayez pas d'utiliser `volatile` pour la synchronisation

##### Raison

En C++, contrairement à d'autres langages, `volatile` ne fournit pas l'atomicité, ne synchronise pas entre les fils d'exécution,
et n'empêche pas le réordonnancement des instructions (ni par le compilateur ni par le matériel).
Il n'a simplement rien à voir avec la concurrence.

##### Exemple, mauvais :

    int free_slots = max_slots; // source actuelle de mémoire pour les objets

    Pool* use()
    {
        if (int n = free_slots--) return &pool[n];
    }

Ici, nous avons un problème :
C'est un code parfaitement correct dans un programme mono-fil, mais si deux fils d'exécution exécutent ce code,
il y a une condition de course sur `free_slots` de sorte que deux fils peuvent obtenir la même valeur et `free_slots`.
C'est (évidemment) un mauvais conflit d'accès, de sorte que des personnes formées dans d'autres langages pourraient essayer de le corriger ainsi :

    volatile int free_slots = max_slots; // source actuelle de mémoire pour les objets

    Pool* use()
    {
        if (int n = free_slots--) return &pool[n];
    }

Cela n'a aucun effet sur la synchronisation : le conflit d'accès est toujours là !

Le mécanisme C++ pour cela est les types `atomic` :

    atomic<int> free_slots = max_slots; // source actuelle de mémoire pour les objets

    Pool* use()
    {
        if (int n = free_slots--) return &pool[n];
    }

Maintenant l'opération `--` est atomique,
plutôt qu'une séquence lecture-incrément-écriture où un autre fil pourrait s'intercaler entre les opérations individuelles.

##### Alternative

Utilisez les types `atomic` là où vous auriez pu utiliser `volatile` dans un autre langage.
Utilisez un `mutex` pour des exemples plus complexes.

##### Voir aussi

[(rare) usages appropriés de `volatile`](012-concurrency.md#rconc-volatile2)

### <a name="rconc-tools"></a>CP.9 : Utilisez des outils pour valider votre code concurrent dès que possible

L'expérience montre que le code concurrent est exceptionnellement difficile à obtenir correctement
et que la vérification à la compilation, les vérifications à l'exécution et les tests sont moins efficaces pour détecter les erreurs de concurrence
que pour détecter les erreurs dans le code séquentiel.
Les erreurs de concurrence subtiles peuvent avoir des effets dramatiquement néfastes, y compris la corruption de mémoire, les interblocages, et les vulnérabilités de sécurité.

##### Exemple

    ???

##### Remarque

La sécurité des fils d'exécution est un défi, souvent remportant sur les programmeurs expérimentés : les outils sont une stratégie importante pour atténuer ces risques.
Il existe de nombreux outils « là-bas », tant commerciaux qu'open source, tant de recherche que de production.
Malheureusement, les besoins et les contraintes des gens diffèrent tellement que nous ne pouvons pas faire de recommandations spécifiques,
mais nous pouvons mentionner :

* Outils de vérification statique : tant [clang](https://clang.llvm.org/docs/ThreadSafetyAnalysis.html)
que certaines versions antérieures de [GCC](https://gcc.gnu.org/wiki/ThreadSafetyAnnotation)
ont un certain support pour l'annotation statique des propriétés de sécurité des fils d'exécution.
L'utilisation cohérente de cette technique transforme de nombreuses classes d'erreurs de sécurité des fils d'exécution en erreurs de compilation.
Les annotations sont généralement locales (marquant un membre de données particulier comme protégé par un mutex particulier),
et sont généralement faciles à apprendre. Cependant, comme pour de nombreux outils statiques, il peut souvent présenter des faux négatifs ;
des cas qui auraient dû être détectés mais qui ont été autorisés.

* Outils de vérification dynamique : le [Thread Sanitizer](https://clang.llvm.org/docs/ThreadSanitizer.html) de Clang (aka TSAN)
est un puissant exemple d'outils dynamiques : il modifie la compilation et l'exécution de votre programme pour ajouter un suivi des accès mémoire,
identifiant absolument les conflits d'accès dans une exécution donnée de votre binaire.
Le coût est à la fois en mémoire (5 à 10 fois dans la plupart des cas) et en ralentissement CPU (2 à 20 fois).
Les outils dynamiques comme celui-ci sont les meilleurs lorsqu'ils sont appliqués aux tests d'intégration, aux déploiements canaris, ou aux tests unitaires qui opèrent sur plusieurs fils d'exécution.
La charge de travail compte : lorsque TSAN identifie un problème, c'est pratiquement toujours un vrai conflit d'accès,
mais il ne peut identifier que les conflits observés dans une exécution donnée.

##### Application

C'est à l'éditeur d'application de choisir quels outils de support sont précieux pour une application particulière.

## <a name="sscp-con"></a>CP.con : Concurrence

Cette section se concentre sur les utilisations relativement ad hoc de plusieurs fils d'exécution communiquant par le biais de données partagées.

* Pour les algorithmes parallèles, voir [parallélisme](012-concurrency.md#sscp-par)
* Pour la communication inter-tâches sans partage explicite, voir [passage de messages](012-concurrency.md#sscp-mess)
* Pour le code parallèle vectorisé, voir [vectorisation](012-concurrency.md#sscp-vec)
* Pour la programmation sans verrou, voir [sans verrou](012-concurrency.md#sscp-free)

Résumé des règles de concurrence :

* [CP.20 : Utilisez RAII, jamais de `lock()`/`unlock()` nus](012-concurrency.md#rconc-raii)
* [CP.21 : Utilisez `std::lock()` ou `std::scoped_lock` pour acquérir plusieurs `mutex`](012-concurrency.md#rconc-lock)
* [CP.22 : N'appellez jamais de code inconnu en tenant un verrou (par ex. un callback)](012-concurrency.md#rconc-unknown)
* [CP.23 : Considérez un `thread` qui joint comme un conteneur à portée](012-concurrency.md#rconc-join)
* [CP.24 : Considérez un `thread` comme un conteneur global](012-concurrency.md#rconc-detach)
* [CP.25 : Préférez `gsl::joining_thread` à `std::thread`](012-concurrency.md#rconc-joining_thread)
* [CP.26 : Ne `detach()`-ez pas un fil d'exécution](012-concurrency.md#rconc-detached_thread)
* [CP.31 : Passez de petites quantités de données entre fils d'exécution par valeur, plutôt que par référence ou pointeur](012-concurrency.md#rconc-data-by-value)
* [CP.32 : Pour partager la propriété entre des `thread` non liés, utilisez `shared_ptr`](012-concurrency.md#rconc-shared)
* [CP.40 : Minimisez les bascules de contexte](012-concurrency.md#rconc-switch)
* [CP.41 : Minimisez la création et la destruction de fils d'exécution](012-concurrency.md#rconc-create)
* [CP.42 : Ne `wait`-ez pas sans condition](012-concurrency.md#rconc-wait)
* [CP.43 : Minimisez le temps passé dans une section critique](012-concurrency.md#rconc-time)
* [CP.44 : N'oubliez pas de nommer vos `lock_guard` et `unique_lock`](012-concurrency.md#rconc-name)
* [CP.50 : Définissez un `mutex` avec les données qu'il protège. Utilisez `synchronized_value<T>` lorsque c'est possible](012-concurrency.md#rconc-mutex)
* ??? quand utiliser un spinlock
* ??? quand utiliser `try_lock()`
* ??? quand préférer `lock_guard` à `unique_lock`
* ??? Multiplexage temporel
* ??? quand/comment utiliser `new thread`

### <a name="rconc-raii"></a>CP.20 : Utilisez RAII, jamais de `lock()`/`unlock()` nus

##### Raison

Évite les erreurs désastreuses dues à des verrous non libérés.

##### Exemple, mauvais

    mutex mtx;

    void do_stuff()
    {
        mtx.lock();
        // ... faire des choses ...
        mtx.unlock();
    }

Plus ou moins tôt, quelqu'un oubliera le `mtx.unlock()`, placera un `return` dans le `... faire des choses ...`, lancera une exception, ou autre chose.

    mutex mtx;

    void do_stuff()
    {
        unique_lock<mutex> lck {mtx};
        // ... faire des choses ...
    }

##### Application

Signaler les appels de membres `lock()` et `unlock()`.  ???


### <a name="rconc-lock"></a>CP.21 : Utilisez `std::lock()` ou `std::scoped_lock` pour acquérir plusieurs `mutex`

##### Raison

Pour éviter les interblocages sur plusieurs `mutex`.

##### Exemple

Cela invite à l'interblocage :

    // fil 1
    lock_guard<mutex> lck1(m1);
    lock_guard<mutex> lck2(m2);

    // fil 2
    lock_guard<mutex> lck2(m2);
    lock_guard<mutex> lck1(m1);

Au lieu de cela, utilisez `lock()` :

    // fil 1
    lock(m1, m2);
    lock_guard<mutex> lck1(m1, adopt_lock);
    lock_guard<mutex> lck2(m2, adopt_lock);

    // fil 2
    lock(m2, m1);
    lock_guard<mutex> lck2(m2, adopt_lock);
    lock_guard<mutex> lck1(m1, adopt_lock);

ou (mieux, mais C++17 uniquement) :

    // fil 1
    scoped_lock<mutex, mutex> lck1(m1, m2);

    // fil 2
    scoped_lock<mutex, mutex> lck2(m2, m1);

Ici, les auteurs de `thread1` et `thread2` ne sont toujours pas d'accord sur l'ordre des `mutex`, mais l'ordre n'a plus d'importance.

##### Remarque

Dans le code réel, les `mutex` sont rarement nommés de manière à rappeler commodément au programmeur une relation et un ordre d'acquisition intended.
Dans le code réel, les `mutex` ne sont pas toujours acquis commodément sur des lignes consécutives.

##### Remarque

En C++17, il est possible d'écrire simplement

    lock_guard lck1(m1, adopt_lock);

et d'avoir le type `mutex` déduit.

##### Application

Détecter l'acquisition de plusieurs `mutex`.
Cela est indécidable en général, mais capturer des exemples simples courants (comme celui ci-dessus) est facile.


### <a name="rconc-unknown"></a>CP.22 : N'appellez jamais de code inconnu en tenant un verrou (par ex. un callback)

##### Raison

Si vous ne savez pas ce qu'un morceau de code fait, vous risquez un interblocage.

##### Exemple

    void do_this(Foo* p)
    {
        lock_guard<mutex> lck {my_mutex};
        // ... faire quelque chose ...
        p->act(my_data);
        // ...
    }

Si vous ne savez pas ce que `Foo::act` fait (peut-être est-ce une fonction virtuelle appelant un membre de classe dérivée d'une classe pas encore écrite),
elle pourrait appeler `do_this` (récursivement) et provoquer un interblocage sur `my_mutex`.
Peut-être verrouillera-t-elle sur un mutex différent et ne reviendra-t-elle pas dans un temps raisonnable, provoquant des retards pour tout code appelant `do_this`.

##### Exemple

Un exemple courant du problème d'« appel de code inconnu » est un appel à une fonction qui tente d'obtenir un accès verrouillé au même objet.
Ce problème peut souvent être résolu en utilisant un `recursive_mutex`. Par exemple :

    recursive_mutex my_mutex;

    template<typename Action>
    void do_something(Action f)
    {
        unique_lock<recursive_mutex> lck {my_mutex};
        // ... faire quelque chose ...
        f(this);    // f fera quelque chose à *this
        // ...
    }

Si, comme c'est probable, `f()` invoque des opérations sur `*this`, nous devons nous assurer que l'invariant de l'objet est respecté avant l'appel.

##### Application

* Signaler l'appel d'une fonction virtuelle en tenant un `mutex` non récursif
* Signaler l'appel d'un callback en tenant un `mutex` non récursif


### <a name="rconc-join"></a>CP.23 : Considérez un `thread` qui joint comme un conteneur à portée

##### Raison

Pour maintenir la sécurité des pointeurs et éviter les fuites, nous devons considérer quels pointeurs sont utilisés par un `thread`.
Si un `thread` joint, nous pouvons passer en toute sécurité des pointeurs vers des objets dans la portée du `thread` et de ses portées englobantes.

##### Exemple

    void f(int* p)
    {
        // ...
        *p = 99;
        // ...
    }
    int glob = 33;

    void some_fct(int* p)
    {
        int x = 77;
        joining_thread t0(f, &x);           // OK
        joining_thread t1(f, p);            // OK
        joining_thread t2(f, &glob);        // OK
        auto q = make_unique<int>(99);
        joining_thread t3(f, q.get());      // OK
        // ...
    }

Un `gsl::joining_thread` est un `std::thread` avec un destructeur qui joint et qui ne peut pas être `detach()`-é.
Par « OK », nous entendons que l'objet sera dans la portée (« vivant ») aussi longtemps qu'un `thread` peut utiliser le pointeur vers lui.
Le fait que les `thread` s'exécutent en parallèle n'affecte pas les questions de durée de vie ou de propriété ici ;
ces `thread` peuvent être considérés comme simplement un objet fonction appelé depuis `some_fct`.

##### Application

S'assurer que les `joining_thread` ne `detach()`-ent pas.
Après cela, l'application habituelle de la durée de vie et de la propriété (pour les objets locaux) s'applique.

### <a name="rconc-detach"></a>CP.24 : Considérez un `thread` comme un conteneur global

##### Raison

Pour maintenir la sécurité des pointeurs et éviter les fuites, nous devons considérer quels pointeurs sont utilisés par un `thread`.
Si un `thread` est détaché, nous ne pouvons passer en toute sécurité que des pointeurs vers des objets statiques et de la zone libre (uniquement).

##### Exemple

    void f(int* p)
    {
        // ...
        *p = 99;
        // ...
    }

    int glob = 33;

    void some_fct(int* p)
    {
        int x = 77;
        std::thread t0(f, &x);           // Mauvais
        std::thread t1(f, p);            // Mauvais
        std::thread t2(f, &glob);        // OK
        auto q = make_unique<int>(99);
        std::thread t3(f, q.get());      // Mauvais
        // ...
        t0.detach();
        t1.detach();
        t2.detach();
        t3.detach();
        // ...
    }

Par « OK », nous entendons que l'objet sera dans la portée (« vivant ») aussi longtemps qu'un `thread` peut utiliser les pointeurs vers lui.
Par « Mauvais », nous entendons qu'un `thread` pourrait utiliser un pointeur après que l'objet pointé a été détruit.
Le fait que les `thread` s'exécutent en parallèle n'affecte pas les questions de durée de vie ou de propriété ici ;
ces `thread` peuvent être considérés comme simplement un objet fonction appelé depuis `some_fct`.

##### Remarque

Même les objets avec une durée de vie statique peuvent poser problème s'ils sont utilisés depuis des fils d'exécution détachés : si le
fil continue jusqu'à la fin du programme, il pourrait s'exécuter en parallèle avec la destruction
des objets à durée de vie statique, et ainsi les accès à de tels objets pourraient entrer en conflit.

##### Remarque

Cette règle est redondante si vous [ne `detach()`-ez pas](012-concurrency.md#rconc-detached_thread) et [utilisez `gsl::joining_thread`](012-concurrency.md#rconc-joining_thread).
Cependant, convertir le code pour suivre ces directives pourrait être difficile et même impossible pour les bibliothèques tierces.
Dans de tels cas, la règle devient essentielle pour la sécurité de la durée de vie et la sécurité des types.


En général, il est indécidable si un `detach()` est exécuté pour un `thread`, mais les cas courants simples sont facilement détectés.
Si nous ne pouvons pas prouver qu'un `thread` ne `detach()`-e pas, nous devons supposer qu'il le fait et qu'il survit à la portée dans laquelle il a été construit ;
après cela, l'application habituelle de la durée de vie et de la propriété (pour les objets globaux) s'applique.

##### Application

Signaler les tentatives de passer des variables locales à un fil d'exécution qui pourrait `detach()`-er.

### <a name="rconc-joining_thread"></a>CP.25 : Préférez `gsl::joining_thread` à `std::thread`

##### Raison

Un `joining_thread` est un fil d'exécution qui joint à la fin de sa portée.
Les fils d'exécution détachés sont difficiles à surveiller.
Il est plus difficile de garantir l'absence d'erreurs dans les fils d'exécution détachés (et potentiellement détachés).

##### Exemple, mauvais

    void f() { std::cout << "Hello "; }

    struct F {
        void operator()() const { std::cout << "parallel world "; }
    };

    int main()
    {
        std::thread t1{f};      // f() s'exécute dans un fil séparé
        std::thread t2{F()};    // F()() s'exécute dans un fil séparé
    }  // repérez les bugs

##### Exemple

    void f() { std::cout << "Hello "; }

    struct F {
        void operator()() const { std::cout << "parallel world "; }
    };

    int main()
    {
        std::thread t1{f};      // f() s'exécute dans un fil séparé
        std::thread t2{F()};    // F()() s'exécute dans un fil séparé

        t1.join();
        t2.join();
    }  // un mauvais bug reste

##### Remarque

Rendez les « fils immortels » globaux, placez-les dans une portée englobante, ou placez-les dans la zone libre plutôt que de `detach()`-er.
[Ne `detach()`-ez pas](012-concurrency.md#rconc-detached_thread).

##### Remarque

En raison de l'ancien code et des bibliothèques tierces utilisant `std::thread`, cette règle peut être difficile à introduire.

##### Application

Signaler les utilisations de `std::thread` :

* Suggérer l'utilisation de `gsl::joining_thread` ou de `std::jthread` C++20.
* Suggérer l'« [exportation de la propriété](012-concurrency.md#rconc-detached_thread) » vers une portée englobante s'il détache.
* Avertir s'il n'est pas évident si un fil joint ou détache.

### <a name="rconc-detached_thread"></a>CP.26 : Ne `detach()`-ez pas un fil d'exécution

##### Raison

Souvent, le besoin de survivre à la portée de sa création est inhérent à la tâche du `thread`,
mais implémenter cette idée par `detach` le rend plus difficile à surveiller et à communiquer avec le fil détaché.
En particulier, il est plus difficile (bien que pas impossible) de garantir que le fil s'est terminé comme prévu ou vit aussi longtemps que prévu.

##### Exemple

    void heartbeat();

    void use()
    {
        std::thread t(heartbeat);             // ne pas joindre ; heartbeat est censé tourner indéfiniment
        t.detach();
        // ...
    }

C'est un usage raisonnable d'un fil d'exécution, pour lequel `detach()` est couramment utilisé.
Il y a des problèmes, cependant.
Comment surveillons-nous le fil détaché pour voir s'il est vivant ?
Quelque chose pourrait mal tourner avec le heartbeat, et perdre un heartbeat peut être très grave dans un système qui en a besoin.
Donc, nous devons communiquer avec le fil heartbeat
(par exemple, à travers un flux de messages ou des événements de notification utilisant un `condition_variable`).

Une alternative, et généralement une solution supérieure, est de contrôler sa durée de vie en le plaçant dans une portée extérieure à son point de création (ou d'activation).
Par exemple :

    void heartbeat();

    gsl::joining_thread t(heartbeat);             // heartbeat est censé tourner « indéfiniment »

Ce heartbeat tournera (à moins d'erreur, de problème matériel, etc.) aussi longtemps que le programme.

Parfois, nous devons séparer le point de création du point de propriété :

    void heartbeat();

    unique_ptr<gsl::joining_thread> tick_tock {nullptr};

    void use()
    {
        // heartbeat est censé tourner aussi longtemps que tick_tock vit
        tick_tock = make_unique<gsl::joining_thread>(heartbeat);
        // ...
    }

#### Application

Signaler `detach()`.


### <a name="rconc-data-by-value"></a>CP.31 : Passez de petites quantités de données entre fils d'exécution par valeur, plutôt que par référence ou pointeur

##### Raison

Une petite quantité de données est moins coûteuse à copier et à accéder qu'à partager à l'aide d'un mécanisme de verrouillage.
La copie donne naturellement une propriété unique (simplifie le code) et élimine la possibilité de conflits d'accès.

##### Remarque

Définir précisément « petite quantité » est impossible.

##### Exemple

    string modify1(string);
    void modify2(string&);

    void fct(string& s)
    {
        auto res = async(modify1, s);
        async(modify2, s);
    }

L'appel de `modify1` implique la copie de deux valeurs `string` ; l'appel de `modify2` ne le fait pas.
D'autre part, l'implémentation de `modify1` est exactement celle que nous aurions écrite pour du code mono-fil,
tandis que l'implémentation de `modify2` aura besoin d'une forme de verrouillage pour éviter les conflits d'accès.
Si la chaîne est courte (disons 10 caractères), l'appel de `modify1` peut être surprenamment rapide ;
essentiellement tout le coût est dans la bascule de `thread`. Si la chaîne est longue (disons 1 000 000 de caractères), la copier deux fois
n'est probablement pas une bonne idée.

Notez que cet argument n'a rien à voir avec `async` en soi. Il s'applique également aux considérations sur l'utilisation
du passage de messages ou de la mémoire partagée.

##### Application

???


### <a name="rconc-shared"></a>CP.32 : Pour partager la propriété entre des `thread` non liés, utilisez `shared_ptr`

##### Raison

Si les fils d'exécution sont non liés (c'est-à-dire, non connus pour être dans la même portée ou l'un dans la durée de vie de l'autre)
et qu'ils doivent partager de la mémoire de la zone libre qui doit être supprimée, un `shared_ptr` (ou équivalent) est le seul
moyen sûr de garantir une suppression appropriée.

##### Exemple

    ???

##### Remarque

* Un objet statique (par ex. un global) peut être partagé car il n'est pas possédé au sens où un fil d'exécution est responsable de sa suppression.
* Un objet dans la zone libre qui ne doit jamais être supprimé peut être partagé.
* Un objet possédé par un fil d'exécution peut être partagé en toute sécurité avec un autre tant que ce second fil ne survit pas au propriétaire.

##### Application

???


### <a name="rconc-switch"></a>CP.40 : Minimisez les bascules de contexte

##### Raison

Les bascules de contexte sont coûteuses.

##### Exemple

    ???

##### Application

???


### <a name="rconc-create"></a>CP.41 : Minimisez la création et la destruction de fils d'exécution

##### Raison

La création de fils d'exécution est coûteuse.

##### Exemple

    void worker(Message m)
    {
        // traiter
    }

    void dispatcher(istream& is)
    {
        for (Message m; is >> m; )
            run_list.push_back(new thread(worker, m));
    }

Cela crée un `thread` par message, et le `run_list` est présumé géré pour détruire ces tâches une fois terminées.

Au lieu de cela, nous pourrions avoir un ensemble de fils d'exécution de travail pré-créés traitant les messages

    Sync_queue<Message> work;

    void dispatcher(istream& is)
    {
        for (Message m; is >> m; )
            work.put(m);
    }

    void worker()
    {
        for (Message m; m = work.get(); ) {
            // traiter
        }
    }

    void workers()  // configure les fils de travail (spécifiquement 4 fils de travail)
    {
        joining_thread w1 {worker};
        joining_thread w2 {worker};
        joining_thread w3 {worker};
        joining_thread w4 {worker};
    }

##### Remarque

Si votre système a une bonne pool de fils d'exécution, utilisez-la.
Si votre système a une bonne file de messages, utilisez-la.

##### Application

???


### <a name="rconc-wait"></a>CP.42 : Ne `wait`-ez pas sans condition

##### Raison

Un `wait` sans condition peut manquer un réveil ou se réveiller simplement pour découvrir qu'il n'y a pas de travail à faire.

##### Exemple, mauvais

    std::condition_variable cv;
    std::mutex mx;

    void thread1()
    {
        while (true) {
            // faire du travail ...
            std::unique_lock<std::mutex> lock(mx);
            cv.notify_one();    // réveiller l'autre fil
        }
    }

    void thread2()
    {
        while (true) {
            std::unique_lock<std::mutex> lock(mx);
            cv.wait(lock);    // pourrait bloquer indéfiniment
            // faire du travail ...
        }
    }

Ici, si un autre `thread` consomme la notification de `thread1`, `thread2` peut attendre indéfiniment.

##### Exemple

    template<typename T>
    class Sync_queue {
    public:
        void put(const T& val);
        void put(T&& val);
        void get(T& val);
    private:
        mutex mtx;
        condition_variable cond;    // cela contrôle l'accès
        list<T> q;
    };

    template<typename T>
    void Sync_queue<T>::put(const T& val)
    {
        lock_guard<mutex> lck(mtx);
        q.push_back(val);
        cond.notify_one();
    }

    template<typename T>
    void Sync_queue<T>::get(T& val)
    {
        unique_lock<mutex> lck(mtx);
        cond.wait(lck, [this] { return !q.empty(); });    // prévenir le réveil intempestif
        val = q.front();
        q.pop_front();
    }

Maintenant, si la file est vide lorsqu'un fil exécutant `get()` se réveille (par exemple, parce qu'un autre fil est arrivé à `get()` avant lui),
il retournera immédiatement en sommeil, en attente.

##### Application

Signaler tous les `wait` sans conditions.


### <a name="rconc-time"></a>CP.43 : Minimisez le temps passé dans une section critique

##### Raison

Moins de temps est passé avec un `mutex` acquis, moins un autre `thread` a de chances d'attendre,
et la suspension et la reprise des `thread` sont coûteuses.

##### Exemple

    void do_something() // Mauvais
    {
        unique_lock<mutex> lck(my_lock);
        do0();  // préparation : n'a pas besoin de verrou
        do1();  // transaction : a besoin de verrouillage
        do2();  // nettoyage : n'a pas besoin de verrouillage
    }

Ici, nous tenons le verrou plus longtemps que nécessaire :
Nous ne devrions pas avoir pris le verrou avant d'en avoir besoin et devrions l'avoir relâché avant de commencer le nettoyage.
Nous pourrions réécrire cela ainsi

    void do_something() // Mauvais
    {
        do0();  // préparation : n'a pas besoin de verrou
        my_lock.lock();
        do1();  // transaction : a besoin de verrouillage
        my_lock.unlock();
        do2();  // nettoyage : n'a pas besoin de verrouillage
    }

Mais cela compromet la sécurité et viole la règle [utiliser RAII](012-concurrency.md#rconc-raii).
Au lieu de cela, ajoutez un bloc pour la section critique :

    void do_something() // OK
    {
        do0();  // préparation : n'a pas besoin de verrou
        {
            unique_lock<mutex> lck(my_lock);
            do1();  // transaction : a besoin de verrouillage
        }
        do2();  // nettoyage : n'a pas besoin de verrouillage
    }

##### Application

Impossible en général.
Signaler les `lock()` et `unlock()` « nus ».


### <a name="rconc-name"></a>CP.44 : N'oubliez pas de nommer vos `lock_guard` et `unique_lock`

##### Raison

Un objet local non nommé est un objet temporaire qui sort immédiatement de portée.

##### Exemple

    // mutex globaux
    mutex m1;
    mutex m2;

    void f()
    {
        unique_lock<mutex>(m1); // (A)
        lock_guard<mutex> {m2}; // (B)
        // faire du travail dans la section critique ...
    }

Cela semble inoffensif, mais ne l'est pas. À (A), `m1` est un
`unique_lock` local construit par défaut, qui masque le `::m1` global (et ne le verrouille pas).
À (B), un `lock_guard` temporaire non nommé est construit et verrouille `::m2`,
mais sort immédiatement de portée et déverrouille `::m2` à nouveau.
Pour le reste de la fonction `f()`, aucun des deux mutex n'est verrouillé.

##### Application

Signaler tous les `lock_guard` et `unique_lock` non nommés.



### <a name="rconc-mutex"></a>CP.50 : Définissez un `mutex` avec les données qu'il protège. Utilisez `synchronized_value<T>` lorsque c'est possible

##### Raison

Il devrait être évident pour un lecteur que les données sont à protéger et comment. Cela diminue la probabilité que le mauvais mutex soit verrouillé, ou que le mutex ne soit pas verrouillé.

L'utilisation d'un `synchronized_value<T>` garantit que les données ont un mutex, et que le bon mutex est verrouillé lorsque les données sont accédées.
Voir la [proposition WG21](https://www.open-std.org/jtc1/sc22/wg21/docs/papers/2023/p0290r4.html) pour ajouter `synchronized_value` à une future TS ou révision du standard C++.

##### Exemple

    struct Record {
        std::mutex m;   // prendre ce mutex avant d'accéder aux autres membres
        // ...
    };

    class MyClass {
        struct DataRecord {
           // ...
        };
        synchronized_value<DataRecord> data; // Protéger les données avec un mutex
    };

##### Application

??? Possible ?


## <a name="sscp-coro"></a>CP.coro : Coroutines

Cette section se concentre sur les utilisations de coroutines.

Résumé des règles de coroutines :

* [CP.51 : N'utilisez pas de lambdas capturant qui sont des coroutines](012-concurrency.md#rcoro-capture)
* [CP.52 : Ne tenez pas de verrous ou d'autres primitives de synchronisation à travers des points de suspension](012-concurrency.md#rcoro-locks)
* [CP.53 : Les paramètres des coroutines ne doivent pas être passés par référence](012-concurrency.md#rcoro-reference-parameters)

### <a name="rcoro-capture"></a>CP.51 : N'utilisez pas de lambdas capturant qui sont des coroutines

##### Raison

Les motifs d'utilisation qui sont corrects avec des lambdas normales sont dangereux avec des lambdas coroutines. Le motif évident de capturer des variables résultera en un accès à de la mémoire libérée après le premier point de suspension, même pour les pointeurs intelligents avec comptage de référence et les types copiables.

Une lambda résulte en un objet de fermeture avec un stockage, souvent sur la pile, qui sortira de portée à un moment donné. Lorsque l'objet de fermeture sort de portée, les captures sortiront aussi de portée. Les lambdas normales auront terminé leur exécution à ce moment-là, donc ce n'est pas un problème. Les lambdas coroutines peuvent reprendre depuis une suspension après que l'objet de fermeture a été détruit, et à ce point toutes les captures seront des accès mémoire après libération.

##### Exemple, mauvais

    int value = get_value();
    std::shared_ptr<Foo> sharedFoo = get_foo();
    {
      const auto lambda = [value, sharedFoo]() -> std::future<void>
      {
        co_await something();
        // "sharedFoo" et "value" ont déjà été détruits
        // le pointeur "shared" n'a rien accompli
      };
      lambda();
    } // l'objet de fermeture de la lambda est maintenant hors de portée

##### Exemple, meilleur

    int value = get_value();
    std::shared_ptr<Foo> sharedFoo = get_foo();
    {
      // prendre comme paramètre par valeur au lieu d'une capture
      const auto lambda = [](auto sharedFoo, auto value) -> std::future<void>
      {
        co_await something();
        // sharedFoo et value sont toujours valides à ce point
      };
      lambda(sharedFoo, value);
    } // l'objet de fermeture de la lambda est maintenant hors de portée

##### Exemple, optimal

Utilisez une fonction pour les coroutines.

    std::future<void> Class::do_something(int value, std::shared_ptr<Foo> sharedFoo)
    {
      co_await something();
      // sharedFoo et value sont toujours valides à ce point
    }

    void SomeOtherFunction()
    {
      int value = get_value();
      std::shared_ptr<Foo> sharedFoo = get_foo();
      do_something(value, sharedFoo);
    }

##### Application

Signaler une lambda qui est une coroutine et qui a une liste de captures non vide.


### <a name="rcoro-locks"></a>CP.52 : Ne tenez pas de verrous ou d'autres primitives de synchronisation à travers des points de suspension

##### Raison

Ce motif crée un risque significatif d'interblocage. Certains types d'attente autorisent le fil d'exécution courant à effectuer un travail supplémentaire jusqu'à ce que l'opération asynchrone soit terminée. Si le fil tenant le verrou effectue un travail qui nécessite le même verrou, il se produira un interblocage car il tente d'acquérir un verrou qu'il tient déjà.

Si la coroutine se termine sur un fil d'exécution différent de celui qui a acquis le verrou, alors c'est un comportement indéfini. Même avec un retour explicite au fil d'origine, une exception pourrait être lancée avant la reprise de la coroutine et le résultat sera que le garde de verrou ne sera pas détruit.

##### Exemple, mauvais

    std::mutex g_lock;

    std::future<void> Class::do_something()
    {
        std::lock_guard<std::mutex> guard(g_lock);
        co_await something(); // DANGER : la coroutine a suspendu l'exécution en tenant un verrou
        co_await somethingElse();
    }

##### Exemple, bon

    std::mutex g_lock;

    std::future<void> Class::do_something()
    {
        {
            std::lock_guard<std::mutex> guard(g_lock);
            // modifier les données protégées par le verrou
        }
        co_await something(); // OK : le verrou a été relâché avant la suspension de la coroutine
        co_await somethingElse();
    }


##### Remarque

Ce motif est également mauvais pour les performances. Lorsqu'un point de suspension est atteint, tel que co_await, l'exécution de la fonction actuelle s'arrête et d'autres codes commencent à s'exécuter. Il peut s'écouler une longue période avant que la coroutine ne reprenne. Pendant toute cette durée, le verrou sera tenu et ne pourra pas être acquis par d'autres fils d'exécution pour effectuer du travail.

##### Application

Signaler tous les gardes de verrou qui ne sont pas détruits avant qu'une coroutine ne se suspende.

### <a name="rcoro-reference-parameters"></a>CP.53 : Les paramètres des coroutines ne doivent pas être passés par référence

##### Raison

Une fois qu'une coroutine atteint le premier point de suspension, tel qu'un co_await, la partie synchrone retourne. Après ce point, tout paramètre passé par référence est pendentif. Tout usage au-delà est un comportement indéfini qui peut inclure l'écriture dans une mémoire libérée.

##### Exemple, mauvais

    std::future<int> Class::do_something(const std::shared_ptr<int>& input)
    {
        co_await something();

        // DANGER : la référence vers input n'est plus valide et peut être une mémoire libérée
        co_return *input + 1;
    }

##### Exemple, bon

    std::future<int> Class::do_something(std::shared_ptr<int> input)
    {
        co_await something();
        co_return *input + 1; // input est une copie qui est toujours valide ici
    }

##### Remarque

Ce problème ne s'applique pas aux paramètres par référence qui ne sont accédés qu'avant le premier point de suspension. Des modifications ultérieures de la fonction peuvent ajouter ou déplacer des points de suspension qui réintroduiraient cette classe de bug. Certains types de coroutines ont le point de suspension avant que la première ligne de code de la coroutine ne s'exécute, auquel cas les paramètres par référence sont toujours dangereux. Il est plus sûr de toujours passer par valeur car le paramètre copié vivra dans le cadre de la coroutine qui est sûr d'accéder tout au long de la coroutine.

##### Remarque

Le même danger s'applique aux paramètres de sortie. [F.20 : Pour les valeurs de sortie « out », préférez les valeurs de retour aux paramètres de sortie](006-functions.md#rf-out) décourage les paramètres de sortie. Les coroutines devraient les éviter entièrement. @TODO-LINK

##### Application

Signaler tous les paramètres par référence d'une coroutine.

## <a name="sscp-par"></a>CP.par : Parallélisme

Par « parallélisme », nous entendons l'exécution d'une tâche (plus ou moins) simultanément (« en parallèle avec ») sur de nombreux éléments de données.

Résumé des règles de parallélisme :

* ???
* ???
* Lorsque c'est approprié, préférez les algorithmes parallèles de la bibliothèque standard
* Utilisez des algorithmes conçus pour le parallélisme, pas des algorithmes avec une dépendance inutile à l'évaluation linéaire



## <a name="sscp-mess"></a>CP.mess : Passage de messages

Les fonctionnalités de la bibliothèque standard sont assez de bas niveau, axées sur les besoins de la programmation critique proche du matériel utilisant des `thread`, des `mutex`, des types `atomic`, etc.
La plupart des gens ne devraient pas travailler à ce niveau : c'est sujet aux erreurs et le développement est lent.
Si possible, utilisez une fonctionnalité de plus haut niveau : bibliothèques de messagerie, algorithmes parallèles, et vectorisation.
Cette section examine le passage de messages de sorte qu'un programmeur n'ait pas à faire de synchronisation explicite.

Résumé des règles de passage de messages :

* [CP.60 : Utilisez un `future` pour retourner une valeur depuis une tâche concurrente](012-concurrency.md#rconc-future)
* [CP.61 : Utilisez `async()` pour lancer des tâches concurrentes](012-concurrency.md#rconc-async)
* files de messages
* bibliothèques de messagerie

???? devrait-il y avoir un « utilisez X plutôt que `std::async` » où X est quelque chose qui utiliserait une pool de fils d'exécution mieux spécifiée ?

??? `std::async` vaut-il la peine d'être utilisé au vu des fonctionnalités de parallélisme futures (et même existantes, en tant que bibliothèques) ? Que devraient recommander les lignes directrices si quelqu'un veut paralléliser, par exemple, `std::accumulate` (avec la précondition supplémentaire de commutativité), ou le tri fusionnel ?


### <a name="rconc-future"></a>CP.60 : Utilisez un `future` pour retourner une valeur depuis une tâche concurrente

##### Raison

Un `future` préserve la sémantique habituelle de retour d'appel de fonction pour les tâches asynchrones.
Il n'y a pas de verrouillage explicite et à la fois le retour correct (valeur) et le retour d'erreur (exception) sont gérés simplement.

##### Exemple

    ???

##### Remarque

???

##### Application

???

### <a name="rconc-async"></a>CP.61 : Utilisez `async()` pour lancer des tâches concurrentes

##### Raison

Similaire à [R.12](009-resource.md#rr-immediate-alloc), qui vous dit d'éviter les pointeurs propriétaires nus, vous devriez
également éviter les fils d'exécution nus et les promesses nus lorsque c'est possible. Utilisez une fonction fabrique telle que `std::async`,
qui gère le lancement ou la réutilisation d'un fil d'exécution sans exposer de fils d'exécution nus à votre propre code. @TODO-LINK

##### Exemple

    int read_value(const std::string& filename)
    {
        std::ifstream in(filename);
        in.exceptions(std::ifstream::failbit);
        int value;
        in >> value;
        return value;
    }

    void async_example()
    {
        try {
            std::future<int> f1 = std::async(read_value, "v1.txt");
            std::future<int> f2 = std::async(read_value, "v2.txt");
            std::cout << f1.get() + f2.get() << '\n';
        } catch (const std::ios_base::failure& fail) {
            // gérer l'exception ici
        }
    }

##### Remarque

Malheureusement, `std::async` n'est pas parfait. Par exemple, il n'utilise pas de pool de fils d'exécution,
ce qui signifie qu'il pourrait échouer en raison d'une épuisement des ressources, plutôt que de mettre vos tâches en file
pour être exécutées plus tard. Cependant, même si vous ne pouvez pas utiliser `std::async`, vous devriez préférer
écrire votre propre fonction fabrique retournant un `future`, plutôt que d'utiliser des promesses nues.

##### Exemple (mauvais)

Cet exemple montre deux façons différentes de réussir à utiliser `std::future`, mais d'échouer
à éviter la gestion de `std::thread` nus.

    void async_example()
    {
        std::promise<int> p1;
        std::future<int> f1 = p1.get_future();
        std::thread t1([p1 = std::move(p1)]() mutable {
            p1.set_value(read_value("v1.txt"));
        });
        t1.detach(); // méchant

        std::packaged_task<int()> pt2(read_value, "v2.txt");
        std::future<int> f2 = pt2.get_future();
        std::thread(std::move(pt2)).detach();

        std::cout << f1.get() + f2.get() << '\n';
    }

##### Exemple (bon)

Cet exemple montre une façon dont vous pourriez suivre le motif général établi par
`std::async`, dans un contexte où `std::async` lui-même serait inacceptable pour
un usage en production.

    void async_example(WorkQueue& wq)
    {
        std::future<int> f1 = wq.enqueue([]() {
            return read_value("v1.txt");
        });
        std::future<int> f2 = wq.enqueue([]() {
            return read_value("v2.txt");
        });
        std::cout << f1.get() + f2.get() << '\n';
    }

Tous les fils d'exécution lancés pour exécuter le code de `read_value` sont cachés derrière
l'appel à `WorkQueue::enqueue`. Le code utilisateur ne traite que des objets `future`,
jamais des objets `thread`, `promise`, ou `packaged_task` nus.

##### Application

???


## <a name="sscp-vec"></a>CP.vec : Vectorisation

La vectorisation est une technique pour exécuter un certain nombre de tâches simultanément sans introduire de synchronisation explicite.
Une opération est simplement appliquée aux éléments d'une structure de données (un vecteur, un tableau, etc.) en parallèle.
La vectorisation a la propriété intéressante de souvent ne nécessiter aucune modification non locale d'un programme.
Cependant, la vectorisation fonctionne le mieux avec des structures de données simples et avec des algorithmes spécifiquement conçus pour l'activer.

Résumé des règles de vectorisation :

* ???
* ???

## <a name="sscp-free"></a>CP.free : Programmation sans verrou

La synchronisation à l'aide de `mutex` et de `condition_variable` peut être relativement coûteuse.
De plus, elle peut mener à l'interblocage.
Pour les performances et pour éliminer la possibilité d'interblocage, nous devons parfois utiliser les fonctionnalités de bas niveau « sans verrou » délicates
qui reposent sur l'obtention brève d'un accès exclusif (« atomique ») à la mémoire.
La programmation sans verrou est également utilisée pour implémenter des mécanismes de concurrence de plus haut niveau, tels que les `thread` et les `mutex`.

Résumé des règles de programmation sans verrou :

* [CP.100 : N'utilisez pas la programmation sans verrou à moins que vous n'en ayez absolument besoin](012-concurrency.md#rconc-lockfree)
* [CP.101 : Méfiez-vous de votre combinaison matériel/compilateur](012-concurrency.md#rconc-distrust)
* [CP.102 : Étudiez attentivement la littérature](012-concurrency.md#rconc-literature)
* comment/quand utiliser les atomiques
* éviter la famine
* utiliser une structure de données sans verrou plutôt que de créer un accès sans verrou spécifique à la main
* [CP.110 : N'écrivez pas votre propre double vérification de verrouillage pour l'initialisation](012-concurrency.md#rconc-double)
* [CP.111 : Utilisez un motif conventionnel si vous avez vraiment besoin de double vérification de verrouillage](012-concurrency.md#rconc-double-pattern)
* comment/quand comparer et échanger


### <a name="rconc-lockfree"></a>CP.100 : N'utilisez pas la programmation sans verrou à moins que vous n'en ayez absolument besoin

##### Raison

C'est sujet aux erreurs et nécessite des connaissances de niveau expert sur les fonctionnalités du langage, l'architecture de la machine, et les structures de données.

##### Exemple, mauvais

    extern atomic<Link*> head;        // la tête partagée d'une liste chaînée

    Link* nh = new Link(data, nullptr);    // créer un lien prêt à l'insertion
    Link* h = head.load();                 // lire la tête partagée de la liste

    do {
        if (h->data <= data) break;        // si oui, insérer ailleurs
        nh->next = h;                      // l'élément suivant est la tête précédente
    } while (!head.compare_exchange_weak(h, nh));    // écrire nh dans head ou dans h

Repérez le bug.
Ce serait vraiment difficile à trouver par les tests.
Lisez à propos du problème ABA.

##### Exception

Les [variables atomiques](#???) @TODO-LINK peuvent être utilisées simplement et en toute sécurité, tant que vous utilisez le modèle mémoire séquentiellement cohérent (memory_order_seq_cst), qui est le défaut.

##### Remarque

Les mécanismes de concurrence de plus haut niveau, tels que les `thread` et les `mutex`, sont implémentés à l'aide de la programmation sans verrou.

**Alternative** : Utilisez des structures de données sans verrou implémentées par d'autres dans le cadre d'une bibliothèque.


### <a name="rconc-distrust"></a>CP.101 : Méfiez-vous de votre combinaison matériel/compilateur

##### Raison

Les interfaces matérielles de bas niveau utilisées par la programmation sans verrou sont parmi les plus difficiles à bien implémenter et parmi
les domaines où les problèmes de portabilité les plus subtils se produisent.
Si vous faites de la programmation sans verrou pour les performances, vous devez vérifier les régressions.

##### Remarque

Le réordonnancement des instructions (statique et dynamique) rend difficile pour nous de penser efficacement à ce niveau (surtout si vous utilisez des modèles mémoire relâchés).
L'expérience, les modèles (semi)formels et la vérification par modèle peuvent être utiles.
Les tests - souvent à un degré extrême - sont essentiels.
« Ne volez pas trop près du soleil. »

##### Application

Avoir des règles strictes de re-test en place qui couvrent tout changement de matériel, système d'exploitation, compilateur, et bibliothèques.


### <a name="rconc-literature"></a>CP.102 : Étudiez attentivement la littérature

##### Raison

À l'exception des atomiques et de quelques autres motifs standard, la programmation sans verrou est vraiment un sujet réservé aux experts.
Devenez expert avant de livrer du code sans verrou pour que d'autres l'utilisent.

##### Références

* Anthony Williams : C++ Concurrency in Action. Manning Publications.
* Boehm, Adve, You Don't Know Jack About Shared Variables or Memory Models, Communications of the ACM, Feb 2012.
* Boehm, "Threads Basics", HPL TR 2009-259.
* Adve, Boehm, "Memory Models: A Case for Rethinking Parallel Languages and Hardware", Communications of the ACM, August 2010.
* Boehm, Adve, "Foundations of the C++ Concurrency Memory Model", PLDI 08.
* Mark Batty, Scott Owens, Susmit Sarkar, Peter Sewell, and Tjark Weber, "Mathematizing C++ Concurrency", POPL 2011.
* Damian Dechev, Peter Pirkelbauer, and Bjarne Stroustrup: Understanding and Effectively Preventing the ABA Problem in Descriptor-based Lock-free Designs. 13th IEEE Computer Society ISORC 2010 Symposium. May 2010.
* Damian Dechev and Bjarne Stroustrup: Scalable Non-blocking Concurrent Objects for Mission Critical Code. ACM OOPSLA'09. October 2009
* Damian Dechev, Peter Pirkelbauer, Nicolas Rouquette, and Bjarne Stroustrup: Semantically Enhanced Containers for Concurrent Real-Time Systems. Proc. 16th Annual IEEE International Conference and Workshop on the Engineering of Computer Based Systems (IEEE ECBS). April 2009.
* Maurice Herlihy, Nir Shavit, Victor Luchangco, Michael Spear, "The Art of Multiprocessor Programming", 2nd ed. September 2020

### <a name="rconc-double"></a>CP.110 : N'écrivez pas votre propre double vérification de verrouillage pour l'initialisation

##### Raison

Depuis C++11, les variables locales statiques sont initialisées de manière sûre pour les fils d'exécution. Combiné au motif RAII, les variables locales statiques peuvent remplacer le besoin d'écrire votre propre double vérification de verrouillage pour l'initialisation. std::call_once peut également atteindre le même objectif. Utilisez soit les variables locales statiques de C++11 soit std::call_once au lieu d'écrire votre propre double vérification de verrouillage pour l'initialisation.

##### Exemple

Exemple avec std::call_once.

    void f()
    {
        static std::once_flag my_once_flag;
        std::call_once(my_once_flag, []()
        {
            // faire ceci une seule fois
        });
        // ...
    }

Exemple avec les variables locales statiques sûres pour les fils d'exécution de C++11.

    void f()
    {
        // En supposant que le compilateur est conforme à C++11
        static My_class my_object; // Constructeur appelé une seule fois
        // ...
    }

    class My_class
    {
    public:
        My_class()
        {
            // faire ceci une seule fois
        }
    };

##### Application

??? Est-il possible de détecter le motif ?


### <a name="rconc-double-pattern"></a>CP.111 : Utilisez un motif conventionnel si vous avez vraiment besoin de double vérification de verrouillage

##### Raison

La double vérification de verrouillage est facile à mal faire. Si vous avez vraiment besoin d'écrire votre propre double vérification de verrouillage, malgré les règles [CP.110 : N'écrivez pas votre propre double vérification de verrouillage pour l'initialisation](012-concurrency.md#rconc-double) et [CP.100 : N'utilisez pas la programmation sans verrou à moins que vous n'en ayez absolument besoin](012-concurrency.md#rconc-lockfree), alors faites-le avec un motif conventionnel.

Les utilisations du motif de double vérification de verrouillage qui ne violent pas [CP.110 : N'écrivez pas votre propre double vérification de verrouillage pour l'initialisation](012-concurrency.md#rconc-double) surviennent lorsqu'une action non sûre pour les fils d'exécution est à la fois difficile et rare, et qu'il existe un test rapide sûr pour les fils d'exécution qui peut être utilisé pour garantir que l'action n'est pas nécessaire, mais qui ne peut pas être utilisé pour garantir le contraire.

##### Exemple, mauvais

L'utilisation de volatile ne rend pas la première vérification sûre pour les fils d'exécution, voir aussi [CP.200 : Utilisez `volatile` uniquement pour parler à une mémoire non-C++](012-concurrency.md#rconc-volatile2)

    mutex action_mutex;
    volatile bool action_needed;

    if (action_needed) {
        std::lock_guard<std::mutex> lock(action_mutex);
        if (action_needed) {
            take_action();
            action_needed = false;
        }
    }

##### Exemple, bon

    mutex action_mutex;
    atomic<bool> action_needed;

    if (action_needed) {
        std::lock_guard<std::mutex> lock(action_mutex);
        if (action_needed) {
            take_action();
            action_needed = false;
        }
    }

Un ordre mémoire affiné pourrait être bénéfique là où une lecture d'acquisition est plus efficace qu'une lecture séquentiellement cohérente

    mutex action_mutex;
    atomic<bool> action_needed;

    if (action_needed.load(memory_order_acquire)) {
        lock_guard<std::mutex> lock(action_mutex);
        if (action_needed.load(memory_order_relaxed)) {
            take_action();
            action_needed.store(false, memory_order_release);
        }
    }

##### Application

??? Est-il possible de détecter le motif ?


## <a name="sscp-etc"></a>CP.etc : Autres règles de concurrence

Ces règles défient une catégorisation simple :

* [CP.200 : Utilisez `volatile` uniquement pour parler à une mémoire non-C++](012-concurrency.md#rconc-volatile2)
* [CP.201 : ??? Signaux](012-concurrency.md#rconc-signal)

### <a name="rconc-volatile2"></a>CP.200 : Utilisez `volatile` uniquement pour parler à une mémoire non-C++

##### Raison

`volatile` est utilisé pour référencer des objets partagés avec du code « non-C++ » ou du matériel qui ne suit pas le modèle mémoire C++.

##### Exemple

    const volatile long clock;

Cela décrit un registre constamment mis à jour par un circuit horloge.
`clock` est `volatile` car sa valeur changera sans aucune action de la part du programme C++ qui l'utilise.
Par exemple, lire `clock` deux fois donnera souvent deux valeurs différentes, donc l'optimiseur ne devrait pas optimiser la seconde lecture dans ce code :

    long t1 = clock;
    // ... pas d'utilisation de clock ici ...
    long t2 = clock;

`clock` est `const` car le programme ne devrait pas essayer d'écrire dans `clock`.

##### Remarque

À moins que vous ne rédigiez le code de plus bas niveau manipulant directement le matériel, considérez `volatile` comme une fonctionnalité ésotérique qu'il vaut mieux éviter.

##### Exemple

Généralement, le code C++ reçoit de la mémoire `volatile` qui est possédée ailleurs (matériel ou un autre langage) :

    int volatile* vi = get_hardware_memory_location();
        // note : nous obtenons un pointeur vers la mémoire de quelqu'un d'autre ici
        // volatile dit « traitez ceci avec un respect supplémentaire »

Parfois, le code C++ alloue la mémoire `volatile` et la partage avec « ailleurs » (matériel ou un autre langage) en échappant délibérément un pointeur :

    static volatile long vl;
    please_use_this(&vl);   // échapper une référence à ceci vers « ailleurs » (non-C++)

##### Exemple, mauvais

Les variables locales `volatile` sont presque toujours incorrectes -- comment pourraient-elles être partagées avec d'autres langages ou du matériel si elles sont éphémères ?
La même chose s'applique presque aussi fortement aux membres de données, pour la même raison.

    void f()
    {
        volatile int i = 0; // Mauvais, variable locale volatile
        // etc.
    }

    class My_type {
        volatile int i = 0; // Suspect, membre de données volatile
        // etc.
    };

##### Remarque

En C++, contrairement à d'autres langages, `volatile` n'a [rien à voir avec la synchronisation](012-concurrency.md#rconc-volatile).

##### Application

* Signaler les membres locaux et de données `volatile T` ; vous avez presque certainement voulu utiliser `atomic<T>` à la place.
* ???

### <a name="rconc-signal"></a>CP.201 : ??? Signaux

???Gestion des signaux UNIX???. Il pourrait être utile de rappeler à quel point peu de fonctions sont sûres pour les signaux asynchrones, et comment communiquer avec un gestionnaire de signaux (le mieux est probablement « pas du tout »)
