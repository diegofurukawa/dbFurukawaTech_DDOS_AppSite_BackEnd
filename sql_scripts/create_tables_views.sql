--DROP TABLE if exists public.alerts CASCADE;
--DROP TABLE if exists public.mitigations CASCADE;
--DROP TABLE if exists public.access_requests CASCADE;
--DROP TABLE if exists public.managedobjects CASCADE;
--DROP TABLE if exists public.users CASCADE;

CREATE TABLE IF NOT EXISTS public.alerts (
	alert_id varchar(255) NOT NULL,
	alert_name varchar(255) NULL,
	alert_type varchar(255) NULL,
	start_time timestamp NULL,
	stop_time timestamp NULL,
	duration int4 NULL,
	max_impact_bps int8 NULL,
	max_impact_pps int8 NULL,
	confidence int4 NULL,
	ongoing bool NULL,
	importance varchar(255) NULL,
	mo_gid varchar(255) NULL,
	mo_name varchar(255) NULL,
	mo_misusesig varchar(255) NULL,
	host_address varchar(255) NULL,
	ip_version varchar(255) NULL,
	isfastdetected bool NULL,
	direction varchar(255) NULL,
	device_gid varchar(255) NULL,
	device_name varchar(255) NULL,
	threshold float8 NULL,
	severity_pct float8 NULL,
	unit varchar(255) NULL,
	max_impact_boundary varchar(255) NULL,
	mo_importance varchar(255) NULL,
	misusetypes varchar(255) NULL,
	mimpact_bps varchar(255) NULL,
	updated_at timestamp NULL,
	inserted_at timestamp DEFAULT CURRENT_TIMESTAMP NULL,
	country varchar(255) NULL,
	CONSTRAINT alerts_pkey PRIMARY KEY (alert_id)
);


CREATE TABLE IF NOT EXISTS public.mitigations (
	mitigation_id varchar(255) NOT NULL,
	"name" varchar(255) NULL,
	subtype varchar(255) NULL,
	auto bool NULL,
	"type" varchar(255) NULL,
	type_name varchar(255) NULL,
	config_id varchar(255) NULL,
	prefix varchar(255) NULL,
	alert_id varchar(255) NULL,
	degraded varchar(255) NULL,
	user_mitigation varchar(255) NULL,
	is_automitigation bool NULL,
	ip_version int4 NULL,
	flist_gid varchar(255) NULL,
	is_learning bool NULL,
	learning_cancelled bool NULL,
	mo_name varchar(255) NULL,
	mo_gid varchar(255) NULL,
	duration int4 NULL,
	ongoing bool NULL,
	start_time timestamp NULL,
	stop_time timestamp NULL,
	updated_at timestamp NULL,
	inserted_at timestamp DEFAULT CURRENT_TIMESTAMP NULL,
	CONSTRAINT mitigations_pkey PRIMARY KEY (mitigation_id)
);


CREATE TABLE IF NOT EXISTS public.managedobjects (
	id varchar(255) NOT NULL,
	gid varchar(255) NULL,
	"name" varchar(255) NULL,
	description text NULL,
	autodetected bool NULL,
	"match" text NULL,
	intf_boundary text NULL,
	treat_external_as_internal bool NULL,
	num_children int4 NULL,
	scrubber_baselines text NULL,
	automitigation_profiled bool NULL,
	mitigation_automitigation_traffic text NULL,
	automitigation_learned_prefixes bool NULL,
	automitigation_learned_prefixes_mitigate_on_query_failure bool NULL,
	scrub_insight_mo_match text NULL,
	automitigation_tms_enabled bool NULL,
	automitigation_tms_reuse bool NULL,
	automitigation_stop_minutes int4 NULL,
	tiered_blackhole_tms_bps int8 NULL,
	tiered_blackhole_tms_pps int8 NULL,
	blackhole_auto_enabled bool NULL,
	blackhole_auto_stop_minutes int4 NULL,
	blackhole_auto_bgp_session_ipv4 text NULL,
	flowspec_auto_enabled bool NULL,
	flowspec_auto_ruleset text NULL,
	sightline_signaling_auto_enabled bool NULL,
	match_dark bool NULL,
	mitigation_templates_manual_ipv4 text NULL,
	mitigation_templates_manual_ipv6 text NULL,
	mitigation_templates_auto_ipv4 text NULL,
	mitigation_templates_auto_ipv6 text NULL,
	full_match text NULL,
	ip_location_policing_rates text NULL,
	host_detection_shared_set text NULL,
	host_detection_shared_set_custom text NULL,
	match_enabled bool NULL,
	dynamic_match_enabled bool NULL,
	dynamic_match_multitenant_enabled bool NULL,
	profiled_severity_duration int4 NULL,
	profiled_incoming_bps int8 NULL,
	profiled_incoming_pps int8 NULL,
	profiled_outgoing_bps int8 NULL,
	profiled_outgoing_pps int8 NULL,
	profiled_use_snmp bool NULL,
	bandwidth_threshold int8 NULL,
	pps_threshold int8 NULL,
	protocol_threshold int8 NULL,
	host_severity_duration int4 NULL,
	host_chargen_amp_trigger int8 NULL,
	host_chargen_amp_pps_trigger int8 NULL,
	host_chargen_amp_severity int8 NULL,
	host_chargen_amp_pps_severity int8 NULL,
	host_cldap_amp_trigger int8 NULL,
	host_cldap_amp_pps_trigger int8 NULL,
	host_cldap_amp_severity int8 NULL,
	host_cldap_amp_pps_severity int8 NULL,
	host_dns_trigger int8 NULL,
	host_dns_pps_trigger int8 NULL,
	host_dns_severity int8 NULL,
	host_dns_pps_severity int8 NULL,
	host_dns_amp_trigger int8 NULL,
	host_dns_amp_pps_trigger int8 NULL,
	host_dns_amp_severity int8 NULL,
	host_dns_amp_pps_severity int8 NULL,
	host_icmp_trigger int8 NULL,
	host_icmp_pps_trigger int8 NULL,
	host_icmp_severity int8 NULL,
	host_icmp_pps_severity int8 NULL,
	host_ipfrag_trigger int8 NULL,
	host_ipfrag_pps_trigger int8 NULL,
	host_ipfrag_severity int8 NULL,
	host_ipfrag_pps_severity int8 NULL,
	host_ipnull_trigger int8 NULL,
	host_ipnull_pps_trigger int8 NULL,
	host_ipnull_severity int8 NULL,
	host_ipnull_pps_severity int8 NULL,
	host_ippriv_trigger int8 NULL,
	host_ippriv_pps_trigger int8 NULL,
	host_ippriv_severity int8 NULL,
	host_ippriv_pps_severity int8 NULL,
	host_l2tp_amp_trigger int8 NULL,
	host_l2tp_amp_pps_trigger int8 NULL,
	host_l2tp_amp_severity int8 NULL,
	host_l2tp_amp_pps_severity int8 NULL,
	host_mdns_amp_trigger int8 NULL,
	host_mdns_amp_pps_trigger int8 NULL,
	host_mdns_amp_severity int8 NULL,
	host_mdns_amp_pps_severity int8 NULL,
	host_memcached_amp_trigger int8 NULL,
	host_memcached_amp_pps_trigger int8 NULL,
	host_memcached_amp_severity int8 NULL,
	host_memcached_amp_pps_severity int8 NULL,
	host_mssql_amp_trigger int8 NULL,
	host_mssql_amp_pps_trigger int8 NULL,
	host_mssql_amp_severity int8 NULL,
	host_mssql_amp_pps_severity int8 NULL,
	host_netbios_amp_trigger int8 NULL,
	host_netbios_amp_pps_trigger int8 NULL,
	host_netbios_amp_severity int8 NULL,
	host_netbios_amp_pps_severity int8 NULL,
	host_ntp_amp_trigger int8 NULL,
	host_ntp_amp_pps_trigger int8 NULL,
	host_ntp_amp_severity int8 NULL,
	host_ntp_amp_pps_severity int8 NULL,
	host_ripv1_amp_trigger int8 NULL,
	host_ripv1_amp_pps_trigger int8 NULL,
	host_ripv1_amp_severity int8 NULL,
	host_ripv1_amp_pps_severity int8 NULL,
	host_rpcbind_amp_trigger int8 NULL,
	host_rpcbind_amp_pps_trigger int8 NULL,
	host_rpcbind_amp_severity int8 NULL,
	host_rpcbind_amp_pps_severity int8 NULL,
	host_snmp_amp_trigger int8 NULL,
	host_snmp_amp_pps_trigger int8 NULL,
	host_snmp_amp_severity int8 NULL,
	host_snmp_amp_pps_severity int8 NULL,
	host_ssdp_amp_trigger int8 NULL,
	host_ssdp_amp_pps_trigger int8 NULL,
	host_ssdp_amp_severity int8 NULL,
	host_ssdp_amp_pps_severity int8 NULL,
	host_tcpack_trigger int8 NULL,
	host_tcpack_pps_trigger int8 NULL,
	host_tcpack_severity int8 NULL,
	host_tcpack_pps_severity int8 NULL,
	host_tcpnull_trigger int8 NULL,
	host_tcpnull_pps_trigger int8 NULL,
	host_tcpnull_severity int8 NULL,
	host_tcpnull_pps_severity int8 NULL,
	host_tcprst_trigger int8 NULL,
	host_tcprst_pps_trigger int8 NULL,
	host_tcprst_severity int8 NULL,
	host_tcprst_pps_severity int8 NULL,
	host_tcpsyn_trigger int8 NULL,
	host_tcpsyn_pps_trigger int8 NULL,
	host_tcpsyn_severity int8 NULL,
	host_tcpsyn_pps_severity int8 NULL,
	host_tcpsynack_trigger int8 NULL,
	host_tcpsynack_pps_trigger int8 NULL,
	host_tcpsynack_severity int8 NULL,
	host_tcpsynack_pps_severity int8 NULL,
	host_total_trigger int8 NULL,
	host_total_pps_trigger int8 NULL,
	host_total_severity int8 NULL,
	host_total_pps_severity int8 NULL,
	host_udp_trigger int8 NULL,
	host_udp_pps_trigger int8 NULL,
	host_udp_severity int8 NULL,
	host_udp_pps_severity int8 NULL,
	host_user_defined_1_trigger int8 NULL,
	host_user_defined_1_pps_trigger int8 NULL,
	host_user_defined_1_severity int8 NULL,
	host_user_defined_1_pps_severity int8 NULL,
	host_user_defined_2_trigger int8 NULL,
	host_user_defined_2_pps_trigger int8 NULL,
	host_user_defined_2_severity int8 NULL,
	host_user_defined_2_pps_severity int8 NULL,
	host_user_defined_3_trigger int8 NULL,
	host_user_defined_3_pps_trigger int8 NULL,
	host_user_defined_3_severity int8 NULL,
	host_user_defined_3_pps_severity int8 NULL,
	host_user_defined_4_trigger int8 NULL,
	host_user_defined_4_pps_trigger int8 NULL,
	host_user_defined_4_severity int8 NULL,
	host_user_defined_4_pps_severity int8 NULL,
	host_user_defined_5_trigger int8 NULL,
	host_user_defined_5_pps_trigger int8 NULL,
	host_user_defined_5_severity int8 NULL,
	host_user_defined_5_pps_severity int8 NULL,
	network_severity_duration int4 NULL,
	network_detection_percent_incoming float8 NULL,
	network_severity_percent_incoming float8 NULL,
	network_detection_percent_outgoing float8 NULL,
	network_severity_percent_outgoing float8 NULL,
	require_targeted_cs_requests_evaluated bool NULL,
	row_id varchar(255) NULL,
	updated_at timestamp DEFAULT CURRENT_TIMESTAMP NULL,
	inserted_at timestamp DEFAULT CURRENT_TIMESTAMP NULL,
	CONSTRAINT managedobjects_pkey PRIMARY KEY (id)
);

CREATE TABLE IF NOT EXISTS public.users(
  idUser serial4 NOT NULL,
  email VARCHAR(255) UNIQUE NOT NULL,
  nameUser VARCHAR(255) NOT NULL,
  password_hash VARCHAR(255) NOT NULL,
  company VARCHAR(255),
  "role" VARCHAR(50) DEFAULT 'user',
  active BOOLEAN DEFAULT true,
  createdAt TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  updatedAt TIMESTAMP,
  lastLogin TIMESTAMP,
  refresh_token VARCHAR(255),
	CONSTRAINT users_email_key UNIQUE (email),
	CONSTRAINT users_pkey PRIMARY KEY (idUser)
);
CREATE INDEX IF NOT EXISTS idx_users_email ON public.users USING btree (email);


CREATE TABLE IF NOT EXISTS public.access_requests (
	idAccessRequest serial4 NOT NULL,
	email varchar(255) NOT NULL,
	"name" varchar(255) NOT NULL,
	company varchar(255) NOT NULL,
	reason text NOT NULL,
	status varchar(50) DEFAULT 'pending'::character varying NULL,
	created_at timestamptz DEFAULT CURRENT_TIMESTAMP NULL,
	processed_at timestamptz NULL,
	processed_by int4 NULL,
	CONSTRAINT access_requests_pkey PRIMARY KEY (idAccessRequest)
);
CREATE INDEX IF NOT EXISTS idx_access_requests_email ON public.access_requests USING btree (email);
CREATE INDEX IF NOT EXISTS idx_access_requests_status ON public.access_requests USING btree (status);

ALTER TABLE IF EXISTS public.access_requests DROP CONSTRAINT IF EXISTS access_requests_processed_by_fkey;
ALTER TABLE IF EXISTS public.access_requests ADD CONSTRAINT access_requests_processed_by_fkey FOREIGN KEY (processed_by) REFERENCES public.users(idUser);



CREATE TABLE IF NOT EXISTS public.companys(
  idCompany serial4 NOT NULL,
  nameCompany VARCHAR(255) UNIQUE NOT NULL,
  address VARCHAR(255) NULL,
	emailContact VARCHAR(255) NULL,
  phoneNumberContact VARCHAR(255) NULL,
  active BOOLEAN DEFAULT true,
  createdAt TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  updatedAt TIMESTAMP,
	CONSTRAINT company_pkey PRIMARY KEY (idCompany)
);

CREATE TABLE IF NOT EXISTS public.customers(
  idCustomer serial4 NOT NULL
  ,idCompany serial4 NOT NULL
  ,nameCustomer VARCHAR(255) UNIQUE NOT NULL
  ,address VARCHAR(255) NULL
	,emailContact VARCHAR(255) NULL
  ,phoneNumberContact VARCHAR(255) NULL
  ,active BOOLEAN DEFAULT true
  ,createdAt TIMESTAMP DEFAULT CURRENT_TIMESTAMP
  ,updatedAt TIMESTAMP
  ,CONSTRAINT company_customer_pkey PRIMARY KEY (idCustomer, idCompany)
);

--drop table customer_managed_objects
--ALTER TABLE orders DROP CONSTRAINT fk_orders_customers;

CREATE TABLE IF NOT EXISTS public.customer_managed_objects(
		idMogid VARCHAR(255) PRIMARY KEY  -- Chave primária única, pois um MO só pode ter um customer
    ,idCustomer serial4 NOT NULL
    ,active BOOLEAN DEFAULT true
    ,createdAt TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    ,updatedAt TIMESTAMP
    ,FOREIGN KEY (idMogid) REFERENCES managedobjects(id)
    --,FOREIGN KEY (idCustomer) REFERENCES customers(idCustomer)
);

-- CREATE TABLE IF NOT EXISTS public.customers_mo(
--   idCustomer serial4 NOT NULL,
--   idMogid VARCHAR(255) NOT NULL,
--   active BOOLEAN DEFAULT true,
--   createdAt TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
--   updatedAt TIMESTAMP,
--   FOREIGN KEY (idMogid) REFERENCES managedobjects(id),
-- 	CONSTRAINT customer_mo_pkey PRIMARY KEY (idCustomer, idMogid)
-- );


/*

SELECT con.*
FROM pg_catalog.pg_constraint con
INNER JOIN pg_catalog.pg_class rel ON rel.oid = con.conrelid
INNER JOIN pg_catalog.pg_namespace nsp ON nsp.oid = connamespace
WHERE nsp.nspname = 'public'
 AND rel.relname = 'customers';

*/

-- public.vw_datenow source

CREATE OR REPLACE VIEW public.vw_datenow
AS SELECT now() - '03:00:00'::interval AS ddatenow;


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
  
  
  
  
  
  -- public.vw_alert_traffic source

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
  
  
  -- public.vw_amount_alerts source

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
  
  
  
  -- public.vw_amount_alerts_ongoing source

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
  
  
  -- public.vw_calendar_month source

CREATE OR REPLACE VIEW public.vw_calendar_month
AS WITH cte_datenow AS (
         SELECT vw_datenow.ddatenow
           FROM vw_datenow
        ), cte_calendar AS (
         SELECT calendar.ddate
           FROM ( SELECT generate_series(concat(date_part('year'::text, cte_datenow.ddatenow), '-01-01')::timestamp without time zone, concat(date_part('year'::text, cte_datenow.ddatenow), '-12-31')::timestamp without time zone, '1 day'::interval) AS date_series
                   FROM cte_datenow) calendar(ddate)
        )
 SELECT cte_calendar.ddate::date AS ddate
   FROM cte_calendar
  WHERE 1 = 1 AND date_part('month'::text, cte_calendar.ddate) = date_part('month'::text, ( SELECT cte_datenow.ddatenow
           FROM cte_datenow));
           
           
           
-- public.vw_calendar_today source

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
           
           
           
           
           
           
-- public.vw_calendar_year source

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
   FROM cte_calendar
  WHERE 1 = 1;

-- public.vw_mitigation_graphic source

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
  
  
  
  -- public.vw_mitigations_count source

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
WHERE 1=1
	--and a.start_time >= CURRENT_DATE
	--and m.ongoing is true OR a.ongoing is true
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
	--and a.start_time >= CURRENT_DATE
	--and m.ongoing is true OR a.ongoing is true
ORDER BY A.start_time DESC
LIMIT 1
)
SELECT 
	*
FROM mitigations_get_current
ORDER BY start_time desc;


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


-- public.vw_customer_dashboard source

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