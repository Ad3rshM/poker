from hand_checker import HandChecker
from dealer import Dealer

def is_consecutive(lst):
    if not lst:
        return True
    return any(lst[i] + 1 == lst[i+1] for i in range(len(lst) - 1))

class Player:
    def __init__(self, dealer, name):
        self.prev_move = ''

        self.id = name
        self.dealer = dealer

        self.money = 2000
        self.cards = self.dealer.deal(2)

        self.contribution = 0
        self.ALL_IN = False
        self.prev_option = ''
    def get_action(self, game):
        self.options = ['fold', 'raise', 'check']
        query = ''

        if self.contribution < self.opponent.contribution:
            self.options.remove('check')
            self.options.append('call')

        for i in self.options:
            if i == self.options[-1]:
                query += 'or ' + i.capitalize()
            else:
                query += i.capitalize() + ', '
        query += ': '

        option = input(query).strip().lower()

        while option not in self.options:
            option = input(query).strip().lower()

        return option

    def amount_raised(self, game):
        amount = input('Amount: ').strip()
        while True:
            try:
                while int(amount) <= 0:
                    print("Enter a positive integer")
                    amount = input('Amount: ').strip()
                while int(amount) > self.money:
                    print("You do not have that much money.")
                    amount = input('Amount: ').strip()
                return int(amount)
            except:
                amount = input('Amount: ').strip()
    
    def check_ALL_IN(self):
        if self.money == 0:
            self.ALL_IN = True
        else:
            self.ALL_IN = False


class AI(Player):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.score = 0
        self.check_denied = True
        self.raises = 3
        self.money = 2000
    def get_action(self, game):
        self.call_amount = self.opponent.contribution - self.contribution
        self.ratio = (2000 - self.money) / (self.money)
        if game.pot != 0:
            equity = self.contribution + self.call_amount / (game.pot + self.call_amount)
        else:
            equity = 0

        raise_bool = self.raises > 0 and self.ratio < (self.score / 2) and self.score > equity + 0.2
        check_bool = self.opponent.prev_move != 'raise'

        if check_bool:
            if raise_bool:
                self.raises -= 1
                return 'raise'
            return 'check'
        
        if equity > self.score:
            return 'fold'
        if raise_bool:
            self.raises -= 1
            return 'raise'
        return 'call'
    
    def amount_raised(self, game):
        if self.score >= 0.9:
            if game.pot // 2 < self.money:
                return game.pot // 2
        if self.score >= 0.8:
            if game.pot // 4 < self.money:
                return max(game.pot // 4, int(self.score * 50))
        else:
            if game.pot // 8 < self.money:
                return max(game.pot // 8, int(self.score * 20))
        return self.money
    
    def evaluate(self, game):
        self.score = 0
        for _ in range(1000):
            checker = HandChecker()
            simul_dealer = Dealer()

            cards_left = 7 - len(game.community_cards) - len(self.cards)
            new_deck = [i for i in simul_dealer.deck if i not in self.cards and i not in game.community_cards]
            simul_dealer.deck = new_deck

            opponent_cards = simul_dealer.deal(2)
            last_cards = simul_dealer.deal(cards_left)

            all_cards = [*game.community_cards, *last_cards]
            
            our_hand = checker.hand_checker([*all_cards, *self.cards])
            their_hand = checker.hand_checker([*all_cards, *opponent_cards])

            if our_hand > their_hand:
                self.score += 1
            elif their_hand == our_hand:
                self.score += 0.5
            
        self.score /= 1000