"""Implementation of the game window.

"""
from PyQt5.QtWidgets import (QWidget, QPushButton, QLabel, QToolButton,
                             QHBoxLayout, QVBoxLayout)
from PyQt5.QtCore import Qt, QTimer
from PyQt5.QtGui import QFont

from bot import randomBot, alphaBetaBot, minMaxBot, HumanPlayer
from board import Board

from functools import partial
import sip
import copy


class Game(QWidget):
    """Game window.

    Parameters
    ----------
    parent : QWidget
        The main window object. It will be used to send a signal to the main menu.

    player1_name : str
        The name of the first player. It should be one of 'Human', 'Random', 'AI-Minimax', 'AI-AlphaBeta'.

    player2_name : str
        The name of the second player. It should be one of 'Human', 'Random', 'AI-Minimax', 'AI-AlphaBeta'.

    depth1_limit : int
        The maximum search depth to be used in the Minimax algorithm by the first AI.

    depth2_limit : int
        The maximum search depth to be used in the Minimax algorithm by the second AI.

    height : int
        The height of the board. It must be greater than or equal to 4.

    width : int
        The width of the board. It must be greater than or equal to 4.

    """

    players = {
        'Human': HumanPlayer,
        'Random': randomBot,
        'AI-Minimax': minMaxBot,
        'AI-AlphaBeta': alphaBetaBot
    }
    """Mapping from player names to classes."""

    def __init__(self, parent, player1_name, player2_name, depth1_limit, depth2_limit, height, width):
        super(Game, self).__init__(parent)

        # Construct the players.
        self.player1 = Game.players[player1_name](depth1_limit, True)
        self.player2 = Game.players[player2_name](depth2_limit, False)
        self.turn = self.player1

        self.header = QLabel()
        self.buttons = []
        self.board = Board(height=height, width=width)

        self.board_widget = QWidget()
        self.set_ui(parent)

        # Trigger the next AI move.
        # The time delay is required to update the GUI.
        QTimer.singleShot(10, self.next)

    def next(self):
        """Calls findMove method of the player. If the player is human, it will ignore it.
        """
        move = self.turn.findMove(copy.deepcopy(self.board))
        if move is not None:  # If the move has been made by an AI.
            self.make_move(move)

    def update_board(self):
        """Redraws the game board.
        """

        # Clear the old board. Note sip is required for immediate deletion.
        if self.board_widget.layout():
            sip.delete(self.board_widget.layout())

        # The board container.
        board_vbox = QVBoxLayout()

        # Add the discs from the top to the bottom.
        for i in reversed(range(self.board.height)):
            row_hbox = QHBoxLayout()  # The row container
            row_hbox.addStretch(1)
            for j in range(self.board.width):  # For each column
                btn = QToolButton()
                btn.setDisabled(True)
                if i < len(self.board.board[j]):
                    if self.board.board[j][i]:  # If it belongs to the second player
                        color = '#F00F0F'
                    else:  # If it belongs to the first player
                        color = '#0F0FF0'
                else:  # If it is an empty slot
                    color = 'white'
                btn.setStyleSheet('''
                    QToolButton{
                        height: 32px;
                        width: 32px;
                        border-style: solid;
                        border-color: grey;
                        border-width: 1px;
                        border-radius: 16px;
                        background-color : ''' + color + ''';
                    }
                ''')
                row_hbox.addWidget(btn)
                row_hbox.addStretch(1)
            board_vbox.addLayout(row_hbox)
        self.board_widget.setLayout(board_vbox)

    def update_header(self):
        """Redraws the header. It is called before each turn.
        """
        is_over = self.board.isGoal()
        if is_over == -1:  # If the game continues
            if self.turn is self.player1:
                self.header.setText('Player 1\'s turn')
                self.header.setStyleSheet('color: #0F0FF0')
            else:
                self.header.setText('Player 2\'s turn')
                self.header.setStyleSheet('color: #F00F0F')
        elif is_over == 0:  # If it is draw
            self.header.setText('Draw!')
            self.header.setStyleSheet('color: black')
        else:  # If one of the players wins
            if self.turn is self.player2:
                self.header.setText('Player 1 wins!')
                self.header.setStyleSheet('color: #0F0FF0')
            else:
                self.header.setText('Player 2 wins!')
                self.header.setStyleSheet('color: #F00F0F')
        return is_over

    def update_buttons(self):
        """Changes the color of buttons (down arrows) after each turn.
        """
        color = '#0F0FF0' if self.turn is self.player1 else '#F00F0F'
        for btn in self.buttons:
            btn.setArrowType(Qt.DownArrow)
            btn.setStyleSheet('''
                QToolButton{
                    height: 30px;
                    width: 30px;
                    color : ''' + color + ''';
                }
            ''')

    def make_move(self, move):
        """Drops a disc into the column chosen (move); and updates the board, the header and the buttons accordingly.

        Parameters
        ----------
        move : int
            The column selected by the player or the AI.
        """
        # If the move is illegal or the game ended, ignore the move.
        if len(self.board.board[move]) == self.board.height or self.board.isGoal() > -1:
            return
        self.board.makeMove(move)
        # Update the turn.
        self.turn = self.player2 if self.turn is self.player1 else self.player1
        self.update_buttons()
        self.update_board()

        # Next move.
        if self.update_header() == -1:
            QTimer.singleShot(10, self.next)

    def set_ui(self, parent):
        """Initializes the game window.

        Parameters
        ----------
        parent : QWidget
            The main window object. It will be used to send a signal to the main menu.

        """
        # The main layout.
        vbox = QVBoxLayout()
        vbox.addStretch(1)

        # HEADER
        self.header.setAlignment(Qt.AlignCenter)
        self.header.setFont(QFont('Times', 18))
        vbox.addWidget(self.header)
        self.update_header()

        vbox.addStretch(1)

        # BOARD
        buttons_hbox = QHBoxLayout()
        buttons_hbox.addStretch(1)

        for i in range(self.board.width):
            btn = QToolButton()
            btn.setArrowType(Qt.DownArrow)
            btn.clicked.connect(partial(self.make_move, i))
            self.buttons.append(btn)
            buttons_hbox.addWidget(btn)
        self.update_buttons()

        buttons_hbox.addStretch(1)
        vbox.addLayout(buttons_hbox)

        board_hbox = QHBoxLayout()
        board_hbox.addStretch(1)
        self.update_board()
        board_hbox.addWidget(self.board_widget)
        board_hbox.addStretch(1)
        vbox.addLayout(board_hbox)

        vbox.addStretch(1)

        # NEW GAME
        newgame_hbox = QHBoxLayout()
        newgame_hbox.addStretch(1)
        newgame = QPushButton('New Game')
        newgame.clicked.connect(parent.newgame)
        newgame_hbox.addWidget(newgame)
        newgame_hbox.addStretch(1)
        vbox.addLayout(newgame_hbox)
        vbox.addStretch(3)

        self.setLayout(vbox)
