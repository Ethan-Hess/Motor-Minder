from unittest import TestCase

from models import ServiceRecord, Vehicle, ServiceName

oil_change = ServiceRecord(600, "2021-11-11")
tire_rotation = ServiceRecord(6000, "2025-01-15")

record = ServiceRecord(60000, "2022-12-10")
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

        expected = {
            "mileage": 60000,
            "date": "2022-12-10"
        }

        self.assertEqual(result, expected)

    def test_from_dict(self):
        """
        Tests whether a ServiceRecord object was converted from a dictionary.
        Test Case: #22
        Test Date: 2/6/2026:
        """
        result = {
            "mileage": 60000,
            "date": "2022-12-10"
        }

        service_record = ServiceRecord.from_dict(result)

        assert service_record.mileage == 60000
        assert service_record.date == "2022-12-10"


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
                ServiceName.OIL_CHANGE: {"mileage": 600, "date": "2021-11-11"},
                ServiceName.TIRE_ROTATION: {"mileage": 6000, "date": "2025-01-15"}
            }
        }

        assert result == expected

    def test_from_dict(self):
        """
        Tests whether a Vehicle object was converted from a dictionary.
        Test Case: #24
        Test Date: 2/6/2026:
        """
        result = {
            "make": "Hyundai",
            "model": "Elantra",
            "year": 2023,
            "current_mileage": 62000,
            "last_service": {
                ServiceName.OIL_CHANGE: {"mileage": 600, "date": "2021-11-11"},
                ServiceName.TIRE_ROTATION: {"mileage": 6000, "date": "2025-01-15"}
            }
        }

        vehicle_record = Vehicle.from_dict(result)

        assert vehicle_record.make == "Hyundai"
        assert vehicle_record.model == "Elantra"
        assert vehicle_record.year == 2023
        assert vehicle_record.current_mileage == 62000
        assert vehicle_record.last_service[ServiceName.OIL_CHANGE].mileage == 600
        assert vehicle_record.last_service[ServiceName.OIL_CHANGE].date == "2021-11-11"
        assert vehicle_record.last_service[ServiceName.TIRE_ROTATION].mileage == 6000
        assert vehicle_record.last_service[ServiceName.TIRE_ROTATION].date == "2025-01-15"
