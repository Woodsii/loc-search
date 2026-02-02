'''
This is a screen for displaying a group of books.

Groups can be genres, tags or any other piece of metadata that describes a set of works. 
'''


from textual.screen import Screen
from textual.app import ComposeResult
from textual.widgets import Static, Button

class GroupScreen(Screen): 
    
    def compose(self) -> ComposeResult:
        yield Static("Group Screen ", id="title")