from random import choice


class Game:
    def __init__(self, client_1_sock, client_2_sock):
        """
        :param client_1_sock:
        :param client_2_sock:
        """
        self.client_1_sock = client_1_sock
        self.client_2_sock = client_2_sock
        self.win = None
        self.word = None
        self.category = self._rand_category()

    @staticmethod
    def _rand_category() -> str:
        """
        :return category -> str:
        """
        # TODO write more categories
        categories = [
            'things',
            'animals',
            'cars'
        ]
        return choice(categories)

    def set_word(self):
        raise NotImplementedError

    def game_logic(self):
        # TODO implement game logic
        raise NotImplementedError
