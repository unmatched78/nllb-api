from collections.abc import AsyncIterator
from contextlib import asynccontextmanager

from litestar import Litestar

from server.config import Config
from server.features import get_language_detector


@asynccontextmanager
async def load_fasttext_model(app: Litestar) -> AsyncIterator[None]:
    """
    Summary
    -------
    download and load the FastText model

    Parameters
    ----------
    app (Litestar)
        the application instance
    """
    with get_language_detector(
        Config.language_detector_repository,
        stub=Config.stub_language_detector,
    ) as language_detector:
        app.state.language_detector = language_detector
        yield
