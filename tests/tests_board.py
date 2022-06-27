import unittest
from board.board import Board, CoordinatesException, InvalidPlane, CellException


class TestEntity(unittest.TestCase):
    def setUp(self):
        self.__b = Board(5)

    def test_initialization(self):
        self.assertEqual(self.__b.get_content_cell(3, 3), 0)

    def test_get_size(self):
        self.assertEqual(self.__b.get_size(), 5)

    def test_get_content_cell(self):
        size = str(5 - 1)
        self.assertEqual(self.__b.get_content_cell(3, 3), 0)

        try:
            self.__b.get_content_cell('A', 3)
            self.assertEqual(True, False)
        except CoordinatesException as ce:
            self.assertEqual(str(ce), 'x coordinate should be an integer between 0 and ' + size + '!')

        try:
            self.__b.get_content_cell(3, 'B')
            self.assertEqual(True, False)
        except CoordinatesException as ce:
            self.assertEqual(str(ce), 'y coordinate should be an integer between 0 and ' + size + '!')

        try:
            self.__b.get_content_cell(3, -2)
            self.assertEqual(True, False)
        except CoordinatesException as ce:
            self.assertEqual(str(ce), 'coordinate out of bounds - y should be between 0 and ' + size + '!')

        try:
            self.__b.get_content_cell(11, 0)
            self.assertEqual(True, False)
        except CoordinatesException as ce:
            self.assertEqual(str(ce), 'coordinate out of bounds - x should be between 0 and ' + size + '!')

    def test_set_content_cell(self):
        size = str(5 - 1)
        self.__b.set_content_cell(3, 3, 1)
        self.assertEqual(self.__b.get_content_cell(3, 3), 1)

        try:
            self.__b.set_content_cell('A', 3, 0)
            self.assertEqual(True, False)
        except CoordinatesException as ce:
            self.assertEqual(str(ce), 'x coordinate should be an integer between 0 and ' + size + '!')

        try:
            self.__b.set_content_cell(3, 'B', 0)
            self.assertEqual(True, False)
        except CoordinatesException as ce:
            self.assertEqual(str(ce), 'y coordinate should be an integer between 0 and ' + size + '!')

        try:
            self.__b.set_content_cell(3, -2, 0)
            self.assertEqual(True, False)
        except CoordinatesException as ce:
            self.assertEqual(str(ce), 'coordinate out of bounds - y should be between 0 and ' + size + '!')

        try:
            self.__b.set_content_cell(11, 0, 0)
            self.assertEqual(True, False)
        except CoordinatesException as ce:
            self.assertEqual(str(ce), 'coordinate out of bounds - x should be between 0 and ' + size + '!')

    def test_board_won(self):
        self.assertEqual(self.__b.board_won(), True)

        self.__b.set_content_cell(1, 2, 1)
        self.assertEqual(self.__b.board_won(), False)

        self.__b.set_content_cell(1, 3, 'N')
        self.assertEqual(self.__b.board_won(), False)

        self.__b.set_content_cell(1, 2, 'X')
        self.__b.set_content_cell(1, 3, 'X')
        self.assertEqual(self.__b.board_won(), True)

    def test_set_coordinates(self):
        size = str(5 - 1)
        try:
            self.__b.set_coordinates('A', 0, 'N')
            self.assertEqual(True, False)
        except CoordinatesException as ce:
            self.assertEqual(str(ce), 'x coordinate should be an integer between 0 and ' + size + '!')

        try:
            self.__b.set_coordinates(0, 'A', 'N')
            self.assertEqual(True, False)
        except CoordinatesException as ce:
            self.assertEqual(str(ce), 'y coordinate should be an integer between 0 and ' + size + '!')

        try:
            self.__b.set_coordinates(0, 0, 'Q')
            self.assertEqual(True, False)
        except InvalidPlane as ip:
            self.assertEqual(str(ip), 'The orientation should be only "N" / "E" / "S" / "W"')

        self.assertEqual(self.__b.set_coordinates(1, 2, 'E'),
                         [(1, 3), (0, 2), (2, 2), (1, 1), (1, 0), (0, 0), (2, 0)])

        self.assertEqual(self.__b.set_coordinates(1, 1, 'W'),
                         [(1, 0), (0, 1), (2, 1), (1, 2), (1, 3), (0, 3), (2, 3)])

        self.assertEqual(self.__b.set_coordinates(2, 1, 'S'),
                         [(3, 1), (2, 0), (2, 2), (1, 1), (0, 1), (0, 0), (0, 2)])

        self.assertEqual(self.__b.set_coordinates(1, 1, 'N'),
                         [(0, 1), (1, 2), (1, 0), (2, 1), (3, 1), (3, 0), (3, 2)])

    def test_add_plane(self):
        self.__b.add_plane(1, 2, 'E')
        self.assertEqual(self.__b.get_content_cell(1, 3), 1)
        self.assertEqual(self.__b.get_content_cell(1, 2), 'E')

        try:
            self.__b.add_plane(4, 4, 'N')
            self.assertEqual(True, False)
        except InvalidPlane as ip:
            self.assertEqual(str(ip), 'The plane you chose goes beyond the board size!')

        try:
            self.__b.add_plane(1, 1, 'W')
            self.assertEqual(True, False)
        except InvalidPlane as ip:
            self.assertEqual(str(ip), 'The plane you chose overlaps another plane!')

        try:
            self.__b.add_plane(2, 3, 'E')
            self.assertEqual(True, False)
        except InvalidPlane as ip:
            self.assertEqual(str(ip), 'The plane you chose overlaps another plane!')

    def test_attack_position(self):
        self.__b.add_plane(1, 2, 'E')

        self.__b.attack_position(1, 3)
        self.assertEqual(self.__b.get_content_cell(1, 3), 'x')

        self.__b.attack_position(0, 1)
        self.assertEqual(self.__b.get_content_cell(0, 1), 'O')

        self.__b.attack_position(1, 2)
        self.assertEqual(self.__b.get_content_cell(1, 3), 'X')
        self.assertEqual(self.__b.board_won(), True)

        try:
            self.__b.attack_position(1, 2)
            self.assertEqual(True, False)
        except CellException as ce:
            self.assertEqual(str(ce), 'This cell was already attacked!')

    def tearDown(self):
        pass
