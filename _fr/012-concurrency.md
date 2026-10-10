# <a name="s-concurrency"></a>CP: Concurrence et parallélisme

Nous voulons souvent que nos ordinateurs effectuent plusieurs tâches simultanément (ou qu'ils donnent l’impression de le faire en même temps). Les raisons de cette démarche varient (par ex., attendre de nombreux événements en n’utilisant qu’un seul processeur, traiter simultanément plusieurs flux de données, ou exploiter de nombreuses ressources matérielles) et les facilités de base pour exprimer la concurrence et le parallélisme varient d'autant. Ici, nous articulons des principes et des règles pour utiliser les facilités ISO de C++ afin d’exprimer la concurrence et le parallélisme de base.

Les threads constituent la fondation machine à la programmation concurrente et parallèle. Ils permettent d’exécuter plusieurs sections d’un programme de façon indépendante tout en partageant la même mémoire. La programmation concurrente est délicate : protéger les données partagées entre threads est plus simple à dire qu’à faire. Faire exécuter un code mono‑threadé de façon concurrente peut être aussi trivial que d’ajouter stratégiquement `std::async` ou `std::thread`, ou bien nécessiter une réécriture complète, selon que le code d’origine a été écrit dans un style favorable aux threads.

Les règles de concurrence / parallélisme dans ce document sont conçues avec trois objectifs à l’esprit :

* Aider à écrire un code qui peut être utilisé dans un environnement multi‑threadé.
* Montrer des façons propres et sûres d’utiliser les primitives de thread offertes par la bibliothèque standard.
* Fournir des indications quant à la manière de réagir lorsque la concurrence et le parallélisme ne procurent pas les gains de performance attendus.

Il est également important de noter que la concurrence en C++ est une histoire inachevée. C++11 a introduit de nombreuses primitives de concurrence de base, C++14 et C++17 les ont améliorées, et l’intérêt pour rendre la rédaction de programmes concurrents en C++ plus simple ne cesse de croître. Nous attendons que certaines recommandations liées aux bibliothèques puissent changer de façon significative au fil du temps.

Cette section nécessite beaucoup de travail (évidemment). Nous débutons avec des règles destinées aux non‑experts. Les experts devront attendre un peu ; les contributions sont bienvenues, mais pensez à la majorité des programmeurs qui ont du mal à rendre leurs programmes concurrents corrects et performants.

## Résumé des règles de concurrence et parallélisme :

* [CP.1 : Supposons que votre code s'exécutera dans le cadre d'un programme multi‑threadé](#rconc-multi)
* [CP.2 : Éviter les courses de données](#rconc-races)
* [CP.3 : Minimiser le partage explicite de données modifiables](#rconc-data)
* [CP.4 : Penser en termes de tâches plutôt que de threads](#rconc-task)
* [CP.8 : Ne pas essayer d'utiliser `volatile` pour la synchronisation](#rconc-volatile)
* [CP.9 : Chaque fois qu'il est possible, utiliser des outils pour valider votre code concurrent](#rconc-tools)

**Voir également** :

* [CP.con : Concurrence](#sscp-con)
* [CP.coro : Coroutines](#sscp-coro)
* [CP.par : Parallélisme](#sscp-par)
* [CP.mess : Passage de messages](#sscp-mess)
* [CP.vec : Vectorisation](#sscp-vec)
* [CP.free : Programmation sans verrou](#sscp-free)
* [CP.etc : Autres règles de concurrence](#sscp-etc)

### <a name="rconc-multi"></a>CP.1 : Supposons que votre code s'exécutera dans le cadre d'un programme multi‑threadé

#### Raison

Il est difficile de garantir que la concurrence n’est pas déjà utilisée ou ne l’êtreait pas dans un futur. Le code est réutilisé. Une bibliothèque qui ne fait pas usage de threads peut être appelée depuis une partie d'un programme qui l'utilise. Notez que cette règle s'applique de façon urgente aux bibliothèques et moins aux applications autonomes. Cependant, au fil du temps, des fragments de code peuvent apparaître en des endroits inattendus.

#### Exemple, mauvais

    double cached_computation(int x)
    {
        // Mauvais : ces statiques provoquent des courses de données dans un contexte multi‑thread
        static int cached_x = 0.0;
        static double cached_result = COMPUTATION_OF_ZERO;

        if (cached_x != x) {
            cached_x = x;
            cached_result = computation(x);
        }
        return cached_result;
    }

Bien que `cached_computation` fonctionne parfaitement dans un environnement mono‑thread, dans un environnement multi‑thread les deux variables statiques provoquent des courses de données et du comportement indéfini.

#### Exemple, bon

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

Ici, le cache est stocké comme données membres d’un objet `ComputationCache`, plutôt que comme état statique partagé. Ce refactorisation délègue essentiellement la préoccupation vers l’appelant : un programme mono‑threadé peut encore choisir d’avoir un `ComputationCache` global, tandis qu’un programme multi‑threadé peut en avoir un par thread, ou un par « contexte » pour n’importe quelle définition de « contexte ». La fonction refactorisée n’essaye plus de gérer l’allocation de `cached_x`. En ce sens, c’est une application du principe de responsabilité unique.

Dans cet exemple précis, refactoriser pour la sécurité thread améliore également la réutilisabilité dans les programmes mono‑thread. Il n’est pas difficile d’imaginer qu’un programme mono‑threadé veuille disposer de deux instances `ComputationCache` à utiliser dans différentes parties du programme, sans qu’elles n’écrasent leurs données mises en cache.

Il existe plusieurs autres moyens d’ajouter la sécurité thread à un code écrit pour un environnement multi‑threadé standard (c’est‑à‑dire où la seule forme de concurrence est `std::thread`) :

* Marquer les variables d’état comme `thread_local` plutôt que comme `static`.
* Mettre en place un contrôle de concurrence, par ex. : protéger l’accès aux deux variables `static` avec un `static std::mutex`.
* Refuser de construire ou exécuter dans un environnement multi‑threadé.
* Fournir deux implémentations : une pour les environnements mono‑threadés et une autre pour les environnements multi‑threadés.

#### Exception

Code qui n’est jamais exécuté dans un environnement multi‑threadé.

Soyez prudent : il existe de nombreux exemples où un code que l’on supposait « ne jamais s’exécuter dans un programme multi‑threadé » est en fait utilisé dans un tel programme, souvent des années plus tard. Les programmes ainsi créés conduisent souvent à un effort douloureux pour enlever les courses de données. Par conséquent, un code qui n’est pas destiné à s’exécuter dans un environnement multi‑threadé doit être clairement identifié comme tel et idéalement accompagné d’un mécanisme de vérification à la compilation ou à l’exécution afin de détecter ces bugs d’usage dès que possible.

### <a name="rconc-races"></a>CP.2 : Éviter les courses de données

#### Raison

Au contraire, rien ne garantit du tout le bon fonctionnement et les erreurs subtiles persistent.

#### Note

En courte forme, si deux threads peuvent accéder simultanément à la même instance (sans synchronisation) et que l’un d’eux écrit (opération non‑constante), une course de données s’est produite. Pour plus d’information sur la façon d’utiliser la synchronisation correctement afin d’éliminer les courses de données, consultez un bon livre de la littérature (voir [Étudier soigneusement la littérature](#rconc-literature)).

#### Exemple, mauvais

Il existe de nombreux exemples de courses de données qui existent, certains de ceux‑ci tournent même dans un logiciel de production en ce moment. Un exemple très simple :

    int get_id()
    {
      static int id = 1;
      return id++;
    }

L’incrément ci‑dessus est un exemple de course de données. Voici quelques façons dont cela peut mal tourner :

* Le thread A charge la valeur de `id`, l’OS bascule A hors de son contexte pour un certain temps, durant lequel d’autres threads créent des centaines d’ID. Quand le thread A est autorisé à reprendre, `id` est réécrit à cette position comme la lecture de `id` par A plus un.
* Le thread A et le thread B chargent `id` et l’incrémentent simultanément. Ils obtiennent alors le même ID.

Les variables statiques locales sont une source courante de courses de données.

#### Exemple, mauvais

    void f(fstream& fs, regex pattern)
    {
        array<double, max> buf;
        int sz = read_vec(fs, buf, max);            // lire depuis fs dans buf
        gsl::span<double> s {buf};
        // ...
        auto h1 = async([&] { sort(std::execution::par, s); });     // lancer une tâche pour trier
        // ...
        auto h2 = async([&] { return find_all(buf, sz, pattern); });   // lancer une tâche pour chercher les correspondances
        // ...
    }

Ici, il y a une (désastreuse) course de données sur les éléments de `buf` (`sort` lira et écrira). Toutes les courses de données sont désastreuses. Ici, nous avons réussi à obtenir une course de données sur les données de la pile. Toutes les courses de données ne sont pas aussi faciles à repérer que celle‑ci.

#### Exemple, mauvais

    // Code non contrôlé par un verrou

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

Un compilateur qui ne sait pas que `val` peut changer l’implémentera très probablement `switch` à l’aide d’une table d’appels avec cinq entrées. Ensuite, un `val` hors de l’intervalle `[0..4]` provoquera un saut vers une adresse qui peut se trouver n’importe où dans le programme, et l’exécution se poursuivra là. En fin de compte, « tout est possible » si vous obtenez une course de données. En fait, cela peut être pire encore : en examinant le code généré, vous pouvez déterminer vers quel endroit l’exécution sautera pour une valeur donnée ; ce qui peut constituer un risque de sécurité.

#### Application

Certaines solutions sont possibles : faites quelque chose au moins. Il existe des outils commerciaux et open‑source qui tentent de résoudre ce problème, mais soyez conscient que ces solutions ont des coûts et des zones d’ombre. Les outils statiques donnent souvent de faux positifs, et les outils à exécution ont souvent un coût significatif. Nous espérons de meilleurs outils. L’usage de plusieurs outils permet de détecter plus de problèmes qu’un seul.

Il existe d’autres moyens d’atténuer la probabilité de courses de données :

* Éviter les données globales
* Éviter les variables `static`
* Utiliser davantage de types concrets sur la pile (et ne pas passer trop de pointeurs)
* Utiliser davantage de données immutables (literals, `constexpr`, et `const`)

### <a name="rconc-data"></a>CP.3 : Minimiser le partage explicite de données modifiables

#### Raison

Si vous ne partagez pas de données modifiables, vous ne pouvez pas avoir de course de données. Moins vous partagez, moins votre risque d’oublier de synchroniser l’accès (et de créer des courses de données). Moins vous partagez, moins vous risquez de bloquer sur un verrou (donc la performance peut s’améliorer).

#### Exemple

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

Sans ces `const`, nous devrions passer en revue chaque fonction invoquée de façon asynchrone pour des courses de données potentielles sur `surface_readings`. Faire de `surface_readings` `const` (du point de vue de cette fonction) permet de raisonner avec uniquement le corps de la fonction.

#### Note

Les données immutables peuvent être partagées en toute sécurité et efficacement. Aucun verrou n’est nécessaire : on ne peut pas avoir de course de données sur une constante. Voir également [CP.mess : Passage de messages](#sscp-mess) et [CP.31 : Préférer le passage par valeur](#rconc-data-by-value).

#### Application

???. 

### <a name="rconc-task"></a>CP.4 : Penser en termes de tâches plutôt que de threads

#### Raison

Un `thread` est un concept d’implémentation, une façon d’envisager la machine. Une tâche est un concept d’application, quelque chose que vous voulez faire, idéalement simultanément avec d’autres tâches. Les concepts d’application sont plus faciles à raisonner.

#### Exemple

    void some_fun(const std::string& msg)
    {
        std::thread publisher([=] { std::cout << msg; });      // mauvais : moins expressif
                                                               //      et plus sujette aux erreurs
        auto pubtask = std::async([=] { std::cout << msg; });  // OK
        // ...
        publisher.join();
    }

#### Note

À l’exception de `async()`, les facilités de la bibliothèque standard restent de basse couche, orientées machine, threads et verrou. C’est une base nécessaire, mais nous devons essayer d’élever le niveau d’abstraction : pour la productivité, la fiabilité et la performance. C’est un argument puissant en faveur de l’utilisation de bibliothèques plus haut niveau, plus appliquées (si possible, construites au-dessus des facilités de la bibliothèque standard).

#### Application

???. 

### <a name="rconc-volatile"></a>CP.8 : Ne pas essayer d’utiliser `volatile` pour la synchronisation

#### Raison

En C++, contrairement à d’autres langages, `volatile` ne fournit pas d’atome, ne synchronise pas entre les threads, et ne prévient pas le réordonnancement des instructions (ni le compilateur ni le matériel). Il n’a rien à voir avec la concurrence.

#### Exemple, mauvais

    int free_slots = max_slots; // source actuelle de mémoire pour les objets

    Pool* use()
    {
        if (int n = free_slots--) return &pool[n];
    }

Ici, un problème : c’est un code parfaitement valable dans un programme mono‑threadé, mais si deux threads exécutent ce code, il y a une condition de course sur `free_slots` de sorte que deux threads puissent obtenir la même valeur et l’objet. C’est (évidemment) une course de données, donc les personnes formées dans d’autres langages peuvent tenter de corriger ce problème ainsi :

    volatile int free_slots = max_slots; // source actuelle de mémoire pour les objets

    Pool* use()
    {
        if (int n = free_slots--) return &pool[n];
    }

Cela n’affecte pas la synchronisation : la course de données est toujours présente !

La mécanique C++ pour ce problème consiste à utiliser les types `atomic` :

    atomic<int> free_slots = max_slots; // source actuelle de mémoire pour les objets

    Pool* use()
    {
        if (int n = free_slots--) return &pool[n];
    }

Maintenant, l’opération `--` est atomique, plutôt qu’une séquence lecture‑incrément‑écriture où un autre thread peut intercaler entre les opérations individuelles.

#### Alternative

Utilisez des types `atomic` là où vous pourriez avoir utilisé `volatile` dans un autre langage. Utilisez un `mutex` pour les exemples plus compliqués.

#### Voir aussi

[(Utilisations rares de `volatile`)](#rconc-volatile2)

### <a name="rconc-tools"></a>CP.9 : Chaque fois qu’il est possible, utiliser des outils pour valider votre code concurrent

L’expérience montre que le code concurrent est exceptionnellement difficile à maîtriser et que la vérification à la compilation, les vérifications d’exécution, et les tests sont moins efficaces pour détecter les erreurs de concurrence que pour identifier les erreurs dans un code séquentiel. Les erreurs subtiles de concurrence peuvent avoir des effets catastrophiques, notamment la corruption de la mémoire, les interblocages et les failles de sécurité.

#### Exemple

    ???  

#### Note

La sécurité d’un code concurrent est un défi, souvent plus délicat que celui des programmeurs expérimentés. Les outils constituent une stratégie importante pour atténuer ces risques. Il existe de nombreux outils « out there », à la fois commerciaux et open source, à la fois de recherche et de production. Malheureusement, les besoins et contraintes des développeurs diffèrent tellement que nous ne pouvons pas faire de recommandations spécifiques, mais nous pouvons mentionner :

* Outils d’application statique : tant [clang](https://clang.llvm.org/docs/ThreadSafetyAnalysis.html) que certaines versions plus anciennes de [GCC](https://gcc.gnu.org/wiki/ThreadSafetyAnnotation) offrent un support pour l’annotation statique des propriétés de sécurité des threads. Un usage cohérent de cette technique transforme de nombreuses catégories d’erreurs de sécurité des threads en erreurs de compilation. Les annotations sont généralement localisations (marquer un membre de données particulier par un mutex particulier), et sont généralement faciles à apprendre. Cependant, comme pour beaucoup d’outils statiques, il arrive souvent des faux négatifs ; les cas qui auraient dû être capturés restent autorisés.

* Outils d’application runtime : le [Thread Sanitizer](https://clang.llvm.org/docs/ThreadSanitizer.html) (alias TSAN) est un exemple puissant d’outils dynamiques : il modifie la construction et l’exécution de votre programme pour ajouter un bookkeeping sur l’accès mémoire, et identifier absolument les courses de données dans une exécution donnée de votre binaire. Le coût, à la fois en mémoire (5‑10× en général) et en baisse du CPU (2‑20×), est considérable. Les outils dynamiques comme celui‑ci sont les plus efficaces lorsqu’ils sont appliqués aux tests d’intégration, aux canaris de push ou aux tests unitaires qui utilisent plusieurs threads. La charge de travail compte : quand TSAN identifie un problème, c’est généralement une vraie course de données ; cependant il ne peut identifier que les courses observées dans une exécution donnée.

#### Application

Il appartient au constructeur de l’application de choisir les outils de support qui sont précieux pour cette application particulière.

## <a name="sscp-con"></a>CP.con : Concurrence

Cette section se concentre sur les utilisations ad‑hoc de plusieurs threads communiquant via des données partagées.

* Pour les algorithmes parallèles, voir [Parallélisme](#sscp-par)
* Pour la communication inter‑tâche sans partage explicite, voir [Passage de messages](#sscp-mess)
* Pour les codes vectoriels parallèles, voir [Vectorisation](#sscp-vec)
* Pour la programmation sans verrou, voir [Sans verrou](#sscp-free)

### Résumé des règles de concurrence :

* [CP.20 : Utilisez RAII, jamais `lock()`/`unlock()`](#rconc-raii)
* [CP.21 : Utilisez `std::lock()` ou `std::scoped_lock` pour acquérir plusieurs `mutex`](#rconc-lock)
* [CP.22 : N’appelons jamais de code inconnu tout en tenant un verrou (ex. un rappel)](#rconc-unknown)
* [CP.23 : Considérez un `thread` qui joint comme un conteneur de portée](#rconc-join)
* [CP.24 : Considérez un `thread` comme un conteneur global](#rconc-detach)
* [CP.25 : Préférez `gsl::joining_thread` à `std::thread`](#rconc-joining_thread)
* [CP.26 : Ne jamais `detach()` un thread](#rconc-detached_thread)
* [CP.31 : Passez de petites quantités de données entre threads par valeur plutôt que par référence ou pointeur](#rconc-data-by-value)
* [CP.32 : Pour partager la propriété entre des `thread` non liés, utilisez `shared_ptr`](#rconc-shared)
* [CP.40 : Minimiser les changements de contexte](#rconc-switch)
* [CP.41 : Minimiser la création et la destruction de threads](#rconc-create)
* [CP.42 : Ne pas attendre sans condition](#rconc-wait)
* [CP.43 : Minimiser le temps passé dans une section critique](#rconc-time)
* [CP.44 : N’oubliez pas de nommer vos `lock_guard` et `unique_lock`](#rconc-name)
* [CP.50 : Définir un `mutex` avec les données qu’il protège. Utiliser `synchronized_value<T>` quand c'est possible](#rconc-mutex)
* ***??? Quand utiliser un spinlock***  
* ***??? Quand utiliser `try_lock()`***  
* ***??? Quand privilégier `lock_guard` à `unique_lock`***  
* ***??? Multiplexage temporel***  
* ***??? Comment/quoi utiliser `new thread`***  

### <a name="rconc-raii"></a>CP.20 : Utilisez RAII, jamais `lock()`/`unlock()`

#### Raison

Évite les erreurs désastreuses dues à des verrous non libérés.

#### Exemple, mauvais

    mutex mtx;

    void do_stuff()
    {
        mtx.lock();
        // ... faire du travail ...
        mtx.unlock();
    }

Bientôt ou tard, quelqu’un oubliera l’appel à `mtx.unlock()`, mettra un `return` dans le corps, déclenchera une exception ou autre.

    mutex mtx;

    void do_stuff()
    {
        unique_lock<mutex> lck {mtx};
        // ... faire du travail ...
    }

#### Application

Marquer les appels aux méthodes `lock()` et `unlock()` de membres.  ???  

### <a name="rconc-lock"></a>CP.21 : Utilisez `std::lock()` ou `std::scoped_lock` pour acquérir plusieurs `mutex`

#### Raison

Évite les blocages (deadlocks) sur plusieurs `mutex`.

#### Exemple

Cela entraîne un blocage :

    // thread 1
    lock_guard<mutex> lck1(m1);
    lock_guard<mutex> lck2(m2);

    // thread 2
    lock_guard<mutex> lck2(m2);
    lock_guard<mutex> lck1(m1);

À la place, utilisez `lock()` :

    // thread 1
    lock(m1, m2);
    lock_guard<mutex> lck1(m1, adopt_lock);
    lock_guard<mutex> lck2(m2, adopt_lock);

    // thread 2
    lock(m2, m1);
    lock_guard<mutex> lck2(m2, adopt_lock);
    lock_guard<mutex> lck1(m1, adopt_lock);

ou (meilleur, mais uniquement en C++17) :

    // thread 1
    scoped_lock<mutex, mutex> lck1(m1, m2);

    // thread 2
    scoped_lock<mutex, mutex> lck2(m2, m1);

Ici, les rédacteurs des threads 1 et 2 ne parviennent pas à s’accorder sur l’ordre des `mutex`, mais l’ordre n’a plus d’importance.

#### Note

Dans du code réel, les `mutex` sont rarement nommés de manière à rappeler facilement l’utilisateur la relation attendue et l’ordre d’acquisition souhaité. Dans du code réel, les `mutex` ne sont pas toujours acquis sur des lignes consécutives.

#### Note

En C++17 il est possible d’écrire simplement

    lock_guard lck1(m1, adopt_lock);

et que le type du `mutex` soit déduit.

#### Application

Détecter les acquisitions de plusieurs `mutex`. Cela est indécidable en général, mais attraper les exemples simples courants (comme celui‑ci) est facile.

### <a name="rconc-unknown"></a>CP.22 : N’appelons jamais de code inconnu tout en tenant un verrou (ex. un rappel)

#### Raison

Si vous ne savez pas ce qu’un morceau de code fait, vous courrez un risque de blocage.

#### Exemple

    void do_this(Foo* p)
    {
        lock_guard<mutex> lck {my_mutex};
        // ... faire quelque chose ...
        p->act(my_data);
        // ...
    }

Si vous ne savez pas ce que fait `Foo::act` (peut-être qu’il s’agit d’une fonction virtuelle invoquant un membre d’une classe dérivée non encore écrite), il peut appeler `do_this` (récursivement) et provoquer un blocage sur `my_mutex`. Il peut aussi verrouiller un autre `mutex` et ne pas retourner dans un délai raisonnable, provoquant des retards pour tout code appelant `do_this`.

#### Exemple

Un exemple courant du problème « appel de code inconnu » est un appel à une fonction qui tente de gagner l’accès verrouillé au même objet. Ce problème peut souvent être résolu en utilisant un `recursive_mutex`. Par exemple :

    recursive_mutex my_mutex;

    template<typename Action>
    void do_something(Action f)
    {
        unique_lock<recursive_mutex> lck {my_mutex};
        // ... faire quelque chose ...
        f(this);    // f fera quelque chose sur *this
        // ...
    }

Si, comme il est probable, `f()` invoque des opérations sur `*this`, nous devons nous assurer que l’invariant de l’objet est maintenu avant l’appel.

#### Application

* Flag appeler une fonction virtuelle avec un `mutex` non récursif tenu  
* Flag appeler un rappel avec un `mutex` non récursif tenu  

### <a name="rconc-join"></a>CP.23 : Considérez un `thread` qui joint comme un conteneur de portée

#### Raison

Afin de maintenir la sécurité de pointeur et d’éviter les fuites, il faut prendre en compte les pointeurs utilisés par un `thread`. Si un `thread` joint, nous pouvons passer en toute sécurité des pointeurs vers des objets du cadre du `thread` et de ses cadres enveloppants.

#### Exemple

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

Un `gsl::joining_thread` est un `std::thread` dont le destructeur effectue un `join()` et qui ne peut pas être `detach()`. Par « OK » nous entendons que l’objet sera dans le scope ("vivant") aussi longtemps qu’un `thread` peut utiliser le pointeur. Le fait que les `thread`s fonctionnent en concurrence n’affecte pas la durée de vie ou les questions de propriété ici ; ces `thread`s peuvent être vus simplement comme un objet fonction appelé depuis `some_fct`.

#### Application

S’assurer que les `joining_thread` ne `detach()` pas. Après cela, les règles habituelles de durée de vie et d’exploitation (pour les objets locaux) s’appliquent.

### <a name="rconc-detach"></a>CP.24 : Considérez un `thread` comme un conteneur global

#### Raison

Afin de maintenir la sécurité de pointeur et d’éviter les fuites, il faut prendre en compte les pointeurs utilisés par un `thread`. Si un `thread` est détaché, nous pouvons passer en toute sécurité des pointeurs vers les objets statiques et du tas (seulement).

#### Exemple

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

Par « OK » nous entendons que l’objet sera dans le scope ("vivant") aussi longtemps qu’un `thread` peut utiliser les pointeurs. Par « mauvais » nous entendons qu’un `thread` peut utiliser un pointeur après la destruction de l’objet pointé. Le fait que les `thread`s fonctionnent en concurrence n’affecte pas les problèmes de durée de vie ou de propriété ; ces `thread`s peuvent être vus simplement comme un objet fonction appelé depuis `some_fct`.

#### Note

Même les objets de durée de stockage statique peuvent poser problème s’ils sont utilisés par des `thread` détachés : si le thread continue jusqu’à la fin du programme, il peut s’exécuter simultanément avec la destruction des objets de stockage statique, et donc des accès à ces objets peuvent se produire en concurrence.

#### Note

Cette règle est redondante si vous ne `detach()` pas et utilisez `gsl::joining_thread`. Cependant, convertir le code pour suivre ces lignes directrices peut être difficile et même impossible pour les bibliothèques tierces. Dans de tels cas, la règle devient essentielle pour la sécurité de la durée de vie et de la sécurité du type.

En général, il est indécidable si un `detach()` est exécuté pour un `thread`, mais les cas simples sont faciles à détecter. Si nous ne pouvons pas prouver qu’un `thread` ne `detach()`, nous devons supposer qu’il le fait et qu’il dépasse le scope dans lequel il a été construit ; après cela, les règles habituelles de durée de vie et d’exploitation (pour les objets globaux) s’appliquent.

#### Application

Flag les tentatives de passer des variables locales à un thread qui pourrait `detach()`.

### <a name="rconc-joining_thread"></a>CP.25 : Préférez `gsl::joining_thread` à `std::thread`

#### Raison

Un `joining_thread` est un thread qui « join» à la fin de son scope. Les threads détachés sont difficiles à surveiller. Il est plus difficile d’assurer l’absence d’erreurs dans les threads détachés (et potentiellement détachés).

#### Exemple, mauvais

    void f() { std::cout << "Hello "; }

    struct F {
        void operator()() const { std::cout << "world "; }
    };

    int main()
    {
        std::thread t1{f};      // f() s’exécute dans un thread séparé
        std::thread t2{F()};    // F()() s’exécute dans un thread séparé
    }  // les bugs apparaissent ici

#### Exemple

    void f() { std::cout << "Hello "; }

    struct F {
        void operator()() const { std::cout << "world "; }
    };

    int main()
    {
        std::thread t1{f};      // f() s’exécute dans un thread séparé
        std::thread t2{F()};    // F()() s’exécute dans un thread séparé

        t1.join();
        t2.join();
    }  // un bug reste

#### Note

Faites des « threads immortels » des globals, placez-les dans un cadre englobant ou placez-les sur le tas plutôt que de les détacher. [Ne détachez pas](#rconc-detached_thread).

#### Note

À cause du code ancien et des bibliothèques tierces utilisant `std::thread`, cette règle peut être difficile à introduire.

#### Application

Flag les utilisations de `std::thread` :

* Suggérer l’utilisation de `gsl::joining_thread` ou `std::jthread` (C++20).
* Suggérer l’« exportation de la propriété » vers un cadre englobant si on détache.
* Avertir s’il n’est pas évident si le thread join ou detach.

### <a name="rconc-detached_thread"></a>CP.26 : Ne jamais `detach()` un thread

#### Raison

Souvent, la nécessité de dépasser le scope de création d’un thread est inhérente à la tâche du thread, mais implémenter cela via `detach` rend plus difficile la surveillance et la communication avec le thread détaché. En particulier, il est plus difficile (mais pas impossible) de s’assurer que le thread a terminé comme prévu ou vit aussi longtemps qu’attendu.

#### Exemple

    void heartbeat();

    void use()
    {
        std::thread t(heartbeat);             // ne pas joindre ; heartbeat est censé tourner pour toujours
        t.detach();
        // ...
    }

C’est une utilisation raisonnable d’un thread, pour laquelle `detach()` est commun. Il y a cependant des problèmes : comment surveiller un thread détaché pour voir s’il est toujours actif ? Quelque chose peut mal se passer avec la pulse de santé et perdre une pulse peut être très sérieux dans un système où elle est nécessaire. Donc, nous devons communiquer avec le thread de l’alarme (ex. via un flux de messages ou un événement de notification utilisant un `condition_variable`).

Une alternative, et généralement supérieure, consiste à contrôler son cycle de vie en le plaçant dans un scope hors du point de création (ou d’activation). Par exemple :

    void heartbeat();

    gsl::joining_thread t(heartbeat);             // heartbeat est censé tourner "pour toujours"

Cette alarme va (sauf erreur, problèmes matériels, etc.) tourner aussi longtemps que le programme tourne.

Parfois, il faut séparer le point de création du point de possession :

    void heartbeat();

    unique_ptr<gsl::joining_thread> tick_tock {nullptr};

    void use()
    {
        // l’alarme est censée fonctionner aussi longtemps que tick_tock vive
        tick_tock = make_unique<gsl::joining_thread>(heartbeat);
        // ...
    }

#### Application

Flag `detach()`.

### <a name="rconc-data-by-value"></a>CP.31 : Passez de petites quantités de données entre threads par valeur plutôt que par référence ou pointeur

#### Raison

Une petite quantité de données coûte moins cher à copier et à accéder qu’à la partager en utilisant un verrou quelconque. Copier donne naturellement une possession unique (simplifie le code) et élimine la possibilité de courses de données.

#### Note

Définir précisément ce que l’on considère comme « petite » est impossible.

#### Exemple

    string modify1(string);
    void modify2(string&);

    void fct(string& s)
    {
        auto res = async(modify1, s);
        async(modify2, s);
    }

L’appel de `modify1` implique la copie de deux valeurs `string`; l’appel de `modify2` ne le fait pas. En l’autre main, l’implémentation de `modify1` est exactement ce qu’on écrirait pour un code mono‑threadé, alors que l’implémentation de `modify2` devra nécessiter une forme de verrou pour éviter les courses de données. Si la chaîne est courte (disons 10 caractères), l’appel de `modify1` peut être étonnamment rapide ; essentiellement, le coût est dans le passage du thread. Si la chaîne est longue (disons 1 000 000 de caractères), copier deux fois n’est probablement pas une bonne idée.

Notez que cet argument n’a rien à voir avec `async` en tant que tel ; il s’applique également aux considérations de “passage de messages” vs “partage mémoire”.

#### Application

???. 

### <a name="rconc-shared"></a>CP.32 : Pour partager la propriété entre des `thread` non liés, utilisez `shared_ptr`

#### Raison

Si les threads sont non liés (c’est‑à‑dire, qu’ils ne sont pas connus pour être dans le même scope ou l’un dans la durée de vie de l’autre) et qu’ils ont besoin de partager de la mémoire du tas qui doit être supprimée, un `shared_ptr` (ou équivalent) est la seule façon sécurisée d’assurer la suppression appropriée.

#### Exemple

    ???

#### Note

* Un objet statique (p. ex. un global) peut être partagé car il n’est pas détenu de manière à ce qu’un thread soit responsable de sa suppression.
* Un objet alloué sur le tas qui ne doit jamais être supprimé peut être partagé.
* Un objet détenu par un thread peut être partagé en toute sécurité avec un autre tant que celui‑ci ne dépasse pas la durée de vie du premier.

#### Application

???. 

### <a name="rconc-switch"></a>CP.40 : Minimiser les changements de contexte

#### Raison

Les changements de contexte sont coûteux.

#### Exemple

    ???  

#### Application

???.  

### <a name="rconc-create"></a>CP.41 : Minimiser la création et la destruction de threads

#### Raison

Créer un thread est coûteux.

#### Exemple

    void worker(Message m)
    {
        // process
    }

    void dispatcher(istream& is)
    {
        for (Message m; is >> m; )
            run_list.push_back(new thread(worker, m));
    }

Cet exemple crée un `thread` pour chaque message, et la liste `run_list` est censée être gérée pour détruire ces tâches une fois terminées.

À la place, on pourrait avoir un ensemble de threads pré‑créés traitant les messages

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

    void workers()  // set up worker threads (specifically 4 worker threads)
    {
        joining_thread w1 {worker};
        joining_thread w2 {worker};
        joining_thread w3 {worker};
        joining_thread w4 {worker};
    }

##### Note

Si votre système dispose d’un bon pool de threads, utilisez‑le. Si votre système dispose d’une bonne queue message, utilisez‑la.

#### Application

???.  

### <a name="rconc-wait"></a>CP.42 : Ne pas attendre sans condition

#### Raison

Un `wait` sans condition peut manquer un réveil ou réveiller simplement pour constater qu’il n’y a pas de travail à faire.

#### Exemple, mauvais

    std::condition_variable cv;
    std::mutex mx;

    void thread1()
    {
        while (true) {
            // faire un peu de travail ...
            std::unique_lock<std::mutex> lock(mx);
            cv.notify_one();    // réveiller un autre thread
        }
    }

    void thread2()
    {
        while (true) {
            std::unique_lock<std::mutex> lock(mx);
            cv.wait(lock);    // peut bloquer à jamais
            // faire du travail ...
        }
    }

Ici, si un autre thread consomme la notification de `thread1`, `thread2` peut rester bloquée à jamais.

#### Exemple

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
        cond.wait(lck, [this] { return !q.empty(); });    // éviter les réveils aléatoires
        val = q.front();
        q.pop_front();
    }

Maintenant, si la queue est vide quand un thread exécutant `get()` se réveille (par ex., parce qu’un autre thread a déjà `get()` avant lui), il retombera immédiatement au sommeil, attendant.

#### Application

Marquer tous les `wait` sans conditions.

### <a name="rconc-time"></a>CP.43 : Minimiser le temps passé dans une section critique

#### Raison

Moins de temps passé avec un `mutex` pris signifie moins de chances qu’un autre `thread` doive attendre, et la suspension et la reprise de thread sont coûteuses.

#### Exemple

    void do_something() // mauvais
    {
        unique_lock<mutex> lck(my_lock);
        do0();  // préparation : besoin pas de verrou
        do1();  // transaction : besoin de verrou
        do2();  // nettoyage : besoin pas de verrou
    }

Ici, nous tenons le verrou plus longtemps que nécessaire : nous ne devrions pas l’acquérir avant qu’il soit vraiment besoin, et le libérer avant de commencer le nettoyage. Nous pourrions réécrire ceci en

    void do_something() // mauvais
    {
        do0();  // préparation : besoin pas de verrou
        my_lock.lock();
        do1();  // transaction : besoin de verrou
        my_lock.unlock();
        do2();  // nettoyage : besoin pas de verrou
    }

Cela compromet la sécurité et violerait la règle [Utiliser RAII](#rconc-raii). À la place, ajouter un bloc pour la section critique :

    void do_something() // OK
    {
        do0();  // préparation : besoin pas de verrou
        {
            unique_lock<mutex> lck(my_lock);
            do1();  // transaction : besoin de verrou
        }
        do2();  // nettoyage : besoin pas de verrou
    }

#### Application

Impossible en général. Marquer les appels “bruts” `lock()` et `unlock()`.

### <a name="rconc-name"></a>CP.44 : N’oubliez pas de nommer vos `lock_guard` et `unique_lock`

#### Raison

Un objet local sans nom est un temporaire qui sort immédiatement de portée.

#### Exemple

    // mutex globaux
    mutex m1;
    mutex m2;

    void f()
    {
        unique_lock<mutex>(m1); // (A)
        lock_guard<mutex> {m2}; // (B)
        // faire du travail dans la section critique …
    }

Cela semble innocent, mais ce n’est pas le cas. À (A), `m1` est un `unique_lock` local par défaut qui masque le `m1` global (et ne le verrouille pas). À (B) un `lock_guard` anonyme est construit et verrouille `m2`, mais sort immédiatement de portée et le déverrouille à nouveau. Pour le reste de `f()`, aucun des deux mutex n’est verrouillé.

#### Application

Marquer tous les `lock_guard` et `unique_lock` anonymes.

### <a name="rconc-mutex"></a>CP.50 : Définir un `mutex` avec les données qu’il protège. Utiliser `synchronized_value<T>` quand c'est possible

#### Raison

Il doit être évident pour le lecteur que les données sont protégées et comment. Cela diminue le risque de verrou incorrect ou de prise d’un mauvais mutex.

Utiliser un `synchronized_value<T>` garantit que les données possèdent un mutex et que le bon mutex est acquis lors de l’accès aux données. Voir la proposition WG21 (https://www.open-std.org/wg21/docs/papers/2023/p0290r4.html) d’ajout de `synchronized_value` à une future TS ou à une révision du standard C++.

#### Exemple

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

#### Application

????

## <a name="sscp-coro"></a>CP.coro : Coroutines

Cette section se concentre sur les utilisations de coroutines.

Résumé des règles sur les coroutines :

* [CP.51 : Ne pas utiliser de lambdas capturantes qui sont coroutines](#rcoro-capture)
* [CP.52 : Ne pas tenir de verrous ou autres primitives de synchronisation à travers les points de suspension](#rcoro-locks)
* [CP.53 : Les paramètres des coroutines ne doivent pas être passés par référence](#rcoro-reference-parameters)

### <a name="rcoro-capture"></a>CP.51 : Ne pas utiliser de lambdas capturantes qui sont coroutines

#### Raison

Les modèles corrects avec des lambdas normales deviennent dangereux avec des lambdas coroutines. Le pattern évident de capture de variables entraînera l’accès à une mémoire libérée après le premier point de suspension, même pour des pointeurs intelligents comptés et des types copiable.

...

#### Exemple, Méchant

    int value = get_value();
    std::shared_ptr<Foo> sharedFoo = get_foo();
    {
      const auto lambda = [value, sharedFoo]() -> std::future<void>
      {
        co_await something();
        // "sharedFoo" et "value" ont déjà été détruits
        // le pointeur "shared" n'a pas accompli quoi‑que‑ce‑soit
      };
      lambda();
    } // l’objet de clôture lambda est maintenant hors de scope

#### Exemple, Amélioré

    int value = get_value();
    std::shared_ptr<Foo> sharedFoo = get_foo();
    {
      // passer comme un paramètre par valeur plutôt que comme capture
      const auto lambda = [](auto sharedFoo, auto value) -> std::future<void>
      {
        co_await something();
        // sharedFoo et value sont toujours valides à ce point
      };
      lambda(sharedFoo, value);
    } // l'objet de clôture lambda est maintenant hors de scope

#### Exemple, Meilleur

Utiliser une fonction pour les coroutines.

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

#### Application

Marquer une lambda qui est une coroutine et possède une liste de captures non vide.

### <a name="rcoro-locks"></a>CP.52 : Ne pas tenir de verrous ou autres primitives de synchronisation à travers les points de suspension

#### Raison

Ce pattern crée un risque important de blocage. Certains types d’attente autorisent le thread courant à effectuer un travail supplémentaire jusqu’à ce que l’opération asynchrone soit terminée. Si le thread qui détient le verrou effectue un travail nécessitant le même verrou, il se retrouvera bloqué car il tente d’acquérir un verrou qu’il possède déjà.

...

#### Exemple, Méchant

    std::mutex g_lock;

    std::future<void> Class::do_something()
    {
        std::lock_guard<std::mutex> guard(g_lock);
        co_await something(); // DANGER : la coroutine suspend l’exécution tout en gardant un verrou
        co_await somethingElse();
    }

#### Exemple, Bon

    std::mutex g_lock;

    std::future<void> Class::do_something()
    {
        {
            std::lock_guard<std::mutex> guard(g_lock);
            // modifier les données protégées par le verrou
        }
        co_await something(); // OK : le verrou a été libéré avant que la coroutine ne suspend
        co_await somethingElse();
    }

#### Note

Ce pattern est aussi mauvais pour la performance. Lorsqu’un point de suspension est atteint (ex. co_await), l’exécution de la fonction courante s’arrête et d’autres codes commencent à tourner. Il peut prendre longtemps avant que la coroutine ne reprenne. Pour toute cette période, le verrou reste retenu et ne peut être acquis par d’autres threads pour travailler.

#### Application

Marquer tous les gardiens de verrou qui ne sont pas destructés avant qu’une coroutine ne suspend.

### <a name="rcoro-reference-parameters"></a>CP.53 : Les paramètres des coroutines ne doivent pas être passés par référence

#### Raison

Une fois qu’une coroutine atteint son premier point de suspension, comme `co_await`, la partie synchrone se termine. Au-delà, tout paramètre passé par référence est pendu. Toute utilisation supplémentaire est un comportement indéfini qui peut inclure l’écriture dans une mémoire libérée.

#### Exemple, Méchant

    std::future<int> Class::do_something(const std::shared_ptr<int>& input)
    {
        co_await something();

        // DANGER : la référence à input peut ne plus être valide et
        // peut être une mémoire libérée
        co_return *input + 1;
    }

#### Exemple, Bon

    std::future<int> Class::do_something(std::shared_ptr<int> input)
    {
        co_await something();
        co_return *input + 1; // input est une copie toujours valide ici
    }

#### Note

Ce problème ne s’applique pas aux paramètres par référence qui ne sont accédés qu’avant le premier point de suspension. Les changements de la coroutine peuvent ajouter ou déplacer des points de suspension qui réintroduisent cette classe d’erreur. Certains types de coroutines ont le premier point de suspension avant la première ligne de code de la coroutine, dans ce cas les paramètres par référence sont toujours dangereux. Il est plus sûr de toujours passer par valeur, puisque la copie du paramètre demeurera dans le cadre de la coroutine, à l’origine. 

#### Note

Le même danger s’applique aux paramètres de sortie.  [F.20 : Pour les valeurs “out” de sortie, préférez les valeurs de retour aux paramètres de sortie](#rf-out) @TODO-LINK décourage les paramètres de sortie. Dans les coroutines, il faut éviter totalement les paramètres de sortie.

#### Application

Marquer tous les paramètres par référence d’une coroutine.

## <a name="sscp-par"></a>CP.par : Parallélisme

Par "parallélisme" nous entendons l'exécution d'une tâche (plus ou moins) en parallèle sur beaucoup d'items de données.

Résumé des règles de parallélisme :

* ???  
* ???  
* Là où c'est approprié, privilégier les algorithmes parallèles standard.  
* Utiliser des algorithmes conçus pour le parallélisme, pas ceux qui reposent sur une dépendance linéaire inutile.  

## <a name="sscp-mess"></a>CP.mess : Passage de messages

Les facilités de la bibliothèque standard sont très bas niveau, focalisées sur le besoin de programmation critique à bas niveau avec `thread`, `mutex`, `atomic`, etc. La plupart des gens ne devraient pas travailler à ce niveau : c’est source d’erreurs et de lenteur. Si possible, utilisez une solution de haut niveau : bibliothèques de messages, algorithmes parallèles, et vectorisation. Cette section examine le passage de messages afin que le programmeur n'ait pas besoin de synchronisation explicite.

Règles de passage de messages :

* [CP.60 : Utilisez un `future` pour renvoyer une valeur d'une tâche concurrente](#rconc-future)
* [CP.61 : Utilisez `async()` pour créer des tâches concurrentes](#rconc-async)
* files d’attente de messages  
* bibliothèques de messages  

????  

### <a name="rconc-future"></a>CP.60 : Utilisez un `future` pour renvoyer une valeur d'une tâche concurrente

#### Raison

Un `future` préserve les mêmes sémantiques d’appel de fonction que les tâches asynchrones. Il n'y a pas de verrou explicite et les retours de valeur corrects et les exceptions sont gérés proprement.

#### Exemple

    ???  

#### Note

???  

#### Application

???  

### <a name="rconc-async"></a>CP.61 : Utilisez `async()` pour lancer des tâches concurrentes

#### Raison

Semblable à [R.12](#rr-immediate-alloc) (voir [R.12] (#rr-immediate-alloc) @TODO-LINK), qui vous dit d'éviter les pointeurs bruts possédants, vous devriez également éviter les threads bruts et les promesses brutes là où c'est possible. Utilisez une fonction fabriquant comme `std::async`, qui s'occupe de lancer ou réutiliser un thread sans exposer de threads à votre propre code.

#### Exemple

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
            // handle exception here
        }
    }

#### Note

Hélas, `std::async` n'est pas parfait. Par ex., il n’utilise pas de pool de threads, ce qui peut entraîner des échecs à cause de ressources épuisées, plutôt que de mettre en file d'attente vos tâches pour être exécutées plus tard. Toutefois, même si vous ne pouvez pas utiliser `std::async`, vous devriez privilégier l’écriture de votre propre fabrique retournant un `future`, plutôt que d'utiliser des `std::thread` bruts.

#### Exemple (mauvais)

Ce code montre deux façons de réussir à utiliser `std::future`, mais d'échouer à éviter la gestion brute de `std::thread`.

    void async_example()
    {
        std::promise<int> p1;
        std::future<int> f1 = p1.get_future();
        std::thread t1([p1 = std::move(p1)]() mutable {
            p1.set_value(read_value("v1.txt"));
        });
        t1.detach(); // mauvais

        std::packaged_task<int()> pt2(read_value, "v2.txt");
        std::future<int> f2 = pt2.get_future();
        std::thread(std::move(pt2)).detach();

        std::cout << f1.get() + f2.get() << '\n';
    }

#### Exemple, Bon

Cet exemple montre une façon où on peut suivre le même schéma que `std::async` dans un cadre où `std::async` est inacceptable en production.

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

Toute tâche lancée pour exécuter le code de `read_value` se cache derrière l’appel à `WorkQueue::enqueue`. Le code utilisateur ne gère que les objets `future`, jamais un `thread`, `promise` ou `packaged_task`.

#### Application

???  

## <a name="sscp-vec"></a>CP.vec : Vectorisation

La vectorisation est une technique d'exécution d'un nombre de tâches en parallèle sans introduire de synchronisation explicite. Une opération est simplement appliquée aux éléments d'une structure de données (vecteur, tableau, etc.) en parallèle. La vectorisation présente la propriété intéressante qu'elle ne nécessite souvent pas de changements non locaux d'un programme. Cependant, elle fonctionne mieux avec des structures de données simples et avec des algorithmes spécialement conçus pour l'exploiter.

### Résumé des règles de vectorisation :

* ???  
* ???  

## <a name="sscp-free"></a>CP.free : Programmation sans verrou

La synchronisation utilisant des `mutex` et des `condition_variable` peut être relativement coûteuse. De plus, elle peut entraîner des blocages (deadlock). Pour la performance et l'élimination du risque de blocage, on utilise parfois les subtils moyens low‑level « sans verrou » qui reposent sur un accès exclusif (“atomique”) à la mémoire. La programmation sans verrou est aussi utilisée pour implémenter des mécanismes de concurrence plus élevés, tels que `thread` et `mutex`.

### Résumé des règles de programmation sans verrou :

* [CP.100 : N'utilisez pas la programmation sans verrou à moins d'être absolument obligé](#rconc-lockfree)
* [CP.101 : Mistrustez votre matériel/compilateur](#rconc-distrust)
* [CP.102 : Étudiez soigneusement la littérature](#rconc-literature)
* comment utiliser les atomiques
* éviter la famine
* utiliser une structure sans verrou au lieu de crocheter l'accès spécifique
* [CP.110 : N'écrivez pas votre propre double‑checked locking pour l'initialisation](#rconc-double)
* [CP.111 : Utilisez un patron conventionnel si vous avez réellement besoin de double‑checked locking](#rconc-double-pattern)
* comment/à quel moment utiliser CAS

### <a name="rconc-lockfree"></a>CP.100 : N'utilisez pas la programmation sans verrou à moins d'être absolument obligé

#### Raison

C&#39;est sujet à la tricherie et nécessite une connaissance experte des caractéristiques du langage, de l’architecture matérielle et des structures de données.

…  

### <a name="rconc-distrust"></a>CP.101 : Mistrustez votre matériel/compilateur

…  

### <a name="rconc-literature"></a>CP.102 : Étudiez soigneusement la littérature

…  

### <a name="rconc-double"></a>CP.110 : N'écrivez pas votre propre double‑checked locking pour l'initialisation

…  

### <a name="rconc-double-pattern"></a>CP.111 : Utilisez un patron conventionnel si vous avez réellement besoin de double‑checked locking

…  

## <a name="sscp-etc"></a>CP.etc : Autres règles

Ces règles dévient d’une simple catégorisation :

* [CP.200 : Utilisez `volatile` seulement pour communiquer avec de la mémoire non‑C++](#rconc-volatile2)
* [CP.201 : ??? Signaux](#rconc-signal)

### <a name="rconc-volatile2"></a>CP.200 : Utilisez `volatile` seulement pour communiquer avec de la mémoire non‑C++

#### Raison

`volatile` est utilisé pour référencer les objets partagés avec du non‑C++ ou du matériel qui ne suit pas le modèle mémoire C++.

…  

### <a name="rconc-signal"></a>CP.201 : ??? Signaux

…  