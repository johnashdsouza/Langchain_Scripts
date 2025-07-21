import getpass
import os

from langchain_groq import ChatGroq
#from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.embeddings import HuggingFaceEmbeddings



if "GROQ_API_KEY" not in os.environ:
    #os.environ["GROQ_API_KEY"] = getpass.getpass("Enter your Groq API key: ")
    os.environ["GROQ_API_KEY"] = ""

if "HUGGINGFACEHUB_API_TOKEN" not in os.environ:
    os.environ["HUGGINGFACEHUB_API_TOKEN"] = ""



llm = ChatGroq(model_name = 'llama-3-8b-8192')
embedding_model = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")

from langchain.vectorstores import Chroma

# Create or connect to a persistent ChromaDB
db = Chroma(collection_name="my_collection", embedding_function=embedding_model, persist_directory="./chroma_db")

from langchain.schema import Document

texts = ["Gorq is a multi-agent workflow orchestration tool.", "LangChain enables chaining of LLM calls."]
documents = [Document(page_content=t) for t in texts]

db.add_documents(documents)

query = "What is Gorq?"
results = db.similarity_search(query, k=1)

for res in results:
    print(res.page_content)