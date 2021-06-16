from random import choice


class Game:
    def __init__(self, client_1_sock, client_2_sock, format, buff_size):
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
        self.word_client_1_answer = None
        self.word_client_2 = None
        self.word_client_2_answer = None
        self.lives_client_1 = 1
        self.lives_client_2 = 1
        self.category = self._rand_category()
        self.format = format
        self.buff_size = buff_size
        self.send_result = 0

    @staticmethod
    def _rand_category() -> str:
        """
        :return category -> str:
        """

        categories = [
            'Amphibians',
            'Arctic Animals',
            'Cars',
            'Birds',
            'Dangerous Animals',
            'Farm Animals',
            'Fast Animals',
            'Fish',
            'Slow Animals',
            'Colors',
            'Famous Artists',
            'Photography',
            'Medical Terms',
            'Office Items',
            'Areas of Study',
            'Men’s Clothing',
            'Women’s Clothing',
            'Music',
            'Cartoon Characters',
            'Actors',
            'Actresses',
            'Classic Movies',
            'Comedies',
            'Fantasy',
            'Science Fiction',
            'Sports Played Outside',
            'Sports Played Inside',
            'Water Sports',
            'Breakfast Foods',
            'Candy',
            'Dairy Products',
            'Cakes',
            'Fast Food',
            'Ice Cream Flavors',
            'Meats',
            'Sandwiches',
            'Gardening Tasks',
            'Growing Vegetables',
            'Trees',
            'African Countries',
            'Asian Capital Cities',
            'Canadian Provinces',
            'Cold Places',
            'Countries',
            'European Capital Cities',
            'Lakes',
            'South American Countries',
            'Politics',
            'Wars',
            'Holidays',
            'Bathroom Accessories',
            'Mythology',
            'Math Terms',
            'Theme Songs',
            'Chemicals',
            'Constellations',
            'Metals',
            'Minerals',
            'Weather',
            'Internet',
            'Hobbies'
        ]
        return choice(categories)



    def set_words(self, client_number: int, msg: str):
        if client_number == 0:
            self.word_client_1 = msg
            self.word_client_1_answer = '_' * len(self.word_client_1)
        else:
            self.word_client_2 = msg
            self.word_client_2_answer = '_' * len(self.word_client_2)


    def set_lives(self, lives: int):
            self.lives_client_1 = lives
            self.lives_client_2 = lives

    def playing_hangman(self, client_number: int, msg: str):
        try:
            msg = msg[0]
        except IndexError:
            # TODO Save information about system to logs
            err_msg = "You haven't put any letter"
            if client_number == 0:
                self.client_2_sock.send(err_msg.encode(self.format))
            else:
                self.client_1_sock.send(err_msg.encode(self.format))

        if client_number == 0:
            guess = msg
            index = 0
            damage = True
            for character in self.word_client_2:
                if character == guess:
                    self.word_client_2_answer = self.word_client_2_answer[
                                                :index] + character + self.word_client_2_answer[index + 1:]
                    damage = False

                index = index + 1
            if damage:
                self.lives_client_1 = self.lives_client_1 - 1
                self.client_1_sock.send(('Miss! ' + str(self.lives_client_1)
                                         + ' lives remaining.').encode(self.format))
            else:
                self.client_1_sock.send(('Got it!').encode(self.format))
                self.client_1_sock.send((self.word_client_2_answer).encode(self.format))
        else:
            guess = msg
            index = 0
            damage = True
            for character in self.word_client_1:
                if (character == guess):
                    self.word_client_1_answer = self.word_client_1_answer[
                                                :index] + character + self.word_client_1_answer[index + 1:]
                    damage = False

                index = index + 1
            if damage:
                self.lives_client_2 = self.lives_client_2 - 1
                self.client_2_sock.send(('Miss! ' + str(self.lives_client_2)
                                         + ' lives remaining.').encode(self.format))
            else:
                self.client_2_sock.send(('Got it!').encode(self.format))
                self.client_2_sock.send((self.word_client_1_answer).encode(self.format))

    """If missed, player loses 1 life
        If gussed, player receives progress of an answer"""


    def score(self) -> bool:
        msgWin = "You won the game!"
        msgLose = "You lost the game!"
        if self.lives_client_1 <= 0:
            self.client_1_sock.send((msgLose).encode(self.format))
            self.client_2_sock.send((msgWin).encode(self.format))
            return True

        if self.lives_client_2 <= 0:
            self.client_1_sock.send((msgWin).encode(self.format))
            self.client_2_sock.send((msgLose).encode(self.format))
            return True

        if self.word_client_1_answer == self.word_client_1:
            self.client_1_sock.send((msgLose).encode(self.format))
            self.client_2_sock.send((msgWin).encode(self.format))
            return True

        if self.word_client_2_answer == self.word_client_2:
            self.client_1_sock.send((msgWin).encode(self.format))
            self.client_2_sock.send((msgLose).encode(self.format))
            return True

        return False

    """If guessed whole word, wins. If lost all lives, loses"""

