"""
Module : random_agent.py
Agent totalement aléatoire avec logs DEBUG.
"""

import random
from tqdm import tqdm
from env_dev_dev.agents.base_agent import BaseAgent
from env_dev_dev.actors.goalkeeper import GoalKeeper


class RandomAgent(BaseAgent):
    """
    Agent Random :
    - FieldPlayer ➜ actions variées (passe, tir, dribble, déplacement)
    - GoalKeeper ➜ relance seulement
    """

    def decide_action(self, entity, context):
        """
        Décide une action aléatoire et trace tout.
        """
        if isinstance(entity, GoalKeeper):
            if entity.has_ball:
                ##tqdm.write(f"[RANDOM AGENT] GoalKeeper#{entity.player_id} ➜ Action : relancer")
                return {"type": "relancer"}
            else:
                ##tqdm.write(f"[RANDOM AGENT] GoalKeeper#{entity.player_id} ➜ Action : none (pas de ballon)")
                return {"type": "none"}

        # === FieldPlayer ===
        # Détermine actions possibles
        actions = ["passer", "dribbler", "se_deplacer"]

        half_field = context["field_width"] / 2
        # Autorise "tirer" seulement si le joueur est DANS LA MOITIÉ ADVERSE
        if (entity.color == (0, 0, 255) and entity.x >= half_field) or \
           (entity.color == (255, 0, 0) and entity.x <= half_field):
            actions.append("tirer")

        action_type = random.choice(actions)
        ##tqdm.write(f"[RANDOM AGENT] Player#{entity.player_id} ➜ Action choisie : {action_type}")

        if not entity.has_ball:
            dx, dy = random.uniform(-1, 1), random.uniform(-1, 1)
            ##tqdm.write(f"[RANDOM AGENT] Player#{entity.player_id} ➜ Pas de balle ➜ se_deplacer (dx={dx:.2f}, dy={dy:.2f})")
            return {"type": "se_deplacer", "dir_x": dx, "dir_y": dy}

        if action_type == "passer":
            teammates = [
                p for p in context["players"]
                if p != entity and p.color == entity.color and not isinstance(p, GoalKeeper)
            ]
            if teammates:
                cible = random.choice(teammates)
                ##tqdm.write(f"[RANDOM AGENT] Player#{entity.player_id} ➜ Passe vers Player#{cible.player_id}")
                return {"type": "passer", "cible": cible}
            else:
                ##tqdm.write(f"[RANDOM AGENT] Player#{entity.player_id} ➜ Pas de coéquipier ➜ Dribbler forcé")
                dx, dy = random.uniform(-1, 1), random.uniform(-1, 1)
                return {"type": "dribbler", "dir_x": dx, "dir_y": dy}

        elif action_type == "tirer":
            but_x, but_y = context["but_adverse"]
            ##tqdm.write(f"[RANDOM AGENT] Player#{entity.player_id} ➜ Tir vers but ({but_x},{but_y})")
            return {"type": "tirer", "but_x": but_x, "but_y": but_y}

        elif action_type == "dribbler":
            dx, dy = random.uniform(-1, 1), random.uniform(-1, 1)
            ##tqdm.write(f"[RANDOM AGENT] Player#{entity.player_id} ➜ Dribble (dx={dx:.2f}, dy={dy:.2f})")
            return {"type": "dribbler", "dir_x": dx, "dir_y": dy}

        else:
            dx, dy = random.uniform(-1, 1), random.uniform(-1, 1)
            ##tqdm.write(f"[RANDOM AGENT] Player#{entity.player_id} ➜ Se déplacer (dx={dx:.2f}, dy={dy:.2f})")
            return {"type": "se_deplacer", "dir_x": dx, "dir_y": dy}
