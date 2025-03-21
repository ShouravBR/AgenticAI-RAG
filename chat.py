from llama_index.core import VectorStoreIndex, SimpleDirectoryReader, Settings
from llama_index.core.agent.workflow import AgentWorkflow
from llama_index.core.workflow import Context
from llama_index.llms.ollama import Ollama
from llama_index.embeddings.huggingface import HuggingFaceEmbedding
import asyncio

# Later, load the index
from llama_index.core import StorageContext, load_index_from_storage

# Settings control global defaults
Settings.embed_model = HuggingFaceEmbedding(model_name="BAAI/bge-base-en-v1.5")
Settings.llm = Ollama(model="llama3.1", request_timeout=360.0)

# Create a RAG tool using LlamaIndex
try:
    # raise Exception("redo")
    storage_context = StorageContext.from_defaults(persist_dir="storage")
    index = load_index_from_storage(
        storage_context,
        # we can optionally override the embed_model here
        # it's important to use the same embed_model as the one used to build the index
        # embed_model=Settings.embed_model,
    )
except Exception as e:
    print(e)
    documents = SimpleDirectoryReader("data").load_data()
    index = VectorStoreIndex.from_documents(
        documents,
        # we can optionally override the embed_model here
        # embed_model=Settings.embed_model,
    )

query_engine = index.as_query_engine(
    # we can optionally override the llm here
    # llm=Settings.llm,
)


def multiply(a: float, b: float) -> float:
    """Useful for multiplying two numbers."""
    print(f'AI: Multiplying {a} x {b}')
    return a * b


async def search_documents(query: str) -> str:
    """Useful for answering natural language questions about an personal essay written by Paul Graham."""
    print(f'AI: Looking for "{str}" in documents.')

    response = await query_engine.aquery(query)
    return str(response)



# Create an enhanced workflow with both tools
agent = AgentWorkflow.from_tools_or_functions(
    [multiply, search_documents],
    llm=Settings.llm,
    system_prompt="""You are a helpful assistant that can perform calculations
    and search through documents to answer questions. Read each question and answer.
    If you encounter errors, resolve internally and reattempt. 
    Only tell about errors if you are unable to solve it.""",
)


# Now we can ask questions about the documents or do calculations
async def main():
    # create context
    ctx = Context(agent)

    examples = [
        "What was the author's major in college?"
        "Also, what's 7 * 8? Then multiply 2 with the result."
    ]

    print('This is a chatbot to help with do math and find information from a text document. Type "exit" to stop.')
    print('Try asking:')
    for e in examples:
        print(e)

    response = await agent.run(query, ctx=ctx)
    print(response)

    # Save the index
    index.storage_context.persist("storage")


# Run the agent
if __name__ == "__main__":
    asyncio.run(main())