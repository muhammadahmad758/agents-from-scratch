"""
Agent memory system.

Memory is explicit storage, not consciousness.
It's data that persists across agent steps and can be queried.
"""

import json
from pathlib import Path


class Memory:
    """
    Simple memory storage for the agent.
    
    This is intentionally basic and grows in lessons:
    - Lesson 07: Basic list-based memory
    - Persistence: save()/load() write the items to a JSON file,
      so memory survives across restarts
    - Future: Add semantic search, etc.
    """
    
    def __init__(self):
        """Initialize empty memory."""
        self.items = []
    
    def add(self, item: str):
        """
        Add an item to memory.
        
        Args:
            item: String to remember
        """
        if item and item not in self.items:
            self.items.append(item)
    
    def get_all(self) -> list[str]:
        """
        Retrieve all memory items.
        
        Returns:
            List of all stored items
        """
        return self.items.copy()
    
    def get_recent(self, n: int = 5) -> list[str]:
        """
        Get the n most recent memory items.
        
        Args:
            n: Number of recent items to retrieve
            
        Returns:
            List of recent items
        """
        return self.items[-n:] if self.items else []
    
    def search(self, query: str) -> list[str]:
        """
        Simple search through memory items.
        
        Args:
            query: String to search for
            
        Returns:
            List of items containing the query
        """
        query_lower = query.lower()
        return [item for item in self.items if query_lower in item.lower()]
    
    def clear(self):
        """Clear all memory."""
        self.items = []
    
    def save(self, filepath: str):
        """
        Save memory items to a JSON file.
        
        The file is a plain JSON list of strings, so it can be
        inspected or edited by hand.
        
        Args:
            filepath: Path of the JSON file to write
        """
        Path(filepath).write_text(
            json.dumps(self.items, indent=2), encoding="utf-8"
        )
    
    def load(self, filepath: str) -> int:
        """
        Load memory items from a JSON file written by save().
        
        Loaded items replace the current items. If the file does
        not exist, memory is left unchanged.
        
        Args:
            filepath: Path of the JSON file to read
            
        Returns:
            Number of items loaded (0 if the file does not exist)
            
        Raises:
            ValueError: If the file does not contain a JSON list
        """
        path = Path(filepath)
        if not path.exists():
            return 0
        
        data = json.loads(path.read_text(encoding="utf-8"))
        if not isinstance(data, list):
            raise ValueError("Memory file must contain a JSON list")
        
        self.items = []
        for item in data:
            if isinstance(item, str):
                self.add(item)
        return len(self.items)
    
    def __len__(self) -> int:
        """Return the number of items in memory."""
        return len(self.items)
    
    def __repr__(self) -> str:
        """String representation of memory."""
        return f"Memory({len(self.items)} items)"