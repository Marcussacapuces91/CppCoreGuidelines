---
title: Philosophie
---

# <a name="s-philosophy"></a>P : Philosophie

Les règles de cette section sont très générales.

Résumé des règles de philosophie :

* [P.1 : Exprimer les idées directement dans le code](#rp-direct)
* [P.2 : Écrire en C++ standard ISO](#rp-cplusplus)
* [P.3 : Exprimer l'intention](#rp-what)
* [P.4 : Idéalement, un programme doit être statiquement sûr au niveau des types](#rp-typesafe)
* [P.5 : Privilégier la vérification à la compilation à la vérification à l'exécution](#rp-compile-time)
* [P.6 : Ce qui ne peut pas être vérifié à la compilation doit être vérifiable à l'exécution](#rp-run-time)
* [P.7 : Détecter les erreurs d'exécution tôt](#rp-early)
* [P.8 : Ne fuyez aucune ressource](#rp-leak)
* [P.9 : Ne gaspillez ni temps ni espace](#rp-waste)
* [P.10 : Préférer les données immuables aux données mutables](#rp-mutable)
* [P.11 : Encapsuler les constructions désordonnées, plutôt que de les disperser dans le code](#rp-library)
* [P.12 : Utiliser les outils d'assistance de façon appropriée](#rp-tools)
* [P.13 : Utiliser les bibliothèques d'assistance de façon appropriée](#rp-lib)

Les règles philosophiques ne sont généralement pas vérifiables mécaniquement.  
En revanche, les règles individuelles reflétant ces thèmes philosophiques le sont.  
Sans base philosophique, les règles plus concrètes, spécifiques et vérifiables manquent de justification.

### <a name="rp-direct"></a>P.1 : Exprimer les idées directement dans le code

##### Raison

Les compilateurs ne lisent pas les commentaires (ni les documents de conception) et il en va de même pour de nombreux programmeurs (de façon cohérente). Ce qui est exprimé dans le code possède une sémantique définie et peut (en principe) être vérifié par les compilateurs et d'autres outils.

##### Exemple

    class Date {
    public:
        Month month() const;  // correct
        int month();          // incorrect
        // ...
    };

La première déclaration de `month` est explicite quant au retour d’un `Month` et au fait de ne pas modifier l’état de l’objet `Date`. La seconde version laisse le lecteur deviner et ouvre davantage de possibilités de bogues non détectés.

##### Exemple, mauvais

    void f(vector<string>& v)
    {
        string val;
        cin >> val;
        // ...
        int index = -1;                    // mauvais, il faudrait plutôt utiliser gsl::index
        for (int i = 0; i < v.size(); ++i) {
            if (v[i] == val) {
                index = i;
                break;
            }
        }
        // ...
    }

##### Exemple, bon

    void f(vector<string>& v)
    {
        string val;
        cin >> val;
        // ...
        auto p = find(begin(v), end(v), val);  // préférable
        // ...
    }

Une bibliothèque bien conçue exprime l’intention (ce qui doit être fait, plutôt que comment quelque chose est fait) bien mieux que l’utilisation directe des caractéristiques du langage.

Un programmeur C++ doit connaître les bases de la bibliothèque standard et l’utiliser quand c’est approprié.  
Tout programmeur doit connaître les bases des bibliothèques fondamentales du projet sur lequel il travaille, et les employer de façon adéquate.  
Tout programmeur suivant ces lignes directrices doit connaître la [bibliothèque de support des lignes directrices](#gsl-guidelines-support-library) et l’utiliser correctement.

##### Exemple

    change_speed(double s);   // mauvais : que signifie s ?
    // ...
    change_speed(2.3);

Une meilleure approche consiste à être explicite sur la signification du double (nouvelle vitesse ou delta sur l’ancienne vitesse ?) et sur l’unité utilisée :

    change_speed(Speed s);    // meilleur : le sens de s est spécifié
    // ...
    change_speed(2.3);        // erreur : aucune unité
    change_speed(23_m / 10s);  // mètres par seconde

Nous aurions pu accepter un `double` simple comme delta, mais cela aurait été source d’erreurs. Si nous voulions à la fois une vitesse absolue et des deltas, nous aurions défini un type `Delta`.

##### Application

Très difficile en général.

* utilisez `const` de façon cohérente (vérifiez si les fonctions membres modifient leur objet ; vérifiez si les fonctions modifient les arguments passés par pointeur ou référence)
* signalez l’utilisation de cast (les cast neutralisent le système de types)
* détectez le code qui imite la bibliothèque standard (difficile)

### <a name="rp-cplusplus"></a>P.2 : Écrire en C++ standard ISO

##### Raison

Il s’agit d’un ensemble de lignes directrices pour écrire du C++ standard ISO.

##### Note

Il existe des environnements où les extensions sont nécessaires, par ex., pour accéder aux ressources système. Dans ces cas, localisez l’utilisation des extensions nécessaires et contrôlez‑les à l’aide de lignes directrices de codage non‑core. Si possible, construisez des interfaces qui encapsulent les extensions afin qu’elles puissent être désactivées ou éliminées lors de la compilation sur des systèmes qui ne les supportent pas.

Les extensions n’ont souvent pas de sémantique rigoureusement définie. Même les extensions courantes, implémentées par plusieurs compilateurs, peuvent présenter des comportements légèrement différents et des cas limites, du fait de l’absence d’une définition standard stricte. Une utilisation suffisante de ces extensions affectera la portabilité attendue.

##### Note

Utiliser du C++ ISO valide ne garantit pas la portabilité (encore moins la correction). Évitez la dépendance à un comportement indéfini (par ex., [ordre d'évaluation indéfini](#res-order)) et soyez conscient des constructions dont la signification est définie par l’implémentation (par ex., `sizeof(int)`).

##### Note

Il existe des environnements où des restrictions sur l’utilisation des caractéristiques du langage ou de la bibliothèque standard C++ sont nécessaires, par ex., pour éviter l’allocation dynamique de mémoire comme l’exigent les normes de logiciels de contrôle d’aéronefs. Dans ces cas, contrôlez leur (non)utilisation avec une extension de ces lignes directrices personnalisée pour l’environnement spécifique.

##### Application

Utilisez un compilateur C++ à jour (actuellement C++20 ou C++17) avec un ensemble d’options qui n’acceptent pas les extensions.

### <a name="rp-what"></a>P.3 : Exprimer l'intention

##### Raison

À moins que l’intention d’un morceau de code ne soit exprimée (par ex., dans les noms ou les commentaires), il est impossible de savoir si le code fait ce qu’il est censé faire.

##### Exemple

    gsl::index i = 0;
    while (i < v.size()) {
        // ... faire quelque chose avec v[i] ...
    }

L’intention de « simplement parcourir les éléments de `v` » n’est pas exprimée ici. Le détail d’implémentation d’un index est exposé (et peut donc être mal utilisé), et `i` survit au‑delà du bloc de la boucle, ce qui peut ou ne peut pas être voulu. Le lecteur ne peut pas le savoir à partir de ce fragment de code.

Mieux :

    for (const auto& x : v) { /* faire quelque chose avec la valeur de x */ }

Il n’y a aucune mention explicite du mécanisme d’itération, et la boucle travaille sur une référence à des éléments `const` afin d’éviter toute modification accidentelle. Si la modification est souhaitée, indiquez‑le :

    for (auto& x : v) { /* modifier x */ }

Pour plus de détails sur les boucles `for`, voir [ES.71](#res-for-range). Parfois, il est encore préférable d’utiliser un algorithme nommé. Cet exemple utilise `for_each` du Ranges TS car il exprime directement l’intention :

    for_each(v, [](int x) { /* faire quelque chose avec la valeur de x */ });
    for_each(par, v, [](int x) { /* faire quelque chose avec la valeur de x */ });

La dernière variante montre clairement que l’ordre de traitement des éléments de `v` n’a pas d’importance.

Un programmeur devrait être familier avec  

* [la bibliothèque de support des lignes directrices](#gsl-guidelines-support-library)  
* [la bibliothèque standard ISO C++](#sl-the-standard-library)  
* quelles que soient les bibliothèques fondamentales utilisées pour le(s) projet(s) en cours  

##### Note

Formulation alternative : dire ce qui doit être fait, plutôt que simplement comment le faire.

##### Note

Certains constructs de langage expriment mieux l’intention que d’autres.

##### Exemple

Si deux `int` sont censés être les coordonnées d’un point 2‑D, indiquez‑le :

    draw_line(int, int, int, int);  // obscur : (x1,y1,x2,y2) ? (x,y,h,w) ? … ? il faut consulter la documentation
    draw_line(Point, Point);        // plus clair

##### Application

Recherchez les motifs courants pour lesquels il existe de meilleures alternatives  

* boucles `for` simples vs. boucles `for`‑range  
* interfaces `f(T*, int)` vs. interfaces `f(span<T>)`  
* variables de boucle trop larges dans leur portée  
* `new` et `delete` nus  
* fonctions avec de nombreux paramètres de types intégrés  

Il existe un vaste champ pour la transformation astucieuse et semi‑automatisée du code.

### <a name="rp-typesafe"></a>P.4 : Idéalement, un programme doit être statiquement sûr au niveau des types

##### Raison

Idéalement, un programme serait entièrement sûr au niveau des types (à la compilation). Malheureusement, ce n’est pas possible. Les zones problématiques :

* unions  
* casts  
* décrochage de tableau (array decay)  
* erreurs de portée (range errors)  
* conversions rétrécissantes (narrowing conversions)

##### Note

Ces zones sont sources de problèmes graves (p. ex., plantages et violations de sécurité). Nous proposons des techniques alternatives.

##### Application

Nous pouvons interdire, restreindre ou détecter séparément chaque catégorie de problème, selon les besoins et la faisabilité pour chaque programme. Toujours proposer une alternative. Par exemple :

* unions → utilisez `variant` (C++17)  
* casts → réduisez leur utilisation ; les modèles (templates) peuvent aider  
* décrochage de tableau → utilisez `span` (du GSL)  
* erreurs de portée → utilisez `span`  
* conversions rétrécissantes → réduisez leur usage et utilisez `narrow` ou `narrow_cast` (du GSL) lorsqu’elles sont nécessaires  

### <a name="rp-compile-time"></a>P.5 : Privilégier la vérification à la compilation à la vérification à l'exécution

##### Raison

Clarté du code et performances. Vous n’avez pas besoin d’écrire des gestionnaires d’erreurs pour des erreurs détectées à la compilation.

##### Exemple

    // Int est un alias utilisé pour les entiers
    int bits = 0;         // mauvais : code évitable
    for (Int i = 1; i; i <<= 1)
        ++bits;
    if (bits < 32)
        cerr << "Int trop petit\n";

Cet exemple n’atteint pas son objectif (car le dépassement de capacité est indéfini) et devrait être remplacé par un simple `static_assert` :

    // Int est un alias utilisé pour les entiers
    static_assert(sizeof(Int) >= 4);    // faire : vérification à la compilation

Ou mieux, utilisez simplement le système de types et remplacez `Int` par `int32_t`.

##### Exemple

    void read(int* p, int n);   // lire au plus n entiers dans *p

    int a[100];
    read(a, 1000);    // mauvais, dépasse la fin

better

    void read(span<int> r); // lire dans la plage d’entiers r

    int a[100];
    read(a);        // meilleur : laisser le compilateur déterminer le nombre d’éléments

**Formulation alternative** : ne reportez pas à l’exécution ce qui peut être fait correctement à la compilation.

##### Application

* recherchez les arguments pointeur.  
* recherchez les vérifications d’erreurs d’out‑of‑range à l’exécution.

### <a name="rp-run-time"></a>P.6 : Ce qui ne peut pas être vérifié à la compilation doit être vérifiable à l'exécution

##### Raison

Laisser des erreurs difficiles à détecter dans un programme, c’est inviter les plantages et les résultats erronés.

##### Note

Idéalement, nous attrapons toutes les erreurs (qui ne sont pas des erreurs de logique du programmeur) soit à la compilation, soit à l’exécution. Il est impossible d’attraper toutes les erreurs à la compilation et souvent trop coûteux de capturer toutes les erreurs restantes à l’exécution. Cependant, nous devrions écrire des programmes qui, en principe, puissent être vérifiés, à condition de disposer des ressources suffisantes (outils d’analyse, vérifications à l’exécution, ressources machines, temps).

##### Exemple, mauvais

    // compilé séparément, éventuellement chargé dynamiquement
    extern void f(int* p);

    void g(int n)
    {
        // mauvais : le nombre d’éléments n’est pas passé à f()
        f(new int[n]);
    }

Ici, une information cruciale (le nombre d’éléments) a été tellement « obscurcie » que l’analyse statique devient probablement impossible et la vérification dynamique très difficile lorsque `f()` fait partie d’une ABI que l’on ne peut pas « instrumenter ». On pourrait intégrer l’information utile dans le tas, mais cela nécessiterait des changements globaux du système et peut‑être du compilateur. Nous avons alors un design qui rend la détection d’erreurs très difficile.

##### Exemple, mauvais

    // compilé séparément, éventuellement chargé dynamiquement
    extern void f2(int* p, int n);

    void g2(int n)
    {
        // mauvais : le nombre d’éléments erroné peut être transmis à f2()
        f2(new int[n], n);
    }

Passer le nombre d’éléments en argument est meilleur (et bien plus courant) que de ne passer que le pointeur et de compter sur une convention non explicite. Cependant (comme le montre l’exemple), une simple faute de frappe peut introduire une erreur grave. La connexion entre les deux arguments de `f2()` est conventionnelle, plutôt qu’explicite.

De plus, il est implicite que `f2()` doit `delete` son argument (ou bien l’appelant a‑t‑il commis une seconde erreur ?).

##### Exemple, mauvais

    // compilé séparément, éventuellement chargé dynamiquement
    // NB : cela suppose que le code appelant est compatible ABI, utilisant un
    // compilateur C++ compatible et la même implémentation de la stdlib
    extern void f3(unique_ptr<int[]>, int n);

    void g3(int n)
    {
        f3(make_unique<int[]>(n), n);    // mauvais : passer la propriété et la taille séparément
    }

##### Exemple

    extern void f4(vector<int>&);   // compilé séparément, éventuellement chargé dynamiquement
    extern void f4(span<int>);      // compilé séparément, éventuellement chargé dynamiquement
                                    // NB : cela suppose que le code appelant est compatible ABI,
                                    // utilisant un compilateur C++ compatible et la même implémentation de la stdlib

    void g3(int n)
    {
        vector<int> v(n);
        f4(v);                     // passer une référence, conserver la propriété
        f4(span<int>{v});          // passer une vue, conserver la propriété
    }

Ce design transporte le nombre d’éléments comme partie intégrante d’un objet, de sorte que les erreurs sont peu probables et que la vérification dynamique (à l’exécution) est toujours faisable, même si elle n’est pas toujours abordable.

##### Exemple

    vector<int> f5(int n)    // OK : déplacement
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

    owner<int*> f7(int n)    // mauvais : perd n et on risque d’oublier de libérer
    {
        owner<int*> p = new int[n];
        // ... initialiser *p ...
        return p;
    }

##### Exemple

* ???
* montrer comment les vérifications possibles sont contournées par des interfaces qui passent des classes de base polymorphes, alors qu’elles connaissent réellement ce dont elles ont besoin ?
  Ou des chaînes de caractères comme options « libres ».

##### Application

* Signalez les interfaces de type (pointeur, compteur) (cela signalera de nombreux exemples qui ne peuvent pas être corrigés pour des raisons de compatibilité)
* ???

### <a name="rp-early"></a>P.7 : Détecter les erreurs d'exécution tôt

##### Raison

Éviter les plantages « mystérieux ». Éviter les erreurs qui mènent à des résultats (potentiellement non reconnus) erronés.

##### Exemple

    void increment1(int* p, int n)    // mauvais : sujet à l’erreur
    {
        for (int i = 0; i < n; ++i) ++p[i];
    }

    void use1(int m)
    {
        const int n = 10;
        int a[n] = {};
        // ...
        increment1(a, m);   // peut‑être une faute de frappe, peut‑être m <= n était prévu
                            // mais supposons que m == 20
        // ...
    }

Ici, une petite erreur dans `use1` conduit à des données corrompues ou à un plantage. L’interface (pointeur, compteur) laisse `increment1()` sans moyen réaliste de se défendre contre les accès hors limites. Si nous pouvions vérifier les indices pour les accès hors limites, l’erreur ne serait découverte que lorsqu’on accède à `p[10]`. Nous pourrions vérifier plus tôt et améliorer le code :

    void increment2(span<int> p)
    {
        for (int& x : p) ++x;
    }

    void use2(int m)
    {
        const int n = 10;
        int a[n] = {};
        // ...
        increment2({a, m});    // peut‑être une faute de frappe, peut‑être m <= n était prévu
        // ...
    }

Maintenant, `m <= n` peut être vérifié au point d’appel (tôt) plutôt que plus tard. Si la faute était simplement d’utiliser `n` comme borne, le code pourrait être encore simplifié (en éliminant la possibilité d’erreur) :

    void use3(int m)
    {
        const int n = 10;
        int a[n] = {};
        // ...
        increment2(a);   // le nombre d’éléments de a n’a pas besoin d’être répété
        // ...
    }

##### Exemple, mauvais

Ne vérifiez pas plusieurs fois la même valeur. Ne passez pas des données structurées sous forme de chaînes :

    Date read_date(istream& is);    // lire une date depuis un flux d’entrée

    Date extract_date(const string& s);    // extraire une date d’une chaîne

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

La date est validée deux fois (par le constructeur `Date`) et transmise sous forme de chaîne de caractères (données non structurées).

##### Exemple

Un contrôle excessif peut être coûteux. Il existe des cas où le contrôle précoce est inefficace car la valeur peut ne jamais être nécessaire, ou seule une partie de la valeur est plus facilement vérifiable que l’ensemble. De même, n’ajoutez pas de vérifications qui changent le comportement asymptotique de votre interface (par ex., n’ajoutez pas un contrôle `O(n)` à une interface dont la complexité moyenne est `O(1)`).

    class Jet {    // La physique dit : e * e < x * x + y * y + z * z
        float x;
        float y;
        float z;
        float e;
    public:
        Jet(float x, float y, float z, float e)
            :x(x), y(y), z(z), e(e)
        {
            // Doit‑on vérifier ici que les valeurs sont physiquement plausibles ?
        }

        float m() const
        {
            // Doit‑on gérer le cas dégénéré ici ?
            return sqrt(x * x + y * y + z * z - e * e);
        }

        ???
    };

La loi physique d’un jet (`e * e < x * x + y * y + z * z`) n’est pas un invariant à cause des possibles erreurs de mesure.

???

##### Application

* Examiner les pointeurs et les tableaux : faire le contrôle de portée tôt et pas de façon répétée  
* Examiner les conversions : éliminer ou signaler les conversions rétrécissantes  
* Rechercher les valeurs non vérifiées provenant des entrées  
* Rechercher les données structurées (objets de classe avec invariants) converties en chaînes de caractères  
* ???

### <a name="rp-leak"></a>P.8 : Ne fuyez aucune ressource

##### Raison

Même une croissance lente des ressources finira par épuiser la disponibilité de ces ressources. C’est particulièrement important pour les programmes de longue durée, mais constitue également un comportement de programmation responsable.

##### Exemple, mauvais

    void f(const char* name)
    {
        FILE* input = fopen(name, "r");
        // ...
        if (something) return;   // mauvais : si something == true, le descripteur de fichier est perdu
        // ...
        fclose(input);
    }

Préférez [RAII](#rr-raii) :

    void f(const char* name)
    {
        ifstream input {name};
        // ...
        if (something) return;   // OK : pas de fuite
        // ...
    }

**Voir aussi** : [La section de gestion des ressources](#s-resource)

##### Note

Une fuite est, familièrement, « tout ce qui n’est pas nettoyé ». La classification la plus importante est « tout ce qui ne peut plus être nettoyé ». Par exemple, allouer un objet sur le tas puis perdre le dernier pointeur qui pointe vers cette allocation. Cette règle ne doit pas être interprétée comme imposant que les allocations au sein d’objets de longue durée doivent être retournées lors de l’arrêt du programme. Par exemple, compter sur le nettoyage garanti par le système d’exploitation – fermeture de fichiers et désallocation de la mémoire lors de la terminaison du processus – peut simplifier le code. Cependant, compter sur des abstractions qui nettoient implicitement peut être tout aussi simple, et souvent plus sûr.

##### Note

Appliquer le [profil de sécurité de durée de vie](#ss-lifetime) élimine les fuites. Combiné avec la sécurité des ressources fournie par [RAII](#rr-raii), cela élimine le besoin de « ramassage de déchets » (en générant aucun déchet). En le combinant avec l’application des [profils de type et de limites](#ss-force), on obtient une sécurité totale de type et de ressource, garantie par les outils.

##### Application

* Examinez les pointeurs : classifiez‑les en non‑propriétaires (par défaut) et propriétaires. Dans la mesure du possible, remplacez les propriétaires par des gestionnaires de ressources de la bibliothèque standard (comme dans l’exemple ci‑dessus). Sinon, marquez un propriétaire avec `owner` du [GSL](#gsl-guidelines-support-library).  
* Cherchez les `new` et `delete` nus.  
* Cherchez les fonctions connues qui allouent des ressources et renvoient des pointeurs bruts (par ex., `fopen`, `malloc`, `strdup`).

### <a name="rp-waste"></a>P.9 : Ne gaspillez ni temps ni espace

##### Raison

C’est du C++.

##### Note

Le temps et l’espace investis de façon réfléchie pour atteindre un objectif (par ex., rapidité de développement, sécurité des ressources ou simplification des tests) ne sont pas du gaspillage.  
« Un autre avantage de viser l’efficacité est que le processus vous oblige à comprendre le problème plus en profondeur. » – Alex Stepanov

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
        // ... manipulate buffer ...
        X x;
        x.ch = 'a';
        x.s = string(n);    // allouer de l'espace à x.s pour *p
        for (gsl::index i = 0; i < x.s.size(); ++i) x.s[i] = buf[i];  // copier buf dans x.s
        delete[] buf;
        return x;
    }

    void driver()
    {
        X x = waste("Typical argument");
        // ...
    }

Oui, c’est une caricature, mais nous avons vu chaque erreur individuelle en production, et pire. Remarquez que la disposition de `X` garantit qu’au moins 6 octets (et très probablement plus) sont gaspillés. La définition superflue des opérations de copie désactive les sémantiques de déplacement, ce qui rend l’opération de retour lente (notez que l’optimisation de retour de valeur, RVO, n’est pas garantie ici). L’utilisation de `new` et `delete` pour `buf` est redondante ; si nous avions réellement besoin d’une chaîne locale, nous aurions simplement utilisé `string`. Il existe plusieurs autres bogues de performance et de complexité inutile.

##### Exemple, mauvais

    void lower(zstring s)
    {
        for (int i = 0; i < strlen(s); ++i) s[i] = tolower(s[i]);
    }

C’est en fait un exemple de code de production. Nous voyons que dans la condition, nous avons `i < strlen(s)`. Cette expression sera évaluée à chaque itération de la boucle, ce qui signifie que `strlen` doit parcourir la chaîne à chaque fois pour en découvrir la longueur. Bien que le contenu de la chaîne change, on suppose que `tolower` ne change pas la longueur de la chaîne, il vaut donc mieux mettre la longueur en cache avant la boucle afin d’éviter ce coût à chaque itération.

##### Note

Un exemple isolé de gaspillage est rarement significatif, et lorsqu’il l’est, il est généralement facilement éliminable par un expert. Cependant, un gaspillage répandu à travers une base de code peut rapidement devenir important et les experts ne sont pas toujours disponibles. Le but de cette règle (et des règles plus spécifiques qui la soutiennent) est d’éliminer la plupart des gaspillages liés à l’utilisation de C++ avant qu’ils n’apparaissent. Après cela, on pourra examiner le gaspillage lié aux algorithmes et aux exigences, ce qui dépasse le cadre de ces lignes directrices.

##### Application

De nombreuses règles plus spécifiques visent les objectifs globaux de simplicité et d’élimination du gaspillage gratuit.

* Signalez une valeur de retour inutilisée d’une fonction `operator++` ou `operator--` postfixe définie par l’utilisateur et non‑défaut. Privilégiez la forme préfixe. (Remarque : « non‑défaut » est destiné à réduire le bruit. Réévaluez cette application si elle reste trop bruyante en pratique.)

### <a name="rp-mutable"></a>P.10 : Préférer les données immuables aux données mutables

##### Raison

Il est plus facile de raisonner sur les constantes que sur les variables. Une donnée immuable ne peut pas changer de façon inattendue. Parfois l’immuabilité permet une meilleure optimisation. Vous ne pouvez pas avoir de data‑race sur une constante.

Voir [Con : Constantes et immuabilité](#s-const)

### <a name="rp-library"></a>P.11 : Encapsuler les constructions désordonnées, plutôt que de les disperser dans le code

##### Raison

Le code désordonné est plus susceptible de cacher des bogues et plus difficile à écrire. Une bonne interface est plus facile et plus sûre à utiliser. Le code bas‑niveau et désordonné engendre davantage de ce même code.

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

C’est bas‑niveau, verbeux et source d’erreurs. Par exemple, nous « avons » oublié de tester l’épuisement de mémoire et d’ajuster `sz`. À la place, nous pourrions utiliser `vector` :

    vector<int> v;
    v.reserve(100);
    // ...
    for (int x; cin >> x; ) {
        // ... vérifier que x est valide ...
        v.push_back(x);
    }

##### Note

La bibliothèque standard et le GSL sont des exemples de cette philosophie. Par exemple, au lieu de se battre avec les tableaux, les unions, les cast, les subtilités de durée de vie, `gsl::owner`, etc., qui sont nécessaires pour implémenter des abstractions clés comme `vector`, `span`, `lock_guard` ou `future`, nous utilisons les bibliothèques conçues et implémentées par des personnes disposant de plus de temps et d’expertise que nous. De même, nous pouvons et devons concevoir et implémenter des bibliothèques plus spécialisées, au lieu de laisser les utilisateurs (souvent nous‑mêmes) avec le défi de réécrire du code bas‑niveau à chaque fois. C’est une variante du [principe sous‑ensemble du sur‑ensemble](#r0) qui sous‑tend ces directives.

##### Application

* Recherchez « code désordonné » tel que la manipulation complexe de pointeurs et les cast en dehors de l’implémentation d’abstractions.

### <a name="rp-tools"></a>P.12 : Utiliser les outils d’assistance de façon appropriée

##### Raison

Beaucoup de tâches sont mieux réalisées « par machine ». Les ordinateurs ne se fatiguent pas et ne s’ennuient pas face aux tâches répétitives. Nous avons généralement de meilleures choses à faire que de répéter les mêmes tâches de routine.

##### Exemple

Exécuter un analyseur statique pour vérifier que votre code suit les lignes directrices que vous avez choisies.

##### Note

Voir  

* [Outils d’analyse statique](https://en.wikipedia.org/wiki/List_of_tools_for_static_code_analysis)  
* [Outils de concurrence](#rconc-tools)  
* [Outils de test](https://github.com/isocpp/CppCoreGuidelines/tree/master)

Il existe de nombreux autres types d’outils, tels que les dépôts de code source, les outils de construction, etc., mais ceux‑ci sont hors du champ de ces lignes directrices.

##### Note

Soyez prudent à ne pas devenir dépendant de chaînes d’outils trop élaborées ou trop spécialisées. Elles peuvent rendre votre code autrement portable non‑portable.

### <a name="rp-lib"></a>P.13 : Utiliser les bibliothèques d’assistance de façon appropriée

##### Raison

Utiliser une bibliothèque bien conçue, bien documentée et bien maintenue vous fait gagner du temps et des efforts ; sa qualité et sa documentation sont probablement supérieures à ce que vous pourriez obtenir en consacrant la majorité de votre temps à l’implémentation. Le coût (temps, effort, argent, etc.) d’une bibliothèque peut être partagé entre de nombreux utilisateurs. Une bibliothèque largement utilisée est plus susceptible d’être maintenue à jour et portée sur de nouveaux systèmes qu’une application individuelle. La connaissance d’une bibliothèque largement utilisée peut faire gagner du temps sur d’autres projets futurs. Ainsi, si une bibliothèque adaptée existe pour votre domaine d’application, utilisez‑la.

##### Exemple

    std::sort(begin(v), end(v), std::greater<>());

À moins d’être un expert en algorithmes de tri et de disposer de beaucoup de temps, il est plus probable que cela soit correct et plus rapide que tout code que vous écririez pour une application spécifique. Vous avez besoin d’une raison pour ne pas utiliser la bibliothèque standard (ou les bibliothèques fondamentales que votre application utilise) plutôt que d’une raison pour l’utiliser.

##### Note

Par défaut, utilisez  

* La [bibliothèque standard ISO C++](#sl-the-standard-library)  
* La [bibliothèque de support des lignes directrices](#gsl-guidelines-support-library)

##### Note

Si aucune bibliothèque bien conçue, bien documentée et bien supportée n’existe pour un domaine important, peut‑être devriez‑vous la concevoir et l’implémenter, puis l’utiliser.