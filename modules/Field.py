from PyQt5 import QtCore, QtGui, QtWidgets

from modules.MyLabel import MyLabel


class Widget(QtWidgets.QWidget):
    def __init__(self, parent=None):
        QtWidgets.QWidget.__init__(self, parent)
        self.setFocusPolicy(QtCore.Qt.StrongFocus)
        vBoxMain = QtWidgets.QVBoxLayout()
        frame1 = QtWidgets.QFrame()
        frame1.setStyleSheet(
            "background-color:#FF5733;border:1px solid #9AA6A7;"
        )
        print(frame1.styleSheet())
        grid = QtWidgets.QGridLayout()
        grid.setSpacing(0)
        idColor = (
            3, 4, 5, 12, 13, 14, 21, 22, 23,
            27, 28, 29, 36, 37, 38, 45, 46, 47,
            33, 34, 35, 42, 43, 44, 51, 52, 53,
            57, 58, 59, 66, 67, 75, 76, 77
        )
        self.cells = [
            MyLabel(
                i,
                MyLabel.colorGrey if i in idColor else MyLabel.colorOrange
            ) for i in range(0, 81)
        ]
        self.cells[0].setCellFocus()
        self.idCellInFocus = 0
        i = 0
        for j in range(0, 9):
            for k in range(0, 9):
                grid.addWidget(self.cells[i], j, k)
                i += 1
        for cell in self.cells:
            cell.changeCellFocus.connect(self.onChangeCellFocus)
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
            self.cells[self.idCellInFocus].setNewText(chr(key))
        elif (
            key == QtCore.Qt.Key_Delete
            or key == QtCore.Qt.Key_Backspace
            or key == QtCore.Qt.Key_Space
        ):
            self.cells[self.idCellInFocus].setNewText("")
        QtWidgets.QWidget.keyPressEvent(self, evt)

    def onBtn0Clicked(self): 
        self.cells[self.idCellInFocus].setNewText("1")

    def onBtn1Clicked(self): 
        self.cells[self.idCellInFocus].setNewText("2")

    def onBtn2Clicked(self): 
        self.cells[self.idCellInFocus].setNewText("3")

    def onBtn3Clicked(self): 
        self.cells[self.idCellInFocus].setNewText("4")

    def onBtn4Clicked(self): 
        self.cells[self.idCellInFocus].setNewText("5")

    def onBtn5Clicked(self): 
        self.cells[self.idCellInFocus].setNewText("6")

    def onBtn6Clicked(self): 
        self.cells[self.idCellInFocus].setNewText("7")

    def onBtn7Clicked(self): 
        self.cells[self.idCellInFocus].setNewText("8")
    
    def onBtn8Clicked(self): 
        self.cells[self.idCellInFocus].setNewText("9")
    
    def onBtnXClicked(self): 
        self.cells[self.idCellInFocus].setNewText("")

    def setDataAllCells(self, data):
        l = len(data)
        if l == 81:
            for i in range(0, 81):
                if data[i] == "0":
                    self.cells[i].setText("")
                    self.cells[i].clearCellBlock()
                else:
                    self.cells[i].setText(data[i])
                    self.cells[i].setCellBlock()
            self.onChangeCellFocus(0)
        elif l == 162:
            for i in range(0, 162, 2):
                if data[i] == "0":
                    self.cells[i // 2].clearCellBlock()
                else:
                    self.cells[i // 2].setCellBlock()
                self.cells[i // 2].setText("" if data[i + 1] == "0" else data[i + 1])
            self.onChangeCellFocus(0)

    
