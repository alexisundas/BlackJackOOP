import random
import os
import emojis

suits = (":hearts:", ":diamonds:", ":spades:", ":clubs:")
ranks = ('Two', 'Three', 'Four', 'Five', 'Six', 'Seven', 'Eight', 'Nine', 'Ten', 'Jack', 'Queen', 'King', 'Ace')
values = {'Two':2, 'Three':3, 'Four':4, 'Five':5, 'Six':6, 'Seven':7, 'Eight':8, 'Nine':9, 'Ten':10, 'Jack':10,
         'Queen':10, 'King':10, 'Ace':11}

playing = True

class Card:
    
    def __init__(self,suit,rank):
        self.suit = suit
        self.rank = rank
    
    def __str__(self):
        return emojis.encode(self.rank + " of " + self.suit)

class Deck:
    
    def __init__(self):
        self.deck = []  # start with an empty list
        for suit in suits:
            for rank in ranks:
                created_card = Card(suit,rank)
                self.deck.append(created_card)
    
    def __str__(self):
        deck_comp = ''
        for card in self.deck:
            deck_comp += "\n" + card.__str__()
        return "The deck has: "+deck_comp

    def shuffle(self):
        random.shuffle(self.deck)
        
    def deal(self):
        return self.deck.pop()

class Hand:
    def __init__(self):
        self.cards = []  # start with an empty list as we did in the Deck class
        self.value = 0   # start with zero value
        self.aces = 0    # add an attribute to keep track of aces
    
    def add_card(self,card):
        #from Deck.deal() --> Single Card(suit,rank)
        self.cards.append(card)
        self.value += values[card.rank]

        #track aces
        if card.rank == 'Ace':
            self.aces += 1
    
    def adjust_for_ace(self):
        while self.value > 21 and self.aces:
            self.value -= 10
            self.aces -= 1

class Chips:
    
    def __init__(self):
        self.total = 100  # This can be set to a default value or supplied by a user input
        self.bet = 0
        
    def win_bet(self):
        self.total += self.bet
    
    def lose_bet(self):
        self.total -= self.bet


def take_bet(chips):

    while True:
        try:
            chips.bet = int(input("How much :dollar: money do you want to bet? "))
        except ValueError:
            print("Please use numbers")
        else:
            if chips.bet > chips.total:
                print(emojis.encode("You don't have enough money :dollar: :warning:"))
            else:
                break


def hit(deck,hand):
    
    single_card = deck.deal()
    hand.add_card(single_card)
    hand.adjust_for_ace()

def hit_or_stand(deck,hand):
    global playing  # to control an upcoming while loop
    
    while True:
        x = input("Would you like to Hit or Stand? Enter 'h' or 's' ")
        
        if x[0].lower() == 'h':
            hit(deck,hand)  # hit() function defined above

        elif x[0].lower() == 's':
            print("Player stands. Dealer is playing.")
            playing = False

        else:
            print("Sorry, please try again.")
            continue
        break

def show_some(player,dealer):
    print("\nDealer's Hand:")
    print(" <card hidden>")
    print('',dealer.cards[1])  
    print("\nPlayer's Hand:", *player.cards, sep='\n ')
    
def show_all(player,dealer):
    print("\nDealer's Hand:", *dealer.cards, sep='\n ')
    print("Dealer's Hand =",dealer.value)
    print("\nPlayer's Hand:", *player.cards, sep='\n ')
    print("Player's Hand =",player.value)

def player_busts(player,dealer,chips):
    print(emojis.encode("BUST PLAYER! :crying_cat_face:"))
    chips.lose_bet()
    

def player_wins(player,dealer,chips):
    print(emojis.encode("PLAYER WINS!:white_check_mark:"))
    chips.win_bet()

def dealer_busts(player,dealer,chips):
    print(emojis.encode("PLAYER WINS! :white_check_mark:  DEALER BUSTED"))
    chips.win_bet()

def dealer_wins(player,dealer,chips):
    print(emojis.encode("DEALER WINS! PLAYER BUSTED :crying_cat_face:"))
    chips.lose_bet()

def push(player,dealer):
    print("Dealer and player tie! PUSH")



if __name__ == "__main__":
    while True:
        # Print an opening statement
        os.system('clear')

        print('Welcome to BlackJack! Get as close to 21 as you can without going over!\n\
        Dealer hits until she reaches 17. Aces count as 1 or 11.\n')
        # Create & shuffle the deck, deal two cards to each player
        Player = Hand()
        Dealer = Hand()

        the_deck = Deck()
        the_deck.shuffle()

        Player.add_card(the_deck.deal())
        Player.add_card(the_deck.deal())
        Dealer.add_card(the_deck.deal())
        Dealer.add_card(the_deck.deal())

        # Set up the Player's chips
        bankaccount = Chips()
        
        # Prompt the Player for their bet
        take_bet(bankaccount)
        # Show cards (but keep one dealer card hidden)
        show_some(Player,Dealer)
            

        
        while playing:  # recall this variable from our hit_or_stand function
            # Prompt for Player to Hit or Stand
            hit_or_stand(the_deck,Player)
            
            # Show cards (but keep one dealer card hidden)
            show_some(Player,Dealer)
            
            # If player's hand exceeds 21, run player_busts() and break out of loop
            if Player.value > 21:
                player_busts(Player,Dealer,bankaccount)
                break

        if Player.value <= 21:
            
            while Dealer.value < 17:
                hit(the_deck,Dealer)    

            # Show all cards
            show_all(Player,Dealer)
            
            # Run different winning scenarios
            if Dealer.value > 21:
                dealer_busts(Player,Dealer,bankaccount)
                
                

            elif Dealer.value > Player.value:
                dealer_wins(Player,Dealer,bankaccount)
                
                

            elif Dealer.value < Player.value:
                player_wins(Player,Dealer,bankaccount)
                
                

            else:
                push(Player,Dealer)

        # Inform Player of their chips total 
        print("\nPlayer's winnings stand at ",bankaccount.total)
        
        # Ask to play again
        new_game = input("Would you like to play another hand? Enter 'y' or 'n' ")
        
        if new_game[0].lower()=='y':
            playing=True
            continue
        else:
            print("Thanks for playing!")
            break

