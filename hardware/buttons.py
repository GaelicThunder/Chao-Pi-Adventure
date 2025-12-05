"""Button input handling"""

import logging
import time
from typing import Callable, Dict, Optional
from enum import Enum
from config import HardwareConfig

logger = logging.getLogger(__name__)


class Button(Enum):
    """Button identifiers"""
    LEFT = "L"
    RIGHT = "R"
    UP = "U"
    DOWN = "D"
    CENTER = "C"
    A = "A"
    B = "B"


class ButtonHandler:
    """Handles button input with debouncing"""
    
    def __init__(self, use_hardware: bool = True):
        self.use_hardware = use_hardware
        self.buttons: Dict[Button, any] = {}
        self.last_press_time: Dict[Button, float] = {}
        self.debounce_delay = 0.2
        
        if use_hardware:
            self._init_hardware()
        else:
            logger.info("Button handler in virtual mode")
    
    def _init_hardware(self):
        """Initialize GPIO buttons"""
        try:
            import board
            import busio
            from digitalio import DigitalInOut, Direction, Pull
            
            pin_map = {
                Button.LEFT: board.D27,
                Button.RIGHT: board.D23,
                Button.UP: board.D17,
                Button.DOWN: board.D22,
                Button.CENTER: board.D4,
                Button.A: board.D5,
                Button.B: board.D6
            }
            
            for button, pin in pin_map.items():
                btn = DigitalInOut(pin)
                btn.direction = Direction.INPUT
                btn.pull = Pull.UP
                self.buttons[button] = btn
                self.last_press_time[button] = 0
            
            logger.info("Hardware buttons initialized")
            
        except Exception as e:
            logger.error(f"Failed to initialize buttons: {e}")
            self.use_hardware = False
    
    def is_pressed(self, button: Button) -> bool:
        """Check if button is currently pressed with debouncing"""
        if not self.use_hardware:
            return False
        
        current_time = time.time()
        
        # Check if enough time has passed since last press
        if current_time - self.last_press_time[button] < self.debounce_delay:
            return False
        
        # Check hardware state (buttons are active LOW)
        if button in self.buttons:
            is_pressed = not self.buttons[button].value
            if is_pressed:
                self.last_press_time[button] = current_time
            return is_pressed
        
        return False
    
    def wait_for_release(self, button: Button, timeout: float = 1.0):
        """Wait for button to be released"""
        if not self.use_hardware:
            return
        
        start_time = time.time()
        while time.time() - start_time < timeout:
            if not self.is_pressed(button):
                return
            time.sleep(0.05)
    
    def any_pressed(self) -> Optional[Button]:
        """Return first pressed button or None"""
        for button in Button:
            if self.is_pressed(button):
                return button
        return None
