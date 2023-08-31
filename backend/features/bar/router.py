from fastapi import APIRouter
from loguru import logger

router = APIRouter(prefix='/bar',tags=['Bar'])


@router.get('/test-log')
async def test_log():
    logger.info('Bar log')
    return 'ok'
