# <a name="s-discussion"></a>Annexe C : Discussion

Cette section contient du matériel complémentaire sur les règles et les ensembles de règles.
En particulier, nous y présentons des justifications supplémentaires, des exemples plus longs et des discussions sur les alternatives.

### <a name="sd-order"></a>Discussion : Définir et initialiser les membres de données dans l'ordre de leur déclaration

Les membres de données sont toujours initialisés dans l'ordre dans lequel ils sont déclarés dans la définition de la classe. Écrivez-les donc dans cet ordre dans la liste d'initialisation du constructeur. Les écrire dans un ordre différent ne fait que rendre le code confus, car il ne s'exécutera pas dans l'ordre où vous le lisez, et cela peut rendre difficile la détection des bogues dépendant de l'ordre.

    class Employee {
        string email, first, last;
    public:
        Employee(const char* firstName, const char* lastName);
        // ...
    };

    Employee::Employee(const char* firstName, const char* lastName)
      : first(firstName),
        last(lastName),
        // MAUVAIS : first et last ne sont pas encore construits
        email(first + "." + last + "@acme.com")
    {}

Dans cet exemple, `email` sera construit avant `first` et `last` car il est déclaré en premier. Cela signifie que son constructeur tentera d'utiliser `first` et `last` trop tôt — non seulement avant qu'ils ne soient assignés aux valeurs souhaitées, mais avant même qu'ils ne soient construits.

Si la définition de la classe et le corps du constructeur se trouvent dans des fichiers distincts, l'influence à distance que l'ordre des déclarations de membres de données exerce sur la correction du constructeur sera encore plus difficile à repérer.

**Références** :

[\[Cline99\]](032-bibliography.md#Cline99) §22.03-11, [\[Dewhurst03\]](032-bibliography.md#Dewhurst03) §52-53, [\[Koenig97\]](032-bibliography.md#Koenig97) §4, [\[Lakos96\]](032-bibliography.md#Lakos96) §10.3.5, [\[Meyers97\]](032-bibliography.md#Meyers97) §13, [\[Murray93\]](032-bibliography.md#Murray93) §2.1.3, [\[Sutter00\]](032-bibliography.md#Sutter00) §47

### <a name="sd-init"></a>Discussion : Utilisation de `=`, `{}` et `()` comme initialiseurs

???

### <a name="sd-factory"></a>Discussion : Utiliser une fonction fabrique si vous avez besoin d'un « comportement virtuel » pendant l'initialisation

Si votre conception souhaite une dispatch virtuelle vers une classe dérivée depuis le constructeur ou le destructeur d'une classe de base pour des fonctions comme `f` et `g`, vous avez besoin d'autres techniques, telles qu'un post-constructeur — une fonction membre distincte que l'appelant doit invoquer pour compléter l'initialisation, qui peut appeler `f` et `g` en toute sécurité car dans les fonctions membres les appels virtuels se comportent normalement. Certaines techniques à cet effet sont présentées dans les Références. Voici une liste non exhaustive d'options :

* *Déléguer la responsabilité :* Documentez simplement que le code utilisateur doit appeler la fonction de post-initialisation immédiatement après la construction d'un objet.
* *Post-initialiser paresseusement :* Faites-le lors du premier appel d'une fonction membre. Un drapeau booléen dans la classe de base indique si la post-construction a déjà eu lieu.
* *Utiliser la sémantique des classes de base virtuelles :* Les règles du langage stipulent que le constructeur de la classe la plus dérivée décide quel constructeur de base sera invoqué ; vous pouvez en tirer parti. (Voir [\[Taligent94\]](032-bibliography.md#Taligent94).)
* *Utiliser une fonction fabrique :* De cette façon, vous pouvez facilement forcer l'appel obligatoire d'une fonction de post-constructeur.

Voici un exemple de la dernière option :

    class B {
    public:
        B()
        {
            /* ... */
            f(); // MAUVAIS : C.82 : Ne pas appeler de fonctions virtuelles dans les constructeurs et destructeurs
            /* ... */
        }

        virtual void f() = 0;
    };

    class B {
    protected:
        class Token {};

    public:
        // Le constructeur doit être public pour que make_shared puisse y accéder.
        // Le niveau d'accès protégé est obtenu en exigeant un Token.
        explicit B(Token) { /* ... */ }  // crée un objet imparfaitement initialisé
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
            { /* ... */ f(); /* ... */ } // BON : la dispatch virtuelle est sûre
        }
    };


    class D : public B {                 // une classe dérivée
    protected:
        class Token {};

    public:
        // Le constructeur doit être public pour que make_shared puisse y accéder.
        // Le niveau d'accès protégé est obtenu en exigeant un Token.
        explicit D(Token) : B{ B::Token{} } {}
        void f() override { /* ...  */ };

    protected:
        template<class T>
        friend shared_ptr<T> B::create();
    };

    shared_ptr<D> p = D::create<D>();    // création d'un objet D

Cette conception exige la discipline suivante :

* Les classes dérivées telles que `D` ne doivent pas exposer de constructeur publiquement appelable. Sinon, les utilisateurs de `D` pourraient créer des objets `D` qui n'invoquent pas `post_initialize`.
* L'allocation est limitée à `operator new`. `B` peut toutefois surcharger `new` (voir les Articles 45 et 46 dans [SuttAlex05](032-bibliography.md#SuttAlex05)).
* `D` doit définir un constructeur avec les mêmes paramètres que ceux sélectionnés par `B`. Définir plusieurs surcharges de `create` peut atténuer ce problème ; les surcharges peuvent même être templatisées sur les types d'arguments.

Si les exigences ci-dessus sont satisfaites, la conception garantit que `post_initialize` a été appelé pour tout objet dérivé de `B` entièrement construit. `post_initialize` n'a pas besoin d'être virtuel ; il peut toutefois appeler librement des fonctions virtuelles.

En résumé, aucune technique de post-construction n'est parfaite. Les pires techniques esquivent le problème en demandant simplement à l'appelant d'invoquer manuellement le post-constructeur. Même les meilleures exigent une syntaxe différente pour la construction des objets (facile à vérifier à la compilation) et/ou la coopération des auteurs de classes dérivées (impossible à vérifier à la compilation).

**Références** : [\[Alexandrescu01\]](032-bibliography.md#Alexandrescu01) §3, [\[Boost\]](021-references.md#Boost), [\[Dewhurst03\]](032-bibliography.md#Dewhurst03) §75, [\[Meyers97\]](032-bibliography.md#Meyers97) §46, [\[Stroustrup00\]](032-bibliography.md#Stroustrup00) §15.4.3, [\[Taligent94\]](032-bibliography.md#Taligent94)

### <a name="sd-dtor"></a>Discussion : Rendre les destructeurs de classe de base publics et virtuels, ou protégés et non virtuels

La destruction doit-elle se comporter de manière virtuelle ? Autrement dit, la destruction via un pointeur vers une classe `base` doit-elle être autorisée ? Si oui, alors le destructeur de `base` doit être public pour être appelable, et virtuel, sinon son appel entraîne un comportement indéfini. Sinon, il doit être protégé pour que seules les classes dérivées puissent l'invoquer dans leurs propres destructeurs, et non virtuel puisqu'il n'a pas besoin de se comporter de manière virtuelle.

##### Exemple

Le cas courant pour une classe de base est qu'elle est destinée à avoir des classes dérivées publiques, et le code appelant utilisera donc quasi certainement quelque chose comme un `shared_ptr<base>` :

    class Base {
    public:
        ~Base();                   // MAUVAIS, non virtuel
        virtual ~Base();           // BON
        // ...
    };

    class Derived : public Base { /* ... */ };

    {
        unique_ptr<Base> pb = make_unique<Derived>();
        // ...
    } // ~pb n'invoque le destructeur correct que si ~Base est virtuel

Dans des cas plus rares, tels que les classes de politique, la classe est utilisée comme classe de base pour la commodité, et non pour un comportement polymorphe. Il est recommandé de rendre ces destructeurs protégés et non virtuels :

    class My_policy {
    public:
        virtual ~My_policy();      // MAUVAIS, public et virtuel
    protected:
        ~My_policy();              // BON
        // ...
    };

    template<class Policy>
    class customizable : Policy { /* ... */ }; // note : héritage privé

##### Remarque

Cette règle simple illustre un problème subtil et reflète les usages modernes de l'héritage et des principes de conception orientée objet.

Pour une classe de base `Base`, le code appelant pourrait tenter de détruire des objets dérivés via des pointeurs vers `Base`, par exemple lors de l'utilisation d'un `unique_ptr<Base>`. Si le destructeur de `Base` est public et non virtuel (le comportement par défaut), il peut être appelé accidentellement sur un pointeur qui pointe en réalité vers un objet dérivé, auquel cas le comportement de la suppression tentée est indéfini. Cette situation a conduit les normes de codage plus anciennes à imposer une exigence générale selon laquelle tous les destructeurs de classes de base doivent être virtuels. C'est excessif (même si c'est le cas courant) ; la règle devrait plutôt être de rendre les destructeurs de classes de base virtuels si et seulement s'ils sont publics.

Écrire une classe de base, c'est définir une abstraction (voir les Articles 35 à 37). Rappelez-vous que pour chaque fonction membre participant à cette abstraction, vous devez décider :

* Si elle doit se comporter de manière virtuelle ou non.
* Si elle doit être publiquement accessible à tous les appelants utilisant un pointeur vers `Base`, ou si elle doit rester un détail d'implémentation interne caché.

Comme décrit dans l'Article 39, pour une fonction membre ordinaire, le choix est entre lui permettre d'être appelé via un pointeur vers `Base` de manière non virtuelle (mais possiblement avec un comportement virtuel s'il invoque des fonctions virtuelles, comme dans les motifs NVI ou Template Method), de manière virtuelle, ou de ne pas le permettre du tout. Le motif NVI est une technique pour éviter les fonctions virtuelles publiques.

La destruction peut être considérée comme une opération de plus, bien qu'avec des sémantiques spéciales qui rendent les appels non virtuels dangereux ou incorrects. Pour un destructeur de classe de base, le choix est donc entre lui permettre d'être appelé via un pointeur vers `Base` de manière virtuelle ou de ne pas le permettre du tout ; « non virtuellement » n'est pas une option. Ainsi, un destructeur de classe de base est virtuel s'il peut être appelé (c'est-à-dire s'il est public), et non virtuel sinon.

Notez que le motif NVI ne peut pas être appliqué au destructeur car les constructeurs et destructeurs ne peuvent pas effectuer d'appels virtuels profonds. (Voir les Articles 39 et 55.)

Corollaire : lors de l'écriture d'une classe de base, écrivez toujours explicitement un destructeur, car celui généré implicitement est public et non virtuel. Vous pouvez toujours `=default` l'implémentation si le corps par défaut convient et que vous écrivez simplement la fonction pour lui donner la visibilité et la virtualité appropriées.

##### Exception

Certaines architectures de composants (par exemple COM et CORBA) n'utilisent pas de mécanisme de suppression standard et favorisent des protocoles différents pour la libération des objets. Suivez les motifs et les idiomes locaux, et adaptez cette règle en conséquence.

Considérez également ce cas rare :

* `B` est à la fois une classe de base et une classe concrète qui peut être instanciée par elle-même, et le destructeur doit donc être public pour que les objets `B` puissent être créés et détruits.
* Pourtant, `B` n'a aucune fonction virtuelle et n'est pas destinée à être utilisée de manière polymorphe, et bien que le destructeur soit public, il n'a pas besoin d'être virtuel.

Dans ce cas rare, bien que le destructeur doive être public, il peut y avoir une forte pression pour ne pas le rendre virtuel, car en tant que première fonction virtuelle, il entraînerait toute la surcharge de type d'exécution alors que la fonctionnalité ajoutée ne devrait jamais être nécessaire.

Dans ce cas rare, vous pourriez rendre le destructeur public et non virtuel mais documenter clairement que les objets plus dérivés ne doivent pas être utilisés de manière polymorphe en tant que `B`. C'est ce qui a été fait avec `std::unary_function`.

En général, toutefois, évitez les classes de base concrètes (voir l'Article 35). Par exemple, `unary_function` est un ensemble de typedefs qui n'était jamais destiné à être instancié de manière autonome. Il n'a tout simplement pas de sens de lui donner un destructeur public ; une meilleure conception serait de suivre le conseil de cet Article et de lui donner un destructeur protégé non virtuel.

**Références** : [\[SuttAlex05\]](032-bibliography.md#SuttAlex05) Article 50, [\[Cargill92\]](032-bibliography.md#Cargill92) pp. 77-79, 207, [\[Cline99\]](032-bibliography.md#Cline99) §21.06, 21.12-13, [\[Henricson97\]](032-bibliography.md#Henricson97) pp. 110-114, [\[Koenig97\]](032-bibliography.md#Koenig97) Chapitres 4, 11, [\[Meyers97\]](032-bibliography.md#Meyers97) §14, [\[Stroustrup00\]](032-bibliography.md#Stroustrup00) §12.4.2, [\[Sutter02\]](032-bibliography.md#Sutter02) §27, [\[Sutter04\]](032-bibliography.md#Sutter04) §18

### <a name="sd-noexcept"></a>Discussion : Utilisation de noexcept

???

### <a name="sd-never-fail"></a>Discussion : Les destructeurs, la libération de ressources et swap ne doivent jamais échouer

N'autorisez jamais qu'une erreur soit signalée depuis un destructeur, une fonction de libération de ressources (par exemple `operator delete`), ou une fonction `swap` à l'aide de `throw`. Il est quasi impossible d'écrire du code utile si ces opérations peuvent échouer, et même si quelque chose se passe mal, il n'a presque jamais de sens de réessayer. En particulier, les types dont le destructeur pourrait lever une exception sont formellement interdits d'utilisation avec la bibliothèque standard C++. La plupart des destructeurs sont désormais implicitement `noexcept` par défaut.

##### Exemple

    class Nefarious {
    public:
        Nefarious() { /* code qui pourrait lever une exception */ }    // ok
        ~Nefarious() { /* code qui pourrait lever une exception */ }   // MAUVAIS, ne devrait pas lever d'exception
        // ...
    };

1. Les objets `Nefarious` sont difficiles à utiliser en sécurité, même en tant que variables locales :


        void test(string& s)
        {
            Nefarious n;          // des ennuis se préparent
            string copy = s;      // copie la chaîne
        } // détruit copy puis n

    Ici, la copie de `s` pourrait lever une exception, et si c'est le cas et que le destructeur de `n` lève également une exception, le programme se terminera via `std::terminate` car deux exceptions ne peuvent pas être propagées simultanément.

2. Les classes ayant des membres ou des bases de type `Nefarious` sont également difficiles à utiliser en sécurité, car leurs destructeurs doivent invoquer le destructeur de `Nefarious` et sont empoisonnés de la même manière par son mauvais comportement :


        class Innocent_bystander {
            Nefarious member;     // oops, empoisonne le destructeur de la classe englobante
            // ...
        };

        void test(string& s)
        {
            Innocent_bystander i;  // encore des ennuis
            string copy2 = s;      // copie la chaîne
        } // détruit copy puis i

    Ici, si la construction de `copy2` lève une exception, nous avons le même problème car le destructeur de `i` peut également lever une exception, et dans ce cas nous invoquerons `std::terminate`.

3. Vous ne pouvez pas non plus créer fiablement des objets `Nefarious` globaux ou statiques :


        static Nefarious n;       // oops, toute exception de destructeur ne peut pas être capturée

4. Vous ne pouvez pas fiablement créer des tableaux de `Nefarious` :


        void test()
        {
            std::array<Nefarious, 10> arr; // cette ligne peut appeler std::terminate()
        }

    Le comportement des tableaux est indéfini en présence de destructeurs qui lèvent des exceptions, car il n'existe aucun comportement de retour arrière raisonnable qui puisse être conçu. Réfléchissez : quel code le compilateur peut-il générer pour la construction d'un `arr` où, si le constructeur du quatrième objet lève une exception, le code doit abandonner et, en mode de nettoyage, tente d'appeler les destructeurs des objets déjà construits … et l'un ou plusieurs de ces destructeurs lève une exception ? Il n'y a pas de réponse satisfaisante.

5. Vous ne pouvez pas utiliser des objets `Nefarious` dans les conteneurs standard :


        std::vector<Nefarious> vec(10);   // cette ligne peut appeler std::terminate()

    La bibliothèque standard interdit à tous les destructeurs utilisés avec elle de lever des exceptions. Vous ne pouvez pas stocker d'objets `Nefarious` dans des conteneurs standard ni les utiliser avec n'importe quelle autre partie de la bibliothèque standard.

##### Remarque

Ce sont des fonctions clés qui ne doivent pas échouer car elles sont nécessaires aux deux opérations clés de la programmation transactionnelle : annuler le travail si des problèmes sont rencontrés pendant le traitement, et engager le travail si aucun problème ne survient. S'il n'y a pas de moyen d'annuler en sécurité à l'aide d'opérations sans échec, alors le retour arrière sans échec est impossible à implémenter. S'il n'y a pas de moyen d'engager en sécurité les changements d'état à l'aide d'une opération sans échec (notamment, mais pas limité à, `swap`), alors l'engagement sans échec est impossible à implémenter.

Considérez les conseils et exigences suivants trouvés dans la norme C++ :

> Si un destructeur appelé pendant le démantèlement de la pile se termine avec une exception, terminate est appelé (15.5.1). Les destructeurs devraient donc généralement capturer les exceptions et ne pas les laisser se propager hors du destructeur. --[\[C++03\]](032-bibliography.md#Cplusplus03) §15.2(3)
>
> Aucune opération de destructeur définie dans la bibliothèque standard C++ (y compris le destructeur de tout type utilisé pour instancier un gabarit de la bibliothèque standard) ne lèvera d'exception. --[\[C++03\]](032-bibliography.md#Cplusplus03) §17.4.4.8(3)

Les fonctions de libération, y compris spécifiquement `operator delete` et `operator delete[]` surchargés, relèvent de la même catégorie, car elles sont également utilisées pendant le nettoyage en général, et pendant la gestion des exceptions en particulier, pour annuler un travail partiel qui doit être défait.
En plus des destructeurs et des fonctions de libération, les techniques courantes de sécurité face aux erreurs reposent également sur le fait que les opérations `swap` ne doivent jamais échouer — non pas parce qu'elles sont utilisées pour implémenter un retour arrière garanti, mais parce qu'elles sont utilisées pour implémenter un engagement garanti. Par exemple, voici une implémentation idiomatique de `operator=` pour un type `T` qui effectue une construction par copie suivie d'un appel à un `swap` sans échec :

    T& T::operator=(const T& other)
    {
        auto temp = other;
        swap(temp);
        return *this;
    }

(Voir aussi l'Article 56. ???)

Heureusement, lors de la libération d'une ressource, la marge d'échec est nettement plus réduite. Si vous utilisez les exceptions comme mécanisme de signalement d'erreurs, assurez-vous que ces fonctions gèrent toutes les exceptions et autres erreurs que leur traitement interne pourrait générer. (Pour les exceptions, il suffit d'entourer tout ce qui est sensible dans votre destructeur d'un bloc `try/catch(...)`.) C'est particulièrement important car un destructeur pourrait être appelé dans une situation de crise, telle qu'un échec d'allocation d'une ressource système (par exemple mémoire, fichiers, verrous, ports, fenêtres ou autres objets système).

Lorsque vous utilisez les exceptions comme mécanisme de gestion des erreurs, documentez toujours ce comportement en déclarant ces fonctions `noexcept`. (Voir l'Article 75.)

**Références** : [\[SuttAlex05\]](032-bibliography.md#SuttAlex05) Article 51 ; [\[C++03\]](032-bibliography.md#Cplusplus03) §15.2(3), §17.4.4.8(3), [\[Meyers96\]](032-bibliography.md#Meyers96) §11, [\[Stroustrup00\]](032-bibliography.md#Stroustrup00) §14.4.7, §E.2-4, [\[Sutter00\]](032-bibliography.md#Sutter00) §8, §16, [\[Sutter02\]](032-bibliography.md#Sutter02) §18-19

## <a name="sd-consistent"></a>Définir la copie, le déplacement et la destruction de manière cohérente

##### Raison

 ???

##### Remarque

Si vous définissez un constructeur de copie, vous devez également définir un opérateur d'assignation par copie.

##### Remarque

Si vous définissez un constructeur de déplacement, vous devez également définir un opérateur d'assignation par déplacement.

##### Exemple

    class X {
    public:
        X(const X&) { /* trucs */ }

        // MAUVAIS : oubli de définir également un opérateur d'assignation par copie

        X(x&&) noexcept { /* trucs */ }

        // MAUVAIS : oubli de définir également un opérateur d'assignation par déplacement

        // ...
    };

    X x1;
    X x2 = x1; // ok
    x2 = x1;   // piège : échoue à la compilation ou fait quelque chose de suspect

Si vous définissez un destructeur, vous ne devriez pas utiliser les opérations de copie ou de déplacement générées par le compilateur ; vous avez probablement besoin de définir ou de supprimer la copie et/ou le déplacement.

    class X {
        HANDLE hnd;
        // ...
    public:
        ~X() { /* trucs personnalisés, comme fermer hnd */ }
        // suspect : aucune mention de la copie ou du déplacement — que devient hnd ?
    };

    X x1;
    X x2 = x1; // piège : échoue à la compilation ou fait quelque chose de suspect
    x2 = x1;   // piège : échoue à la compilation ou fait quelque chose de suspect

Si vous définissez la copie, et qu'une base ou un membre a un type qui définit une opération de déplacement, vous devriez également définir une opération de déplacement.

    class X {
        string s; // définit des opérations de déplacement plus efficaces
        // ... autres membres de données ...
    public:
        X(const X&) { /* trucs */ }
        X& operator=(const X&) { /* trucs */ }

        // MAUVAIS : oubli de définir également la construction par déplacement et l'assignation par déplacement
        // (pourquoi les « trucs » personnalisés n'ont-ils pas été répétés ici ?)
    };

    X test()
    {
        X local;
        // ...
        return local;  // piège : sera inefficace et/ou fera la mauvaise chose
    }

Si vous définissez l'un du constructeur de copie, de l'opérateur d'assignation par copie ou du destructeur, vous devriez probablement définir les autres.

##### Remarque

Si vous devez définir l'une de ces cinq fonctions, cela signifie qu'elle doit faire plus que son comportement par défaut — et les cinq sont interdépendantes de manière asymétrique. Voici comment :

* Si vous écrivez/désactivez l'un du constructeur de copie ou de l'opérateur d'assignation par copie, vous avez probablement besoin de faire de même pour l'autre : si l'un effectue un travail « spécial », l'autre devrait probablement en faire autant car les deux fonctions devraient avoir des effets similaires. (Voir l'Article 53, qui développe ce point isolément.)
* Si vous écrivez explicitement les fonctions de copie, vous avez probablement besoin d'écrire le destructeur : si le travail « spécial » dans le constructeur de copie est d'allouer ou de dupliquer une ressource (par exemple mémoire, fichier, socket), vous devez la libérer dans le destructeur.
* Si vous écrivez explicitement le destructeur, vous avez probablement besoin d'écrire ou de désactiver explicitement la copie : si vous devez écrire un destructeur non trivial, c'est souvent parce que vous devez libérer manuellement une ressource que l'objet détenait. Dans ce cas, il est probable que ces ressources nécessitent une duplication soignée, et vous devez alors prêter attention à la manière dont les objets sont copiés et assignés, ou désactiver complètement la copie.

Dans de nombreux cas, la détention de ressources correctement encapsulées à l'aide d'objets « propriétaires » RAII peut éliminer le besoin d'écrire ces opérations vous-même. (Voir l'Article 13.)

Préférez les membres spéciaux générés par le compilateur (y compris `=default`) ; seuls ceux-ci peuvent être classés comme « triviaux », et au moins un fournisseur majeur de bibliothèque standard optimise fortement pour les classes ayant des membres spéciaux triviaux. Cela deviendra probablement une pratique courante.

**Exceptions** : lorsque l'une des fonctions spéciales est déclarée uniquement pour la rendre non publique ou virtuelle, mais sans sémantique spéciale, cela n'implique pas que les autres soient nécessaires.
Dans de rares cas, les classes ayant des membres de types étranges (tels que des membres de référence) font exception car elles ont des sémantiques de copie particulières.
Dans une classe détenant une référence, vous avez probablement besoin d'écrire le constructeur de copie et l'opérateur d'assignation, mais le destructeur par défaut fait déjà la bonne chose. (Notez que l'utilisation d'un membre de référence est presque toujours incorrecte.)

**Références** : [\[SuttAlex05\]](032-bibliography.md#SuttAlex05) Article 52 ; [\[Cline99\]](032-bibliography.md#Cline99) §30.01-14, [\[Koenig97\]](032-bibliography.md#Koenig97) §4, [\[Stroustrup00\]](032-bibliography.md#Stroustrup00) §5.5, §10.4, [\[SuttHysl04b\]](032-bibliography.md#SuttHysl04b)

Résumé des règles de gestion des ressources :

* [Fournir une sécurité forte des ressources ; c'est-à-dire ne jamais fuiter ce que vous considérez comme une ressource](028-discussion.md#cr-safety)
* [Ne jamais retourner ou lever une exception en détenant une ressource non détenue par un gestionnaire](028-discussion.md#cr-never)
* [Un pointeur ou une référence « brute » n'est jamais un gestionnaire de ressource](028-discussion.md#cr-raw)
* [Ne jamais laisser un pointeur survivre à l'objet qu'il pointe](028-discussion.md#cr-outlive)
* [Utiliser des gabarits pour exprimer les conteneurs (et autres gestionnaires de ressources)](028-discussion.md#cr-templates)
* [Retourner les conteneurs par valeur (en s'appuyant sur le déplacement ou l'omission de copie pour l'efficacité)](028-discussion.md#cr-value-return)
* [Si une classe est un gestionnaire de ressource, elle a besoin d'un constructeur, d'un destructeur et d'opérations de copie et/ou de déplacement](028-discussion.md#cr-handle)
* [Si une classe est un conteneur, donnez-lui un constructeur par liste d'initialisateurs](028-discussion.md#cr-list)

### <a name="cr-safety"></a>Discussion : Fournir une sécurité forte des ressources ; c'est-à-dire ne jamais fuiter ce que vous considérez comme une ressource

##### Raison

Prévenir les fuites. Les fuites peuvent entraîner une dégradation des performances, des erreurs mystérieuses, des plantages système et des violations de sécurité.

**Formulation alternative** : Faire en sorte que chaque ressource soit représentée par un objet d'une classe gérant son cycle de vie.

##### Exemple

    template<class T>
    class Vector {
    private:
        T* elem;   // sz éléments sur le tas, détenus par l'objet de la classe
        int sz;
        // ...
    };

Cette classe est un gestionnaire de ressource. Elle gère le cycle de vie des `T`. Pour ce faire, `Vector` doit définir ou supprimer [les opérations de copie, de déplacement et de destruction](007-class.md#rc-five).

##### Exemple

    ??? ressource non mémoire « étrange » ???

##### Application

La technique de base pour prévenir les fuites est de faire en sorte que chaque ressource soit détenue par un gestionnaire de ressource doté d'un destructeur approprié. Un vérificateur peut trouver les « `new` nus ». Étant donné une liste de fonctions d'allocation de style C (par exemple `fopen()`), un vérificateur peut également trouver les utilisations non gérées par un gestionnaire de ressource. En général, les « pointeurs nus » peuvent être considérés avec suspicion, signalés et/ou analysés. Une liste complète des ressources ne peut pas être générée sans intervention humaine (la définition de « ressource » est nécessairement trop générale), mais un outil peut être « paramétré » avec une liste de ressources.

### <a name="cr-never"></a>Discussion : Ne jamais retourner ou lever une exception en détenant une ressource non détenue par un gestionnaire

##### Raison

Ce serait une fuite.

##### Exemple

    void f(int i)
    {
        FILE* f = fopen("un fichier", "r");
        ifstream is { "un autre fichier" };
        // ...
        if (i == 0) return;
        // ...
        fclose(f);
    }

Si `i == 0`, le descripteur de fichier pour `un fichier` est perdu. En revanche, le `ifstream` pour `un autre fichier` fermera correctement son fichier (à la destruction). Si vous devez utiliser un pointeur explicite plutôt qu'un gestionnaire de ressource avec des sémantiques spécifiques, utilisez un `unique_ptr` ou un `shared_ptr` avec un libérateur personnalisé :

    void f(int i)
    {
        unique_ptr<FILE, int(*)(FILE*)> f(fopen("un fichier", "r"), fclose);
        // ...
        if (i == 0) return;
        // ...
    }

Mieux :

    void f(int i)
    {
        ifstream input {"un fichier"};
        // ...
        if (i == 0) return;
        // ...
    }

##### Application

Un vérificateur doit considérer tous les « pointeurs nus » comme suspects.
Un vérificateur devra probablement s'appuyer sur une liste de ressources fournie par un humain.
Pour commencer, nous connaissons les conteneurs de la bibliothèque standard, `string` et les pointeurs intelligents.
L'utilisation de `span` et `string_view` devrait beaucoup aider (ce ne sont pas des gestionnaires de ressources).

### <a name="cr-raw"></a>Discussion : Un pointeur ou une référence « brute » n'est jamais un gestionnaire de ressource

##### Raison

Pour pouvoir distinguer les propriétaires des vues.

##### Remarque

Ceci est indépendant de la manière dont vous « écrivez » le pointeur : `T*`, `T&`, `Ptr<T>` et `Range<T>` ne sont pas des propriétaires.

### <a name="cr-outlive"></a>Discussion : Ne jamais laisser un pointeur survivre à l'objet qu'il pointe

##### Raison

Pour éviter des erreurs extrêmement difficiles à trouver. Le déréférencement d'un tel pointeur est un comportement indéfini et pourrait entraîner des violations du système de types.

##### Exemple

    string* bad()   // vraiment mauvais
    {
        vector<string> v = { "Ceci", "va", "causer", "des", "ennuis", "!" };
        // fuite d'un pointeur vers un membre détruit d'un objet détruit (v)
        return &v[0];
    }

    void use()
    {
        string* p = bad();
        vector<int> xx = {7, 8, 9};
        // comportement indéfini : x n'est peut-être pas la chaîne "Ceci"
        string x = *p;
        // comportement indéfini : nous ne savons pas ce (si quelque chose) est alloué à l'emplacement p
        *p = "Malveillant!";
    }

Les `string` de `v` sont détruites à la sortie de `bad()` et `v` lui-même l'est aussi. Le pointeur retourné pointe vers une mémoire non allouée sur le tas. Cette mémoire (pointée par `p`) pourrait avoir été réallouée d'ici l'exécution de `*p`. Il n'y a peut-être pas de `string` à lire et une écriture via `p` pourrait facilement corrompre des objets de types non liés.

##### Application

La plupart des compilateurs émettent déjà des avertissements pour les cas simples et disposent des informations pour en faire plus. Considérez tout pointeur retourné par une fonction comme suspect. Utilisez des conteneurs, des gestionnaires de ressources et des vues (par exemple `span`, connu pour ne pas être un gestionnaire de ressource) pour réduire le nombre de cas à examiner. Pour commencer, considérez toute classe ayant un destructeur comme gestionnaire de ressource.

### <a name="cr-templates"></a>Discussion : Utiliser des gabarits pour exprimer les conteneurs (et autres gestionnaires de ressources)

##### Raison

Pour fournir une manipulation statiquement sûre du type des éléments.

##### Exemple

    template<typename T> class Vector {
        // ...
        T* elem;   // pointe vers sz éléments de type T
        int sz;
    };

### <a name="cr-value-return"></a>Discussion : Retourner les conteneurs par valeur (en s'appuyant sur le déplacement ou l'omission de copie pour l'efficacité)

##### Raison

Pour simplifier le code et éliminer le besoin d'une gestion explicite de la mémoire. Pour amener un objet dans une portée englobante, étendant ainsi son cycle de vie.

**Voir aussi** : [F.20, la règle générale sur les valeurs de sortie « out »](006-functions.md#rf-out)

##### Exemple

    vector<int> get_large_vector()
    {
        return ...;
    }

    auto v = get_large_vector(); //  le retour par valeur est ok, la plupart des compilateurs modernes feront l'omission de copie

##### Exception

Voir les Exceptions dans [F.20](006-functions.md#rf-out).

##### Application

Vérifier les pointeurs et références retournés par des fonctions et voir s'ils sont assignés à des gestionnaires de ressources (par exemple à un `unique_ptr`).

### <a name="cr-handle"></a>Discussion : Si une classe est un gestionnaire de ressource, elle a besoin d'un constructeur, d'un destructeur et d'opérations de copie et/ou de déplacement

##### Raison

Pour fournir un contrôle complet du cycle de vie de la ressource. Pour fournir un ensemble cohérent d'opérations sur la ressource.

##### Exemple

    ??? Manipulation de pointeurs

##### Remarque

Si tous les membres sont des gestionnaires de ressources, reposez-vous sur les opérations générées par le compilateur lorsque c'est possible.

    template<typename T> struct Named {
        string name;
        T value;
    };

`Named` a alors un constructeur par défaut, un destructeur et des opérations de copie et de déplacement efficaces, à condition que `T` en ait.

##### Application

En général, un outil ne peut pas savoir si une classe est un gestionnaire de ressources. Cependant, si une classe a certaines des [opérations par défaut](007-class.md#ss-ctor), elle devrait les avoir toutes, et si une classe a un membre qui est un gestionnaire de ressources, elle devrait être considérée comme gestionnaire de ressources.

### <a name="cr-list"></a>Discussion : Si une classe est un conteneur, donnez-lui un constructeur par liste d'initialisateurs

##### Raison

Il est courant d'avoir besoin d'un ensemble initial d'éléments.

##### Exemple

    template<typename T> class Vector {
    public:
        Vector(std::initializer_list<T>);
        // ...
    };

    Vector<string> vs { "Nygaard", "Ritchie" };

##### Application

Quand une classe est-elle un conteneur ? ???
