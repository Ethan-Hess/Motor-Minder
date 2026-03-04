import json
import os
from typing import List, Dict, Any


class DataHandler:
    """
    Responsible for loading and saving vehicle, service, and mechanic data using JSON.
    """

    _instance = None

    def __new__(cls, filename: str = 'vehicles.json'):
        if cls._instance is None:
            cls._instance = super(DataHandler, cls).__new__(cls)
            cls._instance._initialized = False
        return cls._instance

    def __init__(self, vehicle_file='vehicles.json', mechanic_file='mechanics.json'):
        if self._initialized:
            return
        self.vehicle_file = vehicle_file
        self.mechanic_file = mechanic_file
        self.vehicle_data = {"vehicles": []}
        self.mechanic_data = {"mechanics": []}
        self.load()
        self._initialized = True

    def load(self):
        """
        Loads data from the Vehicle and Mechanics JSON files.
        """
        # Load vehicles
        if os.path.exists(self.vehicle_file):
            with open(self.vehicle_file, 'r') as f:
                self.vehicle_data = json.load(f)
        else:
            self.save_vehicles()

        # Save mechanics
        if os.path.exists(self.mechanic_file):
            with open(self.mechanic_file, 'r') as f:
                self.mechanic_data = json.load(f)
        else:
            self.save_mechanics()

    def save_vehicles(self):
        """
        Saves vehicle data into JSON file.
        """
        with open(self.vehicle_file, 'w') as f:
            json.dump(self.vehicle_data, f, indent=2)

    def save_mechanics(self):
        """
        Saves mechanic data into JSON file.
        """
        with open(self.mechanic_file, 'w') as f:
            json.dump(self.mechanic_data, f, indent=2)

    def get_vehicles(self) -> List[Dict[str, Any]]:
        """
        Gets vehicle data from JSON file.
        :return: vehicle data.
        """
        return self.vehicle_data.get("vehicles", [])

    def add_vehicle(self, vehicle: Dict[str, Any]):
        """
        Adds vehicle data from JSON file.
        :param vehicle: Vehicle data.
        """
        self.vehicle_data["vehicles"].append(vehicle)
        self.save_vehicles()

    def update_vehicle(self, idx: int, vehicle: Dict[str, Any]):
        """
        Updates vehicle data from JSON file.
        :param idx: Vehicle index.
        :param vehicle: Vehicle data.
        """
        self.vehicle_data["vehicles"][idx] = vehicle
        self.save_vehicles()

    def delete_vehicle(self, idx: int):
        """
        Deletes vehicle data from JSON file.
        :param idx: Vehicle index.
        """
        if 0 <= idx < len(self.vehicle_data["vehicles"]):
            self.vehicle_data["vehicles"].pop(idx)
            self.save_vehicles()

    def log_service(self, idx: int, service_name: str, mileage: int, date: str):
        """
        Logs service data from JSON file.
        :param idx: Vehicle index.
        :param service_name: Service name.
        :param mileage: Vehicle mileage.
        :param date: Service date.
        """
        vehicle = self.vehicle_data["vehicles"][idx]

        if "last_service" not in vehicle:
            vehicle["last_service"] = {}

        vehicle["last_service"][service_name] = {"mileage": mileage, "date": date}
        self.save_vehicles()

    def get_mechanics(self):
        return self.mechanic_data.get("mechanics", [])
