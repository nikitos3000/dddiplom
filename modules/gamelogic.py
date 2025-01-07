import random

class SudokuGame:
    def __init__(self):
        self.board = [[0] * 9 for _ in range(9)]

    def is_valid(self, board, row, col, num):
        if num in board[row]:
            return False
        if num in [board[i][col] for i in range(9)]:
            return False
        start_row, start_col = 3 * (row // 3), 3 * (col // 3)
        for i in range(start_row, start_row + 3):
            for j in range(start_col, start_col + 3):
                if board[i][j] == num:
                    return False
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
                                if solve():
                                    return True
                                self.board[row][col] = 0
                        return False
            return True

        solve()

    def remove_numbers(self, num_holes=50):
        count = 0
        while count < num_holes:
            row = random.randint(0, 8)
            col = random.randint(0, 8)
            if self.board[row][col] != 0:
                self.board[row][col] = 0
                count += 1

    def is_completed_correctly(self):
        for row in range(9):
            if len(set(self.board[row])) != 9 or 0 in self.board[row]:
                return False
        for col in range(9):
            if len(set(self.board[i][col] for i in range(9))) != 9:
                return False
        for start_row in range(0, 9, 3):
            for start_col in range(0, 9, 3):
                block = []
                for i in range(3):
                    for j in range(3):
                        block.append(self.board[start_row + i][start_col + j])
                if len(set(block)) != 9:
                    return False
        return True
