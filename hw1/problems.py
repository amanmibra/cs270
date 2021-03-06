from node import Node

from copy import deepcopy

# helper functions
def getXY(board, val):
    for x in range(len(board)):
        for y in range(len(board[0])):
            if board[x][y] == val:
                return [x, y]
    return None


class FifteensNode(Node):
    """Extends the Node class to solve the 15 puzzle.

    Parameters
    ----------
    parent : Node, optional
        The parent node. It is optional only if the input_str is provided. Default is None.

    g : int or float, optional
        The cost to reach this node from the start node : g(n).
        In this puzzle it is the number of moves to reach this node from the initial configuration.
        It is optional only if the input_str is provided. Default is 0.

    board : list of lists
        The two-dimensional list that describes the state. It is a 4x4 array of values 0, ..., 15.
        It is optional only if the input_str is provided. Default is None.

    input_str : str
        The input string to be parsed to create the board.
        The argument 'board' will be ignored, if input_str is provided.
        Example: input_str = '1 2 3 4\n5 6 7 8\n9 10 0 11\n13 14 15 12' # 0 represents the empty cell

    Examples
    ----------
    Initialization with an input string (Only the first/root construction call should be formatted like this):
    >>> n = FifteensNode(input_str=initial_state_str)
    >>> print(n)
      5  1  4  8
      7     2 11
      9  3 14 10
      6 13 15 12

    Generating a child node (All the child construction calls should be formatted like this) ::
    >>> n = FifteensNode(parent=p, g=p.g+c, board=updated_board)
    >>> print(n)
      5  1  4  8
      7  2    11
      9  3 14 10
      6 13 15 12

    """

    def __init__(self, parent=None, g=0, board=None, input_str=None):
        # NOTE: You shouldn't modify the constructor
        if input_str:
            self.board = []
            for i, line in enumerate(filter(None, input_str.splitlines())):
                self.board.append([int(n) for n in line.split()])
        else:
            self.board = board

        self.goal_board = [
            [1, 2, 3, 4],
            [5, 6, 7, 8],
            [9, 10, 11, 12],
            [13, 14, 15, 0]
        ]
        super(FifteensNode, self).__init__(parent, g)

    def generate_children(self):
        """Generates children by trying all 4 possible moves of the empty cell.

        Returns
        -------
            children : list of Nodes
                The list of child nodes.
        """

        # TODO: add your code here
        # You should use self.board to produce children. Don't forget to create a new board for each child
        # e.g you can use copy.deepcopy function from the standard library.
        board = self.board
        row_len = len(board)
        col_len = len(board[0])
        [x, y] = getXY(board, 0)  # get x and y values of empty cell

        children = []

        # creating boards and nodes

        # add board by switching empty cell with...
        # right cell
        if x > 0:
            # make copy of board
            new_board = deepcopy(board)
            temp = new_board[x][y]
            new_board[x][y] = new_board[x - 1][y]
            new_board[x - 1][y] = temp

            new_node = FifteensNode(self, self.g + 1, new_board)
            children.append(new_node)
        # left cell
        if x < row_len - 1:
            # make copy of board
            new_board = deepcopy(board)
            temp = new_board[x][y]
            new_board[x][y] = new_board[x + 1][y]
            new_board[x + 1][y] = temp

            new_node = FifteensNode(self, self.g + 1, new_board)
            children.append(new_node)
        # above cell
        if y > 0:
            # make copy of board
            new_board = deepcopy(board)
            temp = new_board[x][y]
            new_board[x][y] = new_board[x][y - 1]
            new_board[x][y - 1] = temp

            new_node = FifteensNode(self, self.g + 1, new_board)
            children.append(new_node)
        # below cell
        if y < col_len - 1:
            # make copy of board
            new_board = deepcopy(board)
            temp = new_board[x][y]
            new_board[x][y] = new_board[x][y + 1]
            new_board[x][y + 1] = temp

            new_node = FifteensNode(self, self.g + 1, new_board)
            children.append(new_node)
        return children

    def is_goal(self):
        """Decides whether this search state is the final state of the puzzle.

        Returns
        -------
            is_goal : bool
                True if this search state is the goal state, False otherwise.
        """

        # TODO: add your code here
        # You should use self.board to decide.
        return self.board == self.goal_board

    def evaluate_heuristic(self):
        """Heuristic function h(n) that estimates the minimum number of moves
        required to reach the goal state from this node.

        Returns
        -------
            h : int or float
                The heuristic value for this state.
        """

        # h = hueristic
        # the total number of moves each indiv. tile may need
        # to get to its correct spot
        h = 0
        board = self.board
        for i in range(len(board)):
            for j in range(len(board[0])):
                if board[i][j] == 0:
                    continue
                # get coordinates of actual value
                [x, y] = getXY(self.goal_board, board[i][j])
                # add min # of moves to move a single tile to its
                # correct spot to hueristic
                h += abs(x - i) + abs(y - j)
        return h

    def _get_state(self):
        """Returns an hashable representation of this search state.

        Returns
        -------
            state: tuple
                The hashable representation of the search state
        """
        # NOTE: You shouldn't modify this method.
        return tuple([n for row in self.board for n in row])

    def __str__(self):
        """Returns the string representation of this node.

        Returns
        -------
            state_str : str
                The string representation of the node.
        """
        # NOTE: You shouldn't modify this method.
        sb = []  # String builder
        for row in self.board:
            for i in row:
                sb.append(' ')
                if i == 0:
                    sb.append('  ')
                else:
                    if i < 10:
                        sb.append(' ')
                    sb.append(str(i))
            sb.append('\n')
        return ''.join(sb)

    def visited(self, child, visited):
        new_board = child.board
        # path = self.get_path()
        for node in visited:
            if node.board == new_board:
                return True
        return False

    # comparator functions
    def __cmp__(self, other):
        return cmp(self.f, other.f)

    def __lt__(self, other):
        return self.f < other.f


class SuperqueensNode(Node):
    """Extends the Node class to solve the Superqueens problem.

    Parameters
    ----------
    parent : Node, optional
        The parent node. Default is None.

    g : int or float, optional
        The cost to reach this node from the start node : g(n).
        In this problem it is the number of pairs of superqueens that can attack each other in this state configuration.
        Default is 1.

    queen_positions : list of pairs
        The list that stores the x and y positions of the queens in this state configuration.
        Example: [(q1_y,q1_x),(q2_y,q2_x)]. Note that the upper left corner is the origin and y increases downward
        Default is the empty list [].
        ------> x
        |
        |
        v
        y

    n : int
        The size of the board (n x n)

    Examples
    ----------
    Initialization with a board size (Only the first/root construction call should be formatted like this):
    >>> n = SuperqueensNode(n=4)
    >>> print(n)
         .  .  .  .
         .  .  .  .
         .  .  .  .
         .  .  .  .

    Generating a child node (All the child construction calls should be formatted like this):
    >>> n = SuperqueensNode(parent=p, g=p.g+c, queen_positions=updated_queen_positions, n=p.n)
    >>> print(n)
         Q  .  .  .
         .  .  .  .
         .  .  .  .
         .  .  .  .

    """

    def __init__(self, parent=None, g=0, queen_positions=[], n=1):
        # NOTE: You shouldn't modify the constructor
        self.queen_positions = queen_positions
        self.n = n
        super(SuperqueensNode, self).__init__(parent, g)

    def generate_children(self):
        """Generates children by adding a new queen.

        Returns
        -------
            children : list of Nodes
                The list of child nodes.
        """
        # TODO: add your code here
        # You should use self.queen_positions and self.n to produce children.
        # Don't forget to create a new queen_positions list for each child.
        # You can use copy.deepcopy function from the standard library.
        children = []
        queens = self.queen_positions
        x = len(queens)

        # return no children if past board limit
        if x >= self.n:
            return []

        for i in range(self.n):
            if self.can_add_queen((x, i)):
                new_queens = deepcopy(queens)
                new_queens.append((x, i))
                conflicts = self.conflicts((x, i))
                new_node = SuperqueensNode(self, self.g + conflicts, new_queens, self.n)
                children.append(new_node)
        return children

    def is_goal(self):
        """Decides whether all the queens are placed on the board.

        Returns
        -------
            is_goal : bool
                True if all the queens are placed on the board, False otherwise.
        """
        # You should use self.queen_positions and self.n to decide.
        # TODO: add your code here
        # print(self.queen_positions, self.f)
        # print(self.queen_positions)
        # print(self._get_state())
        # print(self)
        return len(self.queen_positions) == self.n

    def evaluate_heuristic(self):
        """Heuristic function h(n) that estimates the minimum number of conflicts required to reach the final state.

        Returns
        -------
            h : int or float
                The heuristic value for this state.
        """
        # If you want to design a heuristic for this problem, you should use self.queen_positions and self.n.
        # TODO: add your code here (optional)
        return 0

    def _get_state(self):
        """Returns an hashable representation of this search state.

        Returns
        -------
            state: tuple
                The hashable representation of the search state
        """
        # NOTE: You shouldn't modify this method.
        return tuple(self.queen_positions)

    def conflicts(self, new_queen):
        queens = self.queen_positions
        output = 0
        [x, y] = new_queen
        for queen in queens:
            [x1, y1] = queen
            if (abs(x - x1) + abs(y - y1)) == 3:
                output += 1
            if abs(x - x1) == abs(y - y1):
                output += 1
        return output

    def can_add_queen(self, new_queen):
        queens = self.queen_positions
        for queen in queens:
            if queen[1] == new_queen[1]:
                return False
        return True

    def __str__(self):
        """Returns the string representation of this node.

        Returns
        -------
            state_str : str
                The string representation of the node.
        """
        # NOTE: You shouldn't modify this method.
        sb = [[' . '] * self.n for i in range(self.n)]  # String builder
        for i, j in self.queen_positions:
            sb[i][j] = ' Q '
        return '\n'.join([''.join(row) for row in sb])

    def visited(self, child, visited):
        for node in visited:
            if node.queen_positions == child.queen_positions:
                return True
        return False

    # comparator functions
    def __cmp__(self, other):
        return cmp(self.f, other.f)

    def __lt__(self, other):
        return self.f < other.f
