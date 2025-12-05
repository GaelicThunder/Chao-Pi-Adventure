"""Inventory menu screen"""

import logging
from typing import Optional
from ui.base_menu import BaseMenu
from hardware.buttons import Button
from core.chao import Chao
from core.inventory import Inventory
from config import SpriteConfig

logger = logging.getLogger(__name__)


class InventoryMenu(BaseMenu):
    """Inventory management menu"""
    
    def __init__(self, display, buttons, renderer, chao: Chao, inventory: Inventory):
        super().__init__(display, buttons, renderer)
        self.chao = chao
        self.inventory = inventory
        self.items = [
            "Swim Fruit", "Fly Fruit", "Run Fruit", "Power Fruit",
            "Dark Fruit", "Hero Fruit", "Chao Fruit"
        ]
    
    def render(self):
        """Render inventory with item counts"""
        counts = self.inventory.get_all_counts()
        
        options_with_counts = [
            f"{item}: {counts.get(item, 0)}" for item in self.items
        ]
        
        image = self.renderer.render_menu(
            options_with_counts,
            self.selected_index
        )
        self.display.display(image)
    
    def handle_input(self) -> Optional[str]:
        """Handle inventory navigation and item use"""
        if self.buttons.is_pressed(Button.UP):
            self.navigate_up(len(self.items) - 1)
        
        elif self.buttons.is_pressed(Button.DOWN):
            self.navigate_down(len(self.items) - 1)
        
        elif self.buttons.is_pressed(Button.B):
            # Use selected item
            selected_item = self.items[self.selected_index]
            if self.inventory.remove_item(selected_item):
                self.chao.consume_item(selected_item)
                logger.info(f"Used {selected_item}")
                return "eat_animation"
        
        elif self.buttons.is_pressed(Button.A):
            self.deactivate()
            return "back"
        
        return None
