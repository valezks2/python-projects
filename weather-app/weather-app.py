import sys
import os
import requests
from dotenv import load_dotenv
from PyQt5.QtWidgets import (QApplication, QWidget, QVBoxLayout, QHBoxLayout, 
                             QLineEdit, QPushButton, QLabel, QDesktopWidget)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont, QIcon

load_dotenv()

class WeatherApp(QWidget):
    def __init__(self):
        super().__init__()
        self.init_ui()
        
    def init_ui(self):
        self.setWindowTitle("Weather App")
        
        self.setFixedSize(350, 250)
        
        self.setStyleSheet("background-color: #f4f4f9;")
        self.setWindowIcon(QIcon("logo.png"))
        self.center_window()
        
        main_layout = QVBoxLayout()
        main_layout.setContentsMargins(20, 20, 20, 20)
        main_layout.setSpacing(15)
        
        search_layout = QHBoxLayout()
        search_layout.setSpacing(8)
        
        self.city_input = QLineEdit()
        self.city_input.setPlaceholderText("Enter a city... (e.g., London)")
        self.city_input.setStyleSheet("padding-left: 8px; padding-right: 8px; border: 1px solid #ccc; border-radius: 4px; background-color: white;")
        self.city_input.setFixedHeight(35)
        self.city_input.returnPressed.connect(self.get_weather)
        
        btn_search = QPushButton("Search")
        btn_search.setCursor(Qt.PointingHandCursor)
        btn_search.setStyleSheet("""
            QPushButton {
                background-color: #007acc; 
                color: white; 
                padding-left: 15px; 
                padding-right: 15px; 
                border: none; 
                border-radius: 4px; 
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #0066aa;
            }
        """)
        btn_search.setFixedHeight(35)
        btn_search.clicked.connect(self.get_weather)
        
        self.lbl_city = QLabel("How's the weather?")
        self.lbl_city.setFont(QFont("Arial", 14, QFont.Bold))
        self.lbl_city.setAlignment(Qt.AlignCenter)
        
        self.lbl_temp = QLabel("-- °C")
        self.lbl_temp.setFont(QFont("Arial", 28, QFont.Bold))
        self.lbl_temp.setAlignment(Qt.AlignCenter)
        self.lbl_temp.setStyleSheet("color: #007acc;")
        
        self.lbl_desc = QLabel("Enter a city to check the weather")
        self.lbl_desc.setFont(QFont("Arial", 10, QFont.StyleItalic))
        self.lbl_desc.setAlignment(Qt.AlignCenter)
        self.lbl_desc.setStyleSheet("color: #555;")
        
        search_layout.addWidget(self.city_input)
        search_layout.addWidget(btn_search)
        
        main_layout.addLayout(search_layout)
        
        main_layout.addStretch()
        main_layout.addWidget(self.lbl_city)
        main_layout.addWidget(self.lbl_temp)
        main_layout.addWidget(self.lbl_desc)
        main_layout.addStretch()
        
        self.setLayout(main_layout)
        
    def center_window(self):
        window_geometry = self.frameGeometry()
        screen_center = QDesktopWidget().availableGeometry().center()
        window_geometry.moveCenter(screen_center)
        self.move(window_geometry.topLeft())
        
    def get_weather(self):
        city = self.city_input.text().strip()
        if not city:
            self.lbl_desc.setText("Please, type something")
            return
            
        api_key = os.getenv("OPENWEATHER_API_KEY")
        
        if not api_key:
            self.lbl_city.setText("Missing Configuration")
            self.lbl_desc.setText("OPENWEATHER_API_KEY not found in your .env file")
            return

        url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric&lang=en"
        
        try:
            res = requests.get(url).json()
            
            if str(res.get("cod")) == "200":
                city_name = res["name"]
                country = res["sys"]["country"]
                temp = round(res["main"]["temp"])
                description = res["weather"][0]["description"].capitalize()
                
                self.lbl_city.setText(f"{city_name}, {country}")
                self.lbl_temp.setText(f"{temp}°C")
                self.lbl_desc.setText(description)
            else:
                self.lbl_city.setText("Oops...")
                self.lbl_temp.setText("-- °C")
                error_message = res.get("message", "city not found").capitalize()
                self.lbl_desc.setText(error_message)
                
        except requests.exceptions.RequestException:
            self.lbl_desc.setText("Network connection error")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = WeatherApp()
    window.show()
    sys.exit(app.exec_())