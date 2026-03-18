

from fastapi import Depends, HTTPException, Security
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from typing import Optional
import logging

from fastapi import security


VALID_API_KEYS = {
    "demo-api-key-123": "demo-user",
    "admin-api-key-456": "admin-user",
    "readonly-api-key-789": "readonly-user",
}

# # API key permissions
# API_KEY_PERMISSIONS = { -> it is bette to use User_PERMISSIONS instead of API_KEY_PERMISSIONS, because it is more flexible and can be easily extended to support multiple users with different permissions

USER_PERMISSIONS = {

    "guest": ["read", "write"],
    "admin": ["read", "write", "delete", "admin"],
    "readonly": ["read"],
}

logger = logging.getLogger(__name__)

async def get_current_user(
    credentials: Optional[HTTPAuthorizationCredentials] = Security(security)
    ) -> Optional[str]:
    if not credentials:
        return None
    api_key = credentials.credentials

    if api_key not in VALID_API_KEYS:
        logger.warning(f"Unauthorized access attempt with API key: {api_key}")
        raise HTTPException(status_code=401, detail="Invalid API key", headers={"WWW-Authenticate": "Bearer"})
    
    user = VALID_API_KEYS[api_key]
    logger.info(f"Authenticated user: {user} with API key: {api_key}")
    return user
    
async def require_auth(
    current_user: Optional[str] = Depends(get_current_user)
    ) -> str:
    if not current_user:
        raise HTTPException(status_code=401, detail="Not authenticated", headers={"WWW-Authenticate": "Bearer"})
    return current_user

async def require_permission(
    permission: str,
    current_user: Optional[str] = Depends(get_current_user)
    ) -> str:
    if not current_user:
        raise HTTPException(status_code=401, detail="Not authenticated", headers={"WWW-Authenticate": "Bearer"})
    
    # reverse lookup, if find key then break the loop
    api_key = None
    for key, user in VALID_API_KEYS.items():
        if user == current_user:
            api_key = key
            break
    
    if permission not in USER_PERMISSIONS.get(current_user, []):
        logger.warning(f"User {current_user} does not have {permission} permission")
        raise HTTPException(status_code=403, detail="Forbidden")
    
    return current_user


# Convenience functions for common permission checks
async def require_read_permission(
    current_user: Optional[str] = Depends(get_current_user),
) -> str:
    """Require read permission."""
    return await require_permission("read", current_user)


async def require_write_permission(
    current_user: Optional[str] = Depends(get_current_user),
) -> str:
    """Require write permission."""
    return await require_permission("write", current_user)


async def require_admin_permission(
    current_user: Optional[str] = Depends(get_current_user),
) -> str:
    """Require admin permission."""
    return await require_permission("admin", current_user)