from .. import *

import os
from hashlib import md5


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
