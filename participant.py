from deck import Card, Deck
from copy import deepcopy


class Participant:
    def __init__(self) -> None:
        self._cards = []

    def give_card(self, deck: Deck) -> None:
        self._cards.append(deck.take_card())

    def clean_hand(self) -> None:
        self._cards = []

    def get_cards_sum(self) -> int:
        has_ace = False
        cards_sum = 0
        for card in self._cards:
            if card.get_name() == 'Ace':
                has_ace = True
                cards_sum += 1
            else:
                cards_sum += card.get_value()
        if has_ace:
            if cards_sum < 12:
                cards_sum += 10
        return cards_sum

    def show_cards_(self) -> None:
        for card in self._cards:
            print('{} of {}'.format(card.get_name(), card.get_suit()))


class Player(Participant):
    def __init__(self, starting_money: int = 5000) -> None:
        super().__init__()
        self.__money = starting_money
        self.__cards2 = []
        self.__hidden_card = Card()

    def take_money(self, money: int) -> None:
        self.__money -= money

    def show_cards(self) -> None:
        print('Player\'s cards:')
        self.show_cards_()

    def is_blackjack(self) -> bool:
        if self._cards[0].get_name() == 'Ace':
            if self._cards[1].get_value() == 10:
                return True
        elif self._cards[0].get_value() == 10:
            if self._cards[1].get_name() == 'Ace':
                return True
        return False

    def can_split(self) -> bool:
        if self._cards[0].get_name() == self._cards[1].get_name():
            return True
        return False

    def hide_second(self) -> None:
        self.__hidden_card = self._cards.pop()

    def show_second(self) -> None:
        self._cards.append(self.__hidden_card)

    def money_won(self, money: int):
        self.__money += money

    def get_money(self) -> int:
        return self.__money

    def move_cards(self) -> None:
        self.__cards2 = deepcopy(self._cards)
        self._cards = []

    def move_cards_back(self) -> None:
        self._cards = deepcopy(self.__cards2)
        self.__cards2 = []


class Croupier(Participant):
    def __init__(self) -> None:
        super().__init__()
        self.__show_second = False

    def show_second(self) -> None:
        self.__show_second = True

    def clean_hand(self) -> None:
        self._cards = []
        self.__show_second = False

    def show_cards(self) -> None:
        print('Croupier\'s cards:')
        if self.__show_second:
            self.show_cards_()
        else:
            card = self._cards[0]
            print('{} of {}'.format(card.get_name(), card.get_suit()))
            print('Hidden card')

    def is_first_card_ace(self) -> bool:
        if self._cards[0].get_name() == 'Ace':
            return True
        return False

    def is_blackjack(self) -> bool:
        if self.is_first_card_ace():
            if self._cards[1].get_value == 10:
                return True
        return False
