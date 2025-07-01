"""
Module : actions.py
Actions + duels Red Lock — version DEBUG.
"""

import numpy as np
from tqdm import tqdm
from env_dev_dev.actors.goalkeeper import GoalKeeper


def passer(passeur, cible, ball):
    """
    Passe : direction, puissance et état ballon.
    """
    if cible == passeur:
        #tqdm.write(f"[PASSER] ❌ ERREUR ➜ Le joueur ne peut PAS se passer le ballon à lui-même !")
        return 0.0

    direction_x = cible.x - passeur.x
    direction_y = cible.y - passeur.y
    distance = np.hypot(direction_x, direction_y)
    stat_passe = passeur.stats.get("précision_passe", 0) / 100.0
    puissance_duel = stat_passe * max(1, 300 / distance)

    ball.kick(direction_x, direction_y, power=10)
    ball.is_shot = False
    ball.puissance_duel = puissance_duel
    passeur.has_ball = False
    ball.last_passer = passeur
    ball.last_kicker = passeur

    #tqdm.write(f"[PASSER] ✅ Player#{getattr(passeur, 'player_id', '?')} passe ➜ Player#{getattr(cible, 'player_id', '?')} | Distance={distance:.2f} | Puissance_duel={puissance_duel:.4f}")
    return puissance_duel


def tirer(tireur, but_x, but_y, ball):
    """
    Tir vers le but.
    """
    direction_x = but_x - tireur.x
    direction_y = but_y - tireur.y
    distance = np.hypot(direction_x, direction_y)
    stat_tir = tireur.stats.get("précision_tir", 0) / 100.0
    puissance_duel = stat_tir * max(1, 500 / distance)

    ball.kick(direction_x, direction_y, power=10, kicker=tireur, is_shot=True)
    ball.puissance_duel = puissance_duel
    tireur.has_ball = False
    ball.last_shooter = tireur

    #tqdm.write(f"[TIRER] 🎯 Player#{getattr(tireur, 'player_id', '?')} tire | Distance={distance:.2f} | Puissance_duel={puissance_duel:.4f}")
    return puissance_duel


def dribbler(joueur, dir_x, dir_y, intensity=1):
    """
    Dribble : mouvement et puissance.
    """
    joueur.move(dir_x, dir_y, intensity=intensity)
    stat_dribble = joueur.stats.get("dribble", 0) / 100.0
    puissance_duel = stat_dribble * intensity

    #tqdm.write(f"[DRIBBLER] 🏃‍♂️ Player#{getattr(joueur, 'player_id', '?')} dribble | Dir=({dir_x:.2f},{dir_y:.2f}) | Intensité={intensity} | Puissance_duel={puissance_duel:.4f}")
    return puissance_duel


def ramasser_balle(joueur, ball):
    """
    Ramasse la balle ➜ Vérifie conditions.
    """
    distance = np.hypot(ball.x - joueur.x, ball.y - joueur.y)

    if joueur == ball.last_kicker and ball.ticks_since_kick < 10:
        #tqdm.write(f"[RAMASSER] ⚠️ Player#{getattr(joueur, 'player_id', '?')} Ignore : vient de passer.")
        return False 

    if ball.is_shot and not isinstance(joueur, GoalKeeper):
        return False 

    if distance < 20 and ball.owner is None:
        joueur.has_ball = True
        ball.owner = joueur
        ball.vx = 0
        ball.vy = 0
        ball.puissance_duel = 0

        #tqdm.write(f"[RAMASSER] ✅ Player#{getattr(joueur, 'player_id', '?')} récupère la balle.")
        return True  

    return False  


def tenter_tacle(tacleur, dribbleur):
    """
    Duel tacle vs dribble.
    """
    stat_tacle = tacleur.stats.get("tacle", 0) / 100.0
    stat_dribble = dribbleur.stats.get("dribble", 0) / 100.0

    if stat_tacle > stat_dribble:
        dribbleur.has_ball = False
        #tqdm.write(f"[TACLE] 🛑 Player#{getattr(tacleur, 'player_id', '?')} réussit le tacle sur Player#{getattr(dribbleur, 'player_id', '?')}")


def tenter_interception(intercepteur, puissance_passe, ball):
    """
    Intercepte une passe ➜ Pas sur tir. Gardien interdit.
    """
    if ball.is_shot:
        return False

    if isinstance(intercepteur, GoalKeeper):
        return False

    stat_inter = intercepteur.stats.get("interception", 0) / 100.0

    if stat_inter > puissance_passe:
        intercepteur.has_ball = True
        ball.intercept(intercepteur)
        #tqdm.write(f"[INTERCEPT] 🚫 Player#{getattr(intercepteur, 'player_id', '?')} intercepte la passe !")
        return True

    return False


def relancer_gardien(gk, teammates, passer_fn, ball):
    """
    Relance GK ➜ vers FieldPlayer allié UNIQUEMENT.
    """
    field_teammates = [
        p for p in teammates
        if not isinstance(p, GoalKeeper)
        and p.color == gk.color
        and p != gk
    ]

    if not field_teammates:
        #tqdm.write("[RELANCE GK] ⚠️ Aucun FieldPlayer allié dispo ➜ pas de relance.")
        return

    cible = np.random.choice(field_teammates)

    distance = np.hypot(cible.x - gk.x, cible.y - gk.y)
    if distance < 30:
        #tqdm.write(f"[RELANCE GK] ⚠️ Relance annulée ➜ cible trop proche (distance {distance:.2f}).")
        return

    passer_fn(gk, cible, ball)
    gk.has_ball = False
    #tqdm.write(f"[RELANCE GK] ✅ Gardien relance ➜ Player#{getattr(cible, 'player_id', '?')} | Distance={distance:.2f}")
