import json
import os
from typing import List, Dict, Any

class DataHandler:
    def __init__(self, filename: str = 'vehicles.json'):
        self.filename = filename
        self.data = {"vehicles": []}
        self.load()

    def load(self):
        if os.path.exists(self.filename):
            with open(self.filename, 'r') as f:
                self.data = json.load(f)
        else:
            self.save()

    def save(self):
        with open(self.filename, 'w') as f:
            json.dump(self.data, f, indent=2)

    def get_vehicles(self) -> List[Dict[str, Any]]:
        return self.data.get("vehicles", [])

    def add_vehicle(self, vehicle: Dict[str, Any]):
        self.data["vehicles"].append(vehicle)
        self.save()

    def update_vehicle(self, idx: int, vehicle: Dict[str, Any]):
        self.data["vehicles"][idx] = vehicle
        self.save()

    def delete_vehicle(self, idx: int):
        if 0 <= idx < len(self.data["vehicles"]):
            self.data["vehicles"].pop(idx)
            self.save()

    def log_service(self, idx: int, service_name: str, mileage: int, date: str):
        vehicle = self.data["vehicles"][idx]
        if "last_service" not in vehicle:
            vehicle["last_service"] = {}
        vehicle["last_service"][service_name] = {"mileage": mileage, "date": date}
        self.save()
