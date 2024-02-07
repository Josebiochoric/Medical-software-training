import sys
import unittest
from PyQt5.QtWidgets import QApplication
from PyQt5.QtCore import QTimer

from UI_basic import TemperatureControlGUI

class TestTemperatureControlGUI(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.app = QApplication(sys.argv)

    def setUp(self):
        """ Set up for the test """
        self.form = TemperatureControlGUI()
        self.form.show()

    def test_initial_state(self):
        """ Test the initial state of the UI elements. """
        self.assertEqual(self.form.progressBar.value(), 0)
        self.assertTrue(self.form.selfTestTimer.isActive())

    def test_self_test_completion(self):
        """ Test the self-test completes and transitions to main UI. """
        # Connect to the timer timeout signal to detect when self-test is done
        self.self_test_completed = False
        def on_self_test_complete():
            self.self_test_completed = True
            self.form.selfTestTimer.timeout.disconnect(on_self_test_complete)

        self.form.selfTestTimer.timeout.connect(on_self_test_complete)
        while not self.self_test_completed:
            QTest.qWait(100)  # Wait until the self-test completes

        self.assertEqual(self.form.progressBar.value(), 100)
        self.assertFalse(self.form.selfTestTimer.isActive())

    def test_transport_button(self):
        """ Test the transport button toggles and updates the UI correctly. """
        # Wait for self-test to complete
        QTest.qWait(5000)
        self.assertTrue(self.form.transport_button.isEnabled())

        # Toggle 'Set transport' button on
        QTest.mouseClick(self.form.transport_button, Qt.LeftButton)
        self.assertTrue(self.form.transport_button.isChecked())
        self.assertFalse(self.form.cool_down_button.isEnabled())
        self.assertFalse(self.form.warm_up_button.isEnabled())

        # Toggle 'Set transport' button off
        QTest.mouseClick(self.form.transport_button, Qt.LeftButton)
        self.assertFalse(self.form.transport_button.isChecked())
        self.assertTrue(self.form.cool_down_button.isEnabled())
        self.assertTrue(self.form.warm_up_button.isEnabled())

    # Other tests can be added here...

if __name__ == '__main__':
    unittest.main()