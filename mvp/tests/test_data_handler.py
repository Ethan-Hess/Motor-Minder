import json
import os
import tempfile
import sys
from unittest import TestCase
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))
from data_handler import DataHandler


class TestDataHandler(TestCase):
    def setUp(self):
        # creates a temporary file to avoid messing up real data
       
       fd, self.temp_filename = tempfile.mkstemp()
       os.close(fd)
        # Initialize with valid JSON so load() doesn't fail
       with open(self.temp_filename, "w") as f:
        json.dump({"vehicles": []}, f)
       self.handler = DataHandler(filename=self.temp_filename)


    def tearDown(self):
        #cleans up after each test
        if os.path.exists(self.temp_filename):
            os.remove(self.temp_filename)

    def test_load(self):
        # prepares data
        sample_data = {"vehicles": [{"make": "Toyota"}]}
        with open(self.temp_filename, "w") as f:
            json.dump(sample_data, f)
        handler = DataHandler(filename=self.temp_filename)

        self.assertEqual(handler.data, sample_data)

    def test_save(self):
        self.handler.data = {"vehicles": [{"make": "Honda"}]}
        self.handler.save()

        with open(self.temp_filename, "r") as f:
            saved_data = json.load(f)
        self.assertEqual(saved_data, {"vehicles": [{"make": "Honda"}]})

    def test_get_vehicles(self):
        self.handler.data = {"vehicles": [{"make": "Ford"}]}
        result = self.handler.get_vehicles()
        self.assertEqual(result, [{"make": "Ford"}])

    def test_add_vehicle(self):
        vehicle = {"make": "Tesla", "model": "Model 3"}
        self.handler.add_vehicle(vehicle)

        with open(self.temp_filename, "r") as f:
            data = json.load(f)

        self.assertIn(vehicle, data["vehicles"])

    def test_update_vehicle(self):
        self.handler.data = {"vehicles": [{"make": "Toyota"}]}
        new_data = {"make": "Subaru"}
        self.handler.update_vehicle(0, new_data)

        with open(self.temp_filename, "r") as f:
            data = json.load(f)

        self.assertEqual(data["vehicles"][0], new_data)

    def test_delete_vehicle(self):
        self.handler.data = {"vehicles": [{"make": "BMW"}, {"make": "Audi"}]}
        self.handler.save()
        self.handler.delete_vehicle(0)

        with open(self.temp_filename, "r") as f:
            data = json.load(f)

        self.assertEqual(len(data["vehicles"]), 1)
        self.assertEqual(data["vehicles"][0]["make"], "Audi")

    def test_log_service(self):
        self.handler.data = {"vehicles": [{"make": "Nissan"}]}
        self.handler.save()

        self.handler.log_service(0, "Oil Change", 12000, "2026-02-06")

        with open(self.temp_filename, "r") as f:
            data = json.load(f)

        service = data["vehicles"][0]["last_service"]["Oil Change"]
        self.assertEqual(service, {"mileage": 12000, "date": "2026-02-06"})
