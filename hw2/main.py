"""Implementation of the main window and the menu.
"""

import sys
from PyQt5.QtWidgets import (QWidget, QPushButton, QLabel, QSpinBox,
                             QHBoxLayout, QVBoxLayout, QApplication, QComboBox)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont

from game import Game


class Menu(QWidget):
    """Main menu.

    Parameters
    ----------
    parent : QWidget
        The main window object. It will be used to send a signal to the main menu.

    """
    def __init__(self, parent):
        super(Menu, self).__init__(parent)

        # MAIN LAYOUT
        vbox = QVBoxLayout()
        vbox.addStretch(1)

        # HEADER
        compsci270 = QLabel('CompSci 270')
        compsci270.setAlignment(Qt.AlignCenter)
        compsci270.setFont(QFont('Times', 24, QFont.Bold))
        vbox.addWidget(compsci270)
        hw2 = QLabel('Homework 2: Connect-Four')
        hw2.setAlignment(Qt.AlignCenter)
        hw2.setFont(QFont('Times', 18))
        vbox.addWidget(hw2)
        vbox.addStretch(1)

        # PLAYERS
        players_hbox = QHBoxLayout()
        players_hbox.addStretch(4)

        # Player 1 Options
        player1 = QComboBox()
        player1.addItems(['Human', 'Random', 'AI-Minimax', 'AI-AlphaBeta'])
        player1_label = QLabel('Player 1: ')
        player1_label.setBuddy(player1)
        players_hbox.addWidget(player1_label)
        players_hbox.addWidget(player1)

        players_hbox.addStretch(1)

        # Player 2 Options
        player2 = QComboBox()
        player2.addItems(['Human', 'Random', 'AI-Minimax', 'AI-AlphaBeta'])
        player2_label = QLabel('Player 2: ')
        player2_label.setBuddy(player2)
        players_hbox.addWidget(player2_label)
        players_hbox.addWidget(player2)

        players_hbox.addStretch(4)

        vbox.addLayout(players_hbox)
        vbox.addStretch(1)

        # DEPTH
        depth_header = QLabel('AI Difficulty (Depth Limit)')
        depth_header.setAlignment(Qt.AlignCenter)
        depth_header.setFont(QFont('Times', 15))
        vbox.addWidget(depth_header)
        depth_hbox = QHBoxLayout()
        depth_hbox.addStretch(5)
        depth1 = QSpinBox()
        depth1.setMinimum(1)
        depth1.setMaximum(16)
        depth1_label = QLabel('Player 1: ')
        depth1_label.setBuddy(depth1_label)
        depth_hbox.addWidget(depth1_label)
        depth_hbox.addWidget(depth1)
        depth_hbox.addStretch(1)
        depth2 = QSpinBox()
        depth2.setMinimum(1)
        depth2.setMaximum(16)
        depth2_label = QLabel('Player 2: ')
        depth2_label.setBuddy(depth2_label)
        depth_hbox.addWidget(depth2_label)
        depth_hbox.addWidget(depth2)
        depth_hbox.addStretch(5)
        vbox.addLayout(depth_hbox)
        vbox.addStretch(1)

        # BOARD SIZE
        board_hbox = QHBoxLayout()
        board_hbox.addStretch(4)

        # Height Options
        height = QSpinBox()
        height.setMinimum(6)
        height.setMaximum(16)
        height_label = QLabel('Height: ')
        height_label.setBuddy(height)
        board_hbox.addWidget(height_label)
        board_hbox.addWidget(height)

        board_hbox.addStretch(1)

        # Width Options
        width = QSpinBox()
        width.setMinimum(7)
        width.setMaximum(16)
        width_label = QLabel('Width: ')
        width_label.setBuddy(width)
        board_hbox.addWidget(width_label)
        board_hbox.addWidget(width)

        board_hbox.addStretch(4)
        vbox.addLayout(board_hbox)

        vbox.addStretch(1)

        # START
        start_hbox = QHBoxLayout()
        start_hbox.addStretch(1)
        start = QPushButton('Start')
        start.clicked.connect(lambda: parent.start(player1.currentText(), player2.currentText(), depth1.value(),
                                                   depth2.value(), height.value(), width.value()))
        start_hbox.addWidget(start)
        start_hbox.addStretch(1)
        vbox.addLayout(start_hbox)
        vbox.addStretch(3)

        self.setLayout(vbox)


class MainWindow(QWidget):
    """Main widget of the application that handles transitions between the main menu and the game.
    """
    def __init__(self):
        super(MainWindow, self).__init__()

        self.resize(512, 512)
        self.setWindowTitle('CompSci 270 - Homework 2 - Connect-Four')

        layout = QVBoxLayout()
        layout.addWidget(Menu(self))
        self.setLayout(layout)

    def clear(self):
        """Removes the widgets attached to the main window.
        """
        for i in reversed(range(self.layout().count())):
            self.layout().itemAt(i).widget().deleteLater()

    def start(self, player1_name, player2_name, depth1_limit, depth2_limit, height, width):
        """Creates a game using the parameters.

        Parameters
        ----------
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
        self.clear()
        self.layout().addWidget(Game(self, player1_name, player2_name, depth1_limit, depth2_limit, height, width))

    def newgame(self):
        """Creates the main menu.
        """
        self.clear()
        self.layout().addWidget(Menu(self))


if __name__ == '__main__':
    app = QApplication(sys.argv)
    app.setStyle('Fusion')

    w = MainWindow()
    w.show()

    sys.exit(app.exec_())
