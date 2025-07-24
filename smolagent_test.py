from smolagents import WebSearchTool,CodeAgent, InferenceClientModel
import os

search_tool = WebSearchTool()
print(search_tool("Who's the current president of Russia?"))



from smolagents import tool

@tool
def model_download_tool(task: str) -> str:
    """
    This is a tool that returns the most downloaded model of a given task on the Hugging Face Hub.
    It returns the name of the checkpoint.

    Args:
        task: The task for which to get the download count.
    """
    most_downloaded_model = next(iter(list_models(filter=task, sort="downloads", direction=-1)))
    return most_downloaded_model.id




# This worked alright with the right key
os.environ["HUGGINGFACE_API_KEY"] = ""
model = InferenceClientModel(
  provider="together",
  model="mistralai/Mixtral-8x7B-Instruct-v0.1",
   api_key=os.environ["HUGGINGFACE_API_KEY"]
)


# Below did not work
os.environ["GROQ_API_KEY"] = ""

model1 = InferenceClientModel(
    provider="groq",
    model="llama3-70b-8192",  # or other supported Groq models
    api_key=os.environ["GROQ_API_KEY"]
)

agent = CodeAgent(tools=[model_download_tool], model=model)


'''
agent.run(
    "Can you give me the name of the model that has the most downloads in the 'text-to-video' task on the Hugging Face Hub?"
)
'''