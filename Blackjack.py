# Modules
import random
from colorama import init
from colorama import Fore, Back, Style
init()

# Card variable definitions
suits = ('Hearts', 'Diamonds', 'Spades', 'Clubs')
ranks = ('Two', 'Three', 'Four', 'Five', 'Six', 'Seven', 'Eight', 'Nine', 'Ten', 'Jack', 'Queen', 'King', 'Ace')
values = {'Ace of Hearts': 11, 'Two of Hearts': 2, 'Three of Hearts': 3, 'Four of Hearts': 4, 'Five of Hearts': 5,
          'Six of Hearts': 6,
          'Seven of Hearts': 7, 'Eight of Hearts': 8, 'Nine of Hearts': 9, 'Ten of Hearts': 10, 'Jack of Hearts': 10,
          'Queen of Hearts': 10, 'King of Hearts': 10, 'Ace of Diamonds': 11, 'Two of Diamonds': 2,
          'Three of Diamonds': 3,
          'Four of Diamonds': 4, 'Five of Diamonds': 5, 'Six of Diamonds': 6, 'Seven of Diamonds': 7,
          'Eight of Diamonds': 8,
          'Nine of Diamonds': 9, 'Ten of Diamonds': 10, 'Jack of Diamonds': 10, 'Queen of Diamonds': 10,
          'King of Diamonds': 10,
          'Ace of Spades': 11, 'Two of Spades': 2, 'Three of Spades': 3, 'Four of Spades': 4, 'Five of Spades': 5,
          'Six of Spades': 6,
          'Seven of Spades': 7, 'Eight of Spades': 8, 'Nine of Spades': 9, 'Ten of Spades': 10, 'Jack of Spades': 10,
          'Queen of Spades': 10, 'King of Spades': 10, 'Ace of Clubs': 11, 'Two of Clubs': 2, 'Three of Clubs': 3,
          'Four of Clubs': 4, 'Five of Clubs': 5, 'Six of Clubs': 6, 'Seven of Clubs': 7, 'Eight of Clubs': 8,
          'Nine of Clubs': 9,
          'Ten of Clubs': 10, 'Jack of Clubs': 10, 'Queen of Clubs': 10, 'King of Clubs': 10}


# Card

class Card():

    def __init__(self, suit, rank):
        self.suit = suit
        self.rank = rank

    def __str__(self):
        return f'{self.rank} of {self.suit}'


# Random card generator

randomcard = Card(suits[random.randint(0, 3)], ranks[random.randint(0, 12)])


# Deck

class Deck():

    def __init__(self):
        self.deck = []
        self.dealt = []
        for suit in suits:
            for rank in ranks:
                self.deck.append(f'{rank} of {suit}')

    def shuffle(self):
        random.shuffle(self.deck)

    def deal(self):
        # self.dealt = self.deck.pop()
        return self.deck.pop()

    def __str__(self):
        return f'{self.deck}'


# Hand

class Hand():

    def __init__(self):
        self.cards = []
        self.value = 0
        self.aces = 0

    def add_card(self, card):
        self.cards.append(card)
        self.value += values[card]
        if 'Ace' in card:
            self.aces += 1

    def adjust_aces(self):
        if self.value > 21 and self.aces > 0:
            self.value -= 10
            self.aces -= 1

    def __type__(self):
        return True


# Chips

class Chips():

    def __init__(self):
        self.total = 100
        self.bet = 0

    def win_bet(self):
        self.total += (self.bet * 2)

    def lose_bet(self):
        self.bet = 0

    def push(self):
        self.total += self.bet


# Core game functions

def take_bet(chips):
    print(f"You have {playerchips.total} chips.")
    while True:
        try:
            bet = int(input('Enter your bet: '))
            if bet > playerchips.total:
                print("You don't have enough chips to place that bet!")
                continue
            elif bet <= 0:
                print("Man up and place a fucking bet.")
                continue
            break
        except:
            print('Please enter your bet as a number')
            continue
    chips.bet = bet
    chips.total -= bet


def hit(deck, hand):
    hand.add_card(deck.deal())
    hand.adjust_aces()


def hit_or_stand(deck, hand):
    global playing
    while True:
        x = input("Do you want to hit(1) or stand(2)? ")
        if '1' in x:
            hit(bdeck, playerhand)
            break
        elif '2' in x:
            playing = False
            break
        else:
            print('Please enter 1 or 2')
            continue


def show_some(player, dealer):
    phand = ''
    dhand = ''
    for card in player.cards:
        phand += f'{card}, '
    for card in dealer.cards[1:]:
        dhand += f'{card}, '
    if phand[-2:] == ', ':
        phand = phand[:-2]
    if dhand[-2:] == ', ':
        dhand = dhand[:-2]
    print(Fore.CYAN + f"\n\nYour hand:     {phand}")
    print(Fore.RED + f"Dealer's hand: (Hidden card), {dhand}\n\n" + Fore.MAGENTA)


def show_all(player, dealer):
    phand = ''
    dhand = ''
    for card in player.cards:
        phand += f'{card}, '
    for card in dealer.cards:
        dhand += f'{card}, '
    if phand[-2:] == ', ':
        phand = phand[:-2]
    if dhand[-2:] == ', ':
        dhand = dhand[:-2]
    print(Fore.CYAN + f"\n\nYour hand:     {phand}")
    print(Fore.RED + f"Dealer's hand: {dhand}\n\n" + Fore.MAGENTA)


# End of game scenarios

def player_busts(chips):
    chips.lose_bet()
    print('\nYou busted!\n')
    playing = False


def player_wins(chips):
    chips.win_bet()
    print('\nYou win!\n')
    playing = False


def dealer_busts(chips):
    chips.win_bet()
    print('\nDealer busted!\n')
    playing = False


def dealer_wins(chips):
    chips.lose_bet()
    print('\nDealer won!\n')
    playing = False


def push(chips):
    chips.push()
    print('\nPush. Bets have been returned.\n')
    playing = False


# Game loop

while True:

    # Initialize or restart the game depending on variable states
    try:
        if type(playerhand) == True:
            print('New game starting...')
    except NameError:
        print(Fore.MAGENTA + Back.BLACK + 'Welcome to Blackjack!')
        playerchips = Chips()
    finally:
        playerhand = Hand()
        dealerhand = Hand()
        bdeck = Deck()

    # Shuffle the deck and deal two cards each
    bdeck.shuffle()
    playerhand.add_card(bdeck.deal())
    playerhand.add_card(bdeck.deal())
    dealerhand.add_card(bdeck.deal())
    dealerhand.add_card(bdeck.deal())

    # Prompt the player for their bet
    take_bet(playerchips)

    # Show cards (except the first card in the dealer's hand)
    show_some(playerhand, dealerhand)

    global playing
    playing = True
    dealing = True
    while playing:

        hit_or_stand(bdeck, playerhand)
        show_some(playerhand, dealerhand)

        # If player's hand exceeds 21, run player_busts() and break out of loop
        if playerhand.value > 21:
            dealing = False
            player_busts(playerchips)
            break

    # Play dealer's hand until dealer reaches 17
    while dealing:
        while dealerhand.value < 17:
            hit(bdeck, dealerhand)
            print('Dealer hits.')
            show_all(playerhand, dealerhand)

        # Test against different winning scenarios
        if dealerhand.value > 21:
            dealer_busts(playerchips)
            show_all(playerhand, dealerhand)
        elif dealerhand.value > playerhand.value:
            dealer_wins(playerchips)
            show_all(playerhand, dealerhand)
        elif dealerhand.value == playerhand.value and dealerhand.value >= 17:
            push(playerchips)
            show_all(playerhand, dealerhand)
        elif dealerhand.value < playerhand.value and dealerhand.value >= 17:
            player_wins(playerchips)
            show_all(playerhand, dealerhand)
        break

    # Inform player of their chips
    print(f'Your current chips: {playerchips.total}')

    # Ask to play again
    while True:
        if playerchips.total > 0:
            replay = input('Do you want to play again? Yes or No')
            if replay[0].lower() == 'y':
                playing = True
                break
            elif replay[0].lower() == 'n':
                print('Thanks for playing!')
                break
            else:
                print("Please enter 'yes' or 'no'\n")
                continue
        else:
            input("You're all out of chips, buddy. Fuck off.")
            continue
        break
