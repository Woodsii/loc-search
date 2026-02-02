'''
this will give in depth information about a work.
'''

from textual.screen import Screen
from textual.app import ComposeResult
from textual.widgets import Static

class WorkScreen(Screen): 
    
    def compose(self) -> ComposeResult:
        yield Static(" Work Page ", id="title")