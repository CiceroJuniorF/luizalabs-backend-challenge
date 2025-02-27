from fastapi import Depends, FastAPI, Request
from fastapi.responses import JSONResponse
from jose import JWTError

from src.application.errors.application_error import ApplicationError
from src.application.errors.application_errors_enum import ApplicationErrors
from src.domain.errors.domain_error import DomainError
from src.presentation.command import auth_controller, customer_controller, favorite_product_controller


app = FastAPI()
app.include_router(customer_controller.router, prefix="/api")
app.include_router(favorite_product_controller.router, prefix="/api")
app.include_router(auth_controller.router, prefix="/api")

### Error Handlers

# Application error handler
@app.exception_handler(ApplicationError)
async def application_exception_handler(request: Request, exc: ApplicationError):
    def status_code_factory(error: ApplicationErrors):
        return {
            ApplicationErrors.NOT_FOUND: 404,
            ApplicationErrors.CONFLICT: 409
        }.get(error, 500)
    return JSONResponse(
        status_code= status_code_factory(exc.error),
        content={"message": exc.message}
    )

# Domain error handler
@app.exception_handler(DomainError)
async def domain_exception_handler(request: Request, exc: DomainError):
    return JSONResponse(
        status_code = 400,
        content={"message": exc.message}
    )


@app.exception_handler(JWTError)
async def jwt_exception_handler(request: Request, exc: JWTError):
    return JSONResponse(
        status_code = 401,
        content={"message": str(exc)}
    )