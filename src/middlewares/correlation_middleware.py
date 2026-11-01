import uuid

from starlette.middleware.base import (
    BaseHTTPMiddleware
)

from src.observability.correlation import (
    correlation_id
)


class CorrelationMiddleware(
    BaseHTTPMiddleware
):

    async def dispatch(
        self,
        request,
        call_next
    ):

        cid = request.headers.get(
            "X-Correlation-Id",
            str(uuid.uuid4())
        )


        print(f"Correlation ID: {cid}")

        correlation_id.set(cid)

        response = await call_next(
            request
        )

        response.headers[
            "X-Correlation-Id"
        ] = cid

        return response