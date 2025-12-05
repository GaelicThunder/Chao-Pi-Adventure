# Chao-Pi-Adventure v2.0

A Tamagotchi-like game based on the "Chao Adventure" VMU for Dreamcast, refactored with modern architecture.

## Features

- **Virtual Pet Care**: Raise and evolve your Chao based on care and stats
- **Multiple Evolution Paths**: Hero, Dark, Chaos, and specialized evolutions
- **Mini-Games**: Races, casino, and more
- **Trading**: Bluetooth Chao trading between devices
- **Multiple Display Support**: OLED (SSD1306), WaveShare e-paper, or headless

## Architecture

### Modular Design

The refactored codebase uses a clean modular architecture:

```
chao-pi-adventure/
├── config.py              # Configuration
├── main.py               # Entry point
├── core/                 # Core game logic
│   ├── chao.py          # Chao entity
│   ├── inventory.py     # Inventory system
│   └── save_manager.py  # Save/load
├── hardware/            # Hardware abstraction
│   ├── display.py       # Display drivers
│   ├── buttons.py       # Button input
│   ├── bluetooth.py     # BT communication
│   └── battery.py       # Battery monitoring
├── ui/                  # User interface
│   ├── renderer.py      # Sprite rendering
│   ├── base_menu.py     # Menu base class
│   └── screens/         # UI screens
│       ├── main_screen.py
│       ├── main_menu.py
│       ├── inventory_menu.py
│       ├── shop_menu.py
│       └── stats_menu.py
└── engine/              # Game engine
    └── game_engine.py   # Main game loop
```

### Key Improvements

1. **Separation of Concerns**: Hardware, UI, and logic are decoupled
2. **Testability**: Each module can be tested independently
3. **Maintainability**: Clear responsibilities and interfaces
4. **Extensibility**: Easy to add new features and displays
5. **Error Handling**: Proper exception handling and logging
6. **JSON Saves**: Human-readable save format (vs pickle)

## Installation

### Requirements

- Python 3.7+
- Raspberry Pi (or compatible)
- OLED/E-paper display (optional)
- GPIO buttons

### Setup

```bash
# Clone repository
git clone https://github.com/GaelicThunder/Chao-Pi-Adventure.git
cd Chao-Pi-Adventure

# Install dependencies
pip3 install -r requirements.txt

# Run game
python3 main.py
```

### Configuration

Edit `config.py` to customize:

- Display type (Oled, WaveShare, Noone)
- GPIO pin mappings
- Game parameters
- Battery monitoring

Or use environment variables:

```bash
export DISPLAY_TYPE=Oled
python3 main.py
```

## Hardware Setup

### Buttons

| Button | GPIO Pin | Function |
|--------|----------|----------|
| Left   | 27       | Navigate left |
| Right  | 23       | Navigate right |
| Up     | 17       | Navigate up / Brightness+ |
| Down   | 22       | Navigate down / Brightness- |
| Center | 4        | Power on/off |
| A      | 5        | Back/Cancel |
| B      | 6        | Select/Confirm |

### Display

#### OLED (SSD1306)
- Connect via I2C (SDA, SCL)
- 128x64 resolution
- Requires `luma.oled` library

#### WaveShare e-Paper
- Connect via SPI
- Slower refresh, lower power
- Requires WaveShare library

## Usage

### Main Screen
- Watch your Chao roam and interact with environment
- Press **B** to open menu
- Press **Center** to power off

### Menu Options
- **Games**: Mini-games (races, casino)
- **Shop**: Buy fruits and items
- **Stats**: View Chao statistics
- **Friend**: Bluetooth trading
- **Inventory**: Use items on your Chao

### Evolution

Your Chao evolves at age 100 based on:
- **Dominant Stat**: Fly, Run, Swim, or Power
- **Alignment**: Hero (positive actions) or Dark (negative actions)
- **Special Forms**: Chaos evolutions with extreme alignment

## Development

### Running Tests

```bash
python3 -m pytest tests/
```

### Adding New Features

1. **New Menu**: Extend `BaseMenu` in `ui/screens/`
2. **New Display**: Implement `BaseDisplay` in `hardware/display.py`
3. **New Animation**: Add to `SpriteConfig` in `config.py`

### Migration from v1.0

The old monolithic `ChaoGotchi.py` has been completely refactored. To migrate:

1. Old pickle saves are **not compatible**
2. Start a new game or manually recreate your Chao
3. JSON save format is now human-editable

## Troubleshooting

### Display Not Working
- Check `config.py` display type setting
- Verify I2C/SPI connections
- Run in headless mode (`DISPLAY_TYPE=Noone`) for testing

### Buttons Not Responding
- Check GPIO pin configuration
- Verify pull-up resistors
- Check logs for hardware init errors

### Import Errors
- Ensure all dependencies installed: `pip3 install -r requirements.txt`
- Some hardware libs only work on ARM (Raspberry Pi)

## Credits

- Original concept: Sonic Team (Chao Adventure VMU)
- Original implementation: GaelicThunder
- Refactoring: v2.0 modular architecture

## License

MIT License - See original README for details
