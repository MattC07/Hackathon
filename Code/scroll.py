from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel
from PyQt5 import QtCore, QtGui
import sys
import os
from Susu_shop_backend import Backend

class MyItems(QMainWindow):

    def __init__(self):
        super().__init__()

        self.backend = Backend(r"./Database/susu_shop.db")
        self.backend.start_session(1)

        self.timer = QtCore.QTimer(self)
        
        self.w_height = 0
        self.w_width = 0
        self.pos_x = 0
        self.pos_y = 0

        self.obj_width = 100
        self.obj_height = 120
        self.border_width = 50
        self.border_height = 80
        self.obj_space_x = 0
        self.obj_space_y = 0
        self.objInitial_flag = True

        self.basket_width = 500
        self.basket_height = 300
        self.basket_border_width = 0
        self.basket_border_height = 0


        self.mouse_x_pos = 0
        self.mouse_y_pos = 0
        self.prev_mouse_x_pos = 0
        self.prev_mouse_y_pos = 0
        self.movement_change_x_pos = 0

        self.moveRight_flag = False
        self.moveLeft_flag = False


        self.objSelected_flag = False
        self.objMove_flag = False
        self.objChange_flag = False
        self.objRelease_flag = False

        self.objTotal_page = 2
        self.objPage_number = 1

        self.obj_added_row  = 0
        self.obj_added_col = 0

        self.imageNumber = 1
        self.obj_count = 0

        self.counter = QLabel('0', self)
        self.counter.move(int(self.w_width-self.border_width-self.basket_width+5),int(self.w_height-self.border_height-(self.basket_width/2)))

        self.windowSize()
        self.setGeometry(int(self.pos_x), int(self.pos_y), int(self.w_width) , int(self.w_height))

    def windowSize(self):
        screen = app.primaryScreen()
        size = screen.size()
        self.w_height = size.height()
        self.w_width  = (2*size.height())/3
        self.pos_x = (size.width()-self.w_width)/2   

    def keyPressEvent(self, event):
        if event.key() == QtCore.Qt.Key_Escape:
            os.remove("./Database/susu_shop.db")
            self.close()

    def paintEvent(self, e):
        painter = QtGui.QPainter(self)
        pixmap_background = QtGui.QPixmap("./Image/wood_background.png")
        painter.drawPixmap(0,0,int(self.w_width),int(self.w_height),pixmap_background)

        self.obj_space_x = (self.w_width-(4*self.obj_width)-(2*self.border_width))/3
        self.obj_space_y = (self.w_height-(2*self.border_height)-self.basket_height-(3*self.obj_height))/3

        for i in range(3):
            pixmap_shelf = QtGui.QPixmap("./Image/wood_shelf.png")
            painter.drawPixmap(0, int((self.border_height + self.obj_height)*(i+1)+(i*4)), int(self.w_width),25,pixmap_shelf)

        self.basket_border_width = (self.w_width - self.basket_width)/2
        self.basket_border_height = (self.w_height - self.border_height - self.basket_height)
        pixmap = QtGui.QPixmap("./Image/shopping_cart.png")
        painter.drawPixmap(int(self.basket_border_width), int(self.basket_border_height), int(self.basket_width), int(self.basket_height),pixmap)

        counter = QtCore.QRect(int(self.w_width-105),int(self.w_height-self.border_height-100),54,50)
        painter.fillRect(counter, QtGui.QBrush(QtCore.Qt.red))
        painter.drawText(counter, QtCore.Qt.AlignCenter, str(self.obj_count))

 
        if self.objMove_flag is True:
            if self.moveLeft_flag is True:
                if self.objPage_number == 1:
                    for i in range(3):
                        for k in range(8):
                            if k < 4:
                                self.imageNumber = self.backend.shelf[self.objPage_number-1,i,k].index 
                                if self.backend.shelf[self.objPage_number-1,i,k].quantity == 0:
                                    pixmap = QtGui.QPixmap("./Inventory/" + "g" + str(self.imageNumber) + ".png")
                                else:
                                    pixmap = QtGui.QPixmap("./Inventory/" + str(self.imageNumber) + ".png")
                            else:
                                self.imageNumber = self.backend.shelf[self.objPage_number-0,i,k-4].index
                                if self.backend.shelf[self.objPage_number-0,i,k-4].quantity == 0:
                                    pixmap = QtGui.QPixmap("./Inventory/" + "g" + str(self.imageNumber) + ".png")
                                else:
                                    pixmap = QtGui.QPixmap("./Inventory/" + str(self.imageNumber) + ".png")
                            painter.drawPixmap(QtCore.QRect(int((self.border_width + ((self.obj_width+self.obj_space_x)*k)-self.movement_change_x_pos)), int(self.border_height +((self.obj_space_y+self.obj_height)*i)), self.obj_width, self.obj_height),pixmap)

                else:
                    for i in range(3):
                        for k in range(4):
                            self.imageNumber = self.backend.shelf[self.objPage_number-1,i,k].index
                            if self.backend.shelf[self.objPage_number-1,i,k].quantity == 0:
                                pixmap = QtGui.QPixmap("./Inventory/" + "g" + str(self.imageNumber) + ".png")
                            else:
                                pixmap = QtGui.QPixmap("./Inventory/" + str(self.imageNumber) + ".png")
                            painter.drawPixmap(QtCore.QRect(int(self.border_width + ((self.obj_width+self.obj_space_x)*k)), int(self.border_height +((self.obj_space_y+self.obj_height)*i)), self.obj_width, self.obj_height),pixmap)

            elif self.moveRight_flag is True:
                if self.objPage_number == 2:
                    for i in range(3):
                        for k in range(8):
                            if k > 3:
                                self.imageNumber = self.backend.shelf[self.objPage_number-1,i,k-4].index
                                if self.backend.shelf[self.objPage_number-1,i,k-4].quantity == 0:
                                    pixmap = QtGui.QPixmap("./Inventory/" + "g" + str(self.imageNumber) + ".png")
                                else:
                                    pixmap = QtGui.QPixmap("./Inventory/" + str(self.imageNumber) + ".png")
                            else:
                                self.imageNumber = self.backend.shelf[self.objPage_number-2,i,k].index
                                if self.backend.shelf[self.objPage_number-2,i,k].quantity == 0:
                                    pixmap = QtGui.QPixmap("./Inventory/" + "g" + str(self.imageNumber) + ".png")
                                else:
                                    pixmap = QtGui.QPixmap("./Inventory/" + str(self.imageNumber) + ".png")
                            painter.drawPixmap(QtCore.QRect(int((self.border_width + ((self.obj_width+self.obj_space_x)*k)-self.movement_change_x_pos)-self.w_width), int(self.border_height +((self.obj_space_y+self.obj_height)*i)), self.obj_width, self.obj_height),pixmap)

                else:
                    for i in range(3):
                        for k in range(4):
                            self.imageNumber = self.backend.shelf[self.objPage_number-1,i,k].index
                            if self.backend.shelf[self.objPage_number-1,i,k].quantity == 0:
                                pixmap = QtGui.QPixmap("./Inventory/" + "g" + str(self.imageNumber) + ".png")
                            else:
                                pixmap = QtGui.QPixmap("./Inventory/" + str(self.imageNumber) + ".png")
                            painter.drawPixmap(QtCore.QRect(int(self.border_width + ((self.obj_width+self.obj_space_x)*k)), int(self.border_height +((self.obj_space_y+self.obj_height)*i)), self.obj_width, self.obj_height),pixmap)

        else:
            for i in range(3):
                for k in range(4):
                    self.imageNumber = self.backend.shelf[self.objPage_number-1,i,k].index
                    if self.backend.shelf[self.objPage_number-1,i,k].quantity == 0:
                        pixmap = QtGui.QPixmap("./Inventory/" + "g" + str(self.imageNumber) + ".png")
                    else:
                        pixmap = QtGui.QPixmap("./Inventory/" + str(self.imageNumber) + ".png")
                    painter.drawPixmap(QtCore.QRect(int(self.border_width + ((self.obj_width+self.obj_space_x)*k)), int(self.border_height +((self.obj_space_y+self.obj_height)*i)), self.obj_width, self.obj_height),pixmap)

        if self.objSelected_flag is True:
            if self.objPage_number == 1:
                self.imageNumber = self.backend.shelf[self.objPage_number-1,self.obj_added_row,self.obj_added_col].index
                pixmap_select = QtGui.QPixmap("./Inventory/" + str(self.imageNumber) + ".png")
            else:
                self.imageNumber = self.backend.shelf[self.objPage_number-1,self.obj_added_row,self.obj_added_col].index
                pixmap_select = QtGui.QPixmap("./Inventory/" + str(self.imageNumber) + ".png")

            for i in range(3):
                for k in range(4):
                    self.imageNumber = self.backend.shelf[self.objPage_number-1,i,k].index
                    if self.backend.shelf[self.objPage_number-1,i,k].quantity == 0:
                        pixmap = QtGui.QPixmap("./Inventory/" + "g" + str(self.imageNumber) + ".png")
                    else:
                        pixmap = QtGui.QPixmap("./Inventory/" + str(self.imageNumber) + ".png")
                    painter.drawPixmap(QtCore.QRect(int(self.border_width + ((self.obj_width+self.obj_space_x)*k)), int(self.border_height +((self.obj_space_y+self.obj_height)*i)), self.obj_width, self.obj_height),pixmap)
            painter.drawPixmap(QtCore.QRect(self.mouse_x_pos, self.mouse_y_pos, self.obj_width, self.obj_height),pixmap_select)
  

        if self.objChange_flag is True:
            for i in range(3):
                for k in range(4):
                    self.imageNumber = self.backend.shelf[self.objPage_number-1,i,k].index
                    if self.backend.shelf[self.objPage_number-1,i,k].quantity == 0:
                            pixmap = QtGui.QPixmap("./Inventory/" + "g" + str(self.imageNumber) + ".png")
                    else:
                            pixmap = QtGui.QPixmap("./Inventory/" + str(self.imageNumber) + ".png")
                    painter.drawPixmap(QtCore.QRect(int(self.border_width + ((self.obj_width+self.obj_space_x)*k)), int(self.border_height +((self.obj_space_y+self.obj_height)*i)), self.obj_width, self.obj_height),pixmap)
            self.objChange_flag = False

    def mousePressEvent(self, event):
        self.mouse_x_pos = event.x()
        self.mouse_y_pos = event.y()

        self.prev_mouse_x_pos = event.x()
        self.prev_mouse_y_pos = event.y()

        for i in range(3):
            obj_y_position = self.border_height+((self.obj_height+self.obj_space_y)*i)

            if((self.mouse_y_pos > obj_y_position) and (self.mouse_y_pos < obj_y_position + self.obj_height)):
                for k in range(4):
                    obj_x_position = self.border_width+((self.obj_width+self.obj_space_x)*k)

                    if((self.mouse_x_pos > obj_x_position) and (self.mouse_x_pos < obj_x_position + self.obj_width)):
                        self.timer.timeout.connect(self.longPressed)
                        self.timer.start(350)
                        self.obj_added_row = i
                        self.obj_added_col = k
                        self.objRelease_flag = False
                        break

        self.objMove_flag = True    

    def mouseMoveEvent(self, event):
        self.mouse_x_pos = event.x()
        self.mouse_y_pos = event.y()

        if self.objSelected_flag is True:
            self.update()

        if(self.mouse_y_pos < self.basket_border_height):
            if self.objMove_flag is True:
                self.movement_change_x_pos = self.prev_mouse_x_pos - self.mouse_x_pos
                if(self.movement_change_x_pos > 0):
                    self.moveLeft_flag = True
                    self.moveRight_flag = False
                else:
                    self.moveRight_flag = True
                    self.moveLeft_flag = False
        
            if(self.mouse_x_pos < self.w_width) and (self.mouse_x_pos > 0):
                self.update()


    def mouseReleaseEvent(self, event):
        self.mouse_x_pos = event.x()
        self.mouse_y_pos = event.y()

        if self.objSelected_flag is True:
            if((self.mouse_y_pos > self.basket_border_height) and (self.mouse_y_pos < self.basket_border_height + self.basket_height )):
                if((self.mouse_x_pos > self.basket_border_width) and (self.mouse_x_pos < self.basket_border_width + self.basket_width )):
                    self.backend.add_item_to_basket(self.backend.shelf[self.objPage_number-1, self.obj_added_row, self.obj_added_col].index,1)
                    print("Quantity: ", self.backend.shelf[self.objPage_number-1, self.obj_added_row, self.obj_added_col].quantity)
                    self.obj_count += 1
        
        if self.objPage_number == 1:
            if self.prev_mouse_x_pos > (self.w_width/2):
                if self.movement_change_x_pos > 0:
                    self.objPage_number = 2
        else:
            if self.prev_mouse_x_pos < (self.w_width/2):
                if self.movement_change_x_pos < 0:
                    self.objPage_number = 1


        self.objChange_flag = True
        self.objRelease_flag = True
        self.objSelected_flag = False 
        self.objMove_flag = False
        self.update()

    def longPressed(self):
        uncertainty = 5

        if(( self.prev_mouse_x_pos + uncertainty >= self.mouse_x_pos) and (self.prev_mouse_x_pos - uncertainty <= self.mouse_x_pos ) and ( self.prev_mouse_y_pos + uncertainty >= self.mouse_y_pos) and (self.prev_mouse_y_pos - uncertainty <= self.mouse_y_pos )):
            if self.backend.shelf[self.objPage_number-1,self.obj_added_row,self.obj_added_col].quantity != 0:
                self.objSelected_flag = True
            else:
                self.objSelected_flag = False
            #self.objSelected_flag = True
            self.objMove_flag = False
            if self.objRelease_flag is False:
                self.update()
        else:
            self.objMove_flag = True

        self.timer.stop()  


if __name__ == '__main__':
    app = QApplication(sys.argv)
    w = MyItems()
    w.show()
    sys.exit(app.exec_())