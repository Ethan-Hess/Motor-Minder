from data_handler import DataHandler
from models import Vehicle, ServiceRecord
from datetime import datetime
from typing import List, Dict

class Controller:
    SERVICE_INTERVALS = {
        "oil_change": {"miles": (5000, 7500), "months": (3, 6)},
        "air_intake_filter": {"miles": (15000, 30000)},
        "cabin_air_filter": {"miles": (15000, 25000), "months": (12, 12)},
        "tire_rotation": {"miles": (5000, 7500)},
        "transmission_fluid": {"miles": (30000, 60000)},
        "brake_pads_inspection": {"miles": (25000, 70000)},
        "battery": {"miles": (30000, 50000), "years": (3, 5)},
        "coolant_flush": {"miles": (30000, 50000)},
        "spark_plugs": {"miles": (30000, 100000)},
        "brake_fluid": {"miles": (20000, 45000), "years": (2, 3)}
    }

    def get_service_status(self, vehicle, service_name, today=None):
        """
        Returns (status, due_miles, due_date) for a service.
        status: 'OK', 'Due Soon', 'Overdue'
        """
        import datetime
        intervals = self.SERVICE_INTERVALS.get(service_name, {})
        last = vehicle.last_service.get(service_name)
        if not last:
            return ("Overdue", None, None)
        status = "OK"
        due_miles = None
        due_date = None
        # Mileage logic
        if "miles" in intervals:
            min_m, max_m = intervals["miles"]
            last_mileage = last.mileage
            current_mileage = vehicle.current_mileage
            miles_since = current_mileage - last_mileage
            if miles_since >= max_m:
                status = "Overdue"
                due_miles = last_mileage + max_m
            elif miles_since >= min_m:
                status = "Due Soon"
                due_miles = last_mileage + max_m
            else:
                due_miles = last_mileage + max_m
        # Time logic
        if "months" in intervals or "years" in intervals:
            last_date = datetime.datetime.strptime(last.date, "%Y-%m-%d")
            if today is None:
                today = datetime.datetime.now()
            months = intervals.get("months")
            years = intervals.get("years")
            if months:
                min_mo, max_mo = months
                delta_months = (today.year - last_date.year) * 12 + (today.month - last_date.month)
                if delta_months >= max_mo:
                    status = "Overdue"
                    due_date = (last_date + datetime.timedelta(days=30*max_mo)).date()
                elif delta_months >= min_mo:
                    status = "Due Soon"
                    due_date = (last_date + datetime.timedelta(days=30*max_mo)).date()
                else:
                    due_date = (last_date + datetime.timedelta(days=30*max_mo)).date()
            if years:
                min_yr, max_yr = years
                delta_years = today.year - last_date.year
                if delta_years >= max_yr:
                    status = "Overdue"
                    due_date = (last_date + datetime.timedelta(days=365*max_yr)).date()
                elif delta_years >= min_yr:
                    status = "Due Soon"
                    due_date = (last_date + datetime.timedelta(days=365*max_yr)).date()
                else:
                    due_date = (last_date + datetime.timedelta(days=365*max_yr)).date()
        return (status, due_miles, due_date)

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
