from sqlalchemy.orm import Session
from models.student import Student  


class StudentRepository:
    """Database access layer for Student."""
#create ------------------------------------------------------------
    def create_many(self, db: Session, students: list[Student]):
        db.add_all(students)
        db.commit()
        for student in students:
            db.refresh(student)
        return students


#Read ---------------------------------------------------------

    def get_all(self, db: Session):
        return db.query(Student).all()

    def get_by_id(self, db: Session, student_id: int):
        return db.query(Student).filter(Student.id == student_id).first()

    def get_by_ids(self, db: Session, ids: list[int]):
        return db.query(Student).filter(Student.id.in_(ids)).all()
    
    def get_all_active(self, db: Session):
        return db.query(Student).filter(Student.is_active == True).all()

    def get_by_email(self, db: Session, email: str):
        return db.query(Student).filter(Student.email == email).first()
#update--------------------------------------------------------------

    def update_many(self, db: Session, students: list[Student]):
        """Persist changes to an existing student."""
        db.commit()
        for student in students:
            db.refresh(student)
        return students