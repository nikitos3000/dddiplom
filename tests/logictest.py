import unittest
import sys
import os


sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from modules.gamelogic import SudokuGame

class TestSudokuGame(unittest.TestCase):
    def setUp(self):
        self.game = SudokuGame()
    
    def test_board_initialization(self):
        self.assertEqual(len(self.game.board), 9)
        self.assertEqual(len(self.game.board[0]), 9)
    
    def test_fill_board(self):
        self.game.fill_board()

        for row in self.game.board:
            self.assertTrue(all(1 <= num <= 9 for num in row))
     
        for row in self.game.board:
            self.assertEqual(len(set(row)), 9)
    
    def test_is_valid(self):

        test_board = [
            [5, 3, 0, 0, 7, 0, 0, 0, 0],
            [6, 0, 0, 1, 9, 5, 0, 0, 0],
            [0, 9, 8, 0, 0, 0, 0, 6, 0],
            [8, 0, 0, 0, 6, 0, 0, 0, 3],
            [4, 0, 0, 8, 0, 3, 0, 0, 1],
            [7, 0, 0, 0, 2, 0, 0, 0, 6],
            [0, 6, 0, 0, 0, 0, 2, 8, 0],
            [0, 0, 0, 4, 1, 9, 0, 0, 5],
            [0, 0, 0, 0, 8, 0, 0, 7, 9]
        ]
        self.game.board = test_board
        
        self.assertTrue(self.game.is_valid(test_board, 0, 2, 4))
        self.assertTrue(self.game.is_valid(test_board, 0, 3, 2))
        
        
        self.assertFalse(self.game.is_valid(test_board, 0, 2, 5))  # Дублирование в строке
        self.assertFalse(self.game.is_valid(test_board, 0, 2, 6))  # Дублирование в столбце
        self.assertFalse(self.game.is_valid(test_board, 0, 2, 8))  # Дублирование в квадрате
    
    def test_remove_numbers(self):
        self.game.fill_board()
        original = [row[:] for row in self.game.board]
        self.game.remove_numbers(40)
        
        empty_count = sum(row.count(0) for row in self.game.board)
        self.assertEqual(empty_count, 40)
        
        
        for i in range(9):
            for j in range(9):
                if self.game.board[i][j] != 0:
                    self.assertEqual(self.game.board[i][j], original[i][j])
    
    def test_is_completed_correctly(self):
      
        solved_board = [
            [5, 3, 4, 6, 7, 8, 9, 1, 2],
            [6, 7, 2, 1, 9, 5, 3, 4, 8],
            [1, 9, 8, 3, 4, 2, 5, 6, 7],
            [8, 5, 9, 7, 6, 1, 4, 2, 3],
            [4, 2, 6, 8, 5, 3, 7, 9, 1],
            [7, 1, 3, 9, 2, 4, 8, 5, 6],
            [9, 6, 1, 5, 3, 7, 2, 8, 4],
            [2, 8, 7, 4, 1, 9, 6, 3, 5],
            [3, 4, 5, 2, 8, 6, 1, 7, 9]
        ]
        self.game.board = solved_board
        self.assertTrue(self.game.is_completed_correctly())
        

        invalid_board = [row[:] for row in solved_board]
        invalid_board[0][0] = 1  
        self.game.board = invalid_board
        self.assertFalse(self.game.is_completed_correctly())