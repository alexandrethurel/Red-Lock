🔴 Très bien ! Voici le **README final**, version **corrigée** avec le **nom exact** : **Red Lock** ⚡

---

# 📘 **Red Lock — README**

---

## 🎯 Pitch

**Red Lock** est un prototype de **simulateur de football 2D** où des joueurs **identiques au départ** apprennent à jouer **collectivement** grâce à un **algorithme de Reinforcement Learning (RL)**.
Inspiré de *Blue Lock*, l’objectif est de faire émerger **des styles de jeu variés**, des **rôles naturels** et des **schémas tactiques collectifs** sans règles figées.

---

## ⚙️ Composition

* **2 équipes**

  * 2 joueurs de champ contrôlés par une IA RL.
  * 1 gardien par équipe (IA scriptée au départ).
* ⚽ Terrain 2D simulé en temps réel.
* 🎮 Chaque joueur agit selon ses **caractéristiques exprimées en %**.
* 📊 Après chaque match, une **analyse collective** permet de détecter le style global de l’équipe : bloc bas, pressing haut, jeu large, compact, etc.

---

## 🔀 Actions possibles

| Action             | Quand ?                                               | Description                                                          |
| ------------------ | ----------------------------------------------------- | -------------------------------------------------------------------- |
| 🔵 **Se déplacer** | Toujours autorisé                                     | Aller vers une position cible, avec une vitesse choisie (1, 2 ou 3). |
| 🟢 **Passer**      | Si **en possession du ballon**                        | Passer à un coéquipier.                                              |
| 🟣 **Tirer**       | Si **en possession du ballon**                        | Tirer vers le but adverse.                                           |
| 🟠 **Dribbler**    | Si **en possession du ballon**                        | Avancer avec le ballon pour échapper à un adversaire.                |
| 🟤 **Intercepter** | Si **PAS en possession** et **balle proche**          | Se placer pour couper une passe ou un tir.                           |
| ⚫ **Tacler**       | Si **PAS en possession** et **joueur porteur proche** | Tenter de récupérer le ballon directement sur un adversaire.         |

---

## ✅ Déplacement avec intensité

Quand un joueur se déplace :

* Il choisit une **intensité** :

  * **1** : marche
  * **2** : course normale
  * **3** : sprint

Sa **vitesse réelle** dépend de sa stat **Vitesse (%)**, et le **nombre total de sprints** est limité par sa stat **Endurance (%)**.

---

## 🧬 **Caractéristiques — somme fixe**

Chaque joueur possède un **ensemble de caractéristiques**, exprimées en pourcentages, dont la **somme est toujours égale à 100**.
Cela garantit que tous les joueurs ont le **même potentiel global**, mais qu’il peut être réparti différemment au fil du temps.

---

## ⚡️ **Impact des caractéristiques sur les actions**

| Stat                    | Impact direct                                                                                                                              |
| ----------------------- | ------------------------------------------------------------------------------------------------------------------------------------------ |
| **Vitesse (%)**         | Détermine la vitesse maximale de déplacement (marche, course, sprint). Plus le pourcentage est haut, plus le joueur peut se déplacer vite. |
| **Endurance (%)**       | Définit le **nombre total de sprints** autorisés par match. Une faible endurance limite le nombre de sprints possibles.                    |
| **Précision passe (%)** | Probabilité de réussir une passe propre. Plus le pourcentage est élevé, moins il y a de risque d’échec ou d’interception.                  |
| **Précision tir (%)**   | Probabilité qu’un tir soit cadré et puissant.                                                                                              |
| **Dribble (%)**         | Probabilité de réussir un dribble face à un adversaire direct.                                                                             |
| **Interception (%)**    | Probabilité de couper une passe ou une trajectoire de balle.                                                                               |
| **Tacle (%)**           | Probabilité de réussir un tacle propre sans faute.                                                                                         |

---

## 🧩 **Exemple concret**

* Un joueur avec **Vitesse 80%** et **Endurance 40%** pourra aller vite mais aura peu de sprints à disposition.
* Un joueur avec **Précision passe 70%** sera fiable dans la distribution mais pourra être vulnérable s’il dribble mal.
* Un joueur avec **Tacle 20%** aura un risque élevé de faute ou d’échec lors d’un tacle.

---

## ⏱️ **Terrain, FPS et durée**

* 🎮 Simulation fluide à 30–60 FPS.
* ⚽ Un match dure entre 2 et 5 minutes pour simuler un scénario réaliste.
* 📏 Dimensions du terrain ajustées pour :

  * Assurer que la vitesse des joueurs est crédible.
  * Éviter qu’un sprint traverse tout le terrain en quelques secondes.
  * Correspondre à la durée et aux FPS choisis.

---

## 📊 **Analyse collective après match**

A la fin de chaque match, l’équipe est analysée comme un bloc :

* 📏 Moyenne X/Y ➜ indique si l’équipe joue bloc bas, médian ou haut.
* 📏 Variance X/Y ➜ indique si l’équipe est large ou resserrée.
* 🔗 Distance moyenne entre joueurs ➜ mesure de compacité.
* ⚽ Statistiques globales : % possession, passes, interceptions, tacles.

Ces métriques permettent de **repérer les styles collectifs** : bloc bas, pressing haut, jeu axial, jeu large, bloc compact.

---

## ✅ **Principe clé**

**Tous les joueurs démarrent avec le même potentiel (somme = 100)**.
Ce sont leurs **répartitions et l’apprentissage** qui feront émerger des profils différents : sprinteur explosif, passeur précis, dribbleur créatif, défenseur rugueux.
