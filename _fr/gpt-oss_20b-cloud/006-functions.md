# <a name="s-functions"></a>F: Fonctions

Une fonction spécifie une action ou un calcul qui fait passer le système d'un état cohérent au suivant. C'est le bloc de construction fondamental des programmes.

Il doit être possible de nommer une fonction de manière significative, de spécifier les exigences de son argument et d'affirmer clairement la relation entre les arguments et le résultat. Une implémentation n'est pas une spécification. Essayez de penser ce que fait une fonction ainsi qu'à comment elle le fait.
Les fonctions sont la partie la plus critique dans la plupart des interfaces, consultez les règles d'interface.

**Résumé des règles de fonction :**

### Règles de définition

- [F.1 : “Package” les opérations significatives sous forme de fonctions soigneusement nommées](006-functions.md#rf-package)
- [F.2 : Une fonction doit effectuer une seule opération logique](006-functions.md#rf-logical)
- [F.3 : Gardez les fonctions courtes et simples](006-functions.md#rf-single)
- [F.4 : Si une fonction doit être évaluée à la compilation, déclarer `constexpr`](006-functions.md#rf-constexpr)
- [F.5 : Si votre fonction est très petite et critique en terme de temps, déclarer `inline`](006-functions.md#rf-inline)
- [F.6 : Si votre fonction ne doit pas lever d'exception, déclarer `noexcept`](006-functions.md#rf-noexcept)
- [F.7 : Pour un usage général, prendre `T*` ou `T&` plutôt que des pointeurs intelligents](006-functions.md#rf-smart)
- [F.8 : Préférez les fonctions pures](006-functions.md#rf-pure)
- [F.9 : Les paramètres inutilisés doivent rester non nommés](006-functions.md#rf-unused)
- [F.10 : Si une opération peut être réutilisée, donnez-lui un nom](006-functions.md#rf-name)
- [F.11 : Utilisez une lambda anonyme si vous avez besoin d'un simple objet fonctionnel en un seul lieu](006-functions.md#rf-lambda)

### Règles d'expression de passage de paramètres

- [F.15 : Préférez les façons simples et conventionnelles de transmettre les informations](006-functions.md#rf-conventional)
- [F.16 : Pour les paramètres « in », passer les types à copie légère par valeur et les autres par référence à `const`](006-functions.md#rf-in)
- [F.17 : Pour les paramètres « in‑out », passer par référence à non‑`const`](006-functions.md#rf-inout)
- [F.18 : Pour les paramètres « will‑move‑from », passer par `X&&` et appeler `std::move` sur le paramètre](006-functions.md#rf-consume)
- [F.19 : Pour les paramètres « forward », passer par `TP&&` et ne `std::forward` que le paramètre](006-functions.md#rf-forward)
- [F.20 : Pour les valeurs de sortie, privilégier les valeurs de retour aux paramètres de sortie](006-functions.md#rf-out)
- [F.21 : Pour retourner plusieurs valeurs de sortie, préférer une structure de retour](006-functions.md#rf-out-multi)
- [F.60 : Préférez `T*` à `T&` quand « aucun argument » est une option valide](006-functions.md#rf-ptr-ref)

### Règles de sémantique de passage de paramètres

- [F.22 : Utilisez `T*` ou `owner<T*>` pour désigner un seul objet](006-functions.md#rf-ptr)
- [F.23 : Utilisez `not_null<T>` pour indiquer que « null » n'est pas une valeur valide](006-functions.md#rf-nullptr)
- [F.24 : Utilisez `span<T>` ou `span_p<T>` pour désigner une séquence à demi‑ouverte](006-functions.md#rf-range)
- [F.25 : Utilisez `zstring` ou `not_null<zstring>` pour désigner une chaîne de type C](006-functions.md#rf-zstring)
- [F.26 : Utilisez `unique_ptr<T>` pour transmettre la propriété lorsqu'un pointeur est requis](006-functions.md#rf-unique_ptr)
- [F.27 : Utilisez `shared_ptr<T>` pour partager la propriété](006-functions.md#rf-shared_ptr)

<a name="rf-value-return"></a>Valeurs de retour sémantiques :

- [F.42 : Retourner un `T*` pour indiquer une position (uniquement)](006-functions.md#rf-return-ptr)
- [F.43 : Ne jamais (directement ou indirectement) retourner un pointeur ou une référence à un objet local](006-functions.md#rf-dangle)
- [F.44 : Retourner un `T&` quand la copie est indésirable et qu'on n'a pas besoin de « retourner aucun objet »](006-functions.md#rf-return-ref)
- [F.45 : Ne pas retourner un `T&&`](006-functions.md#rf-return-ref-ref)
- [F.46 : `int` est le type de retour de `main()`](006-functions.md#rf-main)
- [F.47 : Retourner un `T&` des opérateurs d'assignation](006-functions.md#rf-assignment-op)
- [F.48 : Ne pas retourner `std::move(local)`](006-functions.md#rf-return-move-local)
- [F.49 : Ne pas retourner `const T`](006-functions.md#rf-return-const)

### Autres règles de fonction

- [F.50 : Utilisez une lambda quand une fonction ne le fera pas (pour capturer des variables locales ou écrire une fonction locale)](006-functions.md#rf-capture-vs-overload)
- [F.51 : Quand il y a un choix, privilégier les arguments par défaut sur le surchargage](006-functions.md#rf-default-args)
- [F.52 : Préférer les captures par référence dans les lambdas utilisées localement, y compris les algorithmes](006-functions.md#rf-reference-capture)
- [F.53 : Éviter les captures par référence dans les lambdas utilisées hors de portée locale (retournées, stockées ou transférées à un autre thread)](006-functions.md#rf-value-capture)
- [F.54 : Quand vous écrivez une lambda capturant `this` ou un membre de classe, ne pas utiliser la capture par défaut `[=]`](006-functions.md#rf-this-capture)
- [F.55 : Ne pas utiliser `va_arg`](006-functions.md#f-varargs)
- [F.56 : Éviter l'imbrication inutile des conditions](006-functions.md#f-nesting)

Les fonctions ont de fortes similitudes avec les lambdas et les objets fonctionnels.

**Voir également** : [C.lambdas : Objets fonctionnels et lambdas](007-class.md#ss-lambdas)

## <a name="ss-fct-def"></a>F.def : Définitions de fonction

Une définition de fonction est une déclaration de fonction qui spécifie également la mise en œuvre et le corps de la fonction.

### <a name="rf-package"></a>F.1 : « Package » les opérations significatives sous forme de fonctions soigneusement nommées

#### Raison

Factoriser le code commun rend le code lisible, la réutilisation probable et limite les erreurs de code trop complexe.  
Si quelque chose est une action bien définie, séparez‑le du code environnant et donnez‑lui un nom.

#### Exemple, mauvais

    void read_and_print(istream& is)    // read and print an int
    {
        int x;
        if (is >> x)
            cout << "the int is " << x << '\n';
        else
            cerr << "no int on input\n";
    }

Presque tout est faux avec `read_and_print`.  
Elle lit, elle écrit (à un `ostream` fixe), elle écrit des messages d'erreur (à un `ostream` fixe), elle ne prend que les `int`.  
Il n'y a rien à réutiliser, les opérations logiques sont mêlées et les variables locales restent accessibles après la fin logique.  
Pour un exemple minuscule, c'est correct, mais si les opérations d'entrée, de sortie et de gestion d'erreur étaient plus compliquées, le désordre pourrait devenir difficile à comprendre.

#### Note

Si vous écrivez une lambda non triviale pouvant être utilisée en plusieurs endroits, donnez‑lui un nom en l'affectant à une variable (généralement non locale).

#### Exemple

    sort(a, b, [](T x, T y) { return x.rank() < y.rank() && x.value() < y.value(); });

Nommer cette lambda découpe l'expression en ses parties logiques et donne un indice fort sur la signification de la lambda.

    auto lessT = [](T x, T y) { return x.rank() < y.rank() && x.value() < y.value(); };

    sort(a, b, lessT);

Le code le plus court n'est pas toujours le meilleur en termes de performance ou de maintenabilité.

#### Exception

Les corps de boucle, y compris les lambdas utilisées comme corps de boucle, n'ont rarement besoin d'être nommés.  
Cependant, les gros corps de boucle (plusieurs dizaines de lignes ou de pages) peuvent devenir problématiques.  
La règle [Gardez les fonctions courtes et simples](006-functions.md#rf-single) implique « gardez les corps de boucle courts ».  
De même, les lambdas utilisées comme arguments de rappel peuvent être non triviales, mais peu susceptibles d'être réutilisées.

#### Enforcement

- Voir [Gardez les fonctions courtes et simples](006-functions.md#rf-single)
- Marquer les lambdas identiques ou très similaires utilisées à différents endroits.

### <a name="rf-logical"></a>F.2 : Une fonction doit effectuer une seule opération logique

#### Raison

Une fonction effectuant une seule opération est plus simple à comprendre, à tester et à réutiliser.

#### Exemple

Considérons :

    void read_and_print()    // bad
    {
        int x;
        cin >> x;
        // check for errors
        cout << x << "\n";
    }

Ceci est un monolithe lié à une entrée spécifique et jamais réutilisable. Au lieu de cela, fractionnez la fonction en parties logiques appropriées et paramétrez :

    int read(istream& is)    // better
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

Ces fonctions peuvent maintenant être combinées où il faut :

    void read_and_print()
    {
        auto x = read(cin);
        print(cout, x);
    }

Si besoin, on pourrait encore généraliser `read()` et `print()` sur le type, le mécanisme d'I/O, la gestion d'erreur, etc. Exemple :

    auto read = [](auto& input, auto& value)    // better
    {
        input >> value;
        // check for errors
    };

    void print(auto& output, const auto& value)
    {
        output << value << "\n";
    }

#### Enforcement

- Considérer les fonctions avec plus d'un paramètre « out » suspect; utilisez les valeurs de retour, y compris un `tuple` pour plusieurs valeurs de retour.
- Considérer les fonctions trop volumineuses qui ne tiennent pas sur une fenêtre d'éditeur comme suspectes; factorisez‑les.
- Considérer les fonctions ayant 7 paramètres ou plus comme suspectes.

### <a name="rf-single"></a>F.3 : Gardez les fonctions courtes et simples

#### Raison

Les fonctions volumineuses sont difficiles à lire, plus susceptibles de contenir du code complexe, et ont plus de chances d'avoir des variables en portée plus large que nécessaire.  
Les fonctions avec des structures de contrôle complexes ont plus de chances d'être longues et de dissimuler des erreurs logiques.

#### Exemple

Considérons :

    double simple_func(double val, int flag1, int flag2)
        // simple_func: takes a value and calculates the expected ASIC output,
        // given the two mode flags.
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

C'est trop complexe.  
Comment savoir si toutes les alternatives possibles ont été correctement traitées ? Oui, cela enfreint aussi d'autres règles.

Refactorisation :

    double func1_muon(double val, int flag)
    {
        // ???
    }

    double func1_tau(double val, int flag1, int flag2)
    {
        // ???
    }

    double simple_func(double val, int flag1, int flag2)
        // simple_func: take a value and compute the expected ASIC output,
        // given the two mode flags.
    {
        if (flag1 > 0)
            return func1_muon(val, flag2);
        if (flag1 == -1)
            // handled by func1_tau: flag1 = -flag1;
            return func1_tau(-val, flag1, flag2);
        return 0.;
    }

#### Note

« Il ne tient pas sur l'écran » est souvent une bonne définition pratique de « trop grand ».  
Les fonctions d'une à cinq lignes sont considérées comme normales.

#### Note

Diviser les fonctions volumineuses en fonctions cohésives et bien nommées plus petites.  
Les petites fonctions simples peuvent être en ligne quand l'appel de fonction est coûteux.

#### Enforcement

- Marquer les fonctions qui ne tiennent pas sur une fenêtre d'écran.  
  Combien est une fenêtre ? Essayez 60 lignes par 140 caractères ; c'est à peu près la limite confortable pour une page de livre.
- Marquer les fonctions trop complexes.  
  Utilisez la complexité cyclomatique. Essayez « plus de 10 chemins logiques ».  
  Comptez un `switch` simple comme un chemin.

### <a name="rf-constexpr"></a>F.4 : Si une fonction doit être évaluée à la compilation, déclarer `constexpr`

#### Raison

`constexpr` est nécessaire pour dire au compilateur d'autoriser l'évaluation à la compilation.

#### Exemple

Le (in)fam's factorial :

    constexpr int fac(int n)
    {
        constexpr int max_exp = 17;      // constexpr permet d'utiliser max_exp dans Expects
        Expects(0 <= n && n < max_exp);  // empêcher l'absurde et les dépassements
        int x = 1;
        for (int i = 2; i <= n; ++i) x *= i;
        return x;
    }

C'est du C++14.  
Pour le C++11, utilisez une formulation récursive de `fac()`.

#### Note

`constexpr` ne garantit pas l'évaluation à la compilation ; il garantit simplement qu'une fonction peut être évaluée à la compilation pour des arguments en expression constante si le programmeur le requiert ou que le compilateur décide d'optimiser.

    constexpr int min(int x, int y) { return x < y ? x : y; }

    void test(int v)
    {
        int m1 = min(-1, 2);            // probablement évaluation à la compilation
        constexpr int m2 = min(-1, 2);  // évaluation à la compilation
        int m3 = min(-1, v);            // évaluation à l'exécution
        constexpr int m4 = min(-1, v);  // erreur : impossible à évaluer à la compilation
    }

#### Note

Ne tentez pas de rendre toutes les fonctions `constexpr`.  
La plupart des calculs sont mieux faits à l'exécution.

#### Note

Toute API dépendant potentiellement d'une configuration d'exécution ou de logique métier ne doit pas être rendue `constexpr`.  
Une telle personnalisation ne peut pas être évaluée par le compilateur, et tout `constexpr` dépendant de cette API devrait être refactorisé ou abandonné.

#### Enforcement

Impossible et inutile.  
Le compilateur signale déjà toute fonction non `constexpr` utilisée où une constante est requise.

### <a name="rf-inline"></a>F.5 : Si une fonction est très petite et critique en terme de temps, déclarer `inline`

#### Raison

Certains optimiseurs sont capables d'en‑ligne sans indication, mais on ne doit pas compter sur eux.  
MÉRIEZ !  
Au cours des 40 dernières années, on vous a promis des compilateurs capables d'en‑ligne mieux que les humains sans indices humains.  
Nous attendons encore.  
Faire « inline » (explicite ou implicite quand on écrit les membres de classe dans la définition de la classe) encourage le compilateur à faire un meilleur travail.

#### Exemple

    inline string cat(const string& s, const string& s2) { return s + s2; }

#### Exception

Ne placez pas une fonction `inline` dans une interface stable tant que vous n'êtes pas certain qu'elle ne changera pas.  
Une `inline` fait partie de l'ABI.

#### Note

`constexpr` implique `inline`.

#### Note

Les membres de classe définis dans la définition d'une classe sont `inline` par défaut.

#### Exception

Les modèles de fonctions (ex. `A<T>::function()` et `A::function<T>()`) sont normalement définis dans des fichiers d'en‑tête, donc ils sont `inline`.

#### Note

Envisagez de rendre hors ligne les fonctions de plus de trois instructions et pouvant être déclarées hors ligne (ex. des membres de classe).

### <a name="rf-noexcept"></a>F.6 : Si votre fonction ne doit pas lever d'exception, déclarer `noexcept`

#### Raison

Si une exception n'est pas supposée survenir, le programme ne peut pas traiter l'erreur. Il devrait s'arrêter dès que possible.  
Déclarer `noexcept` aide les optimiseurs en réduisant le nombre de chemins alternatifs. Il accélère aussi la sortie après un échec.

#### Exemple

Mettez `noexcept` sur chaque fonction entièrement écrite en C ou sans exceptions.  
La bibliothèque C++ le fait implicitement pour toutes les fonction de la bibliothèque C.

#### Note

`constexpr` peut lever à l'exécution; un `noexcept` conditionnel peut être nécessaire pour certaines d'elles.

#### Exemple

    vector<string> collect(istream& is) noexcept
    {
        vector<string> res;
        for (string s; is >> s;)
            res.push_back(s);
        return res;
    }

Si `collect()` se retrouve à court de mémoire, le programme plante.  
À moins que le programme ne soit conçu pour survivre à un manque de mémoire, c'est peut-être le bon comportement ; `terminate()` pourrait créer des logs appropriés (mais après épuisement de la mémoire il est difficile d'agir).

#### Note

Vous devez connaître l'environnement d'exécution.  
Le code doit supporter les environnements où une `bad_alloc` peut être traitée de façon significative.  
Dans la plupart des programmes, la plupart des fonctions peuvent lever (ex. via `new`, appel de fonctions externes).  
Ne répandez pas `noexcept` sans raison.

`noexcept` est le plus utile pour les fonctions fréquemment dribblées à bas niveau.

#### Note

Les destructeurs, `swap`, les opérations de déplacement, et les constructeurs par défaut ne doivent jamais lever d'exception.  
Voir aussi [C.44](007-class.md#rc-default00).

#### Note

Attention aux fonctions virtuelles de base ou publiques : déclarer une fonction `noexcept` impose qu'aucune implémentation future ne lèvera d'exception. Les redéfinitions doivent être `noexcept` aussi et retirer le `noexcept` peut casser les appelants.

#### Enforcement

- (Amplifier) Marquer les fonctions de bas niveau qui ne lèvent pas mais ne sont pas `noexcept`.
- Marquer les `swap`, `move`, destructeurs, constructeurs par défaut qui lèvent.

### <a name="rf-smart"></a>F.7 : Pour usage général, prendre `T*` ou `T&` plutôt que pointeurs intelligents

#### Raison

Passer un pointeur intelligent transfère ou partage la propriété.  
Une fonction qui ne manipule pas la durée de vie devrait prendre des pointeurs ou références bruts.

Passer par un pointeur intelligent limite l'usage à des appelants qui utilisent sie pointeur intelligent.  
Une fonction voulant un `widget` devrait accepter n'importe quel `widget`, pas seulement ceux dont la durée de vie est gérée par un pointeur intelligent particulier.

Passer un `shared_ptr` implique un coût d'exécution.

#### Exemple

    // accepte n'importe quel int*
    void f(int*);

    // ne accepte que les ints dont la possession est transférée
    void g(unique_ptr<int>);

    // ne accepte que les ints dont la possession est partagée
    void g(shared_ptr<int>);

    // ne change pas la propriété, mais exige une certaine propriété de l'appelant
    void h(const unique_ptr<int>&);

    // accepte n'importe quel int
    void h(int&);

#### Exemple, mauvais

    // callee
    void f(shared_ptr<widget>& w)
    {
        // ...
        use(*w); // seule utilisation: la durée n'est pas manipulée
        // ...
    };

    // caller
    shared_ptr<widget> my_widget = /* ... */;
    f(my_widget);

    widget stack_widget;
    f(stack_widget); // error

#### Exemple, good

    // callee
    void f(widget& w)
    {
        // ...
        use(w);
        // ...
    };

    // caller
    shared_ptr<widget> my_widget = /* ... */;
    f(*my_widget);

    widget stack_widget;
    f(stack_widget); // ok.

#### Note

Nous pouvons attraper de nombreuses erreurs courantes de pointeurs pendants via l'analyse de la durée de vie.  
Les arguments de fonction vivent naturellement à la durée d'appel, donc moins d'erreurs de durée de vie.

#### Enforcement

- (Simple) Avertir si une fonction prend un paramètre d'un type pointeur intelligent (surcharge d'`operator->` ou `operator*`) qui est copiable mais la fonction ne fait qu'appeler `operator*`, `operator->` ou `get()`.  
Suggérer d'utiliser `T*` ou `T&`.

- Marquer un paramètre de type pointeur intelligent qui est copiable/movable mais n'est jamais copié/mouillé, jamais modifié et n'est jamais passé vers une fonction pouvant le faire.  
La sémantique de propriété n'est pas utilisée.  
Suggérer un `T*` ou `T&`.

**Voir aussi** :

- [Utiliser `T*` plutôt que `T&` quand « aucun argument » est une option valide](006-functions.md#rf-ptr-ref)
- [Règle résumé pointeurs intelligents](009-resource.md#rr-summary-smartptrs)

### <a name="rf-pure"></a>F.8 : Préférez les fonctions pures

#### Raison

Les fonctions pures sont plus faciles à comprendre, parfois plus faciles à optimiser (et même paralléliser), et parfois mémoisables.

#### Exemple

    template<class T>
    auto square(T t) { return t * t; }

#### Enforcement

Impossible.

### <a name="rf-unused"></a>F.9 : Les paramètres inutilisés doivent rester non nommés

#### Raison

Lisibilité. Suppression des avertissements de paramètre inutilisé.

#### Exemple

    widget* find(const set<widget>& s, const widget& w, Hint);   // une fois qu'on utilisait un Hint

#### Note

Permettre que des paramètres restent non nommés a été introduit dans les années 80.

Si des paramètres sont conditionnellement inutilisés, utilisez `[[maybe_unused]]`:

    template <typename Value>
    Value* find(const set<Value>& s, const Value& v, [[maybe_unused]] Hint h)
    {
        if constexpr (sizeof(Value) > CacheSize)
        {
            // un Hint ne sert que si Value a une certaine taille
        }
    }

#### Enforcement

Marquer les paramètres inutilisés nommés.

### <a name="rf-name"></a>F.10 : Si une opération peut être réutilisée, donnez‑lui un nom

#### Raison

Documentation, lisibilité, opportunité de réutilisation.

#### Exemple

    struct Rec {
        string name;
        string addr;
        int id;         // unique identifier
    };

    bool same(const Rec& a, const Rec& b)
    {
        return a.id == b.id;
    }

    vector<Rec*> find_id(const string& name);    // find all records for "name"

    auto x = find_if(vr.begin(), vr.end(),
        [&](Rec& r) {
            if (r.name.size() != n.size()) return false; // name to compare to is in n
            for (int i = 0; i < r.name.size(); ++i)
                if (tolower(r.name[i]) != tolower(n[i])) return false;
            return true;
        }
    );

Il y a une fonction utile ici (comparaison insensible à la casse), alors que la lambda peut devenir trop lourde.

    bool compare_insensitive(const string& a, const string& b)
    {
        if (a.size() != b.size()) return false;
        for (int i = 0; i < a.size(); ++i) if (tolower(a[i]) != tolower(b[i])) return false;
        return true;
    }

    auto x = find_if(vr.begin(), vr.end(),
        [&](Rec& r) { return compare_insensitive(r.name, n); }
    );

Ou si vous préférez éviter le binding implicite de `n` :

    auto cmp_to_n = [&n](const string& a) { return compare_insensitive(a, n); };

    auto x = find_if(vr.begin(), vr.end(),
        [](const Rec& r) { return cmp_to_n(r.name); }
    );

#### Note

Que ce soient des fonctions, des lambdas ou des opérateurs.

#### Exception

- Lambdas uniquement localisées (ex. argument de `for_each` et autres algorithmes).
- Lambdas en tant qu'initialisateurs.

#### Enforcement

- (Hard) Marquer les lambdas semblables.
- ???

### <a name="rf-lambda"></a>F.11 : Utilisez une lambda anonyme si vous avez besoin d'un simple objet fonctionnel en un seul lieu

#### Raison

Cela rend le code plus concis et donne une meilleure localisation que les alternatives.

#### Exemple

    auto earlyUsersEnd = std::remove_if(users.begin(), users.end(),
                                        [](const User &a) { return a.id > 100; });

#### Exception

Nommer une lambda peut être utile pour clarifier même si elle n'est utilisée qu'une fois.

#### Enforcement

- Rechercher les lambdas identiques ou quasi‑identiques (à remplacer par des fonctions nommées ou des lambdas nommées).

## <a name="ss-call"></a>F.call : Passage de paramètres

Il existe une variété de manières de passer des paramètres à une fonction et de retourner des valeurs.

### <a name="rf-conventional"></a>F.15 : Préférer les voies simples et conventionnelles de transmission des informations

#### Raison

L'utilisation de techniques « inhabituées et ingénieuses » peut surprendre, ralentir la compréhension et encourager les bugs.  
Si vous avez vraiment besoin d'une optimisation au-delà de techniques courantes, mesurez pour assurer qu'elle est réellement bénéfique, et documentez/commentaire car l'amélioration peut ne pas être portable.

Les tableaux ci-dessous résument la recommandation pour F.16‑21.

Passage de paramètres normal :

![Normal parameter passing table](./param-passing-normal.png "Normal parameter passing")

Avancement de paramètres avancés :

![Advanced parameter passing table](./param-passing-advanced.png "Advanced parameter passing")

Utilisez les techniques avancées seulement après démonstration de besoin, et documentez ce besoin dans un commentaire.

Pour le passage de séquences de caractères, voir [String](018-stdlib.md#ss-string).

#### Exception

Pour exprimer la propriété partagée à l'aide de types `shared_ptr` plutôt que de suivre F.16‑21, suivez [R.34](009-resource.md#rr-sharedptrparam-owner), [R.35](009-resource.md#rr-sharedptrparam) et [R.36](009-resource.md#rr-sharedptrparam-const).

### <a name="rf-in"></a>F.16 : Pour les paramètres « in », passer les types copiables par valeur, et les autres par référence à const

#### Raison

Les deux indiquent au déclarant que la fonction ne modifiera pas l'argument, et lentées la possibilité d'initialisation par rvalue.

« Copiable à un frais léger » dépend de l'architecture, mais deux ou trois mots (double, pointeur, référence) sont généralement les meilleurs à copier.  
Quand la copie est légère, rien ne bat la simplicité et la sécurité du copier, et pour les petits objets (jusqu'à deux ou trois mots) c'est plus rapide qu'une référence car cela évite une indirection.

#### Exemple

    void f1(const string& s);  // OK : référence à const, toujours léger

    void f2(string s);         // mauvais : potentiellement cher

    void f3(int x);            // OK : unbeatable

    void f4(const int& x);     // mauvais : surcharge d'accès dans f4()

Pour l'usage avancé (uniques), où vous avez vraiment besoin d'optimiser pour les rvalues passées à des paramètres « input‑only » :

* Si la fonction va sans condition se déplacer du paramètre, prenez‑le par `&&`. Voir [F.18](006-functions.md#rf-consume).
* Si la fonction sera simplement garder une copie modifiable localement pour un usage interne, passer par valeur est suffisant.
* Si la fonction conserve une copie à passer à une autre destination (ex : autre fonction, ou stocker dans une zone non locale) en plus de `const&` (pour les lvalues), ajoutez une surcharge utilisant `&&` (pour les rvalues) et faites-mover dans sa destination. Cela surcharge un « will‑move‑from ».
* Dans certains cas, comme plusieurs « input + copy » paramètres, envisagez le « perfect forwarding » (Voir [F.19](006-functions.md#rf-forward)).

#### Exemple

    int multiply(int, int); // just input ints, pass by value

    // suffixe est input‑only mais pas aussi léger qu'un int, passer par const&
    string& concatenate(string&, const string& suffix);

    void sink(unique_ptr<widget>);  // input only, and move out the widget

Éviter les techniques « esotériques » comme passer les arguments en `T&&` pour efficacité.  
La plupart des rumeurs d'avantage de performance avec `T&&` sont fausses ou fragiles (mais voir [F.18](006-functions.md#rf-consume) et [F.19](006-functions.md#rf-forward)).

#### Notes

Une référence peut être supposée référencer un objet valide (règle du langage).  
Il n'y a pas de « référence nulle » valide.  
Si vous avez besoin d'une valeur optionnelle, utilisez un pointeur, `std::optional` ou une valeur spéciale indiquant « pas de valeur ».

#### Enforcement

- (Simple) ((Foundation)) Avertir lorsqu'un paramètre passé par valeur dépasse `4 * sizeof(void*)`.  
Suggérer l'usage d'une référence à const à la place.
- (Simple) ((Foundation)) Avertir lorsqu'un paramètre passé par référence à const a une taille ≤ `2 * sizeof(void*)`.  
Suggérer de passer par valeur.
- (Simple) ((Foundation)) Avertir lorsqu'un paramètre passé par référence à const est déplacé (`moved`).
- (Non simple) Note : une enforcement plus stricte dépendrait des caractéristiques de performance de la cible.

#### Exception

Pour exprimer la propriété partagée à l'aide de types `shared_ptr`, suivez [R.34](009-resource.md#rr-sharedptrparam-owner) ou [R.36](009-resource.md#rr-sharedptrparam-const), selon que la fonction ne prend pas une référence à l'argument sans condition.

### <a name="rf-inout"></a>F.17 : Pour les paramètres « in‑out », passer par référence à non‑const

#### Raison

Cela indique aux appelants que l'objet est supposé être modifié.

#### Exemple

    void update(Record& r);  // suppose que update écrit sur r

#### Note

Les types définis par l'utilisateur comme `span<T>` ou les itérateurs sont [léger à copier](006-functions.md#rf-in) et peuvent être passés par valeur avec la même sémantique mutable (in‑out) :

    void increment_all(span<int> a)
    {
        for (auto&& e : a)
            ++e;
    }

#### Note

Une `T&` peut transmettre des informations en entrée et en sortie.  
C'est un problème potentiel et source d'erreurs :

    void f(string& s)
    {
        s = "New York";  // erreur non évidente
    }

    void g()
    {
        string buffer = ".................................";
        f(buffer);
        // ...
    }

Ici, l'auteur de `g()` fournit un tampon que `f()` doit remplir, mais `f()` le remplace alors qu'on attendrait un remplissage.

#### Enforcement

- (Moderate) ((Foundation)) Avertir les fonctions concernant références à non‑const qui ne les écrivent pas.
- (Simple) ((Foundation)) Avertir lorsqu'un paramètre non‑const passé par référence est déplacé.

### <a name="rf-consume"></a>F.18 : Pour les paramètres « will‑move‑from », passer par `X&&` et `std::move` le paramètre

#### Raison

C'est efficient et élimine les bugs au niveau d'appel : `X&&` se lie à des rvalues, ce qui nécessite un explicit `std::move` à l'appel si on passe une lvalue.

#### Exemple

    void sink(vector<int>&& v)  // sink prend la propriété de tout ce qui était possédé
    {
        // généralement il y a des accès const de v ici
        store_somewhere(std::move(v));
        // généralement plus d'usage de v; elle est déplacée
    }

`std::move(v)` permet à `store_somewhere()` de laisser `v` dans un état déplacé.  
[Cela peut être dangereux](007-class.md#rc-move-semantic).

#### Exception

Les types propriétaires uniques (`unique_ptr`) qui sont movables et légers peuvent être passés par valeur, ce qui est plus simple à écrire et a le même effet.  
Passer par valeur génère une étape de déplacement supplémentaire (légère), mais privilégie la simplicité et la clarté d'abord.

```cpp
template<class T>
void sink(std::unique_ptr<T> p)
{
    // utilisez p ... peut-être std::move(p) ailleurs
}
```

#### Exception

Si le paramètre « will‑move‑from » est un `shared_ptr`, suivez [R.34](009-resource.md#rr-sharedptrparam-owner) et passez le `shared_ptr` par valeur.

#### Enforcement

- Marquer les paramètres `X&&` (où `X` n'est pas un nom de paramètre de modèle) dont le corps ne les utilise pas avec `std::move`.
- Marquer l'accès aux objets déplacés.
- Ne pas déplacer conditionnellement des objets.

### <a name="rf-forward"></a>F.19 : Pour les paramètres « forward », passer par `TP&&` et seulement `std::forward` le paramètre

#### Raison

Si l'objet doit être transmis à un autre code et non utilisé directement, nous voulons rendre cette fonction indépendante du `const`‑ness et du rvalue‑ness de l'argument.

Dans ce cas, et seulement dans ce cas, faites que le paramètre soit `TP&&` où `TP` est un paramètre de type modèle ; cela ignore et préserve simultanément `const`‑ness et rvalue‑ness.  
Tout code utilisant un `TP&&` indique implicitement qu'il ne se soucie pas du `const`‑ness et qu'il souhaite le transmettre à d'autres code qui le fera.  

#### Exemple

En général, vous transférerez l'intégralité du paramètre (ou paquet de paramètres via `...`) exactement une fois sur chaque chemin de contrôle statique :

    template<class F, class... Args>
    inline decltype(auto) invoke(F&& f, Args&&... args)
    {
        return forward<F>(f)(forward<Args>(args)...);
    }

#### Exemple

Vous pouvez parfois transférer un paramètre composite partiellement, chaque sous‑objet une seule fois sur chaque chemin statique :

    template<class PairLike>
    inline auto test(PairLike&& pairlike)
    {
        // ...
        f1(some, args, and, forward<PairLike>(pairlike).first);           // forward .first
        f2(and, forward<PairLike>(pairlike).second, in, another, call);   // forward .second
    }

#### Enforcement

- Marquer une fonction qui prend un paramètre `TP&&` (où `TP` est un paramètre de type modèle) et fait autre chose que `std::forward` exactement une fois sur chaque chemin, ou `std::forward` plusieurs fois mais avec un membre différent exactement une fois sur chaque chemin.

### <a name="rf-out"></a>F.20 : Pour les valeurs de sortie, privilégier les valeurs de retour aux paramètres de sortie

#### Raison

Une valeur de retour est autonome, tandis qu'un `&` peut être d'entrée‑sortie ou seulement de sortie et peut être mal utilisé.

Ceci inclut les gros objets comme les conteneurs standard qui utilisent des mouvements implicites pour les performances et éviter la gestion de mémoire explicite.

Si vous avez plusieurs valeurs à retourner, utilisez un `tuple` ou une structure multimembre.  

#### Exemple

    // OK : retourner des pointeurs vers les éléments avec la valeur x
    vector<const int*> find_all(const vector<int>&, int x);

    // Mauvais : placer les pointeurs des éléments avec valeur x dans un paramètre « out »
    void find_all(const vector<int>&, vector<const int*>& out, int x);

#### Note

Une structure contenant plusieurs éléments (tous individuellement faciles à déplacer) peut être relativement coûteuse à déplacer globalement.

#### Exceptions

- Pour les types non-concrets, tels que les types d'héritage, retourner l'objet par `unique_ptr` ou `shared_ptr`.
- Si un type est coûteux à déplacer (ex. `array<BigTrivial>`), envisagez d'allouer à l'heap et renvoyez un handle (ex. `unique_ptr`), ou le passer dans une référence à un objet cible non‑const à remplir (utiliser comme paramètre de sortie).
- Pour réutiliser un objet qui transporte la capacité (ex. `std::string`, `std::vector`) entre plusieurs appels à une fonction dans une boucle intérieure : [traiter comme un paramètre in‑out et passer par référence](006-functions.md#rf-out-multi).

#### Exemple

Supposons que `Matrix` ait des opérations de mouvement (peut-être en conservant ses éléments dans un `std::vector`) :

    Matrix operator+(const Matrix& a, const Matrix& b)
    {
        Matrix res;
        // ... fill res with the sum ...
        return res;
    }

    Matrix x = m1 + m2;  // constructeur de déplacement

    y = m3 + m3;         // assignation de déplacement

#### Note

L'optimisation de valeur de retour ne s'applique pas à la copie, mais l'assignation de déplacement cela.

#### Exemple

    struct Package {      // cas exceptionnel : objet coûteux à déplacer
        char header[16];
        char load[2024 - 16];
    };

    Package fill();       // Mauvais : grand valeur de retour
    void fill(Package&);  // OK

    int val();            // OK
    void val(int&);       // Mauvais : est val lisant son argument

#### Enforcement

- Marquer les références non‑const qui ne sont pas lues avant d'être écrites et qui sont un type pouvant être retourné ; elles devraient être des valeurs de sortie.

### <a name="rf-out-multi"></a>F.21 : Pour retourner plusieurs valeurs de sortie, privilégier la structure de retour

#### Raison

Une valeur de retour est autonome, et documentée comme valeur de sortie.  
Notez que C++ possède des retours multiples via les tuples, structures etc., et les avantages avec les bindings structurés en C++17.

#### Exemple

    // BAD : paramètre out documenté en commentaire
    int f(const string& input, /*output only*/ string& output_data)
    {
        // ...
        output_data = something();
        return status;
    }

    // GOOD : auto‑documenté
    struct f_result { int status; string data; };

    f_result f(const string& input)
    {
        // ...
        return {status, something()};
    }

Le style du standard library C++98 utilisait une structure `pair`, par exemple :

    // C++98
    pair<set::iterator, bool> result = my_set.insert("Hello");
    if (result.second)
        do_something_with(result.first);    // workaround

Avec C++17, on peut faire une liaison structurée :

    if (auto [ iter, success ] = my_set.insert("Hello"); success)
        do_something_with(iter);

Une structure avec des noms signifants reste plus courante aujourd'hui.

#### Exception

Particulièrement, quand vous voulez passer un objet à une fonction pour qu'il manipule son état. Dans ce cas, transmettre l'objet par référence `T&` est généralement la bonne technique. Retourner l'objet par valeur n'est souvent pas nécessaire.

#### Note

Dans la plupart des cas, il est utile de retourner un type personnalisé et spécifique.  
Un exemple :  

    struct Distance {
        int value;
        int unit = 1;   // 1 signifie mètre
    };

    Distance d1 = measure(obj1);
    auto d2 = measure(obj2);
    auto [ value, unit ] = measure(obj3);   // accessible, mais confus pour certains.

Une boîte générique comme `pair` ou `tuple` doit être utilisée uniquement quand les valeurs retournées représentent des entités indépendantes plutôt qu'une abstraction.

Une autre option est d'utiliser `optional<T>` ou `expected<T, error_code>` plutôt que `pair` ou `tuple`.

#### Note

Quand l'objet retourné est initialisé à partir de variables locales coûteuses à copier, l'utilisation explicite de `std::move` peut aider à éviter la copie :

    pair<LargeObject, LargeObject> f(const string& input)
    {
        LargeObject large1 = g(input);
        LargeObject large2 = h(input);
        // ...
        return { move(large1), move(large2) }; // pas de copies
    }

Ou encore :

    pair<LargeObject, LargeObject> f(const string& input)
    {
        // ...
        return { g(input), h(input) }; // pas de copies ni de moves
    }

#### Enforcement

- Les paramètres de sortie doivent être remplacés par des valeurs de retour.
- `pair` ou `tuple` doivent être remplacés par `struct` si possible.  
Pour les templates variadiques, les `tuple` sont parfois inévitables.

### <a name="rf-ptr-ref"></a>F.60 : Préférer `T*` à `T&` quand « aucun argument » est une option valide

#### Raison

Un pointeur (`T*`) peut être `nullptr` alors qu'une référence (`T&`) ne l'est pas.  
Avoir la possibilité d'`nullptr` pour indiquer « pas d'objet » est utile, mais si ce n'est pas le cas, une référence est simpler et peut exceller en termes de code.

#### Exemple

    string zstring_to_string(zstring p) // zstring est un `char*`; c'est une chaîne C
    {
        if (!p) return string{};    // p pourrait être nullptr; à vérifier
        return string{p};
    }

    void print(const vector<int>& r)
    {
        // r réfère à un vector<int>; pas de vérification nécessaire
    }

#### Note

Il est possible (mais pas valide en C++ de construire une référence qui représente `nullptr` (ex. `T* p=nullptr; T& r=*p;`).  
Cette erreur est très rare.

#### Note

Si vous préférez la notation pointeur (`->` ou `*`), `not_null<T*>` offre la même garantie qu'une référence.

#### Enforcement

- ...

### <a name="rf-ptr"></a>F.22 : Utiliser `T*` ou `owner<T*>` pour désigner un seul objet

#### Raison

Lisibilité : clarifier qu'un pointeur simple désigne un unique objet.  
Permet des soutiens importants d'outils.

#### Note

Dans le code C et C++ traditionnel, un pointeur simple est utilisé pour de multiples buts faibles :

* Identifier un objet unique (non à supprimer par la fonction)
* Pointe à un objet sur le tas (et le supprimer plus tard)
* Contenir `nullptr`
* Identifier une chaîne C
* Identifier un tableau dont la longueur est ailleurs
* Identifier un emplacement dans un tableau

Cela rend difficile de comprendre ce que fait le code et exige plus de vérification et d'outils.

#### Exemple

    void use(int* p, int n, char* s, int* q)
    {
        p[n - 1] = 666; // Mauvais : on ne sait pas si p pointe à n éléments
        cout << s;      // Mauvais : on ne sait pas si s pointe à une suite zerod terminée
        delete q;       // Mauvais : on ne sait pas si *q est alloué sur le tas
    }

Better :

    void use2(span<int> p, zstring s, owner<int*> q)
    {
        p[p.size() - 1] = 666; // OK, une erreur de range peut être détectée
        cout << s;              // OK
        delete q;               // OK
    }

#### Note

`owner<T*>` représente la propriété, `zstring` représente une chaîne de type C.

**See also** : [Support library](#gsl-guidelines-support-library)  
**See also** : [Ne pas passer un tableau comme un pointeur unique](005-interfaces.md#ri-array)

#### Enforcement

- (Simple) ((Bounds)) Avertir pour toute opération arithmétiques sur un pointeur qui produit un pointeur.

### <a name="rf-nullptr"></a>F.23 : Utiliser `not_null<T>` pour indiquer que « null » n'est pas une valeur valide

#### Raison

Clarté.  
Une fonction recevant un `not_null<T>` montre à l'appelant que `nullptr` n'est pas demandé.  
En retour, si une fonction renvoie `not_null<T>`, l'appelant n'a pas besoin de vérifier `nullptr`.

#### Exemple

`not_null<T*>` rend évident pour le lecteur que la vérification de `nullptr` n'est pas requise avant la deref.
Quand on debugge, `owner<T*>` et `not_null<T>` peuvent être instrumentés pour la vérification.

Considérons :

    int length(Record* p);

Quand j'appelle `length(p)`, devrais‑je vérifier `nullptr` ?  
The implementation doit-il vérifier ?

    // c'est le travail du appelant de s'assurer que `p != nullptr`
    int length(not_null<Record*> p);

    // l'implémentateur de `length()` doit supposer que `p` peut être `nullptr`
    int length(Record* p);

#### Note

`not_null<T*>` est supposé ne pas être le `nullptr`; un `T*` peut l'être; ils peuvent être représentés en mémoire de même façon sans surcharge d'exécution.

#### Note

`not_null` n'est pas seulement pour les pointeurs natifs. Ça marche aussi pour `unique_ptr`, `shared_ptr` et d'autres types semblables.

#### Enforcement

- (Simple) Avertir si un pointeur brut est dereférencé sans être testé contre `nullptr` (ou équivalent) dans une fonction; suggérer de déclarer `not_null` à la place.
- (Simple) Erreur si un pointeur brut est parfois dereférencé après un test, parfois non.
- (Simple) Avertir si un pointeur `not_null` est testé contre `nullptr` dans une fonction.

### <a name="rf-range"></a>F.24 : Utiliser `span<T>` ou `span_p<T>` pour désigner une séquence à demi‑ouverte

#### Raison

Les plages non explicites sont source d'erreurs.

#### Exemple

    X* find(span<X> r, const X& v);    // recherche v dans r

    vector<X> vec;
    // ...
    auto p = find({vec.begin(), vec.end()}, X{});  // find X{} in vec

#### Note

Les plages sont extrêmement courantes en C++ : elles sont implicites et leur utilisation correcte est très difficile à assurer.  
Par conséquent, on préfère explicitement passer un `span` ou `span_p`.

#### Exemple

`span` représente une plage d'éléments, mais comment manipuler ?

    void f(span<int> s)
    {
        // Parcours garanti correct
        for (int x : s) cout << x << '\n';

        // Parcours type C (peut être vérifié)
        for (gsl::index i = 0; i < s.size(); ++i) cout << s[i] << '\n';

        // Accès aléatoire (peut être vérifié)
        s[7] = 9;

        // Extraire pointeurs (peut être vérifié)
        std::sort(&s[0], &s[s.size() / 2]);
    }

#### Note

Un objet `span<T>` ne possède pas d'éléments et est si petit qu'il peut être passé par valeur.

#### See also

* [Support library](#gsl-guidelines-support-library)

#### Enforcement

- (Complex) Avertir lorsqu'on accède à un pointeur de paramètre limitée par un paramètre entier et suggérez un `span` à la place.

### <a name="rf-zstring"></a>F.25 : Utiliser `zstring` ou `not_null<zstring>` pour désigner une chaîne de type C

#### Raison

Les chaînes de type C sont omniprésentes.  
Il faut distinguer les chaînes terminées par `\0` de pointer à un caractère ou une ancienne chaîne.

Si vous n'avez pas besoin de terminaison, utilisez `string_view`.

#### Exemple

    int length(const char* p);

Quand j'appelle `length(s)`, devrais‑je vérifier `nullptr` ?  

    // Le concepteur de `length()` doit supposer que `p == nullptr` est possible
    int length(zstring p);

    // L'appelant doit s'assurer que `p != nullptr`
    int length(not_null<zstring> p);

#### Note

`zstring` ne représente pas la possession.

#### See also

* [Support library](#gsl-guidelines-support-library)

### <a name="rf-unique_ptr"></a>F.26 : Utiliser `unique_ptr<T>` pour transmettre la propriété quand un pointeur est requis

#### Raison

Utiliser `unique_ptr` est le moyen le plus économique de passer un pointeur en toute sécurité.

**See also** : [C.50](007-class.md#rc-factory) concernant quand retourner un `shared_ptr` d'une fabrique.

#### Exemple

    unique_ptr<Shape> get_shape(istream& is)  // assemble shape from input stream
    {
        auto kind = read_header(is);
        switch (kind) {
        case kCircle:
            return make_unique<Circle>(is);
        case kTriangle:
            return make_unique<Triangle>(is);
        // ...
        }
    }

#### Note

Vous devez passer un pointeur plutôt qu'un objet si vous transférez un objet d'une hiérarchie de classes à un interface (classe de base).

#### Enforcement

- (Simple) Avertir si une fonction retourne un pointeur brut alloué localement. Suggérer d'utiliser `unique_ptr` ou `shared_ptr`.

### <a name="rf-shared_ptr"></a>F.27 : Utiliser `shared_ptr<T>` pour partager la propriété

#### Raison

Utiliser `std::shared_ptr` est la façon standard de représenter la propriété partagée.  
La dernière propriétaire désalloue l'objet.

#### Exemple

    {
        shared_ptr<const Image> im { read_image(somewhere) };

        std::thread t0 {shade, args0, top_left, im};
        std::thread t1 {shade, args1, top_right, im};
        std::thread t2 {shade, args2, bottom_left, im};
        std::thread t3 {shade, args3, bottom_right, im};

        // détacher les threads nécessite extra vigilance (ex. rejoindre avant que le
        // programme ne se termine), mais même en detach, les threads partagent l'image
    }
    // ...

#### Note

Préférez un `unique_ptr` au lieu d'un `shared_ptr` s'il n'y a jamais plus d'un propriétaire à un instant.

Notez que l'utilisation généralisée de `shared_ptr` entraîne un coût (opérations atomiques sur le compteur).  

#### Alternative

Quevoir un unique propriétaire pour détruire l'objet partagés quand tous les utilisateurs ont fini.

#### Enforcement

Non réalisable; trop complexe à détecter.

### <a name="rf-return-ptr"></a>F.42 : Retourner un `T*` pour indiquer une position (uniquement)

#### Raison

C'est ce pour quoi les pointeurs sont bons.  
Retourner un `T*` pour transférer la propriété est une mauvaise pratique.

#### Exemple

    Node* find(Node* t, const string& s)  // find s in a binary tree of Nodes
    {
        if (!t || t->name == s) return t;
        if ((auto p = find(t->left, s))) return p;
        if ((auto p = find(t->right, s))) return p;
        return nullptr;
    }

Si ce n'est pas `nullptr`, le pointeur retourné indique un `Node` contenant `s`.  
Important : cela ne signifie pas transférer la possession du pointé au caller.

#### Note

La position peut aussi être transmise par des itérateurs, indices ou références.  
Une référence est souvent une meilleure alternative si pas besoin de `nullptr` ([F.60](006-functions.md#rf-ptr-ref)) ou si l'objet référencé ne doit pas changer ([014-const.md](014-const.md)).

#### Note

Ne pas retourner un pointeur vers quelque chose qui n'est pas dans le scope du caller ; voir [F.43](006-functions.md#rf-dangle).

**See also** : [discussion de la prévention des pointeurs tout‑ponctue](#???)

#### Enforcement

- Marquer `delete`, `std::free()` etc. appliqués à un pointeur brut.  
  Seuls les owners doivent être supprimés.
- Marquer `new`, `malloc()` etc. assignés à un pointeur brut.  
  Seuls les owners doivent être responsables de la suppression.

### <a name="rf-dangle"></a>F.43 : Ne jamais (directement ou indirectement) retourner un pointeur ou une référence vers un objet local

#### Raison

Éviter les plantages et la corruption de données qui résultent d'un pointeur ou d'une référence dangling.

#### Exemple, mauvais

Après le retour d'une fonction, ses objets locaux n'existent plus :

    int* f()
    {
        int fx = 9;
        return &fx;  // BAD
    }

    void g(int* p)   // semble innocent
    {
        int gx;
        cout << "*p == " << *p << '\n';
        *p = 999;
        cout << "gx == " << gx << '\n';
    }

    void h()
    {
        int* p = f();
        int z = *p;  // lecture depuis le frame de pile abandonné (bad)
        g(p);        // passer pointeur de frame abandonné à fonction (bad)
    }

#### Exemple, faux

    int* glob;       // variables globales sont mauvaises aussi

    template<class T>
    void steal(T x)
    {
        glob = x();  // BAD
    }

    void f()
    {
        int i = 99;
        steal([&] { return &i; });
    }

    int main()
    {
        f();
        cout << *glob << '\n';
    }

#### Note

Les pointeurs vers des variables locales peuvent également être retournés par une déclaration, en tant que paramètre `T&`, etc.

#### Enforcement

- Les compilateurs saisissent déjà la plupart des cas de retour de référence à un local et potentiellement de retour de pointeurs à un local.
- L'analyse statique peut détecter de nombreuses patterns courants de pointeurs indiquant des positions et éviter les pointeurs hors de portée.

### <a name="rf-return-ref"></a>F.44 : Retourner un `T&` quand la copie est indésirable et que « retourner aucun objet » n'est pas nécessaire

#### Raison

Le langage garantit qu'une `T&` fait référence à un objet, donc la vérification de `nullptr` n'est pas nécessaire.

**Voir aussi** : Le retour d'une référence ne doit pas impliquer un transfert de propriété : [discussion sur la prévention des pointeurs tout‑ponctue](#???) et [discussion sur la propriété](#???).

#### Exemple

    class Car
    {
        array<wheel, 4> w;
    public:
        wheel& get_wheel(int i) { Expects(i < w.size()); return w[i]; }
    };

    void use()
    {
        Car c;
        wheel& w0 = c.get_wheel(0); // w0 a la même durée que c
    }

#### Enforcement

Marquer les fonctions dont aucune expression de retour ne pourrait être `nullptr`.

### <a name="rf-return-ref-ref"></a>F.45 : Ne pas retourner un `T&&`

#### Raison

Il s'agit de retourner une référence vers un objet temporaire détruit.  
Les `&&` attirent les temporaires.

#### Exemple

Un retour d'une référence rvalue part de la portée finale d'une expression.

    auto&& x = max(0, 1);   // OK à présent
    foo(x);                 // comportement indéfini

Ce type de bug est fréquent, souvent mal signalé comme un bug de compilateur.

#### Exception

Retourner un rvalue est acceptable quand la référence vers le temporaire passe « downward » à un callee ; alors le temporaire est garanti de survivre à l'appel.  
Pour pendant, un retour de `auto&&` ne devrait pas être fait. Utilisez simplement `auto`.

#### Enforcement

Marquer toute utilisation d'un `&&` en tant que type de retour, sauf `std::move` ou `std::forward`.

### <a name="rf-main"></a>F.46 : `int` est le type de retour de `main()`

#### Raison

C'est une règle de langage, mais violée par des extensions.  
Déclarer `main()` comme `void` limite la portabilité.

#### Example

        void main() { /* ... */ };  // bad, not C++

        int main()
        {
            std::cout << "This is the way to do it\n";
        }

#### Enforcement

- Le compilateur doit le vérifier ;
- Si le compilateur ne le fait pas, le linter doit le signaler.

### <a name="rf-assignment-op"></a>F.47 : Retourner un `T&` de l'opérateur d'assignation

#### Raison

La convention pour les overloads d'opérateurs sur types concrets est de retourner `*this` non‑const après l'assignation.  
Cela suit les types standards et évite des constructions comme `(a = b) = c`.

#### Example

    class Foo
    {
    public:
        ...
        Foo& operator=(const Foo& rhs)
        {
            // Copy members
            ...
            return *this;
        }
    };

#### Enforcement

Le linter doit vérifier le type de retour et la valeur de tout opérateur d'assignation.

### <a name="rf-return-move-local"></a>F.48 : Ne pas `return std::move(local)`

#### Raison

Lorsque vous retournez une variable locale, le mouvement est implicite.  
Un explicit `std::move` est toujours une pessimisation, car il empêche l'optimisation de valeur de retour (RVO).

#### Exemple, bad

    S bad()
    {
      S result;
      return std::move(result);
    }

#### Exemple, good

    S good()
    {
      S result;
      // Named RVO
      return result;
    }

#### Enforcement

Le linter doit signaler le `return std::move(local)`.

### <a name="rf-return-const"></a>F.49 : Ne pas retourner `const T`

#### Raison

L'usage de `const` sur un retour ajoute un problème inutile.  
Le moteur de move est désactivé.

#### Exemple

    const vector<int> fct();    // bad

    void g(vector<int>& vx)
    {
        fct() = vx;            // interdit par `const`
        vx = fct();            // copie coûteuse
    }

#### Enforcement

- Marquer le retour `const`; corrigez en supprimant `const`.

### <a name="rf-capture-vs-overload"></a>F.50 : Utiliser une lambda lorsqu'une fonction ne le fera pas (pour capturer des variables locales, ou pour écrire une fonction locale)

#### Raison

Les fonctions ne peuvent capturer de variables locales ni être définies à l'intérieur d'une portée.  
Si vous avez besoin de ces caractéristiques, choisissez une lambda; si vous avez besoin de surcharge, utilisez une fonction.

#### Example

    // Fonction écrite pour prendre un int ou une string
    void f(int);
    void f(const string&);

    // Fonction objet qui doit capturer l'état local
    vector<work> v = lots_of_work();
    for (int tasknum = 0; tasknum < max; ++tasknum) {
        pool.run([=, &v] {
            // ...
            // traite une fraction du travail
        });
    }
    pool.join();

#### Exception

Les lambdas génériques sont concises puis sont utiles même lorsqu'un template régulier suffirait, mais la syntaxe s'améliorera avec les concepts.

#### Enforcement

- Avertir sur l'utilisation d'une lambda nommée sans capture qui est globale; préférer une fonction.

### <a name="rf-default-args"></a>F.51 : Quand il y a un choix, privilégier les arguments par défaut sur le surchargage

#### Raison

Les arguments par défaut offrent une interface cohérente à un seul implémentation.  
Le surchargage n'implémente pas forcément les mêmes comportements.

#### Note

Il y a un choix entre l'utilisation d'arguments par défaut et le surchargage ; non applicable quand il y a des fonctions complètement différentes.

#### Enforcement

- Avertir si un ensemble de surcharges partagent un préfixe commun de paramètres.

### <a name="rf-reference-capture"></a>F.52 : Préférer capture par référence dans les lambdas utilisées localement, y compris en passant à des algorithmes

#### Raison

Efficacité et correction : capture par valeur entraîne du copie inutile et évite les effets de bord.  
Capturer par référence dans un lambda local est donc plus correct.

#### Example

    std::for_each(begin(sockets), end(sockets), [&message](auto& socket)
    {
        socket.send(message);
    });

#### Example

Pipeline parallèle simple :

    void send_packets(buffers& bufs)
    {
        stage encryptor([](buffer& b) { encrypt(b); });
        stage compressor([&](buffer& b) { compress(b); encryptor.process(b); });
        stage decorator([&](buffer& b) { decorate(b); compressor.process(b); });
        for (auto& b : bufs) { decorator.process(b); }
    }  // le pipeline se termine avant de sortir

#### Enforcement

Avertir quand une lambda capture par référence tout de même est utilisée hors de la portée locale ou passé à une fonction par référence.

### <a name="rf-value-capture"></a>F.53 : Éviter les captures par référence dans les lambdas qui seront utilisées hors de la portée locale (retournées, stockées sur le heap, ou passées à un autre thread)

#### Raison

Les références locales ne doivent pas survivre hors de leur portée.  

#### Exemple, mauvais

    int local = 42;

    // Want a reference to local.
    // Note that after program exits this scope, local no longer exists,
    // so `process()` will have undefined behavior!
    thread_pool.queue_work([&] { process(local); });

#### Exemple, bon

    int local = 42;
    // Want a copy of local.
    // Since a copy is made, it always exists for call.
    thread_pool.queue_work([=] { process(local); });

#### Note

Si vous avez un pointeur non locale, envisagez `unique_ptr`; il gère l'énumération et la synchronisation.  
Si vous avez besoin de capturer `this`, utilisez `[&]` explicitement pour clarifier.

#### Enforcement

- (Simple) Avertir lorsque le champ de capture contient une référence à une variable locale.
- (Complex) Marquer lorsqu'une lambda capture par référence est passée à un contexte non‑const et hors de portée.

### <a name="rf-this-capture"></a>F.54 : Lors de la rédaction d'une lambda capturant `this` ou un membre de classe, ne pas utiliser la capture par défaut `[=]`

#### Raison

Il est confus. En utilisant `[=]` dans une méthode membre, il capture le pointeur `this` par valeur alors que les membres sont capturés par référence.  
Si l'intention est de copier les membres, exprimez‑le explicitement.

#### Example

    class My_class {
        int x = 0;
        // ...

        void f()
        {
            int i = 0;
            // ...

            auto lambda = [=] { use(i, x); };   // BAD: “looks like” copy/value capture

            x = 42;
            lambda(); // use(0, 42)
            x = 43;
            lambda(); // use(0, 43)

            // ...

            auto lambda2 = [i, this] { use(i, x); }; // ok
        }
    };

#### Note

Si vous souhaitez copier tous les membres de la classe, utilisez `[*this]` (C++17).

#### Enforcement

- Marquer toute liste de capture qui spécifie un capture‑défaut `[=]` et capture aussi `this`.

### <a name="f-varargs"></a>F.55 : Ne pas utiliser `va_arg`

#### Raison

Lire un `va_arg` suppose que le type correct a été passéd.  
Passer à un vararg suppose le type correcte sera lu. C'est fragile, pas vérifiable par le langage.

#### Example

    int sum(...)
    {
        // ...
        while (/*...*/)
            result += va_arg(list, int); // BAD
        // ...
    }

    sum(3, 2); // ok
    sum(3.14159, 2.71828); // BAD

    template<class ...Args>
    auto sum(Args... args) // GOOD
    {
        return (... + args);
    }

#### Alternatives

- surcharge
- variadic templates
- `variant` arguments
- `initializer_list`

#### Note

Déclarer un paramètre `...` est parfois utile comme catch‑all.

#### Enforcement

- Signaler l'utilisation de `va_list`, `va_start`, `va_arg`.
- Signaler l'appel d'un paramètre vararg sans surcharge pour le type.

### <a name="f-nesting"></a>F.56 : Éviter l'imbrication inutile des conditions

#### Raison

Un imbriquement de niveau profond contourne la lisibilité et cache l'intention.  
Mettre l'essentiel au niveau externe, sauf si cela masque la logique.

#### Exemple

Enbadonnage vertical :

    void foo() {
        // ...
        if (x) {
            computeImportantThings(x);
        }
    }

- Redondant else

    void foo() {
        // ...
        if (!x) {
            return;
        }
        else {
            computeImportantThings(x);
        }
    }

- Bon

    void foo() {
        // ...
        if (!x)
            return;

        computeImportantThings(x);
    }

#### Exemple

    void foo() {
        // ...
        if (x) {
            if (y) {
                computeImportantThings(x);
            }
        }
    }

- Bon

    void foo() {
        // ...
        if (!(x && y))
            return;

        computeImportantThings(x);
    }

#### Enforcement

- Signaler un else redondant.
- Signaler une fonction dont le corps est un unique bloc conditionnel.