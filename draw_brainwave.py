import sys
from PyQt5.QtWidgets import QWidget, QApplication
from PyQt5.QtGui import QPainter, QPen
from PyQt5.QtCore import Qt
from time import sleep

class MyApp(QWidget):

    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setGeometry(300, 300, 400, 300)
        self.setWindowTitle('Brainwave Graph')
        self.show()

    def paintEvent(self, e):
        qp = QPainter()
        qp.begin(self)
        self.draw_point(qp)
        qp.end()

    def draw_point(self, qp):
        f = open('D:/ThinkGearData/sample/result.txt', "r")
        con = f.readlines()
        f.close()
        
        qp.setPen(QPen(Qt.blue,  8))
        ##qp.drawPoint(self.width()/2, self.height()/2)
        
        for c in con:
            sleep(1)
            qp.drawPoint()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MyApp()
    sys.exit(app.exec_())