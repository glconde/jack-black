"""
This is a simple game of Black Jack.
The objective is to draw upto five(5) cards and get to or closer to 21 without getting over.
The player is given 100 funds (default setting) to play and each match will cost 50. Which means you get +50 to your funds if you win, -50 if you lose.
The game ends if you have zero(0) funds or you chose to quit.

Please view README file for more details on rules and default settings.

George Conde 2024  
"""

import random
from typing import Final

SUITS:Final = {
    1:'2660',
    2:'2661',
    3:'2662',
    4:'2663'
}

CARD_FACE:Final = {
    1:'A',
    2:'2',
    3:'3',
    4:'4',
    5:'5',
    6:'6',
    7:'7',
    8:'8',
    9:'9',
    10:'10',
    11:'J',
    12:'Q',
    13:'K'
}

VALID_MOVES:Final = ['S','H','F']
YES_NO_RESPONSE:Final = ['Y','N']

MAX_HAND = 5
AI_SAFETY = 17

#get the card symbol or suit
def get_suit(index):
    unicode_str = SUITS.get(index)
    new_str = chr(int(unicode_str,16))
    return new_str

#print the selcted card with it's face and suit
def print_card(selected_card):
    print(CARD_FACE.get(selected_card[0]),get_suit(selected_card[1]))

#draw a card from the existing deck
def draw_card(player, current_deck, used_cards):
    dealt_card = current_deck.pop()
    player.append(dealt_card)
    used_cards.append(dealt_card)

#print the hand of the player
def print_hand(hand, player_name):
    print(f'{player_name} has:')
    for card_id in hand:
        current_card = base_deck.get(card_id)
        print_card(current_card)

#check if the hand has aces
def check_for_acess(hand):
    found = False
    for card_id in hand: 
        current_card = base_deck.get(card_id)
        if CARD_FACE.get(current_card[0]) == 'A':
            return found

#print the table to refresh the view        
def print_table(player,dealer,):
    print_hand(dealer, 'dealer')
    dealer_total = calculate_hand_values(dealer)
    print(f'dealer total {dealer_total}')
    print_hand(player, 'player')
    player_total = calculate_hand_values(player)
    print(f'player total {player_total}')
    print('-'*20)

#calculate total points on a hand
def calculate_hand_values(hand):
    total = 0
    ace_count = 0
    for card_id in hand:
        current_card = base_deck.get(card_id)
        if 1 < current_card[0] < 10:
            total += current_card[0]
        elif current_card[0] <= 13:
            total += 10
        else:
            ace_count += 1
    #Ace special rule
    while ace_count > 0:
        if (total + 11) > 21:
            total += 1
        else:
            total += 11
        ace_count -= 1
    
    if total > 21:
        #bust 
        total = 0
    
    return total

#this is a simple ai that decides when the dealer needs to draw
def move_AI(hand,deck,used):
    score = calculate_hand_values(hand)

    if len(hand) < 5:
        if score < 21:
            if score < AI_SAFETY:
                #dealer risks it
                draw_card(hand, deck, used)
            else:
                #dealer stands
                return False
        elif score >= 21:
            #dealer bust or 21, so dealer stands (stop drawing)
            return False
        else:
            return True
    else:
        return False

#prints available funds
def print_funds(wallet):
    print(f'remaining funds [{wallet}]')


base_deck = {}
playing_deck = []

card_position = 1
suit = 1
drawn = False

#initialize deck
for card in range (52):
    new_id = card + 1
    playing_deck.append(new_id)
    base_deck.update({new_id:[card_position, suit]})
    card_position += 1
    if card_position == 14:
        card_position = 1
        suit += 1

#default funds. change this to a multiple of 50.
player_funds = 100
keep_playing = True

#main game loop, keeps on going while player has money and decides to keep playing
while player_funds > 0 and keep_playing:
    print_funds(player_funds)

    random.shuffle(playing_deck)

    game_is_on = True

    dealer_hand = []
    player_hand = []
    drawn = []
    move = ''
    available_ai_moves = MAX_HAND

    #loop for a single match
    while game_is_on:

        #initial draw of 2 cards
        if len(player_hand) == 0:
            draw_card(player_hand, playing_deck, drawn)
            draw_card(player_hand, playing_deck, drawn)
            draw_card(dealer_hand, playing_deck, drawn)
            draw_card(dealer_hand, playing_deck, drawn)
            #print(drawn)
            print_table(player_hand, dealer_hand)
            if calculate_hand_values(dealer_hand) == 21:
                game_is_on = False
                print('dealer black jack. you lose.')
                break
        else:
            if move == 'H':
                #hit - draw upto 5 cards and get closer to 21 pts without going over.
                draw_card(player_hand, playing_deck,drawn)
                print_table(player_hand, dealer_hand)
                if calculate_hand_values(player_hand) == 0:
                    print('bust. you lose.')
                    game_is_on = False
            elif move == 'S':
                #stand - stop drawing and let AI move
                if calculate_hand_values(player_hand) == 0:
                    print('bust. you lose.')
                else:
                    #dealer AI here -->
                    dealer_needs_to_move = True
                    while dealer_needs_to_move:
                        dealer_needs_to_move = move_AI(dealer_hand, playing_deck,drawn)
                        print('dealer moves...')
                        print_table(player_hand, dealer_hand)
                #game ends either way
                game_is_on = False
                    
            elif move == 'F':
                #forfeit - lose the match
                print('forfeit. you lose.')
                game_is_on = False

        #verify user response, s = stand or stop drawing, h = draw a card, f = automatically lose the match.
        while True and game_is_on:
            move = input('Your move? [S]tand, [H]it, [F]orfeit > ').capitalize()
            if move in VALID_MOVES:
                break
            elif len(move) > 1:
                print('input has exceeded length. please limit response to [S/H/F]')
            elif not move.isalpha:
                print('input is not a letter from the selection [S/H/F]')
            else:
                print('unrecognized response. valid options are [S/H/F]')

    #game has ended compare scores
    player_score = calculate_hand_values(player_hand)
    dealer_score = calculate_hand_values(dealer_hand)

    win = False
    if move == 'F':
        win = False
    elif player_score > dealer_score:
        win = True
    elif player_score == dealer_score:
        #dealer black jack, auto lose
        if check_for_acess(dealer_hand):
            win = False
        #player black jack
        elif check_for_acess(player_hand):
            win = True
        #house always wins a tie
        else:
            win = False
    else:
        win = False

    if win:
        print('player wins.')
        player_funds += 50
    else:
        print('house wins.')
        player_funds -= 50

    #check if the user still wants to play. replying Y will start a new match
    while True and player_funds > 0:
        stay = input(f'Continue (remaining funds {player_funds})? [Y/N]').capitalize()
        if stay in YES_NO_RESPONSE:
            break
        elif len(quit) > 1:
            print('input has exceeded length. please limit response to [Y/N]')
        elif not stay.isalpha:
            print('input is not a letter from the selection [Y/N]')
        else:
            print('unrecognized response. valid options are [Y/N]')
    
    keep_playing = (stay == 'Y') or (player_funds <= 0)

    #some post game features to add here -->