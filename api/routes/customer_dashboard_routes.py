from fastapi import APIRouter, HTTPException, Query
from typing import Optional
from datetime import datetime
from data.database import DatabaseConnection
from utils.log import create_logger
from utils.auth import get_current_user
from ..models.alert_model import PaginatedResponse, PaginationParams
from ..models.customer_dashboard_model import CustomerDashboardResponse

router = APIRouter(prefix="/api/customer-dashboard", tags=["Customer Dashboard"])
logger = create_logger("customer_dashboard_routes")

class CustomerDashboardAPI:
    def __init__(self):
        self.logger = logger.getChild(self.__class__.__name__)
        self.db = DatabaseConnection()
        self.db.connect()

    async def get_dashboard_data(
        self,
        nyear: int = Query(..., description="Ano"),
        nmonth: int = Query(..., description="Mês"),
        nday: Optional[int] = Query(None, description="Dia (opcional)"),
        page: int = Query(1, ge=1, description="Número da página"),
        page_size: int = Query(10, ge=1, le=100, description="Itens por página")
    ) -> PaginatedResponse[CustomerDashboardResponse]:
        try:
            params = PaginationParams(page=page, page_size=page_size)
            
            # Base da query usando a view
            where_conditions = ["nyear = %s AND nmonth = %s"]
            query_params = [nyear, nmonth]
            
            # Adiciona filtro por dia se fornecido
            if nday is not None:
                where_conditions.append("nday = %s")
                query_params.append(nday)
            
            where_clause = " AND ".join(where_conditions)
            
            # Conta total de registros
            count_query = f"""
                SELECT COUNT(*)
                FROM vw_customer_dashboard
                WHERE {where_clause}
            """
            
            count_result = self.db.execute_query(count_query, query_params)
            total_records = count_result[0][0] if count_result else 0
            
            # Query principal
            query = f"""
                SELECT 
                    COALESCE(idcompany, 0) AS idcompany
                    ,COALESCE(namecompany, 'N/A') AS namecompany
                    ,COALESCE(idcustomer, 0) AS idcustomer
                    ,COALESCE(namecustomer, 'N/A') AS namecustomer
                    ,idmogid
                    ,name
                    ,COALESCE(host_address, 'N/A') AS host_address
                    ,namountalerts
                    ,namountmitigations
                    ,nyear
                    ,nmonth
                    ,nday
                    ,nweek
                    ,COALESCE(hosts_address, 'N/A') AS hosts_address
                FROM vw_customer_dashboard
                WHERE {where_clause}
                ORDER BY namecompany, namecustomer, name
                LIMIT %s OFFSET %s
            """
            
            final_params = tuple(query_params + [params.page_size, params.offset])
            result = self.db.execute_query(query, final_params)
            
            # Processa resultados
            dashboard_items = []
            columns = [
                'idcompany', 'namecompany', 'idcustomer', 'namecustomer',
                'idmogid', 'name', 'host_address', 'namountalerts',
                'namountmitigations', 'nyear', 'nmonth', 'nday', 'nweek',
                'hosts_address'
            ]
            
            for row in result:
                item_dict = dict(zip(columns, row))
                # Converte tipos conforme necessário
                item_dict['namountalerts'] = int(item_dict['namountalerts']) if item_dict['namountalerts'] is not None else 0
                item_dict['namountmitigations'] = int(item_dict['namountmitigations']) if item_dict['namountmitigations'] is not None else 0
                item_dict['nyear'] = int(item_dict['nyear']) if item_dict['nyear'] is not None else 0
                item_dict['nmonth'] = int(item_dict['nmonth']) if item_dict['nmonth'] is not None else 0
                item_dict['nday'] = int(item_dict['nday']) if item_dict['nday'] is not None else 0
                item_dict['nweek'] = int(item_dict['nweek']) if item_dict['nweek'] is not None else 0
                
                dashboard_items.append(CustomerDashboardResponse(**item_dict))
            
            return PaginatedResponse.create(
                items=dashboard_items,
                total=total_records,
                params=params
            )
            
        except Exception as e:
            self.logger.error(f"Error fetching dashboard data: {str(e)}")
            raise HTTPException(
                status_code=500,
                detail=f"Failed to fetch dashboard data: {str(e)}"
            )

# Initialize API handler
dashboard_api = CustomerDashboardAPI()

# Route definition
@router.get("", response_model=PaginatedResponse[CustomerDashboardResponse])
async def get_dashboard_data(
    nyear: int = Query(..., ge=2000, le=2100, description="Ano"),
    nmonth: int = Query(..., ge=1, le=12, description="Mês"),
    nday: Optional[int] = Query(None, ge=1, le=31, description="Dia (opcional)"),
    page: int = Query(1, ge=1, description="Número da página"),
    page_size: int = Query(10, ge=1, le=100, description="Itens por página")
):
    """
    Obtém dados do dashboard do cliente com paginação
    - Filtra por ano e mês (obrigatórios)
    - Filtra por dia (opcional)
    - Suporta paginação
    """
    return await dashboard_api.get_dashboard_data(nyear, nmonth, nday, page, page_size)