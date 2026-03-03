from sqlalchemy.orm import Session
from repositories.plant_repository import PlantRepository
from schemas.schemas import PlantBulkUpdate, PlantCreate, PlantUpdate
from model.user import Plant
from utils.exception import NotFoundException


class PlantService:

    def __init__(self) -> None:
        self.repository = PlantRepository()

    def create_plant(self, db: Session, plant_data: PlantCreate) -> Plant:
        plant = Plant(**plant_data.model_dump())
        return self.repository.create(db, plant)

    def get_plants(self, db: Session) -> list[Plant]:
        return self.repository.get_all(db)

    def get_plant(self, db: Session, plant_id: int) -> Plant:
        plant = self.repository.get_by_id(db, plant_id)
        if not plant:
            raise NotFoundException("Plant not found")
        return plant

    def update_plant(
        self, db: Session, plant_id: int, updated_data: PlantCreate
    ) -> Plant:
        plant = self.repository.get_by_id(db, plant_id)
        if not plant:
            raise NotFoundException("Plant not found")

        for key, value in updated_data.model_dump().items():
            setattr(plant, key, value)

        return self.repository.update(db, plant)

    def delete_plant(self, db: Session, plant_id: int) -> None:
        plant = self.repository.get_by_id(db, plant_id)
        if not plant:
            raise NotFoundException("Plant not found")

        self.repository.delete(db, plant)
      
    def create_plants_bulk(self, db: Session, plants_data: list[PlantCreate]) -> list[Plant]:
        plants_objects = [Plant(**data.model_dump()) for data in plants_data]
        return self.repository.create_bulk(db, plants_objects)   
   
    def patch_plant(self, db: Session, plant_id: int, updated_data: PlantUpdate) -> Plant:
        plant = self.repository.get_by_id(db, plant_id)
        
        if not plant:
            raise NotFoundException("plant not found")
        
        update_dict = updated_data.model_dump(exclude_unset=True)
        for key, value in update_dict.items():
            setattr(plant, key, value)
            return self.repository.update(db, plant)
        
    def bulk_update_plants(self, db: Session, plants_data: list[PlantBulkUpdate]) -> list[Plant]:
        updated_plants = []
        for plants_data in plants_data:
            plant = self.repository.get_by-id(db, plants_data.id)
            if not plant:
                raise NotFoundException(f"plant with id {plants_data.id} not found")
            update_dict = plants_data.model_dump(exclude={"id"})
            for key, value in update_dict.items():
                setattr(plant, key, value)
            updated_plants.append(self.repository.update(db, plant))
        db.commit()
        for plants in updated_plants:
            db.refresh(plants)
                
        return updated_plants
    
    def bulk_delete_plants(self, db: Session, plants_ids: list[int]) -> None:
        for plant_id in plants_ids:
            plants = db.query(Plant).filter(Plant.id == plant_id).first()
            if not plants:raise NotFoundException("No matching plants found")
            db.delete(plants)
        db.commit()
            
    