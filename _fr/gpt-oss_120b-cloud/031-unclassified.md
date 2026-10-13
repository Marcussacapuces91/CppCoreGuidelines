# <a name="s-unclassified"></a>À faire : Proto‑règles non classées

Voici notre liste de tâches à faire.  
Finalement, les entrées deviendront des règles ou des parties de règles.  
Sinon, nous déciderons qu’aucun changement n’est nécessaire et nous supprimerons l’entrée.

* Pas d’amitié à distance  
* Faut‑il aborder la conception physique (ce qui se trouve dans un fichier) et la conception à grande échelle (bibliothèques, groupes de bibliothèques) ?  
* Espaces de noms  
* Éviter les directives `using` dans l’espace de noms global (à l’exception de `std` et d’autres espaces de noms « fondamentaux » (p. ex. `experimental`))  
* Quelle granularité doivent avoir les espaces de noms ? Tous les classes/fonctions conçues pour travailler ensemble et être publiées ensemble (comme le définissent Sutter/Alexandrescu) ou quelque chose de plus restreint ou plus large ?  
* Faut‑il introduire des espaces de noms « inline » (à la manière de `std::literals::*_literals`) ?  
* Éviter les conversions implicites  
* Les fonctions membres `const` devraient être thread‑safe … même si je ne modifie pas réellement la variable, je l’initialise la première fois qu’elle est appelée … argh  
* Toujours initialiser les variables, utiliser les listes d’initialisation pour les membres de données.  
* Quiconque écrit une interface publique qui prend ou renvoie `void*` devrait se brûler les pieds. C’est un de mes coups de cœur depuis plusieurs années. :)  
* Utiliser la `const` partout où c’est possible : fonctions membres, variables et (youpi) `const_iterators`  
* Utiliser `auto`  
* `(size)` vs. `{initialisateurs}` vs. `{Extent{size}}`  
* Ne pas sur‑abstraire  
* Ne jamais transmettre un pointeur le long de la pile d’appels  
* Laisser le flux de contrôle atteindre le bas d’une fonction  
* Doit‑on fournir des directives pour choisir entre les différents types de polymorphisme ? OUI. Classique (fonctions virtuelles, sémantique de référence) vs. style Sean Parent (sémantique valeur, type‑effacé, un peu comme `std::function`) vs. CRTP/static ? OUI. Peut‑être même vs. dispatch par tags ?  
* Les appels virtuels doivent‑ils être interdits dans les constructeurs / destructeurs de vos directives ? OUI. Beaucoup les bannissent, même si je pense que c’est une grande force du C++ qu’ils soient … -preserving (D m’a tellement déçu lorsqu’il a suivi la voie Java). **QUEL SERAI‑T‑IL D’UN BON EXEMPLE ?**  
* En parlant de lambdas, quels critères pèsent dans la décision entre les lambdas et les classes (locales ?) dans les appels d’algorithmes et autres scénarios de callbacks ?  
* Et en ce qui concerne `std::bind`, Stephen T. Lavavej le critique tellement que je me demande s’il va effectivement disparaître à l’avenir. Les lambdas doivent‑elles être recommandées à la place ?  
* Que faire des fuites provenant de temporaires ? : `p = (s1 + s2).c_str();`  
* Invalidation de pointeurs/itérateurs entraînant des pointeurs pendants :  

    void bad()
    {
        int* p = new int[700];
        int* q = &p[7];
        delete p;

        vector<int> v(700);
        int* q2 = &v[7];
        v.resize(900);

        // ... use q and q2 ...
    }

* Principe de substitution de Liskov (LSP)  
* Héritage privé vs/et agrégation  
* Éviter les membres de classe statiques (conditions de concurrence, variables quasi‑globales)  

* Utiliser les garde‑fous RAII (`lock_guard`, `unique_lock`, `shared_lock`), ne jamais appeler `mutex.lock` et `mutex.unlock` directement (RAII)  
* Privilégier les verrous non récurrents (souvent employés pour contourner un raisonnement erroné, surcharge)  
* Joignez vos threads ! (sinon `std::terminate` est appelé dans le destructeur si le thread n’est pas joint ou détaché … y a‑t‑il une bonne raison de détacher les threads ?) — ??? Une bibliothèque de support pourrait‑elle fournir un wrapper RAII pour `std::thread` ?  
* Si deux mutex ou plus doivent être acquis simultanément, utilisez `std::lock` (ou un autre algorithme d’évitement de blocage ?)  
* Lors de l’utilisation d’une `condition_variable`, protégez toujours la condition avec un mutex (un booléen atomique dont la valeur serait modifiée en dehors du mutex est erroné !) et utilisez le même mutex pour la variable de condition elle‑même.  
* Ne jamais utiliser `atomic_compare_exchange_strong` avec `std::atomic<user-defined-struct>` (les différences de padding comptent, alors que `compare_exchange_weak` dans une boucle converge vers un padding stable).  
* Les objets `shared_future` individuels ne sont pas thread‑safe : deux threads ne peuvent pas attendre sur le même objet `shared_future` (ils peuvent attendre sur des copies d’un `shared_future` qui référencent le même état partagé).  
* Les objets `shared_ptr` individuels ne sont pas thread‑safe : différents threads peuvent appeler des fonctions membres non‑`const` sur *différents* `shared_ptr` qui référencent le même objet partagé, mais un thread ne peut pas appeler une fonction membre non‑`const` d’un `shared_ptr` pendant qu’un autre thread accède à ce même `shared_ptr` (si vous avez besoin de cela, envisagez `atomic_shared_ptr` à la place).  

* Règles pour l’arithmétique  