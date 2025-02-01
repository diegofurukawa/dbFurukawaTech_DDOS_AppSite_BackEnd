"""
API Models Module
"""

from datetime import datetime
from typing import Optional, List
from pydantic import BaseModel, Field

class MitigationByID(BaseModel):
    """Model para retorno de uma mitigação específica pela view vw_mitigations_get_by_id"""
    mitigation_id: str = Field(description="ID único da mitigação")
    alert_id: str = Field(description="ID do alerta associado")
    host_address: Optional[str] = Field(None, description="Endereço do host afetado")
    max_impact_bps: Optional[float] = Field(None, description="Impacto máximo em bits por segundo")
    max_impact_pps: Optional[float] = Field(None, description="Impacto máximo em pacotes por segundo")
    type: str = Field(description="Tipo da mitigação")
    auto: bool = Field(description="Indica se é uma mitigação automática")
    ip_version: int = Field(description="Versão do IP (4 ou 6)")
    degraded: Optional[str] = Field(None, description="Status de degradação")
    start_time: datetime = Field(description="Horário de início da mitigação")
    stop_time: Optional[datetime] = Field(None, description="Horário de término da mitigação")
    prefix: Optional[str] = Field(None, description="Prefixo de rede afetado")

    class Config:
        from_attributes = True
        json_encoders = {
            datetime: lambda v: v.strftime("%Y-%m-%d %H:%M:%S") if v else None
        }


class MitigationTop(BaseModel):
    """Model para retorno de uma mitigação específica pela view vw_mitigations_get_top"""
    mitigation_id: str = Field(description="ID único da mitigação")
    alert_id: str = Field(description="ID do alerta associado")
    mo_gid: str = Field(description="mo_gid do alerta associado")
    mo_name: str = Field(description="mo_name do alerta associado")    
    host_address: Optional[str] = Field(None, description="Endereço do host afetado")
    max_impact_bps: Optional[float] = Field(None, description="Impacto máximo em bits por segundo")
    max_impact_pps: Optional[float] = Field(None, description="Impacto máximo em pacotes por segundo")
    type: str = Field(description="Tipo da mitigação")
    auto: bool = Field(description="Indica se é uma mitigação automática")
    ip_version: int = Field(description="Versão do IP (4 ou 6)")
    degraded: Optional[str] = Field(None, description="Status de degradação")
    start_time: datetime = Field(description="Horário de início da mitigação")
    stop_time: Optional[datetime] = Field(None, description="Horário de término da mitigação")
    prefix: Optional[str] = Field(None, description="Prefixo de rede afetado")

    class Config:
        from_attributes = True
        json_encoders = {
            datetime: lambda v: v.strftime("%Y-%m-%d %H:%M:%S") if v else None
        }
        

class MitigationCurrent(BaseModel):
    """Model para retorno de uma mitigação específica pela view vw_mitigations_get_current"""
    mitigation_id: str = Field(description="ID único da mitigação")
    alert_id: str = Field(description="ID do alerta associado")
    host_address: Optional[str] = Field(None, description="Endereço do host afetado")
    max_impact_bps: Optional[float] = Field(None, description="Impacto máximo em bits por segundo")
    max_impact_pps: Optional[float] = Field(None, description="Impacto máximo em pacotes por segundo")
    type: str = Field(description="Tipo da mitigação")
    auto: bool = Field(description="Indica se é uma mitigação automática")
    ip_version: int = Field(description="Versão do IP (4 ou 6)")
    degraded: Optional[str] = Field(None, description="Status de degradação")
    start_time: datetime = Field(description="Horário de início da mitigação")
    stop_time: Optional[datetime] = Field(None, description="Horário de término da mitigação")
    prefix: Optional[str] = Field(None, description="Prefixo de rede afetado")

    class Config:
        from_attributes = True
        json_encoders = {
            datetime: lambda v: v.strftime("%Y-%m-%d %H:%M:%S") if v else None
        }

class MitigationActive(BaseModel):
    """Model para retorno de uma mitigação específica pela view vw_mitigations_get_active"""
    mitigation_id: str = Field(description="ID único da mitigação")
    name: str = Field(description="Nome da mitigação")
    type: str = Field(description="Tipo da mitigação")
    start_time: datetime = Field(description="Horário de início da mitigação")
    stop_time: Optional[datetime] = Field(None, description="Horário de término da mitigação")
    host_address: Optional[str] = Field(None, description="Endereço do host afetado")
    mps: Optional[float] = Field(None, description="Impacto máximo em bits por segundo")
    pps: Optional[float] = Field(None, description="Impacto máximo em pacotes por segundo")
    
    class Config:
        from_attributes = True
        json_encoders = {
            datetime: lambda v: v.strftime("%Y-%m-%d %H:%M:%S") if v else None
        }

class MitigationBase(BaseModel):
    mitigation_id: str
    alert_id: Optional[str] = None
    name: Optional[str] = None
    subtype: Optional[str] = None
    auto: bool = False
    type: Optional[str] = None
    type_name: Optional[str] = None
    config_id: Optional[str] = None
    prefix: Optional[str] = None
    alert_id: Optional[str] = None
    degraded: Optional[str] = None
    user_mitigation: Optional[str] = None
    is_automitigation: bool = False
    ip_version: Optional[int] = None
    flist_gid: Optional[str] = None
    is_learning: bool = False
    learning_cancelled: bool = False
    mo_name: Optional[str] = None
    mo_gid: Optional[str] = None
    duration: Optional[int] = None
    ongoing: bool = False
    start_time: Optional[datetime] = None
    stop_time: Optional[datetime] = None
    updated_at: Optional[datetime] = None
    inserted_at: Optional[datetime] = None
    host_address: Optional[str] = None
    max_impact_bps: Optional[float] = None
    max_impact_pps: Optional[float] = None

    class Config:
        from_attributes = True

class MitigationStats(BaseModel):
    active_mitigations: int = 0
    total_mitigated: int = 0
    avg_response_time: float = 0.0
    success_rate: float = 0.0

class MitigationTrafficPoint(BaseModel):
    timestamp: datetime
    pass_traffic: float
    dropped_traffic: float