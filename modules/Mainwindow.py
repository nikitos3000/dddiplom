from PyQt5 import QtWidgets, QtCore
from modules.Field import Widget
from modules.gamelogic import SudokuGame


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

        self.central_widget.addWidget(self.game_widget)
        self.central_widget.addWidget(self.menu_widget)
        self.central_widget.addWidget(self.settings_widget)

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

        back_button.setMinimumSize(150, 50)
        about_button.setMinimumSize(150, 50)
        settings_button.setMinimumSize(150, 50)

        layout.addSpacing(20)
        layout.addWidget(back_button, alignment=QtCore.Qt.AlignCenter)
        layout.addSpacing(10)
        layout.addWidget(about_button, alignment=QtCore.Qt.AlignCenter)
        layout.addSpacing(10)
        layout.addWidget(settings_button, alignment=QtCore.Qt.AlignCenter)

        back_button.clicked.connect(self.switch_to_game)
        about_button.clicked.connect(self.show_about)
        settings_button.clicked.connect(self.switch_to_settings)

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

    def switch_to_game(self):
        if not hasattr(self, 'game_widget') or not self.game_widget:
            self.game_widget = self.create_game_widget()
            self.central_widget.addWidget(self.game_widget)
        self.central_widget.setCurrentWidget(self.game_widget)

    def switch_to_menu(self):
        self.central_widget.setCurrentWidget(self.menu_widget)

    def switch_to_settings(self):
        self.central_widget.setCurrentWidget(self.settings_widget)

    def show_about(self):
        QtWidgets.QMessageBox.information(self, "Об игре", "Это приложение для игры в Судоку 9x9.")

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
        if hasattr(self, 'game_widget') and self.game_widget:
            self.central_widget.removeWidget(self.game_widget)
            self.game_widget.deleteLater()
            self.game_widget = None

        self.game_widget = self.create_game_widget()
        self.central_widget.addWidget(self.game_widget)
        self.central_widget.setCurrentWidget(self.game_widget)


        self.sudoku_field.restart_game(self.num_holes)

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