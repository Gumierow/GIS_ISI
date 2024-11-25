from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy import update
import sys
from database import get_db
from .auth import get_current_user, is_employee
sys.path.append("backend")
import crud
import schemas
import models

router = APIRouter()

# Rota para criar um veículo (e sua localização)
@router.post("/create_vehicle/", response_model=schemas.Vehicle, dependencies=[Depends(is_employee)])
async def create_vehicle(
    vehicle: schemas.VehicleCreate,  
    db: AsyncSession = Depends(get_db),
    current_user: dict = Depends(get_current_user),
):
    # Cria a localização do veículo
    location_data = vehicle.location.dict()
    if isinstance(location_data.get("data_hora"), str):
        location_data["data_hora"] = datetime.strptime(location_data["data_hora"], "%Y-%m-%d").date()
    location = models.VehicleLocation(**location_data)
    db.add(location)
    await db.commit()
    await db.refresh(location)
    
    # Cria o veículo com a localização associada
    vehicle_data = vehicle.dict(exclude={"location"})
    vehicle_data["fk_id_localizacao"] = location.id  # Relaciona a localização com o veículo
    new_vehicle = models.Vehicle(**vehicle_data)
    
    db.add(new_vehicle)
    await db.commit()
    await db.refresh(new_vehicle)
    
    return new_vehicle

# Rota para obter todos os veículos
@router.get("/vehicles/", response_model=list[schemas.Vehicle], dependencies=[Depends(is_employee)])
async def get_all_vehicles(skip: int = 0, limit: int = 10, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(models.Vehicle).offset(skip).limit(limit))
    vehicles = result.scalars().all()
    if not vehicles:
        raise HTTPException(status_code=404, detail="Nenhum veículo encontrado.")
    return vehicles

# Rota para obter um veículo pelo ID
@router.get("/vehicle/{vehicle_id}", response_model=schemas.Vehicle, dependencies=[Depends(is_employee)])
async def get_vehicle_by_id(vehicle_id: int, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(models.Vehicle).where(models.Vehicle.id == vehicle_id))
    vehicle = result.scalars().first()
    if not vehicle:
        raise HTTPException(status_code=404, detail="Veículo não encontrado.")
    return vehicle

# Rota para criar uma localização para um veículo existente
@router.post("/vehicle_location/", response_model=schemas.VehicleLocation, dependencies=[Depends(is_employee)])
async def create_vehicle_location(
    location: schemas.VehicleLocationCreate,
    db: AsyncSession = Depends(get_db),
):
    db_location = models.VehicleLocation(**location.dict())
    db.add(db_location)
    await db.commit()
    await db.refresh(db_location)
    return db_location

# Rota para obter a localização pelo ID
@router.get("/vehicle_location/{location_id}", response_model=schemas.VehicleLocation, dependencies=[Depends(is_employee)])
async def get_vehicle_location_by_id(location_id: int, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(models.VehicleLocation).where(models.VehicleLocation.id == location_id))
    location = result.scalars().first()
    if not location:
        raise HTTPException(status_code=404, detail="Localização não encontrada.")
    return location

# Rota para atualizar a localização de um veículo
@router.put("/vehicle_location/{location_id}", response_model=schemas.VehicleLocation, dependencies=[Depends(is_employee)])
async def update_vehicle_location(
    location_id: int,
    location_update: schemas.VehicleLocationUpdate,
    db: AsyncSession = Depends(get_db),
):
    result = await db.execute(select(models.VehicleLocation).where(models.VehicleLocation.id == location_id))
    db_location = result.scalars().first()
    if not db_location:
        raise HTTPException(status_code=404, detail="Localização não encontrada.")

    # Atualiza os campos da localização
    for key, value in location_update.dict(exclude_unset=True).items():
        setattr(db_location, key, value)

    await db.commit()
    await db.refresh(db_location)
    return db_location
