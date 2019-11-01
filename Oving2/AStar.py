import Map


class Node:
    """
    Simple object to classify nodes. Keeps track of parent to be able to backtrack the shortest path.
    """
    def __init__(self, pos):
        self.parent = None
        self.children = []
        self.pos = pos
        self.weight = 0
        self.heuristic = 0
        self.total_cost = 0

    def find_children(self, mapno):
        """
        :param mapno: which map is being used, defaults to task1
        :return: array of nodes based on available spaces around current node.
        """
        # List of possible cardinal directions from current position
        directions = [[self.pos[0]-1, self.pos[1]], [self.pos[0]+1, self.pos[1]], [self.pos[0], self.pos[1]-1],
                      [self.pos[0], self.pos[1]+1]]
        arr = []
        for direction in directions:
            try:
                x = mapno.get_cell_value(direction)
                if x >= 0:
                    arr.append(Node(direction))
            except IndexError:
                continue
        return arr


def euclidean_distance(pos, goal_pos):
    """
    :param goal_pos: position of target node
    :param pos: position of current node
    :return length of the shortest possible path in the 2D-space, ignoring obstacles
    """
    return abs(pos[0]-goal_pos[0])+abs(pos[1]-goal_pos[1])


def best_first_search(map_task):
    """
    :param map_task: Current map being used to find shortest path
    :return: If path is found, the goal node is returned with values updated, such that it is possible to backtrack,
    else a "Failed"-message is returned.
    """
    closed, opened = [], []
    node = Node(map_task.get_start_pos())  # Starting node
    opened.append(node)
    x = node  # Redefined for use in while-loop
    while x.pos != map_task.get_goal_pos():
        if len(opened) == 0:
            # If no nodes are left to explore and no path is found, we failed
            return "Failed", "Failed"
        x = opened.pop()
        closed.append(x)
        if x.pos == map_task.get_goal_pos():
            return x, "Success"
        succ = x.find_children(map_task)
        for s in succ:
            new_s = has_been_created(s, opened, closed)
            if new_s not in opened and new_s not in closed:
                attach_and_eval(new_s, x, map_task)
                opened.append(new_s)
                opened.sort(key=lambda y: y.total_cost, reverse=True)
            elif x.weight + map_task.get_cell_value(new_s.pos) < new_s.weight:
                attach_and_eval(new_s, x, map_task)
                if new_s in closed:
                    propagate_path_improvements(new_s, map_task)


def has_been_created(node, list1, list2):
    """
    :param node: Current node to check if already exists
    :param list1: First list that is checked for already existing node
    :param list2: Second list that is checked for already existing node
    :return: If node already exists in list1 or 2, it is replaced with the node in one of these lists, else the node is
    returned
    """
    for x in list1:
        # Checks on position as duplicate positions = duplicate node
        if x.pos == node.pos:
            return x
    for x in list2:
        if x.pos == node.pos:
            return x
    return node


def attach_and_eval(child, parent, map_task):
    """
    :param child: The node to attach to parent, with weight calculated
    :param parent: The node which child is attached to
    :param map_task: Which map is used to calculate weights
    :return: returns nothing, but updates the values of the child node.
    """
    child.parent = parent
    child.weight = parent.weight + map_task.get_cell_value(child.pos)
    child.heuristic = euclidean_distance(child.pos, map_task.get_end_goal_pos())
    child.total_cost = child.weight + child.heuristic


def propagate_path_improvements(node, map_task):
    """
    :param node: Current node when improving the path.
    :param map_task: Which map to use when improving the path.
    :return: Returns nothing, but updates the weights of nodes along the new shortest path.
    """
    for x in node.children:
        if node.weight + map_task.get_cell_value(x.pos) < x.weight:
            x.parent = node
            attach_and_eval(x, node, map_task)
            propagate_path_improvements(x, map_task)


def backtrack(node, map_task):
    """
    :param node: which node we are currently on. Starts out on the goal node when this has been found
    :param map_task: which map to use when backtracking
    :return: Shows the map with the shortest path marked in yellow
    """
    x = node
    while x.parent is not None:
        map_task.set_cell_value(x.pos, 5)  # Set to 5 to get yellow coloring of path
        x = x.parent
    map_task.show_map()


def main(task):
    """
    :param task: Which task to run
    :return: either shows the map with the shortest path marked in yellow or "Failed" if no path was found.
    """
    map_task = Map.Map_Obj(task=task)
    x, y = best_first_search(map_task)
    try:
        backtrack(x, map_task)
    except AttributeError:
        print("Failed")


# Optional part 3 of the assignment is not done
# Run with 1,2,3 or 4 for each task. The shortest path will be visualized at the end of the run.
main(4)
