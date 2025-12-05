"""Main menu screen"""

import logging
from typing import Optional
from ui.base_menu import BaseMenu
from hardware.buttons import Button

logger = logging.getLogger(__name__)


class MainMenu(BaseMenu):
    """Main menu with game options"""
    
    def __init__(self, display, buttons, renderer):
        super().__init__(display, buttons, renderer)
        self.options = ["Games", "Shop", "Stats", "Friend", "Inventory"]
    
    def render(self):
        """Render main menu"""
        image = self.renderer.render_menu(self.options, self.selected_index)
        self.display.display(image)
    
    def handle_input(self) -> Optional[str]:
        """Handle menu navigation"""
        if self.buttons.is_pressed(Button.LEFT):
            self.navigate_left(len(self.options))
        
        elif self.buttons.is_pressed(Button.RIGHT):
            self.navigate_right(len(self.options))
        
        elif self.buttons.is_pressed(Button.B):
            # Select option
            selected = self.options[self.selected_index].lower()
            self.deactivate()
            return selected
        
        elif self.buttons.is_pressed(Button.A):
            # Exit menu
            self.deactivate()
            return "back"
        
        return None
