from boid import *

# Window
SIM_WIDTH = 600
SIM_HEIGHT = 600
WIN_WIDTH = 600
WIN_HEIGHT = 800
MARGIN = 10

flock = []

def setup():
    for _ in range(50):
        flock.append(Boid(0))
    for _ in range(50):
        flock.append(Boid(1))
    for _ in range(1):
        flock.append(Boid(2))

def drawWindow(screen):
    screen.fill((255, 255, 255))
    for boid in flock:
        boid.draw(screen)
    pygame.display.update()

def main():
    running = True
    screen = pygame.display.set_mode((WIN_WIDTH, WIN_HEIGHT))
    clock = pygame.time.Clock()
    pygame.display.set_caption("Boids")

    setup()

    while running:
        clock.tick(30)

        # event listening
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                pygame.quit()
                quit()

        for boid in flock:
            boid.checkBounds()  # checks for out of bounds boids
            boid.flock(flock)  # set acceleration
            boid.update()  # updates positions

        drawWindow(screen)

    pygame.quit()
    quit()

main()