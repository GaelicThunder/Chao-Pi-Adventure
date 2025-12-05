"""Games menu with mini-game selection"""

import logging
from typing import Optional
from ui.base_menu import BaseMenu
from hardware.buttons import Button
from core.chao import Chao
from ui.screens.games.race import RaceMenu, RaceLevelMenu, RaceGame, RaceResultScreen
from ui.screens.games.casino import CasinoGame
from ui.screens.games.fight import FightGame

logger = logging.getLogger(__name__)


class GamesMenu(BaseMenu):
    """Main games menu"""
    
    def __init__(self, display, buttons, renderer, chao: Chao):
        super().__init__(display, buttons, renderer)
        self.chao = chao
        self.games = ["Race", "Casino", "Fight"]
    
    def render(self):
        """Render games menu"""
        image = self.renderer.render_menu(
            self.games,
            self.selected_index,
            money=self.chao.money
        )
        self.display.display(image)
    
    def handle_input(self) -> Optional[str]:
        """Handle game selection"""
        if self.buttons.is_pressed(Button.LEFT):
            self.navigate_left(len(self.games))
        elif self.buttons.is_pressed(Button.RIGHT):
            self.navigate_right(len(self.games))
        elif self.buttons.is_pressed(Button.B):
            game = self.games[self.selected_index].lower()
            self.deactivate()
            return game
        elif self.buttons.is_pressed(Button.A):
            self.deactivate()
            return "back"
        return None
    
    def run(self) -> Optional[str]:
        """Run games menu with sub-game handling"""
        self.activate()
        
        while self.active:
            self.render()
            action = self.handle_input()
            
            if action == "back":
                return "back"
            
            elif action == "race":
                self._run_race_game()
            
            elif action == "casino":
                if self.chao.money > 0:
                    self._run_casino_game()
                else:
                    # Show "no money" message
                    img = self.renderer.render_text_screen("NO MONEY!", 20)
                    self.display.display(img)
                    import time
                    time.sleep(1.5)
            
            elif action == "fight":
                self._run_fight_game()
        
        return None
    
    def _run_race_game(self):
        """Run complete race game flow"""
        # Select race type
        race_menu = RaceMenu(self.display, self.buttons, self.renderer, self.chao)
        race_type = race_menu.run()
        
        if race_type == "back" or not race_type:
            return
        
        # Select difficulty level
        level_menu = RaceLevelMenu(self.display, self.buttons, self.renderer, 
                                   self.chao, race_type)
        result = level_menu.run()
        
        if not result or result[0] == "back":
            return
        
        action, level = result
        
        # Run the race
        race = RaceGame(self.display, self.buttons, self.renderer, 
                       self.chao, race_type, level)
        position = race.run()
        
        # Show results
        results = RaceResultScreen(self.display, self.buttons, self.renderer,
                                   self.chao, race_type, level, position)
        results.show()
    
    def _run_casino_game(self):
        """Run casino slot machine"""
        casino = CasinoGame(self.display, self.buttons, self.renderer, self.chao)
        casino.run()
    
    def _run_fight_game(self):
        """Run fight mini-game"""
        fight = FightGame(self.display, self.buttons, self.renderer, self.chao)
        fight.run()
