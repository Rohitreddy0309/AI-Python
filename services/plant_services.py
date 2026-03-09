"""
Plant service layer.

This module contains business logic for plant-related operations.
It acts as an intermediary between the API routes and the repository
layer, handling validation, updates, and error handling.
"""

from sqlalchemy.orm import Session

from model.user import Plant
from repositories.plant_repository import PlantRepository
from schemas.schemas import PlantBulkUpdate, PlantCreate, PlantUpdate
from utils.exceptions import NotFoundException


class PlantService:
    """Service class responsible for plant-related business logic."""

    def __init__(self, db: Session):
        """
        Initialize PlantService.

        Args:
            db (Session): SQLAlchemy database session.
        """
        self.db = db
        self.repository = PlantRepository()

    def create_plant(self, plant_data: PlantCreate) -> Plant:
        """
        Create a new plant.

        Args:
            plant_data (PlantCreate): Plant creation data.

        Returns:
            Plant: Created plant object.
        """
        plant = Plant(**plant_data.model_dump())
        return self.repository.create(self.db, plant)

    def get_plants(self) -> list[Plant]:
        """
        Retrieve all plants.

        Returns:
            list[Plant]: List of plant records.
        """
        return self.repository.get_all(self.db)

    def get_plant(self, plant_id: int) -> Plant:
        """
        Retrieve a plant by its ID.

        Args:
            plant_id (int): Unique plant identifier.

        Returns:
            Plant: Plant object.

        Raises:
            NotFoundException: If the plant does not exist.
        """
        plant = self.repository.get_by_id(self.db, plant_id)

        if not plant:
            raise NotFoundException("Plant not found")

        return plant

    def update_plant(self, plant_id: int, updated_data: PlantCreate) -> Plant:
        """
        Update an existing plant.

        Args:
            plant_id (int): Plant identifier.
            updated_data (PlantCreate): Updated plant data.

        Returns:
            Plant: Updated plant object.
        """
        plant = self.repository.get_by_id(self.db, plant_id)

        if not plant:
            raise NotFoundException("Plant not found")

        for key, value in updated_data.model_dump().items():
            setattr(plant, key, value)

        return self.repository.update(self.db, plant)

    def delete_plant(self, plant_id: int) -> None:
        """
        Delete a plant by ID.

        Args:
            plant_id (int): Plant identifier.

        Raises:
            NotFoundException: If plant does not exist.
        """
        plant = self.repository.get_by_id(self.db, plant_id)

        if not plant:
            raise NotFoundException("Plant not found")

        self.repository.delete(self.db, plant)

    def create_plants_bulk(self, plants_data: list[PlantCreate]) -> list[Plant]:
        """
        Create multiple plants in bulk.

        Args:
            plants_data (list[PlantCreate]): List of plant creation data.

        Returns:
            list[Plant]: List of created plant objects.
        """
        plants_objects = [Plant(**data.model_dump()) for data in plants_data]
        return self.repository.create_bulk(self.db, plants_objects)

    def patch_plant(self, plant_id: int, updated_data: PlantUpdate) -> Plant:
        """
        Partially update a plant.

        Args:
            plant_id (int): Plant identifier.
            updated_data (PlantUpdate): Partial update data.

        Returns:
            Plant: Updated plant object.
        """
        plant = self.repository.get_by_id(self.db, plant_id)

        if not plant:
            raise NotFoundException("Plant not found")

        update_dict = updated_data.model_dump(exclude_unset=True)

        for key, value in update_dict.items():
            setattr(plant, key, value)

        return self.repository.update(self.db, plant)

    def bulk_update_plants(self, plants_data: list[PlantBulkUpdate]) -> list[Plant]:
        """
        Update multiple plants in bulk.

        Args:
            plants_data (list[PlantBulkUpdate]): List of plant update data.

        Returns:
            list[Plant]: List of updated plant objects.

        Raises:
            NotFoundException: If any plant ID does not exist.
        """
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
        """
        Delete multiple plants by their IDs.

        Args:
            plants_ids (list[int]): List of plant IDs to delete.

        Raises:
            NotFoundException: If any plant ID does not exist.
        """
        for plant_id in plants_ids:
            plant = self.db.query(Plant).filter(Plant.id == plant_id).first()

            if not plant:
                raise NotFoundException("No matching plants found")

            self.db.delete(plant)

        self.db.commit()
