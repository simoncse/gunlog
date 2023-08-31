from fastapi import APIRouter
from loguru import logger

router = APIRouter(prefix='/tar',tags=['Tar'])

@router.get('/test-log')
async def test_log():
    logger.info('Tar log')
    return 'ok'
