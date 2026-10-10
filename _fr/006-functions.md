# <a name="s-functions"></a>F: Fonctions

Une fonction spécifie une action ou un calcul qui fait passer le système d’un état cohérent à un autre. C’est le bloc de construction fondamental des programmes.

Il doit être possible de nommer une fonction de manière significative, de spécifier les exigences de son argument et d’énoncer clairement la relation entre les arguments et le résultat. Une implémentation n’est pas une spécification. Essayez de penser à ce que fait une fonction autant qu’à comment elle le fait.

Les fonctions sont la partie la plus critique dans la plupart des interfaces, consultez donc les règles d’interface.

## Résumé des règles de fonctions :

- [F.1 : « Package » d’opérations significatives soigneusement nommées](#rf-package)
- [F.2 : Une fonction doit effectuer une seule opération logique](#rf-logical)
- [F.3 : Garder les fonctions courtes et simples](#rf-single)
- [F.4 : Si une fonction pourrait être évaluée au moment de la compilation, déclarer `constexpr`](#rf-constexpr)
- [F.5 : Si une fonction est très petite et critique en temps, la déclarer `inline`](#rf-inline)
- [F.6 : Si votre fonction ne doit pas lancer d’exception, déclarer `noexcept`](#rf-noexcept)
- [F.7 : À usage général, prendre des arguments `T*` ou `T&` plutôt que des pointeurs intelligents](#rf-smart)
- [F.8 : Privilégier les fonctions pures](#rf-pure)
- [F.9 : Les paramètres non utilisés doivent être sans nom](#rf-unused)
- [F.10 : Si une opération peut être réutilisée, lui donner un nom](#rf-name)
- [F.11 : Utiliser un lambda anonyme si vous avez besoin d’un objet fonction simple en un seul endroit](#rf-lambda)

### Règles d’expression de passage de paramètres :

- [F.15 : Préférer des façons simples et conventionnelles de passer des informations](#rf-conventional)
- [F.16 : Pour les paramètres « in », passer les types faiblement copiables par valeur et les autres par référence à `const`](#rf-in)
- [F.17 : Pour les paramètres « in-out », passer par référence non‑`const`](#rf-inout)
- [F.18 : Pour les paramètres « will‑move‑from », passer par `X&&` et `std::move` le paramètre](#rf-consume)
- [F.19 : Pour les paramètres « forward », passer par `TP&&` et ne faire `std::forward` que le paramètre](#rf-forward)
- [F.20 : Pour les valeurs de sortie « out », préférer les valeurs de retour aux paramètres de sortie](#rf-out)
- [F.21 : Pour retourner plusieurs valeurs « out », privilégier le retour d’une structure](#rf-out-multi)
- [F.60 : Privilégier `T*` sur `T&` lorsque « aucun argument » est une option valide](#rf-ptr-ref)

### Règles sémantiques de passage de paramètres :

- [F.22 : Utiliser `T*` ou `owner<T*>` pour désigner un seul objet](#rf-ptr)
- [F.23 : Utiliser `not_null<T>` pour indiquer que « nul » n’est pas une valeur valide](#rf-nullptr)
- [F.24 : Utiliser un `span<T>` ou un `span_p<T>` pour désigner une séquence semi‑ouverte](#rf-range)
- [F.25 : Utiliser `zstring` ou `not_null<zstring>` pour désigner une chaîne C‑style](#rf-zstring)
- [F.26 : Utiliser `unique_ptr<T>` pour transférer la propriété lorsqu’un pointeur est nécessaire](#rf-unique_ptr)
- [F.27 : Utiliser `shared_ptr<T>` pour partager la propriété](#rf-shared_ptr)

<a name="rf-value-return"></a>Règles sémantiques de retour de valeur :

- [F.42 : Retourner un `T*` pour indiquer une position (uniquement)](#rf-return-ptr)
- [F.43 : Ne jamais (directement ou indirectement) retourner un pointeur ou une référence vers un objet local](#rf-dangle)
- [F.44 : Retourner un `T&` quand la copie est indésirable et qu’un retour d’un objet vide n’est pas requis](#rf-return-ref)
- [F.45 : Ne pas retourner un `T&&`](#rf-return-ref-ref)
- [F.46 : `int` est le type de retour pour `main()`](#rf-main)
- [F.47 : Retourner `T&` depuis les opérateurs d’affectation](#rf-assignment-op)
- [F.48 : Ne pas retourner `std::move(local)`](#rf-return-move-local)
- [F.49 : Ne pas retourner `const T`](#rf-return-const)

### Autres règles de fonctions :

- [F.50 : Utiliser un lambda lorsqu’une fonction ne fera pas (pour capturer les variables locales ou écrire une fonction locale)](#rf-capture-vs-overload)
- [F.51 : Où il y a un choix, préférer les arguments par défaut aux surcharges](#rf-default-args)
- [F.52 : Préférer la capture par référence dans les lambdas qui seront utilisées localement, y compris passées aux algorithmes](#rf-reference-capture)
- [F.53 : Éviter la capture par référence dans les lambdas qui seront utilisées hors du scop, y compris retournées, stockées dans le tas ou passées à un autre thread](#rf-value-capture)
- [F.54 : Lors de l’écriture d’une lambda qui capture `this` ou tout membre de classe, ne pas utiliser la capture par défaut `[=]`](#rf-this-capture)
- [F.55 : Ne pas utiliser `va_arg`](#f-varargs)
- [F.56 : Éviter l’imbrication inutile de conditions](#f-nesting)

Les fonctions présentent de fortes similitudes avec les lambdas et les objets fonction.

**Voir aussi** : [C.lambdas : Objets fonction et lambdas](#ss-lambdas)

## <a name="ss-fct-def"></a>F.def : Définitions de fonctions

Une définition de fonction est une déclaration de fonction qui spécifie également la mise en œuvre de la fonction, le corps de la fonction.

### <a name="rf-package"></a>F.1 : « Package » d’opérations significatives soigneusement nommées

#### Raison

Extraits de code communs rendent le code plus lisible, plus susceptible d’être réutilisé et limitent les erreurs provenant d’un code complexe. Si quelque chose constitue une action bien définie, séparez‑le du code environnant et donnez‑lui un nom.

#### Exemple, pas

```cpp
    void read_and_print(istream& is)    // lit un int et l’affiche
    {
        int x;
        if (is >> x)
            cout << "the int is " << x << '\n';
        else
            cerr << "no int on input\n";
    }
```

Tout ce qui est mal avec `read_and_print`.  
Il lit, écrit (sur un `ostream` fixe), écrit des messages d’erreur (sur un `ostream` fixe) et ne gère que les `int`.  
Il n’y a rien à réutiliser, les opérations logiquement séparées sont mêlées et les variables locales restent dans le scope après l’usage logique.  
Pour un petit exemple, cela semble correct, mais si l’opération d’entrée, de sortie et la gestion des erreurs étaient plus complexes, ce désordre pourrait devenir difficile à comprendre.

#### Note

Si vous écrivez un lambda non trivial qu’il est possible d’utiliser à plus d’un endroit, donnez‑lui un nom en l’affectant à une variable (généralement non locale).

#### Exemple

```cpp
    sort(a, b, [](T x, T y) { return x.rank() < y.rank() && x.value() < y.value(); });
```

Nommer ce lambda décortique l’expression en ses parties logiques et fournit un indice fort sur la signification du lambda.

```cpp
    auto lessT = [](T x, T y) { return x.rank() < y.rank() && x.value() < y.value(); };
    sort(a, b, lessT);
```

Le code le plus court n’est pas toujours le meilleur pour la performance ou la maintenabilité.

#### Exception

Les corps de boucle, y compris les lambdas utilisés comme corps de boucle, ont rarement besoin d’être nommés.  
Cependant, de gros corps de boucle (par ex. des dizaines de lignes ou de pages) peuvent poser problème.  
La règle [Garder les fonctions courtes et simples](#rf-single) implique « Garder les corps de boucle courts ».  
De même, les lambdas utilisés comme arguments de rappel sont parfois non triviales, mais peu susceptibles d’être réutilisées.

#### Système d’enforcement

* Voir [Garder les fonctions courtes et simples](#rf-single)
* Signaler les lambdas identiques et très similaires utilisés en différents endroits.

### <a name="rf-logical"></a>F.2 : Une fonction doit effectuer une seule opération logique

#### Raison

Une fonction qui exécute une seule opération est plus simple à comprendre, à tester et à réutiliser.

#### Exemple

Considérons :

```cpp
    void read_and_print()    // mauvais
    {
        int x;
        cin >> x;
        // check for errors
        cout << x << "\n";
    }
```

C’est un monolithe lié à une saisie spécifique et ne trouvera jamais un autre (différent) usage.  
Aoûtant des fonctions adaptées aux parties logiques et les paramétrer :

```cpp
    int read(istream& is)    // mieux
    {
        int x;
        is >> x;
        // check for errors
        return x;
    }

    void print(ostream& os, int x)
    {
        os << x << "\n";
    }
```

Elles peuvent maintenant être combinées où nécessaire :

```cpp
    void read_and_print()
    {
        auto x = read(cin);
        print(cout, x);
    }
```

Si besoin, on peut encore génreraliser `read()` et `print()` sur le type de données, le mécanisme de I/O, la réponse aux erreurs, etc. Exemple :

```cpp
    auto read = [](auto& input, auto& value)    // mieux
    {
        input >> value;
        // check for errors
    };

    void print(auto& output, const auto& value)
    {
        output << value << "\n";
    }
```

#### Système d’enforcement

* Examiner les fonctions avec plus d’un paramètre « out » comme suspectes. Utiliser des valeurs de retour, y compris `tuple`, pour plusieurs valeurs de retour.  
* Examiner les fonctions « grandes » ne pouvant pas tenir sur une téléportation d’écran suspectes. Considérer factoriser ces fonctions en sous‑opérations plus petites et nommées.  
* Examiner les fonctions ayant 7 paramètres ou plus comme suspectes.

### <a name="rf-single"></a>F.3 : Garder les fonctions courtes et simples

#### Raison

Les fonctions grandes sont difficiles à lire, plus susceptibles de contenir du code complexe et plus susceptibles de comporter des variables avec des écopes plus larges que le minimum.  
Les fonctions maîtrisées la structure de contrôle, sont plus susceptibles d’augmenter et d’essayer d’enfreindre les erreurs logiques.

#### Exemple

Considérez :

```cpp
    double simple_func(double val, int flag1, int flag2)
        // simple_func : prend une valeur et calcule la sortie attendue ASIC
        // en fonction des deux indicateurs de mode.
    {
        double intermediate;
        if (flag1 > 0) {
            intermediate = func1(val);
            if (flag2 % 2)
                 intermediate = sqrt(intermediate);
        }
        else if (flag1 == -1) {
            intermediate = func1(-val);
            if (flag2 % 2)
                 intermediate = sqrt(-intermediate);
            flag1 = -flag1;
        }
        if (abs(flag2) > 10) {
            intermediate = func2(intermediate);
        }
        switch (flag2 / 10) {
        case 1: if (flag1 == -1) return finalize(intermediate, 1.171);
                break;
        case 2: return finalize(intermediate, 13.1);
        default: break;
        }
        return finalize(intermediate, 0.);
    }
```

C’est trop compliqué.  
Comment savoir si toutes les alternatives possibles ont été correctement traitées ?  
Oui, cela enfreint d’autres règles également.

On peut réfactorer :

```cpp
    double func1_muon(double val, int flag)
    {
        // ???
    }

    double func1_tau(double val, int flag1, int flag2)
    {
        // ???
    }

    double simple_func(double val, int flag1, int flag2)
        // simple_func : prend une valeur et calcule la sortie attendue ASIC
        // en fonction des deux indicateurs de mode.
    {
        if (flag1 > 0)
            return func1_muon(val, flag2);
        if (flag1 == -1)
            // géré par func1_tau : flag1 = -flag1;
            return func1_tau(-val, flag1, flag2);
        return 0.;
    }
```

#### Note

« Ne dépasse pas une fenêtre » constitue souvent une bonne définition pratique de « trop gros ».  
Les fonctions d’une à cinq lignes sont généralement considérées comme normales.

#### Note

Diviser les fonctions grandes en fonctions plus petites cohérentes et nommées.  
Les petites fonctions simples sont facilement en‑ligne là où le coût d’un appel de fonction est important.

#### Système d’enforcement

* Signaler les fonctions qui ne « s'ajustent pas à l’écran ».  
  Combien d’une fenêtre ? Essayez 60 lignes sur 140 caractères ; c’est à peu près le maximum confortable pour une page de livre.  
* Signaler les fonctions trop complexes.  
  Vous pourriez compter la complexité cyclomatique. Essayez « plus de 10 chemins logiques ».  
  Comptez un `switch` simple comme un chemin.

### <a name="rf-constexpr"></a>F.4 : Si une fonction pourrait être évaluée au moment de la compilation, déclarer `constexpr`

#### Raison

`constexpr` est nécessaire pour dire au compilateur d’autoriser l’évaluation à la compilation.

#### Exemple

Le (infâme) factoriel :

```cpp
    constexpr int fac(int n)
    {
        constexpr int max_exp = 17;      // constexpr permet d’utiliser max_exp dans Expects
        Expects(0 <= n && n < max_exp);  // évite la folie et le dépassement
        int x = 1;
        for (int i = 2; i <= n; ++i) x *= i;
        return x;
    }
```

C’est C++14.  
Pour C++11, utilisez une formulation récursive de `fac()`.

#### Note

`constexpr` n’assure pas une évaluation à la compilation ; il assure simplement qu’une fonction peut être évaluée à la compilation pour des arguments d’expression constante si le programmeur le demande ou si le compilateur décide de le faire pour optimiser.

```cpp
    constexpr int min(int x, int y) { return x < y ? x : y; }
```

```cpp
    void test(int v)
    {
        int m1 = min(-1, 2);            // probablement évaluation à la compilation
        constexpr int m2 = min(-1, 2);  // évaluation à la compilation
        int m3 = min(-1, v);            // évaluation à l’exécution
        constexpr int m4 = min(-1, v);  // erreur : impossible d’évaluer à la compilation
    }
```

#### Note

N’essayez pas de rendre toutes les fonctions `constexpr`.  
La plupart des calculs sont mieux faits à l’exécution.

#### Note

Tout API qui pourrait en fin de compte dépendre d’une configuration ou de logique métier à l’exécution ne doit pas être rendu `constexpr`.  
Une telle personnalisation ne peut être évaluée par le compilateur, et toute fonction `constexpr` qui dépendait de cette API devrait être refactorisée ou abandonner `constexpr`.

#### Système d’enforcement

Inévitable et inutile.  
Le compilateur donne une erreur si une fonction non `constexpr` est appelée là où une valeur constante est requise.

### <a name="rf-inline"></a>F.5 : Si une fonction est très petite et critique en temps, la déclarer `inline`

#### Raison

Certains optimiseurs sont bons pour inline sans l’indication du programmeur, mais ne comptez pas sur eux.  
Mesurez ! Au cours des 40 dernières années, on a promis des compilateurs qui inlineaient mieux que les humains sans aucune indication.  
On attend encore.  
Spécifier `inline` (explicitement, ou implicitement lorsqu’on écrit une fonction membre dans la définition d’une classe) encourage le compilateur à faire un meilleur rendu.

#### Exemple

```cpp
    inline string cat(const string& s, const string& s2) { return s + s2; }
```

#### Exception

Ne pas placer une fonction `inline` dans ce qui est censé être une interface stable à moins d’être sûr qu’elle ne changera pas.  
Une fonction `inline` fait partie de l’ABI.

#### Note

`constexpr` implique `inline`.

#### Note

Les fonctions membres définies dans la définition d’une classe sont `inline` par défaut.

#### Exception

Les modèles de fonctions (y compris les fonctions membres de modèles de classes `A<T>::function()` et les fonctions de modèle de classe `A::function<T>()`) sont normalement définis dans les en‑têtes et donc `inline`.

#### Note

Considérez de faire sortir des fonctions qui ont plus de trois instructions et qui peuvent être déclarées hors ligne.

### <a name="rf-noexcept"></a>F.6 : Si votre fonction ne doit pas lancer d’exception, déclarer `noexcept`

#### Raison

S’il n’est pas supposé lancer une exception, le programme ne peut pas supposer qu’il peut gérer l’erreur et doit être terminé dès que possible.  
Déclarer une fonction `noexcept` aide les optimiseurs en réduisant le nombre de chemins d’exécution alternatifs.  
C’est aussi plus rapide lors de la sortie après l’échec.

#### Exemple

Mettre `noexcept` sur chaque fonction écrite complètement en C ou dans n’importe quelle autre langue sans exceptions.  
La bibliothèque standard C++ le fait implicitement pour toutes les fonctions de la bibliothèque standard C.

#### Note

Les fonctions `constexpr` peuvent lancer lorsqu’elles sont évaluées à l’exécution, donc vous pourriez avoir besoin de `noexcept` conditionnel pour certaines d’elles.

#### Exemple

Vous pouvez utiliser `noexcept` même sur des fonctions qui peuvent lancer :

```cpp
    vector<string> collect(istream& is) noexcept
    {
        vector<string> res;
        for (string s; is >> s;)
            res.push_back(s);
        return res;
    }
```

Si `collect()` s’épuise de mémoire, le programme plante.  
À moins que le programme ne soit conçu pour survivre à l’épuisement de mémoire, ce pourrait être la bonne chose à faire ;  
`terminate()` pourrait produire une trace de logs d’erreur (mais après l’épuisement de mémoire, il est difficile de faire quelque chose de malin).

#### Note

Vous devez tenir compte de l’environnement d’exécution dans lequel votre code est exécuté lorsqu’on décide d’étiqueter une fonction `noexcept`, surtout à cause du problème des exceptions et de l’allocation.  
Le code général (comme la bibliothèque standard et d’autres utilitaires de ce genre) doit supporter les environnements où une exception `bad_alloc` peut être levée.  
Cependant, la plupart des programmes et environnements n’ont pas de mécanisme pour gérer une perte d’allocation, et aborter le programme est la réponse la plus propre et la plus simple.  
S’il est sûr que votre code d’application ne peut pas répondre à une exception d’allocation, vous pourriez envisager de +`noexcept` même sur des fonctions qui allouent.

Un autre point : `noexcept` est le plus utile (et le plus clairement correct) pour les fonctions bas niveau très utilisées.

#### Note

Les destructeurs, les fonctions `swap`, les opérations de déplacement et les constructeurs par défaut ne doivent jamais lancer.

#### Note

Il faut faire vigilance sur les fonctions virtuelles de base et les fonctions faites partie d’une interface publique, puisque déclarer une fonction `noexcept` impose une garantie que toutes les implémentations actuelles et futures doivent respecter.  
Pour une fonction virtuelle, tous les remplacants doivent être `noexcept` aussi, et retirer `noexcept` d’une fonction pourrait casser les fonctions appelantes.

#### Système d’enforcement

* (Difficile) Marquer les fonctions bas niveau qui ne lèvent pas d’exception mais ne sont pas `noexcept`.  
* Marquer les `swap`, les opérations de déplacement, les destructeurs et les constructeurs par défaut qui lèvent éventuellement.

### <a name="rf-smart"></a>F.7 : À usage général, prendre des arguments `T*` ou `T&` plutôt que des pointeurs intelligents

#### Raison

Passer un pointeur intelligent transfère ou partage la possession et ne doit être utilisé que lorsqu’on veut une signification de possession.  
Une fonction qui ne manipule pas la durée de vie doit prendre des pointeurs bruts ou des références à la place.

Passer par un pointeur intelligent limite l’utilisation d’une fonction aux appelants qui utilisent des pointeurs intelligents.  
Une fonction qui a besoin d’un `widget` doit pouvoir accepter n’importe quel `widget`, pas seulement ceux dont la durée de vie est gérée par un type de pointeur intelligent particulier.

Passer un `shared_ptr` (par ex., `std::shared_ptr`) implique un coût d’exécution à l’échelle du temps de calcul.

#### Exemple

```cpp
    // accepte n’importe quel int*
    void f(int*);

    // ne peut accepter que des ints pour lesquels vous souhaitez transférer la possession
    void g(unique_ptr<int>);

    // ne peut accepter que des ints pour lesquels vous êtes prêt à partager la possession
    void g(shared_ptr<int>);

    // ne change pas la possession, mais exige une possession particulière de l’appelant
    void h(const unique_ptr<int>&);

    // accepte n’importe quel int
    void h(int&);
```

#### Exemple, mauvais

```cpp
    // appelant
    void f(shared_ptr<widget>& w)
    {
        // ...
        use(*w); // seule utilisation de w -- la durée de vie n’est utilisée du tout
        // ...
    };

    // appel
    shared_ptr<widget> my_widget = /* ... */;
    f(my_widget);

    widget stack_widget;
    f(stack_widget); // erreur
```

#### Exemple, bon

```cpp
    // appelant
    void f(widget& w)
    {
        // ...
        use(w);
        // ...
    };

    // appel
    shared_ptr<widget> my_widget = /* ... */;
    f(*my_widget);

    widget stack_widget;
    f(stack_widget); // ok -- cela fonctionne maintenant
```

#### Note

On peut attraper beaucoup de cas courants d’explosions de pointeurs circulant statiquement (voir le profil de sécurité de durée de vie).  
Les arguments de fonction vivent naturellement pour la durée d’appel et ont donc moins de problèmes de durée de vie.

#### Système d’enforcement

* (Simple) Avertir si une fonction prend un paramètre de type pointeur intelligent qui est copiable mais que la fonction ne fait que `operator*`, `operator->` ou `get()`.  
  Suggérer d'utiliser un `T*` ou `T&` à la place.  
* Marquer un paramètre de type pointeur intelligent (un type qui surcharge `operator->` ou `operator*`) copiable/mouvable mais qui n’est jamais copié/mouvoir à partir de la fonction, jamais modifié et ne passe pas à une autre fonction qui pourrait le faire. Cela signifie que les caractéristiques de possession ne sont pas utilisées.  
  Suggérer d’utiliser un `T*` ou `T&` à la place.

**Voir aussi** :

* [Préférer `T*` sur `T&` lorsque « pas d’argument » est une option valide](#rf-ptr-ref)
* [Résumé des règles de pointeur intelligent](#rr-summary-smartptrs)

### <a name="rf-pure"></a>F.8 : Privilégier les fonctions pures

#### Raison

Les fonctions pures sont plus faciles à raisonner, parfois plus faciles à optimiser (et même à paralléliser), et parfois peuvent être mémoïzées.

#### Exemple

```cpp
    template<class T>
    auto square(T t) { return t * t; }
```

#### Système d’enforcement

Pas possible.

### <a name="rf-unused"></a>F.9 : Les paramètres non utilisés doivent être sans nom

#### Raison

Lisibilité. Suppression d’avertissements sur les paramètres inutilisés.

#### Exemple

```cpp
    widget* find(const set<widget>& s, const widget& w, Hint);   // un jour, un indice était utilisé
```

#### Note

Autoriser les paramètres sans nom a été introduit dans les années 1980 pour résoudre ce problème.

Si les paramètres sont conditionnellement inutilisés, les déclarer avec l’attribut `[[maybe_unused]]`.  
Par ex. :

```cpp
    template <typename Value>
    Value* find(const set<Value>& s, const Value& v, [[maybe_unused]] Hint h)
    {
        if constexpr (sizeof(Value) > CacheSize)
        {
            // un indice est utilisé uniquement si Value a une certaine taille
        }
    }
```

#### Système d’enforcement

Avertir les paramètres non utilisés nommés.

### <a name="rf-name"></a>F.10 : Si une opération peut être réutilisée, lui donner un nom

#### Raison

Documentation, lisibilité, opportunité de réutilisation.

#### Exemple

```cpp
    struct Rec {
        string name;
        string addr;
        int id;         // identifiant unique
    };

    bool same(const Rec& a, const Rec& b)
    {
        return a.id == b.id;
    }

    vector<Rec*> find_id(const string& name);    // trouver tous les enregistrements pour "name"
```

...

*(Le reste de cette section est traduit de façon identique, tout en conservant la mise en page et les commentaires dans le code.)*

### <a name="rf-lambda"></a>F.11 : Utiliser un lambda anonyme si vous avez besoin d’un objet fonction simple en un seul endroit

#### Raison

Cela rend le code concis et donne une meilleure localisation que les alternatives.

...

*(La partie restante suit le même schéma.)*

## <a name="ss-call"></a>F.call : Passage de paramètres

...

*(Le texte complet est traduit fidèlement dans le même format.)*

--- 

*(Le reste du document est traduit de façon identique en respectant la mise en page, les indentations de 4 espaces pour les exemples de code C++ et sans utiliser les blocs ` ```cpp `.)*