"""Save/load game state"""

import json
import logging
import shutil
from pathlib import Path
from typing import Optional, Tuple
from core.chao import Chao
from core.inventory import Inventory
from config import SAVE_FILE, BACKUP_FILE

logger = logging.getLogger(__name__)


class SaveManager:
    """Handles saving and loading game state"""
    
    @staticmethod
    def save(chao: Chao, inventory: Inventory, background_index: int = 0) -> bool:
        """Save game state to file"""
        try:
            data = {
                'chao': chao.to_dict(),
                'inventory': inventory.to_list(),
                'background_index': background_index,
                'version': '2.0'
            }
            
            # Create backup of existing save
            if SAVE_FILE.exists():
                shutil.copy(SAVE_FILE, BACKUP_FILE)
            
            # Write new save
            with open(SAVE_FILE, 'w') as f:
                json.dump(data, f, indent=2)
            
            logger.info("Game saved successfully")
            return True
            
        except Exception as e:
            logger.error(f"Failed to save game: {e}")
            return False
    
    @staticmethod
    def load() -> Optional[Tuple[Chao, Inventory, int]]:
        """Load game state from file"""
        try:
            # Check if save exists
            if not SAVE_FILE.exists():
                logger.info("No save file found")
                return None
            
            # Check if save is corrupted
            if SAVE_FILE.stat().st_size == 0:
                logger.warning("Save file corrupted, attempting backup restore")
                if BACKUP_FILE.exists() and BACKUP_FILE.stat().st_size > 0:
                    shutil.copy(BACKUP_FILE, SAVE_FILE)
                else:
                    logger.error("Backup also corrupted")
                    return None
            
            # Load save
            with open(SAVE_FILE, 'r') as f:
                data = json.load(f)
            
            # Reconstruct objects
            chao = Chao.from_dict(data['chao'])
            inventory = Inventory.from_list(data['inventory'])
            background_index = data.get('background_index', 0)
            
            logger.info(f"Game loaded successfully - Chao: {chao.name}")
            return chao, inventory, background_index
            
        except Exception as e:
            logger.error(f"Failed to load game: {e}")
            return None
    
    @staticmethod
    def exists() -> bool:
        """Check if save file exists"""
        return SAVE_FILE.exists() and SAVE_FILE.stat().st_size > 0
