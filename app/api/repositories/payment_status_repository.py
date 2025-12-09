from sqlalchemy.orm import Session
from app.models import PaymentStatus


class PaymentStatusRepository:
    @staticmethod
    def get_all(db: Session):
        return db.query(PaymentStatus).all()

    @staticmethod
    def get_by_id(db: Session, payment_status_id: int):
        return (
            db.query(PaymentStatus)
            .filter(PaymentStatus.id == payment_status_id)
            .first()
        )

    @staticmethod
    def get_by_name(db: Session, payment_status_name: str):
        return (
            db.query(PaymentStatus)
            .filter(PaymentStatus.name == payment_status_name)
            .first()
        )

    @staticmethod
    def create(db: Session, payment_status: PaymentStatus):
        db.add(payment_status)
        db.commit()
        db.refresh(payment_status)
        return payment_status

    @staticmethod
    def update(db: Session, payment_status: PaymentStatus):
        db.commit()
        db.refresh(payment_status)
        return payment_status

    @staticmethod
    def delete(db: Session, payment_status: PaymentStatus):
        db.delete(payment_status)
        db.commit()
        return payment_status
