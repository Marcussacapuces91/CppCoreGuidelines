# <a name="s-unclassified"></a>À faire : règles prototypes non classées

Ceci est notre liste à faire. À terme, les entrées deviendront des règles ou des parties de règles. Sinon, nous déciderons qu'aucun changement n'est nécessaire et supprimerons l'entrée.

* Pas d'amitié à longue distance
* La conception physique (ce qui se trouve dans un fichier) et la conception à grande échelle (bibliothèques, groupes de bibliothèques) doivent‑elles être abordées ?
* Espaces de noms
* Évitez d'utiliser des directives de portée globale (sauf pour `std`, et d’autres espaces de noms « fondamentaux » (ex. `experimental`))
* À quel niveau granularité les espaces de noms devraient‑ils être ? Toutes les classes/fonctions conçues pour fonctionner ensemble et publiées ensemble (tel que défini dans Sutter/Alexandrescu) ou quelque chose de plus restreint ou plus large ?
* Doit‑on disposer d’espaces de noms en ligne (à la `std::literals::*_literals`) ?
* Évitez les conversions implicites
* Les fonctions membres const devraient être thread‑safe … c’est‑à‑dire qu’on ne modifie pas réellement la variable, on lui assigne simplement une valeur lors de la première invocation… argh
* Initialisez toujours les variables, utilisez des listes d'initialisation pour les membres de données.
* Quiconque rédige une interface publique qui prend ou renvoie `void*` devrait bien sentir la chaleur de la gloire sur ses orteils. C’est l’un de mes privilégiés depuis plusieurs années. :)
* Utilisez le mot‑clé `const` partout où c’est possible : fonctions membres, variables et (félicitations) itérateurs const
* Utilisez `auto`
* `(size)` vs. `{initializers}` vs. `{Extent{size}}`
* Ne pas trop abstraire
* Ne jamais transmettre un pointeur le long de la pile d'appels
* Éviter le passage à travers le bas d'une fonction
* Devrions‑nous avoir des directives pour choisir entre les polymorphismes ? OUI. Classique (fonctions virtuelles, sémantique de référence) vs. style Sean Parent (sémantique par valeur, type-erased, à la `std::function`) vs. CRTP / statique ? OUI. Peut‑être même vs. dispatch par tag
* Les appels virtuels devraient‑ils être interdits dans les constructeurs/détructeurs dans vos directives ? OUI. Beaucoup interdisent, même si je pense que c’est un point fort de C++ que ces appels soient préservés (D m’a déçu quand il suivit la voie Java). Quelle serait une bonne illustration ?
* En ce qui concerne les lambdas, quels critères influencerait la décision entre lambdas et classes (locales ?) dans les appels d'algorithmes et autres scénarios de rappel (callbacks) ?
* En parlant de `std::bind`, Stephen T. Lavavej le critique tellement que je commence à me demander s'il disparaîtra réellement à l'avenir. Les lambdas devraient‑elles être recommandées à la place ?
* Que faire des fuites provenant de temporaires ? : `p = (s1 + s2).c_str();`
* Invalidation de pointeurs/itérateurs menant à des pointeurs pendants :
    void bad()
    {
        int* p = new int[700];
        int* q = &p[7];
        delete p;

        vector<int> v(700);
        int* q2 = &v[7];
        v.resize(900);

        // ... utilisez q et q2 ...
    }
* LSP
* Héritage privé vs membres
* Évitez les variables membres statiques (conditions de course, quasi-variables globales)

* Utilisez les verrous RAII (`lock_guard`, `unique_lock`, `shared_lock`), ne jamais appeler `mutex.lock` et `mutex.unlock` directement (RAII)
* Préférez les verrous non récursifs (souvent utilisés pour contourner de mauvais raisonnements et surcoûts)
* Joignez vos threads ! (car `std::terminate` dans le destructeur s'il n'est pas joint ou détaché ... y a‑t‑il une bonne raison de détacher les threads ?) ?? Une librairie de support pourrait offrir un wrapper RAII pour `std::thread` ?
* Si deux ou plusieurs mutex doivent être acquis simultanément, utilisez `std::lock` (ou un autre algorithme d'évitement de deadlock ?)
* Lorsque vous utilisez une `condition_variable`, protégez toujours la condition par un mutex (la variable booléenne atomique dont la valeur est définie hors mutex est incorrecte !), et utilisez le même mutex pour la variable de condition elle‑même
* Ne jamais utiliser `atomic_compare_exchange_strong` avec `std::atomic<user-defined-struct>` (les différences de remplissage comptent, alors que `compare_exchange_weak` dans une boucle converge vers un remplissage stable)
* Les objets `shared_future` individuels ne sont pas thread‑safe : deux threads ne peuvent pas attendre sur le même objet `shared_future` (ils peuvent attendre sur des copies d'un `shared_future` qui référencent le même état partagé)
* Les objets `shared_ptr` individuels ne sont pas thread‑safe : différents threads peuvent appeler des fonctions membres non `const` sur des `shared_ptr` différents qui se réfèrent au même objet partagé, mais un thread ne peut pas appeler une fonction membre non `const` d'un objet `shared_ptr` pendant qu'un autre thread accède au même objet `shared_ptr` (si vous en avez besoin, envisagez `atomic_shared_ptr`)
* Règles d'arithmétique