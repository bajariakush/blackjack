'''Blackjack game implementation'''
from .player import Player, Dealer
from .card import create_shoe, insert_cut_card

import pickle
import os

class BlackJackGame:
    '''blackjack game class'''
    def __init__(self):
        self.players = []
        self.dealer = Dealer("computer AI")
        self.shoe = create_shoe()
        insert_cut_card(self.shoe)
    
    def save_player_banks(self, filename='player_banks.pkl'):
        '''saves the game to a file'''
        player_banks ={player.name: player.bank for player in self.players}
        with open(filename, 'wb') as f:
            pickle.dump((player_banks), f)

    def load_player_banks(self, filename='player_banks.pkl'):
        '''loads player bank from a file'''
        if os.path.exists(filename):
            with open(filename, 'rb') as f:
                return pickle.load(f)
        return {}


    def run(self):
        '''starts the game'''
        print("Kush's Blackjack Table\n")
        while True:
            try:
                recurring_player = input("Welcome to Blackjack! Are you new to the game? (y/n): ").lower()
                if recurring_player == 'y':
                    print("Welcome! Please create a username to continue.")
                    username = input("Create a username: ")
                    player_banks = self.load_player_banks()
                    if username in player_banks:
                        print(f'Welcome back {username}! Your current bank balance is ${player_banks[username]}.')
                    else:
                        print(f'Welcome {username}! Your starting balance is $100.')
                        player_banks[username] = 100
                        self.players.append(Player(username, player_banks[username]))
                    break
                elif recurring_player == 'n':
                    print("Welcome back! Please enter your username to continue.")
                    username = input("Enter your username: ")
                    player_banks = self.load_player_banks()
                    if username in player_banks:
                        print(f'Welcome back {username}! Your current bank balance is ${player_banks[username]}.')
                    else:
                        print(f'Welcome back {username}! It seems you have no previous bank balance. Starting with $100.')
                        player_banks[username] = 100
                        self.players.append(Player(username, player_banks[username]))
                    break
                else:
                    print("Invalid input. Please enter 'y' or 'n'.")
            except ValueError:
                print("Invalid input. Please enter 'y' or 'n'.")

        while True:
            print("\nStarting a new round...")
            for player in self.players:
                if player.bank <= 0:
                    print(f'{player.name} is broke. An anonymous donor has given them $100!')
                    player.bank = 100
            bets = {}
            for player in self.players:
                while True:
                    try:
                        bet = int(input(f'{player.name}, bets are open (1-{player.bank}): '))
                        if 1 <= bet <= player.bank:
                            bets[player] = bet
                            break
                        print(f"Invalid bet. Please enter a number between 1 and {player.bank}.")
                    except ValueError:
                        print("Invalid input. Please enter a number.")

            # clear hands
            for player in self.players:
                player.clear_hand()
            self.dealer.clear_hand()

            # deal initial cards
            for _ in range(2):
                for player in self.players:
                    player.add_card(self.shoe.pop())
                self.dealer.add_card(self.shoe.pop())

            # show dealer's first card
            print(f"Dealer's showing card: {self.dealer.reveal_hand()}")

            # player turns
            for player in self.players:
                print(f"\n{player.name}'s turn:")
                while True:
                    print(f"Your hand: {player.hand}, value: {player.hand_value()}")
                    if player.bust():
                        print('You busted!')
                        break
                    move = input('Hit or stand? (h/s): ').lower()
                    if move == 'h':
                        player.add_card(self.shoe.pop())
                    elif move == 's':
                        break
                    else:
                        print("Invalid input. Please enter 'h' to hit or 's' to stand.")

            # dealers turn
            print(f"\nDealer's hand: {self.dealer.hand}, value: {self.dealer.hand_value()}")
            while self.dealer.should_hit():
                print("Dealer hits.")
                self.dealer.add_card(self.shoe.pop())
            print(f"Dealer's final hand: {self.dealer.hand}, value: {self.dealer.hand_value()}")
            if self.dealer.bust():
                print("Dealer busted!")

            # handle bets
            for player in self.players:
                if player.bust():
                    print(f"{player.name} lost their bet of {bets[player]}.")
                    player.adjust_bank(-bets[player])
                elif self.dealer.bust() or player.hand_value() > self.dealer.hand_value():
                    print(f"{player.name} wins {bets[player] * 2}!")
                    player.adjust_bank(bets[player] * 2)
                elif player.hand_value() < self.dealer.hand_value():
                    print(f"{player.name} lost their bet of {bets[player]}.")
                    player.adjust_bank(-bets[player])
                else:
                    print(f"{player.name} ties with the dealer. Bet returned.")
                    player.adjust_bank(0)

            # check for cut card
            if "CUT_CARD" in self.shoe:
                print("Cut card reached. Reshuffling the shoe.")
                self.shoe = create_shoe()
                insert_cut_card(self.shoe)

            # ask players if they want to play another round
            play_again = input("\nDo you want to play another round? (y/n): ").lower()
            if play_again != 'y':
                print("Thanks for playing!")
                print(f'Your remaining bank balance is ${player_banks[username]}.')
                break

        self.save_player_banks()

        return 0