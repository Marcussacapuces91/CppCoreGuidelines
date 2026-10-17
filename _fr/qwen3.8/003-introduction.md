# <a name="s-introduction"></a>Intro : Introduction

Il s'agit d'un ensemble de lignes directrices fondamentales pour le C++ moderne (actuellement C++20 et C++17), tenant compte des évolutions futures probables et des spécifications techniques ISO (TS).
L'objectif est d'aider les programmateurs C++ à écrire un code plus simple, plus efficace et plus facile à maintenir.

Résumé de l'introduction :

* [Intro.cibles : Cibles](003-introduction.md#ss-readers)
* [Intro.objectifs : Objectifs](003-introduction.md#ss-aims)
* [Intro.non : Non-objectifs](003-introduction.md#ss-non)
* [Intro.force : Application des règles](003-introduction.md#ss-force)
* [Intro.struct : Structure de ce document](003-introduction.md#ss-struct)
* [Intro.sec : Sections principales](003-introduction.md#ss-sec)

## <a name="ss-readers"></a>Intro.cibles : Cibles

Tous les programmateurs C++. Cela inclut les [programmeurs qui pourraient envisager le C](016-cpl.md).

## <a name="ss-aims"></a>Intro.objectifs : Objectifs

Le but de ce document est d'aider les développeurs à adopter le C++ moderne (actuellement C++20 et C++17) et à atteindre un style plus uniforme au sein des bases de code.

Nous n'avons pas l'illusion que chacune de ces règles puisse être appliquée de manière effective à chaque base de code. Moderniser des anciens systèmes est difficile. Toutefois, nous estimons qu'un programme utilisant une règle est moins sujet aux erreurs et plus facile à maintenir qu'un programme qui ne l'utilise pas. Souvent, les règles facilitent également le développement initial (plus rapide et plus simple).
Jusqu'à preuve du contraire, ces règles produisent un code dont les performances sont au moins égales, sinon supérieures, à celles des techniques plus anciennes et plus conventionnelles ; elles suivent le principe du surcoût nul (« ce que vous n'utilisez pas, vous n'en payez pas le prix » ou « lorsque vous utilisez un mécanisme d'abstraction de manière appropriée, vous obtenez au moins les mêmes performances que si vous aviez codé à la main en utilisant des structures de bas niveau »).
Considérez ces règles comme des idéaux pour le nouveau code, des opportunités à saisir lors du travail sur du code ancien, et essayez d'approcher ces idéaux le plus étroitement possible.
Rappelez-vous :

### <a name="r0"></a>Intro.0 : Pas de panique !

Prenez le temps de comprendre les implications d'une règle sur votre programme.

Ces lignes directrices sont conçues selon le principe du « sous-ensemble du sur-ensemble » ([Stroustrup05](032-bibliography.md#Stroustrup05)).
Elles ne définissent pas simplement un sous-ensemble de C++ à utiliser (pour la fiabilité, la sécurité, les performances, ou quoi que ce soit d'autre).
Au contraire, elles recommandent vivement l'utilisation de quelques simples « extensions » ([composantes de la bibliothèque](#gsl-guidelines-support-library)@TODO-LINK)
qui rendent redondantes les fonctionnalités de C++ les plus sujettes aux erreurs, permettant ainsi de les interdire (dans notre ensemble de règles).

Les règles mettent l'accent sur la sécurité des types et la sécurité des ressources.
Pour cette raison, elles soulignent les possibilités de vérification de bornes, d'éviter le déréférencement de `nullptr`, d'éviter les pointeurs pendants, et l'utilisation systématique des exceptions (via le RAII).
En partie pour y parvenir et en partie pour minimiser le code obscur comme source d'erreurs, les règles mettent également l'accent sur la simplicité et le masquage de la complexité nécessaire derrière des interfaces bien spécifiées.

Beaucoup de règles sont prescriptives.
Nous sommes mal à l'aise avec des règles qui se contentent de dire « ne faites pas ça ! » sans proposer d'alternative.
Une conséquence de cela est que certaines règles ne peuvent être soutenues que par des heuristiques, plutôt que par des vérifications précises et mécaniquement vérifiables.
D'autres règles énoncent des principes généraux. Pour ces règles plus générales, des règles plus détaillées et spécifiques fournissent une vérification partielle.

Ces lignes directrices traitent du cœur de C++ et de son utilisation.
Nous prévoyons que la plupart des grandes organisations, les domaines d'application spécifiques et même les grands projets auront besoin de règles supplémentaires, éventuellement de restrictions supplémentaires, et d'un soutien de bibliothèque complémentaire.
Par exemple, les programmeurs en temps réel dur ne peuvent généralement pas utiliser la mémoire dynamique librement et seront restreints dans leur choix de bibliothèques.
Nous encourageons le développement de telles règles plus spécifiques en tant qu'annexes à ces lignes directrices fondamentales.
Construisez votre petite bibliothèque de base idéale et utilisez-la, plutôt que de descendre votre niveau de programmation à un assembleur glorifié.

Les règles sont conçues pour permettre une [adoption progressive](027-modernizing.md).

Certaines règles visent à augmenter différentes formes de sécurité, tandis que d'autres visent à réduire la probabilité d'accidents ; beaucoup font les deux.
Les lignes directrices visant à prévenir les accidents interdisent souvent du C++ parfaitement légal.
Cependant, lorsque deux manières d'exprimer une idée existent et que l'une s'est révélée être une source fréquente d'erreurs tandis que l'autre non, nous essayons d'orienter les programmeurs vers la seconde.

## <a name="ss-non"></a>Intro.non : Non-objectifs

Les règles ne sont pas conçues pour être minimales ou orthogonales.
En particulier, des règles générales peuvent être simples, mais impossible à faire appliquer.
De plus, il est souvent difficile de comprendre les implications d'une règle générale.
Des règles plus spécialisées sont souvent plus faciles à comprendre et à faire appliquer, mais sans les règles générales, elles ne seraient qu'une longue liste de cas particuliers.
Nous proposons des règles visant à aider les débutants ainsi que des règles soutenant l'usage par des experts.
Certaines règles peuvent être entièrement appliquées, mais d'autres sont basées sur des heuristiques.

Ces règles ne sont pas conçues pour être lues séquentiellement, comme un livre.
Vous pouvez les parcourir à l'aide des liens.
Cependant, leur utilisation principale prévue est d'être des cibles pour les outils.
Autrement dit, un outil recherche les violations et renvoie des liens vers les règles violées.
Les règles fournissent alors les raisons, des exemples de conséquences potentielles de la violation, et des remèdes suggérés.

Ces lignes directrices ne sont pas destinées à remplacer un traitement didactique de C++.
Si vous avez besoin d'un tutoriel pour un niveau d'expérience donné, consultez [les références](021-references.md).

Il ne s'agit pas d'un guide sur la conversion de l'ancien code C++ en code plus moderne.
Il vise à formuler des idées pour le nouveau code d'une manière concrète.
Cependant, consultez [la section sur la modernisation](027-modernizing.md) pour quelques approches possibles de modernisation/renouvellement/mise à niveau.
Point important : les règles soutiennent l'adoption progressive : il est généralement impossible de convertir entièrement une grande base de code d'un coup.

Ces lignes directrices ne sont pas destinées à être complètes ou exactes dans tous les détails techniques de la langue.
Pour la parole définitive sur les questions de définition de la langue, y compris chaque exception aux règles générales et chaque fonctionnalité, consultez la norme ISO C++.

Les règles ne sont pas destinées à vous forcer à écrire dans un sous-ensemble appauvri de C++.
Elles ne sont *catégoriquement* pas destinées à définir un sous-ensemble, disons, ressemblant à Java, de C++.
Elles ne sont pas destinées à définir une unique « véritable langue C++ ».
Nous valorisons l'expressivité et des performances non compromis.

Les règles ne sont pas neutres en valeurs.
Elles visent à rendre le code plus simple et plus correct/sûr que la plupart des codes C++ existants, sans perte de performance.
Elles visent à freiner le code C++ parfaitement valide qui est corrélé aux erreurs, à la complexité superflue et aux mauvaises performances.

Les règles ne sont pas précises au point où une personne (ou une machine) peut les suivre sans réfléchir.
Les parties « Application » tentent de l'être, mais nous préférons laisser une règle ou une définition un peu vague
et ouverte à l'interprétation plutôt que de spécifier quelque chose de précis et d'erroné.
Parfois, la précision n'arrive qu'avec le temps et l'expérience.
La conception n'est pas (encore) une forme de mathématiques.

Les règles ne sont pas parfaites.
Une règle peut causer du tort en interdisant quelque chose d'utile dans une situation donnée.
Une règle peut causer du tort en ne interdisant pas quelque chose qui permet une erreur grave dans une situation donnée.
Une règle peut causer beaucoup de tort en étant vague, ambiguë, impossible à faire appliquer, ou en permettant toute solution à un problème.
Il est impossible de satisfaire pleinement le critère « ne pas nuire ».
Notre objectif, plus modeste, est : « Faire le plus de bien possible au plus grand nombre de programmeurs » ;
si vous ne pouvez pas accepter une règle, contestez-la, ignorez-la, mais ne la diluez pas jusqu'à ce qu'elle devienne dénuée de sens.
Suggérez également une amélioration.

## <a name="ss-force"></a>Intro.force : Application des règles

Des règles sans mécanisme d'application sont ingérables pour de grandes bases de code.
L'application de toutes les règles n'est possible que pour un petit ensemble faible de règles ou pour une communauté d'utilisateurs spécifique.

* Mais nous voulons beaucoup de règles, et des règles que tout le monde peut utiliser.
* Mais les gens ont des besoins différents.
* Mais les gens n'aiment pas lire beaucoup de règles.
* Mais les gens ne peuvent pas se souvenir de nombreuses règles.

Il nous faut donc du sous-ensemblistique pour répondre à une variété de besoins.

* Mais un sous-ensemblistique arbitraire mène au chaos.

Nous voulons des lignes directrices qui aident beaucoup de gens, rendent le code plus uniforme, et encouragent fortement les gens à moderniser leur code.
Nous voulons encourager les meilleures pratiques, plutôt que de tout laisser aux choix individuels et aux pressions de gestion.
L'idéal est d'utiliser toutes les règles ; cela donne les plus grands bénéfices.

Tout cela cumule un certain nombre de dilemmes.
Nous essayons de les résoudre à l'aide d'outils.
Chaque règle possède une section **Application** listant des idées pour sa mise en œuvre.
L'application peut se faire par revue de code, par analyse statique, par le compilateur, ou par des vérifications à l'exécution.
Lorsque c'est possible, nous préférons la vérification « mécanique » (les humains sont lents, imprécis et s'ennuient facilement) et la vérification statique.
Les vérifications à l'exécution ne sont suggérées que rarement, lorsque aucune alternative n'existe ; nous ne voulons pas introduire de « gonflement distribué ».
Lorsque c'est approprié, nous étiquetons une règle (dans les sections **Application**) avec le nom de groupes de règles liées (appelés « profils »).
Une règle peut faire partie de plusieurs profils, ou d'aucun.
Pour commencer, nous avons quelques profils correspondant à des besoins courants (envies, idéaux) :

* **type** : aucune violation de types (réinterprétation d'un `T` en `U` par des conversions, des unions ou des varargs)
* **bounds** : aucune violation de bornes (accès au-delà de la plage d'un tableau)
* **lifetime** : aucune fuite (absence de `delete` ou `delete` multiple) et aucun accès à des objets invalides (déréférencement de `nullptr`, utilisation d'une référence pendante).

Les profils sont destinés à être utilisés par des outils, mais servent également d'aide au lecteur humain.
Nous ne limitons pas nos commentaires dans les sections **Application** aux choses que nous savons faire appliquer ; certains commentaires ne sont que des souhaits qui pourraient inspirer un constructeur d'outils.

Les outils qui implémentent ces règles doivent respecter la syntaxe suivante pour supprimer explicitement une règle :

    [[gsl::suppress("tag")]]

et éventuellement avec un message (suivant la syntaxe habituelle des attributs de la norme C++11) :

    [[gsl::suppress("tag", justification: "message")]]

où

* `"tag"` est une littérale de chaîne contenant le nom de l'ancre de l'élément où apparaît la règle d'application (par exemple, pour [C.134](007-class.md#rh-public) il s'agit de « rh-public »), le
nom d'un profil de groupe de règles (« type », « bounds » ou « lifetime »),
ou une règle spécifique dans un profil ([type.4](022-profile.md#pro-type-cstylecast) ou [bounds.2](022-profile.md#pro-bounds-arrayindex)). Tout texte qui n'est pas l'un de ceux-ci doit être rejeté.

* `"message"` est une littérale de chaîne

## <a name="ss-struct"></a>Intro.struct : Structure de ce document

Chaque règle (ligne directrice, suggestion) peut avoir plusieurs parties :

* La règle elle-même -- par exemple, **pas de `new` nu**
* Un numéro de référence de la règle -- par exemple, **C.7** (la 7e règle relative aux classes).
  Puisque les sections principales ne sont pas intrinsèquement ordonnées, nous utilisons des lettres comme première partie du numéro de référence.
  Nous laissons des gaps dans la numérotation pour minimiser les « perturbations » lorsque nous ajoutons ou retirons des règles.
* **Raisons** -- car les programmeurs ont du mal à suivre des règles qu'ils ne comprennent pas
* **Exemple**s -- car les règles sont difficiles à comprendre de manière abstraite ; peuvent être positifs ou négatifs
* **Alternative**s -- pour les règles du type « ne faites pas ceci »
* **Exception**s -- nous préférons des règles générales simples. Toutefois, de nombreuses règles s'appliquent largement, mais pas universellement, donc les exceptions doivent être listées
* **Application** -- des idées sur la manière dont la règle pourrait être vérifiée « mécaniquement »
* **Voir aussi** -- références vers des règles liées et/ou une discussion plus approfondie (dans ce document ou ailleurs)
* **Note**s -- quelque chose qui doit être dit et qui ne s'inscrit pas dans les autres catégories
* **Discussion** -- références vers une justification plus étendue et/ou des exemples placés en dehors des listes principales de règles

Certaines règles sont difficiles à vérifier mécaniquement, mais toutes remplissent le critère minimal selon lequel un programmeur expert peut repérer de nombreuses violations sans trop de difficulté.
Nous espérons que les outils « mécaniques » s'amélioreront avec le temps pour approcher ce qu'un tel programmeur expert remarque.
Nous supposons également que les règles seront affinées au fil du temps pour devenir plus précises et vérifiables.

Une règle vise à être simple, plutôt que soigneusement formulée pour mentionner chaque alternative et cas particulier.
De telles informations se trouvent dans les paragraphes **Alternatives** et les sections [Discussion](028-discussion.md).
Si vous ne comprenez pas une règle ou êtes en désaccord avec elle, veuillez consulter sa **Discussion**.
Si vous estimez qu'une discussion manque ou est incomplète, ouvrez un [Issue](https://github.com/isocpp/CppCoreGuidelines/issues)
expliquant vos préoccupations et éventuellement un PR correspondant.

Les exemples sont écrits pour illustrer les règles.

* Les exemples ne sont pas destinés à être de qualité production ni à couvrir toutes les dimensions d'un tutoriel.
Par exemple, beaucoup d'exemples sont techniques en ce qui concerne la langue et utilisent des noms comme `f`, `base` et `x`.
* Nous essayons de nous assurer que les « bons » exemples suivent les Lignes Directrices Fondamentales.
* Les commentaires illustrent souvent des règles là où ils seraient inutiles et/ou perturbateurs dans un « vrai code ».
* Nous supposons une connaissance de la bibliothèque standard. Par exemple, nous utilisons `vector` simple plutôt que `std::vector`.

Il ne s'agit pas d'un manuel de langue.
Il est conçu pour être utile, plutôt que complet, entièrement exact sur les détails techniques, ou un guide pour le code existant.
Les sources d'information recommandées peuvent être trouvées dans [les références](021-references.md).

## <a name="ss-sec"></a>Intro.sec : Sections principales

* [Intro : Introduction](003-introduction.md)
* [P : Philosophie](004-philosophy.md)
* [I : Interfaces](005-interfaces.md)
* [F : Fonctions](006-functions.md)
* [C : Classes et hiérarchies de classes](007-class.md)
* [Enum : Énumérations](008-enum.md)
* [R : Gestion des ressources](009-resource.md)
* [ES : Expressions et instructions](010-expr.md)
* [Per : Performances](011-performance.md)
* [CP : Concurrence et parallélisme](012-concurrency.md)
* [E : Gestion des erreurs](013-errors.md)
* [Con : Constantes et immutabilité](014-const.md)
* [T : Templates et programmation générique](015-templates.md)
* [CPL : Programmation de style C](016-cpl.md)
* [SF : Fichiers sources](017-source.md)
* [SL : La Bibliothèque Standard](#sl-the-standard-library)@TODO-LINK

Sections d'accompagnement :

* [A : Idées architecturales](019-a.md)
* [NR : Non-règles et mythes](020-not.md)
* [RF : Références](021-references.md)
* [Pro : Profils](022-profile.md)
* [GSL : Bibliothèque de soutien des lignes directrices](#gsl-guidelines-support-library)@TODO-LINK
* [NL : Suggestions de nommage et de mise en page](024-naming.md)
* [FAQ : Réponses aux questions fréquentes](025-faq.md)
* [Annexe A : Bibliothèques](026-libraries.md)
* [Annexe B : Modernisation du code](027-modernizing.md)
* [Annexe C : Discussion](028-discussion.md)
* [Annexe D : Outils de soutien](029-tools.md)
* [Glossaire](030-glossary.md)
* [À faire : Proto-règles non classées](031-unclassified.md)

Ces sections ne sont pas orthogonales.

Chaque section (par exemple, « P » pour « Philosophie ») et chaque sous-section (par exemple, « C.hier » pour « Hiérarchies de classes (OOP) ») ont un sigle pour faciliter la recherche et la référence.
Les sigles des sections principales sont également utilisés dans les numéros de règles (par exemple, « C.11 » pour « Rendre les types concrets réguliers »).