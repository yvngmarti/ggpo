from fastapi import APIRouter, Depends
from app.api.services.expense_status_service import ExpenseStatusService
from app.api.schemas import expense_status_schema
from app.api.helpers import APIResponse, get_expense_status_service

router = APIRouter(prefix="/expense-status", tags=["Expense Status"])


@router.get("/", response_model=APIResponse)
def get_expense_statements(
    service: ExpenseStatusService = Depends(get_expense_status_service),
):
    expense_statements = service.get_all_expense_status()
    data = [
        expense_status_schema.ExpenseStatusResponseSchema.model_validate(es)
        for es in expense_statements
    ]
    message = (
        "Expense statements retrieved successfully"
        if data
        else "No expense statements found"
    )
    return APIResponse(status=True, message=message, data=data)


@router.get("/{expense_status_id}", response_model=APIResponse)
def get_expense_status_by_id(
    expense_status_id: int,
    service: ExpenseStatusService = Depends(get_expense_status_service),
):
    expense_status = service.get_expense_status_by_id(expense_status_id)

    if expense_status is None:
        return APIResponse(status=False, message="Expense status not found", data=None)

    data = expense_status_schema.ExpenseStatusResponseSchema.model_validate(
        expense_status
    )
    return APIResponse(
        status=True, message="Expense status retrieved successfully", data=data
    )


@router.get("/{expense_status_name}/name", response_model=APIResponse)
def get_expense_status_by_name(
    expense_status_name: str,
    service: ExpenseStatusService = Depends(get_expense_status_service),
):
    expense_status = service.get_expense_status_by_name(expense_status_name)

    if expense_status is None:
        return APIResponse(status=False, message="Expense status not found", data=None)

    data = expense_status_schema.ExpenseStatusResponseSchema.model_validate(
        expense_status
    )
    return APIResponse(
        status=True, message="Expense status retrieved successfully", data=data
    )


@router.post("/", response_model=APIResponse)
def create_expense_status(
    create_schema: expense_status_schema.CreateExpenseStatusSchema,
    service: ExpenseStatusService = Depends(get_expense_status_service),
):
    success, message, expense_status = service.create_expense_status(create_schema)

    if not success:
        return APIResponse(status=False, message=message, data=None)

    data = expense_status_schema.ExpenseStatusResponseSchema.model_validate(
        expense_status
    )
    return APIResponse(status=True, message=message, data=data)


@router.patch("/{expense_status_id}", response_model=APIResponse)
def update_expense_status(
    expense_status_id: int,
    update_schema: expense_status_schema.UpdateExpenseStatusSchema,
    service: ExpenseStatusService = Depends(get_expense_status_service),
):
    success, message, expense_status = service.update_expense_status(
        expense_status_id, update_schema
    )

    if not success:
        return APIResponse(status=False, message=message, data=None)

    data = expense_status_schema.ExpenseStatusResponseSchema.model_validate(
        expense_status
    )
    return APIResponse(status=True, message=message, data=data)


@router.delete("/{expense_status_id}", response_model=APIResponse)
def delete_expense_status(
    expense_status_id: int,
    service: ExpenseStatusService = Depends(get_expense_status_service),
):
    success, message, expense_status = service.delete_expense_status(expense_status_id)

    if not success:
        return APIResponse(status=False, message=message, data=None)

    data = expense_status_schema.ExpenseStatusResponseSchema.model_validate(
        expense_status
    )
    return APIResponse(status=True, message=message, data=data)
