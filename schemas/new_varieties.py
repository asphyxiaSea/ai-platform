from pydantic import BaseModel

class NewVarieties(BaseModel):
    variety_name:str=""
    variety_right_number:str=""
    variety_status:str=""
    application_date:str=""
    authorization_date:str=""
    right_holders:str=""
    breeders:str=""
    attachments:str=""
    review_process_records:str=""

