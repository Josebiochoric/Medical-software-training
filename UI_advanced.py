import sys
from PyQt5.QtWidgets import (QApplication, QMainWindow, QTabWidget, QWidget, QVBoxLayout, QLabel, QFrame,
                             QHBoxLayout, QGridLayout, QPushButton)
from PyQt5.QtGui import QFont
from PyQt5.QtCore import Qt, QDateTime
import pyqtgraph as pg
import numpy as np

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Custom PyQt Interface with Rounded Borders")
        self.setGeometry(100, 100, 1024, 768)  # Window size modified to better fit the layout

        self.tabWidget = QTabWidget()
        self.tabWidget.setTabPosition(QTabWidget.South)
        self.setCentralWidget(self.tabWidget)

        self.createGraphTab()
        self.tabWidget.addTab(QWidget(), "Log")
        self.tabWidget.addTab(QWidget(), "Advanced")
        self.tabWidget.addTab(QWidget(), "Shutdown")

    def createGraphTab(self):
        self.graphTab = QWidget()
        self.tabWidget.addTab(self.graphTab, "Graph")
        
        mainLayout = QVBoxLayout()
        headerLayout = QHBoxLayout()
        
        # Empty widget for left spacing
        headerLayout.addWidget(QWidget(), 1)
        
        # Date and Time in the center
        dateTimeLabel = QLabel(QDateTime.currentDateTime().toString("ddd, dd.MM.yyyy HH:mm"))
        dateTimeLabel.setFont(QFont("Arial", 16, QFont.Bold))  # Make font bold and larger
        headerLayout.addWidget(dateTimeLabel, 1, Qt.AlignCenter)
        
        # Empty widget for right spacing
        headerLayout.addWidget(QWidget(), 1)
        
        mainLayout.addLayout(headerLayout)

        gridLayout = QGridLayout()

        # Status section with a button
        statusFrame = self.createFrame("Status", "Storage Mode\nPress to Pause", isButton=True)
        gridLayout.addWidget(statusFrame, 0, 0)

        # Set Temp section
        setTempFrame = self.createFrame("Set Temp", "4.0°C")
        gridLayout.addWidget(setTempFrame, 0, 1)

        # Detected Temp section
        detectedTempFrame = self.createFrame("Detected Temp", "4.0°C")
        gridLayout.addWidget(detectedTempFrame, 1, 0)

        # INDe Status section
        indeStatusFrame = self.createFrame("INDe Status", "OK!\nNo Problem")
        gridLayout.addWidget(indeStatusFrame, 1, 1)

        # Approx. Heart Temp section
        heartTempFrame = self.createFrame("Appx. Heart Temp", "-3.2°C")
        gridLayout.addWidget(heartTempFrame, 1, 2)

        mainLayout.addLayout(gridLayout)

        # Real-time Graph
        self.graphWidget = pg.PlotWidget()
        self.graphWidget.setBackground('w')
        mainLayout.addWidget(self.graphWidget)
        self.plotData()

        self.graphTab.setLayout(mainLayout)

    def createFrame(self, title, value, isButton=False):
        frame = QFrame()
        frame.setFrameShape(QFrame.StyledPanel)
        frame.setStyleSheet(
            "QFrame {"
            "   background-color: #f0f0f0;"
            "   border-radius: 15px;"  # Rounded corners
            "}"
            "QLabel {"
            "   border-style: none;"
            "}"
            "QPushButton {"
            "   background-color: #e7e7e7;"
            "   border-radius: 10px;"  # Rounded corners for buttons
            "}"
        )
        frameLayout = QVBoxLayout()
        titleLabel = QLabel(title)
        titleLabel.setFont(QFont("Arial", 10, QFont.Bold))
        frameLayout.addWidget(titleLabel)

        if isButton:
            button = QPushButton(value)
            frameLayout.addWidget(button)
        else:
            valueLabel = QLabel(value)
            valueLabel.setFont(QFont("Arial", 10))
            frameLayout.addWidget(valueLabel)
        
        frame.setLayout(frameLayout)
        return frame

    def plotData(self):
        self.x = list(range(100))  # 100 time points
        self.y = [np.random.normal(0, 1) for _ in range(100)]  # 100 data points
        self.graphWidget.plot(self.x, self.y, pen=pg.mkPen(color=(255, 0, 0)))

if __name__ == "__main__":
    app = QApplication(sys.argv)
    mainWindow = MainWindow()
    mainWindow.show()
    sys.exit(app.exec_())
