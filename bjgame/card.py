'''This module defines the cards and suits'''
import collections
import random

Card = collections.namedtuple("Card", ["rank", "suit"])

SUITS = ["Hearts", "Diamonds", "Clubs", "Spades"]
RANKS = ["2", "3", "4", "5", "6", "7", "8",
         "9", "10", "Jack", "Queen", "King", "Ace"]


def create_deck():
    '''creates deck of cards'''
    return [Card(rank, suit) for suit in SUITS for rank in RANKS]


def create_shoe(num_decks=8):
    '''create a shoe of cards'''
    shoe = []
    for _ in range(num_decks):
        shoe.extend(create_deck())
    random.shuffle(shoe)
    return shoe


def insert_cut_card(shoe):
    '''inserts a cut card into the shoe at a random position'''
    cut_position = random.randint(60, 80)
    cut_index = len(shoe) - cut_position
    shoe.insert(cut_index, "CUT_CARD")
    return cut_index
