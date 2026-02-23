import os
import time
import logging

import httpx

logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")
logger = logging.getLogger(__name__)

API_URL = os.environ.get("API_URL", "http://api:8000")
UPLOAD_DIR = os.environ.get("UPLOAD_DIR", "/data/uploads")
OUTPUT_DIR = os.environ.get("OUTPUT_DIR", "/data/outputs")
POLL_INTERVAL = int(os.environ.get("POLL_INTERVAL", "10"))


def check_api_health() -> bool:
    """Check if the API service is reachable."""
    try:
        resp = httpx.get(f"{API_URL}/health", timeout=5.0)
        return resp.status_code == 200
    except httpx.HTTPError:
        return False


def poll_jobs():
    """Poll the API for pending jobs (placeholder for future use)."""
    logger.info("Polling for pending jobs (not yet implemented)")


def main():
    logger.info("Processor service starting")
    logger.info("API_URL=%s  UPLOAD_DIR=%s  OUTPUT_DIR=%s", API_URL, UPLOAD_DIR, OUTPUT_DIR)

    while True:
        if check_api_health():
            logger.info("API is healthy")
            poll_jobs()
        else:
            logger.warning("API not reachable, retrying in %ds", POLL_INTERVAL)

        time.sleep(POLL_INTERVAL)


if __name__ == "__main__":
    main()
