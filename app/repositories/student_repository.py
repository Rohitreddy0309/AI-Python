from sqlalchemy.orm import Session
from app.models.student import Student

class StudentRepository:
 
    def get_lowest_available_id(self, db: Session):
        ids = db.query(Student.id).order_by(Student.id).all()

        expected = 1
        for (id_val,) in ids:
            if id_val != expected:
                return expected
            expected += 1

        return expected
    
    def create_student(self, db: Session, name: str, age: int, marks: int):
        new_id = self.get_lowest_available_id(db)
        student = Student(id=new_id, name=name, age=age, marks=marks)
        db.add(student)
        db.commit()
        db.refresh(student)
        return student

    def get_all_students(self, db: Session):
        return db.query(Student).all()

    def get_student(self, db: Session, student_id: int):
        return db.query(Student).filter(Student.id == student_id).first()

    def get_student(self, db: Session, student_id: int):
        return db.query(Student).filter(Student.id == student_id).first()

    def update_student(self, db: Session, student, name: str, age: int, marks: int):
        student.name = name
        student.age = age
        student.marks = marks
        db.commit()
        db.refresh(student)
        return student

    def delete_student(self, db: Session, student):
        db.delete(student)
        db.commit()