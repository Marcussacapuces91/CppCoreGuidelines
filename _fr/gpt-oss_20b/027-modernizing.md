# <a name="s-modernizing"></a>Annexe B : Modernisation du code

Idéalement, nous suivons toutes les règles dans tout le code. Réalistiquement, nous devons gérer beaucoup de vieux code :

* le code d'application écrit avant que les directives soient formulées ou connues  
* les bibliothèques écrites selon des standards plus anciens/différents  
* le code écrit sous « contraintes inhabituelles »  
* le code que nous n’avons pas encore eu l’occasion de moderniser  

Si nous avons un million de lignes de nouveau code, l’idée de « changer tout d’un coup » est généralement irréaliste. Il faut donc une méthode progressive pour moderniser une base de code.

Mettre à niveau du code plus ancien vers un style moderne peut sembler une tâche ardue. Souvent, le vieux code est à la fois un désordre (difficile à comprendre) et fonctionne correctement (pour l’usage actuel). Typiquement, le programmeur original n’est plus disponible et les cas de test sont incomplets. Le fait que le code soit désordonné augmente considérablement l’effort nécessaire à toute modification ainsi que le risque d’introduire des erreurs. Souvent, le code désordonné exécute de façon inutilement lente parce que ses dépendances exigent des compilateurs obsolètes et ne peuvent pas exploiter le matériel moderne. Dans de nombreux cas, un support automatisé de type « modernizer » serait requis pour les grands projets de mise à niveau.

La finalité de la modernisation du code est de simplifier l’ajout de nouvelles fonctionnalités, de faciliter la maintenance, d’améliorer les performances (débit ou latence) et de mieux exploiter le matériel moderne. Faire en sorte que le code « ait une belle apparence » ou « suive un style moderne » n’est pas, en soi, une raison de changer. Chaque modification implique des risques et des coûts (y compris le coût des occasions perdues) liés à la présence d’une base de code obsolète. Les économies de coûts doivent l’emporter sur les risques.

Mais comment ?  
Il n’existe pas une approche unique pour moderniser le code. La meilleure façon dépend du code, de la pression pour les mises à jour, du parcours des développeurs et des outils disponibles. Voici des idées assez générales :

* L’idéal est « tout mettre à niveau d’un coup ». Cela apporte le plus de bénéfices pour le temps total le plus court. Dans la plupart des cas, cela est aussi irréalisable.
* Nous pourrions convertir une base de code module par module, mais toute règle qui touche les interfaces (en particulier les ABIs), comme [utiliser `span`](#ss-views) @TODO-LINK, ne peut être effectuée module par module.
* Nous pourrions convertir le code « de bas en haut », en commençant par les règles qui, selon nous, apporteront les plus grands bénéfices ou les moins de difficultés dans une base de code donnée.
* Nous pourrions débuter en nous concentrant sur les interfaces ; par exemple, s’assurer qu’aucune ressource n’est perdue et qu’aucun pointeur n’est mal utilisé. Cela constituerait un ensemble de changements couvrant l’ensemble de la base de code, mais apportant probablement d’immenses bénéfices. Après cela, le code caché derrière ces interfaces peut être modernisé progressivement sans impacter le reste du code.

Peu importe la méthode choisie, il convient de noter que les avantages majeurs résideront dans la conformité maximale aux directives. Les dernières ne constituent pas un ensemble aléatoire de règles non reliées, dans lesquelles il serait possible de sélectionner aléatoirement sans garantie de succès.

Nous aimerions beaucoup connaître vos expériences et les outils que vous avez employés. La modernisation peut être beaucoup plus rapide, plus simple et plus sûre lorsqu’elle est accompagnée d’outils d’analyse, voire de transformations de code.