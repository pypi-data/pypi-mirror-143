from fastapi import FastAPI

from fief.apps.admin.routers.api_keys import router as api_keys_router
from fief.apps.admin.routers.auth import router as auth_router
from fief.apps.admin.routers.clients import router as clients_router
from fief.apps.admin.routers.tenants import router as tenants_router
from fief.apps.admin.routers.users import router as users_router
from fief.apps.admin.routers.workspaces import router as workspaces_router

app = FastAPI()
app.include_router(api_keys_router, prefix="/api-keys", include_in_schema=False)
app.include_router(auth_router, prefix="/auth", include_in_schema=False)
app.include_router(clients_router, prefix="/clients")
app.include_router(tenants_router, prefix="/tenants")
app.include_router(users_router, prefix="/users")
app.include_router(workspaces_router, prefix="/workspaces", include_in_schema=False)

__all__ = ["app"]
