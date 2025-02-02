# managed_object_routes.py
from fastapi import APIRouter, HTTPException
from typing import List
from data.database import DatabaseConnection
from utils.log import create_logger
from ..models.managed_object_model import (
    ManagedObjectResponse
)

router = APIRouter(prefix="/api/managed-objects", tags=["Managed Objects"])
logger = create_logger("managed_object_routes")

class ManagedObjectAPI:
    def __init__(self):
        self.logger = logger.getChild(self.__class__.__name__)
        self.db = DatabaseConnection()
        self.db.connect()

    async def get_managed_objects(self) -> List[ManagedObjectResponse]:
        try:
            query = """
                SELECT 
                    gid,
                    name,
                    description
                FROM managedobjects
                ORDER BY name
            """
            
            result = self.db.execute_query(query)
            
            managed_objects = []
            for row in result:
                managed_object = ManagedObjectResponse(
                    gid=str(row[0]) if row[0] else "",
                    name=str(row[1]) if row[1] else "",
                    description=str(row[2]) if row[2] else None
                )
                managed_objects.append(managed_object)
            
            return managed_objects
            
        except Exception as e:
            self.logger.error(f"Error fetching managed objects: {str(e)}")
            raise HTTPException(
                status_code=500,
                detail="Failed to fetch managed objects"
            )

# Initialize API handler
managed_object_api = ManagedObjectAPI()

# Route definition
@router.get("", response_model=List[ManagedObjectResponse])
async def get_managed_objects():
    """Get list of managed objects with their GID, name and description"""
    return await managed_object_api.get_managed_objects()