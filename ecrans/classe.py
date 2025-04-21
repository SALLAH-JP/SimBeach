from kivy.uix.label import Label
from kivy.uix.behaviors import ButtonBehavior
from kivy.uix.button import Button
from kivy.properties import StringProperty, ListProperty, NumericProperty
from kivy.metrics import dp
from kivy.config import Config
from kivy.uix.widget import Widget
from kivy.animation import Animation
from kivy.app import App
from kivy.uix.video import Video
from kivy.clock import Clock
from kivy.uix.screenmanager import Screen

# Désactive l'affichage du cercle rouge
Config.set('input', 'mouse', 'mouse,disable_multitouch')


class ButtonIcon(ButtonBehavior, Label):
    icon_source = StringProperty("default_icon.png")
    # Propriété pour la position de l'icône
    icon_pos = ListProperty([0, 0])

    background_color = ListProperty([0.25, 0.5, 0.8, 1])
    def on_press(self):
        anim = Animation(background_color=(0.125, 0.25, 0.4, 1), duration=0.1)
        anim.start(self)

    def on_release(self):
        anim = Animation(background_color=(0.25, 0.5, 0.8, 1), duration=0.1)
        anim.start(self)

class MyButton(ButtonIcon):
    def on_press(self):
        if colors_are_close(self.background_color, (0.25, 0.5, 0.8, 1)):
            anim = Animation(background_color=(0.125, 0.25, 0.4, 1), duration=0.1)
            anim.start(self)
        elif colors_are_close(self.background_color, (1, 0, 0, 1)):
            anim = Animation(background_color=(0.5, 0, 0, 1), duration=0.1)
            anim.start(self)

    def on_release(self):
        if colors_are_close(self.background_color, (0.125, 0.25, 0.4, 1)):
            anim = Animation(background_color=(0.25, 0.5, 0.8, 1), duration=0.1)
            anim.start(self)
        elif colors_are_close(self.background_color, (0.5, 0, 0, 1)):
            anim = Animation(background_color=(1, 0, 0, 1), duration=0.1)
            anim.start(self)

    def on_touch_down(self, touch):
        if self.collide_point(*touch.pos):
            simulation_screen = App.get_running_app().root.get_screen('simulation')
            if touch.button == 'right':
                if colors_are_close(self.background_color, (0.25, 0.5, 0.8, 1)):
                    self.background_color = (1, 0, 0, 1)
                elif colors_are_close(self.background_color, (1, 0, 0, 1)):
                    self.background_color = (0.25, 0.5, 0.8, 1)
                    simulation_screen.ids.simulation_widget.dim_opacity = 0
                    simulation_screen.simulation_widget.active_manuel = False
                return True
            elif touch.button == 'left' and simulation_screen.simulation_widget.etat_simulation == False:
                if colors_are_close(self.background_color, (0.25, 0.5, 0.8, 1)) or colors_are_close(self.background_color, (0.125, 0.25, 0.4, 1)):
                    simulation_screen.simulation_widget.generate_dechets()
                elif colors_are_close(self.background_color, (1, 0, 0, 1)) or colors_are_close(self.background_color, (0.5, 0, 0, 1)):
                    if simulation_screen.simulation_widget.active_manuel == True:
                        simulation_screen.ids.simulation_widget.dim_opacity = 0
                        simulation_screen.simulation_widget.active_manuel = False
                    else:
                        simulation_screen.simulation_widget.clear_dechets()
                        simulation_screen.ids.simulation_widget.dim_opacity = 0.5
                        simulation_screen.simulation_widget.active_manuel = True

        return super(MyButton, self).on_touch_down(touch)


class DimmingWidget(Widget):
    dim_opacity = NumericProperty(0)  # Valeur d'opacité initiale


def colors_are_close(color1, color2, tolerance=0.01):
    return all(abs(a - b) <= tolerance for a, b in zip(color1, color2))


