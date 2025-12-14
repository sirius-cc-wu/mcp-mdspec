import os
from fastmcp import FastMCP

mcp = FastMCP(name="MarkdownNotes")

def get_base_path():
    """Retrieves the base path from an environment variable or defaults to current directory."""
    return os.getenv("MD_NOTES_PATH", ".")

def _get_safe_path(user_path: str) -> str:
    """
    Resolves a user-provided path against the base path and ensures it's safe.

    Raises:
        PermissionError: If the path is outside the base path.
        FileNotFoundError: If the path doesn't exist.
    """
    base_path = os.path.realpath(get_base_path())
    # Prevent user_path from being an absolute path
    if os.path.isabs(user_path):
        raise PermissionError("Error: Absolute paths are not allowed.")

    target_path = os.path.realpath(os.path.join(base_path, user_path))

    if not target_path.startswith(base_path):
        raise PermissionError("Error: Access to paths outside of the notes directory is not allowed.")

    if not os.path.exists(target_path):
        raise FileNotFoundError(f"Error: Path \'{user_path}\' not found.")

    return target_path


@mcp.tool
def list_notes(path: str = "", recursive: bool = False) -> dict:
    """
    Lists notes in a given directory relative to the base path.
    The base path can be set using the 'MD_NOTES_PATH' environment variable,
    otherwise it defaults to the current working directory.
    """
    try:
        safe_path = _get_safe_path(path)
        if recursive:
            file_list = []
            for root, _, files in os.walk(safe_path):
                for file in files:
                    full_path = os.path.join(root, file)
                    relative_path = os.path.relpath(full_path, safe_path)
                    file_list.append(relative_path)
            return {"status": "success", "data": file_list}
        else:
            return {"status": "success", "data": os.listdir(safe_path)}
    except (PermissionError, FileNotFoundError) as e:
        return {"status": "error", "error": str(e)}


@mcp.tool
def read_note(file_path: str) -> dict:
    """
    Reads the content of a note file relative to the base path.
    The base path can be set using the 'MD_NOTES_PATH' environment variable,
    otherwise it defaults to the current working directory.
    """
    try:
        safe_path = _get_safe_path(file_path)
        if os.path.isdir(safe_path):
            return {"status": "error", "error": f"Error: \'{file_path}\' is a directory, not a file."}
        with open(safe_path, "r") as f:
            return {"status": "success", "data": f.read()}
    except (PermissionError, FileNotFoundError) as e:
        return {"status": "error", "error": str(e)}

@mcp.tool
def search_notes(keyword: str, recursive: bool = False) -> dict:
    """
    Searches for a keyword in all markdown files in the notes directory.
    """
    list_response = list_notes(recursive=recursive)
    if list_response["status"] == "error":
        return list_response

    results = []
    for file_path in list_response["data"]:
        if file_path.endswith(".md"):
            read_response = read_note(file_path)
            if read_response["status"] == "success":
                for i, line in enumerate(read_response["data"].splitlines()):
                    if keyword.lower() in line.lower():
                        results.append({
                            "file_path": file_path,
                            "line_number": i + 1,
                            "snippet": line.strip()
                        })
    return {"status": "success", "data": results}

if __name__ == "__main__":
    mcp.run(transport="http", port=8080)
