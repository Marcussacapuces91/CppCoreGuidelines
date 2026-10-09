---
title: Fonctions
---

# <a name="s-functions"></a>F : Fonctions

Une fonction spécifie une action ou un calcul qui fait passer le système d’un état cohérent à l’autre. C’est le bloc de construction fondamental des programmes.

Il doit être possible de nommer une fonction de façon significative, d’indiquer les exigences de ses arguments et d’exprimer clairement la relation entre les arguments et le résultat. Une implémentation n’est pas une spécification. Essayez de réfléchir à ce que fait une fonction autant qu’à la façon dont elle le fait.  
Les fonctions sont la partie la plus critique de la plupart des interfaces, donc consultez les règles d’interfaces.

**Résumé des règles de fonction :**

#### Règles de définition de fonction :

* [F.1 : « Packager » des opérations signifiantes sous forme de fonctions soigneusement nommées](#rf-package)
* [F.2 : Une fonction doit réaliser une seule opération logique](#rf-logical)
* [F.3 : Garder les fonctions courtes et simples](#rf-single)
* [F.4 : Si une fonction peut être évaluée à la compilation, la déclarer `constexpr`](#rf-constexpr)
* [F.5 : Si une fonction est très petite et critique en temps, la déclarer `inline`](#rf-inline)
* [F.6 : Si votre fonction ne doit pas lancer d’exception, la déclarer `noexcept`](#rf-noexcept)
* [F.7 : Pour un usage général, prendre des arguments `T*` ou `T&` plutôt que des pointeurs intelligents](#rf-smart)
* [F.8 : Privilégier les fonctions pures](#rf-pure)
* [F.9 : Les paramètres inutilisés doivent être non nommés](#rf-unused)
* [F.10 : Si une opération peut être réutilisée, lui donner un nom](#rf-name)
* [F.11 : Utiliser une lambda anonyme si vous avez besoin d’un simple objet fonctionnel en un seul lieu](#rf-lambda)

#### Règles d’expression des paramètres :

* [F.15 : Préférer des façons simples et conventionnelles de transmettre l’information](#rf-conventional)
* [F.16 : Pour les paramètres « in », passer les types à copie bon marché par valeur et les autres par référence `const`](#rf-in)
* [F.17 : Pour les paramètres « in‑out », passer par référence non‑`const`](#rf-inout)
* [F.18 : Pour les paramètres « will‑move‑from », les passer par `X&&` et les `std::move` dans la fonction](#rf-consume)
* [F.19 : Pour les paramètres « forward », les passer par `TP&&` et ne les `std::forward` qu’une fois](#rf-forward)
* [F.20 : Pour les valeurs de sortie, préférer les valeurs de retour aux paramètres de sortie](#rf-out)
* [F.21 : Pour retourner plusieurs valeurs « out », préférer renvoyer une `struct`](#rf-out-multi)
* [F.60 : Préférer `T*` à `T&` quand « pas d’argument » est une option valide](#rf-ptr-ref)

#### Règles de sémantique de passage de paramètres :

* [F.22 : Utiliser `T*` ou `owner<T*>` pour désigner un seul objet](#rf-ptr)
* [F.23 : Utiliser un `not_null<T>` pour indiquer que « null » n’est pas une valeur valide](#rf-nullptr)
* [F.24 : Utiliser un `span<T>` ou un `span_p<T>` pour désigner une séquence demi‑ouverte](#rf-range)
* [F.25 : Utiliser un `zstring` ou un `not_null<zstring>` pour désigner une chaîne de style C](#rf-zstring)
* [F.26 : Utiliser un `unique_ptr<T>` pour transférer la propriété lorsqu’un pointeur est nécessaire](#rf-unique_ptr)
* [F.27 : Utiliser un `shared_ptr<T>` pour partager la propriété](#rf-shared_ptr)

#### Règles de retour de valeur :

* [F.42 : Retourner un `T*` pour indiquer uniquement une position](#rf-return-ptr)
* [F.43 : Ne jamais (directement ou indirectement) retourner un pointeur ou une référence à un objet local](#rf-dangle)
* [F.44 : Retourner un `T&` quand la copie est indésirable et qu’« aucun objet à retourner » n’est nécessaire](#rf-return-ref)
* [F.45 : Ne pas retourner un `T&&`](#rf-return-ref-ref)
* [F.46 : `int` est le type de retour de `main()`](#rf-main)
* [F.47 : Retourner `T&` depuis les opérateurs d’affectation](#rf-assignment-op)
* [F.48 : Ne pas retourner `std::move(local)`](#rf-return-move-local)
* [F.49 : Ne pas retourner `const T`](#rf-return-const)

#### Autres règles de fonction :

* [F.50 : Utiliser une lambda quand une fonction ne le ferait pas (pour capturer des variables locales ou écrire une fonction locale)](#rf-capture-vs-overload)
* [F.51 : Quand un choix existe, privilégier les arguments par défaut aux surcharges](#rf-default-args)
* [F.52 : Privilégier la capture par référence dans les lambdas qui seront utilisées localement, y compris lorsqu’elles sont passées à des algorithmes](#rf-reference-capture)
* [F.53 : Éviter la capture par référence dans les lambdas qui seront utilisées de façon non locale, y compris retournées, stockées sur le tas ou passées à un autre thread](#rf-value-capture)
* [F.54 : Lors de l’écriture d’une lambda qui capture `this` ou tout membre de classe, ne pas utiliser de capture par défaut `[=]`](#rf-this-capture)
* [F.55 : Ne pas utiliser d’arguments `va_arg`](#f-varargs)
* [F.56 : Éviter les imbrications de conditions inutiles](#f-nesting)

Les fonctions sont très semblables aux lambdas et aux objets fonctionnels.

**Voir aussi** : [C.lambdas : Objets fonction et lambdas](#ss-lambdas)

---

## <a name="ss-fct-def"></a>F.def : Définitions de fonction

Une définition de fonction est une déclaration qui spécifie également l’implémentation de la fonction, c’est‑à‑dire son corps.

### <a name="rf-package"></a>F.1 : « Packager » des opérations signifiantes sous forme de fonctions soigneusement nommées

#### Raison

Factoriser le code commun rend le code plus lisible, plus susceptible d’être réutilisé, et limite les erreurs dues à du code complexe.  
Si quelque chose est une action bien définie, séparez‑le du code environnant et donnez‑lui un nom.

#### Exemple, ne pas faire

    void read_and_print(istream& is)    // lire et imprimer un int
    {
        int x;
        if (is >> x)
            cout << "the int is " << x << '\n';
        else
            cerr << "no int on input\n";
    }

Presque tout est erroné dans `read_and_print`.  
Il lit, il écrit (vers un `ostream` fixe), il écrit des messages d’erreur (vers un `ostream` fixe), il ne gère que des `int`.  
Il n’y a rien à réutiliser ; des opérations logiquement séparées sont mêlées et les variables locales restent en portée après la fin de leur usage logique.  
Pour un petit exemple cela paraît correct, mais si les opérations d’entrée, de sortie et de traitement d’erreur deviennent plus compliquées, le désordre devient difficile à comprendre.

#### Note

Si vous écrivez une lambda non triviale qui peut être utilisée en plusieurs endroits, donnez‑lui un nom en l’affectant à une variable (généralement non‑locale).

#### Exemple

    sort(a, b, [](T x, T y) { return x.rank() < y.rank() && x.value() < y.value(); });

Nommer cette lambda découpe l’expression en ses parties logiques et donne un indice fort sur le sens de la lambda.

    auto lessT = [](T x, T y) { return x.rank() < y.rank() && x.value() < y.value(); };
    sort(a, b, lessT);

Le code le plus court n’est pas toujours le meilleur en termes de performance ou de maintenabilité.

#### Exception

Les corps de boucle, y compris les lambdas utilisées comme corps de boucle, ont rarement besoin d’être nommés.  
En revanche, les corps de boucle volumineux (ex. dizaines de lignes ou de pages) peuvent poser problème. La règle <a href="#rf-single">« Garder les fonctions courtes et simples »</a> implique « Garder les corps de boucle courts ». De même, les lambdas utilisées comme arguments de rappel sont parfois non triviales, mais peu susceptibles d’être réutilisées.

#### Application

* Voir <a href="#rf-single">« Garder les fonctions courtes et simples »</a>  
* Signaler les lambdas identiques ou très similaires utilisées à des endroits différents.

---

### <a name="rf-logical"></a>F.2 : Une fonction doit réaliser une seule opération logique

#### Raison

Une fonction qui réalise une seule opération est plus simple à comprendre, à tester et à réutiliser.

#### Exemple

    void read_and_print()    // mauvais
    {
        int x;
        cin >> x;
        // vérification d’erreurs
        cout << x << "\n";
    }

C’est un monolithe lié à une entrée spécifique et ne pourra jamais être réutilisé autrement.  
Divisez la fonction en parties logiques appropriées et paramétrez :

    int read(istream& is)    // meilleur
    {
        int x;
        is >> x;
        // vérification d’erreurs
        return x;
    }

    void print(ostream& os, int x)
    {
        os << x << "\n";
    }

Ces deux fonctions peuvent maintenant être combinées où cela est nécessaire :

    void read_and_print()
    {
        auto x = read(cin);
        print(cout, x);
    }

Si besoin, on peut encore templatizer `read()` et `print()` sur le type de données, le mécanisme d’E/S, la réponse aux erreurs, etc. Exemple :

    auto read = [](auto& input, auto& value)    // meilleur
    {
        input >> value;
        // vérification d’erreurs
    };

    void print(auto& output, const auto& value)
    {
        output << value << "\n";
    }

#### Application

* Considérer suspectes les fonctions avec plus d’un paramètre « out ». Utiliser des valeurs de retour à la place, éventuellement un `tuple` pour plusieurs valeurs.  
* Considérer suspectes les fonctions « grosses » qui ne tiennent pas sur un écran d’édition. Envisager de les factoriser en sous‑opérations bien nommées.  
* Considérer suspectes les fonctions avec 7 paramètres ou plus.

---

### <a name="rf-single"></a>F.3 : Garder les fonctions courtes et simples

#### Raison

Les fonctions longues sont difficiles à lire, plus susceptibles de contenir du code complexe, et plus susceptibles d’avoir des variables dont la portée dépasse le nécessaire.  
Les fonctions avec des structures de contrôle complexes ont tendance à être longues et à masquer des erreurs logiques.

#### Exemple

    double simple_func(double val, int flag1, int flag2)
        // simple_func : prend une valeur et calcule la sortie ASIC attendue,
        // compte tenu des deux indicateurs de mode.
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

Cette fonction est trop compliquée.  
Comment savoir si toutes les alternatives possibles ont été correctement traitées ?  
Oui, cela transgresse d’autres règles aussi.

Refactorisation possible :

    double func1_muon(double val, int flag)
    {
        // …
    }

    double func1_tau(double val, int flag1, int flag2)
    {
        // …
    }

    double simple_func(double val, int flag1, int flag2)
        // simple_func : prend une valeur et calcule la sortie ASIC attendue,
        // compte tenu des deux indicateurs de mode.
    {
        if (flag1 > 0)
            return func1_muon(val, flag2);
        if (flag1 == -1)
            // géré par func1_tau : flag1 = -flag1;
            return func1_tau(-val, flag1, flag2);
        return 0.;
    }

#### Note

« Ne tient pas sur un écran » est souvent une bonne définition pratique de « trop large ».  
Les fonctions de une à cinq lignes sont à considérer comme normales.

#### Note

Divisez les fonctions volumineuses en fonctions plus petites, cohésives et nommées.  
Les petites fonctions simples sont facilement inlinees lorsque le coût d’un appel de fonction est important.

#### Application

* Signaler les fonctions qui ne « tiennent pas sur un écran ».  
  Quelle taille ? Essayez : 60 lignes × 140 caractères — cela correspond à peu près à la largeur confortable d’une page de livre.  
* Signaler les fonctions trop complexes.  
  Qu’est‑ce qui est « trop » ? On peut utiliser la complexité cyclomatique : plus de 10 chemins logiques distincts, par exemple.

---

### <a name="rf-constexpr"></a>F.4 : Si une fonction peut devoir être évaluée à la compilation, la déclarer `constexpr`

#### Raison

`constexpr` indique au compilateur qu’il peut autoriser l’évaluation à la compilation.

#### Exemple

Le (in)fâme factoriel :

    constexpr int fac(int n)
    {
        constexpr int max_exp = 17;      // constexpr permet d’utiliser max_exp dans Expects
        Expects(0 <= n && n < max_exp);  // empêche les bêtises et le débordement
        int x = 1;
        for (int i = 2; i <= n; ++i) x *= i;
        return x;
    }

C’est du C++14.  
Pour du C++11, utilisez une formulation récursive de `fac()`.

#### Note

`constexpr` ne garantit pas l’évaluation à la compilation ; il garantit simplement que la fonction peut être évaluée à la compilation pour des arguments littéraux si le programmeur l’exige ou si le compilateur le juge opportun pour l’optimisation.

    constexpr int min(int x, int y) { return x < y ? x : y; }

    void test(int v)
    {
        int m1 = min(-1, 2);            // très probablement évaluation à la compilation
        constexpr int m2 = min(-1, 2);  // évaluation à la compilation
        int m3 = min(-1, v);            // évaluation à l’exécution
        constexpr int m4 = min(-1, v);  // erreur : impossible d’évaluer à la compilation
    }

#### Note

Ne tentez pas de rendre toutes les fonctions `constexpr`.  
La plupart des calculs sont mieux faits à l’exécution.

#### Note

Toute API qui pourrait dépendre d’une configuration d’exécution ou d’une logique métier ne doit pas être marquée `constexpr`. Cette personnalisation ne peut pas être évaluée par le compilateur, et toute fonction `constexpr` qui dépendait de cette API devrait être refactorisée ou perdre le `constexpr`.

#### Application

Impossible et inutile. Le compilateur génère une erreur si une fonction non‑`constexpr` est appelée dans un contexte où une constante est requise.

---

### <a name="rf-inline"></a>F.5 : Si une fonction est très petite et critique en temps, la déclarer `inline`

#### Raison

Certains optimiseurs sont bons pour l’inlining sans indice du programmeur, mais il ne faut pas compter dessus.  
Mesurez ! Au cours des quarante dernières années, on nous a promis des compilateurs capables d’inliner mieux que les humains sans indice. Nous attendons toujours.  
Spécifier `inline` (explicitement, ou implicitement en définissant des fonctions membres dans la classe) incite le compilateur à faire un meilleur travail.

#### Exemple

    inline string cat(const string& s, const string& s2) { return s + s2; }

#### Exception

Ne placez pas une fonction `inline` dans une interface censée être stable à moins d’être certain qu’elle ne changera pas.  
Une fonction `inline` fait partie de l’ABI.

#### Note

`constexpr` implique `inline`.

#### Note

Les fonctions membres définies à l’intérieur d’une classe sont `inline` par défaut.

#### Exception

Les modèles de fonction (y compris les fonctions membres de modèles de classe `A<T>::function()` et les modèles de fonction membre `A::function<T>()`) sont normalement définis dans les en‑têtes et donc `inline`.

#### Note

Envisagez de mettre les fonctions hors‑ligne si elles comportent plus de trois instructions et peuvent être déclarées hors‑ligne (par ex. fonctions membres de classe).

---

### <a name="rf-noexcept"></a>F.6 : Si votre fonction ne doit pas lancer d’exception, la déclarer `noexcept`

#### Raison

Si une exception n’est pas censée être lancée, le programme ne peut pas supposer pouvoir gérer l’erreur et doit être terminé dès que possible. Déclarer une fonction `noexcept` aide les optimiseurs en réduisant le nombre de chemins d’exécution alternatifs. Cela accélère également la sortie après un échec.

#### Exemple

Placez `noexcept` sur chaque fonction entièrement écrite en C ou dans tout autre langage sans exceptions. La bibliothèque standard C++ le fait implicitement pour toutes les fonctions de la bibliothèque C.

#### Note

Les fonctions `constexpr` peuvent lancer d’exception lorsqu’elles sont évaluées à l’exécution, il faut donc parfois rendre `noexcept` conditionnel.

#### Exemple

    vector<string> collect(istream& is) noexcept
    {
        vector<string> res;
        for (string s; is >> s;)
            res.push_back(s);
        return res;
    }

Si `collect()` manque de mémoire, le programme plante.  
À moins que le programme ne soit conçu pour survivre à une pénurie de mémoire, c’est probablement le bon comportement ; `terminate()` peut générer des informations d’erreur utiles (mais après une pénurie de mémoire il est difficile de faire quoi que ce soit d’astucieux).

#### Note

Vous devez connaître l’environnement d’exécution de votre code lorsqu’il s’agit de décider d’ajouter `noexcept`, en particulier à cause des allocations. Le code destiné à être parfaitement générique (bibliothèque standard, utilitaires…) doit supporter les environnements où une exception `bad_alloc` peut être gérée sensément. Cependant, la plupart des programmes et environnements d’exécution ne peuvent pas gérer proprement un échec d’allocation ; dans ce cas, aborter le programme est la réponse la plus simple et la plus propre.  
En d’autres termes : dans la plupart des programmes, la plupart des fonctions peuvent lancer (par ex. parce qu’elles utilisent `new`, appellent des fonctions qui le font, ou utilisent des bibliothèques qui signalent les échecs par des exceptions). N’ajoutez donc pas `noexcept` partout sans réfléchir aux exceptions possibles.

`noexcept` est le plus utile (et le plus clairement correct) pour les fonctions bas‑niveau fréquemment utilisées.

#### Note

Les destructeurs, fonctions `swap`, opérations de déplacement et constructeurs par défaut ne doivent jamais lancer. Voir également [C.44](#rc-default00).

#### Note

Il faut faire attention aux fonctions virtuelles et aux fonctions publiques : déclarer `noexcept` constitue une garantie que toutes les implémentations présentes et futures devront respecter. Pour une fonction virtuelle, tous les redéfinisseurs doivent également être `noexcept`. Supprimer `noexcept` d’une fonction pourrait casser les appels.

#### Application

* (difficile) Signaler les fonctions bas‑niveau qui ne sont pas `noexcept` alors qu’elles ne peuvent pas lancer.  
* Signaler les fonctions `swap`, `move`, destructeurs et constructeurs par défaut qui lancent.

---

### <a name="rf-smart"></a>F.7 : Pour un usage général, prendre des arguments `T*` ou `T&` plutôt que des pointeurs intelligents

#### Raison

Passer un pointeur intelligent transfère ou partage la propriété et ne doit être utilisé que lorsque la sémantique de propriété est intentionnelle.  
Une fonction qui ne manipule pas la durée de vie doit prendre des pointeurs ou références brutes.

Passer un `shared_ptr` restreint l’utilisation de la fonction aux appelants qui utilisent déjà des pointeurs intelligents.  
Une fonction qui a besoin d’un `widget` devrait accepter n’importe quel objet `widget`, pas seulement ceux dont la durée de vie est gérée par un type de pointeur intelligent en particulier.

Passer un `shared_ptr` implique un coût d’exécution.

#### Exemple

    // accepte n’importe quel int*
    void f(int*);

    // n’accepte que les int dont la propriété est transférée
    void g(unique_ptr<int>);

    // n’accepte que les int dont la propriété est partagée
    void g(shared_ptr<int>);

    // ne change pas la propriété, mais impose une propriété particulière du côté appelant
    void h(const unique_ptr<int>&);

    // accepte n’importe quel int
    void h(int&);

#### Exemple, mauvais

    // callee
    void f(shared_ptr<widget>& w)
    {
        // …
        use(*w); // la seule utilisation de w – la durée de vie n’est pas du tout utilisée
        // …
    };

    // caller
    shared_ptr<widget> my_widget = /* … */;
    f(my_widget);

    widget stack_widget;
    f(stack_widget); // erreur

#### Exemple, bon

    // callee
    void f(widget& w)
    {
        // …
        use(w);
        // …
    };

    // caller
    shared_ptr<widget> my_widget = /* … */;
    f(*my_widget);

    widget stack_widget;
    f(stack_widget); // ok – fonctionne maintenant

#### Note

Nous pouvons détecter de nombreux cas courants de pointeurs pendants statiquement (voir le [profil de sécurité de durée de vie](#ss-lifetime)). Les arguments de fonction vivent naturellement pendant l’appel, ce qui réduit les problèmes de durée de vie.

#### Application

* (Simple) Avertir si une fonction prend un paramètre de type pointeur intelligent (qui surcharge `operator->` ou `operator*`) qui est copiable, mais la fonction se contente d’appeler `operator*`, `operator->` ou `get()`. Suggérer d’utiliser `T*` ou `T&` à la place.  
* Signaler un paramètre de type pointeur intelligent copiable/movable qui n’est jamais copié/moved dans le corps, qui n’est jamais modifié et qui n’est jamais passé à une autre fonction qui pourrait le faire. Cela signifie que la sémantique de propriété n’est pas utilisée. Suggérer `T*` ou `T&`.

**Voir aussi** :

* [Préférer `T*` à `T&` quand « pas d’argument » est une option valide](#rf-ptr-ref)  
* [Résumé des règles des pointeurs intelligents](#rr-summary-smartptrs)

---

### <a name="rf-pure"></a>F.8 : Privilégier les fonctions pures

#### Raison

Les fonctions pures sont plus faciles à raisonner, parfois plus faciles à optimiser (et même à paralléliser), et peuvent parfois être mémorisées.

#### Exemple

    template<class T>
    auto square(T t) { return t * t; }

#### Application

Non applicable automatiquement.

---

### <a name="rf-unused"></a>F.9 : Les paramètres inutilisés doivent être non nommés

#### Raison

Lisibilité.  
Évite les avertissements de paramètres inutilisés.

#### Exemple

    widget* find(const set<widget>& s, const widget& w, Hint);   // jadis, un hint était utilisé

#### Note

Autoriser les paramètres non nommés a été introduit au début des années 80 pour résoudre ce problème.

Si des paramètres sont conditionnellement inutilisés, déclarez‑les avec l’attribut `[[maybe_unused]]`. Exemple :

    template <typename Value>
    Value* find(const set<Value>& s, const Value& v, [[maybe_unused]] Hint h)
    {
        if constexpr (sizeof(Value) > CacheSize)
        {
            // le hint n’est utilisé que si Value a une certaine taille
        }
    }

#### Application

Signaler les paramètres nommés qui ne sont jamais utilisés.

---

### <a name="rf-name"></a>F.10 : Si une opération peut être réutilisée, lui donner un nom

#### Raison

Documentation, lisibilité, opportunité de réutilisation.

#### Exemple

    struct Rec {
        string name;
        string addr;
        int id;         // identifiant unique
    };

    bool same(const Rec& a, const Rec& b)
    {
        return a.id == b.id;
    }

    vector<Rec*> find_id(const string& name);    // trouver tous les enregistrements pour « name »

    auto x = find_if(vr.begin(), vr.end(),
        [&](Rec& r) {
            if (r.name.size() != n.size()) return false; // le nom à comparer est dans n
            for (int i = 0; i < r.name.size(); ++i)
                if (tolower(r.name[i]) != tolower(n[i])) return false;
            return true;
        }
    );

Il y a une fonction utile cachée ici (comparaison de chaînes insensible à la casse), comme cela arrive souvent lorsque les arguments lambda deviennent très gros.

    bool compare_insensitive(const string& a, const string& b)
    {
        if (a.size() != b.size()) return false;
        for (int i = 0; i < a.size(); ++i) if (tolower(a[i]) != tolower(b[i])) return false;
        return true;
    }

    auto x = find_if(vr.begin(), vr.end(),
        [&](Rec& r) { return compare_insensitive(r.name, n); }
    );

Ou encore (si vous préférez éviter la liaison implicite à `n`) :

    auto cmp_to_n = [&n](const string& a) { return compare_insensitive(a, n); };
    auto x = find_if(vr.begin(), vr.end(),
        [](const Rec& r) { return cmp_to_n(r.name); }
    );

#### Note

Peu importe que ce soit des fonctions, des lambdas ou des opérateurs.

#### Exception

* Les lambdas logiquement utilisées uniquement localement, comme argument à `for_each` et à d’autres algorithmes de contrôle.  
* Les lambdas comme [initialisateurs](#???).

#### Application

* (difficile) Signaler les lambdas similaires.  
* ??? (non spécifié)

---

### <a name="rf-lambda"></a>F.11 : Utiliser une lambda anonyme si vous avez besoin d’un simple objet fonctionnel en un seul lieu

#### Raison

Cela rend le code concis et donne une meilleure localisation que les alternatives.

#### Exemple

    auto earlyUsersEnd = std::remove_if(users.begin(), users.end(),
                                        [](const User &a) { return a.id > 100; });

#### Exception

Nommer une lambda peut être utile pour la clarté même si elle n’est utilisée qu’une fois.

#### Application

* Rechercher les lambdas identiques ou quasi‑identiques (à remplacer par des fonctions nommées ou des lambdas nommées).

---

## <a name="ss-call"></a>F.call : Passage de paramètres

Il existe une variété de manières de passer des paramètres à une fonction et de retourner des valeurs.

### <a name="rf-conventional"></a>F.15 : Préférer des façons simples et conventionnelles de transmettre l’information

#### Raison

Utiliser des techniques « inhabituelles et astucieuses » provoque des surprises, ralentit la compréhension par d’autres programmeurs et favorise les bugs.  
Si vous avez réellement besoin d’une optimisation au‑delà des techniques courantes, mesurez pour vous assurer que cela apporte réellement un gain, et documentez/commentairez car l’amélioration pourrait ne pas être portable.

Les tableaux suivants résument les conseils des sections suivantes : F.16‑21.

**Passage de paramètres « normal »**  

![Tableau du passage de paramètres normal](./param-passing-normal.png "Passage de paramètres normal")

**Passage de paramètres « avancé »**  

![Tableau du passage de paramètres avancé](./param-passing-advanced.png "Passage de paramètres avancé")

N’utilisez les techniques avancées qu’après avoir démontré le besoin, et commentez ce besoin.

Pour le passage de séquences de caractères, voir [String](#ss-string).

#### Exception

Pour exprimer le partage de propriété à l’aide de `shared_ptr`, au lieu de suivre les lignes directrices F.16‑21, suivez [R.34](#rr-sharedptrparam-owner), [R.35](#rr-sharedptrparam) et [R.36](#rr-sharedptrparam-const).

---

### <a name="rf-in"></a>F.16 : Pour les paramètres « in », passer les types à copie bon marché par valeur et les autres par référence `const`

#### Raison

Les deux indiquent à l’appelant que la fonction ne modifiera pas l’argument, et les deux permettent l’initialisation à partir de r‑values.

Ce qui est « cheap to copy » dépend de l’architecture, mais deux ou trois mots (doubles, pointeurs, références) sont généralement passés par valeur.  
Lorsque la copie est bon marché, rien ne bat la simplicité et la sécurité de la copie, et pour les petits objets (jusqu’à deux ou trois mots) c’est même plus rapide que de passer par référence, car cela évite une indirection supplémentaire.

#### Exemple

    void f1(const string& s);  // OK : passage par référence `const`; toujours bon marché
    void f2(string s);         // mauvais : potentiellement coûteux
    void f3(int x);            // OK : imbattable
    void f4(const int& x);     // mauvais : surcharge d’accès dans f4()

Pour les usages avancés (seulement) où vous devez vraiment optimiser les r‑values passées à des paramètres « in‑only » :

* Si la fonction doit inconditionnellement déplacer l’argument, prenez‑le par `&&`. Voir [F.18](#rf-consume).  
* Si la fonction garde une copie locale modifiable uniquement pour son propre usage, le prendre par valeur est acceptable.  
* Si la fonction garde une copie de l’argument pour la transmettre à un autre endroit (autre fonction ou emplacement non local), en plus du passage par `const&` pour les l‑values, ajoutez une surcharge qui prend le paramètre par `&&` (pour les r‑values) et effectuez un `std::move` vers la destination. Ceci correspond à la notion de « will‑move‑from » ; voir [F.18](#rf-consume).  
* Dans les cas particuliers, comme plusieurs paramètres « in + copy », envisagez le forwarding parfait. Voir [F.19](#rf-forward).

#### Exemple

    int multiply(int, int); // uniquement des int d’entrée, passer par valeur

    // le suffixe est uniquement d’entrée mais moins bon marché qu’un int, passer par const&
    string& concatenate(string&, const string& suffix);

    void sink(unique_ptr<widget>);  // uniquement d’entrée, et déplace la propriété du widget

Évitez les techniques « ésotériques » comme passer des arguments en `T&&` « pour l’efficacité ». La plupart des rumeurs sur les avantages de performance du passage par `&&` sont fausses ou fragiles (mais voir [F.18](#rf-consume) et [F.19](#rf-forward)).

#### Notes

Une référence peut être supposée référencer un objet valide (règle du langage).  
Il n’existe pas de « référence nulle ».  
Si vous avez besoin d’une valeur optionnelle, utilisez un pointeur, `std::optional` ou une valeur spéciale désignant « pas de valeur ».

#### Application

* (Simple) ((Fondation)) Avertir lorsqu’un paramètre passé par valeur dépasse `4 * sizeof(void*)`. Suggérer de le passer par référence `const`.  
* (Simple) ((Fondation)) Avertir lorsqu’un paramètre passé par référence `const` est de taille ≤ `2 * sizeof(void*)`. Suggérer de le passer par valeur.  
* (Simple) ((Fondation)) Avertir lorsqu’un paramètre passé par référence `const` est `move`d.  
* (Pas simple) Note : une application plus stricte dépendrait des caractéristiques de performance de l’architecture ciblée.

#### Exception

Pour exprimer le partage de propriété à l’aide de `shared_ptr`, suivez [R.34](#rr-sharedptrparam-owner) ou [R.36](#rr-sharedptrparam-const), selon que la fonction prend ou non inconditionnellement une référence à l’argument.

---

### <a name="rf-inout"></a>F.17 : Pour les paramètres « in‑out », passer par référence non‑`const`

#### Raison

Cela indique clairement à l’appelant que l’objet doit être modifié.

#### Exemple

    void update(Record& r);  // on suppose que update écrit dans r

#### Note

Certains types définis par l’utilisateur et la bibliothèque standard, comme `span<T>` ou les itérateurs, sont *cheap to copy* (voir <a href="#rf-in">F.16</a>) et peuvent être passés par valeur tout en conservant une sémantique mutable « in‑out » :

    void increment_all(span<int> a)
    {
      for (auto&& e : a)
        ++e;
    }

#### Note

Un paramètre `T&` peut transmettre de l’information dans une fonction ainsi qu’en extraire ; il peut donc être un paramètre « in‑out ». Cela peut en soi poser problème :

    void f(string& s)
    {
        s = "New York";  // erreur non évidente
    }

    void g()
    {
        string buffer = "................................";
        f(buffer);
        // …
    }

Ici, l’auteur de `g()` fournit un tampon à `f()` pour le remplir, mais `f()` le remplace simplement (à un coût légèrement supérieur à une copie simple de caractères). Une mauvaise logique peut survenir si l’auteur de `g()` suppose à tort la taille du tampon.

#### Application

* (Modéré) ((Fondation)) Avertir des fonctions qui prennent une référence non‑`const` et qui **ne** l’écrivent **pas**.  
* (Simple) ((Fondation)) Avertir lorsqu’un paramètre non‑`const` passé par référence est `move`d.

---

### <a name="rf-consume"></a>F.18 : Pour les paramètres « will‑move‑from », les passer par `X&&` et les `std::move` dans la fonction

#### Raison

C’est efficace et élimine les bugs au point d’appel : `X&&` ne lie qu’aux r‑values, ce qui impose un `std::move` explicite au point d’appel si l’on passe un l‑value.

#### Exemple

    void sink(vector<int>&& v)  // sink prend possession de ce que possède l’argument
    {
        // généralement il y aura des accès const à v ici
        store_somewhere(std::move(v));
        // généralement plus aucun usage de v ici ; il est déplacé
    }

Notez que le `std::move(v)` permet à `store_somewhere()` de laisser `v` dans un état déplacé.  
[Cela peut être dangereux](#rc-move-semantic).

#### Exception

Les types propriétaires uniques qui sont uniquement déplaçables et bon marché à déplacer, comme `unique_ptr`, peuvent aussi être passés par valeur ; c’est plus simple à écrire et produit le même effet. Passer par valeur génère une opération de déplacement supplémentaire (mais bon marché) ; privilégiez la simplicité et la clarté d’abord.

Exemple :

    template<class T>
    void sink(std::unique_ptr<T> p)
    {
        // utilisation de p … éventuellement std::move(p) plus loin
    }   // p est détruit

#### Exception

Si le paramètre « will‑move‑from » est un `shared_ptr`, suivez [R.34](#rr-sharedptrparam-owner) et passez le `shared_ptr` par valeur.

#### Application

* Signaler tous les paramètres `X&&` (où `X` n’est pas un nom de paramètre de modèle) dont le corps de fonction les utilise sans `std::move`.  
* Signaler l’accès à des objets déjà déplacés.  
* Ne pas déplacer conditionnellement des objets.

---

### <a name="rf-forward"></a>F.19 : Pour les paramètres « forward », les passer par `TP&&` et ne les `std::forward` qu’une fois

#### Raison

Si l’objet doit être transmis à d’autres code et n’est pas utilisé directement par la fonction, on veut que la fonction soit agnostique du const‑ness et du r‑value‑ness de l’argument.  
Dans ce cas, et seulement dans ce cas, on déclare le paramètre `TP&&` où `TP` est un paramètre de modèle ; cela *ignore* et *préserve* le const‑ness et le r‑value‑ness. Ainsi, tout code qui utilise `TP&&` indique implicitement qu’il ne se soucie pas du const‑ness / r‑value‑ness, mais qu’il a l’intention de transmettre la valeur à un autre code qui, lui, s’en soucie (car il la préserve). Lorsqu’il est utilisé comme paramètre, `TP&&` doit être transmis via `std::forward` exactement une fois sur chaque chemin d’exécution statique.

#### Exemple

    template<class F, class... Args>
    inline decltype(auto) invoke(F&& f, Args&&... args)
    {
        return forward<F>(f)(forward<Args>(args)...);
    }

#### Exemple (forward partiel)

    template<class PairLike>
    inline auto test(PairLike&& pairlike)
    {
        // …
        f1(some, args, and, forward<PairLike>(pairlike).first);           // forward .first
        f2(and, forward<PairLike>(pairlike).second, in, another, call);   // forward .second
    }

#### Application

* Signaler une fonction qui prend un paramètre `TP&&` (où `TP` est un nom de paramètre de modèle) et en fait autre chose que le `std::forward` exactement une fois sur chaque chemin d’exécution statique, ou qui le `std::forward` plus d’une fois mais avec un membre de données différent à chaque fois.

---

### <a name="rf-out"></a>F.20 : Pour les valeurs de sortie, préférer les valeurs de retour aux paramètres de sortie

#### Raison

Une valeur de retour est auto‑documentante, alors qu’un `&` peut être à la fois « in‑out » ou « out » et être sujet à mauvaise utilisation.

Cela inclut les objets volumineux comme les conteneurs standards qui utilisent les déplacements implicites pour la performance et pour éviter la gestion explicite de la mémoire.

Si vous avez plusieurs valeurs à retourner, utilisez un `tuple` (voir <a href="#rf-out-multi">F.21</a>) ou un type multi‑membres similaire.

#### Exemple

    // OK : retourne des pointeurs vers les éléments avec la valeur x
    vector<const int*> find_all(const vector<int>&, int x);

    // Mauvais : place des pointeurs vers les éléments avec la valeur x dans un paramètre in‑out
    void find_all(const vector<int>&, vector<const int*>& out, int x);

#### Note

Une `struct` contenant de nombreux éléments (chacun individuellement bon marché à déplacer) peut être coûteuse à déplacer en agrégat.

#### Exceptions

* Pour les types non concrets, comme les types d’une hiérarchie de classes, retourner l’objet par `unique_ptr` ou `shared_ptr`.  
* Si un type est coûteux à déplacer (ex. `array<BigTrivial>`), envisagez de l’allouer sur le tas et de retourner un handle (ex. `unique_ptr`), ou de le passer par référence non‑`const` à remplir (à utiliser comme paramètre de sortie).  
* Pour réutiliser un objet qui porte une capacité (ex. `std::string`, `std::vector`) à travers plusieurs appels de fonction dans une boucle interne : [le traiter comme un paramètre in/out et le passer par référence](#rf-out-multi).

#### Exemple

Supposons que `Matrix` possède des opérations de déplacement (en gardant ses éléments dans un `std::vector`) :

    Matrix operator+(const Matrix& a, const Matrix& b)
    {
        Matrix res;
        // … remplir res avec la somme …
        return res;
    }

    Matrix x = m1 + m2;  // constructeur de déplacement

    y = m3 + m3;         // assignation de déplacement

#### Note

L’optimisation du retour de valeur (RVO) ne s’applique pas au cas d’assignation, mais l’assignation de déplacement le fait.

#### Exemple (objet coûteux à déplacer)

    struct Package {      // cas exceptionnel : objet coûteux à déplacer
        char header[16];
        char load[2024 - 16];
    };

    Package fill();       // Mauvais : grande valeur de retour
    void fill(Package&);  // OK

    int val();            // OK
    void val(int&);       // Mauvais : est‑ce que val lit son argument ?

#### Application

* Signaler les références à des paramètres non‑`const` qui ne sont pas lues avant d’être écrites et dont le type pourrait être retourné à la place ; elles devraient être des valeurs de retour « out ».

---

### <a name="rf-out-multi"></a>F.21 : Pour retourner plusieurs valeurs « out », préférer renvoyer une `struct`

#### Raison

Une valeur de retour est auto‑documentante comme « valeur uniquement de sortie ».  
Notez que C++ possède effectivement plusieurs valeurs de retour, par convention d’utilisation de types de type tuple (`struct`, `array`, `tuple`, …), éventuellement avec la commodité des *structured bindings* (C++17) au point d’appel.  
Privilégiez un `struct` nommé si possible. Sinon, un `tuple` est pratique dans les modèles variadiques.

#### Exemple

    // MAUVAIS : paramètre de sortie documenté dans un commentaire
    int f(const string& input, /*output only*/ string& output_data)
    {
        // …
        output_data = something();
        return status;
    }

    // BON : auto‑documentant
    struct f_result { int status; string data; };

    f_result f(const string& input)
    {
        // …
        return {status, something()};
    }

La bibliothèque standard C++98 utilisait ce style à certains endroits, en retournant `pair` dans certaines fonctions. Exemple :

    // C++98
    pair<set::iterator, bool> result = my_set.insert("Hello");
    if (result.second)
        do_something_with(result.first);    // solution de contournement

Avec C++17, on peut utiliser les *structured bindings* pour donner un nom à chaque membre :

    if (auto [ iter, success ] = my_set.insert("Hello"); success)
        do_something_with(iter);

Un `struct` avec des noms significatifs est plus courant en C++ moderne. Voir par exemple `ranges::min_max_result`, `from_chars_result`, etc.

#### Exception

Parfois, nous devons passer un objet à une fonction pour manipuler son état. Dans ce cas, passer l’objet par référence `T&` (voir <a href="#rf-inout">F.17</a>) est généralement la bonne technique. Retourner cet « in‑out » comme valeur de retour n’est souvent pas nécessaire. Exemple :

    istream& operator>>(istream& in, string& s);    // très similaire à std::operator>>()

    for (string s; in >> s; ) {
        // … faire quelque chose avec la ligne
    }

Ici, `in` et `s` sont utilisés comme paramètres « in‑out ». Nous passons `in` par référence non‑`const` pour pouvoir modifier son état. Nous passons `s` pour éviter des allocations répétées. En réutilisant `s` (passé par référence), nous n’allouons de nouvelles mémoires que lorsque nous devons étendre la capacité de `s`. Cette technique s’appelle parfois le *caller‑allocated out* et est particulièrement utile pour les types comme `string` et `vector` qui nécessitent des allocations sur le tas.

En comparaison, si nous retournions toutes les valeurs, le code serait moins élégant :

    struct get_string_result { istream& in; string s; };

    get_string_result get_string(istream& in)  // non recommandé
    {
        string s;
        in >> s;
        return { in, move(s) };
    }

    for (auto [in, s] = get_string(cin); in; s = get_string(in).s) {
        // … faire quelque chose avec la chaîne
    }

Nous considérons cela nettement moins élégant et moins performant.

Pour une lecture stricte de cette règle (F.21), l’exception n’est pas réellement une exception car elle repose sur des paramètres « in‑out », pas sur les simples paramètres de sortie mentionnés dans la règle. Nous préférons toutefois être explicites plutôt que subtils.

#### Note

Dans la plupart des cas, il est utile de retourner un type défini par l’utilisateur. Exemple :

    struct Distance {
        int value;
        int unit = 1;   // 1 signifie mètres
    };

    Distance d1 = measure(obj1);        // accéder à d1.value et d1.unit
    auto d2 = measure(obj2);            // même chose
    auto [value, unit] = measure(obj3); // accéder à value et unit ; assez redondant pour ceux qui connaissent `measure()`
    auto [x, y] = measure(obj4);        // pas conseillé : risque de confusion

Le `pair` ou `tuple` trop génériques ne doivent être employés que lorsque la valeur retournée représente des entités indépendantes plutôt qu’une abstraction.

Une autre option consiste à utiliser `optional<T>` ou `expected<T, error_code>` plutôt que `pair` ou `tuple`. Lorsqu’ils sont employés correctement, ces types communiquent davantage d’informations sur la signification des membres que `pair<T, bool>` ou `pair<T, error_code>`.

#### Note

Lorsque l’objet à retourner est initialisé à partir de variables locales coûteuses à copier, un `move` explicite peut aider à éviter les copies :

    pair<LargeObject, LargeObject> f(const string& input)
    {
        LargeObject large1 = g(input);
        LargeObject large2 = h(input);
        // …
        return { move(large1), move(large2) }; // aucune copie
    }

ou bien simplement :

    pair<LargeObject, LargeObject> f(const string& input)
    {
        // …
        return { g(input), h(input) }; // aucune copie, aucun déplacement
    }

Notez que cela diffère du anti‑pattern `return move(...)` décrit dans [ES.56](#res-move).

#### Application

* Les paramètres de sortie doivent être remplacés par des valeurs de retour.  
  Un paramètre de sortie est celui que la fonction écrit, qui invoque une fonction membre non‑`const`, ou qui le transmet à une autre fonction.  
* Les types de retour `pair` ou `tuple` devraient être remplacés par un `struct` lorsque cela est possible.  
  Dans les modèles variadiques, `tuple` reste souvent inévitable.

---

### <a name="rf-ptr-ref"></a>F.60 : Préférer `T*` à `T&` quand « pas d’argument » est une option valide

#### Raison

Un pointeur (`T*`) peut être `nullptr` alors qu’une référence (`T&`) ne le peut pas ; il n’existe pas de « référence nulle » valide.  
Parfois, disposer d’un `nullptr` comme alternative pour indiquer « pas d’objet » est utile ; si ce n’est pas le cas, une référence est plus simple à écrire et peut produire un meilleur code.

#### Exemple

    string zstring_to_string(zstring p) // zstring est un `char*` ; c’est une chaîne C‑style
    {
        if (!p) return string{};    // p peut être nullptr ; n’oubliez pas de vérifier
        return string{p};
    }

    void print(const vector<int>& r)
    {
        // r réfère à un `vector<int>` ; pas de vérification nécessaire
    }

#### Note

Il est possible, mais non valide en C++, de construire une référence qui est essentiellement un `nullptr` (ex. `T* p = nullptr; T& r = *p;`). Cette erreur est très rare.

#### Note

Si vous préférez la notation pointeur (`->` et/ou `*` vs. `.`), `not_null<T*>` offre les mêmes garanties qu’une référence `T&`.

#### Application

* Signaler ??? (non spécifié)

---

### <a name="rf-ptr"></a>F.22 : Utiliser `T*` ou `owner<T*>` pour désigner un objet unique

#### Raison

Lisibilité : cela rend explicite le sens d’un pointeur nu.  
Permet un soutien important des outils.

#### Note

Dans le code C et C++ traditionnel, le `T*` nu est utilisé pour de nombreux usages faiblement liés, comme :

* Identifier un (seul) objet (pas à supprimer par cette fonction)  
* Pointer vers un objet alloué sur le tas (et à le `delete` plus tard)  
* Contenir le `nullptr`  
* Identifier une chaîne de style C (tableau de caractères zéro‑terminé)  
* Identifier un tableau dont la longueur est spécifiée séparément  
* Identifier une position dans un tableau

Cela rend difficile la compréhension du but du code et complique la vérification et le soutien des outils.

#### Exemple

    void use(int* p, int n, char* s, int* q)
    {
        p[n - 1] = 666; // mauvais : on ne sait pas si p pointe sur n éléments ; utiliser `span<int>` serait préférable
        cout << s;      // mauvais : on ne sait pas si s pointe sur une chaîne zéro‑terminée ; utiliser `zstring` serait préférable
        delete q;       // mauvais : on ne sait pas si *q a été alloué sur le tas ; utiliser `owner` serait préférable
    }

Meilleure version :

    void use2(span<int> p, zstring s, owner<int*> q)
    {
        p[p.size() - 1] = 666; // OK, une erreur de portée peut être détectée
        cout << s; // OK
        delete q; // OK
    }

#### Note

`owner<T*>` représente la propriété, `zstring` représente une chaîne de style C.

**Aussi** : on suppose qu’un `T*` obtenu à partir d’un pointeur intelligent (`unique_ptr<T>`) pointe vers un seul élément.

**Voir aussi** : [bibliothèque de support](#gsl-guidelines-support-library)  
**Voir aussi** : [Ne pas passer un tableau comme un seul pointeur](#ri-array)

#### Application

* (Simple) ((Bounds)) Avertir toute opération arithmétique sur une expression de type pointeur qui aboutit à une valeur de type pointeur.

---

### <a name="rf-nullptr"></a>F.23 : Utiliser un `not_null<T>` pour indiquer que « null » n’est pas une valeur valide

#### Raison

Clarté. Un paramètre `not_null<T>` indique clairement que l’appelant est responsable de toute vérification de `nullptr` nécessaire. De même, une fonction qui retourne `not_null<T>` indique que l’appelant n’a pas besoin de vérifier `nullptr`.

#### Exemple

`not_null<T*>` rend évident pour le lecteur (humain ou machine) qu’un test `nullptr` n’est pas nécessaire avant la déréférenciation. De plus, en mode débogage, `owner<T*>` et `not_null<T>` peuvent être instrumentés pour vérifier la conformité.

Considérez :

    int length(Record* p);

Lorsque j’appelle `length(p)`, dois‑je vérifier si `p` est `nullptr` ?  
L’implémentation de `length()` doit‑elle vérifier ?  

    // c’est au travailleur de s’assurer que p != nullptr
    int length(not_null<Record*> p);

    // l’implémenteur de length() doit supposer que p peut être nullptr
    int length(Record* p);

#### Note

Un `not_null<T*>` est supposé ne jamais être `nullptr` ; un `T*` *peut* être `nullptr` ; les deux peuvent être représentés en mémoire de la même façon, donc aucun coût d’exécution supplémentaire n’est implicite.

#### Note

`not_null` ne concerne pas seulement les pointeurs natifs. Il fonctionne également avec `unique_ptr`, `shared_ptr` et d’autres types ressemblant à des pointeurs.

#### Application

* (Simple) Avertir si un pointeur brut est déréférencé sans être testé contre `nullptr` (ou équivalent) dans une fonction, et suggérer de le déclarer `not_null`.  
* (Simple) Erreur si un pointeur brut est parfois déréférencé après avoir été testé contre `nullptr` et parfois pas dans la même fonction.  
* (Simple) Avertir si un pointeur `not_null` est testé contre `nullptr` dans une fonction.

---

### <a name="rf-range"></a>F.24 : Utiliser un `span<T>` ou un `span_p<T>` pour désigner une séquence demi‑ouverte

#### Raison

Les plages informelles/non explicites sont une source d’erreurs.

#### Exemple

    X* find(span<X> r, const X& v);    // recherche v dans r

    vector<X> vec;
    // …
    auto p = find({vec.begin(), vec.end()}, X{});  // recherche X{} dans vec

#### Note

Les plages sont extrêmement courantes en C++. Elles sont souvent implicites et leur utilisation correcte est très difficile à garantir. En particulier, pour une paire d’arguments `(p, n)` désignant un tableau `[p:p+n)`, il est généralement impossible de savoir s’il y a réellement `n` éléments accessibles après `*p`. `span<T>` et `span_p<T>` sont des aides simples désignant respectivement une plage `[p:q)` et une plage qui commence à `p` et se termine au premier élément satisfaisant un prédicat.

#### Exemple

Un `span` représente une collection d’éléments, mais comment manipuler les éléments de cette plage ?

    void f(span<int> s)
    {
        // itération de plage (garantie correcte)
        for (int x : s) cout << x << '\n';

        // itération C‑style (potentiellement vérifiée)
        for (gsl::index i = 0; i < s.size(); ++i) cout << s[i] << '\n';

        // accès aléatoire (potentiellement vérifié)
        s[7] = 9;

        // extraction de pointeurs (potentiellement vérifiée)
        std::sort(&s[0], &s[s.size() / 2]);
    }

#### Note

Un objet `span<T>` ne possède pas les éléments et est si petit qu’il peut être passé par valeur.

Passer un `span` comme argument est aussi efficace que de passer deux pointeurs ou un pointeur et un entier de comptage.

**Voir aussi** : [bibliothèque de support](#gsl-guidelines-support-library)

#### Application

(Complexe) Signaler les accès à des paramètres pointeur qui sont bornés par d’autres paramètres entiers, et suggérer qu’ils pourraient être remplacés par un `span`.

---

### <a name="rf-zstring"></a>F.25 : Utiliser un `zstring` ou un `not_null<zstring>` pour désigner une chaîne de style C

#### Raison

Les chaînes de style C sont omniprésentes. Elles sont définies par convention : tableaux de caractères zéro‑terminés.  
Nous devons les distinguer d’un pointeur vers un caractère unique ou d’un vieux pointeur vers un tableau de caractères.

Si vous n’avez pas besoin de la terminaison nulle, utilisez `string_view`.

#### Exemple

    int length(const char* p);

Quand j’appelle `length(s)`, dois‑je vérifier si `s` est `nullptr` ? L’implémentation de `length()` doit‑elle vérifier si `p` est `nullptr` ?

    // l’implémenteur de length() doit supposer que p peut être nullptr
    int length(zstring p);

    // c’est au travailleur de s’assurer que p != nullptr
    int length(not_null<zstring> p);

#### Note

`zstring` ne représente pas la propriété.

**Voir aussi** : [bibliothèque de support](#gsl-guidelines-support-library)

---

### <a name="rf-unique_ptr"></a>F.26 : Utiliser un `unique_ptr<T>` pour transférer la propriété lorsqu’un pointeur est nécessaire

#### Raison

Utiliser `unique_ptr` est le moyen le plus économique de passer un pointeur en toute sécurité.

**Voir aussi** : [C.50](#rc-factory) concernant le moment où il faut retourner un `shared_ptr` depuis une factory.

#### Exemple

    unique_ptr<Shape> get_shape(istream& is)  // assembler la forme depuis le flux d’entrée
    {
        auto kind = read_header(is); // lire l’en‑tête et identifier la forme suivante dans l’entrée
        switch (kind) {
        case kCircle:
            return make_unique<Circle>(is);
        case kTriangle:
            return make_unique<Triangle>(is);
        // …
        }
    }

#### Note

Vous avez besoin de passer un pointeur plutôt qu’un objet si ce que vous transférez provient d’une hiérarchie de classes à utiliser via une interface (classe de base).

#### Application

(Simple) Avertir lorsqu’une fonction retourne un pointeur brut alloué localement. Suggérer d’utiliser `unique_ptr` ou `shared_ptr` à la place.

---

### <a name="rf-shared_ptr"></a>F.27 : Utiliser un `shared_ptr<T>` pour partager la propriété

#### Raison

`std::shared_ptr` est la façon standard de représenter le partage de propriété. Le dernier propriétaire détruit l’objet.

#### Exemple

    {
        shared_ptr<const Image> im { read_image(somewhere) };

        std::thread t0 {shade, args0, top_left, im};
        std::thread t1 {shade, args1, top_right, im};
        std::thread t2 {shade, args2, bottom_left, im};
        std::thread t3 {shade, args3, bottom_right, im};

        // détacher les threads demande un soin supplémentaire (ex. join avant la fin de main),
        // mais même si nous détachons les quatre threads ici …
    }
    // … le shared_ptr garantit que, finalement, le dernier thread à finir supprime l’image

#### Note

Privilégiez `unique_ptr` lorsqu’il n’y a jamais plus d’un propriétaire à la fois. `shared_ptr` est réservé au partage.

Notez que l’usage généralisé de `shared_ptr` a un coût : les opérations atomiques sur le compteur de référence ajoutent une surcharge mesurable.

#### Alternative

Faire en sorte qu’un seul objet possède l’objet partagé (ex. un objet à portée limitée) et le détruire (de préférence implicitement) lorsque tous les utilisateurs ont terminé.

#### Application

(Not enforceable) Ce motif est trop complexe pour être détecté de façon fiable.

---

### <a name="rf-return-ptr"></a>F.42 : Retourner un `T*` pour indiquer uniquement une position (pas de transfert de propriété)

#### Raison

C’est à quoi les pointeurs servent. Retourner un `T*` pour transférer la propriété est un mauvais usage.

#### Exemple

    Node* find(Node* t, const string& s)  // recherche s dans un arbre binaire de nœuds
    {
        if (!t || t->name == s) return t;
        if ((auto p = find(t->left, s))) return p;
        if ((auto p = find(t->right, s))) return p;
        return nullptr;
    }

Si ce n’est pas `nullptr`, le pointeur retourné indique simplement le `Node` contenant `s`.  
Important : cela ne signifie pas un transfert de propriété du nœud vers l’appelant.

#### Note

Les positions peuvent aussi être transmises par itérateurs, indices ou références. Une référence est souvent une alternative supérieure à un pointeur si `nullptr` n’est pas nécessaire ([F.60](#rf-ptr-ref)) ou si l’objet référencé ne doit pas changer ([s-const](#s-const)).

#### Note

Ne pas retourner un pointeur vers quelque chose qui n’est pas dans la portée de l’appelant ; voir <a href="#rf-dangle">F.43</a>.

**Voir aussi** : [discussion sur la prévention des pointeurs pendants](#???)

#### Application

* Signaler les appels à `delete`, `std::free()`, etc. appliqués à un `T*` simple. Seuls les propriétaires doivent être supprimés.  
* Signaler les appels à `new`, `malloc()`, etc. assignés à un `T*` simple. Seuls les propriétaires doivent être responsables de la suppression.

---

### <a name="rf-dangle"></a>F.43 : Ne jamais (directement ou indirectement) retourner un pointeur ou une référence à un objet local

#### Raison

Éviter les plantages et la corruption de données qui peuvent résulter de l’utilisation d’un tel pointeur pendante.

#### Exemple, mauvais

Après le retour d’une fonction, ses objets locaux n’existent plus :

    int* f()
    {
        int fx = 9;
        return &fx;  // MAUVAIS
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
        int z = *p;  // lecture d’une pile abandonnée (mauvais)
        g(p);        // passer le pointeur d’une pile abandonnée à une fonction (mauvais)
    }

Sur une implémentation populaire, la sortie était :

    *p == 999
    gx == 999

On s’attendrait à ce que, parce que l’appel à `g()` réutilise la pile abandonnée par `f()`, `*p` fasse référence à l’espace maintenant occupé par `gx`.

* Imaginez ce qui arriverait si `fx` et `gx` étaient de types différents.  
* Imaginez ce qui arriverait si `fx` ou `gx` était un type avec invariant.  
* Imaginez ce qui arriverait si ce pointeur pendante était propagé à travers un plus grand ensemble de fonctions.  
* Imaginez ce qu’un attaquant pourrait faire avec ce pointeur pendante.

Heureusement, la plupart (toutes ?) les compilations modernes détectent et préviennent ce cas simple.

#### Note

Cela s’applique aussi aux références :

    int& f()
    {
        int x = 7;
        // …
        return x;  // Mauvais : retourne une référence à un objet qui va bientôt être détruit
    }

#### Note

Cela ne s’applique qu’aux variables locales **non‑`static`**. Toutes les variables `static` sont, comme leur nom l’indique, allouées statiquement, donc les pointeurs vers elles ne peuvent pas pendre.

#### Exemple, mauvais (moins évident)

    int* glob;       // les variables globales sont mauvaises à bien des égards

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

Ici, on lit l’emplacement abandonné par l’appel à `f`. Le pointeur stocké dans `glob` pourrait être utilisé bien plus tard et causer des problèmes imprévisibles.

#### Note

L’adresse d’une variable locale peut être « retournée »/fuyante via une instruction `return`, un paramètre de sortie `T&`, comme membre d’un objet retourné, comme élément d’un tableau retourné, etc.

#### Note

Des exemples similaires peuvent être construits en « fuyant » un pointeur d’une portée intérieure vers une portée extérieure ; ces cas sont traités de façon équivalente aux fuites de pointeurs hors d’une fonction.

Une variante légèrement différente du problème consiste à placer des pointeurs dans un conteneur qui survit plus longtemps que les objets pointés.

**Voir aussi** : une autre façon d’obtenir des pointeurs pendantes est la [invalidation de pointeur](#???). Elle peut être détectée/prévenue par des techniques similaires.

#### Application

* Les compilateurs détectent généralement le retour de référence vers des locaux et, dans de nombreux cas, le retour de pointeur vers des locaux.  
* L’analyse statique peut repérer de nombreux schémas courants d’utilisation de pointeurs indiquant des positions (éliminant ainsi les pointeurs pendantes).

---

### <a name="rf-return-ref"></a>F.44 : Retourner un `T&` quand la copie est indésirable et que « ne rien retourner » n’est pas nécessaire

#### Raison

Le langage garantit qu’un `T&` référencie un objet, donc il n’est pas nécessaire de tester `nullptr`.

**Voir aussi** : le retour d’une référence ne doit pas impliquer un transfert de propriété : [discussion sur la prévention des pointeurs pendantes](#???) et [discussion sur la propriété](#???).

#### Exemple

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
        wheel& w0 = c.get_wheel(0); // w0 vit aussi longtemps que c
    }

#### Application

Signaler les fonctions où aucune expression de retour ne pourrait produire `nullptr`.

---

### <a name="rf-return-ref-ref"></a>F.45 : Ne pas retourner un `T&&`

#### Raison

Cela revient à retourner une référence à un objet temporaire détruit. Un `&&` attire les objets temporaires.

#### Exemple

Un `T&&` retourné sort du scope à la fin de l’expression complète à laquelle il appartient :

    auto&& x = max(0, 1);   // OK, jusqu’ici
    foo(x);                 // Comportement indéfini

Ce type d’utilisation est une source fréquente de bugs, souvent mal interprétée comme un bug du compilateur. Un implémenteur de fonction doit éviter de poser ce type de piège aux utilisateurs.

Le [profil de sécurité de durée de vie](#ss-lifetime) (lorsqu’il sera pleinement implémenté) détectera ces problèmes.

#### Exemple (cas valable)

Retourner une référence r‑value est acceptable lorsqu’on la passe « vers le bas » à un callee ; le temporaire est alors garanti de survivre à l’appel de la fonction (voir <a href="#rf-consume">F.18</a> et <a href="#rf-forward">F.19</a>).  
Ce n’est pas correct lorsqu’on la passe « vers le haut » vers une portée d’appel plus large.

Pour les fonctions qui transmettent des paramètres (par référence ordinaire ou forwarding) et qui souhaitent retourner des valeurs, utilisez la déduction de type `auto` (pas `auto&&`) :

    template<class F>
    auto wrapper(F f)
    {
        log_call(typeid(f)); // instrumentation éventuelle
        return f();          // OK
    }

#### Exception

`std::move` et `std::forward` renvoient des `&&`, mais ce ne sont que des casts ; ils sont utilisés uniquement dans des contextes d’expression où la référence à un temporaire est immédiatement passée au sein de la même expression avant que le temporaire ne soit détruit. Nous ne connaissons pas d’autres bons exemples de retour de `&&`.

#### Application

Signaler tout usage de `&&` comme type de retour, sauf dans `std::move` et `std::forward`.

---

### <a name="rf-main"></a>F.46 : `int` est le type de retour de `main()`

#### Raison

C’est une règle du langage, mais les « extensions de langage » la violent si souvent qu’il vaut la peine de la rappeler. Déclarer `main` (la fonction globale unique d’un programme) comme `void` limite la portabilité.

#### Exemple

    void main() { /* … */ };  // mauvais, pas du C++

    int main()
    {
        std::cout << "Ceci est la façon correcte\n";
    }

#### Note

Nous mentionnons cela uniquement parce que l’erreur persiste dans la communauté. Notez que, même avec le type de retour non‑void, la fonction `main` n’exige pas une instruction `return` explicite.

#### Application

* Le compilateur devrait déjà la signaler.  
* Si le compilateur ne le fait pas, les outils doivent le relever.

---

### <a name="rf-assignment-op"></a>F.47 : Retourner `T&` depuis les opérateurs d’affectation

#### Raison

La convention pour les surcharges d’opérateurs (en particulier sur les types concrets) est que `operator=(const T&)` réalise l’affectation puis retourne (non‑`const`) `*this`. Cela assure la cohérence avec les types de la bibliothèque standard et suit le principe « faire comme les entiers ».

#### Note

Historiquement, il était parfois recommandé de faire retourner `const T&`. Cela évitait les expressions du type `(a = b) = c`; un tel code n’est pas assez répandu pour justifier une rupture avec la cohérence des types standard.

#### Exemple

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

#### Application

Cette règle doit être appliquée par les outils en vérifiant le type de retour (et la valeur de retour) de tout opérateur d’affectation.

---

### <a name="rf-return-move-local"></a>F.48 : Ne pas `return std::move(local)`

#### Raison

Retourner une variable locale implique déjà son déplacement. Un `std::move` explicite est toujours une pessimisation, car il empêche l’optimisation de retour de valeur (RVO), qui peut éliminer complètement le déplacement.

#### Exemple, mauvais

    S bad()
    {
      S result;
      return std::move(result);
    }

#### Exemple, bon

    S good()
    {
      S result;
      // RVO nommé : élimination du déplacement au mieux, déplacement au pire
      return result;
    }

#### Application

Les outils doivent vérifier l’expression de retour et signaler les cas où `std::move` est utilisé inutilement.

---

### <a name="rf-return-const"></a>F.49 : Ne pas retourner `const T`

#### Raison

Il n’est pas recommandé de retourner une valeur `const`. Ce conseil plus ancien est désormais obsolète ; il n’apporte aucun bénéfice et interfère avec les mouvements.

#### Exemple

    const vector<int> fct();    // mauvais : le `const` ne vaut pas le coup

    void g(vector<int>& vx)
    {
        // …
        fct() = vx;   // empêché par le `const`
        // …
        vx = fct();   // copie coûteuse : le mouvement est supprimé par le `const`
        // …
    }

L’argument en faveur du `const` sur la valeur de retour était qu’il empêche un accès accidentel à un temporaire (très rare). L’argument contre est qu’il empêche (très fréquent) l’utilisation de la sémantique de déplacement.

**Voir aussi** : [F.20, la règle générale sur les valeurs de sortie](#rf-out)

#### Application

* Signaler le retour d’une valeur `const`. Solution : enlever le `const` pour retourner une valeur non `const`.

---

### <a name="rf-capture-vs-overload"></a>F.50 : Utiliser une lambda quand une fonction ne le ferait pas (pour capturer des variables locales ou écrire une fonction locale)

#### Raison

Les fonctions ne peuvent pas capturer de variables locales ni être définies dans une portée locale ; si vous avez besoin de ces capacités, privilégiez une lambda, ou un objet fonctionnel écrit à la main si ce n’est pas possible. D’un autre côté, les lambdas et les objets fonctionnels ne se surchargent pas ; si vous avez besoin de surcharger, privilégiez une fonction (les solutions pour faire surcharger les lambdas sont complexes). Si les deux fonctionnent, privilégiez la fonction ; utilisez l’outil le plus simple nécessaire.

#### Exemple

    // écrire une fonction qui ne doit accepter que int ou string
    // – la surcharge est naturelle
    void f(int);
    void f(const string&);

    // écrire un objet fonctionnel qui doit capturer l’état local et apparaître
    // à l’endroit d’une instruction ou d’une expression – une lambda est naturelle
    vector<work> v = lots_of_work();
    for (int tasknum = 0; tasknum < max; ++tasknum) {
        pool.run([=, &v] {
            /*
            …
            … traiter 1/max‑e partie de v, le morceau tasknum‑e
            …
            */
        });
    }
    pool.join();

#### Exception

Les lambdas génériques offrent une façon concise d’écrire des modèles de fonction et peuvent être utiles même quand un modèle de fonction normal ferait le travail avec un peu plus de syntaxe. Cet avantage disparaîtra probablement lorsqu’une fonction pourra avoir des paramètres de concept.

#### Application

* Avertir de l’usage d’une lambda non générique nommée (ex. `auto x = [](int i) { … };`) qui ne capture rien et apparaît à la portée globale. Écrire une fonction ordinaire à la place.

---

### <a name="rf-default-args"></a>F.51 : Quand un choix existe, privilégier les arguments par défaut aux surcharges

#### Raison

Les arguments par défaut offrent simplement des variantes d’interface à une même implémentation.  
Il n’est pas garanti que l’ensemble de fonctions surchargées implémente exactement la même sémantique. Les arguments par défaut évitent la duplication de code.

#### Note

Il y a un choix entre l’utilisation d’un argument par défaut et la surcharge lorsque les alternatives proviennent d’un même ensemble de types d’arguments.  
Par exemple :

    void print(const string& s, format f = {});

 contre

    void print(const string& s);          // utilise le format par défaut
    void print(const string& s, format f);

Il n’y a pas de choix lorsqu’un ensemble de fonctions effectue une opération sémantiquement équivalente sur différents types ; par ex. :

    void print(const char&);
    void print(int);
    void print(zstring);

#### Voir aussi

[Arguments par défaut pour fonctions virtuelles](#rh-virtual-default-arg)

#### Application

* Avertir lorsqu’un ensemble de surcharges possède un préfixe commun de paramètres (ex. `f(int)`, `f(int, const string&)`, `f(int, const string&, double)`). (Note : revoir l’application si cela devient trop bruyant.)

---

### <a name="rf-reference-capture"></a>F.52 : Privilégier la capture par référence dans les lambdas qui seront utilisées localement, y compris lorsqu’elles sont passées à des algorithmes

#### Raison

Pour l’efficacité et la correction, vous devez presque toujours capturer par référence lorsque vous utilisez la lambda localement. Ceci inclut les algorithmes parallèles locaux qui se rejoignent avant de retourner.

#### Discussion

L’efficacité provient du fait que la plupart des types sont moins chers à transmettre par référence qu’à copier.  
La correction vient du fait que de nombreux appels souhaitent effectuer des effets de bord sur l’objet original au point d’appel ; la capture par valeur empêche cela.

#### Note

Malheureusement, il n’existe pas de façon simple de capturer par référence `const` pour obtenir l’efficacité d’une capture locale tout en empêchant les effets de bord.

#### Exemple (capture par référence locale)

    std::for_each(begin(sockets), end(sockets), [&message](auto& socket)
    {
        socket.send(message);
    });

#### Exemple (pipeline parallèle simple)

    void send_packets(buffers& bufs)
    {
        stage encryptor([](buffer& b) { encrypt(b); });
        stage compressor([&](buffer& b) { compress(b); encryptor.process(b); });
        stage decorator([&](buffer& b) { decorate(b); compressor.process(b); });
        for (auto& b : bufs) { decorator.process(b); }
    }  // bloque automatiquement l’attente de la fin du pipeline

#### Application

* Signaler une lambda qui capture par référence mais est utilisée hors du scope local de la fonction ou passée à une fonction par référence. (Cette règle est approximative, mais elle signale les captures par pointeur, qui sont plus susceptibles d’être stockées par le callee, d’entraîner des écritures sur le tas, d’être retournées, etc. Les règles de durée de vie couvriront également les pointeurs et références qui s’échappent via les lambdas.)

---

### <a name="rf-value-capture"></a>F.53 : Éviter la capture par référence dans les lambdas qui seront utilisées de façon non locale, y compris retournées, stockées sur le tas ou passées à un autre thread

#### Raison

Les pointeurs et références vers des variables locales ne doivent pas survivre au-delà de leur portée. Les lambdas qui capturent par référence constituent un autre moyen de stocker une référence à un objet local, et cela ne doit pas être fait si la lambda (ou une copie) survit au scope.

#### Exemple, mauvais

    int local = 42;

    // On veut une référence à local.
    // Note : après la fin du scope, `local` n’existe plus,
    // donc l’appel à `process()` aura un comportement indéfini !
    thread_pool.queue_work([&] { process(local); });

#### Exemple, bon

    int local = 42;
    // On veut une copie de local.
    // Une copie est faite, donc elle sera toujours disponible pour l’appel.
    thread_pool.queue_work([=] { process(local); });

#### Note

Si une référence non locale doit être capturée, envisagez d’utiliser `unique_ptr` ; cela gère à la fois la durée de vie et la synchronisation.

Si le pointeur `this` doit être capturé, envisagez la capture `[ *this ]`, qui crée une copie de l’objet entier.

#### Application

* (Simple) Avertir lorsqu’une capture‑list contient une référence à une variable locale déclarée.  
* (Complexe) Signaler lorsqu’une capture‑list contient une référence à une variable locale et que la lambda est passée à un contexte non‑`const` et non‑local.

---

### <a name="rf-this-capture"></a>F.54 : Lors de l’écriture d’une lambda qui capture `this` ou tout membre de classe, ne pas utiliser la capture par défaut `[=]`

#### Raison

C’est source de confusion. Écrire `[=]` dans une fonction membre donne l’impression de capturer par valeur, mais capture en réalité les membres de données par référence car il capture le pointeur invisible `this` par valeur. Si c’est ce que vous vouliez, écrivez `this` explicitement.

#### Exemple

    class My_class {
        int x = 0;
        // …

        void f()
        {
            int i = 0;
            // …

            auto lambda = [=] { use(i, x); };   // MAUVAIS : « semble » capturer par valeur
            x = 42;
            lambda(); // appelle use(0, 42);
            x = 43;
            lambda(); // appelle use(0, 43);
            // …

            auto lambda2 = [i, this] { use(i, x); }; // OK, le plus explicite et le moins confus
            // …
        }
    };

#### Note

Si vous voulez capturer une copie de tous les membres de la classe, envisagez le `[ *this ]` de C++17.

#### Application

* Signaler toute capture‑list qui spécifie une capture‑default `[=]` et qui capture aussi `this` (explicitement ou implicitement via l’utilisation de `this` dans le corps).

---

### <a name="f-varargs"></a>F.55 : Ne pas utiliser d’arguments `va_arg`

#### Raison

Lire un `va_arg` suppose que le bon type a réellement été passé. Passer à `va_arg` suppose que le bon type sera lu. C’est fragile : le langage ne peut pas assurer la sécurité, et cela repose entièrement sur la discipline du programmeur.

#### Exemple

    int sum(...)
    {
        // …
        while (/*…*/)
            result += va_arg(list, int); // MAUVAIS, suppose que des int sont passés
        // …
    }

    sum(3, 2); // ok
    sum(3.14159, 2.71828); // MAUVAIS, indéfini

    template<class ...Args>
    auto sum(Args... args) // BON, bien plus flexible
    {
        return (... + args); // expression de pliage C++17
    }

    sum(3, 2); // ok : 5
    sum(3.14159, 2.71828); // ok : ~5.85987

#### Alternatives

* Surcharge  
* Modèles variadiques  
* Arguments `variant`  
* `initializer_list` (homogène)

#### Note

Déclarer un paramètre `...` est parfois utile pour des techniques ne impliquant pas réellement le passage d’arguments, notamment pour déclarer des fonctions « prendre tout » afin de désactiver « tout le reste » dans un ensemble de surcharges ou exprimer un cas de capture dans la métaprogrammation.

#### Application

* Émettre un diagnostic lorsqu’on utilise `va_list`, `va_start` ou `va_arg`.  
* Émettre un diagnostic lorsqu’on passe un argument à une fonction à paramètres variadiques qui n’offre pas de surcharge plus spécifique pour le type de cet argument. Solution : utiliser une fonction différente, ou `[[suppress("type")]]`.

---

### <a name="f-nesting"></a>F.56 : Éviter les imbrications de conditions inutiles

#### Raison

Un nesting peu profond rend le code plus facile à suivre. Cela clarifie aussi l’intention. Il faut placer le code essentiel au niveau le plus extérieur possible, sauf si cela obscurcit l’intention.

#### Exemple (retour précoce)

    // Mauvais : imbrication profonde
    void foo() {
        …
        if (x) {
            computeImportantThings(x);
        }
    }

    // Mauvais : encore un else redondant.
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

#### Exemple (fusion de conditions)

    // Mauvais : imbrication inutile
    void foo() {
        …
        if (x) {
            if (y) {
                computeImportantThings(x);
            }
        }
    }

    // Bon : fusionner les conditions + retour précoce
    void foo() {
        …
        if (!(x && y))
            return;

        computeImportantThings(x);
    }

#### Application

* Signaler un `else` redondant.  
* Signaler une fonction dont le corps n’est qu’une instruction conditionnelle qui englobe un bloc.