import numpy as np

from isolation import Board


Directions2D = {
    'UP': np.array([1, 0], dtype=int),
    'DOWN': np.array([-1, 0], dtype=int),
    'LEFT': np.array([0, -1], dtype=int),
    'RIGHT': np.array([0, 1], dtype=int),
    'UP_LEFT': np.array([1, -1], dtype=int),
    'UP_RIGHT': np.array([1, 1], dtype=int),

    'DOWN_LEFT': np.array([-1, -1], dtype=int),
    'DOWN_RIGHT': np.array([-1, 1], dtype=int)
}


class Game2D(object):
    BLANK = Board.BLANK

    def __init__(self, game):
        board = np.zeros(shape=(game.height, game.width), dtype=int)
        for y in range(game.height):
            for x in range(game.width):
                cell_idx = y * game.width + x
                board[y][x] = game._board_state[cell_idx]

        self.board = board
        self.width = game.width
        self.height = game.height

    @staticmethod
    def get_grid_from_1d_index(idx, board_width):
        row = idx % board_width
        col = idx // board_width
        return row, col

    @staticmethod
    def get_1d_idx_from_grid(grid, board_width):
        row, col = grid
        return col * board_width + row


class NeighbourArray(object):

    @staticmethod
    def build_array(array_2d, grouping=None):
        height, width = array_2d.board.shape
        num_cells = height * width
        neighbour_array = np.zeros(shape=(num_cells, num_cells), dtype=int)
        if grouping is None:
            comp_val = Game2D.BLANK
        else:
            comp_val = grouping
        count = 0
        locations = set()
        for y_1 in range(height):
            for x_1 in range(width):
                cell_1_val = array_2d.board[y_1][x_1]
                if cell_1_val != comp_val:
                    continue
                cell_1_idx = y_1 * width + x_1
                for delta_y in [-1, 0, 1]:
                    y_2 = y_1 + delta_y
                    if 0 <= y_2 < height:
                        for delta_x in [-1, 0, 1]:
                            x_2 = x_1 + delta_x
                            # try:
                            if 0 <= x_2 < width:
                                if array_2d.board[y_2][x_2] == comp_val:
                                    cell_2_idx = y_2 * width + x_2
                                    neighbour_array[cell_1_idx][cell_2_idx] = 1
                                    locations.update([(cell_2_idx, cell_1_idx)])
                                    count += 1
        return neighbour_array

    @staticmethod
    def get_location_cluster(neighbour_array, location, board_width,
                             array_shape=None, cluster=None):
        if cluster is None:
            cluster = set()

        if array_shape is None:
            array_shape = neighbour_array.shape

        location_idx = Game2D.get_1d_idx_from_grid(location, board_width)
        row = neighbour_array[location_idx]

        neighbours = NeighbourArray._get_relevant_neighbours(row)

        neighbour_locations = NeighbourArray._get_neighbour_locations(neighbours, cluster, board_width)

        cluster.update(neighbour_locations)

        for neighbour_location in neighbour_locations:
            NeighbourArray.get_location_cluster(
                neighbour_array=neighbour_array,
                location=neighbour_location,
                board_width=board_width,
                array_shape=array_shape,
                cluster=cluster)

        return cluster

    @staticmethod
    def _get_relevant_neighbours(row):
        relevant_neighbours = [(idx, val) for (idx, val) in enumerate(row)
                               if val == 1]
        return relevant_neighbours

    @staticmethod
    def _get_neighbour_locations(neighbours, cluster, board_width):
        neighbour_locations = [Game2D.get_grid_from_1d_index(idx, board_width)
                               for (idx, val) in neighbours]

        neighbour_locations = [location for location in neighbour_locations if
                               location not in cluster]

        return neighbour_locations

class Node(object):
    def __init__(self, parent, board, move=None, depth=None, children=None, player=None):
        self.parent = parent
        if self.parent is not None:
            self.parent.children.append(self)
        self.children = children if children else []
        self.utility = None
        self.minimax_score = None
        self.board = board
        self.move = move
        self.optimal_move = None
        self.board_score = None
        if depth is not None:
            self.depth = depth
        elif self.parent is not None:
            self.depth = self.parent.depth + 1
        else:
            self.depth = 0
        self.node_list = self.parent.node_list if self.parent is not None else []
        self.node_list.append(self)
        self.active_player = self.board.active_player

    def maximin(self, maximize=True):

        for child in self.children:
            child.maximin(not maximize)

        if maximize is True:
            score_func = max
        else:
            score_func = min

        if self.children:
            score_children_list = list(map(lambda child: (child.score, child), self.children))

            optimal_score = score_func(map(lambda score_child: score_child[0], score_children_list))

            for score, child in score_children_list:
               if score == optimal_score:
                   break

            assert child.score == optimal_score
            self.optimal_move = child.move
            self.minimax_score = optimal_score


    @property
    def score(self):
        if self.utility is not None:
            return self.utility

        return self.minimax_score


def next_moveset(layer):
    new_layer = []

    print("num nodes in layer: {}".format(len(layer)))
    for node in layer:
        # assert new_layer is layer
        # import pdb; pdb.set_trace()
        legal_moves = node.board.get_legal_moves(node.active_player)
        # print("num moves in node {}".format(len(legal_moves)))
        for move in legal_moves:
            board_copy = node.board.forecast_move(move)
            new_node = Node(parent=node, board=board_copy, move=move)
            new_layer.append(new_node)
    return new_layer
