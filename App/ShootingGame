import pygame
import random

# Initialize pygame
pygame.init()

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

# Screen dimensions
WIDTH = 800
HEIGHT = 600

# Create the screen and clock
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Shooting Game")
clock = pygame.time.Clock()

# Define the Player class
class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface([50, 30])
        self.image.fill(BLACK)
        self.rect = self.image.get_rect()
        self.rect.x = WIDTH // 2
        self.rect.y = HEIGHT - 40
        self.change_x = 0
        self.damage = 0
        self.invincible_time = 0  # Time remaining for invincibility

    def update(self):
        self.rect.x += self.change_x
        if self.rect.x < 0:
            self.rect.x = 0
        if self.rect.x > WIDTH - 50:
            self.rect.x = WIDTH - 50

        # Reduce invincibility time if greater than 0
        if self.invincible_time > 0:
            self.invincible_time -= 1

    def go_left(self):
        self.change_x = -5

    def go_right(self):
        self.change_x = 5

    def stop(self):
        self.change_x = 0

    def take_damage(self):
        if self.invincible_time == 0:
            self.damage += 1
            self.invincible_time = 60  # Set invincibility for 1 second (60 frames)
            if self.damage >= 3:
                return True
        return False

# Define the Bullet class
class Bullet(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.Surface([5, 10])
        self.image.fill(BLACK)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

    def update(self):
        self.rect.y -= 5

# Define the Meteor class
class Meteor(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface([40, 25])
        self.image.fill(BLACK)
        self.rect = self.image.get_rect()
        self.rect.x = random.randint(0, WIDTH - 40)
        self.rect.y = random.randint(-100, -40)
        self.speed_y = random.randint(1, 3)

    def update(self):
        self.rect.y += self.speed_y
        if self.rect.y > HEIGHT:
            self.rect.y = random.randint(-100, -40)
            self.rect.x = random.randint(0, WIDTH - 40)

# New Score class
class Score():
    def __init__(self):
        self.score = 0
        self.font = pygame.font.SysFont(None, 36)

    def draw(self, screen):
        score_text = self.font.render("Score: " + str(self.score), True, BLACK)
        damage_text = self.font.render(f"Damage: {player.damage}/3", True, BLACK)
        screen.blit(score_text, (10, 10))
        screen.blit(damage_text, (WIDTH - 150, 10))

    def add(self, points):
        self.score += points

player = Player()
all_sprites = pygame.sprite.Group()
all_sprites.add(player)

bullets = pygame.sprite.Group()
meteors = pygame.sprite.Group()

for i in range(5):
    meteor = Meteor()
    all_sprites.add(meteor)
    meteors.add(meteor)

score = Score()

running = True
game_over = False
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                player.go_left()
            elif event.key == pygame.K_RIGHT:
                player.go_right()
            elif event.key == pygame.K_SPACE:
                bullet = Bullet(player.rect.x + 22, player.rect.y)
                all_sprites.add(bullet)
                bullets.add(bullet)
        elif event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                player.stop()

    all_sprites.update()

    bullet_meteor_hit_list = pygame.sprite.groupcollide(bullets, meteors, True, True)
    
    # Check player-meteor collisions
    if pygame.sprite.spritecollideany(player, meteors) and player.take_damage():
        game_over = True
        running = False

    for hit in bullet_meteor_hit_list:
        meteor = Meteor()
        all_sprites.add(meteor)
        meteors.add(meteor)
        score.add(10)

    screen.fill(WHITE)
    all_sprites.draw(screen)
    score.draw(screen)

    # Check for game clear condition
    if score.score >= 100:
        font = pygame.font.SysFont(None, 74)
        clear_text = font.render("Game Clear!", True, BLACK)
        screen.blit(clear_text, (WIDTH//2 - 100, HEIGHT//2 - 37))

    pygame.display.flip()

    clock.tick(60)

if game_over:
    font = pygame.font.SysFont(None, 74)
    game_over_text = font.render("Game Over!", True, BLACK)
    screen.fill(WHITE)
    screen.blit(game_over_text, (WIDTH//2 - 100, HEIGHT//2 - 37))
    pygame.display.flip()
    pygame.time.wait(3000)  # Display the game over message for 3 seconds

pygame.quit()
