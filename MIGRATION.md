# Migration Guide: v1.0 to v2.0

## Overview

Chao-Pi-Adventure v2.0 is a complete refactoring of the original monolithic codebase into a modular, maintainable architecture.

## Breaking Changes

### Save File Format

**Old**: Pickle-based binary format (`Chao.save`)
**New**: JSON-based text format (`Chao.save`)

**Action Required**: Old saves are **not compatible**. You must start a new game or manually migrate.

### Manual Migration

If you want to preserve your old Chao:

1. Load old save in Python:
```python
import pickle
with open('Chao.save.old', 'rb') as f:
    old_data = pickle.load(f)
    # Extract all pickled data...
```

2. Create new save manually by editing `Chao.save` JSON:
```json
{
  "chao": {
    "name": "YourChaoName",
    "appearance": "Normal.jpg",
    "fly": 10,
    "run": 12,
    ...
  },
  "inventory": ["Run Fruit", "Fly Fruit"],
  "background_index": 0,
  "version": "2.0"
}
```

### Configuration

**Old**: Hardcoded variables at top of `ChaoGotchi.py`
**New**: Centralized `config.py` with classes

**Migration**:
```python
# Old
display = 'Oled'
Battery = False
Name = "BansheeBoo"

# New (config.py)
class DisplayConfig:
    TYPE = "Oled"
class HardwareConfig:
    BATTERY_ENABLED = False
# Name now part of Chao object
```

### Import Changes

**Old**: Everything in one file
**New**: Modular imports

```python
# Old
from ChaoGotchi import *

# New
from core.chao import Chao
from core.inventory import Inventory
from hardware.display import get_display
from engine.game_engine import GameEngine
```

## Feature Parity

### Implemented ✅

- [x] Main screen with Chao animations
- [x] Menu system (inventory, shop, stats)
- [x] Evolution system
- [x] Save/load functionality
- [x] Bluetooth framework
- [x] Battery monitoring
- [x] Multiple display support

### Partially Implemented ⚠️

- [ ] **Race mini-game**: Framework ready, needs full implementation
- [ ] **Casino game**: Slot machine logic needs porting
- [ ] **Fight game**: Placeholder only
- [ ] **Bluetooth trading**: Core ready, UI needs completion

### Architecture Changes 🏗️

#### Old Architecture
```
ChaoGotchi.py (3200 lines)
├── Hardcoded config
├── Global variables
├── Hardware init
├── Button polling
├── Menu functions
├── Game logic
└── Main loop
```

#### New Architecture
```
Modular structure
├── config.py         # All configuration
├── core/            # Game logic
├── hardware/        # Hardware abstraction
├── ui/              # User interface
└── engine/          # Game engine
```

## API Changes

### Chao Object

```python
# Old (global variables)
Fly = 10
Run = 12
Swim = 8
Power = 15

# New (Chao class)
chao = Chao()
chao.fly = 10
chao.run = 12
chao.swim = 8
chao.power = 15
```

### Inventory

```python
# Old (global list)
Inv = ["Run Fruit", "Fly Fruit"]
Inv.append("Swim Fruit")

# New (Inventory class)
inventory = Inventory()
inventory.add_item("Swim Fruit")
count = inventory.get_count("Run Fruit")
```

### Display

```python
# Old (direct device access)
device.display(background.convert(device.mode))

# New (abstracted)
display = get_display()  # Auto-detects type
display.display(image)
```

### Buttons

```python
# Old (direct GPIO)
if not button_B.value:
    # Do something

# New (ButtonHandler)
if buttons.is_pressed(Button.B):
    # Do something
```

## Testing Strategy

### Old Code
- Difficult to test (hardware dependencies)
- No separation of concerns
- Manual testing only

### New Code
```python
# Mock hardware for testing
from hardware.display import NullDisplay
from hardware.buttons import ButtonHandler

display = NullDisplay()  # No real hardware
buttons = ButtonHandler(use_hardware=False)
```

## Performance Considerations

- **Save/Load**: JSON is ~10% slower than pickle, but human-readable
- **Display**: No performance impact, abstraction is thin
- **Memory**: Slightly higher due to class overhead (~5%)

## Troubleshooting

### "Module not found"
- Ensure you're in the project root
- Check Python path includes project directory

### "Old save not loading"
- Expected behavior - format incompatible
- Use manual migration or start fresh

### "Display not initializing"
- Check `config.py` display type
- Verify hardware connections
- Try headless mode for debugging

## Rollback

If you need to revert to v1.0:

```bash
git checkout main
python3 ChaoGotchi.py
```

Your old save files will still work with v1.0.

## Getting Help

- Check logs: `chao.log`
- Review module documentation
- Open GitHub issue with logs and config
