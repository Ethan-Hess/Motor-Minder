# MotorMinder

## Overview
<!--
Brief description of the project, its purpose, and the problem it solves.
-->
This project proposes the development of a car maintenance tracking and recommendation application designed to help vehicle owners better understand, manage, and maintain their vehicles' health. A lot of drivers have a hard time keeping track of routine maintenance, like oil changes, tire rotations, inspections, etc. This can lead to unnecessary repairs, wasted money, and reduced vehicle lifespan. This application aims to consolidate vehicle information to give the user valuable maintenance recommendations based on vehicle condition data.

## Project Goals
<!--
High-level objectives for the system.
Example: improve vehicle maintenance awareness, reduce missed service intervals.
-->
On top of maintenance recommendations, the application will also include functionality to track regular checkups and services. Users will be able to record when a maintenance task was performed, update mileage, and view upcoming or even overdue services. A third, and important, feature of the system is the ability to find nearby mechanics. The application will provide a list of local mechanic options (using sample data in the initial release), to allow users to connect service visits with specific repair shops or providers.

## Features
### Implemented in Sprint 1 (MVP)
<!--
List core features available in the first iteration.
-->
The focal point of our minimum viable product (MVP) will be tracking basic vehicle information and simulating maintenance needs using sample data. Users will be able to view one or more vehicles that will have associated attributes like current mileage, service history, and overall health indicators. With this information, the application will recommend when maintenance is due at appropriate times, like oil changes, brake inspections and replacement, or tire replacements. In the initial release, the application will not connect to real vehicles, and all data will be generated and managed internally using predefined or simulated vehicle records. Using this approach will allow the core logic and system design to be developed without having to rely on any external hardware or third-party integrations.

### Planned for Future Sprints
<!--
List features that are intentionally out of scope for Sprint 1.
-->

## System Architecture
<!--
High-level description of system components.
Reference the architecture diagram.
-->

## Design Overview
### Object-Oriented Design
<!--
Brief explanation of how the system is structured using OO principles.
-->

### Design Patterns
<!--
List and justify selected design patterns (e.g., Strategy, Factory, Observer).
-->

## UML Diagrams
<!--
List included UML diagrams (Class, Use Case, etc.).
-->

## Prototype
<!--
Description of the prototype, what it demonstrates, and its limitations.
-->

## Data Model
<!--
Explain the use of sample/mock vehicle data and why it is used in Sprint 1.
-->

## Testing
### Testing Plan
<!--
High-level testing strategy.
-->
Testing in Sprint 1 focuses on validating the core functionality of the MVP, including data handling, vehicle and service logic, and basic user interaction through the terminal-based prototype. Because the system uses simulated vehicle data, testing is limited to logical correctness rather than real-world accuracy.

#### Testing Objectives
- Verify that sample vehicle data is loaded and stored correctly
- Ensure maintenance service recommendations are generated based on mileage rules
- Validate correct interaction flow in the terminal interface
- Identify and document defects early in development

#### Types of Testing

##### Unit Testing
Unit testing will focus on individual classes and methods, including:
- Vehicle mileage updates
- Service due calculations
- JSON data creation and loading

Unit tests will be manual or lightweight, as automated testing is planned for future sprints.

##### Integration Testing
Integration testing will verify interactions between major components, including:
- DataHandler loading vehicle data into the system
- Controller accessing vehicle and service information
- Correct data flow between classes

##### System Testing
System testing will be performed by running the prototype end-to-end to ensure:
- Users can view vehicle information
- Maintenance recommendations are displayed correctly
- The application behaves as expected under normal usage

#### Test Environment
- **Programming Language:** Python
- **Execution Environment:** Local development machines
- **Data Source:** Simulated JSON vehicle data
- **Interface:** Terminal-based user interface

#### Defect Tracking
Defects identified during testing will be documented using a standardized bug report template. Each report will include a description of the issue, steps to reproduce, expected behavior, and actual behavior. Bug resolution will be prioritized in future sprints.

#### Roles and Responsibilities
All team members are responsible for testing features they implement. The team lead coordinates testing efforts and ensures that defects are documented and reviewed.

#### Limitations
Testing in Sprint 1 does not include performance, security, or real vehicle data validation. These areas are planned for later sprints as system functionality expands.

### Test Cases
<!--
Brief description of example test cases.
-->

## Future Enhancements
<!--
Planned improvements such as real vehicle integration, expanded diagnostics, etc.
-->
 Future Improvements
•	Export maintenance logs to CSV or PDF
•	Add reminder notifications (e.g., via email or system alerts)
•	Implement user accounts
•	Develop a GUI 

## Team Roles and Responsibilities
<!--
List team members and their primary responsibilities.
-->
The team follows a collaborative development model in which all members contribute to design, implementation, and documentation. Responsibilities are distributed by area of focus rather than rigid job titles to support flexibility and shared ownership of the project.

- **Preston Little - Team Lead / Systems Coordination**
  - Facilitates SCRUM meetings and sprint planning
  - Maintains contribution logs and meeting notes
  - Oversees system architecture and design consistency
  - Contributes to core design artifacts and implementation
- **Ethan Hess**
  - Developed the software prototype
  - Develops UML and use case diagrams
  - Assists with requirements analysis
  - Contributes to documentation and design reviews
- **Ethan Kidd**
  - Develops UML and use case diagrams
  - Assists with requirements analysis
  - Contributes to documentation and design reviews
- **Ryan Carbine**
  - Develops UML and use case diagrams
  - Assists with requirements analysis
  - Contributes to documentation and design reviews

## Setup and Usage
<!--
Instructions for running the prototype.
-->
Installation
Requirements
•	Python 3.10+
Setup
After downloading the program you’ll see the menu:
MotorMinder - Maintenance Tracker
1. List Vehicles
2. Add Vehicle
3. Edit Vehicle
4. Log Service
5. Maintenance Dashboard
0. Exit

 Usage
1. Add a Vehicle
Make: Toyota
Model: Camry
Year: 2020
Current Mileage: 25000
Vehicle added.
2. Edit a Vehicle
Update make, model, year, or mileage or delete the vehicle entirely.
3. Log a Service
Record a service event:
Select vehicle index: 0
Select service: Oil Change
Service mileage: 26000
Service date (YYYY-MM-DD, blank for today):
Service logged.
4. Maintenance Dashboard
Displays each vehicle’s maintenance status:
[0] 2020 Toyota Camry
Odometer: 26000
  ✅ Oil Change: OK (Due @ 32000 mi)
  🟡 Tire Rotation: Due Soon (Due @ 30000 mi)
  🔴 Battery: Overdue (1,200 mi over)

Data Storage
All data is stored locally in a JSON file (vehicles.json), automatically created at first run.
Example:
{
  "vehicles": [
    {
      "make": "Honda",
      "model": "Civic",
      "year": 2019,
      "current_mileage": 42000,
      "last_service": {
        "oil_change": {"mileage": 40000, "date": "2025-10-01"},
        "tire_rotation": {"mileage": 38000, "date": "2025-08-15"}
      }
    }
  ]
}

Customization
service_intervals.json
Defines when each service becomes Due Soon or Overdue by mileage or time:
{
  "OIL_CHANGE": { "miles": [4000, 6000], "months": [4, 6] },
  "TIRE_ROTATION": { "miles": [5000, 8000] },
  "BATTERY": { "years": [3, 5] }
}
Key	Meaning
"miles": [min, max]	Min = Due Soon threshold; Max = Overdue threshold
"months" / "years"	Optional time-based thresholds

 Example Session
1. Add Vehicle
2. Log Oil Change
3. View Dashboard
Output:
[0] 2020 Toyota Camry
Odometer: 26000
  ✅ Oil Change: OK (Due @ 32000 mi)
  🟡 Tire Rotation: Due Soon

## Repository Structure
<!--
Brief explanation of important directories/files.
-->
MotorMinder

- main.py                 # Entry point, runs CLI
- cli.py                  # Handles user interaction and menu navigation
- controller.py           # Core application logic and service status checks
- data_handler.py         # Handles JSON data loading, saving, and updating
- models.py               # Defines Vehicle, ServiceRecord, and ServiceName enums
- view.py                 # Handles CLI formatting (colors, bold text, etc.)
- service_intervals.json  # Defines maintenance intervals for each service
- vehicles.json           # Auto-generated data file for user’s vehicles

## Assessment and Risks
<!--
Identified risks, assumptions, and mitigation strategies.
-->

## Contributers
Ethan Hess, Ethan Kidd, Preston Little, Ryan Carbine
