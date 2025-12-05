"""Main Chao screen with animations"""

import logging
import time
from typing import Optional
from hardware.display import BaseDisplay
from hardware.buttons import ButtonHandler, Button
from ui.renderer import Renderer
from core.chao import Chao
from config import SpriteConfig, DisplayConfig

logger = logging.getLogger(__name__)


class MainScreen:
    """Main game screen showing Chao and environment"""
    
    def __init__(self,
                 display: BaseDisplay,
                 buttons: ButtonHandler,
                 renderer: Renderer,
                 chao: Chao):
        self.display = display
        self.buttons = buttons
        self.renderer = renderer
        self.chao = chao
        
        self.active = True
        self.current_animation = SpriteConfig.WALK
        self.current_y_animation = [0, 0, 0, 0]
        self.background_moving = True
        self.background_index = 0
        self.background_sprite = "18.jpg"
        
        self.last_update = time.time()
        self.animation_interval = DisplayConfig.ANIMATION_TIME
    
    def set_animation(self, animation: list, y_animation: list, moving: bool = True):
        """Change current animation"""
        self.current_animation = animation
        self.current_y_animation = y_animation
        self.background_moving = moving
    
    def render(self):
        """Render current frame"""
        if not self.active:
            return
        
        # Check if it's time to update frame
        current_time = time.time()
        if current_time - self.last_update < self.animation_interval:
            return
        
        self.last_update = current_time
        
        # Render Chao with current animation
        image = self.renderer.render_chao(
            self.chao.appearance,
            self.background_sprite,
            self.current_animation,
            self.current_y_animation,
            self.background_index,
            self.background_moving
        )
        
        self.display.display(image)
        self.renderer.advance_frame()
    
    def handle_input(self) -> Optional[str]:
        """Handle button input"""
        if self.buttons.is_pressed(Button.B):
            return "open_menu"
        
        if self.buttons.is_pressed(Button.CENTER):
            return "toggle_power"
        
        if self.buttons.is_pressed(Button.UP):
            self.display.set_contrast(255)
        
        if self.buttons.is_pressed(Button.DOWN):
            self.display.set_contrast(0)
        
        return None
    
    def update(self) -> Optional[str]:
        """Update and render frame, return action"""
        self.render()
        return self.handle_input()
