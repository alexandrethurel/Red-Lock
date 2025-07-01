"""
Module : renderer.py
Affichage graphique du match Red Lock — version améliorée.
"""

import pygame


class Renderer:
    """
    Gère le rendu Pygame du match Red Lock.
    """

    def __init__(self, screen, match):
        """
        Initialise le renderer.

        Args:
            screen (pygame.Surface): Surface Pygame.
            match (Match): État courant du match.
        """
        self.screen = screen
        self.match = match
        self.font_main = pygame.font.SysFont("Arial", 32, bold=True)
        self.font_small = pygame.font.SysFont("Arial", 16)
        self.width = match.width
        self.height = match.height

    def draw_field(self):
        """
        Dessine le terrain avec lignes et buts.
        """
        field_color = (50, 150, 50)
        line_color = (255, 255, 255)

        self.screen.fill(field_color)

        # Ligne médiane
        pygame.draw.line(
            self.screen, line_color,
            (self.width // 2, 0), (self.width // 2, self.height), 2
        )

        # Cercle central
        pygame.draw.circle(
            self.screen, line_color,
            (self.width // 2, self.height // 2), 60, 2
        )

        # Buts
        goal_width = 10
        goal_height = 100
        pygame.draw.rect(
            self.screen, line_color,
            pygame.Rect(0, self.height // 2 - goal_height // 2, goal_width, goal_height), 2
        )
        pygame.draw.rect(
            self.screen, line_color,
            pygame.Rect(self.width - goal_width, self.height // 2 - goal_height // 2, goal_width, goal_height), 2
        )

    def draw_players(self):
        """
        Dessine joueurs et gardiens avec ID.
        """
        for player in self.match.players:
            player.render(self.screen)
            # Affiche ID joueur
            if hasattr(player, 'player_id'):
                label = self.font_small.render(str(player.player_id), True, (255, 255, 255))
                self.screen.blit(label, (player.x - 5, player.y - 25))

        for keeper in self.match.keepers:
            keeper.render(self.screen)

    def draw_ball(self):
        """
        Dessine le ballon.
        """
        self.match.ball.render(self.screen)

    def draw_scoreboard(self):
        """
        Affiche le score.
        """
        score_text = f"BLEU {self.match.score_bleu}  -  {self.match.score_rouge} ROUGE"
        text_surface = self.font_main.render(score_text, True, (255, 255, 255))
        text_rect = text_surface.get_rect(center=(self.width // 2, 30))
        self.screen.blit(text_surface, text_rect)

    def draw_debug_info(self):
        """
        Optionnel : debug info, par ex. ticks.
        """
        ticks_text = f"Ticks: {self.match.ticks}"
        ticks_surface = self.font_small.render(ticks_text, True, (200, 200, 200))
        self.screen.blit(ticks_surface, (10, 10))

    def draw(self):
        """
        Affiche tout le rendu complet.
        """
        self.draw_field()
        self.draw_players()
        self.draw_ball()
        self.draw_scoreboard()
        self.draw_debug_info()
        pygame.display.flip()
