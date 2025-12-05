"""Fight mini-game (coming soon)"""

import logging
import time
import random
from typing import Optional
from PIL import Image, ImageDraw
from ui.base_menu import BaseMenu
from hardware.buttons import Button
from core.chao import Chao
from config import DisplayConfig, SpriteConfig

logger = logging.getLogger(__name__)


class Fighter:
    """Represents a fighter in combat"""
    
    def __init__(self, name: str, chao_type: str, power: float, 
                 stamina: int, is_player: bool = False):
        self.name = name
        self.chao_type = chao_type
        self.max_power = power
        self.power = power
        self.max_stamina = stamina
        self.stamina = stamina
        self.is_player = is_player
        self.action = "idle"
        self.charge = 0
    
    def take_damage(self, damage: float):
        """Take damage"""
        self.stamina = max(0, self.stamina - int(damage))
    
    def is_alive(self) -> bool:
        """Check if fighter is still alive"""
        return self.stamina > 0


class FightGame:
    """Turn-based fight mini-game"""
    
    def __init__(self, display, buttons, renderer, chao: Chao):
        self.display = display
        self.buttons = buttons
        self.renderer = renderer
        self.chao = chao
        
        # Create fighters
        self.player = Fighter(
            chao.name,
            chao.appearance,
            chao.power,
            chao.stamina,
            is_player=True
        )
        
        self.opponent = self._generate_opponent()
        self.turn = "player"
        self.message = "Fight Start!"
    
    def _generate_opponent(self) -> Fighter:
        """Generate AI opponent"""
        names = ["Bruiser", "Crusher", "Brawler", "Titan", "Goliath"]
        opponent_power = self.chao.power + random.randint(-2, 2)
        opponent_stamina = self.chao.stamina + random.randint(-10, 10)
        
        return Fighter(
            random.choice(names),
            "Power.jpg",
            max(1, opponent_power),
            max(10, opponent_stamina),
            is_player=False
        )
    
    def run(self) -> bool:
        """Run fight, return True if player wins"""
        logger.info(f"Fight: {self.player.name} vs {self.opponent.name}")
        
        while self.player.is_alive() and self.opponent.is_alive():
            if self.turn == "player":
                self._render_fight()
                action = self._player_turn()
                if action == "quit":
                    return False
                self.turn = "opponent"
            else:
                self._opponent_turn()
                self.turn = "player"
            
            time.sleep(0.5)
        
        # Determine winner
        if self.player.is_alive():
            self._show_result("VICTORY!")
            reward = random.randint(10, 20)
            self.chao.add_money(reward)
            logger.info(f"Fight won: +¥{reward}")
            return True
        else:
            self._show_result("DEFEAT...")
            logger.info("Fight lost")
            return False
    
    def _player_turn(self) -> str:
        """Handle player turn"""
        actions = ["Attack", "Charge", "Defend"]
        selected = 0
        
        while True:
            # Render action menu
            canvas = Image.new("1", (DisplayConfig.WIDTH, DisplayConfig.HEIGHT), "black")
            draw = ImageDraw.Draw(canvas)
            font = self.renderer.load_font("C&C Red Alert [INET].ttf", 12)
            
            # Draw fighters
            draw.text((5, 5), f"{self.player.name}: {self.player.stamina}", 
                     font=font, fill="white")
            draw.text((DisplayConfig.WIDTH - 60, 5), f"{self.opponent.name}: {self.opponent.stamina}", 
                     font=font, fill="white")
            
            # Draw actions
            y_offset = 35
            for i, action in enumerate(actions):
                prefix = "> " if i == selected else "  "
                draw.text((20, y_offset + i * 10), f"{prefix}{action}", 
                         font=font, fill="white")
            
            self.display.display(canvas)
            
            # Handle input
            if self.buttons.is_pressed(Button.UP):
                selected = (selected - 1) % len(actions)
                time.sleep(0.2)
            elif self.buttons.is_pressed(Button.DOWN):
                selected = (selected + 1) % len(actions)
                time.sleep(0.2)
            elif self.buttons.is_pressed(Button.B):
                # Perform action
                if actions[selected] == "Attack":
                    damage = self.player.power + self.player.charge
                    self.opponent.take_damage(damage)
                    self.message = f"Hit for {int(damage)} damage!"
                    self.player.charge = 0
                
                elif actions[selected] == "Charge":
                    self.player.charge += self.player.power * 0.5
                    self.message = "Charging up..."
                
                elif actions[selected] == "Defend":
                    self.player.stamina = min(self.player.max_stamina, 
                                            self.player.stamina + 5)
                    self.message = "Defending..."
                
                return "continue"
            
            elif self.buttons.is_pressed(Button.A):
                return "quit"
    
    def _opponent_turn(self):
        """AI opponent turn"""
        # Simple AI: attack if charged, otherwise charge
        if self.opponent.charge > self.opponent.max_power:
            damage = self.opponent.power + self.opponent.charge
            self.player.take_damage(damage)
            self.message = f"{self.opponent.name} hits for {int(damage)}!"
            self.opponent.charge = 0
        else:
            self.opponent.charge += self.opponent.power * 0.3
            self.message = f"{self.opponent.name} is charging..."
    
    def _render_fight(self):
        """Render fight scene"""
        canvas = Image.new("1", (DisplayConfig.WIDTH, DisplayConfig.HEIGHT), "black")
        draw = ImageDraw.Draw(canvas)
        font = self.renderer.load_font("C&C Red Alert [INET].ttf", 12)
        
        # Draw fighters
        draw.text((5, 5), f"{self.player.name}: {self.player.stamina}", 
                 font=font, fill="white")
        draw.text((DisplayConfig.WIDTH - 60, 5), f"{self.opponent.name}: {self.opponent.stamina}", 
                 font=font, fill="white")
        
        # Draw message
        draw.text((10, DisplayConfig.HEIGHT // 2), self.message, 
                 font=font, fill="white")
        
        self.display.display(canvas)
    
    def _show_result(self, result: str):
        """Show fight result"""
        image = self.renderer.render_text_screen(result, 24)
        self.display.display(image)
        time.sleep(2)
        
        # Wait for input
        while True:
            if self.buttons.is_pressed(Button.A) or self.buttons.is_pressed(Button.B):
                break
            time.sleep(0.1)
