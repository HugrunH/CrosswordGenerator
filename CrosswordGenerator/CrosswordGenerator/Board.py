class Board:
    def __init__(self, size):
        self.__size__ = size
        self.__grid__ = [[1] * size for tile in range(size)]
        self.__solution__ = dict()
        self.__hint_list__ = dict()

    def __str__(self): # Prints board as it is
        board = str()
        for row in self.__grid__:
            for tile in row:
                board = board + tile + " "
            board = board + "\n"
        return board

    def get_grid(self):
        return self.__grid__

    def get_size(self):
        return self.__size__

    def set_grid(self, row, col, value):
        self.__grid__[row][col] = value

    def get_tile(self, row, col):
        return self.__grid__[row][col]

    def get_hint_list(self):
        return self.__hint_list__

    def set_hint_list(self, hint_list):
        self.__hint_list__ = hint_list

    def set_solution(self, solution):
        self.__solution__ = solution

    def get_solution(self):
        return self.__solution__