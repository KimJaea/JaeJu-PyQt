import socket, glob, sys, os
import webbrowser
import subprocess
from time import sleep
from PyQt5 import QtWidgets, QtCore
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *

class MyApp(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        # Set Time for Getting EEG
        self.spinbox = QSpinBox(self)
        self.spinbox.setMinimum(1)
        self.spinbox.setMaximum(10)
        self.spinbox.valueChanged.connect(self.value_changed)
        self.spinbox.setGeometry(50, 50, 50, 20)
        self.minute = QLabel('1', self)
        self.minute.setAlignment(Qt.AlignCenter)
        self.minute.setGeometry(150, 50, 20, 20)
        self.minuteString = QLabel(' minute', self)
        self.minuteString.setAlignment(Qt.AlignCenter)
        self.minuteString.setGeometry(150, 50, 100, 20)

        # Set Path and File Name for Getting EEG
        self.dirSelect = QPushButton("Select Directory", self)
        self.dirSelect.clicked.connect(self.dirSelectClicked)
        self.dirSelect.setGeometry(50, 100, 200, 20)
        self.dirLabel = QLabel(os.getcwd(), self)
        self.dirLabel.setGeometry(250, 100, 200, 20)
        self.dirLabel.setAlignment(Qt.AlignCenter)
        self.fileName = QLineEdit("test", self)
        self.fileName.setGeometry(500, 100, 70, 20)
        self.portName = QLineEdit("COM5", self)
        self.portName.setGeometry(500, 120, 70, 20)
        self.portFormat = QLabel(' port', self)
        self.portFormat.setGeometry(600, 120, 70, 20)
        self.fileFormat = QLabel('.txt', self)
        self.fileFormat.setGeometry(600, 100, 70, 20)
        btnGetEEG = QPushButton("Get EEG", self)
        btnGetEEG.clicked.connect(self.clicked1)
        btnGetEEG.setGeometry(650, 100, 100, 30)
        self.dialog = QDialog()

        # Select Files to Combine and Combine all
        self.filesSelect = QPushButton("Select Files", self)
        self.filesSelect.clicked.connect(self.filesSelectClicked)
        self.filesSelect.setGeometry(50, 200, 200, 20)
        self.filesToCombine = []
        self.filesLabel = QLabel('(병합할 파일을 선택하세요)', self)
        self.filesLabel.setGeometry(250, 200, 300, 80)
        self.filesLabel.setAlignment(Qt.AlignCenter)
        btnCombine = QPushButton('Combine Files', self)
        btnCombine.setGeometry(650, 200, 100, 30)
        btnCombine.clicked.connect(self.combineDataFiles)

        # Set Path and File Name for Preprocessing EEG
        self.fileSelect = QPushButton("Select File", self)
        self.fileSelect.clicked.connect(self.fileSelectClicked)
        self.fileSelect.setGeometry(50, 300, 200, 20)
        self.fileLabel = QLabel('D:/ThinkGearData/result.txt', self)
        self.fileLabel.setGeometry(300, 300, 200, 20)
        self.fileLabel.setAlignment(Qt.AlignCenter)
        btnPreEEG = QPushButton('Preprocess EEG', self)
        btnPreEEG.clicked.connect(self.clicked2)
        btnPreEEG.setGeometry(650, 300, 100, 30)

        # Get Result Button & Web Page Button
        self.getResult = QPushButton("Get Result", self)
        self.getResult.clicked.connect(self.getResultClicked)
        self.getResult.setGeometry(50, 400, 200, 20)
        self.resultLabel = QLabel('(우울증 결과)', self)
        self.resultLabel.setGeometry(300, 400, 250, 20)
        self.resultLabel.setAlignment(Qt.AlignCenter)
        btnWebPage = QPushButton('Web Page', self)
        btnWebPage.clicked.connect(self.clicked3)
        btnWebPage.setGeometry(650, 400, 100, 30)

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

    # combine every file in directory
    '''
    def combineDataFiles(self):
        path = self.dirLabel.text()
        os.chdir(path)

        if os.path.exists("data_total.txt"):
            os.remove("data_total.txt")
        read_files = glob.glob("*.txt")
        with open("data_total.txt", "wb") as outfile:
            for f in read_files:
                i = 0
                i += 1
                with open(f, "rb") as infile:
                    outfile.write(infile.read())
    '''
    
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
        os.startfile("D:\\ThinkGearData\\sample\\video.mp4")
        ## dialog for draw brainwave graph
        #os.startfile('D:\\ThinkGearData\\draw_brainwave.py')
        
        sleep(1) ## time for waiting before get EEG
        data = os.system('D:\\ThinkGearData\\thinkgear_testapp\\Debug\\thinkgear_testapp.exe ' + time + ' ' + path + ' \\\\.\\' + port)
        # data get 1 when PORT ERROR occured, 0 when no error
        
    def clicked2(self):
        QMessageBox.about(self, "message", "PreProcess EEG")
        if not self.fileLabel.text():
            os.system('D:\\ThinkGearData\\preprocess_artifact.py')
        else:
            file = self.fileLabel.text()
            path, f = os.path.split(file)
            os.system('D:\\ThinkGearData\\preprocess_artifact.py ' + file + ' ' + path)

    def clicked3(self):
        QMessageBox.about(self, "message", "opening web page")
        webbrowser.open('http://webpage.com:8080')

    def value_changed(self):
        self.minute.setText(str(self.spinbox.value()))

class MyWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        wg = MyApp()
        self.setCentralWidget(wg)
        self.setWindowTitle('JaeJu - Depression Detection')
        self.setWindowIcon(QIcon('.\\jj.png'))
        self.resize(800, 600)
        self.center()
        self.show()
        
    def center(self):
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())

def socket_client(file_name):
    HOST = '3.16.56.48'
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
    ## print('Received', data.decode())
    # Received accuracy:0.00000000000000 loss:0.00000000000000 predict:0
    client_socket.close()
    
    datas = data.decode().split(' ')
    return return_value(datas[0][9:], datas[2][8])


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MyApp()
    ex2 = MyWindow()
    sys.exit(app.exec_())

    #ex.show()
    #app.exec_()
