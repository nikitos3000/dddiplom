from PyQt5 import QtCore, QtGui, QtWidgets
from modules.MyLabel import MyLabel
from modules.gamelogic import SudokuGame
import time


class Widget(QtWidgets.QWidget):
    cellSelected = QtCore.pyqtSignal()
    gameCompleted = QtCore.pyqtSignal()

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setFocusPolicy(QtCore.Qt.StrongFocus)

        self.sudoku_game = SudokuGame()
        self.sudoku_game.fill_board()

        print("Решение текущей головоломки:")
        self.print_board(self.sudoku_game.board)

        self.sudoku_game.remove_numbers()

        self.timer_started = False
        self.start_time = None

        self.timer_label = QtWidgets.QLabel("00:00")
        self.timer_label.setAlignment(QtCore.Qt.AlignCenter)
        self.timer_label.setStyleSheet("font-size: 16pt; color: black;")

        self.timer = QtCore.QTimer(self)
        self.timer.timeout.connect(self.update_timer)
        self.elapsed_time = 0

        vBoxMain = QtWidgets.QVBoxLayout()

        vBoxMain.addWidget(self.timer_label)

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
                cell.set_editable(False)  # Ячейка с начальным значением не редактируемая
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
        frame2.setFixedSize(400, 150)
        hbox = QtWidgets.QHBoxLayout()
        hbox.setSpacing(1)
        btns = []
        for i in range(1, 10):
            btn = QtWidgets.QPushButton(str(i))
            btn.setFixedSize(35, 60)
            btn.setFocusPolicy(QtCore.Qt.NoFocus)
            btns.append(btn)
        btn = QtWidgets.QPushButton("X")
        btn.setFixedSize(35, 60)
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

    def print_board(self, board):
        for row in board:
            print(" ".join(str(num) if num != 0 else '.' for num in row))

    def onChangeCellFocus(self, id):
        if self.idCellInFocus != id and not (id < 0 or id > 80):
            if not self.timer_started:
                self.cellSelected.emit()
                self.start_time = time.time()
                self.timer.start(1000)
                self.timer_started = True
            self.cells[self.idCellInFocus].clearCellFocus()
            self.idCellInFocus = id
            self.cells[id].setCellFocus()

    def updateCell(self, text):
        row, col = divmod(self.idCellInFocus, 9)
        if not self.cells[self.idCellInFocus].is_editable:
            return  # Если ячейка не редактируемая, ничего не делаем

        if text and not text.isdigit():
            return
        num = int(text) if text else 0

        is_invalid = num != 0 and not self.sudoku_game.is_valid(
            self.sudoku_game.board, row, col, num
        )
        self.sudoku_game.board[row][col] = num
        self.cells[self.idCellInFocus].setNewText(text, is_invalid)

        if all(cell.text() for cell in self.cells):
            if self.sudoku_game.is_completed_correctly():
                self.on_game_completed()
            else:
                QtWidgets.QMessageBox.critical(
                    self,
                    "Ошибка",
                    "Решение игры неправильное. Перепроверьте своё решение.",
                )

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
        if self.cells[self.idCellInFocus].is_editable:
            self.updateCell("")

    def update_timer(self):
        if self.start_time:
            elapsed = int(time.time() - self.start_time + self.elapsed_time)
            minutes = elapsed // 60
            seconds = elapsed % 60
            self.timer_label.setText(f"{minutes:02}:{seconds:02}")

    def on_game_completed(self):
        self.timer.stop()
        elapsed_time = int(time.time() - self.start_time + self.elapsed_time)
        minutes = elapsed_time // 60
        seconds = elapsed_time % 60
        QtWidgets.QMessageBox.information(
            self, "Поздравляем!", f"Игра завершена! Время: {minutes:02}:{seconds:02}"
        )

    def update_board(self):
        """Обновляет отображение доски."""
        for i in range(81):
            row, col = divmod(i, 9)
            value = self.sudoku_game.board[row][col]
            if value != 0:
                self.cells[i].setText(str(value))
            else:
                self.cells[i].setText("")

    def reset_cells(self):
        """Сбрасывает все ячейки и обновляет их состояние."""
        for i in range(81):
            row, col = divmod(i, 9)
            value = self.sudoku_game.board[row][col]
            self.cells[i].setText(str(value) if value != 0 else "")
            self.cells[i].set_editable(value == 0)  # Блокируем начальные ячейки
            self.cells[i].isInvalid = False
            self.cells[i].showColorCurrent()

    def restart_game(self, num_holes):
        """Перезапускает игру с новой сложностью."""
        self.sudoku_game = SudokuGame()
        self.sudoku_game.fill_board()
        self.sudoku_game.remove_numbers(num_holes)
        self.reset_cells()  # Сбрасываем ячейки
        self.timer_started = False
        self.start_time = None
        self.timer_label.setText("00:00")