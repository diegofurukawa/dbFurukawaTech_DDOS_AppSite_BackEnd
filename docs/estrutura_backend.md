.
├── api
│   ├── __init__.py
│   ├── main.py
│   ├── models
│   │   ├── alert_model.py
│   │   ├── __init__.py
│   │   ├── mitigation_model.py
│   │   ├── traffic_model.py
│   │   └── user_model.py
│   └── routes
│       ├── alert_routes.py
│       ├── __init__.py
│       ├── mitigation_routes.py
│       └── user_routes.py
├── data
│   ├── config.py
│   ├── database.py
│   ├── data_saver.py
│   ├── import
│   │   ├── alerts
│   │   ├── geoip
│   │   ├── managed_objects
│   │   └── mitigations
│   ├── __init__.py
│   └── schemas
│       ├── alerts.py
│       ├── __init__.py
│       ├── managed_objects.py
│       └── mitigations.py
├── docs
│   └── estrutura_backend.md
├── LICENSE
├── README.md
├── requirements.txt
├── scripts
│   ├── backup_backend.sh
│   ├── run_api.sh
│   ├── search.sh
│   └── setup_backend.sh
├── src
├── tests
│   ├── integration
│   └── unit
└── utils
    ├── __init__.py
    └── log.py