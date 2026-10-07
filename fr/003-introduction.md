# <a name="s-introduction"></a>In: Introduction

Ceci est un ensemble de directives fondamentales pour le C++ moderne (actuellement C++20 et C++17) prenant en compte les améliorations futures probables et les Spécifications Techniques (TS) de l'ISO.
L'objectif est d'aider les programmeurs C++ à écrire un code plus simple, plus efficace et plus facile à maintenir.

Résumé de l'introduction:

* [In.target: Public cible](#ss-readers)
* [In.aims: Objectifs](#ss-aims)
* [In.not: Non-objectifs](#ss-non)
* [In.force: Application](#ss-force)
* [In.struct: La structure de ce document](#ss-struct)
* [In.sec: Sections principales](#ss-sec)

## <a name="ss-readers"></a>In.target: Public cible

Tous les programmeurs C++. Cela inclut [les programmeurs qui pourraient envisager le C](#s-cpl).

## <a name="ss-aims"></a>In.aims: Objectifs

Le but de ce document est d'aider les développeurs à adopter le C++ moderne (actuellement C++20 et C++17) et à réaliser un style plus uniforme entre les bases de code.

Nous ne souffrons pas de l'illusion que chacune de ces règles peut être efficacement appliquée à chaque base de code. La mise à niveau des anciens systèmes est difficile. Cependant, nous croyons qu'un programme qui respecte une règle est moins[...]
Autant que nous puissions en juger, ces règles conduisent à un code qui fonctionne aussi bien ou mieux que les techniques plus anciennes et conventionnelles; elles sont destinées à suivre le principe du zéro surcharge ("ce que vous n'utilisez pas, vous[...]
Considérez ces règles comme des idéaux pour le nouveau code, des opportunités à exploiter lors du travail sur du code ancien, et essayez de vous rapprocher de ces idéaux aussi étroitement que possible.
Souvenez-vous:

### <a name="r0"></a>In.0: Ne paniquez pas!

Prenez le temps de comprendre les implications d'une règle de directive sur votre programme.

Ces directives sont conçues selon le principe du "sous-ensemble de sur-ensemble" ([Stroustrup05](#Stroustrup05)).
Elles ne définissent pas simplement un sous-ensemble de C++ à utiliser (pour la fiabilité, la sécurité, les performances ou autre).
Au lieu de cela, elles recommandent fortement l'utilisation de quelques simples "extensions" ([composants de bibliothèque](#gsl-guidelines-support-library))
qui rendent l'utilisation des fonctionnalités les plus sujettes aux erreurs de C++ redondante, afin qu'elles puissent être interdites (dans notre ensemble de règles).

Les règles mettent l'accent sur la sécurité de type statique et la sécurité des ressources.
Pour cette raison, elles soulignent les possibilités de vérification des plages, d'éviter la déréférence de `nullptr`, d'éviter les pointeurs pendants, et l'utilisation systématique des exceptions (via RAII).
En partie pour réaliser cela et en partie pour minimiser le code obscur comme source d'erreurs, les règles mettent également l'accent sur la simplicité et la dissimulation de la complexité nécessaire derrière des interfaces bien spécifiées.

Beaucoup de règles sont prescriptives.
Nous sommes mal à l'aise avec les règles qui déclarent simplement "ne fais pas ça!" sans offrir d'alternative.
Une conséquence de cela est que certaines règles ne peuvent être soutenues que par des heuristiques, plutôt que par des vérifications précises et mécaniquement vérifiables.
D'autres règles articulent des principes généraux. Pour ces règles plus générales, des règles plus détaillées et spécifiques fournissent une vérification partielle.

Ces directives abordent le cœur du C++ et son utilisation.
Nous nous attendons à ce que la plupart des grandes organisations, domaines d'application spécifiques, et même les grands projets aient besoin de règles supplémentaires, possiblement des restrictions supplémentaires, et un soutien supplémentaire de la part des bibliothèques.
Par exemple, les programmeurs du temps réel dur ne peuvent généralement pas utiliser librement le tas libre (mémoire dynamique) et seront limités dans leur choix de bibliothèques.
Nous encourageons le développement de telles règles plus spécifiques comme des ajouts à ces directives fondamentales.
Construisez votre bibliothèque de fondation idéale et petite et utilisez-la, plutôt que de baisser votre niveau de programmation en assemblage glorifié.

Les règles sont conçues pour permettre [l'adoption progressive](#s-modernizing).

Certaines règles visent à augmenter diverses formes de sécurité tandis que d'autres visent à réduire la probabilité d'accidents, beaucoup font les deux.
Les directives visant à prévenir les accidents interdisent souvent du C++ tout à fait valide.
Cependant, lorsqu'il y a deux façons d'exprimer une idée et qu'une s'avère être une source courante d'erreurs et l'autre non, nous essayons de guider les programmeurs vers cette dernière.

## <a name="ss-non"></a>In.not: Non-objectifs

Les règles ne sont pas destinées à être minimales ou orthogonales.
En particulier, les règles générales peuvent être simples, mais inapplicables.
De plus, il est souvent difficile de comprendre les implications d'une règle générale.
Les règles plus spécialisées sont souvent plus faciles à comprendre et à appliquer, mais sans règles générales, elles ne seraient qu'une longue liste de cas particuliers.
Nous fournissons des règles destinées à aider les novices ainsi que des règles soutenant l'utilisation par les experts.
Certaines règles peuvent être complètement appliquées, mais d'autres sont basées sur des heuristiques.

Ces règles ne sont pas destinées à être lues en série, comme un livre.
Vous pouvez les parcourir en utilisant les liens.
Cependant, leur utilisation principale prévue est d'être des cibles pour les outils.
C'est-à-dire qu'un outil recherche les violations et l'outil retourne les liens vers les règles violées.
Les règles fournissent ensuite des raisons, des exemples des conséquences potentielles de la violation, et des remèdes suggérés.

Ces directives ne sont pas destinées à être un substitut à un traitement tutoriel du C++.
Si vous avez besoin d'un tutoriel pour un certain niveau d'expérience, voir [les références](#s-references).

Ceci n'est pas un guide sur la façon de convertir l'ancien code C++ en code plus moderne.
Il est destiné à articuler des idées pour le nouveau code de manière concrète.
Cependant, voir [la section sur la modernisation](#s-modernizing) pour certaines approches possibles à la modernisation/rajeunissement/mise à niveau.
Important, les règles soutiennent l'adoption progressive: il est généralement infaisable de convertir complètement une grande base de code en une seule fois.

Ces directives ne sont pas destinées à être complètes ou exactes dans chaque détail technique du langage.
Pour la dernière parole sur les questions de définition du langage, y compris chaque exception aux règles générales et chaque fonctionnalité, voir la norme ISO C++.

Les règles ne sont pas destinées à vous forcer à écrire dans un sous-ensemble appauvri du C++.
Elles ne sont *absolument pas* destinées à définir un sous-ensemble de C++ de type Java.
Elles ne sont pas destinées à définir un seul langage C++ "unique et vrai".
Nous valorisons l'expressivité et les performances sans compromis.

Les règles ne sont pas neutres sur le plan des valeurs.
Elles sont destinées à rendre le code plus simple et plus correct/plus sûr que la plupart du code C++ existant, sans perte de performance.
Elles sont destinées à inhiber le code C++ tout à fait valide qui se corrèle avec des erreurs, une complexité factice, et des performances médiocres.

Les règles ne sont pas précises au point qu'une personne (ou une machine) puisse les suivre sans réfléchir.
Les parties application essaient de l'être, mais nous préférerions laisser une règle ou une définition un peu vague
et ouverte à l'interprétation plutôt que de préciser quelque chose précisément et incorrectement.
Parfois, la précision ne vient qu'avec le temps et l'expérience.
La conception n'est pas (encore) une forme de mathématiques.

Les règles ne sont pas parfaites.
Une règle peut faire du mal en interdisant quelque chose qui est utile dans une situation donnée.
Une règle peut faire du mal en échouant à interdire quelque chose qui permet une erreur grave dans une situation donnée.
Une règle peut faire beaucoup de mal en étant vague, ambiguë, inapplicable, ou en permettant à chaque solution à un problème.
Il est impossible de satisfaire complètement les critères du "ne faire aucun mal".
Au lieu de cela, notre objectif est moins ambitieux: "Faire le plus de bien pour la plupart des programmeurs";
si vous ne pouvez pas vivre avec une règle, objectez-y, ignorez-la, mais ne la diluez pas jusqu'à ce qu'elle devienne dénuée de sens.
De plus, suggérez une amélioration.

## <a name="ss-force"></a>In.force: Application

Les règles sans application sont ingérables pour les grandes bases de code.
L'application de toutes les règles n'est possible que pour un petit ensemble de règles faibles ou pour une communauté d'utilisateurs spécifique.

* Mais nous voulons beaucoup de règles, et nous voulons des règles que tout le monde puisse utiliser.
* Mais les différentes personnes ont des besoins différents.
* Mais les gens n'aiment pas lire beaucoup de règles.
* Mais les gens ne peuvent pas mémoriser beaucoup de règles.

Donc, nous avons besoin d'un sous-ensemble pour répondre à une variété de besoins.

* Mais le sous-ensemble arbitraire mène au chaos.

Nous voulons des directives qui aident beaucoup de gens, rendent le code plus uniforme, et encouragent fortement les gens à moderniser leur code.
Nous voulons encourager les meilleures pratiques, plutôt que de laisser tout aux choix individuels et aux pressions de gestion.
L'idéal est d'utiliser toutes les règles; cela donne les plus grands avantages.

Cela s'ajoute à un bon nombre de dilemmes.
Nous essayons de les résoudre en utilisant des outils.
Chaque règle a une section **Application** listant les idées pour l'application.
L'application peut se faire par examen de code, par analyse statique, par compilateur, ou par vérifications à l'exécution.
Autant que possible, nous préférons la vérification "mécanique" (les humains sont lents, imprécis, et s'ennuient facilement) et la vérification statique.
Les vérifications à l'exécution ne sont suggérées que rarement lorsqu'aucune alternative n'existe; nous ne voulons pas introduire de "surcharge distribuée".
Le cas échéant, nous étiquetons une règle (dans les sections **Application**) avec le nom de groupes de règles associées (appelées "profils").
Une règle peut faire partie de plusieurs profils, ou aucun.
Pour commencer, nous avons quelques profils correspondant à des besoins communs (désirs, idéaux):

* **type**: Pas de violations de type (réinterprétation d'un `T` comme un `U` par des casts, des unions, ou des varargs)
* **bounds**: Pas de violations de limites (accès au-delà de la plage d'un tableau)
* **lifetime**: Pas de fuites (échouer à `delete` ou `delete` multiple) et pas d'accès à des objets invalides (déréférence de `nullptr`, utilisation d'une référence pendante).

Les profils sont destinés à être utilisés par les outils, mais servent également d'aide au lecteur humain.
Nous ne limitons pas notre commentaire dans les sections **Application** aux choses que nous savons comment appliquer; certains commentaires sont de simples souhaits qui pourraient inspirer un créateur d'outils.

Les outils qui implémentent ces règles doivent respecter la syntaxe suivante pour supprimer explicitement une règle:

    [[gsl::suppress("tag")]]

et éventuellement avec un message (en suivant la syntaxe habituelle de l'attribut standard C++11):

    [[gsl::suppress("tag", justification: "message")]]

où

* `"tag"` est un littéral de chaîne avec le nom d'ancre de l'élément où la règle d'application apparaît (p. ex., pour [C.134](#rh-public) c'est "rh-public"), le
nom d'un groupe de profil de règles ("type", "bounds", ou "lifetime"),
ou une règle spécifique dans un profil ([type.4](#pro-type-cstylecast), ou [bounds.2](#pro-bounds-arrayindex)). Tout texte qui n'est pas l'un de ceux-ci doit être rejeté.

* `"message"` est un littéral de chaîne

## <a name="ss-struct"></a>In.struct: La structure de ce document

Chaque règle (directive, suggestion) peut avoir plusieurs parties:

* La règle elle-même -- p. ex., **pas de `new` nu**
* Un numéro de référence de règle -- p. ex., **C.7** (la 7ème règle liée aux classes).
  Puisque les sections principales ne sont pas intrinsèquement ordonnées, nous utilisons des lettres comme première partie d'une référence de règle "numéro".
  Nous laissons des lacunes dans la numérotation pour minimiser la "perturbation" lorsque nous ajoutons ou supprimons des règles.
* **Raisons** (justifications) -- parce que les programmeurs ont du mal à suivre les règles qu'ils ne comprennent pas
* **Exemples** -- parce que les règles sont difficiles à comprendre de façon abstraite; peuvent être positifs ou négatifs
* **Alternatives** -- pour les règles "ne fais pas ça"
* **Exceptions** -- nous préférons les règles générales simples. Cependant, beaucoup de règles s'appliquent largement, mais pas universellement, donc les exceptions doivent être listées
* **Application** -- idées sur la façon dont la règle pourrait être vérifiée "mécaniquement"
* **Voir aussi** -- références à des règles connexes et/ou à d'autres discussions (dans ce document ou ailleurs)
* **Notes** (commentaires) -- quelque chose qui doit être dit et qui ne correspond pas aux autres classifications
* **Discussion** -- références à des justifications plus étendues et/ou des exemples placés en dehors des listes principales de règles

Certaines règles sont difficiles à vérifier mécaniquement, mais elles répondent toutes au critère minimal selon lequel un programmeur expert peut repérer de nombreuses violations sans trop de difficultés.
Nous espérons que les outils "mécaniques" s'amélioreront avec le temps pour se rapprocher de ce qu'un programmeur expert remarque.
De plus, nous supposons que les règles seront affinées au fil du temps pour les rendre plus précises et vérifiables.

Une règle vise à être simple, plutôt que soigneusement formulée pour mentionner chaque alternative et cas particulier.
Ces informations se trouvent dans les paragraphes **Alternatives** et les sections [Discussion](#s-discussion).
Si vous ne comprenez pas une règle ou êtes en désaccord avec elle, veuillez visiter sa **Discussion**.
Si vous estimez qu'une discussion est manquante ou incomplète, entrez un [Issue](https://github.com/isocpp/CppCoreGuidelines/issues)
expliquant vos préoccupations et possiblement une RP correspondante.

Les exemples sont écrits pour illustrer les règles.

* Les exemples ne sont pas destinés à être de qualité production ou à couvrir toutes les dimensions tutorielles.
Par exemple, beaucoup d'exemples sont techniques du langage et utilisent des noms comme `f`, `base`, et `x`.
* Nous essayons de nous assurer que les "bons" exemples suivent les Directives Fondamentales du C++.
* Les commentaires illustrent souvent les règles où ils seraient inutiles et/ou gênants dans le "code réel".
* Nous supposons une connaissance de la bibliothèque standard. Par exemple, nous utilisons `vector` simple plutôt que `std::vector`.

Ceci n'est pas un manuel du langage.
Il est destiné à être utile, plutôt que complet, totalement exact sur les détails techniques, ou un guide du code existant.
Les sources d'information recommandées peuvent être trouvées dans [les références](#s-references).

## <a name="ss-sec"></a>In.sec: Sections principales

* [In: Introduction](#s-introduction)
* [P: Philosophie](#s-philosophy)
* [I: Interfaces](#s-interfaces)
* [F: Fonctions](#s-functions)
* [C: Classes et hiérarchies de classes](#s-class)
* [Enum: Énumérations](#s-enum)
* [R: Gestion des ressources](#s-resource)
* [ES: Expressions et déclarations](#s-expr)
* [Per: Performance](#s-performance)
* [CP: Concurrence et parallélisme](#s-concurrency)
* [E: Gestion des erreurs](#s-errors)
* [Con: Constantes et immutabilité](#s-const)
* [T: Modèles et programmation générique](#s-templates)
* [CPL: Programmation de style C](#s-cpl)
* [SF: Fichiers source](#s-source)
* [SL: La bibliothèque standard](#sl-the-standard-library)

Sections de soutien:

* [A: Idées architecturales](#s-a)
* [NR: Non-règles et mythes](#s-not)
* [RF: Références](#s-references)
* [Pro: Profils](#s-profile)
* [GSL: Bibliothèque de support des directives](#gsl-guidelines-support-library)
* [NL: Suggestions de nommage et de disposition](#s-naming)
* [FAQ: Réponses aux questions fréquemment posées](#s-faq)
* [Appendice A: Bibliothèques](#s-libraries)
* [Appendice B: Modernisation du code](#s-modernizing)
* [Appendice C: Discussion](#s-discussion)
* [Appendice D: Outils de soutien](#s-tools)
* [Glossaire](#s-glossary)
* [À faire: Protoègles non classifiées](#s-unclassified)

Ces sections ne sont pas orthogonales.

Chaque section (p. ex., "P" pour "Philosophie") et chaque sous-section (p. ex., "C.hier" pour "Hiérarchies de classes (POO)") ont une abréviation pour faciliter la recherche et la référence.
Les abréviations de section principale sont également utilisées dans les numéros de règle (p. ex., "C.11" pour "Rendre les types concrets réguliers").
