import random
import math
import time
import cv2
import numpy as np
import importlib.util
from PyQt5.QtWidgets import QApplication, QFileDialog
from variables.config_manager import *
from ecrans.classe import colors_are_close
from kivy.animation import Animation
from kivy.uix.screenmanager import Screen
from kivy.uix.widget import Widget
from kivy.graphics import Rectangle, Color
from kivy.core.window import Window
from kivy.clock import Clock


class SimulationWidget(Widget):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.dechets = []
        self.dechets_ratio = []
        self.robot_ratio = ( 0, 0 )
        self.en_cours = False
        self.etat_simulation = False
        self.active_manuel = False
        

        # Met à jour la position du robot si la fenêtre est redimensionnée
        self.bind(height=self.update_robot_position, width=self.update_robot_position)
        self.bind(height=self.update_dechets_position, width=self.update_dechets_position)

    def debut(self):
        config = load_config()
        self.largeur = config["largeur_plage"] / 100

        video = cv2.VideoCapture(f"assets/backgrounds/plage{config["niveau_maree"]}.mp4")
        self.frames = []
        self.fps = int(video.get(cv2.CAP_PROP_FPS))  # Récupérer les FPS

        # Lire et stocker toutes les frames
        while True:
            ret, frame = video.read()
            if not ret:
                break
            self.frames.append(frame)

        video.release()

    def on_touch_down(self, touch):
        super().on_touch_down(touch)
        if (not colors_are_close(self.parent.ids.bouton_waste.background_color, (0.25, 0.5, 0.8, 1))) and self.active_manuel: 
            self.generate_dechetsM(touch.pos)

    def generate_robot(self):

        if not hasattr(self, 'robot'): #self.parent.ids.simulatio_widget.canvas.remove(self.robot)

            with self.parent.ids.simulation_widget.canvas:

                Color(1, 1, 1, 1)
                self.robot = Rectangle(
                    source="assets/robot/robot.png",
                    pos=(15, 15),
                    size=(60, 60)
                )

            self.robot_ratio = ( 15/self.parent.ids.simulation_widget.width, 15/self.parent.ids.simulation_widget.height )

    def generate_dechets(self):

        if not self.en_cours:

            self.clear_dechets()
            config = load_config()
            nb_dechets = config["nb_dechets"]

            for _ in range(nb_dechets):
                # Position aléatoire dans la zone graphique
                random_x = random.randint(-5, int(self.parent.ids.simulation_widget.width) - 63)
                random_y = random.randint(-10, int(self.parent.ids.simulation_widget.height * self.largeur) - 53)

                with self.parent.ids.simulation_widget.canvas:
                    dechet = Rectangle(
                        source="assets/dechets/dechet.png",
                        pos=(random_x, random_y),
                        size=(100, 100),
                    )

                self.dechets.append(dechet)
                self.dechets_ratio.append((random_x/self.parent.ids.simulation_widget.width, random_y/self.parent.ids.simulation_widget.height))

    def generate_dechetsM(self, posD=(15, 15)):

        if (not self.en_cours) and (posD[1] < self.parent.ids.simulation_widget.height + 25):

            x = max(-5, min(posD[0] - 30, self.parent.ids.simulation_widget.width - 63))
            y = max(-10, min(posD[1] - 30, self.parent.ids.simulation_widget.height - 55))

            with self.parent.ids.simulation_widget.canvas:
                dechet = Rectangle(
                    source="assets/dechets/dechet.png",
                    pos=(x, y),
                    size=(100, 100),
                )

            self.dechets.append(dechet)
            self.dechets_ratio.append((posD[0]/self.parent.ids.simulation_widget.width, posD[1]/self.parent.ids.simulation_widget.height))


    def clear_dechets(self):
        """Efface les anciens déchets du canvas."""
        for dechet in self.dechets:
            self.parent.ids.simulation_widget.canvas.remove(dechet)
        self.dechets = []
        self.dechets_ratio = []

    def update_robot_position(self, *args):
        """Met à jour la position du robot en fonction de la nouvelle taille du widget."""
        pos_x = self.robot_ratio[0] * self.parent.ids.simulation_widget.width
        pos_y = self.robot_ratio[1] * self.parent.ids.simulation_widget.height

        self.robot.pos = ( pos_x, pos_y )

    def update_dechets_position(self, *args):
        """Met à jour la position des déchets en fonction de la nouvelle taille du widget."""
        index = 0
        for dechet in self.dechets:

            pos_x = self.dechets_ratio[index][0] * self.parent.ids.simulation_widget.width
            pos_y = self.dechets_ratio[index][1] * self.parent.ids.simulation_widget.height

            dechet.pos = (pos_x, pos_y)
            index += 1

    def supp_dechets(self):

        x, y = self.robot.pos
        robot_width, robot_height = self.robot.size

        # Vérifier la collision avec chacun des déchets
        for dechet in self.dechets[:]:
            dechet_x, dechet_y = dechet.pos
            dechet_width, dechet_height = dechet.size
            
            # Vérifie si le robot est au-dessus du déchet
            if (x < dechet_x + dechet_width and
                x + robot_width > dechet_x and
                y < dechet_y + dechet_height and
                y + robot_height > dechet_y):

                self.parent.ids.simulation_widget.canvas.remove(dechet)
                self.dechets.remove(dechet)

    def dans_leau(self):
        indice = min(int(self.parent.ids.background.position * self.fps), len(self.frames) - 1)
        frame = self.frames[indice]

        h, w, _ = frame.shape

        # Vérifier si les coordonnées du robot sont valides
        x, y = int(self.robot_ratio[0] * w), int(self.robot_ratio[1] * h)

        if 0 <= x < w and 0 <= y < h:
            frame_array = np.array(frame)  # Convertir en tableau NumPy rapide
            pixel = frame_array[y, x]  # Accès optimisé
            if pixel[0] < 80 and pixel[1] > 200 and pixel[1] < 210 and pixel[2] > 240:
                self.etanche = False
                self.show_temporary_message("Le robot est dans la mer", (1, 0, 0, 1), 1)


    def update(self, dt):

        if self.choix == "Parcours Classique":
            #direction
            x, y = self.robot.pos

            # Calculer la nouvelle position horizontale
            x = x + 10 * self.direction

            # Si le robot atteint un bord, verrouille la position et change de ligne
            if x < 15 or x > self.parent.ids.simulation_widget.width - 30:
                # Contraindre à l'intérieur
                x = max(15, min(x, self.parent.ids.simulation_widget.width - 30))
                # Monter d'une ligne
                y += 50
                y = max(15, min(y, self.parent.ids.simulation_widget.height * self.largeur - 35))
                # Inverser la direction
                self.direction *= -1

            self.supp_dechets()
            
            self.robot.pos = (x, y)
            self.robot_ratio = (x / self.parent.ids.simulation_widget.width, y / self.parent.ids.simulation_widget.height)
            self.dans_leau()
    

            # Si le robot atteint le haut de la zone de jeu, arrêter le parcours
            if y == (self.parent.ids.simulation_widget.height * self.largeur - 35) and x == 15:
                self.stop_simulation()
                if self.etanche:
                    self.show_temporary_message("Simulation terminée avec succès.", (0, 1, 0, 1), 1)
                else:
                    self.show_temporary_message("Échec de la simulation : Robot noyé.", (1, 0, 0, 1), 1)

        elif self.choix == "Parcours PPV":
            cible = self.dechets_copie[self.chemin[self.index]].pos
            x, y = self.robot.pos
            if x < cible[0]:
                x  += min(10, cible[0] - x)
            elif x > cible[0]:
                x -= min(10, x - cible[0])

            # Déplacement sur l'axe Y
            if y < cible[1]:
                y += min(10, cible[1] - y)
            elif y > cible[1]:
                y -= min(10, y - cible[1])

            
            self.robot.pos = (x, y)
            self.robot_ratio = (x / self.parent.ids.simulation_widget.width, y / self.parent.ids.simulation_widget.height)
            self.dans_leau()

            if cible == (x, y):
                self.parent.ids.simulation_widget.canvas.remove(self.dechets_copie[self.chemin[self.index]])
                self.dechets.remove(self.dechets_copie[self.chemin[self.index]])
                self.index += 1

            if (self.robot.pos[0] == self.dechets_copie[self.chemin[-1]].pos[0] and self.robot.pos[1] == self.dechets_copie[self.chemin[-1]].pos[1]):
                self.stop_simulation()
                if self.etanche:
                    self.show_temporary_message("Simulation terminée avec succès.", (0, 1, 0, 1), 1)
                else:
                    self.show_temporary_message("Échec de la simulation : Robot noyé.", (1, 0, 0, 1), 1)

        elif self.choix == "Parcours Hilbert":
            # Utilise la méthode update dédiée au parcours Hilbert
            if self.index >= len(self.hilbert_path):
                self.stop_simulation()
                if self.etanche:
                    self.show_temporary_message("Simulation terminée avec succès.", (0, 1, 0, 1), 1)
                else:
                    self.show_temporary_message("Échec de la simulation : Robot noyé.", (1, 0, 0, 1), 1)
                return

            cible = self.hilbert_path[self.index]
            x, y = self.robot.pos
            cible_x, cible_y = cible
            step = 10  # vitesse de déplacement, ajustable selon la configuration
            # Mise à jour sur l'axe X
            if x < cible_x:
                x += min(step, cible_x - x)
            elif x > cible_x:
                x -= min(step, x - cible_x)
            # Mise à jour sur l'axe Y
            if y < cible_y:
                y += min(step, cible_y - y)
            elif y > cible_y:
                y -= min(step, y - cible_y)

            
            self.robot.pos = (x, y)
            self.robot_ratio = (x / self.parent.ids.simulation_widget.width,
                                y / self.parent.ids.simulation_widget.height)
            self.dans_leau()

            # Si le robot a atteint la position cible, passer à la suivante
            if (x, y) == cible:
                self.index += 1

            self.supp_dechets()


        elif self.choix == "Parcours Spirale":
            
            step_x = int( self.parent.ids.simulation_widget.width / 15 )
            step_y = int( (self.parent.ids.simulation_widget.height * self.largeur) / 15 )
            x, y = self.robot.pos

            # Déterminer le déplacement selon la direction actuelle
            if self.spiral_direction == 0:  # droite
                x += min(step_x, self.spiral_segment_length - self.spiral_current_count)
            elif self.spiral_direction == 1:  # bas
                y -= min(step_y, self.spiral_segment_length - self.spiral_current_count)
            elif self.spiral_direction == 2:  # gauche
                x -= min(step_x, self.spiral_segment_length - self.spiral_current_count)
            elif self.spiral_direction == 3:  # haut
                y += min(step_y, self.spiral_segment_length - self.spiral_current_count)

            self.spiral_current_count += step_x
            x = max(15, min(x, self.parent.ids.simulation_widget.width - 30))
            y = max(15, min(y, self.parent.ids.simulation_widget.height * self.largeur - 35))

            # Si on a atteint (ou dépassé) la longueur du segment, faire un virage
            if self.spiral_current_count >= self.spiral_segment_length:
                self.spiral_direction = (self.spiral_direction + 1) % 4
                self.spiral_current_count = 0
                self.spiral_turn_count += 1
                # Augmenter la longueur du segment tous les deux virages
                if self.spiral_turn_count % 2 == 0:
                    self.spiral_segment_length += 20

            
            self.robot.pos = (x, y)
            self.robot_ratio = (x / self.parent.ids.simulation_widget.width, y / self.parent.ids.simulation_widget.height)
            self.dans_leau()

            self.supp_dechets()

            if y == (self.parent.ids.simulation_widget.height * self.largeur - 35) and x == 15:
                self.stop_simulation()
                if self.etanche:
                    self.show_temporary_message("Simulation terminée avec succès.", (0, 1, 0, 1), 1)
                else:
                    self.show_temporary_message("Échec de la simulation : Robot noyé.", (1, 0, 0, 1), 1)

        elif self.choix == "Parcours Perso":
            try:
                self.module_utilisateur.main(self.robot)
            except Exception as e:
                self.stop_simulation()
                self.show_temporary_message("Erreur dans le main.", (1, 0, 0, 1), 1)

            x, y = self.robot.pos
            x = max(15, min(x, self.parent.ids.simulation_widget.width - 30))
            y = max(15, min(y, self.parent.ids.simulation_widget.height * self.largeur - 35))
            self.robot.pos = (x, y)

            self.dans_leau()
            self.supp_dechets()

            if y == (self.parent.ids.simulation_widget.height * self.largeur - 35) and x == 15:
                self.stop_simulation()
                if self.etanche:
                    self.show_temporary_message("Simulation terminée avec succès.", (0, 1, 0, 1), 1)
                else:
                    self.show_temporary_message("Échec de la simulation : Robot noyé.", (1, 0, 0, 1), 1)

    def ouvrir_explorateur_qt(self):
        app = QApplication([])
        chemin_fichier, _ = QFileDialog.getOpenFileName(
            None, "Choisir un fichier", "", "Fichiers Python (*.py)"
        )
        
        if chemin_fichier:
            return chemin_fichier


    def charger_et_executer(self, chemin_fichier):
        """ Charge dynamiquement le fichier et exécute une fonction spécifique. """
        spec = importlib.util.spec_from_file_location("module_utilisateur", chemin_fichier)
        self.module_utilisateur = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(self.module_utilisateur)

    def calculer_distances(self):
        n = len(self.dechets)
        distances = [[0 for _ in range(n)] for _ in range(n)]
        for i in range(n):
            for j in range(n):
                dx = self.dechets[i].pos[0] - self.dechets[j].pos[0]
                dy = self.dechets[i].pos[1] - self.dechets[j].pos[1]
                distances[i][j] = math.sqrt(dx * dx + dy * dy)

        return distances

    # Résoudre le TSP avec l'algorithme du plus proche voisin
    def plus_proche_voisin(self, start, distances):
        chemin = [start]
        non_visites = list( range( len(self.dechets) ) )
        non_visites.remove(start)

        while non_visites:
            dernier_point = chemin[-1]
            prochain_point = min(non_visites, key=lambda point: distances[dernier_point][point])
            chemin.append(prochain_point)
            non_visites.remove(prochain_point)

        return chemin
        
    def hilbert_index_to_xy(self, n, d):
        """
        Convertit un indice d sur une courbe de Hilbert en coordonnées (x, y) pour une grille n x n,
        où n est une puissance de 2.
        """
        x = 0
        y = 0
        t = d
        s = 1
        while s < n:
            rx = 1 & (t // 2)
            ry = 1 & (t ^ rx)
            if ry == 0:
                if rx == 1:
                    x, y = s - 1 - x, s - 1 - y
                # Échange x et y
                x, y = y, x
            x += s * rx
            y += s * ry
            t //= 4
            s *= 2
        return x, y

    # Méthode pour générer le chemin de Hilbert et l'adapter aux dimensions de la zone
    def generate_hilbert_path(self):
        order = 4  # Par exemple, une grille 16x16
        n = 2 ** order  # Taille de la grille
        total_points = n * n
        points = [self.hilbert_index_to_xy(n, d) for d in range(total_points)]
        # Mise à l'échelle : adapter de la grille [0, n-1] à la zone réelle
        zone_width = self.parent.ids.simulation_widget.width - 30
        zone_height = self.parent.ids.simulation_widget.height * self.largeur - 35
        scaled_points = []
        for (x, y) in points:
            scaled_x = max( 15, int(x / (n - 1) * (zone_width - 1)) )
            scaled_y = max( 15, int(y / (n - 1) * (zone_height - 1)) )
            scaled_points.append((scaled_x, scaled_y))
        self.hilbert_path = scaled_points

    def show_temporary_message(self, message, couleur, temps):
        """Affiche un message temporaire avec animation."""
        label = self.parent.ids.label
        label.text = message
        label.color = couleur

        # Animation pour rendre le message visible et disparaître
        anim = Animation(opacity=1, duration=temps) + Animation(opacity=0, duration=temps*2)
        anim.start(label)

    def demarrer_simulation(self):
        
        if self.dechets:

            self.etat_simulation = not self.etat_simulation
            self.parent.ids.bouton.icon_source = "assets/icones/icone_pause.png" if self.etat_simulation else "assets/icones/icone_start.png"

            if not self.en_cours:

                self.en_cours = True
                self.etanche = True
                self.choix = self.parent.ids.parcours_spinner.text
                self.parent.ids.simulation_widget.dim_opacity = 0
                self.active_manuel = False

                if not hasattr(self, 'robot'):
                    self.generate_robot()
            
                # Placer le robot en bas à gauche
                self.robot.pos = (15, 15)
                self.robot_ratio = ( 15/self.parent.ids.simulation_widget.width, 15/self.parent.ids.simulation_widget.height )
                if self.choix == "Parcours Classique": self.direction = 1

                elif self.choix == "Parcours PPV":
                    distances = self.calculer_distances()
                    self.chemin = self.plus_proche_voisin(0, distances)
                    self.index = 0
                    self.dechets_copie = self.dechets[:]

                elif self.choix == "Parcours Hilbert":
                    self.hilbert_path = []
                    self.index = 0
                    self.generate_hilbert_path()

                elif self.choix == "Parcours Spirale":
                    self.robot.pos = (self.parent.ids.simulation_widget.width / 2, (self.parent.ids.simulation_widget.height * self.largeur - 35) / 2)
                    self.robot_ratio = (self.robot.pos[0] / self.parent.ids.simulation_widget.width, self.robot.pos[1] / self.parent.ids.simulation_widget.height)
                    # Initialisation de l'état de la spirale
                    self.spiral_direction = 0
                    self.spiral_segment_length = 50
                    self.spiral_current_count = 0
                    self.spiral_turn_count = 0

                elif self.choix == "Parcours Perso":
                    chemin = self.ouvrir_explorateur_qt()
                    if not chemin == None: self.charger_et_executer(chemin)
                
                config = load_config()
                vitesse = config["vitesse_simulation"]
                Clock.schedule_interval(self.update, 0.1 / vitesse)

            else:
                if not self.etat_simulation:
                    Clock.unschedule(self.update)
                else:
                    config = load_config()
                    vitesse = config["vitesse_simulation"]
                    Clock.schedule_interval(self.update, 0.1 / vitesse)
        else:
            self.show_temporary_message("La plage est déjà propre.", (0, 1, 0, 1), 1)


    def stop_simulation(self):
        Clock.unschedule(self.update)
        self.etat_simulation = False
        self.en_cours = False
        self.parent.ids.bouton.icon_source = "assets/icones/icone_start.png"

        self.robot.pos = (15, 15)
        self.robot_ratio = ( 15/self.parent.ids.simulation_widget.width, 15/self.parent.ids.simulation_widget.height )


class SimulationScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.simulation_widget = SimulationWidget()
        self.add_widget(self.simulation_widget)
        self.first_time = True

    def on_pre_enter(self):
        self.simulation_widget.generate_robot()
        self.simulation_widget.debut()

    def on_enter(self):
        if self.first_time:
            self.first_time = False
            self.simulation_widget.generate_dechets()

    def on_leave(self):
        if self.simulation_widget.etat_simulation == True:
            self.simulation_widget.demarrer_simulation()