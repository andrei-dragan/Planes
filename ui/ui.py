from texttable import Texttable

from ai.ai import AI
from board.board import Board, CoordinatesException, InvalidPlane, CellException

import PySimpleGUI as sg


class UI:
    def __init__(self, size, planes, interface):
        self.__size = size
        self.__planes = planes

        self.__playerBoard = Board(size)
        self.__aiBoard = Board(size)

        self.__ai = AI(size, planes)

        self.__interface = interface

    ###############################################
    #           Welcome Message Console           #
    ###############################################
    def welcome(self):
        print("Welcome to Planes!")
        print("The computer already chose his planes, now it's your turn! "
              "Choose " + str(self.__planes) + " cells to place your plane's cabins!")
        print("Keep in mind that the board's size is " + str(self.__size) + "X" + str(self.__size))
        print("-------------------------------------------------")

    ###############################################
    #             Welcome Message GUI             #
    ###############################################
    def welcome_gui(self):
        welcome_layout = [[sg.Text('Welcome to planes!')],
                          [sg.Text("The computer already chose his planes, now it's your turn! "
                                   "Choose " + str(self.__planes) + " cells to place your plane's cabins!")],
                          [sg.Text("Keep in mind that the board's size is " +
                                   str(self.__size) + "X" + str(self.__size))],
                          [sg.Button("Let's Choose!")]]
        window = sg.Window('PLANES!', welcome_layout)
        while True:
            event, values = window.read()
            if event == sg.WIN_CLOSED:
                exit()
            elif event == "Let's Choose!":
                window.close()
                break

    ###############################################
    #            Choose Cabin Console             #
    ###############################################
    def print_choice_board(self, board):
        t = Texttable(max_width=1000)

        header_row = ['/']
        for i in range(self.__size):
            header_row.append(i)
        t.header(header_row)

        for i in range(self.__size):
            display_row = [i]
            for j in range(self.__size):
                value = board.get_content_cell(i, j)
                if value == 0:
                    display_row.append(' ')
                else:
                    display_row.append('P')
            t.add_row(display_row)
        return t.draw()

    def choose_plane(self, chosen_plane):
        print("This is your board:\n")
        print(self.print_choice_board(self.__playerBoard))
        print("--------------------------------------------------------------")
        print("Choose plane number " + str(chosen_plane))

        x = input("Choose the x coordinate of the cabin: ")
        y = input("Choose the y coordinate of the cabin: ")
        orientation = input("Choose the orientation of the plane - N / E / S / W: ")

        return x, y, orientation

    ###############################################
    #            Choose Cabin GUI                 #
    ###############################################
    def choose_cabin_gui(self, chosen_plane):
        layout = [[sg.Text('This is your board:')], [sg.Text("Choose plane number " + str(chosen_plane))]]

        for i in range(self.__size):
            layout_row = []
            for j in range(self.__size):
                value = self.__playerBoard.get_content_cell(i, j)
                if value == 0:
                    layout_row.append(sg.Button(' ', size=(4, 2), key=(i, j), pad=(0, 0)))
                else:
                    layout_row.append(sg.Button('P', size=(4, 2), key=(i, j), pad=(0, 0)))
            layout.append(layout_row)

        window = sg.Window('PLANES!', layout)
        while True:
            event, values = window.read()
            if event == sg.WIN_CLOSED:
                exit()
            else:
                window.close()
                return event[0], event[1]

    @staticmethod
    def choose_orientation_gui(chosen_plane):
        layout = [[sg.Text('Now choose the orientation for plane ' + str(chosen_plane))]]

        layout_row = [sg.Button('N', size=(4, 2), key='N', pad=(0, 0)),
                      sg.Button('E', size=(4, 2), key='E', pad=(0, 0)),
                      sg.Button('S', size=(4, 2), key='S', pad=(0, 0)),
                      sg.Button('W', size=(4, 2), key='W', pad=(0, 0))]
        layout.append(layout_row)

        window = sg.Window('PLANES!', layout)
        while True:
            event, values = window.read()
            if event == sg.WIN_CLOSED:
                exit()
            else:
                window.close()
                return event[0]

    ###############################################
    #           Simple Message GUI                #
    ###############################################
    @staticmethod
    def simple_message_gui(message):
        layout = [[sg.Text(message)],
                  [sg.Button('ok')]]

        window = sg.Window('PLANES!', layout)
        while True:
            event, values = window.read()
            if event == sg.WIN_CLOSED:
                exit()
            else:
                window.close()
                return event[0]

    ###############################################
    #            Attack Move Console              #
    ###############################################
    def print_boards(self, board1, board2):
        t = Texttable(max_width=1000)

        header_row = ['/']
        for i in range(self.__size):
            header_row.append(i)

        for i in range(self.__size):
            header_row.append(' ')

        for i in range(self.__size):
            header_row.append(i)

        t.header(header_row)

        for i in range(self.__size):
            display_row = [i]
            for j in range(self.__size):
                value = board1.get_content_cell(i, j)
                if value != 'X' and value != 'O' and value != 'x':
                    display_row.append(' ')
                else:
                    display_row.append(value)

            for j in range(self.__size):
                display_row.append(chr(143))

            for j in range(self.__size):
                value = board2.get_content_cell(i, j)
                if value != 'X' and value != 'O' and value != 'x':
                    display_row.append(' ')
                else:
                    display_row.append(value)

            t.add_row(display_row)
        return t.draw()

    def print_boards_attack(self):
        print("--------------------------------------------------------------")
        print('The left one is yours. The right one is the one of your enemy!')
        print(self.print_boards(self.__playerBoard, self.__aiBoard))
        print('--------------------------------------------------------------')
        print("Choose your position to attack.")

    ###############################################
    #              Attack Move GUI                #
    ###############################################
    def print_boards_attack_gui(self):
        layout = [[sg.Text('The left one is yours. The right one is the one of your enemy!')],
                  [sg.Text('Choose your position to attack.')]]

        for i in range(self.__size):
            layout_row = []
            for j in range(self.__size):
                value = self.__playerBoard.get_content_cell(i, j)
                if value != 'X' and value != 'O' and value != 'x':
                    layout_row.append(sg.Button(' ', disabled=True, size=(4, 2), pad=(0, 0)))
                else:
                    layout_row.append(sg.Button(value, disabled=True, size=(4, 2), pad=(0, 0)))

            for j in range(self.__size):
                layout_row.append(sg.Text(' ', size=(4, 2), pad=(0, 0)))

            for j in range(self.__size):
                value = self.__aiBoard.get_content_cell(i, j)
                if value != 'X' and value != 'O' and value != 'x':
                    layout_row.append(sg.Button(' ', size=(4, 2), key=(i, j), pad=(0, 0)))
                else:
                    layout_row.append(sg.Button(value, size=(4, 2), key=(i, j), pad=(0, 0)))

            layout.append(layout_row)

        window = sg.Window('PLANES!', layout)
        while True:
            event, values = window.read()
            if event == sg.WIN_CLOSED:
                exit()
            else:
                window.close()
                return event[0], event[1]

    ###############################################
    #             Print Boards GUI                #
    ###############################################
    def print_boards_gui(self, message):
        layout = [[sg.Text(message)]]

        for i in range(self.__size):
            layout_row = []
            for j in range(self.__size):
                value = self.__playerBoard.get_content_cell(i, j)
                if value != 'X' and value != 'O' and value != 'x':
                    layout_row.append(sg.Button(' ', disabled=True, size=(4, 2), pad=(0, 0)))
                else:
                    layout_row.append(sg.Button(value, disabled=True, size=(4, 2), pad=(0, 0)))

            for j in range(self.__size):
                layout_row.append(sg.Text(' ', size=(4, 2), pad=(0, 0)))

            for j in range(self.__size):
                value = self.__aiBoard.get_content_cell(i, j)
                if value != 'X' and value != 'O' and value != 'x':
                    layout_row.append(sg.Button(' ', disabled=True, size=(4, 2), key=(i, j), pad=(0, 0)))
                else:
                    layout_row.append(sg.Button(value, disabled=True, size=(4, 2), key=(i, j), pad=(0, 0)))

            layout.append(layout_row)

        layout.append([sg.Button('ok')])

        window = sg.Window('PLANES!', layout)
        while True:
            event, values = window.read()
            if event == sg.WIN_CLOSED or event == 'ok':
                exit()
            else:
                window.close()
                return event[0], event[1]

    ###############################################
    #                   GAME                      #
    ###############################################
    def game(self):
        if self.__interface == 'console':
            self.welcome()
        elif self.__interface == 'gui':
            self.welcome_gui()

        chosen_plane = 1
        while chosen_plane <= self.__planes:
            while True:
                x = None
                y = None
                orientation = None

                if self.__interface == 'console':
                    x, y, orientation = self.choose_plane(chosen_plane)
                elif self.__interface == 'gui':
                    x, y = self.choose_cabin_gui(chosen_plane)
                    orientation = self.choose_orientation_gui(chosen_plane)

                try:
                    self.__playerBoard.add_plane(x, y, orientation)
                    chosen_plane += 1
                    break
                except CoordinatesException as ce:
                    if self.__interface == 'console':
                        print(ce)
                    elif self.__interface == 'gui':
                        self.simple_message_gui(ce)
                        pass
                except InvalidPlane as ie:
                    if self.__interface == 'console':
                        print(ie)
                    elif self.__interface == 'gui':
                        self.simple_message_gui(ie)
                        pass

        self.__ai.choose_planes(self.__aiBoard)

        player_to_move = 1  # The user starts
        while True:
            if player_to_move == 1:
                if self.__interface == 'console':
                    self.print_boards_attack()
                while True:
                    x = None
                    y = None

                    if self.__interface == 'console':
                        x = input("Choose the x coordinate of the cell you want to attack: ")
                        y = input("Choose the y coordinate of the cell you want to attack: ")
                    elif self.__interface == 'gui':
                        x, y = self.print_boards_attack_gui()
                    try:
                        if self.__interface == 'console':
                            print(self.__aiBoard.attack_position(x, y))
                            break
                        elif self.__interface == 'gui':
                            message = self.__aiBoard.attack_position(x, y)
                            self.simple_message_gui(message)
                            break
                    except CellException as ce:
                        if self.__interface == 'console':
                            print(ce)
                        elif self.__interface == 'gui':
                            self.simple_message_gui(ce)
                            pass
                    except CoordinatesException as ce:
                        if self.__interface == 'console':
                            print(ce)
                        elif self.__interface == 'gui':
                            self.simple_message_gui(ce)
                            pass
            else:
                self.__ai.computer_attack(self.__playerBoard)

            player_to_move = player_to_move * (-1)
            if self.__playerBoard.board_won() == 1:
                if self.__interface == 'console':
                    print(self.print_boards(self.__playerBoard, self.__aiBoard))
                    print('--------------------------------------------------------------')
                    print("Oh no! You lost!")
                    return
                elif self.__interface == 'gui':
                    self.print_boards_gui('Oh no! You lost!')
                    return

            elif self.__aiBoard.board_won() == 1:
                if self.__interface == 'console':
                    print(self.print_boards(self.__playerBoard, self.__aiBoard))
                    print('--------------------------------------------------------------')
                    print("Hooray! You won! Good job!")
                    return
                elif self.__interface == 'gui':
                    self.print_boards_gui('Hooray! You won! Good job!')
                    return


# Start the game
start = UI(10, 3, 'gui')
start.game()
