[![C++ Core Guidelines](cpp_core_guidelines_logo_text.png)](http://Marcussacapuces91.github.io/CppCoreGuidelines/CppCoreGuidelines)

>"Within C++ is a smaller, simpler, safer language struggling to get out."
>-- <cite>Bjarne Stroustrup</cite>

*trad* : Dans le C++, il y a un langage plus petit, plus simple et plus sûr qui lutte pour s'exprimer.

Les [Lignes Directrices Essentielles de C++](CppCoreGuidelines.md) sont un effort collaboratif dirigé par Bjarne Stroustrup, tout comme le langage C++ lui-même. Ils sont le fruit de nombreuses *années-personnes* de discussion et de conception au sein de plusieurs organisations. Leur conception favorise une applicabilité générale et une large adoption, mais ils peuvent être librement copiés et modifiés pour répondre aux besoins de votre organisation.

## Pour commencer

Les recommandations elles-mêmes se trouvent dans [CppCoreGuidelines](CppCoreGuidelines.md). Le document est en [MarkDown compatible avec GitHub](https://github.github.com/gfm/). Il est intentionnellement conservé simple, principalement pour être facile à maintenir et à lire, avec plusieurs versions disponibles :
- une [version originale, non traduite, de référence](https://github.com/isocpp/CppCoreGuidelines/blob/master/CppCoreGuidelines.md) ;
- une [version originale, non traduite, pour navigation](http://isocpp.github.io/CppCoreGuidelines/CppCoreGuidelines).

Notez que cette version web est **traduite** et intégrée manuellement et peut être légèrement plus ancienne que la version de la branche principale et originale du site http://github.com/isocpp/CppCoreGuidelines.

Les Lignes Directrices sont un document qui évolue constamment sans cadence de publication stricte. Bjarne Stroustrup examine périodiquement le document et incrémente le numéro de version dans l'introduction. [Vérifiez le numéro de version actuel](fr/001.main.md) (CppCoreGuidelines.md#intro) et les changements récents dans les dépôts.

De nombreuses Lignes Directrices font appel à la bibliothèque de support GSL (Guidelines Support Library), uniquement en-têtes. Une implémentation est disponible à [GSL: Guidelines Support Library](https://github.com/Microsoft/GSL).

## Contexte et périmètre

L'objectif des recommandations est d'aider les gens à utiliser le C++ moderne de manière efficace. Par "C++ moderne", nous entendons C++11 et versions ultérieures. En d'autres termes, à quoi devrait ressembler votre code dans 5 ans, en partant de maintenant ? Et dans 10 ans ?

Les recommandations se concentrent sur des problèmes relativement de haut niveau, tels que les interfaces, la gestion des ressources, la gestion de la mémoire et la concurrence. De telles règles influencent l'architecture des applications et la conception de bibliothèques. Le respect de ces règles conduit à un code statiquement sûr sur le plan des types, sans fuites de ressources, et qui détecte bien plus d'erreurs logiques que ce qui est courant dans les codes actuels. Et cela fonctionne rapidement — vous pouvez vous permettre de faire les choses correctement.

Nous nous soucions moins des problèmes de bas niveau, tels que les conventions de nommage et le style d'indentation. Toutefois, aucun sujet susceptible d'aider un programmeur n'est hors limites.

Notre ensemble initial de règles met l'accent sur la sécurité (sous diverses formes) et la simplicité. Il se peut très bien qu'elles soient trop strictes. Nous nous attendons à devoir introduire davantage d'exceptions pour mieux s'adapter aux besoins du monde réel. Et nous avons encore besoin de plus de règles.

Vous trouverez certaines de ces règles contraires à vos attentes, voire à votre expérience. Si nous n'avons pas réussi à vous faire changer votre style de codage d'une quelconque manière, nous avons échoué ! Veuillez essayer de vérifier ou de réfuter les règles. En particulier, nous aimerions vraiment que certaines de nos règles soient étayées par des mesures ou de meilleurs exemples.

Vous trouverez certaines règles évidentes, voire triviales. N'oubliez pas qu'un objectif d'une ligne directrice est d'aider quelqu'un qui est moins expérimenté ou qui vient d'un autre contexte ou d'un autre langage à se mettre à niveau.

Les règles sont conçues pour être prises en charge par un outil d'analyse. Les violations des règles seront signalées avec des références (ou des liens) vers la règle concernée. Nous ne pensons pas que vous deviez mémoriser toutes les règles avant d'essayer d'écrire du code.

Les règles sont destinées à une introduction progressive dans une base de code. Nous prévoyons de construire des outils pour cela et espérons que d'autres le feront aussi.

## Contributions et licence

Les commentaires et suggestions d'amélioration sont les bienvenus. Nous prévoyons de modifier et d'étendre ce document au fur et à mesure que notre compréhension s'améliorera et que le langage et l'ensemble des bibliothèques disponibles évolueront. Plus de détails sont disponibles dans [CONTRIBUTING](./CONTRIBUTING.md) et [LICENSE](./LICENSE) (*note* : j'ai volontairement conservé la licence du dépôt original).

Merci à [DigitalOcean](https://www.digitalocean.com/?refcode=32f291566cf7&utm_campaign=Referral_Invite&utm_medium=Referral_Program&utm_source=CopyPaste) pour l'hébergement du site de la Fondation C++ Standard.
