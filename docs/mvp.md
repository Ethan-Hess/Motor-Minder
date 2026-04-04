# MotorMinder MVP Documentation

MotorMinder is a Python-based CLI utility designed to help vehicle owners track maintenance history and predict upcoming service needs based on mileage and time intervals.

## Architecture (MVC Pattern)

This project follows the **Model-View-Controller** design pattern to ensure scalability and clean separation of concerns:

- **Model (`models.py` & `data_handler.py`):** Manages the data logic, JSON serialization, and the maintenance interval calculations.
- **View (`cli.py`):** The Console Interface. It handles all user inputs and displays formatted tables/recommendations to the user.
- **Controller (`controller.py`):** Acts as the bridge. It takes input from the CLI, processes it through the Model, and updates the View.

---

## Maintenance Schedule Logic

The system calculates "Service Due" status based on the following threshold table. The script flags a service if _either_ the mileage or the time limit is reached.

| Service                   | Mileage Interval (Miles) | Time Interval |
| ------------------------- | ------------------------ | ------------- |
| **Oil Change**            | 5,000 – 7,500            | 3 – 6 Months  |
| **Air Intake Filter**     | 15,000 – 30,000          | N/A           |
| **Cabin Air Filter**      | 15,000 – 25,000          | 12 Months     |
| **Tire Rotation**         | 5,000 – 7,500            | N/A           |
| **Transmission Fluid**    | 30,000 – 60,000          | N/A           |
| **Brake Pads/Inspection** | 25,000 – 70,000          | N/A           |
| **Battery**               | 30,000 – 50,000          | 3 – 5 Years   |
| **Coolant Flush**         | 30,000 – 50,000          | N/A           |
| **Spark Plugs**           | 30,000 – 100,000         | N/A           |
| **Brake Fluid**           | 20,000 – 45,000          | 2 – 3 Years   |

---

## Data Structure

The system persists data in `vehicles.json`. Below is the schema for a vehicle record:

```json
{
  "vehicles": [
    {
      "make": "Chevrolet",
      "model": "Cobalt",
      "year": 2010,
      "current_mileage": 125000,
      "last_service": {
        "oil_change": { "mileage": 122000, "date": "2025-11-01" },
        "tire_rotation": { "mileage": 120000, "date": "2025-08-15" }
      }
    }
  ]
}
```

## Service Interval Configuration

Service intervals are now stored in `mvp/service_intervals.json` for easy updates without code changes. Each key is a service name (matching the Enum in code). Each value is an object with interval types (miles, months, years) and their min/max values as arrays. Example:

```json
{
  "oil_change": { "miles": [5000, 7500], "months": [3, 6] },
  "air_intake_filter": { "miles": [15000, 30000] }
}
```

- To change recommended intervals, edit this file and restart the app.
- Do not add comments to the JSON file (JSON does not support comments).
- If you need to document changes, use this README or a changelog.

---

## Getting Started

### Prerequisites

- Python 3.x
- Standard Libraries: `json`, `datetime`, `os`

### Installation & Run

1. Clone the repository.
2. Navigate to the directory.
3. Run the script:

```bash
python mvp/main.py

```

---

## Features (MVP Scope)

- [x] **Add/Edit Vehicle:** Store Make, Model, Year, and Odometer.
- [x] **Log Service:** Update the last completed mileage and date for specific tasks.
- [x] **Maintenance Dashboard:** View a color-coded summary of what is "OK", "Due Soon", or "Overdue".
- [x] **JSON Persistence:** Automatically save and load data from `vehicles.json`.

---

## Future Roadmap

WIP
