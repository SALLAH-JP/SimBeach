from variables.config_manager import *
from kivy.app import App
from kivy.uix.widget import Widget
from kivy.uix.screenmanager import Screen
from kivy.uix.video import Video
from kivy.uix.popup import Popup
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.boxlayout import BoxLayout


class AccueilWidget(Widget):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def on_simuler_pressed(self):
        """Vérifie si un robot est connecté et ouvre un Popup si aucun n'est trouvé."""
        config = load_config()

        if not config["robot_connect"]: self.afficher_popup()

        else: self.parent.manager.current = "simulation"


    def afficher_popup(self):
        """Affiche un Popup pour avertir l'utilisateur et lui proposer de jouer."""

        box = BoxLayout(orientation="vertical", spacing=10, padding=10)
        box2 = BoxLayout(orientation="horizontal", spacing=10, padding=5)
        label = Label(text="Aucun robot n'est connecté.\nVoulez-vous lancer la simulation ?")
        spacer1 = Widget(size_hint_x=1)
        spacer2 = Widget(size_hint_x=1)
        spacer3 = Widget(size_hint_x=1)

        # Boutons pour le choix de l'utilisateur
        btn_oui = Button(text="Oui")
        btn_non = Button(text="Non")  # Rouge
        
        # Ajouter les boutons au layout vertical
        box.add_widget(label)
        box2.add_widget(spacer1)
        box2.add_widget(btn_oui)
        box2.add_widget(spacer2)
        box2.add_widget(btn_non)
        box2.add_widget(spacer3)
        box.add_widget(box2)

        # Configuration du popup
        popup = Popup(title="Attention", content=box, size_hint=(0.4, 0.3), auto_dismiss=False)
        
        # Liens des boutons
        btn_oui.bind(on_release=lambda x: self.jouer_mode_simulation(popup))
        btn_non.bind(on_release=lambda x: popup.dismiss())
        
        # Affiche le popup
        popup.open()

    def jouer_mode_simulation(self, popup):
        """Action lorsque l'utilisateur choisit de jouer en mode simulation."""
        
        popup.dismiss()
        self.parent.manager.current = "simulation"


class AccueilScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.accueil_widget = AccueilWidget()
        self.add_widget(self.accueil_widget)