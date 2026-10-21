# <a name="s-const"></a>Con : Constantes et immuabilité

On ne peut pas avoir de condition de course sur une constante.
Il est plus facile de raisonner sur un programme lorsque la plupart des objets ne peuvent pas changer de valeur.
Les interfaces qui promettent « aucun changement » des objets passés en argument augmentent considérablement la lisibilité.

Résumé des règles sur les constantes :

* [Con.1 : Par défaut, rendre les objets immuables](014-const.md#rconst-immutable)
* [Con.2 : Par défaut, rendre les fonctions membres `const`](014-const.md#rconst-fct)
* [Con.3 : Par défaut, passer des pointeurs et des références vers des `const`](014-const.md#rconst-ref)
* [Con.4 : Utiliser `const` pour définir des objets dont la valeur ne change pas après la construction](014-const.md#rconst-const)
* [Con.5 : Utiliser `constexpr` pour les valeurs qui peuvent être calculées au moment de la compilation](014-const.md#rconst-constexpr)

### <a name="rconst-immutable"></a>Con.1 : Par défaut, rendre les objets immuables

##### Justification

Les objets immuables sont plus faciles à comprendre. N'utilisez `const` que lorsque vous avez besoin de modifier la valeur d'un objet.
Cela prévient les modifications accidentelles ou difficiles à détecter.

##### Exemple

    for (const int i : c) cout << i << '\n';    // lecture seule : const

    for (int i : c) cout << i << '\n';          // MAUVAIS : lecture seule

##### Exceptions

Une variable locale qui est renvoyée par valeur et dont le déplacement est moins coûteux que la copie ne doit pas être déclarée `const`,
car cela pourrait forcer une copie inutile.

    std::vector<int> f(int i)
    {
        std::vector<int> v{ i, i, i };  // const inutile
        return v;
    }

Les paramètres de fonction passés par valeur sont rarement modifiés, mais aussi rarement déclarés `const`.
Pour éviter les confusions et un grand nombre de faux positifs, n'imposez pas cette règle pour les paramètres de fonction.

    void g(const int i) { ... }  // trop pointilleux

Notez qu'un paramètre de fonction est une variable locale, donc toute modification qui y est apportée est locale.

##### Application

* Signaler les variables non-`const` qui ne sont pas modifiées (à l'exception des paramètres de fonction pour éviter les faux positifs
et des variables locales renvoyées)

### <a name="rconst-fct"></a>Con.2 : Par défaut, rendre les fonctions membres `const`

##### Justification

Une fonction membre doit être marquée `const` sauf si elle modifie l'état observable de l'objet.
Cela permet d'exprimer plus précisément l'intention de conception, d'améliorer la lisibilité, de détecter davantage d'erreurs au moment de la compilation, et parfois d'offrir davantage d'opportunités d'optimisation.

##### Exemple, mauvais

    class Point {
        int x, y;
    public:
        int getx() { return x; }    // MAUVAIS, devrait être const car il ne modifie pas l'état de l'objet
        // ...
    };

    void f(const Point& pt)
    {
        int x = pt.getx();          // ERREUR, ne compile pas car getx n'est pas marqué const
    }

##### Remarque

Il n'est pas intrinsèquement mauvais de passer un pointeur ou une référence vers un objet non-`const`,
mais cela ne doit se faire que lorsque la fonction appelée est censée modifier l'objet.
Un lecteur de code doit supposer qu'une fonction qui prend un `T*` ou un `T&` « simple » va modifier l'objet référencé.
Si ce n'est pas le cas actuellement, cela pourrait l'être plus tard sans forcer de recompilation.

##### Remarque

Il existe des bibliothèques qui proposent des fonctions déclarant un `T*` alors même
que ces fonctions ne modifient pas ce `T`.
C'est un problème pour ceux qui modernisent du code.
Vous pouvez :

* mettre à jour la bibliothèque pour qu'elle soit `const`-correcte ; solution préférable à long terme
* « retirer le `const` » ; [à éviter autant que possible](010-expr.md#res-casts-const)
* fournir une fonction enveloppe

Exemple :

    void f(int* p);   // ancien code : f() ne modifie pas `*p`
    void f(const int* p) { f(const_cast<int*>(p)); } // enveloppe

Notez que cette solution par enveloppe est un correctif qui ne doit être utilisé que lorsque la déclaration de `f()` ne peut pas être modifiée,
par exemple parce qu'elle se trouve dans une bibliothèque que vous ne pouvez pas modifier.

##### Remarque

Une fonction membre `const` peut modifier la valeur d'un objet `mutable` ou accessible via un membre pointeur.
Un usage courant consiste à maintenir un cache plutôt que de répéter un calcul complexe.
Par exemple, voici une classe `Date` qui met en cache (mémoise) sa représentation en chaîne pour simplifier les utilisations répétées :

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
        void compute_string_rep() const;    // calcule la représentation en chaîne et la place dans string_val
        mutable string string_val;
        // ...
    };

Autrement dit, la `const`-ité n'est pas transitive.
Il est possible qu'une fonction membre `const` modifie la valeur de membres `mutable` et la valeur d'objets accessibles
via des pointeurs non-`const`.
Il incombe à la classe de s'assurer que cette mutation n'est effectuée que lorsque cela a un sens selon la sémantique (les invariants)
qu'elle offre à ses utilisateurs.

**Voir aussi** : [Pimpl](005-interfaces.md#ri-pimpl)

##### Application

* Signaler une fonction membre qui n'est pas marquée `const` mais qui n'effectue aucune opération non-`const` sur un membre de données.

### <a name="rconst-ref"></a>Con.3 : Par défaut, passer des pointeurs et des références vers des `const`

##### Justification

Pour éviter qu'une fonction appelée ne modifie inopinément la valeur d'un objet.
Il est bien plus facile de raisonner sur un programme lorsque les fonctions appelées ne modifient pas l'état.

##### Exemple

    void f(char* p);        // f modifie-t-il *p ? (on suppose que oui)
    void g(const char* p);  // g ne modifie pas *p

##### Remarque

Il n'est pas intrinsèquement mauvais de passer un pointeur ou une référence vers un objet non-`const`,
mais cela ne doit se faire que lorsque la fonction appelée est censée modifier l'objet.

##### Remarque

[Ne pas retirer le `const`](010-expr.md#res-casts-const).

##### Application

* Signaler une fonction qui ne modifie pas un objet passé par pointeur ou par référence vers un non-`const`
* Signaler une fonction qui (en utilisant un cast) modifie un objet passé par pointeur ou par référence vers un `const`

### <a name="rconst-const"></a>Con.4 : Utiliser `const` pour définir des objets dont la valeur ne change pas après la construction

##### Justification

Pour éviter les surprises dues à des modifications inattendues de la valeur d'un objet.

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

Comme `x` n'est pas `const`, nous devons supposer qu'il est modifié quelque part dans la boucle.

##### Application

* Signaler les variables non-`const` non modifiées.

### <a name="rconst-constexpr"></a>Con.5 : Utiliser `constexpr` pour les valeurs qui peuvent être calculées au moment de la compilation

##### Justification

Meilleures performances, meilleure vérification au moment de la compilation, évaluation garantie au moment de la compilation, aucune possibilité de condition de course.

##### Exemple

    double x = f(2);            // évaluation possible au moment de l'exécution
    const double y = f(2);      // évaluation possible au moment de l'exécution
    constexpr double z = f(2);  // erreur sauf si f(2) peut être évalué au moment de la compilation

##### Remarque

Voir F.4.

##### Application

* Signaler les définitions `const` avec des initialiseurs qui sont des expressions constantes.
