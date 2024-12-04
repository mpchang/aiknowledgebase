from flask import Blueprint, request, jsonify
import openai
import logging
from app.config.config import Config
from app.services.container import ServiceContainer

logger = logging.getLogger(__name__)

query_bp = Blueprint('query', __name__)

@query_bp.route("/query", methods=["POST"])
def query():
    try:
        data = request.get_json()
        if not data or "query" not in data:
            return jsonify({"error": "No query provided"}), 400

        query_text = data["query"]
        logger.info(f"Processing query: {query_text}")

        # Get embedding service from container
        embedding_service = ServiceContainer.get_instance().embedding_service

        # Get relevant chunks from embedding service
        relevant_chunks, sources = embedding_service.search(query_text)

        if not relevant_chunks:
            return jsonify({
                "response": "I don't have enough context to answer your question.",
                "sources": []
            })

        # Prepare context from relevant chunks
        context = "\n\n".join(relevant_chunks)

        # Generate response using OpenAI
        messages = [
            {"role": "system", "content": "You are a helpful assistant that answers questions based on the provided context. "
                                        "Always be truthful and if you're not sure about something, say so."},
            {"role": "user", "content": f"Context:\n{context}\n\nQuestion: {query_text}"}
        ]

        # Set API key
        openai.api_key = Config.OPENAI_API_KEY
        
        # Make API call
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=messages,
            temperature=0.7,
            max_tokens=500
        )

        # Return response with sources
        unique_sources = list(set(sources))
        return jsonify({
            "response": response.choices[0].message["content"],
            "sources": unique_sources
        })

    except Exception as e:
        logger.error(f"Error in query: {str(e)}")
        return jsonify({"error": str(e)}), 500
