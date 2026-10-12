# <a name="s-introduction"></a>In : Introduction

Il s'agit d'un ensemble de directives fondamentales pour le C++ moderne (actuellement C++20 et C++17), tenant compte des évolutions futures probables et des spécifications techniques ISO (TS).
L'objectif est d'aider les programmeurs C++ à écrire un code plus simple, plus efficace et plus maintenable.

Résumé de l'introduction :

* [In.target : Public cible](003-introduction.md#ss-readers)
* [In.aims : Objectifs](003-introduction.md#ss-aims)
* [In.not : Non-objectifs](003-introduction.md#ss-non)
* [In.force : Application des règles](003-introduction.md#ss-force)
* [In.struct : Structure de ce document](003-introduction.md#ss-struct)
* [In.sec : Sections principales](003-introduction.md#ss-sec)

## <a name="ss-readers"></a>In.target : Public cible

Tous les programmeurs C++. Cela inclut les [programmeurs susceptibles d'envisager le C](016-cpl.md).

## <a name="ss-aims"></a>In.aims : Objectifs

Le but de ce document est d'aider les développeurs à adopter le C++ moderne (actuellement C++20 et C++17) et à instaurer un style plus uniforme d'un dépôt de code à l'autre.

Nous ne nous faisons pas d'illusions sur le fait que chacune de ces règles puisse être appliquée efficacement à chaque base de code. La modernisation de systèmes anciens est difficile. Toutefois, nous estimons qu'un programme qui respecte une règle est moins sujet aux erreurs et plus maintenable qu'un programme qui ne la respecte pas. Souvent, ces règles facilitent également le développement initial.
Jusqu'où nous pouvons en juger, ces règles produisent un code dont les performances sont au moins égales, voire supérieures, à celles des techniques plus anciennes et plus conventionnelles ; elles suivent le principe du surcoût nul (« ce que vous n'utilisez pas ne vous coûte rien » ou « lorsque vous utilisez un mécanisme d'abstraction de manière appropriée, vous obtenez au moins les mêmes performances que si vous aviez codé à la main avec des structures de langage de bas niveau »).
Considérez ces règles comme des idéaux pour le nouveau code, comme des opportunités à saisir lorsque vous travaillez sur du code plus ancien, et cherchez à vous en approcher le plus près que possible.
Retenez ceci :

### <a name="r0"></a>In.0 : Ne paniquez pas !

Prenez le temps de comprendre les implications d'une règle de ces directives sur votre programme.

Ces directives sont conçues selon le principe du « sous-ensemble de l'ensemble parent » ([Stroustrup05](032-bibliography.md#Stroustrup05)).
Elles ne définissent pas simplement un sous-ensemble de C++ à utiliser (pour la fiabilité, la sécurité, les performances ou tout autre motif).
Au contraire, elles recommandent vivement l'usage de quelques « extensions » simples ([composants de bibliothèque](#gsl-guidelines-support-library) <!-- @TODO-LINK : l'ancre "gsl-guidelines-support-library" n'est pas définie dans ce document -->)
qui rendent redondant l'emploi des fonctionnalités les plus propices aux erreurs du C++, de sorte qu'elles puissent être proscrites (dans notre ensemble de règles).

Les règles insistent sur la sécurité des types statiques et la sécurité des ressources.
Pour cette raison, elles privilégient les possibilités de vérification des limites, l'évitement du déréférencement de `nullptr`, l'évitement des pointeurs pendants et l'usage systématique des exceptions (via RAII).
En partie pour y parvenir et en partie pour minimiser le code obscur comme source d'erreurs, les règles insistent également sur la simplicité et le masquage de la complexité nécessaire derrière des interfaces bien spécifiées.

De nombreuses règles sont prescriptives.
Nous sommes mal à l'aise avec des règles qui se limitent à dire « ne faites pas ça ! » sans offrir d'alternative.
Une conséquence de cela est que certaines règles ne peuvent être appuyées que par des heuristiques, plutôt que par des vérifications précises et mécaniquement contrôlables.
D'autres règles énoncent des principes généraux. Pour ces règles plus générales, des règles plus détaillées et spécifiques fournissent une vérification partielle.

Ces directives portent sur le cœur du C++ et son utilisation.
Nous prévoyons que la plupart des grandes organisations, des domaines d'application spécifiques et même des grands projets auront besoin de règles complémentaires, d'éventuelles restrictions supplémentaires et d'un soutien bibliothécaire accru.
Par exemple, les programmeurs en temps réel dur ne peuvent généralement pas utiliser la mémoire dynamique librement et verront leur choix de bibliothèques restreint.
Nous encourageons l'élaboration de telles règles plus spécifiques en tant qu'addenda à ces directives fondamentales.
Construisez votre petite bibliothèque de fondation idéale et utilisez-la, plutôt que de ramener votre niveau de programmation à un code assembleur sublimé.

Les règles sont conçues pour permettre une [adoption progressive](027-modernizing.md).

Certaines règles visent à accroître différentes formes de sécurité tandis que d'autres visent à réduire la probabilité d'incidents ; beaucoup font les deux.
Les directives visant à prévenir les incidents interdisent souvent du C++ parfaitement légal.
Cependant, lorsque deux manières d'exprimer une idée existent et que l'une s'est révélée être une source fréquente d'erreurs tandis que l'autre ne l'est pas, nous cherchons à orienter les programmeurs vers la seconde.

## <a name="ss-non"></a>In.not : Non-objectifs

Les règles ne sont pas censées être minimales ni orthogonales.
En particulier, les règles générales peuvent être simples, mais difficiles à faire respecter.
De plus, il est souvent difficile de comprendre les implications d'une règle générale.
Les règles plus spécialisées sont souvent plus faciles à comprendre et à faire respecter, mais sans les règles générales, elles ne seraient qu'une longue liste de cas particuliers.
Nous proposons des règles destinées à aider les débutants ainsi que des règles soutenant un usage expert.
Certaines règles peuvent être totalement appliquées mécaniquement, mais d'autres reposent sur des heuristiques.

Ces règles ne sont pas conçues pour être lues de façon séquentielle, comme un livre.
Vous pouvez les parcourir à l'aide des liens.
Cependant, leur usage principal est de servir de cibles pour des outils.
Autrement dit, un outil détecte les violations et renvoie des liens vers les règles violées.
Les règles fournissent alors des justifications, des exemples des conséquences potentielles de la violation et des solutions suggérées.

Ces directives ne sont pas censées remplacer un tutoriel sur le C++.
Si vous avez besoin d'un tutoriel adapté à votre niveau d'expérience, consultez [les références](021-references.md).

Ce n'est pas un guide sur la conversion de l'ancien C++ en un code plus moderne.
Il est destiné à formuler, de manière concrète, des idées pour le nouveau code.
Cependant, consultez la [section sur la modernisation](027-modernizing.md) pour quelques approches possibles de modernisation/jeunesse/mise à niveau.
Il est important de noter que les règles soutiennent l'adoption progressive : il est généralement impossible de convertir entièrement une grande base de code d'un seul coup.

Ces directives ne sont pas censées être exhaustives ou exactes dans le moindre détail technique du langage.
Pour la parole définitive sur les questions de définition du langage, y compris toutes les exceptions aux règles générales et toutes les fonctionnalités, consultez la norme ISO C++.

Les règles ne sont pas destinées à vous forcer à écrire dans un sous-ensemble appauvri du C++.
Elles ne visent *surtout pas* à définir un sous-ensemble ressemblant à Java, par exemple.
Elles ne visent pas à définir un unique « véritable C++ ».
Nous valorisons l'expressivité et les performances sans compromis.

Les règles ne sont pas neutres sur le plan des valeurs.
Elles sont destinées à rendre le code plus simple et plus correct/plus sûr que la plupart du code C++ existant, sans perte de performances.
Elles sont destinées à freiner le C++ parfaitement valide qui est corrélé aux erreurs, à la complexité superflue et aux mauvaises performances.

Les règles ne sont pas assez précises pour qu'une personne (ou une machine) puisse les suivre sans y réfléchir.
Les sections d'application tentent de l'être, mais nous préférons laisser une règle ou une définition un peu vague
et ouverte à l'interprétation plutôt que de préciser quelque chose de manière exacte et erronée.
Parfois, la précision ne vient qu'avec le temps et l'expérience.
La conception n'est pas (encore) une forme de Mathématique.

Les règles ne sont pas parfaites.
Une règle peut nuire en interdisant quelque chose d'utile dans une situation donnée.
Une règle peut nuire en omettant d'interdire quelque chose qui permet une erreur grave dans une situation donnée.
Une règle peut causer beaucoup de préjudice en étant vague, ambiguë, inapplicable ou en permettant toute solution à un problème.
Il est impossible de remplir totalement le critère de « ne pas nuire ».
Au lieu de cela, notre objectif est plus modeste : « Faire le plus de bien pour le plus grand nombre de programmeurs » ;
si vous ne pouvez pas accepter une règle, objectez, ignorez-la, mais ne la diluez pas jusqu'à ce qu'elle devienne dénuée de sens.
Suggérez également une amélioration.

## <a name="ss-force"></a>In.force : Application des règles

Des règles sans mécanisme d'application sont ingérables pour de grandes bases de code.
L'application de toutes les règles n'est possible que pour un petit ensemble de règles peu contraignant ou pour une communauté d'utilisateurs spécifique.

* Mais nous voulons de nombreuses règles, et des règles que tout le monde peut utiliser.
* Mais chacun a des besoins différents.
* Mais les gens n'aiment pas lire de nombreuses règles.
* Mais les gens ne peuvent pas retenir un grand nombre de règles.

Il nous faut donc un découpage par sous-ensembles pour répondre à une variété de besoins.

* Mais un découpage arbitraire mène au chaos.

Nous voulons des directives qui aident beaucoup de monde, rendent le code plus uniforme et encouragent fortement les gens à moderniser leur code.
Nous voulons encourager les bonnes pratiques, plutôt que de tout laisser au choix individuel et aux pressions managériales.
L'idéal est d'utiliser toutes les règles ; cela apporte les bénéfices les plus grands.

Cela engendre pas mal de dilemmes.
Nous essayons de les résoudre à l'aide d'outils.
Chaque règle a une section **Application** listant des idées de contrôle.
L'application peut se faire par revue de code, par analyse statique, par le compilateur ou par des vérifications à l'exécution.
Lorsque c'est possible, nous préférons les vérifications « mécaniques » (les humains sont lents, imprécis et s'ennuient facilement) et les vérifications statiques.
Les vérifications à l'exécution ne sont suggérées que rarement, lorsque aucune alternative n'existe ; nous ne voulons pas introduire de « surcharge distribuée ».
Lorsqu'il y a lieu, nous étiquetons une règle (dans les sections **Application**) avec le nom de groupes de règles connexes (appelés « profils »).
Une règle peut appartenir à plusieurs profils, ou à aucun.
Pour commencer, nous avons quelques profils correspondant à des besoins courants (aspirations, idéaux) :

* **type** : Aucune violation de type (reinterprétation d'un `T` en `U` par casts, unions ou varargs)
* **bounds** : Aucune violation de bornes (accès au-delà de la plage d'un tableau)
* **lifetime** : Aucune fuite (oubli de `delete` ou double `delete`) et aucun accès à des objets invalides (déréférencement de `nullptr`, utilisation d'une référence perrante).

Les profils sont destinés à être utilisés par des outils, mais servent également d'aide à la lecture humaine.
Nous ne limitons pas nos commentaires dans les sections **Application** aux choses que nous savons faire appliquer ; certains commentaires sont de simples souhaits susceptibles d'inspirer un constructeur d'outils.

Les outils qui implémentent ces règles devront respecter la syntaxe suivante pour supprimer explicitement une règle :

    [[gsl::suppress("tag")]]

et éventuellement avec un message (suivant la syntaxe habituelle des attributs du standard C++11) :

    [[gsl::suppress("tag", justification: "message")]]

où

* `"tag"` est un littéral de chaîne contenant le nom de l'ancre de l'élément où la règle d'application apparaît (par exemple, pour [C.134](007-class.md#rh-public) il s'agit de « rh-public »), le
nom d'un groupe de règles par profil (« type », « bounds » ou « lifetime »),
ou une règle spécifique dans un profil ([type.4](022-profile.md#pro-type-cstylecast) ou [bounds.2](022-profile.md#pro-bounds-arrayindex)). Tout texte qui ne correspond à aucun de ces éléments doit être rejeté.

* `"message"` est un littéral de chaîne

## <a name="ss-struct"></a>In.struct : Structure de ce document

Chaque règle (directive, suggestion) peut avoir plusieurs parties :

* La règle elle-même — par ex. **pas de `new` à nu**
* Un numéro de référence de règle — par ex. **C.7** (la 7ᵉ règle relative aux classes).
  Comme les sections principales ne sont pas intrinsèquement ordonnées, nous utilisons des lettres comme première partie d'un numéro de référence de règle.
  Nous laissons des lacunes dans la numérotation pour minimiser la « perturbation » lors de l'ajout ou du retrait de règles.
* **Raisons** (justifications) — car les programmeurs ont du mal à respecter des règles qu'ils ne comprennent pas
* **Exemples** — car les règles sont difficiles à comprendre de manière abstraite ; peuvent être positifs ou négatifs
* **Alternatives** — pour les règles de type « ne faites pas ceci »
* **Exceptions** — nous préférons des règles générales simples. Cependant, de nombreuses règles s'appliquent largement, mais pas universellement, il faut donc lister les exceptions
* **Application** — des idées sur la manière dont la règle pourrait être vérifiée « mécaniquement »
* **Voir aussi** — des références à des règles connexes et/ou des discussions complémentaires (dans ce document ou ailleurs)
* **Notes** (commentaires) — quelque chose qui doit être dit et qui ne rentre pas dans les autres catégories
* **Discussion** — des références à des justifications plus étendues et/ou des exemples placés en dehors des listes principales de règles

Certaines règles sont difficiles à vérifier mécaniquement, mais elles toutes remplissent le critère minimal selon lequel un programmeur expert peut repérer de nombreuses violations sans trop de difficulté.
Nous espérons que les outils « mécaniques » s'amélioreront avec le temps pour s'approcher de ce que tel programmeur expert remarque.
En outre, nous supposons que les règles seront affinées au fil du temps pour les rendre plus précises et vérifiables.

Une règle vise à être simple, plutôt que soigneusement formulée pour mentionner chaque alternative et cas particulier.
De telles informations sont trouvées dans les paragraphes **Alternatives** et les sections [Discussion](028-discussion.md).
Si vous ne comprenez pas une règle ou êtes en désaccord avec elle, veuillez consulter sa **Discussion**.
Si vous estimez qu'une discussion manque ou est incomplète, créez un [Issue](https://github.com/isocpp/CppCoreGuidelines/issues)
expliquant vos préoccupations et éventuellement une PR correspondante.

Les exemples sont écrits pour illustrer les règles.

* Les exemples ne sont pas destinés à être de qualité production ni à couvrir toutes les dimensions d'un tutoriel.
Par exemple, de nombreux exemples sont d'ordre technique du langage et utilisent des noms comme `f`, `base` et `x`.
* Nous cherchons à nous assurer que les exemples « bons » respectent les Directives fondamentales.
* Les commentaires illustrent souvent des règles là où ils seraient inutiles et/ou distrayants dans un « vrai code ».
* Nous supposons la connaissance de la bibliothèque standard. Par exemple, nous utilisons `vector` plutôt que `std::vector`.

Ce n'est pas un manuel de langage.
Il est destiné à être utile, plutôt qu'exhaustif, parfaitement exact sur les détails techniques ou un guide de lecture de code existant.
Les sources d'information recommandées se trouvent dans [les références](021-references.md).

## <a name="ss-sec"></a>In.sec : Sections principales

* [In : Introduction](003-introduction.md)
* [P : Philosophie](004-philosophy.md)
* [I : Interfaces](005-interfaces.md)
* [F : Fonctions](006-functions.md)
* [C : Classes et hiérarchies de classes](007-class.md)
* [Enum : Énumérations](008-enum.md)
* [R : Gestion des ressources](009-resource.md)
* [ES : Expressions et déclarations](010-expr.md)
* [Per : Performances](011-performance.md)
* [CP : Concurrence et parallélisme](012-concurrency.md)
* [E : Gestion des erreurs](013-errors.md)
* [Con : Constantes et immuabilité](014-const.md)
* [T : Modèles et programmation générique](015-templates.md)
* [CPL : Programmation de style C](016-cpl.md)
* [SF : Fichiers source](017-source.md)
* [SL : La bibliothèque standard](#sl-the-standard-library) <!-- @TODO-LINK : l'ancre "sl-the-standard-library" n'est pas définie dans ce document -->

Sections de support :

* [A : Idées architecturales](019-a.md)
* [NR : Non-règles et mythes](020-not.md)
* [RF : Références](021-references.md)
* [Pro : Profils](022-profile.md)
* [GSL : Bibliothèque de support des directives](#gsl-guidelines-support-library) <!-- @TODO-LINK : l'ancre "gsl-guidelines-support-library" n'est pas définie dans ce document -->
* [NL : Suggestions de noms et de mise en page](024-naming.md)
* [FAQ : Réponses aux questions fréquentes](025-faq.md)
* [Annexe A : Bibliothèques](026-libraries.md)
* [Annexe B : Modernisation du code](027-modernizing.md)
* [Annexe C : Discussion](028-discussion.md)
* [Annexe D : Outils de support](029-tools.md)
* [Glossaire](030-glossary.md)
* [À faire : Règles proto non classifiées](031-unclassified.md)

Ces sections ne sont pas orthogonales.

Chaque section (par ex. « P » pour « Philosophie ») et chaque sous-section (par ex. « C.hier » pour « Hiérarchies de classes (POO) ») ont une abréviation pour faciliter la recherche et la référence.
Les abréviations des sections principales sont également utilisées dans les numéros de règles (par ex. « C.11 » pour « Rendre les types concrets réguliers »).