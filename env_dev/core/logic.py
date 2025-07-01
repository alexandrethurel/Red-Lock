"""
Module : logic.py
Regroupe la logique des duels, buts et relances pour Red Lock.
"""

from tqdm import tqdm
import numpy as np
from env_dev.actors.goalkeeper import GoalKeeper


def relancer_gardien(gk, teammates, passer_fn, ball):
    """
    Relance propre du gardien ➜ vers un FieldPlayer allié UNIQUEMENT,
    jamais un gardien ni lui-même.
    """
    field_teammates = [
        p for p in teammates
        if not isinstance(p, GoalKeeper)
        and p.color == gk.color
        and p != gk
    ]
    if not field_teammates:
        #tqdm.write("[RELANCE GK] ❌ Aucun coéquipier dispo pour relancer.")
        return

    cible = np.random.choice(field_teammates)

    distance = np.hypot(cible.x - gk.x, cible.y - gk.y)
    if distance < 30:
        #tqdm.write("[RELANCE GK] ⚠️ Cible trop proche ➜ relance annulée pour éviter boucle.")
        return

    passer_fn(gk, cible, ball)
    gk.has_ball = False
    #tqdm.write(f"[RELANCE GK] ✅ Gardien relance vers Player#{getattr(cible, 'player_id', '?')}")


def handle_goal(ball, keeper, side, players, keepers, rewards):
    """
    Duel tireur vs gardien ➜ Gère but ou arrêt.
    """
    if not ball.is_shot:
        #tqdm.write("[DUEL] 🚫 Ballon non tiré ➜ Pas de but possible.")
        return False

    stat_reflex = keeper.stats["réflexes"] / 100.0
    pu_tir = ball.puissance_duel

    #tqdm.write(f"[DUEL TIR] ⚔️ Reflex={stat_reflex:.2f} vs Puissance_tir={pu_tir:.2f}")

    if stat_reflex >= pu_tir:
        for p in players + keepers:
            p.has_ball = False
        keeper.has_ball = True
        ball.owner = keeper
        ball.x, ball.y = keeper.x, keeper.y
        ball.vx = ball.vy = 0
        #tqdm.write(f"[ARRET] 🧤 Gardien garde la balle !")
        return False
    else:
        if side == "rouge":
            tqdm.write("\033[31m[BUT] 🚨 ROUGE marque !\033[0m")
        else:
            tqdm.write("\033[34m[BUT] 🚨 BLEU marque !\033[0m")
        rewards.apply_goal_rewards(ball, players)
        return True


def reengager(ball, players, keepers, width, height, engage_team="blue"):
    """
    Replace tous les joueurs et redonne la balle après un but.

    Args:
        ball (Ball): Ballon.
        players (list): Joueurs.
        keepers (list): Gardiens.
        width (int): Largeur terrain.
        height (int): Hauteur terrain.
        engage_team (str, optional): "blue" ou "red".
    """
    #tqdm.write(f"[REENGAGER] 🔄 Engagement par {engage_team.upper()}")

    # Centre la balle
    ball.x = width / 2
    ball.y = height / 2
    ball.vx = 0
    ball.vy = 0
    ball.owner = None
    ball.puissance_duel = 0

    # Replace chaque joueur à sa position initiale (il faut que chaque joueur ait start_x / start_y)
    for p in players + keepers:
        p.x = getattr(p, "start_x", p.x)
        p.y = getattr(p, "start_y", p.y)
        p.has_ball = False

    # Donne la balle au premier joueur de la couleur concernée
    if engage_team == "blue":
        engager = next(p for p in players if p.color == (0, 0, 255))
    else:
        engager = next(p for p in players if p.color == (255, 0, 0))

    engager.has_ball = True
    ball.owner = engager

    #tqdm.write(f"[REENGAGER] ✅ Balle donnée à Player#{engager.player_id} au centre.")
    
def handle_goal_kick(ball, keeper):
    """
    Gère une sortie de but ➜ Le gardien récupère la balle pour relancer.
    """
    keeper.has_ball = True
    ball.owner = keeper
    ball.vx = ball.vy = 0
    #tqdm.write(f"[GOAL KICK] 🧤 Sortie de but ➜ GK#{keeper.player_id} prend la balle pour dégager.")
