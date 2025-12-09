from fastapi import FastAPI, APIRouter
from app.api.routers import expense_statements
from app.api.routers import payment_statements
from app.api.routers import transaction_types
from app.api.routers import roles
from app.api.routers import projects
from app.api.routers import bank_accounts
from .utils import constants

# from src.core.middlewares import setup_middlewares

app = FastAPI(
    title=constants.PROJECT_NAME,
    version=constants.PROJECT_VERSION,
)

# setup_middlewares(app)

api_router = APIRouter(prefix=constants.API_PREFIX)

api_router.include_router(expense_statements.router)
api_router.include_router(payment_statements.router)
api_router.include_router(transaction_types.router)
api_router.include_router(roles.router)
api_router.include_router(projects.router)
api_router.include_router(bank_accounts.router)

app.include_router(api_router)


@app.get("/", tags=["Root"])
def root():
    return {"message": "Welcome to the AYS API"}
