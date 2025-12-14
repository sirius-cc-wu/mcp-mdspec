# Markdown Notes MCP Server

This project provides a simple, **read-only** MCP (Model Context Protocol) server for serving local markdown documents to an LLM. It's built using the `fastmcp` library.

The server provides tools to `list_notes`, `read_note`, and `search_notes` from a local directory, but it does not support creating, editing, or deleting files. This makes it a secure way to provide a model with access to a corpus of local documents.

## Prerequisites

- Python 3.13 or newer
- `uv` package manager

## Installation

1.  **Install project dependencies:**

    This project uses `uv` for dependency management. Running the command below will install all dependencies listed in `pyproject.toml`.

    ```bash
    uv pip install .
    ```

## Configuration

The server's behavior can be customized via the `config.py` file or by setting environment variables.

- **`NOTES_DIR`**: Specifies the root directory for all note-related operations. If this variable is not set, the server will default to using the "notes" directory. Both the `list_notes` and `read_note` tools will resolve file and directory paths relative to this base path.

You can also modify the `config.py` file to change the default `notes_dir`.

## Running the Server

You can run the server in two modes: `run` for production/consumption and `dev` for development and testing.

### Run Mode

This mode is for running the server to be used by the Gemini CLI. The `main.py` script can now be run directly as it contains the server startup logic.

```bash
python main.py
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
fastmcp dev main.py --ui-port="9080" --server-port="5080"
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
