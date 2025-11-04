from PyQt6.QtWidgets import QApplication, QWidget, QVBoxLayout, QGridLayout, QPushButton, QLineEdit, QHBoxLayout, QCheckBox, QLabel
from PyQt6.QtGui import QFont
from PyQt6.QtCore import Qt, QTimer
import sys
import math

class DynamicEnglishCalculator(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("QuantumCalc")
        self.setGeometry(100, 100, 550, 650)
        self.setStyleSheet("background-color: #2E2E2E;")
        self.initUI()
    
    def initUI(self):
        # صندوق عرض النتائج
        self.result_display = QLineEdit()
        self.result_display.setReadOnly(True)
        self.result_display.setFixedHeight(60)
        self.result_display.setFont(QFont('Arial', 24))
        self.result_display.setStyleSheet("""
            background-color: #1C1C1C;
            color: #FFFFFF;
            border: none;
            padding: 10px;
        """)
        
        # اختيار وضع الدرجات أو الراديان
        self.deg_checkbox = QCheckBox("Degrees")
        self.deg_checkbox.setStyleSheet("color: #FFFFFF; font-size: 14px;")
        deg_layout = QHBoxLayout()
        deg_layout.addWidget(self.deg_checkbox)
        deg_layout.addStretch()
        
        # أزرار الآلة الحاسبة
        buttons = [
            ['C', '←', '(', ')', '÷'],
            ['7', '8', '9', '√', '×'],
            ['4', '5', '6', '^', '−'],
            ['1', '2', '3', '%', '+'],
            ['0', '.', '=', '', ''],
            ['sin', 'cos', 'tan', 'log', 'ln'],
            ['asin', 'acos', 'atan', 'sinh', 'cosh'],
            ['tanh', 'factorial', 'e^', '', '']
        ]
        
        self.grid_layout = QGridLayout()
        self.grid_layout.setSpacing(10)
        self.buttons = {}
        
        for row, button_row in enumerate(buttons):
            for col, text in enumerate(button_row):
                if text == '':
                    continue
                button = QPushButton(text)
                button.setFixedSize(70, 70)
                button.setFont(QFont('Arial', 16))
                button.clicked.connect(self.on_button_click)
                button.setCursor(Qt.CursorShape.PointingHandCursor)
                
                # ألوان وتأثيرات hover و press
                style = ""
                if text in '0123456789.':
                    style = """
                        QPushButton {
                            background-color: #4D4D4D;
                            color: #FFFFFF;
                            border-radius: 12px;
                        }
                        QPushButton:hover { background-color: #6E6E6E; }
                        QPushButton:pressed { background-color: #8E8E8E; }
                    """
                elif text in '+−×÷^√%()':
                    style = """
                        QPushButton {
                            background-color: #FF9500;
                            color: #FFFFFF;
                            border-radius: 12px;
                        }
                        QPushButton:hover { background-color: #FFA733; }
                        QPushButton:pressed { background-color: #FFB84D; }
                    """
                elif text == '=':
                    style = """
                        QPushButton {
                            background-color: #34C759;
                            color: #FFFFFF;
                            border-radius: 12px;
                        }
                        QPushButton:hover { background-color: #4DD36A; }
                        QPushButton:pressed { background-color: #5ED37C; }
                    """
                elif text == 'C':
                    style = """
                        QPushButton {
                            background-color: #FF3B30;
                            color: #FFFFFF;
                            border-radius: 12px;
                        }
                        QPushButton:hover { background-color: #FF5C4D; }
                        QPushButton:pressed { background-color: #FF6E5E; }
                    """
                elif text == '←':
                    style = """
                        QPushButton {
                            background-color: #5856D6;
                            color: #FFFFFF;
                            border-radius: 12px;
                        }
                        QPushButton:hover { background-color: #6A68E0; }
                        QPushButton:pressed { background-color: #7B7AF0; }
                    """
                else:
                    style = """
                        QPushButton {
                            background-color: #8E8E93;
                            color: #FFFFFF;
                            border-radius: 12px;
                        }
                        QPushButton:hover { background-color: #A3A3A8; }
                        QPushButton:pressed { background-color: #B7B7BC; }
                    """
                button.setStyleSheet(style)
                self.grid_layout.addWidget(button, row, col)
                self.buttons[text] = button
        
        # خانة عرض النتيجة المتحركة
        self.counter_label = QLabel("")
        self.counter_label.setFont(QFont('Arial', 28))
        self.counter_label.setAlignment(Qt.AlignmentFlag.AlignRight)
        self.counter_label.setStyleSheet("color: #34C759; padding: 10px; background-color: #1C1C1C;")
        
        # التخطيط العام
        main_layout = QVBoxLayout()
        main_layout.setSpacing(10)
        main_layout.addLayout(deg_layout)
        main_layout.addWidget(self.result_display)
        main_layout.addWidget(self.counter_label)
        main_layout.addLayout(self.grid_layout)
        self.setLayout(main_layout)
    
    def animate_counter(self, target):
        if hasattr(self, 'timer') and self.timer.isActive():
            self.timer.stop()
        
        self.counter_label.setText("")
        self.current_index = 0
        self.target_text = str(target)
        self.timer = QTimer()
        self.timer.timeout.connect(self.update_counter)
        self.timer.start(50)
    
    def update_counter(self):
        if self.current_index < len(self.target_text):
            self.counter_label.setText(self.counter_label.text() + self.target_text[self.current_index])
            self.current_index += 1
        else:
            self.timer.stop()
    
    def on_button_click(self):
        button = self.sender()
        text = button.text()
        
        if text == 'C':
            self.result_display.clear()
            self.counter_label.setText("")
        elif text == '←':
            self.result_display.setText(self.result_display.text()[:-1])
        elif text == '=':
            try:
                expr = self.result_display.text()
                expr = expr.replace('×','*').replace('÷','/').replace('−','-').replace('^','**')
                # التعامل مع الجذر، النسب، والدوال
                while '√' in expr:
                    idx = expr.find('√')
                    num = ''
                    i = idx + 1
                    while i < len(expr) and (expr[i].isdigit() or expr[i]=='.'):
                        num += expr[i]
                        i += 1
                    if num:
                        expr = expr.replace(f'√{num}', f'math.sqrt({num})')
                    else:
                        expr = expr.replace('√','math.sqrt(')+')'
                expr = expr.replace('%','/100')
                
                funcs = ['sin','cos','tan','asin','acos','atan','sinh','cosh','tanh','log','ln','factorial','e^']
                for func in funcs:
                    while func in expr:
                        idx = expr.find(func)
                        num = ''
                        i = idx + len(func)
                        if i < len(expr) and expr[i]=='(':
                            count=1
                            i+=1
                            start=i
                            while i<len(expr) and count>0:
                                if expr[i]=='(':
                                    count+=1
                                elif expr[i]==')':
                                    count-=1
                                i+=1
                            num=expr[start:i-1]
                        else:
                            while i<len(expr) and (expr[i].isdigit() or expr[i]=='.'):
                                num+=expr[i]
                                i+=1
                        val=float(num) if num else 0
                        if func in ['sin','cos','tan'] and self.deg_checkbox.isChecked():
                            val=math.radians(val)
                        if func=='sin': res=math.sin(val)
                        elif func=='cos': res=math.cos(val)
                        elif func=='tan': res=math.tan(val)
                        elif func=='asin': res=math.degrees(math.asin(val)) if self.deg_checkbox.isChecked() else math.asin(val)
                        elif func=='acos': res=math.degrees(math.acos(val)) if self.deg_checkbox.isChecked() else math.acos(val)
                        elif func=='atan': res=math.degrees(math.atan(val)) if self.deg_checkbox.isChecked() else math.atan(val)
                        elif func=='sinh': res=math.sinh(val)
                        elif func=='cosh': res=math.cosh(val)
                        elif func=='tanh': res=math.tanh(val)
                        elif func=='factorial': res=math.factorial(int(val))
                        elif func=='log': res=math.log10(val)
                        elif func=='ln': res=math.log(val)
                        elif func=='e^': res=math.exp(val)
                        expr=expr.replace(f'{func}({num})',str(res))
                
                result=str(eval(expr))
                self.result_display.setText(result)
                self.counter_label.setStyleSheet("color: #34C759; padding: 10px; background-color: #1C1C1C;")
                self.animate_counter(result)
            except:
                self.counter_label.setText("Error")
                self.counter_label.setStyleSheet("color: #FF3B30; padding: 10px; background-color: #1C1C1C;")
        else:
            self.result_display.setText(self.result_display.text()+text)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    win = DynamicEnglishCalculator()
    win.show()
    sys.exit(app.exec())
