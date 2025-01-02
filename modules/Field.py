from PyQt5 import QtCore, QtGui, QtWidgets
from modules.MyLabel import MyLabel
from modules.gamelogic import SudokuGame  


class Widget(QtWidgets.QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setFocusPolicy(QtCore.Qt.StrongFocus)
        
        # Генерируем начальную игру
        self.sudoku_game = SudokuGame()
        self.sudoku_game.fill_board()
        self.sudoku_game.remove_numbers()
        
        vBoxMain = QtWidgets.QVBoxLayout()
        frame1 = QtWidgets.QFrame()
        frame1.setStyleSheet(
            "background-color:#FF5733;border:1px solid #9AA6A7;"
        )
        grid = QtWidgets.QGridLayout()
        grid.setSpacing(0)
        

        idColor = (
            3, 4, 5, 12, 13, 14, 21, 22, 23,
            27, 28, 29, 36, 37, 38, 45, 46, 47,
            33, 34, 35, 42, 43, 44, 51, 52, 53,
            57, 58, 59, 66, 67, 68, 75, 76, 77
        )
        
        self.cells = []
        for i in range(81):
            row, col = divmod(i, 9)
            cell = MyLabel(
                i,
                MyLabel.colorGrey if i in idColor else MyLabel.colorOrange
            )
            value = self.sudoku_game.board[row][col]
            if value != 0:
                cell.setText(str(value))
            else:
                cell.changeCellFocus.connect(self.onChangeCellFocus)
            self.cells.append(cell)

        self.cells[0].setCellFocus()
        self.idCellInFocus = 0
        
        i = 0
        for j in range(9):
            for k in range(9):
                grid.addWidget(self.cells[i], j, k)
                i += 1
        frame1.setLayout(grid)
        vBoxMain.addWidget(frame1, alignment=QtCore.Qt.AlignHCenter)
        
        frame2 = QtWidgets.QFrame()
        frame2.setFixedSize(272, 36)
        hbox = QtWidgets.QHBoxLayout()
        hbox.setSpacing(1)
        btns = []
        for i in range(1, 10):
            btn = QtWidgets.QPushButton(str(i))
            btn.setFixedSize(27, 27)
            btn.setFocusPolicy(QtCore.Qt.NoFocus)
            btns.append(btn)
        btn = QtWidgets.QPushButton("X")
        btn.setFixedSize(27, 27)
        btns.append(btn)
        for btn in btns:
            hbox.addWidget(btn)
        btns[0].clicked.connect(self.onBtn0Clicked)
        btns[1].clicked.connect(self.onBtn1Clicked)
        btns[2].clicked.connect(self.onBtn2Clicked)
        btns[3].clicked.connect(self.onBtn3Clicked)
        btns[4].clicked.connect(self.onBtn4Clicked)
        btns[5].clicked.connect(self.onBtn5Clicked)
        btns[6].clicked.connect(self.onBtn6Clicked)
        btns[7].clicked.connect(self.onBtn7Clicked)
        btns[8].clicked.connect(self.onBtn8Clicked)
        btns[9].clicked.connect(self.onBtnXClicked)
        frame2.setLayout(hbox)
        vBoxMain.addWidget(frame2, alignment=QtCore.Qt.AlignHCenter)
        self.setLayout(vBoxMain)

    def onChangeCellFocus(self, id):
        if self.idCellInFocus != id and not (id < 0 or id > 80):
            self.cells[self.idCellInFocus].clearCellFocus()
            self.idCellInFocus = id
            self.cells[id].setCellFocus()

    def keyPressEvent(self, evt):
        key = evt.key()
        if key == QtCore.Qt.Key_Up:
            tid = self.idCellInFocus - 9
            if tid < 0:
                tid += 81
            self.onChangeCellFocus(tid)
        elif key == QtCore.Qt.Key_Down:
            tid = self.idCellInFocus + 9
            if tid > 80:
                tid -= 81
            self.onChangeCellFocus(tid)
        elif key == QtCore.Qt.Key_Left:
            tid = self.idCellInFocus - 1
            if tid < 0:
                tid += 81
            self.onChangeCellFocus(tid)
        elif key >= QtCore.Qt.Key_1 and key <= QtCore.Qt.Key_9:
            self.updateCell(chr(key))
        elif (
            key == QtCore.Qt.Key_Delete
            or key == QtCore.Qt.Key_Backspace
            or key == QtCore.Qt.Key_Space
        ):
            self.updateCell("")
        QtWidgets.QWidget.keyPressEvent(self, evt)

    def updateCell(self, text):
        row, col = divmod(self.idCellInFocus, 9)
        if text and not text.isdigit():
            return
        num = int(text) if text else 0
        if num != 0 and not self.sudoku_game.is_valid(self.sudoku_game.board, row, col, num):
            self.cells[self.idCellInFocus].setStyleSheet(
                f"background-color: {self.cells[self.idCellInFocus].bgColorDefault}; color: {MyLabel.colorRed};"
            )
        else:
            self.cells[self.idCellInFocus].setStyleSheet(
                f"background-color: {self.cells[self.idCellInFocus].bgColorDefault}; color: {MyLabel.colorBlack};"
            )
        self.cells[self.idCellInFocus].setNewText(text)

    def onBtn0Clicked(self): 
        self.updateCell("1")

    def onBtn1Clicked(self): 
        self.updateCell("2")

    def onBtn2Clicked(self): 
        self.updateCell("3")

    def onBtn3Clicked(self): 
        self.updateCell("4")

    def onBtn4Clicked(self): 
        self.updateCell("5")

    def onBtn5Clicked(self): 
        self.updateCell("6")

    def onBtn6Clicked(self): 
        self.updateCell("7")

    def onBtn7Clicked(self): 
        self.updateCell("8")
    
    def onBtn8Clicked(self): 
        self.updateCell("9")
    
    def onBtnXClicked(self): 
        self.updateCell("")
