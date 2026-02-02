from textual.app import App, ComposeResult
from textual.widgets import Button, Header, Label
from textual.screen import Screen

from screens.landing import LandingScreen
from screens.search import SearchScreen

class LoCBrowser(App):
    
    SCREENS = {"SearchScreen": SearchScreen}
    TITLE = "Library of Congress Browser"
    BINDINGS = [("s", "push_screen('SearchScreen')", "Search")]

    def compose(self) -> ComposeResult:
        yield Header()
        yield Button("Exit?", id="exit_button")

    def on_button_pressed(self, event: Button.Pressed) -> None:
        if event.button.id == 'exit_button':
            self.exit()
    
    def on_mount(self) -> None:
        self.push_screen(LandingScreen())


if __name__ == "__main__":
    app = LoCBrowser()
    app.run()