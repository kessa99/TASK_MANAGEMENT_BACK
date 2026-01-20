"""
HTTP Routes
"""

from interface.http.routes.user_routes import router as user_router
from interface.http.routes.task_routes import router as task_router
from interface.http.routes.assign_routes import router as assign_router
from interface.http.routes.auth_routes import router as auth_router
from interface.http.routes.invitation_routes import router as invitation_router

__all__ = [
    "user_router",
    "task_router",
    "assign_router",
    "auth_router",
    "invitation_router",
]
