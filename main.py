"""
The main script that initiates and runs the FastAPI application.
This module sets up the application configuration including logging,
 CORS, database connection, static files routing and API routes.
"""

import logging
from functools import partial

import uvicorn
from fastapi import FastAPI, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.gzip import GZipMiddleware
from fastapi.responses import RedirectResponse
from fastapi.staticfiles import StaticFiles
from starlette_graphene3 import GraphQLApp, make_graphiql_handler

from app.api.graphql.schema import schema
from app.config.config import auth_setting, init_setting, setting
from app.core import logging_config
from app.core.lifecycle import lifespan
from app.middlewares.security_headers import SecurityHeadersMiddleware
from app.utils.file_utils.openapi_utils import (
    custom_generate_unique_id,
    custom_openapi,
)

logging_config.setup_logging(init_settings=init_setting, settings=setting)
logger: logging.Logger = logging.getLogger(__name__)

app: FastAPI = FastAPI(
    debug=True,
    openapi_url=f"{auth_setting.API_V1_STR}{init_setting.OPENAPI_FILE_PATH}",
    openapi_tags=init_setting.TAGS_METADATA,
    lifespan=lifespan,
    generate_unique_id_function=custom_generate_unique_id,
)
app.openapi = partial(custom_openapi, app)  # type: ignore
app.add_middleware(SecurityHeadersMiddleware)
app.add_middleware(
    CORSMiddleware,
    allow_origins=setting.BACKEND_CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.add_middleware(GZipMiddleware)

app.mount(
    init_setting.IMAGES_PATH,
    StaticFiles(directory=init_setting.IMAGES_DIRECTORY),
    name=init_setting.IMAGES_APP,
)
app.mount("/", GraphQLApp(schema, on_get=make_graphiql_handler()), "graphql")


@app.get(
    "/",
    status_code=status.HTTP_307_TEMPORARY_REDIRECT,
    response_class=RedirectResponse,
)
async def redirect_to_playground() -> RedirectResponse:
    """
    Redirects the user to the /playground endpoint for GraphQL interaction.
    ## Response:
    - `return:` **The redirected response**
    - `rtype:` **RedirectResponse**
    """
    return RedirectResponse(url="/graphql/")


if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host=f"{setting.SERVER_HOST}",
        port=setting.SERVER_PORT,
        reload=setting.SERVER_RELOAD,
        log_level=setting.SERVER_LOG_LEVEL,
        use_colors=True,
    )
