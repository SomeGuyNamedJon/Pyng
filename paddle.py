import pygame
pygame.init()

PADDLE_DIMENSIONS = ((50, 175))
BASE_COLOR = (200,200,200)
HIT_COLOR = (255,255,255)
POINT_COLOR = (230, 255, 235)
LOSS_COLOR = (230, 180, 200)
BASE_SPEED = 10
BASE_FOLLOW = 150

def map_value_range(n, a, b):
    k = (n/a) * b
    return k

class Paddle(pygame.sprite.Sprite):
    def __init__(self, pos_x, pos_y, sound):
        pygame.sprite.Sprite.__init__(self)
        
        self.sound = sound
        self.position = (pos_x, pos_y)
        self.image = pygame.Surface(PADDLE_DIMENSIONS)
        self.image.fill(BASE_COLOR)
        self.rect = self.image.get_rect()
        self.rect.center = self.position

        self.react_duration = 300
        self.react_start_time = 0
        self.reacted = False

    def draw(self, screen):
        screen.blit(self.image, self.rect)


    def handleBoundry(self, dimensions):
        (_, height) = dimensions
        if(self.rect.top <= 0):
            self.rect.top = 0
        if(self.rect.bottom >= height):
            self.rect.bottom = height

    def clearHit(self):
        current_time = pygame.time.get_ticks()
        elapsed_time = current_time - self.react_start_time

        if self.reacted and elapsed_time >= self.react_duration:
            self.image.fill(BASE_COLOR)
            self.reacted = False

    def reactHit(self):
        current_time = pygame.time.get_ticks()
        if not self.reacted:
            self.sound.play()
            self.image.fill(HIT_COLOR)
            self.react_start_time = current_time
            self.reacted = True

    def handleCollision(self, ball):
        if(self.rect.colliderect(ball)):
            self.reactHit()
            ball.paddleHit(self)

    def update(self, ball, dimensions):
        self.handleCollision(ball)
        self.clearHit()
        self.rect.center = self.position
        self.handleBoundry(dimensions)

class PlayerPaddle(Paddle):
    def update(self, mouse_pos, ball, dimensions):
        (_, mouse_y) = mouse_pos
        self.position = (self.position[0], mouse_y)
        super().update(ball, dimensions)

class EnemyPaddle(Paddle):
    def __init__(self, pos_x, pos_y, sound):
        super().__init__(pos_x, pos_y, sound)
        self.speed = BASE_SPEED
        self.follow_gap = BASE_FOLLOW

        # AI INFLUENCE INDICATORS
        self.ai_top = pygame.Surface((200,5))
        self.ai_top_rect = self.ai_top.get_rect()
        self.ai_top.fill((255, 0, 0))
        self.ai_top_rect.center = (pos_x, self.rect.top)
        
        self.ai_bottom = pygame.Surface((200,5))
        self.ai_bottom_rect = self.ai_bottom.get_rect()
        self.ai_bottom.fill((255, 0, 0))
        self.ai_bottom_rect.center = (pos_x, self.rect.bottom)

    #def draw(self, screen):
    #    screen.blit(self.ai_top, self.ai_top_rect)
    #    screen.blit(self.ai_bottom, self.ai_bottom_rect)
    #    return super().draw(screen)

    def updateXPOS(self, width):
        self.position = (width - 50, self.position[1])

    def update(self, ball, dimensions):
        (width, height) = dimensions
        self.updateXPOS(width)

        (ball_x, ball_y) = ball.position
        distance = self.rect.left - ball_x
        direction = 0
        base_speed = BASE_SPEED + (1/width)*100 + (-1/height)*100
        base_follow = BASE_FOLLOW * map_value_range(height, 540, 1)

        # AI DEBUG BOUNDS
        self.ai_top_rect.right = self.ai_bottom_rect.right = self.rect.right
        self.ai_top_rect.top = self.rect.centery - self.follow_gap
        self.ai_bottom_rect.top = self.rect.centery + self.follow_gap
    
        if(distance <= 0):
            distance = 0
            step = 0
        else:
            step = (BASE_SPEED/(distance*10))

        
        self.follow_gap = map_value_range(distance, width//2, base_follow)
        
        if(self.rect.left < ball_x):
            self.follow_gap = base_follow
            self.speed = 0
        if(self.follow_gap <= 0):
            self.follow_gap = 0

        if(self.rect.centery - self.follow_gap < ball_y < self.rect.centery + self.follow_gap):
            direction = 0
            self.speed = base_speed
        elif(self.rect.centery > ball_y):
            direction = -1
            self.speed += step
        elif(self.rect.centery < ball_y):
            direction = 1
            self.speed += step

        if(ball.direction[0] > 0):
            self.position = (self.position[0], self.position[1]+(self.speed*direction))

        super().update(ball, dimensions)