"""Implementation of the A* algorithm.

This file contains a skeleton implementation of the A* algorithm. It is a single
method that accepts the root node and runs the A* algorithm
using that node's methods to generate children, evaluate heuristics, etc.
This way, plugging in root nodes of different types, we can run this A* to
solve different problems.

"""

from queue import PriorityQueue

def Astar(root):
    """Runs the A* algorithm given the root node. The class of the root node
    defines the problem that's being solved. The algorithm either returns the solution
    as a path from the start node to the goal node or returns None if there's no solution.

    Parameters
    ----------
    root: Node
        The start node of the problem to be solved.

    Returns
    -------
        path: list of Nodes or None
            The solution, a path from the initial node to the goal node.
            If there is no solution it should return None
    """

    # TODO: add your code here
    # Some helper pseudo-code:
    # 1. Create an empty fringe and add your root node (you can use lists, sets, heaps, ... )
    # 2. While the container is not empty:
    # 3.      Pop the best? node (Use the attribute `node.f` in comparison)
    # 4.      If that's a goal node, return node.get_path()
    # 5.      Otherwise, add the children of the node to the fringe
    # 6. Return None
    #
    # Some notes:
    # You can access the state of a node by `node.state`. (You may also want to store evaluated states)
    # You should consider the states evaluated and the ones in the fringe to avoid repeated calculation in 5. above.
    # You can compare two node states by node1.state == node2.state
    if root is None:
        return None

    children = root.generate_children()

    if root.is_goal():
        return root.get_path()
    elif children == []:
        return []
    else:
        pq = PriorityQueue()
        return search(root, pq, [])


# - Add children to PQ
# - If child node exists already in PQ, then update f and update PQ
# - Pop the child in PQ with lowest f value
# - Recursive call
def search(node, queue, visited):
    if node is None:
        return None

    children = node.generate_children()

    if node.is_goal():
        return node.get_path()
    elif children == []:
        return []

    for child in children:
        if not node.visited(child, visited):
            queue.put((child.f, child))

    while not queue.empty():
        element = queue.get()  # tuple of (weight, node)
        node = element[1]
        visited.append(node)
        path = search(node, queue, visited)
        if path != [] and path is not None:
            return path

    return None
