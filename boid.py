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
    TURN_FACTOR = 0.8

    COLORS = [((135, 206, 250), (30, 144, 255)),
              ((216, 191, 216), (75, 0, 130)),
              ((204, 0, 0), (204, 0, 0))]

    # control max speed for avergage velocity of boids
    # reduce max force for bigger groups with more separation

    def __init__(self, boid_type):
        # boid mechanics
        self.position = Vector(randint(0,SIM_WIDTH), randint(0, SIM_WIDTH))
        self.velocity = Vector.random()
        self.velocity.setMag(self.MAX_VELOCITY)
        self.acceleration = Vector(x=0, y=0)
        self.type = boid_type
        self.prev_position = self.position
        self.colors = self.COLORS[self.type]

    def update(self):
        self.velocity += self.acceleration
        self.velocity.limit(self.MAX_VELOCITY)
        self.position += self.velocity
        self.acceleration.set(0, 0)

    def flock(self, flock):
        alignment = self.alignment(flock)
        cohesion = self.cohesion(flock)
        separation = self.separation(flock)

        alignment.multiply(self.ALIGNMENT_SCALE)
        cohesion.multiply(self.COHESION_SCALE)
        separation.multiply(self.SEPARATION_SCALE)

        self.acceleration.add(alignment)  # F = ma, but m = 1, then F = a
        self.acceleration.add(cohesion)
        self.acceleration.add(separation)

    def alignment(self, flock):
        steering = Vector()  # desired velocity, avg of boids withing perception
        num_boids_in_radius = 0
        for boid in flock:
            if boid is not self and Vector.getDistance(self.position, boid.position) <= self.ALIGNMENT_PERCEPTION\
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
            if boid is not self and Vector.getDistance(self.position, boid.position) <= self.COHESION_PERCEPTION:
                if self.type == boid.type:
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
            distance = Vector.getDistance(self.position, boid.position)
            if boid is not self and distance < self.SEPARATION_PERCEPTION:
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

    def draw(self, screen):
        copy = Vector(self.velocity.x, self.velocity.y)
        copy.setMag(8)
        relative_next = self.position + copy
        copy.setMag(4)
        relative_prev = self.position - copy
        pygame.draw.line(screen, (0, 0, 0), (self.position.x, self.position.y), (relative_next.x, relative_next.y))

        pygame.draw.circle(screen, self.colors[0], (relative_prev.x, relative_prev.y), 4)
        pygame.draw.circle(screen, self.colors[1], (self.position.x, self.position.y), 4)