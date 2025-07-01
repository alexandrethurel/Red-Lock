"""
train_multi.py : Entraînement RL multi-process + Sauvegarde intermédiaire + Visualisations.
"""

import sys
import os
import multiprocessing as mp
from tqdm import tqdm

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))

from env.core.game import Game
from env.metrics import compute_style_metrics
from env.core.visualizer import plot_reward_evolution, plot_style_metrics, save_all_plots
from env.agents.rl_agent import RLAgent


# === CONFIG TRAIN ===
episodes = 20
save_every = 5
save_path = "data/models/rl_agent_v1_final.pth"

workers = mp.cpu_count() - 2
max_ticks = 2000


# === Fonction par worker ===
def run_episode(dummy):
    env = Game()
    env.ticks = 0
    env.max_ticks = max_ticks
    env.positions_x = []
    env.positions_y = []
    env.running = True

    while env.running and env.ticks < env.max_ticks:
        env.handle_events()
        env.update()
        for p in env.match.players:
            env.positions_x.append(p.x)
            env.positions_y.append(p.y)
        env.ticks += 1

    reward = env.match.score_bleu - env.match.score_rouge
    mean_x, mean_y, std_x, std_y = compute_style_metrics(env.positions_x, env.positions_y)

    # Chaque agent apprend localement
    for agent in env.match.agents[:4]:  # RL seulement
        all_rewards = agent.local_rewards + [reward]
        agent.learn(agent.saved_log_probs, all_rewards)
        agent.saved_log_probs = []
        agent.local_rewards = []

    return {
        "mean_x": mean_x,
        "mean_y": mean_y,
        "std_x": std_x,
        "std_y": std_y,
        "quality": reward,
        "model_state": env.match.agents[0].policy.state_dict()
    }


if __name__ == "__main__":
    # === RLAgent central ===
    global_agent = RLAgent(["passer", "tirer", "dribbler", "se_deplacer"])

    results = []

    for ep in tqdm(range(episodes), desc="Episodes"):
        with mp.Pool(workers) as pool:
            episodes_data = pool.map(run_episode, range(workers))

        # Log résultats
        for ed in episodes_data:
            results.append({
                "mean_x": ed["mean_x"],
                "mean_y": ed["mean_y"],
                "std_x": ed["std_x"],
                "std_y": ed["std_y"],
                "quality": ed["quality"]
            })

        # Synchronise le modèle global avec le premier worker (exemple simple)
        global_agent.policy.load_state_dict(episodes_data[0]["model_state"])

        if (ep + 1) % save_every == 0:
            checkpoint_path = f"data/models/rl_agent_v1_ep{ep + 1}.pth"
            global_agent.save_model(checkpoint_path)

    # Sauvegarde finale
    global_agent.save_model(save_path)

    # Visualisations
    plot_style_metrics(results)
    plot_reward_evolution(results)
    save_all_plots(results, out_dir="data/plots")
