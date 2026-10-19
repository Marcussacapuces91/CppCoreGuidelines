# <a name="s-const"></a>Con: Constantes et immutabilité

Vous ne pouvez pas rencontrer une condition de concurrence sur une constante.  
Il est plus facile de raisonner sur un programme lorsque de nombreux objets ne peuvent pas changer leurs valeurs.  
Les interfaces qui promettent « aucun changement » des objets passés en paramètres augmentent considérablement la lisibilité.

Résumé des règles de constante :

* [Con.1: Par défaut, rendre les objets immuables](014-const.md#rconst-immutable)
* [Con.2: Par défaut, rendre les fonctions membres `const`](014-const.md#rconst-fct)
* [Con.3: Par défaut, passer des pointeurs et références vers des `const`s](014-const.md#rconst-ref)
* [Con.4: Utiliser `const` pour définir des objets dont les valeurs ne changent pas après construction](014-const.md#rconst-const)
* [Con.5: Utiliser `constexpr` pour les valeurs pouvant être calculées à la compilation](014-const.md#rconst-constexpr)

### <a name="rconst-immutable"></a>Con.1: Par défaut, rendre les objets immuables

##### Raison

Les objets immuables sont plus faciles à raisonner, donc on ne les rend pas `non const` que lorsqu'il est nécessaire de modifier leur valeur.  
Cela évite les changements accidentels ou difficiles à repérer.

##### Exemple

    for (const int i : c) cout << i << '\n';    // lecture seule : const

    for (int i : c) cout << i << '\n';          // MAUVAISE : lecture seule

##### Exceptions

Une variable locale renvoyée par valeur et dont le déplacement est plus léger que la copie ne devrait pas être déclarée `const` car cela peut forcer une copie inutile.

    std::vector<int> f(int i)
    {
        std::vector<int> v{ i, i, i };  // const pas nécessaire
        return v;
    }

Les paramètres de fonction passés par valeur sont rarement modifiés, mais également rarement déclarés `const`.  
Pour éviter toute confusion et de nombreux faux positifs, il ne faut pas appliquer cette règle aux paramètres de fonction.

    void g(const int i) { ... }  // pedantic

Notez qu'un paramètre de fonction est une variable locale, donc les modifications apportées à celui‑ci restent locales.

##### Mise en œuvre

* Marquer les variables non-`const` qui ne sont pas modifiées (à l'exception des paramètres pour éviter de nombreux faux positifs et des variables locales retournées).

### <a name="rconst-fct"></a>Con.2: Par défaut, rendre les fonctions membres `const`

##### Raison

Une fonction membre doit être marquée `const` sauf si elle modifie l'état observable de l'objet.  
Cela donne une déclaration d'intention de conception plus précise, une meilleure lisibilité, détecte plus d'erreurs par le compilateur et offre parfois de meilleures opportunités d'optimisation.

##### Exemple, mauvaise

    class Point {
        int x, y;
    public:
        int getx() { return x; }    // MAUVAISE, devrait être const car il ne modifie pas l'état de l'objet
        // ...
    };

    void f(const Point& pt)
    {
        int x = pt.getx();          // ERREUR, ne compile pas car getx n'est pas marqué const
    }

##### Note

Il n'est pas intrinsèquement mauvais de passer un pointeur ou une référence à non-`const`, mais cela ne doit être fait qu'en l'occurrence où la fonction appelée est censée modifier l'objet.  
Un lecteur de code doit supposer qu'une fonction qui prend un `T*` ou `T&` « simple » modifiera l'objet référencé.  
S'il ne le fait pas maintenant, il pourra bien le faire plus tard sans forcer une recompilation.

##### Note

Il existe des codes/bibliothèques qui offrent des fonctions déclarant un `T*` bien que celles‑ci ne modifient pas ce `T`. C'est un problème pour les personnes qui modernisent du code. Vous pouvez

* mettre à jour la bibliothèque pour qu'elle respecte `const`-correct ; solution préférée à long terme
* "éliminer le const"; [à éviter](010-expr.md#res-casts-const) @TODO-LINK
* fournir une fonction enveloppe

Exemple :

    void f(int* p);   // ancien code : f() ne modifie pas `*p`
    void f(const int* p) { f(const_cast<int*>(p)); } // enveloppe

##### Note

Une fonction membre `const` peut modifier la valeur d'un objet `mutable` ou accédé via un membre pointeur.  
Un usage courant est de maintenir un cache plutôt que de répéter un calcul compliqué.  
Par exemple, voici une `Date` qui met en cache (mémoïsation) sa représentation sous forme de chaîne pour simplifier sa réutilisation :

    class Date {
    public:
        // ...
        const string& string_ref() const
        {
            if (string_val == "") compute_string_rep();
            return string_val;
        }
        // ...
    private:
        void compute_string_rep() const;    // calculer la représentation sous forme de chaîne et la placer dans string_val
        mutable string string_val;
        // ...
    };

Une autre façon de dire cela est que l'immutabilité n'est pas transitive.  
Il est possible qu'une fonction membre `const` modifie la valeur des membres `mutable` et la valeur des objets accessibles via des pointeurs non-`const`.  
C'est la responsabilité de la classe de s'assurer que cette mutation ne se produit qu'à des moments appropriés, conformément aux invariants qu'elle expose à ses utilisateurs.

**Voir aussi** : [Pimpl](005-interfaces.md#ri-pimpl) @TODO-LINK

##### Mise en œuvre

* Marquer une fonction membre qui n'est pas déclarée `const` mais qui n'effectue aucune opération non-`const` sur aucun membre de données.

### <a name="rconst-ref"></a>Con.3: Par défaut, passer des pointeurs et références vers des `const`s

##### Raison

Éviter qu'une fonction appelée modifie de façon inattendue la valeur.  
Il est beaucoup plus facile de raisonner sur un programme lorsque les fonctions appelées ne modifient pas l'état.

##### Exemple

    void f(char* p);        // f modifie *p ? (supposons qu'il le fasse)
    void g(const char* p);  // g ne modifie pas *p

##### Note

Il n'est pas intrinsèquement mauvais de passer un pointeur ou une référence à non-`const`, mais cela ne doit être fait qu'en l'occurrence où la fonction appelée est censée modifier l'objet.

##### Note

[Ne pas abandonner const](010-expr.md#res-casts-const) @TODO-LINK

##### Mise en œuvre

* Marquer une fonction qui ne modifie pas un objet passé par pointeur ou référence à non-`const`
* Marquer une fonction qui, en utilisant un cast, modifie un objet passé par pointeur ou référence à `const`

### <a name="rconst-const"></a>Con.4: Utiliser `const` pour définir des objets dont les valeurs ne changent pas après construction

##### Raison

Prévenir les surprises dues à des valeurs d'objet modifiées accidentellement.

##### Exemple

    void f()
    {
        int x = 7;
        const int y = 9;

        for (;;) {
            // ...
        }
        // ...
    }

Puisque `x` n'est pas `const`, nous devons supposer qu'il est modifié quelque part dans la boucle.

##### Mise en œuvre

* Marquer les variables non-`const` inchangées.

### <a name="rconst-constexpr"></a>Con.5: Utiliser `constexpr` pour les valeurs pouvant être calculées à la compilation

##### Raison

Meilleure performance, meilleure vérification à la compilation, évaluation garantie à la compilation, aucune possibilité de conditions de concurrence.

##### Exemple

    double x = f(2);            // évaluation possible à l'exécution
    const double y = f(2);      // évaluation possible à l'exécution
    constexpr double z = f(2);  // erreur, à moins que f(2) ne puisse être évalué à la compilation

##### Note

Voir F.4.

##### Mise en œuvre

* Marquer les définitions `const` avec des initialiseurs d'expression constante.