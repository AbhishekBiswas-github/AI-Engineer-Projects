from sentence_transformers import SentenceTransformer
from pinecone import Pinecone, ServerlessSpec
import os
from dotenv import load_dotenv
from langchain_groq import ChatGroq
import sys

load_dotenv()

REQUIRED_ENV_VARS = [
    "PINECONE_API_KEY",
    "EMBEDDING_MODEL",
    "HUGGINGFACE_API_KEY",
    "GROQ_API_KEY",
    "HOST",
    "DB_USER",
    "DATABASE_PASSWORD",
    "PORT"
]

missing = [var for var in REQUIRED_ENV_VARS if not os.environ.get(var)]
if missing:
    sys.exit(f"[ERROR] Missing environment variables: {" ".join(missing)}")

# Pinecone connection

PINECONE_CLIENT = Pinecone(
    api_key=os.environ.get("PINECONE_API_KEY")
)

CLOUD_SPECS = ServerlessSpec(
    cloud='aws',
    region='us-east-1'
)

INDEX_NAME = "index-quickquery"

# Embedding model
EMBEDDING_MODEL = SentenceTransformer(
    os.environ.get("EMBEDDING_MODEL"),
    token=os.environ.get("HUGGINGFACE_API_KEY")
)

# USER_QUERY = "Write a query total purchases every year."
# Few shot examples
FEW_SHOT_EXAMPLES = [
    {
        'user_query': "List names all products",
        'response': "select name from products;"
    },
    {
        "user_query": "Customer name with max order amount",
        'response': """SELECT * from customers
WHERE customer_id = (
            Select customer_id from orders
            GROUP BY customer_id
            ORDER BY SUM(total_amount) DESC
            LIMIT 1
);"""
    }
]

# LLM model
MODEL = ChatGroq(
    api_key=os.environ.get("GROQ_API_KEY"),
    model="llama-3.1-8b-instant",
    temperature=0
)

# Database config
DATABASE_NAME = "ecommerce_db"

