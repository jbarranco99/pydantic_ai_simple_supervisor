import json
import os
import asyncio
from dotenv import load_dotenv
from pydantic_ai import Agent, RunContext
from pydantic import BaseModel, Field
from pydantic_ai.models.openai import OpenAIModel
from dataclasses import dataclass

# Load environment variables
load_dotenv()
OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')

# Initialize empty message history
message_history = []


# Define pydantic models for structured output
class StructuredOutput(BaseModel):
    """Defines structured output format for the secretary agent."""
    response: str = Field(description='The response from the LLM')
    tools_used: list[str] = Field(description='The tool(s) used in the response')

class MathOutput(BaseModel):
    """Defines the structured output format for mathematical operations."""
    result: float = Field(description='The result of the math operation')

class ResearchOutput(BaseModel):
    """Defines structured output format for research results."""
    result: str = Field(description='The result of the research')

# Define OpenAI model
model = OpenAIModel(model_name='gpt-4o-mini', api_key=OPENAI_API_KEY)

# Math Agent - responsible for handling mathematical calculations
math_agent = Agent(
    model,
    result_type=MathOutput,
    system_prompt="""
    You are a Math Assistant responsible for executing mathematical expressions step by step.
    Always prioritize multiplication before addition (PEMDAS rule) and break down expressions into separate tool calls.
    """
)

@math_agent.tool
async def multiplication(ctx: RunContext, num1: float, num2: float) -> MathOutput:
    """Multiplies two numbers."""
    print(f"Multiplication tool called with num1={num1}, num2={num2}")
    return MathOutput(result=num1 * num2)

@math_agent.tool
async def addition(ctx: RunContext, num1: float, num2: float) -> MathOutput:
    """Adds two numbers."""
    print(f"Addition tool called with num1={num1}, num2={num2}")
    return MathOutput(result=num1 + num2)

# Research Agent - handles web searches
research_agent = Agent(
    model,
    result_type=ResearchOutput,
    system_prompt="""
    You are a research agent that has access to a web search tool. Use this tool to retrieve relevant information from the internet. Do not execute math operations.
    """
)

@research_agent.tool
async def web_search(ctx: RunContext, search_term: str) -> ResearchOutput:
    """Performs a web search for the given term."""
    print(f"Research tool called with search_term: {search_term}")
    return ResearchOutput(result=
    "Here are the headcounts for each of the FAANG companies:\n"
        "1. **Facebook (Meta)**: 67,317 employees.\n"
        "2. **Apple**: 164,000 employees.\n"
        "3. **Amazon**: 1,551,000 employees.\n"
        "4. **Netflix**: 14,000 employees.\n"
        "5. **Google (Alphabet)**: 181,269 employees."
    )

# Secretary Agent - manages overall conversation flow
secretary_agent = Agent[StructuredOutput](
    model,
    result_type=StructuredOutput,
    system_prompt="""
        # **Secretary Agent System Prompt**

        You are **Secretary Agent**, a highly capable AI assistant designed to efficiently manage tasks and support the user. You have access to two tools:

        1. **Research Tool**: Use this when the user requests information, data, or anything requiring a search.
        2. **Math Tool**: Use this when the user asks for calculations, numerical analysis, or data processing. Do not run calculations by yourself.

        ## **General Guidelines**
        - **Understand Intent:** Determine if the user is asking for data, calculations, or a visual output and select the appropriate tool(s).
        - **Be Efficient:** Use tools only when necessary. If you can answer without using a tool, do so. Call tools efficiently, try to minimize tool usage, and review the results before calling another tool or responding to the user.
        - **Be Structured:** Present information clearly, concisely, and in a user-friendly manner.
        - **Stay Helpful and Professional:** Provide complete, well-formatted responses while keeping interactions natural and engaging.

        ## **Decision Flow**
        1. **If the user asks for information or external data** → Use the **Research Tool**.
        2. **If the user asks for calculations** → Use the **Math Tool**.
        3. **If a request requires multiple steps** → Combine tools strategically to complete the task.

        Always aim for precision, clarity, and effectiveness in every response. Your goal is to provide the best possible support to the user.

    """,
    instrument=True
)

@secretary_agent.tool
async def perform_calculations(ctx: RunContext, math_request: str) -> MathOutput:
    """Delegates mathematical calculations to the Math Agent."""
    print(f"Math agent called with request: {math_request}")
    result = await math_agent.run(f"Execute {math_request}")
    return result.data

@secretary_agent.tool
async def execute_research(ctx: RunContext, search_term: str) -> ResearchOutput:
    """Delegates research tasks to the Research Agent."""
    print(f"Research agent called with search_term: {search_term}")
    result = await research_agent.run(f"Perform research with search term: {search_term}")
    return result.data

async def main():
    """Main function to execute the Secretary Agent."""
    run_prompt = 'whats the combined number of faang employees'
    result = await secretary_agent.run(run_prompt, message_history=message_history)
    message_history.extend(result.new_messages())
    
    # Format JSON output
    formatted_json = json.dumps(json.loads(result.all_messages_json()), indent=4)
    print(formatted_json)

if __name__ == '__main__':
    asyncio.run(main())
