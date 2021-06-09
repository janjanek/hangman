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
        self.word_client_1_answer = None
        self.word_client_2 = None
        self.word_client_2_answer = None
        self.lives_client_1 = None
        self.lives_client_2 = None
        self.category = self._rand_category()
        self.format = format

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

    def logic(self, client_number: int, msg: str) -> None:
        if client_number == 0:
            self.client_2_sock.send(msg.encode(self.format))
        else:
            self.client_1_sock.send(msg.encode(self.format))

    def setWords(self, client_number: int):
        if client_number == 0:
            self.word_client_1 = self.client_1_sock.recv(1024).decode(self.format)
            self.word_client_1_answer = '_' * len(self.word_client_1)
        else:
            self.word_client_2 = self.client_2_sock.recv(1024).decode(self.format)
            self.word_client_2_answer = '_' * len(self.word_client_2)

    def setLives(self, client_number: int, lives: int):
        if client_number == 0:
            self.lives_client_1 = lives
        else:
            self.lives_client_2 = lives

    def playing(self, client_number: int, msg: str):
        if(client_number == 0):
            guess = msg
            # msg must be equal to 1 letter!!!
            index = 0
            damage = True
            for character in self.word_client_2:
                if (character == guess):
                    self.word_client_1_answer = self.word_client_1_answer[:index] + character + self.word_client_1_answer[index + 1:]
                    damage = False
                index = index + 1
            if (damage):
                self.lives_client_1 = self.lives_client_1 - 1
        else:
            guess = msg
            # msg must be equal to 1 letter!!!
            index = 0
            damage = True
            for character in self.word_client_1:
                if (character == guess):
                    self.word_client_2_answer = self.word_client_2_answer[:index] + character + self.word_client_2_answer[index + 1:]
                    damage = False
                index = index + 1
            if (damage):
                self.lives_client_2 = self.lives_client_2 - 1

    def score(self):
        msg = "You won the game!"
        if self.lives_client_1 <= 0:
            self.client_2_sock.send(msg.encode(self.format))

        if self.lives_client_2 <= 0:
            self.client_1_sock.send(msg.encode(self.format))

