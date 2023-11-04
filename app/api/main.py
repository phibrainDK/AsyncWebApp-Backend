# flake8: noqa E402
import json
import logging
import os
from typing import Any

from fastapi import FastAPI, status
from fastapi.exceptions import RequestValidationError
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from mangum import Mangum
from pydantic import ValidationError
from starlette.requests import Request
from api.routes.router import router

from config import settings


# from fastapi_utils.timing import add_timing_middleware

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
DOCUMENTATION_SUFFIX = "/openapi.json"

root_path = f"/{settings.ENV_STAGE}-tf" if settings.ENV_STAGE else ""
# root_path = ""
app: Any = FastAPI(
    title="WDS BACKEND API",
    version=settings.API_VERSION,
    root_path=root_path,
    openapi_url=DOCUMENTATION_SUFFIX
)

# add_timing_middleware(app, record=logger.info, prefix="e2ecarga")


general_exception = {
    "status_code": status.HTTP_422_UNPROCESSABLE_ENTITY,
    "message": "An unexpected internal error ocurred",
    "result_code": "WDS999",
}


@app.exception_handler(ValidationError)
def validation_exception_handler(request: Request, cmd_exception: ValidationError):
    content = {
        "modal_type": "general",
        "result_code": "WDS998",
        "message": (
            f"{cmd_exception.model.__name__}: "
            + str(cmd_exception).replace("\n", " :: ")
        ),
        "status_code": status.HTTP_422_UNPROCESSABLE_ENTITY,
        "translated_error_message": (
            "Hay un error en la validación de alguna estructura interna. "
        ),
    }
    logger.info(json.dumps(content, indent=4))
    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        content=content,
    )


@app.exception_handler(RequestValidationError)
def request_validation_exception_handler(
    request: Request, cmd_exception: RequestValidationError
):
    errors = cmd_exception._errors
    errors = [error["loc"] for error in errors]
    content = {
        "modal_type": "general",
        "result_code": "WDS997",
        "message": "The values on fields " + str(errors) + " are not appropiate",
        "status_code": status.HTTP_422_UNPROCESSABLE_ENTITY,
        "translated_error_message": (
            "Hay un error en la validación en algun campo solicitado. "
        ),
    }
    logger.info(json.dumps(content, indent=4))
    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        content=content,
    )



app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

if settings.USE_SENTRY:  # pragma: no cover
    import sentry_sdk
    from sentry_sdk.integrations.asgi import SentryAsgiMiddleware

    sentry_sdk.init(  # type: ignore
        dsn=settings.SENTRY_DSN,
        environment=settings.ENV_STAGE,
    )

    app.add_middleware(SentryAsgiMiddleware)


@app.get("/", tags=["Health Check"])
def health_check():
    return {"message": f"It Works! (v{settings.API_VERSION})"}  # pragma: no cover


app.include_router(router, prefix=settings.API_URL_PREFIX)

# For deployment via AWS Lambda


def handler(event, context):  # pragma: no cover
    logger.info(f":: event-WDS :: main-handler event = {event}")
    logger.info(f":: event-WDS :: main-handler context = {context}")
    asgi_handler = Mangum(app)
    response = asgi_handler(event, context)
    return response
``