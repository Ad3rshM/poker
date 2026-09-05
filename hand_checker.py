from copy import deepcopy
from collections import Counter

from dealer import switch

class HandChecker:
    def __init__(self):
        self.highcards = []
        self.hand = 0

    def four(self):
        self.handcards = []
        if (4 in self.lstvals):
            for i in self.freq.keys():
                if self.freq[i] == 4:
                    self.handcards.append(switch[i])
            return True
        else:
            return False


    def three(self):
        self.handcards = []
        if (3 in self.lstvals):
            for i in self.freq.keys():
                if self.freq[i] == 3:
                    self.handcards.append(switch[i])
            return True
        else:
            return False
        

    def two(self):
        self.handcards = []

        if (2 in self.lstvals):
            for i in self.freq.keys():
                if self.freq[i] == 2:
                    self.handcards.append(switch[i])
            return True
        else:
            return False
        

    def twopair(self):
        self.handcards = []

        if (self.lstvals.count(2) == 2):
            for i in self.freq.keys():
                if self.freq[i] == 2:
                    self.handcards.append(switch[i])
            self.handcards.sort(reverse=True)
            return True
        else:
            return False
        

    def flush(self):
        self.handcards = []

        suit_freq = Counter(i[0] for i in self.cards)
        for suit, count in suit_freq.items():
            if count >= 5:
                self.handcards = [switch[card[1]] for card in self.cards if card[0] == suit]
                if 14 in self.handcards and {2,3,4,5}.issubset(set(self.handcards)):
                    self.handcards.append(1)
                self.handcards.sort(reverse=True)
                return True
        return False
    

    def straight(self):
        self.handcards = []
        set_check = sorted(set(self.check))

        if 14 in set_check and {2, 3, 4, 5}.issubset(set_check):
            set_check.append(1)
            set_check = sorted(set(set_check))

        if len(set_check) >= 5:
            for i in range(len(set_check) - 4):
                window = set_check[i:i+5]
                if window == list(range(window[0], window[0] + 5)):
                    self.handcards = [window[-1]]
                    return True                
        return False
    
    def straight_flush(self):
        self.handcards = []
        if self.flush() and self.straight():
            self.flush()
            suited = self.handcards
            for i in range(len(suited) - 4):
                window = sorted(suited)[i:i+5]
                if window == list(range(sorted(suited)[i], sorted(suited)[i] + 5)):
                    self.handcards = [window[-1]]
                    return True
        return False
    
    def fullhouse(self):
        self.handcards = []

        two = []
        three = []

        for index, value in self.freq.items():
            if value >= 3:
                three.append(switch[index])
            elif value >= 2:
                two.append(switch[index])
        
        if len(three) >= 2 or (len(three) == 1 and len(two) >= 1):
            three.extend(two)
            self.handcards = list(set(three))
            return True
        return False


    def hand_checker(self, cards):
        self.cards = cards
        self.suits = [card[0] for card in self.cards]
        self.values = [card[1] for card in self.cards]
        self.values.sort()
        self.freq = Counter()
        self.freq.update(self.values)
        self.vals = self.freq.values()
        self.lstvals = list(self.vals)
        self.check = []

        for i in self.values:
            if i == "K":
                self.check.append(13)
            elif i == "Q":
                self.check.append(12)
            elif i == "J":
                self.check.append(11)
            elif i == "A":
                self.check.append(14)
            else:
                self.check.append(int(i))

            if 14 in self.check:
                if 2 in self.check and 3 in self.check and 4 in self.check and 5 in self.check:
                    self.check.append(1)
        

        if self.straight_flush():
            if self.handcards == [14]:
                self.hand = 10
            else:
                self.hand = 9


        elif self.four():
            self.hand = 8

        elif self.fullhouse():
            self.hand = 7

        elif self.flush():
            self.hand = 6

        elif self.straight():
            self.hand = 5

        elif self.three():
            self.hand = 4

        elif self.twopair():
            self.hand = 3

        elif self.two():
            self.hand = 2

        else:
            self.hand = 1
            numbers = [switch[i[1]] for i in self.cards]
            self.handcards = sorted(numbers, reverse=True)

        return (self.hand, tuple(self.handcards))
    
class HandComparison:
    def __init__(self):
        self.results = []
        self.compare = []
        self.besthand = 0
        self.bestplayers = []

    def compare_hands(self, hands):
        self.reset()

        self.hands = [h.cards if hasattr(h, 'cards') else h for h in hands]
        self.checker = HandChecker()
        for hand in self.hands:
            self.results.append(self.checker.hand_checker(hand))
        self.best = max(self.results)
        return self.best

    def reset(self):
        self.results = []
        self.compare = []
        self.besthand = 0
        self.bestplayers = []