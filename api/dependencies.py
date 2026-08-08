from fastapi import Request

from dermclimate_service import DermClimateService


def get_dermclimate_service(
    request: Request,
) -> DermClimateService:
    """
    Return the shared DermClimateService instance
    created during FastAPI startup.
    """

    return request.app.state.dermclimate