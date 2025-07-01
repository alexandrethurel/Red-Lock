"""
visualize.py : Rejoue un match Red Lock, frame par frame, avec visualisation lente.
"""
import os
import sys

# Ajoute la racine du projet au path Python
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))

from env_dev.core.game import Game
from env_dev.metrics import compute_style_metrics, plot_styles

# === Crée le match ===
env_dev = Game()

# === Charge ton modèle RL ===
model_path = "data/models/rl_agent_v1_ep2840.pth"
for agent in env_dev.match.agents[:2]:
    agent.load_model(model_path)

# === Option : charger un autre modèle côté rouge ===
# for agent in env_dev.agents[2:]:
#     agent.load_model("models/rl_agent_v2.pth")

# === Reset du tracking style ===
env_dev.positions_x = []
env_dev.positions_y = []

# === Boucle frame par frame ===
FPS = 30  # Mets 30 pour bien observer
env_dev.running = True
env_dev.ticks = 0

while env_dev.running and env_dev.match.ticks < env_dev.match.max_ticks:
    env_dev.handle_events()
    env_dev.update()
    env_dev.draw()
    env_dev.clock.tick(FPS)

print("\n=== Match terminé ===")

# === Stats après le match ===
reward = env_dev.score_bleu - env_dev.score_rouge
mean_x, mean_y, std_x, std_y = compute_style_metrics(env_dev.positions_x, env_dev.positions_y)

print(f"Score BLEU : {env_dev.score_bleu} | Score ROUGE : {env_dev.score_rouge} | Reward : {reward}")
print(f"Bloc => Moy X: {mean_x:.1f} | Moy Y: {mean_y:.1f} | Std X: {std_x:.1f} | Std Y: {std_y:.1f}")

plot_styles([{
    "mean_x": mean_x,
    "mean_y": mean_y,
    "std_x": std_x,
    "std_y": std_y,
    "quality": reward
}])
