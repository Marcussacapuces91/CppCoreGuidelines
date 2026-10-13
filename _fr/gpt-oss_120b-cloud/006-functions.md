# <a name="s-functions"></a>F : Fonctions

Une fonction spécifie une action ou un calcul qui fait passer le système d'un état cohérent à l'état suivant. C’est le bloc de construction fondamental des programmes.

Il doit être possible de nommer une fonction de façon pertinente, de préciser les exigences de ses arguments et d'énoncer clairement la relation entre les arguments et le résultat. Une implémentation n’est pas une spécification. Essayez de penser à ce que fait une fonction **et** à la façon dont elle le fait.  

Les fonctions sont la partie la plus critique de la plupart des interfaces ; consultez donc les règles d’interface.

## Récapitulatif des règles de fonction

### Règles de définition de fonction

* [F.1 : « Package » opérations significatives comme fonctions soigneusement nommées](006-functions.md#rf-package)  
* [F.2 : Une fonction doit réaliser une seule opération logique](006-functions.md#rf-logical)  
* [F.3 : Garder les fonctions courtes et simples](006-functions.md#rf-single)  
* [F.4 : Si une fonction doit pouvoir être évaluée à la compilation, la déclarer `constexpr`](006-functions.md#rf-constexpr)  
* [F.5 : Si une fonction est très petite et critique en temps, la déclarer `inline`](006-functions.md#rf-inline)  
* [F.6 : Si votre fonction ne doit pas lancer d’exception, la déclarer `noexcept`](006-functions.md#rf-noexcept)  
* [F.7 : Pour un usage général, prendre des arguments `T*` ou `T&` plutôt que des pointeurs intelligents](006-functions.md#rf-smart)  
* [F.8 : Privilégier les fonctions pures](006-functions.md#rf-pure)  
* [F.9 : Les paramètres inutilisés doivent être non nommés](006-functions.md#rf-unused)  
* [F.10 : Si une opération peut être réutilisée, lui donner un nom](006-functions.md#rf-name)  
* [F.11 : Utiliser une lambda anonyme si vous avez besoin d’un simple objet fonctionnel à un seul endroit](006-functions.md#rf-lambda)  

### Règles d’expression du passage de paramètres

* [F.15 : Préférer les façons simples et conventionnelles de transmettre l’information](006-functions.md#rf-conventional)  
* [F.16 : Pour les paramètres « in », passer les types peu coûteux à copier par valeur et les autres par référence `const`](006-functions.md#rf-in)  
* [F.17 : Pour les paramètres « in‑out », passer par référence non‑`const`](006-functions.md#rf-inout)  
* [F.18 : Pour les paramètres « will‑move‑from », passer par `X&&` et `std::move` le paramètre](006-functions.md#rf-consume)  
* [F.19 : Pour les paramètres « forward », passer par `TP&&` et n’utiliser que `std::forward` sur le paramètre](006-functions.md#rf-forward)  
* [F.20 : Pour les valeurs de sortie « out », privilégier les valeurs de retour plutôt que les paramètres de sortie](006-functions.md#rf-out)  
* [F.21 : Pour renvoyer plusieurs valeurs « out », privilégier le retour d’une structure](006-functions.md#rf-out-multi)  
* [F.60 : Préférer `T*` à `T&` lorsqu’une option « pas d’argument » est valide](006-functions.md#rf-ptr-ref)  

### Règles sémantiques du passage de paramètres

* [F.22 : Utiliser `T*` ou `owner<T*>` pour désigner un seul objet](006-functions.md#rf-ptr)  
* [F.23 : Utiliser un `not_null<T>` pour indiquer que « null » n’est pas une valeur valide](006-functions.md#rf-nullptr)  
* [F.24 : Utiliser un `span<T>` ou un `span_p<T>` pour désigner une séquence demi‑ouverte](006-functions.md#rf-range)  
* [F.25 : Utiliser un `zstring` ou un `not_null<zstring>` pour désigner une chaîne de style C](006-functions.md#rf-zstring)  
* [F.26 : Utiliser `unique_ptr<T>` pour transférer la propriété lorsqu’un pointeur est nécessaire](006-functions.md#rf-unique_ptr)  
* [F.27 : Utiliser `shared_ptr<T>` pour partager la propriété](006-functions.md#rf-shared_ptr)  

### Règles sémantiques du retour de valeur

* [F.42 : Retourner un `T*` pour indiquer une position (seulement)](006-functions.md#rf-return-ptr)  
* [F.43 : Ne jamais (directement ou indirectement) retourner un pointeur ou une référence vers un objet local](006-functions.md#rf-dangle)  
* [F.44 : Retourner un `T&` quand la copie est indésirable et que « ne rien retourner » n’est pas nécessaire](006-functions.md#rf-return-ref)  
* [F.45 : Ne pas retourner un `T&&`](006-functions.md#rf-return-ref-ref)  
* [F.46 : `int` est le type de retour de `main()`](006-functions.md#rf-main)  
* [F.47 : Retourner `T&` depuis les opérateurs d’affectation](006-functions.md#rf-assignment-op)  
* [F.48 : Ne pas `return std::move(local)`](006-functions.md#rf-return-move-local)  
* [F.49 : Ne pas retourner `const T`](006-functions.md#rf-return-const)  

### Autres règles de fonction

* [F.50 : Utiliser une lambda lorsqu’une fonction ne convient pas (pour capturer des variables locales ou écrire une fonction locale)](006-functions.md#rf-capture-vs-overload) @TODO‑LINK  
* [F.51 : Quand un choix est possible, privilégier les arguments par défaut aux surcharges](006-functions.md#rf-default-args) @TODO‑LINK  
* [F.52 : Préférer la capture par référence dans les lambdas utilisées localement, y compris lorsqu’elles sont passées à des algorithmes](006-functions.md#rf-reference-capture)  
* [F.53 : Éviter la capture par référence dans les lambdas qui seront utilisées de façon non locale, y compris retournées, stockées sur le tas ou passées à un autre thread](006-functions.md#rf-value-capture)  
* [F.54 : Lors de l’écriture d’une lambda capturant `this` ou tout membre de classe, ne pas utiliser la capture par défaut `[=]`](006-functions.md#rf-this-capture)  
* [F.55 : Ne pas utiliser d’arguments `va_arg`](006-functions.md#f-varargs)  
* [F.56 : Éviter les imbrications de conditions inutiles](006-functions.md#f-nesting)  

Les fonctions présentent de fortes similitudes avec les lambdas et les objets fonctionnels.

**Voir aussi** : [C.lambdas : objets fonctionnels et lambdas](007-class.md#ss-lambdas) @TODO‑LINK  

## <a name="ss-fct-def"></a>F.def : Définitions de fonctions

Une définition de fonction est une déclaration de fonction qui précise également l’implémentation, c’est‑à‑dire le corps de la fonction.

### <a name="rf-package"></a>F.1 : « Package » opérations significatives comme fonctions soigneusement nommées

##### Raison

Factoriser le code commun rend le code plus lisible, plus susceptible d’être réutilisé et limite les erreurs provenant de code complexe.  
Si une action est bien spécifiée, séparez‑la du code qui l’entoure et donnez‑lui un nom.

##### Exemple, à éviter

    void read_and_print(istream& is)    // lire et afficher un int
    {
        int x;
        if (is >> x)
            cout << "the int is " << x << '\n';
        else
            cerr << "no int on input\n";
    }

Pratiquement tout est erroné dans `read_and_print`.  
Elle lit, écrit (vers un `ostream` fixe), écrit les messages d’erreur (vers un `ostream` fixe), ne gère que les `int`.  
Il n’y a rien à réutiliser, les opérations logiques sont entremêlées et les variables locales restent en portée après la fin de leur usage logique.  
Pour un exemple minuscule cela paraît acceptable, mais si les opérations d’entrée, de sortie et de gestion d’erreur deviennent plus complexes, le désordre devient difficile à comprendre.

##### Note

Si vous écrivez une lambda non triviale qui peut être utilisée à plusieurs endroits, donnez‑lui un nom en l’affectant à une (généralement non locale) variable.

##### Exemple

    sort(a, b, [](T x, T y) { return x.rank() < y.rank() && x.value() < y.value(); });

Nommer cette lambda découpe l’expression en ses parties logiques et indique clairement son sens.

    auto lessT = [](T x, T y) { return x.rank() < y.rank() && x.value() < y.value(); };

    sort(a, b, lessT);

Le code le plus court n’est pas toujours le meilleur en termes de performances ou de maintenabilité.

##### Exception

Les corps de boucles, y compris les lambdas utilisées comme corps de boucle, n’ont que rarement besoin d’être nommés.  
Cependant, de gros corps de boucle (ex. plusieurs dizaines de lignes ou pages) peuvent poser problème.  
La règle [Gardez les fonctions courtes et simples](006-functions.md#rf-single) implique « Gardez les corps de boucle courts ».  
De même, les lambdas utilisées comme arguments de rappel sont parfois non triviales, mais peu susceptibles d’être réutilisables.

##### Application

* Voir [Gardez les fonctions courtes et simples](006-functions.md#rf-single)  
* Signaler les lambdas identiques ou très similaires employés à des endroits différents.

### <a name="rf-logical"></a>F.2 : Une fonction doit réaliser une seule opération logique

##### Raison

Une fonction qui réalise une seule opération est plus simple à comprendre, à tester et à réutiliser.

##### Exemple

    void read_and_print()    // mauvais
    {
        int x;
        cin >> x;
        // vérifier les erreurs
        cout << x << "\n";
    }

Il s’agit d’un monolithe lié à une entrée précise et ne pourra jamais être réutilisé autrement.  
Divisez les fonctions en parties logiques appropriées et paramétrez‑les :

    int read(istream& is)    // mieux
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

Elles peuvent maintenant être combinées où nécessaire :

    void read_and_print()
    {
        auto x = read(cin);
        print(cout, x);
    }

Si besoin, on peut encore les rendre génériques :

    auto read = [](auto& input, auto& value)    // mieux
    {
        input >> value;
        // vérifier les erreurs
    };

    void print(auto& output, const auto& value)
    {
        output << value << "\n";
    }

##### Application

* Considérer suspectes les fonctions possédant plus d’un paramètre « out ». Préférer les valeurs de retour, y compris `tuple` pour plusieurs valeurs.  
* Considérer suspectes les fonctions « grosses » qui ne tiennent pas sur un écran d’éditeur. Envisager de les factoriser en sous‑opérations bien nommées.  
* Considérer suspectes les fonctions avec 7 paramètres ou plus.

### <a name="rf-single"></a>F.3 : Garder les fonctions courtes et simples

##### Raison

Les fonctions volumineuses sont difficiles à lire, plus susceptibles de contenir du code complexe et de posséder des variables dont la portée dépasse le strict nécessaire.  
Des structures de contrôle complexes entraînent davantage de lignes et masquent plus facilement les erreurs logiques.

##### Exemple

    double simple_func(double val, int flag1, int flag2)
        // simple_func : prend une valeur et calcule la sortie ASIC attendue,
        // en fonction des deux drapeaux de mode.
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

C’est trop complexe.  
Comment savoir si toutes les alternatives ont été correctement gérées ? Oui, cela viole d’autres règles également.

Refactorisation possible :

    double func1_muon(double val, int flag)
    {
        // ???
    }

    double func1_tau(double val, int flag1, int flag2)
    {
        // ???
    }

    double simple_func(double val, int flag1, int flag2)
        // simple_func : prend une valeur et calcule la sortie ASIC attendue,
        // en fonction des deux drapeaux de mode.
    {
        if (flag1 > 0)
            return func1_muon(val, flag2);
        if (flag1 == -1)
            // géré par func1_tau : flag1 = -flag1;
            return func1_tau(-val, flag1, flag2);
        return 0.;
    }

##### Note

« Ça ne tient pas sur un écran » est souvent une bonne définition pratique de « trop grand ».  
Les fonctions d’une à cinq lignes sont à considérer comme normales.

##### Note

Divisez les fonctions volumineuses en fonctions plus petites, cohésives et nommées.  
Les petites fonctions simples sont facilement inline lorsque le coût d’un appel de fonction est important.

##### Application

* Signaler les fonctions qui ne « tiennent pas sur un écran ».  
  Quelle taille constitue un écran ? On peut prendre 60 lignes sur 140 caractères ; c’est à peu près la limite confortable pour une page de livre.  
* Signaler les fonctions trop complexes. Qu’est‑ce qui est « trop » ? On peut utiliser la complexité cyclomatique : plus de 10 chemins logiques distincts est souvent excessif.

### <a name="rf-constexpr"></a>F.4 : Si une fonction doit pouvoir être évaluée à la compilation, la déclarer `constexpr`

##### Raison

`constexpr` indique au compilateur qu’il est autorisé à évaluer la fonction à la compilation.

##### Exemple

Le (in)fâme factoriel :

    constexpr int fac(int n)
    {
        constexpr int max_exp = 17;      // constexpr rend max_exp utilisable dans Expects
        Expects(0 <= n && n < max_exp); // prévenir les abus et débordements
        int x = 1;
        for (int i = 2; i <= n; ++i) x *= i;
        return x;
    }

C’est du C++14.  
Pour le C++11, on utilise une formulation récursive de `fac()`.

##### Note

`constexpr` ne garantit pas l’évaluation à la compilation ; il garantit seulement que la fonction *peut* être évaluée à la compilation pour des arguments const‑expr si le programmeur l’exige ou si le compilateur le juge opportun pour optimisation.

    constexpr int min(int x, int y) { return x < y ? x : y; }

    void test(int v)
    {
        int m1 = min(-1, 2);            // probablement à la compilation
        constexpr int m2 = min(-1, 2);   // à la compilation
        int m3 = min(-1, v);            // évaluation à l’exécution
        constexpr int m4 = min(-1, v);  // erreur : impossible à évaluer à la compilation
    }

##### Note

Ne cherchez pas à rendre toutes les fonctions `constexpr`.  
La plupart des calculs sont mieux effectués à l’exécution.

##### Note

Toute API qui pourrait dépendre d’une configuration d’exécution haute‑niveau ou de logique métier ne doit pas être `constexpr`. Ce type de personnalisation ne peut pas être évalué par le compilateur, et toute fonction `constexpr` qui dépend de cette API devrait être refactorisée ou perdre le `constexpr`.

##### Application

Impossible et inutile. Le compilateur signale une erreur si une fonction non‑`constexpr` est appelée dans un contexte nécessitant une constante.

### <a name="rf-inline"></a>F.5 : Si une fonction est très petite et critique en temps, la déclarer `inline`

##### Raison

Certains optimiseurs inline sans indice du programmeur, mais ne comptez pas dessus.  
Mesurez ! Depuis plus de quarante ans, on promet des compilateurs capables d’inlining supérieur à celui des humains sans indices. Nous attendons toujours.  
Spécifier `inline` (explicitement ou implicitement lorsqu’on écrit les fonctions membres dans la définition de la classe) incite le compilateur à faire un meilleur travail.

##### Exemple

    inline string cat(const string& s, const string& s2) { return s + s2; }

##### Exception

Ne placez pas une fonction `inline` dans une interface stable tant que vous n’êtes pas certain qu’elle ne changera pas.  
Une fonction `inline` fait partie de l’ABI.

##### Note

`constexpr` implique `inline`.

##### Note

Les fonctions membres définies dans la classe sont `inline` par défaut.

##### Exception

Les modèles de fonction (y compris les fonctions membres de modèles de classe `A<T>::function()` et les modèles de fonction membres `A::function<T>()`) sont généralement définis dans les en‑têtes, donc `inline`.

##### Note

Envisagez de mettre hors‑ligne les fonctions qui comportent plus de trois instructions et qui peuvent être déclarées hors‑ligne (comme les fonctions membres de classe).

### <a name="rf-noexcept"></a>F.6 : Si votre fonction ne doit pas lancer d’exception, la déclarer `noexcept`

##### Raison

Si une exception n’est pas censée être levée, le programme ne peut pas compter sur la capacité à gérer l’erreur et doit se terminer le plus rapidement possible.  
Déclarer une fonction `noexcept` aide les optimiseurs en réduisant le nombre de chemins d’exécution alternatifs. Cela accélère également la sortie après un échec.

##### Exemple

Mettez `noexcept` sur chaque fonction écrite entièrement en C ou dans tout autre langage sans exceptions.  
La bibliothèque standard C++ le fait implicitement pour toutes les fonctions de la bibliothèque C.

##### Note

Les fonctions `constexpr` peuvent lancer lorsqu’elles sont évaluées à l’exécution ; vous pourriez donc avoir besoin d’un `noexcept` conditionnel pour certaines d’elles.

##### Exemple

    vector<string> collect(istream& is) noexcept
    {
        vector<string> res;
        for (string s; is >> s;)
            res.push_back(s);
        return res;
    }

Si `collect()` manque de mémoire, le programme plante.  
À moins que le programme ne soit conçu pour survivre à l’épuisement de la mémoire, cela peut être le comportement souhaité ; `terminate()` peut générer les informations de journal adéquates (mais lorsqu’on n’a plus de mémoire, il est difficile de faire quelque chose d’intelligent).

##### Note

Vous devez connaître l’environnement d’exécution dans lequel votre code s’exécute avant d’ajouter `noexcept`, en particulier à cause du problème de lancer et d’allocation.  
Le code qui se veut parfaitement général (comme la bibliothèque standard et d’autres utilitaires) doit pouvoir gérer les environnements où une exception `bad_alloc` pourrait être traitée de façon significative.  
Cependant, la plupart des programmes et environnements d’exécution ne peuvent pas gérer de façon sensée un échec d’allocation ; abortir le programme est la réponse la plus propre et la plus simple dans ces cas.  
Si vous savez que votre code applicatif ne peut pas réagir à un échec d’allocation, il peut être approprié d’ajouter `noexcept` même sur les fonctions qui allouent.

En d’autres termes : dans la plupart des programmes, la majorité des fonctions peuvent lancer (par ex. parce qu’elles utilisent `new`, appellent des fonctions qui le font ou utilisent des fonctions de bibliothèque qui signalent les échecs par exception), donc ne parsemez pas simplement le code de `noexcept` sans réfléchir à la possibilité de gérer les exceptions.

`no noexcept` est le plus utile (et le plus clairement correct) pour les fonctions bas‑niveau fréquemment utilisées.

##### Note

Les destructeurs, fonctions `swap`, opérations de déplacement et constructeurs par défaut ne doivent jamais lancer. Voir aussi [C.44](007-class.md#rc-default00) @TODO‑LINK.

##### Note

Il faut être prudent avec les fonctions virtuelles de base et les fonctions faisant partie d’une interface publique : déclarer une fonction `noexcept` établit une garantie que toutes les implémentations présentes et futures doivent respecter. Pour une fonction virtuelle, tous les surdéfinisseurs doivent également être `noexcept` ; retirer `noexcept` d’une fonction pourrait casser les appelants.

##### Application

* (rigide) Signaler les fonctions bas‑niveau qui ne sont pas `noexcept` alors qu’elles ne peuvent pas lancer.  
* Signaler les `swap`, `move`, destructeurs et constructeurs par défaut qui lancent.

### <a name="rf-smart"></a>F.7 : Pour un usage général, prendre des arguments `T*` ou `T&` plutôt que des pointeurs intelligents

##### Raison

Passer un pointeur intelligent transfère ou partage la propriété et ne doit être utilisé que lorsqu’on veut réellement exprimer une sémantique de propriété.  
Une fonction qui ne manipule pas la durée de vie d’un objet doit prendre des pointeurs bruts ou des références.

Utiliser un pointeur intelligent restreint l’usage de la fonction aux appelants qui utilisent ce même type de pointeur.  
Une fonction qui a besoin d’un `widget` devrait pouvoir accepter tout objet `widget`, pas seulement ceux dont la durée de vie est gérée par un type de pointeur intelligent donné.

Passer un pointeur partagé (`std::shared_ptr`) implique un coût d’exécution à l’exécution.

##### Exemple

    // accepte n’importe quel int*
    void f(int*);

    // n’accepte que les ints dont on veut transférer la propriété
    void g(unique_ptr<int>);

    // n’accepte que les ints dont on veut partager la propriété
    void g(shared_ptr<int>);

    // ne change pas la propriété, mais requiert une propriété particulière du caller
    void h(const unique_ptr<int>&);

    // accepte tout int
    void h(int&);

##### Exemple, mauvais

    // callee
    void f(shared_ptr<widget>& w)
    {
        // ...
        use(*w); // seul usage de w – la durée de vie n’est pas concernée
        // ...
    };

    // caller
    shared_ptr<widget> my_widget = /* ... */;
    f(my_widget);

    widget stack_widget;
    f(stack_widget); // erreur

##### Exemple, bon

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
    f(stack_widget); // ok – maintenant cela fonctionne

##### Note

Nous pouvons attraper de nombreux cas courants de pointeurs pendants statiquement (voir [profil de sécurité de durée de vie](022-profile.md#ss-lifetime)). Les arguments de fonction vivent naturellement pendant l’appel de la fonction, et donc présentent moins de problèmes de durée de vie.

##### Application

* (simple) Avertir si une fonction prend un paramètre de type pointeur intelligent (qui surcharge `operator->` ou `operator*`) copiable alors que la fonction se contente d’appeler `operator*`, `operator->` ou `get()`. Suggérer d’utiliser `T*` ou `T&` à la place.  
* Signaler un paramètre de type pointeur intelligent copiable/movable qui n’est jamais copié/moved dans le corps de la fonction, qui n’est jamais modifié et qui n’est pas transmis à une autre fonction pouvant le faire. Cela indique que la sémantique de propriété n’est pas utilisée. Suggérer d’utiliser `T*` ou `T&`.

**Voir aussi** :

* [Préférer `T*` à `T&` lorsqu’une option « pas d’argument » est valide](006-functions.md#rf-ptr-ref)  
* [Résumé des règles sur les pointeurs intelligents](009-resource.md#rr-summary-smartptrs)  

### <a name="rf-pure"></a>F.8 : Privilégier les fonctions pures

##### Raison

Les fonctions pures sont plus faciles à raisonner, parfois plus faciles à optimiser (et même à paralléliser) et peuvent parfois être mémorisées.

##### Exemple

    template<class T>
    auto square(T t) { return t * t; }

##### Application

Non applicable ; il n’est pas possible d’imposer cela automatiquement.

### <a name="rf-unused"></a>F.9 : Les paramètres inutilisés doivent être non nommés

##### Raison

Lisibilité. Suppression des avertissements de paramètres inutilisés.

##### Exemple

    widget* find(const set<widget>& s, const widget& w, Hint);   // autrefois, un indice était utilisé

##### Note

Autoriser les paramètres non nommés a été introduit au début des années 80 pour résoudre ce problème.

Si les paramètres sont conditionnellement inutilisés, déclarez‑les avec l’attribut `[[maybe_unused]]`. Par exemple :

    template <typename Value>
    Value* find(const set<Value>& s, const Value& v, [[maybe_unused]] Hint h)
    {
        if constexpr (sizeof(Value) > CacheSize)
        {
            // un indice n’est utilisé que si Value a une certaine taille
        }
    }

##### Application

Signaler les paramètres nommés qui ne sont jamais utilisés.

### <a name="rf-name"></a>F.10 : Si une opération peut être réutilisée, lui donner un nom

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

    vector<Rec*> find_id(const string& name);    // trouve tous les enregistrements pour « name »

    auto x = find_if(vr.begin(), vr.end(),
        [&](Rec& r) {
            if (r.name.size() != n.size()) return false; // n est le nom à comparer
            for (int i = 0; i < r.name.size(); ++i)
                if (tolower(r.name[i]) != tolower(n[i])) return false;
            return true;
        }
    );

Il existe ici une fonction utile (comparaison de chaînes insensible à la casse), comme il arrive souvent quand les arguments lambda deviennent volumineux.

    bool compare_insensitive(const string& a, const string& b)
    {
        if (a.size() != b.size()) return false;
        for (int i = 0; i < a.size(); ++i) if (tolower(a[i]) != tolower(b[i])) return false;
        return true;
    }

    auto x = find_if(vr.begin(), vr.end(),
        [&](Rec& r) { return compare_insensitive(r.name, n); }
    );

Ou, si vous préférez éviter la liaison implicite de `n` :

    auto cmp_to_n = [&n](const string& a) { return compare_insensitive(a, n); };

    auto x = find_if(vr.begin(), vr.end(),
        [](const Rec& r) { return cmp_to_n(r.name); }
    );

##### Note

Cela vaut que ce soit pour des fonctions, des lambdas ou des opérateurs.

##### Exception

* Lambdas logiquement utilisées uniquement localement, comme argument de `for_each` et d’algorithmes similaires.  
* Lambdas comme [initialisateurs](#???) (section manquante).

##### Application

* (rigide) Signaler les lambdas similaires.  
* ?

### <a name="rf-lambda"></a>F.11 : Utiliser une lambda non nommée si vous avez besoin d’un simple objet fonctionnel à un seul endroit

##### Raison

Cela rend le code concis et offre une meilleure localisation que les alternatives.

##### Exemple

    auto earlyUsersEnd = std::remove_if(users.begin(), users.end(),
                                        [](const User &a) { return a.id > 100; });

##### Exception

Nommer une lambda peut être utile pour plus de clarté même si elle n’est utilisée qu’une fois.

##### Application

* Rechercher les lambdas identiques ou quasi‑identiques (pour les remplacer par des fonctions nommées ou des lambdas nommées).

## <a name="ss-call"></a>F.call : Passage de paramètres

Il existe plusieurs façons de passer des paramètres à une fonction et de renvoyer des valeurs.

### <a name="rf-conventional"></a>F.15 : Préférer les façons simples et conventionnelles de transmettre l’information

##### Raison

Les techniques « inhabituelles et astucieuses » provoquent des surprises, ralentissent la compréhension par d’autres programmeurs et favorisent les bugs.  
Si vous avez réellement besoin d’une optimisation au‑delà des techniques courantes, mesurez pour vous assurer que c’est réellement une amélioration, puis documentez/commmentez car l’amélioration peut ne pas être portable.

Les tableaux suivants résument les conseils des lignes directrices F.16‑21.

**Passage de paramètres normal** :

![Normal parameter passing table](./param-passing-normal.png "Passage de paramètres normal")

**Passage de paramètres avancé** :

![Advanced parameter passing table](./param-passing-advanced.png "Passage de paramètres avancé")

Utilisez les techniques avancées seulement après avoir démontré la nécessité, et documentez ce besoin dans un commentaire.

Pour passer des séquences de caractères, voir [String](018-stdlib.md#ss-string).

##### Exception

Pour exprimer la propriété partagée avec des types `shared_ptr`, au lieu de suivre les règles F.16‑21, suivez [R.34](009-resource.md#rr-sharedptrparam-owner), [R.35](009-resource.md#rr-sharedptrparam) et [R.36](009-resource.md#rr-sharedptrparam-const).

### <a name="rf-in"></a>F.16 : Pour les paramètres « in », passer les types peu coûteux à copier par valeur et les autres par référence `const`

##### Raison

Ces deux approches indiquent à l’appelant que la fonction ne modifiera pas l’argument, et les deux permettent l’initialisation à partir de r‑values.

Ce qu’est « peu coûteux à copier » dépend de l’architecture, mais deux ou trois mots (double, pointeur, référence) sont généralement meilleurs passés par valeur.  
Quand la copie est peu coûteuse, rien ne bat la simplicité et la sécurité de la copie ; pour les petits objets (jusqu’à deux ou trois mots) c’est même plus rapide que le passage par référence, puisqu’il n’y a pas d’indirection supplémentaire.

##### Exemple

    void f1(const string& s);  // OK : passage par référence `const`; toujours peu coûteux

    void f2(string s);         // mauvais : potentiellement cher

    void f3(int x);            // OK : imbattable

    void f4(const int& x);     // mauvais : surcharge d’accès dans f4()

Pour les usages avancés (uniquement), lorsque vous devez réellement optimiser les r‑values passées à des paramètres « input‑only » :

* Si la fonction va inconditionnellement déplacer l’argument, prenez‑le par `&&`. Voir [F.18](006-functions.md#rf-consume).  
* Si la fonction garde une copie locale modifiable uniquement pour son usage interne, passer par valeur suffit.  
* Si la fonction garde une copie de l’argument à transmettre ailleurs (à une autre fonction ou à un emplacement non local), en plus du passage par `const&` (pour les l‑values), ajoutez une surcharge qui prend le paramètre par `&&` (pour les r‑values) et dans le corps `std::move` vers la destination. C’est essentiellement le cas « will‑move‑from » ; voir [F.18](006-functions.md#rf-consume).  
* Dans des cas spéciaux, comme plusieurs paramètres « input + copy », envisagez le transfert parfait. Voir [F.19](006-functions.md#rf-forward).

##### Exemple

    int multiply(int, int); // uniquement des int d’entrée, passer par valeur

    // le suffixe est uniquement d’entrée mais pas aussi léger qu’un int, passer par const&
    string& concatenate(string&, const string& suffix);

    void sink(unique_ptr<widget>);  // uniquement d’entrée, et déplace la propriété du widget

Évitez les « techniques ésotériques » comme passer des arguments en `T&&` « pour l’efficacité ». La plupart des rumeurs sur les gains de performance grâce à `&&` sont fausses ou fragiles (mais voir [F.18](006-functions.md#rf-consume) et [F.19](006-functions.md#rf-forward)).

##### Notes

Une référence peut être supposée référencer un objet valide (règle du langage).  
Il n’existe pas de « référence nulle ».  
Si vous avez besoin d’une valeur optionnelle, utilisez un pointeur, `std::optional` ou une valeur spéciale désignant « pas de valeur ».

##### Application

* (simple) Avertir lorsqu’un paramètre passé par valeur a une taille supérieure à `4 * sizeof(void*)`. Suggérer de le passer par référence `const`.  
* (simple) Avertir lorsqu’un paramètre passé par référence `const` a une taille inférieure ou égale à `2 * sizeof(void*)`. Suggérer le passage par valeur.  
* (simple) Avertir lorsqu’un paramètre passé par référence `const` est déplacé (`move`).  
* (non simple) Note : une application plus stricte dépendrait des caractéristiques de performance de l’architecture cible.

##### Exception

Pour exprimer la propriété partagée avec des `shared_ptr`, suivez [R.34](009-resource.md#rr-sharedptrparam-owner) ou [R.36](009-resource.md#rr-sharedptrparam-const), selon que la fonction prend inconditionnellement une référence à l’argument.

### <a name="rf-inout"></a>F.17 : Pour les paramètres « in‑out », passer par référence non‑`const`

##### Raison

Cela indique clairement aux appelants que l’objet est supposé être modifié.

##### Exemple

    void update(Record& r);  // on suppose que update écrit dans r

##### Note

Certains types définis par l’utilisateur et de la bibliothèque standard, comme `span<T>` ou les itérateurs, sont [peu coûteux à copier](006-functions.md#rf-in) et peuvent être passés par valeur tout en conservant une sémantique de référence mutable :

    void increment_all(span<int> a)
    {
      for (auto&& e : a)
        ++e;
    }

##### Note

Un argument `T&` peut transmettre des informations à la fonction ainsi que recevoir des informations. Ainsi `T&` peut être un paramètre in‑out. Cela peut en soi poser problème :

    void f(string& s)
    {
        s = "New York";  // erreur non évidente
    }

    void g()
    {
        string buffer = ".................................";
        f(buffer);
        // …
    }

Ici, l’auteur de `g()` fournit un tampon à remplir, mais `f()` le remplace complètement (à un coût légèrement supérieur à une simple copie des caractères). Une mauvaise logique peut survenir si l’auteur de `g()` suppose à tort la taille du tampon.

##### Application

* (modéré) Avertir sur les fonctions qui prennent une référence non‑`const` mais n’écrivent jamais dedans.  
* (simple) Avertir lorsqu’un paramètre non‑`const` passé par référence est déplacé (`move`).

### <a name="rf-consume"></a>F.18 : Pour les paramètres « will‑move‑from », passer par `X&&` et `std::move` le paramètre

##### Raison

C’est efficace et élimine les bugs du site d’appel : `X&&` ne lie qu’aux r‑values, ce qui oblige l’appelant à faire explicitement `std::move` s’il passe une l‑value.

##### Exemple

    void sink(vector<int>&& v)  // sink prend possession de ce que possède l’argument
    {
        // généralement il pourrait y avoir des accès const à v ici
        store_somewhere(std::move(v));
        // généralement plus d’utilisation de v ici ; il est déplacé
    }

Notez que `std::move(v)` rend possible que `store_somewhere()` laisse `v` dans un état déplacé.  
[Cela pourrait être dangereux](007-class.md#rc-move-semantic) @TODO‑LINK.

##### Exception

Les types propriétaire uniques qui ne sont que *move‑only* et peu coûteux à déplacer, comme `unique_ptr`, peuvent également être passés par valeur, ce qui est plus simple à écrire et donne le même effet. Passer par valeur génère un déplacement supplémentaire (bon marché), mais privilégiez d’abord la simplicité et la clarté.

Par exemple :

    template<class T>
    void sink(std::unique_ptr<T> p)
    {
        // utiliser p … éventuellement std::move(p) plus loin
    }   // p est détruit

##### Exception

Si le paramètre « will‑move‑from » est un `shared_ptr`, suivez [R.34](009-resource.md#rr-sharedptrparam-owner) et passez le `shared_ptr` par valeur.

##### Application

* Signaler tous les paramètres `X&&` (où `X` n’est pas un nom de paramètre de modèle) dont le corps de fonction les utilise sans `std::move`.  
* Signaler l’accès à des objets déplacés.  
* Ne pas déplacer conditionnellement des objets.

### <a name="rf-forward"></a>F.19 : Pour les paramètres « forward », passer par `TP&&` et n’utiliser que `std::forward` sur le paramètre

##### Raison

Si l’objet doit être transmis à d’autres code et n’est pas utilisé directement par cette fonction, on veut que la fonction soit indifférente à la const‑ness et à la nature r‑value/l‑value de l’argument.

Dans ce cas‑exact, on déclare le paramètre `TP&&` où `TP` est un paramètre de modèle ; cela *ignore* et *préserve* la const‑ness et la nature r‑value. Ainsi tout code qui utilise un `TP&&` déclare implicitement qu’il ne se préoccupe pas de la const‑ness / r‑value de la variable (parce qu’il l’ignore), mais qu’il a l’intention de la transmettre à du code qui, lui, s’en préoccupe (parce qu’elle est préservée). Quand il est utilisé comme paramètre, `TP&&` est sûr car tout objet temporaire passé par l’appelant vit pendant la durée de l’appel de fonction. Un paramètre de type `TP&&` doit essentiellement toujours être transmis en aval via `std::forward` dans le corps de la fonction.

##### Exemple

Typiquement, on transmet le paramètre entier (ou le pack de paramètres, via `...`) exactement une fois sur chaque chemin de contrôle statique :

    template<class F, class... Args>
    inline decltype(auto) invoke(F&& f, Args&&... args)
    {
        return forward<F>(f)(forward<Args>(args)...);
    }

##### Exemple

Parfois, on transmet un paramètre composite morceau par morceau, chaque sous‑objet une fois sur chaque chemin de contrôle :

    template<class PairLike>
    inline auto test(PairLike&& pairlike)
    {
        // …
        f1(some, args, and, forward<PairLike>(pairlike).first);           // transmettre .first
        f2(and, forward<PairLike>(pairlike).second, in, another, call); // transmettre .second
    }

##### Application

Signaler une fonction qui prend un paramètre `TP&&` (où `TP` est un nom de paramètre de modèle) et qui fait autre chose que le transmettre exactement une fois via `std::forward` sur chaque chemin statique, ou le transmet plusieurs fois mais avec un membre de données différent exactement une fois par chemin.

### <a name="rf-out"></a>F.20 : Pour les valeurs de sortie « out », privilégier les valeurs de retour aux paramètres de sortie

##### Raison

Une valeur de retour est auto‑documentée, tandis qu’un `&` peut signifier soit « in‑out », soit uniquement « out », et est sujet à mauvaise utilisation.

Cela inclut les gros objets comme les conteneurs standards qui utilisent des déplacements implicites pour les performances et pour éviter une gestion explicite de la mémoire.

Si vous avez plusieurs valeurs à retourner, [utilisez un tuple](006-functions.md#rf-out-multi) ou un type multi‑membre similaire.

##### Exemple

    // OK : retourner des pointeurs vers les éléments contenant la valeur x
    vector<const int*> find_all(const vector<int>&, int x);

    // Mauvais : placer des pointeurs vers les éléments contenant x dans un paramètre in‑out
    void find_all(const vector<int>&, vector<const int*>& out, int x);

##### Note

Une `struct` contenant de nombreux éléments (chacun peu coûteux à déplacer) peut être globalement coûteuse à déplacer.

##### Exceptions

* Pour les types non concrets, comme les types dans une hiérarchie d’héritage, retourner l’objet via `unique_ptr` ou `shared_ptr`.  
* Si un type est coûteux à déplacer (par ex. `array<BigTrivial>`), envisager de l’allouer sur le tas et de retourner un handle (`unique_ptr`), ou le passer par référence non‑`const` à remplir (à utiliser comme paramètre out).  
* Pour réutiliser un objet qui porte une capacité (par ex. `std::string`, `std::vector`) à travers plusieurs appels dans une boucle interne : [le traiter comme paramètre in/out et le passer par référence](006-functions.md#rf-out-multi).

##### Exemple

Supposons que `Matrix` possède des opérations de déplacement (possiblement en gardant ses éléments dans un `std::vector`) :

    Matrix operator+(const Matrix& a, const Matrix& b)
    {
        Matrix res;
        // … remplir res avec la somme …
        return res;
    }

    Matrix x = m1 + m2;  // constructeur de déplacement

    y = m3 + m3;         // assignation de déplacement

##### Note

L’optimisation du retour de valeur (RVO) ne gère pas le cas d’assignation, mais l’assignation de déplacement le fait.

##### Exemple

    struct Package {      // cas exceptionnel : objet coûteux à déplacer
        char header[16];
        char load[2024 - 16];
    };

    Package fill();       // Mauvais : grosse valeur de retour
    void fill(Package&); // OK

    int val();            // OK
    void val(int&);      // Mauvais : est‑ce que val lit son argument ?

##### Application

* Signaler les paramètres de référence non‑`const` qui ne sont pas lus avant d’être écrits et dont le type pourrait être renvoyé facilement ; ils devraient devenir des valeurs de retour.

### <a name="rf-out-multi"></a>F.21 : Pour renvoyer plusieurs valeurs « out », privilégier le retour d’une structure

##### Raison

Une valeur de retour est auto‑documentée comme « valeur de sortie uniquement ».  
C++ dispose de retours multiples via des types du type tuple (`struct`, `array`, `tuple`, …), éventuellement avec les liaisons structurées (C++17) côté appelant. Privilégiez l’utilisation d’un `struct` nommé si possible. Sinon, un `tuple` est utile dans les modèles variadiques.

##### Exemple

    // MAUVAIS : paramètre uniquement sortie documenté dans un commentaire
    int f(const string& input, /*output only*/ string& output_data)
    {
        // …
        output_data = something();
        return status;
    }

    // BON : auto‑documenté
    struct f_result { int status; string data; };

    f_result f(const string& input)
    {
        // …
        return {status, something()};
    }

La bibliothèque standard C++98 utilisait ce style en retournant `pair` dans certaines fonctions. Par exemple, avec un `set<string> my_set` :

    // C++98
    pair<set::iterator, bool> result = my_set.insert("Hello");
    if (result.second)
        do_something_with(result.first);    // contournement

Avec C++17, on peut utiliser les liaisons structurées :

    if (auto [ iter, success ] = my_set.insert("Hello"); success)
        do_something_with(iter);

Un `struct` avec des noms significatifs est plus commun en C++ moderne. Voir, par exemple, `ranges::min_max_result`, `from_chars_result`, etc.

##### Exception

Parfois, nous devons passer un objet à une fonction pour manipuler son état. Dans ces cas, passer l’objet par référence `T&` (voir [F.17](006-functions.md#rf-inout)) est généralement la bonne technique. Renvoyer explicitement un paramètre in‑out comme valeur de retour n’est souvent pas nécessaire. Exemple :

    istream& operator>>(istream& in, string& s);    // similaire à std::operator>>()

    for (string s; in >> s; ) {
        // faire quelque chose avec la ligne
    }

Ici, `s` et `in` sont des paramètres in‑out. Nous passons `in` par référence (non‑`const`) pour pouvoir manipuler son état, et `s` pour éviter des allocations répétées. En réutilisant `s` (passé par référence), nous n’allouons de la mémoire que lorsque c’est nécessaire. Cette technique est parfois appelée le *modèle de sortie allouée par le client* et est très utile pour des types comme `string` et `vector` qui font des allocations sur le tas.

En comparaison, si nous renvoyions toutes les valeurs, nous écririons quelque chose comme :

    struct get_string_result { istream& in; string s; };

    get_string_result get_string(istream& in)  // non recommandé
    {
        string s;
        in >> s;
        return { in, move(s) };
    }

    for (auto [in, s] = get_string(cin); in; s = get_string(in).s) {
        // faire quelque chose avec string
    }

Nous considérons cela nettement moins élégant et nettement moins performant.

Pour une lecture stricte de cette règle (F.21), l’exception n’est pas vraiment une exception car elle repose sur des paramètres in‑out, alors que la règle parle de paramètres out purs. Nous privilégions néanmoins la clarté.

##### Note

Dans la plupart des cas, il est utile de retourner un type défini par l’utilisateur. Par exemple :

    struct Distance {
        int value;
        int unit = 1;   // 1 signifie mètres
    };

    Distance d1 = measure(obj1);        // accéder à d1.value et d1.unit
    auto d2 = measure(obj2);            // accéder à d2.value et d2.unit
    auto [value, unit] = measure(obj3); // accès aux membres ; redondant pour ceux qui connaissent measure()
    auto [x, y] = measure(obj4);        // à éviter : source de confusion

Les `pair` et `tuple` génériques devraient être réservés aux cas où les membres représentent des entités indépendantes plutôt qu’une abstraction.

Une autre option consiste à utiliser `optional<T>` ou `expected<T, error_code>` plutôt que `pair` ou `tuple`. Lorsqu’ils sont employés correctement, ces types transmettent davantage d’informations sur la signification des membres que ne le ferait `pair<T, bool>` ou `pair<T, error_code>`.

##### Note

Lorsque l’objet à retourner est initialisé à partir de variables locales coûteuses à copier, un `move` explicite peut être utile pour éviter la copie :

    pair<LargeObject, LargeObject> f(const string& input)
    {
        LargeObject large1 = g(input);
        LargeObject large2 = h(input);
        // …
        return { move(large1), move(large2) }; // pas de copies
    }

ou bien :

    pair<LargeObject, LargeObject> f(const string& input)
    {
        // …
        return { g(input), h(input) }; // pas de copies, pas de moves
    }

Notez que cela diffère du anti‑pattern `return move(...)` décrit dans [ES.56](010-expr.md#res-move).

##### Application

* Les paramètres de sortie doivent être remplacés par des valeurs de retour. Un paramètre de sortie est celui que la fonction écrit, qui invoque une fonction membre non‑`const`, ou qui le passe à une autre fonction comme non‑`const`.  
* Les types de retour `pair` ou `tuple` doivent être remplacés par un `struct` quand c’est possible. Dans les modèles variadiques, le `tuple` est souvent inévitable.

### <a name="rf-ptr-ref"></a>F.60 : Préférer `T*` à `T&` lorsqu’une option « pas d’argument » est valide

##### Raison

Un pointeur (`T*`) peut être `nullptr` alors qu’une référence (`T&`) ne peut pas l’être ; il n’existe pas de « référence nulle » valable.  
Parfois, disposer d’un `nullptr` comme alternative pour indiquer « pas d’objet » est utile ; sinon, la référence est plus simple à écrire et peut produire un code meilleur.

##### Exemple

    string zstring_to_string(zstring p) // zstring == char* ; chaîne de style C
    {
        if (!p) return string{};    // p peut être nullptr ; n’oubliez pas le test
        return string{p};
    }

    void print(const vector<int>& r)
    {
        // r désigne un vector<int> ; pas de test nécessaire
    }

##### Note

Il est possible, mais non valide en C++, de construire une référence qui serait essentiellement un `nullptr` (ex. : `T* p = nullptr; T& r = *p;`). Cette erreur est très rare.

##### Note

Si vous préférez la notation pointeur (`->` et/ou `*` vs `.`), `not_null<T*>` fournit la même garantie qu’une référence `T&`.

##### Application

* Signaler ??? (à préciser)

### <a name="rf-ptr"></a>F.22 : Utiliser `T*` ou `owner<T*>` pour désigner un seul objet

##### Raison

Lisibilité : cela rend le sens d’un pointeur brut clair.  
Permet un soutien important des outils.

##### Note

Dans le code C et C++ traditionnel, le pointeur brut `T*` est employé à de multiples fins faibles :

* Identifier un (seul) objet (non supprimé par cette fonction)  
* Pointer vers un objet alloué sur le tas (et le supprimer plus tard)  
* Contenir le `nullptr`  
* Identifier une chaîne de style C (tableau de caractères nul‑terminé)  
* Identifier un tableau dont la longueur est spécifiée séparément  
* Identifier une position dans un tableau

Cette multiprise rend difficile la compréhension du code et complique les vérifications et le soutien d’outils.

##### Exemple

    void use(int* p, int n, char* s, int* q)
    {
        p[n - 1] = 666; // Mauvais : on ne sait pas si p pointe sur n éléments ;
                        // supposez que ce n’est pas le cas ou utilisez span<int>
        cout << s;      // Mauvais : on ne sait pas si s pointe sur un tableau de caractères nul‑terminé ;
                        // supposez que ce n’est pas le cas ou utilisez zstring
        delete q;       // Mauvais : on ne sait pas si *q a été alloué sur le tas ;
                        // supposez que ce n’est pas le cas ou utilisez owner
    }

Mieux :

    void use2(span<int> p, zstring s, owner<int*> q)
    {
        p[p.size() - 1] = 666; // OK, une erreur de plage peut être détectée
        cout << s; // OK
        delete q;  // OK
    }

##### Note

`owner<T*>` représente la propriété, `zstring` désigne une chaîne de style C.

**Également** : supposez qu’un `T*` obtenu à partir d’un smart‑pointer (`unique_ptr<T>`) pointe sur un seul élément.

**Voir aussi** : [Bibliothèque de support](#gsl-guidelines-support-library)  
**Voir aussi** : [Ne pas passer de tableau comme pointeur unique](005-interfaces.md#ri-array)

##### Application

* (simple) ((Bounds)) Signaler toute opération arithmétique sur une expression de type pointeur qui produit une nouvelle valeur de type pointeur.

### <a name="rf-nullptr"></a>F.23 : Utiliser un `not_null<T>` pour indiquer que « null » n’est pas une valeur valide

##### Raison

Clarté. Un paramètre `not_null<T>` indique clairement que l’appelant est responsable de tout contrôle `nullptr` qui pourrait être nécessaire. De même, une valeur de retour `not_null<T>` indique que l’appelant n’a pas besoin de vérifier `nullptr`.

##### Exemple

`not_null<T*>` rend évident pour le lecteur (humain ou machine) qu’un test `nullptr` n’est pas nécessaire avant la déréférence. De plus, lors du débogage, `owner<T*>` et `not_null<T>` peuvent être instrumentés pour vérifier la correction.

Considérez :

    int length(Record* p);

Lorsque j’appelle `length(p)`, dois‑je d’abord vérifier que `p` n’est pas `nullptr` ?  
Le corps de `length()` doit‑il vérifier que `p` n’est pas `nullptr` ?

    // c’est au caller de s’assurer que p != nullptr
    int length(not_null<Record*> p);

    // l’implémenteur de length() doit supposer que p == nullptr est possible
    int length(Record* p);

##### Note

Un `not_null<T*>` est supposé ne jamais être `nullptr`; un `T*` peut l’être ; les deux peuvent être représentés en mémoire comme un `T*` (aucune surcharge d’exécution n’est impliquée).

##### Note

`not_null` ne s’applique pas uniquement aux pointeurs natifs. Il fonctionne également avec `unique_ptr`, `shared_ptr` et d’autres types ressemblant à des pointeurs.

##### Application

* (simple) Avertir si un pointeur brut est déréférencé sans avoir été testé contre `nullptr` (ou équivalent) dans une fonction, suggérer de le déclarer `not_null`.  
* (simple) Erreur si un pointeur brut est parfois déréférencé après un test `nullptr` et parfois non dans la même fonction.  
* (simple) Avertir si un pointeur `not_null` est testé contre `nullptr` dans une fonction.

### <a name="rf-range"></a>F.24 : Utiliser un `span<T>` ou un `span_p<T>` pour désigner une séquence demi‑ouverte

##### Raison

Les plages informelles/non explicites sont une source fréquente d’erreurs.

##### Exemple

    X* find(span<X> r, const X& v);    // trouver v dans r

    vector<X> vec;
    // …
    auto p = find({vec.begin(), vec.end()}, X{});  // trouver X{} dans vec

##### Note

Les plages sont extrêmement courantes en C++. Typiquement, elles sont implicites et leur utilisation correcte est très difficile à garantir. En particulier, pour une paire d’arguments `(p, n)` désignant un tableau `[p:p+n)`, il est généralement impossible de savoir s’il y a réellement `n` éléments à accéder après `*p`. `span<T>` et `span_p<T>` sont de simples classes auxiliaires désignant respectivement une plage `[p:q)` et une plage commençant à `p` et se terminant à la première élément qui satisfait un prédicat.

##### Exemple

Un `span` représente une plage d’éléments, mais comment manipuler les éléments de cette plage ?

    void f(span<int> s)
    {
        // traversée de plage (garantie correcte)
        for (int x : s) cout << x << '\n';

        // traversée style C (potentiellement vérifiée)
        for (gsl::index i = 0; i < s.size(); ++i) cout << s[i] << '\n';

        // accès aléatoire (potentiellement vérifié)
        s[7] = 9;

        // extraction de pointeurs (potentiellement vérifiée)
        std::sort(&s[0], &s[s.size() / 2]);
    }

##### Note

Un objet `span<T>` ne possède pas les éléments et est tellement petit qu’il peut être passé par valeur.

Passer un objet `span` comme argument est aussi efficace que de passer deux pointeurs ou un pointeur et un entier de comptage.

**Voir aussi** : [Bibliothèque de support](#gsl-guidelines-support-library)

##### Application

(Complexe) Signaler les accès à des paramètres pointeur qui sont bornés par d’autres paramètres de type entier et suggérer l’usage de `span`.

### <a name="rf-zstring"></a>F.25 : Utiliser un `zstring` ou un `not_null<zstring>` pour désigner une chaîne de style C

##### Raison

Les chaînes de style C sont omniprésentes. Elles sont définies par convention : tableaux de caractères terminés par zéro.  
Nous devons distinguer les chaînes de style C d’un pointeur vers un caractère unique ou d’un ancien pointeur vers un tableau de caractères.

Si vous n’avez pas besoin de la terminaison nulle, utilisez `string_view`.

##### Exemple

    int length(const char* p);

Lorsque j’appelle `length(s)`, dois‑je d’abord vérifier que `s` n’est pas `nullptr` ?  
Le corps de `length()` doit‑il vérifier que `p` n’est pas `nullptr` ?

    // l’implémenteur de length() doit supposer que p == nullptr est possible
    int length(zstring p);

    // c’est au caller de s’assurer que p != nullptr
    int length(not_null<zstring> p);

##### Note

`zstring` ne représente pas la propriété.

**Voir aussi** : [Bibliothèque de support](#gsl-guidelines-support-library)

### <a name="rf-unique_ptr"></a>F.26 : Utiliser `unique_ptr<T>` pour transférer la propriété lorsqu’un pointeur est nécessaire

##### Raison

Utiliser `unique_ptr` est la façon la plus économique de passer un pointeur en toute sécurité.

**Voir aussi** : [C.50](007-class.md#rc-factory) concernant le moment où il faut retourner un `shared_ptr` depuis une usine.

##### Exemple

    unique_ptr<Shape> get_shape(istream& is)  // fabriquer une forme à partir d’un flux d’entrée
    {
        auto kind = read_header(is); // lire l’en‑tête et identifier la forme suivante
        switch (kind) {
        case kCircle:
            return make_unique<Circle>(is);
        case kTriangle:
            return make_unique<Triangle>(is);
        // …
        }
    }

##### Note

Vous devez passer un pointeur plutôt qu’un objet si ce que vous transférez est un objet d’une hiérarchie de classes devant être utilisé via une interface (classe de base).

##### Application

(Simple) Signaler si une fonction retourne un pointeur brut alloué localement. Suggérer d’utiliser `unique_ptr` ou `shared_ptr`.

### <a name="rf-shared_ptr"></a>F.27 : Utiliser `shared_ptr<T>` pour partager la propriété

##### Raison

Utiliser `std::shared_ptr` est la façon standard de représenter la propriété partagée : le dernier propriétaire supprime l’objet.

##### Exemple

    {
        shared_ptr<const Image> im { read_image(somewhere) };

        std::thread t0 {shade, args0, top_left, im};
        std::thread t1 {shade, args1, top_right, im};
        std::thread t2 {shade, args2, bottom_left, im};
        std::thread t3 {shade, args3, bottom_right, im};

        // détacher les threads nécessite des précautions (ex. joindre avant la fin du main),
        // mais même si nous détachions les quatre threads ici …
    }
    // … shared_ptr garantit qu’éventuellement le dernier thread à finir
    //     supprime l’image en toute sécurité

##### Note

Privilégiez `unique_ptr` à `shared_ptr` lorsqu’il n’y a jamais plus d’un propriétaire à la fois. `shared_ptr` implique un coût (opérations atomiques sur le compteur de références).

##### Alternative

Faire qu’un seul objet possède l’objet partagé (ex. un objet scoped) et le détruire (de préférence implicitement) lorsque tous les utilisateurs ont fini.

##### Application

(Non applicable) Ce motif est trop complexe pour être détecté de façon fiable.

### <a name="rf-return-ptr"></a>F.42 : Retourner un `T*` pour indiquer une position (seulement)

##### Raison

C’est exactement ce pour quoi les pointeurs sont faits. Retourner un `T*` pour transférer la propriété est un mauvais usage.

##### Exemple

    Node* find(Node* t, const string& s)  // rechercher s dans un arbre binaire de Nodes
    {
        if (!t || t->name == s) return t;
        if ((auto p = find(t->left, s))) return p;
        if ((auto p = find(t->right, s))) return p;
        return nullptr;
    }

Si ce n’est pas `nullptr`, le pointeur retourné indique un `Node` contenant `s`.  
Cela n’implique pas de transfert de propriété de l’objet pointé au caller.

##### Note

Les positions peuvent également être transférées par itérateurs, indices ou références.  
Une référence est souvent une alternative supérieure à un pointeur [si aucune `nullptr` n’est nécessaire](006-functions.md#rf-ptr-ref) ou [si l’objet référencé ne doit pas changer](014-const.md).

##### Note

Ne retournez jamais un pointeur vers quelque chose qui n’est pas dans la portée du caller ; voir [F.43](006-functions.md#rf-dangle).

**Voir aussi** : [discussion sur la prévention des pointeurs pendants](#???) @TODO‑LINK

##### Application

* Signaler `delete`, `std::free()` etc. appliqués à un pointeur brut `T*`. Seuls les propriétaires doivent être supprimés.  
* Signaler `new`, `malloc()` etc. assignés à un pointeur brut `T*`. Seuls les propriétaires doivent être responsables de la suppression.

### <a name="rf-dangle"></a>F.43 : Ne jamais (directement ou indirectement) retourner un pointeur ou une référence vers un objet local

##### Raison

Éviter les plantages et la corruption de données qui peuvent résulter de l’utilisation d’un tel pointeur pendants.

##### Exemple, mauvais

Après le retour d’une fonction, ses objets locaux n’existent plus :

    int* f()
    {
        int fx = 9;
        return &fx;  // MAUVAIS
    }

    void g(int* p)   // paraît inoffensif
    {
        int gx;
        cout << "*p == " << *p << '\n';
        *p = 999;
        cout << "gx == " << gx << '\n';
    }

    void h()
    {
        int* p = f();
        int z = *p;  // lecture d’une trame de pile abandonnée (mauvais)
        g(p);        // passer le pointeur d’une trame abandonnée à une fonction (mauvais)
    }

Sur une implémentation populaire, la sortie est :

    *p == 999
    gx == 999

On s’attend à cela parce que l’appel à `g()` réutilise l’espace de pile abandonné par `f()` ; `*p` se réfère alors à l’espace occupé désormais par `gx`.

* Imaginez ce qui arriverait si `fx` et `gx` étaient de types différents.  
* Imaginez ce qui arriverait si `fx` ou `gx` était un type avec une invariant.  
* Imaginez ce qui arriverait si ce pointeur pendants était transmis à un plus grand nombre de fonctions.  
* Imaginez ce qu’un attaquant pourrait faire avec ce pointeur pendants.

Heureusement, la plupart des compilateurs modernes détectent et avertissent contre ce cas simple.

##### Note

Cela s’applique également aux références :

    int& f()
    {
        int x = 7;
        // …
        return x;  // Mauvais : retourne une référence vers un objet qui va être détruit
    }

##### Note

Cela ne concerne que les variables locales non‑`static`. Toutes les variables `static` sont, comme leur nom l’indique, allouées statiquement ; leurs pointeurs ne peuvent donc pas devenir pendants.

##### Exemple, mauvais

Tous les exemples de fuite d’un pointeur vers une variable locale ne sont pas toujours aussi évidents :

    int* glob;       // les variables globales sont déjà mauvaises à bien des égards

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

Ici, on lit l’emplacement abandonné par l’appel à `f`.  
Le pointeur stocké dans `glob` pourrait être utilisé bien plus tard et causer des problèmes imprévisibles.

##### Note

L’adresse d’une variable locale peut être « retournée »/ « fuyante » via un `return`, un paramètre de sortie `T&`, comme membre d’un objet retourné, comme élément d’un tableau retourné, etc.

##### Note

Des exemples similaires peuvent être construits en « fuyant » un pointeur d’une portée interne vers une portée externe ; ces exemples sont traités de la même façon que les fuites de pointeurs hors d’une fonction.

Une variante légèrement différente du problème consiste à placer des pointeurs dans un conteneur qui survit aux objets pointés.

**Voir aussi** : une autre façon d’obtenir des pointeurs pendants est [l’invalidation de pointeur](#???) @TODO‑LINK. Cela peut être détecté / prévenu avec des techniques similaires.

##### Application

* Les compilateurs attrapent généralement le retour d’une référence vers des locaux et, dans de nombreux cas, le retour de pointeurs vers des locaux.  
* L’analyse statique peut détecter de nombreux modèles courants d’utilisation de pointeurs indiquant des positions (éliminant ainsi les pointeurs pendants).

### <a name="rf-return-ref"></a>F.44 : Retourner un `T&` quand la copie est indésirable et que « ne rien retourner » n’est pas nécessaire

##### Raison

Le langage garantit qu’un `T&` fait référence à un objet, de sorte qu’il n’est pas nécessaire de tester `nullptr`.

**Voir aussi** : Le retour d’une référence ne doit pas impliquer un transfert de propriété : [discussion sur la prévention des pointeurs pendants](#???) @TODO‑LINK et [discussion sur la propriété](#???).

##### Exemple

    class Car
    {
        array<wheel, 4> w;
        // …
    public:
        wheel& get_wheel(int i) { Expects(i < w.size()); return w[i]; }
        // …
    };

    void use()
    {
        Car c;
        wheel& w0 = c.get_wheel(0); // w0 a la même durée de vie que c
    }

##### Application

Signaler les fonctions où aucune expression `return` ne pourrait produire `nullptr`.

### <a name="rf-return-ref-ref"></a>F.45 : Ne pas retourner un `T&&`

##### Raison

C’est demander à retourner une référence à un objet temporaire détruit. Un `&&` attire les temporaires.

##### Exemple

Une référence r‑value retournée sort de son scope à la fin de l’expression complète à laquelle elle est retournée :

    auto&& x = max(0, 1);   // OK, pour l’instant
    foo(x);                 // comportement indéfini

Ce type d’usage est une source fréquente de bugs, souvent signalés à tort comme un bug de compilateur. Un implémenteur de fonction doit éviter de piéger les utilisateurs de la sorte.

Le [profil de sécurité de durée de vie](022-profile.md#ss-lifetime) (une fois complètement implémenté) attrapera ces problèmes.

##### Exemple

Retourner une référence r‑value est acceptable quand la référence au temporaire est transmise « vers le bas » à un appelant ; alors le temporaire est garanti de survivre à l’appel de fonction (voir [F.18](006-functions.md#rf-consume) et [F.19](006-functions.md#rf-forward)).  
Ce n’est pas le cas lorsqu’on la renvoie « vers le haut » dans une portée appelante plus large.  
Pour les fonctions de passage qui transmettent les paramètres (par référence ordinaire ou par perfect‑forward) et qui souhaitent renvoyer des valeurs, utilisez la déduction de type `auto` (pas `auto&&`).

Supposons que `F` renvoie par valeur :

    template<class F>
    auto&& wrapper(F f)
    {
        log_call(typeid(f)); // ou autre instrumentation
        return f();          // MAUVAIS : retourne une référence à un temporaire
    }

Mieux :

    template<class F>
    auto wrapper(F f)
    {
        log_call(typeid(f)); // ou autre instrumentation
        return f();          // OK
    }

##### Exception

`std::move` et `std::forward` retournent bien `&&`, mais ce ne sont que des casts — utilisés uniquement dans des contextes d’expression où une référence à un objet temporaire est immédiatement transmise dans la même expression avant que le temporaire ne soit détruit. Nous ne connaissons pas d’autres bons exemples de retour de `&&`.

##### Application

Signaler tout usage de `&&` comme type de retour, sauf dans `std::move` et `std::forward`.

### <a name="rf-main"></a>F.46 : `int` est le type de retour de `main()`

##### Raison

C’est une règle du langage, mais elle est souvent violée par des « extensions de langage », d’où l’intérêt de la rappeler. Déclarer `main` (l’unique `main` d’un programme) comme `void` limite la portabilité.

##### Exemple

        void main() { /* … */ };  // mauvais, ce n’est pas du C++
        int main()
        {
            std::cout << "This is the way to do it\n";
        }

##### Note

Nous ne le mentionnons que parce que cette erreur persiste dans la communauté. Notez que malgré son type de retour non‑void, la fonction `main` n’a pas besoin d’une instruction `return` explicite.

##### Application

* Le compilateur doit le signaler.  
* Si le compilateur ne le fait pas, laissez les outils le signaler.

### <a name="rf-assignment-op"></a>F.47 : Retourner `T&` depuis les opérateurs d’affectation

##### Raison

La convention pour les surcharges d’opérateurs (en particulier sur les types concrets) est que `operator=(const T&)` effectue l’affectation puis retourne (non‑`const`) `*this`. Cela assure la cohérence avec les types de la bibliothèque standard et suit le principe « faire comme les entiers ».

##### Note

Historiquement, il était recommandé que l’opérateur d’affectation retourne `const T&` afin d’éviter le code de forme `(a = b) = c` ; ce code n’est pas assez fréquent pour justifier une rupture de cohérence avec les types standards.

##### Exemple

    class Foo
    {
     public:
        …
        Foo& operator=(const Foo& rhs)
        {
          // copier les membres.
          …
          return *this;
        }
    };

##### Application

Doit être appliquée par les outils en vérifiant le type de retour (et la valeur de retour) de tout opérateur d’affectation.

### <a name="rf-return-move-local"></a>F.48 : Ne pas `return std::move(local)`

##### Raison

Retourner une variable locale implique déjà un déplacement implicite. Un `std::move` explicite est toujours une pessimisation : il empêche la Return Value Optimization (RVO), qui peut éliminer complètement le déplacement.

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
      // Named RVO : élimination du déplacement au mieux, construction de déplacement au pire
      return result;
    }

##### Application

Doit être appliquée par les outils en vérifiant l’expression de retour.

### <a name="rf-return-const"></a>F.49 : Ne pas retourner `const T`

##### Raison

Il n’est plus recommandé de retourner une valeur `const`. Ce conseil ancien est désormais obsolète : il n’apporte aucune valeur et interfère avec les mouvements.

##### Exemple

    const vector<int> fct();    // mauvais : le `const` est plus pénalisant qu’utile

    void g(vector<int>& vx)
    {
        // …
        fct() = vx;   // empêché par le `const`
        // …
        vx = fct(); // copie coûteuse : les mouvements sont supprimés par le `const`
        // …
    }

L’argument d’ajouter `const` à une valeur retournée était d’empêcher (très rare) l’accès accidentel à un temporaire. L’argument contre est que cela empêche (très fréquent) l’utilisation des mouvements.

**Voir aussi** : [F.20, l’item général sur les valeurs de sortie « out »](006-functions.md#rf-out)

##### Application

* Signaler le retour d’une valeur `const`. Correction : supprimer le `const` pour retourner une valeur non‑`const`.

### <a name="rf-capture-vs-overload"></a>F.50 : Utiliser une lambda lorsqu’une fonction ne convient pas (pour capturer des variables locales ou écrire une fonction locale)

##### Raison

Les fonctions ne peuvent pas capturer des variables locales ni être définies dans une portée locale ; si vous avez besoin de ces choses, préférez une lambda, ou bien un objet fonctionnel écrit à la main si la lambda n’est pas suffisante. D’autre part, les lambdas et objets fonctionnels ne supportent pas la surcharge ; si vous avez besoin de surcharger, choisissez une fonction (les détours pour rendre les lambdas surchargeables sont complexes). Si les deux conviennent, privilégiez la fonction ; employez l’outil le plus simple nécessaire.

##### Exemple

    // écrire une fonction qui ne doit prendre qu’un int ou une string
    // – la surcharge est naturelle
    void f(int);
    void f(const string&);

    // écrire un objet fonctionnel qui doit capturer un état local et apparaître
    // au niveau d’une instruction ou d’une expression – une lambda est naturelle
    vector<work> v = lots_of_work();
    for (int tasknum = 0; tasknum < max; ++tasknum) {
        pool.run([=, &v] {
            /*
            …
            … traiter 1/max‑ième de v, le morceau tasknum‑ième
            …
            */
        });
    }
    pool.join();

##### Exception

Les lambdas génériques offrent un moyen concis d’écrire des modèles de fonction et peuvent être utiles même lorsqu’un modèle de fonction ordinaire ferait le même travail avec un peu plus de syntaxe. Cet avantage disparaîtra probablement à l’avenir lorsque toutes les fonctions pourront prendre des paramètres de concept.

##### Application

* Avertir sur l’utilisation d’une lambda non générique nommée (ex. : `auto x = [](int i){ … };`) qui ne capture rien et apparaît au niveau global. Écrire une fonction ordinaire à la place.

### <a name="rf-default-args"></a>F.51 : Lorsqu’un choix est possible, privilégier les arguments par défaut aux surcharges

##### Raison

Les arguments par défaut offrent simplement des interfaces alternatives à une seule implémentation.  
Il n’y a aucune garantie que l’ensemble de fonctions surchargées implémente la même sémantique. L’usage d’arguments par défaut évite la duplication de code.

##### Note

Il y a un choix entre argument par défaut et surcharge lorsque les alternatives sont des ensembles d’arguments du même type. Par exemple :

    void print(const string& s, format f = {});

au lieu de :

    void print(const string& s);  // utilise le format par défaut
    void print(const string& s, format f);

Il n’y a pas de choix lorsque l’ensemble de fonctions effectue une opération sémantiquement équivalente sur des types différents. Par exemple :

    void print(const char&);
    void print(int);
    void print(zstring);

##### Voir aussi

[Arguments par défaut pour les fonctions virtuelles](007-class.md#rh-virtual-default-arg) @TODO‑LINK

##### Application

* Avertir sur un jeu de surcharges partageant un préfixe commun de paramètres (ex. `f(int)`, `f(int, const string&)`, `f(int, const string&, double)`). (Note : re‑évaluer si cela devient trop bruyant en pratique.)

### <a name="rf-reference-capture"></a>F.52 : Préférer la capture par référence dans les lambdas utilisées localement, y compris lorsqu’elles sont passées à des algorithmes

##### Raison

Pour l’efficacité et la correction, vous devez presque toujours capturer par référence lorsque vous utilisez la lambda localement. Cela inclut les algorithmes parallèles locaux qui se rejoignent avant de retourner.

##### Discussion

L’aspect d’efficacité est que la plupart des types sont moins coûteux à passer par référence qu’à copier.

L’aspect de correction est que de nombreux appels veulent produire des effets de bord sur l’objet original sur le site de l’appel (voir l’exemple ci‑dessous). Capturer par valeur empêche cela.

##### Note

Il n’existe malheureusement pas de façon simple de capturer par référence `const` afin d’obtenir l’efficacité d’un appel local tout en empêchant les effets de bord.

##### Exemple

Ici, un grand objet (un message réseau) est transmis à un algorithme itératif, et il n’est ni efficace ni correct de copier le message (qui peut ne pas être copiable) :

    std::for_each(begin(sockets), end(sockets), [&message](auto& socket)
    {
        socket.send(message);
    });

##### Exemple

Ceci est une simple chaîne d’étapes parallèles en trois étapes. Chaque objet `stage` encapsule un thread de travail et une file d’attente, possède une fonction `process` pour enfiler du travail, et son destructeur bloque automatiquement jusqu’à ce que la file soit vide avant de terminer le thread.

    void send_packets(buffers& bufs)
    {
        stage encryptor([](buffer& b) { encrypt(b); });
        stage compressor([&](buffer& b) { compress(b); encryptor.process(b); });
        stage decorator([&](buffer& b) { decorate(b); compressor.process(b); });
        for (auto& b : bufs) { decorator.process(b); }
    }  // bloque automatiquement en attendant que le pipeline se termine

##### Application

Signaler une lambda qui capture par référence mais qui est utilisée autrement que localement dans la portée de la fonction ou qui est passée à une fonction par référence. (Note : Cette règle est une approximation, mais elle signale le passage par pointeur, qui est plus susceptible d’être stocké par le callee, d’écrire sur une zone du tas accessible via un paramètre, de retourner la lambda, etc. Les règles de durée de vie fourniront également des règles générales qui signalent les pointeurs et références échappés, y compris via les lambdas.)

### <a name="rf-value-capture"></a>F.53 : Éviter la capture par référence dans les lambdas qui seront utilisées de façon non locale, y compris retournées, stockées sur le tas ou passées à un autre thread

##### Raison

Les pointeurs et références vers des variables locales ne doivent pas survivre à leur portée. Les lambdas qui capturent par référence constituent un autre moyen de stocker une référence vers un objet local, et ne doivent pas le faire si elles (ou une copie) survivent à la portée.

##### Exemple, mauvais

    int local = 42;

    // On veut une référence à local.
    // Notez qu’après la sortie du scope, local n’existe plus, donc
    // l’appel à process() sera indéfini !
    thread_pool.queue_work([&] { process(local); });

##### Exemple, bon

    int local = 42;
    // On veut une copie de local.
    // La copie sera toujours disponible pour l’appel.
    thread_pool.queue_work([=] { process(local); });

##### Note

Si un pointeur non‑local doit être capturé, envisagez d’utiliser `unique_ptr` ; cela gère à la fois la durée de vie et la synchronisation.

Si le pointeur `this` doit être capturé, envisagez la capture `[ *this ]`, qui crée une copie de l’ensemble de l’objet.

##### Application

* (simple) Avertir lorsque la liste de capture contient une référence à une variable déclarée localement.  
* (complexe) Signaler lorsque la liste de capture contient une référence à une variable locale **et** que la lambda est passée à un contexte non‑`const` et non‑local.

### <a name="rf-this-capture"></a>F.54 : Lors de l’écriture d’une lambda capturant `this` ou tout membre de classe, ne pas utiliser la capture par défaut `[=]`

##### Raison

C’est déroutant. Écrire `[=]` dans une méthode membre semble capturer par valeur, mais capture en réalité les membres de données par référence puisqu’il capture le pointeur invisible `this` par valeur. Si vous aviez réellement l’intention de le faire, écrivez `this` explicitement.

##### Exemple

    class My_class {
        int x = 0;
        // ...

        void f()
        {
            int i = 0;
            // ...

            auto lambda = [=] { use(i, x); };   // MAUVAIS : « semble » copie/value capture

            x = 42;
            lambda(); // appelle use(0, 42);
            x = 43;
            lambda(); // appelle use(0, 43);

            // ...

            auto lambda2 = [i, this] { use(i, x); }; // correct, le plus explicite et le moins déroutant

            // ...
        }
    };

##### Note

Si vous avez besoin de copier tous les membres de données de la classe, considérez `[*this]` de C++17.

##### Application

* Signaler toute lambda dont la liste de capture spécifie un capture‑default `[=]` et qui capture également `this` (explicitement ou via la capture par défaut et une utilisation de `this` dans le corps).

### <a name="f-varargs"></a>F.55 : Ne pas utiliser d’arguments `va_arg`

##### Raison

Lire depuis un `va_arg` suppose que le type correct a réellement été passé. Passer à des var‑args suppose que le type correct sera lu. C’est fragile parce que cela ne peut pas être garanti comme sûr par le langage ; on repose alors sur la discipline du programmeur.

##### Exemple

    int sum(...)
    {
        // …
        while (/*...*/)
            result += va_arg(list, int); // MAUVAIS, suppose que l’on passe des `int`
        // …
    }

    sum(3, 2); // OK
    sum(3.14159, 2.71828); // MAUVAIS, indéfini

    template<class ...Args>
    auto sum(Args... args) // BON, beaucoup plus flexible
    {
        return (... + args); // note : expression de pliage C++17
    }

    sum(3, 2); // OK : 5
    sum(3.14159, 2.71828); // OK : ≈ 5,85987

##### Alternatives

* Surcharge  
* Modèles variadiques  
* Arguments `variant`  
* `initializer_list` (homogène)

##### Note

Déclarer un paramètre `...` est parfois utile pour des techniques qui n’impliquent pas réellement le passage d’arguments, notamment pour déclarer des fonctions « prennent tout » afin d’invalider « tout le reste » dans un ensemble de surcharges ou d’exprimer un cas de capture dans une méta‑programmation de modèle.

##### Application

* Signaler l’utilisation de `va_list`, `va_start` ou `va_arg`.  
* Signaler le passage d’un argument à un paramètre var‑arg d’une fonction qui n’offre pas de surcharge pour un type plus spécifique à cet emplacement. Correction : Utiliser une fonction différente, ou `[[suppress("type")]]`.

### <a name="f-nesting"></a>F.56 : Éviter les imbrications de conditions inutiles

##### Raison

Des imbrications peu profondes facilitent la lecture du code. Elles clarifient aussi l’intention. Essayez de placer le code essentiel au niveau le plus externe, sauf si cela obscurcit l’intention.

##### Exemple

Utilisez une clause de garde pour traiter les cas exceptionnels et retourner tôt.

    // Mauvais : imbrication profonde
    void foo() {
        …
        if (x) {
            computeImportantThings(x);
        }
    }

    // Mauvais : else redondant
    void foo() {
        …
        if (!x) {
            return;
        }
        else {
            computeImportantThings(x);
        }
    }

    // Bon : retour précoce, pas d’else redondant
    void foo() {
        …
        if (!x)
            return;

        computeImportantThings(x);
    }

##### Exemple

    // Mauvais : imbrication de conditions inutile
    void foo() {
        …
        if (x) {
            if (y) {
                computeImportantThings(x);
            }
        }
    }

    // Bon : fusion des conditions + retour précoce
    void foo() {
        …
        if (!(x && y))
            return;

        computeImportantThings(x);
    }

##### Application

* Signaler un `else` redondant.  
* Signaler une fonction dont le corps se résume à une instruction conditionnelle englobant un bloc.

## <a name="ss-fct-def"></a>F.def : Définitions de fonctions

(Le contenu détaillé a déjà été traduit dans les sections précédentes.)

---  

*Note :* les références suivantes pointent vers des documents externes qui ne sont pas fournis ; elles sont marquées **@TODO‑LINK** afin d’indiquer qu’une vérification de leur cible est requise :

- [F.50](006-functions.md#rf-capture-vs-overload) – cible manquante.  
- [F.51](006-functions.md#rf-default-args) – cible manquante.  
- [C.lambdas: Function objects and lambdas](007-class.md#ss-lambdas) – cible externe.  
- [C.44](007-class.md#rc-default00) – cible externe.  
- [rc-move-semantic](007-class.md#rc-move-semantic) – cible externe.  
- [lifetime safety profile](022-profile.md#ss-lifetime) – cible externe.  
- [??] placeholders dans le texte (ex. `#??`) – cible manquante.  

Ces @TODO‑LINK signalent les liens à vérifier ou à ajouter dans le document original.