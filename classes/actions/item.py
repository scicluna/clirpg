from enum import Enum, auto


class ItemType(Enum):
    WEAPON = auto()
    ARMOR = auto()
    CONSUMABLE = auto()
    SPECIAL = auto()
    # Add other types as needed


class Item:
    def __init__(self, name: str, description: str, quantity: int, item_type: ItemType,
                 dmg: int = 0, defense: int = 0, healing: int = 0, special=None):
        self.name = name
        self.description = description
        self.quantity = quantity
        self.type = item_type
        self.dmg = dmg
        self.defense = defense
        self.healing = healing
        self.special = special  # This can be more complex depending on your needs

    def use_item(self, player):
        """Use the item and apply its effects to the player."""
        if self.type == ItemType.WEAPON:
            # Equip or use weapon; increase player's dmg by self.dmg
            print(f"Equipped {self.name}!")
            player.equip_weapon(self)
            pass
        elif self.type == ItemType.ARMOR:
            # Equip or use armor; increase player's defense by self.defense
            print(f"Equipped {self.name}!")
            player.equip_armor(self)
            pass
        elif self.type == ItemType.CONSUMABLE:
            # Use consumable item; increase player's health by self.healing
            print(f"Used {self.name}!")
            self.quantity -= 1
            if self.quantity <= 0:
                player.inventory.remove(self)
            pass
        elif self.type == ItemType.SPECIAL:
            # Handle special items; maybe they have unique effects or trigger events
            pass

    def __str__(self):
        return f"{self.name} (x{self.quantity}): {self.description}"
