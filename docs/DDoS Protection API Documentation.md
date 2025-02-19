# DDoS Protection API Documentation

## Table of Contents
- [Overview](#overview)
- [System Architecture](#system-architecture)
- [Features](#features)
- [Technical Stack](#technical-stack)
- [Project Structure](#project-structure)
- [API Endpoints](#api-endpoints)
- [Database Schema](#database-schema)
- [Installation Guide](#installation-guide)
- [Development Guide](#development-guide)

## Overview

The DDoS Protection API is a comprehensive backend system designed to monitor, detect, and manage DDoS attacks. It provides real-time alerts, mitigation strategies, and detailed analytics for network security management.

## System Architecture

The system is built using a modern microservices architecture with the following key components:

- **FastAPI Backend**: High-performance REST API
- **PostgreSQL Database**: Robust data storage
- **Authentication System**: JWT-based secure authentication
- **Real-time Monitoring**: Alert and mitigation tracking
- **Customer Management**: Multi-tenant support with customer-specific views

## Features

### Core Features
- Real-time DDoS attack detection and alerting
- Automated mitigation response
- Traffic analysis and visualization
- Customer-specific monitoring and reporting
- Role-based access control
- Multi-tenant architecture

### Security Features
- JWT authentication
- Role-based permissions
- Secure password hashing
- Request rate limiting
- Audit logging

## Technical Stack

### Backend Framework
- FastAPI (Python 3.8+)
- Uvicorn ASGI server
- Pydantic for data validation

### Database
- PostgreSQL
- SQLAlchemy ORM
- Alembic for migrations

### Authentication
- JWT tokens (jose)
- Bcrypt password hashing
- OAuth2 with Password flow

### Development Tools
- Python 3.8+
- pip for package management
- pytest for testing
- black for code formatting
- flake8 for linting

## Project Structure

```
.
├── api
│   ├── models/
│   │   ├── alert_model.py
│   │   ├── company_model.py
│   │   ├── customer_model.py
│   │   └── ...
│   ├── routes/
│   │   ├── alert_routes.py
│   │   ├── company_routes.py
│   │   └── ...
│   └── main.py
├── data/
│   ├── database.py
│   ├── schemas/
│   └── ...
├── utils/
│   ├── auth.py
│   ├── log.py
│   └── ...
├── tests/
│   ├── integration/
│   └── unit/
└── scripts/
    ├── run_api.sh
    ├── setup_backend.sh
    └── ...
```

## API Endpoints

### Alert Management
- `GET /api/alerts/current` - Get current active alerts
- `GET /api/alerts/stats` - Get alert statistics
- `GET /api/alerts/traffic` - Get traffic data
- `GET /api/alerts/top` - Get top alerts

### Mitigation Management
- `GET /api/mitigations/stats` - Get mitigation statistics
- `GET /api/mitigations/current` - Get current mitigations
- `GET /api/mitigations/top` - Get top mitigations
- `GET /api/mitigations/{id}` - Get specific mitigation

### Customer Management
- `GET /api/customers` - List customers
- `POST /api/customers` - Create customer
- `PATCH /api/customers/{id}` - Update customer
- `GET /api/customers/{id}` - Get customer details

### User Management
- `POST /api/users/login` - User login
- `GET /api/users/me` - Get current user
- `POST /api/users/register` - Register new user
- `PATCH /api/users/{id}` - Update user

## Database Schema

### Core Tables
- `alerts` - DDoS attack alerts
- `mitigations` - Attack mitigation records
- `managed_objects` - Network objects under protection
- `users` - System users
- `companies` - Customer companies
- `customers` - Company customers

### Views
- `vw_alerts` - Consolidated alert view
- `vw_mitigations` - Mitigation status view
- `vw_customer_dashboard` - Customer dashboard data

## Installation Guide

1. Clone the repository:
   ```bash
   git clone [repository-url]
   cd dbFurukawaTech_DDOS_AppSite_BackEnd
   ```

2. Create and activate virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # Linux/Mac
   # or
   .\venv\Scripts\activate  # Windows
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Set up environment variables:
   ```bash
   cp .env.example .env
   # Edit .env with your configurations
   ```

5. Initialize the database:
   ```bash
   python -m alembic upgrade head
   ```

6. Run the application:
   ```bash
   ./scripts/run_api.sh
   ```

## Development Guide

### Setting Up Development Environment

1. Install development dependencies:
   ```bash
   pip install -r requirements-dev.txt
   ```

2. Set up pre-commit hooks:
   ```bash
   pre-commit install
   ```

### Code Style
- Follow PEP 8 guidelines
- Use Black for code formatting
- Use flake8 for linting
- Type hints are required for all functions

### Testing
- Write unit tests for all new features
- Maintain minimum 80% code coverage
- Run tests before committing:
  ```bash
  pytest
  ```

### Logging
- Use the built-in logging system
- Log all critical operations
- Include appropriate context in log messages

### Security
- Follow security best practices
- Never commit sensitive data
- Use environment variables for secrets
- Validate all input data

### Performance
- Use async/await for I/O operations
- Implement caching where appropriate
- Monitor database query performance
- Use connection pooling

### Documentation
- Document all new features
- Update API documentation
- Include docstrings for all functions
- Keep README up to date

## License

This project is proprietary and confidential. Unauthorized copying or distribution is prohibited.