import pygame
from vector import *

SIM_WIDTH = 600
SIM_HEIGHT = 600
MARGIN = 20

class Boid:
    ALIGNMENT_PERCEPTION = 100
    COHESION_PERCEPTION = 150
    SEPARATION_PERCEPTION = 50
    ALIGNMENT_SCALE = 1
    COHESION_SCALE = 1
    SEPARATION_SCALE = 1
    MAX_VELOCITY = 6
    MAX_FORCE = 0.1
    TURN_FACTOR = 1

    # control max speed for avergage velocity of boids
    # reduce max force for bigger groups with more separation

    def __init__(self):
        self.position = Vector(randint(0,SIM_WIDTH), randint(0, SIM_WIDTH))
        self.velocity = Vector.random()
        self.velocity.setMag(self.MAX_VELOCITY)
        self.acceleration = Vector(x=0, y=0)
        self.type = randint(0, 1)

    def update(self):
        self.position += self.velocity
        self.velocity += self.acceleration
        self.velocity.limit(self.MAX_VELOCITY)
        self.acceleration.set(0, 0)

    def flock(self, flock):
        alignment = self.align(flock)
        cohesion = self.cohesion(flock)
        separation = self.separation(flock)

        alignment.multiply(self.ALIGNMENT_SCALE)
        cohesion.multiply(self.COHESION_SCALE)
        separation.multiply(self.SEPARATION_SCALE)

        self.acceleration.add(alignment)  # F = ma, but m = 1, then F = a
        self.acceleration.add(cohesion)
        self.acceleration.add(separation)

    def align(self, flock):
        steering = Vector()  # desired velocity, avg of boids withing perception
        num_boids_in_radius = 0
        for boid in flock:
            if boid is not self and self.getDistance(self.position, boid.position) <= self.ALIGNMENT_PERCEPTION\
                    and self.type == boid.type:
                num_boids_in_radius += 1
                steering.add(boid.velocity)
        if num_boids_in_radius > 0:
            steering.divide(num_boids_in_radius)
            steering.setMag(self.MAX_VELOCITY)
            steering.subtract(self.velocity)  # this is the steering force in direction of average
            steering.limit(self.MAX_FORCE)
        return steering

    def cohesion(self, flock):
        steering = Vector()  # desired location, avg of boids withing perception
        num_boids_in_radius = 0
        for boid in flock:
            if boid is not self and self.getDistance(self.position, boid.position) <= self.COHESION_PERCEPTION\
                    and self.type == boid.type:
                num_boids_in_radius += 1
                steering.add(boid.position)
        if num_boids_in_radius > 0:
            steering.divide(num_boids_in_radius)
            steering.subtract(self.position)
            steering.setMag(self.MAX_VELOCITY)
            steering.subtract(self.velocity)  # this is the steering force in direction of average
            steering.limit(self.MAX_FORCE)
        return steering

    def separation(self, flock):
        steering = Vector()  # desired location, avg of boids withing perception
        num_boids_in_radius = 0
        for boid in flock:
            distance = self.getDistance(self.position, boid.position)
            if boid is not self and distance < self.SEPARATION_PERCEPTION\
                    and self.type == boid.type:
                difference = self.position - boid.position
                difference.divide(distance)  # inversely proportional
                steering.add(difference)
                num_boids_in_radius += 1
        if num_boids_in_radius > 0:
            steering.divide(num_boids_in_radius)
            steering.setMag(self.MAX_VELOCITY)
            steering.subtract(self.velocity)  # this is the steering force in direction of average
            steering.limit(self.MAX_FORCE)
        return steering

    def checkBounds(self):
        if self.position.x > SIM_WIDTH - MARGIN:
            self.velocity.x -= self.TURN_FACTOR
        elif self.position.x < MARGIN:
            self.velocity.x += self.TURN_FACTOR
        if self.position.y > SIM_HEIGHT - MARGIN:
            self.velocity.y -= self.TURN_FACTOR
        elif self.position.y < MARGIN:
            self.velocity.y += self.TURN_FACTOR

    def getDistance(self, a, b):
        return sqrt((a.x-b.x)**2 + (a.y-b.y)**2)

    def draw(self, screen):
        if self.type == 0:
            pygame.draw.circle(screen, (30, 144, 255), (self.position.x, self.position.y), 4)
        else:
            pygame.draw.circle(screen, (75, 0, 130), (self.position.x, self.position.y), 4)