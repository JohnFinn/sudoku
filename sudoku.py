#!/usr/bin/python3

import random

class Sudoku:
    def __init__(self, grid):
        self.grid = grid

    def __getitem__(self, pos):
        row, col = pos
        return self.grid[row][col]

    def __setitem__(self, pos, item):
        row, col = pos
        self.grid[row][col] = item

    def get_row(self, pos):
        return self.grid[pos[0]]

    def get_col(self, pos):
        return [value[pos[1]] for value in self.grid]

    def get_block(self, pos):
        """ Возвращает все значения из квадрата,
        в который попадает позиция pos """
        row, col = pos
        row -= row % 3
        col -= col % 3
        return self.grid[row][col:col+3] + self.grid[row + 1][col:col+3] + self.grid[row + 2][col:col+3]

    @staticmethod
    def positions():
        for i in range(9):
            for j in range(9):
                yield i, j


    def __str__(self):
        width = 2
        line = '+'.join(['-' * (width * 3)] * 3)
        res = ''
        for row in range(9):
            res += ''.join(
                (str(self[row, col]).center(width) if self[row, col] else '.'.center(width)) +
                ('|' if str(col) in '25' else '') for col in range(9)
            ) + '\n'
            if str(row) in '25':
                res += line + '\n'
        return res


    @classmethod
    def from_file(cls, file, fmt='raw'):
        """ Прочитать Судоку из указанного файла """
        s = cls([[None for i in range(9)] for i in range(9)])
        if fmt == 'raw':
            for r, line in enumerate(file):
                for c, ch in enumerate(line.rstrip()):
                    if ch.isdigit():
                        s[r,c] = int(ch)
        elif fmt == 'pretty':
            width = 2
            line = '+'.join(['-' * (width * 3)] * 3)
            # br, sr, sc, bc  means big/small row/column
            for br, strings in enumerate(file.read().split(line)): # three strins of 'x x x | x x x | x x x'
                for sr, string in enumerate(strings.strip().split('\n')): # one string 'x x x | x x x | x x x'
                    for bc, triple in enumerate(string.strip().split('|')): # triple of 'x x x'
                        for sc, value in enumerate(triple.strip().split()):
                            value = value.strip()
                            if value.isdigit():
                                s[br * 3 + sr, bc * 3 + sc] = int(value)
        return s

    def solve(self):
        """ Решение пазла, заданного в grid """
        """ Как решать Судоку?
            1. Найти свободную позицию
            2. Найти все возможные значения,
            которые могут находиться на этой позиции
            3. Для каждого возможного значения:
                3.1. Поместить это значение на эту позицию
                3.2. Продолжить решать оставшуюся часть пазла
        """
        pos = self.find_empty_position()
        if not pos:
            return True # solved
        values = self.find_possible_values(pos)
        for value in values:
            self[pos] = value
            if self.solve():
                return True
            self[pos] = None


    def find_empty_position(self):
        """ Найти первую свободную позицию в пазле

        >>> find_empty_position([['1', '2', '.'], ['4', '5', '6'], ['7', '8', '9']])
        (0, 2)
        >>> find_empty_position([['1', '2', '3'], ['4', '.', '6'], ['7', '8', '9']])
        (1, 1)
        >>> find_empty_position([['1', '2', '3'], ['4', '5', '6'], ['.', '8', '9']])
        (2, 0)
        """
        for i, row in enumerate(self.grid):
            if None in row:
                return i, row.index(None)

    def value_is_possible(self, pos, value):
        return all(map(lambda func : value not in func(pos), (self.get_row, self.get_col, self.get_block)))

    def find_possible_values(self, pos):
        """ Вернуть все возможные значения для указанной позиции"""
        possible_values = []
        for value in range(1, 10):
            if self.value_is_possible(pos, value):
                possible_values.append(value)
        return possible_values


    @staticmethod
    def check_line(line):
        """
        >>> _ = None
        >>> check_line([1, 2, 3, 4, 5, 6, 7, 8, 9])
        True
        >>> check_line([1, 2, 3, 4, 9, 6, 7, 8, 9])
        False
        >>> check_line([_, 1, _, 3, 5, 7, 7, 8, 9])
        False
        >>> check_line([_, 1, 4, 3, 5, _, _, 8, 9])
        True
        """
        for i, value in enumerate(line):
            if not value:
                continue
            elif value in line[:i] + line[i + 1:]:
                return False
        return True

    def check_pos(self, pos):
        return all(map(lambda func: self.check_line(func(pos)), (self.get_row, self.get_col, self.get_block)))




    def check(self):
        """ Если решение solution верно, то вернуть True,
         в противном случае False"""
        for i in range(len(self.grid)):
            for j in range(len(self.grid[i])):
                if not self.check_pos((i,j)):
                    return False
        return True


    def generate_answer(self):
        pos = self.find_empty_position()
        if not pos:
            return True
        values = self.find_possible_values(pos)
        random.shuffle(values)
        for value in values:
            self[pos] = value
            if self.generate_answer():
                return True
            self[pos] = None


    def remove_values(self, n):
        for i in range(n):
            while True:
                pos = random.randrange(9), random.randrange(9)
                if self[pos]:
                    break
            self[pos] = None

    @classmethod
    def random(cls, n):
        s = cls([[None for i in range(9)] for i in range(9)])
        s.generate_answer()
        s.remove_values(81 - n)
        return s


if __name__ == '__main__':
    # TODO
    # auto detect raw/pretty formats
    # open text editor (vi/nano) to input sudoku instead of reading file
    # use C to imporve solving algorithm
    # create graphs (time/complexity) on 2 impementations
    # improve solving algorithm, mesure time again
    # create algorithm in c
    # create algorithm in assembler and use it in this python3 script
        # if C/C++ code can be linked to python assembler also should be able to
    # "./sudoku.py solve filenames" solve sudoku in all files,
    # ^ optionally & default including filename, optionally & non-default the puzzle itself

    def solve(args):
        s = Sudoku.from_file(args.file, fmt='pretty')
        args.file.close()
        s.solve()
        print(s)

    def check(args):
        s = Sudoku.from_file(args.file, fmt='pretty')
        args.file.close()
        print(s.check())

    import argparse
    parser = argparse.ArgumentParser(description="solve or generate sudoku")
    subparsers = parser.add_subparsers()


    # for pname, hlp, agrname, argtype, func in ((), (), ()):
        # p = subparsers.add_parser(pname, help=hlp)
        # p.add_argument(agrname, type=argtype)
        # p.set_defaults(func=func)

    parser_solve = subparsers.add_parser('solve', help='solve sudoku')
    parser_solve.add_argument('file', type=argparse.FileType('rt'))
    parser_solve.set_defaults(func=solve)

    parser_check = subparsers.add_parser('check', help='check if sudoku solved correctly')
    parser_check.add_argument('file', type=argparse.FileType('rt'))
    parser_check.set_defaults(func=check)

    parser_gen = subparsers.add_parser('gen', help='generate sudoku with N inserted cells')
    parser_gen.add_argument('number', type=int)
    parser_gen.set_defaults(func=lambda argrs : print(Sudoku.random(args.number)))

    args = parser.parse_args()
    args.func(args)
