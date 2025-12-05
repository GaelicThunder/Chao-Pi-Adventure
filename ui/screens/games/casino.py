"""Casino slot machine mini-game"""

import logging
import time
import random
from typing import List, Optional
from PIL import Image, ImageDraw
from ui.base_menu import BaseMenu
from hardware.buttons import Button
from core.chao import Chao
from config import DisplayConfig, SPRITES_DIR

logger = logging.getLogger(__name__)


class CasinoGame:
    """Slot machine casino game"""
    
    def __init__(self, display, buttons, renderer, chao: Chao):
        self.display = display
        self.buttons = buttons
        self.renderer = renderer
        self.chao = chao
        
        self.bet = 1
        self.spinning = False
        
        # Load slot symbols
        self.symbols = self._load_symbols()
        self.reels = [list(self.symbols.keys()) for _ in range(3)]
        self.reel_positions = [0, 0, 0]
        self.reel_stopped = [False, False, False]
    
    def _load_symbols(self) -> dict:
        """Load and resize slot symbols"""
        symbols = {}
        symbol_files = ["banana.jpg", "chao.jpg", "seven.jpg", "esclamation.jpg"]
        
        for filename in symbol_files:
            try:
                img = self.renderer.load_sprite(filename)
                if img:
                    symbols[filename] = img.resize((24, 24), Image.LANCZOS)
            except Exception as e:
                logger.error(f"Failed to load symbol {filename}: {e}")
        
        return symbols
    
    def run(self) -> bool:
        """Run casino game, return True to continue playing"""
        while True:
            # Check if player has money
            if self.chao.money < 1:
                self._show_message("NO MONEY!")
                return False
            
            # Show bet selection
            action = self._bet_screen()
            
            if action == "quit":
                return False
            elif action == "spin":
                result = self._spin_reels()
                self._handle_result(result)
    
    def _bet_screen(self) -> str:
        """Bet selection screen"""
        while True:
            # Render bet screen
            canvas = Image.new("1", (DisplayConfig.WIDTH, DisplayConfig.HEIGHT), "black")
            draw = ImageDraw.Draw(canvas)
            font = self.renderer.load_font("C&C Red Alert [INET].ttf", 12)
            
            # Show current symbols
            x_offset = 10
            for i in range(3):
                symbol_key = list(self.symbols.keys())[self.reel_positions[i] % len(self.symbols)]
                if symbol_key in self.symbols:
                    canvas.paste(self.symbols[symbol_key], (x_offset + i * 42, 24))
            
            # Show bet and money
            draw.text((0, 54), f"Bet: ¥{self.bet}", font=font, fill="white")
            draw.text((DisplayConfig.WIDTH - 35, 54), f"¥{self.chao.money}", font=font, fill="white")
            
            self.display.display(canvas)
            
            # Handle input
            if self.buttons.is_pressed(Button.UP):
                if self.bet < self.chao.money:
                    self.bet += 1
                time.sleep(0.1)
            elif self.buttons.is_pressed(Button.DOWN):
                if self.bet > 1:
                    self.bet -= 1
                time.sleep(0.1)
            elif self.buttons.is_pressed(Button.B):
                # Spin!
                self.chao.spend_money(self.bet)
                return "spin"
            elif self.buttons.is_pressed(Button.A):
                return "quit"
    
    def _spin_reels(self) -> List[str]:
        """Animate spinning reels and return result"""
        # Reset state
        self.reel_stopped = [False, False, False]
        stop_count = 0
        
        # Randomize starting positions
        for i in range(3):
            self.reels[i] = list(self.symbols.keys())
            random.shuffle(self.reels[i])
        
        # Spin animation
        while stop_count < 3:
            # Update reel positions
            for i in range(3):
                if not self.reel_stopped[i]:
                    self.reel_positions[i] = (self.reel_positions[i] + 1) % len(self.reels[i])
            
            # Check for stop input
            if self.buttons.is_pressed(Button.B) and stop_count < 3:
                self.reel_stopped[stop_count] = True
                stop_count += 1
                time.sleep(0.2)
            
            # Render spinning reels
            self._render_reels()
            time.sleep(0.1)
        
        # Get final symbols
        result = [
            self.reels[i][self.reel_positions[i] % len(self.reels[i])]
            for i in range(3)
        ]
        
        return result
    
    def _render_reels(self):
        """Render current reel state"""
        canvas = Image.new("1", (DisplayConfig.WIDTH, DisplayConfig.HEIGHT), "black")
        
        # Draw symbols
        x_offset = 10
        for i in range(3):
            if self.reel_stopped[i]:
                # Show stopped symbol
                symbol_key = self.reels[i][self.reel_positions[i] % len(self.reels[i])]
            else:
                # Show moving symbols (blur effect)
                symbol_key = self.reels[i][self.reel_positions[i] % len(self.reels[i])]
            
            if symbol_key in self.symbols:
                canvas.paste(self.symbols[symbol_key], (x_offset + i * 42, 24))
        
        self.display.display(canvas)
    
    def _handle_result(self, result: List[str]):
        """Handle spin result and payout"""
        # Check for win
        if result[0] == result[1] == result[2]:
            # All match!
            symbol = result[0]
            
            # Determine payout
            if symbol == "banana.jpg":
                payout = self.bet * 2
            elif symbol == "esclamation.jpg":
                payout = self.bet * 3
            elif symbol == "chao.jpg":
                payout = self.bet * 5
            elif symbol == "seven.jpg":
                payout = self.bet * 10
            else:
                payout = self.bet
            
            self.chao.add_money(payout)
            self._show_message(f"WIN! +¥{payout}")
            logger.info(f"Casino win: ¥{payout}")
        else:
            self._show_message("TRY AGAIN")
            logger.info("Casino loss")
        
        # Reset bet
        self.bet = 1
    
    def _show_message(self, message: str):
        """Show a message screen"""
        image = self.renderer.render_text_screen(message, 20)
        self.display.display(image)
        time.sleep(2)
