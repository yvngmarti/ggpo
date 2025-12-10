from fastapi import APIRouter, Depends
from app.api.services.user_service import UserService
from app.api.schemas import user_schema
from app.api.helpers import APIResponse, get_user_service

router = APIRouter(prefix="/users", tags=["Users"])


@router.get("/", response_model=APIResponse)
def get_users(service: UserService = Depends(get_user_service)):
    users = service.get_all_users()
    data = [user_schema.UserResponseSchema.model_validate(u) for u in users]
    message = "Users retrieved successfully" if data else "No users found"
    return APIResponse(status=True, message=message, data=data)


@router.get("/{user_id}", response_model=APIResponse)
def get_user_by_id(
    user_id: int,
    service: UserService = Depends(get_user_service),
):
    user = service.get_user_by_id(user_id)

    if user is None:
        return APIResponse(status=False, message="User not found", data=None)

    data = user_schema.UserResponseSchema.model_validate(user)
    return APIResponse(status=True, message="User retrieved successfully", data=data)


@router.post("/", response_model=APIResponse)
def create_user(
    create_schema: user_schema.CreateUserSchema,
    service: UserService = Depends(get_user_service),
):
    success, message, user = service.create_user(create_schema)

    if not success:
        return APIResponse(status=False, message=message, data=None)

    data = user_schema.UserResponseSchema.model_validate(user)
    return APIResponse(status=True, message=message, data=data)


@router.patch("/{user_id}", response_model=APIResponse)
def update_user(
    user_id: int,
    update_schema: user_schema.UpdateUserSchema,
    service: UserService = Depends(get_user_service),
):
    success, message, user = service.update_user(user_id, update_schema)

    if not success:
        return APIResponse(status=False, message=message, data=None)

    data = user_schema.UserResponseSchema.model_validate(user)
    return APIResponse(status=True, message=message, data=data)
