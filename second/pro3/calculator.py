import sys
from PyQt6.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QGridLayout,
    QPushButton, QLineEdit, QSizePolicy
)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont


class Calculator(QWidget):
    def __init__(self):
        super().__init__()
        self.init_ui()

    def init_ui(self):
        self.setWindowTitle('Calculator')
        self.setStyleSheet('background-color: #000000;')
        self.setFixedSize(350, 560)

        main_layout = QVBoxLayout()
        main_layout.setContentsMargins(10, 20, 10, 20)
        main_layout.setSpacing(10)

        # 디스플레이 설정
        self.display = QLineEdit('0')
        self.display.setReadOnly(True)
        self.display.setAlignment(Qt.AlignmentFlag.AlignRight)
        self.display.setFont(QFont('Helvetica Neue', 60, QFont.Weight.Light))
        self.display.setStyleSheet('''
            QLineEdit {
                background-color: #000000;
                color: #FFFFFF;
                border: none;
                padding-right: 15px;
                padding-bottom: 10px;
            }
        ''')
        self.display.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
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
            grid_layout.addWidget(button, row, col, 1, colspan)

        main_layout.addLayout(grid_layout, stretch=5)
        self.setLayout(main_layout)
        self.show()

    def on_button_click(self):
        # 클릭된 버튼의 텍스트 가져오기
        button = self.sender()
        text = button.text()
        current_display = self.display.text()

        if text == 'AC':
            self.display.setText('0')
        
        elif text == '=':
            try:
                # 화면의 기호를 파이썬 연산 기호로 변경 후 계산
                expression = current_display.replace('×', '*').replace('÷', '/')
                result = str(eval(expression))
                self.display.setText(result)
            except Exception:
                self.display.setText('Error')
        
        else:
            # 숫자가 0일 때는 초기화하고 입력, 그 외에는 뒤에 붙이기
            if current_display == '0':
                self.display.setText(text)
            else:
                self.display.setText(current_display + text)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    calc = Calculator()
    sys.exit(app.exec())