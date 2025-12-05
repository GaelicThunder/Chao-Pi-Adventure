"""Race mini-game implementation"""

import logging
import time
import random
from typing import List, Tuple, Optional
from PIL import Image, ImageDraw
from ui.base_menu import BaseMenu
from hardware.buttons import Button
from core.chao import Chao
from config import GameConfig, DisplayConfig

logger = logging.getLogger(__name__)


class RaceMenu(BaseMenu):
    """Race type selection menu"""
    
    def __init__(self, display, buttons, renderer, chao: Chao):
        super().__init__(display, buttons, renderer)
        self.chao = chao
        self.race_types = ["Run", "Fly", "Swim", "Power"]
    
    def render(self):
        """Render race type selection"""
        image = self.renderer.render_menu(
            self.race_types,
            self.selected_index
        )
        self.display.display(image)
    
    def handle_input(self) -> Optional[str]:
        """Handle race type selection"""
        if self.buttons.is_pressed(Button.LEFT):
            self.navigate_left(len(self.race_types))
        elif self.buttons.is_pressed(Button.RIGHT):
            self.navigate_right(len(self.race_types))
        elif self.buttons.is_pressed(Button.B):
            race_type = self.race_types[self.selected_index]
            self.deactivate()
            return race_type
        elif self.buttons.is_pressed(Button.A):
            self.deactivate()
            return "back"
        return None


class RaceLevelMenu(BaseMenu):
    """Race difficulty level selection"""
    
    def __init__(self, display, buttons, renderer, chao: Chao, race_type: str):
        super().__init__(display, buttons, renderer)
        self.chao = chao
        self.race_type = race_type
        
        # Determine max level based on medals
        self.max_level = self._get_max_level()
        self.levels = list(range(1, min(self.max_level + 1, 6)))  # 1-5 stars
    
    def _get_max_level(self) -> int:
        """Get maximum unlocked level"""
        if self.race_type == "Run":
            return self.chao.run_medal
        elif self.race_type == "Fly":
            return self.chao.fly_medal
        elif self.race_type == "Swim":
            return self.chao.swim_medal
        elif self.race_type == "Power":
            return self.chao.power_medal
        return 1
    
    def render(self):
        """Render level selection"""
        level_strings = ["*" * level for level in self.levels]
        image = self.renderer.render_menu(level_strings, self.selected_index)
        self.display.display(image)
    
    def handle_input(self) -> Optional[Tuple[str, int]]:
        """Handle level selection"""
        if self.buttons.is_pressed(Button.LEFT):
            self.navigate_left(len(self.levels))
        elif self.buttons.is_pressed(Button.RIGHT):
            self.navigate_right(len(self.levels))
        elif self.buttons.is_pressed(Button.B):
            level = self.levels[self.selected_index]
            self.deactivate()
            return ("start_race", level)
        elif self.buttons.is_pressed(Button.A):
            self.deactivate()
            return ("back", 0)
        return None


class Racer:
    """Represents a racer in the race"""
    
    def __init__(self, name: str, chao_type: str, fly: float, run: float, 
                 swim: float, power: float, intelligence: float, luck: float):
        self.name = name
        self.chao_type = chao_type
        self.fly = fly
        self.run = run
        self.swim = swim
        self.power = power
        self.intelligence = intelligence
        self.luck = luck
        
        self.position = 0.0
        self.stumble_counter = 0
        self.is_player = False
    
    def get_stat_for_race(self, race_type: str) -> float:
        """Get relevant stat for race type"""
        if race_type == "Run":
            return self.run
        elif race_type == "Fly":
            return self.fly
        elif race_type == "Swim":
            return self.swim
        elif race_type == "Power":
            return self.power
        return 0.0
    
    def update_position(self, race_type: str, race_length: int, boost: bool = False):
        """Update racer position"""
        # Check if stumbling
        if self.stumble_counter > 0:
            self.stumble_counter -= 1
            self.position += 0.001
            return
        
        # Random stumble chance (lower with intelligence)
        stumble_chance = max(12 - int(self.get_stat_for_race(race_type) / 100), 1)
        if random.randint(stumble_chance, 100) > 99:
            self.stumble_counter = random.randint(5, 15)
            return
        
        # Calculate speed
        base_speed = self.get_stat_for_race(race_type) / race_length + 1
        
        # Apply boost if player
        if self.is_player and boost:
            base_speed += 0.5
        
        self.position += base_speed


class RaceGame:
    """Main race game implementation"""
    
    def __init__(self, display, buttons, renderer, chao: Chao, 
                 race_type: str, level: int):
        self.display = display
        self.buttons = buttons
        self.renderer = renderer
        self.chao = chao
        self.race_type = race_type
        self.level = level
        
        self.race_length = random.randint(100 * level, 150 * level)
        self.racers: List[Racer] = []
        self.finished_positions: List[int] = []
        self.boost_active = False
        self.stamina = chao.stamina
        self.max_stamina = chao.stamina
        self.boost_cooldown = 0
        
        self._generate_racers()
    
    def _generate_racers(self):
        """Generate AI racers"""
        # Player racer
        player = Racer(
            self.chao.name,
            self.chao.appearance,
            self.chao.fly,
            self.chao.run,
            self.chao.swim,
            self.chao.power,
            self.chao.intelligence,
            self.chao.luck
        )
        player.is_player = True
        self.racers.append(player)
        
        # Generate 7 AI racers
        total_stats = int(self.chao.fly + self.chao.run + self.chao.swim + 
                         self.chao.power + self.chao.intelligence + self.chao.luck)
        
        chao_names = [
            "Speedy", "Thunder", "Shadow", "Cosmos", "Blaze", "Aqua", "Storm"
        ]
        chao_types = [
            "Normal.jpg", "Run.jpg", "Fly.jpg", "Swim.jpg", "Power.jpg",
            "Hero.jpg", "Devil.jpg"
        ]
        
        for i in range(7):
            # Distribute stats randomly
            remaining_stats = random.randint(total_stats - 5, total_stats + 5)
            stats = {'fly': 0, 'run': 0, 'swim': 0, 'power': 0, 'intel': 0, 'luck': 0}
            
            for _ in range(remaining_stats):
                stat = random.choice(list(stats.keys()))
                stats[stat] += 1
            
            # Determine chao type based on dominant stat
            dominant = max(stats, key=lambda k: stats[k] if k in ['fly', 'run', 'swim', 'power'] else 0)
            if dominant == 'fly':
                chao_type = "Fly.jpg"
            elif dominant == 'run':
                chao_type = "Run.jpg"
            elif dominant == 'swim':
                chao_type = "Swim.jpg"
            elif dominant == 'power':
                chao_type = "Power.jpg"
            else:
                chao_type = random.choice(chao_types)
            
            racer = Racer(
                chao_names[i],
                chao_type,
                stats['fly'],
                stats['run'],
                stats['swim'],
                stats['power'],
                stats['intel'],
                stats['luck']
            )
            self.racers.append(racer)
    
    def run(self) -> Optional[int]:
        """Run the race, return finish position (1-8)"""
        logger.info(f"Starting {self.race_type} race, level {self.level}")
        
        current_racer_view = 0  # Which racer we're viewing
        
        while len(self.finished_positions) < len(self.racers):
            # Handle input
            if self.buttons.is_pressed(Button.LEFT):
                current_racer_view = max(0, current_racer_view - 1)
            elif self.buttons.is_pressed(Button.RIGHT):
                current_racer_view = min(len(self.racers) - 1, current_racer_view + 1)
            elif self.buttons.is_pressed(Button.B):
                # Boost
                if self.max_stamina > 0 and not self.boost_active and self.boost_cooldown == 0:
                    self.max_stamina -= 5
                    self.boost_active = True
                    self.boost_cooldown = 8
            
            # Update boost state
            if self.boost_active:
                if self.boost_cooldown > 0:
                    self.boost_cooldown -= 1
                else:
                    self.boost_active = False
                    self.boost_cooldown = 8
            
            # Update all racers
            for i, racer in enumerate(self.racers):
                if i not in self.finished_positions:
                    racer.update_position(
                        self.race_type, 
                        self.race_length,
                        boost=self.boost_active if racer.is_player else False
                    )
                    
                    # Check if finished
                    if racer.position >= self.race_length:
                        self.finished_positions.append(i)
                        logger.info(f"{racer.name} finished in position {len(self.finished_positions)}")
            
            # Render race
            self._render_race(current_racer_view)
            time.sleep(0.05)
        
        # Find player position
        player_position = self.finished_positions.index(0) + 1
        
        # Update stamina
        self.chao.stamina = max(0, self.max_stamina)
        
        return player_position
    
    def _render_race(self, viewed_racer: int):
        """Render race scene"""
        canvas = Image.new("L", (DisplayConfig.WIDTH, DisplayConfig.HEIGHT), "white")
        draw = ImageDraw.Draw(canvas)
        
        # Draw track
        draw.line([(2, DisplayConfig.HEIGHT - 3), 
                  (DisplayConfig.WIDTH - 3, DisplayConfig.HEIGHT - 3)], 
                 fill="black", width=2)
        
        # Draw racers as circles
        for i, racer in enumerate(self.racers):
            if i not in self.finished_positions:
                # Calculate screen position
                progress = racer.position / self.race_length
                x = int(2 + progress * (DisplayConfig.WIDTH - 6))
                y = DisplayConfig.HEIGHT - 10
                
                # Draw racer
                if i == viewed_racer:
                    # Highlighted racer (filled)
                    draw.ellipse([(x-3, y-3), (x+3, y+3)], fill="black", outline="black")
                    # Draw stumble indicator
                    if racer.stumble_counter > 0:
                        draw.ellipse([(x-2, y-5), (x+2, y-1)], fill="white", outline="black")
                else:
                    # Other racers (outline only)
                    draw.ellipse([(x-3, y-3), (x+3, y+3)], fill="white", outline="black")
        
        # Draw racer name
        font = self.renderer.load_font("C&C Red Alert [INET].ttf", 12)
        racer_name = self.racers[viewed_racer].name
        draw.text((DisplayConfig.WIDTH - 48, 5), racer_name, font=font, fill="black")
        
        # Draw stamina bar if player
        if self.racers[viewed_racer].is_player and self.max_stamina > 0:
            stamina_width = int((self.max_stamina / 135) * 40)
            if stamina_width > 0:
                draw.line([(4, 20), (4 + stamina_width, 20)], fill="black", width=2)
            draw.text((2, 5), "Stamina", font=font, fill="black")
        
        self.display.display(canvas)


class RaceResultScreen:
    """Display race results"""
    
    def __init__(self, display, buttons, renderer, chao: Chao, 
                 race_type: str, level: int, position: int):
        self.display = display
        self.buttons = buttons
        self.renderer = renderer
        self.chao = chao
        self.race_type = race_type
        self.level = level
        self.position = position
    
    def show(self):
        """Show results and handle rewards"""
        # Determine result message and reward
        if self.position == 1:
            message = "FIRST PLACE!"
            reward = 5 * self.level
            
            # Unlock next level
            if self.race_type == "Run" and self.chao.run_medal == self.level:
                self.chao.run_medal += 1
            elif self.race_type == "Fly" and self.chao.fly_medal == self.level:
                self.chao.fly_medal += 1
            elif self.race_type == "Swim" and self.chao.swim_medal == self.level:
                self.chao.swim_medal += 1
            elif self.race_type == "Power" and self.chao.power_medal == self.level:
                self.chao.power_medal += 1
        
        elif self.position == 2:
            message = "SECOND PLACE"
            reward = 3 * self.level
        elif self.position == 3:
            message = "THIRD PLACE"
            reward = 2 * self.level
        else:
            message = "TOO BAD..."
            reward = 1
        
        # Give reward
        self.chao.add_money(reward)
        
        # Display result
        additional = [(f"+¥{reward}", (DisplayConfig.WIDTH // 2 - 15, DisplayConfig.HEIGHT - 15), 12)]
        image = self.renderer.render_text_screen(message, 24, additional)
        self.display.display(image)
        
        # Wait for input
        time.sleep(2)
        while True:
            if self.buttons.is_pressed(Button.A) or self.buttons.is_pressed(Button.B):
                break
            time.sleep(0.1)
        
        logger.info(f"Race finished: Position {self.position}, Reward ¥{reward}")
