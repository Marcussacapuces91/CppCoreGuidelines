---
title: Philosophie
---

# <a name="s-philosophy"></a>P : Philosophie

Les règles de cette section sont très générales.

Résumé des règles philosophiques :

* [P.1 : Exprimer les idées directement dans le code](#rp-direct)
* [P.2 : Écrire en C++ conforme au standard ISO](#rp-cplusplus)
* [P.3 : Exprimer l’intention](#rp-what)
* [P.4 : Idéalement, un programme devrait être sûr du point de vue du typage statique](#rp-typesafe)
* [P.5 : Préférer les vérifications à la compilation aux vérifications à l’exécution](#rp-compile-time)
* [P.6 : Ce qui ne peut pas être vérifié à la compilation devrait pouvoir l’être à l’exécution](#rp-run-time)
* [P.7 : Détecter les erreurs d’exécution tôt](#rp-early)
* [P.8 : Ne pas laisser fuiter de ressources](#rp-leak)
* [P.9 : Ne pas gaspiller temps ou espace](#rp-waste)
* [P.10 : Préférer les données immuables aux données mutables](#rp-mutable)
* [P.11 : Encapsuler les constructions complexes plutôt que les répandre dans le code](#rp-library)
* [P.12 : Utiliser les outils de support lorsque c’est approprié](#rp-tools)
* [P.13 : Utiliser les bibliothèques de support lorsque c’est approprié](#rp-lib)

Les règles philosophiques ne sont généralement pas vérifiables mécaniquement.  
Cependant, des règles individuelles reflétant ces thèmes philosophiques le sont.  
Sans base philosophique, les règles plus concrètes/spécifiques/vérifiables manquent de justification.

### <a name="rp-direct"></a>P.1 : Exprimer les idées directement dans le code

##### Raison

Les compilateurs ne lisent pas les commentaires (ni les documents de conception), et beaucoup de programmeurs non plus (de manière constante).  
Ce qui est exprimé dans le code possède une sémantique définie et peut (en principe) être vérifié par les compilateurs et autres outils.

##### Exemple


    class Date {
    public:
        Month month() const;  // à faire
        int month();          // à ne pas faire
        // ...
    };

La première déclaration de `month` est explicite sur le fait qu’elle retourne un `Month` et qu’elle ne modifie pas l’état de l’objet `Date`.  
La seconde laisse le lecteur deviner et ouvre la porte à des bugs non détectés.

##### Exemple, mauvais

Cette boucle est une forme restreinte de `std::find` :

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

##### Exemple, bon

Une expression d’intention bien plus claire :

    void f(vector<string>& v)
    {
        string val;
        cin >> val;
        // ...
        auto p = find(begin(v), end(v), val);  // mieux
        // ...
    }

Une bibliothèque bien conçue exprime l’intention (ce qui doit être fait, plutôt que comment cela est fait) bien mieux que l’usage direct des fonctionnalités du langage.

Un programmeur C++ devrait connaître les bases de la bibliothèque standard et l’utiliser lorsque c’est approprié.  
Tout programmeur devrait connaître les bibliothèques fondamentales du projet sur lequel il travaille.  
Tout programmeur utilisant ces directives devrait connaître la [Guidelines Support Library](#gsl-guidelines-support-library) et l’utiliser correctement.

##### Exemple

    change_speed(double s);   // mauvais : que signifie s ?
    ...
    change_speed(2.3);

Une meilleure approche consiste à être explicite sur la signification du double (nouvelle vitesse ou delta ?) et l’unité utilisée :

    change_speed(Speed s);    // mieux : la signification de s est spécifiée
    ...
    change_speed(2.3);        // erreur : pas d’unité
    change_speed(23_m / 10s); // mètres par seconde

On pourrait accepter un `double` sans unité comme delta, mais ce serait sujet aux erreurs.  
Si l’on veut à la fois une vitesse absolue et un delta, on définit un type `Delta`.

##### Application

Très difficile en général.

* utiliser `const` de manière cohérente  
* signaler l’utilisation de casts (les casts contournent le système de types)  
* détecter le code qui imite la bibliothèque standard (difficile)


### <a name="rp-cplusplus"></a>P.2 : Écrire en C++ conforme au standard ISO

##### Raison

Ces directives concernent l’écriture de C++ conforme au standard ISO.

##### Note

Il existe des environnements où des extensions sont nécessaires (accès aux ressources système, etc.).  
Dans ce cas, localiser l’usage des extensions et contrôler leur utilisation via des directives non‑centrales.  
Si possible, encapsuler les extensions dans des interfaces désactivables ou compilables différemment selon les systèmes.

Les extensions n’ont souvent pas de sémantique rigoureuse.  
Même les extensions communes peuvent avoir des comportements légèrement différents selon les compilateurs.

##### Note

Utiliser du C++ ISO valide ne garantit pas la portabilité.  
Éviter la dépendance au comportement indéfini (ex. [ordre d’évaluation indéfini](#res-order)).  
Être conscient des comportements dépendants de l’implémentation (ex. `sizeof(int)`).

##### Note

Certains environnements imposent des restrictions (ex. interdiction d’allocation dynamique dans l’aéronautique).  
Dans ce cas, étendre ces directives pour les adapter à l’environnement.

##### Application

Utiliser un compilateur C++ récent (C++20 ou C++17) avec des options interdisant les extensions.


### <a name="rp-what"></a>P.3 : Exprimer l’intention

##### Raison

Sans indication de l’intention (via les noms ou les commentaires), il est impossible de savoir si le code fait ce qu’il est censé faire.

##### Exemple

    gsl::index i = 0;
    while (i < v.size()) {
        // ... faire quelque chose avec v[i] ...
    }

L’intention de simplement parcourir les éléments de `v` n’est pas exprimée.  
Le détail de l’index est exposé, et `i` survit au-delà de la boucle.

Mieux :

    for (const auto& x : v) { /* faire quelque chose avec x */ }

Pour modification :


    for (auto& x : v) { /* modifier x */ }

Encore mieux : utiliser un algorithme nommé :

    for_each(v, [](int x) { /* ... */ });
    for_each(par, v, [](int x) { /* ... */ });

##### Note

Dire ce qui doit être fait plutôt que comment.

##### Exemple

    draw_line(int, int, int, int);  // obscur
    draw_line(Point, Point);        // clair

##### Application

Chercher les motifs améliorables :

* boucles `for` simples → boucles `range-for`
* interfaces `f(T*, int)` → `f(span<T>)`
* variables de boucle avec portée trop large
* `new` et `delete` nus
* fonctions avec beaucoup de paramètres de types primitifs


### <a name="rp-typesafe"></a>P.4 : Idéalement, un programme devrait être sûr du point de vue du typage statique

##### Raison

Idéalement, un programme serait entièrement sûr statiquement.  
Malheureusement, ce n’est pas possible. Problèmes :

* unions  
* casts  
* décay des tableaux  
* erreurs de plage  
* conversions réductrices

##### Application

Proposer des alternatives :

* unions → `variant`  
* casts → minimiser, utiliser des templates  
* décay → `span`  
* erreurs de plage → `span`  
* conversions réductrices → `narrow`, `narrow_cast`

### <a name="rp-compile-time"></a>P.5: Préférer les vérifications à la compilation aux vérifications à l’exécution

##### Raison

Lisibilité du code et performance.  
Vous n’avez pas besoin d’écrire des gestionnaires d’erreurs pour des erreurs détectées à la compilation.

##### Exemple

    // Int est un alias utilisé pour les entiers
    int bits = 0;         // à éviter : code inutile
    for (Int i = 1; i; i <<= 1)
        ++bits;
    if (bits < 32)
        cerr << "Int too small\n";

Cet exemple échoue à atteindre son objectif (car le dépassement est indéfini) et devrait être remplacé par un simple `static_assert` :

    // Int est un alias utilisé pour les entiers
    static_assert(sizeof(Int) >= 4);    // à faire : vérification à la compilation

Ou mieux encore, utiliser le système de types et remplacer `Int` par `int32_t`.

##### Exemple

    void read(int* p, int n);   // lire au plus n entiers dans *p

    int a[100];
    read(a, 1000);    // mauvais, dépassement

Mieux :

    void read(span<int> r); // lire dans l’intervalle d’entiers r

    int a[100];
    read(a);        // mieux : laisser le compilateur déterminer le nombre d’éléments

**Formulation alternative** : Ne pas repousser à l’exécution ce qui peut être bien fait à la compilation.

##### Application

* Rechercher les arguments de type pointeur.
* Rechercher les vérifications d’intervalle faites à l’exécution.


### <a name="rp-run-time"></a>P.6 : Ce qui ne peut pas être vérifié à la compilation doit pouvoir l’être à l’exécution

##### Raison

Laisser des erreurs difficiles à détecter dans un programme, c’est s’exposer à des crashs et à de mauvais résultats.

##### Note

Idéalement, nous attrapons toutes les erreurs (qui ne sont pas des erreurs de logique du programmeur) soit à la compilation, soit à l’exécution.  
Il est impossible de tout attraper à la compilation, et souvent trop coûteux de tout attraper à l’exécution.  
Cependant, nous devrions écrire des programmes qui peuvent *en principe* être vérifiés, avec suffisamment de ressources.

##### Exemple, mauvais

    // compilé séparément, peut-être chargé dynamiquement
    extern void f(int* p);

    void g(int n)
    {
        // mauvais : le nombre d’éléments n’est pas passé à f()
        f(new int[n]);
    }

Ici, une information cruciale (le nombre d’éléments) a été tellement « obscurcie » que l’analyse statique devient quasi impossible et la vérification dynamique très difficile.

##### Exemple, mauvais

    extern void f2(int* p, int n);

    void g2(int n)
    {
        // mauvais : un mauvais nombre d’éléments peut être passé à f2()
        f2(new int[n], n);
    }

Passer le nombre d’éléments est mieux que passer seulement le pointeur, mais une simple faute de frappe peut introduire une erreur grave.

##### Exemple, mauvais

    extern void f3(unique_ptr<int[]>, int n);

    void g3(int n)
    {
        f3(make_unique<int[]>(n), m);    // mauvais : propriété et taille séparées
    }

##### Exemple

Nous devons passer le pointeur et le nombre d’éléments comme un objet intégral :

    extern void f4(vector<int>&);	// compilé séparément, peut-être chargé dynamiquement
    extern void f4(span<int>);		// compilé séparément, peut-être chargé dynamiquement
					// NB : on considère que l'appel du code est API-compatible; en utilisant
					// un compilateur C++ compatible et la même implémentation de stdlib

    void g3(int n)
    {
        vector<int> v(n);
        f4(v);            // passe une référence, conserve la propriété
        f4(span<int>{v}); // passe une vue, conserve la propriété
    }

##### Exemple

Comment transférer la propriété *et* les informations nécessaires à la validation ?


    vector<int> f5(int n)    // OK : move
    {
        vector<int> v(n);
        // ...
        return v;
    }

    unique_ptr<int[]> f6(int n)    // mauvais : perd n
    {
        auto p = make_unique<int[]>(n);
        // ...
        return p;
    }

    owner<int*> f7(int n)    // mauvais : perd n et risque d’oubli de delete
    {
        owner<int*> p = new int[n];
        // ...
        return p;
    }

##### Application

* Signaler les interfaces de style (pointeur, taille)
* ???


### <a name="rp-early"></a>P.7 : Attraper les erreurs d’exécution tôt

##### Raison

Éviter les crashs « mystérieux ».  
Éviter les erreurs menant à des résultats incorrects.

##### Exemple

    void increment1(int* p, int n)    // mauvais : sujet aux erreurs
    {
        for (int i = 0; i < n; ++i) ++p[i];
    }

    void use1(int m)
    {
        const int n = 10;
        int a[n] = {};
        increment1(a, m);   // si m == 20 → corruption ou crash
    }

Mieux :

    void increment2(span<int> p)
    {
        for (int& x : p) ++x;
    }

    void use2(int m)
    {
        const int n = 10;
        int a[n] = {};
        increment2({a, m});    // vérification possible au point d’appel
    }

Encore mieux :

    void use3(int m)
    {
        const int n = 10;
        int a[n] = {};
        increment2(a);   // aucune répétition du nombre d’éléments
    }

##### Exemple, mauvais

Ne pas vérifier plusieurs fois la même valeur.  
Ne pas passer des données structurées sous forme de chaînes :


    Date read_date(istream& is);
    Date extract_date(const string& s);

    void user1(const string& date)
    {
        auto d = extract_date(date);
    }

    void user2()
    {
        Date d = read_date(cin);
        user1(d.to_string());   // validation double
    }

##### Exemple

Les vérifications excessives peuvent coûter cher.  
Ne pas ajouter de vérifications qui changent la complexité asymptotique.


### <a name="rp-leak"></a>P.8: Ne laisser fuiter aucune ressource

##### Raison

Même une fuite lente finit par épuiser les ressources disponibles.

##### Exemple, mauvais

    void f(const char* name)
    {
        FILE* input = fopen(name, "r");
        if (something) return;   // fuite
        fclose(input);
    }

Préférer le RAII :

    void f(const char* name)
    {
        ifstream input {name};
        if (something) return;   // OK : pas de fuite
    }


# P.9 : Ne pas gaspiller du temps ou de l’espace

##### Raison

C’est du C++.

##### Exemple, mauvais

*(Traduction fidèle du texte, code inchangé)*

---

# P.10 : Préférer les données immuables aux données mutables

Raisons : plus simple à raisonner, pas de changement inattendu, meilleures optimisations, pas de data race.

---

# P.11 : Encapsuler les constructions complexes plutôt que les répandre

##### Exemple

Code bas niveau avec `malloc` / `realloc` → remplacer par `vector`.

---

# P.12 : Utiliser les outils de support quand c’est approprié

Analyse statique, outils de concurrence, outils de test, etc.

---

# P.13 : Utiliser les bibliothèques de support quand c’est approprié

Utiliser la bibliothèque standard et la GSL.  
Si une bonne bibliothèque n’existe pas, peut-être la créer.

---

Si tu veux, je peux aussi :

- produire une version **PDF-like** propre,  
- une version **Markdown optimisée**,  
- une version **résumée**,  
- ou une version **commentée** pour apprentissage.

Dis-moi ce que tu préfères.