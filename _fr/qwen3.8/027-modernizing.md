# <a name="s-modernizing"></a>Annexe B : Modernisation du code

Idéalement, nous respectons toutes les règles dans tout le code.
En réalité, nous devons gérer beaucoup de code ancien :

* du code applicatif écrit avant la formulation ou la diffusion des lignes directrices
* des bibliothèques écrites selon des normes plus anciennes ou différentes
* du code écrit sous des contraintes « inhabituelles »
* du code que nous n'avons simplement pas encore eu le temps de moderniser

Si nous disposons d'un million de lignes de code récent, l'idée de « tout changer d'un coup » est généralement irréaliste.
Nous avons donc besoin d'une méthode pour moderniser progressivement une base de code.

La mise à niveau d'un code ancien vers un style moderne peut être une tâche intimidante.
Souvent, le code ancien est à la fois un fouillis (difficile à comprendre) et fonctionnel (pour la plage d'utilisation actuelle).
En général, le développeur d'origine n'est plus là et les cas de test sont incomplets.
Le fait que le code soit un fouillis augmente considérablement l'effort nécessaire pour effectuer toute modification et le risque d'introduire des erreurs.
Souvent, un code ancien en désordre s'exécute inutilement lentement car il nécessite des compilateurs obsolètes et ne peut pas tirer parti du matériel moderne.
Dans de nombreux cas, un support d'outils automatisés de type « modernisateur » serait indispensable pour des efforts de mise à niveau importants.

L'objectif de la modernisation du code est de simplifier l'ajout de nouvelles fonctionnalités, de faciliter la maintenance, d'améliorer les performances (débit ou latence) et de mieux exploiter le matériel moderne.
Rendre le code « joli » ou « conforme au style moderne » ne sont pas, en eux-mêmes, des raisons suffisantes pour le modifier.
Chaque modification implique des risques, et le fait de conserver une base de code obsolète implique des coûts (y compris le coût des opportunités perdues).
Les réductions de coûts doivent l'emporter sur les risques.

Mais comment faire ?

Il n'existe pas une seule approche pour moderniser un code.
La meilleure façon de procéder dépend du code, de la pression pour les mises à jour, du profil des développeurs et des outils disponibles.
Voici quelques idées (très générales) :

* L'idéal serait de « tout mettre à jour d'un coup ». Cela offre les bénéfices les plus importants pour un temps total minimal.
  Dans la plupart des circonstances, c'est aussi impossible.
* Nous pourrions convertir une base de code module par module, mais toute règle affectant les interfaces (en particulier les ABI), telle que [utiliser `span`](023-gsl.md#ss-views) @TODO-LINK, ne peut pas être appliquée module par module.
* Nous pourrions convertir le code « de bas en haut », en commençant par les règles que nous estimons apporter les plus grands avantages et/ou le moins de difficultés dans une base de code donnée.
* Nous pourrions commencer par nous concentrer sur les interfaces, par exemple, nous assurer qu'aucune ressource n'est perdue et qu'aucun pointeur n'est mal utilisé.
  Cela constituerait un ensemble de modifications à travers toute la base de code, mais aurait très probablement des avantages considérables.
  Par la suite, le code masqué derrière ces interfaces peut être progressivement modernisé sans affecter le reste du code.

Quelle que soit l'approche choisie, veuillez noter que les avantages les plus importants sont liés au plus haut degré de conformité aux lignes directrices.
Les lignes directrices ne constituent pas un ensemble aléatoire de règles sans rapport entre elles, où l'on pourrait choisir au hasard en espérant un résultat positif.

Nous serions ravis d'apprendre les retours d'expérience et les outils utilisés.
La modernisation peut être beaucoup plus rapide, plus simple et plus sûre lorsqu'elle est soutenue par des outils d'analyse et même des outils de transformation de code.

---

**Note de traduction :** Le lien `[utiliser `span`](023-gsl.md#ss-views)` pointe vers un fichier externe (`023-gsl.md`) dont la cible `#ss-views` ne peut pas être vérifiée dans le document fourni. Un marqueur `@TODO-LINK` a été ajouté à proximité pour signalement.
