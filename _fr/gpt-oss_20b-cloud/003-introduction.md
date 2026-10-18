# <a name="s-introduction"></a>In: Introduction

Il s'agit d'un ensemble de directives essentielles pour le C++ moderne (actuellement C++20 et C++17), prenant en compte les améliorations futures probables ainsi que les spécifications techniques ISO (TSs).  
L'objectif est d'aider les programmeurs C++ à écrire du code plus simple, plus efficace et plus maintenable.

Résumé de l'introduction :

* [In.target: Public cible](003-introduction.md#ss-readers)
* [In.aims: Objectifs](003-introduction.md#ss-aims)
* [In.not: Non-Objectifs](003-introduction.md#ss-non)
* [In.force: Application](003-introduction.md#ss-force)
* [In.struct: La structure de ce document](003-introduction.md#ss-struct)
* [In.sec: Sections principales](003-introduction.md#ss-sec)

## <a name="ss-readers"></a>In.target: Public cible

Tous les programmeurs C++. Cela inclut [les programmeurs qui pourraient envisager le C](016-cpl.md).

## <a name="ss-aims"></a>In.aims: Objectifs

Le but de ce document est d'aider les développeurs à adopter le C++ moderne (actuellement C++20 et C++17) et à obtenir un style plus uniforme à travers les bases de code.

Nous ne sommes pas naïfs en pensant que chacune de ces règles peut être appliquée efficacement à chaque base de code. Mettre à jour les anciens systèmes est difficile. Cependant, nous pensons qu'un programme qui applique une règle est moins propice aux erreurs et plus maintenable qu'un programme qui ne le fait pas. Souvent, les règles conduisent également à un développement initial plus rapide ou plus facile.

Il semble que ces règles produisent un code qui fonctionne aussi bien ou mieux que les techniques plus anciennes et plus conventionnelles ; elles visent à suivre le principe de non‑surcoût (« ce que vous n'utilisez pas, vous ne payez pas pour » ou « lorsque vous utilisez un mécanisme d'abstraction correctement, vous obtenez au moins la même performance qu'avec du code écrit manuellement en utilisant des constructions de bas niveau »).

Considérez ces règles comme des idéaux pour le nouveau code, des opportunités à exploiter lors du travail sur du code ancien, et essayez d'approcher ces idéaux autant que possible.

Rappelez‑vous :

### <a name="r0"></a>In.0: Pas de panique !

Prenez le temps de comprendre les implications d'une règle de directive sur votre programme.

Ces directives sont conçues selon le principe « sous‑ensemble d'un sur‑ensemble » ([Stroustrup05](032-bibliography.md#Stroustrup05)).  Elles ne se limitent pas simplement à définir un sous‑ensemble de C++ à utiliser (pour la fiabilité, la sécurité, la performance ou autre). Au lieu de cela, elles recommandent vivement l'utilisation de quelques simples « extensions » ([composants de bibliothèque](#gsl-guidelines-support-library) @TODO‑LINK) qui rendent l'utilisation des fonctionnalités les plus sujettes aux erreurs de C++ redondante, afin qu'elles puissent être interdites (dans notre ensemble de règles).

Les règles soulignent la sécurité de type statique et la sécurité des ressources. Pour cette raison, elles mettent en avant les possibilités de vérification de plage, d'éviter la déréférenciation de `nullptr`, d'éviter les pointeurs pendants et l'utilisation systématique des exceptions (via RAII).

En partie pour atteindre cela et en partie pour minimiser le code obscur comme source d'erreurs, les règles soulignent également la simplicité et le masquage de la complexité nécessaire derrière des interfaces bien spécifiées.

Beaucoup de règles sont prescriptives. Nous ne sommes pas à l'aise avec des règles qui disent simplement « ne faites pas cela ! » sans fournir d'alternative. Une conséquence de cela est que certaines règles ne peuvent être soutenues que par des heuristiques, plutôt que par des vérifications précises et mécaniquement vérifiables.

D'autres règles expriment des principes généraux. Pour ces règles plus générales, des règles plus détaillées et spécifiques fournissent une vérification partielle.

Ces directives concernent le cœur du C++ et son utilisation. Nous nous attendons à ce que la plupart des grandes organisations, des domaines d'application spécifiques et même des gros projets requièrent d'autres règles, voire d'autres restrictions et un soutien de bibliothèque supplémentaire. Par exemple, les programmeurs en temps réel strict ne peuvent généralement pas utiliser le tas libre (mémoire dynamique) librement et seront contraints dans leur choix de bibliothèques.

Nous encourageons le développement de telles règles plus spécifiques en tant qu'addenda à ces directives de base.

Construisez votre propre petite bibliothèque de base idéale et utilisez‑la, plutôt que de rétrograder votre niveau de programmation vers un assembleur glorifié.

Ces règles sont conçues pour permettre une adoption progressive (voir le chapitre « Moderniser le code »).

Il est particulièrement important que les règles favorisent une adoption graduelle : il est généralement impossible de convertir complètement une grande base de code d'un coup.

Ces lignes directrices ne sont pas destinées à être complètes ou exactes en toute spécificité technique. Pour la dernière parole sur les problèmes de définition de langage, y compris chaque exception aux règles générales et chaque caractéristique, voir la norme ISO C++.

Les règles ne visent pas à vous forcer à écrire dans un sous‑ensemble réduit du C++. Elles ne sont *évidenceusement* pas conçues pour définir un sous‑ensemble du type Java. Elles ne sont pas destinées à définir un langage « un vrai C++ ». Nous précisons l'expression et la performance sans compromis.

Les règles ne sont pas neutres sur le plan des valeurs. Elles visent à rendre le code plus simple et plus correct/sûr que la plupart des codes C++ existants, sans perte de performance. Elles visent à inhiber le code C++ parfaitement valide qui corrèle avec des erreurs, une complexité inutile et une mauvaise performance.

Les règles ne sont pas précises au point où une personne (ou une machine) peut les suivre sans réfléchir. Les parties d'application tentent de le faire, mais nous préférons laisser une règle ou une définition un peu vague et ouverte à l'interprétation plutôt que de spécifier quelque chose de précis et incorrect. Parfois, la précision ne vient qu'avec le temps et l'expérience. Le design n'est pas (encore) une forme de math.

Les règles ne sont pas parfaites. Une règle peut nuire en interdisant quelque chose qui est utile dans une situation donnée. Une règle peut nuire en ne prohibant pas quelque chose qui cause une erreur grave dans une situation donnée. Une règle peut nuire beaucoup en étant vague, ambiguë, non appliquable ou en permettant chaque solution à un problème. Il est impossible de satisfaire complètement le critère « ne pas faire de mal ». Notre objectif est plus ambitieux : « Faites le plus de bien pour la majorité des programmeurs » ; si vous ne vivez pas avec une règle, contestez‑la, ignorez‑la, mais ne la réduisez pas jusqu'à ce qu'elle devienne sans sens. Suggérez aussi une amélioration.

## <a name="ss-non"></a>In.not: Non-Objectifs

Les règles ne sont pas destinées à être minimales ou orthogonales. En particulier, les règles générales peuvent être simples, mais non applicables. Il est également souvent difficile de comprendre les implications d'une règle générale. Les règles plus spécialisées sont souvent plus faciles à comprendre et à appliquer, mais sans règles générales elles ne feraient qu'une longue liste de cas spéciaux. Nous proposons des règles destinées à aider les débutants ainsi que des règles visant l'utilisation experte. Certaines règles peuvent être entièrement appliquées, d'autres reposent sur des heuristiques.

Ces règles ne sont pas destinées à être lues séquentiellement comme un livre. Vous pouvez les parcourir via les liens. Cependant, leur usage principal est d'être des cibles pour des outils. Un outil cherche les violations et renvoie les liens vers les règles enfreintes. Les règles fournissent alors des raisons, des exemples de conséquences potentielles et des remèdes suggérés.

Ces lignes directrices ne sont pas destinées à être un substitut à un traitement tutoral du C++. Si vous avez besoin d'un tutoriel pour un niveau donné, consultez les [références](021-references.md).

Ce n'est pas un guide sur la façon de convertir le vieux code C++ vers un code plus moderne. Il vise à exprimer des idées pour le nouveau code de façon concrète. Cependant, voir la [section de modernisation](027-modernizing.md) pour des approches d'actualisation/mise à jour.

Il est particulièrement important que les règles favorisent une adoption graduelle : il est généralement impossible de convertir complètement une grande base de code d'un coup.

Ces lignes directrices ne sont pas destinées à être complètes ou exactes en toute spécificité technique. Pour la dernière parole sur les problèmes de définition de langage, y compris chaque exception aux règles générales et chaque caractéristique, voir la norme ISO C++.

Les règles ne visent pas à vous forcer à coder dans un sous‑ensemble arrêté du C++. Elles ne sont *évidenceusement* pas conçues pour définir un sous‑ensemble du type Java. Elles ne sont pas destinées à définir un langage « un vrai C++ ». Nous précisons l'expression et la performance sans compromis.

Les règles ne sont pas neutres sur le plan des valeurs. Elles visent à rendre le code plus simple et plus correct/sûr que la plupart des codes C++ existants, sans perte de performance. Elles visent à inhiber le code C++ parfaitement valide qui corrèle avec des erreurs, une complexité inutile et une mauvaise performance.

Les règles ne sont pas précises au point où une personne (ou une machine) peut les suivre sans réfléchir. Les parties d'application tentent de le faire, mais nous préférons laisser une règle ou une définition un peu vague et ouverte à l'interprétation plutôt que de spécifier quelque chose de précis et incorrect. Parfois, la précision ne vient qu'avec le temps et l'expérience. Le design n'est pas (encore) une forme de math.

Les règles ne sont pas parfaites. Une règle peut nuire en interdisant quelque chose qui est utile dans une situation donnée. Une règle peut nuire en ne prohibant pas quelque chose qui cause une erreur grave dans une situation donnée. Une règle peut nuire beaucoup en étant vague, ambiguë, non appliquable ou en permettant chaque solution à un problème. Il est impossible de satisfaire complètement le critère « ne pas faire de mal ». Notre objectif est plus ambitieux : « Faites le plus de bien pour la majorité des programmeurs » ; si vous ne vivez pas avec une règle, contestez‑la, ignorez‑la, mais ne la réduisez pas jusqu'à ce qu'elle devienne sans sens. Suggérez aussi une amélioration.

### <a name="ss-force"></a>In.force: Application

Les règles sans application sont difficiles à gérer pour de grandes bases de code. L'application de toutes les règles n'est possible qu'avec un petit ensemble de règles faibles ou au sein d'une communauté d'utilisateurs spécifique.

- Mais nous voulons beaucoup de règles, et nous voulons des règles utilisables par tout le monde.
- Mais les gens ont des besoins différents.
- Mais les gens n'aiment pas lire beaucoup de règles.
- Mais les gens ne peuvent pas retenir beaucoup de règles.

Ainsi, nous avons besoin de sous‑ensembles pour répondre à une variété de besoins.

- Mais le sous‑ensemble arbitraire conduit au chaos.

Nous voulons des directives qui aident beaucoup de gens, rendent le code plus uniforme, et encouragent fortement les gens à moderniser leur code. Nous voulons encourager les meilleures pratiques, plutôt que de tout laisser aux choix individuels et aux pressions de gestion. L'idéal est d'utiliser toutes les règles ; cela apporte les plus grands avantages.

Cela conduit à plusieurs dilemmes. Nous essayons de les résoudre à l'aide d'outils. Chaque règle possède une section **Enforcement** présentant des idées d'application. L'application peut se faire par révision de code, analyse statique, compilateur ou vérifications à l'exécution. Dans la mesure du possible, nous privilégions la vérification « mécanique » (les humains sont lents, inexactes et s'ennuient facilement) et la vérification statique. Les vérifications à l'exécution ne sont suggérées que rarement lorsqu'aucune alternative n'existe ; nous ne voulons pas introduire de « distributed bloat ».

Où c'est approprié, nous étiquetons une règle (dans les sections **Enforcement**) avec le nom de groupes de règles liées (appelés « profils »). Une règle peut faire partie de plusieurs profils, ou pas du tout. Pour commencer, nous avons quelques profils correspondant à des besoins courants (désirs, idéaux) :

- **type** : Pas de violations de types (retransformation d'un `T` en un `U` via cast, union ou varargs)
- **bounds** : Pas de violations de bornes (accéder au-delà de la portée d'un tableau)
- **lifetime** : Pas de fuites (ne pas `delete` ou multiples `delete`) et pas d'accès à des objets invalides (déréférencer `nullptr`, utiliser une référence pendante).

Les profils sont destinés à être utilisés par des outils, mais servent aussi d'aide pour le lecteur humain.  
Nous ne limitons pas nos commentaires dans les sections **Enforcement** aux éléments que nous savons faire appliquer ; certains commentaires sont de simples souhaits pouvant inspirer un constructeur d'outil.

Les outils qui implémentent ces règles doivent respecter la syntaxe suivante pour supprimer explicitement une règle :

    [[gsl::suppress("tag")]]
et optionnellement avec un message (conformément à la syntaxe standard des attributs C++11) :

    [[gsl::suppress("tag", justification: "message")]]
où

* `"tag"` est un littéral de chaîne avec le nom d'ancre de l'élément où apparaît la règle d'Enforcement (par ex. pour [C.134](007-class.md#rh-public) il s'agit de « rh‑public »), le nom d'un groupe de profils (« type », « bounds » ou « lifetime »),
* `"message"` est un littéral de chaîne

## <a name="ss-struct"></a>In.struct: La structure de ce document

Chaque règle (directive, suggestion) peut comporter plusieurs parties :

* la règle elle‑même – par exemple **no naked `new`**
* un numéro de référence de règle – par exemple **C.7** (la 7e règle liée aux classes).  
  Étant donné que les sections majeures ne sont pas nativement ordonnées, nous utilisons des lettres comme première partie d'un numéro de référence de règle.  
  Nous laissons des lacunes dans la numérotation afin de minimiser les « disruption » lors de l'ajout ou de la suppression de règles.
* **Raisons** (justifications) – car les programmeurs trouvent difficile de suivre des règles qu'ils ne comprennent pas.  
* **Exemples** – car les règles sont difficiles à comprendre dans l'abstraction ; peuvent être positives ou négatives.  
* **Alternatives** – pour les règles « ne faites pas cela ».  
* **Exceptions** – nous préférons les règles générales simples. Cependant, de nombreuses règles s'appliquent largement, mais pas universellement, donc les exceptions doivent être énumérées.  
* **Application** – idées sur la façon dont la règle pourrait être vérifiée « mécaniquement ».  
* **Voir aussi** – références aux règles connexes et/ou à une discussion plus poussée (dans ce document ou ailleurs).  
* **Notes** – quelque chose qui doit être dit et qui ne rentre pas dans d'autres catégories.  
* **Discussion** – références à des raisonnements plus approfondis et/ou à des exemples placés hors de la liste principale des règles.

Certains règles sont difficiles à vérifier mécaniquement, mais elles répondent à toutes les exigences minimales qu'un programmeur expert peut repérer sans trop de difficulté. Nous espérons que les outils « mécaniques » s'amélioreront avec le temps afin d'approcher ce qu'un tel programmeur expert remarque. Nous supposons également qu'au fil du temps les règles seront affinées pour être plus précises et vérifiables.

Une règle a pour but d'être simple plutôt que soigneusement formulée pour mentionner chaque alternative et chaque cas spécial. De telles informations se trouvent dans les paragraphes **Alternatives** et les sections [Discussion](028-discussion.md). Si vous ne comprenez pas une règle ou n'êtes pas d'accord, veuillez consulter sa **Discussion**. Si vous pensez qu'une discussion est manquante ou incomplète, ouvrez un [Issue](https://github.com/isocpp/CppCoreGuidelines/issues) expliquant vos préoccupations et éventuellement un PR correspondant.

Les exemples sont écrits pour illustrer les règles. Les exemples ne visent pas la qualité de production ni à couvrir toutes les dimensions descriptives. Par exemple, beaucoup d'exemples sont techniques de langage et utilisent des noms comme `f`, `base` et `x`. Nous essayons de nous assurer que les « bons » exemples suivent les Directives Core. Les commentaires illustrent souvent les règles où ils seraient inutiles et/ou distrayants dans « le code réel ». Nous supposons la connaissance de la bibliothèque standard. Par exemple, nous utilisons plain `vector` plutôt que `std::vector`.

Ce n'est pas un manuel de langage. Il est destiné à être utile, plutôt qu'un guide complet, 100 % précis sur les détails techniques, ou un guide de code existant. Les sources d'information recommandées se trouvent dans les [références](021-references.md).

## <a name="ss-sec"></a>In.sec: Sections principales

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
* [Con: Constantes et immuabilité](014-const.md)
* [T: Templates et programmation générique](015-templates.md)
* [CPL: Programmation de style C](016-cpl.md)
* [SF: Fichiers source](017-source.md)
* [SL: La bibliothèque standard](#sl-the-standard-library) @TODO‑LINK
* [Sections de soutien:
    * [A: Idées architecturales](019-a.md)
    * [NR: Non‑règles et mythes](020-not.md)
    * [RF: Références](021-references.md)
    * [Pro: Profils](022-profile.md)
    * [GSL: Bibliothèque de soutien aux directives](#gsl-guidelines-support-library) @TODO‑LINK
    * [NL: Suggestions de nommage et de mise en page](024-naming.md)
    * [FAQ: Réponses aux questions fréquentes](025-faq.md)
    * [Appendix A: Bibliothèques](026-libraries.md)
    * [Appendix B: Moderniser le code](027-modernizing.md)
    * [Appendix C: Discussion](028-discussion.md)
    * [Appendix D: Outils de support](029-tools.md)
    * [Glossaire](030-glossary.md)
    * [To-do: Protocole non classifié](031-unclassified.md)
]

Ces sections ne sont pas orthogonales.

Chaque section (p. ex. « P » pour « Philosophie ») et chaque sous‑section (p. ex. « C.hier » pour « Arborescence de classes (OOP) ») possèdent une abréviation afin de faciliter la recherche et la référence.  
Les abréviations des sections principales sont également utilisées dans les numéros de règles (p. ex. « C.11 » pour « Faire des types concrets réguliers »).