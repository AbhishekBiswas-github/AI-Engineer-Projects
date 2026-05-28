from langchain_core.prompts import (
    HumanMessagePromptTemplate,
    ChatPromptTemplate,
    FewShotChatMessagePromptTemplate,
    SystemMessagePromptTemplate
)



def build_prompt(few_shot_examples: list[dict]):
    """
    Build the initial SQL generation prompt with few-shot examples.

    Expected invoke keys: dialect, schema, user_question
    """
    # Example format
    example_prompt = ChatPromptTemplate.from_messages(
        [
            ("human", "{user_query}"),
            ("ai", "{response}")
        ]
    )

    # Few shot template
    few_shot_prompt = FewShotChatMessagePromptTemplate(
        examples=few_shot_examples,
        example_prompt=example_prompt
    )

    # Final prompt
    final_prompt = ChatPromptTemplate.from_messages(
        [
            ("system", """You are an expert SQL query generator.
Rules:
1. Generate only SQL query.
2. Use the provided database schema.
3. SQL dialect: {dialect}
4. Do not explain the query.
5. Return valid and optimized SQL only.

Database Schema:
{schema}
"""),
            few_shot_prompt,
            ("human", "{user_question}")
        ]
    )

    return final_prompt


def build_regeneration_prompt():
    """
    Build the SQL correction prompt.

    Expected invoke keys: schema, sql_query, error, user_query
    """
    system_prompt = SystemMessagePromptTemplate.from_template(
        template="""You are an expert SQL query generator.

You are given the database schema below:
{schema}

The following SQL query was generated:
{sql_query}

It produced this error:
{error}

Rewrite the query to fix the error using correct syntax, column names, and logic.

NO PREAMBLE. Return only the corrected SQL query.
"""
    )

    human_prompt = HumanMessagePromptTemplate.from_template(
        template="{user_query}"
    )
    
    return ChatPromptTemplate([system_prompt, human_prompt])