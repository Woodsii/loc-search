from textual.screen import Screen
from textual.app import ComposeResult
from textual.widgets import Static

ERROR_TEXT = """
Library of Congress Search!!
"""

class LandingScreen(Screen): 
    
    def compose(self) -> ComposeResult:
        yield Static(" Windows ", id="title")
        yield Static(ERROR_TEXT)
        yield Static("Press any key to continue [blink]_[/]", id="any-key")