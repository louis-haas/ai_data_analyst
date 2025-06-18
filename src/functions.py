import duckdb
import pandas as pd
from dotenv import load_dotenv
import os
from langchain_anthropic import ChatAnthropic
from langchain_core.messages import SystemMessage, HumanMessage
from schemas import Dataset, ListAnalyticsMethods, SQLQuery
import plotly
from jinja2 import Environment, FileSystemLoader
import webbrowser

# Initialize the ChatAnthropic client

load_dotenv()

llm_smart = ChatAnthropic(
    model="claude-sonnet-4-20250514",
    api_key= os.getenv('my_anthropic_api'),
    temperature=0,
    timeout=None,
    max_retries=2,
)

llm_fast = ChatAnthropic(
    model="claude-3-5-haiku-latest",
    api_key= os.getenv('my_anthropic_api'),
    temperature=0,
    timeout=None,
    max_retries=2,
)


def init_duckdb(csv_path: str):
    
    connection = duckdb.connect(database=':memory:')
    connection.execute(f"CREATE TABLE data_table as SELECT * from read_csv('{csv_path}', header = True, auto_detect=True)")
    df = connection.execute("SELECT * FROM data_table").fetchdf()
    
    return connection, df


def summarize_dataframe(df):
        
    prompt = f"""

    Categorize and describe each field in this dataset.

    **Requirements**
    For each field:
    1. Category: Choose from time dimension, categorical dimension, monetary dimension, monetary metric, additive metric, ratio metric, or Other
    2. Description: Write a brief description. For dimensions only, add some possible values to the description.

    **Input**
    Dataset columns: {', '.join(df.columns)}
    Data preview: {df.head().to_string()}

    """
    
    structured_llm = llm_fast.with_structured_output(Dataset, include_raw=True)
    response = structured_llm.invoke([HumanMessage(prompt)])
    
    return response['parsed'].fields


def write_sql_query(df, guideline):

    prompt = f"""

    Write a valid SQL query following the guideline below.

    **Requirements:**
    - Return only raw SQL code without formatting or code blocks

    **Inputs:**   
    Guideline : ### {guideline} ###
    Database: ### You can only the table named "data_table" which contains the following columns: {', '.join(df.columns)} ###
    
    """

    response = llm_fast.invoke([HumanMessage(prompt)])

    return response.content
    


def run_sql_query(connection, sql_query):

    return connection.execute(sql_query).fetchdf()
    
def perform_analytical_task(question, task_assignment, df):

    prompt = f"""

    Perform the analytical task on the dataframe and summarize your findings using bullet points. Format the output in HTML.

    **Requirements:**
    - Format: Plain HTML text only (no code blocks or markdown)
    - No title
    - Convert decimals to percentages (0.8542 → 85.4%)

    **Inputs:**   
    Analytics task: {task_assignment}
    Dataframe: {df.to_string()} 
    User's question: {question}

    """

    response = llm_smart.invoke([HumanMessage(prompt)])

    return response.content

def write_code_to_plot_chart(task_assignment, df):

    prompt = f"""

    Write Python code to generate a plotly graph as follows: {task_assignment}

    **Requirements:**
    - Use dataframe `df_task` with columns: {', '.join(df.columns)}
    - Do not use sample dataframe
    - Return only raw Python code without formatting or code blocks

    """

    response = llm_fast.invoke([HumanMessage(prompt)])

    return response.content



def list_fields(df_summary, field_category):

    fields = []
    for i in range(len(df_summary)):
        if df_summary[i].field_category == field_category:
            fields.append(df_summary[i].field)    

    return fields    

def how_calculate_ratio_metric(question, df_summary):

    prompt = f"""
    
    Provide a way to calculate the metric mentionned in the user's question. Only use the fields included in the dataset.

    **Input:**
    User's question: {question}
    Dataset summary: {df_summary}
    
    """

    response = llm_fast.invoke([HumanMessage(prompt)])
    return response

def select_analytics_methods(question):

    prompt = f"""

    Select the analytics methods that can answer the user's question.

    **Available Methods:**
    - `describe_volume_metric_evolution`: Describe volume metric trends
    - `explain_volume_metric_evolution`: Explains volume metric trends (requires describe_volume_metric_evolution)
    - `describe_ratio_metric_evolution`: Describe ratio metric trends  
    - `explain_ratio_metric_evolution`: Explains ratio metric trends (requires describe_ratio_metric_evolution)

    **Input:**
    User's question: {question}
    
    """

    structured_llm = llm_fast.with_structured_output(ListAnalyticsMethods, include_raw=True)
    parsed_response = structured_llm.invoke([HumanMessage(prompt)])['parsed'].analytics_methods
    
    methods = []
    for i in range(len(parsed_response)):
        methods.append(parsed_response[i].value)
    
    return methods

def combine_findings(findings, question):

    prompt = f"""

    Extract and summarize key information from the findings that answers the user's question. 
    Be concise and include all relevant numbers.

    **Requirements:**
    - Format: Plain HTML text only (no code blocks or markdown)
    - Title: Use <h2>Key Findings</h2>
    - Convert decimals to percentages (0.8542 → 85.4%)

    **Inputs:**
    User's question: {question}
    Findings: {findings}

    """
    
    response = llm_smart.invoke([HumanMessage(prompt)])

    return response.content

def execute_chart_code(code, df):
    
    namespace = {'df_task': df}
    exec(code, namespace)
    return namespace['result']

def prepare_html_blocks(question, exec_summary, findings, plots):

    blocks_data = []

    blocks_data.append({
        "text": f"""
        <h2>Question</h2>
        <p>{question}</p>""",
        "is_question": True
    })

    blocks_data.append({
        "text": exec_summary,
        "is_full_width": True

    })

    blocks_data.append({
        "text": "Detailed analytics process",
        "is_sep": True
    })

    for i in range(len(plots)):
        blocks_data.append({
            "text": findings[i],
            "png_path": plots[i],  
        })

    return blocks_data

def build_html_content(html_template_path, html_blocks_data):

    # Set up Jinja2 environment
    env = Environment(loader=FileSystemLoader('.'))
    
    template = env.get_template('outputs/template.html')

    html_content = template.render(blocks=html_blocks_data)

    # Save the rendered HTML to a file
    with open('outputs/results.html', 'w') as f:
        f.write(html_content)


def open_html_content(html_file_path):
    webbrowser.open('file://' + os.path.realpath(html_file_path))
