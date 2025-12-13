import os
from fastmcp import FastMCP

mcp = FastMCP(name="MarkdownNotes")

def get_base_path():
    """Retrieves the base path from an environment variable or defaults to current directory."""
    return os.getenv("MCP_MD_NOTES_BASE_PATH", ".")

@mcp.tool
def list_files(path: str = "") -> list[str]:
    """
    Lists files in a given directory relative to the base path.
    The base path can be set using the 'MCP_MD_NOTES_BASE_PATH' environment variable,
    otherwise it defaults to the current working directory.
    """
    base_path = get_base_path()
    target_path = os.path.join(base_path, path)
    return os.listdir(target_path)

@mcp.tool
def read_file(file_path: str) -> str:
    """
    Reads the content of a file relative to the base path.
    The base path can be set using the 'MCP_MD_NOTES_BASE_PATH' environment variable,
    otherwise it defaults to the current working directory.
    """
    base_path = get_base_path()
    target_file_path = os.path.join(base_path, file_path)
    with open(target_file_path, "r") as f:
        return f.read()

@mcp.tool
def greet(name:str) -> str:
    """Returns a friendly greeting"""
    return f"Hello {name}! Its a pleasure to connect from your first MCP Server."

if __name__ == "__main__":
    mcp.run(transport="http", port=8080)
