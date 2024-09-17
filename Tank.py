from Image import Image
from Bullet import Bullet
from Muzzle import Muzzle
from math import acos

import pygame

class Tank(pygame.sprite.Sprite):
    def __init__(self, window, image, direction, speed, size, position, *args):
        super().__init__()
        self.window = window
        self.img = Image(image)
        self.img.resize(size)
        self._direction = pygame.math.Vector2(direction)
        self.rect = self.img.img.get_rect()
        self.speed = speed
        self.position = pygame.math.Vector2(position)
        self.tank_width = self.rect.width
        self.tank_height = self.rect.height

        self._transform_direction = pygame.math.Vector2((0, 1))
        self._normal_vector = pygame.math.Vector2((0, 1))

        self.move_stop = False
        self._is_live = True

        self.muzzle = Muzzle(window, self._direction, pygame.math.Vector2(self.position.x, self.position.y - (self.tank_height // 2) - 4),
                             self.position, 10, speed)

        self._live = 3
        self._hit_event = args[0]
        self._dead_event = args[1]

        self.path_img = image

    @property
    def direction(self):
        return self._direction

    @direction.setter
    def direction(self, val):
        self._direction = pygame.math.Vector2(val)
        self.muzzle.direction = val

    @property
    def transform_direction(self):
        return self._transform_direction

    @transform_direction.setter
    def transform_direction(self, val):
        self._transform_direction = pygame.math.Vector2(val)

    @property
    def normal_vector(self):
        return self._normal_vector

    @property
    def is_live(self):
        return self._is_live

    @is_live.setter
    def is_live(self, val):
        if val is False:
            pygame.event.post(pygame.event.Event(self._dead_event))
        self._is_live = val

    @property
    def live(self):
        return self._live

    @live.setter
    def live(self, val):
        if self._live - val > 0:
            self._live -= val
            pygame.event.post(pygame.event.Event(self._hit_event))
        else:
            self.is_live = False

    def fire(self):
        return Bullet(self, self.window)

    def display(self):
        self.muzzle.display()
        self.window.blit(self.img.img, self.rect)

    def move(self):
        if self.move_stop is False:
            self.position += (self.direction * self.speed)
            self.muzzle.move()
            self.rect.center = round(self.position.x), round(self.position.y)
            self.muzzle.rect_pivot = self.rect
            self.rotate()

    def rotate(self):
        angle = self._transform_direction.angle_to(self._normal_vector)
        self.img.rotate(angle)
        self.muzzle.angle = angle
        self._normal_vector = self._transform_direction

    def reflect(self):
        self.direction = self.direction * -1
        self.move()

    def set_new_position(self, position):
        self._transform_direction = pygame.math.Vector2((0, 1))
        self.rotate()

        self.position = pygame.math.Vector2(position)
        self.rect.center = round(self.position.x), round(self.position.y)
        self.muzzle = Muzzle(self.window, self._direction, pygame.math.Vector2(self.position.x, self.position.y - (self.tank_height // 2) - 4),
                             self.position, 10, self.speed)
