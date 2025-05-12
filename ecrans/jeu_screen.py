import random
from variables.config_manager import *
from kivy.uix.screenmanager import Screen
from kivy.uix.label import Label
from kivy.uix.widget import Widget
from kivy.animation import Animation
from kivy.graphics import Rectangle, Color
from kivy.core.image import Image
from kivy.core.window import Window
from kivy.clock import Clock



class JeuWidget(Widget):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.boules = []
        self.en_cours = False
        self.etat_jeu = False
        self.image_feu = Image("assets/dechets/boule2.png").texture

        # Met à jour la position du robot si la fenêtre est redimensionnée
        Window.bind(size=self.on_window_resize)


    def on_window_resize(self, *args):
        if not hasattr(self, 'robot'):
            return
        Clock.schedule_once(self.update_robot_position, 0.4)
        Clock.schedule_once(self.update_kraken_position, 0.4)
        Clock.schedule_once(self.update_dechets_position, 0.4)


    def generate_robot(self):

        with self.parent.ids.jeu_widget.canvas:
            Color(1, 1, 1, 1)

            self.robot = Rectangle(
                source="assets/robot/robot.png",
                pos=(self.parent.ids.jeu_widget.center_x, 15),
                size=(60, 60)
            )

        self.robot_ratio = ( 15/self.parent.ids.jeu_widget.width, 15/self.parent.ids.jeu_widget.height )


    def generate_kraken(self):


        with self.parent.ids.jeu_widget.canvas:
            Color(1, 1, 1, 1)

            self.kraken = Rectangle(
                source="assets/robot/kraken.png",
                pos=(15, self.parent.ids.jeu_widget.height - 190),
                size=(400, 200)
            )

        self.kraken_ratio = ( self.kraken.pos[0]/self.parent.ids.jeu_widget.width, self.kraken.pos[1]/self.parent.ids.jeu_widget.height )


    def generate_dechets(self):

        # Position aléatoire dans la zone graphique
        random_x = random.randint(-5, int(self.parent.ids.jeu_widget.width) - 63)
        random_y = random.randint(-10, int(self.parent.ids.jeu_widget.height) - 53)

        with self.parent.ids.jeu_widget.canvas:
            Color(1, 1, 1, 1)
            self.dechet = Rectangle(
                source="assets/dechets/dechet.png",
                pos=(random_x, random_y),
                size=(100, 100),
            )

        self.dechets_ratio = (random_x/self.parent.ids.jeu_widget.width, random_y/self.parent.ids.jeu_widget.height)

    def on_key_down(self, window, key, scancode, text, modifiers):
        """Déplace le robot en fonction de la touche pressée."""

        if not hasattr(self, 'robot'):
            return

        step = 15
        current_x, current_y = self.robot.pos

        if key == 276:  # Flèche gauche
            current_x -= step
        if key == 275:  # Flèche droite
            current_x += step
        if key == 273:  # Flèche haut
            current_y += step
        if key == 274:  # Flèche bas
            current_y -= step

        self.ramasser_dechet()

        max_x = self.parent.ids.jeu_widget.width - 35
        max_y = self.parent.ids.jeu_widget.height - 35

        current_x = max(15, min(max_x, current_x))
        current_y = max(15, min(max_y, current_y))

        if hasattr(self, 'robot'): self.robot.pos = (current_x, current_y)
        self.robot_ratio = ( current_x/self.parent.ids.jeu_widget.width, current_y/self.parent.ids.jeu_widget.height )

    def load_level(self):

        self.etat_jeu = not self.etat_jeu
        self.parent.ids.bouton.icon_source = "assets/icones/icone_pause.png" if self.etat_jeu else "assets/icones/icone_start.png"

        if not self.en_cours:
            self.parent.ids.jeu_widget.dim_opacity = 0
            self.en_cours = True
            self.score_dechet = 0

            self.parent.ids.game_over.text = ""

            self.parent.ids.score.text = f"Score: {self.score_dechet}"
            self.parent.ids.best_score.text = f"Meilleur Score: {load_config()["best_score"]}"
            self.generate_robot()
            self.generate_kraken()
            self.animer_kraken()
            self.generate_dechets()

            Window.bind(on_key_down=self.on_key_down)
            Clock.schedule_once(self.lancer_feu, random.uniform(2, 5))
            Clock.schedule_interval(self.collision_boules, 1/60)
        else:
            if self.etat_jeu:
                Window.bind(on_key_down=self.on_key_down)
                Clock.schedule_once(self.lancer_feu, random.uniform(2, 5))
                Clock.schedule_interval(self.collision_boules, 1/60)
                self.anim.start(self.kraken)
            else:
                Window.unbind(on_key_down=self.on_key_down)
                Clock.unschedule(self.collision_boules)
                self.anim.stop(self.kraken)


    def ramasser_dechet(self):
        """Ramasse un déchet si le robot est au-dessus."""
        robot_x, robot_y = self.robot.pos
        robot_width, robot_height = self.robot.size
        
        dechet_x, dechet_y = self.dechet.pos
        dechet_width, dechet_height = self.dechet.size
        
        # Vérifie si le robot est au-dessus du déchet
        if (robot_x < dechet_x + dechet_width and
            robot_x + robot_width > dechet_x and
            robot_y < dechet_y + dechet_height and
            robot_y + robot_height > dechet_y):

            self.parent.ids.jeu_widget.canvas.remove(self.dechet)
            del self.dechet
            self.generate_dechets()

            self.score_dechet += 1
            self.parent.ids.score.text = f"Score: {self.score_dechet}"

    def collision_boules(self, dt):
        """ Vérifie si le robot touche une des boules. """
        robot_x, robot_y = self.robot.pos
        robot_width, robot_height = self.robot.size

        for boule in self.boules[:]:  # Parcourir une copie pour éviter des suppressions en cours
            boule_x, boule_y = boule.pos[0] + 4, boule.pos[1] + 4
            boule_width, boule_height = boule.size[0] - 8, boule.size[1] - 8

            # Vérifier si la boule touche le robot
            if (robot_x < boule_x + boule_width and
                robot_x + robot_width > boule_x and
                robot_y < boule_y + boule_height and
                robot_y + robot_height > boule_y):

                Window.unbind(on_key_down=self.on_key_down)
                Clock.unschedule(self.collision_boules)
                
                self.etat_jeu = False
                self.en_cours = False
                self.parent.ids.bouton.icon_source = "assets/icones/icone_start.png"
                if self.score_dechet > load_config()["best_score"]: modify_variable("best_score", self.score_dechet)
                self.parent.ids.jeu_widget.dim_opacity = 0.5
                self.parent.ids.game_over.text = "GAME OVER"

                self.parent.ids.jeu_widget.canvas.remove(self.dechet)
                del self.dechet
                self.parent.ids.jeu_widget.canvas.remove(self.robot)
                del self.robot
                self.parent.ids.jeu_widget.canvas.remove(self.kraken)
                del self.kraken




    def update_robot_position(self, dt):
        """Met à jour la position du robot en fonction de la nouvelle taille du widget."""
        pos_x = self.robot_ratio[0] * self.parent.ids.jeu_widget.width
        pos_y = self.robot_ratio[1] * self.parent.ids.jeu_widget.height

        self.robot.pos = ( pos_x, pos_y )

    def update_kraken_position(self, dt):
        """Met à jour la position du robot en fonction de la nouvelle taille du widget."""
        pos_x = self.kraken_ratio[0] * self.parent.ids.jeu_widget.width
        pos_y = self.kraken_ratio[1] * self.parent.ids.jeu_widget.height

        self.kraken.pos = ( pos_x, pos_y )


    def update_dechets_position(self, dt):
        """Met à jour la position des déchets en fonction de la nouvelle taille du widget."""

        pos_x = self.dechets_ratio[0] * self.parent.ids.jeu_widget.width
        pos_y = self.dechets_ratio[1] * self.parent.ids.jeu_widget.height

        self.dechet.pos = (pos_x, pos_y)


    def animer_kraken(self):
        """
        Fait se déplacer le Kraken d'un côté à l'autre.
        Par exemple, du bord gauche au bord droit de la zone de simulation.
        """
        sim_width = self.parent.ids.jeu_widget.width
        left_limit = 15  # Distance minimale à gauche
        right_limit = sim_width - self.kraken.size[0] + 15  # Distance maximale à droite

        # Animation avec des limites ajustées
        self.anim = Animation(pos=(right_limit, self.kraken.pos[1]), duration=3)
        self.anim += Animation(pos=(left_limit, self.kraken.pos[1]), duration=3)

        self.anim.repeat = True
        self.anim.start(self.kraken)


    def lancer_feu(self, dt):
        if ( not hasattr(self, 'kraken') ) and ( not self.etat_jeu ):
            return
        # Position de départ aléatoire en X et en haut de l'écran
        x = self.kraken.pos[0] + self.kraken.size[0] / 2 - 25  # 25 = 50/2 (si le déchet fait 50 de large)
        # Par exemple, le déchet part de juste en dessous du Kraken
        y = self.kraken.pos[1]

        # Création du déchet sur le canvas
        with self.parent.ids.jeu_widget.canvas:
            feu = Rectangle(
                texture=self.image_feu,
                pos=(x, y),
                size=(50, 50),
            )
        self.boules.append(feu)

        # Animation pour faire tomber le déchet jusqu'en bas (pos[1] = 0)
        anim = Animation(pos=(x, 0), duration=random.uniform(1.5, 3))
        
        # Une fois l'animation complète, effectuer la suppression directement dans le lambda
        anim.bind(on_complete=lambda anim, widget: (
            self.parent.ids.jeu_widget.canvas.remove(feu), 
            self.boules.remove(feu)
        ))

        anim.start(feu)

        if self.etat_jeu:
            next_interval = random.uniform(0, 1)
            Clock.schedule_once(self.lancer_feu, next_interval)



class JeuScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.jeu_widget = JeuWidget()
        self.add_widget(self.jeu_widget)
        self.first_time = True


