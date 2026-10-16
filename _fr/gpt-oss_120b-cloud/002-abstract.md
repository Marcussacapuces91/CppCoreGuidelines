# <a name="s-abstract"></a>Résumé

Ce document est un ensemble de lignes directrices pour bien utiliser C++.

Le but de ce document est d'aider les personnes à exploiter le C++ moderne de façon efficace.
Par « C++ moderne », nous entendons une utilisation efficace de la norme ISO C++ (actuellement C++20, mais presque toutes nos recommandations s'appliquent également à C++17, C++14 et C++11).
En d'autres termes, à quoi aimeriez‑vous que votre code ressemble dans cinq ans, sachant que vous pouvez commencer dès maintenant ? Dans dix ans ?

Les lignes directrices portent principalement sur des problèmes de haut niveau, tels que les interfaces, la gestion des ressources, la gestion de la mémoire et la concurrence.
De telles règles influencent l'architecture des applications et la conception des bibliothèques.
Les suivre conduit à du code statiquement sûr du point de vue du typage, sans fuite de ressources, et qui détecte beaucoup plus d'erreurs logiques que ce qui est habituel aujourd'hui.
Et il s'exécutera rapidement — vous pouvez vous permettre de faire les choses correctement.

Nous nous soucions moins des problèmes de bas niveau, comme les conventions de nommage et le style d'indentation.
Cependant, aucun sujet qui pourrait aider un programmeur n'est hors limites.

Notre jeu de règles initial met l'accent sur la sécurité (sous toutes ses formes) et sur la simplicité.
Il se peut qu'il soit trop strict.
Nous nous attendons à devoir introduire davantage d'exceptions pour mieux répondre aux exigences du monde réel.
Nous avons également besoin de davantage de règles.

Vous trouverez certaines règles contraires à vos attentes, voire à votre expérience.
Si nous ne vous avons pas suggéré de changer votre style de codage d'une quelconque façon, nous avons échoué !
Essayez de vérifier ou d'infirmer les règles !
En particulier, nous aimerions que certaines de nos règles soient étayées par des mesures ou de meilleurs exemples.

D'autres règles vous sembleront évidentes, voire triviales.
Rappelez‑vous qu'un des objectifs d'une ligne directrice est d'aider quelqu'un de moins expérimenté ou issu d'un autre contexte ou d'un autre langage à se mettre à niveau.

De nombreuses règles sont conçues pour être prises en charge par un outil d'analyse.
Les violations de règles seront signalées avec des références (ou des liens) vers la règle concernée.
Nous n'attendons pas que vous mémorisiez toutes les règles avant d'essayer d'écrire du code.
Une façon de concevoir ces lignes directrices est comme une spécification pour des outils qui se lit également par les humains.

Les règles sont destinées à être introduites progressivement dans une base de code.
Nous prévoyons de créer des outils à cet effet et espérons que d'autres le feront également.

Les commentaires et suggestions d'amélioration sont les bienvenus.
Nous prévoyons de modifier et d'étendre ce document à mesure que notre compréhension s'améliore et que le langage ainsi que l'ensemble des bibliothèques disponibles évoluent.
