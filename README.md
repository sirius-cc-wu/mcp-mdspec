# Markdown Specs MCP Server

This project provides a simple, **read-only** MCP (Model Context Protocol) server for serving local markdown documents to an LLM. It's built using the `fastmcp` library.

The server provides tools to `list_specs`, `read_spec`, and `search_specs` from a local directory, but it does not support creating, editing, or deleting files. This makes it a secure way to provide a model with access to a corpus of local documents.

## Prerequisites

- Python 3.13 or newer
- `uv` package manager

## Installation

1.  **Install project dependencies:**

    This project uses `uv` for dependency management. Running the command below will install all dependencies listed in `pyproject.toml` and create a command-line script to run the server.

    ```bash
    uv pip install .
    ```

## Configuration

The server's behavior can be customized by setting environment variables.

- **`SPECS_DIR`**: Specifies the root directory for all spec-related operations. If this variable is not set, the server will default to using the "specs" directory. Both the `list_specs` and `read_spec` tools will resolve file and directory paths relative to this base path.

For advanced configuration, you can modify the `src/config.py` file, but using environment variables is the recommended approach.

## Running the Server

You can run the server in two modes: `run` for production/consumption and `dev` for development and testing.

### Run Mode

This mode is for running the server to be used by the Gemini CLI. After installation, you can run the server using the `mdspec` command.

```bash
mdspec
```

You should see output similar to this:

```
[12/13/25 17:52:18] INFO     Starting MCP server 'MarkdownSpecs' with transport 'http'  server.py:2582
                             on http://127.0.0.1:8080/mcp
INFO:     Started server process [24263]
INFO:     Waiting for application startup.
INFO:     Application startup complete.
INFO:     Uvicorn running on http://127.0.0.1:8080 (Press CTRL+C to quit)
```

### Dev Mode

This mode starts the MCP Inspector, a web-based UI that allows for interactive testing of the tools provided by the MCP server.

```bash
fastmcp dev src/main.py --ui-port="9080" --server-port="5080"
```

You will see output like this, including a URL to access the MCP Inspector:

```
Starting MCP inspector...
⚙ Proxy server listening on localhost:5080
🔑 Session token: <your_session_token>
   Use this token to authenticate requests or set DANGEROUSLY_OMIT_AUTH=true to disable auth

🚀 MCP Inspector is up and running at:
   http://localhost:9080/?MCP_PROXY_PORT=5080&MCP_PROXY_AUTH_TOKEN=<your_session_token>

🌐 Opening browser...
```

## Connecting to Gemini CLI

To use this MCP server with the Gemini CLI, you need to add it as a source.

```bash
gemini mcp add --transport http mdspec http://127.0.0.1:8080/mcp
```

After adding the server, you can use the `/mcp` command in the Gemini CLI to see the available tools.

## Tool Reference

### `list_specs(path: str = "", recursive: bool = False, hierarchical: bool = False) -> dict`

Lists specs in a given directory.

**Parameters:**

*   `path` (optional): The path to a directory relative to `SPECS_DIR`. Defaults to the root of `SPECS_DIR`.
*   `recursive` (optional): If `True`, lists specs in all subdirectories. Defaults to `False`.
*   `hierarchical` (optional): If `True`, returns a tree-like structure of the specs directory. Defaults to `False`.

### `read_spec(file_path: str) -> dict`

Reads the content and metadata of a spec.

**Parameters:**

*   `file_path`: The path to a spec file relative to `SPECS_DIR`.

### `search_specs(keyword: str, recursive: bool = False, before_context: int = 2, after_context: int = 2) -> dict`

Searches for a keyword in all specs.

**Parameters:**

*   `keyword`: The keyword to search for.
*   `recursive` (optional): If `True`, searches in all subdirectories. Defaults to `False`.
*   `before_context` (optional): The number of lines to include before the matching line. Defaults to 2.
*   `after_context` (optional): The number of lines to include after the matching line. Defaults to 2.

### `search_in_spec(file_path: str, keyword: str, before_context: int = 2, after_context: int = 2) -> dict`

Searches for a keyword in a specific spec.

**Parameters:**

*   `file_path`: The path to a spec file relative to `SPECS_DIR`.
*   `keyword`: The keyword to search for.
*   `before_context` (optional): The number of lines to include before the matching line. Defaults to 2.
*   `after_context` (optional): The number of lines to include after the matching line. Defaults to 2.

### `get_table_of_contents(file_path: str) -> dict`

Generates a table of contents from the markdown headings in a file.

**Parameters:**

*   `file_path`: The path to a spec file relative to `SPECS_DIR`.


### `index_specs() -> dict`

Indexes all specs for semantic search.


### `semantic_search(query: str, n_results: int = 5) -> dict`

Performs a semantic search over the indexed specs.

**Parameters:**

*   `query`: The search query.
*   `n_results` (optional): The number of results to return. Defaults to 5.


### `search_by_tag(tag: str) -> dict`

Searches for specs with a specific tag in their frontmatter.

**Parameters:**

*   `tag`: The tag to search for.

## Suggested Prompts for Developers

Here are some suggested prompts to help developers effectively use the `mdspec` MCP server through the Gemini CLI or other coding agents:

### General Information & Discovery

*   "List all specs in the 'project_docs' directory, including their last modified times."
*   "Show me a hierarchical view of all specs in the codebase."
*   "What are the main topics discussed in the 'architecture_overview.md' file?"
*   "Summarize the content of the file 'api_design.md'."

### Targeted Search & Retrieval

*   "Find all specs that mention 'authentication' or 'authorization'."
*   "Search for usage of 'ChromaDB' across all documentation, and show me the surrounding context."
*   "In the 'troubleshooting.md' file, find all mentions of 'error code 500' and show me the lines around it."
*   "What are the specs tagged with 'feature-x'?"
*   "Which specs are semantically similar to 'how to integrate with external services'?"

### Code Understanding & Refactoring

*   "I'm looking for documentation related to our new payment gateway. Can you find relevant specs?"
*   "I need to understand how user roles are managed. What documentation exists for this?"
*   "Find all specs that discuss 'performance optimization' and list their titles."

### Onboarding & New Features

*   "Give me an overview of the 'user management' module by listing relevant documentation."
*   "What are the best practices for writing new API endpoints? Show me relevant specs."
*   "Find documentation on the new 'notification service' feature."

**Tips for Effective Use:**

*   **Consistent Tagging:** Encourage developers to use consistent and meaningful tags in their specs (e.g., in YAML frontmatter) to maximize the effectiveness of `search_by_tag`.
*   **Keep Index Up-to-Date:** For semantic search to provide the most relevant results, ensure that the `index_specs` tool is run regularly after changes to the spec corpus.
