# Markdown Notes MCP Server

This project provides a simple, **read-only** MCP (Model Context Protocol) server for serving local markdown documents to an LLM. It's built using the `fastmcp` library.

The server provides tools to `list_notes`, `read_note`, and `search_notes` from a local directory, but it does not support creating, editing, or deleting files. This makes it a secure way to provide a model with access to a corpus of local documents.

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

- **`NOTES_DIR`**: Specifies the root directory for all note-related operations. If this variable is not set, the server will default to using the "notes" directory. Both the `list_notes` and `read_note` tools will resolve file and directory paths relative to this base path.

For advanced configuration, you can modify the `src/config.py` file, but using environment variables is the recommended approach.

## Running the Server

You can run the server in two modes: `run` for production/consumption and `dev` for development and testing.

### Run Mode

This mode is for running the server to be used by the Gemini CLI. After installation, you can run the server using the `mdnotes` command.

```bash
mdnotes
```

You should see output similar to this:

```
[12/13/25 17:52:18] INFO     Starting MCP server 'MarkdownNotes' with transport 'http'  server.py:2582
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
gemini mcp add --transport http mdnotes http://127.0.0.1:8080/mcp
```

After adding the server, you can use the `/mcp` command in the Gemini CLI to see the available tools.

## Tool Reference

### `list_notes(path: str = "", recursive: bool = False, hierarchical: bool = False) -> dict`

Lists notes in a given directory.

**Parameters:**

*   `path` (optional): The path to a directory relative to `NOTES_DIR`. Defaults to the root of `NOTES_DIR`.
*   `recursive` (optional): If `True`, lists notes in all subdirectories. Defaults to `False`.
*   `hierarchical` (optional): If `True`, returns a tree-like structure of the notes directory. Defaults to `False`.

**Example:**

```
/mcp list_notes
```

**Example (recursive):**

```
/mcp list_notes recursive=True
```

**Example (hierarchical):**

```
/mcp list_notes hierarchical=True
```

### `read_note(file_path: str) -> dict`

Reads the content and metadata of a note.

**Parameters:**

*   `file_path`: The path to a note file relative to `NOTES_DIR`.

**Example:**

```
/mcp read_note file_path="path/to/my/note.md"
```

### `search_notes(keyword: str, recursive: bool = False, before_context: int = 2, after_context: int = 2) -> dict`

Searches for a keyword in all notes.

**Parameters:**

*   `keyword`: The keyword to search for.
*   `recursive` (optional): If `True`, searches in all subdirectories. Defaults to `False`.
*   `before_context` (optional): The number of lines to include before the matching line. Defaults to 2.
*   `after_context` (optional): The number of lines to include after the matching line. Defaults to 2.

**Example:**

```
/mcp search_notes keyword="python"
```

### `search_in_note(file_path: str, keyword: str, before_context: int = 2, after_context: int = 2) -> dict`

Searches for a keyword in a specific note.

**Parameters:**

*   `file_path`: The path to a note file relative to `NOTES_DIR`.
*   `keyword`: The keyword to search for.
*   `before_context` (optional): The number of lines to include before the matching line. Defaults to 2.
*   `after_context` (optional): The number of lines to include after the matching line. Defaults to 2.

**Example:**

```
/mcp search_in_note file_path="path/to/my/note.md" keyword="python"
```

### `get_table_of_contents(file_path: str) -> dict`

Generates a table of contents from the markdown headings in a file.

**Parameters:**

*   `file_path`: The path to a note file relative to `NOTES_DIR`.

**Example:**

```
/mcp get_table_of_contents file_path="path/to/my/note.md"
```

### `index_notes() -> dict`

Indexes all notes for semantic search.

**Example:**

```
/mcp index_notes
```

### `semantic_search(query: str, n_results: int = 5) -> dict`

Performs a semantic search over the indexed notes.

**Parameters:**

*   `query`: The search query.
*   `n_results` (optional): The number of results to return. Defaults to 5.

**Example:**

```
/mcp semantic_search query="how to use python"
```

### `search_by_tag(tag: str) -> dict`

Searches for notes with a specific tag in their frontmatter.

**Parameters:**

*   `tag`: The tag to search for.

**Example:**

```
/mcp search_by_tag tag="python"
```

## Suggested Prompts for Developers

Here are some suggested prompts to help developers effectively use the `mdnotes` MCP server through the Gemini CLI or other coding agents:

### General Information & Discovery

*   "List all notes in the 'project_docs' directory, including their last modified times."
*   "Show me a hierarchical view of all notes in the codebase."
*   "What are the main topics discussed in the 'architecture_overview.md' file?"
*   "Summarize the content of the file 'api_design.md'."

### Targeted Search & Retrieval

*   "Find all notes that mention 'authentication' or 'authorization'."
*   "Search for usage of 'ChromaDB' across all documentation, and show me the surrounding context."
*   "In the 'troubleshooting.md' file, find all mentions of 'error code 500' and show me the lines around it."
*   "What are the notes tagged with 'feature-x'?"
*   "Which notes are semantically similar to 'how to integrate with external services'?"

### Code Understanding & Refactoring

*   "I'm looking for documentation related to our new payment gateway. Can you find relevant notes?"
*   "I need to understand how user roles are managed. What documentation exists for this?"
*   "Find all notes that discuss 'performance optimization' and list their titles."

### Onboarding & New Features

*   "Give me an overview of the 'user management' module by listing relevant documentation."
*   "What are the best practices for writing new API endpoints? Show me relevant notes."
*   "Find documentation on the new 'notification service' feature."

**Tips for Effective Use:**

*   **Consistent Tagging:** Encourage developers to use consistent and meaningful tags in their notes (e.g., in YAML frontmatter) to maximize the effectiveness of `search_by_tag`.
*   **Keep Index Up-to-Date:** For semantic search to provide the most relevant results, ensure that the `index_notes` tool is run regularly after changes to the note corpus.
