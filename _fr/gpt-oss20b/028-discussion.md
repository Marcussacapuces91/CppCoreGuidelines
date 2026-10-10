# <a name="s-discussion"></a>Annexe C : Discussion  
Cette section contient du matériel supplémentaire sur les règles et les ensembles de règles.  
En particulier, nous présentons ici des raisonnements supplémentaires, de plus grands exemples et des discussions d’alternatives.

### <a name="sd-order"></a>Discussion : Définir et initialiser les membres de données dans l’ordre de déclaration  
Les membres de données sont toujours initialisés dans l’ordre dans lequel ils sont déclarés dans la définition de la classe, il faut donc les lister dans cet ordre dans la liste d’initialisation du constructeur. Les placer dans un ordre différent ne fait que rendre le code confus, car le constructeur ne sera pas exécuté dans l’ordre affiché, ce qui peut rendre difficile la détection de bugs dépendants de l’ordre.  

    class Employee {
        string email, first, last;
    public:
        Employee(const char* firstName, const char* lastName);
        // ...
    };

    Employee::Employee(const char* firstName, const char* lastName)
      : first(firstName),
        last(lastName),
        // BAD: first and last not yet constructed
        email(first + "." + last + "@acme.com")
    {}

Dans cet exemple, `email` sera construit avant `first` et `last` car il est déclaré en premier. Cela signifie que son constructeur tentera d’utiliser `first` et `last` trop tôt — pas seulement avant qu’ils soient définis aux valeurs souhaitées, mais avant même qu’ils soient construits.  

Si la définition de la classe et le corps du constructeur se trouvent dans des fichiers séparés, l’influence à longue distance que l’ordre des déclarations des membres de données a sur la validité du constructeur sera encore plus difficile à repérer.  

**Références** :  

- [Cline99](#Cline99) @TODO-LINK §22.03-11, [Dewhurst03](#Dewhurst03) @TODO-LINK §52-53, [Koenig97](#Koenig97) @TODO-LINK §4, [Lakos96](#Lakos96) @TODO-LINK §10.3.5, [Meyers97](#Meyers97) @TODO-LINK §13, [Murray93](#Murray93) @TODO-LINK §2.1-3, [Sutter00](#Sutter00) @TODO-LINK §47  

### <a name="sd-init"></a>Discussion : Utilisation de `=`, `{}` et `()` comme initialiseurs  
???  

### <a name="sd-factory"></a>Discussion : Utiliser une fonction de fabrique si vous avez besoin d'un comportement virtuel pendant l'initialisation  
Si votre conception prévoit un dispatch virtuel vers une classe dérivée depuis un constructeur ou un destructeur de classe de base pour des fonctions comme `f` et `g`, vous avez besoin d’autres techniques, telles qu’un post‑constructeur — une fonction membre distincte que l’appelant doit invoquer pour compléter l’initialisation, ce qui permet d’appeler en toute sécurité `f` et `g` car dans les fonctions membres les appels virtuels se comportent normalement. Certaines techniques sont présentées dans les Références. Voici une liste non exhaustive d’options :  

* Transférer la responsabilité : il suffit de documenter que le code utilisateur doit appeler la fonction de post‑initialisation immédiatement après la construction d’un objet.  
* Le post‑initialiser paresseusement : le faire lors de la première invocation d’une fonction membre. Un indicateur booléen dans la classe de base indique si le post‑construire a déjà eu lieu ou non.  
* Utiliser les sémantiques de classe de base virtuelle : les règles du langage précisent que le constructeur de la classe la plus dérivée décide quel constructeur de base sera invoqué ; vous pouvez exploiter cela à votre avantage. (Voir [Taligent94](#Taligent94).)  
* Utiliser une fonction de fabrique : ainsi vous pouvez facilement forcer une invocation obligatoire d’une fonction de post‑constructeur.  

    class B {
    public:
        B()
        {
            /* ... */
            f(); // MAUVAIS : C.82 : Ne pas appeler des fonctions virtuelles dans les constructeurs et les destructeurs
            /* ... */
        }

        virtual void f() = 0;
    };

    class B {
    protected:
        class Token {};

    public:
        // le constructeur doit être public pour que make_shared puisse y accéder.
        // le niveau d'accès protégé est obtenu en exigeant un Token.
        explicit B(Token) { /* ... */ }  // créer un objet imparfaitement initialisé
        virtual void f() = 0;

        template<class T>
        static shared_ptr<T> create()    // interface pour créer des objets partagés
        {
            auto p = make_shared<T>(typename T::Token{});
            p->post_initialize();
            return p;
        }

    protected:
        virtual void post_initialize()   // appelé juste après la construction
            { /* ... */ f(); /* ... */ } // BIEN : la distribution virtuelle est sûre
        }
    };

    class D : public B {                 // classe dérivée
    protected:
        class Token {};

    public:
        // le constructeur doit être public pour que make_shared puisse y accéder.
        // le niveau d'accès protégé est obtenu en exigeant un Token.
        explicit D(Token) : B{ B::Token{} } {}
        void f() override { /* ...  */ };

    protected:
        template<class T>
        friend shared_ptr<T> B::create();
    };

    shared_ptr<D> p = D::create<D>();    // création d'un objet D  

Cette conception requiert la discipline suivante :  

* Les classes dérivées, comme `D`, ne doivent pas exposer de constructeur appelable publiquement. Sinon, les utilisateurs de `D` pourraient créer des objets `D` qui n’invoquent pas `post_initialize`.  
* L’allocation est limitée à `operator new`. `B` peut cependant remplacer `new` (voir les Items 45 et 46 dans [SuttAlex05](#SuttAlex05)).  
* `D` doit définir un constructeur ayant les mêmes paramètres que ceux sélectionnés par `B`. Définir plusieurs surcharges de `create` peut atténuer ce problème ; les surcharges peuvent même être templatisées sur les types d’arguments.  

Si les exigences ci‑dessus sont remplies, cette conception garantit que `post_initialize` a été invoqué pour tout objet dérivé de `B` complètement construit. `post_initialize` n’a pas besoin d’être virtuel ; il peut toutefois invoquer librement des fonctions virtuelles.  

En résumé, aucune technique de post‑construction n’est parfaite. Les pires techniques évitent simplement le problème en demandant l’appel manuel du post‑constructeur. Même les meilleures requièrent une syntaxe différente pour la construction des objets (facile à vérifier au moment de la compilation) et/ou la coopération des auteurs des classes dérivées (impossible de vérifier au moment de la compilation).  

**Références** : [Alexandrescu01](#Alexandrescu01) @TODO-LINK §3, [Boost](#Boost) @TODO-LINK, [Dewhurst03](#Dewhurst03) @TODO-LINK §75, [Meyers97](#Meyers97) @TODO-LINK §46, [Stroustrup00](#Stroustrup00) @TODO-LINK §15.4.3, [Taligent94](#Taligent94) @TODO-LINK  

### <a name="sd-dtor"></a>Discussion : rendre les destructeurs de classe de base publics et virtuels, ou protégés et non‑virtuels  
Est‑ce que la destruction doit être virtuelle ? En d’autres termes, faut‑il autoriser la destruction via un pointeur sur une classe `base` ? Si oui, le destructeur de `base` doit être public afin d’être appelable et virtuel ; sinon son appel entraînerait un comportement indéterminé. Au contraire, il doit être protégé afin que seules les classes dérivées puissent l’appeler dans leurs propres destructeurs, et non‑virtuel puisqu’il n’a pas besoin de se comporter virtuellement.  

##### Exemple  

    class Base {
    public:
        ~Base();                   // MAUVAIS, pas virtuel
        virtual ~Base();           // BIEN
        // ...
    };

    class Derived : public Base { /* ... */ };

    {
        unique_ptr<Base> pb = make_unique<Derived>();
        // ...
    } // ~pb invoque le destructeur correct uniquement lorsque ~Base est virtuel

    class My_policy {
    public:
        virtual ~My_policy();      // MAUVAIS, public et virtuel
    protected:
        ~My_policy();              // BIEN
        // ...
    };

    template<class Policy>
    class customizable : Policy { /* ... */ }; // remarque : héritage privé  

##### Remarque  
Cette simple ligne directrice illustre un problème subtil et reflète l’utilisation moderne de l’héritage et des principes de conception orientée objet.  

Les objets d’une classe de base `Base` sont souvent détruits via des pointeurs vers `Base`. Si le destructeur de `Base` est public et non virtuel (l’état par défaut), il peut être appelé accidentellement sur un pointeur qui pointe réellement vers un objet dérivé, et le comportement est indéfini. Ce fait a conduit aux anciens standards de codage à imposer que tous les destructeurs de classe de base soient virtuels, ce qui est excessif. La règle devrait être que les destructeurs soient virtuels seulement si ils sont publics.  

##### Exception  
Certaines architectures de composants (par ex. COM et CORBA) n’utilisent pas de mécanisme de suppression standard, et favorisent d’autres protocoles de mise hors service d’objets. Suivez les modèles et idiomes locaux, et adaptez cette ligne directrice en conséquence.  

Prenez également en compte ce cas rare :  

* `B` est à la fois une classe de base et une classe concrète pouvant être instanciée par elle-même, et, par conséquent, son destructeur doit être public pour que les objets `B` soient créés et détruits.  
* Pourtant `B` n’a aucun fonction virtuelle et n’est pas destiné à être utilisé de façon polymorphe. Le destructeur est public, mais il n’a donc pas besoin d’être virtuel.  

Ainsi, même si le destructeur doit rester public, un grand stress peut être exercé pour ne pas le rendre virtuel, car en tant que première fonction virtuelle, il entraînerait tous les frais de surcharge de type d'exécution alors que la fonctionnalité ajoutée ne devrait jamais être nécessaire.  

Dans ce cas rare, vous pourriez rendre le destructeur public et non‑virtuel, mais documenter clairement que les objets dérivés ultérieurs ne doivent pas être utilisés de façon polymorphe à l’égard de `B`. C’est ce qui a été fait avec `std::unary_function`.  

En général, cependant, évitez les classes de base concrètes (voir l'Item 35). Par exemple, `unary_function` est un lot de typedef qui ne devait jamais être instancié de façon autonome. Donner un destructeur public n’a donc aucun sens ; un meilleur design consisterait à suivre les conseils de cet item et à lui donner un destructeur protégé non‑virtuel.  

**Références** : [SuttAlex05](#SuttAlex05) @TODO-LINK Item 50, [Cargill92](#Cargill92) @TODO-LINK pp. 77‑79, 207, [Cline99](#Cline99) @TODO-LINK §21.06, 21.12‑13, [Henricson97](#Henricson97) @TODO-LINK pp. 110‑114, [Koenig97](#Koenig97) @TODO-LINK Chapitres 4, 11, [Meyers97](#Meyers97) @TODO-LINK §14, [Stroustrup00](#Stroustrup00) @TODO-LINK §12.4.2, [Sutter02](#Sutter02) @TODO-LINK §27, [Sutter04](#Sutter04) @TODO-LINK §18  

### <a name="sd-noexcept"></a>Discussion : utilisation de noexcept  
???  

### <a name="sd-never-fail"></a>Discussion : les destructeurs, la libération et le swap ne doivent jamais échouer  
Ne laissez jamais qu'une erreur soit signalée depuis un destructeur, une fonction de désallocation de ressource (par ex. `operator delete`), ou une fonction `swap` qui lève une exception. Il est presque impossible d'écrire du code utile si ces opérations peuvent échouer, et même si quelque chose se trompe, il est presque toujours inutile de réessayer. En particulier, les types dont les destructeurs peuvent lancer une exception sont totalement interdits d'utilisation avec la bibliothèque C++ Standard. La plupart des destructeurs sont désormais `noexcept` par défaut.  

##### Exemple  
    class Nefarious {
    public:
        Nefarious() { /* code that could throw */ }    // bon
        ~Nefarious() { /* code that could throw */ }   // MAUVAIS, ne doit pas lancer
        // ...
    };

1. Les objets `Nefarious` sont difficiles à utiliser en toute sécurité même comme variables locales :  

    void test(string& s)
    {
        Nefarious n;          // problème en cours
        string copy = s;      // copie la chaîne
    } // détruire `copy` puis `n`

    Ici, copier `s` peut lever une exception, et si cela se produit et que le destructeur de `n` lève également une exception, le programme sort via `std::terminate` car deux exceptions ne peuvent pas être propagées simultanément.  

2. Les classes avec des membres ou des bases `Nefarious` sont également difficiles à utiliser en toute sécurité, car leurs destructeurs doivent invoquer le destructeur de `Nefarious`, et sont de même corrompus par son mauvais comportement :  

    class Innocent_bystander {
        Nefarious member;     // oops, poisons le destructeur de classe englobante
        // ...
    };

    void test(string& s)
    {
        Innocent_bystander i;  // plus de problème en cours
        string copy2 = s;      // copie la chaîne
    } // détruire `copy2` puis `i`

    Ici, si la construction de `copy2` lève une exception, nous avons le même problème car le destructeur de `i` peut également lever une exception et, le cas échéant, nous invoquons `std::terminate`.  

3. Vous ne pouvez pas créer de façon fiable d'objets `Nefarious` globaux ou statiques non plus :  

    static Nefarious n;       // oops, toute exception du destructeur ne peut pas être interceptée  

4. Vous ne pouvez pas créer d'arrays de `Nefarious` de façon fiable :  

    void test()
    {
        std::array<Nefarious, 10> arr; // cette ligne peut appeler std::terminate()
    }

    Le comportement des tableaux est indéfini en présence de destructeurs qui lèvent des exceptions car il n'existe aucun rollback raisonnable qu'un compilateur puisse concevoir. Imaginez : quel code le compilateur pourrait‑il générer pour construire un `arr` où, si le quatrième objet levé, le code doit abandonner et, dans son mode de nettoyage, appeler les destructeurs des objets déjà construits … et aucun de ces destructeurs ne lève une exception ? Il n'existe pas de réponse satisfaisante.  

5. Vous ne pouvez pas utiliser des objets `Nefarious` dans les conteneurs standards :  

    std::vector<Nefarious> vec(10);   // cette ligne peut appeler std::terminate()  

    La bibliothèque standard interdit à tout destructeur utilisé avec elle de lever une exception. Vous ne pouvez pas stocker des objets `Nefarious` dans les conteneurs standards ou les utiliser avec toute autre partie de la bibliothèque standard.  

##### Remarque  
Ces fonctions clés ne doivent pas échouer car elles sont nécessaires pour les deux opérations clés de la programmation transactionnelle : revenir en arrière si des problèmes sont rencontrés pendant le traitement, et confirmer les travaux si aucun problème ne se produit. S'il n'y a aucun moyen de revenir en arrière avec des opérations sans échec, la fonction de rollback sans échec est impossible à implémenter. S'il n'y a aucun moyen de confirmer le changement d'état avec une opération sans échec (notamment, mais pas limité à, `swap`), la confirmation sans échec est impossible à implémenter.  

Considérez les conseils et exigences subsistantes dans le standard C++ :  

> Si un destructeur appelé pendant la désenfilement de pile se termine par une exception, `terminate` est appelé (15.5.1). Les destructeurs doivent donc généralement attraper les exceptions et ne pas les laisser passer hors du destructeur. --[C++03](#Cplusplus03) §15.2(3)  

> Aucune opération de destructeur définie dans la bibliothèque C++ Standard (y compris le destructeur de tout type utilisé pour instancier un template de la bibliothèque standard) ne lèvera d'exception. --[C++03](#Cplusplus03) §17.4.4.8(3)  

Les fonctions de désallocation, y compris les surcharges spécifiques de `operator delete` et `operator delete[]`, appartiennent à la même catégorie, puisqu’elles sont également utilisées pendant le nettoyage en général, et pendant le traitement d’exceptions en particulier, pour revenir à un travail partiellement effectué qui doit être annulé.  

En dehors des destructeurs et des fonctions de désallocation, les techniques d'assurance de sécurité communes reposent également sur le fait que les opérations de `swap` ne peuvent jamais échouer, ce qui est le cas non pas parce qu'elles sont utilisées pour implémenter un rollback garanti, mais parce qu'elles sont utilisées pour implémenter un commit garanti. Par exemple, voici une implémentation idiomatique de `operator=` pour un type `T` qui effectue une construction de copie suivie d'un appel à un `swap` sans échec :  

    T& T::operator=(const T& other)
    {
        auto temp = other;
        swap(temp);
        return *this;
    }

(Consultez également l'Item 56. ???)  

**Références** : [SuttAlex05](#SuttAlex05) @TODO-LINK Item 51; [C++03](#Cplusplus03) §15.2(3), §17.4.4.8(3), [Meyers96](#Meyers96) @TODO-LINK §11, [Stroustrup00](#Stroustrup00) @TODO-LINK §14.4.7, §E.2-4, [Sutter00](#Sutter00) @TODO-LINK §8, §16, [Sutter02](#Sutter02) @TODO-LINK §18‑19  

## <a name="sd-consistent"></a>Définir copie, déplacement et destruction de façon cohérente  
##### Raison  
???  

##### Remarque  
Si vous définissez un constructeur de copie, vous devez également définir l’opérateur d’affectation par copie.  

##### Remarque  
Si vous définissez un constructeur de déplacement, vous devez également définir l’opérateur d’affectation par déplacement.  

##### Exemple  
    class X {
    public:
        X(const X&) { /* stuff */ }

        // MAUVAIS : n'a pas également défini l'opérateur d’affectation par copie

        X(x&&) noexcept { /* stuff */ }

        // MAUVAIS : n'a pas également défini l'opérateur d’affectation par déplacement

        // ...
    };

    X x1;
    X x2 = x1; // ok
    x2 = x1;   // piège : le compilateur peut échouer ou faire quelque chose de suspect  

    class X {
        HANDLE hnd;
        // ...
    public:
        ~X() { /* custom stuff, such as closing hnd */ }
        // suspect : aucune mention de copie ou de déplacement -- que se passe‑t‑il avec hnd ?
    };

    X x1;
    X x2 = x1; // piège : le compilateur peut échouer ou faire quelque chose de suspect
    x2 = x1;   // piège : le compilateur peut échouer ou faire quelque chose de suspect  

    class X {
        string s; // defines more efficient move operations
        // ... other data members ...
    public:
        X(const X&) { /* stuff */ }
        X& operator=(const X&) { /* stuff */ }

        // MAUVAIS : n'a pas également défini la construction et l’affectation par déplacement
        // (why wasn't the custom "stuff" repeated here?)
    };

    X test()
    {
        X local;
        // ...
        return local;  // piège : sera inefficace et/ou fera l’erreur
    }

Si vous définissez un constructeur de copie, vous devez également définir l'opérateur d'affectation par copie, et inversement. Si l’un des deux opère de façon spéciale, l’autre devrait l'être aussi, car les deux fonctions devraient avoir des effets similaires.  

Si vous définissez un constructeur de copie qui alloue ou duplique une ressource, vous devez libérer cette ressource dans le destructeur. Si vous définissez un destructeur non trivial, il faut généralement écrire les fonctions de copie et d'affectation de haut niveau.  

Si vous définissez un destructeur non trivial, il peut être nécessaire d'écrire ou de désactiver les opérations de copie.  

Dans de nombreux cas, tenir des ressources correctement encapsulées à l'aide d'objets RAII « occupants » élimine le besoin d'écrire ces opérations vous-même. (Voir Item 13.)  

Préférez les membres spéciaux générés par le compilateur (y compris `=default`) ; ce ne sont que ceux qui peuvent être classés « triviaux », et au moins un grand fournisseur de la bibliothèque standard optimise lourdement les classes ayant des membres spéciaux triviaux. C'est probablement la pratique courante.  

**Exceptions** : lorsqu'un des membres spéciaux est déclaré uniquement pour les rendre non publics ou virtuels, mais sans semantiques particulières, cela n’implique pas que les autres sont nécessaires. Dans des cas rares, les classes ayant des membres de types étranges (comme des références) sont une exception...  

**Références** : [SuttAlex05](#SuttAlex05) @TODO-LINK Item 52, [Cline99](#Cline99) @TODO-LINK §30.01‑14, [Koenig97](#Koenig97) @TODO-LINK §4, [Stroustrup00](#Stroustrup00) @TODO-LINK §5.5, §10.4, [SuttHysl04b](#SuttHysl04b) @TODO-LINK  

## Resource management rule summary:  
- [Fournir une sécurité de ressource forte ; ne jamais fuites d’une ressource que vous considérez comme une ressource](#cr-safety)  
- [Ne jamais retourner ou lever une exception tout en tenant une ressource non gérée par un handle](#cr-never)  
- [Un pointeur ou une référence « brut » n’est jamais un handle de ressource](#cr-raw)  
- [Ne jamais laisser un pointeur survivre à l’objet qu’il pointe](#cr-outlive)  
- [Utiliser des templates pour exprimer des conteneurs (et d’autres handles de ressources)](#cr-templates)  
- [Renvoi des conteneurs par valeur (en se basant sur le move ou l’élimination de copie pour l'efficacité)](#cr-value-return)  
- [Si une classe est un handle de ressource, elle doit avoir un constructeur, un destructeur, et des opérations de copie et/ou déplacement](#cr-handle)  
- [Si une classe est un conteneur, lui donner un constructeur à liste initialisatrice](#cr-list)  

### <a name="cr-safety"></a>Discussion : Fournir une sécurité de ressource forte ; c’est‑à‑dire ne jamais fuites d’une ressource que vous considérez comme une ressource  
##### Raison  
Éviter les fuites. Les fuites peuvent entraîner une perte de performances, des erreurs mystérieuses, des plantages système, et des violations de sécurité.  

**Formulation alternative** : faire en sorte que chaque ressource soit représentée par un objet d’une classe gérant sa durée de vie.  

##### Exemple  
    ??? "odd" non-memory resource ???  

##### Mise en œuvre  
La technique de base pour éviter les fuites consiste à avoir chaque ressource proprement détenue par un handle de ressource avec un destructeur approprié. Un vérificateur peut détecter les `new` « nocien ». Avec une liste de fonctions d’allocation de style C (par ex. `fopen()`), un vérificateur peut également détecter les usages non gérés par un handle de ressource. En général, les « pointeurs nues » sont très suspect, peuvent être signalés et/ou analysés. Une liste complète de ressources ne peut pas être générée sans l’intervention d’un humain (la définition de « une ressource » est trop générale), mais un outil peut être « paramétré » avec une liste de ressources.  

### <a name="cr-never"></a>Discussion : Ne jamais retourner ou lever une exception tout en tenant une ressource non gérée par un handle  
##### Raison  
Cela serait une fuite.  

##### Exemple  
    void f(int i)
    {
        FILE* f = fopen("a file", "r");
        ifstream is { "another file" };
        // ...
        if (i == 0) return;
        // ...
        fclose(f);
    }

Si `i == 0` le descripteur pour `a file` est perdu. D'un autre côté, l`ifstream` pour `another file` se ferme correctement (à la destruction). Si vous devez utiliser un pointeur explicite, plutôt qu'un handle de ressource avec des semantiques spécifiques, utilisez `unique_ptr` ou `shared_ptr` avec un déleter personnalisé :  

    void f(int i)
    {
        unique_ptr<FILE, int(*)(FILE*)> f(fopen("a file", "r"), fclose);
        // ...
        if (i == 0) return;
        // ...
    }

Mieux :  

    void f(int i)
    {
        ifstream input {"a file"};
        // ...
        if (i == 0) return;
        // ...
    }  

##### Mise en œuvre  
Un vérificateur doit considérer tous les pointeurs nues comme suspect. Un vérificateur doit probablement dépendre d'une liste fournie par l'utilisateur. Pour les tests initiaux, l'on connaît la bibliothèques standards, `string`, et les smart pointers. L'utilisation de `span` et `string_view` devrait aider (ils ne sont pas des handles de ressource).  

### <a name="cr-raw"></a>Discussion : Un pointeur ou une référence « brut » n’est jamais un handle de ressource  
##### Raison  
Pour distinguer les propriétaires des vues.  

##### Remarque  
Ceci est indépendant de la façon dont vous « écrivez » le pointeur : `T*`, `T&`, `Ptr<T>` et `Range<T>` ne sont pas des propriétaires.  

### <a name="cr-outlive"></a>Discussion : Ne jamais laisser un pointeur survivre à l’objet qu’il pointe  
##### Raison  
Pour éviter des erreurs extrêmement difficiles à repérer. Déférencer un tel pointeur est un comportement indéfini et peut provoquer des violations de l’architecture type.  

##### Exemple  
    string* bad()   // vraiment mauvais  
    {
        vector<string> v = { "This", "will", "cause", "trouble", "!" };
        // libération d’un pointeur dans un membre détruit d’un objet (v)
        return &v[0];
    }

    void use()
    {
        string* p = bad();
        vector<int> xx = {7, 8, 9};
        // comportement indéfini : x pourrait ne pas être le string "This"
        string x = *p;
        // comportement indéfini : nous ne savons pas ce qui est alloué à l’emplacement p
        *p = "Evil!";
    }  

### <a name="cr-templates"></a>Discussion : Utiliser des templates pour exprimer des conteneurs (et d’autres handles de ressources)  
##### Raison  
Pour fournir une manipulation d'éléments à type statiquement sûr.  

##### Exemple  
    template<typename T> class Vector {
        // ...
        T* elem;   // pointe sur sz éléments de type T
        int sz;
    };  

### <a name="cr-value-return"></a>Discussion : Renvoi des conteneurs par valeur (en se basant sur le move ou l’élimination de copie pour l'efficacité)  
##### Raison  
Pour simplifier le code et éviter la nécessité d'une gestion explicite de la mémoire. Pour introduire un objet dans un scope environnant, prolongeant ainsi sa durée de vie.  

**Voir aussi** : [F.20, la règle générale sur les valeurs « out »](#rf-out)  

##### Exemple  
    vector<int> get_large_vector()
    {
        return ...;
    }

    auto v = get_large_vector(); // le renvoi par valeur est ok, la plupart des compilateurs feront de l'élimination de copie  

##### Exception  
Voir les Exceptions dans [F.20](#rf-out).  

##### Mise en œuvre  
Vérifier les pointeurs et références retournés par les fonctions et s’assurer qu’ils sont attribués à des handles de ressources (par ex. `unique_ptr`).  

### <a name="cr-handle"></a>Discussion : Si une classe est un handle de ressource, elle doit avoir un constructeur, un destructeur, et des opérations de copie et/ou déplacement  
##### Raison  
Pour contrôler entièrement la durée de vie de la ressource. Pour fournir un ensemble cohérent d'opérations sur la ressource.  

##### Exemple  
    ??? Manipulation de pointeurs  

##### Remarque  
Si tous les membres sont des handles de ressource, exploitez les opérations générées par le compilateur quand c'est possible.  

    template<typename T> struct Named {
        string name;
        T value;
    };

Maintenant `Named` a un constructeur par défaut, un destructeur, et des opérations de copie et de déplacement efficaces, tant que `T` le permet.  

##### Mise en œuvre  
En général, un outil ne peut pas savoir qu'une classe est un handle de ressource. Cependant, si une classe possède certaines des [opérations par défaut](#ss-ctor), elle devrait en avoir toutes, et si une classe possède un membre qui est un handle de ressource, elle devrait être considérée comme telle.  

### <a name="cr-list"></a>Discussion : Si une classe est un conteneur, lui donner un constructeur à liste initialisatrice  
##### Raison  
Il est courant d'avoir un ensemble initial d'éléments.  

##### Exemple  
    template<typename T> class Vector {
    public:
        Vector(std::initializer_list<T>);
        // ...
    };

    Vector<string> vs { "Nygaard", "Ritchie" };  

##### Mise en œuvre  
Quand est‑il une classe conteneur ? ???  