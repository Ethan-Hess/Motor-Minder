from controller import Controller
from models import Vehicle
from view import View
import sys

class CLI:
    def __init__(self):
        self.controller = Controller()

    def run(self):
        while True:
            print("\n" + View.header("MotorMinder - Maintenance Tracker"))
            print(View.menu_option(1, "List Vehicles"))
            print(View.menu_option(2, "Add Vehicle"))
            print(View.menu_option(3, "Edit Vehicle"))
            print(View.menu_option(4, "Log Service"))
            print(View.menu_option(5, "Maintenance Dashboard"))
            print(View.error("0. Exit"))
            choice = input(View.bold("Select an option: "))
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
                print(View.ok("Goodbye!"))
                sys.exit(0)
            else:
                print(View.warning("Invalid option."))

    def list_vehicles(self):
        vehicles = self.controller.get_vehicles()
        if not vehicles:
            print(View.color("No vehicles found.", View.OKCYAN))
            return
        print(View.ok("--- Vehicle List ---"))
        for idx, v in enumerate(vehicles):
            print(View.vehicle_row(idx, v))

    def add_vehicle(self):
        make = input("Make: ")
        model = input("Model: ")
        year = int(input("Year: "))
        mileage = int(input("Current Mileage: "))
        self.controller.add_vehicle(make, model, year, mileage)
        print(View.ok("Vehicle added."))

    def edit_vehicle(self):
        self.list_vehicles()
        idx = int(input("Select vehicle index to edit: "))
        vehicles = self.controller.get_vehicles()
        if idx < 0 or idx >= len(vehicles):
            print(View.warning("Invalid vehicle index."))
            return
        v = vehicles[idx]
        while True:
            print("\n" + View.color(f"Edit: {v.year} {v.make} {v.model}", View.OKCYAN))
            print(View.menu_option(1, "Edit Make"))
            print(View.menu_option(2, "Edit Model"))
            print(View.menu_option(3, "Edit Year"))
            print(View.menu_option(4, "Edit Mileage"))
            print(View.error("5. Delete Vehicle"))
            print(View.menu_option(0, "Back"))
            choice = input(View.bold("Select an option: "))
            if choice == '1':
                v.make = input("New Make: ")
                self.controller.edit_vehicle(idx, v.make, v.model, v.year, v.current_mileage)
                print(View.ok("Make updated."))
            elif choice == '2':
                v.model = input("New Model: ")
                self.controller.edit_vehicle(idx, v.make, v.model, v.year, v.current_mileage)
                print(View.ok("Model updated."))
            elif choice == '3':
                v.year = int(input("New Year: "))
                self.controller.edit_vehicle(idx, v.make, v.model, v.year, v.current_mileage)
                print(View.ok("Year updated."))
            elif choice == '4':
                v.current_mileage = int(input("New Current Mileage: "))
                self.controller.edit_vehicle(idx, v.make, v.model, v.year, v.current_mileage)
                print(View.ok("Mileage updated."))
            elif choice == '5':
                confirm = input(View.warning("Are you sure? (y/n): "))
                if confirm.lower() == 'y':
                    self.controller.delete_vehicle(idx)
                    print(View.ok("Vehicle deleted."))
                    return
                else:
                    print("Deletion cancelled.")
            elif choice == '0':
                break
            else:
                print(View.warning("Invalid option."))

    def log_service(self):
        self.list_vehicles()
        idx = int(input("Select vehicle index: "))
        from models import ServiceName
        services = [
            ServiceName.OIL_CHANGE,
            ServiceName.AIR_INTAKE_FILTER,
            ServiceName.CABIN_AIR_FILTER,
            ServiceName.TIRE_ROTATION,
            ServiceName.TRANSMISSION_FLUID,
            ServiceName.BRAKE_PADS_INSPECTION,
            ServiceName.BATTERY,
            ServiceName.COOLANT_FLUSH,
            ServiceName.SPARK_PLUGS,
            ServiceName.BRAKE_FLUID
        ]
        print(View.ok("Select service:"))
        for i, s in enumerate(services):
            print(f"  {i+1}. {s.value.replace('_', ' ').title()}")
        sidx = int(input("Service number: ")) - 1
        if sidx < 0 or sidx >= len(services):
            print(View.warning("Invalid service selection."))
            return
        service = services[sidx]
        mileage = int(input("Service mileage: "))
        date_str = input("Service date (YYYY-MM-DD, blank for today): ")
        self.controller.log_service(idx, service, mileage, date_str or None)
        print(View.ok("Service logged."))

    def maintenance_dashboard(self):
        vehicles = self.controller.get_vehicles()
        if not vehicles:
            print(View.color("No vehicles found.", View.OKCYAN))
            return
        print(View.ok("--- Maintenance Dashboard ---"))
        from models import ServiceName
        all_services = [
            ServiceName.OIL_CHANGE,
            ServiceName.AIR_INTAKE_FILTER,
            ServiceName.CABIN_AIR_FILTER,
            ServiceName.TIRE_ROTATION,
            ServiceName.TRANSMISSION_FLUID,
            ServiceName.BRAKE_PADS_INSPECTION,
            ServiceName.BATTERY,
            ServiceName.COOLANT_FLUSH,
            ServiceName.SPARK_PLUGS,
            ServiceName.BRAKE_FLUID
        ]
        for idx, v in enumerate(vehicles):
            print("\n" + View.color(f"[{idx}] {v.year} {v.make} {v.model}", View.OKCYAN))
            print(f"Odometer: {v.current_mileage}")
            service_rows = []
            for s in all_services:
                svc_status = self.controller.get_service_status(v, s)
                match svc_status.status:
                    case "OK":
                        sort_key = 0
                    case "Due Soon":
                        sort_key = 1
                    case _:
                        sort_key = 2
                msg = View.service_status_msg(s, svc_status)
                service_rows.append((sort_key, msg))
            # Sort by OK (0), Due Soon (1), Overdue (2)
            for _, msg in sorted(service_rows, key=lambda x: x[0]):
                print(msg)

if __name__ == "__main__":
    CLI().run()
