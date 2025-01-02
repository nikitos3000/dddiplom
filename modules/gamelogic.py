import random

class SudokuGame:
    def __init__(self):
        self.board = [[0] * 9 for _ in range(9)]

    def is_valid(self, board, row, col, num):
        if num in board[row]: return False
        if num in [board[i][col] for i in range(9)]: return False
        start_row, start_col = 3 * (row // 3), 3 * (col // 3)
        for i in range(start_row, start_row + 3):
            for j in range(start_col, start_col + 3):
                if board[i][j] == num: return False
        return True

    def fill_board(self):
        def solve():
            for row in range(9):
                for col in range(9):
                    if self.board[row][col] == 0:
                        nums = list(range(1, 10))
                        random.shuffle(nums)
                        for num in nums:
                            if self.is_valid(self.board, row, col, num):
                                self.board[row][col] = num
                                if solve(): return True
                                self.board[row][col] = 0
                        return False
            return True
        solve()

    def remove_numbers(self, difficulty=40):
        for _ in range(difficulty):
            row, col = random.randint(0, 8), random.randint(0, 8)
            while self.board[row][col] == 0:
                row, col = random.randint(0, 8), random.randint(0, 8)
            self.board[row][col] = 0
