from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QMainWindow, QApplication, QWidget, QLabel, QLineEdit, QGridLayout, \
     QPushButton, QTableWidget, QTableWidgetItem, QDialog, QVBoxLayout, QComboBox, QToolBar, \
     QStatusBar, QMessageBox
from PyQt6.QtGui import QAction, QIcon
import sys
import sqlite3
import mysql.connector
import os

PASSWORD = os.getenv("MYSQL_PASS")

class DatabaseConnection():
    def __init__(self, host="localhost", user="root", password=PASSWORD, database="school"):
        self.host = host
        self.user = user
        self.password = password
        self.database = database
        
    def connection(self):
        connection = mysql.connector.connect(host=self.host, user=self.user, 
                                             password=self.password, database=self.database)
        return connection


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        
        """Start adding elements to the main window"""
        self.setWindowTitle("Student Management System")
        self.setMinimumSize(800, 600)
        
        # Add menu bar items with actions (add, search)
        file_menu_item = self.menuBar().addMenu('&File')
        help_menu_item = self.menuBar().addMenu('&Help')
        edit_menu_item = self.menuBar().addMenu('&Edit')
        
        add_student_action = QAction(QIcon("icons/add.png"), "Add Student", self)
        add_student_action.triggered.connect(self.insert) # Insert method defined below
        file_menu_item.addAction(add_student_action)
        
        about_action = QAction("About", self)
        help_menu_item.addAction(about_action)
        about_action.triggered.connect(self.about)
        
        search_student_action = QAction(QIcon("icons/search.png"), "Search", self)
        search_student_action.triggered.connect(self.search) # Search method defined below
        edit_menu_item.addAction(search_student_action) 
        
        # Add table to the main window
        self.table = QTableWidget()
        self.table.setColumnCount(4)
        self.table.setHorizontalHeaderLabels(("Id", "Name", "Course", "Mobile"))
        self.table.verticalHeader().setVisible(False)
        self.setCentralWidget(self.table)
        
        # Create toolbar and add elements
        toolbar = QToolBar()
        toolbar.setMovable(True)
        self.addToolBar(toolbar)
        
        toolbar.addAction(add_student_action)
        toolbar.addAction(search_student_action)
        
        # Add status bar with elements
        self.statusbar = QStatusBar()
        self.setStatusBar(self.statusbar)
        
        # Detect any cell click 
        self.table.cellClicked.connect(self.cell_clicked)
        
    def cell_clicked(self): # Diverts to edit or delete method
        edit_button = QPushButton("Edit Record")
        edit_button.clicked.connect(self.edit)
        
        delete_button = QPushButton("Delete Record")
        delete_button.clicked.connect(self.delete)
        
        children = self.findChildren(QPushButton)
        if children:
            for child in children:
                self.statusbar.removeWidget(child)
        
        self.statusbar.addWidget(edit_button)
        self.statusbar.addWidget(delete_button)
        
    def load_data(self): # Loads the data from the database
        connection = DatabaseConnection().connection()
        cursor = connection.cursor()
        cursor.execute("SELECT * FROM students")
        result = cursor.fetchall()
        self.table.setRowCount(0)
        for row_number, row_data in enumerate(result):
            self.table.insertRow(row_number)
            for column_number, data in enumerate(row_data):
                self.table.setItem(row_number, column_number, QTableWidgetItem(str(data)))
        connection.close()
        
    def insert(self): # Instance for insert dialog
        dialog = InsertDialog()
        dialog.exec()
        
    def search(self): # Instance for search dialog
        dialog = SearchDialog()
        dialog.exec()
      
    def edit(self):
        dialog = EditDialog()
        dialog.exec()
        
    def delete(self):
        dialog = DeleteDialog()
        dialog.exec()
        
    def about(self):
        dialog = AboutDialog()
        dialog.exec()
        

class AboutDialog(QMessageBox):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("About")
        content = """
        This is a minimalistic model of Student Database Management.
        This is built using the PyQt6 GUI.
        And it has common features like insert, edit, search and delete.
        """
        self.setText(content)
    
class InsertDialog(QDialog): # Structure of insert dialog/popup
    
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Insert Student Data")
        self.setFixedWidth(300)
        self.setFixedHeight(300)
        
        layout = QVBoxLayout()
        
        # Add student name widget
        self.student_name = QLineEdit()
        self.student_name.setPlaceholderText("Name")
        layout.addWidget(self.student_name)
        
        # Add course name combo box
        self.course_name = QComboBox()
        courses = ['Biology', 'Math', 'Astronomy', 'Physics']
        self.course_name.addItems(courses)
        layout.addWidget(self.course_name)
        
        # Add student name widget
        self.mobile_number = QLineEdit()
        self.mobile_number.setPlaceholderText("Mobile number")
        layout.addWidget(self.mobile_number)
        
        # Add a submit button
        button = QPushButton("Register")
        button.clicked.connect(self.add_student) # Add student method defined below
        layout.addWidget(button)
        
        self.setLayout(layout)
        
    def add_student(self): # Add new student to database
        name = self.student_name.text()
        course = self.course_name.itemText(self.course_name.currentIndex())
        mobile = self.mobile_number.text()
    
        connection = DatabaseConnection().connection()
        cursor = connection.cursor()
        cursor.execute("INSERT INTO students (name, course, mobile) VALUES (%s, %s, %s)", 
                       (name, course, mobile))
        connection.commit()
        cursor.close()
        connection.close()
        main_window.load_data()
        
        
class SearchDialog(QDialog): # Structure of search dialog/popup
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Search Student Name")
        self.setFixedWidth(300)
        self.setFixedHeight(300)
        
        layout = QVBoxLayout()
        
        # Add student name widget
        self.student_name = QLineEdit()
        self.student_name.setPlaceholderText("Name")
        layout.addWidget(self.student_name)
        
        # Add a Search button
        button = QPushButton("Search")
        button.clicked.connect(self.search)
        layout.addWidget(button)
        
        self.setLayout(layout)
        
    def search(self):
        name = self.student_name.text()
        connection = DatabaseConnection().connection()
        cursor = connection.cursor()
        cursor.execute("SELECT * FROM students WHERE name = %s", (name, ))
        result = cursor.fetchall()
        rows = list(result)
        print(rows)
        items = main_window.table.findItems(name, Qt.MatchFlag.MatchFixedString)
        for item in items:
            print(item.text())
            main_window.table.item(item.row(), 1 ).setSelected(True) # item(row_index, column_index)
            
        cursor.close()
        connection.close()
        

class EditDialog(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Update Student Record")
        self.setFixedWidth(300)
        self.setFixedHeight(300) 

        layout = QVBoxLayout()
        
        # Get current student name
        index = main_window.table.currentRow()
        student_name = main_window.table.item(index, 1).text()
        # Get id of student
        self.student_id = main_window.table.item(index, 0).text()
        
        # Get current student name widget
        self.student_name = QLineEdit(student_name)
        self.student_name.setPlaceholderText("Name")
        layout.addWidget(self.student_name)
        
        # Get current course name
        course_name = main_window.table.item(index,2).text()
        # Add course name combo box
        self.course_name = QComboBox()
        courses = ['Biology', 'Math', 'Astronomy', 'Physics']
        self.course_name.addItems(courses)
        self.course_name.setCurrentText(course_name)
        layout.addWidget(self.course_name)
        
        # Get current mobile number
        mobile_number = main_window.table.item(index, 3).text()
        # Add student name widget
        self.mobile_number = QLineEdit(mobile_number)
        self.mobile_number.setPlaceholderText("Mobile number")
        layout.addWidget(self.mobile_number)
        
        # Add a update button
        button = QPushButton("Update")
        button.clicked.connect(self.update_student) # Update student method defined below
        layout.addWidget(button)
        
        self.setLayout(layout)
        
    def update_student(self):
        # Updated values of the student
        name = self.student_name.text()
        course = self.course_name.itemText(self.course_name.currentIndex())
        mobile = self.mobile_number.text()
        id = self.student_id # Already converted to text()
        connection = DatabaseConnection().connection()
        cursor = connection.cursor()
        cursor.execute("UPDATE students SET name = %s, course = %s, mobile = %s WHERE id = %s", 
                       (name, course, mobile, id))  
        connection.commit()
        cursor.close()
        connection.close()
        main_window.load_data()
        
        self.close()
        
        confirmation_widget = QMessageBox()
        confirmation_widget.setWindowTitle("Updated")
        confirmation_widget.setText("The record is updated successfully!")
        confirmation_widget.exec()

class DeleteDialog(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Confirm delete")
        
        layout = QGridLayout()
        
        confirmation = QLabel("Are you sure you want to delete?")
        yes_button = QPushButton("Yes")
        no_button = QPushButton("No")
        
        layout.addWidget(confirmation, 0, 0, 1, 2)
        layout.addWidget(yes_button, 1, 0)
        layout.addWidget(no_button, 1, 1)
        
        self.setLayout(layout)
        
        yes_button.clicked.connect(self.delete_student)
        
    def delete_student(self):
        # Get selected row index and student id 
        index = main_window.table.currentRow()
        student_id = main_window.table.item(index, 0).text()
        
        connection = DatabaseConnection().connection()
        cursor = connection.cursor()
        cursor.execute("DELETE from students WHERE id = %s", (student_id,))
        connection.commit()
        cursor.close()
        connection.close()
        main_window.load_data()
        
        self.close()
        
        confirmation_widget = QMessageBox()
        confirmation_widget.setWindowTitle("Success")
        confirmation_widget.setText("The record was deleted successfully!")
        confirmation_widget.exec()
        

app = QApplication(sys.argv)
main_window = MainWindow()
main_window.load_data()
main_window.show()
sys.exit(app.exec())