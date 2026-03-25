class View:
    """
    View utility for CLI formatting and message building.
    """

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
        """
        Wraps the given text in the specified ANSI color code.
        :param text: The text to be colorized.
        :param color_code: The ANSI color code.
        :return: A string with the color applied and reset at the end.
        """
        return f"{color_code}{text}{cls.ENDC}"

    @classmethod
    def bold(cls, text):
        """
        Formats the given text in bold for CLI output.
        :param text: The text to be bolded.
        :return: A bold-formatted string.
        """
        return f"{cls.BOLD}{text}{cls.ENDC}"

    @classmethod
    def header(cls, text):
        """
        Formats text as a CLI header using bold and header color styling.
        :param text: The header text.
        :return: A formatted header string.
        """
        return f"{cls.HEADER}{cls.BOLD}{text}{cls.ENDC}"

    @classmethod
    def menu_option(cls, number, text):
        """
        Formats a numbered menu option for CLI display.
        :param number: The menu option number.
        :param text: The description of the menu option.
        :return: A formatted menu option string.
        """
        return f"{cls.OKCYAN}{number}. {text}{cls.ENDC}"

    @classmethod
    def error(cls, text):
        """
        Formats an error message using the error color.
        :param text: The error message text.
        :return: A formatted error message string.
        """
        return f"{cls.FAIL}{text}{cls.ENDC}"

    @classmethod
    def warning(cls, text):
        """
        Formats a warning message using the warning color.
        :param text: The warning message text.
        :return: A formatted warning message string.
        """

        return f"{cls.WARNING}{text}{cls.ENDC}"

    @classmethod
    def ok(cls, text):
        """
        Formats a success or OK message using the success color.
        :param text: The success message text.
        :return: A formatted success message string.
        """
        return f"{cls.OKGREEN}{text}{cls.ENDC}"

    @classmethod
    def vehicle_row(cls, idx, vehicle):
        """
        Formats a single vehicle entry for display in a list.
        :param idx: Index or selection number of the vehicle.
        :param vehicle: A vehicle object containing year, make, model, and current mileage attributes.
        :return: A formatted vehicle display string.
        """
        return f"{cls.OKCYAN}[{idx}] {vehicle.year} {vehicle.make} {vehicle.model} {cls.ENDC}{cls.OKGREEN}(Odometer: {vehicle.current_mileage}){cls.ENDC}"

    @classmethod
    def service_status_msg(cls, service_name, svc_status):
        """
        Builds a formatted service status message with conditional coloring and supplemental service information.
        :param service_name: Enum value representing the service name.
        :param svc_status: ServiceStatus dataclass containing status details.
        :return: A formatted service status message string.
        """
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
