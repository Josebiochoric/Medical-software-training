import unittest
from PyQt5.QtWidgets import QApplication
from UI_basic import TemperatureControlGUI

class TestTemperatureControlGUI(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        """Set up QApplication once for all tests."""
        cls.app = QApplication([])

    def setUp(self):
        """Prepare the environment before each test."""
        self.gui = TemperatureControlGUI()
        # Directly initialize the main UI components to bypass the 5-second delay
        self.gui.startMainUI()

    def test_initial_temperature(self):
        """Test if the initial temperature is set correctly."""
        self.assertEqual(self.gui.temperature, 20)

    def test_toggle_transport(self):
        """Test toggling the transport mode disables/enables temperature adjustments."""
        # Initially, buttons should be enabled
        self.assertTrue(self.gui.cool_down_button.isEnabled())
        self.assertTrue(self.gui.warm_up_button.isEnabled())

        # Toggle transport mode off
        self.gui.toggleTransport()
        self.assertTrue(self.gui.cool_down_button.isEnabled())
        self.assertTrue(self.gui.warm_up_button.isEnabled())
        
        # Toggle transport mode on
        self.gui.transport_button.setChecked(True) 
        self.gui.toggleTransport()
        self.assertFalse(self.gui.cool_down_button.isEnabled())
        self.assertFalse(self.gui.warm_up_button.isEnabled())

    def test_temperature_change_and_limits(self):
        """Test temperature changes and verify limits are respected."""
        # Ensure transport mode is off for temperature adjustments
        self.gui.toggleTransport()  # If transport mode was on, this turns it off

        # Simulate warming up
        self.gui.startTemperatureChange(1)
        self.gui.updateTemperature()
        self.assertTrue(self.gui.temperature > 20)  # Initial temperature is 20, so it should increase

        # Cool down to minimum limit
        self.gui.startTemperatureChange(-1)
        while self.gui.temperature > -4:  # -4 is the lower limit
            self.gui.updateTemperature()
        self.assertAlmostEqual(self.gui.temperature, -4)
        self.gui.timer.stop()

        # Reset and warm up to maximum limit
        self.gui.temperature = 20  # Reset temperature to 20 for the test
        self.gui.startTemperatureChange(1)
        while self.gui.temperature < 20:  # 20 is the upper limit
            self.gui.updateTemperature()
        self.assertEqual(self.gui.temperature, 20)
        self.gui.timer.stop()

    @classmethod
    def tearDownClass(cls):
        """Clean up resources after all tests."""
        del cls.app

if __name__ == '__main__':
    unittest.main()