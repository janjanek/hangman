from random import choice


class Game:
    def __init__(self, client_1_sock, client_2_sock, format):
        """
        :param client_1_sock:
        :param client_2_sock:
        :param format:
        """
        self.client_1_sock = client_1_sock
        self.client_2_sock = client_2_sock
        self.format = format
        self.active = False
        self.win = None
        self.word_client_1 = None
        self.word_client_2 = None
        self.category = self._rand_category()
        self.format = format

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

    def logic(self, client_number: int, msg: str) -> None:
        if client_number == 0:
            self.client_2_sock.send(msg.encode(self.format))
        else:
            self.client_1_sock.send(msg.encode(self.format))
