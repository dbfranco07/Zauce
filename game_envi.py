import pygame as pg
import numpy as np
from aircraft import Aircraft
import random

class Background:
    def __init__(self, screen, max_alt=1_000):
        self.screen = screen
        self.width = self.screen.get_width()
        self.height = self.screen.get_height()
        self.max_alt = max_alt
        self.bg_stuff = []

    def gradient(self, alt):
        max_color = 255
        ground_level = 620
        screen_height_arr = np.arange(self.height)
        alt_array = (-screen_height_arr + ground_level)/ 10 + alt
        color = np.zeros((self.height, 3))
        color[:, 2] = max_color * (1 - alt_array / self.max_alt)  # blue channel
        color[:, 1] = max_color * (1 - alt_array / self.max_alt)  # green channel
        color[:, 0] = max_color * (1 - alt_array / self.max_alt)  # red channel

        color[alt_array < 0] = [0, 0, 0]
        color[alt_array < -0.3] = [139, 69, 19]

        color = np.clip(color, 0, max_color).astype(np.uint8)
        gradient = np.zeros((self.height, self.width, 3), dtype=np.uint8)
        for i in range(3):  # Iterate over the color channels
            gradient[:, :, i] = color[:, i][:, np.newaxis]

        # Transpose the gradient if needed (depends on your requirements)
        gradient_transposed = gradient.transpose(1, 0, 2)
        surface = pg.surfarray.make_surface(gradient_transposed)

        return surface
    
    def show_items(self, speed, alt):
        if random.randint(1, 250) == 1:
            mountain1 = BackgroundItems(
                'background/mountain1.png', self.width, -62)
            self.bg_stuff.append(mountain1) 

        # if random.randint(1, 250) == 1:
        #     mountain2 = BackgroundItems(
        #         'background/mountain2.png', self.width, -62)

        #     self.bg_stuff.append(mountain2)
            

        if random.randint(1, 20) == 1:
            tree1 = BackgroundItems('background/tree1.png', self.width, 522)
            self.bg_stuff.append(tree1)

        if random.randint(1, 30) == 1:
            tree2 = BackgroundItems('background/tree2.png', self.width, 530)
            self.bg_stuff.append(tree2)

        if random.randint(1, 150) == 1:
            new_cloud = BackgroundItems(
                'background/cloud1.png', self.width, 522-1000)
            self.bg_stuff.append(new_cloud)


        for items in self.bg_stuff:
            items.update(speed * 0.01 * 10, alt)
            self.screen.blit(items.image, items.rect)


    # def show_clouds(self, speed, alt):
    #     if random.randint(1, 50) == 1:
    #         new_cloud = BackgroundItems(
    #             'background/cloud1.png', self.width, 522
    #         )
    #         self.bg_stuff.append(new_cloud)
    #     for cloud in self.bg_stuff:
    #         cloud.update(speed * 0.01 * 10, alt)
    #         self.screen.blit(tree.image, tree.rect)

class BackgroundItems(pg.sprite.Sprite):
    def __init__(self, image_path, x, y,**kwargs):
        super().__init__(**kwargs)
        self.image = pg.image.load(image_path).convert_alpha()
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.initial_y = y
        # self.ground_level = ground_level

    def update(self, speed, alt):
        self.rect.x -= speed
        self.rect.y = self.initial_y + alt * 10
        if self.rect.right < 0 or self.rect.top > 1080:
            self.kill()

    