import os
from typing import Optional
import httpx
from tenacity import retry, stop_after_attempt, wait_exponential, retry_if_exception_type

GOODS_SERVICE_URL = os.getenv("GOODS_SERVICE_URL", "http://localhost:8001")

_TIMEOUT = 5.0
_RETRIED_ERRORS = (httpx.ConnectError, httpx.TimeoutException, httpx.RemoteProtocolError)


@retry(
    retry=retry_if_exception_type(_RETRIED_ERRORS),
    stop=stop_after_attempt(3),
    wait=wait_exponential(multiplier=0.5, min=0.5, max=4.0),
    reraise=True,
)
def fetch_good(good_id: int) -> Optional[dict]:
    """Returns good dict, None if 404, raises on other errors (after retries on network failures)."""
    resp = httpx.get(f"{GOODS_SERVICE_URL}/goods/{good_id}", timeout=_TIMEOUT)
    if resp.status_code == 404:
        return None
    if resp.status_code != 200:
        raise httpx.HTTPStatusError(
            f"goods-service returned {resp.status_code}",
            request=resp.request,
            response=resp,
        )
    return resp.json()