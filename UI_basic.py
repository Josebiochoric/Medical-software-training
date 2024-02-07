
import sys
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QPushButton, QLabel, QProgressBar
from PyQt5.QtCore import QTimer

class TemperatureControlGUI(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()
        
    def initUI(self):
        self.setWindowTitle('Temperature Control')
        self.setGeometry(300, 300, 300, 200)

        # Set up the layout
        self.layout = QVBoxLayout()

        # Progress bar for self-test
        self.progressBar = QProgressBar(self)
        self.progressBar.setMaximum(100)
        self.layout.addWidget(self.progressBar)

        # Timer for self-test simulation
        self.selfTestTimer = QTimer(self)
        self.selfTestTimer.timeout.connect(self.performSelfTest)
        self.selfTestTimer.start(50)  # Update self-test progress every 50 ms

        # Set the layout
        self.setLayout(self.layout)
        
    def performSelfTest(self):
        value = self.progressBar.value() + 5
        self.progressBar.setValue(value)
        if value >= 100:
            self.selfTestTimer.stop()
            self.startMainUI()
        
    def startMainUI(self):
        # Remove the progress bar from the layout
        self.layout.removeWidget(self.progressBar)
        self.progressBar.deleteLater()
        self.progressBar = None
        
        # Now set up the main UI elements
        # Temperature label
        self.temperature_label = QLabel('Actual temperature: 20°C', self)
        self.layout.addWidget(self.temperature_label)
        
        # Set transport button
        self.transport_button = QPushButton('Set transport', self)
        self.transport_button.setCheckable(True)
        self.transport_button.clicked.connect(self.toggleTransport)
        self.layout.addWidget(self.transport_button)
        
        # Cool down button
        self.cool_down_button = QPushButton('Cool down', self)
        self.cool_down_button.clicked.connect(lambda: self.startTemperatureChange(-1))
        self.layout.addWidget(self.cool_down_button)
        
        # Warm up button
        self.warm_up_button = QPushButton('Warm up', self)
        self.warm_up_button.clicked.connect(lambda: self.startTemperatureChange(1))
        self.layout.addWidget(self.warm_up_button)
        
        # Increase the vertical size of the buttons
        self.transport_button.setFixedHeight(40)
        self.cool_down_button.setFixedHeight(40)
        self.warm_up_button.setFixedHeight(40)
        
        # Temperature variable and timer setup
        self.temperature = 20
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.updateTemperature)
    def toggleTransport(self):
        if self.transport_button.isChecked():
            self.transport_button.setStyleSheet("background-color: green; border-radius: 5px;")
            self.cool_down_button.setEnabled(False)
            self.warm_up_button.setEnabled(False)
        else:
            self.transport_button.setStyleSheet("")
            self.cool_down_button.setEnabled(True)
            self.warm_up_button.setEnabled(True)
            self.timer.stop()  # Stop temperature change if transport is unset
        
    def startTemperatureChange(self, direction):
        if not self.transport_button.isChecked():
            self.direction = direction
            if not self.timer.isActive():
                self.timer.start(100)  # Update temperature every 100 ms
        
    def updateTemperature(self):
        self.temperature += self.direction * 0.1  # Change the temperature by 0.1°C
        self.temperature_label.setText(f'Actual temperature: {self.temperature:.1f}°C')
        
        # Stopping condition if temperature goes out of bounds
        if (self.direction == -1 and self.temperature <= -4) or (self.direction == 1 and self.temperature >= 20):
            self.timer.stop()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = TemperatureControlGUI()
    ex.show()
    sys.exit(app.exec_())
