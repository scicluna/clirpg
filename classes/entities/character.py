class Character:
    def __init__(self, name: str, hp: int, damage: int, defense: int, gold: int = 0, inventory: list = None):
        self.name = name
        self.hp = hp
        self.damage = damage
        self.defense = defense
        self.gold = gold
        self.inventory = inventory if inventory else []

    def take_damage(self, damage: int):
        """Reduces the character's hp by the given damage, after accounting for defense."""
        net_damage = max(damage - self.defense, 0)
        self.hp -= net_damage
        return net_damage  # might be useful to know how much damage was actually dealt

    def generic_attack(self, target: "Character"):
        """Performs a generic attack on a target."""
        return target.take_damage(self.damage)

    def is_alive(self) -> bool:
        """Checks if the character is still alive."""
        return self.hp > 0

    def add_items(self, items: list):
        """Adds items to the character's inventory."""
        for item in items:
            self.inventory.append(item)

    def remove_from_inventory(self, item):
        """Removes an item from the character's inventory."""
        if item in self.inventory:
            self.inventory.remove(item)
