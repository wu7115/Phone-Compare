from langchain_astradb import AstraDBVectorStore
from langchain_huggingface import HuggingFaceEndpointEmbeddings
from comparer.config import Config
from comparer.data_converter import DataConverter
from utils.logger import get_logger

logger = get_logger(__name__)

class DataIngestor:
    def __init__(self):
        self.embedding = HuggingFaceEndpointEmbeddings(model=Config.EMBEDDING_MODEL)
        self.vstore = AstraDBVectorStore(
            embedding=self.embedding,
            collection_name="phone_comparer",
            api_endpoint=Config.ASTRA_DB_API_ENDPOINT,
            token=Config.ASTRA_DB_APPLICATION_TOKEN,
            namespace=Config.ASTRA_DB_KEYSPACE
        )
    
    def ingest(self, load_existing=True):
        if load_existing:
            return self.vstore
        
        processor = DataConverter()
        docs = processor.process_markdown_files()
        
        if docs:
            self.vstore.add_documents(docs)
            logger.info(f"Successfully ingested {len(docs)} markdown documents")
        else:
            logger.info("No markdown documents found to ingest")
        
        return self.vstore

if __name__ == "__main__":
    ingestor = DataIngestor()
    ingestor.ingest(load_existing=False)