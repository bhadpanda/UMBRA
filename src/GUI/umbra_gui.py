# umrba_gui.py

import sys
import random
import string
from PyQt5.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, 
                            QHBoxLayout, QPushButton, QLabel, QLineEdit, 
                            QTextEdit, QFrame, QSlider, QCheckBox, QTabWidget,
                            QGridLayout, QSpinBox, QComboBox, QSizePolicy)
from PyQt5.QtGui import QFont, QPalette, QColor, QMouseEvent
from PyQt5.QtCore import Qt, QPoint

class UMRBAMainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("UMRBA")
        self.setMinimumSize(900, 600)
        
        # Define the main accent color
        self.accent_color = "#00aaff"  # Cyan-blue color
        
        # Remove default window frame
        self.setWindowFlags(Qt.FramelessWindowHint)
        
        # Variables for window dragging
        self.draggable = True
        self.dragging = False
        self.drag_position = QPoint()
        
        # Set the dark theme
        self.apply_dark_theme()
        
        # Create central widget
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        
        # Main layout
        main_layout = QVBoxLayout(self.central_widget)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)
        
        # Custom title bar
        title_bar = QWidget()
        title_bar.setFixedHeight(30)
        title_bar.setStyleSheet(f"""
            background-color: #0a0a0a;
            border-bottom: 1px solid {self.accent_color};
        """)
        
        title_layout = QHBoxLayout(title_bar)
        title_layout.setContentsMargins(10, 0, 10, 0)
        
        # Window title
        window_title = QLabel("UMRBA v1.0")
        window_title.setFont(QFont("Consolas", 10))
        window_title.setStyleSheet(f"color: {self.accent_color};")
        
        # Window controls
        controls_layout = QHBoxLayout()
        controls_layout.setSpacing(8)
        
        # Minimize button
        minimize_btn = QPushButton("_")
        minimize_btn.setFixedSize(20, 20)
        minimize_btn.setFont(QFont("Consolas", 10))
        minimize_btn.setStyleSheet(f"""
            QPushButton {{
                background-color: #333333;
                color: {self.accent_color};
                border: 1px solid {self.accent_color};
                border-radius: 2px;
                padding: 0px;
            }}
            QPushButton:hover {{
                background-color: #003366;
            }}
            QPushButton:pressed {{
                background-color: #0066aa;
            }}
        """)
        minimize_btn.clicked.connect(self.showMinimized)
        
        # Maximize button
        self.maximize_btn = QPushButton("□")
        self.maximize_btn.setFixedSize(20, 20)
        self.maximize_btn.setFont(QFont("Consolas", 10))
        self.maximize_btn.setStyleSheet(f"""
            QPushButton {{
                background-color: #333333;
                color: {self.accent_color};
                border: 1px solid {self.accent_color};
                border-radius: 2px;
                padding: 0px;
            }}
            QPushButton:hover {{
                background-color: #003366;
            }}
            QPushButton:pressed {{
                background-color: #0066aa;
            }}
        """)
        self.maximize_btn.clicked.connect(self.toggle_maximize)
        
        # Close button
        close_btn = QPushButton("×")
        close_btn.setFixedSize(20, 20)
        close_btn.setFont(QFont("Consolas", 10))
        close_btn.setStyleSheet("""
            QPushButton {
                background-color: #333333;
                color: #ff0000;
                border: 1px solid #ff0000;
                border-radius: 2px;
                padding: 0px;
            }
            QPushButton:hover {
                background-color: #330000;
            }
            QPushButton:pressed {
                background-color: #660000;
            }
        """)
        close_btn.clicked.connect(self.close)
        
        # Add controls to layout
        controls_layout.addWidget(minimize_btn)
        controls_layout.addWidget(self.maximize_btn)
        controls_layout.addWidget(close_btn)
        
        # Add widgets to title bar
        title_layout.addWidget(window_title)
        title_layout.addStretch()
        title_layout.addLayout(controls_layout)
        
        # Content container
        content_container = QWidget()
        content_layout = QVBoxLayout(content_container)
        content_layout.setContentsMargins(10, 10, 10, 10)
        
        # Header
        header = QWidget()
        header_layout = QHBoxLayout(header)
        header_layout.setContentsMargins(0, 0, 0, 0)
        
        title_label = QLabel("UMRBA SECURE PASSWORD SYSTEM")
        title_label.setFont(QFont("Consolas", 14))
        title_label.setStyleSheet(f"color: {self.accent_color};")
        
        status_label = QLabel("● SYSTEM ONLINE")
        status_label.setFont(QFont("Consolas", 10))
        status_label.setStyleSheet(f"color: {self.accent_color};")
        status_label.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
        
        header_layout.addWidget(title_label)
        header_layout.addWidget(status_label)
        
        # Separator line
        separator = QFrame()
        separator.setFrameShape(QFrame.HLine)
        separator.setStyleSheet(f"background-color: {self.accent_color};")
        
        # Main content area with tabs
        tabs = QTabWidget()
        tabs.setStyleSheet(f"""
            QTabWidget::pane {{
                border: 1px solid #333333;
                background-color: #1a1a1a;
            }}
            QTabBar::tab {{
                background-color: #1a1a1a;
                color: {self.accent_color};
                border: 1px solid #333333;
                padding: 5px 10px;
                margin-right: 2px;
            }}
            QTabBar::tab:selected {{
                background-color: #003366;
            }}
            QTabBar::tab:hover {{
                background-color: #2a2a2a;
            }}
        """)
        
        # Password Generator Tab
        password_gen_widget = QWidget()
        password_gen_layout = QVBoxLayout(password_gen_widget)
        
        # Title
        gen_title = QLabel("PASSWORD GENERATOR")
        gen_title.setFont(QFont("Consolas", 12))
        gen_title.setStyleSheet(f"color: {self.accent_color};")
        gen_title.setAlignment(Qt.AlignCenter)
        
        # Password display
        password_display = QLineEdit()
        password_display.setFont(QFont("Consolas", 12))
        password_display.setReadOnly(True)
        password_display.setStyleSheet(f"""
            background-color: #0a0a0a;
            color: {self.accent_color};
            border: 1px solid #333333;
            padding: 8px;
        """)
        password_display.setPlaceholderText("Generated password will appear here")
        
        # Options frame
        options_frame = QFrame()
        options_frame.setFrameShape(QFrame.StyledPanel)
        options_frame.setStyleSheet("""
            background-color: #1a1a1a;
            border: 1px solid #333333;
            padding: 10px;
        """)
        
        options_layout = QGridLayout(options_frame)
        
        # Length option
        length_label = QLabel("Password Length:")
        length_label.setFont(QFont("Consolas", 10))
        length_label.setStyleSheet(f"color: {self.accent_color};")
        
        length_value = QLabel("16")
        length_value.setFont(QFont("Consolas", 10))
        length_value.setStyleSheet(f"color: {self.accent_color};")
        length_value.setAlignment(Qt.AlignCenter)
        
        length_slider = QSlider(Qt.Horizontal)
        length_slider.setMinimum(4)
        length_slider.setMaximum(64)
        length_slider.setValue(16)
        length_slider.setStyleSheet(f"""
            QSlider::groove:horizontal {{
                background: #333333;
                height: 8px;
                border-radius: 4px;
            }}
            QSlider::handle:horizontal {{
                background: {self.accent_color};
                width: 16px;
                margin: -4px 0;
                border-radius: 8px;
            }}
        """)
        length_slider.valueChanged.connect(lambda v: length_value.setText(str(v)))
        
        # Character options
        uppercase_check = QCheckBox("Include Uppercase (A-Z)")
        uppercase_check.setFont(QFont("Consolas", 10))
        uppercase_check.setStyleSheet(f"""
            QCheckBox {{
                color: {self.accent_color};
            }}
            QCheckBox::indicator {{
                width: 16px;
                height: 16px;
                border: 1px solid {self.accent_color};
            }}
            QCheckBox::indicator:checked {{
                background-color: {self.accent_color};
            }}
        """)
        uppercase_check.setChecked(True)
        
        lowercase_check = QCheckBox("Include Lowercase (a-z)")
        lowercase_check.setFont(QFont("Consolas", 10))
        lowercase_check.setStyleSheet(f"""
            QCheckBox {{
                color: {self.accent_color};
            }}
            QCheckBox::indicator {{
                width: 16px;
                height: 16px;
                border: 1px solid {self.accent_color};
            }}
            QCheckBox::indicator:checked {{
                background-color: {self.accent_color};
            }}
        """)
        lowercase_check.setChecked(True)
        
        numbers_check = QCheckBox("Include Numbers (0-9)")
        numbers_check.setFont(QFont("Consolas", 10))
        numbers_check.setStyleSheet(f"""
            QCheckBox {{
                color: {self.accent_color};
            }}
            QCheckBox::indicator {{
                width: 16px;
                height: 16px;
                border: 1px solid {self.accent_color};
            }}
            QCheckBox::indicator:checked {{
                background-color: {self.accent_color};
            }}
        """)
        numbers_check.setChecked(True)
        
        symbols_check = QCheckBox("Include Symbols (!@#$%^&*)")
        symbols_check.setFont(QFont("Consolas", 10))
        symbols_check.setStyleSheet(f"""
            QCheckBox {{
                color: {self.accent_color};
            }}
            QCheckBox::indicator {{
                width: 16px;
                height: 16px;
                border: 1px solid {self.accent_color};
            }}
            QCheckBox::indicator:checked {{
                background-color: {self.accent_color};
            }}
        """)
        symbols_check.setChecked(True)
        
        # Generate button
        generate_btn = QPushButton("GENERATE PASSWORD")
        generate_btn.setFont(QFont("Consolas", 11))
        generate_btn.setStyleSheet(f"""
            QPushButton {{
                background-color: #003366;
                color: {self.accent_color};
                border: 1px solid {self.accent_color};
                padding: 10px;
            }}
            QPushButton:hover {{
                background-color: #004488;
            }}
            QPushButton:pressed {{
                background-color: #0066aa;
            }}
        """)
        
        # Password strength meter
        strength_frame = QFrame()
        strength_frame.setFrameShape(QFrame.StyledPanel)
        strength_frame.setStyleSheet("""
            background-color: #1a1a1a;
            border: 1px solid #333333;
            padding: 10px;
        """)
        
        strength_layout = QVBoxLayout(strength_frame)
        
        strength_label = QLabel("PASSWORD STRENGTH")
        strength_label.setFont(QFont("Consolas", 10))
        strength_label.setStyleSheet(f"color: {self.accent_color};")
        strength_label.setAlignment(Qt.AlignCenter)
        
        strength_meter = QFrame()
        strength_meter.setFixedHeight(20)
        strength_meter.setStyleSheet(f"""
            background-color: #333333;
            border: 1px solid {self.accent_color};
        """)
        
        strength_value = QLabel("Not Generated")
        strength_value.setFont(QFont("Consolas", 10))
        strength_value.setStyleSheet(f"color: {self.accent_color};")
        strength_value.setAlignment(Qt.AlignCenter)
        
        strength_layout.addWidget(strength_label)
        strength_layout.addWidget(strength_meter)
        strength_layout.addWidget(strength_value)
        
        # Add all options to the grid
        options_layout.addWidget(length_label, 0, 0)
        options_layout.addWidget(length_slider, 0, 1)
        options_layout.addWidget(length_value, 0, 2)
        options_layout.addWidget(uppercase_check, 1, 0)
        options_layout.addWidget(lowercase_check, 1, 1)
        options_layout.addWidget(numbers_check, 2, 0)
        options_layout.addWidget(symbols_check, 2, 1)
        
        # Add all elements to the password generator layout
        password_gen_layout.addWidget(gen_title)
        password_gen_layout.addWidget(password_display)
        password_gen_layout.addWidget(options_frame)
        password_gen_layout.addWidget(generate_btn)
        password_gen_layout.addWidget(strength_frame)
        password_gen_layout.addStretch()
        
        # Password Suggestions Tab
        password_suggest_widget = QWidget()
        password_suggest_layout = QVBoxLayout(password_suggest_widget)
        
        # Title
        suggest_title = QLabel("PASSWORD SUGGESTIONS")
        suggest_title.setFont(QFont("Consolas", 12))
        suggest_title.setStyleSheet(f"color: {self.accent_color};")
        suggest_title.setAlignment(Qt.AlignCenter)
        
        # Suggestion options
        suggestion_frame = QFrame()
        suggestion_frame.setFrameShape(QFrame.StyledPanel)
        suggestion_frame.setStyleSheet("""
            background-color: #1a1a1a;
            border: 1px solid #333333;
            padding: 10px;
        """)
        
        suggestion_layout = QGridLayout(suggestion_frame)
        
        # Type selection
        type_label = QLabel("Suggestion Type:")
        type_label.setFont(QFont("Consolas", 10))
        type_label.setStyleSheet(f"color: {self.accent_color};")
        
        type_combo = QComboBox()
        type_combo.setFont(QFont("Consolas", 10))
        type_combo.setStyleSheet(f"""
            QComboBox {{
                background-color: #0a0a0a;
                color: {self.accent_color};
                border: 1px solid #333333;
                padding: 5px;
            }}
            QComboBox::drop-down {{
                border: 0px;
            }}
            QComboBox::down-arrow {{
                image: url(none);
                width: 14px;
                height: 14px;
            }}
            QComboBox QAbstractItemView {{
                background-color: #0a0a0a;
                color: {self.accent_color};
                selection-background-color: #003366;
            }}
        """)
        type_combo.addItems(["Memorable", "Phrase-Based", "Random Strong", "Pattern-Based"])
        
        # Number of suggestions
        count_label = QLabel("Number of Suggestions:")
        count_label.setFont(QFont("Consolas", 10))
        count_label.setStyleSheet(f"color: {self.accent_color};")
        
        count_spin = QSpinBox()
        count_spin.setFont(QFont("Consolas", 10))
        count_spin.setStyleSheet(f"""
            QSpinBox {{
                background-color: #0a0a0a;
                color: {self.accent_color};
                border: 1px solid #333333;
                padding: 5px;
            }}
            QSpinBox::up-button, QSpinBox::down-button {{
                background-color: #333333;
                width: 16px;
            }}
        """)
        count_spin.setMinimum(1)
        count_spin.setMaximum(10)
        count_spin.setValue(5)
        
        # Generate suggestions button
        suggest_btn = QPushButton("GENERATE SUGGESTIONS")
        suggest_btn.setFont(QFont("Consolas", 11))
        suggest_btn.setStyleSheet(f"""
            QPushButton {{
                background-color: #003366;
                color: {self.accent_color};
                border: 1px solid {self.accent_color};
                padding: 10px;
            }}
            QPushButton:hover {{
                background-color: #004488;
            }}
            QPushButton:pressed {{
                background-color: #0066aa;
            }}
        """)
        
        # Add options to the suggestion frame
        suggestion_layout.addWidget(type_label, 0, 0)
        suggestion_layout.addWidget(type_combo, 0, 1)
        suggestion_layout.addWidget(count_label, 1, 0)
        suggestion_layout.addWidget(count_spin, 1, 1)
        
        # Suggestions display
        suggestions_display = QTextEdit()
        suggestions_display.setFont(QFont("Consolas", 11))
        suggestions_display.setReadOnly(True)
        suggestions_display.setStyleSheet(f"""
            background-color: #0a0a0a;
            color: {self.accent_color};
            border: 1px solid #333333;
            padding: 8px;
        """)
        
        # Add all elements to the password suggestions layout
        password_suggest_layout.addWidget(suggest_title)
        password_suggest_layout.addWidget(suggestion_frame)
        password_suggest_layout.addWidget(suggest_btn)
        password_suggest_layout.addWidget(suggestions_display)
        
        # Terminal tab (keeping this from the original design)
        terminal_widget = QWidget()
        terminal_layout = QVBoxLayout(terminal_widget)
        
        terminal_output = QTextEdit()
        terminal_output.setFont(QFont("Consolas", 10))
        terminal_output.setStyleSheet(f"""
            background-color: #0a0a0a;
            color: {self.accent_color};
            border: 1px solid #333333;
        """)
        terminal_output.setReadOnly(True)
        terminal_output.setText("""UMRBA Terminal v1.0
Copyright (c) 2025 UMRBA Systems
        
[SYSTEM] Initializing password systems...
[SYSTEM] Loading encryption modules...
[SYSTEM] Establishing secure environment...
[SYSTEM] All systems operational.

Type 'help' for available commands.
""")
        
        command_layout = QHBoxLayout()
        command_prefix = QLabel("$>")
        command_prefix.setFont(QFont("Consolas", 10))
        command_prefix.setStyleSheet(f"color: {self.accent_color};")
        
        command_input = QLineEdit()
        command_input.setFont(QFont("Consolas", 10))
        command_input.setStyleSheet(f"""
            background-color: #0a0a0a;
            color: {self.accent_color};
            border: 1px solid #333333;
            padding: 5px;
        """)
        
        command_layout.addWidget(command_prefix)
        command_layout.addWidget(command_input)
        
        terminal_layout.addWidget(terminal_output)
        terminal_layout.addLayout(command_layout)
        
        # Add tabs
        tabs.addTab(password_gen_widget, "PASSWORD GENERATOR")
        tabs.addTab(password_suggest_widget, "PASSWORD SUGGESTIONS")
        tabs.addTab(terminal_widget, "TERMINAL")
        
        # Status bar at bottom
        status_bar = QWidget()
        status_bar_layout = QHBoxLayout(status_bar)
        status_bar_layout.setContentsMargins(0, 0, 0, 0)
        
        status_items = [
            "MODE: SECURE",
            "ENCRYPTION: ENABLED",
            "CLIPBOARD: READY",
            "UMRBA v1.0"
        ]
        
        for item in status_items:
            label = QLabel(item)
            label.setFont(QFont("Consolas", 8))
            label.setStyleSheet("color: #888888;")
            status_bar_layout.addWidget(label)
        
        # Add all components to content layout
        content_layout.addWidget(header)
        content_layout.addWidget(separator)
        content_layout.addWidget(tabs)
        content_layout.addWidget(status_bar)
        
        # Add title bar and content to main layout
        main_layout.addWidget(title_bar)
        main_layout.addWidget(content_container)
        
        # Connect signals
        command_input.returnPressed.connect(lambda: self.process_command(command_input, terminal_output))
        generate_btn.clicked.connect(lambda: self.generate_password(
            password_display, 
            length_slider.value(),
            uppercase_check.isChecked(),
            lowercase_check.isChecked(),
            numbers_check.isChecked(),
            symbols_check.isChecked(),
            strength_meter,
            strength_value
        ))
        suggest_btn.clicked.connect(lambda: self.generate_suggestions(
            suggestions_display,
            type_combo.currentText(),
            count_spin.value()
        ))
    
    def apply_dark_theme(self):
        # Set the application style to dark
        dark_palette = QPalette()
        
        # Set color group
        dark_palette.setColor(QPalette.Window, QColor(25, 25, 25))
        dark_palette.setColor(QPalette.WindowText, QColor(0, 170, 255))  # Cyan-blue color
        dark_palette.setColor(QPalette.Base, QColor(10, 10, 10))
        dark_palette.setColor(QPalette.AlternateBase, QColor(35, 35, 35))
        dark_palette.setColor(QPalette.ToolTipBase, QColor(0, 0, 0))
        dark_palette.setColor(QPalette.ToolTipText, QColor(0, 170, 255))  # Cyan-blue color
        dark_palette.setColor(QPalette.Text, QColor(0, 170, 255))  # Cyan-blue color
        dark_palette.setColor(QPalette.Button, QColor(35, 35, 35))
        dark_palette.setColor(QPalette.ButtonText, QColor(0, 170, 255))  # Cyan-blue color
        dark_palette.setColor(QPalette.BrightText, QColor(255, 0, 0))
        dark_palette.setColor(QPalette.Link, QColor(0, 170, 255))  # Cyan-blue color
        dark_palette.setColor(QPalette.Highlight, QColor(0, 51, 102))  # Darker blue for highlights
        dark_palette.setColor(QPalette.HighlightedText, QColor(0, 170, 255))  # Cyan-blue color
        
        # Apply the palette
        self.setPalette(dark_palette)
        
        # Set stylesheet for additional styling
        self.setStyleSheet(f"""
            QMainWindow {{
                background-color: #191919;
                border: 1px solid {self.accent_color};
            }}
            QWidget {{
                background-color: #191919;
                color: {self.accent_color};
            }}
            QPushButton {{
                background-color: #333333;
                color: {self.accent_color};
                border: 1px solid {self.accent_color};
                padding: 5px 10px;
                border-radius: 2px;
            }}
            QPushButton:hover {{
                background-color: #003366;
            }}
            QPushButton:pressed {{
                background-color: #0066aa;
            }}
            QLineEdit, QTextEdit {{
                background-color: #0a0a0a;
                color: {self.accent_color};
                border: 1px solid #333333;
                padding: 5px;
            }}
            QLabel {{
                color: {self.accent_color};
            }}
        """)
    
    def mousePressEvent(self, event: QMouseEvent):
        if event.button() == Qt.LeftButton and self.draggable:
            self.dragging = True
            self.drag_position = event.globalPos() - self.frameGeometry().topLeft()
            event.accept()
    
    def mouseMoveEvent(self, event: QMouseEvent):
        if event.buttons() == Qt.LeftButton and self.dragging:
            self.move(event.globalPos() - self.drag_position)
            event.accept()
    
    def mouseReleaseEvent(self, event: QMouseEvent):
        if event.button() == Qt.LeftButton:
            self.dragging = False
            event.accept()
    
    def toggle_maximize(self):
        if self.isMaximized():
            self.showNormal()
            self.maximize_btn.setText("□")
        else:
            self.showMaximized()
            self.maximize_btn.setText("❐")
    
    def process_command(self, input_field, output_field):
        command = input_field.text()
        current_text = output_field.toPlainText()
        
        # Add the command to the output
        output_field.setText(f"{current_text}\n$> {command}")
        
        # Process the command (simple example)
        if command.lower() == "help":
            response = """
Available commands:
  help         - Display this help message
  clear        - Clear the terminal
  generate     - Generate a random password
  suggest      - Suggest password patterns
  exit         - Exit the application
"""
        elif command.lower() == "clear":
            output_field.clear()
            response = "Terminal cleared."
        elif command.lower() == "generate":
            password = self.generate_random_password(16, True, True, True, True)
            response = f"""
Generated password: {password}
Strength: Strong
"""
        elif command.lower() == "suggest":
            response = """
Password suggestions:
  1. correct-horse-battery-staple
  2. Tr0ub4dor&3
  3. D0g$Ar3Aw3s0m3!
  4. 2Many$ecretsPa$$w0rd
  5. GreenLightRedLight!23
"""
        elif command.lower() == "exit":
            response = "Exiting application..."
            QApplication.quit()
        else:
            response = f"Unknown command: {command}"
        
        # Update the output
        output_field.setText(f"{output_field.toPlainText()}\n{response}")
        
        # Scroll to the bottom
        output_field.verticalScrollBar().setValue(output_field.verticalScrollBar().maximum())
        
        # Clear the input field
        input_field.clear()
    
    def generate_password(self, display, length, use_upper, use_lower, use_numbers, use_symbols, meter, strength_label):
        password = self.generate_random_password(length, use_upper, use_lower, use_numbers, use_symbols)
        display.setText(password)
        
        # Calculate password strength
        strength = self.calculate_password_strength(password)
        
        # Update strength meter
        if strength < 40:
            meter.setStyleSheet("background-color: #990000; border: 1px solid #00aaff;")
            strength_label.setText("Weak")
            strength_label.setStyleSheet("color: #ff0000;")
        elif strength < 70:
            meter.setStyleSheet("background-color: #999900; border: 1px solid #00aaff;")
            strength_label.setText("Medium")
            strength_label.setStyleSheet("color: #ffff00;")
        else:
            meter.setStyleSheet("background-color: #009999; border: 1px solid #00aaff;")
            strength_label.setText("Strong")
            strength_label.setStyleSheet("color: #00aaff;")
    
    def generate_random_password(self, length, use_upper, use_lower, use_numbers, use_symbols):
        chars = ""
        if use_upper:
            chars += string.ascii_uppercase
        if use_lower:
            chars += string.ascii_lowercase
        if use_numbers:
            chars += string.digits
        if use_symbols:
            chars += "!@#$%^&*()-_=+[]{}|;:,.<>?/"
        
        # Ensure at least one character type is selected
        if not chars:
            chars = string.ascii_lowercase
        
        # Generate password
        password = ''.join(random.choice(chars) for _ in range(length))
        return password
    
    def calculate_password_strength(self, password):
        # Simple password strength calculation
        strength = min(100, len(password) * 4)
        
        # Check for variety of character types
        has_lower = any(c.islower() for c in password)
        has_upper = any(c.isupper() for c in password)
        has_digit = any(c.isdigit() for c in password)
        has_symbol = any(not c.isalnum() for c in password)
        
        variety = sum([has_lower, has_upper, has_digit, has_symbol])
        strength += variety * 10
        
        # Cap at 100
        return min(100, strength)
    
    def generate_suggestions(self, display, suggestion_type, count):
        suggestions = []
        
        if suggestion_type == "Memorable":
            words = ["correct", "horse", "battery", "staple", "apple", "orange", 
                    "banana", "grape", "elephant", "giraffe", "tiger", "lion", 
                    "mountain", "river", "ocean", "forest", "happy", "sad", 
                    "angry", "excited", "blue", "red", "green", "yellow"]
            
            for _ in range(count):
                # Generate a memorable password with 3-4 random words
                word_count = random.randint(3, 4)
                selected_words = random.sample(words, word_count)
                suggestion = "-".join(selected_words)
                suggestions.append(suggestion)
                
        elif suggestion_type == "Phrase-Based":
            phrases = [
                "ILove{}In{}!",
                "My{}Is{}2023!",
                "{}Are{}Forever!",
                "{}Is{}Always!",
                "{}And{}Together!"
            ]
            
            nouns = ["Dogs", "Cats", "Books", "Movies", "Music", "Coffee", "Pizza", "Games"]
            adjectives = ["Amazing", "Awesome", "Great", "Fantastic", "Cool", "Super", "Excellent"]
            
            for _ in range(count):
                phrase_template = random.choice(phrases)
                noun = random.choice(nouns)
                adjective = random.choice(adjectives)
                
                suggestion = phrase_template.format(noun, adjective)
                suggestions.append(suggestion)
                
        elif suggestion_type == "Random Strong":
            for _ in range(count):
                # Generate a strong random password
                length = random.randint(12, 16)
                suggestion = self.generate_random_password(length, True, True, True, True)
                suggestions.append(suggestion)
                
        elif suggestion_type == "Pattern-Based":
            patterns = [
                "Xxxx####!",
                "Xxx-###-Xxx!",
                "Xx####Xx!",
                "###Xxxx###!",
                "Xx##Xx##Xx!"
            ]
            
            for _ in range(count):
                pattern = random.choice(patterns)
                suggestion = ""
                
                for char in pattern:
                    if char == 'X':
                        suggestion += random.choice(string.ascii_uppercase)
                    elif char == 'x':
                        suggestion += random.choice(string.ascii_lowercase)
                    elif char == '#':
                        suggestion += random.choice(string.digits)
                    else:
                        suggestion += char
                        
                suggestions.append(suggestion)
        
        # Display the suggestions
        display.clear()
        for i, suggestion in enumerate(suggestions, 1):
            display.append(f"{i}. {suggestion}")