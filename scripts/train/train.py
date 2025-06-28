"""
train.py : Entraînement RL + Sauvegarde + Visualisation styles.
"""

import sys
import os
from tqdm import tqdm
import matplotlib.pyplot as plt

# Ajoute la racine du projet au path Python
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))

from env.core.game import Game
from env.metrics import compute_style_metrics, plot_styles
from env.agents.rl_agent import RLAgent

episodes = 100
save_path = "data/models/rl_agent_v1.pth"
results = []

for ep in tqdm(range(episodes), desc="Episodes"):
    env = Game()
    env.ticks = 0
    env.max_ticks = 10000
    env.positions_x = []
    env.positions_y = []
    env.running = True

    while env.running and env.ticks < env.max_ticks:
        env.handle_events()
        env.update()
        env.draw()  # Désactive pour aller plus vite

        for p in env.players:
            env.positions_x.append(p.x)
            env.positions_y.append(p.y)

        env.ticks += 1

    # Reward global : diff de score
    reward = env.score_bleu - env.score_rouge

    mean_x, mean_y, std_x, std_y = compute_style_metrics(env.positions_x, env.positions_y)

    results.append({
        "mean_x": mean_x,
        "mean_y": mean_y,
        "std_x": std_x,
        "std_y": std_y,
        "quality": reward
    })

    for agent in env.agents[:2]:  # RL seulement
        # Combine : micro + macro
        all_rewards = agent.local_rewards + [reward]
        agent.learn(agent.saved_log_probs, all_rewards)

        # Reset pour le prochain match
        agent.saved_log_probs = []
        agent.local_rewards = []

    tqdm.write(f"[TRAIN] Episode {ep} | Bleu: {env.score_bleu} | Rouge: {env.score_rouge} | Reward: {reward}")

# Sauvegarde finale du modèle
env.agents[0].save_model(save_path)

# Visualisation style de jeu
plot_styles(results)

# Graphique : évolution du reward
rewards = [res["quality"] for res in results]
plt.figure(figsize=(10, 5))
plt.plot(range(len(rewards)), rewards, marker='o')
plt.title("Évolution du reward par épisode")
plt.xlabel("Épisode")
plt.ylabel("Reward (Score Bleu - Score Rouge)")
plt.grid(True)
plt.show()
