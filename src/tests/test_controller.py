import json
import os
import sys
import tempfile
from datetime import datetime
from unittest import TestCase

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from controller import Controller
from data_handler import DataHandler
from models import Vehicle, ServiceRecord, ServiceName

class TestController(TestCase):
    def setUp(self):
        DataHandler._instance = None

        fd, self.temp_filename = tempfile.mkstemp(suffix='.json')
        os.close(fd)

        with open(self.temp_filename, "w") as f:
            json.dump({"vehicles": []}, f)

        self.controller = Controller(data_file=self.temp_filename)

    def tearDown(self):
        DataHandler._instance = None
        if os.path.exists(self.temp_filename):
            os.remove(self.temp_filename)

    def test_get_service_status(self):
        today = datetime(2026, 1, 1)
        vehicle = Vehicle(
            make="Toyota",
            model="Camry",
            year=2020,
            current_mileage=48000,
            last_service={
                ServiceName.OIL_CHANGE.value: ServiceRecord(mileage=45000, date="2025-12-01")
            }
        )

        status = self.controller.get_service_status(vehicle, ServiceName.OIL_CHANGE, today)
        self.assertEqual(status.status, "OK")
        self.assertFalse(status.missing)
        self.assertEqual(status.due_miles, 52500)

        vehicle_due_soon = Vehicle(
            make="Toyota",
            model="Camry",
            year=2020,
            current_mileage=51000,
            last_service={
                ServiceName.OIL_CHANGE.value: ServiceRecord(mileage=45000, date="2026-01-01")
            }
        )
        status = self.controller.get_service_status(vehicle_due_soon, ServiceName.OIL_CHANGE, today)
        self.assertEqual(status.status, "Due Soon")

        vehicle_overdue = Vehicle(
            make="Toyota",
            model="Camry",
            year=2020,
            current_mileage=55000,
            last_service={
                ServiceName.OIL_CHANGE.value: ServiceRecord(mileage=45000, date="2025-01-01")
            }
        )
        status = self.controller.get_service_status(vehicle_overdue, ServiceName.OIL_CHANGE, today)
        self.assertEqual(status.status, "Overdue")
        self.assertIsNotNone(status.overdue_amount)

        vehicle_no_service = Vehicle(
            make="Toyota",
            model="Camry",
            year=2020,
            current_mileage=50000,
            last_service={}
        )
        status = self.controller.get_service_status(vehicle_no_service, ServiceName.OIL_CHANGE, today)
        self.assertEqual(status.status, "Overdue")
        self.assertTrue(status.missing)

        status = self.controller.get_service_status(vehicle, "unknown_service", today)
        self.assertEqual(status.status, "Unknown")
        self.assertTrue(status.missing)

        status = self.controller.get_service_status(vehicle, "oil_change", today)
        self.assertEqual(status.status, "OK")
        self.assertFalse(status.missing)

    def test_get_vehicles(self):
        with open(self.temp_filename, "w") as f:
            json.dump({
                "vehicles": [
                    {"make": "Toyota", "model": "Camry", "year": 2020, "current_mileage": 50000, "last_service": {}},
                    {"make": "Honda", "model": "Civic", "year": 2019, "current_mileage": 60000, "last_service": {}}
                ]
            }, f)

        DataHandler._instance = None
        self.controller = Controller(data_file=self.temp_filename)

        vehicles = self.controller.get_vehicles()

        self.assertEqual(len(vehicles), 2)
        self.assertIsInstance(vehicles[0], Vehicle)
        self.assertEqual(vehicles[0].make, "Toyota")
        self.assertEqual(vehicles[1].make, "Honda")

    def test_add_vehicle(self):
        self.controller.add_vehicle("Ford", "Mustang", 2021, 15000)

        with open(self.temp_filename, "r") as f:
            data = json.load(f)

        self.assertEqual(len(data["vehicles"]), 1)
        self.assertEqual(data["vehicles"][0]["make"], "Ford")
        self.assertEqual(data["vehicles"][0]["model"], "Mustang")
        self.assertEqual(data["vehicles"][0]["year"], 2021)
        self.assertEqual(data["vehicles"][0]["current_mileage"], 15000)

    def test_edit_vehicle(self):
        self.controller.add_vehicle("Toyota", "Camry", 2020, 50000)

        self.controller.edit_vehicle(0, "Toyota", "Corolla", 2021, 55000)

        with open(self.temp_filename, "r") as f:
            data = json.load(f)

        self.assertEqual(data["vehicles"][0]["model"], "Corolla")
        self.assertEqual(data["vehicles"][0]["year"], 2021)
        self.assertEqual(data["vehicles"][0]["current_mileage"], 55000)

    def test_delete_vehicle(self):
        self.controller.add_vehicle("Toyota", "Camry", 2020, 50000)
        self.controller.add_vehicle("Honda", "Civic", 2019, 60000)

        self.controller.delete_vehicle(0)

        with open(self.temp_filename, "r") as f:
            data = json.load(f)

        self.assertEqual(len(data["vehicles"]), 1)
        self.assertEqual(data["vehicles"][0]["make"], "Honda")

    def test_log_service(self):
        self.controller.add_vehicle("Toyota", "Camry", 2020, 50000)

        self.controller.log_service(0, ServiceName.OIL_CHANGE, 50000, "2026-02-12")

        with open(self.temp_filename, "r") as f:
            data = json.load(f)

        service = data["vehicles"][0]["last_service"]["oil_change"]
        self.assertEqual(service["mileage"], 50000)
        self.assertEqual(service["date"], "2026-02-12")

        self.controller.log_service(0, "tire_rotation", 50000, "2026-02-12")

        with open(self.temp_filename, "r") as f:
            data = json.load(f)

        self.assertIn("tire_rotation", data["vehicles"][0]["last_service"])

        self.controller.log_service(0, ServiceName.BRAKE_FLUID, 50000)

        with open(self.temp_filename, "r") as f:
            data = json.load(f)

        self.assertIn("brake_fluid", data["vehicles"][0]["last_service"])
        self.assertEqual(data["vehicles"][0]["last_service"]["brake_fluid"]["date"],
                         datetime.now().strftime('%Y-%m-%d'))

    def test_get_vehicle_services(self):
        with open(self.temp_filename, "w") as f:
            json.dump({
                "vehicles": [{
                    "make": "Toyota",
                    "model": "Camry",
                    "year": 2020,
                    "current_mileage": 50000,
                    "last_service": {
                        "oil_change": {"mileage": 45000, "date": "2025-12-01"},
                        "tire_rotation": {"mileage": 48000, "date": "2026-01-15"}
                    }
                }]
            }, f)

        DataHandler._instance = None
        self.controller = Controller(data_file=self.temp_filename)

        services = self.controller.get_vehicle_services(0)

        self.assertEqual(len(services), 2)
        self.assertIn("oil_change", services)
        self.assertIn("tire_rotation", services)
        self.assertIsInstance(services["oil_change"], ServiceRecord)
        self.assertEqual(services["oil_change"].mileage, 45000)

        services = self.controller.get_vehicle_services(-1)
        self.assertEqual(services, {})

        services = self.controller.get_vehicle_services(999)
        self.assertEqual(services, {})