# <a name="s-concurrency"></a>CP : Concurrence et parallélisme

Nous voulons souvent que nos ordinateurs accomplissent plusieurs tâches en même temps (ou du moins donnent l’impression de le faire).  
Les raisons de le faire varient (par exemple, attendre de nombreux événements en n’utilisant qu’un seul processeur, traiter simultanément de nombreux flux de données, ou exploiter de nombreuses ressources matérielles) tout comme les mécanismes de base permettant d’exprimer la concurrence et le parallélisme.  
Dans cette section, nous énonçons les principes et les règles d’utilisation des fonctionnalités du C++ standard ISO pour exprimer la concurrence et le parallélisme de base.

Les **threads** constituent le socle au niveau machine de la programmation concurrente et parallèle.  
Les threads permettent d’exécuter plusieurs sections d’un programme indépendamment, tout en partageant la même mémoire. La programmation concurrente est délicate, car protéger les données partagées entre threads est plus facile à dire qu’à faire.  

Faire exécuter du code initialement mono‑threadé de façon concurrente peut être aussi trivial que d’ajouter stratégiquement `std::async` ou `std::thread`, ou bien nécessiter une réécriture complète, selon que le code d’origine a été écrit ou non de façon « thread‑friendly ».

Les règles de concurrence/parallélisme de ce document sont conçues avec trois objectifs :

* Aider à écrire du code apte à être utilisé dans un environnement multithread.
* Montrer des manières propres et sûres d’utiliser les primitives de threading offertes par la bibliothèque standard.
* Proposer des orientations sur ce qu’il faut faire quand la concurrence et le parallélisme ne procurent pas les gains de performance attendus.

Il est également important de noter que la concurrence en C++ est une histoire inachevée. C++11 a introduit de nombreuses primitives de concurrence de base, C++14 et C++17 les ont améliorées, et l’intérêt est grand pour rendre l’écriture de programmes concurrents en C++ encore plus facile. Nous nous attendons à ce que certaines des recommandations relatives aux bibliothèques évoluent de façon significative avec le temps.

Cette section nécessite encore beaucoup de travail (évidemment).  
Veuillez noter que nous commençons par des règles destinées à des non‑experts relatifs. Les vrais experts devront attendre un peu ; les contributions sont les bienvenues, mais merci de penser à la majorité des programmeurs qui ont du mal à rendre leurs programmes concurrents corrects et performants.

## Résumé des règles de concurrence et parallélisme

* [CP.1 : Supposer que votre code s’exécutera dans le cadre d’un programme multithread](012-concurrency.md#rconc-multi)
* [CP.2 : Éviter les data races](012-concurrency.md#rconc-races)
* [CP.3 : Réduire le partage explicite de données modifiables](012-concurrency.md#rconc-data)
* [CP.4 : Penser en termes de tâches, plutôt qu’en termes de threads](012-concurrency.md#rconc-task)
* [CP.8 : Ne pas essayer d’utiliser `volatile` pour la synchronisation](012-concurrency.md#rconc-volatile)
* [CP.9 : Utiliser des outils de validation du code concurrent chaque fois que possible](012-concurrency.md#rconc-tools)

**Voir également** :

* [CP.con : Concurrence](012-concurrency.md#sscp-con)
* [CP.coro : Coroutines](012-concurrency.md#sscp-coro)
* [CP.par : Parallélisme](012-concurrency.md#sscp-par)
* [CP.mess : Passage de messages](012-concurrency.md#sscp-mess)
* [CP.vec : Vectorisation](012-concurrency.md#sscp-vec)
* [CP.free : Programmation lock‑free](012-concurrency.md#sscp-free)
* [CP.etc : Autres règles de concurrence](012-concurrency.md#sscp-etc)

---

### <a name="rconc-multi"></a>CP.1 : Supposer que votre code s’exécutera dans le cadre d’un programme multithread

##### Raison

Il est difficile d’être certain que la concurrence n’est pas utilisée maintenant ou ne le sera pas dans le futur.  
Le code est réutilisé.  
Les bibliothèques qui n’utilisent pas de threads peuvent être appelées depuis une autre partie d’un programme qui, elle, utilise des threads.  
Notez que cette règle s’applique surtout au code de bibliothèque et le moins aux applications autonomes.  
Cependant, avec le temps, des fragments de code peuvent apparaître à des endroits inattendus.

##### Exemple, mauvais

    double cached_computation(int x)
    {
        // mauvais : ces variables statiques provoquent des data races en usage multithread
        static int cached_x = 0.0;
        static double cached_result = COMPUTATION_OF_ZERO;

        if (cached_x != x) {
            cached_x = x;
            cached_result = computation(x);
        }
        return cached_result;
    }

Bien que `cached_computation` fonctionne parfaitement dans un environnement mono‑thread, en multithread les deux variables `static` entraînent des data races et donc un comportement indéfini.

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

Ici le cache est stocké comme donnée membre d’un objet `ComputationCache`, plutôt que comme état statique partagé. Cette refactorisation délègue essentiellement la responsabilité au niveau appelant : un programme mono‑thread pourra toujours choisir un `ComputationCache` global, tandis qu’un programme multithread pourra créer une instance de `ComputationCache` par thread, ou par « contexte » selon la définition du terme.  
La fonction refactorisée ne tente plus de gérer l’allocation de `cached_x`. En ce sens, il s’agit d’une application du principe de responsabilité unique.

Dans cet exemple précis, le refactoring pour la sûreté vis‑à‑vis des threads a également amélioré la réutilisabilité en mono‑thread. Il n’est pas difficile d’imaginer qu’un programme mono‑thread souhaitera deux instances de `ComputationCache` pour les utiliser dans des parties différentes du programme, sans qu’elles n’écrasent les données mises en cache les unes des autres.

Il existe plusieurs autres moyens d’ajouter la sûreté vis‑à‑vis des threads à du code écrit pour un environnement multithread standard (c’est‑à‑dire où la seule forme de concurrence est `std::thread`) :

* Marquer les variables d’état comme `thread_local` au lieu de `static`.
* Mettre en place un contrôle de concurrence, par exemple en protégeant l’accès aux deux variables `static` avec un `static std::mutex`.
* Refuser de compiler et/ou d’exécuter en environnement multithread.
* Fournir deux implémentations : une pour les environnements mono‑thread et une autre pour les environnements multithread.

##### Exception

Code jamais exécuté dans un environnement multithread.

Soyez vigilant : de nombreux exemples montrent que du code « connu » pour ne jamais être exécuté dans un programme multithread se retrouve finalement exécuté dans un tel programme, souvent plusieurs années plus tard.  
Typiquement, ces programmes entraînent un effort pénible de suppression des data races.  
Par conséquent, le code qui n’est jamais censé être exécuté dans un environnement multithread doit être clairement indiqué comme tel et, idéalement, être accompagné de mécanismes d’enforcement à la compilation ou à l’exécution pour détecter ces usages erronés tôt.

### <a name="rconc-races"></a>CP.2 : Éviter les data races

##### Raison

À moins d’y faire attention, rien n’est garanti de fonctionner et des erreurs subtiles persisteront.

##### Note

En bref, si deux threads peuvent accéder simultanément au même objet (sans synchronisation), et qu’au moins l’un des deux effectue une écriture (opération non‑`const`), vous avez une data race.  
Pour plus d’informations sur la façon de bien utiliser la synchronisation afin d’éliminer les data races, consultez un bon livre sur la concurrence (voir [Étudier attentivement la littérature](012-concurrency.md#rconc-literature)).

##### Exemple, mauvais

Il existe de nombreux exemples de data races qui existent, certains fonctionnant même dans des logiciels de production à l’instant même. Un exemple très simple :

    int get_id()
    {
        static int id = 1;
        return id++;
    }

L’incrémentation ici constitue une data race. Cela peut échouer de plusieurs manières, notamment :

* Le thread A lit la valeur de `id`, le système d’exploitation bascule le thread A pendant un certain temps, et d’autres threads créent des centaines d’identifiants. Le thread A reprend alors son exécution et écrit `id` avec la valeur lue plus un.
* Les threads A et B lisent `id` et l’incrémentent simultanément. Ils obtiennent le même identifiant.

Les variables `static` locales sont une source fréquente de data races.

##### Exemple, mauvais

    void f(fstream& fs, regex pattern)
    {
        array<double, max> buf;
        int sz = read_vec(fs, buf, max);            // lire depuis fs dans buf
        gsl::span<double> s {buf};
        // ...
        auto h1 = async([&] { sort(std::execution::par, s); });     // créer une tâche pour trier
        // ...
        auto h2 = async([&] { return find_all(buf, sz, pattern); }); // créer une tâche pour rechercher les correspondances
        // ...
    }

Ici nous avons une (laide) data race sur les éléments de `buf` (`sort` lit et écrit).  
Toutes les data races sont mauvaises. Dans cet exemple, nous avons obtenu une data race sur des données de la pile. Toutes les data races ne sont pas aussi faciles à repérer que celle‑ci.

##### Exemple, mauvais

    // code non protégé par un verrou

    unsigned val;

    if (val < 5) {
        // ... un autre thread peut changer val ici ...
        switch (val) {
        case 0: // ...
        case 1: // ...
        case 2: // ...
        case 3: // ...
        case 4: // ...
        }
    }

Un compilateur qui ne sait pas que `val` peut changer implémentera très probablement ce `switch` en utilisant une table de sauts à cinq entrées.  
Ensuite, une valeur de `val` hors de l’intervalle `[0..4]` provoquera un saut vers une adresse qui pourrait être n’importe où dans le programme, et l’exécution se poursuivra là‑bas.  
En réalité, « tout est incertain » si vous avez une data race.  
Cela peut même être pire : en examinant le code généré, il est parfois possible de déterminer où le saut erroné ira pour une valeur donnée ; cela constitue un risque de sécurité.

##### Application

Faire au moins quelque chose.  
Il existe des outils commerciaux et open‑source qui tentent de résoudre ce problème, mais il faut être conscient que les solutions ont des coûts et des angles morts.  
Les outils statiques produisent souvent de nombreux faux positifs et les outils dynamiques entraînent généralement un coût important. Nous espérons de meilleurs outils.  
L’utilisation de plusieurs outils peut détecter plus de problèmes qu’un seul.

D’autres moyens de limiter la probabilité de data races :

* Éviter les données globales.
* Éviter les variables `static`.
* Utiliser davantage de types concrets sur la pile (et ne pas trop passer de pointeurs).
* Utiliser davantage de données immuables (littéraux, `constexpr` et `const`).

### <a name="rconc-data"></a>CP.3 : Réduire le partage explicite de données modifiables

##### Raison

Si vous ne partagez pas de données modifiables, vous ne pouvez pas avoir de data race.  
Moins vous partagez, moins vous avez de chances d’oublier de synchroniser l’accès (et donc d’obtenir des data races).  
Moins vous partagez, moins vous avez de chances d’attendre un verrou (et donc les performances peuvent s’améliorer).

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

Sans ces `const`, nous aurions dû examiner chaque fonction invoquée de façon asynchrone pour détecter d’éventuelles data races sur `surface_readings`.  
Faire de `surface_readings` un `const` (par rapport à cette fonction) permet de raisonner uniquement à partir du corps de la fonction.

##### Note

Les données immuables peuvent être partagées de façon sûre et efficace. Aucun verrou n’est nécessaire : on ne peut pas avoir de data race sur une constante.  
Voir aussi [CP.mess : Passage de messages](012-concurrency.md#sscp-mess) et [CP.31 : préférer le passage par valeur](012-concurrency.md#rconc-data-by-value).

##### Application

???


### <a name="rconc-task"></a>CP.4 : Penser en termes de tâches, plutôt qu’en termes de threads

##### Raison

Un `thread` est un concept d’implémentation, une manière de visualiser la machine.  
Une tâche est une notion d’application, quelque chose que vous voulez faire, de préférence en même temps que d’autres tâches.  
Les concepts d’application sont plus faciles à raisonner.

##### Exemple

    void some_fun(const std::string& msg)
    {
        std::thread publisher([=] { std::cout << msg; });      // mauvais : moins expressif
                                                               //      et plus sujet aux erreurs
        auto pubtask = std::async([=] { std::cout << msg; });  // correct
        // ...
        publisher.join();
    }

##### Note

À l’exception de `async()`, les fonctionnalités de la bibliothèque standard sont de bas niveau, orientées machine, threads‑et‑verrou.  
C’est une base nécessaire, mais nous devons essayer d’élever le niveau d’abstraction : pour la productivité, la fiabilité et la performance.  
C’est un argument solide en faveur de l’utilisation de bibliothèques de plus haut niveau, davantage orientées application (si possible, construites sur les fonctionnalités de la bibliothèque standard).

##### Application

???

### <a name="rconc-volatile"></a>CP.8 : Ne pas essayer d’utiliser `volatile` pour la synchronisation

##### Raison

En C++, contrairement à d’autres langages, `volatile` ne fournit ni atomicité, ni synchronisation entre threads, ni prévention du réordonnancement d’instructions (ni du compilateur ni du matériel).  
Il n’a tout simplement rien à voir avec la concurrence.

##### Exemple, mauvais

    int free_slots = max_slots; // source actuelle de mémoire pour les objets

    Pool* use()
    {
        if (int n = free_slots--) return &pool[n];
    }

Ici nous avons un problème : ce code fonctionne parfaitement en mono‑thread, mais si deux threads l’exécutent il y a une condition de course sur `free_slots` de sorte que deux threads peuvent obtenir la même valeur et le même `free_slots`. C’est (évidemment) une mauvaise data race, donc les programmeurs habitués à d’autres langages pourraient essayer de la corriger ainsi :

    volatile int free_slots = max_slots; // source actuelle de mémoire pour les objets

    Pool* use()
    {
        if (int n = free_slots--) return &pool[n];
    }

Cela n’a aucun effet sur la synchronisation : la data race persiste !

Le mécanisme C++ approprié est le type `atomic` :

    atomic<int> free_slots = max_slots; // source actuelle de mémoire pour les objets

    Pool* use()
    {
        if (int n = free_slots--) return &pool[n];
    }

Désormais, l’opération `--` est atomique, plutôt qu’une séquence lecture‑incrément‑écriture où un autre thread pourrait intervenir entre les opérations individuelles.

##### Alternative

Utiliser les types `atomic` là où vous auriez employé `volatile` dans un autre langage.  
Utiliser un `mutex` pour les exemples plus compliqués.

##### Voir aussi

[(rare) usages corrects de `volatile`](012-concurrency.md#rconc-volatile2)

### <a name="rconc-tools"></a>CP.9 : Utiliser des outils de validation du code concurrent chaque fois que possible

L’expérience montre que le code concurrent est exceptionnellement difficile à rendre correct et que les vérifications à la compilation, les contrôles à l’exécution et les tests sont moins efficaces pour détecter les erreurs de concurrence que pour les erreurs de code séquentiel.  
Des erreurs subtiles de concurrence peuvent avoir des effets dramatiquement néfastes, incluant corruption de mémoire, blocages (deadlocks) et vulnérabilités de sécurité.

##### Exemple

    ???

##### Note

La sûreté vis‑à‑vis des threads est un défi, souvent supérieur à celui des programmeurs expérimentés : les outils sont une stratégie importante pour atténuer ces risques.  
Il existe de nombreux outils, tant commerciaux qu’open‑source, tant de recherche que de production.  
Malheureusement, les besoins et contraintes des gens diffèrent tellement que nous ne pouvons pas faire de recommandations précises, mais nous pouvons mentionner :

* Outils d’enforcement statique : tant [clang](https://clang.llvm.org/docs/ThreadSafetyAnalysis.html) que certaines versions anciennes de [GCC](https://gcc.gnu.org/wiki/ThreadSafetyAnnotation) offrent un support d’annotations de sûreté des threads. L’usage cohérent de cette technique transforme de nombreuses classes d’erreurs de sûreté des threads en erreurs à la compilation. Les annotations sont généralement locales (marquant un membre de donnée particulier comme protégé par un mutex donné) et sont habituellement faciles à apprendre. Cependant, comme beaucoup d’outils statiques, ils peuvent produire de nombreux faux négatifs ; des cas qui auraient dû être attrapés sont autorisés.

* Outils d’enforcement dynamique : le Thread Sanitizer de Clang (TSAN) est un exemple puissant d’outil dynamique : il modifie la construction et l’exécution de votre programme pour ajouter du suivi d’accès à la mémoire, identifiant absolument les data races lors d’une exécution donnée de votre binaire.  
Le coût est à la fois une utilisation mémoire (5‑10 × la normale) et une décélération CPU (2‑20 ×).  
Les outils dynamiques comme celui‑ci sont meilleurs lorsqu’ils sont appliqués aux tests d’intégration, aux déploiements canary ou aux tests unitaires fonctionnant avec plusieurs threads.  
La charge de travail compte : lorsqu’un TSAN identifie un problème, il s’agit toujours d’une vraie data race, mais il ne peut identifier que les races observées lors d’une exécution donnée.

##### Application

Il revient au concepteur d’application de choisir quels outils de support sont utiles pour une application donnée.

## <a name="sscp-con"></a>CP.con : Concurrence

Cette section se concentre sur les usages plutôt ad‑hoc de plusieurs threads communiquant via des données partagées.

* Pour les algorithmes parallèles, voir [parallélisme](012-concurrency.md#sscp-par)
* Pour la communication inter‑tâches sans partage explicite, voir [messagerie](012-concurrency.md#sscp-mess)
* Pour le code vectoriel parallèle, voir [vectorisation](012-concurrency.md#sscp-vec)
* Pour la programmation lock‑free, voir [lock‑free](012-concurrency.md#sscp-free)

### Résumé des règles de concurrence

* [CP.20 : Utiliser le RAII, jamais `lock()`/`unlock()` simples](012-concurrency.md#rconc-raii)
* [CP.21 : Utiliser `std::lock()` ou `std::scoped_lock` pour acquérir plusieurs `mutex`](012-concurrency.md#rconc-lock)
* [CP.22 : Ne jamais appeler du code inconnu pendant qu’un verrou est détenu (ex. : un rappel)](012-concurrency.md#rconc-unknown)
* [CP.23 : Considérer un `thread` joint comme un conteneur à portée limitée](012-concurrency.md#rconc-join)
* [CP.24 : Considérer un `thread` comme un conteneur global](012-concurrency.md#rconc-detach)
* [CP.25 : Privilégier `gsl::joining_thread` à `std::thread`](012-concurrency.md#rconc-joining_thread)
* [CP.26 : Ne pas `detach()` un thread](012-concurrency.md#rconc-detached_thread)
* [CP.31 : Passer de petites quantités de données entre threads par valeur, plutôt que par référence ou pointeur](012-concurrency.md#rconc-data-by-value)
* [CP.32 : Pour partager la possession entre des `thread`s non liés, utiliser `shared_ptr`](012-concurrency.md#rconc-shared)
* [CP.40 : Minimiser les changements de contexte](012-concurrency.md#rconc-switch)
* [CP.41 : Minimiser la création et la destruction de threads](012-concurrency.md#rconc-create)
* [CP.42 : Ne pas `wait` sans condition](012-concurrency.md#rconc-wait)
* [CP.43 : Minimiser le temps passé dans une section critique](012-concurrency.md#rconc-time)
* [CP.44 : Se souvenir de nommer ses `lock_guard`s et `unique_lock`s](012-concurrency.md#rconc-name)
* [CP.50 : Définir un `mutex` avec les données qu’il protège. Utiliser `synchronized_value<T>` quand c’est possible](012-concurrency.md#rconc-mutex)
* ??? quand utiliser un spin‑lock
* ??? quand utiliser `try_lock()`
* ??? quand préférer `lock_guard` à `unique_lock`
* ??? multiplexage temporel
* ??? comment/ quand utiliser `new thread`

### <a name="rconc-raii"></a>CP.20 : Utiliser le RAII, jamais `lock()`/`unlock()` simples

##### Raison

Évite les erreurs désagréables dues à des verrous non libérés.

##### Exemple, mauvais

    mutex mtx;

    void do_stuff()
    {
        mtx.lock();
        // ... faire des choses ...
        mtx.unlock();
    }

Tôt ou tard, quelqu’un oubliera le `mtx.unlock()`, introduira un `return` dans les « … faire des choses … », lèvera une exception, ou autre.

    mutex mtx;

    void do_stuff()
    {
        unique_lock<mutex> lck {mtx};
        // ... faire des choses ...
    }

##### Application

Détecter les appels aux membres `lock()` et `unlock()`.  ???


### <a name="rconc-lock"></a>CP.21 : Utiliser `std::lock()` ou `std::scoped_lock` pour acquérir plusieurs `mutex`

##### Raison

Éviter les interblocages (deadlocks) lorsqu’on acquiert plusieurs `mutex`.

##### Exemple

Voici une situation propice au deadlock :

    // thread 1
    lock_guard<mutex> lck1(m1);
    lock_guard<mutex> lck2(m2);

    // thread 2
    lock_guard<mutex> lck2(m2);
    lock_guard<mutex> lck1(m1);

Utilisez plutôt `lock()` :

    // thread 1
    lock(m1, m2);
    lock_guard<mutex> lck1(m1, adopt_lock);
    lock_guard<mutex> lck2(m2, adopt_lock);

    // thread 2
    lock(m2, m1);
    lock_guard<mutex> lck2(m2, adopt_lock);
    lock_guard<mutex> lck1(m1, adopt_lock);

ou (mieux, mais C++17 uniquement) :

    // thread 1
    scoped_lock<mutex, mutex> lck1(m1, m2);

    // thread 2
    scoped_lock<mutex, mutex> lck2(m2, m1);

Ici, les créateurs de `thread1` et `thread2` ne s’accordent toujours pas sur l’ordre des `mutex`, mais l’ordre n’a plus d’importance.

##### Note

Dans le code réel, les `mutex` sont rarement nommés de façon à rappeler commodément une relation ou un ordre d’acquisition prévu.  
Dans le code réel, les `mutex` ne sont pas toujours acquis consécutivement sur des lignes séparées.

##### Note

En C++17 il est possible d’écrire simplement

    lock_guard lck1(m1, adopt_lock);

et laisser le type du `mutex` être déduit.

##### Application

Détecter l’acquisition de plusieurs `mutex`.  
C’est indécidable en général, mais intercepter les exemples simples et courants (comme celui ci‑dessus) est aisé.

### <a name="rconc-unknown"></a>CP.22 : Ne jamais appeler du code inconnu pendant qu’un verrou est détenu (ex. : un rappel)

##### Raison

Si vous ne savez pas ce que fait un morceau de code, vous risquez un interblocage.

##### Exemple

    void do_this(Foo* p)
    {
        lock_guard<mutex> lck {my_mutex};
        // ... faire quelque chose ...
        p->act(my_data);
        // ...
    }

Si vous ne savez pas ce que `Foo::act` fait (peut‑être une fonction virtuelle appelant un membre d’une classe dérivée qui n’est pas encore écrite), il se peut qu’il rappelle `do_this` (récursivement) et cause un deadlock sur `my_mutex`.  
Il pourrait aussi verrouiller un autre mutex et ne pas revenir dans un délai raisonnable, retardant ainsi tout code appelant `do_this`.

##### Exemple

Un exemple classique du problème « appel de code inconnu » est l’appel d’une fonction qui tente d’obtenir un verrou sur le même objet. Ce problème peut souvent être résolu en utilisant un `recursive_mutex`. Par exemple :

    recursive_mutex my_mutex;

    template<typename Action>
    void do_something(Action f)
    {
        unique_lock<recursive_mutex> lck {my_mutex};
        // ... faire quelque chose ...
        f(this);    // f fera quelque chose sur *this
        // ...
    }

Si, comme c’est probable, `f()` invoque des opérations sur `*this`, il faut s’assurer que l’invariant de l’objet est respecté avant l’appel.

##### Application

* Signaler l’appel d’une fonction virtuelle avec un `mutex` non récursif détenu
* Signaler l’appel d’un rappel avec un `mutex` non récursif détenu


### <a name="rconc-join"></a>CP.23 : Considérer un `thread` joint comme un conteneur à portée limitée

##### Raison

Pour maintenir la sécurité des pointeurs et éviter les fuites, il faut réfléchir aux pointeurs utilisés par un `thread`.  
Si un `thread` rejoint (join), on peut passer en toute sécurité des pointeurs à des objets qui restent en portée pendant la durée de vie du `thread` et de ses scopes englobants.

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

Un `gsl::joining_thread` est un `std::thread` dont le destructeur effectue le `join` et qui ne peut pas être `detach()`é.  
Par « OK » nous entendons que l’objet restera « en vie » tant que le `thread` pourra l’utiliser. Le fait que les `thread`s s’exécutent de façon concurrente n’affecte pas les questions de durée de vie ou de possession ; ces `thread`s peuvent être vus simplement comme des objets fonctionnels appelés depuis `some_fct`.

##### Application

Assurer que les `joining_thread`s ne soient pas `detach()`és.  
Ensuite, les règles habituelles de durée de vie et de possession (pour les objets locaux) s’appliquent.

### <a name="rconc-detach"></a>CP.24 : Considérer un `thread` comme un conteneur global

##### Raison

Pour maintenir la sécurité des pointeurs et éviter les fuites, il faut réfléchir aux pointeurs utilisés par un `thread`.  
Si un `thread` est détaché (`detach()`), on ne peut passer en toute sécurité que des pointeurs vers des objets au stockage statique ou libre.

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
        std::thread t0(f, &x);           // mauvais
        std::thread t1(f, p);            // mauvais
        std::thread t2(f, &glob);        // OK
        auto q = make_unique<int>(99);
        std::thread t3(f, q.get());      // mauvais
        // ...
        t0.detach();
        t1.detach();
        t2.detach();
        t3.detach();
        // ...
    }

Par « OK », nous entendons que l’objet restera « en vie » tant que le `thread` peut utiliser le pointeur. Par « mauvais », nous voulons dire qu’un `thread` pourrait accéder à un pointeur après la destruction de l’objet pointé. Le fait que les `thread`s s’exécutent simultanément n’affecte pas les problèmes de durée de vie ou de possession ; ces `thread`s peuvent être vus simplement comme des objets fonctionnels appelés depuis `some_fct`.

##### Note

Même les objets avec durée de stockage statique peuvent poser problème lorsqu’ils sont utilisés depuis des threads détachés : si le thread continue jusqu’à la fin du programme, il peut s’exécuter en même temps que la destruction de ces objets, et les accès peuvent provoquer des races.

##### Note

Cette règle est redondante si vous [ne `detach()`z pas](012-concurrency.md#rconc-detached_thread) et [utilisez `gsl::joining_thread`](012-concurrency.md#rconc-joining_thread). Cependant, convertir du code existant pour suivre ces indications peut être difficile voire impossible pour des bibliothèques tierces. Dans ces cas, la règle devient indispensable pour la sûreté de la durée de vie et du typage.

En général, il est indécidable de savoir si un `detach()` est exécuté pour un `thread`, mais les cas simples courants sont facilement détectables.  
Si nous ne pouvons pas prouver qu’un `thread` ne `detach()` pas, nous devons supposer qu’il le fait et qu’il survit au scope où il a été créé ; les règles habituelles de durée de vie et de possession (pour les objets globaux) s’appliquent alors.

##### Application

Signaler les tentatives de passage de variables locales à un `thread` qui pourrait `detach()`.

### <a name="rconc-joining_thread"></a>CP.25 : Privilégier `gsl::joining_thread` à `std::thread`

##### Raison

Un `joining_thread` est un thread qui se joint (`join`) à la fin de son scope.  
Les threads détachés sont difficiles à surveiller. Il est plus difficile d’assurer qu’ils se terminent correctement (et potentiellement de les surveiller).

##### Exemple, mauvais

    void f() { std::cout << "Hello "; }

    struct F {
        void operator()() const { std::cout << "parallel world "; }
    };

    int main()
    {
        std::thread t1{f};      // f() s’exécute dans un thread séparé
        std::thread t2{F()};    // F()() s’exécute dans un thread séparé
    }  // repérer les bugs

##### Exemple

    void f() { std::cout << "Hello "; }

    struct F {
        void operator()() const { std::cout << "parallel world "; }
    };

    int main()
    {
        std::thread t1{f};      // f() s’exécute dans un thread séparé
        std::thread t2{F()};    // F()() s’exécute dans un thread séparé

        t1.join();
        t2.join();
    }  // il reste un bug grave

##### Note

Faire des « threads immortels » globaux, les placer dans un scope englobant, ou les mettre sur le tas plutôt que de les `detach()`er.  
[Ne pas `detach`](012-concurrency.md#rconc-detached_thread).

##### Note

À cause du code ancien et des bibliothèques tierces qui utilisent `std::thread`, cette règle peut être difficile à introduire.

##### Application

Signaler les utilisations de `std::thread` :

* Suggérer l’usage de `gsl::joining_thread` ou de `std::jthread` (C++20).
* Suggérer « exporter la possession » (voir [ne pas `detach`](012-concurrency.md#rconc-detached_thread)) vers un scope englobant si le thread est détaché.
* Avertir si l’on ne peut pas déterminer clairement si le thread rejoint ou se détache.

### <a name="rconc-detached_thread"></a>CP.26 : Ne pas `detach()` un thread

##### Raison

Souvent, le besoin de survivre au scope de création est inhérent à la tâche du `thread`, mais implémenter cela par `detach()` le rend plus difficile à surveiller et à communiquer avec lui. En particulier, il est plus difficile (bien que pas impossible) de s’assurer que le thread s’est bien terminé ou vit la durée attendue.

##### Exemple

    void heartbeat();

    void use()
    {
        std::thread t(heartbeat);             // ne pas joindre ; le heartbeat est censé tourner indéfiniment
        t.detach();
        // ...
    }

C’est un usage raisonnable d’un thread, pour lequel `detach()` est couramment employé.  
Il y a toutefois des problèmes.  
Comment surveiller le thread détaché pour savoir s’il est vivant ?  
Quelque chose pourrait mal se passer avec le heartbeat, et perdre le heartbeat peut être très grave dans un système où il est indispensable.  
Il faut donc communiquer avec le thread heartbeat (par exemple via un flux de messages ou des événements de condition avec un `condition_variable`).

Une solution alternative, et généralement supérieure, consiste à contrôler sa durée de vie en le plaçant dans un scope extérieur à son point de création (ou d’activation). Par exemple :

    void heartbeat();

    gsl::joining_thread t(heartbeat);             // le heartbeat doit fonctionner « forever »

Ce heartbeat fonctionnera (sauf erreur, problème matériel, etc.) pendant toute la durée du programme.

Parfois, il faut séparer le point de création de la possession :

    void heartbeat();

    unique_ptr<gsl::joining_thread> tick_tock {nullptr};

    void use()
    {
        // le heartbeat doit fonctionner tant que tick_tock vit
        tick_tock = make_unique<gsl::joining_thread>(heartbeat);
        // ...
    }

#### Application

Signaler chaque appel à `detach()`.

### <a name="rconc-data-by-value"></a>CP.31 : Passer de petites quantités de données entre threads par valeur, plutôt que par référence ou pointeur

##### Raison

Une petite quantité de données coûte moins cher à copier et à accéder que le partage via un mécanisme de verrouillage.  
La copie donne naturellement une possession unique (simplifie le code) et élimine la possibilité de data races.

##### Note

Définir précisément « petite quantité » est impossible.

##### Exemple

    string modify1(string);
    void modify2(string&);

    void fct(string& s)
    {
        auto res = async(modify1, s);
        async(modify2, s);
    }

L’appel de `modify1` implique la copie de deux valeurs `string` ; l’appel de `modify2` n’en fait pas.  
D’autre part, l’implémentation de `modify1` est exactement ce que nous écririons pour du code mono‑thread, alors que celle de `modify2` devra recourir à un mécanisme de verrouillage pour éviter les data races.  
Si la chaîne est courte (disons 10 caractères), l’appel de `modify1` peut être étonnamment rapide ; le coût principal est le basculement de thread. Si la chaîne est longue (1 000 000 de caractères), la copier deux fois n’est probablement pas une bonne idée.

Notez que cet argument n’a rien à voir avec `async` en soi. Il s’applique de manière identique aux considérations d’utilisation de la messagerie ou de la mémoire partagée.

##### Application

???


### <a name="rconc-shared"></a>CP.32 : Pour partager la possession entre des `thread`s non liés, utiliser `shared_ptr`

##### Raison

Si les threads ne sont pas liés (c’est‑à‑dire pas connus pour être dans le même scope ou qu’un thread ne survit pas à l’autre) et qu’ils doivent partager de la mémoire du tas à supprimer, `shared_ptr` (ou équivalent) est le seul moyen sûr d’assurer une suppression correcte.

##### Exemple

    ???

##### Note

* Un objet statique (par ex. global) peut être partagé parce qu’il n’est pas possédé au sens où un thread serait responsable de sa destruction.
* Un objet sur le tas qui ne doit jamais être détruit peut être partagé.
* Un objet possédé par un thread peut être partagé en toute sécurité avec un autre tant que ce second thread ne survit pas au propriétaire.

##### Application

???


### <a name="rconc-switch"></a>CP.40 : Minimiser les changements de contexte

##### Raison

Les changements de contexte sont coûteux.

##### Exemple

    ???

##### Application

???


### <a name="rconc-create"></a>CP.41 : Minimiser la création et la destruction de threads

##### Raison

Créer un thread est coûteux.

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

Cela crée un `thread` par message, et `run_list` est probablement géré afin de détruire les tâches une fois terminées.

Il vaut mieux disposer d’un ensemble de threads travailleurs pré‑créés qui traitent les messages :

    Sync_queue<Message> work;

    void dispatcher(istream& is)
    {
        for (Message m; is >> m; )
            work.put(m);
    }

    void worker()
    {
        for (Message m; m = work.get(); ) {
            // process
        }
    }

    void workers()  // mettre en place des threads travailleurs (par ex. 4 threads)
    {
        joining_thread w1 {worker};
        joining_thread w2 {worker};
        joining_thread w3 {worker};
        joining_thread w4 {worker};
    }

##### Note

Si votre système possède un bon pool de threads, utilisez‑le.  
Si votre système possède une bonne file de messages, utilisez‑la.

##### Application

???


### <a name="rconc-wait"></a>CP.42 : Ne pas `wait` sans condition

##### Raison

Un `wait` sans condition peut manquer un réveil ou se réveiller simplement pour constater qu’il n’y a rien à faire.

##### Exemple, mauvais

    std::condition_variable cv;
    std::mutex mx;

    void thread1()
    {
        while (true) {
            // faire du travail …
            std::unique_lock<std::mutex> lock(mx);
            cv.notify_one();    // réveiller l’autre thread
        }
    }

    void thread2()
    {
        while (true) {
            std::unique_lock<std::mutex> lock(mx);
            cv.wait(lock);    // pourrait bloquer indéfiniment
            // faire du travail …
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
        condition_variable cond;    // contrôle l’accès
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
        cond.wait(lck, [this] { return !q.empty(); });    // empêche les réveils spourieux
        val = q.front();
        q.pop_front();
    }

Maintenant, si la file est vide lorsqu’un thread exécutant `get()` se réveille (par ex. parce qu’un autre thread a atteint `get()` avant lui), il reviendra immédiatement en sommeil, en attente d’un vrai élément.

##### Application

Signaler tous les `wait` dépourvus de condition.

### <a name="rconc-time"></a>CP.43 : Minimiser le temps passé dans une section critique

##### Raison

Moins le temps passé avec un `mutex` verrouillé est long, moins les autres `thread`s sont obligés d’attendre, et la suspension / reprise d’un thread est coûteuse.

##### Exemple

    void do_something() // mauvais
    {
        unique_lock<mutex> lck(my_lock);
        do0();  // préparation : pas besoin de verrou
        do1();  // transaction : nécessite le verrou
        do2();  // nettoyage : pas besoin de verrou
    }

Ici, nous conservons le verrou plus longtemps que nécessaire : nous aurions dû prendre le verrou uniquement quand il était requis et le libérer avant la phase de nettoyage.  
Nous pourrions réécrire ainsi :

    void do_something() // mauvais
    {
        do0();  // préparation : pas besoin de verrou
        my_lock.lock();
        do1();  // transaction : nécessite le verrou
        my_lock.unlock();
        do2();  // nettoyage : pas besoin de verrou
    }

Mais cela compromet la sûreté et viole la règle [utiliser le RAII](012-concurrency.md#rconc-raii).  
À la place, encadrons la section critique :

    void do_something() // OK
    {
        do0();  // préparation : pas besoin de verrou
        {
            unique_lock<mutex> lck(my_lock);
            do1();  // transaction : nécessite le verrou
        }
        do2();  // nettoyage : pas besoin de verrou
    }

##### Application

Impossible en général.  
Signaler les appels « nus » à `lock()` et `unlock()`.

### <a name="rconc-name"></a>CP.44 : Se souvenir de nommer ses `lock_guard`s et `unique_lock`s

##### Raison

Un objet local non nommé est un temporaire qui sort immédiatement du scope.

##### Exemple

    // mutex globaux
    mutex m1;
    mutex m2;

    void f()
    {
        unique_lock<mutex>(m1); // (A)
        lock_guard<mutex> {m2}; // (B)
        // faire du travail en section critique …
    }

Cela peut sembler anodin, mais ce n’est pas le cas.  
À (A), `m1` devient un `unique_lock` local par défaut qui masque le `::m1` global (et ne le verrouille pas).  
À (B), un `lock_guard` temporaire non nommé est construit et verrouille `::m2`, mais sort immédiatement du scope et le déverrouille de nouveau.  
Pour le reste de la fonction `f()`, aucun des deux mutex n’est verrouillé.

##### Application

Signaler tous les `lock_guard`s et `unique_lock`s non nommés.

### <a name="rconc-mutex"></a>CP.50 : Définir un `mutex` avec les données qu’il protège. Utiliser `synchronized_value<T>` quand c’est possible

##### Raison

Il doit être évident pour le lecteur que les données sont à protéger et comment. Cela diminue la probabilité de verrouiller le mauvais mutex, ou d’oublier de le verrouiller.

L’utilisation de `synchronized_value<T>` garantit que les données possèdent un mutex et que le bon mutex est verrouillé lors de l’accès aux données.  
Voir la [proposition WG21](https://www.open-std.org/jtc1/sc22/wg21/docs/papers/2023/p0290r4.html) visant à ajouter `synchronized_value` à une future TS ou révision du standard C++.

##### Exemple

    struct Record {
        std::mutex m;   // prendre ce mutex avant d’accéder aux autres membres
        // ...
    };

    class MyClass {
        struct DataRecord {
           // ...
        };
        synchronized_value<DataRecord> data; // Protéger les données avec un mutex
    };

##### Application

??? Possible ?

## <a name="sscp-coro"></a>CP.coro : Coroutines

Cette section porte sur les utilisations des coroutines.

### Résumé des règles des coroutines

* [CP.51 : Ne pas utiliser de lambda capturant qui sont des coroutines](012-concurrency.md#rcoro-capture)
* [CP.52 : Ne pas garder des verrous ou d’autres primitives de synchronisation à travers les points de suspension](012-concurrency.md#rcoro-locks)
* [CP.53 : Les paramètres des coroutines ne doivent pas être passés par référence](012-concurrency.md#rcoro-reference-parameters)

### <a name="rcoro-capture"></a>CP.51 : Ne pas utiliser de lambda capturant qui sont des coroutines

##### Raison

Les modèles d’utilisation corrects avec les lambdas classiques sont dangereux avec les lambdas‑coroutine. Le modèle évident de capture de variables aboutira à un accès à de la mémoire libérée après le premier point de suspension, même pour les pointeurs intelligents et les types copiable.

Une lambda crée un objet de clôture avec du stockage, souvent sur la pile, qui sortira du scope à un moment donné. Lorsque l’objet de clôture sort du scope, les captures le quittent également. Les lambdas classiques auront fini d’exécuter à ce moment‑ci, donc il n’y a pas de problème. Les lambdas‑coroutine, en revanche, peuvent reprendre après suspension alors que l’objet de clôture a déjà été détruit ; à ce moment les captures sont des accès à de la mémoire libérée.

##### Exemple, mauvais

    int value = get_value();
    std::shared_ptr<Foo> sharedFoo = get_foo();
    {
      const auto lambda = [value, sharedFoo]() -> std::future<void>
      {
        co_await something();
        // "sharedFoo" et "value" ont déjà été détruits
        // le pointeur partagé n’a rien accompli
      };
      lambda();
    } // l’objet de clôture de la lambda est maintenant sorti du scope

##### Exemple, meilleur

    int value = get_value();
    std::shared_ptr<Foo> sharedFoo = get_foo();
    {
      // prendre comme paramètres par valeur plutôt que comme capture
      const auto lambda = [](auto sharedFoo, auto value) -> std::future<void>
      {
        co_await something();
        // sharedFoo et value sont toujours valides ici
      };
      lambda(sharedFoo, value);
    } // l’objet de clôture de la lambda est maintenant sorti du scope

##### Exemple, idéal

Utiliser une fonction pour les coroutines.

    std::future<void> Class::do_something(int value, std::shared_ptr<Foo> sharedFoo)
    {
      co_await something();
      // sharedFoo et value sont toujours valides ici
    }

    void SomeOtherFunction()
    {
      int value = get_value();
      std::shared_ptr<Foo> sharedFoo = get_foo();
      do_something(value, sharedFoo);
    }

##### Application

Signaler une lambda qui est une coroutine et possède une liste de captures non vide.

### <a name="rcoro-locks"></a>CP.52 : Ne pas garder des verrous ou d’autres primitives de synchronisation à travers les points de suspension

##### Raison

Ce modèle crée un risque important d’interblocage. Certains types d’attente permettent au thread actuel d’exécuter du travail supplémentaire jusqu’à ce que l’opération asynchrone se complète. Si le thread qui détient le verrou effectue du travail nécessitant le même verrou, il s’interbloquera car il tente d’acquérir un verrou déjà détenu.

Si la coroutine se termine sur un thread différent de celui qui a acquis le verrou, c’est un comportement indéfini. Même avec un retour explicite au thread d’origine, une exception peut être levée avant que la coroutine ne reprenne, et le garde‑verrou ne sera pas détruit.

##### Exemple, mauvais

    std::mutex g_lock;

    std::future<void> Class::do_something()
    {
        std::lock_guard<std::mutex> guard(g_lock);
        co_await something(); // DANGER : la coroutine est suspendue alors qu’un verrou est détenu
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
        co_await something(); // OK : le verrou a été libéré avant la suspension
        co_await somethingElse();
    }

##### Note

Ce modèle est également mauvais pour la performance. Lorsqu’un point de suspension est atteint, comme `co_await`, l’exécution de la fonction actuelle s’arrête et d’autres codes s’exécutent. Cela peut durer longtemps avant que la coroutine ne reprenne. Pendant toute cette durée, le verrou demeure pris et ne peut être acquis par d’autres threads pour travailler.

##### Application

Signaler tous les garde‑verrou qui ne sont pas détruits avant la suspension d’une coroutine.

### <a name="rcoro-reference-parameters"></a>CP.53 : Les paramètres des coroutines ne doivent pas être passés par référence

##### Raison

Une fois qu’une coroutine atteint le premier point de suspension, comme `co_await`, la partie synchrone retourne. Après ce point, tout paramètre passé par référence devient pendulaire. Toute utilisation au‑delà est un comportement indéfini pouvant inclure l’écriture dans de la mémoire libérée.

##### Exemple, mauvais

    std::future<int> Class::do_something(const std::shared_ptr<int>& input)
    {
        co_await something();

        // DANGER : la référence à input peut ne plus être valide (mémoire libérée)
        co_return *input + 1;
    }

##### Exemple, bon

    std::future<int> Class::do_something(std::shared_ptr<int> input)
    {
        co_await something();
        co_return *input + 1; // input est une copie qui reste valide ici
    }

##### Note

Ce problème ne s’applique pas aux paramètres de référence qui ne sont accédés qu’avant le premier point de suspension. Des modifications ultérieures de la fonction pourraient ajouter ou déplacer des points de suspension, réintroduisant ce type de bug. Certains types de coroutines ont le point de suspension avant même que la première ligne de code ne s’exécute, auquel cas les paramètres de référence sont toujours dangereux. Il est plus sûr de toujours passer par valeur, car la copie du paramètre vivra dans le cadre de la coroutine et sera sûre pendant toute la durée de la coroutine.

##### Note

Le même danger s’applique aux paramètres de sortie. [F.20 : Pour les valeurs de sortie, privilégier les valeurs de retour aux paramètres de sortie](006-functions.md#rf-out) décourage les paramètres de sortie. Les coroutines devraient les éviter complètement.

##### Application

Signaler tous les paramètres de référence d’une coroutine.

## <a name="sscp-par"></a>CP.par : Parallélisme

Par « parallélisme », nous entendons l’exécution d’une tâche (plus ou moins) simultanément (« en parallèle avec ») sur de nombreux éléments de données.

### Résumé des règles de parallélisme

* ???
* ???
* Le cas échéant, privilégier les algorithmes de la bibliothèque standard parallèles
* Utiliser des algorithmes conçus pour le parallélisme, et non des algorithmes dépendant inutilement d’une évaluation linéaire

## <a name="sscp-mess"></a>CP.mess : Passage de messages

Les facilities de la bibliothèque standard sont assez bas‑niveau, orientées vers les besoins de programmation proche du matériel à l’aide de `thread`s, `mutex`es, types `atomic`, etc.  
La plupart des gens ne devraient pas travailler à ce niveau : c’est source d’erreurs et le développement est lent.  
Si possible, utilisez une facility de plus haut niveau : bibliothèques de messagerie, algorithmes parallèles, vectorisation.  
Cette section examine le passage de messages afin que le programmeur n’ait pas à synchroniser explicitement.

### Résumé des règles de passage de messages

* [CP.60 : Utiliser un `future` pour retourner une valeur d’une tâche concurrente](012-concurrency.md#rconc-future)
* [CP.61 : Utiliser `async()` pour créer des tâches concurrentes](012-concurrency.md#rconc-async)
* files d’attente de messages
* bibliothèques de messagerie

???? devrait‑il y avoir un « utiliser X plutôt que `std::async` » où X serait quelque chose offrant un pool de threads mieux spécifié ?

??? `std::async` vaut‑il la peine d’être utilisé à la lumière des futures (et même des facilités de parallélisme existantes ou de bibliothèques) ? Que recommander aux personnes qui souhaitent paralléliser, par exemple, `std::accumulate` (avec la prémisse supplémentaire de commutativité), ou le tri fusion ?

### <a name="rconc-future"></a>CP.60 : Utiliser un `future` pour retourner une valeur d’une tâche concurrente

##### Raison

Un `future` préserve la sémantique habituelle de retour de fonction pour les tâches asynchrones.  
Il n’y a pas besoin de verrou explicite et le retour correct (valeur) comme le retour d’erreur (exception) sont gérés simplement.

##### Exemple

    ???

##### Note

???

##### Application

???

### <a name="rconc-async"></a>CP.61 : Utiliser `async()` pour créer des tâches concurrentes

##### Raison

Semblable à [R.12](009-resource.md#rr-immediate-alloc), qui vous dit d’éviter les pointeurs bruts propriétaires, vous devriez également éviter les threads bruts et les promesses brutes chaque fois que possible. Utilisez une fonction usine comme `std::async`, qui gère la création ou la réutilisation d’un thread sans exposer de threads bruts dans votre propre code.

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
            // gérer l’exception ici
        }
    }

##### Note

Malheureusement, `std::async` n’est pas parfait. Par exemple, il n’utilise pas de pool de threads, ce qui signifie qu’il peut échouer faute de ressources plutôt que de mettre en file d’attente vos tâches pour les exécuter plus tard. Cependant, même si vous ne pouvez pas utiliser `std::async`, vous devriez préférer écrire votre propre fonction usine renvoyant un `future`, plutôt que d’utiliser des promesses brutes.

##### Exemple (mauvais)

Cet exemple montre deux manières différentes de réussir à utiliser `std::future`, mais d’échouer à éviter la gestion brute de `std::thread`.

    void async_example()
    {
        std::promise<int> p1;
        std::future<int> f1 = p1.get_future();
        std::thread t1([p1 = std::move(p1)]() mutable {
            p1.set_value(read_value("v1.txt"));
        });
        t1.detach(); // malveillant

        std::packaged_task<int()> pt2(read_value, "v2.txt");
        std::future<int> f2 = pt2.get_future();
        std::thread(std::move(pt2)).detach();

        std::cout << f1.get() + f2.get() << '\n';
    }

##### Exemple (bon)

Cet exemple montre une façon de suivre le modèle général imposé par `std::async`, dans un contexte où `std::async` lui‑même était inacceptable en production.

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

Tous les threads créés pour exécuter le code de `read_value` sont cachés derrière l’appel à `WorkQueue::enqueue`. L’utilisateur ne travaille qu’avec des objets `future`, jamais avec des objets `thread`, `promise` ou `packaged_task` bruts.

##### Application

???


## <a name="sscp-vec"></a>CP.vec : Vectorisation

La vectorisation est une technique consistant à exécuter simultanément un nombre de tâches sans introduire de synchronisation explicite.  
Une opération est simplement appliquée aux éléments d’une structure de données (un vecteur, un tableau, etc.) en parallèle.  
La vectorisation possède la propriété intéressante de souvent ne nécessiter aucun changement non‑local du programme. Cependant, elle fonctionne mieux avec des structures de données simples et des algorithmes spécialement conçus pour la permettre.

### Résumé des règles de vectorisation

* ???
* ???

## <a name="sscp-free"></a>CP.free : Programmation lock‑free

La synchronisation à l’aide de `mutex`es et de `condition_variable`s peut être relativement chère.  
De plus, elle peut conduire à des interblocages. Pour la performance et afin d’éliminer la possibilité d’interblocages, nous devons parfois recourir aux facilities bas‑niveau « lock‑free » qui nécessitent d’obtenir brièvement un accès exclusif (« atomique ») à la mémoire. La programmation lock‑free est aussi utilisée pour implémenter des mécanismes de concurrence de plus haut niveau, tels que `thread`s et `mutex`es.

### Résumé des règles de programmation lock‑free

* [CP.100 : Ne pas utiliser la programmation lock‑free sauf si c’est absolument nécessaire](012-concurrency.md#rconc-lockfree)
* [CP.101 : Se méfier de la combinaison matériel/compilateur](012-concurrency.md#rconc-distrust)
* [CP.102 : Étudier attentivement la littérature](012-concurrency.md#rconc-literature)
* comment/quand utiliser les atomics
* éviter la starvation
* utiliser une structure de données lock‑free plutôt que d’en concevoir une soi‑même
* [CP.110 : Ne pas écrire son propre double‑checked locking pour l’initialisation](012-concurrency.md#rconc-double)
* [CP.111 : Utiliser un schéma conventionnel si vous avez réellement besoin du double‑checked locking](012-concurrency.md#rconc-double-pattern)
* comment/quand comparer et échanger

### <a name="rconc-lockfree"></a>CP.100 : Ne pas utiliser la programmation lock‑free sauf si c’est absolument nécessaire

##### Raison

C’est source d’erreurs et requiert une expertise avancée du langage, de l’architecture machine et des structures de données.

##### Exemple, mauvais

    extern atomic<Link*> head;        // tête partagée d’une liste chaînée

    Link* nh = new Link(data, nullptr);    // créer un lien prêt pour insertion
    Link* h = head.load();                 // lire la tête partagée de la liste

    do {
        if (h->data <= data) break;        // si c’est le cas, insérer ailleurs
        nh->next = h;                      // l’élément suivant est l’ancienne tête
    } while (!head.compare_exchange_weak(h, nh));    // écrire nh dans head ou mettre à jour h

Repérez le bug. Ce serait vraiment difficile à détecter par tests. Renseignez‑vous sur le problème ABA.

##### Exception

Les variables atomiques peuvent être utilisées simplement et en toute sécurité, tant que vous utilisez le modèle de mémoire séquentiellement cohérent (`memory_order_seq_cst`), qui est la valeur par défaut.

##### Note

Des mécanismes de haut niveau, comme les `thread`s et les `mutex`es, sont implémentés à l’aide de la programmation lock‑free.

**Alternative** : Utiliser des structures de données lock‑free implémentées par d’autres bibliothèques.

### <a name="rconc-distrust"></a>CP.101 : Se méfier de la combinaison matériel/compilateur

##### Raison

Les interfaces matérielles bas‑niveau utilisées par la programmation lock‑free sont parmi les plus difficiles à implémenter correctement et parmi les domaines où les problèmes de portabilité les plus subtils se produisent.  
Si vous faites de la programmation lock‑free pour la performance, vous devez vérifier les régressions.

##### Note

Le réordonnancement des instructions (statique et dynamique) rend difficile une réflexion efficace à ce niveau (surtout si vous utilisez des modèles de mémoire relâchés). L’expérience, les modèles (semi)formels et le model‑checking peuvent être utiles. Les tests – souvent à l’extrême – sont essentiels. « Ne volez pas trop près du soleil ».

##### Application

Mettre en place des règles strictes de re‑test couvrant tout changement de matériel, système d’exploitation, compilateur ou bibliothèques.

### <a name="rconc-literature"></a>CP.102 : Étudier attentivement la littérature

##### Raison

À l’exception des atomics et de quelques autres motifs standards, la programmation lock‑free est vraiment réservée aux experts. Devenez expert avant de livrer du code lock‑free à d’autres.

##### Références

* Anthony Williams : *C++ Concurrency in Action*. Manning Publications.
* Boehm, Adve, *You Don't Know Jack About Shared Variables or Memory Models*, Communications of the ACM, fév. 2012.
* Boehm, *Threads Basics*, HPL TR 2009‑259.
* Adve, Boehm, *Memory Models: A Case for Rethinking Parallel Languages and Hardware*, Communications of the ACM, août 2010.
* Boehm, Adve, *Foundations of the C++ Concurrency Memory Model*, PLDI 2008.
* Mark Batty, Scott Owens, Susmit Sarkar, Peter Sewell, Tjark Weber, *Mathematizing C++ Concurrency*, POPL 2011.
* Damian Dechev, Peter Pirkelbauer, Bjarne Stroustrup, *Understanding and Effectively Preventing the ABA Problem in Descriptor‑based Lock‑free Designs*, 13th IEEE Computer Society ISORC 2010.
* Damian Dechev, Bjarne Stroustrup, *Scalable Non‑blocking Concurrent Objects for Mission Critical Code*, OOPSLA 2009.
* Damian Dechev, Peter Pirkelbauer, Nicolas Rouquette, Bjarne Stroustrup, *Semantically Enhanced Containers for Concurrent Real‑Time Systems*, IEEE ECBS 2009.
* Maurice Herlihy, Nir Shavit, Victor Luchangco, Michael Spear, *The Art of Multiprocessor Programming*, 2e éd., sept. 2020.

### <a name="rconc-double"></a>CP.110 : Ne pas écrire son propre double‑checked locking pour l’initialisation

##### Raison

Depuis C++11, les variables locales `static` sont initialisées de façon thread‑safe. Couplées au pattern RAII, les variables `static` locales peuvent remplacer le besoin d’écrire votre propre double‑checked locking pour l’initialisation. `std::call_once` peut également atteindre le même objectif. Utilisez soit les variables `static` thread‑safe de C++11, soit `std::call_once` au lieu d’écrire votre propre double‑checked locking pour l’initialisation.

##### Exemple (avec `std::call_once`)

    void f()
    {
        static std::once_flag my_once_flag;
        std::call_once(my_once_flag, []()
        {
            // faire cela une seule fois
        });
        // ...
    }

##### Exemple (avec variables locales `static` thread‑safe de C++11)

    void f()
    {
        // En supposant que le compilateur respecte C++11
        static My_class my_object; // le constructeur n’est appelé qu’une fois
        // ...
    }

    class My_class
    {
    public:
        My_class()
        {
            // faire cela une seule fois
        }
    };

##### Application

??? Peut‑on détecter cet idiome ?

### <a name="rconc-double-pattern"></a>CP.111 : Utiliser un schéma conventionnel si vous avez réellement besoin du double‑checked locking

##### Raison

Le double‑checked locking est facile à mal faire. Si vous avez réellement besoin d’écrire votre propre double‑checked locking, en dépit des règles [CP.110] et [CP.100], faites‑le selon un schéma conventionnel.

Les usages du double‑checked locking qui ne violent pas [CP.110] surviennent lorsque une action non‑thread‑safe est à la fois difficile et rare, et qu’il existe un test thread‑safe rapide qui garantit que l’action n’est pas nécessaire, mais qui ne peut pas garantir le contraire.

##### Exemple, mauvais

L’utilisation de `volatile` ne rend pas le premier test thread‑safe ; voir aussi [CP.200 : Utiliser `volatile` uniquement pour communiquer avec de la mémoire non‑C++].

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

Un ordre de mémoire finement ajusté peut être bénéfique lorsque le chargement `acquire` est plus efficace que le chargement séquentiellement cohérent.

    mutex action_mutex;
    atomic<bool> action_needed;

    if (action_needed.load(std::memory_order_acquire)) {
        std::lock_guard<std::mutex> lock(action_mutex);
        if (action_needed.load(std::memory_order_relaxed)) {
            take_action();
            action_needed.store(false, std::memory_order_release);
        }
    }

##### Application

??? Peut‑on détecter cet idiome ?

## <a name="sscp-etc"></a>CP.etc : Autres règles de concurrence

Ces règles échappent à une catégorisation simple :

* [CP.200 : Utiliser `volatile` uniquement pour parler à une mémoire non‑C++](012-concurrency.md#rconc-volatile2)
* [CP.201 : ??? Signaux](012-concurrency.md#rconc-signal)

### <a name="rconc-volatile2"></a>CP.200 : Utiliser `volatile` uniquement pour parler à une mémoire non‑C++

##### Raison

`volatile` est utilisé pour désigner des objets partagés avec du code « non‑C++ » ou du matériel qui ne suit pas le modèle mémoire C++.

##### Exemple

    const volatile long clock;

Cela décrit un registre constamment mis à jour par un circuit d’horloge.  
`clock` est `volatile` parce que sa valeur changera sans aucune action du programme C++ qui l’utilise. Par exemple, lire `clock` deux fois donnera souvent deux valeurs différentes, ainsi l’optimiseur doit au moins ne pas éliminer la seconde lecture :

    long t1 = clock;
    // … aucun usage de clock ici …
    long t2 = clock;

`clock` est `const` parce que le programme ne doit pas écrire dans `clock`.

##### Note

À moins que vous n’écriviez du code de très bas niveau manipulant directement du matériel, considérez `volatile` comme une fonctionnalité ésotérique à éviter.

##### Exemple

Habituellement, le code C++ reçoit de la mémoire `volatile` qui est possédée ailleurs (matériel ou autre langage) :

    int volatile* vi = get_hardware_memory_location();
        // note : nous obtenons un pointeur vers la mémoire de quelqu’un d’autre
        // volatile signifie « traitez ceci avec plus de respect »

Parfois, le code C++ alloue la mémoire `volatile` et la partage avec « ailleurs » (matériel ou autre langage) en échappant volontairement un pointeur :

    static volatile long vl;
    please_use_this(&vl);   // échapper une référence à « ailleurs » (pas C++)

##### Exemple, mauvais

Les variables locales `volatile` sont presque toujours erronées — comment pourraient‑elles être partagées avec d’autres langages ou du matériel si elles sont éphémères ?  
Il en va de même, presque aussi fortement, pour les membres de données.

    void f()
    {
        volatile int i = 0; // mauvais, variable locale volatile
        // …
    }

    class My_type {
        volatile int i = 0; // suspect, membre volatile
        // …
    };

##### Note

En C++, contrairement à certains autres langages, `volatile` n’a **rien à voir avec la synchronisation**.

##### Application

* Signaler les déclarations `volatile T` locales et membres ; il s’agit très probablement d’une utilisation à la place de `atomic<T>`.
* ???

### <a name="rconc-signal"></a>CP.201 : ??? Signaux

??? Gestion des signaux UNIX ? Il pourrait être utile de rappeler à quel point peu de fonctions sont async‑signal‑safe, et comment communiquer avec un gestionnaire de signaux (le meilleur est probablement « pas du tout »).