import copy
import math
import random
import time

import pygame
import socket
import threading
n = -1
players = []
screen = pygame.display.set_mode((800, 600))
pygame.font.init()
stone = pygame.image.load('images/stone.jpg')
skins = [pygame.image.load('images/tank.png'), pygame.image.load('images/tank_2.png'), pygame.image.load('images/tank3.png'), pygame.image.load('images/tank4.png')]
_ = False
TILE = 50
map = [[1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
       [1, _, _, _, _, _, _, _, _, _, _, _, _, _, _, 1],
       [1, _, _, _, _, _, _, _, _, _, _, _, _, _, _, 1],
       [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, _, 1, 1, 1, 1, 1],
       [1, _, 1, _, 1, _, 1, 1, 1, 1, _, _, _, 1, _, 1],
       [1, _, 1, _, 1, _, 1, _, _, 1, _, 1, _, 1, _, 1],
       [1, _, _, _, 1, _, 1, 1, _, 1, _, 1, _, _, _, 1],
       [1, _, 1, 1, 1, _, _, 1, _, 1, _, 1, _, 1, _, 1],
       [1, _, _, _, _, _, _, _, _, _, _, _, _, _, _, 1],
       [1, _, 2, 2, 2, 2, _, _, _, _, 2, 2, 2, 2, _, 1],
       [1, _, _, _, _, 2, _, _, _, _, 2, _, _, _, _, 1],
       [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]]

map_2 = [[1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
         [1, _, _, _, _, _, _, _, _, _, _, _, _, _, _, 1],
         [1, _, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, _, 1],
         [1, _, _, _, _, _, _, _, _, _, _, _, _, 1, _, 1],
         [1, _, 1, _, 1, _, 1, 1, 1, 1, _, _, _, 1, _, 1],
         [1, 1, _, _, _, _, _, _, _, _, _, _, _, 1, _, 1],
         [1, _, _, _, 1, _, 1, 1, _, 1, _, 1, _, 1, _, 1],
         [1, _, 1, 1, 1, _, _, 1, _, 1, _, 1, _, 1, _, 1],
         [1, _, 1, _, _, _, _, _, _, 1, _, _, _, 1, _, 1],
         [1, _, 1, _, _, _, _, _, _, 1, 1, 1, 1, 1, _, 1],
         [1, _, _, _, _, _, _, _, _, _, _, _, _, _, _, 1],
         [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]]

map_3 = [[1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
         [1, 3, 3, 3, 3, 3, _, _, _, _, _, _, 3, 3, 3, 1],
         [1, 2, 1, 1, 1, 1, 1, 1, _, 1, 1, 1, 1, 1, 2, 1],
         [1, _, _, _, 2, _, 1, _, _, _, _, _, _, _, _, 1],
         [1, _, 2, _, 1, _, 1, _, 1, 1, _, _, _, _, _, 1],
         [1, _, 1, _, 2, _, 1, _, _, 2, _, _, _, _, _, 1],
         [1, _, 1, _, 1, _, 1, _, _, 1, _, _, _, _, _, 1],
         [1, _, 1, _, 1, _, 2, _, _, 1, _, _, _, _, _, 1],
         [1, _, 1, _, _, _, _, _, _, 1, _, _, _, _, _, 1],
         [1, 2, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, _, 2, 1],
         [1, 3, 3, 3, 3, 3, _, _, _, _, _, _, 3, _, 3, 1],
         [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]]


class player:
    def __init__(self, pos, nav, color, cart, skin):
        self.pos = [pos[0] * TILE, pos[1] * TILE]
        self.nav = nav
        self.color = color
        self.cart = cart
        self.skin = skin

    def draw(self, screen):
        tank_s = pygame.Surface((40, 41))
        tank_s.fill((255, 255, 255))
        tank_s.blit(skins[skin], (0, 0))
        screen.blit(pygame.transform.rotate(tank_s, self.nav), (self.pos[0], self.pos[1]))

    def shot(self, screen):
        if self.nav == 180:
            for d in range(12 - self.pos[1] // TILE):
                if not c[self.pos[1] // TILE + d][self.pos[0] // TILE]:
                    pygame.draw.line(screen, self.color, (self.pos[0] + 20, self.pos[1] + d * 50), (self.pos[0] + 20, self.pos[1] + (d + 1) * 50), 5)
                else:
                    break
        elif self.nav == 0:
            for d in range(self.pos[1] // TILE - 1):
                if not c[self.pos[1] // TILE - d - 1][self.pos[0] // TILE]:
                    pygame.draw.line(screen, self.color, (self.pos[0] + 20, self.pos[1] - d * 50),
                                     (self.pos[0] + 20, self.pos[1] - (d+1) * 50), 5)
                else:
                    break
        elif self.nav == 270:
            for d in range(16 - self.pos[0] // TILE):
                if not c[self.pos[1] // TILE][self.pos[0] // TILE + d]:
                    pygame.draw.line(screen, self.color, (self.pos[0] + d * 50, self.pos[1] + 20),
                                     (self.pos[0] + d * 50 + 50, self.pos[1] + 20), 5)
                else:
                    break
        elif self.nav == 90:
            for d in range(self.pos[0] // TILE - 1):
                if not c[self.pos[1] // TILE][self.pos[0] // TILE - d - 1]:
                    pygame.draw.line(screen, self.color, (self.pos[0] - d * 50, self.pos[1] + 20),
                                     (self.pos[0] - (d+1) * 50, self.pos[1] + 20), 5)
                else:
                    break


pygame.mixer.init()
fon = pygame.image.load('images/fon.jpg')
pygame.mixer.music.load('music/fon.wav')
pygame.mixer.music.play(-1)
x_fon = 0
y_fon = 0
grass = pygame.image.load('images/grass.jpg')
skin = 0
while True:
    n = -1
    players = []
    number_of_cart = 0
    fl = True
    while fl:
        screen.fill((255, 255, 255))
        screen.blit(fon, (0, 0), (x_fon % 800, y_fon % 600, 800, 600))
        y_fon += random.uniform(0.1, 1.5)
        x_fon += random.uniform(0.1, 5.0)
        screen.blit(pygame.transform.scale(skins[skin], (100, 100)), (320, 170))
        pygame.draw.polygon(screen, (100, 100, 255), ((435, 200), (435, 250), (475, 225)))
        pygame.draw.polygon(screen, (100, 100, 255), ((305, 200), (305, 250), (265, 225)))
        for t in pygame.event.get():
            if t.type == pygame.QUIT:
                exit(1)
            if t.type == pygame.MOUSEBUTTONDOWN:
                x_rect = pygame.Rect(pygame.mouse.get_pos() + (1, 1))
                f_rect = pygame.Rect(50, 250, 240, 180)
                s_rect = pygame.Rect(450, 250, 240, 180)
                th_rect = pygame.Rect(250, 430, 240, 180)
                right_rect = pygame.Rect(435, 200, 40, 50)
                left_rect = pygame.Rect(265, 200, 40, 50)
                if x_rect.colliderect(f_rect):
                    number_of_cart = 1
                    fl = False
                    break
                elif x_rect.colliderect(s_rect):
                    number_of_cart = 0
                    fl = False
                    break
                elif x_rect.colliderect(th_rect):
                    number_of_cart = 2
                    fl = False
                    break
                elif x_rect.colliderect(right_rect) and skin + 1 < len(skins):
                    skin += 1
                elif x_rect.colliderect(left_rect) and skin - 1 > -1:
                    skin -= 1
        pygame.draw.rect(screen, (0, 0, 0), (50, 250, 240, 180))
        for t in range(12):
            for g in range(16):
                if map[t][g] == 1:
                    pygame.draw.rect(screen, (15, 255, 255), (g * 15 + 50, t * 15 + 250, 19, 19))
                elif map[t][g] == 2:
                    sur = pygame.Surface((20, 20))
                    sur.blit(stone, (0, 0))
                    screen.blit(sur, (g * 15 + 50, t * 15 + 250))
                elif map[t][g] == 3:
                    sur = pygame.Surface((20, 20))
                    sur.blit(grass, (0, 0))
                    screen.blit(sur, (g * 15 + 50, t * 15 + 250))
                elif not map[t][g]:
                    pygame.draw.rect(screen, (255, 255, 255), (g * 15 + 50, t * 15 + 250, 19, 19))
        pygame.draw.rect(screen, (0, 0, 0), (450, 250, 240, 180))
        for t in range(12):
            for g in range(16):
                if map_2[t][g] == 1:
                    pygame.draw.rect(screen, (15, 255, 255), (g * 15 + 450, t * 15 + 250, 19, 19))
                elif map_2[t][g] == 2:
                    sur = pygame.Surface((20, 20))
                    sur.blit(stone, (0, 0))
                    screen.blit(sur, (g * 15 + 450, t * 15 + 250))
                elif map_2[t][g] == 3:
                    sur = pygame.Surface((20, 20))
                    sur.blit(grass, (0, 0))
                    screen.blit(sur, (g * 15 + 450, t * 15 + 250))
                elif not map_2[t][g]:
                    pygame.draw.rect(screen, (255, 255, 255), (g * 15 + 450, t * 15 + 250, 19, 19))
        pygame.draw.rect(screen, (0, 0, 0), (250, 430, 240, 180))
        for t in range(12):
            for g in range(16):
                if map_3[t][g] == 1:
                    pygame.draw.rect(screen, (15, 255, 255), (g * 15 + 250, t * 15 + 430, 19, 19))
                elif map_3[t][g] == 2:
                    sur = pygame.Surface((20, 20))
                    sur.blit(stone, (0, 0))
                    screen.blit(sur, (g * 15 + 250, t * 15 + 430))
                elif map_3[t][g] == 3:
                    sur = pygame.Surface((20, 20))
                    sur.blit(grass, (0, 0))
                    screen.blit(sur, (g * 15 + 250, t * 15 + 430))
                elif not map_3[t][g]:
                    pygame.draw.rect(screen, (255, 255, 255), (g * 15 + 250, t * 15 + 430, 19, 19))
        # pygame.draw.rect(screen, (0, 0, 0), (260, 50, 260, 100), border_radius=10)
        # screen.blit(pygame.font.Font('fonts/HighVoltage Rough.ttf', 100).render("Winter", False, (255, 255, 255)), (265, 50))
        tanks = pygame.image.load('images/tanks.png')
        screen.blit(tanks, (0, 0))
        pygame.display.flip()
        time.sleep(0.01)
    x = []
    while len(x) == 0:
        y = random.randint(0, 11)
        x = []
        for t in map[y]:
            if not t:
                x.append(map[y].index(t))
        if len(x) > 0:
            client_player = player([random.choice(x), y], 0, (255, 0, 0), number_of_cart, skin)


    def reading():
        global n, players
        while True:
            if n == "leave":
                n = -1
                return
            try:
                data, address = client.recvfrom(1024)
            except OSError:
                return
            data = data.decode('utf-8')
            players = data.split('  ')[:-1]


    server_2 = '192.168.0.173', 8300
    client = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    client.bind(('', 0))
    read = threading.Thread(target=reading)
    read.start()
    fl = True
    live = [5, 5]
    motion = False
    shot = False
    tank_in_grass = pygame.image.load('images/tank_in_grass.png')
    leave_tank = pygame.image.load('images/leave_tank.png')
    while fl:
        screen.fill((122, 122, 122))
        if client_player.cart == 1:
            c = copy.copy(map)
        elif client_player.cart == 0:
            c = copy.copy(map_2)
        elif client_player.cart == 2:
            c = copy.copy(map_3)
        for t in range(12):
            for g in range(16):
                if c[t][g] == 1:
                    pygame.draw.rect(screen, (15, 245, 255), (g * 50, t * 50, 49, 49))
                elif c[t][g] == 2:
                    screen.blit(stone, (g * 50, t * 50))
                elif not c[t][g]:
                    pygame.draw.rect(screen, (255, 255, 255), (g * 50, t * 50, 49, 49))
                elif c[t][g] == 3:
                    screen.blit(grass, (g * 50, t * 50))
        for t in pygame.event.get():
            if t.type == pygame.QUIT:
                fl = False
                break
            elif t.type == pygame.KEYDOWN:
                if t.key == pygame.K_w:
                    if client_player.nav == 0:
                        motion = 'UP'
                    elif client_player.nav == 270:
                        motion = 'RIGHT'
                    elif client_player.nav == 180:
                        motion = "DOWN"
                    else:
                        motion = "LEFT"
                if t.key == pygame.K_RIGHT:
                    client_player.nav = 270
                if t.key == pygame.K_LEFT:
                    client_player.nav = 90
                if t.key == pygame.K_UP:
                    client_player.nav = 0
                if t.key == pygame.K_DOWN:
                    client_player.nav = 180
                if t.key == pygame.K_SPACE:
                    shot = True
            elif t.type == pygame.KEYUP:
                motion = False
                shot = False
        if fl:
            if motion == "RIGHT":
                if not c[client_player.pos[1] // TILE][client_player.pos[0] // TILE + 1] or c[client_player.pos[1] // TILE][client_player.pos[0] // TILE + 1] == 3:
                    client_player.pos[0] += TILE
            elif motion == 'LEFT':
                if not c[client_player.pos[1] // TILE][client_player.pos[0] // TILE - 1] or c[client_player.pos[1] // TILE][client_player.pos[0] // TILE - 1] == 3:
                    client_player.pos[0] -= TILE
            elif motion == "UP":
                if not c[client_player.pos[1] // TILE - 1][client_player.pos[0] // TILE] or c[client_player.pos[1] // TILE - 1][client_player.pos[0] // TILE] == 3:
                    client_player.pos[1] -= TILE
            elif motion == "DOWN":
                if not c[client_player.pos[1] // TILE + 1][client_player.pos[0] // TILE] or c[client_player.pos[1] // TILE + 1][client_player.pos[0] // TILE] == 3:
                    client_player.pos[1] += TILE
            if shot:
                client_player.shot(screen)
            client.sendto(f'{client_player.pos[0]} {client_player.pos[1]} {client_player.color[0]} {client_player.color[1]} {client_player.color[2]} {client_player.nav} {1 if shot else 0} {client_player.cart} {client_player.skin}'.encode("utf-8"), server_2)
            if c[client_player.pos[1] // TILE][client_player.pos[0] // TILE] != 3:
                client_player.draw(screen)
            else:
                screen.blit(pygame.transform.rotate(tank_in_grass, client_player.nav - 90), client_player.pos)
            for td in players:
                t = td.split()
                if t[0] != 'leave':
                    if int(t[6]) == 1:
                        if int(t[5]) == 180:
                            for d in range(12 - int(t[1]) // TILE):
                                if [int(t[1]) + d * 50, int(t[0])] == [client_player.pos[1], client_player.pos[0]]:
                                    live[0] -= 1
                                    break
                                if c[int(t[1]) // TILE + d][int(t[0]) // TILE] in (False, 3):
                                    pygame.draw.line(screen, (int(t[2]), int(t[3]), int(t[4])), (int(t[0]) + 20, int(t[1]) + d * 50),
                                                     (int(t[0]) + 20, int(t[1]) + (d + 1) * 50), 5)
                                else:
                                    break
                        elif int(t[5]) == 0:
                            for d in range(int(t[1]) // TILE - 1):
                                if [int(t[1]) - d * 50 - 50, int(t[0])] == [client_player.pos[1], client_player.pos[0]]:
                                    live[0] -= 1
                                    break
                                if c[int(t[1]) // TILE - d - 1][int(t[0]) // TILE] in (False, 3):
                                    pygame.draw.line(screen, (int(t[2]), int(t[3]), int(t[4])), (int(t[0]) + 20, int(t[1]) - d * 50),
                                                     (int(t[0]) + 20, int(t[1]) - (d + 1) * 50), 5)
                                else:
                                    break
                        elif int(t[5]) == 270:
                            for d in range(16 - int(t[0]) // TILE):
                                if [int(t[1]), int(t[0]) + d * 50] == [client_player.pos[1], client_player.pos[0]]:
                                    live[0] -= 1
                                    break
                                if c[int(t[1]) // TILE][int(t[0]) // TILE + d]  in (False, 3):
                                    pygame.draw.line(screen, (int(t[2]), int(t[3]), int(t[4])), (int(t[0]) + d * 50, int(t[1]) + 20),
                                                     (int(t[0]) + d * 50 + 50, int(t[1]) + 20), 5)
                                else:
                                    break
                        elif int(t[5]) == 90:
                            for d in range(int(t[0]) // TILE - 1):
                                if [int(t[1]), int(t[0]) - d * 50 - 50] == [client_player.pos[1], client_player.pos[0]]:
                                    live[0] -= 1
                                    break
                                if c[int(t[1]) // TILE][int(t[0]) // TILE - d - 1] in (False, 3):
                                    pygame.draw.line(screen, (int(t[2]), int(t[3]), int(t[4])), (int(t[0]) - d * 50, int(t[1]) + 20),
                                                     (int(t[0]) - (d + 1) * 50, int(t[1]) + 20), 5)
                                else:
                                    break
                    if c[int(t[1]) // TILE][int(t[0]) // TILE] != 3:
                        tank_s = pygame.Surface((40, 41))
                        tank = pygame.image.load("images/tank.png")
                        tank_s.fill((255, 255, 255))
                        tank_s.blit(skins[int(t[8])], (0, 0))
                        screen.blit(pygame.transform.rotate(tank_s, int(t[5])), (int(t[0]), int(t[1])))
                else:
                    print(t)
                    screen.blit(leave_tank, (int(t[1]), int(t[2])))
            if live[0] == 0:
                fl = False
                break
            pygame.draw.rect(screen, (122, 122, 122), (420, 5, 180, 59))
            pygame.draw.rect(screen, (122, 122, 122), (600, 17, 10, 30))
            for t in range(live[0]):
                pygame.draw.polygon(screen, (255, 0, 0), ((t * 33 + 430, 10), (t * 33 + 430 + 25, 10), (t * 33 + 430 + 30, 60), (t * 33 + 430 + 10, 60)))
        pygame.display.flip()
        time.sleep(0.15)
    client.sendto(f"leave {client_player.pos[0]} {client_player.pos[1]} {client_player.color[0]} {client_player.color[1]} {client_player.color[2]} {client_player.nav} {1 if shot else 0} {client_player.cart} {client_player.skin}".encode('utf-8'), server_2)
    n = 'leave'
    client.shutdown(socket.SHUT_WR)
    client.close()
