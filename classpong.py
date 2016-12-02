import pygame as pg
import math
import random
import time

display_width = 800
display_height = 600

black = (0, 0, 0)
white = (255, 255, 255)
red = (255, 0, 0)
green = (0, 255, 0)

kolor_active = (35, 21, 71)
kolor_inactive = (17, 13, 29)

pilka_wys = 40
pilka_sze = 40
paletka_dl = 15
paletka_wys = 125


class pilka(pg.sprite.Sprite):
    "Klasa reprezentująca piłke."

    def __init__(self, kat, szybkosc, x, y):
        #self.kolor = kolor
        pg.sprite.Sprite.__init__(self)
        self.obraz = pg.image.load("data/pilka.png")
        self.kat = kat
        self.szybkosc = szybkosc
        self.x = x  # polozenie pilki
        self.y = y  # polozenie pilki
        self.rect = self.obraz.get_rect()

    def wyswietl(self, gameDisplay):
        #pg.draw.circle(gameDisplay, self.kolor, (self.x, self.y), self.promien)
        gameDisplay.blit(self.obraz, (self.x, self.y))

    def update_rect(self):
        self.rect.x = self.x
        self.rect.y = self.y

    def czy_kolizja(self, paletka, hit_sound):
        sprite_group = pg.sprite.Group()
        sprite_group.add(paletka)
        sprite_list = pg.sprite.spritecollide(self, sprite_group, False)
        if paletka.strona == 'l' and self.rect.x - 1 <= paletka.rect.right and len(sprite_list) != 0:
            pg.mixer.Sound.play(hit_sound)
            paletka.liczba_odbic += 1
            self.szybkosc = abs(self.szybkosc)
            self.kat = self.kat + math.pi / 4 * \
                (self.rect.centery - paletka.rect.centery) / \
                (paletka.rect.height / 2)
            if self.kat * 180 / math.pi > 50:
                self.kat = 50 * math.pi / 180
            elif self.kat * 180 / math.pi < -50:
                self.kat = -50 * math.pi / 180

        if paletka.strona == 'p' and self.rect.right + 1 >= paletka.rect.x and len(sprite_list) != 0:
            pg.mixer.Sound.play(hit_sound)
            paletka.liczba_odbic += 1
            self.szybkosc = -abs(self.szybkosc)
            paletka.factor = paletka.factor * 0.95
            self.kat = self.kat + math.pi / 4 * \
                (self.rect.centery - paletka.rect.centery) / \
                (paletka.rect.height / 2)
            if self.kat * 180 / math.pi > 50:
                self.kat = 50 * math.pi / 180
            elif self.kat * 180 / math.pi < -50:
                self.kat = -50 * math.pi / 180

    def czy_sciana(self):
        if self.y + pilka_wys >= display_height or self.y <= 0:
            self.kat = -self.kat

    def czy_przegrana(self, liczba_graczy, myfont, lose_sound, win_sound, gameDisplay):
        if self.x + pilka_sze >= display_width:
            pg.mixer.music.pause()

            # gameDisplay.fill(white)
            if liczba_graczy == 1:
                label = myfont.render("Losers always lose!", 1, white)
                pg.mixer.Sound.play(lose_sound)
            else:
                label = myfont.render("Czerwony gracz wygrał!", 1, white)
                pg.mixer.Sound.play(win_sound)
            label_rect = label.get_rect()
            label_rect.center = (display_width / 2, display_height / 2)
            gameDisplay.blit(label, label_rect)
            pg.display.update()
            time.sleep(3.5)
            pg.mixer.music.unpause()
            return (False)

        elif self.x <= 0:
            pg.mixer.music.pause()
            pg.mixer.Sound.play(win_sound)

            # gameDisplay.fill(white)
            if liczba_graczy == 1:
                label = myfont.render("Pokonałeś robota! Yupi!", 1, white)
            else:
                label = myfont.render("Niebieski gracz wygrał!", 1, white)
            label_rect = label.get_rect()
            label_rect.center = (display_width / 2, display_height / 2)
            gameDisplay.blit(label, label_rect)
            pg.display.update()
            time.sleep(3.5)
            pg.mixer.music.unpause()
            return(False)
        else:
            return(True)


class paletka(pg.sprite.Sprite):
    "Klasa reprezentujaca prostokąt, którym odbijamy piłke."

    def __init__(self, szerokosc, wysokosc, kolor, x, y, szybkosc, strona, factor, liczba_odbic):
        pg.sprite.Sprite.__init__(self)
        self.szerokosc = paletka_dl
        self.wysokosc = paletka_wys
        self.kolor = kolor
        self.x = x  # polozenie paletki
        self.y = y  # polozenie paletki
        self.strona = strona  # paletka: lewa ('l') czy prawa ('p')
        if self.strona == 'l':
            self.obraz = pg.image.load("data/belka1.png")
        else:
            self.obraz = pg.image.load("data/belka2.png")
        self.rect = self.obraz.get_rect()
        self.szybkosc = szybkosc
        self.factor = factor
        self.liczba_odbic = liczba_odbic

    def wyswietl(self, gameDisplay):
        #pg.draw.rect(gameDisplay, self.kolor, (self.x, self.y, self.szerokosc, self.wysokosc))
        gameDisplay.blit(self.obraz, (self.x, self.y))

    def update_rect(self):
        self.rect.x = self.x
        self.rect.y = self.y

    def ruch(self, klawisze, key_up, key_down):
        if klawisze[key_up]:
            self.y += -self.szybkosc
        if klawisze[key_down]:
            self.y += self.szybkosc

        if self.y <= 2:  # aby zatrzymac belke
            self.y = 1
        if self.y + self.wysokosc >= display_height - 2:  # aby zatrzymac belke
            self.y = display_height - self.wysokosc - 1

    def ruch_robot(self, pilka):
        if pilka.rect.centerx <= display_width / 2:
            if pilka.rect.centery > self.rect.centery + 10:
                self.y = self.y + 5 * self.factor
            elif pilka.rect.centery < self.rect.centery - 10:
                self.y = self.y - 5 * self.factor


class przycisk():
    "Klasa reprezentująca przyciski."

    def __init__(self, text, x, y, wysokosc, szerokosc, col_active, col_inactive, funkcja, argumenty):
        self.text = text
        self.x = x
        self.y = y
        self.wysokosc = wysokosc
        self.szerokosc = szerokosc
        self.col_active = col_active
        self.col_inactive = col_inactive
        self.funkcja = funkcja
        self.argumenty = argumenty

    def wyswietl(self, gameDisplay, myfont_button):
        pg.draw.rect(gameDisplay, self.col_inactive,
                     (self.x, self.y, self.szerokosc, self.wysokosc))
        label = myfont_button.render(self.text, 1, white)
        label_rect = label.get_rect()
        label_rect.center = (self.x + self.szerokosc / 2,
                             self.y + self.wysokosc / 2)
        gameDisplay.blit(label, label_rect)

    def czy_najechany(self, gameDisplay, myfont_button):
        mouse = pg.mouse.get_pos()

        if self.x < mouse[0] < self.x + self.szerokosc and self.y < mouse[1] < self.y + self.wysokosc:
            pg.draw.rect(gameDisplay, self.col_active,
                         (self.x, self.y, self.szerokosc, self.wysokosc))
            label = myfont_button.render(self.text, 1, white)
            label_rect = label.get_rect()
            label_rect.center = (self.x + self.szerokosc /
                                 2, self.y + self.wysokosc / 2)
            gameDisplay.blit(label, label_rect)

    def czy_wybrany(self):
        mouse = pg.mouse.get_pos()
        pressed = pg.mouse.get_pressed()
        klawisze = pg.key.get_pressed()

        if (self.x < mouse[0] < self.x + self.szerokosc and self.y < mouse[1] < self.y + self.wysokosc and pressed[0] == 1):
            self.funkcja(*self.argumenty)
        elif klawisze[pg.K_1]:
            self.funkcja(*[1])
        elif klawisze[pg.K_2]:
            self.funkcja(*[2])
