"""
Module : game.py
Point d'entrée principal du jeu Red Lock.
"""

import pygame
from tqdm import tqdm

from env_dev.core.match import Match
from env_dev.core.event_handler import EventHandler
from env_dev.core.renderer import Renderer  

class Game:
    """
    Wrapper principal du jeu Red Lock.
    Gère Pygame, Match, événements et rendu.
    """

    def __init__(self, width=800, height=600, opponent_mode="random", opponent_model_path=None):
        """
        Initialise le jeu complet (Pygame, match, gestionnaire d'événements et rendu).

        Args:
            width (int, optional): Largeur de la fenêtre. Par défaut 800.
            height (int, optional): Hauteur de la fenêtre. Par défaut 600.
        """
        pygame.init()
        self.width = width
        self.height = height
        self.screen = pygame.display.set_mode((width, height))
        pygame.display.set_caption("Red Lock")
        self.clock = pygame.time.Clock()
        self.running = True

        self.match = Match(width, height)
        self.event_handler = EventHandler(self)
        self.renderer = Renderer(self.screen, self.match)

    def handle_events(self):
        """
        Délègue la gestion des événements à EventHandler.
        """
        self.event_handler.handle_events()

    def update(self):
        """
        Met à jour le match et stoppe dès qu’un but est marqué.
        """
        self.match.update()

        if self.match.score_bleu > 0 or self.match.score_rouge > 0:
            tqdm.write(f"[FIN] But marqué ! Score ➜ BLEU {self.match.score_bleu} - ROUGE {self.match.score_rouge}")
            self.running = False

        self.clock.tick(120)

    def draw(self):
        """
        Affiche le rendu du match via le Renderer.
        """
        self.renderer.draw()

    def run(self):
        """
        Boucle principale du jeu Red Lock.
        """
        while self.running:
            self.handle_events()
            self.update()
            self.draw()
            self.clock.tick(120)
        pygame.quit()
