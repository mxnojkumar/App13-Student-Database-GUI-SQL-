from PyQt6.QtWidgets import QApplication, QLabel, QWidget, QGridLayout, QLineEdit, QPushButton, QComboBox
import sys

class AverageSpeed(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Average Speed Calculator") # Set window title
        grid = QGridLayout() # Create a grid layout instance
        
        # Create widgets
        distance_label = QLabel("Distance:")
        self.distance_line_edit = QLineEdit()
        self.combo_box = QComboBox() # Create a combo instance
        self.combo_box.addItems(['Imperial (miles)', 'Metric (km)']) # Add the entities
        
        time_label = QLabel("Time (hours):")
        self.time_line_edit = QLineEdit()
        
        calculate_button = QPushButton("Calculate")
        calculate_button.clicked.connect(self.calculate)
        
        self.output_label = QLabel("")
        
        # Add the widgets to the grid
        grid.addWidget(distance_label, 0, 0)
        grid.addWidget(self.distance_line_edit, 0, 1)
        grid.addWidget(self.combo_box, 0, 2)
        grid.addWidget(time_label, 1, 0)
        grid.addWidget(self.time_line_edit, 1, 1)
        grid.addWidget(calculate_button, 2, 1)
        grid.addWidget(self.output_label, 3, 0, 1, 3)
        
        self.setLayout(grid)
        
    def calculate(self):
        distance = float(self.distance_line_edit.text())
        time = float(self.time_line_edit.text())
        speed = distance / time
        
        if self.combo_box.currentText() == 'Imperial (miles)':
            speed = round(speed * 0.621371, 2)
            unit = 'mph'
        if self.combo_box.currentText() == 'Metric (km)':
            speed = round(speed, 2)
            unit = 'kmph'
            
        self.output_label.setText(f"Average Speed: {speed} {unit}")
        
app = QApplication(sys.argv)
average_speed = AverageSpeed()
average_speed.show()
sys.exit(app.exec())