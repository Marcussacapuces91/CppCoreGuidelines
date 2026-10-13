# <a name="s-references"></a>RF : Références

De nombreuses normes de codage, règles et directives ont été rédigées pour le C++, et notamment pour les usages spécialisés du C++. Beaucoup

* se concentrent sur les problèmes de bas niveau, comme l’orthographe des identifiants,
* sont écrites par des néophytes du C++,
* considèrent que « empêcher les programmeurs de faire des choses inhabituelles » comme leur objectif principal,
* visent la portabilité sur de nombreux compilateurs (certains datant de plus de 10 ans),
* sont rédigées pour préserver des bases de code de plusieurs décennies,
* se focalisent sur un domaine d’application unique,
* sont carrément contre‑productives,
* sont ignorées (les programmeurs doivent les ignorer pour bien faire leur travail).

Une mauvaise norme de codage est pire qu’aucune norme de codage.  
En revanche, un ensemble approprié de directives vaut bien mieux qu’aucune norme : « La forme est libératrice ».

Pourquoi ne pourrions‑nous pas simplement disposer d’un langage qui autorise tout ce que nous voulons et interdit tout ce que nous ne voulons pas (« un langage parfait ») ? Fondamentalement, parce que les langages abordables (et leurs chaînes d’outils) doivent également répondre aux besoins d’autres personnes, différents des vôtres, et satisfaire davantage de besoins que ceux dont vous avez aujourd’hui. De plus, vos besoins évoluent avec le temps et un langage à usage général est nécessaire pour vous permettre de vous adapter. Un langage idéal aujourd’hui serait trop restrictif demain.

Les directives de codage adaptent l’utilisation d’un langage à des besoins spécifiques. Ainsi, il ne peut exister un style de codage unique pour tous. Nous nous attendons à ce que différentes organisations apportent des compléments, généralement avec davantage de restrictions et des règles de style plus strictes.

Sections de références :

* [RF.rules : Règles de codage](021-references.md#ss-rules)
* [RF.books : Livres contenant des directives de codage](021-references.md#ss-books)
* [RF.C++ : Programmation C++ (C++11/C++14)](021-references.md#ss-cplusplus)
* [RF.web : Sites web](021-references.md#ss-web)
* [RS.video : Vidéos sur le « C++ moderne »](021-references.md#ss-vid)
* [RF.man : Manuels](021-references.md#ss-man)
* [RF.core : Matériaux des Core Guidelines](021-references.md#ss-core)

## <a name="ss-rules"></a>RF.rules : Règles de codage

* [Directives AUTOSAR pour l’usage du langage C++14 dans les systèmes critiques et de sécurité v22.11](https://www.autosar.org/fileadmin/standards/R22-11/AP/AUTOSAR_RS_CPP14Guidelines.pdf) (obsolète, remplacées par [MISRA C++ :2023](https://misra.org.uk/product/misra-cpp2023/))
* [Exigences et directives de la bibliothèque Boost](https://www.boost.org/development/requirements.html). ???
* [Bloomberg : BDE C++ Coding](https://github.com/bloomberg/bde/wiki/CodingStandards.pdf). Met un fort accent sur l’organisation du code et la mise en forme.
* Facebook : ???
* [Conventions de codage GCC](https://gcc.gnu.org/codingconventions.html). C++03 et (relativement) un peu rétrograde.
* [Guide de style C++ de Google](https://google.github.io/styleguide/cppguide.html). Conçu pour C++17 et (également) les bases de code plus anciennes. Les experts de Google collaborent désormais activement pour améliorer ces directives, et espèrent fusionner les efforts afin d’obtenir un ensemble commun moderne qu’ils pourraient recommander.
* [JSF++ : JOINT STRIKE FIGHTER AIR VEHICLE C++ CODING STANDARDS](https://www.stroustrup.com/JSF-AV-rules.pdf). Numéro de document 2RDU00001 Rév C. Décembre 2005. Destiné aux logiciels de contrôle de vol. Pour le temps réel strict. Cela signifie qu’il doit être très restrictif (« si le programme échoue, quelqu’un meurt »). Par exemple, aucune allocation ou désallocation dynamique n’est autorisée après le décollage de l’avion (pas de débordement de mémoire et pas de fragmentation). Aucune exception n’est permise (car aucun outil ne pouvait garantir qu’une exception serait traitée dans un laps de temps court fixé). Les bibliothèques utilisées doivent être approuvées pour les applications critiques. Toute ressemblance avec cet ensemble de directives n’est pas surprenante puisque Bjarne Stroustrup a été co‑auteur du JSF++. Recommandé, mais à noter son focus très spécifique.
* [MISRA C++ :2023 – Directives pour l’utilisation du C++17 dans les systèmes critiques](https://misra.org.uk/product/misra-cpp2023/)
* [Utilisation du C++ dans le code de Mozilla](https://firefox-source-docs.mozilla.org/code-quality/coding-style/using_cxx_in_firefox_code.html). Comme son nom l’indique, cela vise la portabilité sur de nombreux compilateurs (anciens). En conséquence, c’est restrictif.
* [Geosoft.no : Directives de style de programmation C++](https://geosoft.no/development/cppstyle.html). ???
* [Possibility.com : Standard de codage C++](https://www.possibility.com/Cpp/CppCodingStandard.html). ???
* [SEI CERT : Standard de codage C++ sécurisé](https://wiki.sei.cmu.edu/confluence/x/Wnw-BQ). Un ensemble de règles très bien réalisé (avec exemples et justifications) destiné au code sensible à la sécurité. Nombre de leurs règles sont d’application générale.
* [Standard de codage High Integrity C++](https://www.codingstandard.com/)
* [llvm](https://llvm.org/docs/CodingStandards.html). Relativement bref, basé sur C++14, et (raisonnablement) adapté à son domaine.
* ???

## <a name="ss-books"></a>RF.books : Livres contenant des directives de codage

* [Meyers96](032-bibliography.md#Meyers96) Scott Meyers : *More Effective C++*. Addison‑Wesley 1996.
* [Meyers97](032-bibliography.md#Meyers97) Scott Meyers : *Effective C++, Second Edition*. Addison‑Wesley 1997.
* [Meyers01](032-bibliography.md#Meyers01) Scott Meyers : *Effective STL*. Addison‑Wesley 2001.
* [Meyers05](032-bibliography.md#Meyers05) Scott Meyers : *Effective C++, Third Edition*. Addison‑Wesley 2005.
* [Meyers15](032-bibliography.md#Meyers15) Scott Meyers : *Effective Modern C++*. O’Reilly 2015.
* [SuttAlex05](032-bibliography.md#SuttAlex05) Sutter et Alexandrescu : *C++ Coding Standards*. Addison‑Wesley 2005. Plus un ensemble de méta‑règles que de règles concrètes. Pré‑C++11.
* [Stroustrup05](032-bibliography.md#Stroustrup05) Bjarne Stroustrup : [A rationale for semantically enhanced library languages](https://www.stroustrup.com/SELLrationale.pdf). LCSD05. Octobre 2005.
* [Stroustrup14](032-bibliography.md#Stroustrup05) Stroustrup : [A Tour of C++](https://www.stroustrup.com/Tour.html). Addison‑Wesley 2014. Chaque chapitre se termine par une section de conseils contenant un ensemble de recommandations.
* [Stroustrup13](032-bibliography.md#Stroustrup13) Stroustrup : [The C++ Programming Language (4th Edition)](https://www.stroustrup.com/4th.html). Addison‑Wesley 2013. Chaque chapitre se termine par une section de conseils contenant un ensemble de recommandations.
* Stroustrup : [Style Guide](https://www.stroustrup.com/Programming/PPP-style.pdf) pour [Programming : Principles and Practice using C++](https://www.stroustrup.com/programming.html). Principalement des règles de nommage et de mise en forme de bas niveau. Principalement un outil d’enseignement.

## <a name="ss-cplusplus"></a>RF.C++ : Programmation C++ (C++11/C++14)

* [TC++PL4](https://www.stroustrup.com/4th.html) : Une description complète du langage C++ et de ses bibliothèques standard pour les programmeurs expérimentés.
* [Tour++](https://www.stroustrup.com/Tour.html) : Un aperçu du langage C++ et des bibliothèques standard destiné aux programmeurs expérimentés.
* [Programming : Principles and Practice using C++](https://www.stroustrup.com/programming.html) : Un manuel pour débutants et novices relatifs.

## <a name="ss-web"></a>RF.web : Sites web

* [isocpp.org](https://isocpp.org)
* [Pages d’accueil de Bjarne Stroustrup](https://www.stroustrup.com)
* [WG21](https://www.open-std.org/jtc1/sc22/wg21/)
* [Boost](https://www.boost.org)<a name="Boost"></a>
* [Adobe open source](https://opensource.adobe.com/)
* [Bibliothèques Poco](https://pocoproject.org/)
* Sutter’s Mill ?
* ???

## <a name="ss-vid"></a>RS.video : Vidéos sur le « C++ moderne »

* Bjarne Stroustrup : [C++11 Style](https://learn.microsoft.com/en-us/shows/goingnative-2012/keynote-bjarne-stroustrup-cpp11-style). 2012.
* Bjarne Stroustrup : [The Essence of C++ : With Examples in C++84, C++98, C++11, and C++14](https://learn.microsoft.com/en-us/shows/goingnative-2013/opening-keynote-bjarne-stroustrup). 2013.
* Toutes les présentations de [CppCon ’14](https://isocpp.org/blog/2014/11/cppcon-videos-c9)
* Bjarne Stroustrup : [The essence of C++](https://www.youtube.com/watch?v=86xWVb4XIyE) à l’Université d’Édinburgh. 2014.
* Bjarne Stroustrup : [The Evolution of C++ Past, Present and Future](https://www.youtube.com/watch?v=_wzc7a3McOs). Discours d’ouverture du CppCon 2016.
* Bjarne Stroustrup : [Make Simple Tasks Simple!](https://www.youtube.com/watch?v=nesCaocNjtQ). Discours d’ouverture du CppCon 2014.
* Bjarne Stroustrup : [Writing Good C++14](https://www.youtube.com/watch?v=1OEu9C51K2A). Discours d’ouverture du CppCon 2015 sur les Core Guidelines.
* Herb Sutter : [Writing Good C++14… By Default](https://www.youtube.com/watch?v=hEx5DNLWGgA). Discours d’ouverture du CppCon 2015 sur les Core Guidelines.
* CppCon 2015
* ??? C++ Next
* ??? Meting C++
* ??? more ???

## <a name="ss-man"></a>RF.man : Manuels

* Norme ISO C++ : C++11.
* Norme ISO C++ : C++14.
* [Norme ISO C++ : C++17](https://www.open-std.org/jtc1/sc22/wg21/docs/papers/2016/n4606.pdf). Projet de comité.
* [Rapport technique « Concepts » de Palo Alto](https://www.open-std.org/jtc1/sc22/wg21/docs/papers/2012/n3351.pdf).
* [TS Concepts C++ ISO](https://www.open-std.org/jtc1/sc22/wg21/docs/papers/2015/n4553.pdf).
* [Rapport WG21 sur les Ranges](https://www.open-std.org/jtc1/sc22/wg21/docs/papers/2016/n4569.pdf). Projet.

## <a name="ss-core"></a>RF.core : Matériaux des Core Guidelines

Cette section regroupe les documents utiles pour présenter les Core Guidelines et les idées qui les sous-tendent :

* [Notre répertoire de documents](https://github.com/isocpp/CppCoreGuidelines/tree/master/docs)
* Stroustrup, Sutter et Dos Reis : [Une brève introduction au modèle C++ de sûreté de type et de ressources](https://www.stroustrup.com/resource-model.pdf). Un article contenant de nombreux exemples.
* Sergey Zubkov : [une présentation sur les Core Guidelines](https://www.youtube.com/watch?v=DyLwdl_6vmU) et voici les [diapositives](https://www.slideshare.net/slideshow/c-core-guidelines-72335317/72335317). En russe. 2017.
* Neil MacIntosh : [The Guideline Support Library : One Year Later](https://www.youtube.com/watch?v=_GhNnCuaEjo). CppCon 2016.
* Bjarne Stroustrup : [Writing Good C++14](https://www.youtube.com/watch?v=1OEu9C51K2A). Discours d’ouverture du CppCon 2015.
* Herb Sutter : [Writing Good C++14… By Default](https://www.youtube.com/watch?v=hEx5DNLWGgA). Discours d’ouverture du CppCon 2015.
* Peter Sommerlad : [C++ Core Guidelines - Modernize your C++ Code Base](https://www.youtube.com/watch?v=fQ926v4ZzAM). ACCU 2017.
* Bjarne Stroustrup : [No Littering!](https://www.youtube.com/watch?v=01zI9kV4h8c). ACCU Bay Area 2016.

Cela donne une idée du niveau d’ambition des Core Guidelines.

Notez que les diapositives des présentations CppCon sont disponibles (liens avec les vidéos publiées).

Les contributions à cette liste sont les bienvenues.

## <a name="ss-ack"></a>Remerciements

Nous remercions les nombreuses personnes ayant contribué aux règles, suggestions, informations de soutien, références, etc. :

* Peter Juhl
* Neil MacIntosh
* Axel Naumann
* Andrew Pardoe
* Gabriel Dos Reis
* Zhuang, Jiangang (Jeff)
* Sergey Zubkov

et consultez la liste des contributeurs sur GitHub.