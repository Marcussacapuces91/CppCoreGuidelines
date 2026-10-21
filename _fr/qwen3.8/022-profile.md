# <a name="s-profile"></a>Pro : Profils

Idéalement, nous suivrions l'ensemble des lignes directrices.
Cela donnerait le code le plus propre, le plus régulier, le moins sujet aux erreurs, et souvent le plus rapide.
Malheureusement, c'est généralement impossible, car nous devons intégrer notre code dans de grandes bases de code existantes et utiliser des bibliothèques déjà en place.
Souvent, ce code a été écrit sur plusieurs décennies et ne respecte pas ces lignes directrices.
Nous devons viser une [adoption progressive](027-modernizing.md).

Quelle que soit la stratégie d'adoption progressive que nous adoptons, nous devons être en mesure d'appliquer des ensembles de lignes directrices connexes pour traiter d'abord certains problèmes et laisser le reste pour plus tard.
Une idée similaire de « lignes directrices connexes » devient importante lorsque certaines, mais pas toutes, les lignes directrices sont considérées comme pertinentes pour une base de code donnée, ou lorsqu'un ensemble de lignes directrices spécialisées doit être appliqué à un domaine d'application particulier.
Nous appelons un tel ensemble de lignes directrices connexes un « profil ».
Nous visons un ensemble de lignes directrices cohérent afin qu'ensemble, elles nous aident à atteindre un objectif précis, tel que « l'absence d'erreurs de bornes »
ou « la sécurité des types statique ».
Chaque profil est conçu pour éliminer une classe d'erreurs.
L'application de règles « aléatoires » de manière isolée est plus susceptible de perturber une base de code que d'apporter une amélioration tangible.

Un « profil » est un sous-ensemble déterministe et portable de règles (c'est-à-dire de restrictions) applicables de manière uniforme, conçu pour garantir une propriété spécifique.
« Déterministe » signifie qu'il ne requiert qu'une analyse locale et pourrait être implémenté dans un compilateur (bien que ce ne soit pas obligatoire).
« Portable » signifie qu'il fonctionne comme une règle du langage, de sorte que les programmeurs peuvent compter sur le fait que différents outils de vérification donneront la même réponse pour le même code.

Un code écrit de manière à ne générer aucun avertissement en utilisant un tel profil de langage est considéré comme conforme au profil.
Un code conforme est considéré comme sûr par construction en ce qui concerne les propriétés de sécurité ciblées par ce profil.
Un code conforme ne sera pas la cause racine d'erreurs pour cette propriété,
bien que de telles erreurs puissent être introduites dans un programme par d'autres codes, des bibliothèques ou l'environnement externe.
Un profil peut également introduire des types de bibliothèque supplémentaires pour faciliter la conformité et encourager un code correct.

Résumé des profils :

* [Pro.type : Sécurité des types](022-profile.md#ss-type)
* [Pro.bounds : Sécurité des bornes](022-profile.md#ss-bounds)
* [Pro.lifetime : Sécurité du cycle de vie](022-profile.md#ss-lifetime)

À l'avenir, nous prévoyons de définir de nombreux autres profils et d'ajouter davantage de vérifications aux profils existants.
Parmi les candidats figurent :

* les promotions/conversions arithmétiques avec rétrécissement (probablement dans le cadre d'un profil distinct de sécurité arithmétique)
* la conversion arithmétique d'un nombre à virgule flottante négatif vers un type entier non signé (idem)
* certains comportements indéfinis : commencer par la liste des comportements indéfinis de Gabriel Dos Reis, élaborée pour le groupe d'étude du WG21
* certains comportements non spécifiés : traiter les problèmes de portabilité.
* les violations de `const` : déjà largement détectées par les compilateurs, mais nous pouvons capturer les conversions inappropriées et l'underuse de `const`.

L'activation d'un profil est définie par l'implémentation ; typiquement, elle est configurée dans l'outil d'analyse utilisé.

Pour supprimer l'application d'une vérification de profil, placez une annotation `suppress` sur un contrat de langage. Par exemple :

    [[suppress("bounds")]] char* raw_find(char* p, int n, char x)    // cherche x dans p[0]..p[n - 1]
    {
        // ...
    }

Désormais, `raw_find()` peut corrompre la mémoire à sa guise.
Évidemment, la suppression doit être très rare.

## <a name="ss-type"></a>Pro.safety : Profil de sécurité des types

Ce profil facilite la construction de code qui utilise correctement les types et évite la requalification de type involontaire.
Il y parvient en se concentrant sur l'élimination des principales sources de violations de type, notamment les utilisations non sûres des conversions de type et des unions.

Aux fins de cette section,
la sécurité des types est définie comme la propriété selon laquelle une variable n'est pas utilisée d'une manière qui ne respecte pas les règles du type de sa définition.
Une mémoire accédée en tant que type `T` ne doit pas être une mémoire valide contenant en réalité un objet d'un type `U` non apparenté.
Notez que la sécurité est censée être complète uniquement lorsqu'elle est combinée avec la [sécurité des bornes](022-profile.md#ss-bounds) et la [sécurité du cycle de vie](022-profile.md#ss-lifetime).

Une implémentation de ce profil doit reconnaître les motifs suivants dans le code source comme non conformes et émettre un diagnostic.

Résumé du profil de sécurité des types :

* <a name="pro-type-avoidcasts"></a>Type.1 : [Éviter les conversions de type](010-expr.md#res-casts) :

  1. <a name="pro-type-reinterpretcast"></a>Ne pas utiliser `reinterpret_cast` ; version stricte de [Éviter les conversions de type](010-expr.md#res-casts) et de [préférer les conversions nommées](010-expr.md#res-casts-named).
  2. <a name="pro-type-arithmeticcast"></a>Ne pas utiliser `static_cast` pour les types arithmétiques ; version stricte de [Éviter les conversions de type](010-expr.md#res-casts) et de [préférer les conversions nommées](010-expr.md#res-casts-named).
  3. <a name="pro-type-identitycast"></a>Ne pas convertir entre des types de pointeurs lorsque le type source et le type cible sont identiques ; version stricte de [Éviter les conversions de type](010-expr.md#res-casts).
  4. <a name="pro-type-implicitpointercast"></a>Ne pas convertir entre des types de pointeurs lorsque la conversion pourrait être implicite ; version stricte de [Éviter les conversions de type](010-expr.md#res-casts).
* <a name="pro-type-downcast"></a>Type.2 : Ne pas utiliser `static_cast` pour une conversion vers un type dérivé :
[utiliser `dynamic_cast` à la place](007-class.md#rh-dynamic_cast).
* <a name="pro-type-constcast"></a>Type.3 : Ne pas utiliser `const_cast` pour supprimer `const` (c'est-à-dire, ne jamais l'utiliser) :
[ne pas supprimer const](010-expr.md#res-casts-const).
* <a name="pro-type-cstylecast"></a>Type.4 : Ne pas utiliser les conversions de type au style C `(T)expression` ni les conversions fonctionnelles `T(expression)` :
préférer la [construction](010-expr.md#res-construct) ou les [conversions nommées](010-expr.md#res-casts-named) ou `T{expression}`.
* <a name="pro-type-init"></a>Type.5 : Ne pas utiliser une variable avant qu'elle n'ait été initialisée :
[toujours initialiser](010-expr.md#res-always).
* <a name="pro-type-memberinit"></a>Type.6 : Toujours initialiser un membre de données :
[toujours initialiser](010-expr.md#res-always),
éventuellement en utilisant des [constructeurs par défaut](007-class.md#rc-default0) ou des
[initialisateurs de membres par défaut](007-class.md#rc-in-class-initializer).
* <a name="pro-type-union"></a>Type.7 : Éviter les unions nues :
[utiliser `variant` à la place](007-class.md#ru-naked).
* <a name="pro-type-varargs"></a>Type.8 : Éviter les arguments variables :
[ne pas utiliser les arguments `va_arg`](006-functions.md#f-varargs).

##### Impact

Avec le profil de sécurité des types, vous pouvez faire confiance au fait que chaque opération est appliquée à un objet valide.
Une exception peut être levée pour indiquer des erreurs qui ne peuvent pas être détectées statiquement (au moment de la compilation).
Notez que cette sécurité des types ne peut être complète que si nous disposons également de la [sécurité des bornes](022-profile.md#ss-bounds) et de la [sécurité du cycle de vie](022-profile.md#ss-lifetime).
Sans ces garanties, une région de mémoire pourrait être accédée indépendamment de l'objet, des objets ou des parties d'objets qui y sont stockés.


## <a name="ss-bounds"></a>Pro.bounds : Profil de sécurité des bornes

Ce profil facilite la construction de code qui opère dans les limites des blocs de mémoire alloués.
Il y parvient en se concentrant sur l'élimination des principales sources de violations de bornes : l'arithmétique des pointeurs et l'indexation de tableaux.
L'une des fonctionnalités clés de ce profil est de restreindre les pointeurs à ne référencer que des objets unitaires, et non des tableaux.

Nous définissons la sécurité des bornes comme la propriété selon laquelle un programme n'utilise pas un objet pour accéder à une mémoire située en dehors de la plage qui lui a été allouée.
La sécurité des bornes est censée être complète uniquement lorsqu'elle est combinée avec la [sécurité des types](022-profile.md#ss-type) et la [sécurité du cycle de vie](022-profile.md#ss-lifetime),
qui couvrent d'autres opérations non sûres permettant des violations de bornes.

Résumé du profil de sécurité des bornes :

* <a name="pro-bounds-arithmetic"></a>Bounds.1 : Ne pas utiliser l'arithmétique des pointeurs. Utiliser `span` à la place :
[passer des pointeurs vers des objets unitaires (uniquement)](005-interfaces.md#ri-array) et [garder l'arithmétique des pointeurs simple](010-expr.md#res-ptr).
* <a name="pro-bounds-arrayindex"></a>Bounds.2 : N'indexer des tableaux qu'avec des expressions constantes :
[passer des pointeurs vers des objets unitaires (uniquement)](005-interfaces.md#ri-array) et [garder l'arithmétique des pointeurs simple](010-expr.md#res-ptr).
* <a name="pro-bounds-decay"></a>Bounds.3 : Pas de dégénérescence tableau-vers-pointeur :
[passer des pointeurs vers des objets unitaires (uniquement)](005-interfaces.md#ri-array) et [garder l'arithmétique des pointeurs simple](010-expr.md#res-ptr).
* <a name="pro-bounds-stdlib"></a>Bounds.4 : Ne pas utiliser de fonctions et de types de la bibliothèque standard qui ne sont pas vérifiés par bornes :
[utiliser la bibliothèque standard de manière sûre pour les types](018-stdlib.md#rsl-bounds).

##### Impact

La sécurité des bornes implique que l'accès à un objet — notamment un tableau — n'accède pas au-delà de l'allocation mémoire de cet objet.
Cela élimine une grande classe d'erreurs insidieuses et difficiles à trouver, y compris les erreurs (in)fameuses de « débordement de tampon ».
Cela comble également des failles de sécurité ainsi qu'une source majeure de corruption de mémoire (lors d'une écriture hors bornes).
Même si un accès hors bornes est « simplement une lecture », il peut entraîner des violations d'invariants (lorsque l'objet accédé n'est pas du type supposé)
et des « valeurs mystérieuses ».


## <a name="ss-lifetime"></a>Pro.lifetime : Profil de sécurité du cycle de vie

Accéder via un pointeur qui ne pointe vers rien est une source majeure d'erreurs,
et très difficile à éviter dans de nombreux styles de programmation C ou C++ traditionnels.
Par exemple, un pointeur peut être non initialisé, être `nullptr`, pointer au-delà de la plage d'un tableau, ou vers un objet supprimé.

[Consulter la spécification de conception actuelle ici.](https://github.com/isocpp/CppCoreGuidelines/blob/master/docs/Lifetime.pdf)

Résumé du profil de sécurité du cycle de vie :

* <a name="pro-lifetime-invalid-deref"></a>Lifetime.1 : Ne pas déréférencer un pointeur potentiellement invalide :
[détecter ou éviter](010-expr.md#res-deref).

##### Impact

Une fois pleinement appliqué grâce à une combinaison de règles de style, d'analyse statique et de prise en charge par les bibliothèques, ce profil

* élimine l'une des principales sources d'erreurs tenaces en C++
* élimine une source majeure de violations de sécurité potentielles
* améliore les performances en éliminant les vérifications de « paranoïa » redondantes
* augmente la confiance dans la correction du code
* évite les comportements indéfinis en appliquant une règle clé du langage C++
