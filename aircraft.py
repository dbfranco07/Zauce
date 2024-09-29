import pygame as pg
import os
from physics_engine import PhysicsConstants, Atmosphere, AircraftAerodynamics
import time
import numpy as np

class Aircraft(AircraftAerodynamics, pg.sprite.Sprite):
    def __init__(self, name, image_path, 
                 engine_rated_power=73549.9, 
                 propeller_efficiency=0.77, 
                 weight=6333, 
                 initial_pos=(100, 540), 
                 **kwargs):
        self.name = name
        self.surface = pg.image.load(image_path).convert_alpha()
        self.surface = pg.transform.scale(self.surface, (200, 100))
        self.rect = self.surface.get_rect()
        self.rect.update((initial_pos[0], initial_pos[1]), (200, 100))
        # self.rect.move_ip(initial_pos[0], initial_pos[1])

        self.engine_rated_power = engine_rated_power
        self.propeller_efficiency = propeller_efficiency
        self.weight = weight

        # self.aspect_ratio = aspect_ratio
        # self.wing_area = wing_area

        self.power = 0
        self.alt = 0
        self.dx = 0

        self.airspeed = 0
        self.roc = 0
        self.mach_number = 0

        self.acc_x = 0
        self.acc_y = 0

        self.power_percentage = 0
        self.brakes_on = True
        self.engine_on = False
        self.lift = 0
        self.rho = 1.225

        super().__init__(**kwargs)

    @property
    def rated_power_max(self):
        return self.engine_rated_power * self.propeller_efficiency
    
    def toogle_engine(self):
        self.engine_on = not self.engine_on

    def toogle_brakes(self):
        self.brakes_on = not self.brakes_on

    def increase_power(self):
        if self.engine_on:
            self.power += 500
            if self.power > self.rated_power_max:
                self.power = self.rated_power_max      
            self.power_percentage = (self.power / self.rated_power_max) * 100 

    def decrease_power(self):
        self.power -= 800
        if self.power < 0:
            self.power = 0
        self.power_percentage = (self.power / self.rated_power_max) * 100    

    def increase_aoa(self):
        self.angle_of_attack += 0.1

    def decrease_aoa(self):
        self.angle_of_attack -= 0.1
    
    def accelerate(self):
        if not self.brakes_on:
            if self.airspeed < 0.001:
                self.airspeed = 0.001
            m = self.weight / PhysicsConstants.ACC_GRAVITY
            rho = Atmosphere(self.alt).prhoT[1]
            V = self.airspeed
            S = self.wing_area
            cl = self.cl()
            cd = self.cd_total()
            P = self.power
            D = 0.5 * rho * V ** 2 * S * cd
            T = P / V - D
            acc_x = T / m
            self.acc_x = acc_x
            self.airspeed += self.acc_x * 0.01
            self.dx += self.airspeed * 0.01

            L = 0.5 * rho * V ** 2 * S * cl
            self.lift = L

            acc_y = (L - self.weight) / m
            if self.alt <= 0 and acc_y < 0:
                self.acc_y = 0
                self.roc = 0
            else:
                self.acc_y = acc_y
                self.roc += self.acc_y * 0.01

            self.alt += self.roc * 0.01
            if self.alt <= 0:
                self.alt = 0

            temp = Atmosphere(self.alt).prhoT[2]
            speed_of_sound = np.sqrt(1.4 * 287 * temp)
            self.mach_number = self.airspeed / speed_of_sound
