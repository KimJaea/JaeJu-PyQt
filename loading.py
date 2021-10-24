import sys
import time
from PyQt5.QtWidgets import QWidget, QDesktopWidget, QApplication, QMainWindow
from PyQt5.QtGui import QPainter, QPen, QColor
from PyQt5.QtCore import Qt, QTimer, QEventLoop

min = 0
if(len(sys.argv) == 2):
    min = int(sys.argv[1])
else:
    min = 3

class MyApp(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()
        
    def initUI(self):
        QTimer.singleShot(1000 * 1, QApplication.instance().quit)
        
    def paintEvent(self, e):
        qp = QPainter()
        qp.begin(self)
        qp.setPen(QPen(QColor('#FFFFFF'), 15))
        qp.drawLine(50, 50, 350, 50)
        
        print(min)
        
        for i in range(min):
            print("sleeping...")
            time.sleep(1)
            qp.setPen(QPen(QColor('#FFC2C2'),  10))
            qp.drawPoint(50 + int(300 / min * i), 50)

        qp.end()

    def draw_point(self, qp):
        print("draw_point")
        
        
class MyWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        wg = MyApp()
        self.setCentralWidget(wg)
        self.setWindowTitle('JaeJu - Depression Detection')
        #self.setWindowIcon(QIcon('.\\jj.png'))
        self.resize(400, 100)
        self.center()
        self.show()
        
    def center(self):
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MyApp()
    ex2 = MyWindow()
    sys.exit(app.exec_())
