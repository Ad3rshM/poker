
from itertools import cycle

from player import Player, AI
from hand_checker import HandChecker, HandComparison
from dealer import Dealer
from game import Game
from ui import UI

dealer = Dealer()

checker = HandChecker()
comparer = HandComparison()

ui = UI()

ui.clear()
ui.show_title()
ui.enter()

player1 = Player(dealer, "PLAYER 1")
game_type = input("One Player or Two Player (1/2): ")
while game_type != '1' and game_type != "2":
    print('Enter "1" or "2"')
    game_type = input("One Player or Two Player (1/2): ")
if game_type == '1':
    player2 = AI(dealer, "PLAYER 2")
else:
    player2 = Player(dealer, "PLAYER 2")

players = [player1, player2]
player_cycle = cycle(players)
new = next(player_cycle)
for player in players:
    new = next(player_cycle)
    player.opponent = new

game = Game(players, ui.clear, ui.wait)

if __name__ == '__main__':
    while player1.money > 0 and player2.money > 0:
        game.reset_hand()
        game.play_hand(ui)