# Heartbeat - A Dead Man's Switch

A Python-based check-in monitoring system designed to detect missed deadlines and trigger automated alerts when expected check-ins don't occur.

Heartbeat explores backend engineering, API design, persistent data storage, and reliable event processing, with the potential to support personal safety check-ins, scheduled task monitoring, and automated workflows.

## Tech Stack

- **Python** - Core application logic
- **FastAPI** - REST API development
- **SQLite** - Persistent data storage
- **Pydantic** - Request validation

## Features

### Current Implementation
- REST API with a health-check endpoint
- Create monitors with configurable check-in intervals
- Input validation to prevent invalid intervals
- Persistent monitor storage using SQLite
- Automatic deadline calculation using UTC timestamps

### Planned Core Functionality
- Retrieve existing monitors through the API
- Reset deadlines through user check-ins
- Automatically detect missed deadlines
- Trigger notifications when deadlines expire
- Automated tests for core functionality

## Getting Started

### Prerequisites
- Python 3.10+
- pip

### Installation

1. Clone the repository:

   `git clone https://github.com/YOUR_USERNAME/heartbeat-deadman-switch.git`

2. Navigate into the project directory:

   `cd heartbeat-deadman-switch`

3. Install dependencies:

   `python -m pip install "fastapi[standard]"`

4. Start the development server:

   `python -m fastapi dev main.py`

5. Open the interactive API documentation:

   `http://127.0.0.1:8000/docs`

### API Endpoints

| Method | Endpoint | Description |
|---|---|---|
| GET | `/health` | Check API availability |
| POST | `/monitors` | Create a new monitor with a specified interval |

## Architecture

Heartbeat currently follows a simple modular structure:

- **API Layer:** Handles HTTP requests, responses, and input validation.
- **Database Layer:** Manages persistent monitor storage and deadline data.

Separating these responsibilities helps keep the code maintainable and makes future architectural changes easier.

## Development Roadmap

### Core Functionality

- [x] Initialise FastAPI backend
- [x] Implement health-check endpoint
- [x] Create monitors with input validation
- [x] Integrate persistent SQLite storage
- [x] Calculate check-in deadlines
- [ ] Retrieve stored monitors
- [ ] Implement check-in and deadline reset functionality
- [ ] Detect missed check-ins
- [ ] Trigger automated notifications
- [ ] Add automated tests

### Future Possibilities

As Heartbeat evolves, potential engineering improvements include:

- **Scalability:** PostgreSQL, concurrent workers, and distributed task queues.
- **Reliability:** Retry mechanisms, fault recovery, and idempotent event processing.
- **Security:** Authentication, authorisation, and multi-user support.
- **Deployment:** Docker, cloud hosting, and system observability.
- **Integrations:** Webhooks and external APIs for custom automated actions.

These are potential directions for exploration rather than requirements for the initial release.

## Project Status

**Early development — core API and persistent storage implemented.**

Heartbeat is being developed incrementally, with an emphasis on understanding the engineering decisions, testing functionality, and building a reliable foundation before introducing additional complexity.
