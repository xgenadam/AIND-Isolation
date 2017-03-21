

class Node(object):
    def __init__(self, parent, board, move=None, depth=None, children=None, player=None):
        # print('new node')
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

