from fastapi import APIRouter, Depends
from app.api.services import TransactionTypeService
from app.api.schemas import transaction_type_schema
from app.api.helpers import APIResponse, get_transaction_type_service

router = APIRouter(prefix="/transaction-types", tags=["Transaction Types"])


@router.get("", response_model=APIResponse)
def get_transaction_types(
    service: TransactionTypeService = Depends(get_transaction_type_service),
):
    transaction_types = service.get_all_transaction_types()
    data = [
        transaction_type_schema.TransactionTypeResponseSchema.model_validate(tt)
        for tt in transaction_types
    ]
    message = (
        "Transaction types retrieved successfully"
        if data
        else "No transaction types found"
    )
    return APIResponse(status=True, message=message, data=data)


@router.get("/{transaction_type_id}", response_model=APIResponse)
def get_transaction_type_by_id(
    transaction_type_id: int,
    service: TransactionTypeService = Depends(get_transaction_type_service),
):
    transaction_type = service.get_transaction_type_by_id(transaction_type_id)

    if transaction_type is None:
        return APIResponse(
            status=False, message="Transaction type not found", data=None
        )

    data = transaction_type_schema.TransactionTypeResponseSchema.model_validate(
        transaction_type
    )
    return APIResponse(
        status=True, message="Transaction type retrieved successfully", data=data
    )


@router.get("/{transaction_type_name}/name", response_model=APIResponse)
def get_transaction_type_by_name(
    transaction_type_name: str,
    service: TransactionTypeService = Depends(get_transaction_type_service),
):
    transaction_type = service.get_transaction_type_by_name(transaction_type_name)

    if transaction_type is None:
        return APIResponse(
            status=False, message="Transaction type not found", data=None
        )

    data = transaction_type_schema.TransactionTypeResponseSchema.model_validate(
        transaction_type
    )
    return APIResponse(
        status=True, message="Transaction type retrieved successfully", data=data
    )


@router.post("", response_model=APIResponse)
def create_transaction_type(
    create_schema: transaction_type_schema.CreateTransactionTypeSchema,
    service: TransactionTypeService = Depends(get_transaction_type_service),
):
    success, message, transaction_type = service.create_transaction_type(create_schema)

    if not success:
        return APIResponse(status=False, message=message, data=None)

    data = transaction_type_schema.TransactionTypeResponseSchema.model_validate(
        transaction_type
    )
    return APIResponse(status=True, message=message, data=data)


@router.patch("/{transaction_type_id}", response_model=APIResponse)
def update_transaction_type(
    transaction_type_id: int,
    update_schema: transaction_type_schema.UpdateTransactionTypeSchema,
    service: TransactionTypeService = Depends(get_transaction_type_service),
):
    success, message, transaction_type = service.update_transaction_type(
        transaction_type_id, update_schema
    )

    if not success:
        return APIResponse(status=False, message=message, data=None)

    data = transaction_type_schema.TransactionTypeResponseSchema.model_validate(
        transaction_type
    )
    return APIResponse(status=True, message=message, data=data)


@router.delete("/{transaction_type_id}", response_model=APIResponse)
def delete_transaction_type(
    transaction_type_id: int,
    service: TransactionTypeService = Depends(get_transaction_type_service),
):
    success, message, transaction_type = service.delete_transaction_type(
        transaction_type_id
    )

    if not success:
        return APIResponse(status=False, message=message, data=None)

    data = transaction_type_schema.TransactionTypeResponseSchema.model_validate(
        transaction_type
    )
    return APIResponse(status=True, message=message, data=data)
