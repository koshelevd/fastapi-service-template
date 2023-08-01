import asyncio

from fastapi import APIRouter, Depends
from fastapi.responses import JSONResponse
from sqlalchemy import text
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession

from controllers.stub import Stub

router = APIRouter(tags=["healthcheck"])

RESPONSE = {
    200: {"content": {"application/json": {"example": {"healthcheck": "ok"}}}},
    500: {"content": {"application/json": {"example": {"healthcheck": "false", "error": "string"}}}},
}


@router.get("/healthcheck", responses=RESPONSE)
async def healthcheck(db_session: AsyncSession = Depends(Stub(AsyncSession))) -> JSONResponse:
    """
    Service health check.
    Returning OK status after 1 sec awaiting if everything is good, else returning an error.
    """
    await asyncio.sleep(1)
    try:
        await db_session.execute(text("SELECT 1"))
    except SQLAlchemyError as exc:
        return JSONResponse(content={"healthcheck": "false", "error": str(exc)}, status_code=500)
    return JSONResponse(content={"healthcheck": "ok"}, status_code=200)
