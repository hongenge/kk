import sys
from PyQt5 import QtCore, QtGui, QtWidgets
from ui import Ui_Form
import time
import keyboard  #监听键盘
import sqlite3
import win32con
import win32clipboard as w

class MainWindow(QtWidgets.QMainWindow,Ui_Form):
    conn = sqlite3.connect("data.db")
    res = []
    offset = 0
    str1 = ""
    def __init__(self,parent=None):
        super(MainWindow, self).__init__(parent)
        self.setupUi(self)
        _translate = QtCore.QCoreApplication.translate
        # self.pushButton.clicked.connect(self.ok_btn)
        self.lineEdit.textChanged.connect(self.on_edit_textChanged)
        self.lineEdit.returnPressed.connect(self.lineEdit_function)
        self.label.setText(_translate("Form", ""))
        self.label.setStyleSheet("color:RoyalBlue")
        # self.label.setStyleSheet("background-color: RoyalBlue ")


    #回车默认选择第一个
    def lineEdit_function(self):
        str1 = self.lineEdit.text()
        if len(str1)>=1:
            if len(self.res)>=1:
                # print(self.res[0])
                tmp_str = self.res[0][3]
                self.inputtxt(tmp_str)
                self.lineEdit.setText("")
        else:
            print("空的")
        self.ok_btn()

    def on_edit_textChanged(self):
        str1 = self.lineEdit.text()
        str1_len = len(str1)
        if str1_len>=1:
            str_end = str1[-1]
            if str_end.isdigit()==True:
                # print("按下数字")
                tmp_i = int(str_end)-1
                # print(tmp_i)
                # print(self.res)
                if len(self.res)>tmp_i:
                    # print(self.res[tmp_i])
                    tmp_str = self.res[tmp_i][3]
                    self.inputtxt(tmp_str)
                    self.ok_btn()
                    self.lineEdit.setText("")
                # self.lineEdit.setText(str1[0:-1])
            elif str_end=="=":
                print("按下的是=号")
                str1 = str1[0:-1]
                self.offset = self.offset+5
                self.str1 = str1
                self.lineEdit.setText(str1)
                
            elif str_end == "-":
                print("按下的是-号")
                str1 = str1[0:-1]
                self.offset = self.offset-5
                if self.offset <=0:
                    self.offset=0
                self.str1 = str1
                self.lineEdit.setText(str1)
                
            else:
                if self.str1 != str1:
                    self.offset=0
                _translate = QtCore.QCoreApplication.translate
                tmp_res = self.search(str1,offset=self.offset)
                self.upLabel(tmp_res)

        else:
            self.offset=0
            _translate = QtCore.QCoreApplication.translate
            self.label.setText(_translate("Form", ""))

            self.label.setGeometry(QtCore.QRect(0, 43, 756, 31))
            self.lineEdit.setGeometry(QtCore.QRect(0, 0, 756, 41))
            self.resize(756, 77)

    #渲染Label
    def upLabel(self,res):
        res_len = len(res)
        if res_len>=1:
            self.res = res
            _translate = QtCore.QCoreApplication.translate
            tmp_line = ''
            n = 1
            for row in res:
                # print(row)
                tmp_line = tmp_line+" "+str(n)+"."+row[2]
                # print(tmp_line)
                n = n+1
            self.label.setText(_translate("Form", tmp_line))

            txt_width = self.label.fontMetrics().boundingRect(tmp_line).width()+15
            if txt_width>=756:
                self.label.setGeometry(QtCore.QRect(0, 43, txt_width, 31))
                self.lineEdit.setGeometry(QtCore.QRect(0, 0, txt_width, 41))
                self.resize(txt_width, 77)
            else:
                self.label.setGeometry(QtCore.QRect(0, 43, 756, 31))
                self.lineEdit.setGeometry(QtCore.QRect(0, 0, 756, 41))
                self.resize(756, 77)

        else:
            self.offset = self.offset-5
            if self.offset <=0:
                self.offset=0

    def resizeEvent(self, event):
        w = event.size().width()
        # h = event.size().height()
        self.label.setGeometry(QtCore.QRect(0, 43, w, 31))
        self.lineEdit.setGeometry(QtCore.QRect(0, 0, w, 41))


    #写入剪贴板
    def inputtxt(self,string):
        w.OpenClipboard()
        w.EmptyClipboard()
        w.SetClipboardData(win32con.CF_UNICODETEXT,string)
        w.CloseClipboard()
        
    #隐藏窗口
    def ok_btn(self):
        print("隐藏窗口")
        self.hide()
        self.abc()

    #开始监听键盘
    def abc(self):
        if keyboard.wait(hotkey='ctrl+alt') == None:
            a = int(time.time())
            if keyboard.wait(hotkey='ctrl+alt') == None:
                b = int(time.time())
                if b-a<=1:
                    print("显示窗口")
                    self.show()
                else:
                    print("继续监听")
                    self.abc()
                
                

    def search(self,msg,offset=0):
        c = self.conn.cursor()
        sql = "select * from t1 where title like'{}%' limit 5 OFFSET {}".format(msg,offset)
        # print(sql)
        cursor = c.execute(sql)
        mlist = []
        for row in cursor:
            mlist.append(row)
        return mlist

    def closeEvent(self, event):
        print("窗口关闭了")
        self.conn.close()
        event.accept()

if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    main = MainWindow()
    main.setStyleSheet("#Form{background-color:white}")
    main.show()
    sys.exit(app.exec_())