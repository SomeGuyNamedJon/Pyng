import pygame
pygame.init()

PADDLE_DIMENSIONS = ((50, 175))
BASE_COLOR = (200,200,200)
HIT_COLOR = (255,255,255)
POINT_COLOR = (230, 255, 235)
LOSS_COLOR = (230, 180, 200)
BASE_VELOCITY = 3

class Paddle(pygame.sprite.Sprite):
    def __init__(self, pos_x, pos_y):
        pygame.sprite.Sprite.__init__(self)

        self.position = (pos_x, pos_y)
        self.name = ""
        self.image = pygame.Surface(PADDLE_DIMENSIONS)
        self.image.fill(BASE_COLOR)
        self.rect = self.image.get_rect()
        self.rect.center = self.position


    def draw(self, screen):
        screen.blit(self.image, self.rect)

    def handleBoundry(self, height):
        if(self.rect.top <= 0):
            self.rect.top = 0
        if(self.rect.bottom >= height):
            self.rect.bottom = height

    def handleCollision(self, ball):
        if(self.rect.colliderect(ball)):
            ball.paddleHit(self)

    def update(self, ball):
        self.handleCollision(ball)
        self.rect.center = self.position
        self.handleBoundry(540)

class PlayerPaddle(Paddle):
    def __init__(self, pos_x, pos_y):
        super().__init__(pos_x, pos_y)
        self.name = "player"

    def update(self, mouse_pos, ball):
        (_, mouse_y) = mouse_pos
        self.position = (self.position[0], mouse_y)
        super().update(ball)

class EnemyPaddle(Paddle):
    
    def __init__(self, pos_x, pos_y):
        super().__init__(pos_x, pos_y)
        self.velocity = BASE_VELOCITY
        self.name = "enemy"

    def update(self, ball):
        (ball_x, ball_y) = ball.position
        (x, y) = self.position
        distance = x - ball_x

        if(distance <= 0):
            step = 0
        else:
            step = (BASE_VELOCITY/(distance+1)) * 10

        if(self.rect.top < ball_y < self.rect.bottom):
            self.velocity = BASE_VELOCITY
        if(y > ball_y):
            self.position = (x, y-self.velocity)
            self.velocity += step
        if(y < ball_y):
            self.position = (x, y+self.velocity)
            self.velocity += step

        super().update(ball)