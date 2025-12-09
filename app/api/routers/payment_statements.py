from fastapi import APIRouter, Depends
from app.api.services.payment_status_service import PaymentStatusService
from app.api.schemas import payment_status_schema
from app.api.helpers import APIResponse, get_payment_status_service

router = APIRouter(prefix="/payment-status", tags=["Payment Status"])


@router.get("/", response_model=APIResponse)
def get_payment_statements(
    service: PaymentStatusService = Depends(get_payment_status_service),
):
    payment_statements = service.get_all_payment_status()
    data = [
        payment_status_schema.PaymentStatusResponseSchema.model_validate(ps)
        for ps in payment_statements
    ]
    message = (
        "Payment statements retrieved successfully"
        if data
        else "No payment statements found"
    )
    return APIResponse(status=True, message=message, data=data)


@router.get("/{payment_status_id}", response_model=APIResponse)
def get_payment_status_by_id(
    payment_status_id: int,
    service: PaymentStatusService = Depends(get_payment_status_service),
):
    payment_status = service.get_payment_status_by_id(payment_status_id)

    if payment_status is None:
        return APIResponse(status=False, message="Payment status not found", data=None)

    data = payment_status_schema.PaymentStatusResponseSchema.model_validate(
        payment_status
    )
    return APIResponse(
        status=True, message="Payment status retrieved successfully", data=data
    )


@router.get("/{payment_status_name}/name", response_model=APIResponse)
def get_payment_status_by_name(
    payment_status_name: str,
    service: PaymentStatusService = Depends(get_payment_status_service),
):
    payment_status = service.get_payment_status_by_name(payment_status_name)

    if payment_status is None:
        return APIResponse(status=False, message="Payment status not found", data=None)

    data = payment_status_schema.PaymentStatusResponseSchema.model_validate(
        payment_status
    )
    return APIResponse(
        status=True, message="Payment status retrieved successfully", data=data
    )


@router.post("/", response_model=APIResponse)
def create_payment_status(
    create_schema: payment_status_schema.CreatePaymentStatusSchema,
    service: PaymentStatusService = Depends(get_payment_status_service),
):
    success, message, payment_status = service.create_payment_status(create_schema)

    if not success:
        return APIResponse(status=False, message=message, data=None)

    data = payment_status_schema.PaymentStatusResponseSchema.model_validate(
        payment_status
    )
    return APIResponse(status=True, message=message, data=data)


@router.patch("/{payment_status_id}", response_model=APIResponse)
def update_payment_status(
    payment_status_id: int,
    update_schema: payment_status_schema.UpdatePaymentStatusSchema,
    service: PaymentStatusService = Depends(get_payment_status_service),
):
    success, message, payment_status = service.update_payment_status(
        payment_status_id, update_schema
    )

    if not success:
        return APIResponse(status=False, message=message, data=None)

    data = payment_status_schema.PaymentStatusResponseSchema.model_validate(
        payment_status
    )
    return APIResponse(status=True, message=message, data=data)


@router.delete("/{payment_status_id}", response_model=APIResponse)
def delete_payment_status(
    payment_status_id: int,
    service: PaymentStatusService = Depends(get_payment_status_service),
):
    success, message, payment_status = service.delete_payment_status(payment_status_id)

    if not success:
        return APIResponse(status=False, message=message, data=None)

    data = payment_status_schema.PaymentStatusResponseSchema.model_validate(
        payment_status
    )
    return APIResponse(status=True, message=message, data=data)
