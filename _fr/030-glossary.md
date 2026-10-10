# <a name="s-glossary"></a>Glossaire

* *ABI*: Interface binaire d'application, une spécification pour une plateforme matérielle spécifique combinée avec le système d'exploitation. Contrairement à l'API.

* *abstract class*: une classe qui ne peut pas être directement utilisée pour créer des objets, souvent utilisée pour définir une interface aux classes dérivées.  
  Une classe devient abstraite en disposant d'une fonction pure ou uniquement de constructeurs protégés.

* *abstraction*: une description de quelque chose qui ignore de manière sélective et délibérée les détails (par ex., les détails d'implémentation) ; ignorance sélective.

* *address*: une valeur qui permet de localiser un objet en mémoire d'un ordinateur.

* *algorithm*: une procédure ou une formule pour résoudre un problème ; une séquence finie d'étapes computationnelles pour produire un résultat.

* *alias*: une façon alternative de référer à un objet ; souvent un nom, un pointeur ou une référence.

* *API*: Interface de Programmation d'Application, un ensemble de fonctions qui forment la communication entre divers composants logiciels ; Contrairement à l'API.

* *application*: un programme ou une collection de programmes considéré comme une entité par ses utilisateurs.

* *approximation*: quelque chose (ex., une valeur ou un design) qui est proche de la perfection ou de l'idéal ; souvent, une approximation résulte de compromis entre idéaux.

* *argument*: une valeur transmise à une fonction ou un modèle, à laquelle on accède via un paramètre.

* *array*: une séquence homogène d'éléments, généralement numérotés, par ex. `[0:max)`.

* *assertion*: une déclaration insérée dans un programme pour affirmer qu'une chose doit toujours être vraie à ce point du programme.

* *base class*: un type qui est destiné à être dérivé de (par ex., possède une fonction virtuelle non `final`), et les objets de ce type sont destinés à être utilisés uniquement de façon indirecte (ex., par pointeur).  
  [Dans des termes stricts, « base class » pourrait être définie comme « quelque chose que nous dérivons », mais nous la définissons en fonction de l'intention du concepteur de la classe.]  
  En général, une classe de base possède une ou plusieurs fonctions virtuelles.

* *bit*: l'unité de base d'information dans un ordinateur. Un bit peut avoir la valeur 0 ou 1.

* *bug*: une erreur dans un programme.

* *byte*: l'unité de base d'adressage dans la plupart des ordinateurs. En général, un octet contient 8 bits.

* *class*: un type défini par l'utilisateur pouvant contenir des membres de données, des fonctions membres et des types membres.

* *code*: un programme ou une partie d'un programme ; utilisé de façon ambiguë pour le code source et le code objet.

* *compiler*: un programme qui convertit le code source en code objet.

* *complexity*: une notion ou mesure difficile à définir précisément de la difficulté à construire une solution à un problème ou de la solution elle‑même.

* *computation*: l'exécution d'un code, généralement en prenant une entrée et en produisant une sortie.

* *concept*: (1) une notion ou une idée ; (2) un ensemble d'exigences, généralement pour un argument de modèle.

* *concrete type*: un type qui n’est pas une classe de base, et les objets de ce type sont destinés à être utilisés directement (pas seulement via un pointeur/indirection). Sa taille est connue, et il peut typiquement être alloué partout où le programmeur le souhaite (ex., pile ou statiquement).

* *constant*: une valeur qui ne peut pas être modifiée (dans un certain scope) ; non mutable.

* *constructor*: une opération qui initialise (« construit ») un objet.  
  En général, un constructeur établit un invariant et obtient souvent les ressources nécessaires à l'utilisation de l'objet (qui sont ensuite généralement libérées par un destructeur).

* *container*: un objet qui contient des éléments (autres objets).

* *copy*: une opération qui fait que deux objets ont des valeurs qui se comparent égales. Voir aussi move.

* *correctness*: un programme ou une partie d'un programme est correct s'il satisfait à sa spécification.  
  Malheureusement, une spécification peut être incomplète ou incohérente, ou ne pas répondre aux attentes raisonnables des utilisateurs.  
  Ainsi, pour produire un code acceptable, nous devons parfois faire plus que simplement suivre la spécification formelle.

* *cost*: le coût (ex. en temps de programme, en temps d'exécution ou en espace) de la production d'un programme ou de son exécution. Idéalement, le coût devrait être une fonction de la complexité.

* *customization point*: ???

* *data*: valeurs utilisées dans une computation.

* *debugging*: l'action de rechercher et de supprimer des erreurs d'un programme ; généralement beaucoup moins systématique que le testing.

* *declaration*: la spécification d'un nom avec son type dans un programme.

* *definition*: une déclaration d'une entité qui fournit toutes les informations nécessaires pour compléter un programme utilisant l'entité. Définition simplifiée : une déclaration qui alloue de la mémoire.

* *derived class*: une classe dérivée d'une ou plusieurs classes de base.

* *design*: une description globale de la manière dont une pièce de logiciel doit fonctionner pour satisfaire à sa spécification.

* *destructor*: une opération qui est implicitement invoquée (appelée) lorsqu'un objet est détruit (ex., à la fin d'un scope). Souvent, il libère des ressources.

* *encapsulation*: protéger quelque chose censé être privé (ex., les détails d'implémentation) d'un accès non autorisé.

* *error*: un écart entre les attentes raisonnables du comportement d'un programme (souvent exprimé comme une exigence ou un guide d'utilisateur) et ce que le programme fait réellement.

* *executable*: un programme prêt à être exécuté sur un ordinateur.

* *feature creep*: une tendance à ajouter des fonctionnalités excessives à un programme « juste au cas où » .

* *file*: un conteneur d'informations permanentes dans un ordinateur.

* *floating-point number*: approximation d'un nombre réel par un ordinateur, comme 7.93 ou 10.78e-3.

* *function*: une unité de code nommée pouvant être invoquée (appelée) depuis différentes parties d'un programme ; une unité logique de calcul.

* *generic programming*: un style de programmation axé sur la conception et l'implémentation efficace d'algorithmes. Un algorithme générique fonctionne pour tous les types d'arguments qui satisfont à ses exigences. En C++, la programmation générique utilise typiquement des modèles.

* *global variable*: techniquement, un objet nommé en espace de nom.

* *handle*: une classe qui permet d'accéder à une autre via un pointeur ou une référence membre. Voir aussi resource, copy, move.

* *header*: un fichier contenant des déclarations utilisées pour partager des interfaces entre les parties d'un programme.

* *hiding*: l'acte d'empêcher une information d'être directement vue ou accédée. Par exemple, un nom provenant d'un scope imbriqué (inner) peut empêcher que le même nom provenant d'un scope externe (enclosing) soit directement utilisé.

* *ideal*: la version parfaite de quelque chose vers laquelle nous aspirons. En général, nous devons faire des compromis et nous satisfaire d'une approximation.

* *implementation*: (1) l'acte d'écrire et de tester du code ; (2) le code qui implémente un programme.

* *infinite loop*: une boucle dont la condition d'arrêt ne devient jamais vraie. Voir iteration.

* *infinite recursion*: une récursion qui ne se termine pas tant que la machine n'a pas épuisé la mémoire pour contenir les appels. En réalité, une telle récursion n'est jamais infinie mais se termine par une erreur matérielle.

* *information hiding*: l'acte de séparer l'interface et l'implémentation, masquant ainsi les détails d'implémentation non destinés à l'attention de l'utilisateur et fournissant une abstraction.

* *initialize*: donner à un objet sa première valeur (initiale).

* *input*: valeurs utilisées par une computation (ex., arguments de fonction et caractères tapés sur un clavier).

* *integer*: un nombre entier, tel que 42 ou -99.

* *interface*: une déclaration ou un ensemble de déclarations précisant comment un morceau de code (comme une fonction ou une classe) peut être appelé.

* *invariant*: quelque chose qui doit toujours être vrai à un ou plusieurs points d'un programme ; généralement utilisé pour décrire l'état (ensemble de valeurs) d'un objet ou l'état d'une boucle avant l'entrée dans l'instruction répétée.

* *iteration*: l'acte d'exécuter à plusieurs reprises un morceau de code ; voir récursion.

* *iterator*: un objet qui identifie un élément d'une séquence.

* *ISO*: Organisation Internationale de Normalisation. Le langage C++ est un standard ISO, ISO/IEC 14882. Plus d'informations sur [iso.org](https://iso.org).

* *library*: une collection de types, fonctions, classes, etc. implémentant un ensemble de facilités (abstractions) destinées à être potentiellement utilisées dans plus d'un programme.

* *lifetime*: le temps depuis l'initialisation d'un objet jusqu'à ce qu'il devienne inutilisable (sort du scope, est supprimé, ou le programme se termine).

* *linker*: un programme qui combine des fichiers de code objet et des bibliothèques en un programme exécutable.

* *literal*: une notation qui spécifie directement une valeur, comme 12 indiquant la valeur entière « douze ».

* *loop*: un morceau de code exécuté à plusieurs reprises ; en C++, typiquement une instruction for ou une instruction `while`.

* *move*: une opération qui transfère une valeur d'un objet à un autre laissant derrière elle une valeur représentant « vide ». Voir aussi copy.

* *move-only type*: un type concret qui est déplaçable mais non copiable.

* *mutable*: modifiable ; l'opposé d'immuable, constant, et invariable.

* *object*: (1) une région de mémoire initialisée d'un type connu qui contient une valeur de ce type ; (2) une région de mémoire.

* *object code*: sortie d'un compilateur destinée à être entrée pour un linker (afin que le linker produise du code exécutable).

* *object file*: un fichier contenant du code objet.

* *object-oriented programming*: (OOP) un style de programmation axé sur la conception et l'utilisation de classes et de hiérarchies de classes.

* *operation*: quelque chose qui peut réaliser une action, telle qu'une fonction ou un opérateur.

* *output*: valeurs produites par une computation (ex., le résultat d'une fonction ou les lignes de caractères écrites sur un écran).

* *overflow*: produire une valeur qui ne peut pas être stockée dans sa cible prévue.

* *overload*: définir deux fonctions ou opérateurs avec le même nom mais avec des types d'arguments (opérandes) différents.

* *override*: définir une fonction dans une classe dérivée ayant le même nom et les mêmes types d'arguments qu'une fonction virtuelle dans la classe de base, rendant ainsi la fonction appelable via l'interface définie par la classe de base.

* *owner*: un objet responsable de libérer une ressource.

* *paradigm*: un terme quelque peu prétentieux pour désigner un style de conception ou de programmation ; souvent employé avec l'implication erronée qu'il existe un paradigme supérieur à tous les autres.

* *parameter*: une déclaration d'une entrée explicite à une fonction ou un modèle. Lorsqu'elle est appelée, une fonction peut accéder aux arguments passés par les noms de ses paramètres.

* *pointer*: (1) une valeur utilisée pour identifier un objet typé en mémoire ; (2) une variable contenant une telle valeur.

* *post-condition*: une condition qui doit être vraie à la sortie d'un morceau de code, tel qu'une fonction ou une boucle.

* *pre-condition*: une condition qui doit être vraie lors de l'entrée dans un morceau de code, comme une fonction ou une boucle.

* *program*: code (éventuellement accompagné de données) suffisamment complet pour être exécuté par un ordinateur.

* *programming*: l'art d'exprimer des solutions à des problèmes sous forme de code.

* *programming language*: un langage pour exprimer des programmes.

* *pseudo code*: une description d'une computation écrite dans une notation informelle plutôt qu'un langage de programmation.

* *pure virtual function*: une fonction virtuelle qui doit être surchargée dans une classe dérivée.

* *RAII*: (Resource Acquisition Is Initialization) une technique de base pour la gestion des ressources basée sur les scopes.

* *range*: une séquence de valeurs pouvant être décrite par un point de départ et un point d'arrivée. Par ex., `[0:5)` désigne les valeurs 0, 1, 2, 3 et 4.

* *recursion*: l'acte d'une fonction qui s'appelle elle-même ; voir également itération.

* *reference*: (1) une valeur décrivant la localisation d'une valeur typée en mémoire ; (2) une variable contenant une telle valeur.

* *regular expression*: une notation pour les motifs dans des chaînes de caractères.

* *regular*: un type semirégulier qui est comparable à l'égalité (voir le concept `std::regular`). Après une copie, l'objet copié est égal à l'objet original. Un type régulier se comporte de façon similaire aux types intégrés comme `int` et peut être comparé avec `==`. Plus précisément, un objet d'un type régulier peut être copié et le résultat d'une copie est un objet distinct qui est égal à l'original. Voir aussi *semiregular type*.

* *requirement*: (1) une description du comportement attendu d'un programme ou d'une partie de programme ; (2) une description des hypothèses qu'une fonction ou un modèle fait sur ses arguments.

* *resource*: quelque chose qui est acquis et doit être libéré ultérieurement, comme un gestionnaire de fichier, un verrouillage ou la mémoire. Voir aussi handle, copy, move.

* *rounding*: conversion d'une valeur vers la valeur mathématiquement la plus proche d'un type moins précis.

* *RTTI*: Run-Time Type Information. ??? 

* *scope*: la région du texte du programme (code source) dans laquelle un nom peut être référencé.

* *semiregular*: un type concret qui est copiable (y compris déplaçable) et par défaut constructible (voir le concept `std::semiregular`). Le résultat d'une copie est un objet indépendant ayant la même valeur que l'original. Un type semirégulier se comporte à peu près comme un type intégré tel que `int`, mais peut éventuellement ne pas posséder un opérateur `==`.

* *sequence*: éléments pouvant être visités dans un ordre linéaire.

* *software*: une collection de morceaux de code et de données associées ; souvent utilisé de façon interchangeable avec program.

* *source code*: code tel que produit par un programmeur et, en principe, lisible par d'autres programmeurs.

* *source file*: un fichier contenant du code source.

* *specification*: une description de ce qu'un morceau de code doit faire.

* *standard*: une définition officiellement acceptée de quelque chose, comme un langage de programmation.

* *state*: un ensemble de valeurs.

* *STL*: les conteneurs, les itérateurs et les algorithmes faisant partie de la bibliothèque standard.

* *string*: une séquence de caractères.

* *style*: un ensemble de techniques de programmation conduisant à une utilisation cohérente des fonctionnalités du langage ; parfois utilisé dans un sens très restreint pour désigner uniquement les règles de bas niveau concernant la nomenclature et l'apparence du code.

* *subtype*: type dérivé ; un type qui possède toutes les propriétés d'un type et possiblement plus.

* *supertype*: type de base ; un type qui possède un sous-ensemble des propriétés d'un type.

* *system*: (1) un programme ou un ensemble de programmes pour effectuer une tâche sur un ordinateur ; (2) un raccourci pour « système d'exploitation », c’est‑à‑dire l'environnement d'exécution fondamental et les outils pour un ordinateur.

* *TS*: [Technical Specification](https://www.iso.org/deliverables-all.html?type=ts). Une spécification technique traite du travail toujours en cours de développement technique, ou dans le cas où l'on croit qu'un organisme future, mais non immédiate, d’accord sur une norme internationale existe. Une spécification technique est publiée pour une utilisation immédiate, mais elle fournit également un moyen d’obtenir des retours. L’objectif est qu’elle soit finalement transformée et republiée comme norme internationale.

* *template*: une classe ou une fonction paramétrée par un ou plusieurs types ou valeurs (à la compilation) ; le construit de base du langage C++ permettant la programmation générique.

* *testing*: une recherche systématique d’erreurs dans un programme.

* *trade-off*: le résultat de l’équilibrage de plusieurs critères de conception et d’implémentation.

* *truncation*: perte d’information lors d’une conversion d’un type vers un autre qui ne peut pas représenter exactement la valeur à convertir.

* *type*: quelque chose qui définit un ensemble de valeurs possibles et un ensemble d’opérations pour un objet.

* *uninitialized*: l’état (indéfini) d’un objet avant son initialisation.

* *unit*: (1) une unité de mesure standard donnant un sens à une valeur (ex., km pour une distance) ; (2) une partie distinguée (ex., nommée) d'un tout plus grand.

* *use case*: un cas d'utilisation spécifique (typiquement simple) d'un programme destiné à tester sa fonctionnalité et à démontrer son objectif.

* *value*: un ensemble de bits en mémoire interprétés selon un type.

* *value type*: un terme que certaines personnes utilisent pour désigner un type régulier ou semirégulier.

* *variable*: un objet nommé d'un type donné ; contient une valeur à moins d'être non initialisé.

* *virtual function*: une fonction membre qui peut être surchargée dans une classe dérivée.

* *word*: une unité de base de mémoire dans un ordinateur, généralement l'unité utilisée pour représenter un entier.