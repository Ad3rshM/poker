import unittest
from unittest.mock import patch

from dealer import Dealer
from game import Game
from hand_checker import HandChecker, HandComparison
from player import Player


class TestHandChecker(unittest.TestCase):
    def setUp(self):
        self.checker = HandChecker()

    def test_royal_flush(self):
        hand = [
            ('Diamonds', 'A'),
            ('Diamonds', '10'),
            ('Diamonds', 'K'),
            ('Diamonds', 'Q'),
            ('Diamonds', 'J'),
        ]
        self.assertEqual(self.checker.hand_checker(hand), (10, (14,)))

    def test_straight_flush(self):
        hand = [
            ('Diamonds', '9'),
            ('Diamonds', '10'),
            ('Diamonds', 'J'),
            ('Diamonds', 'Q'),
            ('Diamonds', 'K'),
        ]
        self.assertEqual(self.checker.hand_checker(hand), (9, (13,)))

    def test_four_of_a_kind(self):
        hand = [
            ('Diamonds', '9'),
            ('Spades', '9'),
            ('Clubs', '9'),
            ('Hearts', '9'),
            ('Diamonds', '3'),
        ]
        self.assertEqual(self.checker.hand_checker(hand), (8, (9,)))

    def test_full_house(self):
        hand = [
            ('Clubs', '9'),
            ('Diamonds', '9'),
            ('Spades', '3'),
            ('Clubs', '3'),
            ('Diamonds', '3'),
        ]
        self.assertEqual(self.checker.hand_checker(hand), (7, (9, 3)))

    def test_flush(self):
        hand = [
            ('Clubs', 'A'),
            ('Clubs', '5'),
            ('Clubs', '7'),
            ('Clubs', '2'),
            ('Clubs', '3'),
        ]
        self.assertEqual(self.checker.hand_checker(hand), (6, (14, 7, 5, 3, 2)))

    def test_straight(self):
        hand = [
            ('Diamonds', 'A'),
            ('Clubs', '2'),
            ('Hearts', '3'),
            ('Diamonds', '4'),
            ('Clubs', '5'),
        ]
        self.assertEqual(self.checker.hand_checker(hand), (5, (5,)))

    def test_three_of_a_kind(self):
        hand = [
            ('Clubs', '9'),
            ('Diamonds', '9'),
            ('Spades', '9'),
            ('Clubs', '2'),
            ('Diamonds', '3'),
        ]
        self.assertEqual(self.checker.hand_checker(hand), (4, (9,)))

    def test_two_pair(self):
        hand = [
            ('Clubs', '9'),
            ('Diamonds', '2'),
            ('Spades', '9'),
            ('Clubs', '3'),
            ('Diamonds', '3'),
        ]
        self.assertEqual(self.checker.hand_checker(hand), (3, (9, 3)))

    def test_pair(self):
        hand = [
            ('Clubs', '8'),
            ('Diamonds', '2'),
            ('Spades', '9'),
            ('Clubs', '3'),
            ('Diamonds', '3'),
        ]
        self.assertEqual(self.checker.hand_checker(hand), (2, (3,)))

    def test_high_card(self):
        hand = [
            ('Clubs', '8'),
            ('Diamonds', '2'),
            ('Spades', '9'),
            ('Clubs', '4'),
            ('Diamonds', '3'),
        ]
        self.assertEqual(self.checker.hand_checker(hand), (1, (9, 8, 4, 3, 2)))


class TestHandComparison(unittest.TestCase):
    def test_compare_hands_with_player_objects(self):
        dealer = Dealer()
        player1 = Player(dealer, 'PLAYER 1')
        player2 = Player(dealer, 'PLAYER 2')

        player1.cards = [
            ('Diamonds', 'A'),
            ('Diamonds', '10'),
            ('Diamonds', 'K'),
            ('Diamonds', 'Q'),
            ('Diamonds', 'J'),
        ]
        player2.cards = [
            ('Clubs', '8'),
            ('Diamonds', '2'),
            ('Spades', '9'),
            ('Clubs', '3'),
            ('Diamonds', '3'),
        ]

        result = HandComparison().compare_hands([player1, player2])
        self.assertEqual(result, (10, (14,)))

    def test_compare_hands_does_not_accumulate_results(self):
        comparer = HandComparison()
        hand1 = [
            ('Diamonds', 'A'),
            ('Diamonds', '10'),
            ('Diamonds', 'K'),
            ('Diamonds', 'Q'),
            ('Diamonds', 'J'),
        ]
        hand2 = [
            ('Clubs', '8'),
            ('Diamonds', '2'),
            ('Spades', '9'),
            ('Clubs', '3'),
            ('Diamonds', '3'),
        ]

        comparer.compare_hands([hand1])
        first_count = len(comparer.results)
        comparer.compare_hands([hand2])
        second_count = len(comparer.results)

        self.assertEqual(first_count, 1)
        self.assertEqual(second_count, 1)


class TestPlayer(unittest.TestCase):
    @patch('builtins.input', side_effect=['abc', '-5', '200', '50'])
    def test_amount_raised_reprompts_until_valid(self, mocked_input):
        player = Player(Dealer(), 'PLAYER')
        player.money = 100

        amount = player.amount_raised(None)

        self.assertEqual(amount, 50)
        self.assertEqual(mocked_input.call_count, 4)


class TestGame(unittest.TestCase):
    def test_reset_hand_sets_player_state(self):
        dealer = Dealer()
        player1 = Player(dealer, 'PLAYER 1')
        player2 = Player(dealer, 'PLAYER 2')
        game = Game([player1, player2], lambda: None, lambda: None)

        game.reset_hand()

        self.assertFalse(player1.ALL_IN)
        self.assertFalse(player2.ALL_IN)
        self.assertEqual(player1.contribution, 0)
        self.assertEqual(player2.contribution, 0)
        self.assertEqual(player1.prev_move, '')
        self.assertEqual(player2.prev_move, '')
        self.assertEqual(len(player1.cards), 2)
        self.assertEqual(len(player2.cards), 2)

    def test_deal_next_street_progression(self):
        dealer = Dealer()
        player1 = Player(dealer, 'PLAYER 1')
        player2 = Player(dealer, 'PLAYER 2')
        game = Game([player1, player2], lambda: None, lambda: None)

        game.reset_hand()
        game.deal_next_street()
        self.assertTrue(game.flop_over)
        self.assertEqual(len(game.community_cards), 3)
        self.assertEqual(len(player1.cards), 5)
        self.assertEqual(len(player2.cards), 5)

        game.deal_next_street()
        self.assertTrue(game.turn_over)
        self.assertEqual(len(game.community_cards), 4)
        self.assertEqual(len(player1.cards), 6)

        game.deal_next_street()
        self.assertTrue(game.river_over)
        self.assertEqual(len(game.community_cards), 5)
        self.assertEqual(len(player2.cards), 7)

        game.deal_next_street()
        self.assertTrue(game.hand_over)

    def test_game_action_helpers(self):
        dealer = Dealer()
        player1 = Player(dealer, 'PLAYER 1')
        player2 = Player(dealer, 'PLAYER 2')
        player1.opponent = player2
        player2.opponent = player1
        game = Game([player1, player2], lambda: None, lambda: None)

        game.reset_hand()
        player1.contribution = 0
        player1.money = 100
        player2.contribution = 20
        player2.money = 100

        player1.amount_raised = lambda game: 10
        game.raise_option(player1)
        self.assertEqual(player1.contribution, 30)
        self.assertEqual(player1.money, 70)
        self.assertEqual(game.pot, 30)

        player1.contribution = 0
        player1.money = 10
        player2.contribution = 20
        player1.ALL_IN = False
        game.call_option(player1)
        self.assertEqual(player1.contribution, 10)
        self.assertEqual(player1.ALL_IN, True)

        game.pot = 50
        player1.contribution = 10
        player2.money = 40
        game.fold_option(player1)
        self.assertEqual(player2.money, 90)
        self.assertTrue(game.fold)

    def test_handchecker_handles_six_card_flush(self):
        checker = HandChecker()
        hand = [
            ('Clubs', 'A'),
            ('Clubs', 'K'),
            ('Clubs', 'J'),
            ('Clubs', '9'),
            ('Clubs', '7'),
            ('Clubs', '2'),
        ]
        self.assertEqual(checker.hand_checker(hand), (6, (14, 13, 11, 9, 7, 2)))

    def test_handchecker_straight_flush(self):
        checker = HandChecker()
        hand = [
            ('Diamonds', 'A'),
            ('Diamonds', '2'),
            ('Diamonds', '3'),
            ('Diamonds', '4'),
            ('Diamonds', '5'),
            ('Clubs', '7'),
        ]
        self.assertEqual(checker.hand_checker(hand), (9, (5,)))

    @patch('builtins.input', side_effect=['n'])
    def test_play_hand_folds_and_exits(self, mocked_input):
        dealer = Dealer()
        player1 = Player(dealer, 'PLAYER 1')
        player2 = Player(dealer, 'PLAYER 2')
        player1.opponent = player2
        player2.opponent = player1
        ui = type('DummyUI', (), {'enter': lambda self: None, 'clear': lambda self: None, 'play_again': lambda self: None})()
        game = Game([player1, player2], ui.clear, lambda game: None)

        game.reset_hand()
        player1.get_action = lambda g: 'fold'

        game.play_hand(ui)

        self.assertTrue(game.fold)
        self.assertEqual(player2.money, 2000 + game.pot)


if __name__ == '__main__':
    unittest.main()
