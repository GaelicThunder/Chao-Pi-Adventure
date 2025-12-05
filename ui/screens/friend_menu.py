"""Friend/Bluetooth trading menu"""

import logging
import time
import pickle
from pathlib import Path
from typing import Optional, List, Tuple
from ui.base_menu import BaseMenu
from hardware.buttons import Button
from hardware.bluetooth import BluetoothManager
from core.chao import Chao
from config import SAVE_DIR

logger = logging.getLogger(__name__)


class FriendMenu(BaseMenu):
    """Bluetooth friend trading menu"""
    
    def __init__(self, display, buttons, renderer, chao: Chao):
        super().__init__(display, buttons, renderer)
        self.chao = chao
        self.bluetooth = BluetoothManager(chao.name)
        self.options = ["Scan for Friends", "Wait for Friends", "View Friends"]
        self.friends: List[str] = []
        self._load_friends()
    
    def _load_friends(self):
        """Load saved friend Chao files"""
        try:
            friend_files = list(SAVE_DIR.glob("*.chao"))
            self.friends = [f.stem for f in friend_files]
            logger.info(f"Loaded {len(self.friends)} friends")
        except Exception as e:
            logger.error(f"Failed to load friends: {e}")
    
    def render(self):
        """Render friend menu"""
        display_options = self.options.copy()
        if self.friends:
            display_options[2] = f"View Friends ({len(self.friends)})"
        
        image = self.renderer.render_menu(display_options, self.selected_index)
        self.display.display(image)
    
    def handle_input(self) -> Optional[str]:
        """Handle friend menu input"""
        if self.buttons.is_pressed(Button.UP):
            self.navigate_up(len(self.options) - 1)
        elif self.buttons.is_pressed(Button.DOWN):
            self.navigate_down(len(self.options) - 1)
        elif self.buttons.is_pressed(Button.B):
            action = self.options[self.selected_index]
            if "Scan" in action:
                return "scan"
            elif "Wait" in action:
                return "wait"
            elif "View" in action:
                return "view"
        elif self.buttons.is_pressed(Button.A):
            self.deactivate()
            return "back"
        return None
    
    def run(self) -> Optional[str]:
        """Run friend menu with Bluetooth operations"""
        self.activate()
        
        while self.active:
            self.render()
            action = self.handle_input()
            
            if action == "back":
                return "back"
            
            elif action == "scan":
                self._scan_for_friends()
            
            elif action == "wait":
                self._wait_for_friend()
            
            elif action == "view":
                self._view_friends()
        
        return None
    
    def _scan_for_friends(self):
        """Scan for nearby ChaoGotchi devices"""
        # Show scanning message
        img = self.renderer.render_text_screen("Scanning...", 16)
        self.display.display(img)
        
        # Scan for devices
        devices = self.bluetooth.scan_devices()
        
        if not devices:
            img = self.renderer.render_text_screen("No devices found", 16)
            self.display.display(img)
            time.sleep(2)
            return
        
        # Show found device
        device_name, device_addr = devices[0]
        img = self.renderer.render_text_screen(f"Found:\n{device_name}", 12)
        self.display.display(img)
        time.sleep(1)
        
        # Send Chao data
        img = self.renderer.render_text_screen("Sending...", 16)
        self.display.display(img)
        
        chao_data = self.bluetooth.serialize_chao(self.chao)
        success = self.bluetooth.send_chao_data(device_addr, chao_data)
        
        if success:
            img = self.renderer.render_text_screen("Sent!", 20)
        else:
            img = self.renderer.render_text_screen("Failed", 20)
        
        self.display.display(img)
        time.sleep(2)
        
        # Cleanup
        self.bluetooth.disable()
    
    def _wait_for_friend(self):
        """Wait for incoming Chao data"""
        # Show waiting message
        img = self.renderer.render_text_screen("Waiting...", 16)
        self.display.display(img)
        
        # Enable Bluetooth and wait
        self.bluetooth.enable()
        self.bluetooth.make_discoverable()
        
        # Wait for data (with timeout)
        data = self.bluetooth.wait_for_chao_data(timeout=30)
        
        if data:
            # Parse and save received Chao
            try:
                friend_data = self.bluetooth.deserialize_chao(data)
                self._save_friend(friend_data)
                
                img = self.renderer.render_text_screen(
                    f"Received!\n{friend_data['name']}", 12
                )
                self.display.display(img)
                time.sleep(2)
                
                # Reload friends list
                self._load_friends()
            
            except Exception as e:
                logger.error(f"Failed to save friend: {e}")
                img = self.renderer.render_text_screen("Error", 20)
                self.display.display(img)
                time.sleep(2)
        else:
            img = self.renderer.render_text_screen("Timeout", 20)
            self.display.display(img)
            time.sleep(2)
        
        # Cleanup
        self.bluetooth.disable()
    
    def _save_friend(self, friend_data: dict):
        """Save received friend Chao"""
        filename = SAVE_DIR / f"{friend_data['name']}.chao"
        
        with open(filename, 'wb') as f:
            pickle.dump(friend_data, f)
        
        logger.info(f"Saved friend: {friend_data['name']}")
    
    def _view_friends(self):
        """View saved friend Chao"""
        if not self.friends:
            img = self.renderer.render_text_screen("No friends yet", 14)
            self.display.display(img)
            time.sleep(2)
            return
        
        # Browse through friends
        index = 0
        
        while True:
            friend_name = self.friends[index]
            
            # Load friend data
            try:
                filename = SAVE_DIR / f"{friend_name}.chao"
                with open(filename, 'rb') as f:
                    friend_data = pickle.load(f)
                
                # Display friend info
                info_text = (
                    f"{friend_data['name']}\n"
                    f"Age: {int(friend_data['age'])}\n"
                    f"Stats: {int(friend_data.get('fly', 0))} "
                    f"{int(friend_data.get('run', 0))} "
                    f"{int(friend_data.get('swim', 0))} "
                    f"{int(friend_data.get('power', 0))}"
                )
                
                img = self.renderer.render_text_screen(info_text, 10)
                self.display.display(img)
            
            except Exception as e:
                logger.error(f"Failed to load friend {friend_name}: {e}")
                img = self.renderer.render_text_screen("Error loading", 14)
                self.display.display(img)
            
            # Handle navigation
            if self.buttons.is_pressed(Button.LEFT):
                index = (index - 1) % len(self.friends)
                time.sleep(0.2)
            elif self.buttons.is_pressed(Button.RIGHT):
                index = (index + 1) % len(self.friends)
                time.sleep(0.2)
            elif self.buttons.is_pressed(Button.A) or self.buttons.is_pressed(Button.B):
                break
