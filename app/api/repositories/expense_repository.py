from sqlalchemy.orm import Session
from app.models import Expense


class ExpenseRepository:
    @staticmethod
    def get_all(db: Session):
        return db.query(Expense).order_by(Expense.updated_at.desc()).all()

    @staticmethod
    def get_by_id(db: Session, expense_id: int):
        return db.query(Expense).filter(Expense.id == expense_id).first()

    @staticmethod
    def get_by_project(db: Session, project_id: int):
        return db.query(Expense).filter(Expense.project_id == project_id).all()

    @staticmethod
    def create(db: Session, expense: Expense):
        db.add(expense)
        db.commit()
        db.refresh(expense)
        return expense

    @staticmethod
    def update(db: Session, expense: Expense):
        db.commit()
        db.refresh(expense)
        return expense
