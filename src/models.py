from enum import Enum
from typing import Dict, Optional
from datetime import date
from dataclasses import dataclass, field


class ServiceName(Enum):
    """
    Represents a maintenance service's name.
    """

    OIL_CHANGE = "oil_change"
    AIR_INTAKE_FILTER = "air_intake_filter"
    CABIN_AIR_FILTER = "cabin_air_filter"
    TIRE_ROTATION = "tire_rotation"
    TRANSMISSION_FLUID = "transmission_fluid"
    BRAKE_PADS_INSPECTION = "brake_pads_inspection"
    BATTERY = "battery"
    COOLANT_FLUSH = "coolant_flush"
    SPARK_PLUGS = "spark_plugs"
    BRAKE_FLUID = "brake_fluid"


@dataclass
class ServiceRecord:
    """
    Represents a maintenance record.
    """

    mileage: int
    date: str  # ISO format string

    def to_dict(self) -> Dict:
        """
        Converts a ServiceRecord to a dict.
        :return: ServiceRecord as dict.
        """
        return {"mileage": self.mileage, "date": self.date}

    @staticmethod
    def from_dict(data: Dict) -> 'ServiceRecord':
        """

        :param data:
        :return:
        """
        return ServiceRecord(data["mileage"], data["date"])


@dataclass
class Vehicle:
    """
    Represents a vehicle and its current state.
    """

    make: str
    model: str
    year: int
    current_mileage: int
    last_service: Dict[str, ServiceRecord] = field(default_factory=dict)

    def to_dict(self) -> Dict:
        """
        Converts a Vehicle to a dict.
        :return: Vehicle as dict.
        """
        return {
            "make": self.make,
            "model": self.model,
            "year": self.year,
            "current_mileage": self.current_mileage,
            "last_service": {k: v.to_dict() for k, v in self.last_service.items()}
        }

    @staticmethod
    def from_dict(data: Dict) -> 'Vehicle':
        """

        :param data:
        :return:
        """
        last_service = {k: ServiceRecord.from_dict(v) for k, v in data.get("last_service", {}).items()}

        return Vehicle(
            data["make"],
            data["model"],
            data["year"],
            data["current_mileage"],
            last_service
        )
