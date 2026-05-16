# SimBeach

Simulateur de robot nettoyeur de plage développé avec Python et Kivy. L'application permet de simuler différents algorithmes de parcours pour la collecte de déchets sur une plage, avec la possibilité de connecter un vrai robot via USB ou Wi-Fi.

## Fonctionnalités

### Mode Simulation
- Génération de déchets aléatoires ou manuels sur la plage
- Plusieurs algorithmes de parcours :
  - **Parcours Classique** : balayage linéaire de gauche à droite
  - **Parcours PPV** (Plus Proche Voisin) : algorithme du voyageur de commerce (TSP)
  - **Parcours Hilbert** : courbe de remplissage d'espace de Hilbert
  - **Parcours Spirale** : recherche en spirale
  - **Parcours Perso** : chargement d'un script Python personnalisé
- Détection de collision et collecte des déchets
- Détection de l'eau via analyse de frames vidéo (OpenCV)
- Pause / reprise de la simulation
- Vitesse et niveau de marée configurables

### Mode Jeu
- Contrôle du robot avec les touches directionnelles
- Collecte de déchets tombants
- Évitement du Kraken (ennemi qui tire des projectiles)
- Système de score avec meilleur score persistant

### Connexion Robot
- Connexion série USB à un Arduino (115200 baud)
- Connexion socket Wi-Fi avec handshake PING/PONG
- Détection automatique des ports disponibles

## Prérequis

- Python 3.8+
- Kivy
- OpenCV (`cv2`)
- NumPy
- PyQt5
- PySerial

Installation des dépendances :

```bash
pip install kivy opencv-python numpy pyqt5 pyserial
```

## Lancement

```bash
python SimBeach.py
```

## Structure du projet

```
SimBeach/
├── SimBeach.py                 # Point d'entrée principal
├── ecrans/                     # Logique des écrans
│   ├── accueil_screen.py       # Écran d'accueil
│   ├── simulation_screen.py    # Mode simulation
│   ├── jeu_screen.py           # Mode jeu
│   ├── robot_screen.py         # Connexion robot
│   ├── options_screen.py       # Paramètres
│   └── classe.py               # Composants UI personnalisés
├── structure/                  # Fichiers de layout Kivy (.kv)
├── variables/                  # Gestion de la configuration
│   ├── config_manager.py
│   └── config.json
└── assets/                     # Médias (vidéos, images, icônes)
```

## Configuration

Les paramètres sont sauvegardés dans `variables/config.json` :

| Paramètre          | Description                        | Défaut   |
|--------------------|------------------------------------|----------|
| `nb_dechets`       | Nombre de déchets générés          | 20       |
| `largeur_plage`    | Largeur utile de la plage (%)      | 100      |
| `niveau_maree`     | Niveau de marée (0 à 3)            | 0        |
| `vitesse_simulation` | Multiplicateur de vitesse         | 1        |
| `ip`               | Adresse IP du robot (Wi-Fi)        | 192.168.0.1 |
| `port_usb`         | Port série USB                     | COM3     |
| `port_wifi`        | Port Wi-Fi                         | 8080     |

## Parcours personnalisé

Il est possible de charger un script Python définissant un algorithme de parcours custom. Le script doit exposer une fonction compatible avec le système de coordonnées en ratios (0.0 à 1.0) utilisé par la simulation.

## Technologies

- [Kivy](https://kivy.org/) — framework GUI Python multi-plateforme
- [OpenCV](https://opencv.org/) — analyse vidéo pour la détection d'eau
- [NumPy](https://numpy.org/) — calculs matriciels
- [PySerial](https://pythonhosted.org/pyserial/) — communication USB

## Auteurs

Projet réalisé dans le cadre d'un tutoriel / projet pédagogique — SALLAH & RAMOTH (2025).
