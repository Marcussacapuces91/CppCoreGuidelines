# <a name="s-abstract"></a>Abstract

Ce document est un ensemble de lignes directrices pour bien utiliser le C++.  

L'objectif de ce document est d’aider les gens à utiliser le C++ moderne de façon efficace.  

Par « C++ moderne », nous entendons l’utilisation efficace du standard ISO C++ (actuellement C++20, mais la plupart de nos recommandations s’appliquent également à C++17, C++14 et C++11).  

En d’autres termes, à quoi aimeriez‑vous que votre code ressemble dans cinq ans, sachant que vous pouvez commencer dès maintenant ? Et dans dix ans ?  

Les lignes directrices se concentrent sur des sujets relativement généraux, tels que les interfaces, la gestion des ressources, la gestion de la mémoire et la concurrence.  

De telles règles influencent l’architecture des applications et la conception des bibliothèques.  

Suivre ces règles conduit à un code qui assure la sécurité des types à la compilation, évite les fuites de ressources et détecte beaucoup plus d’erreurs de logique que ce qui est courant aujourd’hui.  

Et il sera performant – vous pouvez donc faire les choses correctement.  

Nous sommes moins concernés par les problèmes de bas niveau, tels que les conventions de nommage et le style d'indentation.  

Toutefois, aucun sujet capable d’aider un programmeur ne sort du cadre.  

Notre ensemble initial de règles met l’accent sur la sécurité (de différentes formes) et sur la simplicité.  

Elles pourraient très bien être trop strictes.  

Nous prévoyons d’introduire davantage d’exceptions afin de mieux répondre aux besoins du monde réel.  

Nous avons également besoin de davantage de règles.  

Certaines règles iront à l’encontre de vos attentes, voire de votre expérience.  

Si nous ne vous avons pas suggéré de changer votre style de codage de quelque façon que ce soit, nous avons échoué !  

Essayez de vérifier ou de réfuter les règles !  

En particulier, nous aimerions que certaines de nos règles soient étayées par des mesures ou de meilleurs exemples.  

Certaines règles seront évidentes, voire triviales.  

Gardez à l’esprit qu’un des objectifs d’une directive est d’aider une personne moins expérimentée ou issue d’un autre domaine ou d’un autre langage à se mettre à jour.  

Beaucoup de règles sont conçues pour être prises en charge par un outil d’analyse.  

Les violations seront signalées par des références (ou des liens) vers la règle concernée.  

Nous ne nous attendons pas à ce que vous mémoriez toutes les règles avant d’essayer d’écrire du code.  

Une manière de voir ces lignes directrices est de les considérer comme une spécification pour les outils, tout en restant lisible par les humains.  

Les règles visent à être introduites progressivement dans une base de code.  

Nous prévoyons de développer des outils à cet effet et espérons que d’autres le feront également.  

Les commentaires et suggestions d’amélioration sont les plus bienvenus.  

Nous prévoyons de modifier et d’étendre ce document à mesure que notre compréhension s’améliorera et que le langage ainsi que l’ensemble des bibliothèques disponibles progresseront.