from typing import Optional
from pydantic import BaseModel

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