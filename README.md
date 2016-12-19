# Rules
Durak (Дурак, translated as Fool) is a popular Russian card game.  
the following list contains classic real-life rules of it's basic variant - Podkidnoy (Подкидной, translated as Throw-in) Durak.

* Durak is played with 36-card deck, from 6s to aces
* the number of players varies from 2 to 5
* the goal of the game is to get rid of all cards, the last player with cards in their hands is a Fool
* each players gets 6 card from shuffled deck
* the next card after drawing is laid open on the table and it's suit is a trump of this game
* player that has the lowest trump is moving first
* 6 is the lowest rank, ace is the highest, trump beats every non-trump card
* the clockwise nearest player from moving player is a defender, the rest, including the moving player, are attackers  
* the moving can either put only one card on the table or throw multiple cards if all of them has the same rank
* defender should either beat every card on the table or take all cards to their hand
* while defender doesn't take cards, attackers can throw cards that has the same rank as any of cards on the table
* if attackers don't throw any cards, all cards on the table are placed in the discard pile and the successful defender becomes the moving player
* if defender picks up cards on the table, he loses their turn to attack, so the next moving player is the clockwise nearest to them


# The Goal
learn the basics of:

1. implementing AI
2. building GUI
3. game-development


# Dependencies
[python](python.org/) - for everything  
[kivy](github.com/kivy/kivy) - for GUI  
[pymsgbox](github.com/asweigart/PyMsgBox) - for message box that appears as a game over


# Definitions
**durak_cli.py** - console-version of Podkidnoy Durak with two players, one of which is AI (also contains classes required for game)  
**main.py** - graphical-version of Durak based on kivy library  
**spritesheet.png** - image which contains required sprites for GUI  
**icon.png** - window's icon found with [google](google.com)


# TODO-list
* improve AI's method (_make_move()_)
* place trump card under the deck 90 degrees rotated
* draw discard pile on the screen
* translate game into English
* refactor the code
* provide listing with comments and documentation