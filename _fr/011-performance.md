# <a name="s-performance"></a>Per: Performance

??? Ce chapitre devrait-il figurer dans le guide principal???  

Cette section contient des règles destinées aux personnes qui ont besoin de performances élevées ou de faible latence.  
Il s'agit, en d'autres termes, de règles liées à la façon d'utiliser un minimum de temps et de ressources afin de réaliser une tâche en un laps de temps prévisiblement court.  
Les règles de cette section sont plus restrictives et intrusives que ce qui est nécessaire pour bon nombre d'applications (la majorité).  
Ne tentez pas de les suivre naïvement dans votre code général : atteindre les objectifs de faible latence nécessite un travail supplémentaire.  

### Résumé des règles de performance:

* [Per.1: Ne pas optimiser sans raison](#rper-reason)  
* [Per.2: Ne pas optimiser prématurément](#rper-knuth)  
* [Per.3: Ne pas optimiser une partie qui n'est pas critique en termes de performance](#rper-critical)  
* [Per.4: Ne pas supposer qu'un code compliqué est forcément plus rapide qu'un code simple](#rper-simple)  
* [Per.5: Ne pas supposer qu'un code bas niveau est forcément plus rapide qu'un code haut niveau](#rper-low)  
* [Per.6: Ne pas affirmer la performance sans mesurer](#rper-measure)  
* [Per.7: Concevoir pour permettre l'optimisation](#rper-efficiency)  
* [Per.10: S'appuyer sur le système de types statiques](#rper-type)  
* [Per.11: Déplacer le calcul du temps d'exécution au temps de compilation](#rper-comp)  
* [Per.12: Éliminer les alias redondants](#rper-alias)  
* [Per.13: Éliminer les indirections redondantes](#rper-indirect)  
* [Per.14: Minimiser le nombre d'allocations et de désallocations](#rper-alloc)  
* [Per.15: Ne pas allouer sur une branche critique](#rper-alloc0)  
* [Per.16: Utiliser des structures de données compactes](#rper-compact)  
* [Per.17: Déclarer comme premier l'élément le plus utilisé d'une structure critique de temps](#rper-struct)  
* [Per.18: L'espace est le temps](#rper-space)  
* [Per.19: Accéder à la mémoire de façon prévisible](#rper-access)  
* [Per.30: Éviter les changements de contexte sur le chemin critique](#rper-context)  

### <a name="rper-reason"></a>Per.1: Ne pas optimiser sans raison

##### Reason

Si aucune optimisation n'est nécessaire, le résultat principal de l'effort sera plus d'erreurs et de coûts de maintenance plus élevés.  

##### Note

Certains optimisent par habitude ou simplement parce que c'est amusant.  

???  

### <a name="rper-knuth"></a>Per.2: Ne pas optimiser prématurément

##### Reason

Un code optimisé de façon élaborée est généralement plus volumineux et plus difficile à modifier qu'un code non optimisé.  

???  

### <a name="rper-critical"></a>Per.3: Ne pas optimiser une partie qui n'est pas critique en termes de performance

##### Reason

Optimiser une partie non critique en termes de performance d'un programme n'a aucun effet sur les performances du système.  

##### Note

Si votre programme passe la majorité de son temps à attendre le web ou un humain, l'optimisation des calculs en mémoire est probablement inutile.  

En d'autres termes : si votre programme consacre 4 % de son temps de traitement à la computation A et 40 % à la computation B, une amélioration de 50 % sur A n'est seulement aussi impactante qu'une amélioration de 5 % sur B. (Si vous ne savez même pas combien de temps est dépensé sur A ou B, consultez <a href="#rper-reason">Per.1</a> et <a href="#rper-knuth">Per.2</a>.)  

???  

### <a name="rper-simple"></a>Per.4: Ne pas supposer qu'un code compliqué est forcément plus rapide qu'un code simple

##### Reason

Un code simple peut être très performant. Les optimiseurs accomplissent parfois des merveilles avec du code simple.  

##### Example, bon

    // clear expression of intent, fast execution

    vector<uint8_t> v(100000);

    for (auto& c : v)
        c = ~c;

##### Example, mauvais

    // intended to be faster, but is often slower

    vector<uint8_t> v(100000);

    for (size_t i = 0; i < v.size(); i += sizeof(uint64_t)) {
        uint64_t& quad_word = *reinterpret_cast<uint64_t*>(&v[i]);
        quad_word = ~quad_word;
    }

##### Note

???  

???  

### <a name="rper-low"></a>Per.5: Ne pas supposer qu'un code bas niveau est forcément plus rapide qu'un code haut niveau

##### Reason

Un code bas niveau peut parfois inhiber les optimisations. Les optimiseurs accomplissent parfois des merveilles avec du code haut niveau.  

##### Note

???  

???  

### <a name="rper-measure"></a>Per.6: Ne pas affirmer la performance sans mesurer

##### Reason

Le domaine de la performance est foisonnant de mythes et de folklore du faux. Le matériel moderne et les optimiseurs défient les suppositions naïves ; même les experts sont régulièrement surpris.  

##### Note

Obtenir de bonnes mesures de performance peut être difficile et nécessite des outils spécialisés.  

##### Note

Quelques micro‑benchmarks simples utilisant `time` sur Unix ou la bibliothèque standard `<chrono>` peuvent aider à démystifier les mythes les plus évidents. Si vous ne pouvez pas mesurer votre système complet avec précision, essayez au moins de mesurer quelques‑unes de vos opérations et algorithmes clés. Un profiler peut vous indiquer quelles parties de votre système sont critiques en termes de performance. Souvent, vous serez surpris.  

???  

### <a name="rper-efficiency"></a>Per.7: Concevoir pour permettre l'optimisation

##### Reason

Car nous avons souvent besoin d'optimiser la conception initiale. Un design qui ignore la possibilité d'une amélioration ultérieure est difficile à modifier.  

##### Example

Selon le standard C (et C++):

    void qsort (void* base, size_t num, size_t size, int (*compar)(const void*, const void*));

Là où avez‑vous vraiment voulu trier la mémoire ?  
En réalité, nous trions des séquences d'éléments, généralement stockées dans des conteneurs.  
Un appel à `qsort` jette beaucoup d'informations utiles (p. ex. le type d'élément), force l'utilisateur à répéter des informations déjà connues (p. ex. la taille de l'élément), et force l'utilisateur à écrire du code supplémentaire (p. ex. une fonction pour comparer les `double`).  
Cela implique un travail supplémentaire pour le programmeur, rend la tâche plus sujette à erreur, et prive le compilateur des informations nécessaires à l'optimisation.

    double data[100];
    // ... fill a ...

    // 100 chunks of memory of sizeof(double) starting at
    // address data using the order defined by compare_doubles
    qsort(data, 100, sizeof(double), compare_doubles);

Du point de vue de la conception d'interface, `qsort` jette des informations utiles.  

Nous pouvons faire mieux (en C++98)

    template<typename Iter>
        void sort(Iter b, Iter e);  // sort [b:e)

    sort(data, data + 100);

Ici, nous utilisons la connaissance du compilateur concernant la taille du tableau, le type des éléments, et la façon de comparer les `double`.  

Avec C++20, nous pouvons encore faire mieux :

    // sortable spécifie que c doit être une
    // séquence d'accès aléatoire d'éléments comparables avec <
    void sort(sortable auto& c);

    sort(c);

La clé est de transmettre suffisamment d'information pour qu'une bonne implémentation soit choisie.  
Dans cette interface `sort`, l'interface affichée reste sujette à une faiblesse : elle dépend implicitement du fait que le type d'élément possède l'opérateur `<` défini.  
Pour compléter l'interface, nous avons besoin d'une version secondaire acceptant un critère de comparaison :

    // compare elements of c using r
    template<random_access_range R, class C> requires sortable<R, C>
    void sort(R&& r, C c);

La spécification de la bibliothèque standard de `sort` offre ces deux versions, et d'autres.  

##### Note

La règle [Ne pas optimiser prématurément](#rper-knuth) est dite la racine de tout mal, mais ce n'est pas un motif pour mépriser la performance.  
Il n'est jamais prématuré de considérer ce qui rend un design propice à l'amélioration, et l'amélioration de la performance est un bénéfice communément recherché.  
S'efforcer de créer un ensemble d'habitudes qui, par défaut, donne un code efficace, maintenable et optimisable.  
En particulier, quand vous écrivez une fonction qui n'est pas un détail d'implémentation unique, considérez :

* Transmission d'information : préférez des [interfaces](005-interfaces.md) propres, transportant suffisamment d'information pour l'amélioration ultérieure de l'implémentation. Notez que les informations circulent dans et hors d'une implémentation via les interfaces que nous fournissons.  
* Données compactes : par défaut, [utiliser des données compactes](#rper-compact), telles que `std::vector` et [l'accéder de façon systématique](#rper-access). Si vous pensez qu'une structure liée est nécessaire, essayez de concevoir l'interface de façon à ce que cette structure ne soit pas visible par l'utilisateur.  
* Passage de paramètres et retour de fonction : distinguez entre données mutables et non mutables. Ne imposez pas à vos utilisateurs une charge de gestion des ressources. Ne forcez pas d'indirections d'exécution inutiles sur vos utilisateurs. Utilisez [les façons conventionnelles](#rf-conventional) de transmettre l'information via une interface ; des façons peu conventionnelles ou « optimisées » de transmettre les données peuvent sérieusement compliquer une future re‑implémentation.  
* Abstraction : ne sur-généralisez pas ; un design qui tente de répondre à toute utilisation (et abus) possible et reporte chaque décision de conception plus tard (en utilisant des indirections en temps d'édition ou d'exécution) est généralement un gros bazar, un tas compliqué et difficile à comprendre. Généralisez à partir d'exemples concrets, préservant la performance en générant. Ne générez pas en se basant uniquement sur une spéculation concernant les besoins futurs. L'idéal est une généralisation à aucun surcoût.  
* Bibliothèques : utilisez des bibliothèques avec de bonnes interfaces. Si aucune bibliothèque n'est disponible, construisez-en vous‑même et imitez le style d'interface d'une bonne bibliothèque. La [bibliothèque standard](018-stdlib.md) est un bon premier endroit pour s'inspirer.  
* Isolement : isolez votre code du code désordonné et/ou style ancien en fournissant une interface de votre choix. Cela se nomme parfois « fournir un wrapper » pour le code utile/nécessaire mais désordonné. Ne laissez pas les mauvais designs « s'étendre » dans votre code.  

##### Example

Considérez :

    template<class ForwardIterator, class T>
    bool binary_search(ForwardIterator first, ForwardIterator last, const T& val);

`binary_search(begin(c), end(c), 7)` vous indiquera si `7` est dans `c` ou pas.  
Cependant, il ne vous indiquera pas où le `7` se trouve ni s'il y a plus d'un `7`.  

Parfois, simplement transmettre le minimum d'information en retour (ici, `true` ou `false`) est suffisant, mais une bonne interface transmet l'information nécessaire pour l'appel. Par conséquent, la bibliothèque standard propose aussi

    template<class ForwardIterator, class T>
    ForwardIterator lower_bound(ForwardIterator first, ForwardIterator last, const T& val);

`lower_bound` renvoie un itérateur au premier élément correspondant le cas échéant, sinon au premier élément supérieur à `val`, ou `last` s'il n'y en a pas.  

Cependant, `lower_bound` ne renvoie toujours pas assez d'information pour toutes les utilisations, alors la bibliothèque standard propose aussi

    template<class ForwardIterator, class T>
    pair<ForwardIterator, ForwardIterator>
    equal_range(ForwardIterator first, ForwardIterator last, const T& val);

`equal_range` renvoie un `pair` d'itérateurs indiquant le premier et le suivant en dehors du dernier match.

    auto r = equal_range(begin(c), end(c), 7);
    for (auto p = r.first; p != r.second; ++p)
        cout << *p << '\n';

Évidemment, ces trois interfaces sont implémentées par le même code de base.  
Elles sont simplement trois façons de présenter l'algorithme de recherche binaire aux utilisateurs, allant du plus simple (« rendre les choses simples simples ! ») aux informations complètes, mais pas toujours nécessaires (« ne cachez pas l'information utile »).  
Naturellement, concevoir un tel ensemble d'interfaces requiert expérience et connaissance métier.  

##### Note

Ne conservez pas simplement l'interface correspondant à la première implémentation et au premier cas d'utilisation que vous avez en tête. Quand votre première implémentation est terminée, réévaluez‑la ; une fois déployée, les erreurs seront difficiles à corriger.  

##### Note

Un besoin d'efficacité ne suppose pas un besoin de code bas niveau ; le code haut niveau n'est pas forcément lent ou verbeux.  

##### Note

Les choses ont des coûts. Ne soyez pas paranoïaque à propos des coûts (les ordinateurs modernes sont vraiment rapides), mais ayez une idée approximative de l'ordre de grandeur de ce que vous utilisez. Par exemple, estimer approximativement le coût d'un accès mémoire, d'un appel de fonction, d'une comparaison de chaîne, d'un appel système, d'un accès disque et d'un message réseau.  

##### Note

Si vous ne pouvez imaginer qu'une seule implémentation, vous n'avez probablement pas quelque chose pour lequel vous pouvez concevoir une interface stable. Peut‑être que c'est juste un détail d'implémentation ? Pas tout code a besoin d'une interface stable.  
Prenez un instant pour réfléchir. Une question utile est :  
« Quelle interface serait nécessaire si cette opération devait être implémentée multi‑thread ? vectorisée ? »  

##### Note

Cette règle ne contredit pas la règle de [Ne pas optimiser prématurément](#rper-knuth).  
Elle la complète, encourageant les développeurs à permettre une optimisation future – appropriée et non prématurée – si besoin.  

##### Enforcement  

Sournois.  
Peut‑être en recherchant des arguments de fonction `void*` on trouve des exemples d'interfaces qui entravent une optimisation ultérieure.  

@TODO-LINK: #rf-conventional  

### <a name="rper-type"></a>Per.10: S'appuyer sur le système de types statiques

##### Motif

Les violations de type, les types faibles (p. ex. `void*`), et le code bas niveau (p. ex. la manipulation de séquences en octets individuels) rendent le travail de l'optimiseur bien plus difficile. Le code simple optimise souvent mieux qu'un code complexe passé à la main.  

???  

### <a name="rper-comp"></a>Per.11: Déplacer le calcul du temps d'exécution au temps de compilation

##### Motif

Réduire la taille du code et le temps d'exécution.  
Éviter les conflits d'accès concurrentiel en utilisant des constantes.  
Permettre de détecter les erreurs à la compilation (et ainsi éliminer le besoin de code de gestion des erreurs).  

##### Example

    double square(double d) { return d*d; }
    static double s2 = square(2);    // old-style: dynamic initialization

    constexpr double ntimes(double d, int n)   // assume 0 <= n
    {
            double m = 1;
            while (n--) m *= d;
            return m;
    }
    constexpr double s3 {ntimes(2, 3)};  // modern-style: compile-time initialization

Le type d'initialisation de `s2` n'est pas rare, surtout pour des initialisations plus compliquées que `square()`.  
Cependant, comparé à l'initialisation de `s3` il y a deux problèmes :

* nous subissons le coût d'un appel de fonction à l'exécution  
* `s2` pourrait être accédé par un autre thread avant que l'initialisation ne se fasse.  

Note : vous ne pouvez pas avoir une course de données sur une constante.  

##### Example

Considérez une technique populaire pour fournir un gestionnaire capable de stocker les petits objets dans le gestionnaire lui‑même et les plus gros sur le tas.

    constexpr int on_stack_max = 20;

    template<typename T>
    struct Scoped {     // stocker un T dans Scoped
            // ...
        T obj;
    };

    template<typename T>
    struct On_heap {    // stocker un T sur le tas
            // ...
            T* objp;
    };

    template<typename T>
    using Handle = typename std::conditional<(sizeof(T) <= on_stack_max),
                        Scoped<T>,      // première alternative
                        On_heap<T>      // deuxième alternative
                   >::type;

    void f()
    {
        Handle<double> v1;                   // le double va sur la pile
        Handle<std::array<double, 200>> v2;  // le tableau va sur le tas
        // ...
    }

Supposons que `Scoped` et `On_heap` fournissent des interfaces utilisateurs compatibles.  
Ici nous calculons le type optimal à utiliser à la compilation.  
Il existe des techniques similaires pour choisir la fonction optimale à appeler.  

##### Note

L'idéal n'est pas d'essayer d'exécuter tout à la compilation.  
Évidemment, la plupart des calculs dépendent des entrées, donc ils ne peuvent pas être déplacés à la compilation.  
En plus de cette contrainte logique, une compilation complexe peut fortement allonger les temps de compilation et compliquer le débogage.  
Il est même possible de ralentir le code par le calcul à la compilation, bien que cela soit rare.  
En factorisant un calcul général en sous‑calculs d'optimisation distincts, on peut réduire l'efficacité du cache d'instructions.  

##### Note

???  

### <a name="rper-alias"></a>Per.12: Éliminer les alias redondants

???  

### <a name="rper-indirect"></a>Per.13: Éliminer les indirections redondantes

???  

### <a name="rper-alloc"></a>Per.14: Minimiser le nombre d'allocations et de désallocations

???  

### <a name="rper-alloc0"></a>Per.15: Ne pas allouer sur une branche critique

???  

### <a name="rper-compact"></a>Per.16: Utiliser des structures de données compactes

##### Motif

La performance est généralement dominée par les temps d'accès mémoire.  

???  

### <a name="rper-struct"></a>Per.17: Déclarer comme premier l'élément le plus utilisé d'une structure critique de temps

???  

### <a name="rper-space"></a>Per.18: L'espace est le temps

##### Motif

La performance est généralement dominée par les temps d'accès mémoire.  

???  

### <a name="rper-access"></a>Per.19: Accéder à la mémoire de façon prévisible

##### Motif

La performance est très sensible aux performances du cache, et les algorithmes de cache favorisent l'accès simple (habituellement linéaire) aux données adjacentes.  

##### Example

    int matrix[rows][cols];

    // bad
    for (int c = 0; c < cols; ++c)
        for (int r = 0; r < rows; ++r)
            sum += matrix[r][c];

    // good
    for (int r = 0; r < rows; ++r)
        for (int c = 0; c < cols; ++c)
            sum += matrix[r][c];

### <a name="rper-context"></a>Per.30: Éviter les changements de contexte sur le chemin critique

???