from app.conversation.conversation_state import ConversationState
from app.models.parsed_request import ParsedRequest
from app.ai.intent_extractor import IntentExtractor
from app.routing.intent_router import IntentRouter
from app.models.analysis_result import (
    AnalysisResult,
    AnalysisStatus,
)



class ConversationManager:

    def __init__(
        self,
        intent_extractor: IntentExtractor,
        intent_router: IntentRouter,
    ):
        self.intent_extractor = intent_extractor
        self.intent_router = intent_router



    def handle(
        self,
        user_message: str,
        conversation_state: ConversationState,
    )-> AnalysisResult:

        parsed_request = self.intent_extractor.extract(
            user_message,
        )

        request = self._resolve_request(
            parsed_request,
            conversation_state,
        )

        result = self.intent_router.route(
            request,
        )

        self._update_state(
            conversation_state,
            request,
            result,
        )

        return result



    def _resolve_request(
        self,
        parsed_request: ParsedRequest,
        conversation_state: ConversationState,
    ) -> ParsedRequest:

        pending_request = conversation_state.pending_request

        if pending_request is None:
            return parsed_request

        if self._can_continue_conversation(
            pending_request,
            parsed_request,
        ):
            return self._merge_requests(
                pending_request,
                parsed_request,
            )

        return parsed_request



    def _can_continue_conversation(
        self,
        pending_request: ParsedRequest,
        new_request: ParsedRequest,
    ) -> bool:

        if new_request.intent is None:
            return True

        return new_request.intent == pending_request.intent



    def _merge_requests(
        self,
        pending_request: ParsedRequest,
        new_request: ParsedRequest,
    ) -> ParsedRequest:

        return ParsedRequest(
            intent=new_request.intent or pending_request.intent,
            product=new_request.product or pending_request.product,
            ingredients=new_request.ingredients or pending_request.ingredients,
            concern=new_request.concern or pending_request.concern,
            city=new_request.city or pending_request.city,
        )



    def _update_state(
        self,
        conversation_state: ConversationState,
        request: ParsedRequest,
        result: AnalysisResult,
    ) -> None:

        if result.status == AnalysisStatus.NEEDS_INPUT:
            conversation_state.pending_request = request
        else:
            conversation_state.pending_request = None