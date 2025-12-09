from fastapi import APIRouter, Depends
from app.api.services.role_service import RoleService
from app.api.schemas import role_schema
from app.api.helpers import APIResponse, get_role_service

router = APIRouter(prefix="/roles", tags=["Roles"])


@router.get("/", response_model=APIResponse)
def get_roles(service: RoleService = Depends(get_role_service)):
    roles = service.get_all_roles()
    data = [role_schema.RoleResponseSchema.model_validate(r) for r in roles]
    message = "Roles retrieved successfully" if data else "No roles found"
    return APIResponse(status=True, message=message, data=data)


@router.get("/{role_id}", response_model=APIResponse)
def get_role_by_id(
    role_id: int,
    service: RoleService = Depends(get_role_service),
):
    role = service.get_role_by_id(role_id)

    if role is None:
        return APIResponse(status=False, message="Role not found", data=None)

    data = role_schema.RoleResponseSchema.model_validate(role)
    return APIResponse(status=True, message="Role retrieved successfully", data=data)


@router.get("/{role_name}/name", response_model=APIResponse)
def get_role_by_name(
    role_name: str,
    service: RoleService = Depends(get_role_service),
):
    role = service.get_role_by_name(role_name)

    if role is None:
        return APIResponse(status=False, message="Role not found", data=None)

    data = role_schema.RoleResponseSchema.model_validate(role)
    return APIResponse(status=True, message="Role retrieved successfully", data=data)


@router.post("/", response_model=APIResponse)
def create_role(
    create_schema: role_schema.CreateRoleSchema,
    service: RoleService = Depends(get_role_service),
):
    success, message, role = service.create_role(create_schema)

    if not success:
        return APIResponse(status=False, message=message, data=None)

    data = role_schema.RoleResponseSchema.model_validate(role)
    return APIResponse(status=True, message=message, data=data)


@router.patch("/{role_id}", response_model=APIResponse)
def update_role(
    role_id: int,
    update_schema: role_schema.UpdateRoleSchema,
    service: RoleService = Depends(get_role_service),
):
    success, message, role = service.update_role(role_id, update_schema)

    if not success:
        return APIResponse(status=False, message=message, data=None)

    data = role_schema.RoleResponseSchema.model_validate(role)
    return APIResponse(status=True, message=message, data=data)


@router.delete("/{role_id}", response_model=APIResponse)
def delete_role(
    role_id: int,
    service: RoleService = Depends(get_role_service),
):
    success, message, role = service.delete_role(role_id)

    if not success:
        return APIResponse(status=False, message=message, data=None)

    data = role_schema.RoleResponseSchema.model_validate(role)
    return APIResponse(status=True, message=message, data=data)
