# alerts.py
"""Schema definition for alerts table"""

ALERTS_SCHEMA = """
    CREATE TABLE IF NOT EXISTS alerts (
        alert_id VARCHAR(255) PRIMARY KEY,
        alert_name VARCHAR(255),
        alert_type VARCHAR(255),
        start_time TIMESTAMP,
        stop_time TIMESTAMP,
        duration INTEGER,
        max_impact_bps BIGINT,
        max_impact_pps BIGINT,
        confidence INTEGER,
        ongoing BOOLEAN,
        importance VARCHAR(255),
        mo_gid VARCHAR(255),
        mo_name VARCHAR(255),
        mo_misusesig VARCHAR(255),
        host_address VARCHAR(255),
        ip_version VARCHAR(255),
        isFastDetected BOOLEAN,
        direction VARCHAR(255),
        device_gid VARCHAR(255),
        device_name VARCHAR(255),
        threshold FLOAT,
        severity_pct FLOAT,
        unit VARCHAR(255),
        max_impact_boundary VARCHAR(255),
        mo_importance VARCHAR(255),
        misusetypes VARCHAR(255),
        mimpact_bps VARCHAR(255),
        country VARCHAR(255),
        updated_at TIMESTAMP,
        inserted_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
"""