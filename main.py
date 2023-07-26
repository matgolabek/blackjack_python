import tkinter as tk
from participant import Player, Croupier
from deck import Deck


def clean(croupier: Croupier, player: Player, deck: Deck) -> None:
    croupier.clean_hand()
    player.clean_hand()
    deck.shuffle_if_needed()


def show_current_status(game: tk.Toplevel, croupier: Croupier, player: Player) -> None:
    croupier.show_cards(game)
    print()
    player.show_cards(game)
    print()


def croupier_move(croupier: Croupier, player: Player, deck: Deck, difficulty: str) -> None:
    keep_playing = 15
    if difficulty == 'hard':
        player_cards_sum = player.get_cards_sum()
        if player_cards_sum > keep_playing:
            keep_playing = player_cards_sum
    while croupier.get_cards_sum() < keep_playing:
        croupier.give_card(deck)


def stand(game: tk.Toplevel, croupier: Croupier, player: Player, deck: Deck, difficulty: str, bid: int) -> None:
    croupier.show_second()
    show_current_status(game, croupier, player)
    croupier_move(croupier, player, deck, difficulty)
    show_current_status(game, croupier, player)
    if player.get_cards_sum() > croupier.get_cards_sum():
        player.money_won(bid * 2)
        print('You have won! Account status:', player.get_money())
        clean(croupier, player, deck)
        return
    elif player.get_cards_sum() > croupier.get_cards_sum():
        player.money_won(bid)
        print('Draw, account status:', player.get_money())
        clean(croupier, player, deck)
        return
    else:
        print('You have lost, account status:', player.get_money())
        clean(croupier, player, deck)
        return


def play_again_split(game: tk.Toplevel, croupier: Croupier, player: Player, deck: Deck, bid: int, difficulty: str) -> None:
    if player.get_cards_sum() > 21:
        show_current_status(game, croupier, player)
        print('Your hand has lost')
        return
    print('Do you want to hit or stand?')
    choice = str(input())
    if choice == 'hit':
        player.give_card(deck)
        show_current_status(game, croupier, player)
        play_again_split(game, croupier, player, deck, bid, difficulty)
        return
    if choice == 'stand':
        player.move_cards()
        return
    else:
        print('Wrong input, stand is chosen')
        player.move_cards()
        return


def play_again(game: tk.Toplevel, croupier: Croupier, player: Player, deck: Deck, bid: int, difficulty: str) -> None:
    if player.get_cards_sum() > 21:
        croupier.show_second()
        show_current_status(game, croupier, player)
        print('You have lost, account status: ', player.get_money())
        return
    print('Do you want to hit or stand?')
    choice = str(input())
    if choice == 'hit':
        player.give_card(deck)
        show_current_status(game, croupier, player)
        play_again_split(game, croupier, player, deck, bid, difficulty)
        return
    if choice == 'stand':
        stand(game, croupier, player, deck, difficulty, bid)
    else:
        print('Wrong input, stand is chosen')
        player.move_cards()
        return


def set_bid(game: tk.Toplevel, croupier: Croupier, player: Player, deck: Deck, difficulty: str = 'medium'):
    if player.get_money() <= 0:
        tk.Label(game, text='No money, no honey :(').pack()  # umieszcza wiadomość i kończy
        return
    tk.Label(game, text='How much money do you bid?').pack()

    bid = tk.IntVar()  # wartość stawki (str)
    bid.set(100)
    bid_entry = tk.Entry(game, textvariable=bid)
    bid_entry.pack()  # umieszcza ramkę, do której można wpisać wartość stawki
    submit_bid = tk.Button(game, text='Submit the bid', width=20,
                           command=lambda: play(game, croupier, player, deck, bid, difficulty))
    submit_bid.pack()  # przycisk zatwierdzający stawkę

    game.mainloop()


def play(game: tk.Toplevel, croupier: Croupier, player: Player, deck: Deck, bid: tk.IntVar, difficulty: str) -> None:
    try:
        bid = bid.get()  # bezpieczne ustawienie wartości stawki
    except ValueError:
        bid = 100
    if bid <= 0:  # sprawdzenie ujemnych stawek
        tk.Label(game, text='You cannot bid negative values').pack()
        return
    if player.get_money() - bid < 0:  # sprawdzenie czy saldo dodatnie
        tk.Label(game, text='You have {}, cannot bid {}'.format(player.get_money(), bid)).pack()
        set_bid(game, croupier, player, deck, difficulty)
        clean(croupier, player, deck)
        return
    player.take_money(bid)  # pobranie pieniędzy
    croupier.give_card(deck)  # podanie krupierowi dwóch kart
    croupier.give_card(deck)
    player.give_card(deck)  # podanie graczowi dwóch kart
    player.give_card(deck)
    show_current_status(game, croupier, player)  # wyświetlenie kart
    if player.is_blackjack():
        player.money_won(int(bid * 2.5))
        print('You have got blackjack! Account status:', player.get_money())
        clean(croupier, player, deck)
        return
    if player.can_split() and player.get_money() > bid:
        print('Do you want to hit, stand or split?')
        choice = str(input())
        if choice == 'hit':
            player.give_card(deck)
            show_current_status(game, croupier, player)
            play_again(game, croupier, player, deck, bid, difficulty)
        elif choice == 'stand':
            stand(game, croupier, player, deck, difficulty, bid)
        elif choice == 'split':
            player.take_money(bid)
            player.hide_second()
            player.give_card(deck)
            show_current_status(game, croupier, player)
            play_again_split(game, croupier, player, deck, bid, difficulty)
            player.show_second()
            player.give_card(deck)
            show_current_status(game, croupier, player)
            play_again_split(game, croupier, player, deck, bid, difficulty)
            croupier.show_second()
            show_current_status(game, croupier, player)
            croupier_move(croupier, player, deck, difficulty)
            show_current_status(game, croupier, player)
            if player.get_cards_sum() > croupier.get_cards_sum():
                player.money_won(bid * 2)
                print('Your second hand won!')
                clean(croupier, player, deck)
                return
            if player.get_cards_sum() == croupier.get_cards_sum():
                player.money_won(bid)
                print('Your second hand drew')
                clean(croupier, player, deck)
                return
            if player.get_cards_sum() < croupier.get_cards_sum():
                print('Your second hand lost')
                clean(croupier, player, deck)
                return
            player.move_cards_back()
            if player.get_cards_sum() > croupier.get_cards_sum():
                player.money_won(bid * 2)
                print('Your first hand won!')
                clean(croupier, player, deck)
                return
            if player.get_cards_sum() == croupier.get_cards_sum():
                player.money_won(bid)
                print('Your first hand drew')
                clean(croupier, player, deck)
                return
            if player.get_cards_sum() < croupier.get_cards_sum():
                print('Your first hand lost')
                clean(croupier, player, deck)
                return
            print('Account status:', player.get_money())
            clean(croupier, player, deck)
            return
        else:
            print('Wrong choice')
            return
    if croupier.is_first_card_ace() and player.get_money() >= bid * 0.5:
        print('Do you want to hit, stand or have insurance?')
        choice = str(input())
        if choice == 'hit':
            player.give_card(deck)
            show_current_status(game, croupier, player)
            play_again(game, croupier, player, deck, bid, difficulty)
            clean(croupier, player, deck)
            return
        elif choice == 'stand':
            stand(game, croupier, player, deck, difficulty, bid)
        elif choice == 'have insurance' or choice == 'insurance':
            player.take_money(int(bid * 0.5))
            play_again(game, croupier, player, deck, bid, difficulty)
            if croupier.is_blackjack():
                player.money_won(bid)
                print('Croupier has blackjack, you have won your insurance, account status', player.get_money())
                clean(croupier, player, deck)
                return
        else:
            print('Wrong choice')
            return
    if player.get_cards_sum() > 21:
        print('You have lost, account status:', player.get_money())
        clean(croupier, player, deck)
        return
    print('Do you want to hit, stand or double?')
    choice = str(input())
    if choice == 'hit':
        player.give_card(deck)
        show_current_status(game, croupier, player)
        play_again(game, croupier, player, deck, bid, difficulty)
        clean(croupier, player, deck)
        return
    elif choice == 'stand':
        stand(game, croupier, player, deck, difficulty, bid)
    elif choice == 'double':
        player.take_money(bid)
        player.give_card(deck)
        croupier.show_second()
        show_current_status(game, croupier, player)
        croupier_move(croupier, player, deck, difficulty)
        show_current_status(game, croupier, player)
        if player.get_cards_sum() > croupier.get_cards_sum():
            player.money_won(bid * 4)
            print('You have won! Account status:', player.get_money())
            clean(croupier, player, deck)
            return
        elif player.get_cards_sum() > croupier.get_cards_sum():
            player.money_won(bid * 2)
            print('Draw, account status:', player.get_money())
            clean(croupier, player, deck)
            return
        else:
            print('You have lost, account status:', player.get_money())
            clean(croupier, player, deck)
            return
    else:
        print('Wrong choice')
        return


def start_game(difficulty_level: tk.StringVar, starting_money: tk.IntVar) -> None:
    game = tk.Toplevel()
    game.title('Blackjack')  # nawza na pasku
    game.geometry('800x600')  # wymiary okna

    difficulty_level = difficulty_level.get()  # oraz poziomu trudności
    if difficulty_level == '':
        difficulty_level = 'medium'
    try:
        starting_money = starting_money.get()  # bezpieczne ustawienie wartości początkowej stanu konta
    except ValueError:
        starting_money = 5000
    croupier = Croupier()  # stworzenie instacnji Croupier
    player = Player(starting_money)  # stworzenie instacnji Player
    deck = Deck()  # stworzenie instacnji Deck
    set_bid(game, croupier, player, deck, difficulty_level)  # rozpoczęcie gry

    game.mainloop()


def main() -> None:
    root = tk.Tk()  # główne okno
    root.title('Blackjack')  # nawza na pasku
    root.geometry('300x220')  # wymiary okna

    welcoming_label = tk.Label(root, text='Welcome in the blackjack game!')
    welcoming_label.pack()  # umieszcza napis witający
    info_label = tk.Label(root, text='Select starting configuration')
    info_label.pack()  # umieszcza napis informujący o konfiguracji gry
    difficulty_level_info = tk.Label(root, text='Choose diffiuclty level:')
    difficulty_level_info.pack()  # umieszcza napis informujący o wyborze trudności
    difficulty_level = tk.StringVar()
    difficulty_level.set('medium')  # domyślna waartość poziomu trudności na wyświetlaczu
    medium_radio = tk.Radiobutton(root, text='medium', variable=difficulty_level, value='medium')
    medium_radio.pack()  # umieszcza przycisk wyboru poziomu trudności
    hard_radio = tk.Radiobutton(root, text='hard', variable=difficulty_level, value='hard')
    hard_radio.pack()  # umieszcza przycisk wyboru poziomu trudności
    starting_money_info = tk.Label(root, text='Type amount of money on your starting account:')
    starting_money_info.pack()  # umieszcza napis, gdzie wpisać wartość konta
    starting_money = tk.IntVar()  # początkowa wartość konta (str)
    starting_money.set(5000)  # domyślna wartość pieniędzy na wyświetlaczu
    starting_money_entry = tk.Entry(root, textvariable=starting_money)
    starting_money_entry.pack()  # umieszcza ramkę, do której można wpisać wartość konta
    start_button = tk.Button(root, text='Start the game', width=20,
                             command=lambda: start_game(difficulty_level, starting_money))
    start_button.pack()  # umieszcza przycisk do rozpoczęcia gry
    exit_button = tk.Button(root, text='End the game', width=20, command=root.quit)
    exit_button.pack()   # umieszcza przycisk do zakończenia gry

    root.mainloop()  # ciągłe wykonywanie dopóki nie zamknie się okna


if __name__ == '__main__':
    main()
