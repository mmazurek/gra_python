import pygame as pg
import math
import random
import time
from classpong import *


def game_start(liczba_graczy):

    background = pg.image.load("data/BackgroundForAsteroids.png")

    start = True
    kat = random.uniform(-math.pi / 2 + math.pi / 5, math.pi / 2 - math.pi / 5)
    x = 20
    # y = 300
    ruch = random.choice([-1, 1]) * 6

    pileczka = pilka(kat, ruch, display_width / 2, display_height / 2)
    belka_l = paletka(paletka_dl, paletka_wys, green, x,
                      display_height / 2, 5, 'l', 0.95, 0)
    belka_p = paletka(paletka_dl, paletka_wys, green,
                      display_width - paletka_dl - 20, display_height / 2, 5, 'p', 1, 0)

    pg.key.set_repeat(1, 15)

    while start:
        start = (pileczka.czy_przegrana(
            liczba_graczy, myfont, lose_sound, win_sound, gameDisplay))
        gameDisplay.blit(background, (-20, -10))
        pg.mouse.set_visible(0)

        for event in pg.event.get():
            if event.type == pg.QUIT:
                start = False

        pileczka.update_rect()
        belka_l.update_rect()
        belka_p.update_rect()

        klawisze = pg.key.get_pressed()

        if klawisze[pg.K_m]:
            start = False

        belka_p.ruch(klawisze, pg.K_UP, pg.K_DOWN)
        if liczba_graczy == 1:
            belka_l.ruch_robot(pileczka)
        else:
            belka_l.ruch(klawisze, pg.K_w, pg.K_s)

        # gameDisplay.fill(white)

        pileczka.czy_kolizja(belka_l, hit_sound)
        pileczka.czy_kolizja(belka_p, hit_sound)

        pileczka.czy_sciana()

        pileczka.wyswietl(gameDisplay)
        belka_l.wyswietl(gameDisplay)
        belka_p.wyswietl(gameDisplay)

        pg.display.flip()
        timer.tick(60)

        pileczka.x = pileczka.x + pileczka.szybkosc
        pileczka.y = pileczka.y + \
            abs(pileczka.szybkosc) * math.tan(pileczka.kat)


pg.init()

gameDisplay = pg.display.set_mode((display_width, display_height))

pg.display.set_caption('Pong')

timer = pg.time.Clock()

gameIcon = pg.image.load('data/ping-pong-bat.png')
pg.display.set_icon(gameIcon)

pg.font.init()
myfont = pg.font.SysFont("monospace", 50)
myfont_button = pg.font.SysFont("monospace", 30)

# dzwieki
lose_sound = pg.mixer.Sound("data/horn_fail.wav")
hit_sound = pg.mixer.Sound("data/pilka_odbicie.wav")
win_sound = pg.mixer.Sound("data/yesx2.wav")

pg.mixer.music.load('data/game_music.wav')
pg.mixer.music.set_volume(0.7)
pg.mixer.music.play(-1)

przycisk_play = przycisk("Jeden gracz", 250, 200, 70,
                         240, kolor_active, kolor_inactive, game_start, [1])
przycisk_play2 = przycisk("Dwóch graczy", 250, 350, 70,
                          240, kolor_active, kolor_inactive, game_start, [2])
startm = True
background = pg.image.load("data/BackgroundForAsteroids.png")

while startm:
    pg.mouse.set_visible(1)
    # gameDisplay.fill(white)
    gameDisplay.blit(background, (-20, -10))

    przycisk_play.wyswietl(gameDisplay, myfont_button)
    przycisk_play.czy_najechany(gameDisplay, myfont_button)
    przycisk_play.czy_wybrany()

    przycisk_play2.wyswietl(gameDisplay, myfont_button)
    przycisk_play2.czy_najechany(gameDisplay, myfont_button)
    przycisk_play2.czy_wybrany()

    for eventm in pg.event.get():
        if eventm.type == pg.QUIT:
            startm = False

    klawisze = pg.key.get_pressed()
    if klawisze[pg.K_ESCAPE]:
        startm = False

    pg.display.flip()
    timer.tick(60)

pg.quit()
quit()
