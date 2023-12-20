from __future__ import print_function


# ==============================================================================
# -- find carla module ---------------------------------------------------------
# ==============================================================================


import glob
import os
import sys

try:
    sys.path.append(glob.glob('../carla/dist/carla-*%d.%d-%s.egg' % (
        sys.version_info.major,
        sys.version_info.minor,
        'win-amd64' if os.name == 'nt' else 'linux-x86_64'))[0])
except IndexError:
    pass


# ==============================================================================
# -- imports -------------------------------------------------------------------
# ==============================================================================


import carla

from carla import ColorConverter as cc

import argparse
import collections
import datetime
import logging
import math
import random
import re
import weakref

try:
    import pygame
    from pygame.locals import KMOD_CTRL
    from pygame.locals import KMOD_SHIFT
    from pygame.locals import K_0
    from pygame.locals import K_9
    from pygame.locals import K_BACKQUOTE
    from pygame.locals import K_BACKSPACE
    from pygame.locals import K_COMMA
    from pygame.locals import K_DOWN
    from pygame.locals import K_ESCAPE
    from pygame.locals import K_F1
    from pygame.locals import K_LEFT
    from pygame.locals import K_PERIOD
    from pygame.locals import K_RIGHT
    from pygame.locals import K_SLASH
    from pygame.locals import K_SPACE
    from pygame.locals import K_TAB
    from pygame.locals import K_UP
    from pygame.locals import K_a
    from pygame.locals import K_c
    from pygame.locals import K_g
    from pygame.locals import K_d
    from pygame.locals import K_h
    from pygame.locals import K_m
    from pygame.locals import K_n
    from pygame.locals import K_p
    from pygame.locals import K_q
    from pygame.locals import K_r
    from pygame.locals import K_s
    from pygame.locals import K_w
    from pygame.locals import K_l
    from pygame.locals import K_i
    from pygame.locals import K_z
    from pygame.locals import K_x
    from pygame.locals import K_MINUS
    from pygame.locals import K_EQUALS
except ImportError:
    raise RuntimeError('cannot import pygame, make sure pygame package is installed')

try:
    import numpy as np
except ImportError:
    raise RuntimeError('cannot import numpy, make sure numpy package is installed')

# ==============================================================================
# -- code -------------------------------------------------------------------
# ==============================================================================
parked_locations = [
    carla.Transform(carla.Location(x=-77.0000, y=36.0000, z=1),
                    carla.Rotation(yaw=90.596336))
]

class CarlaParkVehicle():
    '''
    class responsable of:
        -spawning 3 vehicles of which one ego
        -interact with ROS and carla server
        -destroy the created objects
        -execute the parking manoeuvre
    '''
    def __init__(self):
        '''
        construct object CarlaParkVehicle with server connection and
        ros node initiation
        '''
        self.client = carla.Client('localhost',2000)
        self.client.set_timeout(10.0)
        # self.client.load_world('Town03')
        self.world = self.client.get_world()
        self.actor_list = []
        blueprint_library = self.world.get_blueprint_library()

        # create ego vehicle
        bp = random.choice(blueprint_library.filter('vehicle.tesla.model3'))
        self.ob_list = []
        # create 2 parked vehicles
        for pos in parked_locations:
            v = self.world.spawn_actor(bp, pos)
            self.actor_list.append(v)
            self.ob_list.append(v)

        print("--------------")

    def destroy(self):
        '''
        destroy all the actors
        '''
        print('destroying actors')
        for actor in self.actor_list:
            actor.destroy()
        print('done.')

    def run(self):
        '''
        main loop
        '''
        while True:
            pass

# ==============================================================================
# -- code -------------------------------------------------------------------
# ==============================================================================       

def main():
    '''
    main function
    '''
    ego_vehicle = CarlaParkVehicle()
    try:
        ego_vehicle.run()
    finally:
        if ego_vehicle is not None:
            ego_vehicle.destroy()

if __name__ == '__main__':
    main()