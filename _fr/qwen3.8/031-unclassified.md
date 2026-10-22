# <a name="s-unclassified"></a>À faire : Règles proto non classées

Voici notre liste de tâches.
À terme, les entrées deviendront des règles ou des parties de règles.
À l'alternative, nous déciderons qu'aucun changement n'est nécessaire et supprimerons l'entrée.

* Pas d'amitié à longue distance
* Faut-il aborder la conception physique (ce qui se trouve dans un fichier) et la conception à grande échelle (bibliothèques, groupes de bibliothèques) ?
* Espaces de noms
* Éviter les directives `using` dans la portée globale (sauf pour `std` et d'autres espaces de noms « fondamentaux » (p. ex. `experimental`))
* Quel doit être le degré de granularité des espaces de noms ? Toutes les classes/fonctions conçues pour fonctionner ensemble et publiées ensemble (comme défini par Sutter/Alexandrescu) ou quelque chose de plus étroit ou plus large ?
* Faut-il des espaces de noms en ligne (à la `std::literals::*_literals`) ?
* Éviter les conversions implicites
* Les fonctions membres `const` doivent être sûres pour le multithreading … autrement dit, je ne modifie pas vraiment la variable, je lui assigne simplement une valeur la première fois qu'elle est appelée … argh
* Toujours initialiser les variables, utiliser des listes d'initialisation pour les membres de données.
* Quiconque écrit une interface publique qui prend ou retourne `void*` devrait se faire brûler les orteils. C'est une de mes favorites depuis des années. :)
* Utiliser la qualification `const` partout où c'est possible : fonctions membres, variables et (houphla) `const_iterator`
* Utiliser `auto`
* `(size)` vs. `{initialiseurs}` vs. `{Extent{size}}`
* Ne pas sur-abstraire
* Ne jamais passer un pointeur le long de la pile d'appels
* Retour implicite en fin de fonction
* Faut-il des lignes directrices pour choisir entre les polymorphismes ? OUI. Classique (fonctions virtuelles, sémantique de référence) vs. style Sean Parent (sémantique de valeur, effacement de type, un peu comme `std::function`) vs. CRTP/statique ? OUI. Peut-être même vs. déploiement par étiquette ?
* Faut-il interdire les appels virtuels dans les constructeurs/destructeurs dans vos lignes directrices ? OUI. Beaucoup de gens les interdisent, même si je pense que c'est un grand atout de C++ qu'ils soient préservateurs de ??? (D m'a tellement déçu quand il a pris la voie de Java). QUEL SERAIT UN BON EXEMPLE ?
* En parlant de lambdas, que faudrait-il prendre en compte pour trancher entre lambdas et classes (locales ?) dans les appels d'algorithmes et autres scénarios de rappel ?
* Et en parlant de `std::bind`, Stephen T. Lavavej le critique tellement que je commence à me demander s'il ne va pas s'estomper à l'avenir. Faut-il recommander les lambdas à la place ?
* Que faire des fuites depuis des temporaires ? : `p = (s1 + s2).c_str();`
* Invalidation de pointeurs/itérateurs menant à des pointeurs pendants :

        void bad()
        {
            int* p = new int[700];
            int* q = &p[7];
            delete p;

            vector<int> v(700);
            int* q2 = &v[7];
            v.resize(900);

            // ... utilisation de q et q2 ...
        }

* LSP
* Héritage privé vs. et/ou composition
* Éviter les variables membres statiques de classe (conditions de course, variables quasi globales)

* Utiliser des gardiens de verrou RAII (`lock_guard`, `unique_lock`, `shared_lock`), ne jamais appeler `mutex.lock` et `mutex.unlock` directement (RAII)
* Préférer les verrous non récursifs (souvent utilisés pour contourner un mauvais raisonnement, surcoût)
* Rejoignez vos threads ! (à cause de `std::terminate` dans le destructeur si non rejoints ou détachés … y a-t-il une bonne raison de détacher des threads ?) -- ??? une bibliothèque de support pourrait-elle fournir un wrapper RAII pour `std::thread` ?
* Si deux verrous ou plus doivent être acquis simultanément, utiliser `std::lock` (ou un autre algorithme de prévention des interverrouillages ?)
* Lors de l'utilisation d'un `condition_variable`, toujours protéger la condition par un mutex (un booléen atomique dont la valeur est définie en dehors du mutex est incorrect !), et utiliser le même mutex pour la variable de condition elle-même.
* Ne jamais utiliser `atomic_compare_exchange_strong` avec `std::atomic<structure-utilisateur>` (les différences de bourrage comptent, tandis que `compare_exchange_weak` dans une boucle converge vers un bourrage stable)
* Les objets `shared_future` individuels ne sont pas sûrs pour le multithreading : deux threads ne peuvent pas attendre sur le même objet `shared_future` (ils peuvent attendre sur des copies d'un `shared_future` qui référencent le même état partagé)
* Les objets `shared_ptr` individuels ne sont pas sûrs pour le multithreading : des threads différents peuvent appeler des fonctions membres non `const` sur des `shared_ptr` *différents* qui référencent le même objet partagé, mais un thread ne peut pas appeler une fonction membre non `const` d'un objet `shared_ptr` pendant qu'un autre thread accède à cet même objet `shared_ptr` (si vous en avez besoin, envisagez `atomic_shared_ptr` à la place)

* Règles pour l'arithmétique

---

**Notes de traduction :**

- Aucune référence `#ss-` ni autre ancre interne n'a été détectée dans ce fragment ; l'ancre `<a name="s-unclassified"></a>` est définie localement et ne nécessite pas de `@TODO-LINK`.
- Le bloc de code est indenté de 4 espaces sans balises de code, conformément à la consigne.
- Les termes techniques C++ (`friend`, `using`, `const`, `auto`, `RAII`, `CRTP`, `LSP`, etc.) sont conservés en anglais ou traduits selon l'usage établi en français (ex. « amitié » pour `friend`, « gardien de verrou » pour *lock guard*, « interverrouillage » pour *deadlock*).
