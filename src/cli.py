from controller import Controller
from view import View
from datetime import datetime
from models import ServiceName, Address
import sys


class CLI:
    """
    Designed to facilitate a Command Line Interface (CLI) application. It acts as the entry point, defining how the
    program parses, processes, and executes text-based arguments typed by a user into a terminal or command prompt.
    """

    SERVICES = [
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

    def __init__(self):
        self.controller = Controller()

    def run(self):
        """
        Executes the program.
        """
        while True:
            print("\n" + View.header("MotorMinder - Maintenance Tracker"))
            print(View.menu_option(1, "List Vehicles"))
            print(View.menu_option(2, "Add Vehicle"))
            print(View.menu_option(3, "Edit Vehicle"))
            print(View.menu_option(4, "Log Service"))
            print(View.menu_option(5, "Maintenance Dashboard"))
            print(View.menu_option(6, "Find a Mechanic"))
            print(View.error("0. Exit"))

            choice = input(View.bold("Select an option: "))

            actions = {
                '1': self.list_vehicles,
                '2': self.add_vehicle,
                '3': self.edit_vehicle,
                '4': self.log_service,
                '5': self.maintenance_dashboard,
                '6': self.find_mechanic,
            }

            if choice == '0':
                print(View.ok("Goodbye!"))
                sys.exit(0)

            action = actions.get(choice)

            if action:
                action()
            else:
                print(View.warning("Invalid option."))

    def list_vehicles(self):
        """
        Lists all the vehicles in the system.
        """
        vehicles = self.controller.get_vehicles()

        if not vehicles:
            print(View.color("No vehicles found.", View.OKCYAN))
            return

        print(View.ok("--- Vehicle List ---"))

        for idx, v in enumerate(vehicles):
            print(View.vehicle_row(idx, v))

    def add_vehicle(self):
        """
        Adds a new vehicle.
        """
        make = input("Make: ")
        model = input("Model: ")

        # Year validation
        while True:
            year_input = input("Year: ")
            try:
                year = int(year_input)
                if year < 1886:
                    print(View.warning("Invalid input. Year must be greater than 1886."))
                    continue
                break
            except ValueError:
                print(View.warning("Invalid input. Please enter a valid integer for year."))

        # Mileage validation
        while True:
            mileage_input = input("Current Mileage: ")
            try:
                mileage = int(mileage_input)
                if mileage < 0:
                    print(View.warning("Invalid input. Mileage must be greater than 0."))
                    continue
                break
            except ValueError:
                print(View.warning("Invalid input. Please enter a valid integer for mileage."))

        self.controller.add_vehicle(make, model, year, mileage)

        print(View.ok("Vehicle added."))

    def get_valid_vehicle_index(self):
        """
        Gets a valid vehicle index.
        """
        vehicles = self.controller.get_vehicles()

        if not vehicles:
            print(View.error("No vehicles found."))
            return None

        while True:
            try:
                idx = int(input(f"Select vehicle index (0 - {len(vehicles) - 1}): "))
                if idx < 0 or idx >= len(vehicles):
                    print(View.warning(f"Invalid input. Please enter a number between 0 and {len(vehicles) - 1}."))
                    continue
                return idx
            except ValueError:
                print(View.warning("Invalid input. Please enter a valid integer for vehicle."))

    def get_valid_int(self, prompt, min_value=None, max_value=None):
        """
        Gets a valid integer value (i.e., vehicle year or mileage).
        :param prompt: Input prompt.
        :param min_value: Minimum value (for vehicle year, the minimum value should be 1886).
        :param max_value: Maximum value (for vehicle year, the maximum value should be the current year).
        :return: Valid integer value.
        """
        while True:
            try:
                value = int(input(prompt))
                if min_value is not None and value < min_value:
                    print(View.warning(f"Value must be at least {min_value}."))
                    continue

                if max_value is not None and value > max_value:
                    print(View.warning(f"Value must be at most {max_value}."))
                    continue

                return value
            except ValueError:
                print(View.warning("Invalid input. Please enter a valid integer."))

    def edit_vehicle(self):
        """
        Edits an existing vehicle.
        """
        self.list_vehicles()

        idx = self.get_valid_vehicle_index()
        if idx is None:
            return

        vehicles = self.controller.get_vehicles()

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
                current_year = datetime.today().year
                v.year = self.get_valid_int("New Year: ", min_value=1886, max_value=current_year)
                self.controller.edit_vehicle(idx, v.make, v.model, v.year, v.current_mileage)
                print(View.ok("Year updated."))
            elif choice == '4':
                v.current_mileage = self.get_valid_int(f"New Current Mileage (>= {v.current_mileage}): ",
                                                       min_value=v.current_mileage)
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

    def get_valid_date(self, prompt):
        """
        Gets a valid date.
        :param prompt: Users chosen date.
        :return: Valid date.
        """
        while True:
            date_input = input(prompt)

            if date_input.strip() == "":
                return None

            try:
                parsed_date = datetime.strptime(date_input, "%Y-%m-%d")
                if parsed_date.date() > datetime.today().date():
                    print(View.error("Invalid date. Please enter a valid date."))
                    continue
                return date_input
            except ValueError:
                print(View.warning("Invalid date format. Use YYYY-MM-DD."))

    def log_service(self):
        """
        Logs the service of a vehicle to the vehicles details.
        """
        self.list_vehicles()

        idx = self.get_valid_vehicle_index()
        if idx is None:
            return

        services = self.SERVICES

        print(View.ok("Select service:"))

        for i, s in enumerate(services):
            print(f"  {i + 1}. {s.value.replace('_', ' ').title()}")

        sidx = int(input("Service number: ")) - 1

        if sidx < 0 or sidx >= len(services):
            print(View.warning("Invalid service selection."))
            return

        service = services[sidx]

        mileage = self.get_valid_int("Service mileage: ", min_value=0)
        date_str = self.get_valid_date("Service date (YYYY-MM-DD, blank for today): ")
        self.controller.log_service(idx, service, mileage, date_str or None)

        print(View.ok("Service logged."))

    def maintenance_dashboard(self):
        """
        Displays the maintenance dashboard.
        """
        vehicles = self.controller.get_vehicles()

        if not vehicles:
            print(View.color("No vehicles found.", View.OKCYAN))
            return

        print(View.ok("--- Maintenance Dashboard ---"))
        print(View.color("Status Legend:", View.OKCYAN))
        print("  OK        - Service is within the recommended interval.")
        print("  Due Soon  - Service is approaching its mileage limit.")
        print("  Overdue   - Service mileage has exceeded the limit.")

        services = self.SERVICES

        for idx, v in enumerate(vehicles):
            print("\n" + View.color(f"[{idx}] {v.year} {v.make} {v.model}", View.OKCYAN))
            print(f"Odometer: {v.current_mileage}")
            service_rows = []

            for s in services:
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

    def find_mechanic(self):
        """
        Finds a mechanic for the user that is closest to their location.
        """
        city = input("Enter your city: ")
        state = input("Enter your state (e.g., UT): ")

        mechanic = self.controller.get_mechanics_by_city(city, state)

        if mechanic is None:
            print(View.color("No mechanics found.", View.OKCYAN))
            return

        address = mechanic["address"]
        services_formatted = ", ".join(s.replace("_", " ").title() for s in mechanic["services"])

        print("\nA mechanic was found in your city:")
        print("Name:", mechanic["name"])
        print("Address:",
              f"{address['address_line_1']}, "
              f"{address['city']}, "
              f"{address['state']} {address['zip_code']}")
        print("Phone:", mechanic["phone"])
        print("Email:", mechanic["email"])
        print("Website:", mechanic["website"])
        print("Services:", services_formatted)
        print("Rating:", mechanic["rating"])
        print("Price Range:", mechanic["price_range"])
        print("Appointment Required:", mechanic["appointment_required"])
        print("Hours:")
        day_order = ["monday", "tuesday", "wednesday", "thursday", "friday", "saturday", "sunday"]
        for day in day_order:
            if day in mechanic["hours"]:
                print(f"  {day.title():<9} {mechanic['hours'][day]}")


if __name__ == "__main__":
    CLI().run()
