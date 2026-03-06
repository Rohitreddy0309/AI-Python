from sqlalchemy.orm import Session
from repositories.plant_repository import PlantRepository
from schemas.schemas import PlantBulkUpdate, PlantCreate, PlantUpdate
from model.user import Plant
from utils.exceptions import NotFoundException


class PlantService:

    def __init__(self, db: Session):
        self.db = db
        self.repository = PlantRepository()

    def create_plant(self, plant_data: PlantCreate) -> Plant:
        plant = Plant(**plant_data.model_dump())
        return self.repository.create(self.db, plant)

    def get_plants(self) -> list[Plant]:
        return self.repository.get_all(self.db)

    def get_plant(self, plant_id: int) -> Plant:
        plant = self.repository.get_by_id(self.db, plant_id)

        if not plant:
            raise NotFoundException("Plant not found")

        return plant

    def update_plant(self, plant_id: int, updated_data: PlantCreate) -> Plant:

        plant = self.repository.get_by_id(self.db, plant_id)

        if not plant:
            raise NotFoundException("Plant not found")

        for key, value in updated_data.model_dump().items():
            setattr(plant, key, value)

        return self.repository.update(self.db, plant)

    def delete_plant(self, plant_id: int) -> None:

        plant = self.repository.get_by_id(self.db, plant_id)

        if not plant:
            raise NotFoundException("Plant not found")

        self.repository.delete(self.db, plant)

    def create_plants_bulk(self, plants_data: list[PlantCreate]) -> list[Plant]:

        plants_objects = [Plant(**data.model_dump()) for data in plants_data]

        return self.repository.create_bulk(self.db, plants_objects)

    def patch_plant(self, plant_id: int, updated_data: PlantUpdate) -> Plant:

        plant = self.repository.get_by_id(self.db, plant_id)

        if not plant:
            raise NotFoundException("Plant not found")

        update_dict = updated_data.model_dump(exclude_unset=True)

        for key, value in update_dict.items():
            setattr(plant, key, value)

        return self.repository.update(self.db, plant)

    def bulk_update_plants(self, plants_data: list[PlantBulkUpdate]) -> list[Plant]:

        updated_plants = []

        for plant_data in plants_data:

            plant = self.repository.get_by_id(self.db, plant_data.id)

            if not plant:
                raise NotFoundException(f"Plant with id {plant_data.id} not found")

            update_dict = plant_data.model_dump(exclude={"id"})

            for key, value in update_dict.items():
                setattr(plant, key, value)

            updated_plants.append(self.repository.update(self.db, plant))

        self.db.commit()

        for plant in updated_plants:
            self.db.refresh(plant)

        return updated_plants

    def bulk_delete_plants(self, plants_ids: list[int]) -> None:

        for plant_id in plants_ids:

            plant = self.db.query(Plant).filter(Plant.id == plant_id).first()

            if not plant:
                raise NotFoundException("No matching plants found")

            self.db.delete(plant)

        self.db.commit()