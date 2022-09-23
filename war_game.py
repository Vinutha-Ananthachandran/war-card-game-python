suit_list = ('spade','hearts','diamonds','clubs')
rank_list = ('ace','two','three','four','five','six','seven','eight','nine','ten','jack','king','queen')
value = {'ace':14,'two':2,'three':3,'four':4,'five':5,'six':6,'seven':7,'eight':8,'nine':9,'ten':10,'jack':11,'king':12,'queen':13}

from random import shuffle

class Card():
    '''
    card class
    '''
    def __init__(self,suit,rank):
        '''
        initiates a card
        '''
        self.suit = suit.lower()
        self.rank = rank.lower()
        self.value = value[self.rank]

    def __str__(self):
        '''
        prints the card details
        '''
        return self.rank+' of '+self.suit

class Deck():
    '''
    deck class
    '''
    def __init__(self):
        self.card_deck = []
        for suit in suit_list:
            for rank in rank_list:
                self.card_deck.append(Card(suit,rank))

    def print_deck(self):
        print(list(map(lambda card: str(card),self.card_deck)))

    def shuffle_deck(self):
        shuffle(self.card_deck)

    def deal_player_set(self,player_id):
        if player_id == 1:
            return self.card_deck[0:26]
        elif player_id == 2:
            return self.card_deck[26::]

class Player():
    '''
    player class
    '''

    def __init__(self,player_id,deck_obj):
        self.player_id = player_id
        self.player_deck = deck_obj.deal_player_set(self.player_id)

    def deal_card(self):
        return self.player_deck.pop(0)

    def deal_card_set(self,count):
        if count != 0:
            card_set = []
            for i in range(0,count):
                card_set.append(self.player_deck.pop(0))
            return card_set

    def add_new_card(self,card):
        if type(card) == type([]):
            self.player_deck.extend(card)
        else:
            self.player_deck.append(card)

    def __str__(self):
        return f'Player {self.player_id} = {len(self.player_deck)}'

    def __len__(self):
        return len(self.player_deck)

class Game():
    '''
    game logic
    '''
    def __init__(self):
        self.player = {}
        game_deck = Deck()
        game_deck.shuffle_deck()
        for i in range(1,3):
            self.player[i] = Player(i,game_deck)

    def start_game(self):
        while True:
            if len(self.player[1]) == 0 or len(self.player[2]) == 0:
                print(f'{self.player[1]} and {self.player[2]}')
                break
            else:
                card1 = self.player[1].deal_card()
                card2 = self.player[2].deal_card()
                result = self.challenge(card1,card2)
                if result == None:
                    self.war(card1,card2)
                else:
                    self.winning_hand(result,card1,card2)
                    del card1
                    del card2

    def challenge(self,card1,card2):
        print(f'Player 1 = {card1.value} v/s Player 2 = {card2.value}')
        if card1.value < card2.value:
            return 2
        elif card1.value > card2.value:
            return 1
        else:
            return None

    def winning_hand(self,player_id,card1,card2,card_set=[]):
        self.player[player_id].add_new_card(card1)
        self.player[player_id].add_new_card(card2)
        if len(card_set) > 0:
            self.player[player_id].add_new_card(card_set)

    def war(self,card1,card2):
        war_set = []
        while True:
            war_set.append(card1)
            war_set.append(card2)
            count = min(len(self.player[1]),len(self.player[2]))
            if count <= 1:
                rem = 0
            elif count > 2:
                rem = 2
            else:
                rem = 1
            war_set.extend(self.player[1].deal_card_set(rem))
            war_set.extend(self.player[2].deal_card_set(rem))
            war_card1 = self.player[1].deal_card()
            war_card2 = self.player[2].deal_card()
            war_result = self.challenge(war_card1,war_card2)
            if war_result == None:
                del card1
                del card2
                card1 = war_card1
                card2 = war_card2
            else:
                self.winning_hand(war_result,war_card1,war_card2,war_set)
                break

if __name__ == "__main__":
	new_game = Game()
	new_game.start_game()
