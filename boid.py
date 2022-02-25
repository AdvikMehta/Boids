import pygame
from vector import *

SIM_WIDTH = 600
SIM_HEIGHT = 600

class Boid:
    def __init__(self):
        self.position = Vector(x=SIM_WIDTH//2, y=SIM_HEIGHT//2)
        self.velocity = Vector(x=0, y=0)
        self.acceleration = Vector(x=0, y=0)

    def update(self):
        self.position += self.velocity
        self.velocity += self.acceleration

    def draw(self, screen):
        pygame.draw.circle(screen, (51, 204, 255), (self.position.x, self.position.y), 4)