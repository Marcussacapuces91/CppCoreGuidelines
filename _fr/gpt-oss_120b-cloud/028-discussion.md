# <a name="s-discussion"></a>Annexe C : Discussion

Cette section contient du matériel complémentaire sur les règles et ensembles de règles. En particulier, nous présentons ici des justifications supplémentaires, des exemples plus détaillés et des discussions d’alternatives.

### <a name="sd-order"></a>Discussion : définir et initialiser les membres de données dans l’ordre de déclaration

Les membres de données sont toujours initialisés dans l’ordre dans lequel ils sont déclarés dans la définition de la classe, il faut donc les placer dans cet ordre dans la liste d’initialisation du constructeur. Les écrire dans un ordre différent ne fait que rendre le code confus, car il ne s’exécutera pas dans l’ordre que vous voyez, ce qui complique la détection des bugs dépendants de l’ordre.

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

Dans cet exemple, `email` sera construit avant `first` et `last` car il est déclaré en premier. Cela signifie que son constructeur tentera d’utiliser `first` et `last` trop tôt — pas seulement avant qu’ils ne soient affectés aux valeurs souhaitées, mais avant même qu’ils ne soient construits.

Si la définition de la classe et le corps du constructeur sont dans des fichiers séparés, l’influence à longue distance que l’ordre des déclarations de membres de données exerce sur la correction du constructeur sera encore plus difficile à repérer.

**Références** :

[\[Cline99\]](032-bibliography.md#Cline99) §22.03-11, [\[Dewhurst03\]](032-bibliography.md#Dewhurst03) §52-53, [\[Koenig97\]](032-bibliography.md#Koenig97) §4, [\[Lakos96\]](032-bibliography.md#Lakos96) §10.3.5, [\[Meyers97\]](032-bibliography.md#Meyers97) §13, [\[Murray93\]](032-bibliography.md#Murray93) §2.1.3, [\[Sutter00\]](032-bibliography.md#Sutter00) §47

### <a name="sd-init"></a>Discussion : utilisation de `=`, `{}` et `()` comme initialiseurs

???  
@TODO-LINK: le texte de cette discussion doit être ajouté.

### <a name="sd-factory"></a>Discussion : utiliser une fonction‑fabrique si vous avez besoin d’un « comportement virtuel » lors de l’initialisation

Si votre conception nécessite le dispatch virtuel vers une classe dérivée depuis le constructeur ou le destructeur d’une classe de base pour des fonctions comme `f` et `g`, vous devez recourir à d’autres techniques, comme un post‑constructeur — une fonction membre séparée que l’appelant doit invoquer pour terminer l’initialisation, et qui peut appeler en toute sécurité `f` et `g` car les appels virtuels dans les fonctions membres se comportent normalement. Certaines de ces techniques sont présentées dans les Références. Voici une liste non exhaustive d’options :

* *Faire porter la responsabilité :* Documentez simplement que le code utilisateur doit appeler la fonction de post‑initialisation immédiatement après la construction d’un objet.  
* *Post‑initialisation paresseuse :* Effectuez‑la lors du premier appel d’une fonction membre. Un drapeau booléen dans la classe de base indique si la post‑construction a eu lieu ou non.  
* *Utiliser la sémantique des classes de base virtuelles :* Les règles du langage dictent que le constructeur de la classe la plus dérivée décide quel constructeur de base sera invoqué ; vous pouvez exploiter cela à votre avantage. (Voir [\[Taligent94\]](032-bibliography.md#Taligent94).)  
* *Utiliser une fonction‑fabrique :* De cette façon, vous pouvez facilement imposer l’invocation obligatoire d’une fonction post‑constructeur.

Voici un exemple de la dernière option :

    class B {
    public:
        B()
        {
            /* ... */
            f(); // BAD: C.82: Don't call virtual functions in constructors and destructors
            /* ... */
        }

        virtual void f() = 0;
    };

    class B {
    protected:
        class Token {};

    public:
        // constructor needs to be public so that make_shared can access it.
        // protected access level is gained by requiring a Token.
        explicit B(Token) { /* ... */ }  // create an imperfectly initialized object
        virtual void f() = 0;

        template<class T>
        static shared_ptr<T> create()    // interface for creating shared objects
        {
            auto p = make_shared<T>(typename T::Token{});
            p->post_initialize();
            return p;
        }

    protected:
        virtual void post_initialize()   // called right after construction
            { /* ... */ f(); /* ... */ } // GOOD: virtual dispatch is safe
        }
    };

    class D : public B {                 // some derived class
    protected:
        class Token {};

    public:
        // constructor needs to be public so that make_shared can access it.
        // protected access level is gained by requiring a Token.
        explicit D(Token) : B{ B::Token{} } {}
        void f() override { /* ...  */ };

    protected:
        template<class T>
        friend shared_ptr<T> B::create();
    };

    shared_ptr<D> p = D::create<D>();    // creating a D object

Ce design impose la discipline suivante :

* Les classes dérivées telles que `D` ne doivent pas exposer de constructeur appelable publiquement. Sinon, les utilisateurs de `D` pourraient créer des objets `D` qui n’appellent pas `post_initialize`.  
* L’allocation est limitée à `operator new`. `B` peut toutefois surcharger `new` (voir Items 45 et 46 dans [SuttAlex05](032-bibliography.md#SuttAlex05)).  
* `D` doit définir un constructeur avec les mêmes paramètres que ceux choisis par `B`. Définir plusieurs surcharges de `create` peut atténuer ce problème ; les surcharges peuvent même être templatisées sur les types d’arguments.

Si les exigences ci‑dessus sont respectées, le design garantit que `post_initialize` a été appelé pour tout objet dérivé de `B` correctement construit. `post_initialize` n’a pas besoin d’être virtuel ; il peut toutefois invoquer librement des fonctions virtuelles.

En résumé, aucune technique de post‑construction n’est parfaite. Les pires techniques esquivent le problème en demandant simplement à l’appelant d’invoquer le post‑constructeur manuellement. Les meilleures nécessitent une syntaxe différente pour la construction d’objets (facile à vérifier à la compilation) et/ou la coopération des auteurs de classes dérivées (impossible à vérifier à la compilation).

**Références** : [\[Alexandrescu01\]](032-bibliography.md#Alexandrescu01) §3, [\[Boost\]](021-references.md#Boost), [\[Dewhurst03\]](032-bibliography.md#Dewhurst03) §75, [\[Meyers97\]](032-bibliography.md#Meyers97) §46, [\[Stroustrup00\]](032-bibliography.md#Stroustrup00) §15.4.3, [\[Taligent94\]](032-bibliography.md#Taligent94)

### <a name="sd-dtor"></a>Discussion : rendre les destructeurs de classe de base publics et virtuels, ou protégés et non‑virtuels

La destruction doit‑elle se comporter virtuellement ? C’est‑à‑dire, doit‑on autoriser la destruction via un pointeur vers une classe `base` ? Si oui, le destructeur de `base` doit être public afin d’être appelable, et virtuel, sinon l’appel résulte en un comportement indéfini. Sinon, il doit être protégé afin que seules les classes dérivées puissent l’invoquer dans leurs propres destructeurs, et non‑virtuel puisqu’il n’a pas besoin de se comporter virtuellement.

#### Exemple

Le cas le plus répandu pour une classe de base est qu’elle soit destinée à être dérivée publiquement, et le code appelant utilise alors typiquement quelque chose comme `shared_ptr<base>` :

    class Base {
    public:
        ~Base();                   // BAD, not virtual
        virtual ~Base();           // GOOD
        // ...
    };

    class Derived : public Base { /* ... */ };

    {
        unique_ptr<Base> pb = make_unique<Derived>();
        // ...
    } // ~pb invokes correct destructor only when ~Base is virtual

Dans les cas plus rares, comme les classes de politique, la classe est utilisée comme base par commodité, pas pour un comportement polymorphe. Il est recommandé de rendre ces destructeurs protégés et non‑virtuels :

    class My_policy {
    public:
        virtual ~My_policy();      // BAD, public and virtual
    protected:
        ~My_policy();              // GOOD
        // ...
    };

    template<class Policy>
    class customizable : Policy { /* ... */ }; // note: private inheritance

##### Remarque

Cette directive simple illustre un problème subtil et reflète les usages modernes de l’héritage et des principes de conception orientée objet.

Pour une classe `Base`, le code appelant peut tenter de détruire des objets dérivés via des pointeurs vers `Base`, par exemple en utilisant un `unique_ptr<Base>`. Si le destructeur de `Base` est public et non‑virtuel (le comportement par défaut), il peut être accidentellement appelé sur un pointeur qui pointe réellement vers un objet dérivé, ce qui rend le comportement de la suppression indéfini. Cette situation a conduit les anciens standards de codage à imposer l’exigence que tous les destructeurs de classes de base soient virtuels. Cela est excessif (même si c’est le cas le plus fréquent) ; à la place, la règle devrait être : rendre les destructeurs de classes de base virtuels **si et seulement si** ils sont publics.

Écrire une classe de base, c’est définir une abstraction (voir Items 35 à 37). Rappelez‑vous que pour chaque fonction membre participant à cette abstraction, vous devez décider :

* Si elle doit se comporter virtuellement ou non.  
* Si elle doit être disponible publiquement à tous les appelants via un pointeur vers `Base` ou bien rester un détail d’implémentation interne.

Comme décrit dans l’Item 39, pour une fonction membre normale, le choix se porte entre : autoriser l’appel via un pointeur vers `Base` non‑virtuellement (mais éventuellement avec un comportement virtuel si elle invoque des fonctions virtuelles, comme dans les patterns NVI ou Méthode‑Template), virtuellement, ou pas du tout. Le pattern NVI est une technique pour éviter les fonctions virtuelles publiques.

La destruction peut être vue comme une autre opération, avec des sémantiques spéciales qui rendent les appels non‑virtuels dangereux ou incorrects. Ainsi, pour un destructeur de classe de base, le choix se porte entre : autoriser son appel via un pointeur vers `Base` virtuellement ou pas du tout ; « non‑virtuellement » n’est pas une option. Donc, un destructeur de classe de base est virtuel s’il peut être appelé (c’est‑à‑dire, s’il est public), et non‑virtuel sinon.

Notez que le pattern NVI ne peut pas s’appliquer au destructeur car les constructeurs et destructeurs ne peuvent pas réaliser d’appels virtuels profonds. (Voir Items 39 et 55.)

**Corollaire** : Lors de l’écriture d’une classe de base, écrivez toujours explicitement un destructeur, car celui généré implicitement est public et non‑virtuel. Vous pouvez toujours `=default` l’implémentation si le corps par défaut convient et que vous vous contentez d’écrire la fonction pour lui donner la visibilité et la virtualité appropriées.

##### Exception

Certaines architectures de composants (par ex. : COM et CORBA) n’utilisent pas un mécanisme de suppression standard et favorisent des protocoles différents pour la destruction d’objets. Suivez les modèles et idiomes locaux, et adaptez cette directive en conséquence.

Considérez également ce cas rare :

* `B` est à la fois une classe de base et une classe concrète qui peut être instanciée par elle‑même, si bien que le destructeur doit être public pour que les objets `B` puissent être créés et détruits.  
* Pourtant `B` n’a aucune fonction virtuelle et n’est pas censée être utilisée polymorphiquement, de sorte que bien que le destructeur soit public, il n’a pas besoin d’être virtuel.

Dans ce cas rare, vous pourriez rendre le destructeur public et non‑virtuel tout en documentant clairement que les objets dérivés ultérieurs ne doivent pas être utilisés polymorphiquement comme `B`. C’est ce qui a été fait avec `std::unary_function`.

En général, toutefois, évitez les classes de base concrètes (voir Item 35). Par exemple, `unary_function` était un ensemble de typedefs qui n’a jamais eu vocation à être instancié seul. Il n’a aucune raison d’avoir un destructeur public ; un meilleur design aurait suivi le conseil de cet Item et aurait donné à `unary_function` un destructeur protégé et non‑virtuel.

**Références** : [\[SuttAlex05\]](032-bibliography.md#SuttAlex05) Item 50, [\[Cargill92\]](032-bibliography.md#Cargill92) pp. 77‑79, 207, [\[Cline99\]](032-bibliography.md#Cline99) §21.06, 21.12‑13, [\[Henricson97\]](032-bibliography.md#Henricson97) pp. 110‑114, [\[Koenig97\]](032-bibliography.md#Koenig97) Chapters 4, 11, [\[Meyers97\]](032-bibliography.md#Meyers97) §14, [\[Stroustrup00\]](032-bibliography.md#Stroustrup00) §12.4.2, [\[Sutter02\]](032-bibliography.md#Sutter02) §27, [\[Sutter04\]](032-bibliography.md#Sutter04) §18

### <a name="sd-noexcept"></a>Discussion : utilisation de `noexcept`

???  
@TODO-LINK: le texte de cette discussion doit être ajouté.

### <a name="sd-never-fail"></a>Discussion : les destructeurs, la désallocation et `swap` ne doivent jamais échouer

Ne jamais autoriser un rapport d’erreur depuis un destructeur, une fonction de désallocation de ressource (p. ex. `operator delete`) ou une fonction `swap` en utilisant `throw`. Il est quasiment impossible d’écrire du code utile si ces opérations peuvent échouer, et même si quelque chose tourne mal il ne fait presque jamais sens de réessayer. En particulier, les types dont les destructeurs pourraient lancer une exception sont strictement interdits d’utilisation avec la Bibliothèque Standard C++. La plupart des destructeurs sont désormais implicitement `noexcept` par défaut.

##### Exemple

    class Nefarious {
    public:
        Nefarious() { /* code that could throw */ }    // ok
        ~Nefarious() { /* code that could throw */ }   // BAD, should not throw
        // ...
    };

1. Les objets `Nefarious` sont difficiles à utiliser en toute sécurité même comme variables locales :

        void test(string& s)
        {
            Nefarious n;          // trouble brewing
            string copy = s;      // copy the string
        } // destroy copy and then n

    Ici, la copie de `s` pourrait lancer une exception, et si cela se produit et que le destructeur de `n` lance également une exception, le programme se terminera via `std::terminate` parce que deux exceptions ne peuvent pas être propagées simultanément.

2. Les classes contenant des membres ou des bases de type `Nefarious` sont aussi difficiles à utiliser en toute sécurité, car leurs destructeurs doivent invoquer le destructeur de `Nefarious`, et sont ainsi empoisonnés par ce mauvais comportement :

        class Innocent_bystander {
            Nefarious member;     // oops, poisons the enclosing class's destructor
            // ...
        };

        void test(string& s)
        {
            Innocent_bystander i;  // more trouble brewing
            string copy2 = s;      // copy the string
        } // destroy copy and then i

    Si la construction de `copy2` lance une exception, nous avons le même problème car le destructeur de `i` peut aussi lancer une exception, entraînant alors l’appel à `std::terminate`.

3. Vous ne pouvez pas créer de façon fiable des objets globaux ou statiques `Nefarious` :

        static Nefarious n;       // oops, any destructor exception can't be caught

4. Vous ne pouvez pas créer de façon fiable des tableaux de `Nefarious` :

        void test()
        {
            std::array<Nefarious, 10> arr; // this line can std::terminate()
        }

    Le comportement des tableaux est indéfini en présence de destructeurs qui lancent, car il n’existe aucune stratégie de rollback raisonnable que le compilateur pourrait appliquer. Imaginez : quel code le compilateur pourrait‑il générer pour construire un `arr` où, si le constructeur du quatrième objet lance une exception, le code doit abandonner et, dans son mode de nettoyage, appeler les destructeurs des objets déjà construits… et qu’un ou plusieurs de ces destructeurs lancent à leur tour ? Il n’y a aucune réponse satisfaisante.

5. Vous ne pouvez pas utiliser d’objets `Nefarious` dans les conteneurs standards :

        std::vector<Nefarious> vec(10);   // this line can std::terminate()

    La bibliothèque standard interdit que les destructeurs utilisés avec elle puissent lancer une exception. Vous ne pouvez donc pas stocker des objets `Nefarious` dans les conteneurs standards ni les utiliser avec aucune autre partie de la bibliothèque standard.

##### Remarque

Ces fonctions clés ne doivent pas échouer car elles sont nécessaires aux deux opérations essentielles de la programmation transactionnelle : revenir en arrière si des problèmes surviennent pendant le traitement, et valider les changements si aucun problème n’apparaît. Si aucune opération infaillible n’est disponible pour revenir en arrière, le rollback infaillible devient impossible à implémenter. De même, si aucune opération infaillible n’est disponible pour valider les changements d’état (notamment, mais pas uniquement, `swap`), le commit infaillible devient impossible à implémenter.

Considérez les exigences suivantes tirées du Standard C++ :

> If a destructor called during stack unwinding exits with an exception, terminate is called (15.5.1). So destructors should generally catch exceptions and not let them propagate out of the destructor. --[\[C++03\]](032-bibliography.md#Cplusplus03) §15.2(3)  
> No destructor operation defined in the C++ Standard Library (including the destructor of any type that is used to instantiate a standard-library template) will throw an exception. --[\[C++03\]](032-bibliography.md#Cplusplus03) §17.4.4.8(3)

Les fonctions de désallocation, y compris les surcharges spécifiques de `operator delete` et `operator delete[]`, relèvent de la même catégorie, car elles sont également utilisées lors du nettoyage en général et, en particulier, pendant le traitement d’exceptions pour revenir sur un travail partiel qui doit être annulé.

Outre les destructeurs et les fonctions de désallocation, les techniques d’erreur‑sûreté courantes reposent également sur le fait que les opérations `swap` ne doivent jamais échouer — non pas parce qu’elles sont utilisées pour implémenter un rollback garanti, mais parce qu’elles sont utilisées pour implémenter un commit garanti. Par exemple, voici une implémentation idiomatique de `operator=` pour un type `T` qui effectue une construction par copie suivie d’un appel à un `swap` infaillible :

    T& T::operator=(const T& other)
    {
        auto temp = other;
        swap(temp);
        return *this;
    }

(voir aussi Item 56. ???)

Heureusement, lors de la libération d’une ressource, le champ d’échec est nettement plus restreint. Si vous utilisez les exceptions comme mécanisme de rapport d’erreur, assurez‑vous que ces fonctions traitent toutes les exceptions et autres erreurs que leurs traitements internes pourraient générer. (Pour les exceptions, il suffit d’entourer tout le code sensible de votre destructeur d’un bloc `try/catch(...)`). Cela est particulièrement important car un destructeur peut être appelé dans une situation de crise, comme l’échec d’allocation d’une ressource système (mémoire, fichiers, verrous, ports, fenêtres ou autres objets système).

Lorsque vous utilisez les exceptions comme mécanisme de gestion d’erreurs, documentez toujours ce comportement en déclarant ces fonctions `noexcept`. (Voir Item 75.)

**Références** : [\[SuttAlex05\]](032-bibliography.md#SuttAlex05) Item 51 ; [\[C++03\]](032-bibliography.md#Cplusplus03) §15.2(3), §17.4.4.8(3), [\[Meyers96\]](032-bibliography.md#Meyers96) §11, [\[Stroustrup00\]](032-bibliography.md#Stroustrup00) §14.4.7, §E.2‑4, [\[Sutter00\]](032-bibliography.md#Sutter00) §8, §16, [\[Sutter02\]](032-bibliography.md#Sutter02) §18‑19

## <a name="sd-consistent"></a>Définir copie, déplacement et destruction de façon cohérente

##### Raison

???  
@TODO-LINK: le texte de la raison doit être ajouté.

##### Remarque

Si vous définissez un constructeur de copie, vous devez également définir un opérateur d’affectation de copie.

##### Remarque

Si vous définissez un constructeur de déplacement, vous devez également définir un opérateur d’affectation de déplacement.

##### Exemple

    class X {
    public:
        X(const X&) { /* stuff */ }

        // BAD: failed to also define a copy assignment operator

        X(x&&) noexcept { /* stuff */ }

        // BAD: failed to also define a move assignment operator

        // ...
    };

    X x1;
    X x2 = x1; // ok
    x2 = x1;   // pitfall: either fails to compile, or does something suspicious

Si vous définissez un destructeur, vous ne devez pas utiliser les opérations de copie ou de déplacement générées par le compilateur ; vous avez probablement besoin de définir ou de supprimer la copie et/ou le déplacement.

    class X {
        HANDLE hnd;
        // ...
    public:
        ~X() { /* custom stuff, such as closing hnd */ }
        // suspicious: no mention of copying or moving -- what happens to hnd?
    };

    X x1;
    X x2 = x1; // pitfall: either fails to compile, or does something suspicious
    x2 = x1;   // pitfall: either fails to compile, or does something suspicious

Si vous définissez la copie, et qu’une base ou un membre possède un type qui définit une opération de déplacement, vous devez également définir une opération de déplacement.

    class X {
        string s; // defines more efficient move operations
        // ... other data members ...
    public:
        X(const X&) { /* stuff */ }
        X& operator=(const X&) { /* stuff */ }

        // BAD: failed to also define a move construction and move assignment
        // (why wasn't the custom "stuff" repeated here?)
    };

    X test()
    {
        X local;
        // ...
        return local;  // pitfall: will be inefficient and/or do the wrong thing
    }

Si vous définissez l’un des trois : constructeur de copie, opérateur d’affectation de copie ou destructeur, vous devriez probablement définir les autres.

##### Remarque

Si vous avez besoin de définir l’une de ces cinq fonctions, cela signifie que vous avez besoin d’un comportement différent de celui par défaut ; les cinq sont inter‑relées de façon asymétrique. Voici comment :

* Si vous écrivez ou désactivez l’un des constructeurs ou opérateurs de copie, vous devez probablement faire de même pour l’autre : si l’un effectue un « travail spécial », l’autre devrait probablement le faire également, car les deux fonctions doivent produire des effets similaires. (Voir Item 53, qui développe ce point isolément.)  
* Si vous écrivez explicitement les fonctions de copie, vous devez probablement écrire le destructeur : si le « travail spécial » du constructeur de copie consiste à allouer ou dupliquer une ressource (mémoire, fichier, socket, …), il faut la libérer dans le destructeur.  
* Si vous écrivez explicitement le destructeur, vous devez probablement écrire ou désactiver la copie : si vous devez écrire un destructeur non trivial, c’est souvent parce que vous devez libérer manuellement une ressource que l’objet détient. Si tel est le cas, il est probable que ces ressources exigent une duplication soigneuse, d’où la nécessité de prêter attention à la façon dont les objets sont copiés et affectés, ou de désactiver complètement la copie.

Dans de nombreux cas, l’utilisation d’objets « owning » RAII correctement encapsulés élimine le besoin d’écrire ces opérations vous‑même. (Voir Item 13.)

Préférez les membres spéciaux générés par le compilateur (y compris `=default`) ; seuls ceux‑ci peuvent être qualifiés de « triviaux », et au moins un grand fournisseur de bibliothèques standard les optimise fortement. Cela deviendra probablement une pratique courante.

**Exceptions** : lorsqu’une des fonctions spéciales est déclarée uniquement pour la rendre non publique ou virtuelle, mais sans sémantique particulière, cela n’implique pas que les autres soient nécessaires. Dans les cas rares où les classes possèdent des membres de types étranges (comme des références), elles constituent une exception car elles ont des sémantiques de copie particulières. Dans une classe contenant une référence, vous devrez probablement écrire le constructeur de copie et l’opérateur d’affectation, mais le destructeur par défaut fait déjà ce qu’il faut. (Notez que l’utilisation d’un membre de référence est presque toujours une mauvaise idée.)

**Références** : [\[SuttAlex05\]](032-bibliography.md#SuttAlex05) Item 52 ; [\[Cline99\]](032-bibliography.md#Cline99) §30.01‑14, [\[Koenig97\]](032-bibliography.md#Koenig97) §4, [\[Stroustrup00\]](032-bibliography.md#Stroustrup00) §5.5, §10.4, [\[SuttHysl04b\]](032-bibliography.md#SuttHysl04b)

**Résumé des règles de gestion des ressources** :

* [Fournir une forte sécurité des ressources ; c’est‑à‑dire, ne jamais laisser fuir ce qui est considéré comme une ressource](028-discussion.md#cr-safety)  
* [Ne jamais renvoyer ou lancer une exception tout en détenant une ressource non possédée par un handle](028-discussion.md#cr-never)  
* [Un pointeur ou une référence « brut(e) » n’est jamais un handle de ressource](028-discussion.md#cr-raw)  
* [Ne jamais laisser un pointeur survivre à l’objet auquel il pointe](028-discussion.md#cr-outlive)  
* [Utiliser les modèles (templates) pour exprimer les conteneurs (et autres handles de ressource)](028-discussion.md#cr-templates)  
* [Retourner les conteneurs par valeur (en s’appuyant sur le déplacement ou l’élimination de copie pour l’efficacité)](028-discussion.md#cr-value-return)  
* [Si une classe est un handle de ressource, elle a besoin d’un constructeur, d’un destructeur et d’opérations de copie et/ou de déplacement](028-discussion.md#cr-handle)  
* [Si une classe est un conteneur, lui fournir un constructeur à partir d’une liste d’initialisation](028-discussion.md#cr-list)

### <a name="cr-safety"></a>Discussion : fournir une forte sécurité des ressources ; c’est‑à‑dire, ne jamais laisser fuir ce que vous considérez comme une ressource

##### Raison

Empêcher les fuites. Les fuites peuvent entraîner une détérioration des performances, des erreurs mystérieuses, des plantages du système et des violations de sécurité.

**Formulation alternative** : faire de chaque ressource un objet d’une classe qui en gère le cycle de vie.

##### Exemple

    template<class T>
    class Vector {
    private:
        T* elem;   // sz elements on the free store, owned by the class object
        int sz;
        // ...
    };

Cette classe est un handle de ressource. Elle gère le cycle de vie des `T`. Pour ce faire, `Vector` doit définir ou supprimer [les opérations de copie, déplacement et destruction](007-class.md#rc-five).

??? "odd" non‑memory resource ???  
@TODO-LINK: ajouter un exemple de ressource non‑mémoire.

##### Application

La technique de base pour empêcher les fuites consiste à ce que chaque ressource soit possédée par un handle de ressource disposant d’un destructeur approprié. Un analyseur peut repérer les « new » nus. À partir d’une liste de fonctions d’allocation de type C (par ex. `fopen()`), un analyseur peut également repérer les utilisations qui ne sont pas gérées par un handle de ressource. En général, les « pointeurs nus » peuvent être considérés avec suspicion, signalés ou analysés. Une liste exhaustive des ressources ne peut être générée sans intervention humaine (la définition d’une « ressource » est trop générale), mais un outil peut être « paramétré » avec une liste de ressources.

### <a name="cr-never"></a>Discussion : ne jamais renvoyer ou lancer une exception tout en détenant une ressource non possédée par un handle

##### Raison

Cela constituerait une fuite.

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

Si `i == 0`, le handle de fichier pour *a file* est fuité. En revanche, l’`ifstream` pour *another file* sera correctement fermé à sa destruction. Si vous devez utiliser un pointeur explicite plutôt qu’un handle de ressource à sémantique précise, utilisez `unique_ptr` ou `shared_ptr` avec un délégateur personnalisé :

    void f(int i)
    {
        unique_ptr<FILE, int(*)(FILE*)> f(fopen("a file", "r"), fclose);
        // ...
        if (i == 0) return;
        // ...
    }

Mieux :

    void f(int i)
    {
        ifstream input {"a file"};
        // ...
        if (i == 0) return;
        // ...
    }

##### Application

Un analyseur doit considérer tous les « pointeurs nus » comme suspects. Un analyseur devra probablement s’appuyer sur une liste de ressources fournie par l’humain. Pour commencer, nous connaissons les conteneurs de la bibliothèque standard, `string`, et les pointeurs intelligents. L’utilisation de `span` et `string_view` devrait grandement aider (ils ne sont pas des handles de ressource).

### <a name="cr-raw"></a>Discussion : un pointeur ou une référence « brut(e) » n’est jamais un handle de ressource

##### Raison

Être capable de distinguer les propriétaires des vues.

##### Note

Ceci est indépendant de la façon dont vous « spellez » le pointeur : `T*`, `T&`, `Ptr<T>` et `Range<T>` ne sont pas des propriétaires.

### <a name="cr-outlive"></a>Discussion : ne jamais laisser un pointeur survivre à l’objet auquel il pointe

##### Raison

Éviter des erreurs extrêmement difficiles à détecter. Déréférencer un tel pointeur entraîne un comportement indéfini et peut violer le système de types.

##### Exemple

    string* bad()   // really bad
    {
        vector<string> v = { "This", "will", "cause", "trouble", "!" };
        // leaking a pointer into a destroyed member of a destroyed object (v)
        return &v[0];
    }

    void use()
    {
        string* p = bad();
        vector<int> xx = {7, 8, 9};
        // undefined behavior: x might not be the string "This"
        string x = *p;
        // undefined behavior: we don't know what (if anything) is allocated at location p
        *p = "Evil!";
    }

Le tableau `v` est détruit à la sortie de `bad()` ainsi que `v` lui‑même. Le pointeur retourné pointe donc vers de la mémoire non allouée sur le tas. Cette mémoire peut avoir été réallouée d’ici l’exécution de `*p`. Aucun `string` n’est alors disponible à la lecture et écrire via `p` pourrait facilement corrompre des objets de types différents.

##### Application

La plupart des compilateurs émettent déjà des avertissements pour les cas simples et possèdent les informations nécessaires pour aller plus loin. Considérez tout pointeur retourné par une fonction comme suspect. Utilisez les conteneurs, les handles de ressources et les vues (par ex. `span` qui n’est pas un handle de ressource) pour réduire le nombre de cas à examiner. En règle générale, tout type avec un destructeur doit être considéré comme un handle de ressource.

### <a name="cr-templates"></a>Discussion : utiliser les templates pour exprimer les conteneurs (et autres handles de ressource)

##### Raison

Fournir une manipulation statiquement sûre des éléments.

##### Exemple

    template<typename T> class Vector {
        // ...
        T* elem;   // point to sz elements of type T
        int sz;
    };

### <a name="cr-value-return"></a>Discussion : retourner les conteneurs par valeur (en s’appuyant sur le déplacement ou l’élimination de copie pour l’efficacité)

##### Raison

Simplifier le code et éliminer le besoin de gestion explicite de la mémoire. Permettre à un objet d’être introduit dans le scope environnant, prolongeant ainsi sa durée de vie.

**Voir aussi** : [F.20, l’item général sur les valeurs « out »](006-functions.md#rf-out)

##### Exemple

    vector<int> get_large_vector()
    {
        return ...;
    }

    auto v = get_large_vector(); // return by value is ok, most modern compilers will do copy elision

##### Exception

Voir les exceptions dans [F.20](006-functions.md#rf-out).

##### Application

Vérifiez les pointeurs et références retournés par des fonctions et voyez s’ils sont assignés à des handles de ressource (par ex. à un `unique_ptr`).

### <a name="cr-handle"></a>Discussion : si une classe est un handle de ressource, elle a besoin d’un constructeur, d’un destructeur et d’opérations de copie et/ou de déplacement

##### Raison

Fournir un contrôle complet du cycle de vie de la ressource. Fournir un ensemble cohérent d’opérations sur la ressource.

??? Messing with pointers  
@TODO-LINK: ajouter un exemple concret d’utilisation d’un handle de ressource.

##### Note

Si tous les membres sont eux‑mêmes des handles de ressources, utilisez autant que possible les opérations générées par le compilateur.

    template<typename T> struct Named {
        string name;
        T value;
    };

`Named` possède maintenant un constructeur par défaut, un destructeur et des opérations de copie et de déplacement efficaces, à condition que `T` les possède également.

##### Application

En général, un outil ne peut pas déterminer si une classe est un handle de ressource. Cependant, si une classe possède certaines des [opérations par défaut](007-class.md#ss-ctor), elle devrait en disposer de toutes, et si une classe possède un membre qui est un handle de ressource, elle devrait être considérée comme telle.

### <a name="cr-list"></a>Discussion : si une classe est un conteneur, lui fournir un constructeur à partir d’une liste d’initialisation

##### Raison

Il est fréquent de vouloir initialiser un ensemble d’éléments.

##### Exemple

    template<typename T> class Vector {
    public:
        Vector(std::initializer_list<T>);
        // ...
    };

    Vector<string> vs { "Nygaard", "Ritchie" };

##### Application

Quand une classe doit‑elle être considérée comme un conteneur ? ???  
@TODO-LINK: préciser les critères de classification d’une classe comme conteneur.