from pydantic import BaseModel


class AirportBase(BaseModel):

    iata_code: str
    name: str | None
    icao_code: str | None = None
    latitude: float | None = None
    longitude: float | None = None
    city: str


class AirportCreate(AirportBase):
    pass
