from Tile_Game import TileGame
import sys

"""
read from input file the search algorithm,
the size of the board and the elements in the board.
@param- file_name = the name of the file we read from.
@returns - the algorithm type, the size of the board, the board, and the x,y indexes of the blank place.
"""


def read_from_file(file_name):
    try:
        blank_x = int(0)
        blank_y = int(0)
        board = []
        input_file = open(file_name, 'r')
        algo_type = int(input_file.readline())
        board_size = int(input_file.readline())
        info = input_file.readline().split('-')
        i = 0
        for x in range(0, board_size):
            row = []
            for y in range(0, board_size):
                row.append(int(info[i]))
                if int(info[i]) == 0:
                    blank_x = int(x)
                    blank_y = int(y)
                i = i + 1
            board.append(row)
        input_file.close()
        blank = [blank_x, blank_y]
    except IOError:
        # couldn't read file parameters, abort.
        print ('Error in file input parameters.')
        sys.exit(0)
    return algo_type, board_size, board, blank


"""
writing to output file the algorithm results.
@param: route-the route to solution of puzzle, nodes_developed-the number of pops from open list,
cost- the cost of algorithm.
"""


def write_to_output_file(route, nodes_developed, cost):
    try:
        output_file = open("output.txt", 'w')
        output_file.write(route + ' ')
        output_file.write(str(nodes_developed) + ' ')
        output_file.write(str(cost))
    except IOError:
        # couldn't write file parameters, abort.
        print ('Error in file output file handling.')
        sys.exit(0)


"""
implement the right algorithm search according to type parameter.
@:param: algo_type - int type of the algorithm required, tile_game- the game.
@returns- route-the route to solution of puzzle, nodes_developed-the number of pops from open list,
cost- the cost of algorithm.
"""


def algorithm_choosing(algo_type, tile_game):
    if algo_type < 1 or algo_type > 3:
        print ("wrong type of algorithm, exit")
        sys.exit(0)
    if algo_type == 1:
        tile_game.run_ids_search()
    elif algo_type == 2:
        tile_game.run_bfs_search()
    elif algo_type == 3:
        tile_game.run_a_star_search()
    return tile_game.route, tile_game.cost, tile_game.nodes_developed


def main():
    # read input from input file.
    algo_type, board_size, board, blank = read_from_file("input.txt")

    # initialize the game.
    tile_game = TileGame(board, board_size, blank)

    # implementing the right algorithm.
    route, cost, nodes_developed = algorithm_choosing(algo_type, tile_game)

    # write solution to output file.
    write_to_output_file(route, nodes_developed, cost)


if __name__ == '__main__':
    main()
