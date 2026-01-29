from controller import Controller
from models import Vehicle
from datetime import datetime
import sys

class CLI:
    def __init__(self):
        self.controller = Controller()

    def run(self):
        while True:
            print("\nMotorMinder - Maintenance Tracker")
            print("1. List Vehicles")
            print("2. Add Vehicle")
            print("3. Edit Vehicle")
            print("4. Log Service")
            print("5. Maintenance Dashboard")
            print("0. Exit")
            choice = input("Select an option: ")
            if choice == '1':
                self.list_vehicles()
            elif choice == '2':
                self.add_vehicle()
            elif choice == '3':
                self.edit_vehicle()
            elif choice == '4':
                self.log_service()
            elif choice == '5':
                self.maintenance_dashboard()
            elif choice == '0':
                print("Goodbye!")
                sys.exit(0)
            else:
                print("Invalid option.")

    def list_vehicles(self):
        vehicles = self.controller.get_vehicles()
        if not vehicles:
            print("No vehicles found.")
            return
        for idx, v in enumerate(vehicles):
            print(f"[{idx}] {v.year} {v.make} {v.model} (Odometer: {v.current_mileage})")

    def add_vehicle(self):
        make = input("Make: ")
        model = input("Model: ")
        year = int(input("Year: "))
        mileage = int(input("Current Mileage: "))
        self.controller.add_vehicle(make, model, year, mileage)
        print("Vehicle added.")

    def edit_vehicle(self):
        self.list_vehicles()
        idx = int(input("Select vehicle index to edit: "))
        make = input("New Make: ")
        model = input("New Model: ")
        year = int(input("New Year: "))
        mileage = int(input("New Current Mileage: "))
        self.controller.edit_vehicle(idx, make, model, year, mileage)
        print("Vehicle updated.")

    def log_service(self):
        self.list_vehicles()
        idx = int(input("Select vehicle index: "))
        services = [
            "oil_change",
            "air_intake_filter",
            "cabin_air_filter",
            "tire_rotation",
            "transmission_fluid",
            "brake_pads_inspection",
            "battery",
            "coolant_flush",
            "spark_plugs",
            "brake_fluid"
        ]
        print("Select service:")
        for i, s in enumerate(services):
            print(f"  {i+1}. {s.replace('_', ' ').title()}")
        sidx = int(input("Service number: ")) - 1
        if sidx < 0 or sidx >= len(services):
            print("Invalid service selection.")
            return
        service = services[sidx]
        mileage = int(input("Service mileage: "))
        date_str = input("Service date (YYYY-MM-DD, blank for today): ")
        self.controller.log_service(idx, service, mileage, date_str or None)
        print("Service logged.")

    def maintenance_dashboard(self):
        vehicles = self.controller.get_vehicles()
        if not vehicles:
            print("No vehicles found.")
            return
        for idx, v in enumerate(vehicles):
            print(f"\n[{idx}] {v.year} {v.make} {v.model}")
            print(f"Odometer: {v.current_mileage}")
            for s, rec in v.last_service.items():
                print(f"  {s.title()}: {rec.mileage} miles @ {rec.date}")
            # Color-coding and due logic can be added here

if __name__ == "__main__":
    CLI().run()
