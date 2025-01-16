# Dr Michaels
# game.py
# 3/30/22
# This file contains information on a card and deck class.
# Together we will build a player class
# Then begin designing rules for a game

# Global variables used to create a new deck
face = [2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14]
suit = ["Clubs", "Diamonds", "Hearts", "Spades"]

import random

class Card:
    # Constructor method for Card.
    # Takes as input a face and suit value.
    # If they are not found in the global variables above, the card will be set to a 2 of clubs
    def __init__(self, the_face, the_suit):
        global face, suit
        if (the_face in face and the_suit in suit):
            self.face = the_face
            self.suit = the_suit
        else:
            #print("Illegal card value, creating a 2 of Clubs")
            self.face = -1
            self.suit = "ILLEGAL CARD"

    # Retuns the suit value of the calling card
    def get_suit(self):
        return self.suit

    # Returns the face value of the calling card
    def get_face(self):
        return self.face

    # Compares the face and suit attributes of other_card to those possessed by the calling card
    def __eq__(self, other_card):
        return (self.face == other_card.get_face()) and (self.suit == other_card.get_suit())

    # Returns the value of self > other_card
    # The first comparison is on face value. If the faces are different, we return the result of
    # self.face > other_card.get_face()
    # If they are tied, we return the result of self.suit > other_card.get_suit()
    def __gt__(self, other_card):
        if self.face > other_card.get_face():
            return True
        elif (self.face == other_card.get_face()):
            return self.suit > other_card.get_suit()
        else:
            return False

    # Card tostring. Will return the card in the format "Face of Suit"
    def __str__(self):
        return "%s of %s" % (self.face, self.suit)


class Deck:

    # The constructor method for the Deck.
    # It takes no parameters.
    # It fills a deck with 52 unique card, and then uses random.shuffle to randomly order the deck
    # The counter will be used to indicate which card is at the "top" of the deck
    # i.e. all cards above counter will have been dealt
    def __init__(self):
        self.deck = []
        self.counter = 0
        global face
        global suit
        for the_face in face:
            for the_suit in suit:
                self.deck.append(Card(the_face, the_suit))
        for i in range(7):
            random.shuffle(self.deck)

    # Returns the top card of the deck if it exists (if we have not previously dealt 52 cards)
    # We could add in a method to automatically shuffle the deck if we reach this point
    def deal(self):
        if self.counter < 52:
            result = self.deck[self.counter]
            self.counter += 1
            return result

    # Randomly shuffles the deck array seven times.
    def shuffle(self):
        self.counter = 0
        for i in range(7):
            random.shuffle(self.deck)

    # tostring method for deck class.
    # Prints out all 52 cards in the deck, one per line.
    # We indicate with an X cards that have been dealt
    # << Current Top Card indicates which card is the current top of the deck.
    def __str__(self):
        result = ""
        for i in range(52):
            if i == self.counter:
                result += "%s << Current Top Card\n" % self.deck[i]
            elif i < self.counter:
                result += "%s X\n" % self.deck[i]
            else:
                result += "%s\n" % self.deck[i]
        return result



# A class which defines the Game of War.
# The rules of war are as follows:
	# 2 Players
	# 1 Deck of cards (52 unique cards)
	# Could change/expand the base datapoints
	# Deal the cards
	# Cycle of Play
		# Round by round/turn by turn
		# Each player draws a card, and presents it (c1 and c2)
		# If c1 > c2, P1 wins, and gets both cards into their discard
		# If c2 > c1, P2 wins, ...
		# There is no possibility of tie (This will change)
		# Play continues until no cards are in the hand (at the start, 26 rounds/turns will go by)
		# shuffle the discard pile into the hand, and play continues
	# Win Condition:
		# Default is one of the players has all 52 cards
		# We'll look at two possibilities:
			# X Turns of have passed, the player with more cards wins
			# Once a player has X number of cards total (hand + discard)
class War_Game:

    # The init method. It defines both players and the deck.
    def __init__(self, num_players):
        self.deck = Deck()
        self.players = []
        if num_players < 2:
            num_players = 2
        elif num_players > 8:
            num_players = 8
        for i in range(num_players):
            name = "Player %d" % (i+1)
            self.players.append(War_Player(name))

    def deal_cards(self):
        # Assumes hands are empty
        self.deck.shuffle()
        counter = 0
        while(self.players[0].get_hand_size() < 26):
            for player in self.players:
                player.add_card_hand(self.deck.deal())
                counter += 1
                if counter == 52:
                    self.deck.shuffle()
                    counter = 0

    def initialize_game(self):
        for player in self.players:
            player.reset_player()
        self.deal_cards()

    def play_round(self):
        # Get a card from all players, and find the biggest
        cards = []
        for player in self.players:
            cards.append(player.play_card())

        winner = cards.index(max(cards))
        self.players[winner].add_card_discard(cards)

    def game_won(self):
        result = -1
        for i in range(len(self.players)):
            if self.players[i].get_total_cards() >= 39:
                result = i
                return result
        return result

    def check_shuffle(self):
        for player in self.players:
            if player.get_hand_size() == 0:
                player.shuffle_discard()

    def play_game(self):
        check_win = self.game_won()
        counter = 0
        while(check_win == -1):
            self.check_shuffle()
            self.play_round()
            counter += 1
            check_win = self.game_won()
        print("The game is over! %s has won the game!" % self.players[check_win].get_name())
        print("The game took %d rounds to finish!" % counter)
        for i in range(len(self.players)):
            if i == check_win:
                self.players[i].add_win()
            else:
                self.players[i].add_loss()


    # Tostring for War_Game
    def __str__(self):
        result = "CURRENT GAME STATUS\n"
        for player in self.players:
            result += "%s\n\n" % player
        return result


class War_Player:

    def __init__(self, name):
        self.hand = []
        self.discard = []
        self.record = [0,0] # Wins/Losses
        self.myname = name

    def get_name(self):
        return self.myname

    def add_card_hand(self, my_card):
        self.hand.append(my_card)

    def add_card_discard(self, cards_won):
        for my_card in cards_won:
            self.discard.append(my_card)

    def reset_player(self):
        self.hand = []
        self.discard = []

    def play_card(self):
        return self.hand.pop()

    def get_hand_size(self):
        return len(self.hand)

    def get_discard_size(self):
        return len(self.discard)

    def get_total_cards(self):
        return len(self.discard) + len(self.hand)

    def shuffle_discard(self):
        # Shuffle discard and then add to Hand, while removing from discard
        for i in range(7):
            random.shuffle(self.discard)
        while(len(self.discard) > 0):
            self.add_card_hand(self.discard.pop())

    def add_win(self):
        self.record[0] += 1

    def add_loss(self):
        self.record[1] += 1


    def __str__(self):
        result = "%s\n" % self.myname
        result += "Wins: %d Losses: %d\n" % (self.record[0], self.record[1])
        result += "Hand: "
        for item in self.hand:
            result += "%s, " % item
        result += "\nDiscard: "
        for item in self.discard:
            result += "%s, " % item
        return result



def main():

    my_game = War_Game(4)
    print("Time to play the game!")
    print("First we must do testing!")
    # my_game.deal_cards()
    # print(my_game)
    for i in range(10):
        my_game.initialize_game()
        my_game.play_game()
    print("\n\n\n%s" % my_game)




main()
