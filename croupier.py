from card import Deck


class Croupier:
    def __init__(self) -> None:
        self.__cards = []
        self.__show_second = False
        # self.__cards_on_table = []

    def give_card(self, deck: Deck) -> None:
        self.__cards.append(deck.take_card())

    def show_second(self) -> None:
        self.__show_second = True

    def clean_hand(self) -> None:
        self.__cards = []
        self.__show_second = False

    def show_cards(self) -> None:
        print('Croupier\'s cards:')
        if self.__show_second:
            for card in self.__cards:
                print('{} of {}'.format(card.get_name(), card.get_suit()))
        else:
            card = self.__cards[0]
            print('{} of {}'.format(card.get_name(), card.get_suit()))
            print('Hidden card')

    def is_first_card_ace(self) -> bool:
        if self.__cards[0].get_name() == 'Ace':
            return True
        return False

    def is_blackjack(self) -> bool:
        if self.is_first_card_ace():
            if self.__cards[1].get_value == 10:
                return True
        return False

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
