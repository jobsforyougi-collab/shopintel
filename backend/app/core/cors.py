from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.config.settings import settings


def register_cors(app: FastAPI) -> None:
    """
    Register CORS middleware.
    """

    origins = [
        origin.strip()
        for origin in settings.backend_cors_origins.split(",")
    ]

    methods = (
        ["*"]
        if settings.backend_cors_methods == "*"
        else [
            method.strip()
            for method in settings.backend_cors_methods.split(",")
        ]
    )

    headers = (
        ["*"]
        if settings.backend_cors_headers == "*"
        else [
            header.strip()
            for header in settings.backend_cors_headers.split(",")
        ]
    )

    app.add_middleware(
        CORSMiddleware,
        allow_origins=origins,
        allow_credentials=settings.backend_cors_credentials,
        allow_methods=methods,
        allow_headers=headers,
    )