from unittest import TestCase

from models import ServiceRecord, Vehicle, ServiceName

oil_change = ServiceRecord(600, "2021-11-11")
tire_rotation = ServiceRecord(6000, "2025-01-15")

record = ServiceRecord(mileage=60000, date="2022-12-10")
vehicle = Vehicle("Hyundai", "Elantra", 2023, 62000,
                  {ServiceName.OIL_CHANGE: oil_change, ServiceName.TIRE_ROTATION: tire_rotation})


class TestServiceRecord(TestCase):
    def test_to_dict(self):
        """
        Tests whether a ServiceRecord object was converted to a dictionary.

        Test Case: #21
        Test Date: 2/4/2026
        """
        result = record.to_dict()

        self.assertEqual(result, {"mileage": 60000, "date": "2022-12-10"})

    def test_from_dict(self):
        """

        :Test Case:
        :Test Date: 2/4/2026:
        """
        self.fail()


class TestVehicle(TestCase):
    def test_to_dict(self):
        """
        Tests whether a Vehicle object was converted to a dictionary.

        Test Case: #23
        Test Date: 2/4/2026
        """
        result = vehicle.to_dict()

        expected = {
            "make": "Hyundai",
            "model": "Elantra",
            "year": 2023,
            "current_mileage": 62000,
            "last_service": {
                "oil_change": {"mileage": 600, "date": "2021-11-11"},
                "tire_rotation": {"mileage": 6000, "date": "2025-01-15"}
            }
        }

        assert result == expected

    def test_from_dict(self):
        self.fail()
