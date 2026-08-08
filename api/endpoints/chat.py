from fastapi import APIRouter, Depends

from api.dependencies import get_dermclimate_service
from api.schemas import ChatRequest, ChatResponse

from dermclimate_service import DermClimateService


router = APIRouter(
    prefix="/chat",
    tags=["Chat"],
)


@router.post(
    "",
    response_model=ChatResponse,
)
async def chat(
    request: ChatRequest,
    dermclimate: DermClimateService = Depends(
        get_dermclimate_service,
    ),
):

    result = dermclimate.process_message(
        user_message=request.message,
    )

    return ChatResponse(
        status=result.status.value,
        response=result.response,
        message=result.message,
    )

