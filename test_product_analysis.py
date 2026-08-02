from pathlib import Path
import os

from dotenv import load_dotenv

# -------------------------
# AI
# -------------------------

from app.ai.cohere_llm import CohereLLM
from app.ai.intent_prompt import IntentPrompt
from app.ai.product_analysis_prompt import ProductAnalysisPrompt

from app.ai.intent_extractor import IntentExtractor

# -------------------------
# Analysis
# -------------------------

from app.analysis.product_analysis_service import ProductAnalysisService

# -------------------------
# Acquisition
# -------------------------

from app.acquisition.climate_fetcher import ClimateFetcher
from app.acquisition.ingredient_fetcher import IngredientFetcher

# -------------------------
# Feature Engineering
# -------------------------

from app.features.feature_engineer import engineer_features

# -------------------------
# Risk
# -------------------------

from app.risk.tewl_risk_engine import TEWLRiskEngine

# -------------------------
# Embeddings
# -------------------------

from app.embedding.sentence_transformer_embedding_model import (
    SentenceTransformerEmbeddingModel,
)

# -------------------------
# Index Builders
# -------------------------

from app.indexing.faiss_index_builder import FAISSIndexBuilder
from app.indexing.bm25_index_builder import BM25IndexBuilder

# -------------------------
# Persistence
# -------------------------

from app.persistence.faiss_index_storage import (
    FAISSIndexStorage,
)

from app.persistence.bm25_index_storage import (
    BM25IndexStorage,
)

from app.persistence.snowflake_knowledge_base_storage import (
    SnowflakeKnowledgeBaseStorage,
)

# -------------------------
# Knowledge Base
# -------------------------

from app.rag.knowledge_base_service import (
    KnowledgeBaseService,
)

# -------------------------
# Retrieval
# -------------------------

from app.retrieval.hybrid_knowledge_retriever import (
    HybridKnowledgeRetriever,
)

# -------------------------
# Reranking
# -------------------------

from app.reranking.cross_encoder_reranker import (
    CrossEncoderReranker,
)

# -------------------------
# Conversation
# -------------------------

from app.conversation.conversation_manager import ConversationManager
from app.conversation.conversation_state import ConversationState

# -------------------------
# Routing
# -------------------------

from app.routing.intent_router import IntentRouter

from dermclimate_service import DermClimateService

from app.conversation.conversation_manager import ConversationManager
from app.conversation.conversation_state import ConversationState

from app.analysis.climate_analysis_service import ClimateAnalysisService
from app.analysis.ingredient_analysis_service import IngredientAnalysisService

from app.ai.climate_analysis_prompt import ClimateAnalysisPrompt
from app.ai.ingredient_analysis_prompt import IngredientAnalysisPrompt




def main():

    load_dotenv()

    print("=" * 70)
    print("Starting DermClimate...")
    print("=" * 70)

    # ----------------------------------------
    # AI
    # ----------------------------------------

    llm = CohereLLM(
        api_key=os.getenv("COHERE_API_KEY"),
        model="command-a-03-2025",
    )

    intent_prompt = IntentPrompt()

    product_analysis_prompt = ProductAnalysisPrompt()

    climate_analysis_prompt = ClimateAnalysisPrompt()

    ingredient_analysis_prompt = IngredientAnalysisPrompt()

# ----------------------------------------
    # Knowledge Base
    # ----------------------------------------

    project_root = Path(__file__).parent

    faiss_index_storage = FAISSIndexStorage(
        project_root / "indexes" / "faiss.index"
    )

    bm25_index_storage = BM25IndexStorage(
        project_root / "indexes" / "bm25.pkl"
    )

    embedding_model = SentenceTransformerEmbeddingModel()

    storage = SnowflakeKnowledgeBaseStorage()

    faiss_index_builder = FAISSIndexBuilder()

    bm25_index_builder = BM25IndexBuilder()

    knowledge_base_service = KnowledgeBaseService(
        knowledge_chunk_builder=None,
        storage=storage,
        faiss_index_builder=faiss_index_builder,
        bm25_index_builder=bm25_index_builder,
        faiss_index_storage=faiss_index_storage,
        bm25_index_storage=bm25_index_storage,
        embedding_model=embedding_model,
    )


    # ----------------------------------------
    # Retrieval
    # ----------------------------------------

    faiss_retriever = knowledge_base_service.create_faiss_retriever()

    bm25_retriever = knowledge_base_service.create_bm25_retriever()

    retriever = HybridKnowledgeRetriever(
        faiss_retriever=faiss_retriever,
        bm25_retriever=bm25_retriever,
    )

    reranker = CrossEncoderReranker()



    # ----------------------------------------
    # Domain Services
    # ----------------------------------------

    climate_fetcher = ClimateFetcher()

    risk_engine = TEWLRiskEngine()

    ingredient_fetcher = IngredientFetcher()


    # ----------------------------------------
    # Intent Extraction
    # ----------------------------------------

    intent_extractor = IntentExtractor(
        llm=llm,
        prompt=intent_prompt,
    )

        # ----------------------------------------
    # Product Analysis
    # ----------------------------------------

    product_analysis_service = ProductAnalysisService(
        climate_fetcher=climate_fetcher,
        feature_engineer=engineer_features,
        risk_engine=risk_engine,
        ingredient_fetcher=ingredient_fetcher,
        retriever=retriever,
        reranker=reranker,
        prompt=product_analysis_prompt,
        llm=llm,
    )


    climate_analysis_service = ClimateAnalysisService(
        climate_fetcher=climate_fetcher,
        feature_engineer=engineer_features,
        risk_engine=risk_engine,
        prompt=climate_analysis_prompt,
        llm=llm,
    )


    ingredient_analysis_service = IngredientAnalysisService(
        retriever=retriever,
        reranker=reranker,
        prompt=ingredient_analysis_prompt,
        llm=llm,
    )


    # ----------------------------------------
    # Routing
    # ----------------------------------------

    intent_router = IntentRouter(
        ingredient_service=ingredient_analysis_service,
        product_service=product_analysis_service,
        weather_service=climate_analysis_service,
    )


    # ----------------------------------------
    # Conversation
    # ----------------------------------------

    conversation_manager = ConversationManager(
        intent_extractor=intent_extractor,
        intent_router=intent_router,
    )



    # ----------------------------------------
    # DermClimate
    # ----------------------------------------

    dermclimate = DermClimateService(
        conversation_manager=conversation_manager,
    )



    # ----------------------------------------
    # DermClimate CLI
    # ----------------------------------------

    print("\nDermClimate is ready!")
    print("Type 'exit' to quit.\n")

    while True:

        user_message = input("You: ")

        if user_message.lower() == "exit":
            break

        try:

            result = dermclimate.process_message(
                user_message=user_message,
            )

            print("\nDermClimate:\n")

            if result.response:
                print(result.response)
            else:
                print(result.message)

            print()

        except Exception:

            import traceback

            print("\nFULL TRACEBACK:\n")
            traceback.print_exc()
            print()



if __name__ == "__main__":
    main()