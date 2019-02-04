from node import Node
from copy import deepcopy


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
        if x > self.n:
            return []

        for i in range(self.n):
            if self.can_add_queen((x, i)):
                new_queens = deepcopy(queens)
                new_queens.append((x, i))
                new_node = SuperqueensNode(self, self.g + 1, new_queens, self.n)
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
        return len(self.queen_positions) == 7

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

    def can_add_queen(self, new_queen):
        queens = self.queen_positions
        for queen in queens:
            x1 = queen[0]
            y1 = queen[1]
            x2 = new_queen[0]
            y2 = new_queen[1]
            if y1 == y2 or abs(x1 - x2) == abs(y1 - y2):
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
        return False

    # comparator functions
    def __cmp__(self, other):
        return cmp(self.f, other.f)

    def __lt__(self, other):
        return self.f < other.f
