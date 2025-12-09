#!/usr/bin/env python3

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from sqlalchemy.exc import ProgrammingError
from app.core.database import SessionLocal
from app.seeds import initial_data


def main():
    db = SessionLocal()
    try:
        results = initial_data(db)
        total = sum(results.values())
        if total > 0:
            print(f"Results: {results}")
        return 0
    except ProgrammingError:
        print("FAILED: Tables don't exist")
        print("Please run migrations first: alembic upgrade head")
        return 1
    except Exception as e:
        print(f"FAILED: {str(e)}")
        return 1
    finally:
        db.close()


if __name__ == "__main__":
    sys.exit(main())
