
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from loguru import logger

from . import endpoints
from .logger_setup import configure_logger

configure_logger()

app = FastAPI()


endpoints.add_routers(app)


app.add_middleware(CORSMiddleware,
    allow_origins=["*"],
    allow_headers=["*"],
    allow_credentials=True,
    allow_methods=["*"],
)

@app.get('/loguru')
async def print_loguru_logger_obj():
    return f'{logger}'






