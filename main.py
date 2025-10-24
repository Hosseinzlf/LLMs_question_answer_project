from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.messages import HumanMessage
import secret_key
api_key = secret_key.GOOGLE_API_KEY
llm = ChatGoogleGenerativeAI(model="gemini-2.5-flash",api_key=api_key)

# Simple text invocation
result = llm.invoke("Give me a joke.")
print(result.content)
