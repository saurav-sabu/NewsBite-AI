from langchain_google_genai import GoogleGenerativeAI
from src.prompt import summary_prompt_template
from dotenv import load_dotenv
from langchain_core.output_parsers import JsonOutputParser
from langchain_core.pydantic_v1 import BaseModel, Field

load_dotenv()

class Output(BaseModel):
   Summary: str = Field(description="Summary of the news article based on the desired length")
   Tone: str = Field(description="Sentiment tone of the news article")
   Sentiment_Score: str = Field(description="Sentiment score of the news article")

output_parser = JsonOutputParser(pydantic_object=Output)

def get_summary_response(news_article: str, summary_length: str):

    model = GoogleGenerativeAI(model="gemini-2.0-flash-exp")

    chain = summary_prompt_template | model | output_parser

    response = chain.invoke({"news_article": news_article, "summary_length": summary_length})
    
    return response