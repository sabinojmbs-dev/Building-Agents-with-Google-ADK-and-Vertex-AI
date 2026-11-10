import os

from google.adk.agents import Agent
from google.adk.tools import google_search
from google.adk.tools.agent_tool import AgentTool

# Definition of an agent tool that accesses Grounding with Google Search

# Read the instructions from a file in the same
# directory as this file.
script_dir = os.path.dirname(os.path.abspath(__file__))
instruction_file_path = os.path.join(script_dir, "search-prompt.txt")
with open(instruction_file_path, "r") as f:
  instruction = f.read()

# The course rubric recommends a Gemini 2.0/2.5 model for grounded search.
# The required Gemini 2.5 models returned 404 from the current Vertex AI
# environment, so gemini-3.5-flash is used as the available Flash-family
# replacement for responsive web-grounded bird-information queries.
search_agent = Agent(
  name="bird_search_agent",
  model="gemini-3.5-flash",
  description="Answers general bird questions using Google Search.",
  instruction=instruction,
  tools=[google_search],
)

search_agent_tool = AgentTool(agent=search_agent)
