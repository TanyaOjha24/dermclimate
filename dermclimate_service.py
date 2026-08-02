from app.conversation.conversation_manager import ConversationManager
from app.conversation.conversation_state import ConversationState


class DermClimateService:

    def __init__(
        self,
        conversation_manager: ConversationManager,
    ):
        self.conversation_manager = conversation_manager
        self.conversation_state = ConversationState()

    def process_message(
        self,
        user_message: str,
    ):
        return self.conversation_manager.handle(
            user_message=user_message,
            conversation_state=self.conversation_state,
        )