# <a name="s-functions"></a>F : Fonctions

Une fonction spécifie une action ou un calcul qui fait passer le système d'un état cohérent à l'état suivant. C'est le bloc de construction fondamental des programmes.

Il doit être possible de nommer une fonction de manière significative, de spécifier les exigences de son argument, et d'énoncer clairement la relation entre les arguments et le résultat. Une implémentation n'est pas une spécification. Essayez de réfléchir à ce qu'une fonction fait, en plus de la manière dont elle le fait.
Les fonctions sont la partie la plus critique de la plupart des interfaces, voyez donc les règles d'interface.

Résumé des règles sur les fonctions :

Règles de définition de fonction :

* [F.1 : Encapsuler les opérations significatives dans des fonctions soigneusement nommées](006-functions.md#rf-package)
* [F.2 : Une fonction doit effectuer une seule opération logique](006-functions.md#rf-logical)
* [F.3 : Garder les fonctions courtes et simples](006-functions.md#rf-single)
* [F.4 : Si une fonction peut devoir être évaluée au moment de la compilation, la déclarer `constexpr`](006-functions.md#rf-constexpr)
* [F.5 : Si une fonction est très petite et critique en temps, la déclarer `inline`](006-functions.md006-functions.md#rf-inline)
* [F.6 : Si votre fonction ne doit pas lancer d'exception, la déclarer `noexcept`](006-functions.md#rf-noexcept)
* [F.7 : Pour un usage général, prendre des arguments `T*` ou `T&` plutôt que des pointeurs intelligents](006-functions.md#rf-smart)
* [F.8 : Privilégier les fonctions pures](006-functions.md#rf-pure)
* [F.9 : Les paramètres non utilisés doivent être sans nom](006-functions.md#rf-unused)
* [F.10 : Si une opération peut être réutilisée, lui donner un nom](006-functions.md#rf-name)
* [F.11 : Utiliser une lambda anonyme si vous avez besoin d'un simple objet fonctionnel à un seul endroit](006-functions.md#rf-lambda)

Règles d'expression de passage de paramètres :

* [F.15 : Privilégier les moyens simples et conventionnels de transmettre l'information](006-functions.md#rf-conventional)
* [F.16 : Pour les paramètres « en entrée », passer les types à copie économique par valeur et les autres par référence vers `const`](006-functions.md#rf-in)
* [F.17 : Pour les paramètres « en entrée/sortie », passer par référence vers non-`const`](006-functions.md006-functions.md#rf-inout)
* [F.18 : Pour les paramètres « dont on va transférer la propriété », passer par `X&&` et `std::move` le paramètre](006-functions.md#rf-consume)
* [F.19 : Pour les paramètres « de transit », passer par `TP&&` et uniquement `std::forward` le paramètre](006-functions.md#rf-forward)
* [F.20 : Pour les valeurs de sortie « out », privilégier les valeurs de retour aux paramètres de sortie](006-functions.md#rf-out)
* [F.21 : Pour retourner plusieurs valeurs de sortie, privilégier le retour d'un struct](006-functions.md006-functions.md#rf-out-multi)
* [F.60 : Privilégier `T*` à `T&` lorsque « aucun argument » est une option valide](006-functions.md006-functions.md#rf-ptr-ref)

Règles sémantiques de passage de paramètres :

* [F.22 : Utiliser `T*` ou `owner<T*>` pour désigner un seul objet](006-functions.md#rf-ptr)
* [F.23 : Utiliser un `not_null<T>` pour indiquer que « null » n'est pas une valeur valide](006-functions.md#rf-nullptr)
* [F.24 : Utiliser un `span<T>` ou un `span_p<T>` pour désigner une séquence à bornes semi-ouvertes](006-functions.md#rf-range)
* [F.25 : Utiliser un `zstring` ou un `not_null<zstring>` pour désigner une chaîne de style C](006-functions.md#rf-zstring)
* [F.26 : Utiliser un `unique_ptr<T>` pour transférer la propriété lorsqu'un pointeur est nécessaire](006-functions.md#rf-unique_ptr)
* [F.27 : Utiliser un `shared_ptr<T>` pour partager la propriété](006-functions.md#rf-shared_ptr)

<a name="rf-value-return"></a>Règles sémantiques de valeur de retour :

* [F.42 : Retourner un `T*` pour indiquer une position (uniquement)](006-functions.md#rf-return-ptr)
* [F.43 : Ne jamais (directement ou indirectement) retourner un pointeur ou une référence vers un objet local](006-functions.md#rf-dangle)
* [F.44 : Retourner un `T&` lorsque la copie est indésirable et que « ne retourner aucun objet » n'est pas nécessaire](006-functions.md#rf-return-ref)
* [F.45 : Ne pas retourner un `T&&`](006-functions.md006-functions.md#rf-return-ref-ref)
* [F.46 : `int` est le type de retour de `main()`](006-functions.md#rf-main)
* [F.47 : Retourner `T&` des opérateurs d'affectation](006-functions.md#rf-assignment-op)
* [F.48 : Ne pas retourner `std::move(local)`](006-functions.md#rf-return-move-local)
* [F.49 : Ne pas retourner `const T`](006-functions.md#rf-return-const)

Autres règles sur les fonctions :

* [F.50 : Utiliser une lambda lorsqu'une fonction ne suffit pas (pour capturer des variables locales, ou pour écrire une fonction locale)](006-functions.md#rf-capture-vs-overload)
* [F.51 : Lorsqu'il y a un choix, privilégier les arguments par défaut à la surcharge](006-functions.md#rf-default-args)
* [F.52 : Privilégier la capture par référence dans les lambdas utilisées localement, y compris lorsqu'elles sont passées à des algorithmes](006-functions.md#rf-reference-capture)
* [F.53 : Éviter la capture par référence dans les lambdas utilisées non-localement, y compris lorsqu'elles sont retournées, stockées sur le tas, ou passées à un autre thread](006-functions.md#rf-value-capture)
* [F.54 : Lorsque vous écrivez une lambda qui capture `this` ou un membre de données de classe, n'utiliser pas la capture par défaut `[=]`](006-functions.md#rf-this-capture)
* [F.55 : Ne pas utiliser les arguments `va_arg`](006-functions.md#f-varargs)
* [F.56 : Éviter l'imbrication inutile de conditions](006-functions.md#f-nesting)

Les fonctions ont de fortes similitudes avec les lambdas et les objets fonctionnels.

**Voir aussi** : [C.lambdas : Objets fonctionnels et lambdas](007-class.md#ss-lambdas) @TODO-LINK

## <a name="ss-fct-def"></a>F.def : Définitions de fonctions

Une définition de fonction est une déclaration de fonction qui spécifie également l'implémentation de la fonction, le corps de la fonction.

### <a name="rf-package"></a>F.1 : Encapsuler les opérations significatives dans des fonctions soigneusement nommées

##### Raison

Facturer du code commun rend le code plus lisible, plus susceptible d'être réutilisé, et limite les erreurs provenant de code complexe.
Si quelque chose est une action bien spécifiée, l'isoler de son code environnant et lui donner un nom.

##### Exemple, à éviter

    void read_and_print(istream& is)    // lire et afficher un int
    {
        int x;
        if (is >> x)
            cout << "l'entier est " << x << '\n';
        else
            cerr << "pas d'entier en entrée\n";
    }

Presque tout est faux avec `read_and_print`.
Il lit, il écrit (vers un `ostream` fixe), il écrit des messages d'erreur (vers un `ostream` fixe), il ne gère que des `int`.
Il n'y a rien à réutiliser, les opérations logiquement séparées sont mêlées et les variables locales restent en portée après la fin de leur usage logique.
Pour un minuscule exemple, ça paraît acceptable, mais si l'opération d'entrée, l'opération de sortie, et la gestion des erreurs avaient été plus complexes, la
tâche inextricable aurait pu devenir difficile à comprendre.

##### Note

Si vous écrivez une lambda non triviale qui pourrait potentiellement être utilisée à plus d'un endroit, donnez-lui un nom en l'assignant à une variable (généralement non locale).

##### Exemple

    sort(a, b, [](T x, T y) { return x.rank() < y.rank() && x.value() < y.value(); });

Donner un nom à cette lambda décompose l'expression en ses parties logiques et fournit un indice fort sur le sens de la lambda.

    auto lessT = [](T x, T y) { return x.rank() < y.rank() && x.value() < y.value(); };

    sort(a, b, lessT);

Le code le plus court n'est pas toujours le meilleur pour les performances ou la maintainabilité.

##### Exception

Les corps de boucles, y compris les lambdas utilisées comme corps de boucle, ont rarement besoin d'un nom.
Cependant, les grands corps de boucle (par exemple, des dizaines de lignes ou des dizaines de pages) peuvent poser problème.
La règle [Garder les fonctions courtes et simples](006-functions.md#rf-single) implique « Garder les corps de boucles courts. »
De même, les lambdas utilisées comme arguments de callback sont parfois non triviales, mais peu susceptibles d'être réutilisables.

##### Vérification

* Voir [Garder les fonctions courtes et simples](006-functions.md#rf-single)
* Signaler les lambdas identiques et très similaires utilisées dans des endroits différents.

### <a name="rf-logical"></a>F.2 : Une fonction doit effectuer une seule opération logique

##### Raison

Une fonction qui effectue une seule opération est plus simple à comprendre, à tester et à réutiliser.

##### Exemple

Considérons :

    void read_and_print()    // mauvais
    {
        int x;
        cin >> x;
        // vérifier les erreurs
        cout << x << "\n";
    }

C'est un monolithe lié à une entrée spécifique et qui ne trouvera jamais un autre (différent) usage. Au lieu de cela, décomposer les fonctions en parties logiques appropriées et paramétrer :

    int read(istream& is)    // meilleur
    {
        int x;
        is >> x;
        // vérifier les erreurs
        return x;
    }

    void print(ostream& os, int x)
    {
        os << x << "\n";
    }

Celles-ci peuvent maintenant être combinées là où c'est nécessaire :

    void read_and_print()
    {
        auto x = read(cin);
        print(cout, x);
    }

Si le besoin s'en faisait sentir, nous pourrions encore plus modéliser `read()` et `print()` sur le type de données, le mécanisme d'E/S, la réponse aux erreurs, etc. Exemple :

    auto read = [](auto& input, auto& value)    // meilleur
    {
        input >> value;
        // vérifier les erreurs
    };

    void print(auto& output, const auto& value)
    {
        output << value << "\n";
    }

##### Vérification

* Considérer avec suspicion les fonctions ayant plus d'un paramètre « en sortie ». Utiliser des valeurs de retour à la place, y compris `tuple` pour plusieurs valeurs de retour.
* Considérer avec suspicion les fonctions « grandes » qui ne tiennent pas sur un écran d'éditeur. Considérer la factorisation d'une telle fonction en sous-opérations plus petites et bien nommées.
* Considérer avec suspicion les fonctions avec 7 paramètres ou plus.

### <a name="rf-single"></a>F.3 : Garder les fonctions courtes et simples

##### Raison

Les grandes fonctions sont difficiles à lire, plus susceptibles de contenir du code complexe, et plus susceptibles d'avoir des variables dans des portées supérieures au minimum.
Les fonctions avec des structures de contrôle complexes sont plus susceptibles d'être longues et plus susceptibles de masquer des erreurs logiques.

##### Exemple

Considérons :

    double simple_func(double val, int flag1, int flag2)
        // simple_func : prend une valeur et calcule la sortie ASIC attendue,
        // vu les deux drapeaux de mode.
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
Comment sauriez-vous que toutes les alternatives possibles ont été correctement traitées ?
Oui, il enfreint aussi d'autres règles.

Nous pouvons refactoriser :

    double func1_muon(double val, int flag)
    {
        // ???
    }

    double func1_tau(double val, int flag1, int flag2)
    {
        // ???
    }

    double simple_func(double val, int flag1, int flag2)
        // simple_func : prend une valeur et calcule la sortie ASIC attendue,
        // vu les deux drapeaux de mode.
    {
        if (flag1 > 0)
            return func1_muon(val, flag2);
        if (flag1 == -1)
            // géré par func1_tau : flag1 = -flag1 ;
            return func1_tau(-val, flag1, flag2);
        return 0.;
    }

##### Note

« Ça ne tient pas sur un écran » est souvent une bonne définition pratique de « beaucoup trop grand. »
Les fonctions d'une à cinq lignes doivent être considérées comme normales.

##### Note

Décomposer les grandes fonctions en plus petites fonctions cohésives et nommées.
Les petites fonctions simples sont facilement inlinées là où le coût d'un appel de fonction est significatif.

##### Vérification

* Signaler les fonctions qui ne « tiennent pas sur un écran. »
  Quelle est la taille d'un écran ? Essayez 60 lignes par 140 caractères ; c'est approximativement le maximum confortable pour une page de livre.
* Signaler les fonctions trop complexes. Quelle est la complexité « trop complexe » ?
  Vous pourriez utiliser la complexité cyclomatique. Essayez « plus de 10 chemins logiques ». Comptez un switch simple comme un chemin.

### <a name="rf-constexpr"></a>F.4 : Si une fonction peut devoir être évaluée au moment de la compilation, la déclarer `constexpr`

##### Raison

`constexpr` est nécessaire pour indiquer au compilateur d'autoriser l'évaluation au moment de la compilation.

##### Exemple

La (célèbre/in)célèbre factorielle :

    constexpr int fac(int n)
    {
        constexpr int max_exp = 17;      // constexpr permet à max_exp d'être utilisé dans Expects
        Expects(0 <= n && n < max_exp);  // empêcher les bêtises et les dépassements
        int x = 1;
        for (int i = 2; i <= n; ++i) x *= i;
        return x;
    }

C'est du C++14.
Pour C++11, utiliser une formulation récursive de `fac()`.

##### Note

`constexpr` ne garantit pas l'évaluation au moment de la compilation ;
il garantit simplement que la fonction peut être évaluée au moment de la compilation pour des arguments d'expression constante si le programmeur l'exige ou si le compilateur décide de le faire pour optimiser.

    constexpr int min(int x, int y) { return x < y ? x : y; }

    void test(int v)
    {
        int m1 = min(-1, 2);            // probablement une évaluation au moment de la compilation
        constexpr int m2 = min(-1, 2);  // évaluation au moment de la compilation
        int m3 = min(-1, v);            // évaluation au moment de l'exécution
        constexpr int m4 = min(-1, v);  // erreur : ne peut pas être évaluée au moment de la compilation
    }

##### Note

N'essayez pas de rendre toutes les fonctions `constexpr`.
La plupart des calculs sont mieux faits au moment de l'exécution.

##### Note

Toute API qui pourrait éventuellement dépendre d'une configuration d'exécution de haut niveau ou
de logique métier ne devrait pas être rendue `constexpr`. Telle personnalisation ne peut pas être
évaluée par le compilateur, et toute fonction `constexpr` qui en dépendrait devrait être refactorisée ou abandonner `constexpr`.

##### Vérification

Impossible et inutile.
Le compilateur donne une erreur si une fonction non-`constexpr` est appelée là où une constante est requise.

### <a name="rf-inline"></a>F.5 : Si une fonction est très petite et critique en temps, la déclarer `inline`

##### Raison

Certains optimiseurs sont bons à l'inlinage sans indications du programmeur, mais n'y comptez pas.
Mesurez ! Au cours des 40 dernières années environ, on nous a promis des compilateurs capables d'inliner mieux que des humains sans indications humaines.
Nous attendons toujours.
Spécifier inline (explicitement, ou implicitement en écrivant des fonctions membres dans la définition d'une classe) encourage le compilateur à faire un meilleur travail.

##### Exemple

    inline string cat(const string& s, const string& s2) { return s + s2; }

##### Exception

Ne mettez pas une fonction `inline` dans ce qui est censé être une interface stable à moins d'être certain qu'elle ne changera pas.
Une fonction inline fait partie de l'ABI.

##### Note

`constexpr` implique `inline`.

##### Note

Les fonctions membres définies dans la classe sont `inline` par défaut.

##### Exception

Les modèles de fonction (y compris les fonctions membres de modèles de classe `A<T>::function()` et les modèles de fonctions membres `A::function<T>()`) sont normalement définis dans les en-têtes et sont donc inline.

##### Note

Considérez rendre les fonctions hors ligne si elles ont plus de trois déclarations et peuvent être déclarées hors ligne (telles que les fonctions membres de classe).

### <a name="rf-noexcept"></a>F.6 : Si votre fonction ne doit pas lancer d'exception, la déclarer `noexcept`

##### Raison

Si une exception n'est pas censée être lancée, le programme ne peut pas être supposé gérer l'erreur et devrait être terminé le plus tôt possible. Déclarer une fonction `noexcept` aide les optimiseurs en réduisant le nombre de chemins d'exécution alternatifs. Cela accélère aussi la sortie après une défaillance.

##### Exemple

Mettre `noexcept` sur chaque fonction écrite entièrement en C ou dans tout autre langage sans exceptions.
La bibliothèque standard C++ le fait implicitement pour toutes les fonctions de la bibliothèque standard C.

##### Note

Les fonctions `constexpr` peuvent lancer des exceptions lorsqu'elles sont évaluées au moment de l'exécution, donc vous pourriez avoir besoin de `noexcept` conditionnel pour certaines d'entre elles.

##### Exemple

Vous pouvez utiliser `noexcept` même sur des fonctions qui peuvent lancer des exceptions :

    vector<string> collect(istream& is) noexcept
    {
        vector<string> res;
        for (string s; is >> s;)
            res.push_back(s);
        return res;
    }

Si `collect()` épuise la mémoire, le programme plante.
À moins que le programme ne soit conçu pour survivre à l'épuisement de la mémoire, cela pourrait être juste la bonne chose à faire ;
`terminate()` pourrait générer des informations de journal d'erreur appropriées (mais après épuisement de la mémoire, c'est difficile de faire quoi que ce soit d'astucieux).

##### Note

Vous devez être conscient de l'environnement d'exécution dans lequel votre code s'exécute lors
de la décision d'étiqueter une fonction `noexcept`, en raison notamment du problème
des exceptions et de l'allocation. Le code destiné à être parfaitement général (comme
la bibliothèque standard et autres codes utilitaires de ce type) doit supporter
des environnements où une exception `bad_alloc` pourrait être traitée de manière significative.
Cependant, la plupart des programmes et environnements d'exécution ne peuvent pas traiter de
manière significative un échec d'allocation, et l'abandon du programme est la réponse
la plus propre et la plus simple à un échec d'allocation dans ces cas. Si vous savez que
votre code d'application ne peut pas répondre à un échec d'allocation, il peut être
approprié d'ajouter `noexcept` même sur des fonctions qui allouent.

Autrement dit : dans la plupart des programmes, la plupart des fonctions peuvent lancer des exceptions (par exemple parce qu'elles
utilisent `new`, appellent des fonctions qui le font, ou utilisent des fonctions de bibliothèque qui signalent l'échec
en lançant des exceptions), donc ne saupoudrez pas `noexcept` partout sans
considérer si les exceptions possibles peuvent être gérées.

`noexcept` est le plus utile (et le plus clairement correct) pour les fonctions de bas niveau, fréquemment utilisées.

##### Note

Les destructeurs, les fonctions `swap`, les opérations de déplacement et les constructeurs par défaut ne doivent jamais lancer d'exception.
Voir aussi [C.44](007-class.md007-class.md007-class.md#rc-default00). @TODO-LINK

##### Note

Il faut prendre garde aux fonctions virtuelles de base et aux fonctions faisant partie d'une interface publique car déclarer une fonction `noexcept` établit une garantie que toutes les implémentations actuelles et futures doivent respecter. Pour les fonctions virtuelles, tous les surchargeurs doivent aussi être `noexcept` et supprimer `noexcept` d'une fonction pourrait casser les fonctions appelantes.

##### Vérification

* (dur) Signaler les fonctions de bas niveau qui ne sont pas `noexcept`, mais ne peuvent pas lancer d'exception.
* Signaler les `swap`, `move`, destructeurs et constructeurs par défaut qui lancent des exceptions.

### <a name="rf-smart"></a>F.7 : Pour un usage général, prendre des arguments `T*` ou `T&` plutôt que des pointeurs intelligents

##### Raison

Passer un pointeur intelligent transfère ou partage la propriété et ne devrait être utilisé que lorsque des sémantiques de propriété sont intended.
Une fonction qui ne manipule pas la durée de vie devrait prendre des pointeurs bruts ou des références à la place.

Passer par pointeur intelligent restreint l'utilisation d'une fonction aux appelants qui utilisent des pointeurs intelligents.
Une fonction qui a besoin d'un `widget` devrait pouvoir accepter n'importe quel objet `widget`, pas seulement ceux dont la durée de vie est gérée par un type particulier de pointeur intelligent.

Passer un pointeur intelligent partagé (par exemple, `std::shared_ptr`) implique un coût au moment de l'exécution.

##### Exemple

    // accepte n'importe quel int*
    void f(int*);

    // ne peut accepter que des ints pour lesquels on veut transférer la propriété
    void g(unique_ptr<int>);

    // ne peut accepter que des ints pour lesquels on est prêt à partager la propriété
    void g(shared_ptr<int>);

    // ne change pas la propriété, mais requiert une propriété particulière de l'appelant
    void h(const unique_ptr<int>&);

    // accepte n'importe quel int
    void h(int&);

##### Exemple, mauvais

    // appelé
    void f(shared_ptr<widget>& w)
    {
        // ...
        use(*w); // seul usage de w — la durée de vie n'est pas utilisée du tout
        // ...
    };

    // appelant
    shared_ptr<widget> my_widget = /* ... */;
    f(my_widget);

    widget stack_widget;
    f(stack_widget); // erreur

##### Exemple, bon

    // appelé
    void f(widget& w)
    {
        // ...
        use(w);
        // ...
    };

    // appelant
    shared_ptr<widget> my_widget = /* ... */;
    f(*my_widget);

    widget stack_widget;
    f(stack_widget); // ok — maintenant ça marche

##### Note

Nous pouvons détecter statiquement beaucoup de cas courants de pointeurs pendants (voir [profil de sécurité de durée de vie](022-profile.md#ss-lifetime)). @TODO-LINK Les arguments de fonction vivent naturellement pour la durée de l'appel de fonction, et ont donc moins de problèmes de durée de vie.

##### Vérification

* (Simple) Avertir si une fonction prend un paramètre de type pointeur intelligent (qui surcharge `operator->` ou `operator*`) qui est copiable mais que la fonction n'utilise que l'un de : `operator*`, `operator->` ou `get()`.
  Suggérer d'utiliser un `T*` ou un `T&` à la place.
* Signaler un paramètre de type pointeur intelligent (un type qui surcharge `operator->` ou `operator*`) qui est copiable/déplaçable mais n'est jamais copié/déplacé dans le corps de la fonction, et qui n'est jamais modifié, et qui n'est pas transmis à une autre fonction qui pourrait le faire. Cela signifie que les sémantiques de propriété ne sont pas utilisées.
  Suggérer d'utiliser un `T*` ou un `T&` à la place.

**Voir aussi** :

* [Privilégier `T*` à `T&` lorsque « aucun argument » est une option valide](006-functions.md006-functions.md#rf-ptr-ref)
* [Résumé des règles des pointeurs intelligents](009-resource.md#rr-summary-smartptrs) @TODO-LINK

### <a name="rf-pure"></a>F.8 : Privilégier les fonctions pures

##### Raison

Les fonctions pures sont plus faciles à raisonner, parfois plus faciles à optimiser (et même à paralléliser), et parfois peuvent être mémoïsées.

##### Exemple

    template<class T>
    auto square(T t) { return t * t; }

##### Vérification

Non possible.

### <a name="rf-unused"></a>F.9 : Les paramètres non utilisés doivent être sans nom

##### Raison

Lisibilité.
Suppression des avertissements de paramètres non utilisés.

##### Exemple

    widget* find(const set<widget>& s, const widget& w, Hint);   // il fut un temps où un indice était utilisé

##### Note

Autoriser les paramètres sans nom a été introduit dans les années 1980 pour adresser ce problème.

Si les paramètres sont conditionnellement non utilisés, les déclarer avec l'attribut `[[maybe_unused]]`.
Par exemple :

    template <typename Value>
    Value* find(const set<Value>& s, const Value& v, [[maybe_unused]] Hint h)
    {
        if constexpr (sizeof(Value) > CacheSize)
        {
            // un indice est utilisé seulement si Value est d'une certaine taille
        }
    }

##### Vérification

Signaler les paramètres nommés non utilisés.

### <a name="rf-name"></a>F.10 : Si une opération peut être réutilisée, lui donner un nom

##### Raison

Documentation, lisibilité, opportunité de réutilisation.

##### Exemple

    struct Rec {
        string name;
        string addr;
        int id;         // identifiant unique
    };

    bool same(const Rec& a, const Rec& b)
    {
        return a.id == b.id;
    }

    vector<Rec*> find_id(const string& name);    // trouver tous les enregistrements pour « name »

    auto x = find_if(vr.begin(), vr.end(),
        [&](Rec& r) {
            if (r.name.size() != n.size()) return false; // le nom à comparer est dans n
            for (int i = 0; i < r.name.size(); ++i)
                if (tolower(r.name[i]) != tolower(n[i])) return false;
            return true;
        }
    );

Il y a une fonction utile qui se cache ici (comparaison de chaînes insensible à la casse), comme c'est souvent le cas lorsque les arguments de lambda deviennent grands.

    bool compare_insensitive(const string& a, const string& b)
    {
        if (a.size() != b.size()) return false;
        for (int i = 0; i < a.size(); ++i) if (tolower(a[i]) != tolower(b[i])) return false;
        return true;
    }

    auto x = find_if(vr.begin(), vr.end(),
        [&](Rec& r) { return compare_insensitive(r.name, n); }
    );

Ou peut-être (si vous préférez éviter le liage implicite du nom à n) :

    auto cmp_to_n = [&n](const string& a) { return compare_insensitive(a, n); };

    auto x = find_if(vr.begin(), vr.end(),
        [](const Rec& r) { return cmp_to_n(r.name); }
    );

##### Note

que ce soient des fonctions, des lambdas ou des opérateurs.

##### Exception

* Lambdas logiquement utilisées uniquement localement, telles qu'un argument à `for_each` et algorithmes de flux de contrôle similaires.
* Lambdas comme [initialisateurs](#???) @TODO-LINK

##### Vérification

* (dur) signaler les lambdas similaires
* ???

### <a name="rf-lambda"></a>F.11 : Utiliser une lambda anonyme si vous avez besoin d'un simple objet fonctionnel à un seul endroit

##### Raison

Cela rend le code concis et offre une meilleure localité que les alternatives.

##### Exemple

    auto earlyUsersEnd = std::remove_if(users.begin(), users.end(),
                                        [](const User &a) { return a.id > 100; });


##### Exception

Donner un nom à une lambda peut être utile pour la clarté même si elle n'est utilisée qu'une fois.

##### Vérification

* Chercher les lambdas identiques et quasi identiques (à remplacer par des fonctions nommées ou des lambdas nommées).

## <a name="ss-call"></a>F.call : Passage de paramètres

Il existe diverses façons de passer des paramètres à une fonction et de retourner des valeurs.

### <a name="rf-conventional"></a>F.15 : Privilégier les moyens simples et conventionnels de transmettre l'information

##### Raison

L'utilisation de techniques « inhabituelles et astucieuses » cause des surprises, ralentit la compréhension par d'autres programmeurs, et encourage les bugs.
Si vous ressentez vraiment le besoin d'une optimisation au-delà des techniques courantes, mesurez pour vous assurer que c'est réellement une amélioration, et documentez/commentez car l'amélioration pourrait ne pas être portable.

Les tableaux suivants résument les conseils dans les Directives suivantes, F.16-21.

Passage de paramètres normal :

![Tableau de passage de paramètres normal](./param-passing-normal.png "Passage de paramètres normal")

Passage de paramètres avancé :

![Tableau de passage de paramètres avancé](./param-passing-advanced.png "Passage de paramètres avancé")

Utiliser les techniques avancées seulement après avoir démontré le besoin, et documenter ce besoin dans un commentaire.

Pour le passage de séquences de caractères, voir [Chaînes](018-stdlib.md#ss-string). @TODO-LINK

##### Exception

Pour exprimer une propriété partagée en utilisant des types `shared_ptr`, plutôt que de suivre les directives F.16-21,
suivre [R.34](009-resource.md009-resource.md#rr-sharedptrparam-owner), [R.35](009-resource.md#rr-sharedptrparam), et [R.36](009-resource.md009-resource.md#rr-sharedptrparam-const). @TODO-LINK

### <a name="rf-in"></a>F.16 : Pour les paramètres « en entrée », passer les types à copie économique par valeur et les autres par référence vers `const`

##### Raison

Les deux permettent à l'appelant de savoir qu'une fonction ne modifiera pas l'argument, et les deux autorisent l'initialisation par des valeurs de droite.

Ce qui est « économique à copier » dépend de l'architecture de la machine, mais deux ou trois mots (doubles, pointeurs, références) sont généralement meilleurs passés par valeur.
Lorsque la copie est économique, rien ne surpasse la simplicité et la sécurité de la copie, et pour les petits objets (jusqu'à deux ou trois mots) c'est aussi plus rapide que le passage par référence car cela ne requiert pas d'indirection supplémentaire pour y accéder depuis la fonction.

##### Exemple

    void f1(const string& s);  // OK : passer par référence vers const ; toujours économique

    void f2(string s);         // mauvais : potentiellement coûteux

    void f3(int x);            // OK : imbattable

    void f4(const int& x);     // mauvais : surcoût d'accès dans f4()

Pour les usages avancés (uniquement), où vous avez vraiment besoin d'optimiser pour les valeurs de droite passées à des paramètres « en entrée uniquement » :

* Si la fonction va inconditionnellement déplacer depuis l'argument, le prendre par `&&`. Voir [F.18](006-functions.md#rf-consume).
* Si la fonction va garder une copie modifiable localement de l'argument uniquement pour son usage local, le prendre par valeur est suffisant.
* Si la fonction va garder une copie de l'argument pour la passer à une autre destination (à une autre fonction, ou stocker dans un emplacement non local), en plus de passer par `const&` (pour les valeurs de gauche),
  ajouter une surcharge qui passe le paramètre par `&&` (pour les valeurs de droite) et dans le corps `std::move` vers sa destination. Essentiellement, cela surcharge un « dont on va transférer la propriété » ; voir [F.18](006-functions.md#rf-consume).
* Dans des cas spéciaux, tels que plusieurs paramètres « entrée + copie », considérer l'utilisation du transfert parfait. Voir [F.19](006-functions.md#rf-forward).

##### Exemple

    int multiply(int, int); // juste des ints en entrée, passer par valeur

    // suffix est en entrée uniquement mais pas aussi économique qu'un int, passer par const&
    string& concatenate(string&, const string& suffix);

    void sink(unique_ptr<widget>);  // entrée uniquement, et transfère la propriété du widget

Éviter les « techniques ésotériques » telles que passer des arguments en tant que `T&&` « pour l'efficacité ».
La plupart des rumeurs sur les avantages de performance du passage par `&&` sont fausses ou fragiles (mais voir [F.18](006-functions.md#rf-consume) et [F.19](006-functions.md#rf-forward)).

##### Notes

Une référence peut être supposée référencer un objet valide (règle du langage).
Il n'y a pas (de légitime) « référence nulle. »
Si vous avez besoin de la notion de valeur optionnelle, utilisez un pointeur, `std::optional`, ou une valeur spéciale utilisée pour désigner « aucune valeur. »

##### Vérification

* (Simple) ((Fondation)) Avertir lorsqu'un paramètre passé par valeur a une taille supérieure à `4 * sizeof(void*)`.
  Suggérer d'utiliser une référence vers `const` à la place.
* (Simple) ((Fondation)) Avertir lorsqu'un paramètre passé par référence vers `const` a une taille inférieure ou égale à `2 * sizeof(void*)`. Suggérer de passer par valeur à la place.
* (Simple) ((Fondation)) Avertir lorsqu'un paramètre passé par référence vers `const` est `move`'é.
* (Non simple) Note : une vérification plus stricte dépendrait des caractéristiques de performance de l'architecture cible.

##### Exception

Pour exprimer une propriété partagée en utilisant des types `shared_ptr`, suivre [R.34](009-resource.md009-resource.md#rr-sharedptrparam-owner) ou [R.36](009-resource.md009-resource.md#rr-sharedptrparam-const), @TODO-LINK
selon que la fonction prend ou non inconditionnellement une référence à l'argument.

### <a name="rf-inout"></a>F.17 : Pour les paramètres « en entrée/sortie », passer par référence vers non-`const`

##### Raison

Cela rend clair pour les appelants que l'objet est supposé être modifié.

##### Exemple

    void update(Record& r);  // supposer que update écrit dans r

##### Note

Certains types définis par l'utilisateur et de la bibliothèque standard, tels que `span<T>` ou les itérateurs,
sont [économiques à copier](006-functions.md#rf-in) et peuvent être passés par valeur, tout en ayant des
sémantiques de référence modifiables (entrée/sortie) :

    void increment_all(span<int> a)
    {
      for (auto&& e : a)
        ++e;
    }

##### Note

Un argument `T&` peut transmettre de l'information vers une fonction ainsi que depuis elle.
Ainsi `T&` pourrait être un paramètre en entrée/sortie. Cela peut en soi être un problème et une source d'erreurs :

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

Ici, l'auteur de `g()` fournit un tampon pour que `f()` le remplisse, mais `f()` le remplace simplement (à un coût légèrement supérieur à une simple copie des caractères).
Une mauvaise erreur logique peut survenir si l'auteur de `g()` suppose incorrectement la taille du `buffer`.

##### Vérification

* (Modéré) ((Fondation)) Avertir les fonctions concernant des paramètres par référence vers non-`const` qui ne *les* écri *vent* pas.
* (Simple) ((Fondation)) Avertir lorsqu'un paramètre non-`const` passé par référence est `move`'é.

### <a name="rf-consume"></a>F.18 : Pour les paramètres « dont on va transférer la propriété », passer par `X&&` et `std::move` le paramètre

##### Raison

C'est efficace et élimine les bugs au site d'appel : `X&&` se lie aux valeurs de droite, ce qui nécessite un `std::move` explicite au site d'appel si l'on passe une valeur de gauche.

##### Exemple

    void sink(vector<int>&& v)  // sink prend la propriété de tout ce que l'argument possédait
    {
        // il y a généralement des accès en const à v ici
        store_somewhere(std::move(v));
        // généralement plus d'usage de v ici ; il a été déplacé
    }

Notez que le `std::move(v)` permet à `store_somewhere()` de laisser `v` dans un état post-déplacement.
[Cela pourrait être dangereux](007-class.md#rc-move-semantic). @TODO-LINK


##### Exception

Les types propriétaires exclusifs qui sont uniquement déplacables et économiques à déplacer, tels que `unique_ptr`, peuvent aussi être passés par valeur ce qui est plus simple à écrire et atteint le même effet. Le passage par valeur génère une opération de déplacement supplémentaire (économique), mais préférez la simplicité et la clarté d'abord.

Par exemple :

    template<class T>
    void sink(std::unique_ptr<T> p)
    {
        // utiliser p ... possiblement std::move(p) ailleurs
    }   // p est détruit

##### Exception

Si le paramètre « dont on va transférer la propriété » est un `shared_ptr`, suivre [R.34](009-resource.md009-resource.md#rr-sharedptrparam-owner) et passer le `shared_ptr` par valeur. @TODO-LINK

##### Vérification

* Signaler tous les paramètres `X&&` (où `X` n'est pas un nom de paramètre de type de modèle) où le corps de la fonction les utilise sans `std::move`.
* Signaler l'accès à des objets post-déplacement.
* Ne pas conditionnellement déplacer des objets.

### <a name="rf-forward"></a>F.19 : Pour les paramètres « de transit », passer par `TP&&` et uniquement `std::forward` le paramètre

##### Raison

Si l'objet doit être transmis à d'autres codes et n'est pas utilisé directement par cette fonction, nous voulons rendre cette fonction agnostique vis-à-vis de la constance et de la nature valeur-de-droite de l'argument.

Dans ce cas, et uniquement dans ce cas, faire du paramètre `TP&&` où `TP` est un paramètre de type de modèle — cela à la fois *ignore* et *préserve* la constance et la nature valeur-de-droite. Par conséquent, tout code qui utilise un `TP&&` déclare implicitement qu'il ne se soucie pas de la constance et de la nature valeur-de-droite de la variable (parce que c'est ignoré), mais qu'il a l'intention de transmettre la valeur à d'autres codes qui se soucient de la constance et de la nature valeur-de-droite (parce que c'est préservé). Lorsqu'il est utilisé comme paramètre, `TP&&` est sûr car tous les objets temporaires passés par l'appelant vivront pour la durée de l'appel de fonction. Un paramètre de type `TP&&` devrait essentiellement toujours être transmis via `std::forward` dans le corps de la fonction.

##### Exemple

Généralement on transmet le paramètre entier (ou le paquet de paramètres, en utilisant `...`) exactement une fois sur chaque chemin de flux de contrôle statique :

    template<class F, class... Args>
    inline decltype(auto) invoke(F&& f, Args&&... args)
    {
        return forward<F>(f)(forward<Args>(args)...);
    }

##### Exemple

Parfois on peut transmettre un paramètre composite par morceaux, chaque sous-objet une fois sur chaque chemin de flux de contrôle statique :

    template<class PairLike>
    inline auto test(PairLike&& pairlike)
    {
        // ...
        f1(some, args, and, forward<PairLike>(pairlike).first);           // transmet .first
        f2(and, forward<PairLike>(pairlike).second, in, another, call);   // transmet .second
    }

##### Vérification

* Signaler une fonction qui prend un paramètre `TP&&` (où `TP` est un nom de paramètre de type de modèle) et fait autre chose avec elle que `std::forward` exactement une fois sur chaque chemin statique, ou `std::forward` plus d'une fois mais qualifié d'un membre de données différent exactement une fois sur chaque chemin statique.

### <a name="rf-out"></a>F.20 : Pour les valeurs de sortie « out », privilégier les valeurs de retour aux paramètres de sortie

##### Raison

Une valeur de retour est auto-documentante, tandis qu'un `&` pourrait être en entrée/sortie ou en sortie uniquement et est susceptible d'être mal utilisé.

Cela inclut les grands objets comme les conteneurs standard qui utilisent des opérations de déplacement implicites pour les performances et pour éviter la gestion mémoire explicite.

Si vous avez plusieurs valeurs à retourner, [utilisez un tuple](006-functions.md006-functions.md#rf-out-multi) ou un type multi-membres similaire.

##### Exemple

    // OK : retourner des pointeurs vers les éléments avec la valeur x
    vector<const int*> find_all(const vector<int>&, int x);

    // Mauvais : placer les pointeurs vers les éléments avec la valeur x en entrée/sortie
    void find_all(const vector<int>&, vector<const int*>& out, int x);

##### Note

Un `struct` de nombreux éléments (individuellement économiques à déplacer) pourrait être globalement coûteux à déplacer.

##### Exceptions

* Pour les types non concrets, tels que des types dans une hiérarchie d'héritage, retourner l'objet par `unique_ptr` ou `shared_ptr`.
* Si un type est coûteux à déplacer (par exemple, `array<BigTrivial>`), considérer l'allouer sur le tas et retourner un gestionnaire (par exemple, `unique_ptr`), ou le passer dans une référence vers un objet cible non-`const` à remplir (à utiliser comme paramètre de sortie).
* Pour réutiliser un objet qui porte une capacité (par exemple, `std::string`, `std::vector`) sur plusieurs appels à la fonction dans une boucle interne : [le traiter comme un paramètre en entrée/sortie et le passer par référence](006-functions.md006-functions.md#rf-out-multi).

##### Exemple

En supposant que `Matrix` ait des opérations de déplacement (peut-être en gardant ses éléments dans un `std::vector`) :

    Matrix operator+(const Matrix& a, const Matrix& b)
    {
        Matrix res;
        // ... remplir res avec la somme ...
        return res;
    }

    Matrix x = m1 + m2;  // constructeur de déplacement

    y = m3 + m3;         // affectation par déplacement


##### Note

L'optimisation de la valeur de retour ne gère pas le cas d'affectation, mais l'affectation par déplacement le fait.

##### Exemple

    struct Package {      // cas exceptionnel : objet coûteux à déplacer
        char header[16];
        char load[2024 - 16];
    };

    Package fill();       // Mauvais : grande valeur de retour
    void fill(Package&);  // OK

    int val();            // OK
    void val(int&);       // Mauvais : est-ce que val lit son argument

##### Vérification

* Signaler les références vers des paramètres non-`const` qui ne sont pas lus avant d'être écrits et sont d'un type qui pourrait être retourné économiquement ; ils devraient être des valeurs de retour « out ».

### <a name="rf-out-multi"></a>F.21 : Pour retourner plusieurs valeurs de sortie, privilégier le retour d'un struct

##### Raison

Une valeur de retour est auto-documentante en tant que valeur « en sortie uniquement ».
Notez que C++ a bien des valeurs de retour multiples, par convention d'utilisation de types de type tuple (`struct`, `array`, `tuple`, etc.),
peut-être avec le confort supplémentaire des liaisons structurées (C++17) au site d'appel.
Privilégier l'utilisation d'un `struct` nommé si possible.
Sinon, un `tuple` est utile dans les modèles variadiques.

##### Exemple

    // MAUVAIS : paramètre en sortie uniquement documenté dans un commentaire
    int f(const string& input, /*sortie uniquement*/ string& output_data)
    {
        // ...
        output_data = something();
        return status;
    }

    // BON : auto-documentant
    struct f_result { int status; string data; };

    f_result f(const string& input)
    {
        // ...
        return {status, something()};
    }

La bibliothèque standard de C++98 utilisait ce style à certains endroits, en retournant des `pair` dans certaines fonctions.
Par exemple, étant donné un `set<string> my_set`, considérez :

    // C++98
    pair<set::iterator, bool> result = my_set.insert("Hello");
    if (result.second)
        do_something_with(result.first);    // travail around

Avec C++17, nous pouvons utiliser les « liaisons structurées » pour donner un nom à chaque membre :

    if (auto [ iter, success ] = my_set.insert("Hello"); success)
        do_something_with(iter);

Un `struct` avec des noms significatifs est plus courant en C++ moderne.
Voir par exemple `ranges::min_max_result`, `from_chars_result`, et autres.

##### Exception

Parfois, nous avons besoin de passer un objet à une fonction pour manipuler son état.
Dans de tels cas, passer l'objet par référence [`T&`](006-functions.md006-functions.md#rf-inout) est généralement la bonne technique.
Transmettre explicitement un paramètre en entrée/sortie en retour comme valeur de retour est souvent inutile.
Par exemple :

    istream& operator>>(istream& in, string& s);    // tout comme std::operator>>()

    for (string s; in >> s; ) {
        // faire quelque chose avec la ligne
    }

Ici, à la fois `s` et `in` sont utilisés comme paramètres en entrée/sortie.
Nous passons `in` par référence (non-`const`) pour pouvoir manipuler son état.
Nous passons `s` pour éviter les allocations répétées.
En réutilisant `s` (passé par référence), nous n'allouons de nouvelle mémoire que lorsque nous devons étendre la capacité de `s`.
Cette technique est parfois appelée le motif « sortie allouée par l'appelant » et est particulièrement utile pour les types,
tels que `string` et `vector`, qui doivent faire des allocations sur le tas.

Par comparaison, si nous passions toutes les valeurs en retour comme valeurs de retour, nous écririons quelque chose comme ceci :

    struct get_string_result { istream& in; string s; };

    get_string_result get_string(istream& in)  // non recommandé
    {
        string s;
        in >> s;
        return { in, move(s) };
    }

    for (auto [in, s] = get_string(cin); in; s = get_string(in).s) {
        // faire quelque chose avec la chaîne
    }

Nous considérons cela significativement moins élégant avec significativement moins de performance.

Pour une lecture strictement littérale de cette règle (F.21), l'exception n'est pas vraiment une exception car elle repose sur des paramètres en entrée/sortie,
plutôt que sur les simples paramètres en sortie mentionnés dans la règle.
Cependant, nous préférons être explicites, plutôt que subtils.

##### Note

Dans la plupart des cas, il est utile de retourner un type spécifique, défini par l'utilisateur.
Par exemple :

    struct Distance {
        int value;
        int unit = 1;   // 1 signifie mètres
    };

    Distance d1 = measure(obj1);        // accéder à d1.value et d1.unit
    auto d2 = measure(obj2);            // accéder à d2.value et d2.unit
    auto [value, unit] = measure(obj3); // accéder à value et unit ; un peu redondant
                                        // pour ceux qui connaissent measure()
    auto [x, y] = measure(obj4);        // ne pas le faire ; c'est susceptible de confondre

Le `pair` et le `tuple` trop génériques ne devraient être utilisés que lorsque la valeur retournée représente des entités indépendantes plutôt qu'une abstraction.

Une autre option est d'utiliser `optional<T>` ou `expected<T, error_code>`, plutôt que `pair` ou `tuple`.
Lorsqu'ils sont utilisés de manière appropriée, ces types transmettent plus d'information sur la signification des membres que `pair<T, bool>` ou `pair<T, error_code>`.

##### Note

Lorsque l'objet à retourner est initialisé à partir de variables locales coûteuses à copier,
un `move` explicite peut être utile pour éviter la copie :

    pair<LargeObject, LargeObject> f(const string& input)
    {
        LargeObject large1 = g(input);
        LargeObject large2 = h(input);
        // ...
        return { move(large1), move(large2) }; // pas de copies
    }

Alternative,

    pair<LargeObject, LargeObject> f(const string& input)
    {
        // ...
        return { g(input), h(input) }; // pas de copies, pas de déplacements
    }

Notez que c'est différent de l'anti-motif `return move(...)` de [ES.56](010-expr.md#res-move). @TODO-LINK

##### Vérification

* Les paramètres de sortie devraient être remplacés par des valeurs de retour.
  Un paramètre de sortie est celui vers lequel la fonction écrit, appelle une fonction membre non-`const`, ou le transmet en tant que non-`const`.
* Les types de retour `pair` ou `tuple` devraient être remplacés par `struct`, si possible.
  Dans les modèles variadiques, `tuple` est souvent inévitable.

### <a name="rf-ptr-ref"></a>F.60 : Privilégier `T*` à `T&` lorsque « aucun argument » est une option valide

##### Raison

Un pointeur (`T*`) peut être un `nullptr` et une référence (`T&`) ne le peut pas, il n'y a pas de « référence nulle » valide.
Parfois avoir `nullptr` comme alternative pour indiquer « aucun objet » est utile, mais si ce n'est pas le cas, une référence est notationnellement plus simple et pourrait générer un meilleur code.

##### Exemple

    string zstring_to_string(zstring p) // zstring est un char* ; c'est une chaîne de style C
    {
        if (!p) return string{};    // p pourrait être nullptr ; n'oubliez pas de vérifier
        return string{p};
    }

    void print(const vector<int>& r)
    {
        // r référence un vector<int> ; aucune vérification nécessaire
    }

##### Note

Il est possible, mais pas du C++ valide, de construire une référence qui est essentiellement un `nullptr` (par exemple, `T* p = nullptr; T& r = *p;`).
Cette erreur est très rare.

##### Note

Si vous préférez la notation pointeur (`->` et/ou `*` vs. `.`), `not_null<T*>` fournit la même garantie que `T&`.

##### Vérification

* Signaler ???

### <a name="rf-ptr"></a>F.22 : Utiliser `T*` ou `owner<T*>` pour désigner un seul objet

##### Raison

Lisibilité : cela rend le sens d'un pointeur brut clair.
Permet un support d'outils significatif.

##### Note

Dans le code C et C++ traditionnel, le `T*` brut est utilisé pour de nombreuses finalités faiblement liées, telles que :

* Identifier un (seul) objet (ne pas être supprimé par cette fonction)
* Pointer vers un objet alloué sur le tas (et le supprimer plus tard)
* Contenir le `nullptr`
* Identifier une chaîne de style C (tableau de caractères terminé par zéro)
* Identifier un tableau avec une longueur spécifiée séparément
* Identifier un emplacement dans un tableau

Cela rend difficile la compréhension de ce que le code fait et est censé faire.
Cela complique les vérifications et le support d'outils.

##### Exemple

    void use(int* p, int n, char* s, int* q)
    {
        p[n - 1] = 666; // Mauvais : nous ne savons pas si p pointe vers n éléments ;
                        // supposons que non ou utiliser span<int>
        cout << s;      // Mauvais : nous ne savons pas si s pointe vers un tableau de char terminé par zéro ;
                        // supposons que non ou utiliser zstring
        delete q;       // Mauvais : nous ne savons pas si *q est alloué sur le tas ;
                        // supposons que non ou utiliser owner
    }

meilleur

    void use2(span<int> p, zstring s, owner<int*> q)
    {
        p[p.size() - 1] = 666; // OK, une erreur de portée peut être détectée
        cout << s; // OK
        delete q;  // OK
    }

##### Note

`owner<T*>` représente la propriété, `zstring` représente une chaîne de style C.

**Aussi** : Supposer qu'un `T*` obtenu depuis un pointeur intelligent vers `T` (par exemple, `unique_ptr<T>`) pointe vers un seul élément.

**Voir aussi** : [Bibliothèque de support](#gsl-guidelines-support-library) @TODO-LINK

**Voir aussi** : [Ne pas passer un tableau en tant que pointeur unique](005-interfaces.md#ri-array) @TODO-LINK

##### Vérification

* (Simple) ((Bornes)) Avertir pour toute opération arithmétique sur une expression de type pointeur qui aboutit à une valeur de type pointeur.

### <a name="rf-nullptr"></a>F.23 : Utiliser un `not_null<T>` pour indiquer que « null » n'est pas une valeur valide

##### Raison

Clarté. Une fonction avec un paramètre `not_null<T>` rend clair que l'appelant de la fonction est responsable de toute vérification de `nullptr` qui pourrait être nécessaire.
De même, une fonction avec une valeur de retour `not_null<T>` rend clair que l'appelant de la fonction n'a pas besoin de vérifier le `nullptr`.

##### Exemple

`not_null<T*>` rend évident pour un lecteur (humain ou machine) qu'un test pour `nullptr` n'est pas nécessaire avant la déréférenciation.
De plus, lors du débogage, `owner<T*>` et `not_null<T>` peuvent être instrumentés pour vérifier la justesse.

Considérons :

    int length(Record* p);

Lorsque j'appelle `length(p)`, devrais-je vérifier si `p` est `nullptr` d'abord ? L'implémentation de `length()` doit-elle vérifier si `p` est `nullptr` ?

    // c'est le travail de l'appelant de s'assurer que p != nullptr
    int length(not_null<Record*> p);

    // l'implémenteur de length() doit supposer que p == nullptr est possible
    int length(Record* p);

##### Note

Un `not_null<T*>` est supposé ne pas être le `nullptr` ; un `T*` pourrait être le `nullptr` ; les deux peuvent être représentés en mémoire comme un `T*` (donc aucun surcoût au moment de l'exécution n'est impliqué).

##### Note

`not_null` n'est pas seulement pour les pointeurs intégrés. Il fonctionne pour `unique_ptr`, `shared_ptr`, et autres types de type pointeur.

##### Vérification

* (Simple) Avertir si un pointeur brut est déréférencé sans être testé contre `nullptr` (ou équivalent) dans une fonction, suggérer qu'il est déclaré `not_null` à la place.
* (Simple) Erreur si un pointeur brut est parfois déréférencé après avoir été testé contre `nullptr` (ou équivalent) dans la fonction et parfois ne l'est pas.
* (Simple) Avertir si un pointeur `not_null` est testé contre `nullptr` dans une fonction.

### <a name="rf-range"></a>F.24 : Utiliser un `span<T>` ou un `span_p<T>` pour désigner une séquence à bornes semi-ouvertes

##### Raison

Les plages informelles/non explicites sont une source d'erreurs.

##### Exemple

    X* find(span<X> r, const X& v);    // trouver v dans r

    vector<X> vec;
    // ...
    auto p = find({vec.begin(), vec.end()}, X{});  // trouver X{} dans vec

##### Note

Les plages sont extrêmement courantes dans le code C++. Typiquement, elles sont implicites et leur usage correct est très difficile à garantir.
En particulier, étant donné une paire d'arguments `(p, n)` désignant un tableau `[p:p+n)`,
il est généralement impossible de savoir s'il y a vraiment `n` éléments à accéder après `*p`.
`span<T>` et `span_p<T>` sont de simples classes auxiliaires désignant respectivement une plage `[p:q)` et une plage commençant par `p` et se terminant au premier élément pour lequel un prédicat est vrai.

##### Exemple

Un `span` représente une plage d'éléments, mais comment manipulons-nous les éléments de cette plage ?

    void f(span<int> s)
    {
        // parcours de plage (garanti correct)
        for (int x : s) cout << x << '\n';

        // parcours de style C (potentiellement vérifié)
        for (gsl::index i = 0; i < s.size(); ++i) cout << s[i] << '\n';

        // accès aléatoire (potentiellement vérifié)
        s[7] = 9;

        // extraction de pointeurs (potentiellement vérifiée)
        std::sort(&s[0], &s[s.size() / 2]);
    }

##### Note

Un objet `span<T>` ne possède pas ses éléments et est si petit qu'il peut être passé par valeur.

Passer un objet `span` en argument est aussi efficace que de passer une paire d'arguments pointeur ou de passer un pointeur et un compteur entier.

**Voir aussi** : [Bibliothèque de support](#gsl-guidelines-support-library) @TODO-LINK

##### Vérification

(Complexe) Avertir lorsque les accès aux paramètres pointeur sont bornés par d'autres paramètres de types entiers et suggérer qu'ils pourraient utiliser `span` à la place.

### <a name="rf-zstring"></a>F.25 : Utiliser un `zstring` ou un `not_null<zstring>` pour désigner une chaîne de style C

##### Raison

Les chaînes de style C sont omniprésentes. Elles sont définies par convention : tableaux de caractères terminés par zéro.
Nous devons distinguer les chaînes de style C d'un pointeur vers un seul caractère ou d'un ancien pointeur vers un tableau de caractères.

Si vous n'avez pas besoin de terminaison par zéro, utilisez `string_view`.

##### Exemple

Considérons :

    int length(const char* p);

Lorsque j'appelle `length(s)`, devrais-je vérifier si `s` est `nullptr` d'abord ? L'implémentation de `length()` doit-elle vérifier si `p` est `nullptr` ?

    // l'implémenteur de length() doit supposer que p == nullptr est possible
    int length(zstring p);

    // c'est le travail de l'appelant de s'assurer que p != nullptr
    int length(not_null<zstring> p);

##### Note

`zstring` ne représente pas la propriété.

**Voir aussi** : [Bibliothèque de support](#gsl-guidelines-support-library) @TODO-LINK

### <a name="rf-unique_ptr"></a>F.26 : Utiliser un `unique_ptr<T>` pour transférer la propriété lorsqu'un pointeur est nécessaire

##### Raison

L'utilisation de `unique_ptr` est le moyen le moins coûteux de passer un pointeur en sécurité.

**Voir aussi** : [C.50](007-class.md#rc-factory) @TODO-LINK concernant quand retourner un `shared_ptr` d'une fabrique.

##### Exemple

    unique_ptr<Shape> get_shape(istream& is)  // assembler la forme depuis le flux d'entrée
    {
        auto kind = read_header(is); // lire l'en-tête et identifier la prochaine forme en entrée
        switch (kind) {
        case kCircle:
            return make_unique<Circle>(is);
        case kTriangle:
            return make_unique<Triangle>(is);
        // ...
        }
    }

##### Note

Vous devez passer un pointeur plutôt qu'un objet si ce que vous transférez est un objet d'une hiérarchie de classes qui doit être utilisé à travers une interface (classe de base).

##### Vérification

(Simple) Avertir si une fonction retourne un pointeur brut alloué localement. Suggérer d'utiliser soit `unique_ptr` soit `shared_ptr` à la place.

### <a name="rf-shared_ptr"></a>F.27 : Utiliser un `shared_ptr<T>` pour partager la propriété

##### Raison

L'utilisation de `std::shared_ptr` est le moyen standard de représenter une propriété partagée. C'est-à-dire que le dernier propriétaire supprime l'objet.

##### Exemple

    {
        shared_ptr<const Image> im { read_image(somewhere) };

        std::thread t0 {shade, args0, top_left, im};
        std::thread t1 {shade, args1, top_right, im};
        std::thread t2 {shade, args2, bottom_left, im};
        std::thread t3 {shade, args3, bottom_right, im};

        // détacher les threads requiert une attention supplémentaire (par exemple,
        // les joindre avant la fin de main), mais même si nous détachons les quatre threads ici ...
    }
    // ... shared_ptr garantit que le dernier thread à
    //     terminer supprime en sécurité l'image

##### Note

Privilégier un `unique_ptr` à un `shared_ptr` s'il n'y a jamais plus d'un propriétaire à la fois.
`shared_ptr` est pour la propriété partagée.

Notez que l'utilisation généralisée de `shared_ptr` a un coût (les opérations atomiques sur le compteur de référence du `shared_ptr` ont un coût agrégé mesurable).

##### Alternative

Avoir un seul objet possédant l'objet partagé (par exemple, un objet scopé) et le détruire (de préférence implicitement) lorsque tous les utilisateurs ont terminé.

##### Vérification

(Non vérifiable) C'est un motif trop complexe pour être fiablement détecté.

### <a name="rf-return-ptr"></a>F.42 : Retourner un `T*` pour indiquer une position (uniquement)

##### Raison

C'est à quoi les pointeurs sont bons.
Retourner un `T*` pour transférer la propriété est un abus.

##### Exemple

    Node* find(Node* t, const string& s)  // trouver s dans un arbre binaire de Nodes
    {
        if (!t || t->name == s) return t;
        if ((auto p = find(t->left, s))) return p;
        if ((auto p = find(t->right, s))) return p;
        return nullptr;
    }

Si ce n'est pas le `nullptr`, le pointeur retourné par `find` indique un `Node` contenant `s`.
Importamment, cela n'implique pas un transfert de propriété de l'objet pointé vers l'appelant.

##### Note

Les positions peuvent aussi être transférées par des itérateurs, des indices et des références.
Une référence est souvent une alternative supérieure à un pointeur [s'il n'y a pas besoin d'utiliser `nullptr`](006-functions.md006-functions.md#rf-ptr-ref) ou [si l'objet référencé ne devrait pas changer](014-const.md). @TODO-LINK

##### Note

Ne pas retourner un pointeur vers quelque chose qui n'est pas dans la portée de l'appelant ; voir [F.43](006-functions.md#rf-dangle).

**Voir aussi** : [discussion de la prévention des pointeurs pendants](#???) @TODO-LINK

##### Vérification

* Signaler `delete`, `std::free()`, etc. appliqués à un `T*` brut.
Seuls les propriétaires doivent être supprimés.
* Signaler `new`, `malloc()`, etc. assignés à un `T*` brut.
Seuls les propriétaires doivent être responsables de la suppression.

### <a name="rf-dangle"></a>F.43 : Ne jamais (directement ou indirectement) retourner un pointeur ou une référence vers un objet local

##### Raison

Pour éviter les plantages et la corruption de données qui peuvent résulter de l'utilisation d'un tel pointeur pendant.

##### Exemple, mauvais

Après le retour d'une fonction, ses objets locaux n'existent plus :

    int* f()
    {
        int fx = 9;
        return &fx;  // MAUVAIS
    }

    void g(int* p)   // semble inoffensif
    {
        int gx;
        cout << "*p == " << *p << '\n';
        *p = 999;
        cout << "gx == " << gx << '\n';
    }

    void h()
    {
        int* p = f();
        int z = *p;  // lecture depuis un cadre de pile abandonné (mauvais)
        g(p);        // passer un pointeur vers un cadre de pile abandonné à une fonction (mauvais)
    }

Ici, sur une implémentation populaire, j'ai obtenu la sortie :

    *p == 999
    gx == 999

Je m'y attendais parce que l'appel de `g()` réutilise l'espace de pile abandonné par l'appel de `f()` si bien que `*p` référence l'espace maintenant occupé par `gx`.

* Imaginez ce qui se passerait si `fx` et `gx` étaient de différents types.
* Imaginez ce qui se passerait si `fx` ou `gx` était un type avec un invariant.
* Imaginez ce qui se passerait si ce pointeur pendant était transmis parmi un plus grand ensemble de fonctions.
* Imaginez ce qu'un pirate pourrait faire avec ce pointeur pendant.

Heureusement, la plupart (toutes ?) des compilateurs modernes détectent et préviennent contre ce cas simple.

##### Note

Cela s'applique aussi aux références :

    int& f()
    {
        int x = 7;
        // ...
        return x;  // Mauvais : retourne une référence vers un objet sur le point d'être détruit
    }

##### Note

Cela s'applique uniquement aux variables locales non-`static`.
Toutes les variables `static` sont (comme leur nom l'indique) allouées statiquement, si bien que les pointeurs vers elles ne peuvent pas pender.

##### Exemple, mauvais

Tous les exemples de fuite d'un pointeur vers une variable locale ne sont pas aussi évidents :

    int* glob;       // les variables globales sont mauvaises à tellement d'égards

    template<class T>
    void steal(T x)
    {
        glob = x();  // MAUVAIS
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

Ici j'ai réussi à lire l'emplacement abandonné par l'appel de `f`.
Le pointeur stocké dans `glob` pourrait être utilisé bien plus tard et causer des ennuis de manière imprévisible.

##### Note

L'adresse d'une variable locale peut être « retournée »/fuite par une instruction de retour, par un paramètre de sortie `T&`, comme membre d'un objet retourné, comme élément d'un tableau retourné, et plus encore.

##### Note

Des exemples similaires peuvent être construits « fuyant » un pointeur d'une portée interne vers une portée externe ;
tels exemples sont traités de manière équivalente aux fuites de pointeurs hors d'une fonction.

Une variante légèrement différente du problème est de placer des pointeurs dans un conteneur qui survit aux objets pointés.

**Voir aussi** : Un autre moyen d'obtenir des pointeurs pendants est l'[invalidation de pointeurs](#???). @TODO-LINK
Elle peut être détectée/prévenue avec des techniques similaires.

##### Vérification

* Les compilateurs ont tendance à détecter le retour de référence vers des locaux et pourraient dans de nombreux cas détecter le retour de pointeurs vers des locaux.
* L'analyse statique peut détecter de nombreux motifs communs d'utilisation de pointeurs indiquant des positions (éliminant ainsi les pointeurs pendants)

### <a name="rf-return-ref"></a>F.44 : Retourner un `T&` lorsque la copie est indésirable et que « ne retourner aucun objet » n'est pas nécessaire

##### Raison

Le langage garantit qu'un `T&` référence un objet, si bien qu'un test pour `nullptr` n'est pas nécessaire.

**Voir aussi** : Le retour d'une référence ne doit pas impliquer un transfert de propriété :
[discussion de la prévention des pointeurs pendants](#???) @TODO-LINK et [discussion de la propriété](#???). @TODO-LINK

##### Exemple

    class Car
    {
        array<wheel, 4> w;
        // ...
    public:
        wheel& get_wheel(int i) { Expects(i < w.size()); return w[i]; }
        // ...
    };

    void use()
    {
        Car c;
        wheel& w0 = c.get_wheel(0); // w0 a la même durée de vie que c
    }

##### Vérification

Signaler les fonctions où aucune expression de `return` ne pourrait produire `nullptr`.

### <a name="rf-return-ref-ref"></a>F.45 : Ne pas retourner un `T&&`

##### Raison

C'est inviter à retourner une référence vers un objet temporaire détruit.
Un `&&` est un aimant à objets temporaires.

##### Exemple

Une référence de valeur de droite retournée sort de portée à la fin de l'expression complète à laquelle elle est retournée :

    auto&& x = max(0, 1);   // OK, pour l'instant
    foo(x);                 // Comportement indéfini

Ce type d'usage est une source fréquente de bugs, souvent faussement rapportée comme un bug de compilateur.
Un implémenteur de fonction devrait éviter de tendre de tels pièges aux utilisateurs.

Le [profil de sécurité de durée de vie](022-profile.md#ss-lifetime) @TODO-LINK détectera (quand complètement implémenté) de tels problèmes.


##### Exemple

Retourner une référence de valeur de droite est acceptable lorsque la référence vers le temporaire est transmise « vers le bas » à un appelé ;
dans ce cas, le temporaire est garanti de survivre à l'appel de fonction (voir [F.18](006-functions.md#rf-consume) et [F.19](006-functions.md#rf-forward)).
Cependant, ce n'est pas acceptable lorsque l'on transmet une telle référence « vers le haut » vers une portée d'appelant plus grande.
Pour les fonctions de passage qui transmettent des paramètres (par référence ordinaire ou par transfert parfait) et veulent retourner des valeurs, utiliser la déduction simple de type de retour `auto` (pas `auto&&`).

En supposant que `F` retourne par valeur :

    template<class F>
    auto&& wrapper(F f)
    {
        log_call(typeid(f)); // ou toute autre instrumentation
        return f();          // MAUVAIS : retourne une référence vers un temporaire
    }

Meilleur :

    template<class F>
    auto wrapper(F f)
    {
        log_call(typeid(f)); // ou toute autre instrumentation
        return f();          // OK
    }


##### Exception

`std::move` et `std::forward` retournent bien `&&`, mais ce ne sont que des conversions — utilisées par convention uniquement dans des contextes d'expression où une référence vers un objet temporaire est transmise dans la même expression avant que le temporaire soit détruit. Nous ne connaissons pas d'autres bons exemples de retour de `&&`.

##### Vérification

Signaler tout usage de `&&` comme type de retour, à l'exception de `std::move` et `std::forward`.

### <a name="rf-main"></a>F.46 : `int` est le type de retour de `main()`

##### Raison

C'est une règle du langage, mais violée par des « extensions de langage » si souvent que cela vaut la peine d'être mentionné.
Déclarer `main` (le seul `main` global d'un programme) `void` limite la portabilité.

##### Exemple

        void main() { /* ... */ };  // mauvais, pas du C++

        int main()
        {
            std::cout << "C'est la bonne façon de faire\n";
        }

##### Note

Nous mentionnons cela uniquement à cause de la persistance de cette erreur dans la communauté.
Notez que malgré son type de retour non-vide, la fonction main ne requiert pas d'instruction de retour explicite.

##### Vérification

* Le compilateur devrait le faire
* Si le compilateur ne le fait pas, laisser les outils le signaler

### <a name="rf-assignment-op"></a>F.47 : Retourner `T&` des opérateurs d'affectation

##### Raison

La convention pour les surcharges d'opérateurs (surtout sur des types concrets) est que
`operator=(const T&)` effectue l'affectation puis retourne (non-`const`)
`*this`. Cela garantit la cohérence avec les types de la bibliothèque standard et suit le
principe de « fais comme les ints. »

##### Note

Historiquement, il y avait certaines directives pour rendre l'opérateur d'affectation retourner `const T&`.
C'était principalement pour éviter le code de la forme `(a = b) = c` — un tel code n'est pas assez courant pour justifier de violer la cohérence avec les types standards.

##### Exemple

    class Foo
    {
     public:
        ...
        Foo& operator=(const Foo& rhs)
        {
          // Copier les membres.
          ...
          return *this;
        }
    };

##### Vérification

Cela devrait être appliqué par les outils en vérifiant le type de retour (et la valeur de retour) de tout opérateur d'affectation.

### <a name="rf-return-move-local"></a>F.48 : Ne pas `return std::move(local)`

##### Raison

Retourner une variable locale l'implique implicitement le déplacement déjà.
Un `std::move` explicite est toujours une dégradation de performance, car il empêche l'Optimisation de la Valeur de Retour (RVO),
qui peut éliminer le déplacement complètement.

##### Exemple, mauvais

    S bad()
    {
      S result;
      return std::move(result);
    }

##### Exemple, bon

    S good()
    {
      S result;
      // RVO nommé : élision du déplacement au mieux, construction par déplacement au pire
      return result;
    }

##### Vérification

Cela devrait être appliqué par les outils en vérifiant l'expression de retour.

### <a name="rf-return-const"></a>F.49 : Ne pas retourner `const T`

##### Raison

Il n'est pas recommandé de retourner une valeur `const`.
Ce conseil plus ancien est maintenant obsolète ; il n'ajoute pas de valeur, et interfère avec les sémantiques de déplacement.

##### Exemple

    const vector<int> fct();    // mauvais : ce « const » cause plus de problèmes qu'il n'en vaut la peine

    void g(vector<int>& vx)
    {
        // ...
        fct() = vx;   // empêché par le « const »
        // ...
        vx = fct(); // copie coûteuse : les sémantiques de déplacement sont supprimées par le « const »
        // ...
    }

L'argument pour ajouter `const` à une valeur de retour est qu'il empêche (très rare) l'accès accidentel à un temporaire.
L'argument contre est qu'il empêche (très fréquent) l'utilisation des sémantiques de déplacement.

**Voir aussi** : [F.20, l'élément général sur les valeurs de sortie « out »](006-functions.md#rf-out)

##### Vérification

* Signaler le retour d'une valeur `const`. Pour corriger : supprimer `const` pour retourner une valeur non-`const` à la place.


### <a name="rf-capture-vs-overload"></a>F.50 : Utiliser une lambda lorsqu'une fonction ne suffit pas (pour capturer des variables locales, ou pour écrire une fonction locale)

##### Raison

Les fonctions ne peuvent pas capturer des variables locales ni être définies à portée locale ; si vous avez besoin de ces choses, préférez une lambda lorsque c'est possible, et un objet fonctionnel écrit à la main lorsque ce n'est pas le cas. D'autre part, les lambdas et les objets fonctionnels ne surchargent pas ; si vous avez besoin de surcharger, préférez une fonction (les contournements pour faire surcharger des lambdas sont élaborés). Si les deux fonctionnent, préférez écrire une fonction ; utilisez l'outil le plus simple nécessaire.

##### Exemple

    // écrire une fonction qui ne devrait prendre qu'un int ou une string
    // — la surcharge est naturelle
    void f(int);
    void f(const string&);

    // écrire un objet fonctionnel qui doit capturer un état local et apparaître
    // à portée de déclaration ou d'expression — une lambda est naturelle
    vector<work> v = lots_of_work();
    for (int tasknum = 0; tasknum < max; ++tasknum) {
        pool.run([=, &v] {
            /*
            ...
            ... traiter la (1/max)-ième partie de v, le tasknum-ième morceau
            ...
            */
        });
    }
    pool.join();

##### Exception

Les lambdas génériques offrent un moyen concis d'écrire des modèles de fonction et peuvent donc être utiles même lorsqu'un modèle de fonction normal ferait aussi bien avec un peu plus de syntaxe. Cet avantage disparaîtra probablement à l'avenir une fois que toutes les fonctions auront la capacité d'avoir des paramètres de Concept.

##### Vérification

* Avertir sur l'utilisation d'une lambda non générique nommée (par exemple, `auto x = [](int i) { /*...*/; };`) qui ne capture rien et apparaît à portée globale. Écrire une fonction ordinaire à la place.

### <a name="rf-default-args"></a>F.51 : Lorsqu'il y a un choix, privilégier les arguments par défaut à la surcharge

##### Raison

Les arguments par défaut fournissent simplement des interfaces alternatives à une seule implémentation.
Il n'y a pas de garantie qu'un ensemble de fonctions surchargées implémentent toutes les mêmes sémantiques.
L'utilisation d'arguments par défaut peut éviter la duplication de code.

##### Note

Il y a un choix entre utiliser un argument par défaut et la surcharge lorsque les alternatives proviennent d'un ensemble d'arguments de même type.
Par exemple :

    void print(const string& s, format f = {});

par opposition à

    void print(const string& s);  // utiliser le format par défaut
    void print(const string& s, format f);

Il n'y a pas de choix lorsqu'un ensemble de fonctions est utilisé pour effectuer une opération sémantiquement équivalente sur un ensemble de types. Par exemple :

    void print(const char&);
    void print(int);
    void print(zstring);

##### Voir aussi


[Arguments par défaut pour les fonctions virtuelles](007-class.md007-class.md#rh-virtual-default-arg) @TODO-LINK

##### Vérification

* Avertir sur un ensemble de surcharges où les surcharges ont un préfixe commun de paramètres (par exemple, `f(int)`, `f(int, const string&)`, `f(int, const string&, double)`). (Note : Revoir cette vérification si elle est trop bruyante en pratique.)

### <a name="rf-reference-capture"></a>F.52 : Privilégier la capture par référence dans les lambdas utilisées localement, y compris lorsqu'elles sont passées à des algorithmes

##### Raison

Pour l'efficacité et la justesse, vous voulez presque toujours capturer par référence lorsque vous utilisez la lambda localement. Cela inclut l'écriture ou l'appel d'algorithmes parallèles qui sont locaux parce qu'ils se rejoignent avant de retourner.

##### Discussion

La considération d'efficacité est que la plupart des types sont moins chers à passer par référence que par valeur.

La considération de justesse est que beaucoup d'appels veulent effectuer des effets de bord sur l'objet original au site d'appel (voir l'exemple ci-dessous). Passer par valeur l'empêche.

##### Note

Malheureusement, il n'y a pas de simple moyen de capturer par référence vers `const` pour obtenir l'efficacité pour un appel local tout en empêchant les effets de bord.

##### Exemple

Ici, un grand objet (un message réseau) est passé à un algorithme itératif, et ce n'est ni efficace ni correct de copier le message (qui pourrait ne pas être copiable) :

    std::for_each(begin(sockets), end(sockets), [&message](auto& socket)
    {
        socket.send(message);
    });

##### Exemple

Ceci est un simple pipeline parallèle à trois étapes. Chaque objet `stage` encapsule un thread travailleur et une file, a une fonction `process` pour mettre le travail en file, et dans son destructeur bloque automatiquement en attendant que la file se vide avant de terminer le thread.

    void send_packets(buffers& bufs)
    {
        stage encryptor([](buffer& b) { encrypt(b); });
        stage compressor([&](buffer& b) { compress(b); encryptor.process(b); });
        stage decorator([&](buffer& b) { decorate(b); compressor.process(b); });
        for (auto& b : bufs) { decorator.process(b); }
    }  // bloque automatiquement en attendant que le pipeline se termine

##### Vérification

Signaler une lambda qui capture par référence, mais qui est utilisée autre que localement dans la portée de fonction ou passée par référence à une fonction. (Note : cette règle est une approximation, mais signale le passage par pointeur car ceux-ci sont plus susceptibles d'être stockés par l'appelé, d'écrire dans un emplacement du tas accessible via un paramètre, de retourner la lambda, etc. Les règles de Durée de vie fourniront aussi des règles générales qui signalent les pointeurs et références échappants y compris via des lambdas.)

### <a name="rf-value-capture"></a>F.53 : Éviter la capture par référence dans les lambdas utilisées non-localement, y compris lorsqu'elles sont retournées, stockées sur le tas, ou passées à un autre thread

##### Raison

Les pointeurs et références vers des locaux ne devraient pas survivre à leur portée. Les lambdas qui capturent par référence sont juste un autre endroit pour stocker une référence vers un objet local, et ne devraient pas le faire si elles (ou une copie) survivent à la portée.

##### Exemple, mauvais

    int local = 42;

    // Vouloir une référence vers local.
    // Notez qu'après la sortie de ce scope du programme,
    // local n'existe plus, donc
    // l'appel process() aura un comportement indéfini !
    thread_pool.queue_work([&] { process(local); });

##### Exemple, bon

    int local = 42;
    // Vouloir une copie de local.
    // Puisqu'une copie de local est faite, elle sera
    // toujours disponible pour l'appel.
    thread_pool.queue_work([=] { process(local); });

##### Note

Si un pointeur non local doit être capturé, considérer l'utilisation de `unique_ptr` ; cela gère à la fois la durée de vie et la synchronisation.

Si le pointeur `this` doit être capturé, considérer l'utilisation de la capture `[*this]`, qui crée une copie de l'objet entier.

##### Vérification

* (Simple) Avertir lorsque la liste de capture contient une référence vers une variable déclarée localement
* (Complexe) Signaler lorsque la liste de capture contient une référence vers une variable déclarée localement et que la lambda est passée dans un contexte non-`const` et non local

### <a name="rf-this-capture"></a>F.54 : Lorsque vous écrivez une lambda qui capture `this` ou un membre de données de classe, n'utiliser pas la capture par défaut `[=]`

##### Raison

C'est confus. Écrire `[=]` dans une fonction membre semble capturer par valeur, mais capture en réalité les membres de données par référence car elle capture en réalité le pointeur `this` invisible par valeur. Si vous vouliez faire cela, écrire `this` explicitement.

##### Exemple

    class My_class {
        int x = 0;
        // ...

        void f()
        {
            int i = 0;
            // ...

            auto lambda = [=] { use(i, x); };   // MAUVAIS : « ressemble à » une capture par valeur

            x = 42;
            lambda(); // appelle use(0, 42);
            x = 43;
            lambda(); // appelle use(0, 43);

            // ...

            auto lambda2 = [i, this] { use(i, x); }; // ok, le plus explicite et le moins confus

            // ...
        }
    };

##### Note

Si vous