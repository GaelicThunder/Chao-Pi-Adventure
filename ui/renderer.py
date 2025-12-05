"""Sprite and animation rendering"""

import logging
from pathlib import Path
from typing import List, Tuple, Optional
from PIL import Image, ImageDraw, ImageFont
from config import SPRITES_DIR, FONTS_DIR, DisplayConfig, SpriteConfig

logger = logging.getLogger(__name__)


class Renderer:
    """Handles sprite rendering and animations"""
    
    def __init__(self):
        self.width = DisplayConfig.WIDTH
        self.height = DisplayConfig.HEIGHT
        self.sprite_cache = {}
        self.font_cache = {}
        self.frame = 0
    
    def load_sprite(self, filename: str) -> Optional[Image.Image]:
        """Load sprite image with caching"""
        if filename in self.sprite_cache:
            return self.sprite_cache[filename]
        
        try:
            path = SPRITES_DIR / filename
            img = Image.open(path).convert("1")
            self.sprite_cache[filename] = img
            return img
        except Exception as e:
            logger.error(f"Failed to load sprite {filename}: {e}")
            return None
    
    def load_font(self, name: str, size: int) -> ImageFont.FreeTypeFont:
        """Load font with caching"""
        key = f"{name}_{size}"
        if key in self.font_cache:
            return self.font_cache[key]
        
        try:
            path = FONTS_DIR / name
            font = ImageFont.truetype(str(path), size)
            self.font_cache[key] = font
            return font
        except Exception as e:
            logger.error(f"Failed to load font {name}: {e}")
            return ImageFont.load_default()
    
    def render_chao(self, 
                    chao_sprite: str,
                    background_sprite: str,
                    animation: List[int],
                    y_animation: List[int],
                    background_index: int = 0,
                    background_moving: bool = False) -> Image.Image:
        """Render Chao with background"""
        # Create blank canvas
        canvas = Image.new("L", (self.width, self.height), "white")
        
        # Load sprites
        chao_img = self.load_sprite(chao_sprite)
        bg_img = self.load_sprite(background_sprite)
        
        if not chao_img or not bg_img:
            return canvas
        
        # Calculate sprite positions
        w, h = SpriteConfig.SPRITE_WIDTH, SpriteConfig.SPRITE_HEIGHT
        bw, bh = SpriteConfig.BACKGROUND_WIDTH, SpriteConfig.BACKGROUND_HEIGHT
        
        # Extract current frame from spritesheet
        frame_idx = self.frame % len(animation)
        x = w * (animation[frame_idx] % 8)
        y = h * (y_animation[frame_idx] % 8)
        
        # Crop and scale Chao sprite
        scale = self.height / float(h)
        new_size = (int(scale * w), self.height)
        chao_frame = chao_img.crop((x, y, x + w, y + h)).resize(new_size, Image.LANCZOS)
        
        # Extract background tiles
        if background_moving:
            by = 94 + bh * background_index
        else:
            by = 94 + bh * background_index
        
        scale_b = self.height / float(bh)
        new_size_b = (int(scale_b * bw), self.height)
        
        # Left background tile
        bx_left = 38 + bw * ((self.frame * 2) % 8 if background_moving else 0)
        bg_left = bg_img.crop((bx_left, by, bx_left + bw, by + bh)).resize(new_size_b, Image.LANCZOS)
        
        # Right background tile
        bx_right = 38 + bw * (((self.frame * 2) + 1) % 8 if background_moving else 1)
        bg_right = bg_img.crop((bx_right, by, bx_right + bw, by + bh)).resize(new_size_b, Image.LANCZOS)
        
        # Composite image
        canvas.paste(bg_left, (0, 0))
        canvas.paste(chao_frame, ((self.width - chao_frame.width) // 2, 0))
        canvas.paste(bg_right, (self.width - bg_right.width, 0))
        
        return canvas
    
    def render_text_screen(self, 
                           text: str, 
                           font_size: int = 24,
                           additional_elements: Optional[List[Tuple[str, Tuple[int, int], int]]] = None) -> Image.Image:
        """Render simple text screen"""
        canvas = Image.new("1", (self.width, self.height), "black")
        draw = ImageDraw.Draw(canvas)
        
        # Main text
        font = self.load_font("C&C Red Alert [INET].ttf", font_size)
        text_width, text_height = draw.textsize(text, font=font)
        x = (self.width - text_width) // 2
        y = (self.height - text_height) // 2
        draw.text((x, y), text, font=font, fill="white")
        
        # Additional elements
        if additional_elements:
            for elem_text, pos, size in additional_elements:
                elem_font = self.load_font("C&C Red Alert [INET].ttf", size)
                draw.text(pos, elem_text, font=elem_font, fill="white")
        
        return canvas
    
    def render_menu(self, 
                   options: List[str],
                   selected_index: int,
                   money: Optional[int] = None,
                   battery: Optional[int] = None) -> Image.Image:
        """Render menu with selectable options"""
        canvas = Image.new("1", (self.width, self.height), "black")
        draw = ImageDraw.Draw(canvas)
        font = self.load_font("C&C Red Alert [INET].ttf", 12)
        
        # Render options
        y_offset = 0
        for i, option in enumerate(options):
            prefix = "> " if i == selected_index else "  "
            draw.text((5, y_offset), f"{prefix}{option}", font=font, fill="white")
            y_offset += 9
        
        # Render money
        if money is not None:
            draw.text((self.width - 25, 54), f"¥{money}", font=font, fill="white")
        
        # Render battery
        if battery is not None:
            draw.text((self.width - 20, 0), f"{battery}%", font=font, fill="white")
        
        return canvas
    
    def advance_frame(self):
        """Advance animation frame"""
        self.frame = (self.frame + 1) % SpriteConfig.MAX_FRAMES
    
    def reset_frame(self):
        """Reset animation frame to 0"""
        self.frame = 0
