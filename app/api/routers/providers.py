from fastapi import APIRouter, Depends
from app.api.services import ProviderService
from app.api.schemas import provider_schema
from app.api.helpers import APIResponse, get_provider_service

router = APIRouter(prefix="/providers", tags=["Providers"])


@router.get("", response_model=APIResponse)
def get_providers(
    service: ProviderService = Depends(get_provider_service),
):
    providers = service.get_all_providers()
    data = [provider_schema.ProviderResponseSchema.model_validate(p) for p in providers]
    message = "Providers retrieved successfully" if data else "No providers found"
    return APIResponse(status=True, message=message, data=data)


@router.get("/{provider_id}", response_model=APIResponse)
def get_provider_by_id(
    provider_id: int,
    service: ProviderService = Depends(get_provider_service),
):
    provider = service.get_provider_by_id(provider_id)

    if provider is None:
        return APIResponse(status=False, message="Provider not found", data=None)

    data = provider_schema.ProviderResponseSchema.model_validate(provider)
    return APIResponse(
        status=True, message="Provider retrieved successfully", data=data
    )


@router.get("/{rfc}/rfc", response_model=APIResponse)
def get_provider_by_rfc(
    rfc: str,
    service: ProviderService = Depends(get_provider_service),
):
    provider = service.get_provider_by_rfc(rfc)

    if provider is None:
        return APIResponse(status=False, message="Provider not found", data=None)

    data = provider_schema.ProviderResponseSchema.model_validate(provider)
    return APIResponse(
        status=True, message="Provider retrieved successfully", data=data
    )


@router.post("", response_model=APIResponse)
def create_provider(
    create_schema: provider_schema.CreateProviderSchema,
    service: ProviderService = Depends(get_provider_service),
):
    success, message, provider = service.create_provider(create_schema)

    if not success:
        return APIResponse(status=False, message=message, data=None)

    data = provider_schema.ProviderResponseSchema.model_validate(provider)
    return APIResponse(status=True, message=message, data=data)


@router.patch("/{provider_id}", response_model=APIResponse)
def update_provider(
    provider_id: int,
    update_schema: provider_schema.UpdateProviderSchema,
    service: ProviderService = Depends(get_provider_service),
):
    success, message, provider = service.update_provider(provider_id, update_schema)

    if not success:
        return APIResponse(status=False, message=message, data=None)

    data = provider_schema.ProviderResponseSchema.model_validate(provider)
    return APIResponse(status=True, message=message, data=data)
