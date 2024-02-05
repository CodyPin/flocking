import math
import random

import pygame

from boid import Boid

width = 1280
height = 1280
boids = []
boid_count = 100
min_vector = -2
max_vector = 2
local_area = 75
closest = 4
res = 5


def draw(x, y):
    pygame.draw.polygon(screen, "azure4", [(x, y + res * 2), (x + res, y), (x - res, y)])


def steer(b):
    p_sum = pygame.Vector2()
    v_sum = pygame.Vector2()
    count = 0
    for boid in boids:
        if math.sqrt((boid.p.x - b.p.x) ** 2 + (boid.p.y - b.p.y) ** 2) <= local_area:
            if boid != b:
                count += 1
                p_sum += boid.p
                v_sum += boid.v

    if count == 0:
        return

    # Separation
    sep_v = (p_sum - b.p) / count
    # Cohesion
    # coh_v = p_sum / count
    # Alignment
    alig_v = (v_sum - b.v) / count

    total_v = sep_v + alig_v

    if total_v.x > max_vector:
        total_v.x = max_vector
    elif total_v.x < min_vector:
        total_v.x = min_vector

    if total_v.y > max_vector:
        total_v.y = max_vector
    if total_v.y < min_vector:
        total_v.y = min_vector

    b.v = total_v

    return


if __name__ == '__main__':
    # pygame setup
    pygame.init()
    screen = pygame.display.set_mode((width, height))
    clock = pygame.time.Clock()
    running = True

    # Set the window title
    pygame.display.set_caption("Flocking Simulation")

    # Generate boids
    for i in range(boid_count):
        p = pygame.Vector2()
        p.x = random.randint(0, width)
        p.y = random.randint(0, height)
        v = pygame.Vector2()
        v.x = random.randint(min_vector, max_vector)
        v.y = random.randint(min_vector, max_vector)

        boids.append(Boid(p, v))

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        screen.fill("cadetblue2")

        # Render boid
        for boid in boids:
            steer(boid)

            draw(boid.p.x % width, boid.p.y % height)
            boid.p.x = boid.p.x + boid.v.x + random.randint(-1, 1)
            boid.p.y = boid.p.y + boid.v.y + random.randint(-1, 1)

        # flip() the display to put your work on screen
        pygame.display.flip()

        clock.tick(60)

    pygame.quit()
