"""Configuration file for Chao-Pi-Adventure"""

import os
from pathlib import Path

# Paths
BASE_DIR = Path(__file__).parent
SAVE_DIR = Path.home()
SAVE_FILE = SAVE_DIR / "Chao.save"
BACKUP_FILE = SAVE_DIR / "Chao.bak"
SPRITES_DIR = BASE_DIR / "SpritesJpeg"
FONTS_DIR = BASE_DIR / "fonts"

# Display configuration
class DisplayConfig:
    TYPE = os.getenv("DISPLAY_TYPE", "Oled")  # Oled, WaveShare, Noone
    WIDTH = 128
    HEIGHT = 64
    ANIMATION_TIME = 0.5 if TYPE != "WaveShare" else 1.0
    FULLSCREEN = False

# Hardware configuration
class HardwareConfig:
    BATTERY_ENABLED = False
    BATTERY_I2C_ADDRESS = 0x36
    BATTERY_I2C_BUS = 1
    
    # GPIO pins
    BUTTON_L = 27
    BUTTON_R = 23
    BUTTON_U = 17
    BUTTON_D = 22
    BUTTON_C = 4
    BUTTON_A = 5
    BUTTON_B = 6

# Game configuration
class GameConfig:
    VELOCITY_DEC = 15  # seconds between decisions
    SAVE_INTERVAL = 300  # seconds between auto-saves
    
    # Chao lists
    CHAO_TYPES = [
        "Normal.jpg", "Chaos.jpg", "Run.jpg", "Fly.jpg", "Power.jpg", "Swim.jpg",
        "Devil.jpg", "DevilChaos.jpg", "DevilRun.jpg", "DevilFly.jpg", "DevilPower.jpg", "DevilSwim.jpg",
        "Hero.jpg", "HeroChaos.jpg", "HeroRun.jpg", "HeroFly.jpg", "HeroPower.jpg", "HeroSwim.jpg"
    ]
    
    ITEM_LIST = [
        "Run Fruit", "Fly Fruit", "Swim Fruit", "Power Fruit", 
        "Hero Fruit", "Chao Fruit", "Dark Fruit"
    ]
    
    MOODS = [
        "Walk", "Walk", "Walk", "Walk", "Walk", "Walk",
        "Swim", "Fly", "Sleep", "Sad", "Tired", "Think", "Hello", "Draw"
    ]
    
    # Shop prices
    SHOP_PRICES = {
        "Swim Fruit": 50,
        "Fly Fruit": 50,
        "Run Fruit": 50,
        "Power Fruit": 50,
        "Dark Fruit": 50,
        "Hero Fruit": 50,
        "Chao Fruit": 100
    }

# Sprite configuration
class SpriteConfig:
    SPRITE_WIDTH = 25
    SPRITE_HEIGHT = 25
    BACKGROUND_WIDTH = 13
    BACKGROUND_HEIGHT = 26
    MAX_FRAMES = 4
    
    # Animation sequences
    WALK = [1, 0, 1, 2]
    SIT = [3, 4, 5, 4]
    CONFUSED = [6, 7, 6, 7]
    DRAWING = [6, 7, 6, 7]
    PUNCH_CHARGE = [0, 1, 2, 3]
    PUNCH = [0, 1, 0, 1]
    BALL_KICK = [4, 5, 2, 3]
    FALL = [4, 5, 6, 7]
    CRY = [0, 1, 2, 1]
    CRY_CYCLE = [2, 1, 2, 1]
    THINKING = [3, 4, 3, 4]
    SLEEP = [5, 6, 5, 6]
    CANT_SWIM = [7, 0, 7, 0]
    SWIMMING = [2, 3, 4, 3]
    PUNCH_MISS = [5, 6, 7, 7]
    EAT = [0, 1, 2, 3]
    EAT2 = [2, 3, 2, 3]
    FLY = [5, 6, 7, 6]
    SMH = [0, 1, 0, 1]
    LATERAL_WAIT = [4, 4, 6, 6]
    JUMP = [7, 0, 1, 0]
    HELLO_THERE = [2, 3, 2, 3]

# Bluetooth configuration
class BluetoothConfig:
    DEVICE_NAME = "ChaoGotchi"
    PORT = 1
    SCAN_TIMEOUT = 30
