"""
Alert Routes Module

Handles all alert-related API endpoints.
"""

from fastapi import APIRouter, HTTPException, Query
from typing import List
from datetime import datetime, timedelta
from data.database import DatabaseConnection
from utils.log import create_logger
from ..models import (
    Alert, 
    AlertStats, 
    AlertTrafficData, 
    AlertTop,
    PaginatedResponse,
    PaginationParams
)

router = APIRouter(prefix="/api/alerts", tags=["Alerts"])
logger = create_logger("alert_routes")

class AlertAPI:
    def __init__(self):
        self.logger = logger.getChild(self.__class__.__name__)
        self.db = DatabaseConnection()
        self.db.connect()

    async def get_current(self) -> Alert:
        try:
            query = """
            SELECT 
                COALESCE(alert_id::text, 'NO_ALERT') as alert_id,
                COALESCE(mo_name, '') as client,
                COALESCE(mo_misusesig, '') as type,
                cast(timestart_local as time) as start_time,
                COALESCE(host_address, '') as host_address,
                COALESCE(importance, 'Low') as severity,
                COALESCE(mps, 0) as mbps,
                COALESCE(pps, 0) as kpps,
                COALESCE(ongoing, false) as status
            FROM vw_alerts 
            WHERE ongoing = true
            ORDER BY ndiff desc, severity_pct desc
            limit 1
            """
            
            result = self.db.execute_query(query)
            if not result:
                return Alert(
                    alert_id="NO_ALERT",
                    start_time=datetime.now().strftime('%H:%M:%S'),
                    status="No active alerts"
                )
            
            columns = ['alert_id', 'client', 'type', 'start_time', 'host_address', 
                      'severity', 'mbps', 'kpps', 'status']
            data = dict(zip(columns, result[0]))
            
            processed_data = {
                'alert_id': str(data['alert_id']),
                'client': str(data.get('client', '')),
                'type': str(data.get('type', '')),
                'start_time': data['start_time'].strftime('%H:%M:%S') if data['start_time'] else datetime.now().strftime('%H:%M:%S'),
                'host_address': str(data.get('host_address', '')),
                'severity': str(data.get('severity', 'Low')),
                'mbps': float(data.get('mbps', 0.0)),
                'kpps': float(data.get('kpps', 0.0)),
                'status': 'Ongoing' if data.get('status', False) else 'Resolved'
            }
            
            return Alert(**processed_data)
            
        except Exception as e:
            self.logger.error(f"Error fetching current alert: {str(e)}")
            raise HTTPException(
                status_code=500, 
                detail="Failed to fetch current alert"
            )

    async def get_stats(self) -> AlertStats:
        try:
            query = """
                SELECT 
                    COUNT(*) FILTER (WHERE a.ongoing = true) as total,
                    COUNT(*) FILTER (WHERE a.ongoing = true AND a.importance = 'high') as high,
                    COUNT(*) FILTER (WHERE a.ongoing = true AND a.importance = 'medium') as medium,
                    COUNT(*) FILTER (WHERE a.ongoing = true AND a.importance = 'low') as low,
                    COUNT(*) FILTER (where a.importance = 'high') as total_high,
                    COUNT(*) FILTER (where a.importance = 'medium') as total_medium,
                    COUNT(*) FILTER (where a.importance = 'low') as total_low,
                    m.mitigation_id
                FROM vw_alerts a
                left join mitigations m on m.alert_id = a.alert_id 
                group by 
                    mitigation_id
            """
            
            result = self.db.execute_query(query)
            columns = ['total', 'high', 'medium', 'low', 'total_high', 
                      'total_medium', 'total_low', 'mitigation_id']
            data = dict(zip(columns, result[0]))
            
            processed_data = {k: int(v or 0) for k, v in data.items()}
            
            return AlertStats(**processed_data)
            
        except Exception as e:
            self.logger.error(f"Error fetching alert stats: {str(e)}")
            raise HTTPException(
                status_code=500,
                detail="Failed to fetch alert statistics"
            )

    async def get_top(self, page: int = 1, page_size: int = 10) -> PaginatedResponse[AlertTop]:
        """
        Obtém alertas paginados ordenados por severidade e data
        """
        try:
            params = PaginationParams(page=page, page_size=page_size)
            
            # Primeiro obtém o total de registros
            count_query = """
                SELECT COUNT(*)
                FROM vw_alerts 
                WHERE start_time >= CURRENT_DATE
            """
            
            count_result = self.db.execute_query(count_query)
            total_records = count_result[0][0] if count_result else 0
            
            # Query principal com LIMIT e OFFSET
            query = """
                SELECT 
                    a.alert_id::text as id,
                    COALESCE(a.importance, 'Low') as severity,
                    COALESCE(a.mo_name, 'Unknown') as client,
                    COALESCE(a.mo_misusesig, 'Unknown') as type,
                    to_char(a.start_time, 'HH24:MI:SS') as start_time,
                    COALESCE(a.host_address, 'Unknown') as host_address,
                    COALESCE(a.mps, 0) as mbps,
                    COALESCE(a.pps, 0) as kpps,
                        m.mitigation_id
                FROM vw_alerts a
                left join mitigations m on m.alert_id = a.alert_id
                WHERE a.start_time >= CURRENT_DATE
                ORDER BY 
                    COALESCE(m.mitigation_id, '') desc,
                    CASE 
                        WHEN a.importance = 'high' THEN 1
                        WHEN a.importance = 'medium' THEN 2
                        WHEN a.importance = 'low' THEN 3
                        ELSE 4
                    END,
                    a.start_time DESC
                LIMIT %s OFFSET %s
            """
            
            result = self.db.execute_query(query, (params.page_size, params.offset))
            
            top_alerts = []
            columns = ['id', 'severity', 'client', 'type', 'start_time', 
                      'host_address', 'mbps', 'kpps', 'mitigation_id']
            
            for row in result:
                data = dict(zip(columns, row))
                processed_data = {
                    'id': str(data['id']),
                    'severity': str(data['severity']).capitalize(),
                    'client': str(data['client']),
                    'type': str(data['type']),
                    'start_time': str(data['start_time']),
                    'host_address': str(data['host_address']),
                    'mbps': float(data['mbps']),
                    'kpps': float(data['kpps']),
                    'mitigation_id': str(data['mitigation_id'])
                }
                top_alerts.append(AlertTop(**processed_data))
            
            return PaginatedResponse.create(
                items=top_alerts,
                total=total_records,
                params=params
            )
            
        except Exception as e:
            self.logger.error(f"Error fetching top alerts: {str(e)}")
            raise HTTPException(
                status_code=500,
                detail="Failed to fetch top alerts"
            )

    async def get_alert_traffic(self) -> List[AlertTrafficData]:
        try:
            query = """
                SELECT 
                    time,
                    misusetype,
                    value,
                    tcp
                FROM vw_alert_traffic
            """
            
            result = self.db.execute_query(query)
            if not result:
                current_time = datetime.now()
                dummy_data = []
                for i in range(6):
                    time = (current_time - timedelta(minutes=10 * i)).strftime('%H:%M')
                    dummy_data.append(AlertTrafficData(
                        time=time,
                        misusetype="Unknown",
                        value=0.0,
                        tcp=0.0
                    ))
                return list(reversed(dummy_data))
            
            traffic_data = []
            for row in result:
                data = {
                    'time': str(row[0]),
                    'misusetype': str(row[1]),
                    'value': float(row[2] or 0.0),
                    'tcp': float(row[3] or 0.0)
                }
                traffic_data.append(AlertTrafficData(**data))
            
            return traffic_data
            
        except Exception as e:
            self.logger.error(f"Error fetching traffic data: {str(e)}")
            raise HTTPException(
                status_code=500,
                detail="Failed to fetch traffic data"
            )

# Initialize API handler
alert_api = AlertAPI()

# Route definitions
@router.get("/current", response_model=Alert)
async def get_current_alert():
    """Get the most recent active alert"""
    return await alert_api.get_current()

@router.get("/stats", response_model=AlertStats)
async def get_alert_stats():
    """Get alert statistics"""
    return await alert_api.get_stats()

@router.get("/traffic", response_model=List[AlertTrafficData])
async def get_traffic_data():
    """Get Alert traffic data for the last hour"""
    return await alert_api.get_alert_traffic()

@router.get("/top", response_model=PaginatedResponse[AlertTop])
async def get_top_alerts(
    page: int = Query(1, ge=1, description="Número da página"),
    page_size: int = Query(10, ge=1, le=100, description="Itens por página")
):
    """
    Get paginated top alerts of the day
    
    - **page**: Número da página (começa em 1)
    - **page_size**: Quantidade de itens por página (entre 1 e 100)
    """
    return await alert_api.get_top(page, page_size)