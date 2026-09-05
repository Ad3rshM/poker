from random import shuffle

suits = ["Clubs", "Spades", "Diamonds", "Hearts"]
numbers = ['A', '2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K']
switch = {
    '2': 2,
    '3': 3,
    '4': 4,
    '5': 5,
    '6': 6,
    '7': 7,
    '8': 8,
    '9': 9,
    '10': 10,
    'J': 11,
    'Q': 12,
    'K': 13,
    'A': 14
}


class Dealer:
    def __init__(self):
        self.suits = suits
        self.numbers = numbers
        self.deck = [(i, j) for i in self.suits for j in self.numbers]
        self.resetDeck()
    def resetDeck(self):
        shuffle(self.deck)
    def deal(self, repeat):
        return [self.deck.pop() for i in range(repeat)]