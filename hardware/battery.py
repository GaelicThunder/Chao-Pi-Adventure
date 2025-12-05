"""Battery monitoring for UPS HAT"""

import logging
import struct
from typing import Optional
from config import HardwareConfig

logger = logging.getLogger(__name__)


class BatteryMonitor:
    """Monitor battery level via I2C"""
    
    def __init__(self):
        self.enabled = HardwareConfig.BATTERY_ENABLED
        self.bus = None
        
        if self.enabled:
            self._init_hardware()
    
    def _init_hardware(self):
        """Initialize I2C bus"""
        try:
            import smbus
            import RPi.GPIO as GPIO
            
            GPIO.setmode(GPIO.BCM)
            GPIO.setwarnings(False)
            GPIO.setup(HardwareConfig.BUTTON_C, GPIO.IN)
            
            self.bus = smbus.SMBus(HardwareConfig.BATTERY_I2C_BUS)
            self._power_on_reset()
            self._quick_start()
            
            logger.info("Battery monitor initialized")
            
        except Exception as e:
            logger.error(f"Failed to initialize battery monitor: {e}")
            self.enabled = False
    
    def _read_word(self, register: int) -> int:
        """Read word from I2C register"""
        if not self.enabled or not self.bus:
            return 0
        
        read = self.bus.read_word_data(HardwareConfig.BATTERY_I2C_ADDRESS, register)
        return struct.unpack("<H", struct.pack(">H", read))[0]
    
    def get_voltage(self) -> float:
        """Read battery voltage"""
        swapped = self._read_word(0x02)
        return swapped * 1.25 / 1000 / 16
    
    def get_capacity(self) -> int:
        """Read battery capacity percentage"""
        swapped = self._read_word(0x04)
        return int(swapped / 256)
    
    def _quick_start(self):
        """Quick start battery monitor"""
        if self.enabled and self.bus:
            self.bus.write_word_data(HardwareConfig.BATTERY_I2C_ADDRESS, 0x06, 0x4000)
    
    def _power_on_reset(self):
        """Reset battery monitor"""
        if self.enabled and self.bus:
            self.bus.write_word_data(HardwareConfig.BATTERY_I2C_ADDRESS, 0xfe, 0x0054)
