from kivy.config import Config
Config.set('graphics', 'minimum_width', '600')
Config.set('graphics', 'minimum_height', '450')
#Config.set('graphics', 'resizable', '0') # 0 pour désactiver, 1 pour autoriser


from kivy.core.window import Window
from kivy.app import App
from variables.config_manager import *
from kivy.uix.screenmanager import ScreenManager
from ecrans.accueil_screen import AccueilScreen
from ecrans.jeu_screen import JeuScreen
from ecrans.simulation_screen import SimulationScreen
from ecrans.robot_screen import RobotScreen
from ecrans.options_screen import OptionsScreen
from kivy.lang import Builder

# Définir l'icône de la fenêtre
Window.set_icon("assets/robot/robot.jpg")

for nom in ["interface", "style", "accueil_structure", "jeu_structure", "simulation_structure", "robot_structure", "options_structure"]:
    Builder.load_file("structure/" + nom + ".kv")



class MyScreenManager(ScreenManager):
    pass

class MainApp(App):
    def build(self):
        self.config = load_config()
        sm = MyScreenManager()
        sm.current = 'accueil'

        return sm

if __name__ == "__main__":
    MainApp().run()