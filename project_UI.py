import socket, glob, sys, os
import webbrowser
import subprocess
from time import sleep
from PyQt5 import QtWidgets, QtCore
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *

width = 200
height = 30

class MyApp(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        # Set Time for Getting EEG
        self.spinbox = QSpinBox(self)
        self.spinbox.setMinimum(1)
        self.spinbox.setMaximum(10)
        self.spinbox.setGeometry(50, 50, 50, height)
        self.minuteString = QLabel(' minute', self)
        self.minuteString.setGeometry(110, 50, 100, height)

        # Set Path and File Name for Getting EEG
        self.dirSelect = QPushButton("Select Directory", self)
        self.dirSelect.clicked.connect(self.dirSelectClicked)
        self.dirSelect.setGeometry(50, 100, width, height)
        self.dirLabel = QLabel(os.getcwd(), self)
        self.dirLabel.setGeometry(270, 100, 350, height)
        self.fileName = QLineEdit("test", self)
        self.fileName.setGeometry(270, 50, 70, height)
        self.fileFormat = QLabel('.txt', self)
        self.fileFormat.setGeometry(350, 50, 70, height)
        self.portName = QLineEdit("COM6", self)
        self.portName.setGeometry(550, 50, 70, height)
        self.portFormat = QLabel(' port', self)
        self.portFormat.setGeometry(630, 50, 70, height)
        btnGetEEG = QPushButton("Get EEG", self)
        btnGetEEG.clicked.connect(self.clicked1)
        btnGetEEG.setGeometry(600, 100, 150, height)
        self.dialog = QDialog()

        # Select Files to Combine and Combine all
        self.filesSelect = QPushButton("Select Files", self)
        self.filesSelect.clicked.connect(self.filesSelectClicked)
        self.filesSelect.setGeometry(50, 200, width, height)
        self.filesToCombine = []
        self.filesLabel = QLabel('(병합할 파일을 선택하세요)', self)
        self.filesLabel.setGeometry(270, 200, 300, 80)
        btnCombine = QPushButton('Combine Files', self)
        btnCombine.setGeometry(600, 200, 150, height)
        btnCombine.clicked.connect(self.combineDataFiles)

        # Set Path and File Name for Preprocessing EEG
        self.fileSelect = QPushButton("Select File", self)
        self.fileSelect.clicked.connect(self.fileSelectClicked)
        self.fileSelect.setGeometry(50, 300, width, height)
        self.fileLabel = QLabel('(전처리할 파일을 선택하세요.)', self)
        self.fileLabel.setGeometry(270, 300, 300, height)
        btnPreEEG = QPushButton('Preprocess EEG', self)
        btnPreEEG.clicked.connect(self.clicked2)
        btnPreEEG.setGeometry(600, 300, 150, height)

        # Get Result Button & Web Page Button
        self.getResult = QPushButton("Get Result", self)
        self.getResult.clicked.connect(self.getResultClicked)
        self.getResult.setGeometry(50, 400, width, height)
        self.resultLabel = QLabel('(우울증 결과)', self)
        self.resultLabel.setGeometry(270, 400, 300, height)
        btnWebPage = QPushButton('Web Page', self)
        btnWebPage.clicked.connect(self.clicked3)
        btnWebPage.setGeometry(600, 400, 150, height)

    def dirSelectClicked(self):
        dname = QFileDialog.getExistingDirectory(self)
        self.dirLabel.setText(dname)
    
    def filesSelectClicked(self):
        fnames = QFileDialog.getOpenFileNames(self)
        self.filesToCombine = fnames[0]
        des = ""
        for i in self.filesToCombine:
            des += i + '\n'
        self.filesLabel.setText(des)

    def fileSelectClicked(self):
        fname = QFileDialog.getOpenFileName(self)
        self.fileLabel.setText(fname[0])
    
    def combineDataFiles(self):
        path = self.dirLabel.text()
        os.chdir(path)

        if os.path.exists("data_total.txt"):
            os.remove("data_total.txt")
        print('combine!')
        with open("data_total.txt", "wb") as outfile:
            for filename in self.filesToCombine:
                i = 0
                i += 1
                with open(filename, "rb") as infile:
                    outfile.write(infile.read())

    def getResultClicked(self):
        QMessageBox.about(self, "message", "wait for send EEG data")
        file = self.fileLabel.text()
        data = str(socket_client(file))
        per = data[2:4] + '.' + data[4:7]

        if(data[-1] == '0'):
            self.resultLabel.setText(per + "%의 확률로 우울증이 아닙니다.")
        else:
            self.resultLabel.setText(per + "%의 확률로 우울증이 맞습니다.")

    def clicked1(self):
        time = str(self.spinbox.value() * 60)
        path = self.dirLabel.text() + "/" + self.fileName.text() + ".txt"
        port = self.portName.text()
        QMessageBox.about(self, "message", "Getting EEG")
        ## Show Brainwave Visualizer OR Video
        #os.startfile("D:\ThinkGearData\BrainwaveVisualizer\Brainwave Visualizer.exe")
        ##os.startfile("D:\\ThinkGearData\\sample\\video.mp4")
        ## dialog for draw brainwave graph
        #os.startfile('D:\\ThinkGearData\\draw_brainwave.py')
        
        sleep(1) ## time for waiting before get EEG
        data = os.system('.\\thinkgear_testapp\\Debug\\thinkgear_testapp.exe ' + time + ' ' + path + ' \\\\.\\' + port)
        # data get 1 when PORT ERROR occured, 0 when no error
        
    def clicked2(self):
        QMessageBox.about(self, "message", "PreProcess EEG")
        if not self.fileLabel.text():
            os.system('.\\preprocess_artifact.py')
        else:
            file = self.fileLabel.text()
            path, f = os.path.split(file)
            os.system('.\\preprocess_artifact.py ' + file + ' ' + path)

    def clicked3(self):
        QMessageBox.about(self, "message", "opening web page")
        webbrowser.open('http://52.14.220.200:8080/')

    def multipleFileClicked(self):
        file = self.fileLabel.text()
        f = open(file, "r")
        con = f.readline()
        f.close()

        con2 = con
        con2 = con2.split() # list
        num = int(210000 / len(con2)) + 1


        if os.path.exists("data_multiple.txt"):
            os.remove("data_multiple.txt")
        with open("data_multiple.txt", "wb") as outfile:
            for i in range(num):
                outfile.write(con.encode())

class MyWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        wg = MyApp()
        self.setCentralWidget(wg)
        self.setWindowTitle('JaeJu - Depression Detection')
        self.setWindowIcon(QIcon('.\\jj.png'))
        self.resize(800, 500)
        self.center()
        self.show()
        
    def center(self):
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())

def socket_client(file_name):
    HOST = '3.145.22.213'
    PORT = 8080

    def return_value(data1, data2):
        return(data1 + data2)

    ## print('received ' + file_name)
    f = open(file_name, "r")
    con = f.readlines()
    f.close()

    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect((HOST, PORT))
    for i in con:
        data = str(i)
        client_socket.send(data.encode())
    data = "end"
    client_socket.send(data.encode())

    data = client_socket.recv(1024)
    print('Received', data.decode())
    # Received accuracy:0.00000000000000 predict:0
    client_socket.close()
    
    datas = data.decode().split(' ')
    return return_value(datas[0][9:], datas[1][8])


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MyApp()
    ex2 = MyWindow()
    sys.exit(app.exec_())

    #ex.show()
    #app.exec_()
