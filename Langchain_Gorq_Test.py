import getpass
import os

if "GROQ_API_KEY" not in os.environ:
    #os.environ["GROQ_API_KEY"] = getpass.getpass("Enter your Groq API key: ")
    os.environ["GROQ_API_KEY"] = ""


from langchain_groq import ChatGroq

llm = ChatGroq(
    #model="deepseek-r1-distill-llama-70b",
    model="llama3-8b-8192",
    temperature=0,
    max_tokens=None,
    #reasoning_format="parsed",
    timeout=None,
    max_retries=2,
    # other params...
)

messages = [
    (
        "system",
        "You are a helpful assistant that translates English to French. Translate the user sentence.",
    ),
    ("human", "I love programming."),
]
ai_msg = llm.invoke(messages)
print(ai_msg.content)