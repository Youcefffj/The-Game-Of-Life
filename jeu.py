import time
import pygame
import numpy as np
from Sauvegarde_Chargement import sauvegarder_grille, charger_grille
import os
import sys
import subprocess
import matplotlib.pyplot as plt
import pygame.image
#import timeit
#from functools import partial

chemin_python = os.path.abspath(sys.executable)

pygame.init()
screen = pygame.display.set_mode((1280, 720))
plt.ion()
print(os.getcwd())

size = 15
pygame.init()
screen = pygame.display.set_mode((1280, 720))
switch = 0
switch2 = 0
COLOR_BG = (0, 0, 0)
COLOR_GRID = (125, 125, 125)

COLOR_ALIVE = (147, 112, 219)
GRAPH_SIZE = (400, 210)


#courbe et timer
chrono = time.time()
CourbeTime = 2
CellulesTemps = []


speed = 0
speed1 = 0.001
speed2 = 0.05
speed3 = 0.10
dead_cells = 0



def count_alive_cells(cells):
    alive_count = 0
    for row in range(cells.shape[0]):
        for col in range(cells.shape[1]):
            if cells[row, col] == 1:
                alive_count += 1
    return alive_count

def courbe_de_vie(cells):
    celluletemps = count_alive_cells(cells)
    CellulesTemps.append(celluletemps)

    if len(CellulesTemps) % 1 == 0:
        plt.clf()
        plt.plot(CellulesTemps, label='Cellules en vie')
        plt.savefig('graph.png')
        graph_surface = pygame.image.load('graph.png')
        graph_surface = pygame.transform.scale(graph_surface, GRAPH_SIZE)

        return graph_surface

def initialiser_graphique():
    plt.xlabel('Itérations')
    plt.ylabel('Nombre de cellules en vie')
    plt.title('Évolution du nombre de cellules en vie au fil du temps')
    plt.legend()
    plt.savefig('graph.png')
    graph_surface = pygame.image.load('graph.png')
    graph_surface = pygame.transform.scale(graph_surface, GRAPH_SIZE)

    return graph_surface

class Image_Game():
    def __init__(self, x, y, image, scale):
        width = image.get_width()
        height = image.get_height()
        self.image = pygame.transform.scale(image, (int(width * scale), int(height * scale)))
        self.rect = self.image.get_rect()
        self.rect.topleft = (x,y)
    def draw (self):
         screen.blit(self.image,(self.rect.x,self.rect.y))

def update(screen, cells, size, with_progress=False ):
    global dead_cells
    updated_cells = np.zeros((cells.shape[0], cells.shape[1]))

    for row, col in np.ndindex(cells.shape):
        alive = np.sum(cells[row - 1:row + 2, col - 1:col + 2]) - cells[row, col]
        color = COLOR_BG if cells[row, col] == 0 else COLOR_ALIVE

        if cells[row, col] == 1:
            if alive < 2 or alive > 3:
                if with_progress:
                    color = COLOR_BG
                    dead_cells += 1
            elif 2 <= alive <= 3:
                updated_cells[row, col] = 1
                if with_progress:
                    color = COLOR_ALIVE
        else:
            if alive == 3:
                updated_cells[row, col] = 1
                if with_progress:
                    color = COLOR_ALIVE
        pygame.draw.rect(screen, color, (col * size, row * size, size - 1, size - 1))
    return updated_cells

def structure_toad (screen, cells, size):
    global switch
    if pygame.mouse.get_pressed()[2]:
        pos = pygame.mouse.get_pos()
        if (pos[0] <= 740 and pos[1] <= 740):
            cells[(pos[1] // size), (pos[0] // size) - 1] = 1
            cells[(pos[1] // size) + 1, (pos[0] // size) - 1] = 1
            cells[(pos[1] // size) + 2, (pos[0] // size)] = 1
            cells[(pos[1] // size), (pos[0] // size) + 2] = 1
            cells[(pos[1] // size) + 1, (pos[0] // size) + 2] = 1
            cells[(pos[1] // size) - 1, (pos[0] // size) + 1] = 1
            switch = 0

    update(screen, cells, size)

def structure_boat(screen, cells, size):
    global switch
    if pygame.mouse.get_pressed()[2]:
        pos = pygame.mouse.get_pos()
        if (pos[0] <= 740 and pos[1] <= 740):
            cells[(pos[1] // size), (pos[0] // size)] = 1
            cells[(pos[1] // size) + 1, (pos[0] // size)] = 1
            cells[(pos[1] // size), (pos[0] // size) + 1] = 1
            cells[(pos[1] // size) +1, (pos[0] // size) + 2] = 1
            cells[(pos[1] // size) + 2, (pos[0] // size) + 1] = 1
            switch = 0

    update(screen, cells, size)
def structure_glider(screen, cells, size):
    global switch
    if pygame.mouse.get_pressed()[2]:
        pos = pygame.mouse.get_pos()
        if (pos[0] <= 740 and pos[1] <= 740):
            cells[(pos[1] // size), (pos[0] // size)] = 1
            cells[(pos[1] // size), (pos[0] // size) - 1] = 1
            cells[(pos[1] // size - 1), (pos[0] // size) - 2] = 1
            cells[(pos[1] // size) - 1, (pos[0] // size)] = 1
            cells[(pos[1] // size) -2, (pos[0] // size) ] = 1
            switch = 0
    update(screen, cells, size)

def structure_glider_gun(screen, cells, size):
    global switch
    if pygame.mouse.get_pressed()[2]:
        pos = pygame.mouse.get_pos()
        if (pos[0] <= 740 and pos[1] <= 740):
            cells[(pos[1] // size), (pos[0] // size)] = 1
            cells[(pos[1] // size), (pos[0] // size) - 1] = 1
            cells[(pos[1] // size) + 1, (pos[0] // size) - 1] = 1
            cells[(pos[1] // size) - 1, (pos[0] // size) - 1] = 1
            cells[(pos[1] // size) - 2, (pos[0] // size) - 2] = 1
            cells[(pos[1] // size) + 2, (pos[0] // size) - 2] = 1
            cells[(pos[1] // size), (pos[0] // size) - 3] = 1
            cells[(pos[1] // size) - 3, (pos[0] // size) - 4] = 1
            cells[(pos[1] // size) - 3, (pos[0] // size) - 5] = 1
            cells[(pos[1] // size) - 2, (pos[0] // size) - 6] = 1
            cells[(pos[1] // size) + 3, (pos[0] // size) - 4] = 1
            cells[(pos[1] // size) + 3, (pos[0] // size) - 5] = 1
            cells[(pos[1] // size) + 2, (pos[0] // size) - 6] = 1
            cells[(pos[1] // size) + 1, (pos[0] // size) - 7] = 1
            cells[(pos[1] // size) - 1, (pos[0] // size) - 7] = 1
            cells[(pos[1] // size) , (pos[0] // size) - 7] = 1
            cells[(pos[1] // size), (pos[0] // size) - 16] = 1
            cells[(pos[1] // size), (pos[0] // size) - 17] = 1
            cells[(pos[1] // size) - 1, (pos[0] // size) - 16] = 1
            cells[(pos[1] // size) - 1, (pos[0] // size) - 17] = 1
            cells[(pos[1] // size) - 1, (pos[0] // size) + 3] = 1
            cells[(pos[1] // size) - 2, (pos[0] // size) + 3] = 1
            cells[(pos[1] // size) - 3, (pos[0] // size) + 3] = 1
            cells[(pos[1] // size) - 1, (pos[0] // size) + 4] = 1
            cells[(pos[1] // size) - 2, (pos[0] // size) + 4] = 1
            cells[(pos[1] // size) - 3, (pos[0] // size) + 4] = 1
            cells[(pos[1] // size) - 4, (pos[0] // size) + 5] = 1
            cells[(pos[1] // size) - 4, (pos[0] // size) + 7] = 1
            cells[(pos[1] // size) - 5, (pos[0] // size) + 7] = 1
            cells[(pos[1] // size), (pos[0] // size) + 5] = 1
            cells[(pos[1] // size), (pos[0] // size) + 7] = 1
            cells[(pos[1] // size) + 1, (pos[0] // size) + 7] = 1
            cells[(pos[1] // size) - 3, (pos[0] // size) + 17] = 1
            cells[(pos[1] // size) - 3, (pos[0] // size) + 18] = 1
            cells[(pos[1] // size) - 2, (pos[0] // size) + 17] = 1
            cells[(pos[1] // size) - 2, (pos[0] // size) + 18] = 1

            switch = 0
    update(screen, cells, size)



def random_grid(cells):
    for row in range(cells.shape[0]):
        for col in range(cells.shape[1]):
            cells[row, col] = np.random.choice([0, 1])


def main():
    global switch,switch2,speed
    cells = np.zeros((50, 50))
    if len(sys.argv) > 1:
        votre_variable = sys.argv[1]
        if votre_variable == "alea":
            random_grid(cells)
        else :
            cells = charger_grille(votre_variable,cells)
    screen.fill(COLOR_GRID)
    font = pygame.font.Font(None, 36)
    update(screen, cells, size)
    skull_img = pygame.image.load("assets/skull.png")
    skull = Image_Game(800, 150, skull_img, 0.1)
    heart_img = pygame.image.load("assets/heart.png")
    heart = Image_Game(800, 60, heart_img, 0.015)
    sablier_img = pygame.image.load("assets/sablier.png")
    sablier = Image_Game(800, 250, sablier_img, 0.3)
    
    speed_up_img = pygame.image.load("assets/speed_up.png")
    speed_up = Image_Game(1130, 60, speed_up_img, 0.5)
    speed_up_rect = speed_up_img.get_rect(topleft=(1130,60))
    speed_down_img = pygame.image.load("assets/speed_down.png")
    speed_down = Image_Game(1055, 60, speed_down_img, 0.5)
    speed_down_rect = speed_down_img.get_rect(topleft=(1055,60))
    toad_img = pygame.image.load("assets/Toad.png")
    toad = Image_Game(920, 345, toad_img, 0.5)
    toad_rect = toad_img.get_rect(topleft=(920,345))
    boat_img = pygame.image.load("assets/Boat.png")
    boat = Image_Game(990, 345, boat_img, 0.5)
    boat_rect = boat_img.get_rect(topleft=(990, 345))
    glider_img = pygame.image.load("assets/glider.png")
    glider = Image_Game(1050, 345, glider_img, 0.5)
    glider_rect = boat_img.get_rect(topleft=(1050, 345))
    glider_gun_img = pygame.image.load("assets/glider_gun.png")
    glider_gun = Image_Game(870, 415, glider_gun_img, 1)
    glider_gun_rect = boat_img.get_rect(topleft=(900, 430))
    pygame.display.flip()
    pygame.display.update()

    running = False
    temps_actuel = time.time()
    chrono_deduit = 0
    speed = speed2
    tempo = 0

    graph_surface = None

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return

            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    running = not running
                    if running:
                        update(screen, cells, size, with_progress=True)
                        speed_up.draw()
                        speed_down.draw()
                        glider.draw()
                        glider_gun.draw()
                        toad.draw()
                        boat.draw()
                        skull.draw()
                        sablier.draw()
                        heart.draw()
                elif event.key == pygame.K_q:  # Touche "Q" pour quitter
                    running = False
                    pygame.quit()
                    subprocess.run([chemin_python, "menu.py"], check=True)


                elif event.key == pygame.K_s:  # Sauvegarde
                    nom_fichier = input("Entrez un nom pour la sauvegarde : ")  # Demande un nom pour la sauvegarde
                    sauvegarder_grille(cells, f'{nom_fichier}.txt')
                    print("Grille sauvegardée avec succès !")

                    update(screen, cells, size)

            pos = pygame.mouse.get_pos()
            if pygame.mouse.get_pressed()[0]:
                pos = pygame.mouse.get_pos()
                if (pos[0] <= 740 and pos[1] <= 740 and switch == 0):
                    cells[pos[1] // size, pos[0] // size] = 1
                if not running :
                    if toad_rect.collidepoint(pos):
                        switch = 1
                    if boat_rect.collidepoint(pos):
                        switch = 2
                    if glider_rect.collidepoint(pos):
                        switch = 3
                    if glider_gun_rect.collidepoint(pos):
                        switch = 4
                if speed_up_rect.collidepoint(pos):
                    if speed == speed2:
                        speed = speed1
                    if speed == speed3:
                        speed = speed2
                if speed_down_rect.collidepoint(pos):
                    if speed == speed1:
                        speed = speed2
                    if speed == speed2:
                        speed = speed3
                update(screen, cells, size)
                speed_up.draw()
                speed_down.draw()
                toad.draw()
                boat.draw()
                glider.draw()
                glider_gun.draw()
                skull.draw()
                heart.draw()
                sablier.draw()
            if switch == 1:
                structure_toad(screen,cells,size)
            elif switch == 2:
                structure_boat(screen,cells,size)
            elif switch == 3:
                structure_glider(screen,cells,size)
            elif switch == 4:
                structure_glider_gun(screen,cells,size)

        screen.fill(COLOR_GRID)

        if running:
            cells = update(screen, cells, size, with_progress=True)
            speed_up.draw()
            speed_down.draw()
            toad.draw()
            boat.draw()
            glider.draw()
            skull.draw()
            heart.draw()
            sablier.draw()
            glider_gun.draw()
            # tableau de vie pour courbe
            temps_fin = time.time()
            ecart_temp = temps_fin - temps_actuel
            #incrementation des cellules vivantes dans le tableau toutes les 2sec
            if ecart_temp > 2:
                temps_actuel = time.time()
                graph_surface = courbe_de_vie(cells)

        else:
            update(screen, cells, size)
            speed_up.draw()
            speed_down.draw()
            toad.draw()
            boat.draw()
            glider.draw()
            skull.draw()
            heart.draw()
            glider_gun.draw()
            sablier.draw()

        #affichage du graph cellules vivantes
        if graph_surface:
            screen.blit(graph_surface, (800, 500))
            pygame.display.flip()

        alive_cells_count = count_alive_cells(cells)
        chrono_fin = time.time()
        chrono_temp = chrono_fin - chrono

        #temporisation du timer en pause
        if not running:
            chrono_deduit = chrono_temp - tempo
        else:
            tempo = chrono_temp - chrono_deduit

        text = font.render(f"Alive Cells: {alive_cells_count}", True, (255, 255, 255))
        screen.blit(text, (890, 95))
        text = font.render(f"Dead Cells: {dead_cells}", True, (255, 255, 255))
        screen.blit(text, (890, 190))
        temps_virgule = round(chrono_temp - chrono_deduit, 2)
        textTime = font.render(f"Time: {temps_virgule}", True, (255, 255, 255))
        screen.blit(textTime, (890, 285))

        pygame.display.flip()
        time.sleep(speed)

if __name__ == '__main__':
    main()
