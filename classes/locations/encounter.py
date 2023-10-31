from gameelement import GameElement


class Encounter(GameElement):
    def __init__(self, monsters):
        self.monsters = monsters

    def trigger(self):
        # Engage the player in combat
        pass

    def resolve(self):
        # Determine the outcome of the encounter
        pass
