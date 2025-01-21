"""
Database Schemas Module

Define os esquemas das tabelas do banco de dados.
"""

# Definição dos esquemas das tabelas
TABLE_SCHEMAS = {
    "alerts": """
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
    """,
    
    "mitigations": """
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
    """,
    
    "managed_objects": """
        CREATE TABLE IF NOT EXISTS managedobjects (
            id VARCHAR(255) PRIMARY KEY,
            gid VARCHAR(255),
            name VARCHAR(255),
            description TEXT,
            full_match TEXT,
            match TEXT,
            intf_boundary VARCHAR(255),
            
            -- Campos booleanos
            autodetected BOOLEAN,
            treat_external_as_internal BOOLEAN,
            automitigation_profiled BOOLEAN,
            automitigation_learned_prefixes BOOLEAN,
            automitigation_learned_prefixes_mitigate_on_query_failure BOOLEAN,
            automitigation_tms_enabled BOOLEAN,
            automitigation_tms_reuse BOOLEAN,
            blackhole_auto_enabled BOOLEAN,
            flowspec_auto_enabled BOOLEAN,
            sightline_signaling_auto_enabled BOOLEAN,
            match_dark BOOLEAN,
            match_enabled BOOLEAN,
            dynamic_match_enabled BOOLEAN,
            dynamic_match_multitenant_enabled BOOLEAN,
            profiled_use_snmp BOOLEAN,
            require_targeted_cs_requests_evaluated BOOLEAN,
            
            -- Campos numéricos
            tiered_blackhole_tms_bps BIGINT,
            tiered_blackhole_tms_pps BIGINT,
            profiled_incoming_bps BIGINT,
            profiled_incoming_pps BIGINT,
            profiled_outgoing_bps BIGINT,
            profiled_outgoing_pps BIGINT,
            bandwidth_threshold INTEGER,
            pps_threshold INTEGER,
            protocol_threshold INTEGER,
            num_children INTEGER,
            automitigation_stop_minutes INTEGER,
            blackhole_auto_stop_minutes INTEGER,
            profiled_severity_duration INTEGER,
            host_severity_duration INTEGER,
            
            -- Campos de configuração
            ip_location_policing_rates TEXT,
            blackhole_auto_bgp_session_ipv4 TEXT,
            scrubber_baselines TEXT,
            host_detection_shared_set TEXT,
            mitigation_automitigation_traffic TEXT,
            flowspec_auto_ruleset TEXT,
            host_detection_shared_set_custom TEXT,
            scrub_insight_mo_match TEXT,
            mitigation_templates_manual_ipv4 TEXT,
            mitigation_templates_manual_ipv6 TEXT,
            mitigation_templates_auto_ipv4 TEXT,
            mitigation_templates_auto_ipv6 TEXT,
            
            -- Campos de monitoramento de host
            host_chargen_amp_trigger INTEGER,
            host_chargen_amp_trigger_pps INTEGER,
            host_chargen_amp_severity INTEGER,
            host_chargen_amp_severity_pps INTEGER,
            
            host_cldap_amp_trigger INTEGER,
            host_cldap_amp_trigger_pps INTEGER,
            host_cldap_amp_severity INTEGER,
            host_cldap_amp_severity_pps INTEGER,
            
            host_dns_trigger INTEGER,
            host_dns_trigger_pps INTEGER,
            host_dns_severity INTEGER,
            host_dns_severity_pps INTEGER,
            
            host_dns_amp_trigger INTEGER,
            host_dns_amp_trigger_pps INTEGER,
            host_dns_amp_severity INTEGER,
            host_dns_amp_severity_pps INTEGER,
            
            -- Campos de data
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP,
            
            -- Índices
            UNIQUE (gid)
        );

        -- Índices adicionais para otimização
        CREATE INDEX IF NOT EXISTS idx_mo_name ON managedobjects(name);
        CREATE INDEX IF NOT EXISTS idx_mo_updated ON managedobjects(updated_at);        
    """
}