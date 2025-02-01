"""
Mitigation Routes Module

Handles all mitigation-related API endpoints with improved logging.
"""

from fastapi import APIRouter, HTTPException, Query
from typing import Dict, List, Optional
from datetime import datetime, timedelta
from data.database import DatabaseConnection
from utils.log import create_logger
from ..models import (
    MitigationBase, 
    MitigationTrafficPoint, 
    MitigationStats,
    PaginatedResponse,
    PaginationParams,
    MitigationByID,
    MitigationTop,
    MitigationCurrent,
    MitigationActive
)

router = APIRouter(prefix="/api/mitigations", tags=["mitigations"])
logger = create_logger("mitigation_routes")

class MitigationAPI:
    def __init__(self):
        self.logger = logger.getChild(self.__class__.__name__)
        self.db = DatabaseConnection()
        self.db.connect()

    async def get_mitigation_stats(self) -> MitigationStats:
        """Retorna estatísticas gerais das mitigações"""
        self.logger.info("Iniciando busca por estatísticas de mitigação")
        try:
            with self.db.connection.cursor() as cursor:
                # Conta mitigações ativas
                cursor.execute("""
                    SELECT COUNT(*) 
                    FROM vw_alerts a
                    INNER JOIN mitigations c ON c.alert_id = a.alert_id
                    WHERE 1=1
                """)
                active = cursor.fetchone()[0]

                # Total de mitigações
                cursor.execute("""
                    SELECT COUNT(*) 
                    FROM vw_alerts a
                    INNER JOIN mitigations c ON c.alert_id = a.alert_id
                    WHERE 1=1
                """)
                total = cursor.fetchone()[0]

                # Tempo médio de resposta (em segundos)
                cursor.execute("""
                    SELECT AVG(EXTRACT(EPOCH FROM (a.stop_time - a.start_time))) 
                    FROM vw_alerts a
                    INNER JOIN mitigations c ON c.alert_id = a.alert_id
                    WHERE a.stop_time IS NOT NULL
                """)
                avg_time = cursor.fetchone()[0] or 0

                # Taxa de sucesso
                cursor.execute("""
                    SELECT COUNT(*) 
                    FROM vw_alerts a
                    INNER JOIN mitigations c ON c.alert_id = a.alert_id
                    WHERE a.stop_time IS NOT NULL AND degraded = 'false'
                """)
                success = cursor.fetchone()[0]
                success_rate = (success / total * 100) if total > 0 else 100

                return MitigationStats(
                    active_mitigations=active,
                    total_mitigated=total,
                    avg_response_time=round(avg_time / 60, 1),
                    success_rate=round(success_rate, 1)
                )

        except Exception as e:
            self.logger.error(f"Erro ao obter estatísticas de mitigação: {e}", exc_info=True)
            raise HTTPException(status_code=500, detail=str(e))
    
    async def get_mitigation_by_id(self, mitigation_id: str) -> MitigationByID:
        """Obtém uma mitigação específica por ID"""
        self.logger.debug(f"Fetching mitigation with ID: {mitigation_id}")
        try:
            query = """
                SELECT mitigation_id, alert_id, host_address, max_impact_bps,
                    max_impact_pps, type, auto, ip_version, degraded,
                    start_time, stop_time, prefix
                FROM vw_mitigations_get_by_id
                WHERE mitigation_id = %s
            """
            self.logger.debug(f"Executando query com ID {mitigation_id}")
            
            # Executa a query usando o execute_query do DatabaseConnection
            result = self.db.execute_query(query, (mitigation_id,))
            
            # Verifica se encontrou resultados
            if not result:
                self.logger.warning(f"Nenhuma mitigação encontrada com ID: {mitigation_id}")
                raise HTTPException(
                    status_code=404,
                    detail=f"Mitigation not found: {mitigation_id}"
                )
                
            # Define os nomes das colunas que esperamos receber
            columns = [
                'mitigation_id', 'alert_id', 'host_address', 'max_impact_bps',
                'max_impact_pps', 'type', 'auto', 'ip_version', 'degraded',
                'start_time', 'stop_time', 'prefix'
            ]
            
            # Cria o dicionário com os dados
            mitigation_data = dict(zip(columns, result[0]))
            
            # Log dos dados antes da conversão
            self.logger.debug(f"Dados recebidos do banco: {mitigation_data}")
            
            # Converte tipos específicos
            if mitigation_data['max_impact_bps'] is not None:
                mitigation_data['max_impact_bps'] = float(mitigation_data['max_impact_bps'])
            if mitigation_data['max_impact_pps'] is not None:
                mitigation_data['max_impact_pps'] = float(mitigation_data['max_impact_pps'])
            if mitigation_data['auto'] is not None:
                mitigation_data['auto'] = bool(mitigation_data['auto'])
            if mitigation_data['ip_version'] is not None:
                mitigation_data['ip_version'] = int(mitigation_data['ip_version'])
                
            # Log após conversão de tipos
            self.logger.debug(f"Dados após conversão de tipos: {mitigation_data}")
            
            # Cria e retorna o objeto MitigationByID
            try:
                mitigation = MitigationByID(**mitigation_data)
                self.logger.info(f"Mitigação {mitigation_id} recuperada com sucesso")
                return mitigation
            except Exception as e:
                self.logger.error(f"Erro ao criar objeto MitigationByID: {str(e)}")
                raise HTTPException(
                    status_code=500,
                    detail=f"Error creating mitigation object: {str(e)}"
                )
                
        except HTTPException:
            raise
        except Exception as e:
            self.logger.error(f"Erro não esperado ao buscar mitigação: {str(e)}")
            raise HTTPException(
                status_code=500,
                detail=f"Unexpected error fetching mitigation: {str(e)}"
            )

    async def get_current_mitigation(self) -> MitigationCurrent:
        """
        Obtém a mitigação atual/mais recente.
        
        Returns:
            MitigationCurrent: Objeto contendo os dados da mitigação atual
            
        Raises:
            HTTPException: Se houver erro ao buscar a mitigação ou se nenhuma for encontrada
        """
        try:
            self.logger.info("Fetching current mitigation")
            
            query = """
                SELECT 
                    COALESCE(mitigation_id, '') as mitigation_id,
                    COALESCE(alert_id, '') as alert_id,
                    COALESCE(host_address, '') as host_address,
                    COALESCE(max_impact_bps, 0) as max_impact_bps,
                    COALESCE(max_impact_pps, 0) as max_impact_pps,
                    COALESCE(type, '') as type,
                    COALESCE(auto, false) as auto,
                    COALESCE(ip_version, 4) as ip_version,
                    COALESCE(degraded, 'false') as degraded,
                    start_time,
                    stop_time,
                    COALESCE(prefix, '') as prefix
                FROM vw_mitigations_get_current
                WHERE 1=1
                LIMIT 1
            """
            
            result = self.db.execute_query(query)
            
            if not result or len(result) == 0:
                self.logger.warning("No active mitigation found")
                raise HTTPException(
                    status_code=404,
                    detail="No active mitigation found"
                )
                
            # Define column names explicitly
            columns = [
                'mitigation_id', 'alert_id', 'host_address', 'max_impact_bps',
                'max_impact_pps', 'type', 'auto', 'ip_version', 'degraded',
                'start_time', 'stop_time', 'prefix'
            ]
            
            # Create dictionary with proper type conversions
            mitigation_data = {}
            for i, column in enumerate(columns):
                value = result[0][i]
                
                if value is None:
                    if column in ['max_impact_bps', 'max_impact_pps']:
                        mitigation_data[column] = 0.0
                    elif column == 'auto':
                        mitigation_data[column] = False
                    elif column == 'ip_version':
                        mitigation_data[column] = 4
                    elif column in ['mitigation_id', 'alert_id', 'host_address', 'type', 'degraded', 'prefix']:
                        mitigation_data[column] = ''
                    else:
                        mitigation_data[column] = value
                else:
                    if column in ['max_impact_bps', 'max_impact_pps']:
                        mitigation_data[column] = float(value)
                    elif column == 'auto':
                        mitigation_data[column] = bool(value)
                    elif column == 'ip_version':
                        mitigation_data[column] = int(value)
                    elif column in ['start_time', 'stop_time']:
                        mitigation_data[column] = value
                    else:
                        mitigation_data[column] = str(value)
            
            self.logger.debug(f"Parsed mitigation data: {mitigation_data}")
            
            try:
                mitigation = MitigationCurrent(**mitigation_data)
                self.logger.info("Successfully retrieved current mitigation")
                return mitigation
            except Exception as e:
                self.logger.error(f"Error creating MitigationCurrent object: {str(e)}")
                self.logger.error(f"Problematic data: {mitigation_data}")
                raise HTTPException(
                    status_code=500,
                    detail=f"Error creating mitigation object: {str(e)}"
                )
                
        except HTTPException:
            raise
        except Exception as e:
            self.logger.error(f"Error fetching current mitigation: {str(e)}", exc_info=True)
            raise HTTPException(
                status_code=500,
                detail="Failed to fetch current mitigation"
            )

    async def get_top_mitigations(self, page: int = 1, page_size: int = 10) -> PaginatedResponse[MitigationTop]:
        """
        Obtém lista paginada das principais mitigações.
        
        Args:
            page (int): Número da página (começa em 1)
            page_size (int): Quantidade de itens por página
            
        Returns:
            PaginatedResponse[MitigationTop]: Lista paginada de mitigações
            
        Raises:
            HTTPException: Se houver erro ao buscar as mitigações
        """
        try:
            self.logger.info(f"Fetching top mitigations - page: {page}, page_size: {page_size}")
            params = PaginationParams(page=page, page_size=page_size)
            
            # Get total count first
            count_query = """
                SELECT COUNT(*) 
                FROM vw_mitigations_get_top
            """
            count_result = self.db.execute_query(count_query)
            total_records = count_result[0][0] if count_result else 0
            
            self.logger.debug(f"Total records found: {total_records}")
            
            if total_records == 0:
                self.logger.info("No mitigations found, returning empty response")
                return PaginatedResponse.create(
                    items=[],
                    total=0,
                    params=params
                )
            
            # Main query to get paginated results
            query = """
                SELECT 
                    mitigation_id,
                    alert_id,
                    mo_gid,
                    mo_name,
                    COALESCE(host_address, '') as host_address,
                    COALESCE(max_impact_bps, 0) as max_impact_bps,
                    COALESCE(max_impact_pps, 0) as max_impact_pps,
                    COALESCE(type, '') as type,
                    COALESCE(auto, false) as auto,
                    COALESCE(prefix, '') as prefix,
                    COALESCE(ip_version, 4) as ip_version,
                    COALESCE(degraded, 'false') as degraded,
                    COALESCE(start_time, CURRENT_TIMESTAMP) as start_time,
                    COALESCE(stop_time, null) as stop_time
                FROM vw_mitigations_get_top
                ORDER BY start_time DESC
                LIMIT %s OFFSET %s
            """
            
            self.logger.debug(f"Executing query with LIMIT {params.page_size} OFFSET {params.offset}")
            result = self.db.execute_query(query, (params.page_size, params.offset))
            
            if not result:
                self.logger.info("No results found for the current page")
                return PaginatedResponse.create(
                    items=[],
                    total=total_records,
                    params=params
                )
            
            # Define column names explicitly
            columns = [
                'mitigation_id', 'alert_id', 'mo_gid', 'mo_name', 'host_address', 'max_impact_bps',
                'max_impact_pps', 'type', 'auto', 'prefix', 'ip_version',
                'degraded', 'start_time', 'stop_time'
            ]
            
            mitigations = []
            for row in result:
                # Create dictionary with explicit type conversions
                mitigation_dict = {}
                for i, column in enumerate(columns):
                    value = row[i]
                    if column in ['max_impact_bps', 'max_impact_pps']:
                        mitigation_dict[column] = float(value) if value is not None else 0.0
                    elif column == 'auto':
                        mitigation_dict[column] = bool(value) if value is not None else False
                    elif column == 'ip_version':
                        mitigation_dict[column] = int(value) if value is not None else 4
                    elif column in ['start_time', 'stop_time']:
                        mitigation_dict[column] = value
                    else:
                        mitigation_dict[column] = str(value) if value is not None else ''
                
                try:
                    mitigation = MitigationTop(**mitigation_dict)
                    mitigations.append(mitigation)
                except Exception as e:
                    self.logger.error(f"Error creating MitigationTop object: {str(e)}")
                    self.logger.error(f"Problematic data: {mitigation_dict}")
                    continue
            
            self.logger.info(f"Successfully retrieved {len(mitigations)} mitigations")
            return PaginatedResponse.create(
                items=mitigations,
                total=total_records,
                params=params
            )
                
        except Exception as e:
            self.logger.error(f"Error fetching top mitigations: {str(e)}", exc_info=True)
            raise HTTPException(
                status_code=500,
                detail="Failed to fetch top mitigations"
            )

    async def get_traffic_data(self, mitigation_id: str) -> List[MitigationTrafficPoint]:
        """Get traffic data for a specific mitigation"""
        self.logger.info(f"Fetching traffic data for mitigation ID: {mitigation_id}")
        try:
            query = """
                SELECT 
                    a.mo_gid
                    ,a.time
                    ,a.pass_mbps
                    ,a.drop_mbps
                FROM vw_mitigations_get_traffic_data a
                WHERE 1=1
                    and a.mitigation_id = %s             
                ORDER BY time
            """
            
            result = self.db.execute_query(query, (mitigation_id,))
            
            if not result:
                self.logger.warning(f"No traffic data found for mitigation {mitigation_id}")
                return []
                
            traffic_points = []
            for row in result:
                traffic_points.append(MitigationTrafficPoint(
                    timestamp=row[1],  # time
                    pass_traffic=float(row[2]),  # pass_mbps
                    dropped_traffic=float(row[3])  # drop_mbps
                ))
            
            self.logger.info(f"Retrieved {len(traffic_points)} traffic data points")
            return traffic_points
                
        except Exception as e:
            self.logger.error(f"Error fetching traffic data: {e}", exc_info=True)
            raise HTTPException(
                status_code=500,
                detail=f"Error retrieving traffic data: {str(e)}"
            )

    async def get_active_mitigations(self) -> List[Dict]:
        self.logger.info("Fetching active mitigations")
        try:
            query = """
                    SELECT
                        m.mitigation_id
                        ,m.name
                        ,m.type
                        ,m.start_time
                        ,m.stop_time
                        ,coalesce(m.host_address, '') as host_address
                        ,coalesce(m.mps, 0) as mps
                        ,coalesce(m.pps, 0) as pps
                        FROM vw_mitigations_get_active m
                    WHERE 1=1
                    ORDER BY m.start_time DESC
            """
            
            result = self.db.execute_query(query)
            
            if not result:
                return []
                
            columns = ['mitigation_id', 'name', 'type', 'start_time', 
                    'stop_time', 'host_address', 'mps', 'pps']
                    
            mitigations = []
            for row in result:
                mitigation = dict(zip(columns, row))
                for field in ['start_time', 'stop_time']:
                    if mitigation.get(field):
                        mitigation[field] = mitigation[field].strftime('%Y-%m-%d %H:%M:%S')
                mitigations.append(mitigation)
                
            return mitigations
                
        except Exception as e:
            self.logger.error(f"Error listing active mitigations: {e}")
            raise HTTPException(
                status_code=500,
                detail=f"Error retrieving mitigations: {str(e)}"
            )

# Initialize API handler
mitigation_api = MitigationAPI()

# Route definitions
@router.get("/stats", response_model=MitigationStats)
async def get_mitigation_stats():
    """Get mitigation statistics"""
    return await mitigation_api.get_mitigation_stats()

@router.get("/active", response_model=List[MitigationActive])
async def get_active_mitigations():
    """List all active mitigations"""
    return await mitigation_api.get_active_mitigations()

@router.get("/traffic/{mitigation_id}", response_model=List[MitigationTrafficPoint])
async def get_traffic_data(mitigation_id: str):
    """Get traffic data for a specific mitigation"""
    return await mitigation_api.get_traffic_data(mitigation_id)

@router.get("/current", response_model=MitigationCurrent)
async def get_current_mitigation():
    """Get the current/most recent mitigation"""
    return await mitigation_api.get_current_mitigation()

@router.get("/top", response_model=PaginatedResponse[MitigationTop])
async def get_top_mitigations(
    page: int = Query(1, ge=1, description="Page number"),
    page_size: int = Query(10, ge=1, le=100, description="Items per page")
):
    """Get paginated list of top mitigations"""
    return await mitigation_api.get_top_mitigations(page, page_size)

@router.get("/{mitigation_id}", response_model=MitigationByID)
async def get_mitigation(mitigation_id: str):
    """Get a specific mitigation by ID"""
    return await mitigation_api.get_mitigation_by_id(mitigation_id)