"""
visualize_to_video.py : Rejoue un match et enregistre une vidéo.
"""

import pygame
import imageio
import numpy as np
from env_dev_dev.core.game import Game
from env_dev_dev.metrics import compute_style_metrics, plot_styles

# === Init ===
env_dev = Game()
model_path = "models/rl_agent_v1.pth"

# Charge le modèle sauvegardé
for agent in env_dev.agents[:2]:
    agent.load_model(model_path)

# Paramètres vidéo
FPS = 30
frames = []

# Boucle avec capture
while env_dev.running and env_dev.ticks < env_dev.max_ticks:
    env_dev.handle_events()
    env_dev.update()
    env_dev.draw()

    # Capture la frame pygame → numpy
    frame = pygame.surfarray.array3d(env_dev.screen)
    frame = np.transpose(frame, (1, 0, 2))  # Pygame est (width, height)
    frames.append(frame)

    env_dev.clock.tick(FPS)

# === A la fin, export vidéo ===
video_path = "data/redlock_match.mp4"
imageio.mimsave(video_path, frames, fps=FPS)
print(f"✅ Vidéo sauvegardée : {video_path}")

# === Stats style ===
mean_x, mean_y, std_x, std_y = compute_style_metrics(env_dev.positions_x, env_dev.positions_y)
reward = env_dev.score_bleu - env_dev.score_rouge

print(f"Score BLEU : {env_dev.score_bleu} | Score ROUGE : {env_dev.score_rouge} | Reward : {reward}")

plot_styles([{
    "mean_x": mean_x,
    "mean_y": mean_y,
    "std_x": std_x,
    "std_y": std_y,
    "quality": reward
}])
