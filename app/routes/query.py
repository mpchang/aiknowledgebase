"""Query route handler for the AI Knowledge Base application.

This module implements the semantic search endpoint that allows users to query
the knowledge base using natural language. It processes queries using embeddings
and GPT to generate contextual responses based on the document store.

The main endpoint /query accepts POST requests with a query string and returns
AI-generated responses with relevant source context.
"""

import logging
from flask import Blueprint, request, jsonify
from openai import OpenAI
from app.config.config import Config
from app.services.container import ServiceContainer

logger = logging.getLogger(__name__)

query_bp = Blueprint('query', __name__)

@query_bp.route("/query", methods=["POST"])
def query():
    """Process semantic search queries against the knowledge base.

    Expects a POST request with JSON payload containing a 'query' field.
    Uses embeddings to find relevant document chunks and generates an AI response.

    Returns:
        JSON response containing:
        - response: AI-generated answer based on relevant context
        - sources: List of source documents used for the response

    Status Codes:
        200: Success
        400: Missing or invalid query
        500: Server error
    """
    try:
        data = request.get_json()
        if not data or "query" not in data:
            return jsonify({"error": "No query provided"}), 400

        query_text = data["query"]
        logger.info("Processing query: %s", query_text)

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

        # Initialize OpenAI client
        client = OpenAI(api_key=Config.OPENAI_API_KEY)
        
        # Make API call
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=messages,
            temperature=0.7,
            max_tokens=500
        )

        # Return response with sources
        unique_sources = list(set(sources))
        return jsonify({
            "response": response.choices[0].message.content,
            "sources": unique_sources
        })

    except Exception as e:
        logger.error(f"Error in query: {str(e)}")
        return jsonify({"error": str(e)}), 500
