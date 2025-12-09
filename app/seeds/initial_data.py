from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError, OperationalError, ProgrammingError
from app.models import Role, TransactionType, ExpenseStatus, PaymentStatus
from app.seeds.seed_data import ROLES, EXPENSE_STATUS, PAYMENT_STATUS, TRANSACTION_TYPES


def seed_roles(db: Session) -> int:
    count = 0
    try:
        for role_data in ROLES:
            if isinstance(role_data, dict):
                role_name = role_data["name"]
                role_description = role_data.get("description")
            else:
                role_name = role_data
                role_description = None

            existing = db.query(Role).filter(Role.name == role_name).first()
            if not existing:
                role = Role(name=role_name, description=role_description)
                db.add(role)
                count += 1

        db.commit()
        return count
    except (ProgrammingError, OperationalError) as e:
        db.rollback()
        raise ProgrammingError(
            "Table 'roles' does not exist."
            "Please run migrations first: alembic upgrade head",
            params=None,
            orig=e,
        ) from e
    except SQLAlchemyError:
        db.rollback()
        raise


def seed_transaction_types(db: Session) -> int:
    count = 0
    try:
        for transaction_type_name in TRANSACTION_TYPES:
            existing = (
                db.query(TransactionType)
                .filter(TransactionType.name == transaction_type_name)
                .first()
            )
            if not existing:
                transaction_type = TransactionType(name=transaction_type_name)
                db.add(transaction_type)
                count += 1
        db.commit()
        return count
    except (ProgrammingError, OperationalError) as e:
        db.rollback()
        raise ProgrammingError(
            "Table 'transaction_types' does not exist."
            "Please run migrations first: alembic upgrade head",
            params=None,
            orig=e,
        ) from e
    except SQLAlchemyError:
        db.rollback()
        raise


def seed_payment_status(db: Session) -> int:
    count = 0
    try:
        for payment_status_name in PAYMENT_STATUS:
            existing = (
                db.query(PaymentStatus)
                .filter(PaymentStatus.name == payment_status_name)
                .first()
            )
            if not existing:
                payment_status = PaymentStatus(name=payment_status_name)
                db.add(payment_status)
                count += 1
        db.commit()
        return count
    except (ProgrammingError, OperationalError) as e:
        db.rollback()
        raise ProgrammingError(
            "Table 'payment_status' does not exist."
            "Please run migrations first: alembic upgrade head",
            params=None,
            orig=e,
        ) from e
    except SQLAlchemyError:
        db.rollback()
        raise


def seed_expense_status(db: Session) -> int:
    count = 0
    try:
        for expense_status_name in EXPENSE_STATUS:
            existing = (
                db.query(ExpenseStatus)
                .filter(ExpenseStatus.name == expense_status_name)
                .first()
            )
            if not existing:
                expense_status = ExpenseStatus(name=expense_status_name)
                db.add(expense_status)
                count += 1
        db.commit()
        return count
    except (ProgrammingError, OperationalError) as e:
        db.rollback()
        raise ProgrammingError(
            "Table 'expense_status' does not exist."
            "Please run migrations first: alembic upgrade head",
            params=None,
            orig=e,
        ) from e
    except SQLAlchemyError:
        db.rollback()
        raise


def initial_data(db: Session) -> dict:
    print("Starting database seeding...")
    results = {}
    try:
        count = seed_roles(db)
        results["roles"] = count
        if count > 0:
            print(f"Inserted {count} roles")

        count = seed_transaction_types(db)
        results["transaction_types"] = count
        if count > 0:
            print(f"Inserted {count} transaction types")

        count = seed_payment_status(db)
        results["payment_status"] = count
        if count > 0:
            print(f"Inserted {count} payment statuses")

        count = seed_expense_status(db)
        results["expense_status"] = count
        if count > 0:
            print(f"Inserted {count} expense statuses")

        print("Seeding completed")
        return results

    except ProgrammingError as e:
        print(f"\nError: {str(e)}")
        print("Make sure to run 'alembic upgrade head' before seeding data.")
        raise
    except Exception as e:
        print(f"\nUnexpected error during seeding: {str(e)}")
        raise
