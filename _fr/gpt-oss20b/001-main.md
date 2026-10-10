# <a name="main"></a>Lignes directrices de C++

14 Juin 2026

Éditeurs :

* [Bjarne Stroustrup](https://www.stroustrup.com)
* [Herb Sutter](https://herbsutter.com/)

Ceci est un document vivant en amélioration continue.  
S’il s’agissait d’un projet open‑source (code), cette version serait 0.8.  
La copie, l’utilisation, la modification et la création d’œuvres dérivées de ce projet sont licenciées sous une licence de style MIT.  
Contribuer à ce projet nécessite l'acceptation d'une licence de contributeur. Reportez‑vous au fichier [LICENSE](https://github.com/isocpp/CppCoreGuidelines/blob/master/LICENSE) pour plus de détails.  
Nous mettons ce projet à disposition des « utilisateurs amicaux » afin qu’ils l’utilisent, le copient, le modifient et en dérivent, en espérant obtenir des retours constructifs.

Les commentaires et suggestions d'amélioration sont les bienvenus.  
Nous prévoyons de modifier et d'étendre ce document au fur et à mesure que notre compréhension, le langage et l’ensemble des bibliothèques disponibles s'améliorent.  
Lorsque vous commentez, veuillez prendre en compte [l’introduction](003-introduction.md) qui décrit nos buts et notre approche générale.  
La liste des contributeurs se trouve [ici](#ss-ack) @TODO-LINK.

Problèmes :

* Les ensembles de règles n'ont pas été entièrement vérifiés pour leur exhaustivité, leur cohérence ou leur applicabilité.  
* Les trois points d'interrogation (???) indiquent les informations manquantes connues.  
* Mettre à jour les sections de référence ; de nombreuses sources pré‑C++11 sont trop anciennes.  
* Pour une liste de tâches plus ou moins actualisée, consultez : [À faire : proto‑règles non classées](031-unclassified.md).

Vous pouvez [lire une explication de la portée et de la structure de ce Guide](002-abstract.md) ou passer directement au contenu :

* [Dans : Introduction](003-introduction.md)  
* [P : Philosophie](004-philosophy.md)  
* [I : Interfaces](005-interfaces.md)  
* [F : Fonctions](006-functions.md)  
* [C : Classes et hiérarchies de classes](007-class.md)  
* [Enum : Énumérations](008-enum.md)  
* [R : Gestion des ressources](009-resource.md)  
* [ES : Expressions et instructions](010-expr.md)  
* [Per : Performance](011-performance.md)  
* [CP : Concurrence et parallélisme](012-concurrency.md)  
* [E : Gestion des erreurs](013-errors.md)  
* [Con : Constantes et immutabilité](014-const.md)  
* [T : Templates et programmation générique](015-templates.md)  
* [CPL : Programmation de style C](016-cpl.md)  
* [SF : Fichiers sources](017-source.md)  
* [SL : La Bibliothèque Standard](018-stdlib.md)

Sections de soutien :

* [A : Idées architecturales](019-a.md)  
* [NR : Non‑règles et mythes](020-not.md)  
* [RF : Références](021-references.md)  
* [Pro : Profils](022-profile.md)  
* [GSL : Bibliothèque d’assistance aux lignes directrices](023-gsl.md)  
* [NL : Suggestions de nommage et de mise en page](024-naming.md)  
* [FAQ : Réponses aux questions fréquemment posées](025-faq.md)  
* [Annexe A : Bibliothèques](026-libraries.md)  
* [Annexe B : Modernisation du code](027-modernizing.md)  
* [Annexe C : Discussion](028-discussion.md)  
* [Annexe D : Outils de soutien](029-tools.md)  
* [Glossaire](030-glossary.md)  
* [À faire : proto‑règles non classées](031-unclassified.md)

Vous pouvez échantillonner des règles pour des fonctionnalités spécifiques :

* assignment :  
[types réguliers](#rc-regular) -- @TODO-LINK  
[préférer l'initialisation](#rc-initialize) -- @TODO-LINK  
[copie](#rc-copy-semantic) -- @TODO-LINK  
[déplacement](#rc-move-semantic) -- @TODO-LINK  
[autres opérations](#rc-matched) -- @TODO-LINK  
[par défaut](#rc-eqdefault) -- @TODO-LINK  

* `class` :  
[données](#rc-org) -- @TODO-LINK  
[invariant](#rc-struct) -- @TODO-LINK  
[membres](#rc-member) -- @TODO-LINK  
[aides](#rc-helper) -- @TODO-LINK  
[types concrets](#ss-concrete) -- @TODO-LINK  
[Constructeurs, = , et destructeurs](#s-ctor) -- @TODO-LINK  
[hiérarchie](#ss-hier) -- @TODO-LINK  
[opérateurs](#ss-overload) -- @TODO-LINK  

* `concept` :  
[règles](#ss-concepts) -- @TODO-LINK  
[en programmation générique](#rt-raise) -- @TODO-LINK  
[arguments de modèles](#rt-concepts) -- @TODO-LINK  
[semantique](#rt-low) -- @TODO-LINK  

* constructor :  
[invariant](#rc-struct) -- @TODO-LINK  
[établir l'invariant](#rc-ctor) -- @TODO-LINK  
[lancer](#rc-throw) -- @TODO-LINK  
[par défaut](#rc-default0) -- @TODO-LINK  
[pas nécessaire](#rc-default) -- @TODO-LINK  
[explicite](#rc-explicit) -- @TODO-LINK  
[délégant](#rc-delegating) -- @TODO-LINK  
[virtuel](#rc-ctor-virtual) -- @TODO-LINK  

* derived `class` :  
[quand l'utiliser](#rh-domain) -- @TODO-LINK  
[en tant qu'interface](#rh-abstract) -- @TODO-LINK  
[destructeurs](#rh-dtor) -- @TODO-LINK  
[copie](#rh-copy) -- @TODO-LINK  
[accesseurs et mutateurs](#rh-get) -- @TODO-LINK  
[héritage multiple](#rh-mi-interface) -- @TODO-LINK  
[surcharge](#rh-using) -- @TODO-LINK  
[découpage](#rc-copy-virtual) -- @TODO-LINK  
[conversion dynamique](#rh-dynamic_cast) -- @TODO-LINK  

* destructor :  
[et constructeurs](#rc-matched) -- @TODO-LINK  
[nécessaire ?](#rc-dtor) -- @TODO-LINK  
[doit ne pas échouer](#rc-dtor-fail) -- @TODO-LINK  

* exception :  
[erreurs](013-errors.md) --  
[`lancer`](#re-throw) -- @TODO-LINK  
[pour erreurs uniquement](#re-errors) -- @TODO-LINK  
[`noexcept`](#re-noexcept) -- @TODO-LINK  
[minimiser `try`](#re-catch) -- @TODO-LINK  
[et si pas d'exception ?](#re-no-throw-codes) -- @TODO-LINK  

* `for` :  
[boucle range-for et for](#res-for-range) -- @TODO-LINK  
[for et while](#res-for-while) -- @TODO-LINK  
[initialiseur for](#res-for-init) -- @TODO-LINK  
[corps vide](#res-empty) -- @TODO-LINK  
[variable de boucle](#res-loop-counter) -- @TODO-LINK  
[type de variable de boucle ???](#res-???) -- @TODO-LINK  

* function :  
[nommage](#rf-package) -- @TODO-LINK  
[opération unique](#rf-logical) -- @TODO-LINK  
[ne pas lancer](#rf-noexcept) -- @TODO-LINK  
[arguments](#rf-smart) -- @TODO-LINK  
[passage d'arguments](#rf-conventional) -- @TODO-LINK  
[plusieurs valeurs de retour](#rf-out-multi) -- @TODO-LINK  
[pointeurs](#rf-return-ptr) -- @TODO-LINK  
[lambda](#rf-capture-vs-overload) -- @TODO-LINK  

* `inline` :  
[fonctions petites](#rf-inline) -- @TODO-LINK  
[... dans les en‑têtes](#rs-inline) -- @TODO-LINK  

* initialization :  
[toujours](#res-always) -- @TODO-LINK  
[préférer \{\}](#res-list) -- @TODO-LINK  
[lambdas](#res-lambda-init) -- @TODO-LINK  
[initialisateurs de membres par défaut](#rc-in-class-initializer) -- @TODO-LINK  
[membres de classe](#rc-initialize) -- @TODO-LINK  
[fonctions de fabrique](#rc-factory) -- @TODO-LINK  

* lambda expression :  
[quand l'utiliser](#ss-lambdas) -- @TODO-LINK  

* operator :  
[conventionnel](#ro-conventional) -- @TODO-LINK  
[éviter les opérateurs de conversion](#ro-conversion) -- @TODO-LINK  
[et lambdas](#ro-lambda) -- @TODO-LINK  

* `public`, `private`, and `protected` :  
[cacher l'information](#rc-private) -- @TODO-LINK  
[cohérence](#rh-public) -- @TODO-LINK  
[`protected`](#rh-protected) -- @TODO-LINK  

* `static_assert` :  
[vérification à la compilation](#rp-compile-time) -- @TODO-LINK  
[et concepts](#rt-check-class) -- @TODO-LINK  

* struct :  
[pour organiser les données](#rc-org) -- @TODO-LINK  
[utiliser s'il n'y a pas d'invariant](#rc-struct) -- @TODO-LINK  
[ne possède pas de membres privés](#rc-class) -- @TODO-LINK  

* template :  
[abstraction](#rt-raise) -- @TODO-LINK  
[conteneurs](#rt-cont) -- @TODO-LINK  
[concepts](#rt-concepts) -- @TODO-LINK  

* unsigned :  
[et signé](#res-mix) -- @TODO-LINK  
[manipulation de bits](#res-unsigned) -- @TODO-LINK  

* virtual :  
[interfaces](#ri-abstract) -- @TODO-LINK  
[ne pas `virtual`](#rc-concrete) -- @TODO-LINK  
[destructeur](#rc-dtor-virtual) -- @TODO-LINK  
[ne jamais échouer](#rc-dtor-fail) -- @TODO-LINK  

Vous pouvez voir les concepts de conception utilisés pour exprimer les règles :

* assertion : ???  
* erreur : ???  
* exception : garantie d'exception (???)  
* échec : ???  
* invariant : ???  
* fuite : ???  
* bibliothèque : ???  
* précondition : ???  
* postcondition : ???  
* ressource : ???