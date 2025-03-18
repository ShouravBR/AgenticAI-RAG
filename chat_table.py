from llama_index.core import VectorStoreIndex, SimpleDirectoryReader, Settings
from llama_index.core.agent.workflow import AgentWorkflow
from llama_index.core.workflow import Context
from llama_index.llms.ollama import Ollama
from llama_index.embeddings.huggingface import HuggingFaceEmbedding
import asyncio

from agents.pandasql import get as get_pandas_agent


# Settings control global defaults
Settings.embed_model = HuggingFaceEmbedding(model_name="BAAI/bge-base-en-v1.5")
Settings.llm = Ollama(model="llama3.1", request_timeout=360.0)

# Create an enhanced workflow with both tools
agent = get_pandas_agent(Settings.llm)

# AgentWorkflow.from_tools_or_functions(
#     [sql_tool],
#     llm=Settings.llm,
#     system_prompt="""You are a SQLite expert. 
#     Carefully listen to user and create SQL command for 'iris_df' table.""",
# )


# Now we can ask questions about the documents or do calculations
async def main():
    # create context
    ctx = Context(agent)

    examples = [
        "How many samples and columns are there?"
        "What is the min and max sepal length of setosa variety?"
    ]

    print('This is a chatbot to help with find information from Iris data table. Type "exit" to stop.')
    print('Try asking:')
    for e in examples:
        print(e)

    while True:
        query = input(">>> ");
        
        if query == 'exit': break

        response = await agent.run(query, ctx=ctx)
        print('Agent:', response)


# Run the agent
if __name__ == "__main__":
    asyncio.run(main())