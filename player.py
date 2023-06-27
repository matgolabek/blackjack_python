from card import Card, Deck
from copy import deepcopy


class Player:
    def __init__(self, starting_money: int = 5000):
        self.__money = starting_money
        self.__cards = []
        self.__cards2 = []
        self.__hidden_card = Card()
        # self.__cards_on_table = []

    def give_card(self, deck: Deck) -> None:
        self.__cards.append(deck.take_card())

    def take_money(self, money: int) -> None:
        self.__money -= money

    def show_cards(self) -> None:
        print('Player\'s cards:')
        for card in self.__cards:
            print('{} of {}'.format(card.get_name(), card.get_suit()))

    def get_cards_sum(self) -> int:
        has_ace = False
        cards_sum = 0
        for card in self.__cards:
            if card.get_name() == 'Ace':
                has_ace = True
                cards_sum += 1
            else:
                cards_sum += card.get_value()
        if has_ace:
            if cards_sum < 12:
                cards_sum += 10
        return cards_sum

    def is_blackjack(self) -> bool:
        if self.__cards[0].get_name() == 'Ace':
            if self.__cards[1].get_value() == 10:
                return True
        elif self.__cards[0].get_value() == 10:
            if self.__cards[1].get_name() == 'Ace':
                return True
        return False

    def clean_hand(self) -> None:
        self.__cards = []

    def can_split(self) -> bool:
        if self.__cards[0].get_name() == self.__cards[1].get_name():
            return True
        return False

    def hide_second(self) -> None:
        self.__hidden_card = self.__cards.pop()

    def show_second(self) -> None:
        self.__cards.append(self.__hidden_card)
        # self.__hidden_card = Card()

    def money_won(self, money: int):
        self.__money += money

    def get_money(self) -> int:
        return self.__money

    def move_cards(self) -> None:
        self.__cards2 = deepcopy(self.__cards)
        self.__cards = []

    def move_cards_back(self) -> None:
        self.__cards = deepcopy(self.__cards2)
        self.__cards2 = []
