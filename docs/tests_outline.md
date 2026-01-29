# MotorMinder Test Plan

This document outlines suggested tests and test cases for the MotorMinder CLI vehicle maintenance tracker.

## 1. DataHandler (src/data_handler.py)
- **Test loading vehicles.json**
  - Loads valid JSON file
  - Handles missing or malformed file gracefully
- **Test saving vehicles.json**
  - Persists new/edited vehicle data
- **Test CRUD operations**
  - Add vehicle
  - Edit vehicle
  - Delete vehicle

## 2. Models (src/models.py)
- **Test Vehicle and ServiceRecord dataclasses**
  - to_dict/from_dict round-trip
  - Handles missing/extra fields
- **Test ServiceName Enum**
  - All expected services present

## 3. Controller (src/controller.py)
- **Test get_vehicles()**
  - Returns correct list of Vehicle objects
- **Test add/edit vehicle**
  - Adds/edits vehicle and persists changes
- **Test log_service()**
  - Adds service record to correct vehicle
  - Handles invalid vehicle/service gracefully
- **Test get_service_status()**
  - Returns correct status (OK, Due Soon, Overdue)
  - Handles missing service records
  - Correctly calculates due/overdue amounts

## 4. CLI (src/cli.py)
- **Test menu navigation**
  - All options accessible
  - Handles invalid input
- **Test add/edit vehicle via CLI**
  - Prompts for all fields
  - Updates data as expected
- **Test log service via CLI**
  - Prompts for service, mileage, date
  - Updates service record
- **Test maintenance dashboard**
  - Displays correct color/status for each service
  - Handles vehicles with no service records

## 5. Integration Tests
- **End-to-end: Add vehicle, log service, check dashboard**
- **Edge cases:**
  - No vehicles in system
  - Vehicle with no services logged
  - Overdue service by mileage/date
  - Service logged with future date/mileage

## 6. Error Handling
- **Invalid user input**
- **File I/O errors**
- **Corrupt/missing config files**

---

## Example Test Case (pytest style)

```python
# test_controller.py
import pytest
from controller import Controller
from models import ServiceName

def test_add_vehicle_and_log_service(tmp_path):
    # Setup: use temp file for vehicles.json
    controller = Controller(data_path=tmp_path / "vehicles.json")
    controller.add_vehicle("Toyota", "Camry", 2020, 10000)
    vehicles = controller.get_vehicles()
    assert len(vehicles) == 1
    v = vehicles[0]
    controller.log_service(0, ServiceName.OIL_CHANGE, 10000, "2024-01-01")
    status = controller.get_service_status(v, ServiceName.OIL_CHANGE)
    assert status.status == "OK"
```

---

## Notes
- Use `pytest` for unit and integration tests.
- Use fixtures or temp files to avoid overwriting real data.
- Mock user input for CLI tests.
- Consider code coverage tools to ensure all logic is tested.
