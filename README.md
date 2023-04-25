# Pyng-Pong

Pyng Pong est une version en python du fameux jeu pong, mais avec la particularité d'être 100% controllé par la détection de la main.

# Pré-requis

## Modules requis :

 * mediapipe
 * pygame
 * opencv-python

`commande pour les installer : 'pip install mediapipe pygame opencv-python'`

## Matériel requis :
 
* une caméra

# Protocole d'utilisation

1. Lancer le fichier 'main_code.py' situé dans le répertoire 'sources';
2. Appuyer sur la touche `<Entrée>` pour démarrer une partie, ou `<Échap>` pour quitter;
3. Si la point à côté de la raquette est bleu, la main est détectée. S'il est rouge, elle ne l'est pas.

# Informations suplémentaires

 * Dans le fichier 'hand_estimation_module.py' situé dans le répertoire 'sources', attribuer la valeur `True` à `DEBUG_IMAGE` permet d'afficher les images de la caméra.
 * Dans le fichier 'pong.py' situé dans le répertoire 'sources', attribuer la valeur `True` à `DEBUG_HITBOX` permet d'afficher des points représentant les masques de collision des deux raquettes et de la balle.
