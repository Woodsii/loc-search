'''
This will display the results of the search.
'''

from textual.screen import Screen
from textual.app import ComposeResult
from textual.widgets import Static, Button

class SearchResultsScreen(Screen):

    def compose(self) -> ComposeResult:
        yield Static("Search Results Screen", id="any-key")
        yield Button("Author", id='author')
        yield Button("Tag", id='tag')
        yield Button("Title", id='title')