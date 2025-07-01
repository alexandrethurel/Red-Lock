"""
Module : ball.py
Ballon Red Lock — version DEBUG avec rebonds.
"""

import numpy as np
import pygame
from tqdm import tqdm


class Ball:
    """
    Ballon Red Lock.

    Attributes:
        x (float): Position X.
        y (float): Position Y.
        vx (float): Vitesse X.
        vy (float): Vitesse Y.
        owner (object or None): Porteur du ballon.
        puissance_duel (float): Puissance calculée pour duel gardien/but.
        is_shot (bool): True = tir en cours.
    """

    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.vx = 0.0
        self.vy = 0.0
        self.owner = None
        self.puissance_duel = 0.0
        self.last_kicker = None
        self.ticks_since_kick = 9999
        self.is_shot = False
        self.last_shooter = None

    def update_position(self, field_width, field_height):
        if self.owner:
            self.x = self.owner.x
            self.y = self.owner.y
            self.ticks_since_kick = 9999
            if self.is_shot:
                #tqdm.write(f"[BALL] 🎯 Possédé ➜ Tir annulé.")
                pass
            self.is_shot = False
            #tqdm.write(f"[BALL] ✅ Suivi ➜ Ballon collé à Player#{getattr(self.owner, 'player_id', '?')}")
        else:
            old_x, old_y = self.x, self.y
            self.x += self.vx
            self.y += self.vy
            self.ticks_since_kick += 1

            # Rebonds haut/bas
            if self.y <= 0 or self.y >= field_height:
                self.vy *= -1
                self.y = max(0, min(self.y, field_height))
                #tqdm.write(f"[BALL] 🔁 Rebonds ligne horizontale ➜ vy inversé ➜ vy={self.vy:.2f}")

            # Option : rebonds lignes gauche/droite (à activer pour jeu arcade)
            # if self.x <= 0 or self.x >= field_width:
            #     self.vx *= -1
            #     self.x = max(0, min(self.x, field_width))
            #     #tqdm.write(f"[BALL] 🔁 Rebonds ligne verticale ➜ vx inversé ➜ vx={self.vx:.2f}")

            #tqdm.write(f"[BALL] ➡️ Libre ➜ Déplacement ({old_x:.2f},{old_y:.2f}) ➜ ({self.x:.2f},{self.y:.2f}) | vx={self.vx:.2f} vy={self.vy:.2f}")

    def kick(self, direction_x, direction_y, power, kicker=None, is_shot=False):
        """
        Donne une impulsion à la balle.
        """
        norm = np.sqrt(direction_x ** 2 + direction_y ** 2)
        if norm == 0:
            #tqdm.write("[BALL] ❌ Kick ignoré ➜ direction nulle.")
            return

        self.vx = (direction_x / norm) * power
        self.vy = (direction_y / norm) * power

        self.owner = None
        self.last_kicker = kicker
        self.ticks_since_kick = 0
        self.is_shot = is_shot

        #tqdm.write(f"[BALL] ⚡ Kick ➜ Kicker=Player#{getattr(kicker, 'player_id', '?')} | vx={self.vx:.2f} vy={self.vy:.2f} | Shot={self.is_shot}")

    def intercept(self, new_owner):
        """
        Interception ➜ Donne possession immédiate.
        """
        self.owner = new_owner
        self.vx = 0.0
        self.vy = 0.0
        self.is_shot = False
        #tqdm.write(f"[BALL] 🚫 Interception ➜ Ballon pris par Player#{getattr(new_owner, 'player_id', '?')}")

    def render(self, surface):
        """
        Dessine le ballon.
        """
        pos = (int(self.x), int(self.y))
        radius = 6
        pygame.draw.circle(surface, (255, 255, 255), pos, radius)
        pygame.draw.circle(surface, (0, 0, 0), pos, radius, 1)

        if self.is_shot:
            pygame.draw.circle(surface, (255, 0, 0), pos, radius + 4, 1)
        elif not self.owner:
            pygame.draw.circle(surface, (255, 215, 0), pos, radius + 2, 1)

    def __repr__(self):
        return f"<Ball (x={self.x:.2f}, y={self.y:.2f}, vx={self.vx:.2f}, vy={self.vy:.2f}, is_shot={self.is_shot})>"
