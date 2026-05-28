import re
from global_veriables import MODEL, FEW_SHOT_EXAMPLES, DATABASE_NAME
from prompt_creation import build_prompt, build_regeneration_prompt
from content_extraction import content_extraction
from validation_sql import validation_sql

MAX_ATTEMPTS = 3

def generation(user_query:str) -> dict:
    """
    Generate a SQL query for user_query, validate it, and retry on failure.
    Returns the final validation result dict.
    """
    schema = content_extraction(user_query)
    previous_result = None

    for attempt in range(1, MAX_ATTEMPTS + 1):
        print(f"[INFO] Attempt {attempt}")

        if attempt == 1:
            chain = build_prompt(FEW_SHOT_EXAMPLES) | MODEL

            schema = content_extraction(user_query=user_query)

            response = chain.invoke({
                'dialect': "MySQL", 
                'schema': schema, 
                'user_question': user_query, 
            })

        else:
            chain = build_regeneration_prompt() | MODEL

            schema = content_extraction(user_query=user_query)

            response = chain.invoke({
        'error': previous_result["Error"],
        'schema': schema,
        'sql_query': previous_result["Generated Query"],
        'user_query': user_query
            })

        sql_query = re.sub(r"```sql|```", "", response.content).strip()  
        result = validation_sql(query=sql_query, user_query=user_query, attempt=attempt)

        if result['Status'] == "Success":
            print(f"[INFO] Query succeeded on attempt {attempt}.")
            return result
        
        print(f"[WARN] Attempt {attempt} failed: {result.get('Error')}")
        previous_result = result

    print("[ERROR] All attempts exhausted. Returning last failed result.")
    return previous_result

if __name__ == "__main__":
    query = "Write a query for give all persons names with total purchased in last 2 months from last delivery."
    result = generation(query)
    if result['Status'] == "Failed":
        print(f"""User input is not appropriate. Provide more information.
Below is the query which I have generated: 
{result['Generated Query']}
But getting below error:
{result["Error"]}
""")
    else:
        print(result['Generated Query'])
