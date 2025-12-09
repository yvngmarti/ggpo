from sqlalchemy.orm import Session
from app.models import ExpenseStatus


class ExpenseStatusRepository:
    @staticmethod
    def get_all(db: Session):
        return db.query(ExpenseStatus).all()

    @staticmethod
    def get_by_id(db: Session, expense_status_id: int):
        return (
            db.query(ExpenseStatus)
            .filter(ExpenseStatus.id == expense_status_id)
            .first()
        )

    @staticmethod
    def get_by_name(db: Session, expense_status_name: str):
        return (
            db.query(ExpenseStatus)
            .filter(ExpenseStatus.name == expense_status_name)
            .first()
        )

    @staticmethod
    def create(db: Session, expense_status: ExpenseStatus):
        db.add(expense_status)
        db.commit()
        db.refresh(expense_status)
        return expense_status

    @staticmethod
    def update(db: Session, expense_status: ExpenseStatus):
        db.commit()
        db.refresh(expense_status)
        return expense_status

    @staticmethod
    def delete(db: Session, expense_status: ExpenseStatus):
        db.delete(expense_status)
        db.commit()
        return expense_status
