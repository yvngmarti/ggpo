from fastapi import APIRouter, Depends
from app.api.services import ExpenseService
from app.api.schemas import expense_schema
from app.api.helpers import (
    APIResponse,
    get_expense_service,
    RoleChecker,
)
from app.utils import constants
from app.models import User

router = APIRouter(prefix="/expenses", tags=["Expenses"])


@router.get("", response_model=APIResponse)
def get_expenses(service: ExpenseService = Depends(get_expense_service)):
    expenses = service.get_all_expenses()
    data = [expense_schema.ExpenseResponseSchema.model_validate(e) for e in expenses]
    message = "Expenses retrieved successfully" if data else "No expenses found"
    return APIResponse(status=True, message=message, data=data)


@router.get("/{expense_id}", response_model=APIResponse)
def get_expense_by_id(
    expense_id: int,
    service: ExpenseService = Depends(get_expense_service),
):
    expense = service.get_expense_by_id(expense_id)

    if expense is None:
        return APIResponse(status=False, message="Expense not found", data=None)

    data = expense_schema.ExpenseResponseSchema.model_validate(expense)
    return APIResponse(status=True, message="Expense retrieved successfully", data=data)


@router.post("/", response_model=APIResponse)
def create_expense(
    create_schema: expense_schema.CreateExpenseSchema,
    service: ExpenseService = Depends(get_expense_service),
    current_user: User = Depends(RoleChecker([constants.ROLE_ENGINEER])),
):
    success, message, expense = service.create_expense(create_schema, current_user)

    if not success:
        return APIResponse(status=False, message=message, data=None)

    data = expense_schema.ExpenseResponseSchema.model_validate(expense)
    return APIResponse(status=True, message=message, data=data)


@router.patch("/{expense_id}", response_model=APIResponse)
def update_expense(
    expense_id: int,
    update_schema: expense_schema.UpdateExpenseSchema,
    service: ExpenseService = Depends(get_expense_service),
):
    success, message, expense = service.update_expense(expense_id, update_schema)

    if not success:
        return APIResponse(status=False, message=message, data=None)

    data = expense_schema.ExpenseResponseSchema.model_validate(expense)
    return APIResponse(status=True, message=message, data=data)


@router.patch("/{expense_id}/review", response_model=APIResponse)
def review_expense(
    expense_id: int,
    review_schema: expense_schema.ReviewExpenseSchema,
    service: ExpenseService = Depends(get_expense_service),
    current_user: User = Depends(RoleChecker([constants.ROLE_DIRECTOR])),
):
    success, message, expense = service.review_expense(
        expense_id, review_schema, current_user
    )

    if not success:
        return APIResponse(status=False, message=message, data=None)

    data = expense_schema.ExpenseResponseSchema.model_validate(expense)
    return APIResponse(status=True, message=message, data=data)
