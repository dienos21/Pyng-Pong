# Documentation du jeu Pyng Pong

## main_code.py
* menu()  

affiche le menu du jeu  
  
## fusion.py
* main()  

fonction principale du programme, met en lien les fonctions 'main' de 'pong.py' et 'hand_estimation_module.py'

## hand_estimation_module.py
* PoseDetect()  
détecte la position d'une main 

  * find_pose()  
  fonction qui sert a trouver la position d'un point de la main  
  `img` une image de la vidéo de la caméra  
  `return` l'image, la position du point y et la position du point x  
  
* main()  
fonction principale de hand_estimation_module.py qui sert a détécter la positions des mains des joueurs
elle attribue la valeur de y par rapport à la valeur des x  
`cap` la vidéo de la caméra utilisée  
`detecteur` la détéction de la main  
`return` les valeurs des y d'un point des mains des deux joueurs  

## pong.py
* Paddle()  
classe servant à définir les paddles  

  * draw()  
  fonction gérant l'affichage du paddle  
  `win` fenêtre sur laqualle il doit être affiché  
  
  * move()  
  fonction gérant le déplacement du paddle  
  `up` booléen, définit si il doit se déplacer vers le haut ou non  
  
  * reset()  
  fonction gérant la mise à zéro du paddle, utilisée si un joueur à marqué  
  
* Ball()  
classe servant à définir la balle  

  * draw()  
  fonction gérant l'affichage de la balle  
  `win` fenêtre sur laquelle la balle doit être affichée  
  
  * move()  
  fonction gérant les déplacements de la balle  
  
  * reset()  
  fonction gérant la mise à zéro de la balle, utilisée si un joueur à marqué  
  
* Point()  
classe servant à définir les points de position de la main  

  * draw()  
  méthode gérant l'affichage du point  
  `win` fenêtre sur laquelle le point doit être affiché  
  
  * move()  
  fonction gérant le déplacement du point  
  `pose` valeur représentant le point de l'axe des ordonnées de la main  
  
  * color()  
  fonction permettant de changer la couleur du point en fonction de si la main est détectée ou non  
  `return` la couleur correspondante  
  
* draw()  
fonction gérant l'affichage des différents éléments sur la fenêtre  
`win` fenêtre sur laquelle seront déssinés les éléments  
`paddles` liste contenant les différents paddles à dessiner, objets de la calle Paddle  
`points` liste contenant les différents points à dessiner, objets de la class Point  
`ball` objet de la classe Ball  
`left_score_int` valeur correspondante au score du joueur gauche  
`right_score_int` valeur correspondante au score du joueur droit  
`col` couleur des scores des joueurs  
`score_font` police des scores des joueurs  
    
* handle_collision()  
fonction gérant les collisions entre la balle et les parois ainsi qu'entre la balle et les paddles  
`ball` objet de la classe Ball  
`left_paddle` objet de la classe Paddle  
`right_paddle` objet de la classe Paddle  
    
* handle_paddle_movement()  
fonction gérant le déplacement des paddles  
`left_paddle` objet de la classe Paddle  
`right_paddle` objet de la classe Paddle  
`left_point` objet de la classe Point, sert à indiquer la position vers laquelle left_paddle doit se diriger  
`right_point` objet de la classe Point, sert à indiquer la position vers laquelle right_paddle doit se diriger  
    
* main()  
fonction permettant de faire tourner le jeu  
`left_paddle` objet de la classe Paddle, représente la raquette gauche  
`right_paddle` objet de la classe Paddle, représente la raquette droite  
`left_point` objet de la classe Point, représente le point de la main gauche  
`right_point` objet de la classe Point, représente le point de la main droite  
`ball` objet de la classe Ball, représente la balle du jeu  
`left_y` valeur de la main gauche indiquant jusqu'où la raquette gauche doit se déplacée  
n'est pas pris en compte dans le programme si < 0  
`right_y` valeur de la main droite indiquant jusqu'où la raquette droite doit se déplacée  
n'est pas pris en compte dans le programme si < 0  
`return` booléen indiquant si la partie s'est terminée ou non  
    
---

# Documentation des modules utilisés

* [mediapipe](https://developers.google.com/mediapipe)
* [pygame](https://he-arc.github.io/livre-python/pygame/index.html)
* [opencv-python](https://docs.opencv.org/4.x/d6/d00/tutorial_py_root.html)
