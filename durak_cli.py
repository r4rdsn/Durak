import random
import os
from hashlib import md5


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
                    if element[1] == player.move[1] and deck.ranks.index(element[0]) > deck.ranks.index(player.move[0]):
                        #if element[1] != deck.trump[1] or len(self.without_trumps) < 3 or len(deck.deck) < (9 + random.randint(0, 3)):
                        return True
                else:
                    if not deck.table or element[0] in [c[0] for c in deck.table]:
                        #if element[1] != deck.trump[1] or len(self.without_trumps) < 3 or len(deck.deck) > (9 + random.randint(0, 3)):
                        return True
                return False

            minimum = None
            for element in seq:
                if st(element) and (minimum is None or deck.ranks.index(element[0]) < deck.ranks.index(minimum[0])):
                    minimum = element
            return minimum

        apt = mincard(self.without_trumps)
        if apt is None:
            apt = mincard(self.hand)

        if apt is not None:
            self.move = apt
            self.hand.remove(self.move)
            deck.table.append(self.move)
        elif player.moving:
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


if __name__ == "__main__":
    def clearscreen():
        os.system('cls' if os.name == 'nt' else 'clear')

    cheat_code = '237975ee340d9560cd0af3f8382df77a'

    deck.shuffle()

    for _ in range(6):
        player.take_card()
        opponent.take_card()

    deck.trump = deck.take()
    deck.deck.append(deck.trump)
    deck.suits.remove(deck.trump[1])
    deck.suits.append(deck.trump[1])

    player.trump = None
    opponent.trump = None

    for c in range(6):
        if player.hand[c][1] == deck.trump[1]:
            if not player.trump or deck.order(player.hand[c]) < deck.order(player.trump):
                player.trump = player.hand[c]

        if opponent.hand[c][1] == deck.trump[1]:
            if not opponent.trump or deck.order(opponent.hand[c]) < deck.order(opponent.trump):
                opponent.trump = opponent.hand[c]

    clearscreen()

    if player.trump:
        print('Ваша наименьшая козырная карта:', ''.join(player.trump))
    else:
        print('У вас в руке нет козырных карт.')
    if opponent.trump:
        print('Минимальный козырь у оппонента:', ''.join(opponent.trump))
    else:
        print('У вашего оппонента нет козырей.')

    if player.trump and opponent.trump:
        if deck.order(player.trump) < deck.order(opponent.trump):
            player.moving = True
        else:
            player.moving = False
    elif player.trump:
        player.moving = True
    elif opponent.trump:
        player.moving = False
    else:
        player.moving = random.randint(0, 1)

    if player.moving:
        print('Вы ходите первым.')
    else:
        print('Оппонент ходит первым.')

    print()

    deck.table = []

    while True:
        if not player.moving or deck.table:
            opponent.make_move()

        deck.show()
        player.show()

        if player.moving and player.throwing:
            print('Вы подкинули на стол', ''.join(player.move))
            if opponent.move:
                print('Оппонент отбился картой', ''.join(opponent.move))
            else:
                print('Оппонент взял карты.')

        elif not player.moving:
            if len(deck.table) > 1:
                print('Вы отбились картой', ''.join(player.move))
            print('Оппонент подкинул на стол', ''.join(opponent.move))

        if not player.hand or not opponent.hand:
            if not player.hand and not opponent.hand:
                print('Ничья!')
            elif not player.hand:
                print('Вы победили!')
            else:
                print('Вы проиграли...')
            break

        while True:
            move = input('Введите ваш игровой ход: ')

            if md5(move.encode()).hexdigest() == cheat_code:
                print(opponent.hand)

            try:
                if not move:
                    if player.moving:
                        if not player.throwing:
                            raise ValueError

                        player.moving = False
                        player.throwing = False

                        player.fill_hand()
                        opponent.fill_hand()

                    elif not player.moving:
                        player.hand += deck.table

                        opponent.fill_hand()
                        player.fill_hand()

                    deck.table = []
                    break

                else:
                    move = int(move) - 1

                    if player.moving:
                        table_ranks = [card[0] for card in deck.table]

                        if not player.throwing:
                            player.throwing = True
                        elif not player.hand[move][0] in table_ranks:
                            raise MoveError('Эту карту нельзя подкинуть ни к одной на столе.\n')

                    else:
                        if opponent.move[1] != player.hand[move][1] != deck.trump[1]:
                            raise MoveError('Бьющая карта должна быть той же масти или козырем.\n')
                        if deck.order(player.hand[move]) < deck.order(opponent.move):
                            raise MoveError('Бьющая карта должна быть старше побиваемой.\n')

                    player.move = player.hand.pop(move)
                    deck.table.append(player.move)

                    break

            except (TypeError, ValueError, IndexError):
                print('Ход должен содержать номер карты в вашей руке.\n')
            except MoveError as ErrorMessage:
                print(ErrorMessage)

        clearscreen()
