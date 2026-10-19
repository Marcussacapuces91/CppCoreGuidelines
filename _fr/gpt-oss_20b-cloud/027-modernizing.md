# <a name="s-modernizing"></a>Annexe B : Modernisation du code

Idéalement, nous suivons toutes les règles dans tout le code.  
Réellement, nous devons faire face à beaucoup de code ancien :

* code d'application écrit avant que les directives ne soient formulées ou connues  
* bibliothèques écrites pour des normes plus anciennes / différentes  
* code écrit sous des contraintes « inhabituelles »  
* code que nous n'avons tout simplement pas encore modernisé  

Si nous avons un million de lignes de nouveau code, l'idée de « tout changer d'un coup » est généralement irréaliste.  
Ainsi, nous avons besoin d'une façon de moderniser progressivement une base de code.

Mettre à jour un code ancien vers un style moderne peut être une tâche redoutable.  
Souvent, le vieux code est à la fois un désordre (difficile à comprendre) et fonctionne correctement (pour l'étendue actuelle d'utilisation).  
Typiquement, le programmeur original n'est pas présent et les cas de test sont incomplets.  
Le fait que le code soit un désordre augmente considérablement l'effort nécessaire pour effectuer tout changement et le risque d'introduire des erreurs.  
Souvent, le vieux code désordonné s'exécute inutilement lentement parce qu'il nécessite des compilateurs obsolètes et ne peut pas profiter du matériel moderne.  
Dans de nombreux cas, un support automatisé « modernizer » serait requis pour les efforts de mise à niveau majeurs.

Le but de la modernisation du code est de simplifier l'ajout de nouvelles fonctionnalités, de faciliter la maintenance et d'augmenter les performances (débit ou latence), et d'utiliser mieux le matériel moderne.  
Faire en sorte que le code « ait l'air joli » ou « suive le style moderne » n'est pas, en soi, une raison de changer.  
Il y a des risques implicites à chaque changement et des coûts (y compris le coût des opportunités perdues) implicites à avoir une base de code obsolète.  
Les réductions de coûts doivent l'emporter sur les risques.

Mais comment ?

Il n'existe pas d'approche unique pour moderniser le code.  
La meilleure façon de le faire dépend du code, de la pression pour les mises à jour, des antécédents des développeurs et des outils disponibles.  
Voici quelques idées (très générales) :

* L'idéal est « juste mettre à niveau tout ». Cela donne les plus grands avantages pour le temps total le plus court.  
  Dans la plupart des circonstances, c'est également impossible.  
* Nous pourrions convertir une base de code module par module, mais toute règle qui affecte les interfaces (surtout les ABI), telle que [utiliser `span`](023-gsl.md#ss-views) @TODO-LINK, ne peut pas être faite sur une base par module.  
* Nous pourrions convertir le code « de bas en haut » en commençant par les règles que nous estimons donneront les plus grands avantages et/ou le moindre désagrément dans une base de code donnée.  
* Nous pourrions commencer par nous concentrer sur les interfaces, par exemple, en veillant à ce qu'aucune ressource ne soit perdue et qu'aucun pointeur ne soit mal utilisé.  
  Cela constituerait un ensemble de changements à travers toute la base de code, mais aurait très probablement d'énormes avantages.  
  Ensuite, le code caché derrière ces interfaces peut être modernisé progressivement sans affecter d'autres codes.

Quelle que soit la façon que vous choisissez, notez que les avantages les plus importants viennent avec la plus grande conformité aux directives.  
Les directives ne sont pas un ensemble aléatoire de règles non liées où vous pouvez choisir et choisir au hasard avec une attente de succès.

Nous aimerions beaucoup entendre vos expériences et les outils utilisés.  
La modernisation peut être beaucoup plus rapide, plus simple et plus sûre lorsqu'elle est soutenue par des outils d'analyse et même des outils de transformation de code.
