from dataclasses import dataclass
# Dataclass for service status result
@dataclass
class ServiceStatus:
    status: str
    due_miles: int | None
    due_date: object | None
    overdue_amount: str | None
    missing: bool
import json
import os
from data_handler import DataHandler
from models import Vehicle, ServiceRecord, ServiceName
from datetime import datetime
from typing import List, Dict


class Controller:

    def get_service_status(self, vehicle, service_name, today=None) -> 'ServiceStatus':
        # Accept both Enum and str for backward compatibility
        if isinstance(service_name, str):
            try:
                service_name = ServiceName(service_name)
            except ValueError:
                return ServiceStatus("Unknown", None, None, None, True)
        """
        Returns (status, due_miles, due_date) for a service.
        status: 'OK', 'Due Soon', 'Overdue'
        """
        import datetime
        intervals = self.SERVICE_INTERVALS.get(service_name, {})
        last = vehicle.last_service.get(service_name.value)
        if not last:
            return ServiceStatus("Overdue", None, None, None, True)
        status = "OK"
        due_miles = None
        due_date = None
        overdue_amount = None
        # Mileage logic
        if "miles" in intervals:
            min_m, max_m = intervals["miles"]
            last_mileage = last.mileage
            current_mileage = vehicle.current_mileage
            miles_since = current_mileage - last_mileage
            if miles_since >= max_m:
                status = "Overdue"
                due_miles = last_mileage + max_m
                overdue_amount = f"{current_mileage - due_miles} mi over" if current_mileage > due_miles else None
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
                    days_over = (today.date() - due_date).days
                    if days_over > 0:
                        overdue_amount = (overdue_amount + ", " if overdue_amount else "") + f"{days_over} days over"
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
                    days_over = (today.date() - due_date).days
                    if days_over > 0:
                        overdue_amount = (overdue_amount + ", " if overdue_amount else "") + f"{days_over} days over"
                elif delta_years >= min_yr:
                    status = "Due Soon"
                    due_date = (last_date + datetime.timedelta(days=365*max_yr)).date()
                else:
                    due_date = (last_date + datetime.timedelta(days=365*max_yr)).date()
        return ServiceStatus(status, due_miles, due_date, overdue_amount, False)

    def __init__(self, data_file: str = 'vehicles.json'):
        self.data_handler = DataHandler(data_file)
        # Load service intervals from JSON file
        intervals_path = os.path.join(os.path.dirname(__file__), 'service_intervals.json')
        with open(intervals_path, 'r') as f:
            raw_intervals = json.load(f)
        # Convert keys to ServiceName Enum and tuple values
        self.SERVICE_INTERVALS = {}
        for k, v in raw_intervals.items():
            try:
                enum_key = ServiceName(k)
            except ValueError:
                continue
            self.SERVICE_INTERVALS[enum_key] = {}
            for intv, val in v.items():
                # Convert lists to tuples for compatibility
                self.SERVICE_INTERVALS[enum_key][intv] = tuple(val)

    def get_vehicles(self) -> List[Vehicle]:
        return [Vehicle.from_dict(v) for v in self.data_handler.get_vehicles()]

    def add_vehicle(self, make: str, model: str, year: int, current_mileage: int):
        vehicle = Vehicle(make, model, year, current_mileage)
        self.data_handler.add_vehicle(vehicle.to_dict())

    def edit_vehicle(self, idx: int, make: str, model: str, year: int, current_mileage: int):
        vehicle = Vehicle(make, model, year, current_mileage)
        self.data_handler.update_vehicle(idx, vehicle.to_dict())

    def delete_vehicle(self, idx: int):
        self.data_handler.delete_vehicle(idx)

    def log_service(self, idx: int, service_name, mileage: int, date_str: str = None):
        # Accept both Enum and str for backward compatibility
        if isinstance(service_name, ServiceName):
            service_name = service_name.value
        if not date_str:
            date_str = datetime.now().strftime('%Y-%m-%d')
        self.data_handler.log_service(idx, service_name, mileage, date_str)

    def get_vehicle_services(self, idx: int) -> Dict[str, ServiceRecord]:
        vehicles = self.data_handler.get_vehicles()
        if idx < 0 or idx >= len(vehicles):
            return {}
        v = vehicles[idx]
        return {k: ServiceRecord.from_dict(vv) for k, vv in v.get('last_service', {}).items()}
