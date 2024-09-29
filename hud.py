import pygame as pg

class HeadsUpDisplay:
    def __init__(self, aircraft, screen):
        self.aircraft = aircraft
        self.screen = screen
        padding = 70
        screen_width, screen_height = screen.get_width(), screen.get_height()
        hud_width, hud_height = screen_width / 2 - padding * 2 , 300
        hud_left, hud_top = padding, screen_height - 350

        self.rect = pg.rect.Rect(hud_left, hud_top, hud_width, hud_height)
        self.surface = pg.Surface((self.rect.width, self.rect.height), 
                                  pg.SRCALPHA)
        self.show_status()

    def put_text(self, text, size, color, rel_pos):
        font = pg.font.Font(None, size)
        text = font.render(text, True, color)
        pos = text.get_rect(left=rel_pos[0], top=rel_pos[1])
        self.surface.blit(text, pos)

    def show_status(self):
        self.surface.fill((100, 100, 100, 128))
        status_dict = {
            'name': [self.aircraft.name, 30, (255, 255, 255), (10, 10)],
            'speed': [
                f'V [knots] : {1.94384*self.aircraft.airspeed:.2f}', 
                30, (255, 255, 255), (10, 40)
            ],
            'roc': [
                f'ROC [ft/min] : {196.85*self.aircraft.roc:.2f}', 
                30, (255, 255, 255), (10, 70)
            ],
            'a_x': [
                f'a_x [ft/s^2] : {3.28084*self.aircraft.acc_x:.2f}', 
                30, (255, 255, 255), (10, 100)
            ],
            'a_y': [
                f'a_y [ft/s^2] : {3.28084*self.aircraft.acc_y:.2f}', 
                30, (255, 255, 255), (10, 130)
            ],
            'altitude': [
                f'alt [ft] : {3.28084*self.aircraft.alt:.2f}', 
                30, (255, 255, 255), (10, 160)
            ],
            'power': [
                f'power [%]: {self.aircraft.power_percentage:.2f}', 
                30, (255, 255, 255), (10, 190)
            ],
            'engine status': [
                f'Engines: {"ON" if self.aircraft.engine_on else "OFF"}', 
                30, (255, 255, 255), (10, 220)
            ],   
            'brake status': [
                f'Brakes: {"ON" if self.aircraft.brakes_on else "OFF"}', 
                30, (255, 255, 255), (10, 250)
            ],    
            'load factor': [
                f'Load Factor [-]: {self.aircraft.lift/self.aircraft.weight:.2f}', 
                30, (255, 255, 255), (10, 280)
            ],   
            'angle of attack': [
                f'AoA [deg]: {self.aircraft.angle_of_attack:.2f}', 
                30, (255, 255, 255), (300, 40)
            ],
            'distance': [
                f'Distance travelled [m]: {self.aircraft.dx:.2f}', 
                30, (255, 255, 255), (300, 70)
            ],
            'mach': [
                f'Mach No. [-]: {self.aircraft.mach_number:.2f}', 
                30, (255, 255, 255), (300, 100)
            ],       
        }

        if self.aircraft.power_percentage > 85.:
            status_dict['power'][2] = (255, 0, 0)
        if self.aircraft.brakes_on and self.aircraft.acc_x > 0:
            status_dict['brake status'][2] = (255, 0, 0) 

        for arg in status_dict.values():
            self.put_text(*arg)


