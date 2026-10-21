# <a name="s-performance"></a>Per : Performance

??? cette section devrait-elle figurer dans le guide principal ???

Cette section contient des règles destinées aux personnes qui ont besoin de hautes performances ou de faible latence.
Autrement dit, il s'agit de règles relatives à la manière d'accomplir une tâche en un temps prévisible le plus court possible, en utilisant le moins de temps et de ressources possible.
Les règles de cette section sont plus restrictives et plus contraignantes que ce qui est nécessaire pour la plupart des applications.
Ne tentez pas naïvement de les suivre dans du code général : atteindre les objectifs de faible latence exige un travail supplémentaire.

Résumé des règles de performance :

* [Per.1 : Ne pas optimiser sans raison](011-performance.md#rper-reason)
* [Per.2 : Ne pas optimiser prématurément](011-performance.md#rper-knuth)
* [Per.3 : Ne pas optimiser ce qui n'est pas critique en termes de performance](011-performance.md#rper-critical)
* [Per.4 : Ne pas supposer que du code complexe est nécessairement plus rapide que du code simple](011-performance.md#rper-simple)
* [Per.5 : Ne pas supposer que du code bas niveau est nécessairement plus rapide que du code haut niveau](011-performance.md#rper-low)
* [Per.6 : Ne pas faire d'affirmations sur les performances sans mesures](011-performance.md#rper-measure)
* [Per.7 : Concevoir pour permettre l'optimisation](011-performance.md#rper-efficiency)
* [Per.10 : S'appuyer sur le système de types statique](011-performance.md#rper-type)
* [Per.11 : Déplacer les calculs du temps d'exécution vers le temps de compilation](011-performance.md#rper-comp)
* [Per.12 : Éliminer les alias redondants](011-performance.md#rper-alias)
* [Per.13 : Éliminer les indirections redondantes](011-performance.md#rper-indirect)
* [Per.14 : Minimiser le nombre d'allocations et de désallocations](011-performance.md#rper-alloc)
* [Per.15 : Ne pas allouer sur une branche critique](011-performance.md#rper-alloc0)
* [Per.16 : Utiliser des structures de données compactes](011-performance.md#rper-compact)
* [Per.17 : Déclarer en premier le membre le plus utilisé d'une structure sensible au temps](011-performance.md#rper-struct)
* [Per.18 : L'espace, c'est du temps](011-performance.md#rper-space)
* [Per.19 : Accéder à la mémoire de manière prévisible](011-performance.md#rper-access)
* [Per.30 : Éviter les bascules de contexte sur le chemin critique](011-performance.md#rper-context)

### <a name="rper-reason"></a>Per.1 : Ne pas optimiser sans raison

##### Justification

S'il n'y a pas besoin d'optimisation, le résultat principal de l'effort sera davantage d'erreurs et des coûts de maintenance plus élevés.

##### Remarque

Certaines personnes optimisent par habitude ou parce que c'est amusant.

???

### <a name="rper-knuth"></a>Per.2 : Ne pas optimiser prématurément

##### Justification

Un code soigneusement optimisé est généralement plus volumineux et plus difficile à modifier qu'un code non optimisé.

???

### <a name="rper-critical"></a>Per.3 : Ne pas optimiser ce qui n'est pas critique en termes de performance

##### Justification

Optimiser une partie non critique d'un programme n'a aucun effet sur les performances du système.

##### Remarque

Si votre programme passe la majeure partie de son temps à attendre le réseau ou un humain, l'optimisation des calculs en mémoire est probablement inutile.

Autrement dit : si votre programme passe 4 % de son temps de traitement sur le calcul A et 40 % sur le calcul B, une amélioration de 50 % sur A n'a qu'un impact équivalent à une amélioration de 5 % sur B. (Si vous ne savez même pas combien de temps est consacré à A ou B, voir <a href="#rper-reason">Per.1</a> et <a href="#rper-knuth">Per.2</a>.)

### <a name="rper-simple"></a>Per.4 : Ne pas supposer que du code complexe est nécessairement plus rapide que du code simple

##### Justification

Un code simple peut être très rapide. Les optimiseurs parviennent parfois à des merveilles avec du code simple.

##### Exemple, bon

    // expression claire de l'intention, exécution rapide

    vector<uint8_t> v(100000);

    for (auto& c : v)
        c = ~c;

##### Exemple, mauvais

    // censé être plus rapide, mais souvent plus lent

    vector<uint8_t> v(100000);

    for (size_t i = 0; i < v.size(); i += sizeof(uint64_t)) {
        uint64_t& quad_word = *reinterpret_cast<uint64_t*>(&v[i]);
        quad_word = ~quad_word;
    }

##### Remarque

???

???

### <a name="rper-low"></a>Per.5 : Ne pas supposer que du code bas niveau est nécessairement plus rapide que du code haut niveau

##### Justification

Le code bas niveau peut parfois entraver les optimisations. Les optimiseurs parviennent parfois à des merveilles avec du code haut niveau.

##### Remarque

???

???

### <a name="rper-measure"></a>Per.6 : Ne pas faire d'affirmations sur les performances sans mesures

##### Justification

Le domaine des performances est jonché de mythes et de folklore douteux.
Le matériel moderne et les optimiseurs défient les suppositions naïves ; même les experts sont régulièrement surpris.

##### Remarque

Obtenir de bonnes mesures de performance peut être difficile et nécessiter des outils spécialisés.

##### Remarque

Quelques micro-benchmarks simples utilisant `time` sous Unix ou la bibliothèque standard `<chrono>` peuvent aider à dissiper les mythes les plus évidents.
Si vous ne pouvez pas mesurer précisément votre système complet, essayez au moins de mesurer quelques-unes de vos opérations et algorithmes clés.
Un profilageur peut vous aider à identifier quelles parties de votre système sont critiques en termes de performance.
Souvent, vous serez surpris.

???

### <a name="rper-efficiency"></a>Per.7 : Concevoir pour permettre l'optimisation

##### Justification

Parce que nous avons souvent besoin d'optimiser la conception initiale.
Parce qu'une conception qui ignore la possibilité d'améliorations ultérieures est difficile à modifier.

##### Exemple

D'après le standard C (et C++) :

    void qsort (void* base, size_t num, size_t size, int (*compar)(const void*, const void*));

Quand avez-vous vraiment eu besoin de trier de la mémoire brute ?
En réalité, nous trions des séquences d'éléments, généralement stockés dans des conteneurs.
Un appel à `qsort` jette par la fenêtre beaucoup d'informations utiles (par exemple, le type des éléments), oblige l'utilisateur à répéter des informations
déjà connues (par exemple, la taille des éléments) et oblige l'utilisateur à écrire du code supplémentaire (par exemple, une fonction pour comparer des `double`).
Cela implique un travail supplémentaire pour le programmeur, est source d'erreurs, et prive le compilateur d'informations nécessaires à l'optimisation.

    double data[100];
    // ... remplir data ...

    // 100 blocs de mémoire de sizeof(double) commençant à
    // l'adresse data, en utilisant l'ordre défini par compare_doubles
    qsort(data, 100, sizeof(double), compare_doubles);

Du point de vue de la conception d'interface, `qsort` jette par la fenêtre des informations utiles.

Nous pouvons faire mieux (en C++98) :

    template<typename Iter>
        void sort(Iter b, Iter e);  // trie [b:e)

    sort(data, data + 100);

Ici, nous exploitons la connaissance du compilateur sur la taille du tableau, le type des éléments et la manière de comparer des `double`.

Avec C++20, nous pouvons faire encore mieux :

    // sortable spécifie que c doit être une
    // séquence à accès aléatoire d'éléments comparables avec <
    void sort(sortable auto& c);

    sort(c);

L'essentiel est de transmettre suffisamment d'informations pour qu'une bonne implémentation puisse être choisie.
À cet égard, les interfaces `sort` présentées ici ont encore une faiblesse :
elles s'appuient implicitement sur le fait que le type des éléments définit un opérateur moins que (`<`).
Pour compléter l'interface, nous avons besoin d'une seconde version qui accepte un critère de comparaison :

    // compare les éléments de c en utilisant r
    template<random_access_range R, class C> requires sortable<R, C>
    void sort(R&& r, C c);

La spécification de la bibliothèque standard pour `sort` propose ces deux versions, et d'autres encore.

##### Remarque

L'optimisation prématurée est réputée être [la racine de tout mal](011-performance.md#rper-knuth), mais ce n'est pas une raison pour mépriser les performances.
Il n'est jamais prématuré de réfléchir à ce qui rend une conception propice à l'amélioration, et une meilleure performance est une amélioration couramment recherchée.
Visez à développer un ensemble d'habitudes qui, par défaut, produit un code efficace, maintenable et optimisable.
En particulier, lorsque vous écrivez une fonction qui n'est pas un détail d'implémentation ponctuel, considérez :

* Transmission d'informations :
Préférez des [interfaces](005-interfaces.md) propres, portant suffisamment d'informations pour permettre une amélioration ultérieure de l'implémentation.
Notez que les informations entrent et sortent d'une implémentation à travers les interfaces que nous fournissons.
* Données compactes : par défaut, [utilisez des données compactes](011-performance.md#rper-compact), telles que `std::vector`, et [accédez-y de manière systématique](011-performance.md#rper-access).
Si vous pensez avoir besoin d'une structure chaînée, essayez de concevoir l'interface de sorte que cette structure ne soit pas visible par les utilisateurs.
* Passage des arguments de fonction et retour de valeur :
Distinguez entre les données mutables et non mutables.
N'imposez pas à vos utilisateurs une charge de gestion des ressources.
N'imposez pas à vos utilisateurs des indirections inutiles au temps d'exécution.
Utilisez les [manières conventionnelles](006-functions.md#rf-conventional) de transmettre des informations à travers une interface ;
les manières non conventionnelles et/ou « optimisées » de transmettre des données peuvent sérieusement compliquer une réimplémentation ultérieure.
* Abstraction :
Ne généralisez pas excessivement ; une conception qui tente de couvrir tous les usages possibles (et abus) et qui diffère toute décision de conception pour plus tard
(en utilisant des indirections au temps de compilation ou d'exécution) est généralement un enchevêtrement complexe, gonflé et difficile à comprendre.
Généralisez à partir d'exemples concrets, en préservant les performances lors de la généralisation.
Ne généralisez pas sur la base de simples spéculations sur des besoins futurs.
L'idéal est une généralisation sans surcoût.
* Bibliothèques :
Utilisez des bibliothèques aux interfaces de qualité.
Si aucune bibliothèque n'est disponible, construisez-en une vous-même et imitez le style d'interface d'une bonne bibliothèque.
La [bibliothèque standard](#sl-the-standard-library) @TODO-LINK est un bon premier endroit où chercher de l'inspiration.
* Isolation :
Isolez votre code du code désordonné et/ou de l'ancien style en fournissant une interface de votre choix vers ce code.
On appelle parfois cela « fournir un wrapper » pour le code utile/nécessaire mais désordonné.
Ne laissez pas les mauvaises conceptions « contaminer » votre code.

##### Exemple

Considérez :

    template<class ForwardIterator, class T>
    bool binary_search(ForwardIterator first, ForwardIterator last, const T& val);

`binary_search(begin(c), end(c), 7)` vous dira si `7` est dans `c` ou non.
Cependant, il ne vous dira pas où se trouve ce `7` ni s'il y en a plus d'un.

Parfois, renvoyer simplement le minimum d'informations (ici, `true` ou `false`) suffit, mais une bonne interface renvoie
les informations nécessaires à l'appelant. C'est pourquoi la bibliothèque standard propose également :

    template<class ForwardIterator, class T>
    ForwardIterator lower_bound(ForwardIterator first, ForwardIterator last, const T& val);

`lower_bound` renvoie un itérateur vers la première occurrence s'il y en a une, sinon vers le premier élément supérieur à `val`, ou `last` si aucun tel élément n'est trouvé.

Cependant, `lower_bound` ne renvoie toujours pas assez d'informations pour tous les usages, c'est pourquoi la bibliothèque standard propose aussi :

    template<class ForwardIterator, class T>
    pair<ForwardIterator, ForwardIterator>
    equal_range(ForwardIterator first, ForwardIterator last, const T& val);

`equal_range` renvoie un `pair` d'itérateurs spécifiant la première occurrence et l'élément juste après la dernière occurrence.

    auto r = equal_range(begin(c), end(c), 7);
    for (auto p = r.first; p != r.second; ++p)
        cout << *p << '\n';

Évidemment, ces trois interfaces sont implémentées par le même code de base.
Ce sont simplement trois manières de présenter l'algorithme de recherche binaire de base aux utilisateurs,
allant du plus simple (« rendre les choses simples simples ! »)
au renvoi d'informations complètes, mais pas toujours nécessaires (« ne masquez pas les informations utiles »).
Naturellement, concevoir un tel ensemble d'interfaces exige de l'expérience et des connaissances du domaine.

##### Remarque

Ne concevez pas simplement l'interface pour correspondre à la première implémentation et au premier cas d'usage qui vous vient à l'esprit.
Dès que votre première implémentation initiale est terminée, revolez-la ; une fois déployée, les erreurs seront difficiles à corriger.

##### Remarque

Un besoin d'efficacité n'implique pas un besoin de [code bas niveau](011-performance.md#rper-low).
Le code haut niveau n'est pas nécessairement lent ou gonflé.

##### Remarque

Les choses ont un coût.
Ne soyez pas paranoïaque à propos des coûts (les ordinateurs modernes sont vraiment très rapides),
mais ayez une idée approximative de l'ordre de grandeur du coût de ce que vous utilisez.
Par exemple, ayez une idée approximative du coût de
un accès mémoire,
un appel de fonction,
une comparaison de chaînes,
un appel système,
un accès disque,
et un message à travers un réseau.

##### Remarque

Si vous ne pouvez penser qu'à une seule implémentation, vous n'avez probablement pas quelque chose pour lequel vous pouvez concevoir une interface stable.
Peut-être est-ce simplement un détail d'implémentation — tout le code n'a pas besoin d'une interface stable — mais prenez un moment pour y réfléchir.
Une question qui peut être utile est
« quelle interface serait nécessaire si cette opération devait être implémentée en utilisant plusieurs threads ? être vectorisée ? »

##### Remarque

Cette règle ne contredit pas la règle [Ne pas optimiser prématurément](011-performance.md#rper-knuth).
Elle la complète, en encourageant les développeurs à permettre une optimisation ultérieure — appropriée et non prématurée — si et où nécessaire.

##### Application

Délicat.
Peut-être que la recherche d'arguments de fonction `void*` permettra de trouver des exemples d'interfaces qui entravent l'optimisation ultérieure.

### <a name="rper-type"></a>Per.10 : S'appuyer sur le système de types statique

##### Justification

Les violations de type, les types faibles (par exemple `void*`) et le code bas niveau (par exemple, la manipulation de séquences comme des octets individuels) rendent le travail de l'optimiseur beaucoup plus difficile. Un code simple s'optimise souvent mieux qu'un code complexe élaboré à la main.

???

### <a name="rper-comp"></a>Per.11 : Déplacer les calculs du temps d'exécution vers le temps de compilation

##### Justification

Pour réduire la taille du code et le temps d'exécution.
Pour éviter les courses d'accès aux données en utilisant des constantes.
Pour détecter les erreurs au temps de compilation (et ainsi éliminer le besoin de code de gestion d'erreurs).

##### Exemple

    double square(double d) { return d*d; }
    static double s2 = square(2);    // ancien style : initialisation dynamique

    constexpr double ntimes(double d, int n)   // suppose 0 <= n
    {
            double m = 1;
            while (n--) m *= d;
            return m;
    }
    constexpr double s3 {ntimes(2, 3)};  // style moderne : initialisation au temps de compilation

Un code comme l'initialisation de `s2` n'est pas rare, surtout pour une initialisation un peu plus complexe que `square()`.
Cependant, par rapport à l'initialisation de `s3`, il y a deux problèmes :

* nous subissons le surcoût d'un appel de fonction au temps d'exécution
* `s2` pourrait tout simplement être accédé par un autre thread avant que l'initialisation n'ait lieu.

Remarque : on ne peut pas avoir de course d'accès aux données sur une constante.

##### Exemple

Considérez une technique populaire pour fournir un gestionnaire qui stocke les petits objets dans le gestionnaire lui-même et les plus grands sur le tas.

    constexpr int on_stack_max = 20;

    template<typename T>
    struct Scoped {     // stocke un T dans Scoped
            // ...
        T obj;
    };

    template<typename T>
    struct On_heap {    // stocke un T sur le tas
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

Supposons que `Scoped` et `On_heap` fournissent des interfaces utilisateur compatibles.
Ici, nous calculons le type optimal à utiliser au temps de compilation.
Il existe des techniques similaires pour sélectionner la fonction optimale à appeler.

##### Remarque

L'idéal est de *ne pas* essayer d'exécuter tout au temps de compilation.
Évidemment, la plupart des calculs dépendent des entrées, donc ils ne peuvent pas être déplacés au temps de compilation,
mais au-delà de cette contrainte logique, le fait est qu'un calcul complexe au temps de compilation peut sérieusement augmenter les temps de compilation
et compliquer le débogage.
Il est même possible de ralentir le code par un calcul au temps de compilation.
C'est admittedly rare, mais en factorisant un calcul général en sous-calculs optimaux séparés, il est possible de rendre le cache d'instructions moins efficace.

##### Application

* Cherchez des fonctions simples qui pourraient être `constexpr` (mais ne le sont pas).
* Cherchez des fonctions appelées avec des arguments qui sont tous des expressions constantes.
* Cherchez des macros qui pourraient être `constexpr`.

### <a name="rper-alias"></a>Per.12 : Éliminer les alias redondants

???

### <a name="rper-indirect"></a>Per.13 : Éliminer les indirections redondantes

???

### <a name="rper-alloc"></a>Per.14 : Minimiser le nombre d'allocations et de désallocations

???

### <a name="rper-alloc0"></a>Per.15 : Ne pas allouer sur une branche critique

???

### <a name="rper-compact"></a>Per.16 : Utiliser des structures de données compactes

##### Justification

Les performances sont typiquement dominées par les temps d'accès à la mémoire.

???

### <a name="rper-struct"></a>Per.17 : Déclarer en premier le membre le plus utilisé d'une structure sensible au temps

???

### <a name="rper-space"></a>Per.18 : L'espace, c'est du temps

##### Justification

Les performances sont typiquement dominées par les temps d'accès à la mémoire.

???

### <a name="rper-access"></a>Per.19 : Accéder à la mémoire de manière prévisible

##### Justification

Les performances sont très sensibles aux performances du cache, et les algorithmes de cache favorisent un accès simple (généralement linéaire) aux données adjacentes.

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

### <a name="rper-context"></a>Per.30 : Éviter les bascules de contexte sur le chemin critique

???
