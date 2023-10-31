from character import Character


class Monster(Character):
    def __init__(self, name: str, health: int, attack: int, defense: int, loot: list = None, exp: int = 0):
        super().__init__(name, health, attack, defense)
        self.loot = loot if loot else []
        self.exp = exp

    def drop_all_loot(self):
        """Drops items upon defeat."""
        return self.loot

    def reward_exp(self):
        """Rewards EXP upon defeat."""
        return self.exp
