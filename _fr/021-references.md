## <a name="s-references"></a>RF : Références

De nombreux standards, règles et directives ont été écrits pour le C++, notamment pour l’utilisation spécialisée du C++.

* se concentrent sur des questions de bas niveau, telles que l’orthographe des identificateurs
* sont rédigés par des novices en C++
* considèrent « empêcher les programmeurs de faire des choses inhabituelles » comme leur objectif principal
* visent la portabilité sur de nombreux compilateurs (certains ayant environ 10 ans d’existence)
* sont rédigés pour préserver des bases de code d’époques révolues
* visent un domaine d’application unique
* sont carrément contre-productifs
* sont ignorés (les programmeurs doivent les ignorer pour bien accomplir leur travail)

Un mauvais standard de codage est pire qu’aucun standard.  
Cependant, un ensemble de directives appropriées est bien meilleur qu’aucun standard : « La forme est libératrice. »

Pourquoi ne pouvons‑nous pas simplement avoir un langage qui permette tout ce que nous voulons et interdise tout ce que nous ne voulons pas (« un langage parfait » )?  
Fondamentalement, parce que les langages abordables (et leurs chaînes d’outils) servent également des personnes ayant des besoins différents des vôtres et répondent à davantage de besoins que vous avez aujourd’hui.  
De plus, vos besoins évoluent avec le temps et un langage de but général est nécessaire pour vous permettre de vous adapter.  
Un langage idéal pour aujourd’hui serait trop restrictif demain.

Les directives de codage adaptent l’utilisation d’un langage à des besoins spécifiques.  
Il ne peut donc exister un style de codage unique pour tout le monde.  
Nous nous attendons à ce que différentes organisations ajoutent des règles, généralement avec plus de restrictions et des règles de style plus strictes.

**Sections de référence :**

* [RF.rules : Règles de codage](#ss-rules)
* [RF.books : Livres avec directives de codage](#ss-books)
* [RF.C++ : Programmation C++ (C++11/C++14/C++17)](#ss-cplusplus)
* [RF.web : Sites Web](#ss-web)
* [RS.video : Vidéos sur « le C++ moderne »](#ss-vid)
* [RF.man : Manuels](#ss-man)
* [RF.core : Matériels des Directives de Base](#ss-core)

## <a name="ss-rules"></a>RF.rules : Règles de codage

* [Directives AUTOSAR pour l’utilisation du langage C++14 dans les systèmes critiques et liés à la sécurité v22.11](https://www.autosar.org/fileadmin/standards/R22-11/AP/AUTOSAR_RS_CPP14Guidelines.pdf) (obsolète, remplacé par [MISRA C++:2023](https://misra.org.uk/product/misra-cpp2023/))
* [Exigences et directives de la bibliothèque Boost](https://www.boost.org/development/requirements.html). ??? 
* [Bloomberg : Codage C++ BDE](https://github.com/bloomberg/bde/wiki/CodingStandards.pdf). Met l’accent sur l’organisation et la mise en page du code.
* Facebook : ??? 
* [Conventions de codage GCC](https://gcc.gnu.org/codingconventions.html). C++03 et (raisonnablement) légèrement tourné vers le passé.
* [Guide de style C++ de Google](https://google.github.io/styleguide/cppguide.html). Conçu pour C++17 et (également) pour des bases de code plus anciennes. Les experts de Google collaborent activement ici pour améliorer ces directives, en espérant fusionner les efforts afin qu’elles deviennent un ensemble moderne qu'ils pourraient également recommander.
* [JSF++ : CODAGES DE L'ENSEIGNEMENT C++ JOINT STRIKE FIGHTER AIR VEHICLE](https://www.stroustrup.com/JSF-AV-rules.pdf). Numéro de Document 2RDU00001 Rev C. Décembre 2005. Pour les logiciels de contrôle de vol. Pour le temps réel dur. Cela signifie qu'il est forcément très restrictif (« si le programme échoue, quelqu’un meurt »). Par exemple, aucune allocation ou désallocation en mémoire dynamique n’est autorisée après le décollage (pas de dépassement mémoire et pas de fragmentation). Aucune exception n’est permise (puisqu’il n’existait pas d’outil garantissant qu’une exception serait traitée dans un délai fixe court). Les bibliothèques utilisées doivent avoir été approuvées pour les applications critiques. Toute similitude avec cet ensemble de directives n’est pas surprenante puisque Bjarne Stroustrup a co‑écrit JSF++. Recommandé, mais notez son focus très spécifique.
* [MISRA C++:2023 : Directives pour l’utilisation de C++17 dans les systèmes critiques](https://misra.org.uk/product/misra-cpp2023/)
* [Utiliser C++ dans le code Mozilla](https://firefox-source-docs.mozilla.org/code-quality/coding-style/using_cxx_in_firefox_code.html). Comme son nom l’indique, cela vise la portabilité à travers de nombreux (anciens) compilateurs. En conséquence, c’est restrictif.
* [Geosoft.no : Directives de style de programmation C++](https://geosoft.no/development/cppstyle.html). ??? 
* [Possibility.com : Standard de codage C++](https://www.possibility.com/Cpp/CppCodingStandard.html). ??? 
* [SEI CERT : Standard de codage C++ Sécurisé](https://wiki.sei.cmu.edu/confluence/x/Wnw-BQ). Un ensemble de règles très bien réalisé (avec exemples et raisonnement) destiné aux codes sensibles à la sécurité. Nombre de leurs règles s’appliquent en général.
* [Standard de codage C++ Haute Intégrité](https://www.codingstandard.com/)
* [llvm](https://llvm.org/docs/CodingStandards.html). Un peu bref, basé sur C++14 et (non irréaliste) ajusté à son domaine.
* ??? 

## <a name="ss-books"></a>RF.books : Livres avec directives de codage

* [Meyers96](#Meyers96) Scott Meyers : *Plus efficace C++*. Addison‑Wesley 1996. @TODO-LINK
* [Meyers97](#Meyers97) Scott Meyers : *Effective C++, Second Edition*. Addison‑Wesley 1997. @TODO-LINK
* [Meyers01](#Meyers01) Scott Meyers : *Effective STL*. Addison‑Wesley 2001. @TODO-LINK
* [Meyers05](#Meyers05) Scott Meyers : *Effective C++, Third Edition*. Addison‑Wesley 2005. @TODO-LINK
* [Meyers15](#Meyers15) Scott Meyers : *Effective Modern C++*. O’Reilly 2015. @TODO-LINK
* [SuttAlex05](#SuttAlex05) Sutter et Alexandrescu : *C++ Coding Standards*. Addison‑Wesley 2005. Plus un ensemble de méta‑règles plutôt qu'un ensemble de règles. Avant C++11. @TODO-LINK
* [Stroustrup05](#Stroustrup05) Bjarne Stroustrup : [Une justification pour des langages de bibliothèques enrichies sémantiquement](https://www.stroustrup.com/SELLrationale.pdf). LCSD05. Octobre 2005.
* [Stroustrup14](#Stroustrup05) Stroustrup : [Tour de C++](https://www.stroustrup.com/Tour.html). Addison‑Wesley 2014.
* [Stroustrup13](#Stroustrup13) Stroustrup : [Le Langage de Programmation C++ (4e edition)](https://www.stroustrup.com/4th.html). Addison‑Wesley 2013. Chaque chapitre se termine par une section de conseils comprenant un ensemble de recommandations. @TODO-LINK
* Stroustrup : [Guide de style](https://www.stroustrup.com/Programming/PPP-style.pdf) pour [Programming : Principles and Practice using C++](https://www.stroustrup.com/programming.html). Principalement des règles de nommage et de mise en page de bas niveau. Principalement un outil pédagogique.

## <a name="ss-cplusplus"></a>RF.C++ : Programmation C++ (C++11/C++14)

* [TC++PL4](https://www.stroustrup.com/4th.html) : Une description approfondie du langage C++ et des bibliothèques standard pour les programmeurs expérimentés.
* [Tour++](https://www.stroustrup.com/Tour.html) : Un aperçu du langage C++ et des bibliothèques standard pour les programmeurs expérimentés.
* [Programming : Principles and Practice using C++](https://www.stroustrup.com/programming.html) : Un manuel pour débutants et novices relatifs.

## <a name="ss-web"></a>RF.web : Sites Web

* [isocpp.org](https://isocpp.org)
* [Bjarne Stroustrup’s home pages](https://www.stroustrup.com)
* [WG21](https://www.open-std.org/jtc1/sc22/wg21/)
* [Boost](https://www.boost.org)<a name="Boost"></a>
* [Adobe open source](https://opensource.adobe.com/)
* [Poco libraries](https://pocoproject.org/)
* Sutter’s Mill ?
* ???

## <a name="ss-vid"></a>RS.video : Vidéos sur « le C++ moderne »

* Bjarne Stroustrup : [C++11 Style](https://learn.microsoft.com/en-us/shows/goingnative-2012/keynote-bjarne-stroustrup-cpp11-style). 2012.
* Bjarne Stroustrup : [The Essence of C++ : With Examples in C++84, C++98, C++11, and C++14](https://learn.microsoft.com/en-us/shows/goingnative-2013/opening-keynote-bjarne-stroustrup). 2013
* Tous les talks de [CppCon ’14](https://isocpp.org/blog/2014/11/cppcon-videos-c9)
* Bjarne Stroustrup : [The essence of C++](https://www.youtube.com/watch?v=86xWVb4XIyE) à l’Université d’Édimbourg. 2014.
* Bjarne Stroustrup : [The Evolution of C++ Past, Present and Future](https://www.youtube.com/watch?v=_wzc7a3McOs). CppCon 2016 keynote.
* Bjarne Stroustrup : [Make Simple Tasks Simple!](https://www.youtube.com/watch?v=nesCaocNjtQ). CppCon 2014 keynote.
* Bjarne Stroustrup : [Writing Good C++14](https://www.youtube.com/watch?v=1OEu9C51K2A). CppCon 2015 keynote about the Core Guidelines.
* Herb Sutter : [Writing Good C++14… By Default](https://www.youtube.com/watch?v=hEx5DNLWGgA). CppCon 2015 keynote about the Core Guidelines.
* CppCon 15
* ??? C++ Next
* ??? Meting C++
* ??? plus ???

## <a name="ss-man"></a>RF.man : Manuels

* Norme ISO C++ C++11.
* Norme ISO C++ C++14.
* [Norme ISO C++ C++17](https://www.open-std.org/jtc1/sc22/wg21/docs/papers/2016/n4606.pdf). Version comité.
* [Palo Alto "Concepts" TR](https://www.open-std.org/jtc1/sc22/wg21/docs/papers/2012/n3351.pdf).
* [ISO C++ Concepts TS](https://www.open-std.org/jtc1/sc22/wg21/docs/papers/2015/n4553.pdf).
* [WG21 Ranges report](https://www.open-std.org/jtc1/sc22/wg21/docs/papers/2016/n4569.pdf). Draft.

## <a name="ss-core"></a>RF.core : Matériels des Directives de Base

Cette section contient des matériels utiles pour présenter les Directives de Base et les idées derrière :

* [Notre répertoire de documents](https://github.com/isocpp/CppCoreGuidelines/tree/master/docs)
* Stroustrup, Sutter et Dos Reis : [Une brève introduction au modèle de C++ pour la sécurité des types et des ressources](https://www.stroustrup.com/resource-model.pdf). Un article avec de nombreux exemples.
* Sergey Zubkov : [Un exposé des Directives de Base] et voici les [diapositives](https://www.slideshare.net/slideshow/c-core-guidelines-72335317/72335317). En russe. 2017.
* Neil MacIntosh : [The Guideline Support Library : One Year Later](https://www.youtube.com/watch?v=_GhNnCuaEjo). CppCon 2016.
* Bjarne Stroustrup : [Writing Good C++14](https://www.youtube.com/watch?v=1OEu9C51K2A). CppCon 2015 keynote.
* Herb Sutter : [Writing Good C++14… By Default](https://www.youtube.com/watch?v=hEx5DNLWGgA). CppCon 2015 keynote.
* Peter Sommerlad : [C++ Core Guidelines – Modernize Your C++ Code Base](https://www.youtube.com/watch?v=fQ926v4ZzAM). ACCU 2017.
* Bjarne Stroustrup : [No Littering!](https://www.youtube.com/watch?v=01zI9kV4h8c). Bay Area ACCU 2016.

Il donne une idée du niveau d’ambition des Directives de Base.

Notez que les diapositives des présentations CppCon sont disponibles (liens avec les vidéos publiées).

Les contributions à cette liste sont les bienvenues.

## <a name="ss-ack"></a>Remerciements

Thanks to the many people who contributed rules, suggestions, supporting information, references, etc.:

* Peter Juhl
* Neil MacIntosh
* Axel Naumann
* Andrew Pardoe
* Gabriel Dos Reis
* Zhuang, Jiangang (Jeff)
* Sergey Zubkov

et consultez la liste des contributeurs sur GitHub.