import pygame
pygame.init()
pygame.mixer.init()

# DEBUG_HITBOX = True: permet d'afficher, à l'aide de points verts, la hitbox des paddles et de la balle
#                      permet de vérifier que l'image utilisée soit bien à la même position
DEBUG_HITBOX = False


left_score = 0
right_score = 0
WIDTH, HEIGHT = 1920, 1080
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Pyng Pong")

FPS = 120

CYAN = (51, 51, 255)
GREEN = (0, 255, 0)
BLUE = (12, 99, 198)
RED = (255, 0, 0)
PADDLE_WIDTH, PADDLE_HEIGHT = 20, HEIGHT / 7

SCORE_FONT = pygame.font.SysFont("comicsans", 50)
WINNING_SCORE = 5

left_paddle_img = pygame.image.load("images/red_paddle.png")
right_paddle_img = pygame.image.load("images/blue_paddle.png")
background_img = pygame.image.load("images/terrain_pyng_pong.jpg").convert()
background_img = pygame.transform.scale(background_img, (WIDTH, HEIGHT))
ball_img = pygame.image.load("images/balle.png")
trophee_bleu = pygame.image.load("images/win_bleu.png")
trophee_rouge = pygame.image.load("images/win_rouge.png")
pygame.mixer.music.load("sons/point.mp3")


class Paddle:
    """
    classe servant à définir les paddles
    """
    VEL = 30

    def __init__(self, x, y, width, height, is_left):
        self.x = x
        self.y = self.original_y = y
        self.width = width
        self.height = height
        self.is_left = is_left

    def draw(self, win):
        """
        fonction gérant l'affichage du paddle
        :param win: fenêtre sur laqualle il doit être affiché
        """
        if self.is_left:
            win.blit(left_paddle_img, (60 + self.x, self.y))
            if DEBUG_HITBOX:
                pygame.draw.circle(win, GREEN, (60 + self.x, self.y), 5)
                pygame.draw.circle(win, GREEN, (60 + self.x + self.width, self.y + self.height), 5)
        else:
            win.blit(right_paddle_img, (self.x, self.y))
            if DEBUG_HITBOX:
                pygame.draw.circle(win, GREEN, (self.x, self.y), 5)
                pygame.draw.circle(win, GREEN, (self.x + self.width, self.y + self.height), 5)

    def move(self, up=True):
        """
        fonction gérant le déplacement du paddle
        :param up: booléen, définit si il doit se déplacer vers le haut ou non
        """
        if up:
            self.y -= self.VEL
        else:
            self.y += self.VEL

    def reset(self):
        """
        fonction gérant la mise à zéro du paddle, utilisée si un joueur à marqué
        """
        self.y = self.original_y


class Ball:
    """
    classe servant à définir la balle
    """
    MAX_VEL = 30

    def __init__(self, x, y, radius):
        self.x = self.original_x = x
        self.y = self.original_y = y
        self.radius = radius
        self.x_vel = 15
        self.y_vel = 0
        self.impact_counter = 0

    def draw(self, win):
        """
        fonction gérant l'affichage de la balle
        :param win: fenêtre sur laquelle la balle doit être affichée
        """
        win.blit(ball_img, (self.x, self.y))
        if DEBUG_HITBOX:
            pygame.draw.circle(win, GREEN, (self.x, self.y), 5)
            pygame.draw.circle(win, GREEN, (self.x + self.radius, self.y + self.radius), 5)

    def move(self):
        """
        fonction gérant les déplacements de la balle
        """
        self.x += self.x_vel
        self.y += self.y_vel

    def reset(self):
        """
        fonction gérant la mise à zéro de la balle, utilisée si un joueur à marqué
        """
        self.x = self.original_x
        self.y = self.original_y
        self.y_vel = 0
        self.x_vel *= -1
        self.impact_counter = 0


class Point:
    """
    classe servant à définir les points de position de la main
    """

    def __init__(self, x, y, rad):
        self.x = x
        self.y = y
        self.rad = rad
        self.pose = -1

    def draw(self, win):
        """
        méthode gérant l'affichage du point
        :param win: fenêtre sur laquelle le point doit être affiché
        """
        color = self.color()
        pygame.draw.circle(win, color, (self.x, self.y), self.rad)

    def move(self, pose):
        """
        fonction gérant le déplacement du point
        :param pose: valeur représentant le point de l'axe des ordonnées de la main
        """
        self.pose = pose
        if pose >= 0:
            self.y = pose

    def color(self):
        """
        fonction permettant de changer la couleur du point en fonction de si la main est détectée ou non
        :return: la couleur correspondante
        """
        if self.pose >= 0:
            return BLUE
        return RED


def draw(win, paddles, points, ball, left_score_int, right_score_int, col, score_font):
    """
    fonction gérant l'affichage des différents éléments sur la fenêtre
    :param win: fenêtre sur laquelle seront déssinés les éléments
    :param paddles: liste contenant les différents paddles à dessiner, objets de la calle Paddle
    :param points: liste contenant les différents points à dessiner, objets de la class Point
    :param ball: objet de la classe Ball
    :param left_score_int: valeur correspondante au score du joueur gauche
    :param right_score_int: valeur correspondante au score du joueur droit
    :param col: couleur des scores des joueurs
    :param score_font: police des scores des joueurs
    """
    win.blit(background_img, (0, 0))

    left_score_text = score_font.render(f"{left_score_int}", 1, col)
    right_score_text = score_font.render(f"{right_score_int}", 1, col)
    win.blit(left_score_text, (WIDTH // 4 - left_score_text.get_width() // 2, -15))
    win.blit(right_score_text, (WIDTH * (3 / 4) -
                                right_score_text.get_width() // 2, -15))

    for paddle in paddles:
        paddle.draw(win)

    for point in points:
        point.draw(win)

    ball.draw(win)
    pygame.display.update()


def handle_collision(ball, left_paddle, right_paddle):
    """
    fonction gérant les collisions entre la balle et les parois ainsi qu'entre la balle et les paddles
    :param ball: objet de la classe Ball
    :param left_paddle: objet de la classe Paddle
    :param right_paddle: objet de la classe Paddle
    """
    if ball.y + ball.radius >= HEIGHT:
        ball.y_vel *= -1
    elif ball.y <= 0:
        ball.y_vel *= -1

    # paddle gauche
    if ball.x_vel < 0:
        if ball.y <= left_paddle.y <= ball.y + ball.radius \
                or left_paddle.y <= ball.y <= left_paddle.y + left_paddle.height:
            if ball.x - ball.radius <= left_paddle.x + left_paddle.width:
                ball.x_vel *= -1
                middle_y = left_paddle.y + left_paddle.height / 2 - 3.75
                difference_in_y = middle_y - (ball.y + ball.radius / 2)
                reduction_factor = (left_paddle.height / 2) / ball.MAX_VEL
                y_vel = difference_in_y / reduction_factor
                ball.y_vel = -1 * y_vel
                if ball.impact_counter == 5:
                    ball.x_vel += 2
                    ball.impact_counter = 0
                else:
                    ball.impact_counter += 1

    # paddle droit
    elif ball.x_vel > 0:
        if ball.y <= right_paddle.y <= ball.y + ball.radius \
                or right_paddle.y <= ball.y <= right_paddle.y + right_paddle.height:
            if ball.x + ball.radius >= right_paddle.x:
                ball.x_vel *= -1
                middle_y = right_paddle.y + right_paddle.height / 2
                difference_in_y = middle_y - (ball.y + ball.radius // 2)
                reduction_factor = (right_paddle.height / 2) / ball.MAX_VEL
                y_vel = difference_in_y / reduction_factor
                ball.y_vel = -1 * y_vel
                if ball.impact_counter == 5:
                    ball.x_vel += 2
                    ball.impact_counter = 0
                else:
                    ball.impact_counter += 1


def handle_paddle_movement(left_paddle, right_paddle, left_point, right_point):
    """
    fonction gérant le déplacement des paddles
    :param left_paddle: objet de la classe Paddle
    :param right_paddle: objet de la classe Paddle
    :param left_point: objet de la classe Point, sert à indiquer la position vers laquelle left_paddle doit se diriger
    :param right_point: objet de la classe Point, sert à indiquer la position vers laquelle right_paddle doit se diriger
    """
    if left_point.pose >= 0:
        if left_paddle.y > left_point.y and left_paddle.y - left_paddle.VEL >= 0:
            left_paddle.move(up=True)
        if left_paddle.y < left_point.y and left_paddle.y + left_paddle.VEL + left_paddle.height <= HEIGHT:
            left_paddle.move(up=False)

    if right_point.pose >= 0:
        if right_paddle.y > right_point.y and right_paddle.y - right_paddle.VEL >= 0:
            right_paddle.move(up=True)
        if right_paddle.y < right_point.y and right_paddle.y + right_paddle.VEL + right_paddle.height <= HEIGHT:
            right_paddle.move(up=False)


def main(left_paddle, right_paddle, left_point, right_point, ball, left_y, right_y):
    """
    fonction permettant de faire tourner le jeu
    :param left_paddle: objet de la classe Paddle, représente la raquette gauche
    :param right_paddle: objet de la classe Paddle, représente la raquette droite
    :param left_point: objet de la classe Point, représente le point de la main gauche
    :param right_point: objet de la classe Point, représente le point de la main droite
    :param ball: objet de la classe Ball, représente la balle du jeu
    :param left_y: valeur de la main gauche indiquant jusqu'où la raquette gauche doit se déplacée,
                    n'est pas prise en compte dans le programme si < 0
    :param right_y: valeur de la main droite indiquant jusqu'où la raquette droite doit se déplacée,
                    n'est pas prise en compte dans le programme si < 0
    :return: booléen indiquant si la partie s'est terminée ou non
    """
    global left_score
    global right_score
    pygame.time.Clock().tick(FPS)
    draw(WIN, [left_paddle, right_paddle], [left_point, right_point], ball, left_score, right_score, BLUE, SCORE_FONT)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            break

    left_point.move(left_y * 2.25)
    right_point.move(right_y * 2.25)
    handle_paddle_movement(left_paddle, right_paddle, left_point, right_point)
    ball.move()
    handle_collision(ball, left_paddle, right_paddle)

    if ball.x < -55:
        right_score += 1
        ball.reset()
        pygame.mixer.music.play(1)
        left_paddle.reset()
        right_paddle.reset()
        ball.impact_counter = 0
        ball.x_vel = -12
        pygame.time.delay(800)

    elif ball.x > WIDTH + 5:
        left_score += 1
        ball.reset()
        pygame.mixer.music.play(1)
        left_paddle.reset()
        right_paddle.reset()
        ball.impact_counter = 0
        ball.x_vel = 12
        pygame.time.delay(800)

    won = False
    if left_score >= WINNING_SCORE:
        won = True
        WIN.blit(trophee_rouge, (681, 270))
        pygame.time.delay(800)
    elif right_score >= WINNING_SCORE:
        won = True
        WIN.blit(trophee_bleu, (681, 270))
        pygame.time.delay(800)

    if won:
        return False
    return True
