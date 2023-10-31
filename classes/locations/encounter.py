from gameelement import GameElement
from ..entities.player import Player
from ..entities.monster import Monster


class Encounter(GameElement):
    def __init__(self, monsters: list[Monster], player: Player):
        self.monsters = monsters
        self.player = player

    def trigger(self):
        # Engage the player in combat

        pass

    def resolve(self):
        # Determine the outcome of the encounter
        for monster in self.monsters:
            self.player.add_items(monster.drop_all_loot())
            self.player.gain_experience(monster.reward_exp())
        pass
