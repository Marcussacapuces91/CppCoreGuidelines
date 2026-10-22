# <a name="s-glossary"></a>Glossaire

Définitions relativement informelles des termes utilisés dans les lignes directrices
(d'après le glossaire de [Programming: Principles and Practice using C++](https://www.stroustrup.com/programming.html))

De plus amples informations sur de nombreux sujets liés à C++ sont disponibles sur le site de la [Standard C++ Foundation](https://isocpp.org).

* *ABI* : Application Binary Interface, spécification pour une plateforme matérielle donnée combinée au système d'exploitation. À ne pas confondre avec API.
* *classe abstraite* : une classe qui ne peut pas être utilisée directement pour créer des objets ; souvent utilisée pour définir une interface destinée aux classes dérivées.
  Une classe devient abstraite lorsqu'elle possède une fonction virtuelle pure ou uniquement des constructeurs protégés.
* *abstraction* : une description de quelque chose qui ignore (masque) délibérément et sélectivement certains détails (par exemple, les détails d'implémentation) ; ignorance sélective.
* *adresse* : une valeur qui nous permet de localiser un objet dans la mémoire d'un ordinateur.
* *algorithme* : une procédure ou une formule pour résoudre un problème ; une série finie d'étapes de calcul pour produire un résultat.
* *alias* : une manière alternative de désigner un objet ; souvent un nom, un pointeur ou une référence.
* *API* : Application Programming Interface, un ensemble de fonctions qui forme la communication entre divers composants logiciels. À ne pas confondre avec ABI.
* *application* : un programme ou un ensemble de programmes considéré comme une entité par ses utilisateurs.
* *approximation* : quelque chose (par exemple, une valeur ou une conception) qui est proche de la valeur ou de la conception parfaite ou idéale.
  Souvent, une approximation est le résultat de compromis entre plusieurs idéaux.
* *argument* : une valeur transmise à une fonction ou à un modèle, dans laquelle elle est accessible via un paramètre.
* *tableau* : une séquence homogène d'éléments, généralement numérotés, par exemple `[0:max)`.
* *assertion* : une instruction insérée dans un programme pour affirmer que quelque chose doit toujours être vrai à ce point du programme.
* *classe de base* : un type destiné à être dérivé (par exemple, possédant une fonction virtuelle non `final`), dont les objets sont destinés à n'être utilisés qu'indirectement (par exemple, via un pointeur). \[En termes stricts, « classe de base » pourrait se définir comme « quelque chose dont nous avons dérivé », mais nous la spécifions ici en fonction de l'intention du concepteur de la classe.\] Typiquement, une classe de base possède une ou plusieurs fonctions virtuelles.
* *bit* : l'unité fondamentale d'information dans un ordinateur. Un bit peut avoir la valeur 0 ou la valeur 1.
* *bogue* : une erreur dans un programme.
* *octet* : l'unité fondamentale d'adressage dans la plupart des ordinateurs. Typiquement, un octet contient 8 bits.
* *classe* : un type défini par l'utilisateur pouvant contenir des membres de données, des membres fonctions et des types membres.
* *code* : un programme ou une partie d'un programme ; terme ambigu utilisé à la fois pour le code source et le code objet.
* *compilateur* : un programme qui transforme le code source en code objet.
* *complexité* : une notion ou une mesure difficile à définir précisément, relative à la difficulté de construire une solution à un problème ou à la solution elle-même.
  Parfois, la complexité est utilisée pour désigner simplement une estimation du nombre d'opérations nécessaires à l'exécution d'un algorithme.
* *calcul* : l'exécution d'un certain code, prenant généralement une entrée et produisant une sortie.
* *concept* : (1) une notion, une idée ; (2) un ensemble d'exigences, généralement pour un argument de modèle.
* *type concret* : un type qui n'est pas une classe de base, dont les objets sont destinés à être utilisés directement (et non uniquement via un pointeur/indirection), dont la taille est connue et qui peut typiquement être alloué n'importe où le programmeur le souhaite (par exemple, sur la pile ou statiquement).
* *constante* : une valeur qui ne peut pas être modifiée (dans une portée donnée) ; non mutable.
* *constructeur* : une opération qui initialise (« construit ») un objet.
  Typiquement, un constructeur établit un invariant et acquiert souvent les ressources nécessaires à l'utilisation d'un objet (qui sont ensuite généralement libérées par un destructeur).
* *conteneur* : un objet qui contient des éléments (d'autres objets).
* *copie* : une opération qui fait que deux objets ont des valeurs qui se comparent égales. Voir aussi déplacement.
* *correctitude* : un programme ou une partie d'un programme est correct s'il satisfait sa spécification.
  Malheureusement, une spécification peut être incomplète ou incohérente, ou ne pas répondre aux attentes raisonnables des utilisateurs.
  Ainsi, pour produire un code acceptable, il nous faut parfois faire plus que simplement suivre la spécification formelle.
* *coût* : la dépense (par exemple, en temps de programmation, temps d'exécution ou espace) de la production d'un programme ou de son exécution.
  Idéalement, le coût devrait être une fonction de la complexité.
* *point de personnalisation* : ???
* *données* : des valeurs utilisées dans un calcul.
* *débogage* : l'acte de rechercher et d'éliminer les erreurs d'un programme ; généralement beaucoup moins systématique que les tests.
* *déclaration* : la spécification d'un nom avec son type dans un programme.
* *définition* : une déclaration d'une entité qui fournit toutes les informations nécessaires pour compléter un programme utilisant cette entité.
  Définition simplifiée : une déclaration qui alloue de la mémoire.
* *classe dérivée* : une classe dérivée d'une ou plusieurs classes de base.
* *conception* : une description globale de la manière dont un logiciel doit fonctionner pour satisfaire sa spécification.
* *destructeur* : une opération invoquée implicitement (appelée) lorsqu'un objet est détruit (par exemple, à la fin d'une portée). Souvent, il libère des ressources.
* *encapsulation* : la protection de quelque chose destiné à rester privé (par exemple, des détails d'implémentation) contre un accès non autorisé.
* *erreur* : un écart entre les attentes raisonnables du comportement d'un programme (souvent exprimées sous forme d'exigence ou de guide utilisateur) et ce que le programme fait réellement.
* *exécutable* : un programme prêt à être exécuté sur un ordinateur.
* *dérive fonctionnelle* : la tendance à ajouter des fonctionnalités superflues à un programme « au cas où ».
* *fichier* : un conteneur d'informations permanentes dans un ordinateur.
* *nombre à virgule flottante* : l'approximation par un ordinateur d'un nombre réel, tel que 7,93 ou 10,78e-3.
* *fonction* : une unité de code nommée qui peut être invoquée (appelée) depuis différentes parties d'un programme ; une unité logique de calcul.
* *programmation générique* : un style de programmation axé sur la conception et l'implémentation efficace d'algorithmes.
  Un algorithme générique fonctionnera pour tous les types d'arguments qui satisfont ses exigences. En C++, la programmation générique utilise typiquement les modèles.
* *variable globale* : techniquement, un objet nommé dans une portée d'espace de noms.
* *poignée* : une classe qui permet l'accès à un autre objet via un pointeur ou une référence membre. Voir aussi ressource, copie, déplacement.
* *en-tête* : un fichier contenant des déclarations utilisées pour partager des interfaces entre les parties d'un programme.
* *masquage* : l'acte d'empêcher une information d'être directement visible ou accessible.
  Par exemple, un nom d'une portée imbriquée (interne) peut empêcher l'utilisation directe du même nom d'une portée englobante (externe).
* *idéal* : la version parfaite de quelque chose que nous cherchons à atteindre. Nous devons généralement faire des compromis et nous contenter d'une approximation.
* *implémentation* : (1) l'acte d'écrire et de tester du code ; (2) le code qui implémente un programme.
* *boucle infinie* : une boucle dont la condition d'arrêt ne devient jamais vraie. Voir itération.
* *récursion infinie* : une récursion qui ne s'arrête pas tant que la machine n'a pas épuisé sa mémoire pour stocker les appels.
  En réalité, une telle récursion n'est jamais infinie mais est terminée par une erreur matérielle.
* *masquage d'information* : l'acte de séparer l'interface et l'implémentation, masquant ainsi les détails d'implémentation non destinés à l'attention de l'utilisateur et fournissant une abstraction.
* *initialiser* : donner à un objet sa première (initiale) valeur.
* *entrée* : des valeurs utilisées par un calcul (par exemple, des arguments de fonction et des caractères saisis au clavier).
* *entier* : un nombre entier, tel que 42 ou -99.
* *interface* : une déclaration ou un ensemble de déclarations spécifiant comment un morceau de code (tel qu'une fonction ou une classe) peut être appelé.
* *invariant* : quelque chose qui doit toujours être vrai à un point donné (ou à certains points) d'un programme ; typiquement utilisé pour décrire l'état (ensemble de valeurs) d'un objet ou l'état d'une boucle avant l'entrée dans l'instruction répétée.
* *itération* : l'acte d'exécuter répétitivement un morceau de code ; voir récursion.
* *itérateur* : un objet qui identifie un élément d'une séquence.
* *ISO* : International Organization for Standardization. Le langage C++ est une norme ISO, ISO/IEC 14882. Plus d'informations sur [iso.org](https://iso.org).
* *bibliothèque* : une collection de types, de fonctions, de classes, etc. implémentant un ensemble de fonctionnalités (abstractions) destinées à être potentiellement utilisées dans plus d'un programme.
* *durée de vie* : la période allant de l'initialisation d'un objet jusqu'à ce qu'il devienne inutilisable (sort de portée, est supprimé, ou le programme se termine).
* *éditeur de liens* : un programme qui combine les fichiers de code objet et les bibliothèques en un programme exécutable.
* *littéral* : une notation qui spécifie directement une valeur, par exemple 12 spécifiant la valeur entière « douze ».
* *boucle* : un morceau de code exécuté de manière répétée ; en C++, typiquement une instruction `for` ou une instruction `while`.
* *déplacement* : une opération qui transfère une valeur d'un objet à un autre, laissant derrière une valeur représentant « vide ». Voir aussi copie.
* *type non copiable* : un type concret qui est déplaçable mais non copiable.
* *mutable* : modifiable ; l'opposé de immuable, constant et invariable.
* *objet* : (1) une région initialisée de mémoire d'un type connu contenant une valeur de ce type ; (2) une région de mémoire.
* *code objet* : la sortie d'un compilateur destinée à être l'entrée d'un éditeur de liens (pour produire du code exécutable).
* *fichier objet* : un fichier contenant du code objet.
* *programmation orientée objet* : (POO) un style de programmation axé sur la conception et l'utilisation de classes et de hiérarchies de classes.
* *opération* : quelque chose qui peut effectuer une action, telle qu'une fonction ou un opérateur.
* *sortie* : des valeurs produites par un calcul (par exemple, un résultat de fonction ou des lignes de caractères écrites à l'écran).
* *dépassement* : la production d'une valeur qui ne peut pas être stockée dans sa cible prévue.
* *surcharge* : la définition de deux fonctions ou opérateurs portant le même nom mais ayant des types d'arguments (opérandes) différents.
* *réécriture* : la définition d'une fonction dans une classe dérivée portant le même nom et les mêmes types d'arguments qu'une fonction virtuelle dans la classe de base, rendant ainsi la fonction appelable via l'interface définie par la classe de base.
* *propriétaire* : un objet responsable de la libération d'une ressource.
* *paradigme* : un terme quelque peu pompeux pour désigner un style de conception ou de programmation ; souvent utilisé avec l'implication (erronée) qu'il existe un paradigme supérieur à tous les autres.
* *paramètre* : une déclaration d'une entrée explicite d'une fonction ou d'un modèle. Lors de l'appel, une fonction peut accéder aux arguments passés via les noms de ses paramètres.
* *pointeur* : (1) une valeur utilisée pour identifier un objet typé en mémoire ; (2) une variable contenant une telle valeur.
* *postcondition* : une condition qui doit être satisfaite à la sortie d'un morceau de code, tel qu'une fonction ou une boucle.
* *précondition* : une condition qui doit être satisfaite à l'entrée d'un morceau de code, tel qu'une fonction ou une boucle.
* *programme* : du code (éventuellement avec des données associées) suffisamment complet pour être exécuté par un ordinateur.
* *programmation* : l'art d'exprimer des solutions à des problèmes sous forme de code.
* *langage de programmation* : un langage pour exprimer des programmes.
* *pseudo-code* : une description d'un calcul écrite dans une notation informelle plutôt que dans un langage de programmation.
* *fonction virtuelle pure* : une fonction virtuelle qui doit être réécrite dans une classe dérivée.
* *RAII* : (« Resource Acquisition Is Initialization ») une technique fondamentale de gestion des ressources basée sur les portées.
* *intervalle* : une séquence de valeurs qui peut être décrite par un point de départ et un point de fin. Par exemple, `[0:5)` signifie les valeurs 0, 1, 2, 3 et 4.
* *récursion* : l'acte pour une fonction de s'appeler elle-même ; voir aussi itération.
* *référence* : (1) une valeur décrivant l'emplacement d'une valeur typée en mémoire ; (2) une variable contenant une telle valeur.
* *expression régulière* : une notation pour les motifs dans les chaînes de caractères.
* *régulier* : un type semi-régulier qui est comparable par égalité (voir le concept `std::regular`). Après une copie, l'objet copié se compare égal à l'objet d'origine. Un type régulier se comporte de manière similaire aux types intégrés comme `int` et peut être comparé avec `==`.
En particulier, un objet d'un type régulier peut être copié et le résultat d'une copie est un objet distinct qui se compare égal à l'original. Voir aussi *type semi-régulier*.
* *exigence* : (1) une description du comportement souhaité d'un programme ou d'une partie d'un programme ; (2) une description des hypothèses qu'une fonction ou un modèle fait sur ses arguments.
* *ressource* : quelque chose qui est acquis et qui doit ensuite être libéré, tel qu'un descripteur de fichier, un verrou ou de la mémoire. Voir aussi poignée, propriétaire.
* *arrondi* : la conversion d'une valeur à la valeur mathématiquement la plus proche d'un type moins précis.
* *RTTI* : Run-Time Type Information. ???
* *portée* : la région du texte du programme (code source) dans laquelle un nom peut être référencé.
* *semi-régulier* : un type concret qui est copiable (y compris déplaçable) et constructible par défaut (voir le concept `std::semiregular`). Le résultat d'une copie est un objet indépendant ayant la même valeur que l'original. Un type semi-régulier se comporte approximativement comme un type intégré comme `int`, mais possiblement sans opérateur `==`. Voir aussi *type régulier*.
* *séquence* : des éléments qui peuvent être parcourus dans un ordre linéaire.
* *logiciel* : une collection de morceaux de code et de données associées ; souvent utilisé de manière interchangeable avec programme.
* *code source* : le code produit par un programmeur et (en principe) lisible par d'autres programmeurs.
* *fichier source* : un fichier contenant du code source.
* *spécification* : une description de ce qu'un morceau de code doit faire.
* *norme* : une définition officiellement convenue de quelque chose, tel qu'un langage de programmation.
* *état* : un ensemble de valeurs.
* *STL* : la partie conteneurs, itérateurs et algorithmes de la bibliothèque standard.
* *chaîne de caractères* : une séquence de caractères.
* *style* : un ensemble de techniques de programmation menant à une utilisation cohérente des fonctionnalités du langage ; parfois utilisé au sens très restreint pour désigner uniquement les règles de bas niveau relatives à la nomenclature et à l'apparence du code.
* *sous-type* : type dérivé ; un type qui possède toutes les propriétés d'un type et possiblement plus.
* *sur-type* : type de base ; un type qui possède un sous-ensemble des propriétés d'un type.
* *système* : (1) un programme ou un ensemble de programmes pour effectuer une tâche sur un ordinateur ; (2) un raccourci pour « système d'exploitation », c'est-à-dire l'environnement d'exécution fondamental et les outils d'un ordinateur.
* *TS* : [Technical Specification](https://www.iso.org/deliverables-all.html?type=ts). Une Technical Specification traite d'un travail encore en développement technique, ou pour lequel on estime qu'il y aura une possibilité future, mais non immédiate, d'accord sur une norme internationale. Une Technical Specification est publiée pour un usage immédiat, mais elle fournit également un moyen d'obtenir des retours. L'objectif est qu'elle soit éventuellement transformée et republiée en tant que norme internationale.
* *modèle* : une classe ou une fonction paramétrée par un ou plusieurs types ou valeurs (de temps de compilation) ; la construction de base du langage C++ supportant la programmation générique.
* *tests* : une recherche systématique d'erreurs dans un programme.
* *compromis* : le résultat de l'équilibrage de plusieurs critères de conception et d'implémentation.
* *troncature* : la perte d'information lors d'une conversion d'un type vers un autre qui ne peut pas représenter exactement la valeur à convertir.
* *type* : quelque chose qui définit un ensemble de valeurs possibles et un ensemble d'opérations pour un objet.
* *non initialisé* : l'état (non défini) d'un objet avant qu'il ne soit initialisé.
* *unité* : (1) une mesure standard qui donne un sens à une valeur (par exemple, km pour une distance) ; (2) une partie distinguée (par exemple, nommée) d'un tout plus grand.
* *cas d'utilisation* : un usage spécifique (généralement simple) d'un programme destiné à tester sa fonctionnalité et à démontrer son objectif.
* *valeur* : un ensemble de bits en mémoire interprété selon un type.
* *type valeur* : un terme utilisé par certaines personnes pour désigner un type régulier ou semi-régulier.
* *variable* : un objet nommé d'un type donné ; contient une valeur sauf s'il n'est pas initialisé.
* *fonction virtuelle* : une fonction membre qui peut être réécrite dans une classe dérivée.
* *mot* : une unité fondamentale de mémoire dans un ordinateur, souvent l'unité utilisée pour stocker un entier.
