from enum import Enum
from typing import Dict, List
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
        Creates a ServiceRecord instance from a dictionary.
        :param data: A dictionary containing service record data with keys:
                    - 'mileage' (int): Mileage at which the service was performed
                    - 'date' (str): Date of service in ISO format (YYYY-MM-DD)
        :return:  ServiceRecord object populated with the provided data.
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
    last_service: Dict[ServiceName, ServiceRecord] = field(default_factory=dict)

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
        Creates a Vehicle instance from a dictionary.
        :param data: A dictionary containing vehicle data with keys:
                    - 'make' (str): Vehicle manufacturer
                    - 'model' (str): Vehicle model
                    - 'year' (int): Vehicle model year
                    - 'current_mileage' (int): Current mileage of the vehicle
                    - 'last_service' (dict, optional): A mapping of service names to service record dictionaries
        :return: A Vehicle object populated with the provided data.
        """
        last_service = {k: ServiceRecord.from_dict(v) for k, v in data.get("last_service", {}).items()}

        return Vehicle(
            data["make"],
            data["model"],
            data["year"],
            data["current_mileage"],
            last_service
        )


@dataclass
class Address:
    """
    Represents an address.
    """
    address_line_1: str
    address_line_2: str
    city: str
    state: str
    zip_code: int
    country: str

    def to_dict(self) -> Dict:
        """
        Converts an Address to a dict.
        :return: Address as dict.
        """
        return {
            "address_line_1": self.address_line_1,
            "address_line_2": self.address_line_2,
            "city": self.city,
            "state": self.state,
            "zip_code": self.zip_code,
            "country": self.country,
        }

    @staticmethod
    def from_dict(data: Dict) -> 'Address':
        """
        Creates an Address instance from a dictionary.
        :param data: A dictionary containing address data with keys.
        :return: An Address object populated with the provided data.
        """
        return Address(
            data["address_line_1"],
            data.get("address_line_2", ""),
            data["city"],
            data["state"],
            data["zip_code"],
            data["country"],
        )


@dataclass
class Mechanic:
    """
    Represents a mechanic.
    """
    name: str
    address: Address
    phone: str
    email: str
    website: str
    services: List[str]
    rating: float
    price_range: str
    appointment_required: bool
    hours: Dict[str, str] = field(default_factory=dict)

    def to_dict(self) -> Dict:
        return {
            "name": self.name,
            "address": self.address.to_dict(),
            "phone": self.phone,
            "email": self.email,
            "website": self.website,
            "services": self.services,
            "rating": self.rating,
            "price_range": self.price_range,
            "appointment_required": self.appointment_required,
            "hours": self.hours,
        }

    @staticmethod
    def from_dict(data: Dict) -> 'Mechanic':
        return Mechanic(
            name=data["name"],
            address=Address.from_dict(data["address"]),
            phone=data["phone"],
            email=data["email"],
            website=data["website"],
            services=data.get("services", []),
            rating=float(data.get("rating", 0.0)),
            price_range=data.get("price_range", "$"),
            appointment_required=data.get("appointment_required", False),
            hours=data.get("hours", {}),
        )
