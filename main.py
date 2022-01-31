from cmath import sin, cos, sqrt
from math import radians
import pygame
import random
from pygame import Vector2

WIDTH, HEIGHT = 1020, 720
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Sinai billiard Simulation")

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
BLUE = (30, 144, 255)

FPS = 120


def get_distance_sqr(P: Vector2, Q: Vector2):
    return (P.x - Q.x) ** 2 + (P.y - Q.y) ** 2

def get_distance(P: Vector2, Q: Vector2):
    return sqrt(get_distance_sqr(P, Q)).real


class Balls():
    def __init__(self, color=WHITE, x=0, y=0, r=1, vel_x=0, vel_y=0):
        self.color = color
        self.x = x
        self.y =  y
        self.radius = r

        self.velocity = Vector2(vel_x, vel_y)
        pass

    def draw(self):
        pygame.draw.circle(
            WIN, 
            self.color, 
            (self.x, self.y), 
            self.radius
        )
    
    def move(self):
        self.x += self.velocity.x
        self.y += self.velocity.y

    def check_out_of_bound(self) -> bool:
        is_collision = False
        if self.x - self.radius <= 0 or self.x + self.radius >= WIDTH:
            self.velocity.x = -self.velocity.x
            is_collision = True
        if self.y - self.radius <= 0 or self.y + self.radius >= HEIGHT:
            self.velocity.y = -self.velocity.y
            is_collision = True
        return is_collision

    def check_collision(self, other_ball) -> bool:
        is_collision = False
        pos_this = Vector2(self.x, self.y)
        pos_other = Vector2(other_ball.x, other_ball.y)
        if get_distance(pos_this, pos_other) <= self.radius + other_ball.radius:
            velocity_vector = pos_this - pos_other
            angle = radians(velocity_vector.as_polar()[1])
            x_comp = self.velocity.length() * cos(angle).real
            y_comp = self.velocity.length() * sin(angle).real
            self.velocity = Vector2(x_comp, y_comp)
            is_collision = True
        return is_collision


def draw_window():
    WIN.fill(BLACK)


def random_ball(obstacle: Balls):
    x, y = random.randint(10, WIDTH - 10), random.randint(10, HEIGHT - 10)
    while get_distance(Vector2(x, y), Vector2(obstacle.x, obstacle.y)) <= obstacle.radius:
        x, y = random.randint(10, WIDTH - 10), random.randint(10, HEIGHT - 10)
    return Balls(
        color=WHITE,
        x=x,
        y=y,
        r=10,
        vel_x=random.randint(-10, 10),
        vel_y=random.randint(-10, 10)
    )


def main():

    obstacle = Balls(
        color=BLUE,
        x=WIDTH // 2,
        y=HEIGHT // 2,
        r=200,
        vel_x=0,
        vel_y=0
    )

    ball = random_ball(obstacle)

    print(f"""
    BALL INFO:
        color              = {ball.color},\n
        pos_x              = {ball.x},\n
        pos_y              = {ball.y},\n
        radius             = {ball.radius},\n
        initial_velocity_x = {ball.velocity.x},\n
        initial_velocity_y = {ball.velocity.y},\n
        speed              = {ball.velocity.length()}
    """)

    clock = pygame.time.Clock()
    run = True
    while run:
        clock.tick(FPS)
        for event in  pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

        draw_window()

        obstacle.draw()
        
        ball.draw()
        ball.move()
        ball.check_out_of_bound()
        ball.check_collision(obstacle)

        pygame.display.update()
    
    pygame.quit()


if __name__ == "__main__":
    main()
