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


class Player:
    """Класс для управления игроком."""

    def __init__(self, x: int, y: int) -> None:
        self.x = x
        self.y = y
        self.size = 25  # Размер квадрата игрока
        self.speed = 7

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
        """
        Создает пулю, вылетающую из центра игрока.

        Returns:
            pygame.Rect: Прямоугольник, представляющий пулю.
        """
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


def main():
    """Главная функция игры."""
    # Создаем игрока
    player = Player(WINDOW_WIDTH // 2, WINDOW_HEIGHT - 50)
    bullets = []  # Список для хранения пуль
    enemies = []  # Список для хранения врагов
    enemy_spawn_timer = 0  # Таймер для появления врагов
    score = 0  # Переменная для подсчета очков

    # Настройки шрифта для отображения счета
    font = pygame.font.SysFont(None, 36)

    running = True
    while running:
        # Обработка событий
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:  # Стрельба при нажатии пробела
                    bullets.append(Bullet(player.shoot()))

        # Получаем состояние клавиш
        keys = pygame.key.get_pressed()

        # Обновление логики
        player.move(keys)

        # Обновляем таймер появления врагов
        enemy_spawn_timer += 1
        if enemy_spawn_timer >= 60:  # Каждые 60 кадров появляется враг
            x_position = random.randint(0, WINDOW_WIDTH - 30)  # Случайная позиция
            enemies.append(Enemy(x_position, 0))
            enemy_spawn_timer = 0

        # Обновление врагов
        for enemy in enemies[:]:
            enemy.update()
            if enemy.rect.top > WINDOW_HEIGHT:  # Удаляем врагов, если они выходят за экран
                enemies.remove(enemy)
            if enemy.rect.colliderect(player.x, player.y, player.size, player.size):
                running = False  # Завершаем игру, если враг касается игрока

        # Обновление пуль
        for bullet in bullets[:]:
            bullet.update()
            if bullet.rect.bottom < 0:  # Удаляем пулю, если она вышла за верх экрана
                bullets.remove(bullet)

            # Проверяем столкновения пуль с врагами
            for enemy in enemies[:]:
                if bullet.rect.colliderect(enemy.rect):  # Столкновение
                    enemies.remove(enemy)  # Удаляем врага
                    bullets.remove(bullet)  # Удаляем пулю
                    score += 1  # Увеличиваем счет
                    break

        # Отрисовка
        screen.fill(BLACK)  # Очищаем экран
        player.draw(screen)  # Рисуем игрока
        for bullet in bullets:  # Рисуем все активные пули
            bullet.draw(screen)
        for enemy in enemies:  # Рисуем всех врагов
            enemy.draw(screen)

        # Отображение счета
        score_text = font.render(f"Score: {score}", True, WHITE)
        screen.blit(score_text, (10, 10))

        pygame.display.flip()  # Обновляем экран

        # Ограничение FPS
        clock.tick(60)

    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    main()