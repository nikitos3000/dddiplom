from PyQt5 import QtCore, QtWidgets


class MyLabel(QtWidgets.QLabel):
    colorYellow = "#FFFF90"
    colorOrange = "#F5D8C1"
    colorGrey = "#E8E8E8"
    colorBlack = "#000000"
    colorRed = "#D77A38"

    changeCellFocus = QtCore.pyqtSignal(int)

    currentFocusedCell = None  

    def __init__(self, id, bgColor, parent=None):
        super().__init__(parent)
        self.setAlignment(QtCore.Qt.AlignCenter)
        self.setFixedSize(45, 60)
        self.setMargin(0)
        self.setText("")
        if id < 0 or id > 80:
            id = 0
        self.id = id
        self.isCellChange = True
        self.isInvalid = False  # Флаг для некорректной цифры
        self.fontColorCurrent = self.colorBlack
        self.bgColorDefault = bgColor
        self.bgColorCurrent = bgColor
        self.showColorCurrent()

    def mousePressEvent(self, evt):
        if MyLabel.currentFocusedCell is not None:
            MyLabel.currentFocusedCell.clearCellFocus()

        MyLabel.currentFocusedCell = self
        self.setCellFocus()
        self.changeCellFocus.emit(self.id)
        super().mousePressEvent(evt)

    def showColorCurrent(self):
        """Обновляет стиль ячейки в зависимости от состояния."""
        color = self.colorRed if self.isInvalid else self.fontColorCurrent
        self.setStyleSheet(
            f"background-color: {self.bgColorCurrent}; color: {color};"
        )

    def setCellFocus(self):
        self.bgColorCurrent = self.colorYellow
        self.showColorCurrent()

    def clearCellFocus(self):
        self.bgColorCurrent = self.bgColorDefault
        self.showColorCurrent()

    def setNewText(self, text, is_invalid=False):
        """Устанавливает текст ячейки и обновляет статус некорректности."""
        if self.isCellChange:
            self.setText(text)
            self.isInvalid = is_invalid
            self.showColorCurrent()
