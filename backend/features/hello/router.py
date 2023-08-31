from fastapi import APIRouter
from loguru import logger

router = APIRouter(prefix='/hello',tags=['Hello'])


@router.get('/test-log')
async def test_log():
    logger.info('Hello log')
    return 'ok'
