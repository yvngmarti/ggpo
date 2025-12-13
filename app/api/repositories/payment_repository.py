from sqlalchemy.orm import Session
from app.models import Payment


class PaymentRepository:
    @staticmethod
    def get_all(db: Session):
        return db.query(Payment).order_by(Payment.updated_at.desc()).all()

    @staticmethod
    def get_by_id(db: Session, payment_id: int):
        return db.query(Payment).filter(Payment.id == payment_id).first()

    @staticmethod
    def get_by_expense_id(db: Session, expense_id: int):
        return db.query(Payment).filter(Payment.expense_id == expense_id).first()

    @staticmethod
    def create(db: Session, payment: Payment):
        db.add(payment)
        db.commit()
        db.refresh(payment)
        return payment

    @staticmethod
    def update(db: Session, payment: Payment):
        db.commit()
        db.refresh(payment)
        return payment
