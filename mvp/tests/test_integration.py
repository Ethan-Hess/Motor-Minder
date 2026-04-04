import json
import os
import sys
import tempfile
from datetime import datetime
from unittest import TestCase
from unittest.mock import patch

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

from controller import Controller
from data_handler import DataHandler
from models import Vehicle, ServiceRecord, ServiceName
from cli import CLI
from view import View


class TestVehicleLifecycleIntegration(TestCase):
    """
    Integration tests for Vehicle CRUD operations across Controller and DataHandler.
    Verifies that data flows correctly from user commands through the Controller
    into persistent storage and back as properly deserialized model objects.
    """

    def setUp(self):
        DataHandler._instance = None
        fd, self.temp_vehicle_file = tempfile.mkstemp(suffix='.json')
        os.close(fd)
        with open(self.temp_vehicle_file, 'w') as f:
            json.dump({"vehicles": []}, f)
        self.controller = Controller(vehicle_file=self.temp_vehicle_file)

    def tearDown(self):
        DataHandler._instance = None
        if os.path.exists(self.temp_vehicle_file):
            os.remove(self.temp_vehicle_file)

    def test_add_vehicle_persists_and_retrieves_as_model(self):
        """
        Adding a vehicle through the Controller persists it and can be retrieved
        as a fully hydrated Vehicle model object.
        Test Case: #31
        Test Date: 3/4/2026
        """
        self.controller.add_vehicle("Toyota", "Camry", 2020, 50000)
        vehicles = self.controller.get_vehicles()

        self.assertEqual(len(vehicles), 1)
        self.assertIsInstance(vehicles[0], Vehicle)
        self.assertEqual(vehicles[0].make, "Toyota")
        self.assertEqual(vehicles[0].model, "Camry")
        self.assertEqual(vehicles[0].year, 2020)
        self.assertEqual(vehicles[0].current_mileage, 50000)

    def test_edit_vehicle_updates_persisted_storage(self):
        """
        Editing a vehicle through the Controller updates both the in-memory state
        and the persisted JSON file.
        Test Case: #32
        Test Date: 3/4/2026
        """
        self.controller.add_vehicle("Ford", "Focus", 2015, 30000)
        self.controller.edit_vehicle(0, "Ford", "Mustang", 2016, 35000)

        vehicles = self.controller.get_vehicles()
        self.assertEqual(vehicles[0].model, "Mustang")
        self.assertEqual(vehicles[0].year, 2016)

        with open(self.temp_vehicle_file, 'r') as f:
            data = json.load(f)
        self.assertEqual(data["vehicles"][0]["model"], "Mustang")
        self.assertEqual(data["vehicles"][0]["current_mileage"], 35000)

    def test_delete_vehicle_removes_from_storage(self):
        """
        Deleting a vehicle removes it from persistent storage, and the remaining
        vehicles shift correctly.
        Test Case: #33
        Test Date: 3/4/2026
        """
        self.controller.add_vehicle("Honda", "Civic", 2019, 45000)
        self.controller.add_vehicle("Mazda", "3", 2020, 20000)
        self.controller.delete_vehicle(0)

        vehicles = self.controller.get_vehicles()
        self.assertEqual(len(vehicles), 1)
        self.assertEqual(vehicles[0].make, "Mazda")

        with open(self.temp_vehicle_file, 'r') as f:
            data = json.load(f)
        self.assertEqual(len(data["vehicles"]), 1)

    def test_vehicle_data_survives_reload(self):
        """
        Vehicle data persisted via Controller can be fully re-loaded into a new
        Controller instance backed by the same file, verifying true persistence.
        Test Case: #34
        Test Date: 3/4/2026
        """
        self.controller.add_vehicle("Hyundai", "Elantra", 2022, 12000)

        DataHandler._instance = None
        fresh_controller = Controller(vehicle_file=self.temp_vehicle_file)

        vehicles = fresh_controller.get_vehicles()
        self.assertEqual(len(vehicles), 1)
        self.assertEqual(vehicles[0].make, "Hyundai")
        self.assertEqual(vehicles[0].model, "Elantra")
        self.assertEqual(vehicles[0].year, 2022)
        self.assertEqual(vehicles[0].current_mileage, 12000)


class TestServiceWorkflowIntegration(TestCase):
    """
    Integration tests for the service logging and status checking workflow.
    Verifies that logged service records are persisted and correctly influence
    service status calculations across the Controller and DataHandler layers.
    """

    def setUp(self):
        DataHandler._instance = None
        fd, self.temp_vehicle_file = tempfile.mkstemp(suffix='.json')
        os.close(fd)
        with open(self.temp_vehicle_file, 'w') as f:
            json.dump({"vehicles": []}, f)
        self.controller = Controller(vehicle_file=self.temp_vehicle_file)

    def tearDown(self):
        DataHandler._instance = None
        if os.path.exists(self.temp_vehicle_file):
            os.remove(self.temp_vehicle_file)

    def test_log_service_persists_and_retrievable(self):
        """
        A logged service is persisted to storage and is retrievable via
        get_vehicle_services as a ServiceRecord instance with correct values.
        Test Case: #35
        Test Date: 3/4/2026
        """
        self.controller.add_vehicle("Toyota", "Camry", 2020, 50000)
        self.controller.log_service(0, ServiceName.OIL_CHANGE, 49000, "2026-01-15")

        services = self.controller.get_vehicle_services(0)

        self.assertIn("oil_change", services)
        self.assertIsInstance(services["oil_change"], ServiceRecord)
        self.assertEqual(services["oil_change"].mileage, 49000)
        self.assertEqual(services["oil_change"].date, "2026-01-15")

    def test_logged_service_reflects_ok_status(self):
        """
        After logging a recent service, the status calculation correctly returns 'OK',
        confirming that persisted service records feed the status logic.
        Test Case: #36
        Test Date: 3/4/2026
        """
        self.controller.add_vehicle("Toyota", "Camry", 2020, 51000)
        self.controller.log_service(0, ServiceName.OIL_CHANGE, 50000, "2026-01-01")

        DataHandler._instance = None
        self.controller = Controller(vehicle_file=self.temp_vehicle_file)

        vehicles = self.controller.get_vehicles()
        today = datetime(2026, 3, 1)
        status = self.controller.get_service_status(vehicles[0], ServiceName.OIL_CHANGE, today)

        self.assertEqual(status.status, "OK")
        self.assertFalse(status.missing)

    def test_unlogged_service_shows_as_overdue(self):
        """
        A service with no logged record shows as 'Overdue' with the missing flag set,
        verifying the Controller correctly handles the absence of persisted data.
        Test Case: #37
        Test Date: 3/4/2026
        """
        self.controller.add_vehicle("Toyota", "Camry", 2020, 50000)
        vehicles = self.controller.get_vehicles()

        status = self.controller.get_service_status(vehicles[0], ServiceName.OIL_CHANGE)

        self.assertEqual(status.status, "Overdue")
        self.assertTrue(status.missing)

    def test_service_status_changes_after_logging(self):
        """
        Service status transitions from missing/Overdue to a tracked status after
        a service is logged, verifying end-to-end status update integration.
        Test Case: #38
        Test Date: 3/4/2026
        """
        self.controller.add_vehicle("Honda", "Accord", 2018, 75000)
        vehicles = self.controller.get_vehicles()

        status_before = self.controller.get_service_status(vehicles[0], ServiceName.TIRE_ROTATION)
        self.assertTrue(status_before.missing)

        self.controller.log_service(0, ServiceName.TIRE_ROTATION, 74000, "2026-02-01")

        DataHandler._instance = None
        self.controller = Controller(vehicle_file=self.temp_vehicle_file)
        vehicles = self.controller.get_vehicles()

        today = datetime(2026, 3, 1)
        status_after = self.controller.get_service_status(vehicles[0], ServiceName.TIRE_ROTATION, today)
        self.assertFalse(status_after.missing)

    def test_multiple_services_logged_and_retrieved(self):
        """
        Multiple services can be logged for a single vehicle and all are retrievable
        with correct data, verifying that service records don't overwrite each other.
        Test Case: #39
        Test Date: 3/4/2026
        """
        self.controller.add_vehicle("Nissan", "Altima", 2021, 40000)
        self.controller.log_service(0, ServiceName.OIL_CHANGE, 39000, "2026-01-01")
        self.controller.log_service(0, ServiceName.TIRE_ROTATION, 38000, "2025-11-01")
        self.controller.log_service(0, ServiceName.BRAKE_FLUID, 35000, "2025-06-01")

        services = self.controller.get_vehicle_services(0)

        self.assertIn("oil_change", services)
        self.assertIn("tire_rotation", services)
        self.assertIn("brake_fluid", services)
        self.assertEqual(len(services), 3)
        self.assertEqual(services["oil_change"].mileage, 39000)
        self.assertEqual(services["tire_rotation"].date, "2025-11-01")


class TestMechanicLookupIntegration(TestCase):
    """
    Integration tests for the mechanic lookup workflow.
    Verifies that the Controller correctly queries the DataHandler and returns
    matching mechanics based on city and state.
    """

    def setUp(self):
        DataHandler._instance = None
        fd, self.temp_vehicle_file = tempfile.mkstemp(suffix='.json')
        os.close(fd)
        with open(self.temp_vehicle_file, 'w') as f:
            json.dump({"vehicles": []}, f)
        self.controller = Controller(vehicle_file=self.temp_vehicle_file)

        self.controller.data_handler.mechanic_data = {
            "mechanics": [
                {
                    "name": "Test Garage",
                    "address": {
                        "address_line_1": "123 Test St",
                        "address_line_2": "",
                        "city": "Provo",
                        "state": "UT",
                        "zip_code": 84601,
                        "country": "USA"
                    },
                    "phone": "801-555-0001",
                    "email": "test@testgarage.com",
                    "website": "https://www.testgarage.com",
                    "services": ["oil_change", "tire_rotation"],
                    "rating": 4.5,
                    "price_range": "$$",
                    "appointment_required": False,
                    "hours": {"monday": "8:00-17:00"}
                },
                {
                    "name": "Orem Auto Shop",
                    "address": {
                        "address_line_1": "456 Center St",
                        "address_line_2": "",
                        "city": "Orem",
                        "state": "UT",
                        "zip_code": 84058,
                        "country": "USA"
                    },
                    "phone": "801-555-0002",
                    "email": "info@oremauto.com",
                    "website": "https://www.oremauto.com",
                    "services": ["oil_change", "brake_fluid"],
                    "rating": 4.0,
                    "price_range": "$",
                    "appointment_required": True,
                    "hours": {"monday": "9:00-18:00"}
                }
            ]
        }

    def tearDown(self):
        DataHandler._instance = None
        if os.path.exists(self.temp_vehicle_file):
            os.remove(self.temp_vehicle_file)

    def test_find_mechanic_returns_correct_match(self):
        """
        Searching by city and state returns the correct mechanic entry from the data store.
        Test Case: #40
        Test Date: 3/4/2026
        """
        mechanic = self.controller.get_mechanics_by_city("Provo", "UT")

        self.assertIsNotNone(mechanic)
        self.assertEqual(mechanic["name"], "Test Garage")
        self.assertEqual(mechanic["address"]["city"], "Provo")

    def test_find_mechanic_no_match_returns_none(self):
        """
        Searching for a city with no registered mechanic returns None.
        Test Case: #41
        Test Date: 3/4/2026
        """
        mechanic = self.controller.get_mechanics_by_city("Nonexistent City", "XX")

        self.assertIsNone(mechanic)

    def test_find_mechanic_case_insensitive(self):
        """
        Mechanic lookup is case-insensitive for both city and state inputs.
        Test Case: #42
        Test Date: 3/4/2026
        """
        mechanic_lower = self.controller.get_mechanics_by_city("provo", "ut")
        mechanic_upper = self.controller.get_mechanics_by_city("PROVO", "UT")
        mechanic_mixed = self.controller.get_mechanics_by_city("Provo", "Ut")

        self.assertIsNotNone(mechanic_lower)
        self.assertIsNotNone(mechanic_upper)
        self.assertIsNotNone(mechanic_mixed)
        self.assertEqual(mechanic_lower["name"], "Test Garage")
        self.assertEqual(mechanic_upper["name"], "Test Garage")

    def test_find_mechanic_distinguishes_between_cities(self):
        """
        Searching for different cities returns the distinct correct mechanic for each city.
        Test Case: #43
        Test Date: 3/4/2026
        """
        provo_mechanic = self.controller.get_mechanics_by_city("Provo", "UT")
        orem_mechanic = self.controller.get_mechanics_by_city("Orem", "UT")

        self.assertIsNotNone(provo_mechanic)
        self.assertIsNotNone(orem_mechanic)
        self.assertEqual(provo_mechanic["name"], "Test Garage")
        self.assertEqual(orem_mechanic["name"], "Orem Auto Shop")


class TestCLIControllerIntegration(TestCase):
    """
    Integration tests for the CLI and Controller interaction.
    Verifies that CLI user input correctly drives Controller and DataHandler operations,
    with real data persisted to and retrieved from storage.
    """

    def setUp(self):
        DataHandler._instance = None
        fd, self.temp_vehicle_file = tempfile.mkstemp(suffix='.json')
        os.close(fd)
        with open(self.temp_vehicle_file, 'w') as f:
            json.dump({"vehicles": []}, f)
        self.controller = Controller(vehicle_file=self.temp_vehicle_file)
        self.cli = CLI.__new__(CLI)
        self.cli.controller = self.controller

    def tearDown(self):
        DataHandler._instance = None
        if os.path.exists(self.temp_vehicle_file):
            os.remove(self.temp_vehicle_file)

    @patch('builtins.input', side_effect=['Honda', 'Civic', '2019', '30000'])
    @patch('builtins.print')
    def test_cli_add_vehicle_persists_to_storage(self, mock_print, mock_input):
        """
        Calling CLI.add_vehicle() with valid input persists the vehicle via
        Controller through to the data file.
        Test Case: #44
        Test Date: 3/4/2026
        """
        self.cli.add_vehicle()

        vehicles = self.cli.controller.get_vehicles()
        self.assertEqual(len(vehicles), 1)
        self.assertEqual(vehicles[0].make, "Honda")
        self.assertEqual(vehicles[0].model, "Civic")
        self.assertEqual(vehicles[0].year, 2019)
        self.assertEqual(vehicles[0].current_mileage, 30000)
        mock_print.assert_any_call(View.ok("Vehicle added."))

    @patch('builtins.input', side_effect=['0', '1', '40000', '2026-01-10'])
    @patch('builtins.print')
    def test_cli_log_service_persists_service_record(self, mock_print, mock_input):
        """
        Calling CLI.log_service() with valid input persists the service record
        via Controller to the data file, which is then retrievable.
        Test Case: #45
        Test Date: 3/4/2026
        """
        self.cli.controller.add_vehicle("Toyota", "Camry", 2020, 50000)
        self.cli.log_service()

        services = self.cli.controller.get_vehicle_services(0)
        self.assertGreater(len(services), 0)
        mock_print.assert_any_call(View.ok("Service logged."))

    @patch('builtins.print')
    def test_cli_maintenance_dashboard_reflects_logged_services(self, mock_print):
        """
        The maintenance dashboard displays output reflecting actual service records
        stored by the Controller, confirming full stack data flow to the View.
        Test Case: #46
        Test Date: 3/4/2026
        """
        self.cli.controller.add_vehicle("Toyota", "Camry", 2020, 50000)
        self.cli.controller.log_service(0, ServiceName.OIL_CHANGE, 49500, "2026-02-01")

        self.cli.maintenance_dashboard()

        mock_print.assert_any_call(View.ok("--- Maintenance Dashboard ---"))

    @patch('builtins.print')
    def test_cli_list_vehicles_shows_all_added_vehicles(self, mock_print):
        """
        CLI.list_vehicles() displays all vehicles that were added via the Controller,
        confirming that the CLI correctly reads from the shared data layer.
        Test Case: #47
        Test Date: 3/4/2026
        """
        self.cli.controller.add_vehicle("Toyota", "Camry", 2020, 50000)
        self.cli.controller.add_vehicle("Honda", "Civic", 2019, 30000)

        self.cli.list_vehicles()

        mock_print.assert_any_call(View.ok("--- Vehicle List ---"))
        printed_calls = [str(call) for call in mock_print.call_args_list]
        all_output = ' '.join(printed_calls)
        self.assertIn("Toyota", all_output)
        self.assertIn("Honda", all_output)