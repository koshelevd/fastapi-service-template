from starlette.middleware import Middleware
from starlette.middleware.cors import CORSMiddleware


def get_cors_middleware(origins: str) -> Middleware:
    return Middleware(
        CORSMiddleware,
        allow_origins=origins.split(","),
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
