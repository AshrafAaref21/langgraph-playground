from dotenv import load_dotenv
from langchain_openai import ChatOpenAI

load_dotenv()

research_llm = ChatOpenAI(model="gpt-4o-mini", temperature=0)
writing_llm = ChatOpenAI(model="gpt-4o-mini", temperature=0.7)
