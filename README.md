<div align="center">

<img src="robot.ico" alt="SimBeach Logo" width="100"/>

# 🏖️ SimBeach

### *Simulateur de robot nettoyeur de plage*

**Application Python/Kivy permettant de simuler et comparer différents algorithmes de parcours pour la collecte autonome de déchets sur une plage, avec connexion optionnelle à un robot réel via USB ou Wi-Fi.**

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Python](https://img.shields.io/badge/Python-3.8+-blue.svg?logo=python&logoColor=white)](https://www.python.org/)
[![Kivy](https://img.shields.io/badge/GUI-Kivy-1976D2)](https://kivy.org/)
[![OpenCV](https://img.shields.io/badge/Vision-OpenCV-5C3EE8?logo=opencv&logoColor=white)](https://opencv.org/)
[![Arduino](https://img.shields.io/badge/Arduino-USB%20%2F%20Wi--Fi-00979D?logo=arduino&logoColor=white)](https://www.arduino.cc/)

[**🚀 Installation**](#-installation) · [**🧮 Algorithmes**](#-algorithmes-de-parcours)

</div>

---

## 📋 Sommaire

- [À propos](#-à-propos)
- [Fonctionnalités](#-fonctionnalités)
- [Algorithmes de parcours](#-algorithmes-de-parcours)
- [Mode Jeu](#-mode-jeu)
- [Connexion à un robot réel](#-connexion-à-un-robot-réel)
- [Installation](#-installation)
- [Lancement](#%EF%B8%8F-lancement)
- [Configuration](#%EF%B8%8F-configuration)
- [Structure du projet](#-structure-du-projet)
- [Auteurs](#-auteurs)
- [Licence](#-licence)

---

## 🎯 À propos

**SimBeach** est un simulateur permettant d'explorer et de comparer plusieurs **algorithmes de parcours** dans un contexte concret : un robot autonome qui nettoie une plage en ramassant les déchets. Le simulateur intègre la **détection visuelle de l'eau** par traitement d'image, et peut piloter un véritable robot via série USB ou socket Wi-Fi.

L'application combine **trois axes** :
- 🧮 **Algorithmique** : implémentation de stratégies de parcours classiques (balayage, PPV/TSP, courbes de Hilbert, spirale) et chargement de scripts personnalisés
- 🎮 **Ludique** : un mode jeu interactif avec contrôle clavier, ennemi à éviter et système de score
- 🤖 **Embarqué** : protocole de communication avec un robot réel (handshake PING/PONG, détection automatique de ports)

---

## ✨ Fonctionnalités

### 🖥️ Mode Simulation
- Génération de déchets **aléatoires** ou **manuels** (placement à la souris)
- **5 algorithmes de parcours** sélectionnables et comparables
- **Détection de collision** et collecte automatique des déchets
- **Détection de l'eau** via OpenCV (analyse de frames vidéo)
- Pause / reprise à tout moment
- **Vitesse** et **niveau de marée** configurables

### 🎮 Mode Jeu
- Contrôle du robot aux **touches directionnelles**
- Collecte de déchets tombants
- Évitement du **Kraken** (ennemi qui tire des projectiles)
- **Système de score** avec sauvegarde du meilleur score

### 🤖 Connexion Robot
- **Série USB** vers Arduino à 115 200 bauds
- **Socket Wi-Fi** avec handshake PING/PONG
- **Détection automatique** des ports série disponibles

---

## 🧮 Algorithmes de parcours

| Algorithme | Description | Cas d'usage |
| --- | --- | --- |
| **Parcours Classique** | Balayage linéaire de gauche à droite, ligne par ligne | Référence simple, couverture exhaustive |
| **Parcours PPV** | Plus Proche Voisin — heuristique du voyageur de commerce (TSP) | Optimisation du chemin sur déchets clairsemés |
| **Parcours Hilbert** | Courbe de remplissage d'espace fractale | Couverture homogène avec préservation de localité |
| **Parcours Spirale** | Recherche en spirale depuis le centre | Stratégie de découverte progressive |
| **Parcours Perso** | Chargement d'un script Python personnalisé | Tester ses propres algorithmes |

Chaque parcours utilise un système de **coordonnées normalisées** (ratios `0.0` à `1.0`) pour être indépendant de la résolution d'écran.

---

## 🎮 Mode Jeu

Une touche fun au projet : un mode interactif inspiré des arcades classiques.

**Contrôles :**
- ⬅️ ➡️ ⬆️ ⬇️ Déplacer le robot
- 🗑️ Ramasser les déchets qui tombent
- ⚠️ Éviter les projectiles du Kraken
- 🏆 Battre le meilleur score (sauvegardé entre les sessions)

---

## 🤖 Connexion à un robot réel

L'application peut piloter un robot physique selon deux modes :

### Mode USB (Série)
- Détection automatique des ports COM/ttyACM
- Communication à **115 200 bauds**
- Envoi des coordonnées du parcours

### Mode Wi-Fi (Socket)
- Connexion TCP/IP à l'IP du robot
- **Handshake PING/PONG** pour valider la connexion
- Port configurable (par défaut **8080**)

---

## 🚀 Installation

### Prérequis

- **Python 3.8** ou supérieur
- pip

### Dépendances

```bash
pip install kivy opencv-python numpy pyqt5 pyserial
```

Détail des bibliothèques :

| Bibliothèque | Usage |
| --- | --- |
| `kivy` | Framework GUI multi-plateforme |
| `opencv-python` | Analyse vidéo (détection d'eau) |
| `numpy` | Calculs matriciels |
| `pyqt5` | Composants additionnels |
| `pyserial` | Communication série USB |

### Cloner le dépôt

```bash
git clone https://github.com/SALLAH-JP/SimBeach.git
cd SimBeach
```

---

## ▶️ Lancement

```bash
python SimBeach.py
```

L'application s'ouvre sur l'écran d'accueil. Naviguer ensuite vers :
- **Simulation** pour comparer les algorithmes
- **Jeu** pour le mode arcade
- **Robot** pour la connexion physique
- **Options** pour la configuration

---

## ⚙️ Configuration

Les paramètres sont sauvegardés dans `variables/config.json` :

| Paramètre | Description | Défaut |
| --- | --- | --- |
| `nb_dechets` | Nombre de déchets générés | `20` |
| `largeur_plage` | Largeur utile de la plage (%) | `100` |
| `niveau_maree` | Niveau de marée (0 à 3) | `0` |
| `vitesse_simulation` | Multiplicateur de vitesse | `1` |
| `ip` | Adresse IP du robot (Wi-Fi) | `192.168.0.1` |
| `port_usb` | Port série USB | `COM3` |
| `port_wifi` | Port Wi-Fi | `8080` |

---

## 🧩 Parcours personnalisé

Tu peux charger un **script Python custom** définissant ton propre algorithme de parcours. Le script doit exposer une fonction compatible avec le système de coordonnées en ratios (`0.0` à `1.0`).

Exemple de signature attendue :

```python
def generer_parcours(largeur, hauteur, dechets):
    """
    Génère une liste de points (x, y) en ratios 0.0-1.0
    
    Args:
        largeur: largeur normalisée de la zone (1.0)
        hauteur: hauteur normalisée de la zone (1.0)
        dechets: liste des positions des déchets
    
    Returns:
        list[tuple[float, float]]: séquence de points à visiter
    """
    points = []
    # Votre algorithme ici
    return points
```

---

## 📁 Structure du projet

```
SimBeach/
├── SimBeach.py                 # Point d'entrée principal
│
├── ecrans/                     # Logique des écrans
│   ├── accueil_screen.py       # Écran d'accueil
│   ├── simulation_screen.py    # Mode simulation
│   ├── jeu_screen.py           # Mode jeu
│   ├── robot_screen.py         # Connexion robot
│   ├── options_screen.py       # Paramètres
│   └── classe.py               # Composants UI personnalisés
│
├── structure/                  # Fichiers de layout Kivy (.kv)
│
├── variables/                  # Gestion de la configuration
│   ├── config_manager.py
│   └── config.json
│
├── assets/                     # Médias (vidéos, images, icônes)
├── robot.ico                   # Icône de l'application
└── LICENSE
```

---

## 🛠️ Technologies

- [**Kivy**](https://kivy.org/) — framework GUI Python multi-plateforme
- [**OpenCV**](https://opencv.org/) — vision par ordinateur (détection d'eau)
- [**NumPy**](https://numpy.org/) — calculs matriciels et géométriques
- [**PyQt5**](https://pypi.org/project/PyQt5/) — composants additionnels
- [**PySerial**](https://pythonhosted.org/pyserial/) — communication USB

---

## 👥 Auteurs

Projet réalisé dans le cadre d'un projet pédagogique encadré.

**Jean-Paul SALLAH**
Étudiant en Licence Informatique Appliquée
🎓 Université des Mascareignes (Maurice)

[![GitHub](https://img.shields.io/badge/GitHub-SALLAH--JP-181717?logo=github)](https://github.com/SALLAH-JP)
[![LinkedIn](https://img.shields.io/badge/LinkedIn-Jean--Paul%20SALLAH-0A66C2?logo=linkedin)](https://www.linkedin.com/in/jeanpaul-sallah/)


---

## 📜 Licence

Ce projet est distribué sous licence **MIT** — voir le fichier [`LICENSE`](LICENSE).

---

<div align="center">

*Si ce projet vous a plu, n'hésitez pas à laisser une ⭐ !*

</div>
