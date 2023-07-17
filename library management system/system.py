from PyQt6.QtWidgets import QMainWindow, QApplication, QDialog, QMessageBox, QTableWidgetItem
from gui import Ui_MainWindow
from addbook import add_Dialog
from insertmember import insert_Dialog
from viewbooks import view_Dialog
from viewmember import member_Dialog
import mysql.connector as mc


class MainWindow(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)

        self.toolButton.clicked.connect(self.add_d)
        self.toolButton_2.clicked.connect(self.insert_m)
        self.toolButton_3.clicked.connect(self.view_b)
        self.toolButton_4.clicked.connect(self.view_m)
        self.book_id.returnPressed.connect(self.book_data)
        self.book_id_2.returnPressed.connect(self.member_data)
        self.toolButton_issue.clicked.connect(self.issue_book)
        self.lineEdit.returnPressed.connect(self.v_issue)
        self.toolButton_issue_3.clicked.connect(self.summit_b)
        self.toolButton_issue_2.clicked.connect(self.renew_b)
    def add_d(self):
        dialog = QDialog()
        md = add_Dialog()
        md.setupUi(dialog)
        dialog.exec()

    def insert_m(self):
        dialog = QDialog()
        im = insert_Dialog()
        im.setupUi(dialog)
        dialog.exec()

    def view_b(self):
        dialog = QDialog()
        vd = view_Dialog()
        vd.setupUi(dialog)
        dialog.exec()

    def view_m(self):
        dialog = QDialog()
        vm = member_Dialog()
        vm.setupUi(dialog)
        dialog.exec()

    def book_data(self):
        id = self.book_id.text()
        try:
            database = mc.connect(
                host="localhost",
                user="root",
                password="",
                database="library"
            )
            cursor = database.cursor()
            cursor.execute(f"SELECT * FROM l_data WHERE id = '"+id+"'")
            data = cursor.fetchall()
            for row in data:
                self.label.setText(f"Book Name: \n{row[0]}")
                self.label_2.setText(f"Book Author: \n{row[2]}")

        except mc.Error as e:
            return

    def member_data(self):
        id = self.book_id_2.text()
        try:
            database = mc.connect(
                host="localhost",
                user="root",
                password="",
                database="library"
            )
            cursor = database.cursor()
            cursor.execute( f"SELECT * FROM member WHERE id = '" + id + "'" )
            data = cursor.fetchall()
            for row in data:
                self.label_3.setText( f"Member Name: \n{row[1]}" )
                self.label_4.setText( f"Email: \n{row[3]}" )
        except mc.Error as e:
            return

    def issue_book(self):
        b_id = self.book_id.text()
        m_id = self.book_id_2.text()
        try:
            database = mc.connect(
                host="localhost",
                user="root",
                password="",
                database="library"
            )
            cursor = database.cursor()
            sql = "INSERT INTO tbl_issue (bookID, memberID) VALUES (%s,%s)"
            value = (b_id,m_id)
            sql2 = "UPDATE l_data SET isAvail = FALSE WHERE id = '"+b_id+"'"
            cursor.execute(sql,value)
            cursor.execute(sql2)
            database.commit()
            QMessageBox.about(self,"ISSUE BOOK","Issue book was a success")
        except mc.Error as e:
            print('error my friend')

    def v_issue(self):
        b_id = self.lineEdit.text()
        try:
            database = mc.connect(
                host="localhost",
                user="root",
                password="",
                database="library"
            )
            cursor = database.cursor()
            cursor.execute("SELECT * FROM tbl_issue WHERE bookID = '"+b_id+"'")
            data = cursor.fetchall()
            for row,result in enumerate(data):
                self.tableWidget.insertRow(row)
                for column, value in enumerate(result):
                    self.tableWidget.setItem(row,column,QTableWidgetItem(str(value)))
        except mc.Error as e:
            print('error')

    def summit_b(self):
        b_id = self.lineEdit.text()
        try:
            database = mc.connect(
                host="localhost",
                user="root",
                password="",
                database="library"
            )
            if b_id == "":
                return
            cursor = database.cursor()
            sql = "DELETE FROM tbl_issue WHERE bookID = '"+b_id+"'"
            cursor.execute(sql)
            cursor.execute("UPDATE l_data SET isAvail = TRUE WHERE id = '"+b_id+"'")
            database.commit()
            QMessageBox.about(self,"SUMMIT BOOK","Sir Your Book Have Been Summitted ")

        except:
            print('error')
    def renew_b(self):
        b_id = self.lineEdit.text()
        try:
            database = mc.connect(
                host="localhost",
                user="root",
                password="",
                database="library"
            )
            if b_id == "":
                QMessageBox.about(self,"About Book","Enter a Book Name Sir ")
                return
            cursor = database.cursor()
            cursor.execute("UPDATE tbl_issue SET issueTime = CURRENT_TIMESTAMP , renewCount = renewCount+1 WHERE bookID = '"+b_id+"'")
            database.commit()
            QMessageBox.about(self,"Renew Book","Book Have Been Successfully Renewed")
        except mc.Error as e:
            return