import os

from google.api_core.client_options import ClientOptions
from google.cloud import discoveryengine_v1 as discoveryengine

# Definition of a tool that accesses a Vertex AI Search Datastore

#
# This is based on code provided by Google at
# https://cloud.google.com/generative-ai-app-builder/docs/samples/genappbuilder-search
# Search parameters request snippets plus extractive answers and segments
# because Betty's documents are short unstructured PDFs and these fields
# provide concise passages for the root agent to use in its response.
#
# The object definitions aren't available to all IDEs because of Google's ProtoBuf
# implementation, so the IDE may generate a warning, but work fine. I've used
# dicts here instead, but indicated the Class that could be used instead.
# You can see the definitions at
# https://cloud.google.com/python/docs/reference/discoveryengine/latest/google.cloud.discoveryengine_v1.types
#
def search(
    project_id: str,
    location: str,
    engine_id: str,
    search_query: str,
) -> list[str]:
  #  For more information, refer to:
  # https://cloud.google.com/generative-ai-app-builder/docs/locations#specify_a_multi-region_for_your_data_store
  client_options = (
    ClientOptions(api_endpoint=f"{location}-discoveryengine.googleapis.com")
    if location != "global"
    else None
  )

  # Create a client
  client = discoveryengine.SearchServiceClient(client_options=client_options)

  # The full resource name of the search app serving config
  serving_config = f"projects/{project_id}/locations/{location}/collections/default_collection/engines/{engine_id}/servingConfigs/default_config"

  # discoveryengine.SearchRequest
  request = {
    "serving_config": serving_config,
    "query": search_query,
    "page_size": 5,
    "content_search_spec": {
        "snippet_spec": {
            "return_snippet": True,
        },
        "extractive_content_spec": {
            "max_extractive_answer_count": 3,
            "max_extractive_segment_count": 3,
        },
    },
}

  page_result = client.search(request)

  results = []

  for result in page_result:
    document = result.document
    derived_data = document.derived_struct_data

    title = derived_data.get("title", "Betty's store document")

    content_parts = []

    for answer in derived_data.get("extractive_answers", []):
      content = answer.get("content")
      if content:
        content_parts.append(content)

    for segment in derived_data.get("extractive_segments", []):
      content = segment.get("content")
      if content:
        content_parts.append(content)

    for snippet in derived_data.get("snippets", []):
      content = snippet.get("snippet") or snippet.get("content")
      if content:
        content_parts.append(content)

    if content_parts:
      results.append(
        f"Source: {title}\n"
        + "\n".join(content_parts)
      )

  return results


def search_store_documents(search_query: str) -> dict:
  """Search Betty's Bird Boutique documents.

  Use this tool for questions about Betty's store hours, location,
  history, staff, staff-owned birds, and other store-specific information.

  Args:
    search_query: A question about Betty's Bird Boutique.

  Returns:
    Relevant information retrieved from Betty's store documents.
  """

  import os

  project_id = os.getenv("DATASTORE_PROJECT_ID")
  engine_id = os.getenv("DATASTORE_ENGINE_ID")
  location = os.getenv("DATASTORE_LOCATION", "global")

  if not project_id or not engine_id:
    return {
      "status": "error",
      "message": "The document search configuration is incomplete.",
    }

  results = search(
    project_id=project_id,
    location=location,
    engine_id=engine_id,
    search_query=search_query,
  )

  if not results:
    return {
      "status": "not_found",
      "message": "No relevant information was found in Betty's store documents.",
    }

  return {
    "status": "success",
    "results": results,
  }