'''
This is the author screen.

It displays information about an author.
'''

from textual.screen import Screen
from textual.app import ComposeResult
from textual.widgets import Static

class AuthorScreen(Screen): 
    
    def compose(self) -> ComposeResult:
        yield Static(" Work Page ", id="title")