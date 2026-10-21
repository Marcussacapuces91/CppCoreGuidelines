# <a name="s-references"></a>RF : Références

De nombreuses normes, règles et lignes directrices de codage ont été rédigées pour C++, et en particulier pour des usages spécialisés de C++. Beaucoup

* se concentrent sur des problèmes de bas niveau, tels que l'orthographe des identifiants
* sont rédigées par des novices en C++
* visent à « empêcher les programmeurs de faire des choses inhabituelles » comme objectif principal
* visent la portabilité sur de nombreux compilateurs (certains datant d'une dizaine d'années)
* sont rédigées pour préserver des bases de code datant de plusieurs décennies
* visent un seul domaine d'application
* sont carrément contre-productives
* sont ignorées (doivent être ignorées par les programmeurs pour bien faire leur travail)

Une mauvaise norme de codage est pire que l'absence de norme.
Cependant, un ensemble approprié de lignes directrices est bien meilleur que l'absence de norme : « La forme est libératrice. »

Pourquoi ne pas simplement disposer d'un langage qui autorise tout ce que nous voulons et interdit tout ce que nous ne voulons pas (« un langage parfait ») ?
Fondamentalement, parce que les langages abordables (et leurs chaînes d'outils) servent aussi des personnes dont les besoins diffèrent des vôtres et couvrent plus de besoins que ceux que vous avez aujourd'hui.
De plus, vos besoins évoluent avec le temps et un langage généraliste est nécessaire pour vous permettre de vous adapter.
Un langage idéal aujourd'hui serait trop restrictif demain.

Les lignes directrices de codage adaptent l'utilisation d'un langage à des besoins spécifiques.
Ainsi, il ne peut exister qu'un seul style de codage pour tout le monde.
Nous nous attendons à ce que différentes organisations apportent des compléments, généralement avec plus de restrictions et des règles de style plus strictes.

Sections de référence :

* [RF.rules : Règles de codage](021-references.md#ss-rules)
* [RF.books : Livres avec des lignes directrices de codage](021-references.md#ss-books)
* [RF.C++ : Programmation C++ (C++11/C++14/C++17)](021-references.md#ss-cplusplus)
* [RF.web : Sites web](021-references.md#ss-web)
* [RS.video : Vidéos sur le « C++ moderne »](021-references.md#ss-vid)
* [RF.man : Manuels](021-references.md#ss-man)
* [RF.core : Matériaux des Lignes directrices essentielles](021-references.md#ss-core)

## <a name="ss-rules"></a>RF.rules : Règles de codage

* [Lignes directrices AUTOSAR pour l'utilisation du langage C++14 dans les systèmes critiques et liés à la sécurité v22.11](https://www.autosar.org/fileadmin/standards/R22-11/AP/AUTOSAR_RS_CPP14Guidelines.pdf) (obsolète, remplacé par [MISRA C++:2023](https://misra.org.uk/product/misra-cpp2023/))
* [Exigences et lignes directrices de la bibliothèque Boost](https://www.boost.org/development/requirements.html).
  ???.
* [Bloomberg : Codage BDE C++](https://github.com/bloomberg/bde/wiki/CodingStandards.pdf).
  Met un accent particulier sur l'organisation et la mise en page du code.
* Facebook : ???
* [Conventions de codage GCC](https://gcc.gnu.org/codingconventions.html).
  C++03 et (raisonnablement) un peu rétroactif.
* [Guide de style C++ de Google](https://google.github.io/styleguide/cppguide.html).
  Orienté C++17 et (également) bases de code plus anciennes. Les experts de Google collaborent désormais activement ici pour aider à améliorer ces lignes directrices, et espèrent fusionner les efforts afin qu'elles puissent devenir un ensemble commun moderne qu'ils pourraient également recommander.
* [JSF++ : NORMES DE CODAGE C++ POUR L'AÉRONEF JOINT STRIKE FIGHTER](https://www.stroustrup.com/JSF-AV-rules.pdf).
  Document n° 2RDU00001, révision C. Décembre 2005.
  Pour le logiciel de commande de vol.
  Pour le temps réel dur.
  Cela signifie qu'il est nécessairement très restrictif (« si le programme échoue, quelqu'un meurt »).
  Par exemple, aucune allocation ni libération de mémoire libre n'est autorisée après le décollage de l'avion (aucun débordement mémoire ni fragmentation autorisés).
  Aucune exception n'est autorisée (car aucun outil disponible ne permettait de garantir qu'une exception serait gérée dans un court délai fixe).
* Les bibliothèques utilisées doivent avoir été approuvées pour des applications critiques pour la mission.
  Toute ressemblance avec cet ensemble de lignes directrices n'a rien de surprenant, car Bjarne Stroustrup était l'un des auteurs de JSF++.
  Recommandé, mais notez son focus très spécifique.
* [MISRA C++:2023 – Lignes directrices pour l'utilisation de C++17 dans les systèmes critiques](https://misra.org.uk/product/misra-cpp2023/).
* [Utilisation de C++ dans le code Mozilla](https://firefox-source-docs.mozilla.org/code-quality/coding-style/using_cxx_in_firefox_code.html).
  Comme l'indique le nom, cela vise la portabilité sur de nombreux (anciens) compilateurs.
  En tant que tel, il est restrictif.
* [Geosoft.no : Lignes directrices de style de programmation C++](https://geosoft.no/development/cppstyle.html).
  ???.
* [Possibility.com : Norme de codage C++](https://www.possibility.com/Cpp/CppCodingStandard.html).
  ???.
* [SEI CERT : Norme de codage C++ sécurisé](https://wiki.sei.cmu.edu/confluence/x/Wnw-BQ).
  Un ensemble de règles très bien réalisé (avec exemples et justifications), conçu pour le code sensible à la sécurité.
  Beaucoup de leurs règles s'appliquent de manière générale.
* [Norme de codage C++ à haute intégrité](https://www.codingstandard.com/).
* [llvm](https://llvm.org/docs/CodingStandards.html).
  Plutôt concis, basé sur C++14, et (raisonnablement) adapté à son domaine.
* ???

## <a name="ss-books"></a>RF.books : Livres avec des lignes directrices de codage

* [Meyers96](032-bibliography.md#Meyers96) Scott Meyers : *More Effective C++*. Addison-Wesley 1996.
* [Meyers97](032-bibliography.md#Meyers97) Scott Meyers : *Effective C++, Second Edition*. Addison-Wesley 1997.
* [Meyers01](032-bibliography.md#Meyers01) Scott Meyers : *Effective STL*. Addison-Wesley 2001.
* [Meyers05](032-bibliography.md#Meyers05) Scott Meyers : *Effective C++, Third Edition*. Addison-Wesley 2005.
* [Meyers15](032-bibliography.md#Meyers15) Scott Meyers : *Effective Modern C++*. O'Reilly 2015.
* [SuttAlex05](032-bibliography.md#SuttAlex05) Sutter et Alexandrescu : *C++ Coding Standards*. Addison-Wesley 2005. Plutôt un ensemble de méta-règles qu'un ensemble de règles. Antérieur à C++11.
* [Stroustrup05](032-bibliography.md#Stroustrup05) Bjarne Stroustrup : [Une justification pour les langages de bibliothèque sémantiquement enrichis](https://www.stroustrup.com/SELLrationale.pdf).
  LCSD05. Octobre 2005.
* [Stroustrup14](032-bibliography.md#Stroustrup05) Stroustrup : [A Tour of C++](https://www.stroustrup.com/Tour.html).
  Addison-Wesley 2014.
  Chaque chapitre se termine par une section de conseils consistant en un ensemble de recommandations.
* [Stroustrup13](032-bibliography.md#Stroustrup13) Stroustrup : [The C++ Programming Language (4th Edition)](https://www.stroustrup.com/4th.html).
  Addison-Wesley 2013.
  Chaque chapitre se termine par une section de conseils consistant en un ensemble de recommandations.
* Stroustrup : [Guide de style](https://www.stroustrup.com/Programming/PPP-style.pdf)
  pour [Programming: Principles and Practice using C++](https://www.stroustrup.com/programming.html).
  Principalement des règles de bas niveau sur la nomenclature et la mise en page.
  Surtout un outil pédagogique.

## <a name="ss-cplusplus"></a>RF.C++ : Programmation C++ (C++11/C++14)

* [TC++PL4](https://www.stroustrup.com/4th.html) :
Une description approfondie du langage C++ et des bibliothèques standard pour programmeurs expérimentés.
* [Tour++](https://www.stroustrup.com/Tour.html) :
Une vue d'ensemble du langage C++ et des bibliothèques standard pour programmeurs expérimentés.
* [Programming: Principles and Practice using C++](https://www.stroustrup.com/programming.html) :
Un manuel pour débutants et novices.

## <a name="ss-web"></a>RF.web : Sites web

* [isocpp.org](https://isocpp.org)
* [Pages personnelles de Bjarne Stroustrup](https://www.stroustrup.com)
* [WG21](https://www.open-std.org/jtc1/sc22/wg21/)
* [Boost](https://www.boost.org)<a name="Boost"></a>
* [Adobe open source](https://opensource.adobe.com/)
* [Bibliothèques Poco](https://pocoproject.org/)
* Sutter's Mill ?
* ???

## <a name="ss-vid"></a>RS.video : Vidéos sur le « C++ moderne »

* Bjarne Stroustrup : [C++11 Style](https://learn.microsoft.com/en-us/shows/goingnative-2012/keynote-bjarne-stroustrup-cpp11-style). 2012.
* Bjarne Stroustrup : [The Essence of C++: With Examples in C++84, C++98, C++11, and C++14](https://learn.microsoft.com/en-us/shows/goingnative-2013/opening-keynote-bjarne-stroustrup). 2013.
* Toutes les présentations de [CppCon '14](https://isocpp.org/blog/2014/11/cppcon-videos-c9)
* Bjarne Stroustrup : [The essence of C++](https://www.youtube.com/watch?v=86xWVb4XIyE) à l'Université d'Édimbourg. 2014.
* Bjarne Stroustrup : [The Evolution of C++ Past, Present and Future](https://www.youtube.com/watch?v=_wzc7a3McOs). Conférence d'ouverture CppCon 2016.
* Bjarne Stroustrup : [Make Simple Tasks Simple!](https://www.youtube.com/watch?v=nesCaocNjtQ). Conférence d'ouverture CppCon 2014.
* Bjarne Stroustrup : [Writing Good C++14](https://www.youtube.com/watch?v=1OEu9C51K2A). Conférence d'ouverture CppCon 2015 sur les Lignes directrices essentielles.
* Herb Sutter : [Writing Good C++14... By Default](https://www.youtube.com/watch?v=hEx5DNLWGgA). Conférence d'ouverture CppCon 2015 sur les Lignes directrices essentielles.
* CppCon 15
* ??? C++ Next
* ??? Meeting C++
* ??? plus ???

## <a name="ss-man"></a>RF.man : Manuels

* Norme ISO C++ C++11.
* Norme ISO C++ C++14.
* [Norme ISO C++ C++17](https://www.open-std.org/jtc1/sc22/wg21/docs/papers/2016/n4606.pdf). Projet de comité.
* [TR « Concepts » de Palo Alto](https://www.open-std.org/jtc1/sc22/wg21/docs/papers/2012/n3351.pdf).
* [TS Concepts C++ ISO](https://www.open-std.org/jtc1/sc22/wg21/docs/papers/2015/n4553.pdf).
* [Rapport Ranges du WG21](https://www.open-std.org/jtc1/sc22/wg21/docs/papers/2016/n4569.pdf). Brouillon.

## <a name="ss-core"></a>RF.core : Matériaux des Lignes directrices essentielles

Cette section contient des matériaux qui ont été utiles pour présenter les lignes directrices essentielles et les idées qui les sous-tendent :

* [Notre répertoire de documents](https://github.com/isocpp/CppCoreGuidelines/tree/master/docs)
* Stroustrup, Sutter et Dos Reis : [Une brève introduction au modèle C++ pour la sécurité des types et des ressources](https://www.stroustrup.com/resource-model.pdf). Un article riche en exemples.
* Sergey Zubkov : [une présentation sur les Lignes directrices essentielles](https://www.youtube.com/watch?v=DyLwdl_6vmU)
et voici les [diapositives](https://www.slideshare.net/slideshow/c-core-guidelines-72335317/72335317). En russe. 2017.
* Neil MacIntosh : [The Guideline Support Library: One Year Later](https://www.youtube.com/watch?v=_GhNnCuaEjo). CppCon 2016.
* Bjarne Stroustrup : [Writing Good C++14](https://www.youtube.com/watch?v=1OEu9C51K2A). Conférence d'ouverture CppCon 2015.
* Herb Sutter : [Writing Good C++14... By Default](https://www.youtube.com/watch?v=hEx5DNLWGgA). Conférence d'ouverture CppCon 2015.
* Peter Sommerlad : [C++ Core Guidelines - Modernize your C++ Code Base](https://www.youtube.com/watch?v=fQ926v4ZzAM). ACCU 2017.
* Bjarne Stroustrup : [No Littering!](https://www.youtube.com/watch?v=01zI9kV4h8c). Bay Area ACCU 2016.
Elle donne une idée du niveau d'ambition des Lignes directrices essentielles.

Notez que les diapositives des présentations CppCon sont disponibles (liens avec les vidéos publiées).

Les contributions à cette liste seraient les bienvenues.

## <a name="ss-ack"></a>Remerciements

Merci à toutes les personnes qui ont contribué des règles, des suggestions, des informations de soutien, des références, etc. :

* Peter Juhl
* Neil MacIntosh
* Axel Naumann
* Andrew Pardoe
* Gabriel Dos Reis
* Zhuang, Jiangang (Jeff)
* Sergey Zubkov

et consultez la liste des contributeurs sur GitHub.
