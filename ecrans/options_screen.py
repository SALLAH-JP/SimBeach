from kivy.app import App
from kivy.uix.widget import Widget
from kivy.uix.screenmanager import Screen
from kivy.animation import Animation
from variables.config_manager import *

class OptionsWidget(Widget):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def on_pre_enter(self):
        # Avant d'afficher l'écran, charger la configuration et remplir les champs
        config = load_config()

        self.parent.ids.nb_dechets.text = ""
        self.parent.ids.largeur_plage.text = ""
        self.parent.ids.vitesse_simulation.text = ""

        self.parent.ids.nb_dechets.hint_text = str( config.get("nb_dechets", "") )
        self.parent.ids.largeur_plage.hint_text = str( config.get("largeur_plage", "") )
        self.parent.ids.vitesse_simulation.hint_text = str( config.get("vitesse_simulation", "") )
        self.parent.ids.niveau_maree.value = config.get("niveau_maree", 1)


    def enregistrer_parametres(self):
        config = load_config()
        
        try:
            for index in ["nb_dechets", "largeur_plage", "vitesse_simulation"]:
                value = self.parent.ids[index].text
                
                if value == "": value = config[index]
                
                try:
                    value = int(value)
                except ValueError:
                    raise ValueError(f"Le paramètre '{index}' doit être un entier valide.")

                if value <= 0:
                    raise ValueError(f"Le paramètre '{index}' doit être strictement supérieur à zéro.")
        
        except ValueError as e:
            self.show_temporary_message(str(e), (1, 0, 0, 1))
            return

        for index in ["nb_dechets", "largeur_plage", "vitesse_simulation"]:
            value = self.parent.ids[index].text
            if value == "": value = config[index]

            if index == "nb_dechets" and int(value) > 1000: value = 1000
            if index == "largeur_plage" and int(value) > 100: value = 100
            
            modify_variable(index, int(value))
        modify_variable("niveau_maree", int(self.parent.ids["niveau_maree"].value))

        if not config["niveau_maree"] == int(self.parent.ids["niveau_maree"].value):
            App.get_running_app().root.get_screen('simulation').ids.background.source = f"assets/backgrounds/plage{int(self.parent.ids["niveau_maree"].value)}.mp4"

        self.on_pre_enter()
        self.show_temporary_message("Les paramètres ont été enregistrer avec succès.", (0, 1, 0, 1))



    def show_temporary_message(self, message, couleur):
        """Affiche un message temporaire avec animation."""
        label = self.parent.ids.error_label
        label.text = message
        label.color = couleur

        # Animation pour rendre le message visible et disparaître
        anim = Animation(opacity=1, duration=1) + Animation(opacity=0, duration=2)
        anim.start(label)



class OptionsScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.options_widget = OptionsWidget()
        self.add_widget(self.options_widget)

    def on_pre_enter(self):
        self.options_widget.on_pre_enter()