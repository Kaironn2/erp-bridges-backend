from typing import Optional, TypedDict

from company.models import Company


class CompanyDataType(TypedDict, total=False):
    cnpj: str
    name: Optional[str]
    email: Optional[str]
    ie: Optional[str]
    phone: Optional[str]
    address: Optional[str]
    city: Optional[str]
    state: Optional[str]
    country: Optional[str]


class CompanyRepository:
    def find_by_cnpj(self, cnpj: str) -> Optional[Company]:
        try:
            return Company.objects.get(cnpj=cnpj)
        except Company.DoesNotExist:
            return None

    def get_or_create(self, company_data: CompanyDataType) -> Company:
        obj, created = Company.objects.get_or_create(**company_data)
        return obj
