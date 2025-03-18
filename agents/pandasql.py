# csv and pandas
import pandas as pd
import pandasql as psql
from llama_index.core.tools import FunctionTool
from llama_index.core.agent.workflow import AgentWorkflow

iris_df = pd.read_csv('./data/tables/iris.csv')

def basic_info():
    """
    get basic info tuple about the Pandas Dataframe.
    returns a tuple containining (df.shape, df.columns)
    """
    shape = iris_df.shape
    columns = iris_df.columns
    return shape, columns

# Define SQL execution function
def query_sql(sql: str):
    status = 'FAIL'
    """Executes a SQL query on the Pandas DataFrame."""
    try:
        result = psql.sqldf(sql, globals())
        result = result.to_dict()
        status = "OKAY"
    except Exception as e:
        result = str(e)
    # print(f'[{status}] query_sql/in:', sql)
    # print(f'[{status}] query_sql/out:', result)
    return result

# Create a FunctionTool for SQL execution
sql_tool = FunctionTool.from_defaults(fn=query_sql)

def get(llm):
    # Create an enhanced workflow with both tools
    agent = AgentWorkflow.from_tools_or_functions(
        [basic_info, sql_tool],
        llm=llm,
        system_prompt="""You are the expert on Iris data. 
        The data is loaded as a Pandas DataFrame and stored in 'iris_df' variable. 
        Carefully listen to user and use available tools.
        Remember, complex request can be done by creating SQL command with "FROM iris_df".
        Then use the results of the SQL to answer the question.""",
    )
    
    return agent