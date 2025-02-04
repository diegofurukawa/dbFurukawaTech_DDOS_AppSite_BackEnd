from typing import Optional
from pydantic import BaseModel

class CustomerDashboardStatsResponse(BaseModel):
    idcompany: int
    namecompany: str
    idcustomer: int
    namecustomer: str
    idmogid: str
    name: str
    namountalerts: Optional[int] = 0
    namountmitigations: Optional[int] = 0
    hosts_address: str

    class Config:
        from_attributes = True

class CustomerDashboardGraphPoint(BaseModel):
    nyear: int
    nmonth: int
    nday: int
    idmogid: str
    name: str
    namountalerts: int

    class Config:
        from_attributes = True

class CustomerDashboardResponse(BaseModel):
    idcompany: int
    namecompany: str
    idcustomer: int
    namecustomer: str
    idmogid: str
    name: str
    host_address: str
    namountalerts: int
    namountmitigations: int
    nyear: int
    nmonth: int
    nday: int
    nweek: int
    hosts_address: str

    class Config:
        from_attributes = True

class CustomerListResponse(BaseModel):
    idcompany: int
    namecompany: str
    idcustomer: int
    namecustomer: str
    idmogid: str
    name: str
    host_address: str
    namountalerts: int
    namountmitigations: int
    nyear: int
    nmonth: int
    nday: int
    nweek: int
    hosts_address: str

    class Config:
        from_attributes = True