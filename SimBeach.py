from kivy.config import Config
Config.set('graphics', 'minimum_width', '600')
Config.set('graphics', 'minimum_height', '450')
#Config.set('graphics', 'resizable', '0')  # 0 pour désactiver, 1 pour autoriser

from kivy.core.window import Window
Window.set_icon("assets/robot/robot.jpg")

from variables.config_manager import *
from kivy.uix.screenmanager import ScreenManager
from ecrans.accueil_screen import AccueilScreen
from ecrans.jeu_screen import JeuScreen
from ecrans.simulation_screen import SimulationScreen
from ecrans.robot_screen import RobotScreen
from ecrans.options_screen import OptionsScreen
from kivy.lang import Builder
from kivy.app import App

# Chargeament d tout les fichiers de structure
for nom in ["interface", "style", "accueil_structure", "jeu_structure", "simulation_structure", "robot_structure", "options_structure"]:
    Builder.load_file("structure/" + nom + ".kv")


class MyScreenManager(ScreenManager):
    pass


class SimBeachApp(App):
    def build(self):
        self.config = load_config()

        sm = MyScreenManager()
        return sm


if __name__ == "__main__":
    SimBeachApp().run()