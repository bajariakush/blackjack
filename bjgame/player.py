'''This module defines the player and dealer classes'''


class Player:
    '''player class'''
    def __init__(self, name, bank=100):
        '''initializes player with a name and bank balance'''
        self.name = name
        self.bank = bank
        self.hand = []
        self.is_active = True

    def add_card(self, card):
        '''adds a card to the players hand'''
        self.hand.append(card)

    def clear_hand(self):
        '''clears the players hand'''
        self.hand = []

    def adjust_bank(self, amount):
        '''adjusts the players bank balance'''
        self.bank += amount

    def hand_value(self):
        '''calculates the hand value for the player'''
        value = 0
        aces = 0
        for card in self.hand:
            if card.rank in ["Jack", "Queen", "King"]:
                value += 10
            elif card.rank == "Ace":
                aces += 1
                value += 11
            else:
                value += int(card.rank)
        while value > 21 and aces:
            value -= 10
            aces -= 1
        return value

    def bust(self):
        '''checks if the player busted'''
        return self.hand_value() > 21


class Dealer(Player):
    '''dealer class'''
    def __init__(self, name, bank=100):
        '''initializes dealer with a name and bank balance'''
        super().__init__(name, bank)
        self.is_active = False

    def reveal_hand(self):
        '''reveals the dealer's hand'''
        if self.hand:
            return self.hand[0]
        return None

    def should_hit(self):
        '''determines if the dealer should hit or stand'''
        return self.hand_value() < 17
