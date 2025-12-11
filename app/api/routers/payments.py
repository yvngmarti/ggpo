from fastapi import APIRouter, Depends
from app.api.services.payment_service import PaymentService
from app.api.schemas import payment_schema
from app.api.helpers import (
    APIResponse,
    get_payment_service,
    RoleChecker,
)
from app.utils.constants import constants
from app.models import User

router = APIRouter(prefix="/payments", tags=["Payments"])


@router.get("", response_model=APIResponse)
def get_payments(
    service: PaymentService = Depends(get_payment_service),
    current_user: User = Depends(
        RoleChecker([constants.ROLE_DIRECTOR, constants.ROLE_TREASURER])
    ),
):
    payments = service.get_all_payments()
    data = [payment_schema.PaymentResponseSchema.model_validate(p) for p in payments]
    message = "Payments retrieved successfully" if data else "No payments found"
    return APIResponse(status=True, message=message, data=data)


@router.get("/{payment_id}", response_model=APIResponse)
def get_payment_by_id(
    payment_id: int,
    service: PaymentService = Depends(get_payment_service),
    current_user: User = Depends(
        RoleChecker([constants.ROLE_DIRECTOR, constants.ROLE_TREASURER])
    ),
):
    payment = service.get_payment_by_id(payment_id)

    if payment is None:
        return APIResponse(status=False, message="Payment not found", data=None)

    data = payment_schema.PaymentResponseSchema.model_validate(payment)
    return APIResponse(status=True, message="Payment retrieved successfully", data=data)


@router.post("/", response_model=APIResponse)
def create_payment(
    create_schema: payment_schema.CreatePaymentSchema,
    service: PaymentService = Depends(get_payment_service),
    current_user: User = Depends(RoleChecker([constants.ROLE_DIRECTOR])),
):
    success, message, payment = service.create_payment(create_schema, current_user)

    if not success:
        return APIResponse(status=False, message=message, data=None)

    data = payment_schema.PaymentResponseSchema.model_validate(payment)
    return APIResponse(status=True, message=message, data=data)


@router.patch("/{payment_id}/process", response_model=APIResponse)
def process_payment(
    payment_id: int,
    process_schema: payment_schema.ProcessPaymentSchema,
    service: PaymentService = Depends(get_payment_service),
    current_user: User = Depends(RoleChecker([constants.ROLE_TREASURER])),
):
    success, message, payment = service.process_payment(
        payment_id, process_schema, current_user
    )

    if not success:
        return APIResponse(status=False, message=message, data=None)

    data = payment_schema.PaymentResponseSchema.model_validate(payment)
    return APIResponse(status=True, message=message, data=data)
