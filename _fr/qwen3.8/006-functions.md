# <a name="s-functions"></a>F : Fonctions

Une fonction spécifie une action ou un calcul qui amène le système d'un état cohérent à l'état suivant. C'est le bloc de construction fondamental des programmes.

Il doit être possible de nommer une fonction de manière significative, de spécifier les exigences de son argument et d'énoncer clairement la relation entre les arguments et le résultat. Une implémentation n'est pas une spécification. Essayez de réfléchir à ce qu'une fonction fait ainsi qu'à la manière dont elle le fait.
Les fonctions sont la partie la plus critique dans la plupart des interfaces, voir donc les règles des interfaces.

Résumé des règles des fonctions :

Règles de définition des fonctions :

* [F.1 : « Emballer » les opérations significatives en des fonctions soigneusement nommées](006-functions.md#rf-package)
* [F.2 : Une fonction doit effectuer une seule opération logique](006-functions.md#rf-logical)
* [F.3 : Garder les fonctions courtes et simples](006-functions.md#rf-single)
* [F.4 : Si une fonction doit potentiellement être évaluée au moment de la compilation, la déclarer `constexpr`](006-functions.md#rf-constexpr)
* [F.5 : Si une fonction est très petite et critique en termes de temps, la déclarer `inline`](006-functions.md#rf-inline)
* [F.6 : Si votre fonction ne doit pas lever d'exception, la déclarer `noexcept`](006-functions.md#rf-noexcept)
* [F.7 : Pour un usage général, prendre des arguments `T*` ou `T&` plutôt que des pointeurs intelligents](006-functions.md#rf-smart)
* [F.8 : Préférer les fonctions pures](006-functions.md#rf-pure)
* [F.9 : Les paramètres non utilisés doivent être sans nom](006-functions.md#rf-unused)
* [F.10 : Si une opération peut être réutilisée, lui donner un nom](006-functions.md#rf-name)
* [F.11 : Utiliser une lambda sans nom si vous avez besoin d'un simple objet fonctionnel à un seul endroit](006-functions.md#rf-lambda)

Règles d'expression du passage de paramètres :

* [F.15 : Préférer des moyens simples et conventionnels de transmission d'informations](006-functions.md#rf-conventional)
* [F.16 : Pour les paramètres « en lecture », passer les types à copie peu coûteuse par valeur et les autres par référence à `const`](006-functions.md#rf-in)
* [F.17 : Pour les paramètres « en lecture-écriture », passer par référence à non-`const`](006-functions.md#rf-inout)
* [F.18 : Pour les paramètres « seront déplacés », passer par `X&&` et `std::move` le paramètre](006-functions.md#rf-consume)
* [F.19 : Pour les paramètres « à transmettre », passer par `TP&&` et uniquement `std::forward` le paramètre](006-functions.md.md#rf-forward)
* [F.20 : Pour les valeurs de sortie « en écriture », préférer les valeurs retournées aux paramètres de sortie](006-functions.md#rf-out)
* [F.21 : Pour retourner plusieurs valeurs de sortie, préférer le retour d'une structure](006-functions.md#rf-out-multi)
* [F.60 : Préférer `T*` à `T&` lorsque « aucun argument » est une option valide](006-functions.md#rf-ptr-ref)

Règles sémantiques du passage de paramètres :

* [F.22 : Utiliser `T*` ou `owner<T*>` pour désigner un seul objet](006-functions.md#rf-ptr)
* [F.23 : Utiliser `not_null<T>` pour indiquer que « null » n'est pas une valeur valide](006-functions.md#rf-nullptr)
* [F.24 : Utiliser `span<T>` ou `span_p<T>` pour désigner une séquence semi-ouverte](006-functions.md#rf-range)
* [F.25 : Utiliser `zstring` ou `not_null<zstring>` pour désigner une chaîne au style C](006-functions.md#rf-zstring)
* [F.26 : Utiliser `unique_ptr<T>` pour transférer la propriété là où un pointeur est nécessaire](006-functions.md#rf-unique_ptr)
* [F.27 : Utiliser `shared_ptr<T>` pour partager la propriété](006-functions.md#rf-shared_ptr)

<a name="rf-value-return"></a>Règles sémantiques de retour de valeur :

* [F.42 : Retourner un `T*` pour indiquer une position (uniquement)](006-functions.md#rf-return-ptr)
* [F.43 : Ne jamais (directement ou indirectement) retourner un pointeur ou une référence à un objet local](006-functions.md#rf-dangle)
* [F.44 : Retourner un `T&` quand la copie est indésirable et que « ne retourner aucun objet » n'est pas nécessaire](006-functions.md#rf-return-ref)
* [F.45 : Ne pas retourner un `T&&`](006-functions.md#rf-return-ref-ref)
* [F.46 : `int` est le type de retour de `main()`](006-functions.md#rf-main)
* [F.47 : Retourner `T&` depuis les opérateurs d'affectation](006-functions.md#rf-assignment-op)
* [F.48 : Ne pas retourner `std::move(local)`](006-functions.md#rf-return-move-local)
* [F.49 : Ne pas retourner `const T`](006-functions.md#rf-return-const)

Autres règles des fonctions :

* [F.50 : Utiliser une lambda quand une fonction ne suffit pas (pour capturer des variables locales, ou pour écrire une fonction locale)](006-functions.md#rf-capture-vs-overload)
* [F.51 : Quand il y a un choix, préférer les arguments par défaut à la surcharge](006-functions.md#rf-default-args)
* [F.52 : Préférer la capture par référence dans les lambdas qui seront utilisées localement, y compris transmises à des algorithmes](006-functions.md#rf-reference-capture)
* [F.53 : Éviter la capture par référence dans les lambdas qui seront utilisées non localement, y compris retournées, stockées sur le tas, ou transmises à un autre thread](006-functions.md#rf-value-capture)
* [F.54 : Quand on écrit une lambda qui capture `this` ou un membre de données de classe, ne pas utiliser la capture par défaut `[=]`](006-functions.md#rf-this-capture)
* [F.55 : Ne pas utiliser les arguments `va_arg`](006-functions.md#f-varargs)
* [F.56 : Éviter l'imbrication inutile de conditions](006-functions.md#f-nesting)

Les fonctions présentent de fortes similarités avec les lambdas et les objets fonctionnels.

**Voir aussi** : [C.lambdas : Objets fonctionnels et lambdas](007-class.md#ss-lambdas)

## <a name="ss-fct-def"></a>F.def : Définitions de fonctions

Une définition de fonction est une déclaration de fonction qui spécifie également l'implémentation de la fonction, le corps de la fonction.

### <a name="rf-package"></a>F.1 : « Emballer » les opérations significatives en des fonctions soigneusement nommées

##### Justification

Factoriser du code commun rend le code plus lisible, plus susceptible d'être réutilisé et limite les erreurs dues à un code complexe.
Si quelque chose est une action bien spécifiée, la séparer du code environnant et lui donner un nom.

##### Exemple, à éviter

    void read_and_print(istream& is)    // lit et affiche un int
    {
        int x;
        if (is >> x)
            cout << "the int is " << x << '\n';
        else
            cerr << "no int on input\n";
    }

Presque tout est incorrect dans `read_and_print`.
Il lit, il écrit (vers un `ostream` fixe), il écrit des messages d'erreur (vers un `ostream` fixe), il ne gère que des `int`.
Il n'y a rien à réutiliser, des opérations logiquement séparées sont entremêlées et les variables locales sont en portée après la fin de leur usage logique.
Pour un exemple aussi petit, ça passe, mais si l'opération d'entrée, l'opération de sortie et la gestion des erreurs avaient été plus compliquées, le
tâcheris pouvait devenir difficile à comprendre.

##### Remarque

Si vous écrivez une lambda non triviale qui peut potentiellement être utilisée à plus d'un endroit, donnez-lui un nom en l'assignant à une variable (généralement non locale).

##### Exemple

    sort(a, b, [](T x, T y) { return x.rank() < y.rank() && x.value() < y.value(); });

Donner un nom à cette lambda découpe l'expression en ses parties logiques et fournit un indice puissant sur le sens de la lambda.

    auto lessT = [](T x, T y) { return x.rank() < y.rank() && x.value() < y.value(); };

    sort(a, b, lessT);

Le code le plus court n'est pas toujours le meilleur pour les performances ou la maintenabilité.

##### Exception

Les corps de boucles, y compris les lambdas utilisées comme corps de boucles, ont rarement besoin d'être nommées.
Cependant, les grands corps de boucles (par ex. des dizaines de lignes ou des dizaines de pages) peuvent poser problème.
La règle [Garder les fonctions courtes et simples](006-functions.md#rf-single) implique « Garder les corps de boucles courts. »
De même, les lambdas utilisées comme arguments de callback sont parfois non triviales, mais peu susceptibles d'être réutilisables.

##### Application

* Voir [Garder les fonctions courtes et simples](006-functions.md#rf-single)
* Signaler les lambdas identiques ou très similaires utilisées dans différents endroits.

### <a name="rf-logical"></a>F.2 : Une fonction doit effectuer une seule opération logique

##### Justification

Une fonction qui effectue une seule opération est plus simple à comprendre, à tester et à réutiliser.

##### Exemple

Considérez :

    void read_and_print()    // mauvais
    {
        int x;
        cin >> x;
        // vérifier les erreurs
        cout << x << "\n";
    }

C'est un monolithe lié à une entrée spécifique qui ne trouvera jamais un autre (différent) usage. À la place, découpez les fonctions en parties logiques appropriées et paramétrez :

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

Elles peuvent maintenant être combinées là où c'est nécessaire :

    void read_and_print()
    {
        auto x = read(cin);
        print(cout, x);
    }

S'il y avait un besoin, on pourrait further templatiser `read()` et `print()` sur le type de données, le mécanisme d'E/S, la réponse aux erreurs, etc. Exemple :

    auto read = [](auto& input, auto& value)    // meilleur
    {
        input >> value;
        // vérifier les erreurs
    };

    void print(auto& output, const auto& value)
    {
        output << value << "\n";
    }

##### Application

* Considérer avec suspicion les fonctions ayant plus d'un paramètre de sortie. Utiliser des valeurs retournées à la place, y compris `tuple` pour plusieurs valeurs de retour.
* Considérer avec suspicion les « grandes » fonctions qui ne tiennent pas sur un écran d'éditeur. Envisager de factoriser une telle fonction en sous-opérations plus petites et bien nommées.
* Considérer avec suspicion les fonctions ayant 7 paramètres ou plus.

### <a name="rf-single"></a>F.3 : Garder les fonctions courtes et simples

##### Justification

Les grandes fonctions sont difficiles à lire, plus susceptibles de contenir du code complexe et plus susceptibles d'avoir des variables dans des portées plus grandes que minimales.
Les fonctions avec des structures de contrôle complexes sont plus susceptibles d'être longues et plus susceptibles de cacher des erreurs logiques.

##### Exemple

Considérez :

    double simple_func(double val, int flag1, int flag2)
        // simple_func : prend une valeur et calcule la sortie ASIC attendue,
        // compte tenu des deux modes.
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
Comment savoir si toutes les alternatives possibles ont été correctement gérées ?
Oui, il viole aussi d'autres règles.

On peut refactoriser :

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
        // compte tenu des deux modes.
    {
        if (flag1 > 0)
            return func1_muon(val, flag2);
        if (flag1 == -1)
            // géré par func1_tau : flag1 = -flag1;
            return func1_tau(-val, flag1, flag2);
        return 0.;
    }

##### Remarque

« Ça ne tient pas sur un écran » est souvent une bonne définition pratique de « beaucoup trop grand. »
Les fonctions d'une à cinq lignes devraient être considérées comme normales.

##### Remarque

Découper les grandes fonctions en plus petites fonctions cohérentes et nommées.
Les petites fonctions simples peuvent facilement être inline-ées là où le coût d'un appel de fonction est significatif.

##### Application

* Signaler les fonctions qui ne « tiennent pas sur un écran. »
  Quelle est la taille d'un écran ? Essayez 60 lignes par 140 caractères ; c'est approximativement le maximum confortable pour une page de livre.
* Signaler les fonctions trop complexes. Quelle est la limite de complexité ?
  Vous pouvez utiliser la complexité cyclomatique. Essayez « plus de 10 chemins logiques. » Comptez un switch simple comme un chemin.

### <a name="rf-constexpr"></a>F.4 : Si une fonction doit potentiellement être évaluée au moment de la compilation, la déclarer `constexpr`

##### Justification

`constexpr` est nécessaire pour dire au compilateur d'autoriser l'évaluation au moment de la compilation.

##### Exemple

La factorielle (in)célèbre :

    constexpr int fac(int n)
    {
        constexpr int max_exp = 17;      // constexpr permet d'utiliser max_exp dans Expects
        Expects(0 <= n && n < max_exp);  // éviter les absurdités et le débordement
        int x = 1;
        for (int i = 2; i <= n; ++i) x *= i;
        return x;
    }

C'est du C++14.
Pour C++11, utiliser une formulation récursive de `fac()`.

##### Remarque

`constexpr` ne garantit pas l'évaluation au moment de la compilation ;
il garantit simplement que la fonction peut être évaluée au moment de la compilation pour des arguments d'expression constante si le programmeur l'exige ou si le compilateur décide de le faire pour optimiser.

    constexpr int min(int x, int y) { return x < y ? x : y; }

    void test(int v)
    {
        int m1 = min(-1, 2);            // probablement une évaluation au moment de la compilation
        constexpr int m2 = min(-1, 2);  // évaluation au moment de la compilation
        int m3 = min(-1, v);            // évaluation à l'exécution
        constexpr int m4 = min(-1, v);  // erreur : impossible d'évaluer au moment de la compilation
    }

##### Remarque

Ne pas essayer de rendre toutes les fonctions `constexpr`.
La plupart des calculs sont mieux faits à l'exécution.

##### Remarque

Toute API qui pourrait éventuellement dépendre d'une configuration de haut niveau à l'exécution ou
de la logique métier ne devrait pas être rendue `constexpr`. Une telle personnalisation ne peut pas être
évaluée par le compilateur, et toute fonction `constexpr` qui en dépendrait devrait être refactorisée ou perdre son `constexpr`.

##### Application

Impossible et inutile.
Le compilateur signale une erreur si une fonction non-`constexpr` est appelée là où une constante est requise.

### <a name="rf-inline"></a>F.5 : Si une fonction est très petite et critique en termes de temps, la déclarer `inline`

##### Justification

Certains optimiseurs sont bons pour inline-er sans indices du programmeur, mais ne comptez pas dessus.
Mesurez ! Au cours des 40 dernières années environ, on nous a promis des compilateurs capables d'inline-er mieux que les humains sans indices humains.
Nous attendons toujours.
Spécifier inline (explicitement, ou implicitement en écrivant des fonctions membres à l'intérieur d'une définition de classe) encourage le compilateur à faire un meilleur travail.

##### Exemple

    inline string cat(const string& s, const string& s2) { return s + s2; }

##### Exception

Ne pas mettre une fonction `inline` dans ce qui est censé être une interface stable à moins d'être certain qu'elle ne changera pas.
Une fonction inline fait partie de l'ABI.

##### Remarque

`constexpr` implique `inline`.

##### Remarque

Les fonctions membres définies dans la classe sont `inline` par défaut.

##### Exception

Les gabarits de fonctions (y compris les fonctions membres de classes gabarit `A<T>::function()` et les gabarits de fonctions membres `A::function<T>()`) sont normalement définis dans les en-têtes et donc inline.

##### Remarque

Envisager de rendre les fonctions hors ligne si elles ont plus de trois instructions et peuvent être déclarées hors ligne (telles que les fonctions membres de classe).

### <a name="rf-noexcept"></a>F.6 : Si votre fonction ne doit pas lever d'exception, la déclarer `noexcept`

##### Justification

Si une exception n'est pas censée être levée, le programme ne peut pas être supposé gérer l'erreur et devrait être terminé le plus tôt possible. Déclarer une fonction `noexcept` aide les optimiseurs en réduisant le nombre de chemins d'exécution alternatifs. Cela accélère aussi la sortie après un échec.

##### Exemple

Mettre `noexcept` sur chaque fonction écrite entièrement en C ou dans tout autre langage sans exceptions.
La bibliothèque standard C++ le fait implicitement pour toutes les fonctions de la bibliothèque standard C.

##### Remarque

Les fonctions `constexpr` peuvent lever des exceptions lorsqu'elles sont évaluées à l'exécution, il peut donc être nécessaire d'utiliser `noexcept` conditionnel pour certaines d'entre elles.

##### Exemple

Vous pouvez utiliser `noexcept` même sur des fonctions qui peuvent lever des exceptions :

    vector<string> collect(istream& is) noexcept
    {
        vector<string> res;
        for (string s; is >> s;)
            res.push_back(s);
        return res;
    }

Si `collect()` épuise la mémoire, le programme plante.
À moins que le programme ne soit conçu pour survivre à l'épuisement de la mémoire, ce pourrait être exactement la bonne chose à faire ;
`terminate()` pourrait générer des informations de journal d'erreur appropriées (mais après épuisement de la mémoire, il est difficile de faire quoi que ce soit de malin).

##### Remarque

Vous devez être conscient de l'environnement d'exécution dans lequel votre code s'exécute lors de la
décision d'ajouter `noexcept` à une fonction, en particulier en raison du problème
des exceptions et de l'allocation. Le code destiné à être parfaitement général (comme
la bibliothèque standard et d'autres code d'utilité de ce type) doit supporter des
environnements où une exception `bad_alloc` pourrait être gérée de manière significative.
Cependant, la plupart des programmes et environnements d'exécution ne peuvent pas significativement
gérer un échec d'allocation, et l'interruption du programme est la réponse la plus
propre et la plus simple à un échec d'allocation dans ces cas. Si vous savez que
votre code applicatif ne peut pas répondre à un échec d'allocation, il peut être
approprié d'ajouter `noexcept` même sur des fonctions qui allouent.

Autrement dit : Dans la plupart des programmes, la plupart des fonctions peuvent lever des exceptions (par ex. parce qu'elles
utilisent `new`, appellent des fonctions qui le font, ou utilisent des fonctions de bibliothèque qui signalent l'échec
en levant une exception), donc ne dispersez pas `noexcept` partout sans
considérer si les exceptions possibles peuvent être gérées.

`noexcept` est le plus utile (et le plus clairement correct) pour les fonctions bas niveau
fréquemment utilisées.

##### Remarque

Les destructeurs, les fonctions `swap`, les opérations de déplacement et les constructeurs par défaut ne doivent jamais lever d'exception.
Voir aussi [C.44](007-class.md#rc-default00).

##### Remarque

Il faut faire attention avec les fonctions virtuelles de base et les fonctions faisant partie d'une interface publique, car déclarer une fonction `noexcept` établit une garantie que toutes les implémentations actuelles et futures doivent respecter. Pour les fonctions virtuelles, tous les redéfineurs doivent aussi être `noexcept` et supprimer `noexcept` d'une fonction pourrait casser les fonctions appelantes.

##### Application

* (strict) Signaler les fonctions bas niveau qui ne sont pas `noexcept`, mais qui ne peuvent pas lever d'exception.
* Signaler les `swap`, `move`, destructeurs et constructeurs par défaut qui lèvent des exceptions.

### <a name="rf-smart"></a>F.7 : Pour un usage général, prendre des arguments `T*` ou `T&` plutôt que des pointeurs intelligents

##### Justification

Passer un pointeur intelligent transfère ou partage la propriété et ne devrait être utilisé que lorsque la sémantique de propriété est intentionnelle.
Une fonction qui ne manipule pas la durée de vie devrait prendre des pointeurs bruts ou des références à la place.

Passer par pointeur intelligent restreint l'utilisation d'une fonction aux appelants qui utilisent des pointeurs intelligents.
Une fonction qui a besoin d'un `widget` devrait pouvoir accepter n'importe quel objet `widget`, pas seulement ceux dont la durée de vie est gérée par un type particulier de pointeur intelligent.

Passer un pointeur intelligent partagé (par ex. `std::shared_ptr`) implique un coût à l'exécution.

##### Exemple

    // accepte n'importe quel int*
    void f(int*);

    // ne peut accepter que des ints pour lesquels vous voulez transférer la propriété
    void g(unique_ptr<int>);

    // ne peut accepter que des ints pour lesquels vous êtes disposé à partager la propriété
    void g(shared_ptr<int>);

    // ne change pas la propriété, mais requiert une propriété particulière de l'appelant
    void h(const unique_ptr<int>&);

    // accepte n'importe quel int
    void h(int&);

##### Exemple, mauvais

    // appelant
    void f(shared_ptr<widget>& w)
    {
        // ...
        use(*w); // seule utilisation de w -- la durée de vie n'est pas utilisée du tout
        // ...
    };

    // appelant
    shared_ptr<widget> my_widget = /* ... */;
    f(my_widget);

    widget stack_widget;
    f(stack_widget); // erreur

##### Exemple, bon

    // appelant
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
    f(stack_widget); // ok -- maintenant ça marche

##### Remarque

Nous pouvons détecter statiquement de nombreux cas courants de pointeurs pendants (voir [profil de sécurité de durée de vie](022-profile.md#ss-lifetime)). Les arguments de fonction vivent naturellement pendant la durée de l'appel de fonction, et ont donc moins de problèmes de durée de vie.

##### Application

* (Simple) Émettre un avertissement si une fonction prend un paramètre de type pointeur intelligent (qui surcharge `operator->` ou `operator*`) qui est copiable mais que la fonction n'utilise que pour appeler : `operator*`, `operator->` ou `get()`.
  Suggérer d'utiliser un `T*` ou `T&` à la place.
* Signaler un paramètre de type pointeur intelligent (un type qui surcharge `operator->` ou `operator*`) qui est copiable/déplaçable mais jamais copié/déplacé dans le corps de la fonction, et qui n'est jamais modifié, et qui n'est pas transmis à une autre fonction qui pourrait le faire. Cela signifie que la sémantique de propriété n'est pas utilisée.
  Suggérer d'utiliser un `T*` ou `T&` à la place.

**Voir aussi** :

* [Préférer `T*` à `T&` lorsque « aucun argument » est une option valide](006-functions.md#rf-ptr-ref)
* [Résumé des règles des pointeurs intelligents](009-resource.md#rr-summary-smartptrs)

### <a name="rf-pure"></a>F.8 : Préférer les fonctions pures

##### Justification

Les fonctions pures sont plus faciles à raisonner, parfois plus faciles à optimiser (et même à paralléliser), et parfois peuvent être mémorisées.

##### Exemple

    template<class T>
    auto square(T t) { return t * t; }

##### Application

Impossible.

### <a name="rf-unused"></a>F.9 : Les paramètres non utilisés doivent être sans nom

##### Justification

Lisibilité.
Suppression des avertissements de paramètres non utilisés.

##### Exemple

    widget* find(const set<widget>& s, const widget& w, Hint);   // à une époque, une indication était utilisée

##### Remarque

Permettre aux paramètres d'être sans nom a été introduit dans les années 1980 pour résoudre ce problème.

Si les paramètres sont conditionnellement non utilisés, les déclarer avec l'attribut `[[maybe_unused]]`.
Par exemple :

    template <typename Value>
    Value* find(const set<Value>& s, const Value& v, [[maybe_unused]] Hint h)
    {
        if constexpr (sizeof(Value) > CacheSize)
        {
            // une indication n'est utilisée que si Value est d'une certaine taille
        }
    }

##### Application

Signaler les paramètres non utilisés nommés.

### <a name="rf-name"></a>F.10 : Si une opération peut être réutilisée, lui donner un nom

##### Justification

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

    vector<Rec*> find_id(const string& name);    // trouve tous les enregistrements pour « name »

    auto x = find_if(vr.begin(), vr.end(),
        [&](Rec& r) {
            if (r.name.size() != n.size()) return false; // le nom à comparer est dans n
            for (int i = 0; i < r.name.size(); ++i)
                if (tolower(r.name[i]) != tolower(n[i])) return false;
            return true;
        }
    );

Il y a une fonction utile qui se cache ici (comparaison de chaînes insensible à la casse), comme c'est souvent le cas quand les arguments de lambda deviennent volumineux.

    bool compare_insensitive(const string& a, const string& b)
    {
        if (a.size() != b.size()) return false;
        for (int i = 0; i < a.size(); ++i) if (tolower(a[i]) != tolower(b[i])) return false;
        return true;
    }

    auto x = find_if(vr.begin(), vr.end(),
        [&](Rec& r) { return compare_insensitive(r.name, n); }
    );

Ou peut-être (si vous préférez éviter la liaison de nom implicite à n) :

    auto cmp_to_n = [&n](const string& a) { return compare_insensitive(a, n); };

    auto x = find_if(vr.begin(), vr.end(),
        [](const Rec& r) { return cmp_to_n(r.name); }
    );

##### Remarque

que ce soient des fonctions, des lambdas ou des opérateurs.

##### Exception

* Les lambdas logiquement utilisées uniquement localement, telles qu'un argument pour `for_each` et des algorithmes de flux de contrôle similaires.
* Les lambdas comme [initialisateurs](#??? <!-- @TODO-LINK : cible « initialisateurs » introuvable dans le document -->)

##### Application

* (strict) signaler les lambdas similaires
* ???

### <a name="rf-lambda"></a>F.11 : Utiliser une lambda sans nom si vous avez besoin d'un simple objet fonctionnel à un seul endroit

##### Justification

Cela rend le code concis et donne une meilleure localité que les alternatives.

##### Exemple

    auto earlyUsersEnd = std::remove_if(users.begin(), users.end(),
                                        [](const User &a) { return a.id > 100; });


##### Exception

Donner un nom à une lambda peut être utile pour la clarté même si elle n'est utilisée qu'une fois.

##### Application

* Chercher les lambdas identiques ou quasi identiques (à remplacer par des fonctions nommées ou des lambdas nommées).

## <a name="ss-call"></a>F.call : Passage de paramètres

Il existe diverses façons de passer des paramètres à une fonction et de retourner des valeurs.

### <a name="rf-conventional"></a>F.15 : Préférer des moyens simples et conventionnels de transmission d'informations

##### Justification

L'utilisation de techniques « inhabituelles et malines » cause des surprises, ralentit la compréhension par d'autres programmeurs et encourage les bogues.
Si vous ressentez vraiment le besoin d'une optimisation au-delà des techniques courantes, mesurez pour vous assurer que c'est vraiment une amélioration, et documentez/commentez car l'amélioration pourrait ne pas être portable.

Les tableaux suivants récapitulent les conseils des Lignes Directrices suivantes, F.16-21.

Passage de paramètres normal :

![Tableau du passage de paramètres normal](./param-passing-normal.png "Passage de paramètres normal")

Passage de paramètres avancé :

![Tableau du passage de paramètres avancé](./param-passing-advanced.png "Passage de paramètres avancé")

Utilisez les techniques avancées uniquement après avoir démontré le besoin, et documentez ce besoin dans un commentaire.

Pour le passage de séquences de caractères, voir [Chaînes](018-stdlib.md#ss-string).

##### Exception

Pour exprimer la propriété partagée en utilisant des types `shared_ptr`, plutôt que de suivre les Lignes Directrices F.16-21,
suivre [R.34](009-resource.md#rr-sharedptrparam-owner), [R.35](009-resource.md#rr-sharedptrparam) et [R.36](009-resource.md#rr-sharedptrparam-const).

### <a name="rf-in"></a>F.16 : Pour les paramètres « en lecture », passer les types à copie peu coûteuse par valeur et les autres par référence à `const`

##### Justification

Les deux permettent à l'appelant de savoir qu'une fonction ne modifiera pas l'argument, et les deux permettent l'initialisation par valeurs non l-value.

Ce qui est « peu coûteux à copier » dépend de l'architecture de la machine, mais deux ou trois mots (doubles, pointeurs, références) sont généralement les meilleurs à passer par valeur.
Quand la copie est peu coûteuse, rien ne surpasse la simplicité et la sécurité de la copie, et pour les petits objets (jusqu'à deux ou trois mots), c'est aussi plus rapide que le passage par référence car cela n'exige pas une indirection supplémentaire pour y accéder depuis la fonction.

##### Exemple

    void f1(const string& s);  // OK : passage par référence à const ; toujours peu coûteux

    void f2(string s);         // mauvais : potentiellement coûteux

    void f3(int x);            // OK : imbattable

    void f4(const int& x);     // mauvais : surcoût d'accès dans f4()

Pour des usages avancés (uniquement), où vous avez vraiment besoin d'optimiser pour les valeurs non l-value passées à des paramètres « en lecture seule » :

* Si la fonction va inconditionnellement déplacer depuis l'argument, le prendre par `&&`. Voir [F.18](006-functions.md#rf-consume).
* Si la fonction va garder une copie locale modifiable de l'argument uniquement pour son usage local, le prendre par valeur convient.
* Si la fonction va garder une copie de l'argument pour la passer à une autre destination (à une autre fonction, ou la stocker dans un emplacement non local), en plus du passage par `const&` (pour les l-values),
  ajouter une surcharge qui passe le paramètre par `&&` (pour les valeurs non l-value) et dans le corps faire `std::move` vers sa destination. Essentiellement, cela surcharge un « seront déplacés » ; voir [F.18](006-functions.md#rf-consume).
* Dans des cas spéciaux, tels que plusieurs paramètres « lecture + copie », envisager d'utiliser le transfert parfait. Voir [F.19](006-functions.md#rf-forward).

##### Exemple

    int multiply(int, int); // juste des ints en lecture, passer par valeur

    // suffix est en lecture seule mais pas aussi peu coûteux qu'un int, passer par const&
    string& concatenate(string&, const string& suffix);

    void sink(unique_ptr<widget>);  // en lecture seule, et transfère la propriété du widget

Évitez les « techniques ésotériques » telles que le passage d'arguments comme `T&&` « pour l'efficacité ».
La plupart des rumeurs sur les avantages de performance du passage par `&&` sont fausses ou fragiles (mais voir [F.18](006-functions.md#rf-consume) et [F.19](006-functions.md#rf-forward)).

##### Remarques

Une référence peut être supposée désigner un objet valide (règle du langage).
Il n'y a pas de (légitime) « référence nulle. »
Si vous avez besoin de la notion de valeur optionnelle, utilisez un pointeur, `std::optional`, ou une valeur spéciale utilisée pour désigner « aucune valeur. »

##### Application

* (Simple) ((Fondation)) Avertir quand un paramètre passé par valeur a une taille supérieure à `4 * sizeof(void*)`.
  Suggérer d'utiliser une référence à `const` à la place.
* (Simple) ((Fondation)) Avertir quand un paramètre passé par référence à `const` a une taille inférieure ou égale à `2 * sizeof(void*)`. Suggérer de passer par valeur à la place.
* (Simple) ((Fondation)) Avertir quand un paramètre passé par référence à `const` est `move`d.
* (Non simple) Remarque : une application plus stricte dépendrait des caractéristiques de performance de l'architecture cible.

##### Exception

Pour exprimer la propriété partagée en utilisant des types `shared_ptr`, suivre [R.34](009-resource.md#rr-sharedptrparam-owner) ou [R.36](009-resource.md#rr-sharedptrparam-const),
selon que la fonction prend ou non inconditionnellement une référence à l'argument.

### <a name="rf-inout"></a>F.17 : Pour les paramètres « en lecture-écriture », passer par référence à non-`const`

##### Justification

Cela fait comprendre clairement aux appelants que l'objet est supposé être modifié.

##### Exemple

    void update(Record& r);  // suppose que update écrit dans r

##### Remarque

Certains types définis par l'utilisateur et de la bibliothèque standard, tels que `span<T>` ou les itérateurs
sont [peu coûteux à copier](006-functions.md#rf-in) et peuvent être passés par valeur, tout en ayant ainsi une
sémantique de référence (lecture-écriture) mutable :

    void increment_all(span<int> a)
    {
      for (auto&& e : a)
        ++e;
    }

##### Remarque

Un argument `T&` peut transmettre des informations dans une fonction ainsi que dehors.
Ainsi `T&` pourrait être un paramètre en lecture-écriture. Cela peut en soi être un problème et une source d'erreurs :

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

Ici, l'auteur de `g()` fournit un tampon pour que `f()` le remplisse, mais `f()` le remplace simplement (à un coût légèrement plus élevé qu'une simple copie des caractères).
Une mauvaise erreur logique peut se produire si l'auteur de `g()` suppose incorrectement la taille du `buffer`.

##### Application

* (Modéré) ((Fondation)) Avertir au sujet des fonctions concernant les paramètres par référence à non-`const` qui ne les *écrivent pas*.
* (Simple) ((Fondation)) Avertir quand un paramètre non-`const` passé par référence est `move`d.

### <a name="rf-consume"></a>F.18 : Pour les paramètres « seront déplacés », passer par `X&&` et `std::move` le paramètre

##### Justification

C'est efficace et élimine les bogues au point d'appel : `X&&` se lie aux valeurs non l-value, ce qui exige un `std::move` explicite au point d'appel si on passe une l-value.

##### Exemple

    void sink(vector<int>&& v)  // sink prend la propriété de ce que l'argument possédait
    {
        // normalement il y aurait des accès en lecture de v ici
        store_somewhere(std::move(v));
        // normalement plus d'utilisation de v ici ; il a été déplacé
    }

Notez que le `std::move(v)` rend possible pour `store_somewhere()` de laisser `v` dans un état déplacé.
[Cela pourrait être dangereux](007-class.md#rc-move-semantic).


##### Exception

Les types propriétaire uniques qui sont uniquement déplacables et peu coûteux à déplacer, tels que `unique_ptr`, peuvent aussi être passés par valeur, ce qui est plus simple à écrire et atteint le même effet. Le passage par valeur génère un déplacement supplémentaire (peu coûteux), mais préférez la simplicité et la clarté d'abord.

Par exemple :

    template<class T>
    void sink(std::unique_ptr<T> p)
    {
        // utiliser p ... possiblement std::move(p) plus loin ailleurs
    }   // p est détruit

##### Exception

Si le paramètre « sera déplacé » est un `shared_ptr`, suivre [R.34](009-resource.md#rr-sharedptrparam-owner) et passer le `shared_ptr` par valeur.

##### Application

* Signaler tous les paramètres `X&&` (où `X` n'est pas un nom de paramètre de type gabarit) dont le corps de fonction les utilise sans `std::move`.
* Signaler les accès à des objets déplacés.
* Ne pas conditionnellement déplacer des objets

### <a name="rf-forward"></a>F.19 : Pour les paramètres « à transmettre », passer par `TP&&` et uniquement `std::forward` le paramètre

##### Justification

Si l'objet doit être transmis à d'autres codes et non directement utilisé par cette fonction, nous voulons que cette fonction soit agnostique quant à la constance et à la nature de valeur non l-value de l'argument.

Dans ce cas, et seulement dans ce cas, rendre le paramètre `TP&&` où `TP` est un paramètre de type gabarit -- cela *ignore* et *préserve* la constance et la nature de valeur non l-value. Par conséquent, tout code qui utilise un `TP&&` déclare implicitement qu'il ne se soucie pas de la constance et de la nature de valeur non l-value de la variable (car elles sont ignorées), mais qu'il a l'intention de transmettre la valeur à d'autres codes qui s'en soucient (car elles sont préservées). Quand utilisé comme paramètre, `TP&&` est sûr car tout objet temporaire passé par l'appelant vivra pendant la durée de l'appel de fonction. Un paramètre de type `TP&&` devrait essentiellement toujours être transmis via `std::forward` dans le corps de la fonction.

##### Exemple

Généralement, on transmet le paramètre entier (ou le paquet de paramètres, en utilisant `...`) exactement une fois sur chaque chemin de contrôle statique :

    template<class F, class... Args>
    inline decltype(auto) invoke(F&& f, Args&&... args)
    {
        return forward<F>(f)(forward<Args>(args)...);
    }

##### Exemple

Parfois, on peut transmettre un paramètre composé par morceaux, chaque sous-objet une fois sur chaque chemin de contrôle statique :

    template<class PairLike>
    inline auto test(PairLike&& pairlike)
    {
        // ...
        f1(some, args, and, forward<PairLike>(pairlike).first);           // transmettre .first
        f2(and, forward<PairLike>(pairlike).second, in, another, call);   // transmettre .second
    }

##### Application

* Signaler une fonction qui prend un paramètre `TP&&` (où `TP` est un nom de paramètre de type gabarit) et fait quoi que ce soit d'autre que `std::forward` exactement une fois sur chaque chemin statique, ou `std::forward` plus d'une fois mais qualifié par un membre de données différent exactement une fois sur chaque chemin statique.

### <a name="rf-out"></a>F.20 : Pour les valeurs de sortie « en écriture », préférer les valeurs retournées aux paramètres de sortie

##### Justification

Une valeur retournée se documente d'elle-même, alors qu'un `&` pourrait être en lecture-écriture ou en écriture seule et est susceptible d'être mal utilisé.

Cela inclut les grands objets comme les conteneurs standard qui utilisent des opérations de déplacement implicites pour les performances et pour éviter la gestion explicite de la mémoire.

Si vous avez plusieurs valeurs à retourner, [utilisez un tuple](006-functions.md#rf-out-multi) ou un type multi-membres similaire.

##### Exemple

    // OK : retourner des pointeurs vers les éléments avec la valeur x
    vector<const int*> find_all(const vector<int>&, int x);

    // Mauvais : placer les pointeurs vers les éléments avec la valeur x en lecture-écriture
    void find_all(const vector<int>&, vector<const int*>& out, int x);

##### Remarque

Une `struct` de nombreux éléments (individuellement peu coûteux à déplacer) pourrait être collectivement coûteuse à déplacer.

##### Exceptions

* Pour les types non concrets, tels que les types dans une hiérarchie d'héritage, retourner l'objet par `unique_ptr` ou `shared_ptr`.
* Si un type est coûteux à déplacer (par ex. `array<BigTrivial>`), envisager de l'allouer sur le tas libre et retourner un gestionnaire (par ex. `unique_ptr`), ou de le passer dans une référence à un objet cible non-`const` à remplir (à utiliser comme paramètre de sortie).
* Pour réutiliser un objet qui porte une capacité (par ex. `std::string`, `std::vector`) à travers plusieurs appels à la fonction dans une boucle interne : [le traiter comme un paramètre en lecture-écriture et le passer par référence](006-functions.md#rf-out-multi).

##### Exemple

En supposant que `Matrix` ait des opérations de déplacement (possiblement en gardant ses éléments dans un `std::vector`) :

    Matrix operator+(const Matrix& a, const Matrix& b)
    {
        Matrix res;
        // ... remplir res avec la somme ...
        return res;
    }

    Matrix x = m1 + m2;  // constructeur par déplacement

    y = m3 + m3;         // affectation par déplacement


##### Remarque

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

##### Application

* Signaler les références à des paramètres non-`const` qui ne sont pas lus avant d'être écrits et sont d'un type qui pourrait être retourné peu coûteusement ; ils devraient être des valeurs de retour de sortie.

### <a name="rf-out-multi"></a>F.21 : Pour retourner plusieurs valeurs de sortie, préférer le retour d'une structure

##### Justification

Une valeur retournée se documente d'elle-même comme valeur « en écriture seule ».
Notez que C++ a bien des valeurs de retour multiples, par convention d'utilisation de types de type tuple (`struct`, `array`, `tuple`, etc.),
possiblement avec la commodité supplémentaire des liaisons structurées (C++17) au point d'appel.
Préférer l'utilisation d'une `struct` nommée si possible.
Sinon, un `tuple` est utile dans les gabarits variadiques.

##### Exemple

    // MAUVAIS : paramètre en écriture seule documenté dans un commentaire
    int f(const string& input, /*sortie seule*/ string& output_data)
    {
        // ...
        output_data = something();
        return status;
    }

    // BON : auto-documenté
    struct f_result { int status; string data; };

    f_result f(const string& input)
    {
        // ...
        return {status, something()};
    }

La bibliothèque standard C++98 utilisait ce style par endroits, en retournant des `pair` dans certaines fonctions.
Par exemple, étant donné un `set<string> my_set`, considérez :

    // C++98
    pair<set::iterator, bool> result = my_set.insert("Hello");
    if (result.second)
        do_something_with(result.first);    // contournement

Avec C++17, nous pouvons utiliser des « liaisons structurées » pour donner un nom à chaque membre :

    if (auto [ iter, success ] = my_set.insert("Hello"); success)
        do_something_with(iter);

Une `struct` avec des noms significatifs est plus courante en C++ moderne.
Voir par exemple `ranges::min_max_result`, `from_chars_result`, et d'autres.

##### Exception

Parfois, nous avons besoin de passer un objet à une fonction pour manipuler son état.
Dans de tels cas, passer l'objet par référence [`T&`](006-functions.md#rf-inout) est généralement la bonne technique.
Transmettre explicitement un paramètre en lecture-écriture de nouveau en retour comme valeur de retour est souvent inutile.
Par exemple :

    istream& operator>>(istream& in, string& s);    // comme std::operator>>()

    for (string s; in >> s; ) {
        // faire quelque chose avec la ligne
    }

Ici, `s` et `in` sont tous deux utilisés comme paramètres en lecture-écriture.
Nous passons `in` par référence (non-`const`) pour pouvoir manipuler son état.
Nous passons `s` pour éviter des allocations répétées.
En réutilisant `s` (passé par référence), nous allouons de la nouvelle mémoire seulement quand nous avons besoin d'élargir la capacité de `s`.
Cette technique est parfois appelée le « motif de sortie allouée par l'appelant » et est particulièrement utile pour les types,
tels que `string` et `vector`, qui ont besoin de faire des allocations sur le tas libre.

Pour comparer, si nous passions toutes les valeurs comme valeurs de retour, nous écririons quelque chose comme ceci :

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

Nous considérons cela considérablement moins élégant avec des performances considérablement inférieures.

Pour une lecture strictement littérale de cette règle (F.21), l'exception n'est pas vraiment une exception car elle repose sur des paramètres en lecture-écriture,
plutôt que sur les simples paramètres de sortie mentionnés dans la règle.
Cependant, nous préférons être explicites, plutôt que subtils.

##### Remarque

Dans la plupart des cas, il est utile de retourner un type spécifique défini par l'utilisateur.
Par exemple :

    struct Distance {
        int value;
        int unit = 1;   // 1 signifie mètres
    };

    Distance d1 = measure(obj1);        // accéder à d1.value et d1.unit
    auto d2 = measure(obj2);            // accéder à d2.value et d2.unit
    auto [value, unit] = measure(obj3); // accéder à value et unit ; un peu redondant
                                        // pour ceux qui connaissent measure()
    auto [x, y] = measure(obj4);        // ne pas faire ; susceptible d'être confus

Les `pair` et `tuple` trop génériques ne devraient être utilisés que lorsque la valeur retournée représente des entités indépendantes plutôt qu'une abstraction.

Une autre option est d'utiliser `optional<T>` ou `expected<T, error_code>`, plutôt que `pair` ou `tuple`.
Quand utilisés de manière appropriée, ces types transmettent plus d'informations sur ce que les membres signifient que `pair<T, bool>` ou `pair<T, error_code>`.

##### Remarque

Quand l'objet à retourner est initialisé à partir de variables locales qui sont coûteuses à copier,
un `move` explicite peut être utile pour éviter la copie :

    pair<LargeObject, LargeObject> f(const string& input)
    {
        LargeObject large1 = g(input);
        LargeObject large2 = h(input);
        // ...
        return { move(large1), move(large2) }; // pas de copies
    }

Ou alternativement,

    pair<LargeObject, LargeObject> f(const string& input)
    {
        // ...
        return { g(input), h(input) }; // pas de copies, pas de déplacements
    }

Notez que c'est différent de l'anti-motif `return move(...)` de [ES.56](010-expr.md#res-move).

##### Application

* Les paramètres de sortie devraient être remplacés par des valeurs de retour.
  Un paramètre de sortie est celui que la fonction écrit, invoque une fonction membre non-`const`, ou transmet comme non-`const`.
* Les types de retour `pair` ou `tuple` devraient être remplacés par `struct`, si possible.
  Dans les gabarits variadiques, `tuple` est souvent inévitable.

### <a name="rf-ptr-ref"></a>F.60 : Préférer `T*` à `T&` lorsque « aucun argument » est une option valide

##### Justification

Un pointeur (`T*`) peut être `nullptr` et une référence (`T&`) ne peut pas, il n'y a pas de « référence nulle » valide.
Parfois, avoir `nullptr` comme alternative pour indiquer « aucun objet » est utile, mais si ce n'est pas le cas, une référence est notatoirement plus simple et pourrait produire un meilleur code.

##### Exemple

    string zstring_to_string(zstring p) // zstring est un char* ; c'est une chaîne au style C
    {
        if (!p) return string{};    // p pourrait être nullptr ; penser à vérifier
        return string{p};
    }

    void print(const vector<int>& r)
    {
        // r désigne un vector<int> ; pas de vérification nécessaire
    }

##### Remarque

Il est possible, mais ce n'est pas du C++ valide, de construire une référence qui est essentiellement un `nullptr` (par ex. `T* p = nullptr; T& r = *p;`).
Cette erreur est très rare.

##### Remarque

Si vous préférez la notation pointeur (`->` et/ou `*` vs. `.`), `not_null<T*>` fournit la même garantie que `T&`.

##### Application

* Signaler ???

### <a name="rf-ptr"></a>F.22 : Utiliser `T*` ou `owner<T*>` pour désigner un seul objet

##### Justification

Lisibilité : cela rend le sens d'un pointeur brut clair.
Permet un support significatif des outils.

##### Remarque

Dans le code C et C++ traditionnel, un simple `T*` est utilisé à de nombreuses fins faiblement liées, telles que :

* Identifier un (seul) objet (ne pas être supprimé par cette fonction)
* Point