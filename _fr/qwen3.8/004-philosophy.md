# <a name="s-philosophy"></a>P : Philosophie

Les règles de cette section sont très générales.

Résumé des règles de philosophie :

* [P.1 : Exprimer les idées directement dans le code](004-philosophy.md#rp-direct)
* [P.2 : Écrire en C++ standard ISO](004-philosophy.md#rp-cplusplus)
* [P.3 : Exprimer l'intention](004-philosophy.md#rp-what)
* [P.4 : Idéalement, un programme doit être sûre de type statiquement](004-philosophy.md#rp-typesafe)
* [P.5 : Privilégier les vérifications au temps de compilation plutôt qu'au temps d'exécution](004-philosophy.md#rp-compile-time)
* [P.6 : Ce qui ne peut pas être vérifié au temps de compilation doit pouvoir l'être au temps d'exécution](004-philosophy.md#rp-run-time)
* [P.7 : Détecter les erreurs d'exécution tôt](004-philosophy.md#rp-early)
* [P.8 : Ne jamais fuir de ressources](004-philosophy.md#rp-leak)
* [P.9 : Ne pas gaspiller du temps ou de l'espace](004-philosophy.md#rp-waste)
* [P.10 : Privilégier les données immuables aux données mutables](004-philosophy.md#rp-mutable)
* [P.11 : Encapsuler les constructions complexes plutôt que de les disséminer dans le code](004-philosophy.md004-philosophy.md#rp-library)
* [P.12 : Utiliser les outils d'assistance lorsque c'est approprié](004-philosophy.md#rp-tools)
* [P.13 : Utiliser les bibliothèques d'assistance lorsque c'est approprié](004-philosophy.md#rp-lib)

Les règles philosophiques ne sont généralement pas vérifiables de manière mécanique.
En revanche, des règles individuelles reflétant ces thèmes philosophiques le sont.
Sans un fondement philosophique, les règles plus concrètes/spécifiques/vérifiables manquent de justification.

### <a name="rp-direct"></a>P.1 : Exprimer les idées directement dans le code

##### Raison

Les compilateurs ne lisent pas les commentaires (ni les documents de conception), et beaucoup de programmeurs non plus (pas de façon constante).
Ce qui est exprimé dans le code a une sémantique définie et peut (en principe) être vérifié par les compilateurs et d'autres outils.

##### Exemple

    class Date {
    public:
        Month month() const;  // à faire
        int month();          // à ne pas faire
        // ...
    };

La première déclaration de `month` est explicite quant au fait de retourner un `Month` et de ne pas modifier l'état de l'objet `Date`.
La deuxième version laisse le lecteur deviner et ouvre la porte à plus de bugs potentiels non détectés.

##### Exemple, mauvais

Cette boucle est une forme restreinte de `std::find` :

    void f(vector<string>& v)
    {
        string val;
        cin >> val;
        // ...
        int index = -1;                    // mauvais, de plus devrait utiliser gsl::index
        for (int i = 0; i < v.size(); ++i) {
            if (v[i] == val) {
                index = i;
                break;
            }
        }
        // ...
    }

##### Exemple, bon

Une expression beaucoup plus claire de l'intention serait :

    void f(vector<string>& v)
    {
        string val;
        cin >> val;
        // ...
        auto p = find(begin(v), end(v), val);  // mieux
        // ...
    }

Une bibliothèque bien conçue exprime l'intention (ce qui doit être fait, plutôt que simplement comment quelque chose est fait) bien mieux que l'utilisation directe des fonctionnalités du langage.

Un programmeur C++ doit connaître les bases de la bibliothèque standard et l'utiliser lorsqu'il y a lieu.
Tout programmeur doit connaître les bases des bibliothèques fondamentales du projet sur lequel il travaille et les utiliser de manière appropriée.
Tout programmeur utilisant ces directives doit connaître la [bibliothèque de support des directives](#gsl-guidelines-support-library) @TODO-LINK, et l'utiliser de manière appropriée.

##### Exemple

    change_speed(double s);   // mauvais : que signifie s ?
    // ...
    change_speed(2.3);

Une meilleure approche consiste à être explicite quant au sens du double (nouvelle vitesse ou différence par rapport à l'ancienne vitesse ?) et à l'unité utilisée :

    change_speed(Speed s);    // mieux : le sens de s est précisé
    // ...
    change_speed(2.3);        // erreur : pas d'unité
    change_speed(23_m / 10s);  // mètres par seconde

Nous aurions pu accepter un simple `double` (sans unité) comme différence, mais cela aurait été source d'erreurs.
Si nous avions voulu à la fois la vitesse absolue et les différences, nous aurions défini un type `Delta`.

##### Application

Très difficile en général.

* utiliser `const` de façon cohérente (vérifier si les fonctions membres modifient leur objet ; vérifier si les fonctions modifient les arguments passés par pointeur ou par référence)
* signaler les utilisations de conversions de type (les conversions neutralisent le système de types)
* détecter le code qui imite la bibliothèque standard (difficile)

### <a name="rp-cplusplus"></a>P.2 : Écrire en C++ standard ISO

##### Raison

Ceci est un ensemble de directives pour écrire du C++ standard ISO.

##### Remarque

Il existe des environnements où des extensions sont nécessaires, par exemple pour accéder aux ressources système.
Dans de tels cas, localiser l'utilisation des extensions nécessaires et contrôler leur usage avec des directives de codage non fondamentales.  Si possible, concevoir des interfaces qui encapsulent les extensions afin qu'elles puissent être désactivées ou éliminées lors de la compilation sur des systèmes qui ne prennent pas en charge ces extensions.

Les extensions n'ont souvent pas de sémantique rigoureusement définie.  Même les extensions
courantes et implémentées par plusieurs compilateurs peuvent avoir des comportements légèrement
différents et des cas limites aux comportements inattendus, directement en raison de l'absence
d'une définition standard rigoureuse.  Une utilisation suffisante de toute extension de ce type
aura un impact sur la portabilité attendue.

##### Remarque

L'utilisation de C++ ISO valide ne garantit pas la portabilité (pourtant moins que la correction).
Éviter la dépendance à un comportement indéfini (par exemple, [l'ordre indéfini d'évaluation](010-expr.md#res-order))
et prendre conscience des constructions au sens défini par l'implémentation (par exemple, `sizeof(int)`).

##### Remarque

Il existe des environnements où des restrictions sur l'utilisation de fonctionnalités du langage ou de la bibliothèque C++ standard sont nécessaires, par exemple pour éviter l'allocation dynamique de mémoire comme l'exigent les normes logicielles de pilotage d'aéronefs.
Dans de tels cas, contrôler leur (non-)utilisation par une extension de ces directives de codage adaptée à l'environnement spécifique.

##### Application

Utiliser un compilateur C++ à jour (actuellement C++20 ou C++17) avec un ensemble d'options qui n'acceptent pas les extensions.

### <a name="rp-what"></a>P.3 : Exprimer l'intention

##### Raison

À moins que l'intention d'un code ne soit exprimée (par exemple, dans des noms ou des commentaires), il est impossible de savoir si le code fait ce qu'il est censé faire.

##### Exemple

    gsl::index i = 0;
    while (i < v.size()) {
        // ... faire quelque chose avec v[i] ...
    }

L'intention de « simplement » parcourir les éléments de `v` n'est pas exprimée ici. Le détail d'implémentation d'un index est exposé (et pourrait donc être mal utilisé), et `i` dépasse le portée de la boucle, ce qui peut ou non être intentionnel. Le lecteur ne peut pas le savoir à partir de cet extrait de code seul.

Mieux :

    for (const auto& x : v) { /* faire quelque chose avec la valeur de x */ }

Ici, il n'y a plus de mention explicite du mécanisme d'itération, et la boucle opère sur une référence à des éléments `const` pour qu'une modification accidentelle ne puisse pas se produire. Si la modification est souhaitée, le dire :

    for (auto& x : v) { /* modifier x */ }

Pour plus de détails sur les énoncés for, voir [ES.71](010-expr.md#res-for-range).
Parfois encore mieux, utiliser un algorithme nommé. Cet exemple utilise `for_each` du TS Ranges car il exprime directement l'intention :

    for_each(v, [](int x) { /* faire quelque chose avec la valeur de x */ });
    for_each(par, v, [](int x) { /* faire quelque chose avec la valeur de x */ });

La dernière variante rend clair que nous ne sommes pas intéressés par l'ordre dans lequel les éléments de `v` sont traités.

Un programmeur devrait être familier avec

* [La bibliothèque de support des directives](#gsl-guidelines-support-library) @TODO-LINK
* [La bibliothèque standard C++ ISO](#sl-the-standard-library) @TODO-LINK
* Les bibliothèques fondamentales utilisées pour le(s) projet(s) actuel(s)

##### Remarque

Formulation alternative : Dire ce qui doit être fait, plutôt que simplement comment il doit être fait.

##### Remarque

Certaines constructions du langage expriment mieux l'intention que d'autres.

##### Exemple

Si deux `int` sont censés être les coordonnées d'un point 2D, le dire :

    draw_line(int, int, int, int);  // obscur : (x1,y1,x2,y2) ? (x,y,h,w) ? ... ?
                                    // il faut consulter la documentation pour savoir

    draw_line(Point, Point);        // plus clair

##### Application

Rechercher les schémas courants pour lesquels de meilleures alternatives existent

* les boucles `for` simples vs. les boucles `for` par plage
* les interfaces `f(T*, int)` vs. les interfaces `f(span<T>)`
* les variables de boucle dans un portée trop large
* les `new` et `delete` nus
* les fonctions avec de nombreux paramètres de types intégrés

Il y a une immense place pour l'ingéniosité et la transformation semi-automatique de programmes.

### <a name="rp-typesafe"></a>P.4 : Idéalement, un programme doit être sûre de type statiquement

##### Raison

Idéalement, un programme serait complètement sûr de type statiquement (au temps de compilation).
Malheureusement, cela n'est pas possible. Domaines problématiques :

* les unions
* les conversions de type (casts)
* la dégradation de tableau
* les erreurs de portée
* les conversions par rétrécissement

##### Remarque

Ces domaines sont sources de problèmes graves (par exemple, des plantages et des violations de sécurité).
Nous essayons de fournir des techniques alternatives.

##### Application

Nous pouvons interdire, restreindre ou détecter les catégories de problèmes individuelles séparément, selon les besoins et les possibilités pour des programmes individuels.
Toujours suggérer une alternative.
Par exemple :

* unions -- utiliser `variant` (en C++17)
* conversions de type -- minimiser leur utilisation ; les gabarits peuvent aider
* dégradation de tableau -- utiliser `span` (de la GSL)
* erreurs de portée -- utiliser `span`
* conversions par rétrécissement -- minimiser leur utilisation et utiliser `narrow` ou `narrow_cast` (de la GSL) là où elles sont nécessaires

### <a name="rp-compile-time"></a>P.5 : Privilégier les vérifications au temps de compilation plutôt qu'au temps d'exécution

##### Raison

Clarté du code et performance.
On n'a pas besoin d'écrire des gestionnaires d'erreurs pour des erreurs détectées au temps de compilation.

##### Exemple

    // Int est un alias utilisé pour les entiers
    int bits = 0;         // à ne pas faire : code évitable
    for (Int i = 1; i; i <<= 1)
        ++bits;
    if (bits < 32)
        cerr << "Int too small\n";

Cet exemple échoue à atteindre ce qu'il essaie d'accomplir (car le dépassement de capacité est indéfini) et devrait être remplacé par un simple `static_assert` :

    // Int est un alias utilisé pour les entiers
    static_assert(sizeof(Int) >= 4);    // à faire : vérification au temps de compilation

Ou encore mieux, simplement utiliser le système de types et remplacer `Int` par `int32_t`.

##### Exemple

    void read(int* p, int n);   // lit au maximum n entiers dans *p

    int a[100];
    read(a, 1000);    // mauvais, hors limites

mieux

    void read(span<int> r); // lit dans la plage d'entiers r

    int a[100];
    read(a);        // mieux : laisser le compilateur déterminer le nombre d'éléments

**Formulation alternative** : Ne pas reporter au temps d'exécution ce qui peut être bien fait au temps de compilation.

##### Application

* Rechercher les arguments pointeurs.
* Rechercher les vérifications au temps d'exécution de violations de portée.

### <a name="rp-run-time"></a>P.6 : Ce qui ne peut pas être vérifié au temps de compilation doit pouvoir l'être au temps d'exécution

##### Raison

Laisser des erreurs difficiles à détecter dans un programme, c'est s'exposer à des plantages et à de mauvais résultats.

##### Remarque

Idéalement, nous capturons toutes les erreurs (qui ne sont pas des erreurs de logique du programmeur) soit au temps de compilation, soit au temps d'exécution. Il est impossible de capturer toutes les erreurs au temps de compilation et souvent trop coûteux de capturer toutes les erreurs restantes au temps d'exécution. Cependant, nous devrions nous efforcer d'écrire des programmes qui, en principe, peuvent être vérifiés, moyennant des ressources suffisantes (programmes d'analyse, vérifications au temps d'exécution, ressources machine, temps).

##### Exemple, mauvais

    // compilé séparément, peut-être chargé dynamiquement
    extern void f(int* p);

    void g(int n)
    {
        // mauvais : le nombre d'éléments n'est pas transmis à f()
        f(new int[n]);
    }

Ici, un élément crucial d'information (le nombre d'éléments) a été si thoroughly « obscurci » que l'analyse statique est probablement rendue infeasible et la vérification dynamique peut être très difficile lorsque `f()` fait partie d'une ABI, de sorte que nous ne pouvons pas « instrumenter » ce pointeur. Nous pourrions intégrer des informations utiles dans la pile libre, mais cela nécessite des changements globaux au système et peut-être au compilateur. Ce que nous avons ici est une conception qui rend la détection d'erreurs très difficile.

##### Exemple, mauvais

Bien sûr, nous pouvons transmettre le nombre d'éléments avec le pointeur :

    // compilé séparément, peut-être chargé dynamiquement
    extern void f2(int* p, int n);

    void g2(int n)
    {
        // mauvais : un mauvais nombre d'éléments peut être transmis à f2()
        f2(new int[n], n);
    }

Transmettre le nombre d'éléments comme argument est mieux (et beaucoup plus courant) que de simplement passer le pointeur et de compter sur une convention (non formulée) pour connaître ou découvrir le nombre d'éléments. Cependant (comme montré), une simple coquille peut introduire une erreur grave. Le lien entre les deux arguments de `f2()` est conventionnel, plutôt qu'explicite.

De plus, il est implicite que `f2()` est censée `delete` son argument (ou l'appelant a-t-il fait une deuxième erreur ?).

##### Exemple, mauvais

Les pointeurs de gestion de ressources de la bibliothèque standard échouent à transmettre la taille lorsqu'ils pointent vers un objet :

    // compilé séparément, peut-être chargé dynamiquement
    // NB : cela suppose que le code appelant est compatible ABI, utilisant un
    // compilateur C++ compatible et la même implémentation de stdlib
    extern void f3(unique_ptr<int[]>, int n);

    void g3(int n)
    {
        f3(make_unique<int[]>(n), m);    // mauvais : transmettre la propriété et la taille séparément
    }

##### Exemple

Nous devons transmettre le pointeur et le nombre d'éléments comme un objet intégré :

    extern void f4(vector<int>&);   // compilé séparément, peut-être chargé dynamiquement
    extern void f4(span<int>);      // compilé séparément, peut-être chargé dynamiquement
                                    // NB : cela suppose que le code appelant est compatible ABI, utilisant un
                                    // compilateur C++ compatible et la même implémentation de stdlib

    void g3(int n)
    {
        vector<int> v(n);
        f4(v);                     // passer une référence, conserver la propriété
        f4(span<int>{v});          // passer une vue, conserver la propriété
    }

Cette conception transporte le nombre d'éléments comme une partie intégrante d'un objet, de sorte que les erreurs sont peu probables et que la vérification dynamique (au temps d'exécution) est toujours faisable, même si pas toujours abordable.

##### Exemple

Comment transférer à la fois la propriété et toutes les informations nécessaires pour valider l'utilisation ?

    vector<int> f5(int n)    // OK : mouvement
    {
        vector<int> v(n);
        // ... initialiser v ...
        return v;
    }

    unique_ptr<int[]> f6(int n)    // mauvais : perd n
    {
        auto p = make_unique<int[]>(n);
        // ... initialiser *p ...
        return p;
    }

    owner<int*> f7(int n)    // mauvais : perd n et nous pourrions oublier de delete
    {
        owner<int*> p = new int[n];
        // ... initialiser *p ...
        return p;
    }

##### Exemple

* ???
* montrer comment les vérifications possibles sont évitées par des interfaces qui transmettent des classes de base polymorphes, alors qu'elles savent en fait de quoi elles ont besoin ?
  Ou les chaînes de caractères comme options en « style libre »

##### Application

* Signaler les interfaces de style (pointeur, nombre) (cela signalera beaucoup d'exemples qui ne peuvent pas être corrigés pour des raisons de compatibilité)
* ???

### <a name="rp-early"></a>P.7 : Détecter les erreurs d'exécution tôt

##### Raison

Éviter les plantages « mystérieux ».
Éviter les erreurs menant à des résultats incorrects (éventuellement non reconnus).

##### Exemple

    void increment1(int* p, int n)    // mauvais : source d'erreurs
    {
        for (int i = 0; i < n; ++i) ++p[i];
    }

    void use1(int m)
    {
        const int n = 10;
        int a[n] = {};
        // ...
        increment1(a, m);   // peut-être une coquille, peut-être m <= n est censé
                            // mais supposons que m == 20
        // ...
    }

Ici, nous avons fait une petite erreur dans `use1` qui mènera à des données corrompues ou à un plantage.
L'interface de style (pointeur, nombre) ne laisse à `increment1()` aucun moyen réaliste de se défendre contre les accès hors limites.
Si nous pouvions vérifier les index hors limites, l'erreur ne serait pas découverte avant l'accès à `p[10]`.
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
        increment2({a, m});    // peut-être une coquille, peut-être m <= n est censé
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

##### Exemple, mauvais

Ne pas vérifier la même valeur à plusieurs reprises. Ne pas transmettre des données structurées comme des chaînes de caractères :

    Date read_date(istream& is);    // lit une date depuis istream

    Date extract_date(const string& s);    // extrait une date d'une chaîne

    void user1(const string& date)    // manipule la date
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

La date est validée deux fois (par le constructeur de `Date`) et transmise comme chaîne de caractères (données non structurées).

##### Exemple

Un excès de vérifications peut être coûteux.
Il y a des cas où vérifier tôt est inefficace car vous n'aurez peut-être jamais besoin de la valeur, ou n'aurez peut-être besoin que d'une partie de la valeur qui est plus facilement vérifiable que le tout.  De même, n'ajoutez pas de vérifications de validité qui modifient le comportement asymptotique de votre interface (par exemple, n'ajoutez pas une vérification en `O(n)` à une interface dont la complexité moyenne est `O(1)`).

    class Jet {    // La physique dit : e * e < x * x + y * y + z * z
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
            // Dois-je gérer le cas dégénéré ici ?
            return sqrt(x * x + y * y + z * z - e * e);
        }

        ???
    };

La loi physique pour un jet (`e * e < x * x + y * y + z * z`) n'est pas un invariant en raison de la possibilité d'erreurs de mesure.

???

##### Application

* Examiner les pointeurs et les tableaux : faire la vérification de portée tôt et non de manière répétée
* Examiner les conversions : éliminer ou marquer les conversions par rétrécissement
* Rechercher les valeurs non vérifiées provenant de l'entrée
* Rechercher les données structurées (objets de classes avec invariants) converties en chaînes de caractères
* ???

### <a name="rp-leak"></a>P.8 : Ne jamais fuir de ressources

##### Raison

Même une croissance lente des ressources finira, avec le temps, par épuiser la disponibilité de ces ressources.
Ceci est particulièrement important pour les programmes à longue durée d'exécution, mais c'est un élément essentiel d'un comportement de programmation responsable.

##### Exemple, mauvais

    void f(const char* name)
    {
        FILE* input = fopen(name, "r");
        // ...
        if (something) return;   // mauvais : si something == true, un descripteur de fichier est perdu
        // ...
        fclose(input);
    }

Privilégier [RAII](009-resource.md#rr-raii) :

    void f(const char* name)
    {
        ifstream input {name};
        // ...
        if (something) return;   // OK : pas de fuite
        // ...
    }

**Voir aussi** : [La section sur la gestion des ressources](009-resource.md)

##### Remarque

Une fuite est communément « tout ce qui n'est pas nettoyé ».
La classification plus importante est « tout ce qui ne peut plus être nettoyé ».
Par exemple, allouer un objet sur le tas puis perdre le dernier pointeur qui pointe vers cette allocation.
Cette règle ne devrait pas être comprise comme exigeant que les allocations dans des objets à longue durée de vie soient rendues à l'arrêt du programme.
Par exemple, s'appuyer sur le nettoyage garanti par le système comme la fermeture des fichiers et le libération de la mémoire à l'arrêt du processus peut simplifier le code.
Cependant, s'appuyer sur des abstractions qui nettoient implicitement peut être aussi simple, et souvent plus sûr.

##### Remarque

L'application du [profil de sûreté de durée de vie](022-profile.md#ss-lifetime) élimine les fuites.
Combinée à la sûreté des ressources fournie par [RAII](009-resource.md#rr-raii), elle élimine le besoin de « collecte des ordures » (en ne générant aucun déchet).
Combiner cela avec l'application des [profils de type et de portée](003-introduction.md#ss-force) et on obtient une sûreté complète des types et des ressources, garantie par des outils.

##### Application

* Examiner les pointeurs : les classer en non-propriétaires (la valeur par défaut) et propriétaires.
  Là où c'est faisable, remplacer les propriétaires par des descripteurs de ressources de la bibliothèque standard (comme dans l'exemple ci-dessus).
  Sinon, marquer un propriétaire comme tel en utilisant `owner` de [la GSL](#gsl-guidelines-support-library) @TODO-LINK.
* Rechercher les `new` et `delete` nus
* Rechercher les fonctions d'allocation de ressources connues qui renvoient des pointeurs bruts (tels que `fopen`, `malloc`, et `strdup`)

### <a name="rp-waste"></a>P.9 : Ne pas gaspiller du temps ou de l'espace

##### Raison

C'est du C++.

##### Remarque

Le temps et l'espace bien dépensés pour atteindre un objectif (par exemple, la vitesse de développement, la sûreté des ressources, ou la simplification des tests) ne sont pas gaspillés.
« Un autre avantage de viser l'efficacité est que le processus vous force à comprendre le problème en profondeur. » - Alex Stepanov

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

Oui, c'est une caricature, mais nous avons vu chaque erreur individuelle dans du code de production, et pire encore.
Notez que la disposition de `X` garantit qu'au moins 6 octets (et probablement plus) sont gaspillés.
La définition superflue des opérations de copie désactive les sémantiques de mouvement, rendant l'opération de retour lente
(veuillez noter que l'Optimisation de la Valeur de Retour, RVO, n'est pas garantie ici).
L'utilisation de `new` et `delete` pour `buf` est redondante ; si nous avions vraiment besoin d'une chaîne locale, nous devrions utiliser une chaîne `string` locale.
Il y a plusieurs autres bugs de performance et une complication gratuite.

##### Exemple, mauvais

    void lower(zstring s)
    {
        for (int i = 0; i < strlen(s); ++i) s[i] = tolower(s[i]);
    }

C'est en fait un exemple provenant de code de production.
On peut voir que dans notre condition nous avons `i < strlen(s)`. Cette expression sera évaluée à chaque itération de la boucle, ce qui signifie que `strlen` doit parcourir la chaîne à chaque itération pour découvrir sa longueur. Bien que le contenu de la chaîne change, il est supposé que `tolower` n'affectera pas la longueur de la chaîne, il est donc préférable de mettre en cache la longueur hors de la boucle et de ne pas assumer ce coût à chaque itération.

##### Remarque

Un exemple individuel de gaspillage est rarement significatif, et là où c'est significatif, c'est généralement facilement éliminé par un expert.
Cependant, un gaspillage répandu à travers une base de code peut facilement être significatif et les experts ne sont pas toujours aussi disponibles que nous le souhaiterions.
L'objectif de cette règle (et des règles plus spécifiques qui la soutiennent) est d'éliminer la plupart des gaspillages liés à l'utilisation de C++ avant qu'ils ne se produisent.
Après cela, nous pouvons examiner les gaspillages liés aux algorithmes et aux exigences, mais cela dépasse le cadre de ces directives.

##### Application

Beaucoup plus de règles spécifiques visent les objectifs globaux de simplicité et d'élimination des gaspillages gratuits.

* Signaler une valeur de retour inutilisée d'une fonction `operator++` ou `operator--` postfixée non par défaut définie par l'utilisateur. Privilégier l'utilisation de la forme préfixée. (Note : « Non par défaut définie par l'utilisateur » est destiné à réduire le bruit. Réexaminer cette application si elle est toujours trop bruyante en pratique.)


### <a name="rp-mutable"></a>P.10 : Privilégier les données immuables aux données mutables

##### Raison

Il est plus facile de raisonner sur des constantes que sur des variables.
Quelque chose d'immuable ne peut pas changer de manière inattendue.
Parfois l'immuabilité permet une meilleure optimisation.
On ne peut pas avoir de concurrence de données sur une constante.

Voir [Con : Constantes et immuabilité](014-const.md)

### <a name="rp-library"></a>P.11 : Encapsuler les constructions complexes plutôt que de les disséminer dans le code

##### Raison

Le code complexe est plus susceptible de cacher des bugs et est plus difficile à écrire.
Une bonne interface est plus facile et plus sûre à utiliser.
Le code bas niveau et complexe engendre plus de tel code.

##### Exemple

    int sz = 100;
    int* p = (int*) malloc(sizeof(int) * sz);
    int count = 0;
    // ...
    for (;;) {
        // ... lire un int dans x, quitter la boucle si fin de fichier atteinte ...
        // ... vérifier que x est valide ...
        if (count == sz)
            p = (int*) realloc(p, sizeof(int) * sz * 2);
        p[count++] = x;
        // ...
    }

Ceci est du code bas niveau, verbeux et source d'erreurs.
Par exemple, nous avons « oublié » de tester l'épuisement de la mémoire et d'assigner la nouvelle valeur à `sz`.
À la place, nous pourrions utiliser `vector` :

    vector<int> v;
    v.reserve(100);
    // ...
    for (int x; cin >> x; ) {
        // ... vérifier que x est valide ...
        v.push_back(x);
    }

##### Remarque

La bibliothèque standard et la GSL sont des exemples de cette philosophie.
Par exemple, au lieu de manipuler les tableaux, les unions, les conversions de type, les problèmes de durée de vie complexes, `gsl::owner`, etc.,
nécessaires pour implémenter des abstractions clés, telles que `vector`, `span`, `lock_guard` et `future`, nous utilisons les bibliothèques
conçues et implémentées par des personnes ayant plus de temps et d'expertise que nous n'en avons généralement.
De même, nous pouvons et devrions concevoir et implémenter des bibliothèques plus spécialisées, plutôt que de laisser les utilisateurs (souvent nous-mêmes)
le défi de faire correctement du code bas niveau à répétition.
Ceci est une variante du [principe de sous-ensemble du sur-ensemble](003-introduction.md#r0) qui sous-tend ces directives.

##### Application

* Rechercher le « code complexe » tel que la manipulation complexe de pointeurs et les conversions de type en dehors de l'implémentation d'abstractions.


### <a name="rp-tools"></a>P.12 : Utiliser les outils d'assistance lorsque c'est approprié

##### Raison

Il y a beaucoup de choses qui sont mieux faites « par machine ».
Les ordinateurs ne se fatiguent pas ni ne s'ennuient avec des tâches répétitives.
Nous avons généralement de meilleures choses à faire que de répéter des tâches routinières.

##### Exemple

Exécuter un analyseur statique pour vérifier que votre code suit les directives que vous souhaitez qu'il suive.

##### Remarque

Voir

* [Outils d'analyse statique](https://en.wikipedia.org/wiki/List_of_tools_for_static_code_analysis)
* [Outils de concurrence](012-concurrency.md#rconc-tools)
* [Outils de test](https://github.com/isocpp/CppCoreGuidelines/tree/master)

Il existe beaucoup d'autres types d'outils, tels que les dépôts de code source, les outils de build, etc.,
mais ceux-ci sont hors du champ de ces directives.

##### Remarque

Faites attention à ne pas devenir dépendant de chaînes d'outils sur-élaborées ou sur-spécialisées.
Celles-ci peuvent rendre votre code autrement portable non portable.


### <a name="rp-lib"></a>P.13 : Utiliser les bibliothèques d'assistance lorsque c'est approprié

##### Raison

L'utilisation d'une bibliothèque bien conçue, bien documentée et bien supportée fait gagner du temps et de l'effort ;
sa qualité et sa documentation sont susceptibles d'être supérieures à ce que vous pourriez faire
si la majorité de votre temps devait être consacrée à une implémentation.
Le coût (temps, effort, argent, etc.) d'une bibliothèque peut être partagé entre de nombreux utilisateurs.
Une bibliothèque largement utilisée est plus susceptible d'être maintenue à jour et移植ée sur de nouveaux systèmes qu'une application individuelle.
La connaissance d'une bibliothèque largement utilisée peut faire gagner du temps sur d'autres/futurs projets.
Donc, si une bibliothèque appropriée existe pour votre domaine d'application, utilisez-la.

##### Exemple

    std::sort(begin(v), end(v), std::greater<>());

À moins que vous ne soyez un expert en algorithmes de tri et que vous ayez amplement de temps,
c'est plus susceptible d'être correct et d'exécuter plus rapidement que n'importe quoi que vous écririez pour une application spécifique.
Vous avez besoin d'une raison de ne pas utiliser la bibliothèque standard (ou les bibliothèques fondamentales que votre application utilise) plutôt que d'une raison de l'utiliser.

##### Remarque

Par défaut, utiliser

* [La bibliothèque standard C++ ISO](#sl-the-standard-library) @TODO-LINK
* [La bibliothèque de support des directives](#gsl-guidelines-support-library) @TODO-LINK

##### Remarque

Si aucune bibliothèque bien conçue, bien documentée et bien supportée n'existe pour un domaine important,
peut-être devriez-vous la concevoir et l'implémenter, puis l'utiliser.