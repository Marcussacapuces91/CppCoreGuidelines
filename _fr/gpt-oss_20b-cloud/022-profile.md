# <a name="s-profile"></a>Pro: Profils

En théorie, nous suivrions toutes les directives.  
Cela garantirait le code le plus propre, le plus régulier, le moins sujet aux erreurs et souvent le plus rapide.  
Malheureusement, cela est généralement impossible car nous devons intégrer notre code dans de grandes bases de code et utiliser des bibliothèques existantes.  
Souvent, un tel code a été écrit pendant des décennies et ne suit pas ces directives.  
Nous devons viser une [adoption progressive](027-modernizing.md).  

Quelle que soit la stratégie d'adoption progressive que nous adoptons, nous devons être capables d'appliquer des ensembles de directives connexes pour résoudre certains problèmes en premier et laisser le reste jusqu'à plus tard.  
Une idée similaire de « directives connexes » devient importante lorsqu'une partie, mais pas la totalité, des directives est jugée pertinente pour une base de code ou lorsqu'un ensemble de directives spécialisées doit être appliqué pour un domaine d'application spécialisé.  
Nous appelons un tel ensemble de directives connexes un « profil ».  
Nous visons à ce que ce type d'ensemble de directives soit cohérent afin qu'il nous aide à atteindre un objectif spécifique, tel que « absence d'erreurs de portée » ou « sécurité statique de type ».  
Chaque profil est conçu pour éliminer une catégorie d'erreurs.  
L'application de règles « aléatoires » isolées est plus susceptible de perturber une base de code qu'elle ne fournit une amélioration définitive.  

Un « profil » est un ensemble de règles déterministes et portables à faire respecter (c'est-à-dire des restrictions) conçu pour atteindre une garantie spécifique.  
Déterministe signifie qu'elles exigent seulement une analyse locale et pourraient être mises en œuvre dans un compilateur (même si ce n'est pas obligatoire).  
Portables à faire respecter signifie qu'ils agissent comme des règles de langage, de sorte que les programmeurs peuvent compter sur différents outils d'application pour donner la même réponse pour le même code.  

Un code écrit pour être exempt d'avertissements en utilisant un tel profil linguistique est considéré comme conforme au profil.  
Le code conforme est considéré comme sûr par construction en ce qui concerne les propriétés de sécurité ciblées par ce profil.  
Le code conforme ne sera pas à l'origine des erreurs pour cette propriété, bien que ces erreurs puissent être introduites dans un programme par d'autres codes, bibliothèques ou l'environnement externe.  
Un profil peut également introduire des types de bibliothèque supplémentaires pour faciliter la conformité et encourager un code correct.  

Résumé des profils :  

* [Pro.type: Sécurité de type](022-profile.md#ss-type)  
* [Pro.bounds: Sécurité des bornes](022-profile.md#ss-bounds)  
* [Pro.lifetime: Sécurité du cycle de vie](022-profile.md#ss-lifetime) @TODO-LINK  

À l'avenir, nous prévoyons de définir de nombreux profils supplémentaires et d'ajouter plus de vérifications aux profils existants.  
Les candidats comprennent :  

* promotions/conversions arithmétiques restrictives (probablement partie d'un profil arithmétique‑sécurisé séparé)  
* conversion arithmétique d'un point flottant négatif vers un type entier non signé (ditto)  
* comportements indéfinis sélectionnés : Commencez par la liste UB de Gabriel Dos Reis développée pour le groupe d'étude WG21  
* comportements non déterminés sélectionnés : traiter les préoccupations de portabilité.  
* violations de `const` : majoritairement déjà prises en charge par les compilateurs, mais nous pouvons détecter les castings inappropriés et la sous‑utilisation de `const`.  

Activer un profil est défini par l'implémentation ; typiquement, il est réglé dans l'outil d'analyse utilisé.  

Pour supprimer l'application d'une vérification de profil, placez une annotation `suppress` sur un contrat de langage. Par exemple :  

    [[suppress("bounds")]] char* raw_find(char* p, int n, char x)    // trouver x dans p[0]..p[n - 1]  
    {  
        // ...  
    }  

Maintenant `raw_find()` peut brouiller la mémoire jusqu'au fond. Évidemment, la suppression doit être très rare.  

## <a name="ss-type"></a>Pro.type: Profil de sécurité de type  

Ce profil facilite la création de code qui utilise correctement les types et évite les pugillages de type involontaires.  
Il le fait en se concentrant sur la suppression des sources principales de violations de type, y compris les utilisations dangereuses de cast et de unions.  

À des fins de cette section, la sécurité de type est définie comme la propriété qu'une variable ne soit pas utilisée d'une manière qui n'obéit pas aux règles du type de sa définition.  
La mémoire accédée comme un type `T` ne doit pas être une mémoire valide qui contient réellement un objet d'un type `U` non apparenté.  
À noter que la sécurité est censée être complète lorsqu'elle est combinée avec [Sécurité des bornes](022-profile.md#ss-bounds) et [Sécurité du cycle de vie](022-profile.md#ss-lifetime).  

Une implémentation de ce profil doit reconnaître les schémas suivants dans le code source comme non conformes et déclencher un diagnostic.  

Résumé du profil de sécurité de type :  

* <a name="pro-type-avoidcasts"></a>Type.1: [Éviter les casts](010-expr.md#res-casts):  

    1. <a name="pro-type-reinterpretcast"></a>N'utilisez pas `reinterpret_cast`; une version stricte de [Éviter les casts](010-expr.md#res-casts) et de [préférer les casts nommés](010-expr.md#res-casts-named).  
    2. <a name="pro-type-arithmeticcast"></a>N'utilisez pas `static_cast` pour les types arithmétiques ; une version stricte de [Éviter les casts](010-expr.md#res-casts) et de [préférer les casts nommés](010-expr.md#res-casts-named).  
    3. <a name="pro-type-identitycast"></a>N'effectuez aucun cast entre des types pointeurs lorsque le type source et le type cible sont identiques ; une version stricte de [Éviter les casts](010-expr.md#res-casts).  
    4. <a name="pro-type-implicitpointercast"></a>N'effectuez pas de cast entre des types pointeurs lorsque la conversion pourrait être implicite ; une version stricte de [Éviter les casts](010-expr.md#res-casts).  
* <a name="pro-type-downcast"></a>Type.2: Ne pas utiliser `static_cast` pour un downcast : [Utilisez `dynamic_cast` à la place](007-class.md#rh-dynamic_cast).  
* <a name="pro-type-constcast"></a>Type.3: Ne pas utiliser `const_cast` pour enlever `const` (c'est‑à‑dire aucunement) : [Ne retirez pas const](010-expr.md#res-casts-const).  
* <a name="pro-type-cstylecast"></a>Type.4: Ne pas utiliser le cast de style C `(T)expression` ou fonctionnel `T(expression)` : Privilégiez [la construction](010-expr.md#res-construct) ou [les casts nommés](010-expr.md#res-casts-named) ou `T{expression}`.  
* <a name="pro-type-init"></a>Type.5: Ne pas utiliser une variable avant qu'elle n'ait été initialisée : [toujours initialiser](010-expr.md#res-always).  
* <a name="pro-type-memberinit"></a>Type.6: Initialisez toujours un membre de données : [toujours initialiser](010-expr.md#res-always), éventuellement en utilisant [les constructeurs par défaut](007-class.md#rc-default0) ou [les initialiseurs de membres par défaut](007-class.md#rc-in-class-initializer).  
* <a name="pro-type-union"></a>Type.7: Évitez les unions nus : [Utilisez `variant` à la place](007-class.md#ru-naked).  
* <a name="pro-type-varargs"></a>Type.8: Évitez les varargs : [Ne pas utiliser les arguments `va_arg`](006-functions.md#f-varargs).  

##### Impact  

Avec le profil de sécurité de type, vous pouvez compter sur le fait que chaque opération est appliquée à un objet valide.  
Une exception peut être levée pour indiquer des erreurs qui ne peuvent pas être détectées statiquement (au moment de la compilation).  
Notez que cette sécurité de type ne peut être complète que si nous avons également [Sécurité des bornes](022-profile.md#ss-bounds) et [Sécurité du cycle de vie](022-profile.md#ss-lifetime).  
Sans ces garanties, une région de mémoire pourrait être accédée indépendamment de l'objet, des objets ou des parties d'objets qui y sont stockés.  

## <a name="ss-bounds"></a>Pro.bounds: Profil de sécurité des bornes  

Ce profil facilite la création de code qui fonctionne dans les limites des blocs de mémoire alloués.  
Il le fait en se concentrant sur la suppression des principales sources de violations de bornes, l'arithmétique des pointeurs et l'indexation des tableaux.  
Une des caractéristiques clés de ce profil est de restreindre les pointeurs à ne faire référence qu'à de simples objets, pas à des tableaux.  

Nous définissons la sécurité des bornes comme la propriété qu'un programme n'utilise pas un objet pour accéder à la mémoire en dehors de la plage qui lui a été allouée.  
La sécurité des bornes est censée être complète uniquement lorsqu'elle est combinée avec [Sécurité des types](022-profile.md#ss-type) et [Sécurité du cycle de vie](022-profile.md#ss-lifetime), qui couvrent d'autres opérations non sécurisées permettant des violations de bornes.  

Résumé du profil de sécurité des bornes :  

* <a name="pro-bounds-arithmetic"></a>Bounds.1: Ne pas utiliser l'arithmétique des pointeurs. Utilisez span à la place : [Passez des pointeurs à des objets uniques (seulement)](005-interfaces.md#ri-array) et [Gardez l'arithmétique des pointeurs simple](010-expr.md#res-ptr).  
*   <a name="pro-bounds-arrayindex"></a>Bounds.2: Indexer uniquement les tableaux avec des expressions constantes :  
[Passez des pointeurs à des objets uniques (seulement)](005-interfaces.md#ri-array) et uniquement…​?  
*   <a name="pro-bounds-decay"></a>Bounds.3: Pas de décay tableau-pointeur :  
*   <a name="pro-bounds-stdlib"></a>Bounds.4: Ne pas utiliser les fonctions et types de la bibliothèque standard qui ne sont pas vérifiés des bornes :  
[Utilisez la bibliothèque standard de façon sécurisée de type…](018-stdlib.md#rsl-bounds)