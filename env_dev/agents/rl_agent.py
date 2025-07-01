"""
Module : rl_agent.py
Agent RL PyTorch pour Red Lock — version REINFORCE avec tir simplifié.
"""

import random
import torch
import torch.nn as nn
import torch.optim as optim
from tqdm import tqdm

from env_dev_dev.agents.base_agent import BaseAgent
from env_dev_dev.actors.goalkeeper import GoalKeeper


class PolicyNetwork(nn.Module):
    """
    Réseau de policy simple.
    """
    def __init__(self, state_dim, action_dim):
        super().__init__()
        self.fc = nn.Sequential(
            nn.Linear(state_dim, 64),
            nn.ReLU(),
            nn.Linear(64, action_dim)
        )

    def forward(self, x):
        return self.fc(x)


class RLAgent(BaseAgent):
    """
    Agent RL Red Lock — version REINFORCE, tir dirigé auto.
    """
    def __init__(self, action_space, state_dim=13):
        self.action_space = action_space
        self.state_dim = state_dim
        self.action_dim = len(action_space)

        self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

        self.policy = PolicyNetwork(state_dim, self.action_dim)
        self.policy.to(self.device)

        self.optimizer = optim.Adam(self.policy.parameters(), lr=1e-3)

        self.saved_log_probs = []
        self.local_rewards = []

        #tqdm.write(f"[RLAgent] ✅ Policy initialisée sur {self.device}")

    def decide_action(self, player, game_state):
        """
        Décide une action valide :
        - Passe à un coéquipier.
        - Tir seulement si joueur dans la moitié adverse.
        - Se déplacer ou dribbler sinon.
        """
        state = self._extract_state(player, game_state)
        state_tensor = torch.tensor(state, dtype=torch.float32).to(self.device)

        logits = self.policy(state_tensor)
        if torch.isnan(logits).any():
            logits = torch.zeros_like(logits)
        else:
            logits = torch.clamp(logits, -50, 50)

        probs = torch.softmax(logits, dim=0)

        # === Masque dynamique des actions valides ===
        valid_actions = ["passer", "dribbler", "se_deplacer"]
        half_field = game_state["field_width"] / 2

        if (player.color == (0, 0, 255) and player.x > half_field) or \
           (player.color == (255, 0, 0) and player.x < half_field):
            valid_actions.append("tirer")

        mask_values = [
            1 if self.action_space[i] in valid_actions else 0
            for i in range(self.action_dim)
        ]

        mask = torch.tensor(mask_values, dtype=torch.float32).to(self.device)

        masked_probs = probs * mask

        if masked_probs.sum() == 0:
            return {
                "type": "se_deplacer",
                "dir_x": random.uniform(-1, 1),
                "dir_y": random.uniform(-1, 1),
                "intensity": random.choice([1, 2, 3])
            }

        masked_probs /= masked_probs.sum()

        m = torch.distributions.Categorical(masked_probs)
        action_index = m.sample()
        log_prob = m.log_prob(action_index)

        self.saved_log_probs.append(log_prob)

        action_type = self.action_space[action_index.item()]
        teammates = [
            p for p in game_state["players"]
            if p != player and p.color == player.color and not isinstance(p, GoalKeeper)
        ]

        if isinstance(player, GoalKeeper):
            if player.has_ball:
                if teammates:
                    cible = random.choice(teammates)
                    return {"type": "passer", "cible": cible}
                return {"type": "none"}
            return {"type": "none"}

        if not player.has_ball:
            return {
                "type": "se_deplacer",
                "dir_x": random.uniform(-1, 1),
                "dir_y": random.uniform(-1, 1),
                "intensity": random.choice([1, 2, 3])
            }

        if action_type == "passer":
            if teammates:
                cible = random.choice(teammates)
                return {"type": "passer", "cible": cible}
            return {
                "type": "dribbler",
                "dir_x": random.uniform(-1, 1),
                "dir_y": random.uniform(-1, 1),
                "intensity": random.choice([1, 2, 3])
            }

        if action_type == "tirer":
            return {"type": "tirer"}

        if action_type == "dribbler":
            return {
                "type": "dribbler",
                "dir_x": random.uniform(-1, 1),
                "dir_y": random.uniform(-1, 1),
                "intensity": random.choice([1, 2, 3])
            }

        return {
            "type": "se_deplacer",
            "dir_x": random.uniform(-1, 1),
            "dir_y": random.uniform(-1, 1),
            "intensity": random.choice([1, 2, 3])
        }

    def _extract_state(self, player, game_state):
        """
        Extrait un vecteur d'état normalisé.
        """
        state = [
            player.x / 800,
            player.y / 600,
            int(player.has_ball),
            game_state["ball"].x / 800,
            game_state["ball"].y / 600
        ]

        teammates = [p for p in game_state["players"] if p != player and p.color == player.color]
        opponents = [p for p in game_state["players"] if p.color != player.color]

        teammates.sort(key=lambda p: (p.x - player.x) ** 2 + (p.y - player.y) ** 2)
        opponents.sort(key=lambda p: (p.x - player.x) ** 2 + (p.y - player.y) ** 2)

        for mate in teammates[:2]:
            state.append(mate.x / 800)
            state.append(mate.y / 600)
        while len(teammates) < 2:
            state.extend([0.0, 0.0])
            teammates.append(None)

        for opp in opponents[:2]:
            state.append(opp.x / 800)
            state.append(opp.y / 600)
        while len(opponents) < 2:
            state.extend([0.0, 0.0])
            opponents.append(None)

        return state

    def learn(self, log_probs, rewards, gamma=0.99):
        """
        REINFORCE final avec micro-rewards inclus.
        """
        if len(log_probs) == 0 or len(rewards) == 0:
            return

        discounted_rewards = []
        R = 0
        for r in reversed(rewards):
            R = r + gamma * R
            discounted_rewards.insert(0, R)

        discounted_rewards = torch.tensor(discounted_rewards, dtype=torch.float32).to(self.device)

        if discounted_rewards.std() > 0:
            discounted_rewards = (discounted_rewards - discounted_rewards.mean()) / (discounted_rewards.std() + 1e-9)
        else:
            discounted_rewards *= 0

        loss = 0
        for log_prob, R in zip(log_probs, discounted_rewards):
            loss -= log_prob * R

        self.optimizer.zero_grad()
        loss.backward()
        self.optimizer.step()
        tqdm.write(f"[RLAgent] 🔍 Learn sur device = {self.device} | Loss: {loss.item():.4f}")

    def save_model(self, path):
        checkpoint = {
            "state_dim": self.state_dim,
            "action_dim": self.action_dim,
            "model_state": self.policy.state_dict()
        }
        torch.save(checkpoint, path)

    def load_model(self, path):
        checkpoint = torch.load(path)
        self.state_dim = checkpoint["state_dim"]
        self.action_dim = checkpoint["action_dim"]
        self.policy = PolicyNetwork(self.state_dim, self.action_dim)
        self.policy.load_state_dict(checkpoint["model_state"])
        self.policy.to(self.device)
