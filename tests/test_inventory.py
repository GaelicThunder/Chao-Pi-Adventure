"""Tests for Inventory system"""

import pytest
from core.inventory import Inventory


class TestInventory:
    """Test Inventory class"""
    
    def test_inventory_creation(self):
        """Test empty inventory creation"""
        inv = Inventory()
        assert inv.is_empty()
        assert len(inv.to_list()) == 0
    
    def test_add_remove_items(self):
        """Test adding and removing items"""
        inv = Inventory()
        
        inv.add_item("Run Fruit")
        assert not inv.is_empty()
        assert inv.get_count("Run Fruit") == 1
        
        success = inv.remove_item("Run Fruit")
        assert success
        assert inv.is_empty()
    
    def test_item_counts(self):
        """Test counting items"""
        inv = Inventory()
        
        inv.add_item("Fly Fruit")
        inv.add_item("Fly Fruit")
        inv.add_item("Run Fruit")
        
        counts = inv.get_all_counts()
        assert counts["Fly Fruit"] == 2
        assert counts["Run Fruit"] == 1
    
    def test_serialization(self):
        """Test list conversion"""
        inv = Inventory()
        inv.add_item("Swim Fruit")
        inv.add_item("Power Fruit")
        
        items = inv.to_list()
        restored = Inventory.from_list(items)
        
        assert restored.get_count("Swim Fruit") == 1
        assert restored.get_count("Power Fruit") == 1
