"""Display abstraction supporting multiple display types"""

import logging
from abc import ABC, abstractmethod
from typing import Optional
from PIL import Image
from config import DisplayConfig, SPRITES_DIR

logger = logging.getLogger(__name__)


class BaseDisplay(ABC):
    """Abstract base display interface"""
    
    def __init__(self):
        self.width = DisplayConfig.WIDTH
        self.height = DisplayConfig.HEIGHT
        self.contrast = 255
    
    @abstractmethod
    def display(self, image: Image.Image):
        """Display image"""
        pass
    
    @abstractmethod
    def clear(self):
        """Clear display"""
        pass
    
    @abstractmethod
    def show(self):
        """Turn on display"""
        pass
    
    @abstractmethod
    def hide(self):
        """Turn off display"""
        pass
    
    def set_contrast(self, value: int):
        """Set display contrast (0-255)"""
        self.contrast = max(0, min(255, value))


class OLEDDisplay(BaseDisplay):
    """OLED display using luma.oled"""
    
    def __init__(self):
        super().__init__()
        try:
            from demo_opts import get_device
            self.device = get_device()
            logger.info("OLED display initialized")
        except Exception as e:
            logger.error(f"Failed to initialize OLED: {e}")
            raise
    
    def display(self, image: Image.Image):
        """Display image on OLED"""
        self.device.display(image.convert(self.device.mode))
    
    def clear(self):
        """Clear OLED"""
        blank = Image.new("1", (self.width, self.height), "black")
        self.device.display(blank)
    
    def show(self):
        """Turn on OLED"""
        self.device.show()
    
    def hide(self):
        """Turn off OLED"""
        self.device.hide()
    
    def set_contrast(self, value: int):
        """Set OLED contrast"""
        super().set_contrast(value)
        self.device.contrast(self.contrast)


class WaveShareDisplay(BaseDisplay):
    """WaveShare e-paper display"""
    
    def __init__(self):
        super().__init__()
        try:
            from lib.waveshare_epd import epd2in13_V2
            self.epd = epd2in13_V2.EPD()
            self.epd.init(self.epd.FULL_UPDATE)
            self.epd.Clear(0xFF)
            self.display_width = self.epd.height
            self.display_height = self.epd.width
            self.needs_full_refresh = True
            logger.info("WaveShare display initialized")
        except Exception as e:
            logger.error(f"Failed to initialize WaveShare: {e}")
            raise
    
    def display(self, image: Image.Image):
        """Display image on e-paper"""
        img = image.convert("1")
        
        if not DisplayConfig.FULLSCREEN:
            # Center image
            centered = Image.new("1", (self.display_width, self.display_height), 255)
            x_offset = (self.display_width - img.width) // 4
            y_offset = (self.display_height - img.height) // 4
            centered.paste(img, (x_offset, y_offset))
            img = centered
        else:
            img = img.resize((250, 122), Image.LANCZOS)
        
        if self.needs_full_refresh:
            self.epd.display(self.epd.getbuffer(img))
            self.needs_full_refresh = False
        else:
            self.epd.init(self.epd.PART_UPDATE)
            self.epd.displayPartial(self.epd.getbuffer(img))
    
    def clear(self):
        """Clear e-paper display"""
        self.epd.Clear(0xFF)
        self.needs_full_refresh = True
    
    def show(self):
        """Wake display"""
        self.epd.init(self.epd.FULL_UPDATE)
    
    def hide(self):
        """Sleep display"""
        self.epd.sleep()


class NullDisplay(BaseDisplay):
    """No display (headless mode for testing)"""
    
    def __init__(self):
        super().__init__()
        logger.info("Running in headless mode (no display)")
    
    def display(self, image: Image.Image):
        """Save image to file instead of displaying"""
        image.save("/tmp/chao_screen.png")
    
    def clear(self):
        pass
    
    def show(self):
        pass
    
    def hide(self):
        pass


def get_display() -> BaseDisplay:
    """Factory function to get appropriate display"""
    display_type = DisplayConfig.TYPE.lower()
    
    if display_type == "oled":
        return OLEDDisplay()
    elif display_type == "waveshare":
        return WaveShareDisplay()
    else:
        return NullDisplay()
