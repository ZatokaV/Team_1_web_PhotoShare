from typing import List
from fastapi import Depends, HTTPException

from src.database.models import User, UserRole
from src.services.auth import auth_service
from src.services.messages_templates import FORBIDDEN_ACCESS


class RoleChecker:
    def __init__(self, allowed_roles: List[UserRole]):
        self.allowed_roles = allowed_roles

    def __call__(self, user: User = Depends(auth_service.get_current_user)):
        print(user.user_role)
        print(self.allowed_roles)
        if user.user_role not in self.allowed_roles:
            raise HTTPException(status_code=403, detail=FORBIDDEN_ACCESS)
