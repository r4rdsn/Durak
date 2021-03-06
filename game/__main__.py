from . import *

from pymsgbox.native import confirm
from kivy.config import Config
from kivy.core.window import Window

from kivy.app import App
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.widget import Widget
from kivy.clock import Clock

from kivy.core.image import Image
from kivy.graphics import Rectangle, Rotate

from kivy.uix.behaviors import ButtonBehavior

from kivy.properties import DictProperty, NumericProperty


Window.size = (738, 399)
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
    def __init__(self, x, y, card, angle=0):
        super(CardSprite, self).__init__()

        self.card = card
        self.texture = atlas.sprite[card[1]][card[0]]

        self.pos = x, y
        self.size_hint = (None, None)
        self.size = (atlas.cw, atlas.ch)
        self.angle = angle

        with self.canvas:
            Rotate(angle=self.angle,
                   origin=self.center)

            self.sprite = Rectangle(pos=self.pos,
                                    size=self.size,
                                    texture=self.texture)

            Rotate(angle=-self.angle,
                   origin=self.center)

    def on_press(self):
        if self.card in player.hand:
            try:
                move = player.hand.index(self.card)

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

                if deck.deck or (player.hand or len(opponent.hand) == 1) and len(deck.table) <= 12:
                    opponent.make_move()

            except MoveError as ErrorMessage:
                logger.warning_message(ErrorMessage)

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
                logger.warning_message(warning.first_move)

        Clock.schedule_once(game.update, 0)


class DurakGame(FloatLayout):
    def update(self, dt):
        player.hand = sorted(player.hand, key=deck.order)
        opponent.hand = sorted(opponent.hand, key=deck.order)

        self.clear_widgets()

        self.add_widget(CardSprite(32, 5, ('button', 'service')))

        x = 144
        for card in player.hand:
            self.add_widget(CardSprite(x, 5, card))
            cards_amount = len(player.hand)
            x += 495 // ((cards_amount - 1) if cards_amount >= 4 else 3)

        x = 144
        for card in opponent.hand:
            self.add_widget(CardSprite(x, 271, ('back', 'service')))
            cards_amount = len(opponent.hand)
            x += 495 // ((cards_amount - 1) if cards_amount >= 4 else 3)

        for c in range(len(deck.table)):
            x = ((99 if c % 2 == 0 else 114) + (c // 2) * 99) + 45
            self.add_widget(CardSprite(x, 138, deck.table[c]), len(deck.table) - c)

        if deck.deck:
            if len(deck.deck) > 1:
                first_card = deck.last_card - 3 * (len(deck.deck) // 9 + 1)
                for x in range(first_card, deck.last_card, 3):
                    self.add_widget(CardSprite(x, 138, ('back', 'service')), x)
            self.add_widget(CardSprite(33, 138, deck.trump, 90), x + 1)

        if len(deck.table) == 12:
            player.fill_hand()
            opponent.fill_hand()
            deck.table = []

            Clock.schedule_once(self.update, 1)

        if not deck.deck and \
           ((not opponent.hand and len(player.hand) > 1) or (not player.hand and len(opponent.hand) > 1) or (not player.hand and not opponent.hand)):

            Clock.schedule_once(self.over)

    def first_state(self):
        player.hand = sorted(player.hand, key=deck.order)
        opponent.hand = sorted(opponent.hand, key=deck.order)

        self.clear_widgets()

        x = 45
        for card in player.hand:
            x += 99
            if card == player.trump:
                self.add_widget(CardSprite(x, 5, card))
            else:
                self.add_widget(CardSprite(x, 5, ('back', 'service')))

        x = 45
        for card in opponent.hand:
            x += 99
            if card == opponent.trump:
                self.add_widget(CardSprite(x, 271, card))
            else:
                self.add_widget(CardSprite(x, 271, ('back', 'service')))

        if deck.deck:
            if len(deck.deck) > 1:
                first_card = deck.last_card - 3 * (len(deck.deck) // 9 + 1)
                for x in range(first_card, deck.last_card, 3):
                    self.add_widget(CardSprite(x, 138, ('back', 'service')), x)
            self.add_widget(CardSprite(33, 138, deck.trump, 90), x + 1)

    def over(self, dt):
        if not player.hand and not opponent.hand:
            message = result.draw
        elif not player.hand:
            message = result.victory
        else:
            message = result.loss
        title = result.game_over
        buttons = (result.play_again_btn, result.quit_game_btn)

        answer = confirm(message, title, buttons)
        app.stop()

        if answer == buttons[0]:
            deck.__init__()
            opponent.__init__()
            player.__init__()
            app.run()


game = DurakGame()


class DurakApp(App):
    def build(self):
        self.icon = 'icon.png'

        deck.shuffle()

        for c in range(6):
            player.take_card()
            opponent.take_card()

        deck.last_card = 5 + 3 * (len(deck.deck) // 9 + 1)

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
