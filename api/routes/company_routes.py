from ..models.company_model import CompanyBase, CompanyCreate, CompanyUpdate, CompanyResponse
from fastapi import APIRouter, HTTPException, Depends, Query, status
from typing import List, Optional
from datetime import datetime
from data.database import DatabaseConnection
from utils.log import create_logger
from utils.auth import get_current_user
from ..models.alert_model import PaginatedResponse, PaginationParams

router = APIRouter(prefix="/api/Companys", tags=["Companys"])
logger = create_logger("Company_routes")

class CompanyAPI:
    def __init__(self):
        self.logger = logger.getChild(self.__class__.__name__)
        self.db = DatabaseConnection()
        self.db.connect()

    async def create_Company(self, Company: CompanyCreate, current_user: dict) -> CompanyResponse:
        try:
            # Check if Company exists
            result = self.db.execute_query(
                "SELECT idCompany FROM Companys WHERE emailContact = %s",
                (Company.emailContact,)
            )
            if result:
                raise HTTPException(
                    status_code=400,
                    detail="Email already registered"
                )

            query = """
                INSERT INTO Companys (
                    nameCompany, 
                    emailContact, 
                    phoneNumberContact, 
                    address, 
                    active, 
                    createdAt
                )
                VALUES (%s, %s, %s, %s, %s, %s)
                RETURNING 
                    idCompany, 
                    nameCompany, 
                    emailContact, 
                    phoneNumberContact, 
                    address, 
                    active, 
                    createdAt, 
                    updatedAt
            """
            
            # Convert boolean to database format
            values = (
                Company.nameCompany,
                Company.emailContact,                
                Company.phoneNumberContact,
                Company.address,
                Company.active,  # Now it's a boolean
                datetime.now()
            )

            self.logger.debug(f"Executing query with values: {values}")
            result = self.db.execute_query(query, values)
            
            if not result or not result[0]:
                raise HTTPException(
                    status_code=500,
                    detail="Failed to create company record"
                )
            
            # Map the returned columns to a dictionary
            columns = [
                'idCompany', 'nameCompany', 'emailContact', 
                'phoneNumberContact', 'address', 'active', 
                'createdAt', 'updatedAt'
            ]
            company_data = dict(zip(columns, result[0]))
            
            self.logger.debug(f"Created company data: {company_data}")
            return CompanyResponse(**company_data)

        except HTTPException:
            raise
        except Exception as e:
            self.logger.error(f"Error creating Company: {str(e)}", exc_info=True)
            raise HTTPException(
                status_code=500,
                detail=f"Failed to create Company: {str(e)}"
            )
        
        
    async def update_Company(self, idCompany: int, Company_data: CompanyUpdate, current_user: dict) -> CompanyResponse:
        try:
            update_fields = []
            values = []
            
            if Company_data.nameCompany is not None:
                update_fields.append("nameCompany = %s")
                values.append(Company_data.nameCompany)
            if Company_data.emailContact is not None:
                update_fields.append("emailContact = %s")
                values.append(Company_data.emailContact)
            # if Company_data.company is not None:
            #     update_fields.append("company = %s")
            #     values.append(Company_data.company)
            if Company_data.phoneNumberContact is not None:
                update_fields.append("phoneNumberContact = %s")
                values.append(Company_data.phoneNumberContact)
            if Company_data.address is not None:
                update_fields.append("address = %s")
                values.append(Company_data.address)
            if Company_data.active is not None:
                update_fields.append("active = %s")
                values.append(Company_data.active)

            if not update_fields:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="No fields to update"
                )

            update_fields.append("updatedAt = %s")
            values.append(datetime.now())
            values.append(idCompany)  # for WHERE clause

            query = f"""
                UPDATE Companys 
                SET {', '.join(update_fields)}
                WHERE idCompany = %s
                RETURNING idCompany, nameCompany, emailContact, phoneNumberContact, address, active, createdAt, updatedAt
            """
            
            result = self.db.execute_query(query, values)
            
            if not result:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="Company not found"
                )
                
            return CompanyResponse(**dict(zip(
                ['idCompany', 'nameCompany', 'emailContact', 'phoneNumberContact', 'address', 
                 'active', 'createdAt', 'updatedAt'],
                result[0]
            )))

        except HTTPException:
            raise
        except Exception as e:
            self.logger.error(f"Error updating Company: {str(e)}")
            raise HTTPException(status_code=500, detail="Failed to update Company")

    async def get_Company_by_id(self, idCompany: int) -> CompanyResponse:
        try:
            query = """
                SELECT idCompany, nameCompany, emailContact, phoneNumberContact, address, active, createdAt, updatedAt
                FROM Companys
                WHERE idCompany = %s
            """
            
            result = self.db.execute_query(query, (idCompany,))
            
            if not result:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="Company not found"
                )
                
            return CompanyResponse(**dict(zip(
                ['idCompany', 'nameCompany', 'emailContact', 'phoneNumberContact', 'address', 
                 'active', 'createdAt', 'updatedAt'],
                result[0]
            )))

        except HTTPException:
            raise
        except Exception as e:
            self.logger.error(f"Error fetching Company: {str(e)}")
            raise HTTPException(status_code=500, detail="Failed to fetch Company")

    async def search_Companys(
        self, 
        search: Optional[str] = None,
        page: int = 1, 
        page_size: int = 10
    ) -> PaginatedResponse[CompanyResponse]:
        try:
            params = PaginationParams(page=page, page_size=page_size)
            
            # Base query
            where_clause = "WHERE 1=1"
            query_params = []
            
            # Add search condition if search term is provided
            if search:
                where_clause += """ 
                    AND (
                        LOWER(nameCompany) LIKE LOWER(%s) OR 
                        LOWER(emailContact) LIKE LOWER(%s) 
                    )
                """
                search_term = f"%{search}%"
                query_params.extend([search_term, search_term, search_term])
            
            # Count total records
            count_query = f"SELECT COUNT(*) FROM Companys {where_clause}"
            count_result = self.db.execute_query(count_query, query_params)
            total_records = count_result[0][0] if count_result else 0
            
            # Main query with pagination
            query = f"""
                SELECT idCompany, nameCompany, emailContact, phoneNumberContact, address, active, createdAt, updatedAt
                FROM Companys
                {where_clause}
                ORDER BY nameCompany
                LIMIT %s OFFSET %s
            """
            
            final_params = tuple(query_params + [params.page_size, params.offset])
            result = self.db.execute_query(query, final_params)
            
            # Process results
            Companys = []
            columns = ['idCompany', 'nameCompany', 'emailContact', 'phoneNumberContact', 'address', 'active', 'createdAt', 'updatedAt']
            
            for row in result:
                Company_dict = dict(zip(columns, row))
                Companys.append(CompanyResponse(**Company_dict))
            
            return PaginatedResponse.create(
                items=Companys,
                total=total_records,
                params=params
            )

        except Exception as e:
            self.logger.error(f"Error searching Companys: {str(e)}")
            raise HTTPException(status_code=500, detail="Failed to search Companys")

# Initialize API handler
Company_api = CompanyAPI()

# Route definitions
@router.post("", response_model=CompanyResponse)
async def create_Company(
    Company: CompanyCreate,
    current_user: dict = Depends(get_current_user)
):
    """Create a new Company"""
    return await Company_api.create_Company(Company, current_user)

@router.patch("/{idCompany}", response_model=CompanyResponse)
async def update_Company(
    idCompany: int,
    Company_data: CompanyUpdate,
    current_user: dict = Depends(get_current_user)
):
    """Update an existing Company"""
    return await Company_api.update_Company(idCompany, Company_data, current_user)

@router.get("/{idCompany}", response_model=CompanyResponse)
async def get_Company(
    idCompany: int,
    current_user: dict = Depends(get_current_user)
):
    """Get a specific Company by ID"""
    return await Company_api.get_Company_by_id(idCompany)

@router.get("", response_model=PaginatedResponse[CompanyResponse])
async def search_Companys(
    search: Optional[str] = None,
    page: int = Query(1, ge=1, description="Page number"),
    page_size: int = Query(10, ge=1, le=100, description="Items per page"),
    current_user: dict = Depends(get_current_user)
):
    """
    Search Companys with pagination
    - Optional search term to filter by name, email or company
    - Pagination parameters
    """
    return await Company_api.search_Companys(search, page, page_size)
