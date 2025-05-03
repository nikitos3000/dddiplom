from PyQt5 import QtWidgets, QtTest, QtCore
import unittest
import sys
import os


sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from modules.Field import Widget

class TestSudokuWidget(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.app = QtWidgets.QApplication(sys.argv)
    
    @classmethod
    def tearDownClass(cls):
        cls.app.quit()
    
    def setUp(self):
        self.widget = Widget()
    
    def test_initial_state(self):
        self.assertEqual(self.widget.timer_label.text(), "00:00")
        self.assertFalse(self.widget.timer_started)
        self.assertIsNone(self.widget.start_time)
        
        self.assertEqual(len(self.widget.cells), 81)
        
        editable_cells = [cell for cell in self.widget.cells if cell.is_editable]
        self.assertGreater(len(editable_cells), 0)
        self.assertLess(len(editable_cells), 81)
    
    def test_cell_selection(self):
        initial_id = self.widget.idCellInFocus
        target_cell = self.widget.cells[10]
        
        QtTest.QTest.mouseClick(target_cell, QtCore.Qt.LeftButton)
        
        self.assertEqual(self.widget.idCellInFocus, 10)
        self.assertNotEqual(initial_id, 10)
        self.assertTrue(target_cell.bgColorCurrent == target_cell.colorYellow)
    
    def test_number_input(self):
        editable_cell = next(cell for cell in self.widget.cells if cell.is_editable)
        QtTest.QTest.mouseClick(editable_cell, QtCore.Qt.LeftButton)
        
        self.widget.onBtnClicked(5)
        self.assertEqual(editable_cell.text(), "5")
        
        self.widget.onBtnXClicked()
        self.assertEqual(editable_cell.text(), "")
    
    def test_restart_game(self):
        initial_state = [cell.text() for cell in self.widget.cells]
        
        self.widget.restart_game(40)
        
        new_state = [cell.text() for cell in self.widget.cells]
        self.assertNotEqual(initial_state, new_state)
        
        empty_count = sum(1 for cell in self.widget.cells if cell.text() == "")
        self.assertEqual(empty_count, 40)