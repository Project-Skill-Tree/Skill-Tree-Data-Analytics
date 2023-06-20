from stdata import *
from stgraphs import *
from PyQt6.QtWidgets import *
import sys

# Definition of PyQt App, Layout and Window
app = QApplication(sys.argv)


class MainWin(QMainWindow):
    def __init__(self):
        super().__init__()
        self.button = QPushButton('Top')
        self.button.clicked.connect(self.show_new_window)
        self.setCentralWidget(self.button)

    def show_new_window(self, checked):
        self.w = SkillWin()
        self.w.show()

class SkillWin(QWidget):
    def __init__(self):
        super().__init__()
        layout = QVBoxLayout()
        label = QLabel(str(SkillData().get_ease()))
        layout.addWidget(label)
        self.setLayout(layout)

mainWin = MainWin()
mainWin.show()
app.exec()
