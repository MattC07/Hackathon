from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton, QVBoxLayout, QWidget, QLabel, QLineEdit
from PyQt5 import QtCore, QtGui
import sys




class MainWindow(QMainWindow):

    def __init__(self):
        super().__init__()
        self.w = None
        
        #Get Window Size
        screen = app.primaryScreen()
        size = screen.size()
        w_height = size.height()
        w_width  = (2*size.height())/3
        pos_x = (size.width()-w_width)/2
        pos_y = 0    
        self.setGeometry(int(pos_x), int(pos_y), int(w_width) , int(w_height))
        self.windowLayout = loginWdiget()
        self.setCentralWidget(self.windowLayout)

    def keyPressEvent(self, event):
        if event.key() == QtCore.Qt.Key_Escape:
            self.close()


class loginWdiget(QWidget):
    def __init__(self):
        super().__init__()

        logoLabel = QLabel(self)
        pixmap = QtGui.QPixmap('./Image/shop.png')
        logoLabel.setPixmap(pixmap)

        self.userTextBox = QLineEdit()
        self.passTextBox = QLineEdit()
        self.loginButton = QPushButton("LOGIN")

        layout = QVBoxLayout(self)
        layout.addWidget(logoLabel)
        layout.addWidget(self.userTextBox)
        layout.addWidget(self.passTextBox)
        layout.addWidget(self.loginButton)


        







        #self.button = QPushButton("Push for Window")
        #self.button.clicked.connect(self.show_new_window)
        #self.setCentralWidget(self.button)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    w = MainWindow()
    w.show()
    sys.exit(app.exec_())