import sys
from PyQt5.QtWidgets import (
    QApplication, QWidget, QLabel, QLineEdit, QPushButton, 
    QVBoxLayout, QHBoxLayout, QListWidget, QMessageBox, QFrame
)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont, QIcon

class GradingSystem(QWidget):
    def __init__(self):
        super().__init__()
        self.grades = []
        self.init_ui()

    def init_ui(self):
        self.setWindowTitle("Grading System")
        self.resize(520, 660) 
        
        self.setWindowIcon(QIcon("logo.png"))
        
        self.setStyleSheet("""
            .GradingSystem {
                background-color: #f8f9fa;
            }
            
            QLabel {
                font-family: 'Segoe UI', Arial, sans-serif;
                font-size: 18px;
                font-weight: normal;
                color: #212529;
                background-color: transparent;
            }
            
            QLineEdit {
                background-color: #ffffff;
                border: 2px solid #ced4da;
                border-radius: 8px;
                padding: 10px 14px;
                min-height: 30px;
                color: #212529;
                font-size: 18px;
                font-family: 'Segoe UI', Arial, sans-serif;
            }
            QLineEdit:focus {
                border: 2px solid #4dadf7;
            }
            
            QPushButton#btn_add, QPushButton#btn_calculate {
                background-color: #339af0;
                color: #ffffff;
                border: none;
                border-radius: 8px;
                padding: 10px 14px;
                min-height: 30px;
                font-weight: bold;
                font-size: 18px;
                font-family: 'Segoe UI', Arial, sans-serif;
            }
            QPushButton#btn_add:hover, QPushButton#btn_calculate:hover {
                background-color: #228be6;
            }
            
            QPushButton#btn_clear {
                background-color: #ff6b6b;
                color: #ffffff;
                border: none;
                border-radius: 8px;
                padding: 10px 14px;
                min-height: 30px;
                font-weight: bold;
                font-size: 18px;
                font-family: 'Segoe UI', Arial, sans-serif;
            }
            QPushButton#btn_clear:hover {
                background-color: #fa5252;
            }
            
            QListWidget {
                background-color: #ffffff;
                border: 2px solid #e9ecef;
                border-radius: 8px;
                padding: 8px;
                font-size: 18px;
                color: #212529;
                font-family: 'Segoe UI', Arial, sans-serif;
            }
            
            QFrame#result_card {
                background-color: #ffffff;
                border-radius: 10px;
                border: 2px solid #e9ecef;
            }
        """)

        main_layout = QVBoxLayout()
        main_layout.setSpacing(18)
        main_layout.setContentsMargins(25, 25, 25, 25)

        lbl_title = QLabel("Grading System")
        lbl_title.setFont(QFont('Segoe UI', 32, QFont.Bold))
        lbl_title.setStyleSheet("color: #1c7ed6; margin-bottom: 5px; background-color: transparent; font-weight: bold;")
        lbl_title.setAlignment(Qt.AlignCenter)
        main_layout.addWidget(lbl_title)

        input_layout = QHBoxLayout()
        input_layout.setAlignment(Qt.AlignVCenter) 
        
        self.grade_input = QLineEdit()
        self.grade_input.setPlaceholderText("Enter a grade (0 - 100)")
        self.grade_input.returnPressed.connect(self.add_grade)
        
        btn_add = QPushButton("Add Grade")
        btn_add.setObjectName("btn_add") 
        btn_add.setCursor(Qt.PointingHandCursor) 
        btn_add.clicked.connect(self.add_grade)
        
        input_layout.addWidget(self.grade_input, stretch=4)
        input_layout.addWidget(btn_add, stretch=2) 
        main_layout.addLayout(input_layout)

        lbl_list = QLabel("Grades registered in the period:")
        lbl_list.setFont(QFont('Segoe UI', 15, QFont.Medium))
        main_layout.addWidget(lbl_list)
        
        self.visual_list = QListWidget()
        main_layout.addWidget(self.visual_list)

        actions_layout = QHBoxLayout()
        
        btn_calculate = QPushButton("Calculate Academic Status")
        btn_calculate.setObjectName("btn_calculate") 
        btn_calculate.setCursor(Qt.PointingHandCursor) 
        btn_calculate.clicked.connect(self.calculate_status)
        
        btn_clear = QPushButton("Reset")
        btn_clear.setObjectName("btn_clear") 
        btn_clear.setCursor(Qt.PointingHandCursor) 
        btn_clear.clicked.connect(self.clear_all)
        
        actions_layout.addWidget(btn_calculate, stretch=3)
        actions_layout.addWidget(btn_clear, stretch=1)
        main_layout.addLayout(actions_layout)

        self.result_card = QFrame()
        self.result_card.setObjectName("result_card")
        result_layout = QVBoxLayout(self.result_card)
        result_layout.setContentsMargins(15, 15, 15, 15)
        
        self.lbl_average = QLabel("Average: —")
        self.lbl_average.setFont(QFont('Segoe UI', 20, QFont.Bold))
        
        self.lbl_status = QLabel("Status: —")
        self.lbl_status.setFont(QFont('Segoe UI', 15))
        self.lbl_status.setWordWrap(True)
        
        result_layout.addWidget(self.lbl_average)
        result_layout.addWidget(self.lbl_status)
        main_layout.addWidget(self.result_card)

        self.setLayout(main_layout)

    def add_grade(self):
        text = self.grade_input.text().strip()
        
        try:
            grade = float(text)
            if 0 <= grade <= 100:
                self.grades.append(grade)
                self.visual_list.addItem(f"Grade {len(self.grades)}: {grade:.1f}")
                self.grade_input.clear()
                self.grade_input.setFocus()
            else:
                QMessageBox.warning(self, "Range Error", "The grade must be between 0 and 100.")
        except ValueError:
            QMessageBox.critical(self, "Type Error", "Please enter a valid number.")
            self.grade_input.clear()

    def calculate_status(self):
        if not self.grades:
            QMessageBox.information(self, "No Data", "Please add at least one grade first.")
            return

        total_grades = len(self.grades)
        grades_sum = sum(self.grades)
        average = grades_sum / total_grades

        self.lbl_average.setText(f"Average: {average:.2f}")

        if average >= 90:
            status = "Excellent"
            border_color = "#40c057"
            background_color = "#ebfbee"
        elif average >= 75:
            status = "Good."
            border_color = "#fab005"
            background_color = "#fff9db"
        elif average >= 60:
            status = "Regular"
            border_color = "#fd7e14"
            background_color = "#fff4e6"
        else:
            status = "Insufficient"
            border_color = "#fa5252"
            background_color = "#fff5f5"

        self.lbl_status.setText(f"Status: {status}")
        
        self.result_card.setStyleSheet(f"""
            QFrame#result_card {{ 
                background-color: {background_color};
                border: 2px solid {border_color}; 
            }}
        """)

    def clear_all(self):
        self.grades.clear()
        self.visual_list.clear()
        self.grade_input.clear()
        self.lbl_average.setText("Average: —")
        self.lbl_status.setText("Status: —")
        self.result_card.setStyleSheet("""
            QFrame#result_card { 
                background-color: #ffffff;
                border: 2px solid #e9ecef; 
            }
        """)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = GradingSystem()
    window.show()
    sys.exit(app.exec())