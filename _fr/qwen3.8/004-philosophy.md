# <a name="s-philosophy"></a>P : Philosophie

Les règles de cette section sont très générales.

Résumé des règles philosophiques :

* [P.1 : Exprimez les idées directement dans le code](004-philosophy.md#rp-direct)
* [P.2 : Écrivez en C++ standard ISO](004-philosophy.md#rp-cplusplus)
* [P.3 : Exprimez l'intention](004-philosophy.md#rp-what)
* [P.4 : Idéalement, un programme doit être sûrement typé de manière statique](004-philosophy.md#rp-typesafe)
* [P.5 : Privilégiez la vérification au temps de compilation à celle au temps d'exécution](004-philosophy.md#rp-compile-time)
* [P.6 : Ce qui ne peut pas être vérifié au temps de compilation devrait l'être au temps d'exécution](004-philosophy.md#rp-run-time)
* [P.7 : Détectez les erreurs au temps d'exécution le plus tôt possible](004-philosophy.md#rp-early)
* [P.8 : Ne fuyez aucune ressource](004-philosophy.md#rp-leak)
* [P.9 : Ne gaspillez ni temps ni espace](004-philosophy.md#rp-waste)
* [P.10 : Privilégiez les données immuables aux données mutables](004-philosophy.md#rp-mutable)
* [P.11 : Encapsulez les constructions complexes plutôt que de les disperser dans le code](004-philosophy.md#rp-library)
* [P.12 : Utilisez les outils d'assistance le cas échéant](004-philosophy.md#rp-tools)
* [P.13 : Utilisez les bibliothèques d'assistance le cas échéant](004-philosophy.md#rp-lib)

Les règles philosophiques ne sont généralement pas vérifiables mécaniquement.
En revanche, les règles individuelles reflétant ces thèmes philosophiques le sont.
Sans un fondement philosophique, les règles plus concrètes/spécifiques/vérifiables manquent de justification.

### <a name="rp-direct"></a>P.1 : Exprimez les idées directement dans le code

##### Raison

Les compilateurs ne lisent pas les commentaires (ni les documents de conception), et de nombreux programmeurs non plus (de façon constante).
Ce qui est exprimé dans le code a une sémantique définie et peut (en principe) être vérifié par les compilateurs et d'autres outils.

##### Exemple

    class Date {
    public:
        Month month() const;  // à faire
        int month();          // à éviter
        // ...
    };

La première déclaration de `month` est explicite quant au retour d'un `Month` et au fait de ne pas modifier l'état de l'objet `Date`.
La seconde version laisse le lecteur deviner et ouvre la porte à davantage de bugs non détectés.

##### Exemple, à éviter

Cette boucle est une forme restreinte de `std::find` :

    void f(vector<string>& v)
    {
        string val;
        cin >> val;
        // ...
        int index = -1;                    // à éviter, de plus faudrait utiliser gsl::index
        for (int i = 0; i < v.size(); ++i) {
            if (v[i] == val) {
                index = i;
                break;
            }
        }
        // ...
    }

##### Exemple, recommandé

Une expression bien plus claire de l'intention serait :

    void f(vector<string>& v)
    {
        string val;
        cin >> val;
        // ...
        auto p = find(begin(v), end(v), val);  // meilleur
        // ...
    }

Une bibliothèque bien conçue exprime l'intention (ce qui doit être fait, plutôt que simplement comment quelque chose est fait) bien mieux que l'utilisation directe des fonctionnalités du langage.

Un programmeur C++ devrait connaître les bases de la bibliothèque standard et l'utiliser le cas échéant.
Tout programmeur devrait connaître les bases des bibliothèques fondamentales du projet sur lequel il travaille et les utiliser à bon escient.
Tout programmeur utilisant ces lignes directrices devrait connaître la [bibliothèque de support des lignes directrices](#gsl-guidelines-support-library) @TODO-LINK et l'utiliser à bon escient.

##### Exemple

    change_speed(double s);   // à éviter : que signifie s ?
    // ...
    change_speed(2.3);

Une meilleure approche est d'être explicite sur le sens du `double` (nouvelle vitesse ou incrément sur l'ancienne vitesse ?) et sur l'unité utilisée :

    change_speed(Speed s);    // meilleur : le sens de s est précisé
    // ...
    change_speed(2.3);        // erreur : pas d'unité
    change_speed(23_m / 10s);  // mètres par seconde

Nous aurions pu accepter un simple `double` (sans unité) comme incrément, mais cela aurait été source d'erreurs.
Si nous voulions à la fois la vitesse absolue et les incréments, nous aurions défini un type `Delta`.

##### Application

Très difficile en général.

* utiliser `const` de manière cohérente (vérifier si les fonctions membres modifient leur objet ; vérifier si les fonctions modifient des arguments passés par pointeur ou par référence)
* signaler les utilisations de conversions de type (les conversions neutralisent le système de types)
* détecter le code qui imite la bibliothèque standard (difficile)

### <a name="rp-cplusplus"></a>P.2 : Écrivez en C++ standard ISO

##### Raison

Il s'agit d'un ensemble de lignes directrices pour écrire du C++ standard ISO.

##### Remarque

Il existe des environnements où des extensions sont nécessaires, par exemple pour accéder aux ressources système.
Dans de tels cas, localisez l'utilisation des extensions nécessaires et contrôlez leur usage au moyen de lignes directrices de codage non fondamentales. Si possible, créez des interfaces qui encapsulent les extensions afin qu'elles puissent être désactivées ou éliminées lors de la compilation sur des systèmes qui ne les prennent pas en charge.

Les extensions n'ont souvent pas de sémantique rigoureusement définie. Même les extensions
courantes et implémentées par plusieurs compilateurs peuvent avoir des comportements légèrement
différents ou des comportements de cas limites comme conséquence directe du fait de ne *pas*
disposer d'une définition standard rigoureuse. Avec un usage suffisant de toute extension de ce
type, la portabilité attendue sera affectée.

##### Remarque

L'utilisation de C++ ISO valide ne garantit pas la portabilité (et encore moins la correction).
Évitez la dépendance à un comportement indéfini (p. ex., [ordre d'évaluation indéfini](010-expr.md#res-order))
et soyez conscient des constructions ayant une signification définie par l'implémentation (p. ex., `sizeof(int)`).

##### Remarque

Il existe des environnements où des restrictions sur l'utilisation des fonctionnalités du langage ou de la bibliothèque C++ standard sont nécessaires, par exemple pour éviter l'allocation mémoire dynamique comme l'exigent les normes logicielles de contrôle aéronautique.
Dans de tels cas, contrôlez leur (dé)susage au moyen d'une extension de ces lignes directrices de codage adaptée à l'environnement spécifique.

##### Application

Utilisez un compilateur C++ à jour (actuellement C++20 ou C++17) avec un ensemble d'options qui n'accepte pas les extensions.

### <a name="rp-what"></a>P.3 : Exprimez l'intention

##### Raison

À moins que l'intention d'un code ne soit énoncée (p. ex., dans les noms ou les commentaires), il est impossible de savoir si le code fait ce qu'il est censé faire.

##### Exemple

    gsl::index i = 0;
    while (i < v.size()) {
        // ... faire quelque chose avec v[i] ...
    }

L'intention de « simplement » parcourir les éléments de `v` n'est pas exprimée ici. Le détail d'implémentation d'un index est exposé (et pourrait donc être mal utilisé), et `i` survit à la portée de la boucle, ce qui est peut-être voulu ou non. Le lecteur ne peut pas savoir à partir de cet extrait de code seul.

Mieux :

    for (const auto& x : v) { /* faire quelque chose avec la valeur de x */ }

Ici, il n'y a aucune mention explicite du mécanisme d'itération, et la boucle opère sur des références aux éléments `const` de sorte qu'une modification accidentelle ne peut pas se produire. Si une modification est souhaitée, dites-le :

    for (auto& x : v) { /* modifier x */ }

Pour plus de détails sur les boucles for, voir [ES.71](010-expr.md#res-for-range).
Parfois, mieux encore, utilisez un algorithme nommé. Cet exemple utilise `for_each` de la TS Ranges car il exprime directement l'intention :

    for_each(v, [](int x) { /* faire quelque chose avec la valeur de x */ });
    for_each(par, v, [](int x) { /* faire quelque chose avec la valeur de x */ });

La dernière variante montre clairement que nous ne sommes pas intéressés par l'ordre dans lequel les éléments de `v` sont traités.

Un programmeur devrait être familier avec

* [La bibliothèque de support des lignes directrices](#gsl-guidelines-support-library) @TODO-LINK
* [La bibliothèque standard ISO C++](#sl-the-standard-library) @TODO-LINK
* Les bibliothèques fondamentales utilisées pour le(s) projet(s) en cours

##### Remarque

Formulation alternative : Dites ce qui doit être fait, plutôt que simplement comment cela doit être fait.

##### Remarque

Certaines constructions du langage expriment l'intention mieux que d'autres.

##### Exemple

Si deux `int` sont censés être les coordonnées d'un point 2D, dites-le :

    draw_line(int, int, int, int);  // obscur : (x1,y1,x2,y2) ? (x,y,h,w) ? ... ?
                                    // faut consulter la documentation pour savoir

    draw_line(Point, Point);        // plus clair

##### Application

Recherchez les motifs courants pour lesquels il existe de meilleures alternatives

* boucles `for` simples vs. boucles range-`for`
* interfaces `f(T*, int)` vs. interfaces `f(span<T>)`
* variables de boucle dans une portée trop grande
* `new` et `delete` nus
* fonctions avec de nombreux paramètres de types primitifs

Il y a un vaste champ pour la subtilité et la transformation semi-automatique de programmes.

### <a name="rp-typesafe"></a>P.4 : Idéalement, un programme doit être sûrement typé de manière statique

##### Raison

Idéalement, un programme serait complètement sûrement typé de manière statique (au temps de compilation).
Malheureusement, ce n'est pas possible. Zones problématiques :

* unions
* conversions de type (casts)
* décroissance de tableau (array decay)
* erreurs de bornes
* conversions réductrices (narrowing conversions)

##### Remarque

Ces zones sont sources de problèmes sérieux (p. ex., plantages et violations de sécurité).
Nous tentons de fournir des techniques alternatives.

##### Application

Nous pouvons interdire, restreindre ou détecter les catégories de problèmes individuelles séparément, selon les besoins et la faisabilité pour les programmes individuels.
Suggérez toujours une alternative.
Par exemple :

* unions -- utiliser `variant` (en C++17)
* conversions de type -- minimiser leur usage ; les gabarits peuvent aider
* décroissance de tableau -- utiliser `span` (de la GSL)
* erreurs de bornes -- utiliser `span`
* conversions réductrices -- minimiser leur usage et utiliser `narrow` ou `narrow_cast` (de la GSL) là où elles sont nécessaires

### <a name="rp-compile-time"></a>P.5 : Privilégiez la vérification au temps de compilation à celle au temps d'exécution

##### Raison

Clarté du code et performances.
Vous n'avez pas besoin d'écrire des gestionnaires d'erreurs pour des erreurs détectées au temps de compilation.

##### Exemple

    // Int est un alias utilisé pour les entiers
    int bits = 0;         // à éviter : code évitable
    for (Int i = 1; i; i <<= 1)
        ++bits;
    if (bits < 32)
        cerr << "Int too small\n";

Cet exemple échoue à réaliser ce qu'il essaie de faire (car le dépassement est indéfini) et devrait être remplacé par un simple `static_assert` :

    // Int est un alias utilisé pour les entiers
    static_assert(sizeof(Int) >= 4);    // à faire : vérification au temps de compilation

Ou mieux encore, utilisez simplement le système de types et remplacez `Int` par `int32_t`.

##### Exemple

    void read(int* p, int n);   // lit au maximum n entiers dans *p

    int a[100];
    read(a, 1000);    // à éviter, hors bornes

mieux

    void read(span<int> r); // lit dans l'intervalle d'entiers r

    int a[100];
    read(a);        // meilleur : laisser le compilateur déterminer le nombre d'éléments

**Formulation alternative** : Ne repoussez pas au temps d'exécution ce qui peut être fait correctement au temps de compilation.

##### Application

* Recherchez les arguments pointeur.
* Recherchez les vérifications au temps d'exécution pour les violations de bornes.

### <a name="rp-run-time"></a>P.6 : Ce qui ne peut pas être vérifié au temps de compilation devrait l'être au temps d'exécution

##### Raison

Laisser des erreurs difficiles à détecter dans un programme, c'est s'exposer à des plantages et de mauvais résultats.

##### Remarque

Idéalement, nous capturons toutes les erreurs (qui ne sont pas des erreurs de logique du programmeur) au temps de compilation ou au temps d'exécution. Il est impossible de capturer toutes les erreurs au temps de compilation et souvent pas envisageable de capturer toutes les erreurs restantes au temps d'exécution. Toutefois, nous devrions nous efforcer d'écrire des programmes qui peuvent en principe être vérifiés, moyennant des ressources suffisantes (programmes d'analyse, vérifications au temps d'exécution, ressources matérielles, temps).

##### Exemple, à éviter

    // compilé séparément, possiblement chargé dynamiquement
    extern void f(int* p);

    void g(int n)
    {
        // à éviter : le nombre d'éléments n'est pas transmis à f()
        f(new int[n]);
    }

Ici, une information cruciale (le nombre d'éléments) a été si profondément « obscurcie » que l'analyse statique est probablement rendue infeasible et la vérification dynamique peut être très difficile lorsque `f()` fait partie d'une ABI, de sorte que nous ne pouvons pas « instrumenter » ce pointeur. Nous pourrions intégrer des informations utiles dans le magasin mémoire libre, mais cela nécessiterait des modifications globales au système et peut-être au compilateur. Ce que nous avons ici, c'est une conception qui rend la détection d'erreurs très difficile.

##### Exemple, à éviter

Bien sûr, nous pouvons transmettre le nombre d'éléments avec le pointeur :

    // compilé séparément, possiblement chargé dynamiquement
    extern void f2(int* p, int n);

    void g2(int n)
    {
        // à éviter : le mauvais nombre d'éléments peut être transmis à f2()
        f2(new int[n], n);
    }

Transmettre le nombre d'éléments en argument est meilleur (et beaucoup plus courant) que de simplement transmettre le pointeur et de se fier à une convention (non énoncée) pour connaître ou découvrir le nombre d'éléments. Cependant (comme montré), une simple coquille peut introduire une erreur grave. Le lien entre les deux arguments de `f2()` est conventionnel, plutôt qu'explicite.

De plus, il est implicite que `f2()` est censée `delete` son argument (ou l'appelant a-t-il fait une seconde erreur ?).

##### Exemple, à éviter

Les pointeurs de gestion de ressources de la bibliothèque standard échouent à transmettre la taille lorsqu'ils pointent vers un objet :

    // compilé séparément, possiblement chargé dynamiquement
    // NB : cela suppose que le code appelant est compatible ABI, utilisant un
    // compilateur C++ compatible et la même implémentation de stdlib
    extern void f3(unique_ptr<int[]>, int n);

    void g3(int n)
    {
        f3(make_unique<int[]>(n), m);    // à éviter : transmettre la propriété et la taille séparément
    }

##### Exemple

Nous devons transmettre le pointeur et le nombre d'éléments en tant qu'objet intégral :

    extern void f4(vector<int>&);   // compilé séparément, possiblement chargé dynamiquement
    extern void f4(span<int>);      // compilé séparément, possiblement chargé dynamiquement
                                    // NB : cela suppose que le code appelant est compatible ABI, utilisant un
                                    // compilateur C++ compatible et la même implémentation de stdlib

    void g3(int n)
    {
        vector<int> v(n);
        f4(v);                     // passer une référence, conserver la propriété
        f4(span<int>{v});          // passer une vue, conserver la propriété
    }

Cette conception porte le nombre d'éléments comme partie intégrante d'un objet, de sorte que les erreurs sont peu probables et que la vérification dynamique (au temps d'exécution) est toujours feasible, même si pas toujours envisageable.

##### Exemple

Comment transférer à la fois la propriété et toutes les informations nécessaires pour valider l'utilisation ?

    vector<int> f5(int n)    // OK : déplacement (move)
    {
        vector<int> v(n);
        // ... initialiser v ...
        return v;
    }

    unique_ptr<int[]> f6(int n)    // à éviter : perd n
    {
        auto p = make_unique<int[]>(n);
        // ... initialiser *p ...
        return p;
    }

    owner<int*> f7(int n)    // à éviter : perd n et nous pourrions oublier de delete
    {
        owner<int*> p = new int[n];
        // ... initialiser *p ...
        return p;
    }

##### Exemple

* ???
* montrer comment les vérifications possibles sont évitées par des interfaces qui transmettent des classes de base polymorphes, alors qu'elles savent en fait ce dont elles ont besoin ?
  Ou des chaînes de caractères en tant qu'options « libres »

##### Application

* Signaler les interfaces de type (pointeur, compteur) (cela signalera beaucoup d'exemples qui ne peuvent pas être corrigés pour des raisons de compatibilité)
* ???

### <a name="rp-early"></a>P.7 : Détectez les erreurs au temps d'exécution le plus tôt possible

##### Raison

Évitez les plantages « mystérieux ».
Évitez les erreurs menant à de mauvais résultats (peut-être non reconnus).

##### Exemple

    void increment1(int* p, int n)    // à éviter : source d'erreurs
    {
        for (int i = 0; i < n; ++i) ++p[i];
    }

    void use1(int m)
    {
        const int n = 10;
        int a[n] = {};
        // ...
        increment1(a, m);   // peut-être une coquille, peut-être que m <= n est censé
                            // mais supposons que m == 20
        // ...
    }

Ici, nous avons commis une petite erreur dans `use1` qui conduira à des données corrompues ou à un plantage.
L'interface de type (pointeur, compteur) ne laisse pas à `increment1()` de moyen réaliste de se défendre contre les erreurs hors bornes.
Si nous pouvions vérifier les indices hors bornes, l'erreur ne serait découverte qu'à l'accès de `p[10]`.
Nous pourrions vérifier plus tôt et améliorer le code :

    void increment2(span<int> p)
    {
        for (int& x : p) ++x;
    }

    void use2(int m)
    {
        const int n = 10;
        int a[n] = {};
        // ...
        increment2({a, m});    // peut-être une coquille, peut-être que m <= n est censé
        // ...
    }

Maintenant, `m <= n` peut être vérifié au point d'appel (tôt) plutôt que plus tard.
Si nous avions simplement une coquille et que nous voulions utiliser `n` comme borne, le code pourrait être simplifié davantage (éliminant la possibilité d'une erreur) :

    void use3(int m)
    {
        const int n = 10;
        int a[n] = {};
        // ...
        increment2(a);   // le nombre d'éléments de a n'a pas besoin d'être répété
        // ...
    }

##### Exemple, à éviter

Ne vérifiez pas répéter la même valeur. Ne transmettez pas des données structurées sous forme de chaînes :

    Date read_date(istream& is);    // lire une date d'un flux d'entrée

    Date extract_date(const string& s);    // extraire une date d'une chaîne

    void user1(const string& date)    // manipuler une date
    {
        auto d = extract_date(date);
        // ...
    }

    void user2()
    {
        Date d = read_date(cin);
        // ...
        user1(d.to_string());
        // ...
    }

La date est validée deux fois (par le constructeur `Date`) et transmise comme chaîne de caractères (données non structurées).

##### Exemple

Les vérifications excédentaires peuvent être coûteuses.
Il y a des cas où vérifier tôt est inefficace, car vous n'aurez peut-être jamais besoin de la valeur, ou n'aurez peut-être besoin que d'une partie de la valeur qui est plus facilement vérifiable que le tout. De même, n'ajoutez pas de vérifications de validité qui modifient le comportement asymptotique de votre interface (p. ex., n'ajoutez pas une vérification en `O(n)` à une interface d'une complexité moyenne de `O(1)`).

    class Jet {    // La physique dit : e * e < x * x + y * y + z * z
        float x;
        float y;
        float z;
        float e;
    public:
        Jet(float x, float y, float z, float e)
            :x(x), y(y), z(z), e(e)
        {
            // Dois-je vérifier ici que les valeurs sont physiquement significatives ?
        }

        float m() const
        {
            // Dois-je gérer le cas dégénéré ici ?
            return sqrt(x * x + y * y + z * z - e * e);
        }

        ???
    };

La loi physique pour un jet (`e * e < x * x + y * y + z * z`) n'est pas un invariant en raison de la possibilité d'erreurs de mesure.

???

##### Application

* Examinez les pointeurs et les tableaux : effectuez la vérification des bornes tôt et non de manière répétée
* Examinez les conversions : éliminez ou marquez les conversions réductrices
* Recherchez les valeurs non vérifiées provenant d'une entrée
* Recherchez des données structurées (objets de classes avec des invariants) converties en chaînes
* ???

### <a name="rp-leak"></a>P.8 : Ne fuyez aucune ressource

##### Raison

Même une croissance lente des ressources épuisera, avec le temps, la disponibilité de ces ressources.
C'est particulièrement important pour les programmes de longue durée, mais c'est un élément essentiel d'un comportement de programmation responsable.

##### Exemple, à éviter

    void f(const char* name)
    {
        FILE* input = fopen(name, "r");
        // ...
        if (something) return;   // à éviter : si something == true, un descripteur de fichier fuit
        // ...
        fclose(input);
    }

Privilégiez le [RAII](009-resource.md#rr-raii) :

    void f(const char* name)
    {
        ifstream input {name};
        // ...
        if (something) return;   // OK : pas de fuite
        // ...
    }

**Voir aussi** : [La section sur la gestion des ressources](009-resource.md)

##### Remarque

Une fuite est couramment « tout ce qui n'est pas nettoyé ».
La classification plus importante est « tout ce qui ne peut plus être nettoyé ».
Par exemple, allouer un objet sur le tas puis perdre le dernier pointeur qui pointe vers cette allocation.
Cette règle ne devrait pas être interprétée comme exigeant que les allocations dans des objets de longue durée soient rendues lors de l'arrêt du programme.
Par exemple, se fier à un nettoyage garanti par le système, tel que la fermeture des fichiers et la libération de la mémoire lors de l'arrêt du processus, peut simplifier le code.
Cependant, se fier à des abstractions qui nettoient implicitement peut être tout aussi simple, et souvent plus sûr.

##### Remarque

L'application du [profil de sûreté des temps de vie](022-profile.md#ss-lifetime) élimine les fuites.
Combiné à la sûreté des ressources fournie par le [RAII](009-resource.md#rr-raii), il élimine le besoin de « collecte des ordures » (en ne générant aucun déchet).
Combinez cela avec l'application des [profils de types et de bornes](003-introduction.md#ss-force) et vous obtenez une sûreté complète des types et des ressources, garantie par les outils.

##### Application

* Examinez les pointeurs : classez-les en non-propriétaires (la valeur par défaut) et propriétaires.
  Lorsque c'est faisable, remplacez les propriétaires par des gestionnaires de ressources de la bibliothèque standard (comme dans l'exemple ci-dessus).
  Sinon, marquez un propriétaire comme tel en utilisant `owner` de [la GSL](#gsl-guidelines-support-library) @TODO-LINK.
* Recherchez les `new` et `delete` nus
* Recherchez les fonctions d'allocation de ressources connues renvoyant des pointeurs bruts (tels que `fopen`, `malloc` et `strdup`)

### <a name="rp-waste"></a>P.9 : Ne gaspillez ni temps ni espace

##### Raison

C'est du C++.

##### Remarque

Le temps et l'espace que vous utilisez bien pour atteindre un objectif (p. ex., vitesse de développement, sûreté des ressources ou simplification des tests) ne sont pas gaspillés.
« Un autre avantage de viser l'efficacité est que le processus vous force à comprendre le problème plus en profondeur. » - Alex Stepanov

##### Exemple, à éviter

    struct X {
        char ch;
        int i;
        string s;
        char ch2;

        X& operator=(const X& a);
        X(const X&);
    };

    X waste(const char* p)
    {
        if (!p) throw Nullptr_error{};
        int n = strlen(p);
        auto buf = new char[n];
        if (!buf) throw Allocation_error{};
        for (int i = 0; i < n; ++i) buf[i] = p[i];
        // ... manipuler le tampon ...
        X x;
        x.ch = 'a';
        x.s = string(n);    // donner à x.s de la place pour *p
        for (gsl::index i = 0; i < x.s.size(); ++i) x.s[i] = buf[i];  // copier buf dans x.s
        delete[] buf;
        return x;
    }

    void driver()
    {
        X x = waste("Typical argument");
        // ...
    }

Oui, c'est une caricature, mais nous avons vu chaque erreur individuelle dans du code en production, et pire encore.
Remarquez que la disposition de `X` garantit qu'au moins 6 octets (et probablement plus) sont gaspillés.
La définition superflue des opérations de copie désactive la sémantique de déplacement, de sorte que l'opération de retour est lente
(veuillez noter que l'Optimisation de la Valeur Renvoyée, RVO, n'est pas garantie ici).
L'utilisation de `new` et `delete` pour `buf` est redondante ; si nous avions vraiment besoin d'une chaîne locale, nous devrions utiliser un `string` local.
Il y a plusieurs autres bugs de performances et une complication gratuite.

##### Exemple, à éviter

    void lower(zstring s)
    {
        for (int i = 0; i < strlen(s); ++i) s[i] = tolower(s[i]);
    }

C'est en fait un exemple de code en production.
Nous pouvons voir que dans notre condition nous avons `i < strlen(s)`. Cette expression sera évaluée à chaque itération de la boucle, ce qui signifie que `strlen` doit parcourir la chaîne à chaque boucle pour découvrir sa longueur. Bien que le contenu de la chaîne change, on suppose que `tolower` n'affectera pas la longueur de la chaîne, il est donc mieux de mettre la longueur en cache hors de la boucle et d'éviter ce coût à chaque itération.

##### Remarque

Un exemple individuel de gaspillage est rarement significatif, et lorsqu'il l'est, il est généralement facilement éliminé par un expert.
Cependant, un gaspillage répandu à travers une base de code peut facilement être significatif et les experts ne sont pas toujours aussi disponibles que nous le souhaiterions.
L'objectif de cette règle (et des règles plus spécifiques qui la soutiennent) est d'éliminer la majeure partie du gaspillage lié à l'utilisation du C++ avant qu'il ne se produise.
Après cela, nous pouvons examiner le gaspillage lié aux algorithmes et aux exigences, mais cela dépasse le cadre de ces lignes directrices.

##### Application

Beaucoup de règles plus spécifiques visent les objectifs globaux de simplicité et d'élimination du gaspillage gratuit.

* Signaler une valeur de retour inutilisée d'une fonction postfixe `operator++` ou `operator--` utilisateur non définie par défaut. Privilégiez l'utilisation de la forme préfixe. (Note : « Utilisateur non définie par défaut » est destiné à réduire le bruit. Réexaminez cette application si elle est encore trop bruyante en pratique.)


### <a name="rp-mutable"></a>P.10 : Privilégiez les données immuables aux données mutables

##### Raison

Il est plus facile de raisonner sur des constantes que sur des variables.
Quelque chose d'immuable ne peut pas changer de manière inattendue.
Parfois l'immutabilité permet de meilleures optimisations.
Vous ne pouvez pas avoir de concurrence de données sur une constante.

Voir [Con : Constantes et immutabilité](014-const.md)

### <a name="rp-library"></a>P.11 : Encapsulez les constructions complexes plutôt que de les disperser dans le code

##### Raison

Un code complexe est plus susceptible de masquer des bugs et plus difficile à écrire.
Une bonne interface est plus facile et plus sûre à utiliser.
Un code bas niveau et complexe engendre davantage de ce type de code.

##### Exemple

    int sz = 100;
    int* p = (int*) malloc(sizeof(int) * sz);
    int count = 0;
    // ...
    for (;;) {
        // ... lire un int dans x, quitter la boucle si fin de fichier ...
        // ... vérifier que x est valide ...
        if (count == sz)
            p = (int*) realloc(p, sizeof(int) * sz * 2);
        p[count++] = x;
        // ...
    }

C'est du bas niveau, verbeux et source d'erreurs.
Par exemple, nous avons « oublié » de tester l'épuisement mémoire et d'assigner la nouvelle valeur à `sz`.
Au lieu de cela, nous pourrions utiliser `vector` :

    vector<int> v;
    v.reserve(100);
    // ...
    for (int x; cin >> x; ) {
        // ... vérifier que x est valide ...
        v.push_back(x);
    }

##### Remarque

La bibliothèque standard et la GSL sont des exemples de cette philosophie.
Par exemple, au lieu de gérer les tableaux, les unions, les conversions de type, les questions complexes de temps de vie, `gsl::owner`, etc.,
nécessaires pour implémenter des abstractions clés telles que `vector`, `span`, `lock_guard` et `future`, nous utilisons les bibliothèques
conçues et implémentées par des personnes ayant plus de temps et d'expertise que nous n'en avons habituellement.
De même, nous pouvons et devrions concevoir et implémenter des bibliothèques plus spécialisées, plutôt que de laisser les utilisateurs (souvent nous-mêmes)
avec le défi de réussir à réécrire correctement du code bas niveau à répétition.
C'est une variante du [principe du sous-ensemble du sur-ensemble](003-introduction.md#r0) qui sous-tend ces lignes directrices.

##### Application

* Recherchez le « code complexe » tel que la manipulation complexe de pointeurs et les conversions de type en dehors de l'implémentation des abstractions.


### <a name="rp-tools"></a>P.12 : Utilisez les outils d'assistance le cas échéant

##### Raison

Il y a beaucoup de choses qui sont mieux faites « par machine ».
Les ordinateurs ne se fatiguent pas et ne s'ennuient pas des tâches répétitives.
Nous avons généralement de meilleures choses à faire que de répéter des tâches courantes.

##### Exemple

Lancez un analyseur statique pour vérifier que votre code suit les lignes directrices que vous souhaitez qu'il suive.

##### Remarque

Voir

* [Outils d'analyse statique](https://en.wikipedia.org/wiki/List_of_tools_for_static_code_analysis)
* [Outils de concurrence](012-concurrency.md#rconc-tools)
* [Outils de test](https://github.com/isocpp/CppCoreGuidelines/tree/master)

Il existe de nombreux autres types d'outils, tels que les dépôts de code source, les outils de construction, etc.,
mais ceux-ci dépassent le cadre de ces lignes directrices.

##### Remarque

Faites attention à ne pas devenir dépendant de chaînes d'outils trop élaborées ou trop spécialisées.
Celles-ci peuvent rendre votre code autrement portable non portable.


### <a name="rp-lib"></a>P.13 : Utilisez les bibliothèques d'assistance le cas échéant

##### Raison

L'utilisation d'une bibliothèque bien conçue, bien documentée et bien soutenue fait gagner du temps et des efforts ;
sa qualité et sa documentation sont susceptibles d'être supérieures à ce que vous pourriez faire
si la majorité de votre temps devait être consacrée à une implémentation.
Le coût (temps, efforts, argent, etc.) d'une bibliothèque peut être partagé entre de nombreux utilisateurs.
Une bibliothèque largement utilisée est plus susceptible d'être maintenue à jour et portée sur de nouveaux systèmes qu'une application individuelle.
La connaissance d'une bibliothèque largement utilisée peut faire gagner du temps sur d'autres/projets futurs.
Ainsi, si une bibliothèque adaptée existe pour votre domaine d'application, utilisez-la.

##### Exemple

    std::sort(begin(v), end(v), std::greater<>());

À moins que vous ne soyez un expert en algorithmes de tri et que vous n'ayez beaucoup de temps,
cette solution est plus susceptible d'être correcte et d'exécuter plus rapidement que n'importe quoi que vous écririez pour une application spécifique.
Vous avez besoin d'une raison de ne pas utiliser la bibliothèque standard (ou les bibliothèques fondamentales que votre application utilise) plutôt que d'une raison de l'utiliser.

##### Remarque

Par défaut, utilisez

* La [bibliothèque standard ISO C++](#sl-the-standard-library) @TODO-LINK
* La [bibliothèque de support des lignes directrices](#gsl-guidelines-support-library) @TODO-LINK

##### Remarque

Si aucune bibliothèque bien conçue, bien documentée et bien soutenue n'existe pour un domaine important,
peut-être devriez-vous la concevoir et l'implémenter, puis l'utiliser.