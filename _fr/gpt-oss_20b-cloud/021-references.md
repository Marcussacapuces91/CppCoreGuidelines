# <a name="s-references"></a>RF: Références

De nombreux

* se concentrent sur les problèmes de bas niveau, tels que l'orthographe des identifiants
* sont écrits par des novices du C++
* considèrent «interdire aux programmeurs de faire des choses inhabituelles» comme leur objectif principal
* visent la portabilité sur de nombreux compilateurs (certains ont plus de 10 ans)
* sont rédigés pour préserver des bases de code datant de plusieurs décennies
* visent un unique domaine d'application
* sont tout à fait contre-productifs
* sont ignorés (doivent être ignorés par les programmeurs pour accomplir efficacement leur travail)

Un mauvais standard de codage est pire qu'aucun standard.  
Cependant, un ensemble approprié de directives est beaucoup meilleur qu'aucun standard : « La forme est libératrice. »

Pourquoi ne pouvons‑nous pas simplement avoir un langage qui permet tout ce que nous voulons et interdit tout ce que nous ne voulons pas (« un langage parfait ») ?

Fondamentalement, car les langages abordables (et leurs chaînes d'outils) servent également des personnes dont les besoins diffèrent des vôtres et répondent à davantage de besoins que ceux dont vous disposez aujourd'hui.  
De plus, vos besoins évoluent dans le temps et un langage généraliste est nécessaire pour vous permettre de vous adapter. Un langage idéal aujourd'hui sera trop restrictif demain.

Les directives de codage adaptent l'utilisation d'un langage aux besoins spécifiques.  
Ainsi, il ne peut pas y avoir d'unique style de codage pour tout le monde.

Sections de référence :

* [RF.rules : Règles de codage](021-references.md#ss-rules)
* [RF.books : Livres avec des directives de codage](021-references.md#ss-books)
* [RF.C++ : Programmation C++ (C++11/C++14/C++17)](021-references.md#ss-cplusplus)
* [RF.web : Sites Web](021-references.md#ss-web)
* [RS.video : Vidéos sur le C++ moderne](021-references.md#ss-vid)
* [RF.man : Manuels](021-references.md#ss-man)
* [RF.core : Matériaux des Directives fondamentales](021-references.md#ss-core)

## <a name="ss-rules"></a>RF.rules: Règles de codage

* [Directives AUTOSAR pour l'utilisation du C++14 dans les systèmes critiques et liés à la sécurité v22.11](https://www.autosar.org/fileadmin/standards/R22-11/AP/AUTOSAR_RS_CPP14Guidelines.pdf) (obsolète, remplacé par [MISRA C++:2023](https://misra.org.uk/product/misra-cpp2023/))
* [Exigences et directives de la bibliothèque Boost](https://www.boost.org/development/requirements.html). ???.
* [Bloomberg : Codage BDE C++] (https://github.com/bloomberg/bde/wiki/CodingStandards.pdf). Met un fort accent sur l'organisation du code et sa mise en page.
* Facebook : ???.
* [Conventions de codage GCC](https://gcc.gnu.org/codingconventions.html).
* [Guide de style C++ de Google](https://google.github.io/styleguide/cppguide.html). Orienté vers C++17 (et également vers de plus anciennes bases de code). Les experts de Google collaborent activement dès maintenant pour aider à améliorer ces règles et, l'espoir, à fusionner les efforts afin qu'elles deviennent un ensemble moderne commun qu'ils pourraient également recommander.
* [JSF++ : Règles de codage C++ pour l'avion de combat JSF] (https://www.stroustrup.com/JSF-AV-rules.pdf). Document numéro 2RDU00001 Rev C. Décembre 2005.  
Pour le logiciel de contrôle de vol.  
Pour le temps réel strict.  
Cela signifie qu'il est nécessairement très restrictif (« si le programme échoue, quelqu'un meurt »).  
Par exemple, aucune allocation ou désallocation de la mémoire libre n'est autorisée après le décollage de l'avion (pas de dépassement de mémoire, pas de fragmentation).  
Aucune exception n'est autorisée (car il n'existe aucun outil disponible pour garantir qu'une exception sera gérée dans un délai fixe et court).  
Les bibliothèques utilisées doivent avoir été approuvées pour les applications critiques.  
Toute similitude avec cet ensemble de directives n'est pas surprenante car Bjarne Stroustrup était un auteur de JSF++.  
Recommandé, mais notez son focus très spécifique.
* [MISRA C++ : Directives d'utilisation de C++17 dans les systèmes critiques](https://misra.org.uk/product/misra-cpp2023/)
* [Utiliser le C++ dans le code Mozilla](https://firefox-source-docs.mozilla.org/code-quality/coding-style/using_cxx_in_firefox_code.html). Comme le nom l'indique, cette démarche vise la portabilité sur de nombreux compilateurs (anciens). En conséquence, elle est restrictive.
* [Geosoft.no : Directives de style de programmation C++] (https://geosoft.no/development/cppstyle.html). ???.
* [Possibility.com : Standard de codage C++] (https://www.possibility.com/Cpp/CppCodingStandard.html). ???.
* [SEI CERT : Standard de codage C++ sécurisé](https://wiki.sei.cmu.edu/confluence/x/Wnw-BQ). Un très ensemble de règles bien faites (avec des exemples et justifications) pour le code sensible à la sécurité. Nombreuses de leurs règles s'appliquent de façon générale.
* [Standard de codage C++ haute intégrité](https://www.codingstandard.com/)
* [llvm](https://llvm.org/docs/CodingStandards.html). Un peu bref, basé sur C++14, et (pas de façon injustifiée) adapté à son domaine.
* ???.

## <a name="ss-books"></a>RF.books: Livres avec des directives de codage

* [Meyers96] Scott Meyers : *More Effective C++*. Addison‑Wesley 1996.
* [Meyers97] Scott Meyers : *Effective C++, Second Edition*. Addison‑Wesley 1997.
* [Meyers01] Scott Meyers : *Effective STL*. Addison‑Wesley 2001.
* [Meyers05] Scott Meyers : *Effective C++, Third Edition*. Addison‑Wesley 2005.
* [Meyers15] Scott Meyers : *Effective Modern C++*. O'Reilly 2015.
* [SuttAlex05] Sutter et Alexandrescu : *C++ Coding Standards*. Addison‑Wesley 2005. Il s'agit davantage d'un ensemble de méta‑règles qu'un ensemble de règles, avant C++11.
* [Stroustrup05] Bjarne Stroustrup : *Une justification pour les langages de bibliothèques semantiquement améliorés* (https://www.stroustrup.com/SELLrationale.pdf). LCSD05. Octobre 2005.
* [Stroustrup14] Stroustrup : *Une visite du C++* (https://www.stroustrup.com/Tour.html). Addison‑Wesley 2014. Chaque chapitre se termine par une section de conseils composée d'un ensemble de recommandations.
* [Stroustrup13] Stroustrup : *The C++ Programming Language (4th Edition)* (https://www.stroustrup.com/4th.html). Addison‑Wesley 2013. Chaque chapitre se termine par une section de conseils composée d'un ensemble de recommandations.
* Stroustrup : *Guide de style* (https://www.stroustrup.com/Programming/PPP-style.pdf) pour [Programming: Principles and Practice using C++] (https://www.stroustrup.com/programming.html). Principalement des règles de nommage et de mise en page de bas niveau. Principalement un outil pédagogique.

## <a name="ss-cplusplus"></a>RF.C++: Programmation C++ (C++11/C++14)

* [TC++PL4](https://www.stroustrup.com/4th.html) : Une description approfondie du langage C++ et des bibliothèques standard pour les programmeurs expérimentés.
* [Tour++](https://www.stroustrup.com/Tour.html) : Une vue d'ensemble du langage C++ et des bibliothèques standard pour les programmeurs expérimentés.
* [Programming: Principles and Practice using C++](https://www.stroustrup.com/programming.html) : Un manuel pour les débutants et novices relatifs.

## <a name="ss-web"></a>RF.web: Sites Web

* [isocpp.org](https://isocpp.org)
* [Pages d'accueil de Bjarne Stroustrup](https://www.stroustrup.com)
* [WG21](https://www.open-std.org/jtc1/sc22/wg21/)
* [Boost](https://www.boost.org)<a name="Boost"></a>
* [Adobe open source](https://opensource.adobe.com/)
* [Bibliothèques Poco](https://pocoproject.org/)
* Sutter's Mill?
* ???.

## <a name="ss-vid"></a>RS.video: Vidéos sur le C++ moderne

* Bjarne Stroustrup : [C++11 Style](https://learn.microsoft.com/en-us/shows/goingnative-2012/keynote-bjarne-stroustrup-cpp11-style). 2012.
* Bjarne Stroustrup : [The Essence of C++ : With Examples in C++84, C++98, C++11, and C++14](https://learn.microsoft.com/en-us/shows/goingnative-2013/opening-keynote-bjarne-stroustrup). 2013.
* Toutes les présentations de [CppCon '14](https://isocpp.org/blog/2014/11/cppcon-videos-c9).
* Bjarne Stroustrup : [The essence of C++](https://www.youtube.com/watch?v=86xWVb4XIyE) à l'Université d'Édimbourg. 2014.
* Bjarne Stroustrup : [The Evolution of C++ Past, Present and Future](https://www.youtube.com/watch?v=_wzc7a3McOs). CppCon 2016 keynote.
* Bjarne Stroustrup : [Make Simple Tasks Simple!](https://www.youtube.com/watch?v=nesCaocNjtQ). CppCon 2014 keynote.
* Bjarne Stroustrup : [Writing Good C++14](https://www.youtube.com/watch?v=1OEu9C51K2A). CppCon 2015 keynote about the Core Guidelines.
* Herb Sutter : [Writing Good C++14… By Default](https://www.youtube.com/watch?v=hEx5DNLWGgA). CppCon 2015 keynote about the Core Guidelines.
* CppCon 15
* ??? C++ Next
* ??? Meting C++
* ??? more …

## <a name="ss-man"></a>RF.man: Manuels

* ISO C++ Standard C++11.
* ISO C++ Standard C++14.
* [ISO C++ Standard C++17](https://www.open-std.org/jtc1/sc22/wg21/docs/papers/2016/n4606.pdf). Draft du comité.
* [Palo Alto "Concepts" TR](https://www.open-std.org/jtc1/sc22/wg21/docs/papers/2012/n3351.pdf).
* [ISO C++ Concepts TS](https://www.open-std.org/jtc1/sc22/wg21/docs/papers/2015/n4553.pdf).
* [WG21 Ranges report](https://www.open-std.org/jtc1/sc22/wg21/docs/papers/2016/n4569.pdf). Rûe de la rédaction.

## <a name="ss-core"></a>RF.core: Matériaux des Directives fondamentales

* [Notre répertoire de documents](https://github.com/isocpp/CppCoreGuidelines/tree/master/docs)
* Stroustrup, Sutter et Dos Reis : *Une brève introduction au modèle de C++ pour la sécurité des types et des ressources* (https://www.stroustrup.com/resource-model.pdf). Un article avec beaucoup d'exemples.
* Sergey Zubkov : Un discours sur les Directives fondamentales et les diapositives (en russe). 2017.
* Neil MacIntosh : La Bibliothèque de Soutien des Directives : Un an plus tard.
* Bjarne Stroustrup : *Writing Good C++14*.
* Herb Sutter : *Writing Good C++14… By Default*.
* Peter Sommerlad : *C++ Core Guidelines – Modernize your C++ Code Base*.
* Bjarne Stroustrup : *No Littering!*.

Il donne une idée du niveau d'ambition pour les Directives fondamentales.  
Notez que les diapositives pour les présentations CppCon sont disponibles (liens vers les vidéos publiées).  
Les contributions à cette liste seraient les bienvenues.

## <a name="ss-ack"></a>Remerciements

* Peter Juhl
* Neil MacIntosh
* Axel Naumann
* Andrew Pardoe
* Gabriel Dos Reis
* Zhuang, Jiangang (Jeff)
* Sergey Zubkov