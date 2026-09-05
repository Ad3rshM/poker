from hand_checker import HandChecker

checker = HandChecker()

royal_flush = [('Diamonds', 'A'), ('Diamonds', '10'), ('Diamonds', 'K'), ('Diamonds', 'Q'), ('Diamonds', 'J')]

straight_flush = [("Diamonds", 'A'), ('Diamonds', '2'), ('Diamonds', '3'), ('Diamonds', '4'), ('Diamonds', '5'), ('Clubs','6')]

four_of_a_kind = [('Diamonds', '9'), ('Spades', '9'), ('Clubs', '9'), ('Hearts', '9'), ('Diamonds', '3')]

full_house = [('Clubs', '9'), ('Diamonds', '9'), ('Spades', '3'), ('Clubs', '3'), ('Diamonds', '3')]

flush = [('Clubs', 'A'), ('Clubs', '5'), ('Clubs', '7'), ('Clubs', '2'), ('Clubs', '3')]

straight = [('Diamonds', 'A'), ('Clubs', '2'), ('Hearts', '3'), ('Diamonds', '4'), ('Clubs', '5')]

three_of_a_kind = [('Clubs', '9'), ('Diamonds', '9'), ('Spades', '9'), ('Clubs', '2'), ('Diamonds', '3')]

two_pair = [('Clubs', '9'), ('Diamonds', '2'), ('Spades', '9'), ('Clubs', '3'), ('Diamonds', '3')]

pair = [('Clubs', '8'), ('Diamonds', '2'), ('Spades', '9'), ('Clubs', '3'), ('Diamonds', '3')]

high_card = [('Clubs', '8'), ('Diamonds', '2'), ('Spades', '9'), ('Clubs', '4'), ('Diamonds', '3')]

print(checker.hand_checker(royal_flush))
print(checker.hand_checker(straight_flush))
print(checker.hand_checker(four_of_a_kind))
print(checker.hand_checker(full_house))
print(checker.hand_checker(flush))
print(checker.hand_checker(straight))
print(checker.hand_checker(three_of_a_kind))
print(checker.hand_checker(two_pair))
print(checker.hand_checker(pair))
print(checker.hand_checker(high_card))

