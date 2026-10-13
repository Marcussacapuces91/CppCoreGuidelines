# <a name="s-performance"></a>Per : Performance

??? cette section devrait-elle figurer dans le guide principal ???

Cette section contient des règles destinées à ceux qui ont besoin de hautes performances ou d'une faible latence.
Autrement dit, il s'agit de règles relatives à l'accomplissement d'une tâche dans un délai court prévisible, en utilisant le minimum de temps et de ressources possible.
Les règles de cette section sont plus restrictives et plus intrusives que ce qui est nécessaire pour de nombreuses (la plupart des) applications.
Ne cherchez pas naïvement à les suivre dans du code général : atteindre l'objectif d'une faible latence requiert un travail supplémentaire.

Résumé des règles de performance :

* [Per.1 : Ne pas optimiser sans raison](011-performance.md#rper-reason)
* [Per.2 : Ne pas optimiser prématurément](011-performance.md#rper-knuth)
* [Per.3 : Ne pas optimiser ce qui n'est pas critique en termes de performance](011-performance.md#rper-critical)
* [Per.4 : Ne pas supposer qu'un code complexe est nécessairement plus rapide qu'un code simple](011-performance.md#rper-simple)
* [Per.5 : Ne pas supposer qu'un code bas niveau est nécessairement plus rapide qu'un code de haut niveau](011-performance.md#rper-low)
* [Per.6 : Ne pas formuler d'affirmations sur la performance sans mesures](011-performance.md#rper-measure)
* [Per.7 : Concevoir pour permettre l'optimisation](011-performance.md#rper-efficiency)
* [Per.10 : S'appuyer sur le système de types statique](011-performance.md#rper-type)
* [Per.11 : Déplacer les calculs du temps d'exécution au temps de compilation](011-performance.md#rper-comp)
* [Per.12 : Éliminer les alias redondants](011-performance.md#rper-alias)
* [Per.13 : Éliminer les indirections redondantes](011-performance.md#rper-indirect)
* [Per.14 : Minimiser le nombre d'allocations et de désallocations](011-performance.md#rper-alloc)
* [Per.15 : Ne pas effectuer d'allocation sur un chemin critique](011-performance.md011-performance.md#rper-alloc0)
* [Per.16 : Utiliser des structures de données compactes](011-performance.md011-performance.md#rper-compact)
* [Per.17 : Déclarer d'abord le membre le plus utilisé d'une structure sensible au temps](011-performance.md#rper-struct)
* [Per.18 : L'espace, c'est du temps](011-performance.md#rper-space)
* [Per.19 : Accéder à la mémoire de manière prévisible](011-performance.md#rper-access)
* [Per.30 : Éviter les changements de contexte sur le chemin critique](011-performance.md#rper-context)

### <a name="rper-reason"></a>Per.1 : Ne pas optimiser sans raison

##### Justification

En l'absence de besoin d'optimisation, le principal résultat de cet effort sera davantage d'erreurs et des coûts de maintenance plus élevés.

##### Note

Certaines personnes optimisent par habitude ou par plaisir.

???

### <a name="rper-knuth"></a>Per.2 : Ne pas optimiser prématurément

##### Justification

Un code élaboré avec des optimisations est généralement plus volumineux et plus difficile à modifier qu'un code non optimisé.

???

### <a name="rper-critical"></a>Per.3 : Ne pas optimiser ce qui n'est pas critique en termes de performance

##### Justification

L'optimisation d'une partie non critique d'un point de vue performance d'un programme n'a aucun effet sur la performance globale du système.

##### Note

Si votre programme passe la majorité de son temps à attendre le réseau ou un humain, l'optimisation des calculs en mémoire est probablement inutile.

Autrement dit : si votre programme consacre 4 % de son temps de traitement au calcul A et 40 % au calcul B, une amélioration de 50 % sur A n'a d'impact qu'équivalent à une amélioration de 5 % sur B. (Si vous ignorez même combien de temps est consacré à A ou B, voir <a href="011-performance.md#rper-reason">Per.1</a> et <a
href="011-performance.md#rper-knuth">Per.2</a>.)

### <a name="rper-simple"></a>Per.4 : Ne pas supposer qu'un code complexe est nécessairement plus rapide qu'un code simple

##### Justification

Un code simple peut être très rapide. Les optimiseurs accomplissent parfois des prodiges avec un code simple.

##### Exemple, correct

    // expression claire de l'intention, exécution rapide

    vector<uint8_t> v(100000);

    for (auto& c : v)
        c = ~c;

##### Exemple, incorrect

    // censé être plus rapide, mais souvent plus lent

    vector<uint8_t> v(100000);

    for (size_t i = 0; i < v.size(); i += sizeof(uint64_t)) {
        uint64_t& quad_word = *reinterpret_cast<uint64_t*>(&v[i]);
        quad_word = ~quad_word;
    }

##### Note

???

???

### <a name="rper-low"></a>Per.5 : Ne pas supposer qu'un code bas niveau est nécessairement plus rapide qu'un code de haut niveau

##### Justification

Le code bas niveau entrave parfois les optimisations. Les optimiseurs accomplissent parfois des prodiges avec un code de haut niveau.

##### Note

???

???

### <a name="rper-measure"></a>Per.6 : Ne pas formuler d'affirmations sur la performance sans mesures

##### Justification

Le domaine de la performance est jonché de mythes et de folklore sans fondement.
Le matériel moderne et les optimiseurs contredisent les suppositions naïves ; même les experts sont régulièrement surpris.

##### Note

Obtenir de bonnes mesures de performance peut être difficile et requiert des outils spécialisés.

##### Note

Quelques micro-benchmarks simples à l'aide de `time` sous Unix ou de la bibliothèque standard `<chrono>` peuvent aider à dissiper les mythes les plus évidents.
Si vous ne pouvez pas mesurer précisément votre système complet, essayez au moins de mesurer quelques-unes de vos opérations et algorithmes clés.
Un profileur peut vous aider à identifier les parties de votre système qui sont critiques en termes de performance.
Souvent, vous serez surpris.

???

### <a name="rper-efficiency"></a>Per.7 : Concevoir pour permettre l'optimisation

##### Justification

Parce qu'il est souvent nécessaire d'optimiser la conception initiale.
Parce qu'une conception qui ignore la possibilité d'amélioration ultérieure est difficile à modifier.

##### Exemple

D'après le standard C (et C++) :

    void qsort (void* base, size_t num, size_t size, int (*compar)(const void*, const void*));

Quand est-ce que l'on a réellement voulu trier de la mémoire brute ?
En réalité, on trie des séquences d'éléments, généralement stockées dans des conteneurs.
Un appel à `qsort` jette une grande partie d'informations utiles (par exemple, le type des éléments), oblige l'utilisateur à répéter des informations
déjà connues (par exemple, la taille des éléments), et oblige l'utilisateur à écrire du code supplémentaire (par exemple, une fonction pour comparer des `double`).
Cela implique un travail supplémentaire pour le programmeur, est source d'erreurs, et prive le compilateur d'informations nécessaires à l'optimisation.

    double data[100];
    // ... remplir le tableau ...

    // 100 blocs de mémoire de sizeof(double) commençant à
    // l'adresse data, selon l'ordre défini par compare_doubles
    qsort(data, 100, sizeof(double), compare_doubles);

Du point de vue de la conception d'interface, `qsort` jette des informations utiles.

On peut faire mieux (en C++98) :

    template<typename Iter>
        void sort(Iter b, Iter e);  // trie [b:e)

    sort(data, data + 100);

Ici, nous utilisons la connaissance du compilateur quant à la taille du tableau, au type des éléments et à la manière de comparer des `double`.

Avec C++20, nous pouvons faire encore mieux :

    // sortable spécifie que c doit être une
    // séquence d'accès aléatoire d'éléments comparables avec <
    void sort(sortable auto& c);

    sort(c);

L'essentiel est de transmettre suffisamment d'informations pour qu'une bonne implémentation puisse être choisie.
À cet égard, les interfaces `sort` présentées ici présentent encore une faiblesse :
elles reposent implicitement sur le fait que le type des éléments définit un opérateur inférieur (`<`).
Pour compléter l'interface, une seconde version acceptant un critère de comparaison est nécessaire :

    // compare les éléments de c en utilisant r
    template<random_access_range R, class C> requires sortable<R, C>
    void sort(R&& r, C c);

La spécification de la bibliothèque standard de `sort` propose ces deux versions, et d'autres encore.

##### Note

L'optimisation prématurée est réputée être [la racine de tout mal](011-performance.md#rper-knuth), mais ce n'est pas une raison pour mépriser la performance.
Il n'est jamais prématuré de réfléchir à ce qui rend une conception susceptible d'être améliorée, et une meilleure performance est une amélioration fréquemment souhaitée.
Visez à développer un ensemble d'habitudes qui, par défaut, produit du code efficace, maintenable et optimisable.
En particulier, quand vous écrivez une fonction qui n'est pas un simple détail d'implémentation ponctuel, réfléchissez à :

* Transmission d'informations :
Privilégiez des [interfaces](005-interfaces.md) @TODO-LINK claires transmettant suffisamment d'informations pour une amélioration ultérieure de l'implémentation.
Notez que les informations entrent et sortent d'une implémentation à travers les interfaces que nous fournissons.
* Données compactes : Par défaut, [utilisez des structures de données compactes](011-performance.md011-performance.md#rper-compact), telles que `std::vector`, et [accédez-y de manière systématique](011-performance.md#rper-access).
Si vous pensez avoir besoin d'une structure chaînée, essayez de concevoir l'interface de sorte que cette structure ne soit pas visible par les utilisateurs.
* Passage et retour d'arguments de fonction :
Distinguez entre les données mutables et non mutables.
N'imposez pas à vos utilisateurs un fardeau de gestion des ressources.
N'imposez pas à vos utilisateurs des indirections d'exécution superflues.
Utilisez les [modes habituels](006-functions.md#rf-conventional) @TODO-LINK de transmission d'informations à travers une interface ;
les modes inhabituels et/ou « optimisés » de transmission de données peuvent sérieusement compliquer une réimplémentation ultérieure.
* Abstraction :
N'abstraitez pas de manière excessive ; une conception qui tente de couvrir tous les usages possibles (et abusifs) et qui reporte chaque décision de conception
à plus tard (en utilisant des indirections de temps de compilation ou d'exécution) est généralement un fouillis compliqué, surdimensionné et difficile à comprendre.
Abstrayez à partir d'exemples concrets, en préservant les performances lors de la généralisation.
Ne généralisez pas sur la base de simples spéculations sur des besoins futurs.
L'idéal est une généralisation sans surcoût.
* Bibliothèques :
Utilisez des bibliothèques dotées de bonnes interfaces.
Si aucune bibliothèque n'est disponible, construisez-en une vous-même en imitant le style d'interface d'une bonne bibliothèque.
La [bibliothèque standard](#sl-the-standard-library) @TODO-LINK est un bon premier endroit où chercher de l'inspiration.
* Isolement :
Isolez votre code du code mal organisé et/ou de style ancien en fournissant une interface de votre choix vers ce code.
On appelle parfois cela « fournir un enveloppe » (*wrapper*) pour le code utile/nécessaire mais mal organisé.
Ne laissez pas les mauvaises conceptions « contaminer » votre code.

##### Exemple

Considérons :

    template<class ForwardIterator, class T>
    bool binary_search(ForwardIterator first, ForwardIterator last, const T& val);

`binary_search(begin(c), end(c), 7)` vous dira si `7` est dans `c` ou non.
Cependant, il ne vous dira pas où se trouve ce `7`, ni s'il y a plus d'un `7`.

Parfois, ne renvoyer que le minimum d'informations (ici, `true` ou `false`) suffit, mais une bonne interface renvoie
les informations nécessaires à l'appelant. C'est pourquoi la bibliothèque standard propose également

    template<class ForwardIterator, class T>
    ForwardIterator lower_bound(ForwardIterator first, ForwardIterator last, const T& val);

`lower_bound` renvoie un itérateur vers la première occurrence le cas échéant, sinon vers le premier élément supérieur à `val`, ou `last` si aucun tel élément n'est trouvé.

Cependant, `lower_bound` ne renvoie toujours pas assez d'informations pour tous les usages, c'est pourquoi la bibliothèque standard propose également

    template<class ForwardIterator, class T>
    pair<ForwardIterator, ForwardIterator>
    equal_range(ForwardIterator first, ForwardIterator last, const T& val);

`equal_range` renvoie un `pair` d'itérateurs spécifiant la première et celle au-delà de la dernière occurrence.

    auto r = equal_range(begin(c), end(c), 7);
    for (auto p = r.first; p != r.second; ++p)
        cout << *p << '\n';

Évidemment, ces trois interfaces sont implémentées par le même code de base.
Ce sont simplement trois manières de présenter l'algorithme de recherche binaire de base aux utilisateurs,
allant du plus simple (« rendre les choses simples simples ! »)
au plus complet, mais pas toujours nécessaire, renvoyant toute l'information utile (« ne masquez pas d'informations utiles »).
Naturellement, forger un tel ensemble d'interfaces exige de l'expérience et une connaissance du domaine.

##### Note

Ne concevez pas l'interface simplement pour correspondre à la première implémentation et au premier cas d'usage qui vous vient à l'esprit.
Une fois votre première implémentation initiale terminée, faites-en la revue ; une fois déployée, les erreurs seront difficiles à corriger.

##### Note

Un besoin d'efficacité n'implique pas un besoin de [code bas niveau](011-performance.md#rper-low).
Le code de haut niveau n'est pas nécessairement lent ou surdimensionné.

##### Note

Tout a un coût.
Ne soyez pas paranoïaque à propos des coûts (les ordinateurs modernes sont réellement très rapides),
mais ayez une idée approximative de l'ordre de grandeur du coût de ce que vous utilisez.
Par exemple, ayez une idée approximative du coût de
un accès mémoire,
un appel de fonction,
une comparaison de chaînes,
un appel système,
un accès disque,
et un message à travers un réseau.

##### Note

Si vous ne pouvez penser qu'à une seule implémentation, vous n'avez probablement pas quelque chose pour lequel vous pouvez concevoir une interface stable.
Peut-être est-ce simplement un détail d'implémentation — tout fragment de code n'a pas besoin d'une interface stable — mais faites une pause et réfléchissez.
Une question qui peut être utile est
« quelle interface serait nécessaire si cette opération devait être implémentée en utilisant plusieurs threads ? ou être vectorisée ? »

##### Note

Cette règle ne contredit pas la règle [Ne pas optimiser prématurément](011-performance.md#rper-knuth).
Elle la complète, en encourageant les développeurs à permettre une optimisation ultérieure — appropriée et non prématurée — si et où nécessaire.

##### Application

Délicat.
Peut-être la recherche d'arguments de fonction de type `void*` permettra-t-elle de trouver des exemples d'interfaces qui entravent l'optimisation ultérieure.

### <a name="rper-type"></a>Per.10 : S'appuyer sur le système de types statique

##### Justification

Les violations de type, les types faibles (par exemple `void*`), et le code bas niveau (par exemple, la manipulation de séquences comme des octets individuels) rendent la tâche de l'optimiseur beaucoup plus difficile. Un code simple est souvent mieux optimisé qu'un code complexe élaboré à la main.

???

### <a name="rper-comp"></a>Per.11 : Déplacer les calculs du temps d'exécution au temps de compilation

##### Justification

Pour réduire la taille du code et le temps d'exécution.
Pour éviter les conditions de course en utilisant des constantes.
Pour détecter les erreurs au temps de compilation (et ainsi éliminer le besoin de code de gestion d'erreurs).

##### Exemple

    double square(double d) { return d*d; }
    static double s2 = square(2);    // style ancien : initialisation dynamique

    constexpr double ntimes(double d, int n)   // suppose 0 <= n
    {
            double m = 1;
            while (n--) m *= d;
            return m;
    }
    constexpr double s3 {ntimes(2, 3)};  // style moderne : initialisation au temps de compilation

Un code comme l'initialisation de `s2` n'est pas rare, surtout pour une initialisation un peu plus compliquée que `square()`.
Cependant, par rapport à l'initialisation de `s3`, il y a deux problèmes :

* nous subissons le surcoût d'un appel de fonction au temps d'exécution
* `s2` pourrait tout simplement être accédé par un autre thread avant que l'initialisation n'ait eu lieu.

Note : on ne peut pas avoir de condition de course sur une constante.

##### Exemple

Considérons une technique populaire pour fournir un identifiant (*handle*) permettant de stocker les petits objets dans l'identifiant lui-même et les plus grands sur le tas.

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
Ici nous calculons le type optimal à utiliser au temps de compilation.
Des techniques similaires existent pour sélectionner la fonction optimale à appeler.

##### Note

L'idéal est de *ne pas* tenter d'exécuter tout au temps de compilation.
Évidemment, la plupart des calculs dépendent d'entrées, ils ne peuvent donc pas être déplacés au temps de compilation,
mais au-delà de cette contrainte logique, le fait est qu'un calcul complexe au temps de compilation peut sérieusement augmenter les temps de compilation
et compliquer le débogage.
Il est même possible de ralentir le code par un calcul au temps de compilation.
Cela est admittedly rare, mais en factorisant un calcul général en sous-calculs optimaux séparés, il est possible de rendre le cache d'instructions moins efficace.

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

### <a name="rper-alloc0"></a>Per.15 : Ne pas effectuer d'allocation sur un chemin critique

???

### <a name="rper-compact"></a>Per.16 : Utiliser des structures de données compactes

##### Justification

La performance est généralement dominée par les temps d'accès à la mémoire.

???

### <a name="rper-struct"></a>Per.17 : Déclarer d'abord le membre le plus utilisé d'une structure sensible au temps

???

### <a name="rper-space"></a>Per.18 : L'espace, c'est du temps

##### Justification

La performance est généralement dominée par les temps d'accès à la mémoire.

???

### <a name="rper-access"></a>Per.19 : Accéder à la mémoire de manière prévisible

##### Justification

La performance est très sensible aux performances du cache, et les algorithmes de cache privilégient un accès simple (généralement linéaire) à des données adjacentes.

##### Exemple

    int matrix[rows][cols];

    // incorrect
    for (int c = 0; c < cols; ++c)
        for (int r = 0; r < rows; ++r)
            sum += matrix[r][c];

    // correct
    for (int r = 0; r < rows; ++r)
        for (int c = 0; c < cols; ++c)
            sum += matrix[r][c];

### <a name="rper-context"></a>Per.30 : Éviter les changements de contexte sur le chemin critique

???

---

**Notes de traduction :**

| Référence | Statut |
|---|---|
| `#rper-reason`, `#rper-knuth`, `#rper-critical`, `#rper-simple`, `#rper-low`, `#rper-measure`, `#rper-efficiency`, `#rper-type`, `#rper-comp`, `#rper-alias`, `#rper-indirect`, `#rper-alloc`, `#rper-alloc0`, `#rper-compact`, `#rper-struct`, `#rper-space`, `#rper-access`, `#rper-context` | ✅ Ancres présentes dans le document |
| `#sl-the-standard-library` | ⚠️ `@TODO-LINK` ajouté — ancre absente de ce document |
| `005-interfaces.md` | ⚠️ `@TODO-LINK` ajouté — fichier externe, ancre non vérifiable ici |
| `006-functions.md#rf-conventional` | ⚠️ `@TODO-LINK` ajouté — fichier externe, ancre non vérifiable ici |