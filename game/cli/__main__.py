from .. import *

import os


def clearscreen():
    os.system('cls' if os.name == 'nt' else 'clear')


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
    print(cliLocal.players_lowest_trump, ''.join(player.trump))
else:
    print(cliLocal.opponents_lowest_trump)
if opponent.trump:
    print(cliLocal.player_no_trumps, ''.join(opponent.trump))
else:
    print(cliLocal.opponent_no_trumps)

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
    print(cliLocal.player_moving_first)
else:
    print(cliLocal.opponent_moving_first)

print()

deck.table = []

while True:
    if not player.moving or deck.table:
        opponent.make_move()

    deck.show()
    player.show()

    if player.moving and player.throwing:
        print(cliLocal.player_threw, ''.join(player.move))
        if opponent.move:
            print(cliLocal.opponent_defended, ''.join(opponent.move))
        else:
            print(cliLocal.opponent_resigned)

    elif not player.moving:
        if len(deck.table) > 1:
            print(cliLocal.player_defended, ''.join(player.move))
        print(cliLocal.opponent_threw, ''.join(opponent.move))

    if not player.hand or not opponent.hand:
        if not player.hand and not opponent.hand:
            print(result.draw)
        elif not player.hand:
            print(result.victory)
        else:
            print(result.loss)
        break

    while True:
        move = input(cliLocal.ask_move)

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
                        raise MoveError(warning.throw)

                else:
                    if opponent.move[1] != player.hand[move][1] != deck.trump[1]:
                        raise MoveError(warning.beat_suit)
                    if deck.order(player.hand[move]) < deck.order(opponent.move):
                        raise MoveError(warning.beat_rank)

                player.move = player.hand.pop(move)
                deck.table.append(player.move)

                break

        except (TypeError, ValueError, IndexError):
            print(waning.move_format + '\n')
        except MoveError as ErrorMessage:
            print(ErrorMessage + '\n')

    clearscreen()
