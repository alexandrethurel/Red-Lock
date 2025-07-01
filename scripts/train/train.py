"""
train.py : Entraînement RL configurable + Sauvegarde intermédiaire + Visualisations.
"""

import sys
import os
import argparse
from tqdm import tqdm

# Ajoute la racine du projet au path Python
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))

from env_dev_dev.core.game import Game
from env_dev_dev.metrics import compute_style_metrics
from env_dev_dev.core.visualizer import plot_reward_evolution, plot_style_metrics, save_all_plots


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
    env_dev = Game(
        opponent_mode=args.opponent_mode,
        opponent_model_path=args.opponent_model_path
    )
    env_dev.ticks = 0
    env_dev.max_ticks = 1000
    env_dev.positions_x = []
    env_dev.positions_y = []
    env_dev.running = True

    while env_dev.running and env_dev.ticks < env_dev.max_ticks:
        env_dev.handle_events()
        env_dev.update()
        env_dev.draw()  # Active ça si tu veux voir le match

        for p in env_dev.match.players:
            env_dev.positions_x.append(p.x)
            env_dev.positions_y.append(p.y)

        env_dev.ticks += 1

    # === Nouvelle façon de calculer le reward ===
    agents = env_dev.match.agents[:4]  # RL uniquement

    # Prends la moyenne réelle de TOUS les rewards distribués pendant le match
    total_rewards = []
    for agent in agents:
        total_rewards.extend(agent.local_rewards)

    if total_rewards:
        reward_mean = sum(total_rewards) / len(total_rewards)
    else:
        reward_mean = 0.0

    mean_x, mean_y, std_x, std_y = compute_style_metrics(env_dev.positions_x, env_dev.positions_y)

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
        f"[TRAIN] Episode {ep + 1}/{episodes} | Bleu: {env_dev.match.score_bleu} | "
        f"Rouge: {env_dev.match.score_rouge} | Mean RL Reward: {reward_mean:.4f}"
    )

    # === Sauvegarde intermédiaire ===
    if (ep + 1) % save_every == 0:
        checkpoint_path = f"data/models/rl_agent_v1_ep{ep + 1}.pth"
        env_dev.match.agents[0].save_model(checkpoint_path)

# === Sauvegarde finale ===
env_dev.match.agents[0].save_model(save_path)

# === Visualisations ===
plot_style_metrics(results)
plot_reward_evolution(results)
save_all_plots(results, out_dir="data/plots")
