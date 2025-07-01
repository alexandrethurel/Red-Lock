"""
Module : goalkeeper.py
Définit la classe GoalKeeper pour Red Lock — version CLEAN.
"""

import numpy as np
import pygame
from tqdm import tqdm


class GoalKeeper:
    """
    Gardien de but Red Lock.

    Attributes:
        x (float): Position X.
        y (float): Position Y.
        stats (dict): Statistiques du gardien.
        has_ball (bool): Possède le ballon ?
        color (tuple): Couleur RGB.
        player_id (int): Identifiant du joueur.
    """

    def __init__(self, x, y, stats, color=(0, 0, 200), player_id=1):
        """
        Initialise le gardien.

        Args:
            x (float): Position X initiale.
            y (float): Position Y initiale.
            stats (dict): Statistiques.
            color (tuple): Couleur RGB.
            player_id (int): ID joueur.
        """
        self.x = x
        self.y = y
        self.stats = stats
        self.has_ball = False
        self.color = color
        self.player_id = player_id
        # tqdm.write(f"[INIT GK] ✅ GoalKeeper#{self.player_id} prêt à ({self.x:.1f},{self.y:.1f})")

    def move(self, dx, dy, intensity=0):
        """
        Déplace le gardien dans une zone restreinte.

        Args:
            dx (float): Déplacement en X.
            dy (float): Déplacement en Y.
            intensity (float): Non utilisé ici.
        """
        max_step = 1.0
        distance = np.hypot(dx, dy)
        if distance == 0:
            return

        dx /= distance
        dy /= distance

        old_x, old_y = self.x, self.y
        self.x += dx * max_step
        self.y += dy * max_step

        # tqdm.write(f"[MOVE GK] GoalKeeper#{self.player_id} ➜ ({old_x:.1f},{old_y:.1f}) ➜ ({self.x:.1f},{self.y:.1f})")

    def can_save(self):
        """
        Indique si le gardien peut tenter un arrêt.

        Returns:
            bool: Toujours True.
        """
        return True

    def can_intercept(self):
        """
        Indique si le gardien peut intercepter une balle proche.

        Returns:
            bool: Toujours True.
        """
        return True

    def render(self, surface):
        """
        Affiche le gardien sur l'écran.

        Args:
            surface (pygame.Surface): Surface Pygame.
        """
        rect_size = 22
        # Centrer le carré sur (x, y)
        rect_pos = (int(self.x - rect_size // 2), int(self.y - rect_size // 2))
        rect = pygame.Rect(rect_pos, (rect_size, rect_size))

        # Corps du gardien
        pygame.draw.rect(surface, self.color, rect)
        pygame.draw.rect(surface, (255, 255, 255), rect, 2)

        # Indique s'il a le ballon
        if self.has_ball:
            highlight_rect = rect.inflate(8, 8)
            pygame.draw.rect(surface, (255, 215, 0), highlight_rect, 2)

        # ID GARDIEN
        font = pygame.font.SysFont("Arial", 16, bold=True)
        text = font.render("G", True, (0, 0, 0))
        text_rect = text.get_rect(center=(self.x, self.y))
        surface.blit(text, text_rect)

        # Ligne de direction
        end_pos = (int(self.x + 15), int(self.y))
        pygame.draw.line(surface, (255, 255, 255), (self.x, self.y), end_pos, 2)

    def __repr__(self):
        """
        Représentation textuelle pour debug.

        Returns:
            str: Représentation.
        """
        return (
            f"<GoalKeeper#{self.player_id} (x={self.x:.2f}, y={self.y:.2f}, "
            f"has_ball={self.has_ball})>"
        )
