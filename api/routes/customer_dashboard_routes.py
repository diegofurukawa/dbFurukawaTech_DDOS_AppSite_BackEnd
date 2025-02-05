from fastapi import APIRouter, HTTPException, Query
from typing import List, Optional
from datetime import datetime
from data.database import DatabaseConnection
from utils.log import create_logger
from utils.auth import get_current_user
from ..models.alert_model import PaginatedResponse, PaginationParams
from ..models.customer_dashboard_model import (
    CustomerDashboardStatsResponse,
    CustomerDashboardGraphPoint,
    CustomerListResponse
)

router = APIRouter(prefix="/api/customer-dashboard", tags=["Customer Dashboard"])
logger = create_logger("customer_dashboard_routes")

class CustomerDashboardAPI:
    def __init__(self):
        self.logger = logger.getChild(self.__class__.__name__)
        self.db = DatabaseConnection()
        self.db.connect()

    async def get_alerts_stats(
        self,
        mogid: Optional[str] = None,
        nyear: Optional[int] = None,
        nmonth: Optional[int] = None,
        nday: Optional[int] = None
    ) -> CustomerDashboardStatsResponse:
        try:
            # Base query
            query = """
                SELECT 
                    idcompany,
                    namecompany,
                    idcustomer,
                    namecustomer,
                    idmogid,
                    name,
                    SUM(namountalerts) as namountalerts,
                    hosts_address
                FROM vw_customer_dashboard 
                WHERE 1=1
            """
            params = []

            # Add filters
            if mogid:
                query += " AND idmogid = %s"
                params.append(mogid)
            if nyear:
                query += " AND nyear = %s"
                params.append(nyear)
            if nmonth:
                query += " AND nmonth = %s"
                params.append(nmonth)
            if nday:
                query += " AND nday = %s"
                params.append(nday)

            # Add grouping and ordering
            query += """
                GROUP BY 
                    idcompany,
                    namecompany,
                    idcustomer,
                    namecustomer,
                    idmogid,
                    name,
                    hosts_address
                ORDER BY SUM(namountalerts) DESC
                LIMIT 1
            """

            result = self.db.execute_query(query, tuple(params))
            
            if not result:
                return CustomerDashboardStatsResponse(
                    idcompany=0,
                    namecompany="N/A",
                    idcustomer=0,
                    namecustomer="N/A",
                    idmogid="0",
                    name="N/A",
                    namountalerts=0,
                    hosts_address="N/A"
                )

            columns = [
                'idcompany', 'namecompany', 'idcustomer', 'namecustomer',
                'idmogid', 'name', 'namountalerts', 'hosts_address'
            ]
            
            return CustomerDashboardStatsResponse(**dict(zip(columns, result[0])))

        except Exception as e:
            self.logger.error(f"Error fetching alerts stats: {str(e)}")
            raise HTTPException(
                status_code=500,
                detail=f"Failed to fetch alerts stats: {str(e)}"
            )

    async def get_mitigations_stats(
        self,
        mogid: Optional[str] = None,
        nyear: Optional[int] = None,
        nmonth: Optional[int] = None,
        nday: Optional[int] = None
    ) -> CustomerDashboardStatsResponse:
        try:
            # Base query
            query = """
                SELECT 
                    idcompany,
                    namecompany,
                    idcustomer,
                    namecustomer,
                    idmogid,
                    name,
                    SUM(namountmitigations) as namountmitigations,
                    hosts_address
                FROM vw_customer_dashboard 
                WHERE 1=1
            """
            params = []

            # Add filters
            if mogid:
                query += " AND idmogid = %s"
                params.append(mogid)
            if nyear:
                query += " AND nyear = %s"
                params.append(nyear)
            if nmonth:
                query += " AND nmonth = %s"
                params.append(nmonth)
            if nday:
                query += " AND nday = %s"
                params.append(nday)

            # Add grouping and ordering
            query += """
                GROUP BY 
                    idcompany,
                    namecompany,
                    idcustomer,
                    namecustomer,
                    idmogid,
                    name,
                    hosts_address
                ORDER BY SUM(namountmitigations) DESC
                LIMIT 1
            """

            result = self.db.execute_query(query, tuple(params))
            
            if not result:
                return CustomerDashboardStatsResponse(
                    idcompany=0,
                    namecompany="N/A",
                    idcustomer=0,
                    namecustomer="N/A",
                    idmogid="0",
                    name="N/A",
                    namountmitigations=0,
                    hosts_address="N/A"
                )

            columns = [
                'idcompany', 'namecompany', 'idcustomer', 'namecustomer',
                'idmogid', 'name', 'namountmitigations', 'hosts_address'
            ]
            
            return CustomerDashboardStatsResponse(**dict(zip(columns, result[0])))

        except Exception as e:
            self.logger.error(f"Error fetching mitigations stats: {str(e)}")
            raise HTTPException(
                status_code=500,
                detail=f"Failed to fetch mitigations stats: {str(e)}"
            )

    async def get_graph_alerts(
        self,
        nyear: Optional[int] = None,
        nmonth: Optional[int] = None,
        mogid: Optional[str] = None
    ) -> List[CustomerDashboardGraphPoint]:
        try:
            # Use current year/month if not provided
            current_date = datetime.now()
            if not nyear:
                nyear = current_date.year
            if not nmonth:
                nmonth = current_date.month

            query = """
                WITH cte_customer_alerts_all_month AS (
                    SELECT 
                        nyear,
                        nmonth,
                        nday,
                        '0' as idmogid,
                        'Total Alerts' as name,
                        SUM(namountalerts) as namountalerts
                    FROM vw_customer_dashboard
                    WHERE nyear = %s AND nmonth = %s
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
                    WHERE nyear = %s AND nmonth = %s
            """
            params = [nyear, nmonth, nyear, nmonth]

            # Add mogid filter if provided
            if mogid:
                query += " AND idmogid = %s"
                params.append(mogid)

            query += """
                GROUP BY nyear, nmonth, nday, idmogid, name
                )
                ,cte_result as (
                SELECT 
                    1 as RowId
                ,* 
                FROM cte_customer_alerts_all_month
                UNION
                SELECT 
                    ROW_NUMBER() OVER ( PARTITION BY nyear,nmonth, nday ORDER BY namountalerts desc ) as RowId
                ,* 
                FROM cte_customer_alerts_mogid_month
                )
                select
                	nyear
                    ,nmonth
                    ,nday
                    ,idmogid
                    ,name
                    ,namountalerts
                from cte_result
                where rowid <= 5
            """

            result = self.db.execute_query(query, tuple(params))
            
            if not result:
                return []

            columns = ['nyear', 'nmonth', 'nday', 'idmogid', 'name', 'namountalerts']
            return [
                CustomerDashboardGraphPoint(**dict(zip(columns, row)))
                for row in result
            ]

        except Exception as e:
            self.logger.error(f"Error fetching graph data: {str(e)}")
            raise HTTPException(
                status_code=500,
                detail=f"Failed to fetch graph data: {str(e)}"
            )

    async def get_dashboard_data(
        self,
        nyear: int = Query(..., description="Ano"),
        nmonth: int = Query(..., description="Mês"),
        nday: Optional[int] = Query(None, description="Dia (opcional)"),
        page: int = Query(1, ge=1, description="Número da página"),
        page_size: int = Query(10, ge=1, le=100, description="Itens por página")
    ) -> PaginatedResponse[CustomerListResponse]:
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
                
                dashboard_items.append(CustomerListResponse(**item_dict))
            
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

# Route definitions
@router.get("/alerts-stats", response_model=CustomerDashboardStatsResponse)
async def get_alerts_stats(
    mogid: Optional[str] = None,
    nyear: Optional[int] = Query(None, ge=2000, le=2100),
    nmonth: Optional[int] = Query(None, ge=1, le=12),
    nday: Optional[int] = Query(None, ge=1, le=31)
):
    """
    Get alerts statistics for the dashboard
    - Optional filters by managed object ID, year, month, and day
    """
    return await dashboard_api.get_alerts_stats(mogid, nyear, nmonth, nday)

@router.get("/mitigations-stats", response_model=CustomerDashboardStatsResponse)
async def get_mitigations_stats(
    mogid: Optional[str] = None,
    nyear: Optional[int] = Query(None, ge=2000, le=2100),
    nmonth: Optional[int] = Query(None, ge=1, le=12),
    nday: Optional[int] = Query(None, ge=1, le=31)
):
    """
    Get mitigations statistics for the dashboard
    - Optional filters by managed object ID, year, month, and day
    """
    return await dashboard_api.get_mitigations_stats(mogid, nyear, nmonth, nday)

@router.get("/graph-alerts", response_model=List[CustomerDashboardGraphPoint])
async def get_graph_alerts(
    nyear: Optional[int] = Query(None, ge=2000, le=2100),
    nmonth: Optional[int] = Query(None, ge=1, le=12),
    mogid: Optional[str] = None
):
    """
    Get alerts data for graphing
    - Optional filters by year, month, and managed object ID
    - Returns both total alerts and per-object alerts
    """
    return await dashboard_api.get_graph_alerts(nyear, nmonth, mogid)

# Route definition
@router.get("/alerts-list", response_model=PaginatedResponse[CustomerListResponse])
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