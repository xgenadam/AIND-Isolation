import utils


# Simple heuristics
def num_moves(game, player):
    return float(len(game.get_legal_moves(player)))


def axis_move_product(game, player):
    x, y = game.get_player_location(player)

    up_count = 1
    for offset in range(game.height - y):
        if not game.move_is_legal(move=[x, y + offset]):
            break
        up_count += 1

    down_count = 1
    for offset in range(y):
        if not game.move_is_legal(move=[x, y - offset]):
            break
        down_count += 1

    left_count = 1
    for offset in range(x):
        if not game.move_is_legal(move=[x - offset, y]):
            break
        left_count += 1

    right_count = 1
    for offset in range(game.width - x):
        if not game.move_is_legal(move=[x + offset, y]):
            break
        right_count += 1

    up_left_count = 1
    for offset_x, offset_y in zip(range(x), range(game.height - y)):
       if not game.move_is_legal(move=[x - offset_x, y + offset_y]):
           break
       up_left_count += 1

    up_right_count = 1
    for offset_x, offset_y in zip(range(game.width - x), range(game.height - y)):
        if not game.move_is_legal(move=[x + offset_x, y + offset_y]):
            break
        up_right_count += 1

    down_left_count = 1
    for offset_x, offset_y in zip(range(x), range(y)):
        if not game.move_is_legal(move=[x - offset_x, y - offset_y]):
            break
        down_left_count += 1

    down_right_count = 1
    for offset_x, offset_y in zip(range(game.width -x), range(y)):
        if not game.move_is_legal(move=[x + offset_x, y - offset_y]):
            break
        down_right_count += 1

    return float(up_count * down_count * left_count * right_count * up_left_count * up_right_count * down_left_count * down_right_count)


def axis_movement(game, player):
    # Yeah this function is a bit shit but Im desperately lacking sleep and this is working
    # if there is time I will tidy it up but and make it presentable. (its a big if!)
    x, y = game.get_player_location(player)

    num_axis_available = 0
    for direction in utils.Directions2D.values():
        x_prime = x + direction[0]
        y_prime = y + direction[1]
        if game.move_is_legal(move=[x_prime, y_prime]):
            num_axis_available += 1


    return float(num_axis_available/8.0 * len(game.get_legal_moves(player)))


def area_score(game, player):
    location = game.get_player_location(player)
    board_2d = utils.Game2D(game)
    neighbour_array = utils.NeighbourArray.build_array(board_2d)

    cluster = utils.NeighbourArray.get_location_cluster(
        neighbour_array=neighbour_array,
        location=location, board_width=board_2d.width
    )

    return float(len(cluster))


# adversarial heuristics
def adversarial_move_len(game, player, opponent_priority_coeeficient=3.0):
    num_player_moves = len(game.get_legal_moves(player))
    num_opponent_moves = len(game.get_legal_moves(game.get_opponent(player)))
    return float(num_player_moves
                 - opponent_priority_coeeficient
                 * num_opponent_moves)


def area_score_adversarial(game, player, opponent_priority_coefficient=1.0):
    opponent = game.get_opponent(player)

    return (area_score(game, player)
            - opponent_priority_coefficient
            * area_score(game, opponent))


def axis_move_product_adversarial(game, player, opponent_priority_coefficient=2.0):
    opponent = game.get_opponent(player)

    return axis_move_product(game, player) \
           - opponent_priority_coefficient * axis_move_product(game, opponent)


def axis_movement_adversarial(game, player, opponent_priority_coefficient=4.0):
    opponent = game.get_opponent(player)
    return (axis_movement(game, player)
            - opponent_priority_coefficient
            * axis_movement(game, opponent))


# composite methods
def area_score_move_len_adversarial(game, player, opponent_priority_coefficient=2.0):
    return area_score_adversarial(game, player) \
           - adversarial_move_len(game, player, opponent_priority_coefficient)