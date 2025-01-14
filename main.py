import pygame
import sys
import random

# Инициализация Pygame
pygame.init()

# Настройки окна
WINDOW_WIDTH, WINDOW_HEIGHT = 800, 600
screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption("Top-Down Shooter")

# Основные цвета
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
PLAYER_COLOR = (0, 255, 0)  # Зеленый цвет игрока
BULLET_COLOR = (255, 0, 0)  # Красный цвет пуль

# Частота обновления
clock = pygame.time.Clock()

# Звуки
shoot_sound = pygame.mixer.Sound("shoot.wav")
hit_sound = pygame.mixer.Sound("hit.wav")

class Player:
    """Класс для управления игроком."""
    def __init__(self, x: int, y: int) -> None:
        self.x = x
        self.y = y
        self.size = 25  # Размер квадрата игрока
        self.speed = 9

    def move(self, keys: pygame.key.ScancodeWrapper) -> None:
        if keys[pygame.K_w] or keys[pygame.K_UP]:
            self.y -= self.speed
        if keys[pygame.K_s] or keys[pygame.K_DOWN]:
            self.y += self.speed
        if keys[pygame.K_a] or keys[pygame.K_LEFT]:
            self.x -= self.speed
        if keys[pygame.K_d] or keys[pygame.K_RIGHT]:
            self.x += self.speed

        self.x = max(0, min(self.x, WINDOW_WIDTH - self.size))
        self.y = max(0, min(self.y, WINDOW_HEIGHT - self.size))

    def draw(self, surface: pygame.Surface) -> None:
        pygame.draw.rect(surface, PLAYER_COLOR, (self.x, self.y, self.size, self.size))

    def shoot(self) -> pygame.Rect:
        """Создает пулю, вылетающую из центра игрока."""
        bullet_x = self.x + self.size // 2 - 5  # Центр игрока
        bullet_y = self.y  # Пуля вылетает сверху
        return pygame.Rect(bullet_x, bullet_y, 10, 20)  # Размер пули


class Bullet:
    """Класс для управления пулями."""
    def __init__(self, rect: pygame.Rect) -> None:
        self.rect = rect
        self.speed = 10  # Скорость пули

    def update(self) -> None:
        """Обновляет положение пули (движение вверх)."""
        self.rect.y -= self.speed

    def draw(self, surface: pygame.Surface) -> None:
        """Отрисовка пули."""
        pygame.draw.rect(surface, BULLET_COLOR, self.rect)


class Enemy:
    """Класс для управления врагами."""
    def __init__(self, x: int, y: int) -> None:
        self.rect = pygame.Rect(x, y, 30, 30)  # Размер врага
        self.speed = random.randint(2, 5)  # Случайная скорость врага

    def update(self) -> None:
        """Обновляет положение врага (движение вниз)."""
        self.rect.y += self.speed

    def draw(self, surface: pygame.Surface) -> None:
        """Отрисовка врага."""
        pygame.draw.rect(surface, (255, 255, 0), self.rect)  # Желтый цвет врага


def display_score(surface: pygame.Surface, score: int) -> None:
    """Отображает текущий счет на экране."""
    font = pygame.font.Font(None, 36)
    score_text = font.render(f"Score: {score}", True, WHITE)
    surface.blit(score_text, (10, 10))


def game_over_screen() -> str:
    """Отображает экран Game Over и обрабатывает выбор игрока."""
    font = pygame.font.Font(None, 74)
    small_font = pygame.font.Font(None, 36)

    while True:
        screen.fill(BLACK)
        text = font.render("Game Over", True, WHITE)
        restart_text = small_font.render("Press R to Restart", True, WHITE)
        quit_text = small_font.render("Press Q to Quit", True, WHITE)

        screen.blit(text, (WINDOW_WIDTH // 2 - text.get_width() // 2, 200))
        screen.blit(restart_text, (WINDOW_WIDTH // 2 - restart_text.get_width() // 2, 300))
        screen.blit(quit_text, (WINDOW_WIDTH // 2 - quit_text.get_width() // 2, 350))

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    return "restart"
                if event.key == pygame.K_q:
                    pygame.quit()
                    sys.exit()


def main():
    """Главная функция игры."""
    player = Player(WINDOW_WIDTH // 2, WINDOW_HEIGHT - 50)
    bullets = []
    enemies = []
    enemy_spawn_timer = 0
    score = 0  # Счет игры

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:  # Стрельба
                    bullets.append(Bullet(player.shoot()))
                    shoot_sound.play()

        keys = pygame.key.get_pressed()
        player.move(keys)

        # Таймер врагов
        enemy_spawn_timer += 1
        if enemy_spawn_timer >= 60:
            enemies.append(Enemy(random.randint(0, WINDOW_WIDTH - 30), 0))
            enemy_spawn_timer = 0

        # Обновление врагов
        for enemy in enemies[:]:
            enemy.update()
            if enemy.rect.top > WINDOW_HEIGHT:
                enemies.remove(enemy)
            if enemy.rect.colliderect(pygame.Rect(player.x, player.y, player.size, player.size)):
                if game_over_screen() == "restart":
                    main()
                else:
                    running = False

        # Обновление пуль
        for bullet in bullets[:]:
            bullet.update()
            if bullet.rect.bottom < 0:
                bullets.remove(bullet)

            for enemy in enemies[:]:
                if bullet.rect.colliderect(enemy.rect):
                    enemies.remove(enemy)
                    bullets.remove(bullet)
                    hit_sound.play()
                    score += 1  # Увеличение счета
                    break

        # Отрисовка
        screen.fill(BLACK)
        player.draw(screen)
        for bullet in bullets:
            bullet.draw(screen)
        for enemy in enemies:
            enemy.draw(screen)
        display_score(screen, score)  # Отображение счета
        pygame.display.flip()
        clock.tick(60)

    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    main()
