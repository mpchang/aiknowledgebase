import os
import PyPDF2
from datetime import datetime
import mimetypes
from langchain.text_splitter import RecursiveCharacterTextSplitter
import logging

logger = logging.getLogger(__name__)

class DocumentProcessor:
    def __init__(self, embedding_service):
        self.embedding_service = embedding_service
        self.text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=1000,
            chunk_overlap=200,
            length_function=len
        )
        
    def process_file(self, file_path):
        """Process a file based on its type"""
        mime_type, _ = mimetypes.guess_type(file_path)
        
        if mime_type == "application/pdf":
            return self.process_pdf(file_path)
        elif mime_type == "text/plain":
            return self.process_text(file_path)
        else:
            logger.error(f"Unsupported file type: {mime_type}")
            return False
            
    def process_text(self, file_path):
        try:
            with open(file_path, "r", encoding="utf-8") as file:
                text = file.read()
                return self._process_content(text, file_path)
        except Exception as e:
            logger.error(f"Error processing text file {file_path}: {str(e)}")
            return False
            
    def process_pdf(self, file_path):
        try:
            with open(file_path, "rb") as file:
                pdf_reader = PyPDF2.PdfReader(file)
                text = ""
                for page in pdf_reader.pages:
                    text += page.extract_text()
                return self._process_content(text, file_path, num_pages=len(pdf_reader.pages))
        except Exception as e:
            logger.error(f"Error processing PDF {file_path}: {str(e)}")
            return False
            
    def _process_content(self, text, file_path, num_pages=None):
        try:
            # Split text into chunks
            chunks = self.text_splitter.split_text(text)
            
            # Process chunks with embedding service
            self.embedding_service.add_documents(chunks, os.path.basename(file_path))
            
            # Create metadata
            file_stat = os.stat(file_path)
            metadata = {
                "upload_time": datetime.now().isoformat(),
                "size": file_stat.st_size,
                "num_chunks": len(chunks)
            }
            if num_pages is not None:
                metadata["num_pages"] = num_pages
                
            return metadata
        except Exception as e:
            logger.error(f"Error processing content from {file_path}: {str(e)}")
            return False
