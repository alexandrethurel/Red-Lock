"""
Module : match.py
Coordonne la simulation du match Red Lock.
"""

from tqdm import tqdm
from env_dev_dev.actors.goalkeeper import GoalKeeper
import numpy as np

from env_dev_dev.actions.actions import (
    ramasser_balle,
    passer,
    tirer,
    dribbler,
    tenter_interception
)
from env_dev_dev.core.setup import create_match_entities
from env_dev_dev.core.logic import handle_goal, reengager, relancer_gardien, handle_goal_kick
from env_dev_dev.core.reward import RewardEngine


class Match:
    """
    Simulation principale du match Red Lock.
    """

    def __init__(self, width, height, opponent_mode="random", opponent_model_path=None):
        """
        Initialise le match.

        Args:
            width (int): Largeur du terrain.
            height (int): Hauteur du terrain.
            opponent_mode (str): "random" ou "model".
            opponent_model_path (str, optional): Chemin vers modèle si opponent_mode == "model".
        """
        self.width = width
        self.height = height

        # Entités principales configurées dynamiquement
        self.players, self.keepers, self.agents, self.ball = create_match_entities(
            opponent_mode=opponent_mode,
            opponent_model_path=opponent_model_path
        )

        # Engine pour reward RL
        self.reward_engine = RewardEngine()

        # Scores
        self.score_bleu = 0
        self.score_rouge = 0

        # Temps
        self.ticks = 0
        self.max_ticks = 60 * 60 * 5

        self.just_scored = False
        self.just_scored_ticks = 0

    def update(self):
        """
        Met à jour l'état logique du match à chaque tick.
        """
        if self.just_scored:
            self.just_scored_ticks += 1
            if self.just_scored_ticks < 30:
                return
            else:
                self.just_scored = False

        entities = self.players + self.keepers

        for agent, entity in zip(self.agents, entities):
            action = agent.decide_action(entity, {
                "players": self.players,
                "keepers": self.keepers,
                "ball": self.ball,
                "but_adverse": (
                    self.width if entity in self.players[:2] + [self.keepers[0]] else 0,
                    self.height // 2
                ),
                "field_width": self.width
            })

            if action["type"] == "passer":
                puissance = passer(entity, action["cible"], self.ball)
                self.ball.last_passer = entity

                self.reward_engine.apply_forward_pass_reward(entity, action["cible"])

                for opponent in self.players + self.keepers:
                    if opponent != entity and opponent != action["cible"]:
                        intercepted = tenter_interception(opponent, puissance, self.ball)
                        if intercepted:
                            self.reward_engine.apply_interception_reward(opponent, entity)

            elif action["type"] == "tirer":
                if entity.color == (0, 0, 255):
                    but_x = self.width - 5  # But côté droit
                else:
                    but_x = 5  # But côté gauche
                but_y = self.height // 2

                tirer(entity, but_x, but_y, self.ball)

            elif action["type"] == "se_deplacer":
                entity.move(action["dir_x"], action["dir_y"], action.get("intensity", 1))

                if (
                    entity.x < 0 or entity.x > self.width
                    or entity.y < 0 or entity.y > self.height
                ):
                    self.reward_engine.apply_out_of_bounds_malus(entity)

            elif action["type"] == "dribbler":
                if isinstance(entity, GoalKeeper):
                    continue
                dribbler(entity, action["dir_x"], action["dir_y"], action.get("intensity", 1))

            elif action["type"] == "relancer":
                teammates = [p for p in self.players if p.color == entity.color]
                relancer_gardien(entity, teammates, passer, self.ball)

            if not isinstance(entity, GoalKeeper):
                teammates = [
                    p for p in self.players if p.color == entity.color and p != entity
                ]
                opponents = [
                    p for p in self.players if p.color != entity.color
                ]
                self.reward_engine.apply_get_open_reward(
                    entity, self.ball, teammates, opponents
                )

        self.ball.update_position(self.width, self.height)

        if self.ball.owner is None:
            for p in self.players + self.keepers:
                if ramasser_balle(p, self.ball):
                    self.reward_engine.apply_ball_recovery_reward(p)

        self.check_goals()

        self.ticks += 1
        if self.ticks >= self.max_ticks:
            tqdm.write(
                f"[MATCH TERMINE] ⏱️ BLEU: {self.score_bleu} | ROUGE: {self.score_rouge}"
            )


            
    def check_goals(self):
        """
        Vérifie but ou sortie de but.
        """
        if self.just_scored:
            return

        # BUT côté gauche
        if self.ball.x < 10:
            if self.ball.is_shot:
                if handle_goal(self.ball, self.keepers[0], "rouge", self.players, self.keepers, self.reward_engine):
                    self.score_rouge += 1
                    reengager(self.ball, self.players, self.keepers, self.width, self.height, engage_team="blue")
                    self.just_scored = True
                    self.just_scored_ticks = 0
            else:
                handle_goal_kick(self.ball, self.keepers[0])

        # BUT côté droit
        elif self.ball.x > self.width - 10:
            if self.ball.is_shot:
                if handle_goal(self.ball, self.keepers[1], "bleu", self.players, self.keepers, self.reward_engine):
                    self.score_bleu += 1
                    reengager(self.ball, self.players, self.keepers, self.width, self.height, engage_team="rouge")
                    self.just_scored = True
                    self.just_scored_ticks = 0
            else:
                handle_goal_kick(self.ball, self.keepers[1])
