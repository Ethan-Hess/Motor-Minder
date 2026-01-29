from controller import Controller
from models import Vehicle
from datetime import datetime
import sys

class CLI:
    def __init__(self):
        self.controller = Controller()

    def run(self):
        HEADER = '\033[95m'
        OKBLUE = '\033[94m'
        OKCYAN = '\033[96m'
        OKGREEN = '\033[92m'
        WARNING = '\033[93m'
        FAIL = '\033[91m'
        ENDC = '\033[0m'
        BOLD = '\033[1m'
        UNDERLINE = '\033[4m'
        while True:
            print(f"\n{HEADER}{BOLD}MotorMinder - Maintenance Tracker{ENDC}")
            print(f"{OKCYAN}1. List Vehicles{ENDC}")
            print(f"{OKCYAN}2. Add Vehicle{ENDC}")
            print(f"{OKCYAN}3. Edit Vehicle{ENDC}")
            print(f"{OKCYAN}4. Log Service{ENDC}")
            print(f"{OKCYAN}5. Maintenance Dashboard{ENDC}")
            print(f"{FAIL}0. Exit{ENDC}")
            choice = input(f"{BOLD}Select an option: {ENDC}")
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
                print(f"{OKGREEN}Goodbye!{ENDC}")
                sys.exit(0)
            else:
                print(f"{WARNING}Invalid option.{ENDC}")

    def list_vehicles(self):
        OKGREEN = '\033[92m'
        OKCYAN = '\033[96m'
        ENDC = '\033[0m'
        vehicles = self.controller.get_vehicles()
        if not vehicles:
            print(f"{OKCYAN}No vehicles found.{ENDC}")
            return
        print(f"{OKGREEN}--- Vehicle List ---{ENDC}")
        for idx, v in enumerate(vehicles):
            print(f"{OKCYAN}[{idx}] {v.year} {v.make} {v.model} {ENDC}{OKGREEN}(Odometer: {v.current_mileage}){ENDC}")

    def add_vehicle(self):
        OKGREEN = '\033[92m'
        ENDC = '\033[0m'
        make = input("Make: ")
        model = input("Model: ")
        year = int(input("Year: "))
        mileage = int(input("Current Mileage: "))
        self.controller.add_vehicle(make, model, year, mileage)
        print(f"{OKGREEN}Vehicle added.{ENDC}")

    def edit_vehicle(self):
        OKGREEN = '\033[92m'
        ENDC = '\033[0m'
        self.list_vehicles()
        idx = int(input("Select vehicle index to edit: "))
        make = input("New Make: ")
        model = input("New Model: ")
        year = int(input("New Year: "))
        mileage = int(input("New Current Mileage: "))
        self.controller.edit_vehicle(idx, make, model, year, mileage)
        print(f"{OKGREEN}Vehicle updated.{ENDC}")

    def log_service(self):
        OKGREEN = '\033[92m'
        WARNING = '\033[93m'
        ENDC = '\033[0m'
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
        print(f"{OKGREEN}Select service:{ENDC}")
        for i, s in enumerate(services):
            print(f"  {i+1}. {s.replace('_', ' ').title()}")
        sidx = int(input("Service number: ")) - 1
        if sidx < 0 or sidx >= len(services):
            print(f"{WARNING}Invalid service selection.{ENDC}")
            return
        service = services[sidx]
        mileage = int(input("Service mileage: "))
        date_str = input("Service date (YYYY-MM-DD, blank for today): ")
        self.controller.log_service(idx, service, mileage, date_str or None)
        print(f"{OKGREEN}Service logged.{ENDC}")

    def maintenance_dashboard(self):
        OKGREEN = '\033[92m'
        WARNING = '\033[93m'
        FAIL = '\033[91m'
        OKCYAN = '\033[96m'
        ENDC = '\033[0m'
        vehicles = self.controller.get_vehicles()
        if not vehicles:
            print(f"{OKCYAN}No vehicles found.{ENDC}")
            return
        print(f"{OKGREEN}--- Maintenance Dashboard ---{ENDC}")
        all_services = [
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
        from datetime import datetime
        for idx, v in enumerate(vehicles):
            print(f"\n{OKCYAN}[{idx}] {v.year} {v.make} {v.model}{ENDC}")
            print(f"Odometer: {v.current_mileage}")
            service_rows = []
            for s in all_services:
                status, due_miles, due_date = self.controller.get_service_status(v, s)
                last = v.last_service.get(s)
                extra = ""
                if status == "OK":
                    color = OKGREEN
                    sort_key = 0
                elif status == "Due Soon":
                    color = WARNING
                    sort_key = 1
                else:
                    color = FAIL
                    sort_key = 2
                    if not last:
                        extra = " (no service recorded)"
                    else:
                        # Calculate how much overdue
                        over = []
                        if due_miles and v.current_mileage > due_miles:
                            over.append(f"{v.current_mileage - due_miles} mi over")
                        if due_date:
                            try:
                                due_dt = due_date if isinstance(due_date, datetime) else datetime.strptime(str(due_date), "%Y-%m-%d")
                                days_over = (datetime.now().date() - due_dt).days
                                if days_over > 0:
                                    over.append(f"{days_over} days over")
                            except Exception:
                                pass
                        if over:
                            extra = f" ({', '.join(over)})"
                msg = f"  {s.replace('_', ' ').title()}: {color}{status}{ENDC}"
                if due_miles:
                    msg += f" (Due @ {due_miles} mi)"
                if due_date:
                    msg += f" (Due by {due_date})"
                msg += extra
                service_rows.append((sort_key, msg))
            # Sort by OK (0), Due Soon (1), Overdue (2)
            for _, msg in sorted(service_rows, key=lambda x: x[0]):
                print(msg)

if __name__ == "__main__":
    CLI().run()
