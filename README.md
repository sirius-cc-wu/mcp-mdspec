# Markdown Notes MCP Server

This project provides a simple MCP (Model Context Protocol) server for managing markdown notes. It's built using the `fastmcp` library.

## Prerequisites

- Python 3.10 or newer
- `uv` package manager

## Installation

1.  **Install `fastmcp` and project dependencies:**

    This project uses `uv` for dependency management. Running the command below will install `fastmcp` and any other dependencies listed in `pyproject.toml`.

    ```bash
    uv pip install fastmcp
    ```

## Configuration

The server's behavior can be customized via the following environment variable:

- **`MD_NOTES_PATH`**: Specifies the root directory for all note-related operations. If this variable is not set, the server will default to using the current working directory. Both the `list_notes` and `read_note` tools will resolve file and directory paths relative to this base path.

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

This mode starts the MCP Inspector, a web application that allows interactive testing of the tools provided by the MCP server.

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