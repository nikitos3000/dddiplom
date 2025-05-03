from PyQt5 import QtWidgets, QtCore
from .Field import Widget
from .gamelogic import SudokuGame
import json
from .about import rules

class MainWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Судоку")
        self.setGeometry(100, 100, 800, 600)

        self.central_widget = QtWidgets.QStackedWidget()
        self.setCentralWidget(self.central_widget)

        self.game_widget = self.create_game_widget()
        self.menu_widget = self.create_menu_widget()
        self.settings_widget = self.create_settings_widget()
        self.results_widget = self.create_results_widget()

        self.central_widget.addWidget(self.game_widget)
        self.central_widget.addWidget(self.menu_widget)
        self.central_widget.addWidget(self.settings_widget)
        self.central_widget.addWidget(self.results_widget)

        self.apply_theme("light")
        self.num_holes = 50

    def create_game_widget(self):
        game_widget = QtWidgets.QWidget()
        layout = QtWidgets.QVBoxLayout(game_widget)

        self.sudoku_field = Widget()

        new_game_button = QtWidgets.QPushButton("Новая игра")
        menu_button = QtWidgets.QPushButton("Меню")

        new_game_button.setMinimumSize(150, 50)
        menu_button.setMinimumSize(150, 50)

        layout.addWidget(self.sudoku_field)
        layout.addSpacing(20)
        layout.addWidget(new_game_button, alignment=QtCore.Qt.AlignCenter)
        layout.addSpacing(10)
        layout.addWidget(menu_button, alignment=QtCore.Qt.AlignCenter)

        new_game_button.clicked.connect(self.start_new_game)
        menu_button.clicked.connect(self.switch_to_menu)

        return game_widget

    def create_menu_widget(self):
        menu_widget = QtWidgets.QWidget()
        layout = QtWidgets.QVBoxLayout(menu_widget)
        layout.setAlignment(QtCore.Qt.AlignCenter)

        back_button = QtWidgets.QPushButton("Назад")
        about_button = QtWidgets.QPushButton("Об игре")
        settings_button = QtWidgets.QPushButton("Настройки")
        results_button = QtWidgets.QPushButton("Результаты")

        back_button.setMinimumSize(150, 50)
        about_button.setMinimumSize(150, 50)
        settings_button.setMinimumSize(150, 50)
        results_button.setMinimumSize(150, 50)

        layout.addSpacing(20)
        layout.addWidget(back_button, alignment=QtCore.Qt.AlignCenter)
        layout.addSpacing(10)
        layout.addWidget(about_button, alignment=QtCore.Qt.AlignCenter)
        layout.addSpacing(10)
        layout.addWidget(settings_button, alignment=QtCore.Qt.AlignCenter)
        layout.addSpacing(10)
        layout.addWidget(results_button, alignment=QtCore.Qt.AlignCenter)

        back_button.clicked.connect(self.switch_to_game)
        about_button.clicked.connect(self.show_about)
        settings_button.clicked.connect(self.switch_to_settings)
        results_button.clicked.connect(self.switch_to_results)

        return menu_widget

    def create_settings_widget(self):
        settings_widget = QtWidgets.QWidget()
        layout = QtWidgets.QVBoxLayout(settings_widget)
        layout.setAlignment(QtCore.Qt.AlignCenter)

        theme_label = QtWidgets.QLabel("Выберите тему:")
        theme_label.setAlignment(QtCore.Qt.AlignCenter)
        theme_label.setStyleSheet("font-size: 16pt;")

        light_theme_button = QtWidgets.QPushButton("Светлая тема")
        dark_theme_button = QtWidgets.QPushButton("Тёмная тема")

        light_theme_button.setMinimumSize(150, 50)
        dark_theme_button.setMinimumSize(150, 50)

        back_button = QtWidgets.QPushButton("Назад")
        back_button.setMinimumSize(150, 50)

        layout.addWidget(theme_label)
        layout.addSpacing(20)
        layout.addWidget(light_theme_button)
        layout.addSpacing(10)
        layout.addWidget(dark_theme_button)
        layout.addSpacing(20)
        layout.addWidget(back_button)

        light_theme_button.clicked.connect(lambda: self.apply_theme("light"))
        dark_theme_button.clicked.connect(lambda: self.apply_theme("dark"))
        back_button.clicked.connect(self.switch_to_menu)

        return settings_widget

    def create_results_widget(self):
        results_widget = QtWidgets.QWidget()
        layout = QtWidgets.QVBoxLayout(results_widget)
        layout.setAlignment(QtCore.Qt.AlignCenter)

        results_label = QtWidgets.QLabel("Результаты:")
        results_label.setStyleSheet("font-size: 16pt;")
        layout.addWidget(results_label)

        self.results_list = QtWidgets.QListWidget()
        layout.addWidget(self.results_list)

        back_button = QtWidgets.QPushButton("Назад")
        back_button.setMinimumSize(150, 50)
        back_button.clicked.connect(self.switch_to_menu)
        layout.addWidget(back_button)

        return results_widget

    def switch_to_game(self):
        self.central_widget.setCurrentWidget(self.game_widget)

    def switch_to_menu(self):
        self.central_widget.setCurrentWidget(self.menu_widget)

    def switch_to_settings(self):
        self.central_widget.setCurrentWidget(self.settings_widget)

    def switch_to_results(self):
        self.load_results()
        self.central_widget.setCurrentWidget(self.results_widget)

    def load_results(self):
        self.results_list.clear()
        try:
            with open("results.json", "r") as file:
                results = json.load(file)
                results.sort(key=lambda x: int(x['time'].split(':')[0]) * 60 + int(x['time'].split(':')[1]))
                for result in results:
                    self.results_list.addItem(f"{result['name']}: {result['time']}")
        except (FileNotFoundError, json.JSONDecodeError):
            self.results_list.addItem("Результатов пока нет.")

    def show_about(self):
        QtWidgets.QMessageBox.information(self, "Об игре", rules)

    def start_new_game(self):
        difficulty, ok = QtWidgets.QInputDialog.getItem(
            self,
            "Выбор сложности",
            "Выберите уровень сложности:",
            ["Легкий", "Средний", "Сложный"],
            0,
            False
        )

        if ok and difficulty:
            self.apply_difficulty(difficulty)
            self.restart_game()

    def apply_difficulty(self, difficulty):
        if difficulty == "Легкий":
            self.num_holes = 30
        elif difficulty == "Средний":
            self.num_holes = 50
        elif difficulty == "Сложный":
            self.num_holes = 70

    def restart_game(self):
        self.sudoku_field.restart_game(self.num_holes)
        self.central_widget.setCurrentWidget(self.game_widget)

    def apply_theme(self, theme):
        if theme == "light":
            self.setStyleSheet(
                """
                QMainWindow { background-color: #FFFFFF; }
                QPushButton { background-color: #4CAF50; color: white; }
                QLabel { color: #333333; }
                """
            )
        elif theme == "dark":
            self.setStyleSheet(
                """
                QMainWindow { background-color: #2E2E2E; }
                QPushButton { background-color: #444444; color: white; }
                QLabel { color: #FFFFFF; }
                """
            )