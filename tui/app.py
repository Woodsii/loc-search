from textual.app import App, ComposeResult
from textual.widgets import Button, Header, Label
from textual.screen import Screen

from screens.landing import LandingScreen
from screens.search import SearchScreen
from screens.searchResults import SearchResultsScreen
from screens.author import AuthorScreen
from screens.group import GroupScreen
from screens.work import WorkScreen

# my idea currently is to just handle routing here, on the app level.
class LoCBrowser(App):
    
    SCREENS = {"SearchScreen": SearchScreen}
    TITLE = "Library of Congress Browser"
    BINDINGS = [
        ("s", "switch_screen('SearchScreen')", "Search"),
        ("b", "pop_screen()", "Go-Back")
        ]

    def compose(self) -> ComposeResult:
        yield Header()

    def on_button_pressed(self, event: Button.Pressed) -> None:        
        if event.button.id == "start-search": 
            self.push_screen(SearchResultsScreen())
        elif event.button.id == "author": 
            self.push_screen(AuthorScreen()) 
        elif event.button.id == "tag": 
            self.push_screen(GroupScreen())   
        elif event.button.id == "title": 
            self.push_screen(WorkScreen())
    
    def on_mount(self) -> None:
        self.push_screen(LandingScreen())


if __name__ == "__main__":
    app = LoCBrowser()
    app.run()