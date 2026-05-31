# Project Setup Guide

Follow the steps below to set up and run the project successfully.

## 🚀 Setup Instructions

1. **Create a Virtual Environment**

   ```bash
   python -m venv [ENV_NAME]
   ```

2. **Bypass Script Execution Policy (If Required)**  
   Some systems (especially Windows) block script execution by default.  
   To temporarily bypass this restriction, run:

   ```powershell
   Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
   ```

3. **Activate the Virtual Environment**  
   Activate the environment so that all packages install inside it:

   ```bash
   .\[ENV_NAME]\Scripts\activate
   ```

4. **Install Required Packages**  
   Install all dependencies listed in `requirements.txt`:

   ```bash
   pip install -r requirements.txt
   ```

5. **Run the Application**

   ```bash
   streamlit run app.py
   ```

---

✅ Your application should now be running successfully!



# Project Description

Here is the updated `README.md` file, incorporating the specific technologies and configurations revealed in your `global_veriables.py` file. I have added a "Tech Stack" section and updated the module descriptions and the environment variable requirements to reflect your use of Pinecone, Groq (LLaMA 3), HuggingFace, and LangChain.

***

```markdown
# QuickQuery

QuickQuery is an AI-powered data extraction and querying pipeline designed to translate natural language into validated SQL queries for an e-commerce database (`ecommerce_db`). It integrates vector databases for semantic context retrieval, automated prompt engineering, and secure database connections to ingest, generate, and validate data queries seamlessly.

## 🛠️ Tech Stack
* **LLM**: Groq (Llama-3.1-8b-instant via LangChain)
* **Vector Database**: Pinecone (AWS, us-east-1)
* **Embeddings**: HuggingFace Sentence Transformers
* **Database**: MySQL

## 📂 Project Directory Layout

```text
QUICKQUERY/
│
├── __pycache__/                 # Compiled Python bytecode files
├── data_ingestion/              # Handles database connectivity and schema metadata
│   ├── column_description.py    # Fetches or stores descriptions/metadata of DB columns
│   └── mysql_connection.py      # Manages the secure connection to the MySQL database
│
├── extraction/                  # Base data or context extraction modules
│   └── content_extraction.py    # Logic for extracting specific content or context from sources
│
├── extraction_n_prompting/      # Core LLM prompt building and context retrieval
│   ├── content_extraction.py    # Extracts relevant context required for the specific query
│   └── prompt_creation.py       # Combines user input, few-shot examples, and context to engineer the LLM prompt
│
├── generation/                  # LLM integration and query validation
│   ├── generation.py            # Interfaces with the Groq LLaMA model to generate the SQL query
│   └── validation_sql.py        # Validates the generated SQL syntax and ensures execution safety
│
├── quickquery/                  # Core application package or internal modules folder
│
├── setup/                       # Configuration and environment setup
│   ├── .env                     # Stores sensitive environment variables
│   └── global_veriables.py      # Core initializations (Pinecone client, Groq LLM, Embeddings, Few-Shot examples)
│
├── vector_store/                # Vector database configuration for semantic search (RAG)
│   └── vector_db_config.py      # Configuration for connecting and querying the Pinecone index (`index-quickquery`)
│
├── app.py                       # Main application entry point
└── requirements.txt             # List of Python dependencies required to run the project
```

## 🧩 Module Breakdown

### 1. Root Files
*   **`app.py`**: The main driver script of the project. It handles user inputs and orchestrates the flow between data ingestion, prompting, generation, and displaying the final results.

### 2. `data_ingestion/`
Responsible for interacting directly with your SQL database.
*   **`mysql_connection.py`**: Establishes the connection to `ecommerce_db`.
*   **`column_description.py`**: Pulls schema details and column descriptions.

### 3. `vector_store/`
*   **`vector_db_config.py`**: Interacts with the initialized Pinecone client to store and quickly retrieve database schema embeddings or past successful queries for semantic context.

### 4. `extraction_n_prompting/`
This is where the RAG (Retrieval-Augmented Generation) pipeline lives.
*   **`content_extraction.py`**: Pulls the most relevant context from the vector store.
*   **`prompt_creation.py`**: Assembles the system prompt, user query, database schema context, and the predefined `FEW_SHOT_EXAMPLES` into a strict prompt ready for the LLM.

### 5. `generation/`
*   **`generation.py`**: Sends the crafted prompt to the Groq `llama-3.1-8b-instant` model and receives the raw generated SQL.
*   **`validation_sql.py`**: Parses the LLM's response and checks for SQL syntax errors.

### 6. `setup/`
*   **`global_veriables.py`**: The central configuration hub. It validates environment variables, initializes the `Pinecone` client, sets up the HuggingFace `SentenceTransformer` embedding model, loads static `FEW_SHOT_EXAMPLES` for prompt injection, and initializes the LangChain `ChatGroq` model.
*   **`.env`**: Holds the required sensitive variables locally. To run this project, your `.env` must include:
    * `PINECONE_API_KEY`
    * `EMBEDDING_MODEL`
    * `HUGGINGFACE_API_KEY`
    * `GROQ_API_KEY`
    * `HOST`
    * `DB_USER`
    * `DATABASE_PASSWORD`
    * `PORT`

---

## ⚙️ Architecture & Execution Flow
```
flowchart TD
    User([👤 User]) -->|Natural Language Query| App(app.py)
    App --> Prompting(prompt_creation.py)
    
    %% Context Gathering
    Prompting <-->|Retrieve schema context| ColumnMeta(column_description.py)
    Prompting <-->|Semantic Search via SentenceTransformers| VectorStore(Pinecone Vector DB)
    Prompting <-->|Inject Few-Shot Examples| GlobalVars(global_veriables.py)
    
    %% Generation
    Prompting -->|Structured Prompt| Generator(generation.py)
    Generator <-->|LangChain| LLM((Groq LLaMA 3.1))
    Generator -->|Raw SQL Query| Validator(validation_sql.py)
    
    %% Execution
    Validator -->|Validated SQL| DBConnection(mysql_connection.py)
    DBConnection <-->|Execute and Fetch| MySQL[(ecommerce_db)]
    
    %% Results Back to User
    DBConnection -->|Query Results| App
    App -->|Formatted Output| User
```
