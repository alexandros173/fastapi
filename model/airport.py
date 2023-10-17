from sqlalchemy import Column, Integer, String, Float

from database import Base


class Airport(Base):
    __tablename__ = 'airport'

    iata_code = Column(String, primary_key=True)
    name = Column(String(250))
    icao_code = Column(String)
    latitude = Column(Float)
    longitude = Column(Float)
    city = Column(String)
