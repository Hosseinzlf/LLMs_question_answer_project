from dotenv import load_dotenv
import os
load_dotenv()

from langchain_google_genai import ChatGoogleGenerativeAI

google_api_key = os.environ["GOOGLE_API_KEY"]
llm = ChatGoogleGenerativeAI(model="gemini-2.5-flash",api_key=llm = ChatGoogleGenerativeAI(model="gemini-2.5-flash",api_key=api_key, temprature=0)
)