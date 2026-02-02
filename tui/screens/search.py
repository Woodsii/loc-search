from textual.screen import Screen
from textual.app import ComposeResult
from textual.widgets import Static

class SearchScreen(Screen): 
    
    def compose(self) -> ComposeResult:
        yield Static(" Search ", id="title")
        yield Static(" Whats good homeslice ", id="any-key")