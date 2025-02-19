# DDoS Protection API

## Overview
A comprehensive backend system for DDoS attack detection, monitoring, and mitigation, built with FastAPI and PostgreSQL. The system provides real-time alerts, automated mitigation responses, and detailed analytics for network security management.

## Features
- Real-time DDoS attack detection and alerting
- Automated mitigation response
- Traffic analysis and visualization
- Customer-specific monitoring and reporting
- Role-based access control
- Multi-tenant architecture

## Tech Stack
- FastAPI (Python 3.8+)
- PostgreSQL
- JWT Authentication
- SQLAlchemy ORM
- Pydantic
- Pytest

## Quick Start

### Prerequisites
- Python 3.8+
- PostgreSQL
- Git

### Installation

1. Clone the repository:
```bash
git clone [repository-url]
cd dbFurukawaTech_DDOS_AppSite_BackEnd
```

2. Run the setup script:
```bash
./scripts/setup_backend.sh
```

3. Start the API:
```bash
./scripts/run_api.sh
```

The API will be available at `http://localhost:8000`. API documentation can be accessed at `http://localhost:8000/docs`.

## Environment Variables

Create a `.env` file in the root directory with the following variables:

```env
DB_NAME=your_db_name
DB_USER=your_db_user
DB_PASSWORD=your_db_password
DB_HOST=localhost
DB_PORT=5432
SECRET_KEY=your_secret_key
ACCESS_TOKEN_EXPIRE_MINUTES=30
REFRESH_TOKEN_EXPIRE_DAYS=7
```

## Project Structure
```
.
├── api/               # API implementation
├── data/             # Database and data management
├── utils/            # Utility functions
├── tests/            # Test suites
├── scripts/          # Shell scripts
└── docs/             # Documentation
```

## Development

### Setting Up Development Environment
```bash
# Create virtual environment
python -m venv venv
source venv/bin/activate  # Linux/Mac
# or
.\venv\Scripts\activate  # Windows

# Install dependencies
pip install -r requirements.txt
```

### Running Tests
```bash
pytest
```

### Code Style
```bash
# Format code
black .

# Lint code
flake8
```

## API Documentation

Full API documentation is available at:
- Swagger UI: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc`

## Backup

To backup the system:
```bash
./scripts/backup_backend.sh
```

## Support

For support and questions, please contact the development team.

## License

This project is proprietary and confidential. Unauthorized copying or distribution is prohibited.