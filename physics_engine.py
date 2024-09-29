import numpy as np

class PhysicsConstants:
    PRESSURE_0 = 101325 # Pascal
    DENSITY_0 = 1.225 # kilogram / meter ^ 3
    TEMPERATURE_0 = 288 # Kelvin
    ACC_GRAVITY = 9.81 # meters / second ^ 2
    GAS_CONSTANT_AIR = 287 #Joules / Newton x meter 

    AIR_PROP_DICT = { 
        # (min alt, max alt)
        # (km, km)

        # (min alt, lapse rate, pressure, density, temperature)
        # (km, Kelvin/m, Pascal, kg/m^3, Kelvin)
        (0, 11): [0, -6.5e-3, 101325., 1.225, 288.],
        (11, 25): [11, 0, 22586., 0.3634, 216.4],
        (25, 47): [25, 3e-3, 2474., 0.03981, 216.4],
        (47, 53): [47, 0, 119.7, 0.001476, 281.6],
        (53, 79): [53, -4.5e-3, 57.9, 0.0007148, 282.4],
    }
    
    def get_air_prop(self, alt):
        for (min_alt, max_alt), values in self.AIR_PROP_DICT.items():
            if min_alt <= alt/1000 < max_alt:
                return values
        return 0

 
class Atmosphere:
    def __init__(self, alt):
        self.alt = alt

    @property
    def prhoT(self):
        '''a = lapse rate, p = pressure, rho = density, T = temperature'''

        haprhoT = PhysicsConstants().get_air_prop(self.alt)

        min_alt = haprhoT[0]
        a = haprhoT[1]
        p_init = haprhoT[2]
        rho_init = haprhoT[3]
        T_init = haprhoT[4]

        g = PhysicsConstants.ACC_GRAVITY
        R = PhysicsConstants.GAS_CONSTANT_AIR

        if haprhoT[1] != 0: # use the formula where lapse rate is not 0
            p = p_init * (1 + a*self.alt/T_init) ** (-g/(a*R))
            rho = rho_init * (1 + a*self.alt/T_init) ** ((-g/(a*R)) - 1) 
            T= T_init + a * self.alt

            return p, rho, T

        else:  # used if lapse rate is 0
            p = p_init * np.exp(-(g/(R*T_init))*(self.alt - min_alt*1000))
            rho = rho_init * np.exp(-(g/(R*T_init))*(self.alt - min_alt*1000)) 
            T= T_init

            return p, rho, T


class AircraftAerodynamics:
    def __init__(self, 
                 lift_slope_0=0.07, 
                 cl_0=0.34, 
                 cd_paras=0.027, 
                 oswald_eff_factor=0.72,
                 wing_area=10.9, 
                 wing_span=9.91,  
                 alt=0,
                 **kwargs):
        super().__init__(**kwargs)
        self.lift_slope_0 = lift_slope_0
        self.cl_0 = cl_0
        self.cd_paras = cd_paras
        self.oswald_eff_factor = oswald_eff_factor
        self.wing_span = wing_span
        self.wing_area = wing_area
        self.alt = alt
        self.aspect_ratio = np.square(self.wing_span) / self.wing_area
        self.angle_of_attack = 0

    def cl(self):
        cl = self.cl_0 + self.angle_of_attack * self.lift_slope_0
        return cl
    
    def cd_total(self):
        cl = self.cl()
        A = self.aspect_ratio
        e = self.oswald_eff_factor
        cl_i = np.square(cl) / (np.pi * A * e)
        cd = self.cd_paras + cl_i
        return cd

    


