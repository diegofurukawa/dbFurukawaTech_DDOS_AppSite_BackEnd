"""
API Models Module

This module contains all the Pydantic models used for request/response validation
across different API endpoints.
"""

from typing import Optional
from pydantic import BaseModel

class TrafficData(BaseModel):
    time: str
    value: float = 0.0
    tcp: float = 0.0