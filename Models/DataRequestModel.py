
from pydantic import BaseModel


class DataRequestModel(BaseModel):
    county: str
    origin: str
    createdAt: str
    createdAtMonth: int
    createdAtYear: int
    status: str
    price: int
    pricePerAcre: float
    area: float
    acre: float
    bedrooms: int
    bathrooms: int
    electricity: bool
    waterfront: bool
    mineral: bool
    well: bool
    agExempt: bool
    link: str
