from sqlalchemy.orm import Session
from model.user import Plant

class PlantRepository:

    def create(self, db: Session, plant: Plant) -> Plant:
        db.add(plant)
        db.commit()
        db.refresh(plant)
        return plant

    def get_all(self, db: Session):
        return db.query(Plant).all()

    def get_by_id(self, db: Session, plant_id: int):
        return db.query(Plant).filter(Plant.id == plant_id).first()

    def update(self, db: Session, plant: Plant):
        db.commit()
        db.refresh(plant)
        return plant

    def delete(self, db: Session, plant: Plant):
        db.delete(plant)
        db.commit()