import sys
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QVBoxLayout, QLabel
from PyQt5.QtGui import QColor
from PyQt5.QtCore import QTimer

class UI(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Simple UI')

        self.button1 = QPushButton('Cool Down', self)
        self.button1.setStyleSheet("background-color: blue;")
        self.button1.clicked.connect(self.cool_down)

        self.button2 = QPushButton('Warm Up', self)
        self.button2.setStyleSheet("background-color: red;")
        self.button2.clicked.connect(self.warm_up)

        self.button3 = QPushButton('Set for Transport', self)
        self.button3.setStyleSheet("background-color: green;")
        self.button3.clicked.connect(self.set_for_transport)

        self.temperature_label = QLabel('20', self)

        layout = QVBoxLayout()
        layout.addWidget(self.button1)
        layout.addWidget(self.button2)
        layout.addWidget(self.button3)
        layout.addWidget(self.temperature_label)

        self.setLayout(layout)
        self.setGeometry(300, 300, 300, 200)
        self.show()

        self.timer = QTimer()
        self.timer.timeout.connect(self.update_temperature)

    def cool_down(self):
        # Stop warm_up function if running
        if hasattr(self, 'timer'):
            self.timer.stop()

        # Implement cool_down functionality here
        print("Cooling down...")
        self.timer.start(1000)  # Update every 1 second

    def warm_up(self):
        # Stop cool_down function if running
        if hasattr(self, 'timer'):
            self.timer.stop()

        # Implement warm_up functionality here
        print("Warming up...")
        self.timer.start(1000)  # Update every 1 second

    def set_for_transport(self):
        # Stop both cool_down and warm_up functions if running
        if hasattr(self, 'timer'):
            self.timer.stop()

        # Implement set_for_transport functionality here
        print("Setting for transport...")
        self.temperature_label.setText('20')

    def update_temperature(self):
        current_temperature = int(self.temperature_label.text())
        if current_temperature > -4:
            new_temperature = current_temperature - 1
        else:
            new_temperature = current_temperature + 1

        self.temperature_label.setText(str(new_temperature))

        if new_temperature == 24:
            self.timer.stop()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ui = UI()

    def cool_down():
        current_temperature = int(ui.temperature_label.text())
        new_temperature = current_temperature - 1
        ui.temperature_label.setText(str(new_temperature))

    def warm_up():
        current_temperature = int(ui.temperature_label.text())
        new_temperature = current_temperature + 1
        ui.temperature_label.setText(str(new_temperature))

    ui.button1.clicked.connect(cool_down)
    ui.button2.clicked.connect(warm_up)

    sys.exit(app.exec_())
    

    
