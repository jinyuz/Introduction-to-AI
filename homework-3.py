############################################################
# CMPSC 442: Homework 3
############################################################

student_name = "Jinyu Zhao"

############################################################
# Imports
############################################################

import random
import Queue
import math
import copy

# Include your imports here, if any are used.



############################################################
# Section 1: Tile Puzzle
############################################################

dumplicate = {}

def create_tile_puzzle(rows, cols):
    board = []
    count = 1
    for i in range(rows):
        board.append([])
        for j in range(cols):
            board[i].append(count)
            count += 1
    board[rows - 1][cols - 1] = 0
    return TilePuzzle(board)


class TilePuzzle(object):
    
    # Required
    def __init__(self, board):
        self.board = []
        for i in range(len(board)):
            self.board.append([])
            for j in range(len(board[i])):
                self.board[i].append(board[i][j])
        self.direction = {'up': (-1, 0), 'down':(1, 0), 'left':(0, -1), 'right':(0, 1)}
        self.moves = []


    def find_empty(self):
        for i in range(len(self.board)):
            for j in range(len(self.board[i])):
                if self.board[i][j] == 0:
                    return (i, j)


    def get_board(self):
        return self.board

    def is_valid(self, r, c):
        return r >= 0 and r < len(self.board) and c >= 0 and c < len(self.board[0])

    def perform_move(self, direction):
        r, c = self.find_empty()
        tor = r + self.direction[direction][0]
        toc = c + self.direction[direction][1]
        if self.is_valid(tor, toc):
            tem = self.board[r][c]
            self.board[r][c] = self.board[tor][toc]
            self.board[tor][toc] = tem
            return True
        return False

    def scramble(self, num_moves):
        for i in range(num_moves):
            self.perform_move(random.choice(("up", "down", "left", "right")))

    def is_solved(self):
        count = 1
        for i in range(len(self.board)):
            for j in range(len(self.board[i])):
                if i == len(self.board) - 1 and j == len(self.board[i]) - 1:
                    if self.board[i][j] != 0:
                        return False
                else:
                    if self.board[i][j] != count:
                        return False
                count += 1
        return True

    def copy(self):
        return TilePuzzle(self.board)

    def successors(self):
        lst = ['up', 'down', 'left', 'right']
        for dir in lst:
            puzzle = self.copy()
            if puzzle.perform_move(dir):
                yield dir, puzzle

    def get_string(self):
        res = ''
        for i in range(len(self.board)):
            for j in range(len(self.board[i])):
                res += str(self.board[i][j])
        return res


    def iddfs_helpter(self, limit, moves):
        if limit <= 0:
            return
        if self.is_solved():
            yield moves

        for move, new_p in self.successors():
            moves.append(move)
            result = new_p.iddfs_helpter(limit - 1, copy.copy(moves))
            for item in result:
                yield item
            moves.pop(-1)

    # Required
    def find_solutions_iddfs(self):
        for limit in range(1, 10000):
            moves = []
            found = False
            result = self.iddfs_helpter(limit, moves)
            if result:
                for solution in result:
                    yield solution
                    if solution:
                        found = True
            if found:
                break
        

    def manhattan_distance(self):
        res = 0
        for i in range(len(self.board)):
            for j in range(len(self.board[0])):
                if (self.board[i][j] == 0):
                    continue
                else:
                    x = (self.board[i][j]-1) / len(self.board)
                    y = (self.board[i][j]-1) % len(self.board[0])
                    res += abs(x-i)+abs(y-j)
        return res

    def __lt__(self, other):
        return len(self.moves) + self.manhattan_distance() < len(other.moves) + other.manhattan_distance()

    # Required
    def find_solution_a_star(self):

        dumplicate.clear()
        q = Queue.PriorityQueue()
        q.put(self)

        while True:
            if q.empty():
                break
            start = q.get()
            if start.is_solved():
                return start.moves
            for move, child in start.successors():
                str = child.get_string()
                if str not in dumplicate:
                    child.moves = copy.copy(start.moves)
                    child.moves.append(move)
                    q.put(child)
                    dumplicate[str] = 1

        return None



############################################################
# Section 2: Grid Navigation
############################################################


class GridNavigation(object):
    # Required
    def __init__(self, start, goal, board):
        self.start = start
        self.goal = goal
        self.board = []
        for i in range(len(board)):
            self.board.append([])
            for j in range(len(board[i])):
                self.board[i].append(board[i][j])
        self.direction = {'up': (-1, 0), 'down': (1, 0), 'left': (0, -1), 'right': (0, 1), 'up-left':(-1, -1), 'up-right':(-1, 1), 'down-left':(1, -1), 'down-right':(1, 1)}
        self.moves = []

    def get_board(self):
        return self.board

    def is_valid(self, r, c):
        return r >= 0 and r < len(self.board) and c >= 0 and c < len(self.board[0])

    def perform_move(self, direction):
        r, c = (self.start[0] + self.direction[direction][0], self.start[1] + self.direction[direction][1])
        if self.is_valid(r, c):
            if not self.board[r][c]:
                self.start = (r, c)
                return True
        return False

    def is_solved(self):
        return self.start == self.goal

    def copy(self):
        return GridNavigation(self.start, self.goal, self.board)

    def successors(self):
        lst = ['up', 'down', 'left', 'right', 'up-left', 'up-right', 'down-left', 'down-right']
        for dir in lst:
            puzzle = self.copy()
            if puzzle.perform_move(dir):
                yield dir, puzzle

    def euclidean_distance(self):
        return math.sqrt((self.start[0] - self.goal[0]) ** 2 + (self.start[1] - self.goal[1]) ** 2)

    def __lt__(self, other):
        return len(self.moves) + self.euclidean_distance() < len(other.moves) + other.euclidean_distance()

    def get_string(self):
        res = '%d, %d' % (self.start[0], self.start[1])
        return res

    # Required
    def find_solution_a_star(self):

        dumplicate.clear()
        q = Queue.PriorityQueue()
        q.put(self)

        while True:
            if q.empty():
                break
            start = q.get()
            if start.is_solved():
                return start.moves
            for move, child in start.successors():
                str = child.get_string()
                if str not in dumplicate:
                    child.moves = copy.copy(start.moves)
                    child.moves.append(move)
                    q.put(child)
                    dumplicate[str] = 1

        return None

    def find_solution(self, start, goal):
        moves = self.find_solution_a_star()
        if moves is None:
            return None
        r, c = start[0], start[1]
        lst = []
        for move in moves:
            lst.append((r, c))
            r, c = self.direction[move][0] + r, c + self.direction[move][1]
        lst.append((r, c))
        return lst

def find_path(start, goal, scene):
    problem = GridNavigation(start, goal, scene)
    return problem.find_solution(start, goal)


############################################################
# Section 3: Linear Disk Movement, Revisited
############################################################

def solve_distinct_disks(length, n):
    pass

############################################################
# Section 4: Dominoes Game
############################################################

def create_dominoes_game(rows, cols):
    board = []
    for i in range(rows):
        board.append([])
        for j in range(cols):
            board[i].append(False)
    return DominoesGame(board)


class DominoesGame(object):

    states = 0

    # Required
    def __init__(self, board):

        self.board = []
        for i in range(len(board)):
            self.board.append([])
            for j in range(len(board[i])):
                self.board[i].append(board[i][j])

    def get_board(self):
        return self.board

    def reset(self):
        for i in range(len(self.board)):
            for j in range(len(self.board[i])):
                self.board[i][j] = False

    def is_valid(self, r, c):
        return r >= 0 and r < len(self.board) and c >= 0 and c < len(self.board[0])

    def is_legal_move(self, row, col, vertical):
        if vertical:
            if self.is_valid(row, col) and self.is_valid(row + 1, col):
                if not self.board[row][col] and not self.board[row + 1][col]:
                    return True
        else:
            if self.is_valid(row, col) and self.is_valid(row, col + 1):
                if not self.board[row][col] and not self.board[row][col + 1]:
                    return True



    def legal_moves(self, vertical):
        for i in range(len(self.board)):
            for j in range(len(self.board[i])):
                if self.is_legal_move(i, j, vertical):
                    yield (i, j)

    def perform_move(self, row, col, vertical):
        if self.is_legal_move(row, col, vertical):
            if vertical:
                self.board[row][col] = True
                self.board[row + 1][col] = True
            else:
                self.board[row][col] = True
                self.board[row][col + 1] = True

    def game_over(self, vertical=True):
        for i in range(len(self.board)):
            for j in range(len(self.board[i])):
                if self.is_legal_move(i, j, vertical):
                    return False
        return True

    def copy(self):
        return DominoesGame(self.board)

    def successors(self, vertical):
        for move in self.legal_moves(vertical):
            child = self.copy()
            child.perform_move(move[0], move[1], vertical)
            yield (move, child)

    def get_random_move(self, vertical):
        moves = list(self.legal_moves(vertical))
        return random.choice(moves)

    def getScore(self, vertical):
        return len(list(self.legal_moves(vertical))) - len(list(self.legal_moves(not vertical)))


    def max_value(self, player, alpha, beta, depth, limit):
        if depth >= limit:
            DominoesGame.states += 1
            return ((0, 0), self.getScore(player))
        if self.game_over(player):
            DominoesGame.states += 1
            return ((0, 0), self.getScore(player))

        max_v = -999999999
        this_move = None
        for (move, child) in self.successors(player):
            value = child.min_value(player, alpha, beta, depth + 1, limit)[1]
            if max_v < value:
                max_v = value
                this_move = move
            if max_v >= beta:
                break
            if alpha < max_v:
                alpha = max_v
        return (this_move, max_v)

    def min_value(self, player, alpha, beta, depth, limit):
        if depth >= limit:
            DominoesGame.states += 1
            return ((0, 0), self.getScore(player))
        if self.game_over(not player):
            DominoesGame.states += 1
            return ((0, 0), self.getScore(player))

        min_v = 999999999
        this_move = None
        for (move, child) in self.successors(not player):
            value = child.max_value(player, alpha, beta, depth + 1, limit)[1]
            if min_v > value:
                min_v = value
                this_move = move
            if min_v <= alpha:
                break
            if beta > min_v:
                beta = min_v
        return (this_move, min_v)





    # Required
    def get_best_move(self, vertical, limit):
        DominoesGame.states = 0
        move, value = self.max_value(vertical, -999999999, 999999999, 0, limit)
        return (move, value, DominoesGame.states)




############################################################
# Section 5: Feedback
############################################################

feedback_question_1 = """
20 hours
"""

feedback_question_2 = """
It is hard to understand each game. And need to come up how to 
implement the searching algorithm to the real problem.
"""

feedback_question_3 = """
I like the build up suggestion. maybe some video to introduce the game can be better.
"""
