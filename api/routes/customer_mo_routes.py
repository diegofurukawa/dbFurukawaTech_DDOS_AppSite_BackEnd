# customer_mo_routes.py
from fastapi import APIRouter, HTTPException, Depends, Query, status
from typing import Optional
from datetime import datetime
from data.database import DatabaseConnection
from utils.log import create_logger
from utils.auth import get_current_user
from ..models.alert_model import PaginatedResponse, PaginationParams
from ..models.customer_mo_model import CustomerMOCreate, CustomerMOUpdate, CustomerMOResponse

router = APIRouter(prefix="/api/customer-managed-objects", tags=["customer-managed-objects"])
logger = create_logger("customer_mo_routes")

class CustomerMOAPI:
    def __init__(self):
        self.logger = logger.getChild(self.__class__.__name__)
        self.db = DatabaseConnection()
        self.db.connect()

    async def create_assignment(self, customer_mo: CustomerMOCreate, current_user: dict) -> CustomerMOResponse:
        try:
            # Verify if managed object exists
            mo_result = self.db.execute_query(
                "SELECT id FROM managedobjects WHERE id = %s",
                (customer_mo.idMogid,)
            )
            if not mo_result:
                raise HTTPException(
                    status_code=404,
                    detail=f"Managed Object with ID {customer_mo.idMogid} not found"
                )

            # Verify if customer exists
            customer_result = self.db.execute_query(
                "SELECT idCustomer FROM customers WHERE idCustomer = %s",
                (customer_mo.idCustomer,)
            )
            if not customer_result:
                raise HTTPException(
                    status_code=404,
                    detail=f"Customer with ID {customer_mo.idCustomer} not found"
                )

            # Check if MO is already assigned
            existing = self.db.execute_query(
                "SELECT idMogid FROM customer_managed_objects WHERE idMogid = %s",
                (customer_mo.idMogid,)
            )
            if existing:
                raise HTTPException(
                    status_code=400,
                    detail="This Managed Object is already assigned to a customer"
                )

            query = """
                INSERT INTO customer_managed_objects (
                    idMogid,
                    idCustomer,
                    active,
                    createdAt
                )
                VALUES (%s, %s, %s, %s)
                RETURNING idMogid, idCustomer, active, createdAt, updatedAt
            """
            
            values = (
                customer_mo.idMogid,
                customer_mo.idCustomer,
                customer_mo.active,
                datetime.now()
            )

            result = self.db.execute_query(query, values)
            
            columns = ['idMogid', 'idCustomer', 'active', 'createdAt', 'updatedAt']
            return CustomerMOResponse(**dict(zip(columns, result[0])))

        except HTTPException:
            raise
        except Exception as e:
            self.logger.error(f"Error creating assignment: {str(e)}")
            raise HTTPException(
                status_code=500,
                detail=f"Failed to create assignment: {str(e)}"
            )

    async def update_assignment(
        self, 
        idMogid: str, 
        data: CustomerMOUpdate, 
        current_user: dict
    ) -> CustomerMOResponse:
        try:
            update_fields = []
            values = []
            
            if data.idCustomer is not None:
                # Verify if customer exists
                customer_result = self.db.execute_query(
                    "SELECT idCustomer FROM customers WHERE idCustomer = %s",
                    (data.idCustomer,)
                )
                if not customer_result:
                    raise HTTPException(
                        status_code=404,
                        detail=f"Customer with ID {data.idCustomer} not found"
                    )
                update_fields.append("idCustomer = %s")
                values.append(data.idCustomer)

            if data.active is not None:
                update_fields.append("active = %s")
                values.append(data.active)

            if not update_fields:
                raise HTTPException(
                    status_code=400,
                    detail="No fields to update"
                )

            # Add updatedAt
            update_fields.append("updatedAt = %s")
            values.append(datetime.now())
            values.append(idMogid)  # for WHERE clause

            query = f"""
                UPDATE customer_managed_objects 
                SET {', '.join(update_fields)}
                WHERE idMogid = %s
                RETURNING idMogid, idCustomer, active, createdAt, updatedAt
            """

            result = self.db.execute_query(query, values)
            
            if not result:
                raise HTTPException(
                    status_code=404,
                    detail="Assignment not found"
                )
            
            columns = ['idMogid', 'idCustomer', 'active', 'createdAt', 'updatedAt']
            return CustomerMOResponse(**dict(zip(columns, result[0])))

        except HTTPException:
            raise
        except Exception as e:
            self.logger.error(f"Error updating assignment: {str(e)}")
            raise HTTPException(
                status_code=500,
                detail=f"Failed to update assignment: {str(e)}"
            )

    async def list_assignments(
        self,
        search: Optional[str] = None,
        customer_id: Optional[int] = None,
        page: int = 1,
        page_size: int = 10
    ) -> PaginatedResponse[CustomerMOResponse]:
        try:
            params = PaginationParams(page=page, page_size=page_size)
            
            where_clauses = ["1=1"]
            query_params = []
            
            if search:
                where_clauses.append("(idMogid LIKE %s)")
                query_params.append(f"%{search}%")
                
            if customer_id:
                where_clauses.append("idCustomer = %s")
                query_params.append(customer_id)

            # Count total records
            count_query = f"""
                SELECT COUNT(*) 
                FROM customer_managed_objects 
                WHERE {' AND '.join(where_clauses)}
            """
            count_result = self.db.execute_query(count_query, query_params)
            total_records = count_result[0][0] if count_result else 0
            
            # Main query
            query = f"""
                SELECT mo.idMogid, mo.idCustomer, mo.active, mo.createdAt, mo.updatedAt,
                       m.name as mo_name, c.nameCustomer as customer_name
                FROM customer_managed_objects mo
                LEFT JOIN managedobjects m ON mo.idMogid = m.id
                LEFT JOIN customers c ON mo.idCustomer = c.idCustomer
                WHERE {' AND '.join(where_clauses)}
                ORDER BY mo.createdAt DESC
                LIMIT %s OFFSET %s
            """
            
            final_params = tuple(query_params + [params.page_size, params.offset])
            result = self.db.execute_query(query, final_params)
            
            # Process results
            items = []
            for row in result:
                item_dict = {
                    'idMogid': row[0],
                    'idCustomer': row[1],
                    'active': row[2],
                    'createdAt': row[3],
                    'updatedAt': row[4],
                    'mo_name': row[5],
                    'customer_name': row[6]
                }
                items.append(CustomerMOResponse(**item_dict))
            
            return PaginatedResponse.create(
                items=items,
                total=total_records,
                params=params
            )

        except Exception as e:
            self.logger.error(f"Error listing assignments: {str(e)}")
            raise HTTPException(
                status_code=500,
                detail="Failed to list assignments"
            )

# Initialize API handler
customer_mo_api = CustomerMOAPI()

# Route definitions
@router.post("", response_model=CustomerMOResponse)
async def create_assignment(
    customer_mo: CustomerMOCreate,
    current_user: dict = Depends(get_current_user)
):
    """Assign a managed object to a customer"""
    return await customer_mo_api.create_assignment(customer_mo, current_user)

@router.patch("/{idMogid}", response_model=CustomerMOResponse)
async def update_assignment(
    idMogid: str,
    data: CustomerMOUpdate,
    current_user: dict = Depends(get_current_user)
):
    """Update a managed object assignment"""
    return await customer_mo_api.update_assignment(idMogid, data, current_user)

@router.get("", response_model=PaginatedResponse[CustomerMOResponse])
async def list_assignments(
    search: Optional[str] = None,
    customer_id: Optional[int] = None,
    page: int = Query(1, ge=1, description="Page number"),
    page_size: int = Query(10, ge=1, le=100, description="Items per page"),
    current_user: dict = Depends(get_current_user)
):
    """
    List managed object assignments with pagination
    - Optional search by managed object ID
    - Optional filter by customer ID
    - Includes managed object and customer names in response
    """
    return await customer_mo_api.list_assignments(search, customer_id, page, page_size)