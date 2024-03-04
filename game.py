import random

suits = {
    1:'2660',
    2:'2661',
    3:'2662',
    4:'2663'
}

card_face = {
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

def get_suit(index):
    unicode_str = suits.get(index)
    new_str = chr(int(unicode_str,16))
    return new_str

def print_card(selected_card):
    print(card_face.get(selected_card[0]),get_suit(selected_card[1]))

base_deck = {}
playing_deck = []

card_position = 1
suit = 1
drawn = False

for card in range (52):
    new_id = card + 1
    playing_deck.append(new_id)
    base_deck.update({new_id:[card_position, suit, drawn]})
    card_position += 1
    if card_position == 14:
        card_position = 1
        suit += 1
print(f'base: {len(base_deck)}')

for card_id, card in base_deck.items():
    print_card(card)

random.shuffle(playing_deck)

print(f'shuffled: {len(playing_deck)}')

for card_id in playing_deck:
    current_card = base_deck.get(card_id)
    print_card(current_card)