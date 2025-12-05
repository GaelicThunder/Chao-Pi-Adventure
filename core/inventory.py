"""Inventory management"""

from typing import List, Dict
from collections import Counter
from config import GameConfig


class Inventory:
    """Manages items and shop interactions"""
    
    def __init__(self):
        self.items: List[str] = []
    
    def add_item(self, item: str):
        """Add item to inventory"""
        if item in GameConfig.ITEM_LIST:
            self.items.append(item)
    
    def remove_item(self, item: str) -> bool:
        """Remove one instance of item"""
        if item in self.items:
            self.items.remove(item)
            return True
        return False
    
    def get_count(self, item: str) -> int:
        """Count instances of specific item"""
        return self.items.count(item)
    
    def get_all_counts(self) -> Dict[str, int]:
        """Get counts of all items"""
        return dict(Counter(self.items))
    
    def is_empty(self) -> bool:
        """Check if inventory is empty"""
        return len(self.items) == 0
    
    def clear(self):
        """Clear all items"""
        self.items.clear()
    
    def to_list(self) -> List[str]:
        """Return copy of items list"""
        return self.items.copy()
    
    @classmethod
    def from_list(cls, items: List[str]) -> 'Inventory':
        """Create inventory from list"""
        inv = cls()
        inv.items = items.copy()
        return inv
