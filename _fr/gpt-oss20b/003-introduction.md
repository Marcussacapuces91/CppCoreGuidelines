# <a name="s-introduction"></a>In: Introduction

Il s'agit d'un ensemble de directives fondamentales pour le C++ moderne (actuellement C++20 et C++17), prenant en compte les améliorations futures probables et les spécifications techniques ISO (TS).  
L'objectif est d'aider les programmeurs C++ à écrire du code plus simple, plus efficace et plus facile à maintenir.

Résumé de l'introduction :

* [In.target : Public visé](#ss-readers)
* [In.aims : Objectifs](#ss-aims)
* [In.not : Non-Objectifs](#ss-non)
* [In.force : Application](#ss-force)
* [In.struct : La structure de ce document](#ss-struct)
* [In.sec : Sections principales](#ss-sec)

## <a name="ss-readers"></a>In.target : Public visé

Tous les programmeurs C++. Cela inclut [les programmeurs qui pourraient envisager le C](016-cpl.md).

## <a name="ss-aims"></a>In.aims : Objectifs

Le but de ce document est d'aider les développeurs à adopter le C++ moderne (actuellement C++20 et C++17) et à obtenir un style plus uniforme à travers les bases de code.

Nous ne croyons pas à la naïveté selon laquelle chacune de ces règles peut être efficacement appliquée à chaque base de code. Mettre à niveau les anciens systèmes est difficile. Cependant, nous pensons qu'un programme qui applique une règle est moins sujet aux erreurs et plus maintenable qu'un programme qui ne l'applique pas. Souvent, les règles conduisent également à un développement initial plus rapide ou plus facile.

Autant que nous pouvons le constater, ces règles produisent un code qui fonctionne aussi bien ou mieux que les techniques plus anciennes et plus conventionnelles ; elles sont destinées à suivre le principe d'absence de surcharge (« ce que vous n'utilisez pas, vous n'y payez pas » ou « lorsque vous utilisez un mécanisme d'abstraction de façon appropriée, vous obtenez au moins des performances équivalentes à celles d'un code écrit à la main avec des constructions de bas niveau »).

Considérez ces règles comme des idéaux pour le nouveau code, des opportunités à exploiter lorsque vous travaillez sur l'ancien code, et essayez d'approcher ces idéaux aussi près que possible.

Remember:

### <a name="r0"></a>In.0 : Ne paniquez pas !

Prenez le temps de comprendre les implications d'une règle de directive sur votre programme.

Ces directives sont conçues selon le principe du « sous-ensemble du sur-ensemble » ([Stroustrup05](#Stroustrup05)).  
Ils ne définissent pas simplement un sous-ensemble de C++ à utiliser (pour la fiabilité, la sécurité, les performances ou autre).  
À la place, ils recommandent fortement l'usage de quelques « extensions » simples ([composants de la bibliothèque](#gsl-guidelines-support-library)) qui rendent l'utilisation des fonctionnalités les plus sujettes à erreurs de C++ redondante, de façon à ce qu'elles puissent être interdites (dans notre ensemble de règles).

Les règles soulignent la sécurité statique des types et la sécurité des ressources. À cette fin, elles insistent sur les possibilités de vérification de plage, d'éviter de déréférencer `nullptr`, d'éviter les pointeurs pendants, et l'utilisation systématique des exceptions (via RAII). En partie pour atteindre cet objectif et en partie pour minimiser le code obscur en tant que source d'erreurs, les règles soulignent également la simplicité et la dissimulation de la complexité nécessaire derrière des interfaces bien spécifiées.

Bon nombre des règles sont prescriptives. Nous nous sentons mal à l'aise avec les règles qui se contentent d'affirmer « ne faites pas cela ! » sans proposer d'alternative. Une conséquence de cela est que certaines règles ne peuvent être soutenues qu'au moyen d'heuristiques, plutôt que de contrôles précis et mécaniquement vérifiables. D'autres règles expriment des principes généraux. Pour ces règles plus générales, des règles plus détaillées et spécifiques offrent une vérification partielle.

Ces directives traitent du cœur du C++ et de son utilisation. Nous prévoyons que la plupart des grandes organisations, des domaines d'application spécifiques, et même des grands projets auront besoin de règles supplémentaires, potentiellement plus restrictives, ainsi que d'un support de bibliothèque supplémentaire. Par exemple, les programmeurs en temps réel strict ne peuvent généralement pas utiliser librement le heap (mémoire dynamique) et seront restreints dans le choix de leurs bibliothèques. Nous encourageons le développement de règles plus spécifiques comme des annexes à ces directives de base. Construisez votre bibliothèque de base idéale et utilisez-la, plutôt que de réduire votre niveau de programmation à un code assembleur glorifié.

Les règles sont conçues pour permettre une [adoption progressive](027-modernizing.md).

Certaines règles visent à augmenter diverses formes de sécurité tandis que d'autres cherchent à réduire la probabilité d'accidents, beaucoup font les deux. Les directives visant à prévenir les accidents interdisent souvent du C++ parfaitement légal. Cependant, lorsqu'il existe deux manières d'exprimer une idée et qu'une est source fréquente d'erreurs alors qu'une autre ne l'est pas, nous essayons d'orienter les programmeurs vers la seconde.

## <a name="ss-non"></a>In.not : Non-Objectifs

Les règles ne sont pas destinées à être minimales ou orthogonales. En particulier, les règles générales peuvent être simples, mais non applicables. De plus, il est souvent difficile de comprendre les implications d'une règle générale. Les règles plus spécialisées sont souvent plus faciles à comprendre et à appliquer, mais sans règles générales, elles ne constitueraient qu'une longue liste de cas particuliers. Nous fournissons des règles visant à aider les débutants ainsi que des règles soutenant l'utilisation experte. Certaines règles peuvent être entièrement appliquées, tandis que d'autres reposent sur des heuristiques.

Ces règles ne sont pas destinées à être lues de façon séquentielle, comme un livre. Vous pouvez les parcourir en utilisant les liens. Cependant, leur utilisation principale est de servir de cible pour les outils. C'est-à-dire qu'un outil recherche des violations et renvoie des liens vers les règles violées. Les règles fournissent ensuite des raisons, des exemples de conséquences potentielles d'une violation et des remèdes suggérés.

Ces directives ne sont pas destinées à remplacer un traitement tutoriel du C++. Si vous avez besoin d'un tutoriel pour un niveau d'expérience donné, consultez [les références](021-references.md).

Ce n'est pas un guide sur la façon de convertir du vieux code C++ vers une version plus moderne. Il est destiné à articuler des idées pour un nouveau code de façon concrète. Cependant, consultez [la section de modernisation](027-modernizing.md) pour certaines approches possibles de modernisation/réjuvenation/mise à niveau. Il est important que les règles prennent en charge l'adoption progressive : il est généralement irréalisable de convertir complètement une grande base de code d'un seul coup.

Ces directives ne sont pas destinées à être complètes ou exactes dans chaque détail technique du langage. Pour la prise de décision final sur les questions de définition du langage, incluant chaque exception aux règles générales et chaque caractéristique, consultez le standard ISO C++.

Les règles ne visent pas à vous obliger à écrire dans un sous-ensemble impoverissant du C++. Ils ne sont pas *évidemment* destinés à définir un sous-ensemble, disons, semblable à Java de C++. Ils ne sont pas destinés à définir un seul langage « vrai C++ ». Nous valorisons l'expressivité et la performance sans compromis.

Les règles ne sont pas neutres sur le plan de la valeur. Elles visent à rendre le code plus simple et plus correct/sûr que la plupart des codes C++ existants, sans perte de performance. Elles visent à restreindre le code C++ parfaitement valide qui se corrèle avec des erreurs, une complexité sporadique et de mauvaises performances.

Les règles ne sont pas aussi précises qu'une personne (ou une machine) puisse les suivre sans réfléchir. Les parties d'application tentent d'être ainsi, mais nous préférons laisser une règle ou une définition un peu vague et ouverte à l'interprétation plutôt que de spécifier quelque chose de précis et erroné. Parfois, la précision ne vient qu'avec le temps et l'expérience. La conception n'est (encore) pas une forme de mathématiques.

Les règles ne sont pas parfaites. Une règle peut nuire en interdisant quelque chose qui est utile dans une situation donnée. Une règle peut nuire en ne prohibant pas quelque chose qui permet une erreur grave dans une situation donnée. Une règle peut causer beaucoup de tort en étant vague, ambiguë, inapplicable, ou en permettant toutes les solutions à un problème. Il est impossible de satisfaire complètement aux critères de « ne pas nuire ». Au lieu de cela, notre objectif est le moins ambitieux : « Faire le plus de bien pour le plus grand nombre de programmeurs » ; si vous ne pouvez pas vivre avec une règle, contestez-la, ignorez-la, mais ne la diluez pas jusqu'à ce qu'elle devienne sans signification. De plus, suggérez une amélioration.

## <a name="ss-force"></a>In.force : Application

Les règles sans application sont difficiles à gérer pour de grandes bases de code. L'application de toutes les règles n'est possible que pour un petit ensemble faible de règles ou pour une communauté d'utilisateurs spécifique.

* Nous voulons beaucoup de règles, et nous voulons des règles que tout le monde peut utiliser.  
* Mais les gens ont des besoins différents.  
* Mais les gens n'aiment pas lire beaucoup de règles.  
* Mais les gens ne peuvent pas retenir beaucoup de règles.

Ainsi, nous avons besoin de sous-ensembles pour répondre à une variété de besoins.

* Mais un sous-ensemble arbitraire conduit au chaos.

Nous voulons des directives qui aident beaucoup de gens, rendent le code plus uniforme et encouragent fortement les gens à moderniser leur code. Nous voulons encourager les meilleures pratiques, plutôt que de laisser tout aux choix individuels et aux pressions de gestion. L'idéal est d'utiliser toutes les règles ; cela donne les plus grands bénéfices.

Cela engendre plusieurs dilemmes. Nous essayons de résoudre ces dilemmes à l'aide d'outils. Chaque règle possède une section **Enforcement** énumérant des idées d'application. L'application peut se faire par révision de code, analyse statique, compilateur ou contrôles d'exécution. Dans la mesure du possible, nous préférons la vérification « mécanique » (les humains sont lents, inexacts et s'ennuient facilement) et la vérification statique. Les contrôles d'exécution ne sont suggérés que rarement lorsqu'aucune alternative n'existe ; nous ne voulons pas introduire de « gonflement distribué ». Lorsque cela est approprié, nous labelons une règle (dans les sections **Enforcement**) avec le nom des groupes de règles associées (appelés « profils »). Une règle peut faire partie de plusieurs profils, ou aucun. Pour commencer, nous avons quelques profils correspondant à des besoins communs (désirs, idéaux) :

* **type** : Pas de violations de type (réinterpréter un `T` comme un `U` via cast, unions ou varargs).  
* **bounds** : Pas de violations de limites (accès en dehors de la plage d'un tableau).  
* **lifetime** : Pas de fuites (ne pas faire `delete` ou faire plusieurs `delete`) et pas d'accès à des objets invalides (déréférencer `nullptr`, utiliser une référence pendante).

Les profils sont destinés à être utilisés par les outils, mais servent également d'aide au lecteur humain. Nous ne limitons pas nos commentaires dans les sections **Enforcement** aux choses que nous savons appliquer ; certains commentaires ne sont que de simples souhaits qui peuvent inspirer un développeur d'outil.

Les outils qui mettent en œuvre ces règles doivent respecter la syntaxe suivante pour supprimer explicitement une règle :

    [[gsl::suppress("tag")]]

et, éventuellement, avec un message (conformément à la syntaxe habituelle des attributs standard C++11) :

    [[gsl::suppress("tag", justification: "message")]]

où

* `"tag"` est un littéral de chaîne contenant le nom d'ancre de l'élément où apparaît la règle d'Application (par ex. pour [C.134](#rh-public) il s'agit de « rh-public »), le nom d'un groupe de profils (« type », « bounds » ou « lifetime ») ou une règle spécifique dans un profil ([type.4](#pro-type-cstylecast) ou [bounds.2](#pro-bounds-arrayindex)). Tout texte qui ne correspond pas à l'un de ceux-ci doit être rejeté.  
* `"message"` est un littéral de chaîne.

## <a name="ss-struct"></a>In.struct : La structure de ce document

Chaque règle (directive, suggestion) peut comporter plusieurs parties :

* La règle elle-même – par ex., **no naked `new`**  
  Les sections majeures ne sont pas intrinsèquement ordonnées, nous utilisons des lettres comme première partie d'un numéro de référence de règle. Nous laissons des lacunes dans la numérotation afin de minimiser la « perturbation » lors de l'ajout ou de la suppression de règles.  
* Un numéro de référence de règle – par ex., **C.7** (la 7ᵉ règle liée aux classes).  
* **Raisons** (rationales) – car les programmeurs trouvent difficile de suivre des règles qu'ils ne comprennent pas.  
* **Exemples** – car les règles sont difficiles à comprendre en abstraction ; peuvent être positifs ou négatifs.  
* **Alternatives** – pour les règles « ne faites pas cela ».  
* **Exceptions** – nous préférons des règles générales simples. Cependant, de nombreuses règles s'appliquent largement, mais pas universellement, il faut donc lister les exceptions.  
* **Application** (Enforcement) – idées sur la façon dont la règle pourrait être vérifiée **mécaniquement**.  
* **Voir aussi** – références aux règles liées et/ou discussions supplémentaires (dans ce document ou ailleurs).  
* **Remarques** – quelque chose à dire qui ne correspond pas aux autres classifications.  
* **Discussion** – références à une justification plus étendue et/ou à des exemples placés en dehors des listes principales des règles.

Certaines règles sont difficiles à vérifier mécaniquement, mais elles répondent toutes aux critères minimaux qu'un programmeur expert peut repérer sans trop de difficulté. Nous espérons que les outils « mécaniques » s'amélioreront avec le temps pour approcher ce qu'un tel programmeur expert remarque. De plus, nous supposons que les règles seront affinées au fil du temps pour les rendre plus précises et vérifiables.

## <a name="ss-sec"></a>In.sec : Sections principales

* [In: Introduction](003-introduction.md)  
* [P: Philosophie](004-philosophy.md)  
* [I: Interfaces](005-interfaces.md)  
* [F: Fonctions](006-functions.md)  
* [C: Classes et hiérarchies de classes](007-class.md)  
* [Enum: Énumérations](008-enum.md)  
* [R: Gestion des ressources](009-resource.md)  
* [ES: Expressions et déclarations](010-expr.md)  
* [Per: Performance](011-performance.md)  
* [CP: Concurrence et parallélisme](012-concurrency.md)  
* [E: Gestion des erreurs](013-errors.md)  
* [Con: Constantes et immutabilité](014-const.md)  
* [T: Templates et programmation générique](015-templates.md)  
* [CPL: Programmation en style C](016-cpl.md)  
* [SF: Fichiers sources](017-source.md)  
* [SL: La bibliothèque standard](018-stdlib.md)

Section de soutien :

* [A: Idées architecturales](019-a.md)  
* [NR: Non-règles et mythes](020-not.md)  
* [RF: Références](021-references.md)  
* [Pro: Profils](022-profile.md)  
* [GSL: Bibliothèque de support des directives](#gsl-guidelines-support-library)  
* [NL: Suggestions de nommage et d'agencement](024-naming.md)  
* [FAQ: Réponses aux questions fréquentes](025-faq.md)  
* [Annexe A: Bibliothèques](026-libraries.md)  
* [Annexe B: Modernisation du code](027-modernizing.md)  
* [Annexe C: Discussion](028-discussion.md)  
* [Annexe D: Outils de soutien](029-tools.md)  
* [Glossaire](030-glossary.md)  
* [À faire : Proto-règles non classées](031-unclassified.md)