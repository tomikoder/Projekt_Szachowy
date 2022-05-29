from collections.abc import Sequence
from typing import Tuple, List
from .errors import (
    ChessException,
    ChessException_1,
    ChessException_2,
    ChessException_3,
    ChessException_4,
    ChessException_5,
    ChessException_6,
    ChessException_7,
    ChessException_8,
)

possible_errors = {1: 'Zła pozycja figury szachowej.',
                   2: 'Zły kolor figury szachowej.',
                   3: 'Złe argumenty do tworzenia szachownicy',
                   4: 'Złe dane wejściowe. Podałeś źle pozycje figury./n Podaj pawn A2 np.',
                   5: 'Podałeś złą literową pozycję. Dostępne są litery od a-h.',
                   6: 'Podałeś złą numeryczną pozycję. Dostępne są cyfry od 1-8.',
                   7: 'Podałeś złą nazwę figry. Użyj np pawn.',
                   8: 'Dana figura nie znajduje się na danym polu.',
                   9: 'Liczba argumentów jest nie wystarczająca, lub jest za duża.'
                   }

class Data(list):
    def __repr__(self) -> str:
        txt = ''
        for i in self:
            txt += i + '\n'
        txt = txt.rstrip('\n')
        return txt

class Figure():
    '''Ogólna klasa dla wszystkich figur'''
    position_option = (0, 1, 2, 3, 4, 5, 6, 7)
    colour_options = ('b', 'w')
    alphabed = 'abcdefgh'
    def __init__(self, field: Tuple[int, int], colour: str) -> None:
        if (not isinstance(field, tuple) or not len(field) == 2
                or field[0] not in self.position_option or field[1] not in self.position_option):
            error = ChessException_1(possible_errors[1])
            raise error
        self.field: tuple = field
        if not colour in Figure.colour_options:
            raise ChessException_2(possible_errors[2])
        else:
            self.colour: str = colour

    def list_available_moves(self, chess_board: List[List['Figure']]) -> List[str]:
        '''Używam własnej notacji dla nazw metod sprawdzających możliwe ruchy figury.
           Każda nazwa powinna się zaczynać od "figure_move_". Dzięki czemu można je
           wszystkie bezproblemu wywołać.
        '''
        data = Data()
        move_methods = [method for method in dir(self) if method.startswith("figure_move_")]
        for method in move_methods:
            getattr(self, method)(chess_board, data)
        return data

    def validate_move(self, chess_board: List[List['Figure']], dest_position: str) -> bool:
        '''Używam prostego rozwiąznia by sprawdzić czy figura może się poruszyć na dane pole.
            Nie jest wydajne, ale jest bardzo proste.
        '''
        data_set = self.list_available_moves(chess_board)
        if dest_position.lower() in data_set:
            return True
        else:
            return False

    def get_possition_in_chess_notation(self) -> str:
        return (self.alphabed[self.field[0]] + str(self.field[1] + 1))

    @classmethod
    def convert_to_chess_notation(cls, x, y) -> str:
        return cls.alphabed[x] + str(y + 1)



class Pawn(Figure):
    '''Pionek'''
    start_positions_for_white = [(i, 1) for i in range(0, 8)]
    start_positions_for_black = [(i, 6) for i in range(0, 8)]
    def figure_move_pawn(self, chess_board: List[List[Figure]], data: List[str]) -> None:
        letter_position, number_position = self.field
        field_object = None
        position_number_in_chess_notation = number_position + 1
        if self.colour == 'w':
            if position_number_in_chess_notation == 2: # początkowa pozycja dla białych
                field_object = chess_board[letter_position][number_position + 1]
                if field_object is None or field_object.colour == 'b':
                    data.append(self.convert_to_chess_notation(letter_position, number_position + 1))
                field_object = chess_board[letter_position][number_position + 2]
                if field_object is None or field_object.colour == 'b':
                    data.append(self.convert_to_chess_notation(letter_position, number_position + 2))
            elif position_number_in_chess_notation == 8:
                return
            else:
                field_object = chess_board[letter_position][number_position + 1]
                if field_object is None or field_object.colour == 'b':
                    data.append(self.convert_to_chess_notation(letter_position, number_position + 1))
        else:
            if position_number_in_chess_notation == 7: # początkowa pozycja dla czarnych
                field_object = chess_board[letter_position][number_position - 1]
                if field_object is None or field_object.colour == 'w':
                    data.append(self.convert_to_chess_notation(letter_position, number_position - 1))
                field_object = chess_board[letter_position][number_position - 2]
                if field_object is None or field_object.colour == 'w':
                    data.append(self.convert_to_chess_notation(letter_position, number_position - 2))
            elif position_number_in_chess_notation == 1:
                return
            else:
                field_object = chess_board[letter_position][number_position - 1]
                if field_object is None or field_object.colour == 'w':
                    data.append(self.convert_to_chess_notation(letter_position, number_position - 1))

    def __str__(self) -> str:
        if self.colour =='w':
            return '♙'
        else:
            return '♟'

class Rook(Figure):
    '''Wieża'''
    start_positions_for_white = [(0, 0), (7 ,0)]
    start_positions_for_black = [(0, 7), (7, 7)]

    def figure_move_full_in_x_and_y_axis(self, chess_board: List[List[Figure]], data: List[str]) -> None:
        letter_position, number_position = self.field
        field_object = None
        position_number_in_chess_notation = number_position + 1
        counter_y_up = number_position + 1
        counter_y_down = number_position - 1
        while True:
            if counter_y_up == 8:
                break
            field_object = chess_board[letter_position][counter_y_up]
            if field_object is None or field_object.colour != self.colour:
                data.append(self.convert_to_chess_notation(letter_position, counter_y_up))
                counter_y_up += 1
            else:
                break
        while True:
            if counter_y_down == -1:
                break
            field_object = chess_board[letter_position][counter_y_down]
            if field_object is None or field_object.colour != self.colour:
                data.append(self.convert_to_chess_notation(letter_position, counter_y_down))
                counter_y_down -= 1
            else:
                break
        counter_x_left = letter_position - 1
        counter_x_right = letter_position + 1
        while True:
            if counter_x_left == -1:
                break
            field_object = chess_board[counter_x_left][number_position]
            if field_object is None or field_object.colour != self.colour:
                data.append(self.convert_to_chess_notation(counter_x_left, position_number_in_chess_notation))
                counter_x_left -= 1
            else:
                break
        while True:
            if counter_x_right == 8:
                break
            field_object = chess_board[counter_x_right][number_position]
            if field_object is None or field_object.colour != self.colour:
                data.append(self.convert_to_chess_notation(counter_x_right, position_number_in_chess_notation))
                counter_x_right += 1
            else:
                break

    def __str__(self):
        if self.colour == 'w':
            return '♖'
        else:
            return '♜'

class Knight(Figure):
    '''Skoczek'''
    start_positions_for_white = [(1, 0), (6 ,0)]
    start_positions_for_black = [(1, 7), (6, 7)]
    data_to_calculate_moves = [(1, 2), (2, 1), (2, -1), (1, -2), (-1, -2), (-2, -1), (-2, 1), (-1, 2)]

    def figure_move_for_knight(self, chess_board: List[List[Figure]], data: List[str]) -> None:
        letter_position, number_position =  self.field
        field_object = None
        #Ruchy wymienione zgodnie ze ruchem wskazówek zegara.

        for (x, y) in self.data_to_calculate_moves:
            new_x, new_y = (letter_position + x), (number_position + y)
            if (new_x > 7 or new_y > 7) or (new_x < 0 or new_y < 0):       # Sprawdzam czy figura nie jest poza planszą
                continue
            else:
                field_object = chess_board[new_x][new_y]
                if field_object is None or field_object.colour != self.colour:
                    data.append(self.convert_to_chess_notation(new_x, new_y))

    def __str__(self):
        if self.colour == 'w':
            return '♘'
        else:
            return '♞'

class Bishop(Figure):
    '''Goniec'''
    start_positions_for_white = [(2, 0), (5 ,0)]
    start_positions_for_black = [(2, 7), (5, 7)]

    def figure_move_full_diagonally(self, chess_board: List[List[Figure]], data: List[str]) -> None:
        letter_position, number_position = self.field
        field_object = None
        x_counter_right, y_counter_up  = letter_position + 1, number_position + 1
        while True:
            if x_counter_right == 8 or y_counter_up ==8:
                break
            field_object = chess_board[x_counter_right][y_counter_up]
            if field_object is None or field_object.colour != self.colour:
                data.append(self.convert_to_chess_notation(x_counter_right, y_counter_up))
                x_counter_right += 1
                y_counter_up    += 1
            else:
                break

        x_counter_left, y_counter_up  = letter_position - 1, number_position + 1
        while True:
            if x_counter_left == -1 or y_counter_up == 8:
                break
            field_object = chess_board[x_counter_left][y_counter_up]
            if field_object is None or field_object.colour != self.colour:
                data.append(self.convert_to_chess_notation(x_counter_left, y_counter_up))
                x_counter_left -= 1
                y_counter_up   += 1
            else:
                break

        x_counter_right, y_counter_down = letter_position + 1, number_position - 1
        while True:
            if x_counter_right == 8 or y_counter_down == -1:
                break
            field_object = chess_board[x_counter_right][y_counter_down]
            if field_object is None or field_object.colour != self.colour:
                data.append(self.convert_to_chess_notation(x_counter_right, y_counter_down))
                x_counter_right += 1
                y_counter_down  -= 1
            else:
                break

        x_counter_left, y_counter_down = letter_position -1, number_position -1
        while True:
            if x_counter_left == -1 or y_counter_down == -1:
                break
            field_object = chess_board[x_counter_left][y_counter_down]
            if field_object is None or field_object.colour != self.colour:
                data.append(self.convert_to_chess_notation(x_counter_left, y_counter_down))
                x_counter_left -= 1
                y_counter_down -= 1
            else:
                break

    def __str__(self) -> str:
        if self.colour == 'w':
            return '♗'
        else:
            return '♝'

class Queen(Bishop, Rook):
    '''Królowa

       Ta figura ma takie same ruchy jak wieża i goniec, więc nie ma potrzeby
       implementowania metod poruszania się dla niej, kiedy można wykorzystać
       dziedziczenie klas, aby zaimplementować ruchy tamtych figur.
    '''
    start_positions_for_white = [(3, 0)]
    start_positions_for_black = [(3, 7)]

    def __str__(self) -> str:
        if self.colour == 'w':
            return '♕'
        else:
            return '♛'

class King(Figure):
    '''Król'''
    start_positions_for_white = [(4, 0)]
    start_positions_for_black = [(4, 7)]

    def figure_move_king(self, chess_board: List[List[Figure]], data: List[str]) -> None:
        letter_position, number_position = self.field
        field_object = None
        possible_moves_in_left_right = [letter_position -1, letter_position, letter_position + 1]
        possible_moves_in_down_up    = [number_position -1, number_position, number_position + 1]

        #Usuwam wszystkie skrajne pozycje, które mogą przekraczać dopuszczalne pola szachownicy.
        if possible_moves_in_left_right[0] == -1:
           del possible_moves_in_left_right[0]
        elif possible_moves_in_left_right[1] == 8:
            del possible_moves_in_left_right[1]

        if possible_moves_in_down_up[0] == -1:
            del possible_moves_in_down_up[0]
        elif possible_moves_in_down_up[1] == 8:
            del possible_moves_in_down_up[1]

        for x in possible_moves_in_left_right:
            for y in possible_moves_in_down_up:
                field_object = chess_board[x][y]
                if field_object is None or field_object.colour != self.colour:
                    data.append(self.get_possition_in_chess_notation(x, y))

    def __str__(self) -> str:
        if self.colour == 'w':
            return '♔'
        else:
            return '♚'

class Chess_Board():
    figure_options = {'pawn': Pawn, 'rook': Rook, 'knight': Knight, 'bishop':  Bishop, 'queen': Queen, 'king': King}
    letters =       {'a': 1, 'b': 2, 'c': 3, 'd': 4, 'e': 5, 'f': 6, 'g': 7, 'h': 8}

    def __init__(self, custom: bool=False, chessmans: List[Figure]=None):
        '''Możesz tworzyć szachownicę z własnymi ustawieniami pionków. Musisz podać dwa dodatkowe argumenty do inicjatora klasy, "custom" ustawić na True, i
           jako "chessmans" podać sekwencyjną strukturę danych, która zawiera instancję figur z wszystkimi potrzebnymi danymi.
        '''
        self.board = [[None for i in range(8)] for i in range(8)]
        if custom == False:
            for Figure in self.figure_options.values():
                for (x , y) in Figure.start_positions_for_white:
                    self.board[x][y] = Figure(field=(x, y), colour='w')
                for (x, y) in Figure.start_positions_for_black:
                    self.board[x][y] = Figure(field=(x, y), colour='b')
        elif custom == True and chessmans:
            for chm in chessmans:
                x, y = chm.field[0], chm.field[1]
                self.board[x][y] = chm
        else:
            error = ChessException_3(possible_errors[3])
            raise error

    @classmethod
    def validate_position(cls, position: str) -> Tuple[int, int]:
        if len(position) != 2 or not position[0].isalpha or not position[1].isnumeric:
            error = ChessException_4(possible_errors[4])
            raise error
        letter_position, number_position = position[0].lower(), int(position[1])
        if letter_position not in cls.letters.keys():
            raise ChessException_5(possible_errors[5])
        else:
            letter_position = cls.letters.get(letter_position) - 1
        if number_position not in Figure.position_option:
            raise ChessException_6(possible_errors[6])
        else:
            number_position = number_position - 1
        return letter_position, number_position

    def get_figure(self, figure_name: str, letter_position: int, number_position: int) -> Figure:
        if figure_name.lower() not in self.figure_options.keys():
            error = ChessException_7(possible_errors[7])
            raise ChessException_7(possible_errors[7])
        else:
            Figure_Type: type = self.figure_options[figure_name]
        figure_to_check: Figure = self.board[letter_position][number_position]
        if (figure_to_check is None) or not isinstance(figure_to_check, Figure_Type):
            error = ChessException_8(possible_errors[8])
            raise error
        return figure_to_check

    def validate_moves(self, figure_name: str, position: str, dest_position: str) -> bool:
        try: #Sprawdzam dane docelowej pozycji.
            self.validate_position(dest_position)
        except ChessException as exc:
            exc.destination = True
            raise exc
        letter_position, number_position = self.validate_position(position)
        figure_to_check = self.get_figure(figure_name, letter_position, number_position)
        result_data: bool = figure_to_check.validate_move(self.board, dest_position)
        return result_data

    def move_options(self, figure_name: str, position: str) -> List[str]:
        letter_position, number_position = self.validate_position(position)
        figure_to_check = self.get_figure(figure_name, letter_position, number_position)
        result_data = figure_to_check.list_available_moves(self.board)
        return result_data

    def move_figure(self, figure_name: str, position: str, dest_position: str) -> None:
        x1, y1 = self.conver_chess_notation_to_indexes(position)
        x2, y2 = self.conver_chess_notation_to_indexes(dest_position)
        figure = self.get_figure(figure_name, x1, y1)
        if figure.validate_move(self.board, dest_position) == True:
            figure.field = (x2, y2)
            if self.board[x2][y2] is None:
                self.board[x1][y1] = None
                self.board[x2][y2] = figure
            else:
                self.board[x1][y1] = None
                self.board[x2][y2] = None
                self.board[x2][y2] = figure

    @classmethod
    def conver_chess_notation_to_indexes(cls, position: str) -> Tuple[int, int]:
        return (cls.letters[position[0].lower()], int(position[1] - 1))

    def show_board(self) -> None:
        txt = ''
        c = 7
        while c >= 0:
            for f in self.board:
                elem = f[c]
                if elem is not None:
                    txt += str(f[c])
                else:
                    txt += ' '
            txt += '\n'
            c -= 1
        print(txt)

mapping_index = {'a': 0, 'b': 1, 'c': 2, 'd': 3, 'e': 4, 'f': 5, 'g': 6, 'h': 7}

def get_chess_field(pos: str) -> Tuple[int, int]:
    '''Podaj stringę np A1, by dostać odpowiednią pozycje figry na szachownicy
    '''
    return Chess_Board.validate_position(pos)

if __name__ == '__main__':
    pass