import os

from dotenv import load_dotenv


load_dotenv()


API_BASE_URL = os.getenv(
    "API_BASE_URL"
)

API_ACCESS_TOKEN = os.getenv(
    "API_ACCESS_TOKEN"
)


if not API_BASE_URL:
    raise RuntimeError(
        "La variable API_BASE_URL est absente."
    )


if not API_ACCESS_TOKEN:
    raise RuntimeError(
        "La variable API_ACCESS_TOKEN est absente."
    )