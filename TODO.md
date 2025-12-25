# Suggestions for mdspec MCP Server Improvement

Based on my experience interacting with the `mdspec` tools to find the specification for `RoutingActivationResponse`, here are some suggestions for improving the `mdspec` MCP server, with reference to the existing tools.

The available `mdspec` tools are: `list_specs`, `read_spec`, `search_specs`, `search_in_spec`, `get_table_of_contents`, `index_specs`, `semantic_search`, `search_by_tag`.

## 1. Improve Search Flexibility and Accuracy

This suggestion relates to improving the core search functionality provided by `search_specs`, `search_in_spec`, and `semantic_search`.

*   **Problem**: The keyword-based search (`search_specs`, `search_in_spec`) appears to be too literal. A search for "RoutingActivationResponse" yielded no results, while "Routing Activation" did. This suggests a lack of flexibility.
*   **Suggestion**:
    *   **Fuzzy Search & Stemming**: Implement fuzzy search (e.g., Levenshtein distance) and stemming in `search_specs` and `search_in_spec` to handle minor typos, pluralization, and different word forms. Case-insensitivity should be the default.
    *   **Enhanced Indexing**: The `index_specs` tool, which likely powers `semantic_search` and `search_specs`, could be improved to create a more robust index. This could involve extracting and weighing keywords from headings, tables, and bolded text to improve result relevance.

## 2. Enhance Structured Data Handling (especially Tables)

This suggestion focuses on making search results from structured data, like tables, more useful. It primarily concerns `search_specs` and `search_in_spec`.

*   **Problem**: When a search match was found within a table, the returned snippet was just text, making it very difficult to understand the table's structure. I had to piece the table back together from fragmented text snippets.
*   **Suggestion**:
    *   **Table-Aware Output**: `search_specs` and `search_in_spec` should detect if a match is inside a table. If so, they should return a structured representation of the table (e.g., as a JSON object or a formatted Markdown table) or at least the full row with its corresponding headers.
    *   **New Tool Proposal: `get_table`**: Introduce a new tool, e.g., `get_table(file_path: str, table_identifier: str) -> str`, specifically designed to extract and return a full, formatted table from a specification file based on its title or number (e.g., 'Table 48'). This would be a significant improvement over trying to reconstruct tables from text snippets.

## 3. Provide Better Context in Search Results

This is an improvement for the output of `search_specs` and `search_in_spec`.

*   **Problem**: Search results currently provide a snippet of text but lack the broader context of where that text resides in the document.
*   **Suggestion**: Enhance the output of search tools to include the section heading of the markdown document where the match was found. The `get_table_of_contents` tool could potentially be used by the backend to find the relevant section heading for a given line number.

## 4. Ensure Environmental Consistency

This is a general suggestion about the environment in which the agent and the tools operate.

*   **Problem**: I encountered a discrepancy where `list_directory` could not see `ISO_13400_2_2019.md`, but `read_spec` could access it. This inconsistency is confusing and leads to wasted effort.
*   **Suggestion**: The file system view should be consistent. The `list_specs` tool should list all files that `read_spec` and other `mdspec` tools can access. If spec files are in a special, non-obvious location, this location should be made visible or documented.

## 5. Guiding Tool Usage with Prompts

This suggestion addresses how to guide the model towards using `list_specs` over `list_directory` when appropriate.

*   **Problem**: There's an overlap in functionality between `list_directory` (general CLI tool) and `list_specs` (specialized `mdspec` tool), leading to potential confusion when listing specification-related files.
*   **Suggestion**: Implement context-aware prompts or enhanced error handling within the CLI or the `mdspec` tools:
    *   **"Did you mean `list_specs`?" Prompt**: If `list_directory` is used on a path commonly associated with specifications (e.g., `specs/`, `.specify/`) and returns no results or an incomplete list, the system could issue a prompt like: "It looks like you're trying to list specification documents. You might find more relevant information using the `mdspec` tool: `list_specs`. Would you like to try `list_specs` instead?"
    *   **Proactive `mdspec` Suggestion**: When a user's request contains keywords related to specifications (e.g., "list specs", "search docs", "requirements files"), the `mdspec` MCP server could proactively prompt: "For tasks involving project specifications or documentation, consider using the specialized `mdspec` tools: `list_specs`, `read_spec`, `search_specs`, etc."
    *   **Enhanced Tool Descriptions**: Update the `mdspec` tool descriptions to explicitly state their purpose and preferred usage scenarios, e.g., "`list_specs`: Use this to list specification documents managed by the `mdspec` server, ensuring you retrieve structured specification metadata."
