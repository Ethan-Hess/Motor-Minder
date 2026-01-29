from typing import Dict, Optional
from datetime import date

class ServiceRecord:
    def __init__(self, mileage: int, date_str: str):
        self.mileage = mileage
        self.date = date_str  # ISO format string

    def to_dict(self) -> Dict:
        return {"mileage": self.mileage, "date": self.date}

    @staticmethod
    def from_dict(data: Dict) -> 'ServiceRecord':
        return ServiceRecord(data["mileage"], data["date"])

class Vehicle:
    def __init__(self, make: str, model: str, year: int, current_mileage: int, last_service: Optional[Dict[str, ServiceRecord]] = None):
        self.make = make
        self.model = model
        self.year = year
        self.current_mileage = current_mileage
        self.last_service = last_service or {}

    def to_dict(self) -> Dict:
        return {
            "make": self.make,
            "model": self.model,
            "year": self.year,
            "current_mileage": self.current_mileage,
            "last_service": {k: v.to_dict() for k, v in self.last_service.items()}
        }

    @staticmethod
    def from_dict(data: Dict) -> 'Vehicle':
        last_service = {k: ServiceRecord.from_dict(v) for k, v in data.get("last_service", {}).items()}
        return Vehicle(
            data["make"],
            data["model"],
            data["year"],
            data["current_mileage"],
            last_service
        )
