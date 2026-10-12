# <a name="main"></a>Lignes directrices essentielles de C++

14 juin 2026

Éditeurs :

* [Bjarne Stroustrup](https://www.stroustrup.com)
* [Herb Sutter](https://herbsutter.com/)

Ceci est un document vivant, en amélioration continue.
S'il s'était agi d'un projet open source (code), il s'agirait de la version 0.8.
La copie, l'utilisation, la modification et la création d'œuvres dérivées à partir de ce projet sont régies par une licence de type MIT.
Contribuer à ce projet implique d'accepter une licence de contributeur. Consultez le fichier [LICENSE](https://github.com/isocpp/CppCoreGuidelines/blob/master/LICENSE) joint pour plus de détails.
Nous rendons ce projet disponible aux « utilisateurs bienveillants » pour l'utiliser, le copier, le modifier et en créer des dérivations, en espérant recevoir des retours constructifs.

Les commentaires et les suggestions d'amélioration sont les bienvenus.
Nous prévoyons de modifier et d'étendre ce document à mesure que notre compréhension progresse et que le langage ainsi que l'ensemble des bibliothèques disponibles évoluent.
Lorsque vous formulez un commentaire, prenez note de [l'introduction](003-introduction.md) qui présente nos objectifs et notre approche générale.
La liste des contributeurs est disponible [ici](021-references.md#ss-ack).

Problèmes :

* Les ensembles de règles n'ont pas été intégralement vérifiés sous l'angle de l'exhaustivité, de la cohérence ou de l'application pratique.
* Des triples points d'interrogation (???) signalent des informations connues manquantes.
* Mettre à jour les sections de références ; de nombreuses sources antérieures à C++11 sont trop anciennes.
* Pour une liste des tâches à jour, voir : [Tâches : Proto-règles non classées](031-unclassified.md).

Vous pouvez consulter [une explication du périmètre et de la structure de ce guide](002-abstract.md), ou vous plonger directement :

* [In : Introduction](003-introduction.md)
* [P : Philosophie](004-philosophy.md)
* [I : Interfaces](005-interfaces.md)
* [F : Fonctions](006-functions.md)
* [C : Classes et hiérarchies de classes](007-class.md)
* [Enum : Énumérations](008-enum.md)
* [R : Gestion des ressources](009-resource.md)
* [ES : Expressions et déclarations](010-expr.md)
* [Per : Performance](011-performance.md)
* [CP : Concurrency et parallélisme](012-concurrency.md)
* [E : Gestion des erreurs](013-errors.md)
* [Con : Constantes et immuabilité](014-const.md)
* [T : Modèles et programmation générique](015-templates.md)
* [CPL : Programmation de style C](016-cpl.md)
* [SF : Fichiers sources](017-source.md)
* [SL : La bibliothèque standard](#sl-the-standard-library) <!-- @TODO-LINK : ancre `sl-the-standard-library` introuvable dans ce document -->

Sections de support :

* [A : Idées architecturales](019-a.md)
* [NR : Non-règles et mythes](020-not.md)
* [RF : Références](021-references.md)
* [Pro : Profils](022-profile.md)
* [GSL : Bibliothèque de support des lignes directrices](023-gsl.md)
* [NL : Suggestions de nommage et de mise en page](024-naming.md)
* [FAQ : Réponses aux questions fréquemment posées](025-faq.md)
* [Annexe A : Bibliothèques](026-libraries.md)
* [Annexe B : Modernisation du code](027-modernizing.md)
* [Annexe C : Discussion](028-discussion.md)
* [Annexe D : Outils de support](029-tools.md)
* [Glossaire](030-glossary.md)
* [Tâches : Proto-règles non classées](031-unclassified.md)

Vous pouvez consulter des exemples de règles pour des fonctionnalités spécifiques du langage :

* affectation :
[type courant](007-class.md#rc-regular) --
[préférer l'initialisation](007-class.md#rc-initialize) --
[copie](007-class.md#rc-copy-semantic) --
[déplacement](007-class.md#rc-move-semantic) --
[autres opérations](007-class.md#rc-matched) --
[par défaut](007-class.md007-class.md#rc-eqdefault)
* `class` :
[données](007-class.md#rc-org) --
[invariante](007-class.md#rc-struct) --
[membres](007-class.md#rc-member) --
[fonctions d'aide](007-class.md#rc-helper) --
[types concrets](007-class.md018-stdlib.md#ss-concrete) --
[constructeurs, opérateur `=`, destructeurs](007-class.md) --
[hiérarchie](007-class.md#ss-hier) --
[opérateurs](007-class.md#ss-overload)
* `concept` :
[règles](015-templates.md018-stdlib.md#ss-concepts) --
[dans la programmation générique](015-templates.md#rt-raise) --
[arguments de modèle](015-templates.md#rt-concepts) --
[semantique](015-templates.md#rt-low)
* constructeur :
[invariante](007-class.md#rc-struct) --
[établir l'invariante](007-class.md#rc-ctor) --
[`throw`](007-class.md#rc-throw) --
[par défaut](007-class.md007-class.md#rc-default0) --
[n'est pas toujours nécessaire](007-class.md#rc-default) --
[`explicit`](007-class.md#rc-explicit) --
[délégant](007-class.md#rc-delegating) --
[`virtual`](007-class.md007-class.md#rc-ctor-virtual)
* `class` dérivée :
[quand l'utiliser](007-class.md#rh-domain) --
[comme interface](007-class.md#rh-abstract) --
[destructeurs](007-class.md#rh-dtor) --
[copie](007-class.md#rh-copy) --
[accesseurs et modificateurs](007-class.md#rh-get) --
[héritage multiple](007-class.md#rh-mi-interface) --
[surchargement](007-class.md#rh-using) --
[tranchage (slicing)](007-class.md#rc-copy-virtual) --
[`dynamic_cast`](007-class.md#rh-dynamic_cast)
* destructeur :
[et constructeurs](007-class.md#rc-matched) --
[quand est-il nécessaire ?](007-class.md#rc-dtor) --
[ne doit pas échouer](007-class.md007-class.md#rc-dtor-fail)
* exception :
[erreurs](013-errors.md) --
[`throw`](013-errors.md#re-throw) --
[réservé aux erreurs](013-errors.md#re-errors) --
[`noexcept`](013-errors.md#re-noexcept) --
[minimiser `try`](013-errors.md#re-catch) --
[que faire sans exceptions ?](013-errors.md013-errors.md#re-no-throw-codes)
* `for` :
[range-for et for](010-expr.md#res-for-range) --
[for et while](010-expr.md#res-for-while) --
[initialisation dans la boucle](010-expr.md#res-for-init) --
[corps vide](010-expr.md#res-empty) --
[variable de boucle](010-expr.md#res-loop-counter) --
[type de la variable de boucle ???](#res-???) <!-- @TODO-LINK : ancre `res-???` introuvable dans ce document -->
* fonction :
[nommage](006-functions.md#rf-package) --
[une seule opération](006-functions.md#rf-logical) --
[sans throw](006-functions.md#rf-noexcept) --
[arguments](006-functions.md#rf-smart) --
[passage d'arguments](006-functions.md#rf-conventional) --
[valeurs de retour multiples](006-functions.md006-functions.md#rf-out-multi) --
[pointeurs](006-functions.md#rf-return-ptr) --
[lambda](006-functions.md#rf-capture-vs-overload)
* `inline` :
[petites fonctions](006-functions.md006-functions.md#rf-inline) --
[dans les en-têtes](017-source.md#rs-inline)
* initialisation :
[toujours](010-expr.md#res-always) --
[préférer `{}`](010-expr.md#res-list) --
[lambda](010-expr.md#res-lambda-init) --
[initialisateurs de membres par défaut](007-class.md#rc-in-class-initializer) --
[membres de classe](007-class.md#rc-initialize) --
[fonctions fabriques](007-class.md#rc-factory)
* expression lambda :
[quand l'utiliser](007-class.md#ss-lambdas)
* opérateur :
[conventionnel](007-class.md#ro-conventional) --
[éviter les opérateurs de conversion](007-class.md#ro-conversion) --
[et lambda](007-class.md#ro-lambda)
* `public`, `private` et `protected` :
[masquage d'information](007-class.md#rc-private) --
[cohérence](007-class.md#rh-public) --
[`protected`](007-class.md#rh-protected)
* `static_assert` :
[vérification à la compilation](004-philosophy.md#rp-compile-time) --
[et concepts](015-templates.md#rt-check-class)
* `struct` :
[pour organiser des données](007-class.md#rc-org) --
[l'utiliser s'il n'y a pas d'invariante](007-class.md#rc-struct) --
[pas de membres privés](007-class.md#rc-class)
* `template` :
[abstraction](015-templates.md#rt-raise) --
[conteneurs](015-templates.md#rt-cont) --
[concepts](015-templates.md#rt-concepts)
* `unsigned` :
[et signed](010-expr.md#res-mix) --
[manipulation de bits](010-expr.md#res-unsigned)
* `virtual` :
[interfaces](005-interfaces.md#ri-abstract) --
[non `virtual`](007-class.md#rc-concrete) --
[destructeur](007-class.md007-class.md#rc-dtor-virtual) --
[ne jamais échouer](007-class.md007-class.md#rc-dtor-fail)

Vous pouvez consulter les concepts de conception utilisés pour formuler les règles :

* assertion : ???
* erreur : ???
* exception : garantie d'exception (???)
* échec : ???
* invariante : ???
* fuite : ???
* bibliothèque : ???
* précondition : ???
* postcondition : ???
* ressource : ???

---

**Notes de traduction :**
- Deux ancreurs locaux n'ont pas été trouvés dans ce document et ont été signalés avec `@TODO-LINK` :
  - `#sl-the-standard-library` (lien vers « SL : La bibliothèque standard »)
  - `#res-???` (lien vers « type de la variable de boucle ??? »)
- Toutes les autres références (`007-class.md#rc-regular`, etc.) pointent vers des fichiers Markdown externes du projet et ont été conservées telles quelles.