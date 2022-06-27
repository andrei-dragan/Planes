class Board:
    def __init__(self, size):
        """
        Initialize the board based on a given size
        The board will look like a matrix (a list of lists)
        We will also keep the size
        :param size: The size of the board
        """
        self.__size = size
        self.__data = [[0] * self.__size for i in range(self.__size)]
        """
        0 - the cell does not have a plane covering it and the cell was not yet discovered
        1 - the cell has a plane covering it, but it's not a cabin and it was not yet discovered
        'N' / 'E' / 'S' / 'W' - the cell represents a plane's cabin, indicating also its orientation but also not yet
                                discovered
        'O' - the cell was hit -> but no plane was hit
        'x' - the cell was hit -> and a part of a plane (but not the cabin) was hit as well
        'X' - the cell was hit -> and it's part of a destroyed plane
        """

    def get_size(self):
        """
        Return the size of the board
        :return: The size of the board
        """
        return self.__size

    def get_content_cell(self, x, y):
        """
        Get the content of a cell based on the coordinates
        We will also convert the coordinates into integers and check if they are inside the board
        :return: The content of the cell located at (x,y)
        """

        size = str(self.__size - 1)  # For error handling message purposes

        try:
            x = int(x)
        except ValueError:
            raise CoordinatesException('x coordinate should be an integer between 0 and ' + size + '!')
        if not 0 <= x < self.__size:
            raise CoordinatesException('coordinate out of bounds - x should be between 0 and ' + size + '!')

        try:
            y = int(y)
        except ValueError:
            raise CoordinatesException('y coordinate should be an integer between 0 and ' + size + '!')
        if not 0 <= y < self.__size:
            raise CoordinatesException('coordinate out of bounds - y should be between 0 and ' + size + '!')

        return self.__data[x][y]

    def set_content_cell(self, x, y, value):
        """
        Set the content of a board's cell(represented by its coordinates) based on a given value
        We will also convert the coordinates into integers and check if they are inside the board
        :param x: The x coordinate of the cell
        :param y: The y coordinate of the cell
        :param value: The value of the cell
        :return: None
        """
        size = str(self.__size - 1)  # For error handling message purposes
        try:
            x = int(x)
        except ValueError:
            raise CoordinatesException('x coordinate should be an integer between 0 and ' + size + '!')
        if not 0 <= x < self.__size:
            raise CoordinatesException('coordinate out of bounds - x should be between 0 and ' + size + '!')

        try:
            y = int(y)
        except ValueError:
            raise CoordinatesException('y coordinate should be an integer between 0 and ' + size + '!')
        if not 0 <= y < self.__size:
            raise CoordinatesException('coordinate out of bounds - y should be between 0 and ' + size + '!')

        self.__data[x][y] = value

    def board_won(self):
        """
        Check if the board was won - there are no more plane's cells to be discovered
        :return: True if the board was won, False otherwise
        """
        undiscovered_cells = 0
        for i in range(self.__size):
            for j in range(self.__size):
                value = self.get_content_cell(i, j)
                if value != 'X' and value != 'x' and value != 'O' and value != 0:
                    # There is still a cell having a plane part to be discovered
                    undiscovered_cells += 1

        if undiscovered_cells == 0:
            return True
        return False

    def set_coordinates(self, x, y, orientation):
        """
        Set the cells a plane will cover over the board, based on the cabin's coordinates and the plane's orientation
        :param x: The x coordinate of the cabin
        :param y: The y coordinate of the cabin
        :param orientation: The orientation of the plane
        :return: A list of tuples, which represents the coordinates of each cell covered by a plane
        """
        size = str(self.__size - 1)  # For error handling message purposes

        try:
            x = int(x)
        except ValueError:
            raise CoordinatesException('x coordinate should be an integer between 0 and ' + size + '!')

        try:
            y = int(y)
        except ValueError:
            raise CoordinatesException('y coordinate should be an integer between 0 and ' + size + '!')

        if orientation == 'N':
            return [(x - 1, y), (x, y + 1), (x, y - 1), (x + 1, y), (x + 2, y), (x + 2, y - 1), (x + 2, y + 1)]
        elif orientation == 'E':
            return [(x, y + 1), (x - 1, y), (x + 1, y), (x, y - 1), (x, y - 2), (x - 1, y - 2), (x + 1, y - 2)]
        elif orientation == 'S':
            return [(x + 1, y), (x, y - 1), (x, y + 1), (x - 1, y), (x - 2, y), (x - 2, y - 1), (x - 2, y + 1)]
        elif orientation == 'W':
            return [(x, y - 1), (x - 1, y), (x + 1, y), (x, y + 1), (x, y + 2), (x - 1, y + 2), (x + 1, y + 2)]
        else:
            raise InvalidPlane('The orientation should be only "N" / "E" / "S" / "W"')

    def add_plane(self, x, y, orientation):
        """
        Add a plane on the board based on the coordinates of the cabin and the plane's orientation
        :param x: The x coordinate of the plane's cabin
        :param y: The y coordinate of the plane's cabin
        :param orientation: The orientation of the plane
        :return: None
        """
        plane_coordinates = self.set_coordinates(x, y, orientation)

        cabin_cell_value = self.get_content_cell(x, y)
        if not cabin_cell_value == 0:
            raise InvalidPlane('The plane you chose overlaps another plane!')

        for i in range(len(plane_coordinates)):
            x_plane = plane_coordinates[i][0]
            y_plane = plane_coordinates[i][1]

            try:
                cell_value = self.get_content_cell(x_plane, y_plane)
            except CoordinatesException:
                raise InvalidPlane('The plane you chose goes beyond the board size!')

            if not cell_value == 0:
                raise InvalidPlane('The plane you chose overlaps another plane!')

        self.set_content_cell(x, y, orientation)
        for i in range(len(plane_coordinates)):
            x_plane = plane_coordinates[i][0]
            y_plane = plane_coordinates[i][1]
            self.set_content_cell(x_plane, y_plane, 1)

    def attack_position(self, x, y):
        """
        Attack the (x,y) position on the board
        :param x: The x coordinate of the position that will be attacked
        :param y: The y coordinate of the position that will be attacked
        :return: The message that will be printed in the UI, based on the content of the cell attacked
        """
        cell_value = self.get_content_cell(x, y)
        if cell_value == 'X' or cell_value == 'x' or cell_value == 'O':
            raise CellException('This cell was already attacked!')

        answer = ''

        if cell_value == 0:
            # No part of a plane was attacked
            answer = 'Oh! You have missed!'
            self.set_content_cell(x, y, 'O')
        elif cell_value == 1:
            # A part of the plane was attacked, but not the cabin
            answer = 'You hit something! Keep going!'
            self.set_content_cell(x, y, 'x')
        elif cell_value == 'N' or cell_value == 'S' or cell_value == 'E' or cell_value == 'W':
            # The cabin of a plane was attacked
            answer = 'You took down the whole plane! Good job!'
            plane_coordinates = self.set_coordinates(x, y, cell_value)
            self.set_content_cell(x, y, 'X')
            for i in range(len(plane_coordinates)):
                x_plane = plane_coordinates[i][0]
                y_plane = plane_coordinates[i][1]
                self.set_content_cell(x_plane, y_plane, 'X')

        return answer


class CellException(Exception):
    """
    Exception to be thrown when an invalid cell wants to be attacked
    """
    def __init__(self, *args):
        self.message = args[0]

    def __str__(self):
        return self.message


class InvalidPlane(Exception):
    """
    Exception to be thrown when an invalid plane wants to be added
    """
    def __init__(self, *args):
        self.message = args[0]

    def __str__(self):
        return self.message


class CoordinatesException(Exception):
    """
    Exception to be thrown when an invalid cell from the board is accessed
    """
    def __init__(self, *args):
        self.message = args[0]

    def __str__(self):
        return self.message
