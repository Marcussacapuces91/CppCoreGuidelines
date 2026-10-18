<a name="main"></a>Principes guidants C++
14 juin 2026

Éditeurs :

* [Bjarne Stroustrup](https://www.stroustrup.com)
* [Herb Sutter](https://herbsutter.com/)

Ceci est un document vivant en amélioration continue.
S'il s'agissait d'un projet open source (code), ce serait la version 0.8.
La copie, l'utilisation, la modification et la création d'œuvres dérivées à partir de ce projet sont autorisées sous licence de style MIT.
Contribuer à ce projet nécessite d'accepter une licence de contributeur. Voir le fichier [LICENSE](https://github.com/isocpp/CppCoreGuidelines/blob/master/LICENSE) pour plus de détails.
Nous rendons ce projet disponible aux "utilisateurs amicaux" pour l'utiliser, le copier, le modifier et en dériver, en espérant des contributions constructives.

Les commentaires et suggestions d'amélioration sont les bienvenus.
Nous prévoyons de modifier et d'étendre ce document à mesure que notre compréhension s'améliore et que le langage et les bibliothèques disponibles évoluent.
Lorsque vous laissez un commentaire, veuillez noter l'[Introduction](003-introduction.md) qui décrit nos objectifs et notre approche générale.
La liste des contributeurs est [ici](021-references.md#ss-ack).

Problèmes :

* Les ensembles de règles n'ont pas été entièrement vérifiés pour exhaustivité, cohérence ou applicabilité.
* Les points d'interrogation triples (???) indiquent des informations manquantes connues.
* Mettre à jour les sections de référence ; de nombreuses sources antérieures à C++11 sont trop anciennes.
* Pour une liste de tâches plus ou moins à jour, consultez : [À faire : proto-rules non classés](031-unclassified.md).

Vous pouvez [lire une explication de la portée et de la structure de ce guide](002-abstract.md) ou passer directement à l'essentiel :

* [In : Introduction](003-introduction.md)
* [P : Philosophie](004-philosophy.md)
* [I : Interfaces](005-interfaces.md)
* [F : Fonctions](006-functions.md)
* [C : Classes et hiérarchies de classes](007-class.md)
* [Enum : Énumérations](008-enum.md)
* [R : Gestion des ressources](009-resource.md)
* [ES : Expressions et déclarations](010-expr.md)
* [Per : Performance](011-performance.md)
* [CP : Concurrence et parallélisme](012-concurrency.md)
* [E : Gestion des erreurs](013-errors.md)
* [Con : Constantes et immutabilité](014-const.md)
* [T : Modèles et programmation générique](015-templates.md)
* [CPL : Programmation style C](016-cpl.md)
* [SF : Fichiers sources](017-source.md)
* [SL : La Bibliothèque Standard](#sl-the-standard-library)

Sections de soutien :

* [A : Idées architecturales](019-a.md)
* [NR : Non-règles et mythes](020-not.md)
* [RF : Références](021-references.md)
* [Pro : Profils](022-profile.md)
* [GSL : Bibliothèque de support de directives](023-gsl.md)
* [NL : Suggestions de nommage et de mise en page](024-naming.md)
* [FAQ : Réponses aux questions fréquemment posées](025-faq.md)
* [Annexe A : Bibliothèques](026-libraries.md)
* [Annexe B : Modernisation du code](027-modernizing.md)
* [Annexe C : Discussion](028-discussion.md)
* [Annexe D : Outils de support](029-tools.md)
* [Glossaire](030-glossary.md)
* [À faire : proto-rules non classés](031-unclassified.md)

Vous pouvez prélever des règles pour des fonctionnalités spécifiques du langage :

* affectation:
[types réguliers](007-class.md#rc-regular) --
[préférer l'initialisation](007-class.md#rc-initialize) --
[copier](007-class.md#rc-copy-semantic) --
[déplacer](007-class.md#rc-move-semantic) --
[autres opérations](007-class.md#rc-matched) --
[par défaut](007-class.md#rc-eqdefault)

* `class`:
[données](007-class.md#rc-org) --
[invariant](007-class.md#rc-struct) --
[membres](007-class.md#rc-member) --
[aides](007-class.md#rc-helper) --
[types concrets](007-class.md#ss-concrete) --
[constructeurs, =, et destructeurs](007-class.md) --
[hiérarchie](007-class.md#ss-hier) --
[opérateurs](007-class.md#ss-overload)

* `concept`:
[règles](015-templates.md#ss-concepts) --
[en programmation générique](015-templates.md#rt-raise) --
[arguments de modèle](015-templates.md#rt-concepts) --
[semantique](015-templates.md#rt-low)

* `constructor`:
[invariant](007-class.md#rc-struct) --
[établir l'invariant](007-class.md#rc-ctor) --
[`throw`](007-class.md#rc-throw) --
[par défaut](007-class.md#rc-default0) --
[inexistant](007-class.md#rc-default) --
[`explicit`](007-class.md#rc-explicit) --
[delegation](007-class.md#rc-delegating) --
[`virtual`](007-class.md#rc-ctor-virtual)

* `derived class`:
[quand l'utiliser](007-class.md#rh-domain) --
[en tant qu'interface](007-class.md#rh-abstract) --
[destructeurs](007-class.md#rh-dtor) --
[copier](007-class.md#rh-copy) --
[définir des getters et setters](007-class.md#rh-get) --
[héritage multiple](007-class.md#rh-mi-interface) --
[surcharge](007-class.md#rh-using) --
[tranchage](007-class.md#rc-copy-virtual) --
[`dynamic_cast`](007-class.md#rh-dynamic_cast)

* `destructor`:
[et constructeurs](007-class.md#rc-matched) --
[quand nécessaire ?](007-class.md#rc-dtor) --
[ne doit pas échouer](007-class.md#rc-dtor-fail)

* `exception`:
[erreurs](013-errors.md) --
[`throw`](013-errors.md#re-throw) --
[uniquement pour les erreurs](013-errors.md#re-errors) --
[`noexcept`](013-errors.md#re-noexcept) --
[minimiser `try`](013-errors.md#re-catch) --
[et si aucune exception ?](013-errors.md#re-no-throw-codes)

* `for`:
[for range et for](010-expr.md#res-for-range) --
[for et while](010-expr.md#res-for-while) --
[for-initializer](010-expr.md#res-for-init) --
[corps vide](010-expr.md#res-empty) --
[variable de boucle](010-expr.md#res-loop-counter) --
[variable de boucle type ???](#res-???)

* `function`:
[nommage](006-functions.md#rf-package) --
[une seule opération](006-functions.md#rf-logical) --
[pas de `throw`](006-functions.md#rf-noexcept) --
[arguments](006-functions.md#rf-smart) --
[passage d'arguments](006-functions.md#rf-conventional) --
[retour multiples](006-functions.md#rf-out-multi) --
[pointeurs](006-functions.md#rf-return-ptr) --
[lambda](006-functions.md#rf-capture-vs-overload)

* `inline`:
[petites fonctions](006-functions.md#rf-inline) --
[dans les headers](017-source.md#rs-inline)

* initialization:
[toujours](010-expr.md#res-always) --
[préférer `{}`](010-expr.md#res-list) --
[lambda](010-expr.md#res-lambda-init) --
[initialisateurs de membre par défaut](007-class.md#rc-in-class-initializer) --
[membres de classe](007-class.md#rc-initialize) --
[fonctions de fabrique](007-class.md#rc-factory)

* lambda expression:
[quand l'utiliser](007-class.md#ss-lambdas)

* operator:
[conventionnel](007-class.md#ro-conventional) --
[éviter les opérateurs de conversion](007-class.md#ro-conversion) --
[et lambdas](007-class.md#ro-lambda)

* `public`, `private`, et `protected`:
[masquage d'information](007-class.md#rc-private) --
[cohérence](007-class.md#rh-public) --
[`protected`](007-class.md#rh-protected)

* `static_assert`:
[vérifications à la compilation](004-philosophy.md#rp-compile-time) --
[et concepts](015-templates.md#rt-check-class)

* `struct`:
[pour organiser les données](007-class.md#rc-org) --
[utiliser si pas d'invariant](007-class.md#rc-struct) --
[pas de membres privés](007-class.md#rc-class)

* `template`:
[abstraction](015-templates.md#rt-raise) --
[conteneurs](015-templates.md#rt-cont) --
[concepts](015-templates.md#rt-concepts)

* `unsigned`:
[et signé](010-expr.md#res-mix) --
[manipulation des bits](010-expr.md#res-unsigned)

* `virtual`:
[interfaces](005-interfaces.md#ri-abstract) --
[not `virtual`](007-class.md#rc-concrete) --
[destructeur](007-class.md#rc-dtor-virtual) --
[ne jamais échouer](007-class.md#rc-dtor-fail)

Vous pouvez consulter les concepts de conception utilisés pour exprimer les règles :

* assertion : ???
* error : ???
* exception : garantie d'exception (???) 
* failure : ??
* invariant : ???
* leak : ???
* library : ???
* precondition : ???
* postcondition : ???
* resource : ???