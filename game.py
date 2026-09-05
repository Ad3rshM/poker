from termios import tcflush, TCIFLUSH
from sys import stdin, exit


from dealer import Dealer
from player import AI
from hand_checker import HandChecker, HandComparison

class Game:
    def __init__(self, players, clear, Wait):
        self.pot = 0
        self.community_cards = []
        self.checks_in_a_row = 0
        self.finish = False
        self.prev_option = ''
        self.hand_over = False
        self.fold = False
        self.community_cards = []
        self.players = players
        self.wait_between_turns = True
        self.WAIT = Wait
        self.clear = clear
        self.flop_over = False
        self.turn_over = False
        self.river_over = False
    def flop_cards(self):
        self.community_cards = dealer.deal(3)
        for player in self.players:
            player.cards.extend(self.community_cards)
        print(f"The community cards are now: {self.community_cards}")
    
    def turn_cards(self):
        self.community_cards.extend(dealer.deal(1))
        for player in self.players:
            player.cards.append(self.community_cards[-1])
        print(f"The community cards are now: {self.community_cards}")

    def river_cards(self):
        self.community_cards.extend(dealer.deal(1))
        for player in self.players:
            player.cards.append(self.community_cards[-1])
        print(f"The community cards are now: {self.community_cards}")

    def reset_hand(self):
        global dealer
        dealer = Dealer()
        self.hand_over = False
        self.fold = False
        self.pot = 0
        self.flop_over = False
        self.turn_over = False
        self.river_over = False

        for i in self.players:
            i.dealer = dealer
            i.cards = dealer.deal(2)
            i.contribution = 0
            i.ALL_IN = False
            i.prev_move = ''
            if type(i) == AI:
                i.raises = 3

    def deal_next_street(self):
        if not self.flop_over:
            self.flop_cards()
            self.flop_over = True

        elif not self.turn_over:
            self.turn_cards()
            self.turn_over = True

        elif not self.river_over:
            self.river_cards()
            self.river_over = True
            
        else:
            self.hand_over = True
    
    def start_new_round(self):
        for player in self.players:
            player.prev_move = ''
            if type(player) == AI:
                player.raises = 3

    def deal_last_cards(self):
        while len(self.community_cards) < 5:
            card = dealer.deal(1)
            self.community_cards.extend(card)
            for i in self.players:
                i.cards.extend(card)
        self.hand_over = True
    
    def reveal_cards(self):
        self.checks_in_a_row = 0

        self.deal_next_street()
        if self.hand_over:
            return
        self.start_new_round()

    def turn(self, player):
        if not player.ALL_IN:
            if type(player) == AI:
                player.evaluate(self)
            
            print(f'{player.id.upper()} TURN')
            if type(player) != AI:
                print(f"Cards {player.cards}")
                print('\n')

                print(f'Pot: ${self.pot}')
                for i in self.players:
                    print(f"{i.id} wager: ${i.contribution}")
                print(f"Your money: ${player.money}")
                print(f"\n")
            
            option = player.get_action(self)

            if option == 'fold':
                self.fold_option(player)

            elif option == 'raise':
                self.raise_option(player)

            elif option == 'call':
                self.call_option(player)

            elif option == 'check':
                self.checks_in_a_row += 1
            
            if option != 'check':
                self.checks_in_a_row = 0

            if type(player) == AI:
                print(f'{player.id}\'s action was: {option.upper()}')
            
            player.check_ALL_IN()
            if player.ALL_IN:
                print(f'{player.id} has gone ALL IN.')
                self.deal_last_cards()

            if self.checks_in_a_row >= len(self.players):
                self.reveal_cards()

            player.prev_move = option

    def raise_option(self, player):
        amount = player.amount_raised(self)
        if player.contribution < player.opponent.contribution:
            self.call_option(player)
        if not player.ALL_IN:
            self.pot += amount
            player.contribution += amount
            player.money -= amount

    def fold_option(self, player):
        player.opponent.money += self.pot
        self.pot = 0
        self.fold = True

    def call_option(self, player):
        change = player.opponent.contribution - player.contribution
        if change > player.money:
            player.ALL_IN = True
            change = player.money
        self.pot += change
        player.contribution += change
        player.money -= change

    def play_hand(self, ui):
        for player in self.players:
            if type(player) == AI:
                self.wait_between_turns = False

        while not self.hand_over and not self.fold:
            for player in self.players:
                self.WAIT(self)
                self.clear()
                self.turn(player)
                if self.hand_over or self.fold:
                    break
                ui.enter()

        for j in self.players:
            j.original = [i for i in j.cards if i not in self.community_cards]
        
        if self.hand_over:
            self.compare_hands()

        print('\n')
        for player in self.players:
            print(f"{player.id} Hand: {player.original}")
        print('\n')

        for player in self.players:
            print(f"{player.id} Final Money: {player.money}")
            print('\n')
        best_player = max(self.players, key=lambda player: player.money)
        print(f"{best_player.id} Wins!")

        ui.play_again(self.players)

    def compare_hands(self):
        comparer = HandComparison()
        checker = HandChecker()

        win_hands = comparer.compare_hands([i.cards for i in self.players])
        winners = [i for i in self.players if checker.hand_checker(i.cards) == win_hands]

        individual = self.pot / len(winners)
            
        for i in winners:
            print(f'{i.id} wins!')
            i.money += individual
            self.pot -= individual