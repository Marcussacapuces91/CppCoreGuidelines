# <a name="s-philosophy"></a>P : Philosophie

La section de règles est très générale.

Résumé des règles philosophiques :

* [P.1 : Exprimez directement les idées dans le code](004-philosophy.md#rp-direct)
* [P.2 : Écrivez en ISO Standard C++](004-philosophy.md#rp-cplusplus)
* [P.3 : Exprimez l'intention](004-philosophy.md#rp-what)
* [P.4 : Idéalement, un programme devrait être statiquement type‑sûr](004-philosophy.md#rp-typesafe)
* [P.5 : Privilégiez la vérification à la compilation aux vérifications à l'exécution](004-philosophy.md#rp-compile-time)
* [P.6 : Ce qui ne peut pas être vérifié à la compilation doit être vérifiable à l'exécution](004-philosophy.md#rp-run-time)
* [P.7 : Détectez les erreurs à l'exécution dès que possible](004-philosophy.md#rp-early)
* [P.8 : Ne laissez pas de fuites de ressources](004-philosophy.md#rp-leak)
* [P.9 : Ne gaspillez pas de temps ou d'espace](004-philosophy.md#rp-waste)
* [P.10 : Préférez les données immuables aux données mutables](004-philosophy.md#rp-mutable)
* [P.11 : Encapsulez les constructions désordonnées plutôt que de les répandre dans le code](004-philosophy.md#rp-library)
* [P.12 : Utilisez les outils de support de manière appropriée](004-philosophy.md#rp-tools)
* [P.13 : Utilisez les bibliothèques de support de manière appropriée](004-philosophy.md#rp-lib)

### <a name="rp-direct"></a>P.1 : Exprimez directement les idées dans le code

#### Raison

Les compilateurs ne lisent pas les commentaires (ou les documents de conception) et la plupart des programmeurs (de façon cohérente) ne le font pas non plus. Ce qui est exprimé dans le code a une sémantique définie et peut, en principe, être vérifié par les compilateurs et d'autres outils.

#### Exemple

    class Date {
    public:
        Month month() const;  // bon
        int month();          // mauvais
        // ...
    };

La première déclaration de `month` rend explicite qu'elle retourne un `Month` et ne modifie pas l'état de l'objet `Date`. La deuxième version laisse le lecteur deviner et ouvre plus de possibilités de bugs non détectés.

#### Exemple, mauvais

Cette boucle est une version restreinte de `std::find` :

    void f(vector<string>& v)
    {
        string val;
        cin >> val;
        // ...
        int index = -1;                    // mauvais, et devrait utiliser gsl::index
        for (int i = 0; i < v.size(); ++i) {
            if (v[i] == val) {
                index = i;
                break;
            }
        }
        // ...
    }

#### Exemple, bon

Une expression beaucoup plus claire de l'intention serait :

    void f(vector<string>& v)
    {
        string val;
        cin >> val;
        // ...
        auto p = find(begin(v), end(v), val);  // mieux
        // ...
    }

Une bibliothèque bien conçue exprime mieux l'intention (ce que l'on doit faire, plutôt que simplement comment quelque chose est effectué) que l'utilisation directe des fonctionnalités du langage.

Un programmeur C++ devrait connaître les bases de la bibliothèque standard et l'utiliser lorsque c'est approprié. Tout programmeur doit connaître les bases des bibliothèques fondamentales du projet en cours de travail et les utiliser de façon appropriée. Un programmeur suivant ces lignes directrices doit connaître la [bibliothèque de support des directives](#gsl-guidelines-support-library) @TODO-LINK et l'utiliser de façon appropriée.

#### Exemple

    // change_speed(double s);   // mauvais : que signifie s ?
    // ...
    change_speed(2.3);

Une approche meilleure consiste à être explicite sur le sens du double (nouvelle vitesse ou incrément sur la vitesse actuelle ?) et l'unité utilisée :

    change_speed(Speed s);    // mieux : la signification de s est spécifiée
    // ...
    change_speed(2.3);        // erreur : pas d'unité
    change_speed(23_m / 10s);  // mètres par seconde

On aurait pu accepter un double sans unité en tant qu'incrément, mais cela aurait été sujet à erreur. Si nous voulions à la fois la vitesse absolue et les incréments, on aurait défini un type `Delta`.

#### Application

Très difficile en général.

* Utiliser `const` de façon cohérente (vérifier si les fonctions membres modifient leur objet ; vérifier si les fonctions modifient les arguments passés par pointeur ou référence)
* Marquer l'usage de cast (les cast neutralisent le système de types)
* Détecter le code qui imite la bibliothèque standard (difficile)

### <a name="rp-cplusplus"></a>P.2 : Écrivez en ISO Standard C++

#### Raison

Il s'agit d'un ensemble de lignes directrices pour écrire du C++ ISO Standard.

#### Remarque

Il existe des environnements où des extensions sont nécessaires, par exemple pour accéder aux ressources système. Dans de tels cas, localisez l'utilisation des extensions nécessaires et contrôlez leur usage avec des lignes directrices non‑core. Si possible, construisez des interfaces qui encapsulent les extensions de façon à ce qu'elles puissent être désactivées ou compilées loin des systèmes ne les supportant pas.

Les extensions n'ont souvent pas de sémantique définie de façon rigoureuse. Même les extensions courantes et implémentées par plusieurs compilateurs peuvent présenter de légères variations de comportement et de cas limites, en raison du fait qu'elles ne possèdent pas une définition standard rigoureuse. L'utilisation suffisante de toute telle extension peut compromettre la portabilité attendue.

#### Remarque

L'utilisation d'un C++ valide ISO ne garantit pas la portabilité (quoique) ni la correction. Évitez de dépendre du comportement non défini (p. ex., [ordre d'évaluation indéfini](010-expr.md#res-order) @TODO-LINK) et soyez conscient des constructions dont la signification est définie par l'implémentation (p. ex., `sizeof(int)`).

#### Remarque

Il existe des environnements où des restrictions sur l'utilisation du langage ou des bibliothèques C++ standard sont nécessaires, par exemple pour éviter l'allocation dynamique mémoire, comme le exige les normes logicielles de contrôle aéronautique. Dans de tels cas, contrôlez leur usage avec une extension de ces lignes directrices adaptée à l'environnement spécifique.

#### Application

Utilisez un compilateur C++ à jour (actuellement C++20 ou C++17) avec un ensemble d'options qui n'accepte pas d'extensions.

### <a name="rp-what"></a>P.3 : Exprimez l'intention

#### Raison

Si l'intention d'un morceau de code n'est pas déclarée (par exemple dans les noms ou les commentaires), il est impossible de déterminer si le code fait ce qu'il est censé faire.

#### Exemple

    gsl::index i = 0;
    while (i < v.size()) {
        // ... faire quelque chose avec v[i] ...
    }

L'intention de simplement parcourir les éléments de `v` n'est pas exprimée ici. Le détail d'implémentation d'un index est exposé (ce qui peut conduire à une mauvaise utilisation), et `i` dépasse le domaine de la boucle, ce qui peut ou non être prévu. Le lecteur ne peut pas savoir à partir de cette section de code.

#### Exemple, bon

    for (const auto& x : v) { /* faire quelque chose avec la valeur de x */ }

Ici, il n'y a pas de mention explicite du mécanisme d'itération, et la boucle opère sur une référence à des éléments `const`, afin d'empêcher toute modification accidentelle. Si une modification est souhaitée, précisez‑la :

    for (auto& x : v) { /* modifier x */ }

Pour plus de détails sur les instructions `for`, voir [ES.71](010-expr.md#res-for-range) @TODO-LINK.

Parfois encore mieux, utilisez un algorithme nommé. Cet exemple utilise `for_each` de la TS Ranges parce qu'il exprime directement l'intention :

    for_each(v, [](int x) { /* faire quelque chose avec la valeur de x */ });
    for_each(par, v, [](int x) { /* faire quelque chose avec la valeur de x */ });

La dernière variante clarifie que nous ne nous intéressons pas à l'ordre dans lequel les éléments de `v` sont manipulés.

Un programmeur doit être familier avec

* La [bibliothèque de support des directives](#gsl-guidelines-support-library) @TODO-LINK
* La [bibliothèque standard ISO C++](#sl-the-standard-library) @TODO-LINK
* Toutes les bibliothèques fondamentales utilisées pour le projet courant

#### Remarque

Formulation alternative : dites ce qui doit être fait, plutôt que simplement comment cela doit être fait.

#### Remarque

Certains constructeurs de langage expriment mieux l'intention que d'autres.

#### Exemple

Si deux `int` sont censés être les coordonnées d'un point 2D, précisez‑le :

    draw_line(int, int, int, int);  // obscur : (x1,y1,x2,y2)? (x,y,h,w)? ...?
    // ...
    draw_line(Point, Point);        // plus clair

### <a name="rp-typesafe"></a>P.4 : Idéalement, un programme devrait être statiquement type‑sûr

#### Raison

Idéalement, un programme serait entièrement sûr au niveau du type à la compilation. Malheureusement, ce n'est pas possible. Les zones problématiques :

* unions
* casts
* dégradation des tableaux
* erreurs de plage
* conversions restrictives

#### Remarque

Ces domaines sont à l'origine de problèmes graves (par exemple, plantages et violations de sécurité). Nous essayons de fournir des techniques alternatives.

#### Application

Nous pouvons interdire, restreindre ou détecter séparément les catégories de problèmes individuels, selon les besoins et la faisabilité pour chaque programme. Toujours suggérer une alternative. Par exemple :

* unions — utilisez `variant` (en C++17)
* casts — minimisez leur utilisation ; les modèles peuvent aider
* dégradation de tableau — utilisez `span` (du GSL)
* erreurs de plage — utilisez `span`
* conversions restrictives — minimisez leur utilisation et utilisez `narrow` ou `narrow_cast` (du GSL) lorsqu'elles sont nécessaires

### <a name="rp-compile-time"></a>P.5 : Privilégiez la vérification à la compilation aux vérifications à l'exécution

#### Raison

Clarté du code et performance. Vous n'avez pas besoin d'écrire des gestionnaires d'erreurs pour les erreurs détectées à la compilation.

#### Exemple

    // Int est un alias utilisé pour les entiers
    int bits = 0;         // ne faites pas : code évitable
    for (Int i = 1; i; i <<= 1)
        ++bits;
    if (bits < 32)
        cerr << "Int too small\n";

Cet exemple ne parvient pas à atteindre ce qu'il essaie de faire (car le dépassement est indéfini) et devrait être remplacé par une simple `static_assert` :

    // Int est un alias utilisé pour les entiers
    static_assert(sizeof(Int) >= 4);    // do : vérification à la compilation

Ou mieux encore en utilisant le système de types et en remplaçant `Int` par `int32_t`.

#### Exemple

    void read(int* p, int n);   // lire au plus n entiers dans *p

    int a[100];
    read(a, 1000);    // mauvais, dépassement

meilleur

    void read(span<int> r); // lire dans la plage d'entiers r

    int a[100];
    read(a);        // mieux : laissez le compilateur déterminer le nombre d'éléments

**Alternative formulation** : Ne retardez pas à l'exécution ce qui peut être fait au niveau de la compilation.

#### Application

* Cherchez des arguments pointeurs.
* Cherchez des vérifications d'extremité à l'exécution.

### <a name="rp-run-time"></a>P.6 : Ce qui ne peut pas être vérifié à la compilation doit être vérifiable à l'exécution

#### Raison

Laisser des erreurs difficiles à détecter dans un programme conduit à des plantages et à de mauvais résultats.

#### Remarque

Idéalement, nous capturons toutes les erreurs (qui ne sont pas des erreurs de logique du programmeur) soit à la compilation, soit à l'exécution. Il est impossible de capturer toutes les erreurs à la compilation et souvent il n'est pas rentable de capturer toutes les erreurs restantes à l'exécution. Cependant, nous devons nous efforcer d'écrire des programmes qui, en principe, peuvent être vérifiés, compte tenu de ressources suffisantes (programmes d'analyse, vérifications d'exécution, ressources matérielles, temps).

#### Exemple, mauvais

    // compilé distinctement, peut-être chargé dynamiquement
    extern void f(int* p);

    void g(int n)
    {
        // mauvais : le nombre d'éléments n'est pas passé à f()
        f(new int[n]);
    }

Ici, une information cruciale (le nombre d'éléments) est si obscure qu'une analyse statique devient probablement inefficace et la vérification dynamique peut être très difficile lorsqu`f()` fait partie d'une ABI afin que nous ne puissions pas « instrumenter » ce pointeur. On pourrait encapsuler ces informations utiles dans le tas, mais cela requiert des changements globaux du système et peut‑être du compilateur. Ce design rend la détection d'erreurs très difficile.

#### Exemple, mauvais

    // compilé distinctement, peut-être chargé dynamiquement
    extern void f2(int* p, int n);

    void g2(int n)
    {
        // mauvais : le mauvais nombre d'éléments peut être passé à f2()
        f2(new int[n], n);
    }

Passer le nombre d'éléments en tant qu'argument est mieux (et beaucoup plus commun) que simplement passer un pointeur et compter sur une convention (non déclarée) pour connaître ou découvrir le nombre d'éléments. Cependant, comme montré, une simple faute de frappe peut introduire une erreur grave. La connexion entre les deux arguments de `f2()` est conventionnelle, plutôt que explicite.

Également, c'est implicite que `f2()` doit `delete` son argument (ou l'appelant a-t-il fait une seconde erreur ?).

#### Exemple, mauvais

    // compilé distinctement, peut-être chargé dynamiquement
    // NB : ceci suppose que le code appelant est ABI compatible, utilisant un compilateur C++ compatible et la même implémentation de la bibliothèque standard
    extern void f3(unique_ptr<int[]>, int n);

    void g3(int n)
    {
        f3(make_unique<int[]>(n), m);    // mauvais : passer la propriété et la taille séparément
    }

#### Exemple

Nous devons passer le pointeur et le nombre d'éléments en tant qu'objet intégr
e :

    extern void f4(vector<int>&);   // compilé distinctement, peut-être chargé dynamiquement
    extern void f4(span<int>);      // compilé distinctement, peut-être chargé dynamiquement
                                    // NB : ce qui précité suppose que le code appelant est ABI compatible, utilisant un compilateur C++ compatible et la même implémentation de la bibliothèque standard

    void g3(int n)
    {
        vector<int> v(n);
        f4(v);                     // passer une référence, conserver la propriété
        f4(span<int>{v});          // passer une vue, conserver la propriété
    }

Cette conception porte le nombre d'éléments tel que partie intégrante d'un objet, de sorte que les erreurs sont peu probables et la vérification d'exécution est toujours faisable, si ce n'est toujours abordable.

#### Exemple

Comment transférons‑nous la propriété et toutes les informations nécessaires pour valider l'usage ?

    vector<int> f5(int n)    // OK : move
    {
        vector<int> v(n);
        // ... initialiser v ...
        return v;
    }

    unique_ptr<int[]> f6(int n)    // mauvais : perd n
    {
        auto p = make_unique<int[]>(n);
        // ... initialiser *p ...
        return p;
    }

    owner<int*> f7(int n)    // mauvais : perd n et nous pourrions oublier de delete
    {
        owner<int*> p = new int[n];
        // ... initialiser *p ...
        return p;
    }

#### Exemple

* … (en attente)
* montrer comment les vérifications possibles sont évitées par les interfaces qui passent des classes de base polymorphes, lorsque le programmeur connaît réellement ce dont il a besoin ? Ou bien des chaînes de caractères comme « free‑style » options

#### Application

* Marquer (pointeur, nombre)-style interfaces (cela marquera beaucoup d'exemples qui ne peuvent pas être corrigés pour des raisons de compatibilité)
* …

### <a name="rp-early"></a>P.7 : Détectez les erreurs à l'exécution dès que possible

#### Raison

Évitez les plantages mystérieux. Évitez les erreurs conduisant à (probablement non reconnus) mauvais résultats.

#### Exemple, mauvais

    void increment1(int* p, int n)    // mauvais : sujet à erreurs
    {
        for (int i = 0; i < n; ++i) ++p[i];
    }

    void use1(int m)
    {
        const int n = 10;
        int a[n] = {};
        // ...
        increment1(a, m);   // peut-être faute de frappe, peut-être que m <= n est prévu
                            // mais supposons que m == 20
        // ...
    }

Ici, nous avons fait une petite erreur dans `use1` qui conduira à des données corrompues ou à un plantage. L'interface (pointeur, nombre)-type ne donne pas à `increment1()` aucun moyen réaliste de se défendre contre les erreurs hors plage. Si nous pouvions vérifier les sous‑indices hors limites, alors l'erreur ne serait découverte que lorsqu`p[10]` est accédé. Nous pourrions vérifier plus tôt et améliorer le code  :

    void increment2(span<int> p)
    {
        for (int& x : p) ++x;
    }

    void use2(int m)
    {
        const int n = 10;
        int a[n] = {};
        // ...
        increment2({a, m});    // peut-être faute de frappe, peut-être que m <= n est prévu
        // ...
    }

À présent, `m <= n` peut être vérifié au point d'appel (début) plutôt qu'après. Si tout ce que nous avions était une faute de frappe pour utiliser `n` comme la limite, le code pourrait être simplifié davantage (éliminer la possibilité d'une erreur) :

    void use3(int m)
    {
        const int n = 10;
        int a[n] = {};
        // ...
        increment2(a);   // le nombre d'éléments de a n'a pas besoin d'être répété
        // ...
    }

#### Exemple, mauvais

Ne pas vérifier à plusieurs reprises la même valeur. Ne pas passer des données structurées sous forme de chaînes :

    Date read_date(istream& is);    // lire la date depuis istream

    Date extract_date(const string& s);    // extraire la date depuis une chaîne

    void user1(const string& date)    // manipuler la date
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

#### Exemple

Le sur‑vérification peut coûter. Il existe des cas où la vérification précoce est inefficace car vous ne revoyez peut être pas besoin de la valeur, ou vous n'avez besoin que d'une partie de la valeur qui est plus facilement vérifiée que la totalité. De même, ne pas ajouter des vérifications de validité qui changent le comportement asymptotique de votre interface (par ex., ne pas ajouter une vérification `O(n)` à une interface dont la complexité moyenne est `O(1)`).

    class Jet {    // Physique : e * e < x * x + y * y + z * z
        float x;
        float y;
        float z;
        float e;
    public:
        Jet(float x, float y, float z, float e)
            :x(x), y(y), z(z), e(e)
        {
            // Devrais‑je vérifier ici que les valeurs sont physiquement significatives ?
        }

        float m() const
        {
            // Devrais‑je gérer le cas dégénéré ici ?
            return sqrt(x * x + y * y + z * z - e * e);
        }

        ???
    };

La loi physique pour un jet (`e * e < x * x + y * y + z * z`) n'est pas une invariant car de la possibilité d'erreurs de mesure.

???  

#### Application

* Examinez les pointeurs et les tableaux : faites une vérification de plage en début et pas plusieurs fois
* Examinez les conversions : éliminez ou marquez les conversions restrictives
* Cherchez les valeurs non vérifiées provenant de l'entrée
* Cherchez les données structurées (objets de classes avec des invariants) se convertissant en chaînes
* …

### <a name="rp-leak"></a>P.8 : Ne laissez pas de fuites de ressources

#### Raison

Même une croissance lente des ressources finira, au fil du temps, par épuiser la disponibilité de ces ressources. Cela est particulièrement important pour les programmes à longue exécution, mais constitue un élément essentiel du comportement responsable de la programmation.

#### Exemple, mauvais

    void f(const char* name)
    {
        FILE* input = fopen(name, "r");
        // ...
        if (something) return;   // mauvais : si something == true, une poignée de fichier est perdue
        // ...
        fclose(input);
    }

Préférez [RAII](009-resource.md#rr-raii) :

    void f(const char* name)
    {
        ifstream input {name};
        // ...
        if (something) return;   // OK : aucune fuite
        // ...
    }

**Voir également** : [La section de gestion des ressources](009-resource.md)

#### Remarque

Une fuite est un « tout ce qui n'est pas nettoyé ». La classification la plus importante est « tout ce qui ne peut plus être nettoyé ». Par exemple, allouer un objet dans le tas puis perdre le dernier pointeur qui pointe vers cette allocation. Cette règle ne doit pas être interprétée comme exigeant que les allocations dans les objets à long terme soient renvoyées lors de l'arrêt du programme. Par exemple, compter sur un nettoyage garanti par le système tel que la fermeture de fichier et la libération de mémoire lors de l'arrêt du processus peut simplifier le code. Cependant, s'appuyer sur des abstractions qui nettoient implicitement peut être aussi simple et souvent plus sûr.

#### Remarque

L'application du [profil de sécurité de durée de vie](022-profile.md#ss-lifetime) élimine les fuites. Lorsque combiné avec la sécurité des ressources fournie par [RAII](009-resource.md#rr-raii), il élimine le besoin de « collection des déchets » (en générant aucun rebut). Associez cela à l'application des profils de type et de borne [003-introduction.md#ss-force] et vous obtenez une sécurité complète du type et des ressources, garantie par des outils.

#### Application

* Examinez les pointeurs : classez-les en non‑propriétaires (valeur par défaut) et propriétaires. Là où c'est faisable, remplacez les propriétaires par des gestionnaires de ressources de la bibliothèque standard (comme dans l'exemple ci‑dessus). Sinon, marquez un propriétaire via `owner` du [GSL](#gsl-guidelines-support-library) @TODO-LINK.
* Recherchez `new` et `delete` nus
* Recherchez les fonctions d'allocation de ressources connues retournant des pointeurs bruts (telles que `fopen`, `malloc`, `strdup`)

### <a name="rp-waste"></a>P.9 : Ne gaspillez pas de temps ou d'espace

#### Raison

C++.

#### Remarque

Le temps et l'espace que vous consacrez bien à atteindre un objectif (par ex., vitesse de développement, sécurité des ressources, ou simplification des tests) n'est pas gaspillé. « Un autre avantage de viser à l'efficacité c'est que le processus vous oblige à comprendre le problème plus en profondeur » – Alex Stepanov

#### Exemple, mauvais

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
        // ... manipulate buffer ...
        X x;
        x.ch = 'a';
        x.s = string(n);    // donner à x.s de l'espace pour *p
        for (gsl::index i = 0; i < x.s.size(); ++i) x.s[i] = buf[i];  // copier buf dans x.s
        delete[] buf;
        return x;
    }

    void driver()
    {
        X x = waste("Typical argument");
        // ...
    }

Oui, c'est un caricature, mais nous avons vu chaque erreur individuelle en production, et pire. Notez que la disposition de `X` garantit qu'au moins 6 octets (et probablement plus) sont gaspillés. La définition supplémentaire des opérations de copie empêche la sémantique de déplacement, ce qui rend l'opération de retour lente (notez que le RVO n'est pas garanti). L'utilisation de `new` et `delete` pour `buf` est redondante ; si nous avions vraiment besoin d'une chaîne locale, nous devrions utiliser une chaîne locale. Il y a d'autres bogues de performance et des complications gratuit ou inutiles.

#### Exemple, mauvais

    void lower(zstring s)
    {
        for (int i = 0; i < strlen(s); ++i) s[i] = tolower(s[i]);
    }

Ceci est en fait un exemple de production. Nous voyons dans notre condition que `i < strlen(s)`. Cette expression sera évaluée à chaque itération de la boucle, ce qui signifie que `strlen` doit parcourir la chaîne à chaque boucle pour découvrir sa longueur. Alors que le contenu de la chaîne change, il est supposé que `tolower` ne modifie pas la longueur de la chaîne, il vaut mieux mémoriser la longueur à l'extérieur de la boucle et ne pas payer ce coût à chaque itération.

#### Remarque

Un exemple individuel de gaspillage n'est généralement pas significatif, et lorsqu'il l'est, il est généralement facilement éliminable par un expert. Cependant, un gaspillage répandu dans un code base peut être significatif, et les experts ne sont pas toujours aussi disponibles que nous le souhaiterions. L'objectif de cette règle (et des règles plus spécifiques qui la soutiennent) est d'éliminer la plupart des gaspillages liés à l'utilisation de C++ avant qu'il ne se produise. Après cela, nous pouvons examiner le gaspillage lié aux algorithmes et aux exigences, mais cela dépasse le cadre de ces lignes directrices.

#### Application

Beaucoup de règles spécifiques visent les objectifs globaux de simplicité et d'élimination du gaspillage gratuit.

* Marquer une valeur de retour non utilisé d'une fonction incrément/postfix `operator++` ou `operator--` définie par l'utilisateur. Privilégiez l'utilisation de la forme préfixe. (Remarque : « User‑defined non‑defaulted » est destiné à réduire le bruit. Revérifiez cette application si elle est trop bruyante en pratique.)

### <a name="rp-mutable"></a>P.10 : Préférez les données immuables aux données mutables

#### Raison

Il est plus facile de raisonner sur les constantes que sur les variables. Quelque chose d'immuable ne peut pas changer de façon inattendue. Parfois l'immuabilité permet de meilleures optimisations. Vous ne pouvez pas avoir une course de données sur une constante.

Voir [Con : constantes et immutabilité](014-const.md)

### <a name="rp-library"></a>P.11 : Encapsulez les constructions désordonnées plutôt que de les répandre dans le code

#### Raison

Un code désordonné a plus de chances de cacher des bogues et est plus difficile à écrire. Une interface bien conçue est plus simple et plus sûre à utiliser. Un code pas‑mélangeant… etc.

#### Exemple

    int sz = 100;
    int* p = (int*) malloc(sizeof(int) * sz);
    int count = 0;
    // ...
    for (;;) {
        // ... lire un entier dans x, quitter la boucle si fin du fichier est atteinte ...
        // ... vérifier que x est valide ...
        if (count == sz)
            p = (int*) realloc(p, sizeof(int) * sz * 2);
        p[count++] = x;
        // ...
    }

C'est bas niveau, verbeux et sujet aux erreurs. Par exemple, nous « oubliâmes » de tester l'épuisement de la mémoire et d'assigner une nouvelle valeur à `sz`. Au lieu de cela, nous pourrions utiliser `vector` :

    vector<int> v;
    v.reserve(100);
    // ...
    for (int x; cin >> x; ) {
        // ... vérifier que x est valide ...
        v.push_back(x);
    }

#### Remarque

La bibliothèque standard et le GSL sont des exemples de cette philosophie. Par exemple, plutôt que de se battre avec les tableaux, les unions, les casts, les problèmes de durée de vie, `gsl::owner`, etc., nécessaires pour implémenter les abstractions clés telles que `vector`, `span`, `lock_guard`, et `future`, nous utilisons des bibliothèques conçues et mises en œuvre par des personnes possédant plus de temps et d'expertise que nous. De même, nous pouvons concevoir et implémenter des bibliothèques plus spécialisées, plutôt que de laisser les utilisateurs (souvent nous-mêmes) à la tâche de coder à bas niveau régulièrement. C'est une variante du principe « subset du superset » (voir 003‑introduction.md#r0) qui sous‑tend ces lignes directrices.

#### Application

* Cherchez « code désordonné » tel que manipulation complexe de pointeurs et cast en dehors de l'implémentation des abstractions.

### <a name="rp-tools"></a>P.12 : Utilisez les outils de support de manière appropriée

#### Raison

Il existe de nombreuses tâches réalisées mieux « par une machine ». Les ordinateurs ne se fatigaront pas de la même façon qu'un humain. Nous avons souvent plus de choses à faire que de répéter des tâches routinières.

#### Exemple

Exécutez un analyseur statique pour vérifier que votre code suit les lignes directrices que vous voulez qu'il suive.

#### Remarque

Voir

* [Outils d'analyse statique](https://en.wikipedia.org/wiki/List_of_tools_for_static_code_analysis)
* [Outils de concurrence](012-concurrency.md#rconc-tools)
* [Outils de test](https://github.com/isocpp/CppCoreGuidelines/tree/master)

Il existe d'autres types d'outils, tels que les dépôts de code source, les outils de build, etc., mais ils sont hors portée de ces lignes directrices.

#### Remarque

Soyez prudent de ne pas devenir dépendant de chaînes d'outils trop élaborées ou trop spécialisées. Elles peuvent rendre votre code autrement portable, non portable.

### <a name="rp-lib"></a>P.13 : Utilisez les bibliothèques de support de manière appropriée

#### Raison

Utiliser une bibliothèque bien conçue, bien documentée, et bien prise en charge vous fait gagner du temps et des efforts ; sa qualité et sa documentation sont susceptibles d'être supérieures à ce que vous pourriez faire si une majorité de votre temps doit être consacrée à une implémentation. Le coût (temps, effort, argent, etc.) d'une bibliothèque peut être partagé par de nombreux utilisateurs. Une bibliothèque largement utilisée est plus susceptible d'être moderne et portée sur de nouveaux systèmes qu'une application individuelle. La connaissance d'une bibliothèques largement utilisée peut économiser du temps sur d'autres projets / futurs projets. Alors, si une bibliothèque adaptée à votre domaine d'application existe, utilisez‑la.

#### Exemple

    std::sort(begin(v), end(v), std::greater<>());

À moins d'être un expert dans les algorithmes de tri, vous n'aurez qu'un texte plus rapide et plus robuste que n'importe quoi que vous écriviez pour une application spécifique. Vous avez besoin d'une raison pour ne pas utiliser la bibliothèque standard (ou toute autre bibliothèque sous‑fondation utilisée par votre application) plutôt qu'une raison pour l'utiliser.

#### Remarque

Par défaut utilisez

* La [bibliothèque standard ISO C++](#sl-the-standard-library) @TODO-LINK
* La [bibliothèque de support des directives](#gsl-guidelines-support-library) @TODO-LINK

#### Remarque

Si aucune bibliothèque bien conçue, bien documentée, et bien prise en charge n'existe pour un domaine important, peut‑être devriez‑vous la concevoir et l'implémenter, puis l'utiliser.