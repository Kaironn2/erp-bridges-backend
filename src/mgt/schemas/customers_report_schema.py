from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Field


class CustomerReportData(BaseModel):
    customer_external_id: str = Field(alias='ID')
    first_name: str = Field(alias='Firstname')
    last_name: str = Field(alias='Lastname')
    email: str = Field(alias='E-mail')
    customer_group: str = Field(alias='Grupo')
    phone: Optional[str] = Field(alias='Telefone')
    cep: Optional[str] = Field(alias='CEP')
    state: Optional[str] = Field(alias='Estado')
    country: Optional[str] = Field(alias='País')
    customer_since: datetime = Field(alias='Cliente Desde')

    class Config:
        populate_by_name = True
