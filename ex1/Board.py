class Board(object):

    """
    board - the matrix of board puzzle.
    board_size - the size of the puzzle.
    parent - the parent vertex of board in the search.
    """
    def __init__(self, board, board_size):
        self.board = board
        self.board_size = board_size
        self.parent = None
        self.move = ''

    """
    set the parent to new parent.
    @param - parent - the new parent of current object.
    """
    def set_parent(self, parent):
        self.parent = parent

    """
    set move to be U,D,L,R.
    @param - move: the character that defines U,D,L,R.
    """
    def set_move(self, new_move):
        self.move = new_move

    """
    get x,y position in matrix.
    """
    def get_node(self,x, y):
        for row in self.board:
            if self.board.index(row) == x:
                for node in row:
                    if row.index(node) == y:
                        return node

    """
    object gets other_board and check if their values matrixes match.
    """
    def check_if_boards_match(self, other_board):
        if other_board is None:
            return False
        for x in range(0, self.board_size):
            for y in range(0, self.board_size):
                if self.get_node(x, y) != other_board.get_node(x, y):
                    return False
        return True

    """
    get node and return x, y indexes of node in board.
    @param - node: the node to be checked.
    @returns: x,y: the row, column indexes of node in board.
    """
    def get_node_indexes(self, node):
        for x in range(0, self.board_size):
            for y in range(0, self.board_size):
                if self.get_node(x, y) == node:
                    return x, y
        return self.board_size, self.board_size
