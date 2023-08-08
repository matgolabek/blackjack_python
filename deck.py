import random


class Card:
    def __init__(self, name: str = '', suit: str = '', value: int = -1, index: int = -1) -> None:
        self.__name = name
        self.__suit = suit
        self.__value = value
        self.__index = index

    def get_name(self) -> str:
        return self.__name

    def get_suit(self) -> str:
        return self.__suit

    def get_value(self) -> int:
        return self.__value

    def get_index(self) -> int:
        return self.__index

    def __repr__(self) -> str:
        return f'{self.__name} of {self.__suit}'


class Deck:
    def __init__(self) -> None:
        self.__default_deck = [
            Card("Ace", "Hearts", 11, 0),
            Card("Ace", "Diamonds", 11, 1),
            Card("Ace", "Spades", 11, 2),
            Card("Ace", "Clubs", 11, 3),

            Card("King", "Hearts", 10, 4),
            Card("King", "Diamonds", 10, 5),
            Card("King", "Spades", 10, 6),
            Card("King", "Clubs", 10, 7),

            Card("Queen", "Hearts", 10, 8),
            Card("Queen", "Diamonds", 10, 9),
            Card("Queen", "Spades", 10, 10),
            Card("Queen", "Clubs", 10, 11),

            Card("Jack", "Hearts", 10, 12),
            Card("Jack", "Diamonds", 10, 13),
            Card("Jack", "Spades", 10, 14),
            Card("Jack", "Clubs", 10, 15),

            Card("10", "Hearts", 10, 16),
            Card("10", "Diamonds", 10, 17),
            Card("10", "Spades", 10, 18),
            Card("10", "Clubs", 10, 19),

            Card("9", "Hearts", 9, 20),
            Card("9", "Diamonds", 9, 21),
            Card("9", "Spades", 9, 22),
            Card("9", "Clubs", 9, 23),

            Card("8", "Hearts", 8, 24),
            Card("8", "Diamonds", 8, 25),
            Card("8", "Spades", 8, 26),
            Card("8", "Clubs", 8, 27),

            Card("7", "Hearts", 7, 28),
            Card("7", "Diamonds", 7, 29),
            Card("7", "Spades", 7, 30),
            Card("7", "Clubs", 7, 31),

            Card("6", "Hearts", 6, 32),
            Card("6", "Diamonds", 6, 33),
            Card("6", "Spades", 6, 34),
            Card("6", "Clubs", 6, 35),

            Card("5", "Hearts", 5, 36),
            Card("5", "Diamonds", 5, 37),
            Card("5", "Spades", 5, 38),
            Card("5", "Clubs", 5, 39),

            Card("4", "Hearts", 4, 40),
            Card("4", "Diamonds", 4, 41),
            Card("4", "Spades", 4, 42),
            Card("4", "Clubs", 4, 43),

            Card("3", "Hearts", 3, 44),
            Card("3", "Diamonds", 3, 45),
            Card("3", "Spades", 3, 46),
            Card("3", "Clubs", 3, 47),

            Card("2", "Hearts", 2, 48),
            Card("2", "Diamonds", 2, 49),
            Card("2", "Spades", 2, 50),
            Card("2", "Clubs", 2, 51)
        ]

        random_indexes = [i // 2 for i in range(104)]
        random.shuffle(random_indexes)
        self.__shuffled_deck = [Card() for _ in range(104)]
        for i in range(104):
            self.__shuffled_deck[i] = self.__default_deck[random_indexes[i]]

    def shuffle_if_needed(self) -> None:
        if len(self.__shuffled_deck) < 52:
            random_indexes = [i // 2 for i in range(104)]
            random.shuffle(random_indexes)
            self.__shuffled_deck = [Card() for _ in range(104)]
            for i in range(104):
                self.__shuffled_deck[i] = self.__default_deck[random_indexes[i]]

    def take_card(self) -> Card:
        try:
            return self.__shuffled_deck.pop()
        except IndexError:
            return Card()
