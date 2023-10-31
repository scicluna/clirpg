class GameElement:
    def trigger(self):
        raise NotImplementedError

    def resolve(self):
        raise NotImplementedError
