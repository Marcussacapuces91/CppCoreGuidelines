# <a name="s-const"></a>Con: Constantes et immutabilité

Vous ne pouvez pas être confronté à une condition de course sur une constante.  
Il est plus facile de raisonner sur un programme lorsque de nombreux objets ne peuvent pas changer leurs valeurs.  
Les interfaces qui promettent **« pas de changement »** des objets passés en arguments augmentent considérablement la lisibilité.

## Résumé des règles concernant les constantes :

* [Con.1 : Par défaut, rendre les objets immuables](#rconst-immutable)
* [Con.2 : Par défaut, rendre les fonctions membres `const`](#rconst-fct)
* [Con.3 : Par défaut, passer des pointeurs et références vers des `const`](#rconst-ref)
* [Con.4 : Utiliser `const` pour définir des objets dont la valeur ne change pas après construction](#rconst-const)
* [Con.5 : Utiliser `constexpr` pour les valeurs pouvant être calculées à la compilation](#rconst-constexpr)

### <a name="rconst-immutable"></a>Con.1 : Par défaut, rendre les objets immuables

##### Motif

Les objets immuables sont plus faciles à raisonner, il vaut donc mieux ne rendre les objets non‑`const` que lorsqu'il est nécessaire de modifier leur valeur.  
Empêche les modifications accidentelles ou difficiles à remarquer.

##### Exemple

    for (const int i : c) cout << i << '\n';    // lecture seule : const
    for (int i : c) cout << i << '\n';          // ERREUR : lecture seule

##### Exceptions

Une variable locale retournée par valeur et plus économique à déplacer qu’une copie ne doit pas être déclarée `const` car cela pourrait forcer une copie inutile.

    std::vector<int> f(int i)
    {
        std::vector<int> v{ i, i, i };  // const non nécessaire
        return v;
    }

Les paramètres de fonction passés par valeur sont rarement modifiés, mais également rarement déclarés `const`.  
Pour éviter toute confusion et un grand nombre de faux positifs, n'appliquez pas cette règle aux paramètres de fonction.

    void g(const int i) { ... }  // pédant

Remarque : un paramètre de fonction est une variable locale, donc les modifications apportées à celui‑ci sont locales.

##### Application

* Identifier les variables non‑`const` qui ne sont pas modifiées (sauf pour les paramètres afin d’éviter de nombreux faux positifs et les variables locales retournées).

---

### <a name="rconst-fct"></a>Con.2 : Par défaut, rendre les fonctions membres `const`

##### Motif

Une fonction membre doit être marquée `const` sauf si elle modifie l’état observable de l’objet.  
Cela donne une déclaration plus précise de l’intention de conception, une meilleure lisibilité, plus d’erreurs détectées par le compilateur et parfois plus d’opportunités d’optimisation.

##### Exemple, incorrect

    class Point {
        int x, y;
    public:
        int getx() { return x; }    // ERREUR : devrait être const car elle ne modifie pas l'état de l'objet
        // ...
    };

    void f(const Point& pt)
    {
        int x = pt.getx();          // ERREUR : ne compile pas parce que getx n'était pas marquée const
    }

##### Remarque

Il n'est pas intrinsèquement mauvais de passer un pointeur ou une référence à non‑`const`, mais cela ne doit être fait que lorsque la fonction appelée est censée modifier l’objet.  
Un lecteur de code doit supposer qu’une fonction qui prend un `T*` ou `T&` « normal » va modifier l’objet référencé.  
S'il ne le fait pas maintenant, il pourrait le faire plus tard sans forcer une recompilation.

##### Remarque

Il existe du code / des bibliothèques qui proposent des fonctions qui déclarent un `T*` même si ces fonctions ne modifient pas ce `T`.  
Ceci pose un problème pour les personnes qui modernisent le code.  
Vous pouvez

* mettre à jour la bibliothèque pour qu'elle soit `const`‑correcte ; solution à long terme préférée
* "cast away `const`" ; [évité de préférence](#res-casts-const) @TODO-LINK
* fournir une fonction wrapper

Exemple :

    void f(int* p);   // code ancien : f() ne modifie pas `*p`
    void f(const int* p) { f(const_cast<int*>(p)); } // wrapper

Notez que cette solution wrapper est un correctif qui ne doit être utilisé que lorsque la déclaration de `f()` ne peut pas être modifiée, par exemple parce qu’elle se trouve dans une bibliothèque que vous ne pouvez pas modifier.

##### Remarque

Une fonction membre `const` peut modifier la valeur d’un objet `mutable` ou accédé via un membre pointeur.  
Une utilisation courante consiste à maintenir un cache plutôt que de recalculer à chaque fois.  
Par exemple, voici un `Date` qui mémorise sa représentation sous forme de chaîne pour simplifier les utilisations répétées :

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
        void compute_string_rep() const;    // calculer la représentation en chaîne et la placer dans string_val
        mutable string string_val;
        // ...
    };

Une autre façon de le dire est que la constance n’est pas transitive.  
Il est possible qu’une fonction membre `const` modifie la valeur des membres `mutable` ainsi que la valeur d’objets accédés via des pointeurs non‑`const`.  
C’est le rôle de la classe d’assurer que cette mutation se produit uniquement lorsqu’elle a du sens selon les sémantiques (invariants) qu’elle offre à ses utilisateurs.

**Voir également** : [Pimpl](#ri-pimpl) @TODO-LINK

##### Application

* Identifier une fonction membre qui n’est pas marquée `const` mais qui ne réalise pas d’opération non‑`const` sur un membre de données.

---

### <a name="rconst-ref"></a>Con.3 : Par défaut, passer des pointeurs et références vers des `const`

##### Motif

Éviter qu’une fonction appelée modifie de façon inattendue la valeur.  
Il est beaucoup plus facile de raisonner sur les programmes lorsque les fonctions appelées ne modifient pas l’état.

##### Exemple

    void f(char* p);        // f modifie‑t‑il *p ? (supposez qu’il le fasse)
    void g(const char* p);  // g ne modifie pas *p

##### Remarque

Il n'est pas intrinsèquement mauvais de passer un pointeur ou une référence à non‑`const`, mais cela ne doit être fait que lorsque la fonction appelée est censée modifier l'objet.

##### Remarque

[Ne pas enlever le 'const'](#res-casts-const) @TODO-LINK

##### Application

* Identifier une fonction qui ne modifie pas un objet passé par pointeur ou référence à non‑`const`
* Identifier une fonction qui (en utilisant un cast) modifie un objet passé par pointeur ou référence à `const`

---

### <a name="rconst-const"></a>Con.4 : Utiliser `const` pour définir des objets dont les valeurs ne changent pas après construction

##### Motif

Empêche les surprises dues à des valeurs d'objet modifiées de façon inattendue.

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

* Identifier les variables non‑`const` qui ne sont pas modifiées.

---

### <a name="rconst-constexpr"></a>Con.5 : Utiliser `constexpr` pour les valeurs pouvant être calculées à la compilation

##### Motif

Meilleure performance, meilleure vérification à la compilation, évaluation garantie à la compilation, aucune possibilité de condition de course.

##### Exemple

    double x = f(2);            // évaluation possible à l'exécution
    const double y = f(2);      // évaluation possible à l'exécution
    constexpr double z = f(2);  // erreur à moins que f(2) puisse être évalué à la compilation

##### Remarque

Voir F.4.

##### Application

* Identifier les définitions `const` avec des initialiseurs d’expression constante.