"""
Module : setup.py
Contient la fonction pour initialiser les entités du match.
"""

from tqdm import tqdm

from env_dev_dev.actors.field_player import FieldPlayer
from env_dev_dev.actors.goalkeeper import GoalKeeper
from env_dev_dev.actors.ball import Ball
from env_dev_dev.agents.rl_agent import RLAgent
from env_dev_dev.agents.random_agent import RandomAgent


def create_match_entities(opponent_mode="random", opponent_model_path=None):
    """
    Crée joueurs, gardiens, agents et ballon configurés.

    Args:
        opponent_mode (str): "random" ou "model" pour choisir le type d'agents adverses.
        opponent_model_path (str, optional): Chemin vers le modèle RL entraîné.

    Returns:
        tuple: (players, keepers, agents, ball)
    """
    same_player_stats = {
        "vitesse": 100 / 7,
        "endurance": 100 / 7,
        "précision_passe": 100 / 7,
        "précision_tir": 100 / 7,
        "dribble": 100 / 7,
        "tacle": 100 / 7,
        "interception": 100 / 7
    }

    same_keeper_stats = {
        "réflexes": 100 / 6,
        "plongeon": 100 / 3,
        "relance": 100 / 3
    }

    # === Joueurs BLEUS ===
    p1 = FieldPlayer(600, 300, same_player_stats, (0, 0, 255), 1)
    p2 = FieldPlayer(150, 300, same_player_stats, (0, 0, 255), 2)
    p3 = FieldPlayer(325, 150, same_player_stats, (0, 0, 255), 3)
    p4 = FieldPlayer(325, 450, same_player_stats, (0, 0, 255), 4)
    keeper_bleu = GoalKeeper(50, 300, same_keeper_stats, (0, 0, 255))

    # === Joueurs ROUGES ===
    p5 = FieldPlayer(800-600, 600-300, same_player_stats, (255, 0, 0), 5)
    p6 = FieldPlayer(800-150, 600-300, same_player_stats, (255, 0, 0), 6)
    p7 = FieldPlayer(800-325, 600-150, same_player_stats, (255, 0, 0), 7)
    p8 = FieldPlayer(800-325, 600-450, same_player_stats, (255, 0, 0), 8)
    keeper_rouge = GoalKeeper(750, 300, same_keeper_stats, (255, 0, 0))

    # Sauvegarde des positions de départ
    for p in [p1, p2, p3, p4, p5, p6, p7, p8, keeper_bleu, keeper_rouge]:
        p.start_x = p.x
        p.start_y = p.y

    # === Agents BLEUS ===
    agent1 = RLAgent(["passer", "tirer", "dribbler", "se_deplacer"])
    agent2 = RLAgent(["passer", "tirer", "dribbler", "se_deplacer"])
    agent3 = RLAgent(["passer", "tirer", "dribbler", "se_deplacer"])
    agent4 = RLAgent(["passer", "tirer", "dribbler", "se_deplacer"])
    agent_gk_bleu = RandomAgent()

    # === Agents ROUGES ===
    if opponent_mode == "model":
        agent5 = RLAgent(["passer", "tirer", "dribbler", "se_deplacer"])
        agent6 = RLAgent(["passer", "tirer", "dribbler", "se_deplacer"])
        agent7 = RLAgent(["passer", "tirer", "dribbler", "se_deplacer"])
        agent8 = RLAgent(["passer", "tirer", "dribbler", "se_deplacer"])

        if opponent_model_path:
            agent5.load_model(opponent_model_path)
            agent6.load_model(opponent_model_path)
            agent7.load_model(opponent_model_path)
            agent8.load_model(opponent_model_path)

    else:
        agent5 = RandomAgent()
        agent6 = RandomAgent()
        agent7 = RandomAgent()
        agent8 = RandomAgent()

    agent_gk_rouge = RandomAgent()

    # === Liaison Agents <-> Joueurs ===
    p1.agent = agent1
    p2.agent = agent2
    p3.agent = agent3
    p4.agent = agent4

    p5.agent = agent5
    p6.agent = agent6
    p7.agent = agent7
    p8.agent = agent8

    keeper_bleu.agent = agent_gk_bleu
    keeper_rouge.agent = agent_gk_rouge

    # === Groupes ===
    players = [p1, p2, p3, p4, p5, p6, p7, p8]
    keepers = [keeper_bleu, keeper_rouge]
    agents = [
        agent1, agent2, agent3, agent4,
        agent5, agent6, agent7, agent8,
        agent_gk_bleu, agent_gk_rouge
    ]

    # === Ballon ===
    ball = Ball(p1.x, p1.y)
    p1.has_ball = True
    ball.owner = p1

    return players, keepers, agents, ball
