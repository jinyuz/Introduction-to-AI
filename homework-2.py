# Imports

# Include your imports here, if any are used.
import math
import random
import copy
import Queue
from collections import deque


# Section 1: N-Queens

# N^2 choose N
def num_placements_all(n):
    return math.factorial(n * n) / (math.factorial(n) * math.factorial((n * n) - n))

    # N^N


def num_placements_one_per_row(n):
    return n ** n


def n_queens_valid(board):
    # set() will merge any row with the same column number
    # hence if there are conflicts the length of the set will
    # be smaller than the actual list
    if len(set(board)) < len(board):
        return False

    # check if each pair of queen is on a diagonal
    for i in range(len(board)):
        for j in range(i + 1, len(board)):
            if j - i == abs(board[i] - board[j]):
                return False

    # return true if every piece is in valid spot
    return True


def n_queens_solutions(n):
    for i in range(n):
        for solution in n_queens_helper(n, [i]):
            yield solution


def n_queens_helper(n, board):
    if n_queens_valid(board):
        if len(board) == n:
            yield board
        else:
            # iterate through all col not added so far
            for i in [col for col in range(n) if col not in board]:
                # do a quick check if the piece we're adding is not directly below
                # nor diagonal to the last piece - faster than n_queens_valid
                if (i != board[-1] and i != board[-1] + 1 and i != board[-1] - 1):
                    newBoard = list(board);
                    newBoard.append(i);
                    for solution in n_queens_helper(n, newBoard):
                        if solution:
                            yield solution


# Section 2: Lights Out

class LightsOutPuzzle(object):

    def __init__(self, board):
        self.board = board
        self.rLength = len(board) - 1
        self.cLength = len(board[0]) - 1

    def get_board(self):
        # so we don't edit the internal representation by mistake on
        # the outside
        return list(self.board)

    def perform_move(self, row, col):
        self.board[row][col] = not self.board[row][col]
        # bounds checking
        if row - 1 >= 0:
            self.board[row - 1][col] = not self.board[row - 1][col]
        if row + 1 <= self.rLength:
            self.board[row + 1][col] = not self.board[row + 1][col]
        if col - 1 >= 0:
            self.board[row][col - 1] = not self.board[row][col - 1]
        if col + 1 <= self.cLength:
            self.board[row][col + 1] = not self.board[row][col + 1]

    def scramble(self):
        for row in range(self.rLength + 1):
            for col in range(self.cLength + 1):
                if random.random() < 0.5:
                    self.perform_move(row, col)

    def is_solved(self):
        return not any([i for row in self.board for i in row])

    def copy(self):
        return copy.deepcopy(self)

    def successors(self):
        for row in range(self.rLength + 1):
            for col in range(self.cLength + 1):
                newBoard = self.copy()
                newBoard.perform_move(row, col)
                yield ((row, col), newBoard)

    def find_solution(self):

        q = Queue.Queue()
        q.put(self)

        explored = set()

        parent = {}
        parent[self] = None

        moves = {}
        moves[self] = None

        solution = []

        while not q.empty():
            board = q.get()
            explored.add(board.toTup());
            if board.is_solved():
                node = board
                while not parent[node] == None:
                    solution.append(tuple(moves[node]))
                    node = parent[node]
                return list(reversed(solution))
            else:
                for move, nextBoard in board.successors():
                    if nextBoard.toTup() not in explored:
                        q.put(nextBoard)
                        moves[nextBoard] = move
                        parent[nextBoard] = board
        return None

    def toTup(self):
        return tuple(tuple(row) for row in self.get_board())


def create_puzzle(rows, cols):
    return LightsOutPuzzle([[False for col in range(cols)] for row in range(rows)])


# Section 3: Linear Disk Movement
class LinearDiskMovement(object):

    def __init__(self, length, n, idential=True):
        self.length = length
        self.n = n
        if (idential):
            self.cells = [1 if i < n else 0 for i in xrange(length)]
        else:
            self.cells = [i + 1 if i < n else 0 for i in xrange(length)]

    def perform_move(self, fromIndex, toIndex):
        self.cells[toIndex] = self.cells[fromIndex]
        self.cells[fromIndex] = 0

    def copy(self):
        return copy.deepcopy(self)

    def successors(self):
        i = 0
        for i in range(self.length):
            if self.cells[i]:
                if i + 1 < self.length and self.cells[i + 1] == 0:
                    newLinearDisk = self.copy()
                    newLinearDisk.perform_move(i, i + 1)
                    yield (tuple((i, i + 1)), newLinearDisk)
                if i + 2 < self.length and self.cells[i + 2] == 0 and self.cells[i + 1] != 0:
                    newLinearDisk = self.copy()
                    newLinearDisk.perform_move(i, i + 2)
                    yield (tuple((i, i + 2)), newLinearDisk)
                if i - 1 >= 0 and self.cells[i - 1] == 0:
                    newLinearDisk = self.copy()
                    newLinearDisk.perform_move(i, i - 1)
                    yield (tuple((i, i - 1)), newLinearDisk)
                if i - 2 >= 0 and self.cells[i - 2] == 0 and self.cells[i - 1] != 0:
                    newLinearDisk = self.copy()
                    newLinearDisk.perform_move(i, i - 2)
                    yield (tuple((i, i - 2)), newLinearDisk)

    def is_solved_identical(self):
        return all(self.cells[-1 * self.n:])

    def is_solved_distinct(self):
        return range(self.n, 0, -1) == self.cells[-1 * self.n:]

    def solve_cells(self, identical=True):
        q = Queue.Queue()
        q.put(self)

        explored = set()

        parent = {}
        parent[self] = None

        moves = {}
        moves[self] = None

        solution = [];

        while not q.empty():
            board = q.get()
            explored.add(tuple(board.cells));
            if identical and board.is_solved_identical():
                node = board
                while not parent[node] == None:
                    solution.append(moves[node])
                    node = parent[node]
                return list(reversed(solution))
            elif not identical and board.is_solved_distinct():
                node = board
                while not parent[node] == None:
                    solution.append(moves[node])
                    node = parent[node]
                return list(reversed(solution))
            else:
                for move, nextBoard in board.successors():
                    if tuple(nextBoard.cells) not in explored:
                        q.put(nextBoard)
                        moves[nextBoard] = move
                        parent[nextBoard] = board
        return None


def solve_identical_disks(length, n):
    return LinearDiskMovement(length, n).solve_cells()


def solve_distinct_disks(length, n):
    return LinearDiskMovement(length, n, idential=False).solve_cells(identical=False)

print (len(list(n_queens_solutions(8))))