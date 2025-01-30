from ..models.customer_model import CustomerBase, CustomerCreate, CustomerUpdate, CustomerResponse
from fastapi import APIRouter, HTTPException, Depends, Query, status
from typing import List, Optional
from datetime import datetime
from data.database import DatabaseConnection
from utils.log import create_logger
from utils.auth import get_current_user
from ..models.alert_model import PaginatedResponse, PaginationParams

router = APIRouter(prefix="/api/customers", tags=["customers"])
logger = create_logger("customer_routes")

class CustomerAPI:
    def __init__(self):
        self.logger = logger.getChild(self.__class__.__name__)
        self.db = DatabaseConnection()
        self.db.connect()

    async def create_customer(self, customer: CustomerCreate, current_user: dict) -> CustomerResponse:
        try:
            # Check if customer exists
            result = self.db.execute_query(
                "SELECT idCustomer FROM customers WHERE email = %s",
                (customer.email,)
            )
            if result:
                raise HTTPException(
                    status_code=400,
                    detail="Email already registered"
                )

            query = """
                INSERT INTO customers (name, email, company, phoneNumber, address, status, createdAt)
                VALUES (%s, %s, %s, %s, %s, %s, %s)
                RETURNING idCustomer, name, email, company, phoneNumber, address, status, createdAt, updatedAt
            """
            
            values = (
                customer.name,
                customer.email,
                customer.company,
                customer.phoneNumber,
                customer.address,
                customer.status,
                datetime.now()
            )

            result = self.db.execute_query(query, values)
            
            return CustomerResponse(**dict(zip(
                ['idCustomer', 'name', 'email', 'company', 'phoneNumber', 'address', 
                 'status', 'createdAt', 'updatedAt'],
                result[0]
            )))

        except Exception as e:
            self.logger.error(f"Error creating customer: {str(e)}")
            raise HTTPException(status_code=500, detail="Failed to create customer")

    async def update_customer(self, idCustomer: int, customer_data: CustomerUpdate, current_user: dict) -> CustomerResponse:
        try:
            update_fields = []
            values = []
            
            if customer_data.name is not None:
                update_fields.append("name = %s")
                values.append(customer_data.name)
            if customer_data.email is not None:
                update_fields.append("email = %s")
                values.append(customer_data.email)
            if customer_data.company is not None:
                update_fields.append("company = %s")
                values.append(customer_data.company)
            if customer_data.phoneNumber is not None:
                update_fields.append("phoneNumber = %s")
                values.append(customer_data.phoneNumber)
            if customer_data.address is not None:
                update_fields.append("address = %s")
                values.append(customer_data.address)
            if customer_data.status is not None:
                update_fields.append("status = %s")
                values.append(customer_data.status)

            if not update_fields:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="No fields to update"
                )

            update_fields.append("updatedAt = %s")
            values.append(datetime.now())
            values.append(idCustomer)  # for WHERE clause

            query = f"""
                UPDATE customers 
                SET {', '.join(update_fields)}
                WHERE idCustomer = %s
                RETURNING idCustomer, name, email, company, phoneNumber, address, status, createdAt, updatedAt
            """
            
            result = self.db.execute_query(query, values)
            
            if not result:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="Customer not found"
                )
                
            return CustomerResponse(**dict(zip(
                ['idCustomer', 'name', 'email', 'company', 'phoneNumber', 'address', 
                 'status', 'createdAt', 'updatedAt'],
                result[0]
            )))

        except HTTPException:
            raise
        except Exception as e:
            self.logger.error(f"Error updating customer: {str(e)}")
            raise HTTPException(status_code=500, detail="Failed to update customer")

    async def get_customer_by_id(self, idCustomer: int) -> CustomerResponse:
        try:
            query = """
                SELECT idCustomer, name, email, company, phoneNumber, address, status, createdAt, updatedAt
                FROM customers
                WHERE idCustomer = %s
            """
            
            result = self.db.execute_query(query, (idCustomer,))
            
            if not result:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="Customer not found"
                )
                
            return CustomerResponse(**dict(zip(
                ['idCustomer', 'name', 'email', 'company', 'phoneNumber', 'address', 
                 'status', 'createdAt', 'updatedAt'],
                result[0]
            )))

        except HTTPException:
            raise
        except Exception as e:
            self.logger.error(f"Error fetching customer: {str(e)}")
            raise HTTPException(status_code=500, detail="Failed to fetch customer")

    async def search_customers(
        self, 
        search: Optional[str] = None,
        page: int = 1, 
        page_size: int = 10
    ) -> PaginatedResponse[CustomerResponse]:
        try:
            params = PaginationParams(page=page, page_size=page_size)
            
            # Base query
            where_clause = "WHERE 1=1"
            query_params = []
            
            # Add search condition if search term is provided
            if search:
                where_clause += """ 
                    AND (
                        LOWER(name) LIKE LOWER(%s) OR 
                        LOWER(email) LIKE LOWER(%s) OR 
                        LOWER(company) LIKE LOWER(%s)
                    )
                """
                search_term = f"%{search}%"
                query_params.extend([search_term, search_term, search_term])
            
            # Count total records
            count_query = f"SELECT COUNT(*) FROM customers {where_clause}"
            count_result = self.db.execute_query(count_query, query_params)
            total_records = count_result[0][0] if count_result else 0
            
            # Main query with pagination
            query = f"""
                SELECT idCustomer, name, email, company, phoneNumber, address, status, createdAt, updatedAt
                FROM customers
                {where_clause}
                ORDER BY name
                LIMIT %s OFFSET %s
            """
            
            final_params = tuple(query_params + [params.page_size, params.offset])
            result = self.db.execute_query(query, final_params)
            
            # Process results
            customers = []
            columns = ['idCustomer', 'name', 'email', 'company', 'phoneNumber', 'address', 
                      'status', 'createdAt', 'updatedAt']
            
            for row in result:
                customer_dict = dict(zip(columns, row))
                customers.append(CustomerResponse(**customer_dict))
            
            return PaginatedResponse.create(
                items=customers,
                total=total_records,
                params=params
            )

        except Exception as e:
            self.logger.error(f"Error searching customers: {str(e)}")
            raise HTTPException(status_code=500, detail="Failed to search customers")

# Initialize API handler
customer_api = CustomerAPI()

# Route definitions
@router.post("", response_model=CustomerResponse)
async def create_customer(
    customer: CustomerCreate,
    current_user: dict = Depends(get_current_user)
):
    """Create a new customer"""
    return await customer_api.create_customer(customer, current_user)

@router.patch("/{idCustomer}", response_model=CustomerResponse)
async def update_customer(
    idCustomer: int,
    customer_data: CustomerUpdate,
    current_user: dict = Depends(get_current_user)
):
    """Update an existing customer"""
    return await customer_api.update_customer(idCustomer, customer_data, current_user)

@router.get("/{idCustomer}", response_model=CustomerResponse)
async def get_customer(
    idCustomer: int,
    current_user: dict = Depends(get_current_user)
):
    """Get a specific customer by ID"""
    return await customer_api.get_customer_by_id(idCustomer)

@router.get("", response_model=PaginatedResponse[CustomerResponse])
async def search_customers(
    search: Optional[str] = None,
    page: int = Query(1, ge=1, description="Page number"),
    page_size: int = Query(10, ge=1, le=100, description="Items per page"),
    current_user: dict = Depends(get_current_user)
):
    """
    Search customers with pagination
    - Optional search term to filter by name, email or company
    - Pagination parameters
    """
    return await customer_api.search_customers(search, page, page_size)
