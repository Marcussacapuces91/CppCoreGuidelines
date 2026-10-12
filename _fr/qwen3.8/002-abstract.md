# <a name="s-abstract"></a>Résumé

Ce document est un ensemble de lignes directrices pour un bon usage de C++.
L'objectif de ce document est d'aider les développeurs à utiliser efficacement le C++ moderne.
Par « C++ moderne », nous entendons un usage efficace de la norme ISO C++ (actuellement C++20, mais la quasi-totalité de nos recommandations s'appliquent également à C++17, C++14 et C++11).
Autrement dit, à quoi aimeriez-vous que votre code ressemble dans 5 ans, sachant que vous pouvez commencer dès aujourd'hui ? Dans 10 ans ?

Les lignes directrices portent sur des problématiques de niveau relativement élevé, telles que les interfaces, la gestion des ressources, la gestion de la mémoire et la concurrence.
Ces règles influencent l'architecture des applications et la conception des bibliothèques.
Leur respect conduit à un code statiquement sûr sur le plan des types, exempt de fuites de ressources, et qui détecte bien plus d'erreurs de logique de programmation que ce que l'on trouve couramment dans les codes actuels.
Et il sera rapide — vous pouvez vous permettre de bien faire.

Nous nous soucions moins des questions de bas niveau, telles que les conventions de nommage et le style d'indentation.
Cependant, aucun sujet susceptible d'être utile au développeur n'est exclu.

Notre ensemble initial de règles met l'accent sur la sécurité (sous différentes formes) et la simplicité.
Elles pourraient fort bien être trop strictes.
Nous prévoyons d'introduire davantage d'exceptions pour mieux répondre aux besoins du monde réel.
Nous avons également besoin de plus de règles.

Vous trouverez certaines règles contraires à vos attentes, voire à votre expérience.
Si nous ne vous avons pas incité à modifier votre style de codage d'aucune manière, nous avons échoué !
Veuillez essayer de vérifier ou d'infirmer nos règles !
En particulier, nous aimerions vivement que certaines d'entre elles soient étayées par des mesures ou de meilleurs exemples.

Vous trouverez certaines règles évidentes, voire triviales.
N'oubliez pas que l'un des objectifs d'une ligne directrice est d'aider une personne moins expérimentée, ou provenant d'un autre domaine ou d'un autre langage, à se mettre à niveau.

De nombreuses règles sont conçues pour être prises en charge par un outil d'analyse.
Les violations seront signalées avec des références (ou des liens) vers la règle concernée.
Nous ne vous demandons pas de mémoriser toutes les règles avant d'essayer d'écrire du code.
Une façon de concevoir ces lignes directrices est de les considérer comme une spécification pour des outils, qui se trouve être lisible par des humains.

Les règles sont destinées à être introduites progressivement dans une base de code.
Nous prévoyons de développer des outils à cet effet et espérons que d'autres feront de même.

Les commentaires et les suggestions d'amélioration sont les bienvenus.
Nous prévoyons de modifier et d'étendre ce document au fur et à mesure que notre compréhension progresse et que le langage ainsi que l'ensemble des bibliothèques disponibles évoluent.

---

**Note de traduction :** Aucune référence `#ss-` ni autre ancre de type `#` n'a été détectée dans ce passage hormis l'ancre `s-abstract` définie localement, qui est donc valide. Aucune balise `@TODO-LINK` n'a été nécessaire.