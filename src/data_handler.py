import json
import os
from typing import List, Dict, Any


class DataHandler:
    """
    Responsible for loading and saving vehicle and service data using JSON.
    """

    def __init__(self, filename: str = 'vehicles.json'):
        self.filename = filename
        self.data = {"vehicles": []}
        self.load()

    def load(self):
        """
        Loads data from JSON file.
        """
        if os.path.exists(self.filename):
            with open(self.filename, 'r') as f:
                self.data = json.load(f)
        else:
            self.save()

    def save(self):
        """
        Saves data into JSON file.
        """
        with open(self.filename, 'w') as f:
            json.dump(self.data, f, indent=2)

    def get_vehicles(self) -> List[Dict[str, Any]]:
        """
        Gets vehicle data from JSON file.
        :return: vehicle data.
        """
        return self.data.get("vehicles", [])

    def add_vehicle(self, vehicle: Dict[str, Any]):
        """
        Adds vehicle data from JSON file.
        :param vehicle: Vehicle data.
        """
        self.data["vehicles"].append(vehicle)
        self.save()

    def update_vehicle(self, idx: int, vehicle: Dict[str, Any]):
        """
        Updates vehicle data from JSON file.
        :param idx: Vehicle index.
        :param vehicle: Vehicle data.
        """
        self.data["vehicles"][idx] = vehicle
        self.save()

    def delete_vehicle(self, idx: int):
        """
        Deletes vehicle data from JSON file.
        :param idx: Vehicle index.
        """
        if 0 <= idx < len(self.data["vehicles"]):
            self.data["vehicles"].pop(idx)
            self.save()

    def log_service(self, idx: int, service_name: str, mileage: int, date: str):
        """
        Logs service data from JSON file.
        :param idx: Vehicle index.
        :param service_name: Service name.
        :param mileage: Vehicle mileage.
        :param date: Service date.
        """
        vehicle = self.data["vehicles"][idx]

        if "last_service" not in vehicle:
            vehicle["last_service"] = {}

        vehicle["last_service"][service_name] = {"mileage": mileage, "date": date}
        self.save()
