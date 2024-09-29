import os
import pygame as pg
import numpy as np
from aircraft import Aircraft
from game_envi import Background, BackgroundItems
from hud import HeadsUpDisplay
import random

def main():
    pg.init()
    size = pg.display.get_desktop_sizes()[0]
    screen = pg.display.set_mode(size) # Surface of screen
 

    # 100 pixels = 10m; 1m = 10 pixels
    aircraft = Aircraft('Aircraft 1', 'aircraft-models/aircraft2.png')
    background = Background(screen)
    hud = HeadsUpDisplay(aircraft, screen)

    # tree = Tree('background/tree.png', 1000, 522)
    trees = []

    running = True
    return_key_pressed_last_frame = False
    b_key_pressed_last_frame = False

    while running:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                running = False

        keys = pg.key.get_pressed()
        if keys[pg.K_RETURN] and not return_key_pressed_last_frame:
            aircraft.toogle_engine()
            return_key_pressed_last_frame = True
        elif not keys[pg.K_RETURN]:
            return_key_pressed_last_frame = False

        if keys[pg.K_b] and not b_key_pressed_last_frame:
            aircraft.toogle_brakes()
            b_key_pressed_last_frame = True
        elif not keys[pg.K_b]:
            b_key_pressed_last_frame = False

        if keys[pg.K_UP]:
            aircraft.increase_power()
        if keys[pg.K_DOWN]:
            aircraft.decrease_power()

        if keys[pg.K_1]:
            aircraft.increase_aoa()
        if keys[pg.K_2]:
            aircraft.decrease_aoa()

        aircraft.accelerate()  
        sky = background.gradient(aircraft.alt)
        screen.blit(sky, (0, 0))

        background.show_items(aircraft.airspeed, aircraft.alt)
        
        screen.blit(aircraft.surface, aircraft.rect)
        screen.blit(hud.surface, hud.rect)
        hud.show_status()

        pg.display.flip()

    pg.quit()

if __name__ == '__main__':
    main()