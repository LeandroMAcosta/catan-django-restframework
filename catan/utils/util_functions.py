from board.models import Board


def create_test_board(board_data):
    board = Board(**board_data)
    resources = ['desert', 'brick', 'wool']
    tokens = [0, 8, 6, 9, 2, 8, 8, 6, 9, 6, 3, 9, 6, 9, 6, 4, 4, 5, 9]
    board.hexagon_set.create(
        resource=resources[0], token=tokens[0], level=0, index=0)
    i = 1
    for level in range(1, 3):
        for index in range(0, 6*level):
            board.hexagon_set.create(
                resource=resources[level], token=tokens[i], level=level,
                index=index)
            i += 1
    board.save()
    return board
