"""
Module : event_handler.py
Gère les événements utilisateur Pygame.
"""

import pygame


class EventHandler:
    """
    Gestionnaire d'événements utilisateur.
    """

    def __init__(self, game):
        """
        Initialise l'event handler.

        Args:
            game (Game): Instance principale du jeu.
        """
        self.game = game

    def handle_events(self):
        """
        Traite les événements Pygame.
        """
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.game.running = False
