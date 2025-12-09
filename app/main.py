from fastapi import FastAPI, APIRouter
from .utils import constants

# from src.core.middlewares import setup_middlewares
# from src.api.routes import (
#     departments,
#     requirement_types,
#     requirements,
#     service_requests,
#     report_views,
# )

app = FastAPI(
    title=constants.PROJECT_NAME,
    version=constants.PROJECT_VERSION,
)

# setup_middlewares(app)

api_router = APIRouter(prefix=constants.API_PREFIX)

# api_router.include_router(departments.router)
# api_router.include_router(requirement_types.router)
# api_router.include_router(requirements.router)
# api_router.include_router(service_requests.router)
# api_router.include_router(report_views.router)

app.include_router(api_router)


@app.get("/", tags=["Root"])
def root():
    return {"message": "Welcome to the AYS API"}
