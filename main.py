from durak_cli import *
from time import sleep

from pymsgbox.native import confirm
from kivy.config import Config
from kivy.core.window import Window

from kivy.app import App
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.widget import Widget
from kivy.clock import Clock

from kivy.core.image import Image
from kivy.graphics import Rectangle
from kivy.uix.label import Label

from kivy.uix.behaviors import ButtonBehavior

from kivy.properties import DictProperty, NumericProperty


Window.size = (693, 399)
Window.clearcolor = (1, 1, 1, 1)
Config.set('graphics', 'resizable', False)


class DurakAtlas(Widget):
    sprite = DictProperty()
    sheet = Image('spritesheet.png')
    sheet_width, sheet_height = sheet.size

    cw = NumericProperty(sheet_width // len(deck.ranks))
    ch = NumericProperty(sheet_height // (len(deck.suits) + 1))

    def __init__(self, **kwargs):
        super(DurakAtlas, self).__init__(**kwargs)

        texture = self.sheet.texture

        x = y = 0

        self.sprite['service'] = {}
        self.sprite['service']['back'] = texture.get_region(0, 0, self.cw, self.ch)
        self.sprite['service']['button'] = texture.get_region(79, 0, self.cw, self.ch)
        for s in deck.suits:
            self.sprite[s] = {}
            x = 0
            y += self.ch
            for r in deck.ranks:
                self.sprite[s][r] = texture.get_region(x, y, self.cw, self.ch)
                x += self.cw


atlas = DurakAtlas()


class CardSprite(ButtonBehavior, Widget):
    def __init__(self, x, y, card):
        super(CardSprite, self).__init__()

        self.card = card
        self.texture = atlas.sprite[card[1]][card[0]]

        self.pos = x, y
        self.size_hint = (None, None)
        self.size = (atlas.cw, atlas.ch)

        with self.canvas:
            self.sprite = Rectangle(pos=self.pos,
                                    size=self.size,
                                    texture=self.texture)

    def on_press(self):
        if self.card in player.hand:
            try:
                move = player.hand.index(self.card)

                if player.moving:
                    table_ranks = [card[0] for card in deck.table]

                    if not player.throwing:
                        player.throwing = True
                    elif not player.hand[move][0] in table_ranks:
                        raise MoveError('[ERROR] Эту карту нельзя подкинуть ни к одной на столе')

                else:
                    if opponent.move[1] != player.hand[move][1] != deck.trump[1]:
                        raise MoveError('[ERROR] Бьющая карта должна быть той же масти или козырем')
                    if deck.order(player.hand[move]) < deck.order(opponent.move):
                        raise MoveError('[ERROR] Бьющая карта должна быть старше побиваемой')

                player.move = player.hand.pop(move)
                deck.table.append(player.move)

                opponent.make_move()

            except MoveError as ErrorMessage:
                print(ErrorMessage)

        elif self.card == ('button', 'service'):
            try:
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
                opponent.make_move()

            except ValueError:
                print('[ERROR] Вы должны выбрать карту на первом ходе')

        Clock.schedule_once(game.update, 0)


class DurakGame(FloatLayout):
    def update(self, dt):
        player.hand = sorted(player.hand, key=deck.order)
        opponent.hand = sorted(opponent.hand, key=deck.order)

        self.clear_widgets()

        if deck.deck:
            for x in range(0, 3 * (len(deck.deck) // 9 + 1) + 1, 3):
                self.add_widget(CardSprite(x, 138, ('back', 'service')))
            self.add_widget(CardSprite(x + 1, 138, deck.trump))

        self.add_widget(CardSprite(5, 5, ('button', 'service')))

        x = 99
        for card in player.hand:
            self.add_widget(CardSprite(x, 5, card))
            cards_amount = len(player.hand)
            x += 495 // ((cards_amount - 1) if cards_amount >= 4 else 3)

        x = 99
        for card in opponent.hand:
            self.add_widget(CardSprite(x, 271, ('back', 'service')))
            cards_amount = len(opponent.hand)
            x += 495 // ((cards_amount - 1) if cards_amount >= 4 else 3)

        for c in range(len(deck.table)):
            x = (99 if c % 2 == 0 else 114) + (c // 2) * 99
            self.add_widget(CardSprite(x, 138, deck.table[c]), len(deck.table) - c)

        if not player.hand or not opponent.hand:
            Clock.schedule_once(self.over)

    def first_state(self):
        player.hand = sorted(player.hand, key=deck.order)
        opponent.hand = sorted(opponent.hand, key=deck.order)

        self.clear_widgets()

        if deck.deck:
            for x in range(0, 3 * (len(deck.deck) // 9 + 1) + 1, 3):
                self.add_widget(CardSprite(x, 138, ('back', 'service')))
            self.add_widget(CardSprite(x + 1, 138, deck.trump))

        x = 0
        for card in player.hand:
            x += 99
            if card == player.trump:
                self.add_widget(CardSprite(x, 5, card))
            else:
                self.add_widget(CardSprite(x, 5, ('back', 'service')))

        x = 0
        for card in opponent.hand:
            x += 99
            if card == opponent.trump:
                self.add_widget(CardSprite(x, 271, card))
            else:
                self.add_widget(CardSprite(x, 271, ('back', 'service')))

    def over(self, dt):
        if not player.hand and not opponent.hand:
            message = 'Ничья!'
        elif not player.hand:
            message = 'Вы победили!'
        else:
            message = 'Вы проиграли...'
        title = 'Игра окончена'
        buttons = ('Сыграть ещё раз', 'Выйти из игры')

        answer = confirm(message, title, buttons)
        if answer == buttons[0]:
            deck.__init__()
            opponent.__init__()
            player.__init__()
            app.run()
        else:
            app.stop()


game = DurakGame()


class DurakApp(App):
    def build(self):
        self.icon = 'icon.png'

        deck.shuffle()

        for c in range(6):
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

        deck.table = []

        game.first_state()

        if not player.moving:
            opponent.make_move()

        Clock.schedule_once(game.update, 2)
        return game


app = DurakApp()


if __name__ == "__main__":
    app.run()
