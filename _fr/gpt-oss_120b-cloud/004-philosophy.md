# <a name="s-philosophy"></a>P : Philosophie

Les règles de cette section sont très générales.

**Résumé des règles philosophiques :**

* [P.1 : Exprimer les idées directement dans le code](004-philosophy.md#rp-direct)
* [P.2 : Écrire en C++ ISO standard](004-philosophy.md#rp-cplusplus)
* [P.3 : Exprimer l'intention](004-philosophy.md#rp-what)
* [P.4 : Idéalement, un programme devrait être statiquement sûr du typage](004-philosophy.md#rp-typesafe)
* [P.5 : Privilégier la vérification à la compilation à la vérification à l'exécution](004-philosophy.md#rp-compile-time)
* [P.6 : Ce qui ne peut pas être vérifié à la compilation doit être vérifiable à l'exécution](004-philosophy.md#rp-run-time)
* [P.7 : Détecter les erreurs d'exécution tôt](004-philosophy.md#rp-early)
* [P.8 : Ne pas laisser fuir de ressources](004-philosophy.md#rp-leak)
* [P.9 : Ne pas gaspiller de temps ou d'espace](004-philosophy.md#rp-waste)
* [P.10 : Privilégier les données immuables aux données mutables](004-philosophy.md#rp-mutable)
* [P.11 : Encapsuler les constructions désordonnées plutôt que de les disperser dans le code](004-philosophy.md#rp-library)
* [P.12 : Utiliser les outils d'aide appropriés](004-philosophy.md#rp-tools)
* [P.13 : Utiliser les bibliothèques de soutien appropriées](004-philosophy.md#rp-lib)

Les règles philosophiques ne sont généralement pas vérifiables mécaniquement.
Cependant, les règles individuelles reflétant ces thèmes philosophiques le sont.
Sans base philosophique, les règles plus concrètes / spécifiques / vérifiables manquent de justification.

---

### <a name="rp-direct"></a>P.1 : Exprimer les idées directement dans le code

##### Raison

Les compilateurs ne lisent pas les commentaires (ou les documents de conception) et de même beaucoup de programmeurs ne le font pas (de façon constante). Ce qui est exprimé dans le code possède une sémantique définie et peut (en principe) être vérifié par les compilateurs et d'autres outils.

##### Exemple

    class Date {
    public:
        Month month() const;  // à faire
        int month();          // à ne pas faire
        // ...
    };

La première déclaration de `month` indique explicitement qu'elle renvoie un `Month` et qu'elle ne modifie pas l'état de l'objet `Date`.  
La seconde version laisse le lecteur deviner et ouvre davantage de possibilités de bogues non détectés.

##### Exemple, mauvais

Cette boucle est une forme restreinte de `std::find` :

    void f(vector<string>& v)
    {
        string val;
        cin >> val;
        // ...
        int index = -1;                    // mauvais, de plus devrait utiliser gsl::index
        for (int i = 0; i < v.size(); ++i) {
            if (v[i] == val) {
                index = i;
                break;
            }
        }
        // ...
    }

##### Exemple, bon

Une expression beaucoup plus claire de l'intention serait :

    void f(vector<string>& v)
    {
        string val;
        cin >> val;
        // ...
        auto p = find(begin(v), end(v), val);  // meilleur
        // ...
    }

Une bibliothèque bien conçue exprime l'intention (ce qui doit être fait, plutôt que simplement comment quelque chose est fait) bien mieux que l'utilisation directe des caractéristiques du langage.

Un programmeur C++ devrait connaître les bases de la bibliothèque standard et l'utiliser quand il le faut.
Tout programmeur devrait connaître les bases des bibliothèques fondamentales du projet sur lequel il travaille et les utiliser de manière appropriée.
Tout programmeur qui suit ces lignes directrices devrait connaître la [bibliothèque d'assistance aux lignes directrices](#gsl-guidelines-support-library) @TODO‑LINK et l'utiliser correctement.

##### Exemple

    change_speed(double s);   // mauvais : que signifie s ?
    // ...
    change_speed(2.3);

Une meilleure approche consiste à être explicite quant à la signification du `double` (nouvelle vitesse ou variation de la vitesse ?) et à l'unité utilisée :

    change_speed(Speed s);    // meilleur : la signification de s est spécifiée
    // ...
    change_speed(2.3);        // erreur : aucune unité
    change_speed(23_m / 10s); // mètres par seconde

Nous aurions pu accepter un `double` « nu » comme variation, mais cela aurait été source d'erreurs.
Si nous voulions à la fois la vitesse absolue et les variations, nous aurions défini un type `Delta`.

##### Application

Très difficile en général.

* utiliser `const` de façon cohérente (vérifier si les fonctions membres modifient leur objet ; vérifier si les fonctions modifient les arguments passés par pointeur ou référence)  
* signaler les usages de casts (les casts neutralisent le système de types)  
* détecter le code qui imite la bibliothèque standard (difficile)

---

### <a name="rp-cplusplus"></a>P.2 : Écrire en C++ ISO standard

##### Raison

Il s'agit d'un ensemble de lignes directrices pour écrire du C++ ISO standard.

##### Note

Il existe des environnements où les extensions sont nécessaires, par exemple pour accéder à des ressources système.
Dans ces cas, il faut localiser l'usage des extensions requises et contrôler leur utilisation avec des « Coding Guidelines » non‑core.
Si possible, concevez des interfaces qui encapsulent les extensions afin qu'elles puissent être désactivées ou compilées hors du code sur les systèmes qui ne les supportent pas.

Les extensions n'ont souvent pas de sémantique rigoureusement définie. Même les extensions courantes et implémentées par plusieurs compilateurs peuvent présenter des comportements légèrement différents et des cas limites en raison du **manque** d'une définition normative stricte. Une utilisation suffisante de l'une de ces extensions affectera la portabilité attendue.

##### Note

Utiliser du C++ ISO valide ne garantit pas la portabilité (et encore moins la correction).
Évitez de dépendre d'un comportement indéfini (par ex. : [ordre d'évaluation indéfini](010-expr.md#res-order)) et soyez conscient des constructions à signification d'implémentation (par ex. : `sizeof(int)`).

##### Note

Il existe des environnements où des restrictions sur l'usage des fonctionnalités du langage C++ standard ou de la bibliothèque standard sont nécessaires, par exemple pour éviter l'allocation dynamique de mémoire imposée par les standards de logiciels de commande d'avion. Dans ces cas, contrôlez leur (dés)utilisation avec une extension de ces « Coding Guidelines » adaptée à l'environnement spécifique.

##### Application

Utilisez un compilateur C++ à jour (actuellement C++20 ou C++17) avec un ensemble d'options qui n'acceptent pas les extensions.

---

### <a name="rp-what"></a>P.3 : Exprimer l'intention

##### Raison

À moins que l'intention d'un morceau de code ne soit indiquée (par des noms ou des commentaires), il est impossible de savoir si le code fait ce qu'il est censé faire.

##### Exemple

    gsl::index i = 0;
    while (i < v.size()) {
        // ... faire quelque chose avec v[i] ...
    }

L'intention de « simplement » parcourir les éléments de `v` n'est pas exprimée ici. Le détail d'implémentation d'un indice est exposé (et pourrait être mal utilisé), et `i` dépasse la portée de la boucle, ce qui peut ou non être prévu. Le lecteur ne peut pas le savoir à partir de ce seul extrait de code.

Meilleur :

    for (const auto& x : v) { /* faire quelque chose avec la valeur de x */ }

Ici, il n'y a aucune mention explicite du mécanisme d'itération, et la boucle travaille sur une référence à des éléments `const` afin d'éviter toute modification accidentelle. Si la modification est voulue, indiquez‑le :

    for (auto& x : v) { /* modifier x */ }

Pour plus de détails sur les instructions `for`, voir [ES.71](010-expr.md#res-for-range).
Parfois il est encore préférable d'utiliser un algorithme nommé. Cet exemple utilise `for_each` de la Ranges TS car il exprime directement l'intention :

    for_each(v, [](int x) { /* faire quelque chose avec la valeur de x */ });
    for_each(par, v, [](int x) { /* faire quelque chose avec la valeur de x */ });

La dernière variante montre clairement que l'ordre de traitement des éléments de `v` n'a pas d'importance.

Un programmeur devrait être familier avec :

* [La bibliothèque d'assistance aux lignes directrices](#gsl-guidelines-support-library) @TODO‑LINK  
* [La bibliothèque standard ISO C++](#sl-the-standard-library) @TODO‑LINK  
* Les bibliothèques fondamentales utilisées dans le(s) projet(s) en cours.

##### Note

Formulation alternative : dire ce qui doit être fait plutôt que simplement comment le faire.

##### Note

Certains construits du langage expriment mieux l'intention que d'autres.

##### Exemple

Si deux `int` doivent représenter les coordonnées d'un point 2D, indiquez‑le :

    draw_line(int, int, int, int);  // obscur : (x1,y1,x2,y2) ? (x,y,h,w) ? … ?
                                    // il faut consulter la documentation pour savoir

    draw_line(Point, Point);        // plus clair

##### Application

Rechercher les motifs courants pour lesquels il existe de meilleures alternatives :

* boucles `for` simples vs. boucles `range‑for`  
* interfaces `f(T*, int)` vs. interfaces `f(span<T>)`  
* variables de boucle dont la portée est trop large  
* `new` et `delete` nus  
* fonctions avec de nombreux paramètres de types primitifs  

Il existe un vaste champ de possibilités pour des transformations de programme semi‑automatisées.

---

### <a name="rp-typesafe"></a>P.4 : Idéalement, un programme devrait être statiquement sûr du typage

##### Raison

Idéalement, un programme serait entièrement sûr du typage à la compilation.
Malheureusement, ce n'est pas toujours possible. Zones problématiques :

* unions  
* casts  
* décadence de tableau (array decay)  
* erreurs de portée (range errors)  
* conversions d'appauvrissement (narrowing conversions)

##### Note

Ces zones sont à l'origine de problèmes graves (par ex. : plantages et violations de sécurité).
Nous essayons de fournir des techniques alternatives.

##### Application

Nous pouvons interdire, restreindre ou détecter les catégories de problèmes individuellement, selon les exigences et la faisabilité pour chaque programme.
Toujours proposer une alternative :

* unions → utiliser `variant` (C++17)  
* casts → les minimiser ; les modèles (`templates`) peuvent aider  
* décadence de tableau → utiliser `span` (de la GSL)  
* erreurs de portée → utiliser `span`  
* conversions d'appauvrissement → les minimiser et, quand elles sont nécessaires, recourir à `narrow` ou `narrow_cast` (de la GSL)

---

### <a name="rp-compile-time"></a>P.5 : Privilégier la vérification à la compilation sur la vérification à l'exécution

##### Raison

Clarté du code et performances. Vous n'avez pas besoin d'écrire des gestionnaires d'erreurs pour des erreurs déjà détectées à la compilation.

##### Exemple

    // Int est un alias utilisé pour les entiers
    int bits = 0;         // mauvais : code évitable
    for (Int i = 1; i; i <<= 1)
        ++bits;
    if (bits < 32)
        cerr << "Int too small\n";

Cet exemple n'atteint pas son objectif (car le dépassement de capacité est indéfini) et devrait être remplacé par un simple `static_assert` :

    // Int est un alias utilisé pour les entiers
    static_assert(sizeof(Int) >= 4);    // faire : vérification à la compilation

Ou, encore mieux, utilisez simplement le système de types et remplacez `Int` par `int32_t`.

##### Exemple

    void read(int* p, int n);   // lire au maximum n entiers dans *p

    int a[100];
    read(a, 1000);    // mauvais, hors limites

Meilleur :

    void read(span<int> r); // lire dans la plage d'entiers r

    int a[100];
    read(a);        // meilleur : laisser le compilateur déterminer le nombre d'éléments

**Formulation alternative** : ne remettez pas à l'exécution ce qui peut être fait à la compilation.

##### Application

* rechercher les arguments de type pointeur  
* rechercher les vérifications d'exécution de dépassement de portée

---

### <a name="rp-run-time"></a>P.6 : Ce qui ne peut pas être vérifié à la compilation doit être vérifiable à l'exécution

##### Raison

Laisser des erreurs difficiles à détecter dans un programme, c'est inviter les plantages et les résultats incorrects.

##### Note

Idéalement, nous attrapons toutes les erreurs (qui ne découlent pas d'une erreur de logique du programmeur) soit à la compilation, soit à l'exécution.
Il est impossible de toutes les attraper à la compilation et souvent trop coûteux de toutes les attraper à l'exécution. Néanmoins, nous devrions nous efforcer d'écrire des programmes qui, en principe, peuvent être vérifiés, à condition de disposer de ressources suffisantes (outils d'analyse, vérifications d'exécution, ressources machines, temps).

##### Exemple, mauvais

```cpp
// compilation séparée, éventuellement chargée dynamiquement
extern void f(int* p);

void g(int n)
{
    // mauvais : le nombre d'éléments n'est pas transmis à f()
    f(new int[n]);
}
```

Ici, une information cruciale (le nombre d'éléments) est tellement « cachée » que l'analyse statique devient probablement impossible et la vérification dynamique très difficile lorsque `f()` fait partie d'une ABI que l'on ne peut pas « instrumenter ». On pourrait incorporer des informations utiles dans le tas, mais cela nécessite des changements globaux du système, voire du compilateur. Le design proposé rend la détection d'erreurs très ardue.

##### Exemple, mauvais

```cpp
// compilation séparée, éventuellement chargée dynamiquement
extern void f2(int* p, int n);

void g2(int n)
{
    // mauvais : le mauvais nombre d'éléments peut être passé à f2()
    f2(new int[n], n);
}
```

Passer le nombre d'éléments en argument est meilleur (et bien plus répandu) que de ne transmettre que le pointeur et de se reposer sur une convention (non déclarée) pour connaître ou découvrir le nombre d'éléments. Cependant, une simple faute de frappe peut introduire une erreur grave. La connexion entre les deux arguments de `f2()` est conventionnelle, pas explicite.

De plus, il est implicite que `f2()` doit `delete` son argument (ou bien le appelant a commis une seconde erreur ?).

##### Exemple, mauvais

```cpp
// compilation séparée, éventuellement chargée dynamiquement
// NB : cela suppose que le code appelant est compatible ABI, utilise un
// compilateur C++ compatible et la même implémentation de la bibliothèque standard
extern void f3(unique_ptr<int[]>, int n);

void g3(int n)
{
    f3(make_unique<int[]>(n), m);    // mauvais : passer la possession et la taille séparément
}
```

##### Exemple

```cpp
// compilation séparée, éventuellement chargée dynamiquement
extern void f4(vector<int>&);   // compilation séparée, éventuellement chargée dynamiquement
extern void f4(span<int>);      // compilation séparée, éventuellement chargée dynamiquement
                                 // NB : cela suppose que le code appelant est compatible ABI,
                                 // utilise un compilateur C++ compatible et la même implémentation de la bibliothèque standard

void g3(int n)
{
    vector<int> v(n);
    f4(v);                     // passer par référence, conserver la possession
    f4(span<int>{v});          // passer une vue, conserver la possession
}
```

Ce design transporte le nombre d'éléments comme partie intégrante d'un objet, de sorte que les erreurs sont peu probables et que la vérification d'exécution demeure toujours possible, même si elle n'est pas toujours abordable.

##### Exemple

```cpp
vector<int> f5(int n)    // OK : déplacement
{
    vector<int> v(n);
    // ... initialiser v ...
    return v;
}

unique_ptr<int[]> f6(int n)    // mauvais : perd n
{
    auto p = make_unique<int[]>(n);
    // ... initialiser *p ...
    return p;
}

owner<int*> f7(int n)    // mauvais : perd n et on pourrait oublier de libérer
{
    owner<int*> p = new int[n];
    // ... initialiser *p ...
    return p;
}
```

##### Exemple

* ???  
* montrer comment des vérifications possibles sont contournées par des interfaces qui passent des classes de base polymorphes alors qu'elles connaissent réellement ce dont elles ont besoin ?  
  Ou des chaînes de caractères comme « options libres ».

##### Application

* Signaler les interfaces de type « (pointeur, comptage) » (cela cochera de nombreux exemples qui ne peuvent pas être corrigés pour des raisons de compatibilité)  
* ???

---

### <a name="rp-early"></a>P.7 : Détecter les erreurs d'exécution tôt

##### Raison

Éviter les plantages « mystérieux ».
Éviter les erreurs menant à des résultats (potentiellement) incorrects et non reconnus.

##### Exemple

```cpp
void increment1(int* p, int n)    // mauvais : sujet à erreur
{
    for (int i = 0; i < n; ++i) ++p[i];
}

void use1(int m)
{
    const int n = 10;
    int a[n] = {};
    // ...
    increment1(a, m);   // peut-être une faute de frappe, peut-être que m <= n était supposé
                        // mais supposons que m == 20
    // ...
}
```

Nous avons ici introduit une petite erreur dans `use1` qui conduit à des données corrompues ou à un plantage.
L'interface de type (pointeur, comptage) laisse `increment1()` sans moyen réaliste de se défendre contre les accès hors‑borne. Si nous pouvions vérifier les indices dès l'accès, l'erreur ne serait découverte que lorsque `p[10]` serait accédé. Nous pouvons vérifier plus tôt et améliorer le code :

```cpp
void increment2(span<int> p)
{
    for (int& x : p) ++x;
}

void use2(int m)
{
    const int n = 10;
    int a[n] = {};
    // ...
    increment2({a, m});    // peut-être une faute de frappe, peut-être que m <= n était supposé
    // ...
}
```

Maintenant, la condition `m <= n` peut être vérifiée au moment de l'appel (tôt) plutôt que plus tard.
Si la faute de frappe était que nous voulions réellement utiliser `n` comme borne, le code peut être simplifié davantage (en éliminant la possibilité d'erreur) :

```cpp
void use3(int m)
{
    const int n = 10;
    int a[n] = {};
    // ...
    increment2(a);   // le nombre d'éléments de a n'a pas besoin d'être répété
    // ...
}
```

##### Exemple, mauvais

Ne pas vérifier deux fois la même valeur. Ne pas passer des données structurées sous forme de chaînes :

```cpp
Date read_date(istream& is);    // lire une date depuis le flux d'entrée
Date extract_date(const string& s);    // extraire une date depuis une chaîne

void user1(const string& date)    // manipuler la date
{
    auto d = extract_date(date);
    // ...
}

void user2()
{
    Date d = read_date(cin);
    // ...
    user1(d.to_string());
    // ...
}
```

La date est validée deux fois (par le constructeur `Date`) et transmise sous forme de chaîne de caractères (données non structurées).

##### Exemple

Un excès de vérifications peut être coûteux. Il existe des cas où la vérification précoce est inefficace parce que vous pourriez ne jamais avoir besoin de la valeur, ou ne nécessiter qu'une partie de la valeur qui est plus facilement vérifiable que l'ensemble. De même, n'ajoutez pas de vérifications de validité qui changent le comportement asymptotique de votre interface (par ex. : n'ajoutez pas une vérification `O(n)` à une interface dont la complexité moyenne est `O(1)`) :

```cpp
class Jet {    // La physique dit : e * e < x * x + y * y + z * z
    float x;
    float y;
    float z;
    float e;
public:
    Jet(float x, float y, float z, float e)
        :x(x), y(y), z(z), e(e)
    {
        // Dois‑je vérifier ici que les valeurs sont physiquement plausibles ?
    }

    float m() const
    {
        // Dois‑je gérer le cas dégénéré ici ?
        return sqrt(x * x + y * y + z * z - e * e);
    }

    ???
};
```

La loi physique pour un jet (`e * e < x * x + y * y + z * z`) n'est pas un invariant à cause des possibles erreurs de mesure.

???

##### Application

* Examiner les pointeurs et tableaux : faire les contrôles de portée tôt et pas à plusieurs reprises  
* Examiner les conversions : éliminer ou marquer les conversions d'appauvrissement  
* Rechercher des valeurs non vérifiées provenant d'entrées  
* Rechercher des données structurées (objets de classes avec invariants) converties en chaînes  
* ???

---

### <a name="rp-leak"></a>P.8 : Ne pas laisser fuir de ressources

##### Raison

Même une croissance lente des ressources épuisera, à terme, la disponibilité de ces ressources.
C'est particulièrement important pour les programmes de longue durée, mais constitue aussi un principe essentiel de programmation responsable.

##### Exemple, mauvais

```cpp
void f(const char* name)
{
    FILE* input = fopen(name, "r");
    // ...
    if (something) return;   // mauvais : si something == true, le descripteur de fichier est perdu
    // ...
    fclose(input);
}
```

Préférez [RAII](009-resource.md#rr-raii) :

```cpp
void f(const char* name)
{
    ifstream input {name};
    // ...
    if (something) return;   // OK : aucune fuite
    // ...
}
```

**Voir aussi** : [La section de gestion des ressources](009-resource.md)

##### Note

Une fuite est, familièrement, « tout ce qui n'est pas nettoyé ».
La classification la plus importante est « tout ce qui ne peut plus être nettoyé ».
Par exemple, allouer un objet sur le tas puis perdre le dernier pointeur qui pointe vers cette allocation.

Cette règle ne doit pas être interprétée comme imposant que les allocations au sein d'objets de longue durée soient libérées lors de l'arrêt du programme.
Par exemple, compter sur le nettoyage garanti par le système (fermeture de fichiers, désallocation de mémoire à la fin du processus) peut simplifier le code.
Néanmoins, se reposer sur des abstractions qui nettoient implicitement peut être tout aussi simple – et souvent plus sûr.

##### Note

Faire respecter le [profil de sécurité du cycle de vie](022-profile.md#ss-lifetime) élimine les fuites.
Lorsqu'il est combiné avec la sécurité des ressources fournie par [RAII](009-resource.md#rr-raii), il élimine le besoin de « garbage collection » (en générant aucun déchet).
Combinez cela avec l'application des [profils de type et de limites](003-introduction.md#ss-force) et vous obtenez une sécurité totale du type et des ressources, garantie par les outils.

##### Application

* Examiner les pointeurs : les classer en non‑propriétaires (par défaut) et propriétaires.
  Là où cela est possible, remplacer les propriétaires par des gestionnaires de ressources de la bibliothèque standard (comme dans l'exemple ci‑dessus).
  Alternativement, marquer un propriétaire avec `owner` de la [GSL](#gsl-guidelines-support-library) @TODO‑LINK.
* Rechercher les `new` et `delete` nus  
* Rechercher les fonctions connues d'allocation de ressources qui retournent des pointeurs bruts (telles que `fopen`, `malloc` ou `strdup`)

---

### <a name="rp-waste"></a>P.9 : Ne pas gaspiller de temps ou d'espace

##### Raison

C'est du C++.

##### Note

Le temps et l'espace que vous consacrez judicieusement à atteindre un but (par ex. : rapidité de développement, sécurité des ressources ou simplification des tests) ne sont **pas** du gaspillage.
« Un autre avantage de viser l'efficacité est que le processus vous oblige à comprendre le problème plus en profondeur. » – Alex Stepanov

##### Exemple, mauvais

```cpp
struct X {
    char ch;
    int i;
    string s;
    char ch2;

    X& operator=(const X& a);
    X(const X&);
};

X waste(const char* p)
{
    if (!p) throw Nullptr_error{};
    int n = strlen(p);
    auto buf = new char[n];
    if (!buf) throw Allocation_error{};
    for (int i = 0; i < n; ++i) buf[i] = p[i];
    // ... manipuler le tampon ...
    X x;
    x.ch = 'a';
    x.s = string(n);    // donner à x.s l'espace pour *p
    for (gsl::index i = 0; i < x.s.size(); ++i) x.s[i] = buf[i];  // copier buf dans x.s
    delete[] buf;
    return x;
}

void driver()
{
    X x = waste("Typical argument");
    // ...
}
```

Oui, c'est une caricature, mais chaque erreur individuelle a déjà été observée dans du code en production, voire pire.
Notez que la disposition de `X` garantit qu'au moins 6 octets (et très probablement davantage) sont gaspillés.
La définition redondante des opérations de copie désactive les sémantiques de déplacement, ce qui rend l'opération de retour lente (notez que la *Return Value Optimization* (RVO) n'est pas garantie ici).
L'utilisation de `new` et `delete` pour `buf` est superflue ; si nous avions réellement besoin d'une chaîne locale, il aurait fallu utiliser `std::string`.
Il existe plusieurs autres bugs de performance et complexités inutiles.

##### Exemple, mauvais

```cpp
void lower(zstring s)
{
    for (int i = 0; i < strlen(s); ++i) s[i] = tolower(s[i]);
}
```

C'est en fait un extrait de code de production.
Nous voyons que dans notre condition nous avons `i < strlen(s)`. Cette expression est évaluée à chaque itération de la boucle, ce qui oblige `strlen` à parcourir la chaîne à chaque tour pour en connaître la longueur.
Comme le contenu de la chaîne change, on suppose que `tolower` n'affecte pas la longueur, il vaut donc mieux mettre la longueur en cache avant la boucle afin d'éviter ce coût à chaque itération.

##### Note

Un exemple isolé de gaspillage est rarement significatif ; lorsqu'il l'est, il est généralement éliminable par un expert.
En revanche, le gaspillage largement répandu dans une base de code peut rapidement devenir conséquent, et les experts ne sont pas toujours disponibles.
L'objectif de cette règle (et des règles plus spécifiques qui la soutiennent) est d'éliminer la plupart du gaspillage lié à l'usage de C++ avant même qu'il ne survienne.
Ensuite, on pourra s'occuper du gaspillage lié aux algorithmes et aux exigences, ce qui dépasse le cadre de ces lignes directrices.

##### Application

De nombreuses règles plus spécifiques visent les objectifs globaux de simplicité et d'élimination du gaspillage gratuit.

* Signaler une valeur de retour inutilisée d'une fonction `operator++` ou `operator--` postfixe définie par l'utilisateur et non‑défaultée. Préférez la forme préfixe. (Remarque : « non‑défaulté » a pour but de réduire le bruit. Réévaluez cette application si elle reste trop bruyante en pratique.)

---

### <a name="rp-mutable"></a>P.10 : Privilégier les données immutables aux données mutables

##### Raison

Il est plus facile de raisonner sur des constantes que sur des variables.
Quelque chose d'immuable ne peut pas changer de façon inattendue.
Parfois, l'immuabilité permet de meilleures optimisations.
On ne peut pas rencontrer de data race sur une constante.

Voir [Con : Constantes et immuabilité](014-const.md) @TODO‑LINK.

---

### <a name="rp-library"></a>P.11 : Encapsuler les constructions désordonnées plutôt que de les disperser dans le code

##### Raison

Le code désordonné est plus susceptible de masquer des bugs et plus difficile à écrire.
Une bonne interface est plus facile et plus sûre à utiliser.
Le code bas‑niveau, désordonné, engendre davantage de code de ce type.

##### Exemple

```cpp
int sz = 100;
int* p = (int*) malloc(sizeof(int) * sz);
int count = 0;
// ...
for (;;) {
    // ... lire un int dans x, sortir de la boucle si fin de fichier atteinte ...
    // ... vérifier que x est valide ...
    if (count == sz)
        p = (int*) realloc(p, sizeof(int) * sz * 2);
    p[count++] = x;
    // ...
}
```

C'est du bas‑niveau, verbeux et sujet à erreurs. Par exemple, nous avons « oublié » de tester l'épuisement de mémoire et d'ajuster la valeur de `sz`.
À la place, nous pourrions utiliser `vector` :

```cpp
vector<int> v;
v.reserve(100);
// ...
for (int x; cin >> x; ) {
    // ... vérifier que x est valide ...
    v.push_back(x);
}
```

##### Note

La bibliothèque standard et la GSL sont des exemples de cette philosophie.
Par exemple, au lieu de bricoler avec des tableaux, des unions, des casts, des problèmes de durée de vie délicats, `gsl::owner`, etc., qui sont nécessaires pour implémenter des abstractions clés comme `vector`, `span`, `lock_guard` ou `future`, nous utilisons les bibliothèques conçues et implémentées par des personnes disposant de plus de temps et d'expertise que nous n'en avons généralement.
De même, nous pouvons et devons concevoir et implémenter des bibliothèques plus spécialisées, plutôt que de laisser les utilisateurs (souvent nous‑mêmes) relever le défi de réécrire du code bas‑niveau maintes fois.
Il s'agit d'une variante du [principe du sous‑ensemble du sur‑ensemble](003-introduction.md#r0) qui sous‑tend ces lignes directrices.

##### Application

* Rechercher du « code désordonné » tel que la manipulation complexe de pointeurs et les casts en dehors de l'implémentation d'abstractions.

---

### <a name="rp-tools"></a>P.12 : Utiliser les outils d'aide appropriés

##### Raison

De nombreuses tâches sont mieux réalisées « par la machine ».
Les ordinateurs ne se fatiguent pas et ne s'ennuient pas avec les tâches répétitives.
Nous avons généralement de meilleures choses à faire que d'exécuter des tâches de routine à la main.

##### Exemple

Exécuter un analyseur statique pour vérifier que votre code suit les lignes directrices que vous souhaitez respecter.

##### Note

Voir :

* [Outils d'analyse statique](https://en.wikipedia.org/wiki/List_of_tools_for_static_code_analysis)  
* [Outils de concurrence](012-concurrency.md#rconc-tools)  
* [Outils de test](https://github.com/isocpp/CppCoreGuidelines/tree/master)

Il existe de nombreux autres types d'outils, comme les systèmes de contrôle de version, les outils de construction, etc., mais ceux‑ci dépassent le champ de ces lignes directrices.

##### Note

Soyez prudent de ne pas devenir dépendant de chaînes d'outils trop élaborées ou trop spécialisées.
Celles‑ci peuvent rendre votre code, autrement portable, non‑portable.

---

### <a name="rp-lib"></a>P.13 : Utiliser les bibliothèques de soutien appropriées

##### Raison

Utiliser une bibliothèque bien conçue, bien documentée et bien supportée fait gagner du temps et des efforts ; sa qualité et sa documentation sont probablement supérieures à ce que vous pourriez atteindre si la majorité de votre temps devait être consacrée à l'implémentation.
Le coût (temps, effort, argent, etc.) d'une bibliothèque peut être partagé entre de nombreux utilisateurs.
Une bibliothèque largement utilisée a plus de chances d'être maintenue à jour et portée sur de nouveaux systèmes qu'une application individuelle.
La connaissance d'une bibliothèque largement utilisée peut faire gagner du temps sur d'autres projets futurs.
Ainsi, si une bibliothèque adaptée à votre domaine d'application existe, utilisez‑la.

##### Exemple

```cpp
std::sort(begin(v), end(v), std::greater<>());
```

À moins d'être un expert en algorithmes de tri et de disposer de beaucoup de temps, cela est plus susceptible d'être correct et plus rapide que tout ce que vous pourriez écrire vous‑même pour une application spécifique.
Vous avez besoin d'une raison de ne **pas** utiliser la bibliothèque standard (ou quelles que soient les bibliothèques fondamentales que votre application utilise) plutôt que d'une raison de l'utiliser.

##### Note

Par défaut, utilisez :

* La [bibliothèque standard ISO C++](#sl-the-standard-library) @TODO‑LINK  
* La [bibliothèque d'assistance aux lignes directrices](#gsl-guidelines-support-library) @TODO‑LINK

##### Note

Si aucune bibliothèque bien conçue, bien documentée et bien supportée n'existe pour un domaine important, peut‑être devrait‑vous la concevoir et l'implémenter, puis l'utiliser.
