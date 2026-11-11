import os

from google.adk.agents import Agent
from google.adk.sessions import InMemorySessionService
from toolbox_core import ToolboxSyncClient
from .datastore import search_store_documents
from .search_agent import search_agent_tool

# Configure short-term session to use the in-memory service
session_service = InMemorySessionService()

# Read the instructions from a file in the same
# directory as this agent.py file.
script_dir = os.path.dirname(os.path.abspath(__file__))
instruction_file_path = os.path.join(script_dir, "agent-prompt.txt")
with open(instruction_file_path, "r") as f:
    instruction = f.read()

# Set up the tools that we will be using for the root agent
toolbox_url = os.environ.get("TOOLBOX_URL","http://127.0.0.1:5000",)
toolbox_client = ToolboxSyncClient(toolbox_url)

tools = [
    toolbox_client.load_tool("get-product-price"),
    search_store_documents,
    search_agent_tool,
]

# gemini-3.8-flash is used because the Gemini 2.5 models required by the
# original course are no longer available to this Vertex AI project.
# This Flash model provides a suitable balance of response quality and
# latency for an interactive customer-service agent.
root_agent = Agent(
    name="bettys_bird_boutique_agent",
    model="gemini-3.8-flash",
    description="Customer support agent for Betty's Bird Boutique.",
    instruction=instruction,
    tools=tools,
)