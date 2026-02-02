'''
This is the search screen.

Users will create searches that will take them to search results screens.
'''

from textual.screen import Screen
from textual.app import ComposeResult
from textual.widgets import Static

class SearchScreen(Screen): 
    
    def compose(self) -> ComposeResult:
        yield Static(" Search Screen ", id="title")