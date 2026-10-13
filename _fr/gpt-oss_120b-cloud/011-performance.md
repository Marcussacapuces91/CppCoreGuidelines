# <a name="s-performance"></a>Per: Performance

??? cette section devrait‑elle être dans le guide principal ???

Cette section contient des règles destinées aux personnes qui ont besoin d’une haute performance ou d’une faible latence. En d’autres termes, ces règles portent sur la manière d’utiliser le moins de temps et de ressources possible pour accomplir une tâche dans un délai prévisible et court. Les règles de cette section sont plus restrictives et intrusives que ce qui est nécessaire pour la plupart (la majorité) des applications. N’essayez pas de les appliquer naïvement dans du code général : atteindre les objectifs de faible latence nécessite un travail supplémentaire.

**Résumé des règles de performance :**

* [Per.1 : ne pas optimiser sans raison](011-performance.md#rper-reason)
* [Per.2 : ne pas optimiser prématurément](011-performance.md#rper-knuth)
* [Per.3 : ne pas optimiser ce qui n’est pas critique en termes de performance](011-performance.md#rper-critical)
* [Per.4 : ne pas supposer que le code compliqué est forcément plus rapide que le code simple](011-performance.md#rper-simple)
* [Per.5 : ne pas supposer que le code bas‑niveau est forcément plus rapide que le code haut‑niveau](011-performance.md#rper-low)
* [Per.6 : ne pas faire d’affirmations sur les performances sans mesures](011-performance.md#rper-measure)
* [Per.7 : concevoir pour faciliter l’optimisation](011-performance.md#rper-efficiency)
* [Per.10 : s’appuyer sur le système de types statiques](011-performance.md#rper-type)
* [Per.11 : déplacer le calcul du temps d’exécution au temps de compilation](011-performance.md#rper-comp)
* [Per.12 : éliminer les alias redondants](011-performance.md#rper-alias)
* [Per.13 : éliminer les indirections redondantes](011-performance.md#rper-indirect)
* [Per.14 : minimiser le nombre d’allocations et de désallocations](011-performance.md#rper-alloc)
* [Per.15 : ne pas allouer dans une branche critique](011-performance.md#rper-alloc0)
* [Per.16 : utiliser des structures de données compactes](011-performance.md#rper-compact)
* [Per.17 : déclarer le membre le plus utilisé d’une structure critique en temps en premier](011-performance.md#rper-struct)
* [Per.18 : l’espace est du temps](011-performance.md#rper-space)
* [Per.19 : accéder à la mémoire de façon prévisible](011-performance.md#rper-access)
* [Per.30 : éviter les changements de contexte sur le chemin critique](011-performance.md#rper-context)

### <a name="rper-reason"></a>Per.1 : ne pas optimiser sans raison

##### Raison

S’il n’y a pas besoin d’optimisation, le principal résultat de l’effort sera davantage d’erreurs et des coûts de maintenance plus élevés.

##### Note

Certaines personnes optimisent par habitude ou parce que c’est amusant.

???

### <a name="rper-knuth"></a>Per.2 : ne pas optimiser prématurément

##### Raison

Le code fortement optimisé est généralement plus volumineux et plus difficile à modifier que le code non optimisé.

???

### <a name="rper-critical"></a>Per.3 : ne pas optimiser ce qui n’est pas critique en termes de performance

##### Raison

Optimiser une partie d’un programme qui n’est pas critique en performance n’a aucun effet sur les performances du système.

##### Note

Si votre programme passe la majorité de son temps à attendre le réseau ou un humain, l’optimisation du calcul en mémoire est probablement inutile.

Autrement dit : si votre programme consacre 4 % de son temps de traitement à la computation A et 40 % à la computation B, une amélioration de 50 % sur A n’a d’impact que celui d’une amélioration de 5 % sur B. (Si vous ne savez même pas combien de temps est passé sur A ou B, consultez <a href="#rper-reason">Per.1</a> et <a href="#rper-knuth">Per.2</a>.)

### <a name="rper-simple"></a>Per.4 : ne pas supposer que le code compliqué est forcément plus rapide que le code simple

##### Raison

Le code simple peut être très rapide. Les optimiseurs réalisent parfois des merveilles avec du code simple.

##### Exemple, bon

    // expression claire de l’intention, exécution rapide

    vector<uint8_t> v(100000);

    for (auto& c : v)
        c = ~c;

##### Exemple, mauvais

    // destiné à être plus rapide, mais est souvent plus lent

    vector<uint8_t> v(100000);

    for (size_t i = 0; i < v.size(); i += sizeof(uint64_t)) {
        uint64_t& quad_word = *reinterpret_cast<uint64_t*>(&v[i]);
        quad_word = ~quad_word;
    }

##### Note

???

???

### <a name="rper-low"></a>Per.5 : ne pas supposer que le code bas‑niveau est forcément plus rapide que le code haut‑niveau

##### Raison

Le code bas‑niveau empêche parfois les optimisations. Les optimiseurs réalisent parfois des merveilles avec du code haut‑niveau.

##### Note

???

???

### <a name="rper-measure"></a>Per.6 : ne pas faire d’affirmations sur les performances sans mesures

##### Raison

Le domaine de la performance regorge de mythes et de folklore infondé. Le matériel moderne et les optimiseurs contredisent les hypothèses naïves ; même les experts sont régulièrement surpris.

##### Note

Obtenir de bonnes mesures de performance peut être difficile et nécessiter des outils spécialisés.

##### Note

Quelques micro‑benchmarks simples utilisant la commande Unix `time` ou la bibliothèque standard `<chrono>` peuvent aider à dissiper les mythes les plus évidents.  
Si vous ne pouvez pas mesurer votre système complet avec précision, essayez au moins de mesurer quelques‑unes de vos opérations ou algorithmes clés.  
Un profileur peut vous indiquer quelles parties de votre système sont critiques en termes de performance.  
Souvent, vous serez surpris.

???

### <a name="rper-efficiency"></a>Per.7 : concevoir pour faciliter l’optimisation

##### Raison

Parce que nous devons souvent optimiser la conception initiale.  
Parce qu’une conception qui ignore la possibilité d’une amélioration ultérieure est difficile à modifier.

##### Exemple

Depuis la norme C (et C++) :

    void qsort (void* base, size_t num, size_t size, int (*compar)(const void*, const void*));

Quand avez‑vous réellement besoin de trier de la mémoire ?  
En réalité, nous trions des séquences d’éléments, généralement stockées dans des conteneurs.  
Un appel à `qsort` jette beaucoup d’informations utiles (par ex., le type d’élément), oblige l’utilisateur à répéter des informations déjà connues (par ex., la taille de l’élément) et impose à l’utilisateur d’écrire du code supplémentaire (par ex., une fonction de comparaison de `double`).  
Cela entraîne du travail supplémentaire pour le programmeur, augmente le risque d’erreur et prive le compilateur d’informations nécessaires à l’optimisation.

    double data[100];
    // ... remplissez‑les ...

    // 100 blocs de mémoire de sizeof(double) commençant à
    // l’adresse data, ordonnés d’après compare_doubles
    qsort(data, 100, sizeof(double), compare_doubles);

Du point de vue de la conception d’interface, `qsort` jette des informations utiles.

Nous pouvons faire mieux (en C++98) :

    template<typename Iter>
        void sort(Iter b, Iter e);  // trier [b:e)

    sort(data, data + 100);

Ici, nous utilisons la connaissance du compilateur sur la taille du tableau, le type des éléments, et la façon de comparer les `double`.

Avec C++20, nous pouvons faire encore mieux :

    // sortable spécifie que c doit être une
    // séquence d’accès aléatoire d’éléments comparables avec <
    void sort(sortable auto& c);

    sort(c);

L’idée est de transmettre suffisamment d’informations pour qu’une implémentation appropriée soit choisie.  
Dans cette approche, les interfaces `sort` présentées ici ont encore une faiblesse : elles reposent implicitement sur le fait que le type d’élément possède l’opérateur `<`.  
Pour compléter l’interface, nous avons besoin d’une deuxième version qui accepte un critère de comparaison :

    // comparer les éléments de c en utilisant r
    template<random_access_range R, class C> requires sortable<R, C>
    void sort(R&& r, C c);

La spécification de la bibliothèque standard pour `sort` propose ces deux versions, et davantage.

##### Note

L’optimisation prématurée est souvent citée comme étant [la racine de tout mal](011-performance.md#rper-knuth), mais cela ne justifie pas le mépris de la performance.  
Il n’est jamais prématuré de réfléchir à ce qui rend une conception propice à l’amélioration, et une meilleure performance est généralement une amélioration recherchée.  
Visez à développer un ensemble d’habitudes qui, par défaut, produisent du code efficace, maintenable et optimisable.  
En particulier, lorsque vous écrivez une fonction qui n’est pas un détail d’implémentation ponctuel, pensez à :

* **Passage d’informations :** privilégiez des [interfaces](005-interfaces.md) propres, transportant suffisamment d’informations pour une amélioration ultérieure de l’implémentation. Notez que les informations entrent et sortent d’une implémentation via les interfaces que nous fournissons.
* **Données compactes :** par défaut, [utilisez des données compactes](011-performance.md#rper-compact), telles que `std::vector`, et [accédez‑y de façon systématique](011-performance.md#rper-access). Si vous pensez avoir besoin d’une structure chaînée, essayez de concevoir l’interface de sorte que cette structure ne soit pas visible par les utilisateurs.
* **Passage d’arguments et retour de fonction :** distinguez les données mutables et non mutables.  
  Ne surchargez pas vos utilisateurs d’une charge de gestion de ressources.  
  Ne les imposez pas d’indirections inutiles au moment de l’exécution.  
  Utilisez les [modes conventionnels](006-functions.md#rf-conventional) de passage d’informations à travers une interface ; les modes non conventionnels et/ou « optimisés » peuvent compliquer gravement une ré‑implémentation ultérieure.
* **Abstraction :** ne généralisez pas à l’excès ; une conception qui tente de couvrir chaque usage (et mauvais usage) possible et reporte chaque décision de conception à plus tard (en utilisant des indirections à la compilation ou à l’exécution) devient généralement un enchevêtrement compliqué et lourd à comprendre. Généralisez à partir d’exemples concrets, tout en préservant la performance au fur et à mesure que vous généralisez. N’opérez pas de généralisation fondée uniquement sur des spéculations concernant des besoins futurs. L’idéal est une généralisation à coût nul.
* **Bibliothèques :** utilisez des bibliothèques présentant de bonnes interfaces.  
  Si aucune bibliothèque n’est disponible, créez‑en une vous‑même en imitant le style d’interface d’une bonne bibliothèque. La [bibliothèque standard](#sl-the-standard-library) est un bon point de départ pour s’inspirer. @TODO-LINK
* **Isolation :** isolez votre code du code désordonné et/ou ancien en lui fournissant une interface de votre choix. Cela s’apparente parfois à « fournir un wrapper » pour le code utile/nécessaire mais désordonné. Ne laissez pas les mauvais designs « se propager » dans votre code.

##### Exemple

Considérons :

    template<class ForwardIterator, class T>
    bool binary_search(ForwardIterator first, ForwardIterator last, const T& val);

`binary_search(begin(c), end(c), 7)` vous indique simplement si `7` se trouve dans `c`.  
Il ne vous indique pas où se situe ce `7` ni s’il y en a plusieurs.

Parfois, renvoyer uniquement une valeur booléenne (`true` ou `false`) suffit, mais une bonne interface renvoie les informations nécessaires à l’appelant. Ainsi, la bibliothèque standard propose également :

    template<class ForwardIterator, class T>
    ForwardIterator lower_bound(ForwardIterator first, ForwardIterator last, const T& val);

`lower_bound` renvoie un itérateur pointant sur la première occurrence (si elle existe), sinon sur le premier élément strictement supérieur à `val`, ou `last` s’il n’y a aucun tel élément.

Cependant, `lower_bound` ne renvoie toujours pas assez d’informations pour tous les usages, d’où l’existence de :

    template<class ForwardIterator, class T>
    std::pair<ForwardIterator, ForwardIterator>
    equal_range(ForwardIterator first, ForwardIterator last, const T& val);

`equal_range` renvoie une `pair` d’itérateurs spécifiant la première correspondance et la première non‑correspondance.

    auto r = equal_range(begin(c), end(c), 7);
    for (auto p = r.first; p != r.second; ++p)
        std::cout << *p << '\n';

Il est évident que ces trois interfaces sont implémentées à partir du même algorithme de recherche binaire de base. Ce sont simplement trois façon de présenter cet algorithme aux utilisateurs, allant du plus simple (« rendre les choses simples simples ! ») au plus complet (« ne pas cacher les informations utiles »).  
Évidemment, concevoir un tel ensemble d’interfaces nécessite de l’expérience et une bonne connaissance du domaine.

##### Note

Ne façonnez pas simplement l’interface pour qu’elle corresponde à la première implémentation et au premier cas d’utilisation qui vous viennent à l’esprit. Une fois votre première implémentation achevée, revoyez‑la ; une fois déployée, les erreurs seront difficiles à corriger.

##### Note

Un besoin d’efficacité n’implique pas forcément un besoin de [code bas‑niveau](011-performance.md#rper-low).  
Le code de haut niveau n’est pas nécessairement lent ou gonflé.

##### Note

Tout a un coût. Ne soyez pas paranoïaque à propos des coûts (les ordinateurs modernes sont vraiment très rapides), mais ayez une idée approximative de l’ordre de grandeur du coût des opérations que vous utilisez. Par exemple, avez une idée approximative du coût d’un :

* accès mémoire,
* appel de fonction,
* comparaison de chaîne,
* appel système,
* accès disque,
* transmission de message sur le réseau.

##### Note

Si vous ne pouvez concevoir qu’une seule implémentation, vous n’avez probablement pas de sujet pour lequel vous puissiez concevoir une interface stable. Peut‑être s’agit‑il simplement d’un détail d’implémentation – toutes les parties du code n’ont pas besoin d’une interface stable – mais prenez un moment pour y réfléchir. Une question utile est : « Quelle interface serait nécessaire si cette opération devait être implémentée avec plusieurs threads ? ou vectorisée ? »

##### Note

Cette règle ne contredit pas la règle [« ne pas optimiser prématurément »](011-performance.md#rper-knuth).  
Elle la complète en encourageant les développeurs à préparer l’optimisation ultérieure – appropriée et non prématurée – lorsque cela est nécessaire.

##### Application

C’est délicat.  
Rechercher des arguments de fonction de type `void*` peut permettre d’identifier des interfaces qui entravent une optimisation ultérieure.

### <a name="rper-type"></a>Per.10 : s’appuyer sur le système de types statiques

##### Raison

Les violations de type, les types faibles (par ex., les `void*`) et le code bas‑niveau (manipulation de séquences au niveau des octets) compliquent considérablement le travail de l’optimiseur. Le code simple s’optimise souvent mieux que le code complexe fait‑main.

???

### <a name="rper-comp"></a>Per.11 : déplacer le calcul du temps d’exécution au temps de compilation

##### Raison

Réduire la taille du code et le temps d’exécution.  
Éviter les data races en utilisant des constantes.  
Détecter les erreurs à la compilation (et ainsi éliminer le besoin de code de gestion d’erreurs).

##### Exemple

    double square(double d) { return d*d; }
    static double s2 = square(2);    // ancien style : initialisation dynamique

    constexpr double ntimes(double d, int n)   // suppose 0 <= n
    {
        double m = 1;
        while (n--) m *= d;
        return m;
    }
    constexpr double s3 {ntimes(2, 3)};  // style moderne : initialisation au moment de la compilation

Ce type d’initialisation de `s2` n’est pas rare, surtout lorsqu’il s’agit d’une expression un peu plus compliquée que `square()`.  
Cependant, comparé à l’initialisation de `s3`, il y a deux problèmes :

* on paie le coût d’un appel de fonction au temps d’exécution,
* `s2` pourrait être accédé par un autre thread avant que l’initialisation ne s’effectue.

Remarque : vous ne pouvez pas avoir de data race sur une constante.

##### Exemple

Considérons une technique populaire consistant à fournir un handle qui stocke les petits objets dans le handle lui‑même et les plus gros sur le tas.

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
        Handle<double> v1;                   // le double est placé sur la pile
        Handle<std::array<double, 200>> v2;  // le tableau est placé sur le tas
        // ...
    }

On suppose que `Scoped` et `On_heap` offrent des interfaces utilisateurs compatibles.  
Ici, nous calculons le type optimal à utiliser à la compilation. Des techniques similaires existent pour sélectionner la fonction optimale à appeler.

##### Note

L’idéal n’est pas d’essayer d’exécuter tout à la compilation.  
Évidemment, la plupart des calculs dépendent d’entrées, donc ils ne peuvent pas être déplacés à la compilation, mais au‑delà de cette contrainte logique, le calcul intensif à la compilation peut augmenter fortement les temps de compilation et compliquer le débogage. Il est même possible de ralentir le code à cause d’un calcul à la compilation. Cela reste rare, mais en factorisant un calcul général en sous‑calculs optimaux séparés, on peut diminuer l’efficacité du cache d’instructions.

##### Application

* Recherchez des fonctions simples qui pourraient être `constexpr` (mais ne le sont pas).
* Recherchez des fonctions appelées avec tous leurs arguments étant des expressions constantes.
* Recherchez des macros qui pourraient être remplacées par `constexpr`.

### <a name="rper-alias"></a>Per.12 : éliminer les alias redondants

???

### <a name="rper-indirect"></a>Per.13 : éliminer les indirections redondantes

???

### <a name="rper-alloc"></a>Per.14 : minimiser le nombre d’allocations et de désallocations

???

### <a name="rper-alloc0"></a>Per.15 : ne pas allouer dans une branche critique

???

### <a name="rper-compact"></a>Per.16 : utiliser des structures de données compactes

##### Raison

Les performances sont généralement dominées par les temps d’accès à la mémoire.

???

### <a name="rper-struct"></a>Per.17 : déclarer le membre le plus utilisé d’une structure critique en temps en premier

???

### <a name="rper-space"></a>Per.18 : l’espace est du temps

##### Raison

Les performances sont généralement dominées par les temps d’accès à la mémoire.

???

### <a name="rper-access"></a>Per.19 : accéder à la mémoire de façon prévisible

##### Raison

Les performances sont très sensibles à la performance du cache, et les algorithmes de cache privilégient un accès simple (généralement linéaire) aux données adjacentes.

##### Exemple

    int matrix[rows][cols];

    // mauvais
    for (int c = 0; c < cols; ++c)
        for (int r = 0; r < rows; ++r)
            sum += matrix[r][c];

    // bon
    for (int r = 0; r < rows; ++r)
        for (int c = 0; c < cols; ++c)
            sum += matrix[r][c];

### <a name="rper-context"></a>Per.30 : éviter les changements de contexte sur le chemin critique

???