from fastapi import APIRouter, Depends
from app.api.services import ProjectService
from app.api.schemas import project_schema
from app.api.helpers import APIResponse, get_project_service

router = APIRouter(prefix="/projects", tags=["Projects"])


@router.get("", response_model=APIResponse)
def get_projects(service: ProjectService = Depends(get_project_service)):
    projects = service.get_all_projects()
    data = [project_schema.ProjectResponseSchema.model_validate(p) for p in projects]
    message = "Projects retrieved successfully" if data else "No projects found"
    return APIResponse(status=True, message=message, data=data)


@router.get("/{project_id}", response_model=APIResponse)
def get_project_by_id(
    project_id: int,
    service: ProjectService = Depends(get_project_service),
):
    project = service.get_project_by_id(project_id)

    if project is None:
        return APIResponse(status=False, message="Project not found", data=None)

    data = project_schema.ProjectResponseSchema.model_validate(project)
    return APIResponse(status=True, message="Project retrieved successfully", data=data)


@router.get("/{project_code}/code", response_model=APIResponse)
def get_project_by_code(
    project_code: str,
    service: ProjectService = Depends(get_project_service),
):
    project = service.get_project_by_code(project_code)

    if project is None:
        return APIResponse(status=False, message="Project not found", data=None)

    data = project_schema.ProjectResponseSchema.model_validate(project)
    return APIResponse(status=True, message="Project retrieved successfully", data=data)


@router.post("", response_model=APIResponse)
def create_project(
    create_schema: project_schema.CreateProjectSchema,
    service: ProjectService = Depends(get_project_service),
):
    success, message, project = service.create_project(create_schema)

    if not success:
        return APIResponse(status=False, message=message, data=None)

    data = project_schema.ProjectResponseSchema.model_validate(project)
    return APIResponse(status=True, message=message, data=data)


@router.patch("/{project_id}", response_model=APIResponse)
def update_project(
    project_id: int,
    update_schema: project_schema.UpdateProjectSchema,
    service: ProjectService = Depends(get_project_service),
):
    success, message, project = service.update_project(project_id, update_schema)

    if not success:
        return APIResponse(status=False, message=message, data=None)

    data = project_schema.ProjectResponseSchema.model_validate(project)
    return APIResponse(status=True, message=message, data=data)
