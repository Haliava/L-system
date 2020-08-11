import sys
import math
from PyQt5.QtWidgets import QWidget, QApplication, QSlider, QPushButton, QFileDialog, QLineEdit
from PyQt5.QtGui import QPainter, QPen
from PyQt5.QtCore import Qt

FILE_PATH = 'tree.ls'
GEOMETRY = 1000
MAX_GEN = 10


class Example(QWidget):
    def __init__(self):
        super().__init__()
        self.rules = {}
        self.example = ''
        self.res = {}
        self.angle = 0
        self.starting_position = ''
        self.line_len = 10
        self.gen = 1
        self.START_X = 500
        self.START_Y = 980
        self.initUI()

    def initUI(self):
        self.setGeometry(GEOMETRY, GEOMETRY, GEOMETRY, GEOMETRY)

        slider = QSlider(Qt.Horizontal, self)
        slider.resize(GEOMETRY, 20)
        slider.move(0, 20)
        slider.setMaximum(MAX_GEN)
        slider.setMinimum(1)
        slider.valueChanged.connect(self.set_gen)

        butt = QPushButton('Выбрать формулу', self)
        butt.move(GEOMETRY // 2 - 50, 50)
        butt.clicked.connect(self.set_file_path)

        self.start_x = QLineEdit('Х начальной точки', self)
        self.start_x.move(20, 70)
        self.start_x.textEdited.connect(self.set_x)

        self.start_y = QLineEdit('Y начальной точки', self)
        self.start_y.move(20, 100)
        self.start_y.textEdited.connect(self.set_y)

        with open('formulas/' + FILE_PATH) as L:
            data = L.readlines()
            self.setWindowTitle(data[0])
            self.angle = 2 * math.pi / int(data[1])
            self.starting_position = data[2]
            for elem in data[3:]:
                self.rules[elem.split()[0]] = elem.split()[1:]
        self.set_gen(1)
        self.show()

    def set_x(self):
        if self.sender().text().isalnum():
            self.START_X = int(self.sender().text())

    def set_y(self):
        if self.sender().text().isalnum():
            self.START_Y = int(self.sender().text())

    def set_file_path(self):
        global FILE_PATH
        FILE_PATH = QFileDialog.getOpenFileName(self, 'Выбрать файл', '')[0]
        self.rules.clear()

        with open(FILE_PATH) as L:
            data = L.readlines()
            self.setWindowTitle(data[0])
            self.angle = 2 * math.pi / int(data[1])
            self.starting_position = data[2]
            for elem in data[3:]:
                self.rules[elem.split()[0]] = elem.split()[1:]
        self.set_gen()

    def set_gen(self, gen=1):
        self.window().update()
        self.gen = self.sender().value() if self.sender() and type(self.sender()) != QPushButton else gen
        print(self.rules)
        temp = self.starting_position
        for i in range(self.gen):
            new_temp = ''
            for syll in temp:
                if syll in self.rules.keys():
                    new_temp += self.rules[syll][0]
                else:
                    new_temp += syll
            temp = new_temp
        self.example = temp
        self.line_len = 10

    def paintEvent(self, event):
        qp = QPainter()
        qp.begin(self)
        self.draw(qp)
        qp.end()

    def draw(self, qp):
        pen = QPen(Qt.red, 2)
        qp.setPen(pen)
        x, y = self.START_X, self.START_Y
        saved = []
        angle = 0
        for syll in self.example:
            if syll == 'F':
                temp_x = x + self.line_len * math.cos(angle)
                temp_y = y + self.line_len * math.sin(angle)
                qp.drawLine(x, y, round(temp_x), round(temp_y))
                x = round(temp_x)
                y = round(temp_y)
            elif syll == '+':
                angle += self.angle
            elif syll == '-':
                angle -= self.angle
            elif syll == '[':
                saved.append((x, y, angle))
            elif syll == ']':
                x, y, angle = saved.pop()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Example()
    sys.exit(app.exec_())
