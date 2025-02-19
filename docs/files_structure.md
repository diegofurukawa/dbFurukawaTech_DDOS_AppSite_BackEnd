.
├── api
│   ├── __init__.py
│   ├── main.py
│   ├── models
│   │   ├── alert_model.py
│   │   ├── company_model.py
│   │   ├── customer_dashboard_model.py
│   │   ├── customer_model.py
│   │   ├── customer_mo_model.py
│   │   ├── __init__.py
│   │   ├── managed_object_model.py
│   │   ├── mitigation_model.py
│   │   ├── traffic_model.py
│   │   └── user_model.py
│   └── routes
│       ├── alert_routes.py
│       ├── company_routes.py
│       ├── customer_dashboard_routes.py
│       ├── customer_mo_routes copy.py
│       ├── customer_mo_routes.py
│       ├── customer_routes.py
│       ├── __init__.py
│       ├── managed_object_routes.py
│       ├── mitigation_routes.py
│       └── user_routes.py
├── data
│   ├── config.py
│   ├── database.py
│   ├── data_saver.py
│   ├── import
│   │   ├── alerts
│   │   ├── geoip
│   │   ├── managed_objects
│   │   └── mitigations
│   ├── __init__.py
│   └── schemas
│       ├── __init__.py
│       ├── keys.py
│       ├── old
│       │   ├── alerts.py
│       │   ├── managed_objects.py
│       │   ├── mitigations.py
│       │   └── users.py
│       ├── tables.py
│       └── views.py
├── docs
│   └── estrutura_backend.md
├── LICENSE
├── README.md
├── requirements.txt
├── scripts
│   ├── run_api_old.sh
│   ├── run_api.sh
│   ├── search.sh
│   └── setup_backend.sh
├── sql_scripts
│   └── create_tables_views.sql
├── src
├── tests
│   ├── integration
│   └── unit
└── utils
    ├── auth.py
    ├── generate_secret_key.py
    ├── __init__.py
    └── log.py

20 directories, 47 files