"""
Plant repository layer.

This module provides database operations for the Plant model.
It encapsulates CRUD operations and interacts directly with
the SQLAlchemy session.
"""

from sqlalchemy.orm import Session

from model.user import Plant


class PlantRepository:
    """Repository class responsible for plant database operations."""

    def create(self, db: Session, plant: Plant) -> Plant:
        """
        Create a new plant record in the database.

        Args:
            db (Session): Database session.
            plant (Plant): Plant ORM object.

        Returns:
            Plant: Created plant instance.
        """
        db.add(plant)
        db.commit()
        db.refresh(plant)
        return plant

    def get_all(self, db: Session):
        """
        Retrieve all plant records.

        Args:
            db (Session): Database session.

        Returns:
            list[Plant]: List of plant records.
        """
        return db.query(Plant).all()

    def get_by_id(self, db: Session, plant_id: int):
        """
        Retrieve a plant by its ID.

        Args:
            db (Session): Database session.
            plant_id (int): Unique plant identifier.

        Returns:
            Plant | None: Plant record if found, otherwise None.
        """
        return db.query(Plant).filter(Plant.id == plant_id).first()

    def update(self, db: Session, plant: Plant):
        """
        Update an existing plant record.

        Args:
            db (Session): Database session.
            plant (Plant): Plant ORM object with updated values.

        Returns:
            Plant: Updated plant instance.
        """
        db.commit()
        db.refresh(plant)
        return plant

    def delete(self, db: Session, plant: Plant):
        """
        Delete a plant record.

        Args:
            db (Session): Database session.
            plant (Plant): Plant ORM object to delete.
        """
        db.delete(plant)
        db.commit()

    def create_bulk(self, db: Session, plants: list[Plant]) -> list[Plant]:
        """
        Create multiple plant records in bulk.

        Args:
            db (Session): Database session.
            plants (list[Plant]): List of plant ORM objects.

        Returns:
            list[Plant]: List of created plant records.
        """
        db.add_all(plants)
        db.commit()
        for plant in plants:
            db.refresh(plant)
        return plants
