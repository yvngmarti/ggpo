from sqlalchemy.orm import Session
from app.models import BankTransaction


class BankTransactionRepository:
    @staticmethod
    def get_all(db: Session):
        return (
            db.query(BankTransaction).order_by(BankTransaction.created_at.desc()).all()
        )

    @staticmethod
    def get_by_id(db: Session, transaction_id: int):
        return (
            db.query(BankTransaction)
            .filter(BankTransaction.id == transaction_id)
            .first()
        )

    @staticmethod
    def get_by_account(db: Session, bank_account_id: int):
        return (
            db.query(BankTransaction)
            .filter(BankTransaction.bank_account_id == bank_account_id)
            .all()
        )

    @staticmethod
    def create(db: Session, transaction: BankTransaction):
        db.add(transaction)
        db.commit()
        db.refresh(transaction)
        return transaction
