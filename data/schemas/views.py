# sql_scripts/views.py
"""
SQL Views and Additional Scripts

Define as views e scripts SQL adicionais do sistema.
"""

# Índices
INDICES = {
    'users_email_idx': """
        CREATE INDEX IF NOT EXISTS idx_users_email 
        ON public.users USING btree (email)
    """,
    'access_requests_email_idx': """
        CREATE INDEX IF NOT EXISTS idx_access_requests_email 
        ON public.access_requests USING btree (email)
    """,
    'access_requests_status_idx': """
        CREATE INDEX IF NOT EXISTS idx_access_requests_status 
        ON public.access_requests USING btree (status)
    """
}

# Foreign Keys
FOREIGN_KEYS = {
    'access_requests_user_fk': """
        ALTER TABLE IF EXISTS public.access_requests 
        DROP CONSTRAINT IF EXISTS access_requests_processed_by_fkey;
        
        ALTER TABLE IF EXISTS public.access_requests 
        ADD CONSTRAINT access_requests_processed_by_fkey 
        FOREIGN KEY (processed_by) REFERENCES public.users(idUser)
    """
}

# Views Básicas
BASIC_VIEWS = {
    'vw_datenow': """
        CREATE OR REPLACE VIEW public.vw_datenow AS 
        SELECT now() - '03:00:00'::interval AS ddatenow;
    """,
    
    'vw_calendar_month': """
        CREATE OR REPLACE VIEW public.vw_calendar_month AS
        WITH cte_datenow AS (
            SELECT vw_datenow.ddatenow FROM vw_datenow
        ), cte_calendar AS (
            SELECT calendar.ddate
            FROM (
                SELECT generate_series(
                    concat(date_part('year'::text, cte_datenow.ddatenow), '-01-01')::timestamp without time zone,
                    concat(date_part('year'::text, cte_datenow.ddatenow), '-12-31')::timestamp without time zone,
                    '1 day'::interval
                ) AS date_series
                FROM cte_datenow
            ) calendar(ddate)
        )
        SELECT cte_calendar.ddate::date AS ddate
        FROM cte_calendar
        WHERE date_part('month'::text, cte_calendar.ddate) = 
              date_part('month'::text, (SELECT ddatenow FROM cte_datenow))
    """,

    'vw_calendar_today': """
        CREATE OR REPLACE VIEW public.vw_calendar_today
        AS WITH cte_datenow AS (
                SELECT vw_datenow.ddatenow
                FROM vw_datenow
                ), cte_calendar AS (
                SELECT calendar.ddate
                FROM ( SELECT generate_series(concat(date_part('year'::text, cte_datenow.ddatenow), '-01-01')::timestamp without time zone, concat(date_part('year'::text, cte_datenow.ddatenow), '-12-31')::timestamp without time zone, '1 day'::interval) AS date_series
                        FROM cte_datenow) calendar(ddate)
                )
        SELECT cte_calendar.ddate::date AS date
        FROM cte_calendar
        WHERE 1 = 1 AND date_part('month'::text, cte_calendar.ddate) = date_part('month'::text, ( SELECT cte_datenow.ddatenow
                FROM cte_datenow)) AND date_part('day'::text, cte_calendar.ddate) = date_part('day'::text, ( SELECT cte_datenow.ddatenow
                FROM cte_datenow));
    """,


    'vw_calendar_year': """
        CREATE OR REPLACE VIEW public.vw_calendar_year
        AS WITH cte_datenow AS (
                SELECT vw_datenow.ddatenow
                FROM vw_datenow
                ), cte_calendar AS (
                SELECT calendar.ddate
                FROM ( SELECT generate_series(concat(date_part('year'::text, cte_datenow.ddatenow), '-01-01')::timestamp without time zone, concat(date_part('year'::text, cte_datenow.ddatenow), '-12-31')::timestamp without time zone, '1 day'::interval) AS date_series
                        FROM cte_datenow) calendar(ddate)
                )
        SELECT cte_calendar.ddate::date AS ddate
        FROM cte_calendar;
    """


}

# Views de Alertas
ALERT_VIEWS = {
    'vw_alerts': """
        CREATE OR REPLACE VIEW public.vw_alerts
        AS WITH cte_alerts_ongoing AS (
                SELECT a_1.alert_id,
                    a_1.alert_type AS type,
                    a_1.start_time::time without time zone::character varying(8) AS timestart,
                    (a_1.start_time - '03:00:00'::interval)::time without time zone::character varying(8) AS timestart_local,
                    a_1.stop_time::time without time zone::character varying(8) AS timestop,
                    (a_1.stop_time - '03:00:00'::interval)::time without time zone::character varying(8) AS timestop_local,
                    a_1.max_impact_bps::double precision / 1000000::double precision AS mps,
                    a_1.max_impact_pps::double precision / 1000::double precision AS pps,
                    a_1.ongoing,
                    a_1.importance AS severity,
                    a_1.mo_name,
                    a_1.mo_misusesig,
                    a_1.host_address,
                    a_1.country,
                    a_1.threshold,
                    a_1.severity_pct,
                    a_1.start_time,
                    a_1.stop_time,
                    a_1.inserted_at,
                    a_1.updated_at,
                    a_1.importance,
                        CASE a_1.importance
                            WHEN 'low'::text THEN 30
                            WHEN 'medium'::text THEN 60
                            ELSE 100
                        END AS nseverity,
                    (date_part('Day'::text, a_1.updated_at - now()::timestamp without time zone) * 24::double precision + date_part('Hour'::text, a_1.updated_at - now()::timestamp without time zone)) * 60::double precision + date_part('Minute'::text, a_1.updated_at - now()::timestamp without time zone) AS ndiff,
                    a_1.max_impact_pps
                FROM alerts a_1
                WHERE 1 = 1
                ), cte_alerts AS (
                SELECT a_1.alert_id,
                    a_1.alert_type AS type,
                    a_1.start_time::time without time zone::character varying(8) AS timestart,
                    (a_1.start_time - '03:00:00'::interval)::time without time zone::character varying(8) AS timestart_local,
                    a_1.stop_time::time without time zone::character varying(8) AS timestop,
                    (a_1.stop_time - '03:00:00'::interval)::time without time zone::character varying(8) AS timestop_local,
                    a_1.max_impact_bps::double precision / 1000000::double precision AS mps,
                    a_1.max_impact_pps::double precision / 1000::double precision AS pps,
                    a_1.ongoing,
                    a_1.importance AS severity,
                    a_1.mo_name,
                    a_1.mo_misusesig,
                    a_1.host_address,
                    a_1.country,
                    a_1.threshold,
                    a_1.severity_pct,
                    a_1.start_time,
                    a_1.stop_time,
                    a_1.inserted_at,
                    a_1.updated_at,
                    a_1.importance,
                        CASE a_1.importance
                            WHEN 'low'::text THEN 30
                            WHEN 'medium'::text THEN 60
                            ELSE 100
                        END AS nseverity,
                    (date_part('Day'::text, a_1.updated_at - now()::timestamp without time zone) * 24::double precision + date_part('Hour'::text, a_1.updated_at - now()::timestamp without time zone)) * 60::double precision + date_part('Minute'::text, a_1.updated_at - now()::timestamp without time zone) AS ndiff,
                    a_1.max_impact_pps
                FROM alerts a_1
                WHERE NOT (a_1.alert_id::text IN ( SELECT cte_alerts_ongoing.alert_id
                        FROM cte_alerts_ongoing))
                UNION
                SELECT cte_alerts_ongoing.alert_id,
                    cte_alerts_ongoing.type,
                    cte_alerts_ongoing.timestart,
                    cte_alerts_ongoing.timestart_local,
                    cte_alerts_ongoing.timestop,
                    cte_alerts_ongoing.timestop_local,
                    cte_alerts_ongoing.mps,
                    cte_alerts_ongoing.pps,
                    cte_alerts_ongoing.ongoing,
                    cte_alerts_ongoing.severity,
                    cte_alerts_ongoing.mo_name,
                    cte_alerts_ongoing.mo_misusesig,
                    cte_alerts_ongoing.host_address,
                    cte_alerts_ongoing.country,
                    cte_alerts_ongoing.threshold,
                    cte_alerts_ongoing.severity_pct,
                    cte_alerts_ongoing.start_time,
                    cte_alerts_ongoing.stop_time,
                    cte_alerts_ongoing.inserted_at,
                    cte_alerts_ongoing.updated_at,
                    cte_alerts_ongoing.importance,
                    cte_alerts_ongoing.nseverity,
                    cte_alerts_ongoing.ndiff,
                    cte_alerts_ongoing.max_impact_pps
                FROM cte_alerts_ongoing
                )
        SELECT row_number() OVER (PARTITION BY (a.start_time::date), a.ongoing ORDER BY a.updated_at DESC, a.severity DESC) AS rowid,
            a.alert_id,
            a.type,
            a.timestart,
            a.timestart_local,
            a.timestop,
            a.timestop_local,
            a.mps,
            a.pps,
            a.ongoing,
            a.severity,
            a.mo_name,
            a.mo_misusesig,
            a.host_address,
            a.country,
            a.threshold,
            a.severity_pct,
            a.start_time,
            a.stop_time,
            a.inserted_at,
            a.updated_at,
            a.importance,
            a.nseverity,
            a.ndiff,
            a.max_impact_pps
        FROM cte_alerts a
        WHERE a.updated_at >= now()::date;
    """,
    
    'vw_amount_alerts': """
        CREATE OR REPLACE VIEW public.vw_alert_traffic
        AS WITH cte_alert_traffic AS (
                SELECT vw_alerts.rowid,
                    vw_alerts.alert_id,
                    vw_alerts.type,
                    vw_alerts.timestart,
                    vw_alerts.timestart_local,
                    vw_alerts.timestop,
                    vw_alerts.timestop_local,
                    vw_alerts.mps,
                    vw_alerts.pps,
                    vw_alerts.ongoing,
                    vw_alerts.severity,
                    vw_alerts.mo_name,
                    vw_alerts.mo_misusesig,
                    vw_alerts.host_address,
                    vw_alerts.country,
                    vw_alerts.threshold,
                    vw_alerts.severity_pct,
                    vw_alerts.start_time,
                    vw_alerts.stop_time,
                    vw_alerts.inserted_at,
                    vw_alerts.updated_at,
                    vw_alerts.importance,
                    vw_alerts.nseverity,
                    vw_alerts.ndiff,
                    vw_alerts.max_impact_pps
                FROM vw_alerts
                ORDER BY vw_alerts.start_time DESC
                ), cte_misusetypes AS (
                SELECT DISTINCT COALESCE(a.mo_misusesig, 'Undefined'::character varying) AS misusetype
                FROM alerts a
                ), cte_alert_traffic_data AS (
                SELECT cte_alert_traffic.mo_misusesig,
                    cte_alert_traffic.start_time AS date,
                    date_trunc('minute'::text, cte_alert_traffic.timestart_local::time without time zone::interval) AS "time",
                    avg(cte_alert_traffic.pps) / 1::double precision AS value,
                    avg(cte_alert_traffic.pps) * 0.7::double precision / 1::double precision AS tcp
                FROM cte_alert_traffic
                GROUP BY (date_trunc('minute'::text, cte_alert_traffic.timestart_local::time without time zone::interval)), cte_alert_traffic.start_time, cte_alert_traffic.mo_misusesig
                ORDER BY cte_alert_traffic.start_time DESC, (date_trunc('minute'::text, cte_alert_traffic.timestart_local::time without time zone::interval)) DESC
                ), cte_alert_traffic_all AS (
                SELECT cte_alert_traffic_data.date,
                    to_char(cte_alert_traffic_data."time", 'HH24:MI'::text) AS "time",
                    'All Alert Traffic'::text AS misusetype,
                    COALESCE(cte_alert_traffic_data.value, 0::double precision) AS value,
                    COALESCE(cte_alert_traffic_data.tcp, 0::double precision) AS tcp
                FROM cte_alert_traffic_data
                ORDER BY cte_alert_traffic_data.date, (to_char(cte_alert_traffic_data."time", 'HH24:MI'::text))
                ), cte_alert_traffic_return AS (
                SELECT cte_alert_traffic_all.date,
                    cte_alert_traffic_all."time",
                    cte_alert_traffic_all.misusetype,
                    cte_alert_traffic_all.value,
                    cte_alert_traffic_all.tcp
                FROM cte_alert_traffic_all
                UNION
                SELECT d.date,
                    to_char(d."time", 'HH24:MI'::text) AS "time",
                    COALESCE(d.mo_misusesig, 'Undefined'::character varying) AS misusetype,
                    COALESCE(d.value, 0::double precision) AS value,
                    COALESCE(d.tcp, 0::double precision) AS tcp
                FROM cte_alert_traffic_data d
                    JOIN cte_misusetypes mt ON mt.misusetype::text = COALESCE(d.mo_misusesig, 'Undefined'::character varying)::text
                )
        SELECT cte_alert_traffic_return."time",
            cte_alert_traffic_return.misusetype,
            cte_alert_traffic_return.value,
            cte_alert_traffic_return.tcp
        FROM cte_alert_traffic_return
        ORDER BY cte_alert_traffic_return.misusetype, cte_alert_traffic_return.date, cte_alert_traffic_return."time";
    """,


    'vw_alert_traffic': """
        CREATE OR REPLACE VIEW public.vw_amount_alerts
        AS WITH cte_importance AS (
                SELECT 0 AS high,
                    0 AS low,
                    0 AS mediun
                ), cte_amount_alerts AS (
                SELECT a.start_time::date AS date,
                        CASE
                            WHEN a.importance::text = 'high'::text THEN count(1)
                            ELSE 0::bigint
                        END AS high,
                        CASE
                            WHEN a.importance::text = 'mediun'::text THEN count(1)
                            ELSE 0::bigint
                        END AS mediun,
                        CASE
                            WHEN a.importance::text = 'low'::text THEN count(1)
                            ELSE 0::bigint
                        END AS low
                FROM alerts a
                WHERE 1 = 1
                GROUP BY a.importance, (a.start_time::date)
                )
        SELECT cte_amount_alerts.date,
            sum(cte_amount_alerts.high) AS high,
            sum(cte_amount_alerts.mediun) AS mediun,
            sum(cte_amount_alerts.low) AS low
        FROM cte_amount_alerts
        GROUP BY cte_amount_alerts.date;        
    """,


    'vw_amount_alerts_ongoing': """
        CREATE OR REPLACE VIEW public.vw_amount_alerts_ongoing
        AS WITH cte_importance AS (
                SELECT 0 AS high,
                    0 AS low,
                    0 AS mediun
                ), cte_amount_alerts AS (
                SELECT a.start_time::date AS date,
                        CASE
                            WHEN a.importance::text = 'high'::text THEN count(1)
                            ELSE 0::bigint
                        END AS high,
                        CASE
                            WHEN a.importance::text = 'mediun'::text THEN count(1)
                            ELSE 0::bigint
                        END AS mediun,
                        CASE
                            WHEN a.importance::text = 'low'::text THEN count(1)
                            ELSE 0::bigint
                        END AS low
                FROM vw_alerts a
                WHERE 1 = 1 AND a.ongoing = true
                GROUP BY a.importance, (a.start_time::date)
                )
        SELECT cte_amount_alerts.date,
            sum(cte_amount_alerts.high) AS high,
            sum(cte_amount_alerts.mediun) AS mediun,
            sum(cte_amount_alerts.low) AS low
        FROM cte_amount_alerts
        GROUP BY cte_amount_alerts.date;       
    """



}

# Views de Mitigação
MITIGATION_VIEWS = {
    'vw_mitigation_graphic': """
        CREATE OR REPLACE VIEW public.vw_mitigation_graphic
        AS WITH cte_calendar AS (
                SELECT calendar.ddate
                FROM ( SELECT generate_series(concat(date_part('year'::text, (now()::timestamp without time zone AT TIME ZONE 'America/Sao_Paulo'::text)), '-01-01')::timestamp without time zone, concat(date_part('year'::text, (now()::timestamp without time zone AT TIME ZONE 'America/Sao_Paulo'::text)), '-12-31')::timestamp without time zone, '1 day'::interval) AS generate_series) calendar(ddate)
                WHERE date_part('month'::text, calendar.ddate) = date_part('month'::text, (now()::timestamp without time zone AT TIME ZONE 'America/Sao_Paulo'::text)) AND date_part('day'::text, calendar.ddate) = date_part('day'::text, (now()::timestamp without time zone AT TIME ZONE 'America/Sao_Paulo'::text))
                )
        SELECT a.start_time AS "time",
            avg(a.max_impact_bps / 1000000) AS mps,
            avg(a.max_impact_pps) AS pps
        FROM alerts a
        WHERE 1 = 1 AND a.ongoing = true
        GROUP BY a.start_time;
    """,
    
    'vw_mitigations_count': """
        CREATE OR REPLACE VIEW public.vw_mitigations_count
        AS WITH cte_mitigations_count AS (
                SELECT m.mo_gid,
                    count(*) AS namount
                FROM mitigations m
                    JOIN alerts a ON a.alert_id::text = m.alert_id::text
                WHERE 1 = 1
                GROUP BY m.mo_gid
                UNION
                SELECT m.mo_gid,
                    count(*) AS namount
                FROM mitigations m
                WHERE 1 = 1
                GROUP BY m.mo_gid
                )
        SELECT cte_mitigations_count.mo_gid,
            cte_mitigations_count.namount
        FROM cte_mitigations_count;
    """,


    'vw_mitigations_get_top': """
            CREATE OR REPLACE VIEW public.vw_mitigations_get_top AS 
            WITH get_top_mitigations AS (
            SELECT 
            m.mitigation_id
            ,a.alert_id
            ,a.mo_gid
            ,a.mo_name
            ,a.mo_misusesig
                ,a.host_address
            ,a.max_impact_bps
            ,a.max_impact_pps
                ,m.type
            ,m.auto  
            ,m.ip_version
            ,m.degraded
            ,a.start_time
            ,a.stop_time
            ,m.prefix
            FROM mitigations m
            INNER JOIN alerts a ON m.alert_id = a.alert_id
            )
            SELECT
                t.mitigation_id
            ,t.alert_id
            ,t.mo_gid
            ,t.mo_name
                ,t.host_address
            ,t.max_impact_bps
            ,t.max_impact_pps
                ,t.type
            ,t.auto  
            ,t.ip_version
            ,t.degraded
            ,t.start_time
            ,t.stop_time
            ,t.prefix
            FROM get_top_mitigations t
            ORDER BY start_time desc;
    """,



    'vw_mitigations_get_current': """
        CREATE OR REPLACE VIEW public.vw_mitigations_get_current AS 
        WITH mitigations_get_current AS (
        SELECT 
            m.mitigation_id
            ,a.alert_id
            ,a.host_address
            ,a.max_impact_bps
            ,a.max_impact_pps
            ,m.type
            ,m.auto  
            ,m.ip_version
            ,m.degraded
            ,a.start_time
            ,a.stop_time
            ,m.prefix
        FROM mitigations m
        INNER JOIN alerts a ON m.alert_id = a.alert_id
        WHERE 1=1
        ORDER BY A.start_time DESC
        LIMIT 1
        )
        SELECT *
        FROM mitigations_get_current
        ORDER BY start_time desc;            
    """,

    'vw_mitigations_get_by_id': """
        CREATE OR REPLACE VIEW public.vw_mitigations_get_by_id AS 
        WITH mitigations_get_by_id AS (
        SELECT 
        m.mitigation_id
        ,a.alert_id
            ,a.host_address
        ,a.max_impact_bps
        ,a.max_impact_pps
            ,m.type
        ,m.auto  
        ,m.ip_version
        ,m.degraded
        ,a.start_time
        ,a.stop_time
        ,m.prefix
        FROM mitigations m
        INNER JOIN alerts a ON m.alert_id = a.alert_id
        WHERE 1=1
        )
        SELECT
            m.mitigation_id
        ,m.alert_id
            ,COALESCE(m.host_address, '') AS host_address
        ,COALESCE(m.max_impact_bps, 0) AS max_impact_bps
        ,COALESCE(m.max_impact_pps, 0) AS max_impact_pps
            ,m.type
        ,m.auto  
        ,m.ip_version
        ,COALESCE(m.degraded, '') AS degraded
        ,m.start_time
        ,m.stop_time
        ,m.prefix
        FROM mitigations_get_by_id m;           
    """,


    'vw_mitigations_get_active': """
        CREATE OR REPLACE VIEW public.vw_mitigations_get_active AS 
        WITH mitigations_get_active AS (
        SELECT 
            m.mitigation_id, 
            m.name,
            m.type,
            a.start_time,
            a.stop_time,
            a.host_address,
            a.mps as mps,
            a.pps as pps
        FROM mitigations m
        INNER JOIN vw_alerts a ON m.alert_id = a.alert_id
        WHERE 1=1
        )
        SELECT * FROM mitigations_get_active;                
    """,

    'vw_mitigations_get_traffic_data': """
        CREATE OR REPLACE VIEW public.vw_mitigations_get_traffic_data AS 
        WITH mitigations_get_traffic_data AS (
        SELECT 
            m.mitigation_id,
            a.mo_gid,
            a.start_time AS time,
            max(max_impact_bps) / 1000000 AS pass_mbps,
            COALESCE(max(threshold), 0) / 1000000 AS drop_mbps
        FROM alerts a
        INNER JOIN mitigations m ON m.alert_id = a.alert_id
        WHERE 1=1
        GROUP BY a.start_time, a.mo_gid, m.mitigation_id
        )
        SELECT
            a.mitigation_id
        ,a.mo_gid
        ,a.time
        ,coalesce(a.pass_mbps, 0) as pass_mbps
        ,coalesce(a.drop_mbps, 0) as drop_mbps
        FROM mitigations_get_traffic_data a;              
    """

}

# Views de Cliente
CUSTOMER_VIEWS = {
    'vw_customer_alerts': """
        CREATE OR REPLACE VIEW public.vw_customer_alerts AS 
        WITH cte_alerts_amount AS (
        select 
            date_part('year', start_time) as nYear
            ,date_part('month', start_time) as nMonth
            ,date_part('day', start_time) as nDay
            ,date_part('week', start_time) as nWeek
            ,alerts.mo_gid 
            ,alerts.mo_gid as idMogid
            ,count(distinct alerts.alert_id) as nAmountAlerts
            ,alerts.host_address 
        from alerts 
        group by
            date_part('year', start_time)
            ,date_part('month', start_time)
            ,date_part('day', start_time)
            ,date_part('week', start_time)
            ,alerts.mo_gid
            ,alerts.host_address 
        ),cte_alerts_hosts AS (
        select 
            date_part('year', start_time) as nYear
            ,date_part('month', start_time) as nMonth
            ,date_part('day', start_time) as nDay
            ,date_part('week', start_time) as nWeek
            ,alerts.mo_gid 
            ,alerts.mo_gid as idMogid
            ,alerts.host_address 
        from alerts 
        group by
            date_part('year', start_time)
            ,date_part('month', start_time)
            ,date_part('day', start_time)
            ,date_part('week', start_time)
            ,alerts.mo_gid
            ,alerts.host_address 
        )
        select
            aa.idMogid 	
            ,mo.name
            ,aa.host_address
            ,aa.nAmountAlerts	
            ,aa.nYear
            ,aa.nmonth 
            ,aa.nday
            ,aa.nweek 
            ,array_to_string( array_agg(aa.host_address), '; ') as hosts_address
        from managedobjects mo
        LEFT join cte_alerts_amount aa
            on aa.idMogid = mo.gid
        LEFT join cte_alerts_hosts ah
            on ah.idMogid = aa.idMogid
            and ah.nyear = aa.nyear
            and ah.nmonth = aa.nmonth
            and ah.nday = aa.nday
            and ah.nweek = aa.nweek
            and aa.host_address is not null
        group by
            aa.idMogid 	
            ,mo.name
            ,aa.host_address
            ,aa.nAmountAlerts	
            ,aa.nYear
            ,aa.nmonth 
            ,aa.nday
            ,aa.nweek;
    """,
    
    'vw_customer_mitigations': """
        CREATE OR REPLACE VIEW public.vw_customer_mitigations AS 
        WITH cte_mitigations_amount AS (
        select 
            date_part('year', a.start_time) as nYear
            ,date_part('month', a.start_time) as nMonth
            ,date_part('day', a.start_time) as nDay
            ,date_part('week', a.start_time) as nWeek
            ,a.mo_gid 
            ,a.mo_gid as idMogid
            ,count(distinct m.mitigation_id ) as nAmountMitigations 
        from mitigations m
        inner join alerts a on a.alert_id = m.alert_id 
        group by
            date_part('year', a.start_time)
            ,date_part('month', a.start_time)
            ,date_part('day', a.start_time)
            ,date_part('week', a.start_time)
            ,a.mo_gid
        )
        select * from cte_Mitigations_amount;
    """,

    'vw_customer_dashboard': """
        CREATE OR REPLACE VIEW public.vw_customer_dashboard
        AS WITH cte_customer_dashboard AS (
                SELECT c2.idcompany,
                    c2.namecompany,
                    c.idcustomer,
                    c.namecustomer,
                    ca.idmogid,
                    ca.name,
                    ca.host_address,
                    COALESCE(ca.namountalerts, 0::bigint) AS namountalerts,
                    COALESCE(cm.namountmitigations, 0::bigint) AS namountmitigations,
                    ca.nyear,
                    ca.nmonth,
                    ca.nday,
                    ca.nweek,
                    ca.hosts_address
                FROM managedobjects mo
                    LEFT JOIN vw_customer_alerts ca ON ca.idmogid::text = mo.gid::text
                    LEFT JOIN vw_customer_mitigations cm ON cm.idmogid::text = ca.idmogid::text AND cm.nyear = ca.nyear AND cm.nmonth = ca.nmonth AND cm.nday = ca.nday AND cm.nweek = ca.nweek
                    LEFT JOIN customer_managed_objects cmo ON cmo.idmogid::text = mo.gid::text AND cmo.active IS TRUE
                    LEFT JOIN customers c ON c.idcustomer = cmo.idcustomer AND c.active IS TRUE
                    LEFT JOIN companys c2 ON c2.idcompany = c.idcompany AND c2.active IS TRUE
                WHERE 1 = 1
                )
        SELECT COALESCE(cte_customer_dashboard.idcompany, 0) AS idcompany,
            COALESCE(cte_customer_dashboard.namecompany, 'N/A'::character varying) AS namecompany,
            COALESCE(cte_customer_dashboard.idcustomer, 0) AS idcustomer,
            COALESCE(cte_customer_dashboard.namecustomer, 'N/A'::character varying) AS namecustomer,
            cte_customer_dashboard.idmogid,
            cte_customer_dashboard.name,
            COALESCE(cte_customer_dashboard.host_address, 'N/A'::character varying) AS host_address,
            COALESCE(cte_customer_dashboard.namountalerts, 0::bigint) AS namountalerts,
            COALESCE(cte_customer_dashboard.namountmitigations, 0::bigint) AS namountmitigations,
            cte_customer_dashboard.nyear,
            cte_customer_dashboard.nmonth,
            cte_customer_dashboard.nday,
            cte_customer_dashboard.nweek,
            COALESCE(cte_customer_dashboard.hosts_address, 'N/A'::text) AS hosts_address
        FROM cte_customer_dashboard;
    """,

    'vw_customer_alerts_top_month': """
        CREATE OR REPLACE VIEW public.vw_customer_alerts_top_month AS
        WITH cte_customer_alerts_top_month AS (
        SELECT 
        ROW_NUMBER() OVER ( PARTITION BY nyear,nmonth ORDER BY namountalerts desc ) as RowId
        ,* 
        FROM (
        SELECT 
            idmogid 
            ,name as NameMoGid
            ,nyear
            ,nmonth
            ,sum(namountalerts) as namountalerts
        FROM vw_customer_alerts
        GROUP BY 
            idmogid 
            ,name
            ,nyear
            ,nmonth
        ) AS Top
        )
        SELECT
            RowId
            ,idmogid 
            ,NameMoGid
            ,nyear
            ,nmonth
            ,namountalerts
        FROM cte_customer_alerts_top_month;
    """,


    'vw_customer_alerts_graph': """
        CREATE OR REPLACE VIEW public.vw_customer_alerts_graph AS
        WITH cte_customer_alerts_all_month AS (
            SELECT 
                nyear,
                nmonth,
                nday,
                '0' as idmogid,
                'Total Alerts' as name,
                SUM(namountalerts) as namountalerts
            FROM vw_customer_dashboard
            GROUP BY nyear, nmonth, nday
        ),
        cte_customer_alerts_mogid_month AS (
        SELECT 
            nyear,
            nmonth,
            nday,
            idmogid,
            name,
            SUM(namountalerts) as namountalerts
        FROM vw_customer_dashboard
        GROUP BY nyear, nmonth, nday, idmogid, name
        )
        ,cte_result as (
        SELECT * FROM cte_customer_alerts_all_month
        UNION
        SELECT * FROM cte_customer_alerts_mogid_month
        )
        select 
            COALESCE(RowId, 0) AS RowId
            ,a.nyear
            ,a.nmonth
            ,a.nday
            ,a.idmogid
            ,a.name
            ,a.namountalerts
            ,CASE WHEN COALESCE(RowId, 0) = 0 THEN  a.namountalerts ELSE b.namountalerts END as nAmountAlertsMonth
            ,CAST(((a.namountalerts / b.namountalerts) * 100) as numeric(5,2)) as nPercAlerts
        from cte_result a
            LEFT JOIN vw_customer_alerts_top_month b 
            on b.idmogid = a.idmogid
                and b.nyear = a.nyear
                and b.nmonth = a.nmonth  
        where 1=1;
    """,


    'vw_customer_dashboard_list': """
        CREATE OR REPLACE VIEW public.vw_customer_dashboard_list AS
        WITH cte_customer_total_month AS(
        SELECT 
                nyear,
            nmonth,
            0 AS nday,
            0 AS nweek,
            COALESCE(idcompany, 0) AS idcompany,
            COALESCE(namecompany, 'N/A') AS namecompany,
            COALESCE(idcustomer, 0) AS idcustomer,
            COALESCE(namecustomer, 'N/A') AS namecustomer,
            idmogid,
            name,          
            SUM(COALESCE(namountalerts, 0)) as namountalerts,
            SUM(COALESCE(namountmitigations, 0)) as namountmitigations    
        FROM vw_customer_dashboard
        GROUP BY 
                nyear,
            nmonth,    
            COALESCE(idcompany, 0),
            COALESCE(namecompany, 'N/A'),
            COALESCE(idcustomer, 0),
            COALESCE(namecustomer, 'N/A'),
            idmogid,
            name
        ),cte_customer_hosts AS (
        SELECT 
            nyear,
        nmonth,
        idmogid,
            hosts_address
        FROM vw_customer_dashboard 
        GROUP BY 
            nyear,
        nmonth,
        idmogid,
            hosts_address
        ),cte_customer_zero AS (
        SELECT
        aa.idcompany
        ,aa.namecompany
        ,aa.idcustomer
        ,aa.namecustomer
        ,aa.idmogid
        ,aa.name
        ,aa.namountalerts
        ,aa.namountmitigations
        ,aa.nyear
        ,aa.nmonth
        ,aa.nday
        ,aa.nweek
        ,array_to_string(array_agg(DISTINCT bb.hosts_address), '; ') as hosts_address
        FROM cte_customer_total_month aa
        LEFT JOIN cte_customer_hosts bb 
            on aa.idmogid = bb.idmogid
        AND aa.nyear = bb.nyear
        AND aa.nmonth = bb.nmonth
        GROUP BY
            aa.idcompany
        ,aa.namecompany
        ,aa.idcustomer
        ,aa.namecustomer
        ,aa.idmogid
        ,aa.name
        ,aa.namountalerts
        ,aa.namountmitigations
        ,aa.nyear
        ,aa.nmonth
        ,aa.nday
        ,aa.nweek
        ),cte_customer_result AS (
        SELECT 
            idcompany,
            namecompany,
            idcustomer,
            namecustomer,
            idmogid,
            name,
            '' as host_address,
            namountalerts,
            namountmitigations,
            nyear,
            nmonth,
            nday,
            nweek,
            hosts_address
        FROM cte_customer_zero aa
        UNION
        SELECT 
            COALESCE(idcompany, 0) AS idcompany,
            COALESCE(namecompany, 'N/A') AS namecompany,
            COALESCE(idcustomer, 0) AS idcustomer,
            COALESCE(namecustomer, 'N/A') AS namecustomer,
            idmogid,
            name,
            COALESCE(host_address, 'N/A') AS host_address,
            COALESCE(namountalerts, 0) as namountalerts,
            COALESCE(namountmitigations, 0) as namountmitigations,
            nyear,
            nmonth,
            nday,
            nweek,
            COALESCE(hosts_address, 'N/A') AS hosts_address
        FROM vw_customer_dashboard
        )
        SELECT 
        idcompany,
        namecompany,
        idcustomer,
        namecustomer,
        idmogid,
        name,
        host_address,
        namountalerts,
        namountmitigations,
        nyear,
        nmonth,
        nday,
        nweek,
        hosts_address
        FROM cte_customer_result
        WHERE 1=1;
    """

}

# Collection of all SQL scripts
SQL_SCRIPTS = {
    'basic_views': BASIC_VIEWS,
    'alert_views': ALERT_VIEWS,
    'mitigation_views': MITIGATION_VIEWS,
    'customer_views': CUSTOMER_VIEWS
}

def execute_scripts(db_connection) -> None:
    """
    Executa todos os scripts SQL na ordem correta.
    
    Args:
        db_connection: DatabaseConnection instance
    """
    # Define a ordem de execução
    execution_order = [
        'basic_views',
        'alert_views',
        'mitigation_views',
        'customer_views'
    ]
    
    for script_type in execution_order:
        if script_type in SQL_SCRIPTS:
            scripts = SQL_SCRIPTS[script_type]
            for script_name, script in scripts.items():
                try:
                    db_connection.execute_query(script)
                    db_connection.logger.info(
                        f"Successfully executed {script_type} script: {script_name}"
                    )
                except Exception as e:
                    error_msg = f"Error executing {script_type} script {script_name}: {str(e)}"
                    db_connection.logger.error(error_msg)
                    if script_type in ['indices', 'foreign_keys']:
                        db_connection.logger.warning(
                            f"Continuing despite error in {script_type}"
                        )
                    else:
                        raise Exception(error_msg)