"""
visualizer.py : Centralise toutes les visualisations Red Lock.
"""

import os
import matplotlib.pyplot as plt


def plot_style_metrics(results):
    """
    Affiche un scatter des centres de gravité des positions.
    """
    means_x = [r["mean_x"] for r in results]
    means_y = [r["mean_y"] for r in results]
    plt.figure(figsize=(6, 6))
    plt.scatter(means_x, means_y, c='blue')
    plt.title("Centres moyens des positions")
    plt.xlabel("Mean X")
    plt.ylabel("Mean Y")
    plt.grid(True)
    plt.show()


def plot_reward_evolution(results):
    """
    Affiche l'évolution du reward par épisode.
    """
    rewards = [r["quality"] for r in results]
    plt.figure(figsize=(10, 5))
    plt.plot(range(1, len(rewards) + 1), rewards, marker='o')
    plt.title("Évolution du reward par épisode")
    plt.xlabel("Épisode")
    plt.ylabel("Reward (Score Bleu - Score Rouge)")
    plt.grid(True)
    plt.show()


def save_all_plots(results, out_dir="data/plots"):
    """
    Sauvegarde tous les plots sous forme de fichiers PNG.
    """
    os.makedirs(out_dir, exist_ok=True)

    # Reward evolution
    rewards = [r["quality"] for r in results]
    plt.figure(figsize=(10, 5))
    plt.plot(range(1, len(rewards) + 1), rewards, marker='o')
    plt.title("Reward Evolution")
    plt.xlabel("Episode")
    plt.ylabel("Reward")
    plt.grid(True)
    plt.savefig(f"{out_dir}/reward_evolution.png")
    plt.close()

    # Mean positions scatter
    means_x = [r["mean_x"] for r in results]
    means_y = [r["mean_y"] for r in results]
    plt.figure(figsize=(6, 6))
    plt.scatter(means_x, means_y, c='blue')
    plt.title("Mean Positions Scatter")
    plt.xlabel("Mean X")
    plt.ylabel("Mean Y")
    plt.grid(True)
    plt.savefig(f"{out_dir}/mean_positions.png")
    plt.close()
