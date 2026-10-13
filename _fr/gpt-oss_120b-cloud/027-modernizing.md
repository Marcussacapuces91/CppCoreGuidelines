# <a name="s-modernizing"></a>Annexe B : Modernisation du code  

Idéalement, nous appliquons toutes les règles à tout le code.  
En pratique, nous devons gérer un grand nombre de code ancien :

* code applicatif écrit avant que les lignes directrices ne soient formulées ou connues  
* bibliothèques écrites selon d’anciennes ou différentes normes  
* code rédigé sous des contraintes « inhabituelles »  
* code que nous n’avons tout simplement pas encore modernisé  

Si nous disposons d’un million de lignes de nouveau code, l’idée de « tout changer d’un coup » est généralement irréaliste.  
Il nous faut donc une méthode pour moderniser progressivement une base de code.

Mettre à jour du code ancien vers un style moderne peut être une tâche ardue.  
Souvent, le code ancien est à la fois un fouillis (difficile à comprendre) et fonctionnel (pour la gamme d’utilisations actuelle).  
Typiquement, le programmeur d’origine n’est plus disponible et les jeux de tests sont incomplets.  
Le fait que le code soit en désordre augmente considérablement l’effort nécessaire pour y apporter toute modification et le risque d’introduire des erreurs.  
Souvent, le code vétuste s’exécute inutilement lentement parce qu’il nécessite d’anciens compilateurs et ne peut profiter du matériel moderne.  
Dans de nombreux cas, un soutien d’outils automatisés de type « modernizer » serait indispensable pour des efforts de mise à jour majeurs.

Le but de la modernisation du code est de simplifier l’ajout de nouvelles fonctionnalités, de faciliter la maintenance et d’accroître les performances (débit ou latence), ainsi que de mieux exploiter le matériel moderne.  
Faire « beau » le code ou « suivre le style moderne » n’est pas en soi une raison suffisante de le changer.  
Chaque modification implique des risques et des coûts (y compris le coût des occasions manquées) liés au fait de posséder une base de code obsolète.  
Les réductions de coûts doivent l’emporter sur les risques.

**Mais comment ?**

Il n’existe pas d’approche unique pour moderniser du code.  
La meilleure méthode dépend du code, de la pression pour les mises à jour, des antécédents des développeurs et des outils disponibles.  
Voici quelques idées (très générales) :

* L’idéal est « mettre à jour tout en un clin d’œil ». Cela apporte le plus d’avantages en un temps total le plus court possible. Dans la plupart des situations, c’est également impossible.  
* Nous pourrions convertir une base de code module par module, mais toute règle qui affecte les interfaces (en particulier les ABI), telle que [utiliser `span`](023-gsl.md#ss-views) @TODO-LINK, ne peut pas être appliquée module par module.  
* Nous pourrions convertir le code « de bas en haut » en commençant par les règles que nous estimons offrir le plus grand bénéfice et/ou le moindre problème dans une base de code donnée.  
* Nous pourrions commencer par nous concentrer sur les interfaces, c’est‑à‑dire nous assurer qu’aucune ressource n’est perdue et qu’aucun pointeur n’est mal utilisé. Cela impliquerait un jeu de changements à travers toute la base de code, mais offrirait très probablement d’énormes bénéfices. Ensuite, le code caché derrière ces interfaces pourrait être modernisé progressivement sans impacter le reste du code.  

Quelle que soit la voie que vous choisissez, notez que les plus grands avantages sont obtenus avec le plus haut degré de conformité aux lignes directrices.  
Les lignes directrices ne sont pas un ensemble aléatoire de règles indépendantes où l’on peut choisir arbitrairement en espérant le succès.

Nous serions ravis d’entendre vos expériences ainsi que les outils que vous avez employés.  
La modernisation peut être beaucoup plus rapide, plus simple et plus sûre lorsqu’elle est soutenue par des outils d’analyse et même des outils de transformation du code.