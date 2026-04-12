import json
import os
import tempfile
import sys
from unittest import TestCase
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))
from data_handler import DataHandler


class TestDataHandler(TestCase):
    def setUp(self):
        # Reset Singleton so each test gets a fresh instance with the temp file
        DataHandler._instance = None

        # Creates a temporary file to avoid messing up real data
        fd, self.temp_filename = tempfile.mkstemp(suffix='.json')
        os.close(fd)

        # Initialize with valid JSON so load() doesn't fail
        with open(self.temp_filename, "w") as f:
            json.dump({"vehicles": []}, f)

        self.handler = DataHandler(vehicle_file=self.temp_filename)

    def tearDown(self):
        # Reset Singleton and clean up temp file after each test
        DataHandler._instance = None
        if os.path.exists(self.temp_filename):
            os.remove(self.temp_filename)

    def test_load(self):
        # Write sample data to file, reset Singleton, and reload
        sample_data = {"vehicles": [{"make": "Toyota"}]}
        with open(self.temp_filename, "w") as f:
            json.dump(sample_data, f)

        DataHandler._instance = None
        handler = DataHandler(vehicle_file=self.temp_filename)

        self.assertEqual(handler.vehicle_data, sample_data)

    def test_save(self):
        self.handler.vehicle_data = {"vehicles": [{"make": "Honda"}]}
        self.handler.save_vehicles()

        with open(self.temp_filename, "r") as f:
            saved_data = json.load(f)

        self.assertEqual(saved_data, {"vehicles": [{"make": "Honda"}]})

    def test_get_vehicles(self):
        self.handler.vehicle_data = {"vehicles": [{"make": "Ford"}]}
        result = self.handler.get_vehicles()
        self.assertEqual(result, [{"make": "Ford"}])

    def test_add_vehicle(self):
        vehicle = {"make": "Tesla", "model": "Model 3"}
        self.handler.add_vehicle(vehicle)

        with open(self.temp_filename, "r") as f:
            data = json.load(f)

        self.assertIn(vehicle, data["vehicles"])

    def test_update_vehicle(self):
        self.handler.vehicle_data = {"vehicles": [{"make": "Toyota"}]}
        new_data = {"make": "Subaru"}
        self.handler.update_vehicle(0, new_data)

        with open(self.temp_filename, "r") as f:
            data = json.load(f)

        self.assertEqual(data["vehicles"][0], new_data)

    def test_delete_vehicle(self):
        self.handler.vehicle_data = {"vehicles": [{"make": "BMW"}, {"make": "Audi"}]}
        self.handler.save_vehicles()
        self.handler.delete_vehicle(0)

        with open(self.temp_filename, "r") as f:
            data = json.load(f)

        self.assertEqual(len(data["vehicles"]), 1)
        self.assertEqual(data["vehicles"][0]["make"], "Audi")

    def test_log_service(self):
        self.handler.vehicle_data = {"vehicles": [{"make": "Nissan"}]}
        self.handler.save_vehicles()

        self.handler.log_service(0, "Oil Change", 12000, "2026-02-06")

        with open(self.temp_filename, "r") as f:
            data = json.load(f)

        service = data["vehicles"][0]["last_service"]["Oil Change"]
        self.assertEqual(service, {"mileage": 12000, "date": "2026-02-06"})
