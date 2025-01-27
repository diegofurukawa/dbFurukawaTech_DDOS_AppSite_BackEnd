"""
Mitigation Routes Module

Handles all mitigation-related API endpoints with improved logging.
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
        self.logger.info("Iniciando busca por estatísticas de mitigação")
        try:
            with self.db.connection.cursor() as cursor:
                # Conta mitigações ativas
                cursor.execute("""
                    SELECT 
                    COUNT(*) 
                    from vw_alerts  a
                    inner join mitigations c on c.alert_id = a.alert_id
                    WHERE 1=1
                """)
                active = cursor.fetchone()[0]
                self.logger.debug(f"Mitigações ativas encontradas: {active}")

                # Total de mitigações
                cursor.execute("""
                                SELECT 
                                    COUNT(*) 
                                from vw_alerts  a
                                inner join mitigations c on c.alert_id = a.alert_id
                                WHERE 1=1
                            """)
                total = cursor.fetchone()[0]
                self.logger.debug(f"Total de mitigações: {total}")

                # Tempo médio de resposta (em segundos)
                cursor.execute("""
                    SELECT 
                        AVG(EXTRACT(EPOCH FROM (a.stop_time - a.start_time))) 
                    from vw_alerts  a
                    inner join mitigations c on c.alert_id = a.alert_id
                    WHERE a.stop_time IS NOT NULL
                """)
                avg_time = cursor.fetchone()[0] or 0
                self.logger.debug(f"Tempo médio de resposta: {avg_time:.2f} segundos")

                # Taxa de sucesso (mitigações completadas com sucesso)
                cursor.execute("""
                        SELECT 
                            COUNT(*) 
                        from vw_alerts  a
                        inner join mitigations c on c.alert_id = a.alert_id
                        WHERE 1=1
                        and a.stop_time IS NOT NULL
                        AND degraded = 'false'
                """)
                success = cursor.fetchone()[0]
                success_rate = (success / total * 100) if total > 0 else 100
                self.logger.debug(f"Taxa de sucesso: {success_rate:.1f}%")

                stats = MitigationStats(
                    active_mitigations=active,
                    total_mitigated=total,
                    avg_response_time=round(avg_time / 60, 1),  # Converte para minutos
                    success_rate=round(success_rate, 1)
                )
                self.logger.info("Estatísticas de mitigação recuperadas com sucesso")
                return stats

        except Exception as e:
            self.logger.error(f"Erro ao obter estatísticas de mitigação: {e}", exc_info=True)
            raise

    async def get_traffic_data(self, mitigation_id: str) -> List[MitigationTrafficPoint]:
        """Obtém dados de tráfego para uma mitigação específica"""
        self.logger.info(f"Buscando dados de tráfego para mitigação ID: {mitigation_id}")
        try:
            with self.db.connection.cursor() as cursor:
                cursor.execute("""
                        SELECT a.alert_id
                        FROM mitigations m
                        INNER JOIN vw_alerts a ON m.alert_id = a.alert_id
                        ORDER BY m.start_time desc
                        limit 1
                """)
                
                result = cursor.fetchone()
                if not result or not result[0]:
                    self.logger.warning(f"Nenhum alerta associado à mitigação {mitigation_id}")
                    return []
                    
                alert_id = result[0]
                self.logger.debug(f"Alert ID encontrado: {alert_id}")

                # Gera dados simulados para teste
                traffic_points = []
                now = datetime.now()
                self.logger.debug("Gerando pontos de dados de tráfego")
                
                # Gera 30 pontos de dados para os últimos 30 minutos
                for i in range(30):
                    point_time = now - timedelta(minutes=i)
                    traffic_points.append(MitigationTrafficPoint(
                        timestamp=point_time,
                        pass_traffic=float(1000 + (i * 100)),
                        dropped_traffic=float(500 + (i * 50))
                    ))
                
                self.logger.info(f"Gerados {len(traffic_points)} pontos de dados de tráfego")
                return sorted(traffic_points, key=lambda x: x.timestamp)
                
        except Exception as e:
            self.logger.error(
                f"Erro ao obter dados de tráfego para mitigação {mitigation_id}: {e}",
                exc_info=True
            )
            raise HTTPException(
                status_code=500,
                detail=f"Erro ao obter dados de tráfego: {str(e)}"
            )   
        
    async def get_active_mitigations(self) -> List[Dict]:
        """Lista mitigações ativas no momento"""
        self.logger.info("Buscando mitigações ativas")
        try:
            with self.db.connection.cursor() as cursor:
                query = """
                    SELECT m.*, a.host_address, a.mps, a.pps
                    FROM mitigations m
                    INNER JOIN vw_alerts a ON m.alert_id = a.alert_id
                    ORDER BY m.mitigation_id DESC
                    limit 1
                """
                self.logger.debug(f"Executando query: {query}")
                cursor.execute(query)
                
                columns = [desc[0] for desc in cursor.description]
                mitigations = []
                
                for row in cursor.fetchall():
                    mitigation = dict(zip(columns, row))
                    # Formata timestamps para string
                    for field in ['start_time', 'stop_time']:
                        if mitigation[field]:
                            mitigation[field] = mitigation[field].strftime('%Y-%m-%d %H:%M:%S')
                    mitigations.append(mitigation)
                
                self.logger.info(f"Encontradas {len(mitigations)} mitigações ativas")
                return mitigations
                
        except Exception as e:
            self.logger.error(f"Erro ao listar mitigações ativas: {e}", exc_info=True)
            raise

    async def update_mitigation(self, mitigation_id: str, data: Dict) -> Dict:
        """Atualiza uma mitigação"""
        self.logger.info(f"Iniciando atualização da mitigação ID: {mitigation_id}")
        try:
            valid_fields = ['name', 'type', 'config_id', 'is_learning']
            update_data = {k: v for k, v in data.items() if k in valid_fields}
            
            if not update_data:
                msg = "Nenhum campo válido para atualização"
                self.logger.warning(msg)
                raise ValueError(msg)
                
            with self.db.connection.cursor() as cursor:
                fields = ', '.join([f"{k} = %s" for k in update_data.keys()])
                values = list(update_data.values())
                
                query = f"""
                    UPDATE mitigations 
                    SET {fields}, updated_at = CURRENT_TIMESTAMP
                    WHERE mitigation_id = %s
                    RETURNING *
                """
                self.logger.debug(f"Executando query de atualização: {query}")
                cursor.execute(query, values + [mitigation_id])
                
                if cursor.rowcount == 0:
                    msg = "Mitigação não encontrada"
                    self.logger.warning(msg)
                    raise ValueError(msg)
                    
                updated = dict(zip([desc[0] for desc in cursor.description], cursor.fetchone()))
                self.db.connection.commit()
                self.logger.info(f"Mitigação {mitigation_id} atualizada com sucesso")
                return updated
                
        except Exception as e:
            self.db.connection.rollback()
            self.logger.error(f"Erro ao atualizar mitigação: {e}", exc_info=True)
            raise


# Initialize API handler
mitigation_api = MitigationAPI()


# Route definitions with improved logging
@router.get("/stats", response_model=MitigationStats)
async def get_mitigation_stats():
    """Obtém estatísticas de mitigação"""
    logger.info("Recebida requisição para estatísticas de mitigação")
    stats = await mitigation_api.get_mitigation_stats()
    logger.info("Estatísticas de mitigação retornadas com sucesso")
    return stats

@router.get("/active", response_model=List[MitigationBase])
async def get_active_mitigations():
    """Lista todas as mitigações ativas"""
    logger.info("Recebida requisição para listar mitigações ativas")
    mitigations = await mitigation_api.get_active_mitigations()
    logger.info(f"Retornadas {len(mitigations)} mitigações ativas")
    return mitigations

@router.get("/{mitigation_id}/traffic", response_model=List[MitigationTrafficPoint])
async def get_traffic_data(mitigation_id: str):
    """Obtém dados de tráfego de uma mitigação"""
    logger.info(f"Recebida requisição de dados de tráfego para mitigação ID: {mitigation_id}")
    try:
        data = await mitigation_api.get_traffic_data(mitigation_id)
        logger.info(f"Dados de tráfego retornados com sucesso para mitigação {mitigation_id}")
        return data
    except Exception as e:
        logger.error(f"Falha ao obter dados de tráfego: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail=str(e))