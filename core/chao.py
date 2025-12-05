"""Chao entity with stats, evolution, and behavior"""

import random
import logging
from typing import List, Tuple, Optional
from config import GameConfig, SpriteConfig

logger = logging.getLogger(__name__)


class Chao:
    """Represents a Chao with stats, evolution state, and behavior"""
    
    def __init__(self, name: str = "BansheeBoo"):
        self.name = name
        
        # Core stats
        self.fly = random.randint(0, 5)
        self.run = random.randint(0, 5)
        self.swim = random.randint(0, 5)
        self.power = random.randint(0, 5)
        self.intelligence = random.randint(0, 1)
        self.luck = random.randint(0, 1)
        
        # Alignment
        self.hero = 0
        self.dark = 0
        
        # State
        self.age = 0.0
        self.stamina = 100
        self.happiness = 100
        self.meters_walked = 0
        self.money = 0
        
        # Evolution
        self.appearance = "Normal.jpg"
        self.evolved = False
        
        # Medals
        self.run_medal = 1
        self.fly_medal = 1
        self.swim_medal = 1
        self.power_medal = 1
        
        # Behavior
        self.moods = [random.choice(GameConfig.MOODS) for _ in range(30)]
        self.current_decision = ""
    
    @property
    def total_stats(self) -> int:
        """Total stat points"""
        return int(self.fly + self.run + self.swim + self.power + self.intelligence + self.luck)
    
    def age_up(self, amount: float = 0.001):
        """Increase age and trigger evolution if needed"""
        self.age += amount
        if self.age >= 100 and not self.evolved:
            self.evolved = True
            self.evolve()
    
    def evolve(self):
        """Determine evolution based on stats and alignment"""
        logger.info(f"Evolution triggered - Fly:{self.fly} Run:{self.run} Swim:{self.swim} Power:{self.power}")
        
        # Chaos forms (extreme alignment)
        if self.dark > 200:
            self.appearance = "DevilChaos.jpg"
            logger.info("Evolved to Devil Chaos")
            return
        elif self.hero > 200:
            self.appearance = "HeroChaos.jpg"
            logger.info("Evolved to Hero Chaos")
            return
        elif self.hero > 200 and self.dark > 200:
            self.appearance = "Chaos.jpg"
            logger.info("Evolved to Chaos")
            return
        
        # Determine dominant stat
        stats = {
            'fly': self.fly,
            'run': self.run,
            'swim': self.swim,
            'power': self.power
        }
        dominant = max(stats, key=stats.get)
        
        # Apply alignment
        alignment = ""
        if self.hero > self.dark and self.hero > 50:
            alignment = "Hero"
        elif self.dark > self.hero and self.dark > 50:
            alignment = "Devil"
        
        # Build appearance string
        if alignment and dominant != 'normal':
            self.appearance = f"{alignment}{dominant.capitalize()}.jpg"
        elif dominant != 'normal':
            self.appearance = f"{dominant.capitalize()}.jpg"
        elif alignment:
            self.appearance = f"{alignment}.jpg"
        else:
            self.appearance = "Normal.jpg"
        
        logger.info(f"Evolved to {self.appearance}")
    
    def consume_item(self, item: str) -> bool:
        """Apply item effects and return success"""
        if item == "Run Fruit":
            self.run += 0.25
        elif item == "Fly Fruit":
            self.fly += 0.25
        elif item == "Swim Fruit":
            self.swim += 0.25
        elif item == "Power Fruit":
            self.power += 0.25
        elif item == "Hero Fruit":
            self.hero += 5
        elif item == "Dark Fruit":
            self.dark += 5
        elif item == "Chao Fruit":
            self.run += 0.25
            self.fly += 0.25
            self.swim += 0.25
            self.power += 0.25
        elif item == "Stamina Fruit":
            self.stamina = min(100, self.stamina + 5)
        else:
            return False
        return True
    
    def restore_stamina(self, amount: int = 5):
        """Restore stamina up to max"""
        self.stamina = min(100, self.stamina + amount)
    
    def use_stamina(self, amount: int = 1):
        """Use stamina for actions"""
        self.stamina = max(0, self.stamina - amount)
    
    def add_money(self, amount: int):
        """Add money"""
        self.money += amount
    
    def spend_money(self, amount: int) -> bool:
        """Spend money if available"""
        if self.money >= amount:
            self.money -= amount
            return True
        return False
    
    def to_dict(self) -> dict:
        """Serialize to dict for saving"""
        return {
            'name': self.name,
            'appearance': self.appearance,
            'fly': self.fly,
            'run': self.run,
            'swim': self.swim,
            'power': self.power,
            'intelligence': self.intelligence,
            'luck': self.luck,
            'hero': self.hero,
            'dark': self.dark,
            'age': self.age,
            'stamina': self.stamina,
            'happiness': self.happiness,
            'meters_walked': self.meters_walked,
            'money': self.money,
            'evolved': self.evolved,
            'run_medal': self.run_medal,
            'fly_medal': self.fly_medal,
            'swim_medal': self.swim_medal,
            'power_medal': self.power_medal,
            'moods': self.moods,
            'current_decision': self.current_decision
        }
    
    @classmethod
    def from_dict(cls, data: dict) -> 'Chao':
        """Deserialize from dict"""
        chao = cls(data['name'])
        chao.appearance = data['appearance']
        chao.fly = data['fly']
        chao.run = data['run']
        chao.swim = data['swim']
        chao.power = data['power']
        chao.intelligence = data['intelligence']
        chao.luck = data['luck']
        chao.hero = data['hero']
        chao.dark = data['dark']
        chao.age = data['age']
        chao.stamina = data['stamina']
        chao.happiness = data['happiness']
        chao.meters_walked = data['meters_walked']
        chao.money = data['money']
        chao.evolved = data['evolved']
        chao.run_medal = data['run_medal']
        chao.fly_medal = data['fly_medal']
        chao.swim_medal = data['swim_medal']
        chao.power_medal = data['power_medal']
        chao.moods = data['moods']
        chao.current_decision = data['current_decision']
        return chao
