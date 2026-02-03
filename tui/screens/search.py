'''
This is the search screen.

Users will create searches that will take them to search results screens.
'''
from textual import on
from textual.screen import Screen
from textual.app import ComposeResult
from textual.widgets import Button
from textual.containers import VerticalScroll, HorizontalGroup, Vertical

from widgets.SearchTerm import SearchTerm

class SearchScreen(Screen): 
    
    def compose(self) -> ComposeResult:
        with VerticalScroll(id='screen-search'):
            with Vertical(id='search-terms'):
                yield SearchTerm()
            with HorizontalGroup(id='button-bar'):
                yield Button("Start Search", id="start-search") # should take us to a modal loading screen that will fade out when search is done.
                yield Button("Add Search", id="add-search") 
    
    # creates a new search field for the user.
    # Essentially an AND
    @on(Button.Pressed, "#add-search")
    def action_add_search(self):
        sfield = SearchTerm()
        container = self.query_one('#search-terms')
        container.mount(sfield)

    
