from pydantic import BaseModel

class Patent(BaseModel):
    patent_name: str = ""
    patent_type: str = ""
    application_year: str = ""
    grant_year: str = ""
    transfer_year: str = ""
    invalid_year: str = ""
    inventors: str = ""
    patentees: str = ""
    legal_status: str = ""
    patent_number: str = ""
    application_date: str = ""
    reviewer: str = ""
