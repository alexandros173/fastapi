
from typing import List, Annotated

from fastapi import FastAPI, Path, HTTPException, Depends, Query
from sqlalchemy.orm import Session
from starlette.responses import RedirectResponse

import model
from model.airport import Airport
from database import SessionLocal, engine
from model.schemas import AirportBase

model.airport.Base.metadata.create_all(bind=engine)

app = FastAPI()


def get_db():
    try:
        db = SessionLocal()
        yield db
    finally:
        db.close()


@app.get("/")
def main():
    return RedirectResponse(url="/docs/")


@app.get("/airports/", response_model=List[AirportBase])
def get_airports(db: Session = Depends(get_db)) -> List[AirportBase]:
    return db.query(Airport).all()


@app.get('/airport/{code}',
         responses={404: {'description': 'Airport not found'}})
def get_airport(code: str = Path(description='IATA Airport Code'), db: Session = Depends(get_db)) -> AirportBase:

    airport = db.query(Airport).filter(Airport.iata_code == code.upper()).first()
    if airport:
        return AirportBase(name=airport.name,
                           iata_code=airport.iata_code,
                           icao_code=airport.icao_code,
                           latitude=airport.latitude,
                           longitude=airport.longitude,
                           city=airport.city)

    raise HTTPException(status_code=404, detail=f'Airport code: {code} not found')


@app.post('/airport', status_code=201)
async def create_airport(iata_code: Annotated[str, Query(description='IATA Airport code', max_length=3)],
                         name: Annotated[str, Query(description='Airport name', max_length=250)],
                         city: Annotated[str, Query(description='City name', max_length=30)],
                         icao_code: Annotated[str | None, Query(description='ICAO Airport code', max_length=4)] = None,
                         latitude: Annotated[float | None, Query()] = None,
                         longitude: Annotated[float | None, Query()] = None,
                         db: Session = Depends(get_db)):
    airport = db.query(Airport).filter(Airport.iata_code == iata_code.upper()).first()
    if not airport:
        new_airport = Airport(iata_code=iata_code.upper(), name=name, city=city,
                              icao_code=icao_code, latitude=latitude, longitude=longitude)
        db.add(new_airport)
        db.commit()
        db.refresh(new_airport)
        return new_airport

    raise HTTPException(status_code=409, detail='Airport already exists in DB')


@app.delete('/airport', status_code=204)
async def delete_airport(iata_code: Annotated[str, Query(description='IATA Airport code', max_length=3)],
                         db: Session = Depends(get_db)):
    airport = db.query(Airport).filter(Airport.iata_code == iata_code.upper()).first()
    if not airport:
        raise HTTPException(status_code=404, detail=f'Airport code: {iata_code} not found')

    db.delete(airport)
    db.commit()

