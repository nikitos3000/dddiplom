from PyQt5 import QtWidgets
import unittest
import sys
import os


sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from modules.Mainwindow import MainWindow

class TestMainWindow(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.app = QtWidgets.QApplication(sys.argv)
    
    @classmethod
    def tearDownClass(cls):
        cls.app.quit()
    
    def setUp(self):
        self.window = MainWindow()
        self.window.show()
    
    def test_window_initialization(self):

        self.assertEqual(self.window.windowTitle(), "Судоку")
        self.assertEqual(self.window.num_holes, 50)
    
        self.assertIsNotNone(self.window.game_widget)
        self.assertIsNotNone(self.window.menu_widget)
        self.assertIsNotNone(self.window.settings_widget)
        self.assertIsNotNone(self.window.results_widget)
    
    def test_theme_switching(self):
        self.window.apply_theme("dark")
        self.assertIn("background-color: #2E2E2E", self.window.styleSheet())
        
        self.window.apply_theme("light")
        self.assertIn("background-color: #FFFFFF", self.window.styleSheet())
    
    def test_navigation(self):
        self.window.switch_to_menu()
        self.assertEqual(self.window.central_widget.currentWidget(), self.window.menu_widget)
        
        self.window.switch_to_settings()
        self.assertEqual(self.window.central_widget.currentWidget(), self.window.settings_widget)
        
        self.window.switch_to_game()
        self.assertEqual(self.window.central_widget.currentWidget(), self.window.game_widget)
    
    def test_difficulty_selection(self):
        self.window.apply_difficulty("Легкий")
        self.assertEqual(self.window.num_holes, 30)
        
        self.window.apply_difficulty("Средний")
        self.assertEqual(self.window.num_holes, 50)
        
        self.window.apply_difficulty("Сложный")
        self.assertEqual(self.window.num_holes, 70)