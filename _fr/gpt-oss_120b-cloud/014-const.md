# <a name="s-const"></a>Con : Constantes et immutabilité

Vous ne pouvez pas rencontrer de condition de concurrence sur une constante.  
Il est plus facile de raisonner sur un programme lorsque de nombreux objets ne peuvent pas changer de valeur.  
Les interfaces qui promettent « aucun changement » des objets passés en argument améliorent grandement la lisibilité.

Résumé des règles de constance :

* [Con.1 : Par défaut, rendre les objets immuables](014-const.md#rconst-immutable)
* [Con.2 : Par défaut, rendre les fonctions membres `const`](014-const.md#rconst-fct)
* [Con.3 : Par défaut, passer les pointeurs et références vers des `const`](014-const.md#rconst-ref)
* [Con.4 : Utiliser `const` pour définir les objets dont les valeurs ne changent pas après construction](014-const.md#rconst-const)
* [Con.5 : Utiliser `constexpr` pour les valeurs pouvant être calculées à la compilation](014-const.md#rconst-constexpr)

### <a name="rconst-immutable"></a>Con.1 : Par défaut, rendre les objets immuables

##### Raison

Les objets immuables sont plus faciles à raisonner, ainsi on ne rend les objets non‑`const` que lorsqu’il est nécessaire de modifier leur valeur.  
Évite les modifications accidentelles ou difficiles à repérer.

##### Exemple

    for (const int i : c) cout << i << '\n';    // lecture uniquement : const

    for (int i : c) cout << i << '\n';          // MAUVAIS : lecture uniquement

##### Exceptions

Une variable locale retournée par valeur et dont le déplacement (move) est moins coûteux que la copie ne doit pas être déclarée `const` car cela peut imposer une copie inutile.

    std::vector<int> f(int i)
    {
        std::vector<int> v{ i, i, i };  // const inutile
        return v;
    }

Les paramètres de fonction passés par valeur sont rarement mutés, mais ils sont également rarement déclarés `const`. Pour éviter la confusion et de nombreux faux‑positifs, ne forcez pas cette règle pour les paramètres de fonction.

    void g(const int i) { ... }  // pédant

Notez qu’un paramètre de fonction est une variable locale, ainsi les modifications qui l’affectent sont locales.

##### Application

* Signaler les variables non‑`const` qui ne sont pas modifiées (à l’exception des paramètres afin d’éviter de nombreux faux‑positifs et des variables locales retournées).

### <a name="rconst-fct"></a>Con.2 : Par défaut, rendre les fonctions membres `const`

##### Raison

Une fonction membre doit être marquée `const` à moins qu’elle ne modifie l’état observable de l’objet. Cela donne une déclaration plus précise de l’intention de conception, améliore la lisibilité, permet au compilateur de détecter davantage d’erreurs, et parfois d’offrir plus d’opportunités d’optimisation.

##### Exemple, mauvais

    class Point {
        int x, y;
    public:
        int getx() { return x; }    // MAUVAIS, devrait être const car ne modifie pas l’état de l’objet
        // ...
    };

    void f(const Point& pt)
    {
        int x = pt.getx();          // ERREUR, ne compile pas car getx n’est pas marqué const
    }

##### Remarque

Il n’est pas intrinsèquement mauvais de passer un pointeur ou une référence non‑`const`, mais cela ne doit être fait que lorsque la fonction appelée est censée modifier l’objet. Un lecteur du code doit supposer qu’une fonction qui prend un `T*` ou `T&` « simple » modifie l’objet référencé. Si ce n’est pas le cas actuellement, cela pourrait le devenir plus tard sans nécessiter de recompilation.

##### Remarque

Certaines bibliothèques offrent des fonctions déclarant un `T*` même si ces fonctions ne modifient pas ce `T`. Cela pose problème aux personnes modernisant le code. Vous pouvez

* mettre à jour la bibliothèque pour qu’elle soit correcte `const` ; solution à long terme préférée  
* « caster away `const` » ; [à éviter de préférence](010-expr.md#res-casts-const)  
* fournir une fonction d’enveloppe  

Exemple :

    void f(int* p);   // ancien code : f() ne modifie pas `*p`
    void f(const int* p) { f(const_cast<int*>(p)); } // fonction d’enveloppe

Notez que cette solution d’enveloppe est un correctif qui ne doit être utilisé que lorsque la déclaration de `f()` ne peut pas être modifiée, par ex. parce qu’elle se trouve dans une bibliothèque que vous ne pouvez pas modifier.

##### Remarque

Une fonction membre `const` peut modifier la valeur d’un objet qui est `mutable` ou accessible via un membre pointeur. Une utilisation courante consiste à maintenir un cache plutôt que de recalculer une opération coûteuse à chaque appel. Par exemple, voici une classe `Date` qui met en cache (mémoïse) sa représentation sous forme de chaîne afin de simplifier les utilisations répétées :

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
        void compute_string_rep() const;    // calcule la représentation chaîne et la place dans string_val
        mutable string string_val;
        // ...
    };

Dire cela autrement, la constance n’est pas transitive. Il est possible pour une fonction membre `const` de changer la valeur des membres `mutable` et la valeur d’objets accessibles via des pointeurs non‑`const`. C’est au soin de la classe de garantir que de telles mutations ne se produisent que lorsqu’elles ont du sens selon la sémantique (invariants) qu’elle propose à ses utilisateurs.

**Voir aussi** : [Pimpl](005-interfaces.md#ri-pimpl)

##### Application

* Signaler une fonction membre qui n’est pas marquée `const` alors qu’elle n’effectue aucune opération non‑`const` sur un membre de données.

### <a name="rconst-ref"></a>Con.3 : Par défaut, passer les pointeurs et références vers des `const`

##### Raison

Pour éviter qu’une fonction appelée ne modifie de façon inattendue la valeur. Il est beaucoup plus facile de raisonner sur les programmes lorsque les fonctions appelées ne modifient pas l’état.

##### Exemple

    void f(char* p);        // f modifie-t-il *p ? (on suppose que oui)
    void g(const char* p);  // g ne modifie pas *p

##### Remarque

Il n’est pas intrinsèquement mauvais de passer un pointeur ou une référence non‑`const`, mais cela ne doit être fait que lorsque la fonction appelée est censée modifier l’objet.

##### Remarque

[Ne pas enlever le `const`](010-expr.md#res-casts-const).

##### Application

* Signaler une fonction qui ne modifie pas un objet passé par pointeur ou référence non‑`const`.  
* Signaler une fonction qui (en utilisant un cast) modifie un objet passé par pointeur ou référence `const`.

### <a name="rconst-const"></a>Con.4 : Utiliser `const` pour définir les objets dont les valeurs ne changent pas après construction

##### Raison

Éviter les surprises d’une valeur d’objet changée de façon inattendue.

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

Comme `x` n’est pas `const`, nous devons supposer qu’il est modifié quelque part dans la boucle.

##### Application

* Signaler les variables non‑`const` qui ne sont pas modifiées.

### <a name="rconst-constexpr"></a>Con.5 : Utiliser `constexpr` pour les valeurs pouvant être calculées à la compilation

##### Raison

Meilleures performances, meilleure vérification à la compilation, évaluation garantie à la compilation, aucune possibilité de conditions de concurrence.

##### Exemple

    double x = f(2);            // évaluation possible à l’exécution
    const double y = f(2);      // évaluation possible à l’exécution
    constexpr double z = f(2);  // erreur à moins que f(2) puisse être évalué à la compilation

##### Remarque

Voir F.4. @TODO-LINK

##### Application

* Signaler les définitions `const` qui ont des initialiseurs d’expression constante.