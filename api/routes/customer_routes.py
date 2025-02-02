from ..models.customer_model import CustomerBase, CustomerCreate, CustomerUpdate, CustomerResponse
from fastapi import APIRouter, HTTPException, Depends, Query, status
from typing import List, Optional
from datetime import datetime
from data.database import DatabaseConnection
from utils.log import create_logger
from utils.auth import get_current_user
from ..models.alert_model import PaginatedResponse, PaginationParams

router = APIRouter(prefix="/api/customers", tags=["Customers"])
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
                "SELECT idCustomer FROM customers WHERE emailContact = %s",
                (customer.emailContact,)
            )
            if result:
                raise HTTPException(
                    status_code=400,
                    detail="Email already registered"
                )

            # Verify if company exists
            company_result = self.db.execute_query(
                "SELECT idCompany FROM companys WHERE idCompany = %s",
                (customer.idCompany,)
            )
            if not company_result:
                raise HTTPException(
                    status_code=404,
                    detail=f"Company with ID {customer.idCompany} not found"
                )

            query = """
                INSERT INTO customers (
                    nameCustomer, 
                    emailContact, 
                    phoneNumberContact, 
                    address, 
                    active,
                    idCompany,
                    createdAt
                )
                VALUES (%s, %s, %s, %s, %s, %s, %s)
                RETURNING 
                    idCustomer, 
                    nameCustomer, 
                    emailContact, 
                    phoneNumberContact, 
                    address, 
                    active,
                    idCompany,
                    createdAt, 
                    updatedAt
            """
            
            values = (
                customer.nameCustomer,
                customer.emailContact,                
                customer.phoneNumberContact,
                customer.address,
                customer.active,
                customer.idCompany,
                datetime.now()
            )

            self.logger.debug(f"Executing query with values: {values}")
            result = self.db.execute_query(query, values)
            
            if not result or not result[0]:
                raise HTTPException(
                    status_code=500,
                    detail="Failed to create customer record"
                )
            
            # Map the returned columns to a dictionary
            columns = [
                'idCustomer', 'nameCustomer', 'emailContact', 
                'phoneNumberContact', 'address', 'active', 
                'idCompany', 'createdAt', 'updatedAt'
            ]
            customer_data = dict(zip(columns, result[0]))
            
            self.logger.debug(f"Created customer data: {customer_data}")
            return CustomerResponse(**customer_data)

        except HTTPException:
            raise
        except Exception as e:
            self.logger.error(f"Error creating customer: {str(e)}", exc_info=True)
            raise HTTPException(
                status_code=500,
                detail=f"Failed to create customer: {str(e)}"
            )
        
        
    async def update_customer(self, idCustomer: int, customer_data: CustomerUpdate, current_user: dict) -> CustomerResponse:
        try:
            update_fields = []
            values = []
            
            # Check if customer exists first
            check_result = self.db.execute_query(
                "SELECT idCustomer FROM customers WHERE idCustomer = %s",
                (idCustomer,)
            )
            if not check_result:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="Customer not found"
                )
            
            if customer_data.nameCustomer is not None:
                update_fields.append("nameCustomer = %s")
                values.append(customer_data.nameCustomer)

            if customer_data.emailContact is not None:
                # Check if email is already used by another customer
                email_check = self.db.execute_query(
                    "SELECT idCustomer FROM customers WHERE emailContact = %s AND idCustomer != %s",
                    (customer_data.emailContact, idCustomer)
                )
                if email_check:
                    raise HTTPException(
                        status_code=400,
                        detail="Email already registered for another customer"
                    )
                update_fields.append("emailContact = %s")
                values.append(customer_data.emailContact)

            if customer_data.phoneNumberContact is not None:
                update_fields.append("phoneNumberContact = %s")
                values.append(customer_data.phoneNumberContact)

            if customer_data.address is not None:
                update_fields.append("address = %s")
                values.append(customer_data.address)

            if customer_data.active is not None:
                update_fields.append("active = %s")
                values.append(customer_data.active)

            if customer_data.idCompany is not None:
                # Verify if company exists
                company_result = self.db.execute_query(
                    "SELECT idCompany FROM companys WHERE idCompany = %s",
                    (customer_data.idCompany,)
                )
                if not company_result:
                    raise HTTPException(
                        status_code=404,
                        detail=f"Company with ID {customer_data.idCompany} not found"
                    )
                update_fields.append("idCompany = %s")
                values.append(customer_data.idCompany)

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
                RETURNING 
                    idCustomer, 
                    nameCustomer, 
                    emailContact, 
                    phoneNumberContact, 
                    address, 
                    active,
                    idCompany, 
                    createdAt, 
                    updatedAt
            """
            
            self.logger.debug(f"Executing update query: {query}")
            self.logger.debug(f"Update values: {values}")
            
            result = self.db.execute_query(query, values)
            
            if not result:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="Customer not found"
                )
            
            # Map the returned columns to a dictionary
            columns = [
                'idCustomer', 'nameCustomer', 'emailContact', 
                'phoneNumberContact', 'address', 'active',
                'idCompany', 'createdAt', 'updatedAt'
            ]
            customer_data = dict(zip(columns, result[0]))
            
            self.logger.debug(f"Updated customer data: {customer_data}")
            return CustomerResponse(**customer_data)

        except HTTPException:
            raise
        except Exception as e:
            self.logger.error(f"Error updating customer: {str(e)}", exc_info=True)
            raise HTTPException(
                status_code=500,
                detail=f"Failed to update customer: {str(e)}"
            )
        
        
    async def get_customer_by_id(self, idCustomer: int) -> CustomerResponse:
        try:
            query = """
                SELECT idCustomer, nameCustomer, emailContact, phoneNumberContact, address, active, createdAt, updatedAt
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
                ['idCustomer', 'nameCustomer', 'emailContact', 'phoneNumberContact', 'address', 
                 'active', 'createdAt', 'updatedAt'],
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
                        LOWER(nameCustomer) LIKE LOWER(%s) OR 
                        LOWER(emailContact) LIKE LOWER(%s) 
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
                SELECT idCustomer, nameCustomer, emailContact, phoneNumberContact, address, active, createdAt, updatedAt
                FROM customers
                {where_clause}
                ORDER BY nameCustomer
                LIMIT %s OFFSET %s
            """
            
            final_params = tuple(query_params + [params.page_size, params.offset])
            result = self.db.execute_query(query, final_params)
            
            # Process results
            customers = []
            columns = ['idCustomer', 'nameCustomer', 'emailContact', 'phoneNumberContact', 'address', 'active', 'createdAt', 'updatedAt']
            
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
