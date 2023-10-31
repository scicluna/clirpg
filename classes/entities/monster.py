from character import Character


class Monster(Character):
    def __init__(self, name: str, health: int, attack: int, defense: int, loot: list = None):
        super().__init__(name, health, attack, defense)
        self.loot = loot if loot else []

    def drop_loot(self):
        """Drops items upon defeat."""
