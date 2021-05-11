from argparse import ArgumentParser

class sudoku:
    table_sh = '''
    ╒═══════════╤═══════════╤═══════════╕
    │ {}   {}   {} │ {}   {}   {} │ {}   {}   {} │
    │           │           │           │
    │ {}   {}   {} │ {}   {}   {} │ {}   {}   {} │
    │           │           │           │
    │ {}   {}   {} │ {}   {}   {} │ {}   {}   {} │
    ├───────────┼───────────┼───────────┤
    │ {}   {}   {} │ {}   {}   {} │ {}   {}   {} │
    │           │           │           │
    │ {}   {}   {} │ {}   {}   {} │ {}   {}   {} │
    │           │           │           │
    │ {}   {}   {} │ {}   {}   {} │ {}   {}   {} │
    ├───────────┼───────────┼───────────┤
    │ {}   {}   {} │ {}   {}   {} │ {}   {}   {} │
    │           │           │           │
    │ {}   {}   {} │ {}   {}   {} │ {}   {}   {} │
    │           │           │           │
    │ {}   {}   {} │ {}   {}   {} │ {}   {}   {} │
    ╘═══════════╧═══════════╧═══════════╛'''

    def __init__(self, x: str):
        sudoku = list(x)
        indexes = [i for i in range(81) if sudoku[i] == '0']
        x2 = True
        while (sudoku.count('0') > 0) and x2:
            x2 = False
            # Enferadi
            for i in indexes:
                res = self.GetResults(i, sudoku)
                if res.__len__() == 1:
                    sudoku[i] = res[0]
                    indexes.remove(i)
                    x2 = True
            # check rows
            for i in range(0, 81, 9):
                row = set(self.GetRow(i, sudoku, 1)) & set(indexes)
                for num in range(1, 10):
                    res = [0, 0]
                    for index in row:
                        results = self.GetResults(index, sudoku)
                        if num.__str__() in results:
                            res[0] += 1
                            res[1] = index
                    if res[0] == 1:
                        sudoku[res[1]] = num.__str__()
                        indexes.remove(res[1])
                        x2 = True
            # check cloumns
            for i in range(9):
                cloumn = set(self.GetCloumn(i, sudoku, 1)) & set(indexes)
                for num in range(1, 10):
                    res = [0, 0]
                    for index in cloumn:
                        results = self.GetResults(index, sudoku)
                        if num.__str__() in results:
                            res[0] += 1
                            res[1] = index
                    if res[0] == 1:
                        sudoku[res[1]] = num.__str__()
                        indexes.remove(res[1])
                        x2 = True
            # check square
            for i in range(3):
                for i2 in range(i * 27, i * 27 + 27, 12):
                    square = set(self.GetSquare(i, sudoku, 1)) & set(indexes)
                    for num in range(1, 10):
                        res = [0, 0]
                        for index in square:
                            results = self.GetResults(index, sudoku)
                            if num.__str__() in results:
                                res[0] += 1
                                res[1] = index
                        if res[0] == 1:
                            sudoku[res[1]] = num.__str__()
                            indexes.remove(res[1])
                            x2 = True
        self.table_sh = self.table_sh.format(*sudoku)

    def __str__(self):
        return self.table_sh

    def GetRow(self, index: int, table: list, mod=0) -> list:
        row = int(index / 9)
        if mod == 0:
            tb = [table[i:i + 9] for i in range(0, table.__len__(), 9)]
            return tb[row]
        elif mod == 1:
            tb = [row * 9 + i for i in range(9)]
            return tb

    def GetCloumn(self, index: int, table: list, mod=0) -> list:
        if mod == 0:
            return table[index % 9:81:9]
        elif mod == 1:
            return [i for i in range(index % 9, 81, 9)]

    def GetSquare(self, index: int, table: list, mod=0) -> list:
        tb = [[], []]
        for i in range(0, 81, 27):
            for i2 in range(i, i + 9, 3):
                if mod == 0:
                    for i3 in range(0, 19, 9): tb[0].extend(table[i2 + i3:i2 + i3 + 3])
                elif mod == 1:
                    for i3 in range(0, 19, 9): tb[0].extend(list(range(i2 + i3, i2 + i3 + 3)))
                tb[1].append(tb[0].copy())
                tb[0].clear()
        ind = int(index / 27) * 3 + int(index % 9 / 3)
        return tb[1][ind]

    def GetResults(self, index: int, table: list) -> list:
        res = []
        for num in range(1, 10):
            sudoku2 = table.copy()
            sudoku2[index] = num.__str__()
            row = self.GetRow(index, sudoku2)
            cloumn = self.GetCloumn(index, sudoku2)
            square = self.GetSquare(index, sudoku2)
            if all((row.count(num.__str__()) == 1, cloumn.count(num.__str__()) == 1, square.count(num.__str__()) == 1)):
                res.append(num.__str__())
        return res


parser = ArgumentParser()
parser.add_argument('-s', required=True, dest='sudoku', help='enter sudoku for solve', type=str)
args = parser.parse_args()
if __name__ == '__main__':
    if args.sudoku:
        if args.sudoku.__len__() == 81:
            result = sudoku(args.sudoku).__str__()
            print(result)
        else:
            parser.error('sudoku length must be 81 character')
    else:
        parser.print_help()
