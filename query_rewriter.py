from langchain.output_parsers import CommaSeparatedListOutputParser
from langchain.prompts import PromptTemplate
from langchain_core.runnables import RunnableLambda, RunnablePassthrough
from langchain_google_genai.chat_models import ChatGoogleGenerativeAI  # Use this import only
import os

llm = ChatGoogleGenerativeAI(
    model="gemini-1.5-flash",
    google_api_key=os.getenv("GOOGLE_API_KEY"),
    convert_system_message_to_human=True  # Optional but recommended for chat mode
)

# Prompt for legal rephrasing
legal_rephrase_prompt = PromptTemplate.from_template(
    """
    You are a legal language assistant.
    Convert the following user query into a formal legal research query:

    User Query:
    {query}

    Formal Legal Query:
    """
)

# Prompt for decomposition into subqueries
decompose_prompt = PromptTemplate.from_template(
    """
    If the following user query contains multiple legal sub-questions or tasks, break it into smaller parts.
    Otherwise, just return the query as is. Output should be a comma-separated list.

    User Query:
    {query}

    Sub-queries:
    """
)

decompose_chain = (decompose_prompt | llm | CommaSeparatedListOutputParser())
rephrase_chain = (legal_rephrase_prompt | llm)

def rewrite_and_decompose(query: str) -> list:
    """
    Rewrites the user query into legal language and decomposes if needed.

    Args:
        query (str): Raw user input

    Returns:
        list[str]: One or more rewritten legal queries
    """
    try:
        sub_queries = decompose_chain.invoke({"query": query})
        rewritten = []
        for sub_q in sub_queries:
            formal = rephrase_chain.invoke({"query": sub_q.strip()})
            rewritten.append(formal.strip())
        return rewritten
    except Exception as e:
        print("Error in query rewriting:", e)
        return [query]  # Fallback to original query
