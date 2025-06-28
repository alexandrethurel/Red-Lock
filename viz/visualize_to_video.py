"""
visualize_to_video.py : Rejoue un match et enregistre une vidéo.
"""

import pygame
import imageio
import numpy as np
from env.core.game import Game
from env.metrics import compute_style_metrics, plot_styles

# === Init ===
env = Game()
model_path = "models/rl_agent_v1.pth"

# Charge le modèle sauvegardé
for agent in env.agents[:2]:
    agent.load_model(model_path)

# Paramètres vidéo
FPS = 30
frames = []

# Boucle avec capture
while env.running and env.ticks < env.max_ticks:
    env.handle_events()
    env.update()
    env.draw()

    # Capture la frame pygame → numpy
    frame = pygame.surfarray.array3d(env.screen)
    frame = np.transpose(frame, (1, 0, 2))  # Pygame est (width, height)
    frames.append(frame)

    env.clock.tick(FPS)

# === A la fin, export vidéo ===
video_path = "data/redlock_match.mp4"
imageio.mimsave(video_path, frames, fps=FPS)
print(f"✅ Vidéo sauvegardée : {video_path}")

# === Stats style ===
mean_x, mean_y, std_x, std_y = compute_style_metrics(env.positions_x, env.positions_y)
reward = env.score_bleu - env.score_rouge

print(f"Score BLEU : {env.score_bleu} | Score ROUGE : {env.score_rouge} | Reward : {reward}")

plot_styles([{
    "mean_x": mean_x,
    "mean_y": mean_y,
    "std_x": std_x,
    "std_y": std_y,
    "quality": reward
}])
