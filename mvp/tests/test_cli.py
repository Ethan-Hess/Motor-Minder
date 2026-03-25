import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))
from unittest import TestCase
from unittest.mock import patch, MagicMock
from cli import CLI
from models import Vehicle
from view import View



class TestCLI(TestCase):
    @patch('builtins.input', side_effect=['0'])
    @patch('builtins.print')
    def test_run(self, mock_print, mock_input):
        cli = CLI()
        cli.controller = MagicMock()
        with self.assertRaises(SystemExit) as cm:
            cli.run()
        self.assertEqual(cm.exception.code, 0)
        mock_print.assert_any_call(View.ok("Goodbye!"))

    @patch('builtins.print')
    def test_list_vehicles(self, mock_print):
        cli = CLI()
        cli.controller = MagicMock()
        vehicle = Vehicle('Toyota', 'Camry', 2020, 15000)
        cli.controller.get_vehicles.return_value = [vehicle]
        cli.list_vehicles()
        mock_print.assert_any_call(View.ok("--- Vehicle List ---"))

    @patch('builtins.input', side_effect=['Honda', 'Civic', '2018', '30000'])
    @patch('builtins.print')
    def test_add_vehicle(self, mock_print, mock_input):
        cli = CLI()
        cli.controller = MagicMock()
        cli.add_vehicle()
        cli.controller.add_vehicle.assert_called_once_with('Honda', 'Civic', 2018, 30000)
        mock_print.assert_any_call(View.ok("Vehicle added."))

    @patch('builtins.input', side_effect=['0', '1', 'NewMake', '0'])
    @patch('builtins.print')
    def test_edit_vehicle(self, mock_print, mock_input):
        cli = CLI()
        cli.controller = MagicMock()
        vehicle = Vehicle('Ford', 'Focus', 2015, 50000)
        cli.controller.get_vehicles.return_value = [vehicle]
        cli.controller.edit_vehicle = MagicMock()
        cli.edit_vehicle()
        cli.controller.edit_vehicle.assert_any_call(0, 'NewMake', 'Focus', 2015, 50000)

    @patch('builtins.input', side_effect=['0', '1', '40000', '2026-02-09'])
    @patch('builtins.print')
    def test_log_service(self, mock_print, mock_input):
        cli = CLI()
        cli.controller = MagicMock()
        vehicle = Vehicle('Mazda', '3', 2017, 40000)
        cli.controller.get_vehicles.return_value = [vehicle]
        cli.controller.log_service = MagicMock()
        cli.log_service()
        cli.controller.log_service.assert_called()
        mock_print.assert_any_call(View.ok("Service logged."))

    @patch('builtins.print')
    def test_maintenance_dashboard(self, mock_print):
        cli = CLI()
        cli.controller = MagicMock()
        vehicle = Vehicle('Tesla', 'Model 3', 2022, 10000)
        cli.controller.get_vehicles.return_value = [vehicle]
        cli.controller.get_service_status.return_value = MagicMock(status="OK")
        cli.maintenance_dashboard()
        mock_print.assert_any_call(View.ok("--- Maintenance Dashboard ---"))
