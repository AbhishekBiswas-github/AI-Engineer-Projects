# ⚡ QuickQuery

> **Natural Language → SQL · RAG Pipeline**
> 
> Ask questions about your database in plain English. QuickQuery translates them into validated, optimised SQL queries using a two-stage RAG pipeline powered by Pinecone, Groq, and LangChain.

<br>

-----

## 📋 Table of Contents

- [Overview](#-overview)
- [Features](#-features)
- [Tech Stack](#-tech-stack)
- [Project Structure](#-project-structure)
- [Architecture & Pipeline](#-architecture--pipeline)
  - [Phase 1 — One-Time Setup](#phase-1--one-time-setup-vector_db_configpy)
  - [Phase 2 — Runtime Query Pipeline](#phase-2--runtime-query-pipeline)
  - [Two-Stage Retrieval](#two-stage-retrieval-content_extractionpy)
  - [Prompt Construction](#prompt-construction-prompt_creationpy)
  - [SQL Generation & Retry Loop](#sql-generation--retry-loop-generationpy)
  - [Validation Layer](#validation-layer-validation_sqlpy)
- [Database Schema](#-database-schema-ecommerce_db)
- [Environment Variables](#-environment-variables)
- [Installation](#-installation)
- [Running the App](#-running-the-app)
- [Configuration & Tuning](#-configuration--tuning)
- [Module Reference](#-module-reference)
- [Author](#-author)

<br>

-----

## 🧭 Overview

QuickQuery is a **Retrieval-Augmented Generation (RAG)** application that bridges the gap between plain English and structured SQL. Instead of hardcoding schema knowledge into a prompt, it dynamically retrieves only the most relevant table schemas from a Pinecone vector index, feeds them to an LLM, and validates the generated SQL against a live database before returning it to the user.

```
User: "Which customer spent the most money last month?"
         ↓
QuickQuery: SELECT c.first_name, c.last_name, SUM(o.total_amount) AS total_spent
            FROM customers c
            JOIN orders o ON c.customer_id = o.customer_id
            WHERE o.created_at >= DATE_SUB(CURDATE(), INTERVAL 1 MONTH)
            GROUP BY c.customer_id
            ORDER BY total_spent DESC
            LIMIT 1;
```

<br>

-----

## ✨ Features

|Feature                            |Description                                                               |
|-----------------------------------|--------------------------------------------------------------------------|
|**Natural Language Input**         |Ask any question about your data — no SQL knowledge required              |
|**RAG-based Schema Retrieval**     |Only relevant tables are fetched from Pinecone — not the entire schema    |
|**Two-Stage Retrieval**            |Bi-encoder ANN search followed by cross-encoder reranking for precision   |
|**Conversation Context**           |Sliding window of last 5 turns — follow-up queries work naturally         |
|**Auto-Retry with Self-Correction**|Up to 3 attempts; failed SQL + error message fed back to LLM              |
|**Multi-dialect Support**          |MySQL, PostgreSQL, Oracle — dialect injected into the prompt              |
|**Live Validation**                |Every generated query is executed against the real database before display|
|**Table Browser**                  |Browse any table in the connected database with a 5-row preview           |
|**Query Results Viewer**           |Execute the last generated query and view paginated results               |
|**Dark Theme UI**                  |Professional dark-mode Streamlit interface with sticky tab navigation     |

<br>

-----

## 🛠 Tech Stack

### Core

|Layer                |Tool                                              |Version / Notes                             |
|---------------------|--------------------------------------------------|--------------------------------------------|
|**Frontend**         |[Streamlit](https://streamlit.io/)                |`>=1.30` — web UI, session state, chat input|
|**LLM**              |[Groq](https://groq.com/) — `llama-3.1-8b-instant`|Fast inference via GroqCloud API            |
|**LLM Orchestration**|[LangChain](https://www.langchain.com/)           |Prompt templates, chains, message objects   |
|**Vector Database**  |[Pinecone](https://www.pinecone.io/)              |Serverless index on AWS `us-east-1`         |
|**Embedding Model**  |[SentenceTransformers](https://www.sbert.net/)    |Bi-encoder via HuggingFace Hub              |
|**Reranker Model**   |`cross-encoder/ms-marco-MiniLM-L6-v2`             |Cross-encoder from HuggingFace Hub          |
|**Database**         |MySQL                                             |`mysql-connector-python` driver             |
|**Data Layer**       |[pandas](https://pandas.pydata.org/)              |Query results returned as DataFrames        |

### Python Libraries

```txt
langchain
langchain_core
langchain_community
langchain_groq
streamlit
python-dotenv
pinecone
mysql-connector-python
huggingface_hub
sentence-transformers
pandas
```

### External Services & APIs

|Service            |Purpose                          |Credential                                    |
|-------------------|---------------------------------|----------------------------------------------|
|**Groq API**       |LLM inference (SQL generation)   |`GROQ_API_KEY`                                |
|**Pinecone**       |Vector index storage & ANN search|`PINECONE_API_KEY`                            |
|**HuggingFace Hub**|Embedding model download         |`HUGGINGFACE_API_KEY`                         |
|**MySQL Server**   |Source database                  |`HOST`, `DB_USER`, `DATABASE_PASSWORD`, `PORT`|

<br>

-----

## 📁 Project Structure

```
quickquery/
│
├── app.py                   ← Streamlit frontend — UI, session state, tab routing
├── generation.py            ← Top-level pipeline — orchestrates all modules
├── prompt_creation.py       ← LangChain prompt builders (initial + regeneration)
├── content_extraction.py    ← Two-stage retrieval: Pinecone ANN + cross-encoder rerank
├── validation_sql.py        ← SQL execution & result/error capture
├── mysql_connection.py      ← All MySQL operations (connect, schema, query)
├── vector_db_config.py      ← One-time setup: embed schemas → upsert to Pinecone
├── column_description.py    ← 93 semantic column descriptions across 8 tables
├── global_veriables.py      ← Shared config: env validation, clients, constants
│
├── requirements.txt         ← Python dependencies
├── .env                     ← Secret credentials (never commit this)
└── README.md                ← This file
```

<br>

-----

## 🏗 Architecture & Pipeline

QuickQuery has two distinct operational phases:

```
┌─────────────────────────────────────────────────────────────────┐
│  PHASE 1 — ONE-TIME SETUP (run once, or on schema change)       │
│                                                                  │
│   MySQL DB ──► get_schemas() ──► schema text ──► SentenceTransformer │
│                                                        ↓         │
│                                               Pinecone Index     │
└─────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────┐
│  PHASE 2 — RUNTIME (every user query)                           │
│                                                                  │
│   User Input ──► content_extraction() ──► relevant schemas      │
│                         ↓                        ↓              │
│              build_history_message()    prompt_creation()        │
│                         ↓                        ↓              │
│                         └──────────► chain.invoke()             │
│                                           ↓                     │
│                                      Groq LLM                   │
│                                           ↓                     │
│                                     SQL Query                   │
│                                           ↓                     │
│                                   validation_sql()              │
│                                     ↙         ↘                 │
│                                 Success       Failed            │
│                                    ↓              ↓             │
│                              Return result   Retry (×3)         │
└─────────────────────────────────────────────────────────────────┘
```

<br>

### Phase 1 — One-Time Setup (`vector_db_config.py`)

Run this script **once** after setting up your MySQL database, and again any time the schema changes (new tables, renamed columns, etc.).

```
python vector_db_config.py
```

**What it does:**

```
vector_creation()
    │
    ├─ creating_index("index-quickquery")
    │       └─ PINECONE_CLIENT.create_index(
    │               dimension = embedding_model dimension,
    │               metric    = "cosine",
    │               spec      = ServerlessSpec(aws, us-east-1)
    │          )
    │
    └─ get_main_sql("ecommerce_db")
            │
            ├─ get_tables()       ← SHOW TABLES FROM ecommerce_db
            │
            └─ get_schemas()
                    │
                    ├─ DESCRIBE {table}
                    │     └─ Enriched with COLUMN_DESCRIPTIONS (93 entries)
                    │
                    ├─ SELECT COUNT(*) FROM {table}
                    │
                    └─ INFORMATION_SCHEMA.KEY_COLUMN_USAGE
                          └─ Foreign key relationships
                    │
                    └─► schema_to_string()
                              └─► EMBEDDING_MODEL.encode()
                                        └─► Pinecone.upsert(vectors, metadata)
```

**Each Pinecone vector stores:**

```json
{
  "id": "quickquery_0",
  "values": [ 0.023, -0.14, 0.087, ... ],
  "metadata": {
    "table":         "orders",
    "columns":       [ "Column: order_id, Description: ..., Data Type: int, ..." ],
    "total_records": "There are 450 records.",
    "foreign_key":   [ "orders.customer_id references customers.customer_id" ]
  }
}
```

> **Why enrich with column descriptions?**
> Bare column names like `status`, `total_amount`, or `is_active` are ambiguous.
> The 93 descriptions in `column_description.py` give the LLM semantic context
> (e.g. `"status"` → `"Current fulfillment status: pending, confirmed, processing, shipped, delivered, cancelled, refunded, or on_hold"`), which dramatically improves SQL accuracy.

<br>

### Phase 2 — Runtime Query Pipeline

Every time a user submits a question in the chat interface, this full pipeline executes:

```
app.py
  │
  └─► generation(user_query, database_name, message_history, dialect)
            │
            ├─ content_extraction()     ← ONCE before retry loop
            │
            ├─ build_history_message()  ← ONCE, sliding window of last 5 turns
            │
            └─ for attempt in 1..3:
                    │
                    ├─ attempt == 1:
                    │     build_prompt(FEW_SHOT_EXAMPLES) | MODEL
                    │     chain.invoke({ dialect, schema, user_question, history })
                    │
                    └─ attempt > 1:
                          build_regeneration_prompt() | MODEL
                          chain.invoke({ schema, sql_query, error, user_query })
                    │
                    └─ re.sub(r"```sql|```", "", response.content).strip()
                    │
                    └─ validation_sql(query, user_query, database_name, attempt)
                              │
                              ├─ Status == "Success" → return result
                              └─ Status == "Failed"  → feed error into next attempt
```

<br>

### Two-Stage Retrieval (`content_extraction.py`)

A single semantic search is insufficient for schema retrieval — a query like `"top selling products"` could match the `products`, `order_items`, or `orders` table by cosine similarity alone. QuickQuery uses two models in sequence:

```
User Query: "which customer spent the most money"
         │
         ▼
┌────────────────────────────────────────────────────────┐
│  STAGE 1 — BI-ENCODER (fast, approximate)              │
│                                                        │
│  SentenceTransformer.encode(user_query)                │
│         ↓                                              │
│  query_vector = [0.023, -0.14, 0.087, ...]             │
│         ↓                                              │
│  Pinecone.query(vector, top_k=5)                       │
│         ↓                                              │
│  5 candidate schema chunks (by cosine similarity)      │
└────────────────────────────────────────────────────────┘
         │
         ▼
┌────────────────────────────────────────────────────────┐
│  STAGE 2 — CROSS-ENCODER (slower, precise)             │
│                                                        │
│  For each candidate:                                   │
│    pair = (user_query, json(candidate.metadata))       │
│                                                        │
│  CrossEncoder("ms-marco-MiniLM-L6-v2").predict(pairs)  │
│         ↓                                              │
│  Rerank scores: [4.2, 1.1, 0.3, -0.8, -2.1]          │
│         ↓                                              │
│  Filter: score >= MIN_SCORE_THRESHOLD (0.0)            │
│         ↓                                              │
│  Return top 3 chunks by rerank score                   │
└────────────────────────────────────────────────────────┘
         │
         ▼
  3 schema chunks → prompt_creation.py
```

**Why two stages?**

|            |Bi-Encoder                           |Cross-Encoder                             |
|------------|-------------------------------------|------------------------------------------|
|**Speed**   |Very fast (vector lookup)            |Slower (pair scoring)                     |
|**Accuracy**|Approximate                          |High precision                            |
|**Input**   |Single query vector                  |(query, document) pair                    |
|**Role**    |Broad recall from millions of vectors|Precision reranking of small candidate set|

The bi-encoder casts a wide net cheaply; the cross-encoder picks the best from the net precisely.

<br>

### Prompt Construction (`prompt_creation.py`)

#### Initial Generation Prompt (Attempt 1)

```
┌──────────────────────────────────────────────────────┐
│  SYSTEM                                              │
│  You are an expert SQL query generator.              │
│  Rules: generate only SQL, use schema, dialect={X}   │
│  Use history for follow-up queries.                  │
│  Database Schema: {retrieved schema chunks}          │
├──────────────────────────────────────────────────────┤
│  FEW-SHOT EXAMPLES                                   │
│  Human: "List names all products"                    │
│  AI:    SELECT name FROM products;                   │
│                                                      │
│  Human: "Customer name with max order amount"        │
│  AI:    SELECT * FROM customers WHERE ...            │
├──────────────────────────────────────────────────────┤
│  HISTORY (MessagesPlaceholder — last 5 turns)        │
│  Human: "Show me all orders from last month"         │
│  AI:    SELECT * FROM orders WHERE ...               │
│  Human: "Now group that by customer"                 │  ← follow-up
│  AI:    SELECT customer_id, COUNT(*) ...             │
├──────────────────────────────────────────────────────┤
│  HUMAN                                               │
│  {current user question}                             │
└──────────────────────────────────────────────────────┘
```

#### Regeneration Prompt (Attempt 2+)

```
┌──────────────────────────────────────────────────────┐
│  SYSTEM                                              │
│  You are an expert SQL query generator.              │
│  Schema: {same retrieved schema chunks}              │
│                                                      │
│  Generated query:                                    │
│    SELECT ... (broken SQL from previous attempt)     │
│                                                      │
│  Error:                                              │
│    "Unknown column 'custmer_id' in field list"       │
│                                                      │
│  Rewrite to fix the error. NO PREAMBLE.              │
├──────────────────────────────────────────────────────┤
│  HUMAN                                               │
│  {original user question}                            │
└──────────────────────────────────────────────────────┘
```

> **Note:** History is intentionally excluded from the regeneration prompt. It is a focused error-correction loop — adding prior conversation turns would increase token usage and risk distracting the LLM from the specific fix needed.

<br>

### SQL Generation & Retry Loop (`generation.py`)

```
generation(user_query, database_name, message_history, dialect)
│
├─ schema  = content_extraction(query, CANDIDATE_K=5, FINAL_TOP_K=3)
├─ history = build_history_message(message_history)   ← sliding window
│
└─ for attempt in range(1, MAX_ATTEMPTS+1):   ← MAX_ATTEMPTS = 3
        │
        ├─ attempt 1:  build_prompt()       + FEW_SHOT_EXAMPLES + history
        ├─ attempt 2+: build_regeneration_prompt() + broken_sql + error
        │
        ├─ response = chain.invoke(...)
        ├─ sql = re.sub(r"```sql|```", "", response.content).strip()
        │
        └─ result = validation_sql(sql, user_query, database_name, attempt)
                ├─ Status == "Success" → return immediately
                └─ Status == "Failed"  → store error, continue loop
                                              ↓
                               [ERROR] All attempts exhausted
                               → return last failed result
```

**Conversation context window:**

```
message_history (full list from session state)
         │
         └─ filter: keep "user" + "assistant" only
                    drop "system" + "Generating......"
         │
         └─ windowed = clean[-(MAX_CONTEXT_WINDOW * 2):]
                       = last 10 messages = last 5 turns
         │
         └─ convert to LangChain objects:
                "user"      → HumanMessage(content=...)
                "assistant" → AIMessage(content=...)
         │
         └─ injected via MessagesPlaceholder(variable_name="history")
```

<br>

### Validation Layer (`validation_sql.py`)

```
validation_sql(query, user_query, database_name, attempt)
│
├─ connection = get_connection()
├─ cursor.execute(f"USE {database_name}")
├─ cursor.execute(query)
│
├─ SUCCESS →  {
│               "User Query":      user_query,
│               "Generated Query": query,
│               "Result":          rows,       ← list of tuples
│               "Attempts":        attempt,
│               "Status":          "Success"
│             }
│
└─ FAILURE →  {
                "User Query":      user_query,
                "Generated Query": query,
                "Error":           str(e),     ← fed into regeneration prompt
                "Attempts":        attempt,
                "Status":          "Failed"
              }
```

The `Error` string from a failed attempt is injected verbatim into the regeneration prompt so the LLM receives the exact database error message (e.g. `"Table 'ecommerce_db.custmers' doesn't exist"`) and can correct it precisely.

<br>

-----

## 🗄 Database Schema (`ecommerce_db`)

QuickQuery is designed for the `ecommerce_db` MySQL database containing **8 tables** and **93 documented columns**.

```
ecommerce_db
│
├── customers        (13 cols) ── customer accounts, loyalty points, status
├── categories       ( 8 cols) ── hierarchical product categories
├── products         (19 cols) ── listings, pricing, inventory, ratings
├── addresses        (13 cols) ── shipping/billing addresses per customer
├── orders           (20 cols) ── order lifecycle, payment, fulfilment status
├── order_items      ( 9 cols) ── line items per order with price snapshots
├── product_reviews  (11 cols) ── verified reviews, ratings, moderation
└── coupons          (13 cols) ── discount codes, types, validity, usage limits
```

**Entity-Relationship overview:**

```
customers ──< addresses
    │
    └──< orders ──< order_items >── products >── categories
           │               │
           └── coupons     └──< product_reviews
```

**Foreign key relationships:**

|Table            |Column               |References              |
|-----------------|---------------------|------------------------|
|`categories`     |`parent_id`          |`categories.category_id`|
|`products`       |`category_id`        |`categories.category_id`|
|`addresses`      |`customer_id`        |`customers.customer_id` |
|`orders`         |`customer_id`        |`customers.customer_id` |
|`orders`         |`shipping_address_id`|`addresses.address_id`  |
|`orders`         |`billing_address_id` |`addresses.address_id`  |
|`order_items`    |`order_id`           |`orders.order_id`       |
|`order_items`    |`product_id`         |`products.product_id`   |
|`product_reviews`|`product_id`         |`products.product_id`   |
|`product_reviews`|`customer_id`        |`customers.customer_id` |
|`product_reviews`|`order_id`           |`orders.order_id`       |

<br>

-----

## 🔐 Environment Variables

Create a `.env` file in the project root with the following keys:

```env
# ── Pinecone ──────────────────────────────────────────
PINECONE_API_KEY=your_pinecone_api_key_here

# ── HuggingFace ───────────────────────────────────────
HUGGINGFACE_API_KEY=your_huggingface_token_here
EMBEDDING_MODEL=sentence-transformers/all-MiniLM-L6-v2

# ── Groq ──────────────────────────────────────────────
GROQ_API_KEY=your_groq_api_key_here

# ── MySQL ─────────────────────────────────────────────
HOST=localhost
DB_USER=root
DATABASE_PASSWORD=your_mysql_password
PORT=3306
```

> ⚠️ **Never commit `.env` to version control.** Add it to `.gitignore` immediately.

`global_veriables.py` validates all 8 variables at startup and exits with a clear error message if any are missing — no silent failures deep in the pipeline.

<br>

-----

## 🚀 Installation

### Prerequisites

- Python `3.10+`
- MySQL Server running locally or remotely
- Pinecone account (free tier works)
- Groq API key (free tier works)
- HuggingFace account (free)

### Steps

**1. Clone the repository**

```bash
git clone https://github.com/your-username/quickquery.git
cd quickquery
```

**2. Create and activate a virtual environment**

```bash
python -m venv venv

# macOS / Linux
source venv/bin/activate

# Windows
venv\Scripts\activate
```

**3. Install dependencies**

```bash
pip install -r requirements.txt
```

> **Note:** `requirements.txt` lists `dotenv` — install `python-dotenv` instead:
> 
> ```bash
> pip install python-dotenv
> ```

**4. Configure environment variables**

```bash
cp .env.example .env
# Edit .env with your credentials
```

**5. Set up the MySQL database**

```bash
mysql -u root -p < ecommerce_db.sql
```

**6. Build the Pinecone vector index (one-time)**

```bash
python vector_db_config.py
```

Expected output:

```
[INFO] Index 'index-quickquery' created successfully.
[INFO] Upserted batch 1 (8 vectors).
[INFO] 8 schema vectors upserted successfully.
```

> If the index already exists:
> 
> ```
> [INFO] Index 'index-quickquery' already exists. Skipping creation.
> [INFO] 'index-quickquery' already populated. Nothing to do.
> ```

<br>

-----

## ▶️ Running the App

```bash
streamlit run app.py
```

The app opens at `http://localhost:8501`.

**First-time flow:**

```
1. Click "⚙️ Configure Database" in the sidebar
2. Enter your MySQL credentials → click "Connect"
3. Select your database from the dropdown → click "Use This Database"
4. Navigate to the 🤖 Chat tab
5. Type your first question and press Enter
```

**Standalone pipeline test (no Streamlit):**

```bash
python generation.py
```

<br>

-----

## ⚙️ Configuration & Tuning

All tunable parameters live in `global_veriables.py`:

|Constant             |Default               |Effect                                                                                                   |
|---------------------|----------------------|---------------------------------------------------------------------------------------------------------|
|`CANDIDATE_K`        |`5`                   |Number of schema chunks fetched from Pinecone before reranking. Higher = better reranker pool but slower.|
|`FINAL_TOP_K`        |`3`                   |Number of chunks passed to the LLM after reranking. Higher = more context but more tokens.               |
|`MAX_ATTEMPTS`       |`3`                   |Max SQL generation + retry attempts.                                                                     |
|`MAX_CONTEXT_WINDOW` |`5`                   |Number of prior conversation turns kept in context.                                                      |
|`MODEL`              |`llama-3.1-8b-instant`|Swap to `llama-3.3-70b-versatile` for higher accuracy at the cost of latency.                            |
|`MIN_SCORE_THRESHOLD`|`0.0`                 |Cross-encoder minimum score to keep a candidate. Raise to increase precision (try `1.0`–`3.0`).          |

**To switch LLM model:**

```python
# global_veriables.py
MODEL = ChatGroq(
    api_key=os.environ.get("GROQ_API_KEY"),
    model="llama-3.3-70b-versatile",   # ← change here
    temperature=0
)
```

**To rebuild the Pinecone index after schema changes:**

```bash
# Delete the index from Pinecone console, then:
python vector_db_config.py
```

<br>

-----

## 📖 Module Reference

|Module                 |Exports                                                                                                                                                         |Called By                                           |
|-----------------------|----------------------------------------------------------------------------------------------------------------------------------------------------------------|----------------------------------------------------|
|`global_veriables.py`  |`PINECONE_CLIENT`, `INDEX_NAME`, `CLOUD_SPECS`, `CANDIDATE_K`, `FINAL_TOP_K`, `FEW_SHOT_EXAMPLES`, `MODEL`, `DATABASE_NAME`, `MESSAGE_HISTORY`                  |All modules                                         |
|`column_description.py`|`COLUMN_DESCRIPTIONS`, `get_description()`                                                                                                                      |`mysql_connection.py`                               |
|`mysql_connection.py`  |`get_connection()`, `list_of_databases()`, `check_connection()`, `get_tables()`, `get_all_records()`, `get_schemas()`, `run_generated_query()`, `get_main_sql()`|`app.py`, `vector_db_config.py`, `validation_sql.py`|
|`vector_db_config.py`  |`creating_index()`, `schema_to_string()`, `schema_upsert()`, `vector_creation()`                                                                                |Run standalone only                                 |
|`content_extraction.py`|`content_extraction()`                                                                                                                                          |`generation.py`                                     |
|`prompt_creation.py`   |`build_prompt()`, `build_regeneration_prompt()`                                                                                                                 |`generation.py`                                     |
|`validation_sql.py`    |`validation_sql()`                                                                                                                                              |`generation.py`                                     |
|`generation.py`        |`generation()`, `build_history_message()`                                                                                                                       |`app.py`                                            |
|`app.py`               |Streamlit entry point                                                                                                                                           |Run via `streamlit run app.py`                      |

<br>

-----

## 👤 Author

**Abhishek Biswas**

-----

<div align="center">

© 2025 QuickQuery  ·  Built with ♥ by **Abhishek Biswas**  ·  Powered by LangChain · Groq · Pinecone

</div>
