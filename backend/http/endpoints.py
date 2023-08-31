from fastapi import FastAPI

from ..features.bar.router import router as bar_router
from ..features.foo.router import router as foo_router
from ..features.hello.router import router as hello_router
from ..features.tar.router import router as tar_router
from ..features.zoo.router import router as zoo_router


def add_routers(app: FastAPI) -> None:
    app.include_router(bar_router)
    app.include_router(foo_router)
    app.include_router(hello_router)
    app.include_router(tar_router)
    app.include_router(zoo_router)

