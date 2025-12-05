"""Base menu class for UI screens"""

import logging
from abc import ABC, abstractmethod
from typing import Optional
from hardware.display import BaseDisplay
from hardware.buttons import ButtonHandler, Button
from ui.renderer import Renderer

logger = logging.getLogger(__name__)


class BaseMenu(ABC):
    """Abstract base class for menu screens"""
    
    def __init__(self, 
                 display: BaseDisplay, 
                 buttons: ButtonHandler, 
                 renderer: Renderer):
        self.display = display
        self.buttons = buttons
        self.renderer = renderer
        self.active = False
        self.selected_index = 0
    
    @abstractmethod
    def render(self):
        """Render current menu state"""
        pass
    
    @abstractmethod
    def handle_input(self) -> Optional[str]:
        """Handle button input, return action or None"""
        pass
    
    def activate(self):
        """Activate menu"""
        self.active = True
        self.selected_index = 0
        logger.debug(f"{self.__class__.__name__} activated")
    
    def deactivate(self):
        """Deactivate menu"""
        self.active = False
        logger.debug(f"{self.__class__.__name__} deactivated")
    
    def navigate_up(self, max_index: int):
        """Navigate up in menu"""
        if self.selected_index > 0:
            self.selected_index -= 1
    
    def navigate_down(self, max_index: int):
        """Navigate down in menu"""
        if self.selected_index < max_index:
            self.selected_index += 1
    
    def navigate_left(self, options: int):
        """Navigate left (circular)"""
        self.selected_index = (self.selected_index - 1) % options
    
    def navigate_right(self, options: int):
        """Navigate right (circular)"""
        self.selected_index = (self.selected_index + 1) % options
    
    def run(self) -> Optional[str]:
        """Main menu loop, returns next menu action"""
        self.activate()
        
        while self.active:
            self.render()
            action = self.handle_input()
            if action:
                return action
        
        return None
