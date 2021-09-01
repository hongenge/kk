from PyQt5 import QtCore, QtGui, QtWidgets
from add_ui import Ui_AddForm
import sqlite3
import sys
import argparse

#创建数据库
def create_ok():
    conn = sqlite3.connect("data.db")
    c = conn.cursor()
    c.execute("CREATE TABLE IF NOT EXISTS t1(id INTEGER PRIMARY KEY,title TEXT,label TEXT,note TEXT)")
    conn.commit()
    conn.close()
    print("数据库创建成功！")


#删除
def delete(id):
    conn = sqlite3.connect("data.db")
    c = conn.cursor()
    c.execute("DELETE from t1 where id=?;",(id))
    conn.commit()
    conn.close()
    print("删除成功！")

#获取全部记录方法
def select_all():
    conn = sqlite3.connect("data.db")
    c = conn.cursor()
    cursor = c.execute("select * from t1")
    for row in cursor:
        print(row[0],row[1],row[2])
    conn.close()

#查找
def select(str1):
    conn = sqlite3.connect("data.db")
    c = conn.cursor()
    sql = "select * from t1 where title like'{}%'".format(str1)
    cursor = c.execute(sql)
    for row in cursor:
        print(row[0],row[1],row[2])
    conn.close()


#添加界面
class MainWindow(QtWidgets.QMainWindow,Ui_AddForm):

    def __init__(self,parent=None):
        super(MainWindow, self).__init__(parent)
        self.setupUi(self)
        self.pushButton.clicked.connect(self.ok_btn)

    #添加数据按钮
    def ok_btn(self):
        title_text = self.lineEdit_Title.text()
        label_text = self.lineEdit_Lable.text()
        note_text = self.textEdit_Note.toPlainText()
        self.insert_ok(title_text,label_text,note_text)
        self.lineEdit_Title.setText("")
        self.lineEdit_Lable.setText("")
        self.textEdit_Note.setText("")
    

    #添加数据方法
    def insert_ok(self,title,label,note):
        conn = sqlite3.connect("data.db")
        c = conn.cursor()
        c.execute("INSERT INTO t1 (title,label,note) VALUES (?,?,?)",(title,label,note))
        conn.commit()
        conn.close()
        print("数据写入成功！")



#修改界面
class EditWindow(QtWidgets.QMainWindow,Ui_AddForm):
    id = ''
    def __init__(self,parent=None,id=''):
        super(EditWindow, self).__init__(parent)
        self.setupUi(self)
        _translate = QtCore.QCoreApplication.translate
        self.setWindowTitle(_translate("AddForm", "修改"))
        self.pushButton.setText(_translate("AddForm", "修改"))
        self.pushButton.clicked.connect(self.ok_btn)
        self.id = id
        print("ID:%s"%self.id)
        self.select_one(id)
    #添加数据按钮
    def ok_btn(self):
        title_text = self.lineEdit_Title.text()
        label_text = self.lineEdit_Lable.text()
        note_text = self.textEdit_Note.toPlainText()
        self.update(title_text,label_text,note_text)
        self.lineEdit_Title.setText("")
        self.lineEdit_Lable.setText("")
        self.textEdit_Note.setText("")


    #修改方法
    def update(self,title,label,note):
        conn = sqlite3.connect("data.db")
        c = conn.cursor()
        c.execute("UPDATE t1 SET title=?,label=?,note=? WHERE id=?",(title,label,note,self.id))
        conn.commit()
        conn.close()
        print("修改成功！")
        sys.exit(0)

    
    #获取第一条记录
    def select_one(self,id):
        conn = sqlite3.connect("data.db")
        c = conn.cursor()
        try:
            sql = "select * from t1 where id={}".format(id)
            print(sql)
            c.execute(sql)
            res = c.fetchone()
            print(res)
            self.lineEdit_Title.setText(res[1])
            self.lineEdit_Lable.setText(res[2])
            self.textEdit_Note.setText(res[3])
        except:
            print("修改失败，请检查参数是否错误。")
            sys.exit(0)
        conn.commit()
        conn.close()


parser = argparse.ArgumentParser(description='参数说明')
parser.add_argument('--add', help="添加",action="store_true")
parser.add_argument('--list', help="获取全部记录",action="store_true")
parser.add_argument('--search', type=str,required=False,help='搜索要查找的内容')
parser.add_argument('--delete', type=str,required=False,help='删除的ID')
parser.add_argument('--edit', type=str,required=False,help='修改')
parser.add_argument('--create_ok', help="创建数据库",action="store_true")
args = parser.parse_args()
# print(args)


if __name__ == '__main__':
    #创建数据库
    if args.create_ok:
        create_ok()
    #添加
    if args.add:
        print("添加数据：")
        app = QtWidgets.QApplication(sys.argv)
        main = MainWindow()
        main.show()
        sys.exit(app.exec_())
    #修改
    if args.edit:
        print("修改数据：")
        app = QtWidgets.QApplication(sys.argv)
        main = EditWindow(id=args.edit)
        main.show()
        sys.exit(app.exec_())

    #获取全部
    if args.list:
        select_all()
    #查找
    if args.search:
        select(args.search)

    #删除
    if args.delete:
        delete(args.delete)




# create_ok()
# insert_ok()
# select_all()
# search()