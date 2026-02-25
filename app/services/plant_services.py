from sqlalchemy.orm import Session
from app.repositories.plant_repository import PlantRepository
from app.schemas.schemas import PlantCreate
from app.models.models import Plant
from app.utils.exception import NotFoundException


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