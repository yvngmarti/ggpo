from sqlalchemy.orm import Session
from app.models import Provider


class ProviderRepository:
    @staticmethod
    def get_all(db: Session):
        return db.query(Provider).all()

    @staticmethod
    def get_by_id(db: Session, provider_id: int):
        return db.query(Provider).filter(Provider.id == provider_id).first()

    @staticmethod
    def get_by_rfc(db: Session, rfc: str):
        return db.query(Provider).filter(Provider.rfc == rfc).first()

    @staticmethod
    def create(db: Session, provider: Provider):
        db.add(provider)
        db.commit()
        db.refresh(provider)
        return provider

    @staticmethod
    def update(db: Session, provider: Provider):
        db.commit()
        db.refresh(provider)
        return provider

    @staticmethod
    def delete(db: Session, provider: Provider):
        db.delete(provider)
        db.commit()
        return provider
