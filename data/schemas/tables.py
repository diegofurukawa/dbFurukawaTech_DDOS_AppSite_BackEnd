from typing import Optional

USERS_SCHEMA = """
CREATE TABLE IF NOT EXISTS public.users (
    idUser serial4 NOT NULL,
    email VARCHAR(255) UNIQUE NOT NULL,
    nameUser VARCHAR(255) NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    company VARCHAR(255),
    role VARCHAR(50) DEFAULT 'user',
    active BOOLEAN DEFAULT true,
    createdAt TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updatedAt TIMESTAMP,
    lastLogin TIMESTAMP,
    refresh_token VARCHAR(255),
    CONSTRAINT users_email_key UNIQUE (email),
    CONSTRAINT users_pkey PRIMARY KEY (idUser)
)
"""

ACCESS_REQUESTS_SCHEMA = """
CREATE TABLE IF NOT EXISTS public.access_requests (
    idAccessRequest serial4 NOT NULL,
    email varchar(255) NOT NULL,
    name varchar(255) NOT NULL,
    company varchar(255) NOT NULL,
    reason text NOT NULL,
    status varchar(50) DEFAULT 'pending'::character varying NULL,
    created_at timestamptz DEFAULT CURRENT_TIMESTAMP NULL,
    processed_at timestamptz NULL,
    processed_by int4 NULL,
    CONSTRAINT access_requests_pkey PRIMARY KEY (idAccessRequest)
)
"""

COMPANIES_SCHEMA = """
CREATE TABLE IF NOT EXISTS public.companys (
    idCompany serial4 NOT NULL,
    nameCompany VARCHAR(255) UNIQUE NOT NULL,
    address VARCHAR(255) NULL,
    emailContact VARCHAR(255) NULL,
    phoneNumberContact VARCHAR(255) NULL,
    active BOOLEAN DEFAULT true,
    createdAt TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updatedAt TIMESTAMP,
    CONSTRAINT company_pkey PRIMARY KEY (idCompany)
)
"""

CUSTOMERS_SCHEMA = """
CREATE TABLE IF NOT EXISTS public.customers (
    idCustomer serial4 NOT NULL,
    idCompany serial4 NOT NULL,
    nameCustomer VARCHAR(255) UNIQUE NOT NULL,
    address VARCHAR(255) NULL,
    emailContact VARCHAR(255) NULL,
    phoneNumberContact VARCHAR(255) NULL,
    active BOOLEAN DEFAULT true,
    createdAt TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updatedAt TIMESTAMP,
    CONSTRAINT company_customer_pkey PRIMARY KEY (idCustomer, idCompany)
)
"""

CUSTOMER_MO_SCHEMA = """
CREATE TABLE IF NOT EXISTS public.customer_managed_objects (
    idMogid VARCHAR(255) PRIMARY KEY,
    idCustomer serial4 NOT NULL,
    active BOOLEAN DEFAULT true,
    createdAt TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updatedAt TIMESTAMP,
    FOREIGN KEY (idMogid) REFERENCES managedobjects(id)
)
"""

TABLE_SCHEMAS = {
    'companys': COMPANIES_SCHEMA,
    'users': USERS_SCHEMA,
    'access_requests': ACCESS_REQUESTS_SCHEMA,    
    'customers': CUSTOMERS_SCHEMA,
    'customer_managed_objects': CUSTOMER_MO_SCHEMA
}

def execute_tables(db_connection) -> None:
    execution_order = [
        'companys',
        'users',
        'customers', 
        'access_requests',
        'customer_managed_objects'
    ]
    
    for table_name in execution_order:
        if table_name in TABLE_SCHEMAS:
            try:
                script = TABLE_SCHEMAS[table_name]
                db_connection.execute_query(script, fetch_results=False)
                db_connection.logger.info(
                    f"Successfully created/verified table: {table_name}"
                )
            except Exception as e:
                error_msg = f"Error creating table {table_name}: {str(e)}"
                db_connection.logger.error(error_msg)
                raise Exception(error_msg)
        else:
            db_connection.logger.warning(f"Schema not found for table: {table_name}")