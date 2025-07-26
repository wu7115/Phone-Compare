from langchain_core.documents import Document
import os
import glob

class DataConverter:
    def __init__(self, data_dir="data"):
        self.data_dir = data_dir
    
    def process_markdown_files(self):
        documents = []
        markdown_files = glob.glob(os.path.join(self.data_dir, "**/*.md"), recursive=True)
        
        for file_path in markdown_files:
            try:
                with open(file_path, 'r', encoding='utf-8') as file:
                    content = file.read()

                filename = os.path.basename(file_path)
                title = os.path.splitext(filename)[0]
                brand = os.path.basename(os.path.dirname(file_path))

                metadata = {
                    "source": file_path,
                    "title": title,
                    "brand": brand,
                    "file_type": "markdown"
                }

                doc = Document(
                    page_content=content,
                    metadata=metadata
                )
                
                documents.append(doc)
                
            except Exception as e:
                print(f"Error processing {file_path}: {e}")
        
        return documents