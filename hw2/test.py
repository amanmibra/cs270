"""A set of example unit tests.
NOTE: Do not rely on these tests as they are just simple examples.
Your code will be tested on some secret instances of the problems!
"""

import unittest
from board import Board
from bot import Bot, minMaxBot, alphaBetaBot
import math


class TestConnectFour(unittest.TestCase):
    def test_runtime_errors(self):
        """Tests that the methods of the bot classes can be called without an error.
        """
        parent_bot = Bot(3, True)
        minimax_bot = minMaxBot(4, False)
        alphabeta_bot = alphaBetaBot(5, True)
        board = Board()
        parent_bot.generateChildren(board)
        minimax_bot.findMove(board)
        minimax_bot.miniMax(board, depth=2, player=True)
        alphabeta_bot.alphaBeta(board, depth=2, player=False, alpha=3, beta=5)

    def test_generate_children(self):
        """Tests that the generate_children method creates the children of the empty board correctly.
        """
        parent_bot = Bot(3, True)
        board = Board()
        target_states = [
            ((0,), (), (), (), (), (), ()),
            ((), (0,), (), (), (), (), ()),
            ((), (), (0,), (), (), (), ()),
            ((), (), (), (0,), (), (), ()),
            ((), (), (), (), (0,), (), ()),
            ((), (), (), (), (), (0,), ()),
            ((), (), (), (), (), (), (0,)),
        ]
        for target, (i, child) in zip(target_states, parent_bot.generateChildren(board)):
            child_state = tuple([tuple(col) for col in child.board])
            self.assertEqual(child_state, target)

    def test_minimax(self):
        """Tests that the miniMax method returns the correct score and the move for a particular configuration.
        """
        board = Board()
        board.board[0].append(0)
        board.board[1].append(1)
        board.numMoves = 2
        minimax_bot = minMaxBot(4, True)
        s, m = minimax_bot.miniMax(board, minimax_bot.depthLimit, True)
        self.assertEqual(s, 30)
        self.assertEqual(m, 0)

    def test_alphabeta(self):
        """Tests that the alphaBeta method returns the correct score and the move for a particular configuration.
        """
        board = Board()
        board.board[0].append(0)
        board.board[1].append(1)
        board.board[0].append(0)
        board.numMoves = 3
        alphabeta_bot = alphaBetaBot(6, False)
        s, m = alphabeta_bot.alphaBeta(board, alphabeta_bot.depthLimit, False, -math.inf, math.inf)
        self.assertEqual(s, 130)
        self.assertEqual(m, 0)

    def test_alphabeta_eq_minimax(self):
        """Tests that the miniMax and the alphaBeta methods return the same score and move for a particular configuration.
        """
        board = Board()
        board.board[0].append(0)
        board.board[1].append(1)
        board.board[0].append(0)
        board.board[1].append(1)
        board.numMoves = 4
        minimax_bot = minMaxBot(5, True)
        s_mm, m_mm = minimax_bot.miniMax(board, minimax_bot.depthLimit, True)
        alphabeta_bot = alphaBetaBot(5, True)
        s_ab, m_ab = alphabeta_bot.alphaBeta(board, alphabeta_bot.depthLimit, True, -math.inf, math.inf)
        self.assertEqual(s_mm, s_ab)
        self.assertEqual(m_mm, m_ab)


if __name__ == '__main__':
    unittest.main()
