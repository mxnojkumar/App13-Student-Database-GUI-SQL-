from PyQt6.QtWidgets import QApplication, QLabel, QWidget, QGridLayout, QLineEdit, QPushButton
import sys
from datetime import datetime

class AgeCalculator(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Age Calculator") #Set a title for the window
        grid = QGridLayout() # Make a layout
        
        # Create labels
        name_label = QLabel("Name:")
        self.name_line_edit = QLineEdit()
        
        birthdate_label = QLabel("Date of birth MM/DD/YYYY:")
        self.birthdate_line_edit = QLineEdit()
        
        calculate_button = QPushButton("Calculate Age")
        calculate_button.clicked.connect(self.calculate)
        self.output_label = QLabel("")
        
        # Add widgets to the grid
        grid.addWidget(name_label, 0, 0)
        grid.addWidget(self.name_line_edit, 0, 1)
        grid.addWidget(birthdate_label, 1, 0)
        grid.addWidget(self.birthdate_line_edit, 1, 1)
        grid.addWidget(calculate_button, 2, 0, 1, 2)
        grid.addWidget(self.output_label, 3, 0 , 1, 2)
        
        self.setLayout(grid) # Set the widgets to the grid layout
        
    def calculate(self):
        current_year = datetime.now().year
        birth_date = self.birthdate_line_edit.text()
        birth_year = datetime.strptime(birth_date, "%m/%d/%Y").date().year
        age = current_year - birth_year
        self.output_label.setText(f"{self.name_line_edit.text()} is {age} years old.")
        
        
app = QApplication(sys.argv)
age_calculator = AgeCalculator()
age_calculator.show()
sys.exit(app.exec())
