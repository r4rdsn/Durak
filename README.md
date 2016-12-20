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


# Demonstration
<details> 
  <summary>recorded animation</summary>
   ![gameplay animation](gameplay.gif)
</details>


# Dependencies
[python](https://python.org/) - for everything  
[kivy](https://github.com/kivy/kivy) - for GUI  
[pymsgbox](https://github.com/asweigart/PyMsgBox) - for message box that appears as a game over


# Installation guide
* clone this repository:  
```git clone https://github.com/r4rdsn/Durak/```  
* install kivy:  
```pip install kivy```
* follow downloaded folder:  
```cd Durak``` 
* install package:  
```python setup.py install```  

after the end of installation you can run the game itself in different versions.  
to run GUI-version:  
```python -m game```  
to run CLI-version:  
```python -m game.cli```


# The Goal
to learn the basics of:

1. implementing AI
2. building GUI
3. game-development


# TODO-list
* improve AI's method (_make_move()_)
* place trump card under the deck 90 degrees rotated
* draw discard pile on the screen
* translate game into English
* refactor the code
* provide listing with comments and documentation
