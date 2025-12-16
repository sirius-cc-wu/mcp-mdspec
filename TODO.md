# `mdnotes` Improvement Proposals

This file outlines proposed improvements to enhance the `mdnotes` MCP server as a read-only notes management tool.

## Todo List

### Phase 1: Core Functionality Enhancements
- [ ] **Enhanced Search:**
    - [x] Improved `search_notes` implementation for direct file access.
    - [x] Add contextual lines to `search_notes` results.
    - [x] Implement a new `search_in_note(file_path, keyword)` tool.
- [ ] **Improved Navigation:**
    - [x] Create a `get_table_of_contents(file_path)` tool to generate a ToC from markdown headings.
- [ ] **Better Metadata:**
    - [x] Extend `list_notes` to include the last modified timestamp for each note.

### Phase 2: Advanced Features
- [ ] **Semantic Search:**
    - [x] Implement semantic search using a vector database (e.g., ChromaDB).
- [ ] **Tagging System:**
    - [ ] Implement a mechanism to associate tags with notes (e.g., in a separate metadata file or within the note frontmatter).
    - [ ] Create a `search_by_tag(tag)` tool.
- [ ] **Hierarchical Listing:**
    - [ ] Update `list_notes` to optionally return a hierarchical (tree-like) view of the notes directory.

### Phase 3: Usability & Configuration
- [ ] **Configuration:**
    - [ ] Improve configuration management to be more explicit and well-documented (e.g., detailing the use of `.env` files for `NOTES_DIR`).
- [ ] **Documentation:**
    - [ ] Enhance the `README.md` with detailed usage examples for all tools.
