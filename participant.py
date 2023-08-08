from deck import Card, Deck
from copy import deepcopy
import tkinter as tk


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

    def show_cards(self, game: tk.Toplevel, position) -> None:
        num_of_cards = len(self._cards)
        for i, card in enumerate(self._cards):
            img_label = tk.Label(game)  # etykieta do podpięcia referencji na obrazek
            img_label.place(anchor='center', relx=(.5 - (num_of_cards - 1) * 0.05) + i * 0.1, rely=position)  # bez niego uchwyt do obrazka zostaje utracony i wyświetla się nic
            try:
                path = 'graphics/cards/{}/{}.png'.format(card.get_suit(), card.get_name())
                img_label.image = tk.PhotoImage(file=path)
                img_label.configure(image=img_label.image)  # połączenie obrazka z uchwytem
            except FileNotFoundError:  # gdy nie ma obrazka to wyśweitla słownie
                tk.Label(game, text='{} of {}'.format(card.get_name(), card.get_suit())).place(anchor='center', relx=(.5 - (num_of_cards - 1) * 0.05) + i * 0.1, rely=position)
            except tk.TclError:
                tk.Label(game, text='{} of {}'.format(card.get_name(), card.get_suit())).place(anchor='center', relx=(.5 - (num_of_cards - 1) * 0.05) + i * 0.1, rely=position)


class Player(Participant):
    def __init__(self, starting_money: int = 5000) -> None:
        super().__init__()
        self.__money = starting_money
        self.__cards2 = []
        self.__hidden_card = Card()

    def take_money(self, money: int) -> None:
        self.__money -= money

    def show_cards(self, game: tk.Toplevel) -> None:
        tk.Label(game, text='Player\'s cards:').place(anchor='center', relx=.5, rely=.1)
        super().show_cards(game, .25)

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

    def show_cards(self, game: tk.Toplevel) -> None:
        tk.Label(game, text='Croupier\'s cards:').place(anchor='center', relx=.5, rely=.65)  # umieszcza napis o kartach krupiera
        if self.__show_second:
            super().show_cards(game, .6)
        else:
            card = self._cards[0]
            img_label = tk.Label(game)  # etykieta, aby podpiąć do niej referencję na obrazek
            img_label.place(anchor='center', relx=.45, rely=.8)  # bez niego uchwyt do obrazka zostaje utracony i wyświetla się nic
            try:
                path = 'graphics/cards/{}/{}.png'.format(card.get_suit(), card.get_name())
                img_label.image = tk.PhotoImage(file=path)  # pobranie obrazka
                img_label.configure(image=img_label.image)  # zapisanie go w etykiecie
            except FileNotFoundError:  # jak nie znajduje obrazka (bo go nie ma) to wyświetla słownie kartę
                tk.Label(game, text='{} of {}'.format(card.get_name(), card.get_suit())).place(anchor='center', relx=.4, rely=.85)
            except tk.TclError:
                tk.Label(game, text='{} of {}'.format(card.get_name(), card.get_suit())).place(anchor='center', relx=.4, rely=.85)
            finally:
                img_label = tk.Label(game)  # Wyświetlenie zakrytej karty
                img_label.place(anchor='center', relx=.55, rely=.8)
                path = 'graphics/decks/main_deck.png'  # W PRZYSZŁOŚCI WIĘCEJ OPCJI GRAFICZNYCH
                img_label.image = tk.PhotoImage(file=path)  # pobranie obrazka
                img_label.configure(image=img_label.image)  # zapisanie go w etykiecie

    def is_first_card_ace(self) -> bool:
        if self._cards[0].get_name() == 'Ace':
            return True
        return False

    def is_blackjack(self) -> bool:
        if self.is_first_card_ace():
            if self._cards[1].get_value == 10:
                return True
        return False
