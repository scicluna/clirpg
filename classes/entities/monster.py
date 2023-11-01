from .character import Character
from .player import Player
import random


class Monster(Character):
    def __init__(self, name: str, hp: int, damage: int, defense: int, loot: list = None, exp: int = 0):
        super().__init__(name, hp, damage, defense)
        self.loot = loot if loot else []
        self.exp = exp
        self.attacks = [self.generic_attack]

    def drop_all_loot(self):
        """Drops items upon defeat."""
        return self.loot

    def reward_exp(self):
        """Rewards EXP upon defeat."""
        return self.exp

    def pick_attack(self, target: Player):
        """Picks and executes a monster attack"""
        attack = random.choice(self.attacks)
        attack(target)
