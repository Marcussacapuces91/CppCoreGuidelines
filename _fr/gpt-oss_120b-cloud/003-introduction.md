# <a name="s-introduction"></a>In: Introduction

Il s'agit d'un ensemble de lignes directrices essentielles pour le C++ moderne (actuellement C++20 et C++17) en tenant compte des améliorations futures probables ainsi que des Spécifications Techniques ISO (TS). L'objectif est d'aider les programmeurs C++ à écrire du code plus simple, plus efficace et plus maintenable.

Résumé de l'introduction :

* [In.target : Public cible](#ss-readers)
* [In.aims : Objectifs](#ss-aims)
* [In.not : Ce qui n'est pas visé](#ss-non)
* [In.force : Application](#ss-force)
* [In.struct : Structure de ce document](#ss-struct)
* [In.sec : Sections principales](#ss-sec)

## <a name="ss-readers"></a>In.target : Public cible

Tous les programmeurs C++. Cela inclut les [programmeurs qui pourraient envisager C](016-cpl.md).

## <a name="ss-aims"></a>In.aims : Objectifs

L'objectif de ce document est d'aider les développeurs à adopter le C++ moderne (actuellement C++20 et C++17) et à obtenir un style plus uniforme à travers les bases de code.

Nous ne succombons pas à l'illusion que chacune de ces règles peut être appliquée efficacement à chaque base de code. Moderniser d'anciens systèmes est difficile. Cependant, nous pensons qu'un programme qui applique une règle est moins sujet aux erreurs et plus maintenable qu'un programme qui ne le fait pas. Souvent, les règles mènent également à un développement initial plus rapide et plus simple.

Pour autant que nous puissions en juger, ces règles conduisent à du code qui fonctionne aussi bien, voire mieux, que les techniques plus anciennes et plus conventionnelles ; elles s'appuient sur le principe du zéro coût (« ce que vous n'utilisez pas, vous ne payez pas » ou « lorsque vous utilisez correctement un mécanisme d'abstraction, vous obtenez au moins des performances aussi bonnes que si vous aviez codé manuellement en utilisant des constructions de bas niveau »).

Considérez ces règles comme des idéaux pour le nouveau code, des opportunités à exploiter lors du travail sur du code existant, et essayez de vous rapprocher le plus possible de ces idéaux. Rappelez‑vous :

### <a name="r0"></a>In.0 : Ne paniquez pas !

Prenez le temps de comprendre les implications d'une règle de ligne directrice sur votre programme.

Ces lignes directrices sont conçues selon le principe du « sous‑ensemble du sur‑ensemble » ([Stroustrup05](032-bibliography.md#Stroustrup05)). Elles ne définissent pas simplement un sous‑ensemble de C++ à utiliser (pour la fiabilité, la sécurité, les performances, ou autre). Au contraire, elles recommandent fortement l'utilisation de quelques « extensions » simples ([composants de bibliothèque](#gsl-guidelines-support-library)) qui rendent redondante l'utilisation des caractéristiques les plus sujettes aux erreurs du C++, de façon à pouvoir les interdire (dans notre ensemble de règles). @TODO-LINK

Les règles mettent l'accent sur la sécurité de type statique et la sécurité des ressources. Pour cette raison, elles soulignent les possibilités de contrôle de limites, d'éviter la déréférencement de `nullptr`, d'éviter les pointeurs pendants, ainsi que l'utilisation systématique des exceptions (via RAII). En partie pour atteindre cet objectif et en partie pour réduire le code obscur comme source d'erreurs, les règles mettent également l'accent sur la simplicité et sur le fait de masquer la complexité nécessaire derrière des interfaces bien spécifiées.

Beaucoup de règles sont prescriptives. Nous sommes mal à l'aise avec des règles qui se contentent de dire « ne faites pas cela ! » sans offrir d'alternative. L'une des conséquences est que certaines règles ne peuvent être soutenues que par des heuristiques, plutôt que par des vérifications précises et mécaniquement vérifiables. D'autres règles formulent des principes généraux. Pour ces règles plus générales, des règles plus détaillées et spécifiques offrent un contrôle partiel.

Ces lignes directrices portent sur le cœur du C++ et son utilisation. Nous nous attendons à ce que la plupart des grandes organisations, les domaines d'application spécifiques, et même les grands projets, aient besoin de règles supplémentaires, possiblement de restrictions supplémentaires, et de soutien supplémentaire de bibliothèques. Par exemple, les programmeurs temps réel strict ne peuvent généralement pas utiliser la mémoire libre (mémoire dynamique) de façon illimitée et seront limités dans le choix des bibliothèques. Nous encourageons le développement de telles règles plus spécifiques en tant qu'addenda à ces lignes directrices de base. Construisez votre petite bibliothèque de fondation idéale et utilisez‑la, plutôt que d'abaisser votre niveau de programmation à du code assembleur glorifié.

Les règles sont conçues pour permettre [une adoption progressive](027-modernizing.md).

Certaines règles visent à augmenter diverses formes de sécurité tandis que d'autres cherchent à réduire la probabilité d'accidents, et beaucoup font les deux. Les lignes directrices visant à prévenir les accidents interdisent souvent du C++ parfaitement légal. Cependant, lorsqu'il existe deux façons d'exprimer une idée et que l'une s'est révélée source fréquente d'erreurs tandis que l'autre ne l'est pas, nous essayons d'orienter les programmeurs vers cette dernière.

## <a name="ss-non"></a>In.not : Ce qui n'est pas visé

Les règles ne sont pas destinées à être minimalistes ou orthogonales. En particulier, les règles générales peuvent être simples, mais inaptes à être appliquées. De plus, il est souvent difficile de comprendre les implications d'une règle générale. Les règles plus spécialisées sont souvent plus faciles à comprendre et à appliquer, mais sans règles générales, elles ne seraient qu'une longue liste de cas particuliers. Nous proposons des règles visant à aider les novices ainsi que des règles soutenant l'usage expert. Certaines règles peuvent être appliquées de manière totalement automatique, mais d'autres reposent sur des heuristiques.

Ces règles ne sont pas destinées à être lues séquentiellement, comme un livre. Vous pouvez les parcourir en utilisant les liens. Cependant, leur usage principal prévu est de servir de cibles pour les outils. C'est‑à‑dire qu'un outil recherche les violations et renvoie des liens vers les règles enfreintes. Les règles fournissent alors les raisons, des exemples des conséquences potentielles de la violation, ainsi que des remèdes suggérés.

Ces lignes directrices ne sont pas destinées à remplacer un didacticiel sur le C++. Si vous avez besoin d'un tutoriel pour un certain niveau d'expérience, consultez [les références](021-references.md).

Ce n'est pas un guide expliquant comment convertir du vieux code C++ en code plus moderne. Il vise à formuler les idées pour un nouveau code de manière concrète. Cependant, consultez [la section sur la modernisation](027-modernizing.md) pour quelques approches possibles de modernisation/régénération/mise à jour. Il est important de noter que les règles supportent une adoption progressive : il est généralement irréalisable de convertir entièrement une grande base de code d'un seul coup.

Ces lignes directrices ne visent pas à être complètes ou exactes dans chaque détail technique du langage. Pour le mot de la fin sur les questions de définition du langage, incluant chaque exception aux règles générales et chaque fonctionnalité, consultez la norme ISO C++.

Les règles ne visent pas à vous contraindre à écrire dans un sous‑ensemble imposé du C++. Elles ne sont *en aucun cas* destinées à définir, par exemple, un sous‑ensemble du C++ à la Java. Elles ne visent pas à définir un seul « vrai C++ ». Nous valorisons l'expressivité et les performances sans compromis.

Les règles ne sont pas neutres en termes de valeur. Elles visent à rendre le code plus simple et plus correct/sûr que la plupart des codes C++ existants, sans perte de performances. Elles visent à empêcher des codes C++ parfaitement valides qui sont associés à des erreurs, à une complexité superflue et à des performances médiocres.

Les règles ne sont pas d'une précision telle qu'une personne (ou une machine) puisse les suivre sans réfléchir. Les parties d'application tentent d'atteindre ce but, mais nous préférons laisser une règle ou une définition légèrement vague et ouverte à interprétation plutôt que de spécifier quelque chose de façon précise et incorrecte. Parfois, la précision ne vient qu'avec le temps et l'expérience. Le design n'est pas (encore) une forme de mathématiques.

Les règles ne sont pas parfaites. Une règle peut nuire en interdisant quelque chose d'utile dans une situation donnée. Une règle peut nuire en ne prohibant pas quelque chose qui engendre une erreur grave dans une situation donnée. Une règle peut causer beaucoup de tort en étant vague, ambiguë, inapplicable, ou en permettant n'importe quelle solution à un problème. Il est impossible de satisfaire pleinement le critère « ne pas nuire ». Au lieu de cela, notre objectif est moins ambitieux : « Faire le maximum de bien pour la plupart des programmeurs » ; si vous ne pouvez pas vivre avec une règle, opposez‑vous à elle, ignorez‑la, mais ne l'assouplissez pas au point qu'elle devienne insignifiante. De plus, suggérez une amélioration.

## <a name="ss-force"></a>In.force : Application

Les règles sans mécanisme d'application sont ingérables pour les grandes bases de code. L'application de toutes les règles n'est possible que pour un petit ensemble limité de règles ou pour une communauté d'utilisateurs spécifique.

* Mais nous voulons de nombreuses règles, et nous voulons des règles que tout le monde puisse utiliser.
* Mais les gens ont des besoins différents.
* Mais les gens n'aiment pas lire beaucoup de règles.
* Mais les gens ne peuvent pas se souvenir de nombreuses règles.

Donc, nous devons sous‑sélectionner pour répondre à une variété de besoins.

* Mais une sous‑sélection arbitraire conduit au chaos.

Nous voulons des lignes directrices qui aident un grand nombre de personnes, rendent le code plus uniforme et encouragent fortement les gens à moderniser leur code. Nous souhaitons encourager les meilleures pratiques, plutôt que de laisser tout au choix individuel et aux pressions de la gestion. L'idéal est d'utiliser toutes les règles ; cela apporte les plus grands bénéfices.

Cela aboutit à plusieurs dilemmes. Nous essayons de les résoudre en utilisant des outils. Chaque règle possède une section **Application** (Enforcement) listant des idées d'application. L'application peut se faire par révision de code, par analyse statique, par le compilateur, ou par des vérifications à l'exécution. Dans la mesure du possible, nous préférons les contrôles « mécaniques » (les humains sont lents, imprécis et s'ennuient rapidement) et les vérifications statiques. Les vérifications à l'exécution ne sont proposées que rarement lorsqu'aucune alternative n'existe ; nous ne voulons pas introduire de « gonflement distribué ». Le cas échéant, nous étiquetons une règle (dans la section **Application**) avec le nom d'un groupe de règles connexes (appelés « profils »). Une règle peut faire partie de plusieurs profils, ou d'aucun. Pour commencer, nous avons quelques profils correspondant à des besoins courants (désirs, idéaux) :

* **type** : Pas de violations de type (réinterpréter un `T` comme un `U` via des casts, unions ou varargs)
* **bounds** : Pas de violations de limites (accès au‑delà de la portée d'un tableau)
* **lifetime** : Pas de fuites (omission de `delete` ou `delete` multiple) et pas d'accès à des objets invalides (déréférencement de `nullptr`, utilisation d'une référence pendante).

Les profils sont destinés à être utilisés par les outils, mais servent également d'aide au lecteur humain. Nous ne limitons pas nos commentaires dans les sections **Application** aux choses que nous savons comment appliquer ; certains commentaires ne sont que des souhaits qui pourraient inspirer un concepteur d'outil.

Les outils qui implémentent ces règles doivent respecter la syntaxe suivante pour supprimer explicitement une règle :

    [[gsl::suppress("tag")]]

et éventuellement avec un message (en suivant la syntaxe habituelle des attributs C++11) :

    [[gsl::suppress("tag", justification: "message")]]

où

* `"tag"` est une chaîne littérale contenant le nom d'ancre de l'élément où apparaît la règle d'application (par exemple, pour [C.134](007-class.md#rh-public) c'est « rh-public »), le nom d'un groupe de profil de règles (« type », « bounds » ou « lifetime ») ou une règle spécifique dans un profil ([type.4](022-profile.md#pro-type-cstylecast), ou [bounds.2](022-profile.md#pro-bounds-arrayindex)). Tout texte qui ne correspond pas à l'un de ceux‑ci doit être rejeté.
* `"message"` est une chaîne littérale

## <a name="ss-struct"></a>In.struct : Structure de ce document

Chaque règle (ligne directrice, suggestion) peut comporter plusieurs parties :

* La règle elle‑même — par ex., **pas de `new` nu**
* Un numéro de référence de règle — par ex., **C.7** (la 7ᵉ règle liée aux classes).
  Comme les sections principales ne sont pas intrinsèquement ordonnées, nous utilisons des lettres comme première partie d'un « numéro de référence de règle ». Nous laissons des intervalles dans la numérotation afin de minimiser les « perturbations » lorsque nous ajoutons ou supprimons des règles.
* **Raisons** (justifications) — parce que les programmeurs ont du mal à suivre des règles qu'ils ne comprennent pas
* **Exemples** — parce que les règles sont difficiles à comprendre de manière abstraite ; ils peuvent être positifs ou négatifs
* **Alternatives** — pour les règles du type « ne faites pas cela »
* **Exceptions** — nous privilégions les règles générales simples. Cependant, de nombreuses règles s'appliquent largement, mais pas universellement, donc les exceptions doivent être listées
* **Application** — idées sur la façon dont la règle pourrait être vérifiée « mécaniquement »
* **Voir aussi** — références aux règles connexes et/ou à des discussions supplémentaires (dans ce document ou ailleurs)
* **Notes** (commentaires) — quelque chose qui mérite d'être dit mais qui ne correspond à aucune autre catégorie
* **Discussion** — références à des justifications plus détaillées et/ou à des exemples placés en dehors des listes principales de règles

Certaines règles sont difficiles à vérifier mécaniquement, mais elles remplissent toutes le critère minimal selon lequel un programmeur expert peut repérer de nombreuses violations sans trop d'effort. Nous espérons que les outils « mécaniques » s'amélioreront avec le temps pour approcher ce qu'un tel programmeur expert remarque. Nous supposons également que les règles seront affûtées au fil du temps afin de les rendre plus précises et vérifiables.

Une règle vise à être simple, plutôt qu'à être formulée avec soin pour mentionner chaque alternative et cas particulier. Ces informations se trouvent dans les paragraphes **Alternatives** et les sections [Discussion](028-discussion.md). Si vous ne comprenez pas une règle ou êtes en désaccord avec elle, veuillez consulter sa **Discussion**. Si vous estimez qu'une discussion manque ou est incomplète, créez un [Issue](https://github.com/isocpp/CppCoreGuidelines/issues) en expliquant vos préoccupations et éventuellement un PR correspondant.

Les exemples sont rédigés pour illustrer les règles.

* Les exemples ne sont pas destinés à être de qualité production ni à couvrir toutes les dimensions d'un didacticiel. Par exemple, de nombreux exemples sont technique‑linguistiques et utilisent des noms comme `f`, `base` et `x`.
* Nous essayons de garantir que les exemples « bons » respectent les Core Guidelines.
* Les commentaires illustrent souvent les règles alors qu'ils seraient inutiles et/ou distrayants dans du « code réel ».
* Nous supposons la connaissance de la bibliothèque standard. Par exemple, nous utilisons simplement `vector` au lieu de `std::vector`.

Ce n'est pas un manuel de langage. Il se veut utile, plutôt que complet, entièrement exact sur les détails techniques, ou un guide du code existant. Les sources d'information recommandées se trouvent dans [les références](021-references.md).

## <a name="ss-sec"></a>In.sec : Sections principales

* [In : Introduction](003-introduction.md)
* [P : Philosophie](004-philosophy.md)
* [I : Interfaces](005-interfaces.md)
* [F : Fonctions](006-functions.md)
* [C : Classes et Hiérarchies de Classes](007-class.md)
* [Enum : Énumérations](008-enum.md)
* [R : Gestion des Ressources](009-resource.md)
* [ES : Expressions et Instructions](010-expr.md)
* [Per : Performance](011-performance.md)
* [CP : Concurrence et Parallélisme](012-concurrency.md)
* [E : Gestion des Erreurs](013-errors.md)
* [Con : Constantes et Immutabilité](014-const.md)
* [T : Modèles et Programmation Générique](015-templates.md)
* [CPL : Programmation de Style C](016-cpl.md)
* [SF : Fichiers Source](017-source.md)
* [SL : Bibliothèque Standard (stdlib)](018-stdlib.md)

Sections d'appui :

* [A : Idées Architecturales](019-a.md)
* [NR : Non‑Règles et Mythes](020-not.md)
* [RF : Références](021-references.md)
* [Pro : Profils](022-profile.md)
* [GSL : Bibliothèque d'Appui aux Lignes Directrices](023-gsl.md)
* [NL : Nommage et Mise en Page](024-naming.md)
* [FAQ : Réponses aux Questions Fréquentes](025-faq.md)
* [Annexe A : Bibliothèques](026-libraries.md)
* [Annexe B : Modernisation du Code](027-modernizing.md)
* [Annexe C : Discussion](028-discussion.md)
* [Annexe D : Outils de Soutien](029-tools.md)
* [Glossaire](030-glossary.md)
* [À faire : Proto-règles non classées](031-unclassified.md)

Ces sections ne sont pas orthogonales.

Chaque section (par ex., « P » pour « Philosophie ») et chaque sous‑section (par ex., « C.hier » pour « Class Hierarchies (OOP) ») possède une abréviation pour faciliter la recherche et la référence. Les abréviations des sections principales sont également utilisées dans les numéros de règle (par ex., « C.11 » pour « Make concrete types regular »).
