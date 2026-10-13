# <a name="s-naming"></a>NL : Suggestions de nommage et de mise en page  

Le nommage et la mise en page cohérents sont utiles.  
Si ce n’est pour aucune autre raison, c’est parce que cela minimise les arguments du type « mon style est meilleur que le vôtre ».  
Cependant, il existe de nombreux styles différents et les gens y tiennent passionnément (pour et contre).  
De plus, la plupart des projets réels intègrent du code provenant de multiples sources ; il est donc souvent impossible d’unifier tout le code sous un seul style.  
Après de nombreuses demandes de directives de la part des utilisateurs, nous présentons un ensemble de règles que vous pouvez appliquer si vous n’avez pas de meilleures idées ; l’objectif principal étant la cohérence, plutôt qu’un jeu de règles particulier.  
Les IDE et les outils peuvent aider (ou gêner).

**Règles de nommage et de mise en page :**  

* [NL.1 : Ne pas dire dans les commentaires ce qui peut être clairement indiqué dans le code](024-naming.md#rl-comments) @TODO-LINK  
* [NL.2 : Indiquer l’intention dans les commentaires](024-naming.md#rl-comments-intent) @TODO-LINK  
* [NL.3 : Rester concis dans les commentaires](024-naming.md#rl-comments-crisp) @TODO-LINK  
* [NL.4 : Conserver un style d’indentation cohérent](024-naming.md#rl-indent) @TODO-LINK  
* [NL.5 : Éviter d’encoder des informations de type dans les noms](024-naming.md#rl-name-type) @TODO-LINK  
* [NL.7 : Faire en sorte que la longueur d’un nom soit à peu près proportionnelle à la portée du nom](024-naming.md#rl-name-length) @TODO-LINK  
* [NL.8 : Utiliser un style de nommage cohérent](024-naming.md#rl-name) @TODO-LINK  
* [NL.9 : Utiliser `ALL_CAPS` uniquement pour les noms de macros](024-naming.md#rl-all-caps) @TODO-LINK  
* [NL.10 : Privilégier les noms en `underscore_style`](024-naming.md#rl-camel) @TODO-LINK  
* [NL.11 : Rendre les littéraux lisibles](024-naming.md#rl-literals) @TODO-LINK  
* [NL.15 : Utiliser les espaces avec parcimonie](024-naming.md#rl-space) @TODO-LINK  
* [NL.16 : Utiliser un ordre de déclaration de membres de classe conventionnel](024-naming.md#rl-order) @TODO-LINK  
* [NL.17 : Utiliser une mise en page dérivée de K&R](024-naming.md#rl-knr) @TODO-LINK  
* [NL.18 : Utiliser la mise en page des déclarateurs de style C++](024-naming.md#rl-ptr) @TODO-LINK  
* [NL.19 : Éviter les noms facilement confus](024-naming.md#rl-misread) @TODO-LINK  
* [NL.20 : Ne pas placer deux instructions sur la même ligne](024-naming.md#rl-stmt) @TODO-LINK  
* [NL.21 : Déclarer un seul nom (uniquement) par déclaration](024-naming.md#rl-dcl) @TODO-LINK  
* [NL.25 : Ne pas utiliser `void` comme type d’argument](024-naming.md#rl-void) @TODO-LINK  
* [NL.26 : Utiliser la notation `const` conventionnelle](024-naming.md#rl-const) @TODO-LINK  
* [NL.27 : Utiliser l’extension `.cpp` pour les fichiers de code et `.h` pour les fichiers d’interface](024-naming.md#rl-file-suffix) @TODO-LINK  

La plupart de ces règles sont esthétiques et les programmeurs ont des opinions très tranchées.  
Les IDE ont également tendance à fournir des valeurs par défaut et une variété d’alternatives.  
Ces règles sont proposées comme valeurs par défaut à suivre, sauf si vous avez des raisons de les ignorer.

Nous avons reçu des commentaires indiquant que le nommage et la mise en page sont tellement personnels et/ou arbitraires que nous ne devrions pas essayer de les « légiférer ».  
Nous ne « légiférons » pas (voir le paragraphe précédent).  
Cependant, nous avons reçu de nombreuses demandes de conventions de nommage et de mise en page à appliquer lorsqu’il n’y a pas de contraintes externes.

Les règles plus spécifiques et détaillées sont plus faciles à appliquer.

Ces règles rappellent fortement les recommandations du **PPP Style Guide** (https://www.stroustrup.com/Programming/PPP‑style.pdf) rédigé à l’appui de *Programming : Principles and Practice using C++* de Stroustrup.

---

### <a name="rl-comments"></a>NL.1 : Ne pas dire dans les commentaires ce qui peut être clairement indiqué dans le code  

##### Raison  

Les compilateurs ne lisent pas les commentaires.  
Les commentaires sont moins précis que le code.  
Les commentaires ne sont pas mis à jour aussi régulièrement que le code.  

##### Exemple, mauvais  

    auto x = m * v1 + vv;   // multiplier m avec v1 et ajouter le résultat à vv  

##### Application  

Créer un programme d’IA qui interprète le texte anglais familier et vérifier si ce qui est dit pourrait être exprimé plus clairement en C++.  

---

### <a name="rl-comments-intent"></a>NL.2 : Indiquer l’intention dans les commentaires  

##### Raison  

Le code indique ce qui est fait, pas ce qui est censé être fait. Souvent, l’intention peut être exprimée plus clairement et de façon plus concise que l’implémentation.  

##### Exemple  

    void stable_sort(Sortable& c)
        // trier c dans l’ordre déterminé par <, conserver les éléments égaux (définis par ==) dans
        // leur ordre relatif original
    {
        // ... plusieurs lignes de code non trivial ...
    }  

##### Note  

Si le commentaire et le code sont en désaccord, il est probable que les deux soient erronés.  

---

### <a name="rl-comments-crisp"></a>NL.3 : Rester concis dans les commentaires  

##### Raison  

La verbosité ralentit la compréhension et rend le code plus difficile à lire en le dispersant dans le fichier source.  

##### Note  

Utilisez de l’anglais intelligible.  
Je peux être fluide en danois, mais la plupart des programmeurs ne le sont pas ; les mainteneurs de mon code ne le sont peut‑être pas non plus.  
Évitez le langage SMS et veillez à votre grammaire, ponctuation et capitalisation.  
Visez le professionnalisme, pas le « cool ».  

##### Application  

impossible.  

---

### <a name="rl-indent"></a>NL.4 : Conserver un style d’indentation cohérent  

##### Raison  

Lisibilité. Éviter les « erreurs stupides ».  

##### Exemple, mauvais  

    int i;
    for (i = 0; i < max; ++i); // bogue en attente de se produire
    if (i == j)
        return i;  

##### Note  

Il est généralement judicieux d’indenter toujours l’instruction qui suit `if (…)`, `for (…)` et `while (…)` :

    if (i < 0) error("negative argument");

    if (i < 0)
        error("negative argument");  

##### Application  

Utiliser un outil.  

---

### <a name="rl-name-type"></a>NL.5 : Éviter d’encoder des informations de type dans les noms  

##### Raison  

Si les noms reflètent les types plutôt que la fonctionnalité, il devient difficile de changer les types utilisés pour fournir cette fonctionnalité.  
De plus, si le type d’une variable est modifié, le code qui l’utilise devra être modifié.  
Minimiser les conversions involontaires.  

##### Exemple, mauvais  

    void print_int(int i);
    void print_string(const char*);

    print_int(1);          // répétitif, correspondance manuelle des types
    print_string("xyzzy"); // répétitif, correspondance manuelle des types  

##### Exemple, bon  

    void print(int i);
    void print(string_view);    // fonctionne également sur toute séquence de type chaîne

    print(1);              // clair, correspondance de type automatique
    print("xyzzy");        // clair, correspondance de type automatique  

##### Note  

Les noms contenant des informations de type sont soit verbeux, soit cryptiques.  

    printS  // imprimer un std::string
    prints  // imprimer une chaîne de style C
    printi  // imprimer un entier  

Exiger des techniques comme la notation hongroise pour encoder un type a été utilisé dans des langages non typés, mais cela est généralement inutile et même nuisible dans un langage fortement typé statiquement comme C++, parce que les annotations deviennent obsolètes (les défauts sont comme des commentaires et se détériorent tout comme eux) et elles interfèrent avec une bonne utilisation du langage (utiliser le même nom et la résolution de surcharge à la place).  

##### Note  

Certaines conventions utilisent des préfixes très généraux (non spécifiques au type) pour désigner l’usage général d’une variable.  

    auto p = new User();
    auto p = make_unique<User>();
    // note : « p » n’est pas utilisé pour dire « pointeur brut du type User »,
    //        mais simplement pour dire « il s’agit d’une indirection »

    auto cntHits = calc_total_of_hits(/*...*/);
    // note : « cnt » n’est pas utilisé pour encoder un type,
    //        mais simplement pour dire « il s’agit d’un décompte de quelque chose »  

Ce n’est pas nuisible et cela ne relève pas de cette directive parce qu’il n’encode pas d’informations de type.  

##### Note  

Certaines conventions distinguent les membres des variables locales, et/ou des variables globales.  

    struct S {
        int m_;
        S(int m) : m_{abs(m)} { }
    };  

Ce n’est pas nuisible et cela ne relève pas de cette directive parce qu’il n’encode pas d’informations de type.  

##### Note  

Comme C++, certains styles distinguent les types des non‑types. Par exemple, en capitalisant les noms de types, mais pas les noms de fonctions et de variables.  

    template<typename T>
    class HashTable {   // associe une chaîne à T
        // ...
    };

    HashTable<int> index;  

Ce n’est pas nuisible et cela ne relève pas de cette directive parce qu’il n’encode pas d’informations de type.  

---

### <a name="rl-name-length"></a>NL.7 : Faire en sorte que la longueur d’un nom soit à peu près proportionnelle à la portée du nom  

**Raison** : Plus la portée d’un nom est grande, plus il y a de risques de confusion et de collisions de noms involontaires.  

##### Exemple  

    double sqrt(double x);   // renvoie la racine carrée de x ; x doit être non négatif

    int length(const char* p);  // renvoie le nombre de caractères d’une chaîne C terminée par zéro

    int length_of_string(const char zero_terminated_array_of_char[])    // mauvais : verbeux

    int g;      // mauvais : variable globale avec un nom cryptique

    int open;   // mauvais : variable globale avec un nom court et populaire  

L’utilisation de `p` pour un pointeur et `x` pour une variable à virgule flottante est conventionnelle et non confuse dans une portée restreinte.  

##### Application  

???  

---

### <a name="rl-name"></a>NL.8 : Utiliser un style de nommage cohérent  

**Raison** : La cohérence du nommage et du style de nommage augmente la lisibilité.  

##### Note  

Il existe de nombreux styles et, lorsque vous utilisez plusieurs bibliothèques, vous ne pouvez pas suivre toutes leurs conventions différentes. Choisissez un « style maison », mais laissez les bibliothèques « importées » avec leur style d’origine.  

##### Exemple (ISO Standard)  

ISO Standard, n’utiliser que des minuscules et des chiffres, séparer les mots par des underscores :  

* `int`  
* `vector`  
* `my_map`  

Évitez les identificateurs contenant des doubles underscores `__` ou commençant par un underscore suivi d’une majuscule (par ex. : `_Throws`). De tels identificateurs sont réservés à l’implémentation C++.  

##### Exemple (Stroustrup)  

Stroustrup : ISO Standard, mais avec des majuscules utilisées pour vos propres types et concepts :  

* `int`  
* `vector`  
* `My_map`  

##### Exemple (CamelCase)  

CamelCase : capitaliser chaque mot d’un identificateur multi‑mots :  

* `int`  
* `vector`  
* `MyMap`  
* `myMap`  

Certaines conventions capitalisent la première lettre, d’autres non.  

##### Note  

Essayez d’être cohérent dans votre utilisation des acronymes et de la longueur des identificateurs :  

    int mtbf {12};
    int mean_time_between_failures {12}; // décidez vous  

##### Application  

Serait possible sauf pour les bibliothèques aux conventions variées.  

---

### <a name="rl-all-caps"></a>NL.9 : Utiliser `ALL_CAPS` uniquement pour les noms de macros  

##### Raison  

Éviter de confondre les macros avec des noms qui obéissent aux règles de portée et de type.  

##### Exemple  

    void f()
    {
        const int SIZE{1000};  // mauvais, utilisez « size » à la place
        int v[SIZE];
    }  

##### Note  

En particulier, cela évite de confondre les macros avec des constantes symboliques non‑macro (voir aussi [Enum.5 : Ne pas utiliser `ALL_CAPS` pour les énumérateurs](008-enum.md#renum-caps)) :  

    enum bad { BAD, WORSE, HORRIBLE }; // MAUVAIS  

##### Application  

* Signaler les macros contenant des lettres minuscules  
* Signaler les noms non‑macro en `ALL_CAPS`  

---

### <a name="rl-camel"></a>NL.10 : Privilégier les noms en `underscore_style`  

##### Raison  

L’utilisation d’underscores pour séparer les parties d’un nom est le style original du C et du C++ et est utilisé dans la bibliothèque standard C++.  

##### Note  

Cette règle constitue une valeur par défaut à appliquer uniquement si vous avez le choix. Souvent, vous n’avez pas le choix et devez suivre un style établi pour la **cohérence**. Le besoin de cohérence l’emporte sur les préférences personnelles.  

C’est une recommandation pour les cas où vous n’avez aucune contrainte ou meilleure idée (024‑naming.md). Cette règle a été ajoutée après de nombreuses demandes d’orientation.  

##### Exemple (Stroustrup)  

Stroustrup : ISO Standard, mais avec des majuscules utilisées pour vos propres types et concepts :  

* `int`  
* `vector`  
* `My_map`  

##### Application  

Impossible.  

---

### <a name="rl-literals"></a>NL.11 : Rendre les littéraux lisibles  

##### Raison  

Lisibilité.  

##### Exemple (séparateurs de chiffres)  

    auto c = 299'792'458; // m/s²
    auto q2 = 0b0000'1111'0000'0000;
    auto ss_number = 123'456'7890;  

##### Exemple (suffixes littéraux)  

    auto hello = "Hello!"s; // une std::string
    auto world = "world";   // une chaîne de style C
    auto interval = 100ms;  // utilisation de <chrono>  

##### Note  

Les littéraux ne doivent pas être éparpillés partout dans le code comme des « constantes magiques » (010‑expr.md#res‑magic), mais il reste conseillé de les rendre lisibles là où ils sont définis. Il est facile de faire une faute de frappe dans une longue chaîne de chiffres.  

##### Application  

Signaler les séquences de chiffres longues. La difficulté est de définir « long » ; on pourrait fixer la limite à 7.  

---

### <a name="rl-space"></a>NL.15 : Utiliser les espaces avec parcimonie  

##### Raison  

Trop d’espace augmente la taille du texte et distrait.  

##### Exemple, mauvais  

    #include < map >

    int main(int argc, char * argv [ ])
    {
        // ...
    }  

##### Exemple  

    #include <map>

    int main(int argc, char* argv[])
    {
        // ...
    }  

##### Note  

Certains IDE imposent leurs propres opinions et ajoutent des espaces distractifs.  

C’est une recommandation pour les cas où vous n’avez aucune contrainte ou meilleure idée (024‑naming.md). Cette règle a été ajoutée après de nombreuses demandes d’orientation.  

##### Note  

Nous apprécions les espaces bien placés comme aide significative à la lisibilité. Il suffit simplement de ne pas en abuser.  

---

### <a name="rl-order"></a>NL.16 : Utiliser un ordre de déclaration de membres de classe conventionnel  

##### Raison  

Un ordre conventionnel des membres améliore la lisibilité.  

Lors de la déclaration d’une classe, utilisez l’ordre suivant :  

* **types** : classes, énumérations et alias (`using`)  
* **constructeurs, opérateurs d’affectation, destructeur**  
* **fonctions**  
* **données**  

Utilisez l’ordre `public` → `protected` → `private`.  

C’est une recommandation pour les cas où vous n’avez aucune contrainte ou meilleure idée (024‑naming.md). Cette règle a été ajoutée après de nombreuses demandes d’orientation.  

##### Exemple  

    class X {
    public:
        // interface
    protected:
        // fonction non vérifiée pour être utilisée par les implémentations des classes dérivées
    private:
        // détails d’implémentation
    };  

##### Exemple (découpage du public)  

    class X {
    public:
        // interface
    protected:
        // fonction non vérifiée pour être utilisée par les implémentations des classes dérivées
    private:
        // détails d’implémentation (types, fonctions et données)
    };  

##### Exemple, mauvais  

    class X {   // mauvais
    public:
        void f();
    public:
        int g();
        // ...
    };  

L’utilisation de macros pour déclarer des groupes de membres conduit souvent à la violation de toute règle d’ordre. Or, les macros masquent déjà ce qui est exprimé.  

##### Application  

Signaler les écarts par rapport à l’ordre suggéré. De nombreux anciens codes ne suivront pas cette règle.  

---

### <a name="rl-knr"></a>NL.17 : Utiliser une mise en page dérivée de K&R  

##### Raison  

C’est le style original du C et du C++. Il préserve bien l’espace vertical et distingue les différentes constructions du langage (fonctions, classes, …).  

##### Note  

Dans le contexte du C++, ce style est souvent appelé « Stroustrup ».  

C’est une recommandation pour les cas où vous n’avez aucune contrainte ou meilleure idée (024‑naming.md). Cette règle a été ajoutée après de nombreuses demandes d’orientation.  

##### Exemple  

    struct Cable {
        int x;
        // ...
    };

    double foo(int x)
    {
        if (0 < x) {
            // ...
        }

        switch (x) {
        case 0:
            // ...
            break;
        case amazing:
            // ...
            break;
        default:
            // ...
            break;
        }

        if (0 < x)
            ++x;

        if (x < 0)
            something();
        else
            something_else();

        return some_value;
    }  

Remarquez l’espace entre `if` et `(`.  

##### Note  

Utilisez une ligne distincte pour chaque instruction, les branches d’un `if`, et le corps d’un `for`.  

##### Note  

Le caractère `{` d’une `class` ou d’un `struct` n’est **pas** sur une ligne séparée, tandis que le `{` d’une fonction **est** sur une ligne distincte.  

##### Note  

Capitalisez les noms de vos types définis par l’utilisateur pour les distinguer des types de la bibliothèque standard.  

##### Note  

Ne capitalisez pas les noms de fonctions.  

##### Application  

Si vous désirez une application stricte, utilisez un IDE pour reformater le code.  

---

### <a name="rl-ptr"></a>NL.18 : Utiliser la mise en page des déclarateurs de style C++  

##### Raison  

Le style C met l’accent sur l’utilisation dans les expressions et la grammaire, tandis que le style C++ met l’accent sur les types. L’argument d’utilisation dans les expressions ne tient pas pour les références.  

##### Exemple  

    T& operator[](size_t);   // OK
    T &operator[](size_t);   // juste étrange
    T & operator[](size_t);   // indécis  

##### Note  

C’est une recommandation pour les cas où vous n’avez aucune contrainte ou meilleure idée (024‑naming.md). Cette règle a été ajoutée après de nombreuses demandes d’orientation.  

##### Application  

Impossible face à l’historique.  

---

### <a name="rl-misread"></a>NL.19 : Éviter les noms facilement confus  

##### Raison  

Lisibilité. Tous les écrans et imprimantes ne permettent pas de distinguer facilement tous les caractères. Nous confondons facilement les mots similaires ou légèrement mal orthographiés.  

##### Exemple  

    int oO01lL = 6; // mauvais

    int splunk = 7;
    int splonk = 8; // mauvais : splunk et splonk sont facilement confondus  

##### Application  

???  

---

### <a name="rl-stmt"></a>NL.20 : Ne pas placer deux instructions sur la même ligne  

##### Raison  

Lisibilité. Il est très facile de négliger une instruction lorsqu’il y en a d’autres sur la même ligne.  

##### Exemple  

    int x = 7; char* p = 29;    // ne pas
    int x = 7; f(x);  ++x;      // ne pas  

##### Application  

Facile.  

---

### <a name="rl-dcl"></a>NL.21 : Déclarer un seul nom (uniquement) par déclaration  

##### Raison  

Lisibilité. Minimiser la confusion avec la syntaxe du déclarateur.  

##### Note  

Pour plus de détails, voir [ES.10](010-expr.md#res-name-one) @TODO-LINK.  

---

### <a name="rl-void"></a>NL.25 : Ne pas utiliser `void` comme type d’argument  

##### Raison  

C’est verbeux et seulement nécessaire lorsque la compatibilité C importe.  

##### Exemple  

    void f(void);   // mauvais
    void g();       // meilleur  

##### Note  

Même Dennis Ritchie considérait `void f(void)` comme une abomination. Vous pouvez justifier cette abomination en C lorsqu’il n’y avait pas beaucoup de prototypes de fonctions, mais cela n’a plus de sens au XXIᵉ siècle et en C++.  

---

### <a name="rl-const"></a>NL.26 : Utiliser la notation `const` conventionnelle  

##### Raison  

La notation conventionnelle est plus familière à la plupart des programmeurs. La cohérence dans de grandes bases de code.  

##### Exemple  

    const int x = 7;    // OK
    int const y = 9;    // mauvais

    const int *const p = nullptr;   // OK, pointeur constant vers int constant
    int const *const p = nullptr;   // mauvais, pointeur constant vers int constant  

##### Note  

Nous sommes bien conscients que vous pourriez prétendre que les « mauvais » exemples sont plus logiques que ceux marqués « OK », mais ils confondent davantage les gens, en particulier les novices qui s’appuient sur du matériel d’apprentissage utilisant le style « OK » largement répandu.  

Comme toujours, rappelez‑vous que le but de ces règles de nommage et de mise en page est la cohérence et que l’esthétique varie énormément.  

C’est une recommandation pour les cas où vous n’avez aucune contrainte ou meilleure idée (024‑naming.md). Cette règle a été ajoutée après de nombreuses demandes d’orientation.  

##### Application  

Signaler `const` utilisé comme suffixe d’un type.  

---

### <a name="rl-file-suffix"></a>NL.27 : Utiliser l’extension `.cpp` pour les fichiers de code et `.h` pour les fichiers d’interface  

##### Raison  

C’est une convention de longue date. Mais la cohérence est plus importante ; si votre projet utilise autre chose, suivez‑le.  

##### Note  

Cette convention reflète un schéma d’usage commun : les en‑têtes sont souvent partagés avec le C pour être compilés à la fois en C++ et en C, d’où l’extension `.h`. Il est plus simple de nommer toutes les en‑têtes `.h` plutôt que d’utiliser des extensions différentes uniquement pour les en‑têtes destinés à être partagés avec le C. En revanche, les fichiers d’implémentation sont rarement partagés avec le C et doivent donc être distingués des fichiers `.c`. Il est donc généralement préférable de nommer tous les fichiers d’implémentation C++ avec autre chose (par ex. `.cpp`).  

Les noms spécifiques `.h` et `.cpp` ne sont pas obligatoires (juste recommandés par défaut) ; d’autres extensions sont largement utilisées (`.hh`, `.C`, `.cxx`, etc.). Dans ce document, nous nous référons à `.h` et `.cpp` comme raccourci pour les fichiers d’en‑téte et d’implémentation, même si l’extension réelle peut différer.  

Votre IDE (si vous en utilisez un) pourra avoir des opinions fortes sur les suffixes.  

##### Exemple  

    // foo.h :
    extern int a;   // une déclaration
    extern void foo();

    // foo.cpp :
    int a;   // une définition
    void foo() { ++a; }  

`foo.h` fournit l’interface à `foo.cpp`. Les variables globales sont à éviter.  

##### Exemple, mauvais  

    // foo.h :
    int a;   // une définition
    void foo() { ++a; }  

Inclure `<foo.h>` deux fois dans un programme entraîne une erreur d’édition de liens du fait de deux violations de la règle d’une définition unique.  

##### Application  

* Signaler les noms de fichiers non conventionnels.  
* Vérifier que les `.h` et `.cpp` (et leurs équivalents) respectent les règles ci‑dessus.  