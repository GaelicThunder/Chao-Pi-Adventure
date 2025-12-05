# Changelog

All notable changes to Chao-Pi-Adventure will be documented in this file.

## [2.0.0] - 2024-12-05

### 🎉 Major Refactoring

#### Architecture
- **BREAKING**: Complete rewrite from monolithic to modular architecture
- **BREAKING**: Save format changed from pickle to JSON
- Split 3200-line file into 35+ focused modules
- Eliminated all global variables
- Implemented clean separation of concerns

#### Core Systems
- **Added**: `Chao` class with encapsulated stats and behavior
- **Added**: `Inventory` class for item management
- **Added**: `SaveManager` with JSON format and backup system
- **Improved**: Evolution system with better stat tracking
- **Improved**: Age and stamina mechanics

#### Hardware Layer
- **Added**: Abstract display interface supporting multiple types
- **Added**: `OLEDDisplay`, `WaveShareDisplay`, `NullDisplay` implementations
- **Added**: `ButtonHandler` with hardware debouncing
- **Added**: `BluetoothManager` for device communication
- **Added**: `BatteryMonitor` for UPS HAT support
- **Improved**: Error handling for missing hardware

#### UI System
- **Added**: `Renderer` class for sprite and animation handling
- **Added**: `BaseMenu` abstract class for consistent menu behavior
- **Added**: `MainScreen` with animation management
- **Added**: `MainMenu`, `InventoryMenu`, `ShopMenu`, `StatsMenu`
- **Improved**: Menu navigation consistency
- **Improved**: Visual feedback and rendering

#### Mini-Games
- **Added**: Complete race mini-game with 8 AI racers
- **Added**: Boost mechanics with stamina consumption
- **Added**: Race level progression and medal system
- **Added**: Casino slot machine with 4 symbols
- **Added**: Turn-based fight system
- **Added**: Unified games menu

#### Bluetooth & Social
- **Added**: Friend trading system
- **Added**: Scan for nearby devices
- **Added**: Wait for incoming Chao data
- **Added**: View saved friend Chao
- **Added**: Friend data persistence

### 🐛 Bug Fixes

- Fixed file existence check before size check
- Fixed race conditions in button polling
- Fixed display refresh logic
- Fixed save corruption with backup system
- Fixed Bluetooth cleanup on errors
- Fixed stamina overflow
- Fixed evolution trigger timing

### 📚 Documentation

- **Added**: Comprehensive README_NEW.md
- **Added**: Migration guide (MIGRATION.md)
- **Added**: Setup script (setup.py)
- **Added**: Pull request template
- **Added**: Complete docstrings for all modules
- **Improved**: Code comments and type hints

### 🧪 Testing

- **Added**: Unit tests for Chao class
- **Added**: Unit tests for Inventory
- **Added**: Unit tests for SaveManager
- **Added**: pytest configuration
- **Added**: Test requirements

### ⚡ Performance

- Optimized sprite caching
- Improved frame rate consistency
- Reduced memory allocations
- Lazy loading of resources

### 🔧 Configuration

- **Added**: Centralized config.py
- **Added**: Environment variable support
- **Added**: Display type configuration
- **Added**: Hardware pin mapping
- **Added**: Game parameter tuning

---

## [1.0.0] - 2020-12-01

### Initial Release

- Basic Chao virtual pet
- Evolution system
- Simple menus
- OLED display support
- Save/load with pickle
- Bluetooth framework
- Basic animations

---

### Migration Notes

#### v1.0 → v2.0

**Save Files**: Not compatible. See MIGRATION.md for manual migration.

**Configuration**: Update from inline variables to config.py.

**Imports**: Update to modular structure.

**API**: Replace global variable access with class methods.

---

### Versioning

This project uses [Semantic Versioning](https://semver.org/):
- **MAJOR**: Incompatible API changes
- **MINOR**: Backward-compatible functionality
- **PATCH**: Backward-compatible bug fixes
