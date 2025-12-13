from sqlalchemy.orm import Session
from app.models import BankAccount


class BankAccountRepository:
    @staticmethod
    def get_all(db: Session):
        return db.query(BankAccount).order_by(BankAccount.id).all()

    @staticmethod
    def get_by_id(db: Session, account_id: int):
        return db.query(BankAccount).filter(BankAccount.id == account_id).first()

    @staticmethod
    def get_by_account_number(db: Session, account_number: str):
        return (
            db.query(BankAccount)
            .filter(BankAccount.account_number == account_number)
            .first()
        )

    @staticmethod
    def create(db: Session, bank_account: BankAccount):
        db.add(bank_account)
        db.commit()
        db.refresh(bank_account)
        return bank_account

    @staticmethod
    def update(db: Session, bank_account: BankAccount):
        db.commit()
        db.refresh(bank_account)
        return bank_account
