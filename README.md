# arronwh

## Description  
This repository implements a FastAPI-based AI chat and voice assistant system integrated with OpenAI models and various NLP tools. It features a web server with CORS middleware, a chat router for handling AI chatbot endpoints, and real-time voice interaction via WebSocket. The project uses embedding models, document processing utilities, and a persistent vector database (ChromaDB) for knowledge retrieval. It supports audio transcription with Whisper, MongoDB for data storage, and includes tools for structured quote creation and database querying. Configuration and hyperparameters are managed through dedicated modules. The system facilitates dynamic, context-aware AI responses with retrieval-augmented generation and prompt management.

## Run Instructions  
1. Clone the repository:  
   `git clone <repo-url>`  
2. Create a virtual environment:  
   `py -3.13 -m venv venv`  
3. Activate the virtual environment:  
   - On Windows:  
     `venv\Scripts\activate`  
   - On Unix/Mac:  
     `source venv/bin/activate`  
4. Install dependencies:  
   `pip install -r requirements.txt`  
5. Run only the important files:  
   - `python main.py`  
   - `python test.py`  
   - `python test_1.py`  
   - `python test_2.py`  

## Folder Structure  
```
arronwh  
|-- .python-version  
|-- main.py  
|-- pyproject.toml  
|-- README.md  
|-- test.py  
|-- test_1.py  
|-- test_2.py  
|-- test_html.html  
|-- uv.lock  
|-- api  
|   |-- router  
|   |   |-- chat_route.py  
|   |-- schemas  
|       |-- chat_body.py  
|-- src  
|   |-- hyper_parameters.py  
|   |-- config  
|   |   |-- config_audio_model.py  
|   |   |-- config_chat_model.py  
|   |   |-- config_chromadb.py  
|   |   |-- config_db.py  
|   |   |-- config_embedding_model.py  
|   |-- controller  
|   |   |-- agent_controller.py  
|   |-- db  
|   |   |-- db_queries.py  
|   |-- services  
|   |   |-- data_processor.py  
|   |   |-- delete_path.py  
|   |   |-- process_result.py  
|   |   |-- prompt_templete.py  
|   |   |-- rag_knowledge.py  
|   |-- tools  
|       |-- create_quote.py  
|       |-- database_tools.py  
|       |-- quote_tool.py  
```

## File Descriptions  
- `.python-version`: Specifies Python interpreter version 3.13 for environment consistency.  
- `main.py`: FastAPI app with CORS middleware and chat router for AI chatbot endpoints.  
- `pyproject.toml`: Project metadata and dependency specification for Python 3.13 and required libraries.  
- `README.md`: Project overview, purpose, setup instructions, and usage guidelines.  
- `test.py`: FastAPI WebSocket server enabling real-time voice interaction with OpenAI GPT-4o assistant.  
- `test_1.py`: Script demonstrating ChatOpenAI model initialization and basic prompt-response interaction.  
- `test_2.py`: Script reading and processing DOCX document content using DataProcessor.  
- `test_html.html`: HTML page for real-time voice call test via WebSocket with audio capture and playback.  
- `uv.lock`: Dependency lock file ensuring reproducible installs with pinned package versions.  
- `api/router/chat_route.py`: FastAPI router handling chatbot API endpoint with retrieval-augmented generation.  
- `api/schemas/chat_body.py`: Pydantic models for validating and structuring chat history and user queries.  
- `src/hyper_parameters.py`: Configuration of AI model parameters, database paths, and data collection settings.  
- `src/config/config_audio_model.py`: Defines AudioModel class for audio transcription using OpenAI Whisper.  
- `src/config/config_chat_model.py`: Defines ChatModels class to configure and instantiate ChatOpenAI models with tools.  
- `src/config/config_chromadb.py`: Manages ChromaDB vector store for embedding storage and semantic search.  
- `src/config/config_db.py`: Loads environment variables and connects to MongoDB database.  
- `src/config/config_embedding_model.py`: Defines Embedder class to create text embedding models using SentenceTransformer.  
- `src/controller/agent_controller.py`: Integrates chat model with external tools to generate context-aware AI responses.  
- `src/db/db_queries.py`: Provides database query methods for MongoDB with field selection and filters.  
- `src/services/data_processor.py`: Utility class for cleaning text and managing chat/document history preprocessing.  
- `src/services/delete_path.py`: Forcefully deletes directories including read-only files with error handling.  
- `src/services/process_result.py`: Handles chat response processing using model configuration (constructor naming error present).  
- `src/services/prompt_templete.py`: Generates concise prompt templates from chat history with formatting instructions.  
- `src/services/rag_knowledge.py`: Manages knowledge base embedding, storage, and retrieval using embeddings and ChromaDB.  
- `src/tools/create_quote.py`: Defines data models and function to create new quotes via backend API interaction.  
- `src/tools/database_tools.py`: Provides database querying tools for retrieving data from MongoDB collections.  
- `src/tools/quote_tool.py`: Implements a strict sequential quiz tool to collect user information for quotes.