# <a name="s-glossary"></a>Glossaire

Une définition relativement informelle des termes utilisés dans les lignes directrices (basée sur le glossaire de [Programming: Principles and Practice using C++](https://www.stroustrup.com/programming.html)).

Plus d’informations sur de nombreux sujets concernant C++ sont disponibles sur le site de la [Standard C++ Foundation](https://isocpp.org).

* *ABI* : Interface binaire d’application, une spécification d’une plate‑forme matérielle spécifique combinée avec le système d’exploitation. À ne pas confondre avec l’API.  
* *abstract class* : classe qui ne peut pas être directement utilisée pour créer des objets ; souvent employée pour définir une interface vers des classes dérivées.  
  Une classe devient abstraite en contenant une fonction virtuelle pure ou uniquement des constructeurs protégés.  
* *abstraction* : description de quelque chose qui ignore délibérément et sélectivement (cachant) des détails (par ex. les détails d’implémentation) ; ignorance sélective.  
* *address* : valeur qui nous permet de localiser un objet dans la mémoire d’un ordinateur.  
* *algorithm* : procédure ou formule permettant de résoudre un problème ; une suite finie d’étapes de calcul produisant un résultat.  
* *alias* : manière alternative de désigner un objet ; souvent un nom, un pointeur ou une référence.  
* *API* : Interface de programmation d’application, un ensemble de fonctions qui assure la communication entre différents composants logiciels. À ne pas confondre avec l’ABI.  
* *application* : programme ou ensemble de programmes considéré comme une entité par ses utilisateurs.  
* *approximation* : chose (par ex. une valeur ou une conception) qui se rapproche du parfait ou de l’idéal (valeur ou conception). Une approximation résulte souvent de compromis entre plusieurs idéaux.  
* *argument* : valeur passée à une fonction ou à un modèle, accessible via un paramètre.  
* *array* : séquence homogène d’éléments, généralement indexée, par ex. `[0:max)`.  
* *assertion* : instruction insérée dans un programme pour affirmer que quelque chose doit toujours être vrai à ce point du programme.  
* *base class* : type destiné à être dérivé (par ex. possède une fonction virtuelle non `final`), et les objets de ce type sont destinés à être utilisés uniquement de façon indirecte (par ex. via un pointeur). \[Dans le sens strict, « classe de base » pourrait être définie comme « quelque chose dont nous dérivons », mais nous la définissons selon l’intention du concepteur de classe.\] Typiquement, une classe de base possède une ou plusieurs fonctions virtuelles.  
* *bit* : unité de base d’information dans un ordinateur. Un bit peut prendre la valeur 0 ou la valeur 1.  
* *bug* : une erreur dans un programme.  
* *byte* (octet) : unité de base d’adressage dans la plupart des ordinateurs. Un octet contient généralement 8 bits.  
* *class* : type défini par l’utilisateur pouvant contenir des membres de données, des membres de fonctions et des types membres.  
* *code* : programme ou partie d’un programme ; terme ambigu utilisé à la fois pour le code source et le code objet.  
* *compiler* : programme qui transforme le code source en code objet.  
* *complexity* : notion ou mesure difficile à définir précisément de la difficulté à construire une solution à un problème ou de la solution elle‑même.  
  Parfois, le terme complexité est utilisé simplement pour désigner une estimation du nombre d’opérations nécessaires à l’exécution d’un algorithme.  
* *computation* : exécution d’un bout de code, généralement à partir d’entrées et produisant des sorties.  
* *concept* : (1) notion, idée ; (2) ensemble d’exigences, généralement pour un argument de modèle.  
* *concrete type* : type qui n’est pas une classe de base, et dont les objets sont destinés à être utilisés directement (pas seulement via un pointeur/indirection), dont la taille est connue, et qui peut typiquement être alloué où le programmeur le souhaite (par ex. sur la pile ou statiquement).  
* *constant* : valeur qui ne peut pas être modifiée (dans une portée donnée) ; non mutable.  
* *constructor* : opération qui initialise (« construit ») un objet. Typiquement, un constructeur établit un invariant et acquiert souvent les ressources nécessaires à l’utilisation d’un objet (ressources qui sont généralement libérées par le destructeur).  
* *container* : objet qui contient des éléments (autres objets).  
* *copy* : opération qui rend deux objets dotés de valeurs égales (comparables). Voir aussi *move*.  
* *correctness* : un programme ou une partie de programme est correct s’il respecte sa spécification.  
  Malheureusement, une spécification peut être incomplète ou incohérente, ou ne pas répondre aux attentes raisonnables des utilisateurs.  
  Ainsi, pour produire du code acceptable, il faut parfois faire plus que se conformer à la spécification formelle.  
* *cost* : dépense (ex. en temps de programmation, temps d’exécution ou espace) nécessaire à la production d’un programme ou à son exécution.  
  Idéalement, le coût devrait être fonction de la complexité.  
* *customization point* : ??? @TODO-LINK (définition manquante).  
* *data* : valeurs utilisées dans une computation.  
* *debugging* : recherche et élimination d’erreurs dans un programme ; généralement beaucoup moins systématique que les tests.  
* *declaration* : spécification d’un nom avec son type dans un programme.  
* *definition* : déclaration d’une entité qui fournit toutes les informations nécessaires pour compléter un programme l’utilisant.  
  Définition simplifiée : déclaration qui alloue de la mémoire.  
* *derived class* : classe dérivée d’une ou plusieurs classes de base.  
* *design* : description globale du fonctionnement d’un logiciel afin de répondre à sa spécification.  
* *destructor* : opération invoquée implicitement (appelée) lorsqu’un objet est détruit (par ex. à la fin d’une portée). Souvent, il libère des ressources.  
* *encapsulation* : protection de ce qui doit rester privé (par ex. les détails d’implémentation) contre tout accès non autorisé.  
* *error* : incompatibilité entre les attentes raisonnables du comportement du programme (souvent exprimées comme exigences ou guide utilisateur) et ce que le programme fait réellement.  
* *executable* : programme prêt à être exécuté sur un ordinateur.  
* *feature creep* : tendance à ajouter des fonctionnalités superflues à un programme « juste au cas où ».  
* *file* : conteneur d’informations permanentes dans un ordinateur.  
* *floating-point number* : nombre à virgule flottante, approximation informatique d’un nombre réel, comme 7,93 et 10,78e‑3.  
* *function* : unité de code nommée pouvant être invoquée (appelée) depuis différentes parties d’un programme ; unité logique de calcul.  
* *generic programming* : style de programmation centré sur la conception et l’implémentation efficace d’algorithmes.  
  Un algorithme générique fonctionne pour tous les types d’arguments qui répondent à ses exigences. En C++, la programmation générique utilise généralement les modèles.  
* *global variable* : objet nommé au niveau de l’espace de noms, techniquement.  
* *handle* : classe permettant l’accès à un autre objet via un pointeur ou une référence membre. Voir aussi *resource*, *owner*, *copy*, *move*.  
* *header* : fichier contenant des déclarations utilisées pour partager des interfaces entre différentes parties d’un programme.  
* *hiding* : action d’empêcher qu’une information soit directement vue ou accédée.  
  Par exemple, un nom provenant d’un espace de noms imbriqué (interne) peut empêcher l’utilisation directe du même nom provenant d’un espace de noms externe.  
* *ideal* : version parfaite de quelque chose que nous visons. En général, des compromis sont nécessaires et l’on se satisfait d’une approximation.  
* *implementation* : (1) action d’écrire et de tester du code ; (2) code qui implémente un programme.  
* *infinite loop* : boucle dont la condition de terminaison ne devient jamais vraie. Voir *iteration*.  
* *infinite recursion* : récursion qui ne se termine pas tant que la machine ne manque pas de mémoire pour stocker les appels.  
  En réalité, une telle récursion n’est jamais infinie mais est interrompue par une erreur matérielle.  
* *information hiding* : séparation de l’interface et de l’implémentation, cachant ainsi les détails d’implémentation non destinés à l’utilisateur et fournissant une abstraction.  
* *initialize* : fournir à un objet sa première (initiale) valeur.  
* *input* : valeurs utilisées par une computation (par ex. arguments de fonction et caractères saisis au clavier).  
* *integer* : nombre entier, tel que 42 ou ‑99.  
* *interface* : déclaration ou ensemble de déclarations spécifiant comment une portion de code (par ex. une fonction ou une classe) peut être appelée.  
* *invariant* : chose qui doit toujours être vraie à un moment (ou à des moments) donné(s) d’un programme ; généralement utilisé pour décrire l’état (ensemble de valeurs) d’un objet ou l’état d’une boucle avant d’entrer dans l’instruction répétée.  
* *iteration* : action d’exécuter de façon répétée un morceau de code ; voir *recursion*.  
* *iterator* : objet identifiant un élément d’une séquence.  
* *ISO* : Organisation internationale de normalisation. Le langage C++ est une norme ISO, ISO/IEC 14882. Plus d’informations sur [iso.org](https://iso.org).  
* *library* : collection de types, fonctions, classes, etc. implémentant un ensemble de facilités (abstractions) destinées à être éventuellement utilisées dans plusieurs programmes.  
* *lifetime* : intervalle de temps depuis l’initialisation d’un objet jusqu’à ce qu’il devienne inutilisable (sortie de portée, suppression, ou terminaison du programme).  
* *linker* : programme qui combine des fichiers d’object code et des bibliothèques en un programme exécutable.  
* *literal* : notation qui spécifie directement une valeur, par ex. 12 indiquant la valeur entière « douze ».  
* *loop* : morceau de code exécuté de façon répétée ; en C++, typiquement une instruction *for* ou une instruction `while`.  
* *move* : opération qui transfère une valeur d’un objet à un autre en laissant derrière une valeur représentant « vide ». Voir aussi *copy*.  
* *move-only type* : type concret qui est déplaçable mais pas copiable.  
* *mutable* : modifiable ; opposé de *immutable*, *const*, *invariable*.  
* *object* : (1) région de mémoire initialisée d’un type connu contenant une valeur de ce type ; (2) région de mémoire.  
* *object code* : sortie d’un compilateur destinée à être entrée d’un éditeur de liens (pour que celui‑ci produise du code exécutable).  
* *object file* : fichier contenant du code objet.  
* *object-oriented programming* : (POO) style de programmation centré sur la conception et l’utilisation de classes et de hiérarchies de classes.  
* *operation* : chose capable d’effectuer une action, telle qu’une fonction ou un opérateur.  
* *output* : valeurs produites par une computation (par ex. résultat de fonction ou lignes de caractères affichées à l’écran).  
* *overflow* : production d’une valeur qui ne peut pas être stockée dans la destination prévue.  
* *overload* : définition de deux fonctions ou opérateurs portant le même nom mais avec des types d’argument (ou d’opérande) différents.  
* *override* : définition d’une fonction dans une classe dérivée avec le même nom et les mêmes types d’arguments qu’une fonction virtuelle de la classe de base, ce qui rend la fonction appelable via l’interface définie par la classe de base.  
* *owner* : objet responsable de la libération d’une ressource.  
* *paradigm* : terme un peu prétentieux désignant le style de conception ou de programmation ; souvent utilisé avec l’implication (erronée) qu’un paradigme est supérieur à tous les autres.  
* *parameter* : déclaration d’une entrée explicite pour une fonction ou un modèle. Lors de l’appel, la fonction peut accéder aux arguments via les noms de ses paramètres.  
* *pointer* : (1) valeur utilisée pour identifier un objet typé en mémoire ; (2) variable contenant une telle valeur.  
* *post-condition* : condition qui doit être vraie à la sortie d’un morceau de code, tel qu’une fonction ou une boucle.  
* *pre-condition* : condition qui doit être vraie à l’entrée d’un morceau de code, tel qu’une fonction ou une boucle.  
* *program* : code (éventuellement avec des données associées) suffisamment complet pour être exécuté par un ordinateur.  
* *programming* : art d’exprimer des solutions à des problèmes sous forme de code.  
* *programming language* : langage permettant d’exprimer des programmes.  
* *pseudo code* : description d’une computation écrite dans une notation informelle plutôt que dans un langage de programmation.  
* *pure virtual function* : fonction virtuelle qui doit être redéfinie dans une classe dérivée.  
* *RAII* : (« Resource Acquisition Is Initialization ») technique de base pour la gestion de ressources basée sur les portées.  
* *range* : séquence de valeurs pouvant être décrite par un point de départ et un point de fin. Par exemple, `[0:5)` désigne les valeurs 0, 1, 2, 3 et 4.  
* *recursion* : fait pour une fonction de s’appeler elle‑même ; voir aussi *iteration*.  
* *reference* : (1) valeur décrivant la localisation d’une valeur typée en mémoire ; (2) variable contenant une telle valeur.  
* *regular expression* : notation décrivant des motifs dans des chaînes de caractères.  
* *regular* : type semi‑régulier comparable pour l’égalité (voir le concept `std::regular`). Après une copie, l’objet copié compare égal à l’original. Un type régulier se comporte de façon similaire aux types intégrés comme `int` et peut être comparé avec `==`. En particulier, un objet d’un type régulier peut être copié et le résultat de la copie est un objet distinct qui compare égal à l’original. Voir également *type semi‑régulier*.  
* *requirement* : (1) description du comportement attendu d’un programme ou d’une partie de programme ; (2) description des hypothèses qu’une fonction ou un modèle fait sur ses arguments.  
* *resource* : chose acquise et qui doit être libérée plus tard, comme un handle de fichier, un verrou, ou de la mémoire. Voir aussi *handle*, *owner*.  
* *rounding* : conversion d’une valeur vers la valeur mathématiquement la plus proche d’un type de précision moindre.  
* *RTTI* : informations de type à l’exécution. ??? @TODO-LINK  
* *scope* : région du texte du programme (code source) dans laquelle un nom peut être référencé.  
* *semiregular* : type concret copiable (y compris déplaçable) et par défaut constructible (voir le concept `std::semiregular`). Le résultat d’une copie est un objet indépendant avec la même valeur que l’original. Un type semi‑régulier se comporte approximativement comme un type intégré comme `int`, mais éventuellement sans opérateur `==`. Voir également *type régulier*.  
* *sequence* : éléments pouvant être parcourus dans un ordre linéaire.  
* *software* : collection de morceaux de code et de données associées ; souvent utilisé de façon interchangeable avec *programme*.  
* *source code* : code produit par un programmeur et (en principe) lisible par d’autres programmeurs.  
* *source file* : fichier contenant du code source.  
* *specification* : description de ce qu’un morceau de code doit faire.  
* *standard* : définition officielle convenue d’un élément, comme un langage de programmation.  
* *state* : ensemble de valeurs.  
* *STL* : les conteneurs, itérateurs et algorithmes de la bibliothèque standard.  
* *string* : séquence de caractères.  
* *style* : ensemble de techniques de programmation conduisant à une utilisation cohérente des fonctionnalités du langage ; parfois utilisé de façon très restreinte pour ne désigner que les règles de bas niveau de nommage et d’apparence du code.  
* *subtype* : type dérivé ; type qui possède toutes les propriétés d’un type et possiblement davantage.  
* *supertype* : type de base ; type qui possède un sous‑ensemble des propriétés d’un type.  
* *system* : (1) programme ou ensemble de programmes exécutant une tâche sur un ordinateur ; (2) abréviation de « système d’exploitation », c’est‑à‑dire l’environnement d’exécution fondamental et les outils d’un ordinateur.  
* *TS* : [Spécification technique](https://www.iso.org/deliverables-all.html?type=ts), une spécification technique traite d’un travail encore en cours de développement ou lorsqu’il est prévu qu’une norme internationale sera adoptée à terme, mais pas immédiatement. Elle est publiée pour une utilisation immédiate, tout en offrant un moyen de recueillir des retours. L’objectif est qu’elle finisse par être transformée et republiée comme norme internationale.  
* *template* : classe ou fonction paramétrée par un ou plusieurs types ou valeurs (à la compilation) ; construction de base du langage C++ supportant la programmation générique.  
* *testing* : recherche systématique d’erreurs dans un programme.  
* *trade‑off* : résultat d’un équilibrage de plusieurs critères de conception et d’implémentation.  
* *truncation* : perte d’information lors d’une conversion d’un type vers un autre qui ne peut pas représenter exactement la valeur à convertir.  
* *type* : chose qui définit un ensemble de valeurs possibles et un ensemble d’opérations pour un objet.  
* *uninitialized* : état (indéfini) d’un objet avant son initialisation.  
* *unit* : (1) mesure standard donnant un sens à une valeur (par ex. km pour une distance) ; (2) partie distinguée (par ex. nommée) d’un tout plus grand.  
* *use case* : utilisation spécifique (généralement simple) d’un programme destinée à tester sa fonctionnalité et à démontrer son objectif.  
* *value* : ensemble de bits en mémoire interprété selon un type.  
* *value type* : terme utilisé par certains pour désigner un type régulier ou semi‑régulier.  
* *variable* : objet nommé d’un type donné ; contient une valeur sauf s’il est non initialisé.  
* *virtual function* : fonction membre pouvant être redéfinie dans une classe dérivée.  
* *word* : unité de base de mémoire dans un ordinateur, souvent utilisée pour contenir un entier.