import os
from fastmcp import FastMCP
from .config import settings

mcp = FastMCP(name="MarkdownNotes")

def _get_safe_path(user_path: str) -> str:
    """
    Resolves a user-provided path against the base path and ensures it's safe.

    Raises:
        PermissionError: If the path is outside the base path.
        FileNotFoundError: If the path doesn't exist.
    """
    base_path = os.path.realpath(settings.notes_dir)
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
    The base path can be set using the 'NOTES_DIR' environment variable,
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
    The base path can be set using the 'NOTES_DIR' environment variable,
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
def search_notes(keyword: str, recursive: bool = False, before_context: int = 2, after_context: int = 2) -> dict:
    """
    Searches for a keyword in all markdown files in the notes directory and returns
    matching lines with surrounding context.
    """
    results = []
    try:
        base_path = _get_safe_path("")
        file_list = []
        if recursive:
            for root, _, files in os.walk(base_path):
                for file in files:
                    full_path = os.path.join(root, file)
                    relative_path = os.path.relpath(full_path, base_path)
                    file_list.append(relative_path)
        else:
            file_list = os.listdir(base_path)

        for file_path in file_list:
            if file_path.endswith(".md"):
                try:
                    full_path = _get_safe_path(file_path)
                    if os.path.isdir(full_path):
                        continue
                    with open(full_path, "r", encoding="utf-8") as f:
                        lines = f.readlines()
                        for i, line in enumerate(lines):
                            if keyword.lower() in line.lower():
                                start_line = max(0, i - before_context)
                                end_line = min(len(lines), i + after_context + 1)
                                context_lines = [l.strip() for l in lines[start_line:end_line]]
                                results.append({
                                    "file_path": file_path,
                                    "line_number": i + 1,
                                    "snippet": context_lines
                                })
                except (PermissionError, FileNotFoundError):
                    # Ignore files that can't be read
                    continue
    except (PermissionError, FileNotFoundError) as e:
        return {"status": "error", "error": str(e)}

    return {"status": "success", "data": results}

@mcp.tool
def search_in_note(file_path: str, keyword: str, before_context: int = 2, after_context: int = 2) -> dict:
    """
    Searches for a keyword within a specific markdown file and returns
    matching lines with surrounding context.
    """
    results = []
    try:
        full_path = _get_safe_path(file_path)
        if os.path.isdir(full_path):
            return {"status": "error", "error": f"Error: '{file_path}' is a directory, not a file."}
        
        with open(full_path, "r", encoding="utf-8") as f:
            lines = f.readlines()
            for i, line in enumerate(lines):
                if keyword.lower() in line.lower():
                    start_line = max(0, i - before_context)
                    end_line = min(len(lines), i + after_context + 1)
                    context_lines = [l.strip() for l in lines[start_line:end_line]]
                    results.append({
                        "file_path": file_path,
                        "line_number": i + 1,
                        "snippet": context_lines
                    })
        return {"status": "success", "data": results}
    except (PermissionError, FileNotFoundError) as e:
        return {"status": "error", "error": str(e)}

def main():
    """Runs the MCP server."""
    mcp.run(transport="http", port=8080)

if __name__ == "__main__":
    main()
