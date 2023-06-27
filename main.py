from player import Player
from croupier import Croupier
from card import Deck


def clean(croupier: Croupier, player: Player, deck: Deck) -> None:
    croupier.clean_hand()
    player.clean_hand()
    deck.shuffle_if_needed()


def show_current_status(croupier: Croupier, player: Player) -> None:
    croupier.show_cards()
    print()
    player.show_cards()
    print()


def croupier_move(croupier: Croupier, player: Player, deck: Deck, difficulty: str) -> None:
    keep_playing = 15
    if difficulty == 'hard':
        player_cards_sum = player.get_cards_sum()
        if player_cards_sum > keep_playing:
            keep_playing = player_cards_sum
    while croupier.get_cards_sum() < keep_playing:
        croupier.give_card(deck)


def play_again_split(croupier: Croupier, player: Player, deck: Deck, bid: int, difficulty: str) -> None:
    if player.get_cards_sum() > 21:
        show_current_status(croupier, player)
        print('Your hand has lost')
        return
    print('Do you want to hit or stand?')
    choice = str(input())
    if choice == 'hit':
        player.give_card(deck)
        show_current_status(croupier, player)
        play_again_split(croupier, player, deck, bid, difficulty)
        return
    if choice == 'stand':
        player.move_cards()
        return
    else:
        print('Wrong input, stand is chosen')
        player.move_cards()
        return


def play_again(croupier: Croupier, player: Player, deck: Deck, bid: int, difficulty: str) -> None:
    if player.get_cards_sum() > 21:
        croupier.show_second()
        show_current_status(croupier, player)
        print('You have lost, account status: ', player.get_money())
        return
    print('Do you want to hit or stand?')
    choice = str(input())
    if choice == 'hit':
        player.give_card(deck)
        show_current_status(croupier, player)
        play_again_split(croupier, player, deck, bid, difficulty)
        return
    if choice == 'stand':
        croupier.show_second()
        show_current_status(croupier, player)
        croupier_move(croupier, player, deck, difficulty)
        show_current_status(croupier, player)
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
    else:
        print('Wrong input, stand is chosen')
        player.move_cards()
        return


def play(croupier: Croupier, player: Player, deck: Deck, difficulty: str = 'medium') -> None:
    if player.get_money() <= 0:
        print('No money, no honey :(')
        return
    print('How much money do you bid?')
    try:
        bid = int(input())
    except ValueError:
        print('Wrong input')
        return
    if bid <= 0:
        print('You cannot bid negative values')
        return
    if player.get_money() - bid < 0:
        print('You have {}, cannot bid {}'.format(player.get_money(), bid))
        play_again(croupier, player, deck, bid, difficulty)
        clean(croupier, player, deck)
        return
    player.take_money(bid)
    croupier.give_card(deck)
    croupier.give_card(deck)
    player.give_card(deck)
    player.give_card(deck)
    show_current_status(croupier, player)
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
            show_current_status(croupier, player)
            play_again(croupier, player, deck, bid, difficulty)
        elif choice == 'stand':
            croupier.show_second()
            show_current_status(croupier, player)
            croupier_move(croupier, player, deck, difficulty)
            show_current_status(croupier, player)
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
        elif choice == 'split':
            player.take_money(bid)
            player.hide_second()
            player.give_card(deck)
            show_current_status(croupier, player)
            play_again_split(croupier, player, deck, bid, difficulty)
            player.show_second()
            player.give_card(deck)
            show_current_status(croupier, player)
            play_again_split(croupier, player, deck, bid, difficulty)
            croupier.show_second()
            show_current_status(croupier, player)
            croupier_move(croupier, player, deck, difficulty)
            show_current_status(croupier, player)
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
            show_current_status(croupier, player)
            play_again(croupier, player, deck, bid, difficulty)
            clean(croupier, player, deck)
            return
        elif choice == 'stand':
            croupier.show_second()
            show_current_status(croupier, player)
            croupier_move(croupier, player, deck, difficulty)
            show_current_status(croupier, player)
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
        elif choice == 'have insurance' or choice == 'insurance':
            player.take_money(int(bid * 0.5))
            play_again(croupier, player, deck, bid, difficulty)
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
        show_current_status(croupier, player)
        play_again(croupier, player, deck, bid, difficulty)
        clean(croupier, player, deck)
        return
    elif choice == 'stand':
        croupier.show_second()
        show_current_status(croupier, player)
        croupier_move(croupier, player, deck, difficulty)
        show_current_status(croupier, player)
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
    elif choice == 'double':
        player.take_money(bid)
        player.give_card(deck)
        croupier.show_second()
        show_current_status(croupier, player)
        croupier_move(croupier, player, deck, difficulty)
        show_current_status(croupier, player)
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


def main() -> None:
    print('Welcome in the blackjack game! If you want to play type \'Y\', to quit type \'n\'')
    starting = str(input())
    if starting == 'n' or starting == 'N':
        return
    elif starting == 'Y' or starting == 'y':
        print('Choose difficulty level, type \'medium\' or \'hard\'')
        difficulty_level = str(input())
        if not (difficulty_level == 'medium' or difficulty_level == 'm'
                or difficulty_level == 'hard' or difficulty_level == 'h'):
            difficulty_level = 'medium'
        print('Type amount of money on your starting account')
        try:
            starting_money = int(input())
        except ValueError:
            starting_money = 5000
        croupier = Croupier()
        player = Player(starting_money)
        deck = Deck()
        play(croupier, player, deck, difficulty_level)
        if player.get_money() <= 0:
            print('No money, no honey :(')
            return
        while player.get_money() > 0:
            print('If you want to play again, type \'Y\', to quit type \'n\'')
            starting = str(input())
            if starting == 'n' or starting == 'N':
                return
            elif starting == 'Y' or starting == 'y':
                play(croupier, player, deck, difficulty_level)
    else:
        return


if __name__ == '__main__':
    main()
