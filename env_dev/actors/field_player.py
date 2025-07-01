"""
Module : field_player.py
Définit la classe FieldPlayer pour Red Lock — version DEBUG.
"""

import numpy as np
import pygame
from tqdm import tqdm


class FieldPlayer:
    """
    Joueur de champ Red Lock.

    Attributes:
        x (float): Position X.
        y (float): Position Y.
        stats (dict): Caractéristiques, somme = 100.
        has_ball (bool): Indique si le joueur possède le ballon.
        sprints_left (int): Sprints restants.
        color (tuple): Couleur RGB du joueur.
        player_id (int): Identifiant unique du joueur.
    """

    def __init__(self, x, y, stats, color=(0, 0, 255), player_id=1):
        """
        Initialise un joueur de champ Red Lock.
        """
        self.x = x
        self.y = y
        self.stats = stats
        self.has_ball = False
        self.sprints_left = int(stats.get("endurance", 0))
        self.color = color
        self.player_id = player_id
        #tqdm.write(f"[INIT] ✅ Player#{self.player_id} initialisé à ({self.x:.1f},{self.y:.1f})")

    def move(self, dx, dy, intensity=1):
        """
        Déplace le joueur selon un vecteur (dx, dy).
        """
        speed_factor = self.stats.get("vitesse", 0) / 100.0
        distance = np.sqrt(dx ** 2 + dy ** 2)

        if distance == 0:
            #tqdm.write(f"[MOVE] Player#{self.player_id} ➜ AUCUN déplacement (vecteur nul)")
            return

        dx /= distance
        dy /= distance

        step = intensity * speed_factor * 20
        old_x, old_y = self.x, self.y
        self.x += dx * step 
        self.y += dy * step 

        if intensity == 3 and self.sprints_left > 0:
            self.sprints_left -= 1
            #tqdm.write(f"[MOVE] Player#{self.player_id} ➜ Sprint ! Sprints restants: {self.sprints_left}")

        #tqdm.write(f"[MOVE] Player#{self.player_id} ➜ ({old_x:.1f},{old_y:.1f}) ➜ ({self.x:.1f},{self.y:.1f}) | Intensité={intensity}")

    def can_pass(self):
        """Indique si le joueur peut passer le ballon."""
        return self.has_ball

    def can_shoot(self):
        """Indique si le joueur peut tirer."""
        return self.has_ball

    def can_dribble(self):
        """Indique si le joueur peut dribbler."""
        return self.has_ball

    def render(self, surface):
        """
        Dessine le joueur sur la surface Pygame.
        """
        pos = (int(self.x), int(self.y))
        radius = 12

        pygame.draw.circle(surface, self.color, pos, radius)
        pygame.draw.circle(surface, (255, 255, 255), pos, radius, 2)

        if self.has_ball:
            pygame.draw.circle(surface, (255, 215, 0), pos, radius + 4, 2)

        end_pos = (pos[0] + 15, pos[1])
        pygame.draw.line(surface, (200, 200, 200), pos, end_pos, 2)

        font = pygame.font.SysFont("Arial", 14, bold=True)
        id_text = font.render(str(self.player_id), True, (0, 0, 0))
        id_rect = id_text.get_rect(center=pos)
        surface.blit(id_text, id_rect)

    def __repr__(self):
        """
        Représentation textuelle pour debug.
        """
        return (
            f"<FieldPlayer#{self.player_id} (x={self.x:.2f}, y={self.y:.2f}, "
            f"has_ball={self.has_ball}, sprints_left={self.sprints_left})>"
        )
