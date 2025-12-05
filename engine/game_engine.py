"""Main game engine coordinating all systems"""

import logging
import time
import random
from typing import Optional
from core.chao import Chao
from core.inventory import Inventory
from core.save_manager import SaveManager
from hardware.display import get_display
from hardware.buttons import ButtonHandler, Button
from hardware.battery import BatteryMonitor
from ui.renderer import Renderer
from ui.screens.main_screen import MainScreen
from ui.screens.main_menu import MainMenu
from ui.screens.inventory_menu import InventoryMenu
from ui.screens.shop_menu import ShopMenu
from ui.screens.stats_menu import StatsMenu
from ui.screens.games_menu import GamesMenu
from ui.screens.friend_menu import FriendMenu
from config import GameConfig, SpriteConfig

logger = logging.getLogger(__name__)


class GameEngine:
    """Main game engine"""
    
    def __init__(self):
        # Hardware
        self.display = get_display()
        self.buttons = ButtonHandler(use_hardware=True)
        self.battery = BatteryMonitor()
        
        # Core systems
        self.renderer = Renderer()
        self.save_manager = SaveManager()
        
        # Game state
        self.chao: Optional[Chao] = None
        self.inventory: Optional[Inventory] = None
        self.background_index = 0
        
        # Screens
        self.main_screen: Optional[MainScreen] = None
        self.current_menu: Optional[str] = None
        
        # Timing
        self.last_decision = time.time()
        self.last_save = time.time()
        
        self.running = True
        self.powered_on = True
    
    def initialize(self):
        """Initialize game"""
        logger.info("Initializing game engine...")
        
        # Load or create new game
        save_data = self.save_manager.load()
        if save_data:
            self.chao, self.inventory, self.background_index = save_data
            logger.info(f"Loaded save: {self.chao.name}")
        else:
            self.chao = Chao()
            self.inventory = Inventory()
            self.background_index = random.randint(0, 2)
            logger.info("Started new game")
        
        # Initialize main screen
        self.main_screen = MainScreen(
            self.display,
            self.buttons,
            self.renderer,
            self.chao
        )
        
        logger.info("Game engine initialized")
    
    def update_decision(self):
        """Update Chao's decision and behavior"""
        current_time = time.time()
        if current_time - self.last_decision < GameConfig.VELOCITY_DEC:
            return
        
        self.last_decision = current_time
        
        # Random events
        encounter = random.randint(0, 100)
        place_change = random.randint(0, 100)
        
        # Make decision
        decision = random.choice(self.chao.moods)
        self.chao.current_decision = decision
        
        logger.debug(f"Decision: {decision}")
        
        # Apply decision effects
        if decision == "Walk":
            self.main_screen.set_animation(SpriteConfig.WALK, [0, 0, 0, 0], True)
            self.chao.age_up(0.001)
            self.chao.meters_walked += 1
            
            if place_change > 99:
                self.background_index = random.choice([0, 1, 2])
            
            if encounter > 99:
                item = random.choice(GameConfig.ITEM_LIST)
                self.inventory.add_item(item)
                logger.info(f"Found {item}!")
        
        elif decision == "Swim":
            if self.chao.swim / 10 > 2:
                self.main_screen.set_animation(SpriteConfig.SWIMMING, [4, 4, 4, 4], True)
                self.chao.age_up(0.001)
                self.chao.meters_walked += 1
                
                if encounter > 99:
                    item = random.choice(GameConfig.ITEM_LIST)
                    self.inventory.add_item(item)
            else:
                self.main_screen.set_animation(SpriteConfig.CANT_SWIM, [3, 4, 3, 4], False)
        
        elif decision == "Fly":
            self.main_screen.set_animation(SpriteConfig.FLY, [5, 5, 5, 5], True)
            self.chao.age_up(0.1)
            self.chao.meters_walked += 1
            
            if encounter > 99:
                item = random.choice(GameConfig.ITEM_LIST)
                self.inventory.add_item(item)
        
        elif decision == "Sleep":
            self.main_screen.set_animation(SpriteConfig.SLEEP, [3, 3, 3, 3], False)
            self.chao.restore_stamina(5)
        
        elif decision == "Sad":
            self.main_screen.set_animation(SpriteConfig.CRY, [3, 3, 3, 3], False)
            self.chao.restore_stamina(5)
        
        elif decision == "Tired":
            self.main_screen.set_animation(SpriteConfig.SIT, [0, 0, 0, 0], False)
            self.chao.restore_stamina(5)
        
        elif decision == "Happy":
            self.main_screen.set_animation(SpriteConfig.JUMP, [6, 7, 7, 7], False)
            self.chao.restore_stamina(5)
        
        elif decision == "Think":
            self.main_screen.set_animation(SpriteConfig.THINKING, [3, 3, 3, 3], False)
            self.chao.restore_stamina(5)
        
        elif decision == "Hello":
            self.main_screen.set_animation(SpriteConfig.HELLO_THERE, [7, 7, 7, 7], False)
            self.chao.restore_stamina(5)
        
        elif decision == "Draw":
            self.main_screen.set_animation(SpriteConfig.DRAWING, [1, 1, 1, 1], False)
            self.chao.restore_stamina(5)
    
    def auto_save(self):
        """Auto-save game state"""
        current_time = time.time()
        if current_time - self.last_save < GameConfig.SAVE_INTERVAL:
            return
        
        self.last_save = current_time
        success = self.save_manager.save(self.chao, self.inventory, self.background_index)
        
        if success:
            # Show save icon briefly
            logger.debug("Auto-saved game")
    
    def handle_menu_action(self, action: str):
        """Handle menu actions"""
        if action == "back":
            self.current_menu = None
            self.main_screen.active = True
        
        elif action == "inventory":
            menu = InventoryMenu(
                self.display, 
                self.buttons, 
                self.renderer, 
                self.chao, 
                self.inventory
            )
            result = menu.run()
            
            if result == "eat_animation":
                self.main_screen.set_animation(SpriteConfig.EAT, [5, 5, 5, 5], False)
                time.sleep(1.5)
            
            self.current_menu = None
            self.main_screen.active = True
        
        elif action == "shop":
            menu = ShopMenu(
                self.display, 
                self.buttons, 
                self.renderer,
                self.chao, 
                self.inventory
            )
            menu.run()
            self.current_menu = None
            self.main_screen.active = True
        
        elif action == "stats":
            menu = StatsMenu(
                self.display, 
                self.buttons, 
                self.renderer, 
                self.chao
            )
            menu.run()
            self.current_menu = None
            self.main_screen.active = True
        
        elif action == "games":
            menu = GamesMenu(
                self.display, 
                self.buttons, 
                self.renderer, 
                self.chao
            )
            menu.run()
            self.current_menu = None
            self.main_screen.active = True
        
        elif action == "friend":
            menu = FriendMenu(
                self.display, 
                self.buttons, 
                self.renderer, 
                self.chao
            )
            menu.run()
            self.current_menu = None
            self.main_screen.active = True
    
    def run(self):
        """Main game loop"""
        self.initialize()
        
        logger.info("Starting game loop")
        
        try:
            while self.running:
                if not self.powered_on:
                    time.sleep(0.1)
                    
                    # Check for power button
                    if self.buttons.is_pressed(Button.CENTER):
                        self.powered_on = True
                        self.display.show()
                        self.main_screen.active = True
                        logger.info("System powered on")
                    
                    continue
                
                # Update Chao behavior
                if self.current_menu is None:
                    self.update_decision()
                
                # Main screen update
                if self.main_screen.active:
                    action = self.main_screen.update()
                    
                    if action == "open_menu":
                        self.main_screen.active = False
                        menu = MainMenu(self.display, self.buttons, self.renderer)
                        result = menu.run()
                        
                        if result:
                            self.handle_menu_action(result)
                        else:
                            self.main_screen.active = True
                    
                    elif action == "toggle_power":
                        self.powered_on = False
                        self.display.hide()
                        self.save_manager.save(self.chao, self.inventory, self.background_index)
                        logger.info("System powered off")
                
                # Auto-save
                self.auto_save()
                
                time.sleep(0.05)
        
        except KeyboardInterrupt:
            logger.info("Shutting down...")
        
        finally:
            self.save_manager.save(self.chao, self.inventory, self.background_index)
            self.display.clear()
            logger.info("Game engine stopped")
