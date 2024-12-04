import numpy as np
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity
import logging
from app.config.config import Config

logger = logging.getLogger(__name__)

class EmbeddingService:
    def __init__(self):
        self.model = SentenceTransformer("all-MiniLM-L6-v2")
        self.document_chunks = []
        self.chunk_embeddings = []
        self.chunk_sources = []
        
    def add_documents(self, chunks, source):
        """Add new documents to the embedding store"""
        embeddings = self.model.encode(chunks)
        
        for chunk, embedding in zip(chunks, embeddings):
            self.document_chunks.append(chunk)
            self.chunk_embeddings.append(embedding)
            self.chunk_sources.append(source)
            
    def search(self, query):
        """Search for relevant documents"""
        if not self.document_chunks:
            return [], []
            
        query_embedding = self.model.encode(query)
        similarities = cosine_similarity([query_embedding], self.chunk_embeddings)[0]
        
        relevant_indices = self._get_relevant_chunks(similarities)
        
        results = []
        sources = []
        for idx in relevant_indices:
            results.append(self.document_chunks[idx])
            sources.append(self.chunk_sources[idx])
            
        return results, sources
        
    def _get_relevant_chunks(self, similarities):
        """Get relevant chunks based on similarity threshold"""
        relevant_indices = np.where(similarities > Config.SIMILARITY_THRESHOLD)[0]
        relevant_indices = relevant_indices[np.argsort(similarities[relevant_indices])[::-1]]
        
        total_length = 0
        final_indices = []
        
        for idx in relevant_indices:
            chunk_length = len(self.document_chunks[idx])
            if total_length + chunk_length <= Config.MAX_CONTEXT_LENGTH:
                final_indices.append(idx)
                total_length += chunk_length
            else:
                break
                
        return final_indices
