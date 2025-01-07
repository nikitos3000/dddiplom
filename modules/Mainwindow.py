from PyQt5 import QtCore, QtGui, QtWidgets
from modules.Field import Widget
import sys
import os


class MainWindow(QtWidgets.QMainWindow):
    def __init__(self, parent=None):
        super().__init__(
            parent,
            flags=QtCore.Qt.Window | QtCore.Qt.MSWindowsFixedSizeDialogHint
        )
        self.setWindowTitle("Судоку 2.0.0")
        self.setStyleSheet(
            """
            QMainWindow {
                background-color: #DFFFD6;
            }
            QFrame QPushButton {
                font-size: 10pt;
                font-family: Verdana;
                color: black;
                font-weight: bold;
            }
            MyLabel {
                font-size: 14pt;
                font-family: Verdana;
                border: 1px solid #9AA6A7;
            }
            """
        )

        self.time_elapsed = 0  
        self.timer = QtCore.QTimer(self)
        self.timer.timeout.connect(self.update_timer)

        self.settings = QtCore.QSettings("Sudoku")
        self.sudoku = Widget()
        self.setCentralWidget(self.sudoku)

        
        self.sudoku.cellSelected.connect(self.start_timer)
        self.sudoku.gameCompleted.connect(self.stop_timer)

        buttonContainer = QtWidgets.QWidget()
        buttonLayout = QtWidgets.QHBoxLayout(buttonContainer)

        self.newGameButton = QtWidgets.QPushButton("Новая игра")
        self.menuButton = QtWidgets.QPushButton("Меню")

        self.newGameButton.setMinimumSize(200, 60)
        self.menuButton.setMinimumSize(200, 60)

        buttonLayout.addWidget(self.newGameButton)
        buttonLayout.addStretch()
        buttonLayout.addWidget(self.menuButton)

        mainLayout = QtWidgets.QVBoxLayout()
        mainLayout.addWidget(self.sudoku)
        mainLayout.addWidget(buttonContainer)

        centralWidget = QtWidgets.QWidget()
        centralWidget.setLayout(mainLayout)
        self.setCentralWidget(centralWidget)

        statusBar = self.statusBar()
        statusBar.setSizeGripEnabled(False)
        statusBar.showMessage("\"Судоку\" приветствует вас", 20000)
        if self.settings.contains("X") and self.settings.contains("Y"):
            self.move(self.settings.value("X"), self.settings.value("Y"))

        self.newGameButton.clicked.connect(self.restart_application)

    def update_timer(self):
        self.time_elapsed += 1

    def start_timer(self):
        if not self.timer.isActive():
            self.time_elapsed = 0
            self.timer.start(1000)

    def stop_timer(self):
        if self.timer.isActive():
            self.timer.stop()
            minutes, seconds = divmod(self.time_elapsed, 60)
            message = f"Поздравляем! Вы завершили игру за {minutes:02}:{seconds:02}."
            QtWidgets.QMessageBox.information(self, "Игра завершена", message)

    def restart_application(self):
        QtWidgets.QApplication.quit()
        os.execl(sys.executable, sys.executable, *sys.argv)

    def closeEvent(self, event):
        self.settings.setValue("X", self.x())
        self.settings.setValue("Y", self.y())
        event.accept()
