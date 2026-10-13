# <a name="s-profile"></a>Profils

Idéalement, nous suivrions toutes les directives. Ce serait le code le plus propre, le plus régulier, le moins sujet aux erreurs, et souvent le plus rapide.

Malheureusement, cela est généralement impossible, car nous devons intégrer notre code dans de grandes bases de code et utiliser des bibliothèques existantes.

Souvent, ce code a été écrit sur plusieurs décennies et ne suit pas ces directives.

Nous devons viser une [adoption progressive](027-modernizing.md).

Quelle que soit la stratégie d'adoption progressive que nous adoptons, nous devons être capables d'appliquer des ensembles de directives liées afin de résoudre d’abord certaines problématiques et de laisser les autres pour plus tard.

Cette idée similaire de « directives liées » devient importante lorsqu’une partie, mais pas toutes, des directives sont jugées pertinentes pour une base de code ou lorsqu’un ensemble de directives spécialisées doit être appliqué à un domaine d’application spécialisé.

Nous appelons un tel ensemble de directives liées un « profil ».

Nous visons que cet ensemble de directives soit cohérent afin de nous aider à atteindre un objectif précis, tel que l’« absence d’erreurs de portée » ou la « sécurité statique des types ».

L'application de règles « aléatoires » isolément est plus susceptible de perturber une base de code qu'apporter une amélioration décisive.

Un « profil » est un ensemble de règles déterministes et applicables portablement (c’est‑à‑dire des restrictions) conçu pour atteindre une garantie précise.  
« Déterministe » signifie qu'elles ne nécessitent qu’une analyse locale et pourraient être implémentées dans un compilateur (though they don't need to be).  
« Appliqué portablement » signifie qu’elles agissent comme des règles de langage; les programmeurs peuvent compter sur différents outils d’application donnant la même réponse pour le même code.

Le code écrit pour être sans avertissement grâce à un tel profil de langage est considéré comme conforme au profil.  
Le code conforme est considéré comme sûr par construction en ce qui concerne les propriétés de sécurité visées par ce profil.  
Le code conforme ne sera pas la cause racine d'erreurs pour cette propriété, même si de telles erreurs peuvent être introduites dans un programme par d'autres code, bibliothèques ou l'environnement externe.

Un profil pourra également introduire des types de bibliothèque supplémentaires pour faciliter la conformité et encourager des codes corrects.

### Profils

* [Pro.type : Sécurité des types](#ss-type)  
* [Pro.bounds : Sécurité des limites](#ss-bounds)  
* [Pro.lifetime : Sécurité de la durée de vie](#ss-lifetime)

**À l'avenir, nous attendons de définir de nombreux autres profils et d'ajouter davantage de vérifications aux profils existants.  
Les candidats incluent :**

* promotions/conversions arithmétiques de réduction (probablement partie d'un profil d'arithmétique sécurisée séparé)  
* conversion arithmétique d'un flottant négatif vers un type entier non signé (idem)  
* comportements indéterminés sélectionnés : commencer par la liste UB de Gabriel Dos Reis développée pour le groupe d'étude WG21  
* comportements non spécifiés sélectionnés : résoudre les soucis de portabilité.  
* violations de `const` : la plupart déjà détectées par les compilateurs, mais nous pouvons intercepter les castings inappropriés et la sous‑utilisation de `const`.

Activer un profil est défini par l'implémentation; typiquement, il est configuré dans l'outil d'analyse utilisé.

Pour supprimer l'application d'un contrôle de profil, placez une annotation `suppress` sur un contrat linguistique. Par exemple :

    [[suppress("bounds")]] char* raw_find(char* p, int n, char x)    // trouver x dans p[0]..p[n - 1]
    {
        // ...
    }


## <a name="ss-type"></a>Pro.safety : Profil de sécurité des types

Ce profil facilite la construction de code qui utilise correctement les types, évitant les punitions de type involontaires.  
Il se concentre sur l'élimination des principales sources de violations de type, notamment les utilisations dangereuses de cast et d'unions.

Pour les besoins de cette section, la sécurité des types se définit comme la propriété qu’une variable n’est pas utilisée d’une manière qui ne respecte pas les règles du type de sa définition.  
Un accès mémoire en tant qu’un type `T` ne doit pas pointer sur une mémoire valide contenant un objet d’un type `U` non lié.  
La sécurité est entendue comme complète lorsqu'elle est combinée également avec la [Sécurité des limites](#ss-bounds) et la [Sécurité de la durée de vie](#ss-lifetime).

Un implémenteur de ce profil doit reconnaître les patterns suivants dans le code source comme non conformes et émettre un diagnostic.

**Résumé du profil de sécurité des types :**

* **Type.1 : [Éviter les casts](#res-casts) @TODO-LINK :**

    1. <a name="pro-type-reinterpretcast"></a>Ne pas utiliser `reinterpret_cast` ; une version stricte de [Éviter les casts](#res-casts) @TODO-LINK et de [Préférer les casts nommés](#res-casts-named) @TODO-LINK.
    2. <a name="pro-type-arithmeticcast"></a>Ne pas utiliser `static_cast` pour les types arithmétiques ; une version stricte de [Éviter les casts](#res-casts) @TODO-LINK et de [Préférer les casts nommés](#res-casts-named) @TODO-LINK.
    3. <a name="pro-type-identitycast"></a>Ne pas caster entre des types pointeurs dont le type source et le type cible sont les mêmes ; une version stricte de [Éviter les casts](#res-casts) @TODO-LINK.
    4. <a name="pro-type-implicitpointercast"></a>Ne pas caster entre des types pointeurs lorsque la conversion pourrait être implicite ; une version stricte de [Éviter les casts](#res-casts) @TODO-LINK.

* **Type.2 : Ne pas utiliser `static_cast` pour le downcast : [Utiliser `dynamic_cast` à la place](#rh-dynamic_cast) @TODO-LINK.**

* **Type.3 : Ne pas utiliser `const_cast` pour enlever `const` (c’est‑à‑dire jamais) : [Ne pas enlever const](#res-casts-const) @TODO-LINK.**

* **Type.4 : Ne pas utiliser les casts de style C `(T)expression` ou fonctionnels `T(expression)` : privilégier [la construction](#res-construct) @TODO-LINK ou [les casts nommés](#res-casts-named) @TODO-LINK ou `T{expression}`.**

* **Type.5 : Ne pas utiliser une variable avant qu'elle ait été initialisée : [Toujours initialiser](#res-always) @TODO-LINK.**

* **Type.6 : Initialiser toujours un membre de données : [Toujours initialiser](#res-always) @TODO-LINK, éventuellement en utilisant [constructeurs par défaut](#rc-default0) @TODO-LINK ou [initialiseurs de membre par défaut](#rc-in-class-initializer) @TODO-LINK.**

* **Type.7 : Éviter les unions non avérées : [Utiliser `variant` à la place](#ru-naked) @TODO-LINK.**

* **Type.8 : Éviter les varargs : [Ne pas utiliser `va_arg`](#f-varargs) @TODO-LINK.**

### Impact

Avec le profil de sécurité des types, vous pouvez avoir confiance que chaque opération est appliquée à un objet valide. Une exception peut être levée pour indiquer des erreurs qui ne peuvent pas être détectées statiquement (au moment de la compilation). Notez que cette sécurité des types ne peut être complète qu'en combinaison avec la [Sécurité des limites](#ss-bounds) et la [Sécurité de la durée de vie](#ss-lifetime).

## <a name="ss-bounds"></a>Pro.bounds : Profil de sécurité des limites

Ce profil facilite la construction de code qui fonctionne à l’intérieur des limites des blocs de mémoire alloués.  
Il le fait en se concentrant sur l’élimination des principales sources de violations de limites : l’arithmétique de pointeurs et l’indexation de tableaux.  
L’une des caractéristiques clés de ce profil est de restreindre les pointeurs à ne référer qu’à des objets uniques, pas à des tableaux.

Nous définissons la sécurité des limites comme la propriété qu'un programme n’utilise pas un objet pour accéder à la mémoire hors de la plage allouée pour celui‑ci.  
La sécurité des limites ne peut être complète qu’en combinaison avec la [Sécurité des types](#ss-type) et la [Sécurité de la durée de vie](#ss-lifetime), qui couvrent d’autres opérations dangereuses pouvant conduire à des violations de limites.

**Résumé du profil de sécurité des limites :**

* **Bounds.1 : Ne pas faire d’arithmétique de pointeurs. Utiliser `span` à la place :**

    [Passer des pointeurs vers des objets uniques (seulement)](#ri-array) @TODO-LINK et [Garder l’arithmétique de pointeurs simple](#res-ptr) @TODO-LINK.

* **Bounds.2 : Indexer uniquement les tableaux avec des expressions constantes :**

    [Passer des pointeurs vers des objets uniques (seulement)](#ri-array) @TODO-LINK et [Garder l’arithmétique de pointeurs simple](#res-ptr) @TODO-LINK.

* **Bounds.3 : Pas de décay tableau-pointeur :**

    [Passer des pointeurs vers des objets uniques (seulement)](#ri-array) @TODO-LINK et [Garder l’arithmétique de pointeurs simple](#res-ptr) @TODO-LINK.

* **Bounds.4 : Ne pas utiliser les fonctions et types de la bibliothèque standard qui ne sont pas vérifiés par les limites :**

    [Utiliser la bibliothèque standard de manière type‑sûre](#rsl-bounds) @TODO-LINK.

### Impact

La sécurité des limites implique que l’accès à un objet — notamment les tableaux — ne dépasse pas la mémoire allouée à cet objet.  
Cela élimine une large classe d’erreurs insidieuses et difficiles à détecter, y compris les tristement célèbres erreurs de dépassement de tampon (« buffer overflow »).  
Cela comble également les failles de sécurité ainsi qu’une source importante de corruption de mémoire (lorsqu’on écrit hors limites).  
Même si un accès hors limites ne fait que lire, il peut provoquer des violations d’invariants (lorsque l’objet accédé n’est pas du type attendu) et des valeurs « mysterious ».

## <a name="ss-lifetime"></a>Pro.lifetime : Profil de sécurité de la durée de vie

Accéder via un pointeur qui ne pointe vers rien constitue une source majeure d’erreurs, et il est très difficile à éviter dans de nombreux styles de programmation C ou C++ traditionnels.  
Par exemple, un pointeur peut être non initialisé, `nullptr`, pointer au-delà de la portée d’un tableau, ou vers un objet supprimé.

[Voir la spécification de conception actuelle ici.](https://github.com/isocpp/CppCoreGuidelines/blob/master/docs/Lifetime.pdf)

### Résumé du profil de sécurité de la durée de vie :

* **Lifetime.1** : Ne pas déréférencer un pointeur potentiellement invalide : [Détecter ou éviter](#res-deref) @TODO-LINK.

### Impact

Une fois complètement appliqué grâce à une combinaison de règles de style, d’analyse statique, et de support de bibliothèque, ce profil

* élimine l’une des sources majeures d’erreurs désagréables en C++  
* élimine une source majeure de violations potentielles de sécurité  
* améliore les performances en éliminant les vérifications de « paranoïa » redondantes  
* augmente la confiance en la correction du code  
* évite le comportement indéfini en appliquant une règle clé du langage C++.