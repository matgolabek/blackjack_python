import tkinter as tk
from participant import Player, Croupier
from deck import Deck
import webbrowser


def clean(game: tk.Toplevel, croupier: Croupier, player: Player, deck: Deck, difficulty: str, deck_g: str, table_g: str) -> None:
    croupier.clean_hand()
    player.clean_hand()
    deck.shuffle_if_needed()
    for widget in game.winfo_children():
        widget.destroy()

    try:
        background_label = tk.Label(game)  # grafika stołu
        background_label.place(x=0, y=0, relwidth=1, relheight=1)  # umieszczenie pod innymi elementami
        background_label.image = tk.PhotoImage(file=table_g)
        background_label.configure(image=background_label.image)
    except FileNotFoundError:
        background_label = tk.Label(game)  # grafika stołu
        background_label.place(x=0, y=0, relwidth=1, relheight=1)  # umieszczenie pod innymi elementami
        background_label.image = tk.PhotoImage(file='graphics/tables/Motyw_jasny.png')
        background_label.configure(image=background_label.image)

    set_bid(game, croupier, player, deck, difficulty, deck_g, table_g)


def show_current_status(game: tk.Toplevel, croupier: Croupier, player: Player, deck_g: str) -> None:
    for widget in croupier.get_visible_cards():
        widget.destroy()
    for widget in player.get_visible_cards():
        widget.destroy()
    croupier.show_cards(game, deck_g)
    player.show_cards(game)


def show_win_info(game: tk.Toplevel, croupier: Croupier, player: Player, deck: Deck, difficulty: str, deck_g: str, table_g: str, is_blackjack: bool = False, first_hand: bool = False,
                  second_hand: bool = False) -> None:
    def cont():  # continue
        info_box.destroy()
        clean(game, croupier, player, deck, difficulty, deck_g, table_g)

    info_box = tk.Toplevel(game)
    info_box.title('You have won!')
    info_box.geometry('600x80+400+300')  # jak ma być na środku chyba trzeba przekazać tu parametr game

    if is_blackjack:
        tk.Label(info_box, text=f'You have got blackjack! Account status: {player.get_money()}',
                 font=('Arial', 20)).pack()
    elif first_hand:
        tk.Label(info_box, text='Your first hand won!').pack()
    elif second_hand:
        tk.Label(info_box, text='Your second hand won!').pack()
    else:
        tk.Label(info_box, text=f'You have won! Account status: {player.get_money()}', font=('Arial', 20)).pack()
    tk.Button(info_box, text='OK', width=20, command=cont).pack()

    info_box.mainloop()


def show_draw_info(game: tk.Toplevel, croupier: Croupier, player: Player, deck: Deck, difficulty: str, deck_g: str, table_g: str, first_hand: bool = False, second_hand: bool = False) -> None:
    def cont():
        info_box.destroy()
        clean(game, croupier, player, deck, difficulty, deck_g, table_g)

    info_box = tk.Toplevel(game)
    info_box.title('Draw')
    info_box.geometry('600x80+400+300')
    if first_hand:
        tk.Label(info_box, text='Your first hand drew').pack()
    elif second_hand:
        tk.Label(info_box, text='Your second hand drew').pack()
    else:
        tk.Label(info_box, text=f'Draw! Account status: {player.get_money()}', font=('Arial', 20)).pack()
    tk.Button(info_box, text='OK', width=20, command=cont).pack()

    info_box.mainloop()


def show_lose_info(game: tk.Toplevel, croupier: Croupier, player: Player, deck: Deck, difficulty: str, deck_g: str, table_g: str, is_hand: bool = False, first_hand: bool = False, second_hand: bool = False,
                   insurance: bool = False) -> None:
    def cont():
        info_box.destroy()
        clean(game, croupier, player, deck, difficulty, deck_g, table_g)

    info_box = tk.Toplevel(game)
    info_box.title('Lose')
    info_box.geometry('600x80+400+300')
    if is_hand:
        tk.Label(info_box, text=f'Your hand has lost', font=('Arial', 20)).pack()
    elif first_hand:
        tk.Label(info_box, text='Your first hand lost').pack()
    elif second_hand:
        tk.Label(info_box, text='Your second hand lost').pack()
    elif insurance:
        tk.Label(info_box, text=f'Croupier has blackjack, you have won your insurance, account status: {player.get_money()}').pack()

    else:
        tk.Label(info_box, text=f'You have lost, account status: {player.get_money()}', font=('Arial', 20)).pack()
    tk.Button(info_box, text='OK', width=20, command=cont).pack()

    info_box.mainloop()


def croupier_move(croupier: Croupier, player: Player, deck: Deck, difficulty: str) -> None:
    keep_playing = 15
    if difficulty == 'hard':
        player_cards_sum = player.get_cards_sum()
        if player_cards_sum > keep_playing:
            keep_playing = player_cards_sum
    while croupier.get_cards_sum() < keep_playing:
        croupier.give_card(deck)


def stand(game: tk.Toplevel, croupier: Croupier, player: Player, deck: Deck, difficulty: str, deck_g: str, table_g: str, bid: int) -> None:
    croupier.show_second()
    show_current_status(game, croupier, player, deck_g)
    croupier_move(croupier, player, deck, difficulty)
    show_current_status(game, croupier, player, deck_g)
    if player.get_cards_sum() > 21:
        show_lose_info(game, croupier, player, deck, difficulty, deck_g, table_g)
        return
    elif player.get_cards_sum() > croupier.get_cards_sum():
        player.money_won(bid * 2)
        show_win_info(game, croupier, player, deck, difficulty, deck_g, table_g)
        return
    elif player.get_cards_sum() == croupier.get_cards_sum():
        player.money_won(bid)
        show_draw_info(game, croupier, player, deck, difficulty, deck_g, table_g)
        return
    else:
        show_lose_info(game, croupier, player, deck, difficulty, deck_g, table_g)
        return


def play_again_split(game: tk.Toplevel, croupier: Croupier, player: Player, deck: Deck, bid: int,
                     difficulty: str, deck_g: str, table_g: str) -> None:
    if player.get_cards_sum() > 21:
        show_current_status(game, croupier, player, deck_g)
        show_lose_info(game, croupier, player, deck, difficulty, deck_g, table_g, True)
        return

    tk.Button(game, text='Hit', width=20, command=lambda: decision_pas('hit')).place(anchor='center', relx=.8, rely=.45)
    tk.Button(game, text='Stand', width=20, command=lambda: decision_pas('stand')).place(anchor='center', relx=.8,
                                                                                         rely=.55)

    def decision_pas(choice: str):
        if choice == 'hit':
            player.give_card(deck)
            show_current_status(game, croupier, player, deck_g)
            play_again_split(game, croupier, player, deck, bid, difficulty, deck_g, table_g)
            return
        if choice == 'stand':
            player.move_cards()
            return
        else:
            print('Wrong input, stand is chosen')
            player.move_cards()
            return


def play_again(game: tk.Toplevel, croupier: Croupier, player: Player, deck: Deck, bid: int, difficulty: str, deck_g: str, table_g: str) -> None:
    if player.get_cards_sum() > 21:
        croupier.show_second()
        show_current_status(game, croupier, player, deck_g)
        show_lose_info(game, croupier, player, deck, difficulty, deck_g, table_g)
        return

    tk.Button(game, text='Hit', width=20, command=lambda: decision_pa('hit')).place(anchor='center', relx=.8, rely=.45)
    tk.Button(game, text='Stand', width=20, command=lambda: decision_pa('stand')).place(anchor='center', relx=.8,
                                                                                        rely=.5)
    tk.Button(game, text='', width=20).place(anchor='center', relx=.8, rely=.55)

    def decision_pa(choice: str):
        if choice == 'hit':
            player.give_card(deck)
            show_current_status(game, croupier, player, deck_g)
            play_again(game, croupier, player, deck, bid, difficulty, deck_g, table_g)
            return
        if choice == 'stand':
            stand(game, croupier, player, deck, difficulty, deck_g, table_g, bid)
        else:
            print('Wrong input, stand is chosen')
            player.move_cards()
            return


def set_bid(game: tk.Toplevel, croupier: Croupier, player: Player, deck: Deck, difficulty: str, deck_g: str, table_g: str):
    if player.get_money() <= 0:
        tk.Label(game, text='No money, no honey :(').place(anchor='center', relx=.15,
                                                           rely=.45)  # umieszcza wiadomość i kończy
        return
    tk.Label(game, text='How much money do you bid?').place(anchor='center', relx=.15, rely=.45)

    bid = tk.IntVar()  # wartość stawki (str)
    bid.set(100)
    bid_entry = tk.Entry(game, textvariable=bid)
    bid_entry.place(anchor='center', relx=.15, rely=.5)  # umieszcza ramkę, do której można wpisać wartość stawki
    submit_bid = tk.Button(game, text='Submit the bid', width=20,
                           command=lambda: play(game, croupier, player, deck, bid, difficulty, deck_g, table_g))
    submit_bid.place(anchor='center', relx=.15, rely=.55)  # przycisk zatwierdzający stawkę
    tk.Label(game, text=f'Current account status: {player.get_money()}').place(anchor='center', relx=.15, rely=.6)

    game.mainloop()


def play(game: tk.Toplevel, croupier: Croupier, player: Player, deck: Deck, bid: tk.IntVar, difficulty: str, deck_g: str, table_g: str) -> None:
    try:
        bid = bid.get()  # bezpieczne ustawienie wartości stawki
    except ValueError:
        bid = 100
    if bid <= 0:  # sprawdzenie ujemnych stawek
        tk.Label(game, text='You cannot bid negative values').place(anchor='center', relx=.15, rely=.65)
        return
    if player.get_money() - bid < 0:  # sprawdzenie czy saldo dodatnie
        tk.Label(game, text='You have {}, cannot bid {}'.format(player.get_money(), bid)).place(anchor='center',
                                                                                                relx=.15, rely=.65)
        set_bid(game, croupier, player, deck, difficulty, deck_g, table_g)
        clean(game, croupier, player, deck, difficulty, deck_g, table_g)
        return
    player.take_money(bid)  # pobranie pieniędzy
    tk.Label(game, text=f'Current account status: {player.get_money()}').place(anchor='center', relx=.15, rely=.6)
    croupier.give_card(deck)  # podanie krupierowi dwóch kart
    croupier.give_card(deck)
    player.give_card(deck)  # podanie graczowi dwóch kart
    player.give_card(deck)
    show_current_status(game, croupier, player, deck_g)  # wyświetlenie kart
    if player.is_blackjack():
        player.money_won(int(bid * 2.5))
        show_win_info(game, croupier, player, deck, difficulty, deck_g, table_g, True)
        return
    if player.can_split() and player.get_money() > bid:

        tk.Button(game, text='Hit', width=20, command=lambda: decision_split('hit')).place(anchor='center', relx=.8,
                                                                                           rely=.45)
        tk.Button(game, text='Stand', width=20, command=lambda: decision_split('stand')).place(anchor='center', relx=.8,
                                                                                               rely=.5)
        tk.Button(game, text='Split', width=20, command=lambda: decision_split('split')).place(anchor='center', relx=.8,
                                                                                               rely=.55)

        def decision_split(choice: str):
            if choice == 'hit':
                player.give_card(deck)
                show_current_status(game, croupier, player, deck_g)
                play_again(game, croupier, player, deck, bid, difficulty, deck_g, table_g)
            elif choice == 'stand':
                stand(game, croupier, player, deck, difficulty, deck_g, table_g, bid)
            elif choice == 'split':
                player.take_money(bid)
                player.hide_second()
                player.give_card(deck)
                show_current_status(game, croupier, player, deck_g)
                play_again_split(game, croupier, player, deck, bid, difficulty, deck_g, table_g)
                player.show_second()
                player.give_card(deck)
                show_current_status(game, croupier, player, deck_g)
                play_again_split(game, croupier, player, deck, bid, difficulty, deck_g, table_g)
                croupier.show_second()
                show_current_status(game, croupier, player, deck_g)
                croupier_move(croupier, player, deck, difficulty)
                show_current_status(game, croupier, player, deck_g)
                if player.get_cards_sum() > 21:
                    show_lose_info(game, croupier, player, deck, difficulty, deck_g, table_g, second_hand=True)
                elif player.get_cards_sum() > croupier.get_cards_sum():
                    player.money_won(bid * 2)
                    show_win_info(game, croupier, player, deck, difficulty, deck_g, table_g, second_hand=True)
                elif player.get_cards_sum() == croupier.get_cards_sum():
                    player.money_won(bid)
                    show_draw_info(game, croupier, player, deck, difficulty, deck_g, table_g, second_hand=True)
                elif croupier.get_cards_sum() > 21:
                    player.money_won(bid * 2)
                    show_win_info(game, croupier, player, deck, difficulty, deck_g, table_g, second_hand=True)
                elif player.get_cards_sum() < croupier.get_cards_sum():
                    show_lose_info(game, croupier, player, deck, difficulty, deck_g, table_g, second_hand=True)
                player.move_cards_back()
                if player.get_cards_sum() > 21:
                    show_lose_info(game, croupier, player, deck, difficulty, deck_g, table_g, first_hand=True)
                elif player.get_cards_sum() > croupier.get_cards_sum():
                    player.money_won(bid * 2)
                    show_win_info(game, croupier, player, deck, difficulty, deck_g, table_g, first_hand=True)
                elif player.get_cards_sum() == croupier.get_cards_sum():
                    player.money_won(bid)
                    show_draw_info(game, croupier, player, deck, difficulty, deck_g, table_g, first_hand=True)
                elif croupier.get_cards_sum() > 21:
                    player.money_won(bid * 2)
                    show_win_info(game, croupier, player, deck, difficulty, deck_g, table_g, first_hand=True)
                elif player.get_cards_sum() < croupier.get_cards_sum():
                    show_lose_info(game, croupier, player, deck, difficulty, deck_g, table_g, first_hand=True)
                return
            else:
                print('Wrong choice')
                return
    if croupier.is_first_card_ace() and player.get_money() >= bid * 0.5:
        tk.Button(game, text='Hit', width=20, command=lambda: decision_ins('hit')).place(anchor='center', relx=.8,
                                                                                         rely=.45)
        tk.Button(game, text='Stand', width=20, command=lambda: decision_ins('stand')).place(anchor='center', relx=.8,
                                                                                             rely=.5)
        tk.Button(game, text='Insurance', width=20, command=lambda: decision_ins('insurance')).place(anchor='center',
                                                                                                     relx=.8, rely=.55)

        def decision_ins(choice):
            if choice == 'hit':
                player.give_card(deck)
                show_current_status(game, croupier, player, deck_g)
                play_again(game, croupier, player, deck, bid, difficulty, deck_g, table_g)
                return
            elif choice == 'stand':
                stand(game, croupier, player, deck, difficulty, deck_g, table_g, bid)
            elif choice == 'insurance':
                player.take_money(int(bid * 0.5))
                play_again(game, croupier, player, deck, bid, difficulty, deck_g, table_g)
                if croupier.is_blackjack():
                    player.money_won(bid)
                    show_lose_info(game, croupier, player, deck, difficulty, deck_g, table_g, insurance=True)
                    return
            else:
                print('Wrong choice')
                return
    if player.get_cards_sum() > 21:
        show_lose_info(game, croupier, player, deck, difficulty, deck_g, table_g)
        return

    tk.Button(game, text='Hit', width=20, command=lambda: decision('hit')).place(anchor='center', relx=.8, rely=.45)
    tk.Button(game, text='Stand', width=20, command=lambda: decision('stand')).place(anchor='center', relx=.8, rely=.5)
    tk.Button(game, text='Double', width=20, command=lambda: decision('double')).place(anchor='center', relx=.8,
                                                                                       rely=.55)

    def decision(choice: str):
        if choice == 'hit':
            player.give_card(deck)
            show_current_status(game, croupier, player, deck_g)
            play_again(game, croupier, player, deck, bid, difficulty, deck_g, table_g)
            return
        elif choice == 'stand':
            stand(game, croupier, player, deck, difficulty, deck_g, table_g, bid)
        elif choice == 'double':
            player.take_money(bid)
            tk.Label(game, text=f'Current account status: {player.get_money()}').place(anchor='center', relx=.15,
                                                                                       rely=.6)
            player.give_card(deck)
            croupier.show_second()
            show_current_status(game, croupier, player, deck_g)
            croupier_move(croupier, player, deck, difficulty)
            show_current_status(game, croupier, player, deck_g)
            if player.get_cards_sum() > 21:
                show_lose_info(game, croupier, player, deck, difficulty, deck_g, table_g)
            elif player.get_cards_sum() > croupier.get_cards_sum():
                player.money_won(bid * 4)
                show_win_info(game, croupier, player, deck, difficulty, deck_g, table_g)
            elif player.get_cards_sum() == croupier.get_cards_sum():
                player.money_won(bid * 2)
                show_draw_info(game, croupier, player, deck, difficulty, deck_g, table_g)
            elif croupier.get_cards_sum() > 21:
                player.money_won(bid * 4)
                show_win_info(game, croupier, player, deck, difficulty, deck_g, table_g)
            elif player.get_cards_sum() < croupier.get_cards_sum():
                show_lose_info(game, croupier, player, deck, difficulty, deck_g, table_g)
            return
        else:
            print('Wrong choice')
            return


def start_game(difficulty_level: tk.StringVar, starting_money: tk.IntVar, deck_g: str, table_g: str) -> None:
    game = tk.Toplevel()
    game.title('Blackjack')  # nawza na pasku
    game.geometry('980x678')  # wymiary okna

    try:
        background_label = tk.Label(game)  # grafika stołu
        background_label.place(x=0, y=0, relwidth=1, relheight=1)  # umieszczenie pod innymi elementami
        background_label.image = tk.PhotoImage(file=table_g)
        background_label.configure(image=background_label.image)
    except FileNotFoundError:
        background_label = tk.Label(game)  # grafika stołu
        background_label.place(x=0, y=0, relwidth=1, relheight=1)  # umieszczenie pod innymi elementami
        background_label.image = tk.PhotoImage(file='graphics/tables/Motyw_jasny.png')
        background_label.configure(image=background_label.image)

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
    set_bid(game, croupier, player, deck, difficulty_level, deck_g, table_g)  # rozpoczęcie gry

    game.mainloop()


def credits():
    cr = tk.Toplevel()
    cr.title('Credits')
    cr.geometry('200x80')

    tk.Label(cr, text='Source code: Mateusz Gołąbek').pack()
    tk.Label(cr, text='Graphics design: Jan Gallina').pack()
    tk.Label(cr, text='AGH UST 2023').pack()

    cr.mainloop()


def main() -> None:
    root = tk.Tk()  # główne okno
    root.title('Blackjack')  # nawza na pasku
    root.geometry('300x240')  # wymiary okna

    root.eval('tk::PlaceWindow . center')  # okno na środku ekranu

    table_g = 'graphics/tables/Motyw_jasny.png'  # ścieżka do grafiki stołu

    def bright_table():
        nonlocal table_g
        table_g = 'graphics/tables/Motyw_jasny.png'

    def dark_table():
        nonlocal table_g
        table_g = 'graphics/tables/Motyw_ciemny.png'

    deck_g = 'graphics/decks/main_deck.png'  # ścieżka do grafiki talii

    def default_deck():
        nonlocal deck_g
        deck_g = 'graphics/decks/main_deck.png'

    def deck_1():
        nonlocal deck_g
        deck_g = 'graphics/decks/Talia_1.png'

    def deck_2():
        nonlocal deck_g
        deck_g = 'graphics/decks/Talia_2.png'

    def deck_3():
        nonlocal deck_g
        deck_g = 'graphics/decks/Talia_3.png'

    def deck_4():
        nonlocal deck_g
        deck_g = 'graphics/decks/Talia_4.png'

    def deck_5():
        nonlocal deck_g
        deck_g = 'graphics/decks/Talia_5.png'

    menubar = tk.Menu(root)  # stworzenie paska zadań

    file = tk.Menu(menubar, tearoff=0)  # opcje zapisu i odczytu
    menubar.add_cascade(label='File', menu=file)
    file.add_command(label='Save', command=None)  # implementacja serializacji TO DO !!!
    file.add_command(label='Write', command=None)
    file.add_separator()
    file.add_command(label='Exit', command=root.destroy)

    options = tk.Menu(menubar, tearoff=0)  # opcje graficzne
    menubar.add_cascade(label='Options', menu=options)

    view = tk.Menu(menubar, tearoff=0)  # motyw stołu jasny i ciemny
    view.add_command(label='Bright', command=bright_table)
    view.add_command(label='Dark', command=dark_table)

    graphics = tk.Menu(menubar, tearoff=0)  # wybór talii
    graphics.add_command(label='Default', command=default_deck)
    graphics.add_command(label='Deck 1', command=deck_1)
    graphics.add_command(label='Deck 2', command=deck_2)
    graphics.add_command(label='Deck 3', command=deck_3)
    graphics.add_command(label='Deck 4', command=deck_4)
    graphics.add_command(label='Deck 5', command=deck_5)

    options.add_cascade(label='View', menu=view)  # wybór motywu
    options.add_cascade(label='Graphics', menu=graphics)  # wybór talii

    help = tk.Menu(menubar, tearoff=0)  # opcje pomocy
    menubar.add_cascade(label='Help', menu=help)
    help.add_command(label='Game rules', command=lambda: webbrowser.open('https://www.officialgamerules.org/blackjack'))  # link do zasad gry w Blackjacka
    help.add_separator()
    help.add_command(label='Credits', command=credits)  # twórcy

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
                             command=lambda: start_game(difficulty_level, starting_money, deck_g, table_g))
    start_button.pack()  # umieszcza przycisk do rozpoczęcia gry
    exit_button = tk.Button(root, text='End the game', width=20, command=root.quit)
    exit_button.pack()  # umieszcza przycisk do zakończenia gry

    root.config(menu=menubar)  # dodanie paska zadań
    root.mainloop()  # ciągłe wykonywanie dopóki nie zamknie się okna


if __name__ == '__main__':
    main()
