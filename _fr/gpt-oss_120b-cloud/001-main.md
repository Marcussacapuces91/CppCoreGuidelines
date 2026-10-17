# <a name="main"></a>Lignes Directrices essentielles du C++

14 juin 2026  

**Éditeurs :**

* [Bjarne Stroustrup](https://www.stroustrup.com)  
* [Herb Sutter](https://herbsutter.com/)

Ce document est vivant et en amélioration continue.  
S'il s'agissait d'un projet open‑source (code), il aurait été la version 0.8.  
La copie, l'utilisation, la modification et la création d'œuvres dérivées à partir de ce projet sont autorisées sous une licence de type MIT.  
Contribuer à ce projet requiert l'acceptation d'une licence de contributeur. Voir le fichier [LICENSE](https://github.com/isocpp/CppCoreGuidelines/blob/master/LICENSE) joint pour plus de détails.  
Nous mettons ce projet à disposition des « utilisateurs amicaux » afin qu'ils l'utilisent, le copient, le modifient et en dérivent, dans l'espoir d'obtenir des retours constructifs.

Les commentaires et suggestions d'améliorations sont les bienvenus.  
Nous prévoyons de modifier et d'étendre ce document à mesure que notre compréhension s'améliore ainsi que le langage et l'ensemble des bibliothèques disponibles.  
Lors de vos commentaires, veuillez vous référer à [l'introduction](003-introduction.md) qui expose nos objectifs et notre approche générale.  
La liste des contributeurs se trouve [ici](021-references.md#ss-ack)

**Problèmes :**

* Les ensembles de règles n'ont pas été entièrement vérifiés quant à leur exhaustivité, cohérence ou applicabilité.  
* Les triples points d'interrogation (???) indiquent des informations manquantes connues.  
* Mettez à jour les sections de références ; de nombreuses sources antérieures à C++11 sont trop anciennes.
* Pour une liste de tâches à jour (plus ou moins), consultez : [À faire : Règles proto non classifiées](031-unclassified.md).

Vous pouvez [lire une explication de la portée et de la structure de ce Guide](002-abstract.md) ou simplement y plonger immédiatement :

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

**Sections d'appui :**

* [A : Idées architecturales](019-a.md)  
* [NR : Non‑Règles et mythes](020-not.md)  
* [RF : Références](021-references.md)  
* [Pro : Profils](022-profile.md)  
* [GSL : Bibliothèque de soutien aux directives](023-gsl.md)  
* [NL : Suggestions de nommage et de mise en page](024-naming.md)  
* [FAQ : Réponses aux questions fréquentes](025-faq.md)  
* [Annexe A : Bibliothèques](026-libraries.md)  
* [Annexe B : Modernisation du code](027-modernizing.md)  
* [Annexe C : Discussion](028-discussion.md)  
* [Annexe D : Outils d'aide](029-tools.md)  
* [Glossaire](030-glossary.md)  
* [À faire : Règles proto non classifiées](031-unclassified.md)

Vous pouvez consulter des règles pour des caractéristiques spécifiques du langage :

* affectation :
[types réguliers](007-class.md#rc-regular) --
[préférer l'initialisation](007-class.md#rc-initialize) --
[copie](007-class.md#rc-copy-semantic) --
[déplacement](007-class.md#rc-move-semantic) --
[autres opérations](007-class.md#rc-matched) --
[défaut](007-class.md#rc-eqdefault)

* `class` :
[données](007-class.md#rc-org) --
[invariant](007-class.md#rc-struct) --
[membres](007-class.md#rc-member) --
[aides](007-class.md#rc-helper) --
[types concrets](007-class.md#ss-concrete) @TODO-LINK --
[constructeurs, =, et destructeurs](007-class.md) --
[hiérarchie](007-class.md#ss-hier) @TODO-LINK --
[opérateurs](007-class.md#ss-overload) @TODO-LINK

* `concept` :
[règles](015-templates.md#ss-concepts) --
[dans la programmation générique](015-templates.md#rt-raise) --
[arguments de modèle](015-templates.md#rt-concepts) --
[sémantique](015-templates.md#rt-low)

* constructeur :
[invariant](007-class.md#rc-struct) --
[établir l'invariant](007-class.md#rc-ctor) --
[`throw`](007-class.md#rc-throw) --
[défaut](007-class.md#rc-default0) --
[non nécessaire](007-class.md#rc-default) --
[`explicit`](007-class.md#rc-explicit) --
[délégation](007-class.md#rc-delegating) --
[`virtual`](007-class.md#rc-ctor-virtual)

* classe dérivée `class` :
[quand l'utiliser](007-class.md#rh-domain) --
[comme interface](007-class.md#rh-abstract) --
[destructeurs](007-class.md#rh-dtor) --
[copie](007-class.md#rh-copy) --
[accesseurs et mutateurs](007-class.md#rh-get) --
[héritage multiple](007-class.md#rh-mi-interface) --
[surcharge](007-class.md#rh-using) --
[slicing](007-class.md#rc-copy-virtual) --
[`dynamic_cast`](007-class.md#rh-dynamic_cast)

* destructeur :
[et constructeurs](007-class.md#rc-matched) --
[quand nécessaire ?](007-class.md#rc-dtor) --
[ne doit pas échouer](007-class.md#rc-dtor-fail)

* exception :
[erreurs](013-errors.md) --
[`throw`](013-errors.md#re-throw) --
[pour les erreurs uniquement](013-errors.md#re-errors) --
[`noexcept`](013-errors.md#re-noexcept) --
[minimiser `try`](013-errors.md#re-catch) --
[et si aucune exception ?](013-errors.md#re-no-throw-codes)

* `for` :
[range‑for et for](010-expr.md#res-for-range) --
[for et while](010-expr.md#res-for-while) --
[initialisation du for](010-expr.md#res-for-init) --
[corps vide](010-expr.md#res-empty) --
[variable de boucle](010-expr.md#res-loop-counter) --
[type de variable de boucle ???](#res-???)

* fonction :
[nommage](006-functions.md#rf-package) --
[opération unique](006-functions.md#rf-logical) --
[pas d'exception](006-functions.md#rf-noexcept) --
[arguments](006-functions.md#rf-smart) --
[passage d'arguments](006-functions.md#rf-conventional) --
[valeurs de retour multiples](006-functions.md#rf-out-multi) --
[pointeurs](006-functions.md#rf-return-ptr) --
[lambdas](006-functions.md#rf-capture-vs-overload)

* `inline` :
[fonctions petites](006-functions.md#rf-inline) --
[dans les en‑têtes](017-source.md#rs-inline)

* initialisation :
[toujours](010-expr.md#res-always) --
[préférer `{}`](010-expr.md#res-list) --
[lambdas](010-expr.md#res-lambda-init) --
[initialiseurs de membres par défaut](007-class.md#rc-in-class-initializer) --
[membres de classe](007-class.md#rc-initialize) --
[fonctions usine](007-class.md#rc-factory)

* expression lambda :
[quand l'utiliser](007-class.md#ss-lambdas) @TODO-LINK

* opérateur :
[conventionnel](007-class.md#ro-conventional) --
[éviter les opérateurs de conversion](007-class.md#ro-conversion) --
[et lambdas](007-class.md#ro-lambda)

* `public`, `private` et `protected` :
[cacher l'information](007-class.md#rc-private) --
[cohérence](007-class.md#rh-public) --
[`protected`](007-class.md#rh-protected)

* `static_assert` :
[vérification à la compilation](004-philosophy.md#rp-compile-time) --
[et concepts](015-templates.md#rt-check-class)

* `struct` :
[pour organiser des données](007-class.md#rc-org) --
[utiliser si aucun invariant](007-class.md#rc-struct) --
[pas de membres privés](007-class.md#rc-class)

* `template` :
[abstraction](015-templates.md#rt-raise) --
[conteneurs](015-templates.md#rt-cont) --
[concepts](015-templates.md#rt-concepts)

* `unsigned` :
[et signé](010-expr.md#res-mix) --
[manipulation de bits](010-expr.md#res-unsigned)

* `virtual` :
[interfaces](005-interfaces.md#ri-abstract) --
[pas `virtual`](007-class.md#rc-concrete) --
[destructeur](007-class.md#rc-dtor-virtual) --
[ne jamais échouer](007-class.md#rc-dtor-fail)

Vous pouvez consulter les concepts de conception utilisés pour exprimer les règles :

* assertion : ???  
* erreur : ???  
* exception : garantie d'exception (???)  
* échec : ???  
* invariant : ???  
* fuite : ???  
* bibliothèque : ???  
* précondition : ???  
* postcondition : ???  
* ressource : ???
