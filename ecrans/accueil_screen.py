from kivy.uix.widget import Widget
from kivy.uix.screenmanager import Screen



class AccueilWidget(Widget):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def on_simuler_pressed(self):
        self.parent.manager.current = "simulation"



class AccueilScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.accueil_widget = AccueilWidget()
        self.add_widget(self.accueil_widget)

