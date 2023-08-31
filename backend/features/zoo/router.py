from fastapi import APIRouter
from loguru import logger

router = APIRouter(prefix='/zoo',tags=['Zoo'])


@router.get('/test-log')
async def test_log():
    logger.info('Zoo log')
    return 'ok'
