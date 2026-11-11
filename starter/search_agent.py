import os

from google.adk.agents import Agent
from google.adk.tools import google_search
from google.adk.tools.agent_tool import AgentTool


# Definition of an agent tool that accesses Grounding with Google Search

# Read the instructions from a file in the same directory as this file.
script_dir = os.path.dirname(os.path.abspath(__file__))

instruction_file_path = os.path.join(
    script_dir,
    "search-prompt.txt",
)

with open(instruction_file_path, "r") as f:
    instruction = f.read()


# MODEL SELECTION
#
# The project rubric recommends a Gemini 2.0 or 2.5 Flash-family model.
# These models were unavailable in the current Vertex AI lab environment.
#
# gemini-3.8-flash was selected because it was available during testing
# and provides a suitable balance of response quality and latency for
# Google Search-grounded bird-information retrieval.
#
# The search agent uses its own Gemini model configuration, separate
# from the root customer service agent.

search_agent = Agent(
    name="bird_search_agent",
    model="gemini-3.8-flash",
    description=(
        "Specialized bird research agent that retrieves current "
        "and reliable bird-related information using "
        "Grounding with Google Search."
    ),
    instruction=instruction,
    tools=[google_search],
)


# Wrap the specialized search agent as an AgentTool so the root
# customer service agent can delegate external research questions.

search_agent_tool = AgentTool(agent=search_agent)