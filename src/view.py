# View utility for CLI formatting and message building
class View:
    # ANSI color codes
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

    @classmethod
    def color(cls, text, color_code):
        return f"{color_code}{text}{cls.ENDC}"

    @classmethod
    def bold(cls, text):
        return f"{cls.BOLD}{text}{cls.ENDC}"

    @classmethod
    def header(cls, text):
        return f"{cls.HEADER}{cls.BOLD}{text}{cls.ENDC}"

    @classmethod
    def menu_option(cls, number, text):
        return f"{cls.OKCYAN}{number}. {text}{cls.ENDC}"

    @classmethod
    def error(cls, text):
        return f"{cls.FAIL}{text}{cls.ENDC}"

    @classmethod
    def warning(cls, text):
        return f"{cls.WARNING}{text}{cls.ENDC}"

    @classmethod
    def ok(cls, text):
        return f"{cls.OKGREEN}{text}{cls.ENDC}"

    @classmethod
    def vehicle_row(cls, idx, vehicle):
        return f"{cls.OKCYAN}[{idx}] {vehicle.year} {vehicle.make} {vehicle.model} {cls.ENDC}{cls.OKGREEN}(Odometer: {vehicle.current_mileage}){cls.ENDC}"

    @classmethod
    def service_status_msg(cls, service_name, svc_status):
        # svc_status: ServiceStatus dataclass
        match svc_status.status:
            case "OK":
                color = cls.OKGREEN
            case "Due Soon":
                color = cls.WARNING
            case _:
                color = cls.FAIL
        msg = f"  {service_name.value.replace('_', ' ').title()}: {color}{svc_status.status}{cls.ENDC}"
        if svc_status.due_miles:
            msg += f" (Due @ {svc_status.due_miles} mi)"
        if svc_status.due_date:
            msg += f" (Due by {svc_status.due_date})"
        if svc_status.missing:
            msg += " (no service recorded)"
        if svc_status.overdue_amount:
            msg += f" ({svc_status.overdue_amount})"
        return msg
