from comparer.ood_detection_agent import OODDetectionAgent
from comparer.build_agent_graph import create_phone_comparison_graph
from langchain_core.runnables.history import RunnableWithMessageHistory
from langchain_community.chat_message_histories import ChatMessageHistory
from langchain_core.chat_history import BaseChatMessageHistory
from utils.logger import get_logger
import time

logger = get_logger(__name__)

class LangGraphPhoneSystem:   
    def __init__(self, vector_store):
        self.graph = create_phone_comparison_graph(vector_store)
        self.history_store = {}
    
    def _get_history(self, session_id: str) -> BaseChatMessageHistory:
        # If don't find that session id then create a new session
        if session_id not in self.history_store:
            self.history_store[session_id] = ChatMessageHistory()
        return self.history_store[session_id]
    
    def process_query(self, query: str, session_id: str = "default"):
        try:
            graph_with_history = RunnableWithMessageHistory(
                self.graph,
                self._get_history,
                input_messages_key="query",
                history_messages_key="chat_history",
                output_messages_key="response"
            )

            result = graph_with_history.invoke(
                {"query": query, "session_id": session_id},
                config={"configurable": {"session_id": session_id}}
            )
            
            return result["response"], result["is_ood"]
        
        except Exception as e:
            logger.error(f"Error in graph execution: {e}")
            return "I'm having trouble processing your request. Please try again.", False