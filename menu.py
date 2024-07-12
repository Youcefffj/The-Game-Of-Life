import pygame, sys
import subprocess
import os
from button import Button_Menu


jeu = os.path.abspath("jeu.py")
aleavar = "alea"

chemin_python = os.path.abspath(sys.executable)

pygame.init()

SCREEN = pygame.display.set_mode((1280, 720))
pygame.display.set_caption("Menu Game Of Life 2")

BG = pygame.image.load("assets/fond.jpg")
BG = pygame.transform.scale(BG,(1280,720))

def get_font(size):
    return pygame.font.Font("assets/font.ttf", size)


def options():
    while True:

        regles = [
            "Règles du jeu",
            "Space: pause/play -- clique gauche: créer une cellule",
            "Flèche haut/bas: régles la vitesse -- S: Sauvegarder",
            "",
            "- Survie : Une cellule vivante avec deux ou trois voisines ",
            "vivantes reste vivante à la génération suivante.",
            "- Naissance : Une cellule morte avec exactement trois voisines",
            " vivantes devient vivante à la génération suivante.",
            "- Mort par solitude : Une cellule vivante avec moins de deux voisines",
            " vivantes meurt par solitude à la génération suivante.",
            "- Mort par étouffement : Une cellule vivante avec plus de trois voisines",
            " vivantes meurt d'étouffement à la génération suivante."
        ]


        OPTIONS_MOUSE_POS = pygame.mouse.get_pos()

        SCREEN.fill("white")

        OPTIONS_TEXT = get_font(45).render("Rules and Commands", True, "Black")
        OPTIONS_RECT = OPTIONS_TEXT.get_rect(center=(640, 50))

        SCREEN.blit(OPTIONS_TEXT, OPTIONS_RECT)

        OPTIONS_BACK = Button_Menu(image=None, pos=(640, 680),
                              text_input="BACK", font=get_font(75), base_color="Black", hovering_color="Green")

        OPTIONS_BACK.changeColor(OPTIONS_MOUSE_POS)
        OPTIONS_BACK.update(SCREEN)

        y=120
        for regle in regles:
            texte = get_font(15).render(regle, True, "Black")
            rect = texte.get_rect(center=(1280 // 2, y))
            SCREEN.blit(texte, rect)
            y += 40

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if OPTIONS_BACK.checkForInput(OPTIONS_MOUSE_POS):
                    main_menu()

        pygame.display.update()

def main_menu():
    while True:
        SCREEN.blit(BG, (0, 0))

        MENU_MOUSE_POS = pygame.mouse.get_pos()

        MENU_TEXT = get_font(75).render("Game Of Life", True, "yellow")
        MENU_RECT = MENU_TEXT.get_rect(center=(640, 50))

        PLAY_BUTTON = Button_Menu(image=pygame.image.load("assets/Play Rect.png"), pos=(640, 150),
                             text_input="PLAY", font=get_font(65), base_color="#d7fcd4", hovering_color="purple")
        LOAD_BUTTON = Button_Menu(image=pygame.image.load("assets/Options Rect.png"), pos=(640, 275),
                             text_input="LOAD GAME", font=get_font(65), base_color="#d7fcd4", hovering_color="purple")
        BONUS_BUTTON = Button_Menu(image=pygame.image.load("assets/Options Rect.png"), pos=(640, 400),
                              text_input="RANDOM", font=get_font(65), base_color="#d7fcd4",hovering_color="purple")
        OPTIONS_BUTTON = Button_Menu(image=pygame.image.load("assets/Options Rect.png"), pos=(640, 525),
                                text_input="OPTIONS", font=get_font(65), base_color="#d7fcd4", hovering_color="purple")
        QUIT_BUTTON = Button_Menu(image=pygame.image.load("assets/Quit Rect.png"), pos=(640, 650),
                             text_input="QUIT", font=get_font(65), base_color="#d7fcd4", hovering_color="purple")

        SCREEN.blit(MENU_TEXT, MENU_RECT)

        for button in [PLAY_BUTTON, LOAD_BUTTON, BONUS_BUTTON, OPTIONS_BUTTON, QUIT_BUTTON]:
            button.changeColor(MENU_MOUSE_POS)
            button.update(SCREEN)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if PLAY_BUTTON.checkForInput(MENU_MOUSE_POS):
                    subprocess.run([chemin_python, jeu], check=True)
                elif LOAD_BUTTON.checkForInput(MENU_MOUSE_POS):
                    files_svg = []
                    save_files = [f for f in os.listdir() if f.endswith('.txt')]
                    print("Grilles sauvegardées disponibles :")
                    for file in (save_files):
                        files_svg.append(f"{file}")
                    print(files_svg)

                    choice = input("Saisissez le nom de la grille à charger : ")
                    while True :
                        for i in range (len(files_svg)):
                            if files_svg[i] == choice :
                                aleavar = choice
                                subprocess.run([chemin_python, jeu, aleavar], check=True)
                        choice = input("Saisissez un nom valide : ")


                    pass
                elif BONUS_BUTTON.checkForInput(MENU_MOUSE_POS):
                    aleavar = "alea"
                    subprocess.run([chemin_python, jeu, aleavar], check=True)
                    pass
                elif OPTIONS_BUTTON.checkForInput(MENU_MOUSE_POS):
                    options()
                elif QUIT_BUTTON.checkForInput(MENU_MOUSE_POS):
                    pygame.quit()
                    sys.exit()

        pygame.display.update()


main_menu()