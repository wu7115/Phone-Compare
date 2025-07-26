from langchain_groq import ChatGroq
from langchain.chains import create_history_aware_retriever, create_retrieval_chain
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.runnables.history import RunnableWithMessageHistory
from langchain_community.chat_message_histories import ChatMessageHistory
from langchain_core.chat_history import BaseChatMessageHistory
from comparer.config import Config

class RAGChainBuilder:
    def __init__(self, vector_store):
        self.vector_Store = vector_store
        self.model = ChatGroq(model=Config.MODEL_NAME, temperature=0.5)
        self.history_store = {}

    def _get_history(self, session_id: str) -> BaseChatMessageHistory:
        # If don't find that session id then create a new session
        if session_id not in self.history_store:
            self.history_store[session_id] = ChatMessageHistory() # BaseChatMessageHistory is the data type of ChatMessageHistory, like "abc" and str
        
        return self.history_store[session_id]
    
    def build_chain(self):
        retriever = self.vector_Store.as_retriever(search_kwargs={"k": 3})

        context_prompt = ChatPromptTemplate.from_messages([
            ("system", "Given the chat history and user question, rewrite it as a standalone question."),
            MessagesPlaceholder(variable_name="chat_history"), 
            ("human", "{input}")  
        ])

        qa_prompt = ChatPromptTemplate.from_messages([
            ("system", """You're a phone expert answering product-related queries using the given information.
                          Stick to context. Be concise and helpful.\n\nCONTEXT:\n{context}\n\nQUESTION: {input}"""),
            MessagesPlaceholder(variable_name="chat_history"), 
            ("human", "{input}")  
        ])

        history_aware_retriever = create_history_aware_retriever(self.model, retriever, context_prompt)
        question_answer_chain = create_stuff_documents_chain(self.model, qa_prompt)
        rag_chain = create_retrieval_chain(history_aware_retriever, question_answer_chain)

        return RunnableWithMessageHistory(
            rag_chain, 
            self._get_history, 
            input_messages_key="input", 
            history_messages_key="chat_history", 
            output_messages_key="answer"
        )