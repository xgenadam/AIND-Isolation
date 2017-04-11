import utils


def heuristic_axis_move_product(game, player):
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

    return up_count * down_count * left_count * right_count * up_left_count * up_right_count * down_left_count * down_right_count


def heuristic_direction_of_movement(game, player):
    raise NotImplementedError('function not complete!')
    player_legal_moves = len(game.get_legal_moves(player))
    location = game.get_player_location(player)
    num_blank_surrounding = 0
    for x, y in utils.Directions2D:
        x_prime = location[0] + x
        y_prime = location[1] + y
        if 0 > x_prime or x_prime >= game.width or \
                        0 > y_prime or y_prime >= game.height:
            try:
                idx = (y_prime * game.height) + x_prime
            except:
                continue
            raise Exception
        num_blank_surrounding += 1
    return float(player_legal_moves + num_blank_surrounding + game.utility(player))


def heuristic_composite(game, player):
    location = game.get_player_location(player)
    board_2d = utils.Game2D(game)
    neighbour_array = utils.NeighbourArray.build_array(board_2d)

    cluster = utils.NeighbourArray.get_location_cluster(
        neighbour_array=neighbour_array,
        location=location, board_width=board_2d.width
    )

    return float(len(game.get_legal_moves(player))) + game.utility(
        player) + len(cluster)


def area_score(game, player):
    location = game.get_player_location(player)
    board_2d = utils.Game2D(game)
    neighbour_array = utils.NeighbourArray.build_array(board_2d)

    cluster = utils.NeighbourArray.get_location_cluster(
        neighbour_array=neighbour_array,
        location=location, board_width=board_2d.width
    )

    return float(len(cluster)) + game.utility(player)


def heuristic_adversarial(game, player, opponent_priority_coeeficient=2):
    num_player_moves = len(game.get_legal_moves(player))
    num_opponent_moves = len(game.get_legal_moves(game.get_opponent(player)))
    return float(num_player_moves
                 - opponent_priority_coeeficient
                 * num_opponent_moves)