"""Stats display menu"""

import logging
from typing import Optional
from ui.base_menu import BaseMenu
from hardware.buttons import Button
from core.chao import Chao

logger = logging.getLogger(__name__)


class StatsMenu(BaseMenu):
    """Display Chao statistics"""
    
    def __init__(self, display, buttons, renderer, chao: Chao):
        super().__init__(display, buttons, renderer)
        self.chao = chao
    
    def render(self):
        """Render stats screen"""
        stats_lines = [
            f"Swim: Lv {int(self.chao.swim)}",
            f"Fly: Lv {int(self.chao.fly)}",
            f"Run: Lv {int(self.chao.run)}",
            f"Power: Lv {int(self.chao.power)}",
            f"Dark/Hero: {self.chao.dark}/{self.chao.hero}",
            f"Age: {int(self.chao.age)}",
            f"Meters: {self.chao.meters_walked}"
        ]
        
        image = self.renderer.render_menu(stats_lines, -1)  # No selection
        self.display.display(image)
    
    def handle_input(self) -> Optional[str]:
        """Handle stats screen input"""
        if self.buttons.is_pressed(Button.A) or self.buttons.is_pressed(Button.B):
            self.deactivate()
            return "back"
        
        return None
