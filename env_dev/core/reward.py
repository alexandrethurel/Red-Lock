"""
Module : reward.py
Gestion centralisée des rewards/malus pour agents RL.
"""

from tqdm import tqdm
from env_dev_dev.agents.rl_agent import RLAgent
import numpy as np


class RewardEngine:
    """
    Moteur de récompenses/malus pour les RLAgents (équipe BLEUE principalement).
    """

    def __init__(self):
        pass

    def is_blue(self, player):
        """
        Vérifie si le joueur est bleu.
        """
        if hasattr(player, "color"):
            return player.color == (0, 0, 255) or player.color[2] >= 200
        return False

    def apply_goal_rewards(self, ball, players):
        """
        Récompense le dernier tireur et passeur pour un but marqué.
        Applique un gros malus à l'équipe adverse.
        """
        if hasattr(ball, "last_shooter") and hasattr(ball.last_shooter, "agent"):
            if isinstance(ball.last_shooter.agent, RLAgent) and self.is_blue(ball.last_shooter):
                ball.last_shooter.agent.local_rewards.append(100.0)
                tqdm.write(f"[+REWARD] ✅ BUT | Player#{getattr(ball.last_shooter, 'player_id', '?')} : +100")

        if (
            hasattr(ball, "last_passer")
            and ball.last_passer != ball.last_shooter
            and hasattr(ball.last_passer, "agent")
        ):
            if isinstance(ball.last_passer.agent, RLAgent) and self.is_blue(ball.last_passer):
                ball.last_passer.agent.local_rewards.append(5.0)

        if hasattr(ball.last_shooter, "color"):
            if self.is_blue(ball.last_shooter):
                self.apply_goal_conceded_malus(team_color=(255, 0, 0), players=players)
            else:
                self.apply_goal_conceded_malus(team_color=(0, 0, 255), players=players)

    def apply_goal_conceded_malus(self, team_color, players, malus_value=-50.0):
        """
        Malus pour tous les RLAgents de l'équipe qui encaisse.
        """
        for p in players:
            if hasattr(p, "agent") and isinstance(p.agent, RLAgent) and p.color == team_color:
                p.agent.local_rewards.append(malus_value)

    def apply_interception_reward(self, intercepteur, passeur):
        """
        Récompense un intercepteur RL bleu et punit le passeur RL bleu.
        """
        if hasattr(intercepteur, "agent") and isinstance(intercepteur.agent, RLAgent) and self.is_blue(intercepteur):
            intercepteur.agent.local_rewards.append(0.2)

        if hasattr(passeur, "agent") and isinstance(passeur.agent, RLAgent) and self.is_blue(passeur):
            passeur.agent.local_rewards.append(-0.02)

    def apply_out_of_bounds_malus(self, joueur):
        """
        Malus pour sortie de terrain (RL bleu uniquement).
        """
        if hasattr(joueur, "agent") and isinstance(joueur.agent, RLAgent) and self.is_blue(joueur):
            joueur.agent.local_rewards.append(-1.0)

    def apply_forward_pass_reward(self, passeur, cible):
        """
        Reward pour une passe vers l'avant réussie (RL bleu uniquement).
        """
        if hasattr(passeur, "agent") and isinstance(passeur.agent, RLAgent):
            if self.is_blue(passeur) and self.is_blue(cible):
                if cible.x > passeur.x:
                    passeur.agent.local_rewards.append(0.05)

    def apply_ball_recovery_reward(self, joueur):
        """
        Reward pour récupération de balle (RL bleu uniquement).
        """
        if hasattr(joueur, "agent") and isinstance(joueur.agent, RLAgent) and self.is_blue(joueur):
            joueur.agent.local_rewards.append(0.2)

    def apply_get_open_reward(self, joueur, ball, teammates, opponents):
        """
        Reward pour se démarquer intelligemment.
        """
        if (
            not joueur.has_ball
            and hasattr(joueur, "agent")
            and isinstance(joueur.agent, RLAgent)
            and self.is_blue(joueur)
        ):
            reward = 0

            if ball.owner and ball.owner.color == joueur.color:
                dx = ball.owner.x - joueur.x
                if abs(dx) > 50 and dx > 0:
                    reward += 0.02

            for opp in opponents:
                dist_opp = np.hypot(joueur.x - opp.x, joueur.y - opp.y)
                if dist_opp < 50:
                    reward += 0.02

            if ball.owner and ball.owner != joueur:
                dist_p = np.hypot(joueur.x - ball.owner.x, joueur.y - ball.owner.y)
                if dist_p < 30:
                    reward -= 0.001

            if reward != 0:
                joueur.agent.local_rewards.append(reward)

    def apply_possession_duration_reward(self, player, team_possession_ticks):
        """
        Bonus pour conserver le ballon longtemps collectivement.
        """
        if hasattr(player, "agent") and isinstance(player.agent, RLAgent) and self.is_blue(player):
            if team_possession_ticks > 50:
                player.agent.local_rewards.append(0.0)

    def apply_short_pass_reward(self, passer, receiver):
        """
        Bonus pour passe courte.
        """
        if hasattr(passer, "agent") and isinstance(passer.agent, RLAgent) and self.is_blue(passer):
            distance = np.hypot(passer.x - receiver.x, passer.y - receiver.y)
            if distance < 50:
                passer.agent.local_rewards.append(0.0)

    def apply_patience_reward(self, player, has_forced_action):
        """
        Bonus si pas d'action forcée (tir précipité par ex).
        """
        if hasattr(player, "agent") and isinstance(player.agent, RLAgent) and self.is_blue(player):
            if not has_forced_action:
                player.agent.local_rewards.append(0.0)

    def apply_hold_ball_reward(self, player, hold_ticks):
        """
        Bonus pour garder le ballon longtemps individuellement.
        """
        if hasattr(player, "agent") and isinstance(player.agent, RLAgent) and self.is_blue(player):
            if player.has_ball and hold_ticks > 30:
                player.agent.local_rewards.append(0.0)

    def apply_fast_attack_after_recovery_reward(self, player, ticks_since_recovery, did_attack):
        """
        Bonus pour déclenchement rapide après récupération.
        """
        if hasattr(player, "agent") and isinstance(player.agent, RLAgent) and self.is_blue(player):
            if ticks_since_recovery < 30 and did_attack:
                player.agent.local_rewards.append(0.0)

    def apply_compact_block_reward(self, players, field_height):
        """
        Bonus pour bloc bas/médian compact.
        """
        blue_positions = [p.y for p in players if hasattr(p, "agent") and isinstance(p.agent, RLAgent) and self.is_blue(p)]
        if blue_positions:
            spread = max(blue_positions) - min(blue_positions)
            if spread < field_height * 0.5:
                for p in players:
                    if hasattr(p, "agent") and isinstance(p.agent, RLAgent) and self.is_blue(p):
                        p.agent.local_rewards.append(0.0)

    def apply_depth_run_reward(self, player, last_defender_x):
        """
        Bonus pour course en profondeur.
        """
        if hasattr(player, "agent") and isinstance(player.agent, RLAgent) and self.is_blue(player):
            if player.x > last_defender_x:
                player.agent.local_rewards.append(0.0)

    def apply_long_ball_reward(self, passer, receiver):
        """
        Bonus pour long ballon vers l'avant.
        """
        if hasattr(passer, "agent") and isinstance(passer.agent, RLAgent) and self.is_blue(passer):
            distance = np.hypot(passer.x - receiver.x, passer.y - receiver.y)
            if distance > 200:
                passer.agent.local_rewards.append(0.0)

    def apply_duel_win_reward(self, winner):
        """
        Bonus pour duel gagné.
        """
        if hasattr(winner, "agent") and isinstance(winner.agent, RLAgent) and self.is_blue(winner):
            winner.agent.local_rewards.append(0.0)

    def apply_high_recovery_reward(self, player, goal_x):
        """
        Bonus pour récupération très haute.
        """
        if hasattr(player, "agent") and isinstance(player.agent, RLAgent) and self.is_blue(player):
            if abs(player.x - goal_x) < 200:
                player.agent.local_rewards.append(0.0)

    def apply_lines_tightness_reward(self, players):
        """
        Bonus pour lignes serrées.
        """
        blue_x = [p.x for p in players if hasattr(p, "agent") and isinstance(p.agent, RLAgent) and self.is_blue(p)]
        if blue_x:
            spread = max(blue_x) - min(blue_x)
            if spread < 300:
                for p in players:
                    if hasattr(p, "agent") and isinstance(p.agent, RLAgent) and self.is_blue(p):
                        p.agent.local_rewards.append(0.0)

    def apply_unrealistic_movement_malus(self, joueur, last_dx, last_dy, threshold=0.8):
        """
        Malus pour mouvement pas naturel.
        """
        if hasattr(joueur, "agent") and isinstance(joueur.agent, RLAgent) and self.is_blue(joueur):
            variation = abs(last_dx) + abs(last_dy)
            if variation > threshold:
                joueur.agent.local_rewards.append(0.0)

    def apply_no_shot_malus(self, joueur, possession_ticks):
        """
        Malus si aucun tir après longue possession.
        """
        if hasattr(joueur, "agent") and isinstance(joueur.agent, RLAgent) and self.is_blue(joueur):
            if joueur.has_ball and possession_ticks > 50:
                joueur.agent.local_rewards.append(0.0)

    def apply_clean_sheet_reward(self, team_players, no_goal_ticks, threshold=500):
        """
        Bonus collectif si pas de but encaissé pendant un moment.
        """
        if no_goal_ticks >= threshold:
            for p in team_players:
                if hasattr(p, "agent") and isinstance(p.agent, RLAgent) and self.is_blue(p):
                    p.agent.local_rewards.append(0.0)
