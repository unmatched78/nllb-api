from logging import getLogger

from litestar import Litestar, Response, Router
from litestar.openapi import OpenAPIConfig
from litestar.openapi.spec import Server
from litestar.status_codes import HTTP_500_INTERNAL_SERVER_ERROR

from server.api import v4
from server.config import Config
from server.lifespans import load_fasttext_model, load_translator_model


def exception_handler(_, exception: Exception) -> Response[dict[str, str]]:
    """
    Summary
    -------
    the Litestar exception handler

    Parameters
    ----------
    request (Request) : the request
    exception (Exception) : the exception

    Returns
    -------
    response (Response[dict[str, str]]) : the response
    """
    getLogger('custom.access').error(exception, exc_info=True)

    return Response(
        content={'detail': 'Internal Server Error'},
        status_code=HTTP_500_INTERNAL_SERVER_ERROR,
    )


def app() -> Litestar:
    """
    Summary
    -------
    the Litestar application
    """
    description = (
        "A performant high-throughput CPU-based API for Meta's No Language Left Behind (NLLB) using CTranslate2, "
        'hosted on Hugging Face Spaces.'
    )

    openapi_config = OpenAPIConfig(
        title='nllb-api',
        version='4.1.0',
        description=description,
        use_handler_docstrings=True,
        servers=[Server(url=Config.server_root_path)],
    )

    v4_router = Router(
        '/v4',
        tags=['v4'],
        route_handlers=[v4.index, v4.language, v4.TranslatorController],
    )

    return Litestar(
        openapi_config=openapi_config,
        exception_handlers={HTTP_500_INTERNAL_SERVER_ERROR: exception_handler},
        route_handlers=[v4_router],
        lifespan=[load_fasttext_model, load_translator_model],
    )
