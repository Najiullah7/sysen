# 03_agents_with_function_calling.py
# Agents with Function Calling
# Pairs with 03_agents_with_function_calling.R
# Tim Fraser

# This script demonstrates how to build agents that can use function calling.
# Students will learn how to create agent wrapper functions and use multiple tools.

# 0. SETUP ###################################

## 0.1 Load Packages #################################

import requests  # for HTTP requests
import json      # for working with JSON
import pandas as pd  # for data manipulation
import functions as tool_runtime  # access globals used by agent() tool execution

# If you haven't already, install these packages...
# pip install requests pandas

## 0.2 Load Functions #################################

# Load helper functions for agent orchestration
from functions import agent

## 0.3 Configuration #################################

# Select model of interest
MODEL = "smollm2:1.7b"

# 1. DEFINE FUNCTIONS TO BE USED AS TOOLS ###################################

# Define a function to be used as a tool
def add_two_numbers(x, y):
    """Add two numbers together."""
    return x + y

# Define another function to be used as a tool
def get_table(df):
    """
    Convert a pandas DataFrame into a markdown table.
    
    Parameters:
    -----------
    df : pandas.DataFrame
        The DataFrame to convert to a markdown table
    
    Returns:
    --------
    str
        Markdown-formatted table string
    """
    # Tool arguments may arrive as dict/list/scalar from the model.
    # Convert those formats into a DataFrame before rendering markdown.
    if isinstance(df, pd.DataFrame):
        table_df = df
    elif isinstance(df, dict):
        table_df = pd.DataFrame(df)
    elif isinstance(df, list):
        table_df = pd.DataFrame(df)
    else:
        table_df = pd.DataFrame({"value": [df]})
    try:
        return table_df.to_markdown(index=False)
    except ImportError:
        # Fallback when optional dependency `tabulate` is not installed.
        return table_df.to_string(index=False)


# Define a third function to be used as a tool
def calculate_average(numbers):
    """
    Calculate the average value from a list of numbers.

    Parameters:
    -----------
    numbers : list
        A list of numeric values

    Returns:
    --------
    float
        Mean of all numeric values
    """
    if len(numbers) == 0:
        return 0
    return sum(numbers) / len(numbers)

# 2. DEFINE TOOL METADATA ###################################

# Define the tool metadata for add_two_numbers
tool_add_two_numbers = {
    "type": "function",
    "function": {
        "name": "add_two_numbers",
        "description": "Add two numbers",
        "parameters": {
            "type": "object",
            "required": ["x", "y"],
            "properties": {
                "x": {
                    "type": "number",
                    "description": "first number"
                },
                "y": {
                    "type": "number",
                    "description": "second number"
                }
            }
        }
    }
}

# Define the tool metadata for get_table
tool_get_table = {
    "type": "function",
    "function": {
        "name": "get_table",
        "description": "Convert a data.frame into a markdown table",
        "parameters": {
            "type": "object",
            "required": ["df"],
            "properties": {
                "df": {
                    "type": "object",
                    "description": "The data.frame to convert to a markdown table using pandas to_markdown()"
                }
            }
        }
    }
}

# Define the tool metadata for calculate_average
tool_calculate_average = {
    "type": "function",
    "function": {
        "name": "calculate_average",
        "description": "Calculate the average from a list of numbers",
        "parameters": {
            "type": "object",
            "required": ["numbers"],
            "properties": {
                "numbers": {
                    "type": "array",
                    "description": "A list of numeric values to average",
                    "items": {"type": "number"}
                }
            }
        }
    }
}

# Register tool functions into functions.py module globals.
# The agent() wrapper executes tool calls by looking up function names in that module.
tool_runtime.add_two_numbers = add_two_numbers
tool_runtime.get_table = get_table
tool_runtime.calculate_average = calculate_average

# 3. EXAMPLE 1: STANDARD CHAT (NO TOOLS) ###################################

# Trying to call a standard chat without tools
# The agent() function from functions.py handles this automatically
messages = [
    {"role": "user", "content": "Write a haiku about cheese."}
]

resp = agent(messages=messages, model=MODEL, output="text")
print("📝 Standard Chat Response:")
print(resp)
print()

# 4. EXAMPLE 2: TOOL CALL #1 ###################################

# Try calling tool #1 (add_two_numbers)
messages = [
    {"role": "user", "content": "Add 3 + 5."}
]

resp = agent(messages=messages, model=MODEL, output="tools", tools=[tool_add_two_numbers])
print("🔧 Tool Call #1 Result:")
print(resp)
print()

# Access the output from the tool call
if isinstance(resp, list) and len(resp) > 0:
    print(f"Tool output: {resp[0].get('output', 'No output')}")
    print()

# 5. EXAMPLE 3: TOOL CALL #2 ###################################

# Try calling tool #2 (get_table)
# First, create a simple DataFrame with the result from tool #1
if isinstance(resp, list) and len(resp) > 0:
    result_value = resp[0].get("output", 0)
else:
    try:
        result_value = float(resp)
    except (TypeError, ValueError):
        result_value = 0
df = pd.DataFrame({"x": [result_value]})

messages = [
    {"role": "user", "content": f"Place the numeric value {result_value} into a 1x1 data.frame with column name 'x' and format as a markdown table."}
]

resp2 = agent(messages=messages, model=MODEL, output="tools", tools=[tool_get_table])
print("🔧 Tool Call #2 Result:")
print(resp2)
print()

# Compare against manual approach
print("📊 Manual Table Creation:")
try:
    manual_table = df.to_markdown(index=False)
except ImportError:
    manual_table = df.to_string(index=False)
print(manual_table)
print()

# 6. EXAMPLE 4: TOOL CALL #3 ###################################

# Try calling tool #3 (calculate_average)
messages = [
    {"role": "user", "content": "Calculate the average of 10, 20, 30, and 40."}
]

resp3 = agent(messages=messages, model=MODEL, output="tools", tools=[tool_calculate_average])
print("🔧 Tool Call #3 Result:")
print(resp3)
print()

if isinstance(resp3, list) and len(resp3) > 0:
    print(f"Tool output: {resp3[0].get('output', 'No output')}")
    print()

# Note: We can use the agent() function to rapidly build and test out agents with or without tools.
