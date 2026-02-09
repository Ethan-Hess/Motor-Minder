# Design Patterns in MotorMinder

## Overview

MotorMinder is a Python-based CLI application for vehicle maintenance tracking. The project is architected to ensure scalability, maintainability, and clear separation of concerns. This documentation summarizes the design patterns incorporated into the project.

---

## 1. Model-View-Controller (MVC)

**Pattern:** MVC

- **Model:** Handles data logic and persistence (`models.py`, `data_handler.py`).
- **View:** Manages CLI formatting and user output (`view.py`).
- **Controller:** Bridges user actions and model updates (`controller.py`).
- **CLI:** Entry point for user interaction (`cli.py`).

**Benefit:** Promotes separation of concerns, easier maintenance, and scalability.

---

## 2. Singleton Pattern

**Pattern:** Singleton

- **Where:** `DataHandler` class in `data_handler.py`.
- **How:** Uses a class-level `_instance` and custom `__new__` method to ensure only one instance exists for data management.

**Benefit:** Centralizes data access and persistence, prevents conflicting data states.

---

## 3. Command Pattern

**Pattern:** Command

- **Where:** `CLI` class in `cli.py`.
- **How:** Maps user menu selections to method calls, acting as a command dispatcher.

**Benefit:** Simplifies user input handling, makes adding new commands straightforward.

---

## 4. Additional Patterns and Principles

- **Dataclass/Value Object:** `ServiceRecord`, `Vehicle`, and `ServiceStatus` use Python's `@dataclass` for clean, immutable data structures.
- **Adapter (Implicit):** The `Controller` adapts between CLI and model/data layers.
- **Enum Usage:** `ServiceName` enum for type-safe service names.
- **Composition:** Controller composes a DataHandler instance.

---

## Summary

MotorMinder incorporates at least three distinct design patterns:

- Model-View-Controller (MVC)
- Singleton
- Command

These patterns, along with additional object-oriented principles, ensure the project is well-structured, maintainable, and extensible.

---

**For further details, see:**

- [mvp.md](mvp.md)
- [src/cli.py](src/cli.py)
- [src/controller.py](src/controller.py)
- [src/data_handler.py](src/data_handler.py)
- [src/models.py](src/models.py)
- [src/view.py](src/view.py)
