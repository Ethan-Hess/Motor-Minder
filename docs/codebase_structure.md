# MotorMinder — Codebase Structure Reference

## Table of Contents

1. [Project Overview](#1-project-overview)
2. [Directory Layout](#2-directory-layout)
3. [Architecture & Design Patterns](#3-architecture--design-patterns)
4. [Source Files](#4-source-files)
   - [main.py](#41-mainpy)
   - [cli.py](#42-clipy)
   - [controller.py](#43-controllerpy)
   - [data_handler.py](#44-data_handlerpy)
   - [models.py](#45-modelspy)
   - [view.py](#46-viewpy)
5. [Data Files](#5-data-files)
   - [vehicles.json](#51-vehiclesjson)
   - [service_intervals.json](#52-service_intervalsjson)
6. [Test Suite](#6-test-suite)
7. [Data Flow](#7-data-flow)
8. [Class & Type Reference](#8-class--type-reference)

---

## 1. Project Overview

**MotorMinder** is a terminal-based vehicle maintenance tracking application written in Python 3.10+. It allows users to manage a list of personal vehicles, log service events (oil changes, tire rotations, etc.), and view a maintenance dashboard that flags services as OK, Due Soon, or Overdue based on configurable mileage and time thresholds.

All data is stored locally in JSON files — no external database or network connection is required.

---

## 2. Directory Layout

```
The-Backlog-Blackhole/
├── README.md                          # Project overview, usage, design summary
├── .gitignore
│
├── docs/
│   ├── diagrams/
│   │   ├── Architecture.md            # C4-style architecture diagram (Mermaid)
│   │   ├── UML Diagram.png            # Class diagram
│   │   └── Use Case Diagram.png       # Use case diagram
│   ├── meeting_logs/                  # Weekly meeting notes (.docx)
│   ├── Contribution Form.docx
│   ├── maintenance_items.txt
│   ├── mvp.md
│   ├── MotorMinder (Project Outline).pdf
│   ├── Project Description - MotorMinder.pdf
│   ├── Prototype Demo.pdf
│   └── Sprint 1 Backlog and Tasks.tsv
│
└── src/
    ├── main.py                        # Entry point — instantiates and runs CLI
    ├── cli.py                         # User-facing menus and input handling
    ├── controller.py                  # Business logic; service status calculation
    ├── data_handler.py                # JSON read/write (Singleton)
    ├── models.py                      # Core data structures (Vehicle, ServiceRecord, ServiceName)
    ├── view.py                        # ANSI-colored CLI output formatting
    ├── vehicles.json                  # Persisted vehicle and service data
    ├── service_intervals.json         # Maintenance thresholds per service type
    └── tests/
        ├── __init__.py
        ├── test_cli.py
        ├── test_controller.py
        ├── test_data_handler.py
        └── test_models.py
```

---

## 3. Architecture & Design Patterns

The system follows a layered **MVC (Model-View-Controller)** structure, supplemented by two additional design patterns.

### Layer Responsibilities

| Layer | File(s) | Responsibility |
|---|---|---|
| **Model** | `models.py`, `data_handler.py` | Data structures and JSON persistence |
| **View** | `view.py` | Terminal output formatting (colors, bold, layout) |
| **Controller** | `controller.py` | Business logic, service status calculation, coordinates model and view |
| **Entry Point** | `cli.py`, `main.py` | User interaction loop, menu dispatch |

### Design Patterns Applied

#### 1. MVC (Model-View-Controller)
The application separates data (`models.py`, `data_handler.py`), display formatting (`view.py`), and application logic (`controller.py`) into distinct layers. The `CLI` class (`cli.py`) acts as the primary consumer, calling the Controller to process actions and using the View to format responses.

#### 2. Singleton (`DataHandler`)
`DataHandler` overrides `__new__` to ensure only one instance is ever created. This centralizes all file I/O so concurrent operations cannot produce conflicting data states. The singleton guard uses a class-level `_instance` attribute and an `_initialized` flag to prevent re-initialization.

```python
# data_handler.py:12-24
_instance = None

def __new__(cls, filename='vehicles.json'):
    if cls._instance is None:
        cls._instance = super(DataHandler, cls).__new__(cls)
        cls._instance._initialized = False
    return cls._instance
```

#### 3. Command Pattern (`CLI`)
The `CLI.run()` loop maps integer menu choices to specific method calls. Each menu option corresponds to a discrete command (`list_vehicles`, `add_vehicle`, `edit_vehicle`, `log_service`, `maintenance_dashboard`). Adding a new feature requires only registering a new menu entry and a corresponding method.

---

## 4. Source Files

### 4.1 `main.py`

**Lines:** 4
**Purpose:** Sole entry point of the application.

```python
from cli import CLI

if __name__ == "__main__":
    CLI().run()
```

Imports `CLI`, instantiates it, and calls `run()`. All startup logic is delegated to `CLI.__init__`, which in turn instantiates `Controller`, which instantiates `DataHandler`.

---

### 4.2 `cli.py`

**Class:** `CLI`
**Purpose:** The interactive shell. Renders menus, reads user input, delegates to the `Controller`, and uses the `View` to format output.

**Constructor:**
```python
def __init__(self):
    self.controller = Controller()
```
Instantiating `CLI` automatically boots the full application stack (Controller → DataHandler → file load).

**Methods:**

| Method | Description |
|---|---|
| `run()` | Infinite loop displaying the main menu and routing input to handler methods. Exits on choice `'0'` via `sys.exit(0)`. |
| `list_vehicles()` | Retrieves all vehicles from the Controller and prints them using `View.vehicle_row()`. |
| `add_vehicle()` | Prompts for make, model, year, and mileage, then calls `controller.add_vehicle()`. |
| `edit_vehicle()` | Lists vehicles, selects one by index, then provides a sub-menu to edit make/model/year/mileage or delete the vehicle. |
| `log_service()` | Lists vehicles, selects one, displays a numbered list of service types, prompts for mileage and date, then calls `controller.log_service()`. |
| `maintenance_dashboard()` | Iterates all vehicles and all service types, calls `controller.get_service_status()` for each combination, sorts results by urgency (OK → Due Soon → Overdue), and prints them. |

**Main Menu Options:**

```
1. List Vehicles
2. Add Vehicle
3. Edit Vehicle
4. Log Service
5. Maintenance Dashboard
0. Exit
```

**Notable behaviors:**
- The edit sub-menu loops until the user chooses `'0'` (Back) or confirms a deletion.
- Service date defaults to today's date if left blank.
- The dashboard sorts services per-vehicle so Overdue items appear last (highest urgency displayed at bottom for easy scanning).

---

### 4.3 `controller.py`

**Classes:** `ServiceStatus` (dataclass), `Controller`
**Purpose:** Business logic layer. Computes service status and coordinates CRUD operations between the CLI and DataHandler.

#### `ServiceStatus` dataclass

```python
@dataclass
class ServiceStatus:
    status: str           # "OK", "Due Soon", "Overdue", or "Unknown"
    due_miles: int | None
    due_date: object | None
    overdue_amount: str | None
    missing: bool         # True if no service record exists for this service
```

Returned by `get_service_status()` and consumed by `View.service_status_msg()`.

#### `Controller.__init__(data_file='vehicles.json')`

1. Instantiates `DataHandler` with the given filename.
2. Reads `service_intervals.json` from the same directory as `controller.py`.
3. Parses interval data: converts string keys to `ServiceName` enum values, and list values to tuples for use in comparisons.
4. Stores the result in `self.SERVICE_INTERVALS: Dict[ServiceName, dict]`.

#### `Controller.get_service_status(vehicle, service_name, today=None) → ServiceStatus`

The core calculation method. Determines whether a service is OK, Due Soon, or Overdue for a given vehicle.

**Input normalization:** Accepts either a `ServiceName` enum or a plain string. If the string doesn't match any known service, returns `ServiceStatus("Unknown", ...)`.

**Logic flow:**

1. Look up the service's intervals in `self.SERVICE_INTERVALS`.
2. Look up the vehicle's last service record for this service type.
3. If no record exists → return `ServiceStatus("Overdue", ..., missing=True)`.
4. **Mileage check** (if `"miles"` key exists in the interval):
   - `miles_since = current_mileage - last_mileage`
   - If `miles_since >= max` → `"Overdue"`
   - If `miles_since >= min` → `"Due Soon"`
5. **Time check — months** (if `"months"` key exists):
   - Computes `delta_months` from `last.date` to `today`.
   - Same min/max threshold logic as mileage.
6. **Time check — years** (if `"years"` key exists):
   - Computes `delta_years` from `last.date` to `today`.
   - Same min/max threshold logic.
7. `overdue_amount` is a human-readable string like `"500 mi over"` or `"12 days over"` (can combine both with `, `).

**Key design note:** If both mileage and time checks are present, either can escalate the status to `"Overdue"` or `"Due Soon"`. The worst-case status wins.

#### Other Controller methods

| Method | Description |
|---|---|
| `get_vehicles()` | Returns a list of `Vehicle` objects by calling `DataHandler.get_vehicles()` and converting each dict via `Vehicle.from_dict()`. |
| `add_vehicle(make, model, year, current_mileage)` | Constructs a `Vehicle`, converts to dict, passes to `DataHandler.add_vehicle()`. |
| `edit_vehicle(idx, make, model, year, current_mileage)` | Constructs a `Vehicle` with new values and calls `DataHandler.update_vehicle(idx, ...)`. |
| `delete_vehicle(idx)` | Delegates to `DataHandler.delete_vehicle(idx)`. |
| `log_service(idx, service_name, mileage, date_str)` | Normalizes `service_name` to its string value, defaults `date_str` to today if not provided, then calls `DataHandler.log_service()`. |
| `get_vehicle_services(idx)` | Returns a `Dict[str, ServiceRecord]` of all service records for the vehicle at index `idx`. Returns `{}` if the index is out of bounds. |

---

### 4.4 `data_handler.py`

**Class:** `DataHandler` (Singleton)
**Purpose:** All JSON file I/O. The single source of truth for persistent data within a running session.

**Internal state:**
- `self.filename` — path to the JSON file
- `self.data` — in-memory dict: `{"vehicles": [...]}`

#### Singleton mechanism

`__new__` checks `cls._instance`. If `None`, creates the instance and sets `_initialized = False`. `__init__` guards with `if self._initialized: return` to prevent re-running initialization on subsequent calls with the same or a different filename.

> **Test note:** Tests reset `DataHandler._instance = None` in `setUp` to force fresh instances per test.

#### Methods

| Method | Signature | Description |
|---|---|---|
| `load()` | `→ None` | Opens `self.filename` and loads JSON into `self.data`. If the file doesn't exist, calls `save()` to create it. |
| `save()` | `→ None` | Writes `self.data` to `self.filename` with 2-space indentation. |
| `get_vehicles()` | `→ List[Dict]` | Returns `self.data["vehicles"]`, or `[]` if the key is missing. |
| `add_vehicle(vehicle)` | `→ None` | Appends the vehicle dict to `self.data["vehicles"]` and calls `save()`. |
| `update_vehicle(idx, vehicle)` | `→ None` | Replaces the vehicle at position `idx` and calls `save()`. |
| `delete_vehicle(idx)` | `→ None` | Removes the vehicle at position `idx` if the index is valid, then calls `save()`. |
| `log_service(idx, service_name, mileage, date)` | `→ None` | Adds or updates the `last_service[service_name]` entry on the vehicle dict at `idx`, then calls `save()`. |

---

### 4.5 `models.py`

**Classes/Enums:** `ServiceName`, `ServiceRecord`, `Vehicle`
**Purpose:** Core data structures representing domain objects.

#### `ServiceName` (Enum)

An enum of all supported service types. Each member's value is the snake_case string used as a key in JSON.

| Member | Value |
|---|---|
| `OIL_CHANGE` | `"oil_change"` |
| `AIR_INTAKE_FILTER` | `"air_intake_filter"` |
| `CABIN_AIR_FILTER` | `"cabin_air_filter"` |
| `TIRE_ROTATION` | `"tire_rotation"` |
| `TRANSMISSION_FLUID` | `"transmission_fluid"` |
| `BRAKE_PADS_INSPECTION` | `"brake_pads_inspection"` |
| `BATTERY` | `"battery"` |
| `COOLANT_FLUSH` | `"coolant_flush"` |
| `SPARK_PLUGS` | `"spark_plugs"` |
| `BRAKE_FLUID` | `"brake_fluid"` |

#### `ServiceRecord` (dataclass)

Represents a single logged maintenance event.

| Field | Type | Description |
|---|---|---|
| `mileage` | `int` | Odometer reading when the service was performed |
| `date` | `str` | ISO 8601 date string (`"YYYY-MM-DD"`) |

**Methods:**
- `to_dict() → Dict` — serializes to `{"mileage": int, "date": str}`
- `from_dict(data) → ServiceRecord` (static) — deserializes from the same dict shape

#### `Vehicle` (dataclass)

Represents a vehicle and its full service history.

| Field | Type | Description |
|---|---|---|
| `make` | `str` | Manufacturer (e.g., `"Toyota"`) |
| `model` | `str` | Model name (e.g., `"Camry"`) |
| `year` | `int` | Model year |
| `current_mileage` | `int` | Current odometer reading |
| `last_service` | `Dict[ServiceName, ServiceRecord]` | Map of service type to most recent record; defaults to `{}` |

**Methods:**
- `to_dict() → Dict` — serializes the vehicle including nested `last_service` records
- `from_dict(data) → Vehicle` (static) — deserializes, converting each `last_service` entry via `ServiceRecord.from_dict()`

---

### 4.6 `view.py`

**Class:** `View`
**Purpose:** Pure formatting utility. All methods are class methods — `View` is never instantiated. Applies ANSI escape codes for colored terminal output.

**ANSI color constants:**

| Constant | ANSI Code | Usage |
|---|---|---|
| `HEADER` | `\033[95m` | Section headers |
| `OKBLUE` | `\033[94m` | (Available for use) |
| `OKCYAN` | `\033[96m` | Menu options, vehicle rows |
| `OKGREEN` | `\033[92m` | Success messages, OK status |
| `WARNING` | `\033[93m` | Warnings, Due Soon status |
| `FAIL` | `\033[91m` | Errors, Overdue status, Exit option |
| `BOLD` | `\033[1m` | Bold text |
| `UNDERLINE` | `\033[4m` | Underlined text |
| `ENDC` | `\033[0m` | Resets all formatting |

**Methods:**

| Method | Output |
|---|---|
| `color(text, color_code)` | Wraps text in any given ANSI code |
| `bold(text)` | Bold-formatted text |
| `header(text)` | Bold + header-colored text |
| `menu_option(number, text)` | Cyan-colored `"N. text"` line |
| `error(text)` | Red-colored text |
| `warning(text)` | Yellow-colored text |
| `ok(text)` | Green-colored text |
| `vehicle_row(idx, vehicle)` | Cyan `[idx] year make model` + green `(Odometer: N)` |
| `service_status_msg(service_name, svc_status)` | Formatted service line with conditional color (green/yellow/red), due mileage, due date, overdue amount, and missing flag |

---

## 5. Data Files

### 5.1 `vehicles.json`

Auto-generated on first run. Stores all vehicle and service data. Structure:

```json
{
  "vehicles": [
    {
      "make": "Toyota",
      "model": "Camry",
      "year": 2017,
      "current_mileage": 68500,
      "last_service": {
        "oil_change": { "mileage": 65000, "date": "2025-10-01" },
        "tire_rotation": { "mileage": 65000, "date": "2025-10-01" }
      }
    }
  ]
}
```

- The `last_service` object is a flat map: service type string → `{mileage, date}`.
- Only the most recent record per service type is stored (each log overwrites the previous).
- The array index of a vehicle is its ID; deletion shifts all subsequent indices.

### 5.2 `service_intervals.json`

Read-only configuration file. Defines the `[Due Soon threshold, Overdue threshold]` for each service type by mileage and/or time. Loaded once at `Controller.__init__`.

```json
{
  "oil_change":           { "miles": [5000, 7500], "months": [3, 6] },
  "air_intake_filter":    { "miles": [15000, 30000] },
  "cabin_air_filter":     { "miles": [15000, 25000], "months": [12, 12] },
  "tire_rotation":        { "miles": [5000, 7500] },
  "transmission_fluid":   { "miles": [30000, 60000] },
  "brake_pads_inspection":{ "miles": [25000, 70000] },
  "battery":              { "miles": [30000, 50000], "years": [3, 5] },
  "coolant_flush":        { "miles": [30000, 50000] },
  "spark_plugs":          { "miles": [30000, 100000] },
  "brake_fluid":          { "miles": [20000, 45000], "years": [2, 3] }
}
```

**Interval format:** `[min, max]`
- `min` = miles/months/years since last service before the service becomes **Due Soon**
- `max` = threshold at which the service becomes **Overdue**

When `min == max` (e.g., `cabin_air_filter` months: `[12, 12]`), there is no "Due Soon" window — the status jumps directly from OK to Overdue.

---

## 6. Test Suite

Located in `src/tests/`. Uses Python's built-in `unittest` framework. Each test file adds `src/` to `sys.path` to allow direct imports.

### `test_models.py`

Tests `ServiceRecord` and `Vehicle` serialization round-trips.

| Test | Description |
|---|---|
| `TestServiceRecord.test_to_dict` | Verifies `ServiceRecord.to_dict()` produces the correct dict |
| `TestServiceRecord.test_from_dict` | Verifies `ServiceRecord.from_dict()` produces correct field values |
| `TestVehicle.test_to_dict` | Verifies `Vehicle.to_dict()` including nested service records |
| `TestVehicle.test_from_dict` | Verifies `Vehicle.from_dict()` reconstructs all fields and service records |

### `test_data_handler.py`

Uses `tempfile.mkstemp()` to create a temporary JSON file per test. Resets `DataHandler._instance = None` is handled implicitly through fresh temp files.

| Test | Description |
|---|---|
| `test_load` | Writes sample JSON then checks `handler.data` matches |
| `test_save` | Mutates `handler.data` and verifies the file is updated |
| `test_get_vehicles` | Verifies vehicle list retrieval from in-memory data |
| `test_add_vehicle` | Adds a vehicle and verifies the file contains it |
| `test_update_vehicle` | Replaces a vehicle at index 0 and checks the file |
| `test_delete_vehicle` | Deletes index 0 from a two-vehicle list and checks the survivor |
| `test_log_service` | Logs a service entry and verifies the nested `last_service` structure |

### `test_controller.py`

Uses `tempfile` for isolation and resets `DataHandler._instance = None` in both `setUp` and `tearDown`.

| Test | Description |
|---|---|
| `test_get_service_status` | Tests all four status outcomes: OK, Due Soon, Overdue (by mileage), Overdue (no record), and unknown service name; also tests string input normalization |
| `test_get_vehicles` | Writes two vehicles to a temp file and verifies both are returned as `Vehicle` instances |
| `test_add_vehicle` | Adds a vehicle and inspects the saved JSON |
| `test_edit_vehicle` | Adds then edits a vehicle and verifies the updated fields |
| `test_delete_vehicle` | Adds two vehicles, deletes the first, verifies only the second remains |
| `test_log_service` | Logs a service with enum, with string, and with no date (defaulting to today); verifies all three cases |
| `test_get_vehicle_services` | Verifies service retrieval, `ServiceRecord` typing, and out-of-bounds index handling |

### `test_cli.py`

Uses `unittest.mock.patch` to intercept `input()` and `print()`, and `MagicMock` to replace the Controller.

| Test | Description |
|---|---|
| `test_run` | Simulates input `'0'`; asserts `SystemExit(0)` and `"Goodbye!"` is printed |
| `test_list_vehicles` | Mocks controller returning one vehicle; asserts header is printed |
| `test_add_vehicle` | Simulates user typing vehicle details; asserts `controller.add_vehicle` is called correctly |
| `test_edit_vehicle` | Simulates selecting vehicle 0, choosing "Edit Make", typing a new make, then going back |
| `test_log_service` | Simulates selecting vehicle 0, service 1, and entering mileage/date |
| `test_maintenance_dashboard` | Mocks vehicle list and service status; asserts dashboard header is printed |

---

## 7. Data Flow

### Adding a Vehicle

```
User input (CLI.add_vehicle)
  → Controller.add_vehicle(make, model, year, mileage)
    → Vehicle(make, model, year, mileage).to_dict()
    → DataHandler.add_vehicle(dict)
      → self.data["vehicles"].append(dict)
      → self.save() → vehicles.json
```

### Viewing the Dashboard

```
CLI.maintenance_dashboard()
  → Controller.get_vehicles()
    → DataHandler.get_vehicles() → List[dict]
    → [Vehicle.from_dict(d) for d in list]
  → for each vehicle, for each ServiceName:
      Controller.get_service_status(vehicle, service_name)
        → reads SERVICE_INTERVALS[service_name]
        → reads vehicle.last_service[service_name]
        → computes mileage and/or time delta
        → returns ServiceStatus
    → View.service_status_msg(service_name, svc_status) → formatted string
    → print(msg)
```

### Logging a Service

```
User input (CLI.log_service)
  → Controller.log_service(idx, service_name, mileage, date_str)
    → normalizes service_name to str value
    → defaults date_str to today if None
    → DataHandler.log_service(idx, service_name, mileage, date_str)
      → vehicle["last_service"][service_name] = {mileage, date}
      → self.save() → vehicles.json
```

---

## 8. Class & Type Reference

```
ServiceName (Enum)
├── Values: oil_change, air_intake_filter, cabin_air_filter, tire_rotation,
│           transmission_fluid, brake_pads_inspection, battery,
│           coolant_flush, spark_plugs, brake_fluid

ServiceRecord (dataclass)
├── mileage: int
├── date: str                          # "YYYY-MM-DD"
├── to_dict() → Dict
└── from_dict(data: Dict) → ServiceRecord  [static]

Vehicle (dataclass)
├── make: str
├── model: str
├── year: int
├── current_mileage: int
├── last_service: Dict[ServiceName, ServiceRecord]  (default: {})
├── to_dict() → Dict
└── from_dict(data: Dict) → Vehicle    [static]

ServiceStatus (dataclass)
├── status: str                        # "OK" | "Due Soon" | "Overdue" | "Unknown"
├── due_miles: int | None
├── due_date: date | None
├── overdue_amount: str | None         # e.g. "500 mi over, 12 days over"
└── missing: bool

DataHandler (Singleton)
├── _instance: ClassVar
├── filename: str
├── data: Dict                         # {"vehicles": [...]}
├── load()
├── save()
├── get_vehicles() → List[Dict]
├── add_vehicle(vehicle: Dict)
├── update_vehicle(idx: int, vehicle: Dict)
├── delete_vehicle(idx: int)
└── log_service(idx: int, service_name: str, mileage: int, date: str)

Controller
├── data_handler: DataHandler
├── SERVICE_INTERVALS: Dict[ServiceName, Dict[str, tuple]]
├── get_service_status(vehicle, service_name, today=None) → ServiceStatus
├── get_vehicles() → List[Vehicle]
├── add_vehicle(make, model, year, current_mileage)
├── edit_vehicle(idx, make, model, year, current_mileage)
├── delete_vehicle(idx)
├── log_service(idx, service_name, mileage, date_str=None)
└── get_vehicle_services(idx) → Dict[str, ServiceRecord]

View (utility class — all class methods)
├── color(text, color_code) → str
├── bold(text) → str
├── header(text) → str
├── menu_option(number, text) → str
├── error(text) → str
├── warning(text) → str
├── ok(text) → str
├── vehicle_row(idx, vehicle) → str
└── service_status_msg(service_name, svc_status) → str

CLI
├── controller: Controller
├── run()
├── list_vehicles()
├── add_vehicle()
├── edit_vehicle()
├── log_service()
└── maintenance_dashboard()
```
