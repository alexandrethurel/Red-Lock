"""
metrics.py : Outils pour calculer et afficher le style.
"""

import numpy as np
import matplotlib.pyplot as plt


def compute_style_metrics(positions_x, positions_y):
    mean_x = np.mean(positions_x)
    mean_y = np.mean(positions_y)
    std_x = np.std(positions_x)
    std_y = np.std(positions_y)
    return mean_x, mean_y, std_x, std_y


def plot_styles(results):
    # Trier les résultats par 'quality' décroissante
    results_sorted = sorted(results, key=lambda r: r["quality"], reverse=True)

    # Garder seulement les 10 meilleurs
    top_results = results_sorted[:10]

    fig, ax = plt.subplots()

    for res in top_results:
        ax.scatter(
            res["mean_x"],
            res["mean_y"],
            s=50 + res["quality"] * 20,
            alpha=0.7,
            label=f'Reward: {res["quality"]}'
        )
        ax.errorbar(
            res["mean_x"],
            res["mean_y"],
            xerr=res["std_x"],
            yerr=res["std_y"],
            fmt='o',
            color='gray',
            alpha=0.5
        )

    ax.set_xlabel("Profondeur moyenne des équipes")
    ax.set_ylabel("Largeur moyenne des équipes")
    ax.set_title("Style de jeu du modèle")
    ax.legend()
    plt.show()

