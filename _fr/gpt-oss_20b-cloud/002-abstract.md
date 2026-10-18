# <a name="s-abstract"></a>Résumé

Ce document constitue un ensemble de recommandations pour utiliser efficacement le C++.
Son objectif est d'aider les développeurs à exploiter au mieux le C++ moderne.
Par « C++ moderne », nous entendons une utilisation efficace de la norme ISO C++ (actuellement C++20, mais la plupart de nos recommandations s'appliquent également à C++17, C++14 et C++11).
En d'autres termes, à quoi aimeriez-vous que votre code ressemble dans cinq ans, sachant que vous pouvez commencer dès maintenant ? Et dans dix ans ?

Les recommandations se concentrent sur des questions relativement globales, telles que les interfaces, la gestion de ressources, la gestion de mémoire et la concurrence.
Ces règles influencent l'architecture des applications et la conception des bibliothèques.
En les suivant, vous produirez du code à la fois fortement typé, sans fuites de ressources et qui détecte de nombreuses erreurs logiques que l'on trouve couramment dans le code actuel.
En outre, il sera performant : vous pourrez faire les choses correctement sans compromis.

Nous accordons moins d'attention aux détails de bas niveau, tels que les conventions de nommage et le style d'indentation.
Toutefois, aucun sujet utile à un programmeur ne nous est hors de portée.

Notre premier ensemble de règles porte sur la sécurité (multiforme) et la simplicité.
Il se peut qu'elles soient trop strictes.
Nous prévoyons de devoir introduire davantage d'exceptions pour mieux répondre aux besoins du monde réel, et nous aurons également besoin de créer plus de règles.

Il arrivera que certaines règles semblent contre‑voulues ou même contraires à votre expérience.
Si nous ne vous suggérons pas de modifier votre style de programmation de quelque façon que ce soit, alors nous avons échoué !
N'hésitez pas à vérifier ou réfuter les règles !
Nous aimerions particulièrement que certaines de nos règles soient étayées par des mesures ou de meilleurs exemples.

Vous trouverez certains principes évidents ou même triviaux.
Souvenez‑vous qu'un objectif de ce type de directive est d'aider ceux qui sont moins expérimentés ou qui viennent d'un autre environnement ou d'un autre langage à progresser rapidement.

De nombreuses règles sont conçues pour être vérifiées par un outil d'analyse.
Les violations seront signalées avec des références (ou des liens) vers la règle concernée.
Nous ne vous attendons pas à mémoriser toutes les règles avant de tenter d'écrire du code.
Une façon de concevoir ces recommandations est de les traiter comme une spécification d'outils, tout en restant lisible par les humains.

Les règles visent une introduction progressive dans une base de code.
Nous prévoyons de développer des outils pour cela et nous espérons que d'autres s'engageront également à cet égard.

Des commentaires et des suggestions d'amélioration sont les bienvenus.
Nous prévoyons de modifier et d'étendre ce document à mesure que notre compréhension évolue et que le langage ainsi que l'ensemble des bibliothèques disponibles progressent.