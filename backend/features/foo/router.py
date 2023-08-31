from fastapi import APIRouter
from loguru import logger

router = APIRouter(prefix='/foo',tags=['Foo'])


@router.get('/test-log')
async def test_log():
    logger.info('Foo log 3')
    return 'ok 3'
