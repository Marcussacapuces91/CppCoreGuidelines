# <a name="s-expr"></a>ES : Expressions et instructions  

Les expressions et les instructions sont le moyen le plus fondamental et direct d’exprimer des actions et des calculs. Les déclarations dans les portées locales sont des instructions.  

Pour les règles de nommage, de commentaires et d’indentation, voir **[NL : Nomage et mise en page]**(024-naming.md) @TODO-LINK.

## Règles générales :

* **[ES.1 : Préférez la bibliothèque standard aux autres bibliothèques et au « code fait‑main »]**(010-expr.md#res-lib) @TODO-LINK
* **[ES.2 : Préférez les abstractions appropriées à l’utilisation directe des caractéristiques du langage]**(010-expr.md#res-abstr) @TODO-LINK
* **[ES.3 : Ne vous répétez pas, évitez le code redondant]**(010-expr.md#res-dry) @TODO-LINK

## Règles de déclaration :

* **[ES.5 : Gardez les portées petites]**(010-expr.md#res-scope) @TODO-LINK
* **[ES.6 : Déclarez les noms dans les initialiseurs et les conditions de for afin de limiter la portée]**(010-expr.md#res-cond) @TODO-LINK
* **[ES.7 : Gardez les noms courants et locaux courts, et les noms rares et non‑locaux plus longs]**(010-expr.md#res‑name‑length) @TODO-LINK
* **[ES.8 : Évitez les noms qui se ressemblent]**(010-expr.md#res‑name‑similar) @TODO-LINK
* **[ES.9 : Évitez les noms en `ALL_CAPS`]**(010-expr.md#res‑not‑caps) @TODO-LINK
* **[ES.10 : Déclarez un seul nom (uniquement) par déclaration]**(010-expr.md#res‑name‑one) @TODO-LINK
* **[ES.11 : Utilisez `auto` pour éviter la répétition redondante de noms de type]**(010-expr.md#res‑auto) @TODO-LINK
* **[ES.12 : Ne réutilisez pas les noms dans des portées imbriquées]**(010-expr.md#res‑reuse) @TODO-LINK
* **[ES.20 : Initialise toujours un objet]**(010-expr.md#res‑always) @TODO-LINK
* **[ES.21 : N’instanciez pas une variable (ou une constante) avant d’en avoir besoin]**(010-expr.md#res‑introduce) @TODO-LINK
* **[ES.22 : Ne déclarez pas de variable tant que vous n’avez pas de valeur pour l’initialiser]**(010-expr.md#res‑init) @TODO-LINK
* **[ES.23 : Préférez la syntaxe d’initialisation `{}`]**(010-expr.md#res‑list) @TODO-LINK
* **[ES.24 : Utilisez un `unique_ptr<T>` pour détenir des pointeurs]**(010-expr.md#res‑unique) @TODO-LINK
* **[ES.25 : Déclarez un objet `const` ou `constexpr` sauf si vous avez besoin de le modifier plus tard]**(010-expr.md#res‑const) @TODO-LINK
* **[ES.26 : N’utilisez pas une variable à deux fins non liées]**(010-expr.md#res‑recycle) @TODO-LINK
* **[ES.27 : Utilisez `std::array` ou `stack_array` pour les tableaux sur la pile]**(010-expr.md#res‑stack) @TODO-LINK
* **[ES.28 : Utilisez les lambda pour des initialisations complexes, notamment de variables `const`]**(010-expr.md#res‑lambda‑init) @TODO-LINK
* **[ES.30 : N’utilisez pas les macros pour manipuler le texte du programme]**(010-expr.md#res‑macros) @TODO-LINK
* **[ES.31 : N’utilisez pas les macros pour des constantes ou « fonctions »]**(010-expr.md#res‑macros2) @TODO-LINK
* **[ES.32 : Utilisez `ALL_CAPS` pour tous les noms de macro]**(010-expr.md#res‑all_caps) @TODO-LINK
* **[ES.33 : Si vous devez utiliser des macros, donnez‑leur des noms uniques]**(010-expr.md#res‑macros3) @TODO-LINK
* **[ES.34 : N’introduisez pas une fonction variadique de type C]**(010-expr.md#res‑ellipses) @TODO-LINK

## Règles d’expression :

* **[ES.40 : Évitez les expressions compliquées]**(010-expr.md#res‑complicated) @TODO-LINK
* **[ES.41 : En cas de doute sur la priorité des opérateurs, mettez des parenthèses]**(010-expr.md#res‑parens) @TODO-LINK
* **[ES.42 : Gardez l’utilisation des pointeurs simple et directe]**(010-expr.md#res‑ptr) @TODO-LINK
* **[ES.43 : Évitez les expressions dont l’ordre d’évaluation est indéfini]**(010-expr.md#res‑order) @TODO-LINK
* **[ES.44 : Ne dépendez pas de l’ordre d’évaluation des arguments de fonction]**(010-expr.md#res‑order‑fct) @TODO-LINK
* **[ES.45 : Évitez les « constantes magiques » ; utilisez des constantes symboliques]**(010-expr.md#res‑magic) @TODO-LINK
* **[ES.46 : Évitez les conversions de rétrécissement]**(010-expr.md#res‑narrowing) @TODO-LINK
* **[ES.47 : Utilisez `nullptr` plutôt que `0` ou `NULL`]**(010-expr.md#res‑nullptr) @TODO-LINK
* **[ES.48 : Évitez les castings]**(010-expr.md#res‑casts) @TODO-LINK
* **[ES.49 : Si vous devez caster, utilisez un cast nommé]**(010-expr.md#res‑casts‑named) @TODO-LINK
* **[ES.50 : Ne retirez pas le `const` avec un cast]**(010-expr.md#res‑casts‑const) @TODO-LINK
* **[ES.55 : Évitez le besoin de vérifications d’intervalle]**(010-expr.md#res‑range‑checking) @TODO-LINK
* **[ES.56 : N’écrivez `std::move()` que quand vous avez réellement besoin de déplacer explicitement un objet vers une autre portée]**(010-expr.md#res‑move) @TODO-LINK
* **[ES.60 : Évitez `new` et `delete` en dehors des fonctions de gestion de ressources]**(010-expr.md#res‑new) @TODO-LINK
* **[ES.61 : Supprimez les tableaux avec `delete[]` et les non‑tableaux avec `delete`]**(010-expr.md#res‑del) @TODO-LINK
* **[ES.62 : Ne comparez pas des pointeurs provenant de tableaux différents]**(010-expr.md#res‑arr2) @TODO-LINK
* **[ES.63 : N’effectuez pas de slicing]**(010-expr.md#res‑slice) @TODO-LINK
* **[ES.64 : Utilisez la notation `T{e}` pour la construction]**(010-expr.md#res‑construct) @TODO-LINK
* **[ES.65 : Ne déréférencez pas un pointeur invalide]**(010-expr.md#res‑deref) @TODO-LINK

## Règles d’instruction :

* **[ES.70 : Préférez un `switch` à un `if` lorsqu’il y a un choix]**(010-expr.md#res‑switch‑if) @TODO-LINK
* **[ES.71 : Préférez un `for`‑range à un `for` classique lorsqu’il y a un choix]**(010-expr.md#res‑for‑range) @TODO-LINK
* **[ES.72 : Préférez un `for` à un `while` lorsqu’un compteur de boucle est évident]**(010-expr.md#res‑for‑while) @TODO-LINK
* **[ES.73 : Préférez un `while` à un `for` lorsqu’il n’y a pas de compteur de boucle évident]**(010-expr.md#res‑while‑for) @TODO-LINK
* **[ES.74 : Préférez déclarer la variable de boucle dans la partie initialisation du `for`]**(010-expr.md#res‑for‑init) @TODO-LINK
* **[ES.75 : Évitez les instructions `do`]**(010-expr.md#res‑do) @TODO-LINK
* **[ES.76 : Évitez le `goto`]**(010-expr.md#res‑goto) @TODO-LINK
* **[ES.77 : Minimisez l’usage de `break` et `continue` dans les boucles]**(010-expr.md#res‑continue) @TODO-LINK
* **[ES.78 : Ne comptez pas sur le « fallthrough » implicite dans les `switch`]**(010-expr.md#res‑break) @TODO-LINK
* **[ES.79 : Utilisez `default` pour traiter les cas courants (seulement)]**(010-expr.md#res‑default) @TODO-LINK
* **[ES.84 : N’essayez pas de déclarer une variable locale sans nom]**(010-expr.md#res‑noname) @TODO-LINK
* **[ES.85 : Rendez les instructions vides visibles]**(010-expr.md#res‑empty) @TODO-LINK
* **[ES.86 : Évitez de modifier la variable de contrôle d’une boucle `for` brute à l’intérieur de son corps]**(010-expr.md#res‑loop‑counter) @TODO-LINK
* **[ES.87 : N’ajoutez pas de `==` ou `!=` redondants aux conditions]**(010-expr.md#res‑if) @TODO-LINK

## Règles arithmétiques :

* **[ES.100 : Ne mélangez pas des calculs signés et non signés]**(010-expr.md#res‑mix) @TODO-LINK
* **[ES.101 : Utilisez des types non signés pour la manipulation de bits]**(010-expr.md#res‑unsigned) @TODO-LINK
* **[ES.102 : Utilisez des types signés pour les calculs]**(010-expr.md#res‑signed) @TODO-LINK
* **[ES.103 : Ne dépassez pas les limites (overflow)]**(010-expr.md#res‑overflow) @TODO-LINK
* **[ES.104 : Ne sous‑débordez pas (underflow)]**(010-expr.md#res‑underflow) @TODO-LINK
* **[ES.105 : Ne divisez pas par zéro entier]**(010-expr.md#res‑zero) @TODO-LINK
* **[ES.106 : N’essayez pas d’éviter les valeurs négatives en utilisant `unsigned`]**(010-expr.md#res‑nonnegative) @TODO-LINK
* **[ES.107 : N’utilisez pas `unsigned` pour les index, préférez `gsl::index`]**(010-expr.md#res‑subscripts) @TODO-LINK

---  

### <a name="res-lib"></a>ES.1 : Préférez la bibliothèque standard aux autres bibliothèques et au « code fait‑main »

#### Raison  

Un code qui utilise une bibliothèque peut être bien plus facile à écrire qu’un code qui travaille directement avec les fonctionnalités du langage, beaucoup plus court, tend à être d’un niveau d’abstraction supérieur, et le code de la bibliothèque est présumé déjà testé.  
La bibliothèque standard ISO C++ fait partie des bibliothèques les plus connues et les mieux testées. Elle est disponible avec toutes les implémentations de C++.

#### Exemple  

```    
    auto sum = accumulate(begin(a), end(a), 0.0);   // bon
```  

Une version à portée de `accumulate` serait encore meilleure :

```    
    auto sum = accumulate(v, 0.0); // meilleur
```  

mais n’écrivez pas à la main un algorithme bien connu :

```    
    int max = v.size();   // mauvais : verbeux, but non indiqué
    double sum = 0.0;
    for (int i = 0; i < max; ++i)
        sum = sum + v[i];
```  

#### Exception  

Une grande partie de la bibliothèque standard repose sur l’allocation dynamique (tas). Ces parties, notamment les conteneurs mais pas les algorithmes, ne conviennent pas aux applications temps réel strictes ou embarquées. Dans ce cas, envisagez de fournir/utiliser des installations similaires, par ex. : un conteneur de type « standard‑library‑style » implémenté avec un allocateur de pool.

#### Application  

Pas simple. ??? Cherchez des boucles désordonnées, des boucles imbriquées, des fonctions longues, l’absence d’appels de fonction, le manque d’utilisation de types intégrés. Complexité cyclomatique ? @TODO-LINK  

---

### <a name="res-abstr"></a>ES.2 : Préférez les abstractions appropriées à l’utilisation directe des fonctionnalités du langage  

#### Raison  

Une « abstraction appropriée » (bibliothèque ou classe) se rapproche davantage des concepts de l’application que le langage brut, conduit à un code plus court et plus clair, et est probablement mieux testé.

#### Exemple  

```    
    vector<string> read1(istream& is)   // bon
    {
        vector<string> res;
        for (string s; is >> s;)
            res.push_back(s);
        return res;
    }
```  

L’équivalent plus traditionnel et bas niveau est plus long, plus confus, plus difficile à bien faire et très probablement plus lent :

```    
    char** read2(istream& is, int maxelem, int maxstring, int* nread)   // mauvais : verbeux et incomplet
    {
        auto res = new char*[maxelem];
        int elemcount = 0;
        while (is && elemcount < maxelem) {
            auto s = new char[maxstring];
            is.read(s, maxstring);
            res[elemcount++] = s;
        }
        *nread = elemcount;
        return res;
    }
```  

Lorsque le contrôle des dépassements et la gestion des erreurs sont ajoutés, le code devient très confus, et il reste le problème de se souvenir de `delete` le pointeur retourné ainsi que les chaînes C‑style que le tableau contient.

#### Application  

Pas simple. ??? Cherchez des boucles désordonnées, des boucles imbriquées, des fonctions longues, l’absence d’appels de fonction, le manque d’utilisation de types intégrés. Complexité cyclomatique ? @TODO-LINK  

---

### <a name="res-dry"></a>ES.3 : Ne vous répétez pas, évitez le code redondant  

Le code dupliqué ou autrement redondant masque l’intention, rend la logique plus difficile à comprendre et complique la maintenance, entre autres problèmes. Il apparaît souvent à force de copier‑coller du code.  

Utilisez les algorithmes standard quand cela est approprié, plutôt que d’écrire votre propre implémentation.  

**Voir aussi** : [SL.1](018-stdlib.md#rsl-lib) @TODO-LINK, [ES.11](010-expr.md#res‑auto) @TODO-LINK  

#### Exemple  

```    
    void func(bool flag)    // Mauvais, code dupliqué.
    {
        if (flag) {
            x();
            y();
        }
        else {
            x();
            z();
        }
    }

    void func(bool flag)    // Meilleur, pas de code dupliqué.
    {
        x();

        if (flag)
            y();
        else
            z();
    }
```  

#### Application  

* Utilisez un analyseur statique ; il détectera au moins certaines constructions redondantes.  
* Revue de code  

---

## ES.dcl : Déclarations  

Une déclaration est une instruction. Une déclaration introduit un nom dans une portée et peut entraîner la construction d’un objet nommé.

### <a name="res-scope"></a>ES.5 : Gardez les portées petites  

#### Raison  

Lisibilité. Minimiser la rétention de ressources. Éviter les mauvais usages accidentels d’une valeur.  

**Formulation alternative** : Ne déclarez pas un nom dans une portée inutilement grande.

#### Exemple  

```    
    void use()
    {
        int i;    // mauvais : i est accessible inutilement après la boucle
        for (i = 0; i < 20; ++i) { /* ... */ }
        // aucun usage prévu de i ici
        for (int i = 0; i < 20; ++i) { /* ... */ }  // bon : i est local à la boucle for

        if (auto pc = dynamic_cast<Circle*>(ps)) {  // bon : pc est local à l’instruction if
            // ... traitement de Circle ...
        }
        else {
            // ... traitement d’erreur ...
        }
    }
```  

#### Exemple, mauvais  

```    
    void use(const string& name)
    {
        string fn = name + ".txt";
        ifstream is {fn};
        Record r;
        is >> r;
        // ... 200 lignes de code sans usage prévu de fn ou is ...
    }
```  

Cette fonction est déjà trop longue, mais le point est que les ressources utilisées par `fn` et le descripteur de fichier `is` sont retenues bien plus longtemps que nécessaire, ce qui pourrait entraîner un usage imprévu plus tard dans la fonction.  
Dans ce cas, il peut être judicieux d’extraire la lecture :

```    
    Record load_record(const string& name)
    {
        string fn = name + ".txt";
        ifstream is {fn};
        Record r;
        is >> r;
        return r;
    }

    void use(const string& name)
    {
        Record r = load_record(name);
        // ... 200 lignes de code ...
    }
```  

#### Application  

* Signaler les variables de boucle déclarées hors de la boucle et non utilisées après la boucle.  
* Signaler quand des ressources coûteuses (descripteurs de fichiers, verrous, …) ne sont pas utilisées pendant N lignes (pour un N adapté). @TODO-LINK  

---

### <a name="res-cond"></a>ES.6 : Déclarez les noms dans les initialiseurs et les conditions de `for` afin de limiter la portée  

#### Raison  

Lisibilité. Limiter la visibilité de la variable de boucle à la portée de la boucle. Éviter d’utiliser la variable de boucle à d’autres fins après la boucle. Minimiser la rétention de ressources.

#### Exemple  

```    
    void use()
    {
        for (string s; cin >> s;)
            v.push_back(s);

        for (int i = 0; i < 20; ++i) {   // bon : i est local à la boucle for
            // ...
        }

        if (auto pc = dynamic_cast<Circle*>(ps)) {   // bon : pc est local à l’instruction if
            // ... traitement de Circle ...
        }
        else {
            // ... traitement d’erreur ...
        }
    }
```  

#### Exemple, à éviter  

```    
    int j;                            // MAUVAIS : j est visible hors de la boucle
    for (j = 0; j < 100; ++j) {
        // ...
    }
    // j est encore visible ici et n’est pas nécessaire
```  

**Voir aussi** : [Ne pas utiliser une variable à deux fins non liées](010-expr.md#res‑recycle) @TODO-LINK  

#### Application  

* Avertir lorsqu’une variable modifiée dans l’instruction `for` est déclarée en dehors de la boucle et n’est pas utilisée à l’extérieur.  
* (difficile) Signaler les variables de boucle déclarées avant la boucle et réutilisées après la boucle à des fins non liées. @TODO-LINK  

**Discussion** : Limiter la variable de boucle au corps de la boucle aide grandement les optimisateurs. Reconnaître que la variable d’induction n’est accessible que dans le corps débloque des optimisations telles que le hissage, la réduction de force, le déplacement du code invariant, etc.

#### Exemple C++17 et C++20  

Note : C++17 et C++20 ajoutent également les initialiseurs d’instructions `if`, `switch` et `range‑for`. Ces dernières nécessitent le support de C++17 et C++20.

```    
    map<int, string> mymap;

    if (auto result = mymap.insert(value); result.second) {
        // insertion réussie, et result est valide pour ce bloc
        use(result.first);  // ok
        // ...
    } // result est détruit ici
```  

#### Application C++17/C++20 (si le compilateur supporte C++17 ou C++20)  

* Signaler les variables de sélection/boucle déclarées avant le corps et non utilisées après le corps.  
* (difficile) Signaler les variables de sélection/boucle déclarées avant le corps et utilisées après le corps à des fins non liées. @TODO-LINK  

---

### <a name="res-name-length"></a>ES.7 : Gardez les noms courants et locaux courts, et les noms rares et non‑locaux plus longs  

#### Raison  

Lisibilité. Réduire les risques de collisions entre noms non liés.

#### Exemple  

Les noms courts et locaux conventionnels augmentent la lisibilité :

```    
    template<typename T>    // bon
    void print(ostream& os, const vector<T>& v)
    {
        for (gsl::index i = 0; i < v.size(); ++i)
            os << v[i] << '\n';
    }
```  

Un indice se nomme habituellement `i` et il n’y a aucune indication sur le sens du vecteur dans cette fonction générique, donc `v` est un nom aussi bon que n’importe quel autre. Comparez :

```    
    template<typename Element_type>   // mauvais : verbeux, difficile à lire
    void print(ostream& target_stream, const vector<Element_type>& current_vector)
    {
        for (gsl::index current_element_index = 0;
             current_element_index < current_vector.size();
             ++current_element_index
        )
        target_stream << current_vector[current_element_index] << '\n';
    }
```  

Oui, c’est une caricature, mais on a vu pire.

#### Exemple  

Des noms non‑locaux peu conventionnels et courts obscurcissent le code :

```    
    void use1(const string& s)
    {
        // ...
        tt(s);   // mauvais : qu’est‑ce que tt() ?
        // ...
    }
```  

Mieux, donnez aux entités non‑locales des noms lisibles :

```    
    void use1(const string& s)
    {
        // ...
        trim_tail(s);   // meilleur
        // ...
    }
```  

#### Exemple, mauvais  

Les noms d’arguments de fonctions volumineuses sont de facto non‑locaux et doivent être significatifs :

```    
    void complicated_algorithm(vector<Record>& vr, const vector<int>& vi, map<string, int>& out)
    // lire les événements dans vr (marquant les Records utilisés) pour les index dans
    // vi plaçant des paires (nom, index) dans out
    {
        // ... 500 lignes de code utilisant vr, vi et out ...
    }
```  

Nous recommandons de garder les fonctions courtes, mais cette règle n’est pas toujours appliquée et la dénomination doit refléter cela.

#### Application  

Vérifier la longueur des noms locaux et non‑locaux. Tenir également compte de la longueur des fonctions. @TODO-LINK  

---

### <a name="res-name-similar"></a>ES.8 : Évitez les noms qui se ressemblent  

#### Raison  

Clarté et lisibilité du code. Des noms trop similaires ralentissent la compréhension et augmentent la probabilité d’erreurs.

#### Exemple, mauvais  

```    
    if (readable(i1 + l1 + ol + o1 + o0 + ol + o1 + I0 + l0)) surprise();
```  

#### Exemple, mauvais  

Ne déclarez pas un non‑type avec le même nom qu’un type dans la même portée. Cela supprime le besoin de désambiguïser avec un mot‑clé tel que `struct` ou `enum`. Cela élimine aussi une source d’erreurs, puisque `struct X` peut implicitement déclarer `X` si la recherche échoue.

```    
    struct foo { int n; };
    struct foo foo();       // MAUVAIS, foo est déjà un type dans la portée
    struct foo x = foo();   // nécessite désambiguïsation
```  

#### Exception  

Des en‑têtes antiques peuvent déclarer des non‑types et des types avec le même nom dans la même portée.

#### Application  

* Vérifier les noms contre une liste de combinaisons de lettres et chiffres connues pour être source de confusion.  
* Signaler une déclaration de variable, fonction ou énumérateur qui masque une classe ou une énumération déclarée dans la même portée. @TODO-LINK  

---

### <a name="res-not-caps"></a>ES.9 : Évitez les noms en `ALL_CAPS`  

#### Raison  

Ces noms sont couramment utilisés pour les macros. Ainsi, les noms en `ALL_CAPS` sont vulnérables à une substitution macro non intentionnée.

#### Exemple  

```    
    // quelque part dans un en‑tête :
    #define NE !=

    // ailleurs dans un autre en‑tête :
    enum Coord { N, NE, NW, S, SE, SW, E, W };

    // dans un troisième en‑tête d’un mauvais programmeur :
    switch (direction) {
    case N:
        // ...
    case NE:
        // ...
    // ...
    }
```  

#### Note  

N’utilisez pas `ALL_CAPS` pour les constantes simplement parce que les constantes étaient autrefois des macros.

#### Application  

* Signaler toute utilisation de `ALL_CAPS`. Pour le code ancien, accepter les `ALL_CAPS` pour les noms de macros et signaler les noms de macros non `ALL_CAPS`. @TODO-LINK  

---

### <a name="res-name-one"></a>ES.10 : Déclarez un seul nom (uniquement) par déclaration  

#### Raison  

Une déclaration par ligne augmente la lisibilité et évite les erreurs liées à la grammaire C/C++. Elle laisse également de la place pour un commentaire de fin de ligne plus descriptif.

#### Exemple, mauvais  

```    
    char *p, c, a[7], *pp[7], **aa[10];   // yuck !
```  

#### Exception  

Une déclaration de fonction peut contenir plusieurs déclarations d’arguments de fonction.

#### Exception  

Une liaison structurée (C++17) est conçue spécifiquement pour introduire plusieurs variables :

```    
    auto [iter, inserted] = m.insert_or_assign(k, val);
    if (inserted) { /* une nouvelle entrée a été insérée */ }
```  

#### Exemple  

```    
    template<class InputIterator, class Predicate>
    bool any_of(InputIterator first, InputIterator last, Predicate pred);
```  

ou mieux en utilisant les concepts :

```    
    bool any_of(input_iterator auto first, input_iterator auto last, predicate auto pred);
```  

#### Exemple  

```    
    double scalbn(double x, int n);   // OK : x * pow(FLT_RADIX, n); FLT_RADIX vaut généralement 2
```  

ou :

```    
    double scalbn(    // meilleur : x * pow(FLT_RADIX, n); FLT_RADIX vaut généralement 2
        double x,     // valeur de base
        int n         // exposant
    );
```  

ou :

```    
    // meilleur : base * pow(FLT_RADIX, exponent); FLT_RADIX vaut généralement 2
    double scalbn(double base, int exponent);
```  

#### Exemple  

```    
    int a = 10, b = 11, c = 12, d, e = 14, f = 15;
```  

Dans une longue liste de déclarateurs, il est facile d’omettre une variable non initialisée.

#### Application  

* Signaler les déclarations de variables et de constantes contenant plusieurs déclarateurs (par ex. `int* p, q;`). @TODO-LINK  

---

### <a name="res-auto"></a>ES.11 : Utilisez `auto` pour éviter la répétition redondante de noms de type  

#### Raison  

* La répétition simple est fastidieuse et propice aux erreurs.  
* Quand vous utilisez `auto`, le nom de l’entité déclarée se trouve à une position fixe dans la déclaration, ce qui augmente la lisibilité.  
* Dans une déclaration de fonction‑template, le type de retour peut être un type membre.

#### Exemple  

```    
    auto p = v.begin();      // vector<DataRecord>::iterator
    auto z1 = v[3];          // copie de DataRecord
    auto& z2 = v[3];         // évite la copie
    const auto& z3 = v[3];   // const et évite la copie
    auto h = t.future();
    auto q = make_unique<int[]>(s);
    auto f = [](int x) { return x + 10; };
```  

Dans chaque cas, on évite d’écrire un type long et difficile à retenir que le compilateur connaît déjà, mais qu’un programmeur pourrait mal écrire.

#### Exemple  

```    
    template<class T>
    auto Container<T>::first() -> Iterator;   // Container<T>::Iterator
```  

#### Exception  

Évitez `auto` pour les listes d’initialisation et dans les cas où vous savez exactement quel type vous voulez et où un initialiseur pourrait nécessiter une conversion.

#### Exemple  

```    
    auto lst = { 1, 2, 3 };   // lst est un initializer_list
    auto x{1};   // x est un int (en C++17 ; initializer_list en C++11)
```  

#### Note  

Depuis C++20, nous pouvons (et devrions) utiliser des concepts pour être plus précis sur le type que nous déduisons :

```    
    // …
    forward_iterator auto p = algo(x, y, z);
```  

#### Exemple (C++17)  

```    
    std::set<int> values;
    // …
    auto [ position, newly_inserted ] = values.insert(5);   // décompose les membres du std::pair
```  

#### Application  

* Signaler la répétition redondante de noms de type dans une déclaration. @TODO-LINK  

---

### <a name="res-reuse"></a>ES.12 : Ne réutilisez pas les noms dans des portées imbriquées  

#### Raison  

Il est facile de se tromper sur la variable réellement utilisée. Cela peut causer des problèmes de maintenance.

#### Exemple, mauvais  

```    
    int d = 0;
    // …
    if (cond) {
        // …
        d = 9;
        // …
    }
    else {
        // …
        int d = 7;
        // …
        d = value_to_be_returned;
        // …
    }

    return d;
```  

Si c’est une grande instruction `if`, il est facile d’oublier qu’un nouveau `d` a été introduit dans la portée interne. C’est une source connue de bugs. Parfois, ce réemploi de nom dans une portée interne est appelé « shadowing ».

#### Note  

Le shadowing pose surtout problème lorsque les fonctions sont trop grandes et trop complexes.

#### Exemple  

Le shadowing des arguments de fonction dans le bloc le plus externe est interdit par le langage :

```    
    void f(int x)
    {
        int x = 4;  // erreur : réutilisation du nom d’argument de fonction

        if (x) {
            int x = 7;  // autorisé, mais mauvais
            // …
        }
    }
```  

#### Exemple, mauvais  

Réutiliser le nom d’un membre comme variable locale peut aussi poser problème :

```    
    struct S {
        int m;
        void f(int x);
    };

    void S::f(int x)
    {
        m = 7;    // affecte le membre
        if (x) {
            int m = 9;
            // …
            m = 99; // affecte la variable locale
            // …
        }
    }
```  

#### Exception  

Nous réutilisons souvent les noms de fonctions d’une classe de base dans une classe dérivée :

```    
    struct B {
        void f(int);
    };

    struct D : B {
        void f(double);
        using B::f;
    };
```  

C’est source d’erreurs. Par exemple, si l’on avait oublié la déclaration `using`, un appel `d.f(1)` n’aurait pas trouvé la version `int` de `f`.

??? Faut‑il une règle spécifique sur le shadowing/hiding dans les hiérarchies de classes ? @TODO-LINK  

#### Application  

* Signaler le réemploi de nom dans des portées locales imbriquées.  
* Signaler le réemploi d’un nom de membre comme variable locale dans une fonction membre.  
* Signaler le réemploi d’un nom global comme variable locale ou nom de membre.  
* Signaler le réemploi d’un nom de membre de classe de base dans une classe dérivée (sauf pour les noms de fonctions). @TODO-LINK  

---

### <a name="res-always"></a>ES.20 : Initialise toujours un objet  

#### Raison  

Éviter les erreurs d’usage avant initialisation (undefined behaviour). Éviter les problèmes de compréhension d’une initialisation complexe. Simplifier le refactoring.

#### Exemple  

```    
    void use(int arg)
    {
        int i;   // mauvais : variable non initialisée
        // …
        i = 7;   // initialise i
    }
```  

Non, `i = 7` n’initialise pas `i` ; c’est une assignation. De plus, `i` peut être lu dans la partie `...`. Mieux :

```    
    void use(int arg)   // OK
    {
        int i = 7;   // OK : initialisé
        string s;    // OK : initialisé par défaut
        // …
    }
```  

#### Note  

La règle « always initialize » est volontairement plus stricte que la règle du langage « un objet doit être assigné avant d’être utilisé ». Cette dernière règle, moins contraignante, repère les bugs techniques, mais :

* Elle conduit à un code moins lisible.  
* Elle incite à déclarer des noms dans des portées plus grandes que nécessaire.  
* Elle rend le code plus difficile à lire.  
* Elle engendre des bugs logiques en encourageant du code complexe.  
* Elle complique le refactoring.  

La règle « always initialize » est une règle de style visant à améliorer la maintenabilité ainsi qu’une règle de protection contre les usages avant initialisation.

#### Exemple  

Voici un exemple souvent considéré comme démontrant le besoin d’une règle plus souple pour l’initialisation :

```    
    widget i;    // « widget » est un type coûteux à initialiser, possiblement un grand type trivial
    widget j;

    if (cond) {  // mauvais : i et j sont initialisés « tard »
        i = f1();
        j = f2();
    }
    else {
        i = f3();
        j = f4();
    }
```  

Cela ne peut pas être réécrit trivially pour initialiser `i` et `j` avec des initialiseurs. Notez que pour les types avec constructeur par défaut, tenter de différer l’initialisation conduit simplement à une initialisation par défaut suivie d’une assignation. Une raison populaire pour de tels exemples est « l’efficacité », mais un compilateur capable de détecter une erreur d’usage avant initialisation peut également éliminer toute double initialisation redondante.

En supposant qu’il existe un lien logique entre `i` et `j`, ce lien devrait probablement être exprimé dans le code :

```    
    pair<widget, widget> make_related_widgets(bool x)
    {
        return (x) ? {f1(), f2()} : {f3(), f4()};
    }

    auto [i, j] = make_related_widgets(cond);    // C++17
```  

Si la fonction `make_related_widgets` est sinon redondante, on peut l’éliminer en utilisant une lambda [ES.28](010-expr.md#res‑lambda‑init) :

```    
    auto [i, j] = [x] { return (x) ? pair{f1(), f2()} : pair{f3(), f4()} }();    // C++17
```  

Utiliser une valeur représentant « non initialisé » est le symptôme d’un problème, pas une solution :

```    
    widget i = uninit;  // mauvais
    widget j = uninit;

    // …
    use(i);         // possiblement utilisé avant d’être fixé
    // …

    if (cond) {     // mauvais : i et j sont initialisés « tard »
        i = f1();
        j = f2();
    }
    else {
        i = f3();
        j = f4();
    }
```  

Le compilateur ne peut même pas détecter aisément une utilisation avant assignation. De plus, nous introduisons une complexité dans l’espace d’état du widget : quelles opérations sont valides sur un widget « uninit » et lesquelles ne le sont pas ?

#### Note  

L’initialisation complexe a longtemps séduit les programmeurs ingénieux. Elle a aussi été une source majeure d’erreurs et de complexité. De nombreuses erreurs sont introduites lors de la maintenance, années après l’implémentation initiale.

#### Exemple (membres de données)  

```    
    class X {
    public:
        X(int i, int ci) : m2{i}, cm2{ci} {}
        // …

    private:
        int m1 = 7;
        int m2;
        int m3;

        const int cm1 = 7;
        const int cm2;
        const int cm3;
    };
```  

Le compilateur signalera le `cm3` non initialisé parce qu’il est `const`, mais il ne détectera pas le manque d’initialisation du `m3`. Habituellement, une initialisation de membre rare vaut la peine d’être ajoutée pour éviter les erreurs d’absence d’initialisation, et souvent un optimiseur peut éliminer une initialisation redondante (par ex. une initialisation qui se produit juste avant une assignation).

#### Exception  

Si vous déclarez un objet qui va être immédiatement initialisé à partir d’une entrée, l’initialiser provoquerait une double initialisation. Cependant, cela peut laisser des données non initialisées au‑delà de l’entrée — et c’est une source fertile d’erreurs et de failles de sécurité :

```    
    constexpr int max = 8 * 1024;
    int buf[max];         // OK, mais suspect : non initialisé
    f.read(buf, max);
```  

Le coût d’initialisation de ce tableau peut être significatif dans certaines situations. Cependant, de tels exemples tendent à laisser des variables non initialisées accessibles, il faut donc les considérer avec suspicion.

```    
    constexpr int max = 8 * 1024;
    int buf[max] = {};   // Initialise tous les éléments à zéro ; meilleur dans certaines situations
    f.read(buf, max);
```  

À cause des règles restrictives d’initialisation des tableaux et de `std::array`, ils offrent les exemples les plus convaincants nécessitant cette exception.

Lorsque cela est possible, utilisez une fonction de bibliothèque connue pour ne pas dépasser le tampon. Par exemple :

```    
    string s;   // s est initialisé par défaut à ""
    cin >> s;   // s s’étend pour contenir la chaîne
```  

Ne considérez pas les variables simples qui sont des cibles d’opérations d’entrée comme une exception à cette règle :

```    
    int i;   // mauvais
    // …
    cin >> i;
```  

Dans le cas pas rare où la cible d’entrée et l’opération d’entrée sont séparées (ce qui ne devrait pas arriver) le risque d’usage avant initialisation apparaît.

```    
    int i2 = 0;   // meilleur, en supposant que zéro soit une valeur acceptable pour i2
    // …
    cin >> i2;
```  

Un bon optimiseur devrait connaître les opérations d’entrée et éliminer l’opération redondante.

#### Note  

Parfois, une lambda peut être utilisée comme initialisateur pour éviter une variable non initialisée :

```    
    error_code ec;
    Value v = [&] {
        auto p = get_value();   // get_value() renvoie un pair<error_code, Value>
        ec = p.first;
        return p.second;
    }();
```  

ou peut‑être :

```    
    Value v = [] {
        auto p = get_value();   // get_value() renvoie un pair<error_code, Value>
        if (p.first) throw Bad_value{p.first};
        return p.second;
    }();
```  

**Voir aussi** : [ES.28](010-expr.md#res‑lambda‑init) @TODO-LINK  

#### Application  

* Signaler chaque variable non initialisée. Ne pas signaler les variables de types définis par l’utilisateur possédant un constructeur par défaut.  
* Vérifier qu’un tampon non initialisé soit écrit *immédiatement* après la déclaration. Passer une variable non initialisée par référence à un argument non‑`const` peut être supposé être une écriture dans la variable. @TODO-LINK  

---

### <a name="res-introduce"></a>ES.21 : N’instanciez pas une variable (ou une constante) avant d’en avoir besoin  

#### Raison  

Lisibilité. Limiter la portée où la variable peut être utilisée.

#### Exemple  

```    
    int x = 7;
    // ... aucune utilisation de x ici ...
    ++x;
```  

#### Application  

* Signaler les déclarations qui sont éloignées de leur première utilisation. @TODO-LINK  

---

### <a name="res-init"></a>ES.22 : Ne déclarez pas de variable tant que vous n’avez pas de valeur pour l’initialiser  

#### Raison  

Lisibilité. Limiter la portée où la variable peut être utilisée. Éviter le risque d’usage avant initialisation. L’initialisation est souvent plus efficace qu’une assignation.

#### Exemple, mauvais  

```    
    string s;
    // ... aucune utilisation de s ici ...
    s = "what a waste";
```  

#### Exemple, mauvais  

```    
    SomeLargeType var;  // nom difficile à lire CaMeLcAsEvArIaBlE

    if (cond)   // condition non triviale
        Set(&var);
    else if (cond2 || !cond3) {
        var = Set2(3.14);
    }
    else {
        var = 0;
        for (auto& e : something)
            var += e;
    }

    // utilise var ; s’assurer que cela n’est pas fait trop tôt peut être imposé statiquement uniquement avec le flux de contrôle
```  

Ce serait correct s’il existait une initialisation par défaut pour `SomeLargeType` qui ne soit pas trop coûteuse. Sinon, le programmeur peut très bien se demander si chaque chemin possible à travers le labyrinthe de conditions a bien été couvert. Si ce n’est pas le cas, on a un bug « utilisation avant initialisation ». C’est un piège de maintenance.

Pour des initialiseurs d’une complexité modérée, y compris pour des variables `const`, envisagez d’utiliser une lambda pour exprimer l’initialiseur ; voir [ES.28](010-expr.md#res‑lambda‑init).

#### Application  

* Signaler les déclarations avec initialisation par défaut qui sont assignées avant d’être lues pour la première fois.  
* Signaler tout calcul compliqué après une variable non initialisée et avant son utilisation. @TODO-LINK  

---

### <a name="res-list"></a>ES.23 : Préférez la syntaxe d’initialisation `{}`  

#### Raison  

Préférez `{}`. Les règles d’initialisation `{}` sont plus simples, plus générales, moins ambiguës et plus sûres que d’autres formes d’initialisation.  

Utilisez `=` seulement quand vous êtes sûr qu’il ne peut y avoir aucune conversion de rétrécissement. Pour les types arithmétiques intégrés, utilisez `=` uniquement avec `auto`.  

Évitez l’initialisation `()` qui autorise des ambiguïtés d’analyse.

#### Exemple  

```    
    int x {f(99)};
    int y = x;
    vector<int> v = {1, 2, 3, 4, 5, 6};
```  

#### Exception  

Pour les conteneurs, il y a une tradition d’utiliser `{...}` pour une liste d’éléments et `(...)` pour les tailles :

```    
    vector<int> v1(10);    // vecteur de 10 éléments avec la valeur par défaut 0
    vector<int> v2{10};    // vecteur de 1 élément avec la valeur 10

    vector<int> v3(1, 2);  // vecteur de 1 élément avec la valeur 2
    vector<int> v4{1, 2};  // vecteur de 2 éléments avec les valeurs 1 et 2
```  

#### Note  

Les initialiseurs `{}` n’autorisent pas les conversions de rétrécissement (et c’est généralement une bonne chose) et autorisent les constructeurs explicites (ce qui est bien, nous initialisons intentionnellement une nouvelle variable).

#### Exemple  

```    
    int x {7.9};   // erreur : rétrécissement
    int y = 7.9;    // OK : y devient 7. Espérez un avertissement du compilateur
    int z {gsl::narrow_cast<int>(7.9)};    // OK : vous l’avez demandé
    auto zz = gsl::narrow_cast<int>(7.9);  // OK : vous l’avez demandé
```  

#### Note  

L’initialisation `{}` peut être utilisée pour presque toutes les initialisations ; les autres formes d’initialisation ne le peuvent pas :

```    
    auto p = new vector<int> {1, 2, 3, 4, 5};   // vecteur initialisé
    D::D(int a, int b) :m{a, b} {   // initialisateur de membre (par ex. m pourrait être une paire)
        // …
    };
    X var {};   // initialise var comme vide
    struct S {
        int m {7};   // initialisateur par défaut d’un membre
        // …
    };
```  

Pour cette raison, l’initialisation `{}` est souvent appelée « initialisation uniforme » (bien qu’il reste malheureusement quelques irrégularités).

#### Note  

L’initialisation d’une variable déclarée avec `auto` à partir d’une unique valeur, par ex. `{v}`, a eu des résultats surprenants jusqu’en C++17. Les règles de C++17 sont un peu moins surprenantes :

```    
    auto x1 {7};        // x1 est un int valant 7
    auto x2 = {7};      // x2 est un initializer_list<int> contenant un élément 7

    auto x11 {7, 8};    // erreur : deux initialiseurs
    auto x22 = {7, 8};  // x22 est un initializer_list<int> contenant 7 et 8

    // utilisez `={...}` si vous voulez réellement un `initializer_list<T>`
    auto fib10 = {1, 1, 2, 3, 5, 8, 13, 21, 34, 55};   // fib10 est une liste
```  

#### Note  

`={}` effectue une initialisation par copie alors que `{}` effectue une initialisation directe. Comme la distinction entre initialisation par copie et direct, cela peut conduire à des surprises. `{}` accepte les constructeurs `explicit` ; `={}` ne le fait pas. Par exemple :

```    
    struct Z { explicit Z() {} };

    Z z1{};     // OK : initialisation directe, donc on utilise le constructeur explicit
    Z z2 = {};  // erreur : initialisation par copie, on ne peut pas utiliser le constructeur explicit
```  

Utilisez l’initialisation simple `{}` sauf si vous voulez spécifiquement désactiver les constructeurs `explicit`.

#### Exemple  

```    
    template<typename T>
    void f()
    {
        T x1(1);    // T initialisé avec 1
        T x0();     // mauvais : déclaration de fonction (souvent une erreur)

        T y1 {1};   // T initialisé avec 1
        T y0 {};    // T initialisé par défaut
        // …
    }
```  

**Voir aussi** : [Discussion](#???) @TODO-LINK  

#### Application  

* Signaler l’usage de `=` pour initialiser des types arithmétiques lorsqu’un rétrécissement se produit.  
* Signaler l’usage de la syntaxe `()` d’initialisation qui correspond en fait à une déclaration. (De nombreux compilateurs devraient déjà avertir à ce sujet.) @TODO-LINK  

---

### <a name="res-unique"></a>ES.24 : Utilisez un `unique_ptr<T>` pour détenir des pointeurs  

#### Raison  

Utiliser `std::unique_ptr` est le moyen le plus simple d’éviter les fuites. C’est fiable, cela fait faire au système de types le plus gros du travail de validation de la propriété, cela augmente la lisibilité et cela n’impose aucun coût d’exécution (ou presque).

#### Exemple  

```    
    void use(bool leak)
    {
        auto p1 = make_unique<int>(7);   // OK
        int* p2 = new int{7};            // mauvais : risque de fuite
        // ... aucune assignation à p2 ...
        if (leak) return;
        // ... aucune assignation à p2 ...
        vector<int> v(7);
        v.at(7) = 0;                    // exception lancée
        delete p2;                      // trop tard pour éviter les fuites
        // …
    }
```  

Si `leak == true` l’objet pointé par `p2` est perdu et l’objet pointé par `p1` ne l’est pas. Le même problème survient quand `at()` lance une exception. Dans les deux cas, l’instruction `delete p2` n’est jamais atteinte.

#### Application  

Recherchez les pointeurs bruts qui sont la cible de `new`, `malloc()` ou de fonctions pouvant retourner de tels pointeurs. @TODO-LINK  

---

### <a name="res-const"></a>ES.25 : Déclarez un objet `const` ou `constexpr` à moins de vouloir le modifier plus tard  

#### Raison  

Ainsi vous ne pouvez pas changer la valeur par accident. Cela peut aussi offrir des opportunités d’optimisation au compilateur.

#### Exemple  

```    
    void f(int n)
    {
        const int bufmax = 2 * n + 2;  // bon : on ne peut pas changer bufmax par accident
        int xmax = n;                  // suspect : xmax est‑il censé changer ?
        // …
    }
```  

#### Application  

Vérifiez si une variable est réellement mutée, et signalez‑la si ce n’est pas le cas. Malheureusement, il peut être impossible de détecter quand un `non‑const` n’a **pas** été **intentionnellement** modifié (vs quand il simplement ne l’a pas été). @TODO-LINK  

---

### <a name="res-recycle"></a>ES.26 : N’utilisez pas une variable pour deux buts non liés  

#### Raison  

Lisibilité et sécurité.

#### Exemple, mauvais  

```    
    void use()
    {
        int i;
        for (i = 0; i < 20; ++i) { /* … */ }
        for (i = 0; i < 200; ++i) { /* … */ } // mauvais : i recyclé
    }
```  

#### Note  

Comme optimisation, vous pourriez vouloir réutiliser un tampon comme espace de travail, mais même alors privilégiez la limitation de la portée de la variable autant que possible et veillez à ne pas créer de bugs à cause de données résiduelles dans un tampon recyclé ; c’est une source courante de vulnérabilités de sécurité.

```    
    void write_to_file()
    {
        std::string buffer;             // pour éviter les réallocations à chaque itération
        for (auto& o : objects) {
            // Première partie du travail.
            generate_first_string(buffer, o);
            write_to_file(buffer);

            // Deuxième partie du travail.
            generate_second_string(buffer, o);
            write_to_file(buffer);

            // …
        }
    }
```  

#### Application  

* Signaler les variables recyclées. @TODO-LINK  

---

### <a name="res-stack"></a>ES.27 : Utilisez `std::array` ou `stack_array` pour les tableaux sur la pile  

#### Raison  

Ils sont lisibles et ne se convertissent pas implicitement en pointeurs. Ils ne sont pas confondus avec les extensions non‑standard des tableaux intégrés.

#### Exemple, mauvais  

```    
    const int n = 7;
    int m = 9;

    void f()
    {
        int a1[n];
        int a2[m];   // erreur : pas du C++
        // …
    }
```  

#### Note  

La définition de `a1` est du C++ légal et l’a toujours été. Il y a beaucoup de code de ce type. Elle est toutefois source d’erreurs, notamment lorsque la borne n’est pas locale. C’est également une « source populaire » d’erreurs (débordement de tampon, décadence de pointeur, …). La définition de `a2` est du C mais pas du C++ et elle est considérée comme un risque de sécurité.

#### Exemple  

```    
    const int n = 7;
    int m = 9;

    void f()
    {
        array<int, n> a1;
        stack_array<int> a2(m);
        // …
    }
```  

#### Application  

* Signaler les tableaux avec des bornes non constantes (VLA C‑style).  
* Signaler les tableaux avec des bornes constantes non locales. @TODO-LINK  

---

### <a name="res-lambda-init"></a>ES.28 : Utilisez les lambdas pour des initialisations complexes, surtout de variables `const`  

#### Raison  

Cela encapsule joliment l’initialisation locale, y compris le nettoyage des variables temporaires nécessaires uniquement à l’initialisation, sans devoir créer une fonction non‑locale mais non réutilisable. Cela fonctionne aussi pour les variables qui devraient être `const` mais seulement après un travail d’initialisation.

#### Exemple, mauvais  

```    
    widget x;   // devrait être const, mais :
    for (auto i = 2; i <= N; ++i) {          // cela pourrait être du code long
        x += some_obj.do_something_with(i);  // code arbitrairement long
    }                                        // à partir d’ici, x devrait être const, mais on ne peut pas le dire dans ce style
```  

#### Exemple, bon  

```    
    const widget x = [&] {
        widget val;                                // supposons que widget possède un constructeur par défaut
        for (auto i = 2; i <= N; ++i) {            // cela pourrait être du code long
            val += some_obj.do_something_with(i);  // code arbitrairement long
        }                                          // nécessaire pour initialiser x
        return val;
    }();
```  

Si possible, réduisez les conditions à un simple ensemble d’alternatives (par ex. un `enum`) et ne mélangez pas sélection et initialisation.

#### Application  

Difficile. Au mieux une heuristique. Recherchez une variable non initialisée suivie d’une boucle qui lui assigne des valeurs. @TODO-LINK  

---

### <a name="res-macros"></a>ES.30 : N’utilisez pas les macros pour manipuler le texte du programme  

#### Raison  

Les macros sont une source majeure de bugs.  
Les macros n’obéissent pas aux règles habituelles de portée et de type.  
Les macros font en sorte que le lecteur humain voit autre chose que ce que le compilateur voit.  
Les macros compliquent la construction d’outils.

#### Exemple, mauvais  

```    
    #define Case break; case   /* MAUVAIS */
```  

Cette macro apparemment inoffensive transforme un simple `c` minuscule en `C` majuscule, ce qui crée un bug de contrôle de flux.

#### Note  

Cette règle ne prohibe pas l’usage des macros pour le « contrôle de configuration » dans les `#ifdef`, etc.  
À l’avenir, les modules sont susceptibles d’éliminer le besoin de macros dans le contrôle de configuration.

#### Note  

Cette règle vise également à décourager l’usage de `#` pour la stringification et `##` pour la concaténation. Comme d’habitude pour les macros, il existe des usages « principalement sans danger », mais même ceux‑ci peuvent poser problème aux outils (auto‑complétion, analyseurs statiques, débogueurs). Souvent, le désir d’utiliser des macros sophistiquées indique un design excessivement complexe. De plus, `#` et `##` encouragent la définition et l’usage de macros :

```    
    #define CAT(a, b) a ## b
    #define STRINGIFY(a) #a

    void f(int x, int y)
    {
        string CAT(x, y) = "asdf";   // MAUVAIS : difficile à gérer pour les outils (et laid)
        string sx2 = STRINGIFY(x);
        // …
    }
```  

Il existe des solutions de contournement pour la manipulation low‑level de chaînes de caractères avec des macros. Par exemple :

```    
    enum E { a, b };

    template<int x>
    constexpr const char* stringify()
    {
        switch (x) {
        case a: return "a";
        case b: return "b";
        }
    }

    void f()
    {
        string s1 = stringify<a>();
        string s2 = stringify<b>();
        // …
    }
```  

Ce n’est pas aussi pratique qu’une macro, mais c’est tout aussi simple à utiliser, sans coût, typé et à portée.  

À l’avenir, la réflexion statique devrait éliminer le dernier besoin du préprocesseur pour la manipulation du texte du programme.

#### Application  

* Crier (ou émettre un diagnostic) lorsqu’une macro n’est pas uniquement utilisée pour le contrôle de source (par ex. `#ifdef`). @TODO-LINK  

---

### <a name="res-macros2"></a>ES.31 : N’utilisez pas les macros pour des constantes ou des « fonctions »  

#### Raison  

Les macros sont une source majeure de bugs.  
Les macros n’obéissent pas aux règles habituelles de portée et de type.  
Les macros n’obéissent pas aux règles habituelles de passage d’arguments.  
Les macros font en sorte que le lecteur humain voit autre chose que ce que le compilateur voit.  
Les macros compliquent la construction d’outils.

#### Exemple, mauvais  

```    
    #define PI 3.14
    #define SQUARE(a, b) (a * b)
```  

Même si nous n’avions pas laissé le bug bien connu dans `SQUARE`, il existe de bien meilleures alternatives :

```    
    constexpr double pi = 3.14;
    template<typename T> T square(T a, T b) { return a * b; }
```  

#### Application  

* Crier (ou émettre un diagnostic) lorsqu’une macro n’est pas uniquement utilisée pour le contrôle de source (par ex. `#ifdef`). @TODO-LINK  

---

### <a name="res-all_caps"></a>ES.32 : Utilisez `ALL_CAPS` pour tous les noms de macro  

#### Raison  

Convention. Lisibilité. Distinguer les macros.

#### Exemple  

```    
    #define forever for (;;)   /* très MAUVAIS */

    #define FOREVER for (;;)   /* Toujours mauvais, mais au moins visible aux humains */
```  

#### Application  

* Crier (ou émettre un diagnostic) lorsqu’une macro est en minuscule. @TODO-LINK  

---

### <a name="res-macros3"></a>ES.33 : Si vous devez utiliser des macros, donnez‑leur des noms uniques  

#### Raison  

Les macros n’obéissent pas aux règles de portée.

#### Exemple  

```    
    #define MYCHAR        /* MAUVAIS, finira par entrer en conflit avec le MYCHAR de quelqu’un d’autre */

    #define ZCORP_CHAR    /* Toujours mauvais, mais moins susceptible d’entrer en conflit */
```  

#### Note  

Évitez les macros si vous le pouvez : [ES.30](010-expr.md#res‑macros) @TODO-LINK, [ES.31](010-expr.md#res‑macros2) @TODO-LINK, et [ES.32](010-expr.md#res‑all_caps) @TODO-LINK. Cependant, des milliards de lignes de code sont parsemées de macros et une longue tradition d’utilisation et de sur‑utilisation subsiste. Si vous êtes contraint d’utiliser des macros, employez des noms longs et des préfixes supposés uniques (par ex. le nom de votre organisation) afin de réduire la probabilité d’un conflit.

#### Application  

* Avertir contre les noms de macro courts. @TODO-LINK  

---

### <a name="res-ellipses"></a>ES.34 : N’instanciez pas une fonction variadique de style C  

#### Raison  

Pas sûr du type. Nécessite du code cast‑et‑macro lourd pour fonctionner correctement.

#### Exemple  

```    
    #include <cstdarg>

    // « severity » suivi d’une liste terminée par zéro de char* ; écrit les chaînes C‑style sur cerr
    void error(int severity ...)
    {
        va_list ap;             // type magique pour tenir les arguments
        va_start(ap, severity); // démarrage des arguments : « severity » est le premier argument de error()

        for (;;) {
            // traite l’argument suivant comme un char* ; pas de vérification : un cast déguisé
            char* p = va_arg(ap, char*);
            if (!p) break;
            cerr << p << ' ';
        }

        va_end(ap);             // nettoyage des arguments (n’oubliez pas)

        cerr << '\n';
        if (severity) exit(severity);
    }

    void use()
    {
        error(7, "this", "is", "an", "error", nullptr);
        error(7); // crash
        error(7, "this", "is", "an", "error");  // crash
        const char* is = "is";
        string an = "an";
        error(7, "this", is, an, "error"); // crash
    }
```  

**Alternative** : surcharge, templates, templates variadiques.

```    
    #include <iostream>

    void error(int severity)
    {
        std::cerr << '\n';
        std::exit(severity);
    }

    template<typename T, typename... Ts>
    constexpr void error(int severity, T head, Ts... tail)
    {
        std::cerr << head;
        error(severity, tail...);
    }

    void use()
    {
        error(7); // Aucun crash !
        error(5, "this", "is", "not", "an", "error"); // Aucun crash !

        std::string an = "an";
        error(7, "this", "is", "not", an, "error"); // Aucun crash !

        error(5, "oh", "no", nullptr); // Erreur de compilation ! Pas de crash possible.
    }
```  

#### Note  

C’est essentiellement la façon dont `printf` est implémenté.

#### Application  

* Signaler les définitions de fonctions variadiques de type C.  
* Signaler les inclusions de `<cstdarg>` et `<stdarg.h>`. @TODO-LINK  

---  

## ES.expr : Expressions  

Les expressions manipulent des valeurs.

### <a name="res-complicated"></a>ES.40 : Évitez les expressions compliquées  

#### Raison  

Les expressions compliquées sont sources d’erreurs.

#### Exemple  

```    
    // mauvais : assignation cachée dans une sous‑expression
    while ((c = getc()) != -1)

    // mauvais : deux variables non locales assignées dans des sous‑expressions
    while ((cin >> c1, cin >> c2), c1 == c2)

    // meilleur, mais peut‑être encore trop compliqué
    for (char c1, c2; cin >> c1 >> c2 && c1 == c2;)

    // OK : si i et j ne sont pas aliasés
    int x = ++i + ++j;

    // OK : si i != j et i != k
    v[i] = v[j] + v[k];

    // mauvais : plusieurs assignations « cachées » dans des sous‑expressions
    x = a + (b = f()) + (c = g()) * 7;

    // mauvais : s’appuie sur des règles de priorité souvent mal comprises
    x = a & b + c * d && e ^ f == 7;

    // mauvais : comportement indéfini
    x = x++ + x++ + ++x;
```  

Certaines de ces expressions sont toujours mauvaises (elles s’appuient sur un comportement indéfini). D’autres sont simplement tellement compliquées / inhabituelles que même de bons programmeurs pourraient les mal comprendre ou en laisser passer un problème lorsqu’ils sont pressés.

#### Note  

C++17 resserre les règles d’ordre d’évaluation (de gauche à droite sauf de droite à gauche dans les assignations, et l’ordre d’évaluation des arguments de fonction reste non spécifié ; voir [ES.43](010-expr.md#res‑order)) ; cela ne change pas le fait que les expressions compliquées peuvent être source de confusion.

#### Note  

Un programmeur devrait connaître et appliquer les règles de base des expressions.

#### Exemple  

```    
    x = k * y + z;             // OK

    auto t1 = k * y;           // mauvais : inutilement verbeux
    x = t1 + z;

    if (0 <= x && x < max)    // OK

    auto t1 = 0 <= x;          // mauvais : inutilement verbeux
    auto t2 = x < max;
    if (t1 && t2)              // …
```  

#### Application  

Difficile. Combien d’opérateurs faut‑il avant de considérer une expression comme « compliquée » ? Écrire les calculs sous forme d’instructions avec une opération chacune est aussi source de confusion. Points à considérer :

* effets de bord : effets de bord sur plusieurs variables non locales (pour une certaine définition de « non locale ») peuvent être suspects, surtout si les effets de bord se trouvent dans des sous‑expressions séparées  
* écritures sur des variables aliasées  
* plus de N opérateurs (et quel N choisir ?)  
* recours à des règles de priorité subtiles  
* utilisation d’un comportement indéfini (pouvons‑nous tous les détecter ?)  
* comportement dépendant de l’implémentation ?  
* ???  

---

### <a name="res-parens"></a>ES.41 : En cas de doute sur la priorité des opérateurs, mettez des parenthèses  

#### Raison  

Éviter les erreurs. Lisibilité. Tout le monde ne connaît pas la table de priorités par cœur.

#### Exemple  

```    
    const unsigned int flag = 2;
    unsigned int a = flag;

    if (a & flag != 0)  // mauvais : signifie a&(flag != 0)
```  

Nous recommandons que les programmeurs connaissent la table de priorités pour les opérations arithmétiques, logiques, mais envisagent d’ajouter des parenthèses lorsqu’ils mélangent opérateurs bitwise et autres opérateurs.

```    
    if ((a & flag) != 0)  // OK : fonctionne comme prévu
```  

#### Note  

Vous ne devez pas forcément mettre de parenthèses pour :

```    
    if (a < 0 || a <= max) {
        // …
    }
```  

#### Application  

* Signaler les combinaisons d’opérateurs bitwise‑logiques avec d’autres opérateurs.  
* Signaler les opérateurs d’affectation qui ne sont pas l’opérateur le plus à gauche.  
* ???  

---

### <a name="res-ptr"></a>ES.42 : Gardez l’utilisation des pointeurs simple et directe  

#### Raison  

La manipulation compliquée de pointeurs est une source majeure d’erreurs.

#### Note  

Utilisez `gsl::span` à la place.  
Les pointeurs ne doivent **référencer qu’un seul objet** (005-interfaces.md#ri‑array).  
L’arithmétique de pointeurs est fragile et facile à mal faire, source de nombreux bogues et failles de sécurité.  
`span` est un type sûr, borné, pour accéder aux tableaux de données.  
Accéder à un tableau dont les limites sont connues à l’aide d’un indice constant peut être validé par le compilateur.

#### Exemple, mauvais  

```    
    void f(int* p, int count)
    {
        if (count < 2) return;

        int* q = p + 1;    // MAUVAIS

        ptrdiff_t d;
        int n;
        d = (p - &n);      // OK
        d = (q - p);      // OK

        int n = *p++;      // MAUVAIS

        if (count < 6) return;

        p[4] = 1;          // MAUVAIS

        p[count - 1] = 2;  // MAUVAIS

        use(&p[0], 3);     // MAUVAIS
    }
```  

#### Exemple, bon  

```    
    void f(span<int> a) // MIEUX : utilise span dans la déclaration de fonction
    {
        if (a.size() < 2) return;

        int n = a[0];      // OK

        span<int> q = a.subspan(1); // OK

        if (a.size() < 6) return;

        a[4] = 1;          // OK

        a[a.size() - 1] = 2;  // OK

        use(a.data(), 3);  // OK
    }
```  

#### Note  

L’indexation avec une variable est difficile à valider tant pour les outils que pour les humains. `span` fournit une vérification de limites à l’exécution. `at()` est une autre alternative qui garantit que chaque accès est contrôlé. Si vous avez besoin d’itérateurs pour accéder à un tableau, utilisez les itérateurs fournis par un `span` construit sur le tableau.

#### Exemple, mauvais  

```    
    void f(array<int, 10> a, int pos)
    {
        a[pos / 2] = 1; // MAUVAIS
        a[pos - 1] = 2; // MAUVAIS
        a[-1] = 3;    // MAUVAIS (mais facilement détecté par les outils) -- pas de remplacement, simplement ne pas le faire
        a[10] = 4;    // MAUVAIS (mais facilement détecté par les outils) -- pas de remplacement, simplement ne pas le faire
    }
```  

#### Exemple, bon  

Utilisez un `span` :

```    
    void f1(span<int, 10> a, int pos) // A1 : change le type de paramètre pour utiliser span
    {
        a[pos / 2] = 1; // OK
        a[pos - 1] = 2; // OK
    }

    void f2(array<int, 10> arr, int pos) // A2 : ajoute un span local et l’utilise
    {
        span<int> a = {arr.data(), pos};
        a[pos / 2] = 1; // OK
        a[pos - 1] = 2; // OK
    }
```  

Utilisez `at()` :

```    
    void f3(array<int, 10> a, int pos) // ALTERNATIVE B : utilise at() pour l’accès
    {
        at(a, pos / 2) = 1; // OK
        at(a, pos - 1) = 2; // OK
    }
```  

#### Exemple, mauvais  

```    
    void f()
    {
        int arr[COUNT];
        for (int i = 0; i < COUNT; ++i)
            arr[i] = i; // MAUVAIS, impossible d’utiliser un indexeur non constant
    }
```  

#### Exemple, bon  

Utilisez un `span` :

```    
    void f1()
    {
        int arr[COUNT];
        span<int> av = arr;
        for (int i = 0; i < COUNT; ++i)
            av[i] = i;
    }
```  

Utilisez un `span` et un `range‑for` :

```    
    void f1a()
    {
         int arr[COUNT];
         span<int, COUNT> av = arr;
         int i = 0;
         for (auto& e : av)
             e = i++;
    }
```  

Utilisez `at()` pour l’accès :

```    
    void f2()
    {
        int arr[COUNT];
        for (int i = 0; i < COUNT; ++i)
            at(arr, i) = i;
    }
```  

Utilisez un `range‑for` :

```    
    void f3()
    {
        int arr[COUNT];
        int i = 0;
        for (auto& e : arr)
             e = i++;
    }
```  

#### Note  

Les outils peuvent proposer des réécritures d’accès à des tableaux avec des index dynamiques pour utiliser `at()` à la place :

```    
    static int a[10];

    void f(int i, int j)
    {
        a[i + j] = 12;      // MAUVAIS, pourrait être réécrit en …
        at(a, i + j) = 12;  // OK — vérifié à l’exécution
    }
```  

#### Exemple  

Transformer un tableau en pointeur (comme le langage le fait essentiellement toujours) supprime les possibilités de vérification, donc évitez‑le :

```    
    void g(int* p);

    void f()
    {
        int a[5];
        g(a);        // MAUVAIS : essayons‑nous de passer un tableau ?
        g(&a[0]);    // OK : on passe un seul objet
    }
```  

Si vous voulez passer un tableau, dites‑le :

```    
    void g(int* p, size_t length);  // ancien code (dangereux)

    void g1(span<int> av); // MIEUX : modifiez g()
```  

```    
    void f2()
    {
        int a[5];
        span<int> av = a;

        g(av.data(), av.size());   // OK, si vous n’avez pas le choix
        g1(a);                     // OK — pas de décadence ici, utilisez le constructeur implicite de span
    }
```  

#### Application  

* Signaler toute opération arithmétique sur une expression de type pointeur qui produit une valeur de type pointeur.  
* Signaler toute expression d’indexation sur une expression ou variable de type tableau (tableau statique ou `std::array`) où l’indexeur n’est pas une expression constante comprise entre `0` et la borne supérieure du tableau.  
* Signaler toute expression qui dépendrait de la conversion implicite d’un type tableau en pointeur.  

Cette règle fait partie du **profil de sécurité des limites**[022-profile.md#ss‑bounds] @TODO-LINK  

---

### <a name="res-order"></a>ES.43 : Évitez les expressions dont l’ordre d’évaluation est indéfini  

#### Raison  

Vous ne savez pas ce que fait réellement ce code. Portabilité.  
Même si cela fait quelque chose de sensé pour vous, cela peut faire autre chose sur un autre compilateur (par ex. la prochaine version de votre compilateur) ou avec une optimisation différente.

#### Note  

C++17 resserre les règles d’ordre d’évaluation : de gauche à droite sauf de droite à gauche dans les assignations, et l’ordre d’évaluation des arguments de fonction reste non spécifié.

Cependant, souvenez‑vous que votre code peut être compilé avec un compilateur pré‑C++17 (par ex. via copier‑coller) ; ne soyez donc pas trop malin.

#### Exemple  

```    
    v[i] = ++i;   // le résultat est indéfini
```  

Une bonne règle de base est de ne pas lire une valeur deux fois dans une expression où vous écrivez dedans.

#### Application  

Peut être détecté par un bon analyseur. @TODO-LINK  

---

### <a name="res-order-fct"></a>ES.44 : Ne dépendez pas de l’ordre d’évaluation des arguments de fonction  

#### Raison  

Parce que cet ordre est non spécifié.

#### Note  

C++17 restreint les règles d’ordre d’évaluation, mais l’ordre d’évaluation des arguments de fonction reste non spécifié.

#### Exemple  

```    
    int i = 0;
    f(++i, ++i);
```  

Avant C++17 le comportement était indéfini, donc le résultat pouvait être n’importe quoi (par ex. `f(2, 2)`).  
Depuis C++17, ce code n’a pas de comportement indéfini, mais il n’est toujours pas spécifié quel argument est évalué en premier. L’appel sera `f(1, 2)` ou `f(2, 1)`, mais vous ne savez pas lequel.

#### Exemple  

Les opérateurs surchargés peuvent entraîner des problèmes d’ordre d’évaluation :

```    
    f1()->m(f2());          // m(f1(), f2())
    cout << f1() << f2();   // operator<<(operator<<(cout, f1()), f2())
```  

En C++17, ces exemples fonctionnent comme prévu (de gauche à droite) et les assignations sont évaluées de droite à gauche (tout comme la liaison de `=`).

```    
    f1() = f2();    // comportement indéfini en C++14 ; en C++17, f2() est évalué avant f1()
```  

#### Application  

Peut être détecté par un bon analyseur. @TODO-LINK  

---

### <a name="res-magic"></a>ES.45 : Évitez les « constantes magiques » ; utilisez des constantes symboliques  

#### Raison  

Les constantes non nommées intégrées aux expressions sont facilement oubliées et souvent difficiles à comprendre.

#### Exemple  

```    
    for (int m = 1; m <= 12; ++m)   // mauvais : constante magique 12
        cout << month[m] << '\n';
```  

Non, nous ne savons pas tous qu’il y a 12 mois, numérotés de 1 à 12, dans une année. Mieux :

```    
    // les mois sont indexés de 1 à 12
    constexpr int first_month = 1;
    constexpr int last_month = 12;

    for (int m = first_month; m <= last_month; ++m)   // meilleur
        cout << month[m] << '\n';
```  

Encore mieux, n’exposez pas les constantes :

```    
    for (auto m : month)
        cout << m << '\n';
```  

#### Application  

Signaler les littéraux dans le code. Faire une exception pour `0`, `1`, `nullptr`, `'\n'`, `""`, etc., sur une liste positive. @TODO-LINK  

---

### <a name="res-narrowing"></a>ES.46 : Évitez les conversions arithmétiques rétrécissantes (lossy)  

#### Raison  

Une conversion de rétrécissement détruit de l’information, souvent de façon inattendue.

#### Exemple, mauvais  

Un exemple clé est le rétrécissement de base :

```    
    double d = 7.9;
    int i = d;    // mauvais : rétrécissement ; i devient 7
    i = (int) d;  // mauvais : même remarque
```  

```    
    void f(int x, long y, double d)
    {
        char c1 = x;   // mauvais : rétrécissement
        char c2 = y;   // mauvais : rétrécissement
        char c3 = d;   // mauvais : rétrécissement
    }
```  

#### Note  

Le profil de directives de la bibliothèque de lignes directrices fournit une opération `narrow_cast` pour indiquer qu’un rétrécissement est acceptable et un `narrow` (« narrow if ») qui lève une exception si le rétrécissement entraînerait la perte de valeurs légales :

```    
    i = gsl::narrow_cast<int>(d);   // OK (vous l’avez demandé) : i devient 7
    i = gsl::narrow<int>(d);        // OK : lève narrowing_error
```  

Nous incluons également les casts arithmétiques lossys, comme la conversion d’un type flottant négatif en entier non signé :

```    
    double d = -7.9;
    unsigned u = 0;

    u = d;                               // mauvais : rétrécissement
    u = gsl::narrow_cast<unsigned>(d);   // OK (vous l’avez demandé) : u devient 4294967289
    u = gsl::narrow<unsigned>(d);        // OK : lève narrowing_error
```  

#### Note  

Cette règle ne s’applique pas aux **conversions contextuelles vers bool** :

```    
    if (ptr) do_something(*ptr);   // OK : ptr est utilisé comme condition
    bool b = ptr;                  // mauvais : rétrécissement
```  

#### Application  

Un bon analyseur peut détecter toutes les conversions de rétrécissement. Cependant, signaler toutes les conversions de rétrécissement entraînera de nombreux faux positifs. Suggestions :

* Signaler toutes les conversions de flottant à entier (peut‑être seulement `float`→`char` et `double`→`int`. Ici, il faut du dragon ! Nous avons besoin de données.)  
* Signaler toutes les conversions `long`→`char`. (Je soupçonne que `int`→`char` soit très fréquent. Ici, il faut du dragon ! Nous avons besoin de données.)  
* Considérer les conversions d’arguments de fonction comme particulièrement suspectes. @TODO-LINK  

---

### <a name="res-nullptr"></a>ES.47 : Utilisez `nullptr` plutôt que `0` ou `NULL`  

#### Raison  

Lisibilité. Minimiser les surprises : `nullptr` ne peut pas être confondu avec un `int`. `nullptr` possède également un type bien spécifié (très restrictif) et fonctionne donc dans davantage de scénarios où la déduction de type pourrait faire la mauvaise chose avec `NULL` ou `0`.

#### Exemple  

```    
    void f(int);
    void f(char*);
    f(0);         // appel f(int)
    f(nullptr);   // appel f(char*)
```  

#### Application  

* Signaler l’usage de `0` et `NULL` pour les pointeurs. La transformation pourra être aidée par une simple transformation de programme. @TODO-LINK  

---

### <a name="res-casts"></a>ES.48 : Évitez les casts  

#### Raison  

Les casts sont une source bien connue d’erreurs et rendent certaines optimisations incertaines.

#### Exemple, mauvais  

```    
    double d = 2;
    auto p = (long*)&d;
    auto q = (long long*)&d;
    cout << d << ' ' << *p << ' ' << *q << '\n';
```  

Que pensez‑vous que ce fragment imprime ? Le résultat est au mieux dépendant de l’implémentation. J’ai obtenu  

```    
    2 0 4611686018427387904
```  

Ajoutons  

```    
    *q = 666;
    cout << d << ' ' << *p << ' ' << *q << '\n';
```  

J’ai obtenu  

```    
    3.29048e-321 666 666
```  

Surpris ? C’est en fait un comportement indéfini, et cela pourrait également planter le programme.

#### Note  

Les programmeurs qui écrivent des casts supposent généralement qu’ils savent ce qu’ils font, ou que le cast rend le programme « plus lisible ». En fait, ils désactivent souvent les règles générales d’utilisation des valeurs. La résolution de surcharges et l’instanciation de templates choisissent habituellement la bonne fonction s’il existe une fonction adéquate. S’il n’y en a pas, il devrait y en avoir une ; alors, il vaut mieux éviter une solution locale (le cast).

#### Notes  

Les casts sont nécessaires dans un langage de programmation système. Par exemple, comment obtenons‑nous l’adresse d’un registre d’appareil dans un pointeur ? Cependant, les casts sont largement sur‑utilisés et constituent une source majeure d’erreurs.

Si vous avez besoin d’un grand nombre de casts, il y a probablement un problème de conception fondamental.

Le **profil de type**[022-profile.md#pro‑type‑reinterpretcast] interdit `reinterpret_cast` et les casts de style C.

Ne cast jamais à `(void)` pour ignorer la valeur de retour marquée `[[nodiscard]]`.  
Si vous voulez réellement ignorer un tel résultat, réfléchissez d’abord sérieusement pourquoi c’est une bonne idée (il y a généralement une bonne raison pour que l’auteur de la fonction ou du type de retour utilise `[[nodiscard]]`).  
Si vous pensez encore que c’est approprié et que votre réviseur de code est d’accord, utilisez `std::ignore =` pour désactiver l’avertissement ; c’est simple, portable et facile à rechercher.

#### Alternatives  

Les casts sont largement (mal) utilisés. Le C++ moderne possède des règles et constructions qui éliminent le besoin de casts dans de nombreux contextes, tels que :

* Utilisez les templates  
* Utilisez `std::variant`  
* Comptez sur les conversions implicites sûres entre types de pointeurs  
* Utilisez `std::ignore =` pour ignorer les valeurs `[[nodiscard]]`

#### Application  

* Signaler tous les casts de style C, y compris vers `void`.  
* Signaler les casts de style fonctionnel utilisant `Type(value)`. Utilisez `Type{value}` à la place, qui n’est pas un rétrécissement. (Voir [ES.64](010-expr.md#res‑construct).)  
* Signaler les **identity casts** (022-profile.md#pro‑type‑identitycast) entre types pointeurs où le type source et le type cible sont identiques.  
* Signaler un cast explicite de pointeur qui pourrait être **implicite** (022-profile.md#pro‑type‑implicitpointercast). @TODO-LINK  

---

### <a name="res-casts-named"></a>ES.49 : Si vous devez caster, utilisez un cast nommé  

#### Raison  

Lisibilité. Évitement d’erreurs.  
Les casts nommés sont plus spécifiques qu’un cast de style C ou fonctionnel, ce qui permet au compilateur d’intercepter certaines erreurs.

Les casts nommés sont :

* `static_cast`  
* `const_cast`  
* `reinterpret_cast`  
* `dynamic_cast`  
* `std::move` // `move(x)` est une référence rvalue à `x`  
* `std::forward` // `forward<T>(x)` est une référence lvalue ou rvalue à `x` selon `T`  
* `gsl::narrow_cast` // `narrow_cast<T>(x)` est équivalent à `static_cast<T>(x)`  
* `gsl::narrow` // `narrow<T>(x)` est `static_cast<T>(x)` si `static_cast<T>(x) == x` sinon il lève `narrowing_error`

#### Exemple  

```    
    class B { /* … */ };
    class D { /* … */ };

    D* downcast(B* pb)
    {
        D* pd0 = pb;                        // erreur : aucune conversion implicite de B* vers D*
        D* pd1 = (D*)pb;                    // légal, mais que fait‑on ?
        D* pd2 = static_cast<D*>(pb);       // erreur : D n’est pas dérivé de B
        D* pd3 = reinterpret_cast<D*>(pb);  // OK : à vos risques et périls !
        D* pd4 = dynamic_cast<D*>(pb);      // OK : renvoie nullptr
        // …
    }
```  

L’exemple provient de bugs réels où `D` était dérivé de `B`, mais quelqu’un a refactorisé la hiérarchie. Le cast de style C est dangereux parce qu’il peut effectuer n’importe quel type de conversion, nous privant de toute protection contre les erreurs (aujourd’hui ou demain).

#### Note  

Lorsque vous convertissez entre des types sans perte d’information (par ex. de `float` à `double` ou de `int32` à `int64`), l’initialisation par accolades peut être utilisée à la place.

```    
    double d {some_float};
    int64_t i {some_int32};
```  

Cela rend clair que la conversion de type était intentionnelle et empêche également les conversions entre types qui pourraient entraîner une perte de précision. (Il s’agit d’une erreur de compilation d’essayer d’initialiser un `float` à partir d’un `double` dans cette forme, par exemple.)

#### Note  

`reinterpret_cast` peut être essentiel, mais les usages essentiels (par ex. transformer une adresse machine en pointeur) ne sont pas sûrs du tout :

```    
    auto p = reinterpret_cast<Device_register>(0x800);  // intrinsèquement dangereux
```  

#### Application  

* Signaler tous les casts de style C, y compris vers `void`.  
* Signaler les casts de style fonctionnel utilisant `Type(value)`. Utilisez `Type{value}` à la place, qui n’est pas un rétrécissement. (Voir [ES.64](010-expr.md#res‑construct).)  
* Le **profil de type**[022-profile.md#pro‑type‑reinterpretcast] interdit `reinterpret_cast`.  
* Le **profil de type**[022-profile.md#pro‑type‑arithmeticcast] avertit lorsqu’on utilise `static_cast` entre types arithmétiques. @TODO-LINK  

---

### <a name="res-casts-const"></a>ES.50 : Ne retirez pas le `const` avec un cast  

#### Raison  

Cela ment au sujet du `const`.  
Si la variable est réellement déclarée `const`, la modifier entraîne un comportement indéfini.

#### Exemple, mauvais  

```    
    void f(const int& x)
    {
        const_cast<int&>(x) = 42;   // MAUVAIS
    }

    static int i = 0;
    static const int j = 0;

    f(i); // effet secondaire silencieux
    f(j); // comportement indéfini
```  

#### Exemple  

Parfois, on peut être tenté d’utiliser `const_cast` pour éviter la duplication de code, par exemple lorsque deux fonctions d’accès qui diffèrent uniquement par le const‑ness ont des implémentations similaires. Par exemple :

```    
    class Bar;

    class Foo {
    public:
        // MAUVAIS, duplique la logique
        Bar& get_bar()
        {
            /* logique complexe pour obtenir une référence non‑const à my_bar */
        }

        const Bar& get_bar() const
        {
            /* même logique complexe pour obtenir une référence const à my_bar */
        }
    private:
        Bar my_bar;
    };
```  

Il vaut mieux partager les implémentations. Normalement, vous pouvez simplement faire appeler la fonction non‑`const` la fonction `const`. Cependant, lorsque la logique est complexe, cela peut conduire au patron suivant qui recourt encore à `const_cast` :

```    
    class Foo {
    public:
        // pas idéal, non‑const appelle const mais utilise const_cast
        Bar& get_bar()
        {
            return const_cast<Bar&>(static_cast<const Foo&>(*this).get_bar());
        }
        const Bar& get_bar() const
        {
            /* même logique complexe autour de l’obtention de my_bar */
        }
    private:
        Bar my_bar;
    };
```  

Ce patron est sûr lorsqu’il est appliqué correctement, car l’appelant doit avoir un objet non‑`const` au départ, mais ce n’est pas idéal parce que la sécurité est difficile à faire appliquer automatiquement comme règle de vérificateur.

À la place, placez le code commun dans une fonction auxiliaire — et rendez‑la un template afin qu’elle déduise le `const`. Cela n’utilise aucun `const_cast` :

```    
    class Foo {
    public:                         // bon
              Bar& get_bar()       { return get_bar_impl(*this); }
        const Bar& get_bar() const { return get_bar_impl(*this); }
    private:
        Bar my_bar;

        template<class T>           // bon, déduit si T est const ou non‑const
        static auto& get_bar_impl(T& t)
            { /* logique complexe autour de l’obtention d’une référence possiblement const à my_bar */ }
    };
```  

Note : Ne placez pas de travail non dépendant de template important ici, cela engendre du code bloat. Par exemple, une amélioration supplémentaire serait de faire en sorte qu’une partie ou la totalité de `get_bar_impl` soit non dépendante et soit facturée hors du template, ce qui pourrait réduire sensiblement la taille du code.

#### Exception  

Vous pouvez avoir besoin de retirer le `const` lors de l’appel à des fonctions qui ne sont pas correctement `const`‑correctes. Préférez envelopper de telles fonctions dans des wrappers inline `const`‑corrects afin de centraliser le cast en un seul endroit.

#### Exemple  

Parfois, « retirer le `const` » sert à mettre à jour des informations transitoires d’un objet autrement immutable. Exemples : cache, mémoïsation, pré‑calcul. Ces cas sont souvent mieux gérés à l’aide de `mutable` ou d’une indirection plutôt qu’avec `const_cast`.

Exemple d’utilisation d’un cache :

```    
    int compute(int x); // calcule une valeur pour x ; supposé coûteux

    class Cache {   // type implémentant un cache pour une opération int→int
    public:
        pair<bool, int> find(int x) const;   // y a‑t‑il une valeur pour x ?
        void set(int x, int v);             // insérer la valeur x
        // …
    private:
        // …
    };

    class X {
    public:
        int get_val(int x)
        {
            auto p = cache.find(x);
            if (p.first) return p.second;
            int val = compute(x);
            cache.set(x, val); // insérer la valeur
            return val;
        }
        // …
    private:
        Cache cache;
    };
```  

Ici, `get_val()` est logiquement `const`, nous aimerions donc le déclarer `const`. Pour ce faire, nous devons encore muter `cache`, donc certaines personnes utilisent un `const_cast` :

```    
    class X {   // solution suspecte basée sur le cast
    public:
        int get_val(int x) const
        {
            auto p = cache.find(x);
            if (p.first) return p.second;
            int val = compute(x);
            const_cast<Cache&>(cache).set(x, val);   // laid
            return val;
        }
        // …
    private:
        Cache cache;
    };
```  

Heureusement, il y a une meilleure solution : déclarer `cache` comme `mutable` même pour un objet `const` :

```    
    class X {   // meilleure solution
    public:
        int get_val(int x) const
        {
            auto p = cache.find(x);
            if (p.first) return p.second;
            int val = compute(x);
            cache.set(x, val);
            return val;
        }
        // …
    private:
        mutable Cache cache;
    };
```  

Une solution alternative serait de stocker un pointeur vers le `cache` :

```    
    class X {   // OK, mais légèrement plus compliqué
    public:
        int get_val(int x) const
        {
            auto p = cache->find(x);
            if (p.first) return p.second;
            int val = compute(x);
            cache->set(x, val);
            return val;
        }
        // …
    private:
        unique_ptr<Cache> cache;
    };
```  

Cette solution est la plus flexible, mais nécessite une construction et destruction explicites de `*cache` (probablement dans le constructeur et le destructeur de `X`).

Dans toutes les variantes, il faut protéger contre les data races sur le `cache` en code multithread, éventuellement à l’aide d’un `std::mutex`.

#### Application  

* Signaler les `const_cast`.  
* Cette règle fait partie du **profil de sécurité de type**[022-profile.md#pro‑type‑constcast] pour le profil associé. @TODO-LINK  

---

### <a name="res-range-checking"></a>ES.55 : Évitez le besoin de vérifications d’intervalle  

#### Raison  

Les constructions qui ne peuvent pas déborder ne débordent pas (et sont généralement plus rapides).

#### Exemple  

```    
    for (auto& x : v)      // imprime tous les éléments de v
        cout << x << '\n';

    auto p = find(v, x);   // trouve x dans v
```  

#### Application  

Cherchez les vérifications d’intervalle explicites et suggérez heuristiquement des alternatives. @TODO-LINK  

---

### <a name="res-move"></a>ES.56 : N’écrivez `std::move()` que lorsque vous devez réellement déplacer explicitement un objet vers une autre portée  

#### Raison  

Nous déplaçons, plutôt que de copier, pour éviter la duplication et améliorer les performances.  
Un déplacement laisse généralement derrière lui un objet vide ([C.64](007-class.md#rc‑move‑semantic)), ce qui peut être surprenant voire dangereux, donc nous essayons d’éviter de déplacer des l‑values (elles pourraient être ré‑utilisées plus tard).

#### Notes  

Le déplacement se fait implicitement lorsque la source est une r‑value (par ex. une valeur retournée ou le résultat d’une fonction), donc ne compliquez pas inutilement le code dans ces cas en écrivant `move` explicitement. Écrivez plutôt de petites fonctions qui retournent des valeurs ; le retour de la fonction et l’acceptation de ce retour seront naturellement optimisés.

En général, suivre les lignes directrices de ce document (notamment ne pas élargir inutilement les portées des variables, écrire de courtes fonctions qui retournent des valeurs, retourner des variables locales) aide à éliminer la plupart des besoins en `std::move` explicite.  

`std::move` est nécessaire uniquement pour déplacer explicitement un objet vers une autre portée, notamment pour le passer à une fonction « sink » et dans les implémentations de ses propres opérations de déplacement (constructeur de déplacement, opérateur d’affectation de déplacement) et d’échange.

#### Exemple, mauvais  

```    
    void sink(X&& x);   // sink prend possession de x

    void user()
    {
        X x;
        // erreur : ne peut pas lier un l‑value à une référence r‑value
        sink(x);
        // OK : sink prend le contenu de x, x doit maintenant être considéré comme vide
        sink(std::move(x));

        // ...

        // probablement une erreur
        use(x);
    }
```  

Habituellement, `std::move()` est utilisé comme argument d’un paramètre `&&`. Après cela, supposez que l’objet a été déplacé (voir [C.64](007-class.md#rc‑move‑semantic)) et ne lisez plus son état tant que vous ne l’avez pas d’abord ré‑initialisé.

```    
    void f()
    {
        string s1 = "supercalifragilisticexpialidocious";

        string s2 = s1;             // OK, copie
        assert(s1 == "supercalifragilisticexpialidocious");  // OK

        // mauvais, si vous voulez garder la valeur de s1
        string s3 = move(s1);

        // mauvais, l’assertion échouera probablement, s1 a probablement changé
        assert(s1 == "supercalifragilisticexpialidocious");
    }
```  

#### Exemple  

```    
    void sink(unique_ptr<widget> p);  // passe la propriété de p à sink()

    void f()
    {
        auto w = make_unique<widget>();
        // ...
        sink(std::move(w));               // ok, donne à sink()
        // ...
        sink(w);    // Erreur : unique_ptr est conçu pour ne pas pouvoir être copié
    }
```  

#### Notes  

`std::move()` est un cast vers `&&` déguisé ; il ne déplace rien en soi, il marque simplement un objet nommé comme candidat pouvant être déplacé. Le langage connaît déjà les cas courants où les objets peuvent être déplacés, surtout lorsqu’on retourne des valeurs de fonctions, donc n’encombrez pas le code avec des `std::move()` redondants.

Ne jamais écrire `std::move()` simplement parce que vous avez entendu « c’est plus efficace ».  
En général, ne croyez pas les affirmations d’« efficacité » sans données (???).  
En général, ne compliquez pas votre code sans raison (??).  
Ne jamais écrire `std::move()` sur un objet `const` ; il sera silencieusement transformé en copie (voir Item 23 dans [Meyers15](032-bibliography.md#Meyers15)).

#### Exemple, mauvais  

```    
    vector<int> make_vector()
    {
        vector<int> result;
        // ... charger result avec des données
        return std::move(result);       // mauvais ; écrivez simplement « return result; »
    }
```  

Ne jamais écrire `return move(local_variable);`, car le langage sait déjà que la variable est un candidat au déplacement. Écrire `move` ici n’aide pas, et peut même être préjudiciable car sur certains compilateurs cela interfère avec le RVO (optimisation de retour) en créant une référence supplémentaire à la variable locale.

#### Exemple, mauvais  

```    
    vector<int> v = std::move(make_vector());   // mauvais ; le std::move est entièrement redondant
```  

Ne jamais écrire `move` sur une valeur retournée telle que `x = move(f());` où `f` retourne par valeur. Le langage sait déjà que la valeur retournée est un objet temporaire pouvant être déplacé.

#### Exemple  

```    
    void mover(X&& x)
    {
        call_something(std::move(x));         // ok
        call_something(std::forward<X>(x));   // mauvais, ne pas std::forward un r‑value reference
        call_something(x);                    // suspect, pourquoi pas std::move ?
    }

    template<class T>
    void forwarder(T&& t)
    {
        call_something(std::move(t));         // mauvais, ne pas std::move une référence d’expédition
        call_something(std::forward<T>(t));   // ok
        call_something(t);                    // suspect, pourquoi pas std::forward ?
    }
```  

#### Application  

* Signaler l’usage de `std::move(x)` où `x` est une r‑value ou le langage le traitera déjà comme r‑value, y compris `return std::move(local_variable);` et `std::move(f())` sur une fonction qui retourne par valeur.  
* Signaler les fonctions qui prennent un paramètre `S&&` s’il n’existe pas de surcharge `const S&` pour accepter les l‑values.  
* Signaler un argument déplacé (`std::move`) passé à un paramètre, sauf si le type du paramètre est une référence r‑value `X&&` ou si le type est move‑only et le paramètre est passé par valeur.  
* Signaler quand `std::move` est appliqué à une référence d’expédition (`T&&` où `T` est un paramètre de modèle). Utilisez `std::forward` à la place.  
* Signaler quand `std::move` est appliqué à autre chose qu’une référence r‑value à un type non‑const. (Cas plus général de la règle précédente pour couvrir les cas non‑d’expédition.)  
* Signaler quand `std::forward` est appliqué à une référence r‑value (`X&&` où `X` n’est pas un paramètre de modèle). Utilisez `std::move` à la place.  
* Signaler quand `std::forward` est appliqué à autre chose qu’une référence d’expédition. (Cas plus général de la règle précédente.)  
* Signaler quand un objet est potentiellement déplacé et que l’opération suivante est une opération `const` ; il devrait d’abord y avoir une opération non‑`const`, idéalement une assignation, pour réinitialiser la valeur de l’objet. @TODO-LINK  

---

### <a name="res-new"></a>ES.60 : Évitez `new` et `delete` en dehors des fonctions de gestion de ressources  

#### Raison  

La gestion directe des ressources dans le code applicatif est source d’erreurs et fastidieuse.

#### Note  

C’est aussi connu sous le nom de règle « No naked `new`! ».

#### Exemple, mauvais  

```    
    void f(int n)
    {
        auto p = new X[n];   // n X‑s par défaut construits
        // …
        delete[] p;
    }
```  

Il peut y avoir du code dans la partie `…` qui empêche que le `delete` soit jamais exécuté.

**Voir aussi** : [R : Gestion des ressources](009-resource.md) @TODO-LINK  

#### Application  

* Signaler les `new` bruts et les `delete` bruts. @TODO-LINK  

---

### <a name="res-del"></a>ES.61 : Supprimez les tableaux avec `delete[]` et les non‑tableaux avec `delete`  

#### Raison  

C’est ce que le langage impose, et les incompatibilités peuvent entraîner des erreurs de libération de ressources et/ou corruption mémoire.

#### Exemple, mauvais  

```    
    void f(int n)
    {
        auto p = new X[n];   // n X‑s par défaut construits
        // …
        delete p;   // erreur : on supprime l’objet p, pas le tableau p[]
    }
```  

#### Note  

Cet exemple viole non seulement la règle « no naked `new` » précédente, mais comporte de nombreux autres problèmes.

#### Application  

* Signaler les `new`/`delete` incompatibles s’ils sont dans la même portée.  
* Signaler les `new`/`delete` incompatibles s’ils sont dans une paire constructeur/destructeur. @TODO-LINK  

---

### <a name="res-arr2"></a>ES.62 : Ne comparez pas des pointeurs provenant de différents tableaux  

#### Raison  

Le résultat est indéfini.

#### Exemple, mauvais  

```    
    void f()
    {
        int a1[7];
        int a2[9];
        if (&a1[5] < &a2[7]) {}       // mauvais : indéfini
        if (0 < &a1[5] - &a2[7]) {}   // mauvais : indéfini
    }
```  

#### Note  

Cet exemple comporte bien d’autres problèmes.

#### Application  

??? @TODO-LINK  

---

### <a name="res-slice"></a>ES.63 : Ne faites pas de slicing  

#### Raison  

Le slicing—copier seulement une partie d’un objet via assignation ou initialisation—conduit le plus souvent à des erreurs parce que l’objet était censé être considéré dans sa totalité. Dans les rares cas où le slicing était intentionnel, le code peut être surprenant.

#### Note  

Il n’est pas possible de copier une partie d’un objet vide, donc cette définition de slicing exclut délibérément les objets vides (sans membres non‑statiques), comme les types vides utilisés pour le tag‑dispatch.

#### Exemple  

```    
    class Shape { /* … */ };
    class Circle : public Shape { /* … */ Point c; int r; };

    Circle c { {0, 0}, 42 };
    Shape s {c};    // copie seulement la partie Shape de Circle
    s = c;          // ou copie‑assignation seulement de la partie Shape de Circle

    void assign(const Shape& src, Shape& dest)
    {
        dest = src;
    }
    Circle c2 { {1, 1}, 43 };
    assign(c, c2);   // oups, pas tout l’état transféré
    assert(c == c2); // si on fournit un opérateur de comparaison, il renverra probablement false
```  

Le résultat serait dénué de sens parce que le centre et le rayon ne sont pas copiés de `c` vers `s`. La première défense contre cela consiste à **définir la classe de base `Shape` de façon à ne pas autoriser cela**[007-class.md#rc‑copy‑virtual].

#### Alternative  

Si vous voulez faire du slicing, définissez une opération explicite pour le faire. Cela évite aux lecteurs la confusion. Par exemple :

```    
    class Smiley : public Circle {
        public:
        Circle copy_circle();
        // …
    };

    Smiley sm { /* … */ };
    Circle c1 {sm};  // idéalement empêché par la définition de Circle
    Circle c2 {sm.copy_circle()}; // OK
```  

#### Application  

* Avertir lorsqu’un slicing est détecté si le type de base possède des membres non‑statiques (éventuellement via les bases transitive). @TODO-LINK  

---

### <a name="res-construct"></a>ES.64 : Utilisez la notation `T{e}` pour la construction  

#### Raison  

La syntaxe de construction `T{e}` rend explicite le désir de construction.  
`T{e}` n’autorise pas le rétrécissement.  
`T{e}` est l’expression sûre et générale pour construire une valeur de type `T` à partir d’une expression `e`.  
Les notations de cast `T(e)` et `(T)e` ne sont ni sûres ni générales.

#### Exemple  

Pour les types intégrés, la notation de construction protège contre le rétrécissement et la réinterprétation :

```    
    void use(char ch, int i, double d, char* p, long long lng)
    {
        int x1 = int{ch};     // OK, mais redondant
        int x2 = int{d};      // erreur : double→int rétrécissant ; utilisez un cast si nécessaire
        int x3 = int{p};      // erreur : pointeur→int ; utilisez reinterpret_cast si besoin
        int x4 = int{lng};    // erreur : long long→int rétrécissant ; utilisez un cast si nécessaire

        int y1 = int(ch);     // OK, mais redondant
        int y2 = int(d);      // mauvais : double→int rétrécissant ; utilisez un cast si nécessaire
        int y3 = int(p);      // mauvais : pointeur→int ; utilisez reinterpret_cast si besoin
        int y4 = int(lng);    // mauvais : long long→int rétrécissant ; utilisez un cast si nécessaire

        int z1 = (int)ch;     // OK, mais redondant
        int z2 = (int)d;      // mauvais : double→int rétrécissant ; utilisez un cast si nécessaire
        int z3 = (int)p;      // mauvais : pointeur→int ; utilisez reinterpret_cast si besoin
        int z4 = (int)lng;    // mauvais : long long→int rétrécissant ; utilisez un cast si nécessaire
    }
```  

Les conversions entier↔pointeur sont implémentation‑dépendantes avec les notations `T(e)` ou `(T)e`, et non portables entre plateformes où les tailles d’entier et de pointeur diffèrent.

#### Note  

[Évitez les casts](010-expr.md#res‑casts) (conversion de type explicite) et, si vous devez absolument caster, **préférez les casts nommés** (voir [ES.49](010-expr.md#res‑casts‑named)).  

#### Note  

Lorsque c’est non ambigu, le `T` peut être omis de `T{e}`.

```    
    complex<double> f(complex<double>);

    auto z = f({2*pi, 1});
```  

#### Note  

La notation de construction est la plus générale des **notations d’initialisation**[010-expr.md#res‑list].

#### Exception  

`std::vector` et d’autres conteneurs ont été définis avant que nous ayons `{}` comme notation de construction. Considérez :

```    
    vector<string> vs {10};                           // dix chaînes vides
    vector<int> vi1 {1, 2, 3, 4, 5, 6, 7, 8, 9, 10};  // dix éléments 1…10
    vector<int> vi2 {10};                             // un élément de valeur 10
```  

Comment obtenir un `vector` de 10 `int` par défaut ?

```    
    vector<int> v3(10); // dix éléments de valeur 0
```  

L’usage de `()` plutôt que `{}` pour le nombre d’éléments est une tradition (années 1980), difficile à changer, mais c’est tout de même une **erreur de design** : pour un conteneur où le type d’élément peut être confondu avec le nombre d’éléments, nous avons une ambiguïté qui doit être résolue. La résolution conventionnelle consiste à interpréter `{10}` comme une liste d’un seul élément et à utiliser `(10)` pour distinguer la taille.

Cette erreur ne doit plus être reproduite dans le nouveau code. Nous pouvons définir un type pour représenter le nombre d’éléments :

```    
    struct Count { int n; };

    template<typename T>
    class Vector {
    public:
        Vector(Count n);                     // n éléments par défaut initialisés
        Vector(initializer_list<T> init);    // init.size() éléments
        // …
    };
```  

```    
    Vector<int> v1{10};
    Vector<int> v2{Count{10}};
    Vector<Count> v3{Count{10}};    // oui, il reste un problème mineur
```  

Le problème majeur restant est de trouver un nom adéquat pour `Count`.

#### Application  

* Signaler les casts de type C‑style `(T)e` et les casts fonctionnels `T(e)`. @TODO-LINK  

---

### <a name="res-deref"></a>ES.65 : Ne déréférencez pas un pointeur invalide  

#### Raison  

Déréférencer un pointeur invalide, tel que `nullptr`, entraîne un comportement indéfini, généralement un crash immédiat, des résultats erronés ou une corruption mémoire.

#### Note  

Par « pointeur », on entend toute forme d’indirection vers un objet, y compris les itérateurs ou vues équivalentes.

#### Note  

Cette règle est évidente et bien connue, mais son respect peut être difficile. Il faut une bonne discipline de codage, le support de bibliothèques et une analyse statique pour éliminer les violations sans un coût majeur. Cela constitue une partie importante de la discussion sur le **modèle de sûreté de type et de ressources** de C++[032-bibliography.md#Stroustrup15].

**Voir aussi** :

* Utilisez [RAII](009-resource.md#rr‑raii) pour éviter les problèmes de durée de vie.  
* Utilisez [unique_ptr](006-functions.md#rf‑unique_ptr) pour éviter les problèmes de durée de vie.  
* Utilisez [shared_ptr](006-functions.md#rf‑shared_ptr) pour éviter les problèmes de durée de vie.  
* Utilisez [references](006-functions.md#rf‑ptr‑ref) quand `nullptr` n’est pas une possibilité.  
* Utilisez [not_null](006-functions.md#rf‑nullptr) pour détecter `nullptr` tôt.  
* Utilisez le **profil de limites**[022-profile.md#ss‑bounds] pour éviter les erreurs d’intervalle.

#### Exemple  

```    
    void f()
    {
        int x = 0;
        int* p = &x;

        if (condition()) {
            int y = 0;
            p = &y;
        } // invalide p

        *p = 42;            // MAUVAIS, p pourrait être invalide si le branchement a été pris
    }
```  

Pour résoudre le problème, soit prolongez la durée de vie de l’objet auquel le pointeur doit se référer, soit raccourcissez la durée de vie du pointeur (déplacez la déréférence avant la fin de vie de l’objet pointé).

```    
    void f1()
    {
        int x = 0;
        int* p = &x;

        int y = 0;
        if (condition()) {
            p = &y;
        }

        *p = 42;            // OK, p pointe sur x ou y et les deux sont encore en portée
    }
```  

Malheureusement, la plupart des problèmes de pointeur invalide sont plus difficiles à repérer et à réparer.

#### Exemple  

```    
    void f(int* p)
    {
        int x = *p; // MAUVAIS : comment savons‑nous que p est valide ?
    }
```  

Il existe une quantité énorme de ce type de code. La plupart du temps—après de nombreux tests—ça fonctionne, mais de façon isolée il est impossible de savoir si `p` peut être `nullptr`.  

Il y a de nombreuses approches :

```    
    void f1(int* p) // gérer nullptr
    {
        if (!p) {
            // gérer nullptr (allouer, retourner, lancer, etc.)
        }
        int x = *p;
    }
```  

Les deux problèmes potentiels de tester `nullptr` :

* il n’est pas toujours évident que faire si on trouve `nullptr`  
* le test peut être redondant et/ou relativement coûteux  
* il n’est pas clair si le test sert à protéger contre une violation ou fait partie de la logique requise.

```    
    void f2(int* p) // déclarer que p ne doit pas être nullptr
    {
        assert(p);
        int x = *p;
    }
```  

Cela n’a un coût que lorsque les assertions sont activées et fournit aux analyseurs un indice utile. Cela fonctionnerait encore mieux si C++ proposait un support direct pour les contrats :

```    
    void f3(int* p) // déclarer que p ne doit pas être nullptr
        [[expects: p]]
    {
        int x = *p;
    }
```  

Ou encore, utilisez `gsl::not_null` pour garantir que `p` n’est pas `nullptr` :

```    
    void f(not_null<int*> p)
    {
        int x = *p;
    }
```  

Ces remèdes ne concernent que `nullptr`. Rappelez‑vous qu’il existe d’autres façons d’obtenir un pointeur invalide.

#### Exemple  

```    
    void f(int* p)  // code ancien, n’utilise pas de propriétaire
    {
        delete p;
    }

    void g()        // code ancien : utilise naked new
    {
        auto q = new int{7};
        f(q);
        int x = *q; // MAUVAIS : déréférence d’un pointeur invalide
    }
```  

#### Exemple  

```    
    void f()
    {
        vector<int> v(10);
        int* p = &v[5];
        v.push_back(99); // pourrait réallouer les éléments de v
        int x = *p; // MAUVAIS : déréférence d’un pointeur potentiellement invalide
    }
```  

#### Application  

Cette règle fait partie du **profil de sûreté de durée de vie**[022-profile.md#ss‑lifetime] @TODO-LINK  

* Signaler une déréférence d’un pointeur qui pointe vers un objet sorti de sa portée.  
* Signaler une déréférence d’un pointeur qui pourrait avoir été invalidé en lui assignant `nullptr`.  
* Signaler une déréférence d’un pointeur qui pourrait avoir été invalidé par un `delete`.  
* Signaler une déréférence d’un pointeur vers un élément de conteneur qui pourrait avoir été invalidé par la déréférence du conteneur. @TODO-LINK  

---

## ES.stmt : Instructions  

Les instructions contrôlent le flux (à l’exception des appels de fonction et des lancers d’exception, qui sont des expressions).

### <a name="res-switch-if"></a>ES.70 : Préférez un `switch` à un `if` lorsqu’il y a un choix  

#### Raison  

* Lisibilité.  
* Efficacité : un `switch` compare des constantes et est généralement mieux optimisé que plusieurs tests dans une chaîne `if‑then‑else`.  
* Un `switch` permet certaines vérifications heuristiques. Par exemple, toutes les valeurs d’une `enum` ont‑elles été couvertes ? Si non, y a‑t‑il un `default` ?

#### Exemple  

```    
    void use(int n)
    {
        switch (n) {   // bon
        case 0:
            // …
            break;
        case 7:
            // …
            break;
        default:
            // …
            break;
        }
    }
```  

plutôt que :

```    
    void use2(int n)
    {
        if (n == 0)   // mauvais : chaîne `if‑then‑else` comparant des constantes
            // …
        else if (n == 7)
            // …
    }
```  

#### Application  

* Signaler les chaînes `if‑then‑else` qui comparent contre des constantes (uniquement). @TODO-LINK  

---

### <a name="res-for-range"></a>ES.71 : Préférez un `for`‑range à un `for` classique lorsqu’il y a un choix  

#### Raison  

Lisibilité. Prévention d’erreurs. Efficacité.

#### Exemple  

```    
    for (gsl::index i = 0; i < v.size(); ++i)   // mauvais
        cout << v[i] << '\n';

    for (auto p = v.begin(); p != v.end(); ++p)   // mauvais
        cout << *p << '\n';

    for (auto& x : v)    // OK
        cout << x << '\n';

    for (gsl::index i = 1; i < v.size(); ++i) // touche deux éléments : ne peut pas être un range‑for
        cout << v[i] + v[i - 1] << '\n';

    for (gsl::index i = 0; i < v.size(); ++i) // possible effet de bord : ne peut pas être un range‑for
        cout << f(v, &v[i]) << '\n';

    for (gsl::index i = 0; i < v.size(); ++i) { // le corps modifie la variable de boucle : ne peut pas être un range‑for
        if (i % 2 != 0)
            cout << v[i] << '\n'; // sortie des éléments impairs
    }
```  

Un humain ou un bon analyseur statique pourrait déterminer qu’il n’y a réellement aucun effet de bord sur `v` dans `f(v, &v[i])` afin que la boucle puisse être réécrite.

« Modifier la variable de boucle » dans le corps d’une boucle est généralement à éviter.

#### Note  

Ne copiez pas de façon coûteuse la variable de boucle d’un `range‑for` :

```    
    for (string s : vs) // …
```  

Cela copiera chaque élément de `vs` dans `s`. Mieux :

```    
    for (string& s : vs) // …
```  

Encore mieux, si la variable de boucle n’est ni modifiée ni copiée :

```    
    for (const string& s : vs) // …
```  

#### Application  

* Rechercher les boucles ; si une boucle traditionnelle ne fait qu’itérer chaque élément d’une séquence et qu’il n’y a pas d’effets de bord sur les éléments, réécrivez‑la en boucle `range‑for`. @TODO-LINK  

---

### <a name="res-for-while"></a>ES.72 : Préférez un `for` à un `while` lorsqu’il y a une variable de boucle évidente  

#### Raison  

Lisibilité : la logique complète de la boucle est visible « en amont ». La portée de la variable de boucle peut être limitée.

#### Exemple  

```    
    for (gsl::index i = 0; i < vec.size(); i++) {
        // faire du travail
    }
```  

#### Exemple, mauvais  

```    
    int i = 0;
    while (i < vec.size()) {
        // faire du travail
        i++;
    }
```  

#### Application  

??? @TODO-LINK  

---

### <a name="res-while-for"></a>ES.73 : Préférez un `while` à un `for` lorsqu’il n’y a pas de variable de boucle évidente  

#### Raison  

Lisibilité.

#### Exemple  

```    
    int events = 0;
    for (; wait_for_event(); ++events) {  // mauvais, confus
        // …
    }
    // « boucle d’événement » est trompeuse parce que le compteur `events` n’a rien à voir avec la condition `wait_for_event()`.
    // Mieux
    int events = 0;
    while (wait_for_event()) {      // mieux
        ++events;
        // …
    }
```  

#### Application  

* Signaler les actions dans les initialiseurs et incréments de `for` qui ne sont pas liées à la condition du `for`. @TODO-LINK  

---

### <a name="res-for-init"></a>ES.74 : Préférez déclarer une variable de boucle dans la partie initialisation d’un `for`  

Voir **[ES.6](010-expr.md#res‑cond)** @TODO-LINK  

---

### <a name="res-do"></a>ES.75 : Évitez les instructions `do`  

#### Raison  

Lisibilité, éviter les erreurs. La condition de terminaison est à la fin (où elle peut être négligée) et la condition n’est pas vérifiée la première fois.

#### Exemple  

```    
    int x;
    do {
        cin >> x;
        // …
    } while (x < 0);
```  

#### Note  

Oui, il existe des exemples sincères où une instruction `do` clarifie la solution, mais il y a aussi beaucoup de bugs.

#### Application  

* Signaler les instructions `do`. @TODO-LINK  

---

### <a name="res-goto"></a>ES.76 : Évitez le `goto`  

#### Raison  

Lisibilité, éviter les erreurs. Il existe de meilleures structures de contrôle pour les humains ; `goto` est destiné au code généré par la machine.

#### Exception  

Sortir d’une boucle imbriquée. Dans ce cas, sautez toujours en avant.

```    
    for (int i = 0; i < imax; ++i)
        for (int j = 0; j < jmax; ++j) {
            if (a[i][j] > elem_max) goto finished;
            // …
        }
    finished:
    // …
```  

#### Exemple, mauvais  

Il y a pas mal d’usage de l’idiome C `goto‑exit` :

```    
    void f()
    {
        // …
            goto exit;
        // …
            goto exit;
        // …
    exit:
        // … code de nettoyage commun …
    }
```  

Il s’agit d’une simulation ad‑hoc des destructeurs. Déclarez vos ressources avec des gestionnaires qui nettoient automatiquement. Si, pour une raison quelconque, vous ne pouvez pas gérer tout le nettoyage avec des destructeurs pour les variables utilisées, envisagez `gsl::finally()` comme alternative plus propre et fiable au `goto exit`.

#### Application  

* Signaler le `goto`. Mieux encore, signalez tous les `goto` qui ne sautent pas d’une boucle imbriquée à la déclaration immédiatement après la série de boucles. @TODO-LINK  

---

### <a name="res-continue"></a>ES.77 : Minimisez l’usage de `break` et `continue` dans les boucles  

#### Raison  

Dans une boucle non triviale, il est facile d’oublier un `break` ou un `continue`.  

`break` dans une boucle a une signification très différente d’un `break` dans un `switch` (et vous pouvez avoir un `switch` dans une boucle et une boucle dans un `case`).

#### Exemple  

```    
    switch(x) {
    case 1 :
        while (/* condition */) {
            // …
        break;
        } // OUPS ! break du switch ou break du while prévu ?
    case 2 :
        // …
        break;
    }
```  

#### Alternative  

Souvent, une boucle qui nécessite un `break` est un bon candidat pour une fonction (algorithme), auquel cas le `break` devient un `return`.

```    
    // Original : break à l’intérieur de la boucle
    void use1()
    {
        std::vector<T> vec = {/* initialisé avec certaines valeurs */};
        T value;
        for (const T item : vec) {
            if (/* condition */) {
                value = item;
                break;
            }
        }
        /* puis faire quelque chose avec value */
    }

    // MIEUX : créer une fonction et retourner depuis la boucle
    T search(const std::vector<T> &vec)
    {
        for (const T &item : vec) {
            if (/* condition */) return item;
        }
        return T(); // valeur par défaut
    }

    void use2()
    {
        std::vector<T> vec = {/* initialisé avec certaines valeurs */};
        T value = search(vec);
        /* puis faire quelque chose avec value */
    }
```  

Souvent, une boucle qui utilise `continue` peut être exprimée de façon équivalente et aussi claire par un `if` :

```    
    for (int item : vec) {  // MAUVAIS
        if (item%2 == 0) continue;
        if (item == 5) continue;
        if (item > 10) continue;
        /* faire quelque chose avec item */
    }

    for (int item : vec) {  // BON
        if (item%2 != 0 && item != 5 && item <= 10) {
            /* faire quelque chose avec item */
        }
    }
```  

#### Note  

Si vous devez vraiment sortir d’une boucle, un `break` est typiquement meilleur que d’autres alternatives telles que **modifier la variable de boucle** ([ES.86](010-expr.md#res‑loop‑counter)) ou un **`goto`** ([ES.76](010-expr.md#res‑goto)).

#### Application  

??? @TODO-LINK  

---

### <a name="res-break"></a>ES.78 : Ne comptez pas sur le « fallthrough » implicite dans les `switch`  

#### Raison  

Terminez toujours un `case` non vide par un `break`. Oublier un `break` est un bug assez fréquent. Un fallthrough implicite délibéré peut être un risque de maintenance et devrait être rare et explicite.

#### Exemple  

```    
    switch (eventType) {
    case Information:
        update_status_bar();
        break;
    case Warning:
        write_event_log();
        // Mauvais — fallthrough implicite
    case Error:
        display_error_window();
        break;
    }
```  

Des multiples libellés `case` d’une même instruction sont acceptables :

```    
    switch (x) {
    case 'a':
    case 'b':
    case 'f':
        do_something(x);
        break;
    }
```  

Des instructions `return` dans un `case` sont également acceptables :

```    
    switch (x) {
    case 'a':
        return 1;
    case 'b':
        return 2;
    case 'c':
        return 3;
    }
```  

#### Exceptions  

Dans de rares cas où le fallthrough est jugé approprié, soyez explicite et utilisez l’attribut `[[fallthrough]]` :

```    
    switch (eventType) {
    case Information:
        update_status_bar();
        break;
    case Warning:
        write_event_log();
        [[fallthrough]];
    case Error:
        display_error_window();
        break;
    }
```  

#### Note  

@TODO-LINK  

#### Application  

* Signaler tous les fallthrough implicites depuis des `case` non vides. @TODO-LINK  

---

### <a name="res-default"></a>ES.79 : Utilisez `default` pour gérer les cas courants (seulement)  

#### Raison  

Clarté du code. Meilleures opportunités de détection d’erreurs.

#### Exemple  

```    
    enum E { a, b, c, d };

    void f1(E x)
    {
        switch (x) {
        case a:
            do_something();
            break;
        case b:
            do_something_else();
            break;
        default:
            take_the_default_action();
            break;
        }
    }
```  

Il est clair ici qu’il existe une action par défaut et que les cas `a` et `b` sont spéciaux.

#### Exemple  

Mais que se passe‑t‑il s’il n’y a pas d’action par défaut et que vous ne gérez que des cas spécifiques ? Dans ce cas, mettez un `default` vide ou omettez‑le ; sinon, il est impossible de savoir si vous vouliez gérer *tous* les cas :

```    
    void f2(E x)
    {
        switch (x) {
        case a:
            do_something();
            break;
        case b:
            do_something_else();
            break;
        default:
            // ne rien faire pour le reste des cas
            break;
        }
    }
```  

Si vous omettez le `default`, un mainteneur (ou le compilateur) pourrait raisonnablement supposer que vous aviez l’intention de couvrir tous les cas :

```    
    void f2(E x)
    {
        switch (x) {
        case a:
            do_something();
            break;
        case b:
        case c:
            do_something_else();
            break;
        }
    }
```  

Avez‑vous oublié le cas `d` ou l’avez‑vous délibérément omis ? Oublier un cas se produit souvent lorsqu’on ajoute un nouveau cas à une `enum` et qu’on oublie de l’ajouter à chaque `switch` portant sur cet énumérateur.

#### Application  

* Signaler les `switch` sur une `enum` qui ne gèrent pas toutes les valeurs d’énumération et qui n’ont pas de `default`.  
* (Cette règle peut générer trop de faux positifs dans certains bases de code ; si c’est le cas, ne signalez que les `switch` qui gèrent la plupart, mais pas tous, les cas (c’était la stratégie du tout premier compilateur C++)). @TODO-LINK  

---

### <a name="res-noname"></a>ES.84 : N’essayez pas de déclarer une variable locale sans nom  

#### Raison  

Il n’existe pas de tel concept. Ce qui semble pour un humain être une variable sans nom est, pour le compilateur, une instruction constituée d’un temporaire qui sort immédiatement de la portée.

#### Exemple, mauvais  

```    
    void f()
    {
        lock_guard<mutex>{mx};   // mauvais
        // …
    }
```  

Cela déclare un objet `lock_guard` anonyme qui sort immédiatement de la portée au point‑virgule. Ce n’est pas une erreur rare. En particulier, cet exemple peut entraîner des conditions de concurrence difficiles à repérer.

#### Note  

Les arguments de fonction anonymes sont acceptables.

#### Application  

* Signaler les instructions qui ne sont qu’un temporaire. @TODO-LINK  

---

### <a name="res-empty"></a>ES.85 : Faites apparaître les instructions vides  

#### Raison  

Lisibilité.

#### Exemple  

```    
    for (i = 0; i < max; ++i);   // MAUVAIS : l’instruction vide est facilement oubliée
    v[i] = f(v[i]);

    for (auto x : v) {           // meilleur
        // rien
    }
    v[i] = f(v[i]);
```  

#### Application  

* Signaler les instructions vides qui ne sont pas des blocs et ne contiennent pas de commentaires. @TODO-LINK  

---

### <a name="res-loop-counter"></a>ES.86 : Évitez de modifier les variables de contrôle d’une boucle `for` brute à l’intérieur de son corps  

#### Raison  

Le contrôle de boucle en amont doit permettre de raisonner correctement sur ce qui se passe à l’intérieur de la boucle. Modifier les compteurs de boucle à la fois dans l’expression d’itération et à l’intérieur du corps d’une boucle est une source perpétuelle de surprises et de bugs.

#### Exemple  

```    
    for (int i = 0; i < 10; ++i) {
        // aucune mise à jour de i — OK
    }

    for (int i = 0; i < 10; ++i) {
        //
        if (/* quelque chose */) ++i; // MAUVAIS
        //
    }

    bool skip = false;
    for (int i = 0; i < 10; ++i) {
        if (skip) { skip = false; continue; }
        //
        if (/* quelque chose */) skip = true;  // Mieux : deux variables pour deux concepts
        //
    }
```  

#### Application  

* Signaler les variables qui sont potentiellement mises à jour (utilisées de façon non‑`const`) à la fois dans l’expression d’itération de contrôle de boucle et dans le corps de la boucle. @TODO-LINK  

---

### <a name="res-if"></a>ES.87 : N’ajoutez pas de `==` ou `!=` redondants aux conditions  

#### Raison  

Cela évite la verbosité et élimine certaines possibilités d’erreurs. Aide à garder le style cohérent et conventionnel.

#### Exemple  

Par définition, une condition dans une instruction `if`, `while` ou `for` sélectionne entre `true` et `false`. Un nombre est comparé à `0` et une valeur de pointeur à `nullptr`.

```    
    // Tous ces exemples signifient « si p n’est pas nullptr »
    if (p) { ... }            // bon
    if (p != 0) { ... }       // redondant !=0, mauvais : n’utilisez pas 0 pour les pointeurs
    if (p != nullptr) { ... } // redondant !=nullptr, non recommandé
```  

Souvent, `if (p)` se lit comme « si `p` est valide », ce qui exprime directement l’intention du programmeur, alors que `if (p != nullptr)` serait une solution verbeuse.

#### Exemple  

Cette règle est particulièrement utile lorsqu’une déclaration est utilisée comme condition :

```    
    if (auto pc = dynamic_cast<Circle*>(ps)) { ... } // exécuter si ps pointe vers un Circle, bon

    if (auto pc = dynamic_cast<Circle*>(ps); pc != nullptr) { ... } // non recommandé
```  

#### Exemple  

Notez que la conversion implicite en bool est appliquée dans les conditions. Par exemple :

```    
    for (string s; cin >> s; ) v.push_back(s);
```  

Ceci invoque `operator bool()` de `istream`.

#### Note  

Comparer explicitement un entier à `0` n’est généralement **pas** redondant. La raison est que (contrairement aux pointeurs et aux booléens) un entier possède souvent plus de deux valeurs raisonnables. De plus, `0` (zéro) est souvent utilisé pour indiquer le succès. Par conséquent, il vaut mieux être précis quant à la comparaison.

```    
    void f(int i)
    {
        if (i)            // suspect
        // …
        if (i == success) // peut‑être meilleur
        // …
    }
```  

Rappelez‑vous toujours qu’un entier peut avoir plus de deux valeurs.

#### Exemple, mauvais  

Il a été noté que  

```    
    if(strcmp(p1, p2)) { ... }   // les deux chaînes C‑style sont‑elles égales ? (erreur !)
```  

est une erreur fréquente des débutants. Si vous utilisez des chaînes C‑style, vous devez bien connaître les fonctions de `<cstring>`. Être verbeux et écrire  

```    
    if(strcmp(p1, p2) != 0) { ... }   // les deux chaînes C‑style sont‑elles égales ? (erreur !)
```  

ne vous sauverait pas en soi.

#### Note  

La condition opposée s’exprime le plus facilement avec une négation :

```    
    // Tous ces exemples signifient « si p est nullptr »
    if (!p) { ... }           // bon
    if (p == 0) { ... }       // redondant == 0, mauvais : n’utilisez pas 0 pour les pointeurs
    if (p == nullptr) { ... } // redondant == nullptr, non recommandé
```  

#### Application  

Facile : chercher l’usage redondant de `!=` et `==` dans les conditions. @TODO-LINK  

---

## <a name="ss-numbers"></a>Arithmétique  

### <a name="res-mix"></a>ES.100 : Ne mélangez pas des calculs signés et non signés  

#### Raison  

Éviter les résultats erronés.

#### Exemple  

```    
    int x = -3;
    unsigned int y = 7;

    cout << x - y << '\n';  // résultat unsigned, possiblement 4294967286
    cout << x + y << '\n';  // résultat unsigned : 4
    cout << x * y << '\n';  // résultat unsigned, possiblement 4294967275
```  

Il est plus difficile de repérer le problème dans des exemples plus réalistes.

#### Note  

Malheureusement, C++ utilise les entiers signés pour les index de tableau et la bibliothèque standard utilise les entiers non signés pour les index de conteneur. Cela empêche la cohérence. Utilisez `gsl::index` pour les index ; **voir ES.107**(010-expr.md#res‑subscripts) @TODO-LINK.

#### Application  

* Les compilateurs connaissent déjà cela et parfois avertissent.  
* (Pour éviter le bruit) Ne signalez pas les comparaisons signées/unsigned où l’un des arguments est `sizeof` ou une appel à `.size()` d’un conteneur et l’autre est `ptrdiff_t`. @TODO-LINK  

---

### <a name="res-unsigned"></a>ES.101 : Utilisez des types non signés pour la manipulation de bits  

#### Raison  

Les types non signés supportent la manipulation de bits sans les surprises du bit de signe.

#### Exemple  

```    
    unsigned char x = 0b1010'1010;
    unsigned char y = ~x;   // y vaut 0b0101'0101;
```  

#### Note  

Les types non signés peuvent aussi être utiles pour l’arithmétique modulaire.  
Cependant, si vous voulez une arithmétique modulaire, ajoutez des commentaires expliquant le recours au comportement de débordement, car ce code peut surprendre de nombreux programmeurs.

#### Application  

* Pratiquement impossible en général à cause de l’usage d’entiers non signés pour les indices de conteneur.  
* ??? @TODO-LINK  

---

### <a name="res-signed"></a>ES.102 : Utilisez des types signés pour les calculs  

#### Raison  

Parce que la plupart des calculs sont supposés être signés ; `x - y` donne un nombre négatif quand `y > x` excepté les rares cas où vous voulez réellement de l’arithmétique modulaire.

#### Exemple  

L’arithmétique non signée peut produire des résultats surprenants si vous ne l’attendez pas. C’est encore plus vrai lorsqu’on mélange signé et non signé.

```    
    template<typename T, typename T2>
    T subtract(T x, T2 y)
    {
        return x - y;
    }

    void test()
    {
        int s = 5;
        unsigned int us = 5;
        cout << subtract(s, 7) << '\n';       // -2
        cout << subtract(us, 7u) << '\n';     // 4294967294
        cout << subtract(s, 7u) << '\n';      // -2
        cout << subtract(us, 7) << '\n';      // 4294967294
        cout << subtract(s, us + 2) << '\n'; // -2
        cout << subtract(us, s + 2) << '\n'; // 4294967294
    }
```  

Même très explicite, on peut se tromper avec `us - (s + 2)` ou `s += 2; …; us - s`.

#### Exception  

Utilisez des types non signés si vous voulez réellement de l’arithmétique modulaire ; ajoutez des commentaires expliquant le

but.

#### Exemple  

La bibliothèque standard utilise des types non signés pour les index de conteneur. Le tableau intégré utilise des types signés pour les index. Cela crée inévitablement des surprises (et des bugs).

```    
    int a[10];
    for (int i = 0; i < 10; ++i) a[i] = i;
    vector<int> v(10);
    // compare signed to unsigned ; certains compilateurs avertissent, mais nous ne devrions pas
    for (gsl::index i = 0; i < v.size(); i += 2) v[i] = i;

    int a2[-2];         // erreur : taille négative

    // OK, mais le nombre d’int (4294967294) est tellement grand qu’on devrait obtenir une exception
    vector<int> v2(-2);
```  

Utilisez `gsl::index` pour les index ; **voir ES.107**(010-expr.md#res‑subscripts) @TODO-LINK.

#### Application  

* Signaler les calculs mixtes signés/unsigned.  
* Signaler les résultats d’arithmétique unsigned assignés ou imprimés comme signed.  
* Signaler les littéraux négatifs (ex. `-2`) utilisés comme index de conteneur.  
* (Pour éviter le bruit) Ne signalez pas les comparaisons signées/unsigned où l’un des arguments est `sizeof` ou un appel à `.size()` d’un conteneur et l’autre est `ptrdiff_t`. @TODO-LINK  

---

### <a name="res-overflow"></a>ES.103 : Ne dépassez pas les limites (overflow)  

#### Raison  

Le dépassement rend généralement votre algorithme numérique dénué de sens. Incrémenter une valeur au‑delà d’une valeur maximale peut entraîner une corruption mémoire et un comportement indéfini.

#### Exemple, mauvais  

```    
    int a[10];
    a[10] = 7;   // mauvais, dépassement de tableau

    for (int n = 0; n <= 10; ++n)
        a[n] = 9;   // mauvais, dépassement de tableau
```  

```    
    int n = numeric_limits<int>::max();
    int m = n + 1;   // mauvais, dépassement numérique
```  

```    
    int area(int h, int w) { return h * w; }

    auto a = area(10'000'000, 100'000'000);   // mauvais, dépassement numérique
```  

#### Exception  

Utilisez des types non signés si vous voulez vraiment de l’arithmétique modulaire.

**Alternative** : Pour les applications critiques qui peuvent se permettre un petit surcoût, utilisez un type entier ou flottant vérifié (range‑checked).

#### Application  

??? @TODO-LINK  

---

### <a name="res-underflow"></a>ES.104 : Ne sous‑débordez pas (underflow)  

#### Raison  

Décrémenter une valeur en dessous d’une borne minimale peut entraîner de la corruption mémoire et un comportement indéfini.

#### Exemple, mauvais  

```    
    int a[10];
    a[-2] = 7;   // mauvais

    int n = 101;
    while (n--)
        a[n - 1] = 9;   // mauvais (deux fois)
```  

#### Exception  

Utilisez des types non signés si vous voulez vraiment de l’arithmétique modulaire.

#### Application  

??? @TODO-LINK  

---

### <a name="res-zero"></a>ES.105 : Ne divisez pas par zéro entier  

#### Raison  

Le résultat est indéfini et provoque probablement un crash.

#### Note  

Cela vaut aussi pour `%`.

#### Exemple, mauvais  

```    
    int divide(int a, int b)
    {
        // MAUVAIS, devrait être vérifié (ex. via précondition)
        return a / b;
    }
```  

#### Exemple, bon  

```    
    int divide(int a, int b)
    {
        // bon, gérer via précondition (et remplacer par des contrats quand C++ les aura)
        Expects(b != 0);
        return a / b;
    }

    double divide(double a, double b)
    {
        // bon, gérer via l’utilisation de double
        return a / b;
    }
```  

**Alternative** : Pour les applications critiques qui peuvent se permettre un petit surcoût, utilisez un type entier ou flottant vérifié.

#### Application  

* Signaler la division par une valeur entière qui pourrait être zéro. @TODO-LINK  

---

### <a name="res-nonnegative"></a>ES.106 : N’essayez pas d’éviter les valeurs négatives en utilisant `unsigned`  

#### Raison  

Choisir `unsigned` implique de nombreux changements de comportement des entiers, y compris l’arithmétique modulaire, supprime les avertissements liés au dépassement, et ouvre la porte à des erreurs liées aux mélanges signés/unsigned. Utiliser `unsigned` n’élimine pas réellement la possibilité de valeurs négatives.

#### Exemple  

```    
    unsigned int u1 = -2;   // valide : u1 vaut 4294967294
    int i1 = -2;
    unsigned int u2 = i1;   // valide : u2 vaut 4294967294
    int i2 = u2;            // valide : i2 vaut -2
```  

Ces problèmes avec de telles constructions parfaitement légales sont difficiles à repérer dans du code réel et sont à l’origine de nombreuses erreurs réelles. Considérez :

```    
    unsigned area(unsigned height, unsigned width) { return height*width; } // (voir aussi 005‑interfaces.md#ri‑expects)
    // …
    int height;
    cin >> height;
    auto a = area(height, 2);   // si l’entrée est –2, a devient 4294967292
```  

Rappelez‑vous que `-1` assigné à un `unsigned int` devient le plus grand `unsigned int`. De plus, comme l’arithmétique unsigned est modulaire, la multiplication ne déborde pas ; elle « wrap‑around » simplement.

#### Exemple  

```    
    unsigned max = 100000;    // « typo accidentelle », je voulais dire 10'000
    unsigned short x = 100;
    while (x < max) x += 100; // boucle infinie
```  

Si `x` avait été un `short` signé, nous aurions pu avertir d’un comportement indéfini lors du dépassement.

#### Alternatives  

* Utilisez des entiers signés et vérifiez `x >= 0`.  
* Utilisez un type entier positif.  
* Utilisez un type entier de sous‑intervalle.  
* `Assert(-1 < x)`

Par exemple :

```    
    struct Positive {
        int val;
        Positive(int x) :val{x} { Assert(0 < x); }
        operator int() { return val; }
    };

    int f(Positive arg) { return arg; }

    int r1 = f(2);
    int r2 = f(-2);  // lance une exception
```  

#### Note  

???  

#### Application  

Voir les applications de **ES.100**. @TODO-LINK  

---

### <a name="res-subscripts"></a>ES.107 : N’utilisez pas `unsigned` pour les index, privilégiez `gsl::index`  

#### Raison  

Éviter les confusions signées/unsigned. Permettre de meilleures optimisations. Permettre une meilleure détection d’erreurs. Éviter les problèmes avec `auto` et `int`.

#### Exemple, mauvais  

```    
    vector<int> vec = /*…*/;

    for (int i = 0; i < vec.size(); i += 2)                    // pourrait ne pas être assez grand
        cout << vec[i] << '\n';
    for (unsigned i = 0; i < vec.size(); i += 2)               // risque de wrap‑around
        cout << vec[i] << '\n';
    for (auto i = 0; i < vec.size(); i += 2)                   // pourrait ne pas être assez grand
        cout << vec[i] << '\n';
    for (vector<int>::size_type i = 0; i < vec.size(); i += 2) // verbeux
        cout << vec[i] << '\n';
    for (auto i = vec.size()-1; i >= 0; i -= 2)                // bug
        cout << vec[i] << '\n';
    for (int i = vec.size()-1; i >= 0; i -= 2)                 // pourrait ne pas être assez grand
        cout << vec[i] << '\n';
```  

#### Exemple, bon  

```    
    vector<int> vec = /*…*/;

    for (gsl::index i = 0; i < vec.size(); i += 2)             // ok
        cout << vec[i] << '\n';
    for (gsl::index i = vec.size()-1; i >= 0; i -= 2)          // ok
        cout << vec[i] << '\n';
```  

#### Note  

Le tableau intégré autorise les index signés. Les conteneurs de la bibliothèque standard utilisent des index non signés. Ainsi, aucune solution parfaite et totalement compatible n’existe (à moins que les conteneurs de la bibliothèque standard ne changent un jour pour utiliser des index signés).  

Étant donné les problèmes connus avec les unsigned et les mélanges signés/unsigned, il vaut mieux s’en tenir aux entiers (signés) suffisants, ce que garantit `gsl::index`.

#### Exemple  

```    
    template<typename T>
    struct My_container {
    public:
        // …
        T& operator[](gsl::index i);    // pas unsigned
        // …
    };
```  

#### Exemple  

??? démontrer l’amélioration du code généré et le potentiel de détection d’erreurs ???

#### Alternatives  

Alternatives pour les utilisateurs :

* Utilisez des algorithmes  
* Utilisez `range‑for`  
* Utilisez des itérateurs/pointeurs  

#### Application  

* Très difficile tant que les conteneurs de la bibliothèque standard restent incohérents.  
* (Pour éviter le bruit) Ne signalez pas les comparaisons signées/unsigned où l’un des arguments est `sizeof` ou un appel à `.size()` d’un conteneur et l’autre est `ptrdiff_t`. @TODO-LINK  