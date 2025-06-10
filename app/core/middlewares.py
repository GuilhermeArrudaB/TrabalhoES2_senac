import time
import logging
from fastapi import Request, Response
from starlette.middleware.base import BaseHTTPMiddleware

# Configuração do logger
logging.basicConfig(
    filename="app/logs/app.log",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)

class LoggingMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        start_time = time.time()
        response = await call_next(request)
        process_time = time.time() - start_time
        log_message = (
            f"method={request.method} "
            f"path={request.url.path} "
            f"status_code={response.status_code} "
            f"process_time={process_time:.4f}s"
        )
        logger.info(log_message)
        return response
