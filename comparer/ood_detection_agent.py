from langchain_groq import ChatGroq
from comparer.config import Config
from dotenv import load_dotenv
from utils.logger import get_logger

load_dotenv()

logger = get_logger(__name__)

class OODDetectionAgent:
    def __init__(self):
        self.model = ChatGroq(model=Config.MODEL_NAME, temperature=0)
        self.ood_prompt = """You are an expert at detecting whether user queries are related to smartphones.

Your task is to determine if a query is IN_DOMAIN (about phones) or OUT_OF_DOMAIN (not about phones).

IN_DOMAIN examples:
- "Compare iPhone 15 and Samsung S25"
- "Which phone has better camera?"
- "What's the battery life of iPhone 15 Pro?"
- "Show me phone specs"
- "Compare phone prices"

OUT_OF_DOMAIN examples:
- "What's the weather today?"
- "How to cook pasta?"
- "Tell me about movies"
- "What's the stock price?"
- "How to fix my car?"

Given the query, respond with ONLY "IN_DOMAIN" or "OUT_OF_DOMAIN".

Query: {query}
Response:"""
    
    def detect(self, query):
        try:
            response = self.model.invoke(self.ood_prompt.format(query=query))
            return "OUT_OF_DOMAIN" in response.content.upper()
        except Exception as e:
            logger.info(f"Error in OOD detection: {e}")
            return False  # Default to in-domain on error
    
    def generate_ood_response(self, query):
        """Generate appropriate response for out-of-domain queries"""
        return "I can only help with phone-related questions. Please ask about smartphones, iPhones, Samsung phones, phone comparisons, specs, features, or prices."