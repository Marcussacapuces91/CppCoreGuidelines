# <a name="s-abstract"></a>Résumé

Ce document est un ensemble de lignes directrices pour bien utiliser C++.  
L'objectif de ce document est d'aider les développeurs à utiliser efficacement le C++ moderne.  
Par « C++ moderne », nous entendons l'utilisation efficace de la norme ISO C++ (actuellement C++20, mais presque toutes nos recommandations s'appliquent aussi à C++17, C++14 et C++11).  
En d'autres termes : à quoi aimeriez-vous que votre code ressemble dans 5 ans, sachant que vous pouvez commencer maintenant ? Dans 10 ans ?

Les lignes directrices se concentrent sur des aspects relativement haut niveau, tels que les interfaces, la gestion des ressources, la gestion de la mémoire et la concurrence.  
Ces règles influencent l'architecture des applications et la conception des bibliothèques.  
Les suivre conduit à du code sûr au niveau du typage statique, sans fuite de ressources, et qui détecte bien plus d'erreurs logiques que ce qui est courant aujourd'hui.  
Et ce code sera rapide — vous pouvez vous permettre de bien faire les choses.

Nous nous préoccupons moins des aspects bas niveau, tels que les conventions de nommage ou le style d'indentation.  
Cependant, aucun sujet susceptible d'aider un programmeur n'est hors limites.

Notre ensemble initial de règles met l'accent sur la sécurité (sous diverses formes) et la simplicité.  
Elles pourraient très bien être trop strictes.  
Nous nous attendons à devoir introduire davantage d'exceptions pour mieux répondre aux besoins du monde réel.  
Nous avons également besoin de plus de règles.

Vous trouverez certaines règles contraires à vos attentes, voire à votre expérience.  
Si nous ne vous avons pas suggéré de modifier votre style de programmation d'une manière ou d'une autre, nous avons échoué !  
Veuillez essayer de vérifier ou de réfuter les règles !  
En particulier, nous aimerions vraiment que certaines de nos règles soient étayées par des mesures ou de meilleurs exemples.

Vous trouverez certaines règles évidentes, voire triviales.  
Souvenez-vous qu'un des objectifs d'une ligne directrice est d'aider quelqu'un de moins expérimenté ou venant d'un autre contexte ou langage à monter en compétence.

Beaucoup de règles sont conçues pour être prises en charge par un outil d'analyse.  
Les violations seront signalées avec des références (ou des liens) vers la règle concernée.  
Nous ne nous attendons pas à ce que vous mémorisiez toutes les règles avant d'essayer d'écrire du code.  
Une façon de considérer ces lignes directrices est de les voir comme une spécification pour des outils, qui se trouve être lisible par des humains.

Les règles sont destinées à être introduites progressivement dans une base de code.  
Nous prévoyons de construire des outils pour cela, et espérons que d'autres le feront aussi.

Les commentaires et suggestions d'amélioration sont les bienvenus.  
Nous prévoyons de modifier et d'étendre ce document à mesure que notre compréhension progresse et que le langage et l'ensemble des bibliothèques disponibles évoluent.
