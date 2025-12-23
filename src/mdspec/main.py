import frontmatter
import os
from datetime import datetime
from fastmcp import FastMCP
from .config import settings
from .vector_search import VectorSearch

mcp = FastMCP(name="MarkdownSpecs")
vector_search = VectorSearch()


def _get_safe_path(user_path: str) -> str:
    """
    Resolves a user-provided path against the base path and ensures it's safe.

    Raises:
        PermissionError: If the path is outside the base path.
        FileNotFoundError: If the path doesn't exist.
    """
    base_path = os.path.realpath(settings.specs_dir)
    # Prevent user_path from being an absolute path
    if os.path.isabs(user_path):
        raise PermissionError("Error: Absolute paths are not allowed.")

    target_path = os.path.realpath(os.path.join(base_path, user_path))

    if not target_path.startswith(base_path):
        raise PermissionError(
            "Error: Access to paths outside of the specs directory is not allowed.")

    if not os.path.exists(target_path):
        raise FileNotFoundError(f"Error: Path '{user_path}' not found.")

    return target_path


@mcp.tool
def list_specs(path: str = "", recursive: bool = False, hierarchical: bool = False) -> dict:
    """
    Lists specs in a given directory relative to the base path, including their last modified timestamp.
    The base path can be set using the 'SPECS_DIR' environment variable,
    otherwise it defaults to the current working directory.
    """
    try:
        safe_path = _get_safe_path(path)

        def get_file_data(full_path, base_for_relpath):
            last_modified_timestamp = os.path.getmtime(full_path)
            last_modified = datetime.fromtimestamp(
                last_modified_timestamp).isoformat()
            relative_path = os.path.relpath(full_path, base_for_relpath)
            return {"name": relative_path, "last_modified": last_modified}

        def get_tree(dir_path, base_for_relpath):
            tree = []
            for item in os.listdir(dir_path):
                full_path = os.path.join(dir_path, item)
                if os.path.isdir(full_path):
                    tree.append({
                        "name": os.path.relpath(full_path, base_for_relpath),
                        "type": "directory",
                        "children": get_tree(full_path, base_for_relpath)
                    })
                else:
                    tree.append({
                        "name": os.path.relpath(full_path, base_for_relpath),
                        "type": "file",
                        "last_modified": datetime.fromtimestamp(os.path.getmtime(full_path)).isoformat()
                    })
            return tree

        if hierarchical:
            return {"status": "success", "data": get_tree(safe_path, safe_path)}

        if recursive:
            file_list = []
            for root, _, files in os.walk(safe_path):
                for file in files:
                    full_path = os.path.join(root, file)
                    file_list.append(get_file_data(full_path, safe_path))
            return {"status": "success", "data": file_list}
        else:
            detailed_file_list = []
            for item in os.listdir(safe_path):
                full_path = os.path.join(safe_path, item)
                detailed_file_list.append(
                    get_file_data(full_path, safe_path))
            return {"status": "success", "data": detailed_file_list}

    except (PermissionError, FileNotFoundError) as e:
        return {"status": "error", "error": str(e)}


@mcp.tool
def read_spec(file_path: str) -> dict:
    """
    Reads the content and metadata of a spec file relative to the base path.
    The base path can be set using the 'SPECS_DIR' environment variable,
    otherwise it defaults to the current working directory.
    """
    try:
        safe_path = _get_safe_path(file_path)
        if os.path.isdir(safe_path):
            return {"status": "error", "error": f"Error: '{file_path}' is a directory, not a file."}
        with open(safe_path, "r") as f:
            spec = frontmatter.load(f)
            return {"status": "success", "data": {"content": spec.content, "metadata": spec.metadata}}
    except (PermissionError, FileNotFoundError) as e:
        return {"status": "error", "error": str(e)}


@mcp.tool
def search_specs(keyword: str, recursive: bool = False, before_context: int = 2, after_context: int = 2) -> dict:
    """
    Searches for a keyword in all markdown files in the specs directory and returns
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
                                end_line = min(
                                    len(lines), i + after_context + 1)
                                context_lines = [l.strip()
                                                 for l in lines[start_line:end_line]]
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
def search_in_spec(file_path: str, keyword: str, before_context: int = 2, after_context: int = 2) -> dict:
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
                    context_lines = [l.strip()
                                     for l in lines[start_line:end_line]]
                    results.append({
                        "file_path": file_path,
                        "line_number": i + 1,
                        "snippet": context_lines
                    })
        return {"status": "success", "data": results}
    except (PermissionError, FileNotFoundError) as e:
        return {"status": "error", "error": str(e)}


@mcp.tool
def get_table_of_contents(file_path: str) -> dict:
    """
    Generates a table of contents from the markdown headings in a file.
    """
    toc = []
    try:
        full_path = _get_safe_path(file_path)
        if os.path.isdir(full_path):
            return {"status": "error", "error": f"Error: '{file_path}' is a directory, not a file."}

        with open(full_path, "r", encoding="utf-8") as f:
            for line in f:
                if line.strip().startswith("#"):
                    parts = line.strip().split(" ", 1)
                    level = len(parts[0])
                    title = parts[1].strip() if len(parts) > 1 else ""
                    toc.append({"level": level, "title": title})
        return {"status": "success", "data": toc}
    except (PermissionError, FileNotFoundError) as e:
        return {"status": "error", "error": str(e)}


@mcp.tool
def index_specs() -> dict:
    """
    Indexes all specs for semantic search.
    This process can take a while depending on the number of specs.
    """
    try:
        base_path = _get_safe_path("")
        specs_to_index = []
        for root, _, files in os.walk(base_path):
            for file in files:
                if file.endswith(".md"):
                    full_path = os.path.join(root, file)
                    relative_path = os.path.relpath(full_path, base_path)
                    with open(full_path, "r", encoding="utf-8") as f:
                        content = f.read()
                    specs_to_index.append(
                        {"path": relative_path, "content": content})
        vector_search.index_specs(specs_to_index)
        return {"status": "success", "message": "Specs indexed successfully."}
    except Exception as e:
        return {"status": "error", "error": str(e)}


@mcp.tool
def semantic_search(query: str, n_results: int = 5) -> dict:
    """
    Performs a semantic search over the indexed specs.
    """
    try:
        results = vector_search.search(query, n_results)
        return {"status": "success", "data": results}
    except Exception as e:
        return {"status": "error", "error": str(e)}


@mcp.tool
def search_by_tag(tag: str) -> dict:
    """
    Searches for specs with a specific tag in their frontmatter.
    """
    results = []
    try:
        base_path = _get_safe_path("")
        for root, _, files in os.walk(base_path):
            for file in files:
                if file.endswith(".md"):
                    full_path = os.path.join(root, file)
                    relative_path = os.path.relpath(full_path, base_path)
                    try:
                        with open(full_path, "r", encoding="utf-8") as f:
                            spec = frontmatter.load(f)
                            if "tags" in spec.metadata and tag in spec.metadata["tags"]:
                                results.append(relative_path)
                    except Exception:
                        continue
        return {"status": "success", "data": results}
    except (PermissionError, FileNotFoundError) as e:
        return {"status": "error", "error": str(e)}


def main():
    """Runs the MCP server."""
    mcp.run(transport="stdio")


if __name__ == "__main__":
    main()