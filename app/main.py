from fastapi import FastAPI, APIRouter, Depends
from app.api.routers import auth
from app.api.routers import expense_statements
from app.api.routers import payment_statements
from app.api.routers import transaction_types
from app.api.routers import roles
from app.api.routers import projects
from app.api.routers import bank_accounts
from app.api.routers import providers
from app.api.routers import users
from app.api.routers import expenses
from app.api.helpers import get_current_user
from .utils import constants

# from src.core.middlewares import setup_middlewares

app = FastAPI(
    title=constants.PROJECT_NAME,
    version=constants.PROJECT_VERSION,
)

# setup_middlewares(app)

public_router = APIRouter(prefix=constants.API_PREFIX)
public_router.include_router(auth.router)

protected_router = APIRouter(
    prefix=constants.API_PREFIX, dependencies=[Depends(get_current_user)]
)
protected_router.include_router(expense_statements.router)
protected_router.include_router(payment_statements.router)
protected_router.include_router(transaction_types.router)
protected_router.include_router(roles.router)
protected_router.include_router(projects.router)
protected_router.include_router(bank_accounts.router)
protected_router.include_router(providers.router)
protected_router.include_router(users.router)
protected_router.include_router(expenses.router)

app.include_router(public_router)
app.include_router(protected_router)


@app.get("/", tags=["Root"])
def root():
    return {"message": "Welcome to the GGPO API"}
