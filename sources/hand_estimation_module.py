import cv2
import mediapipe as mp

# DEBUG_IMAGE = True: permet d'afficher les images renvoyées par la caméra
DEBUG_IMAGE = False


class PoseDetect:
    """
    détecte la position d'une main
    """
    def __init__(self, mode=False, num_hands=1, complexite=1, min_detect_conf=0.5, max_detect_conf=0.5):
        self.mode = mode
        self.num_hands = num_hands
        self.complexite = complexite
        self.min_detect_conf = min_detect_conf
        self.max_detect_conf = max_detect_conf

        self.mp_draw = mp.solutions.drawing_utils
        self.mp_hands = mp.solutions.hands
        self.hands = self.mp_hands.Hands(self.mode, self.num_hands,
                                         self.complexite, self.min_detect_conf, self.max_detect_conf)

    def find_pose(self, img):
        """
        fonction qui sert a trouver la position d'un point de la main
        :param img: une image de la vidéo de la caméra
        :return: l'image, la position du point y et la position du point x
        """
        img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        results = self.hands.process(img_rgb)
        h, w, c = img.shape
        pose_point_y = -100
        pose_point_x = -100
        if results.multi_hand_landmarks:
            for hand_lm in results.multi_hand_landmarks:
                pose_point_y = hand_lm.landmark[self.mp_hands.HandLandmark.MIDDLE_FINGER_MCP].y * h
                pose_point_x = hand_lm.landmark[self.mp_hands.HandLandmark.MIDDLE_FINGER_MCP].x * w
                if DEBUG_IMAGE:
                    cv2.circle(img, (int(pose_point_x), int(pose_point_y)), 5, (255, 255, 0), cv2.FILLED)
        return img, pose_point_y, pose_point_x, w


def main(cap, detecteur):
    """
    fonction principale de hand_estimation_module.py qui sert a détécter la positions des mains des joueurs
    elle attribue la valeur de y par rapport à la valeur des x
    :param cap: la vidéo de la caméra utilisée
    :param detecteur: la détéction de la main
    :return: les valeurs des y d'un point des mains des deux joueurs
    """
    success, img = cap.read()
    h, w, c = img.shape
    moitie = w // 2
    detec_left = detecteur.find_pose(img[:, :moitie])
    detec_right = detecteur.find_pose(img[:, moitie:])
    img_left = detec_left[0]
    img_right = detec_right[0]
    right_y = detec_right[1]
    left_y = detec_left[1]

    if DEBUG_IMAGE:
        cv2.imshow("Joueur droit", img_left)
        cv2.imshow("Joueur gauche", img_right)
    cv2.waitKey(1)
    return int(left_y), int(right_y)
