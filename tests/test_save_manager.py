"""Tests for SaveManager"""

import pytest
import tempfile
from pathlib import Path
from core.chao import Chao
from core.inventory import Inventory
from core.save_manager import SaveManager
from config import SAVE_FILE, BACKUP_FILE


class TestSaveManager:
    """Test SaveManager class"""
    
    def test_save_and_load(self, tmp_path):
        """Test saving and loading"""
        # Override save path for testing
        import config
        original_save = config.SAVE_FILE
        original_backup = config.BACKUP_FILE
        
        config.SAVE_FILE = tmp_path / "test.save"
        config.BACKUP_FILE = tmp_path / "test.bak"
        
        try:
            # Create test data
            chao = Chao("TestChao")
            chao.fly = 15
            chao.money = 100
            
            inv = Inventory()
            inv.add_item("Run Fruit")
            
            # Save
            manager = SaveManager()
            success = manager.save(chao, inv, 1)
            assert success
            assert config.SAVE_FILE.exists()
            
            # Load
            result = manager.load()
            assert result is not None
            
            loaded_chao, loaded_inv, bg_index = result
            assert loaded_chao.name == "TestChao"
            assert loaded_chao.fly == 15
            assert loaded_chao.money == 100
            assert loaded_inv.get_count("Run Fruit") == 1
            assert bg_index == 1
        
        finally:
            # Restore original paths
            config.SAVE_FILE = original_save
            config.BACKUP_FILE = original_backup
