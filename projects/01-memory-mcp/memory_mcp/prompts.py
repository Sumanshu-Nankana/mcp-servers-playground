def memory_assistant_prompt() -> str:
    """Get help with memory operations and best practices"""
    return """You are using MemoryMCP for long-term memory management.

How to use:
- save_memory: Save facts, preferences, or anything user wants remembered
- search_memory: Semantic search before answering any question
- list_memories: Browse all saved memories
- delete_memory: Remove a specific memory (find ID via search/list first)
- delete_all_memories: Clear everything

Best practices:
- ALWAYS search memories before answering user questions
- Save any preference or fact the user mentions
- When user says "remember that..." always call save_memory
- When deleting specific memory, first search/list to find the ID"""
