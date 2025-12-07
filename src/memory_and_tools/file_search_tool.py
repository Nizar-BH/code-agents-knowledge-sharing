def file_search_tool(file_path: str) -> str:
    """
    Search for a file and return its content.

    Args:
        file_path (str): Path to the file to search.

    Returns:
        str: file content
    """
    try:
        with open(file_path, 'r') as f:
            lines = f.readlines()
        return "\n".join(lines) if lines else "No matches found."
    except Exception as e:
        return f"Error: {str(e)}"
