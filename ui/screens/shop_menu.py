"""Shop menu screen"""

import logging
from typing import Optional
from ui.base_menu import BaseMenu
from hardware.buttons import Button
from core.chao import Chao
from core.inventory import Inventory
from config import GameConfig

logger = logging.getLogger(__name__)


class ShopMenu(BaseMenu):
    """Shop menu for buying items"""
    
    def __init__(self, display, buttons, renderer, chao: Chao, inventory: Inventory):
        super().__init__(display, buttons, renderer)
        self.chao = chao
        self.inventory = inventory
        self.items = list(GameConfig.SHOP_PRICES.keys())
    
    def render(self):
        """Render shop with prices"""
        options_with_prices = [
            f"{item}: ¥{GameConfig.SHOP_PRICES[item]}" 
            for item in self.items
        ]
        
        image = self.renderer.render_menu(
            options_with_prices,
            self.selected_index,
            money=self.chao.money
        )
        self.display.display(image)
    
    def handle_input(self) -> Optional[str]:
        """Handle shop navigation and purchases"""
        if self.buttons.is_pressed(Button.UP):
            self.navigate_up(len(self.items) - 1)
        
        elif self.buttons.is_pressed(Button.DOWN):
            self.navigate_down(len(self.items) - 1)
        
        elif self.buttons.is_pressed(Button.B):
            # Purchase selected item
            selected_item = self.items[self.selected_index]
            price = GameConfig.SHOP_PRICES[selected_item]
            
            if self.chao.spend_money(price):
                self.inventory.add_item(selected_item)
                logger.info(f"Purchased {selected_item} for ¥{price}")
                self.render()  # Update display
        
        elif self.buttons.is_pressed(Button.A):
            self.deactivate()
            return "back"
        
        return None
