from crewai import Agent
from TravelTools import search_web_tool, web_search_tool
from langchain_openai import ChatOpenAI
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Get API key from environment variables
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

# Check if API key is available
if not OPENAI_API_KEY:
    raise ValueError(
        "OpenAI API key not found. Please set the OPENAI_API_KEY environment variable "
        "in a .env file or directly in your environment."
    )

# Initialize ChatGPT LLM
# Using gpt-3.5-turbo for better reliability in agent workflows
chatgpt_llm = ChatOpenAI(
    temperature=0.5,  # Lower temperature for more deterministic outputs
    model="gpt-3.5-turbo",  # Using gpt-3.5-turbo to reduce token usage and improve reliability
    api_key=OPENAI_API_KEY
)

# Agents
guide_expert = Agent(
    role="City Local Guide Expert",
    goal="Provides information on things to do in the city based on user interests.",
    backstory="A local expert passionate about sharing city experiences.",
    tools=[search_web_tool],
    verbose=True,
    max_iter=3,  # Reduced max iterations to avoid loops
    llm=chatgpt_llm,
    allow_delegation=False,
)

location_expert = Agent(
    role="Travel Trip Expert",
    goal="Provides travel logistics and essential information.",
    backstory="A seasoned traveler who knows everything about different cities.",
    tools=[search_web_tool],  # Simplified to just one tool
    verbose=True,
    max_iter=3,  # Reduced max iterations
    llm=chatgpt_llm,
    allow_delegation=False,
)

planner_expert = Agent(
    role="Travel Planning Expert",
    goal="Compiles all gathered information to create a travel plan.",
    backstory="An expert in planning seamless travel itineraries.",
    tools=[search_web_tool],
    verbose=True,
    max_iter=3,  # Reduced max iterations
    llm=chatgpt_llm,
    allow_delegation=False,
)