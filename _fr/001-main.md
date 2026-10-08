---
title: Lignes Directrices Essentielles de C++
---

# <a name="main">Lignes Directrices Essentielles de C++</a>

14 juin 2026

Éditeurs :

* [Bjarne Stroustrup](https://www.stroustrup.com)
* [Herb Sutter](https://herbsutter.com/)

Ceci est un document vivant, en amélioration continue.
S'il s'agissait d'un projet open source (de code), ce serait la version 0.8.
La copie, l'utilisation, la modification et la création d'œuvres dérivées de ce projet sont soumises à une licence de type MIT.
Contribuer à ce projet exige l'acceptation d'une licence du contributeur. Voir le fichier joint [LICENSE](https://github.com/isocpp/CppCoreGuidelines/blob/master/LICENSE) pour plus de détails.
Nous mettons ce projet à disposition des « utilisateurs bienveillants » pour l'utiliser, le copier, le modifier et en dériver, dans l'espoir d'obtenir des retours constructifs.

Les commentaires et suggestions d'amélioration sont les bienvenus.
Nous prévoyons de modifier et d'étendre ce document au fur et à mesure que notre compréhension s'améliore et que le langage ainsi que l'ensemble des bibliothèques disponibles progressent.
Lors de vos commentaires, veuillez tenir compte de [l'introduction](#s-introduction), qui présente nos objectifs et notre approche générale.
La liste des contributeurs est [ici](#ss-ack).

Problèmes :

* Les ensembles de règles n'ont pas encore été vérifiés de manière exhaustive pour leur exhaustivité, leur cohérence ou leur applicabilité.
* Les triples points d'interrogation (???) indiquent des informations connues manquantes.
* Mettre à jour les sections de références ; de nombreuses sources antérieures à C++11 sont désormais trop anciennes.
* Pour une liste de tâches à faire plus ou moins à jour, voir : [À faire : Proto-règles non classées](#s-unclassified).

Vous pouvez [lire une explication sur la portée et la structure de ce guide](#s-abstract) ou passer directement à :

* [In : Introduction](#s-introduction)
* [P : Philosophie](#s-philosophy)
* [I : Interfaces](#s-interfaces)
* [F : Fonctions](#s-functions)
* [C : Classes et hiérarchies de classes](#s-class)
* [Enum : Énumérations](#s-enum)
* [R : Gestion des ressources](#s-resource)
* [ES : Expressions et instructions](#s-expr)
* [Per : Performance](#s-performance)
* [CP : Concurrence et parallélisme](#s-concurrency)
* [E : Gestion des erreurs](#s-errors)
* [Con : Constantes et immuabilité](#s-const)
* [T : Modèles et programmation générique](#s-templates)
* [CPL : Programmation de style C](#s-cpl)
* [SF : Fichiers sources](#s-source)
* [SL : Bibliothèque standard](#sl-the-standard-library)

Sections de soutien :

* [A : Idées architecturales](#s-a)
* [NR : Non-règles et mythes](#s-not)
* [RF : Références](#s-references)
* [Pro : Profils](#s-profile)
* [GSL : Bibliothèque de support des directives](#s-gsl)
* [NL : Suggestions de noms et de mise en page](#s-naming)
* [FAQ : Réponses aux questions fréquemment posées](#s-faq)
* [Appendice A : Bibliothèques](#s-libraries)
* [Appendice B : Modernisation du code](#s-modernizing)
* [Appendice C : Discussion](#s-discussion)
* [Appendice D : Outils de support](#s-tools)
* [Glossaire](#s-glossary)
* [À faire : Proto-règles non classées](#s-unclassified)

Vous pouvez consulter des règles sur des fonctionnalités linguistiques spécifiques :

* affectation :
[types réguliers](#rc-regular) --
[préférer l'initialisation](#rc-initialize) --
[copie](#rc-copy-semantic) --
[déplacement](#rc-move-semantic) --
[autres opérations](#rc-matched) --
[par défaut](#rc-eqdefault)
* `class` :
[données](#rc-org) --
[invariant](#rc-struct) --
[membres](#rc-member) --
[assistants](#rc-helper) --
[types concrets](#ss-concrete) --
[constructeurs, = et destructeurs](#s-ctor) --
[hiérarchie](#ss-hier) --
[opérateurs](#ss-overload)
* `concept` :
[règles](#ss-concepts) --
[dans la programmation générique](#rt-raise) --
[arguments de modèles](#rt-concepts) --
[sémantique](#rt-low)
* constructeur :
[invariant](#rc-struct) --
[établir l'invariant](#rc-ctor) --
[`throw`](#rc-throw) --
[par défaut](#rc-default0) --
[non nécessaire](#rc-default) --
[`explicit`](#rc-explicit) --
[délégué](#rc-delegating) --
[`virtual`](#rc-ctor-virtual)
* classe dérivée :
[quand l'utiliser](#rh-domain) --
[comme interface](#rh-abstract) --
[destructeurs](#rh-dtor) --
[copie](#rh-copy) --
[accesseurs](#rh-get) --
[héritage multiple](#rh-mi-interface) --
[surcharge](#rh-using) --
[troncature](#rc-copy-virtual) --
[`dynamic_cast`](#rh-dynamic_cast)
* destructeur :
[et constructeurs](#rc-matched) --
[quand est-il nécessaire ?](#rc-dtor) --
[ne doit pas échouer](#rc-dtor-fail)
* exception :
[erreurs](#s-errors) --
[`throw`](#re-throw) --
[pour les erreurs uniquement](#re-errors) --
[`noexcept`](#re-noexcept) --
[minimiser `try`](#re-catch) --
[et si pas d'exceptions ?](#re-no-throw-codes)
* `for` :
[range-for et for](#res-for-range) --
[for et while](#res-for-while) --
[initialiseur de for](#res-for-init) --
[corps vide](#res-empty) --
[variable de boucle](#res-loop-counter) --
[type de variable de boucle ???](#res-??? )
* fonction :
[nommage](#rf-package) --
[opération unique](#rf-logical) --
[sans exception](#rf-noexcept) --
[arguments](#rf-smart) --
[passage des arguments](#rf-conventional) --
[valeurs de retour multiples](#rf-out-multi) --
[pointeurs](#rf-return-ptr) --
[lambdas](#rf-capture-vs-overload)
* `inline` :
[petites fonctions](#rf-inline) --
[dans les en-têtes](#rs-inline)
* initialisation :
[toujours](#res-always) --
[préférer `{}`](#res-list) --
[lambdas](#res-lambda-init) --
[initialiseurs de membres par défaut](#rc-in-class-initializer) --
[membres de classe](#rc-initialize) --
[fonctions de fabrique](#rc-factory)
* expression lambda :
[quand l'utiliser](#ss-lambdas)
* opérateur :
[conventionnel](#ro-conventional) --
[éviter les opérateurs de conversion](#ro-conversion) --
[et lambdas](#ro-lambda)
* `public`, `private` et `protected` :
[masquage de l'information](#rc-private) --
[cohérence](#rh-public) --
[`protected`](#rh-protected)
* `static_assert` :
[vérification à la compilation](#rp-compile-time) --
[et concepts](#rt-check-class)
* `struct` :
[pour organiser les données](#rc-org) --
[utiliser si pas d'invariant](#rc-struct) --
[pas de membres privés](#rc-class)
* `template` :
[abstraction](#rt-raise) --
[conteneurs](#rt-cont) --
[concepts](#rt-concepts)
* `unsigned` :
[et signé](#res-mix) --
[manipulation de bits](#res-unsigned)
* `virtual` :
[interfaces](#ri-abstract) --
[pas `virtual`](#rc-concrete) --
[destructeur](#rc-dtor-virtual) --
[jamais échouer](#rc-dtor-fail)

Vous pouvez consulter les concepts de conception utilisés pour exprimer les règles :

* assertion : ???
* error : ???
* exception : garantie d'exception (???)
* failure : ???
* invariant : ???
* leak : ???
* library : ???
* precondition : ???
* postcondition : ???
* resource : ???
