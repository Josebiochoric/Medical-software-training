"""
File Name: UI_basic.py
Purpose: Implements a GUI for controlling and monitoring temperature within a specified environment.
         This module simulates temperature changes and allows user interaction for temperature management.
Dependencies: PyQt5 for the GUI components.
Version: 1.0
Last Modified: 2024-02-13
Author: Jose Villarejo
Position: Engineer at Biochoric inc
"""
import sys
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QPushButton, QLabel
from PyQt5.QtCore import QTimer

class TemperatureControlGUI(QWidget):
    """
    A graphical user interface for temperature control and monitoring.
    
    This class provides a GUI for displaying the current temperature, simulating a self-test
    of the temperature control system, and allowing the user to adjust the temperature.
    """
    def __init__(self) -> None:
        """
        Initializes the TemperatureControlGUI object and sets up the initial user interface,
        replacing the progress bar with a text message indicating system start-up.
        """
        super().__init__()
        self.temperature: float = 20  # Initial temperature
        self.direction: int = 0  # Temperature change direction
        self.self_test()
        
    def self_test(self) -> None:
        """
        Initializes the user interface components and layout.
        
        Sets up the temperature control GUI, including a label indicating system start-up
        and buttons for temperature adjustments after a 5-second delay.
        """
        self.setWindowTitle('Temperature Control')  # Window title
        self.setGeometry(300, 300, 300, 200)  # Window position and size

        self.layout: QVBoxLayout = QVBoxLayout()  # Vertical layout for widget arrangement

        # Label to indicate system is starting
        self.startingLabel: QLabel = QLabel('Starting the system...', self)
        self.layout.addWidget(self.startingLabel)  # Add starting label to layout

        # Timer to delay the main UI start-up by 5 seconds
        self.startupTimer: QTimer = QTimer(self)  # Timer for delaying the start of the main UI
        self.startupTimer.timeout.connect(self.startMainUI)  # Connect timer signal to startMainUI method
        self.startupTimer.start(5000)  # Set timer for 5 seconds

        self.setLayout(self.layout)  # Apply the layout to the widget
        
    def startMainUI(self) -> None:
        """
        Sets up the main user interface elements after the initial delay.
        
        This method is called after a 5-second delay, indicated by the starting label,
        and includes temperature display, transport mode toggle, and temperature adjustment buttons.
        """
        # Remove the starting label from the layout and delete it
        self.layout.removeWidget(self.startingLabel)
        self.startingLabel.deleteLater()
        self.startingLabel = None

        # Stop the startup timer
        self.startupTimer.stop()

        # Main UI components setup
        self.temperature_label: QLabel = QLabel(f'Actual temperature: {self.temperature}°C', self)
        self.layout.addWidget(self.temperature_label)

        self.transport_button: QPushButton = QPushButton('Set transport', self)
        self.transport_button.setCheckable(True)
        self.transport_button.clicked.connect(self.toggleTransport)
        self.layout.addWidget(self.transport_button)

        self.cool_down_button: QPushButton = QPushButton('Cool down', self)
        self.cool_down_button.clicked.connect(lambda: self.startTemperatureChange(-1))
        self.layout.addWidget(self.cool_down_button)

        self.warm_up_button: QPushButton = QPushButton('Warm up', self)
        self.warm_up_button.clicked.connect(lambda: self.startTemperatureChange(1))
        self.layout.addWidget(self.warm_up_button)

        # Adjust button sizes for better UI appearance
        self.transport_button.setFixedHeight(40)
        self.cool_down_button.setFixedHeight(40)
        self.warm_up_button.setFixedHeight(40)

        # Timer for temperature updates
        self.timer: QTimer = QTimer(self)
        self.timer.timeout.connect(self.updateTemperature)
        
    def toggleTransport(self) -> None:
        """
        Toggles transport mode, disabling temperature adjustment buttons when active.
        
        Changes button style to indicate active/inactive transport mode.
        """
        isActive: bool = self.transport_button.isChecked()
        if isActive:
            self.transport_button.setStyleSheet("background-color: green; border-radius: 5px;")
            self.cool_down_button.setEnabled(False)
            self.warm_up_button.setEnabled(False)
        else:
            self.transport_button.setStyleSheet("")
            self.cool_down_button.setEnabled(True)
            self.warm_up_button.setEnabled(True)
            self.timer.stop()
        
    def startTemperatureChange(self, direction: int) -> None:
        """
        Initiates temperature change in the specified direction.
        
        Temperature change occurs only if transport mode is not active.
        """
        if not self.transport_button.isChecked():
            self.direction = direction
            if not self.timer.isActive():
                self.timer.start(100)
        
    def updateTemperature(self) -> None:
        self.temperature += self.direction * 0.1
        self.temperature_label.setText(f'Actual temperature: {self.temperature:.1f}°C')

        if (self.direction == -1 and self.temperature <= -4) or (self.direction == 1 and self.temperature >= 20):
            self.timer.stop()

if __name__ == '__main__':
    app: QApplication = QApplication(sys.argv)
    ex: TemperatureControlGUI = TemperatureControlGUI()
    ex.show()
    sys.exit(app.exec_())