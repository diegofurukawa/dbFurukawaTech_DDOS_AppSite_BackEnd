"""
Mitigation Routes Module

Handles all mitigation-related API endpoints.
"""

from fastapi import APIRouter, HTTPException
from typing import Dict, List, Optional
from datetime import datetime, timedelta
from data.database import DatabaseConnection
from utils.log import create_logger
from ..models import MitigationBase, MitigationTrafficPoint, MitigationStats

router = APIRouter(prefix="/api/mitigations", tags=["mitigations"])
logger = create_logger("mitigation_routes")

class MitigationAPI:
    def __init__(self):
        self.logger = logger.getChild(self.__class__.__name__)
        self.db = DatabaseConnection()
        self.db.connect()

    async def get_mitigation_stats(self) -> MitigationStats:
        """Retorna estatísticas gerais das mitigações"""
        try:
            with self.db.connection.cursor() as cursor:
                # Conta mitigações ativas
                cursor.execute("""
                    SELECT COUNT(*) FROM mitigations m
                    inner join alerts a on a.alert_id = m.alert_id 
                    WHERE m.ongoing = true
                """)
                active = cursor.fetchone()[0]

                # Total de mitigações
                cursor.execute("SELECT COUNT(*) FROM mitigations")
                total = cursor.fetchone()[0]

                # Tempo médio de resposta (em segundos)
                cursor.execute("""
                    SELECT AVG(EXTRACT(EPOCH FROM (stop_time - start_time))) 
                    FROM mitigations 
                    WHERE stop_time IS NOT NULL
                """)
                avg_time = cursor.fetchone()[0] or 0

                # Taxa de sucesso (mitigações completadas com sucesso)
                cursor.execute("""
                    SELECT COUNT(*) 
                    FROM mitigations 
                    WHERE stop_time IS NOT NULL AND degraded = 'false'
                """)
                success = cursor.fetchone()[0]
                success_rate = (success / total * 100) if total > 0 else 100

                return MitigationStats(
                    active_mitigations=active,
                    total_mitigated=total,
                    avg_response_time=round(avg_time / 60, 1),  # Converte para minutos
                    success_rate=round(success_rate, 1)
                )
        except Exception as e:
            self.logger.error(f"Erro ao obter estatísticas de mitigação: {e}")
            raise

    async def get_traffic_data(self, mitigation_id: str) -> List[MitigationTrafficPoint]:
            """Obtém dados de tráfego para uma mitigação específica"""
            try:
                with self.db.connection.cursor() as cursor:
                    # Primeiro, busca o alert_id associado à mitigação
                    cursor.execute("""
                            SELECT a.alert_id
                            FROM mitigations m
                            INNER JOIN alerts a ON m.alert_id = a.alert_id
                            ORDER BY m.start_time desc
                            limit 1
                    """)
                    
                    result = cursor.fetchone()
                    if not result or not result[0]:
                        self.logger.warning(f"Nenhum alerta associado à mitigação {mitigation_id}")
                        return []
                        
                    alert_id = result[0]

                    # Gera dados simulados para teste
                    traffic_points = []
                    now = datetime.now()
                    
                    # Gera 30 pontos de dados para os últimos 30 minutos
                    for i in range(30):
                        point_time = now - timedelta(minutes=i)
                        traffic_points.append(MitigationTrafficPoint(
                            timestamp=point_time,
                            pass_traffic=float(1000 + (i * 100)),  # Dados simulados
                            dropped_traffic=float(500 + (i * 50))   # Dados simulados
                        ))
                    
                    return sorted(traffic_points, key=lambda x: x.timestamp)
                    
            except Exception as e:
                self.logger.error(f"Erro ao obter dados de tráfego: {e}")
                raise HTTPException(
                    status_code=500,
                    detail=f"Erro ao obter dados de tráfego: {str(e)}"
                )   
        
    async def get_active_mitigations(self) -> List[Dict]:
        """Lista mitigações ativas no momento"""
        try:
            with self.db.connection.cursor() as cursor:
                cursor.execute("""
                    SELECT m.*, a.host_address, a.max_impact_bps, a.max_impact_pps
                    FROM mitigations m
                    INNER JOIN alerts a ON m.alert_id = a.alert_id
                    ORDER BY m.start_time DESC
                """)
                columns = [desc[0] for desc in cursor.description]
                mitigations = []
                
                for row in cursor.fetchall():
                    mitigation = dict(zip(columns, row))
                    # Formata timestamps para string
                    for field in ['start_time', 'stop_time']:
                        if mitigation[field]:
                            mitigation[field] = mitigation[field].strftime('%Y-%m-%d %H:%M:%S')
                    mitigations.append(mitigation)
                
                return mitigations
        except Exception as e:
            self.logger.error(f"Erro ao listar mitigações ativas: {e}")
            raise

    async def update_mitigation(self, mitigation_id: str, data: Dict) -> Dict:
        """Atualiza uma mitigação"""
        try:
            valid_fields = ['name', 'type', 'config_id', 'is_learning']
            update_data = {k: v for k, v in data.items() if k in valid_fields}
            
            if not update_data:
                raise ValueError("Nenhum campo válido para atualização")
                
            with self.db.connection.cursor() as cursor:
                fields = ', '.join([f"{k} = %s" for k in update_data.keys()])
                values = list(update_data.values())
                
                cursor.execute(f"""
                    UPDATE mitigations 
                    SET {fields}, updated_at = CURRENT_TIMESTAMP
                    WHERE mitigation_id = %s
                    RETURNING *
                """, values + [mitigation_id])
                
                if cursor.rowcount == 0:
                    raise ValueError("Mitigação não encontrada")
                    
                updated = dict(zip([desc[0] for desc in cursor.description], cursor.fetchone()))
                self.db.connection.commit()
                return updated
                
        except Exception as e:
            self.db.connection.rollback()
            self.logger.error(f"Erro ao atualizar mitigação: {e}")
            raise


# Initialize API handler
mitigation_api = MitigationAPI()


# Route definitions

@router.get("/stats", response_model=MitigationStats)
async def get_mitigation_stats():
    return await mitigation_api.get_mitigation_stats()

@router.get("/active", response_model=List[MitigationBase])  # Corrigido aqui
async def get_active_mitigations():
    """Lista todas as mitigações ativas"""
    return await mitigation_api.get_active_mitigations()

@router.get("/{mitigation_id}/traffic", response_model=List[MitigationTrafficPoint])
async def get_traffic_data(mitigation_id: str):
    try:
        return await mitigation_api.get_traffic_data(mitigation_id)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))