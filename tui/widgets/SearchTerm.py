from textual.widget import Widget
from textual.widgets import Static, Input, Select
from textual.app import ComposeResult
from textual.containers import HorizontalGroup

class SearchTerm(Widget):
    BORDER_TITLE = "Search Term" 

    def compose(self) -> ComposeResult: 
        with HorizontalGroup():  
            yield Select(options=((str(i), str(i)) for i in range(10)), classes='search-fields')
            yield Input(placeholder="enter search term here", classes='search-input')