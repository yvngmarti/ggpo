from sqlalchemy.orm import Session
from app.models import TransactionType


class TransactionTypeRepository:
    @staticmethod
    def get_all(db: Session):
        return db.query(TransactionType).all()

    @staticmethod
    def get_by_id(db: Session, transaction_type_id: int):
        return (
            db.query(TransactionType)
            .filter(TransactionType.id == transaction_type_id)
            .first()
        )

    @staticmethod
    def get_by_name(db: Session, transaction_type_name: str):
        return (
            db.query(TransactionType)
            .filter(TransactionType.name == transaction_type_name)
            .first()
        )

    @staticmethod
    def create(db: Session, transaction_type: TransactionType):
        db.add(transaction_type)
        db.commit()
        db.refresh(transaction_type)
        return transaction_type

    @staticmethod
    def update(db: Session, transaction_type: TransactionType):
        db.commit()
        db.refresh(transaction_type)
        return transaction_type

    @staticmethod
    def delete(db: Session, transaction_type: TransactionType):
        db.delete(transaction_type)
        db.commit()
        return transaction_type
