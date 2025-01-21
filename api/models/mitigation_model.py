"""
API Models Module
"""

from datetime import datetime
from typing import Optional, List
from pydantic import BaseModel

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