import jwt

from fastapi import Request
from jwt import InvalidTokenError
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.responses import JSONResponse, Response


class AuthenticationMiddleware(BaseHTTPMiddleware):

    PUBLIC_ROUTES = {
        ("POST", "/api/auth/login"),
        ("POST", "/api/auth/refresh"),
        ("POST", "/api/user/create"),        

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
                status_code=401,
                content={"message": "Authentication required"},
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
                raise InvalidTokenError("Invalid token type")

            user_id = payload.get("sub")

            if not user_id:
                raise InvalidTokenError("Missing subject")

        except InvalidTokenError as error:
            return JSONResponse(
                status_code=401,
                content={
                    "message": "Invalid or expired access token"
                },
            )

        request.state.current_user = {
            "id": user_id,
            "email": payload.get("email"),
            "role": payload.get("role"),
        }

        return await call_next(request)