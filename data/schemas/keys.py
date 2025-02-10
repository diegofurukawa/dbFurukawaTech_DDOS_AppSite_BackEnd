# keys.py
"""
Database Keys and Indices

Define os índices e chaves estrangeiras do sistema.
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
        FOREIGN KEY (processed_by) REFERENCES public.users(idUser);
    """,
    'customer_mo_refs': """
        ALTER TABLE IF EXISTS public.customer_managed_objects
        DROP CONSTRAINT IF EXISTS customer_mo_mogid_fkey;
                
        ALTER TABLE IF EXISTS public.customer_managed_objects
        ADD CONSTRAINT customer_mo_mogid_fkey
        FOREIGN KEY (idMogid) REFERENCES managedobjects(id);
    """
}

# Collection of all SQL scripts
SQL_SCRIPTS = {
    'indices': INDICES,
    'foreign_keys': FOREIGN_KEYS
}

def execute_keys(db_connection) -> None:
    """
    Executa a criação dos índices e chaves estrangeiras.
    Continua mesmo se houver erros, pois eles podem ocorrer se as constraints
    já existirem.
    
    Args:
        db_connection: DatabaseConnection instance
    """
    # Define a ordem de execução
    execution_order = [
        'indices',    # Índices primeiro para otimizar as foreign keys
        'foreign_keys'
    ]
    
    for script_type in execution_order:
        if script_type in SQL_SCRIPTS:
            scripts = SQL_SCRIPTS[script_type]
            for script_name, script in scripts.items():
                try:
                    db_connection.execute_query(script)
                    db_connection.logger.info(
                        f"Successfully executed {script_type}: {script_name}"
                    )
                except Exception as e:
                    # Apenas loga o erro mas não interrompe a execução
                    error_msg = f"Error executing {script_type} {script_name}: {str(e)}"
                    db_connection.logger.warning(error_msg)