from fastapi import Cookie
from typing import Annotated, Union
from database.tools.users import UserTool
from web_api.dependencies.cookies_auth import get_jwt_payload
from database.models.users import UserModel


async def get_user(
    access_token: Annotated[str | None, Cookie(alias="access_token")] = None,
) -> Union[UserModel, None]:
    if payload_temp := get_jwt_payload(access_token):
        return await UserTool(payload_temp["sub"]).get()
    return None