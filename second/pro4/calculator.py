import sys
from PyQt6.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QGridLayout,
    QPushButton, QLineEdit, QSizePolicy
)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont


class Calculator:
    def __init__(self):
        self.reset()

    def reset(self):
        self.current_value = 0.0
        self.previous_value = 0.0
        self.operator = None
        self.is_new_input = True

    def add(self, a, b):
        return a + b

    def subtract(self, a, b):
        return a - b

    def multiply(self, a, b):
        return a * b

    def divide(self, a, b):
        if b == 0:
            raise ValueError('Division by zero')
        return a / b

    def negative_positive(self, a):
        return a * -1

    def percent(self, a):
        return a / 100


class CalculatorUI(QWidget):
    def __init__(self):
        super().__init__()
        self.calc = Calculator()
        self.init_ui()

    def init_ui(self):
        self.setWindowTitle('Calculator')
        self.setStyleSheet('background-color: #000000;')
        self.setFixedSize(350, 560)

        main_layout = QVBoxLayout()
        main_layout.setContentsMargins(10, 20, 10, 20)
        main_layout.setSpacing(10)

        self.display = QLineEdit('0')
        self.display.setReadOnly(True)
        self.display.setAlignment(Qt.AlignmentFlag.AlignRight)
        self.display.setFont(QFont('Helvetica Neue', 60, QFont.Weight.Light))
        self.display.setStyleSheet('''
            QLineEdit {
                background-color: #000000; color: #FFFFFF;
                border: none; padding-right: 15px; padding-bottom: 10px;
            }
        ''')
        main_layout.addWidget(self.display, stretch=2)

        grid_layout = QGridLayout()
        grid_layout.setSpacing(12)

        buttons = [
            ('AC', 0, 0, 1, 'fn'), ('+/-', 0, 1, 1, 'fn'), ('%', 0, 2, 1, 'fn'), ('÷', 0, 3, 1, 'op'),
            ('7', 1, 0, 1, 'num'), ('8', 1, 1, 1, 'num'), ('9', 1, 2, 1, 'num'), ('×', 1, 3, 1, 'op'),
            ('4', 2, 0, 1, 'num'), ('5', 2, 1, 1, 'num'), ('6', 2, 2, 1, 'num'), ('-', 2, 3, 1, 'op'),
            ('1', 3, 0, 1, 'num'), ('2', 3, 1, 1, 'num'), ('3', 3, 2, 1, 'num'), ('+', 3, 3, 1, 'op'),
            ('0', 4, 0, 2, 'num'), ('.', 4, 2, 1, 'num'), ('=', 4, 3, 1, 'op')
        ]

        # 스타일 생략 (이전과 동일)
        # ... (생략된 스타일 정의는 이전 코드와 동일하게 적용)
        self._setup_buttons(grid_layout, buttons)
        main_layout.addLayout(grid_layout, stretch=5)
        self.setLayout(main_layout)
        self.show()

    def _setup_buttons(self, grid, buttons):
        common_style = '''
            QPushButton {
                border: none;
                color: #FFFFFF;
                font-family: 'Helvetica Neue';
                font-size: 28px;
                font-weight: Regular;
                border-radius: 33px;
            }
        '''

        style_sheet = {
            'fn': common_style + '''
                QPushButton { background-color: #A5A5A5; color: #000000; }
                QPushButton:pressed { background-color: #D9D9D9; }
            ''',
            'op': common_style + '''
                QPushButton { background-color: #FF9F0A; font-size: 35px; }
                QPushButton:pressed { background-color: #FCCB8F; }
            ''',
            'num': common_style + '''
                QPushButton { background-color: #333333; }
                QPushButton:pressed { background-color: #737373; }
            '''
        }

        for text, row, col, colspan, style_type in buttons:
            button = QPushButton(text)
            button.setStyleSheet(style_sheet[style_type])
            
            if text != '0':
                button.setFixedSize(66, 66)
            else:
                button.setFixedSize(144, 66)
                button.setStyleSheet(style_sheet[style_type] + 'text-align: left; padding-left: 25px;')

            button.clicked.connect(self.on_button_click)
            grid.addWidget(button, row, col, 1, colspan)


    def update_display(self):
        text = str(self.calc.current_value)
        # 보너스: 소수점 6자리 반올림
        if '.' in text:
            text = format(self.calc.current_value, '.6g')
        
        self.display.setText(text)
        self.adjust_font_size(text)

    def adjust_font_size(self, text):
        # 보너스: 글자 길이에 따른 폰트 크기 조정
        length = len(text)
        if length > 12:
            size = 30
        elif length > 8:
            size = 45
        else:
            size = 60
        self.display.setFont(QFont('Helvetica Neue', size, QFont.Weight.Light))

    def on_button_click(self):
        sender = self.sender().text()

        if sender.isdigit():
            if self.calc.is_new_input:
                self.display.setText(sender)
                self.calc.is_new_input = False
            else:
                self.display.setText(self.display.text() + sender)
            self.calc.current_value = float(self.display.text())

        elif sender == '.':
            if '.' not in self.display.text():
                self.display.setText(self.display.text() + '.')

        elif sender == 'AC':
            self.calc.reset()
            self.display.setText('0')

        elif sender in ['+', '-', '×', '÷']:
            self.calc.previous_value = float(self.display.text())
            self.calc.operator = sender
            self.calc.is_new_input = True

        elif sender == '=':
            self.equal()

    def equal(self):
        try:
            b = float(self.display.text())
            a = self.calc.previous_value
            op = self.calc.operator

            if op == '+': result = self.calc.add(a, b)
            elif op == '-': result = self.calc.subtract(a, b)
            elif op == '×': result = self.calc.multiply(a, b)
            elif op == '÷': result = self.calc.divide(a, b)
            else: result = b

            self.calc.current_value = result
            self.update_display()
            self.calc.is_new_input = True
        except ValueError:
            self.display.setText('Error')

if __name__ == '__main__':
    app = QApplication(sys.argv)
    calc_ui = CalculatorUI()
    sys.exit(app.exec())