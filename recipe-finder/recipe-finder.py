import sys
import requests
from PyQt5.QtWidgets import (QApplication, QWidget, QVBoxLayout, QHBoxLayout, 
    QLineEdit, QPushButton, QLabel, QTextBrowser, QFrame)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont, QPixmap, QIcon 

style = """
    QWidget {
        background-color: #FAFAFA;
    }
    QLabel {
        color: #1E293B;
    }
    #TitleLabel {
        color: #0F172A;
        font-weight: bold;
        margin-bottom: 5px;
    }
    QLineEdit {
        background-color: #FFFFFF;
        color: #1E293B;
        border: 2px solid #E2E8F0;
        border-radius: 12px;
        padding: 0px 15px;
        font-size: 14px;
    }
    QLineEdit:focus {
        border: 2px solid #2563EB;
    }
    QPushButton {
        background-color: #2563EB;
        color: #FFFFFF;
        border-radius: 12px;
        font-weight: bold;
        font-size: 14px;
        padding: 0px 20px;
    }
    QPushButton:hover {
        background-color: #1D4ED8;
    }
    QPushButton:pressed {
        background-color: #1E40AF;
    }
    #BtnRandom {
        background-color: #0D9488;
        color: #FFFFFF;
    }
    #BtnRandom:hover {
        background-color: #0F766E;
    }
    QTextBrowser {
        background-color: #FFFFFF;
        color: #334155;
        border: 2px solid #E2E8F0;
        border-radius: 15px;
        padding: 15px;
        font-size: 14px;
    }

    QScrollBar:vertical {
        border: none;
        background: #F1F5F9;
        width: 10px;
        margin: 4px 2px 4px 2px;
        border-radius: 4px;
    }
    QScrollBar::handle:vertical {
        background: #CBD5E1;
        min-height: 20px;
        border-radius: 4px;
    }
    QScrollBar::handle:vertical:hover {
        background: #94A3B8;
    }
    QScrollBar::add-page:vertical, QScrollBar::sub-page:vertical {
        background: none;
    }
    QScrollBar::sub-line:vertical, QScrollBar::add-line:vertical {
        border: none;
        background: none;
        height: 0px;
    }
"""

class RecipeManager(QWidget):
    def __init__(self):
        super().__init__()
        self.init_ui()
        
    def init_ui(self):
        self.setWindowTitle('Recipe Finder')
        self.setFixedSize(680, 680)
        self.setStyleSheet(style)
        
        self.setWindowIcon(QIcon('logo.png')) 

        main_layout = QVBoxLayout()
        main_layout.setContentsMargins(30, 30, 30, 30)
        main_layout.setSpacing(20)

        self.title = QLabel("Recipe Finder")
        self.title.setObjectName("TitleLabel")
        self.title.setFont(QFont("Urbanist", 22))
        self.title.setAlignment(Qt.AlignCenter)
        main_layout.addWidget(self.title)

        search_layout = QHBoxLayout()
        search_layout.setSpacing(10)
        
        row_height = 40

        self.recipe_input = QLineEdit()
        self.recipe_input.setPlaceholderText("Search for a recipe (e.g., Arrabiata, Burger)...")
        self.recipe_input.setFixedHeight(row_height)
        self.recipe_input.returnPressed.connect(self.search_recipe)
        
        self.btn_search = QPushButton("Search")
        self.btn_search.setCursor(Qt.PointingHandCursor)
        self.btn_search.setDefault(True)
        self.btn_search.setFixedHeight(row_height)
        self.btn_search.clicked.connect(self.search_recipe)
        
        self.btn_random = QPushButton("Surprise Me")
        self.btn_random.setObjectName("BtnRandom")
        self.btn_random.setCursor(Qt.PointingHandCursor)
        self.btn_random.setFixedHeight(row_height)
        self.btn_random.clicked.connect(self.get_random_recipe)
        
        search_layout.addWidget(self.recipe_input, stretch=4)
        search_layout.addWidget(self.btn_search, stretch=1)
        search_layout.addWidget(self.btn_random, stretch=1)
        main_layout.addLayout(search_layout)

        self.info_frame = QFrame()
        info_layout = QHBoxLayout(self.info_frame)
        info_layout.setContentsMargins(0, 0, 0, 0)
        info_layout.setSpacing(15)
        
        self.img_dish = QLabel()
        self.img_dish.setFixedSize(110, 110)
        self.img_dish.setStyleSheet("background-color: #FFFFFF; border-radius: 15px; border: 2px solid #E2E8F0;")
        self.img_dish.setAlignment(Qt.AlignCenter)
        
        text_info_layout = QVBoxLayout()
        text_info_layout.setSpacing(6)
        
        self.label_name = QLabel("Find your next meal")
        self.label_name.setFont(QFont("Urbanist", 14, QFont.Bold))
        self.label_name.setWordWrap(True)
        
        self.label_category = QLabel("Category: -")
        self.label_category.setStyleSheet("color: #64748B;")
        self.label_category.setFont(QFont("Urbanist", 10))
        
        text_info_layout.addWidget(self.label_name)
        text_info_layout.addWidget(self.label_category)
        
        info_layout.addWidget(self.img_dish)
        info_layout.addLayout(text_info_layout, Qt.AlignVCenter)
        
        main_layout.addWidget(self.info_frame)

        self.recipe_display = QTextBrowser()
        self.recipe_display.setPlaceholderText("Ingredients and preparation steps will appear here...")
        self.recipe_display.setOpenExternalLinks(True)
        main_layout.addWidget(self.recipe_display)

        self.setLayout(main_layout)

    def search_recipe(self):
        dish = self.recipe_input.text().strip()
        if not dish:
            self.recipe_display.setHtml("<font color='#DC2626'>⚠️ Please enter a recipe name to search.</font>")
            return

        url = f"https://www.themealdb.com/api/json/v1/1/search.php?s={dish}"
        self.fetch_api_data(url)

    def get_random_recipe(self):
        url = "https://www.themealdb.com/api/json/v1/1/random.php"
        self.fetch_api_data(url)

    def fetch_api_data(self, url):
        self.recipe_display.setHtml("<font color='#475569'>⏳ Searching the virtual kitchen...</font>")
        
        try:
            response = requests.get(url, timeout=7)
            if response.status_code == 200:
                data = response.json()
                if data['meals']:
                    self.display_recipe(data['meals'][0])
                else:
                    self.display_error("No recipe found with that name. Try another one!")
            else:
                self.display_error("Server error while connecting to TheMealDB.")
        except requests.exceptions.RequestException:
            self.display_error("Connection error. Please check your internet access.")

    def display_recipe(self, recipe):
        name = recipe.get('strMeal', 'Unknown Recipe')
        category = recipe.get('strCategory', '-')
        origin = recipe.get('strArea', '-')
        instructions = recipe.get('strInstructions', 'No instructions available.').replace('\r\n', '<br>')
        video = recipe.get('strYoutube', '')
        
        self.label_name.setText(name)
        self.label_category.setText(f"Category: {category} | Origin: {origin}")
        
        img_url = recipe.get('strMealThumb')
        if img_url:
            try:
                img_data = requests.get(img_url, timeout=5).content
                pixmap = QPixmap()
                pixmap.loadFromData(img_data)
                self.img_dish.setPixmap(pixmap.scaled(110, 110, Qt.KeepAspectRatio, Qt.SmoothTransformation))
            except:
                self.img_dish.setText("🍳")
        else:
            self.img_dish.setText("🍳")

        ingredients_html = "<h3 style='color: #0F172A; margin-top: 0px;'>📋 INGREDIENTS:</h3>"
        for i in range(1, 21):
            ingredient = recipe.get(f'strIngredient{i}')
            measure = recipe.get(f'strMeasure{i}')
            
            if ingredient and ingredient.strip():
                quantity = measure.strip() if measure else ""
                ingredients_html += f"• {ingredient.strip()} — <font color='#0D9488'><b>{quantity}</b></font><br>"
            else:
                break

        full_html = f"""
        {ingredients_html}
        <hr style="border: 1px solid #E2E8F0; margin: 15px 0;">
        <h3 style='color: #0F172A;'>🧑‍🍳 PREPARATION:</h3>
        <p style="line-height: 1.5; color: #334155;">{instructions}</p>
        """
        
        if video:
            full_html += f"""
            <hr style="border: 1px solid #E2E8F0; margin: 15px 0;">
            <p>📺 <b>Video Tutorial:</b> <a href="{video}" style="color: #2563EB; text-decoration: none;">Watch step-by-step on YouTube</a></p>
            """
            
        self.recipe_display.setHtml(full_html)

    def display_error(self, message):
        self.label_name.setText("Oops...")
        self.label_category.setText("-")
        self.img_dish.clear()
        self.img_dish.setText("❌")
        self.recipe_display.setHtml(f"<font color='#DC2626'>{message}</font>")

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = RecipeManager()
    ex.show()
    sys.exit(app.exec_())