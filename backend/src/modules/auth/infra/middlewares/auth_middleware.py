import jwt

from fastapi import Request, status
from jwt import InvalidTokenError
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.responses import JSONResponse, Response
from src.modules.auth.domain.errors.auth_error_usecase import AuthUnathorizedAction

class AuthenticationMiddleware(BaseHTTPMiddleware):

    PUBLIC_ROUTES = {
        ("POST", "/api/auth/login"),
        ("POST", "/api/auth/logout"),
        ("POST", "/api/auth/refresh"),
        ("POST", "/api/user/create"),        
        ("GET", "/api/tea"),

        ("GET", "/docs"),
        ("GET", "/openapi.json"),
        ("GET", "/redoc")
        }

    def __init__(self, app, jwt_secret: str) -> None:
        super().__init__(app)
        self.jwt_secret = jwt_secret

    async def dispatch(
        self,
        request: Request,
        call_next,
    ) -> Response:

        if request.method == "OPTIONS":
            return await call_next(request)

        route = (request.method, request.url.path)

        if route in self.PUBLIC_ROUTES:
            return await call_next(request)

        token = request.cookies.get("access_token")

        if not token:
            return JSONResponse(
                status_code=status.HTTP_401_UNAUTHORIZED,
                content={"message": "Unauthorizated"}
            )

        try:
            payload = jwt.decode(
                token,
                self.jwt_secret,
                algorithms=["HS256"],
                options={
                    "require": ['exp', 'sub', 'type'],
                }
            )

            if payload.get("type") != "access":
                return JSONResponse(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    content={"message": "Authentication is failed"}
                )

            user_id = payload.get("sub")

            if not user_id:
                return JSONResponse(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    content={"message": "Authentication is failed"}
                )

        except InvalidTokenError as error:
            return JSONResponse(
                status_code=status.HTTP_401_UNAUTHORIZED,
                content={"message": "Authentication is failed"}
            )

        request.state.current_user = {
            "user_id": user_id,
            "role": payload.get("role"),
        }

        return await call_next(request)