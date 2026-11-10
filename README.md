# Building Agents with Google ADK and Vertex AI

This project implements a customer service agent for Betty's Bird Boutique using Google Agent Development Kit (ADK), Vertex AI, Vertex AI Search, MCP Toolbox for Databases, Cloud SQL for MySQL, and Grounding with Google Search.

The agent can retrieve product prices, search store-specific PDF documents, answer general bird-related questions using grounded web search, maintain short-term conversational context, and enforce guardrails around unrelated requests and order processing.

## Getting Started

The project contains a root customer service agent and three specialized capabilities:

1. Product pricing through MCP Toolbox and Cloud SQL for MySQL.
2. Store information retrieval through Vertex AI Search.
3. General bird information through Grounding with Google Search.

### Dependencies

The project uses:

- Google Agent Development Kit (ADK)
- Google Vertex AI
- Google Cloud Discovery Engine / Vertex AI Search
- MCP Toolbox for Databases
- Cloud SQL for MySQL
- `toolbox-core`
- Python
- Google Cloud Application Default Credentials

The course environment can be activated with:

```bash
source /voc/course/public/adk/bin/activate
```

Environment-specific configuration is stored in `.env`.

Example variables include:

```text
GOOGLE_GENAI_USE_VERTEXAI
GOOGLE_CLOUD_PROJECT
GOOGLE_CLOUD_LOCATION

MYSQL_HOST
MYSQL_PORT
MYSQL_DATABASE
MYSQL_USER
MYSQL_PASSWORD

TOOLBOX_URL

DATASTORE_PROJECT_ID
DATASTORE_ENGINE_ID
DATASTORE_LOCATION
```

The `.env` file is excluded from version control because it contains credentials and environment-specific values.

### Installation

Activate the course ADK environment:

```bash
source /voc/course/public/adk/bin/activate
```

Load environment variables:

```bash
set -a
source .env
set +a
```

Start MCP Toolbox:

```bash
./toolbox-1.16.0 --config starter/tools.yaml --port 5000 --enable-api
```

The Toolbox service provides the `get-product-price` MySQL tool used by the root agent.

Run the agent from another terminal:

```bash
source /voc/course/public/adk/bin/activate
cd ~/cd14768-GCP-AgenticAI-C3-Classroom/project
set -a
source .env
set +a
adk run starter
```

For the ADK Web development interface used during assessment:

```bash
/voc/work/.local/bin/adk web \
  --host 0.0.0.0 \
  --port 8000 \
  --url_prefix /proxy/8000 .
```

## Testing

The final integrated agent was tested using a continuous conversation to demonstrate conversational context and correct tool selection.

The required assessment sequence was:

```text
When are you open on Thursday?

Who is Betty?

What kind of bird did she own?

What do they eat?

Can I buy that from you?
```

Additional validation included:

```text
How much is the Bird Bath?

How much is the Golden Eagle Cage?

Can you place the order for me?
```

Assessment screenshots are stored in:

```text
evidence/
```

The screenshots include the conversation, tool requests, tool responses, datastore source content, grounded web-search attribution, database results, missing-product behavior, and order-processing guardrail.

### Break Down Tests



#### Vertex AI Search

The following questions verify retrieval from Betty's indexed store documents:

```text
When are you open on Thursday?
Who is Betty?
What kind of bird did she own?
```

The `search_store_documents` tool retrieves information from the PDFs indexed by Vertex AI Search.

For example, the store-hours document returns:

```text
Thursday: 9am - 5pm
```

#### Grounding with Google Search

General bird-information questions are delegated to `bird_search_agent`, which uses Grounding with Google Search.

Example:

```text
What do they eat?
```

A separate current-information test was also performed:

```text
Search Google for the latest guidance on feeding budgies and cite your sources.
```

The resulting response included visible source attribution.

#### Product Database

Product prices are retrieved through MCP Toolbox and Cloud SQL.

Example:

```text
How much is the Bird Bath?
```

Expected database result:

```text
Bird Bath - $75.99
```

A missing-product case was also tested:

```text
How much is the Golden Eagle Cage?
```

The agent does not invent a database price when no product match is returned.

#### Order Guardrail

The agent does not place, reserve, modify, or cancel customer orders.

Example:

```text
Can you place the order for me?
```

The agent refuses to perform the transaction and directs the customer to Betty's Bird Boutique for assistance.

## Project Instructions

The root agent is implemented in:

```text
starter/agent.py
```

The root agent:

- Uses `InMemorySessionService` for short-term conversational context.
- Loads its instructions from `starter/agent-prompt.txt`.
- Uses a Gemini model for customer service conversations.
- Routes product-price requests to the MCP Toolbox database tool.
- Routes store-specific requests to Vertex AI Search.
- Routes general bird-information requests to the Google Search grounded agent.

The project is organized as follows:

```text
project/
├── README.md
├── evidence/
├── starter/
│   ├── __init__.py
│   ├── agent.py
│   ├── agent-prompt.txt
│   ├── datastore.py
│   ├── search_agent.py
│   ├── search-prompt.txt
│   ├── tools.yaml
│   └── docs/
│       ├── betty_db.sql
│       ├── bettys-history.pdf
│       ├── bettys-hours.pdf
│       └── bettys-staff.pdf
└── .gitignore
```

The completed student deliverables include:

- Root customer service agent in `starter/agent.py`
- Root-agent instructions in `starter/agent-prompt.txt`
- MCP Toolbox configuration in `starter/tools.yaml`
- Vertex AI Search implementation in `starter/datastore.py`
- Google Search grounding agent in `starter/search_agent.py`
- Grounded search instructions in `starter/search-prompt.txt`
- Database initialization script in `starter/docs/betty_db.sql`
- Source PDF documents in `starter/docs/`
- Assessment screenshots in `evidence/`

### Product Database Tool

`starter/tools.yaml` defines the `betty-db` MySQL source and the `get-product-price` tool.

The SQL uses a parameterized `LIKE` query with wildcards:

```sql
SELECT product_name, price
FROM products
WHERE LOWER(product_name) LIKE LOWER(CONCAT('%', ?, '%'))
LIMIT 10;
```

Database credentials are supplied through environment variables rather than being hardcoded.

### Vertex AI Search Tool

`starter/datastore.py` implements document retrieval using `google.cloud.discoveryengine_v1`.

The tool retrieves store-specific information from:

```text
bettys-history.pdf
bettys-hours.pdf
bettys-staff.pdf
```

### Grounding with Google Search

`starter/search_agent.py` defines a separate bird search agent using the built-in `google_search` tool.

The search agent is wrapped in an `AgentTool` and made available to the root customer service agent.

### Model Selection

The original course exercises required experimentation with Gemini 2.5 models. Those models were unavailable to the current Vertex AI lab project during implementation.

`gemini-3.5-flash` was therefore used as the available Flash-family replacement because it provides an appropriate balance of response quality and latency for an interactive customer service agent and grounded search workflow.

## Built With

- Google Agent Development Kit (ADK) - Agent framework and orchestration
- Google Vertex AI - Gemini model hosting
- Vertex AI Search / Discovery Engine - Search over unstructured store documents
- Grounding with Google Search - Grounded general bird-information retrieval
- MCP Toolbox for Databases - Database tool integration
- Google Cloud SQL for MySQL - Product price database
- Google Cloud Storage - Storage for Betty's PDF documents
- Python - Agent and tool implementation
- MySQL - Betty's product database

## License

This project was developed as part of the Building Agents with Google ADK and Vertex AI classroom assessment.