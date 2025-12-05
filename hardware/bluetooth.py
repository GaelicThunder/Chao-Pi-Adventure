"""Bluetooth communication for Chao trading"""

import logging
import subprocess
from typing import List, Tuple, Optional
from config import BluetoothConfig

logger = logging.getLogger(__name__)


class BluetoothManager:
    """Manages Bluetooth connections for Chao trading"""
    
    def __init__(self, device_name: str):
        self.device_name = f"{BluetoothConfig.DEVICE_NAME} {device_name}"
        self.enabled = False
    
    def enable(self):
        """Enable Bluetooth"""
        try:
            subprocess.check_output('sudo rfkill unblock bluetooth', shell=True)
            subprocess.check_output(f"sudo hciconfig hci0 name '{self.device_name}'", shell=True)
            self.enabled = True
            logger.info(f"Bluetooth enabled as '{self.device_name}'")
        except subprocess.CalledProcessError as e:
            logger.error(f"Failed to enable Bluetooth: {e}")
            self.enabled = False
    
    def disable(self):
        """Disable Bluetooth"""
        try:
            subprocess.check_output('sudo rfkill block bluetooth', shell=True)
            self.enabled = False
            logger.info("Bluetooth disabled")
        except subprocess.CalledProcessError as e:
            logger.error(f"Failed to disable Bluetooth: {e}")
    
    def make_discoverable(self):
        """Make device discoverable"""
        try:
            subprocess.check_output('sudo hciconfig hci0 piscan', shell=True)
            logger.info("Device is now discoverable")
        except subprocess.CalledProcessError as e:
            logger.error(f"Failed to make discoverable: {e}")
    
    def scan_devices(self) -> List[Tuple[str, str]]:
        """Scan for nearby ChaoGotchi devices"""
        if not self.enabled:
            self.enable()
        
        try:
            import bluetooth
            
            logger.info("Scanning for devices...")
            nearby_devices = bluetooth.discover_devices()
            chao_devices = []
            
            for addr in nearby_devices:
                name = bluetooth.lookup_name(addr)
                if name and BluetoothConfig.DEVICE_NAME in name:
                    chao_devices.append((name, addr))
                    logger.info(f"Found ChaoGotchi: {name} [{addr}]")
            
            return chao_devices
            
        except ImportError:
            logger.error("pybluez not installed")
            return []
        except Exception as e:
            logger.error(f"Scan failed: {e}")
            return []
    
    def send_chao_data(self, address: str, data: str) -> bool:
        """Send Chao data to another device"""
        try:
            import bluetooth
            
            sock = bluetooth.BluetoothSocket(bluetooth.RFCOMM)
            sock.connect((address, BluetoothConfig.PORT))
            sock.send(data.encode('utf-8'))
            sock.close()
            
            logger.info(f"Sent Chao data to {address}")
            return True
            
        except ImportError:
            logger.error("pybluez not installed")
            return False
        except Exception as e:
            logger.error(f"Failed to send data: {e}")
            return False
    
    def wait_for_chao_data(self, timeout: int = 30) -> Optional[str]:
        """Wait for incoming Chao data"""
        try:
            import bluetooth
            
            server_sock = bluetooth.BluetoothSocket(bluetooth.RFCOMM)
            server_sock.bind(("", BluetoothConfig.PORT))
            server_sock.listen(1)
            server_sock.settimeout(timeout)
            
            logger.info("Waiting for connection...")
            client_sock, address = server_sock.accept()
            logger.info(f"Accepted connection from {address}")
            
            data = client_sock.recv(1024).decode('utf-8')
            
            client_sock.close()
            server_sock.close()
            
            return data
            
        except ImportError:
            logger.error("pybluez not installed")
            return None
        except bluetooth.btcommon.BluetoothError as e:
            logger.warning(f"Connection timeout or error: {e}")
            return None
        except Exception as e:
            logger.error(f"Failed to receive data: {e}")
            return None
    
    def serialize_chao(self, chao) -> str:
        """Serialize Chao object for transmission"""
        data = chao.to_dict()
        return f"{data['name']},{data['appearance']},{data['fly']},{data['run']},{data['swim']},{data['power']},{data['intelligence']},{data['luck']},{data['meters_walked']},{data['age']}"
    
    def deserialize_chao(self, data: str) -> dict:
        """Deserialize received Chao data"""
        parts = data.split(',')
        if len(parts) != 10:
            raise ValueError("Invalid Chao data format")
        
        return {
            'name': parts[0],
            'appearance': parts[1],
            'fly': float(parts[2]),
            'run': float(parts[3]),
            'swim': float(parts[4]),
            'power': float(parts[5]),
            'intelligence': float(parts[6]),
            'luck': float(parts[7]),
            'meters_walked': int(parts[8]),
            'age': float(parts[9])
        }
    
    def __del__(self):
        """Cleanup on deletion"""
        if self.enabled:
            self.disable()
