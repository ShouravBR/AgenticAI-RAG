Chatbot agents with document (RAG) and table crunching (SQL) ablities. This repository uses LlamaIndex to create agentic ai workflows. 

Requirements:
- Ollama for easy LLM model management and usage over REST API
- Python enviroment (see requirement.txt)
- at least 8GB RAM (because I used llama3.1 7B model)

How to use:
- clone/copy this repository to your working folder and open a terminal.
- Install Ollama. Open console and install llama-3.1 8B model using `$ ollama pull llama3.1`. 
- Now that you have the LLM model, you can expose it via REST API using `$ ollama serve`
- Install Python and requirements using `pip install -r requirements.txt`. (I suggest using an environment manager)
- Then run `$ python chat.py` to ask questions from documents or `$ python chat_table.py` to ask question about the Fisher Iris dataset