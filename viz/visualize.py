"""
visualize.py : Rejoue un match Red Lock, frame par frame, avec visualisation lente.
"""

from env.core.game import Game
from env.metrics import compute_style_metrics, plot_styles

# === Crée le match ===
env = Game()

# === Charge ton modèle RL ===
model_path = "models/rl_agent_v1.pth"
for agent in env.agents[:2]:
    agent.load_model(model_path)

# === Option : charger un autre modèle côté rouge ===
# for agent in env.agents[2:]:
#     agent.load_model("models/rl_agent_v2.pth")

# === Reset du tracking style ===
env.positions_x = []
env.positions_y = []

# === Boucle frame par frame ===
FPS = 30  # Mets 30 pour bien observer
env.running = True
env.ticks = 0

while env.running and env.ticks < env.max_ticks:
    env.handle_events()
    env.update()
    env.draw()
    env.clock.tick(FPS)  # <= C'est ça qui impose la vitesse frame par frame

print("\n=== Match terminé ===")

# === Stats après le match ===
reward = env.score_bleu - env.score_rouge
mean_x, mean_y, std_x, std_y = compute_style_metrics(env.positions_x, env.positions_y)

print(f"Score BLEU : {env.score_bleu} | Score ROUGE : {env.score_rouge} | Reward : {reward}")
print(f"Bloc => Moy X: {mean_x:.1f} | Moy Y: {mean_y:.1f} | Std X: {std_x:.1f} | Std Y: {std_y:.1f}")

plot_styles([{
    "mean_x": mean_x,
    "mean_y": mean_y,
    "std_x": std_x,
    "std_y": std_y,
    "quality": reward
}])
