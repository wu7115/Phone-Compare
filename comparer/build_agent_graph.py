from langgraph.graph import StateGraph, END
from typing import TypedDict, Annotated
from comparer.ood_detection_agent import OODDetectionAgent
from comparer.response_agent import ResponseGenerationAgent
from langchain_core.messages import HumanMessage, AIMessage
from utils.logger import get_logger

logger = get_logger(__name__)

class AgentState(TypedDict):
    query: str
    is_ood: bool
    response: str
    session_id: str
    chat_history: list

def create_phone_comparison_graph(vector_store):
    ood_agent = OODDetectionAgent()
    response_agent = ResponseGenerationAgent(vector_store)

    def ood_detection_node(state: AgentState) -> AgentState:
        try:
            logger.info(f"OOD Detection for query: {state['query']}")

            chat_history = state.get("chat_history", [])

            if chat_history and len(chat_history) > 0:
                context = " ".join([msg.content for msg in chat_history[-3:]])
                full_query = f"Context: {context}\nCurrent query: {state['query']}\nIs this about phones?"
                is_ood = ood_agent.detect(full_query)
            
            else:
                is_ood = ood_agent.detect(state["query"])

            logger.info(f"OOD Detection result: {is_ood}")
            return {"is_ood": is_ood}
        except Exception as e:
            logger.error(f"Error in OOD detection: {e}")
            return {"is_ood": False}  # Default to in-domain on error

    def response_generation_node(state: AgentState) -> AgentState:
        try:
            logger.info(f"Response generation for query: {state['query']}, is_ood: {state['is_ood']}")

            chat_history = state.get("chat_history", [])
            
            if state["is_ood"]:
                response = ood_agent.generate_ood_response(state["query"])
                logger.info("Generated OOD response")
            else:
                response = response_agent.generate_response(state["query"], chat_history, state["session_id"])
                logger.info("Generated in-domain response")
            
            return {"response": response}
        except Exception as e:
            logger.error(f"Error in response generation: {e}")
            return {"response": "I'm having trouble processing your request. Please try again."}

    workflow = StateGraph(AgentState)

    workflow.add_node("ood_detection", ood_detection_node)
    workflow.add_node("response_generation", response_generation_node)

    workflow.set_entry_point("ood_detection")

    workflow.add_edge("ood_detection", "response_generation")
    workflow.add_edge("response_generation", END)

    compiled_graph = workflow.compile()
    
    logger.info("Phone comparison graph created successfully")
    return compiled_graph
