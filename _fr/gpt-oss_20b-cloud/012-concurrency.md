# <a name="s-concurrency"></a>CP: Concurrence et parallélisme

Nous voulons souvent que nos ordinateurs effectuent de nombreuses tâches simultanément (ou du moins semblent les faire en même temps).  
Les raisons de le faire varient (par ex., attendre de nombreux événements en n'utilisant qu'un seul processeur, traiter simultanément de nombreux flux de données ou exploiter de nombreuses ressources matérielles), tout comme les bases des moyens d'exprimer la concurrence et le parallélisme.  
Ici, nous articulons des principes et des règles pour utiliser les fonctionnalités standards ISO C++ afin d'exprimer la concurrence et le parallélisme basiques.  

Les threads sont le fondement au niveau machine pour la programmation concurrente et parallèle.  
Les threads permettent d'exécuter plusieurs sections d'un programme de façon indépendante tout en partageant la même mémoire.  
La programmation concurrente est délicate, car la protection des données partagées entre les threads est plus facile à dire qu'à faire.  

Faire en sorte qu'un code existant à thread unique s'exécute de façon concurrente peut être aussi trivial qu'ajouter stratégiquement `std::async` ou `std::thread`, ou bien cela peut nécessiter une réécriture complète, selon que le code d'origine a été écrit de façon favorable aux threads.  

Les règles de concurrence / parallélisme de ce document sont conçues avec trois objectifs en tête :  

- Aider à écrire du code qui peut être utilisé dans un environnement à threads  
- Montrer des façons propres et sûres d'utiliser les primitives de threading offertes par la bibliothèque standard  
- Donner des conseils sur ce qu'il faut faire lorsque la concurrence et le parallélisme ne procurent pas les gains de performance attendus  

Il est également important de noter que la concurrence en C++ reste inachevée :  
C++11 a introduit de nombreuses primitives de base de la concurrence, que C++14 et C++17 ont améliorées, et il existe un vif intérêt pour rendre l'écriture de programmes concurrents en C++ encore plus simple.  
Nous prévoyons que certaines recommandations liées à la bibliothèque évolueront de façon significative au fil du temps.  

Cette section nécessite beaucoup de travail (évidemment).  
Veuillez noter que nous commençons par des règles destinées aux non‑experts relatifs.  
Les experts réels doivent attendre un peu ;  
les contributions sont les bienvenues, mais pensez au grand nombre de programmeurs qui peinent à rendre leurs programmes concurrents corrects et performants.  

**Résumé des règles de concurrence et de parallélisme :**  

- [CP.1 : Supposons que votre code s'exécutera dans le cadre d'un programme multi‑threadé](012-concurrency.md#rconc-multi)  
- [CP.2 : Éviter les courses de données](012-concurrency.md#rconc-races)  
- [CP.3 : Réduire le partage explicite de données modifiables](012-concurrency.md#rconc-data)  
- [CP.4 : Penser en termes de tâches plutôt que de threads](012-concurrency.md#rconc-task)  
- [CP.8 : Ne pas essayer d'utiliser volatile pour la synchronisation](012-concurrency.md#rconc-volatile)  
- [CP.9 : Quand c'est possible, utilisez des outils pour valider votre code concurrent](012-concurrency.md#rconc-tools)  

**Voir également :**  

- [CP.con : Concurrence](012-concurrency.md#sscp-con)  
- [CP.coro : Coroutines](012-concurrency.md#sscp-coro)  
- [CP.par : Parallélisme](012-concurrency.md#sscp-par)  
- [CP.mess : Passage de messages](012-concurrency.md#sscp-mess)  
- [CP.vec : Vectorisation](012-concurrency.md#sscp-vec)  
- [CP.free : Programmation sans verrou](012-concurrency.md#sscp-free)  
- [CP.etc : Etc. règles de concurrence](012-concurrency.md#sscp-etc)  

### <a name="rconc-multi"></a>CP.1 : Supposons que votre code s'exécutera dans le cadre d'un programme multi‑threadé  

##### Raison  

Il est difficile d'être certain que la concurrence n'est pas déjà utilisée ou ne le sera pas à l'avenir.  
Le code est réutilisé.  
Des bibliothèques qui n'utilisent pas de threads pourraient être utilisées par une autre partie d'un programme qui les utilise.  
Notez que cette règle s'applique de manière prioritaire au code de bibliothèque et moins prioritairement aux applications autonomes.  
Cependant, avec le temps, les fragments de code peuvent apparaître dans des endroits inattendus.  

##### Exemple, mauvais  

```
    double cached_computation(int x)
    {
        // Mauvais : ces variables statiques provoquent des courses de données dans l'utilisation multi‑threadée
        static int cached_x = 0.0;
        static double cached_result = COMPUTATION_OF_ZERO;

        if (cached_x != x) {
            cached_x = x;
            cached_result = computation(x);
        }
        return cached_result;
    }
```

Il fonctionne correctement en environnement à thread unique, mais dans un environnement multi‑threadé les deux variables statiques entraînent des courses de données et donc un comportement indéfini.  

##### Exemple, bon  

```
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
```

Ici le cache est stocké dans les données membres d'un objet `ComputationCache`, plutôt que dans un état statique partagé.  
Ce refactoring délègue essentiellement la préoccupation aux appelants : un programme à thread unique peut choisir un cache global, tandis qu'un programme multi‑threadé peut créer une instance de cache par thread ou par « contexte ».  
L'appel refactorisé n'essaie plus de contrôler l'allocation de `cached_x`.  En ce sens, c'est une application du principe de responsabilité unique.  

Dans cet exemple, le refactoring pour la sûreté des threads améliore également la réutilisabilité dans les programmes à thread unique.  
Il est facile d'imaginer un programme à thread unique voulant deux `ComputationCache` pour différents morceaux de programme, sans qu'ils ne se surécrivent.  

Il existe plusieurs autres façons d'ajouter la sûreté des threads au code écrit pour un environnement multi‑threadé standard (c'est‑à‑dire où la seule forme de concurrence est `std::thread`) :  

- Marquer les variables d'état avec `thread_local` au lieu de `static`.  
- Implémenter un contrôle de concurrence, par exemple, protéger l'accès aux deux variables statiques avec un `static std::mutex`.  
- Refuser de construire et/ou d'exécuter dans un environnement multi‑threadé.  
- Fournir deux implémentations : une pour les environnements à thread unique et une autre pour les environnements multi‑threadé.  

##### Exception  

Code qui ne s'exécute jamais dans un environnement multi‑threadé.  
Soyez prudent : il existe de nombreux exemples où un code supposé ne jamais être exécuté dans un programme multi‑threadé l'a été lorsqu'il faisait partie d'un programme multi‑threadé, souvent des années plus tard.  
Typiquement, de tels programmes entraînent un effort pénible pour éliminer les courses de données.  
Par conséquent, le code qui n'est jamais destiné à s'exécuter dans un environnement multi‑threadé doit être clairement identifié comme tel et, idéalement, doté de mécanismes de vérification à la compilation ou à l'exécution pour détecter ces bugs d'utilisation tôt.  

### <a name="rconc-races"></a>CP.2 : Éviter les courses de données  

##### Raison  

À moins que vous ne le fassiez, rien n'est garanti de fonctionner et des erreurs subtiles persistent.  

##### Remarque  

En un mot, si deux threads peuvent accéder simultanément au même objet (sans synchronisation) et qu'au moins l'un est un écrivain (effectuant une opération non‑`const`), vous avez une course de données.  
Pour plus d'informations sur la façon d'utiliser correctement la synchronisation afin d'éliminer les courses de données, veuillez consulter un bon ouvrage sur la concurrence (voir [Apprendre attentivement la littérature](012-concurrency.md#rconc-literature)).  

##### Exemple, mauvais  

```
    int get_id()
    {
      static int id = 1;
      return id++;
    }
```

L'incrément est un exemple de course de données.  Cela peut mal tourner de plusieurs façons, y compris :  

- Le thread A charge la valeur de `id`, le système d'exploitation le met hors service pendant un certain temps, pendant lequel d'autres threads créent des IDs. À la reprise du thread A, `id` est réécrit avec la valeur lue par le thread A plus un.  
- Le thread A et le thread B chargent `id` et l'incrémentent simultanément : ils obtiennent les mêmes IDs.  

Les variables statiques locales sont une source courante de courses de données.  

##### Exemple, mauvais  

```
    void f(fstream& fs, regex pattern)
    {
        array<double, max> buf;
        int sz = read_vec(fs, buf, max);            // lire de fs dans buf
        gsl::span<double> s {buf};
        // ...
        auto h1 = async([&] { sort(std::execution::par, s); });     // lancer une tâche pour trier
        // ...
        auto h2 = async([&] { return find_all(buf, sz, pattern); });   // lancer une tâche pour trouver les correspondances
        // ...
    }
```

Ici, nous avons une (nauséeuse) course de données sur les éléments de `buf` (`sort` lit et écrit).  
Toutes les courses de données sont néfastes.  
Nous avons réussi à obtenir une course de données sur des données dans la pile.  
Toutes les courses de données ne sont pas aussi faciles à repérer que celle-ci.  

##### Exemple, mauvais  

```
    // code non contrôlé par un verrou

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
```

Maintenant, un compilateur qui ne sait pas que `val` peut changer implémentera très probablement ce `switch` en utilisant une table de sauts avec cinq entrées.  
Puis, une valeur `val` hors de l'intervalle `[0..4]` provoquera un saut vers une adresse qui pourrait être n'importe où dans le programme, et l'exécution y poursuivra.  
En réalité, « tout est possible » si vous obtenez une course de données.  
En fait, cela peut être encore pire : en examinant le code généré, vous pourriez être en mesure de déterminer où le saut errou sur un valeur donnée ; cela peut être un risque de sécurité.  

##### Application  

Certaines solutions existent :  

- Éviter les données globales  
- Éviter les variables `static`  
- Utiliser davantage de types concrets sur la pile (et ne pas trop passer de pointeurs)  
- Utiliser davantage de données immuables (literals, `constexpr`, et `const`)  

Il existe d'autres moyens de réduire la probabilité de courses de données, notamment :  

- Avoir l'outil la plus récent et le plus compréhensif, ajouter un minimum.  
- Utiliser plusieurs outils pour couvrir plus de cas que l'un seul.  

### <a name="rconc-data"></a>CP.3 : Réduire le partage explicite de données modifiables  

##### Raison  

Si vous ne partagez pas de données modifiables, vous ne pouvez pas avoir de course de données.  
Moins vous partagez, moins vous avez de chances d'oublier de synchroniser l'accès (et d'obtenir des courses de données).  
Moins vous partagez, moins vous avez de chances d'attendre un verrou (et la performance peut s'améliorer).  

##### Exemple  

```
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
```

Sans ces `const`, nous devrions passer en revue chaque fonction invoquée de façon asynchrone pour détecter un potentiel problème de course de données sur `surface_readings`.  
Faire que `surface_readings` soit `const` (par rapport à cette fonction) permet de raisonner uniquement à l'aide du corps de la fonction.  

##### Remarque  

Les données immuables peuvent être partagées de façon sûre et efficace.  
Aucun verrouillage n'est nécessaire : vous ne pouvez pas avoir de course de données sur une constante.  
Voir également [CP.mess : Passage de messages](012-concurrency.md#sscp-mess) et [CP.31 : privilégier le passage par valeur](012-concurrency.md#rconc-data-by-value).  

##### Application  

???  

### <a name="rconc-task"></a>CP.4 : Penser en termes de tâches plutôt que de threads  

##### Raison  

Un `thread` est un concept d'implémentation, une manière de penser la machine.  
Une tâche est un concept d'application, quelque chose que vous souhaitez faire, de préférence en même temps que d'autres tâches.  
Les concepts d'application sont plus simples à raisonner.  

##### Exemple  

```
    void some_fun(const std::string& msg)
    {
        std::thread publisher([=] { std::cout << msg; });      // Mauvais : moins expressif
                                                               //      et plus source d'erreur
        auto pubtask = std::async([=] { std::cout << msg; });  // OK
        // ...
        publisher.join();
    }
```

##### Remarque  

À l'exception d'`async()`, les facilities de la bibliothèque standard sont de bas niveau, orientées machine, au niveau des threads et des locks.  
Il s'agit d'un fondement nécessaire, mais nous devons essayer d'élever le niveau d'abstraction : pour la productivité, la fiabilité, et la performance.  
C'est un argument fort en faveur d'utiliser des bibliothèques plus haut niveau, libres de dépendances à la bibliothèque standard, si possible, construit sur ces facilities.  

##### Application  

???  

### <a name="rconc-volatile"></a>CP.8 : Ne pas essayer d'utiliser volatile pour la synchronisation  

##### Raison  

En C++, contrairement à certains autres langages, `volatile` ne fournit pas d'atomicité, ne synchronise pas entre threads, et ne prévient pas le réordonnancement des instructions (ni le compilateur, ni le matériel).  
Il n'a tout simplement rien à voir avec la concurrence.  

##### Exemple, mauvais  

```
    int free_slots = max_slots; // source courante de mémoire pour les objets

    Pool* use()
    {
        if (int n = free_slots--) return &pool[n];
    }
```

Ici un problème : ce code est parfaitement correct dans un programme à thread unique, mais si deux threads l'exécutent, il y a une condition de course sur `free_slots`, de sorte que deux threads peuvent obtenir la même valeur et libérer `free_slots`.  
Ceci est (évidemment) une mauvaise race de données, donc les personnes formées sur d'autres langages essayeront de le corriger ainsi :  

```
    volatile int free_slots = max_slots; // source courante de mémoire pour les objets

    Pool* use()
    {
        if (int n = free_slots--) return &pool[n];
    }
```

Il n'y a pas d'effet sur la synchronisation : la course de données persiste !  

Le mécanisme C++ pour ce besoin est `atomic` :  

```
    atomic<int> free_slots = max_slots; // source courante de mémoire pour les objets

    Pool* use()
    {
        if (int n = free_slots--) return &pool[n];
    }
```

Maintenant l'opération `--` est atomique, plutôt qu'une séquence lecture-incrément-écriture où un autre thread peut interférer.  

##### Alternative  

Utilisez des types atomiques quand vous auriez pu utiliser `volatile` dans un autre langage.  
Utilisez un mutex pour des exemples plus complexes.  

##### Voir également  

[(rare) utilisations appropriées de `volatile`](012-concurrency.md#rconc-volatile2)  

### <a name="rconc-tools"></a>CP.9 : Quand c'est possible, utilisez des outils pour valider votre code concurrent  

Expérience montre que le code concurrent est exceptionnellement difficile à mettre au point correctement, et qu'un contrôle à la compilation, des vérifications à l'exécution, et les tests sont moins efficaces pour détecter les erreurs de concurrence que les erreurs de code séquentiel.  
Les erreurs de concurrence subtiles peuvent avoir des effets dramatiques, notamment corruption mémoire, interblocages, et vulnérabilités de sécurité.  

##### Exemple  

??  

##### Remarque  

La sûreté des threads est difficile : elle surpasse souvent le programmeur expérimenté ; l'outillage est une stratégie clé pour mitiger ces risques.  
Il existe de nombreux outils « out there », à la fois commerciaux et open-source, de recherche et de production.  
Malheureusement, les besoins et restrictions de chacun diffèrent tellement que nous ne pouvons pas faire de recommandations spécifiques, mais nous pouvons mentionner :  

- Outils d'enforcement statique : **clang** (https://clang.llvm.org/docs/ThreadSafetyAnalysis.html) et certaines versions plus anciennes de **GCC** (https://gcc.gnu.org/wiki/ThreadSafetyAnnotation) offrent une prise en charge de l'annotation statique de propriétés de sécurité des threads.  
  Une utilisation cohérente de cette technique transforme de nombreuses classes d'erreurs de sécurité des threads en erreurs à la compilation.  
  Les annotations sont généralement locales (marquer un membre de données particulier, protégé par un mutex particulier), et sont généralement faciles à apprendre.  
  Comme beaucoup d'outils statiques, ils peuvent présenter des faux négatifs ; les cas qui auraient dû être détectés sont parfois autorisés.  

- Outils d'enforcement dynamique : **Thread Sanitizer** de Clang est un exemple puissant : il modifie la construction et l'exécution de votre programme pour ajouter un suivi de l'accès mémoire, identifiant absolument les courses de données dans une exécution donnée.  
  Le coût de cette solution est à la fois mémoire (5‑10× dans la plupart des cas) et temps CPU (2‑20×).  
  Les outils dynamiques comme ça sont les meilleurs lorsqu'ils sont appliqués à des tests d'intégration, des poussées de canary, ou à des tests unitaires opérant sur plusieurs threads.  
  La charge dépend de la charge : quand **TSAN** signale un problème, il s'agit toujours d'une vraie course de données ; mais il ne peut détecter que les courses de données vues dans une exécution donnée.  

- Utiliser plusieurs outils peut attraper plus de problèmes qu'un seul.  

##### Application  

Il appartient à l'éditeur d'application de choisir quels outils de soutien sont utiles pour une application particulière.  

## <a name="sscp-con"></a>CP.con : Concurrence  

Cette section se concentre sur des utilisations relativement ad-hoc de plusieurs threads communiquant via des données partagées.  

- Pour les algorithmes parallèles, voir [Parallélisme](012-concurrency.md#sscp-par)  
- Pour la communication inter‑tâches sans partage explicite, voir [Passage de messages](012-concurrency.md#sscp-mess)  
- Pour le code vectoriel parallèle, voir [Vectorisation](012-concurrency.md#sscp-vec)  
- Pour la programmation sans verrou, voir [Sans verrou](012-concurrency.md#sscp-free)  

**Résumé des règles de concurrence :**  

- [CP.20 : Utiliser RAII, jamais lock()/unlock()](012-concurrency.md#rconc-raii)  
- [CP.21 : Utiliser std::lock() ou std::scoped_lock pour acquérir plusieurs mutex](012-concurrency.md#rconc-lock)  
- [CP.22 : Ne jamais appeler du code inconnu tout en tenant un verrou (ex. rappel)](012-concurrency.md#rconc-unknown)  
- [CP.23 : Considérez un thread qui fait join comme un conteneur à portée](012-concurrency.md#rconc-join)  
- [CP.24 : Considérez un thread comme un conteneur global](012-concurrency.md#rconc-detach)  
- [CP.25 : Privilégier gsl::joining_thread sur std::thread](012-concurrency.md#rconc-joining_thread)  
- [CP.26 : Ne pas détacher un thread](012-concurrency.md#rconc-detached_thread)  
- [CP.31 : Privilégier le passage par valeur de petites quantités de données entre threads plutôt que par référence ou pointeur](012-concurrency.md#rconc-data-by-value)  
- [CP.32 : Partager la propriété entre threads non liés à l'aide de shared_ptr](012-concurrency.md#rconc-shared)  
- [CP.40 : Minimiser les changements de contexte](012-concurrency.md#rconc-switch)  
- [CP.41 : Minimiser la création et la destruction de threads](012-concurrency.md#rconc-create)  
- [CP.42 : Ne pas attendre sans condition](012-concurrency.md#rconc-wait)  
- [CP.43 : Minimiser le temps passé dans une section critique](012-concurrency.md#rconc-time)  
- [CP.44 : N'oubliez pas de nommer vos lock_guard et unique_lock](012-concurrency.md#rconc-name)  
- [CP.50 : Définir un mutex en même temps que les données qu'il protège. Utiliser synchronized_value<T> lorsque possible](012-concurrency.md#rconc-mutex)  
- **??? quand utiliser un spinlock**  
- **??? quand utiliser try_lock()**  
- **???. quand privilégier lock_guard sur unique_lock**  
- **???. multiplexer temporel**  
- **???. quand/comment utiliser new thread**  

### <a name="rconc-raii"></a>CP.20 : Utiliser RAII, jamais lock()/unlock()  

##### Raison  

Évite les erreurs désastreuses dues à des verrous non libérés.  

##### Exemple, mauvais  

```
    mutex mtx;

    void do_stuff()
    {
        mtx.lock();
        // ... faire du travail ...
        mtx.unlock();
    }
```

Mieux, une fois, quelqu'un oubliera le `mtx.unlock()`, placera un `return` dans le ... de travail, lèvera une exception, ou quelque chose.  

```
    mutex mtx;

    void do_stuff()
    {
        unique_lock<mutex> lck {mtx};
        // ... faire du travail ...
    }
```

##### Application  

Marquer les appels aux fonctions membres lock() et unlock().  ???  

### <a name="rconc-lock"></a>CP.21 : Utiliser std::lock() ou std::scoped_lock pour acquérir plusieurs mutex  

##### Raison  

Pour éviter les interblocages sur plusieurs mutex.  

##### Exemple  

Demonstrating deadlock:  

```  
    // thread 1  
    lock_guard<mutex> lck1(m1);  
    lock_guard<mutex> lck2(m2);  

    // thread 2  
    lock_guard<mutex> lck2(m2);  
    lock_guard<mutex> lck1(m1);  
```  

Utilisez plutôt :  

```
    // thread 1  
    lock(m1, m2);  
    lock_guard<mutex> lck1(m1, adopt_lock);  
    lock_guard<mutex> lck2(m2, adopt_lock);  

    // thread 2  
    lock(m2, m1);  
    lock_guard<mutex> lck2(m2, adopt_lock);  
    lock_guard<mutex> lck1(m1, adopt_lock);  
```  
ou (mieux, C++17 uniquement) :  

```
    // thread 1  
    scoped_lock<mutex, mutex> lck1(m1, m2);  

    // thread 2  
    scoped_lock<mutex, mutex> lck2(m2, m1);  
```  

Ici, les auteurs de thread1 et thread2 ne s'accordent toujours pas sur l'ordre des mutex, mais l'ordre ne compte plus.  

##### Remarque  

En code réel, les mutex sont rarement nommés de façon à rappeler à l'utilisateur l'intention et l'ordre d'acquisition.  
En code réel, les mutex ne sont pas toujours acquis sur des lignes adjacentes.  

##### Remarque  

En C++17, il est possible d'écrire plus simplement  

```
    lock_guard lck1(m1, adopt_lock);  
```  

et que le type de mutex soit déduit.  

##### Application  

Détecter l'acquisition de plusieurs mutex.  
C'est indécidable en général, mais capturer des exemples simples courants (comme ci‑dessus) est facile.  

### <a name="rconc-unknown"></a>CP.22 : Ne jamais appeler du code inconnu tout en tenant un verrou (ex. rappel)  

##### Raison  

Si vous ne savez pas ce que fait un morceau de code, vous risquez un interblocage.  

##### Exemple  

```
    void do_this(Foo* p)
    {
        lock_guard<mutex> lck {my_mutex};
        // ... faire quelque chose ...
        p->act(my_data);
        // ...
    }
```

Si vous ne savez pas ce que fait `Foo::act` (peut-être une fonction virtuelle invoquant un membre d'une classe dérivée encore à écrire), elle pourrait appeler `do_this` (récursivement) et provoquer un interblocage sur `my_mutex`.  
Peut-être verrouillera-t-elle un autre mutex et ne retournera pas dans un délai raisonnable, provoquant des retards pour tout code appelant `do_this`.  

##### Exemple  

Un exemple courant du problème « appel de code inconnu » est un appel à une fonction qui tente d'acquérir un accès verrouillé à l'objet même.  
Ce problème peut souvent être résolu en utilisant un `recursive_mutex`.  

```
    recursive_mutex my_mutex;

    template<typename Action>
    void do_something(Action f)
    {
        unique_lock<recursive_mutex> lck {my_mutex};
        // ... faire quelque chose ...
        f(this);    // f va faire quelque chose à *this
        // ...
    }
```

Si, comme il est probable, `f()` invoque des opérations sur `*this`, nous devons nous assurer que l'invariant de l'objet est maintenu avant l'appel.  

##### Application  

- Marquer l'appel d'une fonction virtuelle avec un mutex non récursif en cours de possession  
- Marquer l'appel d'un rappel avec un mutex non récursif en cours de possession  

### <a name="rconc-join"></a>CP.23 : Considérez un thread qui fait join comme un conteneur à portée  

##### Raison  

Pour maintenir la sécurité des pointeurs et éviter les fuites, nous devons considérer quels pointeurs sont utilisés par un thread.  
Si un thread fait join, nous pouvons transmettre en toute sécurité des pointeurs vers des objets dans le domaine de portée du thread et de son domaine englobant.  

##### Exemple  

```
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
```

Un `gsl::joining_thread` est un `std::thread` avec un destructeur qui fait join et qui ne peut pas être `detached()`.  
Par « OK » nous entendons que l'objet restera dans l'état « vivant » le temps qu'un thread puisse en utiliser le pointeur.  
Le fait que les threads s'exécutent en même temps n'affecte pas les problèmes de durée de vie ni de possession ; ces threads peuvent être vus comme un simple objet fonctionnel appelé depuis `some_fct`.  

##### Application  

Assurez que les `joining_thread` ne se détachent pas.  
Après cela, les règles habituelles concernant la durée de vie et la possession (pour les objets locaux) s'appliquent.  

### <a name="rconc-detach"></a>CP.24 : Considérez un thread comme un conteneur global  

##### Raison  

Pour maintenir la sécurité des pointeurs et éviter les fuites, nous devons considérer quels pointeurs sont utilisés par un thread.  
Si un thread est détaché, nous pouvons transmettre en toute sécurité des pointeurs vers des objets statiques et de la zone d'allocation dynamique (seulement).  

##### Exemple  

```
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
```

Par « OK » nous entendons que l'objet restera dans l'état « vivant » le temps qu'un thread puisse en utiliser le pointeur.  
Par « mauvais » nous entendons qu'un thread peut utiliser un pointeur après que l'objet pointé a été détruit.  
Le fait que les threads s'exécutent en même temps n'affecte pas les problèmes de durée de vie ou de possession ; ces threads peuvent être vus comme un simple objet fonctionnel appelé depuis `some_fct`.  

##### Remarque  

Même les objets à durée de stockage statique peuvent poser problème lorsqu'ils sont utilisés depuis des threads détachés : si le thread continue jusqu'à la fin du programme, il peut fonctionner en simultané avec la destruction d'objets à durée statique, et ainsi les accès à ces objets peuvent être en course.  

##### Remarque  

Cette règle est redondante si vous ne `detach()` ni n'utilisez `gsl::joining_thread`.  
Cependant, convertir du code pour suivre ces lignes directrices peut être difficile et même impossible pour les bibliothèques tierces.  
Dans ces cas, la règle devient essentielle pour la sécurité de la durée de vie et de la sécurité de type.  

En général, il est indécidable de savoir si un `detach()` est exécuté pour un thread, mais les cas simples courants sont faciles à détecter.  
S'il n'est pas possible de prouver qu'un thread ne se détache pas, nous devons supposer qu'il le fait et qu'il survit au-delà du cadre où il a été construit ; après cela, les règles habituelles de durée de vie et de possession (pour les objets globaux) s'appliquent.  

##### Application  

Marquer les tentatives de passer des variables locales à un thread qui pourrait se détacher.  

### <a name="rconc-joining_thread"></a>CP.25 : Privilégier gsl::joining_thread sur std::thread  

##### Raison  

Un `joining_thread` est un thread qui fait join à la fin de son domaine.  
Les threads détachés sont difficiles à surveiller.  
Il est plus ardu de garantir l'absence d'erreurs dans les threads détachés (et potentiellement détachés).  

##### Exemple, mauvais  

```
    void f() { std::cout << "Hello "; }

    struct F {
        void operator()() const { std::cout << "parallel world "; }
    };

    int main()
    {
        std::thread t1{f};      // f() s'exécute dans un thread séparé
        std::thread t2{F()};    // F() s'exécute dans un thread séparé
    }  // repérez les bugs
```

##### Exemple  

```
    void f() { std::cout << "Hello "; }

    struct F {
        void operator()() const { std::cout << "parallel world "; }
    };

    int main()
    {
        std::thread t1{f};      // f() s'exécute dans un thread séparé
        std::thread t2{F()};    // F() s'exécute dans un thread séparé

        t1.join();
        t2.join();
    }  // un seul bug restant
```

##### Remarque  

Faites « threads immortels » globaux, les placer dans un contenant englobant, ou les placer sur la zone d'allocation dynamique plutôt qu'en les détachant.  
[Ne pas détacher](012-concurrency.md#rconc-detached_thread).  

##### Remarque  

À cause de code ancien et des bibliothèques tierces qui utilisent `std::thread`, cette règle peut être difficile à introduire.  

##### Application  

Marquer les utilisations de `std::thread` :  

- Suggérer l'usage de `gsl::joining_thread` ou `std::jthread` de C++20.  
- Suggérer l'« exportation de la possession » vers un domaine englobant si le thread se détache.  
- Prévenir le cas où il n'est pas évident qu'un thread fait join ou se détache.  

### <a name="rconc-detached_thread"></a>CP.26 : Ne pas détacher un thread  

##### Raison  

Souvent, le besoin de survivre au-delà du cadre de création d'un thread est inhérent à la tâche du thread, mais l'implémentation de cette idée par `detach` rend plus difficile la surveillance et la communication avec le thread détaché.  
En particulier, il est plus difficile (mais pas impossible) de s'assurer que le thread a terminé comme prévu ou vit aussi longtemps que prévu.  

##### Exemple  

```
    void heartbeat();

    void use()
    {
        std::thread t(heartbeat);             // ne joignez pas ; heartbeat est censé fonctionner indéfiniment
        t.detach();
        // ...
    }
```

C'est un usage raisonnable d'un thread, pour lequel `detach()` est couramment utilisé.  
Il y a des problèmes : comment surveiller le thread détaché pour voir s'il est encore actif ? Quelque chose peut mal se passer avec le heartbeat, et perdre un heartbeat peut être très grave dans un système qui en a besoin.  
Nous devons donc communiquer avec le thread de heartbeat (ex., via un flux de messages ou des événements de notification en utilisant un `condition_variable`).  

Une solution alternative, et en général supérieure, est de contrôler sa durée de vie en le plaçant dans un cadre extérieur à son point de création (ou d'activation).  
Par exemple :  

```
    void heartbeat();

    gsl::joining_thread t(heartbeat);             // heartbeat est censé fonctionner « indéfiniment »

```

Ce heartbeat fonctionnera (sauf erreur, problèmes matériels, etc.) aussi longtemps que le programme tourne.  

Parfois, nous devons séparer le point de création de celui d'occupation :  

```
    void heartbeat();

    unique_ptr<gsl::joining_thread> tick_tock {nullptr};

    void use()
    {
        // heartbeat est censé fonctionner tant que tick_tock vit
        tick_tock = make_unique<gsl::joining_thread>(heartbeat);
        // ...
    }
```

#### Application  

Marquer `detach()`.  

### <a name="rconc-data-by-value"></a>CP.31 : Privilégier le passage par valeur de petites quantités de données entre threads plutôt que par référence ou pointeur  

##### Raison  

Peu de données sont moins chers à copier et à accéder que de les partager en utilisant un mécanisme de verrou.  
Copier donne naturellement une propriété unique (simplifie le code) et élimine la possibilité de courses de données.  

##### Remarque  

Définir exactement ce qu'est « petite quantité » est impossible.  

##### Exemple  

```
    string modify1(string);
    void modify2(string&);

    void fct(string& s)
    {
        auto res = async(modify1, s);
        async(modify2, s);
    }
```

L'appel à `modify1` implique deux copies de `string`, tandis que l'appel à `modify2` n'en implique aucune.  
Par ailleurs, la mise en œuvre de `modify1` est exactement ce que nous aurions écrit pour un code à thread unique, tandis que la mise en œuvre de `modify2` devra probablement inclure une forme de verrouillage pour éviter les courses de données.  
Si la chaîne est courte (ex. 10 caractères), l'appel à `modify1` peut être étonnamment rapide ; essentiellement, tout le coût est dans le changement de thread.  
Si la chaîne est longue (ex. 1 000 000 caractères), copier deux fois elle n'est probablement pas une bonne idée.  

Notez que cet argument n'a rien à voir avec `async` à proprement parler ; il s'applique également aux considérations de micro‑service plutôt que de mémoire partagée.  

##### Application  

???  

### <a name="rconc-shared"></a>CP.32 : Partager la propriété entre threads non liés à l'aide de shared_ptr  

##### Raison  

Si les threads sont indépendants (c.-à-d. non connus pour être dans le même cadre de portée ou l'un dans la durée de vie de l'autre) et ils doivent partager de la mémoire dynamique qui doit être libérée, un `shared_ptr` (ou équivalent) est le seul moyen sûr d'assurer une suppression correcte.  

##### Exemple  

???  

##### Remarque  

- Un objet statique (ex. un global) peut être partagé car il n'est pas « propriétaire » dans le sens où un thread est responsable de sa suppression.  
- Un objet sur la zone d'allocation dynamique qui n'est jamais censé être supprimé peut être partagé.  
- Un objet appartenant à un thread peut être partagé en toute sécurité avec un autre thread tant que le deuxième thread ne survit pas au propriétaire.  

##### Application  

???  

### <a name="rconc-switch"></a>CP.40 : Minimiser les changements de contexte  

##### Raison  

Les changements de contexte sont coûteux.  

##### Exemple  

??  

##### Application  

??  

### <a name="rconc-create"></a>CP.41 : Minimiser la création et la destruction de threads  

##### Raison  

La création de thread est coûteuse.  

##### Exemple  

```
    void worker(Message m)
    {
        // traiter
    }

    void dispatcher(istream& is)
    {
        for (Message m; is >> m; )
            run_list.push_back(new thread(worker, m));
    }
```

Cette approche crée un thread par message, et `run_list` est, on l'imagine, gérée pour détruire ces tâches une fois terminées.  

À la place, nous pourrions avoir un ensemble de threads de travail pré‑créés traitant les messages :  

```
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

    void workers()  // mettre en place les threads de travail (4 workers spécifiquement)
    {
        joining_thread w1 {worker};
        joining_thread w2 {worker};
        joining_thread w3 {worker};
        joining_thread w4 {worker};
    }
```

##### Remarque  

Si votre système possède un bon pool de threads, utilisez-le.  
Si votre système possède une bonne file de messages, utilisez-la.  

##### Application  

??  

### <a name="rconc-wait"></a>CP.42 : Ne pas attendre sans condition  

##### Raison  

Un `wait` sans condition peut manquer un réveil ou se réveiller simplement pour découvrir qu'il n'y a pas de travail à faire.  

##### Exemple, mauvais  

```
    std::condition_variable cv;
    std::mutex mx;

    void thread1()
    {
        while (true) {
            // faire du travail ...
            std::unique_lock<std::mutex> lock(mx);
            cv.notify_one();    // réveiller l'autre thread
        }
    }

    void thread2()
    {
        while (true) {
            std::unique_lock<std::mutex> lock(mx);
            cv.wait(lock);    // peut bloquer pour toujours
            // faire le travail ...
        }
    }
```

Ici si un autre thread consomme la notification de `thread1`, `thread2` peut attendre à jamais.  

##### Exemple  

```
    template<typename T>
    class Sync_queue {
    public:
        void put(const T& val);
        void put(T&& val);
        void get(T& val);
    private:
        mutex mtx;
        condition_variable cond;    // contrôle l'accès
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
        cond.wait(lck, [this] { return !q.empty(); });    // éviter les réveils faux
        val = q.front();
        q.pop_front();
    }
```

Maintenant si la file est vide quand un thread exécutant `get()` se réveille (ex. parce qu'un autre thread a déjà accédé `get()` avant lui), il rentre immédiatement en sommeil.  

##### Application  

Marquer tous les `wait` sans conditions.  

### <a name="rconc-time"></a>CP.43 : Minimiser le temps passé dans une section critique  

##### Raison  

Moins de temps en possession d'un mutex signifie moins de chances qu'un autre thread attende, et la suspension et la reprise de threads sont coûteuses.  

##### Exemple  

```
    void do_something() // mauvais
    {
        unique_lock<mutex> lck(my_lock);
        do0();  // préparation : ne nécessite pas de verrou
        do1();  // transaction : nécessite verrou
        do2();  // nettoyage : ne nécessite pas de verrou
    }
```

Ici, nous tenons le lock un peu plus longtemps que nécessaire : nous ne devrions pas avoir pris le lock avant d'en avoir besoin et devrions le libérer avant de commencer le nettoyage.  
Nous pourrions réécrire ceci :  

```
    void do_something() // mauvais
    {
        do0();  // préparation : ne nécessite pas de verrou
        my_lock.lock();
        do1();  // transaction : nécessite verrou
        my_lock.unlock();
        do2();  // nettoyage : ne nécessite pas de verrou
    }
```

Mais cela compromet la sécurité et viole la règle [Utiliser RAII](012-concurrency.md#rconc-raii).  
À la place, ajouter un bloc pour la section critique :  

```
    void do_something() // OK
    {
        do0();  // préparation : ne nécessite pas de verrou
        {
            unique_lock<mutex> lck(my_lock);
            do1();  // transaction : nécessite verrou
        }
        do2();  // nettoyage : ne nécessite pas de verrou
    }
```

##### Application  

Imprévisible en général.  
Marquer les `lock()` et `unlock()` « naked ».  

### <a name="rconc-name"></a>CP.44 : N'oubliez pas de nommer vos lock_guard et unique_lock  

##### Raison  

Un objet local anonyme est un temporaire qui sort immédiatement de portée.  

##### Exemple  

```
    // mutex globaux
    mutex m1;
    mutex m2;

    void f()
    {
        unique_lock<mutex>(m1); // (A)
        lock_guard<mutex> {m2}; // (B)
        // faire le travail dans la section critique …
    }
```

Ceci est à première vue innocent, mais ce n'est pas le cas.  
À (A), `m1` est un `unique_lock` local par défaut qui shadow le `::m1` global (et ne le verrouille pas).  
À (B), un `lock_guard` temporaire est construit et verrouille `::m2`, mais se libère immédiatement.  
Le reste de la fonction `f()` n'a aucun mutex verrouillé.  

##### Application  

Marquer tous les `lock_guard` et `unique_lock` anonymes.  

### <a name="rconc-mutex"></a>CP.50 : Définir un mutex en même temps que les données qu'il protège. Utiliser synchronized_value<T> lorsque possible  

##### Raison  

Il doit être clair pour le lecteur que les données sont à protéger et comment.  
Cela réduit la probabilité de verrouiller le mauvais mutex, ou de ne pas verrouiller du tout.  
Utiliser `synchronized_value<T>` garantit qu'il y a un mutex et qu'il est verrouillé lorsqu'on accède aux données.  
Voir la proposition [WG21 p0290r4](https://www.open-std.org/jtc1/sc22/wg21/docs/papers/2023/p0290r4.html) pour ajouter `synchronized_value` à un TS ou révision future du standard C++.  

##### Exemple  

```
    struct Record {
        std::mutex m;   // verrouiller avant d'accéder aux autres membres
        // ...
    };

    class MyClass {
        struct DataRecord {
           // ...
        };
        synchronized_value<DataRecord> data; // Protéger les données avec un mutex
    };
```

##### Application  

???  

## <a name="sscp-coro"></a>CP.coro : Coroutines  

Cette section se concentre sur les utilisations de coroutines.  

**Résumé des règles de coroutines :**  

- [CP.51 : Ne pas utiliser de lambdas capturant qui sont des coroutines](012-concurrency.md#rcoro-capture)  
- [CP.52 : Ne pas tenir de locks ou d'autres primitives de synchronisation à travers les points de suspension](012-concurrency.md#rcoro-locks)  
- [CP.53 : Les paramètres aux coroutines ne doivent pas être passés par référence](012-concurrency.md#rcoro-reference-parameters)  

### <a name="rcoro-capture"></a>CP.51 : Ne pas utiliser de lambdas capturant qui sont des coroutines  

##### Raison  

Les schémas corrects avec des lambdas normales sont dangereux avec des lambdas coroutines.  
Une capture de variable entraînera un accès à de la mémoire libérée après le premier point de suspension, même pour des pointeurs gérés par référence et des types copiable.  

##### Exemple, Mauvais  

```
    int value = get_value();
    std::shared_ptr<Foo> sharedFoo = get_foo();
    {
      const auto lambda = [value, sharedFoo]() -> std::future<void>
      {
        co_await something();
        // "sharedFoo" and "value" have already been destroyed
        // the "shared" pointer didn't accomplish anything
      };
      lambda();
    } // the lambda closure object has now gone out of scope
```

##### Exemple, Meilleur  

```
    int value = get_value();
    std::shared_ptr<Foo> sharedFoo = get_foo();
    {
      // take as by-value parameter instead of as a capture
      const auto lambda = [](auto sharedFoo, auto value) -> std::future<void>
      {
        co_await something();
        // sharedFoo and value are still valid at this point
      };
      lambda(sharedFoo, value);
    } // the lambda closure object has now gone out of scope
```

##### Exemple, Meilleur  

```
    std::future<void> Class::do_something(int value, std::shared_ptr<Foo> sharedFoo)
    {
      co_await something();
      // sharedFoo and value are still valid at this point
    }

    void SomeOtherFunction()
    {
      int value = get_value();
      std::shared_ptr<Foo> sharedFoo = get_foo();
      do_something(value, sharedFoo);
    }
```

##### Application  

Marquer une lambda qui est une coroutine et qui a une liste de captures non vide.  

### <a name="rcoro-locks"></a>CP.52 : Ne pas tenir de locks ou d'autres primitives de synchronisation à travers les points de suspension  

##### Raison  

Ce schéma crée un risque important d'interblocages.  
Certaines formes d'attente laisseront le thread actuel faire d'autres travaux jusqu'à ce que l'opération asynchrone soit terminée.  
Si le thread qui détient le verrou effectue un travail nécessitant le même verrou, cela entraînera un interblocage, car il essaie d'acquérir un verrou qu'il détient déjà.  

S'il le coroutine se termine sur un thread différent de celui qui a acquis le verrou, c'est un comportement indéfini.  
Même avec un retour explicite au thread d'origine, une exception peut être levée avant la reprise de la coroutine et le verrou ne sera pas détruit.  

##### Exemple, Mauvais  

```
    std::mutex g_lock;

    std::future<void> Class::do_something()
    {
        std::lock_guard<std::mutex> guard(g_lock);
        co_await something(); // DANGEREUX : la coroutine a suspendu tout en tenant un verrou
        co_await somethingElse();
    }
```

##### Exemple, Bon  

```
    std::mutex g_lock;

    std::future<void> Class::do_something()
    {
        {
            std::lock_guard<std::mutex> guard(g_lock);
            // modifier les données protégées par le verrou
        }
        co_await something(); // OK : le verrou est libéré avant la suspension
        co_await somethingElse();
    }
```

##### Remarque  

Ce schéma est aussi mauvais pour la performance. Lorsqu'un point de suspension est atteint (telle qu'un `co_await`), l'exécution de la fonction courante s'arrête, et d'autres code commence à s'exécuter.  
Il peut passer un long moment avant que la coroutine ne reprenne.  
Pendant toute cette durée, le verrou reste bloqué et ne peut pas être pris par d'autres threads pour faire du travail.  

##### Application  

Marquer tous les garde-guard qui ne sont pas détruits avant qu'une coroutine ne suspend.  

### <a name="rcoro-reference-parameters"></a>CP.53 : Les paramètres aux coroutines ne doivent pas être passés par référence  

##### Raison  

Une fois qu'une coroutine atteint le premier point de suspension, comme un `co_await`, la partie synchrone renvoie.  
À partir de ce point, tout paramètre passé par référence est en train de tomber.  
Toute utilisation au-delà de ce point est un comportement indéfini qui peut inclure l'écriture dans une mémoire libérée.  

##### Exemple, Mauvais  

```
    std::future<int> Class::do_something(const std::shared_ptr<int>& input)
    {
        co_await something();

        // DANGER : la référence à input peut ne plus être valide et pointer vers de la mémoire libérée
        co_return *input + 1;
    }
```

##### Exemple, Bon  

```
    std::future<int> Class::do_something(std::shared_ptr<int> input)
    {
        co_await something();
        co_return *input + 1; // input est une copie qui est toujours valide ici
    }
```

##### Remarque  

Ce problème ne s'applique pas aux paramètres par référence qui ne sont accédés qu'avant le premier point de suspension.  
Les changements ultérieurs de la fonction peuvent ajouter ou déplacer des points de suspension qui réintroduisent cette classe de bug.  
Certaines coroutines ont un point de suspension avant la première ligne de code, auquel cas les paramètres par référence sont toujours non sûrs.  
Il est plus sûr d'utiliser toujours le passage par valeur, car le paramètre copié vivra dans le cadre de coroutine qui est sûr à accéder tout au long de la coroutine.  

##### Remarque  

Le même danger s'applique aux paramètres de sortie.  
[**F.20** : Pour les valeurs "out", privilégier les valeurs de retour aux paramètres de sortie](006-functions.md#rf-out) décourage les paramètres de sortie.  
Les coroutines doivent les éviter complètement.  

##### Application  

Marquer tous les paramètres par référence d'une coroutine.  

## <a name="sscp-par"></a>CP.par : Parallélisme  

Par "parallélisme" nous entendons l'exécution d'une tâche (plus ou moins) simultanément (« en parallèle ») sur de nombreux éléments de données.  

**Résumé des règles de parallélisme :**  

- ???  
- ???  
- Lorsque approprié, privilégier les algorithmes parallèles de la bibliothèque standard  
- Utiliser des algorithmes conçus pour le parallélisme, sans dépendance inutile à l'évaluation linéaire  

## <a name="sscp-mess"></a>CP.mess : Passage de messages  

Les facilities de la bibliothèque standard sont très bas niveau, orientés vers les besoins des programmes proches du matériel à haute prudence, utilisant `thread`, `mutex`, `atomic`, etc.  
La plupart des gens ne devraient pas travailler à ce niveau : c'est sujet aux erreurs et le développement est lent.  
Si possible, utilisez une facility plus haut niveau : bibliothèques de messaging, algorithmes parallèles, vectorisation.  
Cette section examine la façon d'envoyer des messages afin qu'un programmeur ne doive pas faire de synchronisation explicite.  

**Résumé des règles de passage de messages :**  

- [CP.60 : Utiliser un future pour retourner une valeur d'une tâche concurrente](012-concurrency.md#rconc-future)  
- [CP.61 : Utiliser async() pour déclencher des tâches concurrentes](012-concurrency.md#rconc-async)  
- files d'attente de messages  
- bibliothèques de messaging  

- ??? faut-il un « use X rather than `std::async` » où X serait une meilleure spécification d'un pool de threads ?  
- ??? Est‑-il utile d'utiliser std::async compte tenu des facilities de parallélisme existantes (future, etc.) ? Que recommander pour paralléliser, ex. `std::accumulate` (avec la précondition de commutativité), merge‑sort, etc.  

### <a name="rconc-future"></a>CP.60 : Utiliser un future pour retourner une valeur d'une tâche concurrente  

##### Raison  

Un future préserve les mêmes semantiques de retour de fonction pour les tâches asynchrones.  
Il n'y a pas de verrou explicite et le bon (valeur) ou l'erreur (exception) de retour sont gérés simplement.  

##### Exemple  

???  

##### Remarque  

???  

##### Application  

???  

### <a name="rconc-async"></a>CP.61 : Utiliser async() pour déclencher des tâches concurrentes  

##### Raison  

Similaire à [R.12](009-resource.md#rr-immediate-alloc), qui vous dit d'éviter les pointeurs gérants bruts, vous devez également éviter les threads bruts et les promises brutes lorsque c'est possible. Utilisez une fonction usine telle que `std::async`, qui gère le déclenchement ou la réutilisation d'un thread sans exposer vos propres threads.  

##### Exemple  

```
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
```

##### Remarque  

`std::async` n'est pas parfait. Par exemple, il n'utilise pas de pool de threads, ce qui signifie qu'il peut échouer en raison d'un épuisement des ressources, plutôt que de mettre les tâches en file d'attente pour être exécutées plus tard.  
Même si vous ne pouvez pas utiliser `std::async`, vous devriez aussi préférer écrire votre propre fonction qui renvoie un future, plutôt que d'utiliser des promises brutes.  

##### Exemple (mauvais)  

Cet exemple montre deux manières d'atteindre la réussite d'utiliser `std::future`, mais d'échouer d'éviter la gestion brute de `std::thread`.  

```
    void async_example()
    {
        std::promise<int> p1;
        std::future<int> f1 = p1.get_future();
        std::thread t1([p1 = std::move(p1)]() mutable {
            p1.set_value(read_value("v1.txt"));
        });
        t1.detach(); // mal

        std::packaged_task<int()> pt2(read_value, "v2.txt");
        std::future<int> f2 = pt2.get_future();
        std::thread(std::move(pt2)).detach();

        std::cout << f1.get() + f2.get() << '\n';
    }
```

##### Exemple (bon)  

Cet exemple montre une façon dont vous pourriez suivre le modèle général fourni par `std::async`, dans un contexte où `std::async` lui‑même était inacceptable en production.  

```
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
```

Toutes les threads déclenchées pour exécuter le code de `read_value` sont masquées derrière l'appel à `WorkQueue::enqueue`.  
L'utilisateur ne manipule que des objets `future`, jamais de `thread`, `promise` ou `packaged_task`.  

##### Application  

???  

## <a name="sscp-vec"></a>CP.vec : Vectorisation  

Vectorisation est une technique d'exécuter un nombre de tâches simultanément sans introduire de synchronisation explicite.  
Une opération est simplement appliquée sur des éléments d'une structure de données (vecteur, tableau, etc.) en parallèle.  
Vectorisation possède la particularité d'il n'est souvent pas nécessaire de modifier le programme de façon non locale.  
Cependant, la vectorisation fonctionne mieux avec des structures de données simples et avec des algorithmes spécifiquement conçus pour la le permettre.  

**Résumé des règles de vectorisation :**  

- ???  
- ???  

## <a name="sscp-free"></a>CP.free : Programmation sans verrou  

Synchronisation via des mutex et `condition_variable` peut être relativement coûteuse.  
De plus, elle peut conduire à des interblocages.  
Pour des performances et pour éliminer la possibilité d'interblocage, nous devons parfois utiliser les facilities « sans verrou » de bas niveau qui reposent sur un accès exclusif bref (`atomic`).  
La programmation sans verrou est aussi utilisée pour implémenter des mécanismes de concurrence plus élevés, tel que `thread`, `mutex`.  

**Résumé des règles de programmation sans verrou :**  

- [CP.100 : Ne pas utiliser la programmation sans verrou sauf si vous en avez réellement besoin](012-concurrency.md#rconc-lockfree)  
- [CP.101 : Méfiez-vous de votre combinaison matériel/compilateur](012-concurrency.md#rconc-distrust)  
- [CP.102 : Étudiez attentivement la littérature](012-concurrency.md#rconc-literature)  
- comment/ quand utiliser atomics  
- éviter la famine  
- utiliser une structure de données sans verrou plutôt que de bricoler un accès sans verrou spécifique  
- [CP.110 : Ne pas écrire votre propre double‑checked locking pour l'initialisation](012-concurrency.md#rconc-double)  
- [CP.111 : Utiliser un pattern conventionnel si vous avez vraiment besoin de double‑checked locking](012-concurrency.md#rconc-double-pattern)  
- comment/ quand utiliser compare_and_swap  

### <a name="rconc-lockfree"></a>CP.100 : Ne pas utiliser la programmation sans verrou sauf si vous en avez réellement besoin  

##### Raison  

C'est un sujet épineux et nécessite une expertise du niveau langage, de l'architecture machine et des structures de données.  

##### Exemple, mauvais  

```
    extern atomic<Link*> head;        // tête partagée de la liste

    Link* nh = new Link(data, nullptr);    // prépare une entrée pour l'insertion
    Link* h = head.load();                 // lire la tête partagée de la liste

    do {
        if (h->data <= data) break;        // si oui, insérer ailleurs
        nh->next = h;                      // suivant est l'ancien head
    } while (!head.compare_exchange_weak(h, nh));    // écrire nh à head ou à h
```

Références la faille.  
Cela est vraiment difficile à corriger par tests.  
Il faut se lire sur le problème ABA.  

##### Exception  

`Atomic variables` peuvent être utilisées simplement et en toute sécurité, tant que vous utilisez le modèle de mémoire séquentielles (memory_order_seq_cst), qui est le défaut.  

##### Remarque  

Les mécanismes plus haut niveau, tel que `thread`, `mutex` sont construits sur l'utilisation de la programmation sans verrou.  

**Alternative** : Utiliser des structures de données sans verrou implémentées par d'autres parties dans une bibliothèque.  

### <a name="rconc-distrust"></a>CP.101 : Méfiez-vous de votre combinaison matériel/compilateur  

##### Raison  

Les interfaces matérielles bas niveau utilisées par la programmation sans verrou sont parmi les plus difficiles à bien implémenter et où les problèmes de portabilité sont les plus subtils.  
Si vous faites du sans verrou pour la performance, vous devez vérifier les régressions.  

##### Remarque  

Le réordonnancement statique et dynamique rend difficile de penser à ce niveau.  
Les modèles formels, la vérification et les tests (souvent à l'extrême) sont essentiels.  
« Ne vous tenez pas trop près du soleil. »  

##### Application  

Avoir des règles solides pour le renforcement des tests qui couvrent tout changement de matériel, système d'exploitation, compilateur et bibliothèques.  

### <a name="rconc-literature"></a>CP.102 : Étudiez attentivement la littérature  

##### Raison  

À l'exception des atomics et de quelques autres modèles, la programmation sans verrou reste un sujet réservé aux experts.  
Devenez expert avant de mettre en production du code sans verrou pour d'autres.  

##### Références  

- Anthony Williams : *C++ concurrency in action*. Manning Publications.  
- Boehm, Adve, *You Don't Know Jack About Shared Variables or Memory Models*, Communications of the ACM, Feb 2012.  
- Boehm, *Threads Basics*, HPL TR 2009‑259.  
- Adve, Boehm, *Memory Models: A Case for Rethinking Parallel Languages and Hardware*, Communications of the ACM, Aug 2010.  
- Boehm, Adve, *Foundations of the C++ Concurrency Memory Model*, PLDI 08.  
- Mark Batty, Scott Owens, Susmit Sarkar, Peter Sewell, Tjark Weber, *Mathematizing C++ Concurrency*, POPL 2011.  
- Damian Dechev, Peter Pirkelbauer, Bjarne Stroustrup : *Understanding and Effectively Preventing the ABA Problem in Descriptor‑based Lock‑free Designs*. 13th IEEE Computer Society ISORC 2010 Schen May 2010.  
- Damian Dechev et Bjarne Stroustrup : *Scalable Non‑blocking Concurrent Objects for Mission Critical Code*. ACM OOPSLA'09, Oct 2009.  
- Damian Dechev, Peter Pirkelbauer, Nicolas Rouquette, Bjarne Stroustrup : *Semantically Enhanced Containers for Concurrent Real‑Time Systems*. Proc. 16th Annual IEEE International Conference and Workshop on the Engineering of Computer-Based Systems (IEEE ECBS), Apr 2009.  
- Maurice Herlihy, Nir Shavit, Victor Luchangco, Michael Spear : *The Art of Multiprocessor Programming*, 2nd ed., Sept 2020.  

### <a name="rconc-double"></a>CP.110 : Ne pas écrire votre propre double‑checked locking pour l'initialisation  

##### Raison  

Depuis C++11, les variables locales statiques sont maintenant initialisées de manière thread‑sûre.  
Avec le principe de RAII, les variables locales statiques remplacent le besoin d'écrire un double‑checked locking.  
`std::call_once` peut également réaliser le même but.  
Utilisez plutôt les variables statiques locales C++11 ou `std::call_once`.  

##### Exemple  

Exemple avec `std::call_once`.  

```
    void f()
    {
        static std::once_flag my_once_flag;
        std::call_once(my_once_flag, []()
        {
            // faire ceci une seule fois
        });
        // ...
    }
```

Exemple avec des variables statiques locales thread‑sûres de C++11.  

```
    void f()
    {
        // Supposant que le compilateur est conforme à C++11
        static My_class my_object; // le constructeur est appelé une seule fois
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
```

##### Application  

???  

### <a name="rconc-double-pattern"></a>CP.111 : Utiliser un pattern conventionnel si vous avez vraiment besoin de double‑checked locking  

##### Raison  

Le double‑checked locking est facile à défaire.  
Si vous avez vraiment besoin d'écrire votre propre double‑checked locking, malgré les règles [CP.110 : Ne pas écrire votre propre double‑checked locking pour l'initialisation](012-concurrency.md#rconc-double) et [CP.100 : Ne pas utiliser la programmation sans verrou sauf si vous en avez réellement besoin](012-concurrency.md#rconc-lockfree), faites‑le d'une façon conventional.  

##### Exemple, mauvais  

L'utilisation de `volatile` ne rend pas le premier test thread‑sûr, voir [CP.200 : Méfiez‑vous de `volatile` sauf pour le non‑C++](012-concurrency.md#rconc-volatile2)  

```
    mutex action_mutex;
    volatile bool action_needed;

    if (action_needed) {
        std::lock_guard<std::mutex> lock(action_mutex);
        if (action_needed) {
            take_action();
            action_needed = false;
        }
    }
```

##### Exemple, bon  

```
    mutex action_mutex;
    atomic<bool> action_needed;

    if (action_needed) {
        std::lock_guard<std::mutex> lock(action_mutex);
        if (action_needed) {
            take_action();
            action_needed = false;
        }
    }
```

Une mémoire d'ordre plus fin peut être bénéfique :  

```
    mutex action_mutex;
    atomic<bool> action_needed;

    if (action_needed.load(memory_order_acquire)) {
        lock_guard<std::mutex> lock(action_mutex);
        if (action_needed.load(memory_order_relaxed)) {
            take_action();
            action_needed.store(false, memory_order_release);
        }
    }
```

##### Application  

???  

## <a name="sscp-etc"></a>CP.etc : etc. règles de concurrence  

Ces règles n'ont pas de catégorisation simple :  

- [CP.200 : Méfiez‑vous de `volatile` sauf pour le non‑C++](012-concurrency.md#rconc-volatile2)  
- [CP.201 : ??? Signaux](012-concurrency.md#rconc-signal)  

### <a name="rconc-volatile2"></a>CP.200 : Méfiez‑vous de `volatile` sauf pour le non‑C++  

##### Raison  

`volatile` est utilisé pour désigner des objets partagés avec du code « non‑C++ » ou avec du matériel qui ne suit pas le modèle mémoire C++.  

##### Exemple  

```
    const volatile long clock;
```

Cela décrit un registre constamment mis à jour par un circuit d'horloge.  
`clock` est `volatile` parce que sa valeur changera sans aucune action du programme C++ qui l'utilise.  
Par ex., lire `clock` deux fois produira souvent deux valeurs différentes, donc l'optimiseur doit faire attention à ne pas optimiser la seconde lecture.  

```
    long t1 = clock;
    // ... aucune utilisation de clock ici ...
    long t2 = clock;
```

`clock` est `const` car le programme ne doit pas essayer d'écrire sur cet horloge.  

##### Remarque  

À moins que vous ne travailliez au plus bas niveau manipulant directement le matériel, considérez `volatile` comme un feature ésotérique à éviter.  

##### Exemple  

Normalement, le code C++ reçoit de la mémoire `volatile` qui est possédée ailleurs (hardware ou un autre langage ):  

```
    int volatile* vi = get_hardware_memory_location();
        // note: nous obtenons un pointeur vers la mémoire d'un autre
        // volatile dit "treat this with extra respect"
```

Parfois, le code C++ alloue la mémoire volatile et la partage avec « ailleurs » (hardware ou un autre langage) en faisant échapper une référence :  

```
    static volatile long vl;
    please_use_this(&vl);   // échapper une référence vers ailleurs (pas C++)
```

##### Exemple, mauvais  

Les variables locales `volatile` sont presque toujours incorrectes — comment peuvent-elles être partagées avec d'autres langages ou hardware si elles sont éphémères ?  
La même remarque s'applique aux membres de données.  

```
    void f()
    {
        volatile int i = 0; // mauvais, volatile local variable
        // etc.
    }

    class My_type {
        volatile int i = 0; // suspicion, volatile data member
        // etc.
    };
```

##### Remarque  

En C++, contrairement à d'autres langages, `volatile` n'a rien à voir avec la synchronisation.  

##### Application  

- Flag `volatile T` variables locales et membres de données ; vous vouliez probablement utiliser `atomic<T>` à la place.  
- ???  

### <a name="rconc-signal"></a>CP.201 : ??? Signaux  

??? UNIX signal handling ???.  
Il vaut peut-être utile de rappeler la faible sécurité d'utilisation asynchrone de signaux, et de communiquer avec un handler de signal (le meilleur est probablement « pas du tout »).