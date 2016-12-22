import random


class Deck:
    def __init__(self):
        self.ranks = ['6', '7', '8', '9', '10', 'J', 'Q', 'K', 'A']
        self.suits = ['S', 'H', 'D', 'C']

        self.deck = [(rank, suit) for rank in self.ranks for suit in self.suits]

    def shuffle(self):
        random.shuffle(self.deck)

    def take(self):
        return self.deck.pop(0)

    def show(self):
        if self.deck:
            print('[' + deck.trump[1] + ']' * (len(self.deck) // 9 + 1), end=' ' if self.table else '\n')
        if self.table:
            print(''.join(['[' + c[0] + c[1] for c in self.table]) + ']')

    def order(self, card):
        return (self.suits.index(card[1]), self.ranks.index(card[0]))


class Player:
    def __init__(self):
        self.hand = []
        self.move = None
        self.throwing = False

    def take_card(self):
        global deck
        self.hand.append(deck.take())

    def fill_hand(self):
        global deck
        self.throwing = False
        while deck.deck and len(self.hand) < 6:
            self.take_card()


class Computer(Player):
    def make_move(self):
        self.without_trumps = list(filter(lambda c: c[1] != deck.trump[1], self.hand))

        def mincard(seq):
            def st(element):
                if player.moving:
                    if (element[1] == player.move[1] and deck.ranks.index(element[0]) > deck.ranks.index(player.move[0])) \
                       or element[1] == deck.trump[1] != player.move[1]:
                        return True
                else:
                    if not deck.table or element[0] in [c[0] for c in deck.table]:
                        return True
                return False
                return True

            minimum = None
            for element in seq:
                if st(element) and (minimum is None or deck.ranks.index(element[0]) < deck.ranks.index(minimum[0])):
                    minimum = element
            return minimum

        apt = mincard(self.without_trumps)
        if apt is None:

            if len(deck.deck) <= (9 + random.randint(0, 3)) or \
               (player.moving and len(self.without_trumps) < 3) or \
               (not player.moving and not deck.table):

                apt = mincard(self.hand)

        if apt is not None:
            self.move = apt

            self.hand.remove(self.move)
            deck.table.append(self.move)

        else:
            if player.moving:
                self.hand += deck.table
                deck.table = []

                player.fill_hand()
            else:
                deck.table = []
                player.moving = True

                opponent.fill_hand()
                player.fill_hand()


class User(Player):
    def show(self):
        self.hand = sorted(self.hand, key=deck.order)
        print('Рука:', ' '.join([c[0] + c[1] for c in self.hand]))


class MoveError(Exception):
    pass


deck = Deck()
opponent = Computer()
player = User()
