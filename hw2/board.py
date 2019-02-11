# This class represents the game board
class Board(object):

    def __init__(self, original=None, height=6, width=7):

        if (original):
            self.board = [list(col) for col in original.board]
            self.numMoves = original.numMoves
            self.height = original.height
            self.width = original.width
            return

        # create new board
        else:
            self.height = height
            self.width = width
            self.board = [[] for x in range(self.width)]
            self.numMoves = 0
            return

    # put a token to the defined column
    #    0 - Player 1 token
    #    1 - Player 2 token
    def makeMove(self, column):
        token = self.numMoves % 2
        self.numMoves += 1
        self.board[column].append(token)

    # check if the board is terminal and return:
    #   -1 if the game is not over yet
    #    0 if it's a draw
    #    1 if Player 1 is the winner
    #    2 if Player 2 is the winner
    def isGoal(self):
        for i in range(0, self.width):
            for j in range(0, self.height):
                try:
                    if self.board[i][j] == self.board[i + 1][j] == self.board[i + 2][j] == self.board[i + 3][j]:
                        return self.board[i][j] + 1
                except IndexError:
                    pass

                try:
                    if self.board[i][j] == self.board[i][j + 1] == self.board[i][j + 2] == self.board[i][j + 3]:
                        return self.board[i][j] + 1
                except IndexError:
                    pass

                try:
                    if not j + 3 > self.height and self.board[i][j] == self.board[i + 1][j + 1] == self.board[i + 2][
                        j + 2] == self.board[i + 3][j + 3]:
                        return self.board[i][j] + 1
                except IndexError:
                    pass

                try:
                    if not j - 3 < 0 and self.board[i][j] == self.board[i + 1][j - 1] == self.board[i + 2][j - 2] == \
                            self.board[i + 3][j - 3]:
                        return self.board[i][j] + 1
                except IndexError:
                    pass
        if self.isFull():
            return 0
        return -1

    # return True when the board is full
    def isFull(self):
        return self.numMoves == self.width * self.height

    # return heuristic for a board
    def heuristic(self):
        h = 0
        state = self.board
        for i in range(0, self.width):
            for j in range(0, self.height):
                # check horizontal streaks
                try:
                    # player 1
                    if state[i][j] == state[i + 1][j] == 0:
                        h += 10
                    if state[i][j] == state[i + 1][j] == state[i + 2][j] == 0:
                        h += 100
                    if state[i][j] == state[i + 1][j] == state[i + 2][j] == state[i + 3][j] == 0:
                        h += 10000

                    # player 2
                    if state[i][j] == state[i + 1][j] == 1:
                        h -= 10
                    if state[i][j] == state[i + 1][j] == state[i + 2][j] == 1:
                        h -= 100
                    if state[i][j] == state[i + 1][j] == state[i + 2][j] == state[i + 3][j] == 1:
                        h -= 10000
                except IndexError:
                    pass

                # check vertical streaks
                try:
                    # player 1
                    if state[i][j] == state[i][j + 1] == 0:
                        h += 10
                    if state[i][j] == state[i][j + 1] == state[i][j + 2] == 0:
                        h += 100
                    if state[i][j] == state[i][j + 1] == state[i][j + 2] == state[i][j + 3] == 0:
                        h += 10000

                    # player 2
                    if state[i][j] == state[i][j + 1] == 1:
                        h -= 10
                    if state[i][j] == state[i][j + 1] == state[i][j + 2] == 1:
                        h -= 100
                    if state[i][j] == state[i][j + 1] == state[i][j + 2] == state[i][j + 3] == 1:
                        h -= 10000
                except IndexError:
                    pass

                # check positive diagonal streaks
                try:
                    # player 1
                    if not j + 3 > self.height and state[i][j] == state[i + 1][j + 1] == 0:
                        h += 100
                    if not j + 3 > self.height and state[i][j] == state[i + 1][j + 1] == state[i + 2][j + 2] == 0:
                        h += 100
                    if not j + 3 > self.height and state[i][j] == state[i + 1][j + 1] == state[i + 2][j + 2] \
                            == state[i + 3][j + 3] == 0:
                        h += 10000

                    # player 2
                    if not j + 3 > self.height and state[i][j] == state[i + 1][j + 1] == 1:
                        h -= 100
                    if not j + 3 > self.height and state[i][j] == state[i + 1][j + 1] == state[i + 2][j + 2] == 1:
                        h -= 100
                    if not j + 3 > self.height and state[i][j] == state[i + 1][j + 1] == state[i + 2][j + 2] \
                            == state[i + 3][j + 3] == 1:
                        h -= 10000
                except IndexError:
                    pass

                # check negative diagonal streaks
                try:
                    # player 1
                    if not j - 3 < 0 and state[i][j] == state[i + 1][j - 1] == 0:
                        h += 10
                    if not j - 3 < 0 and state[i][j] == state[i + 1][j - 1] == state[i + 2][j - 2] == 0:
                        h += 100
                    if not j - 3 < 0 and state[i][j] == state[i + 1][j - 1] == state[i + 2][j - 2] \
                            == state[i + 3][j - 3] == 0:
                        h += 10000

                    # player 2
                    if not j - 3 < 0 and state[i][j] == state[i + 1][j - 1] == 1:
                        h -= 10
                    if not j - 3 < 0 and state[i][j] == state[i + 1][j - 1] == state[i + 2][j - 2] == 1:
                        h -= 100
                    if not j - 3 < 0 and state[i][j] == state[i + 1][j - 1] == state[i + 2][j - 2] \
                            == state[i + 3][j - 3] == 1:
                        h -= 10000
                except IndexError:
                    pass
        return h
