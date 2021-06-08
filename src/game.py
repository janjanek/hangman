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
