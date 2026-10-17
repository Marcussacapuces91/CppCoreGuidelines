# <a name="s-abstract"></a>Résumé

Ce document est un ensemble de directives pour un bon usage de C++.
L'objectif est d'aider les développeurs à utiliser efficacement le C++ moderne.
Par « C++ moderne », nous entendons une utilisation efficace de la norme ISO C++ (actuellement C++20, mais la quasi-totalité de nos recommandations s'appliquent également à C++17, C++14 et C++11).
En d'autres termes, à quoi aimeriez-vous que votre code ressemble dans 5 ans, sachant que vous pouvez commencer dès maintenant ? Et dans 10 ans ?

Les directives se concentrent sur des sujets de niveau relativement élevé, tels que les interfaces, la gestion des ressources, la gestion de la mémoire et la concurrence.
De telles règles influencent l'architecture des applications et la conception des bibliothèques.
Leur respect aboutira à un code statiquement sûr sur le plan des types, sans fuite de ressources, et qui détectera bien plus d'erreurs de logique que ce que l'on observe généralement dans le code actuel.
Et il sera rapide — vous pouvez vous permettre de bien faire les choses.

Nous accordons moins d'attention aux questions de bas niveau, telles que les conventions de nommage et le style d'indentation.
Cependant, aucun sujet susceptible d'aider un développeur n'est exclu.

Notre ensemble initial de règles met l'accent sur la sécurité (sous diverses formes) et la simplicité.
Elles sont sans doute trop strictes.
Nous prévoyons d'introduire davantage d'exceptions pour mieux répondre aux besoins concrets.
Nous avons également besoin de plus de règles.

Vous trouverez certaines règles contraires à vos attentes, voire à votre expérience.
Si nous n'avons pas cherché à vous inciter, d'une façon ou d'une autre, à modifier votre style de programmation, nous avons échoué !
Veuillez essayer de vérifier ou de réfuter les règles !
En particulier, nous aimerions vivement voir certaines d'entre elles étayées par des mesures ou de meilleurs exemples.

Vous trouverez certaines règles évidentes, voire triviales.
N'oubliez pas qu'un des buts d'une directive est d'aider une personne moins expérimentée, ou venant d'un domaine ou d'un langage différent, à s'intégrer rapidement.

De nombreuses règles sont conçues pour être détectées par un outil d'analyse.
Les violations seront signalées avec des références (ou des liens) vers la règle correspondante.
Nous n'attendons pas que vous mémorisiez toutes les règles avant de commencer à écrire du code.
On peut voir ces directives comme la spécification d'outils qui se trouve aussi être lisible par des humains.

Les règles sont conçues pour être introduites progressivement dans un code existant.
Nous prévoyons de créer des outils à cet effet et espérons que d'autres en feront de même.

Les commentaires et suggestions d'amélioration sont les bienvenus.
Nous prévoyons de modifier et d'étendre ce document à mesure que notre compréhension progresse et que le langage ainsi que l'ensemble des bibliothèques disponibles évoluent.

---
*Note : aucune référence interne `#ss-` n'est présente dans cette section. L'ancre `#s-abstract` est auto-référente et valide.*