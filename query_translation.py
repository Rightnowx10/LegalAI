# query_translation.py
from langchain_google_genai import GoogleGenerativeAI
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import PromptTemplate
import os

def translate_query(query: str) -> str:
    prompt = PromptTemplate.from_template("Convert the following legal query into a more precise, legally contextualized version:\n\n{query}")
    llm = GoogleGenerativeAI(
        model="models/gemini-1.5-flash",
        google_api_key=os.getenv("GOOGLE_API_KEY"),
        temperature=0.2,
    )
    chain = prompt | llm | StrOutputParser()
    return chain.invoke({"query": query})
