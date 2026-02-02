'''
This is the landing page.

Pretty title!
'''

from textual.screen import Screen
from textual.app import ComposeResult
from textual.widgets import Static

class LandingScreen(Screen): 
    
    def compose(self) -> ComposeResult:
        yield Static("Landing Screen", id="title")
        yield Static("Press s to continue", id="cont")