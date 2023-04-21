import hand_estimation_module
import pong
import cv2
import pygame

pygame.init()
pygame.mixer.init()

WIDTH, HEIGHT = 1920, 1080
PADDLE_WIDTH, PADDLE_HEIGHT = 20, 100
BALL_RADIUS = 50
musique_fond = pygame.mixer.Sound("sons/fond.mp3")


def main():
    """
    fonction principale du programme, met en lien les fonctions 'main' de 'pong.py' et 'hand_estimation_module.py'
    """
    cap = cv2.VideoCapture(0)
    assert cap.read()[0] is True, 'Une caméra doit être branchée.'
    # -----hand_estimation_module
    detecteur = hand_estimation_module.PoseDetect()

    # -----Pyng Pong
    left_paddle = pong.Paddle(-58, HEIGHT / 2 - PADDLE_HEIGHT / 2,
                              PADDLE_WIDTH, PADDLE_HEIGHT, is_left=True)
    right_paddle = pong.Paddle(WIDTH - 2 - PADDLE_WIDTH, HEIGHT / 2 - PADDLE_HEIGHT / 2,
                               PADDLE_WIDTH, PADDLE_HEIGHT, is_left=False)
    left_point = pong.Point(left_paddle.x + left_paddle.width + 72, left_paddle.y, 5)
    right_point = pong.Point(right_paddle.x - 10, right_paddle.y, 5)
    ball = pong.Ball(WIDTH / 2 - BALL_RADIUS / 2, HEIGHT / 2 - BALL_RADIUS / 2, BALL_RADIUS)

    jouer = True
    musique_fond.play()
    while jouer:
        hand_tracker = hand_estimation_module.main(cap, detecteur)
        right_y = hand_tracker[0]
        left_y = hand_tracker[1]
        jouer = pong.main(left_paddle, right_paddle, left_point, right_point, ball, left_y, right_y)
    musique_fond.stop()
