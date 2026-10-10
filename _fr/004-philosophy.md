<a name="s-philosophy"></a>P: Philosophie

Les règles dans cette section sont très générales.

Résumé des règles de philosophie :
* [P.1 : Exprimer les idées directement dans le code](#rp-direct)
* [P.2 : Écrire dans le C++ ISO Standard](#rp-cplusplus)
* [P.3 : Exprimer l'intention](#rp-what)
* [P.4 : Idéalement, un programme devrait être statiquement sûr en termes de type](#rp-typesafe)
* [P.5 : Préférer la vérification à la compilation à la vérification à l'exécution](#rp-compile-time)
* [P.6 : Ce qui ne peut pas être vérifié à la compilation doit pouvoir l’être à l'exécution](#rp-run-time)
* [P.7 : Attraper les erreurs à l'exécution tôt](#rp-early)
* [P.8 : Ne pas laisser fuites de ressources](#rp-leak)
* [P.9 : Ne pas gaspiller ni du temps ni de l'espace](#rp-waste)
* [P.10 : Préférer les données immuables aux données mutables](#rp-mutable)
* [P.11 : Encapsuler les constructions désordonnées plutôt que de les répandre dans le code](#rp-library)
* [P.12 : Utiliser les outils de support de manière appropriée](#rp-tools)
* [P.13 : Utiliser les bibliothèques de support de manière appropriée](#rp-lib)

Les règles philosophiques ne sont généralement pas vérifiables mécaniquement. Cependant, des règles individuelles reflétant ces thèmes philosophiques le sont. Sans une base philosophique, les règles plus concrètes / spécifiques / vérifiables manquent de justification.

### <a name="rp-direct"></a>P.1 : Exprimer les idées directement dans le code

##### Raison

Les compilateurs ne lisent pas les commentaires (ou documents de conception) et la plupart des programmeurs ne le font pas de façon cohérente. Ce qui est exprimé dans le code a une sémantique définie et peut (en principe) être vérifié par les compilateurs et d’autres outils.

##### Exemple

    class Date {
    public:
        Month month() const;  // faire
        int month();          // ne pas faire
        // ...
    };

Le premier déclarant de `month` est explicite concernant le retour d'un `Month` et le fait de ne pas modifier l'état de l’objet `Date`. La deuxième version laisse le lecteur deviner et ouvre plus de possibilités d'erreurs non découvertes.

##### Exemple, mauvais

Cette boucle est une forme restreinte de `std::find` :

    void f(vector<string>& v)
    {
        string val;
        cin >> val;
        // ...
        int index = -1;                    // mauvais, plus doit utiliser gsl::index
        for (int i = 0; i < v.size(); ++i) {
            if (v[i] == val) {
                index = i;
                break;
            }
        }
        // ...
    }

##### Exemple, bon

Une expression beaucoup plus claire de l’intention serait :

    void f(vector<string>& v)
    {
        string val;
        cin >> val;
        // ...
        auto p = find(begin(v), end(v), val);  // mieux
        // ...
    }

Une bibliothèque bien conçue exprime l’intention (ce qui doit être fait, plutôt que simplement comment quelque chose est fait) beaucoup mieux qu’une utilisation directe des fonctionnalités du langage.

Un programmeur C++ devrait connaître les bases de la bibliothèque standard et l’utiliser lorsqu’elle est appropriée. Tout programmeur devrait connaître les bases des bibliothèques fondamentales du projet sur lequel il travaille et l’utiliser de manière appropriée. Tout programmeur utilisant ces directives devrait connaître la [bibliothèque de support des Directives](#gsl-guidelines-support-library) et l’utiliser de manière appropriée.

##### Exemple

    change_speed(double s);   // mauvais : que signifie s ?
    // ...
    change_speed(2.3);

Une meilleure approche serait d’être explicite sur la signification du double (nouvelle vitesse ou delta de la vitesse actuelle ?) et l’unité utilisée :

    change_speed(Speed s);    // mieux : la signification de s est spécifiée
    // ...
    change_speed(2.3);        // erreur : aucune unité
    change_speed(23_m / 10s);  // mètres par seconde

Nous aurions pu accepter un `double` simple (sans unité) comme delta, mais cela aurait été propice aux erreurs. Si nous voulions à la fois une vitesse absolue et des deltas, nous aurions défini un type `Delta`.

##### Mise en œuvre

Très difficile en général.

* Utiliser `const` de façon cohérente (vérifier si les fonctions membres modifient leur objet ; vérifier si les fonctions modifient les arguments passés par pointeur ou référence)
* Marquer les utilisations de conversions (les conversions annulent le système de types)
* Détecter le code qui imite la bibliothèque standard (du dur)

### <a name="rp-cplusplus"></a>P.2 : Écrire en ISO Standard C++

##### Raison

Il s’agit d’un ensemble de directives pour écrire du C++ ISO Standard.

##### Remarque

Il existe des environnements où des extensions sont nécessaires, par exemple pour accéder aux ressources système. Dans de tels cas, localisez l’utilisation des extensions nécessaires et contrôlez leur utilisation avec des directives de codage hors cœur.  Si possible, construisez des interfaces qui encapsulent les extensions afin qu’elles puissent être désactivées ou compilées hors des systèmes qui ne prennent pas en charge ces extensions.

Les extensions n’ont souvent pas de sémantique rigoureusement définie. Même les extensions qui sont courantes et implémentées par plusieurs compilateurs peuvent présenter des comportements légèrement différents et des comportements de bord en raison de *l'absence* d'une définition rigoureuse de la norme. Avec une utilisation suffisante de toute telle extension, la portabilité attendue sera impactée.

##### Remarque

L’utilisation d’un ISO C++ valide ne garantit pas la portabilité (voire la correction). Évitez la dépendance à un comportement indéfini (par ex. [ordre d’évaluation indéfini](#res-order)) et soyez conscient des constructions avec un sens défini par l’implémentation (par ex. `sizeof(int)`).

##### Remarque

Il existe des environnements où des restrictions sur l’utilisation des caractéristiques du langage C++ ou de la bibliothèque standards sont nécessaires, par exemple éviter l’allocation dynamique de mémoire requise par les normes des logiciels de contrôle aérien. Dans de tels cas, contrôlez leur utilisation avec une extension de ces Directives de Codage personnalisée pour l’environnement spécifique.

##### Mise en œuvre

Utilisez un compilateur C++ à jour (actuellement C++20 ou C++17) avec un ensemble d’options qui n’acceptent pas d’extensions.

### <a name="rp-what"></a>P.3 : Exprimer l'intention

##### Raison

Sans que l’intention d’un morceau de code soit indiquée (par ex. dans le nom ou les commentaires), il est impossible de savoir si le code fait ce qu’il est censé faire.

##### Exemple

    gsl::index i = 0;
    while (i < v.size()) {
        // ... faire quelque chose avec v[i] ...
    }

L’intention de simplement parcourir les éléments de `v` n’est pas exprimée ici. Le détail d’une indexation est exposé (afin qu’il puisse être mal utilisé), et `i` dépasse la portée de la boucle, ce qui peut ou non être voulu. Le lecteur ne peut pas savoir à partir de cette partie du code.

Meilleur :

    for (const auto& x : v) { /* faire quelque chose avec la valeur de x */ }

Désormais, il n’y a pas de mention explicite du mécanisme d’itération, et la boucle opère sur une référence à des éléments `const` afin qu’une modification accidentelle ne puisse pas se produire. Si une modification est souhaitée, indiquez‑la :

    for (auto& x : v) { /* modifier x */ }

Pour plus de détails sur les instructions `for`, voir [ES.71](#res-for-range).

Parfois encore mieux, utilisez un algorithme nommé. Cet exemple utilise le `for_each` du TS Ranges parce qu’il exprime directement l’intention :

    for_each(v, [](int x) { /* faire quelque chose avec la valeur de x */ });
    for_each(par, v, [](int x) { /* faire quelque chose avec la valeur de x */ });

La dernière variante indique clairement que nous ne nous intéressons pas à l’ordre dans lequel les éléments de `v` sont traités.

Un programmeur doit être familier avec

* La bibliothèque de support des Directives
* La Bibliothèque C++ ISO Standard (voir [018-stdlib.md](018-stdlib.md))
* Toutes les bibliothèques de base utilisées pour le ou les projets actuels

##### Remarque

Formulation alternative : dire ce qui doit être fait, plutôt que simplement comment il doit être fait.

##### Remarque

Certains constructs du langage expriment l’intention mieux que d’autres.

##### Exemple

Si deux `int` sont censés être les coordonnées d’un point 2D, indiquez‑les :

    draw_line(int, int, int, int);  // obscur : (x1,y1,x2,y2)? (x,y,h,w)? ...
                                    // il faut consulter la documentation pour savoir

    draw_line(Point, Point);        // plus clair

### <a name="rp-typesafe"></a>P.4 : Idéalement, un programme devrait être statiquement sûr en termes de type

##### Raison

Idéalement, un programme serait complètement statiquement (en temps de compilation) sûr en type. Malheureusement, ce n’est pas possible. Les zones problématiques :

* unions
* conversions explicites (casts)
* décay d’array
* erreurs de plage
* conversions de type diminution

##### Remarque

Ces domaines sont sources de problèmes graves (p.ex. plantages et violations de sécurité). Nous essayons de fournir des techniques alternatives.

##### Mise en œuvre

Nous pouvons bannir, restreindre ou détecter les catégories de problèmes individuelles séparément, comme requis et faisable pour les programmes individuels. Toujours proposer une alternative. Par exemple :

* unions -- utiliser `variant` (C++17)
* conversions explicites (casts) -- minimiser leur usage ; les modèles (templates) peuvent aider
* décay d’array -- utiliser `span` (du GSL)
* erreurs de plage -- utiliser `span`
* conversions de type diminution -- minimiser leur usage et utiliser `narrow` ou `narrow_cast` (du GSL) lorsqu’elles sont nécessaires

### <a name="rp-compile-time"></a>P.5 : Préférer la vérification à la compilation à la vérification à l'exécution

##### Raison

Clarté de code et performance. On n’a pas besoin d’écrire des gestionnaires d’erreurs pour les erreurs détectées à la compilation.

##### Exemple

    // Int est un alias utilisé pour les entiers
    int bits = 0;         // ne pas : code évitable
    for (Int i = 1; i; i <<= 1)
        ++bits;
    if (bits < 32)
        cerr << "Int trop petit\n";

Cet exemple ne réussit pas à accomplir ce qu’il vise (car le dépassement est indéfini) et devrait être remplacé par une simple assertion à la compilation :

    // Int est un alias utilisé pour les entiers
    static_assert(sizeof(Int) >= 4);    // faire : vérification à la compilation

Ou mieux encore simplement utiliser le système de type et remplacer `Int` par `int32_t`.

##### Exemple

    void read(int* p, int n);   // lire jusqu'à n entiers dans *p

    int a[100];
    read(a, 1000);    // mauvais, dépassement de la fin

meilleur

    void read(span<int> r); // lire dans la gamme d'entiers r

    int a[100];
    read(a);        // mieux : laisser le compilateur déterminer le nombre d'éléments

**Formulation alternative** : ne pas repousser à l'exécution ce qui peut être bien fait au moment de la compilation.

##### Mise en œuvre

* Rechercher les arguments pointeur.
* Rechercher les vérifications d'exécution pour les violations de plage.

### <a name="rp-run-time"></a>P.6 : Ce qui ne peut pas être vérifié à la compilation doit pouvoir l’être à l'exécution

##### Raison

Laisser des erreurs difficiles à détecter dans un programme revient à prévoir des plantages et de mauvais résultats.

##### Remarque

Idéalement, nous attrapons toutes les erreurs (qui ne sont pas des erreurs de logique du programme) à la compilation ou à l'exécution. Il est impossible de capter toutes les erreurs à la compilation et souvent pas rentable d'en capturer toutes les restantes à l'exécution. Cependant, nous devrions nous efforcer d'écrire des programmes qui, en principe, peuvent être vérifiés, donné des ressources suffisantes (programmes d'analyse, vérifications à l'exécution, ressources machine, temps).

##### Exemple, mauvais

    // compilé séparément, peut-être chargé dynamiquement
    extern void f(int* p);

    void g(int n)
    {
        // mauvais : le nombre d'éléments n'est pas passé à f()
        f(new int[n]);
    }

Ici, un morceau d'information crucial (le nombre d'éléments) a été tellement « obscur‑tifié » que l'analyse statique est probablement rendue infructueuse et la vérification dynamique peut être très difficile quand `f()` fait partie d'un ABI afin que nous ne puissions pas « instrumenter » ce pointeur. Nous pourrions embarquer des informations utiles dans le mendiant, mais cela nécessite des changements globaux à un système et peut-être aussi au compilateur. Ce que nous avons ici est un design qui rend difficile la détection d'erreurs.

##### Exemple, mauvais

Nous pouvons bien sûr passer le nombre d'éléments avec le pointeur :

    // compilé séparément, peut-être chargé dynamiquement
    extern void f2(int* p, int n);

    void g2(int n)
    {
        // mauvais : le mauvais nombre d'éléments peut être passé à f2()
        f2(new int[n], n);
    }

Passer le nombre d'éléments comme argument est mieux (et bien plus commun) que simplement passer le pointeur et compter sur une convention (non déclarée) de connaître ou de découvrir le nombre d'éléments. Cependant (comme démontré), une simple faute de frappe peut introduire une erreur grave. La connexion entre les deux arguments de `f2()` est conventionnelle, plutôt que explicite.

De plus, il est implicite que `f2()` est censé appeler `delete` sur son argument (ou l'appelant a fini de faire une deuxième faute ?).

##### Exemple, mauvais

Les pointeurs de gestion de ressources de la bibliothèque standard ne passent pas la taille lorsqu'ils pointent vers un objet :

    // compilé séparément, peut-être chargé dynamiquement
    // NB : cela suppose que le code appelant est ABI‑compatible, utilise un
    // compilateur C++ compatible et la même implémentation de libstdc++
    extern void f3(unique_ptr<int[]>, int n);

    void g3(int n)
    {
        f3(make_unique<int[]>(n), m);    // mauvais : passation d'unicité et de la taille séparément
    }

##### Exemple

Nous devons passer le pointeur et le nombre d'éléments comme un objet intégral :

    extern void f4(vector<int>&);   // compilé séparément, peut-être chargé dynamiquement
    extern void f4(span<int>);      // compilé séparément, peut-être chargé dynamiquement
                                    // NB : cela suppose que le code appelant est ABI‑compatible, utilise un
                                    // compilateur C++ compatible et la même implémentation de libstdc++

    void g3(int n)
    {
        vector<int> v(n);
        f4(v);                     // passer une référence, conserver la propriété
        f4(span<int>{v});          // passer une vue, conserver la propriété
    }

Cette conception comporte le nombre d'éléments comme partie intégrante d'un objet, afin que les erreurs soient peu probables et la vérification à l'exécution soit toujours faisable, si ce n'est toujours pas rentable.

##### Exemple

Comment transférer à la fois la propriété et toutes les informations nécessaires à la validation d'utilisation ?

    vector<int> f5(int n)    // OK : mouvement
    {
        vector<int> v(n);
        // ... initialiser v ...
        return v;
    }

    unique_ptr<int[]> f6(int n)    // mauvais : perd n
    {
        auto p = make_unique<int[]>(n);
        // ... initialiser *p ...
        return p;
    }

    owner<int*> f7(int n)    // mauvais : perd n et nous pourrions oublier de supprimer
    {
        owner<int*> p = new int[n];
        // ... initialiser *p ...
        return p;
    }

##### Exemple

* ???  
* montrer comment les vérifications possibles sont évitées par les interfaces qui passent des classes de base polymorphes, lorsqu'elles savent réellement ce dont elles ont besoin ?  
  Ou chaînes de caractères comme options « free‑style »

##### Mise en œuvre

* Marquer les interfaces (pointeur, taille) (cela va signaler un éventail d'exemples qui ne peuvent pas être corrigés pour des raisons de compatibilité)
* ???

### <a name="rp-early"></a>P.7 : Attraper les erreurs à l'exécution tôt

##### Raison

Éviter les plantages “mystérieux”.
Éviter les erreurs menant à des résultats (éventuellement non reconnus) erronés.

##### Exemple, mauvais

    void increment1(int* p, int n)    // mauvais : subject to errors
    {
        for (int i = 0; i < n; ++i) ++p[i];
    }

    void use1(int m)
    {
        const int n = 10;
        int a[n] = {};
        // ...
        increment1(a, m);   // peut être une faute de frappe, peut être que m <= n est supposé
                            // mais supposons que m == 20
        // ...
    }

Ici, nous avons commis une petite erreur dans `use1` qui entraînera la corruption des données ou un plantage. L’interface (pointeur, compte) laisse `increment1()` sans véritable moyen de se défendre contre les erreurs hors plage. Si nous pouvions vérifier les index hors plage, l’erreur ne serait découverte que lorsque `p[10]` est accédé. Nous pourrions vérifier plus tôt et améliorer le code :

    void increment2(span<int> p)
    {
        for (int& x : p) ++x;
    }

    void use2(int m)
    {
        const int n = 10;
        int a[n] = {};
        // ...
        increment2({a, m});    // peut être une faute de frappe, a supposé que m <= n
        // ...
    }

Maintenant, `m <= n` peut être vérifié au point d’appel (tôt) plutôt qu’après. Si la seule faute de frappe était que nous voulions utiliser `n` comme borne, le code pourrait être simplifié davantage (éliminant la possibilité d’erreur) :

    void use3(int m)
    {
        const int n = 10;
        int a[n] = {};
        // ...
        increment2(a);   // le nombre d'éléments de a n'a pas besoin d'être répété
        // ...
    }

##### Exemple, mauvais

Ne pas vérifier à plusieurs reprises la même valeur. Ne pas passer des données structurées sous forme de chaînes :

    Date read_date(istream& is);    // lire une date depuis ios
    Date extract_date(const string& s);    // extraire la date d'une chaîne

    void user1(const string& date)    // manipuler date
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

La date est validée deux fois (par le constructeur `Date`) et passée sous forme de chaîne de caractères (données non structurées).

##### Exemple

Une vérification excessive peut être coûteuse. Il existe des cas où la vérification rapide est inefficace car vous ne pourriez jamais avoir besoin de la valeur, ou ne pourriez avoir besoin qu'une partie de la valeur qui est plus facilement vérifiable que l'ensemble. De même, ne pas ajouter de vérifications de validité qui changent le comportement asymptotic de votre interface (par ex. ne pas ajouter une vérification O(n) à une interface en moyenne O(1)).

    class Jet {    // Physiquement : e * e < x * x + y * y + z * z
        float x;
        float y;
        float z;
        float e;
    public:
        Jet(float x, float y, float z, float e)
            :x(x), y(y), z(z), e(e)
        {
            // Devrais-je vérifier ici que les valeurs sont physiquement significatives ?
        }

        float m() const
        {
            // Devrais-je gérer le cas dégénéré ici ?
            return sqrt(x * x + y * y + z * z - e * e);
        }

        ???
    };

La loi physique pour un jet (`e * e < x * x + y * y + z * z`) n’est pas une invariant car il y a possibilité d’erreur de mesure.

???  

##### Mise en œuvre

* Examiner les pointeurs et les tableaux : faire des vérifications de plage tôt et pas à plusieurs reprises
* Examiner les conversions : éliminer ou marquer les conversions de type diminution
* Chercher les valeurs non vérifiées provenant de l’entrée
* Chercher les données structurées (objets de classes avec invariants) convertis en chaînes
* ???

### <a name="rp-leak"></a>P.8 : Ne pas laisser fuites de ressources

##### Raison

Même une croissance lente des ressources entraînera, avec le temps, l'épuisement de celles – un problème particulièrement critique pour les programmes de longue durée, mais un aspect essentiel de la programmation responsable.

##### Exemple, mauvais

    void f(const char* name)
    {
        FILE* input = fopen(name, "r");
        // ...
        if (something) return;   // mauvais : si something == true, une poignée de fichier est perdue
        // ...
        fclose(input);
    }

Privilégier RAII :

    void f(const char* name)
    {
        ifstream input {name};
        // ...
        if (something) return;   // OK : pas de fuite
        // ...
    }

**Voir aussi** : [La section gestion des ressources](#s-resource)

##### Remarque

Une fuite est couramment "tout ce qui n'est pas nettoyé." La classification la plus importante est "tout ce qui ne peut plus être nettoyé." Par exemple, allouer un objet alloué sur le tas et perdre le dernier pointeur qui pointe vers cette allocation. Cette règle ne doit pas être interprétée comme exigeant que les allocations dans les objets à long terme soient libérées lors de l'arrêt du programme. Par exemple, le fait de compter sur la libération garantie par le système, comme la fermeture de fichier et la désallocation de mémoire lors de l'arrêt du processus, peut simplifier le code. Cependant, les abstractions qui nettoient implicitement peuvent être tout aussi simples, et souvent plus sûres.

##### Remarque

Enforcer le profil de sécurité de la durée de vie élimine les fuites. Combinaison avec la sécurité de la ressource proposée par RAII élimine le besoin de "garbage collection" (générant aucun ramasse‑miettes). Combinez avec l’application du profil "type et bornes" et vous obtenez une sécurité de type et de ressource complète, garantie par des outils.

##### Mise en œuvre

* Examiner les pointeurs : les classer en non‑propriétaires (défaut) et propriétaires. Où il est faisable, remplacer les propriétaires par des gestionnaires de ressources de la bibliothèque standard (comme dans l'exemple ci‑dessus). Alternativement, marquer un propriétaire en utilisant `owner` de la GSL.
* Chercher des `new` et `delete` nus
* Rechercher les fonctions d'allocation de ressources connues retournant des pointeurs bruts (fopen, malloc, strdup, etc.)

### <a name="rp-waste"></a>P.9 : Ne pas gaspiller ni du temps ni de l'espace

##### Raison

C’est du C++.

##### Remarque

Le temps et l’espace que vous investissez judicieusement pour atteindre un objectif (ex. vitesse de développement, sécurité des ressources ou simplification des tests) ne sont pas gaspillés. "Un autre avantage de la recherche de l'efficacité est que le processus vous oblige à comprendre le problème plus en profondeur." – Alex Stepanov

##### Exemple, mauvais

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
        x.s = string(n);    // donner à x.s de l'espace pour *p
        for (gsl::index i = 0; i < x.s.size(); ++i) x.s[i] = buf[i];  // copier buf dans x.s
        delete[] buf;
        return x;
    }

    void driver()
    {
        X x = waste("Argument typique");
        // ...
    }

Oui, c’est une caricature, mais nous avons vu chaque erreur individuelle en production, et pire encore. Notez que la disposition de `X` garantit qu’au moins 6 octets (et probablement plus) sont gaspillés. La définition fictive des opérations de copie désactive la sémantique de déplacement, rendant le retour lent (précisez que RVO n’est pas garanti ici). L’utilisation de `new` et `delete` pour `buf` est redondante; si nous avons réellement besoin d’une chaîne locale, nous devrions utiliser une `string` locale. Il y a plusieurs bugs de performance et complications gratuit.

##### Exemple, mauvais

    void lower(zstring s)
    {
        for (int i = 0; i < strlen(s); ++i) s[i] = tolower(s[i]);
    }

Ceci est en fait un exemple issu de la production. On remarque que dans notre condition, nous avons `i < strlen(s)`. Cette expression est évaluée à chaque itération, ce qui signifie que `strlen` doit parcourir la chaîne à chaque boucle pour découvrir sa longueur. Alors que le contenu de la chaîne change, on suppose que `tolower` ne modifie pas la longueur de la chaîne, il vaut mieux mettre la longueur en cache en dehors de la boucle pour ne pas charger ce coût à chaque itération.

##### Remarque

Un exemple individuel de gaspillage est rarement significatif, et, lorsqu’il le devient, il est généralement facilement éliminable par un expert. Cependant, le gaspillage répandu dans une base de code peut être significatif et les experts ne sont pas toujours disponibles comme nous le souhaitons. L’objectif de cette règle (et des règles plus spécifiques qui la soutiennent) est d’éliminer la plupart des gaspillages liés à l’utilisation de C++ avant qu'ils ne se produisent. Après cela, nous pourrons examiner les gaspillages liés aux algorithmes et aux exigences, mais cela dépasse le cadre de ces directives.

##### Mise en œuvre

De nombreuses règles plus spécifiques visent aux objectifs globaux de simplicité et d'élimination du gaspillage gratuit.

* Signaler une valeur de retour non utilisée d’une fonction d’incrémentation post‑définie par l’utilisateur non par défaut. Privilégier l’utilisation de la forme préfixe au lieu de la suffixe. (Note : "définie par l’utilisateur et non par défaut" est destiné à réduire le bruit. Réexaminez cette mise en œuvre s’il est toujours trop bruyante en pratique.)

### <a name="rp-mutable"></a>P.10 : Préférer les données immuables aux données mutables

##### Raison

Il est plus facile de raisonner sur les constantes que sur les variables. Quelque chose d'immuable ne peut pas changer de façon inattendue. Parfois, l'immuabilité permet de meilleures optimisations. Vous ne pouvez pas avoir de concurrence de données sur une constante.

Voir [C : Constantes et immutabilité](#s-const)

### <a name="rp-library"></a>P.11 : Encapsuler les constructions désordonnées plutôt que de les répandre dans le code

##### Raison

Le code désordonné est plus susceptible de cacher des bugs et est plus difficile à écrire. Une bonne interface est plus simple et plus sûre à utiliser. Un code désordonné de bas niveau engendre plus de ce genre de code.

##### Exemple

    int sz = 100;
    int* p = (int*) malloc(sizeof(int) * sz);
    int count = 0;
    // ...
    for (;;) {
        // ... lire un int dans x, sortir de la boucle si fin de fichier est atteinte ...
        // ... vérifier que x est valide ...
        if (count == sz)
            p = (int*) realloc(p, sizeof(int) * sz * 2);
        p[count++] = x;
        // ...
    }

Ceci est de bas niveau, verbeux et sujet à erreurs. Par exemple, nous « oublions » de tester l'épuisement de mémoire et d'assigner la nouvelle valeur à `sz`. Au lieu de cela, nous pourrions utiliser `vector` :

    vector<int> v;
    v.reserve(100);
    // ...
    for (int x; cin >> x; ) {
        // ... vérifier que x est valide ...
        v.push_back(x);
    }

### <a name="rp-tools"></a>P.12 : Utiliser les outils de support de manière appropriée

##### Raison

Il y a de nombreuses choses qui sont mieux faites « par machine ». Les ordinateurs ne se fatiguent pas ou ne s’ennuient pas à faire des tâches répétitives. Nous avons généralement mieux à faire que de répéter les tâches de routine.

##### Exemple

Exécuter un analyseur statique afin de vérifier que votre code suit les directives que vous voulez suivre.

##### Remarque

Voir

* [Outils d'analyse statique](https://en.wikipedia.org/wiki/List_of_tools_for_static_code_analysis)
* [Outils de concurrence](#rconc-tools)
* [Outils de test](https://github.com/isocpp/CppCoreGuidelines/tree/master)

Il existe de nombreux autres types d’outils, tels que les dépôts de code source, les outils de build, etc., mais ces derniers dépassent le cadre de ces directives.

##### Remarque

Soyez prudent de ne pas devenir dépendant d’une chaîne d’outils trop élaborée ou trop spécialisée. Ceux-ci peuvent rendre votre code autrement portable non‑portable.

### <a name="rp-lib"></a>P.13 : Utiliser les bibliothèques de support de manière appropriée

##### Raison

Utiliser une bibliothèque bien conçue, bien documentée et bien supportée fait gagner du temps et des efforts ; sa qualité et sa documentation seront probablement plus bonnes que ce que vous pouvez faire si le temps majoritaire doit être consacré à l'implémentation. Le coût (temps, effort, argent, etc.) d’une bibliothèque peut être partagé entre de nombreux utilisateurs. Une bibliothèque largement utilisée est plus susceptible d’être mise à jour et portée vers de nouveaux systèmes qu’une application individuelle. La connaissance d’une bibliothèque largement utilisée peut faire gagner du temps dans d’autres projets futurs. Alors, si un domaine d’application existe, utilisez‑le.

##### Exemple

    std::sort(begin(v), end(v), std::greater<>());

À moins que vous ne soyez un expert en tri, vous ne l’écrireiez probablement pas plus correct. Vous avez une raison de ne pas utiliser la bibliothèque standard (ou les bibliothèques fondatrices) plutôt qu’une raison de l'utiliser.

##### Remarque

Par défaut utilisez

* La [Bibliothèque C++ ISO Standard](018-stdlib.md)
* La [Bibliothèque de support des Directives](#gsl-guidelines-support-library)

##### Remarque

Si aucune bibliothèque bien conçue, bien documentée et bien supportée n’existe pour un domaine important, peut‑être que vous devriez la concevoir et l’implémenter, puis l'utiliser.