from data_handler import DataHandler
from models import Vehicle, ServiceRecord
from datetime import datetime
from typing import List, Dict

class Controller:
    def __init__(self, data_file: str = 'vehicles.json'):
        self.data_handler = DataHandler(data_file)

    def get_vehicles(self) -> List[Vehicle]:
        return [Vehicle.from_dict(v) for v in self.data_handler.get_vehicles()]

    def add_vehicle(self, make: str, model: str, year: int, current_mileage: int):
        vehicle = Vehicle(make, model, year, current_mileage)
        self.data_handler.add_vehicle(vehicle.to_dict())

    def edit_vehicle(self, idx: int, make: str, model: str, year: int, current_mileage: int):
        vehicle = Vehicle(make, model, year, current_mileage)
        self.data_handler.update_vehicle(idx, vehicle.to_dict())

    def log_service(self, idx: int, service_name: str, mileage: int, date_str: str = None):
        if not date_str:
            date_str = datetime.now().strftime('%Y-%m-%d')
        self.data_handler.log_service(idx, service_name, mileage, date_str)

    def get_vehicle_services(self, idx: int) -> Dict[str, ServiceRecord]:
        vehicles = self.data_handler.get_vehicles()
        if idx < 0 or idx >= len(vehicles):
            return {}
        v = vehicles[idx]
        return {k: ServiceRecord.from_dict(vv) for k, vv in v.get('last_service', {}).items()}
