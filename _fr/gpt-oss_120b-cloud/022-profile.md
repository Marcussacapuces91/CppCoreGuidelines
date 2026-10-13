# <a name="s-profile"></a>Pro: Profils

Idéalement, nous suivrions toutes les directives.  
Cela permettrait d'obtenir le code le plus propre, le plus régulier, le moins sujet aux erreurs et souvent le plus rapide.  
Malheureusement, cela est généralement impossible, car nous devons adapter notre code à de grandes bases de code existantes et utiliser des bibliothèques déjà en place.  
Souvent, ce code a été écrit pendant des décennies et ne suit pas ces directives.  
Nous devons viser une [adoption progressive](027-modernizing.md).

Quelle que soit la stratégie d'adoption progressive que nous choisissons, nous devons pouvoir appliquer des ensembles de directives connexes afin de résoudre d'abord un groupe de problèmes et de laisser le reste pour plus tard.  
Une idée similaire d’« directives liées » devient importante lorsqu'une partie, mais pas toutes, les directives sont jugées pertinentes pour une base de code ou lorsqu'un ensemble de directives spécialisées doit être appliqué à un domaine d'application particulier.  
Nous appelons cet ensemble de directives liées un « profil ».  
Nous visons à ce que cet ensemble de directives soit cohérent afin qu'il nous aide à atteindre un objectif précis, tel que « absence d'erreurs de débordement » ou « sécurité statique du type ».  
Chaque profil est conçu pour éliminer une catégorie d'erreurs.  
L'application de règles « aléatoires » isolément est plus susceptible de perturber une base de code que d'apporter une amélioration tangible.

Un « profil » est un ensemble déterministe et applicables de façon portable d’un sous‑ensemble de règles (c’est‑à‑dire de restrictions) conçues pour obtenir une garantie spécifique.  
« Déterministe » signifie qu'elles ne nécessitent qu’une analyse locale et pourraient être implémentées dans un compilateur (sans que cela soit obligatoire).  
« Portable » signifie qu'elles se comportent comme des règles du langage, de sorte que les programmeurs peuvent s’attendre à ce que différents outils d’application donnent la même réponse pour le même code.

Le code écrit pour être exempt d’avertissements en utilisant un tel profil de langage est considéré comme conforme au profil.  
Un code conforme est considéré comme sûr par construction par rapport aux propriétés de sécurité ciblées par ce profil.  
Le code conforme ne sera pas la cause principale d’erreurs pour cette propriété, bien que de telles erreurs puissent être introduites dans un programme par d’autres codes, bibliothèques ou par l’environnement externe.  
Un profil peut également introduire des types de bibliothèque supplémentaires afin de faciliter la conformité et d’encourager un code correct.

Résumé des profils :

* [Pro.type : Sécurité des types](022-profile.md#ss-type)
* [Pro.bounds : Sécurité des limites](022-profile.md#ss-bounds)
* [Pro.lifetime : Sécurité de la durée de vie](022-profile.md#ss-lifetime)

À l’avenir, nous prévoyons de définir de nombreux autres profils et d’ajouter davantage de vérifications aux profils existants.  
Les candidats comprennent :

* promotions/conversions arithmétiques rétrécissantes (probablement parties d’un profil d’arithmétique sûre séparé)
* cast arithmétique d’un point flottant négatif vers un type entier non signé (idem)
* comportement indéfini sélectionné : commencer avec la liste d’UB de Gabriel Dos Reis développée pour le groupe d’étude WG21
* comportement non spécifié sélectionné : prise en compte des problèmes de portabilité.
* violations du `const` : déjà en grande partie gérées par les compilateurs, mais nous pouvons détecter les conversions inappropriées et le sous‑usage du `const`.

L’activation d’un profil est définie par l’implémentation ; généralement, elle se fait dans l’outil d’analyse utilisé.

Pour supprimer l’application d’une vérification de profil, placez une annotation `suppress` sur un contrat de langage. Par exemple :

    [[suppress("bounds")]] char* raw_find(char* p, int n, char x)    // find x in p[0]..p[n - 1]
    {
        // ...
    }

Maintenant, `raw_find()` peut bousculer la mémoire à sa guise.  
Évidemment, la suppression devrait être très rare.

## <a name="ss-type"></a>Pro.safety: Profil de sécurité de type

Ce profil facilite la construction de code qui utilise les types correctement et évite les conversions de type involontaires.  
Il le fait en ciblant les sources principales de violations de type, notamment les usages dangereux de casts et les unions.

Aux fins de cette section, la sécurité de type est définie comme la propriété selon laquelle une variable n’est pas utilisée d’une manière qui ne respecte pas les règles du type de sa définition.  
Une mémoire accédée comme un type `T` ne doit pas être une mémoire valide contenant réellement un objet d’un type sans rapport `U`.  
Notez que la sécurité est censée être complète lorsqu’elle est combinée avec la [sécurité des limites](022-profile.md#ss-bounds) et la [sécurité de la durée de vie](022-profile.md#ss-lifetime).

Une implémentation de ce profil doit reconnaître les modèles suivants dans le code source comme non conformes et émettre un diagnostic.

Résumé du profil de sécurité de type :

* <a name="pro-type-avoidcasts"></a>Type.1 : [Éviter les castings](010-expr.md#res-casts) :
  1. <a name="pro-type-reinterpretcast"></a>Ne pas utiliser `reinterpret_cast` ; version stricte de [Éviter les castings](010-expr.md#res-casts) et [préférer les castings nommés](010-expr.md#res-casts-named).
  2. <a name="pro-type-arithmeticcast"></a>Ne pas utiliser `static_cast` pour les types arithmétiques ; version stricte de [Éviter les castings](010-expr.md#res-casts) et [préférer les castings nommés](010-expr.md#res-casts-named).
  3. <a name="pro-type-identitycast"></a>Ne pas caster entre types de pointeur lorsque le type source et le type cible sont identiques ; version stricte de [Éviter les castings](010-expr.md#res-casts).
  4. <a name="pro-type-implicitpointercast"></a>Ne pas caster entre types de pointeur lorsque la conversion pourrait être implicite ; version stricte de [Éviter les castings](010-expr.md#res-casts).
* <a name="pro-type-downcast"></a>Type.2 : Ne pas utiliser `static_cast` pour un downcast : [Utiliser `dynamic_cast` à la place](007-class.md#rh-dynamic_cast).
* <a name="pro-type-constcast"></a>Type.3 : Ne pas utiliser `const_cast` pour enlever le `const` (c’est‑à‑dire jamais) : [Ne pas enlever le const](010-expr.md#res-casts-const).
* <a name="pro-type-cstylecast"></a>Type.4 : Ne pas utiliser les casts de style C `(T)expression` ou fonctionnels `T(expression)` : préférer [la construction](010-expr.md#res-construct) ou [les castings nommés](010-expr.md#res-casts-named) ou `T{expression}`.
* <a name="pro-type-init"></a>Type.5 : Ne pas utiliser une variable avant qu’elle ne soit initialisée : [toujours initialiser](010-expr.md#res-always).
* <a name="pro-type-memberinit"></a>Type.6 : Toujours initialiser un membre de donnée : [toujours initialiser](010-expr.md#res-always), éventuellement en utilisant [des constructeurs par défaut](007-class.md#rc-default0) ou [des initialiseurs de membres par défaut](007-class.md#rc-in-class-initializer).
* <a name="pro-type-union"></a>Type.7 : Éviter les unions nues : [Utiliser `variant` à la place](007-class.md#ru-naked).
* <a name="pro-type-varargs"></a>Type.8 : Éviter les varargs : [Ne pas utiliser les arguments `va_arg`](006-functions.md#f-varargs).

##### Impact

Avec le profil de sécurité de type, vous pouvez faire confiance au fait que chaque opération s’applique à un objet valide.  
Une exception peut être levée pour indiquer des erreurs qui ne peuvent pas être détectées statiquement (à la compilation).  
Notez que cette sécurité de type ne peut être complète que si nous disposons également de la [sécurité des limites](022-profile.md#ss-bounds) et de la [sécurité de la durée de vie](022-profile.md#ss-lifetime).  
Sans ces garanties, une région de mémoire pourrait être accédée sans tenir compte de quel objet, quels objets ou quelles parties d’objets y sont stockés.

## <a name="ss-bounds"></a>Pro.bounds: Profil de sécurité des limites

Ce profil facilite la construction de code qui opère à l’intérieur des limites des blocs de mémoire alloués.  
Il le fait en ciblant les sources principales de violations de limites : l’arithmétique de pointeurs et l’indexation de tableaux.  
L’une des caractéristiques essentielles de ce profil est de restreindre les pointeurs afin qu’ils ne référencent que des objets uniques, pas des tableaux.

Nous définissons la sécurité des limites comme la propriété selon laquelle un programme n’utilise pas un objet pour accéder à de la mémoire hors de la plage qui a été allouée pour cet objet.  
La sécurité des limites est censée être complète lorsqu’elle est combinée à la [sécurité de type](022-profile.md#ss-type) et à la [sécurité de la durée de vie](022-profile.md#ss-lifetime), qui couvrent d’autres opérations dangereuses pouvant engendrer des violations de limites.

Résumé du profil de sécurité des limites :

* <a name="pro-bounds-arithmetic"></a>Bounds.1 : Ne pas utiliser l’arithmétique de pointeurs. Utiliser `span` à la place : [Passer des pointeurs vers des objets uniques (seulement)](005-interfaces.md#ri-array) et [garder l’arithmétique de pointeurs simple](010-expr.md#res-ptr).
* <a name="pro-bounds-arrayindex"></a>Bounds.2 : Indexer les tableaux uniquement avec des expressions constantes : [Passer des pointeurs vers des objets uniques (seulement)](005-interfaces.md#ri-array) et [garder l’arithmétique de pointeurs simple](010-expr.md#res-ptr).
* <a name="pro-bounds-decay"></a>Bounds.3 : Pas de conversion tableau‑vers‑pointeur : [Passer des pointeurs vers des objets uniques (seulement)](005-interfaces.md#ri-array) et [garder l’arithmétique de pointeurs simple](010-expr.md#res-ptr).
* <a name="pro-bounds-stdlib"></a>Bounds.4 : Ne pas utiliser les fonctions et types de la bibliothèque standard qui ne sont pas vérifiés pour les limites : [Utiliser la bibliothèque standard de manière sûre](018-stdlib.md#rsl-bounds).

##### Impact

La sécurité des limites implique que l’accès à un objet — notamment les tableaux — ne dépasse pas la zone mémoire allouée à cet objet.  
Cela élimine une large classe d’erreurs insidieuses et difficiles à repérer, notamment les fameuses « débordements de tampon ».  
Cela comble des failles de sécurité ainsi qu’une source importante de corruption mémoire (lors d’écritures hors limites).  
Même si un accès hors limites n’est « qu’une lecture », il peut entraîner des violations d’invariants (lorsque l’accès n’est pas du type supposé) et des « valeurs mystérieuses ».

## <a name="ss-lifetime"></a>Pro.lifetime: Profil de sécurité de la durée de vie

L’accès via un pointeur qui ne pointe sur rien est une source majeure d’erreurs, et très difficile à éviter dans de nombreux styles de programmation C ou C++ traditionnels.  
Par exemple, un pointeur peut être non initialisé, être `nullptr`, pointer au‑delà d’un tableau, ou vers un objet supprimé.

[Voir la spécification de conception actuelle ici.](https://github.com/isocpp/CppCoreGuidelines/blob/master/docs/Lifetime.pdf)

Résumé du profil de sécurité de la durée de vie :

* <a name="pro-lifetime-invalid-deref"></a>Lifetime.1 : Ne pas déréférencer un pointeur potentiellement invalide : [détecter ou éviter](010-expr.md#res-deref).

##### Impact

Une fois appliqué complètement grâce à une combinaison de règles de style, d’analyse statique et de support bibliothécaire, ce profil :

* élimine l’une des principales sources d’erreurs subtiles en C++
* élimine une source majeure de potentielles violations de sécurité
* améliore les performances en supprimant les tests de « paranoïa » redondants
* augmente la confiance dans la correction du code
* évite le comportement indéfini en appliquant une règle clé du langage C++