# mitigations.py
"""Schema definition for mitigations table"""

MITIGATIONS_SCHEMA = """
    CREATE TABLE IF NOT EXISTS mitigations (
        mitigation_id VARCHAR(255) PRIMARY KEY,
        name VARCHAR(255),
        subtype VARCHAR(255),
        auto BOOLEAN,
        type VARCHAR(255),
        type_name VARCHAR(255),
        config_id VARCHAR(255),
        prefix VARCHAR(255),
        alert_id VARCHAR(255),
        degraded VARCHAR(255),
        user_mitigation VARCHAR(255),
        is_automitigation BOOLEAN,
        ip_version INTEGER,
        flist_gid VARCHAR(255),
        is_learning BOOLEAN,
        learning_cancelled BOOLEAN,
        mo_name VARCHAR(255),
        mo_gid VARCHAR(255),
        duration INTEGER,
        ongoing BOOLEAN,
        start_time TIMESTAMP,
        stop_time TIMESTAMP,
        updated_at TIMESTAMP,
        inserted_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
"""