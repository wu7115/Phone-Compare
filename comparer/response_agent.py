from comparer.rag_chain import RAGChainBuilder
from langchain_core.messages import HumanMessage, AIMessage
from utils.logger import get_logger

logger = get_logger(__name__)

class ResponseGenerationAgent: 
    def __init__(self, vector_store):
        self.rag_chain = RAGChainBuilder(vector_store).build_chain()
    
    def generate_response(self, query, chat_history=None, session_id="user-session"):
        response = self.rag_chain.invoke(
            {"input": query},
            config={"configurable": {"session_id": session_id}}
        )["answer"]
        return response
       