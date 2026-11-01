import logging

from src.observability.correlation import (
    correlation_id
)


class CorrelationFilter(
    logging.Filter
):

    def filter(
        self,
        record
    ):

        record.correlation_id = (
            correlation_id.get()
        )

        return True


logger = logging.getLogger(
    "os-api"
)

handler = logging.StreamHandler()

formatter = logging.Formatter(
    "[%(correlation_id)s] "
    "%(levelname)s - "
    "%(message)s"
)

handler.setFormatter(
    formatter
)

handler.addFilter(
    CorrelationFilter()
)

logger.addHandler(
    handler
)

logger.setLevel(
    logging.INFO
)