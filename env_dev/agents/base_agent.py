"""
Module : base_agent.py
Définit l'interface de base pour tout agent Red Lock.
"""

from abc import ABC, abstractmethod


class BaseAgent(ABC):
    """
    Interface de base pour les agents.
    Chaque agent doit implémenter `decide_action`.
    """

    @abstractmethod
    def decide_action(self, player, game_state):
        """
        Décide quoi faire.

        Args:
            player: FieldPlayer contrôlé.
            game_state: Infos globales (balle, autres joueurs, etc.)

        Returns:
            dict: Action à exécuter.
        """
        pass
