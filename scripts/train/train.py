"""
train.py : Entraînement RL configurable + Sauvegarde intermédiaire + Visualisations.
"""

import sys
import os
import argparse
from tqdm import tqdm

# Ajoute la racine du projet au path Python
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))

from env.core.game import Game
from env.metrics import compute_style_metrics
from env.core.visualizer import plot_reward_evolution, plot_style_metrics, save_all_plots


# === ARGPARSE ===
parser = argparse.ArgumentParser(description="Train Red Lock RL Agent")
parser.add_argument("--opponent_mode", type=str, choices=["random", "model"], default="random",
                    help="Type d'adversaire : random ou model")
parser.add_argument("--opponent_model_path", type=str, default=None,
                    help="Chemin vers le modèle si opponent_mode = model")
args = parser.parse_args()

# === CONFIG TRAIN ===
episodes = 1500
save_every = 50  # Sauvegarde tous les X épisodes
save_path = "data/models/rl_agent_v1_final.pth"

results = []

for ep in tqdm(range(episodes), desc="Episodes"):
    env = Game(
        opponent_mode=args.opponent_mode,
        opponent_model_path=args.opponent_model_path
    )
    env.ticks = 0
    env.max_ticks = 1000
    env.positions_x = []
    env.positions_y = []
    env.running = True

    while env.running and env.ticks < env.max_ticks:
        env.handle_events()
        env.update()
        env.draw()  # Active ça si tu veux voir le match

        for p in env.match.players:
            env.positions_x.append(p.x)
            env.positions_y.append(p.y)

        env.ticks += 1

    # === Nouvelle façon de calculer le reward ===
    agents = env.match.agents[:4]  # RL uniquement

    # Prends la moyenne réelle de TOUS les rewards distribués pendant le match
    total_rewards = []
    for agent in agents:
        total_rewards.extend(agent.local_rewards)

    if total_rewards:
        reward_mean = sum(total_rewards) / len(total_rewards)
    else:
        reward_mean = 0.0

    mean_x, mean_y, std_x, std_y = compute_style_metrics(env.positions_x, env.positions_y)

    results.append({
        "mean_x": mean_x,
        "mean_y": mean_y,
        "std_x": std_x,
        "std_y": std_y,
        "quality": reward_mean
    })

    for agent in agents:
        # Utilise TOUS les rewards déjà accumulés (pas besoin de + [reward_mean])
        agent.learn(agent.saved_log_probs, agent.local_rewards)
        agent.saved_log_probs = []
        agent.local_rewards = []

    tqdm.write(
        f"[TRAIN] Episode {ep + 1}/{episodes} | Bleu: {env.match.score_bleu} | "
        f"Rouge: {env.match.score_rouge} | Mean RL Reward: {reward_mean:.4f}"
    )

    # === Sauvegarde intermédiaire ===
    if (ep + 1) % save_every == 0:
        checkpoint_path = f"data/models/rl_agent_v1_ep{ep + 1}.pth"
        env.match.agents[0].save_model(checkpoint_path)

# === Sauvegarde finale ===
env.match.agents[0].save_model(save_path)

# === Visualisations ===
plot_style_metrics(results)
plot_reward_evolution(results)
save_all_plots(results, out_dir="data/plots")
