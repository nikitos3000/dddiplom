from PyQt5 import QtWidgets, QtGui
import unittest

import sys
import os


sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from modules.MyLabel import MyLabel

class TestMyLabel(unittest.TestCase):
    def setUp(self):
        self.app = QtWidgets.QApplication([])
        self.cell = MyLabel(0, MyLabel.colorOrange)
    
    def tearDown(self):
        self.app.quit()
    
    def test_initial_state(self):
        self.assertEqual(self.cell.text(), "")
        self.assertTrue(self.cell.is_editable)
        self.assertFalse(self.cell.isInvalid)
        self.assertEqual(self.cell.bgColorCurrent, self.cell.bgColorDefault)
    
    def test_focus_handling(self):
        # Проверяем изменение фокуса
        self.cell.setCellFocus()
        self.assertEqual(self.cell.bgColorCurrent, self.cell.colorYellow)
        
        self.cell.clearCellFocus()
        self.assertEqual(self.cell.bgColorCurrent, self.cell.bgColorDefault)
    
    def test_text_update(self):
        # Проверяем обновление текста
        self.cell.setNewText("5", False)
        self.assertEqual(self.cell.text(), "5")
        self.assertFalse(self.cell.isInvalid)
        
        # Проверяем отметку невалидного значения
        self.cell.setNewText("5", True)
        self.assertTrue(self.cell.isInvalid)
    
