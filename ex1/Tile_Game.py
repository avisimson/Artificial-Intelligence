from Board import Board
from heapq import heappush, heappop


class TileGame(object):

    """
    cost- the cost of algorithm running.
    nodes_developed - number of nodes poped from open list.
    route- the route to solution of puzzle.
    board- the board game of puzzle.
    board_size - size of the puzzle.
    blank- x,y of 0 in puzzle.
    goal_state- the goal state we look for in tile puzzle.
    """
    def __init__(self, board, board_size, blank):
        self.cost = int(0)
        self.nodes_developed = int(0)
        self.route = ""
        self.board = Board(board, board_size)
        self.open_list = [self.board]
        self.blank = blank
        self.goal_state = self.get_goal_state()

    """
    @returns- the goal state of board puzzle.
    """
    def get_goal_state(self):
        goal = Board([], self.board.board_size)
        value = int(1)
        for x in range(0, self.board.board_size):
            row = []
            for y in range(0, self.board.board_size):
                if (x == self.board.board_size - 1) and y == (self.board.board_size - 1):
                    row.append(int(0))
                    break
                row.append(value)
                value = value + 1
            goal.board.append(row)
        return goal


    """
    check if board is in goal state.
    @param: the current board and the size of board.
    @returns: true if board is in goal state, false if not.
    """
    def check_if_goal(self, board, board_size):
        for x in range(0, board_size):
            for y in range(0, board_size):
                if x == (board_size - 1) and y == (board_size - 1) and board.get_node(x, y) == int(0):
                    return True
                if board.get_node(x, y) != int((x * board_size) + y + 1):
                    return False
        return True


    """
    copy one board values to another.
    @param: source is the board to be copied, copy is the copy of source.
    """
    def copy_board(self, source, copy):
        for x in range(0, self.board.board_size):
            row = []
            for y in range(0, self.board.board_size):
                row.append(source.get_node(x, y))
            copy.board.append(row)


    """
    get all possible sons of board from current board without its parent.
    @param: the current board.
    @return: list of all possible son boards.
    """
    def get_sons(self, current_board):
        sons = []
        left_son = Board([], self.board.board_size)
        right_son = Board([], self.board.board_size)
        up_son = Board([], self.board.board_size)
        down_son = Board([], self.board.board_size)
        # update all sons parent.
        up_son.set_parent(current_board)
        down_son.set_parent(current_board)
        left_son.set_parent(current_board)
        right_son.set_parent(current_board)
        # update moves to sons.
        up_son.set_move('U')
        down_son.set_move('D')
        left_son.set_move('L')
        right_son.set_move('R')

        # handling up son possibility.
        if self.blank[0] < (self.board.board_size - 1):
            self.copy_board(current_board, up_son)
            up_son.board[self.blank[0]][self.blank[1]] = up_son.board[self.blank[0] + 1][self.blank[1]]
            up_son.board[self.blank[0] + 1][self.blank[1]] = int(0)
            sons.append(up_son)

        # handling down son possibility.
        if self.blank[0] > 0:
            self.copy_board(current_board, down_son)
            down_son.board[self.blank[0]][self.blank[1]] = down_son.board[self.blank[0] - 1][self.blank[1]]
            down_son.board[self.blank[0] - 1][self.blank[1]] = int(0)
            sons.append(down_son)

        # handling left son possibility.
        if self.blank[1] < (self.board.board_size - 1):
            self.copy_board(current_board, left_son)
            left_son.board[self.blank[0]][self.blank[1]] = left_son.board[self.blank[0]][self.blank[1] + 1]
            left_son.board[self.blank[0]][self.blank[1] + 1] = int(0)
            sons.append(left_son)

        # handling right son possibility.
        if self.blank[1] > 0:
            self.copy_board(current_board, right_son)
            right_son.board[self.blank[0]][self.blank[1]] = right_son.board[self.blank[0]][self.blank[1] - 1]
            right_son.board[self.blank[0]][self.blank[1] - 1] = int(0)
            sons.append(right_son)
        return sons

    """
    Update the blank placement in current grid.
    @param: current_board- the current state of board.
    """
    def update_blank(self, current_board):
        for x in range(0, self.board.board_size):
            for y in range(0, self.board.board_size):
                if current_board.get_node(x, y) == 0:
                    self.blank[0] = int(x)
                    self.blank[1] = int(y)
                    return

    """
    set route from initial board state to current board state.
    @:param: current_board - the current state of the board.
    @returns - the route from initial to current state as a string.
    """
    def set_route(self, current_board):
        solution = ""
        while current_board.parent is not None:
            solution = current_board.move + solution
            current_board = current_board.parent
        return solution

    """
    running bfs algorithm on board until reaching goal state.
    """
    def run_bfs_search(self):
        while len(self.open_list):
            self.nodes_developed = self.nodes_developed + 1
            current_board = self.open_list.pop(0)
            self.update_blank(current_board)
            if self.check_if_goal(current_board, self.board.board_size):
                self.route = self.set_route(current_board)
                return
            else:
                sons = self.get_sons(current_board)
                for son in sons:
                    i = 0
                    for node in self.open_list:
                        if son.check_if_boards_match(node):
                            break
                        i = i + 1
                    if i == len(self.open_list):
                        self.open_list.append(son)

    """
    run single iteration of ids algorithm.
    @param - current_board: the current board being taken care of. depth: the depth of algorithm to run.
    @returns - True if goal state found or False if not.
    """
    def ids_single_run(self, current_board, depth):
        self.update_blank(current_board)
        self.nodes_developed = self.nodes_developed + 1
        if depth == 0:
            if self.check_if_goal(current_board, self.board.board_size):
                self.route = self.set_route(current_board)
                return True
            else:  # dead end for this iteration.
                return False
        else:  # depth > 0
            sons = self.get_sons(current_board)
            for son in sons:
                if self.ids_single_run(son, depth - 1):
                    return True


    """
    running ids algorithm on board until reaching goal state.
    """
    def run_ids_search(self):
        depth = int(0)
        while not self.ids_single_run(self.board, depth):
            depth = depth + 1
            self.nodes_developed = int(0)
        self.cost = depth

    """
    get board and node and check the manhatten distance of node in board
    from node in goal board.
    @param- node: the node to be checked. board: the board to check distance from.
    @return- the manhatten distance of node.
    """
    def distance_of_node(self, node, board):
        distance = 0
        x_goal, y_goal = self.goal_state.get_node_indexes(node)
        for x in range(0, self.board.board_size):
            for y in range(0, self.board.board_size):
                if board.get_node(x, y) == node:
                    distance = int(abs(x_goal - x) + abs(y_goal - y))
                    return distance
        return distance



    """
    Run heuristic function evaluation - manhatten distance
    @param- current_board: board to check distance from to goal board.
    @returns- the manhatten distance.
    """
    def heuristic_function(self, current_board):
        num_of_nodes = int((self.board.board_size * self.board.board_size) - 1)
        manhatten_distance = int(0)
        for x in range(1, num_of_nodes + 1):
            manhatten_distance = manhatten_distance + self.distance_of_node(x, current_board)
        return manhatten_distance

    """
    run a-star algorithm until reaching goal state.
    """
    def run_a_star_search(self):
        self.open_list = []
        place = int(0)
        heappush(self.open_list, (self.heuristic_function(self.board), place, self.board))
        while len(self.open_list):
            self.nodes_developed = self.nodes_developed + 1
            current_board = heappop(self.open_list)[2]
            self.update_blank(current_board)
            if self.check_if_goal(current_board, self.board.board_size):
                self.route = self.set_route(current_board)
                self.cost = len(self.route)
                return
            else:
                sons = self.get_sons(current_board)
                for son in sons:
                    place = place + 1
                    heappush(self.open_list, (self.heuristic_function(son) + len(self.set_route(son)), place, son))
