'''
This will display the results of the search.
'''

from textual.screen import Screen
from textual.app import ComposeResult
from textual.widgets import Static

class SearchResultsScreen(Screen):

    def compose(self) -> ComposeResult:
        yield Static("Search Results Screen", id="any-key")