import pygame
pygame.init()

PADDLE_DIMENSIONS = ((50, 175))
BASE_COLOR = (200,200,200)
HIT_COLOR = (255,255,255)
POINT_COLOR = (230, 255, 235)
LOSS_COLOR = (230, 180, 200)

class Paddle(pygame.sprite.Sprite):
    def __init__(self, pos_x, pos_y):
        pygame.sprite.Sprite.__init__(self)

        self.position = (pos_x, pos_y)

        self.image = pygame.Surface(PADDLE_DIMENSIONS)
        self.image.fill(BASE_COLOR)
        self.rect = self.image.get_rect()
        self.rect.center = self.position


    def draw(self, screen):
        screen.blit(self.image, self.rect)

    def handleBoundry(self, dimensions):
        (width, height) = dimensions

    def checkCollision(self, ball):
        if(self.rect.colliderect(ball)):
            ball.paddleHit(self)

    def update(self, ball):
        self.checkCollision(ball)
        self.rect.center = self.position

class PlayerPaddle(Paddle):
    def update(self, mouse_pos, ball):
        (_, mouse_y) = mouse_pos
        self.position = (self.position[0], mouse_y)
        super().update(ball)

class EnemyPaddle(Paddle):
    def update(self, ball):
        (_, ball_y) = ball.position
        self.position = (self.position[0], ball_y)
        super().update(ball)