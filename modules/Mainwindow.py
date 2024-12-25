

from PyQt5 import QtCore, QtGui, QtWidgets, QtPrintSupport
from modules.Field import Widget





class MainWindow(QtWidgets.QMainWindow):
    def __init__(self, parent=None):
        QtWidgets.QMainWindow.__init__(
            self,
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
        self.settings = QtCore.QSettings("Sudoku")
        self.sudoku = Widget()
        self.setCentralWidget(self.sudoku)

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
    


