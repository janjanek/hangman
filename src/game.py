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

    def startGame(self, client_number: int, msg: str):
        if client_number == 0:
            # if self.client_2_sock.recv(msg.decode(self.format)) == 'start':
            if msg == 'start':
                self.client_2_sock.send('Opponent wants to start! Game is starting'.encode(self.format))

        if client_number == 1:
            # if self.client_1_sock.recv(msg.decode(self.format)) == 'start':
            if msg == 'start':
                self.client_1_sock.send('Opponent wants to start. Game is starting'.encode(self.format))



    def logic(self, client_number: int, msg: str) -> None:
        if client_number == 0:
            self.client_2_sock.send(msg.encode(self.format))
        else:
            self.client_1_sock.send(msg.encode(self.format))

    def setWords(self, client_number: int):
        msg = 'Set the word from category: ' + self._rand_category()
        if client_number == 0:
            self.client_1_sock.send(msg.encode(self.format))
            self.word_client_1 = self.client_1_sock.recv(1024).decode(self.format)
            self.word_client_1_answer = '_' * len(self.word_client_1)
        else:
            self.client_2_sock.send(msg.encode(self.format))
            self.word_client_2 = self.client_2_sock.recv(1024).decode(self.format)
            self.word_client_2_answer = '_' * len(self.word_client_2)

    def setLives(self, client_number: int):
        msg = 'Set number of lives. Must be a number!'
        lives = 1
        if client_number == 0:
            self.client_1_sock.send(msg.encode(self.format))
            strLives = self.client_1_sock.recv(1024).decode(self.format)
            lives = int(strLives)
            self.lives_client_1 = int(lives)
            self.lives_client_2 = int(lives)
            self.client_2_sock.send(('Your number of lives is: ' + str(lives)).encode(self.format))


    def playing(self, client_number: int):
        while True:
                if(client_number == 0):
                    self.client_1_sock.send(self.word_client_1_answer.encode(self.format))
                    if(self.word_client_1_answer == self.word_client_2):
                        self.client_1_sock.send(('You won the game!').encode(self.format))
                        self.client_2_sock.send(('You lost the game!').encode(self.format))
                        break
                    if(self.lives_client_1 <= 0):
                        self.client_1_sock.send(('You lost the game!').encode(self.format))
                        self.client_2_sock.send(('You won the game!').encode(self.format))
                        break

                    msg = self.client_1_sock.recv(1024).decode(self.format)
                    guess = msg
                    # msg must be equal to 1 letter!!! Check for it
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
                    self.client_1_sock.send(self.word_client_2_answer.encode(self.format))
                    if(self.word_client_2_answer == self.word_client_1 or self.lives_client_2 <= 0):
                        self.client_2_sock.send(('You won the game!').encode(self.format))
                        self.client_1_sock.send(('You lost the game!').encode(self.format))
                        break
                    if(self.lives_client_1 <= 0):
                        self.client_2_sock.send(('You lost the game!').encode(self.format))
                        self.client_1_sock.send(('You won the game!').encode(self.format))
                        break

                    msg = self.client_2_sock.recv(1024).decode(self.format)
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

    def score(self) -> bool:
        msg = "You won the game!"
        if self.lives_client_1 <= 0:
            self.client_2_sock.send(msg.encode(self.format))
            return True

        if self.lives_client_2 <= 0:
            self.client_1_sock.send(msg.encode(self.format))
            return True

        return False
