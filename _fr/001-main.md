# <a name="main"></a>Directives C++ Core

14 juin 2026

Éditeurs :

* [Bjarne Stroustrup](https://www.stroustrup.com)
* [Herb Sutter](https://herbsutter.com/)

Il s'agit d'un document vivant en amélioration continue.
S'il s'agissait d'un projet open‑source (code), cette version serait la 0.8.
La copie, l'utilisation, la modification et la création d'œuvres dérivées de ce projet sont autorisées sous licence de type MIT.
Contribuer à ce projet nécessite l'accord d'une licence de contributeur. Veuillez consulter le fichier [LICENSE](https://github.com/isocpp/CppCoreGuidelines/blob/master/LICENSE) pour plus de détails.
Nous rendons ce projet disponible aux « utilisateurs amicaux » afin qu'ils l'utilisent, le copient, le modifient et en dérivent, dans l'espoir de retours constructifs.

Les commentaires et suggestions d'amélioration sont les bienvenus.
Nous prévoyons de modifier et de mettre à jour ce document à mesure que notre compréhension, le langage et l'ensemble des bibliothèques disponibles s'améliorent.
Lors de vos commentaires, veuillez noter [l'introduction](003-introduction.md) qui expose nos objectifs et notre approche générale.
La liste des contributeurs est [ici](#ss-ack).

Problèmes :

* Les ensembles de règles n'ont pas été entièrement vérifiés pour exhaustivité, cohérence ou applicabilité.
* Les tripespoints (???) indiquent des informations manquantes connues.
* Mettez à jour les sections de référence ; de nombreuses sources pré‑C++11 sont trop anciennes.
* Pour une liste de tâches plus ou moins à jour, consultez : [À faire : proto‑règles non classées](031-unclassified.md).

Vous pouvez [lire une explication de la portée et de la structure de ce guide](002-abstract.md) ou passer directement à la lecture :

* [Dans : Introduction](003-introduction.md)
* [P : Philosophie](004-philosophy.md)
* [I : Interfaces](005-interfaces.md)
* [F : Fonctions](006-functions.md)
* [C : Classes et hiérarchies de classes](007-class.md)
* [Enum : Énumérations](008-enum.md)
* [R : Gestion des ressources](009-resource.md)
* [ES : Expressions et déclarations](010-expr.md)
* [Per : Performance](011-performance.md)
* [CP : Concurrence et parallélisme](012-concurrency.md)
* [E : Gestion des erreurs](013-errors.md)
* [Con : Constantes et immuabilité](014-const.md)
* [T : Modèles et programmation générique](015-templates.md)
* [CPL : Programmation de style C](016-cpl.md)
* [SF : Fichiers sources](017-source.md)
* [SL : La bibliothèque standard](018-stdlib.md)

Sections de soutien :

* [A : Idées architecturales](019-a.md)
* [NR : Non‑règles et mythes](020-not.md)
* [RF : Références](021-references.md)
* [Pro : Profils](022-profile.md)
* [GSL : Bibliothèque de support des directives](023-gsl.md)
* [NL : Suggestions de nommage et d’agencement](024-naming.md)
* [FAQ : Réponses aux questions fréquentes](025-faq.md)
* [Annexe A : Bibliothèques](026-libraries.md)
* [Annexe B : Modernisation du code](027-modernizing.md)
* [Annexe C : Discussion](028-discussion.md)
* [Annexe D : Outils de soutien](029-tools.md)
* [Glossaire](030-glossary.md)
* [À faire : proto‑règles non classées](031-unclassified.md)

Vous pouvez consulter les règles pour les caractéristiques suivantes :

* affectation :
[taux réguliers](#rc-regular) --
[préférer l'initialisation](#rc-initialize) --
[copie](#rc-copy-semantic) --
[déplacement](#rc-move-semantic) --
[autres opérations](#rc-matched) --
[par défaut](#rc-eqdefault)
* `class` :
[données](#rc-org) --
[invariant](#rc-struct) --
[membres](#rc-member) --
[aides](#rc-helper) --
[types concrets](#ss-concrete) --
[constructeurs, = et destructeurs](#s-ctor) --
[hiérarchie](#ss-hier) --
[opérateurs](#ss-overload)
* `concept` :
[règles](#ss-concepts) --
[en programmation générique](#rt-raise) --
[argements de modèles](#rt-concepts) --
[sémantiques](#rt-low)
* constructeur :
[invariant](#rc-struct) --
[établir l'invariant](#rc-ctor) --
[`throw`](#rc-throw) --
[par défaut](#rc-default0) --
[non nécessaire](#rc-default) --
[`explicit`](#rc-explicit) --
[delegating](#rc-delegating) --
[`virtual`](#rc-ctor-virtual)
* `class` dérivée :
[quand l'utiliser](#rh-domain) --
[comme interface](#rh-abstract) --
[destructeurs](#rh-dtor) --
[copie](#rh-copy) --
[getters et setters](#rh-get) --
[héritage multiple](#rh-mi-interface) --
[chargement d'opérateurs](#rh-using) --
[slicing](#rc-copy-virtual) --
[`dynamic_cast`](#rh-dynamic_cast)
* destructeur :
[et constructeurs](#rc-matched) --
[quand nécessaire ?](#rc-dtor) --
[ne doit pas échouer](#rc-dtor-fail)
* exception :
[erreurs](013-errors.md) --
[`throw`](#re-throw) --
[pour erreurs uniquement](#re-errors) --
[`noexcept`](#re-noexcept) --
[minimiser `try`](#re-catch) --
[quand aucune exception ?](#re-no-throw-codes)
* `for` :
[for de plage et for](#res-for-range) --
[for et while](#res-for-while) --
[for initialiseur](#res-for-init) --
[corps vide](#res-empty) --
[variable de boucle](#res-loop-counter) --
[type de variable de boucle ???](#res-???)
* fonction :
[nommage](#rf-package) --
[une seule opération](#rf-logical) --
[sans throw](#rf-noexcept) --
[arguments](#rf-smart) --
[passage d'arguments](#rf-conventional) --
[plusieurs valeurs de retour](#rf-out-multi) --
[pointeurs](#rf-return-ptr) --
[lambdas](#rf-capture-vs-overload)
* `inline` :
[fonctions petites](#rf-inline) --
[dans les en-têtes](#rs-inline)
* initialisation :
[toujours](#res-always) --
[préférer `{}`](#res-list) --
[lambdas](#res-lambda-init) --
[initialiseurs par défaut des membres](#rc-in-class-initializer) --
[membres de classe](#rc-initialize) --
[fonctions de fabrique](#rc-factory)
* expression lambda :
[quand l'utiliser](#ss-lambdas)
* opérateur :
[conventionnel](#ro-conventional) --
[éviter les opérateurs de conversion](#ro-conversion) --
[et lambdas](#ro-lambda)
* `public`, `private`, et `protected` :
[masquage d'information](#rc-private) --
[cohérence](#rh-public) --
[`protected`](#rh-protected)
* `static_assert` :
[vérification à la compilation](#rp-compile-time) --
[et concepts](#rt-check-class)
* `struct` :
[organisation de données](#rc-org) --
[utiliser s'il n'y a pas d'invariant](#rc-struct) --
[pas de membres privés](#rc-class)
* `template` :
[abstraction](#rt-raise) --
[conteneurs](#rt-cont) --
[concepts](#rt-concepts)
* `unsigned` :
[et signé](#res-mix) --
[manipulation bit à bit](#res-unsigned)
* `virtual` :
[interfaces](#ri-abstract) --
[pas de `virtual`](#rc-concrete) --
[destructeur](#rc-dtor-virtual) --
[ne jamais échouer](#rc-dtor-fail)

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