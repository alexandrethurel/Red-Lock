📘 Red Lock — README
🎯 Pitch

Red Lock est un prototype de simulateur de football 2D où des joueurs identiques au départ apprennent à jouer collectivement grâce à un algorithme de Reinforcement Learning (RL).
Inspiré de Blue Lock, l’objectif est de simuler l’émergence de styles de jeu variés, de rôles naturels et de tactiques collectives sans règles codées en dur.
⚙️ Composition

    2 équipes

        2 joueurs de champ IA RL.

        1 gardien par équipe (IA scriptée au départ).

    ⚽ Terrain 2D affiché en temps réel (Pygame).

    🎮 Chaque joueur décide quoi faire, influencé par ses caractéristiques %.

    📊 Après chaque match, l’équipe est caractérisée collectivement (bloc haut/bas, large/resserré, etc.).

🔀 Actions possibles
Action	Condition	Description
🔵 Se déplacer	Toujours autorisé	Aller vers une position cible en choisissant une vitesse (1, 2, 3).
🟢 Passer	Si en possession du ballon	Passer à un coéquipier, réussite dépend de la précision passe (%).
🟣 Tirer	Si en possession du ballon	Tirer vers le but adverse, réussite dépend de la précision tir (%).
🟠 Dribbler	Si en possession du ballon	Avancer avec le ballon en essayant d’échapper à un adversaire, succès dépend du dribble (%).
🟤 Intercepter	Si PAS en possession et ballon proche	Se placer sur la trajectoire pour couper une passe/tir, succès dépend de l’interception (%).
⚫ Tacler	Si PAS en possession et joueur porteur proche	Tenter de récupérer le ballon directement, succès dépend du tacle (%).
✅ Déplacement avec intensité

    Lorsqu’un joueur se déplace, il choisit :

        Une direction cible.

        Une intensité :

            1 : déplacement lent (marche).

            2 : déplacement normal (course).

            3 : sprint (vitesse max).

    La vitesse réelle est limitée par la stat Vitesse (%).

    Le nombre total de sprints est limité par la stat Endurance (%).

⏱️ Terrain, FPS et durée

    🎮 FPS cible : 30–60 FPS pour une simulation fluide.

    ⚽ Durée d’un match : typiquement 2–5 minutes par simulation.

    📏 Dimensions du terrain :

        Cohérentes avec vitesse des joueurs, nombre de frames et durée totale.

        Par exemple : un joueur ne doit pas traverser le terrain en 2 secondes en sprint.

🧬 Statistiques — somme fixe

Chaque joueur possède un ensemble de caractéristiques, exprimées en %, dont la somme est toujours égale à 100.
Stat	Impact direct
Vitesse (%)	Limite la vitesse max de déplacement (marche/course/sprint).
Endurance (%)	Définit le nombre total de sprints autorisés par match.
Précision passe (%)	Détermine la probabilité de réussir une passe propre.
Précision tir (%)	Détermine la probabilité qu’un tir soit cadré et puissant.
Dribble (%)	Détermine la probabilité de réussir un dribble face à un adversaire.
Interception (%)	Détermine la probabilité de couper une trajectoire de balle.
Tacle (%)	Détermine la probabilité de récupérer proprement le ballon lors d’un duel.

Règle clé :

    Tous les joueurs commencent avec une répartition identique ➜ même potentiel.

    L’apprentissage (RL) redistribue ces % pour créer des styles uniques :

        Plus de vitesse ➜ moins de dribble ou de précision.

        Plus de passes ➜ moins d’agressivité défensive.

        Etc.

🎁 Exemple de limitation

    Endurance = 40% ➜ maximum 40 sprints autorisés par match.

    Vitesse = 80% ➜ vitesse max de déplacement = 80% de la vitesse max du moteur.

    Précision passe = 60% ➜ 60% de chance de passe réussie, sinon imprécision.

📊 Analyse collective

Après chaque match :

    Calcul de :

        📏 Moyenne X/Y ➜ bloc haut/bas, axe du jeu.

        📏 Variance X/Y ➜ jeu large ou resserré.

        🔗 Distance moyenne entre joueurs ➜ indice de compacité.

        ⚽ % de possession, passes réussies, interceptions, tacles ➜ style collectif.

    Ces métriques servent à identifier des styles d’équipe : bloc bas, pressing haut, jeu axial, jeu large, etc.
