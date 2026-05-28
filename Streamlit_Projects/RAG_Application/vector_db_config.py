from mysql_connection import get_main_sql
from global_veriables import PINECONE_CLIENT, EMBEDDING_MODEL, INDEX_NAME, CLOUD_SPECS


def creating_index(index_name:str) -> bool:
    """Create Pinecone index if it doesn't exist. Returns True if newly created."""
    index_list = [index.name for index in PINECONE_CLIENT.list_indexes()]
    if INDEX_NAME not in index_list:
        PINECONE_CLIENT.create_index(
            name = INDEX_NAME,
            dimension=EMBEDDING_MODEL.get_embedding_dimension(),
            metric='cosine',
            spec=CLOUD_SPECS
        )
        print(f"[INFO] Index '{index_name}' created.")
        return True
    else:
        print(f"[INFO] Index '{index_name}' already exists.")
        return False

def get_string(schema:dict) -> str:
    """Convert a schema dict into a plain text string for embedding."""
    lines = [f"TABLE_NAME: {schema['table_name']}"]
    for col in schema["column_details"]:
        lines.append(col)
    lines.append(schema["total_records"])
    fk = schema["foreign_key_details"]
    if isinstance(fk, list):
        lines.extend(fk)
    else:
        lines.append(fk)

    return "\n".join(lines)

def schema_upsert(schemas:list, batch_size:int = 100):
    """Embed and upsert all schema vectors into Pinecone in batches."""
    index = PINECONE_CLIENT.Index(name=INDEX_NAME)
    schema_list = []
    for i, schema in enumerate(schemas):
        schema_list.append({
            "id": f"quickquery_{i}",
            "values": EMBEDDING_MODEL.encode(get_string(schema=schema)).tolist(),
            "metadata": {
                "table": schema['table_name'],
                "columns": schema["column_details"],
                "total records": schema["total_records"],
                "foreign key": schema["foreign_key_details"]
            }
        })

    # Upserting in batches
    if len(schema_list) > batch_size:
        for i in range(0, len(schema_list), batch_size):
            batch = schema_list[i:i+batch_size]
            index.upsert(vectors=batch)
            print(f"[INFO] Upserted batch {i // batch_size + 1} ({len(batch)} vectors)")
    else:
        index.upsert(vectors=schema_list)

    print(f"{len(schema_list)} vectors inserted successfully")

def vector_creation():
    """Orchestrate index creation and schema upsert."""
    is_new = creating_index(INDEX_NAME)
    if is_new:
        schemas = get_main_sql()
        if schemas:
            schema_upsert(schemas=schemas)
        else:
            print("[ERROR] No schemas returned from MySQL. Upsert skipped.")
    else:
        print(f"{INDEX_NAME} index already created and data is already exists")
