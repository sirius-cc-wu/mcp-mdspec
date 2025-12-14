import os
from fastmcp import FastMCP

mcp = FastMCP(name="MarkdownNotes")

def get_base_path():
    """Retrieves the base path from an environment variable or defaults to current directory."""
    return os.getenv("MD_NOTES_PATH", ".")

@mcp.tool
def list_notes(path: str = "") -> list[str]:
    """
    Lists notes in a given directory relative to the base path.
    The base path can be set using the 'MD_NOTES_PATH' environment variable,
    otherwise it defaults to the current working directory.
    """
    base_path = get_base_path()
    target_path = os.path.join(base_path, path)
    return os.listdir(target_path)

@mcp.tool
def read_note(file_path: str) -> str:
    """
    Reads the content of a note file relative to the base path.
    The base path can be set using the 'MD_NOTES_PATH' environment variable,
    otherwise it defaults to the current working directory.
    """
    base_path = get_base_path()
    target_file_path = os.path.join(base_path, file_path)
    with open(target_file_path, "r") as f:
        return f.read()

@mcp.tool
def search_notes(keyword: str) -> list[str]:
    """
    Searches for a keyword in all markdown files in the notes directory.
    """
    results = []
    for file_path in list_notes():
        if file_path.endswith(".md"):
            content = read_note(file_path)
            if keyword.lower() in content.lower():
                results.append(file_path)
    return results

if __name__ == "__main__":
    mcp.run(transport="http", port=8080)
