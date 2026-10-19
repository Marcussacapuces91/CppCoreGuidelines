<a name="s-performance"></a>Per: Performance

??? Cette section devrait-elle figurer dans le guide principal ??? 

Cette section contient des règles destinées aux personnes qui ont besoin de haute performance ou de faible latence. Autrement dit, ces règles concernent la façon d'utiliser le moins de temps et de ressources possible pour accomplir une tâche dans un délai prévisible. Les règles de cette section sont plus restrictives et intrusives que ce qui est nécessaire pour la majorité des applications. Ne tentez pas naïvement de les appliquer dans le code général : atteindre les objectifs de faible latence nécessite un travail supplémentaire.

Résumé des règles de performance :

* [Per.1: Ne pas optimiser sans raison](011-performance.md#rper-reason)
* [Per.2: Ne pas optimiser prématurément](011-performance.md#rper-knuth)
* [Per.3: Ne pas optimiser une partie qui n'est pas critique en termes de performance](011-performance.md#rper-critical)
* [Per.4: Ne pas supposer qu'un code compliqué est forcément plus rapide qu'un code simple](011-performance.md#rper-simple)
* [Per.5: Ne pas supposer qu'un code bas niveau est forcément plus rapide qu'un code haut niveau](011-performance.md#rper-low)
* [Per.6: Ne pas faire d'affirmations sur les performances sans mesures](011-performance.md#rper-measure)
* [Per.7: Concevoir pour permettre l'optimisation](011-performance.md#rper-efficiency)
* [Per.10: S'appuyer sur le système de types statiques](011-performance.md#rper-type)
* [Per.11: Déplacer le calcul de l'exécution vers la compilation](011-performance.md#rper-comp)
* [Per.12: Éliminer les alias redondants](011-performance.md#rper-alias)
* [Per.13: Éliminer les indirections redondantes](011-performance.md#rper-indirect)
* [Per.14: Minimiser le nombre d'allocation et de désallocation](011-performance.md#rper-alloc)
* [Per.15: Ne pas allouer dans une branche critique](011-performance.md#rper-alloc0)
* [Per.16: Utiliser des structures de données compactes](011-performance.md#rper-compact)
* [Per.17: Déclarer le membre le plus utilisé d'une structure critique en temps en premier](011-performance.md#rper-struct)
* [Per.18: L'espace, c'est du temps](011-performance.md#rper-space)
* [Per.19: Accéder à la mémoire de façon prévisible](011-performance.md#rper-access)
* [Per.30: Éviter les changements de contexte sur le chemin critique](011-performance.md#rper-context)

### <a name="rper-reason"></a>Per.1: Ne pas optimiser sans raison

##### Raison

S'il n'y a pas besoin d'optimisation, le principal résultat de l'effort sera plus d'erreurs et de coûts de maintenance plus élevés.

##### Remarque

Certains optimisent par habitude ou parce que c'est amusant.

???

### <a name="rper-knuth"></a>Per.2: Ne pas optimiser prématurément

##### Raison

Un code très optimisé est généralement plus gros et plus difficile à modifier que du code non optimisé.

???

### <a name="rper-critical"></a>Per.3: Ne pas optimiser une partie qui n'est pas critique en termes de performance

##### Raison

Optimiser une partie non critique en termes de performance d'un programme n'a aucun effet sur les performances système.

##### Remarque

Si votre programme passe la majorité de son temps à attendre le web ou un humain, l'optimisation du calcul en mémoire est probablement inutile.

En d'autres termes : si votre programme passe 4 % de son temps de traitement à exécuter le calcul A et 40 % à exécuter le calcul B, une amélioration de 50 % sur A n'est impactante que d'une amélioration de 5 % sur B. (Si vous ne savez même pas combien de temps est passé sur A ou B, consultez <a href="#rper-reason">Per.1</a> et <a href="#rper-knuth">Per.2</a>.)

### <a name="rper-simple"></a>Per.4: Ne pas supposer qu'un code compliqué est forcément plus rapide qu'un code simple

##### Raison

Un code simple peut être très rapide. Les optimiseurs peuvent parfois accomplir des merveilles avec du code simple.

##### Exemple, bon

    // expression claire de l'intention, exécution rapide

    vector<uint8_t> v(100000);

    for (auto& c : v)
        c = ~c;

##### Exemple, mauvais

    // censé être plus rapide, mais est souvent plus lent

    vector<uint8_t> v(100000);

    for (size_t i = 0; i < v.size(); i += sizeof(uint64_t)) {
        uint64_t& quad_word = *reinterpret_cast<uint64_t*>(&v[i]);
        quad_word = ~quad_word;
    }

##### Remarque

???

???

### <a name="rper-low"></a>Per.5: Ne pas supposer qu'un code bas niveau est forcément plus rapide qu'un code haut niveau

##### Raison

Un code bas niveau peut parfois inhiber les optimisations. Les optimiseurs peuvent parfois accomplir des merveilles avec du code haut niveau.

##### Remarque

???

???

### <a name="rper-measure"></a>Per.6: Ne pas faire d'affirmations sur les performances sans mesures

##### Raison

Le domaine des performances est rempli de mythes et de folklore injustifié. Le matériel moderne et les optimiseurs défient les suppositions naïves ; même les experts sont régulièrement surpris.

##### Remarque

Obtenir de bonnes mesures de performance peut être difficile et nécessiter des outils spécialisés.

##### Remarque

Quelques micro-benchmarks simples utilisant Unix `time` ou la bibliothèque standard `<chrono>` peuvent aider à dissiper les mythes les plus évidents. Si vous ne pouvez pas mesurer votre système complet avec précision, essayez au moins de mesurer quelques-unes de vos opérations et algorithmes clés. Un profilé peut vous aider à identifier les parties de votre système critiques en termes de performance. Souvent, vous serez surpris.

???

### <a name="rper-efficiency"></a>Per.7: Concevoir pour permettre l'optimisation

##### Raison

Parce que nous avons souvent besoin d'optimiser la conception initiale, et qu'une conception qui ignore la possibilité d'amélioration future est difficile à modifier.

##### Exemple

À partir du standard C (et C++) :

    void qsort(void* base, size_t num, size_t size, int (*compar)(const void*, const void*));

Quand avez‑vous vraiment besoin de trier de la mémoire ? En réalité, nous trions des séquences d'éléments, généralement stockées dans des conteneurs. Un appel à `qsort` jette beaucoup d'informations utiles (par ex. le type d'élément), force l'utilisateur à répéter des informations déjà connues (par ex. la taille d'élément), et force l'utilisateur à écrire un code supplémentaire (par ex. une fonction pour comparer les `double`). Cela implique un travail supplémentaire pour le programmeur, est sujet à erreurs, et prive le compilateur des informations nécessaires à l'optimisation.

    double data[100];
    // ... remplir ...

    // 100 blocs de mémoire de sizeof(double) à partir de
    // l'adresse data en utilisant l'ordre défini par compare_doubles
    qsort(data, 100, sizeof(double), compare_doubles);

Du point de vue de la conception d'interface, `qsort` jette des informations utiles.

Nous pouvons faire mieux (en C++98)

    template<typename Iter>
    void sort(Iter b, Iter e);  // tri [b:e)

    sort(data, data + 100);

Ici, nous utilisons les connaissances du compilateur concernant la taille du tableau, le type des éléments, et comment comparer les `double`.

Avec C++20, nous pouvons encore mieux faire

    // sortable spécifie que c doit être un
    // séquence d'accès aléatoire d'éléments comparables avec <
    void sort(sortable auto& c);

    sort(c);

Le point clé est de fournir suffisamment d'informations pour qu'une bonne implémentation soit choisie. Dans cette interaction, les interfaces `sort` présentées ici présentent encore une faiblesse : elles comptent implicitement que le type d'élément a défini l'opérateur `<` (`<`). Pour compléter l'interface, nous avons besoin d'une seconde version qui accepte un critère de comparaison :

    template<random_access_range R, class C> requires sortable<R, C>
    void sort(R&& r, C c);

La spécification de la bibliothèque standard de `sort` propose ces deux versions, et plus.

##### Remarque

Il est dit que l'optimisation prématurée est la racine de tout mal, mais ce n'est pas une raison de mépriser la performance. Il n'est jamais prématuré de considérer ce qui rend une conception favorable à l'amélioration, et l'amélioration des performances est une amélioration couramment souhaitée. S'efforcer de créer un ensemble d'habitudes qui, par défaut, donne un code efficace, maintenable et optimisable. En particulier, lorsque vous écrivez une fonction qui n'est pas un détail d'implémentation unique, considérez :

* Passage d'informations : Préférez des interfaces propres [interfaces](005-interfaces.md) transportant suffisamment d'informations pour l'amélioration ultérieure de l'implémentation. Notez que l'information circule vers et hors d'une implémentation à travers les interfaces que nous fournissons.
* Données compactes : Par défaut, [utilisez des données compactes](011-performance.md#rper-compact), telles que `std::vector` et [accédez‑y de façon systématique](011-performance.md#rper-access). Si vous pensez avoir besoin d'une structure liée, essayez de concevoir l'interface de sorte que cette structure ne soit pas visible par les utilisateurs.
* Passage d'arguments et retours de fonctions : Différenciez les données mutables et non mutables. Ne imposez pas de charge de gestion de ressources à vos utilisateurs. Ne imposez pas d'indirections de temps d'exécution superflues à vos utilisateurs. Utilisez les [moyens conventionnels](006-functions.md#rf-conventional) de passer des informations via une interface ; les moyens non conventionnels ou « optimisés » de passer des données peuvent compliquer sérieusement une réimplémentation ultérieure.
* Abstraction : Ne surchargez pas trop l'abstraction ; un design qui tente de répondre à toutes les utilisations possibles (et erreurs) et reporte chaque décision de conception à plus tard (à l'aide d'indirections de temps d'exécution ou de compilation) est généralement un désordre compliqué, gonflé et difficile à comprendre. Généralisiez à partir d'exemples concrets tout en préservant les performances. Ne généralisez pas sur la seule base de spéculations sur les besoins futurs. L'idéal est une généralisation sans surcoût.
* Bibliothèques : Utilisez des bibliothèques avec de bonnes interfaces. S'il n'existe pas de bibliothèque adaptée, construisez-en une vous-même et imitez le style d'interface d'une bonne bibliothèque. La [bibliothèque standard](#sl-the-standard-library) est une première bonne source d'inspiration.
* Isolement : Isolez votre code du code désordonné et/ou de style ancien en lui fournissant une interface de votre choix. Cela est parfois appelé « fournir un wrapper » pour le code utile / nécessaire mais désordonné. Ne laissez pas de mauvaises conceptions « se propager » dans votre code.

##### Exemple

Considérez :

    template<class ForwardIterator, class T>
    bool binary_search(ForwardIterator first, ForwardIterator last, const T& val);

binary_search(begin(c), end(c), 7) vous indiquera si 7 est dans c ou non.  
Cependant, il ne vous indiquera pas où cette 7 se trouve ou s'il y a plus d'un 7.

Parfois, simplement retourner le montant minimal d'information rendu (ici, vrai ou faux) suffit, mais une bonne interface transmet des informations nécessaires au rappel. Par conséquent, la bibliothèque standard propose également

    template<class ForwardIterator, class T>
    ForwardIterator lower_bound(ForwardIterator first, ForwardIterator last, const T& val);

lower_bound renvoie un itérateur vers la première correspondance s'il y en a une, sinon vers le premier élément supérieur à val, ou last s'il n'y a pas d'élément correspondant.

Cependant lower_bound ne renvoie pas suffisamment d'informations pour toutes les utilisations, c'est pourquoi la bibliothèque standard propose également

    template<class ForwardIterator, class T>
    pair<ForwardIterator, ForwardIterator>
    equal_range(ForwardIterator first, ForwardIterator last, const T& val);

equal_range renvoie une paire d'itérateurs spécifiant le premier et un après le dernier correspondant.

    auto r = equal_range(begin(c), end(c), 7);
    for (auto p = r.first; p != r.second; ++p)
        cout << *p << '\n';

Évidemment, ces trois interfaces sont implémentées par le même code de base. Ce ne sont que trois façons de présenter l'algorithme de recherche binaire de base aux utilisateurs, passant du plus simple (« Simplifier les choses simples ! ») à la fourniture d'informations complètes, mais pas toujours nécessaires (« ne pas masquer les informations utiles »). Naturellement, créer un tel ensemble d'interfaces nécessite de l'expérience et des connaissances spécialisées.

##### Remarque

Ne créez pas simplement l'interface pour correspondre à votre première implémentation et le premier cas d'utilisation que vous envisagez. Une fois votre première implémentation initiale terminée, passez‑la en revue ; une fois déployée, les erreurs seront difficiles à corriger.

##### Remarque

Un besoin d'efficacité n'implique pas un besoin de code bas niveau. Un code haut niveau n'est pas forcément lent ou gonflé.

##### Remarque

Les choses ont un coût. Ne soyez pas paranoïaque à propos des coûts (les ordinateurs modernes sont vraiment très rapides), mais ayez une idée approximative de l'ordre de grandeur des coûts de ce que vous utilisez. Par exemple, ayez une idée approximative du coût d'un accès mémoire, d'un appel de fonction, d'une comparaison de chaîne, d'un appel système, d'un accès disque, et d'un message via un réseau.

##### Remarque

Si vous ne pensez qu'à une seule implémentation, vous n'avez probablement pas quelque chose pour lequel vous pouvez concevoir une interface stable. Il se peut que ce soit simplement un détail d'implémentation — chaque morceau de code n'a pas besoin d'une interface stable — mais prenez un moment pour réfléchir. Une question utile serait « quelle interface serait nécessaire si cette opération devait être implémentée en utilisant plusieurs threads ou vectorisée ? »

##### Remarque

Cette règle ne contredit pas la règle [Ne pas optimiser prématurément](011-performance.md#rper-knuth). Elle le complète, en encourageant les développeurs à autoriser une optimisation tardive — appropriée et non prématurée — lorsqu'elle est nécessaire.

##### Application

Difficile ; peut-être qu'en cherchant des arguments de fonction `void*` on trouvera des exemples d'interfaces qui entravent l'optimisation ultérieure.

<a name="rper-type"></a>Per.10: S'appuyer sur le système de types statiques

##### Raison

Les violations de type, les types faibles (par ex. `void*`) et le code bas niveau (par ex. la manipulation de séquences comme des octets individuels) rendent le travail de l'optimiseur beaucoup plus difficile. Un code simple optimise souvent mieux qu'un code complexe fabriqué à la main.

<a name="rper-comp"></a>Per.11: Déplacer le calcul de l'exécution vers la compilation

##### Raison

Réduire la taille du code et le temps d'exécution. Éviter les conditions de concurrence en utilisant des constantes. Détecter les erreurs à la compilation (et ainsi éliminer le besoin de code de gestion d'erreurs).

##### Exemple

    double square(double d) { return d*d; }
    static double s2 = square(2);    // style ancien : initialisation dynamique

    constexpr double ntimes(double d, int n)   // assume 0 <= n
    {
            double m = 1;
            while (n--) m *= d;
            return m;
    }
    constexpr double s3 {ntimes(2, 3)};  // style moderne : initialisation au moment de la compilation

##### Exemple

Considérons une technique populaire pour fournir un gestionnaire pour stocker de petits objets dans le gestionnaire lui‑même et les plus grands sur le tas.

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
                On_heap<T>      // seconde alternative
           >::type;

    void f()
    {
        Handle<double> v1;                   // le double part sur la pile
        Handle<std::array<double, 200>> v2;  // le tableau part sur le tas
        // ...
    }

Supposons que `Scoped` et `On_heap` offrent des interfaces utilisateur compatibles. Ici, nous calculons le type optimal à utiliser à la compilation. Il existe des techniques similaires pour sélectionner la fonction optimale à appeler.

##### Remarque

L'idéal n'est pas d'essayer d'exécuter tout à la compilation. Évidemment, la plupart des calculs dépendent des entrées, donc ils ne peuvent pas être déplacés à la compilation, mais au-delà de cette contrainte logique, il est possible que des calculs complexes à la compilation augmentent considérablement les temps de compilation et compliquent le débogage. Il est même possible de ralentir le code par des calculs à la compilation.

##### Application

* Cherchez des fonctions simples qui pourraient être `constexpr` (mais ne le sont pas).
* Cherchez des fonctions appelées avec tous les arguments exprressés en constantes.
* Cherchez des macros qui pourraient être `constexpr`.

<a name="rper-alias"></a>Per.12: Éliminer les alias redondants

<a name="rper-indirect"></a>Per.13: Éliminer les indirections redondantes

<a name="rper-alloc"></a>Per.14: Minimiser le nombre d'allocation et de désallocation

<a name="rper-alloc0"></a>Per.15: Ne pas allouer dans une branche critique

<a name="rper-compact"></a>Per.16: Utiliser des structures de données compactes

##### Raison

La performance est généralement dominée par les temps d'accès mémoire.

???

<a name="rper-struct"></a>Per.17: Déclarer le membre le plus utilisé d'une structure critique en temps en premier

<a name="rper-space"></a>Per.18: L'espace, c'est du temps

##### Raison

La performance est généralement dominée par les temps d'accès mémoire.

???

<a name="rper-access"></a>Per.19: Accéder à la mémoire de façon prévisible

##### Raison

Les performances sont très sensibles aux performances cache, et les algorithmes de cache favorisent un accès simple (généralement linéaire) aux données adjacentes.

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

<a name="rper-context"></a>Per.30: Éviter les changements de contexte sur le chemin critique

???