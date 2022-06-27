import unittest

from ai.ai import AI
from board.board import Board, CoordinatesException, InvalidPlane, CellException


class TestEntity(unittest.TestCase):
    def setUp(self):
        self.__playerBoard = Board(5)
        self.__aiBoard = Board(5)
        self.__ai = AI(5, 1)

    def test_computer_choose_planes(self):
        self.__ai.choose_planes(self.__aiBoard)
        cabins = 0
        x_cabin = 0
        y_cabin = 0
        orientation = ''
        for i in range(5):
            for j in range(5):
                if self.__aiBoard.get_content_cell(i, j) == 'N' \
                        or self.__aiBoard.get_content_cell(i, j) == 'E' \
                        or self.__aiBoard.get_content_cell(i, j) == 'S' \
                        or self.__aiBoard.get_content_cell(i, j) == 'W':
                    cabins += 1
                    x_cabin = i
                    y_cabin = j
                    orientation = self.__aiBoard.get_content_cell(i, j)

        self.assertEqual(cabins, 1)

        plane_coordinate = self.__aiBoard.set_coordinates(x_cabin, y_cabin, orientation)
        for i in range(len(plane_coordinate)):
            x = plane_coordinate[i][0]
            y = plane_coordinate[i][1]
            self.assertEqual(self.__aiBoard.get_content_cell(x, y), 1)

    def test_computer_attack(self):
        self.__playerBoard.add_plane(1, 2, 'E')
        self.__playerBoard.attack_position(0, 2)
        self.__playerBoard.attack_position(2, 2)
        self.__playerBoard.attack_position(1, 1)
        self.__playerBoard.attack_position(1, 3)

        self.__ai.computer_attack(self.__playerBoard)
        self.assertEqual(self.__playerBoard.get_content_cell(1, 2), 'X')

    def tearDown(self):
        pass
