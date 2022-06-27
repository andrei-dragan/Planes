import random
from board.board import InvalidPlane


class AI:
    def __init__(self, size, planes):
        """
        Initialize the computer's game behaviour
        :param size: The size of the board
        :param planes: The number of planes to be placed on the board
        """
        self.__size = size
        self.__planes = planes

    def choose_planes(self, board):
        """
        Make the computer randomly choose and place all the plane's cabins
        :param board: The computer's board
        :return: None
        """
        size = self.__size
        for i in range(self.__planes):
            while True:
                x = random.randrange(size)
                y = random.randrange(size)
                orientation = random.choice(('N', 'S', 'E', 'W'))
                try:
                    board.add_plane(x, y, orientation)
                    break
                except InvalidPlane:
                    pass

    def computer_attack(self, board):
        """
        Make the computer choose an optimal move and attack that position
        :param board: The player's board
        :return: None
        """
        hit_grade = [[0] * self.__size for i in range(self.__size)]  # every cell has the same priority
        max_grade = 0

        for i in range(self.__size):
            for j in range(self.__size):
                if board.get_content_cell(i, j) == 'x':
                    # All the surrounding columns and rows have greater priority
                    if i + 1 < self.__size and board.get_content_cell(i + 1, j) != 'X' \
                            and board.get_content_cell(i + 1, j) != 'O' and board.get_content_cell(i + 1, j) != 'x':
                        hit_grade[i + 1][j] += 1
                        if hit_grade[i + 1][j] > max_grade:
                            max_grade = hit_grade[i + 1][j]

                    if i - 1 > 0 and board.get_content_cell(i - 1, j) != 'X' \
                            and board.get_content_cell(i - 1, j) != 'O' and board.get_content_cell(i - 1, j) != 'x':
                        hit_grade[i - 1][j] += 1
                        if hit_grade[i - 1][j] > max_grade:
                            max_grade = hit_grade[i - 1][j]

                    if j + 1 < self.__size and board.get_content_cell(i, j + 1) != 'X' \
                            and board.get_content_cell(i, j + 1) != 'O' and board.get_content_cell(i, j + 1) != 'x':
                        hit_grade[i][j + 1] += 1
                        if hit_grade[i][j + 1] > max_grade:
                            max_grade = hit_grade[i][j + 1]

                    if j - 1 > 0 and board.get_content_cell(i, j - 1) != 'X' \
                            and board.get_content_cell(i, j - 1) != 'O' and board.get_content_cell(i, j - 1) != 'x':
                        hit_grade[i][j - 1] += 1
                        if hit_grade[i][j - 1] > max_grade:
                            max_grade = hit_grade[i][j - 1]

        hits = []
        for i in range(self.__size):
            for j in range(self.__size):
                if hit_grade[i][j] == max_grade and board.get_content_cell(i, j) != 'X' \
                        and board.get_content_cell(i, j) != 'O' and board.get_content_cell(i, j) != 'x':
                    hits.append((i, j))

        # We choose randomly from hits
        x, y = random.choice(hits)
        board.attack_position(x, y)
