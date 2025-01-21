"""
API Models Module

This module contains all the Pydantic models used for request/response validation
across different API endpoints.
"""

from typing import Optional, List, Generic, TypeVar
from pydantic import BaseModel, ConfigDict

T = TypeVar('T')

# Base Alert Models
class Alert(BaseModel):
    alert_id: str
    client: Optional[str] = None
    type: Optional[str] = None
    start_time: str
    host_address: Optional[str] = None
    severity: Optional[str] = "low"
    mbps: float = 0.0
    kpps: float = 0.0
    status: str = "Unknown"

    model_config = ConfigDict(from_attributes=True)

class AlertStats(BaseModel):
    total: int = 0
    high: int = 0
    medium: int = 0
    low: int = 0
    total_high: int = 0
    total_medium: int = 0
    total_low: int = 0

    model_config = ConfigDict(from_attributes=True)

class AlertTop(BaseModel):
    id: str
    severity: str
    client: str
    type: str
    start_time: str
    host_address: str
    mbps: float
    kpps: float
    mitigation_id: Optional[str] = None

    model_config = ConfigDict(from_attributes=True)

class AlertTrafficData(BaseModel):
    time: str
    misusetype: str
    value: float = 0.0
    tcp: float = 0.0

    model_config = ConfigDict(from_attributes=True)

# Pagination Models
class PaginationParams(BaseModel):
    """Parâmetros de paginação para requisições"""
    page: int = 1
    page_size: int = 10

    @property
    def offset(self) -> int:
        return (self.page - 1) * self.page_size

    model_config = ConfigDict(
        from_attributes=True,
        json_schema_extra = {
            "example": {
                "page": 1,
                "page_size": 10
            }
        }
    )

class PaginatedResponse(BaseModel, Generic[T]):
    """Resposta paginada genérica"""
    items: List[T]
    total: int
    page: int
    page_size: int
    total_pages: int

    model_config = ConfigDict(
        from_attributes=True,
        json_schema_extra = {
            "example": {
                "items": [],
                "total": 0,
                "page": 1,
                "page_size": 10,
                "total_pages": 0
            }
        }
    )

    @classmethod
    def create(cls, items: List[T], total: int, params: PaginationParams) -> 'PaginatedResponse[T]':
        """
        Cria uma resposta paginada a partir dos items e parâmetros de paginação
        
        Args:
            items: Lista de items da página atual
            total: Total de registros
            params: Parâmetros de paginação utilizados
            
        Returns:
            PaginatedResponse com os metadados calculados
        """
        return cls(
            items=items,
            total=total,
            page=params.page,
            page_size=params.page_size,
            total_pages=((total - 1) // params.page_size) + 1 if total > 0 else 0
        )