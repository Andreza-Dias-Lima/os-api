from fastapi import Request
from fastapi.responses import JSONResponse

from src.exceptions.not_found import (
    NotFoundException
)


async def requester_not_found_handler(
    request: Request,
    exc: NotFoundException
):

    return JSONResponse(

        status_code=exc.status,

        content={
            "type": exc.type,
            "title": exc.title,
            "status": exc.status,
            "detail": exc.detail
        }
    )